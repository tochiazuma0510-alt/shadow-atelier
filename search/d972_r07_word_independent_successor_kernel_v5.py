#!/usr/bin/env python3
"""R07 A4/v5 producer.

The audited invariant is S(uv)=S(u)S(v) in the ten typed affine/Fox
semidirect products.  The producer evaluates the authenticated primitive
corpus once on a forward DAG, assembles each authority row from its literal
ancestry, and decides queries in the quotient by the complete 65-family
support-inversion oracle.  A K item is the triple (normalized row, literal
word, raw boundary ledger); the ledger is part of the invariant and is never
replaced by a digest or a Boolean.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
import stat
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-word-independent-successor-kernel/v5"
SELFTEST_SCHEMA = SCHEMA + "/selftest-fixture/v5"
PASS = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PASS"
ISO = PASS
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
    # The accepted task176 artifact also names this independent checker
    # result.  It is deliberately a physical input, not the prose copy in
    # sol/luna_reply_176_*.md; task348 restored this pinned owner physically.
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
CONTEXT_IDS = (21, 22, 23, 24, 25, 1, 27, 21, 26, 28)
CONTEXT_TYPES = ("E3", "E3", "E3", "E3", "E3", "E4", "E4", "E4", "E4", "E4")
CONTEXT_TAGS = ("E3-C21", "E3-C22", "E3-C23", "E3-C24", "E3-C25",
                "E4-C1", "E4-C27", "E4-C21", "E4-C26", "E4-C28")
EXPECTED_INVENTORY = {
    "sections": 243, "records": 26, "q0_relators": 19,
    "primitive_words": 288, "literal_primitive_letters": 114458,
    "prefix_edges": 15970, "suffix_edges": 26136,
    "stored_row_letters": 5475488,
}
CAPS = {
    "wall_seconds": 14400, "rss_bytes": 8000000000, "input_bytes": 500000000,
    "serialized_bytes": 2000000000, "canonicalization": 100000000,
    "final_write": 2, "prefix_nodes": 50000, "prefix_edges": 50000,
    "suffix_nodes": 50000, "suffix_edges": 50000, "row_assemblies": ROWS,
    "literal_comparisons": 6000000, "prefix_edge_state_products": 200000,
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
    # A typed, bounded transport budget remains available after a normal
    # semantic cap trips, so the required UNKNOWN/HARD certificate can still
    # be written with truthful physical accounting.
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


class InputStop(Reject):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float, limit: int | float,
                 state: str):
        self.phase, self.cap, self.value, self.limit, self.state = phase, cap, value, limit, state
        super().__init__(f"{phase}:{cap}:{value}>{limit}:state={state}")


class HardStop(RuntimeError):
    pass


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))




def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def jsonable(value: Any) -> Any:
    if isinstance(value, bytes):
        return {"__bytes__": value.hex()}
    if isinstance(value, tuple):
        return [jsonable(x) for x in value]
    if isinstance(value, list):
        return [jsonable(x) for x in value]
    if isinstance(value, set):
        return sorted(jsonable(x) for x in value)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    return repr(value)


def token(value: Any) -> str:
    return canon(jsonable(value)).hex()


KEYS: dict[str, Any] = {}
LIVE_STATE: dict[str, Any] = {}
# Primitive words are authenticated and reduced once during inventory
# construction.  Row replay consumes these registered tuples directly.
PRIMITIVE_WORDS: dict[tuple[int, ...], tuple[int, ...]] = {}
PRIMITIVE_INVERSES: dict[tuple[int, ...], tuple[int, ...]] = {}


def decode_token(value: str) -> Any:
    if value not in KEYS:
        KEYS[value] = _from_jsonable(json.loads(bytes.fromhex(value).decode("ascii")))
    return KEYS[value]


def _from_jsonable(value: Any) -> Any:
    if isinstance(value, dict) and set(value) == {"__bytes__"}:
        return bytes.fromhex(value["__bytes__"])
    if isinstance(value, list):
        return tuple(_from_jsonable(x) for x in value)
    if isinstance(value, dict):
        return {key: _from_jsonable(item) for key, item in value.items()}
    return value


def row_key(context: int, component: int, element: Any) -> str:
    t = token(element); KEYS[t] = element
    return f"{context}:{int(component)}:{t}"


def split_row_key(value: str) -> tuple[int, int, str]:
    a, b, c = value.split(":", 2)
    return int(a), int(b), c


def raw_key(context: int, relation: int, element: Any) -> str:
    t = token(element); KEYS[t] = element
    return f"{context}:{relation}:{t}"


def split_raw_key(value: str) -> tuple[int, int, str]:
    a, b, c = value.split(":", 2)
    return int(a), int(b), c


def add_row(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        v = (out.get(key, 0) + int(scale) * int(value)) % 3
        if v:
            out[key] = v
        else:
            out.pop(key, None)
    return out


def scale_row(row: dict[str, int], scale: int) -> dict[str, int]:
    return {key: (int(value) * int(scale)) % 3 for key, value in row.items()
            if (int(value) * int(scale)) % 3}


def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for item in word:
        value = int(item)
        require(value in (-2, -1, 1, 2), "word:letter")
        if out and out[-1] == -value:
            out.pop()
        else:
            out.append(value)
    return tuple(out)


def word_inv(word: Sequence[int]) -> tuple[int, ...]:
    return word_reduce(-int(x) for x in reversed(word))


def word_mul(*words: Sequence[int]) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for word in words:
        out = word_reduce(out + tuple(int(x) for x in word))
    return out


COUNTER_TYPES = {key: ("validation" if key == "restore_validation" else
                       "host" if key in {"wall_seconds", "input_bytes"}
                       else "peak" if key in {"rss_bytes", "checkpoint_peak_bytes"} else "semantic")
                 for key in CAPS}


class Meter:
    def __init__(self, limits: dict[str, int | float] | None = None):
        self.limits = dict(limits or CAPS)
        self.counter_types = dict(COUNTER_TYPES)
        require(set(self.limits) == set(self.counter_types), "meter:counter_registry")
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
        self.started = time.monotonic(); self.wall_base = 0.0
        self.work_units_since_sample = 0; self.sample_interval = 4096
        self.restore_mode = False; self.state_name = "AUTHORITY_UNREAD"; self.authority_complete = False
        self._sync()

    def _sync(self) -> None:
        for key, kind in self.counter_types.items():
            if kind == "semantic": self.counters[key] = self.semantic_counters.get(key, 0)
            elif kind == "host": self.counters[key] = self.host_counters.get(key, 0)
            elif kind == "peak": self.counters[key] = self.peak_counters.get(key, 0)
            else: self.counters[key] = self.restore_validation_counters.get(key, 0)

    def _value(self, key: str) -> int | float:
        kind = self.counter_types.get(key)
        require(kind is not None, "meter:unregistered_counter:" + str(key))
        if kind == "semantic": return self.semantic_counters.get(key, 0)
        if kind == "host": return self.host_counters.get(key, 0)
        if kind == "peak": return self.peak_counters.get(key, 0)
        return self.restore_validation_counters.get(key, 0)

    def state(self, name: str) -> None:
        self.state_name = str(name)

    def check(self, phase: str | None = None) -> None:
        if phase: self.state(phase)
        self.host_counters["wall_seconds"] = self.wall_base + time.monotonic() - self.started
        try:
            self.peak_counters["rss_bytes"] = max(self.peak_counters.get("rss_bytes", 0),
                int(getattr(__import__("resource"), "getrusage")(0).ru_maxrss) * 1024)
        except Exception: pass
        self._sync()
        for key, limit in self.limits.items():
            value = self._value(key)
            if value > limit:
                raise ResourceStop(self.state_name, key, value, limit, self.state_name)
        self.work_units_since_sample = 0

    def bump(self, key: str, amount: int = 1, phase: str | None = None) -> None:
        require(key in self.counter_types, "meter:unregistered_counter:" + str(key))
        kind = self.counter_types[key]
        if self.restore_mode and kind == "semantic":
            target = self.restore_validation_counters; target_key = "restore_validation"
        elif kind == "semantic": target = self.semantic_counters
        elif kind == "host": target = self.host_counters
        elif kind == "peak": target = self.peak_counters
        else: target = self.restore_validation_counters
        if not (self.restore_mode and kind == "semantic"): target_key = key
        if kind == "peak": target[target_key] = max(target.get(target_key, 0), int(amount))
        else: target[target_key] = target.get(target_key, 0) + int(amount)
        value = self._value(target_key)
        limit = self.limits["restore_validation"] if self.restore_mode and kind == "semantic" else self.limits[key]
        if value > limit:
            raise ResourceStop(phase or self.state_name, key, value, limit, self.state_name)
        self.work_units_since_sample += max(1, int(amount))
        if self.work_units_since_sample >= self.sample_interval:
            self.check(phase)

    def validation_bump(self, amount: int = 1, phase: str = "checkpoint.restore") -> None:
        self.restore_validation_counters["restore_validation"] = (
            self.restore_validation_counters.get("restore_validation", 0) + int(amount))
        value = self.restore_validation_counters["restore_validation"]
        require(value <= self.limits["restore_validation"], "meter:restore_validation_cap")
        self.work_units_since_sample += max(1, int(amount))
        if self.work_units_since_sample >= self.sample_interval:
            self.check(phase)

    def terminal_bump(self, key: str, amount: int = 1, phase: str = "terminal.transport") -> None:
        """Charge the reserved terminal channel without semantic rerouting."""
        require(key in {"terminal_canonicalization", "terminal_checkpoint_bytes",
                        "terminal_serialized_bytes",
                        "terminal_final_write"}, "meter:terminal_counter")
        value = self.semantic_counters.get(key, 0) + int(amount)
        require(value <= self.limits[key], "meter:terminal_transport_cap:" + key)
        self.semantic_counters[key] = value
        self.completed_counters[key] = value
        self.counters[key] = value

    def reserve(self, key: str, amount: int, phase: str) -> None:
        require(key in self.counter_types, "meter:unregistered_counter:" + str(key))
        kind = self.counter_types[key]
        current = self._value(key)
        if self.restore_mode and kind == "semantic":
            current = self.restore_validation_counters.get("restore_validation", 0)
        limit = self.limits["restore_validation"] if self.restore_mode and kind == "semantic" else self.limits[key]
        if current + int(amount) > limit:
            raise ResourceStop(phase, key, current + int(amount), limit, self.state_name)

    def install_completed(self, saved: dict[str, int | float], saved_validation: dict[str, int | float],
                          saved_peak: dict[str, int | float] | None = None) -> None:
        require(set(saved) == set(self.semantic_counters), "meter:saved_semantic_registry")
        require(set(saved_validation) <= {key for key, kind in self.counter_types.items() if kind == "validation"},
                "meter:saved_validation_registry")
        require(all(isinstance(value, (int, float)) and value >= 0 for value in saved.values()),
                "meter:saved_semantic_values")
        self.semantic_counters = dict(saved); self.completed_counters = dict(saved)
        self.pending_completed_counters = None; self.pending_saved_validation = None; self.pending_saved_peak = None
        self.restore_validation_counters = dict(saved_validation)
        if saved_peak is not None:
            self.peak_counters = {key: max(self.peak_counters.get(key, 0), value)
                                  for key, value in saved_peak.items()}
        # H1 is measured from process invocation.  Do not restart the clock
        # after validation: that would grant the continuation a second wall
        # budget.  The saved H0 is retained separately by restore_checkpoint.
        self.wall_base = 0.0; self.restore_mode = False
        self._sync(); self.check("checkpoint.continuation")

    def public(self, strict: bool = True) -> dict[str, Any]:
        if strict: self.check()
        else: self._sync()
        return {"limits": dict(self.limits), "counter_registry": dict(self.counter_types),
                "counters": dict(self.counters), "semantic_counters": dict(self.semantic_counters),
                "completed_counters": dict(self.completed_counters),
                "restore_validation_counters": dict(self.restore_validation_counters),
                "host_counters": dict(self.host_counters), "host_history": list(self.host_history),
                "peak_counters": dict(self.peak_counters),
                "last_replayable_state": self.state_name, "single_process": True,
                "no_retry_or_pool": True, "object_caps": dict(OBJECT_CAPS)}





def _windows_guard(path: Path) -> None:
    """Open with FILE_FLAG_OPEN_REPARSE_POINT and inspect handle identity."""
    if os.name != "nt":
        return
    try:
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        create = kernel.CreateFileW
        create.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
                           ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32,
                           ctypes.c_void_p]
        create.restype = ctypes.c_void_p
        handle = create(str(path), 0x80000000, 0x00000001 | 0x00000002 | 0x00000004,
                        None, 3, 0x00200000 | 0x00000080, None)
        if handle in (None, ctypes.c_void_p(-1).value):
            raise InputStop("path:windows_no_follow_unavailable")
        kernel.CloseHandle(handle)
    except InputStop:
        raise
    except Exception as exc:
        raise InputStop("path:windows_no_follow_unavailable") from exc


def exact_path(text: str, area: str, basename: str, label: str,
               must_exist: bool = True) -> Path:
    raw = str(text).replace("\\", "/")
    p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts,
            label + ":lexical_path")
    # A dot area means that the supplied path itself is the expected rooted
    # path (used for pinned inputs living below search/, crosscheck/, or ci/).
    # Named areas retain the stricter basename binding used by authority files.
    try:
        expected = ((ROOT / p) if area == "." else (ROOT / area / basename)).resolve(strict=must_exist)
        actual = (ROOT / p).resolve(strict=must_exist)
    except (FileNotFoundError, OSError) as exc:
        raise InputStop(label + ":resolved_path_missing") from exc
    require(actual == expected and actual.name == basename, label + ":resolved_path")
    cursor = ROOT
    for part in p.parts:
        cursor /= part
        try:
            st = os.lstat(cursor)
        except OSError as exc:
            raise InputStop(label + ":identity_unavailable") from exc
        if stat.S_ISLNK(st.st_mode) or (os.name == "nt" and
                                        bool(getattr(st, "st_file_attributes", 0) & 0x400)):
            raise InputStop(label + ":reparse_or_symlink")
    _windows_guard(actual)
    return actual


def output_path(text: str, area: str, label: str) -> Path:
    raw = str(text).replace("\\", "/")
    p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts,
            label + ":lexical_path")
    out = (ROOT / p).resolve(strict=False)
    require(out.parent == (ROOT / area).resolve(strict=True), label + ":containment")
    cursor = ROOT
    for part in p.parts[:-1]:
        cursor /= part
        try:
            info = os.lstat(cursor)
        except OSError as exc:
            raise InputStop(label + ":parent_identity_unavailable") from exc
        require(not stat.S_ISLNK(info.st_mode) and not
                (os.name == "nt" and bool(getattr(info, "st_file_attributes", 0) & 0x400)),
                label + ":parent_reparse_or_symlink")
    return out


def checkpoint_input(path: Path, label: str) -> Path:
    """Revalidate a checkpoint path, accepting only the resolved ci/out owner."""
    try:
        relative = path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()
    except ValueError as exc:
        raise InputStop(label + ":outside_workspace") from exc
    return exact_path(relative, "ci/out", path.name, label)


def read_once(path: Path, expected: tuple[str, int, str], meter: Meter,
              label: str, terminal_transport: bool = False) -> bytes:
    relative, size, expected_sha = expected
    require(path.as_posix().replace(ROOT.as_posix() + "/", "") == relative,
            label + ":relative")
    # The Windows branch must read and recheck the very same no-follow handle.
    # This implementation only has a separate probe handle; fail closed as a
    # typed input stop instead of pretending that probe+os.open is equivalent.
    if os.name == "nt":
        raise InputStop(label + ":windows_same_handle_identity_unavailable")
    _windows_guard(path)
    try:
        before = os.lstat(path)
        if stat.S_ISLNK(before.st_mode):
            raise InputStop(label + ":symlink")
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
            raise InputStop(label + ":no_follow_unavailable")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | no_follow
        fd = os.open(str(path), flags)
        try:
            opened = os.fstat(fd)
            opened_identity = (opened.st_dev, opened.st_ino, opened.st_size,
                               getattr(opened, "st_mtime_ns", int(opened.st_mtime * 1000000000)))
            if opened_identity != before_identity or getattr(opened, "st_nlink", 1) != 1:
                raise InputStop(label + ":identity_changed_before_read")
            buffer = bytearray(int(opened.st_size))
            offset = 0; remaining = int(opened.st_size)
            while remaining:
                part = os.read(fd, min(1024 * 1024, remaining))
                if not part:
                    raise InputStop(label + ":short_read")
                buffer[offset:offset + len(part)] = part
                offset += len(part); remaining -= len(part)
            raw = buffer
            after = os.fstat(fd)
        finally:
            os.close(fd)
        after_identity = (after.st_dev, after.st_ino, after.st_size,
                          getattr(after, "st_mtime_ns", int(after.st_mtime * 1000000000)))
        path_after = os.lstat(path)
        path_after_identity = (path_after.st_dev, path_after.st_ino, path_after.st_size,
                               getattr(path_after, "st_mtime_ns", int(path_after.st_mtime * 1000000000)))
        if (after_identity != before_identity or path_after_identity != after_identity or
                getattr(path_after, "st_nlink", 1) != 1 or len(raw) != size or
                (expected_sha and sha(raw) != expected_sha)):
            raise InputStop(label + ":bytes_sha256")
        _windows_guard(path)
        return raw
    except InputStop:
        raise
    except (OSError, ValueError) as exc:
        raise InputStop(label + ":no_follow_identity") from exc


def load_json_raw(path: Path, expected: tuple[str, int, str], meter: Meter,
                  label: str) -> tuple[bytes, dict[str, Any]]:
    raw = read_once(path, expected, meter, label)
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputStop(label + ":canonical_ascii_json") from exc
    require(isinstance(value, dict), label + ":object")
    return raw, value


def element_blob(value: Any) -> bytes:
    require(isinstance(value, tuple) and len(value) == 2 and
            isinstance(value[0], bytes) and isinstance(value[1], bytes), "EKey:blob")
    return value[0] + value[1]


class AuthorityAdapter:
    """One-pass physical adapter; all semantic owners are recomputed here."""
    def __init__(self, args: argparse.Namespace, meter: Meter):
        self.meter = meter
        self.paths = {key: exact_path(getattr(args, "task198_" + key), "ci/in",
                                      basename, "TASK198_" + key.upper())
                       for key, basename in AUTH.items()}
        self.raw: dict[str, bytes] = {}; self.values: dict[str, dict[str, Any]] = {}
        for key in ("manifest", "verdict", "receipt"):
            raw, value = load_json_raw(self.paths[key],
                                       self._authority_pin(key), meter, "authority." + key)
            self.raw[key], self.values[key] = raw, value
        for key in ("producer", "checker"):
            raw = read_once(self.paths[key], self._authority_pin(key), meter,
                            "authority." + key)
            require(raw.endswith(b"\n") and raw.decode("ascii"),
                    "authority." + key + ":attestation")
            self.raw[key] = raw
        self.task176_raw, self.task176 = load_json_raw(
            exact_path("ci/in/d972_r07_all_seven_extension_section_census_v1.json", "ci/in",
                       Path(TASK176["receipt"][0]).name, "TASK176_RECEIPT"),
            TASK176["receipt"], meter, "task176.receipt")
        self.task176_manifest_raw = read_once(
            exact_path("ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json",
                       "ci/in", Path(TASK176["manifest"][0]).name, "TASK176_MANIFEST"),
            TASK176["manifest"], meter, "task176.manifest")
        self.task176_sources: dict[str, bytes] = {}
        for side in ("producer", "checker"):
            expected = TASK176[side]
            source_path = exact_path(expected[0], ".", Path(expected[0]).name,
                                     "TASK176_SOURCE_" + side.upper())
            self.task176_sources[side] = read_once(source_path, expected, meter,
                                                   "task176.source." + side)
        checker_result_path = exact_path(TASK176["checker_result"][0], ".",
                                         Path(TASK176["checker_result"][0]).name,
                                         "TASK176_CHECKER_RESULT")
        self.task176_checker_result_raw, self.task176_checker_result = load_json_raw(
            checker_result_path, TASK176["checker_result"], meter, "task176.checker_result")
        recovery_v1_pin = TASK176["recovery_manifest_v1"]
        recovery_v1_path = exact_path(recovery_v1_pin[0], ".", Path(recovery_v1_pin[0]).name,
                                      "TASK176_RECOVERY_MANIFEST_V1")
        self.task176_recovery_v1_raw, self.task176_recovery_v1 = load_json_raw(
            recovery_v1_path, recovery_v1_pin, meter, "task176.recovery_manifest_v1")
        recovery_pin = TASK176["recovery_manifest"]
        recovery_path = exact_path(recovery_pin[0], ".", Path(recovery_pin[0]).name,
                                   "TASK176_RECOVERY_MANIFEST")
        self.task176_recovery_raw, self.task176_recovery = load_json_raw(
            recovery_path, recovery_pin, meter, "task176.recovery_manifest")
        self.validate()
        self.identity = {
            "task198": {key: {"path": AUTH[key], "bytes": len(raw), "sha256": sha(raw)}
                        for key, raw in self.raw.items()},
            "task176": {key: {"path": value[0], "bytes": value[1], "sha256": value[2]}
                        for key, value in TASK176.items()},
            "task176_source_identities": {
                key: {"path": TASK176[key][0], "bytes": len(raw), "sha256": sha(raw)}
                for key, raw in self.task176_sources.items()},
            "receipt_sha256": RECEIPT_SHA, "receipt_bytes": RECEIPT_BYTES,
            "manifest_sha256": MANIFEST_SHA,
        }

    def _authority_pin(self, key: str) -> tuple[str, int, str]:
        if key == "receipt": return ("ci/in/" + AUTH[key], RECEIPT_BYTES, RECEIPT_SHA)
        if key == "manifest": return ("ci/in/" + AUTH[key], 2722, MANIFEST_SHA)
        if key == "verdict": return ("ci/in/" + AUTH[key], 150, VERDICT_SHA)
        return ("ci/in/" + AUTH[key], 81 if key == "producer" else 95,
                "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"
                if key == "producer" else
                "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e")

    @property
    def receipt(self) -> dict[str, Any]:
        return self.values["receipt"]

    @property
    def rows(self) -> list[dict[str, Any]]:
        return self.receipt["Delta0"]["presentation"]["rows"]

    def validate(self) -> None:
        receipt, manifest, verdict = self.values["receipt"], self.values["manifest"], self.values["verdict"]
        body = dict(manifest); claimed = body.pop("manifest_self_digest_sha256", None)
        require(manifest.get("schema") == MANIFEST_SCHEMA and manifest.get("accepted") is True and
                manifest.get("independent") is True and manifest.get("synthetic") is False and
                claimed == "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684" and
                claimed == digest(body), "authority:manifest_seal")
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
            item = manifest.get("task198_source_identities", {}).get(side, {})
            require(item.get("path") == expected[0] and item.get("bytes") == expected[1] and
                    item.get("sha256") == expected[2], "authority:manifest_source:" + side)
            physical = read_once(exact_path(expected[0], ".", Path(expected[0]).name,
                                            "TASK198_PHYSICAL_" + side), expected, self.meter,
                                 "authority.physical." + side)
            require(sha(physical) == expected[2], "authority:physical_source:" + side)
        for side in ("producer", "checker"):
            item = manifest.get(side, {}); att = manifest.get(side + "_attestation", {})
            require(item.get("run") == "33155710862" and
                    item.get("head") == "bed1d5e6b41477b8799f2a33a24e46f7800f9510" and
                    item.get("artifact_id") == "9686477718" and
                    item.get("zip_sha256") ==
                    "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854" and
                    att.get("basename") == AUTH[side] and att.get("bytes") == len(self.raw[side]) and
                    att.get("sha256") == sha(self.raw[side]), "authority:run_attestation:" + side)
        presentation = receipt.get("Delta0", {}).get("presentation")
        require(isinstance(presentation, dict) and presentation.get("row_count") == ROWS and
                presentation.get("layer_counts") == LAYERS and len(presentation.get("rows", [])) == ROWS and
                presentation.get("resume_cursor") == ROWS and presentation.get("normal_generation") is True,
                "authority:presentation_header")
        local = {name: [] for name in LAYERS}; global_owner = []
        for row in self.rows:
            self.meter.bump("literal_comparisons", 1, "authority.row_parse")
            require(row.get("layer") in LAYERS and isinstance(row.get("ordinal"), int),
                    "authority:row_shape")
            literal = row.get("word")
            require(isinstance(literal, list) and
                    all(type(letter) is int and letter in (-2, -1, 1, 2) for letter in literal),
                    "authority:row_word_shape")
            require(tuple(word_reduce(literal)) == tuple(literal), "authority:row_word_reduced")
            local[row["layer"]].append(row["ordinal"])
            global_owner.append((row["layer"], row["ordinal"]))
        for layer, count in LAYERS.items():
            require(local[layer] == list(range(1, count + 1)), "authority:ordinal:" + layer)
        expected_global = [(layer, ordinal) for layer, count in LAYERS.items()
                           for ordinal in range(1, count + 1)]
        require(global_owner == expected_global, "authority:global_layer_sequence")
        # One literal row traversal feeds the complete digest and all seven
        # chunk digests.  Re-slicing the 6,441-row list here would charge and
        # canonicalize the authority a second time.
        row_hash = hashlib.sha256(); row_hash.update(b"[")
        chunk_hash = hashlib.sha256(); chunk_hash.update(b"[")
        chunk_items = 0
        chunks = presentation.get("chunks", []); require(len(chunks) == 7, "authority:seven_chunks")
        by_end = {int(item.get("end")): item for item in chunks}
        require(set(by_end) == {1024, 2048, 3072, 4096, 5120, 6144, 6441},
                "authority:chunk_boundaries")
        for ordinal, literal_row in enumerate(self.rows, 1):
            encoded = canon(literal_row)
            if ordinal > 1: row_hash.update(b",")
            if chunk_items: chunk_hash.update(b",")
            row_hash.update(encoded); chunk_hash.update(encoded); chunk_items += 1
            if ordinal in by_end:
                item = by_end[ordinal]
                chunk_hash.update(b"]")
                require(chunk_hash.hexdigest() == item.get("sha256") and
                        item.get("sealed") is True and item.get("prefix_complete") is True,
                        "authority:chunk_slice_recomputed")
                chunk_hash = hashlib.sha256(); chunk_hash.update(b"["); chunk_items = 0
        row_hash.update(b"]")
        require(row_hash.hexdigest() == presentation.get("rows_sha256"),
                "authority:rows_digest_recomputed")
        proof = presentation.get("normal_generation_proof", {})
        expected_proof = {
            "Gamma_cayley_edge_count": 6318, "Gamma_cayley_state_count": 243,
            "Q0_defect_normal_closure_order": 243, "Q0_lift_count": 19,
            "all_record_generator_closure_order": 243, "marked_action_loop_count": 104,
            "selected_gamma_records": [1, 3, 6, 9],
            "presentation_quotient_order_upper_bound": 357128352,
            "surjective_marked_image_order": 357128352,
            "upper_bound_equals_image_order": True,
        }
        for key, value in expected_proof.items():
            require(proof.get(key) == value, "authority:normal_proof:" + key)
        qproof = proof.get("Q0_order_proof", {})
        for key, value in {"G9_abstract_presentation_order": 2916,
                           "G9_direct_image_order": 2916, "P_abstract_presentation_order": 504,
                           "P_direct_image_order": 504, "Q0_marked_image_order": 1469664,
                           "Q0_presentation_order_upper_bound": 1469664,
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
                bridge.get("occurrence_ledger_sha256") == digest(ledger) and len(ledger) == 11 and
                bridge.get("typed_coordinate_ledger_sha256") == digest(self.task176.get("coordinates")),
                "authority:bridge_literal_ledger")
        required_ledger_fields = ("block", "block_index", "block_slot", "context_id", "factor_sign",
                                  "fox_prefix_occurrences", "occurrence", "ordinal", "orientation",
                                  "role", "ten_index", "type")
        for item in ledger:
            require(all(key in item for key in required_ledger_fields), "authority:bridge_owner_fields")
        evaluator = receipt.get("evaluator", {}); canaries = evaluator.get("canaries", {})
        require(evaluator.get("schema") == "d972-r07-v188-roof-consumer-action-abi/v1" and
                evaluator.get("coordinate_widths") == [40, 40, 40, 40, 40, 154, 154, 154, 154, 154] and
                evaluator.get("relator_rows_sha256") == presentation.get("rows_sha256"),
                "authority:evaluator_abi")
        require(set(canaries) == {"nonsplit_y_y_section_cocycle", "source_2_2", "x",
                                  "x_action_y", "x_inverse", "xy", "xy_section_cocycle", "y"},
                "authority:actual_canary_roster")
        require(canaries.get("nonsplit_y_y_section_cocycle") is None,
                "authority:nonsplit_canary")
        for name in ("x", "x_action_y", "x_inverse", "xy", "xy_section_cocycle", "y", "source_2_2"):
            require(isinstance(canaries.get(name), dict) and isinstance(canaries[name].get("value"), list),
                    "authority:canary_value:" + name)
        require(receipt.get("Ihara_witness") is False and receipt.get("cofinal_lift") is False and
                receipt.get("fake") is False and receipt.get("direct_Delta_states_enumerated") == 0 and
                receipt.get("D_all", {}).get("materialized") is False, "authority:forbidden_flags")
        require(self.task176.get("schema") == "d972-r07-all-seven-extension-section-census/v1" and
                self.task176.get("status") == "COMPLETE" and
                self.task176.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
                self.task176.get("boundaries", {}).get("fake") is False and
                self.task176.get("boundaries", {}).get("Ihara_witness") is False,
                "task176:accepted_receipt")
        manifest176 = json.loads(self.task176_manifest_raw.decode("ascii"))
        require(manifest176 == {"artifact_id": "9635036013", "head": "0533e42019c9f67f6cec3d1566152db17b903836",
                                "member": "d972_r07_all_seven_extension_section_census_v1.json",
                                "member_bytes": 13649089, "member_sha256": TASK176["receipt"][2],
                                "run": "33044121344",
                                "zip_sha256": "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912"},
                "task176:manifest_owner")
        result = self.task176_checker_result
        result_body = dict(result); result_claim = result_body.pop("self_digest_sha256", None)
        require(result.get("schema") == "d972-r07-all-seven-extension-section-census-check/v1" and
                result.get("grade") == "CROSS_CHECKED" and
                result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
                result.get("receipt_terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
                result.get("receipt_bytes") == TASK176["receipt"][1] and
                result.get("receipt_sha256") == TASK176["receipt"][2] and
                result.get("producer_sha256") == TASK176["producer"][2] and
                result_claim == "e9d42ea064e7caaa9a333f7e2a8aec42f709bf1565e9fc9a8950ef92e18ce473" and
                result_claim == digest(result_body), "task176:physical_checker_result")
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


def load_pinned_module(path_tuple: tuple[str, int, str], name: str, meter: Meter) -> Any:
    path, size, expected = path_tuple
    raw = read_once(exact_path(path, ".", Path(path).name, "PINNED_MODULE"), path_tuple,
                    meter, "pinned." + name)
    # Execute the bytes already authenticated by read_once; this avoids a
    # second pathname open and keeps the source identity tied to one handle.
    module = type(sys)(name); module.__file__ = str(ROOT / path)
    sys.modules[name] = module
    exec(compile(bytes(raw), str(ROOT / path), "exec"), module.__dict__)
    return module


def load_pinned_json(path_tuple: tuple[str, int, str], meter: Meter) -> dict[str, Any]:
    path, _, _ = path_tuple
    _, value = load_json_raw(exact_path(path, ".", Path(path).name, "PINNED_JSON"),
                             path_tuple, meter, "pinned.q3")
    return value


class AffineState:
    def __init__(self, quotient: Any, a: Any, u: dict[tuple[int, Any], int]):
        self.q, self.a, self.u = quotient, a, {key: int(value) % 3 for key, value in u.items()
                                               if int(value) % 3}

    def mul(self, other: "AffineState") -> "AffineState":
        require(self.q is other.q, "affine:quotient_identity")
        moved = {(component, self.q.mul(self.a, element)): coefficient
                 for (component, element), coefficient in other.u.items()}
        return AffineState(self.q, self.q.mul(self.a, other.a), add_local(self.u, moved))

    def inv(self) -> "AffineState":
        ai = self.q.inverse(self.a)
        return AffineState(self.q, ai, translate_local(self.u, ai, self.q, -1))

    def identity_roof(self) -> bool:
        return self.a == self.q.identity


def add_local(left: dict[tuple[int, Any], int], right: dict[tuple[int, Any], int],
              scale: int = 1) -> dict[tuple[int, Any], int]:
    out = dict(left)
    for key, value in right.items():
        coefficient = (out.get(key, 0) + int(scale) * int(value)) % 3
        if coefficient: out[key] = coefficient
        else: out.pop(key, None)
    return out


def translate_local(vector: dict[tuple[int, Any], int], translation: Any, quotient: Any,
                    scale: int = 1) -> dict[tuple[int, Any], int]:
    out: dict[tuple[int, Any], int] = {}
    for (component, element), coefficient in vector.items():
        key = (component, quotient.mul(translation, element))
        out[key] = (out.get(key, 0) + int(scale) * int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


class Runtime:
    """Pinned public arithmetic only; no old producer/checker helper is imported."""
    def __init__(self, authority: AuthorityAdapter, meter: Meter):
        self.meter = meter; self.old = load_pinned_module(E4_SOURCE, "r07_v5_frozen_e4", meter)
        self.q3 = load_pinned_json(Q3_SOURCE, meter)
        self.e3, self.e4, _ = self.old.reconstruct_quotients(self.q3)
        x, y = [1], [3]
        z = self.old.inv_word(self.old.pp_words([x, y])); u = self.old.inv_word(self.old.pp_words([y, x]))
        pairs = [(x, y), (x, z), (y, z), (u, x), (u, y), ([4], [6]),
                 (self.old.pp_words([[1], [2]]), self.old.pp_words([[5], [6]])),
                 ([1], [4]), (self.old.pp_words([[2], [4]]), [6]),
                 ([1], self.old.pp_words([[4], [5]]))]
        self.contexts = [{"index": i, "type": CONTEXT_TYPES[i], "id": CONTEXT_IDS[i],
                          "tag": CONTEXT_TAGS[i], "left": list(pair[0]), "right": list(pair[1])}
                         for i, pair in enumerate(pairs)]
        self.actors: dict[tuple[int, int], AffineState] = {}
        for index in range(10):
            for letter in (1, -1, 2, -2):
                self.actors[index, letter] = self.eval((letter,), index)
                meter.bump("typed_context_products", 1, "actor_cache")
            require(self.actors[index, -1].a == self.actors[index, 1].inv().a and
                    self.actors[index, -1].u == self.actors[index, 1].inv().u and
                    self.actors[index, -2].a == self.actors[index, 2].inv().a and
                    self.actors[index, -2].u == self.actors[index, 2].inv().u,
                    "actor:direct_inverse_word")
        self.check_canaries(authority.receipt)

    def quotient(self, index: int) -> Any:
        return self.e3 if self.contexts[index]["type"] == "E3" else self.e4

    def identity(self, index: int) -> AffineState:
        q = self.quotient(index); return AffineState(q, q.identity, {})

    def eval(self, word: Sequence[int], index: int, charge_direct: bool = True) -> AffineState:
        if charge_direct:
            self.meter.reserve("direct_replays", 1, "direct_replay")
            self.meter.bump("direct_replays", 1, "direct_replay")
        c = self.contexts[index]; q = self.quotient(index)
        substituted = self.old.f2_substitute(tuple(word), c["left"], c["right"])
        gradient, roof = self.old.fox_gradient_without_sections(substituted, q)
        self.meter.bump("quotient_reductions", max(1, len(substituted)), "direct_affine")
        return AffineState(q, roof, {(int(k[0]), k[1]): int(v) % 3 for k, v in gradient.items()
                                     if int(v) % 3})

    def eval_pb(self, word: Sequence[int], index: int) -> AffineState:
        q = self.quotient(index); gradient, roof = self.old.fox_gradient_without_sections(tuple(word), q)
        self.meter.bump("quotient_reductions", max(1, len(word)), "base_affine")
        return AffineState(q, roof, {(int(k[0]), k[1]): int(v) % 3 for k, v in gradient.items()
                                     if int(v) % 3})

    def state_roof_blob(self, state: AffineState) -> str:
        return element_blob(state.a).hex()

    def row_from_states(self, states: Sequence[AffineState]) -> dict[str, int]:
        out: dict[str, int] = {}
        for index, state in enumerate(states):
            require(state.identity_roof(), "row:nontrivial_roof")
            out = add_row(out, {row_key(index, component, element): coefficient
                                for (component, element), coefficient in state.u.items()})
        return out

    def states_direct(self, word: Sequence[int]) -> list[AffineState]:
        # One direct-replay unit is one literal word in one typed context.
        # Reserve and charge the complete ten-context batch before evaluating.
        self.meter.reserve("direct_replays", 10, "direct_replay")
        self.meter.bump("direct_replays", 10, "direct_replay")
        states = [self.eval(word, index, charge_direct=False) for index in range(10)]
        return states

    def check_canaries(self, receipt: dict[str, Any]) -> None:
        canaries = receipt["evaluator"]["canaries"]
        expected_names = {"nonsplit_y_y_section_cocycle", "source_2_2", "x", "x_action_y",
                          "x_inverse", "xy", "xy_section_cocycle", "y"}
        require(set(canaries) == expected_names, "evaluator:canary_keyset")
        for name, letter in (("x", 1), ("y", 2), ("x_inverse", -1)):
            expected = [self.state_roof_blob(self.actors[index, letter]) for index in range(10)]
            require(canaries[name]["value"] == expected, "evaluator:canary:" + name)
        expected_xy = [self.state_roof_blob(self.actors[index, 1].mul(self.actors[index, 2]))
                       for index in range(10)]
        require(canaries["xy"]["value"] == expected_xy, "evaluator:canary:xy")
        expected_action = [self.state_roof_blob(self.actors[index, 1].mul(
            self.actors[index, 2]).mul(self.actors[index, -1])) for index in range(10)]
        require(canaries["x_action_y"]["value"] == expected_action, "evaluator:canary:action")
        cocycle = [self.state_roof_blob(self.eval(word_mul([1], [2], word_inv([1, 2])), index))
                   for index in range(10)]
        require(canaries["xy_section_cocycle"]["value"] == cocycle,
                "evaluator:canary:section_cocycle")
        source_word = canaries["source_2_2"].get("source_word")
        require(isinstance(source_word, list), "evaluator:canary:source_word")
        require(canaries["source_2_2"]["value"] ==
                [self.state_roof_blob(self.eval(source_word, index)) for index in range(10)],
                "evaluator:canary:source_2_2")
        widths = receipt["evaluator"]["coordinate_widths"]
        for name in ("x", "y", "x_inverse", "xy", "x_action_y", "xy_section_cocycle", "source_2_2"):
            for index, value in enumerate(canaries[name]["value"]):
                require(len(bytes.fromhex(value)) == widths[index], "evaluator:canary_width")


def local_to_row(local: dict[tuple[int, Any], int], index: int) -> dict[str, int]:
    return {row_key(index, component, element): int(value) % 3
            for (component, element), value in local.items() if int(value) % 3}


BRIDGE_TEN_TO_ELEVEN = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
BRIDGE_DELETE_DUPLICATE = (0, 1, 2, 3, 5, 6, 7, 8, 9, 10)
BRIDGE_REINSERT = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 0, 4), (5,), (6,), (7,), (8,), (9,))
# This is an independent literal reconstruction of the task198 owner.  It is
# deliberately kept as scalar fields rather than copied trace objects: every
# row below is checked against the authenticated ledger before its live
# ten-coordinate spelling is selected.
BRIDGE_OWNER_LAYOUT = (
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


def bridge_trace_from_states(authority: AuthorityAdapter, states: Sequence[AffineState],
                             word: Sequence[int], row: dict[str, Any], meter: Meter) -> dict[str, Any]:
    """Replay the ten/eleven/seven public bridge in the row's live pass."""
    require(len(states) == 10, "bridge:ten_arity")
    owner = authority.receipt.get("bridge", {}).get("occurrence_ledger", [])
    require(len(owner) == len(BRIDGE_OWNER_LAYOUT) == 11, "bridge:occurrence_owner_count")
    # Reconstruct all non-value owner fields independently.  In particular,
    # the spelling and prefix lists are not accepted merely because the
    # receipt's aggregate digest is sealed.
    for index, item in enumerate(owner):
        expected = BRIDGE_OWNER_LAYOUT[index]
        actual = (item.get("block"), int(item.get("block_index")), int(item.get("block_slot")),
                  item.get("occurrence"), item.get("type"), int(item.get("ten_index")),
                  int(item.get("context_id")), item.get("role"), int(item.get("factor_sign")),
                  item.get("orientation"), tuple(item.get("fox_prefix_occurrences", ())))
        require(int(item.get("ordinal")) == index + 1 and actual == expected,
                "bridge:literal_occurrence_owner")
        require(expected[5] == BRIDGE_TEN_TO_ELEVEN[index], "bridge:owner_insertion_binding")
        coordinate = authority.task176.get("coordinates", [])[expected[5]]
        require((item.get("type"), int(item.get("context_id")), item.get("role")) ==
                (coordinate.get("type"), int(coordinate.get("context_id")), coordinate.get("role")),
                "bridge:typed_coordinate_owner")
    ten_blobs = [element_blob(state.a).hex() for state in states]
    eleven_blobs = [ten_blobs[index] for index in BRIDGE_TEN_TO_ELEVEN]
    seven_blobs = [[eleven_blobs[index] for index in block] for block in BRIDGE_SEVEN_BLOCKS]
    deleted_blobs = [eleven_blobs[index] for index in BRIDGE_DELETE_DUPLICATE]
    reinserted_blobs = [deleted_blobs[index] for index in BRIDGE_REINSERT]
    flattened_blobs = [blob for block in seven_blobs for blob in block]
    require(eleven_blobs[0] == eleven_blobs[4] and deleted_blobs == ten_blobs and
            reinserted_blobs == eleven_blobs and flattened_blobs == eleven_blobs,
            "bridge:inverse_replay")
    occurrences = []
    for item in owner:
        ordinal = int(item["ordinal"]); ten_index = int(item["ten_index"])
        require(1 <= ordinal <= 11 and ten_index == BRIDGE_TEN_TO_ELEVEN[ordinal - 1],
                "bridge:occurrence_index")
        occurrences.append({"block": item["block"], "block_index": int(item["block_index"]),
                            "block_slot": int(item["block_slot"]), "context_id": int(item["context_id"]),
                            "factor_sign": int(item["factor_sign"]),
                            "fox_prefix_occurrences": list(item["fox_prefix_occurrences"]),
                            "occurrence": item["occurrence"], "ordinal": ordinal,
                            "orientation": item["orientation"], "role": item["role"],
                            "ten_index": ten_index, "type": item["type"],
                            "ten_spelling": ten_blobs[ten_index],
                            "eleven_spelling": eleven_blobs[ordinal - 1]})
        meter.bump("bridge_occurrences", 1, "bridge.literal_occurrence")
    meter.bump("bridge_rows", 1, "bridge.row_replay")
    core = {"label": f"relator:{row['layer']}:{row['ordinal']}", "word": list(word),
            "word_sha256": digest(list(word)), "ten_sha256": digest(ten_blobs),
            "eleven_sha256": digest(eleven_blobs), "seven_sha256": digest(seven_blobs),
            "occurrence_values_sha256": digest([eleven_blobs[item["ordinal"] - 1] for item in owner]),
            "left_inverse": deleted_blobs == ten_blobs, "image_inverse": reinserted_blobs == eleven_blobs,
            "regroup_inverse": flattened_blobs == eleven_blobs}
    core["occurrence_owner_sha256"] = digest(occurrences)
    core["bridge_trace_digest"] = digest({key: core[key] for key in
                                           ("label", "word", "word_sha256", "ten_sha256",
                                            "eleven_sha256", "seven_sha256",
                                            "occurrence_values_sha256", "left_inverse",
                                            "image_inverse", "regroup_inverse")})
    return core


