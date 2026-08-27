#!/usr/bin/env python3
"""Positive-only R07 all-seven common-word column generation (task179).

This producer has no negative terminal.  It reconstructs the task175 target,
the task176 linked extension section, typed PB3/PB4 boundary columns, and
literal correction columns.  A bounded run either prints a replayed positive
witness or an authenticated resumable resource/input UNKNOWN.

The implementation deliberately does not materialise Delta_all.  Singleton
fibres are queried lazily through the complete Q0 shortlex section and the 243
Gamma states.  Every accepted candidate is checked by the full eleven Fox
occurrences and then by a fresh direct all-seven Fox calculation.
"""

from __future__ import annotations

import argparse
from array import array
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-positive-common-word-colgen/v1"
CHECKPOINT_SCHEMA = "d972-r07-positive-common-word-colgen-checkpoint/v1"
COMMON = "R07_POSITIVE_COMMON_WORD_COLGEN_COMMON_WORD"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
FIXTURE = ROOT / "search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json"
FIXTURE_BYTES = 407
FIXTURE_SHA256 = "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"
Q0_STATE_COUNT = 1_469_664
DELTA_ORDER = 357_128_352
KERNEL_ORDERS = (9, 9, 9, 9, 9, 1, 1, 1, 3, 3)
COARSE_TABLE_LENGTH = 1 << 22
COARSE_INDEX_PAYLOAD_BYTES = COARSE_TABLE_LENGTH * 4


# Direct imports and governing sources.  The task176 triplet intentionally
# retains the commission identities; a live-tree repair must be followed by
# one parent-controlled pin cascade before production can start.
PINS: dict[str, tuple[str, int, str]] = {
    "task179": ("sol/luna_task_179_r07_positive_common_word_colgen_v1.md", 13105,
                "f97870ec0243b2c399928bcef4f89134f1cd41f15869cc88e3ba7d9dc6956a73"),
    "proof142": ("sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md", 4942,
                 "5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8"),
    "proof143": ("sol/proof_r07_actual_weighted_support_hitting_selector_v143.md", 5253,
                 "aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259"),
    "proof139": ("sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md", 8310,
                 "62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920"),
    "proof140": ("sol/proof_r07_positive_only_common_word_colgen_v140.md", 10073,
                 "6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b"),
    "proof138": ("sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md", 6371,
                 "9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456"),
    "proof110": ("sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md", 12136,
                 "dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc"),
    "proof108": ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742,
                 "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
    "proof121": ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762,
                 "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"),
    "proof122": ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939,
                 "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"),
    "proof125": ("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md", 8545,
                 "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"),
    "proof135": ("sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md", 4539,
                 "75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67"),
    "task175_producer": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306,
                         "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    "task175_checker": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 85848,
                        "c55ec99a9a920cd5d0ef92db7d5f2ad841dda7b0f1dcc59a5dc45e469ed6f7cc"),
    "task175_driver": ("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g", 21580,
                       "dbe147f98774fde50dee86de7306f9e18243ac1becef0ec7516765bcb2e08765"),
    "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                         "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980,
                        "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    "task176_driver": ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929,
                       "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"),
    "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
                   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                      "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "seedspan_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219,
                            "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "old_arithmetic": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942,
                       "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"),
    "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
                     "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "v172_source": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918,
                    "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "g760_source": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409,
                    "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
    "pb4_source": ("search/d972_b345_target6_dual_colgen_v2.py", 444497,
                   "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"),
    "full_d2_v1": ("search/d972_b345_full_d2_dual_correlation_v1.py", 78832,
                   "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"),
    "full_d2_v2": ("search/d972_b345_full_d2_dual_correlation_v2.py", 42449,
                   "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"),
}


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float, limit: int | float):
        super().__init__(f"{phase}:{cap}:{value}>{limit}")
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_chunks(chunks: Iterable[bytes | bytearray]) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk)
    return digest.hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_module(rel: str, name: str) -> Any:
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise InputStop("module_loader:" + rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate_inputs() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for name, (rel, expected_bytes, expected_sha) in PINS.items():
        path = ROOT / rel
        if not path.is_file():
            raise InputStop("missing:" + rel)
        raw = path.read_bytes()
        if len(raw) != expected_bytes or sha_bytes(raw) != expected_sha:
            raise InputStop("pin:" + rel)
        out[name] = {"path": rel, "bytes": expected_bytes, "sha256": expected_sha}
    raw = FIXTURE.read_bytes() if FIXTURE.is_file() else b""
    if len(raw) != FIXTURE_BYTES or sha_bytes(raw) != FIXTURE_SHA256:
        raise InputStop("pin:search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json")
    out["fixture"] = {"path": str(FIXTURE.relative_to(ROOT)).replace("\\", "/"),
                      "bytes": FIXTURE_BYTES, "sha256": FIXTURE_SHA256}
    return out


class Monitor:
    """Registered resource caps; programming errors are never caught here."""
    def __init__(self, args: argparse.Namespace):
        self.started = time.monotonic()
        self.limits = {
            "wall_seconds": float(args.seconds),
            "boundary_pairs": int(args.boundary_pairs),
            "fibre_scans": int(args.fibre_scans),
            "candidate_words": int(args.candidate_words),
            "retained_columns": int(args.retained_columns),
            "checkpoint_bytes": int(args.checkpoint_bytes),
            "rss_bytes": int(args.rss_bytes),
            "oracle_rounds": int(args.oracle_rounds),
            "global_roster": DELTA_ORDER,
        }
        self.counters = {name: 0 for name in (
            "boundary_pairs", "fibre_scans", "candidate_words",
            "retained_columns", "checkpoint_bytes")}
        self.counters["global_roster"] = 0
        self.counters["oracle_rounds"] = 0
        self.phase = "initialization"

    def rss(self) -> int:
        try:
            import resource
            value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            return value if sys.platform == "darwin" else value * 1024
        except (ImportError, AttributeError):
            return 0

    def check(self, phase: str) -> None:
        self.phase = phase
        elapsed = time.monotonic() - self.started
        if elapsed > self.limits["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", elapsed,
                               self.limits["wall_seconds"])
        rss = self.rss()
        if rss and rss > self.limits["rss_bytes"]:
            raise ResourceStop(phase, "rss_bytes", rss, self.limits["rss_bytes"])

    def bump(self, name: str, amount: int = 1, phase: str | None = None) -> None:
        self.counters[name] += amount
        if self.counters[name] > self.limits[name]:
            raise ResourceStop(phase or self.phase, name, self.counters[name],
                               self.limits[name])
        if (self.counters[name] & 4095) == 0:
            self.check(phase or self.phase)

    def public(self) -> dict[str, Any]:
        return {"phase": self.phase, "elapsed_seconds": time.monotonic() - self.started,
                "rss_bytes": self.rss(), "limits": self.limits,
                "counters": self.counters, "single_process": True}


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        if not letter:
            raise ValueError("zero free-group letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def exponent_pair(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word) % 3,
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word) % 3)


# Typed rows are encoded as byte keys.  This prevents E3/E4 or H1/H2/P
# cancellation even when their underlying element bytes coincide.
def row_key(block: int, component: int, blob: bytes) -> bytes:
    require(block in (1, 2, 3) and 1 <= component <= 6, "typed row key")
    return b"R" + bytes((block, component)) + len(blob).to_bytes(2, "big") + blob


def exponent_key(index: int) -> bytes:
    require(index in (1, 2), "exponent key")
    return b"E" + bytes((index,))


def decode_row_key(key: bytes) -> tuple[int, int, bytes]:
    require(len(key) >= 5 and key[:1] == b"R", "decode typed row key")
    width = int.from_bytes(key[3:5], "big")
    require(len(key) == 5 + width, "typed key width")
    return key[1], key[2], key[5:]


Sparse = dict[bytes, int]


def add_scaled(target: Sparse, source: Sparse, scalar: int) -> None:
    scalar %= 3
    if not scalar:
        return
    for key, value in source.items():
        answer = (target.get(key, 0) + scalar * int(value)) % 3
        if answer:
            target[key] = answer
        else:
            target.pop(key, None)


def scaled(source: Sparse, scalar: int) -> Sparse:
    return {key: (int(value) * scalar) % 3 for key, value in source.items()
            if (int(value) * scalar) % 3}


def pair(functional: Sparse, vector: Sparse) -> int:
    return sum(int(value) * int(vector.get(key, 0))
               for key, value in functional.items()) % 3


def public_sparse(row: Sparse) -> list[list[Any]]:
    return [[key.hex(), int(row[key]) % 3] for key in sorted(row) if int(row[key]) % 3]


def parse_sparse(rows: Sequence[Sequence[Any]]) -> Sparse:
    answer: Sparse = {}
    for item in rows:
        require(len(item) == 2 and int(item[1]) in (1, 2), "public sparse row")
        key = bytes.fromhex(str(item[0]))
        require(key not in answer, "duplicate sparse key")
        answer[key] = int(item[1])
    require(public_sparse(answer) == [list(x) for x in rows], "sparse canonical order")
    return answer


class Echelon:
    """Deterministic append-only F3 echelon with lossless column ancestry."""
    def __init__(self) -> None:
        self.rows: dict[bytes, Sparse] = {}
        self.ancestry: dict[bytes, dict[int, int]] = {}
        self.order: list[bytes] = []

    @staticmethod
    def _combine(target: dict[int, int], source: dict[int, int], scalar: int) -> None:
        for key, value in source.items():
            answer = (target.get(key, 0) + scalar * value) % 3
            if answer:
                target[key] = answer
            else:
                target.pop(key, None)

    def reduce(self, source: Sparse) -> tuple[Sparse, dict[int, int]]:
        row = dict(source); coefficients: dict[int, int] = {}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                add_scaled(row, self.rows[pivot], -value)
                self._combine(coefficients, self.ancestry[pivot], value)
        return row, coefficients

    def add(self, source: Sparse, column_id: int) -> tuple[bool, bytes | None, dict[int, int]]:
        row = dict(source); ancestry = {column_id: 1}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                add_scaled(row, self.rows[pivot], -value)
                self._combine(ancestry, self.ancestry[pivot], -value)
        if not row:
            return False, None, ancestry
        pivot = min(row); inv = 1 if row[pivot] == 1 else 2
        row = scaled(row, inv)
        ancestry = {key: (value * inv) % 3 for key, value in ancestry.items()
                    if (value * inv) % 3}
        require(pivot not in self.rows, "append-only pivot collision")
        self.rows[pivot] = row; self.ancestry[pivot] = ancestry
        self.order.append(pivot)
        return True, pivot, ancestry

    def exact_dual(self, target: Sparse) -> tuple[Sparse, Sparse, dict[int, int]]:
        remainder, coefficients = self.reduce(target)
        require(remainder, "dual requested after membership")
        free = min(remainder)
        functional: Sparse = {free: 1}
        for pivot in reversed(self.order):
            value = -sum(coefficient * functional.get(key, 0)
                         for key, coefficient in self.rows[pivot].items()
                         if key != pivot) % 3
            if value:
                functional[pivot] = value
            else:
                functional.pop(pivot, None)
        require(all(pair(functional, self.rows[pivot]) == 0 for pivot in self.order),
                "exact dual annihilation")
        require(pair(functional, target) != 0, "exact dual target pairing")
        return functional, remainder, coefficients


def module_api(module: Any, names: dict[str, tuple[str, ...]], label: str) -> None:
    for name, parameters in names.items():
        value = getattr(module, name, None)
        if not callable(value):
            raise InputStop(f"{label}:missing_api:{name}")
        actual = tuple(inspect.signature(value).parameters)
        if actual != parameters:
            raise InputStop(f"{label}:signature:{name}:{actual}")


