#!/usr/bin/env python3
"""Task995: independent fixed-lambda, one-batch cycle checker.

The frozen continuation is an admitted read-only parent.  Selection belongs to
its separator; a growing reduction state does not export a current separator.
Only a complete finalizer can justify a new public physical HEAD.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import tempfile
import time
from typing import Any, Callable

import numpy as np

REPOSITORY = Path(__file__).resolve().parents[1]
RETAINED_CHECKER = "search/check_d972_r07_complete_oracle_cegar_continuation_v2.py"
RETAINED_CHECKER_BYTES = 129557
RETAINED_CHECKER_SHA = "e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"
_retained_path = REPOSITORY / RETAINED_CHECKER
if (_retained_path.is_symlink() or _retained_path.stat().st_size != RETAINED_CHECKER_BYTES or
        hashlib.sha256(_retained_path.read_bytes()).hexdigest() != RETAINED_CHECKER_SHA):
    raise ValueError("cycle_batch:retained_checker_source_pin")
import check_d972_r07_complete_oracle_cegar_continuation_v2 as C

O, E, L, BASE, REFINE = C.O, C.E, C.LEGACY, C.BASE, C.REFINE
canonical, sha, pack, unpack, dot = C.canonical, C.sha, C.pack, C.unpack, C.dot
SCHEMA = "d972.r07.fixed-lambda-cycle-batch.v1"
PHYSICAL, TOP, LOWER, VERTICES, EDGES, CHORDS, ROW_BYTES = 48384, 36288, 96776, 54432, 108864, 54433, 12096
BATCH_SIZE = 32
POLICY = "CHORD_FIRST_ROSTER_32_THEN_FIRST_AUX"
PARTIAL_POLICY = "PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY"
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
PARENT_ROLES = ("state", "delta", "seed34", "packet", "refinement", "oracle", "e", "prepare",
                "block-0", "block-1", "block-2", "block-3", "p1", "task712", "continuation")
PRODUCER_FILE = "search/d972_r07_fixed_lambda_cycle_batch_v1.py"
CHECKER_FILE = "search/check_d972_r07_fixed_lambda_cycle_batch_v1.py"
FORMULA = "v548-fixed-section;v547-signed-word;canonical-P1;four-B;batch-physical-reduction;single-final-separator"
SCOPE = {"vertices": VERTICES, "edges": EDGES, "chords": CHORDS, "legality_rows": 5, "source_lower": LOWER,
    "physical_lower": 32260, "physical": PHYSICAL, "p1_rows": 8059, "characters": [0, 1, 2, 3],
    "auxiliary_tests": 2, "batch_size": BATCH_SIZE, "max_batches": 1}
SELECTION_PHASES = ("section", "cochain", "tree")
CANDIDATE_PHASES = ("raw", "source", "primal", "p1", "B", "reduction")
DIAGNOSTIC_TYPES = {"resource-stop.json": ("resource-stop", "UNKNOWN_RESOURCE", "UNKNOWN_RESOURCE"),
                    "rejected.json": ("rejected", "FAIL", "REJECTED")}
RHO2_SHA = "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"
# Public metadata only, independently carried from the accepted source receipt.
CHECKER_DEPENDENCIES = {
    "search/check_d972_r07_complete_oracle_cegar_continuation_v2.py": (129557, RETAINED_CHECKER_SHA),
    "search/check_d972_r07_selected_cycle_materializer_v1.py": (103757, "a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4"),
    "search/check_d972_r07_section_cochain_oracle_v2.py": (84402, "a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d"),
    "search/check_d972_r07_section_cochain_oracle_v1.py": (80740, "2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967"),
    "search/check_d972_r07_full_origin_refinement_v1.py": (75083, "1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2"),
    "search/check_d972_r07_fixed_root_packet_loop_v2.py": (66251, "5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5"),
    "search/check_d972_r07_actual_root_seed_materializer_v3.py": (64626, "eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701"),
    "search/check_d972_r07_rank1355_root_seed_scalars_v1.py": (36236, "f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62"),
    "search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py": (119619, "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6"),
    "search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py": (141770, "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"),
}
PRODUCER_DEPENDENCIES = {
    "search/d972_r07_complete_oracle_cegar_continuation_v1.py": (126940, "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"),
    "search/d972_r07_selected_cycle_materializer_v1.py": (88929, "4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3"),
    "search/d972_r07_section_cochain_oracle_v1.py": (73290, "4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb"),
    "search/d972_r07_full_origin_refinement_v1.py": (97806, "d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa"),
    "search/d972_r07_fixed_root_packet_loop_v2.py": (84173, "e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6"),
    "search/d972_r07_actual_root_seed_materializer_v3.py": (86643, "36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332"),
    "search/d972_r07_rank1355_root_seed_scalars_v1.py": (31578, "973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb"),
    "search/d972_r07_actual_grade2_root_scalar_batch_v2.py": (118315, "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856"),
    "search/d972_r07_targeted_grade2_owner_generated_join_v15.py": (126565, "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"),
}
DATA_PINS = {
    "scratchpad/fuda1_a0_rmax_data.g": (4709, "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"),
    "scratchpad/a0_paper_words_v1.json": (115928, "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"),
    "scratchpad/a0_v2_words.json": (106133, "fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"),
}
FIXED_ARTIFACTS = {
    "state": (33891714539, "7b7b9de20faaa3b8f26e331bb738b374f6f5708c", 9944214057,
        "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1", 107195261,
        "2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017", "d972-r07-grade2-physical-state-separator-v2.yml"),
    "delta": (33946247365, "7f6dfaddf4150449e62a9b3e85def472fcb41c01", 9963533999,
        "d972-r07-actual-seed30-materializer-v1-candidate-33946247365-1", 915410,
        "f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6", "d972-r07-actual-seed30-materializer-v1.yml"),
    "seed34": (33956437467, "b9ae78b0950b186463849c3ec874f6474f359851", 9966542166,
        "d972-r07-actual-root-seed-materializer-v3-candidate-33956437467-1", 984053,
        "a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc", "d972-r07-actual-root-seed-materializer-v3.yml"),
    "packet": (33964709359, "fff114c41bd8748ad0e708919fe0820335c9cce8", 9969090590,
        "d972-r07-fixed-root-packet-loop-v2-candidate-33964709359-1", 1855391,
        "b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428", "d972-r07-fixed-root-packet-loop-v2.yml"),
    "refinement": (33971897879, "64475e1dfab1537a38d1b3131971bfed5fc3071c", 9971466432,
        "d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1", 51943596,
        "0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8", "d972-r07-full-origin-checker-completion-v1.yml"),
    "oracle": (33977701313, "bbce98d8f95a845f36fe89c0f507b9360792666f", 9972829869,
        "d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1", 2299772,
        "1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d", "d972-r07-section-cochain-checker-completion-v1.yml"),
    "e": (33981657987, "444c71c9e554ae8feb9c8ee54df57d3df19ed66f", 9973974150,
        "d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1", 2816692,
        "884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25", "d972-r07-selected-cycle-materializer-v1.yml"),
    "p1": (33851744070, "6673eb2ea15ca6022acc2ddc5a8a204a0380172f", 9931437113,
        "task809-canonical-p1-degree2-lift-v9-33851744070-1", 641518300,
        "6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c", "d972-r07-canonical-p1-dag-degree2-lift-v9.yml"),
    "task712": (33814194630, "5ff2c5a30b604536df12acba8801828a5a7e5fe0", 9915928157,
        "d972-r07-grade2-maps-v4-33814194630-1", 22404961,
        "abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858", "d972-r07-grade2-maps-v4.yml"),
    "continuation": (33990567016, "c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70", 9977040548,
        "d972-r07-complete-oracle-cegar-resume64-v1-candidate-33990567016-1", 304642285,
        "a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792", "d972-r07-complete-oracle-cegar-resume64-v1.yml"),
}
for _role, _id, _name, _size, _sha in (
    ("prepare", 9865061266, "prepare", 204360988, "da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4"),
    ("block-0", 9865238399, "state-block-0", 81729645, "2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838"),
    ("block-1", 9865242284, "state-block-1", 82259824, "849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb"),
    ("block-2", 9865193269, "state-block-2", 82200189, "d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d"),
    ("block-3", 9865239848, "state-block-3", 82266526, "87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92"),
):
    FIXED_ARTIFACTS[_role] = (33677346616, "22c6dddb43d107c05e65f53ad898823ae8ebe276", _id,
        f"task554-grade1-v3-{_name}-33677346616-1", _size, _sha, "d972-r07-a0-first-rung-grade1-v3.yml")
STARTED = time.monotonic()
DEADLINE: float | None = None
MAX_RSS_BYTES: int | None = None
LAST_PHASE = "initialization"
CHECKED_CURSOR: dict[str, Any] = {"selection_compared": False, "processed_candidates": 0,
    "accepted_new_rows": 0, "last_complete_phase": None, "public_head_compared": False}


class ResourceStop(Exception):
    pass


def require(condition: Any, label: str) -> None:
    if not condition:
        raise ValueError("cycle_batch:" + label)


def integer(value: Any, label: str, lower: int = 0, upper: int | None = None) -> int:
    require(type(value) is int and value >= lower and (upper is None or value <= upper), label)
    return value


def boundary(phase: str, **fields: Any) -> None:
    global LAST_PHASE
    LAST_PHASE = phase
    if DEADLINE is not None and time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)
    if MAX_RSS_BYTES is not None:
        try:
            import resource
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024 > MAX_RSS_BYTES:
                raise ResourceStop("memory:" + phase)
        except ImportError:
            pass
    if fields:
        print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def document(kind: str, fields: dict[str, Any]) -> dict[str, Any]:
    # Exported nested values never alias a later mutation of a reduction state.
    value = {"schema": SCHEMA + "." + kind, **copy.deepcopy(fields)}
    return {**value, "sha256": sha(canonical(value))}


def scalar(value: Any, label: str) -> int:
    return integer(value, label, 0, 2)


def trit_vector(value: np.ndarray, size: int, label: str) -> None:
    require(isinstance(value, np.ndarray) and value.shape == (size,) and value.dtype == np.uint8 and
            not np.any(value > 2), label)


def packed_vector(raw: bytes, size: int, label: str) -> np.ndarray:
    require(type(raw) is bytes and len(raw) == (size + 3) // 4 and
            not np.any(np.frombuffer(raw, dtype=np.uint8) > 80), label + ":packed_bytes")
    value = unpack(raw, size)
    require(pack(value) == raw, label + ":canonical_padding_and_EOF")
    return value


def select_all_residuals(chord_edges: np.ndarray, tau: np.ndarray, values: np.ndarray,
                         basis_indices: list[int], inverse: np.ndarray,
                         residuals: np.ndarray, b_aux: np.ndarray) -> dict[str, Any]:
    """Only the registered first 32 failures are offered; the whole array is read."""
    require(chord_edges.shape == (CHORDS,) and np.issubdtype(chord_edges.dtype, np.integer) and
            np.all(chord_edges >= 0) and np.all(chord_edges < EDGES) and
            len(np.unique(chord_edges)) == CHORDS, "complete_distinct_actual_chord_roster")
    require(tau.shape == (CHORDS, 5) and tau.dtype == np.uint8 and not np.any(tau > 2), "complete_five_carry_rows")
    trit_vector(values, CHORDS, "complete_chord_values")
    trit_vector(residuals, CHORDS, "complete_chord_residuals")
    trit_vector(b_aux, 2, "both_auxiliary_tests")
    require(type(basis_indices) is list and len(basis_indices) == 5 and
            len(set(basis_indices)) == 5 and all(type(i) is int and 0 <= i < CHORDS for i in basis_indices),
            "five_actual_basis_roster_indices")
    basis = tau[basis_indices].astype(np.int64)
    require(inverse.shape == (5, 5) and np.issubdtype(inverse.dtype, np.integer) and
        not np.any(inverse < 0) and not np.any(inverse > 2) and np.array_equal(
        basis.T @ inverse.astype(np.int64) % 3, np.eye(5, dtype=np.int64)), "fixed_tau_inverse_orientation")
    fit = values[basis_indices].astype(np.int64) @ inverse.astype(np.int64) % 3
    require(np.array_equal(residuals, (values.astype(np.int64) - tau.astype(np.int64) @ fit) % 3),
            "every_residual_matches_fixed_basis_fit")
    failed = np.flatnonzero(residuals)
    bodies = []
    if len(failed):
        mode = "CHORD_BATCH"
        for ordinal, position in enumerate(failed[:BATCH_SIZE]):
            position = int(position)
            coefficients = inverse.astype(np.int64) @ tau[position].astype(np.int64) % 3
            direct_tau = (tau[position].astype(np.int64) - coefficients @ basis) % 3
            selected_scalar = int((int(values[position]) - coefficients @ values[basis_indices].astype(np.int64)) % 3)
            require(not np.any(direct_tau) and selected_scalar == int(residuals[position]) and selected_scalar in (1, 2),
                    "each_selected_six_cycle_legal_and_nonzero")
            basis_edges = [int(chord_edges[i]) for i in basis_indices]
            cycles = [{"edge": int(chord_edges[position]), "coefficient": 1}] + [
                {"edge": edge, "coefficient": int(-coefficient % 3)}
                for edge, coefficient in zip(basis_edges, coefficients)]
            bodies.append({"ordinal": ordinal, "roster_index": position, "witness": {
                "kind": "chord", "failed_chord": int(chord_edges[position]), "basis_chords": basis_edges,
                "basis_coefficients": coefficients.tolist(), "cycles": cycles, "eta": [0, 0],
                "tau": direct_tau.tolist(), "scalar": selected_scalar, "materialization": "MATERIALIZATION_PENDING"}})
    elif np.any(b_aux):
        mode = "AUXILIARY"
        coordinate = int(np.flatnonzero(b_aux)[0])
        eta = [0, 0]; eta[coordinate] = 1
        bodies.append({"ordinal": 0, "roster_index": None, "witness": {
            "kind": "auxiliary", "coordinate": coordinate, "cycles": [], "eta": eta,
            "tau": [0] * 5, "scalar": int(b_aux[coordinate]), "materialization": "MATERIALIZATION_PENDING"}})
    else:
        mode = "COMPLETE_ZERO_CANDIDATE"
    require(len(bodies) <= BATCH_SIZE, "one_batch_candidate_limit")
    boundary("fixed_lambda_all_residuals_selected", chords=CHORDS, failed=len(failed), selected=len(bodies))
    return {"mode": mode, "fit": fit.astype(np.uint8), "failed_indices": failed.astype(np.uint32),
        "failed_edges": chord_edges[failed].astype(np.uint32), "candidates": bodies,
        "first_failed_index": int(failed[0]) if len(failed) else None,
        "first_failed_edge": int(chord_edges[failed[0]]) if len(failed) else None}


@dataclass
class SelectionArithmetic:
    section: dict[str, Any]
    score: np.ndarray
    f: np.ndarray
    b_aux: np.ndarray
    tree: dict[str, Any]
    plan: dict[str, Any]
    ordinary_anchor: dict[str, Any]


@dataclass
class DecisionArithmetic:
    raw: np.ndarray
    remainder: np.ndarray
    reductions: list[dict[str, Any]]
    selected_scalar: int
    remainder_scalar: int
    normalized: np.ndarray | None
    lead: int | None
    sigma: int | None
    target_before: np.ndarray
    target_after: np.ndarray
    target_scalar: int | None

    @property
    def dependent(self) -> bool:
        return self.normalized is None


class BatchReductionState:
    """Private growing span.  Its only functional is the immutable selection one."""

    def __init__(self, anchor: ThinAnchor, old_continuation_rows: int):
        require(anchor.kind == "Separator" and anchor.functional is not None, "batch_requires_separator_anchor")
        self.anchor = anchor
        self.old_continuation_rows = integer(old_continuation_rows, "old_continuation_row_count")
        self.anchor_rank, self.anchor_generation, self.anchor_head = anchor.rank, anchor.generation, anchor.head
        self.selection_lambda = anchor.functional.copy()
        self.initial_target, self.target = anchor.target.copy(), anchor.target.copy()
        self.pivots = copy.deepcopy(anchor.pivots)
        self.rows: list[bytes] = []
        self.row_manifests: list[str] = []
        self.parents = copy.deepcopy(anchor.parents)
        self.physical_head = anchor.head
        self.processed_candidates = 0
        self.dependent_candidates = 0
        self.decisions: list[dict[str, Any]] = []

    @property
    def rank(self) -> int:
        return self.anchor_rank + len(self.rows)

    @property
    def generation(self) -> int:
        return self.anchor_generation + len(self.rows)

    def row(self, row_id: int) -> bytes:
        integer(row_id, "batch_physical_row_id", 0, self.rank - 1)
        return self.anchor.row(row_id) if row_id < self.anchor_rank else self.rows[row_id - self.anchor_rank]

    def reduce(self, raw: np.ndarray, selected_scalar: int) -> DecisionArithmetic:
        trit_vector(raw, PHYSICAL, "candidate_full_physical_raw")
        require(np.any(self.target), "no_candidate_after_linear_target")
        require(scalar(selected_scalar, "candidate_selection_scalar") in (1, 2) and
                dot(self.selection_lambda, raw) == selected_scalar, "candidate_selected_under_frozen_lambda")
        remainder, reductions = L.reduce_dense(raw, self.pivots, self.row, verbose=True)
        remainder_scalar = dot(self.selection_lambda, remainder)
        new_contribution = 0
        for event in reductions:
            if event["pivot_id"] >= self.anchor_rank:
                new_contribution += event["scalar"] * dot(self.selection_lambda, unpack(self.row(event["pivot_id"]), PHYSICAL))
        require(remainder_scalar == (selected_scalar - new_contribution) % 3,
                "frozen_lambda_remainder_accounts_for_new_rows")
        if not np.any(remainder):
            require(remainder_scalar == 0, "dependent_full_zero_remainder")
            return DecisionArithmetic(raw.copy(), remainder, reductions, selected_scalar, remainder_scalar,
                None, None, None, self.target.copy(), self.target.copy(), None)
        normalized, lead, sigma = L.normalize(remainder)
        target, coefficient = L.next_target(self.target, normalized, lead, [p["lead"] for p in self.pivots])
        require(np.array_equal((self.target.astype(np.int16) - target) % 3,
                               coefficient * normalized.astype(np.int16) % 3), "complete_target_subtraction_identity")
        return DecisionArithmetic(raw.copy(), remainder, reductions, selected_scalar, remainder_scalar,
            normalized, lead, sigma, self.target.copy(), target, coefficient)

    def advance(self, decision: DecisionArithmetic, physical_head: str | None,
                parent_record: dict[str, Any] | None, row_manifest_sha: str | None = None) -> None:
        require(np.array_equal(self.target, decision.target_before), "decision_target_has_same_private_parent")
        if decision.dependent:
            require(physical_head is None and parent_record is None and row_manifest_sha is None and not np.any(decision.remainder) and
                    decision.lead is decision.sigma is decision.target_scalar is None and
                    np.array_equal(decision.target_after, self.target), "dependent_has_no_physical_append")
            self.dependent_candidates += 1
        else:
            require(isinstance(physical_head, str) and re.fullmatch(r"[0-9a-f]{64}", physical_head) is not None and
                    isinstance(parent_record, dict) and type(row_manifest_sha) is str and
                    re.fullmatch(r"[0-9a-f]{64}", row_manifest_sha) and self.rank < PHYSICAL, "accepted_row_new_physical_provenance")
            require(decision.normalized is not None and decision.lead is not None and decision.sigma in (1, 2),
                    "accepted_decision_normalized_type")
            self.pivots.append({"offer": self.generation, "lead": decision.lead, "physical_offset": self.rank * ROW_BYTES,
                "coefficient_offset": None, "rolling_sha256": physical_head})
            self.rows.append(pack(decision.normalized))
            self.row_manifests.append(row_manifest_sha)
            self.parents.append(copy.deepcopy(parent_record))
            self.target = decision.target_after.copy()
            self.physical_head = physical_head
        self.processed_candidates += 1
        require(self.processed_candidates <= BATCH_SIZE and self.rank == len(self.pivots), "private_candidate_and_rank_counters")

    def finish_arithmetic(self) -> dict[str, Any]:
        if not np.any(self.target):
            return {"kind": "LinearMembershipCandidate", "lambda": None, "separator": None, "direct_pairing": None}
        if self.rows:
            last = self.pivots[-1]
            solved = L.next_separator(self.target, self.pivots[:-1], unpack(self.rows[-1], PHYSICAL),
                                      last["lead"], self.row, last["offer"])
            functional = solved["lambda"]
        else:
            solved = None
            functional = self.selection_lambda.copy()
        pairings = []
        for row_id in range(self.rank):
            pairings.append(dot(functional, unpack(self.row(row_id), PHYSICAL)))
            if (row_id + 1) % 256 == 0:
                boundary("finalizer_all_physical_rows", rows=row_id + 1)
        initial_dot, final_dot = dot(functional, self.initial_target), dot(functional, self.target)
        require(not any(pairings) and initial_dot == final_dot == 1, "finalizer_actual_all_rows_both_targets")
        direct = {"rows": self.rank, "row_pairings_sha256": sha(bytes(pairings)), "lambda_pivots": 0,
                  "lambda_parent_remainder": initial_dot, "lambda_new_remainder": final_dot}
        return {"kind": "Separator", "lambda": functional, "separator": solved, "direct_pairing": direct}


def relative_name(value: Any, label: str) -> str:
    require(type(value) is str and value and "\\" not in value and "\x00" not in value,
            label + ":relative_text")
    parts = value.split("/")
    require(all(part not in ("", ".", "..") for part in parts) and
            not Path(value).is_absolute() and ":" not in value, label + ":relative_components")
    return value


def file_path(root: Path, name: str) -> Path:
    name = relative_name(name, "file_path")
    require(root.is_dir() and not root.is_symlink(), "file_path_root")
    candidate = root
    for part in name.split("/"):
        candidate /= part
        require(not candidate.is_symlink(), "file_path_no_symlink")
    require(candidate.is_file() and candidate.resolve().is_relative_to(root.resolve()), "file_path_containment")
    return candidate


def json_value(raw: bytes, label: str, canonical_required: bool = False) -> Any:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, label + ":duplicate_key")
            result[key] = value
        return result

    def nonfinite(value: str) -> Any:
        raise ValueError("cycle_batch:" + label + ":nonfinite:" + value)

    result = json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=nonfinite)
    require(not canonical_required or canonical(result) == raw, label + ":canonical_bytes")
    return result


def check_document(value: Any, suffix: str | None = None) -> None:
    require(type(value) is dict and type(value.get("sha256")) is str and
            re.fullmatch(r"[0-9a-f]{64}", value["sha256"]) is not None, "document_seal_type")
    require(value["sha256"] == sha(canonical({key: item for key, item in value.items() if key != "sha256"})),
            "document_seal")
    require(suffix is None or value.get("schema") == SCHEMA + "." + suffix, "document_schema")


def same_json(left: Any, right: Any, label: str) -> None:
    require(canonical(left) == canonical(right), label)


def receipt(name: str, raw: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def pin_receipts(pins: dict[str, tuple[int, str]]) -> list[dict[str, Any]]:
    return [{"file": name, "bytes": identity[0], "sha256": identity[1]} for name, identity in sorted(pins.items())]


def check_file_descriptor(value: Any) -> None:
    require(type(value) is dict and set(value) == {"file", "bytes", "sha256"}, "file_descriptor_fields")
    relative_name(value["file"], "file_descriptor_name")
    integer(value["bytes"], "file_descriptor_bytes")
    require(type(value["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", value["sha256"]), "file_descriptor_hash")


def artifact_identity(role: str) -> dict[str, Any]:
    run, head, identifier, name, size, digest, workflow = FIXED_ARTIFACTS[role]
    return {"run": run, "attempt": 1, "head": head, "workflow": ".github/workflows/" + workflow,
        "id": identifier, "name": name, "bytes": size, "sha256": "sha256:" + digest,
        "repository_id": 1312092366, "conclusion": "failure" if role == "prepare" or role.startswith("block-") else "success"}


def registered_limits(args: argparse.Namespace) -> dict[str, Any]:
    return {"batch_size": BATCH_SIZE, "max_batches": 1, "selection_policy": POLICY, "partial_policy": PARTIAL_POLICY,
        "refill": False, "producer_limits": {"max_seconds": args.producer_max_seconds,
            "max_memory_mib": args.producer_max_memory_mib},
        "checker_limits": {"max_seconds": args.max_seconds, "max_memory_mib": args.max_memory_mib}}


class AcceptedInputs:
    """Exact Task997 admission, portable identity, complete original inventories."""

    def __init__(self, args: argparse.Namespace):
        self.args = args
        require(args.acceptance.is_file() and not args.acceptance.is_symlink(), "actual_acceptance_file")
        raw = args.acceptance.read_bytes()
        require(len(raw) <= 64 << 20, "acceptance_bounded_bytes")
        value = json_value(raw, "acceptance", True)
        require(type(value) is dict and set(value) == {"schema", "parents", "anchor", "code", "runtime", "registration"} and
                value["schema"] == SCHEMA + ".acceptance", "acceptance_exact_six_plain_keys")
        require(type(value["parents"]) is list and [item["role"] for item in value["parents"]] == list(PARENT_ROLES),
                "acceptance_all_fifteen_parent_roles")
        self.value, self.raw, self.sha256 = value, raw, sha(raw)
        portable = copy.deepcopy(value)
        roots = {role: getattr(args, role.replace("-", "_") + "_root") for role in PARENT_ROLES if not role.startswith("block-")}
        require(type(args.block_root) is list and len(args.block_root) == 4, "exact_four_block_roots")
        roots.update({f"block-{owner}": args.block_root[owner] for owner in range(4)})
        self.trees: dict[str, PinnedTree] = {}
        for item, portable_item in zip(value["parents"], portable["parents"]):
            require(type(item) is dict and set(item) == {"role", "path", "artifact", "files", "directories"},
                    "accepted_parent_exact_keys")
            role = item["role"]
            require(type(item["path"]) is str and Path(item["path"]).is_absolute() and
                    item["path"] == str(roots[role].resolve()), "accepted_parent_actual_CLI_path")
            same_json(item["artifact"], artifact_identity(role), "registered_actual_parent_artifact:" + role)
            require(type(item["files"]) is list and type(item["directories"]) is list, "whole_parent_inventory_type")
            del portable_item["path"]
            self.trees[role] = PinnedTree(role, roots[role], item["files"], item["directories"])
        self.portable = portable
        self.portable_sha256 = sha(canonical(portable))
        same_json(value["runtime"], {"python": sys.version, "numpy": np.__version__}, "actual_registered_runtime")
        registration = registered_limits(args)
        for limits in (registration["producer_limits"], registration["checker_limits"]):
            integer(limits["max_seconds"], "registered_seconds", 1)
            integer(limits["max_memory_mib"], "registered_memory_mib", 1)
        same_json(value["registration"], registration, "same_declared_resource_and_batch_limits")
        require(registration["producer_limits"] == {"max_seconds": 5400, "max_memory_mib": 7168} and
                registration["checker_limits"] == {"max_seconds": 10800, "max_memory_mib": 7168},
                "first_registered_batch_resource_envelope")
        code = value["code"]
        require(type(code) is dict and set(code) == {"producer", "checker", "producer_dependencies", "checker_dependencies", "data"},
                "code_exact_closure_keys")
        check_file_descriptor(code["producer"])
        check_file_descriptor(code["checker"])
        require(code["producer"]["file"] == PRODUCER_FILE and code["checker"]["file"] == CHECKER_FILE,
                "registered_new_executable_paths")
        same_json(code["producer_dependencies"], pin_receipts(PRODUCER_DEPENDENCIES), "registered_retained_P_metadata_pins")
        same_json(code["checker_dependencies"], pin_receipts(CHECKER_DEPENDENCIES), "registered_retained_C_metadata_pins")
        same_json(code["data"], pin_receipts(DATA_PINS), "registered_three_raw_inputs")
        self.code_files = sorted([code["producer"], code["checker"], *code["producer_dependencies"],
                                 *code["checker_dependencies"], *code["data"]], key=lambda item: item["file"])
        require(len(self.code_files) == len({item["file"] for item in self.code_files}), "unique_union_code_and_raw_files")
        self.authenticate_code()
        self.anchor_metadata()

    def authenticate_code(self) -> None:
        for item in self.code_files:
            check_file_descriptor(item)
            actual = hash_file(file_path(REPOSITORY, item["file"]), item["file"])
            require(actual == (item["bytes"], item["sha256"]), "executed_code_or_raw_full_pin")

    def anchor_metadata(self) -> None:
        anchor, tree = self.value["anchor"], self.trees["continuation"]
        require(type(anchor) is dict and set(anchor) == {"head", "result", "checker", "owner", "source", "start", "fixed",
            "invocations", "checker_prefix", "completed_steps", "rank", "generation", "kind", "state_head",
            "target_remainder_sha256", "lambda_sha256", "terminal"}, "accepted_anchor_exact_keys")
        expected_names = {"head": "output/HEAD", "result": "output/result.json", "checker": "checker-result.json",
            "owner": "output/owner.json", "source": "output/source.json", "start": "output/start.json", "fixed": "output/fixed/manifest.json"}
        for key, name in expected_names.items():
            same_json(anchor[key], tree.by_name[name], "anchor_seven_exact_entry_pins:" + key)
        checked, result, head, source = (tree.json(name, True) for name in
                                       ("checker-result.json", "output/result.json", "output/HEAD", "output/source.json"))
        for key in ("completed_steps", "rank", "generation", "kind", "state_head", "target_remainder_sha256", "lambda_sha256"):
            same_json(anchor[key], head[key], "actual_anchor_value:" + key)
        same_json(anchor["terminal"], result["terminal"], "actual_anchor_terminal")
        require(anchor["completed_steps"] == 64 and anchor["rank"] == 1450 and anchor["generation"] == 8155 and
                anchor["kind"] == "Separator" and anchor["terminal"] == "UNKNOWN_CAP", "observed_64_anchor_only")
        expected_invocations = [item for item in tree.files if item["file"].startswith("output/invocations/")]
        same_json(anchor["invocations"], expected_invocations, "all_saved_invocation_files_including_diagnostics")
        expected_prefix = {"steps": len(checked["steps"]), "snapshots": len(checked["snapshots"]),
            "steps_sha256": sha(canonical(checked["steps"])), "snapshots_sha256": sha(canonical(checked["snapshots"])),
            "invocations_sha256": sha(canonical(checked["invocations"]))}
        same_json(anchor["checker_prefix"], expected_prefix, "accepted_complete_checker_lists")
        require(expected_prefix["steps"] == expected_prefix["snapshots"] == 64 and
                source["python"] == checked["python"] == self.value["runtime"]["python"] and
                source["numpy"] == checked["numpy"] == self.value["runtime"]["numpy"], "accepted_old_same_runtime")

    def parent_inventory(self) -> list[dict[str, Any]]:
        return [{"role": role, "files": copy.deepcopy(self.trees[role].files),
                 "directories": copy.deepcopy(self.trees[role].directories)} for role in PARENT_ROLES]

    def unchanged(self) -> None:
        require(self.args.acceptance.read_bytes() == self.raw, "acceptance_unchanged")
        self.authenticate_code()
        for role in PARENT_ROLES:
            self.trees[role].authenticate()

    def external_state(self) -> dict[str, Any]:
        # This is a typed adapter for fixed source inputs, not a historical
        # state reconstruction.  The retained literal reader needs these two
        # authenticated metadata joins in addition to the Task554 descriptors.
        index = self.trees["continuation"].json("output/fixed/canonical-index.json", True)
        original_index = self.trees["refinement"].json("output/canonical-index.json", True)
        same_json(index, original_index, "same_accepted_canonical_P1_index")
        p1_parent = self.trees["delta"].json("output/result.json", True)["parents"]["p1"]
        return {"task554": L.ROOTS.task554_parent(self.args),
            "accepted_refinement": {"index": copy.deepcopy(index)},
            "launch": {"p1_parent": copy.deepcopy(p1_parent)}}


def hash_file(path: Path, label: str) -> tuple[int, str]:
    digest, count = hashlib.sha256(), 0
    with path.open("rb", buffering=1 << 20) as stream:
        while True:
            data = stream.read(1 << 20)
            if not data:
                break
            digest.update(data)
            count += len(data)
            if count % (64 << 20) == 0:
                boundary("input_hash", input=label, bytes=count)
    return count, digest.hexdigest()


def tree_names(root: Path) -> tuple[list[str], list[str]]:
    require(root.is_dir() and not root.is_symlink(), "tree_root")
    files, directories, pending = [], [], [root]
    while pending:
        parent = pending.pop()
        with os.scandir(parent) as entries:
            for item in entries:
                require(not item.is_symlink(), "tree_symlink")
                path = Path(item.path)
                name = path.relative_to(root).as_posix()
                relative_name(name, "tree_name")
                if item.is_dir(follow_symlinks=False):
                    directories.append(name)
                    pending.append(path)
                else:
                    require(item.is_file(follow_symlinks=False), "tree_regular_file")
                    files.append(name)
    return sorted(files), sorted(directories)


class PinnedTree:
    """Whole immutable artifact authentication; hidden diagnostics remain data."""

    def __init__(self, role: str, root: Path, files: list[dict[str, Any]], directories: list[str]):
        self.role, self.root = role, root
        self.files = copy.deepcopy(files)
        self.directories = copy.deepcopy(directories)
        names = []
        for record in self.files:
            require(set(record) == {"file", "bytes", "sha256"}, "pinned_file_fields")
            names.append(relative_name(record["file"], "pinned_file"))
            integer(record["bytes"], "pinned_file_bytes")
            require(type(record["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", record["sha256"]),
                    "pinned_file_sha256")
        require(names == sorted(set(names)) and self.directories == sorted(set(self.directories)),
                "pinned_tree_sorted_unique")
        for name in self.directories:
            relative_name(name, "pinned_directory")
        self.by_name = {record["file"]: record for record in self.files}
        self.authenticate()

    def authenticate(self) -> None:
        files, directories = tree_names(self.root)
        require(files == list(self.by_name) and directories == self.directories, "whole_parent_roster:" + self.role)
        for number, record in enumerate(self.files):
            observed = hash_file(file_path(self.root, record["file"]), self.role + "/" + record["file"])
            require(observed == (record["bytes"], record["sha256"]), "whole_parent_file:" + self.role)
            if number % 128 == 0:
                boundary("parent_files_authenticated", role=self.role, files=number + 1, total=len(self.files))

    def read(self, name: str, cap: int = 64 << 20) -> bytes:
        record = self.by_name[name]
        require(record["bytes"] <= cap, "bounded_parent_read")
        raw = file_path(self.root, name).read_bytes()
        require((len(raw), sha(raw)) == (record["bytes"], record["sha256"]), "parent_read_pin")
        return raw

    def json(self, name: str, canonical_required: bool = False, cap: int = 64 << 20) -> Any:
        return json_value(self.read(name, cap), self.role + "/" + name, canonical_required)

    def expected(self, name: str, identity: tuple[int, str]) -> None:
        record = self.by_name[name]
        require((record["bytes"], record["sha256"]) == tuple(identity), "retained_parent_pin:" + self.role)


@dataclass(frozen=True)
class SavedPhysicalRow:
    tree: PinnedTree
    file: str
    offset: int
    sha256: str | None


def base_pivot_metadata(tree: PinnedTree) -> list[dict[str, Any]]:
    """Authenticate 8059 saved instructions without replaying their offers."""
    for name in ("state/manifest.json", "state/HEAD", "state/physical.bin", "state/instructions.jsonl"):
        tree.expected(name, L.STATE_FILES[name])
    state, head = tree.json("state/manifest.json"), tree.json("state/HEAD")
    require(state["rank"] == head["rank"] == 1354 and state["generation"] == head["generation"] == 8059 and
            state["cursor"] == head["cursor"] == 8059 and head["rolling_head"] == L.OLD_HEAD and
            head["manifest_sha256"] == L.STATE_FILES["state/manifest.json"][1] and
            state["physical"]["sha256"] == L.STATE_FILES["state/physical.bin"][1], "thin_base_identity")
    result, rolling, digest, count = [], "0" * 64, hashlib.sha256(), 0
    with file_path(tree.root, "state/instructions.jsonl").open("rb", buffering=1 << 20) as stream:
        for offer in range(8059):
            raw = stream.readline(2 << 20)
            require(raw.endswith(b"\n"), "thin_base_instruction_eof")
            item = json_value(raw, "base_instruction", True)
            require(item["offer"] == offer and item["rolling_sha256"] == sha(bytes.fromhex(rolling) +
                    canonical({key: value for key, value in item.items() if key != "rolling_sha256"})),
                    "thin_base_instruction_rolling")
            rolling = item["rolling_sha256"]
            digest.update(raw)
            count += len(raw)
            if item["kind"] == "physical_pivot":
                require(item["physical_offset"] == len(result) * ROW_BYTES and
                        item["coefficient_offset"] == len(result) * 2015 and item["rank"] == len(result) + 1,
                        "thin_base_row_position")
                integer(item["lead"], "thin_base_lead", 0, PHYSICAL - 1)
                result.append({"offer": offer, "lead": item["lead"], "physical_offset": item["physical_offset"],
                               "coefficient_offset": item["coefficient_offset"], "rolling_sha256": rolling})
        require(stream.read(1) == b"", "thin_base_instruction_tail")
    require((count, digest.hexdigest()) == L.STATE_FILES["state/instructions.jsonl"] and rolling == L.OLD_HEAD and
            len(result) == len({row["lead"] for row in result}) == 1354, "thin_base_complete_metadata")
    return result


class ThinAnchor:
    """Saved normalized rows plus one directly measured current separator.

    Admission supplies the successful old checker and all exact file receipts.
    No accepted oracle, E, physical reduction, or separator solve is rerun here.
    """

    def __init__(self, pivots: list[dict[str, Any]], rows: list[SavedPhysicalRow], current: dict[str, Any],
                 target: bytes, previous_target: bytes, functional: bytes, parents: list[dict[str, Any]]):
        self.pivots, self.parents = copy.deepcopy(pivots), copy.deepcopy(parents)
        self.rows = list(rows)
        self.rank = integer(current["rank"], "anchor_rank", 1, PHYSICAL)
        self.generation = integer(current["generation"], "anchor_generation", self.rank)
        self.head, self.kind = current["state_head"], current["kind"]
        self.completed_steps = integer(current["completed_steps"], "anchor_completed_steps")
        require(self.kind == "Separator" and len(self.pivots) == len(self.rows) == self.rank and
                len({row["lead"] for row in self.pivots}) == self.rank, "anchor_complete_row_metadata")
        self.target = packed_vector(target, PHYSICAL, "anchor_target")
        self.previous_target = packed_vector(previous_target, PHYSICAL, "anchor_previous_target")
        self.functional = packed_vector(functional, PHYSICAL, "anchor_lambda")
        require(sha(target) == current["target_remainder_sha256"] and sha(functional) == current["lambda_sha256"],
                "anchor_head_payload_identity")
        self.stack = ExitStack()
        self.streams: dict[tuple[str, str], Any] = {}
        self.direct_pairing: dict[str, Any] | None = None

    def __enter__(self) -> ThinAnchor:
        return self

    def __exit__(self, *error: Any) -> None:
        self.stack.close()

    def row(self, index: int) -> bytes:
        index = integer(index, "anchor_row_index", 0, self.rank - 1)
        entry = self.rows[index]
        key = (entry.tree.role, entry.file)
        if key not in self.streams:
            self.streams[key] = self.stack.enter_context(file_path(entry.tree.root, entry.file).open("rb"))
        stream = self.streams[key]
        stream.seek(entry.offset)
        raw = stream.read(ROW_BYTES)
        require(len(raw) == ROW_BYTES and (entry.sha256 is None or sha(raw) == entry.sha256), "anchor_row_bytes")
        return raw

    def measure_selection(self) -> dict[str, Any]:
        values, leads = [], []
        for index, pivot in enumerate(self.pivots):
            lead = integer(pivot["lead"], "anchor_pivot_lead", 0, PHYSICAL - 1)
            row = packed_vector(self.row(index), PHYSICAL, "anchor_normalized_row")
            require(row[lead] == 1 and all(row[earlier] == 0 for earlier in leads), "anchor_triangular_row")
            values.append(dot(self.functional, row))
            leads.append(lead)
            if (index + 1) % 128 == 0:
                boundary("selection_direct_old_rows", rows=index + 1, total=self.rank)
        before, current = dot(self.functional, self.previous_target), dot(self.functional, self.target)
        require(not any(values) and before == current == 1 and not np.any(self.target[leads]),
                "selection_all_old_rows_and_both_targets")
        self.direct_pairing = {"rows": self.rank, "row_pairings_sha256": sha(bytes(values)), "lambda_pivots": 0,
                               "lambda_parent_remainder": before, "lambda_new_remainder": current}
        return copy.deepcopy(self.direct_pairing)


def saved_manifest_members(tree: PinnedTree, prefix: str, manifest: dict[str, Any]) -> None:
    check_document(manifest)
    names = []
    for item in manifest["files"]:
        name = relative_name(item["file"], "saved_manifest_file")
        require("/" not in name, "saved_manifest_local_filename")
        names.append(name)
        entry = tree.by_name[prefix + "/" + name]
        require(entry["bytes"] == item["bytes"] and entry["sha256"] == item["sha256"], "saved_manifest_exact_file_pin")
    require(names == sorted(set(names)), "saved_manifest_sorted_unique_files")


def restore_physical_anchor(trees: dict[str, PinnedTree]) -> tuple[ThinAnchor, dict[str, Any]]:
    """Read the accepted state chain and named identities; never rebuild it."""
    continuation = trees["continuation"]
    old_root = continuation.root / "output"
    objects = {name: continuation.json("output/" + name, True) for name in ("HEAD", "start.json", "owner.json", "source.json", "result.json")}
    head, start, owner, source, result = (objects[name] for name in ("HEAD", "start.json", "owner.json", "source.json", "result.json"))
    checked = continuation.json("checker-result.json", True)
    for item in (*objects.values(), checked):
        check_document(item)
    require(head["schema"] == C.SCHEMA + ".head" and result["schema"] == C.SCHEMA + ".result" and
            checked["schema"] == C.SCHEMA + ".checker-result" and checked["status"] == "PASS" and
            checked["checker_sha256"] == RETAINED_CHECKER_SHA and source["producer_sha256"] ==
            "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c", "accepted_continuation_code_and_success")
    count = integer(head["completed_steps"], "accepted_continuation_count", 1)
    for key in ("completed_steps", "rank", "generation", "kind", "state_head", "lambda_sha256", "target_remainder_sha256",
                "owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256",
                "current_snapshot_sha256", "current_checkpoint_sha256"):
        require(head[key] == result[key] == checked[key], "accepted_head_result_checker:" + key)
    require(head["kind"] == "Separator" and result["terminal"] == checked["terminal"] and
            result["terminal"] in ("UNKNOWN_CAP", "UNKNOWN_RESOURCE", "COMPLETE_ZERO_CANDIDATE") and
            result["head_sha256"] == checked["head_sha256"] == continuation.by_name["output/HEAD"]["sha256"] and
            checked["result_sha256"] == continuation.by_name["output/result.json"]["sha256"] and
            checked["prefix_steps_replayed"] == checked["physical_appends"] == count and
            type(checked["external_e_attached"]) is int and checked["external_e_attached"] == 1 and
            checked["all_new_committed_arrays_and_json_compared"] is True and
            checked["current_checkpoint_fully_compared"] is True and checked["full_four_character_scope"] is True and
            checked["section_equalities_each"] == 8059 and checked["chords_each"] == CHORDS and
            checked["auxiliary_tests_each"] == 2 and checked["source_lower_trits_each_E"] == LOWER and
            checked["literal_modulus"] == 54 and checked["all_four_B_summed_each_E"] is True and
            checked["ordinary27_actual_source"] is True, "accepted_full_old_prefix_gate")
    for name in ("owner", "source", "start"):
        require(head[name + "_sha256"] == continuation.by_name["output/" + name + ".json"]["sha256"],
                "accepted_root_receipt_join")
    require(head["fixed_manifest_sha256"] == continuation.by_name["output/fixed/manifest.json"]["sha256"] and
            len(checked["steps"]) == count and len(checked["snapshots"]) == count + (head["current_snapshot_sha256"] is not None),
            "accepted_complete_old_receipt_counts")
    # Each immutable upstream entry still has its previously accepted identity.
    pin_groups = (("state", L.ROOTS.STATE_FILES), ("delta", L.ROOTS.DELTA_FILES),
                  ("seed34", C.FIXED.SEED34_FILES), ("packet", REFINE.PACKET_FILES),
                  ("refinement", O.REFINEMENT_FILES), ("oracle", E.ORACLE_FILES), ("e", C.E_FILES))
    for role, pins in pin_groups:
        for name, identity in pins.items():
            trees[role].expected(name, identity)
    facts = C.FIXED.validate_parent_generations(*(trees[role].json("output/result.json") for role in ("state", "delta", "seed34")))
    pivots = base_pivot_metadata(trees["state"])
    rows = [SavedPhysicalRow(trees["state"], "state/physical.bin", number * ROW_BYTES, None) for number in range(1354)]
    base_target = facts["base"]["target_reduction"]
    require(base_target == trees["state"].json("output/terminal.json")["target_reduction"], "accepted_base_named_target")
    named = [{"role": "base", "manifest_sha256": trees["state"].by_name["state/manifest.json"]["sha256"],
        "result_sha256": trees["state"].by_name["output/result.json"]["sha256"],
        "target_sha256": sha(canonical(base_target)), "state_head": L.OLD_HEAD}]
    previous_head, previous_target, generation = L.OLD_HEAD, base_target["remainder_sha256"], 8059

    def append_saved(role: str, prefix: str, manifest_name: str, named_role: str, is_loop: bool = False) -> dict[str, Any]:
        nonlocal previous_head, previous_target, generation
        tree = trees[role]
        instruction = tree.json(prefix + "/instruction.json", True)
        saved = tree.json(prefix + "/result.json", True)
        manifest = tree.json(manifest_name, True)
        check_document(saved)
        check_document(manifest)
        if not is_loop:
            saved_manifest_members(tree, prefix, manifest)
        normalized_name, target_name = prefix + "/physical-normalized.bin", prefix + "/target-remainder.bin"
        normalized_pin, target_pin = tree.by_name[normalized_name], tree.by_name[target_name]
        require(normalized_pin["bytes"] == target_pin["bytes"] == ROW_BYTES, "accepted_saved_row_and_target_width")
        rank = len(rows)
        unsigned_instruction = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
        require(instruction["predecessor"] == previous_head and instruction["offer"] == generation and
                instruction["generation"] == generation + 1 and instruction["rank"] == rank + 1 and
                instruction["physical_offset"] == rank * ROW_BYTES and instruction["rolling_sha256"] ==
                sha(bytes.fromhex(previous_head) + canonical(unsigned_instruction)), "accepted_saved_instruction_ancestry")
        target, pivot = saved["target"], saved["pivot"]
        target_parent_key = "old_remainder_sha256" if role in ("delta", "seed34") else "parent_remainder_sha256"
        require(target[target_parent_key] == previous_target and target["remainder_sha256"] == target_pin["sha256"] and
                pivot["normalized_sha256"] == normalized_pin["sha256"] and pivot["lead"] == instruction["lead"],
                "accepted_saved_target_and_normalized_identity")
        if role not in ("delta", "seed34"):
            require(instruction["physical_sha256"] == normalized_pin["sha256"] and
                    instruction["target_scalar"] == target["scalar"] and
                    instruction["target_remainder_sha256"] == target_pin["sha256"], "accepted_saved_payload_instruction_join")
        if role in ("e", "continuation"):
            require(saved["instruction_sha256"] == tree.by_name[prefix + "/instruction.json"]["sha256"],
                    "accepted_E_result_instruction_hash")
        integer(instruction["lead"], "accepted_saved_lead", 0, PHYSICAL - 1)
        pivots.append({"offer": instruction["offer"], "lead": instruction["lead"],
            "physical_offset": rank * ROW_BYTES, "coefficient_offset": None, "rolling_sha256": instruction["rolling_sha256"]})
        rows.append(SavedPhysicalRow(tree, normalized_name, 0, normalized_pin["sha256"]))
        parent = {"role": named_role, "manifest_sha256": tree.by_name[manifest_name]["sha256"],
            "result_sha256": tree.by_name[prefix + "/result.json"]["sha256"],
            "target_sha256": sha(canonical(target)), "state_head": instruction["rolling_sha256"]}
        if role in ("e", "continuation"):
            derivation = saved["target_derivation"]
            require(derivation["mode"] == "derived" and derivation["original_rho2_directly_read"] is False and
                    derivation["original_rho2_packed_sha256"] == base_target["rho2_sha256"] and
                    derivation["accepted_target_derivation_parents"] == named and
                    derivation["new_delta"] == {"instruction_sha256": tree.by_name[prefix + "/instruction.json"]["sha256"],
                        "state_head": instruction["rolling_sha256"], "normalized_sha256": normalized_pin["sha256"],
                        "target_sha256": sha(canonical(target))}, "accepted_named_E_target_identity")
            parent["instruction_sha256"] = tree.by_name[prefix + "/instruction.json"]["sha256"]
        named.append(parent)
        previous_head, previous_target, generation = instruction["rolling_sha256"], target_pin["sha256"], generation + 1
        return {"instruction": instruction, "result": saved, "manifest": manifest,
                "manifest_sha256": tree.by_name[manifest_name]["sha256"], "prefix": prefix}

    append_saved("delta", "output", "output/manifest.json", "seed30")
    append_saved("seed34", "output", "output/manifest.json", "seed34")
    for number in range(1, 4):
        prefix = f"output/steps/{number:06d}"
        append_saved("packet", prefix, prefix + "/manifest.json", f"packet-step-{number}")
    for number in range(1, 27):
        prefix = f"output/steps/{number:06d}"
        append_saved("refinement", prefix, prefix + "/manifest.json", f"refinement-step-{number}")
    append_saved("e", "output", "output/manifest.json", "external-e")
    require(len(rows) == start["rank"] == 1386 and generation == start["generation"] == 8091 and
            previous_head == start["state_head"] and previous_target == start["target_remainder_sha256"] and
            start["accepted_target_derivation_parents"] == named and start["completed_steps"] == 0 and
            type(start["external_e_attached"]) is int and start["external_e_attached"] == 1,
            "accepted_external_E_is_start_once")
    selection_previous = trees["e"].read("output/target-remainder.bin", ROW_BYTES)
    require(sha(selection_previous) == start["target_remainder_sha256"], "selection_previous_is_accepted_continuation_start")
    previous_step = None
    for number in range(1, count + 1):
        snapshot_prefix = f"output/snapshots/{number - 1:06d}"
        snapshot = continuation.json(snapshot_prefix + "/start.json", True)
        check_document(snapshot)
        require(snapshot["step"] == number - 1 and snapshot["rank"] == len(rows) and snapshot["generation"] == generation and
                snapshot["state_head"] == previous_head and snapshot["target_remainder_sha256"] == previous_target and
                snapshot["accepted_target_derivation_parents"] == named, "accepted_each_old_snapshot_metadata")
        saved = append_saved("continuation", snapshot_prefix + "/e/physical", f"output/steps/{number:06d}/manifest.json",
                             f"loop-e-{number:06d}", True)
        manifest = saved["manifest"]
        require(manifest["step"] == number and manifest["predecessor_step_manifest_sha256"] == previous_step and
                manifest["snapshot_sha256"] == continuation.by_name[snapshot_prefix + "/start.json"]["sha256"] and
                manifest["state_head"] == previous_head and manifest["rank"] == len(rows) and
                manifest["generation"] == generation and manifest["phase_eof"] == list(C.PHASES), "accepted_old_step_metadata")
        for phase in C.PHASES:
            phase_prefix = snapshot_prefix + ("/" if phase in C.PHASES[:3] else "/e/") + phase
            phase_manifest = continuation.json(phase_prefix + "/manifest.json", True)
            require(continuation.by_name[phase_prefix + "/manifest.json"]["sha256"] == manifest["phase_manifests"][phase],
                    "accepted_all_old_phase_manifest_hashes")
            saved_manifest_members(continuation, phase_prefix, phase_manifest)
        # Reuse only the frozen checker's serialization contract for this saved
        # step receipt; no arithmetic is called by the comparison below.
        old_checked = checked["steps"][number - 1]
        require(old_checked["step"] == number and old_checked["manifest_sha256"] == saved["manifest_sha256"],
                "accepted_old_checker_step_manifest")
        old_snapshot = checked["snapshots"][number - 1]
        require(old_snapshot["step"] == number - 1 and old_snapshot["snapshot_sha256"] == manifest["snapshot_sha256"] and
                old_snapshot["phase_manifests"] == manifest["phase_manifests"] and
                old_snapshot["oracle_manifest_sha256"] == manifest["oracle_manifest_sha256"],
                "accepted_old_checker_snapshot_all_phase_join")
        previous_step = saved["manifest_sha256"]
        if number % 8 == 0:
            boundary("accepted_old_prefix_metadata", steps=number, total=count)
    require(previous_step == head["last_step_manifest_sha256"] and previous_head == head["state_head"] and
            previous_target == head["target_remainder_sha256"] and generation == head["generation"] and
            len(rows) == head["rank"] == 1386 + count and generation == 8091 + count and
            result["lambda_rho2"] == checked["lambda_rho2"] and result["lambda_rho2"]["mode"] == "derived" and
            result["lambda_rho2"]["value"] == 1 and result["lambda_rho2"]["original_rho2_directly_read"] is False and
            result["lambda_rho2"]["original_rho2_packed_sha256"] == base_target["rho2_sha256"] and
            result["lambda_rho2"]["accepted_target_derivation_parents"] == named, "accepted_final_named_target_chain")
    invocations = C.check_invocations(old_root, start, owner, source, head["fixed_manifest_sha256"], result)
    require(invocations == checked["invocations"], "accepted_all_saved_invocation_values")
    prefix = f"output/snapshots/{count - 1:06d}/e/physical"
    anchor = ThinAnchor(pivots, rows, head, continuation.read(prefix + "/target-remainder.bin", ROW_BYTES),
                        selection_previous, continuation.read(prefix + "/lambda.bin", ROW_BYTES), named)
    return anchor, {**objects, "checker": checked, "invocations": invocations,
                    "parent_layout": C.FIXED.parent_layout_receipt(facts)}


class CandidateFiles:
    """Read-only candidate bytes and the exact files already independently read."""

    def __init__(self, root: Path):
        self.root = root
        self.files, self.directories = tree_names(root)
        self.expected: dict[str, dict[str, Any]] = {}
        self.before = {name: hash_file(file_path(root, name), "candidate/" + name) for name in self.files}

    def read(self, name: str, cap: int = 64 << 20) -> bytes:
        require(name in self.before and self.before[name][0] <= cap, "bounded_existing_candidate_file")
        raw = file_path(self.root, name).read_bytes()
        require((len(raw), sha(raw)) == self.before[name], "candidate_file_unchanged_when_read")
        return raw

    def json(self, name: str, suffix: str | None = None) -> dict[str, Any]:
        value = json_value(self.read(name), "candidate/" + name, True)
        require(type(value) is dict, "candidate_json_object")
        if suffix is not None:
            check_document(value, suffix)
        return value

    def compare(self, name: str, raw: bytes) -> dict[str, Any]:
        require(name in self.before and self.before[name] == (len(raw), sha(raw)), "candidate_expected_size_hash:" + name)
        with file_path(self.root, name).open("rb") as stream:
            require(stream.read(len(raw) + 1) == raw, "candidate_complete_actual_bytes_EOF:" + name)
        result = receipt(name, raw)
        if name in self.expected:
            same_json(result, self.expected[name], "same_file_has_one_independent_expected_value")
        self.expected[name] = result
        return result

    def object(self, name: str, value: Any) -> dict[str, Any]:
        return self.compare(name, canonical(value))

    def unchanged(self) -> None:
        require(tree_names(self.root) == (self.files, self.directories), "all_candidate_files_and_directories_unchanged")
        for name, identity in self.before.items():
            require(hash_file(file_path(self.root, name), "candidate-after/" + name) == identity, "candidate_full_output_unchanged")


def binary_descriptor(name: str, item: tuple[bytes, str, Any]) -> dict[str, Any]:
    raw, dtype, shape = item
    result = receipt(name, raw)
    if dtype == "json":
        require(shape is None, "json_payload_has_no_array_shape")
    else:
        require(dtype in ("packed3", "u8", "u32le") and type(shape) in (tuple, list), "registered_binary_payload_type")
        result.update({"dtype": dtype, "shape": list(shape)})
    return result


def payload_roster(payloads: dict[str, tuple[bytes, str, Any]]) -> list[dict[str, Any]]:
    return [binary_descriptor(name, item) for name, item in sorted(payloads.items())]


def finite_measurement(value: Any, label: str) -> None:
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0, label)


def telemetry_record(files: CandidateFiles, prefix: str, phase: str, payload_bytes: int) -> tuple[dict[str, Any], bytes]:
    raw = files.read(prefix + "/telemetry.json", 1 << 20)
    value = json_value(raw, "phase_telemetry", True)
    check_document(value, "phase-telemetry")
    require(set(value) == {"schema", "sha256", "phase", "elapsed_seconds", "process_ru_maxrss_kib", "proc_io_before",
            "proc_io_after", "payload_bytes", "measurement_scope", "eof"} and value["phase"] == phase and
            value["payload_bytes"] == payload_bytes and type(value["payload_bytes"]) is int and value["eof"] is True and
            value["measurement_scope"] == "process-cumulative-rusage-and-proc-io;payload-bytes-are-output-only",
            "phase_telemetry_exact_type_and_payload_bytes")
    finite_measurement(value["elapsed_seconds"], "phase_elapsed_finite_nonnegative")
    integer(value["process_ru_maxrss_kib"], "process_cumulative_peak_kib")
    for key in ("proc_io_before", "proc_io_after"):
        item = value[key]
        require(item is None or type(item) is dict and set(item) == {"rchar", "wchar", "read_bytes", "write_bytes"}, "proc_io_exact_type")
        if item is not None:
            for count in item.values():
                integer(count, "proc_io_ordinary_counter")
    if value["proc_io_before"] is not None and value["proc_io_after"] is not None:
        require(all(value["proc_io_after"][key] >= before for key, before in value["proc_io_before"].items()),
                "proc_io_cumulative_monotonic")
    return value, raw


@dataclass
class RootRecords:
    parent_layout: dict[str, Any]
    source: dict[str, Any]
    owner: dict[str, Any]
    start: dict[str, Any]
    fixed: dict[str, Any]
    selection_start: dict[str, Any]

    def binding(self) -> dict[str, str]:
        return {"owner_sha256": sha(canonical(self.owner)), "source_sha256": sha(canonical(self.source)),
            "start_sha256": sha(canonical(self.start)), "fixed_manifest_sha256": sha(canonical(self.fixed)),
            "selection_start_sha256": sha(canonical(self.selection_start))}


def root_records(inputs: AcceptedInputs, anchor: ThinAnchor, old: dict[str, Any], bundle: C.FixedBundle) -> RootRecords:
    acceptance = inputs.value
    layout = document("parent-layout", {"portable_acceptance_sha256": inputs.portable_sha256,
        **{key: copy.deepcopy(inputs.portable[key]) for key in ("parents", "anchor", "code", "runtime", "registration")}})
    code = acceptance["code"]
    source = document("source", {"producer": code["producer"], "retained_producer_dependencies": code["producer_dependencies"],
        "checker": code["checker"], "retained_checker_dependencies": code["checker_dependencies"], "data": code["data"],
        "runtime": acceptance["runtime"], "formula_id": FORMULA, "retained_TCB_independence_reproved": False})
    owner = document("owner", {"formula_id": FORMULA, "scope": SCOPE, "parent_layout_sha256": sha(canonical(layout)),
        "source_sha256": sha(canonical(source)), "portable_acceptance_sha256": inputs.portable_sha256,
        "registration": acceptance["registration"]})
    pairing = anchor.measure_selection()
    start = document("start", {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)),
        "parent_layout_sha256": sha(canonical(layout)), "anchor_head_sha256": acceptance["anchor"]["head"]["sha256"],
        "anchor_result_sha256": acceptance["anchor"]["result"]["sha256"],
        "anchor_checker_sha256": acceptance["anchor"]["checker"]["sha256"], "anchor_completed_steps": anchor.completed_steps,
        "rank": anchor.rank, "generation": anchor.generation, "kind": "Separator", "state_head": anchor.head,
        "target_remainder_sha256": sha(pack(anchor.target)), "previous_target_remainder_sha256": sha(pack(anchor.previous_target)),
        "selection_lambda_sha256": sha(pack(anchor.functional)), "original_rho2_packed_sha256": RHO2_SHA,
        "accepted_target_derivation_parents": copy.deepcopy(anchor.parents), "anchor_pairing": pairing,
        "anchor_pairing_rows": anchor.rank, "old_snapshot_numeric_replays": 0, "old_insert_numeric_replays": 0,
        "external_e_attached": 1, "registration": acceptance["registration"]})
    old_fixed = inputs.trees["continuation"].json("output/fixed/manifest.json", True)
    geometry_sha = inputs.trees["oracle"].by_name["output/geometry/manifest.json"]["sha256"]
    fixed_sha, rebuilt_old_fixed = C.check_fixed(inputs.trees["continuation"].root / "output", bundle,
        {"stage_hashes": {"geometry": geometry_sha}}, sha(canonical(old["owner.json"])), sha(canonical(old["source.json"])))
    same_json(old_fixed, rebuilt_old_fixed, "all_accepted_lambda_independent_fixed_values")
    require(fixed_sha == acceptance["anchor"]["fixed"]["sha256"], "accepted_fixed_complete_hash")
    projected = []
    for item in old_fixed["files"]:
        require(set(item) == {"file", "bytes", "sha256", "dtype", "shape"}, "retained_fixed_five_key_descriptor")
        if item["dtype"] == "json":
            require(item["shape"] is None, "retained_fixed_JSON_shape_null")
            projected.append({key: item[key] for key in ("file", "bytes", "sha256")})
        else:
            projected.append(copy.deepcopy(item))
    fixed = document("fixed-manifest", {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)),
        "start_sha256": sha(canonical(start)), "accepted_fixed_manifest": acceptance["anchor"]["fixed"],
        "accepted_geometry_stage_sha256": geometry_sha, "files": projected, "fixed_values_independent_of_lambda": True})
    selection_start = document("selection-start", {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)),
        "start_sha256": sha(canonical(start)), "fixed_manifest_sha256": sha(canonical(fixed)),
        "anchor_completed_steps": anchor.completed_steps, "rank": anchor.rank, "generation": anchor.generation,
        "state_head": anchor.head, "target_remainder_sha256": sha(pack(anchor.target)),
        "previous_target_remainder_sha256": sha(pack(anchor.previous_target)), "selection_lambda_sha256": sha(pack(anchor.functional)),
        "selection_policy": POLICY, "batch_size": BATCH_SIZE, "max_batches": 1})
    return RootRecords(layout, source, owner, start, fixed, selection_start)


def compare_root_records(files: CandidateFiles, records: RootRecords) -> None:
    for name, value in (("parent-layout.json", records.parent_layout), ("source.json", records.source),
                        ("owner.json", records.owner), ("start.json", records.start), ("fixed/manifest.json", records.fixed),
                        ("selection/start.json", records.selection_start)):
        files.object(name, value)


def compare_phase(files: CandidateFiles, prefix: str, phase: str, payloads: dict[str, tuple[bytes, str, Any]],
                  records: RootRecords, previous: str | None, selection_sha: str | None = None,
                  ordinal: int | None = None, witness_sha: str | None = None) -> tuple[str, dict[str, Any]]:
    telemetry, raw = telemetry_record(files, prefix, phase, sum(len(item[0]) for item in payloads.values()))
    complete = {**payloads, "telemetry.json": (raw, "json", None)}
    manifest = document("phase-manifest", {**records.binding(), "selection_sha256": selection_sha,
        "candidate_ordinal": ordinal, "witness_sha256": witness_sha, "phase": phase,
        "previous_phase_manifest_sha256": previous, "files": payload_roster(complete), "eof": True})
    for name, item in complete.items():
        files.compare(prefix + "/" + name, item[0])
    result = files.object(prefix + "/manifest.json", manifest)
    boundary("new_phase_fully_compared", phase_name=phase, ordinal=ordinal, files=len(complete))
    return result["sha256"], telemetry


def witness_records(plan: dict[str, Any], records: RootRecords) -> list[dict[str, Any]]:
    common = {key: value for key, value in records.binding().items() if key != "fixed_manifest_sha256"}
    result = []
    for selected in plan["candidates"]:
        witness = selected["witness"]
        chord = witness["kind"] == "chord"
        result.append(document("witness", {**common, "ordinal": selected["ordinal"], "selection_policy": POLICY,
            "kind": witness["kind"], "roster_index": selected["roster_index"],
            "edge": witness["failed_chord"] if chord else None, "coordinate": None if chord else witness["coordinate"],
            "failed_chord": witness["failed_chord"] if chord else None,
            "basis_chords": witness["basis_chords"] if chord else [],
            "basis_coefficients": witness["basis_coefficients"] if chord else [], "cycles": witness["cycles"],
            "eta": witness["eta"], "tau": witness["tau"], "scalar": witness["scalar"],
            "materialization": "MATERIALIZATION_PENDING"}))
    require(len(result) <= BATCH_SIZE and len({sha(canonical(item)) for item in result}) == len(result),
            "each_candidate_has_its_own_witness_identity")
    return result


def batch_tree_payloads(selection: SelectionArithmetic, bundle: C.FixedBundle,
                        records: RootRecords, witnesses: list[dict[str, Any]]) -> dict[str, tuple[bytes, str, Any]]:
    tree, plan = selection.tree, selection.plan
    result = {"potential-f.u8": O.typed_array(tree["potential_f"], "u8", (VERTICES,)),
        "potential-tau.u8": O.typed_array(tree["potential_tau"], "u8", (VERTICES, 5)),
        "chord-values.u8": O.typed_array(tree["chord_values"], "u8", (CHORDS,)),
        "chord-tau.u8": O.typed_array(tree["tau"], "u8", (CHORDS, 5)),
        "chord-residuals.u8": O.typed_array(tree["residuals"], "u8", (CHORDS,)),
        "selected-chords.u32": O.typed_array(tree["selected_edges"], "u32le", (5,)),
        "fit.u8": O.typed_array(plan["fit"], "u8", (5,)),
        "basis-tau.u8": O.typed_array(tree["tau"][bundle.selected], "u8", (5, 5)),
        "failed-indices.u32": O.typed_array(plan["failed_indices"], "u32le", (len(plan["failed_indices"]),)),
        "failed-edges.u32": O.typed_array(plan["failed_edges"], "u32le", (len(plan["failed_edges"]),))}
    metadata = document("tree", {"vertices": VERTICES, "tree_edges": VERTICES - 1, "chords": CHORDS,
        "independent_tau_columns": 5, "basis_chords": tree["selected_edges"].tolist(), "fit": plan["fit"].tolist(),
        "aux_values": selection.b_aux.tolist(), "first_failed_index": plan["first_failed_index"],
        "first_failed_edge": plan["first_failed_edge"], "residual_nonzero": len(plan["failed_indices"]),
        "full_chord_eof": True, "selection_policy": POLICY})
    roster = document("witness-roster", {**{key: value for key, value in records.binding().items()
                                           if key != "fixed_manifest_sha256"}, "witnesses": witnesses, "eof": True})
    result.update({"tree.json": O.json_payload(metadata), "witness-roster.json": O.json_payload(roster)})
    return result


@dataclass
class SelectionReplay:
    phases: dict[str, str]
    telemetry: dict[str, dict[str, Any]]
    arithmetic: SelectionArithmetic | None
    witnesses: list[dict[str, Any]]
    record: dict[str, Any] | None
    views: list[dict[str, Any]]
    metadata_complete: bool

    @property
    def sha256(self) -> str | None:
        return sha(canonical(self.record)) if self.record is not None and self.metadata_complete else None


def selection_record(selection: SelectionArithmetic, bundle: C.FixedBundle, records: RootRecords,
                     phase_hashes: dict[str, str], witnesses: list[dict[str, Any]]) -> dict[str, Any]:
    plan = selection.plan
    payloads = batch_tree_payloads(selection, bundle, records, witnesses)
    return document("selection", {**records.binding(), "phase_manifests": phase_hashes,
        "selection_policy": POLICY, "batch_size": BATCH_SIZE, "max_batches": 1, "refill": False,
        "chords_checked": CHORDS, "auxiliary_tests": 2, "failed_count": len(plan["failed_indices"]),
        "first_failed_index": plan["first_failed_index"], "first_failed_edge": plan["first_failed_edge"],
        "failed_indices": binary_descriptor("failed-indices.u32", payloads["failed-indices.u32"]),
        "failed_edges": binary_descriptor("failed-edges.u32", payloads["failed-edges.u32"]),
        "selected_count": len(witnesses), "selected": [{"ordinal": item["ordinal"], "kind": item["kind"],
            "roster_index": item["roster_index"], "edge": item["edge"], "coordinate": item["coordinate"],
            "scalar": item["scalar"], "witness": receipt(f"candidates/{item['ordinal']:06d}/witness.json", canonical(item))}
            for item in witnesses], "aux_values": selection.b_aux.tolist(),
        "basis_chords": selection.tree["selected_edges"].tolist(), "basis_tau": selection.tree["tau"][bundle.selected].tolist(),
        "fit": plan["fit"].tolist(), "terminal": "COMPLETE_ZERO_CANDIDATE" if not witnesses else "VIOLATION_CANDIDATE", "eof": True})


def oracle_view_record(records: RootRecords, selected: dict[str, Any], witness: dict[str, Any]) -> dict[str, Any]:
    return document("oracle-view", {**records.binding(), "selection_sha256": sha(canonical(selected)),
        "ordinal": witness["ordinal"], "witness_sha256": sha(canonical(witness)),
        "geometry_manifest_sha256": records.binding()["fixed_manifest_sha256"],
        "phase_manifests": selected["phase_manifests"], "anchor_state_head": records.start["state_head"],
        "selection_lambda_sha256": records.start["selection_lambda_sha256"], "terminal": "VIOLATION_CANDIDATE"})


def compare_selection_publication(files: CandidateFiles, records: RootRecords, selected: dict[str, Any],
                                  witnesses: list[dict[str, Any]], required: bool) -> tuple[list[dict[str, Any]], bool]:
    witness_present = []
    for witness in witnesses:
        name = f"candidates/{witness['ordinal']:06d}/witness.json"
        present = name in files.before
        witness_present.append(present)
        require(present or not required, "all_selected_witness_shells_published")
        if present:
            files.object(name, witness)
    require(witness_present == sorted(witness_present, reverse=True), "witness_copy_publication_prefix")
    selection_present = "selection/selection.json" in files.before
    require(not selection_present or all(witness_present), "selection_after_all_witness_copies")
    require(selection_present or not required, "completed_selection_metadata_present")
    if selection_present:
        files.object("selection/selection.json", selected)
    views, view_present = [], []
    for witness in witnesses:
        view = oracle_view_record(records, selected, witness)
        views.append(view)
        name = f"candidates/{witness['ordinal']:06d}/oracle-view.json"
        present = name in files.before
        view_present.append(present)
        require(not present or selection_present, "oracle_views_after_completed_selection")
        require(present or not required, "all_selected_oracle_views_published")
        if present:
            files.object(name, view)
    require(view_present == sorted(view_present, reverse=True), "oracle_view_publication_prefix")
    return views, selection_present and all(witness_present) and all(view_present)


def replay_selection(files: CandidateFiles, records: RootRecords, bundle: C.FixedBundle, anchor: ThinAnchor,
                     phase_count: int, metadata_required: bool,
                     after_phase: Callable[[int, dict[str, str], str | None, bool], None]) -> SelectionReplay:
    integer(phase_count, "selection_phase_prefix", 0, 3)
    hashes: dict[str, str] = {}
    telemetry: dict[str, dict[str, Any]] = {}
    result = SelectionReplay(hashes, telemetry, None, [], None, [], False)
    if phase_count == 0:
        return result
    section = bundle.section(anchor.functional)
    hashes["section"], telemetry["section"] = compare_phase(files, "selection/section", "section", O.section_payloads(section), records, None)
    CHECKED_CURSOR["last_complete_phase"] = "selection/section"
    after_phase(1, hashes, None, True)
    if phase_count == 1:
        return result
    score, ordinary = O.source_scores(bundle.geometry, section["roots"], section["kappa"])
    f, b_aux, _ = O.raw_edge_cochain(bundle.geometry, score, section["kappa"])
    hashes["cochain"], telemetry["cochain"] = compare_phase(files, "selection/cochain", "cochain", O.cochain_payloads(score, f, b_aux), records, hashes["section"])
    CHECKED_CURSOR["last_complete_phase"] = "selection/cochain"
    after_phase(2, hashes, None, True)
    if phase_count == 2:
        return result
    tree = C.current_tree(bundle, f, b_aux)
    plan = select_all_residuals(bundle.geometry.chords, tree["tau"], tree["chord_values"], bundle.selected,
                                bundle.inverse, tree["residuals"], b_aux)
    require(np.array_equal(plan["fit"], tree["fit"]), "same_fixed_lambda_fit")
    arithmetic = SelectionArithmetic(section, score, f, b_aux, tree, plan, ordinary)
    witnesses = witness_records(plan, records)
    payloads = batch_tree_payloads(arithmetic, bundle, records, witnesses)
    hashes["tree"], telemetry["tree"] = compare_phase(files, "selection/tree", "tree", payloads, records, hashes["cochain"])
    CHECKED_CURSOR["last_complete_phase"] = "selection/tree"
    selected = selection_record(arithmetic, bundle, records, hashes, witnesses)
    views, complete = compare_selection_publication(files, records, selected, witnesses, metadata_required)
    after_phase(3, hashes, sha(canonical(selected)) if complete else None, complete)
    CHECKED_CURSOR["selection_compared"] = complete
    return SelectionReplay(hashes, telemetry, arithmetic, witnesses, selected, views, complete)


def row_source(state: BatchReductionState, index: int) -> dict[str, Any]:
    raw = state.row(index)
    if index < state.anchor_rank:
        saved = state.anchor.rows[index]
        original = saved.tree.by_name[saved.file]
        require(saved.offset >= 0 and saved.offset + ROW_BYTES <= original["bytes"], "parent_row_exact_source_range")
        return {"kind": "parent-row", "role": saved.tree.role, "file": saved.file,
            "file_bytes": original["bytes"], "file_sha256": original["sha256"], "offset": saved.offset,
            "length": ROW_BYTES, "row_sha256": sha(raw)}
    local = index - state.anchor_rank
    require(local < len(state.row_manifests), "only_prior_accepted_batch_row_reference")
    return {"kind": "batch-row", "local_row_offset": local, "file": f"rows/{local:06d}/physical-normalized.bin",
            "bytes": ROW_BYTES, "sha256": sha(raw), "row_manifest_sha256": state.row_manifests[local]}


def reduction_payloads(state: BatchReductionState, decision: DecisionArithmetic, ordinal: int,
                       selection_sha: str, witness_sha: str, correction_sha: str,
                       roots_sha: str) -> tuple[dict[str, tuple[bytes, str, Any]], dict[str, Any]]:
    coefficients = complete_reduction_coefficients(state, decision)
    ordered = [{"row_id": index, "source": row_source(state, index), "lead": pivot["lead"], "coefficient": int(coefficients[index])}
               for index, pivot in enumerate(state.pivots)]
    signs = literal_signs(coefficients, decision.sigma, decision.target_scalar)
    literal = document("physical-literal", {"candidate_ordinal": ordinal, "selection_sha256": selection_sha,
        "witness_sha256": witness_sha, "source_correction_sha256": correction_sha, "p1_roots_sha256": roots_sha,
        "physical_factors": [{"row_id": row["row_id"], "source": row["source"], "coefficient": row["coefficient"],
            "exponent": exponent} for row, exponent in zip(ordered, signs["physical_factor_exponents"])],
        "outer_exponent": signs["normalized_outer_exponent"], "physical_lower_zero": True,
        "source_lower_zero": "NOT_ASSERTED", "normalized_word_available": not decision.dependent})
    target = None if decision.dependent else {"parent_remainder_sha256": sha(pack(decision.target_before)),
        "remainder_sha256": sha(pack(decision.target_after)), "scalar": decision.target_scalar}
    instruction = None
    if not decision.dependent:
        body = {"predecessor": state.physical_head, "offer": state.generation, "global_row_id": state.rank,
            "rank": state.rank + 1, "generation": state.generation + 1, "lead": decision.lead, "sigma": decision.sigma,
            "physical_offset": state.rank * ROW_BYTES, "local_row_offset": len(state.rows), "candidate_ordinal": ordinal,
            "selection_sha256": selection_sha, "witness_sha256": witness_sha,
            "physical_sha256": sha(pack(decision.normalized)), "literal_sha256": sha(canonical(literal)),
            "target_sha256": sha(canonical(target)), "target_scalar": decision.target_scalar,
            "coefficients_sha256": sha(coefficients.tobytes())}
        # The new rolling body deliberately excludes schema and the outer seal.
        body["rolling_sha256"] = sha(bytes.fromhex(state.physical_head) + canonical(body))
        instruction = document("physical-instruction", body)
    contribution = sum(int(coefficients[index]) * dot(state.selection_lambda, unpack(state.row(index), PHYSICAL))
                       for index in range(state.anchor_rank, state.rank)) % 3
    require((decision.selected_scalar - contribution) % 3 == decision.remainder_scalar,
            "reduction_selection_functional_including_new_basis")
    record = document("reduction", {"candidate_ordinal": ordinal, "selection_sha256": selection_sha,
        "witness_sha256": witness_sha, "selection_scalar": decision.selected_scalar,
        "raw_pairing": dot(state.selection_lambda, decision.raw), "remainder_pairing": decision.remainder_scalar,
        "subtracted_new_pairing": contribution, "rank_before": state.rank, "generation_before": state.generation,
        "parent_state_head": state.physical_head, "target_before_sha256": sha(pack(decision.target_before)),
        "coefficients_sha256": sha(coefficients.tobytes()), "ordered_reductions": ordered,
        "remainder_sha256": sha(pack(decision.remainder)), "remainder_zero": decision.dependent,
        "outcome": "DEPENDENT" if decision.dependent else "INDEPENDENT", "lead": decision.lead, "sigma": decision.sigma,
        "normalized_sha256": None if decision.dependent else sha(pack(decision.normalized)),
        "target_scalar": decision.target_scalar, "target_after_sha256": sha(pack(decision.target_after)),
        "rank_after": state.rank + (not decision.dependent), "generation_after": state.generation + (not decision.dependent),
        "state_head": state.physical_head if instruction is None else instruction["rolling_sha256"],
        "new_row_offset": None if decision.dependent else len(state.rows)})
    payloads = {"coefficients.u8": O.typed_array(coefficients, "u8", (state.rank,)),
        "physical-remainder.bin": O.typed_array(decision.remainder, "packed3", (PHYSICAL,)),
        "target-before.bin": O.typed_array(decision.target_before, "packed3", (PHYSICAL,)),
        "target-remainder.bin": O.typed_array(decision.target_after, "packed3", (PHYSICAL,)),
        "physical-literal.json": O.json_payload(literal), "reduction.json": O.json_payload(record)}
    if instruction is not None:
        payloads.update({"physical-normalized.bin": O.typed_array(decision.normalized, "packed3", (PHYSICAL,)),
            "instruction.json": O.json_payload(instruction), "target.json": O.json_payload(target)})
    return payloads, {"reduction": record, "literal": literal, "target": target, "instruction": instruction}


def accepted_row_record(records: RootRecords, state: BatchReductionState, decision: DecisionArithmetic, ordinal: int,
                        selection_sha: str, reduction_sha: str, payloads: dict[str, tuple[bytes, str, Any]],
                        objects: dict[str, Any]) -> dict[str, Any]:
    require(not decision.dependent and objects["instruction"] is not None, "accepted_row_requires_independent_remainder")
    instruction = objects["instruction"]
    row_payloads = {name: payloads[name] for name in ("physical-normalized.bin", "instruction.json", "target.json")}
    return document("row-manifest", {**{key: value for key, value in records.binding().items() if key != "fixed_manifest_sha256"},
        "selection_sha256": selection_sha, "local_row_offset": len(state.rows), "global_row_id": state.rank,
        "candidate_ordinal": ordinal, "predecessor_row_manifest_sha256": state.row_manifests[-1] if state.row_manifests else None,
        "reduction_manifest_sha256": reduction_sha, "files": payload_roster(row_payloads),
        "state_head": instruction["rolling_sha256"], "rank": state.rank + 1, "generation": state.generation + 1,
        "target_literal_factor": {"row_id": state.rank, "local_row_offset": len(state.rows), "coefficient": decision.target_scalar,
            "exponent": E.signed(decision.target_scalar), "normalized_literal_sha256": sha(canonical(objects["literal"]))}, "eof": True})


def candidate_decision_record(records: RootRecords, state: BatchReductionState, ordinal: int, selection_sha: str,
                              witness_sha: str, view_sha: str, phases: dict[str, str], objects: dict[str, Any],
                              row_sha: str | None) -> dict[str, Any]:
    reduction = objects["reduction"]
    return document("candidate-manifest", {**{key: value for key, value in records.binding().items() if key != "fixed_manifest_sha256"},
        "selection_sha256": selection_sha, "ordinal": ordinal, "witness_sha256": witness_sha,
        "oracle_view_sha256": view_sha, "phase_manifests": phases,
        "predecessor_candidate_manifest_sha256": sha(canonical(state.decisions[-1])) if state.decisions else None,
        "outcome": reduction["outcome"], "row_manifest_sha256": row_sha, "accepted_new_rows_before": len(state.rows),
        "accepted_new_rows_after": len(state.rows) + (row_sha is not None),
        **{key: reduction[key] for key in ("rank_before", "rank_after", "generation_before", "generation_after",
                                         "parent_state_head", "state_head")},
        "target_before_sha256": reduction["target_before_sha256"], "target_after_sha256": reduction["target_after_sha256"], "eof": True})


def batch_target_parent(row: dict[str, Any], objects: dict[str, Any]) -> dict[str, Any]:
    target = objects["target"]
    return {"role": "batch-row", "local_row_offset": row["local_row_offset"], "candidate_ordinal": row["candidate_ordinal"],
        "row_manifest_sha256": sha(canonical(row)), "instruction_sha256": sha(canonical(objects["instruction"])),
        "target_sha256": sha(canonical(target)), "state_head": row["state_head"],
        "parent_remainder_sha256": target["parent_remainder_sha256"], "remainder_sha256": target["remainder_sha256"],
        "scalar": target["scalar"]}


def compare_candidate_publication(files: CandidateFiles, records: RootRecords, state: BatchReductionState,
                                  decision: DecisionArithmetic, ordinal: int, selection_sha: str, witness_sha: str,
                                  view_sha: str, phases: dict[str, str], payloads: dict[str, tuple[bytes, str, Any]],
                                  objects: dict[str, Any], required: bool) -> tuple[dict[str, Any], dict[str, Any] | None, bool]:
    row, row_sha, row_present = None, None, False
    if not decision.dependent:
        row = accepted_row_record(records, state, decision, ordinal, selection_sha, phases["reduction"], payloads, objects)
        row_sha = sha(canonical(row))
        prefix = f"rows/{len(state.rows):06d}"
        row_present = prefix + "/manifest.json" in files.before
        require(row_present or not required, "accepted_row_publication_present")
        if row_present:
            for name in ("physical-normalized.bin", "instruction.json", "target.json"):
                files.compare(prefix + "/" + name, payloads[name][0])
            files.object(prefix + "/manifest.json", row)
    candidate = candidate_decision_record(records, state, ordinal, selection_sha, witness_sha, view_sha, phases, objects, row_sha)
    name = f"candidates/{ordinal:06d}/manifest.json"
    present = name in files.before
    require(present or not required, "candidate_decision_publication_present")
    require(not present or decision.dependent or row_present, "candidate_decision_after_accepted_row")
    if present:
        files.object(name, candidate)
        state.advance(decision, None if decision.dependent else objects["instruction"]["rolling_sha256"],
                      None if row is None else batch_target_parent(row, objects), row_sha)
        state.decisions.append(copy.deepcopy(candidate))
    return candidate, row if row_present else None, present


@dataclass
class CandidateReplay:
    ordinal: int
    phases: dict[str, str]
    telemetry: dict[str, dict[str, Any]]
    decision: dict[str, Any] | None
    row: dict[str, Any] | None
    published: bool
    reduction: dict[str, Any] | None
    raw_readout: dict[str, Any] | None


def replay_candidate(files: CandidateFiles, records: RootRecords, selection: SelectionReplay,
                     bundle: C.FixedBundle, state: BatchReductionState, ordinal: int, phase_count: int,
                     publication_required: bool,
                     after_phase: Callable[[int, dict[str, str], bool, dict[str, Any] | None, dict[str, Any] | None], None]) -> CandidateReplay:
    integer(phase_count, "candidate_phase_prefix", 1, 6)
    require(selection.metadata_complete and selection.arithmetic is not None and selection.record is not None,
            "candidate_requires_complete_shared_selection")
    selected = selection.arithmetic
    witness = selection.witnesses[ordinal]
    selection_sha, witness_sha = sha(canonical(selection.record)), sha(canonical(witness))
    view_sha = sha(canonical(selection.views[ordinal]))
    prefix = f"candidates/{ordinal:06d}/e"
    hashes: dict[str, str] = {}
    telemetry: dict[str, dict[str, Any]] = {}
    previous = view_sha

    def compare(phase: str, payloads: dict[str, tuple[bytes, str, Any]]) -> None:
        nonlocal previous
        phase_prefix = f"candidates/{ordinal:06d}/reduction" if phase == "reduction" else prefix + "/" + phase
        digest, measurement = compare_phase(files, phase_prefix, phase, payloads, records, previous,
                                            selection_sha, ordinal, witness_sha)
        hashes[phase], telemetry[phase], previous = digest, measurement, digest
        CHECKED_CURSOR["last_complete_phase"] = f"candidate/{ordinal:06d}/{phase}"
        if phase != "reduction":
            after_phase(CANDIDATE_PHASES.index(phase) + 1, hashes, True, None, None)

    oracle = {"witness": copy.deepcopy(witness), "witness_sha256": witness_sha,
        "stage_hashes": {"geometry": records.binding()["fixed_manifest_sha256"]},
        "arrays": {"section": {"q.bin": selected.section["roots"], "kappa.bin": selected.section["kappa"]},
                   "cochain": {"f.u8": selected.f, "b-aux.u8": selected.b_aux}}}
    geometry, normalizers = bundle.raw_geometry()
    raw = E.raw_materialization(geometry, normalizers, oracle)
    compare("raw", {"raw-word.json": O.json_payload(raw["raw_word"]), "raw-chain.bin": O.typed_array(raw["chain"], "packed3", (EDGES,))})
    if phase_count == 1:
        return CandidateReplay(ordinal, hashes, telemetry, None, None, False, None, None)
    source_payloads = {"raw-source-" + role + ".bin": O.typed_array(part, "packed3", part.shape)
                       for role, part in zip(("d0", "d1", "d2", "aux"), raw["source"])}
    source_payloads["raw-source.json"] = O.json_payload(raw["raw_source"])
    compare("source", source_payloads)
    if phase_count == 2:
        return CandidateReplay(ordinal, hashes, telemetry, None, None, False, None, None)
    primal = bundle.primal(raw["source"])
    reductions = E.document("p1-reductions", {"order": "old-global-ascending-embedded-original-lead;new-owner-major-ascending-original-lead",
        "rows": 8059, "events": primal["events"], "coefficients_sha256": sha(primal["alpha"].tobytes()),
        "lower_zero": {"trits": LOWER, "packed_sha256": sha(pack(primal["lower"]))}, "eof": True})
    compare("primal", {"p1-coefficients.u8": O.typed_array(primal["alpha"], "u8", (8059,)),
        "p1-reductions.json": O.json_payload(reductions), "p1-exponent-residues.json": O.json_payload(C.exponent_record(bundle))})
    if phase_count == 3:
        return CandidateReplay(ordinal, hashes, telemetry, None, None, False, None, None)
    corrected, roots = bundle.corrected(raw["source"], primal)
    correction = E.source_correction_record(raw, corrected, primal, bundle.basis, roots, bundle.index)
    compare("p1", {"p1-roots.json": O.json_payload(roots),
        "source-lower-remainder.bin": O.typed_array(primal["lower"], "packed3", (LOWER,)),
        "source-top-corrected.bin": O.typed_array(corrected[2], "packed3", (4, TOP)),
        "source-correction.json": O.json_payload(correction)})
    if phase_count == 4:
        return CandidateReplay(ordinal, hashes, telemetry, None, None, False, None, None)
    require(not np.any(primal["lower"]) and np.array_equal(E.full_lower(corrected), primal["lower"]), "each_candidate_full_96776_zero")
    by_character = np.stack([E.grouped_forward(bundle.tables[owner]["entries"], corrected[2][owner]) for owner in range(4)])
    physical_raw = (by_character.sum(axis=0, dtype=np.uint16) % 3).astype(np.uint8)
    corrected_scalar = sum(dot(selected.section["roots"][owner], corrected[2][owner]) for owner in range(4)) % 3
    require(corrected_scalar == raw["selected_scalar"] == witness["scalar"] == dot(state.selection_lambda, physical_raw) and
            corrected_scalar == (raw["homogeneous_scalar"] - raw["section_scalar"]) % 3, "every_selected_four_B_scalar_identity")
    B_record = C.document("B", {"characters": [0, 1, 2, 3], "physical_trits": PHYSICAL,
        "source_correction_sha256": sha(canonical(correction)), "witness_sha256": witness_sha,
        "corrected_scalar": corrected_scalar, "physical_scalar": dot(state.selection_lambda, physical_raw),
        "raw_sha256": sha(pack(physical_raw)), "by_character_sha256": sha(pack(by_character)), "all_four_summed": True, "eof": True})
    compare("B", {"physical-by-character.bin": O.typed_array(by_character, "packed3", (4, PHYSICAL)),
        "physical-raw.bin": O.typed_array(physical_raw, "packed3", (PHYSICAL,)), "B.json": O.json_payload(B_record)})
    if phase_count == 5:
        return CandidateReplay(ordinal, hashes, telemetry, None, None, False, None, None)
    decision = state.reduce(physical_raw, witness["scalar"])
    payloads, objects = reduction_payloads(state, decision, ordinal, selection_sha, witness_sha,
                                          sha(canonical(correction)), sha(canonical(roots)))
    compare("reduction", payloads)
    candidate, row, published = compare_candidate_publication(files, records, state, decision, ordinal, selection_sha,
        witness_sha, view_sha, hashes, payloads, objects, publication_required)
    after_phase(6, hashes, published, candidate if published else None, row)
    w = raw["slp"].values["w"]
    repair = None if witness["kind"] == "auxiliary" else [-int(w["exponent"][0]) // 6, -int(w["exponent"][1]) // 6, E.signed(int(w["omega"]))]
    readout = {"epsilon_unrepaired": [int(value) for value in w["exponent"]], "omega_unrepaired": int(w["omega"]),
        "repair_exponents": repair, "raw_slp_letters": raw["slp"].values["raw-root"]["length"],
        "source_homogeneous_scalar": raw["homogeneous_scalar"], "section_scalar": raw["section_scalar"],
        "selection_scalar": witness["scalar"], "alpha_support": int(np.count_nonzero(primal["alpha"]))}
    return CandidateReplay(ordinal, hashes, telemetry, candidate if published else None, row, published, objects["reduction"], readout)


def private_values(state: BatchReductionState) -> dict[str, Any]:
    return {"kind": "BatchReductionState", "processed_candidates": state.processed_candidates,
        "dependent_candidates": state.dependent_candidates, "accepted_new_rows": len(state.rows),
        "rank": state.rank, "generation": state.generation, "reduction_state_head": state.physical_head,
        "target_remainder_sha256": sha(pack(state.target)), "current_lambda_sha256": None}


def checkpoint_record(records: RootRecords, state: BatchReductionState, sequence: int, predecessor: str | None,
                      selection_sha: str | None, selection_phases: dict[str, str], ordinal: int | None,
                      candidate_phases: dict[str, str]) -> dict[str, Any]:
    return document("checkpoint", {**records.binding(), "selection_sha256": selection_sha,
        "predecessor_checkpoint_sha256": predecessor, "sequence": sequence, **private_values(state),
        "current_candidate_ordinal": ordinal, "current_phase_manifests": candidate_phases,
        "last_candidate_manifest_sha256": sha(canonical(state.decisions[-1])) if state.decisions else None,
        "last_row_manifest_sha256": state.row_manifests[-1] if state.row_manifests else None,
        "selection_phase_manifests": selection_phases})


def progress_head_record(checkpoint: dict[str, Any]) -> dict[str, Any]:
    return document("progress-head", {"checkpoint_sha256": sha(canonical(checkpoint)),
        **{key: checkpoint[key] for key in ("owner_sha256", "source_sha256", "start_sha256", "sequence", "kind",
            "processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation",
            "reduction_state_head", "target_remainder_sha256", "current_lambda_sha256")}})


def phase_at_sequence(sequence: int) -> tuple[str, str, int | None]:
    integer(sequence, "registered_phase_sequence", 1, 3 + 6 * BATCH_SIZE)
    if sequence <= 3:
        phase = SELECTION_PHASES[sequence - 1]
        return "selection/" + phase, phase, None
    ordinal, phase_index = divmod(sequence - 4, 6)
    phase = CANDIDATE_PHASES[phase_index]
    prefix = f"candidates/{ordinal:06d}/" + ("reduction" if phase == "reduction" else "e/" + phase)
    return prefix, phase, ordinal


class ProgressAudit:
    def __init__(self, files: CandidateFiles, records: RootRecords):
        self.files, self.records = files, records
        self.head = files.json("progress/HEAD", "progress-head") if "progress/HEAD" in files.before else None
        self.sequence = -1 if self.head is None else integer(self.head["sequence"], "actual_progress_sequence", 0, 3 + 6 * BATCH_SIZE)
        self.checkpoints: dict[int, tuple[str, dict[str, Any]]] = {}
        self.validated: dict[int, str] = {}
        self.committed: dict[str, Any] | None = None
        self.tail: dict[str, Any] | None = None
        for name in files.files:
            match = re.fullmatch(r"progress/checkpoints/([0-9a-f]{64})\.json", name)
            if match is None:
                continue
            checkpoint = files.json(name, "checkpoint")
            sequence = integer(checkpoint["sequence"], "saved_checkpoint_sequence", 0, 3 + 6 * BATCH_SIZE)
            require(match[1] == files.before[name][1] and sequence not in self.checkpoints and sequence <= self.sequence + 1,
                    "checkpoint_named_full_hash_unique_and_at_most_one_ahead")
            self.checkpoints[sequence] = name, checkpoint
        if self.checkpoints:
            require(sorted(self.checkpoints) == list(range(max(self.checkpoints) + 1)), "no_saved_checkpoint_hole")
        require(self.sequence < 0 or self.sequence in self.checkpoints, "progress_head_has_its_complete_checkpoint")
        if self.head is not None:
            checkpoint_name = self.checkpoints[self.sequence][0]
            require(self.head["checkpoint_sha256"] == files.before[checkpoint_name][1], "progress_HEAD_references_its_actual_checkpoint_file")
        self.phase_sequences = set()
        for sequence in range(1, 3 + 6 * BATCH_SIZE + 1):
            prefix, _, _ = phase_at_sequence(sequence)
            if prefix + "/manifest.json" in files.before:
                self.phase_sequences.add(sequence)
        require(self.phase_sequences.issubset(set(range(1, self.sequence + 2))) and
                set(range(1, self.sequence + 1)).issubset(self.phase_sequences), "one_next_phase_and_no_phase_holes")
        self.phase_end = max(self.phase_sequences, default=0)

    def compare(self, state: BatchReductionState, sequence: int, selection_sha: str | None,
                selection_phases: dict[str, str], ordinal: int | None, candidate_phases: dict[str, str],
                metadata_complete: bool = True) -> None:
        require(sequence <= self.sequence + 1, "only_registered_next_checkpoint_comparison")
        actual = self.checkpoints.get(sequence)
        required = sequence <= self.sequence
        require(actual is not None or not required, "all_committed_checkpoints_present")
        if actual is None:
            return
        require(metadata_complete, "checkpoint_after_its_complete_metadata_publication")
        predecessor = None if sequence == 0 else self.validated.get(sequence - 1)
        require(sequence == 0 or predecessor is not None, "checkpoint_complete_predecessor")
        checkpoint = checkpoint_record(self.records, state, sequence, predecessor, selection_sha,
                                       selection_phases, ordinal, candidate_phases)
        name, _ = actual
        digest = self.files.object(name, checkpoint)["sha256"]
        self.validated[sequence] = digest
        if sequence == self.sequence:
            expected_head = progress_head_record(checkpoint)
            self.files.object("progress/HEAD", expected_head)
            self.committed = copy.deepcopy(checkpoint)

    def tail_record(self, phase: str, ordinal: int | None, phase_sha: str, selection_sha: str | None,
                    row: dict[str, Any] | None = None, candidate: dict[str, Any] | None = None) -> None:
        self.tail = {"kind": "NEXT_SELECTION_PHASE" if ordinal is None else "NEXT_CANDIDATE_PHASE", "phase": phase,
            "candidate_ordinal": ordinal, "selection_sha256": selection_sha, "phase_manifest_sha256": phase_sha,
            "row_manifest_sha256": None if row is None else sha(canonical(row)),
            "candidate_manifest_sha256": None if candidate is None else sha(canonical(candidate)),
            "checkpoint_sha256": self.validated.get(self.sequence + 1), "final_manifest_sha256": None,
            "public_head_sha256": None, "independently_compared": True, "published_by_checker": False}

    def complete(self) -> None:
        require(set(self.checkpoints) == set(self.validated), "all_formed_checkpoint_objects_compared")
        require(self.sequence < 0 or self.committed is not None, "actual_progress_prefix_fully_compared")
        require((self.phase_end > self.sequence and self.phase_end > 0) == (self.tail is not None),
                "every_extra_durable_phase_has_explicit_scope")


def character_support(values: np.ndarray, width: int) -> list[dict[str, Any]]:
    require(values.shape == (4, width) and values.dtype == np.uint8 and not np.any(values > 2), "four_character_support_input")
    return [{"character": owner, "offset": owner * width, "trits": width,
        "support": int(np.count_nonzero(values[owner])),
        "trit_counts": [int(np.count_nonzero(values[owner] == trit)) for trit in range(3)]} for owner in range(4)]


def selection_readout(selection: SelectionReplay, functional: np.ndarray) -> dict[str, Any]:
    require(selection.arithmetic is not None and selection.record is not None, "complete_selection_readout")
    arithmetic, record = selection.arithmetic, selection.record
    kappa = arithmetic.section["kappa"]
    d0 = np.count_nonzero(kappa[:24192].reshape(4, 6, 2, 504), axis=(2, 3)).tolist()
    d1 = np.count_nonzero(kappa[24192:96768].reshape(4, 6, 2, 3, 504), axis=(2, 3, 4)).tolist()
    auxiliary = kappa[96768:].tolist()
    total = sum(sum(row) for row in d0) + sum(sum(row) for row in d1) + sum(value != 0 for value in auxiliary)
    score_by_tag = np.count_nonzero(arithmetic.score, axis=(1, 2)).tolist()
    require(total == int(np.count_nonzero(kappa)) and sum(score_by_tag) == int(np.count_nonzero(arithmetic.score)),
            "all_character_tag_and_shared_aux_support_totals")
    return {**{key: copy.deepcopy(record[key]) for key in ("failed_count", "first_failed_index", "first_failed_edge", "failed_indices", "failed_edges")},
        "q_characters": character_support(arithmetic.section["roots"], TOP),
        "lambda_characters": character_support(functional.reshape(4, PHYSICAL // 4), PHYSICAL // 4),
        "aux_values": arithmetic.b_aux.tolist(), "score_support": {"total": sum(score_by_tag), "by_tag": score_by_tag},
        "kappa_support": {"total": total, "degree0_by_character_tag": d0, "degree1_by_character_tag": d1, "aux_values": auxiliary},
        "p1_equation_residual_support": int(np.count_nonzero(arithmetic.section["equation_residuals"]))}


def final_rho2(state: BatchReductionState) -> dict[str, Any]:
    require(len(state.parents) == len(state.anchor.parents) + len(state.rows), "one_target_identity_per_accepted_batch_row")
    return {"mode": "derived", "value": 1, "original_rho2_directly_read": False, "original_rho2_packed_sha256": RHO2_SHA,
        "accepted_target_derivation_parents": copy.deepcopy(state.parents), "identity_convention": {
            "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",
            "all_one_row_steps": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row",
            "batch_rows": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row; correction appends normalized_word^sr(target.scalar)"},
        "anchor_completed_steps": state.old_continuation_rows, "new_batch_target_steps_executed": len(state.rows)}


def candidate_readouts(selection: SelectionReplay, candidates: list[CandidateReplay]) -> list[dict[str, Any]]:
    complete = {item.ordinal: item for item in candidates if item.published}
    result = []
    for witness in selection.witnesses:
        ordinal = witness["ordinal"]
        item = complete.get(ordinal)
        if item is None:
            result.append({"ordinal": ordinal, "kind": witness["kind"], "witness_sha256": sha(canonical(witness)),
                "selection_scalar": witness["scalar"], "outcome": "SKIPPED_AFTER_LINEAR", "candidate_manifest_sha256": None,
                "row_manifest_sha256": None, "lead": None, "sigma": None, "target_scalar": None,
                "rank_before": None, "rank_after": None, "generation_before": None, "generation_after": None,
                "phase_telemetry": {phase: None for phase in CANDIDATE_PHASES}, "raw_readout": None})
            continue
        require(item.decision is not None and item.reduction is not None, "processed_candidate_readout_has_decision")
        result.append({"ordinal": ordinal, "kind": witness["kind"], "witness_sha256": sha(canonical(witness)),
            "selection_scalar": witness["scalar"], "outcome": item.decision["outcome"],
            "candidate_manifest_sha256": sha(canonical(item.decision)),
            "row_manifest_sha256": None if item.row is None else sha(canonical(item.row)),
            **{key: item.reduction[key] for key in ("lead", "sigma", "target_scalar", "rank_before", "rank_after", "generation_before", "generation_after")},
            "phase_telemetry": {phase: receipt(f"candidates/{ordinal:06d}/" +
                ("reduction" if phase == "reduction" else "e/" + phase) + "/telemetry.json", canonical(item.telemetry[phase]))
                for phase in CANDIDATE_PHASES}, "raw_readout": copy.deepcopy(item.raw_readout)})
    return result


@dataclass
class FinalReplay:
    terminal: str
    kind: str
    manifest: dict[str, Any]
    separator: dict[str, Any]
    functional: np.ndarray | None
    head: dict[str, Any] | None
    telemetry: dict[str, Any]
    skipped: list[int]


def compare_final(files: CandidateFiles, records: RootRecords, selection: SelectionReplay,
                  state: BatchReductionState, progress: ProgressAudit) -> FinalReplay:
    require(selection.metadata_complete and selection.record is not None and progress.tail is None and
            progress.sequence == 3 + 6 * state.processed_candidates and progress.committed is not None,
            "finalizer_only_after_complete_private_candidate_prefix")
    selected_count = len(selection.witnesses)
    linear = not np.any(state.target)
    require(state.processed_candidates == selected_count or linear, "no_partial_candidate_flush")
    require(selected_count == 0 or len(state.rows) >= 1, "nonempty_complete_batch_has_an_independent_first_row")
    require(not linear or state.processed_candidates > 0, "linear_from_actual_new_reduction")
    arithmetic = state.finish_arithmetic()
    functional = arithmetic["lambda"]
    terminal = "LINEAR_MEMBERSHIP_CANDIDATE" if linear else "BATCH_COMPLETE_CANDIDATE" if selected_count else "COMPLETE_ZERO_CANDIDATE"
    skipped = list(range(state.processed_candidates, selected_count)) if linear else []
    separator = document("separator", {"kind": arithmetic["kind"], "selection_lambda_sha256": sha(pack(state.selection_lambda)),
        "lambda_sha256": None if linear else sha(pack(functional)), "lambda_rho2": None if linear else final_rho2(state),
        "direct_pairing": arithmetic["direct_pairing"], "anchor_pairing_rows": None if linear else state.anchor_rank,
        "final_pairing_rows": None if linear else state.rank, "new_lambda_oracle": None,
        "source_lower_zero": "NOT_ASSERTED", "physical_lower_zero": True})
    payloads = {"target-remainder.bin": O.typed_array(state.target, "packed3", (PHYSICAL,)), "separator.json": O.json_payload(separator)}
    if functional is not None:
        payloads["lambda.bin"] = O.typed_array(functional, "packed3", (PHYSICAL,))
    telemetry, telemetry_raw = telemetry_record(files, "final", "final", sum(len(item[0]) for item in payloads.values()))
    payloads["telemetry.json"] = (telemetry_raw, "json", None)
    common = {key: value for key, value in records.binding().items() if key != "fixed_manifest_sha256"}
    counts = {"anchor_completed_steps": state.old_continuation_rows, "selected_count": selected_count,
        "processed_candidates": state.processed_candidates, "dependent_candidates": state.dependent_candidates,
        "accepted_new_rows": len(state.rows), "rank": state.rank, "generation": state.generation,
        "state_head": state.physical_head, "target_remainder_sha256": sha(pack(state.target)),
        "lambda_sha256": None if functional is None else sha(pack(functional))}
    manifest = document("final-manifest", {**common, "selection_sha256": selection.sha256, "terminal": terminal,
        "kind": arithmetic["kind"], **counts, "skipped_after_linear": skipped,
        "last_candidate_manifest_sha256": sha(canonical(state.decisions[-1])) if state.decisions else None,
        "last_row_manifest_sha256": state.row_manifests[-1] if state.row_manifests else None,
        "files": payload_roster(payloads), "eof": True})
    for name, item in payloads.items():
        files.compare("final/" + name, item[0])
    files.object("final/manifest.json", manifest)
    head = document("head", {**common, "selection_sha256": selection.sha256, "final_manifest_sha256": sha(canonical(manifest)),
        "terminal": terminal, "kind": arithmetic["kind"], **counts, "new_lambda_oracle": None})
    if "HEAD" in files.before:
        files.object("HEAD", head)
    else:
        head = None
    require("result.json" not in files.before or head is not None, "producer_result_after_public_physical_HEAD")
    CHECKED_CURSOR["public_head_compared"] = head is not None
    return FinalReplay(terminal, arithmetic["kind"], manifest, separator, functional, head, telemetry, skipped)


def invocation_records(files: CandidateFiles, inputs: AcceptedInputs, records: RootRecords,
                       progress: ProgressAudit, final: FinalReplay | None) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Authenticate every explicit invocation; never infer the latest by UUID/time."""
    keys = {"id", "portable_acceptance_sha256", "acceptance_sha256", "owner_sha256", "source_sha256", "start_sha256",
        "fixed_manifest_sha256", "selection_start_sha256", "registration", "resume", "batch_size", "max_batches",
        "max_seconds", "max_memory_mib", "progress_head_before_sha256", "physical_head_before_sha256",
        "processed_candidates_before", "accepted_new_rows_before", "started_utc", "launch", "host_paths"}
    heads = {sha(canonical(progress_head_record(value))): value for sequence, (_, value) in progress.checkpoints.items()
             if sequence in progress.validated and sequence <= progress.sequence}
    descriptors, by_sha, fresh, bootstraps = [], {}, 0, 0
    for name in files.files:
        match = re.fullmatch(r"invocations/([0-9a-f]{32})\.json", name)
        if match is None:
            continue
        value = files.json(name, "invocation")
        require(set(value) == keys | {"schema", "sha256"} and value["id"] == match[1], "invocation_exact_keys_and_id")
        for key, expected in records.binding().items():
            same_json(value[key], expected, "invocation_same_portable_binding:" + key)
        same_json(value["portable_acceptance_sha256"], inputs.portable_sha256, "invocation_portable_acceptance")
        same_json(value["registration"], inputs.value["registration"], "invocation_registered_policy")
        require(type(value["resume"]) is bool and type(value["batch_size"]) is int and value["batch_size"] == BATCH_SIZE and
                type(value["max_batches"]) is int and value["max_batches"] == 1, "invocation_single_absolute_batch")
        same_json({key: value[key] for key in ("max_seconds", "max_memory_mib")},
                  inputs.value["registration"]["producer_limits"], "invocation_registered_producer_limits")
        host = value["host_paths"]
        require(type(host) is dict and set(host) == {"parents", "acceptance", "output"} and
                type(host["parents"]) is dict and set(host["parents"]) == set(PARENT_ROLES), "invocation_exact_host_paths")
        for item in [host["acceptance"], host["output"], *host["parents"].values()]:
            require(type(item) is str and Path(item).is_absolute(), "invocation_explicit_absolute_path")
        old_acceptance = copy.deepcopy(inputs.portable)
        for parent in old_acceptance["parents"]:
            parent["path"] = host["parents"][parent["role"]]
        require(value["acceptance_sha256"] == sha(canonical(old_acceptance)), "invocation_exact_relocated_acceptance_hash")
        launch = value["launch"]
        require(type(launch) is dict and set(launch) == {"run", "attempt", "head", "workflow"}, "invocation_launch_exact_keys")
        integer(launch["run"], "invocation_run", 1)
        integer(launch["attempt"], "invocation_attempt", 1)
        require(type(launch["head"]) is str and re.fullmatch(r"[0-9a-f]{40}", launch["head"]) is not None and
                type(launch["workflow"]) is str and re.fullmatch(r"\.github/workflows/[a-z0-9-]+\.yml", launch["workflow"]) is not None,
                "invocation_explicit_launch_identity")
        require(type(value["started_utc"]) is str, "invocation_started_UTC_string")
        stamp = datetime.fromisoformat(value["started_utc"].replace("Z", "+00:00"))
        require(stamp.tzinfo is not None and stamp.utcoffset() == timezone.utc.utcoffset(stamp), "invocation_actual_UTC_offset")
        before = value["progress_head_before_sha256"]
        if before is None:
            require(value["processed_candidates_before"] == value["accepted_new_rows_before"] == 0 and
                    type(value["processed_candidates_before"]) is type(value["accepted_new_rows_before"]) is int,
                    "no_progress_before_has_zero_counts")
        else:
            require(before in heads, "invocation_before_is_an_actual_replayed_progress_HEAD")
            checkpoint = heads[before]
            for key in ("processed_candidates", "accepted_new_rows"):
                same_json(value[key + "_before"], checkpoint[key], "invocation_before_absolute_counts")
        physical_before = value["physical_head_before_sha256"]
        if physical_before is not None:
            require(final is not None and final.head is not None and physical_before == sha(canonical(final.head)) and
                    before == sha(canonical(progress_head_record(progress.committed))), "completed_resume_same_physical_HEAD")
        if value["resume"] is False:
            fresh += 1
            require(before is physical_before is None, "fresh_invocation_has_no_preexisting_HEAD")
        elif before is physical_before is None:
            # The real resume flag survives a stop before the first normal
            # invocation or HEAD.  The strict zero counts were checked above.
            bootstraps += 1
        pin = files.object(name, value)
        descriptors.append(pin)
        by_sha[pin["sha256"]] = value
    require(fresh <= 1 and (bool(descriptors) and (fresh == 1 or bootstraps > 0) or
            not descriptors and progress.sequence < 0 and not progress.checkpoints and not progress.phase_sequences) and
            len(by_sha) == len(descriptors), "one_fresh_or_bootstrap_history_or_unformed_preinvocation_stop")
    return descriptors, by_sha


