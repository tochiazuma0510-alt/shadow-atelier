#!/usr/bin/env python3
"""R07 A4/v6 independent checker: frozen core plus physical-owner gate.

This version remains fail-closed while the complete 48-route physical owner
registry is absent; no shallow mutation result is treated as acceptance.

This file deliberately has no import edge to the producer.  It authenticates
the same authority files, reads the pinned quotient source only as a physical
identity (the collector below is checker-owned), evaluates an opposite
(right-associated) suffix DAG, and rebuilds the raw B/K closure and action
matrices itself.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-word-independent-successor-kernel/v6"
PASS = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
HARD_STOP = "HARD_STOP"
PRE_AUTHORITY_STATE = "PRE_AUTHORITY"
ROWS = 6441
LAYERS = {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}
PRESENTATION_SCHEMA = "d972-r07-seven-context-roof-presentation/v1"
MANIFEST_SCHEMA = PRESENTATION_SCHEMA + "/acceptance-manifest/v3"
AUTH = {
    "receipt": "d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}
TASK176 = {
    "receipt": ("ci/in/d972_r07_all_seven_extension_section_census_v1.json", 13649089,
                "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41"),
    "manifest": ("ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json", 349,
                 "de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1"),
    "producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                 "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980,
                "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    # Bind the artifact's independent checker result to a physical file.  A
    # digest quoted only by the old reply is not an owner and must fail closed.
    "checker_result": ("ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json", 757,
                        "e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5"),
    "recovery_manifest_v1": ("ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.json", 2035,
                              "41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8"),
    "recovery_manifest": ("ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.v2.json", 2690,
                           "67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f"),
}
TASK198 = {
    "producer": ("search/d972_r07_seven_context_roof_presentation_v1.py", 137169,
                 "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"),
    "checker": ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", 157253,
                "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"),
    "driver": ("search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", 20541,
               "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"),
}
RECEIPT_SHA = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
RECEIPT_BYTES = 31017244
MANIFEST_SHA = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
VERDICT_SHA = "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"
E4_SOURCE = ("search/d972_b345_seedspan_triple4_v1.py", 535219,
             "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29")
Q3_SOURCE = ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
             "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72")
PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v6.py"
CONTEXT_IDS = (21, 22, 23, 24, 25, 1, 27, 21, 26, 28)
CONTEXT_TYPES = ("E3", "E3", "E3", "E3", "E3", "E4", "E4", "E4", "E4", "E4")
CONTEXT_TAGS = ("E3-C21", "E3-C22", "E3-C23", "E3-C24", "E3-C25",
                "E4-C1", "E4-C27", "E4-C21", "E4-C26", "E4-C28")
CAPS = {
    "wall_seconds": 14400, "rss_bytes": 8000000000, "input_bytes": 500000000,
    "serialized_bytes": 2000000000, "canonicalization": 100000000,
    "final_write": 2, "suffix_nodes": 50000, "suffix_edges": 50000,
    "row_assemblies": ROWS, "literal_comparisons": 6000000,
    "suffix_edge_state_products": 300000, "row_piece_products": 30000,
    "typed_context_products": 1000000, "quotient_reductions": 100000000,
    "affine_sparse_ops": 100000000, "membership_queries": 200000,
    "membership_reductions": 50000000, "dual_support": 10000000,
    "correlation_pairs": 10000000, "boundary_rank_rises": 1000000,
    "queue_actions": 500000, "word_nodes": 2000000,
    "expanded_letters": 4000000, "direct_replays": 100000,
    "bridge_rows": ROWS, "bridge_occurrences": ROWS * 11,
    "checkpoint_total_bytes": 2000000000, "checkpoint_peak_bytes": 400000000,
    "active_keys": 10000000, "restore_validation": 100000000,
    # A bounded typed transport channel remains usable after a normal cap
    # raises, allowing a truthful UNKNOWN/HARD certificate to be emitted.
    "terminal_canonicalization": 64, "terminal_checkpoint_bytes": 400000000,
    "terminal_serialized_bytes": 16000000,
    "terminal_final_write": 1,
}
OBJECT_CAPS = {"checkpoint_current_bytes": 400000000}
MUTATIONS = (
    "per_layer_ordinal", "authority_binding", "canonical_input_bytes",
    "resolved_path_traversal", "normal_generation_proof",
    "bridge_typed_occurrence_ledger", "evaluator_abi_canary",
    "raw_boundary_coefficient", "live_echelon_inherited_scale",
    "producer_checker_basis_change", "conjugator_order",
    "source_word_basis_boundary_difference", "negative_dual", "action_matrix",
    "projected_h2_exponent", "k_z_inverse_scalar_powered_word",
    "live_resource_cap", "positive_status_terminal", "nonpositive_false_progress",
    "duplicate_markers", "inconsistent_section_word", "altered_primitive_terminal",
    "wrong_trie_edge_orientation", "wrong_action_orientation", "wrong_target_inverse",
    "producer_checker_row_mismatch", "missing_base_boundary", "changed_boundary_block_tag",
    "left_right_translation_swap", "omitted_inverse_action", "changed_parent_action_ancestry",
    "incomplete_queue_claim", "wrong_support_inversion_product", "false_zero_correlation",
    "omitted_candidate_discrepancy", "omitted_prior_k_discrepancy", "flipped_q_sign",
    "missing_discrepancy_scale", "reversed_source_action_discrepancy",
    "changed_raw_tag_translation", "modulo_discovered_b_only_replay", "deleted_active_key",
    "unregistered_dual_key", "raw_pivot_functional", "omitted_matching_occurrence",
    "incomplete_translation_key", "premature_zero_correlation", "omitted_new_key_registration",
)
OWNERS = dict(zip(MUTATIONS, (
    "authority.layer_ordinal", "authority.acceptance_manifest", "authority.canonical_bytes",
    "authority.resolved_containment", "authority.normal_generation_proof",
    "authority.bridge_occurrence_ledger", "authority.evaluator_abi_canary",
    "echelon.raw_boundary_replay", "echelon.inherited_scale",
    "checker.producer_checker_basis_change", "ancestry.outer_first_conjugation",
    "boundary.source_word_difference", "dual.negative_functional", "closure.action_matrix",
    "anchor.projected_h2_exponent", "anchor.inverse_scalar_powered_word",
    "resource.live_cap_witness", "terminal.positive_status", "terminal.false_progress",
    "driver.duplicate_markers", "ancestry.section_word_replay", "trie.primitive_terminal",
    "trie.forward_edge_orientation", "ancestry.action_orientation", "ancestry.target_inverse",
    "checker.typed_row_equality", "boundary.base_seed_roster", "boundary.block_tag",
    "boundary.translation_orientation", "boundary.inverse_action_queue",
    "boundary.parent_action_ancestry", "boundary.queue_exhaustion",
    "dual.support_inversion_product", "dual.complete_zero_correlation",
    "discrepancy.omitted_candidate_E", "discrepancy.omitted_prior_K_E",
    "discrepancy.flipped_Q_sign", "discrepancy.missing_scale",
    "discrepancy.reversed_source_action", "discrepancy.changed_raw_tag_translation",
    "discrepancy.modulo_B_only_replay", "dual.deleted_active_key",
    "dual.unregistered_nonzero_key", "dual.raw_pivot_functional",
    "dual.omitted_matching_occurrence", "dual.incomplete_translation_key",
    "dual.premature_zero_correlation", "dual.omitted_new_key_registration",
)))


class Reject(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float, limit: int | float, state: str):
        self.phase, self.cap, self.value, self.limit, self.state = phase, cap, value, limit, state
        super().__init__(f"{phase}:{cap}:{value}>{limit}:state={state}")


class HardStop(RuntimeError):
    pass


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def jsonable(value: Any) -> Any:
    if isinstance(value, bytes): return {"__bytes__": value.hex()}
    if isinstance(value, tuple): return [jsonable(x) for x in value]
    if isinstance(value, list): return [jsonable(x) for x in value]
    if isinstance(value, set): return sorted(jsonable(x) for x in value)
    if isinstance(value, dict): return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (str, int, bool)) or value is None: return value
    return repr(value)


KEYS: dict[str, Any] = {}
LIVE_STATE: dict[str, Any] = {}
# Checker-owned primitive registry: each literal is reduced and authenticated
# once during inventory construction, then row replay performs only tuple
# lookup and the final linear stored-word comparison.
PRIMITIVE_WORDS: dict[tuple[int, ...], tuple[int, ...]] = {}
PRIMITIVE_INVERSES: dict[tuple[int, ...], tuple[int, ...]] = {}


def token(value: Any) -> str:
    text = canon(jsonable(value)).hex(); KEYS[text] = value; return text


def decode_token(text: str) -> Any:
    if text not in KEYS:
        value = json.loads(bytes.fromhex(text).decode("ascii"))
        def restore(item: Any) -> Any:
            if isinstance(item, dict) and set(item) == {"__bytes__"}: return bytes.fromhex(item["__bytes__"])
            if isinstance(item, list): return tuple(restore(x) for x in item)
            if isinstance(item, dict): return {k: restore(v) for k, v in item.items()}
            return item
        KEYS[text] = restore(value)
    return KEYS[text]


def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw); require(letter in (-2, -1, 1, 2), "word:letter")
        if out and out[-1] == -letter: out.pop()
        else: out.append(letter)
    return tuple(out)


def word_inv(word: Sequence[int]) -> tuple[int, ...]:
    return word_reduce(-int(x) for x in reversed(word))


def word_mul(*words: Sequence[int]) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for word in words: out = word_reduce(out + tuple(int(x) for x in word))
    return out


def checker_free_reduce(word: Iterable[int], width: int = 6) -> tuple[int, ...]:
    """Free reduction for substituted PB3/PB4 words (generators 1..6)."""
    out: list[int] = []
    for raw in word:
        letter = int(raw); require(letter != 0 and abs(letter) <= width,
                                   "checker:free_word_letter")
        if out and out[-1] == -letter: out.pop()
        else: out.append(letter)
    return tuple(out)


def checker_word_inv(word: Sequence[int]) -> tuple[int, ...]:
    return checker_free_reduce(-int(x) for x in reversed(word))


def checker_pp_words(words: Sequence[Sequence[int]]) -> tuple[int, ...]:
    require(bool(words), "checker:empty_paper_product")
    return checker_free_reduce(x for word in reversed(words) for x in word)


def checker_word_substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Independent free-group substitution used by the checker.

    The pinned E4 module supplies only quotient/group operations.  Keeping
    this literal recurrence here prevents the producer's word collector from
    silently becoming the checker implementation.
    """
    out: tuple[int, ...] = ()
    for raw in word:
        letter = int(raw); require(1 <= abs(letter) <= len(images), "checker:word_substitution_index")
        image = tuple(int(x) for x in images[abs(letter) - 1])
        out = checker_free_reduce(out + (image if letter > 0 else checker_word_inv(image)))
    return out


def checker_fox_gradient(word: Sequence[int], quotient: Any) -> tuple[dict[tuple[int, Any], int], Any]:
    """Independent left Fox recurrence (without producer helper calls)."""
    prefix = quotient.identity; gradient: dict[tuple[int, Any], int] = {}
    for raw in word:
        letter = int(raw); index = abs(letter)
        require(1 <= index <= len(quotient.generators), "checker:fox_generator_index")
        coefficient = 1 if letter > 0 else 2
        if letter < 0:
            prefix = quotient.mul(prefix, quotient.inverse_generators[index - 1])
        key = (index, prefix if letter < 0 else prefix)
        value = (gradient.get(key, 0) + coefficient) % 3
        if value: gradient[key] = value
        else: gradient.pop(key, None)
        if letter > 0:
            prefix = quotient.mul(prefix, quotient.generators[index - 1])
    return gradient, prefix


def checker_pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i + 1, rank + 1)]


def checker_pair_index(rank: int, pair: Sequence[int]) -> int:
    try: return checker_pairs(rank).index([int(pair[0]), int(pair[1])]) + 1
    except (ValueError, IndexError) as exc: raise Reject("checker:bad_pair_index") from exc


def checker_artin_step(rank: int, letter: int) -> list[list[int]]:
    index = abs(int(letter)); require(1 <= index < rank, "checker:artin_letter")
    images = [[j] for j in range(1, rank + 1)]
    if letter > 0:
        images[index - 1], images[index] = [index, index + 1, -index], [index]
    else:
        images[index - 1], images[index] = [index + 1], [-(index + 1), index, index + 1]
    return images


def checker_artin_images(rank: int, braid: Sequence[int]) -> list[list[int]]:
    images = [[j] for j in range(1, rank + 1)]
    for letter in braid:
        step = checker_artin_step(rank, int(letter))
        images = [list(checker_word_substitute(word, step)) for word in images]
    return images


def checker_aij_braid(i: int, j: int) -> list[int]:
    return list(range(j - 1, i, -1)) + [i, i] + [-k for k in range(i + 1, j)]


def checker_pure_relations(rank: int) -> list[list[int]]:
    """PB3/PB4 2/11 relation recurrence, owned by this checker."""
    if rank == 2: return []
    old_pairs = checker_pairs(rank - 1)
    old_map = [[checker_pair_index(rank, pair)] for pair in old_pairs]
    relations = [list(checker_word_substitute(word, old_map))
                 for word in checker_pure_relations(rank - 1)]
    kernel = [[checker_pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        generator = checker_pair_index(rank, [i, j])
        action = checker_artin_images(rank - 1, checker_aij_braid(i, j))
        for k in range(1, rank):
            h = checker_pair_index(rank, [k, rank])
            tail = checker_word_substitute(action[k - 1], kernel)
            relations.append(list(checker_free_reduce(
                [-generator, h, generator] + list(checker_word_inv(tail)))))
    return relations


def row_key(context: int, component: int, element: Any) -> str:
    return f"{context}:{int(component)}:{token(element)}"


def raw_key(context: int, relation: int, element: Any) -> str:
    return f"{context}:{relation}:{token(element)}"


def split_key(value: str) -> tuple[int, int, str]:
    a, b, c = value.split(":", 2); return int(a), int(b), c


def add_sparse(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, raw in right.items():
        value = (out.get(key, 0) + int(scale) * int(raw)) % 3
        if value: out[key] = value
        else: out.pop(key, None)
    return out


def scale_sparse(value: dict[str, int], scale: int) -> dict[str, int]:
    return {key: (int(raw) * int(scale)) % 3 for key, raw in value.items()
            if (int(raw) * int(scale)) % 3}


COUNTER_TYPES = {key: ("validation" if key == "restore_validation" else
                       "host" if key in {"wall_seconds", "input_bytes"}
                       else "peak" if key in {"rss_bytes", "checkpoint_peak_bytes"} else "semantic")
                 for key in CAPS}

# The producer owns the forward prefix counters which are not part of this
# checker-side suffix registry.  Keep a distinct, exact contract for that
# physical receipt while requiring every shared limit to agree byte-for-byte.
PRODUCER_CAPS = {**CAPS, "prefix_nodes": 50000, "prefix_edges": 50000,
                 "prefix_edge_state_products": 200000}
PRODUCER_COUNTER_TYPES = {key: ("validation" if key == "restore_validation" else
                                "host" if key in {"wall_seconds", "input_bytes"}
                                else "peak" if key in {"rss_bytes", "checkpoint_peak_bytes"}
                                else "semantic") for key in PRODUCER_CAPS}


class Meter:
    def __init__(self, limits: dict[str, int | float] | None = None):
        self.limits = dict(limits or CAPS); self.counter_types = dict(COUNTER_TYPES)
        require(set(self.limits) == set(self.counter_types), "checker:meter_counter_registry")
        self.semantic_counters: dict[str, int | float] = {
            key: 0 for key, kind in self.counter_types.items() if kind == "semantic"}
        self.restore_validation_counters: dict[str, int | float] = {}
        self.host_counters: dict[str, int | float] = {"wall_seconds": 0.0, "input_bytes": 0}
        self.host_history: list[dict[str, int | float]] = []
        self.peak_counters: dict[str, int | float] = {"rss_bytes": 0, "checkpoint_peak_bytes": 0}
        self.counters = {key: 0 for key in self.limits}
        self.completed_counters: dict[str, int | float] = dict(self.semantic_counters)
        self.pending_completed_counters: dict[str, int | float] | None = None
        self.pending_saved_validation: dict[str, int | float] | None = None
        self.pending_saved_peak: dict[str, int | float] | None = None
        self.started = time.monotonic(); self.wall_base = 0.0; self.restore_mode = False
        self.work_units_since_sample = 0; self.sample_interval = 4096
        self.state_name = "AUTHORITY_UNREAD"; self.authority_complete = False; self._sync()

    def _sync(self) -> None:
        for key, kind in self.counter_types.items():
            if kind == "semantic": self.counters[key] = self.semantic_counters.get(key, 0)
            elif kind == "host": self.counters[key] = self.host_counters.get(key, 0)
            elif kind == "peak": self.counters[key] = self.peak_counters.get(key, 0)
            else: self.counters[key] = self.restore_validation_counters.get(key, 0)

    def _value(self, key: str) -> int | float:
        kind = self.counter_types.get(key); require(kind is not None, "checker:unregistered_counter:" + str(key))
        if kind == "semantic": return self.semantic_counters.get(key, 0)
        if kind == "host": return self.host_counters.get(key, 0)
        if kind == "peak": return self.peak_counters.get(key, 0)
        return self.restore_validation_counters.get(key, 0)

    def check(self, state: str | None = None) -> None:
        if state: self.state_name = state
        self.host_counters["wall_seconds"] = self.wall_base + time.monotonic() - self.started
        if "rss_bytes" in self.limits:
            try: self.peak_counters["rss_bytes"] = max(self.peak_counters.get("rss_bytes", 0), int(__import__("resource").getrusage(0).ru_maxrss) * 1024)
            except Exception: pass
        self._sync()
        for key, limit in self.limits.items():
            value = self._value(key)
            if value > limit: raise ResourceStop(self.state_name, key, value, limit, self.state_name)
        self.work_units_since_sample = 0

    def bump(self, key: str, amount: int = 1, state: str | None = None) -> None:
        require(key in self.counter_types, "checker:unregistered_counter:" + str(key)); kind = self.counter_types[key]
        if self.restore_mode and kind == "semantic": target = self.restore_validation_counters; target_key = "restore_validation"
        elif kind == "semantic": target = self.semantic_counters
        elif kind == "host": target = self.host_counters
        elif kind == "peak": target = self.peak_counters
        else: target = self.restore_validation_counters
        if not (self.restore_mode and kind == "semantic"): target_key = key
        if kind == "peak": target[target_key] = max(target.get(target_key, 0), int(amount))
        else: target[target_key] = target.get(target_key, 0) + int(amount)
        value = self._value(target_key)
        limit = self.limits["restore_validation"] if self.restore_mode and kind == "semantic" else self.limits[key]
        if value > limit: raise ResourceStop(state or self.state_name, key, value, limit, self.state_name)
        self.work_units_since_sample += max(1, int(amount))
        if self.work_units_since_sample >= self.sample_interval: self.check(state)

    def validation_bump(self, amount: int = 1, state: str = "checker.checkpoint.restore") -> None:
        self.restore_validation_counters["restore_validation"] = self.restore_validation_counters.get("restore_validation", 0) + int(amount)
        value = self.restore_validation_counters["restore_validation"]
        require(value <= self.limits["restore_validation"], "checker:restore_validation_cap")
        self.work_units_since_sample += max(1, int(amount))
        if self.work_units_since_sample >= self.sample_interval:
            self.check(state)

    def terminal_bump(self, key: str, amount: int = 1, state: str = "checker.terminal.transport") -> None:
        """Charge the reserved terminal channel without semantic rerouting."""
        require(key in {"terminal_canonicalization", "terminal_checkpoint_bytes",
                        "terminal_serialized_bytes",
                        "terminal_final_write"}, "checker:terminal_counter")
        value = self.semantic_counters.get(key, 0) + int(amount)
        require(value <= self.limits[key], "checker:terminal_transport_cap:" + key)
        self.semantic_counters[key] = value
        self.completed_counters[key] = value
        self.counters[key] = value

    def reserve(self, key: str, amount: int, state: str) -> None:
        require(key in self.counter_types, "checker:unregistered_counter:" + str(key)); kind = self.counter_types[key]
        current = self._value(key)
        if self.restore_mode and kind == "semantic": current = self.restore_validation_counters.get("restore_validation", 0)
        limit = self.limits["restore_validation"] if self.restore_mode and kind == "semantic" else self.limits[key]
        if current + int(amount) > limit: raise ResourceStop(state, key, current + int(amount), limit, self.state_name)

    def install_completed(self, saved: dict[str, int | float], saved_validation: dict[str, int | float],
                          saved_peak: dict[str, int | float] | None = None) -> None:
        require(set(saved) == set(self.semantic_counters), "checker:saved_semantic_registry")
        require(set(saved_validation) <= {key for key, kind in self.counter_types.items() if kind == "validation"},
                "checker:saved_validation_registry")
        require(all(isinstance(value, (int, float)) and value >= 0 for value in saved.values()), "checker:saved_semantic_values")
        self.semantic_counters = dict(saved); self.completed_counters = dict(saved)
        self.pending_completed_counters = None; self.pending_saved_validation = None; self.pending_saved_peak = None
        self.restore_validation_counters = dict(saved_validation)
        if saved_peak is not None:
            self.peak_counters = {key: max(self.peak_counters.get(key, 0), value)
                                  for key, value in saved_peak.items()}
        # H1 remains anchored at process invocation; resetting started here
        # would grant the continuation a second wall-time budget.
        self.wall_base = 0.0; self.restore_mode = False
        self._sync(); self.check("checker.checkpoint.continuation")

    def public(self, strict: bool = True) -> dict[str, Any]:
        if strict: self.check()
        else: self._sync()
        return {"limits": dict(self.limits), "counter_registry": dict(self.counter_types),
                              "counters": dict(self.counters), "semantic_counters": dict(self.semantic_counters),
                              "completed_counters": dict(self.completed_counters),
                              "restore_validation_counters": dict(self.restore_validation_counters),
                              "host_counters": dict(self.host_counters), "host_history": list(self.host_history),
                              "peak_counters": dict(self.peak_counters),
                              "last_replayable_state": self.state_name, "single_process": True, "no_retry_or_pool": True,
                              "object_caps": dict(OBJECT_CAPS)}





def windows_no_follow(path: Path) -> None:
    if os.name != "nt": return
    try:
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        open_file = kernel.CreateFileW
        open_file.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
                              ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        open_file.restype = ctypes.c_void_p
        handle = open_file(str(path), 0x80000000, 0x00000001 | 0x00000002 | 0x00000004,
                           None, 3, 0x00200000 | 0x00000080, None)
        if handle in (None, ctypes.c_void_p(-1).value): raise Reject("path:windows_no_follow")
        kernel.CloseHandle(handle)
    except Reject: raise
    except Exception as exc: raise Reject("path:windows_no_follow") from exc


def exact_path(text: str, area: str, basename: str, label: str, strict: bool = True) -> Path:
    raw = str(text).replace("\\", "/"); p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts, label + ":lexical_path")
    try:
        expected = ((ROOT / p) if area == "." else (ROOT / area / basename)).resolve(strict=strict)
        actual = (ROOT / p).resolve(strict=strict)
    except (FileNotFoundError, OSError) as exc:
        raise Reject(label + ":resolved_path_missing") from exc
    require(actual == expected and actual.name == basename, label + ":resolved_path")
    cursor = ROOT
    for part in p.parts:
        cursor /= part
        try: info = os.lstat(cursor)
        except OSError as exc: raise Reject(label + ":identity_unavailable") from exc
        if stat.S_ISLNK(info.st_mode) or (os.name == "nt" and bool(getattr(info, "st_file_attributes", 0) & 0x400)):
            raise Reject(label + ":reparse_or_symlink")
    windows_no_follow(actual); return actual


def output_path(text: str, area: str, label: str) -> Path:
    raw = str(text).replace("\\", "/"); p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts, label + ":lexical_path")
    out = (ROOT / p).resolve(strict=False); parent = (ROOT / area).resolve(strict=True)
    require(out.parent == parent, label + ":containment")
    cursor = ROOT
    for part in p.parts[:-1]:
        cursor /= part
        try: info = os.lstat(cursor)
        except OSError as exc: raise Reject(label + ":parent_identity_unavailable") from exc
        require(not stat.S_ISLNK(info.st_mode) and not
                (os.name == "nt" and bool(getattr(info, "st_file_attributes", 0) & 0x400)),
                label + ":parent_reparse_or_symlink")
    return out


def checkpoint_input(path: Path, label: str) -> Path:
    """Revalidate a checkpoint path, accepting only the resolved ci/out owner."""
    try:
        relative = path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()
    except ValueError as exc:
        raise Reject(label + ":outside_workspace") from exc
    return exact_path(relative, "ci/out", path.name, label)


def read_once(path: Path, expected: tuple[str, int, str], meter: Meter, label: str,
              terminal_transport: bool = False) -> bytes:
    relative, size, expected_sha = expected
    require(path.as_posix().replace(ROOT.as_posix() + "/", "") == relative, label + ":relative")
    # A separate Windows probe followed by os.open cannot prove that the read
    # came from the probed handle.  Until a same-handle CreateFileW/ReadFile
    # implementation exists, fail closed as typed UNKNOWN_INPUT.
    if os.name == "nt":
        raise Reject(label + ":windows_same_handle_identity_unavailable")
    windows_no_follow(path)
    try:
        before = os.lstat(path); require(not stat.S_ISLNK(before.st_mode), label + ":symlink")
        require(getattr(before, "st_nlink", 1) == 1, label + ":hardlink_identity")
        before_identity = (before.st_dev, before.st_ino, before.st_size,
                           getattr(before, "st_mtime_ns", int(before.st_mtime * 1000000000)))
        if terminal_transport:
            meter.terminal_bump("terminal_checkpoint_bytes", int(before.st_size),
                                label + ":reserved_checkpoint_read")
        else:
            meter.bump("input_bytes", int(before.st_size), label + ":charge_before_read")
        no_follow = getattr(os, "O_NOFOLLOW", 0)
        if not no_follow:
            raise Reject(label + ":no_follow_unavailable")
        fd = os.open(str(path), os.O_RDONLY | getattr(os, "O_BINARY", 0) | no_follow)
        try:
            opened = os.fstat(fd)
            opened_identity = (opened.st_dev, opened.st_ino, opened.st_size,
                               getattr(opened, "st_mtime_ns", int(opened.st_mtime * 1000000000)))
            require(opened_identity == before_identity and getattr(opened, "st_nlink", 1) == 1,
                    label + ":identity_changed")
            buffer = bytearray(int(opened.st_size)); offset = 0; left = int(opened.st_size)
            while left:
                block = os.read(fd, min(1024 * 1024, left)); require(block, label + ":short_read")
                buffer[offset:offset + len(block)] = block
                offset += len(block); left -= len(block)
            raw = buffer; after = os.fstat(fd)
        finally: os.close(fd)
        after_identity = (after.st_dev, after.st_ino, after.st_size,
                          getattr(after, "st_mtime_ns", int(after.st_mtime * 1000000000)))
        path_after = os.lstat(path)
        path_after_identity = (path_after.st_dev, path_after.st_ino, path_after.st_size,
                               getattr(path_after, "st_mtime_ns", int(path_after.st_mtime * 1000000000)))
        require(after_identity == before_identity and path_after_identity == after_identity and
                getattr(path_after, "st_nlink", 1) == 1 and len(raw) == size and
                (not expected_sha or sha(raw) == expected_sha), label + ":bytes_sha256")
        windows_no_follow(path); return raw
    except Reject: raise
    except (OSError, ValueError) as exc: raise Reject(label + ":no_follow_identity") from exc


def read_json(path: Path, pin: tuple[str, int, str], meter: Meter, label: str) -> tuple[bytes, dict[str, Any]]:
    raw = read_once(path, pin, meter, label)
    try: value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise Reject(label + ":canonical_ascii_json") from exc
    require(isinstance(value, dict), label + ":object"); return raw, value


class Authority:
    """Independent one-pass authority adapter and literal-owner audit."""
    def __init__(self, args: argparse.Namespace, meter: Meter):
        self.meter = meter
        self.paths = {key: exact_path(getattr(args, "task198_" + key), "ci/in", value,
                                      "TASK198_" + key.upper()) for key, value in AUTH.items()}
        self.raw: dict[str, bytes] = {}; self.values: dict[str, dict[str, Any]] = {}
        for key in ("manifest", "verdict", "receipt"):
            pin = self.pin(key); raw, value = read_json(self.paths[key], pin, meter, "authority." + key)
            self.raw[key], self.values[key] = raw, value
        for key in ("producer", "checker"):
            raw = read_once(self.paths[key], self.pin(key), meter, "authority." + key)
            require(raw.endswith(b"\n") and raw.decode("ascii"), "authority." + key + ":attestation")
            self.raw[key] = raw
        self.task176: dict[str, Any] = {}; self.task176_raw: bytes = b""; self.task176_sources: dict[str, bytes] = {}
        task_path = exact_path(TASK176["receipt"][0], ".", Path(TASK176["receipt"][0]).name, "TASK176_RECEIPT")
        self.task176_raw, self.task176 = read_json(task_path, TASK176["receipt"], meter, "task176.receipt")
        manifest_path = exact_path(TASK176["manifest"][0], ".", Path(TASK176["manifest"][0]).name, "TASK176_MANIFEST")
        manifest_raw = read_once(manifest_path, TASK176["manifest"], meter, "task176.manifest")
        self.task176_manifest = json.loads(manifest_raw.decode("ascii"))
        for key in ("producer", "checker"):
            pin = TASK176[key]; p = exact_path(pin[0], ".", Path(pin[0]).name, "TASK176_SOURCE_" + key.upper())
            self.task176_sources[key] = read_once(p, pin, meter, "task176.source." + key)
        result_pin = TASK176["checker_result"]
        result_path = exact_path(result_pin[0], ".", Path(result_pin[0]).name, "TASK176_CHECKER_RESULT")
        self.task176_checker_result_raw, self.task176_checker_result = read_json(
            result_path, result_pin, meter, "task176.checker_result")
        recovery_v1_pin = TASK176["recovery_manifest_v1"]
        recovery_v1_path = exact_path(recovery_v1_pin[0], ".", Path(recovery_v1_pin[0]).name,
                                      "TASK176_RECOVERY_MANIFEST_V1")
        self.task176_recovery_v1_raw, self.task176_recovery_v1 = read_json(
            recovery_v1_path, recovery_v1_pin, meter, "task176.recovery_manifest_v1")
        recovery_pin = TASK176["recovery_manifest"]
        recovery_path = exact_path(recovery_pin[0], ".", Path(recovery_pin[0]).name,
                                   "TASK176_RECOVERY_MANIFEST")
        self.task176_recovery_raw, self.task176_recovery = read_json(
            recovery_path, recovery_pin, meter, "task176.recovery_manifest")
        self.validate()
        self.identity = {
            "task198": {key: {"path": "ci/in/" + AUTH[key], "bytes": len(raw), "sha256": sha(raw)}
                        for key, raw in self.raw.items()},
            "task176": {key: {"path": value[0], "bytes": value[1], "sha256": value[2]}
                        for key, value in TASK176.items()},
            "task176_source_identities": {key: {"path": TASK176[key][0], "bytes": len(raw), "sha256": sha(raw)}
                                           for key, raw in self.task176_sources.items()},
            "receipt_sha256": RECEIPT_SHA, "manifest_sha256": MANIFEST_SHA,
        }

    def pin(self, key: str) -> tuple[str, int, str]:
        if key == "receipt": return ("ci/in/" + AUTH[key], RECEIPT_BYTES, RECEIPT_SHA)
        if key == "manifest": return ("ci/in/" + AUTH[key], 2722, MANIFEST_SHA)
        if key == "verdict": return ("ci/in/" + AUTH[key], 150, VERDICT_SHA)
        return ("ci/in/" + AUTH[key], 81 if key == "producer" else 95,
                "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"
                if key == "producer" else
                "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e")

    @property
    def receipt(self) -> dict[str, Any]: return self.values["receipt"]

    @property
    def rows(self) -> list[dict[str, Any]]:
        return self.receipt["Delta0"]["presentation"]["rows"]

    def validate(self) -> None:
        receipt, manifest, verdict = self.values["receipt"], self.values["manifest"], self.values["verdict"]
        mbody = dict(manifest); mclaim = mbody.pop("manifest_self_digest_sha256", None)
        require(manifest.get("schema") == MANIFEST_SCHEMA and manifest.get("accepted") is True and
                manifest.get("independent") is True and manifest.get("synthetic") is False and
                mclaim == "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684" and
                mclaim == digest(mbody), "authority:manifest_seal")
        rbody = dict(receipt); rclaim = rbody.pop("self_digest_sha256", None)
        require(receipt.get("schema") == PRESENTATION_SCHEMA and receipt.get("status") == "COMPLETE" and
                receipt.get("terminal") == "ROOF_BRIDGE_ISOMORPHISM" and
                rclaim == "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f" and
                rclaim == digest(rbody), "authority:receipt_seal")
        require(verdict.get("schema") == PRESENTATION_SCHEMA + "/crosscheck/v2" and
                verdict.get("accepted") is True and verdict.get("independent") is True and
                verdict.get("receipt_terminal") == "ROOF_BRIDGE_ISOMORPHISM", "authority:verdict")
        require(manifest.get("accepted_receipt_basename") == AUTH["receipt"] and
                manifest.get("receipt", {}).get("sha256") == RECEIPT_SHA and
                manifest.get("receipt", {}).get("bytes") == RECEIPT_BYTES and
                manifest.get("checker_verdict", {}).get("sha256") == VERDICT_SHA and
                manifest.get("checker_verdict", {}).get("bytes") == 150, "authority:members")
        for side, expected in TASK198.items():
            copied = manifest.get("task198_source_identities", {}).get(side, {})
            require(copied.get("path") == expected[0] and copied.get("bytes") == expected[1] and
                    copied.get("sha256") == expected[2], "authority:manifest_source:" + side)
            p = exact_path(expected[0], ".", Path(expected[0]).name, "TASK198_PHYSICAL_" + side)
            raw = read_once(p, expected, self.meter, "authority.physical." + side)
            require(sha(raw) == expected[2], "authority:physical_source:" + side)
        for side in ("producer", "checker"):
            item, att = manifest.get(side, {}), manifest.get(side + "_attestation", {})
            require(item.get("run") == "33155710862" and item.get("head") == "bed1d5e6b41477b8799f2a33a24e46f7800f9510" and
                    item.get("artifact_id") == "9686477718" and
                    item.get("zip_sha256") == "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854" and
                    att.get("basename") == AUTH[side] and att.get("bytes") == len(self.raw[side]) and
                    att.get("sha256") == sha(self.raw[side]), "authority:run_attestation:" + side)
        presentation = receipt.get("Delta0", {}).get("presentation", {})
        require(presentation.get("row_count") == ROWS and presentation.get("layer_counts") == LAYERS and
                len(presentation.get("rows", [])) == ROWS and presentation.get("resume_cursor") == ROWS and
                presentation.get("normal_generation") is True, "authority:presentation_header")
        ordinals = {layer: [] for layer in LAYERS}; global_owner = []
        for row in self.rows:
            self.meter.bump("literal_comparisons", 1, "authority.row_parse")
            require(row.get("layer") in LAYERS and isinstance(row.get("ordinal"), int), "authority:row_shape")
            literal = row.get("word")
            require(isinstance(literal, list) and
                    all(type(letter) is int and letter in (-2, -1, 1, 2) for letter in literal),
                    "authority:row_word_shape")
            require(tuple(word_reduce(literal)) == tuple(literal), "authority:row_word_reduced")
            ordinals[row["layer"]].append(row["ordinal"])
            global_owner.append((row["layer"], row["ordinal"]))
        for layer, count in LAYERS.items(): require(ordinals[layer] == list(range(1, count + 1)), "authority:ordinal:" + layer)
        expected_global = [(layer, ordinal) for layer, count in LAYERS.items()
                           for ordinal in range(1, count + 1)]
        require(global_owner == expected_global, "authority:global_layer_sequence")
        # Hash the literal rows once while closing each authenticated chunk;
        # do not walk the 6,441-row object once per chunk after the full pass.
        row_hash = hashlib.sha256(); row_hash.update(b"[")
        chunk_hash = hashlib.sha256(); chunk_hash.update(b"[")
        chunk_items = 0
        chunks = presentation.get("chunks", []); require(len(chunks) == 7, "authority:seven_chunks")
        by_end = {int(item.get("end")): item for item in chunks}
        require(set(by_end) == {1024, 2048, 3072, 4096, 5120, 6144, 6441}, "authority:chunk_boundaries")
        for ordinal, literal_row in enumerate(self.rows, 1):
            encoded = canon(literal_row)
            if ordinal > 1: row_hash.update(b",")
            if chunk_items: chunk_hash.update(b",")
            row_hash.update(encoded); chunk_hash.update(encoded); chunk_items += 1
            if ordinal in by_end:
                item = by_end[ordinal]
                chunk_hash.update(b"]")
                require(chunk_hash.hexdigest() == item.get("sha256") and item.get("sealed") is True and
                        item.get("prefix_complete") is True, "authority:chunk_slice_recomputed")
                chunk_hash = hashlib.sha256(); chunk_hash.update(b"["); chunk_items = 0
        row_hash.update(b"]")
        require(row_hash.hexdigest() == presentation.get("rows_sha256"), "authority:rows_digest_recomputed")
        proof = presentation.get("normal_generation_proof", {})
        for key, value in {"Gamma_cayley_edge_count": 6318, "Gamma_cayley_state_count": 243,
                           "Q0_defect_normal_closure_order": 243, "Q0_lift_count": 19,
                           "all_record_generator_closure_order": 243, "marked_action_loop_count": 104,
                           "selected_gamma_records": [1, 3, 6, 9],
                           "presentation_quotient_order_upper_bound": 357128352,
                           "surjective_marked_image_order": 357128352,
                           "upper_bound_equals_image_order": True}.items():
            require(proof.get(key) == value, "authority:normal_generation_proof:" + key)
        qproof = proof.get("Q0_order_proof", {})
        for key, value in {"G9_abstract_presentation_order": 2916, "G9_direct_image_order": 2916,
                           "P_abstract_presentation_order": 504, "P_direct_image_order": 504,
                           "Q0_marked_image_order": 1469664, "Q0_presentation_order_upper_bound": 1469664,
                           "complete_relator_count": 19,
                           "complete_relators_sha256": "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a",
                           "cross_commutator_count": 4,
                           "factor_payload_sha256": "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba",
                           "marked_splitting_equation_count": 2}.items():
            require(qproof.get(key) == value, "authority:qproof:" + key)
        bridge = receipt.get("bridge", {}); ledger = bridge.get("occurrence_ledger")
        require(bridge.get("ten_to_eleven") == [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9] and
                bridge.get("eleven_delete_duplicate") == [0, 1, 2, 3, 5, 6, 7, 8, 9, 10] and
                bridge.get("seven_blocks") == [[0, 1, 2], [3, 0, 4], [5], [6], [7], [8], [9]] and
                bridge.get("occurrence_ledger_sha256") == digest(ledger) and isinstance(ledger, list) and len(ledger) == 11 and
                bridge.get("typed_coordinate_ledger_sha256") == digest(self.task176.get("coordinates")), "authority:bridge_owners")
        fields = ("block", "block_index", "block_slot", "context_id", "factor_sign", "fox_prefix_occurrences",
                  "occurrence", "ordinal", "orientation", "role", "ten_index", "type")
        for item in ledger: require(all(field in item for field in fields), "authority:bridge_field")
        evaluator, canaries = receipt.get("evaluator", {}), receipt.get("evaluator", {}).get("canaries", {})
        require(evaluator.get("schema") == "d972-r07-v188-roof-consumer-action-abi/v1" and
                evaluator.get("coordinate_widths") == [40, 40, 40, 40, 40, 154, 154, 154, 154, 154] and
                evaluator.get("relator_rows_sha256") == presentation.get("rows_sha256"), "authority:evaluator_abi")
        require(set(canaries) == {"nonsplit_y_y_section_cocycle", "source_2_2", "x", "x_action_y",
                                  "x_inverse", "xy", "xy_section_cocycle", "y"}, "authority:actual_canary_roster")
        require(canaries.get("nonsplit_y_y_section_cocycle") is None, "authority:nonsplit_canary")
        for key in ("x", "x_action_y", "x_inverse", "xy", "xy_section_cocycle", "y", "source_2_2"):
            require(isinstance(canaries.get(key), dict) and isinstance(canaries[key].get("value"), list), "authority:canary_value:" + key)
        require(receipt.get("Ihara_witness") is False and receipt.get("cofinal_lift") is False and
                receipt.get("fake") is False and receipt.get("direct_Delta_states_enumerated") == 0 and
                receipt.get("D_all", {}).get("materialized") is False, "authority:forbidden_flags")
        require(self.task176.get("schema") == "d972-r07-all-seven-extension-section-census/v1" and
                self.task176.get("status") == "COMPLETE" and
                self.task176.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
                self.task176.get("boundaries", {}).get("fake") is False and
                self.task176.get("boundaries", {}).get("Ihara_witness") is False, "task176:accepted_receipt")
        require(self.task176_manifest == {"artifact_id": "9635036013", "head": "0533e42019c9f67f6cec3d1566152db17b903836",
                                         "member": "d972_r07_all_seven_extension_section_census_v1.json", "member_bytes": 13649089,
                                         "member_sha256": TASK176["receipt"][2], "run": "33044121344",
                                         "zip_sha256": "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912"},
                "task176:manifest_owner")
        recovery_v1 = self.task176_recovery_v1; recovery_v1_body = dict(recovery_v1)
        recovery_v1_claim = recovery_v1_body.pop("self_digest_sha256", None)
        require(recovery_v1.get("schema") == "d972-r07-all-seven-extension-section-census-recovery-manifest/v1" and
                recovery_v1_claim == "f8c6c0faf2588cd58d8a2aec75a2a1f9950ea67769dd913fbd796d018098f581" and
                recovery_v1_claim == digest(recovery_v1_body) and
                recovery_v1.get("recovered_verdict", {}).get("sha256") == TASK176["checker_result"][2] and
                recovery_v1.get("accepted_receipt", {}).get("self_digest_sha256") ==
                "f8f0ce249ff547d3e1235bd4b9760daa2b34f23771bf7da47b48dbd5cbbfae1d" and
                recovery_v1.get("accepted_receipt", {}).get("self_digest_sha256") !=
                self.task176.get("self_digest_sha256"), "task176:recovery_v1_superseded")
        recovery = self.task176_recovery; recovery_body = dict(recovery)
        recovery_claim = recovery_body.pop("self_digest_sha256", None)
        require(recovery.get("schema") == "d972-r07-all-seven-extension-section-census-recovery-manifest/v2" and
                recovery_claim == "e95b4e7781a14cffd07d445141f20c942861168d201f2ce62879a0ddf3a45026" and
                recovery_claim == digest(recovery_body) and
                recovery.get("accepted_receipt") == {
                    "bytes": TASK176["receipt"][1], "path": TASK176["receipt"][0],
                    "self_digest_sha256": self.task176.get("self_digest_sha256"),
                    "sha256": TASK176["receipt"][2]} and
                recovery.get("recovered_verdict") == {
                    "bytes": TASK176["checker_result"][1], "path": TASK176["checker_result"][0],
                    "self_digest_sha256": "e9d42ea064e7caaa9a333f7e2a8aec42f709bf1565e9fc9a8950ef92e18ce473",
                    "sha256": TASK176["checker_result"][2]} and
                recovery.get("physical_sources") == {
                    side: {"bytes": TASK176[side][1], "path": TASK176[side][0], "sha256": TASK176[side][2]}
                    for side in ("producer", "checker")} and
                recovery.get("receipt_manifest") == {
                    "bytes": TASK176["manifest"][1], "path": TASK176["manifest"][0], "sha256": TASK176["manifest"][2]} and
                recovery.get("mathematical_grade_change") is False and
                recovery.get("correction") == {
                    "json_pointer": "/accepted_receipt/self_digest_sha256",
                    "old_value": "f8f0ce249ff547d3e1235bd4b9760daa2b34f23771bf7da47b48dbd5cbbfae1d",
                    "new_value": self.task176.get("self_digest_sha256"),
                    "reason": "transcription mismatch against physical accepted receipt and reply348"} and
                recovery.get("supersedes") == {
                    "bytes": TASK176["recovery_manifest_v1"][1], "path": TASK176["recovery_manifest_v1"][0],
                    "self_digest_sha256": "f8c6c0faf2588cd58d8a2aec75a2a1f9950ea67769dd913fbd796d018098f581",
                    "sha256": TASK176["recovery_manifest_v1"][2]}, "task176:recovery_manifest_v2")
        result = self.task176_checker_result; result_body = dict(result)
        result_claim = result_body.pop("self_digest_sha256", None)
        require(result.get("schema") == "d972-r07-all-seven-extension-section-census-check/v1" and
                result.get("grade") == "CROSS_CHECKED" and
                result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
                result.get("receipt_terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
                result.get("receipt_bytes") == TASK176["receipt"][1] and
                result.get("receipt_sha256") == TASK176["receipt"][2] and
                result.get("producer_sha256") == TASK176["producer"][2] and
                result_claim == "e9d42ea064e7caaa9a333f7e2a8aec42f709bf1565e9fc9a8950ef92e18ce473" and
                result_claim == digest(result_body), "task176:physical_checker_result")

    def stream(self, values: Iterable[Any]) -> str:
        h = hashlib.sha256()
        first = True; h.update(b"[")
        for value in values:
            if not first: h.update(b",")
            first = False
            self.meter.bump("canonicalization", 1, "authority.canonical_stream"); h.update(canon(value))
        h.update(b"]")
        return h.hexdigest()


def element_blob(value: Any) -> bytes:
    require(isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], bytes) and
            isinstance(value[1], bytes), "element:blob")
    return value[0] + value[1]