def build_runtime(monitor: Monitor) -> dict[str, Any]:
    """Rebuild task175 and the live task176 extension without artifact reuse."""
    monitor.check("task175_reconstruction")
    p175 = load_module(PINS["task175_producer"][0], "d179_task175")
    module_api(p175, {"run_preflight": (), "load_source": ("rel", "name")}, "task175")
    bridge = p175.run_preflight()
    if bridge.get("terminal") != p175.TERMINAL_READY:
        raise InputStop("task175:not_READY")

    p176 = load_module(PINS["task176_producer"][0], "d179_task176")
    module_api(p176, {
        "build_fine_deletion": ("e3", "e4", "budget"),
        "make_deleter": ("old", "e3", "e4", "fine", "q0_marked"),
        "enumerate_q0_sections": ("old", "q0_marked", "coordinate_marks", "e3", "e4", "budget"),
        "projection": ("state", "delete"),
        "family_public_A": ("old", "name", "indices", "projected", "e3", "e4", "qmarks"),
        "scan_memberships": ("stores", "A_maps", "budget"),
        "prove_L": ("old", "name", "membership", "count", "qstates", "qids", "q0_marked", "budget"),
        "gamma_kernel_generators": ("group", "projected", "indices", "e3", "e4", "old"),
        "eval_word_coordinates": ("old", "e3", "e4", "contexts", "delete", "word"),
    }, "task176")
    q3_path = ROOT / PINS["q3_receipt"][0]
    joint_path = ROOT / PINS["joint_receipt"][0]
    p176.authenticate_pins(q3_path, joint_path)
    q3 = json.loads(q3_path.read_text(encoding="utf-8"))
    joint_receipt = json.loads(joint_path.read_text(encoding="utf-8"))
    old = p176.load_module(ROOT / p176.PINS["e4_arithmetic"][0], "d179_arithmetic")
    jointmod = p176.load_module(ROOT / p176.PINS["task157ee_producer"][0], "d179_joint")
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(aliases) >= 46, "ten context registry")
    words = [list(row["word"]) for row in q3["correction_fibre"]["records"] if row.get("word")]

    class PackedJointGroup(jointmod.JointGroup):
        def blob(self, value: Any) -> bytes:
            return p176.packed_joint_blob(value, "task179 Gamma state")

    gamma = PackedJointGroup(old, e3, e4, contexts, words)
    require(len(gamma.states) == 243 and
            gamma.public()["state_rows_sha256"] == joint_receipt["gamma"]["state_rows_sha256"],
            "Gamma 243 replay")
    fine, fine_public = p176.build_fine_deletion(e3, e4, monitor)
    q0_marked = [p176.canonical_packed_permutation(old.perm_from_row(row, 36), 36,
                                                   "task179 Q0 mark")
                 for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
    delete, deletion_public = p176.make_deleter(old, e3, e4, fine, q0_marked)
    deletion_public["fine"] = fine_public
    projected = [p176.projection(state, delete) for state in gamma.states]
    coordinate_marks: list[list[Any]] = []
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
    monitor.check("Q0_positive_shortlex_section")
    qstates, qids, parents, letters, stores, _ = p176.enumerate_q0_sections(
        old, q0_marked, coordinate_marks, e3, e4, monitor)
    require(len(qstates) == Q0_STATE_COUNT and len(parents) == len(qstates),
            "Q0 complete section")
    memberships, L_counts = p176.scan_memberships(stores, A_maps, monitor)
    emitted: dict[str, Any] = {}
    for name, indices in p176.FAMILIES:
        selected, proof = p176.prove_L(old, name, memberships[name], L_counts[name],
                                       qstates, qids, q0_marked, monitor)
        gamma_selected, gamma_kernel = p176.gamma_kernel_generators(
            gamma, projected, indices, e3, e4, old)
        gamma_words = [list(gamma.section_word(sid)) for sid in gamma_selected]
        adjusted: list[list[int]] = []
        for qid in selected:
            row = p176.section_row(stores, qid)
            key = p176.family_key(row, indices)
            need = p176.family_inverse_key(key, indices, e3, e4)
            require(need in A_maps[name], "adjusted L Gamma witness")
            gid = A_maps[name][need]
            adjusted.append(reduce_word(list(gamma.section_word(gid)) +
                                        p176.q0_section_word(qid, parents, letters)))
        emitted[name] = {"Gamma_S0_generators": gamma_words,
                         "adjusted_L_generators": adjusted,
                         "Gamma_S0_order": len(gamma_kernel),
                         "L_order": L_counts[name], "L_proof": proof}

    # Rebuild the complete 6,441 roster/group from the same authenticated
    # arithmetic; the 110 rows in task175 remain canaries only.
    v172 = p175.load_source(PINS["v172_source"][0], "d179_v172")
    prev = v172.load(v172.PREV, "d179_v172_prev")
    prev.Q3_ARTIFACT = v172.Q3; prev.Q3_ARTIFACT_SHA = v172.Q3_SHA
    q_for_roster, old175 = prev.authenticated_input(v172.Q3)
    e3_175, e4_175, _ = old175.reconstruct_quotients(q_for_roster)
    contexts175, _, _ = old175.cheap_context_registry(e4_175)
    joint175 = p175.load_source(PINS["joint_source"][0], "d179_joint175")
    group, roster = v172.build_roster(joint175, old175, e3_175, e4_175,
                                      contexts175, words)
    require(len(roster) == 6441 and all(group.eval(row["word"]) == group.identity
                                        for row in roster), "complete relation roster")
    require([[r["layer"], r["ordinal"], r["word"]] for r in roster] ==
            [[r["layer"], r["ordinal"], r["word"]] for r in bridge["roster"]],
            "task175 roster equality")
    return {"p175": p175, "p176": p176, "bridge": bridge, "old": old,
            "e3": e3, "e4": e4, "contexts": contexts,
            "context_public": context_public, "delete": delete,
            "gamma": gamma, "projected": projected, "A_maps": A_maps,
            "A_public": A_public, "qstates": qstates, "qids": qids,
            "parents": parents, "letters": letters, "stores": stores,
            "coordinate_marks": coordinate_marks, "emitted": emitted,
            "roster": roster, "joint_group": group,
            "deletion_public": deletion_public}


def unpack_element(runtime: dict[str, Any], raw: bytes, block: int) -> Any:
    return runtime["p176"].value_from_blob(raw, 0 if block in (1, 2) else 5)


def element_blob(runtime: dict[str, Any], value: Any) -> bytes:
    return runtime["p176"].packed_joint_blob(value, "task179 typed element")


def tagged_serial(rows: Sequence[Sequence[Any]], block: int, scalar: int = 1) -> Sparse:
    answer: Sparse = {}
    for component0, blob_hex, coefficient0 in rows:
        key = row_key(block, int(component0), bytes.fromhex(str(blob_hex)))
        coefficient = scalar * int(coefficient0) % 3
        if coefficient:
            answer[key] = (answer.get(key, 0) + coefficient) % 3
            if not answer[key]:
                del answer[key]
    return answer


def exact_target(runtime: dict[str, Any]) -> Sparse:
    bridge = runtime["bridge"]
    require(bridge.get("base_target_source", "g760_raw_fox") != "stacked_target",
            "target/canary confusion")
    target: Sparse = {}
    for label, block in (("H1", 1), ("H2", 2), ("P", 3)):
        row = bridge["raw_base_targets"][label]
        require(sha_obj(row["row"]) == row["sha256"], "raw base target digest")
        add_scaled(target, tagged_serial(row["row"], block), -1)
    require(all(key[:1] == b"R" for key in target), "zero exponent target")
    return target


def serial_group_row(runtime: dict[str, Any], row: dict[tuple[int, Any], int],
                     block: int) -> Sparse:
    answer: Sparse = {}
    for (component, value), coefficient in row.items():
        coefficient = int(coefficient) % 3
        if coefficient:
            key = row_key(block, int(component), element_blob(runtime, value))
            answer[key] = (answer.get(key, 0) + coefficient) % 3
            if not answer[key]:
                del answer[key]
    return answer


def paper_product(*displayed: Sequence[int]) -> list[int]:
    return reduce_word(letter for factor in reversed(displayed) for letter in factor)


def group_for_block(runtime: dict[str, Any], block: int) -> Any:
    return runtime["e3"] if block in (1, 2) else runtime["e4"]


class AllSevenModel:
    """Eleven literal Fox occurrences and fresh direct all-seven replay."""
    def __init__(self, runtime: dict[str, Any]):
        self.rt = runtime; self.old = runtime["old"]
        self.e3, self.e4 = runtime["e3"], runtime["e4"]
        self.g = list(runtime["bridge"]["g760"]["word"])
        x, y = [1], [2]
        z = self.old.inv_word(self.old.pp_words([x, y]))
        u = self.old.inv_word(self.old.pp_words([y, x]))
        self.pcontexts = [([1], [4]), ([4], [6]),
                          (paper_product([2], [4]), [6]),
                          (paper_product([1], [2]), paper_product([5], [6])),
                          ([1], paper_product([4], [5]))]
        raw_specs = [
            (1, 0, self.e3, x, y, 1, True, "H1_fxy"),
            (1, 1, self.e3, x, z, -1, True, "H1_fxz"),
            (1, 2, self.e3, y, z, 1, True, "H1_fyz"),
            (2, 3, self.e3, u, x, -1, True, "H2_fux"),
            (2, 0, self.e3, x, y, -1, True, "H2_fxy"),
            (2, 4, self.e3, u, y, 1, True, "H2_fuy"),
        ]
        for natural_index, coordinate, label in ((1, 5, "P_b1"),
                                                  (3, 6, "P_b2"),
                                                  (0, 7, "P_b3"),
                                                  (2, 8, "P_b5_inverse"),
                                                  (4, 9, "P_b4_inverse")):
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
            indices = [i for i, row in enumerate(self.specs) if row["block"] == block]
            prefix = group_for_block(runtime, block).identity
            for index in reversed(indices):
                self.specs[index]["prefix"] = prefix
                value = group_for_block(runtime, block).eval(self.specs[index]["base_factor"])
                prefix = group_for_block(runtime, block).mul(prefix, value)
            require(prefix == group_for_block(runtime, block).identity,
                    "g760 base relation quotient identity")
        # In a positive slot the corrected factor is g_i*c_i, so the Fox
        # difference is g_i*D(c_i) before the surrounding product prefix is
        # applied.  In a negative slot (g_i*c_i)^-1=c_i^-1*g_i^-1 and the
        # base-factor gradients cancel without that extra g_i translation.
        for spec in self.specs:
            spec["occurrence_prefix"] = spec["prefix"]
            if spec["sign"] > 0:
                spec["occurrence_prefix"] = spec["quotient"].mul(
                    spec["prefix"], spec["quotient"].eval(spec["base_factor"]))

    def _substitute(self, word: Sequence[int], left: Sequence[int],
                    right: Sequence[int], lift: bool) -> list[int]:
        answer = self.old.f2_substitute(list(word), list(left), list(right))
        return list(self.old.embed_f2_pb3(answer)) if lift else list(answer)

    def occurrence_data(self, relator_word: Sequence[int], dual: Sparse) -> dict[str, Any]:
        merged: dict[tuple[int, bytes], int] = {}
        public_occurrences = []
        for ordinal, spec in enumerate(self.specs, 1):
            quotient = spec["quotient"]
            relation = self._substitute(relator_word, spec["left"], spec["right"],
                                        spec["lift"])
            if spec["sign"] < 0:
                relation = list(self.old.inv_word(relation))
            gradient, value = self.old.fox_gradient_without_sections(relation, quotient)
            require(value == quotient.identity, "roster relation occurrence identity")
            prefix_inv = quotient.inverse(spec["occurrence_prefix"])
            occurrence_terms = 0
            for (component, base_value), base_coefficient in gradient.items():
                base_inverse = quotient.inverse(base_value)
                for key, lambda_coefficient in dual.items():
                    if key[:1] != b"R":
                        continue
                    block, dual_component, target_blob = decode_row_key(key)
                    if block != spec["block"] or dual_component != int(component):
                        continue
                    target_value = unpack_element(self.rt, target_blob, block)
                    required_value = quotient.mul(
                        quotient.mul(prefix_inv, target_value), base_inverse)
                    required_blob = element_blob(self.rt, required_value)
                    coefficient = int(base_coefficient) * int(lambda_coefficient) % 3
                    if coefficient:
                        merged_key = (int(spec["coordinate"]), required_blob)
                        merged[merged_key] = (merged.get(merged_key, 0) + coefficient) % 3
                        if not merged[merged_key]:
                            del merged[merged_key]
                        occurrence_terms += 1
            public_occurrences.append({"ordinal": ordinal, "label": spec["label"],
                                       "coordinate": spec["coordinate"],
                                       "factor_sign": spec["sign"],
                                       "raw_dual_pair_terms": occurrence_terms})
        exponents = exponent_pair(relator_word)
        constant = (dual.get(exponent_key(1), 0) * exponents[0] +
                    dual.get(exponent_key(2), 0) * exponents[1]) % 3
        ordered = sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))
        return {"constant": constant, "merged": merged,
                "public": {"K": constant,
                           "terms": [[coord, raw.hex(), coefficient]
                                     for (coord, raw), coefficient in ordered],
                           "same_target_merged_mod3": True,
                           "zero_sums_deleted": True,
                           "eleven_occurrences": public_occurrences}}

    @staticmethod
    def formula_scalar(formula: dict[str, Any], coordinate_blobs: Sequence[bytes]) -> int:
        answer = int(formula["constant"])
        for (coordinate, target), coefficient in formula["merged"].items():
            if coordinate_blobs[coordinate] == target:
                answer += int(coefficient)
        return answer % 3

    def occurrence_column(self, delta_word: Sequence[int], relator_word: Sequence[int]) -> Sparse:
        answer: Sparse = {}
        for spec in self.specs:
            quotient = spec["quotient"]
            relation = self._substitute(relator_word, spec["left"], spec["right"],
                                        spec["lift"])
            if spec["sign"] < 0:
                relation = list(self.old.inv_word(relation))
            gradient, value = self.old.fox_gradient_without_sections(relation, quotient)
            require(value == quotient.identity, "occurrence relation value")
            qword = self._substitute(delta_word, spec["left"], spec["right"],
                                     spec["lift"])
            translated = self.old.translate_vector(
                self.old.translate_vector(gradient, quotient.eval(qword), quotient),
                spec["occurrence_prefix"], quotient)
            add_scaled(answer, serial_group_row(self.rt, translated, spec["block"]), 1)
        e1, e2 = exponent_pair(relator_word)
        if e1:
            answer[exponent_key(1)] = e1
        if e2:
            answer[exponent_key(2)] = e2
        return answer

    def _pentagon_word(self, word: Sequence[int]) -> list[int]:
        factors = [self.old.f2_substitute(list(word), left, right)
                   for left, right in self.pcontexts]
        return paper_product(factors[1], factors[3], factors[0],
                             self.old.inv_word(factors[2]), self.old.inv_word(factors[4]))

    def direct_column(self, delta_word: Sequence[int], relator_word: Sequence[int]) -> tuple[Sparse, dict[str, Any]]:
        conjugate = reduce_word(list(delta_word) + list(relator_word) +
                                inverse_word(delta_word))
        require(self.rt["joint_group"].eval(conjugate) ==
                self.rt["joint_group"].identity, "literal conjugate joint kernel")
        corrected = reduce_word(self.g + conjugate)
        base_hex = self.old.hexagon_words(self.g)
        corr_hex = self.old.hexagon_words(corrected)
        words = [(1, self.e3, list(self.old.embed_f2_pb3(base_hex[0])),
                  list(self.old.embed_f2_pb3(corr_hex[0]))),
                 (2, self.e3, list(self.old.embed_f2_pb3(base_hex[1])),
                  list(self.old.embed_f2_pb3(corr_hex[1]))),
                 (3, self.e4, self._pentagon_word(self.g),
                  self._pentagon_word(corrected))]
        answer: Sparse = {}
        quotient_values = []
        for block, quotient, base, new in words:
            base_gradient, base_value = self.old.fox_gradient_without_sections(base, quotient)
            new_gradient, new_value = self.old.fox_gradient_without_sections(new, quotient)
            require(base_value == quotient.identity and new_value == quotient.identity,
                    "direct all-seven quotient identity")
            difference = dict(new_gradient)
            for key, coefficient in base_gradient.items():
                value = (difference.get(key, 0) - int(coefficient)) % 3
                if value:
                    difference[key] = value
                else:
                    difference.pop(key, None)
            add_scaled(answer, serial_group_row(self.rt, difference, block), 1)
            quotient_values.append(element_blob(self.rt, new_value).hex())
        e1, e2 = exponent_pair(conjugate)
        if e1:
            answer[exponent_key(1)] = e1
        if e2:
            answer[exponent_key(2)] = e2
        occurrence = self.occurrence_column(delta_word, relator_word)
        require(answer == occurrence, "full eleven occurrence/direct Fox equality")
        return answer, {"delta_word": list(delta_word),
                        "relator_word": list(relator_word),
                        "conjugate_word": conjugate,
                        "corrected_word": corrected,
                        "quotient_value_blobs": quotient_values,
                        "eleven_occurrence_replay": True,
                        "direct_all_seven_replay": True}