class ForwardDAG:
    """Each nonroot edge is evaluated once in all ten typed contexts."""
    def __init__(self, runtime: Runtime, meter: Meter):
        self.runtime, self.meter = runtime, meter
        self.nodes = [{"parent": None, "letter": None, "edges": {}, "length": 0,
                       "states": [runtime.identity(i) for i in range(10)]}]
        self.terminals: dict[tuple[int, ...], int] = {}
        # Inverse primitive words are not extra trie edges.  Their ten states
        # are derived once from the authenticated terminal for the inverse
        # literal and then reused by every row assembly.
        self.inverse_states: dict[tuple[int, ...], list[AffineState]] = {}

    def add(self, word: Sequence[int]) -> int:
        normalized = tuple(word_reduce(word))
        if normalized in self.terminals:
            return self.terminals[normalized]
        node = 0
        for letter in normalized:
            edge = int(letter); child = self.nodes[node]["edges"].get(edge)
            if child is None:
                self.meter.reserve("prefix_nodes", 1, "forward_dag_edge")
                self.meter.reserve("prefix_edges", 1, "forward_dag_edge")
                self.meter.reserve("prefix_edge_state_products", 10, "forward_dag_edge")
                parent_states = self.nodes[node]["states"]
                states = [parent_states[i].mul(self.runtime.actors[i, edge]) for i in range(10)]
                child = len(self.nodes)
                self.nodes[node]["edges"][edge] = child
                self.nodes.append({"parent": node, "letter": edge, "edges": {},
                                   "length": self.nodes[node]["length"] + 1, "states": states})
                self.meter.bump("prefix_nodes", 1, "forward_dag_edge")
                self.meter.bump("prefix_edges", 1, "forward_dag_edge")
                self.meter.bump("prefix_edge_state_products", 10, "forward_dag_edge")
            node = child
        self.terminals[normalized] = node
        return node

    def state(self, word: Sequence[int], index: int) -> AffineState:
        # replay_ancestry supplies canonical reduced tuples; direct lookup is
        # intentional so each primitive is reduced exactly once at assembly.
        normalized = tuple(int(letter) for letter in word)
        require(all(letter in (-2, -1, 1, 2) for letter in normalized),
                "forward_dag:letter")
        if normalized in self.terminals:
            return self.nodes[self.terminals[normalized]]["states"][index]
        cached = self.inverse_states.get(normalized)
        if cached is None:
            inverse_literal = tuple(word_inv(normalized))
            base = self.terminals.get(inverse_literal)
            require(base is not None, "forward_dag:unregistered_primitive")
            self.meter.reserve("typed_context_products", 10, "forward_dag.inverse_primitive")
            cached = [state.inv() for state in self.nodes[base]["states"]]
            original = self.nodes[base]["states"]
            for left, right in zip(original, cached):
                product = left.mul(right)
                require(product.identity_roof() and not product.u,
                        "forward_dag:inverse_primitive_law")
            self.meter.bump("typed_context_products", 10, "forward_dag.inverse_primitive")
            self.inverse_states[normalized] = cached
        return cached[index]