def add_local(left: dict[tuple[int, Any], int], right: dict[tuple[int, Any], int], scale: int = 1) -> dict[tuple[int, Any], int]:
    out = dict(left)
    for key, raw in right.items():
        value = (out.get(key, 0) + int(scale) * int(raw)) % 3
        if value: out[key] = value
        else: out.pop(key, None)
    return out


def move_local(value: dict[tuple[int, Any], int], element: Any, quotient: Any, scale: int = 1) -> dict[tuple[int, Any], int]:
    out: dict[tuple[int, Any], int] = {}
    for (component, key), raw in value.items():
        moved = (component, quotient.mul(element, key)); coefficient = (scale * int(raw)) % 3
        out[moved] = (out.get(moved, 0) + coefficient) % 3
    return {key: raw for key, raw in out.items() if raw}


def checker_coords_word(coords: Sequence[int]) -> tuple[int, ...]:
    out: list[int] = []
    for index, exponent in enumerate(coords, 1):
        value = int(exponent)
        require(0 <= value < 3, "checker:pc_coordinate_exponent")
        out.extend([index] * value)
    return tuple(out)


def checker_perm_row(row: Any, degree: int) -> bytes:
    if isinstance(row, str):
        values = [int(value) for value in row.replace(",", " ").split()]
    else:
        values = [int(value) for value in row]
    require(len(values) == degree and all(1 <= value <= degree for value in values),
            "checker:permutation_row")
    answer = bytes(value - 1 for value in values)
    require(set(answer) == set(range(degree)), "checker:permutation_bijection")
    return answer


def checker_perm_one(degree: int) -> bytes:
    require(degree <= 256, "checker:permutation_degree")
    return bytes(range(degree))


def checker_perm_mul(left: bytes, right: bytes) -> bytes:
    require(len(left) == len(right), "checker:permutation_product_degree")
    return bytes(right[left[index]] for index in range(len(left)))


def checker_perm_inv(value: bytes) -> bytes:
    answer = [0] * len(value)
    for index, image in enumerate(value):
        answer[image] = index
    return bytes(answer)


class CheckerPcCollector:
    """Checker-local class-2 collector reconstructed from the frozen receipt."""

    def __init__(self, receipt: dict[str, Any]):
        self.n = int(receipt["generator_count"])
        self.orders = [int(value) for value in receipt["relative_orders"]]
        require(self.n == len(self.orders) <= 175 and all(value == 3 for value in self.orders),
                "checker:pc_rank_orders")
        self.powers = [self.coord(value) for value in receipt["power_relations"]]
        self.inverses = [self.coord(value) for value in receipt["inverses"]]
        self.conjugates = {(int(value["i"]), int(value["j"])): self.coord(value["coords"])
                           for value in receipt["conjugate_relations"]}
        self.inverse_conjugates = {(int(value["i"]), int(value["j"])): self.coord(value["coords"])
                                   for value in receipt["inverse_conjugate_relations"]}
        require(len(self.conjugates) == self.n * (self.n - 1) // 2 and
                set(self.conjugates) == set(self.inverse_conjugates),
                "checker:pc_conjugate_tables")
        self._products: dict[bytes, bytes] = {}
        self._inverses: dict[bytes, bytes] = {}

    def coord(self, row: Any) -> bytes:
        if isinstance(row, str):
            values = [int(value) for value in row.replace(",", " ").split()]
        else:
            values = [int(value) for value in row]
        require(len(values) == self.n and all(0 <= value < 3 for value in values),
                "checker:pc_coordinate")
        return bytes(values)

    def one(self) -> bytes:
        return bytes(self.n)

    def collect_uncached(self, word: Sequence[int]) -> bytes:
        tokens: list[int] = []
        for raw in word:
            value = int(raw)
            require(1 <= abs(value) <= self.n, "checker:pc_letter")
            tokens.extend((value,) if value > 0 else checker_coords_word(self.inverses[-value - 1]))
        steps = 0
        cap = max(10000, 1000 * (1 + len(tokens)) * (1 + self.n))
        while True:
            changed = False
            for position in range(len(tokens) - 1):
                left, right = tokens[position], tokens[position + 1]
                if left > right:
                    relation = self.conjugates.get((left, right))
                    require(relation is not None, "checker:pc_missing_conjugate")
                    tokens[position:position + 2] = [right] + list(checker_coords_word(relation))
                    changed = True
                    break
            if not changed:
                position = 0
                while position < len(tokens):
                    generator, end = tokens[position], position
                    while end < len(tokens) and tokens[end] == generator:
                        end += 1
                    if end - position >= 3:
                        tokens[position:position + 3] = list(checker_coords_word(self.powers[generator - 1]))
                        changed = True
                        break
                    position = end
            if not changed:
                break
            steps += 1
            require(steps <= cap, "checker:pc_collection_cap")
        row = [0] * self.n
        previous = 0
        for value in tokens:
            require(value >= previous, "checker:pc_order")
            row[value - 1] += 1
            require(row[value - 1] < 3, "checker:pc_power")
            previous = value
        return bytes(row)

    def mul(self, left: bytes, right: bytes) -> bytes:
        require(len(left) == len(right) == self.n, "checker:pc_product_width")
        key = left + right
        if key in self._products:
            return self._products[key]
        answer = self.collect_uncached(checker_coords_word(left) + checker_coords_word(right))
        if len(self._products) >= 8192:
            self._products.pop(next(iter(self._products)))
        self._products[key] = answer
        return answer

    def inverse(self, value: bytes) -> bytes:
        require(len(value) == self.n, "checker:pc_inverse_width")
        if value in self._inverses:
            return self._inverses[value]
        word: list[int] = []
        for index in range(self.n, 0, -1):
            for _ in range(value[index - 1]):
                word.extend(checker_coords_word(self.inverses[index - 1]))
        answer = self.collect_uncached(word)
        if len(self._inverses) >= 8192:
            self._inverses.pop(next(iter(self._inverses)))
        self._inverses[value] = answer
        return answer


class CheckerMatchedQuotient:
    """Matched permutation/PC quotient owned entirely by the checker."""

    def __init__(self, rank: int, degree: int, pc: CheckerPcCollector,
                 generators: Sequence[tuple[bytes, bytes]]):
        require(len(generators) == len(checker_pairs(rank)), "checker:matched_marked_width")
        self.rank, self.degree, self.pc = rank, degree, pc
        self.generators = list(generators)
        self.identity = (checker_perm_one(degree), self.pc.one())
        self.inverse_generators = [self.inverse(value) for value in self.generators]

    def mul(self, left: tuple[bytes, bytes], right: tuple[bytes, bytes]) -> tuple[bytes, bytes]:
        return checker_perm_mul(left[0], right[0]), self.pc.mul(left[1], right[1])

    def inverse(self, value: tuple[bytes, bytes]) -> tuple[bytes, bytes]:
        return checker_perm_inv(value[0]), self.pc.inverse(value[1])

    def eval(self, word: Sequence[int], images: Sequence[tuple[bytes, bytes]] | None = None) -> tuple[bytes, bytes]:
        marked = self.generators if images is None else images
        result = self.identity
        for raw in word:
            value = marked[abs(int(raw)) - 1]
            result = self.mul(result, value if int(raw) > 0 else self.inverse(value))
        return result


def checker_reconstruct_quotients(data: dict[str, Any]) -> tuple[CheckerMatchedQuotient,
                                                                   CheckerMatchedQuotient]:
    pc3 = CheckerPcCollector(data["groups"]["PB3"])
    pc4 = CheckerPcCollector(data["groups"]["PB4"])
    p3 = [pc3.coord(value["coords"]) for value in data["groups"]["PB3"]["marked_generators"]]
    p4 = [pc4.coord(value["coords"]) for value in data["groups"]["PB4"]["marked_generators"]]
    q0_model, q4_model = data["coarse_models"]["Q0"], data["coarse_models"]["Q4"]
    q0 = [checker_perm_row(value, int(q0_model["degree"]))
          for value in q0_model["marked_permutations"]]
    q4 = [checker_perm_row(value, int(q4_model["degree"]))
          for value in q4_model["marked_permutations"]]
    require(len(q0) == 2 and len(q4) == 6, "checker:coarse_marked_width")
    q0z = checker_perm_inv(checker_perm_mul(q0[1], q0[0]))
    e3 = CheckerMatchedQuotient(3, int(q0_model["degree"]), pc3,
                                 [(q0[0], p3[0]), (q0z, p3[1]), (q0[1], p3[2])])
    e4 = CheckerMatchedQuotient(4, int(q4_model["degree"]), pc4, list(zip(q4, p4)))
    for rank, quotient in ((3, e3), (4, e4)):
        require(all(quotient.eval(value) == quotient.identity
                    for value in checker_pure_relations(rank)),
                f"checker:PB{rank}_matched_presentation")
    return e3, e4


class CState:
    """Checker-owned affine state; no producer state or node is accepted."""
    def __init__(self, quotient: Any, roof: Any, local: dict[tuple[int, Any], int]):
        self.q, self.a = quotient, roof
        self.u = {key: int(value) % 3 for key, value in local.items() if int(value) % 3}

    def mul(self, other: "CState") -> "CState":
        require(self.q is other.q, "state:quotient_identity")
        moved = {(component, self.q.mul(self.a, element)): coefficient
                 for (component, element), coefficient in other.u.items()}
        return CState(self.q, self.q.mul(self.a, other.a), add_local(self.u, moved))

    def inv(self) -> "CState":
        inverse = self.q.inverse(self.a)
        return CState(self.q, inverse, move_local(self.u, inverse, self.q, -1))

    def identity_roof(self) -> bool: return self.a == self.q.identity


