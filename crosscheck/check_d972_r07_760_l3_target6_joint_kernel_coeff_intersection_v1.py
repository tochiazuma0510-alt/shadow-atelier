#!/usr/bin/env python3
"""Helper-nonshared checker for task-169 joint coefficient receipts.

This checker never imports the task-169 producer.  It rebuilds the frozen
finite quotient objects from the pinned task-157ee/task-168 foundations,
constructs the three presentation layers and every Delta conjugate again,
performs its own Schreier rewriting and F3 elimination, and then checks any
completed-j affine intersection and selected relation word.  A positive D2
statement remains conditional on the independently authenticated task-168
append-only checkpoint chain.
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
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path(
    "crosscheck/check_d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py")
PRODUCER_PATH = Path(
    "search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py")
DEFAULT_RECEIPT = Path(
    "search/certs/d972_r07_760_l3_target6_joint_kernel_coeff_"
    "intersection_preflight_v1_20260827.json")
DEFAULT_OUTPUT = Path(
    "ci/out/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_check_v1.json")
DEFAULT_CHECKPOINT_DIR = Path(
    "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoints")
COEFF_PATH = Path(
    "search/d972_r07_760_l3_target6_legal_coefficients_v1.py")
JOINT_PATH = Path("search/d972_b345_joint_kernel_qstar_closure_v1.py")
JOINT_RECEIPT_PATH = Path(
    "ci/b345_157ee_artifacts_32359956713/"
    "d972_b345_joint_kernel_qstar_closure_v1.json")
Q3_PATH = Path(
    "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json")

SCHEMA = "d972-r07-760-l3-target6-joint-kernel-coeff-intersection-check/v1"
TARGET_SCHEMA = "d972-r07-760-l3-target6-joint-kernel-coeff-intersection/v1"
DOMAIN_SCHEMA = "d972-r07-registered-joint-value-exp3-domain/v1"
PREFLIGHT_STATE = "R07_760_JOINT_COEFF_INTERSECTION_V1_PREFLIGHT_READY"
FINAL_MARKER = "R07_760_JOINT_COEFF_INTERSECTION_V1_CHECKER_PASS"
N_SCHREIER = 28
N_DELTA = 27
RELATION_COUNTS = {"gamma_cayley_edge": 6318,
                   "xy_action": 104, "q0_factor": 19}
TOTAL_RELATIONS = 6441
TOTAL_RS_ROWS = 173907
MAX_DOMAIN_SECONDS = 600.0
MAX_GHA_DOMAIN_SECONDS = 5400.0
LEGACY_CANARY_GLOBAL_ORDINALS = tuple(sorted(
    {1, 6318, 6319, 6422, 6423, 6441} |
    set(range(257, TOTAL_RELATIONS + 1, 257))))
LEGACY_CANARY_COUNT = 31
CONTEXT_ROWS_SHA = (
    "bf07578f91f5ed66e6ddddd4ef83dafa45817a29df066940bbc13bd53cdd00f6")
ALIAS_ROWS_SHA = (
    "15cdac950ede8ce4596e5014ae1b6d0caa28523898cb42f3387f435a11b919a8")
RECORD_WORDS_SHA = (
    "08d11c68dcbacc1b81e5e2732eedcbc41df82a16c8a0f97dfbbb13d6accee24f")
COMPLETE_RELATORS_SHA = (
    "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a")
TARGET_ALIAS_IDS = {
    "correction_coface_0": 1, "hexagon_1_fxy_0": 1,
    "hexagon_1_fxz_0": 2, "hexagon_1_fyz_0": 3,
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
FALSE_CLAIMS = {"actual_A18_lift": False, "fake": False,
                "cofinal_lift": False, "Ihara_witness": False}
TERMINALS = {
    "R07_760_JOINT_COEFF_INTERSECTION_NONEMPTY",
    "R07_760_JOINT_COEFF_INTERSECTION_EMPTY",
    "R07_760_JOINT_COEFF_UNKNOWN_RESOURCE",
    "R07_760_JOINT_COEFF_INPUT_STOP",
}

# Frozen task-169b exact-transition producer.
PRODUCER_BYTES = 111249
PRODUCER_SHA = "f7d80db6197224b2096d8034e2bccc7f3f62956cc0454727156652131cfaf0c7"
COEFF_BYTES = 57792
COEFF_SHA = "7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962"
JOINT_BYTES = 67945
JOINT_SHA = "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"
JOINT_RECEIPT_BYTES = 2166036
JOINT_RECEIPT_SHA = (
    "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df")
Q3_BYTES = 231570
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_domain_seconds(value: float) -> float:
    require(type(value) is float and math.isfinite(value) and
            0.0 < value <= MAX_GHA_DOMAIN_SECONDS,
            "checker domain-seconds finite positive and at most 5400")
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


def load_module(name: str, path: Path, digest: str) -> Any:
    require(name not in sys.modules and digest_file(ROOT / path) == digest,
            "independent module pin " + path.as_posix())
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None, "module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def authenticate_sources() -> dict[str, Any]:
    specs = {
        "producer": (PRODUCER_PATH, PRODUCER_BYTES, PRODUCER_SHA),
        "task169": (Path(
            "sol/luna_task_169_r07_joint_kernel_coeff_intersection_v1.md"),
            10445,
            "6223245e9e3ec7476b5b0c55631d7bcea254c7890c5220f2b5866b9f31b22fa7"),
        "proof107": (Path(
            "sol/proof_r07_joint_kernel_coefficient_intersection_v107.md"),
            9359,
            "81f83d16abac3a8ffa59b6747b4b36e10796f353916ee4078c8c29c2ad2b07cd"),
        "proof108_read_not_consumed": (Path(
            "sol/proof_pb4_eleven_relator_presentation_equality_v108.md"),
            6742,
            "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
        "proof109_read_not_consumed": (Path(
            "sol/proof_r07_full_e4_joint_orbit_selector_v109.md"),
            11228,
            "3224f0be545ac1ffe1d3c674087b30f55c0eb97fda0bd7702eb5f85b768255f0"),
        "task168_producer": (COEFF_PATH, COEFF_BYTES, COEFF_SHA),
        "task168": (Path(
            "sol/luna_task_168_r07_jennings_legal_coefficients_v1.md"),
            7262,
            "4d85fd8f9ec69a618828c06498aa22922cf5372e21d10ed65280ca2468f5b7f1"),
        "reply168": (Path(
            "sol/luna_reply_168_r07_jennings_legal_coefficients_v1.md"),
            10692,
            "d22bed5ee8331fd5eb1d84256813699d0985df5a5bdf9a31152fdc448f847940"),
        "task168_checker": (Path(
            "crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py"),
            49633,
            "a54383185601e8251b7cbac87b6c57f89d3a8df8519cb93014b08a3893825e25"),
        "task168_driver": (Path(
            "search/d972_r07_760_l3_target6_legal_coefficients_gha_driver_v1.g"),
            19176,
            "bad7911b0958983aacd541bb682b0f14a2903de02cecfc01043b593b17ab1e16"),
        "task168_preflight": (Path(
            "search/certs/d972_r07_760_l3_target6_legal_coefficients_preflight_v1_20260827.json"),
            6833,
            "f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138"),
        "task157ee_producer": (JOINT_PATH, JOINT_BYTES, JOINT_SHA),
        "task157ee": (Path(
            "sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md"),
            11226,
            "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"),
        "reply157ee": (Path(
            "sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md"),
            4118,
            "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee"),
        "task157ef": (Path(
            "sol/luna_task_157ef_b345_joint_kernel_checker_repair.md"),
            3235,
            "e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed"),
        "reply157ef": (Path(
            "sol/luna_reply_157ef_b345_joint_kernel_checker_repair.md"),
            4541,
            "71ba794479eea934c6ae06d94333f890983e53c909813dd17bab26039bce80e0"),
        "task157ef_checker_v2": (Path(
            "search/check_d972_b345_joint_kernel_qstar_closure_v2.py"),
            5942,
            "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
        "task157ef_driver_v2": (Path(
            "search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g"),
            3912,
            "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"),
        "task157ee_full_receipt": (
            JOINT_RECEIPT_PATH, JOINT_RECEIPT_BYTES, JOINT_RECEIPT_SHA),
        "task157ee_q3_input": (Q3_PATH, Q3_BYTES, Q3_SHA),
    }
    rows = {}
    for label, (path, size, digest) in specs.items():
        full = ROOT / path
        require(full.is_file() and full.stat().st_size == size and
                digest_file(full) == digest,
                "checker authenticated source " + label)
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter in (-2, -1, 1, 2), "checker F2 alphabet")
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


def substitute(relator: Sequence[int], left: Sequence[int],
               right: Sequence[int]) -> list[int]:
    out: list[int] = []
    for letter in relator:
        word = left if abs(letter) == 1 else right
        append_reduced(out, word if letter > 0 else inv_word(word))
    return out


def complete_relators_independent(joint: Any) -> list[list[int]]:
    p_rows = [substitute(row, joint.SPLIT_WORDS[0], joint.SPLIT_WORDS[1])
              for row in joint.P_RELATORS]
    g_rows = [substitute(row, joint.SPLIT_WORDS[2], joint.SPLIT_WORDS[3])
              for row in joint.G9_RELATORS]
    def commutator(a: Sequence[int], b: Sequence[int]) -> list[int]:
        return reduce_word(inv_word(a) + inv_word(b) + list(a) + list(b))
    cross = [commutator(a, b) for a in joint.SPLIT_WORDS[:2]
             for b in joint.SPLIT_WORDS[2:]]
    split = [
        reduce_word([1] + inv_word(reduce_word(
            joint.SPLIT_WORDS[0] + joint.SPLIT_WORDS[2]))),
        reduce_word([2] + inv_word(reduce_word(
            joint.SPLIT_WORDS[1] + joint.SPLIT_WORDS[3]))),
    ]
    rows = p_rows + g_rows + cross + split
    require(len(rows) == 19 and digest_obj(rows) == COMPLETE_RELATORS_SHA,
            "independent complete Q0 relators")
    return rows


class IndependentJointGroup:
    def __init__(self, old: Any, e3: Any, e4: Any,
                 contexts: Sequence[Any], words: Sequence[Sequence[int]]) -> None:
        self.old, self.e3, self.e4 = old, e3, e4
        self.contexts = list(contexts)
        self.words = [list(x) for x in words]
        self.identity = (e3.identity,
                         tuple(e4.identity for _ in self.contexts))
        self.generators = [self.eval(word) for word in self.words]
        self.states = [self.identity]
        self.ids = {self.key(self.identity): 0}
        self.parent: list[int | None] = [None]
        self.parent_generator: list[int | None] = [None]
        for sid, state in enumerate(self.states):
            for gid, generator in enumerate(self.generators):
                value = self.mul(state, generator)
                key = self.key(value)
                if key not in self.ids:
                    self.ids[key] = len(self.states)
                    self.states.append(value)
                    self.parent.append(sid)
                    self.parent_generator.append(gid)
        require(len(self.states) == 243, "independent Gamma order")
        self.transitions = [[self.ids[self.key(self.mul(state, generator))]
                             for generator in self.generators]
                            for state in self.states]

    def key(self, state: Any) -> tuple[bytes, ...]:
        return (bytes(self.old._element_blob(state[0])),) + tuple(
            bytes(self.old._element_blob(value)) for value in state[1])

    def mul(self, left: Any, right: Any) -> Any:
        return (self.e3.mul(left[0], right[0]),
                tuple(self.e4.mul(left[1][i], right[1][i])
                      for i in range(len(self.contexts))))

    def inverse(self, value: Any) -> Any:
        return (self.e3.inverse(value[0]),
                tuple(self.e4.inverse(x) for x in value[1]))

    def eval(self, word: Sequence[int]) -> Any:
        return (self.e3.eval(self.old.embed_f2_pb3(word)),
                tuple(self.e4.eval(word, pair) for pair in self.contexts))

    def section_factors(self, state: int) -> list[int]:
        out = []
        while state:
            generator = self.parent_generator[state]
            parent = self.parent[state]
            require(generator is not None and parent is not None,
                    "independent Gamma section")
            out.append(generator)
            state = parent
        out.reverse()
        return out

    def section_word(self, state: int) -> list[int]:
        out: list[int] = []
        for generator in self.section_factors(state):
            append_reduced(out, self.words[generator])
        return out


class IndependentDelta:
    def __init__(self, v1: Any, e4: Any) -> None:
        self.pc = e4.pc
        xbar, ybar, zbar = (e4.eval(list(word))[1]
                             for word in (v1.X0, v1.Y0, v1.Z0))
        require(zbar == self.pc.inverse(self.pc.mul(ybar, xbar)),
                "independent Delta z")
        self.generators = {1: (xbar, xbar, ybar),
                           2: (ybar, zbar, zbar)}
        self.inverse_generators = {letter: tuple(
            self.pc.inverse(x) for x in generator)
            for letter, generator in self.generators.items()}
        identity = (self.pc.one(), self.pc.one(), self.pc.one())
        self.states = [identity]
        self.ids = {identity: 0}
        self.sections = [[]]
        tree = {}
        for sid, state in enumerate(self.states):
            for letter in (1, 2):
                following = self.mul(state, self.generators[letter])
                if following not in self.ids:
                    target = len(self.states)
                    self.ids[following] = target
                    self.states.append(following)
                    self.sections.append(self.sections[sid] + [letter])
                    tree[target] = (sid, letter)
        require(len(self.states) == N_DELTA, "independent Delta order")
        self.transition_table = {}
        self.edges = {}
        self.basis = []
        for sid, state in enumerate(self.states):
            for letter in (1, 2):
                target = self.ids[self.mul(state, self.generators[letter])]
                self.transition_table[(sid, letter)] = target
                if tree.get(target) == (sid, letter):
                    self.edges[(sid, letter)] = []
                else:
                    word = reduce_word(self.sections[sid] + [letter] +
                                       inv_word(self.sections[target]))
                    self.basis.append(word)
                    self.edges[(sid, letter)] = [len(self.basis)]
        require(len(self.basis) == N_SCHREIER,
                "independent Schreier rank")

    def mul(self, left: Any, right: Any) -> Any:
        return tuple(self.pc.mul(left[i], right[i]) for i in range(3))

    def step(self, state: int, letter: int) -> tuple[int, list[int]]:
        if letter > 0:
            return (self.transition_table[(state, letter)],
                    self.edges[(state, letter)])
        positive = -letter
        target = self.ids[self.mul(
            self.states[state], self.inverse_generators[positive])]
        return target, [-x for x in reversed(
            self.edges[(target, positive)])]

    def eval(self, word: Sequence[int], start: int = 0) -> int:
        state = start
        for letter in word:
            state, _ = self.step(state, int(letter))
        return state

    def rewrite(self, word: Sequence[int], start: int) \
            -> tuple[list[int], int]:
        state = start
        out: list[int] = []
        for letter in word:
            state, edge = self.step(state, int(letter))
            append_reduced(out, edge)
        return out, state

    def expand(self, word: Sequence[int]) -> list[int]:
        out: list[int] = []
        for letter in word:
            basis = self.basis[abs(letter) - 1]
            append_reduced(out, basis if letter > 0 else inv_word(basis))
        return out


class Echelon:
    def __init__(self, width: int) -> None:
        self.width = width
        self.pivots: dict[int, list[int]] = {}

    def add(self, row: Sequence[int]) -> bool:
        value = [int(x) % 3 for x in row]
        require(len(value) == self.width, "checker echelon width")
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


def row_reduce(rows: Sequence[Sequence[int]], width: int) -> list[list[int]]:
    matrix = [[int(x) % 3 for x in row] for row in rows if any(row)]
    require(all(len(row) == width for row in matrix), "checker row width")
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
                matrix[r] = [(a - factor * b) % 3
                             for a, b in zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    answer = [row for row in matrix if any(row)]
    answer.sort(key=lambda row: next(i for i, x in enumerate(row) if x))
    return answer


def schreier_row(word: Sequence[int]) -> list[int]:
    row = [0] * N_SCHREIER
    for letter in word:
        row[abs(letter) - 1] = (row[abs(letter) - 1] +
                                (1 if letter > 0 else 2)) % 3
    return row


def relation_roster(context: dict[str, Any], *, started: float,
                    domain_seconds: float) \
        -> tuple[list[dict[str, Any]], dict[str, Any]]:
    domain_seconds = validate_domain_seconds(domain_seconds)
    group: IndependentJointGroup = context["group"]
    words = context["words"]
    rows = []
    receipt = context["joint_receipt"]
    internal_frozen_rows = []
    action_frozen_rows = []
    q0_frozen_rows = []
    omega_evaluation_hash = hashlib.sha256()
    omega_evaluation_count = 0
    omega_canary_hash = hashlib.sha256()
    omega_canary_rows = []
    qgens = context["qgens"]
    qid = tuple(range(1, 37))
    # Deliberately organized differently from the producer: four signed
    # letters index separate exact transition tables.  Each table maps the
    # complete canonical source state to the complete target element.
    positive_joint = {1: group.eval([1]), 2: group.eval([2])}
    signed_joint_factors = {
        1: positive_joint[1], 2: positive_joint[2],
        -1: group.inverse(positive_joint[1]),
        -2: group.inverse(positive_joint[2]),
    }
    signed_q0_factors = {
        1: qgens[0], 2: qgens[1],
        -1: context["joint"].p_inv(qgens[0]),
        -2: context["joint"].p_inv(qgens[1]),
    }
    joint_tables: dict[int, dict[tuple[bytes, ...], Any]] = {
        letter: {} for letter in (-2, -1, 1, 2)}
    q0_tables: dict[int, dict[tuple[int, ...], tuple[int, ...]]] = {
        letter: {} for letter in (-2, -1, 1, 2)}
    joint_hits = 0
    joint_misses = 0
    q0_hits = 0
    q0_misses = 0

    def evaluate_from_identity(word: Sequence[int]) \
            -> tuple[tuple[int, ...], Any]:
        nonlocal joint_hits, joint_misses, q0_hits, q0_misses
        joint_state = group.identity
        q0_state = qid
        for raw_letter in word:
            letter = int(raw_letter)
            joint_key = group.key(joint_state)
            joint_table = joint_tables[letter]
            if joint_key in joint_table:
                joint_state = joint_table[joint_key]
                joint_hits += 1
            else:
                following = group.mul(
                    joint_state, signed_joint_factors[letter])
                joint_table[joint_key] = following
                joint_state = following
                joint_misses += 1
            q0_table = q0_tables[letter]
            if q0_state in q0_table:
                q0_state = q0_table[q0_state]
                q0_hits += 1
            else:
                following_q0 = context["joint"].p_mul(
                    q0_state, signed_q0_factors[letter])
                q0_table[q0_state] = following_q0
                q0_state = following_q0
                q0_misses += 1
        return q0_state, joint_state

    def add(layer: str, ordinal: int, word: Sequence[int],
            binding: dict[str, Any]) -> None:
        nonlocal omega_evaluation_count
        if omega_evaluation_count % 32 == 0:
            require(time.monotonic() - started <= domain_seconds,
                    "checker relation roster wall cap")
        reduced = reduce_word(word)
        q0_value, joint_value = evaluate_from_identity(reduced)
        joint_key = group.key(joint_value)
        require(q0_value == qid and joint_key == group.key(group.identity),
                "checker direct full relation Omega evaluation")
        global_ordinal = len(rows) + 1
        if global_ordinal in LEGACY_CANARY_GLOBAL_ORDINALS:
            legacy_q0 = context["joint"].p_eval(reduced, qgens)
            legacy_joint_key = group.key(group.eval(reduced))
            require(legacy_q0 == q0_value and legacy_joint_key == joint_key,
                    "checker cached evaluator legacy canary")
            canary_row = {
                "global_ordinal": global_ordinal,
                "layer": layer,
                "layer_ordinal": ordinal,
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
            "global_ordinal": global_ordinal, "layer": layer,
            "layer_ordinal": ordinal, "word": reduced,
            "word_length": len(reduced), "word_sha256": digest_obj(reduced),
            "original_157ee_row_binding": binding,
            "Omega_identity_by_exact_construction": True,
        })
    for state, transitions in enumerate(group.transitions):
        for generator, target in enumerate(transitions):
            require(group.key(group.mul(group.states[state],
                                        group.generators[generator])) ==
                    group.key(group.states[target]),
                    "independent internal transition")
            ordinal = state * 26 + generator + 1
            internal_frozen_rows.append(
                [state + 1, generator + 1, target + 1, 0, 0, 0, 0])
            add("gamma_cayley_edge", ordinal,
                group.section_word(state) + words[generator] +
                inv_word(group.section_word(target)), {
                    "157ee_layer": "internal_relations",
                    "157ee_rows_sha256":
                        receipt["internal_relations"]["rows_sha256"],
                    "state_id_one_based": state + 1,
                    "record_id_one_based": generator + 1,
                    "target_state_id_one_based": target + 1,
                })
    outer = [group.eval([1]), group.eval([2])]
    ordinal = 0
    for record, generator in enumerate(group.generators):
        for letter, value in enumerate(outer, 1):
            for orientation in (1, -1):
                ordinal += 1
                if orientation == 1:
                    conjugate = group.mul(group.mul(
                        group.inverse(value), generator), value)
                    prefix = [-letter] + words[record] + [letter]
                else:
                    conjugate = group.mul(group.mul(
                        value, generator), group.inverse(value))
                    prefix = [letter] + words[record] + [-letter]
                target = group.ids[group.key(conjugate)]
                action_frozen_rows.append([
                    record + 1, letter, orientation, target + 1,
                    len(group.section_factors(target)), 0, 0, 0, 0])
                add("xy_action", ordinal,
                    prefix + inv_word(group.section_word(target)), {
                        "157ee_layer": "action_relations",
                        "157ee_rows_sha256":
                            receipt["action_relations"]["rows_sha256"],
                        "record_id_one_based": record + 1,
                        "outer_letter": letter,
                        "orientation": orientation,
                        "target_state_id_one_based": target + 1,
                    })
    for ordinal, relator in enumerate(context["q0_relators"], 1):
        require(context["joint"].p_eval(relator, qgens) == qid,
                "independent Q0 relator identity")
        target = group.ids[group.key(group.eval(relator))]
        q0_frozen_rows.append([
            ordinal, len(relator), target + 1,
            len(group.section_factors(target)), 0, 0, 0, 0])
        add("q0_factor", ordinal,
            relator + inv_word(group.section_word(target)), {
                "157ee_layer": "q0_relations",
                "157ee_rows_sha256":
                    receipt["q0_relations"]["rows_sha256"],
                "complete_Q0_relator_ordinal": ordinal,
                "complete_Q0_relator_sha256": digest_obj(relator),
                "Gamma_defect_state_id_one_based": target + 1,
            })
    require(len(rows) == TOTAL_RELATIONS and
            dict(Counter(row["layer"] for row in rows)) == RELATION_COUNTS and
            [row["layer_ordinal"] for row in rows[6318:6422]] ==
                list(range(1, 105)),
            "independent relation roster layers and local ordinals")
    require(digest_obj(internal_frozen_rows) ==
                receipt["internal_relations"]["rows_sha256"] and
            action_frozen_rows == receipt["action_relations"]["rows"] and
            digest_obj(action_frozen_rows) ==
                receipt["action_relations"]["rows_sha256"] and
            q0_frozen_rows == receipt["q0_relations"]["rows"] and
            digest_obj(q0_frozen_rows) ==
                receipt["q0_relations"]["rows_sha256"],
            "independent literal frozen relation-row binding")
    require(omega_evaluation_count == TOTAL_RELATIONS,
            "checker full Omega relation count")
    require(len(omega_canary_rows) == LEGACY_CANARY_COUNT and
            [row["global_ordinal"] for row in omega_canary_rows] ==
                list(LEGACY_CANARY_GLOBAL_ORDINALS),
            "checker deterministic legacy canary roster")
    return rows, {
        "complete_digest_sha256": omega_evaluation_hash.hexdigest(),
        "joint_transition_cache_entries":
            sum(len(table) for table in joint_tables.values()),
        "q0_transition_cache_entries":
            sum(len(table) for table in q0_tables.values()),
        "joint_transition_cache_hits": joint_hits,
        "joint_transition_cache_misses": joint_misses,
        "q0_transition_cache_hits": q0_hits,
        "q0_transition_cache_misses": q0_misses,
        "legacy_group_eval_canary_count": len(omega_canary_rows),
        "legacy_group_eval_canary_global_ordinals":
            list(LEGACY_CANARY_GLOBAL_ORDINALS),
        "legacy_group_eval_canary_rows": omega_canary_rows,
        "legacy_group_eval_canary_rows_sha256":
            digest_obj(omega_canary_rows),
        "legacy_group_eval_canary_digest_sha256":
            omega_canary_hash.hexdigest(),
        "fail_closed": True,
    }


def exact_transition_cache_fixture() -> dict[str, Any]:
    """Exhaustive S3 cached/uncached equality through signed length five."""
    alphabet = (-2, -1, 1, 2)
    maximum_length = 5
    identity = (1, 2, 3)
    positive = {1: (2, 1, 3), 2: (2, 3, 1)}

    def mul(left: tuple[int, ...], right: tuple[int, ...]) \
            -> tuple[int, ...]:
        return tuple(left[right[i] - 1] for i in range(len(left)))

    def inverse(value: tuple[int, ...]) -> tuple[int, ...]:
        answer = [0] * len(value)
        for index, image in enumerate(value, 1):
            answer[image - 1] = index
        return tuple(answer)

    signed = {1: positive[1], 2: positive[2],
              -1: inverse(positive[1]), -2: inverse(positive[2])}
    words: list[tuple[int, ...]] = [()]
    frontier: list[tuple[int, ...]] = [()]
    for _ in range(maximum_length):
        frontier = [word + (letter,) for word in frontier
                    for letter in alphabet]
        words.extend(frontier)

    tables: dict[int, dict[tuple[int, ...], tuple[int, ...]]] = {
        letter: {} for letter in alphabet}
    evaluation_rows = []
    hits = 0
    misses = 0
    for ordinal, word in enumerate(words, 1):
        uncached = identity
        cached = identity
        for letter in word:
            uncached = mul(uncached, signed[letter])
            table = tables[letter]
            if cached in table:
                cached = table[cached]
                hits += 1
            else:
                following = mul(cached, signed[letter])
                table[cached] = following
                cached = following
                misses += 1
        require(cached == uncached,
                "fixture cached/uncached exact equality")
        evaluation_rows.append({
            "ordinal": ordinal, "word": list(word),
            "value": list(cached)})
    transition_rows = [
        {"letter": letter, "source": list(source), "target": list(target)}
        for letter in alphabet
        for source, target in sorted(tables[letter].items())]
    canary_ordinals = tuple(sorted(
        {1, len(words)} | set(range(113, len(words) + 1, 113))))
    canary_rows = [copy.deepcopy(evaluation_rows[i - 1])
                   for i in canary_ordinals]
    complete_digest = digest_obj(evaluation_rows)

    def validate_fixture(candidate: dict[str, Any]) -> None:
        require(candidate["group"] == "S3" and
                candidate["signed_alphabet"] == list(alphabet) and
                candidate["maximum_word_length"] == maximum_length and
                candidate["word_count"] == len(words) == 1365 and
                candidate["transition_rows"] == transition_rows and
                candidate["transition_rows_sha256"] ==
                    digest_obj(transition_rows) and
                candidate["canary_global_ordinals"] ==
                    list(canary_ordinals) and
                candidate["canary_rows"] == canary_rows and
                candidate["canary_rows_sha256"] ==
                    digest_obj(canary_rows) and
                candidate["complete_evaluation_digest_sha256"] ==
                    complete_digest and
                candidate["cache_hits"] == hits and
                candidate["cache_misses"] == misses and
                candidate["cache_entries"] == len(transition_rows),
                "exact transition exhaustive fixture")

    public = {
        "group": "S3", "nonabelian": True,
        "signed_alphabet": list(alphabet),
        "maximum_word_length": maximum_length,
        "word_count": len(words),
        "transition_rows": transition_rows,
        "transition_rows_sha256": digest_obj(transition_rows),
        "canary_global_ordinals": list(canary_ordinals),
        "canary_rows": canary_rows,
        "canary_rows_sha256": digest_obj(canary_rows),
        "complete_evaluation_digest_sha256": complete_digest,
        "cache_hits": hits, "cache_misses": misses,
        "cache_entries": len(transition_rows),
        "cached_equals_uncached_for_every_registered_word": True,
        "preregistered_before_execution": True,
    }
    validate_fixture(public)
    rejected = 0
    mutations = []
    changed = copy.deepcopy(public)
    changed["transition_rows"][0]["target"] = [9, 9, 9]
    mutations.append(changed)
    changed = copy.deepcopy(public)
    changed["canary_rows"][0]["value"][0] = 3
    mutations.append(changed)
    changed = copy.deepcopy(public)
    changed["canary_global_ordinals"][0] = 2
    mutations.append(changed)
    changed = copy.deepcopy(public)
    changed["complete_evaluation_digest_sha256"] = "0" * 64
    mutations.append(changed)
    for changed in mutations:
        try:
            validate_fixture(changed)
        except RuntimeError:
            rejected += 1
    require(rejected == 4, "exact transition fixture mutations")
    public["mutation_tests_rejected"] = rejected
    return public


def context() -> dict[str, Any]:
    coeff = load_module("_task169_checker_task168", COEFF_PATH, COEFF_SHA)
    v5 = coeff.load_v5()
    v3, v2, v1, summary, private, prior, _, meta = v5.build_context()
    joint = load_module("_task169_checker_157ee", JOINT_PATH, JOINT_SHA)
    predecessor = joint.load_prev()
    q3 = json.loads((ROOT / Q3_PATH).read_text(encoding="utf-8"))
    old = predecessor.load_pinned_module(
        predecessor.OLD_PRODUCER, predecessor.OLD_PRODUCER_SHA,
        "_task169_checker_old")
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, public = old.cheap_context_registry(e4)
    receipt = json.loads((ROOT / JOINT_RECEIPT_PATH).read_text(
        encoding="utf-8"))
    require(public == receipt["context_registry"] and
            public["context_rows_sha256"] == CONTEXT_ROWS_SHA and
            public["named_use_mapping_sha256"] == ALIAS_ROWS_SHA,
            "independent context registry")
    words = [list(row["word"]) for row in
             q3["correction_fibre"]["records"] if row["word"]]
    require(len(words) == 26 and digest_obj(words) == RECORD_WORDS_SHA,
            "independent record words")
    group = IndependentJointGroup(old, e3, e4, contexts, words)
    qgens = [tuple(row) for row in
             q3["coarse_models"]["Q0"]["marked_permutations"]]
    qid = tuple(range(1, 37))
    require(all(joint.p_eval(word, qgens) == qid for word in words),
            "independent record Q0 kernel")
    return {"coeff": coeff, "v5": v5, "v3": v3, "v2": v2,
            "v1": v1, "summary": summary, "private": private,
            "prior": prior, "meta": meta, "joint": joint,
            "old": old, "q3": q3, "e3": e3, "e4": e4,
            "contexts": contexts, "aliases": aliases,
            "context_public": public, "joint_receipt": receipt,
            "words": words, "group": group, "qgens": qgens,
            "q0_relators": complete_relators_independent(joint)}


def decode_roster(public: dict[str, Any]) -> list[list[int]]:
    raw = base64.b64decode(public["payload_base64"], validate=True)
    require(len(raw) == public["byte_length"] and
            hashlib.sha256(raw).hexdigest() == public["payload_sha256"],
            "independent roster payload")
    words = []
    for row in public["rows"]:
        start = row["i8_offset_bytes"]
        word = [x if x < 128 else x - 256
                for x in raw[start:start + row["word_length"]]]
        require(digest_obj(word) == row["word_sha256"],
                "independent packed word")
        words.append(word)
    return words


def replay_joint_word(ctx: dict[str, Any], word: Sequence[int], *,
                      require_exp3: bool = True) \
        -> dict[str, Any]:
    qid = tuple(range(1, 37))
    require(ctx["joint"].p_eval(word, ctx["qgens"]) == qid and
            ctx["e3"].eval(ctx["old"].embed_f2_pb3(word)) ==
                ctx["e3"].identity,
            "independent word Q0/E3")
    values = [ctx["e4"].eval(word, pair) for pair in ctx["contexts"]]
    require(values == [ctx["e4"].identity] * 31,
            "independent word 31 contexts")
    aliases = [values[row["context_id"] - 1]
               for row in ctx["context_public"]["named_uses"]]
    require(aliases == [ctx["e4"].identity] * 46,
            "independent word 46 aliases")
    exp = exponent_sums(word)
    exp_mod3 = [x % 3 for x in exp]
    if require_exp3:
        require(exp_mod3 == [0, 0],
                "independent word exponent gate")
    blobs = [ctx["old"]._element_blob(value).hex() for value in values]
    return {"Q0_identity": True, "E3_identity": True,
            "all_31_context_ids_identity": True,
            "all_46_named_aliases_identity": True,
            "three_target6_context_ids": [1, 2, 3],
            "three_target6_contexts_identity": True,
            "context_value_blobs_sha256": digest_obj(blobs),
            "free_exponent_sums": exp,
            "free_exponent_sums_mod3": exp_mod3,
            "historical_exp3_prefilter_pass": exp_mod3 == [0, 0]}


def nullspace(matrix: Sequence[Sequence[int]], nvariables: int) \
        -> list[list[int]]:
    rows = [[int(x) % 3 for x in row] for row in matrix]
    pivot_row = 0
    pivots = []
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
    answer = []
    for free in [i for i in range(nvariables) if i not in set(pivots)]:
        vector = [0] * nvariables
        vector[free] = 1
        for pivot in pivots:
            vector[pivot] = (-pivot_rows[pivot][free]) % 3
        answer.append(vector)
    return row_reduce(answer, nvariables)


def combine_rows(rows: Sequence[Sequence[int]], coefficients: Sequence[int],
                 width: int) -> list[int]:
    out = [0] * width
    for row, coefficient in zip(rows, coefficients):
        for i, value in enumerate(row):
            out[i] = (out[i] + int(coefficient) * int(value)) % 3
    return out


def combine_words(words: Sequence[Sequence[int]],
                  coefficients: Sequence[int]) -> list[int]:
    out: list[int] = []
    for word, coefficient in zip(words, coefficients):
        for _ in range(int(coefficient)):
            append_reduced(out, word)
    return out


def independent_domain_check(receipt: dict[str, Any],
                             ctx: dict[str, Any],
                             domain_seconds: float) -> dict[str, Any]:
    domain_seconds = validate_domain_seconds(domain_seconds)
    started = time.monotonic()
    domain = receipt["registered_joint_domain"]
    verify_self_digest(domain, "checker domain")
    require(domain["schema"] == DOMAIN_SCHEMA and
            domain["scope_name"] ==
                "registered_joint_value_and_exp3_domain" and
            domain["full_E4_positive_class_reconstructed"] is False and
            domain["true_PB4_D2_equality_used"] is False,
            "checker domain boundary")
    target = domain["context_registry"]["target6_binding"]
    aliases = {row["name"]: row["context_id"] for row in
               ctx["context_public"]["named_uses"]}
    require(target["registry_context_ids"] == [1, 2, 3] and
            {row["name"]: row["context_id"] for row in
             target["named_alias_rows"]} == TARGET_ALIAS_IDS and
            all(aliases[name] == cid for name, cid in TARGET_ALIAS_IDS.items()),
            "checker target contexts and aliases")

    group: IndependentJointGroup = ctx["group"]
    state_rows = [[blob.hex() for blob in group.key(state)]
                  for state in group.states]
    gamma = domain["joint_group_replay"]["Gamma_invariants"]
    require(gamma == ctx["joint_receipt"]["gamma"] and
            len(group.states) == gamma["order"] == 243 and
            digest_obj(state_rows) == gamma["state_rows_sha256"] and
            digest_obj(group.transitions) ==
                gamma["transition_rows_sha256"] and
            domain["joint_group_replay"]["Q0_presentation"] ==
                ctx["joint_receipt"]["q0_presentation"] and
            domain["joint_group_replay"]["record_words_sha256"] ==
                RECORD_WORDS_SHA and
            domain["joint_group_replay"]["complete_Q0_relators_sha256"] ==
                COMPLETE_RELATORS_SHA,
            "independent marked joint image/presentation invariants")

    delta = IndependentDelta(ctx["v1"], ctx["private"]["e4"])
    task_pairs = ((ctx["v1"].X0, ctx["v1"].Y0),
                  (ctx["v1"].X0, ctx["v1"].Z0),
                  (ctx["v1"].Y0, ctx["v1"].Z0))
    task_blobs = [[
        (bytes(ctx["private"]["e4"].eval(list(left))[0]) +
         bytes(ctx["private"]["e4"].eval(list(left))[1])).hex(),
        (bytes(ctx["private"]["e4"].eval(list(right))[0]) +
         bytes(ctx["private"]["e4"].eval(list(right))[1])).hex(),
    ] for left, right in task_pairs]
    registry_rows = ctx["context_public"]["contexts"]
    exact_ids = []
    for pair in task_blobs:
        matches = [row["context_id"] for row in registry_rows
                   if row["left_hex"] == pair[0] and
                   row["right_hex"] == pair[1]]
        require(len(matches) == 1,
                "checker exact target context registry row")
        exact_ids.append(matches[0])
    projected = [tuple(ctx["e4"].eval(
        [letter], ctx["contexts"][cid - 1])[1] for cid in exact_ids)
        for letter in (1, 2)]
    exact_target = {
        "registry_context_ids": exact_ids,
        "registry_rows": [copy.deepcopy(registry_rows[cid - 1])
                          for cid in exact_ids],
        "named_alias_rows": [
            {"name": name, "context_id": aliases[name]}
            for name in TARGET_ALIAS_IDS],
        "task168_literal_context_pair_blobs": task_blobs,
        "exact_pair_and_alias_binding": True,
        "projection_is_E4_coordinate_then_Pi4_3_pc_component": True,
        "marked_generator_images_equal_omega3": True,
    }
    require(exact_ids == [1, 2, 3] and target == exact_target and
            projected == [delta.generators[1], delta.generators[2]],
            "independent Omega-to-Delta marked projection")
    typing = domain["exact_sequence_typing"]
    require(typing == {
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
    } and len(delta.states) == N_DELTA,
            "independent exact-sequence typing and onto gate")

    roster, omega_stats = relation_roster(
        ctx, started=started, domain_seconds=domain_seconds)
    public_roster = domain["relation_roster"]
    decoded = decode_roster(public_roster)
    require(decoded == [row["word"] for row in roster] and
            len(roster) == public_roster["row_count"] == TOTAL_RELATIONS,
            "independent relation words equal lossless roster")
    require(public_roster["direct_full_Omega_relation_evaluation_count"] ==
                TOTAL_RELATIONS and
            public_roster[
                "direct_full_Omega_relation_evaluation_digest_sha256"] ==
                omega_stats["complete_digest_sha256"],
            "independent full Q0/E3/31-context relation digest")
    public_evaluator = public_roster["exact_transition_evaluator"]
    for key in (
            "joint_transition_cache_entries",
            "q0_transition_cache_entries",
            "joint_transition_cache_hits",
            "joint_transition_cache_misses",
            "q0_transition_cache_hits",
            "q0_transition_cache_misses",
            "legacy_group_eval_canary_count",
            "legacy_group_eval_canary_global_ordinals",
            "legacy_group_eval_canary_rows",
            "legacy_group_eval_canary_rows_sha256",
            "legacy_group_eval_canary_digest_sha256",
            "fail_closed"):
        require(public_evaluator[key] == omega_stats[key],
                "independent exact-transition field " + key)
    require(public_evaluator["semantics"] ==
                "letter-by-letter multiplication in the exact pinned "
                "Q0 x E3 x E4^31 direct product on every final reduced "
                "F2 relation word" and
            public_evaluator["legacy_canary_rule"] ==
                "first and last local ordinal of each relation layer, "
                "plus every global ordinal divisible by 257" and
            public_evaluator["joint_transition_cache_hits"] +
                public_evaluator["joint_transition_cache_misses"] ==
                public_roster["total_signed_letters"] and
            public_evaluator["q0_transition_cache_hits"] +
                public_evaluator["q0_transition_cache_misses"] ==
                public_roster["total_signed_letters"],
            "independent exact-transition semantics and counts")
    for actual, public in zip(roster, public_roster["rows"]):
        compare = {key: value for key, value in actual.items() if key != "word"}
        compare["i8_offset_bytes"] = public["i8_offset_bytes"]
        require(compare == public, "independent relation metadata")

    delta_public = domain["Delta3_and_Schreier"]
    require(delta.basis == delta_public["ordered_schreier_words"] and
            delta.sections == delta_public["positive_BFS_transversal_words"],
            "independent Delta/Schreier order")
    echelon = Echelon(N_SCHREIER)
    selected = []
    input_hash = hashlib.sha256()
    input_ordinal = 0
    for relation in roster:
        require(delta.eval(relation["word"]) == 0,
                "independent relation in K3")
        for tid, transversal in enumerate(delta.sections):
            input_ordinal += 1
            if input_ordinal % 1024 == 0:
                require(time.monotonic() - started <= domain_seconds,
                        "checker RS wall cap")
            rewritten, end = delta.rewrite(relation["word"], tid)
            f2_word = reduce_word(transversal + relation["word"] +
                                  inv_word(transversal))
            require(end == tid and delta.expand(rewritten) == f2_word,
                    "independent conjugate reconstruction")
            coefficients = schreier_row(rewritten)
            input_record = {
                "input_ordinal": input_ordinal,
                "relation_global_ordinal": relation["global_ordinal"],
                "relation_layer": relation["layer"],
                "relation_layer_ordinal": relation["layer_ordinal"],
                "transversal_id_one_based": tid + 1,
                "transversal_word": list(transversal),
                "coefficient_row": coefficients,
                "conjugate_word_sha256": digest_obj(f2_word),
                "schreier_word_sha256": digest_obj(rewritten),
            }
            input_hash.update(canonical_bytes(input_record) + b"\n")
            if echelon.add(coefficients):
                selected.append({
                    **input_record,
                    "source_relation_word_sha256": relation["word_sha256"],
                    "source_relation_binding": copy.deepcopy(
                        relation["original_157ee_row_binding"]),
                    "signed_F2_word": f2_word,
                    "signed_F2_word_length": len(f2_word),
                    "signed_F2_word_sha256": digest_obj(f2_word),
                    "signed_schreier_word": rewritten,
                    "signed_schreier_word_length": len(rewritten),
                    "direct_reconstruction_equal": True,
                    "registered_joint_replay": replay_joint_word(
                        ctx, f2_word, require_exp3=False),
                })
    rs = domain["RS_abelianization"]
    require(input_ordinal == TOTAL_RS_ROWS and
            input_hash.hexdigest() ==
                rs["complete_input_row_digest_sha256"] and
            selected == rs["word_bearing_first_independent_input_rows"] and
            echelon.rank() == rs["rank_B_joint"] and
            row_reduce([row["coefficient_row"] for row in selected],
                       N_SCHREIER) == rs["canonical_B_joint_basis"] and
            rs["all_conjugates_identity_under_Omega"] is True and
            rs["kernel_H1_K3_to_H1_Q_equals_rowspace"] is True and
            rs["normal_presentation_theorem_dependency"]["used"] is True and
            rs["order_independent_elimination_crosscheck"]["status"] ==
                "COMPLETED" and
            rs["order_independent_elimination_crosscheck"]["rank"] ==
                echelon.rank() and
            rs["second_independent_Q_presentation_route"]["status"] ==
                "UNKNOWN_NO_THEOREM_INDEPENDENT_ROUTE" and
            rs["second_independent_Q_presentation_route"][
                "same_packed_rows_reverse_elimination_is_not_claimed_independent"]
                is True and
            rs["second_independent_Q_presentation_route"][
                "helper_nonshared_checker_rebuilds_the_same_normal_presentation_route"]
                is True,
            "independent complete RS abelianization")

    exp_rows = [[exponent_sums(word)[axis] % 3 for word in delta.basis]
                for axis in (0, 1)]
    joint_rows = [row["coefficient_row"] for row in selected]
    exp_on_joint = [[sum(exp_rows[axis][i] * row[i]
                         for i in range(N_SCHREIER)) % 3
                     for row in joint_rows] for axis in (0, 1)]
    exp_kernel = nullspace(exp_on_joint, len(joint_rows))
    gate = domain["historical_exponent_gate"]
    require(exp_rows == gate["two_exponent_rows_on_28_schreier_words"] and
            exp_on_joint == gate["exponent_map_on_B_joint_basis"] and
            len(exp_kernel) == gate["rank_B_legal_value"],
            "independent exponent intersection dimension")
    legal = gate["word_bearing_basis"]
    legal_rows = []
    for row in legal:
        coefficients = row["joint_basis_coefficients"]
        expected_row = combine_rows(joint_rows, coefficients, N_SCHREIER)
        expected_word = combine_words(
            [entry["signed_F2_word"] for entry in selected], coefficients)
        require(expected_row == row["coefficient_row"] and
                expected_word == row["signed_F2_word"] and
                digest_obj(expected_word) == row["signed_F2_word_sha256"] and
                replay_joint_word(ctx, expected_word) ==
                    row["registered_joint_replay"],
                "independent legal word provenance/replay")
        legal_rows.append(expected_row)
    require(row_reduce(legal_rows, N_SCHREIER) ==
            gate["canonical_B_legal_value_basis"] and
            (len(legal_rows) < len(joint_rows)) is gate["intersection_strict"],
            "independent legal basis")
    return {"relation_count": len(roster), "RS_row_count": input_ordinal,
            "rank_B_joint": echelon.rank(),
            "H1_Q_dimension": N_SCHREIER - echelon.rank(),
            "rank_B_legal_value": len(legal_rows),
            "exponent_intersection_strict": gate["intersection_strict"],
            "all_relation_words_reconstructed": True,
            "all_RS_conjugates_reconstructed": True,
            "rowspace_kernel_identification_depends_on_normal_presentation_theorem":
                True,
            "same_rows_reverse_elimination_not_claimed_independent": True,
            "exact_transition_cache_and_canaries_reproduced": True,
            "domain_seconds": domain_seconds,
            "helper_shared_with_task169_producer": False}


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
    zl, zr = mask & ~(ones | twos), mask & ~(add_one | add_two)
    return ((ones & zr) | (zl & add_one) | (twos & add_two),
            (twos & zr) | (zl & add_two) | (ones & add_one))


def bitplane_scale(value: tuple[int, int], coefficient: int) \
        -> tuple[int, int]:
    return (0, 0) if coefficient == 0 else value if coefficient == 1 \
        else (value[1], value[0])


def equations_from_bitplanes(columns: Sequence[tuple[int, int]],
                             rhs: tuple[int, int], dimension: int) \
        -> list[tuple[list[int], int]]:
    rows: dict[int, list[int]] = {}
    for j, (ones, twos) in enumerate(columns):
        require((ones & twos) == 0 and
                (ones | twos).bit_length() <= dimension,
                "checker affine bitplanes")
        for value, coefficient in ((ones, 1), (twos, 2)):
            plane = value
            while plane:
                bit = plane & -plane
                rows.setdefault(bit.bit_length() - 1,
                                [0] * len(columns))[j] = coefficient
                plane ^= bit
    right: dict[int, int] = {}
    for value, coefficient in ((rhs[0], 1), (rhs[1], 2)):
        plane = value
        while plane:
            bit = plane & -plane
            right[bit.bit_length() - 1] = coefficient
            plane ^= bit
    return [(rows.get(i, [0] * len(columns)), right.get(i, 0))
            for i in sorted(set(rows) | set(right))]


def rref_affine(equations: Sequence[tuple[Sequence[int], int]],
                nvariables: int) -> dict[str, Any]:
    matrix = [[int(x) % 3 for x in row] + [int(rhs) % 3]
              for row, rhs in equations]
    pivots = []
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
    kernel = nullspace([row[:-1] for row in nonzero if any(row[:-1])],
                       nvariables)
    return {"consistent": not inconsistent, "rank": len(pivots),
            "nullity": nvariables - len(pivots),
            "canonical_particular_free_zero": particular,
            "canonical_kernel_basis": kernel,
            "rref_rows": nonzero}


def independent_intersection(task: dict[str, Any],
                             domain: dict[str, Any]) -> dict[str, Any]:
    U = [row["coefficient_row"] for row in
         domain["historical_exponent_gate"]["word_bearing_basis"]]
    d = len(U)
    dimension = task["dimension"]
    legal = [bitplane(row) for row in
             task["ordered_reduced_quotient_legal_rows"]]
    target = bitplane(task["reduced_quotient_target"])
    columns = []
    for basis_row in U:
        value = (0, 0)
        for column, coefficient in zip(legal, basis_row):
            value = bitplane_add(value,
                bitplane_scale(column, int(coefficient)), dimension)
        columns.append(value)
    equations = equations_from_bitplanes(columns, target, dimension)
    solved = rref_affine(equations, d)
    public_columns = [public_bitplane(value, dimension) for value in columns]
    result = {
        "j": task["j"], "consistent": solved["consistent"],
        "rank": solved["rank"], "nullity": solved["nullity"],
        "word_basis_dimension": d,
        "ordered_word_basis_U_rows_in_original_28_coordinates": U,
        "ordered_word_basis_U_rows_sha256": digest_obj(U),
        "ordered_reduced_quotient_LjU_columns": public_columns,
        "ordered_reduced_quotient_LjU_columns_sha256":
            digest_obj(public_columns),
        "coefficient_system_equation_count": len(equations),
        "coefficient_system_rref_rows": solved["rref_rows"],
        "coefficient_system_matrix_rhs_sha256": digest_obj({
            "nvariables": d, "equations": equations}),
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
    constraints = []
    lex_a = []
    for coordinate in range(N_SCHREIER):
        row = [U[k][coordinate] for k in range(d)]
        choice = None
        for value in (0, 1, 2):
            if rref_affine(equations + constraints + [(row, value)],
                           d)["consistent"]:
                choice = value
                break
        require(choice is not None, "checker lex a extension")
        constraints.append((row, choice))
        lex_a.append(choice)
    fixed = rref_affine(equations + constraints, d)
    z = fixed["canonical_particular_free_zero"]
    require(z is not None and combine_rows(U, z, N_SCHREIER) == lex_a,
            "checker canonical z")
    result.update({
        "lex_first_coefficient_vector_a": lex_a,
        "canonical_word_basis_coefficients_z_for_lex_a": z,
        "canonical_coefficient_kernel_basis_a": row_reduce([
            combine_rows(U, row, N_SCHREIER)
            for row in solved["canonical_kernel_basis"]], N_SCHREIER),
    })
    return result


def independent_empty_affine_regression() -> dict[str, Any]:
    """A second-coordinate target outside the span of two first-coordinate columns."""
    first_coordinate = {
        "dimension": 2, "coefficient_one_plane_hex": "1",
        "coefficient_two_plane_hex": "0"}
    zero = {
        "dimension": 2, "coefficient_one_plane_hex": "0",
        "coefficient_two_plane_hex": "0"}
    task = {
        "j": 2, "dimension": 2,
        "ordered_reduced_quotient_legal_rows":
            [copy.deepcopy(first_coordinate),
             copy.deepcopy(first_coordinate)] +
            [copy.deepcopy(zero) for _ in range(26)],
        "reduced_quotient_target": {
            "dimension": 2, "coefficient_one_plane_hex": "2",
            "coefficient_two_plane_hex": "0"},
    }
    U = [[0, 1] + [0] * 26, [1, 0] + [0] * 26]
    domain = {"historical_exponent_gate": {"word_bearing_basis": [
        {"coefficient_row": row} for row in U]}}
    result = independent_intersection(task, domain)
    expected_column = public_bitplane((1, 0), 2)
    require(result["consistent"] is False and
            result["ordered_reduced_quotient_LjU_columns"] ==
                [expected_column, expected_column] and
            result["coefficient_system_equation_count"] == 2 and
            result["coefficient_system_rref_rows"] ==
                [[1, 1, 0], [0, 0, 1]] and
            result["canonical_z_particular_free_zero"] is None,
            "checker genuinely inconsistent second-coordinate affine fixture")
    return {
        "production_independent_intersection_path_used": True,
        "LjU_span": "first coordinate only",
        "target": "second coordinate",
        "consistent": False,
        "equation_count": 2,
        "contradiction_row": [0, 0, 1],
    }


def evaluate_task168(certificate: dict[str, Any],
                     coefficients: Sequence[int]) -> bool:
    dimension = certificate["dimension"]
    value = (0, 0)
    for column, coefficient in zip(
            certificate["ordered_reduced_quotient_legal_rows"], coefficients):
        value = bitplane_add(value, bitplane_scale(
            bitplane(column), int(coefficient)), dimension)
    return value == bitplane(certificate["reduced_quotient_target"])


def independent_depth_inclusion(previous: dict[str, Any],
                                current: dict[str, Any],
                                previous_task: dict[str, Any]) \
        -> dict[str, Any]:
    require(previous["j"] < current["j"],
            "checker joint depth order")
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
            "checker nonempty family after empty predecessor")
    particular = current["lex_first_coefficient_vector_a"]
    require(evaluate_task168(previous_task, particular),
            "checker new particular in previous family")
    homogeneous = copy.deepcopy(previous_task)
    homogeneous["reduced_quotient_target"][
        "coefficient_one_plane_hex"] = "0"
    homogeneous["reduced_quotient_target"][
        "coefficient_two_plane_hex"] = "0"
    for row in current["canonical_coefficient_kernel_basis_a"]:
        require(evaluate_task168(homogeneous, row),
                "checker new kernel direction in previous family")
    return {
        "previous_j": previous["j"], "new_j": current["j"],
        "proof_kind": "particular_and_homogeneous_directions",
        "new_particular_in_previous_joint_family": True,
        "new_kernel_direction_count": len(
            current["canonical_coefficient_kernel_basis_a"]),
        "all_new_kernel_directions_in_previous_joint_family": True,
        "A_joint_new_subset_A_joint_previous": True,
    }


def completed_d2_states(ctx: dict[str, Any], task168: dict[str, Any],
                        checkpoint_dir: Path) \
        -> dict[int, tuple[dict[str, Any], Any]]:
    v5, v3, v2, v1 = (ctx[key] for key in ("v5", "v3", "v2", "v1"))
    summary, private, prior, meta = (ctx[key] for key in
                                     ("summary", "private", "prior", "meta"))
    bindings = v5.fixed_bindings(summary, prior, meta)
    states = {}
    left_cache = v3.LeftMultiplyCache(private["e4"].pc, enabled=True)
    progression = task168["frozen_v5_receipt"]["result"].get(
        "j_progression", [])
    for row in progression:
        j = row["j"]
        path = v5.delta_path(checkpoint_dir, j, 11)
        header, echelon, records, _ = v5.replay_delta_chain(
            path, checkpoint_dir, v3, v2, v1,
            summary, prior, bindings)
        require(header["cumulative_state_commitment_sha256"] ==
                    row["v5_append_only_delta"]
                       ["terminal_state_commitment_sha256"] and
                records[-1]["relator"] == 11,
                "checker authenticated task168 D2 chain")
        workspace = v3.j_workspace(
            v1, private, j, accelerators=True, left_cache=left_cache)
        states[j] = (workspace, echelon)
    return states


def pc_combination(v1: Any, rows: Sequence[dict[Any, int]],
                   coefficients: Sequence[int]) -> dict[Any, int]:
    value: dict[Any, int] = {}
    for row, coefficient in zip(rows, coefficients):
        if coefficient == 1:
            value = v1.add_vec(value, row)
        elif coefficient == 2:
            value = v1.add_vec(value, v1.neg_vec(row))
        else:
            require(coefficient == 0, "checker PC coefficient")
    return value


def prefix_for_sigma(ctx: dict[str, Any]) -> Any:
    v1, e4 = ctx["v1"], ctx["private"]["e4"]
    _, base = v1.construct_base()
    words = [v1.substitute2(base, left, right) for left, right in
             ((v1.X0, v1.Y0), (v1.X0, v1.Z0), (v1.Y0, v1.Z0))]
    _, bbar, cbar = (e4.eval(word) for word in words)
    return e4.mul(bbar, e4.inverse(cbar))


def replay_actual_sigma(ctx: dict[str, Any], workspace: dict[str, Any],
                        echelon: Any, word: Sequence[int],
                        coefficients: Sequence[int]) -> dict[str, Any]:
    v1, private = ctx["v1"], ctx["private"]
    e4 = private["e4"]
    pairs = ((v1.X0, v1.Y0), (v1.X0, v1.Z0), (v1.Y0, v1.Z0))
    values = [e4.eval(v1.substitute2(word, left, right))[1]
              for left, right in pairs]
    require(values == [e4.pc.one()] * 3,
            "checker actual word target contexts")
    ga = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.X0, v1.Y0))
    gb = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.X0, v1.Z0))
    gc = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.Y0, v1.Z0))
    sigma = v1.add_vec(private["core"].translate_vec(
        e4, v1.add_vec(gc, v1.neg_vec(gb)), prefix_for_sigma(ctx)), ga)
    sigma_pc = private["core"].project_to_pi(sigma)
    require(sigma_pc == pc_combination(
        v1, private["sigma_pc"], coefficients),
        "checker actual word Sigma rows")
    projected = v1.project_vec_to_Ij(sigma_pc, workspace["j"])
    sigma_vector = workspace["sp"].vec({
        workspace["idx"][key]: value for key, value in projected.items()
        if key in workspace["idx"]})
    expected = (0, 0)
    for column, coefficient in zip(workspace["legal_vectors"], coefficients):
        expected = workspace["sp"].add(
            expected, workspace["sp"].scale(column, coefficient))
    require(sigma_vector == expected, "checker Jennings Sigma")
    remainder, pivot = echelon.reduce(
        workspace["sp"].sub(workspace["target_vector"], sigma_vector))
    require(remainder == (0, 0) and pivot == -1,
            "checker actual word D2 remainder")
    public = v1.serialize_pc_gradient(sigma_pc)
    return {"three_target6_context_values_identity": True,
            "projected_Sigma": public,
            "projected_Sigma_sha256": digest_obj(public),
            "Sigma_equals_28_row_linear_combination": True,
            "Jennings_projection_equals_28_row_linear_combination": True,
            "target_minus_Sigma_reduces_to_zero_mod_authenticated_D2": True,
            "first_unreduced_coordinate": pivot}


def check_full_intersections(receipt: dict[str, Any], ctx: dict[str, Any],
                             checkpoint_dir: Path) \
        -> dict[str, Any]:
    task168 = receipt["frozen_task168_receipt"]
    verify_self_digest(task168, "embedded task168 receipt")
    require(digest_obj(task168) == receipt["frozen_task168_receipt_sha256"],
            "embedded task168 binding")
    d2_states = completed_d2_states(ctx, task168, checkpoint_dir)
    task_rows = task168["result"]["coefficient_certificates"]
    task_by_j = {row["j"]: row for row in task_rows}
    require(receipt["result"]["completed_task168_j_values"] ==
            sorted(task_by_j) and
            (not task_by_j or min(task_by_j) == 9),
            "same-invocation completed task168 j roster")
    domain = receipt["registered_joint_domain"]
    basis = domain["historical_exponent_gate"]["word_bearing_basis"]
    checked = 0
    file_by_j = {row["j"]: row for row in
                 receipt["result"]["joint_coeff_certificate_file_manifest"]}
    certificates = receipt["result"]["joint_coeff_certificates"]
    member_j = [row["j"] for row in task_rows
                if row["affine_family"]["nonempty"]]
    require(receipt["result"][
                "joint_coeff_certificate_file_manifest_count"] ==
            len(file_by_j) == len(certificates) and
            [row["j"] for row in certificates] == member_j and
            receipt["result"]["completed_member_depth_count"] ==
                len(member_j) and
            receipt["result"]["joint_coeff_certificate_count"] ==
                len(certificates) and
            receipt["result"]["joint_intersections"] ==
                [row["intersection"] for row in certificates],
            "joint certificate/member/intersection rosters")
    expected_inclusions = []
    previous_intersection = None
    previous_task = None
    for certificate in certificates:
        verify_self_digest(certificate, "joint certificate")
        require(certificate["claims"] == FALSE_CLAIMS and
                all(certificate[key] is value
                    for key, value in BOUNDARIES.items()),
                "joint certificate boundaries")
        j = certificate["j"]
        task = task_by_j[j]
        file_row = file_by_j[j]
        certificate_path = Path(file_row["path"])
        certificate_path = certificate_path if certificate_path.is_absolute() \
            else ROOT / certificate_path
        certificate_raw = certificate_path.read_bytes()
        require(certificate_raw == canonical_bytes(certificate) + b"\n" and
                len(certificate_raw) == file_row["bytes"] and
                hashlib.sha256(certificate_raw).hexdigest() ==
                    file_row["sha256"] and
                file_row["self_digest_sha256"] ==
                    certificate["self_digest_sha256"],
                "joint coefficient immutable file binding")
        require(certificate["g760_base_sha256"] ==
                    ctx["summary"]["base"]["sha256"] and
                certificate["task168_certificate_self_digest_sha256"] ==
                    task["self_digest_sha256"] and
                certificate["task168_completed_public_row_sha256"] ==
                    task["completed_public_row_sha256"] and
                certificate["task168_completed_j_checkpoint"] ==
                    task["completed_j_checkpoint"] and
                certificate["task168_terminal_D2_state_commitment_sha256"] ==
                    task["terminal_D2_state_commitment_sha256"] and
                certificate["task168_D2_rank"] == task["D2_rank"] and
                certificate["task168_Jennings_basis_sha256"] ==
                    task["Jennings_basis_sha256"],
                "joint certificate g760/public-row/D2 bindings")
        intersection = certificate["intersection"]
        require(independent_intersection(task, domain) == intersection,
                "independent full affine family and lex point")
        if previous_intersection is not None:
            require(previous_task is not None,
                    "checker previous task certificate")
            expected_inclusions.append(independent_depth_inclusion(
                previous_intersection, intersection, previous_task))
        previous_intersection = intersection
        previous_task = task
        if intersection["consistent"]:
            a = intersection["lex_first_coefficient_vector_a"]
            z = intersection[
                "canonical_word_basis_coefficients_z_for_lex_a"]
            require(evaluate_task168(task, a),
                    "independent selected a in task168 family")
            expected_a = combine_rows(
                [row["coefficient_row"] for row in basis], z, N_SCHREIER)
            expected_word = combine_words(
                [row["signed_F2_word"] for row in basis], z)
            public_word = certificate["actual_joint_kernel_word"]
            require(expected_a == a and
                    expected_word == public_word["signed_F2_word"] and
                    digest_obj(expected_word) ==
                        public_word["signed_F2_word_sha256"] and
                    replay_joint_word(ctx, expected_word) ==
                        public_word["registered_joint_replay"] and
                    public_word["naive_Schreier_product_used"] is False,
                    "independent actual relation word")
            workspace, echelon = d2_states[j]
            require(replay_actual_sigma(
                ctx, workspace, echelon, expected_word, a) ==
                    public_word["task168_projected_D2_replay"],
                    "independent actual word Sigma/D2 replay")
        else:
            require(certificate["actual_joint_kernel_word"] is None,
                    "empty joint intersection no word")
        checked += 1
    require(receipt["result"]["depth_inclusion_receipts"] ==
                expected_inclusions,
            "independent adjacent joint-family inclusions")
    any_underlying_nonmember = any(
        not row["affine_family"]["nonempty"] for row in task_rows)
    intersections = [row["intersection"] for row in certificates]
    if any_underlying_nonmember or any(
            not row["consistent"] for row in intersections):
        expected_terminal = "R07_760_JOINT_COEFF_INTERSECTION_EMPTY"
    elif intersections and all(row["consistent"] for row in intersections):
        expected_terminal = "R07_760_JOINT_COEFF_INTERSECTION_NONEMPTY"
    elif task168["terminal_token"] == "R07_760_L3_TARGET6_INPUT_STOP":
        expected_terminal = "R07_760_JOINT_COEFF_INPUT_STOP"
    else:
        expected_terminal = "R07_760_JOINT_COEFF_UNKNOWN_RESOURCE"
    require(receipt["terminal_token"] == expected_terminal,
            "independent task169 terminal semantics")
    return {"joint_certificate_count": checked,
            "adjacent_inclusion_count": len(expected_inclusions),
            "task168_state_commitments_authenticated": True,
            "positive_D2_check_conditional_on_authenticated_task168_state": True,
            "full_D2_columns_regenerated_by_checker": False}


def validate_envelope(receipt: dict[str, Any],
                      domain_seconds: float) -> None:
    domain_seconds = validate_domain_seconds(domain_seconds)
    verify_self_digest(receipt, "target receipt")
    require(receipt.get("task169_domain_resource_policy") == {
        "domain_seconds": domain_seconds,
        "default_local_domain_seconds": MAX_DOMAIN_SECONDS,
        "maximum_GHA_domain_seconds": MAX_GHA_DOMAIN_SECONDS,
        "separate_from_task168_full_search_seconds": True,
        "not_part_of_mathematical_universe": True,
    }, "target receipt domain resource policy")
    expected_boundaries = BOUNDARIES if (
        receipt.get("mode") == "preflight" or
        "registered_joint_domain" in receipt) else STOP_BOUNDARIES
    require(receipt.get("schema") == TARGET_SCHEMA and
            receipt.get("grade") == "CANDIDATE" and
            receipt.get("claim_boundaries") == expected_boundaries and
            all(receipt.get(key) is value
                for key, value in expected_boundaries.items()) and
            receipt.get("claims") == FALSE_CLAIMS and
            receipt.get("proof108_read_but_not_consumed") is True and
            receipt.get("proof109_read_but_not_consumed") is True,
            "target receipt envelope")
    if receipt.get("mode") == "preflight":
        require(receipt.get("preflight_state") == PREFLIGHT_STATE and
                receipt.get("status") == PREFLIGHT_STATE and
                receipt.get("mutation_tests_rejected") == 19 and
                receipt.get("full_j9_run_locally") is False and
                receipt.get("parallel_local_computation") is False,
                "target preflight envelope")
        structural = receipt.get("structural_mutation_tests_rejected", {})
        require(structural.get("all_31_context_ids") == 31 and
                structural.get("all_46_named_aliases") == 46 and
                structural.get("all_3_relation_layers") == 3 and
                structural.get("all_27_transversals") == 27 and
                structural.get("all_28_schreier_sign_rows") == 28 and
                structural.get("all_56_exponent_entries") == 56 and
                structural.get("task168_aggregate_state_commitment") == 1 and
                structural.get("all_forbidden_claims") == 10,
                "target indexed structural mutations")
    else:
        require(receipt.get("mode") == "full" and
                receipt.get("terminal_token") in TERMINALS and
                receipt.get("status") == receipt["terminal_token"] and
                receipt.get("result", {}).get("state") ==
                    receipt["terminal_token"],
                "target full terminal envelope")


def check_receipt(path: Path, checkpoint_dir: Path,
                  domain_seconds: float) -> dict[str, Any]:
    domain_seconds = validate_domain_seconds(domain_seconds)
    pins = authenticate_sources()
    raw = path.read_bytes()
    receipt = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(receipt) + b"\n",
            "canonical target receipt bytes")
    expected_manifest = {key: value for key, value in pins.items()
                         if key != "producer"}
    require(receipt.get("producer_source") == pins["producer"] and
            receipt.get("pin_manifest") == expected_manifest and
            receipt.get("pin_manifest_sha256") ==
                digest_obj(expected_manifest),
            "target receipt source and complete input pin manifest")
    validate_envelope(receipt, domain_seconds)
    cache_fixture = exact_transition_cache_fixture()
    empty_affine_regression = independent_empty_affine_regression()
    receipt_mutations = mutation_tests(receipt, domain_seconds)
    ctx = context()
    domain_result = None
    full_result = None
    if "registered_joint_domain" in receipt:
        require(receipt["registered_joint_domain"]["resource_accounting"]
                    ["registered_wall_seconds_cap"] == domain_seconds,
                "checker domain-seconds receipt/domain propagation")
        domain_result = independent_domain_check(
            receipt, ctx, domain_seconds)
    else:
        require(receipt.get("terminal_token") in {
                    "R07_760_JOINT_COEFF_UNKNOWN_RESOURCE",
                    "R07_760_JOINT_COEFF_INPUT_STOP"},
                "missing domain only on stopped terminal")
    if receipt["mode"] == "full" and domain_result is not None:
        full_result = check_full_intersections(
            receipt, ctx, checkpoint_dir)
    output = {
        "schema": SCHEMA, "grade": "CROSS_CHECKED",
        "target_path": path.as_posix(),
        "target_bytes": len(raw),
        "target_sha256": hashlib.sha256(raw).hexdigest(),
        "target_self_digest_sha256": receipt["self_digest_sha256"],
        "target_terminal_token": receipt.get("terminal_token"),
        "source_pin_manifest": pins,
        "source_pin_manifest_sha256": digest_obj(pins),
        "domain_crosscheck": domain_result,
        "completed_j_crosscheck": full_result,
        "exact_transition_cache_fixture": cache_fixture,
        "independent_empty_affine_regression": empty_affine_regression,
        "mutation_tests_rejected": receipt_mutations,
        "helper_shared_with_task169_producer": False,
        "imports_task169_producer": False,
        "full_j9_recomputed": False,
        "task169_domain_seconds": domain_seconds,
        "full_E4_positive_class_reconstructed": False,
        "true_PB4_D2_equality_used": False,
        "literal_A18_replayed": False,
        "claims": FALSE_CLAIMS,
        "status": "CROSSCHECK_PASS",
    }
    output["self_digest_sha256"] = digest_obj(output)
    return output


def resign(data: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(data)
    row.pop("self_digest_sha256", None)
    row["self_digest_sha256"] = digest_obj(row)
    return row


def mutation_tests(receipt: dict[str, Any],
                   domain_seconds: float) -> int:
    rejected = 0
    total = 0
    def mutation(path: Sequence[Any], value: Any) -> None:
        nonlocal rejected, total
        row = copy.deepcopy(receipt)
        target: Any = row
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        row = resign(row)
        total += 1
        try:
            validate_envelope(row, domain_seconds)
            verify_self_digest(row["registered_joint_domain"],
                               "mutated domain")
            regression = row["task168_regression"]
            require(regression["task168_preflight_sha256"] ==
                    digest_obj(row["embedded_task168_preflight"]),
                    "mutated task168 commitment")
        except RuntimeError:
            rejected += 1
    mutation(["registered_joint_domain", "context_registry",
              "target6_binding", "registry_context_ids", 0], 2)
    mutation(["registered_joint_domain", "context_registry",
              "target6_binding", "named_alias_rows", 0, "context_id"], 2)
    mutation(["registered_joint_domain", "relation_roster", "rows", 6318,
              "layer_ordinal"], 6319)
    mutation(["registered_joint_domain", "Delta3_and_Schreier",
              "positive_BFS_transversal_words", 1], [2])
    mutation(["registered_joint_domain", "Delta3_and_Schreier",
              "ordered_schreier_words", 0, 0], -1)
    mutation(["registered_joint_domain", "historical_exponent_gate",
              "two_exponent_rows_on_28_schreier_words", 0, 0], 1)
    coefficient_path = ["registered_joint_domain", "RS_abelianization",
                        "word_bearing_first_independent_input_rows", 0,
                        "coefficient_row", 0]
    coefficient_original = receipt["registered_joint_domain"][
        "RS_abelianization"]["word_bearing_first_independent_input_rows"][0][
            "coefficient_row"][0]
    mutation(coefficient_path, (coefficient_original + 1) % 3)
    mutation(["registered_joint_domain", "RS_abelianization",
              "word_bearing_first_independent_input_rows", 0,
              "source_relation_binding", "157ee_layer"], "q0_relations")
    mutation(["task168_regression", "task168_preflight_sha256"], "0" * 64)
    evaluator_path = ["registered_joint_domain", "relation_roster",
                      "exact_transition_evaluator"]
    mutation(evaluator_path + ["joint_transition_cache_entries"], -1)
    mutation(evaluator_path + ["legacy_group_eval_canary_rows", 0,
                               "E3_and_31_E4_value_blobs", 0], "00")
    mutation(evaluator_path + ["legacy_group_eval_canary_global_ordinals", 0],
             2)
    mutation(["registered_joint_domain", "relation_roster",
              "direct_full_Omega_relation_evaluation_digest_sha256"],
             "0" * 64)
    for key in ("full_E4_positive_class_reconstructed",
                "true_PB4_D2_equality_used", "literal_A18_replayed",
                "two_hexagons_replayed_as_joint_system",
                "HT1_HT5_all_edges_proved", "cofinal_compatibility_proved"):
        mutation([key], True)
    for key in FALSE_CLAIMS:
        mutation(["claims", key], True)
    require(rejected == total == 23, "checker mutation rejection")
    return rejected


def atomic_write(path: Path, raw: bytes) -> None:
    full = path if path.is_absolute() else ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    temporary = full.with_name(full.name + ".tmp")
    require(not temporary.exists(), "checker temporary collision")
    temporary.write_bytes(raw)
    temporary.replace(full)


def self_test(domain_seconds: float) -> None:
    target = ROOT / DEFAULT_RECEIPT
    require(target.is_file(), "checker selftest needs finalized preflight")
    raw = target.read_bytes()
    receipt = json.loads(raw.decode("ascii"))
    validate_envelope(receipt, domain_seconds)
    result = check_receipt(target, DEFAULT_CHECKPOINT_DIR, domain_seconds)
    verify_self_digest(result, "checker selftest result")
    print(FINAL_MARKER + "_SELFTEST_PASS "
          f"relations={result['domain_crosscheck']['relation_count']} "
          f"RS_rows={result['domain_crosscheck']['RS_row_count']} "
          f"rank_B_joint={result['domain_crosscheck']['rank_B_joint']} "
          f"mutations={result['mutation_tests_rejected']} "
          f"cache_fixture_words={result['exact_transition_cache_fixture']['word_count']} "
          f"cache_fixture_mutations={result['exact_transition_cache_fixture']['mutation_tests_rejected']} "
          "empty_affine_inconsistent=true "
          f"canaries={LEGACY_CANARY_COUNT} "
          f"domain_seconds={domain_seconds:g} "
          "full_j9_recomputed=false", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--domain-seconds", type=float,
                        default=MAX_DOMAIN_SECONDS)
    args = parser.parse_args()
    domain_seconds = validate_domain_seconds(args.domain_seconds)
    require(args.self_test is not args.check, "select checker mode")
    if args.self_test:
        self_test(domain_seconds)
        return 0
    receipt_path = args.receipt if args.receipt.is_absolute() \
        else ROOT / args.receipt
    result = check_receipt(
        receipt_path, args.checkpoint_dir, domain_seconds)
    raw = canonical_bytes(result) + b"\n"
    atomic_write(args.output, raw)
    terminal = result.get("target_terminal_token")
    rank = -1 if result["domain_crosscheck"] is None else \
        result["domain_crosscheck"]["rank_B_joint"]
    print(FINAL_MARKER +
          f" target_sha256={result['target_sha256']} "
          f"terminal={terminal} rank_B_joint={rank} "
          f"mutations={result['mutation_tests_rejected']} "
          f"cache_fixture_words={result['exact_transition_cache_fixture']['word_count']} "
          f"cache_fixture_mutations={result['exact_transition_cache_fixture']['mutation_tests_rejected']} "
          "empty_affine_inconsistent=true "
          f"canaries={LEGACY_CANARY_COUNT} "
          f"domain_seconds={domain_seconds:g} "
          f"bytes={len(raw)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