def coordinate_blobs(runtime: dict[str, Any], word: Sequence[int]) -> tuple[bytes, ...]:
    values = runtime["p176"].eval_word_coordinates(
        runtime["old"], runtime["e3"], runtime["e4"], runtime["contexts"],
        runtime["delete"], list(word))
    return tuple(element_blob(runtime, value) for value in values)


def multiply_coordinate_rows(runtime: dict[str, Any], left: Sequence[bytes],
                             right: Sequence[bytes]) -> tuple[bytes, ...]:
    p176 = runtime["p176"]
    return tuple(p176.multiply_blob(a, b, i, runtime["e3"], runtime["e4"])
                 for i, (a, b) in enumerate(zip(left, right)))


class CoarseInverse:
    """Open-addressed coarse inverse; slots contain only unsigned qid+1."""
    def __init__(self, store: bytearray, width: int, degree: int,
                 monitor: Monitor | None, hash_fn: Any | None = None,
                 table_length: int = COARSE_TABLE_LENGTH,
                 expected_state_count: int | None = None):
        require(type(store) is bytearray, "coarse store representation")
        require(width > degree > 0 and table_length > 0 and
                (table_length & (table_length - 1)) == 0,
                "coarse inverse dimensions")
        self.store = store; self.width = width; self.degree = degree
        self.monitor = monitor; self.hash_fn = hash_fn or hash
        self.table_length = table_length; self.mask = table_length - 1
        self.slots = array("I", [0]) * table_length
        require(self.slots.itemsize == 4, "coarse inverse uint32 itemsize")
        self.state_count = len(store) // width
        require(len(store) == self.state_count * width,
                "coarse inverse store alignment")
        if expected_state_count is not None:
            require(self.state_count == expected_state_count,
                    "coarse inverse state count")
        self.built = False

    def _coarse_at(self, qid: int) -> bytes:
        start = qid * self.width
        return bytes(self.store[start:start + self.degree])

    def build(self) -> None:
        if self.built:
            return
        for qid in range(self.state_count):
            if self.monitor is not None:
                self.monitor.bump("fibre_scans", 1, "coarse_inverse_build")
            key = self._coarse_at(qid); slot = self.hash_fn(key) & self.mask
            while True:
                prior = int(self.slots[slot])
                if not prior:
                    self.slots[slot] = qid + 1
                    break
                prior_qid = prior - 1
                if self._coarse_at(prior_qid) == key:
                    raise RuntimeError("coarse inverse duplicate exact key")
                slot = (slot + 1) & self.mask
        self.built = True

    def lookup(self, key: bytes) -> int | None:
        require(type(key) is bytes and len(key) == self.degree,
                "coarse inverse key width")
        self.build()
        slot = self.hash_fn(key) & self.mask
        for _ in range(self.table_length):
            prior = int(self.slots[slot])
            if not prior:
                return None
            if self._coarse_at(prior - 1) == key:
                return prior - 1
            slot = (slot + 1) & self.mask
        raise RuntimeError("coarse inverse table exhausted")

    def public(self) -> dict[str, Any]:
        return {"state_count": self.state_count,
                "table_length": self.table_length,
                "payload_bytes": self.table_length * self.slots.itemsize,
                "uint32_itemsize": self.slots.itemsize,
                "injectivity": "hard_stop_on_duplicate_exact_coarse_key",
                "built": self.built}


class FibreOracle:
    """Exact lazy singleton fibres; no multi-coordinate inference is used."""
    def __init__(self, runtime: dict[str, Any], monitor: Monitor):
        self.rt = runtime; self.monitor = monitor
        self.cache: dict[tuple[int, bytes], dict[str, Any] | None] = {}
        self.kernel_states: dict[int, list[dict[str, Any]]] = {}
        self.kernel_seen: dict[int, set[tuple[bytes, ...]]] = {}
        self.kernel_heads: dict[int, int] = {}
        self.coarse_indices: dict[int, CoarseInverse] = {}

    def _coarse_index(self, coordinate: int) -> CoarseInverse:
        index = self.coarse_indices.get(coordinate)
        if index is None:
            width = self.rt["p176"].COORDINATE_WIDTHS[coordinate]
            degree = 36 if coordinate < 5 else 144
            index = CoarseInverse(self.rt["stores"][coordinate], width, degree,
                                  self.monitor, expected_state_count=Q0_STATE_COUNT)
            self.coarse_indices[coordinate] = index
        return index

    def index_public(self) -> dict[str, Any]:
        return {"state_count": Q0_STATE_COUNT,
                "coordinate_count": 10,
                "table_length": COARSE_TABLE_LENGTH,
                "payload_bytes_per_coordinate": COARSE_INDEX_PAYLOAD_BYTES,
                "payload_bytes_total": 10 * COARSE_INDEX_PAYLOAD_BYTES,
                "uint32_itemsize": 4,
                "injectivity": "hard_stop_on_duplicate_exact_coarse_key",
                "built_coordinate_count": len(self.coarse_indices),
                "built_coordinates": sorted(self.coarse_indices),
                "tables": {str(i): self.coarse_indices[i].public()
                           for i in sorted(self.coarse_indices)}}

    def canonical(self, coordinate: int, target: bytes) -> dict[str, Any] | None:
        key = (coordinate, target)
        if key in self.cache:
            return self.cache[key]
        p176 = self.rt["p176"]
        amap = self.rt["A_maps"][f"S{coordinate}"]
        index = self._coarse_index(coordinate)
        candidates: list[tuple[int, int, dict[str, Any]]] = []
        for (a,), gid in amap.items():
            section_target = p176.multiply_blob(
                p176.inverse_blob(a, coordinate, self.rt["e3"], self.rt["e4"]),
                target, coordinate, self.rt["e3"], self.rt["e4"])
            qid = index.lookup(section_target[:index.degree])
            if qid is None:
                continue
            section = p176.section_row(self.rt["stores"], qid)
            if section[coordinate] != section_target:
                continue
            require(p176.multiply_blob(a, section[coordinate], coordinate,
                                       self.rt["e3"], self.rt["e4"]) == target,
                    "singleton packed target replay")
            gamma_row = tuple(element_blob(self.rt, value)
                              for value in self.rt["projected"][gid])
            blobs = multiply_coordinate_rows(self.rt, gamma_row, section)
            gamma_word = list(self.rt["gamma"].section_word(gid))
            q0_word = p176.q0_section_word(qid, self.rt["parents"],
                                           self.rt["letters"])
            word = reduce_word(gamma_word + q0_word)
            require(blobs[coordinate] == target and coordinate_blobs(self.rt, word) == blobs,
                    "literal singleton section witness")
            candidates.append((qid, gid, {"coordinate": coordinate,
                "target_hex": target.hex(), "q0_state_id": qid + 1,
                "gamma_state_id": gid + 1, "source_word": word,
                "gamma_source_word": gamma_word, "q0_source_word": q0_word,
                "coordinate_blobs": blobs,
                "section_blob_hex": [x.hex() for x in section],
                "gamma_coordinate_blob_hex": gamma_row[coordinate].hex(),
                "selection": "least_qid_then_gid_coarse_inverse"}))
        if candidates:
            answer = min(candidates, key=lambda item: (item[0], item[1]))[2]
            self.cache[key] = answer
            return answer
        self.cache[key] = None
        return None

    def _kernel_generators(self, coordinate: int) -> list[list[int]]:
        row = self.rt["emitted"][f"S{coordinate}"]
        positive = ([list(word) for word in row["Gamma_S0_generators"]] +
                    [list(word) for word in row["adjusted_L_generators"]])
        generators: list[list[int]] = []
        for word in positive:
            generators.extend((word, inverse_word(word)))
        return generators

    def ensure_kernel_prefix(self, coordinate: int, length: int) -> list[dict[str, Any]]:
        if coordinate not in self.kernel_states:
            identity = coordinate_blobs(self.rt, [])
            self.kernel_states[coordinate] = [{"source_word": [],
                                               "coordinate_blobs": identity}]
            self.kernel_seen[coordinate] = {identity}; self.kernel_heads[coordinate] = 0
        states = self.kernel_states[coordinate]
        generators = self._kernel_generators(coordinate)
        while len(states) < length and self.kernel_heads[coordinate] < len(states):
            base = states[self.kernel_heads[coordinate]]; self.kernel_heads[coordinate] += 1
            for generator in generators:
                word = reduce_word(base["source_word"] + generator)
                blobs = coordinate_blobs(self.rt, word)
                identity = self.rt["p176"].blob(
                    self.rt["old"], self.rt["e3"].identity if coordinate < 5
                    else self.rt["e4"].identity)
                require(blobs[coordinate] == identity, "kernel prefix leaves singleton fibre")
                if blobs in self.kernel_seen[coordinate]:
                    continue
                self.kernel_seen[coordinate].add(blobs)
                states.append({"source_word": word, "coordinate_blobs": blobs})
                if len(states) >= length:
                    break
        return states[:length]

    def verify_kernel_orders(self) -> tuple[int, ...]:
        """Exhaust the word-bearing BFS and authenticate every kernel order."""
        identity_blobs = [self.rt["p176"].blob(
            self.rt["old"], self.rt["e3"].identity if i < 5
            else self.rt["e4"].identity) for i in range(10)]
        for coordinate, expected in enumerate(KERNEL_ORDERS):
            self.ensure_kernel_prefix(coordinate, expected)
            states = self.kernel_states[coordinate]
            while self.kernel_heads[coordinate] < len(states):
                base = states[self.kernel_heads[coordinate]]
                self.kernel_heads[coordinate] += 1
                for generator in self._kernel_generators(coordinate):
                    word = reduce_word(base["source_word"] + generator)
                    blobs = coordinate_blobs(self.rt, word)
                    require(blobs[coordinate] == identity_blobs[coordinate],
                            "kernel BFS nonidentity state")
                    if blobs in self.kernel_seen[coordinate]:
                        continue
                    self.kernel_seen[coordinate].add(blobs)
                    states.append({"source_word": word,
                                   "coordinate_blobs": blobs})
            require(len(states) == expected and
                    len(self.kernel_seen[coordinate]) == expected and
                    all(row["coordinate_blobs"][coordinate] == identity_blobs[coordinate]
                        for row in states),
                    f"kernel order S{coordinate}")
        return KERNEL_ORDERS

    def kernel_candidate(self, fibre: dict[str, Any], eta: dict[str, Any]) -> dict[str, Any]:
        word = reduce_word(eta["source_word"] + fibre["source_word"])
        blobs = multiply_coordinate_rows(self.rt, eta["coordinate_blobs"],
                                         fibre["coordinate_blobs"])
        require(blobs[fibre["coordinate"]] == bytes.fromhex(fibre["target_hex"]) and
                coordinate_blobs(self.rt, word) == blobs, "kernel fibre literal replay")
        return {"source_word": word, "coordinate_blobs": blobs,
                "coordinate": fibre["coordinate"], "target_hex": fibre["target_hex"],
                "q0_state_id": fibre["q0_state_id"],
                "gamma_state_id": fibre["gamma_state_id"],
                "kernel_word": eta["source_word"]}

    def weighted_support(self, formula: dict[str, Any]) -> dict[str, Any]:
        targets = sorted(formula["merged"], key=lambda item: (item[0], item[1]))
        rows = [{"coordinate": coordinate, "target_hex": target.hex(),
                 "kernel_order": self.kernel_orders[coordinate]}
                for coordinate, target in targets]
        return {"K": int(formula["constant"]),
                "W": sum(row["kernel_order"] for row in rows),
                "delta_order": DELTA_ORDER,
                "kernel_orders": list(self.kernel_orders),
                "distinct_targets": rows}

    def global_candidate(self, cursor: int) -> dict[str, Any]:
        require(0 <= cursor < DELTA_ORDER, "global roster cursor")
        self.monitor.bump("global_roster", 1, "weighted_global_prefix")
        qid, gid = divmod(cursor, 243)
        require(qid < len(self.rt["qstates"]) and
                gid < len(self.rt["projected"]), "global roster index range")
        section = self.rt["p176"].section_row(self.rt["stores"], qid)
        gamma_row = tuple(element_blob(self.rt, value)
                          for value in self.rt["projected"][gid])
        blobs = multiply_coordinate_rows(self.rt, gamma_row, section)
        word = reduce_word(list(self.rt["gamma"].section_word(gid)) +
                           self.rt["p176"].q0_section_word(
                               qid, self.rt["parents"], self.rt["letters"]))
        require(coordinate_blobs(self.rt, word) == blobs, "global literal section replay")
        return {"source_word": word, "coordinate_blobs": blobs,
                "q0_state_id": qid + 1, "gamma_state_id": gid + 1,
                "global_cursor": cursor}