class CheckerArithmetic:
    def __init__(self, authority: Authority, meter: Meter):
        self.meter = meter
        e4_path = exact_path(E4_SOURCE[0], ".", Path(E4_SOURCE[0]).name, "PINNED_E4_SOURCE")
        e4_raw = read_once(e4_path, E4_SOURCE, meter, "pinned.e4_source")
        self.e4_source_sha = sha(e4_raw)
        q3raw = read_once(exact_path(Q3_SOURCE[0], ".", Path(Q3_SOURCE[0]).name, "Q3_RECEIPT"), Q3_SOURCE, meter, "pinned.q3")
        try: self.q3 = json.loads(q3raw.decode("ascii"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise Reject("pinned.q3:json") from exc
        self.e3, self.e4 = checker_reconstruct_quotients(self.q3)
        x, y = [1], [3]
        z = checker_word_inv(checker_pp_words([x, y])); u = checker_word_inv(checker_pp_words([y, x]))
        pairs = [(x, y), (x, z), (y, z), (u, x), (u, y), ([4], [6]),
                 (checker_pp_words([[1], [2]]), checker_pp_words([[5], [6]])),
                 ([1], [4]), (checker_pp_words([[2], [4]]), [6]),
                 ([1], checker_pp_words([[4], [5]]))]
        self.contexts = [{"index": i, "type": CONTEXT_TYPES[i], "id": CONTEXT_IDS[i], "tag": CONTEXT_TAGS[i],
                          "left": list(pair[0]), "right": list(pair[1])} for i, pair in enumerate(pairs)]
        self.actors: dict[tuple[int, int], CState] = {}
        for index in range(10):
            for letter in (1, -1, 2, -2):
                self.actors[index, letter] = self.direct((letter,), index); meter.bump("typed_context_products", 1, "checker.actor_cache")
            require(self.actors[index, -1].a == self.actors[index, 1].inv().a and
                    self.actors[index, -1].u == self.actors[index, 1].inv().u and
                    self.actors[index, -2].a == self.actors[index, 2].inv().a and
                    self.actors[index, -2].u == self.actors[index, 2].inv().u, "checker:actor_inverse_word")
        self.verify_canaries(authority.receipt)

    def quotient(self, index: int) -> Any: return self.e3 if self.contexts[index]["type"] == "E3" else self.e4

    def identity(self, index: int) -> CState: return CState(self.quotient(index), self.quotient(index).identity, {})

    def direct(self, word: Sequence[int], index: int) -> CState:
        self.meter.reserve("direct_replays", 1, "checker.direct_replay")
        self.meter.bump("direct_replays", 1, "checker.direct_replay")
        context = self.contexts[index]; quotient = self.quotient(index)
        substituted = checker_word_substitute(tuple(word), (context["left"], context["right"]))
        gradient, roof = checker_fox_gradient(substituted, quotient)
        self.meter.bump("quotient_reductions", max(1, len(substituted)), "checker.direct_affine")
        return CState(quotient, roof, {(int(key[0]), key[1]): int(value) % 3 for key, value in gradient.items() if int(value) % 3})

    def base(self, word: Sequence[int], index: int) -> CState:
        quotient = self.quotient(index); gradient, roof = checker_fox_gradient(tuple(word), quotient)
        self.meter.bump("quotient_reductions", max(1, len(word)), "checker.base_affine")
        return CState(quotient, roof, {(int(key[0]), key[1]): int(value) % 3 for key, value in gradient.items() if int(value) % 3})

    def row(self, states: Sequence[CState]) -> dict[str, int]:
        out: dict[str, int] = {}
        for index, state in enumerate(states):
            require(state.identity_roof(), "checker:row_roof")
            for (component, element), coefficient in state.u.items():
                out[row_key(index, component, element)] = (out.get(row_key(index, component, element), 0) + int(coefficient)) % 3
        return {key: value for key, value in out.items() if value}

    def verify_canaries(self, receipt: dict[str, Any]) -> None:
        canaries = receipt["evaluator"]["canaries"]
        require(set(canaries) == {"nonsplit_y_y_section_cocycle", "source_2_2", "x", "x_action_y",
                                  "x_inverse", "xy", "xy_section_cocycle", "y"}, "checker:canary_keyset")
        for name, letter in (("x", 1), ("y", 2), ("x_inverse", -1)):
            require(canaries[name]["value"] == [element_blob(self.actors[i, letter].a).hex() for i in range(10)],
                    "checker:canary:" + name)
        expected_xy = [element_blob(self.actors[i, 1].mul(self.actors[i, 2]).a).hex() for i in range(10)]
        require(canaries["xy"]["value"] == expected_xy, "checker:canary:xy")
        expected_action = [element_blob(self.actors[i, 1].mul(self.actors[i, 2]).mul(self.actors[i, -1]).a).hex() for i in range(10)]
        require(canaries["x_action_y"]["value"] == expected_action, "checker:canary:action")
        cocycle_word = word_mul([1], [2], word_inv([1, 2]))
        require(canaries["xy_section_cocycle"]["value"] == [element_blob(self.direct(cocycle_word, i).a).hex() for i in range(10)],
                "checker:canary:section_cocycle")
        source_word = canaries["source_2_2"].get("source_word"); require(isinstance(source_word, list), "checker:canary:source_word")
        require(canaries["source_2_2"]["value"] == [element_blob(self.direct(source_word, i).a).hex() for i in range(10)],
                "checker:canary:source_2_2")
        widths = receipt["evaluator"]["coordinate_widths"]
        for name in ("x", "y", "x_inverse", "xy", "x_action_y", "xy_section_cocycle", "source_2_2"):
            for i, value in enumerate(canaries[name]["value"]): require(len(bytes.fromhex(value)) == widths[i], "checker:canary_width")


class SuffixDAG:
    """Hash-consed reversed trie; state([g]+suffix)=actor(g)*state(suffix)."""
    def __init__(self, arithmetic: CheckerArithmetic, meter: Meter):
        self.arithmetic, self.meter = arithmetic, meter
        self.nodes = [{"edges": {}, "length": 0, "states": [arithmetic.identity(i) for i in range(10)]}]
        self.terminals: dict[tuple[int, ...], int] = {}
        # Missing inverse literals reuse the state of their authenticated
        # terminal inverse; no additional suffix edge is admitted.
        self.inverse_states: dict[tuple[int, ...], list[CState]] = {}

    def add(self, word: Sequence[int]) -> int:
        normalized = tuple(word_reduce(word))
        if normalized in self.terminals: return self.terminals[normalized]
        node = 0
        for letter in reversed(normalized):
            child = self.nodes[node]["edges"].get(int(letter))
            if child is None:
                self.meter.reserve("suffix_nodes", 1, "reverse_suffix_edge")
                self.meter.reserve("suffix_edges", 1, "reverse_suffix_edge")
                self.meter.reserve("suffix_edge_state_products", 10, "reverse_suffix_edge")
                states = [self.arithmetic.actors[i, int(letter)].mul(self.nodes[node]["states"][i]) for i in range(10)]
                child = len(self.nodes); self.nodes[node]["edges"][int(letter)] = child
                self.nodes.append({"edges": {}, "length": self.nodes[node]["length"] + 1, "letter": int(letter), "states": states})
                self.meter.bump("suffix_nodes", 1, "reverse_suffix_edge"); self.meter.bump("suffix_edges", 1, "reverse_suffix_edge")
                self.meter.bump("suffix_edge_state_products", 10, "reverse_suffix_edge")
            node = child
        self.terminals[normalized] = node; return node

    def state(self, word: Sequence[int], index: int) -> CState:
        # replay_ancestry has already produced a canonical reduced tuple;
        # suffix lookup must not reduce the same long primitive a second time.
        normalized = tuple(int(letter) for letter in word)
        require(all(letter in (-2, -1, 1, 2) for letter in normalized), "suffix:letter")
        if normalized in self.terminals:
            return self.nodes[self.terminals[normalized]]["states"][index]
        cached = self.inverse_states.get(normalized)
        if cached is None:
            inverse_literal = tuple(checker_word_inv(normalized))
            base = self.terminals.get(inverse_literal)
            require(base is not None, "suffix:unregistered_primitive")
            self.meter.reserve("typed_context_products", 10, "checker.suffix_inverse_primitive")
            cached = [state.inv() for state in self.nodes[base]["states"]]
            original = self.nodes[base]["states"]
            for left, right in zip(original, cached):
                product = left.mul(right)
                require(product.identity_roof() and not product.u,
                        "suffix:inverse_primitive_law")
            self.meter.bump("typed_context_products", 10, "checker.suffix_inverse_primitive")
            self.inverse_states[normalized] = cached
        return cached[index]


def primitive_inventory(authority: Authority) -> tuple[list[tuple[int, ...]], dict[str, Any]]:
    PRIMITIVE_WORDS.clear(); PRIMITIVE_INVERSES.clear()
    sections: set[tuple[int, ...]] = set(); records: set[tuple[int, ...]] = set(); qrels: set[tuple[int, ...]] = set()
    def register(value: Any, label: str) -> tuple[int, ...]:
        require(isinstance(value, (list, tuple)), label + ":shape")
        literal = tuple(int(item) for item in value)
        if literal not in PRIMITIVE_WORDS:
            require(tuple(word_reduce(literal)) == literal, label + ":reduced")
            PRIMITIVE_WORDS[literal] = literal; PRIMITIVE_INVERSES[literal] = word_inv(literal)
        return PRIMITIVE_WORDS[literal]
    for row in authority.rows:
        ancestry = row.get("ancestry", {})
        sections.add(register(ancestry.get("section_source_word", []), "checker:primitive_section_source"))
        sections.add(register(ancestry.get("section_target_word", []), "checker:primitive_section_target"))
        records.add(register(ancestry.get("record_word", []), "checker:primitive_record"))
        if isinstance(ancestry.get("q0_relator_word"), list):
            qrels.add(register(ancestry["q0_relator_word"], "checker:primitive_q0_relator"))
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for name, item in value.items():
                if name == "q0_relator_word" and isinstance(item, list):
                    qrels.add(register(item, "checker:primitive_q0_relator"))
                elif isinstance(item, (dict, list)): walk(item)
        elif isinstance(value, list):
            for item in value: walk(item)
    walk(authority.receipt.get("Q0", {})); walk(authority.receipt.get("bridge", {}))
    words = sorted(sections | records | qrels, key=lambda word: (len(word), word))
    require((len(sections), len(records), len(qrels), len(words)) == (243, 26, 19, 288), "checker:primitive_inventory")
    literal = sum(len(word) for word in words); by_layer = {layer: sum(len(row.get("word", [])) for row in authority.rows if row.get("layer") == layer) for layer in LAYERS}
    require(literal == 114458 and sum(by_layer.values()) == 5475488 and
            by_layer == {"Gamma_Cayley": 5433366, "action": 33206, "Q0_lift": 8916}, "checker:literal_inventory")
    return words, {"sections": len(sections), "records": len(records), "q0_relators": len(qrels),
                   "primitive_words": len(words), "literal_primitive_letters": literal,
                   "stored_row_letters": sum(by_layer.values()), "stored_row_letters_by_layer": by_layer}


def registered_primitive(value: Any, label: str) -> tuple[int, ...]:
    require(isinstance(value, (list, tuple)), label + ":shape")
    literal = tuple(int(item) for item in value)
    require(literal in PRIMITIVE_WORDS, label + ":unregistered")
    return PRIMITIVE_WORDS[literal]


def registered_inverse(value: Any, label: str) -> tuple[int, ...]:
    literal = registered_primitive(value, label)
    return PRIMITIVE_INVERSES[literal]


def replay_ancestry(row: dict[str, Any]) -> tuple[tuple[int, ...], list[tuple[int, ...]], dict[str, Any]]:
    ancestry = row.get("ancestry", {})
    record = registered_primitive(ancestry.get("record_word", []), "checker:ancestry_record")
    target = registered_primitive(ancestry.get("section_target_word", []), "checker:ancestry_target")
    source = registered_primitive(ancestry.get("section_source_word", []), "checker:ancestry_source")
    layer = row.get("layer")
    if layer == "Gamma_Cayley":
        parts = [source, record, registered_inverse(ancestry.get("section_target_word", []), "checker:ancestry_target")]
        expected = word_mul(*parts); grammar = "Gamma_Cayley"
    elif layer == "action":
        letter = int(row.get("letter")); require(letter in (-2, -1, 1, 2), "checker:action_letter")
        tokens = tuple(int(item) for item in ancestry.get("tokens", [])); orientation = int(row.get("orientation"))
        expected_tokens = ((-letter,) + record + (letter,) if orientation == 1 else (letter,) + record + (-letter,))
        require(tokens == expected_tokens, "checker:action_tokens")
        parts = [record, registered_inverse(ancestry.get("section_target_word", []), "checker:ancestry_target")]
        # `tokens` already is the conjugated record; only append the target
        # inverse.  Re-appending `record` would double the first action
        # factor and corrupt row 6,319 (the first action row).
        expected = word_mul(tokens, parts[1]); grammar = "action"
    elif layer == "Q0_lift":
        qrel = registered_primitive(ancestry.get("q0_relator_word", []), "checker:ancestry_q0_relator")
        parts = [qrel, registered_inverse(ancestry.get("section_target_word", []), "checker:ancestry_target")]
        expected = word_mul(*parts); grammar = "Q0_lift"
    else: raise Reject("checker:unknown_layer")
    # The authority pass proves reducedness once; row replay compares the
    # reconstructed literal directly and does not free-reduce 5.4M letters.
    require(expected == tuple(row.get("word", [])), "checker:stored_word_mismatch")
    return expected, parts, {"grammar": grammar, "parts": [list(part) for part in parts]}


class BoundarySeed:
    def __init__(self, index: int, context: int, relation: int, quotient: Any, occurrences: list[tuple[int, Any, int]]):
        self.index, self.context, self.relation, self.q = index, context, relation, quotient
        self.occurrences = occurrences; self.identity = raw_key(context, relation, quotient.identity)

    def translate(self, element: Any) -> dict[str, int]:
        return {row_key(self.context, component, self.q.mul(element, key)): int(value) % 3
                for component, key, value in self.occurrences if int(value) % 3}


class Boundary:
    """Checker-owned 65-family seed and matching-occurrence oracle."""
    def __init__(self, arithmetic: CheckerArithmetic, meter: Meter):
        self.arithmetic, self.meter = arithmetic, meter; self.seeds: list[BoundarySeed] = []
        self.by_component: dict[tuple[int, int], list[tuple[BoundarySeed, Any, int]]] = {}
        self.by_key: dict[tuple[int, int], BoundarySeed] = {}; self.inverses: dict[tuple[int, Any], Any] = {}
        self.psi_cache: dict[str, dict[str, int]] = {}; ordinal = 0
        for context in range(10):
            quotient = arithmetic.quotient(context); relations = checker_pure_relations(3 if context < 5 else 4)
            require(len(relations) == (2 if context < 5 else 11), "checker:typed_seed_count")
            for relation, word in enumerate(relations):
                state = arithmetic.base(word, context); require(state.identity_roof(), "checker:seed_roof")
                occurrences = [(component, element, coefficient) for (component, element), coefficient in state.u.items() if coefficient % 3]
                seed = BoundarySeed(ordinal, context, relation, quotient, occurrences); self.seeds.append(seed); self.by_key[context, relation] = seed
                for component, element, coefficient in occurrences:
                    self.by_component.setdefault((context, component), []).append((seed, element, coefficient))
                    self.inverses[context, element] = quotient.inverse(element)
                ordinal += 1; meter.bump("typed_context_products", 1, "checker.boundary_seed")
        require(len(self.seeds) == 65 and sum(seed.context < 5 for seed in self.seeds) == 10 and
                sum(seed.context >= 5 for seed in self.seeds) == 55, "checker:65_seed_roster")

    def psi(self, ledger: dict[str, int]) -> dict[str, int]:
        ident = digest(ledger)
        if ident in self.psi_cache: return self.psi_cache[ident]
        out: dict[str, int] = {}
        for key, coefficient in ledger.items():
            context, relation, text = split_key(key); seed = self.by_key.get((context, relation))
            require(seed is not None, "checker:ledger_seed_key")
            out = add_sparse(out, seed.translate(decode_token(text)), coefficient); self.meter.bump("canonicalization", 1, "checker.psi_once")
        self.psi_cache[ident] = out; return out

    def act(self, ledger: dict[str, int], actors: Sequence[Any]) -> dict[str, int]:
        out: dict[str, int] = {}
        self.meter.reserve("affine_sparse_ops", len(ledger), "checker.ledger_action")
        for key, coefficient in ledger.items():
            context, relation, text = split_key(key); moved = self.arithmetic.quotient(context).mul(actors[context], decode_token(text))
            target = raw_key(context, relation, moved); out[target] = (out.get(target, 0) + int(coefficient)) % 3
        self.meter.bump("affine_sparse_ops", len(ledger), "checker.ledger_action")
        return {key: value for key, value in out.items() if value}


class Echelon:
    def __init__(self, meter: Meter):
        self.meter = meter; self.rows: dict[str, dict[str, int]] = {}; self.labels: dict[str, str] = {}; self.pivots: list[str] = []

    def reduce(self, value: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        remainder = {key: int(raw) % 3 for key, raw in value.items() if int(raw) % 3}; coefficients: dict[str, int] = {}
        for pivot in self.pivots:
            factor = remainder.get(pivot, 0)
            if factor:
                remainder = add_sparse(remainder, self.rows[pivot], -factor)
                label = self.labels[pivot]; coefficients[label] = (coefficients.get(label, 0) + factor) % 3
                self.meter.bump("membership_reductions", 1, "checker.echelon_reduce")
        return remainder, {key: raw for key, raw in coefficients.items() if raw}

    def insert(self, value: dict[str, int], label: str) -> dict[str, Any] | None:
        remainder, old = self.reduce(value)
        if not remainder: return None
        pivot = min(remainder); scale = 1 if remainder[pivot] == 1 else 2
        stored = scale_sparse(remainder, scale); self.rows[pivot] = stored; self.labels[pivot] = label
        # The pivot list is the actual elimination order; sorting would make
        # a later small pivot reintroduce an earlier coordinate.
        self.pivots.append(pivot)
        self.meter.bump("affine_sparse_ops", 1, "checker.echelon_insert")
        relation = {label: scale}; relation.update({key: (-scale * raw) % 3 for key, raw in old.items()})
        return {"pivot": pivot, "scale": scale, "row": stored, "reduction": old,
                "relation": {key: raw for key, raw in relation.items() if raw}}

    def replay(self, coefficients: dict[str, int], roster: dict[str, dict[str, int]]) -> dict[str, int]:
        out: dict[str, int] = {}
        for label, coefficient in coefficients.items():
            require(label in roster, "checker:relation_label"); out = add_sparse(out, roster[label], coefficient)
        return out


class Basis:
    def __init__(self, boundary: Boundary, meter: Meter):
        self.boundary, self.meter = boundary, meter; self.combined = Echelon(meter); self.bspace = Echelon(meter)
        self.b_rows: dict[str, dict[str, int]] = {}; self.b_ledgers: dict[str, dict[str, int]] = {}
        self.boundary_ledgers: dict[str, dict[str, int]] = {}; self.combined_ledgers: dict[str, dict[str, int]] = {}
        self.b_coefficients: dict[str, dict[str, int]] = {}; self.b_formals: dict[str, tuple[dict[str, int], dict[str, int]]] = {}
        self.k_rows: dict[str, dict[str, int]] = {}; self.k_items: list[dict[str, Any]] = []
        self.active_registry: set[str] = set()
        self.insertion_events: list[dict[str, Any]] = []

    def add_boundary(self, column: dict[str, int], raw_identity: str) -> dict[str, Any]:
        remainder, old = self.bspace.reduce(column); require(remainder, "checker:boundary_not_new")
        pivot = min(remainder); scale = 1 if remainder[pivot] == 1 else 2; label = f"B:{len(self.b_rows)}"
        ledger = {raw_identity: 1}
        for old_label, coefficient in old.items(): ledger = add_sparse(ledger, self.boundary_ledgers[old_label], -coefficient)
        ledger, stored = scale_sparse(ledger, scale), scale_sparse(remainder, scale)
        inserted = self.bspace.insert(column, label); require(inserted is not None and inserted["row"] == stored, "checker:boundary_replay")
        combined = self.combined.insert(stored, label); require(combined is not None, "checker:boundary_combined")
        combined_ledger = scale_sparse(ledger, combined["scale"]); combined_coefficients: dict[str, int] = {}
        for old_label, coefficient in combined["reduction"].items():
            require(old_label in self.b_formals, "checker:combined_formal_old")
            old_q, old_c = self.b_formals[old_label]
            combined_ledger = add_sparse(combined_ledger, old_q, -combined["scale"] * coefficient)
            combined_coefficients = add_sparse(combined_coefficients, old_c, -combined["scale"] * coefficient)
        self.b_rows[label], self.b_ledgers[label] = combined["row"], combined_ledger
        self.b_coefficients[label] = combined_coefficients; self.b_formals[label] = (combined_ledger, combined_coefficients)
        self.boundary_ledgers[label], self.combined_ledgers[label] = ledger, combined_ledger
        self.active_registry.update(combined["row"])
        self.insertion_events.append({"kind": "B", "label": label, "column": column,
                                      "raw_identity": raw_identity, "boundary_row": stored,
                                      "combined_row": combined["row"], "boundary_pivot": pivot,
                                      "boundary_scale": scale, "boundary_reduction": old,
                                      "combined_detail": combined})
        self.meter.bump("boundary_rank_rises", 1, "checker.boundary_rank_rise")
        return {"label": label, "row": stored, "ledger": ledger, "pivot": combined["pivot"], "scale": scale, "raw_identity": raw_identity}

    def add_k(self, row: dict[str, int], label: str, word: Sequence[int], ledger: dict[str, int], node: int,
              states: Sequence[CState], ancestry: dict[str, Any]) -> dict[str, Any]:
        self.meter.reserve("active_keys", len(row), "checker.kernel_rank_rise")
        detail = self.combined.insert(row, label); require(detail is not None and not detail["reduction"], "checker:k_not_strict_rank_rise")
        self.combined_ledgers[label] = {}; self.b_formals[label] = ({}, {label: 1})
        flattened: dict[str, int] = {}
        for index, state in enumerate(states): flattened = add_sparse(flattened, local_row(index, state.u))
        normalized_flattened = add_sparse(flattened, self.boundary.psi(ledger), -1)
        require(normalized_flattened == detail["row"], "checker:rho1_normalized_K_row")
        item = {"label": label, "row": detail["row"], "word": list(word), "discrepancy": ledger,
                "pivot": detail["pivot"], "rank": self.rank(), "raw_coefficients": detail["relation"], "word_node": node,
                "rho0": [element_blob(state.a).hex() for state in states],
                "rho1": [{"roof": element_blob(state.a).hex(), "fox": local_row(index, state.u)}
                         for index, state in enumerate(states)], "rho1_flattened": normalized_flattened,
                "rho1_actual_flattened": flattened,
                "q": list(h2_word(word)), "ancestry": ancestry}
        self.k_rows[label], self.k_items = detail["row"], self.k_items + [item]
        self.active_registry.update(detail["row"])
        self.meter.bump("active_keys", len(detail["row"]), "checker.kernel_rank_rise")
        self.insertion_events.append({"kind": "K", "label": label, "row": row,
                                      "combined_detail": detail})
        return item

    def rank(self) -> int: return len(self.combined.pivots)

    def roster(self) -> dict[str, dict[str, int]]: return {**self.b_rows, **self.k_rows}

    def expand_correction(self, correction: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        boundary_q: dict[str, int] = {}; k_coefficients: dict[str, int] = {}
        for label, coefficient in correction.items():
            if label.startswith("B:"):
                require(label in self.b_formals, "checker:formal_boundary_label")
                q_value, c_value = self.b_formals[label]
                boundary_q = add_sparse(boundary_q, q_value, coefficient)
                k_coefficients = add_sparse(k_coefficients, c_value, coefficient)
            else:
                k_coefficients[label] = (k_coefficients.get(label, 0) + int(coefficient)) % 3
        return boundary_q, {label: value for label, value in k_coefficients.items() if value}


def dual_pullback(basis: Basis, target: dict[str, int], meter: Meter) -> tuple[dict[str, int], int]:
    remainder, _ = basis.combined.reduce(target); require(remainder, "checker:dual_member_target")
    active = set(target) | set(basis.active_registry)
    free = min(remainder); dual: dict[str, int] = {free: 1}
    # MaxPivot pullback is checked below; the actual pullback walks inverse
    # operation order, i.e. the reverse of the ascending pivot elimination.
    for pivot in reversed(basis.combined.pivots):
        dot = sum(int(value) * dual.get(key, 0) for key, value in basis.combined.rows[pivot].items()) % 3
        if dot: dual[pivot] = (-dot) % 3
    dual = {key: value for key, value in dual.items() if value % 3}; require(set(dual) <= active, "checker:dual_active_registry")
    for row in basis.combined.rows.values(): require(sum(int(value) * dual.get(key, 0) for key, value in row.items()) % 3 == 0, "checker:dual_live_dots")
    target_dot = sum(int(value) * dual.get(key, 0) for key, value in target.items()) % 3; require(target_dot != 0, "checker:dual_target_dot")
    meter.bump("dual_support", len(dual), "checker.dual_pullback"); return dual, target_dot


def correlate(boundary: Boundary, dual: dict[str, int], meter: Meter) -> dict[str, Any]:
    accum: dict[tuple[int, int, str], int] = {}; pairs = 0
    expected_pairs = sum(len(boundary.by_component.get(split_key(key)[:2], ()))
                         for key in dual)
    meter.reserve("correlation_pairs", expected_pairs, "checker.full_D_correlation")
    for key, coefficient in dual.items():
        context, component, text = split_key(key); g = decode_token(text)
        for seed, h, seed_coefficient in boundary.by_component.get((context, component), []):
            inverse_h = boundary.inverses[context, h]; translation = seed.q.mul(g, inverse_h)
            require(seed.q.mul(translation, h) == g, "checker:translation_product")
            target = (context, seed.relation, token(translation)); accum[target] = (accum.get(target, 0) + int(coefficient) * int(seed_coefficient)) % 3
            pairs += 1
    require(pairs == expected_pairs, "checker:correlation_pair_count")
    meter.bump("correlation_pairs", pairs, "checker.full_D_correlation")
    nonzero = sorted(((key, value) for key, value in accum.items() if value), key=lambda item: item[0])
    return {"pair_count": pairs, "accumulator_digest": digest(sorted((list(key), value) for key, value in accum.items())),
            "selected": ([nonzero[0][0][0], nonzero[0][0][1], nonzero[0][0][2], nonzero[0][1]] if nonzero else None),
            "complete": True}


def maxpivot_arithmetic_canary() -> dict[str, Any]:
    rows = {"a": {"a": 1, "b": 1, "c": 1}, "b": {"b": 1, "c": 1}}
    def pull(order: Sequence[str]) -> dict[str, int]:
        value = {"c": 1}
        for pivot in order:
            dot = sum(int(coefficient) * value.get(key, 0) for key, coefficient in rows[pivot].items()) % 3
            if dot: value[pivot] = (-dot) % 3
        return value
    wrong, correct = pull(("a", "b")), pull(("b", "a"))
    require(wrong != correct, "checker:maxpivot_canary_not_noncommuting")
    return {"wrong_descending": wrong, "correct_inverse_order": correct, "differ": True}


def h2_mul(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = left; ap, bp, rp = right
    return ((a + ap) % 9, (b + bp) % 9, (r + rp - b * ap) % 9)


def h2_inv(value: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = value; return ((-a) % 9, (-b) % 9, (-r - a * b) % 9)


def h2_word(word: Iterable[int]) -> tuple[int, int, int]:
    result = (0, 0, 0); generators = {1: (1, 0, 0), 2: (0, 1, 0)}
    for raw in word:
        base = generators[abs(int(raw))]; result = h2_mul(result, base if raw > 0 else h2_inv(base))
    return result


def compact_terminal_record(record: dict[str, Any]) -> dict[str, Any]:
    """Retain R:* terminals without duplicating completed sparse vectors.

    ZERO is the canonical owner for the K item created from that query, so
    its Q/c/s/word relation remains lossless.  Other completed row terminals
    retain only bounded identity/rank fields; action records remain full.
    """
    if record.get("schema") == "ZERO_CORRELATION/K_RANK_RISE":
        return {key: record[key] for key in (
            "schema", "query_id", "rank", "remainder", "normalization_scale",
            "normalized", "Q", "c", "B_coefficients", "candidate_word",
            "candidate_discrepancy", "row_digest", "target_digest",
            "discrepancy_digest", "dual_digest", "target_dot", "dual_support_digest",
            "pair_count", "accumulator_digest", "selected", "correlation_complete"
        ) if key in record} | {"terminal": True}
    return {"schema": record["schema"], "query_id": record["query_id"],
            "rank": record.get("rank", record.get("rank_after", 0)),
            "row_digest": record.get("row_digest"), "terminal": True}


def is_row_terminal(record: dict[str, Any]) -> bool:
    return (str(record.get("query_id", "")).startswith("R:") and
            record.get("schema") in ("MEMBER", "ZERO_CORRELATION/K_RANK_RISE"))


class Oracle:
    def __init__(self, arithmetic: CheckerArithmetic, boundary: Boundary, meter: Meter):
        self.arithmetic, self.boundary, self.meter = arithmetic, boundary, meter
        self.basis = Basis(boundary, meter); self.records: list[dict[str, Any]] = []
        self.live_duals: list[dict[str, Any]] = []; self.event_chain: list[dict[str, Any]] = []
        self.dual_chain: list[dict[str, Any]] = []; self.bridge_chain: list[str] = []
        self.epoch = "0" * 64

    def query(self, target: dict[str, int], discrepancy: dict[str, int], word: Sequence[int], query_id: str) -> dict[str, Any]:
        self.meter.bump("membership_queries", 1, "checker.quotient_query")
        while True:
            remainder, correction = self.basis.combined.reduce(target)
            if not remainder:
                replay = self.basis.combined.replay(correction, self.basis.roster()); require(replay == target, "checker:member_replay")
                boundary_q, k_coefficients = self.basis.expand_correction(correction)
                result = {"schema": "MEMBER", "query_id": query_id, "rank": self.basis.rank(), "coefficients": correction,
                          "boundary_Q": boundary_q, "K_coefficients": k_coefficients,
                          "row_digest": digest(target)}; self.record(result); return result
            dual, target_dot = dual_pullback(self.basis, target, self.meter); correlation = correlate(self.boundary, dual, self.meter)
            if not self.live_duals:
                # Keep one bounded actual dual sample.  The complete history
                # is represented by dual_event_chain/epoch digest entries.
                self.live_duals.append({"query_id": query_id, "dual": dict(dual),
                                        "target": dict(target), "target_dot": target_dot,
                                        "correlation": correlation})
            dual_digest = digest({"query_id": query_id, "dual": sorted(dual.items()),
                                  "target": target, "target_dot": target_dot,
                                  "correlation": correlation})
            self.dual_chain.append({"index": len(self.dual_chain) + 1,
                                    "query_id": query_id, "digest": dual_digest})
            if correlation["selected"] is not None:
                context, relation, text, coefficient = correlation["selected"]; seed = self.boundary.by_key[context, relation]
                translated = decode_token(text); column = seed.translate(translated); raw_identity = raw_key(context, relation, translated)
                self.meter.reserve("active_keys", len(column), "checker.boundary_rank_rise")
                added = self.basis.add_boundary(column, raw_identity)
                self.meter.bump("active_keys", len(column), "checker.boundary_rank_rise")
                result = {"schema": "BOUNDARY_RANK_RISE", "query_id": query_id, "rank_before": self.basis.rank() - 1,
                          "rank_after": self.basis.rank(), "selected": [context, relation, text, coefficient],
                          "column_digest": digest(column), "ledger_digest": digest(added["ledger"]),
                          "dual_digest": digest(sorted(dual.items())), "pair_count": correlation["pair_count"],
                          "accumulator_digest": correlation["accumulator_digest"]}; self.record(result); continue
            q, c = self.basis.expand_correction(correction)
            pivot = min(remainder); scale = 1 if remainder[pivot] == 1 else 2
            result = {"schema": "ZERO_CORRELATION/K_RANK_RISE", "query_id": query_id, "rank": self.basis.rank(),
                      "remainder": remainder, "normalization_scale": scale, "normalized": scale_sparse(remainder, scale),
                      "Q": q, "c": c, "B_coefficients": {label: value for label, value in correction.items() if label.startswith("B:")},
                      "candidate_word": list(word), "candidate_discrepancy": discrepancy,
                      "target_digest": digest(target), "discrepancy_digest": digest(discrepancy),
                      "dual_digest": digest(sorted(dual.items())), "target_dot": target_dot,
                      "pair_count": correlation["pair_count"], "accumulator_digest": correlation["accumulator_digest"],
                      "selected": None, "dual_support_digest": digest(sorted(dual.items())),
                      "correlation_complete": correlation.get("complete") is True}; self.record(result); return result

    def record(self, value: dict[str, Any]) -> None:
        stored = compact_terminal_record(value) if is_row_terminal(value) else value
        record_digest = digest(stored); self.records.append(stored)
        self.event_chain.append({"index": len(self.event_chain) + 1,
                                 "query_id": value["query_id"], "schema": value["schema"],
                                 "digest": record_digest})
        self.epoch = sha((self.epoch + record_digest).encode("ascii"))


def local_row(context: int, value: dict[tuple[int, Any], int]) -> dict[str, int]:
    out: dict[str, int] = {}
    for (component, element), coefficient in value.items():
        key = row_key(context, component, element); out[key] = (out.get(key, 0) + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


# Independently reconstructed literal owner fields for the task198 bridge.
# The checker does not import the producer's ledger or trace helper.
CHECKER_BRIDGE_TEN_TO_ELEVEN = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
CHECKER_BRIDGE_DELETE_DUPLICATE = (0, 1, 2, 3, 5, 6, 7, 8, 9, 10)
CHECKER_BRIDGE_REINSERT = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
CHECKER_BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 0, 4), (5,), (6,), (7,), (8,), (9,))
CHECKER_BRIDGE_OWNER_LAYOUT = (
    ("H1", 1, 1, "H1_fxy", "E3", 0, 21, "hexagon_fxy", 1, "direct", (3, 2)),
    ("H1", 1, 2, "H1_fxz", "E3", 1, 22, "hexagon_fxz", -1, "inverse", (3,)),
    ("H1", 1, 3, "H1_fyz", "E3", 2, 23, "hexagon_fyz", 1, "direct", ()),
    ("H2", 2, 1, "H2_fux", "E3", 3, 24, "hexagon_fux", -1, "inverse", (6, 5)),
    ("H2", 2, 2, "H2_fxy", "E3", 0, 21, "hexagon_fxy", -1, "inverse", (6,)),
    ("H2", 2, 3, "H2_fuy", "E3", 4, 25, "hexagon_fuy", 1, "direct", ()),
    ("P1", 3, 1, "P_b1", "E4", 5, 1, "pentagon_b1", 1, "direct", (11, 10, 9, 8)),
    ("P2", 4, 1, "P_b2", "E4", 6, 27, "pentagon_b2", 1, "direct", (11, 10, 9)),
    ("P3", 5, 1, "P_b3", "E4", 7, 21, "pentagon_b3", 1, "direct", (11, 10)),
    ("P5", 6, 1, "P_b5_inverse", "E4", 8, 26, "pentagon_b5_inverse_slot", -1, "inverse", (11,)),
    ("P4", 7, 1, "P_b4_inverse", "E4", 9, 28, "pentagon_b4_inverse_slot", -1, "inverse", ()),
)


def checker_bridge_trace(states: Sequence[CState], word: Sequence[int], row: dict[str, Any],
                         authority: Authority, meter: Meter) -> dict[str, Any]:
    """Independently factor the bridge trace from the live ten-state pass."""
    require(len(states) == 10, "checker:bridge_ten_arity")
    owner = authority.receipt.get("bridge", {}).get("occurrence_ledger", [])
    require(len(owner) == len(CHECKER_BRIDGE_OWNER_LAYOUT) == 11,
            "checker:bridge_occurrence_owner_count")
    occurrences = []
    for index, item in enumerate(owner):
        expected = CHECKER_BRIDGE_OWNER_LAYOUT[index]
        actual = (item.get("block"), int(item.get("block_index")), int(item.get("block_slot")),
                  item.get("occurrence"), item.get("type"), int(item.get("ten_index")),
                  int(item.get("context_id")), item.get("role"), int(item.get("factor_sign")),
                  item.get("orientation"), tuple(item.get("fox_prefix_occurrences", ())))
        require(int(item.get("ordinal")) == index + 1 and actual == expected and
                expected[5] == CHECKER_BRIDGE_TEN_TO_ELEVEN[index],
                "checker:bridge_literal_occurrence_owner")
        coordinate = authority.task176.get("coordinates", [])[expected[5]]
        require((item.get("type"), int(item.get("context_id")), item.get("role")) ==
                (coordinate.get("type"), int(coordinate.get("context_id")), coordinate.get("role")),
                "checker:bridge_typed_coordinate_owner")
    ten_blobs = [element_blob(state.a).hex() for state in states]
    eleven_blobs = [ten_blobs[index] for index in CHECKER_BRIDGE_TEN_TO_ELEVEN]
    seven_blobs = [[eleven_blobs[index] for index in block]
                   for block in CHECKER_BRIDGE_SEVEN_BLOCKS]
    deleted_blobs = [eleven_blobs[index] for index in CHECKER_BRIDGE_DELETE_DUPLICATE]
    reinserted_blobs = [deleted_blobs[index] for index in CHECKER_BRIDGE_REINSERT]
    flattened_blobs = [blob for block in seven_blobs for blob in block]
    require(eleven_blobs[0] == eleven_blobs[4] and deleted_blobs == ten_blobs and
            reinserted_blobs == eleven_blobs and flattened_blobs == eleven_blobs,
            "checker:bridge_inverse_replay")
    for item in owner:
        ordinal = int(item["ordinal"]); ten_index = int(item["ten_index"])
        occurrences.append({"block": item["block"], "block_index": int(item["block_index"]),
                            "block_slot": int(item["block_slot"]), "context_id": int(item["context_id"]),
                            "factor_sign": int(item["factor_sign"]),
                            "fox_prefix_occurrences": list(item["fox_prefix_occurrences"]),
                            "occurrence": item["occurrence"], "ordinal": ordinal,
                            "orientation": item["orientation"], "role": item["role"],
                            "ten_index": ten_index, "type": item["type"],
                            "ten_spelling": ten_blobs[ten_index],
                            "eleven_spelling": eleven_blobs[ordinal - 1]})
        meter.bump("bridge_occurrences", 1, "checker.bridge_literal_occurrence")
    meter.bump("bridge_rows", 1, "checker.bridge_row_replay")
    core = {"label": f"relator:{row['layer']}:{row['ordinal']}", "word": list(word),
            "word_sha256": digest(list(word)), "ten_sha256": digest(ten_blobs),
            "eleven_sha256": digest(eleven_blobs), "seven_sha256": digest(seven_blobs),
            "occurrence_values_sha256": digest([eleven_blobs[item["ordinal"] - 1]
                                                 for item in owner]),
            "left_inverse": deleted_blobs == ten_blobs,
            "image_inverse": reinserted_blobs == eleven_blobs,
            "regroup_inverse": flattened_blobs == eleven_blobs}
    core["occurrence_owner_sha256"] = digest(occurrences)
    core["bridge_trace_digest"] = digest({key: core[key] for key in
                                           ("label", "word", "word_sha256", "ten_sha256",
                                            "eleven_sha256", "seven_sha256",
                                            "occurrence_values_sha256", "left_inverse",
                                            "image_inverse", "regroup_inverse")})
    return core


class WordNodeDAG:
    """Checker-owned persistent state/ledger DAG with pre-expansion cap."""
    def __init__(self, arithmetic: CheckerArithmetic, meter: Meter, cap: int = 4000000):
        self.arithmetic, self.meter, self.cap = arithmetic, meter, cap; self.nodes: list[dict[str, Any]] = []
        self.interned: dict[tuple[Any, ...], int] = {}; self.literal_cache: dict[int, tuple[int, ...]] = {}

    def new(self, key: tuple[Any, ...], value: dict[str, Any]) -> int:
        if key in self.interned: return self.interned[key]
        self.meter.reserve("word_nodes", 1, "checker.word_node")
        ident = len(self.nodes); self.interned[key] = ident; self.nodes.append(value); self.meter.bump("word_nodes", 1, "checker.word_node"); return ident

    def _charge_affine(self, amount: int, phase: str) -> None:
        if amount:
            self.meter.reserve("affine_sparse_ops", int(amount), phase)
            self.meter.bump("affine_sparse_ops", int(amount), phase)

    def _charge_context(self, amount: int, phase: str) -> None:
        if amount:
            self.meter.reserve("typed_context_products", int(amount), phase)
            self.meter.bump("typed_context_products", int(amount), phase)

    def source(self, word: Sequence[int]) -> int:
        literal = tuple(word_reduce(word)); key = ("source", literal)
        if key in self.interned: return self.interned[key]
        states = [self.arithmetic.direct(literal, i) for i in range(10)]
        return self.new(key, {"op": "source", "word": list(literal), "length": len(literal), "states": states, "ledger": {}})

    def product(self, children: Sequence[int]) -> int:
        ids = tuple(int(child) for child in children)
        require(all(0 <= child < len(self.nodes) for child in ids), "checker:word_child")
        length = sum(self.nodes[child]["length"] for child in ids); require(length <= self.cap, "checker:word_length_cap")
        key = ("product", ids)
        if key in self.interned: return self.interned[key]
        self._charge_context(10 * len(ids), "checker.word_product_state_products")
        self._charge_affine(sum(len(self.nodes[x]["ledger"]) for x in ids),
                            "checker.word_product_ledger_add")
        states = [self.arithmetic.identity(i) for i in range(10)]; ledger: dict[str, int] = {}
        for child in ids:
            states = [states[i].mul(self.nodes[child]["states"][i]) for i in range(10)]; ledger = add_sparse(ledger, self.nodes[child]["ledger"])
        return self.new(key, {"op": "product", "children": list(ids), "length": length, "states": states, "ledger": ledger})

    def inverse(self, child: int) -> int:
        require(0 <= child < len(self.nodes), "checker:word_child")
        key = ("inverse", child)
        if key in self.interned: return self.interned[key]
        node = self.nodes[child]
        self._charge_context(10, "checker.word_inverse_state_products")
        self._charge_affine(len(node["ledger"]), "checker.word_inverse_ledger")
        return self.new(key, {"op": "inverse", "child": child, "length": node["length"],
                         "states": [state.inv() for state in node["states"]], "ledger": scale_sparse(node["ledger"], -1)})

    def power(self, child: int, exponent: int) -> int:
        require(exponent in (0, 1, 2), "checker:word_power")
        if exponent == 0: return self.source(())
        return self.product([child] * exponent)

    def attach_ledger(self, child: int, ledger: dict[str, int]) -> int:
        require(0 <= child < len(self.nodes), "checker:word_child")
        key = ("ledger_attach", child, digest(ledger))
        if key in self.interned: return self.interned[key]
        self._charge_affine(len(ledger), "checker.word_attach_affine")
        return self.new(key, {"op": "ledger_attach", "child": child,
                          "length": self.nodes[child]["length"], "states": self.nodes[child]["states"], "ledger": ledger})

    def conjugate(self, letter: int, child: int) -> int:
        require(letter in (-2, -1, 1, 2) and 0 <= child < len(self.nodes), "checker:word_conjugate_owner")
        node_key = ("conjugate", letter, child)
        if node_key in self.interned: return self.interned[node_key]
        actor = self.new(("actor", letter), {"op": "actor", "letter": letter, "length": 1,
                                             "states": [self.arithmetic.actors[i, letter] for i in range(10)], "ledger": {}})
        inverse = self.new(("actor", -letter), {"op": "actor", "letter": -letter, "length": 1,
                                                "states": [self.arithmetic.actors[i, -letter] for i in range(10)], "ledger": {}})
        # Do not retain an untranslated actor*child*actor^-1 product
        # intermediate; every checkpoint-visible node owns its true ledger.
        self._charge_context(20, "checker.word_conjugate_state_products")
        states = [self.arithmetic.actors[i, letter].mul(self.nodes[child]["states"][i]).mul(
                  self.arithmetic.actors[i, -letter]) for i in range(10)]
        translated: dict[str, int] = {}
        self.meter.reserve("affine_sparse_ops", 10 * len(self.nodes[child]["ledger"]),
                           "checker.word_conjugate_affine")
        for ledger_key, coefficient in self.nodes[child]["ledger"].items():
            context, relation, text = split_key(ledger_key)
            moved = self.arithmetic.quotient(context).mul(self.arithmetic.actors[context, letter].a, decode_token(text))
            target = raw_key(context, relation, moved)
            translated[target] = (translated.get(target, 0) + int(coefficient)) % 3
        self.meter.bump("affine_sparse_ops", 10 * len(self.nodes[child]["ledger"]),
                        "checker.word_conjugate_affine")
        return self.new(node_key, {"op": "conjugate", "letter": letter, "child": child,
                         "length": self.nodes[child]["length"] + 2, "states": states,
                         "ledger": {key: value for key, value in translated.items() if value}})

    def literal(self, node: int) -> tuple[int, ...]:
        if node in self.literal_cache: return self.literal_cache[node]
        require(0 <= int(node) < len(self.nodes), "checker:materialize_node")
        pending: list[tuple[int, bool]] = [(int(node), False)]
        while pending:
            ident, ready = pending.pop()
            if ident in self.literal_cache: continue
            item = self.nodes[ident]; op = item["op"]
            children = ([int(item["child"])] if op in {"inverse", "ledger_attach", "conjugate"} else
                        [int(value) for value in item.get("children", [])] if op == "product" else [])
            require(all(0 <= child < len(self.nodes) for child in children), "checker:materialize_child")
            require(int(item.get("length", 0)) <= self.cap, "checker:expanded_word_cap")
            if not ready:
                pending.append((ident, True))
                for child in reversed(children):
                    if child not in self.literal_cache: pending.append((child, False))
                continue
            if op == "source": out = tuple(item["word"])
            elif op == "actor": out = (int(item["letter"]),)
            elif op == "inverse": out = word_inv(self.literal_cache[children[0]])
            elif op == "ledger_attach": out = self.literal_cache[children[0]]
            elif op == "conjugate": out = word_mul((int(item["letter"]),), self.literal_cache[children[0]],
                                                    (-int(item["letter"]),))
            else: out = word_mul(*(self.literal_cache[child] for child in children))
            # Product/inverse/conjugate lengths are safe pre-expansion upper
            # bounds; free reduction may cancel at their joins.  The
            # memoized literal is the exact reduced spelling after this
            # capped assembly.
            require(len(out) <= int(item["length"]) and len(out) <= self.cap,
                    "checker:expanded_word_cap")
            self.meter.bump("expanded_letters", len(out), "checker.word_materialize")
            self.literal_cache[ident] = out
        return self.literal_cache[node]


def restore_word_dag(words: WordNodeDAG, saved: list[dict[str, Any]]) -> None:
    """Restore the checker DAG topologically, without replaying authority rows."""
    require(isinstance(saved, list), "checker:checkpoint_word_dag_shape")
    for ident, record in enumerate(saved):
        require(isinstance(record, dict), "checker:checkpoint_word_dag_node_shape")
        op = record.get("op")
        required = {"source": {"op", "word", "length", "ledger"},
                    "actor": {"op", "letter", "length", "ledger"},
                    "product": {"op", "children", "length", "ledger"},
                    "inverse": {"op", "child", "length", "ledger"},
                    "ledger_attach": {"op", "child", "length", "ledger"},
                    "conjugate": {"op", "letter", "child", "length", "ledger"}}.get(op)
        require(required is not None and set(record) == required, "checker:checkpoint_word_dag_node_fields")
        if op == "source":
            node = words.source(record.get("word", []))
            # Source nodes in the checker have no mutable discrepancy ledger.
            require(record.get("ledger", {}) == {}, "checker:checkpoint_source_ledger")
        elif op == "actor":
            letter = int(record.get("letter")); require(letter in (-2, -1, 1, 2),
                                                        "checker:checkpoint_actor_letter")
            node = words.new(("actor", letter), {"op": "actor", "letter": letter,
                "length": 1, "states": [words.arithmetic.actors[i, letter] for i in range(10)],
                "ledger": {}})
        elif op == "product":
            node = words.product(record.get("children", []))
        elif op == "inverse":
            node = words.inverse(int(record.get("child", -1)))
        elif op == "ledger_attach":
            node = words.attach_ledger(int(record.get("child", -1)), record.get("ledger", {}))
        elif op == "conjugate":
            node = words.conjugate(int(record.get("letter")), int(record.get("child", -1)))
        else:
            raise Reject("checker:checkpoint_word_dag_opcode")
        require(node == ident, "checker:checkpoint_word_dag_topology")
        actual = words.nodes[node]
        for key in required: require(actual.get(key) == record[key], "checker:checkpoint_word_dag_node:" + key)


def restore_basis(basis: Basis, state: dict[str, Any], words: WordNodeDAG | None = None) -> None:
    """Rebuild checker echelons and bind every owner to its event/DAG node."""
    boundary_state = state.get("boundary_echelon", {})
    combined_state = state.get("echelon_rebuild", {})
    events = state.get("insertion_events", [])
    require(isinstance(boundary_state, dict) and isinstance(combined_state, dict) and
            isinstance(events, list) and isinstance(state.get("B_roster"), dict) and
            isinstance(state.get("B_ledgers"), dict) and isinstance(state.get("boundary_ledgers"), dict) and
            isinstance(state.get("combined_ledgers"), dict) and isinstance(state.get("B_coefficients"), dict) and
            isinstance(state.get("B_formals"), dict) and isinstance(state.get("K_roster"), list),
            "checker:checkpoint_echelon_state_shape")
    saved_b_rows = dict(state["B_roster"]); saved_b_ledgers = dict(state["B_ledgers"])
    saved_boundary_ledgers = dict(state["boundary_ledgers"]); saved_combined_ledgers = dict(state["combined_ledgers"])
    saved_b_coefficients = dict(state["B_coefficients"])
    saved_formals = {str(label): (pair[0], pair[1]) for label, pair in state["B_formals"].items()}
    saved_items = list(state["K_roster"]); saved_by_label = {str(item.get("label")): item for item in saved_items}
    saved_records = {str(record.get("query_id")): record
                     for record in state.get("oracle_records", [])
                     if isinstance(record, dict) and record.get("query_id") is not None}
    require(len(saved_by_label) == len(saved_items), "checker:K_duplicate_label")
    rebuilt_boundary = Echelon(basis.meter); rebuilt_combined = Echelon(basis.meter)
    derived_b_rows: dict[str, dict[str, int]] = {}; derived_b_ledgers: dict[str, dict[str, int]] = {}
    derived_boundary_ledgers: dict[str, dict[str, int]] = {}; derived_combined_ledgers: dict[str, dict[str, int]] = {}
    derived_b_coefficients: dict[str, dict[str, int]] = {}
    derived_formals: dict[str, tuple[dict[str, int], dict[str, int]]] = {}
    derived_k_rows: dict[str, dict[str, int]] = {}; derived_items: list[dict[str, Any]] = []
    derived_active: set[str] = set()
    next_b_label = 0; next_k_label = 0
    for event in events:
        require(isinstance(event, dict) and event.get("label"), "checker:checkpoint_echelon_event_shape")
        label = str(event["label"]); kind = event.get("kind")
        if kind == "B":
            require(label == "B:" + str(next_b_label) and isinstance(event.get("raw_identity"), str),
                    "checker:boundary_event_owner")
            next_b_label += 1
            bdetail = rebuilt_boundary.insert(event.get("column", {}), label)
            require(bdetail is not None and bdetail.get("pivot") == event.get("boundary_pivot") and
                    bdetail.get("scale") == event.get("boundary_scale") and
                    bdetail.get("row") == event.get("boundary_row") and
                    bdetail.get("reduction") == event.get("boundary_reduction"),
                    "checker:checkpoint_boundary_event_replay")
            cdetail = rebuilt_combined.insert(event.get("boundary_row", {}), label)
            require(cdetail is not None and cdetail == event.get("combined_detail") and
                    event.get("combined_row") == cdetail.get("row"),
                    "checker:checkpoint_combined_boundary_event")
            raw_ledger = {event["raw_identity"]: 1}
            for old, coefficient in bdetail["reduction"].items():
                require(old in derived_boundary_ledgers, "checker:boundary_old_owner")
                raw_ledger = add_sparse(raw_ledger, derived_boundary_ledgers[old], -coefficient)
            boundary_ledger = scale_sparse(raw_ledger, int(bdetail["scale"]))
            require(basis.boundary.psi({event["raw_identity"]: 1}) == event.get("column"),
                    "checker:boundary_raw_identity")
            combined_ledger = scale_sparse(boundary_ledger, int(cdetail["scale"]))
            combined_coefficients: dict[str, int] = {}
            for old, coefficient in cdetail["reduction"].items():
                require(old in derived_formals, "checker:combined_formal_old")
                old_q, old_c = derived_formals[old]
                combined_ledger = add_sparse(combined_ledger, old_q, -int(cdetail["scale"]) * coefficient)
                combined_coefficients = add_sparse(combined_coefficients, old_c,
                                                   -int(cdetail["scale"]) * coefficient)
            derived_b_rows[label] = cdetail["row"]; derived_b_ledgers[label] = combined_ledger
            derived_active.update(cdetail["row"])
            derived_boundary_ledgers[label] = boundary_ledger; derived_combined_ledgers[label] = combined_ledger
            derived_b_coefficients[label] = combined_coefficients
            derived_formals[label] = (combined_ledger, combined_coefficients)
        elif kind == "K":
            require(label == "K:" + str(next_k_label) and label in saved_by_label,
                    "checker:K_event_owner")
            next_k_label += 1
            cdetail = rebuilt_combined.insert(event.get("row", {}), label)
            item = saved_by_label[label]
            require(cdetail is not None and cdetail == event.get("combined_detail") and
                    item.get("row") == cdetail.get("row") and
                    item.get("pivot") == cdetail.get("pivot") and
                    item.get("raw_coefficients") == cdetail.get("relation") and
                    int(item.get("rank", -1)) == len(rebuilt_combined.pivots),
                    "checker:K_event_owner")
            require(words is not None, "checker:K_word_dag_required")
            ancestry = item.get("ancestry", {}); parent_query = str(ancestry.get("parent_query", ""))
            query = saved_records.get(parent_query)
            require(isinstance(query, dict) and query.get("schema") == "ZERO_CORRELATION/K_RANK_RISE" and
                    query.get("query_id") == parent_query and ancestry.get("kind") == "K_recurrence" and
                    ancestry.get("candidate_word") == item.get("candidate_word") and
                    ancestry.get("Q") == item.get("Q") and ancestry.get("c") == item.get("c") and
                    int(ancestry.get("s", -1)) == int(item.get("normalization_scale", -2)) and
                    query.get("candidate_word") == item.get("candidate_word") and
                    query.get("candidate_discrepancy") == item.get("candidate_E") and
                    query.get("Q") == item.get("Q") and query.get("c") == item.get("c") and
                    int(query.get("normalization_scale", -1)) == int(item.get("normalization_scale", -2)) and
                    query.get("normalized") == item.get("row"), "checker:K_query_ancestry")
            prior_labels = list(ancestry.get("prior_labels", [])); prior_map = {prior["label"]: prior for prior in derived_items}
            require(prior_labels == sorted(item.get("c", {}).keys()) and
                    all(label in prior_map for label in prior_labels) and
                    all(label in item.get("c", {}) and int(item["c"][label]) in (1, 2)
                        for label in prior_labels), "checker:K_prior_ancestry")
            candidate_node = int(item.get("candidate_node", ancestry.get("candidate_node", -1)))
            require(0 <= candidate_node < len(words.nodes), "checker:K_candidate_node")
            candidate_word = tuple(words.literal(candidate_node))
            require(list(candidate_word) == item.get("candidate_word"), "checker:K_candidate_word")
            candidate_with_q = words.attach_ledger(candidate_node,
                                                     add_sparse(words.nodes[candidate_node]["ledger"], item["Q"]))
            children = [candidate_with_q]
            for prior_label in prior_labels:
                for _ in range(int(item["c"][prior_label])):
                    children.append(words.inverse(prior_map[prior_label]["word_node"]))
            expected_node = words.power(words.product(children), int(item["normalization_scale"]))
            node_id = int(item.get("word_node", -1)); require(expected_node == node_id and
                                                               0 <= node_id < len(words.nodes),
                                                               "checker:K_dag_recurrence")
            node = words.nodes[node_id]
            require(item.get("word") == list(words.literal(node_id)) and
                    node.get("ledger") == item.get("discrepancy"), "checker:K_word_recurrence")
            states = node.get("states", []); require(isinstance(states, list) and len(states) == 10,
                                                      "checker:K_state_arity")
            require(all(state.identity_roof() for state in states), "checker:K_rho0_identity")
            rho0 = [element_blob(state.a).hex() for state in states]
            rho1 = [{"roof": element_blob(state.a).hex(), "fox": local_row(index, state.u)}
                    for index, state in enumerate(states)]
            actual_flattened: dict[str, int] = {}
            for index, state in enumerate(states): actual_flattened = add_sparse(actual_flattened, local_row(index, state.u))
            normalized_flattened = add_sparse(actual_flattened, basis.boundary.psi(item["discrepancy"]), -1)
            require(item.get("rho0") == rho0 and item.get("rho1") == rho1 and
                    item.get("q") == list(h2_word(item["word"])) and
                    item.get("rho1_actual_flattened") == actual_flattened and
                    item.get("rho1_flattened") == normalized_flattened and
                    item.get("row") == normalized_flattened, "checker:K_state_owner")
            derived_k_rows[label] = cdetail["row"]; derived_combined_ledgers[label] = {}
            derived_active.update(cdetail["row"])
            derived_formals[label] = ({}, {label: 1}); derived_items.append(item)
        else:
            raise Reject("checker:checkpoint_echelon_event_kind")
    require(rebuilt_boundary.pivots == boundary_state.get("pivots") and
            rebuilt_boundary.rows == boundary_state.get("rows") and
            rebuilt_boundary.labels == boundary_state.get("labels") and
            rebuilt_combined.pivots == combined_state.get("pivots") and
            rebuilt_combined.rows == combined_state.get("rows") and
            rebuilt_combined.labels == combined_state.get("labels"),
            "checker:checkpoint_echelon_rebuild_mismatch")
    require(saved_b_rows == derived_b_rows and saved_b_ledgers == derived_b_ledgers and
            saved_boundary_ledgers == derived_boundary_ledgers and saved_combined_ledgers == derived_combined_ledgers and
            saved_b_coefficients == derived_b_coefficients and saved_formals == derived_formals and
            saved_items == derived_items, "checker:checkpoint_chronological_owner_mismatch")
    basis.bspace = rebuilt_boundary; basis.combined = rebuilt_combined
    basis.b_rows = derived_b_rows; basis.b_ledgers = derived_b_ledgers
    basis.boundary_ledgers = derived_boundary_ledgers; basis.combined_ledgers = derived_combined_ledgers
    basis.b_coefficients = derived_b_coefficients; basis.b_formals = derived_formals
    basis.k_items = derived_items; basis.k_rows = derived_k_rows; basis.insertion_events = list(events)
    basis.active_registry = derived_active
    require(set(basis.b_rows) == {label for label in rebuilt_combined.labels.values() if label.startswith("B:")} and
            set(basis.k_rows) == {label for label in rebuilt_combined.labels.values() if label.startswith("K:")},
            "checker:checkpoint_echelon_label_registry")
    for pivot, label in rebuilt_boundary.labels.items():
        require(label in basis.boundary_ledgers and
                basis.boundary.psi(basis.boundary_ledgers[label]) == rebuilt_boundary.rows[pivot],
                "checker:checkpoint_raw_boundary_replay")
    for pivot, label in rebuilt_combined.labels.items():
        require(label in basis.b_formals, "checker:checkpoint_combined_formal_label")
        q_value, c_value = basis.b_formals[label]
        require(add_sparse(basis.boundary.psi(q_value), rebuilt_combined.replay(c_value, basis.k_rows)) ==
                rebuilt_combined.rows[pivot], "checker:checkpoint_combined_formal_replay")
    active = sorted(derived_active)
    require(active == sorted(state.get("active_registry", [])), "checker:checkpoint_active_registry")


def exact_discrepancy(arithmetic: CheckerArithmetic, boundary: Boundary, word: Sequence[int], representative: dict[str, int], ledger: dict[str, int], meter: Meter,
                      states: Sequence[CState] | None = None) -> dict[str, Any]:
    states = list(states) if states is not None else [arithmetic.direct(word, i) for i in range(10)]
    actual = arithmetic.row(states); expected = add_sparse(representative, boundary.psi(ledger))
    require(actual == expected, "checker:raw_discrepancy_replay")
    return {"word": list(word), "row_digest": digest(actual), "ledger_digest": digest(ledger),
            "actual": actual}


def accept_k(oracle: Oracle, arithmetic: CheckerArithmetic, boundary: Boundary, words: WordNodeDAG,
             query: dict[str, Any], candidate_node: int, label: str) -> dict[str, Any]:
    c = {str(key): int(value) for key, value in query["c"].items()}; prior = {item["label"]: item for item in oracle.basis.k_items}; prior_sum: dict[str, int] = {}
    for key, coefficient in c.items(): require(key in prior, "checker:prior_k_label"); prior_sum = add_sparse(prior_sum, prior[key]["discrepancy"], coefficient)
    e_new = scale_sparse(add_sparse(add_sparse(query["candidate_discrepancy"], query["Q"]), prior_sum, -1), int(query["normalization_scale"]))
    candidate_with_q = words.attach_ledger(candidate_node,
                                            add_sparse(words.nodes[candidate_node]["ledger"], query["Q"]))
    children = [candidate_with_q]
    for key in sorted(c):
        for _ in range(c[key]): children.append(words.inverse(prior[key]["word_node"]))
    node = words.power(words.product(children), int(query["normalization_scale"])); literal = words.literal(node)
    require(words.nodes[node]["ledger"] == e_new, "checker:word_ledger_recurrence")
    states = words.nodes[node]["states"]
    # WordNodeDAG.literal already returns the canonical reduced tuple; do not
    # walk the potentially long spelling through a second free reduction.
    require(tuple(literal) == words.literal(node), "checker:word_recurrence")
    replay = exact_discrepancy(arithmetic, boundary, literal, query["normalized"], e_new,
                               oracle.meter, states)
    ancestry = {"kind": "K_recurrence", "parent_query": query["query_id"], "candidate_word": list(words.literal(candidate_node)),
                "Q": query["Q"], "c": c, "s": int(query["normalization_scale"]), "prior_labels": sorted(c)}
    item = oracle.basis.add_k(query["normalized"], label, literal, e_new, node, states, ancestry)
    item.update({"candidate_node": candidate_node,
                 "candidate_word": list(words.literal(candidate_node)),
                 "candidate_E": query["candidate_discrepancy"], "Q": query["Q"], "c": c,
                 "normalization_scale": int(query["normalization_scale"]),
                 "word_formula": "red((W_v product_l W_l^(-c_l))^s)",
                 "E_formula": "s*(E_v+Q-sum(c_l E_l))", "replay": replay,
                 "strict_rank_rise": True})
    return item


def pure_boundary_roster(basis: Basis) -> list[dict[str, Any]]:
    events = {event["label"]: event for event in basis.insertion_events if event.get("kind") == "B"}
    result = []
    for index, pivot in enumerate(basis.bspace.pivots):
        label = basis.bspace.labels[pivot]; event = events.get(label)
        require(event is not None, "checker:pure_roster_event")
        require(label == f"B:{index}" and event["boundary_pivot"] == pivot,
                "checker:pure_roster_order")
        result.append({"label": label, "pivot": pivot, "column": event["column"],
                       "raw_identity": event["raw_identity"], "boundary_row": basis.bspace.rows[pivot],
                       "boundary_reduction": event["boundary_reduction"],
                       "boundary_scale": event["boundary_scale"],
                       "boundary_ledger": basis.boundary_ledgers[label],
                       "combined_row": event["combined_row"],
                       "combined_formal": [basis.b_formals[label][0], basis.b_formals[label][1]]})
    return result


def public_k_roster(items: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Export canonical K recurrence owners, excluding local DAG ids."""
    result: list[dict[str, Any]] = []
    for source in items:
        item = dict(source); item.pop("word_node", None); item.pop("candidate_node", None)
        ancestry = dict(item.get("ancestry", {})); ancestry.pop("candidate_node", None)
        item["ancestry"] = ancestry; result.append(item)
    return result


def translated_row(value: dict[str, int], arithmetic: CheckerArithmetic, letter: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for key, coefficient in value.items():
        context, component, text = split_key(key); moved = arithmetic.quotient(context).mul(arithmetic.actors[context, letter].a, decode_token(text))
        target = row_key(context, component, moved); out[target] = (out.get(target, 0) + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def compose(left: dict[str, dict[str, int]], right: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for source, middle_terms in right.items():
        column: dict[str, int] = {}
        for middle, coefficient in middle_terms.items():
            for target, value in left.get(middle, {}).items(): column[target] = (column.get(target, 0) + int(coefficient) * int(value)) % 3
        result[source] = {key: value for key, value in column.items() if value}
    return result


def validate_action_matrix(matrix: dict[str, dict[str, dict[str, int]]],
                           labels: set[str], message: str) -> None:
    """Fail closed on both outer source and inner K-label support."""
    require(isinstance(matrix, dict) and set(matrix) == {"1", "-1", "2", "-2"}, message + ":letters")
    for letter, columns in matrix.items():
        require(isinstance(columns, dict), message + ":columns")
        for source, column in columns.items():
            require(source in labels and isinstance(column, dict), message + ":source")
            require(set(column) <= labels and
                    all(type(value) is int and value in (1, 2) for value in column.values()),
                    message + ":inner_support")


def action_column(basis: Basis, query: dict[str, Any], new_label: str | None = None) -> dict[str, int]:
    if query["schema"] == "MEMBER":
        return {label: int(value) % 3 for label, value in query["K_coefficients"].items() if int(value) % 3}
    require(query["schema"] == "ZERO_CORRELATION/K_RANK_RISE" and new_label is not None, "checker:action_column_schema")
    result = {label: int(value) % 3 for label, value in query["c"].items()
              if label.startswith("K:") and int(value) % 3}
    scale = int(query["normalization_scale"]) % 3
    require(scale in (1, 2) and (scale * scale) % 3 == 1, "checker:action_scale_inverse")
    inverse_scale = scale  # in F_3 the nonzero scalars are self-inverse.
    result[new_label] = (result.get(new_label, 0) + inverse_scale) % 3
    return {label: value for label, value in result.items() if value}


def replay_action_projection(basis: Basis, boundary: Boundary, target: dict[str, int],
                             query: dict[str, Any], column: dict[str, int]) -> None:
    target_mod_boundary = add_sparse(target, boundary.psi(query.get("boundary_Q", query.get("Q", {}))), -1)
    require(basis.combined.replay(column, basis.k_rows) == target_mod_boundary, "checker:projected_K_replay")


def validate_queue_prefix(basis: Basis, boundary: Boundary, arithmetic: CheckerArithmetic,
                          records: list[dict[str, Any]], queue: list[int], cursor: int,
                          actions: list[dict[str, Any]], matrix: dict[str, dict[str, dict[str, int]]],
                          action_events: list[dict[str, Any]]) -> None:
    """Replay only saved action relations against the restored checker state."""
    order = (1, -1, 2, -2)
    require(isinstance(queue, list) and all(type(index) is int for index in queue) and
            0 <= cursor <= len(queue) and len(set(queue)) == len(queue) and
            queue == list(range(len(basis.k_items))) and
            len(actions) == len(action_events) == 4 * cursor,
            "checker:action_prefix_shape")
    for parent_index in queue[:cursor]:
        require(0 <= parent_index < len(basis.k_items), "checker:action_parent_registry")
    processed = {basis.k_items[queue[index]]["label"] for index in range(cursor)}
    expected_columns = {str(letter): {} for letter in order}
    for index in range(cursor):
        parent = basis.k_items[queue[index]]
        for offset, letter in enumerate(order):
            action = actions[index * 4 + offset]; event = action_events[index * 4 + offset]
            require(action.get("parent") == parent["label"] and int(action.get("letter")) == letter and
                    event.get("index") == index * 4 + offset + 1 and
                    event.get("digest") == digest(action), "checker:action_order")
            terminal_id = int(action.get("terminal_id", -1)); require(0 <= terminal_id < len(records),
                                                                     "checker:action_terminal_id")
            query = records[terminal_id]
            require(query.get("query_id") == event.get("query_id") and
                    query.get("schema") in ("MEMBER", "ZERO_CORRELATION/K_RANK_RISE"),
                    "checker:action_terminal_record")
            target = translated_row(parent["row"], arithmetic, letter)
            if query["schema"] == "MEMBER":
                column = action_column(basis, query)
            else:
                matches = [item for item in basis.k_items
                           if item.get("candidate_word") == query.get("candidate_word") and
                           item.get("candidate_E") == query.get("candidate_discrepancy") and
                           item.get("Q") == query.get("Q") and item.get("c") == query.get("c") and
                           int(item.get("normalization_scale", -1)) == int(query.get("normalization_scale", -2)) and
                           item.get("ancestry", {}).get("parent_query") == query.get("query_id") and
                           int(action.get("candidate_node", -1)) ==
                           int(item.get("candidate_node", item.get("ancestry", {}).get("candidate_node", -2)))]
                require(len(matches) == 1, "checker:action_new_K_owner")
                column = action_column(basis, query, matches[0]["label"])
            require(action.get("basis_column") == column and matrix.get(str(letter), {}).get(parent["label"]) == column,
                    "checker:action_column_replay")
            replay_action_projection(basis, boundary, target, query, column)
            expected_columns[str(letter)][parent["label"]] = column
    validate_action_matrix(matrix, {item["label"] for item in basis.k_items},
                           "checker:action_matrix_prefix")
    for letter in order:
        require(isinstance(matrix.get(str(letter), {}), dict) and
                set(matrix.get(str(letter), {})) == processed and
                matrix.get(str(letter), {}) == expected_columns[str(letter)],
                "checker:action_matrix_prefix")


def h2_projection(arithmetic: CheckerArithmetic, basis: Basis, meter: Meter) -> list[dict[str, Any]]:
    out = []
    for item in basis.k_items:
        word = tuple(item["word"]); states = [arithmetic.direct(word, i) for i in range(10)]
        require(all(state.identity_roof() for state in states), "checker:rho0_identity")
        q = h2_word(word); require(q[0] == 0 and q[1] == 0 and q[2] in (0, 3, 6), "checker:q_image")
        rho0 = [element_blob(state.a).hex() for state in states]
        rho1 = [{"roof": element_blob(state.a).hex(), "fox": local_row(index, state.u)}
                for index, state in enumerate(states)]
        actual_flattened = arithmetic.row(states)
        normalized_flattened = add_sparse(actual_flattened,
                                          basis.boundary.psi(item["discrepancy"]), -1)
        require(item.get("rho0") == rho0 and item.get("rho1") == rho1 and
                item.get("q") == list(q) and
                normalized_flattened == item.get("row") and
                actual_flattened == item.get("rho1_actual_flattened") and
                normalized_flattened == item.get("rho1_flattened"),
                "checker:stored_projection_replay")
        out.append({"label": item["label"], "q": list(q), "exponent": q[2] // 3 % 3,
                    "rho0": rho0, "rho1": rho1,
                    "rho1_flattened": item["rho1_flattened"], "rho1_actual_flattened": item["rho1_actual_flattened"]})
    return out


def derive_anchor(arithmetic: CheckerArithmetic, boundary: Boundary, basis: Basis, words: WordNodeDAG, meter: Meter) -> dict[str, Any]:
    projections = h2_projection(arithmetic, basis, meter); active = [i for i, value in enumerate(projections) if value["exponent"] != 0]
    require(active, "checker:anchor_all_q_zero:UNKNOWN_INPUT")
    selected = active[0]; exponent = int(projections[selected]["exponent"]); scalar = 1 if exponent == 1 else 2
    source = basis.k_items[selected]; node = words.power(source["word_node"], scalar); powered = words.literal(node); powered_states = words.nodes[node]["states"]
    q = h2_word(powered); require(q == (0, 0, 3), "checker:anchor_q_z0")
    representative = scale_sparse(source["row"], scalar); discrepancy = scale_sparse(source["discrepancy"], scalar)
    replay = exact_discrepancy(arithmetic, boundary, powered, representative, discrepancy, meter,
                               powered_states)
    labels = [item["label"] for item in basis.k_items]; anchor_label = source["label"]
    transform: dict[str, dict[str, int]] = {}
    for index, item in enumerate(basis.k_items):
        if index == selected: transform[item["label"]] = {item["label"]: scalar}
        else:
            ai = int(projections[index]["exponent"])
            transform[item["label"]] = {item["label"]: 1, anchor_label: (-ai * scalar) % 3}
    inverse_transform: dict[str, dict[str, int]] = {}; anchor_exponent = exponent % 3
    for index, label in enumerate(labels):
        if index == selected: inverse_transform[label] = {label: anchor_exponent}
        else:
            ai = int(projections[index]["exponent"])
            inverse_transform[label] = {label: 1, anchor_label: ai % 3}
    identity_matrix = {label: {label: 1} for label in labels}
    require(compose(transform, inverse_transform) == identity_matrix and compose(inverse_transform, transform) == identity_matrix,
            "checker:adapted_change_matrix_inverse")
    adapted = []
    for index, item in enumerate(basis.k_items):
        if index == selected: continue
        exponent_i = int(projections[index]["exponent"]); adapted_word = word_mul(tuple(item["word"]), *(word_inv(powered) for _ in range(exponent_i)))
        adapted_row = add_sparse(item["row"], representative, -exponent_i); adapted_e = add_sparse(item["discrepancy"], discrepancy, -exponent_i)
        states = [arithmetic.direct(adapted_word, i) for i in range(10)]; require(h2_word(adapted_word) == (0, 0, 0), "checker:adapted_q")
        adapted_replay = exact_discrepancy(arithmetic, boundary, adapted_word, adapted_row, adapted_e, meter,
                                           states)
        require(all(state.identity_roof() for state in states), "checker:adapted_rho0")
        actual: dict[str, int] = {}
        for context, state in enumerate(states): actual = add_sparse(actual, local_row(context, state.u))
        require(add_sparse(actual, boundary.psi(adapted_e), -1) == adapted_row, "checker:adapted_rho1")
        adapted.append({"old_label": item["label"], "word": list(adapted_word), "q": [0, 0, 0], "row": adapted_row,
                        "discrepancy": adapted_e, "rho0": [element_blob(state.a).hex() for state in states],
                        "rho1_flattened": adapted_row, "rho1_actual_flattened": actual, "replay": adapted_replay})
    return {"diagnostic_only": True, "basis_q": projections, "least_index": selected, "inverse_scalar": scalar,
            "powered_word": list(powered), "powered_q": list(q), "powered_row": representative,
            "powered_discrepancy": discrepancy, "powered_rho0": [element_blob(state.a).hex() for state in powered_states],
            "powered_rho1_flattened": add_sparse(arithmetic.row(powered_states), boundary.psi(discrepancy), -1),
            "powered_rho1_actual_flattened": arithmetic.row(powered_states), "powered_replay": replay,
            "adapted_basis": adapted, "change_matrix": transform, "inverse_change_matrix": inverse_transform,
            "v280_derivation": "a_i=actual q(k_i); j=min nonzero; e=a_j^-1; red(u_i u_*^-a_i)"}


def build_checker_kernel(authority: Authority, arithmetic: CheckerArithmetic, suffix: SuffixDAG,
                         primitive: list[tuple[int, ...]], inventory: dict[str, Any], meter: Meter,
                         checkpoint: Path | None = None,
                         resume_state: dict[str, Any] | None = None) -> dict[str, Any]:
    for word in primitive: suffix.add(word)
    require(len(suffix.nodes) - 1 == 26136, "checker:suffix_edge_count")
    boundary = Boundary(arithmetic, meter); oracle = Oracle(arithmetic, boundary, meter); words = WordNodeDAG(arithmetic, meter)
    row_digests: list[str] = []; chunks: list[dict[str, Any]] = []; chunk_start = 1
    initial: list[dict[str, Any]] = []; samples: list[dict[str, Any]] = []; sample_rows: dict[int, dict[str, Any]] = {}; sample_indices = {0, 6317, 6318, 6421, 6422, 6440}
    action_event_chain: list[dict[str, Any]] = []
    matrices: dict[str, dict[str, dict[str, int]]] = {str(letter): {} for letter in (1, -1, 2, -2)}
    queue: list[int] = []; actions: list[dict[str, Any]] = []
    inverse_laws: dict[str, Any] = {}
    if resume_state is not None:
        restore_word_dag(words, resume_state.get("word_ledger_dag", []))
        restore_basis(oracle.basis, resume_state, words)
        for item in oracle.basis.k_items:
            node_id = int(item.get("word_node", -1)); require(0 <= node_id < len(words.nodes),
                                                               "checker:checkpoint_K_word_node")
            require(words.literal(node_id) == tuple(item.get("word", [])),
                    "checker:checkpoint_K_word_recurrence")
        oracle.records = list(resume_state.get("oracle_records", []))
        oracle.live_duals = list(resume_state.get("live_duals", []))
        oracle.event_chain = list(resume_state.get("query_event_chain", []))
        oracle.dual_chain = list(resume_state.get("dual_event_chain", []))
        oracle.epoch = str(resume_state.get("epoch_digest"))
        oracle.bridge_chain = list(resume_state.get("bridge_digests", []))
        row_digests = list(resume_state.get("row_digests", [])); chunks = list(resume_state.get("row_chunks", []))
        initial = list(resume_state.get("initial_terminal_records", []))
        samples = list(resume_state.get("samples", []))
        sample_rows = {int(key): value for key, value in resume_state.get("sample_rows", {}).items()}
        phase = resume_state.get("queue_phase", {})
        queue = [int(index) for index in resume_state.get("queue", [])]
        actions = list(phase.get("actions", [])); action_event_chain = list(phase.get("action_event_chain", []))
        matrices = {str(key): value for key, value in phase.get("matrix", {}).items()}
        inverse_laws = dict(phase.get("inverse_laws", {}))
        cursor = int(resume_state.get("queue_head", 0))
        require(all(0 <= index < len(oracle.basis.k_items) for index in queue),
                "checker:checkpoint_queue_item_registry")
        require(queue_phase_snapshot(queue, cursor, actions, matrices, inverse_laws,
                                     action_event_chain) == phase,
                "checker:checkpoint_queue_phase_restore")
    oracle.row_digests = row_digests; oracle.row_chunks = chunks
    oracle.samples = samples; oracle.sample_rows = sample_rows
    resume_row = 1 if resume_state is None else int(resume_state.get("next_row", 0))
    require(1 <= resume_row <= ROWS + 1, "checker:checkpoint_next_row_range")
    if resume_state is not None:
        require((not chunks and resume_row == 1) or
                (chunks and int(chunks[-1]["end"]) == resume_row - 1),
                "checker:checkpoint_row_chunk_cursor")
        chunk_start = 1 if not chunks else int(chunks[-1]["end"]) + 1
        require(chunk_start == resume_row, "checker:checkpoint_row_chunk_next_start")
    checkpoint_writes_enabled = resume_state is None

    def consume_row(ordinal: int, row: dict[str, Any]) -> None:
        meter.check("CHECKER_ROW_" + str(ordinal)); source_word, parts, ancestry = replay_ancestry(row)
        # Structural row pieces are counted once per row; ten-context affine
        # products have their own typed work charge and must not multiply the
        # 19,408 structural cap by ten.
        piece_count = 4 if row["layer"] == "action" else len(parts)
        meter.bump("row_piece_products", piece_count, "checker.row_piece_structure")
        meter.bump("typed_context_products", 10 * piece_count, "checker.row_piece_context")
        states: list[CState] = []
        for index in range(10):
            state = arithmetic.identity(index)
            if row["layer"] == "action":
                letter = int(row["letter"]); orientation = int(row["orientation"])
                state = state.mul(arithmetic.actors[index, -letter if orientation == 1 else letter])
                state = state.mul(suffix.state(parts[0], index))
                state = state.mul(arithmetic.actors[index, letter if orientation == 1 else -letter])
                state = state.mul(suffix.state(parts[1], index))
            else:
                for part in parts: state = state.mul(suffix.state(part, index))
            require(state.identity_roof(), "checker:row_roof"); states.append(state)
        assembled = arithmetic.row(states); meter.bump("row_assemblies", 1, "checker.row_assembly")
        meter.bump("literal_comparisons", len(source_word), "checker.literal_word_compare")
        # The reverse suffix DAG has already supplied the exact ten states;
        # derive the task198 bridge trace from that live row pass instead of
        # invoking a second flat evaluator over the 6,441 source words.
        bridge_trace = checker_bridge_trace(states, source_word, row, authority, meter)
        oracle.bridge_chain.append(bridge_trace["bridge_trace_digest"])
        row_value = {"ordinal": ordinal, "layer": row["layer"], "word": list(source_word), "row": assembled}
        row_digests.append(digest(row_value))
        if ordinal in {1024, 2048, 3072, 4096, 5120, 6144, 6441}:
            chunks.append({"start": chunk_start, "end": ordinal,
                           "sha256": digest(row_digests[chunk_start - 1:ordinal])})
            chunk_start = ordinal + 1
        if ordinal - 1 in sample_indices:
            samples.append({"ordinal": ordinal, "word": list(source_word), "row_digest": digest(assembled)})
            sample_rows[ordinal] = {"word": tuple(source_word), "row": assembled}
        query = oracle.query(assembled, {}, source_word, f"R:{ordinal}")
        initial.append(compact_terminal_record(query))
        if query["schema"] == "ZERO_CORRELATION/K_RANK_RISE":
            node = words.source(source_word); accept_k(oracle, arithmetic, boundary, words, query, node, f"K:{len(oracle.basis.k_items)}")
            queue.append(len(oracle.basis.k_items) - 1)
        if checkpoint is not None and checkpoint_writes_enabled and ordinal in {1024, 2048, 3072, 4096, 5120, ROWS}:
            write_checkpoint(checkpoint, authority, meter, ordinal + 1, oracle, words, queue, 0,
                             queue_phase_snapshot(queue, 0, actions, matrices, inverse_laws,
                                                  action_event_chain))
    if resume_state is not None:
        require(0 <= cursor <= len(queue) and cursor == int(resume_state.get("queue_head", 0)),
                "checker:checkpoint_queue_head_range")
        validate_queue_prefix(oracle.basis, boundary, arithmetic, oracle.records, queue, cursor,
                              actions, matrices, action_event_chain)
        rebuilt = checkpoint_payload(authority, meter, resume_row, oracle, words, queue, cursor,
                                     queue_phase_snapshot(queue, cursor, actions, matrices, inverse_laws,
                                                          action_event_chain))
        require(rebuilt["rebuild_digest"] == resume_state.get("rebuild_digest"),
                "checker:checkpoint_deterministic_rebuild_mismatch")
        meter.validation_bump(len(resume_state.get("word_ledger_dag", [])) +
                             len(resume_state.get("insertion_events", [])) +
                             len(resume_state.get("oracle_records", [])) +
                             len(resume_state.get("queue_phase", {}).get("actions", [])) + 1,
                             "checker.checkpoint.restore_state")
        require(meter.pending_completed_counters is not None and meter.pending_saved_validation is not None,
                "checker:checkpoint_pending_counter_state")
        meter.install_completed(meter.pending_completed_counters, dict(meter.restore_validation_counters),
                                meter.pending_saved_peak)
        checkpoint_writes_enabled = True
    for ordinal, row in enumerate(authority.rows[resume_row - 1:], resume_row):
        consume_row(ordinal, row)
    require(len(initial) == ROWS and len(row_digests) == ROWS and len(chunks) == 7,
            "checker:row_stream_complete")
    bridge_digests = list(oracle.bridge_chain)
    expected_bridge = authority.receipt.get("bridge", {}).get("relator_replay", {})
    require(len(bridge_digests) == ROWS and expected_bridge.get("count") == ROWS and
            expected_bridge.get("all_left_and_right_inverses") is True and
            digest(bridge_digests) == expected_bridge.get("digest_sha256"),
            "checker:bridge_relator_replay_owner")
    bridge_summary = {"count": len(bridge_digests), "digest_sha256": digest(bridge_digests),
                      "all_left_and_right_inverses": True,
                      "prefix_canary": digest(bridge_digests)}
    if resume_state is None:
        cursor = 0

    def run_queue(stop_at: int | None = None) -> None:
        nonlocal cursor
        while cursor < len(queue) and (stop_at is None or cursor < stop_at):
            parent = oracle.basis.k_items[queue[cursor]]; cursor += 1; meter.check("CHECKER_K_QUEUE_" + str(cursor))
            for letter in (1, -1, 2, -2):
                structural_word = word_mul((letter,), tuple(parent["word"]), (-letter,))
                node = words.conjugate(letter, parent["word_node"])
                candidate_word = words.literal(node)
                require(candidate_word == structural_word, "checker:action_word_recurrence")
                representative = translated_row(parent["row"], arithmetic, letter)
                discrepancy = boundary.act(parent["discrepancy"], [arithmetic.actors[i, letter].a for i in range(10)])
                query = oracle.query(representative, discrepancy, candidate_word, f"A:{parent['label']}:{letter}")
                if query["schema"] == "MEMBER":
                    column = action_column(oracle.basis, query)
                    replay_action_projection(oracle.basis, boundary, representative, query, column)
                    matrices[str(letter)][parent["label"]] = column
                elif query["schema"] == "ZERO_CORRELATION/K_RANK_RISE":
                    item = accept_k(oracle, arithmetic, boundary, words, query, node, f"K:{len(oracle.basis.k_items)}")
                    column = action_column(oracle.basis, query, item["label"])
                    replay_action_projection(oracle.basis, boundary, representative, query, column)
                    matrices[str(letter)][parent["label"]] = column; queue.append(len(oracle.basis.k_items) - 1)
                else: raise HardStop("checker:unexpected_action_terminal")
                action_value = {"parent": parent["label"], "letter": letter,
                                "basis_column": matrices[str(letter)][parent["label"]],
                                "terminal_id": len(oracle.records) - 1}
                if query["schema"] == "ZERO_CORRELATION/K_RANK_RISE":
                    action_value["candidate_node"] = item["candidate_node"]
                actions.append(action_value)
                action_event_chain.append({"index": len(action_event_chain) + 1,
                                           "query_id": query["query_id"],
                                           "digest": digest(actions[-1])})
                meter.bump("queue_actions", 1, "checker.action_queue")
            if checkpoint is not None and checkpoint_writes_enabled and queue_checkpoint_due(cursor, len(queue)):
                write_checkpoint(checkpoint, authority, meter, ROWS + 1, oracle, words, queue, cursor,
                                 queue_phase_snapshot(queue, cursor, actions, matrices, inverse_laws,
                                                      action_event_chain))

    run_queue()
    require(cursor == len(queue) and queue, "checker:queue_exhaustion")
    labels = {item["label"] for item in oracle.basis.k_items}; identity = {label: {label: 1} for label in labels}
    for item in oracle.basis.k_items:
        require(oracle.basis.k_rows.get(item["label"]) == item.get("row"), "checker:K_row_owner")
    validate_action_matrix(matrices, labels, "checker:complete_action_matrix")
    for letter in matrices: require(set(matrices[letter]) == labels, "checker:complete_action_matrix")
    inverse_laws = {}
    for positive, negative in (("1", "-1"), ("2", "-2")):
        require(compose(matrices[positive], matrices[negative]) == identity and compose(matrices[negative], matrices[positive]) == identity, "checker:inverse_matrix_law")
        inverse_laws[positive + negative] = True; inverse_laws[negative + positive] = True
    if checkpoint is not None and checkpoint_writes_enabled:
        write_checkpoint(checkpoint, authority, meter, ROWS + 1, oracle, words, queue, cursor,
                         queue_phase_snapshot(queue, cursor, actions, matrices, inverse_laws,
                                              action_event_chain))
    require(all(scale_sparse(item["row"], 3) == {} for item in oracle.basis.k_items), "checker:order_three")
    if len(oracle.basis.k_items) >= 2:
        left, right = oracle.basis.k_items[:2]
        for context in range(10):
            ab = arithmetic.direct(word_mul(left["word"], right["word"]), context)
            ba = arithmetic.direct(word_mul(right["word"], left["word"]), context)
            require((element_blob(ab.a).hex(), local_row(context, ab.u)) ==
                    (element_blob(ba.a).hex(), local_row(context, ba.u)),
                    "checker:fixed_commutation_canary")
    anchor = derive_anchor(arithmetic, boundary, oracle.basis, words, meter)
    queue_state = {"accepted": len(queue), "cursor": cursor, "next": cursor}
    LIVE_STATE.update({"authority": authority, "arithmetic": arithmetic, "suffix": suffix,
                       "boundary": boundary, "oracle": oracle, "basis": oracle.basis,
                       "words": words, "queue": queue, "actions": actions,
                       "action_matrices": matrices, "anchor": anchor, "samples": samples,
                       "sample_rows": sample_rows, "queue_cursor": cursor, "queue_state": queue_state,
                       "action_event_chain": action_event_chain, "bridge_digests": bridge_digests,
                        "row_digests": row_digests,
                       "meter": meter})
    return {"initial": {"count": ROWS, "terminal_digest": digest(initial), "member_count": sum(item["schema"] == "MEMBER" for item in initial),
                         "rank_rise_count": sum(item["schema"] == "ZERO_CORRELATION/K_RANK_RISE" for item in initial)},
             "row_stream": {"sha256": digest(row_digests), "chunks": chunks, "samples": samples},
            "bridge": bridge_summary,
            "K_roster": public_k_roster(oracle.basis.k_items), "actions": actions, "action_matrices": matrices, "inverse_laws": inverse_laws,
            "queue": {"accepted": len(queue), "cursor": cursor, "next": cursor},
             "boundary": {"seed_count": len(boundary.seeds), "rank": len(oracle.basis.b_rows), "epoch_digest": oracle.epoch,
                         "record_count": len(oracle.records), "terminal_digest": digest(oracle.records),
                         "event_digest": digest(oracle.event_chain),
                         "pure_B_roster": pure_boundary_roster(oracle.basis),
                         "mixed_basis": oracle.basis.b_rows},
            "anchor_diagnostics": anchor,
            "word_dag": {"nodes": len(words.nodes), "persistent": True, "memoized_psi": True, "pre_expansion_cap": words.cap},
            "inventory": {**inventory, "suffix_edges": len(suffix.nodes) - 1},
            "basis_algorithm": "v272-lazy-full-D-v273-ledger-v274-active-dual-v282-reverse-suffix-DAG",
            "maxpivot_canary": maxpivot_arithmetic_canary(), "complete": True}


def sealed(value: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    body = dict(value); body.pop("self_digest_sha256", None); body["self_digest_sha256"] = digest(body); return body, canon(body)


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); fd, temporary = tempfile.mkstemp(prefix=".v6-checker-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        if os.name != "nt":
            directory_fd = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        else:
            # Flush the replacement handle on Windows; directory handles do
            # not provide a portable fsync equivalent.  Unavailable support
            # is a typed fail-closed transport stop.
            try:
                msvcrt = __import__("msvcrt")
                kernel = ctypes.WinDLL("kernel32", use_last_error=True)
                kernel.FlushFileBuffers.argtypes = [ctypes.c_void_p]
                kernel.FlushFileBuffers.restype = ctypes.c_int
                sync_fd = os.open(str(path), os.O_RDONLY | getattr(os, "O_BINARY", 0))
                try:
                    handle = ctypes.c_void_p(msvcrt.get_osfhandle(sync_fd))
                    if not kernel.FlushFileBuffers(handle):
                        raise Reject("checker:atomic_windows_flush_unavailable")
                finally:
                    os.close(sync_fd)
            except Reject:
                raise
            except Exception as exc:
                raise Reject("checker:atomic_windows_flush_unavailable") from exc
    except Exception:
        try: os.unlink(temporary)
        except OSError: pass
        raise


def write_sealed(path: Path, value: dict[str, Any], meter: Meter | None = None,
                 terminal_transport: bool = False) -> None:
    base = dict(value); base.setdefault("serialization", {"canonicalization": True, "atomic": True})
    if meter is None:
        _, raw = sealed(base); atomic_write(path, raw); return
    if terminal_transport:
        # Normal semantic caps may already be exhausted.  Use only the
        # reserved, bounded terminal counters while still recording the exact
        # physical envelope size and canonicalization work used to make it.
        output_size = 0; final_charged = False
        for _ in range(16):
            meter.terminal_bump("terminal_canonicalization", 1,
                                "checker.terminal.transport.canonicalization")
            body = dict(base)
            body["serialization"] = {
                "canonicalization": True, "atomic": True, "terminal_transport": True,
                "terminal_canonicalization": int(meter._value("terminal_canonicalization")),
                "serialized_work_bytes": int(meter._value("terminal_serialized_bytes")),
                "output_bytes": output_size,
                "final_write": int(meter._value("terminal_final_write")) + (0 if final_charged else 1)}
            body["resource"] = meter.public(strict=False)
            _, raw = sealed(body); desired = len(raw)
            require(desired <= OBJECT_CAPS["checkpoint_current_bytes"],
                    "checker:terminal_transport_object_cap")
            if desired != output_size:
                output_size = desired; continue
            serialized_total = int(meter._value("terminal_serialized_bytes"))
            if desired > serialized_total:
                meter.terminal_bump("terminal_serialized_bytes", desired - serialized_total,
                                    "checker.terminal.transport.serialized_bytes")
                continue
            if not final_charged:
                meter.terminal_bump("terminal_final_write", 1,
                                    "checker.terminal.transport.final_write")
                final_charged = True; continue
            require(body["serialization"]["output_bytes"] == desired and
                    body["serialization"]["serialized_work_bytes"] ==
                    int(meter._value("terminal_serialized_bytes")) and
                    body["serialization"]["final_write"] ==
                    int(meter._value("terminal_final_write")),
                    "checker:terminal_transport_accounting")
            atomic_write(path, raw); return
        raise HardStop("checker:terminal_transport_fixed_point_unstable")
    meter.reserve("final_write", 1, "checker.atomic_final_write")
    meter.bump("final_write", 1, "checker.atomic_final_write")
    start = int(meter._value("serialized_bytes")); charged = 0; output_size = 0
    for _ in range(16):
        meter.bump("canonicalization", 2, "checker.serialize.canonicalization")
        body = dict(base)
        body["serialization"] = {"canonicalization": True, "atomic": True,
                                  "canonicalization_count": int(meter._value("canonicalization")),
                                  "serialized_work_bytes": start + charged,
                                  "output_bytes": output_size}
        body["resource"] = meter.public()
        if isinstance(body.get("performance"), dict):
            performance = dict(body["performance"])
            performance["measured"] = {
                "status": "RUNTIME", "owner": "resource.host_counters",
                "wall_seconds": body["resource"]["host_counters"]["wall_seconds"],
                "input_bytes": body["resource"]["host_counters"]["input_bytes"],
                "rss_bytes": body["resource"]["peak_counters"]["rss_bytes"]}
            body["performance"] = performance
        _, raw = sealed(body); desired = len(raw)
        require(desired <= OBJECT_CAPS["checkpoint_current_bytes"],
                "checker:serialize_output_object_cap")
        if desired != output_size:
            output_size = desired; continue
        if charged != desired:
            require(desired >= charged, "checker:serialize_fixed_point_shrunk")
            delta = desired - charged
            meter.reserve("serialized_bytes", delta, "checker.serialize_before_seal")
            meter.bump("serialized_bytes", delta, "checker.serialize_before_seal")
            charged = desired; continue
        require(body["serialization"]["canonicalization_count"] ==
                int(meter._value("canonicalization")) and
                body["serialization"]["output_bytes"] == desired and
                int(meter._value("serialized_bytes")) == start + charged,
                "checker:serialize_fixed_point_counter")
        atomic_write(path, raw); return
    raise HardStop("checker:serialize_fixed_point_unstable")


def queue_phase_snapshot(queue: list[int], cursor: int, actions: list[dict[str, Any]],
                         matrix: dict[str, Any], inverse_laws: dict[str, Any],
                         action_event_chain: list[dict[str, Any]]) -> dict[str, Any]:
    return {"queue_head": cursor, "queue_length": len(queue),
            "action_count": len(actions), "actions": list(actions),
            "action_event_chain": list(action_event_chain), "matrix": matrix,
            "matrix_digest": digest(matrix), "inverse_laws": dict(inverse_laws)}


def queue_checkpoint_due(cursor: int, queue_length: int) -> bool:
    """Use geometric queue milestones; never serialize the growing state per item."""
    return cursor > 0 and ((cursor & (cursor - 1)) == 0 or cursor == queue_length)


CHECKPOINT_STATE_FIELDS = (
    "owner", "next_row", "next_query", "B_roster", "B_ledgers", "boundary_ledgers",
    "combined_ledgers", "B_coefficients", "B_formals", "K_roster", "boundary_echelon",
    "echelon_rebuild", "insertion_events", "active_registry", "queue", "queue_head",
    "word_ledger_dag", "epoch_digest", "query_event_chain", "oracle_records", "live_duals",
    "dual_event_chain", "initial_terminal_chain", "initial_terminal_records", "row_digests",
    "row_cursor", "row_chunks", "samples", "sample_rows", "row_replay_sha256",
    "row_prefix_canary", "bridge_digests", "bridge_cursor", "bridge_replay_sha256",
    "bridge_prefix_canary", "queue_phase")
CHECKPOINT_COUNTER_FIELDS = (
    "counter_registry", "counters", "completed_counters", "restore_validation_counters",
    "semantic_counters", "host_counters", "host_history", "peak_counters", "resource_envelope",
    "resource_object_caps")


def checkpoint_state_digest(body: dict[str, Any]) -> str:
    return digest({key: body[key] for key in CHECKPOINT_STATE_FIELDS})


def checkpoint_counter_digest(body: dict[str, Any]) -> str:
    return digest({key: body[key] for key in CHECKPOINT_COUNTER_FIELDS})


def checkpoint_next_state_canary(body: dict[str, Any]) -> str:
    boundary = body["boundary_echelon"]; combined = body["echelon_rebuild"]
    return digest({"owner": body["owner"], "next_row": body["next_row"],
                   "queue_head": body["queue_head"], "queue_length": len(body["queue"]),
                   "epoch": body["epoch_digest"], "queue_phase": body["queue_phase"],
                   "rank": len(combined.get("pivots", [])),
                   "boundary_rank": len(boundary.get("pivots", [])),
                   "combined_pivots": list(combined.get("pivots", [])),
                   "boundary_pivots": list(boundary.get("pivots", [])),
                   "active_registry_digest": digest(body["active_registry"]),
                   "counter_registry": body["counter_registry"], "counters": body["counters"],
                   "semantic_counters": body["semantic_counters"], "host_counters": body["host_counters"],
                   "host_history": body["host_history"], "peak_counters": body["peak_counters"],
                   "completed_counters": body["completed_counters"],
                   "restore_validation_counters": body["restore_validation_counters"]})


def checkpoint_payload(authority: Authority, meter: Meter, next_row: int, oracle: Oracle,
                       words: WordNodeDAG, queue: list[int], queue_head: int,
                       queue_phase: dict[str, Any] | None = None) -> dict[str, Any]:
    basis = oracle.basis
    meter.completed_counters = dict(meter.semantic_counters); meter._sync()
    row_digests = list(getattr(oracle, "row_digests", []))
    phase = queue_phase or {"queue_head": queue_head, "queue_length": len(queue),
                            "action_count": 0, "actions": [], "action_event_chain": [],
                            "matrix": {str(x): {} for x in (1, -1, 2, -2)},
                            "matrix_digest": digest({str(x): {} for x in (1, -1, 2, -2)}),
                            "inverse_laws": {}}
    body = {"schema": SCHEMA + "/checkpoint/v1", "owner": "checker", "authority": authority.identity,
            "counter_registry": dict(COUNTER_TYPES),
            "code_sha256": sha(Path(__file__).read_bytes()), "next_row": next_row,
            "next_query": len(oracle.records), "B_roster": basis.b_rows, "B_ledgers": basis.b_ledgers,
            "boundary_ledgers": basis.boundary_ledgers, "combined_ledgers": basis.combined_ledgers,
            "B_coefficients": basis.b_coefficients,
            "B_formals": {label: [q, c] for label, (q, c) in basis.b_formals.items()},
            "K_roster": basis.k_items,
            "boundary_echelon": {"pivots": basis.bspace.pivots, "rows": basis.bspace.rows,
                                 "labels": basis.bspace.labels},
            "echelon_rebuild": {"pivots": basis.combined.pivots, "rows": basis.combined.rows,
                                 "labels": basis.combined.labels},
            "insertion_events": basis.insertion_events,
            "active_registry": sorted(basis.active_registry),
            "queue": queue, "queue_head": queue_head,
            "word_ledger_dag": [{key: value for key, value in node.items() if key != "states"} for node in words.nodes],
            "epoch_digest": oracle.epoch, "query_event_chain": oracle.event_chain,
            "oracle_records": oracle.records, "live_duals": oracle.live_duals,
            "dual_event_chain": oracle.dual_chain,
            "initial_terminal_chain": [event for event in oracle.event_chain
                                         if is_row_terminal(event)],
            "initial_terminal_records": [record for record in oracle.records
                                           if is_row_terminal(record)],
            "bridge_digests": list(oracle.bridge_chain),
            "bridge_cursor": len(oracle.bridge_chain),
            "bridge_replay_sha256": digest(oracle.bridge_chain),
            "bridge_prefix_canary": digest({"next_row": next_row,
                                               "bridge_cursor": len(oracle.bridge_chain),
                                               "bridge_replay_sha256": digest(oracle.bridge_chain)}),
             "row_digests": row_digests, "row_cursor": len(row_digests),
             "row_chunks": list(getattr(oracle, "row_chunks", [])),
             "samples": list(getattr(oracle, "samples", [])),
             "sample_rows": dict(getattr(oracle, "sample_rows", {})),
             "row_replay_sha256": digest(row_digests),
             "row_prefix_canary": digest({"next_row": next_row, "row_cursor": len(row_digests),
                                            "row_replay_sha256": digest(row_digests)}),
             "queue_phase": phase, "counters": dict(meter.counters),
             "completed_counters": dict(meter.semantic_counters),
             "restore_validation_counters": dict(getattr(meter, "restore_validation_counters", {})),
             "semantic_counters": dict(meter.semantic_counters), "host_counters": dict(meter.host_counters),
             "host_history": list(meter.host_history),
             "peak_counters": dict(meter.peak_counters),
             "resource_envelope": dict(meter.limits), "resource_object_caps": dict(OBJECT_CAPS),
            "next_state_canary": ""}
    body["rebuild_digest"] = checkpoint_state_digest(body)
    body["counter_digest"] = checkpoint_counter_digest(body)
    body["next_state_canary"] = checkpoint_next_state_canary(body)
    return body


def write_checkpoint(path: Path, authority: Authority, meter: Meter, next_row: int,
                     oracle: Oracle, words: WordNodeDAG, queue: list[int], queue_head: int,
                     queue_phase: dict[str, Any] | None = None) -> None:
    def make_body() -> dict[str, Any]:
        return checkpoint_payload(authority, meter, next_row, oracle, words, queue, queue_head, queue_phase)
    write_checkpoint_snapshot(path, meter, make_body, "checker.checkpoint_serialize")


def write_checkpoint_snapshot(path: Path, meter: Meter, make_body: Any, phase: str) -> None:
    """Charge each sealed snapshot, including its own counter transition."""
    start = int(meter._value("checkpoint_total_bytes")); charged = 0
    for _ in range(16):
        meter.bump("canonicalization", 2, phase)
        body = make_body(); raw = canon(body)
        sealed_body = dict(body); sealed_body["self_digest_sha256"] = sha(raw)
        encoded = canon(sealed_body); desired = len(encoded)
        require(desired <= OBJECT_CAPS["checkpoint_current_bytes"], "checker:checkpoint_current_object_cap")
        prior_peak = int(meter._value("checkpoint_peak_bytes"))
        if desired > prior_peak:
            meter.bump("checkpoint_peak_bytes", desired, phase)
            continue
        require(desired >= charged, "checker:checkpoint_fixed_point_shrunk")
        delta = desired - charged
        if delta:
            meter.reserve("checkpoint_total_bytes", delta, phase); meter.bump("checkpoint_total_bytes", delta, phase)
            charged += delta
            continue
        require(int(meter._value("checkpoint_total_bytes")) == start + charged,
                "checker:checkpoint_fixed_point_counter")
        atomic_write(path, encoded)
        return
    raise HardStop("checker:checkpoint_fixed_point_unstable")


def write_prefrontier_checkpoint(path: Path, authority: Authority, meter: Meter) -> None:
    phase = {"queue_head": 0, "queue_length": 0, "action_count": 0, "actions": [],
             "action_event_chain": [], "matrix": {str(x): {} for x in (1, -1, 2, -2)},
             "matrix_digest": digest({str(x): {} for x in (1, -1, 2, -2)}), "inverse_laws": {}}
    body = {"schema": SCHEMA + "/checkpoint/v1", "owner": "checker", "authority": authority.identity,
            "counter_registry": dict(COUNTER_TYPES),
            "code_sha256": sha(Path(__file__).read_bytes()), "next_row": 1,
            "next_query": 0, "B_roster": {}, "B_ledgers": {},
            "boundary_ledgers": {}, "combined_ledgers": {}, "B_coefficients": {},
            "B_formals": {}, "K_roster": [],
            "boundary_echelon": {"pivots": [], "rows": {}, "labels": {}},
            "echelon_rebuild": {"pivots": [], "rows": {}, "labels": {}}, "insertion_events": [], "active_registry": [],
            "queue": [], "queue_head": 0, "word_ledger_dag": [], "epoch_digest": "0" * 64,
            "query_event_chain": [], "oracle_records": [], "live_duals": [], "dual_event_chain": [],
            "initial_terminal_chain": [], "initial_terminal_records": [],
             "row_digests": [], "row_cursor": 0, "row_chunks": [], "samples": [], "sample_rows": {},
             "row_replay_sha256": digest([]),
            "row_prefix_canary": digest({"next_row": 1, "row_cursor": 0, "row_replay_sha256": digest([])}),
            "bridge_digests": [], "bridge_cursor": 0, "bridge_replay_sha256": digest([]),
            "bridge_prefix_canary": digest({"next_row": 1, "bridge_cursor": 0,
                                               "bridge_replay_sha256": digest([])}),
            "queue_phase": phase, "counters": dict(meter.counters),
            "completed_counters": dict(meter.semantic_counters),
            "restore_validation_counters": dict(getattr(meter, "restore_validation_counters", {})),
            "semantic_counters": dict(meter.semantic_counters), "host_counters": dict(meter.host_counters),
            "host_history": list(meter.host_history),
            "peak_counters": dict(meter.peak_counters),
             "resource_envelope": dict(meter.limits), "resource_object_caps": dict(OBJECT_CAPS),
            "next_state_canary": ""}
    body["rebuild_digest"] = checkpoint_state_digest(body)
    body["counter_digest"] = checkpoint_counter_digest(body)

    def make_body() -> dict[str, Any]:
        meter.completed_counters = dict(meter.semantic_counters); meter._sync()
        body.update({"counters": dict(meter.counters),
                     "completed_counters": dict(meter.semantic_counters),
                     "restore_validation_counters": dict(meter.restore_validation_counters),
                     "semantic_counters": dict(meter.semantic_counters),
                     "host_counters": dict(meter.host_counters),
                     "host_history": list(meter.host_history),
                     "peak_counters": dict(meter.peak_counters)})
        body["next_state_canary"] = checkpoint_next_state_canary(body)
        body["rebuild_digest"] = checkpoint_state_digest(body)
        body["counter_digest"] = checkpoint_counter_digest(body)
        return body
    write_checkpoint_snapshot(path, meter, make_body, "checker.prefrontier_checkpoint")


def restore_checkpoint(path: Path, authority: Authority, meter: Meter) -> dict[str, Any]:
    checked = checkpoint_input(path, "CHECKER_CHECKPOINT_RESUME")
    raw = read_once(checked, (checked.as_posix().replace(ROOT.as_posix() + "/", ""), int(os.lstat(checked).st_size), ""), meter, "checker.checkpoint_resume")
    require(len(raw) <= OBJECT_CAPS["checkpoint_current_bytes"], "checker:checkpoint_cap")
    try: value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise Reject("checker:checkpoint_json") from exc
    claimed = value.pop("self_digest_sha256", None); require(claimed == digest(value), "checker:checkpoint_seal")
    require(value.get("schema") == SCHEMA + "/checkpoint/v1" and value.get("authority") == authority.identity and
            value.get("owner") == "checker" and
            value.get("code_sha256") == sha(Path(__file__).read_bytes()), "checker:checkpoint_identity")
    counters = value.get("counters", {}); semantic = value.get("semantic_counters", {})
    completed_counters = value.get("completed_counters", {}); restore_counters = value.get("restore_validation_counters", {})
    host_counters = value.get("host_counters", {}); host_history = value.get("host_history", [])
    peak_counters = value.get("peak_counters", {})
    require(value.get("counter_registry") == COUNTER_TYPES and isinstance(counters, dict) and
            isinstance(semantic, dict) and isinstance(completed_counters, dict) and semantic == completed_counters and
            isinstance(restore_counters, dict) and isinstance(host_counters, dict) and isinstance(peak_counters, dict) and
            isinstance(host_history, list) and all(isinstance(entry, dict) and
                set(entry) == {"wall_seconds", "input_bytes"} and
                all(isinstance(number, (int, float)) and number >= 0 for number in entry.values())
                for entry in host_history) and
            set(semantic) == {key for key, kind in COUNTER_TYPES.items() if kind == "semantic"} and
            set(host_counters) == {"wall_seconds", "input_bytes"} and
            set(peak_counters) == {"rss_bytes", "checkpoint_peak_bytes"} and
            set(counters) == set(COUNTER_TYPES) and value.get("resource_envelope") == meter.limits and
            value.get("resource_object_caps") == OBJECT_CAPS and
            all(counters[key] == semantic[key] for key, kind in COUNTER_TYPES.items() if kind == "semantic") and
            counters["wall_seconds"] == host_counters["wall_seconds"] and
            counters["input_bytes"] == host_counters["input_bytes"] and
            counters["rss_bytes"] == peak_counters["rss_bytes"] and
            counters["checkpoint_peak_bytes"] == peak_counters["checkpoint_peak_bytes"] and
            counters["restore_validation"] == restore_counters.get("restore_validation", 0) and
            all(isinstance(number, (int, float)) and number >= 0 for mapping in
                (counters, semantic, completed_counters, restore_counters, host_counters, peak_counters)
                for number in mapping.values()), "checker:checkpoint_counters")
    require(value.get("counter_digest") == checkpoint_counter_digest(value),
            "checker:checkpoint_counter_digest")
    current_validation = dict(meter.restore_validation_counters)
    meter.validation_bump(1, "checker.checkpoint.restore_validate")
    merged_validation = {key: int(restore_counters.get(key, 0)) + int(current_validation.get(key, 0))
                         for key in set(restore_counters) | set(current_validation)}
    merged_validation["restore_validation"] = merged_validation.get("restore_validation", 0) + 1
    meter.restore_validation_counters = dict(merged_validation); meter._sync()
    meter.pending_completed_counters = dict(completed_counters)
    meter.pending_saved_validation = merged_validation
    meter.pending_saved_peak = dict(peak_counters)
    meter.host_history = list(host_history) + [dict(host_counters)]
    require(checkpoint_next_state_canary(value) == value.get("next_state_canary"),
            "checker:checkpoint_canary")
    require(value.get("bridge_cursor") == len(value.get("bridge_digests", [])) and
            value.get("bridge_replay_sha256") == digest(value.get("bridge_digests", [])) and
            value.get("bridge_prefix_canary") == digest({"next_row": value["next_row"],
                                                           "bridge_cursor": value["bridge_cursor"],
                                                           "bridge_replay_sha256": value["bridge_replay_sha256"]}),
             "checker:checkpoint_bridge_prefix")
    require(value.get("row_cursor") == len(value.get("row_digests", [])) and
            value.get("row_cursor") == int(value.get("next_row", 0)) - 1 and
            value.get("row_replay_sha256") == digest(value.get("row_digests", [])) and
            value.get("row_prefix_canary") == digest({"next_row": value["next_row"],
                                                         "row_cursor": value["row_cursor"],
                                                         "row_replay_sha256": value["row_replay_sha256"]}),
             "checker:checkpoint_row_prefix")
    row_prefix = value.get("row_digests", []); chunks = value.get("row_chunks", []); prior_end = 0
    require(isinstance(chunks, list), "checker:checkpoint_row_chunks_shape")
    for chunk in chunks:
        start = int(chunk.get("start", 0)); end = int(chunk.get("end", 0))
        require(start == prior_end + 1 and start <= end <= len(row_prefix) and
                chunk.get("sha256") == digest(row_prefix[start - 1:end]),
                "checker:checkpoint_row_chunk_prefix")
        prior_end = end
    require(prior_end == len(row_prefix), "checker:checkpoint_row_chunk_cursor")
    records = value.get("oracle_records", []); events = value.get("query_event_chain", [])
    require(isinstance(records, list) and isinstance(events, list) and len(records) == len(events) == int(value["next_query"]),
            "checker:checkpoint_oracle_event_prefix")
    for record, event in zip(records, events):
        require(event.get("query_id") == record.get("query_id") and event.get("schema") == record.get("schema") and
                event.get("digest") == digest(record), "checker:checkpoint_oracle_event_digest")
    require(value.get("initial_terminal_records") == [record for record in records
            if is_row_terminal(record)], "checker:checkpoint_initial_terminal_records")
    require(value.get("initial_terminal_chain") == [event for event in events
            if is_row_terminal(event)], "checker:checkpoint_initial_terminal_chain")
    epoch = "0" * 64
    for record in records: epoch = sha((epoch + digest(record)).encode("ascii"))
    require(value.get("epoch_digest") == epoch, "checker:checkpoint_epoch_chain")
    duals = value.get("live_duals", []); dual_events = value.get("dual_event_chain", [])
    require(isinstance(duals, list) and isinstance(dual_events, list) and
            len(duals) == (1 if dual_events else 0), "checker:checkpoint_dual_event_prefix")
    for index, event in enumerate(dual_events, 1):
        require(event.get("index") == index and isinstance(event.get("query_id"), str) and
                isinstance(event.get("digest"), str) and len(event["digest"]) == 64,
                "checker:checkpoint_dual_event_chain")
    if duals:
        dual = duals[0]; event = dual_events[0]
        dual_digest = digest({"query_id": dual.get("query_id"), "dual": sorted(dual.get("dual", {}).items()),
                              "target": dual.get("target"), "target_dot": dual.get("target_dot"),
                              "correlation": dual.get("correlation")})
        require(event.get("query_id") == dual.get("query_id") and
                event.get("digest") == dual_digest, "checker:checkpoint_dual_event_digest")
    phase = value.get("queue_phase", {}); require(isinstance(phase, dict) and
             phase.get("action_count") == len(phase.get("actions", [])) and
             phase.get("matrix_digest") == digest(phase.get("matrix", {})) and
             phase.get("action_count") == len(phase.get("action_event_chain", [])),
             "checker:checkpoint_queue_phase_state")
    queue = value.get("queue", []); actions = phase.get("actions", []); action_events = phase.get("action_event_chain", [])
    require(phase.get("queue_head") == value.get("queue_head") and
            phase.get("queue_length") == len(queue) and
            len(actions) == 4 * int(value.get("queue_head", 0)), "checker:checkpoint_queue_action_prefix")
    for action, event in zip(actions, action_events):
        require(event.get("digest") == digest(action) and int(action.get("letter", 0)) in (-2, -1, 1, 2) and
                isinstance(action.get("parent"), str), "checker:checkpoint_action_event_prefix")
    require(value.get("rebuild_digest") == checkpoint_state_digest(value),
            "checker:checkpoint_rebuild_digest")
    return value


def owner_specs() -> list[dict[str, Any]]:
    stages = ["authority"] * 7 + ["echelon", "echelon", "checker", "ancestry", "boundary", "dual", "closure", "anchor", "anchor",
              "resource", "terminal", "terminal", "driver", "ancestry", "trie", "trie", "ancestry", "ancestry", "checker",
              "boundary", "boundary", "boundary", "boundary", "boundary", "boundary", "boundary", "dual", "dual",
              "discrepancy", "discrepancy", "discrepancy", "discrepancy", "discrepancy", "discrepancy", "discrepancy", "dual",
              "dual", "dual", "dual", "dual", "dual", "dual"]
    return [{"name": name, "owner": OWNERS[name], "stage": stages[index]}
            for index, name in enumerate(MUTATIONS)]


def owner_digest(value: Any) -> str:
    return sha(canon(jsonable(value)))


class OwnerRoute:
    """Exercise a real loaded slot and call its normal stage validator."""
    def __init__(self, owner: str, stage: str, read: Any, write: Any,
                 mutate: Any, validate: Any):
        self.owner, self.stage, self.read, self.write = owner, stage, read, write
        self.mutate, self.validate = mutate, validate

    def exercise(self, name: str, expected: dict[str, Any] | None = None) -> dict[str, Any]:
        require(isinstance(expected, dict) and
                set(expected) == {"normal_validator", "first_rejection"} and
                expected.get("normal_validator") == self.stage and
                isinstance(expected.get("first_rejection"), str) and expected["first_rejection"],
                "checker:selftest_expected_rejection_registry:" + self.owner)
        old = self.read(); before = owner_digest(old); mutant = self.mutate(old)
        self.write(mutant)
        after = owner_digest(self.read()); require(before != after, "checker:selftest_owner_unchanged:" + self.owner)
        reached = False
        try:
            reached = True
            self.validate()
        except Reject as exc:
            first_rejection = str(exc)
            require(first_rejection == expected["first_rejection"],
                    "checker:selftest_unexpected_first_rejection:" + self.owner)
            return {"name": name, "owner": self.owner, "stage": self.stage,
                    "normal_validator": self.stage, "before_sha256": before,
                    "after_sha256": after, "reached_normal_validator": reached,
                    "first_rejection": first_rejection}
        finally:
            self.write(old)
        raise Reject("checker:selftest_owner_not_rejected:" + self.owner)


def _slot(holder: Any, key: Any, owner: str, stage: str, mutate: Any,
          validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: holder[key],
                      lambda value: holder.__setitem__(key, value), mutate, validate)


def _list_route(holder: list[Any], owner: str, stage: str, mutate: Any,
                validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: list(holder),
                      lambda value: holder.__setitem__(slice(None), value), mutate, validate)


def _flip_int(value: Any) -> int:
    require(type(value) is int, "checker:selftest_integer_owner")
    return value + 1


def _zero_int(value: Any) -> int:
    require(type(value) is int, "checker:selftest_integer_owner")
    return 0


def _flip_bool(value: Any) -> bool:
    require(type(value) is bool, "checker:selftest_boolean_owner")
    return not value


def _flip_text(value: Any) -> str:
    require(isinstance(value, str), "checker:selftest_text_owner")
    return value + "!"


def _flip_bytes(value: Any) -> bytes:
    require(isinstance(value, (bytes, bytearray)), "checker:selftest_bytes_owner")
    changed = bytearray(value); changed[-1:] = bytes([(changed[-1] ^ 1) if changed else 1])
    return type(value)(changed)


def _flip_path(value: Any) -> Path:
    require(isinstance(value, Path), "checker:selftest_path_owner")
    return Path(str(value) + ".mutated")


def _flip_sparse_coefficient(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and value, "checker:selftest_sparse_owner")
    out = dict(value); key = next(iter(out)); out[key] = 1 if int(out[key]) == 2 else 2
    return out


def _omit_sparse_entry(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and value, "checker:selftest_nonempty_sparse_owner")
    out = dict(value); out.pop(next(iter(out))); return out


def _mutate_selected(value: Any) -> list[Any]:
    if value is None: return [0, 0, "00", 1]
    require(isinstance(value, list) and len(value) == 4, "checker:selftest_selected_owner")
    out = list(value); out[3] = 1 if int(out[3]) == 2 else 2; return out


def _set_remove(value: Any) -> set[str]:
    require(isinstance(value, set) and value, "checker:selftest_active_registry_owner")
    out = set(value); out.remove(next(iter(out))); return out


def _set_route(holder: Any, owner: str, stage: str, mutate: Any,
               validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: set(holder),
                      lambda value: (holder.clear(), holder.update(value)), mutate, validate)


def _append_bad_word(value: Any) -> list[int]:
    require(isinstance(value, (list, tuple)), "checker:selftest_word_owner")
    return list(value) + [3]


def _drop_first(value: Any) -> list[Any]:
    require(isinstance(value, list) and value, "checker:selftest_list_owner")
    return list(value[1:])


def _bad_mapping(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "checker:selftest_mapping_owner")
    out = dict(value); out["__v6_mutation__"] = 1; return out


def _flip_sparse_coefficient(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and value, "checker:selftest_sparse_owner")
    out = dict(value); key = next(iter(out)); out[key] = 1 if int(out[key]) == 2 else 2
    return out


def _omit_sparse_entry(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and value, "checker:selftest_nonempty_sparse_owner")
    out = dict(value); out.pop(next(iter(out))); return out


def _mutate_selected(value: Any) -> list[Any]:
    if value is None: return [0, 0, "00", 1]
    require(isinstance(value, list) and len(value) == 4, "checker:selftest_selected_owner")
    out = list(value); out[3] = 1 if int(out[3]) == 2 else 2; return out


def _set_remove(value: Any) -> set[str]:
    require(isinstance(value, set) and value, "checker:selftest_active_registry_owner")
    out = set(value); out.remove(next(iter(out))); return out


def _set_route(holder: Any, owner: str, stage: str, mutate: Any,
               validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: set(holder),
                      lambda value: (holder.clear(), holder.update(value)), mutate, validate)


def _mapping_remove(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and value, "checker:selftest_nonempty_mapping_owner")
    out = dict(value); out.pop(next(iter(out))); return out


def _mapping_route(holder: Any, owner: str, stage: str, mutate: Any,
                   validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: dict(holder),
                      lambda value: (holder.clear(), holder.update(value)), mutate, validate)


def _invalid_orientation(value: Any) -> int:
    require(type(value) is int, "checker:selftest_orientation_owner")
    return 7 if value != 7 else 6


def owner_routes(authority: Authority, normal: dict[str, Any]) -> dict[str, OwnerRoute]:
    live = LIVE_STATE; require(live.get("basis") is not None, "checker:selftest_live_kernel_missing")
    arithmetic: CheckerArithmetic = live["arithmetic"]; boundary: Boundary = live["boundary"]
    oracle: Oracle = live["oracle"]; basis: Basis = live["basis"]
    words: WordNodeDAG = live["words"]; suffix: SuffixDAG = live["suffix"]
    anchor = live["anchor"]; matrices = live["action_matrices"]
    queue = live["queue"]; actions = live["actions"]; sample_rows = live["sample_rows"]
    require(basis.k_items and oracle.live_duals, "checker:selftest_owner_precondition:K_or_dual")
    first_item = basis.k_items[0]; first_dual = oracle.live_duals[0]; first_corr = first_dual["correlation"]
    candidate_item = next((item for item in basis.k_items if item.get("candidate_E")), None)
    prior_item = next((item for item in basis.k_items if item.get("discrepancy")), None)
    translation_item = next((item for item in basis.k_items if item.get("c")), None)
    require(candidate_item is not None, "checker:selftest_owner_precondition:candidate_E")
    require(prior_item is not None, "checker:selftest_owner_precondition:discrepancy")
    require(translation_item is not None, "checker:selftest_owner_precondition:c")

    def check_echelon() -> None:
        require(set(basis.bspace.pivots) == set(basis.bspace.rows), "checker:selftest_echelon_boundary_pivots")
        for pivot in basis.bspace.pivots:
            label = basis.bspace.labels[pivot]
            require(label in basis.boundary_ledgers and
                    basis.boundary.psi(basis.boundary_ledgers[label]) == basis.bspace.rows[pivot],
                    "checker:selftest_echelon_raw_boundary_replay")
        require(set(basis.combined.pivots) == set(basis.combined.rows), "checker:selftest_echelon_pivots")
        for pivot in basis.combined.pivots:
            label = basis.combined.labels[pivot]; require(label in basis.b_formals, "checker:selftest_echelon_formal")
            q_value, c_value = basis.b_formals[label]
            require(add_sparse(boundary.psi(q_value), basis.combined.replay(c_value, basis.k_rows)) ==
                    basis.combined.rows[pivot], "checker:selftest_echelon_replay")

    def check_k() -> None:
        prior_rank = 0
        for index, item in enumerate(basis.k_items):
            label = f"K:{index}"; require(item.get("label") == label and label in basis.k_rows,
                                             "checker:selftest_K_roster")
            require(basis.k_rows[label] == item.get("row"), "checker:selftest_K_row_owner")
            require(item.get("rank", 0) > prior_rank and item.get("pivot") in item.get("row", {}),
                    "checker:selftest_K_rank")
            prior_rank = int(item["rank"])
            require(isinstance(item.get("word"), list) and isinstance(item.get("discrepancy"), dict),
                    "checker:selftest_K_shape")
            require(all(int(letter) in (-2, -1, 1, 2) for letter in item["word"]),
                    "checker:selftest_K_word_alphabet")
            for owner_name in ("discrepancy", "candidate_E", "Q"):
                value = item.get(owner_name, {})
                require(isinstance(value, dict) and
                        all(isinstance(key, str) and key.count(":") == 2 for key in value),
                        "checker:selftest_K_raw_ledger_key:" + owner_name)
            states = [arithmetic.direct(item["word"], i) for i in range(10)]; actual = arithmetic.row(states)
            require(actual == add_sparse(item["row"], boundary.psi(item["discrepancy"])),
                    "checker:selftest_K_discrepancy")
            require(item.get("q") == list(h2_word(item["word"])), "checker:selftest_K_q")
            require(item.get("raw_coefficients") == {label: 1}, "checker:selftest_K_raw_coefficients")
            require(item.get("ancestry", {}).get("prior_labels") ==
                    sorted(item.get("c", {}).keys()), "checker:selftest_K_prior_ancestry")
            rho0 = [element_blob(state.a).hex() for state in states]
            rho1 = [{"roof": element_blob(state.a).hex(), "fox": local_row(i, state.u)}
                    for i, state in enumerate(states)]
            require(item.get("rho0") == rho0 and item.get("rho1") == rho1 and
                    item.get("rho1_actual_flattened") == actual and
                    item.get("rho1_flattened") == add_sparse(actual, boundary.psi(item["discrepancy"]), -1),
                    "checker:selftest_K_projection")
            query = next((record for record in oracle.records
                          if record.get("query_id") == item.get("ancestry", {}).get("parent_query")), None)
            require(query is not None and item.get("candidate_E") == query.get("candidate_discrepancy") and
                    item.get("Q") == query.get("Q") and item.get("c") == query.get("c") and
                    item.get("normalization_scale") == query.get("normalization_scale") and
                    item.get("E_formula") == "s*(E_v+Q-sum(c_l E_l))",
                    "checker:selftest_K_recurrence")

    def check_ancestry(index: int) -> None:
        replay_ancestry(authority.rows[index])

    def check_suffix() -> None:
        for word, node in suffix.terminals.items():
            current = 0
            for letter in reversed(word):
                current = suffix.nodes[current]["edges"].get(int(letter)); require(current is not None, "checker:selftest_suffix_edge")
            require(current == node and suffix.nodes[node]["length"] == len(word), "checker:selftest_suffix_orientation")

    def check_dual() -> None:
        dual = first_dual["dual"]; target = first_dual["target"]
        require(dual and first_dual["target_dot"] in (1, 2), "checker:selftest_dual_nonzero")
        require(all(int(value) % 3 for value in dual.values()), "checker:selftest_dual_nonzero_coefficients")
        registry = set().union(*(set(row) for row in basis.roster().values())) if basis.roster() else set()
        require(basis.active_registry == registry, "checker:selftest_active_registry_owner")
        require(set(dual) <= registry, "checker:selftest_dual_active_registry")
        for row in basis.combined.rows.values(): require(sum(int(value) * dual.get(key, 0) for key, value in row.items()) % 3 == 0, "checker:selftest_dual_dot")
        require(sum(int(value) * dual.get(key, 0) for key, value in target.items()) % 3 != 0, "checker:selftest_dual_target")
        recomputed = correlate(boundary, dual, live["meter"])
        require(recomputed["pair_count"] == first_corr["pair_count"] and recomputed["accumulator_digest"] == first_corr["accumulator_digest"] and recomputed["selected"] == first_corr["selected"], "checker:selftest_correlation")

    def check_actions() -> None:
        labels = {item["label"] for item in basis.k_items}; identity = {label: {label: 1} for label in labels}
        validate_action_matrix(matrices, labels, "checker:selftest_action_support")
        require(all(set(column) == labels for column in matrices.values()), "checker:selftest_action_complete")
        for positive, negative in (("1", "-1"), ("2", "-2")):
            require(compose(matrices[positive], matrices[negative]) == identity and compose(matrices[negative], matrices[positive]) == identity, "checker:selftest_action_inverse")

    def check_anchor() -> None:
        require(anchor.get("basis_q") == h2_projection(arithmetic, basis, live["meter"]), "checker:selftest_anchor_projection")
        require(all(int(letter) in (-2, -1, 1, 2)
                    for letter in anchor.get("powered_word", [])),
                "checker:selftest_anchor_word_alphabet")
        require(h2_word(anchor.get("powered_word", [])) == (0, 0, 3), "checker:selftest_anchor_word")
        require(compose(anchor["change_matrix"], anchor["inverse_change_matrix"]) ==
                {label: {label: 1} for label in anchor["change_matrix"]} and
                compose(anchor["inverse_change_matrix"], anchor["change_matrix"]) ==
                {label: {label: 1} for label in anchor["change_matrix"]}, "checker:selftest_anchor_matrix")

    queue_state = live["queue_state"]
    def check_queue() -> None:
        require(queue and queue_state.get("accepted") == len(queue) and queue_state.get("cursor") == len(queue) and all(index == position for position, index in enumerate(queue)), "checker:selftest_queue")

    def check_sample() -> None:
        sample = sample_rows[1]; source, parts, _ = replay_ancestry(authority.rows[0]); states = []
        for index in range(10):
            value = arithmetic.identity(index)
            for part in parts: value = value.mul(suffix.state(part, index))
            states.append(value)
        require(sample["word"] == source and sample["row"] == arithmetic.row(states), "checker:selftest_sample")

    def check_terminal() -> None:
        require(normal.get("status") == "COMPLETE" and normal.get("terminal") == PASS and normal.get("complete") is True, "checker:selftest_terminal")

    def check_driver() -> None:
        contract = normal.get("driver_contract", {})
        require(contract.get("producer_terminal_lines") == 1 and contract.get("checker_terminal_lines") == 1 and contract.get("sentinel_last") is True, "checker:selftest_driver")

    routes: dict[str, OwnerRoute] = {}
    def add(route: OwnerRoute) -> None: routes[route.owner] = route
    add(_slot(authority.rows[0], "ordinal", "authority.layer_ordinal", "authority", _zero_int, authority.validate))
    add(_slot(authority.values["manifest"], "accepted", "authority.acceptance_manifest", "authority", _flip_bool, authority.validate))
    add(_slot(authority.raw, "receipt", "authority.canonical_bytes", "authority", _flip_bytes, lambda: require(sha(authority.raw["receipt"]) == RECEIPT_SHA, "checker:selftest_input_bytes")))
    add(_slot(authority.paths, "receipt", "authority.resolved_containment", "authority", _flip_path, lambda: exact_path(str(authority.paths["receipt"]), "ci/in", AUTH["receipt"], "checker:selftest_path")))
    proof = authority.receipt["Delta0"]["presentation"]["normal_generation_proof"]
    add(_slot(proof, "Gamma_cayley_edge_count", "authority.normal_generation_proof", "authority", _flip_int, authority.validate))
    add(_slot(authority.receipt["bridge"]["occurrence_ledger"][0], "block", "authority.bridge_occurrence_ledger", "authority", _flip_text, authority.validate))
    add(_slot(authority.receipt["evaluator"]["coordinate_widths"], 0, "authority.evaluator_abi_canary", "authority", _flip_int, authority.validate))
    add(_slot(basis.bspace.rows[basis.bspace.pivots[0]], next(iter(basis.bspace.rows[basis.bspace.pivots[0]])), "echelon.raw_boundary_replay", "echelon", _flip_int, check_echelon))
    add(_slot(basis.combined.rows[basis.combined.pivots[0]], next(iter(basis.combined.rows[basis.combined.pivots[0]])), "echelon.inherited_scale", "echelon", _flip_int, check_echelon))
    add(_slot(first_item["raw_coefficients"], next(iter(first_item["raw_coefficients"])), "checker.producer_checker_basis_change", "checker", _flip_int, check_k))
    add(_slot(authority.rows[6318]["ancestry"], "tokens", "ancestry.outer_first_conjugation", "ancestry", _append_bad_word, lambda: check_ancestry(6318)))
    add(_slot(first_item, "word", "boundary.source_word_difference", "boundary", _append_bad_word, check_k))
    add(_slot(first_dual["dual"], next(iter(first_dual["dual"])), "dual.negative_functional", "dual", _zero_int, check_dual))
    add(_slot(matrices["1"], next(iter(matrices["1"])), "closure.action_matrix", "closure", _bad_mapping, check_actions))
    add(_slot(anchor["basis_q"][0], "exponent", "anchor.projected_h2_exponent", "anchor", _flip_int, check_anchor))
    add(_slot(anchor, "powered_word", "anchor.inverse_scalar_powered_word", "anchor", _append_bad_word, check_anchor))
    add(_slot(live["meter"].limits, "wall_seconds", "resource.live_cap_witness", "resource", _zero_int, lambda: require(live["meter"].limits["wall_seconds"] > 0, "checker:selftest_cap")))
    add(_slot(normal, "status", "terminal.positive_status", "terminal", lambda value: UNKNOWN_INPUT, check_terminal))
    add(_slot(normal, "complete", "terminal.false_progress", "terminal", _flip_bool, check_terminal))
    add(_slot(normal["driver_contract"], "checker_terminal_lines", "driver.duplicate_markers", "driver", _flip_int, check_driver))
    add(_slot(authority.rows[0]["ancestry"], "record_word", "ancestry.section_word_replay", "ancestry", _append_bad_word, lambda: check_ancestry(0)))
    add(_slot(suffix.nodes[1], "length", "trie.primitive_terminal", "trie", _flip_int, check_suffix))
    edge_key = next(iter(suffix.nodes[0]["edges"]))
    add(_slot(suffix.nodes[0]["edges"], edge_key, "trie.forward_edge_orientation", "trie", _flip_int, check_suffix))
    add(_slot(authority.rows[6318], "orientation", "ancestry.action_orientation", "ancestry", _invalid_orientation, lambda: check_ancestry(6318)))
    add(_slot(authority.rows[0]["ancestry"], "section_target_word", "ancestry.target_inverse", "ancestry", _append_bad_word, lambda: check_ancestry(0)))
    add(_slot(sample_rows[1]["row"], next(iter(sample_rows[1]["row"])), "checker.typed_row_equality", "checker", _flip_int, check_sample))
    add(_slot(boundary.seeds[0], "index", "boundary.base_seed_roster", "boundary", _flip_int, lambda: require([seed.index for seed in boundary.seeds] == list(range(65)), "checker:selftest_seed_roster")))
    add(_slot(authority.receipt["bridge"]["occurrence_ledger"][0], "block", "boundary.block_tag", "boundary", _flip_text, authority.validate))
    add(_slot(first_corr, "selected", "boundary.translation_orientation", "boundary", lambda value: [0] if value is None else None, check_dual))
    add(_slot(matrices["-1"], next(iter(matrices["-1"])), "boundary.inverse_action_queue", "boundary", _bad_mapping, check_actions))
    add(_slot(actions[0], "parent", "boundary.parent_action_ancestry", "boundary", _flip_text, lambda: require(actions[0]["parent"] in {item["label"] for item in basis.k_items}, "checker:selftest_parent")))
    add(_slot(queue_state, "cursor", "boundary.queue_exhaustion", "boundary", _zero_int, check_queue))
    add(_slot(first_corr, "selected", "dual.support_inversion_product", "dual", _mutate_selected, check_dual))
    add(_slot(first_corr, "pair_count", "dual.complete_zero_correlation", "dual", _zero_int, check_dual))
    add(_slot(candidate_item, "candidate_E", "discrepancy.omitted_candidate_E", "discrepancy", _omit_sparse_entry, check_k))
    add(_slot(prior_item, "discrepancy", "discrepancy.omitted_prior_K_E", "discrepancy", _omit_sparse_entry, check_k))
    add(_slot(first_item, "Q", "discrepancy.flipped_Q_sign", "discrepancy", _flip_sparse_coefficient, check_k))
    add(_slot(first_item, "normalization_scale", "discrepancy.missing_scale", "discrepancy", _zero_int, check_k))
    add(_slot(first_item, "E_formula", "discrepancy.reversed_source_action", "discrepancy", _flip_text, check_k))
    add(_slot(first_item, "discrepancy", "discrepancy.changed_raw_tag_translation", "discrepancy", _flip_sparse_coefficient, check_k))
    add(_slot(first_item, "row", "discrepancy.modulo_B_only_replay", "discrepancy", _flip_sparse_coefficient, check_k))
    add(_set_route(basis.active_registry, "dual.deleted_active_key", "dual", _set_remove, check_dual))
    add(_slot(first_dual, "dual", "dual.unregistered_nonzero_key", "dual", _bad_mapping, check_dual))
    add(_slot(basis.k_rows, first_item["label"], "dual.raw_pivot_functional", "dual", _flip_sparse_coefficient, check_k))
    add(_slot(first_corr, "pair_count", "dual.omitted_matching_occurrence", "dual", _zero_int, check_dual))
    add(_slot(translation_item, "c", "dual.incomplete_translation_key", "dual", _omit_sparse_entry, check_k))
    add(_slot(first_corr, "pair_count", "dual.premature_zero_correlation", "dual", _zero_int, check_dual))
    add(_mapping_route(basis.k_rows, "dual.omitted_new_key_registration", "dual", _mapping_remove, check_k))
    require(set(routes) == {spec["owner"] for spec in owner_specs()}, "checker:selftest_owner_registry")
    return routes


def selftest_certificate(fixture: dict[str, Any], authority: Authority, normal: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == SCHEMA + "/selftest-fixture/v6" and fixture.get("synthetic") is False and
            fixture.get("expected_mutation_count") == 48 and fixture.get("mutations") == owner_specs(), "checker:selftest_registry")
    expected_ids = {"task198_receipt": RECEIPT_SHA, "task176_receipt": TASK176["receipt"][2], "q3": Q3_SOURCE[2], "e4": E4_SOURCE[2]}
    require(fixture.get("immutable_input_identities") == expected_ids, "checker:selftest_immutable_inputs")
    expected_registry = fixture.get("expected_rejections")
    require(isinstance(expected_registry, dict) and set(expected_registry) == {"producer", "checker"} and
            isinstance(expected_registry.get("checker"), dict) and
            set(expected_registry["checker"]) == set(MUTATIONS),
            "checker:selftest_expected_rejection_registry")
    expected = expected_registry["checker"]
    routes = owner_routes(authority, normal)
    records = [routes[spec["owner"]].exercise(spec["name"], expected[spec["name"]])
               for spec in owner_specs()]
    return {"schema": SCHEMA + "/selftest", "status": "PASS", "terminal": "SELFTEST_COMPLETE", "synthetic": False,
            "input_identities": authority.identity, "mutations": {"attempted": len(records), "rejected": len(records), "records": records},
            "normal_route": {"schema": normal.get("schema"), "terminal": normal.get("terminal"), "owner_route_count": len(owner_specs())}}


def read_output(path_text: str, meter: Meter) -> tuple[bytes, dict[str, Any]]:
    path = exact_path(path_text, "ci/out", Path(path_text).name, "PRODUCER_RECEIPT")
    size = int(os.lstat(path).st_size)
    require(size <= OBJECT_CAPS["checkpoint_current_bytes"], "checker:producer_receipt_object_cap")
    meter.reserve("input_bytes", size, "producer.receipt_size")
    raw = read_once(path, (path.as_posix().replace(ROOT.as_posix() + "/", ""), size, ""), meter, "producer.receipt")
    try: value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise Reject("producer:canonical_json") from exc
    require(isinstance(value, dict), "producer:receipt_object")
    claimed = value.get("self_digest_sha256"); body = dict(value); body.pop("self_digest_sha256", None)
    require(claimed == digest(body), "producer:receipt_seal")
    serialization = value.get("serialization")
    require(isinstance(serialization, dict) and
            isinstance(serialization.get("output_bytes"), int) and
            serialization.get("output_bytes") == len(raw),
            "producer:serialized_output_bytes")
    return raw, value


def compare_kernel(producer: dict[str, Any], checker: dict[str, Any], authority: str) -> None:
    pk, ck = producer["kernel"], checker["kernel"]
    required_producer = {"schema", "status", "terminal", "complete", "A4_presentation_input",
                         "A4_invariant_closure", "A4_word_bearing_K", "authority", "runtime",
                         "primitive_inventory", "forward_dag", "kernel", "performance", "resource",
                         "driver_contract", "forbidden_downstream", "resume", "serialization",
                         "self_digest_sha256"}
    require(set(producer) == required_producer and producer.get("schema") == SCHEMA and
            producer.get("status") == "COMPLETE" and producer.get("terminal") == PASS and
            producer.get("complete") is True and producer.get("accepted") is None and
            producer.get("independent") is None, "producer:positive_terminal_schema")
    required_checker = {"schema", "status", "terminal", "accepted", "independent", "complete",
                        "A4_presentation_input", "A4_invariant_closure", "A4_word_bearing_K",
                        "authority", "runtime", "primitive_inventory", "reverse_suffix_dag", "kernel",
                        "performance", "resource", "driver_contract", "forbidden_downstream", "resume"}
    require(set(checker) == required_checker and checker.get("schema") == SCHEMA and checker.get("status") == "COMPLETE" and
            checker.get("terminal") == PASS and checker.get("accepted") is True and
            checker.get("independent") is True and checker.get("complete") is True,
            "checker:positive_terminal_schema")
    require(producer.get("authority") == authority and checker.get("authority") == authority and
            producer.get("authority") == checker.get("authority"), "checker:authority_identity")
    require(producer.get("resume") == checker.get("resume"), "checker:resume_owner")
    expected_contexts = [{"index": i, "type": CONTEXT_TYPES[i],
                          "context_id": CONTEXT_IDS[i], "tag": CONTEXT_TAGS[i]}
                         for i in range(10)]
    producer_limits = producer.get("resource", {}).get("limits")
    checker_limits = checker.get("resource", {}).get("limits")
    require(isinstance(producer_limits, dict) and isinstance(checker_limits, dict) and
            producer_limits == PRODUCER_CAPS and checker_limits == CAPS and
            all(producer_limits[key] == checker_limits[key]
                for key in set(PRODUCER_CAPS) & set(CAPS)),
            "checker:compatible_resource_limits")
    for result, label in ((producer, "producer"), (checker, "checker")):
        expected_caps = PRODUCER_CAPS if label == "producer" else CAPS
        expected_types = PRODUCER_COUNTER_TYPES if label == "producer" else COUNTER_TYPES
        runtime = result.get("runtime", {})
        require(runtime.get("contexts") == expected_contexts and
                runtime.get("affine_law") == "(a,u)*(b,v)=(a*b,u+a.v)" and
                runtime.get("inverse_law") ==
                "S(x^-1)=(rho(x)^-1,-rho(x)^-1 delta(x))" and
                runtime.get("actor_cache_signed") == 40 and
                runtime.get("actual_inverse_word_checks") is True,
                "checker:" + label + "_runtime_owner")
        inventory = result.get("primitive_inventory", {})
        require(inventory.get("sections") == 243 and inventory.get("records") == 26 and
                inventory.get("q0_relators") == 19 and inventory.get("primitive_words") == 288 and
                inventory.get("literal_primitive_letters") == 114458 and
                inventory.get("stored_row_letters") == 5475488,
                "checker:" + label + "_primitive_inventory")
        if label == "producer":
            dag = result.get("forward_dag", {})
            require(dag.get("nodes") == 15971 and dag.get("edges") == 15970 and
                    dag.get("edge_state_products") == 159700 and
                    dag.get("all_primitive_terminals_used_by_row_assembly") is True,
                    "checker:producer_forward_dag_owner")
        else:
            dag = result.get("reverse_suffix_dag", {})
            require(dag.get("nodes") == 26137 and dag.get("edges") == 26136 and
                    dag.get("edge_state_products") == 261360 and
                    dag.get("right_associated") is True and
                    dag.get("all_primitive_terminals_used_by_row_assembly") is True,
                    "checker:checker_reverse_dag_owner")
        performance = result.get("performance", {})
        measured = performance.get("measured")
        require(performance.get("n") == ROWS and performance.get("t") == len(result["kernel"]["K_roster"]) and
                performance.get("p") == result["kernel"]["boundary"]["rank"] and
                performance.get("Q") == ROWS + 4 * performance.get("t") + 1 and
                performance.get("row_piece_products") == 19408 and
                isinstance(measured, dict) and set(measured) ==
                {"status", "owner", "wall_seconds", "input_bytes", "rss_bytes"} and
                measured.get("status") == "RUNTIME" and
                measured.get("owner") == "resource.host_counters" and
                all(isinstance(measured.get(key), (int, float)) and measured.get(key) >= 0
                    for key in ("wall_seconds", "input_bytes", "rss_bytes")),
                "checker:" + label + "_performance_owner")
        resource = result.get("resource", {})
        counters = resource.get("counters", {})
        semantic = resource.get("semantic_counters", {})
        completed = resource.get("completed_counters", {})
        host = resource.get("host_counters", {})
        host_history = resource.get("host_history", [])
        peak = resource.get("peak_counters", {})
        restore = resource.get("restore_validation_counters", {})
        require(resource.get("counter_registry") == expected_types and
                resource.get("limits") == expected_caps and
                set(counters) == set(expected_types) and
                set(semantic) == {key for key, kind in expected_types.items() if kind == "semantic"} and
                set(completed) == set(semantic) and completed == semantic and
                set(host) == {"wall_seconds", "input_bytes"} and
                isinstance(host_history, list) and
                all(isinstance(entry, dict) and set(entry) == {"wall_seconds", "input_bytes"} and
                    all(isinstance(value, (int, float)) and value >= 0 for value in entry.values())
                    for entry in host_history) and
                set(peak) == {"rss_bytes", "checkpoint_peak_bytes"} and
                set(restore) <= {key for key, kind in expected_types.items() if kind == "validation"} and
                all(counters[key] == semantic[key] for key, kind in expected_types.items()
                    if kind == "semantic") and
                counters["wall_seconds"] == host["wall_seconds"] and
                counters["input_bytes"] == host["input_bytes"] and
                counters["rss_bytes"] == peak["rss_bytes"] and
                counters["checkpoint_peak_bytes"] == peak["checkpoint_peak_bytes"] and
                counters["restore_validation"] == restore.get("restore_validation", 0) and
                resource.get("object_caps") == OBJECT_CAPS and
                measured["wall_seconds"] == host["wall_seconds"] and
                measured["input_bytes"] == host["input_bytes"] and
                measured["rss_bytes"] == peak["rss_bytes"] and
                all(isinstance(value, (int, float)) and value >= 0 and
                    value <= expected_caps[key]
                    for key, value in counters.items()),
                "checker:" + label + "_resource_owner")
    forbidden = {"lift": False, "fake": False, "Ihara": False,
                 "base_pairs": False, "ambient_E3_E4_enumeration": False}
    require(producer.get("forbidden_downstream") == forbidden and
            checker.get("forbidden_downstream") == forbidden, "checker:forbidden_downstream")
    require(producer.get("A4_presentation_input") == 1 and
            producer.get("A4_invariant_closure") == 1 and producer.get("A4_word_bearing_K") == 1 and
            checker.get("A4_presentation_input") == 1 and checker.get("A4_invariant_closure") == 1 and
            checker.get("A4_word_bearing_K") == 1, "checker:A4_flags")
    require(pk["row_stream"] == ck["row_stream"], "checker:row_stream_two_way")
    require(pk.get("bridge") == ck.get("bridge"), "checker:bridge_two_way")
    require(pk["initial"] == ck["initial"], "checker:initial_terminal_two_way")
    validate_action_matrix(pk["action_matrices"],
                           {item["label"] for item in pk["K_roster"]},
                           "checker:producer_action_matrix_support")
    validate_action_matrix(ck["action_matrices"],
                           {item["label"] for item in ck["K_roster"]},
                           "checker:checker_action_matrix_support")
    require(pk["action_matrices"] == ck["action_matrices"], "checker:action_matrix_two_way")
    require(pk["queue"] == ck["queue"] and pk["boundary"]["seed_count"] == ck["boundary"]["seed_count"] and
            pk["boundary"]["rank"] == ck["boundary"]["rank"], "checker:closure_two_way")
    pboundary, cboundary = pk["boundary"], ck["boundary"]
    def span_reduce(rows: dict[str, dict[str, int]], value: dict[str, int]) -> dict[str, int]:
        pivots: list[str] = []; stored: dict[str, dict[str, int]] = {}
        for source in rows.values():
            remainder = {key: int(raw) % 3 for key, raw in source.items() if int(raw) % 3}
            for pivot in pivots:
                factor = remainder.get(pivot, 0)
                if factor: remainder = add_sparse(remainder, stored[pivot], -factor)
            if remainder:
                pivot = min(remainder); scalar = 1 if remainder[pivot] == 1 else 2
                stored[pivot] = {key: (int(raw) * scalar) % 3 for key, raw in remainder.items()
                                 if (int(raw) * scalar) % 3}; pivots.append(pivot)
        for pivot in pivots:
            factor = value.get(pivot, 0)
            if factor: value = add_sparse(value, stored[pivot], -factor)
        return value
    def roster_rows(boundary: dict[str, Any], label: str) -> dict[str, dict[str, int]]:
        roster = boundary.get("pure_B_roster")
        require(isinstance(roster, list), "checker:" + label + "_pure_roster_shape")
        rows: dict[str, dict[str, int]] = {}
        for index, item in enumerate(roster):
            require(isinstance(item, dict) and set(item) ==
                    {"label", "pivot", "column", "raw_identity", "boundary_row",
                     "boundary_reduction", "boundary_scale", "boundary_ledger",
                     "combined_row", "combined_formal"},
                    "checker:" + label + "_pure_roster_fields")
            key = str(item["label"]); require(key == f"B:{index}" and key not in rows,
                                              "checker:" + label + "_pure_roster_order")
            require(isinstance(item["boundary_row"], dict) and item["boundary_row"],
                    "checker:" + label + "_pure_roster_row")
            rows[key] = dict(item["boundary_row"])
        return rows

    pure_p, pure_c = roster_rows(pboundary, "producer"), roster_rows(cboundary, "checker")
    require(all(not span_reduce(pure_c, dict(row)) for row in pure_p.values()) and
            all(not span_reduce(pure_p, dict(row)) for row in pure_c.values()),
            "checker:boundary_span_two_way_reduction")
    def canonical_span_digest(rows: dict[str, dict[str, int]]) -> str:
        pivots: list[str] = []; stored: dict[str, dict[str, int]] = {}
        for key in sorted(rows):
            remainder = {name: int(raw) % 3 for name, raw in rows[key].items() if int(raw) % 3}
            for pivot in pivots:
                factor = remainder.get(pivot, 0)
                if factor: remainder = add_sparse(remainder, stored[pivot], -factor)
            if remainder:
                pivot = min(remainder); scalar = 1 if remainder[pivot] == 1 else 2
                stored[pivot] = {name: (int(raw) * scalar) % 3 for name, raw in remainder.items()
                                 if (int(raw) * scalar) % 3}; pivots.append(pivot)
        return digest({"pivots": pivots, "rows": stored})
    require(isinstance(pboundary.get("mixed_basis"), dict) and isinstance(cboundary.get("mixed_basis"), dict) and
            canonical_span_digest(pboundary["mixed_basis"]) == canonical_span_digest(cboundary["mixed_basis"]),
            "checker:mixed_span_canonical_owner")
    require(pboundary.get("epoch_digest") == cboundary.get("epoch_digest") and
            pboundary.get("record_count") == cboundary.get("record_count") and
            pboundary.get("terminal_digest") == cboundary.get("terminal_digest") and
            pboundary.get("event_digest") == cboundary.get("event_digest"),
            "checker:boundary_terminal_payload")
    require(pk["inverse_laws"] == ck["inverse_laws"], "checker:inverse_laws_two_way")
    pitems, citems = pk["K_roster"], ck["K_roster"]
    require(len(pitems) == len(citems) and [item["label"] for item in pitems] == [item["label"] for item in citems], "checker:chronological_K_roster")
    fields = ("label", "row", "word", "discrepancy", "pivot", "rank", "raw_coefficients",
              "rho0", "rho1", "rho1_flattened", "rho1_actual_flattened", "q",
              "candidate_word", "candidate_E", "Q", "c", "normalization_scale",
              "word_formula", "E_formula", "replay", "strict_rank_rise")
    for producer_item, checker_item in zip(pitems, citems):
        require(set(producer_item) == set(checker_item) ==
                set(fields) | {"ancestry"},
                "checker:K_owner_schema")
        for field in fields: require(producer_item.get(field) == checker_item.get(field), "checker:K_owner:" + field)
        require(producer_item.get("ancestry") == checker_item.get("ancestry"), "checker:K_owner:ancestry")
    require(pk["anchor_diagnostics"] == ck["anchor_diagnostics"], "checker:v280_recomputed_anchor")
    require(ck["maxpivot_canary"]["differ"] is True, "checker:maxpivot_canary")


def positive_result(authority: Authority, meter: Meter, checkpoint: Path | None = None,
                   resume_state: dict[str, Any] | None = None) -> dict[str, Any]:
    arithmetic = CheckerArithmetic(authority, meter); primitive, inventory = primitive_inventory(authority); suffix = SuffixDAG(arithmetic, meter)
    kernel = build_checker_kernel(authority, arithmetic, suffix, primitive, inventory, meter,
                                  checkpoint, resume_state)
    meter._sync()
    resource = meter.public()
    measurement = {"status": "RUNTIME", "owner": "resource.host_counters",
                    "wall_seconds": resource["host_counters"]["wall_seconds"],
                    "input_bytes": resource["host_counters"]["input_bytes"],
                    "rss_bytes": resource["peak_counters"]["rss_bytes"]}
    return {"schema": SCHEMA, "status": "COMPLETE", "terminal": PASS, "accepted": True, "independent": True,
            "complete": True, "A4_presentation_input": 1, "A4_invariant_closure": 1, "A4_word_bearing_K": 1,
            "authority": authority.identity, "runtime": {"contexts": [{"index": i, "type": CONTEXT_TYPES[i], "context_id": CONTEXT_IDS[i], "tag": CONTEXT_TAGS[i]} for i in range(10)],
                       "affine_law": "(a,u)*(b,v)=(a*b,u+a.v)", "inverse_law": "S(x^-1)=(rho(x)^-1,-rho(x)^-1 delta(x))",
                       "actor_cache_signed": 40, "actual_inverse_word_checks": True, "independent_module": True},
            "primitive_inventory": {**inventory, "suffix_edges": len(suffix.nodes) - 1},
            "reverse_suffix_dag": {"nodes": len(suffix.nodes), "edges": len(suffix.nodes) - 1,
                                   "edge_state_products": 10 * (len(suffix.nodes) - 1), "right_associated": True,
                                   "all_primitive_terminals_used_by_row_assembly": True},
            "kernel": kernel, "performance": {"n": ROWS, "t": len(kernel["K_roster"]), "p": kernel["boundary"]["rank"],
                         "Q": ROWS + 4 * len(kernel["K_roster"]) + 1, "correlation_pair_sum": meter.counters.get("correlation_pairs", 0),
                         "row_piece_products": meter.counters.get("row_piece_products", 0), "checkpoint": str(checkpoint) if checkpoint else None,
                         "measured": measurement}, "resource": resource,
            "driver_contract": {"producer_terminal_lines": 1,
                                 "checker_terminal_lines": 1,
                                 "sentinel_last": True,
                                 "typed_unknown_exit_zero": True},
            "forbidden_downstream": {"lift": False, "fake": False, "Ihara": False, "base_pairs": False, "ambient_E3_E4_enumeration": False},
            "resume": {"restored": resume_state is not None,
                       "next_row": (resume_state or {}).get("next_row", 1),
                       "rebuild_compared": resume_state is not None}}


def checkpoint_reference(path: Path | None, meter: Meter,
                         authority_identity: str | None = None) -> dict[str, Any]:
    if not meter.authority_complete and authority_identity is None:
        return {"kind": "pre_authority_resource", "owner": "checker", "authority": None,
                "state": PRE_AUTHORITY_STATE, "path": str(path) if path else None,
                "bytes": 0, "sha256": None, "replayable": False}
    if path is None or not path.exists():
        return {"kind": "missing_checkpoint", "path": str(path) if path else None,
                "bytes": 0, "sha256": None, "replayable": False}
    try:
        checked = checkpoint_input(path, "CHECKER_TERMINAL_CHECKPOINT_REFERENCE")
        size = int(os.lstat(checked).st_size)
        require(size <= OBJECT_CAPS["checkpoint_current_bytes"], "checker:terminal_checkpoint_object_cap")
        raw = read_once(checked, (checked.as_posix().replace(ROOT.as_posix() + "/", ""), size, ""),
                         meter, "checker.terminal_checkpoint_reference", terminal_transport=True)
        value = json.loads(raw.decode("ascii")); claimed = value.get("self_digest_sha256")
        body = dict(value); body.pop("self_digest_sha256", None)
        require(claimed == digest(body) and value.get("schema") == SCHEMA + "/checkpoint/v1" and
                value.get("owner") == "checker" and isinstance(value.get("code_sha256"), str) and
                isinstance(value.get("next_state_canary"), str), "checker:terminal_checkpoint_seal")
    except Exception:
        return {"kind": "missing_checkpoint", "path": str(path), "bytes": 0,
                "sha256": None, "replayable": False}
    return {"kind": "sealed_checkpoint", "path": checked.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": sha(raw), "owner": value["owner"], "code_sha256": value["code_sha256"],
            "next_row": value["next_row"], "next_state_canary": value["next_state_canary"],
            "checkpoint_self_digest_sha256": claimed, "replayable": True, "sealed": True}


def validate_terminal_checkpoint(reference: dict[str, Any], authority: Authority | None, meter: Meter) -> None:
    require(isinstance(reference, dict), "checker:terminal_checkpoint_shape")
    if reference.get("kind") == "pre_authority_resource":
        require(set(reference) == {"kind", "owner", "authority", "state", "path", "bytes",
                                   "sha256", "replayable"} and reference.get("owner") == "producer" and
                reference.get("authority") is None and reference.get("state") == PRE_AUTHORITY_STATE and
                reference.get("bytes") == 0 and reference.get("sha256") is None and
                reference.get("replayable") is False,
                "checker:pre_authority_resource")
        return
    require(reference.get("replayable") is True, "checker:terminal_checkpoint_shape")
    require(reference.get("kind") == "sealed_checkpoint" and
            isinstance(reference.get("path"), str) and isinstance(reference.get("bytes"), int) and
            isinstance(reference.get("sha256"), str), "checker:terminal_checkpoint_physical")
    path = checkpoint_input(Path(reference["path"]), "CHECKER_TERMINAL_CHECKPOINT")
    require(int(reference["bytes"]) <= OBJECT_CAPS["checkpoint_current_bytes"],
            "checker:terminal_checkpoint_object_cap")
    raw = read_once(path, (path.as_posix().replace(ROOT.as_posix() + "/", ""),
                           reference["bytes"], reference["sha256"]), meter,
                    "checker.terminal_checkpoint", terminal_transport=True)
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject("checker:terminal_checkpoint_json") from exc
    claimed = value.pop("self_digest_sha256", None)
    require(claimed == digest(value) and value.get("schema") == SCHEMA + "/checkpoint/v1" and
            value.get("owner") == "producer" and reference.get("owner") == "producer" and
            value.get("code_sha256") == reference.get("code_sha256") and
            value.get("code_sha256") == sha((ROOT / PRODUCER_CODE_PATH).read_bytes()) and
            reference.get("checkpoint_self_digest_sha256") == claimed and
            value.get("authority") == (authority.identity if authority is not None else None) and
            1 <= int(value.get("next_row", 0)) <= ROWS + 1 and
            checkpoint_next_state_canary(value) == value.get("next_state_canary") and
            value.get("counter_digest") == checkpoint_counter_digest(value) and
            value.get("rebuild_digest") == checkpoint_state_digest(value) and
            value.get("counter_registry") == PRODUCER_COUNTER_TYPES and
            value.get("resource_envelope") == PRODUCER_CAPS and
            isinstance(value.get("counters"), dict) and isinstance(value.get("semantic_counters"), dict) and
            value.get("completed_counters") == value.get("semantic_counters") and
            set(value.get("counters", {})) == set(PRODUCER_COUNTER_TYPES) and
            set(value.get("semantic_counters", {})) == {key for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "semantic"} and
            set(value.get("host_counters", {})) == {"wall_seconds", "input_bytes"} and
            set(value.get("peak_counters", {})) == {"rss_bytes", "checkpoint_peak_bytes"} and
            value["counters"]["wall_seconds"] == value["host_counters"]["wall_seconds"] and
            value["counters"]["input_bytes"] == value["host_counters"]["input_bytes"] and
            value["counters"]["rss_bytes"] == value["peak_counters"]["rss_bytes"] and
            value["counters"]["checkpoint_peak_bytes"] == value["peak_counters"]["checkpoint_peak_bytes"] and
            all(value["counters"][key] == value["semantic_counters"][key]
                for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "semantic") and
            isinstance(value.get("restore_validation_counters"), dict) and
            set(value["restore_validation_counters"]) <=
                {key for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "validation"} and
            value["counters"]["restore_validation"] ==
                value["restore_validation_counters"].get("restore_validation", 0) and
            isinstance(value.get("host_history"), list) and
            all(isinstance(entry, dict) and set(entry) == {"wall_seconds", "input_bytes"} and
                all(isinstance(number, (int, float)) and number >= 0 for number in entry.values())
                for entry in value["host_history"]) and
            value.get("resource_object_caps") == OBJECT_CAPS and
            value.get("bridge_cursor") == len(value.get("bridge_digests", [])) and
            value.get("bridge_replay_sha256") == digest(value.get("bridge_digests", [])) and
            value.get("bridge_prefix_canary") == digest({"next_row": value["next_row"],
                                                            "bridge_cursor": value["bridge_cursor"],
                                                            "bridge_replay_sha256": value["bridge_replay_sha256"]}) and
            value.get("row_cursor") == len(value.get("row_digests", [])) and
            value.get("row_cursor") == int(value.get("next_row", 0)) - 1 and
            value.get("row_replay_sha256") == digest(value.get("row_digests", [])) and
            value.get("row_prefix_canary") == digest({"next_row": value["next_row"],
                                                         "row_cursor": value["row_cursor"],
                                                         "row_replay_sha256": value["row_replay_sha256"]}),
            "checker:terminal_checkpoint_replayable")


def validate_terminal_payload(producer: dict[str, Any], status: str,
                              authority: Authority | None, meter: Meter) -> None:
    """Independently authenticate a producer typed nonpositive terminal.

    The checker transports only a typed terminal after validating its complete
    envelope and the narrow reason witness; it never treats a copied status or
    prose reason as evidence.
    """
    require(set(producer) == {"schema", "status", "terminal", "complete", "authority",
                              "reason", "checkpoint", "resource", "forbidden_downstream",
                              "serialization", "self_digest_sha256"},
            "checker:producer_terminal_schema")
    producer_authority = producer.get("authority")
    pre_authority = producer_authority is None
    require(producer.get("schema") == SCHEMA and producer.get("status") == status and
            producer.get("terminal") == status and producer.get("complete") is False and
            (producer_authority == (authority.identity if authority is not None else None) or pre_authority) and
            isinstance(producer.get("reason"), str) and producer.get("reason") and
            producer.get("forbidden_downstream") ==
            {"lift": False, "fake": False, "Ihara": False},
            "checker:producer_terminal_identity")
    resource = producer.get("resource")
    terminal_counters = resource.get("counters", {}) if isinstance(resource, dict) else {}
    terminal_semantic = resource.get("semantic_counters", {}) if isinstance(resource, dict) else {}
    terminal_completed = resource.get("completed_counters", {}) if isinstance(resource, dict) else {}
    terminal_restore = resource.get("restore_validation_counters", {}) if isinstance(resource, dict) else {}
    terminal_host = resource.get("host_counters", {}) if isinstance(resource, dict) else {}
    terminal_peak = resource.get("peak_counters", {}) if isinstance(resource, dict) else {}
    serialization = producer.get("serialization")
    require(isinstance(resource, dict) and resource.get("limits") == PRODUCER_CAPS and
            resource.get("counter_registry") == PRODUCER_COUNTER_TYPES and
            isinstance(terminal_counters, dict) and set(terminal_counters) == set(PRODUCER_COUNTER_TYPES) and
            isinstance(terminal_semantic, dict) and
            set(terminal_semantic) == {key for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "semantic"} and
            isinstance(terminal_completed, dict) and terminal_completed == terminal_semantic and
            isinstance(terminal_restore, dict) and
            set(terminal_restore) <= {key for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "validation"} and
            isinstance(terminal_host, dict) and set(terminal_host) == {"wall_seconds", "input_bytes"} and
            isinstance(resource.get("host_history"), list) and
            all(isinstance(entry, dict) and set(entry) == {"wall_seconds", "input_bytes"} and
                all(isinstance(number, (int, float)) and number >= 0 for number in entry.values())
                for entry in resource["host_history"]) and
            isinstance(terminal_peak, dict) and set(terminal_peak) == {"rss_bytes", "checkpoint_peak_bytes"} and
            terminal_counters["wall_seconds"] == terminal_host["wall_seconds"] and
            terminal_counters["input_bytes"] == terminal_host["input_bytes"] and
            terminal_counters["rss_bytes"] == terminal_peak["rss_bytes"] and
            terminal_counters["checkpoint_peak_bytes"] == terminal_peak["checkpoint_peak_bytes"] and
            terminal_counters["restore_validation"] == terminal_restore.get("restore_validation", 0) and
            all(terminal_counters[key] == terminal_semantic[key]
                for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "semantic") and
            resource.get("object_caps") == OBJECT_CAPS and
            all(isinstance(number, (int, float)) and number >= 0
                and number <= PRODUCER_CAPS[key]
                for mapping in (terminal_counters, terminal_semantic, terminal_completed,
                                terminal_restore, terminal_host, terminal_peak)
                for key, number in mapping.items()),
            "checker:producer_terminal_resource_envelope")
    require(isinstance(serialization, dict) and
            set(serialization) == {"canonicalization", "atomic", "terminal_transport",
                                   "terminal_canonicalization", "serialized_work_bytes",
                                   "output_bytes", "final_write"} and
            serialization.get("canonicalization") is True and serialization.get("atomic") is True and
            serialization.get("terminal_transport") is True and
            serialization.get("terminal_canonicalization") == terminal_counters["terminal_canonicalization"] and
            serialization.get("serialized_work_bytes") == terminal_counters["terminal_serialized_bytes"] and
            serialization.get("final_write") == terminal_counters["terminal_final_write"] and
            isinstance(serialization.get("output_bytes"), int) and
            serialization["output_bytes"] > 0 and
            serialization["output_bytes"] <= OBJECT_CAPS["checkpoint_current_bytes"],
            "checker:producer_terminal_serialization")
    reason = producer["reason"]
    if status == UNKNOWN_INPUT:
        allowed = ("authority.", "authority:", "task176.", "task176:",
                   "pinned.", "pinned:", "checkpoint", "selftest.",
                   "ancestry:", "evaluator:", "primitive:", "anchor:all_q_exponents_zero:UNKNOWN_INPUT",
                   "input", "path:")
        require(reason.startswith(allowed) and "TypeError" not in reason and
                "HARD_STOP" not in reason, "checker:producer_unknown_input_reason")
        if pre_authority:
            require(reason.startswith(("authority.", "authority:", "task176.", "task176:",
                                       "pinned.", "pinned:", "input", "path:")) and
                    producer.get("checkpoint", {}).get("kind") == "pre_authority_resource" and
                    producer.get("checkpoint", {}).get("owner") == "producer" and
                    producer.get("checkpoint", {}).get("authority") is None and
                    producer.get("checkpoint", {}).get("state") == PRE_AUTHORITY_STATE and
                    producer.get("checkpoint", {}).get("bytes") == 0 and
                    producer.get("checkpoint", {}).get("sha256") is None and
                    producer.get("checkpoint", {}).get("replayable") is False,
                    "checker:pre_authority_unknown_input")
        if "windows_same_handle_identity_unavailable" in reason:
            require(os.name == "nt", "checker:producer_windows_reason")
    elif status == UNKNOWN_RESOURCE:
        witness = re.search(r"(?P<cap>[A-Za-z0-9_]+):(?P<value>[0-9]+(?:\.[0-9]+)?)>(?P<limit>[0-9]+(?:\.[0-9]+)?):state=(?P<state>.+)$", reason)
        require(witness is not None, "checker:producer_resource_reason")
        cap = witness.group("cap"); value = float(witness.group("value")); limit = float(witness.group("limit"))
        require(cap in PRODUCER_COUNTER_TYPES and value > limit and
                resource["counters"].get(cap, 0) >= value and
                float(resource["limits"].get(cap, -1)) == limit and
                resource.get("last_replayable_state") == witness.group("state"),
                "checker:producer_resource_witness")
        if pre_authority:
            require(producer.get("checkpoint", {}).get("state") == PRE_AUTHORITY_STATE and
                    producer.get("checkpoint", {}).get("kind") == "pre_authority_resource" and
                    producer.get("checkpoint", {}).get("owner") == "producer" and
                    producer.get("checkpoint", {}).get("authority") is None and
                    producer.get("checkpoint", {}).get("state") == PRE_AUTHORITY_STATE and
                    producer.get("checkpoint", {}).get("bytes") == 0 and
                    producer.get("checkpoint", {}).get("sha256") is None and
                    producer.get("checkpoint", {}).get("replayable") is False,
                    "checker:pre_authority_unknown_resource")


def terminal_certificate(status: str, reason: str, meter: Meter,
                         checkpoint: Path | None = None,
                         producer_checkpoint: dict[str, Any] | None = None,
                         authority_identity: str | None = None) -> dict[str, Any]:
    meter._sync()
    reference = producer_checkpoint or checkpoint_reference(checkpoint, meter, authority_identity)
    return {"schema": SCHEMA, "status": status, "terminal": status, "accepted": False,
            "independent": True, "complete": False, "authority": authority_identity, "reason": reason,
            "checkpoint": reference,
            "resource": {"limits": meter.limits, "counter_registry": dict(meter.counter_types),
                          "counters": dict(meter.counters),
                          "semantic_counters": dict(meter.semantic_counters),
                          "completed_counters": dict(meter.completed_counters),
                          "restore_validation_counters": dict(meter.restore_validation_counters),
                          "host_counters": dict(meter.host_counters),
                          "host_history": list(meter.host_history),
                          "peak_counters": dict(meter.peak_counters),
                          "object_caps": dict(OBJECT_CAPS),
                          "last_replayable_state": meter.state_name,
                          "terminal_checkpoint": reference},
            "forbidden_downstream": {"lift": False, "fake": False, "Ihara": False}}


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(); parser.add_argument("--selftest", action="store_true"); parser.add_argument("--fixture")
    parser.add_argument("--producer"); parser.add_argument("--output"); parser.add_argument("--checkpoint"); parser.add_argument("--resume")
    parser.add_argument("--input", default="ci/in/d972_r07_seven_context_roof_presentation_v1.json")
    parser.add_argument("--seconds", type=int, default=14400); parser.add_argument("--rss-bytes", type=int, default=8000000000)
    for key, value in AUTH.items(): parser.add_argument("--task198-" + key.replace("_", "-"), dest="task198_" + key, default="ci/in/" + value)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv); meter = Meter({**CAPS, "wall_seconds": args.seconds, "rss_bytes": args.rss_bytes})
    meter.restore_mode = bool(args.resume)
    checkpoint_arg: Path | None = None
    resume_arg: Path | None = None
    output: Path | None = None
    authority_identity: str | None = None
    try:
        # Resolve caller-controlled output/checkpoint names only under the
        # typed-input guard.  An unsafe target is a fail-closed transport stop,
        # never an unhandled path exception before terminal handling exists.
        try:
            if args.output:
                output = output_path(args.output, "ci/out", "CHECKER_OUTPUT")
            if args.checkpoint:
                checkpoint_text = str(args.checkpoint).replace("\\", "/")
                checkpoint_arg = output_path(checkpoint_text, "ci/out", "CHECKER_CHECKPOINT")
            if args.resume:
                resume_text = str(args.resume).replace("\\", "/")
                resume_path = Path(resume_text)
                resume_arg = exact_path(resume_text, "ci/out", resume_path.name, "CHECKER_CHECKPOINT_RESUME")
        except Reject as exc:
            raise HardStop("checker:transport:untrusted_output_path:" + str(exc)) from exc
        require(args.seconds == CAPS["wall_seconds"] and args.rss_bytes == CAPS["rss_bytes"],
                "checker:driver_registered_wall_rss_limits")
        # A producer pre-authority terminal must be authenticated before the
        # checker opens the heavy authority.  Otherwise a malformed/missing
        # producer input is masked by the checker's own authority stop and
        # cannot be independently transported.
        producer: dict[str, Any] | None = None
        pstatus: str | None = None
        if not args.selftest:
            if args.producer is None:
                raise Reject("CHECKER_PRODUCER_REQUIRED")
            _, producer = read_output(args.producer, meter)
            pstatus = producer.get("status")
            require(pstatus in (PASS, "COMPLETE", UNKNOWN_INPUT, UNKNOWN_RESOURCE, HARD_STOP),
                    "producer:terminal_token")
            if pstatus in (UNKNOWN_INPUT, UNKNOWN_RESOURCE, HARD_STOP) or \
                    producer.get("terminal") in (UNKNOWN_INPUT, UNKNOWN_RESOURCE, HARD_STOP):
                status = producer.get("terminal") if producer.get("terminal") in \
                    (UNKNOWN_INPUT, UNKNOWN_RESOURCE, HARD_STOP) else pstatus
                if status == HARD_STOP:
                    raise HardStop("producer:hard_stop_propagation")
                # AUTHORITY_UNREAD is a closed, separately typed route.  Do
                # not construct Authority merely to reject a receipt whose
                # authority cannot yet exist.
                if producer.get("authority") is None:
                    producer_checkpoint = producer.get("checkpoint")
                    validate_terminal_payload(producer, status, None, meter)
                    if status in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):
                        validate_terminal_checkpoint(producer_checkpoint, None, meter)
                    result = terminal_certificate(
                        status, str(producer.get("reason", "producer_typed_terminal")), meter,
                        checkpoint=checkpoint_arg, producer_checkpoint=producer_checkpoint,
                        authority_identity=None)
                    if output:
                        write_sealed(output, result, meter, terminal_transport=True)
                    print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL " + status,
                          flush=True)
                    return 0
        authority = Authority(args, meter)
        authority_identity = authority.identity
        meter.authority_complete = True
        if checkpoint_arg is not None and args.resume is None:
            write_prefrontier_checkpoint(checkpoint_arg, authority, meter)
        if args.selftest:
            require(args.fixture is not None, "CHECKER_SELFTEST_FIXTURE_REQUIRED")
            fixture_path = exact_path(args.fixture, ".", Path(args.fixture).name, "CHECKER_SELFTEST_FIXTURE")
            raw = read_once(fixture_path, (fixture_path.as_posix().replace(ROOT.as_posix() + "/", ""), int(os.lstat(fixture_path).st_size), ""), meter, "checker.selftest.fixture")
            fixture = json.loads(raw.decode("ascii")); normal = positive_result(authority, meter, checkpoint_arg)
            result = selftest_certificate(fixture, authority, normal)
            if output: write_sealed(output, result, meter)
            print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_SELFTEST_PASS", flush=True); return 0
        require(producer is not None and pstatus is not None, "CHECKER_PRODUCER_REQUIRED")
        if pstatus in (UNKNOWN_INPUT, UNKNOWN_RESOURCE, HARD_STOP) or producer.get("terminal") in (UNKNOWN_INPUT, UNKNOWN_RESOURCE, HARD_STOP):
            status = producer.get("terminal") if producer.get("terminal") in (UNKNOWN_INPUT, UNKNOWN_RESOURCE, HARD_STOP) else pstatus
            if status == HARD_STOP: raise HardStop("producer:hard_stop_propagation")
            producer_checkpoint = producer.get("checkpoint")
            validate_terminal_payload(producer, status, authority, meter)
            if status in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):
                validate_terminal_checkpoint(producer_checkpoint, authority, meter)
            result = terminal_certificate(status, str(producer.get("reason", "producer_typed_terminal")), meter,
                                          checkpoint=checkpoint_arg,
                                          producer_checkpoint=producer_checkpoint,
                                          authority_identity=authority_identity)
            if output: write_sealed(output, result, meter, terminal_transport=True)
            print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL " + status, flush=True); return 0
        resume_state = restore_checkpoint(resume_arg, authority, meter) if resume_arg else None
        normal = positive_result(authority, meter, checkpoint_arg, resume_state); compare_kernel(producer, normal, authority.identity)
        if output: write_sealed(output, {**normal, "producer_receipt_digest": digest(producer), "two_way_replay": True}, meter)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL " + PASS, flush=True); return 0
    except ResourceStop as exc:
        if output: write_sealed(output, terminal_certificate(UNKNOWN_RESOURCE, str(exc), meter, checkpoint_arg,
                                                             authority_identity=authority_identity), meter,
                                terminal_transport=True)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL " + UNKNOWN_RESOURCE, flush=True); return 0
    except (Reject, UnicodeDecodeError, json.JSONDecodeError, FileNotFoundError) as exc:
        if output: write_sealed(output, terminal_certificate(UNKNOWN_INPUT, str(exc), meter, checkpoint_arg,
                                                             authority_identity=authority_identity), meter,
                                terminal_transport=True)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL " + UNKNOWN_INPUT, flush=True); return 0
    except Exception as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_STOP " +
              type(exc).__name__ + ":" + str(exc), file=sys.stderr, flush=True)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_STOP " + type(exc).__name__, flush=True); return 2


if __name__ == "__main__": raise SystemExit(main())