def primitive_inventory(authority: AuthorityAdapter) -> tuple[list[tuple[int, ...]], dict[str, Any]]:
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
        anc = row.get("ancestry", {})
        sections.add(register(anc.get("section_source_word", []), "primitive:section_source"))
        sections.add(register(anc.get("section_target_word", []), "primitive:section_target"))
        records.add(register(anc.get("record_word", []), "primitive:record"))
        if isinstance(anc.get("q0_relator_word"), list):
            qrels.add(register(anc["q0_relator_word"], "primitive:q0_relator"))
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for name, item in value.items():
                if name == "q0_relator_word" and isinstance(item, list):
                    qrels.add(register(item, "primitive:q0_relator"))
                elif isinstance(item, (dict, list)): walk(item)
        elif isinstance(value, list):
            for item in value: walk(item)
    walk(authority.receipt.get("Q0", {})); walk(authority.receipt.get("bridge", {}))
    words = sorted(sections | records | qrels, key=lambda x: (len(x), x))
    require((len(sections), len(records), len(qrels), len(words)) == (243, 26, 19, 288),
            "primitive:inventory")
    literal = sum(map(len, words)); by_layer = {layer: sum(len(row.get("word", [])) for row in authority.rows
                                                            if row.get("layer") == layer) for layer in LAYERS}
    require(literal == 114458 and sum(by_layer.values()) == 5475488 and
            by_layer == {"Gamma_Cayley": 5433366, "action": 33206, "Q0_lift": 8916},
            "primitive:literal_inventory")
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
    anc = row.get("ancestry", {})
    record = registered_primitive(anc.get("record_word", []), "ancestry:record")
    target = registered_primitive(anc.get("section_target_word", []), "ancestry:target")
    source = registered_primitive(anc.get("section_source_word", []), "ancestry:source")
    layer = row.get("layer")
    if layer == "Gamma_Cayley":
        parts = [source, record, registered_inverse(anc.get("section_target_word", []), "ancestry:target")]; grammar = "Gamma_Cayley"
    elif layer == "action":
        letter = int(row.get("letter")); require(letter in (-2, -1, 1, 2), "ancestry:action_letter")
        tokens = tuple(int(x) for x in anc.get("tokens", []))
        expected_tokens = ((-letter,) + record + (letter,) if int(row.get("orientation")) == 1
                          else (letter,) + record + (-letter,))
        require(tokens == expected_tokens, "ancestry:action_tokens")
        # The actor pair is assembled by the action row evaluator.  Keep the
        # record and target as the two DAG pieces so the outer actors are not
        # accidentally evaluated twice.
        parts = [record, registered_inverse(anc.get("section_target_word", []), "ancestry:target")]; grammar = "action"
    elif layer == "Q0_lift":
        qrel = registered_primitive(anc.get("q0_relator_word", []), "ancestry:q0_relator")
        parts = [qrel, registered_inverse(anc.get("section_target_word", []), "ancestry:target")]; grammar = "Q0_lift"
    else:
        raise InputStop("ancestry:unknown_layer")
    expected = (word_mul(*parts) if layer != "action" else
                word_mul(tokens, parts[1]))
    # Authority validation has already proved the stored literal is reduced;
    # this route performs only the required linear literal comparison.
    require(expected == tuple(row.get("word", [])), "ancestry:stored_word_mismatch")
    return expected, parts, {"grammar": grammar, "parts": [list(p) for p in parts]}


class BoundarySeed:
    def __init__(self, index: int, context: int, relation: int, quotient: Any,
                 occurrences: list[tuple[int, Any, int]]):
        self.index, self.context, self.relation, self.q = index, context, relation, quotient
        self.occurrences = occurrences; self.identity = raw_key(context, relation, quotient.identity)

    def translate(self, t: Any) -> dict[str, int]:
        return {row_key(self.context, component, self.q.mul(t, element)): coefficient
                for component, element, coefficient in self.occurrences if coefficient % 3}


class BoundaryLedger:
    """65 typed seeds; occurrence index makes work exactly P_q."""
    def __init__(self, runtime: Runtime, meter: Meter):
        self.runtime, self.meter = runtime, meter; self.seeds: list[BoundarySeed] = []
        self.by_component: dict[tuple[int, int], list[tuple[BoundarySeed, Any, int]]] = {}
        self.seed_by_context_relation: dict[tuple[int, int], BoundarySeed] = {}
        self.inverse_cache: dict[tuple[int, Any], Any] = {}; self.psi_cache: dict[str, dict[str, int]] = {}
        index = 0
        for context in range(10):
            q = runtime.quotient(context); relations = runtime.old.pure_relations(3 if context < 5 else 4)
            require(len(relations) == (2 if context < 5 else 11), "boundary:typed_relation_count")
            for relation, word in enumerate(relations):
                state = runtime.eval_pb(word, context); require(state.identity_roof(), "boundary:seed_roof")
                occurrences = [(component, element, coefficient) for (component, element), coefficient in state.u.items()
                               if coefficient % 3]
                seed = BoundarySeed(index, context, relation, q, occurrences); self.seeds.append(seed)
                self.seed_by_context_relation[context, relation] = seed
                for component, element, coefficient in occurrences:
                    self.by_component.setdefault((context, component), []).append((seed, element, coefficient))
                    self.inverse_cache[context, element] = q.inverse(element)
                index += 1; meter.bump("typed_context_products", 1, "boundary_seed")
        require(len(self.seeds) == 65 and sum(x.context < 5 for x in self.seeds) == 10 and
                sum(x.context >= 5 for x in self.seeds) == 55, "boundary:65_seed_roster")

    def psi(self, ledger: dict[str, int]) -> dict[str, int]:
        ident = digest(ledger)
        if ident in self.psi_cache: return self.psi_cache[ident]
        out: dict[str, int] = {}
        for key, coefficient in ledger.items():
            context, relation, text = split_raw_key(key); t = decode_token(text)
            seed = self.seed_by_context_relation.get((context, relation))
            require(seed is not None, "boundary:ledger_seed")
            out = add_row(out, seed.translate(t), coefficient)
            self.meter.bump("canonicalization", 1, "psi_once")
        self.psi_cache[ident] = out; return out

    def action(self, ledger: dict[str, int], actors: Sequence[Any]) -> dict[str, int]:
        out: dict[str, int] = {}
        self.meter.reserve("affine_sparse_ops", len(ledger), "ledger_action")
        for key, coefficient in ledger.items():
            context, relation, text = split_raw_key(key); q = self.runtime.quotient(context)
            moved = q.mul(actors[context], decode_token(text)); out_key = raw_key(context, relation, moved)
            out[out_key] = (out.get(out_key, 0) + int(coefficient)) % 3
        self.meter.bump("affine_sparse_ops", len(ledger), "ledger_action")
        return {key: value for key, value in out.items() if value}