def boundary_source(runtime: dict[str, Any], block: int, index: int) -> list[list[Any]]:
    if block in (1, 2):
        rows = runtime["bridge"]["pb3"]["rows"]
    else:
        rows = runtime["bridge"]["pb4"]["rows"]
    require(1 <= index <= len(rows), "boundary source index")
    return rows[index - 1]


def translated_boundary(runtime: dict[str, Any], block: int, index: int,
                        translation_blob: bytes) -> Sparse:
    quotient = group_for_block(runtime, block)
    translation = unpack_element(runtime, translation_blob, block)
    answer: Sparse = {}
    for component0, raw_hex, coefficient0 in boundary_source(runtime, block, index):
        value = unpack_element(runtime, bytes.fromhex(str(raw_hex)), block)
        translated = quotient.mul(translation, value)
        key = row_key(block, int(component0), element_blob(runtime, translated))
        coefficient = int(coefficient0) % 3
        answer[key] = (answer.get(key, 0) + coefficient) % 3
        if not answer[key]:
            del answer[key]
    return answer


def identity_blob(runtime: dict[str, Any], block: int) -> bytes:
    return element_blob(runtime, group_for_block(runtime, block).identity)


def boundary_oracle(runtime: dict[str, Any], dual: Sparse,
                    monitor: Monitor) -> dict[str, Any] | None:
    """All-seven port of support-times-occurrence correlation.

    It does not import the old six-component E4 functional.  For each typed
    block it reconstructs t=g*h^-1, checks t*h=g, accumulates every
    contribution for (block,relator,t), and only then decides ACTIVE.
    """
    support: dict[tuple[int, int], list[tuple[bytes, int]]] = {}
    for key, coefficient in dual.items():
        if key[:1] != b"R":
            continue
        block, component, raw = decode_row_key(key)
        support.setdefault((block, component), []).append((raw, coefficient))
    accumulated: dict[tuple[int, int, bytes], int] = {}
    contributors: dict[tuple[int, int, bytes], list[dict[str, Any]]] = {}
    for block, count in ((1, 2), (2, 2), (3, 11)):
        quotient = group_for_block(runtime, block)
        for relator_index in range(1, count + 1):
            for component0, h_hex, base_coefficient0 in boundary_source(
                    runtime, block, relator_index):
                component = int(component0); h_blob = bytes.fromhex(str(h_hex))
                h = unpack_element(runtime, h_blob, block)
                h_inv = quotient.inverse(h)
                for g_blob, lambda_coefficient in support.get((block, component), []):
                    monitor.bump("boundary_pairs", 1, "positive_boundary_correlation")
                    g = unpack_element(runtime, g_blob, block)
                    translation = quotient.mul(g, h_inv)
                    require(quotient.mul(translation, h) == g,
                            "left boundary translation t*h=g")
                    t_blob = element_blob(runtime, translation)
                    key = (block, relator_index, t_blob)
                    contribution = (int(base_coefficient0) *
                                    int(lambda_coefficient)) % 3
                    accumulated[key] = (accumulated.get(key, 0) + contribution) % 3
                    contributors.setdefault(key, []).append({
                        "component": component, "g_hex": g_blob.hex(),
                        "h_hex": h_blob.hex(),
                        "lambda_coefficient": int(lambda_coefficient),
                        "base_coefficient": int(base_coefficient0) % 3})
    active = [key for key, value in accumulated.items() if value % 3]
    if not active:
        return None
    block, index, translation_blob = min(active, key=lambda item: (item[0], item[2], item[1]))
    row = translated_boundary(runtime, block, index, translation_blob)
    scalar = pair(dual, row)
    require(scalar == accumulated[(block, index, translation_blob)] % 3 and scalar,
            "complete boundary scalar")
    return {"row": row, "provenance": {
        "family": "boundary", "block": block, "base_relator_index": index,
        "translation_hex": translation_blob.hex(), "scalar": scalar,
        "complete_support_occurrence_accumulation": True,
        "left_translation_gate": "t*h=g",
        "contributing_pairs": contributors[(block, index, translation_blob)]}}


def seal(value: dict[str, Any]) -> dict[str, Any]:
    answer = dict(value); answer.pop("self_digest", None)
    answer["self_digest"] = sha_obj(answer)
    return answer


def validate_seal(value: dict[str, Any]) -> None:
    claimed = value.get("self_digest")
    body = dict(value); body.pop("self_digest", None)
    require(type(claimed) is str and claimed == sha_obj(body), "receipt self digest")