def input_inventories(files: CandidateFiles, inputs: AcceptedInputs, complete_required: bool) -> dict[str, Any]:
    expected = {"parents": inputs.parent_inventory(), "code": inputs.code_files}
    pins: dict[str, str | None] = {}
    for kind in ("parents", "code"):
        for stage in ("before", "after"):
            name = "inputs/" + kind + "-" + stage + ".json"
            present = name in files.before
            require(present or not complete_required, "complete_input_inventory_present")
            pins[kind + "_" + stage + "_sha256"] = files.object(name, expected[kind])["sha256"] if present else None
    # The independent actual before/after authentication is performed by the
    # caller before these true values can be used in a completed checker result.
    return {**pins, "portable_acceptance_sha256": inputs.portable_sha256, "acceptance_sha256": inputs.sha256,
        "all_parent_files_and_directories_unchanged": True, "all_code_and_raw_unchanged": True, "acceptance_unchanged": True}


def compare_producer_result(files: CandidateFiles, inputs: AcceptedInputs, records: RootRecords,
                            selection: SelectionReplay, state: BatchReductionState, candidates: list[CandidateReplay],
                            final: FinalReplay, invocations: list[dict[str, Any]], by_sha: dict[str, dict[str, Any]],
                            preservation: dict[str, Any]) -> dict[str, Any]:
    require(final.head is not None and all(preservation[key] is not None for key in
            ("parents_before_sha256", "parents_after_sha256", "code_before_sha256", "code_after_sha256")),
            "producer_success_after_HEAD_and_input_inventory")
    actual = files.json("result.json", "result")
    finite_measurement(actual["elapsed_seconds"], "producer_total_elapsed")
    invocation_sha = actual["invocation_sha256"]
    require(invocation_sha in by_sha, "producer_result_explicit_invocation_file")
    # Task1004: a completed packet may be re-admitted on a different host.
    # Its original invocation/result bytes remain unchanged.  The invocation
    # reader reconstructed that exact historical acceptance from portable
    # input pins plus the recorded host paths; current admission is reported
    # separately by this checker and the outer execution receipt.
    producer_preservation = copy.deepcopy(preservation)
    producer_preservation["acceptance_sha256"] = by_sha[invocation_sha]["acceptance_sha256"]
    expected = document("result", {"status": "PASS", "terminal": final.terminal, "kind": final.kind,
        **{key: records.binding()[key] for key in ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "parent_layout_sha256": sha(canonical(records.parent_layout)), "selection_sha256": selection.sha256,
        "head_sha256": sha(canonical(final.head)), "final_manifest_sha256": sha(canonical(final.manifest)),
        **{key: final.manifest[key] for key in ("anchor_completed_steps", "selected_count", "processed_candidates",
            "dependent_candidates", "accepted_new_rows", "skipped_after_linear", "rank", "generation", "state_head",
            "target_remainder_sha256", "lambda_sha256")}, "new_lambda_oracle": None,
        "selection_readout": selection_readout(selection, state.selection_lambda),
        "final_lambda_characters": None if final.functional is None else character_support(final.functional.reshape(4, PHYSICAL // 4), PHYSICAL // 4),
        "candidates": candidate_readouts(selection, candidates),
        "selection_telemetry": {phase: receipt("selection/" + phase + "/telemetry.json", canonical(selection.telemetry[phase]))
                                for phase in SELECTION_PHASES},
        "final_telemetry": receipt("final/telemetry.json", canonical(final.telemetry)), "invocation_sha256": invocation_sha,
        "invocations": invocations, "input_preservation": producer_preservation, "elapsed_seconds": actual["elapsed_seconds"],
        "old_snapshot_numeric_replays": 0, "old_insert_numeric_replays": 0, "old_success_suites": 0,
        "positive_readout": "NEW_BATCH_SAME_WORD_ADAPTER_PENDING" if final.kind == "LinearMembershipCandidate" else "NOT_APPLICABLE",
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "candidate": True, "cross_checked": False, "verified": False})
    files.object("result.json", expected)
    return expected


def compare_diagnostic(name: str, files: CandidateFiles, inputs: AcceptedInputs, records: RootRecords,
                       progress: ProgressAudit, final: FinalReplay | None,
                       invocations: dict[str, dict[str, Any]]) -> dict[str, Any]:
    require(name in DIAGNOSTIC_TYPES, "registered_diagnostic_filename")
    suffix, status, terminal = DIAGNOSTIC_TYPES[name]
    value = files.json(name, suffix)
    keys = {"status", "terminal", "phase", "reason", "partial", "owner_sha256", "source_sha256", "start_sha256",
        "selection_start_sha256", "selection_sha256", "invocation_sha256", "progress_head_sha256", "checkpoint_sha256",
        "public_head_sha256", "final_manifest_sha256", "processed_candidates", "dependent_candidates", "accepted_new_rows",
        "rank", "generation", "max_seconds", "max_memory_mib", "elapsed_seconds", "candidate", "cross_checked", "verified"}
    require(set(value) == keys | {"schema", "sha256"} and value["partial"] is True and value["candidate"] is False and
            value["cross_checked"] is False and value["verified"] is False and
            (value["status"], value["terminal"]) == (status, terminal),
            "producer_diagnostic_exact_nonpromotion_type")
    require(type(value["phase"]) is str and type(value["reason"]) is str, "producer_diagnostic_reason_and_phase")
    finite_measurement(value["elapsed_seconds"], "producer_diagnostic_elapsed")
    same_json({key: value[key] for key in ("max_seconds", "max_memory_mib")},
              inputs.value["registration"]["producer_limits"], "producer_diagnostic_registered_limits")
    for key, filename in (("owner_sha256", "owner.json"), ("source_sha256", "source.json"),
                          ("start_sha256", "start.json"), ("selection_start_sha256", "selection/start.json")):
        require(value[key] is None or filename in files.expected and
                value[key] == records.binding()[key] == files.expected[filename]["sha256"],
                "diagnostic_only_actual_formed_root_binding")
    formed_selection = files.expected.get("selection/selection.json", {}).get("sha256")
    require(value["selection_sha256"] is None or value["selection_sha256"] == formed_selection, "diagnostic_formed_selection_only")
    require(value["invocation_sha256"] is None or value["invocation_sha256"] in invocations, "diagnostic_actual_invocation")
    checkpoints = {digest: progress.checkpoints[sequence][1] for sequence, digest in progress.validated.items()
                   if sequence <= progress.sequence}
    checkpoint_sha = value["checkpoint_sha256"]
    if value["progress_head_sha256"] is None:
        require(checkpoint_sha is None and all(value[key] is None for key in
            ("processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation")),
            "unformed_diagnostic_progress_has_no_counts")
    else:
        require(checkpoint_sha in checkpoints, "diagnostic_actual_historical_progress_checkpoint")
        checkpoint = checkpoints[checkpoint_sha]
        require(value["progress_head_sha256"] == sha(canonical(progress_head_record(checkpoint))), "diagnostic_actual_progress_HEAD_hash")
        for key in ("processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation"):
            same_json(value[key], checkpoint[key], "diagnostic_exact_saved_counts")
    require(value["final_manifest_sha256"] is None or "final/manifest.json" in files.expected and final is not None and
            value["final_manifest_sha256"] == sha(canonical(final.manifest)), "diagnostic_formed_final_manifest")
    require(value["public_head_sha256"] is None or "HEAD" in files.expected and final is not None and final.head is not None and
            value["public_head_sha256"] == sha(canonical(final.head)), "diagnostic_formed_public_HEAD")
    files.object(name, value)
    return value


def compare_diagnostics(files: CandidateFiles, inputs: AcceptedInputs, records: RootRecords,
                        progress: ProgressAudit, final: FinalReplay | None,
                        invocations: dict[str, dict[str, Any]]) -> str | None:
    # Both are authenticated histories.  Their names and timestamps cannot
    # establish which stop was latest, and neither overrides a complete final.
    checked = [compare_diagnostic(name, files, inputs, records, progress, final, invocations)
               for name in DIAGNOSTIC_TYPES if name in files.before]
    return checked[0]["terminal"] if len(checked) == 1 else None


def registered_basenames(selected_count: int) -> dict[str, set[str]]:
    """Exact normal names, used only to recognize preserved atomic diagnostics."""
    result: dict[str, set[str]] = {"": {"parent-layout.json", "source.json", "owner.json", "start.json", "HEAD", "result.json", *DIAGNOSTIC_TYPES},
        "fixed": {"manifest.json"}, "selection": {"start.json", "selection.json"}, "progress": {"HEAD"},
        "inputs": {kind + "-" + stage + ".json" for kind in ("parents", "code") for stage in ("before", "after")},
        "final": {"target-remainder.bin", "lambda.bin", "separator.json", "telemetry.json", "manifest.json"}}
    phase_names = {
        "section": {"q.bin", "p1-values.u8", "chi.u8", "equation-values.u8", "equation-residuals.u8", "beta.u8", "kappa.bin",
            "lead-original.u32", "lead-embedded.u32", "new-solve-order.u32", "old-solve-order.u32", "section.json"},
        "cochain": {"score.u8", "f.u8", "b-aux.u8", "cochain.json"},
        "tree": {"potential-f.u8", "potential-tau.u8", "chord-values.u8", "chord-tau.u8", "chord-residuals.u8",
            "selected-chords.u32", "fit.u8", "basis-tau.u8", "failed-indices.u32", "failed-edges.u32", "tree.json", "witness-roster.json"},
        "raw": {"raw-word.json", "raw-chain.bin"},
        "source": {"raw-source-d0.bin", "raw-source-d1.bin", "raw-source-d2.bin", "raw-source-aux.bin", "raw-source.json"},
        "primal": {"p1-coefficients.u8", "p1-reductions.json", "p1-exponent-residues.json"},
        "p1": {"p1-roots.json", "source-lower-remainder.bin", "source-top-corrected.bin", "source-correction.json"},
        "B": {"physical-by-character.bin", "physical-raw.bin", "B.json"},
        "reduction": {"coefficients.u8", "physical-remainder.bin", "target-before.bin", "target-remainder.bin", "physical-literal.json",
            "reduction.json", "physical-normalized.bin", "instruction.json", "target.json"}}
    for phase in SELECTION_PHASES:
        result["selection/" + phase] = phase_names[phase] | {"manifest.json", "telemetry.json"}
    for ordinal in range(selected_count):
        prefix = f"candidates/{ordinal:06d}"
        result[prefix] = {"witness.json", "oracle-view.json", "manifest.json"}
        for phase in CANDIDATE_PHASES:
            directory = prefix + ("/" if phase == "reduction" else "/e/") + phase
            result[directory] = phase_names[phase] | {"manifest.json", "telemetry.json"}
    for offset in range(BATCH_SIZE):
        result[f"rows/{offset:06d}"] = {"physical-normalized.bin", "instruction.json", "target.json", "manifest.json"}
    return result


def compare_candidate_roster(files: CandidateFiles, selected_count: int) -> None:
    registered = registered_basenames(selected_count)
    normal_directories = {"fixed", "selection", "candidates", "rows", "progress", "progress/checkpoints", "invocations", "inputs"}
    for ordinal in range(selected_count):
        normal_directories.update({f"candidates/{ordinal:06d}", f"candidates/{ordinal:06d}/e"})
    for name in files.expected:
        parent = name.rpartition("/")[0]
        while parent:
            normal_directories.add(parent)
            parent = parent.rpartition("/")[0]
    diagnostic_roots = set()
    for directory in files.directories:
        parent, _, basename = directory.rpartition("/")
        match = re.fullmatch(r"\.(pending|orphan)-([A-Za-z0-9-]+)-[0-9a-f]{32}", basename)
        accepted = False
        if parent == "" and re.fullmatch(r"\.pending-final-[0-9a-f]{32}", basename):
            accepted = True
        elif parent == "rows" and re.fullmatch(r"\.pending-row-[0-9]{6}-[0-9a-f]{32}", basename):
            offset = int(basename.split("-")[2])
            accepted = offset < BATCH_SIZE
        elif match is not None:
            phase = match[2]
            accepted = (parent == "selection" and phase in SELECTION_PHASES or
                re.fullmatch(r"candidates/[0-9]{6}/e", parent) is not None and
                int(parent.split("/")[1]) < selected_count and phase in CANDIDATE_PHASES[:-1] or
                re.fullmatch(r"candidates/[0-9]{6}", parent) is not None and
                int(parent.split("/")[1]) < selected_count and phase == "reduction")
        if accepted:
            diagnostic_roots.add(directory)
    def inside_diagnostic(name: str) -> bool:
        return any(name == root or name.startswith(root + "/") for root in diagnostic_roots)
    for name in files.files:
        if name in files.expected or inside_diagnostic(name):
            continue
        parent, _, basename = name.rpartition("/")
        match = re.fullmatch(r"\.([^/]+)\.pending-[0-9a-f]{32}", basename)
        require(match is not None, "no_unregistered_normal_file:" + name)
        original = match[1]
        accepted = original in registered.get(parent, set())
        if parent == "invocations":
            accepted = re.fullmatch(r"[0-9a-f]{32}\.json", original) is not None
        elif parent == "progress/checkpoints":
            accepted = re.fullmatch(r"[0-9a-f]{64}\.json", original) is not None
        require(accepted, "atomic_pending_only_at_its_registered_basename:" + name)
    for directory in files.directories:
        require(directory in normal_directories or inside_diagnostic(directory), "no_unregistered_normal_directory:" + directory)


def checker_receipt_template() -> dict[str, Any]:
    self_raw = file_path(REPOSITORY, CHECKER_FILE).read_bytes()
    return {"status": "UNKNOWN_RESOURCE", "partial": True, "terminal": None,
        "owner_sha256": None, "source_sha256": None, "start_sha256": None, "selection_start_sha256": None,
        "selection_sha256": None, "progress_head_sha256": None, "public_head_sha256": None, "producer_result_sha256": None,
        "final_manifest_sha256": None, "anchor_completed_steps": None, "selected_count": None,
        "processed_candidates": None, "dependent_candidates": None, "accepted_new_rows": None, "rank": None,
        "generation": None, "state_head": None, "target_remainder_sha256": None, "lambda_sha256": None,
        "selection_phases_compared": [], "candidate_phases_compared": [], "candidate_decisions_compared": 0,
        "accepted_rows_compared": 0, "all_completed_payloads_and_json_compared": False, "public_final_compared": False,
        "old_snapshot_numeric_replays": 0, "old_insert_numeric_replays": 0, "old_success_suites": 0,
        "checker_source": receipt(CHECKER_FILE, self_raw), "runtime": {"python": sys.version, "numpy": np.__version__},
        "elapsed_seconds": 0.0, "input_preservation": None, "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED",
        "full_A0": False, "candidate": False, "cross_checked": False, "verified": False, "durable_tail": None}


def report_progress(report: dict[str, Any], progress: ProgressAudit) -> None:
    # Even a fully compared next reduction may have mutated the in-memory
    # replay state.  Every public private-state field comes from this frozen
    # copy of the actual HEAD checkpoint, never from that advanced state.
    if progress.committed is None:
        return
    committed = progress.committed
    report["progress_head_sha256"] = sha(canonical(progress_head_record(committed)))
    for key in ("processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation", "target_remainder_sha256"):
        report[key] = copy.deepcopy(committed[key])
    report["state_head"] = committed["reduction_state_head"]
    report["lambda_sha256"] = None


def check_actual(args: argparse.Namespace, report: dict[str, Any]) -> dict[str, Any]:
    inputs = AcceptedInputs(args)
    files = CandidateFiles(args.candidate_root)
    anchor, old = restore_physical_anchor(inputs.trees)
    with ExitStack() as stack:
        stack.enter_context(anchor)
        tables = REFINE.load_tables(args)
        context, words = BASE.checker_source_context()
        geometry = O.Geometry(context)
        bundle = stack.enter_context(C.FixedBundle(args, inputs.external_state(), words, tables, geometry))
        records = root_records(inputs, anchor, old, bundle)
        root_items = (("parent-layout.json", records.parent_layout), ("source.json", records.source),
            ("owner.json", records.owner), ("start.json", records.start), ("fixed/manifest.json", records.fixed),
            ("selection/start.json", records.selection_start))
        for name, value in root_items:
            if name in files.before:
                files.object(name, value)
        roots_complete = all(name in files.expected for name, _ in root_items)
        require(roots_complete or any(name in files.before for name in DIAGNOSTIC_TYPES), "partial_root_requires_explicit_diagnostic")
        for key, name in (("owner_sha256", "owner.json"), ("source_sha256", "source.json"),
                          ("start_sha256", "start.json"), ("selection_start_sha256", "selection/start.json")):
            if name in files.expected:
                report[key] = files.expected[name]["sha256"]
        if "start.json" in files.expected:
            report["anchor_completed_steps"] = anchor.completed_steps
        progress = ProgressAudit(files, records)
        require(roots_complete or progress.sequence < 0 and not progress.checkpoints and not progress.phase_sequences,
                "progress_after_all_immutable_root_metadata")
        state = BatchReductionState(anchor, anchor.completed_steps)
        progress.compare(state, 0, None, {}, None, {})
        report_progress(report, progress)

        def selection_done(sequence: int, hashes: dict[str, str], selection_sha: str | None, complete: bool) -> None:
            progress.compare(state, sequence, selection_sha, hashes, None, {}, complete)
            report["selection_phases_compared"] = list(hashes)
            if sequence == progress.sequence + 1:
                phase = SELECTION_PHASES[sequence - 1]
                formed = files.expected.get("selection/selection.json", {}).get("sha256")
                progress.tail_record(phase, None, hashes[phase], formed)
            report_progress(report, progress)
            boundary("completed_selection_phase", phase_number=sequence)

        selection = replay_selection(files, records, bundle, anchor, min(3, progress.phase_end), progress.sequence >= 3, selection_done)
        if "selection/selection.json" in files.expected:
            report["selection_sha256"] = files.expected["selection/selection.json"]["sha256"]
            report["selected_count"] = len(selection.witnesses)
        candidates: list[CandidateReplay] = []
        if progress.phase_end > 3:
            require(selection.metadata_complete, "candidate_phases_after_complete_selection_publication")
            candidate_count = (progress.phase_end - 3 + 5) // 6
            require(candidate_count <= len(selection.witnesses), "all_candidate_ordinals_belong_to_selected_roster")
            for ordinal in range(candidate_count):
                require(np.any(state.target), "no_candidate_phase_after_Linear")
                phase_count = min(6, progress.phase_end - 3 - 6 * ordinal)
                def candidate_done(number: int, hashes: dict[str, str], complete: bool,
                                   candidate: dict[str, Any] | None, row: dict[str, Any] | None) -> None:
                    sequence = 3 + 6 * ordinal + number
                    progress.compare(state, sequence, selection.sha256, selection.phases,
                        None if number == 6 and complete else ordinal, {} if number == 6 and complete else hashes, complete)
                    values = {item["ordinal"]: item for item in report["candidate_phases_compared"]}
                    values[ordinal] = {"ordinal": ordinal, "phases": list(hashes)}
                    report["candidate_phases_compared"] = [copy.deepcopy(values[index]) for index in sorted(values)]
                    if candidate is not None:
                        report["candidate_decisions_compared"] += 1
                    if row is not None:
                        report["accepted_rows_compared"] += 1
                    if sequence == progress.sequence + 1:
                        phase = CANDIDATE_PHASES[number - 1]
                        progress.tail_record(phase, ordinal, hashes[phase], selection.sha256, row, candidate)
                    report_progress(report, progress)
                    boundary("completed_candidate_phase", ordinal=ordinal, phase_number=number)
                item = replay_candidate(files, records, selection, bundle, state, ordinal, phase_count,
                                        3 + 6 * (ordinal + 1) <= progress.sequence, candidate_done)
                candidates.append(item)
        progress.complete()
        final = None
        if "final/manifest.json" in files.before:
            final = compare_final(files, records, selection, state, progress)
            report["final_manifest_sha256"] = sha(canonical(final.manifest))
            report["public_head_sha256"] = None if final.head is None else sha(canonical(final.head))
            report["public_final_compared"] = True
            report["terminal"] = final.terminal
        require("HEAD" not in files.before or final is not None and final.head is not None, "public_HEAD_after_full_final_comparison")
        complete_result = "result.json" in files.before
        require(not complete_result or final is not None and final.head is not None, "result_after_complete_public_final")
        invocations, by_sha = invocation_records(files, inputs, records, progress, final)
        diagnostic_terminal = compare_diagnostics(files, inputs, records, progress, final, by_sha)
        preservation = input_inventories(files, inputs, complete_result)
        if complete_result:
            produced = compare_producer_result(files, inputs, records, selection, state, candidates, final,
                                               invocations, by_sha, preservation)
            report["producer_result_sha256"] = sha(canonical(produced))
        elif final is not None:
            progress.tail = {"kind": "FINAL_PUBLICATION_TAIL", "phase": "final", "candidate_ordinal": None,
                "selection_sha256": selection.sha256, "phase_manifest_sha256": None, "row_manifest_sha256": None,
                "candidate_manifest_sha256": None, "checkpoint_sha256": None,
                "final_manifest_sha256": sha(canonical(final.manifest)),
                "public_head_sha256": None if final.head is None else sha(canonical(final.head)),
                "independently_compared": True, "published_by_checker": False}
        if not complete_result and any(name in files.before for name in DIAGNOSTIC_TYPES):
            report["terminal"] = diagnostic_terminal
        compare_candidate_roster(files, len(selection.witnesses))
        bundle.unchanged()
        inputs.unchanged()
        files.unchanged()
        report["input_preservation"] = preservation
        report["status"] = "PASS"
        report["partial"] = not complete_result
        report["candidate"] = complete_result
        report["all_completed_payloads_and_json_compared"] = True
        report["cross_checked"] = bool(report["selection_phases_compared"] or report["candidate_phases_compared"] or final is not None)
        report["durable_tail"] = copy.deepcopy(progress.tail)
        if final is not None and final.head is not None:
            # Actual physical HEAD is disclosed even if result publication was
            # interrupted.  The unchanged private counts still come from HEAD.
            report["lambda_sha256"] = final.head["lambda_sha256"]
        report["elapsed_seconds"] = time.monotonic() - STARTED
        boundary("all_saved_new_scope_compared", selected=report["selected_count"], processed=report["processed_candidates"], partial=report["partial"])
        return document("checker-result", report)


def complete_reduction_coefficients(state: BatchReductionState, decision: DecisionArithmetic) -> np.ndarray:
    """The immutable basis insertion order includes every zero coefficient."""
    coefficients = np.zeros(state.rank, dtype=np.uint8)
    previous = -1
    for event in decision.reductions:
        index = integer(event["pivot_id"], "reduction_pivot_id", 0, state.rank - 1)
        require(index > previous, "strict_reduction_insertion_order")
        previous = index
        pivot = state.pivots[index]
        require(event["offer"] == pivot["offer"] and event["lead"] == pivot["lead"] and
                event["physical_offset"] == index * ROW_BYTES == pivot["physical_offset"] and
                event["row_sha256"] == sha(state.row(index)), "reduction_exact_row_identity")
        coefficients[index] = integer(event["scalar"], "nonzero_reduction_scalar", 1, 2)
    return coefficients


def literal_signs(coefficients: np.ndarray, sigma: int | None, target_scalar: int | None) -> dict[str, Any]:
    require(coefficients.dtype == np.uint8 and coefficients.ndim == 1 and not np.any(coefficients > 2),
            "literal_all_basis_coefficients")
    if sigma is None:
        require(target_scalar is None, "dependent_literal_null_normalization_and_target")
    else:
        integer(sigma, "literal_sigma", 1, 2)
        scalar(target_scalar, "literal_target_scalar")
    return {"physical_factor_exponents": [-E.signed(int(value)) for value in coefficients],
            "normalized_outer_exponent": None if sigma is None else E.signed(sigma),
            "positive_correction_exponent": None if target_scalar is None else E.signed(target_scalar),
            "numerical_target_coefficient": target_scalar}


def rejected(operation: Callable[[], Any], label: str) -> None:
    try:
        operation()
    except (ValueError, KeyError, TypeError, AssertionError, IndexError):
        return
    raise ValueError("cycle_batch:missing_required_rejection:" + label)


def selector_canary() -> dict[str, Any]:
    """Full-sized synthetic array contract, not an accepted arithmetic parent."""
    edges = np.arange(CHORDS, dtype=np.uint32)
    tau = np.zeros((CHORDS, 5), dtype=np.uint8)
    basis = [11, 3, 19, 5, 27]
    tau[basis] = np.eye(5, dtype=np.uint8)
    tau[100] = [2, 0, 1, 0, 0]
    inverse = np.eye(5, dtype=np.uint8)
    values = np.zeros(CHORDS, dtype=np.uint8)
    values[100:140] = 1
    values[-1] = 2
    auxiliary = np.asarray([2, 1], dtype=np.uint8)
    result = select_all_residuals(edges, tau, values, basis, inverse, values.copy(), auxiliary)
    require(result["mode"] == "CHORD_BATCH" and result["failed_indices"].tolist() == list(range(100, 140)) + [CHORDS - 1] and
            result["failed_edges"].tolist() == result["failed_indices"].tolist() and
            [item["roster_index"] for item in result["candidates"]] == list(range(100, 132)),
            "canary_full_failure_roster_and_first32")
    require(all(len(item["witness"]["cycles"]) == 6 for item in result["candidates"]) and
            result["candidates"][0]["witness"]["basis_coefficients"] == [2, 0, 1, 0, 0] and
            any(item["coefficient"] == 0 for item in result["candidates"][0]["witness"]["cycles"]),
            "canary_six_cycles_keep_zero_basis_factors")
    wrong = values.copy(); wrong[-1] = 0
    rejected(lambda: select_all_residuals(edges, tau, values, basis, inverse, wrong, auxiliary), "full_tail_residual")
    rejected(lambda: select_all_residuals(edges[:-1], tau, values, basis, inverse, values, auxiliary), "chord_eof")
    no_chords = np.zeros(CHORDS, dtype=np.uint8)
    auxiliary_result = select_all_residuals(edges, tau, no_chords, basis, inverse, no_chords, auxiliary)
    require(auxiliary_result["mode"] == "AUXILIARY" and len(auxiliary_result["candidates"]) == 1 and
            auxiliary_result["candidates"][0]["witness"]["coordinate"] == 0 and
            auxiliary_result["candidates"][0]["witness"]["scalar"] == 2, "canary_first_auxiliary_fallback")
    zero = select_all_residuals(edges, tau, no_chords, basis, inverse, no_chords, np.zeros(2, dtype=np.uint8))
    require(zero["mode"] == "COMPLETE_ZERO_CANDIDATE" and zero["candidates"] == [], "canary_complete_current_zero")
    return {"name": "whole_chord_roster_first32_tail_and_auxiliary", "status": "PASS",
        "full_residual_count": CHORDS, "synthetic_array_fixture": True,
        "checks": ["all-failed-roster", "chord-before-aux", "first32-no-refill", "six-including-zero-coefficients",
                   "full-tail-mutation-rejected", "exact-EOF", "first-aux-fallback", "complete-current-zero"]}


def reduction_canary() -> dict[str, Any]:
    class FixtureAnchor:
        def __init__(self, first: int):
            self.rank, self.generation, self.head, self.kind = 0, 0, "0" * 64, "Separator"
            self.pivots: list[dict[str, Any]] = []
            self.parents = [{"role": "synthetic", "nested": {"value": 1}}]
            self.target = np.zeros(PHYSICAL, dtype=np.uint8)
            self.target[0], self.target[2] = first, 1
            self.functional = np.zeros(PHYSICAL, dtype=np.uint8)
            self.functional[0] = first

        def row(self, index: int) -> bytes:
            raise ValueError("empty_synthetic_anchor_has_no_row:" + str(index))

    def vector(a: int, b: int, c: int = 0) -> np.ndarray:
        value = np.zeros(PHYSICAL, dtype=np.uint8)
        value[:3] = [a, b, c]
        return value

    def commit(state: BatchReductionState, decision: DecisionArithmetic) -> None:
        number = state.processed_candidates
        state.advance(decision, None if decision.dependent else sha(canonical({"synthetic_row": number})),
                      None if decision.dependent else {"role": "synthetic-new", "ordinal": number},
                      None if decision.dependent else sha(canonical({"synthetic_manifest": number})))

    anchor = FixtureAnchor(1)
    state = BatchReductionState(anchor, 0)
    initial_parent = canonical(anchor.parents)
    first = state.reduce(vector(2, 0), 2)
    require(first.sigma == 2 and first.target_scalar == 1 and not first.dependent, "canary_sigma_two")
    first_signs = literal_signs(complete_reduction_coefficients(state, first), first.sigma, first.target_scalar)
    require(first_signs["normalized_outer_exponent"] == -1 and first_signs["positive_correction_exponent"] == 1,
            "canary_normalized_and_positive_correction_signs")
    commit(state, first)
    second = state.reduce(vector(1, 1), 1)
    require(second.remainder_scalar == 0 and not second.dependent and second.target_scalar == 0 and second.lead == 1,
            "canary_frozen_lambda_zero_independent_remainder")
    require(complete_reduction_coefficients(state, second).tolist() == [1], "canary_old_then_new_reduction")
    commit(state, second)
    dependent = state.reduce(vector(1, 2), 1)
    old_rank, old_generation, old_head, old_target = state.rank, state.generation, state.physical_head, pack(state.target)
    require(dependent.dependent and dependent.lead is dependent.sigma is dependent.target_scalar is None and
            not np.any(dependent.remainder), "canary_dependent_full_zero_and_nulls")
    require(complete_reduction_coefficients(state, dependent).tolist() == [1, 2] and
            literal_signs(np.asarray([1, 0, 2], dtype=np.uint8), 2, 2) == {
                "physical_factor_exponents": [-1, 0, 1], "normalized_outer_exponent": -1,
                "positive_correction_exponent": -1, "numerical_target_coefficient": 2},
            "canary_zero_factor_and_both_target_signs")
    commit(state, dependent)
    require((state.rank, state.generation, state.physical_head, pack(state.target)) ==
            (old_rank, old_generation, old_head, old_target), "canary_dependence_never_advances_physical_state")
    final = state.finish_arithmetic()
    require(final["kind"] == "Separator" and final["lambda"] is not None and final["lambda"][2] == 1 and
            final["direct_pairing"]["lambda_pivots"] == 0, "canary_one_final_all_rows_separator")
    linear = state.reduce(vector(1, 0, 1), 1)
    commit(state, linear)
    require(state.finish_arithmetic() == {"kind": "LinearMembershipCandidate", "lambda": None,
                                         "separator": None, "direct_pairing": None}, "canary_early_linear_typed_null")
    rejected(lambda: state.reduce(vector(1, 0), 1), "no_candidate_after_linear")
    two = BatchReductionState(FixtureAnchor(2), 0)
    theta_two = two.reduce(vector(1, 0), 2)
    require(theta_two.target_scalar == 2 and np.array_equal(theta_two.target_after, vector(0, 0, 1)),
            "canary_actual_target_theta_two_subtraction")
    require(canonical(anchor.parents) == initial_parent, "canary_parent_metadata_not_aliased")
    wrong = bytearray(pack(vector(1, 0))); wrong[-1] = 81
    rejected(lambda: packed_vector(bytes(wrong), PHYSICAL, "canary_wrong_packed"), "packed_range")
    rejected(lambda: packed_vector(pack(vector(1, 0)) + b"\0", PHYSICAL, "canary_tail"), "packed_EOF")
    return {"name": "actual_reduction_dependence_signed_target_and_finalizer", "status": "PASS",
        "synthetic_sparse_physical_fixture": True, "physical_width": PHYSICAL,
        "checks": ["sigma-two", "selection-lambda-zero-independent", "dependent-null-no-advance",
                   "all-zero-factors-retained", "target-subtraction-theta-one-and-two", "correction-positive-sign",
                   "one-final-separator-all-rows", "early-linear-null", "packed-range-and-EOF"]}


def publication_canary() -> dict[str, Any]:
    """Real private serializers and read-only replay, with an explicit fixture.

    Earlier phase bodies are empty protocol fixtures.  The reduction payloads,
    target, normalized row, row/decision/checkpoint and HEAD are produced by the
    actual new helpers.  This is not a successful accepted-parent oracle run.
    """
    class FixtureAnchor:
        rank, generation, head, kind = 0, 0, "0" * 64, "Separator"
        def __init__(self) -> None:
            self.pivots = []
            self.parents = [{"role": "fixture", "identity": {"value": 1}}]
            self.target = np.zeros(PHYSICAL, dtype=np.uint8)
            self.target[[0, 2]] = 1
            self.functional = np.zeros(PHYSICAL, dtype=np.uint8)
            self.functional[0] = 1
        def row(self, index: int) -> bytes:
            raise ValueError("empty_fixture_anchor:" + str(index))

    anchor = FixtureAnchor()
    state = BatchReductionState(anchor, 0)
    records = RootRecords(document("parent-layout", {"fixture": True}), document("source", {"fixture": True}),
        document("owner", {"fixture": True}), document("start", {"fixture": True, "accepted_target_derivation_parents": state.parents}),
        document("fixed-manifest", {"fixture": True}), document("selection-start", {"fixture": True}))
    immutable_start = canonical(records.start)
    selection_sha, witness_sha, view_sha = (sha(canonical({"fixture": name})) for name in ("selection", "witness", "view"))
    raw = np.zeros(PHYSICAL, dtype=np.uint8); raw[0] = 2
    decision = state.reduce(raw, 2)
    payloads, objects = reduction_payloads(state, decision, 0, selection_sha, witness_sha, "1" * 64, "2" * 64)
    with tempfile.TemporaryDirectory(prefix="r07-batch-checker-interface-") as temporary:
        root = Path(temporary)
        def write(name: str, data: bytes) -> None:
            relative_name(name, "fixture_relative_path")
            target = root / name
            require(root.resolve() in target.resolve().parents, "fixture_write_containment")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        def save_phase(prefix: str, phase: str, data: dict[str, tuple[bytes, str, Any]], previous: str | None,
                       ordinal: int | None) -> tuple[str, dict[str, Any]]:
            measurement = document("phase-telemetry", {"phase": phase, "elapsed_seconds": 0.0,
                "process_ru_maxrss_kib": 1, "proc_io_before": None, "proc_io_after": None,
                "payload_bytes": sum(len(item[0]) for item in data.values()),
                "measurement_scope": "process-cumulative-rusage-and-proc-io;payload-bytes-are-output-only", "eof": True})
            complete = {**data, "telemetry.json": O.json_payload(measurement)}
            manifest = document("phase-manifest", {**records.binding(), "selection_sha256": None if ordinal is None else selection_sha,
                "candidate_ordinal": ordinal, "witness_sha256": None if ordinal is None else witness_sha, "phase": phase,
                "previous_phase_manifest_sha256": previous, "files": payload_roster(complete), "eof": True})
            for name, item in complete.items():
                write(prefix + "/" + name, item[0])
            write(prefix + "/manifest.json", canonical(manifest))
            return sha(canonical(manifest)), measurement
        checkpoints: list[dict[str, Any]] = []
        selection_phases: dict[str, str] = {}
        candidate_phases: dict[str, str] = {}
        def save_checkpoint(sequence: int, source_state: BatchReductionState) -> dict[str, Any]:
            item = checkpoint_record(records, source_state, sequence,
                None if not checkpoints else sha(canonical(checkpoints[-1])), None if sequence < 3 else selection_sha,
                selection_phases, 0 if 4 <= sequence <= 8 else None, candidate_phases if 4 <= sequence <= 8 else {})
            checkpoints.append(item)
            write("progress/checkpoints/" + sha(canonical(item)) + ".json", canonical(item))
            return item
        save_checkpoint(0, state)
        for sequence, phase in enumerate(SELECTION_PHASES, 1):
            previous = None if sequence == 1 else selection_phases[SELECTION_PHASES[sequence - 2]]
            selection_phases[phase], _ = save_phase("selection/" + phase, phase, {}, previous, None)
            save_checkpoint(sequence, state)
        for number, phase in enumerate(CANDIDATE_PHASES[:-1], 1):
            previous = view_sha if number == 1 else candidate_phases[CANDIDATE_PHASES[number - 2]]
            candidate_phases[phase], _ = save_phase("candidates/000000/e/" + phase, phase, {}, previous, 0)
            save_checkpoint(3 + number, state)
        candidate_phases["reduction"], _ = save_phase("candidates/000000/reduction", "reduction", payloads, candidate_phases["B"], 0)
        row = accepted_row_record(records, state, decision, 0, selection_sha, candidate_phases["reduction"], payloads, objects)
        candidate = candidate_decision_record(records, state, 0, selection_sha, witness_sha, view_sha, candidate_phases,
                                             objects, sha(canonical(row)))
        for name in ("physical-normalized.bin", "instruction.json", "target.json"):
            write("rows/000000/" + name, payloads[name][0])
        write("rows/000000/manifest.json", canonical(row))
        write("candidates/000000/manifest.json", canonical(candidate))
        preview = copy.deepcopy(state)
        preview.advance(decision, objects["instruction"]["rolling_sha256"], batch_target_parent(row, objects), sha(canonical(row)))
        preview.decisions.append(copy.deepcopy(candidate))
        save_checkpoint(9, preview)
        write("progress/HEAD", canonical(progress_head_record(checkpoints[8])))
        files = CandidateFiles(root)
        audit = ProgressAudit(files, records)
        audit.compare(state, 0, None, {}, None, {})
        for sequence in range(1, 9):
            prefix, phase, ordinal = phase_at_sequence(sequence)
            if ordinal is None:
                previous = None if sequence == 1 else selection_phases[SELECTION_PHASES[sequence - 2]]
                compare_phase(files, prefix, phase, {}, records, previous)
            else:
                number = sequence - 3
                previous = view_sha if number == 1 else candidate_phases[CANDIDATE_PHASES[number - 2]]
                compare_phase(files, prefix, phase, {}, records, previous, selection_sha, 0, witness_sha)
            audit.compare(state, sequence, None if sequence < 3 else selection_sha,
                {key: selection_phases[key] for key in SELECTION_PHASES[:min(sequence, 3)]},
                0 if sequence >= 4 else None,
                {key: candidate_phases[key] for key in CANDIDATE_PHASES[:sequence - 3]} if sequence >= 4 else {})
        reduction_sha, _ = compare_phase(files, "candidates/000000/reduction", "reduction", payloads,
                                        records, candidate_phases["B"], selection_sha, 0, witness_sha)
        actual_candidate, actual_row, published = compare_candidate_publication(files, records, state, decision, 0,
            selection_sha, witness_sha, view_sha, candidate_phases, payloads, objects, False)
        require(published and actual_row is not None, "canary_complete_durable_reduction_metadata")
        audit.compare(state, 9, selection_sha, selection_phases, None, {})
        audit.tail_record("reduction", 0, reduction_sha, selection_sha, actual_row, actual_candidate)
        audit.complete()
        report = checker_receipt_template()
        report_progress(report, audit)
        require(state.rank == 1 and state.processed_candidates == 1 and report["rank"] == 0 and report["processed_candidates"] == 0 and
                report["accepted_new_rows"] == 0 and audit.tail["candidate_manifest_sha256"] == sha(canonical(candidate)) and
                audit.tail["published_by_checker"] is False and not (root / "HEAD").exists(), "canary_tail_never_promotes_HEAD_counts")
        incomplete_selection = SelectionReplay(selection_phases, {}, None, [{}], {"fixture": True}, [], True)
        rejected(lambda: compare_final(files, records, incomplete_selection, state, audit), "no_public_final_flush_before_private_HEAD")
        require(canonical(records.start) == immutable_start, "canary_start_deepcopy_survives_actual_append")
        state.parents[0]["identity"]["value"] = 2
        require(records.start["accepted_target_derivation_parents"][0]["identity"]["value"] == 1 and
                anchor.parents[0]["identity"]["value"] == 1, "canary_deep_parent_isolation")
        prior_committed = canonical(audit.committed)
        state.target[2] = 2
        require(canonical(audit.committed) == prior_committed, "canary_checkpoint_isolation_after_advance")
        bad_records = copy.deepcopy(records)
        bad_records.owner = document("owner", {"fixture": "wrong-owner"})
        rejected(lambda: ProgressAudit(CandidateFiles(root), bad_records).compare(BatchReductionState(anchor, 0), 0, None, {}, None, {}),
                 "fully_resealed_wrong_owner")
        write("candidates/000001/e/raw/manifest.json", canonical({"fixture": True}))
        rejected(lambda: ProgressAudit(CandidateFiles(root), records), "two_phases_ahead")
        (root / "candidates/000001/e/raw/manifest.json").unlink()
        prefix0 = "progress/checkpoints/" + sha(canonical(checkpoints[0])) + ".json"
        original0 = (root / prefix0).read_bytes()
        (root / prefix0).unlink()
        rejected(lambda: ProgressAudit(CandidateFiles(root), records), "checkpoint_hole")
        write(prefix0, original0)
        write("candidates/000000/reduction/target-remainder.bin", payloads["target-remainder.bin"][0] + b"\0")
        rejected(lambda: files.compare("candidates/000000/reduction/target-remainder.bin", payloads["target-remainder.bin"][0]), "payload_tail_EOF")
        write("candidates/000000/reduction/target-remainder.bin", payloads["target-remainder.bin"][0])
        bad_body = {key: copy.deepcopy(value) for key, value in checkpoints[8].items() if key not in ("schema", "sha256")}
        bad_body["processed_candidates"] = 1
        bad_head = progress_head_record(document("checkpoint", bad_body))
        write("progress/HEAD", canonical(bad_head))
        rejected(lambda: ProgressAudit(CandidateFiles(root), records), "fully_resealed_HEAD_checkpoint_reset")
    # Task1011 exercises the actual metadata consumers with small protocol
    # documents.  This fixture does not claim a successful accepted oracle or
    # public finalizer, and does not add an invocation to any real packet.
    with tempfile.TemporaryDirectory(prefix="r07-batch-checker-history-") as temporary:
        root = Path(temporary)
        def save(name: str, data: bytes) -> None:
            relative_name(name, "history_fixture_relative_path")
            target = root / name
            require(root.resolve() in target.resolve().parents, "history_fixture_write_containment")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        registration = registered_limits(argparse.Namespace(producer_max_seconds=5400, producer_max_memory_mib=7168,
                                                             max_seconds=10800, max_memory_mib=7168))
        portable = {"schema": SCHEMA + ".acceptance", "parents": [{"role": role} for role in PARENT_ROLES],
            "anchor": {"fixture": True}, "code": {"fixture": True}, "runtime": {"fixture": True},
            "registration": registration}
        host = {"parents": {role: str((root / "fixture-parents" / role).resolve()) for role in PARENT_ROLES},
                "acceptance": str((root / "fixture-acceptance.json").resolve()), "output": str(root.resolve())}
        acceptance = copy.deepcopy(portable)
        for parent in acceptance["parents"]:
            parent["path"] = host["parents"][parent["role"]]
        fixture_inputs = argparse.Namespace(value=acceptance, portable=portable, portable_sha256=sha(canonical(portable)))
        def invocation(nonce: str, resume: bool = True) -> dict[str, Any]:
            return document("invocation", {"id": nonce, **records.binding(),
                "portable_acceptance_sha256": fixture_inputs.portable_sha256, "acceptance_sha256": sha(canonical(acceptance)),
                "registration": registration, "resume": resume, "batch_size": BATCH_SIZE, "max_batches": 1,
                **registration["producer_limits"], "progress_head_before_sha256": None, "physical_head_before_sha256": None,
                "processed_candidates_before": 0, "accepted_new_rows_before": 0, "started_utc": "2000-01-01T00:00:00Z",
                "launch": {"run": 1, "attempt": 1, "head": "0" * 40, "workflow": ".github/workflows/fixture.yml"},
                "host_paths": host})
        def reseal(value: dict[str, Any], **changes: Any) -> dict[str, Any]:
            body = {key: copy.deepcopy(item) for key, item in value.items() if key not in ("schema", "sha256")}
            body.update(changes)
            return document(value["schema"].removeprefix(SCHEMA + "."), body)
        def history() -> tuple[CandidateFiles, ProgressAudit, list[dict[str, Any]], dict[str, dict[str, Any]]]:
            saved = CandidateFiles(root)
            progress = ProgressAudit(saved, records)
            if progress.sequence == 0:
                progress.compare(BatchReductionState(FixtureAnchor(), 0), 0, None, {}, None, {})
            descriptors, values = invocation_records(saved, fixture_inputs, records, progress, None)
            return saved, progress, descriptors, values
        pending = "invocations/." + "f" * 32 + ".json.pending-" + "e" * 32
        save(pending, b'{"partial":')
        saved, _, descriptors, values = history()
        require(descriptors == [] and values == {} and pending not in saved.expected, "canary_pending_new_nonce_is_not_an_invocation")
        compare_candidate_roster(saved, 0)
        saved.unchanged()
        first, second = invocation("1" * 32), invocation("2" * 32)
        first_name, second_name = "invocations/" + first["id"] + ".json", "invocations/" + second["id"] + ".json"
        save(first_name, canonical(first))
        _, _, descriptors, values = history()
        require(len(descriptors) == 1 and all(value["resume"] is True for value in values.values()), "canary_zero_fresh_one_bootstrap")
        save(second_name, canonical(second))
        saved, _, descriptors, values = history()
        require(len(descriptors) == 2 and all(value["resume"] is True for value in values.values()) and
                not (root / ("invocations/" + "f" * 32 + ".json")).exists(), "canary_multiple_bootstraps_without_pending_normal_nonce")
        compare_candidate_roster(saved, 0)
        saved.unchanged()
        for key in ("processed_candidates_before", "accepted_new_rows_before"):
            save(first_name, canonical(reseal(first, **{key: False})))
            rejected(history, "bootstrap_boolean_before_count")
        save(first_name, canonical(reseal(first, resume=False)))
        save(second_name, canonical(reseal(second, resume=False)))
        rejected(history, "two_fresh_invocations")
        (root / first_name).unlink()
        (root / second_name).unlink()
        checkpoint = checkpoint_record(records, BatchReductionState(FixtureAnchor(), 0), 0, None, None, {}, None, {})
        checkpoint_name = "progress/checkpoints/" + sha(canonical(checkpoint)) + ".json"
        save(checkpoint_name, canonical(checkpoint))
        rejected(history, "zero_normal_invocations_after_checkpoint_formation")
        save("progress/HEAD", canonical(progress_head_record(checkpoint)))
        rejected(history, "zero_normal_invocations_after_progress_HEAD")
        save(first_name, canonical(first))
        save(second_name, canonical(second))
        _, _, descriptors, values = history()
        require(len(descriptors) == 2 and all(value["progress_head_before_sha256"] is None for value in values.values()),
                "canary_early_bootstrap_nulls_survive_later_HEAD")
        metadata = {"parent-layout.json": records.parent_layout, "source.json": records.source, "owner.json": records.owner,
            "start.json": records.start, "fixed/manifest.json": records.fixed, "selection/start.json": records.selection_start,
            "selection/selection.json": document("selection", {"fixture": True})}
        for name, value in metadata.items():
            save(name, canonical(value))
        root_keys = ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")
        count_keys = ("processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation")
        binding_keys = (*root_keys, "selection_sha256", "invocation_sha256", "progress_head_sha256", "checkpoint_sha256",
                        "public_head_sha256", "final_manifest_sha256")
        diagnostic_fields = {"phase": "fixture-metadata", "reason": "registered-stop-fixture", "partial": True,
            **{key: None for key in (*binding_keys, *count_keys)}, **registration["producer_limits"], "elapsed_seconds": 0.0,
            "candidate": False, "cross_checked": False, "verified": False}
        stopped = document("resource-stop", {**diagnostic_fields, "status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE"})
        failed = document("rejected", {**diagnostic_fields, "status": "FAIL", "terminal": "REJECTED",
            **{key: records.binding()[key] for key in root_keys},
            "selection_sha256": sha(canonical(metadata["selection/selection.json"])), "invocation_sha256": sha(canonical(second)),
            "checkpoint_sha256": sha(canonical(checkpoint)), "progress_head_sha256": sha(canonical(progress_head_record(checkpoint))),
            **{key: checkpoint[key] for key in count_keys}})
        def diagnostics() -> tuple[CandidateFiles, str | None]:
            current_files, progress, _, by_sha = history()
            for name, value in metadata.items():
                if name in current_files.before:
                    current_files.object(name, value)
            terminal = compare_diagnostics(current_files, fixture_inputs, records, progress, None, by_sha)
            return current_files, terminal
        save("resource-stop.json", canonical(stopped))
        saved, terminal = diagnostics()
        require(terminal == "UNKNOWN_RESOURCE", "canary_single_resource_diagnostic_terminal")
        save("rejected.json", canonical(failed))
        saved, terminal = diagnostics()
        require(terminal is None and all(name in saved.expected for name in DIAGNOSTIC_TYPES) and
                all(saved.json("resource-stop.json")[key] is None for key in (*binding_keys, *count_keys)),
                "canary_both_diagnostics_and_early_null_history")
        compare_candidate_roster(saved, 0)
        saved.unchanged()
        (root / "resource-stop.json").unlink()
        _, terminal = diagnostics()
        require(terminal == "REJECTED", "canary_single_rejected_diagnostic_terminal")
        save("resource-stop.json", canonical(stopped))
        for name, own, other in (("resource-stop.json", stopped, failed), ("rejected.json", failed, stopped)):
            save(name, canonical(other))
            rejected(diagnostics, "diagnostic_filename_schema_swap")
            save(name, canonical(reseal(own, status=other["status"], terminal=other["terminal"])))
            rejected(diagnostics, "diagnostic_filename_status_swap")
            save(name, canonical(own))
        for key in binding_keys:
            save("rejected.json", canonical(reseal(failed, **{key: "9" * 64})))
            rejected(diagnostics, "diagnostic_nonnull_binding_tamper:" + key)
        for key in count_keys:
            save("rejected.json", canonical(reseal(failed, **{key: checkpoint[key] + 1})))
            rejected(diagnostics, "diagnostic_saved_count_tamper:" + key)
        save("rejected.json", canonical(reseal(failed, progress_head_sha256=None, checkpoint_sha256=None)))
        rejected(diagnostics, "diagnostic_null_progress_with_formed_counts")
        save("rejected.json", canonical(failed))
        (root / "owner.json").unlink()
        rejected(diagnostics, "diagnostic_nonnull_binding_to_unformed_root")
        save("owner.json", canonical(records.owner))
        saved, terminal = diagnostics()
        _, _, after_descriptors, _ = history()
        require(terminal is None and len(after_descriptors) == 2,
                "canary_diagnostic_history_does_not_change_normal_invocations")
        compare_candidate_roster(saved, 0)
        saved.unchanged()
    return {"name": "private-prefix-publication-resume-and-isolation", "status": "PASS", "rejected_cases": [
        "no-public-final-flush-before-private-HEAD", "fully-resealed-wrong-owner", "two-phases-ahead", "checkpoint-hole",
        "payload-tail-EOF", "fully-resealed-HEAD-checkpoint-reset", "two-fresh-invocations", "bootstrap-boolean-before-count",
        "zero-normal-invocations-after-checkpoint-or-HEAD", "diagnostic-filename-schema-or-status-swap",
        "diagnostic-nonnull-binding-tamper", "diagnostic-saved-count-tamper", "diagnostic-null-progress-with-counts",
        "diagnostic-nonnull-binding-to-unformed-root"]}


def selftest() -> dict[str, Any]:
    first, second = selector_canary(), reduction_canary()
    third = publication_canary()
    tests = [{"name": "fixed-selection-full-roster-and-aux", "status": first["status"],
              "rejected_cases": ["full-tail-residual", "chord-EOF"]},
             {"name": "dependent-independent-target-signs-and-packed", "status": second["status"],
              "rejected_cases": ["no-candidate-after-Linear", "packed-range", "packed-EOF"]}, third]
    return document("selftest", {"status": "PASS", "tests": tests,
        "fixture_scope": "full-sized-synthetic-chord-arrays;sparse-physical-rows;empty-predecessor-phase-protocol-fixtures;bootstrap-and-diagnostic-metadata;no-accepted-parent-run",
        "production_interfaces_used": ["select_all_residuals", "BatchReductionState.reduce", "BatchReductionState.advance",
            "BatchReductionState.finish_arithmetic", "complete_reduction_coefficients", "reduction_payloads", "compare_phase",
            "compare_candidate_publication", "checkpoint_record", "progress_head_record", "ProgressAudit", "report_progress", "compare_final",
            "invocation_records", "compare_diagnostic", "compare_diagnostics", "compare_candidate_roster"],
        "old_success_suites": 0, "actual_anchor_arithmetic_replayed": False, "candidate": False, "cross_checked": False, "verified": False})


def positive_integer(value: str) -> int:
    require(re.fullmatch(r"[1-9][0-9]*", value) is not None, "CLI_positive_ordinary_integer")
    return int(value)


def output_location(args: argparse.Namespace) -> None:
    require(args.output is not None and not args.output.is_symlink(), "separate_checker_report_file")
    output = args.output.resolve()
    roots = [args.candidate_root, *args.block_root] + [getattr(args, role.replace("-", "_") + "_root")
             for role in PARENT_ROLES if not role.startswith("block-")]
    for root in roots:
        if root is not None:
            resolved = root.resolve()
            require(output != resolved and resolved not in output.parents, "checker_never_writes_candidate_or_parent_tree")
    require(output != args.acceptance.resolve() and REPOSITORY / "search" not in output.parents and
            REPOSITORY / ".github" not in output.parents and REPOSITORY / "scratchpad" not in output.parents,
            "checker_report_outside_acceptance_and_executable_inputs")
    for parent in args.output.parents:
        require(not parent.is_symlink(), "checker_report_parent_not_symlink")


def main() -> int:
    global STARTED, DEADLINE, MAX_RSS_BYTES
    parser = argparse.ArgumentParser(description=__doc__)
    for role in PARENT_ROLES:
        if not role.startswith("block-"):
            parser.add_argument("--" + role + "-root", type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--acceptance", type=Path)
    parser.add_argument("--candidate-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-seconds", type=positive_integer)
    parser.add_argument("--max-memory-mib", type=positive_integer, default=7168)
    parser.add_argument("--producer-max-seconds", type=positive_integer, default=5400)
    parser.add_argument("--producer-max-memory-mib", type=positive_integer, default=7168)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    STARTED = time.monotonic()
    if args.max_seconds is None:
        args.max_seconds = 300 if args.selftest else 10800
    DEADLINE, MAX_RSS_BYTES = STARTED + args.max_seconds, args.max_memory_mib << 20
    def interrupted(signum: int, frame: Any) -> None:
        raise ResourceStop("signal-" + str(signum) + ":" + LAST_PHASE)
    signal.signal(signal.SIGINT, interrupted)
    signal.signal(signal.SIGTERM, interrupted)
    def retained_progress(phase: str, **fields: Any) -> None:
        boundary("retained:" + phase, **fields)
    modules = (C, E, O, E.ORACLE, REFINE, C.FIXED, L, L.ROOTS, BASE)
    for module in modules:
        for name in ("boundary", "progress"):
            if hasattr(module, name):
                setattr(module, name, retained_progress)
    report = checker_receipt_template()
    report_output_safe = False
    exit_code = 0
    try:
        if args.selftest:
            require(args.output is None and args.acceptance is None and args.candidate_root is None,
                    "selftest_stdout_only_and_no_real_candidate")
            result = selftest()
        else:
            require(all(getattr(args, role.replace("-", "_") + "_root") is not None for role in PARENT_ROLES if not role.startswith("block-")) and
                    len(args.block_root) == 4 and args.acceptance is not None and args.candidate_root is not None,
                    "all_fifteen_roots_and_exact_acceptance")
            output_location(args)
            report_output_safe = True
            result = check_actual(args, report)
    except BaseException as error:
        resources = tuple({ResourceStop, MemoryError, *(getattr(module, "ResourceStop") for module in modules if hasattr(module, "ResourceStop"))})
        resource_failure = isinstance(error, resources)
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            resource_failure = True
        exit_code = 3 if resource_failure else 1
        print(json.dumps({"status": "UNKNOWN_RESOURCE" if resource_failure else "FAIL", "phase": LAST_PHASE,
            "reason": type(error).__name__ + ":" + str(error), "checked_cursor": copy.deepcopy(CHECKED_CURSOR)}, sort_keys=True),
            file=sys.stderr, flush=True)
        report.update({"status": "UNKNOWN_RESOURCE" if resource_failure else "FAIL", "terminal": "UNKNOWN_RESOURCE" if resource_failure else "REJECTED",
            "partial": True, "all_completed_payloads_and_json_compared": False, "candidate": False, "cross_checked": False,
            "elapsed_seconds": time.monotonic() - STARTED})
        result = document("checker-result", report)
    raw = canonical(result)
    if report_output_safe:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
    sys.stdout.buffer.write(raw)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