class Echelon:
    def __init__(self, meter: Meter):
        self.meter = meter; self.rows: dict[str, dict[str, int]] = {}; self.labels: dict[str, str] = {}
        self.pivots: list[str] = []

    def reduce(self, row: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        rem = {key: int(value) % 3 for key, value in row.items() if int(value) % 3}; corr: dict[str, int] = {}
        for pivot in self.pivots:
            coefficient = rem.get(pivot, 0)
            if coefficient:
                rem = add_row(rem, self.rows[pivot], -coefficient)
                label = self.labels[pivot]; corr[label] = (corr.get(label, 0) + coefficient) % 3
                self.meter.bump("membership_reductions", 1, "echelon_reduce")
        return rem, {key: value for key, value in corr.items() if value}

    def insert(self, row: dict[str, int], label: str) -> dict[str, Any] | None:
        rem, correction = self.reduce(row)
        if not rem: return None
        pivot = min(rem); scale = 1 if rem[pivot] == 1 else 2
        stored = scale_row(rem, scale); self.rows[pivot] = stored; self.labels[pivot] = label
        # Keep elimination order, not lexicographic pivot order: later rows
        # are reduced against every earlier pivot and may have a smaller key.
        self.pivots.append(pivot); self.meter.bump("affine_sparse_ops", 1, "echelon_insert")
        relation = {label: scale}
        for old, value in correction.items(): relation[old] = (-scale * value) % 3
        return {"pivot": pivot, "scale": scale, "row": stored,
                "reduction": correction,
                "relation": {key: value for key, value in relation.items() if value}}

    def replay(self, relation: dict[str, int], roster: dict[str, dict[str, int]]) -> dict[str, int]:
        out: dict[str, int] = {}
        for label, coefficient in relation.items():
            require(label in roster, "echelon:relation_label")
            out = add_row(out, roster[label], coefficient)
        return out


class LiveBasis:
    def __init__(self, meter: Meter, ledger: BoundaryLedger):
        self.meter, self.ledger = meter, ledger; self.combined = Echelon(meter); self.boundary = Echelon(meter)
        self.b_rows: dict[str, dict[str, int]] = {}; self.b_ledgers: dict[str, dict[str, int]] = {}
        self.boundary_ledgers: dict[str, dict[str, int]] = {}; self.combined_ledgers: dict[str, dict[str, int]] = {}
        self.b_coefficients: dict[str, dict[str, int]] = {}
        self.b_formals: dict[str, tuple[dict[str, int], dict[str, int]]] = {}
        self.k_rows: dict[str, dict[str, int]] = {}; self.k_items: list[dict[str, Any]] = []
        self.active_registry: set[str] = set()
        self.insertion_events: list[dict[str, Any]] = []

    def add_boundary(self, column: dict[str, int], raw_identity: str) -> dict[str, Any]:
        before, correction = self.boundary.reduce(column)
        require(before, "boundary:selected_already_span")
        pivot = min(before); scale = 1 if before[pivot] == 1 else 2
        label = f"B:{len(self.b_rows)}"; ledger_value = {raw_identity: 1}
        for old, coefficient in correction.items():
            require(old in self.boundary_ledgers, "boundary:ledger_old_label")
            ledger_value = add_ledger(ledger_value, self.boundary_ledgers[old], -coefficient)
        ledger_value = scale_ledger(ledger_value, scale); stored = scale_row(before, scale)
        bdetail = self.boundary.insert(column, label); require(bdetail and bdetail["row"] == stored,
                                                              "boundary:insert_replay")
        cdetail = self.combined.insert(stored, label); require(cdetail is not None, "boundary:combined_insert")
        combined_ledger = scale_ledger(ledger_value, cdetail["scale"])
        combined_coefficients: dict[str, int] = {}
        for old, coefficient in cdetail["reduction"].items():
            require(old in self.b_formals, "boundary:combined_formal_old")
            old_q, old_c = self.b_formals[old]
            combined_ledger = add_ledger(combined_ledger, old_q, -cdetail["scale"] * coefficient)
            combined_coefficients = add_row(combined_coefficients, old_c,
                                            -cdetail["scale"] * coefficient)
        self.b_rows[label], self.b_ledgers[label] = cdetail["row"], combined_ledger
        self.b_coefficients[label] = combined_coefficients
        self.b_formals[label] = (combined_ledger, combined_coefficients)
        self.boundary_ledgers[label] = ledger_value; self.combined_ledgers[label] = combined_ledger
        self.active_registry.update(cdetail["row"])
        self.insertion_events.append({"kind": "B", "label": label, "column": column,
                                      "raw_identity": raw_identity, "boundary_row": stored,
                                      "combined_row": cdetail["row"], "boundary_pivot": pivot,
                                      "boundary_scale": scale, "boundary_reduction": correction,
                                      "combined_detail": cdetail})
        self.meter.bump("boundary_rank_rises", 1, "boundary_rank_rise")
        return {"label": label, "row": stored, "ledger": ledger_value, "pivot": cdetail["pivot"],
                "scale": scale, "raw_identity": raw_identity}

    def add_k(self, row: dict[str, int], label: str, word: Sequence[int], ledger_value: dict[str, int],
              word_node: int, actual: list[AffineState]) -> dict[str, Any]:
        self.meter.reserve("active_keys", len(row), "kernel_rank_rise")
        detail = self.combined.insert(row, label); require(detail is not None and not detail["reduction"], "kernel:strict_rank_rise")
        self.combined_ledgers[label] = {}
        self.b_formals[label] = ({}, {label: 1})
        flattened: dict[str, int] = {}
        for index, state in enumerate(actual):
            flattened = add_row(flattened, local_to_row(state.u, index))
        normalized_flattened = add_row(flattened, self.ledger.psi(ledger_value), -1)
        require(normalized_flattened == detail["row"], "rho1:normalized_K_row")
        item = {"label": label, "row": detail["row"], "word": list(word),
                "discrepancy": ledger_value, "pivot": detail["pivot"], "rank": self.rank(),
                "raw_coefficients": detail["relation"], "word_node": word_node,
                "rho0": [element_blob(state.a).hex() for state in actual],
                "rho1": [{"roof": element_blob(state.a).hex(),
                          "fox": local_to_row(state.u, index)} for index, state in enumerate(actual)],
                "rho1_flattened": normalized_flattened, "rho1_actual_flattened": flattened,
                "q": list(h2_word(word))}
        self.k_rows[label] = detail["row"]; self.k_items.append(item)
        self.active_registry.update(detail["row"])
        self.meter.bump("active_keys", len(detail["row"]), "kernel_rank_rise")
        self.insertion_events.append({"kind": "K", "label": label, "row": row,
                                      "combined_detail": detail})
        return item

    def rank(self) -> int:
        return len(self.combined.pivots)

    def roster(self) -> dict[str, dict[str, int]]:
        return {**self.b_rows, **self.k_rows}

    def expand_correction(self, correction: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        q: dict[str, int] = {}; c: dict[str, int] = {}
        for label, coefficient in correction.items():
            if label.startswith("B:"):
                require(label in self.b_formals, "basis:formal_boundary_label")
                q_value, c_value = self.b_formals[label]
                q = add_ledger(q, q_value, coefficient)
                c = add_row(c, c_value, coefficient)
            else:
                c[label] = (c.get(label, 0) + int(coefficient)) % 3
        return q, {label: value for label, value in c.items() if value}


def dual_from_projection(basis: LiveBasis, target: dict[str, int], meter: Meter) -> tuple[dict[str, int], int, set[str]]:
    remainder, _ = basis.combined.reduce(target); require(remainder, "dual:member_target")
    active = set(target) | set(basis.active_registry)
    free = min(remainder); dual: dict[str, int] = {free: 1}
    # Ascending producer elimination is pulled back in its inverse order.
    for pivot in reversed(basis.combined.pivots):
        dot = sum(int(value) * int(dual.get(key, 0)) for key, value in basis.combined.rows[pivot].items()) % 3
        if dot: dual[pivot] = (-dot) % 3
    dual = {key: value % 3 for key, value in dual.items() if value % 3}
    require(set(dual) <= active, "dual:active_registry")
    for row in basis.combined.rows.values():
        require(sum(int(value) * dual.get(key, 0) for key, value in row.items()) % 3 == 0,
                "dual:all_live_dots")
    target_dot = sum(int(value) * dual.get(key, 0) for key, value in target.items()) % 3
    require(target_dot != 0, "dual:target_dot")
    meter.bump("dual_support", len(dual), "dual_pullback")
    return dual, target_dot, active


def correlate(ledger: BoundaryLedger, dual: dict[str, int], meter: Meter) -> dict[str, Any]:
    accum: dict[tuple[int, int, str], int] = {}; pairs = 0
    expected_pairs = sum(len(ledger.by_component.get(split_row_key(key)[:2], ()))
                         for key in dual)
    meter.reserve("correlation_pairs", expected_pairs, "full_D_correlation")
    for dual_key, lambda_value in dual.items():
        context, component, text = split_row_key(dual_key); g = decode_token(text)
        for seed, h, seed_coefficient in ledger.by_component.get((context, component), []):
            inverse_h = ledger.inverse_cache[context, h]; t = seed.q.mul(g, inverse_h)
            require(seed.q.mul(t, h) == g, "dual:translation_product")
            key = (context, seed.relation, token(t)); KEYS[key[2]] = t
            accum[key] = (accum.get(key, 0) + int(lambda_value) * int(seed_coefficient)) % 3
            pairs += 1
    require(pairs == expected_pairs, "dual:correlation_pair_count")
    meter.bump("correlation_pairs", pairs, "full_D_correlation")
    ordered = sorted(((key, value) for key, value in accum.items() if value),
                     key=lambda item: item[0])
    return {"pair_count": pairs, "accumulator_digest": digest(sorted((list(k), v) for k, v in accum.items())),
            "selected": ([ordered[0][0][0], ordered[0][0][1], ordered[0][0][2], ordered[0][1]]
                         if ordered else None), "complete": True}


def h2_mul(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = left; ap, bp, rp = right
    return ((a + ap) % 9, (b + bp) % 9, (r + rp - b * ap) % 9)


def h2_inv(value: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = value; return ((-a) % 9, (-b) % 9, (-r - a * b) % 9)


def h2_word(word: Iterable[int]) -> tuple[int, int, int]:
    out = (0, 0, 0); gens = {1: (1, 0, 0), 2: (0, 1, 0)}
    for letter in word:
        base = gens[abs(int(letter))]; out = h2_mul(out, base if letter > 0 else h2_inv(base))
    return out


def compact_terminal_record(record: dict[str, Any]) -> dict[str, Any]:
    """Retain R:* terminals without duplicating completed sparse vectors.

    A ZERO terminal is the lossless owner for the K item it creates, so its
    Q/c/s/word relation is retained.  Other completed row terminals need only
    their typed identity/rank digest; action records (which are not R:)
    remain lossless for continuation.
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
    """Distinct typed MEMBER, BOUNDARY_RANK_RISE and ZERO_CORRELATION records."""
    def __init__(self, runtime: Runtime, ledger: BoundaryLedger, meter: Meter):
        self.runtime, self.ledger, self.meter = runtime, ledger, meter; self.basis = LiveBasis(meter, ledger)
        self.records: list[dict[str, Any]] = []; self.live_duals: list[dict[str, Any]] = []
        self.event_chain: list[dict[str, Any]] = []; self.dual_chain: list[dict[str, Any]] = []
        # Canonical per-row task198 trace digests; retaining only fixed-size
        # 64-hex values keeps the checkpoint prefix replayable and bounded.
        self.bridge_chain: list[str] = []
        self.epoch = "0" * 64

    def query(self, target: dict[str, int], discrepancy: dict[str, int], word: Sequence[int],
              query_id: str) -> dict[str, Any]:
        meter = self.meter; meter.bump("membership_queries", 1, "quotient_query")
        while True:
            remainder, correction = self.basis.combined.reduce(target)
            if not remainder:
                replay = self.basis.combined.replay(correction, self.basis.roster())
                require(replay == target, "member:coefficient_replay")
                member_q, member_c = self.basis.expand_correction(correction)
                record = {"schema": "MEMBER", "query_id": query_id, "rank": self.basis.rank(),
                          "coefficients": correction, "boundary_Q": member_q,
                          "K_coefficients": member_c, "row_digest": digest(target)}
                self._record(record); return record
            dual, target_dot, active = dual_from_projection(self.basis, target, meter)
            corr = correlate(self.ledger, dual, meter)
            if not self.live_duals:
                self.live_duals.append({"query_id": query_id, "dual": dict(dual),
                                       "target": dict(target), "target_dot": target_dot,
                                       "correlation": corr})
            dual_digest = digest({"query_id": query_id, "dual": sorted(dual.items()),
                                  "target": target, "target_dot": target_dot,
                                  "correlation": corr})
            self.dual_chain.append({"index": len(self.dual_chain) + 1,
                                    "query_id": query_id, "digest": dual_digest})
            if corr["selected"] is not None:
                context, relation, text, coefficient = corr["selected"]; translation = decode_token(text)
                seed = self.ledger.seed_by_context_relation.get((context, relation))
                require(seed is not None, "boundary:selected_seed")
                raw_id = raw_key(context, relation, translation); column = seed.translate(translation)
                self.meter.reserve("active_keys", len(column), "boundary_rank_rise")
                reg = self.basis.add_boundary(column, raw_id)
                self.meter.bump("active_keys", len(column), "boundary_rank_rise")
                record = {"schema": "BOUNDARY_RANK_RISE", "query_id": query_id,
                          "rank_before": self.basis.rank() - 1, "rank_after": self.basis.rank(),
                          "selected": [context, relation, text, coefficient],
                          "column_digest": digest(column), "ledger_digest": digest(reg["ledger"]),
                          "dual_digest": digest(sorted(dual.items())),
                          "pair_count": corr["pair_count"], "accumulator_digest": corr["accumulator_digest"]}
                self._record(record); continue
            q, c = self.basis.expand_correction(correction)
            pivot = min(remainder); scale = 1 if remainder[pivot] == 1 else 2
            record = {"schema": "ZERO_CORRELATION/K_RANK_RISE", "query_id": query_id,
                      "rank": self.basis.rank(), "remainder": remainder,
                      "normalization_scale": scale, "normalized": scale_row(remainder, scale),
                      "Q": q, "c": c, "B_coefficients": {label: value for label, value in correction.items()
                                                             if label.startswith("B:")}, "candidate_word": list(word),
                      "candidate_discrepancy": discrepancy, "target_digest": digest(target),
                      "discrepancy_digest": digest(discrepancy), "dual_digest": digest(sorted(dual.items())),
                      "target_dot": target_dot, "dual_support_digest": digest(sorted(dual.items())),
                      "pair_count": corr["pair_count"], "accumulator_digest": corr["accumulator_digest"],
                      "selected": None, "correlation_complete": corr.get("complete") is True}
            self._record(record); return record

    def _record(self, record: dict[str, Any]) -> None:
        stored = compact_terminal_record(record) if is_row_terminal(record) else record
        record_digest = digest(stored); self.records.append(stored)
        self.event_chain.append({"index": len(self.event_chain) + 1,
                                 "query_id": record["query_id"],
                                 "schema": record["schema"], "digest": record_digest})
        self.epoch = sha((self.epoch + record_digest).encode("ascii"))


class WordDAG:
    """Hash-consed persistent word/ledger DAG with capped materialization."""
    def __init__(self, runtime: Runtime, ledger: BoundaryLedger, meter: Meter, cap: int = 4000000):
        self.runtime, self.ledger, self.meter, self.cap = runtime, ledger, meter, cap
        self.nodes: list[dict[str, Any]] = []; self.interned: dict[tuple[Any, ...], int] = {}
        self.literal_cache: dict[int, tuple[int, ...]] = {}; self.ledger_cache: dict[int, dict[str, int]] = {}

    def _new(self, key: tuple[Any, ...], node: dict[str, Any]) -> int:
        if key in self.interned: return self.interned[key]
        self.meter.reserve("word_nodes", 1, "word_dag_allocate")
        ident = len(self.nodes); self.interned[key] = ident; self.nodes.append(node)
        self.meter.bump("word_nodes", 1, "word_dag_allocate"); return ident

    def _charge_affine(self, amount: int, phase: str) -> None:
        if amount:
            self.meter.reserve("affine_sparse_ops", int(amount), phase)
            self.meter.bump("affine_sparse_ops", int(amount), phase)

    def _charge_context(self, amount: int, phase: str) -> None:
        if amount:
            self.meter.reserve("typed_context_products", int(amount), phase)
            self.meter.bump("typed_context_products", int(amount), phase)

    def source(self, word: Sequence[int], ledger_value: dict[str, int] | None = None) -> int:
        literal = tuple(word_reduce(word)); key = ("source", literal)
        if key in self.interned: return self.interned[key]
        states = self.runtime.states_direct(literal)
        ident = self._new(key, {"op": "source", "word": list(literal),
            "length": len(literal), "states": states, "ledger": ledger_value or {}})
        return ident

    def _state_product(self, left: int, right: int) -> list[AffineState]:
        return [self.nodes[left]["states"][i].mul(self.nodes[right]["states"][i]) for i in range(10)]

    def product(self, children: Sequence[int]) -> int:
        ids = tuple(int(x) for x in children); require(all(x < len(self.nodes) for x in ids), "word_dag:child")
        require(sum(self.nodes[x]["length"] for x in ids) <= self.cap, "word_dag:length_cap")
        key = ("product", ids)
        if key in self.interned: return self.interned[key]
        self._charge_context(10 * len(ids), "word_dag.product_state_products")
        self._charge_affine(sum(len(self.nodes[x]["ledger"]) for x in ids),
                            "word_dag.product_ledger_add")
        states = [self.runtime.identity(i) for i in range(10)]
        ledger_value: dict[str, int] = {}
        for child in ids:
            states = [states[i].mul(self.nodes[child]["states"][i]) for i in range(10)]
            ledger_value = add_ledger(ledger_value, self.nodes[child]["ledger"])
        return self._new(key, {"op": "product", "children": list(ids),
            "length": sum(self.nodes[x]["length"] for x in ids), "states": states, "ledger": ledger_value})

    def inverse(self, child: int) -> int:
        require(0 <= child < len(self.nodes), "word_dag:child")
        key = ("inverse", child)
        if key in self.interned: return self.interned[key]
        node = self.nodes[child]
        self._charge_context(10, "word_dag.inverse_state_products")
        self._charge_affine(len(node["ledger"]), "word_dag.inverse_ledger")
        return self._new(key, {"op": "inverse", "child": child,
            "length": node["length"], "states": [state.inv() for state in node["states"]],
            "ledger": scale_ledger(node["ledger"], -1)})

    def power(self, child: int, exponent: int) -> int:
        require(exponent in (0, 1, 2), "word_dag:power_exponent")
        if exponent == 0:
            return self.source((), {})
        return self.product([child] * exponent)

    def attach_ledger(self, child: int, ledger_value: dict[str, int]) -> int:
        """Attach the live B-correction to the candidate word state."""
        require(0 <= child < len(self.nodes), "word_dag:child")
        key = ("ledger_attach", child, digest(ledger_value))
        if key in self.interned: return self.interned[key]
        self._charge_affine(len(ledger_value), "word_dag.attach_affine")
        return self._new(key,
                         {"op": "ledger_attach", "child": child,
                          "length": self.nodes[child]["length"],
                          "states": self.nodes[child]["states"], "ledger": ledger_value})

    def conjugate(self, letter: int, child: int) -> int:
        require(letter in (-2, -1, 1, 2) and 0 <= child < len(self.nodes), "word_dag:conjugate_owner")
        key = ("conjugate", int(letter), child)
        if key in self.interned: return self.interned[key]
        actor = self._new(("actor", int(letter)), {"op": "actor", "letter": int(letter), "length": 1,
            "states": [self.runtime.actors[i, int(letter)] for i in range(10)], "ledger": {}})
        inverse_actor = self._new(("actor", -int(letter)), {"op": "actor", "letter": -int(letter), "length": 1,
            "states": [self.runtime.actors[i, -int(letter)] for i in range(10)], "ledger": {}})
        # Do not intern actor*child*actor^-1 as an ordinary product: that
        # intermediate would carry the child's untranslated ledger into a
        # checkpoint-visible node.
        self._charge_context(20, "word_dag.conjugate_state_products")
        states = [self.nodes[actor]["states"][i].mul(self.nodes[child]["states"][i]).mul(
                  self.nodes[inverse_actor]["states"][i]) for i in range(10)]
        translated = self.ledger.action(self.nodes[child]["ledger"],
                                         [self.runtime.actors[i, int(letter)].a for i in range(10)])
        return self._new(key,
                         {"op": "conjugate", "letter": int(letter), "child": child,
                          "length": self.nodes[child]["length"] + 2, "states": states,
                          "ledger": translated})

    def materialize(self, node: int) -> tuple[int, ...]:
        if node in self.literal_cache: return self.literal_cache[node]
        require(0 <= int(node) < len(self.nodes), "word_dag:materialize_node")
        pending: list[tuple[int, bool]] = [(int(node), False)]
        while pending:
            ident, ready = pending.pop()
            if ident in self.literal_cache: continue
            item = self.nodes[ident]; op = item["op"]
            children = ([int(item["child"])] if op in {"inverse", "ledger_attach", "conjugate"} else
                        [int(value) for value in item.get("children", [])] if op == "product" else [])
            require(all(0 <= child < len(self.nodes) for child in children), "word_dag:materialize_child")
            require(int(item.get("length", 0)) <= self.cap, "word_dag:expanded_cap")
            if not ready:
                pending.append((ident, True))
                for child in reversed(children):
                    if child not in self.literal_cache: pending.append((child, False))
                continue
            if op == "source": out = tuple(item["word"])
            elif op == "actor": out = (int(item["letter"]),)
            elif op == "inverse": out = word_inv(self.literal_cache[children[0]])
            elif op == "conjugate":
                out = word_mul((int(item["letter"]),), self.literal_cache[children[0]],
                               (-int(item["letter"]),))
            elif op == "ledger_attach": out = self.literal_cache[children[0]]
            else: out = word_mul(*(self.literal_cache[child] for child in children))
            # Stored DAG length is a pre-expansion upper bound; joins may
            # freely cancel.  The memoized literal is the exact reduced
            # spelling and therefore supplies the exact length after the
            # capped assembly.
            require(len(out) <= int(item["length"]) and len(out) <= self.cap,
                    "word_dag:expanded_cap")
            self.meter.bump("expanded_letters", len(out), "word_dag_materialize")
            self.literal_cache[ident] = out
        return self.literal_cache[node]


def restore_word_dag(words: WordDAG, saved: list[dict[str, Any]]) -> None:
    """Restore the topologically ordered live DAG without consuming rows."""
    require(isinstance(saved, list), "checkpoint:word_dag_shape")
    for ident, record in enumerate(saved):
        require(isinstance(record, dict), "checkpoint:word_dag_node_shape")
        op = record.get("op")
        required = {"source": {"op", "word", "length", "ledger"},
                    "actor": {"op", "letter", "length", "ledger"},
                    "product": {"op", "children", "length", "ledger"},
                    "inverse": {"op", "child", "length", "ledger"},
                    "ledger_attach": {"op", "child", "length", "ledger"},
                    "conjugate": {"op", "letter", "child", "length", "ledger"}}.get(op)
        require(required is not None and set(record) == required, "checkpoint:word_dag_node_fields")
        if op == "source":
            # A source is a literal word owner, never a mutable discrepancy
            # owner.  Reject a resealed checkpoint which injects a ledger at
            # this boundary instead of silently installing that detached
            # value into the live DAG.
            require(record.get("ledger", {}) == {}, "checkpoint:source_ledger")
            node = words.source(record.get("word", []), {})
        elif op == "actor":
            letter = int(record.get("letter")); require(letter in (-2, -1, 1, 2),
                                                        "checkpoint:word_dag_actor_letter")
            node = words._new(("actor", letter), {"op": "actor", "letter": letter,
                "length": 1, "states": [words.runtime.actors[i, letter] for i in range(10)],
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
            raise Reject("checkpoint:word_dag_opcode")
        require(node == ident, "checkpoint:word_dag_topology")
        actual = words.nodes[node]
        for key in required: require(actual.get(key) == record[key], "checkpoint:word_dag_node:" + key)


def restore_basis(basis: LiveBasis, state: dict[str, Any], words: WordDAG | None = None) -> None:
    """Rebuild mixed echelons and every owner from the chronological events."""
    boundary_state = state.get("boundary_echelon", {})
    combined_state = state.get("echelon_rebuild", {})
    events = state.get("insertion_events", [])
    require(isinstance(boundary_state, dict) and isinstance(combined_state, dict) and
            isinstance(events, list) and isinstance(state.get("B_roster"), dict) and
            isinstance(state.get("B_ledgers"), dict) and isinstance(state.get("boundary_ledgers"), dict) and
            isinstance(state.get("combined_ledgers"), dict) and isinstance(state.get("B_coefficients"), dict) and
            isinstance(state.get("B_formals"), dict) and isinstance(state.get("K_roster"), list),
            "checkpoint:echelon_state_shape")
    saved_b_rows = dict(state["B_roster"]); saved_b_ledgers = dict(state["B_ledgers"])
    saved_boundary_ledgers = dict(state["boundary_ledgers"]); saved_combined_ledgers = dict(state["combined_ledgers"])
    saved_b_coefficients = dict(state["B_coefficients"])
    saved_formals = {str(label): (pair[0], pair[1]) for label, pair in state["B_formals"].items()}
    saved_items = list(state["K_roster"]); saved_by_label = {str(item.get("label")): item for item in saved_items}
    saved_records = {str(record.get("query_id")): record
                     for record in state.get("oracle_records", [])
                     if isinstance(record, dict) and record.get("query_id") is not None}
    require(len(saved_by_label) == len(saved_items), "checkpoint:K_duplicate_label")
    rebuilt_boundary = Echelon(basis.meter); rebuilt_combined = Echelon(basis.meter)
    derived_b_rows: dict[str, dict[str, int]] = {}; derived_b_ledgers: dict[str, dict[str, int]] = {}
    derived_boundary_ledgers: dict[str, dict[str, int]] = {}; derived_combined_ledgers: dict[str, dict[str, int]] = {}
    derived_b_coefficients: dict[str, dict[str, int]] = {}
    derived_formals: dict[str, tuple[dict[str, int], dict[str, int]]] = {}
    derived_k_rows: dict[str, dict[str, int]] = {}; derived_items: list[dict[str, Any]] = []
    derived_active: set[str] = set()
    next_b_label = 0; next_k_label = 0
    for event in events:
        require(isinstance(event, dict) and event.get("label"), "checkpoint:echelon_event_shape")
        label = str(event["label"]); kind = event.get("kind")
        if kind == "B":
            require(label == "B:" + str(next_b_label) and isinstance(event.get("raw_identity"), str),
                    "checkpoint:boundary_event_owner")
            next_b_label += 1
            bdetail = rebuilt_boundary.insert(event.get("column", {}), label)
            require(bdetail is not None and bdetail.get("pivot") == event.get("boundary_pivot") and
                    bdetail.get("scale") == event.get("boundary_scale") and
                    bdetail.get("row") == event.get("boundary_row") and
                    bdetail.get("reduction") == event.get("boundary_reduction"),
                    "checkpoint:boundary_event_replay")
            cdetail = rebuilt_combined.insert(event.get("boundary_row", {}), label)
            require(cdetail is not None and cdetail == event.get("combined_detail") and
                    event.get("combined_row") == cdetail.get("row"),
                    "checkpoint:combined_boundary_event_replay")
            raw_ledger = {event["raw_identity"]: 1}
            for old, coefficient in bdetail["reduction"].items():
                require(old in derived_boundary_ledgers, "checkpoint:boundary_old_owner")
                raw_ledger = add_ledger(raw_ledger, derived_boundary_ledgers[old], -coefficient)
            boundary_ledger = scale_ledger(raw_ledger, int(bdetail["scale"]))
            require(basis.ledger.psi({event["raw_identity"]: 1}) == event.get("column"),
                    "checkpoint:boundary_raw_identity")
            combined_ledger = scale_ledger(boundary_ledger, int(cdetail["scale"]))
            combined_coefficients: dict[str, int] = {}
            for old, coefficient in cdetail["reduction"].items():
                require(old in derived_formals, "checkpoint:combined_formal_old")
                old_q, old_c = derived_formals[old]
                combined_ledger = add_ledger(combined_ledger, old_q, -int(cdetail["scale"]) * coefficient)
                combined_coefficients = add_row(combined_coefficients, old_c,
                                                -int(cdetail["scale"]) * coefficient)
            derived_b_rows[label] = cdetail["row"]; derived_b_ledgers[label] = combined_ledger
            derived_active.update(cdetail["row"])
            derived_boundary_ledgers[label] = boundary_ledger; derived_combined_ledgers[label] = combined_ledger
            derived_b_coefficients[label] = combined_coefficients
            derived_formals[label] = (combined_ledger, combined_coefficients)
        elif kind == "K":
            require(label == "K:" + str(next_k_label) and label in saved_by_label,
                    "checkpoint:K_event_owner")
            next_k_label += 1
            item = saved_by_label[label]; cdetail = rebuilt_combined.insert(event.get("row", {}), label)
            require(cdetail is not None and cdetail == event.get("combined_detail") and
                    item.get("row") == cdetail.get("row") and
                    item.get("pivot") == cdetail.get("pivot") and
                    item.get("raw_coefficients") == cdetail.get("relation") and
                    int(item.get("rank", -1)) == len(rebuilt_combined.pivots),
                    "checkpoint:K_event_owner")
            require(words is not None, "checkpoint:K_word_dag_required")
            ancestry = item.get("ancestry", {}); parent_query = str(ancestry.get("parent_query", ""))
            query = saved_records.get(parent_query)
            require(isinstance(query, dict) and query.get("schema") == "ZERO_CORRELATION/K_RANK_RISE" and
                    query.get("query_id") == parent_query and
                    ancestry.get("kind") == "K_recurrence" and
                    ancestry.get("candidate_word") == item.get("candidate_word") and
                    ancestry.get("Q") == item.get("Q") and ancestry.get("c") == item.get("c") and
                    int(ancestry.get("s", -1)) == int(item.get("normalization_scale", -2)) and
                    query.get("candidate_word") == item.get("candidate_word") and
                    query.get("candidate_discrepancy") == item.get("candidate_E") and
                    query.get("Q") == item.get("Q") and query.get("c") == item.get("c") and
                    int(query.get("normalization_scale", -1)) == int(item.get("normalization_scale", -2)) and
                    query.get("normalized") == item.get("row"), "checkpoint:K_query_ancestry")
            prior_labels = list(ancestry.get("prior_labels", [])); prior_map = {prior["label"]: prior for prior in derived_items}
            require(prior_labels == sorted(item.get("c", {}).keys()) and
                    all(label in prior_map for label in prior_labels) and
                    all(label in item.get("c", {}) and int(item["c"][label]) in (1, 2)
                        for label in prior_labels), "checkpoint:K_prior_ancestry")
            candidate_node = int(item.get("candidate_node", ancestry.get("candidate_node", -1)))
            require(0 <= candidate_node < len(words.nodes), "checkpoint:K_candidate_node")
            candidate_word = tuple(words.materialize(candidate_node))
            require(list(candidate_word) == item.get("candidate_word"), "checkpoint:K_candidate_word")
            candidate_with_q = words.attach_ledger(candidate_node,
                                                     add_ledger(words.nodes[candidate_node]["ledger"], item["Q"]))
            product_children = [candidate_with_q]
            for prior_label in prior_labels:
                for _ in range(int(item["c"][prior_label])):
                    product_children.append(words.inverse(prior_map[prior_label]["word_node"]))
            expected_node = words.power(words.product(product_children),
                                        int(item["normalization_scale"]))
            node_id = int(item.get("word_node", -1)); require(expected_node == node_id and
                                                               0 <= node_id < len(words.nodes),
                                                               "checkpoint:K_dag_recurrence")
            node = words.nodes[node_id]
            require(item.get("word") == list(words.materialize(node_id)) and
                    node.get("ledger") == item.get("discrepancy"), "checkpoint:K_word_recurrence")
            states = node.get("states", []); require(isinstance(states, list) and len(states) == 10,
                                                      "checkpoint:K_state_arity")
            require(all(state.identity_roof() for state in states), "checkpoint:K_rho0_identity")
            rho0 = [element_blob(state.a).hex() for state in states]
            rho1 = [{"roof": element_blob(state.a).hex(), "fox": local_to_row(state.u, index)}
                    for index, state in enumerate(states)]
            actual_flattened: dict[str, int] = {}
            for index, state in enumerate(states): actual_flattened = add_row(actual_flattened, local_to_row(state.u, index))
            normalized_flattened = add_row(actual_flattened, basis.ledger.psi(item["discrepancy"]), -1)
            require(item.get("rho0") == rho0 and item.get("rho1") == rho1 and
                    item.get("q") == list(h2_word(item["word"])) and
                    item.get("rho1_actual_flattened") == actual_flattened and
                    item.get("rho1_flattened") == normalized_flattened and
                    item.get("row") == normalized_flattened, "checkpoint:K_state_owner")
            derived_k_rows[label] = cdetail["row"]; derived_combined_ledgers[label] = {}
            derived_active.update(cdetail["row"])
            derived_formals[label] = ({}, {label: 1}); derived_items.append(item)
        else:
            raise Reject("checkpoint:echelon_event_kind")
    require(rebuilt_boundary.pivots == boundary_state.get("pivots") and
            rebuilt_boundary.rows == boundary_state.get("rows") and
            rebuilt_boundary.labels == boundary_state.get("labels") and
            rebuilt_combined.pivots == combined_state.get("pivots") and
            rebuilt_combined.rows == combined_state.get("rows") and
            rebuilt_combined.labels == combined_state.get("labels"),
            "checkpoint:echelon_rebuild_mismatch")
    require(saved_b_rows == derived_b_rows and saved_b_ledgers == derived_b_ledgers and
            saved_boundary_ledgers == derived_boundary_ledgers and saved_combined_ledgers == derived_combined_ledgers and
            saved_b_coefficients == derived_b_coefficients and saved_formals == derived_formals and
            saved_items == derived_items, "checkpoint:chronological_owner_mismatch")
    basis.boundary = rebuilt_boundary; basis.combined = rebuilt_combined
    basis.b_rows = derived_b_rows; basis.b_ledgers = derived_b_ledgers
    basis.boundary_ledgers = derived_boundary_ledgers; basis.combined_ledgers = derived_combined_ledgers
    basis.b_coefficients = derived_b_coefficients; basis.b_formals = derived_formals
    basis.k_items = derived_items; basis.k_rows = derived_k_rows; basis.insertion_events = list(events)
    basis.active_registry = derived_active
    require(set(basis.b_rows) == {label for label in rebuilt_combined.labels.values() if label.startswith("B:")} and
            set(basis.k_rows) == {label for label in rebuilt_combined.labels.values() if label.startswith("K:")},
            "checkpoint:echelon_label_registry")
    for pivot, label in rebuilt_boundary.labels.items():
        require(label in basis.boundary_ledgers and
                basis.ledger.psi(basis.boundary_ledgers[label]) == rebuilt_boundary.rows[pivot],
                "checkpoint:raw_boundary_replay")
    for pivot, label in rebuilt_combined.labels.items():
        require(label in basis.b_formals, "checkpoint:combined_formal_label")
        q_value, c_value = basis.b_formals[label]
        require(add_row(basis.ledger.psi(q_value), rebuilt_combined.replay(c_value, basis.k_rows)) ==
                rebuilt_combined.rows[pivot], "checkpoint:combined_formal_replay")
    active = sorted(derived_active)
    require(active == sorted(state.get("active_registry", [])), "checkpoint:active_registry")


def add_ledger(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        coefficient = (out.get(key, 0) + int(scale) * int(value)) % 3
        if coefficient: out[key] = coefficient
        else: out.pop(key, None)
    return out


def scale_ledger(value: dict[str, int], scale: int) -> dict[str, int]:
    return {key: (int(coefficient) * int(scale)) % 3 for key, coefficient in value.items()
            if (int(coefficient) * int(scale)) % 3}


def h2_projection_checks(runtime: Runtime, basis: LiveBasis) -> list[dict[str, Any]]:
    out = []
    for item in basis.k_items:
        word = tuple(item["word"]); states = runtime.states_direct(word)
        require(all(state.identity_roof() for state in states), "anchor:rho0_identity")
        q = h2_word(word); require(q[0] == 0 and q[1] == 0 and q[2] in (0, 3, 6), "anchor:q_image")
        exponent = q[2] // 3 % 3
        rho0 = [element_blob(state.a).hex() for state in states]
        rho1 = [{"roof": element_blob(state.a).hex(), "fox": local_to_row(state.u, index)}
                for index, state in enumerate(states)]
        actual_flattened = runtime.row_from_states(states)
        normalized_flattened = add_row(actual_flattened,
                                       basis.ledger.psi(item["discrepancy"]), -1)
        require(item.get("rho0") == rho0 and item.get("rho1") == rho1 and
                item.get("q") == list(q) and
                normalized_flattened == item.get("row") and
                actual_flattened == item.get("rho1_actual_flattened") and
                normalized_flattened == item.get("rho1_flattened"),
                "anchor:stored_projection_replay")
        out.append({"label": item["label"], "q": list(q), "exponent": exponent,
                    "rho0": rho0, "rho1": rho1,
                    "rho1_flattened": item["rho1_flattened"],
                    "rho1_actual_flattened": item["rho1_actual_flattened"]})
    return out


def exact_discrepancy(runtime: Runtime, ledger: BoundaryLedger, word: Sequence[int],
                      representative: dict[str, int], ledger_value: dict[str, int], meter: Meter,
                      states: Sequence[AffineState] | None = None) -> dict[str, Any]:
    states = list(states) if states is not None else runtime.states_direct(word)
    actual = runtime.row_from_states(states)
    expected = add_row(representative, ledger.psi(ledger_value))
    require(actual == expected, "discrepancy:raw_affine_equality")
    return {"word": list(word), "row_digest": digest(actual), "ledger_digest": digest(ledger_value),
            "actual": actual}


def accept_k(oracle: Oracle, runtime: Runtime, ledger: BoundaryLedger, dag: WordDAG,
             query: dict[str, Any], candidate_node: int, label: str, meter: Meter) -> dict[str, Any]:
    require(query["schema"] == "ZERO_CORRELATION/K_RANK_RISE", "kernel:typed_zero_schema")
    c = {str(key): int(value) for key, value in query["c"].items()}; q = query["Q"]
    prior = {item["label"]: item for item in oracle.basis.k_items}; prior_sum: dict[str, int] = {}
    for klabel, coefficient in c.items():
        require(klabel in prior, "discrepancy:prior_label")
        prior_sum = add_ledger(prior_sum, prior[klabel]["discrepancy"], coefficient)
    candidate_E = query["candidate_discrepancy"]
    e_new = scale_ledger(add_ledger(add_ledger(candidate_E, q), prior_sum, -1),
                         int(query["normalization_scale"]))
    candidate_with_q = dag.attach_ledger(candidate_node,
                                         add_ledger(dag.nodes[candidate_node]["ledger"], q))
    product_children = [candidate_with_q]
    for klabel in sorted(c):
        for _ in range(c[klabel]): product_children.append(dag.inverse(prior[klabel]["word_node"]))
    product_node = dag.product(product_children); item_node = dag.power(product_node, int(query["normalization_scale"]))
    require(dag.nodes[item_node]["ledger"] ==
            scale_ledger(add_ledger(add_ledger(candidate_E, q), prior_sum, -1),
                         int(query["normalization_scale"])),
            "discrepancy:word_ledger_recurrence")
    new_word = dag.materialize(item_node); actual = runtime.states_direct(new_word)
    representative = query["normalized"]
    replay = exact_discrepancy(runtime, ledger, new_word, representative, e_new, meter, actual)
    item = oracle.basis.add_k(representative, label, new_word, e_new, item_node, actual)
    item.update({"candidate_node": candidate_node, "candidate_word": list(dag.materialize(candidate_node)),
                 "candidate_E": candidate_E, "Q": q, "c": c,
                 "normalization_scale": int(query["normalization_scale"]),
                 "word_formula": "red((W_v product_l W_l^(-c_l))^s)",
                 "E_formula": "s*(E_v+Q-sum(c_l E_l))", "replay": replay,
                 "strict_rank_rise": True,
                 "ancestry": {"kind": "K_recurrence", "parent_query": query["query_id"],
                              "candidate_node": candidate_node, "candidate_word": list(dag.materialize(candidate_node)),
                              "Q": q, "c": c, "s": int(query["normalization_scale"]),
                              "prior_labels": sorted(c) }})
    return item


def compose_matrix(left: dict[str, dict[str, int]], right: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for source, middle_terms in right.items():
        column: dict[str, int] = {}
        for middle, coefficient in middle_terms.items():
            for target, value in left.get(middle, {}).items():
                column[target] = (column.get(target, 0) + int(coefficient) * int(value)) % 3
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


def action_column(basis: LiveBasis, query: dict[str, Any], new_label: str | None = None) -> dict[str, int]:
    """Project an action query to the final K quotient, retaining rank rises."""
    if query["schema"] == "MEMBER":
        return {label: int(coefficient) % 3 for label, coefficient in query["K_coefficients"].items()
                if int(coefficient) % 3}
    require(query["schema"] == "ZERO_CORRELATION/K_RANK_RISE" and new_label is not None,
            "action:column_schema")
    column = {label: int(coefficient) % 3 for label, coefficient in query.get("c", {}).items()
              if label.startswith("K:") and int(coefficient) % 3}
    scale = int(query["normalization_scale"]) % 3
    require(scale in (1, 2) and (scale * scale) % 3 == 1, "action:scale_inverse")
    inverse_scale = scale  # F_3^*: s^{-1}=s for s in {1,2}.
    column[new_label] = (column.get(new_label, 0) + inverse_scale) % 3
    return {label: value for label, value in column.items() if value}


def replay_action_projection(basis: LiveBasis, ledger: BoundaryLedger, target: dict[str, int],
                             query: dict[str, Any], column: dict[str, int]) -> None:
    target_mod_b = add_row(target, ledger.psi(query.get("boundary_Q", query.get("Q", {}))), -1)
    kpart = basis.combined.replay(column, basis.k_rows)
    require(kpart == target_mod_b, "action:projected_K_replay")


def validate_queue_prefix(basis: LiveBasis, ledger: BoundaryLedger, runtime: Runtime,
                          records: list[dict[str, Any]], queue: list[int], cursor: int,
                          actions: list[dict[str, Any]], matrix: dict[str, dict[str, dict[str, int]]],
                          action_events: list[dict[str, Any]]) -> None:
    """Replay only saved action relations; completed actions are not rerun."""
    order = (1, -1, 2, -2)
    require(isinstance(queue, list) and all(type(index) is int for index in queue) and
            0 <= cursor <= len(queue) and len(set(queue)) == len(queue) and
            queue == list(range(len(basis.k_items))) and
            len(actions) == len(action_events) == 4 * cursor,
            "checkpoint:action_prefix_shape")
    for parent_index in queue[:cursor]:
        require(0 <= parent_index < len(basis.k_items), "checkpoint:action_parent_registry")
    processed = {basis.k_items[queue[index]]["label"] for index in range(cursor)}
    expected_columns = {str(letter): {} for letter in order}
    for index in range(cursor):
        parent = basis.k_items[queue[index]]
        for offset, letter in enumerate(order):
            action = actions[index * 4 + offset]; event = action_events[index * 4 + offset]
            require(action.get("parent") == parent["label"] and int(action.get("letter")) == letter and
                    event.get("index") == index * 4 + offset + 1 and
                    event.get("digest") == digest(action), "checkpoint:action_order")
            terminal_id = int(action.get("terminal_id", -1)); require(0 <= terminal_id < len(records),
                                                                     "checkpoint:action_terminal_id")
            query = records[terminal_id]
            require(query.get("query_id") == event.get("query_id") and
                    query.get("schema") in ("MEMBER", "ZERO_CORRELATION/K_RANK_RISE"),
                    "checkpoint:action_terminal_record")
            target = translated_row(parent["row"], runtime, letter)
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
                require(len(matches) == 1, "checkpoint:action_new_K_owner")
                column = action_column(basis, query, matches[0]["label"])
            require(action.get("basis_column") == column and matrix.get(str(letter), {}).get(parent["label"]) == column,
                    "checkpoint:action_column_replay")
            replay_action_projection(basis, ledger, target, query, column)
            expected_columns[str(letter)][parent["label"]] = column
    validate_action_matrix(matrix, {item["label"] for item in basis.k_items},
                           "checkpoint:action_matrix_prefix")
    for letter in order:
        require(isinstance(matrix.get(str(letter), {}), dict) and
                set(matrix.get(str(letter), {})) == processed and
                matrix.get(str(letter), {}) == expected_columns[str(letter)],
                "checkpoint:action_matrix_prefix")


def build_anchor(runtime: Runtime, ledger: BoundaryLedger, basis: LiveBasis, dag: WordDAG,
                 meter: Meter) -> dict[str, Any]:
    projections = h2_projection_checks(runtime, basis); active = [i for i, row in enumerate(projections)
                                                                   if row["exponent"] != 0]
    require(active, "anchor:all_q_exponents_zero:UNKNOWN_INPUT")
    selected = active[0]; exponent = int(projections[selected]["exponent"]); scalar = 1 if exponent == 1 else 2
    source = basis.k_items[selected]; powered_node = dag.power(source["word_node"], scalar)
    powered = dag.materialize(powered_node); states = runtime.states_direct(powered); q = h2_word(powered)
    require(q == (0, 0, 3), "anchor:q_z0")
    rep = scale_row(source["row"], scalar); e = scale_ledger(source["discrepancy"], scalar)
    replay = exact_discrepancy(runtime, ledger, powered, rep, e, meter, states)
    labels = [item["label"] for item in basis.k_items]; anchor_label = source["label"]
    transform: dict[str, dict[str, int]] = {}
    for index, item in enumerate(basis.k_items):
        label = item["label"]
        if index == selected: transform[label] = {label: scalar}
        else:
            ai = int(projections[index]["exponent"])
            # K~=K*T: the non-anchor column is e_i-a_i*e*e_j.
            transform[label] = {label: 1, anchor_label: (-ai * scalar) % 3}
    inverse_transform: dict[str, dict[str, int]] = {}; anchor_exponent = exponent % 3
    for index, label in enumerate(labels):
        if index == selected: inverse_transform[label] = {label: anchor_exponent}
        else:
            ai = int(projections[index]["exponent"])
            # T^-1 sends the adapted non-anchor back by e_i+a_i*e_j.
            inverse_transform[label] = {label: 1, anchor_label: ai % 3}
    identity_matrix = {label: {label: 1} for label in labels}
    require(compose_matrix(transform, inverse_transform) == identity_matrix and
            compose_matrix(inverse_transform, transform) == identity_matrix,
            "anchor:adapted_change_matrix_inverse")
    adapted = []
    for index, item in enumerate(basis.k_items):
        if index == selected: continue
        ai = int(projections[index]["exponent"]); adapted_word = word_mul(tuple(item["word"]), *(word_inv(powered) for _ in range(ai)))
        adapted_row = add_row(item["row"], rep, -ai); adapted_e = add_ledger(item["discrepancy"], e, -ai)
        adapted_states = runtime.states_direct(adapted_word); aq = h2_word(adapted_word)
        adapted_replay = exact_discrepancy(runtime, ledger, adapted_word, adapted_row, adapted_e, meter,
                                           adapted_states)
        require(aq == (0, 0, 0), "anchor:adapted_q")
        require(all(state.identity_roof() for state in adapted_states), "anchor:adapted_rho0")
        adapted_actual: dict[str, int] = {}
        for context, state in enumerate(adapted_states): adapted_actual = add_row(adapted_actual, local_to_row(state.u, context))
        require(add_row(adapted_actual, ledger.psi(adapted_e), -1) == adapted_row, "anchor:adapted_rho1")
        adapted.append({"old_label": item["label"], "word": list(adapted_word), "q": list(aq), "row": adapted_row,
                        "discrepancy": adapted_e, "rho0": [element_blob(state.a).hex() for state in adapted_states],
                        "rho1_flattened": adapted_row, "rho1_actual_flattened": adapted_actual,
                        "replay": adapted_replay})
    return {"diagnostic_only": True, "basis_q": projections, "least_index": selected,
            "inverse_scalar": scalar, "powered_word": list(powered), "powered_q": list(q), "powered_row": rep,
            "powered_discrepancy": e, "powered_rho0": [element_blob(state.a).hex() for state in states],
            "powered_rho1_flattened": add_row(runtime.row_from_states(states), ledger.psi(e), -1),
            "powered_rho1_actual_flattened": runtime.row_from_states(states), "powered_replay": replay,
            "adapted_basis": adapted, "change_matrix": transform, "inverse_change_matrix": inverse_transform,
            "v280_derivation": "a_i from actual q; least j; e=a_j^-1; red(u_i u_*^-a_i)"}


def build_kernel(authority: AuthorityAdapter, runtime: Runtime, dag_forward: ForwardDAG,
                 primitive: list[tuple[int, ...]], inventory: dict[str, Any], meter: Meter,
                 checkpoint_path: Path | None = None,
                 resume_state: dict[str, Any] | None = None) -> dict[str, Any]:
    for word in primitive: dag_forward.add(word)
    require(len(dag_forward.nodes) - 1 == 15970, "forward_dag:edge_count")
    ledger = BoundaryLedger(runtime, meter); oracle = Oracle(runtime, ledger, meter)
    words = WordDAG(runtime, ledger, meter)
    row_digests: list[str] = []; chunks: list[dict[str, Any]] = []; chunk_start = 1
    queue: list[int] = []; actions: list[dict[str, Any]] = []
    action_event_chain: list[dict[str, Any]] = []
    matrix: dict[str, dict[str, dict[str, int]]] = {str(x): {} for x in (1, -1, 2, -2)}
    inverse_checks: dict[str, Any] = {}
    initial_terminals: list[dict[str, Any]] = []; samples = []; sample_rows: dict[int, dict[str, Any]] = {}
    sample_indices = {0, 6317, 6318, 6421, 6422, 6440}
    if resume_state is not None:
        restore_word_dag(words, resume_state.get("word_ledger_dag", []))
        restore_basis(oracle.basis, resume_state, words)
        for item in oracle.basis.k_items:
            node_id = int(item.get("word_node", -1)); require(0 <= node_id < len(words.nodes),
                                                               "checkpoint:K_word_node")
            require(words.materialize(node_id) == tuple(item.get("word", [])),
                    "checkpoint:K_word_recurrence")
        oracle.records = list(resume_state.get("oracle_records", []))
        oracle.live_duals = list(resume_state.get("live_duals", []))
        oracle.event_chain = list(resume_state.get("query_event_chain", []))
        oracle.dual_chain = list(resume_state.get("dual_event_chain", []))
        oracle.epoch = str(resume_state.get("epoch_digest"))
        oracle.bridge_chain = list(resume_state.get("bridge_digests", []))
        row_digests = list(resume_state.get("row_digests", [])); chunks = list(resume_state.get("row_chunks", []))
        initial_terminals = list(resume_state.get("initial_terminal_records", []))
        samples = list(resume_state.get("samples", []))
        sample_rows = {int(key): value for key, value in resume_state.get("sample_rows", {}).items()}
        phase = resume_state.get("queue_phase", {})
        queue = [int(index) for index in resume_state.get("queue", [])]
        actions = list(phase.get("actions", [])); action_event_chain = list(phase.get("action_event_chain", []))
        matrix = {str(key): value for key, value in phase.get("matrix", {}).items()}
        inverse_checks = dict(phase.get("inverse_laws", {}))
        cursor = int(resume_state.get("queue_head", 0))
        require(all(0 <= index < len(oracle.basis.k_items) for index in queue),
                "checkpoint:queue_item_registry")
        require(queue_phase_snapshot(queue, cursor, actions, matrix, inverse_checks,
                                     action_event_chain) == phase,
                "checkpoint:queue_phase_restore")
    oracle.row_digests = row_digests; oracle.row_chunks = chunks
    oracle.samples = samples; oracle.sample_rows = sample_rows
    resume_row = 1 if resume_state is None else int(resume_state.get("next_row", 0))
    require(1 <= resume_row <= ROWS + 1, "checkpoint:next_row_range")
    if resume_state is not None:
        require((not chunks and resume_row == 1) or
                (chunks and int(chunks[-1]["end"]) == resume_row - 1),
                "checkpoint:row_chunk_cursor")
        chunk_start = 1 if not chunks else int(chunks[-1]["end"]) + 1
        require(chunk_start == resume_row, "checkpoint:row_chunk_next_start")
    checkpoint_writes_enabled = resume_state is None

    def consume_row(ordinal: int, row: dict[str, Any]) -> None:
        meter.state(f"ROW_{ordinal}"); source_word, parts, ancestry = replay_ancestry(row)
        # One structural row-piece charge per literal row; the ten typed
        # affine products are a separate work counter.  Charging inside the
        # context loop used to report 10*19,408 against the 30,000 structural
        # cap.
        piece_count = 4 if row["layer"] == "action" else len(parts)
        meter.bump("row_piece_products", piece_count, "row_piece_structure")
        meter.bump("typed_context_products", 10 * piece_count, "row_piece_context")
        assembled_states: list[AffineState] = []
        for index in range(10):
            state = runtime.identity(index)
            if row["layer"] == "action":
                letter = int(row["letter"]); action_state = runtime.actors[index, -letter if int(row["orientation"]) == 1 else letter]
                state = state.mul(action_state)
                record_part = parts[0]
                state = state.mul(dag_forward.state(record_part, index))
                state = state.mul(runtime.actors[index, letter if int(row["orientation"]) == 1 else -letter])
                state = state.mul(dag_forward.state(parts[1], index))
            else:
                for part in parts:
                    state = state.mul(dag_forward.state(part, index))
            require(state.identity_roof(), "row:roof_identity")
            assembled_states.append(state)
        assembled = runtime.row_from_states(assembled_states); meter.bump("row_assemblies", 1, "row_assembly")
        meter.bump("literal_comparisons", len(source_word), "literal_word_compare")
        # The ten states above are the exact DAG result for this authenticated
        # word.  Factor the task198 bridge trace from that live state now; no
        # second flat evaluator is permitted for the 6,441-row corpus.
        bridge_trace = bridge_trace_from_states(authority, assembled_states, source_word, row, meter)
        oracle.bridge_chain.append(bridge_trace["bridge_trace_digest"])
        row_value = {"ordinal": ordinal, "layer": row["layer"], "word": list(source_word), "row": assembled}
        row_digests.append(digest(row_value))
        if ordinal in {1024, 2048, 3072, 4096, 5120, 6144, 6441}:
            chunks.append({"start": chunk_start, "end": ordinal,
                           "sha256": digest(row_digests[chunk_start - 1:ordinal])})
            chunk_start = ordinal + 1
        if ordinal - 1 in sample_indices:
            direct = runtime.states_direct(source_word); require(runtime.row_from_states(direct) == assembled,
                                                               "row:fixed_direct_canary")
            samples.append({"ordinal": ordinal, "word": list(source_word), "row_digest": digest(assembled)})
            sample_rows[ordinal] = {"word": tuple(source_word), "row": assembled}
        query = oracle.query(assembled, {}, source_word, f"R:{ordinal}")
        initial_terminals.append(compact_terminal_record(query))
        if query["schema"] == "ZERO_CORRELATION/K_RANK_RISE":
            node = words.source(source_word, {})
            item = accept_k(oracle, runtime, ledger, words, query, node, f"K:{len(oracle.basis.k_items)}", meter)
            queue.append(len(oracle.basis.k_items) - 1)
        if checkpoint_path is not None and checkpoint_writes_enabled and ordinal in {1024, 2048, 3072, 4096, 5120, 6144, ROWS}:
            write_checkpoint(checkpoint_path, authority, meter, ordinal + 1, oracle, words, queue, 0,
                             queue_phase_snapshot(queue, 0, actions, matrix, inverse_checks,
                                                  action_event_chain))
    if resume_state is not None:
        require(0 <= cursor <= len(queue) and cursor == int(resume_state.get("queue_head", 0)),
                "checkpoint:queue_head_range")
        validate_queue_prefix(oracle.basis, ledger, runtime, oracle.records, queue, cursor,
                              actions, matrix, action_event_chain)
        rebuilt = checkpoint_payload(authority, meter, resume_row, oracle, words, queue, cursor,
                                     queue_phase_snapshot(queue, cursor, actions, matrix, inverse_checks,
                                                          action_event_chain))
        require(rebuilt["rebuild_digest"] == resume_state.get("rebuild_digest"),
                "checkpoint:deterministic_rebuild_mismatch")
        meter.validation_bump(len(resume_state.get("word_ledger_dag", [])) +
                             len(resume_state.get("insertion_events", [])) +
                             len(resume_state.get("oracle_records", [])) +
                             len(resume_state.get("queue_phase", {}).get("actions", [])) + 1,
                             "checkpoint.restore_state")
        require(meter.pending_completed_counters is not None and meter.pending_saved_validation is not None,
                "checkpoint:pending_counter_state")
        meter.install_completed(meter.pending_completed_counters, dict(meter.restore_validation_counters),
                                meter.pending_saved_peak)
        checkpoint_writes_enabled = True
    for ordinal, row in enumerate(authority.rows[resume_row - 1:], resume_row):
        consume_row(ordinal, row)
    require(len(initial_terminals) == ROWS and len(row_digests) == ROWS and len(chunks) == 7,
            "row:complete_stream")
    bridge_digests = list(oracle.bridge_chain)
    expected_bridge = authority.receipt.get("bridge", {}).get("relator_replay", {})
    require(len(bridge_digests) == ROWS and expected_bridge.get("count") == ROWS and
            expected_bridge.get("all_left_and_right_inverses") is True and
            digest(bridge_digests) == expected_bridge.get("digest_sha256"),
            "bridge:relator_replay_owner")
    bridge_summary = {"count": len(bridge_digests), "digest_sha256": digest(bridge_digests),
                      "all_left_and_right_inverses": True,
                      "prefix_canary": digest(bridge_digests)}
    if resume_state is None:
        cursor = 0

    def run_queue(stop_at: int | None = None) -> None:
        nonlocal cursor
        while cursor < len(queue) and (stop_at is None or cursor < stop_at):
            parent_index = queue[cursor]; cursor += 1; parent = oracle.basis.k_items[parent_index]
            meter.state(f"K_QUEUE_{cursor}")
            for letter in (1, -1, 2, -2):
                structural_word = word_mul((letter,), tuple(parent["word"]), (-letter,))
                candidate_node = words.conjugate(letter, parent["word_node"])
                candidate_word = words.materialize(candidate_node)
                require(candidate_word == structural_word, "action:word_dag")
                candidate_rep = translated_row(parent["row"], runtime, letter)
                candidate_E = ledger.action(parent["discrepancy"], [runtime.actors[i, letter].a for i in range(10)])
                query = oracle.query(candidate_rep, candidate_E, candidate_word, f"A:{parent['label']}:{letter}")
                if query["schema"] == "MEMBER":
                    column = action_column(oracle.basis, query)
                    replay_action_projection(oracle.basis, ledger, candidate_rep, query, column)
                    matrix[str(letter)][parent["label"]] = column
                elif query["schema"] == "ZERO_CORRELATION/K_RANK_RISE":
                    item = accept_k(oracle, runtime, ledger, words, query, candidate_node,
                                    f"K:{len(oracle.basis.k_items)}", meter)
                    column = action_column(oracle.basis, query, item["label"])
                    replay_action_projection(oracle.basis, ledger, candidate_rep, query, column)
                    matrix[str(letter)][parent["label"]] = column; queue.append(len(oracle.basis.k_items) - 1)
                else:
                    raise HardStop("closure:unexpected_boundary_terminal")
                action_value = {"parent": parent["label"], "letter": letter,
                                "terminal_id": len(oracle.records) - 1,
                                "basis_column": matrix[str(letter)][parent["label"]]}
                if query["schema"] == "ZERO_CORRELATION/K_RANK_RISE":
                    action_value["candidate_node"] = item["candidate_node"]
                actions.append(action_value)
                action_event_chain.append({"index": len(action_event_chain) + 1,
                                           "query_id": query["query_id"],
                                           "digest": digest(actions[-1])})
                meter.bump("queue_actions", 1, "K_action")
            if checkpoint_path is not None and checkpoint_writes_enabled and queue_checkpoint_due(cursor, len(queue)):
                write_checkpoint(checkpoint_path, authority, meter, ROWS + 1, oracle, words, queue, cursor,
                                 queue_phase_snapshot(queue, cursor, actions, matrix, inverse_checks,
                                                      action_event_chain))

    run_queue()
    require(cursor == len(queue) and queue, "closure:queue_exhaustion")
    queue_state = {"accepted": len(queue), "cursor": cursor, "next": cursor}
    rank = len(oracle.basis.k_items)
    for item in oracle.basis.k_items:
        require(oracle.basis.k_rows.get(item["label"]) == item.get("row"), "closure:K_row_owner")
    labels = {item["label"] for item in oracle.basis.k_items}
    validate_action_matrix(matrix, labels, "closure:complete_action_column")
    for letter in matrix: require(set(matrix[letter]) == labels,
                                  "closure:complete_action_column")
    identity = {item["label"]: {item["label"]: 1} for item in oracle.basis.k_items}
    inverse_checks = {}
    for positive, negative in (("1", "-1"), ("2", "-2")):
        require(compose_matrix(matrix[positive], matrix[negative]) == identity and
                compose_matrix(matrix[negative], matrix[positive]) == identity, "closure:inverse_laws")
        inverse_checks[positive + negative] = True; inverse_checks[negative + positive] = True
    if checkpoint_path is not None and checkpoint_writes_enabled:
        write_checkpoint(checkpoint_path, authority, meter, ROWS + 1, oracle, words, queue, cursor,
                         queue_phase_snapshot(queue, cursor, actions, matrix, inverse_checks,
                                              action_event_chain))
    require(all(scale_row(item["row"], 3) == {} for item in oracle.basis.k_items), "closure:order_three")
    if rank >= 2:
        a, b = oracle.basis.k_items[:2]; direct_ab = runtime.states_direct(word_mul(a["word"], b["word"]))
        direct_ba = runtime.states_direct(word_mul(b["word"], a["word"]))
        require([(element_blob(x.a).hex(), local_to_row(x.u, i)) for i, x in enumerate(direct_ab)] ==
                [(element_blob(x.a).hex(), local_to_row(x.u, i)) for i, x in enumerate(direct_ba)],
                "closure:fixed_direct_commutation_canary")
    anchor = build_anchor(runtime, ledger, oracle.basis, words, meter)
    LIVE_STATE.update({"authority": authority, "runtime": runtime, "forward": dag_forward,
                       "ledger": ledger, "oracle": oracle, "basis": oracle.basis,
                       "words": words, "queue": queue, "actions": actions,
                       "action_matrices": matrix, "anchor": anchor,
                       "samples": samples, "sample_rows": sample_rows,
                       "queue_cursor": cursor, "queue_state": queue_state,
                       "action_event_chain": action_event_chain,
                       "bridge_digests": bridge_digests,
             "row_digests": row_digests, "meter": meter})
    return {"initial": {"count": ROWS, "terminal_digest": digest(initial_terminals),
                         "member_count": sum(x["schema"] == "MEMBER" for x in initial_terminals),
                         "rank_rise_count": sum(x["schema"] == "ZERO_CORRELATION/K_RANK_RISE" for x in initial_terminals)},
             "row_stream": {"sha256": digest(row_digests), "chunks": chunks, "samples": samples},
            "bridge": bridge_summary,
            "K_roster": public_k_roster(oracle.basis.k_items), "actions": actions,
            "action_matrices": matrix, "inverse_laws": inverse_checks,
            "queue": {"accepted": len(queue), "cursor": cursor, "next": cursor},
             "boundary": {"seed_count": len(ledger.seeds), "rank": len(oracle.basis.b_rows),
                          "epoch_digest": oracle.epoch, "record_count": len(oracle.records),
                          "terminal_digest": digest(oracle.records),
                          "event_digest": digest(oracle.event_chain),
                          "pure_B_roster": pure_boundary_roster(oracle.basis),
                          "mixed_basis": oracle.basis.b_rows},
            "anchor_diagnostics": anchor,
            "word_dag": {"nodes": len(words.nodes), "persistent": True, "memoized_psi": True,
                          "pre_expansion_cap": words.cap},
            "inventory": {**inventory, "prefix_edges": len(dag_forward.nodes) - 1},
            "basis_algorithm": "v272-lazy-full-D-v273-ledger-v274-active-dual-v282-forward-DAG",
            "complete": True}


def pure_boundary_roster(basis: LiveBasis) -> list[dict[str, Any]]:
    events = {event["label"]: event for event in basis.insertion_events if event.get("kind") == "B"}
    result = []
    for index, pivot in enumerate(basis.boundary.pivots):
        label = basis.boundary.labels[pivot]; event = events.get(label)
        require(event is not None, "boundary:pure_roster_event")
        require(label == f"B:{index}" and event["boundary_pivot"] == pivot,
                "boundary:pure_roster_order")
        result.append({"label": label, "pivot": pivot, "column": event["column"],
                       "raw_identity": event["raw_identity"], "boundary_row": basis.boundary.rows[pivot],
                       "boundary_reduction": event["boundary_reduction"],
                       "boundary_scale": event["boundary_scale"],
                       "boundary_ledger": basis.boundary_ledgers[label],
                       "combined_row": event["combined_row"],
                       "combined_formal": [basis.b_formals[label][0], basis.b_formals[label][1]]})
    return result


def public_k_roster(items: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Export semantic K owners, never process-local DAG node ids.

    The lossless node ids remain checkpoint-internal and are validated by the
    recurrence restore path.  The receipt carries the literal candidate and
    recurrence owners instead, so a consumer cannot silently accept an
    unchecked producer-local identifier.
    """
    result: list[dict[str, Any]] = []
    for source in items:
        item = dict(source); item.pop("word_node", None); item.pop("candidate_node", None)
        ancestry = dict(item.get("ancestry", {})); ancestry.pop("candidate_node", None)
        item["ancestry"] = ancestry; result.append(item)
    return result


def translated_row(row: dict[str, int], runtime: Runtime, letter: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for key, coefficient in row.items():
        context, component, text = split_row_key(key); q = runtime.quotient(context)
        moved = q.mul(runtime.actors[context, letter].a, decode_token(text)); new = row_key(context, component, moved)
        out[new] = (out.get(new, 0) + int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def write_atomic(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".v5-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        # A durable replace requires the containing directory to be synced as
        # well as the file.  Keep this POSIX path explicit; Windows is already
        # fail-closed for physical input identity above.
        if os.name != "nt":
            directory_fd = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        else:
            # Windows has no portable directory-fd fsync.  Flush the handle
            # for the replaced file and fail closed if that contract is not
            # available; a bare os.replace is not a durable owner.
            try:
                msvcrt = __import__("msvcrt")
                kernel = ctypes.WinDLL("kernel32", use_last_error=True)
                kernel.FlushFileBuffers.argtypes = [ctypes.c_void_p]
                kernel.FlushFileBuffers.restype = ctypes.c_int
                sync_fd = os.open(str(path), os.O_RDONLY | getattr(os, "O_BINARY", 0))
                try:
                    handle = ctypes.c_void_p(msvcrt.get_osfhandle(sync_fd))
                    if not kernel.FlushFileBuffers(handle):
                        raise InputStop("atomic:windows_flush_unavailable")
                finally:
                    os.close(sync_fd)
            except InputStop:
                raise
            except Exception as exc:
                raise InputStop("atomic:windows_flush_unavailable") from exc
    except Exception:
        try: os.unlink(temporary)
        except OSError: pass
        raise


def seal(value: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    body = dict(value); body.pop("self_digest_sha256", None); body["self_digest_sha256"] = digest(body)
    return body, canon(body)


def write_sealed(path: Path, value: dict[str, Any], meter: Meter | None = None,
                 terminal_transport: bool = False) -> None:
    base = dict(value); base.setdefault("serialization", {"canonicalization": True, "atomic": True})
    if meter is None:
        _, encoded = seal(base); write_atomic(path, encoded); return
    if terminal_transport:
        # Normal semantic caps may already be exhausted.  Use only the
        # reserved, bounded terminal counters while still recording the exact
        # physical envelope size and the canonicalization work used to make
        # it.  The small fixed-point loop accounts for counter digit growth.
        output_size = 0; final_charged = False
        for _ in range(16):
            meter.terminal_bump("terminal_canonicalization", 1,
                                "terminal.transport.canonicalization")
            body = dict(base)
            body["serialization"] = {
                "canonicalization": True, "atomic": True, "terminal_transport": True,
                "terminal_canonicalization": int(meter._value("terminal_canonicalization")),
                "serialized_work_bytes": int(meter._value("terminal_serialized_bytes")),
                "output_bytes": output_size,
                "final_write": int(meter._value("terminal_final_write")) + (0 if final_charged else 1)}
            body["resource"] = meter.public(strict=False)
            _, encoded = seal(body); desired = len(encoded)
            require(desired <= OBJECT_CAPS["checkpoint_current_bytes"],
                    "serialize:terminal_transport_object_cap")
            if desired != output_size:
                output_size = desired; continue
            serialized_total = int(meter._value("terminal_serialized_bytes"))
            if desired > serialized_total:
                meter.terminal_bump("terminal_serialized_bytes", desired - serialized_total,
                                    "terminal.transport.serialized_bytes")
                continue
            if not final_charged:
                meter.terminal_bump("terminal_final_write", 1,
                                    "terminal.transport.final_write")
                final_charged = True; continue
            require(body["serialization"]["output_bytes"] == desired and
                    body["serialization"]["serialized_work_bytes"] ==
                    int(meter._value("terminal_serialized_bytes")) and
                    body["serialization"]["final_write"] ==
                    int(meter._value("terminal_final_write")),
                    "serialize:terminal_transport_accounting")
            write_atomic(path, encoded); return
        raise HardStop("serialize:terminal_transport_fixed_point_unstable")
    # Reserve the one physical write before taking the resource snapshot so
    # the sealed receipt cannot omit that transition.  serialized_bytes is a
    # separate additive work counter; the bounded fixed point below charges
    # the exact final envelope length, including its own counter digits.
    meter.reserve("final_write", 1, "atomic_final_write")
    meter.bump("final_write", 1, "atomic_final_write")
    start = int(meter._value("serialized_bytes")); charged = 0; output_size = 0
    for _ in range(16):
        meter.bump("canonicalization", 2, "serialize.canonicalization")
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
        _, encoded = seal(body); desired = len(encoded)
        require(desired <= OBJECT_CAPS["checkpoint_current_bytes"],
                "serialize:output_object_cap")
        if desired != output_size:
            output_size = desired; continue
        if charged != desired:
            require(desired >= charged, "serialize:fixed_point_shrunk")
            delta = desired - charged
            meter.reserve("serialized_bytes", delta, "serialize_before_seal")
            meter.bump("serialized_bytes", delta, "serialize_before_seal")
            charged = desired; continue
        require(body["serialization"]["canonicalization_count"] ==
                int(meter._value("canonicalization")) and
                body["serialization"]["output_bytes"] == desired and
                int(meter._value("serialized_bytes")) == start + charged,
                "serialize:fixed_point_counter")
        write_atomic(path, encoded); return
    raise HardStop("serialize:fixed_point_unstable")


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


def checkpoint_payload(authority: AuthorityAdapter, meter: Meter, next_row: int,
                       oracle: Oracle, words: WordDAG, queue: list[int], cursor: int,
                       queue_phase: dict[str, Any] | None = None) -> dict[str, Any]:
    basis = oracle.basis
    meter.completed_counters = dict(meter.semantic_counters); meter._sync()
    row_digests = list(getattr(oracle, "row_digests", []))
    phase = queue_phase or {"queue_head": cursor, "queue_length": len(queue),
                            "action_count": 0, "actions": [], "action_event_chain": [],
                            "matrix": {str(x): {} for x in (1, -1, 2, -2)},
                            "matrix_digest": digest({str(x): {} for x in (1, -1, 2, -2)}),
                            "inverse_laws": {}}
    body = {"schema": SCHEMA + "/checkpoint/v1", "owner": "producer", "authority": authority.identity,
            "counter_registry": dict(COUNTER_TYPES),
            "code_sha256": sha(Path(__file__).read_bytes()), "next_row": next_row,
            "next_query": len(oracle.records), "B_roster": basis.b_rows,
            "B_ledgers": basis.b_ledgers, "boundary_ledgers": basis.boundary_ledgers,
            "combined_ledgers": basis.combined_ledgers, "B_coefficients": basis.b_coefficients,
            "B_formals": {label: [q, c] for label, (q, c) in basis.b_formals.items()},
            "K_roster": basis.k_items,
            "boundary_echelon": {"pivots": basis.boundary.pivots, "rows": basis.boundary.rows,
                                 "labels": basis.boundary.labels},
            "echelon_rebuild": {"pivots": basis.combined.pivots, "rows": basis.combined.rows,
                                 "labels": basis.combined.labels},
            "insertion_events": basis.insertion_events,
            "active_registry": sorted(basis.active_registry),
            "queue": queue, "queue_head": cursor,
            "word_ledger_dag": [{key: value for key, value in node.items() if key not in ("states",)}
                                for node in words.nodes],
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


def write_checkpoint(path: Path, authority: AuthorityAdapter, meter: Meter, next_row: int,
                     oracle: Oracle, words: WordDAG, queue: list[int], cursor: int,
                     queue_phase: dict[str, Any] | None = None) -> None:
    def make_body() -> dict[str, Any]:
        return checkpoint_payload(authority, meter, next_row, oracle, words, queue, cursor, queue_phase)
    write_checkpoint_snapshot(path, meter, make_body, "checkpoint_serialize")


def write_checkpoint_snapshot(path: Path, meter: Meter, make_body: Any, phase: str) -> None:
    """Charge the complete sealed snapshot with a bounded fixed point.

    checkpoint_total_bytes is an additive semantic counter, so its own transition
    must be present in the authenticated body.  The byte length can change by
    a digit when that counter is inserted; at most four bounded passes are
    permitted to reach the fixed point.
    """
    start = int(meter._value("checkpoint_total_bytes")); charged = 0
    for _ in range(16):
        meter.bump("canonicalization", 2, phase)
        body = make_body(); raw = canon(body)
        sealed = dict(body); sealed["self_digest_sha256"] = sha(raw)
        encoded = canon(sealed); desired = len(encoded)
        require(desired <= OBJECT_CAPS["checkpoint_current_bytes"], "checkpoint:current_object_cap")
        prior_peak = int(meter._value("checkpoint_peak_bytes"))
        if desired > prior_peak:
            meter.bump("checkpoint_peak_bytes", desired, phase)
            continue
        require(desired >= charged, "checkpoint:fixed_point_shrunk")
        delta = desired - charged
        if delta:
            meter.reserve("checkpoint_total_bytes", delta, phase)
            meter.bump("checkpoint_total_bytes", delta, phase)
            charged += delta
            continue
        require(int(meter._value("checkpoint_total_bytes")) == start + charged,
                "checkpoint:fixed_point_counter")
        write_atomic(path, encoded)
        return
    raise HardStop("checkpoint:fixed_point_unstable")


def write_prefrontier_checkpoint(path: Path, authority: AuthorityAdapter, meter: Meter) -> None:
    """Install an atomic empty state before any row/resource work begins."""
    phase = {"queue_head": 0, "queue_length": 0, "action_count": 0, "actions": [],
             "action_event_chain": [], "matrix": {str(x): {} for x in (1, -1, 2, -2)},
             "matrix_digest": digest({str(x): {} for x in (1, -1, 2, -2)}), "inverse_laws": {}}
    body = {"schema": SCHEMA + "/checkpoint/v1", "owner": "producer", "authority": authority.identity,
            "counter_registry": dict(COUNTER_TYPES),
            "code_sha256": sha(Path(__file__).read_bytes()), "next_row": 1,
            "next_query": 0, "B_roster": {}, "B_ledgers": {},
            "boundary_ledgers": {}, "combined_ledgers": {}, "B_coefficients": {},
            "B_formals": {}, "K_roster": [],
            "boundary_echelon": {"pivots": [], "rows": {}, "labels": {}},
            "echelon_rebuild": {"pivots": [], "rows": {}, "labels": {}}, "insertion_events": [], "active_registry": [],
            "queue": [], "queue_head": 0, "word_ledger_dag": [],
            "epoch_digest": "0" * 64, "query_event_chain": [], "oracle_records": [], "live_duals": [],
            "dual_event_chain": [], "initial_terminal_chain": [], "initial_terminal_records": [],
            "row_digests": [], "row_cursor": 0, "row_replay_sha256": digest([]),
            "row_chunks": [], "samples": [], "sample_rows": {},
            "row_prefix_canary": digest({"next_row": 1, "row_cursor": 0, "row_replay_sha256": digest([])}),
            "queue_phase": phase,
            "bridge_digests": [], "bridge_cursor": 0,
            "bridge_replay_sha256": digest([]),
            "bridge_prefix_canary": digest({"next_row": 1, "bridge_cursor": 0,
                                               "bridge_replay_sha256": digest([])}),
            "counters": dict(meter.counters), "completed_counters": dict(meter.semantic_counters),
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
    write_checkpoint_snapshot(path, meter, make_body, "prefrontier_checkpoint")


def restore_checkpoint(path: Path, authority: AuthorityAdapter, meter: Meter) -> dict[str, Any]:
    checked = checkpoint_input(path, "CHECKPOINT_RESUME")
    raw = read_once(checked, (checked.as_posix().replace(ROOT.as_posix() + "/", ""),
                              int(os.lstat(checked).st_size), ""), meter,
                    "checkpoint.resume")
    require(len(raw) <= OBJECT_CAPS["checkpoint_current_bytes"], "checkpoint:cap")
    value = json.loads(raw.decode("ascii")); claimed = value.pop("self_digest_sha256", None)
    require(claimed == digest(value), "checkpoint:seal")
    require(value.get("schema") == SCHEMA + "/checkpoint/v1" and value.get("authority") == authority.identity and
            value.get("owner") == "producer" and
            value.get("code_sha256") == sha(Path(__file__).read_bytes()), "checkpoint:identity")
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
                for number in mapping.values()), "checkpoint:counters")
    require(value.get("counter_digest") == checkpoint_counter_digest(value),
            "checkpoint:counter_digest")
    current_validation = dict(meter.restore_validation_counters)
    meter.validation_bump(1, "checkpoint.restore_validate")
    merged_validation = {key: int(restore_counters.get(key, 0)) + int(current_validation.get(key, 0))
                         for key in set(restore_counters) | set(current_validation)}
    merged_validation["restore_validation"] = merged_validation.get("restore_validation", 0) + 1
    meter.restore_validation_counters = dict(merged_validation); meter._sync()
    meter.pending_completed_counters = dict(completed_counters)
    meter.pending_saved_validation = merged_validation
    meter.pending_saved_peak = dict(peak_counters)
    meter.host_history = list(host_history) + [dict(host_counters)]
    require(checkpoint_next_state_canary(value) == value.get("next_state_canary"),
            "checkpoint:next_state_canary")
    require(value.get("bridge_cursor") == len(value.get("bridge_digests", [])) and
            value.get("bridge_replay_sha256") == digest(value.get("bridge_digests", [])) and
            value.get("bridge_prefix_canary") == digest({"next_row": value["next_row"],
                                                           "bridge_cursor": value["bridge_cursor"],
                                                           "bridge_replay_sha256": value["bridge_replay_sha256"]}),
             "checkpoint:bridge_prefix")
    require(value.get("row_cursor") == len(value.get("row_digests", [])) and
            value.get("row_cursor") == int(value.get("next_row", 0)) - 1 and
            value.get("row_replay_sha256") == digest(value.get("row_digests", [])) and
            value.get("row_prefix_canary") == digest({"next_row": value["next_row"],
                                                         "row_cursor": value["row_cursor"],
                                                         "row_replay_sha256": value["row_replay_sha256"]}),
             "checkpoint:row_prefix")
    row_prefix = value.get("row_digests", []); chunks = value.get("row_chunks", []); prior_end = 0
    require(isinstance(chunks, list), "checkpoint:row_chunks_shape")
    for chunk in chunks:
        start = int(chunk.get("start", 0)); end = int(chunk.get("end", 0))
        require(start == prior_end + 1 and start <= end <= len(row_prefix) and
                chunk.get("sha256") == digest(row_prefix[start - 1:end]),
                "checkpoint:row_chunk_prefix")
        prior_end = end
    require(prior_end == len(row_prefix), "checkpoint:row_chunk_cursor")
    records = value.get("oracle_records", []); events = value.get("query_event_chain", [])
    require(isinstance(records, list) and isinstance(events, list) and len(records) == len(events) == int(value["next_query"]),
            "checkpoint:oracle_event_prefix")
    for record, event in zip(records, events):
        require(event.get("query_id") == record.get("query_id") and event.get("schema") == record.get("schema") and
                event.get("digest") == digest(record), "checkpoint:oracle_event_digest")
    require(value.get("initial_terminal_records") == [record for record in records
            if is_row_terminal(record)], "checkpoint:initial_terminal_records")
    require(value.get("initial_terminal_chain") == [event for event in events
            if is_row_terminal(event)], "checkpoint:initial_terminal_chain")
    epoch = "0" * 64
    for record in records: epoch = sha((epoch + digest(record)).encode("ascii"))
    require(value.get("epoch_digest") == epoch, "checkpoint:epoch_chain")
    duals = value.get("live_duals", []); dual_events = value.get("dual_event_chain", [])
    # Full historical dual vectors are intentionally not checkpoint owners;
    # one actual sample is retained and the chronological digest chain is
    # sufficient for continuation validation.
    require(isinstance(duals, list) and isinstance(dual_events, list) and
            len(duals) == (1 if dual_events else 0), "checkpoint:dual_event_prefix")
    for index, event in enumerate(dual_events, 1):
        require(event.get("index") == index and isinstance(event.get("query_id"), str) and
                isinstance(event.get("digest"), str) and len(event["digest"]) == 64,
                "checkpoint:dual_event_chain")
    if duals:
        dual = duals[0]; event = dual_events[0]
        dual_digest = digest({"query_id": dual.get("query_id"), "dual": sorted(dual.get("dual", {}).items()),
                              "target": dual.get("target"), "target_dot": dual.get("target_dot"),
                              "correlation": dual.get("correlation")})
        require(event.get("query_id") == dual.get("query_id") and
                event.get("digest") == dual_digest, "checkpoint:dual_event_digest")
    phase = value.get("queue_phase", {}); require(isinstance(phase, dict) and
             phase.get("action_count") == len(phase.get("actions", [])) and
             phase.get("matrix_digest") == digest(phase.get("matrix", {})) and
             phase.get("action_count") == len(phase.get("action_event_chain", [])),
             "checkpoint:queue_phase_state")
    queue = value.get("queue", []); actions = phase.get("actions", []); action_events = phase.get("action_event_chain", [])
    require(phase.get("queue_head") == value.get("queue_head") and
            phase.get("queue_length") == len(queue) and
            len(actions) == 4 * int(value.get("queue_head", 0)), "checkpoint:queue_action_prefix")
    for action, event in zip(actions, action_events):
        require(event.get("digest") == digest(action) and int(action.get("letter", 0)) in (-2, -1, 1, 2) and
                isinstance(action.get("parent"), str), "checkpoint:action_event_prefix")
    require(value.get("rebuild_digest") == checkpoint_state_digest(value),
            "checkpoint:rebuild_digest")
    return value


def owner_specs() -> list[dict[str, Any]]:
    stages = ["authority", "authority", "authority", "authority", "authority", "authority", "authority",
              "echelon", "echelon", "checker", "ancestry", "boundary", "dual", "closure", "anchor", "anchor",
              "resource", "terminal", "terminal", "driver", "ancestry", "trie", "trie", "ancestry", "ancestry",
              "checker", "boundary", "boundary", "boundary", "boundary", "boundary", "boundary", "boundary",
              "dual", "dual", "discrepancy", "discrepancy", "discrepancy", "discrepancy", "discrepancy",
              "discrepancy", "discrepancy", "dual", "dual", "dual", "dual", "dual", "dual", "dual"]
    return [{"name": name, "owner": OWNERS[name], "stage": stages[i]}
            for i, name in enumerate(MUTATIONS)]


def owner_digest(value: Any) -> str:
    return sha(canon(jsonable(value)))


class OwnerRoute:
    """A live owner slot with an explicit narrow normal-stage validator."""
    def __init__(self, owner: str, stage: str, read: Any, write: Any,
                 mutate: Any, validate: Any):
        self.owner, self.stage, self.read, self.write = owner, stage, read, write
        self.mutate, self.validate = mutate, validate

    def exercise(self, name: str, expected: dict[str, Any] | None = None) -> dict[str, Any]:
        # Read and hash the narrow live slot, install the mutation into that
        # same owner, then observe the installed slot again.  In particular,
        # do not compare a detached mutant (or deepcopy a result transcript).
        require(isinstance(expected, dict) and
                set(expected) == {"normal_validator", "first_rejection"} and
                expected.get("normal_validator") == self.stage and
                isinstance(expected.get("first_rejection"), str) and expected["first_rejection"],
                "selftest:expected_rejection_registry:" + self.owner)
        old = self.read(); before = owner_digest(old); mutant = self.mutate(old)
        self.write(mutant)
        after = owner_digest(self.read()); require(before != after, "selftest:owner_unchanged:" + self.owner)
        reached = False
        try:
            reached = True
            self.validate()
        except Reject as exc:
            first_rejection = str(exc)
            require(first_rejection == expected["first_rejection"],
                    "selftest:unexpected_first_rejection:" + self.owner)
            return {"name": name, "owner": self.owner, "stage": self.stage,
                    "normal_validator": self.stage, "before_sha256": before,
                    "after_sha256": after, "reached_normal_validator": reached,
                    "first_rejection": first_rejection}
        finally:
            self.write(old)
        raise Reject("selftest:owner_not_rejected:" + self.owner)


def _slot(holder: Any, key: Any, owner: str, stage: str, mutate: Any,
          validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: holder[key],
                      lambda value: holder.__setitem__(key, value), mutate, validate)


def _flip_int(value: Any) -> int:
    require(type(value) is int, "selftest:integer_owner")
    return value + 1


def _zero_int(value: Any) -> int:
    require(type(value) is int, "selftest:integer_owner")
    return 0


def _flip_bool(value: Any) -> bool:
    require(type(value) is bool, "selftest:boolean_owner")
    return not value


def _flip_text(value: Any) -> str:
    require(isinstance(value, str), "selftest:text_owner")
    return value + "!"


def _flip_bytes(value: Any) -> bytes:
    require(isinstance(value, (bytes, bytearray)), "selftest:bytes_owner")
    changed = bytearray(value); changed[-1:] = bytes([(changed[-1] ^ 1) if changed else 1])
    return type(value)(changed)


def _flip_path(value: Any) -> Path:
    require(isinstance(value, Path), "selftest:path_owner")
    return Path(str(value) + ".mutated")


def _append_bad_word(value: Any) -> list[int]:
    require(isinstance(value, (list, tuple)), "selftest:word_owner")
    return list(value) + [3]


def _invalid_orientation(value: Any) -> int:
    require(type(value) is int, "selftest:orientation_owner")
    return 7 if value != 7 else 6


def _drop_first(value: Any) -> list[Any]:
    require(isinstance(value, list) and value, "selftest:list_owner")
    return list(value[1:])


def _bad_mapping(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "selftest:mapping_owner")
    out = dict(value); out["__v5_mutation__"] = 1; return out


def _flip_sparse_coefficient(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and value, "selftest:sparse_owner")
    out = dict(value); key = next(iter(out)); out[key] = 1 if int(out[key]) == 2 else 2
    return out


def _omit_sparse_entry(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and value, "selftest:nonempty_sparse_owner")
    out = dict(value); out.pop(next(iter(out))); return out


def _mutate_selected(value: Any) -> list[Any]:
    # The selected support occurrence is an actual correlation owner.  Retain
    # its typed shape while changing its coefficient so the normal support /
    # ZERO validator, rather than a generic equality check, rejects it.
    if value is None: return [0, 0, "00", 1]
    require(isinstance(value, list) and len(value) == 4, "selftest:selected_owner")
    out = list(value); out[3] = 1 if int(out[3]) == 2 else 2; return out


def _set_remove(value: Any) -> set[str]:
    require(isinstance(value, set) and value, "selftest:active_registry_owner")
    out = set(value); out.remove(next(iter(out))); return out


def _set_route(holder: Any, owner: str, stage: str, mutate: Any,
               validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: set(holder),
                      lambda value: (holder.clear(), holder.update(value)), mutate, validate)


def _mapping_remove(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and value, "selftest:nonempty_mapping_owner")
    out = dict(value); out.pop(next(iter(out))); return out


def _mapping_route(holder: Any, owner: str, stage: str, mutate: Any,
                   validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: dict(holder),
                      lambda value: (holder.clear(), holder.update(value)), mutate, validate)


def _list_route(holder: list[Any], owner: str, stage: str, mutate: Any,
                validate: Any) -> OwnerRoute:
    return OwnerRoute(owner, stage, lambda: list(holder),
                      lambda value: (holder.__setitem__(slice(None), value)), mutate, validate)


def producer_owner_routes(authority: AuthorityAdapter, normal: dict[str, Any]) -> dict[str, OwnerRoute]:
    live = LIVE_STATE; require(live.get("basis") is not None, "selftest:live_kernel_missing")
    runtime: Runtime = live["runtime"]; ledger: BoundaryLedger = live["ledger"]
    oracle: Oracle = live["oracle"]; basis: LiveBasis = live["basis"]
    words: WordDAG = live["words"]; forward: ForwardDAG = live["forward"]
    anchor = live["anchor"]; matrices = live["action_matrices"]
    queue = live["queue"]; actions = live["actions"]; sample_rows = live["sample_rows"]
    require(basis.k_items and oracle.live_duals, "selftest:owner_precondition:K_or_dual")
    first_item = basis.k_items[0]; first_dual = oracle.live_duals[0]
    first_corr = first_dual["correlation"]
    candidate_item = next((item for item in basis.k_items if item.get("candidate_E")), None)
    prior_item = next((item for item in basis.k_items if item.get("discrepancy")), None)
    translation_item = next((item for item in basis.k_items if item.get("c")), None)
    require(candidate_item is not None, "selftest:owner_precondition:candidate_E")
    require(prior_item is not None, "selftest:owner_precondition:discrepancy")
    require(translation_item is not None, "selftest:owner_precondition:c")

    def check_echelon() -> None:
        require(len(basis.boundary.pivots) == len(set(basis.boundary.pivots)) and
                set(basis.boundary.pivots) == set(basis.boundary.rows), "selftest:echelon_boundary_order")
        require(set(basis.combined.pivots) == set(basis.combined.rows), "selftest:echelon_pivot_registry")
        for pivot in basis.boundary.pivots:
            label = basis.boundary.labels[pivot]; require(label in basis.boundary_ledgers, "selftest:echelon_boundary_ledger")
            require(basis.boundary.rows[pivot] == ledger.psi(basis.boundary_ledgers[label]),
                    "selftest:echelon_raw_boundary_replay")
        for pivot in basis.combined.pivots:
            label = basis.combined.labels[pivot]; require(label in basis.b_formals, "selftest:echelon_formal_label")
            q_value, c_value = basis.b_formals[label]
            replay = add_row(ledger.psi(q_value), basis.combined.replay(c_value, basis.k_rows))
            require(replay == basis.combined.rows[pivot], "selftest:echelon_formal_replay")

    def check_k() -> None:
        previous_rank = 0
        for index, item in enumerate(basis.k_items):
            label = f"K:{index}"; require(item.get("label") == label and label in basis.k_rows,
                                             "selftest:chronological_K_roster")
            require(basis.k_rows[label] == item.get("row"), "selftest:K_row_owner")
            require(item.get("rank", 0) > previous_rank and item.get("pivot") in item.get("row", {}),
                    "selftest:K_rank_pivot")
            previous_rank = int(item["rank"])
            require(isinstance(item.get("word"), list) and isinstance(item.get("discrepancy"), dict),
                    "selftest:K_owner_shape")
            require(all(int(letter) in (-2, -1, 1, 2) for letter in item["word"]),
                    "selftest:K_word_alphabet")
            for owner_name in ("discrepancy", "candidate_E", "Q"):
                value = item.get(owner_name, {})
                require(isinstance(value, dict) and
                        all(isinstance(key, str) and key.count(":") == 2 for key in value),
                        "selftest:K_raw_ledger_key:" + owner_name)
            states = runtime.states_direct(item["word"]); actual = runtime.row_from_states(states)
            require(actual == add_row(item["row"], ledger.psi(item["discrepancy"])),
                    "selftest:K_rho1_discrepancy")
            require(item.get("q") == list(h2_word(item["word"])), "selftest:K_q")
            rho0 = [element_blob(state.a).hex() for state in states]
            rho1 = [{"roof": element_blob(state.a).hex(), "fox": local_to_row(state.u, i)}
                    for i, state in enumerate(states)]
            require(item.get("rho0") == rho0 and item.get("rho1") == rho1,
                    "selftest:K_rho_projection")
            require(item.get("rho1_actual_flattened") == actual and
                    item.get("rho1_flattened") == add_row(actual, ledger.psi(item["discrepancy"]), -1),
                    "selftest:K_flattened_projection")
            require(item.get("raw_coefficients") == {label: 1},
                    "selftest:K_raw_coefficients")
            require(item.get("ancestry", {}).get("prior_labels") ==
                    sorted(item.get("c", {}).keys()), "selftest:K_prior_ancestry")
            query = next((record for record in oracle.records
                          if record.get("query_id") == item.get("ancestry", {}).get("parent_query")), None)
            require(query is not None and item.get("candidate_E") == query.get("candidate_discrepancy") and
                    item.get("Q") == query.get("Q") and item.get("c") == query.get("c") and
                    item.get("normalization_scale") == query.get("normalization_scale"),
                    "selftest:K_recurrence_owner")
            require(item.get("E_formula") == "s*(E_v+Q-sum(c_l E_l))" and
                    item.get("word_formula") == "red((W_v product_l W_l^(-c_l))^s)",
                    "selftest:K_formula_owner")

    def check_ancestry(index: int) -> None:
        replay_ancestry(authority.rows[index])

    def check_dag() -> None:
        for ident, node in enumerate(forward.nodes[1:], 1):
            parent = node.get("parent"); letter = node.get("letter")
            require(isinstance(parent, int) and parent < ident and letter in (-2, -1, 1, 2),
                    "selftest:forward_edge_owner")
            require(forward.nodes[parent]["edges"].get(letter) == ident and
                    node["length"] == forward.nodes[parent]["length"] + 1,
                    "selftest:forward_edge_orientation")
            expected = [forward.nodes[parent]["states"][i].mul(runtime.actors[i, letter]) for i in range(10)]
            require(all(left.a == right.a and left.u == right.u
                        for left, right in zip(node["states"], expected)), "selftest:forward_state_replay")

    def check_dual() -> None:
        dual = first_dual["dual"]; target = first_dual["target"]
        require(dual and first_dual["target_dot"] in (1, 2), "selftest:dual_nonzero")
        require(all(int(value) % 3 for value in dual.values()), "selftest:dual_nonzero_coefficients")
        registry = set().union(*(set(row) for row in basis.roster().values())) if basis.roster() else set()
        require(basis.active_registry == registry, "selftest:active_registry_owner")
        require(set(dual) <= registry, "selftest:dual_active_registry")
        for row in basis.combined.rows.values():
            require(sum(int(value) * dual.get(key, 0) for key, value in row.items()) % 3 == 0,
                    "selftest:dual_live_dot")
        require(sum(int(value) * dual.get(key, 0) for key, value in target.items()) % 3 != 0,
                "selftest:dual_target_dot")
        recomputed = correlate(ledger, dual, live["meter"])
        require(recomputed["pair_count"] == first_corr["pair_count"] and
                recomputed["accumulator_digest"] == first_corr["accumulator_digest"] and
                recomputed["selected"] == first_corr["selected"], "selftest:dual_correlation")

    def check_actions() -> None:
        labels = {item["label"] for item in basis.k_items}; identity = {label: {label: 1} for label in labels}
        validate_action_matrix(matrices, labels, "selftest:action_support")
        require(all(set(column) == labels for column in matrices.values()), "selftest:action_complete")
        for positive, negative in (("1", "-1"), ("2", "-2")):
            require(compose_matrix(matrices[positive], matrices[negative]) == identity and
                    compose_matrix(matrices[negative], matrices[positive]) == identity,
                    "selftest:action_inverse")

    def check_anchor() -> None:
        recomputed = h2_projection_checks(runtime, basis)
        require(anchor.get("basis_q") == recomputed, "selftest:anchor_projection")
        require(all(int(letter) in (-2, -1, 1, 2)
                    for letter in anchor.get("powered_word", [])),
                "selftest:anchor_word_alphabet")
        require(h2_word(anchor.get("powered_word", [])) == (0, 0, 3), "selftest:anchor_word")
        require(anchor.get("change_matrix") and anchor.get("inverse_change_matrix"),
                "selftest:anchor_change_matrix")
        require(compose_matrix(anchor["change_matrix"], anchor["inverse_change_matrix"]) ==
                {label: {label: 1} for label in anchor["change_matrix"]} and
                compose_matrix(anchor["inverse_change_matrix"], anchor["change_matrix"]) ==
                {label: {label: 1} for label in anchor["change_matrix"]},
                "selftest:anchor_matrix_inverse")

    def check_queue() -> None:
        require(queue and live.get("queue_cursor") == len(queue) and
                live.get("queue_state", {}).get("accepted") == len(queue) and
                all(index == position for position, index in enumerate(queue)),
                "selftest:queue_exhaustion")

    def check_sample() -> None:
        sample = sample_rows[1]; row = authority.rows[0]; source, parts, _ = replay_ancestry(row)
        states = []
        for index in range(10):
            value = runtime.identity(index)
            for part in parts: value = value.mul(forward.state(part, index))
            states.append(value)
        require(sample["word"] == source and sample["row"] == runtime.row_from_states(states),
                "selftest:sample_row_replay")

    def check_terminal() -> None:
        require(normal.get("status") == "COMPLETE" and normal.get("terminal") == PASS and
                normal.get("complete") is True, "selftest:positive_terminal")

    def check_driver() -> None:
        require(normal.get("driver_contract", {}).get("producer_terminal_lines") == 1 and
                normal["driver_contract"].get("checker_terminal_lines") == 1 and
                normal["driver_contract"].get("sentinel_last") is True,
                "selftest:driver_contract")

    def check_registry() -> None:
        check_dual(); check_k(); require(len(basis.combined.pivots) == basis.rank(), "selftest:active_registry")

    routes: dict[str, OwnerRoute] = {}
    def add(route: OwnerRoute) -> None: routes[route.owner] = route
    add(_slot(authority.rows[0], "ordinal", "authority.layer_ordinal", "authority", _zero_int, authority.validate))
    add(_slot(authority.values["manifest"], "accepted", "authority.acceptance_manifest", "authority", _flip_bool, authority.validate))
    add(_slot(authority.raw, "receipt", "authority.canonical_bytes", "authority", _flip_bytes,
              lambda: require(sha(authority.raw["receipt"]) == RECEIPT_SHA, "selftest:canonical_input_bytes")))
    add(_slot(authority.paths, "receipt", "authority.resolved_containment", "authority", _flip_path,
              lambda: exact_path(str(authority.paths["receipt"]), "ci/in", AUTH["receipt"], "selftest:path_owner")))
    proof = authority.receipt["Delta0"]["presentation"]["normal_generation_proof"]
    add(_slot(proof, "Gamma_cayley_edge_count", "authority.normal_generation_proof", "authority", _flip_int, authority.validate))
    add(_slot(authority.receipt["bridge"]["occurrence_ledger"][0], "block", "authority.bridge_occurrence_ledger", "authority", _flip_text, authority.validate))
    add(_slot(authority.receipt["evaluator"]["coordinate_widths"], 0, "authority.evaluator_abi_canary", "authority", _flip_int, authority.validate))
    add(_slot(basis.boundary.rows[basis.boundary.pivots[0]], next(iter(basis.boundary.rows[basis.boundary.pivots[0]])), "echelon.raw_boundary_replay", "echelon", _flip_int, check_echelon))
    add(_slot(basis.combined.rows[basis.combined.pivots[0]], next(iter(basis.combined.rows[basis.combined.pivots[0]])), "echelon.inherited_scale", "echelon", _flip_int, check_echelon))
    add(_slot(first_item["raw_coefficients"], next(iter(first_item["raw_coefficients"])), "checker.producer_checker_basis_change", "checker", _flip_int, check_k))
    add(_slot(authority.rows[6318]["ancestry"], "tokens", "ancestry.outer_first_conjugation", "ancestry", _append_bad_word, lambda: check_ancestry(6318)))
    add(_slot(first_item, "word", "boundary.source_word_difference", "boundary", _append_bad_word, check_k))
    add(_slot(first_dual["dual"], next(iter(first_dual["dual"])), "dual.negative_functional", "dual", _zero_int, check_dual))
    add(_slot(matrices["1"], next(iter(matrices["1"])), "closure.action_matrix", "closure", _bad_mapping, check_actions))
    add(_slot(anchor["basis_q"][0], "exponent", "anchor.projected_h2_exponent", "anchor", _flip_int, check_anchor))
    add(_slot(anchor, "powered_word", "anchor.inverse_scalar_powered_word", "anchor", _append_bad_word, check_anchor))
    add(_slot(live["meter"].limits, "wall_seconds", "resource.live_cap_witness", "resource", _zero_int,
              lambda: require(live["meter"].limits["wall_seconds"] > 0, "selftest:resource_cap")))
    add(_slot(normal, "status", "terminal.positive_status", "terminal", lambda value: UNKNOWN_INPUT, check_terminal))
    add(_slot(normal, "complete", "terminal.false_progress", "terminal", _flip_bool, check_terminal))
    add(_slot(normal["driver_contract"], "producer_terminal_lines", "driver.duplicate_markers", "driver", _flip_int, check_driver))
    add(_slot(authority.rows[0]["ancestry"], "record_word", "ancestry.section_word_replay", "ancestry", _append_bad_word, lambda: check_ancestry(0)))
    add(_slot(forward.nodes[1], "length", "trie.primitive_terminal", "trie", _flip_int, check_dag))
    edge_key = next(iter(forward.nodes[0]["edges"]))
    add(_slot(forward.nodes[0]["edges"], edge_key, "trie.forward_edge_orientation", "trie", _flip_int, check_dag))
    add(_slot(authority.rows[6318], "orientation", "ancestry.action_orientation", "ancestry", _invalid_orientation, lambda: check_ancestry(6318)))
    add(_slot(authority.rows[0]["ancestry"], "section_target_word", "ancestry.target_inverse", "ancestry", _append_bad_word, lambda: check_ancestry(0)))
    add(_slot(sample_rows[1]["row"], next(iter(sample_rows[1]["row"])), "checker.typed_row_equality", "checker", _flip_int, check_sample))
    add(_slot(ledger.seeds[0], "index", "boundary.base_seed_roster", "boundary", _flip_int,
              lambda: require([seed.index for seed in ledger.seeds] == list(range(65)), "selftest:seed_roster")))
    add(_slot(authority.receipt["bridge"]["occurrence_ledger"][0], "block", "boundary.block_tag", "boundary", _flip_text, authority.validate))
    add(_slot(first_corr, "selected", "boundary.translation_orientation", "boundary",
              lambda value: [0] if value is None else None, check_dual))
    add(_slot(matrices["-1"], next(iter(matrices["-1"])), "boundary.inverse_action_queue", "boundary", _bad_mapping, check_actions))
    add(_slot(actions[0], "parent", "boundary.parent_action_ancestry", "boundary", _flip_text,
              lambda: require(actions[0]["parent"] in {item["label"] for item in basis.k_items}, "selftest:parent_ancestry")))
    queue_state = live["queue_state"]
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
    require(set(routes) == {spec["owner"] for spec in owner_specs()}, "selftest:owner_route_registry")
    return routes


def selftest_certificate(fixture: dict[str, Any], authority: AuthorityAdapter,
                         normal: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == SELFTEST_SCHEMA and fixture.get("synthetic") is False and
            fixture.get("expected_mutation_count") == 48 and fixture.get("mutations") == owner_specs() and
            fixture.get("immutable_input_identities") == {"task198_receipt": RECEIPT_SHA,
                "task176_receipt": TASK176["receipt"][2], "q3": Q3_SOURCE[2], "e4": E4_SOURCE[2]},
            "selftest:fixture_registry")
    expected_registry = fixture.get("expected_rejections")
    require(isinstance(expected_registry, dict) and set(expected_registry) == {"producer", "checker"} and
            isinstance(expected_registry.get("producer"), dict) and
            set(expected_registry["producer"]) == set(MUTATIONS),
            "selftest:expected_rejection_registry")
    expected = expected_registry["producer"]
    routes = producer_owner_routes(authority, normal)
    records = [routes[spec["owner"]].exercise(spec["name"], expected[spec["name"]])
               for spec in owner_specs()]
    return {"schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": "SELFTEST_COMPLETE",
             "synthetic": False, "input_identities": authority.identity,
             "mutations": {"attempted": len(records), "rejected": len(records), "records": records},
             "normal_route": {"schema": normal.get("schema"), "terminal": normal.get("terminal"),
                              "owner_route_count": len(routes)}}


def actual_result(authority: AuthorityAdapter, meter: Meter, checkpoint: Path | None = None,
                  resume_state: dict[str, Any] | None = None) -> dict[str, Any]:
    runtime = Runtime(authority, meter); primitive, inventory = primitive_inventory(authority)
    forward = ForwardDAG(runtime, meter); kernel = build_kernel(authority, runtime, forward, primitive,
                                                                  inventory, meter, checkpoint, resume_state)
    meter._sync()
    resource = meter.public()
    measurement = {"status": "RUNTIME", "owner": "resource.host_counters",
                    "wall_seconds": resource["host_counters"]["wall_seconds"],
                    "input_bytes": resource["host_counters"]["input_bytes"],
                    "rss_bytes": resource["peak_counters"]["rss_bytes"]}
    result = {"schema": SCHEMA, "status": "COMPLETE", "terminal": PASS, "complete": True,
              "A4_presentation_input": 1, "A4_invariant_closure": 1, "A4_word_bearing_K": 1,
              "authority": authority.identity, "runtime": {"contexts": [
                  {"index": i, "type": CONTEXT_TYPES[i], "context_id": CONTEXT_IDS[i],
                   "tag": CONTEXT_TAGS[i]} for i in range(10)],
                  "affine_law": "(a,u)*(b,v)=(a*b,u+a.v)",
                  "inverse_law": "S(x^-1)=(rho(x)^-1,-rho(x)^-1 delta(x))",
                  "actor_cache_signed": 40, "actual_inverse_word_checks": True},
              "primitive_inventory": {**inventory, "prefix_edges": len(forward.nodes) - 1},
              "forward_dag": {"nodes": len(forward.nodes), "edges": len(forward.nodes) - 1,
                              "edge_state_products": 10 * (len(forward.nodes) - 1),
                              "all_primitive_terminals_used_by_row_assembly": True},
              "kernel": kernel,
              "performance": {"n": ROWS, "t": len(kernel["K_roster"]),
                              "p": kernel["boundary"]["rank"],
                              "Q": ROWS + 4 * len(kernel["K_roster"]) + 1,
                              "correlation_pair_sum": meter.counters.get("correlation_pairs", 0),
                              "row_piece_products": meter.counters.get("row_piece_products", 0),
                              "checkpoint": str(checkpoint) if checkpoint else None,
                              "measured": measurement},
              "resource": resource,
              "driver_contract": {"producer_terminal_lines": 1,
                                  "checker_terminal_lines": 1,
                                  "sentinel_last": True,
                                  "typed_unknown_exit_zero": True},
              "forbidden_downstream": {"lift": False, "fake": False, "Ihara": False,
                                        "base_pairs": False, "ambient_E3_E4_enumeration": False}}
    LIVE_STATE["normal"] = result
    result["resume"] = {"restored": resume_state is not None,
                         "next_row": (resume_state or {}).get("next_row", 1),
                         "rebuild_compared": resume_state is not None}
    return result


def checkpoint_reference(path: Path | None, meter: Meter,
                         authority_identity: str | None = None) -> dict[str, Any]:
    """Bind a resource terminal to a physical checkpoint or pre-authority stop."""
    if not meter.authority_complete and authority_identity is None:
        return {"kind": "pre_authority_resource", "owner": "producer", "authority": None,
                "state": PRE_AUTHORITY_STATE, "path": str(path) if path else None,
                "bytes": 0, "sha256": None, "replayable": False}
    if path is None or not path.exists():
        return {"kind": "missing_checkpoint", "path": str(path) if path else None,
                "bytes": 0, "sha256": None, "replayable": False}
    try:
        checked = checkpoint_input(path, "TERMINAL_CHECKPOINT_REFERENCE")
        size = int(os.lstat(checked).st_size)
        require(size <= OBJECT_CAPS["checkpoint_current_bytes"], "terminal:checkpoint_object_cap")
        raw = read_once(checked, (checked.as_posix().replace(ROOT.as_posix() + "/", ""), size, ""),
                         meter, "terminal.checkpoint_reference", terminal_transport=True)
        value = json.loads(raw.decode("ascii")); claimed = value.get("self_digest_sha256")
        body = dict(value); body.pop("self_digest_sha256", None)
        require(claimed == digest(body) and value.get("schema") == SCHEMA + "/checkpoint/v1" and
                value.get("owner") == "producer" and isinstance(value.get("code_sha256"), str) and
                isinstance(value.get("next_state_canary"), str), "terminal:checkpoint_seal")
    except Exception:
        return {"kind": "missing_checkpoint", "path": str(path), "bytes": 0,
                "sha256": None, "replayable": False}
    return {"kind": "sealed_checkpoint", "path": checked.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": sha(raw), "owner": value["owner"], "code_sha256": value["code_sha256"],
            "next_row": value["next_row"], "next_state_canary": value["next_state_canary"],
            "checkpoint_self_digest_sha256": claimed, "replayable": True, "sealed": True}


def terminal_certificate(status: str, reason: str, meter: Meter,
                         checkpoint: Path | None = None,
                         authority_identity: str | None = None) -> dict[str, Any]:
    meter._sync()
    reference = checkpoint_reference(checkpoint, meter, authority_identity)
    return {"schema": SCHEMA, "status": status, "terminal": status, "complete": False,
            "authority": authority_identity,
            "reason": reason, "checkpoint": reference,
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
    p = argparse.ArgumentParser(); p.add_argument("--selftest", action="store_true"); p.add_argument("--fixture")
    p.add_argument("--output"); p.add_argument("--checkpoint"); p.add_argument("--resume")
    p.add_argument("--input", default="ci/in/d972_r07_seven_context_roof_presentation_v1.json")
    p.add_argument("--seconds", type=int, default=14400); p.add_argument("--rss-bytes", type=int, default=8000000000)
    for key, value in AUTH.items():
        p.add_argument("--task198-" + key.replace("_", "-"), dest="task198_" + key,
                       default="ci/in/" + value)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv); meter = Meter({**CAPS, "wall_seconds": args.seconds, "rss_bytes": args.rss_bytes})
    meter.restore_mode = bool(args.resume)
    checkpoint_arg: Path | None = None
    resume_arg: Path | None = None
    output: Path | None = None
    authority_identity: str | None = None
    try:
        # All caller-controlled output/checkpoint names are resolved inside the
        # typed-input guard.  A rejected target is a fail-closed transport
        # stop; it must never escape as an untyped path exception before the
        # terminal handlers are installed.
        try:
            if args.output:
                output = output_path(args.output, "ci/out", "PRODUCER_OUTPUT")
            if args.checkpoint:
                checkpoint_text = str(args.checkpoint).replace("\\", "/")
                checkpoint_arg = output_path(checkpoint_text, "ci/out", "PRODUCER_CHECKPOINT")
            if args.resume:
                resume_text = str(args.resume).replace("\\", "/")
                resume_path = Path(resume_text)
                resume_arg = exact_path(resume_text, "ci/out", resume_path.name, "CHECKPOINT_RESUME")
        except Reject as exc:
            raise HardStop("transport:untrusted_output_path:" + str(exc)) from exc
        require(args.seconds == CAPS["wall_seconds"] and args.rss_bytes == CAPS["rss_bytes"],
                "driver:registered_wall_rss_limits")
        authority = AuthorityAdapter(args, meter)
        authority_identity = authority.identity
        meter.authority_complete = True
        if checkpoint_arg is not None and args.resume is None:
            write_prefrontier_checkpoint(checkpoint_arg, authority, meter)
        if args.selftest:
            require(args.fixture is not None, "SELFTEST_FIXTURE_REQUIRED")
            fixture_path = exact_path(args.fixture, ".", Path(args.fixture).name, "SELFTEST_FIXTURE")
            fixture_raw = read_once(fixture_path, (str(Path(args.fixture).as_posix()),
                                                    int(os.lstat(fixture_path).st_size), ""),
                                    meter, "selftest.fixture")
            fixture = json.loads(fixture_raw.decode("ascii"))
            normal = actual_result(authority, meter, checkpoint_arg)
            result = selftest_certificate(fixture, authority, normal)
            if output: write_sealed(output, result, meter)
            print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_SELFTEST_PASS", flush=True); return 0
        resume_state = restore_checkpoint(resume_arg, authority, meter) if resume_arg else None
        result = actual_result(authority, meter, checkpoint_arg, resume_state)
        if output: write_sealed(output, result, meter)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_TERMINAL " + PASS, flush=True); return 0
    except ResourceStop as exc:
        if output:
            write_sealed(output, terminal_certificate(UNKNOWN_RESOURCE, str(exc), meter, checkpoint_arg,
                                                     authority_identity), meter, terminal_transport=True)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_TERMINAL " + UNKNOWN_RESOURCE, flush=True); return 0
    except (Reject, UnicodeDecodeError, json.JSONDecodeError, FileNotFoundError) as exc:
        if output: write_sealed(output, terminal_certificate(UNKNOWN_INPUT, str(exc), meter, checkpoint_arg,
                                                             authority_identity), meter, terminal_transport=True)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_TERMINAL " + UNKNOWN_INPUT, flush=True); return 0
    except Exception as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_STOP " +
              type(exc).__name__ + ":" + str(exc), file=sys.stderr, flush=True)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_STOP " + type(exc).__name__, flush=True); return 2


if __name__ == "__main__":
    raise SystemExit(main())
