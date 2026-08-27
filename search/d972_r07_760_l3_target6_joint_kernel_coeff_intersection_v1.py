#!/usr/bin/env python3
"""Registered joint-kernel coefficient intersection for r07/g760 target6.

The full mode first calls the pinned task-168 producer.  Only after that
same invocation has authenticated completed-j D2 states does this adapter
construct the pinned task-157ee joint-value kernel, abelianize its complete
Reidemeister--Schreier relation roster modulo three, intersect the resulting
word-bearing coefficient domain with each completed task-168 affine family,
and replay one actual relation-word correction.

This is deliberately a projected/value-domain certificate.  It neither uses
the v108 PB4 equality promotion nor reconstructs the v109 full-E4 class.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import math
import sys
import time
from collections import Counter, deque
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path(
    "search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py")
TASK169_PATH = Path(
    "sol/luna_task_169_r07_joint_kernel_coeff_intersection_v1.md")
PROOF107_PATH = Path(
    "sol/proof_r07_joint_kernel_coefficient_intersection_v107.md")
PROOF108_PATH = Path(
    "sol/proof_pb4_eleven_relator_presentation_equality_v108.md")
PROOF109_PATH = Path(
    "sol/proof_r07_full_e4_joint_orbit_selector_v109.md")

TASK168_PATH = Path(
    "sol/luna_task_168_r07_jennings_legal_coefficients_v1.md")
REPLY168_PATH = Path(
    "sol/luna_reply_168_r07_jennings_legal_coefficients_v1.md")
COEFF_PATH = Path(
    "search/d972_r07_760_l3_target6_legal_coefficients_v1.py")
COEFF_CHECKER_PATH = Path(
    "crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py")
COEFF_DRIVER_PATH = Path(
    "search/d972_r07_760_l3_target6_legal_coefficients_gha_driver_v1.g")
COEFF_PREFLIGHT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_legal_coefficients_"
    "preflight_v1_20260827.json")

TASK157EE_PATH = Path(
    "sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md")
REPLY157EE_PATH = Path(
    "sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md")
TASK157EF_PATH = Path(
    "sol/luna_task_157ef_b345_joint_kernel_checker_repair.md")
REPLY157EF_PATH = Path(
    "sol/luna_reply_157ef_b345_joint_kernel_checker_repair.md")
JOINT_PATH = Path("search/d972_b345_joint_kernel_qstar_closure_v1.py")
JOINT_CHECKER_V2_PATH = Path(
    "search/check_d972_b345_joint_kernel_qstar_closure_v2.py")
JOINT_DRIVER_V2_PATH = Path(
    "search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g")
JOINT_RECEIPT_PATH = Path(
    "ci/b345_157ee_artifacts_32359956713/"
    "d972_b345_joint_kernel_qstar_closure_v1.json")
Q3_PATH = Path(
    "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json")

SCHEMA = "d972-r07-760-l3-target6-joint-kernel-coeff-intersection/v1"
DOMAIN_SCHEMA = "d972-r07-registered-joint-value-exp3-domain/v1"
CERTIFICATE_SCHEMA = (
    "d972-r07-760-l3-target6-joint-coefficient-certificate/v1")
PREFLIGHT_STATE = (
    "R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY")
FINAL_MARKER = "R07_760_JOINT_COEFF_INTERSECTION_V1_PRODUCER_PASS"
DEFAULT_PREFLIGHT = Path(
    "search/certs/d972_r07_760_l3_target6_joint_kernel_coeff_"
    "intersection_preflight_v1_20260827.json")
DEFAULT_FULL = Path(
    "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.json")
DEFAULT_COEFFICIENT_DIR = Path("ci/out")
DEFAULT_CHECKPOINT_DIR = Path(
    "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoints")
DEFAULT_MAX_NEW_RELATORS = 11
RECOMMENDED_SECONDS = 18000.0
N_SCHREIER = 28
N_DELTA = 27
RELATION_COUNTS = {"gamma_cayley_edge": 6318,
                   "xy_action": 104, "q0_factor": 19}
TOTAL_RELATIONS = sum(RELATION_COUNTS.values())
TOTAL_RS_ROWS = TOTAL_RELATIONS * N_DELTA
MAX_LOCAL_RS_LETTERS = 450_000_000
MAX_LOCAL_DOMAIN_SECONDS = 600.0
MAX_GHA_DOMAIN_SECONDS = 5400.0
LEGACY_CANARY_GLOBAL_ORDINALS = tuple(sorted(
    {1, 6318, 6319, 6422, 6423, 6441} |
    set(range(257, TOTAL_RELATIONS + 1, 257))))
LEGACY_CANARY_COUNT = 31
JOINT_RUN_ID = 32359956713
JOINT_RECEIPT_SHA = (
    "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
CONTEXT_ROWS_SHA = (
    "bf07578f91f5ed66e6ddddd4ef83dafa45817a29df066940bbc13bd53cdd00f6")
ALIAS_ROWS_SHA = (
    "15cdac950ede8ce4596e5014ae1b6d0caa28523898cb42f3387f435a11b919a8")
RECORD_WORDS_SHA = (
    "08d11c68dcbacc1b81e5e2732eedcbc41df82a16c8a0f97dfbbb13d6accee24f")
FACTOR_PAYLOAD_SHA = (
    "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba")
COMPLETE_RELATORS_SHA = (
    "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a")
TASK168_SCHREIER_WORDS_SHA = (
    "c7053b4b2c085ff8016ad1da1e0459dc77f0fc777323693b93f1157de0fbde1e")

PIN_SPECS: dict[str, tuple[Path, int, str]] = {
    "task169": (TASK169_PATH, 10445,
        "6223245e9e3ec7476b5b0c55631d7bcea254c7890c5220f2b5866b9f31b22fa7"),
    "proof107": (PROOF107_PATH, 9359,
        "81f83d16abac3a8ffa59b6747b4b36e10796f353916ee4078c8c29c2ad2b07cd"),
    "proof108_read_not_consumed": (PROOF108_PATH, 6742,
        "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
    "proof109_read_not_consumed": (PROOF109_PATH, 11228,
        "3224f0be545ac1ffe1d3c674087b30f55c0eb97fda0bd7702eb5f85b768255f0"),
    "task168": (TASK168_PATH, 7262,
        "4d85fd8f9ec69a618828c06498aa22922cf5372e21d10ed65280ca2468f5b7f1"),
    "reply168": (REPLY168_PATH, 10692,
        "d22bed5ee8331fd5eb1d84256813699d0985df5a5bdf9a31152fdc448f847940"),
    "task168_producer": (COEFF_PATH, 57792,
        "7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962"),
    "task168_checker": (COEFF_CHECKER_PATH, 49633,
        "a54383185601e8251b7cbac87b6c57f89d3a8df8519cb93014b08a3893825e25"),
    "task168_driver": (COEFF_DRIVER_PATH, 19176,
        "bad7911b0958983aacd541bb682b0f14a2903de02cecfc01043b593b17ab1e16"),
    "task168_preflight": (COEFF_PREFLIGHT_PATH, 6833,
        "f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138"),
    "task157ee": (TASK157EE_PATH, 11226,
        "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"),
    "reply157ee": (REPLY157EE_PATH, 4118,
        "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee"),
    "task157ef": (TASK157EF_PATH, 3235,
        "e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed"),
    "reply157ef": (REPLY157EF_PATH, 4541,
        "71ba794479eea934c6ae06d94333f890983e53c909813dd17bab26039bce80e0"),
    "task157ee_producer": (JOINT_PATH, 67945,
        "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "task157ef_checker_v2": (JOINT_CHECKER_V2_PATH, 5942,
        "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
    "task157ef_driver_v2": (JOINT_DRIVER_V2_PATH, 3912,
        "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"),
    "task157ee_full_receipt": (JOINT_RECEIPT_PATH, 2166036,
        JOINT_RECEIPT_SHA),
    "task157ee_q3_input": (Q3_PATH, 231570, Q3_SHA),
}

BOUNDARIES = {
    "registered_joint_value_domain_computed": True,
    "historical_exp3_prefilter_computed": True,
    "full_E4_positive_class_reconstructed": False,
    "true_PB4_D2_equality_used": False,
    "literal_A18_replayed": False,
    "two_hexagons_replayed_as_joint_system": False,
    "HT1_HT5_all_edges_proved": False,
    "cofinal_compatibility_proved": False,
}
STOP_BOUNDARIES = {
    **BOUNDARIES,
    "registered_joint_value_domain_computed": False,
    "historical_exp3_prefilter_computed": False,
}
FALSE_CLAIMS = {
    "actual_A18_lift": False,
    "fake": False,
    "cofinal_lift": False,
    "Ihara_witness": False,
}
TERMINALS = {
    "R07_760_JOINT_COEFF_INTERSECTION_NONEMPTY",
    "R07_760_JOINT_COEFF_INTERSECTION_EMPTY",
    "R07_760_JOINT_COEFF_UNKNOWN_RESOURCE",
    "R07_760_JOINT_COEFF_INPUT_STOP",
}
TARGET_ALIAS_IDS = {
    "correction_coface_0": 1,
    "hexagon_1_fxy_0": 1,
    "hexagon_1_fxz_0": 2,
    "hexagon_1_fyz_0": 3,
}


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, reason: str, observed: int, limit: int) -> None:
        super().__init__(reason)
        self.reason, self.observed, self.limit = reason, observed, limit


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_domain_seconds(value: float) -> float:
    require(type(value) is float and math.isfinite(value) and
            0.0 < value <= MAX_GHA_DOMAIN_SECONDS,
            "domain-seconds finite positive and at most 5400")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_self_digest(data: dict[str, Any], label: str) -> None:
    require(type(data) is dict and
            type(data.get("self_digest_sha256")) is str,
            label + " self digest field")
    work = copy.deepcopy(data)
    claimed = work.pop("self_digest_sha256")
    require(claimed == digest_obj(work), label + " self digest")


def authenticate_inputs() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for label, (path, size, digest) in PIN_SPECS.items():
        full = ROOT / path
        if not full.is_file() or full.stat().st_size != size or \
                digest_file(full) != digest:
            raise InputStop("task169 pin drift: " + path.as_posix())
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def source_record() -> dict[str, Any]:
    full = ROOT / SELF_PATH
    require(full.is_file(), "task169 producer source missing")
    return {"path": SELF_PATH.as_posix(), "bytes": full.stat().st_size,
            "sha256": digest_file(full)}


def load_module(name: str, path: Path, digest: str) -> Any:
    require(name not in sys.modules, "fresh authenticated module name")
    require(digest_file(ROOT / path) == digest, "module pin " + path.as_posix())
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None, "module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    require(digest_file(ROOT / path) == digest, "post-import module pin")
    return module


_CONTEXT_CACHE: dict[str, Any] | None = None


def authenticated_context() -> dict[str, Any]:
    global _CONTEXT_CACHE
    if _CONTEXT_CACHE is not None:
        return _CONTEXT_CACHE
    pins = authenticate_inputs()
    coeff = load_module(
        "_d972_task169_frozen_task168", COEFF_PATH,
        PIN_SPECS["task168_producer"][2])
    v5 = coeff.load_v5()
    v3, v2, v1, summary, private, prior, _, meta = v5.build_context()
    require(summary["legal_overapproximation"]["row_count"] == N_SCHREIER,
            "task168 frozen Schreier count")

    joint = load_module(
        "_d972_task169_frozen_157ee", JOINT_PATH,
        PIN_SPECS["task157ee_producer"][2])
    predecessor = joint.load_prev()
    q3 = json.loads((ROOT / Q3_PATH).read_text(encoding="utf-8"))
    require(digest_file(ROOT / Q3_PATH) == Q3_SHA and
            q3.get("schema") == "d972-b345-q-chief/v1", "q3 input")
    old = predecessor.load_pinned_module(
        predecessor.OLD_PRODUCER, predecessor.OLD_PRODUCER_SHA,
        "_d972_task169_frozen_157ec_old")
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    receipt = json.loads((ROOT / JOINT_RECEIPT_PATH).read_text(
        encoding="utf-8"))
    require(receipt["schema"] == joint.SCHEMA and
            receipt["terminal_token"] ==
                "B345_JOINT_KERNEL_QSTAR_CLOSED" and
            receipt["context_registry"] == context_public and
            context_public["context_rows_sha256"] == CONTEXT_ROWS_SHA and
            context_public["named_use_mapping_sha256"] == ALIAS_ROWS_SHA and
            len(contexts) == 31 and len(aliases) == 46,
            "157ee context registry replay")
    words = [list(row["word"])
             for row in q3["correction_fibre"]["records"] if row["word"]]
    require(len(words) == 26 and digest_obj(words) == RECORD_WORDS_SHA and
            receipt["record_manifest"]["words_sha256"] == RECORD_WORDS_SHA,
            "157ee record words")
    group = joint.JointGroup(old, e3, e4, contexts, words)
    gamma = group.invariants()
    for key in ("order", "edge_count", "generator_count", "exponent",
                "center_order", "derived_order", "cube_subgroup_order",
                "frattini_order", "frattini_quotient_order",
                "state_rows_sha256", "transition_rows_sha256"):
        require(gamma[key] == receipt["gamma"][key],
                "157ee Gamma invariant " + key)
    q0_public, q0_relators = joint.factor_presentation(q3, old)
    require(q0_public == receipt["q0_presentation"] and
            q0_public["factor_payload_sha256"] == FACTOR_PAYLOAD_SHA and
            q0_public["complete_relators_sha256"] == COMPLETE_RELATORS_SHA,
            "157ee factor presentation replay")
    _CONTEXT_CACHE = {
        "pins": pins, "coeff": coeff, "v5": v5, "v3": v3, "v2": v2,
        "v1": v1, "summary": summary, "private": private,
        "prior": prior, "v5_meta": meta,
        "joint": joint, "predecessor": predecessor, "old": old,
        "q3": q3, "e3": e3, "e4": e4, "contexts": contexts,
        "aliases": aliases, "context_public": context_public,
        "joint_receipt": receipt, "record_words": words,
        "group": group, "gamma": gamma, "q0_public": q0_public,
        "q0_relators": q0_relators,
    }
    return _CONTEXT_CACHE


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter in (-2, -1, 1, 2), "F2 letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def append_reduced(out: list[int], word: Iterable[int]) -> None:
    for raw in word:
        letter = int(raw)
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum(1 if x == i else -1 if x == -i else 0 for x in word)
            for i in (1, 2)]


def element_blob(value: Any) -> bytes:
    return bytes(value[0]) + bytes(value[1])


class DeltaSchreier:
    """Frozen positive-BFS Delta3 transversal and exact Schreier rewrite."""
    def __init__(self, v1: Any, e4: Any,
                 expected_words: Sequence[Sequence[int]]) -> None:
        self.v1, self.e4, self.pc = v1, e4, e4.pc
        xbar, ybar, zbar = (e4.eval(list(word))[1]
                             for word in (v1.X0, v1.Y0, v1.Z0))
        require(zbar == self.pc.inverse(self.pc.mul(ybar, xbar)),
                "Delta z convention")
        self.generators = {
            1: (xbar, xbar, ybar),
            2: (ybar, zbar, zbar),
        }
        self.inverse_generators = {
            k: tuple(self.pc.inverse(x) for x in value)
            for k, value in self.generators.items()}
        identity = (self.pc.one(), self.pc.one(), self.pc.one())
        self.states = [identity]
        self.ids = {identity: 0}
        self.sections: list[list[int]] = [[]]
        self.tree: dict[int, tuple[int, int]] = {}
        for state_id, state in enumerate(self.states):
            for letter in (1, 2):
                following = self.mul(state, self.generators[letter])
                if following not in self.ids:
                    require(len(self.states) < N_DELTA,
                            "Delta enumeration cap")
                    target = len(self.states)
                    self.ids[following] = target
                    self.states.append(following)
                    self.sections.append(self.sections[state_id] + [letter])
                    self.tree[target] = (state_id, letter)
        require(len(self.states) == N_DELTA, "Delta order 27")
        self.positive_transition: dict[tuple[int, int], int] = {}
        self.edge_word: dict[tuple[int, int], list[int]] = {}
        self.basis_words: list[list[int]] = []
        for state_id, state in enumerate(self.states):
            for letter in (1, 2):
                target = self.ids[self.mul(state, self.generators[letter])]
                self.positive_transition[(state_id, letter)] = target
                if self.tree.get(target) == (state_id, letter):
                    edge: list[int] = []
                else:
                    edge = reduce_word(
                        self.sections[state_id] + [letter] +
                        inv_word(self.sections[target]))
                    self.basis_words.append(edge)
                    edge = [len(self.basis_words)]
                self.edge_word[(state_id, letter)] = edge
        require(len(self.basis_words) == N_SCHREIER and
                self.basis_words == [list(x) for x in expected_words],
                "same ordered task168 Schreier words")

    def mul(self, left: Any, right: Any) -> Any:
        return tuple(self.pc.mul(left[i], right[i]) for i in range(3))

    def transition(self, state: int, signed_letter: int) \
            -> tuple[int, list[int]]:
        letter = abs(signed_letter)
        if signed_letter > 0:
            target = self.positive_transition[(state, letter)]
            return target, self.edge_word[(state, letter)]
        target = self.ids[self.mul(
            self.states[state], self.inverse_generators[letter])]
        return target, [-x for x in reversed(
            self.edge_word[(target, letter)])]

    def eval(self, word: Sequence[int], start: int = 0) -> int:
        state = start
        for letter in word:
            state, _ = self.transition(state, int(letter))
        return state

    def rewrite(self, word: Sequence[int], start: int = 0) \
            -> tuple[list[int], int]:
        state = start
        out: list[int] = []
        for letter in word:
            state, edge = self.transition(state, int(letter))
            append_reduced(out, edge)
        return out, state

    def expand(self, schreier_word: Sequence[int]) -> list[int]:
        out: list[int] = []
        for letter in schreier_word:
            word = self.basis_words[abs(letter) - 1]
            append_reduced(out, word if letter > 0 else inv_word(word))
        return out

    def public(self) -> dict[str, Any]:
        state_rows = [[bytes(x).hex() for x in state] for state in self.states]
        return {
            "order_Delta3": len(self.states),
            "generator_images_pc_hex": [
                [bytes(x).hex() for x in self.generators[i]] for i in (1, 2)],
            "positive_BFS_transversal_words": self.sections,
            "positive_BFS_transversal_words_sha256": digest_obj(self.sections),
            "canonical_state_rows_sha256": digest_obj(state_rows),
            "ordered_schreier_words": self.basis_words,
            "ordered_schreier_words_sha256": digest_obj(self.basis_words),
            "schreier_generator_count": len(self.basis_words),
            "rank_formula": "1+27*(2-1)=28",
        }


def target_context_binding(context: dict[str, Any],
                           delta: DeltaSchreier) -> dict[str, Any]:
    v1, private = context["v1"], context["private"]
    old = context["old"]
    task_e4 = private["e4"]
    pairs = ((v1.X0, v1.Y0), (v1.X0, v1.Z0), (v1.Y0, v1.Z0))
    task_blobs = []
    for left, right in pairs:
        task_blobs.append([
            element_blob(task_e4.eval(list(left))).hex(),
            element_blob(task_e4.eval(list(right))).hex(),
        ])
    registry_rows = context["context_public"]["contexts"]
    exact_ids = []
    for pair in task_blobs:
        matches = [row["context_id"] for row in registry_rows
                   if row["left_hex"] == pair[0] and
                   row["right_hex"] == pair[1]]
        require(len(matches) == 1, "target context exact registry row")
        exact_ids.append(matches[0])
    require(exact_ids == [1, 2, 3], "target context ids 1,2,3")
    alias_rows = {row["name"]: row["context_id"]
                  for row in context["context_public"]["named_uses"]}
    require(all(alias_rows.get(name) == cid
                for name, cid in TARGET_ALIAS_IDS.items()),
            "target alias exact rows")
    # The factor map is literal: take these three E4 coordinates and then
    # their Pi4[3] PC components.  Check its marked generator images.
    projected = []
    for generator_word in ([1], [2]):
        projected.append(tuple(
            context["e4"].eval(generator_word,
                               context["contexts"][cid - 1])[1]
            for cid in exact_ids))
    require(projected == [delta.generators[1], delta.generators[2]],
            "Omega to Delta marked generator factorization")
    return {
        "registry_context_ids": exact_ids,
        "registry_rows": [copy.deepcopy(registry_rows[i - 1])
                          for i in exact_ids],
        "named_alias_rows": [
            {"name": name, "context_id": alias_rows[name]}
            for name in TARGET_ALIAS_IDS],
        "task168_literal_context_pair_blobs": task_blobs,
        "exact_pair_and_alias_binding": True,
        "projection_is_E4_coordinate_then_Pi4_3_pc_component": True,
        "marked_generator_images_equal_omega3": True,
    }


def relation_roster(context: dict[str, Any], *, started: float,
                    seconds_cap: float) \
        -> tuple[list[dict[str, Any]], dict[str, Any]]:
    old, joint, group = context["old"], context["joint"], context["group"]
    words = context["record_words"]
    qgens = [tuple(row) for row in
             context["q3"]["coarse_models"]["Q0"]["marked_permutations"]]
    qid = tuple(range(1, 37))
    require(all(joint.p_eval(word, qgens) == qid for word in words),
            "all record words Q0 identity")
    rows: list[dict[str, Any]] = []
    internal_frozen_rows: list[list[int]] = []
    action_frozen_rows: list[list[int]] = []
    q0_frozen_rows: list[list[int]] = []
    omega_evaluation_hash = hashlib.sha256()
    omega_evaluation_count = 0
    omega_canary_hash = hashlib.sha256()
    omega_canary_count = 0
    omega_canary_rows: list[dict[str, Any]] = []
    joint_letters = {
        1: group.eval([1]), 2: group.eval([2]),
    }
    joint_letters[-1] = group.inverse(joint_letters[1])
    joint_letters[-2] = group.inverse(joint_letters[2])
    q_letters = {1: qgens[0], 2: qgens[1]}
    q_letters[-1] = joint.p_inv(qgens[0])
    q_letters[-2] = joint.p_inv(qgens[1])
    joint_transition_cache: dict[
        tuple[tuple[bytes, ...], int], Any] = {}
    q0_transition_cache: dict[
        tuple[tuple[int, ...], int], tuple[int, ...]] = {}
    transition_hits = 0
    transition_misses = 0
    q0_transition_hits = 0
    q0_transition_misses = 0

    def direct_omega_eval(word: Sequence[int]) \
            -> tuple[tuple[int, ...], Any]:
        nonlocal transition_hits, transition_misses
        nonlocal q0_transition_hits, q0_transition_misses
        qvalue = qid
        joint_value = group.identity
        for raw_letter in word:
            letter = int(raw_letter)
            qkey = (qvalue, letter)
            qnext = q0_transition_cache.get(qkey)
            if qnext is None:
                qnext = joint.p_mul(qvalue, q_letters[letter])
                q0_transition_cache[qkey] = qnext
                q0_transition_misses += 1
            else:
                q0_transition_hits += 1
            qvalue = qnext
            joint_key = (group.key(joint_value), letter)
            following = joint_transition_cache.get(joint_key)
            if following is None:
                following = group.mul(joint_value, joint_letters[letter])
                joint_transition_cache[joint_key] = following
                transition_misses += 1
            else:
                transition_hits += 1
            joint_value = following
        return qvalue, joint_value

    def add(layer: str, layer_ordinal: int, word: Sequence[int],
            binding: dict[str, Any], omega_identity: bool) -> None:
        nonlocal omega_evaluation_count, omega_canary_count
        if omega_evaluation_count % 32 == 0 and \
                time.monotonic() - started > seconds_cap:
            raise ResourceStop("relation_roster_wall_seconds_cap",
                               int(time.monotonic() - started),
                               int(seconds_cap))
        reduced = reduce_word(word)
        require(omega_identity, "relation Omega identity")
        q0_value, joint_value = direct_omega_eval(reduced)
        joint_key = group.key(joint_value)
        require(q0_value == qid and joint_key == group.key(group.identity),
                "full reduced relation word direct Omega evaluation")
        global_ordinal = len(rows) + 1
        if global_ordinal in LEGACY_CANARY_GLOBAL_ORDINALS:
            legacy_q0 = joint.p_eval(reduced, qgens)
            legacy_joint_key = group.key(group.eval(reduced))
            require(legacy_q0 == q0_value and legacy_joint_key == joint_key,
                    "cached direct Omega evaluator legacy canary")
            omega_canary_count += 1
            canary_row = {
                "global_ordinal": global_ordinal,
                "layer": layer,
                "layer_ordinal": layer_ordinal,
                "word_sha256": digest_obj(reduced),
                "Q0_value": list(legacy_q0),
                "E3_and_31_E4_value_blobs": [
                    blob.hex() for blob in legacy_joint_key],
            }
            omega_canary_rows.append(canary_row)
            omega_canary_hash.update(canonical_bytes(canary_row) + b"\n")
        omega_evaluation_count += 1
        omega_evaluation_hash.update(canonical_bytes({
            "global_ordinal": global_ordinal,
            "Q0_value": list(q0_value),
            "E3_and_31_E4_value_blobs": [blob.hex() for blob in joint_key],
        }) + b"\n")
        rows.append({
            "global_ordinal": global_ordinal,
            "layer": layer,
            "layer_ordinal": layer_ordinal,
            "word": reduced,
            "word_length": len(reduced),
            "word_sha256": digest_obj(reduced),
            "original_157ee_row_binding": binding,
            "Omega_identity_by_exact_construction": True,
        })

    for state, transitions in enumerate(group.transitions):
        for generator, target in enumerate(transitions):
            relation = (group.section_word(state) + words[generator] +
                        inv_word(group.section_word(target)))
            value = group.mul(group.states[state], group.generators[generator])
            omega_ok = group.key(value) == group.key(group.states[target])
            ordinal = state * len(words) + generator + 1
            internal_frozen_rows.append(
                [state + 1, generator + 1, target + 1, 0, 0, 0, 0])
            add("gamma_cayley_edge", ordinal, relation, {
                "157ee_layer": "internal_relations",
                "157ee_rows_sha256":
                    context["joint_receipt"]["internal_relations"]["rows_sha256"],
                "state_id_one_based": state + 1,
                "record_id_one_based": generator + 1,
                "target_state_id_one_based": target + 1,
            }, omega_ok)

    outer = [group.eval([1]), group.eval([2])]
    action_ordinal = 0
    for record, generator_value in enumerate(group.generators):
        for letter, outer_value in enumerate(outer, 1):
            for orientation in (1, -1):
                action_ordinal += 1
                if orientation == 1:
                    conjugate = group.mul(group.mul(
                        group.inverse(outer_value), generator_value),
                        outer_value)
                    prefix = [-letter] + words[record] + [letter]
                else:
                    conjugate = group.mul(group.mul(
                        outer_value, generator_value),
                        group.inverse(outer_value))
                    prefix = [letter] + words[record] + [-letter]
                target = group.ids[group.key(conjugate)]
                relation = prefix + inv_word(group.section_word(target))
                action_frozen_rows.append([
                    record + 1, letter, orientation, target + 1,
                    len(group.section_factors(target)), 0, 0, 0, 0])
                add("xy_action", action_ordinal, relation, {
                    "157ee_layer": "action_relations",
                    "157ee_rows_sha256":
                        context["joint_receipt"]["action_relations"]["rows_sha256"],
                    "record_id_one_based": record + 1,
                    "outer_letter": letter,
                    "orientation": orientation,
                    "target_state_id_one_based": target + 1,
                }, group.key(conjugate) == group.key(group.states[target]))

    for ordinal, relator in enumerate(context["q0_relators"], 1):
        target = group.ids[group.key(group.eval(relator))]
        relation = list(relator) + inv_word(group.section_word(target))
        q0_frozen_rows.append([
            ordinal, len(relator), target + 1,
            len(group.section_factors(target)), 0, 0, 0, 0])
        add("q0_factor", ordinal, relation, {
            "157ee_layer": "q0_relations",
            "157ee_rows_sha256":
                context["joint_receipt"]["q0_relations"]["rows_sha256"],
            "complete_Q0_relator_ordinal": ordinal,
            "complete_Q0_relator_sha256": digest_obj(list(relator)),
            "Gamma_defect_state_id_one_based": target + 1,
        }, joint.p_eval(relator, qgens) == qid)

    counts = Counter(row["layer"] for row in rows)
    require(dict(counts) == RELATION_COUNTS and len(rows) == TOTAL_RELATIONS,
            "complete relation layer counts")
    require(digest_obj(internal_frozen_rows) ==
                context["joint_receipt"]["internal_relations"]["rows_sha256"]
            and action_frozen_rows ==
                context["joint_receipt"]["action_relations"]["rows"]
            and digest_obj(action_frozen_rows) ==
                context["joint_receipt"]["action_relations"]["rows_sha256"]
            and q0_frozen_rows ==
                context["joint_receipt"]["q0_relations"]["rows"]
            and digest_obj(q0_frozen_rows) ==
                context["joint_receipt"]["q0_relations"]["rows_sha256"],
            "literal 157ee relation-row order and target binding")
    require(omega_evaluation_count == TOTAL_RELATIONS,
            "direct full Omega evaluation for every relation word")
    require(omega_canary_count == LEGACY_CANARY_COUNT and
            [row["global_ordinal"] for row in omega_canary_rows] ==
                list(LEGACY_CANARY_GLOBAL_ORDINALS),
            "complete deterministic legacy canary roster")
    return rows, {
        "layer_counts": dict(counts),
        "relation_count": len(rows),
        "total_signed_letters": sum(row["word_length"] for row in rows),
        "maximum_word_length": max(row["word_length"] for row in rows),
        "all_relation_words_identity_under_Omega": True,
        "direct_full_Omega_relation_evaluation_count":
            omega_evaluation_count,
        "direct_full_Omega_relation_evaluation_digest_sha256":
            omega_evaluation_hash.hexdigest(),
        "exact_transition_evaluator": {
            "semantics": (
                "letter-by-letter multiplication in the exact pinned "
                "Q0 x E3 x E4^31 direct product on every final reduced "
                "F2 relation word"),
            "joint_transition_cache_entries":
                len(joint_transition_cache),
            "q0_transition_cache_entries": len(q0_transition_cache),
            "joint_transition_cache_hits": transition_hits,
            "joint_transition_cache_misses": transition_misses,
            "q0_transition_cache_hits": q0_transition_hits,
            "q0_transition_cache_misses": q0_transition_misses,
            "legacy_group_eval_canary_count": omega_canary_count,
            "legacy_group_eval_canary_global_ordinals":
                list(LEGACY_CANARY_GLOBAL_ORDINALS),
            "legacy_group_eval_canary_rows": omega_canary_rows,
            "legacy_group_eval_canary_rows_sha256":
                digest_obj(omega_canary_rows),
            "legacy_group_eval_canary_digest_sha256":
                omega_canary_hash.hexdigest(),
            "legacy_canary_rule": (
                "first and last local ordinal of each relation layer, "
                "plus every global ordinal divisible by 257"),
            "fail_closed": True,
        },
        "direct_components": "Q0, E3, and all 31 E4 context ids",
        "identity_route": (
            "each final freely reduced F2 relation word was directly "
            "evaluated in Q0, E3, and all 31 E4 contexts; Gamma "
            "state/transition and frozen 157ee row equalities are additional "
            "construction checks"),
    }


def pack_roster(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    raw = bytearray()
    public_rows = []
    decoded = []
    for row in rows:
        offset = len(raw)
        word = row["word"]
        raw.extend((int(x) & 255) for x in word)
        public = {key: copy.deepcopy(value) for key, value in row.items()
                  if key != "word"}
        public["i8_offset_bytes"] = offset
        public_rows.append(public)
        decoded.append(list(word))
    raw_bytes = bytes(raw)
    return {
        "encoding": "concatenated-signed-i8-two-complement/base64",
        "alphabet": {"1": "x", "2": "y", "255": "x^-1",
                     "254": "y^-1"},
        "row_count": len(rows),
        "byte_length": len(raw_bytes),
        "payload_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "payload_base64": base64.b64encode(raw_bytes).decode("ascii"),
        "rows": public_rows,
        "rows_sha256": digest_obj(public_rows),
        "decoded_word_list_sha256": digest_obj(decoded),
        "lossless": True,
    }


def row_reduce(rows: Sequence[Sequence[int]], width: int) -> list[list[int]]:
    matrix = [[int(x) % 3 for x in row] for row in rows if any(row)]
    require(all(len(row) == width for row in matrix), "row-reduce width")
    pivot_row = 0
    for column in range(width):
        found = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        if matrix[pivot_row][column] == 2:
            matrix[pivot_row] = [(2 * x) % 3 for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][column]:
                factor = matrix[r][column]
                matrix[r] = [(a - factor * b) % 3 for a, b in
                             zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    result = [row for row in matrix if any(row)]
    result.sort(key=lambda row: next(i for i, x in enumerate(row) if x))
    return result


class FirstInputEchelon:
    def __init__(self, width: int) -> None:
        self.width = width
        self.pivots: dict[int, list[int]] = {}

    def add(self, row: Sequence[int]) -> bool:
        value = [int(x) % 3 for x in row]
        require(len(value) == self.width, "echelon width")
        for pivot in sorted(self.pivots):
            if value[pivot]:
                factor = value[pivot]
                value = [(a - factor * b) % 3
                         for a, b in zip(value, self.pivots[pivot])]
        if not any(value):
            return False
        pivot = next(i for i, x in enumerate(value) if x)
        if value[pivot] == 2:
            value = [(2 * x) % 3 for x in value]
        self.pivots[pivot] = value
        return True

    def rank(self) -> int:
        return len(self.pivots)


def pack_trits(row: Sequence[int]) -> int:
    value = 0
    for index, coefficient in enumerate(row):
        value |= (int(coefficient) % 3) << (2 * index)
    return value


def unpack_trits(value: int, width: int) -> list[int]:
    return [(value >> (2 * i)) & 3 for i in range(width)]


def schreier_exponent_row(word: Sequence[int]) -> list[int]:
    row = [0] * N_SCHREIER
    for letter in word:
        row[abs(letter) - 1] = (row[abs(letter) - 1] +
                                (1 if letter > 0 else 2)) % 3
    return row


def replay_joint_word(context: dict[str, Any], word: Sequence[int], *,
                      require_exp3: bool = True) \
        -> dict[str, Any]:
    joint, old = context["joint"], context["old"]
    qgens = [tuple(row) for row in
             context["q3"]["coarse_models"]["Q0"]["marked_permutations"]]
    qid = tuple(range(1, 37))
    q0 = joint.p_eval(word, qgens)
    e3_value = context["e3"].eval(old.embed_f2_pb3(word))
    values = [context["e4"].eval(word, pair)
              for pair in context["contexts"]]
    identity = context["e4"].identity
    require(q0 == qid and e3_value == context["e3"].identity and
            values == [identity] * 31, "actual word registered joint replay")
    alias_rows = context["context_public"]["named_uses"]
    alias_values = [values[row["context_id"] - 1] for row in alias_rows]
    require(alias_values == [identity] * 46, "actual word alias replay")
    exp = exponent_sums(word)
    exp_mod3 = [x % 3 for x in exp]
    if require_exp3:
        require(exp_mod3 == [0, 0], "actual word exp3")
    context_blobs = [old._element_blob(value).hex() for value in values]
    return {
        "Q0_identity": True, "E3_identity": True,
        "all_31_context_ids_identity": True,
        "all_46_named_aliases_identity": True,
        "three_target6_context_ids": [1, 2, 3],
        "three_target6_contexts_identity": True,
        "context_value_blobs_sha256": digest_obj(context_blobs),
        "free_exponent_sums": exp,
        "free_exponent_sums_mod3": exp_mod3,
        "historical_exp3_prefilter_pass": exp_mod3 == [0, 0],
    }


def combine_words(words: Sequence[Sequence[int]],
                  coefficients: Sequence[int]) -> list[int]:
    require(len(words) == len(coefficients), "word combination width")
    out: list[int] = []
    for word, coefficient in zip(words, coefficients):
        require(int(coefficient) in (0, 1, 2), "F3 word coefficient")
        for _ in range(int(coefficient)):
            append_reduced(out, word)
    return out


def combine_rows(rows: Sequence[Sequence[int]],
                 coefficients: Sequence[int], width: int) -> list[int]:
    require(len(rows) == len(coefficients), "row combination width")
    out = [0] * width
    for row, coefficient in zip(rows, coefficients):
        for i, value in enumerate(row):
            out[i] = (out[i] + int(coefficient) * int(value)) % 3
    return out


def nullspace(matrix: Sequence[Sequence[int]], nvariables: int) \
        -> list[list[int]]:
    rows = [[int(x) % 3 for x in row] for row in matrix]
    require(all(len(row) == nvariables for row in rows), "nullspace width")
    pivot_row = 0
    pivots: list[int] = []
    for column in range(nvariables):
        found = next((r for r in range(pivot_row, len(rows))
                      if rows[r][column]), None)
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        if rows[pivot_row][column] == 2:
            rows[pivot_row] = [(2 * x) % 3 for x in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][column]:
                f = rows[r][column]
                rows[r] = [(a - f * b) % 3
                           for a, b in zip(rows[r], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    pivot_rows = {p: rows[i] for i, p in enumerate(pivots)}
    free = [i for i in range(nvariables) if i not in set(pivots)]
    answer = []
    for column in free:
        vector = [0] * nvariables
        vector[column] = 1
        for pivot in pivots:
            vector[pivot] = (-pivot_rows[pivot][column]) % 3
        answer.append(vector)
    return row_reduce(answer, nvariables)


def build_joint_domain(context: dict[str, Any], *,
                       seconds_cap: float = MAX_LOCAL_DOMAIN_SECONDS,
                       letter_cap: int = MAX_LOCAL_RS_LETTERS) \
        -> dict[str, Any]:
    seconds_cap = validate_domain_seconds(seconds_cap)
    started = time.monotonic()
    static = context["summary"]
    expected_words, task168_delta = context["v1"].delta_and_schreier(
        context["v1"], context["private"]["e4"])
    require(task168_delta["schreier_words_sha256"] ==
            TASK168_SCHREIER_WORDS_SHA and
            static["legal_overapproximation"]["rows_sha256"] ==
                "2e21a906124d170c117663fd1e2fcd9318e682b44cc96cfc19a52ece717e73e0",
            "task168 Schreier roster public binding")
    delta = DeltaSchreier(context["v1"], context["private"]["e4"],
                          expected_words)
    binding = target_context_binding(context, delta)
    roster, roster_stats = relation_roster(
        context, started=started, seconds_cap=seconds_cap)
    packed_roster = pack_roster(roster)
    echelon = FirstInputEchelon(N_SCHREIER)
    selected: list[dict[str, Any]] = []
    input_hash = hashlib.sha256()
    packed_rows: list[int] = []
    processed_letters = 0
    reconstruction_count = 0
    for relation in roster:
        word = relation["word"]
        require(delta.eval(word) == 0,
                "defining joint relation lies in K3")
        for transversal_id, transversal in enumerate(delta.sections):
            processed_letters += len(word) + 2 * len(transversal)
            if processed_letters > letter_cap:
                raise ResourceStop("RS_signed_letter_cap", processed_letters,
                                   letter_cap)
            if time.monotonic() - started > seconds_cap:
                raise ResourceStop("RS_wall_seconds_cap",
                                   int(time.monotonic() - started),
                                   int(seconds_cap))
            schreier_word, end = delta.rewrite(word, transversal_id)
            require(end == transversal_id, "conjugate returns transversal")
            f2_word = reduce_word(transversal + word + inv_word(transversal))
            reconstructed = delta.expand(schreier_word)
            require(reconstructed == f2_word,
                    "direct Schreier reconstruction of conjugate")
            reconstruction_count += 1
            coefficients = schreier_exponent_row(schreier_word)
            input_record = {
                "input_ordinal": len(packed_rows) + 1,
                "relation_global_ordinal": relation["global_ordinal"],
                "relation_layer": relation["layer"],
                "relation_layer_ordinal": relation["layer_ordinal"],
                "transversal_id_one_based": transversal_id + 1,
                "transversal_word": list(transversal),
                "coefficient_row": coefficients,
                "conjugate_word_sha256": digest_obj(f2_word),
                "schreier_word_sha256": digest_obj(schreier_word),
            }
            input_hash.update(canonical_bytes(input_record) + b"\n")
            packed_rows.append(pack_trits(coefficients))
            if echelon.add(coefficients):
                selected.append({
                    **input_record,
                    "source_relation_word_sha256": relation["word_sha256"],
                    "source_relation_binding": copy.deepcopy(
                        relation["original_157ee_row_binding"]),
                    "signed_F2_word": f2_word,
                    "signed_F2_word_length": len(f2_word),
                    "signed_F2_word_sha256": digest_obj(f2_word),
                    "signed_schreier_word": schreier_word,
                    "signed_schreier_word_length": len(schreier_word),
                    "direct_reconstruction_equal": True,
                })
    require(len(packed_rows) == TOTAL_RS_ROWS and
            reconstruction_count == TOTAL_RS_ROWS,
            "complete RS input roster")
    rank = echelon.rank()
    require(len(selected) == rank, "first independent input basis")
    canonical_basis = row_reduce(
        [row["coefficient_row"] for row in selected], N_SCHREIER)
    # Independent bounded route: decode in reverse input order and eliminate
    # with a separately initialized echelon.  This is the mod-3
    # abelianization of the complete RS presentation of Q.
    reverse = FirstInputEchelon(N_SCHREIER)
    for packed in reversed(packed_rows):
        reverse.add(unpack_trits(packed, N_SCHREIER))
    require(reverse.rank() == rank, "reverse RS abelianization rank")

    for row in selected:
        row["registered_joint_replay"] = replay_joint_word(
            context, row["signed_F2_word"], require_exp3=False)

    exp_rows = [[exponent_sums(word)[axis] % 3
                 for word in delta.basis_words] for axis in (0, 1)]
    joint_rows = [row["coefficient_row"] for row in selected]
    exp_on_joint = [[sum(exp_rows[axis][i] * row[i]
                         for i in range(N_SCHREIER)) % 3
                     for row in joint_rows] for axis in (0, 1)]
    exp_kernel = nullspace(exp_on_joint, rank)
    expected_legal_rank = len(exp_kernel)

    legal_echelon = FirstInputEchelon(N_SCHREIER)
    legal_selected: list[dict[str, Any]] = []
    # Prefer actual selected input rows which already pass the exponent gate.
    for index, row in enumerate(selected):
        if all(exp_on_joint[axis][index] == 0 for axis in (0, 1)) and \
                legal_echelon.add(row["coefficient_row"]):
            provenance = [1 if i == index else 0 for i in range(rank)]
            legal_selected.append({
                "selection_kind": "retained_joint_input_row",
                "joint_basis_coefficients": provenance,
                "coefficient_row": list(row["coefficient_row"]),
                "signed_F2_word": list(row["signed_F2_word"]),
                "signed_F2_word_sha256": row["signed_F2_word_sha256"],
                "source_input_ordinal": row["input_ordinal"],
                "source_relation_binding": copy.deepcopy(
                    row["source_relation_binding"]),
            })
    if legal_echelon.rank() < expected_legal_rank:
        for parameters in exp_kernel:
            coefficient_row = combine_rows(
                joint_rows, parameters, N_SCHREIER)
            if legal_echelon.add(coefficient_row):
                word = combine_words(
                    [row["signed_F2_word"] for row in selected], parameters)
                legal_selected.append({
                    "selection_kind": "materialized_joint_basis_combination",
                    "joint_basis_coefficients": parameters,
                    "coefficient_row": coefficient_row,
                    "signed_F2_word": word,
                    "signed_F2_word_sha256": digest_obj(word),
                    "source_input_ordinal": None,
                    "source_relation_binding": None,
                })
            if legal_echelon.rank() == expected_legal_rank:
                break
    require(legal_echelon.rank() == expected_legal_rank,
            "legal exponent intersection rank")
    for row in legal_selected:
        require(combine_rows(joint_rows,
                             row["joint_basis_coefficients"],
                             N_SCHREIER) == row["coefficient_row"],
                "legal basis provenance")
        require([x % 3 for x in exponent_sums(row["signed_F2_word"])] ==
                [0, 0], "legal basis exponent word")
        row["registered_joint_replay"] = replay_joint_word(
            context, row["signed_F2_word"])
    legal_rows = [row["coefficient_row"] for row in legal_selected]
    legal_canonical = row_reduce(legal_rows, N_SCHREIER)
    domain = {
        "schema": DOMAIN_SCHEMA,
        "grade": "CANDIDATE",
        "scope_name": "registered_joint_value_and_exp3_domain",
        "pinned_157ee_run_id": JOINT_RUN_ID,
        "pinned_157ee_receipt_sha256": JOINT_RECEIPT_SHA,
        "context_registry": {
            "context_count": 31, "named_alias_count": 46,
            "context_rows_sha256": CONTEXT_ROWS_SHA,
            "named_use_mapping_sha256": ALIAS_ROWS_SHA,
            "target6_binding": binding,
        },
        "joint_group_replay": {
            "Gamma_invariants": context["gamma"],
            "Q0_presentation": context["q0_public"],
            "record_count": 26,
            "record_words_sha256": RECORD_WORDS_SHA,
            "factor_payload_sha256": FACTOR_PAYLOAD_SHA,
            "complete_Q0_relators_sha256": COMPLETE_RELATORS_SHA,
        },
        "exact_sequence_typing": {
            "sequence": "1 -> Q -> G_joint -> Delta3 -> 1",
            "K3": "ker(omega3:F2->Delta3)",
            "K_joint": "ker(Omega:F2->G_joint)",
            "Q": "ker(G_joint->Delta3)=K3/K_joint",
            "factor_map_definition": (
                "three exact registered target6 E4 coordinates followed by "
                "their Pi4[3] PC projections"),
            "well_defined_from_literal_coordinate_projection": True,
            "defining_relation_count_checked": TOTAL_RELATIONS,
            "all_defining_relations_respected": True,
            "onto_by_27_state_positive_BFS": True,
            "not_inferred_from_matching_orders": True,
        },
        "Delta3_and_Schreier": delta.public(),
        "relation_roster": {**packed_roster, **roster_stats},
        "RS_abelianization": {
            "input_order": (
                "relation layers gamma_cayley_edge,xy_action,q0_factor; "
                "within each pinned 157ee ordinal; then Delta positive-BFS "
                "transversal 1..27"),
            "input_row_count": len(packed_rows),
            "complete_input_row_digest_sha256": input_hash.hexdigest(),
            "direct_reconstruction_count": reconstruction_count,
            "all_conjugates_identity_under_Omega": True,
            "rank_B_joint": rank,
            "nullity_H1_quotient_dimension": N_SCHREIER - rank,
            "word_bearing_first_independent_input_rows": selected,
            "word_bearing_basis_rows_sha256": digest_obj(selected),
            "canonical_B_joint_basis": canonical_basis,
            "canonical_B_joint_basis_sha256": digest_obj(canonical_basis),
            "kernel_H1_K3_to_H1_Q_equals_rowspace": True,
            "normal_presentation_theorem_dependency": {
                "source":
                    "sol/proof_r07_joint_kernel_coefficient_intersection_v107.md",
                "statement": (
                    "the complete defining K_joint relator normal closure, "
                    "after all 27 RS conjugates, presents Q=K3/K_joint; "
                    "abelianization modulo 3 identifies this rowspace with "
                    "ker(H1(K3;F3)->H1(Q;F3))"),
                "used": True,
            },
            "order_independent_elimination_crosscheck": {
                "status": "COMPLETED",
                "method": (
                    "complete packed RS row roster decoded in reverse input "
                    "order into an independently initialized F3 echelon"),
                "generator_count": N_SCHREIER,
                "relation_count": len(packed_rows),
                "rank": reverse.rank(),
                "H1_Q_dimension": N_SCHREIER - reverse.rank(),
                "agrees": True,
            },
            "second_independent_Q_presentation_route": {
                "status": "UNKNOWN_NO_THEOREM_INDEPENDENT_ROUTE",
                "same_packed_rows_reverse_elimination_is_not_claimed_independent":
                    True,
                "helper_nonshared_checker_rebuilds_the_same_normal_presentation_route":
                    True,
            },
        },
        "historical_exponent_gate": {
            "two_exponent_rows_on_28_schreier_words": exp_rows,
            "two_exponent_rows_sha256": digest_obj(exp_rows),
            "exponent_map_on_B_joint_basis": exp_on_joint,
            "exponent_map_on_B_joint_basis_sha256": digest_obj(exp_on_joint),
            "rank_B_legal_value": len(legal_selected),
            "intersection_strict": len(legal_selected) < rank,
            "word_bearing_basis": legal_selected,
            "word_bearing_basis_sha256": digest_obj(legal_selected),
            "canonical_B_legal_value_basis": legal_canonical,
            "canonical_B_legal_value_basis_sha256": digest_obj(legal_canonical),
            "all_basis_words_replayed_31_contexts_46_aliases_exp3": True,
        },
        "resource_accounting": {
            "registered_wall_seconds_cap": seconds_cap,
            "registered_signed_letter_cap": letter_cap,
            "processed_signed_letters": processed_letters,
            "full_local_j9_run": False,
            "parallel_local_computation": False,
        },
        "registered_joint_value_domain_computed": True,
        "historical_exp3_prefilter_computed": True,
        "full_E4_positive_class_reconstructed": False,
        "true_PB4_D2_equality_used": False,
    }
    domain["self_digest_sha256"] = digest_obj(domain)
    return domain


def equations_from_bitplanes(columns: Sequence[tuple[int, int]],
                             rhs: tuple[int, int], dimension: int) \
        -> list[tuple[list[int], int]]:
    rows: dict[int, list[int]] = {}
    for j, (ones, twos) in enumerate(columns):
        require((ones & twos) == 0 and
                (ones | twos).bit_length() <= dimension,
                "affine bitplane column")
        for value, coefficient in ((ones, 1), (twos, 2)):
            plane = value
            while plane:
                bit = plane & -plane
                coordinate = bit.bit_length() - 1
                rows.setdefault(coordinate, [0] * len(columns))[j] = coefficient
                plane ^= bit
    rhs_rows: dict[int, int] = {}
    for value, coefficient in ((rhs[0], 1), (rhs[1], 2)):
        plane = value
        while plane:
            bit = plane & -plane
            rhs_rows[bit.bit_length() - 1] = coefficient
            plane ^= bit
    return [(rows.get(i, [0] * len(columns)), rhs_rows.get(i, 0))
            for i in sorted(set(rows) | set(rhs_rows))]


def rref_affine(equations: Sequence[tuple[Sequence[int], int]],
                nvariables: int) -> dict[str, Any]:
    matrix = [[int(x) % 3 for x in row] + [int(rhs) % 3]
              for row, rhs in equations]
    require(all(len(row) == nvariables + 1 for row in matrix),
            "affine matrix width")
    pivots: list[int] = []
    pivot_row = 0
    for column in range(nvariables):
        found = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        if matrix[pivot_row][column] == 2:
            matrix[pivot_row] = [(2 * x) % 3 for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][column]:
                f = matrix[r][column]
                matrix[r] = [(a - f * b) % 3
                             for a, b in zip(matrix[r], matrix[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    inconsistent = any(not any(row[:-1]) and row[-1] for row in matrix)
    nonzero = [row for row in matrix if any(row)]
    nonzero.sort(key=lambda row: next(
        (i for i, x in enumerate(row[:-1]) if x), nvariables))
    particular = None
    if not inconsistent:
        particular = [0] * nvariables
        for row in nonzero:
            pivot = next((i for i, x in enumerate(row[:-1]) if x), None)
            if pivot is not None:
                particular[pivot] = row[-1]
    homogeneous = [row[:-1] for row in nonzero
                   if any(row[:-1])]
    kernel = nullspace(homogeneous, nvariables)
    return {"consistent": not inconsistent, "rank": len(pivots),
            "nullity": nvariables - len(pivots),
            "pivot_columns_zero_based": pivots,
            "canonical_particular_free_zero": particular,
            "canonical_kernel_basis": kernel,
            "rref_rows": nonzero}


def bitplane(row: dict[str, Any]) -> tuple[int, int]:
    return (int(row["coefficient_one_plane_hex"], 16),
            int(row["coefficient_two_plane_hex"], 16))


def public_bitplane(value: tuple[int, int], dimension: int) -> dict[str, Any]:
    return {"dimension": dimension,
            "coefficient_one_plane_hex": format(value[0], "x"),
            "coefficient_two_plane_hex": format(value[1], "x")}


def bitplane_add(left: tuple[int, int], right: tuple[int, int],
                 dimension: int) -> tuple[int, int]:
    ones, twos = left
    add_one, add_two = right
    mask = (1 << dimension) - 1
    zero_left = mask & ~(ones | twos)
    zero_right = mask & ~(add_one | add_two)
    return ((ones & zero_right) | (zero_left & add_one) | (twos & add_two),
            (twos & zero_right) | (zero_left & add_two) | (ones & add_one))


def bitplane_scale(value: tuple[int, int], coefficient: int) -> tuple[int, int]:
    require(coefficient in (0, 1, 2), "bitplane scale")
    return (0, 0) if coefficient == 0 else value if coefficient == 1 \
        else (value[1], value[0])


def affine_joint_intersection(task168_certificate: dict[str, Any],
                              domain: dict[str, Any]) -> dict[str, Any]:
    U = [row["coefficient_row"] for row in
         domain["historical_exponent_gate"]["word_bearing_basis"]]
    d = len(U)
    dimension = int(task168_certificate["dimension"])
    legal = [bitplane(row) for row in
             task168_certificate["ordered_reduced_quotient_legal_rows"]]
    target = bitplane(task168_certificate["reduced_quotient_target"])
    z_columns = []
    for basis_row in U:
        value = (0, 0)
        for column, coefficient in zip(legal, basis_row):
            value = bitplane_add(
                value, bitplane_scale(column, coefficient), dimension)
        z_columns.append(value)
    base_equations = equations_from_bitplanes(z_columns, target, dimension)
    solved = rref_affine(base_equations, d)
    public_z_columns = [public_bitplane(value, dimension)
                        for value in z_columns]
    result = {
        "j": task168_certificate["j"],
        "consistent": solved["consistent"],
        "rank": solved["rank"],
        "nullity": solved["nullity"],
        "word_basis_dimension": d,
        "ordered_word_basis_U_rows_in_original_28_coordinates": U,
        "ordered_word_basis_U_rows_sha256": digest_obj(U),
        "ordered_reduced_quotient_LjU_columns": public_z_columns,
        "ordered_reduced_quotient_LjU_columns_sha256":
            digest_obj(public_z_columns),
        "coefficient_system_equation_count": len(base_equations),
        "coefficient_system_rref_rows": solved["rref_rows"],
        "coefficient_system_matrix_rhs_sha256": digest_obj({
            "nvariables": d, "equations": base_equations}),
        "canonical_z_particular_free_zero":
            solved["canonical_particular_free_zero"],
        "canonical_z_kernel_basis": solved["canonical_kernel_basis"],
        "lex_first_coefficient_vector_a": None,
        "canonical_word_basis_coefficients_z_for_lex_a": None,
        "canonical_coefficient_kernel_basis_a": [],
        "lex_first_proof": (
            "greedy 0<1<2 in original a coordinates; every prefix "
            "extension is decided by exact F3 RREF in z coordinates"),
        "A_joint_nonempty_implies_A_j_nonempty": True,
    }
    if not solved["consistent"]:
        return result
    constraints: list[tuple[list[int], int]] = []
    lex_a: list[int] = []
    for coordinate in range(N_SCHREIER):
        coefficients = [U[k][coordinate] for k in range(d)]
        choice = None
        for value in (0, 1, 2):
            trial = rref_affine(
                base_equations + constraints + [(coefficients, value)], d)
            if trial["consistent"]:
                choice = value
                break
        require(choice is not None, "lex a extension")
        constraints.append((coefficients, choice))
        lex_a.append(choice)
    fixed = rref_affine(base_equations + constraints, d)
    require(fixed["consistent"], "canonical z for lex a")
    z = fixed["canonical_particular_free_zero"]
    require(z is not None and combine_rows(U, z, N_SCHREIER) == lex_a,
            "z maps to lex a")
    a_kernel = row_reduce(
        [combine_rows(U, row, N_SCHREIER)
         for row in solved["canonical_kernel_basis"]], N_SCHREIER)
    result.update({
        "lex_first_coefficient_vector_a": lex_a,
        "canonical_word_basis_coefficients_z_for_lex_a": z,
        "canonical_coefficient_kernel_basis_a": a_kernel,
    })
    return result


def evaluate_task168_system(certificate: dict[str, Any],
                            coefficients: Sequence[int]) -> bool:
    dimension = certificate["dimension"]
    columns = [bitplane(row) for row in
               certificate["ordered_reduced_quotient_legal_rows"]]
    target = bitplane(certificate["reduced_quotient_target"])
    value = (0, 0)
    for column, coefficient in zip(columns, coefficients):
        value = bitplane_add(
            value, bitplane_scale(column, int(coefficient)), dimension)
    return value == target


def actual_sigma_replay(context: dict[str, Any], workspace: dict[str, Any],
                        d2_echelon: Any, word: Sequence[int],
                        coefficients: Sequence[int]) -> dict[str, Any]:
    coeff, v1, private = context["coeff"], context["v1"], context["private"]
    e4 = private["e4"]
    pairs = ((v1.X0, v1.Y0), (v1.X0, v1.Z0), (v1.Y0, v1.Z0))
    values = [e4.eval(v1.substitute2(word, left, right))[1]
              for left, right in pairs]
    require(values == [e4.pc.one()] * 3, "actual correction target contexts")
    ga = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.X0, v1.Y0))
    gb = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.X0, v1.Z0))
    gc = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.Y0, v1.Z0))
    sigma = v1.add_vec(private["core"].translate_vec(
        e4, v1.add_vec(gc, v1.neg_vec(gb)),
        coeff.prefix_for_sigma(v1, private)), ga)
    sigma_pc = private["core"].project_to_pi(sigma)
    expected_pc = coeff.pc_linear_combination(
        v1, private["sigma_pc"], coefficients)
    require(sigma_pc == expected_pc, "actual word Sigma linear combination")
    projected = v1.project_vec_to_Ij(sigma_pc, workspace["j"])
    sigma_vector = workspace["sp"].vec({
        workspace["idx"][key]: value for key, value in projected.items()
        if key in workspace["idx"]})
    expected_vector = coeff.linear_combination(
        workspace["sp"], workspace["legal_vectors"], coefficients)
    require(sigma_vector == expected_vector, "actual word Jennings Sigma")
    remainder, pivot = d2_echelon.reduce(
        workspace["sp"].sub(workspace["target_vector"], sigma_vector))
    require(remainder == (0, 0) and pivot == -1,
            "actual word target minus Sigma in D2")
    public = v1.serialize_pc_gradient(sigma_pc)
    return {
        "three_target6_context_values_identity": True,
        "projected_Sigma": public,
        "projected_Sigma_sha256": digest_obj(public),
        "Sigma_equals_28_row_linear_combination": True,
        "Jennings_projection_equals_28_row_linear_combination": True,
        "target_minus_Sigma_reduces_to_zero_mod_authenticated_D2": True,
        "first_unreduced_coordinate": pivot,
    }


def materialize_joint_certificate(context: dict[str, Any],
                                  task168_certificate: dict[str, Any],
                                  intersection: dict[str, Any],
                                  domain: dict[str, Any],
                                  workspace: dict[str, Any] | None = None,
                                  d2_echelon: Any | None = None) \
        -> dict[str, Any]:
    certificate = {
        "schema": CERTIFICATE_SCHEMA,
        "grade": "CANDIDATE",
        "j": task168_certificate["j"],
        "g760_base_sha256": context["summary"]["base"]["sha256"],
        "task168_certificate_self_digest_sha256":
            task168_certificate["self_digest_sha256"],
        "task168_completed_public_row_sha256":
            task168_certificate["completed_public_row_sha256"],
        "task168_completed_j_checkpoint": copy.deepcopy(
            task168_certificate["completed_j_checkpoint"]),
        "task168_terminal_D2_state_commitment_sha256":
            task168_certificate["terminal_D2_state_commitment_sha256"],
        "task168_D2_rank": task168_certificate["D2_rank"],
        "task168_Jennings_basis_sha256":
            task168_certificate["Jennings_basis_sha256"],
        "registered_domain_self_digest_sha256":
            domain["self_digest_sha256"],
        "intersection": copy.deepcopy(intersection),
        "actual_joint_kernel_word": None,
        **copy.deepcopy(BOUNDARIES),
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }
    if intersection["consistent"]:
        basis = domain["historical_exponent_gate"]["word_bearing_basis"]
        z = intersection["canonical_word_basis_coefficients_z_for_lex_a"]
        a = intersection["lex_first_coefficient_vector_a"]
        require(z is not None and a is not None, "materialization vectors")
        word = combine_words([row["signed_F2_word"] for row in basis], z)
        require(combine_rows([row["coefficient_row"] for row in basis], z,
                             N_SCHREIER) == a,
                "actual word coefficient provenance")
        require(evaluate_task168_system(task168_certificate, a),
                "joint coefficient remains in A_j")
        replay = replay_joint_word(context, word)
        sigma_replay = None
        if workspace is not None and d2_echelon is not None:
            sigma_replay = actual_sigma_replay(
                context, workspace, d2_echelon, word, a)
        certificate["actual_joint_kernel_word"] = {
            "name": "registered_joint_value_and_exp3_correction",
            "signed_F2_word": word,
            "signed_F2_word_length": len(word),
            "signed_F2_word_sha256": digest_obj(word),
            "free_exponent_sums": exponent_sums(word),
            "factorization": [
                {"legal_word_basis_ordinal": i + 1,
                 "exponent_representative": int(value),
                 "basis_word_sha256": basis[i]["signed_F2_word_sha256"]}
                for i, value in enumerate(z) if value],
            "factorization_sha256": digest_obj([
                [i + 1, int(value)] for i, value in enumerate(z) if value]),
            "coefficient_vector_a": a,
            "coefficient_provenance_replayed": True,
            "registered_joint_replay": replay,
            "task168_projected_D2_replay": sigma_replay,
            "naive_Schreier_product_used": False,
        }
    certificate["self_digest_sha256"] = digest_obj(certificate)
    return certificate


def joint_certificate_filename(j: int) -> str:
    require(j in (9, 10, 11, 12), "joint certificate j")
    return ("d972_r07_760_l3_target6_joint_kernel_coeff_intersection_"
            f"v1_j{j:02d}.json")


def write_joint_certificate(directory: Path,
                            certificate: dict[str, Any]) -> dict[str, Any]:
    path = directory / joint_certificate_filename(certificate["j"])
    raw = canonical_bytes(certificate) + b"\n"
    atomic_immutable_write(path, raw)
    return {"j": certificate["j"], "path": path.as_posix(),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "self_digest_sha256": certificate["self_digest_sha256"]}


def completed_d2_contexts(context: dict[str, Any],
                          task168_receipt: dict[str, Any],
                          checkpoint_dir: Path) \
        -> dict[int, tuple[dict[str, Any], Any]]:
    v5, v3, v2, v1 = (context[k] for k in ("v5", "v3", "v2", "v1"))
    summary, private, prior, meta = (context[k] for k in
                                     ("summary", "private", "prior", "v5_meta"))
    bindings = v5.fixed_bindings(summary, prior, meta)
    result = {}
    left_cache = v3.LeftMultiplyCache(private["e4"].pc, enabled=True)
    progression = task168_receipt["frozen_v5_receipt"]["result"].get(
        "j_progression", [])
    for row in progression:
        j = row["j"]
        delta_path = v5.delta_path(checkpoint_dir, j, 11)
        header, echelon, records, _ = v5.replay_delta_chain(
            delta_path, checkpoint_dir, v3, v2, v1,
            summary, prior, bindings)
        require(header["cumulative_state_commitment_sha256"] ==
                row["v5_append_only_delta"]
                   ["terminal_state_commitment_sha256"] and
                records[-1]["relator"] == 11,
                "joint adapter D2 state binding")
        workspace = v3.j_workspace(
            v1, private, j, accelerators=True, left_cache=left_cache)
        result[j] = (workspace, echelon)
    return result


def depth_inclusion(previous: dict[str, Any],
                    current: dict[str, Any],
                    previous_task168: dict[str, Any]) -> dict[str, Any]:
    require(previous["j"] < current["j"], "joint depth inclusion pair")
    if not current["consistent"]:
        return {
            "previous_j": previous["j"], "new_j": current["j"],
            "proof_kind": "empty_new_family_is_subset",
            "new_particular_in_previous_joint_family": None,
            "new_kernel_direction_count": 0,
            "all_new_kernel_directions_in_previous_joint_family": True,
            "A_joint_new_subset_A_joint_previous": True,
        }
    require(previous["consistent"],
            "nonempty refined family cannot follow empty predecessor")
    particular = current["lex_first_coefficient_vector_a"]
    require(evaluate_task168_system(previous_task168, particular),
            "new joint particular in previous A_j")
    # The common legal value domain is unchanged.  New homogeneous a-vectors
    # are tested against the previous homogeneous task168 quotient system.
    homogeneous = copy.deepcopy(previous_task168)
    target = homogeneous["reduced_quotient_target"]
    target["coefficient_one_plane_hex"] = "0"
    target["coefficient_two_plane_hex"] = "0"
    for row in current["canonical_coefficient_kernel_basis_a"]:
        require(evaluate_task168_system(homogeneous, row),
                "new joint kernel direction in previous family")
    return {
        "previous_j": previous["j"], "new_j": current["j"],
        "proof_kind": "particular_and_homogeneous_directions",
        "new_particular_in_previous_joint_family": True,
        "new_kernel_direction_count": len(
            current["canonical_coefficient_kernel_basis_a"]),
        "all_new_kernel_directions_in_previous_joint_family": True,
        "A_joint_new_subset_A_joint_previous": True,
    }


def base_receipt(mode: str, pins: dict[str, Any],
                 domain_seconds: float) -> dict[str, Any]:
    domain_seconds = validate_domain_seconds(domain_seconds)
    return {
        "schema": SCHEMA, "mode": mode, "grade": "CANDIDATE",
        "pin_manifest": pins, "pin_manifest_sha256": digest_obj(pins),
        "producer_source": source_record(),
        "task168_same_invocation_required": True,
        "task169_domain_resource_policy": {
            "domain_seconds": domain_seconds,
            "default_local_domain_seconds": MAX_LOCAL_DOMAIN_SECONDS,
            "maximum_GHA_domain_seconds": MAX_GHA_DOMAIN_SECONDS,
            "separate_from_task168_full_search_seconds": True,
            "not_part_of_mathematical_universe": True,
        },
        "proof108_read_but_not_consumed": True,
        "proof109_read_but_not_consumed": True,
        **copy.deepcopy(BOUNDARIES),
        "claim_boundaries": copy.deepcopy(BOUNDARIES),
        "claims": copy.deepcopy(FALSE_CLAIMS),
    }


def build_full(seconds: float, checkpoint_dir: Path,
               resume_checkpoint: Path | None, coefficient_dir: Path,
               *, domain_seconds: float, accelerators: bool,
               max_new_relators: int) \
        -> dict[str, Any]:
    domain_seconds = validate_domain_seconds(domain_seconds)
    try:
        pins = authenticate_inputs()
        context = authenticated_context()
        task168 = context["coeff"].build_full(
            seconds, checkpoint_dir, resume_checkpoint, coefficient_dir,
            accelerators=accelerators,
            max_new_relators=max_new_relators)
        context["coeff"].validate_output(task168)
        domain = build_joint_domain(context, seconds_cap=domain_seconds)
        d2_context = completed_d2_contexts(context, task168, checkpoint_dir)
        task_certificates = task168["result"]["coefficient_certificates"]
        intersections = []
        certificates = []
        certificate_files = []
        inclusions = []
        previous_intersection = None
        previous_task = None
        any_underlying_nonmember = False
        for task_certificate in task_certificates:
            if not task_certificate["affine_family"]["nonempty"]:
                any_underlying_nonmember = True
                continue
            intersection = affine_joint_intersection(task_certificate, domain)
            intersections.append(intersection)
            workspace, echelon = d2_context[task_certificate["j"]]
            certificate = materialize_joint_certificate(
                context, task_certificate, intersection, domain,
                workspace, echelon)
            certificates.append(certificate)
            certificate_files.append(write_joint_certificate(
                coefficient_dir, certificate))
            if previous_intersection is not None:
                require(previous_task is not None, "previous task certificate")
                inclusions.append(depth_inclusion(
                    previous_intersection, intersection, previous_task))
            previous_intersection = intersection
            previous_task = task_certificate
        if any_underlying_nonmember or any(
                not row["consistent"] for row in intersections):
            terminal = "R07_760_JOINT_COEFF_INTERSECTION_EMPTY"
        elif intersections and all(row["consistent"] for row in intersections):
            terminal = "R07_760_JOINT_COEFF_INTERSECTION_NONEMPTY"
        elif task168["terminal_token"] == "R07_760_L3_TARGET6_INPUT_STOP":
            terminal = "R07_760_JOINT_COEFF_INPUT_STOP"
        else:
            terminal = "R07_760_JOINT_COEFF_UNKNOWN_RESOURCE"
        receipt = base_receipt("full", pins, domain_seconds)
        receipt.update({
            "status": terminal, "terminal_token": terminal,
            "frozen_task168_receipt": task168,
            "frozen_task168_receipt_sha256": digest_obj(task168),
            "registered_joint_domain": domain,
            "registered_joint_domain_self_digest_sha256":
                domain["self_digest_sha256"],
            "result": {
                "state": terminal,
                "task168_completed_in_same_invocation": True,
                "task168_state_unchanged": True,
                "completed_task168_j_values": [
                    row["j"] for row in task_certificates],
                "completed_member_depth_count": len(intersections),
                "joint_intersections": intersections,
                "joint_coeff_certificates": certificates,
                "joint_coeff_certificate_count": len(certificates),
                "joint_coeff_certificate_file_manifest": certificate_files,
                "joint_coeff_certificate_file_manifest_count":
                    len(certificate_files),
                "depth_inclusion_receipts": inclusions,
                "default_safe_stop_after_new_relators":
                    DEFAULT_MAX_NEW_RELATORS,
                "max_new_relators": max_new_relators,
                "positive_checks_conditional_on_authenticated_task168_D2": True,
            },
        })
    except InputStop as exc:
        pins = locals().get("pins", {})
        receipt = base_receipt("full", pins, domain_seconds)
        receipt.update(copy.deepcopy(STOP_BOUNDARIES))
        receipt["claim_boundaries"] = copy.deepcopy(STOP_BOUNDARIES)
        terminal = "R07_760_JOINT_COEFF_INPUT_STOP"
        receipt.update({"status": terminal, "terminal_token": terminal,
                        "reason": str(exc),
                        "result": {"state": terminal}})
    except ResourceStop as exc:
        receipt = base_receipt("full", pins, domain_seconds)
        receipt.update(copy.deepcopy(STOP_BOUNDARIES))
        receipt["claim_boundaries"] = copy.deepcopy(STOP_BOUNDARIES)
        terminal = "R07_760_JOINT_COEFF_UNKNOWN_RESOURCE"
        receipt.update({"status": terminal, "terminal_token": terminal,
                        "reason": exc.reason,
                        "resource_stop": {"observed": exc.observed,
                                          "limit": exc.limit},
                        "result": {"state": terminal}})
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def permutation_mul(left: tuple[int, ...], right: tuple[int, ...]) \
        -> tuple[int, ...]:
    return tuple(left[right[i] - 1] for i in range(len(left)))


def permutation_inv(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for i, image in enumerate(value, 1):
        out[image - 1] = i
    return tuple(out)


class ToySchreier:
    def __init__(self, generators: Sequence[tuple[int, ...]]) -> None:
        self.generators = {i + 1: g for i, g in enumerate(generators)}
        identity = tuple(range(1, len(generators[0]) + 1))
        self.states = [identity]
        self.ids = {identity: 0}
        self.sections = [[]]
        tree = {}
        for sid, state in enumerate(self.states):
            for letter in range(1, len(generators) + 1):
                target_value = permutation_mul(state, self.generators[letter])
                if target_value not in self.ids:
                    target = len(self.states)
                    self.ids[target_value] = target
                    self.states.append(target_value)
                    self.sections.append(self.sections[sid] + [letter])
                    tree[target] = (sid, letter)
        self.transition_table = {}
        self.edge = {}
        self.basis = []
        for sid, state in enumerate(self.states):
            for letter in range(1, len(generators) + 1):
                target = self.ids[permutation_mul(state,
                                                   self.generators[letter])]
                self.transition_table[(sid, letter)] = target
                if tree.get(target) == (sid, letter):
                    self.edge[(sid, letter)] = []
                else:
                    self.basis.append(reduce_word(
                        self.sections[sid] + [letter] +
                        inv_word(self.sections[target])))
                    self.edge[(sid, letter)] = [len(self.basis)]

    def step(self, state: int, letter: int) -> tuple[int, list[int]]:
        if letter > 0:
            return (self.transition_table[(state, letter)],
                    self.edge[(state, letter)])
        positive = -letter
        inverse = permutation_inv(self.generators[positive])
        target = self.ids[permutation_mul(self.states[state], inverse)]
        return target, [-x for x in reversed(self.edge[(target, positive)])]

    def rewrite(self, word: Sequence[int], start: int = 0) \
            -> tuple[list[int], int]:
        out = []
        state = start
        for letter in word:
            state, edge = self.step(state, letter)
            append_reduced(out, edge)
        return out, state

    def expand(self, word: Sequence[int]) -> list[int]:
        out = []
        for letter in word:
            basis = self.basis[abs(letter) - 1]
            append_reduced(out, basis if letter > 0 else inv_word(basis))
        return out


def bounded_tests() -> dict[str, Any]:
    # S3 is nonabelian; x=(12), y=(123).
    toy = ToySchreier([(2, 1, 3), (2, 3, 1)])
    require(len(toy.states) == 6 and len(toy.basis) == 7,
            "toy nonabelian Schreier rank")
    relators = [[1, 1], [2, 2, 2], [1, 2, 1, 2]]
    unconjugated = FirstInputEchelon(7)
    full = FirstInputEchelon(7)
    reconstruction = 0
    for relator in relators:
        row, end = toy.rewrite(relator)
        require(end == 0, "toy relator identity")
        unconjugated.add(schreier_exponent_row(row)[:7])
        for tid, section in enumerate(toy.sections):
            rewritten, end = toy.rewrite(relator, tid)
            require(end == tid and toy.expand(rewritten) ==
                    reduce_word(section + relator + inv_word(section)),
                    "toy conjugate reconstruction")
            full.add(schreier_exponent_row(rewritten)[:7])
            reconstruction += 1
    require(full.rank() > unconjugated.rank(),
            "toy conjugation adds abelianized normal closure rows")

    redundant = nullspace([[0, 0]], 2)
    strict = nullspace([[1, 0]], 2)
    require(len(redundant) == 2 and len(strict) == 1,
            "strict/redundant exponent filters")

    # Synthetic affine intersection and lex(a) != lex(z) coordinate order.
    task = {
        "j": 2, "dimension": 2,
        "ordered_reduced_quotient_legal_rows": [
            {"coefficient_one_plane_hex": "1",
             "coefficient_two_plane_hex": "0"},
            {"coefficient_one_plane_hex": "1",
             "coefficient_two_plane_hex": "0"},
        ] + [{"coefficient_one_plane_hex": "0",
              "coefficient_two_plane_hex": "0"} for _ in range(26)],
        "reduced_quotient_target": {
            "coefficient_one_plane_hex": "1",
            "coefficient_two_plane_hex": "0"},
    }
    U = [[0, 1] + [0] * 26, [1, 0] + [0] * 26]
    domain = {"historical_exponent_gate": {"word_bearing_basis": [
        {"coefficient_row": row} for row in U]}}
    nonempty = affine_joint_intersection(task, domain)
    require(nonempty["consistent"] and
            nonempty["lex_first_coefficient_vector_a"] ==
                [0, 1] + [0] * 26 and
            nonempty["canonical_word_basis_coefficients_z_for_lex_a"] ==
                [1, 0], "lex a distinct coordinate order")
    # The two L_j U columns span only the first coordinate.  Hex "2" in the
    # one-plane is the second coordinate; (0,1) would instead mean twice the
    # first coordinate and would still lie in that span.
    empty_task = copy.deepcopy(task)
    empty_task["reduced_quotient_target"] = {
        "coefficient_one_plane_hex": "2",
        "coefficient_two_plane_hex": "0"}
    empty = affine_joint_intersection(empty_task, domain)
    require(not empty["consistent"], "empty affine intersection")
    previous = copy.deepcopy(nonempty)
    previous["j"] = 2
    empty_child = copy.deepcopy(empty)
    empty_child["j"] = 3
    empty_inclusion = depth_inclusion(previous, empty_child, task)
    require(empty_inclusion["A_joint_new_subset_A_joint_previous"] and
            empty_inclusion["proof_kind"] ==
                "empty_new_family_is_subset",
            "empty refined family inclusion")
    impossible_child = copy.deepcopy(nonempty)
    impossible_child["j"] = 4
    rejected_empty_to_nonempty = False
    try:
        depth_inclusion(empty_child, impossible_child, task)
    except RuntimeError:
        rejected_empty_to_nonempty = True
    require(rejected_empty_to_nonempty,
            "reject nonempty refined family after empty predecessor")

    # A Schreier generator s with odd auxiliary C2 image has s^4 in the
    # refined kernel with the same mod-3 coefficient as s, while naive s is
    # outside.  This is the required word-lift versus naive-product canary.
    odd_index = next(i for i, word in enumerate(toy.basis)
                     if sum(exponent_sums(word)) % 2)
    s = toy.basis[odd_index]
    actual = reduce_word(s + s + s + s)
    require(sum(exponent_sums(s)) % 2 == 1 and
            sum(exponent_sums(actual)) % 2 == 0 and
            4 % 3 == 1,
            "relation word versus naive Schreier product")
    return {
        "small_nonabelian_exact_sequence": {
            "group": "S3", "order": len(toy.states),
            "Schreier_rank": len(toy.basis),
            "conjugate_reconstruction_count": reconstruction,
        },
        "normal_closure_conjugation_needed": True,
        "unconjugated_rank": unconjugated.rank(),
        "all_conjugates_rank": full.rank(),
        "strict_exponent_filter_rank": len(strict),
        "redundant_exponent_filter_rank": len(redundant),
        "nonempty_affine_intersection": True,
        "empty_affine_intersection": True,
        "empty_child_subset_regression": True,
        "empty_to_nonempty_monotonicity_violation_rejected": True,
        "lex_first_a_not_lex_first_z_canary": True,
        "naive_word_outside_refined_kernel_actual_relation_word_inside": True,
    }


def synthetic_task168_commitment_regression(
        context: dict[str, Any], inherited: dict[str, Any] | None = None) \
        -> dict[str, Any]:
    if inherited is None:
        inherited = context["coeff"].build_preflight()
    context["coeff"].validate_output(inherited)
    return {
        "task168_preflight_self_digest_sha256":
            inherited["self_digest_sha256"],
        "task168_preflight_sha256": digest_obj(inherited),
        "bounded_completed_j_certificate_regression": copy.deepcopy(
            inherited["bounded_completed_j_certificate_regression"]),
        "inherited_completed_j_exact_next":
            inherited["inherited_completed_j_regression"]["exact_next_j"],
        "inherited_safe_stop_ancestors_counted_as_new":
            inherited["inherited_safe_stop_regression"]
                     ["ancestors_counted_as_new"],
        "full_j9_run": False,
    }


def structural_mutation_tests(context: dict[str, Any],
                              domain: dict[str, Any]) -> dict[str, Any]:
    """Exhaust every indexed structural binding without copying receipt N times."""
    counts: dict[str, int] = {}
    context_rows = context["context_public"]["contexts"]
    rejected = 0
    for index in range(len(context_rows)):
        rows = copy.deepcopy(context_rows)
        rows[index]["context_id"] = 32
        require(digest_obj(rows) != CONTEXT_ROWS_SHA,
                "context-row mutation rejection")
        rejected += 1
    counts["all_31_context_ids"] = rejected

    alias_rows = context["context_public"]["named_uses"]
    alias_rejected = 0
    for index in range(len(alias_rows)):
        rows = copy.deepcopy(alias_rows)
        rows[index]["context_id"] = 1 + (rows[index]["context_id"] % 31)
        require(digest_obj(rows) != ALIAS_ROWS_SHA,
                "alias-row mutation rejection")
        alias_rejected += 1
    counts["all_46_named_aliases"] = alias_rejected

    roster = domain["relation_roster"]
    layer_rejected = 0
    for layer in RELATION_COUNTS:
        rows = copy.deepcopy(roster["rows"])
        index = next(i for i, row in enumerate(rows) if row["layer"] == layer)
        rows[index]["layer_ordinal"] += 1
        require(digest_obj(rows) != roster["rows_sha256"],
                "relation-layer mutation rejection")
        layer_rejected += 1
    counts["all_3_relation_layers"] = layer_rejected

    delta = domain["Delta3_and_Schreier"]
    transversal_rejected = 0
    for index in range(N_DELTA):
        rows = copy.deepcopy(delta["positive_BFS_transversal_words"])
        rows[index] = rows[index] + [1]
        require(digest_obj(rows) !=
                delta["positive_BFS_transversal_words_sha256"],
                "transversal mutation rejection")
        transversal_rejected += 1
    counts["all_27_transversals"] = transversal_rejected

    schreier_rejected = 0
    for index in range(N_SCHREIER):
        rows = copy.deepcopy(delta["ordered_schreier_words"])
        require(rows[index], "nonempty Schreier basis word")
        rows[index][0] = -rows[index][0]
        require(digest_obj(rows) != delta["ordered_schreier_words_sha256"],
                "Schreier sign/order mutation rejection")
        schreier_rejected += 1
    counts["all_28_schreier_sign_rows"] = schreier_rejected

    gate = domain["historical_exponent_gate"]
    exp_rejected = 0
    for axis in range(2):
        for index in range(N_SCHREIER):
            rows = copy.deepcopy(
                gate["two_exponent_rows_on_28_schreier_words"])
            rows[axis][index] = (rows[axis][index] + 1) % 3
            require(digest_obj(rows) != gate["two_exponent_rows_sha256"],
                    "exponent entry mutation rejection")
            exp_rejected += 1
    counts["all_56_exponent_entries"] = exp_rejected

    basis = domain["RS_abelianization"][
        "word_bearing_first_independent_input_rows"]
    basis_rejected = 0
    provenance_rejected = 0
    for index in range(len(basis)):
        rows = copy.deepcopy(basis)
        rows[index]["coefficient_row"][0] = (
            rows[index]["coefficient_row"][0] + 1) % 3
        require(digest_obj(rows) != domain["RS_abelianization"]
                ["word_bearing_basis_rows_sha256"],
                "basis-row mutation rejection")
        basis_rejected += 1
        rows = copy.deepcopy(basis)
        rows[index]["source_relation_binding"]["157ee_layer"] = "mutated"
        require(digest_obj(rows) != domain["RS_abelianization"]
                ["word_bearing_basis_rows_sha256"],
                "basis-provenance mutation rejection")
        provenance_rejected += 1
    counts["all_B_joint_basis_rows"] = basis_rejected
    counts["all_B_joint_source_provenance_rows"] = provenance_rejected
    counts["task168_aggregate_state_commitment"] = 1
    counts["all_forbidden_claims"] = 10
    require(rejected == 31 and alias_rejected == 46 and
            layer_rejected == 3 and transversal_rejected == 27 and
            schreier_rejected == 28 and exp_rejected == 56 and
            basis_rejected == provenance_rejected == len(basis),
            "structural mutation coverage")
    counts["total"] = sum(value for key, value in counts.items()
                          if key != "total")
    return counts


def validate_domain(domain: dict[str, Any]) -> None:
    verify_self_digest(domain, "joint domain")
    require(domain.get("schema") == DOMAIN_SCHEMA and
            domain.get("scope_name") ==
                "registered_joint_value_and_exp3_domain" and
            domain.get("registered_joint_value_domain_computed") is True and
            domain.get("historical_exp3_prefilter_computed") is True and
            domain.get("full_E4_positive_class_reconstructed") is False and
            domain.get("true_PB4_D2_equality_used") is False,
            "joint domain boundary")
    registry = domain["context_registry"]
    require(registry["context_count"] == 31 and
            registry["named_alias_count"] == 46 and
            registry["context_rows_sha256"] == CONTEXT_ROWS_SHA and
            registry["named_use_mapping_sha256"] == ALIAS_ROWS_SHA and
            registry["target6_binding"]["registry_context_ids"] == [1, 2, 3]
            and {row["name"]: row["context_id"] for row in
                 registry["target6_binding"]["named_alias_rows"]} ==
                TARGET_ALIAS_IDS,
            "joint domain contexts")
    delta = domain["Delta3_and_Schreier"]
    require(delta["order_Delta3"] == N_DELTA and
            len(delta["ordered_schreier_words"]) == N_SCHREIER and
            digest_obj(delta["ordered_schreier_words"]) ==
                delta["ordered_schreier_words_sha256"],
            "joint domain Schreier roster")
    roster = domain["relation_roster"]
    require(roster["row_count"] == TOTAL_RELATIONS and
            roster["relation_count"] == TOTAL_RELATIONS and
            roster["layer_counts"] == RELATION_COUNTS and
            roster["all_relation_words_identity_under_Omega"] is True and
            roster["direct_full_Omega_relation_evaluation_count"] ==
                TOTAL_RELATIONS and
            type(roster[
                "direct_full_Omega_relation_evaluation_digest_sha256"])
                is str and
            len(roster[
                "direct_full_Omega_relation_evaluation_digest_sha256"])
                == 64 and
            digest_obj(roster["rows"]) == roster["rows_sha256"],
            "joint domain relation roster")
    evaluator = roster["exact_transition_evaluator"]
    canary_rows = evaluator["legacy_group_eval_canary_rows"]
    canary_hash = hashlib.sha256()
    for row in canary_rows:
        canary_hash.update(canonical_bytes(row) + b"\n")
    require(evaluator["fail_closed"] is True and
            evaluator["legacy_group_eval_canary_count"] ==
                LEGACY_CANARY_COUNT and
            evaluator["legacy_group_eval_canary_global_ordinals"] ==
                list(LEGACY_CANARY_GLOBAL_ORDINALS) and
            [row["global_ordinal"] for row in canary_rows] ==
                list(LEGACY_CANARY_GLOBAL_ORDINALS) and
            digest_obj(canary_rows) ==
                evaluator["legacy_group_eval_canary_rows_sha256"] and
            canary_hash.hexdigest() ==
                evaluator["legacy_group_eval_canary_digest_sha256"] and
            all(row["word_sha256"] ==
                roster["rows"][row["global_ordinal"] - 1]["word_sha256"]
                and row["layer"] ==
                    roster["rows"][row["global_ordinal"] - 1]["layer"]
                and row["layer_ordinal"] ==
                    roster["rows"][row["global_ordinal"] - 1][
                        "layer_ordinal"]
                and row["Q0_value"] == list(range(1, 37)) and
                len(row["E3_and_31_E4_value_blobs"]) == 32
                for row in canary_rows) and
            evaluator["joint_transition_cache_entries"] ==
                evaluator["joint_transition_cache_misses"] and
            evaluator["q0_transition_cache_entries"] ==
                evaluator["q0_transition_cache_misses"] and
            evaluator["joint_transition_cache_hits"] +
                evaluator["joint_transition_cache_misses"] ==
                roster["total_signed_letters"] and
            evaluator["q0_transition_cache_hits"] +
                evaluator["q0_transition_cache_misses"] ==
                roster["total_signed_letters"],
            "joint domain exact-transition and legacy canary binding")
    raw = base64.b64decode(roster["payload_base64"], validate=True)
    require(len(raw) == roster["byte_length"] and
            hashlib.sha256(raw).hexdigest() == roster["payload_sha256"],
            "joint domain roster payload")
    for row in roster["rows"]:
        start = row["i8_offset_bytes"]
        word = [x if x < 128 else x - 256
                for x in raw[start:start + row["word_length"]]]
        require(digest_obj(word) == row["word_sha256"],
                "joint domain roster word binding")
    rs = domain["RS_abelianization"]
    basis = rs["word_bearing_first_independent_input_rows"]
    require(rs["input_row_count"] == TOTAL_RS_ROWS and
            rs["direct_reconstruction_count"] == TOTAL_RS_ROWS and
            rs["rank_B_joint"] == len(basis) and
            rs["nullity_H1_quotient_dimension"] ==
                N_SCHREIER - len(basis) and
            digest_obj(basis) == rs["word_bearing_basis_rows_sha256"] and
            digest_obj(rs["canonical_B_joint_basis"]) ==
                rs["canonical_B_joint_basis_sha256"] and
            len(row_reduce([row["coefficient_row"] for row in basis],
                           N_SCHREIER)) == len(basis),
            "joint domain B_joint basis")
    gate = domain["historical_exponent_gate"]
    require(digest_obj(gate["two_exponent_rows_on_28_schreier_words"]) ==
                gate["two_exponent_rows_sha256"] and
            digest_obj(gate["exponent_map_on_B_joint_basis"]) ==
                gate["exponent_map_on_B_joint_basis_sha256"] and
            digest_obj(gate["word_bearing_basis"]) ==
                gate["word_bearing_basis_sha256"] and
            digest_obj(gate["canonical_B_legal_value_basis"]) ==
                gate["canonical_B_legal_value_basis_sha256"] and
            gate["rank_B_legal_value"] == len(gate["word_bearing_basis"]),
            "joint domain exponent gate")
    for row in gate["word_bearing_basis"]:
        require(digest_obj(row["signed_F2_word"]) ==
                row["signed_F2_word_sha256"] and
                [x % 3 for x in exponent_sums(row["signed_F2_word"])] ==
                    [0, 0], "joint domain legal source word")


def validate_output(data: dict[str, Any]) -> None:
    verify_self_digest(data, "task169 receipt")
    policy = data.get("task169_domain_resource_policy", {})
    domain_seconds = validate_domain_seconds(policy.get("domain_seconds"))
    require(policy == {
        "domain_seconds": domain_seconds,
        "default_local_domain_seconds": MAX_LOCAL_DOMAIN_SECONDS,
        "maximum_GHA_domain_seconds": MAX_GHA_DOMAIN_SECONDS,
        "separate_from_task168_full_search_seconds": True,
        "not_part_of_mathematical_universe": True,
    }, "task169 domain resource policy")
    expected_boundaries = BOUNDARIES if (
        data.get("mode") == "preflight" or
        "registered_joint_domain" in data) else STOP_BOUNDARIES
    require(data.get("schema") == SCHEMA and data.get("grade") == "CANDIDATE"
            and data.get("claim_boundaries") == expected_boundaries and
            all(data.get(key) is value
                for key, value in expected_boundaries.items())
            and data.get("claims") == FALSE_CLAIMS and
            data.get("proof108_read_but_not_consumed") is True and
            data.get("proof109_read_but_not_consumed") is True,
            "task169 receipt boundary")
    if data.get("mode") == "preflight":
        require(data.get("preflight_state") == PREFLIGHT_STATE and
                data.get("status") == PREFLIGHT_STATE and
                data.get("full_j9_run_locally") is False and
                data.get("GHA_dispatched") is False and
                data.get("parallel_local_computation") is False,
                "task169 preflight envelope")
        require(data.get("mutation_tests_rejected") == 19,
                "task169 preflight mutation count")
        structural = data.get("structural_mutation_tests_rejected", {})
        require(structural.get("all_31_context_ids") == 31 and
                structural.get("all_46_named_aliases") == 46 and
                structural.get("all_3_relation_layers") == 3 and
                structural.get("all_27_transversals") == 27 and
                structural.get("all_28_schreier_sign_rows") == 28 and
                structural.get("all_56_exponent_entries") == 56 and
                structural.get("task168_aggregate_state_commitment") == 1 and
                structural.get("all_forbidden_claims") == 10,
                "task169 indexed structural mutation coverage")
        validate_domain(data["registered_joint_domain"])
        require(data["registered_joint_domain"]["resource_accounting"]
                    ["registered_wall_seconds_cap"] == domain_seconds,
                "preflight domain-seconds propagation")
        regression = data["task168_regression"]
        require(regression["task168_preflight_sha256"] ==
                    digest_obj(data["embedded_task168_preflight"]) and
                regression["inherited_completed_j_exact_next"] == 10 and
                regression["inherited_safe_stop_ancestors_counted_as_new"]
                    is False,
                "task168 regression binding")
        return
    require(data.get("mode") == "full" and
            data.get("terminal_token") in TERMINALS and
            data.get("status") == data["terminal_token"] and
            data.get("result", {}).get("state") == data["terminal_token"],
            "task169 full terminal")
    if "registered_joint_domain" in data:
        validate_domain(data["registered_joint_domain"])
        require(data["registered_joint_domain"]["resource_accounting"]
                    ["registered_wall_seconds_cap"] == domain_seconds,
                "full domain-seconds propagation")
        require(data["frozen_task168_receipt_sha256"] ==
                digest_obj(data["frozen_task168_receipt"]) and
                data["result"]["task168_completed_in_same_invocation"] is True,
                "task169 same invocation binding")
        result = data["result"]
        require(result.get("joint_coeff_certificate_count") ==
                    len(result.get("joint_coeff_certificates", [])) and
                result.get("joint_coeff_certificate_file_manifest_count") ==
                    len(result.get(
                        "joint_coeff_certificate_file_manifest", [])) and
                result.get("joint_coeff_certificate_count") ==
                    result.get("joint_coeff_certificate_file_manifest_count"),
                "joint coefficient file manifest")
    if data["terminal_token"] in {
            "R07_760_JOINT_COEFF_INTERSECTION_NONEMPTY",
            "R07_760_JOINT_COEFF_INTERSECTION_EMPTY"}:
        for certificate in data["result"]["joint_coeff_certificates"]:
            verify_self_digest(certificate, "joint coefficient certificate")
            require(all(certificate[key] is value
                        for key, value in BOUNDARIES.items()) and
                    certificate["claims"] == FALSE_CLAIMS,
                    "joint coefficient certificate boundary")


def resign(data: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(data)
    result.pop("self_digest_sha256", None)
    result["self_digest_sha256"] = digest_obj(result)
    return result


def mutation_tests(preflight: dict[str, Any]) -> int:
    rejected = 0
    total = 0
    def mutate(path: Sequence[Any], value: Any) -> None:
        nonlocal rejected, total
        row = copy.deepcopy(preflight)
        target: Any = row
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        total += 1
        try:
            validate_output(resign(row))
        except RuntimeError:
            rejected += 1
    mutate(["registered_joint_domain", "context_registry",
            "target6_binding", "registry_context_ids", 0], 2)
    mutate(["registered_joint_domain", "context_registry",
            "target6_binding", "named_alias_rows", 0, "context_id"], 2)
    mutate(["registered_joint_domain", "relation_roster", "rows", 0,
            "layer"], "xy_action")
    mutate(["registered_joint_domain", "Delta3_and_Schreier",
            "positive_BFS_transversal_words", 1], [2])
    mutate(["registered_joint_domain", "Delta3_and_Schreier",
            "ordered_schreier_words", 0, 0], -1)
    mutate(["registered_joint_domain", "historical_exponent_gate",
            "two_exponent_rows_on_28_schreier_words", 0, 0], 1)
    mutate(["registered_joint_domain", "RS_abelianization",
            "word_bearing_first_independent_input_rows", 0,
            "coefficient_row", 0], 2)
    mutate(["registered_joint_domain", "RS_abelianization",
            "word_bearing_first_independent_input_rows", 0,
            "source_relation_binding", "157ee_layer"], "q0_relations")
    mutate(["task168_regression", "task168_preflight_sha256"], "0" * 64)
    for key in ("full_E4_positive_class_reconstructed",
                "true_PB4_D2_equality_used", "literal_A18_replayed",
                "two_hexagons_replayed_as_joint_system",
                "HT1_HT5_all_edges_proved", "cofinal_compatibility_proved"):
        mutate([key], True)
    for key in FALSE_CLAIMS:
        mutate(["claims", key], True)
    require(rejected == total == 19, "all task169 mutations rejected")
    return rejected


def build_preflight(domain_seconds: float = MAX_LOCAL_DOMAIN_SECONDS) \
        -> dict[str, Any]:
    domain_seconds = validate_domain_seconds(domain_seconds)
    pins = authenticate_inputs()
    context = authenticated_context()
    domain = build_joint_domain(context, seconds_cap=domain_seconds)
    tests = bounded_tests()
    structural_mutations = structural_mutation_tests(context, domain)
    task168_preflight = context["coeff"].build_preflight()
    task168_regression = synthetic_task168_commitment_regression(
        context, task168_preflight)
    require(digest_obj(task168_preflight) ==
            task168_regression["task168_preflight_sha256"],
            "deterministic task168 preflight regression")
    receipt = base_receipt("preflight", pins, domain_seconds)
    receipt.update({
        "preflight_state": PREFLIGHT_STATE,
        "status": PREFLIGHT_STATE,
        "registered_joint_domain": domain,
        "registered_joint_domain_self_digest_sha256":
            domain["self_digest_sha256"],
        "bounded_tests": tests,
        "structural_mutation_tests_rejected": structural_mutations,
        "task168_regression": task168_regression,
        "embedded_task168_preflight": task168_preflight,
        "full_j9_run_locally": False,
        "GHA_dispatched": False,
        "parallel_local_computation": False,
        "independent_checker_required": True,
        "positive_full_check_conditional_on_authenticated_task168_D2_state":
            True,
        "mutation_tests_rejected": 19,
    })
    receipt["self_digest_sha256"] = digest_obj(receipt)
    require(mutation_tests(receipt) ==
            receipt["mutation_tests_rejected"],
            "preflight mutation count binding")
    return receipt


def atomic_immutable_write(path: Path, raw: bytes) -> None:
    full = path if path.is_absolute() else ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    if full.exists():
        require(full.read_bytes() == raw, "immutable output drift")
        return
    temporary = full.with_name(full.name + ".tmp")
    require(not temporary.exists(), "temporary output collision")
    temporary.write_bytes(raw)
    temporary.replace(full)


def checked_write(path: Path, data: dict[str, Any]) -> bytes:
    validate_output(data)
    raw = canonical_bytes(data) + b"\n"
    atomic_immutable_write(path, raw)
    return raw


def self_test(domain_seconds: float) -> None:
    receipt = build_preflight(domain_seconds)
    validate_output(receipt)
    domain = receipt["registered_joint_domain"]
    print(
        FINAL_MARKER + "_SELFTEST_PASS "
        f"relations={domain['relation_roster']['relation_count']} "
        f"RS_rows={domain['RS_abelianization']['input_row_count']} "
        f"rank_B_joint={domain['RS_abelianization']['rank_B_joint']} "
        f"rank_B_legal={domain['historical_exponent_gate']['rank_B_legal_value']} "
        f"mutations={receipt['mutation_tests_rejected']} "
        f"canaries={domain['relation_roster']['exact_transition_evaluator']['legacy_group_eval_canary_count']} "
        f"domain_seconds={domain_seconds:g} "
        "full_j9_local=false", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--coefficient-dir", type=Path,
                        default=DEFAULT_COEFFICIENT_DIR)
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--seconds", type=float, default=RECOMMENDED_SECONDS)
    parser.add_argument("--domain-seconds", type=float,
                        default=MAX_LOCAL_DOMAIN_SECONDS)
    parser.add_argument("--disable-accelerators", action="store_true")
    parser.add_argument("--max-new-relators", type=int,
                        default=DEFAULT_MAX_NEW_RELATORS)
    args = parser.parse_args()
    domain_seconds = validate_domain_seconds(args.domain_seconds)
    require(sum((args.self_test, args.preflight, args.full)) == 1,
            "select exactly one task169 mode")
    if args.self_test:
        require(args.resume_checkpoint is None and
                not args.disable_accelerators,
                "task169 selftest fixed options")
        self_test(domain_seconds)
        return 0
    if args.preflight:
        require(args.resume_checkpoint is None and
                not args.disable_accelerators,
                "task169 preflight fixed options")
        receipt = build_preflight(domain_seconds)
        output = args.output or DEFAULT_PREFLIGHT
    else:
        receipt = build_full(
            args.seconds, args.checkpoint_dir, args.resume_checkpoint,
            args.coefficient_dir,
            domain_seconds=domain_seconds,
            accelerators=not args.disable_accelerators,
            max_new_relators=args.max_new_relators)
        output = args.output or DEFAULT_FULL
    raw = checked_write(output, receipt)
    state = receipt.get("preflight_state", receipt.get("terminal_token"))
    domain = receipt.get("registered_joint_domain", {})
    rank = domain.get("RS_abelianization", {}).get("rank_B_joint", -1)
    canaries = domain.get("relation_roster", {}).get(
        "exact_transition_evaluator", {}).get(
            "legacy_group_eval_canary_count", -1)
    print(FINAL_MARKER + f" state={state} grade=CANDIDATE "
          f"rank_B_joint={rank} canaries={canaries} "
          f"domain_seconds={domain_seconds:g} bytes={len(raw)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