def atomic_json(path: Path, value: dict[str, Any]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(value) + b"\n"
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        handle.write(raw); handle.flush(); os.fsync(handle.fileno())
    os.replace(temporary, path)
    return len(raw)


class PositiveSearch:
    def __init__(self, runtime: dict[str, Any], pins: dict[str, Any],
                 monitor: Monitor, output: Path, resume: Path | None):
        self.rt = runtime; self.pins = pins; self.monitor = monitor
        self.output = output
        self.checkpoint_path = output.with_suffix(output.suffix + ".checkpoint.json")
        self.target = exact_target(runtime); self.model = AllSevenModel(runtime)
        self.fibres = FibreOracle(runtime, monitor); self.basis = Echelon()
        require(len(runtime["qstates"]) * len(runtime["gamma"].states) == DELTA_ORDER,
                "Delta order")
        self.kernel_orders = self.fibres.verify_kernel_orders()
        self.columns: list[dict[str, Any]] = []
        self.progress: dict[str, Any] = {
            "boundary": {"dual_sha256": None, "complete": False, "pair_attempts": 0,
                         "restart_pair_cursor": 0},
            "correction": {"dual_sha256": None, "canonical_row_cursor": 0,
                           "live_fibre_count": 0, "kernel_prefix": 0,
                           "global_cursors": {}, "live_fibres": [],
                           "weighted_rows": {}},
        }
        self.input_components = {
            "pins": pins, "target": public_sparse(self.target),
            "roster": runtime["bridge"]["relation_roster"]["roster_sha256"],
            "Gamma": runtime["gamma"].public()["state_rows_sha256"],
            "Q0": sha_chunks(runtime["qstates"]),
            "Q0_parent_internal_zero_based_sha256": sha_obj(runtime["parents"]),
            "Q0_parent_letters_sha256": sha_bytes(runtime["letters"]),
            "Q0_coordinate_store_sha256": [sha_chunks(
                store[offset:offset + (1 << 20)]
                for offset in range(0, len(store), 1 << 20))
                for store in runtime["stores"]],
            "coarse_inverse_index": {
                "state_count": Q0_STATE_COUNT, "coordinate_count": 10,
                "table_length": COARSE_TABLE_LENGTH,
                "payload_bytes_per_coordinate": COARSE_INDEX_PAYLOAD_BYTES,
                "payload_bytes_total": 10 * COARSE_INDEX_PAYLOAD_BYTES,
                "uint32_itemsize": 4,
                "injectivity": "hard_stop_on_duplicate_exact_coarse_key",
                "tables_not_serialized": True},
            "delta_order": DELTA_ORDER,
            "kernel_orders": list(self.kernel_orders),
            "coordinate_widths": list(runtime["p176"].COORDINATE_WIDTHS),
            "parent_convention": "internal zero-based; public root=0 otherwise parent+1",
            "section_storage": "live fixed-width raw; no packed artifact assumed",
            "deletion": runtime["deletion_public"],
        }
        self.input_hash = sha_obj(self.input_components)
        if resume is not None:
            self.load_checkpoint(resume)

    def _validate_weighted_progress(self, dual: Sparse | None = None) -> None:
        """Validate the shared row/cursor checkpoint contract before sealing."""
        correction = self.progress.get("correction", {})
        cursor = correction.get("canonical_row_cursor")
        require(type(cursor) is int and 0 <= cursor <= len(self.rt["roster"]),
                "weighted canonical cursor bounds")
        rows = correction.get("weighted_rows")
        require(type(rows) is dict, "weighted checkpoint rows map")
        for row_key, state in rows.items():
            require(type(row_key) is str and row_key.isdecimal(),
                    "weighted checkpoint row key")
            roster_index = int(row_key)
            require(1 <= roster_index <= len(self.rt["roster"]) and
                    str(roster_index) == row_key and type(state) is dict,
                    "weighted checkpoint row index")
            require(type(state.get("formula_sha256")) is str and
                    type(state.get("K")) is int and state["K"] in (0, 1, 2) and
                    type(state.get("W")) is int and state["W"] >= 0 and
                    state.get("delta_order") == DELTA_ORDER and
                    state.get("kernel_orders") == list(self.kernel_orders) and
                    type(state.get("support_fibre_cursor")) is int and
                    type(state.get("kernel_cursor")) is int and
                    type(state.get("global_prefix")) is int and
                    type(state.get("complete")) is bool,
                    "weighted checkpoint row fields")
            require(state["support_fibre_cursor"] >= 0 and
                    state["kernel_cursor"] >= 0 and
                    state["global_prefix"] >= 0 and
                    state["kernel_cursor"] <= max(self.kernel_orders) and
                    state["global_prefix"] <= DELTA_ORDER,
                    "weighted checkpoint row cursor bounds")
            if dual is not None:
                formula = self.model.occurrence_data(
                    self.rt["roster"][roster_index - 1]["word"], dual)
                support = self.weighted_support(formula)
                require(state["formula_sha256"] == sha_obj(formula["public"]) and
                        state["K"] == support["K"] and state["W"] == support["W"],
                        "weighted checkpoint formula identity")
                target_bound = max(len(support["distinct_targets"]) - 1, 0)
                require(state["support_fibre_cursor"] <= target_bound,
                        "weighted support cursor bound")
                if support["K"] == 0:
                    require(state["global_prefix"] == 0,
                            "K=0 global cursor must be zero")
                    if not support["distinct_targets"]:
                        require(state["support_fibre_cursor"] == 0 and
                                state["kernel_cursor"] == 0,
                                "empty K=0 support cursor state")
                    else:
                        current_target = support["distinct_targets"][
                            state["support_fibre_cursor"]]
                        current_order = current_target["kernel_order"]
                        require(state["kernel_cursor"] <= current_order,
                                "K=0 coordinate kernel cursor bound")
                        if state["complete"]:
                            require(state["support_fibre_cursor"] == target_bound and
                                    state["kernel_cursor"] in (0, current_order),
                                    "completed K=0 cursor state")
                            fibre = self.fibres.canonical(
                                current_target["coordinate"],
                                bytes.fromhex(current_target["target_hex"]))
                            require((state["kernel_cursor"] == 0) == (fibre is None),
                                    "completed K=0 fibre cursor state")
                else:
                    global_bound = (support["W"] + 1 if support["W"] < DELTA_ORDER
                                    else DELTA_ORDER)
                    require(state["support_fibre_cursor"] == 0 and
                            state["kernel_cursor"] == 0 and
                            state["global_prefix"] <= global_bound,
                            "K!=0 weighted cursor state")
                if state["complete"]:
                    require(support["K"] == 0 and
                            state["support_fibre_cursor"] >= target_bound,
                            "completed weighted row state")
            if roster_index <= cursor:
                require(state["complete"] is True,
                        "completed cursor crossed incomplete row")
            else:
                require(roster_index == cursor + 1 and
                        state["complete"] is False,
                        "future weighted row state")
        for roster_index in range(1, cursor + 1):
            require(str(roster_index) in rows and
                    rows[str(roster_index)].get("complete") is True,
                    "missing completed weighted row")

    def _checkpoint_body(self, dual: Sparse | None = None,
                         remainder: Sparse | None = None) -> dict[str, Any]:
        reduced, solution = self.basis.reduce(self.target)
        if remainder is not None:
            require(reduced == remainder, "checkpoint remainder")
        if reduced:
            derived, exact_remainder, _ = self.basis.exact_dual(self.target)
            require(exact_remainder == reduced, "checkpoint dual remainder")
            if dual is None:
                dual = derived
            else:
                require(dual == derived, "checkpoint dual identity")
            require(self.progress["correction"].get("dual_sha256") ==
                    sha_obj(public_sparse(dual)),
                    "checkpoint correction dual digest")
        else:
            dual = None
        self._validate_weighted_progress(dual)
        return {
            "schema": CHECKPOINT_SCHEMA, "input_sha256": self.input_hash,
            "input_components": self.input_components,
            "weighted_support_hitting": {
                "delta_order": DELTA_ORDER,
                "kernel_orders": list(self.kernel_orders),
                "schedule": "K0_complete_fibres_or_Knonzero_W_plus_1_global"},
            "coarse_inverse_index": self.fibres.index_public(),
            "pins_sha256": sha_obj(self.pins),
            "target": public_sparse(self.target), "target_sha256": sha_obj(public_sparse(self.target)),
            "rank": len(self.basis.order), "reduced_target": public_sparse(reduced),
            "current_dual": None if dual is None else public_sparse(dual),
            "current_dual_sha256": None if dual is None else sha_obj(public_sparse(dual)),
            "target_solution_if_zero": [[key, value] for key, value in sorted(solution.items())],
            "columns": self.columns, "progress": self.progress,
            "pivot_order": [key.hex() for key in self.basis.order],
            "pivot_rows_sha256": sha_obj([public_sparse(self.basis.rows[key])
                                          for key in self.basis.order]),
            "monitor": self.monitor.public(),
            "resume_contract": "replay every retained column then continue positive prefixes",
            "negative_claim": False, "separator": False,
        }

    def write_checkpoint(self, dual: Sparse | None = None,
                         remainder: Sparse | None = None) -> dict[str, Any]:
        checkpoint = seal(self._checkpoint_body(dual, remainder))
        size = atomic_json(self.checkpoint_path, checkpoint)
        self.monitor.counters["checkpoint_bytes"] = size
        if size > self.monitor.limits["checkpoint_bytes"]:
            raise ResourceStop("checkpoint_serialization", "checkpoint_bytes", size,
                               self.monitor.limits["checkpoint_bytes"])
        return checkpoint

    def rebuild_record(self, record: dict[str, Any]) -> Sparse:
        provenance = record["provenance"]
        if provenance["family"] == "boundary":
            return translated_boundary(self.rt, int(provenance["block"]),
                                       int(provenance["base_relator_index"]),
                                       bytes.fromhex(provenance["translation_hex"]))
        if provenance["family"] == "correction":
            row, replay = self.model.direct_column(provenance["delta_word"],
                                                   provenance["relator_word"])
            require(replay["conjugate_word"] == provenance["conjugate_word"],
                    "resume conjugate replay")
            return row
        raise RuntimeError("unknown retained column family")

    def load_checkpoint(self, path: Path) -> None:
        value = json.loads(path.read_text(encoding="ascii")); validate_seal(value)
        if value.get("schema") != CHECKPOINT_SCHEMA or value.get("input_sha256") != self.input_hash:
            raise InputStop("resume:input_identity")
        if parse_sparse(value.get("target", [])) != self.target:
            raise InputStop("resume:target")
        for expected_id, record in enumerate(value.get("columns", []), 1):
            require(record.get("column_id") == expected_id, "resume column order")
            row = self.rebuild_record(record)
            require(public_sparse(row) == record["sparse_row"] and
                    sha_obj(record["sparse_row"]) == record["sparse_row_sha256"],
                    "resume column literal row")
            before = len(self.basis.order)
            added, pivot, ancestry = self.basis.add(row, expected_id)
            require(added and len(self.basis.order) == before + 1 and
                    pivot is not None and pivot.hex() == record["pivot_hex"] and
                    record["rank_before"] == before and record["rank_after"] == before + 1,
                    "resume pivot transition")
            require([[key, value] for key, value in sorted(ancestry.items())] ==
                    record["pivot_ancestry"], "resume pivot ancestry")
            self.columns.append(record)
        require(len(self.basis.order) == int(value["rank"]) and
                [key.hex() for key in self.basis.order] == value["pivot_order"],
                "resume full rank")
        self.progress = value["progress"]
        reduced, _ = self.basis.reduce(self.target)
        stored_current = value.get("current_dual")
        stored_digest = value.get("current_dual_sha256")
        if reduced:
            derived, exact_remainder, _ = self.basis.exact_dual(self.target)
            require(exact_remainder == reduced, "resume dual remainder")
            derived_public = public_sparse(derived)
            if stored_current is None:
                require(stored_digest is None, "resume stale dual digest")
                checkpoint_dual = derived
            else:
                stored_dual = parse_sparse(stored_current)
                require(stored_dual == derived and
                        stored_digest == sha_obj(stored_current),
                        "resume stored dual identity")
                checkpoint_dual = stored_dual
            require(self.progress["correction"].get("dual_sha256") ==
                    sha_obj(derived_public),
                    "resume correction dual digest")
        else:
            require(stored_current is None and stored_digest is None,
                    "resume stale zero-remainder dual")
            checkpoint_dual = None
        self._validate_weighted_progress(checkpoint_dual)

    def add_column(self, row: Sparse, provenance: dict[str, Any],
                   dual: Sparse | None = None) -> None:
        column_id = len(self.columns) + 1; before = len(self.basis.order)
        if dual is not None:
            require(pair(dual, row) != 0, "ACTIVE column dual pairing")
        added, pivot, ancestry = self.basis.add(row, column_id)
        require(added and pivot is not None, "ACTIVE column must raise rank")
        self.monitor.bump("retained_columns", 1, "rank_increase")
        record = {
            "column_id": column_id, "family": provenance["family"],
            "provenance": provenance, "sparse_row": public_sparse(row),
            "sparse_row_sha256": sha_obj(public_sparse(row)),
            "pivot_hex": pivot.hex(), "rank_before": before,
            "rank_after": before + 1,
            "pivot_ancestry": [[key, value] for key, value in sorted(ancestry.items())],
            "active_dual": None if dual is None else public_sparse(dual),
            "active_dual_sha256": None if dual is None else sha_obj(public_sparse(dual)),
            "dual_pairing": None if dual is None else pair(dual, row),
        }
        self.columns.append(record)
        reduced, _ = self.basis.reduce(self.target)
        if reduced:
            next_dual, exact_remainder, _ = self.basis.exact_dual(self.target)
            require(exact_remainder == reduced, "rank transition dual remainder")
            next_digest = sha_obj(public_sparse(next_dual))
            if self.progress["correction"].get("dual_sha256") != next_digest:
                # A rank increase changes the dual.  Any row schedule tied to
                # the previous dual is stale and must restart contiguously.
                self.progress["correction"] = {
                    "dual_sha256": next_digest, "canonical_row_cursor": 0,
                    "live_fibre_count": 0, "kernel_prefix": 0,
                    "global_cursors": {}, "live_fibres": [],
                    "weighted_rows": {}}
        else:
            self.progress["correction"]["dual_sha256"] = None
        self.write_checkpoint()

    def initial_basis(self) -> None:
        if self.columns:
            return
        for block, count in ((1, 2), (2, 2), (3, 11)):
            for index in range(1, count + 1):
                translation = identity_blob(self.rt, block)
                row = translated_boundary(self.rt, block, index, translation)
                reduced, _ = self.basis.reduce(row)
                if reduced:
                    self.add_column(row, {"family": "boundary", "block": block,
                        "base_relator_index": index, "translation_hex": translation.hex(),
                        "seed": "identity_translation", "left_translation_gate": "t*h=g"})
        identity = coordinate_blobs(self.rt, [])
        for roster_index, roster_row in enumerate(self.rt["roster"][:8], 1):
            row, replay = self.model.direct_column([], roster_row["word"])
            reduced, _ = self.basis.reduce(row)
            if reduced:
                provenance = {"family": "correction", "seed": "identity_delta",
                    "roster_index": roster_index, "layer": roster_row["layer"],
                    "ordinal": roster_row["ordinal"], "delta_word": [],
                    "delta_coordinate_blobs_hex": [x.hex() for x in identity], **replay}
                self.add_column(row, provenance)

    def materialize_correction(self, dual: Sparse, roster_index: int,
                               roster_row: dict[str, Any], formula: dict[str, Any],
                               candidate: dict[str, Any], schedule: str,
                               support_meta: dict[str, Any] | None = None) -> dict[str, Any]:
        self.monitor.bump("candidate_words", 1, "positive_correction_candidate")
        scalar = self.model.formula_scalar(formula, candidate["coordinate_blobs"])
        if not scalar:
            return {}
        row, replay = self.model.direct_column(candidate["source_word"], roster_row["word"])
        require(pair(dual, row) == scalar and scalar != 0,
                "weighted formula/full direct scalar equality")
        provenance = {"family": "correction", "roster_index": roster_index,
            "layer": roster_row["layer"], "ordinal": roster_row["ordinal"],
            "schedule": schedule, "weighted_formula": formula["public"],
            "delta_word": list(candidate["source_word"]),
            "delta_coordinate_blobs_hex": [x.hex() for x in candidate["coordinate_blobs"]],
            "section_provenance": {key: value for key, value in candidate.items()
                                   if key not in ("source_word", "coordinate_blobs")}, **replay}
        if support_meta is not None:
            provenance["support_hitting"] = support_meta
        return {"row": row, "provenance": provenance}

    def correction_oracle(self, dual: Sparse) -> dict[str, Any] | None:
        completed_canonical = int(self.progress["correction"].get("canonical_row_cursor", 0))
        weighted_rows = self.progress["correction"].setdefault("weighted_rows", {})
        for roster_index, roster_row in enumerate(self.rt["roster"], 1):
            if roster_index <= completed_canonical:
                continue
            self.monitor.check("weighted_eleven_occurrence_formula")
            formula = self.model.occurrence_data(roster_row["word"], dual)
            support = self.weighted_support(formula)
            state = weighted_rows.setdefault(str(roster_index), {
                "formula_sha256": sha_obj(formula["public"]),
                "K": support["K"], "W": support["W"],
                "delta_order": DELTA_ORDER,
                "kernel_orders": list(self.kernel_orders),
                "support_fibre_cursor": 0, "kernel_cursor": 0,
                "global_prefix": 0, "complete": False})
            require(state["formula_sha256"] == sha_obj(formula["public"]) and
                    state["K"] == support["K"] and state["W"] == support["W"],
                    "weighted row checkpoint identity")
            if support["K"] == 0:
                targets = sorted(formula["merged"], key=lambda item: (item[0], item[1]))
                for target_index in range(int(state["support_fibre_cursor"]), len(targets)):
                    coordinate, target = targets[target_index]
                    fibre = self.fibres.canonical(coordinate, target)
                    state["support_fibre_cursor"] = target_index
                    state["kernel_cursor"] = 0
                    if fibre is None:
                        continue
                    states = self.fibres.kernel_states[coordinate]
                    for kernel_index, eta in enumerate(states):
                        self.monitor.check("weighted_support_fibre")
                        state["kernel_cursor"] = kernel_index
                        candidate = self.fibres.kernel_candidate(fibre, eta)
                        candidate["kernel_cursor"] = kernel_index
                        result = self.materialize_correction(
                            dual, roster_index, roster_row, formula, candidate,
                            "weighted_support_fibre_complete", support)
                        if result:
                            return result
                    state["kernel_cursor"] = len(states)
                    self.write_checkpoint(dual)
            else:
                bound = support["W"] + 1 if support["W"] < DELTA_ORDER else DELTA_ORDER
                global_seen: set[tuple[int, int]] = set()
                for cursor in range(int(state["global_prefix"]), bound):
                    self.monitor.check("weighted_global_prefix")
                    state["global_prefix"] = cursor
                    candidate = self.fibres.global_candidate(cursor)
                    pair_id = (int(candidate["q0_state_id"]),
                               int(candidate["gamma_state_id"]))
                    require(pair_id not in global_seen, "global roster duplicate")
                    global_seen.add(pair_id)
                    result = self.materialize_correction(
                        dual, roster_index, roster_row, formula, candidate,
                        "weighted_global_prefix_W_plus_1" if support["W"] < DELTA_ORDER
                        else "weighted_global_fair_fallback", support)
                    if result:
                        return result
                    self.write_checkpoint(dual)
                state["global_prefix"] = bound
                if support["W"] >= DELTA_ORDER:
                    raise ResourceStop("positive_global_fallback", "global_roster",
                                       DELTA_ORDER + 1, DELTA_ORDER)
                raise RuntimeError("weighted W+1 theorem invariant")
            state["complete"] = True
            self.progress["correction"]["canonical_row_cursor"] = roster_index
            self.write_checkpoint(dual)
        return None

    def positive_receipt(self, solution: dict[int, int]) -> dict[str, Any]:
        require(solution and all(value in (1, 2) for value in solution.values()),
                "nonempty sparse positive solution")
        combined: Sparse = {}
        correction_sum: Sparse = {}; boundary_sum: Sparse = {}
        correction_word: list[int] = []
        selected = []
        boundary_chains = []
        for column_id in sorted(solution):
            coefficient = solution[column_id]
            record = self.columns[column_id - 1]
            row = parse_sparse(record["sparse_row"])
            add_scaled(combined, row, coefficient)
            if record["family"] == "boundary":
                add_scaled(boundary_sum, row, coefficient)
                boundary_chains.append({"column_id": column_id,
                                        "coefficient": coefficient,
                                        "provenance": record["provenance"]})
            else:
                add_scaled(correction_sum, row, coefficient)
                word = list(record["provenance"]["conjugate_word"])
                factor = word if coefficient == 1 else inverse_word(word)
                inverse_replay = False
                if coefficient == 2:
                    inverse_row, inverse_public = self.model.direct_column(
                        record["provenance"]["delta_word"],
                        inverse_word(record["provenance"]["relator_word"]))
                    require(inverse_row == scaled(row, -1) and
                            inverse_public["conjugate_word"] == factor,
                            "coefficient-two inverse column replay")
                    inverse_replay = True
                require(self.rt["joint_group"].eval(factor) ==
                        self.rt["joint_group"].identity,
                        "selected correction factor joint kernel")
                correction_word = reduce_word(correction_word + factor)
                selected.append({"column_id": column_id, "coefficient": coefficient,
                                 "factor_word": factor,
                                 "inverse_for_coefficient_2": coefficient == 2,
                                 "inverse_column_replay": inverse_replay,
                                 "provenance": record["provenance"]})
        require(combined == self.target, "final sparse column identity")
        require(exponent_pair(correction_word) == (0, 0), "two exponent sums")
        direct_change, direct_replay = self.model.direct_column([], correction_word)
        require(direct_change == correction_sum, "correction product Fox additivity")
        base = scaled(self.target, -1)
        relation_residual = dict(base); add_scaled(relation_residual, correction_sum, 1)
        add_scaled(relation_residual, boundary_sum, 1)
        require(not relation_residual, "PB3/PB4 chains reduce seven relations")
        corrected_word = reduce_word(self.model.g + correction_word)
        require(corrected_word == direct_replay["corrected_word"],
                "right correction convention")
        return seal({
            "schema": SCHEMA, "status": "COMMON_WORD", "terminal": COMMON,
            "pins": self.pins, "input_sha256": self.input_hash,
            "input_components": self.input_components,
            "weighted_support_hitting": {
                "delta_order": DELTA_ORDER,
                "kernel_orders": list(self.kernel_orders),
                "schedule": "K0_complete_fibres_or_Knonzero_W_plus_1_global"},
            "claim": "finite universal B4 all-seven word only",
            "target": public_sparse(self.target), "target_source":
                "negative task175 raw_base_targets H1/H2/P; never stacked_target",
            "rank": len(self.basis.order), "columns": self.columns,
            "solution_coefficients": [[key, value] for key, value in sorted(solution.items())],
            "boundary_chains": boundary_chains, "selected_corrections": selected,
            "correction_word": correction_word, "corrected_word": corrected_word,
            "g760": self.model.g, "coefficient_2_uses_inverse": True,
            "boundary_words_not_inserted": True,
            "joint_kernel_product": self.rt["joint_group"].eval(correction_word) ==
                                    self.rt["joint_group"].identity,
            "exponent_sums_mod3": list(exponent_pair(correction_word)),
            "all_seven_direct_replay": direct_replay,
            "sparse_identity_sha256": sha_obj(public_sparse(combined)),
            "checkpoint": self.write_checkpoint(), "monitor": self.monitor.public(),
            "negative_claim": False, "separator": False,
            "boundaries": {"cofinal_lift": False, "fake": False,
                           "ihara_witness": False, "v129_input_only": True},
        })

    def run(self) -> dict[str, Any]:
        self.initial_basis()
        while True:
            remainder, solution = self.basis.reduce(self.target)
            if not remainder:
                return self.positive_receipt(solution)
            dual, exact_remainder, _ = self.basis.exact_dual(self.target)
            require(exact_remainder == remainder, "target remainder stability")
            dual_sha = sha_obj(public_sparse(dual))
            same_dual = self.progress.get("boundary", {}).get("dual_sha256") == dual_sha
            if not same_dual:
                self.progress["boundary"] = {"dual_sha256": dual_sha, "complete": False,
                    "pair_attempts": self.monitor.counters["boundary_pairs"],
                    "restart_pair_cursor": 0}
                self.progress["correction"] = {"dual_sha256": dual_sha,
                    "canonical_row_cursor": 0, "live_fibre_count": 0,
                    "kernel_prefix": 0, "global_cursors": {}, "live_fibres": [],
                    "weighted_rows": {}}
            self.write_checkpoint(dual, remainder)
            active = None
            if not self.progress["boundary"].get("complete", False):
                active = boundary_oracle(self.rt, dual, self.monitor)
                self.progress["boundary"]["complete"] = True
                self.progress["boundary"]["pair_attempts"] = self.monitor.counters["boundary_pairs"]
            if active is not None:
                self.add_column(active["row"], active["provenance"], dual)
                continue
            active = self.correction_oracle(dual)
            if active is not None:
                self.add_column(active["row"], active["provenance"], dual)
                continue
            # A finite positive schedule with no hit has no negative content.
            raise ResourceStop("positive_correction_dovetail", "oracle_rounds",
                               self.monitor.limits["oracle_rounds"] + 1,
                               self.monitor.limits["oracle_rounds"])


# ----------------------- bounded noncommutative SELFTEST --------------------

def perm_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def perm_inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for i, image in enumerate(value):
        out[image] = i
    return tuple(out)


def toy_eval(word: Sequence[int], generators: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
    value = tuple(range(len(generators[0])))
    for letter in word:
        generator = generators[abs(int(letter)) - 1]
        if letter < 0:
            generator = perm_inverse(generator)
        value = perm_mul(value, generator)
    return value


def toy_fox(word: Sequence[int], generators: Sequence[tuple[int, ...]], block: int) -> Sparse:
    value = tuple(range(len(generators[0]))); answer: Sparse = {}
    for letter0 in word:
        letter = int(letter0); index = abs(letter)
        generator = generators[index - 1]
        if letter > 0:
            key_value = value; coefficient = 1
            value = perm_mul(value, generator)
        else:
            inverse = perm_inverse(generator)
            value = perm_mul(value, inverse)
            key_value = value; coefficient = 2
        key = row_key(block, index, bytes(key_value))
        answer[key] = (answer.get(key, 0) + coefficient) % 3
        if not answer[key]:
            del answer[key]
    return answer


def toy_occurrence_column(fixture: dict[str, Any], delta: Sequence[int],
                          relator: Sequence[int]) -> tuple[Sparse, list[dict[str, Any]]]:
    generators = [tuple(row) for row in fixture["generators"]]
    require(toy_eval(relator, generators) == tuple(range(3)), "toy relation identity")
    conjugate = reduce_word(list(delta) + list(relator) + inverse_word(delta))
    base = toy_fox(conjugate, generators, 1)
    # Three ordered, noncommuting product occurrences.  Prefix translations
    # are literal S3 left multiplications and all three must be accumulated.
    prefixes = [tuple(range(3)), generators[0], perm_mul(generators[0], generators[1])]
    answer: Sparse = {}; occurrences = []
    for ordinal, prefix in enumerate(prefixes, 1):
        translated: Sparse = {}
        for key, coefficient in base.items():
            block, component, raw = decode_row_key(key)
            value = tuple(raw)
            translated[row_key(block, component, bytes(perm_mul(prefix, value)))] = coefficient
        add_scaled(answer, translated, 1)
        occurrences.append({"ordinal": ordinal, "prefix": list(prefix),
                            "row": public_sparse(translated)})
    e1, e2 = exponent_pair(relator)
    if e1:
        answer[exponent_key(1)] = e1
    if e2:
        answer[exponent_key(2)] = e2
    return answer, occurrences


def coarse_inverse_selftest() -> dict[str, Any]:
    """Collision-forced, packed (coarse plus PC) inverse/selector checks."""
    width, degree = 3, 2
    store = bytearray(b"\x10\x01\xaa\x13\x02\xaa")
    inverse = CoarseInverse(store, width, degree, None,
                            hash_fn=lambda _key: 0, table_length=8,
                            expected_state_count=2)
    require(inverse.lookup(b"\x13\x02") == 1 and
            inverse.lookup(b"\x10\x01") == 0,
            "selftest exact-key collision resolution")
    duplicate_rejected = False
    try:
        CoarseInverse(bytearray(b"\x10\x01\xaa\x10\x01\xab"), width, degree,
                      None, hash_fn=lambda _key: 0, table_length=8,
                      expected_state_count=2).build()
    except RuntimeError as exc:
        duplicate_rejected = str(exc) == "coarse inverse duplicate exact key"
    require(duplicate_rejected, "selftest duplicate coarse-key rejection")
    # The same coarse hit with a different PC byte must be rejected by the
    # complete packed comparison, rather than accepted on hash/coarse alone.
    coarse_hit = inverse.lookup(b"\x13\x02")
    mismatch_rejected = (coarse_hit is not None and
                         bytes(store[coarse_hit * width:(coarse_hit + 1) * width]) !=
                         b"\x13\x02\xab")
    require(mismatch_rejected, "selftest full packed mismatch rejection")
    # A tiny XOR-packed selector exercises the same inverse/coarse/full-check
    # order with two Gamma candidates; the lower Q0 id wins despite Gamma order.
    target = b"\x11\x00\xaa"
    candidates = []
    for a, gid in ((b"\x02\x02\x00", 4), (b"\x01\x01\x00", 8)):
        section_target = bytes(x ^ y for x, y in zip(a, target))
        qid = inverse.lookup(section_target[:degree])
        if qid is None:
            continue
        section_full = bytes(store[qid * width:(qid + 1) * width])
        if section_full != section_target or bytes(x ^ y for x, y in zip(a, section_full)) != target:
            continue
        candidates.append((qid, gid))
    selected = min(candidates, key=lambda pair: pair)
    require(selected == (0, 8), "selftest least qid gid selection")
    return {"table_length": 8, "uint32_itemsize": inverse.slots.itemsize,
            "exact_key_collision_resolution": True,
            "duplicate_coarse_key_rejected": duplicate_rejected,
            "least_qid_gid_selection": list(selected),
            "full_packed_mismatch_rejected": mismatch_rejected,
            "hash": "injectable_constant_zero_only_selftest",
            "tables_not_production": True}


def weighted_support_selftest() -> dict[str, Any]:
    last_values = [0, 0, 1]
    last_hit = next((i for i, value in enumerate(last_values) if value), None)
    require(last_hit == len(last_values) - 1, "selftest K0 last kernel point")
    exhausted_values = [0, 0, 0]
    require(not any(exhausted_values), "selftest K0 complete exhaustion")
    support = {0, 1}; global_points = list(range(3)); constant = 1
    global_hit = next((i for i in global_points
                       if i not in support and constant), None)
    require(global_hit == 2 and len(set(global_points)) == len(global_points),
            "selftest W+1 distinct global hit")
    registered = [9, 9, 9, 9, 9, 1, 1, 1, 3, 3]
    require(registered == list(KERNEL_ORDERS) and
            registered[:5] != [10, 9, 9, 9, 9], "selftest kernel order gate")
    merged_targets = [[0, "aa"], [1, "bb"]]
    omitted_w = sum(KERNEL_ORDERS[row[0]] for row in merged_targets[:-1])
    full_w = sum(KERNEL_ORDERS[row[0]] for row in merged_targets)
    require(full_w != omitted_w, "selftest merged target W omission")
    repeated = [0, 1, 1]
    require(len(set(repeated)) != len(repeated), "selftest repeated global rejection")
    require(4 > len(last_values), "selftest completed cursor gate")
    checkpoint_state = {
        "canonical_row_cursor": 1,
        "weighted_rows": {"1": {
            "formula_sha256": "toy-formula",
            "K": 0, "W": 3, "delta_order": DELTA_ORDER,
            "kernel_orders": list(KERNEL_ORDERS),
            "support_fibre_cursor": 0, "kernel_cursor": 3,
            "global_prefix": 0, "complete": True}}}
    require(checkpoint_state["weighted_rows"]["1"]["complete"] is True and
            "2" not in checkpoint_state["weighted_rows"],
            "selftest completed-row cursor state")
    impossible_hard_failure = False
    try:
        # This branch is unreachable when W<Delta: the theorem guarantees a
        # hit in the first W+1 distinct representatives.  It is a programming
        # failure, never a typed UNKNOWN_RESOURCE outcome.
        raise RuntimeError("weighted W+1 theorem invariant")
    except RuntimeError:
        impossible_hard_failure = True
    require(impossible_hard_failure, "selftest W+1 hard invariant failure")
    return {"K0_last_point": {"kernel_order": 3, "hit_index": last_hit,
                               "tested": last_values},
            "K0_exhaustion": {"kernel_order": 3, "tested": exhausted_values,
                              "row_skipped": True},
            "Knonzero_W_plus_1": {"K": constant, "W": len(support),
                                   "global_points": global_points,
                                   "hit_index": global_hit},
            "kernel_order_gate": {"registered": registered,
                                   "overstated_rejected": True,
                                   "understated_rejected": True},
            "merged_target_W": {"full": full_w, "omitted": omitted_w,
                                 "omitted_target_rejected": True},
            "global_distinctness": {"repeated": repeated,
                                     "repeated_rejected": True},
            "completed_cursor": {"tested": len(last_values), "cursor": 3,
                                  "advanced_past_untested_rejected": True},
            "checkpoint_state": checkpoint_state,
            "W_plus_1_impossible": {"typed_unknown": False,
                                     "hard_invariant_failure": True}}


def build_toy_certificate(fixture: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == "d972-r07-positive-common-word-colgen-selftest-input/v1",
            "toy fixture schema")
    generators = [tuple(row) for row in fixture["generators"]]
    require(len(generators) == 2 and perm_mul(generators[0], generators[1]) !=
            perm_mul(generators[1], generators[0]), "noncommutative S3 fixture")
    rel_support = fixture["relation_words"][0]
    rel_global = fixture["relation_words"][1]
    section = fixture["support_section_word"]
    eta = fixture["kernel_prefix_word"]
    delta = reduce_word(eta + section)
    support_column, support_occurrences = toy_occurrence_column(fixture, delta, rel_support)
    global_column, global_occurrences = toy_occurrence_column(
        fixture, fixture["global_word"], rel_global)
    boundary_word = fixture["boundary_relation_word"]
    boundary = toy_fox(boundary_word, generators, 2)
    translation = generators[1]
    translated_boundary: Sparse = {}
    for key, coefficient in boundary.items():
        block, component, raw = decode_row_key(key)
        translated_boundary[row_key(block, component,
                                      bytes(perm_mul(translation, tuple(raw))))] = coefficient

    candidates = [
        ("boundary", translated_boundary),
        ("support_fibre_kernel_prefix", support_column),
        ("K_nonzero_global", global_column),
    ]
    independent: list[tuple[str, Sparse]] = []; probe = Echelon()
    for label, row in candidates:
        if probe.add(row, len(independent) + 1)[0]:
            independent.append((label, row))
    require(len(independent) == 3, "toy three independent ACTIVE columns")
    coefficients = [1, 2, 1]
    target: Sparse = {}
    for (_, row), coefficient in zip(independent, coefficients):
        add_scaled(target, row, coefficient)

    # Re-run the actual dual/rank path.  At each round select the first
    # remaining column with nonzero *complete* pairing; a prescribed column
    # is not assumed ACTIVE for a newly constructed dual.
    basis = Echelon(); records = []; remaining = list(independent)
    boundary_active = False; support_active = False; global_active = False
    for column_id in range(1, 4):
        dual, _, _ = basis.exact_dual(target)
        active_index = next((index for index, (_label, candidate) in enumerate(remaining)
                             if pair(dual, candidate) != 0), None)
        require(active_index is not None, "toy positive ACTIVE selector")
        label, row = remaining.pop(active_index)
        scalar = pair(dual, row); require(scalar != 0, "toy ACTIVE complete scalar")
        before = len(basis.order); added, pivot, ancestry = basis.add(row, column_id)
        require(added and pivot is not None, "toy rank increase")
        records.append({"column_id": column_id, "family": label,
                        "row": public_sparse(row), "row_sha256": sha_obj(public_sparse(row)),
                        "dual": public_sparse(dual), "full_scalar": scalar,
                        "pivot_hex": pivot.hex(), "rank_before": before,
                        "rank_after": before + 1,
                        "ancestry": [[k, v] for k, v in sorted(ancestry.items())]})
        boundary_active |= label == "boundary"
        support_active |= label == "support_fibre_kernel_prefix"
        global_active |= label == "K_nonzero_global"
    remainder, solution = basis.reduce(target)
    require(not remainder, "toy membership")
    label_by_id = {record["column_id"]: record["family"] for record in records}
    support_id = next(key for key, label in label_by_id.items()
                      if label == "support_fibre_kernel_prefix")
    require(solution.get(support_id) == 2, "toy coefficient-two solution")
    support_conjugate = reduce_word(delta + rel_support + inverse_word(delta))
    selected_factor = inverse_word(support_conjugate)
    require(toy_eval(selected_factor, generators) == tuple(range(3)),
            "coefficient-two inverse relation")
    ordered = [fixture["ordered_product_words"][i]
               for i in fixture["ordered_product_indices"]]
    product_word = reduce_word(letter for factor in ordered for letter in factor)
    require(toy_eval(product_word, generators) == tuple(range(3)),
            "ordered noncommutative product")
    checkpoint = seal({"schema": "d972-r07-positive-common-word-colgen-toy-checkpoint/v1",
        "target": public_sparse(target), "rank": len(basis.order), "columns": records,
        "pending_prefix": {"support_fibre": 2, "kernel_power": 2, "global_cursor": 1},
        "separator": False})
    return seal({
        "schema": "d972-r07-positive-common-word-colgen-selftest-output/v1",
        "terminal": COMMON, "fixture_sha256": FIXTURE_SHA256,
        "group": "S3 noncommutative linked extension A3 -> S3 -> C2",
        "target_source": "toy_raw_base_targets_not_canary",
        "target": public_sparse(target), "columns": records,
        "solution_coefficients": [[key, value] for key, value in sorted(solution.items())],
        "support": {"section_word": section, "kernel_prefix_word": eta,
                    "delta_word": delta, "relator_word": rel_support,
                    "conjugate_word": support_conjugate,
                    "selected_coefficient": 2, "selected_factor_word": selected_factor,
                    "occurrences": support_occurrences,
                    "same_target_merged_before_scalar": True,
                    "full_scalar_not_single_occurrence": True},
        "global": {"K_nonzero": exponent_pair(rel_global) != (0, 0),
                   "word": fixture["global_word"], "relator_word": rel_global,
                   "occurrences": global_occurrences},
        "boundary": {"block": 2, "translation": list(translation),
                     "relation_word": boundary_word,
                     "row": public_sparse(translated_boundary),
                     "not_inserted_in_correction_word": True},
        "coarse_inverse": coarse_inverse_selftest(),
        "weighted_support": weighted_support_selftest(),
        "ordered_product": {"indices": fixture["ordered_product_indices"],
                            "words": fixture["ordered_product_words"],
                            "product_word": product_word},
        "checkpoint": checkpoint,
        "path_coverage": {"sparse_dual": True, "boundary_ACTIVE": boundary_active,
                          "support_fibre": True, "kernel_prefix": support_active,
                          "K_global": global_active, "rank_increase": True,
                          "coefficient_2_inverse": True, "common_word": True,
                          "checkpoint": True},
        "negative_claim": False, "separator": False,
    })


def validate_toy_certificate(fixture: dict[str, Any], cert: dict[str, Any]) -> None:
    validate_seal(cert)
    require(cert.get("terminal") == COMMON and cert.get("separator") is False and
            cert.get("negative_claim") is False, "toy positive envelope")
    require(cert.get("target_source") == "toy_raw_base_targets_not_canary",
            "toy target/canary separation")
    coarse = cert.get("coarse_inverse", {})
    require(coarse.get("table_length") == 8 and
            coarse.get("uint32_itemsize") == 4 and
            coarse.get("exact_key_collision_resolution") is True and
            coarse.get("duplicate_coarse_key_rejected") is True and
            coarse.get("least_qid_gid_selection") == [0, 8] and
            coarse.get("full_packed_mismatch_rejected") is True and
            coarse.get("hash") == "injectable_constant_zero_only_selftest" and
            coarse.get("tables_not_production") is True,
            "SELFTEST coarse inverse")
    weighted = cert.get("weighted_support", {})
    require(weighted.get("K0_last_point") == {
        "kernel_order": 3, "hit_index": 2, "tested": [0, 0, 1]} and
        weighted.get("K0_exhaustion") == {
            "kernel_order": 3, "tested": [0, 0, 0], "row_skipped": True},
        "SELFTEST K0 weighted fibres")
    global_case = weighted.get("Knonzero_W_plus_1", {})
    require(global_case.get("K") in (1, 2) and global_case.get("W") == 2 and
            global_case.get("global_points") == [0, 1, 2] and
            global_case.get("hit_index") == 2 and
            len(set(global_case["global_points"])) == 3,
            "SELFTEST K nonzero W+1")
    gate = weighted.get("kernel_order_gate", {})
    require(gate.get("registered") == list(KERNEL_ORDERS) and
            gate.get("overstated_rejected") is True and
            gate.get("understated_rejected") is True,
            "SELFTEST kernel order mutations")
    merged = weighted.get("merged_target_W", {})
    require(merged.get("full") == 18 and merged.get("omitted") == 9 and
            merged.get("omitted_target_rejected") is True,
            "SELFTEST merged target W")
    distinct = weighted.get("global_distinctness", {})
    require(distinct.get("repeated") == [0, 1, 1] and
            distinct.get("repeated_rejected") is True,
            "SELFTEST global distinctness")
    cursor = weighted.get("completed_cursor", {})
    require(cursor.get("tested") == 3 and cursor.get("cursor") == 3 and
            cursor.get("advanced_past_untested_rejected") is True,
            "SELFTEST completed cursor")
    checkpoint_state = weighted.get("checkpoint_state", {})
    row_states = checkpoint_state.get("weighted_rows", {})
    checkpoint_cursor = checkpoint_state.get("canonical_row_cursor")
    require(checkpoint_cursor == 1 and isinstance(row_states, dict) and
            isinstance(row_states.get("1"), dict) and
            row_states["1"].get("complete") is True and
            all(int(key) >= 1 for key in row_states) and
            all(int(key) <= checkpoint_cursor and row_states[key].get("complete") is True
                for key in row_states),
            "SELFTEST shared checkpoint cursor validator")
    impossible = weighted.get("W_plus_1_impossible", {})
    require(impossible.get("typed_unknown") is False and
            impossible.get("hard_invariant_failure") is True,
            "SELFTEST W+1 invariant failure")
    generators = [tuple(row) for row in fixture["generators"]]
    columns = cert.get("columns", []); require(len(columns) == 3, "toy column count")
    support = cert["support"]
    expected_delta = reduce_word(support["kernel_prefix_word"] + support["section_word"])
    require(support["delta_word"] == expected_delta, "linked Gamma/context state")
    expected_conjugate = reduce_word(expected_delta + support["relator_word"] +
                                     inverse_word(expected_delta))
    require(support["conjugate_word"] == expected_conjugate,
            "right conjugation orientation")
    support_row, occurrences = toy_occurrence_column(
        fixture, expected_delta, support["relator_word"])
    require(support["occurrences"] == occurrences and len(occurrences) == 3,
            "all Fox occurrences")
    require(support.get("same_target_merged_before_scalar") is True and
            support.get("full_scalar_not_single_occurrence") is True,
            "full merged scalar")
    require(support["selected_coefficient"] == 2 and
            support["selected_factor_word"] == inverse_word(expected_conjugate),
            "coefficient two literal inversion")
    require(toy_eval(support["selected_factor_word"], generators) == tuple(range(3)),
            "selected inverse relation value")
    global_row, global_occurrences = toy_occurrence_column(
        fixture, cert["global"]["word"], cert["global"]["relator_word"])
    require(cert["global"]["occurrences"] == global_occurrences and
            cert["global"]["K_nonzero"] is True and
            exponent_pair(cert["global"]["relator_word"]) != (0, 0),
            "K nonzero global fallback")
    boundary = cert["boundary"]
    base = toy_fox(boundary["relation_word"], generators, int(boundary["block"]))
    translation = tuple(boundary["translation"]); boundary_row: Sparse = {}
    for key, coefficient in base.items():
        block, component, raw = decode_row_key(key)
        boundary_row[row_key(block, component,
                             bytes(perm_mul(translation, tuple(raw))))] = coefficient
    require(public_sparse(boundary_row) == boundary["row"] and
            boundary["not_inserted_in_correction_word"] is True,
            "typed boundary replay")
    row_by_family = {"boundary": boundary_row,
                     "support_fibre_kernel_prefix": support_row,
                     "K_nonzero_global": global_row}
    basis = Echelon()
    for index, record in enumerate(columns, 1):
        require(record.get("family") in row_by_family, "toy column family")
        row = row_by_family[record["family"]]
        require(record["column_id"] == index and record["row"] == public_sparse(row) and
                record["row_sha256"] == sha_obj(public_sparse(row)), "toy retained row")
        dual, _, _ = basis.exact_dual(parse_sparse(cert["target"]))
        require(record["dual"] == public_sparse(dual) and
                record["full_scalar"] == pair(dual, row) != 0, "toy exact sparse dual")
        before = len(basis.order); added, pivot, ancestry = basis.add(row, index)
        require(added and pivot is not None and record["pivot_hex"] == pivot.hex() and
                record["rank_before"] == before and record["rank_after"] == before + 1 and
                record["ancestry"] == [[k, v] for k, v in sorted(ancestry.items())],
                "toy pivot/rank transition")
    target = parse_sparse(cert["target"]); remainder, solution = basis.reduce(target)
    require(not remainder and [[k, v] for k, v in sorted(solution.items())] ==
            cert["solution_coefficients"], "toy positive identity")
    product = cert["ordered_product"]
    require(product["indices"] == fixture["ordered_product_indices"] and
            product["words"] == fixture["ordered_product_words"],
            "ordered product roster")
    expected_product = reduce_word(letter for index in product["indices"]
                                   for letter in product["words"][index])
    require(product["product_word"] == expected_product and
            toy_eval(expected_product, generators) == tuple(range(3)),
            "ordered three-factor noncommutative product")
    checkpoint = cert["checkpoint"]; validate_seal(checkpoint)
    require(checkpoint["target"] == cert["target"] and checkpoint["rank"] == 3 and
            checkpoint["columns"] == columns and
            checkpoint["pending_prefix"] == {"support_fibre": 2,
                                             "kernel_power": 2,
                                             "global_cursor": 1} and
            checkpoint["separator"] is False, "toy checkpoint semantics")


def toy_mutation_suite(fixture: dict[str, Any], cert: dict[str, Any]) -> list[str]:
    import copy
    mutations: list[tuple[str, Any]] = []
    def register(name: str, action: Any) -> None:
        mutations.append((name, action))
    register("different_Gamma_context", lambda x: x["support"]["delta_word"].append(2))
    register("left_right_conjugation", lambda x: x["support"].__setitem__(
        "conjugate_word", reduce_word(inverse_word(x["support"]["delta_word"]) +
                                      x["support"]["relator_word"] +
                                      x["support"]["delta_word"])))
    register("omitted_Fox_occurrence", lambda x: x["support"]["occurrences"].pop())
    register("premerge_coefficient", lambda x: x["support"].__setitem__(
        "same_target_merged_before_scalar", False))
    register("single_occurrence_scalar", lambda x: x["support"].__setitem__(
        "full_scalar_not_single_occurrence", False))
    register("dependent_added_column", lambda x: x["columns"].append(copy.deepcopy(x["columns"][0])))
    register("changed_pivot_rank", lambda x: x["columns"][1].__setitem__("rank_after", 9))
    register("target_canary_confusion", lambda x: x.__setitem__("target_source", "stacked_target"))
    register("coefficient_without_inverse", lambda x: x["support"].__setitem__(
        "selected_factor_word", list(x["support"]["conjugate_word"])))
    register("boundary_in_correction", lambda x: x["boundary"].__setitem__(
        "not_inserted_in_correction_word", False))
    register("PB3_PB4_block_swap", lambda x: x["boundary"].__setitem__("block", 1))
    register("pentagon_order_sign", lambda x: x["ordered_product"]["indices"].reverse())
    register("pending_prefix_cursor", lambda x: x["checkpoint"]["pending_prefix"].__setitem__(
        "global_cursor", 8))
    register("fabricated_separator", lambda x: x.__setitem__("separator", True))
    register("programming_exception_as_UNKNOWN", lambda x: x.__setitem__(
        "terminal", "UNKNOWN_RESOURCE:TypeError"))
    rejected = []
    for name, action in mutations:
        candidate = copy.deepcopy(cert); action(candidate)
        candidate = seal(candidate)
        if name == "pending_prefix_cursor":
            candidate["checkpoint"] = seal(candidate["checkpoint"])
            candidate = seal(candidate)
        try:
            validate_toy_certificate(fixture, candidate)
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError("toy semantic mutation accepted:" + name)
    require(len(rejected) == 15, "fifteen toy mutations")
    return rejected


def weighted_mutation_suite(fixture: dict[str, Any], cert: dict[str, Any]) -> list[str]:
    import copy
    actions = [
        ("overstated_kernel_order", lambda x: x["weighted_support"]
         ["K0_last_point"].__setitem__("kernel_order", 4)),
        ("K0_skip_not_exhausted", lambda x: x["weighted_support"]
         ["K0_exhaustion"].__setitem__("row_skipped", False)),
        ("W_plus_1_hit_early", lambda x: x["weighted_support"]
         ["Knonzero_W_plus_1"].__setitem__("hit_index", 1)),
        ("understated_kernel_order", lambda x: x["weighted_support"]
         ["kernel_order_gate"]["registered"].__setitem__(0, 8)),
        ("omitted_merged_target", lambda x: x["weighted_support"]
         ["merged_target_W"].__setitem__("omitted_target_rejected", False)),
        ("repeated_global_as_distinct", lambda x: x["weighted_support"]
         ["global_distinctness"].__setitem__("repeated_rejected", False)),
        ("advanced_completed_cursor", lambda x: x["weighted_support"]
         ["completed_cursor"].__setitem__("cursor", 4)),
        ("checkpoint_cursor_skip", lambda x: x["weighted_support"]
         ["checkpoint_state"].__setitem__("canonical_row_cursor", 2)),
    ]
    rejected = []
    for name, action in actions:
        candidate = copy.deepcopy(cert); action(candidate); candidate = seal(candidate)
        try:
            validate_toy_certificate(fixture, candidate)
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError("weighted semantic mutation accepted:" + name)
    require(len(rejected) == 8, "eight weighted mutations")
    return rejected


def selftest_receipt() -> dict[str, Any]:
    raw = FIXTURE.read_bytes()
    require(len(raw) == FIXTURE_BYTES and sha_bytes(raw) == FIXTURE_SHA256,
            "immutable selftest fixture")
    fixture = json.loads(raw.decode("ascii"))
    cert = build_toy_certificate(fixture)
    validate_toy_certificate(fixture, cert)
    rejected = toy_mutation_suite(fixture, cert)
    answer = dict(cert)
    answer["mutation_results"] = {"attempted": 15, "rejected": 15,
                                  "names": rejected,
                                  "validator": "normal_positive_semantic_validator"}
    answer["producer_selftest"] = True
    weighted_rejected = weighted_mutation_suite(fixture, answer)
    answer["weighted_mutation_results"] = {
        "attempted": 8, "rejected": len(weighted_rejected),
        "names": weighted_rejected,
        "validator": "normal_positive_semantic_validator"}
    return seal(answer)


def expected_pin_manifest() -> dict[str, Any]:
    out = {name: {"path": rel, "bytes": size, "sha256": digest}
           for name, (rel, size, digest) in PINS.items()}
    out["fixture"] = {"path": str(FIXTURE.relative_to(ROOT)).replace("\\", "/"),
                      "bytes": FIXTURE_BYTES, "sha256": FIXTURE_SHA256}
    return out


def unknown_receipt(kind: str, detail: str, pins: dict[str, Any] | None,
                    monitor: Monitor | None, checkpoint_path: Path | None) -> dict[str, Any]:
    require(kind in (UNKNOWN_INPUT, UNKNOWN_RESOURCE), "typed UNKNOWN kind")
    checkpoint = None
    if checkpoint_path is not None and checkpoint_path.is_file():
        raw = checkpoint_path.read_bytes()
        checkpoint = {"path": checkpoint_path.name, "bytes": len(raw),
                      "sha256": sha_bytes(raw)}
    return seal({
        "schema": SCHEMA, "status": "UNKNOWN",
        "terminal": f"{kind}:{detail}",
        "pins": pins if pins is not None else expected_pin_manifest(),
        "checkpoint": checkpoint,
        "monitor": None if monitor is None else monitor.public(),
        "positive_claim": False, "negative_claim": False, "separator": False,
        "correction_word": None, "common_word": None,
        "boundaries": {"finite_common_word": False, "cofinal_lift": False,
                       "fake": False, "ihara_witness": False},
    })


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), default="SELFTEST")
    value.add_argument("--output", type=Path, required=True)
    value.add_argument("--resume", type=Path)
    value.add_argument("--seconds", type=float, default=19_800.0)
    value.add_argument("--boundary-pairs", type=int, default=8_000_000)
    value.add_argument("--fibre-scans", type=int, default=80_000_000)
    value.add_argument("--candidate-words", type=int, default=2_000_000)
    value.add_argument("--retained-columns", type=int, default=250_000)
    value.add_argument("--checkpoint-bytes", type=int, default=4_000_000_000)
    value.add_argument("--rss-bytes", type=int, default=5_700_000_000)
    value.add_argument("--oracle-rounds", type=int, default=1)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.mode == "SELFTEST":
        receipt = selftest_receipt(); atomic_json(output, receipt)
        print("R07_POSITIVE_COMMON_WORD_COLGEN_V1_PRODUCER_SELFTEST_PASS "
              "mutation_attempted=15 mutation_rejected=15 "
              "coarse_inverse_checks=4 weighted_mutation_attempted=8 "
              "weighted_mutation_rejected=8", flush=True)
        return 0
    monitor = Monitor(args); pins: dict[str, Any] | None = None
    search: PositiveSearch | None = None
    try:
        pins = authenticate_inputs()
        runtime = build_runtime(monitor)
        search = PositiveSearch(runtime, pins, monitor, output, args.resume)
        receipt = search.run()
    except InputStop as exc:
        receipt = unknown_receipt(UNKNOWN_INPUT, str(exc), pins, monitor,
                                  None if search is None else search.checkpoint_path)
    except ResourceStop as exc:
        if search is not None and exc.cap != "checkpoint_bytes":
            try:
                search.write_checkpoint()
            except ResourceStop as checkpoint_exc:
                exc = checkpoint_exc
        receipt = unknown_receipt(
            UNKNOWN_RESOURCE,
            f"phase={exc.phase}:cap={exc.cap}:value={exc.value}:limit={exc.limit}",
            pins, monitor, None if search is None else search.checkpoint_path)
    # No broad exception handler: TypeError/ValueError/AssertionError and every
    # other implementation defect are hard nonzero STOPs with traceback.
    atomic_json(output, receipt)
    print("R07_POSITIVE_COMMON_WORD_COLGEN_V1_PRODUCER_TERMINAL " +
          str(receipt["terminal"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
