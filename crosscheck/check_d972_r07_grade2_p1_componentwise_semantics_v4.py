#!/usr/bin/env python3
"""Independent componentwise P1 semantic checker for the R07 Task554 state.

This file deliberately contains its own quotient, affine/Fox, packed-F3 and
state-replay kernels.  It does not import the Task709/711 producer, the v4
producer, or the structural producer.  The producer is used only as a
receipt-bearing peer: its arithmetic is replayed independently here.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import math
import os
import re
import stat
import sys
import tempfile
import time
from collections import deque
from pathlib import Path
from typing import Any, Iterable

import numpy as np

try:
    import resource
except ImportError:  # pragma: no cover - Windows
    resource = None


ROOT = Path(__file__).resolve().parents[1]

# Immutable Task554 ancestry and dimensions.
SOURCE_RUN = "33677346616"
SOURCE_ATTEMPT = "1"
SOURCE_HEAD = "22c6dddb43d107c05e65f53ad898823ae8ebe276"
PREPARE_DIGEST = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
PARENTS = (
    "9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01",
)
BASIS = (
    "cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39",
    "0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461",
    "602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6",
    "4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9",
)
WORDS_SHA = "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"
PERMS_SHA = "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"
OLD_RANKS = (505, 503, 503, 503)
NEW_RANKS = (1509, 1512, 1512, 1512)
ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
ACTORS = (1, -1, 2, -2)
ETA = ((0, 1), (1, 0), (1, 1))
MONOMIALS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
OO = (([1], [2]), ([1], [-1, -2]), ([2], [-1, -2]),
      ([-2, -1], [1]), ([1], [2]), ([-2, -1], [2]))
PURE_Q1_WORDS = {
    (0, 0): (),
    (0, 1): (-2,) * 9,
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}

SOURCE_BASE = 6048
SOURCE_BLOCK = 18144
SOURCE_TOTAL = 72576
PHYSICAL_LOWER_REGULAR = 8064
PHYSICAL_LOWER = 8068
PHYSICAL_GRADE = 24192
LOWER_AUX = 8
LOWER_WIDTH = 6056
PACKED_WIDTH = SOURCE_BLOCK // 4
CLAIMS = {
    "A0": False,
    "COMMON": False,
    "COMPATIBLE_LIFT": False,
    "FAKE": False,
    "FULL_Q0": False,
    "IHARA": False,
    "ORDER_54432": False,
    "verified": False,
}
FALSE_FIELDS = (
    "resident_global_matrix", "independent_checker", "precision2", "A0",
    "COMMON", "COMPATIBLE_LIFT", "FAKE", "IHARA", "verified",
)
MARKER = "R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS"
CHECKER_SCHEMA = "d972.r07.p1.componentwise.independent.v1"
STATE_SCHEMA = "d972.r07.a0.first-rung-grade1.v3"
SEALED_HEAD_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state.head"

# This is a provenance path, not an executable dependency.  The checker never
# imports it; the digest binds every peer receipt to the accepted producer v5.
PRODUCER_V5_SOURCE = ROOT / "search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py"
PRODUCER_V5_SHA = "dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf"

# The v4 input manifest is reconstructed from bytes rather than imported.
INPUT_PINS = {
    "sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md": "5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb",
    "sol/sol_reply_544_audit_r07_a0_relative_fibre_echelon_v1.md": "7875fa2641355c8d6d09248b23c9fa9c766f48db751d34b90826ab609b457eb3",
    "sol/proof_r07_a0_explicit_g9_two_rung_twisting_v442.md": "afa91b6137f8321522cf97fa11502213bde45c7c4c325b3b2ad28e8f6e844de4",
    "sol/sol_reply_548_audit_r07_a0_explicit_g9_two_rung_twisting_v1.md": "bd1b0239e0410f2ab63abd30e7ff9a422528d141138cfeafc8ca3960da1cd834",
    "sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md": "80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c",
    "sol/proof_r07_filtered_transition_defect_closure_v444.md": "705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645",
    "sol/sol_reply_550_audit_r07_a0_affine_engine_transition_defects_v1.md": "329aa9b8c8b87e5672938cb70ab99dbf365b59a0e63468a3df58420ee26e4616",
    "sol/proof_r07_first_rung_character_blocks_coupled_monomials_v446.md": "389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756",
    "sol/sol_reply_553_audit_r07_a0_character_blocks_coupled_monomials_v1.md": "9e06ae4022e6267846561b13fed2f64a73909ba0d3b68436173763cf6bdba1df",
    "sol/sol_reply_549_audit_r07_a0_order2016_literal_member_v1.md": "a088d27203e2064ac8240b813fd15e905ec82633b93b829e89b4a073f111256c",
    "sol/sol_reply_547_audit_r07_a0_psl504_canonical_payload_v1.md": "84029c2f64ac8a20f83d9680e2b105f6994db140c4062d8e5c8f99228f7ab32f",
    "search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json": "e55b7dfa5a0876054b05259f115266c0b2651431f1f2670efe85e9b34c94222b",
    "search/d972_r07_a0_c2fourier_joint_floor_v1.py": "6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba",
    "scratchpad/a0_paper_words_v1.json": WORDS_SHA,
    "scratchpad/fuda1_a0_rmax_data.g": PERMS_SHA,
    "sol/proof_r07_first_rung_character_projector_word_repair_v447.md": "3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2",
    "sol/proof_r07_first_rung_six_grade_index_repair_v449.md": "0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9",
    "sol/sol_reply_555_audit_r07_a0_six_grade_schedule_v1.md": "8dcdfbb4825c65bff9698311b735e830c27d39f98405bcfb01af3411d97a2e45",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
             ensure_ascii=True) + "\n").encode("ascii")


def fail(reason: str) -> None:
    raise RuntimeError(reason)


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def finite_float(value: Any, reason: str) -> None:
    require((isinstance(value, (int, float)) and not isinstance(value, bool)
             and math.isfinite(float(value)) and float(value) >= 0), reason)


class ResourceExhausted(RuntimeError):
    """A bounded resource stop; no semantic certificate may be emitted."""


def guard(started: float, phase: str) -> None:
    seconds = float(os.environ.get("D972_P1_CHECKER_SECONDS", "21600"))
    if time.monotonic() - started > seconds:
        raise ResourceExhausted(f"UNKNOWN_RESOURCE:{phase}:time_cap")
    if resource is not None:
        # Linux ru_maxrss is KiB; Windows has no resource module.
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if sys.platform != "darwin":
            rss *= 1024
        limit = int(os.environ.get("D972_P1_CHECKER_MAX_RSS", str(8 * 1024**3)))
        if rss > limit:
            raise ResourceExhausted(f"UNKNOWN_RESOURCE:{phase}:rss_cap")


def progress(phase: str, current: int, total: int, *, force: bool = False) -> None:
    if force or current == total or current <= 2 or current % 256 == 0:
        print(json.dumps({"phase": phase, "current": current, "total": total},
                         separators=(",", ":")), flush=True)


# ---------------------------------------------------------------------------
# Independent quotient / affine / Fox arithmetic

ID9 = tuple(range(9))
Affine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]


def perm_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(right[left[i]] for i in range(len(left)))


def perm_inv(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for i, j in enumerate(value):
        out[j] = i
    return tuple(out)


def word_inv(word: Iterable[int]) -> list[int]:
    return [-int(x) for x in reversed(tuple(word))]


def word_mul(*words: Iterable[int]) -> list[int]:
    out: list[int] = []
    for word in words:
        for x in word:
            x = int(x)
            require(x in (-2, -1, 1, 2), "word_letter")
            if out and out[-1] == -x:
                out.pop()
            else:
                out.append(x)
    return out


def word_sub(word: Iterable[int], x: Iterable[int], y: Iterable[int]) -> list[int]:
    return word_mul(*[(list(x) if q == 1 else list(y) if q == 2 else
                       word_inv(x) if q == -1 else word_inv(y)) for q in word])


def qmul(left: tuple[tuple[int, ...], int, int],
         right: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return perm_mul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2]


def qinv(value: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return perm_inv(value[0]), value[1], value[2]


def qeval(word: Iterable[int], images: tuple[tuple[tuple[int, ...], int, int],
                                                tuple[tuple[int, ...], int, int]]) -> tuple[tuple[int, ...], int, int]:
    value = (ID9, 0, 0)
    inverses = (qinv(images[0]), qinv(images[1]))
    for letter in word:
        value = qmul(value, images[abs(int(letter)) - 1] if letter > 0
                     else inverses[abs(int(letter)) - 1])
    return value


def cv(label: tuple[int, int], a: int, b: int) -> int:
    return 1 if ((label[0] * a + label[1] * b) & 1) == 0 else 2


def xor_label(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] ^ right[0], left[1] ^ right[1]


def sign_kernel(parity: tuple[int, int], vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((cv(ETA[i], parity[0], parity[1]) * vector[i]) % 3
                 for i in range(3))  # type: ignore[return-value]


def affine_mul(left: Affine, right: Affine) -> Affine:
    acted = sign_kernel((right[1], right[2]), left[3])
    return (perm_mul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2],
            tuple((acted[i] + right[3][i]) % 3 for i in range(3)))


def affine_inv(value: Affine) -> Affine:
    acted = sign_kernel((value[1], value[2]), value[3])
    return (perm_inv(value[0]), value[1], value[2],
            tuple((-x) % 3 for x in acted))


def affine_eval(word: Iterable[int], images: tuple[Affine, Affine]) -> Affine:
    value: Affine = (ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for letter in word:
        value = affine_mul(value, images[abs(int(letter)) - 1] if letter > 0
                           else inverses[abs(int(letter)) - 1])
    return value


def affine_fox(word: Iterable[int], images: tuple[Affine, Affine]) -> tuple[dict[tuple[int, Affine], int], Affine]:
    out: dict[tuple[int, Affine], int] = {}
    prefix: Affine = (ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for raw in word:
        letter = int(raw)
        generator = abs(letter) - 1
        if letter > 0:
            key = generator, prefix
            out[key] = (out.get(key, 0) + 1) % 3
            prefix = affine_mul(prefix, images[generator])
        else:
            prefix = affine_mul(prefix, inverses[generator])
            key = generator, prefix
            out[key] = (out.get(key, 0) - 1) % 3
        if out.get(key) == 0:
            out.pop(key, None)
    return out, prefix


def closure(generators: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[tuple[tuple[int, ...], ...], dict[tuple[int, ...], int]]:
    steps = generators + (perm_inv(generators[0]), perm_inv(generators[1]))
    elements = [ID9]
    index = {ID9: 0}
    todo: deque[tuple[int, ...]] = deque([ID9])
    while todo:
        parent = todo.popleft()
        for generator in steps:
            value = perm_mul(parent, generator)
            if value not in index:
                index[value] = len(elements)
                elements.append(value)
                todo.append(value)
    return tuple(elements), index


def parse_permutations() -> tuple[tuple[int, ...], tuple[int, ...]]:
    path = ROOT / "scratchpad/fuda1_a0_rmax_data.g"
    raw = path.read_bytes()
    require(sha(raw) == PERMS_SHA, "permutation_source_pin")
    match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;",
                      raw.decode("utf-8"), re.S)
    require(match is not None, "permutation_source_parse")
    return tuple(tuple(int(x) - 1 for x in ast.literal_eval(match.group(i)))
                 for i in (1, 2))  # type: ignore[return-value]


def exponents(word: Iterable[int]) -> tuple[int, int]:
    out = [0, 0]
    for raw in word:
        letter = int(raw)
        if abs(letter) == 1:
            out[0] += 1 if letter == 1 else -1
        else:
            out[1] += 1 if letter == 2 else -1
    return tuple(out)


def lower_coord(tag: int, component: int, psl: int) -> int:
    return (tag * 2 + component) * 504 + psl


def grade_coord(tag: int, component: int, monomial: int, psl: int) -> int:
    return ((tag * 2 + component) * 3 + monomial) * 504 + psl


def physical_lower_coord(character: int, block: int, component: int, psl: int) -> int:
    return ((character * 2 + block) * 2 + component) * 504 + psl


def physical_grade_coord(character: int, block: int, component: int, monomial: int, psl: int) -> int:
    return (((character * 2 + block) * 2 + component) * 3 + monomial) * 504 + psl


class Context:
    """Standalone quotient and affine data reconstructed from the two pins."""

    def __init__(self, words: dict[str, Any]):
        q36 = parse_permutations()
        self.a, self.c = q36[0][:9], q36[1][:9]
        self.psels, self.psidx = closure((self.a, self.c))
        require(len(self.psels) == 504, "psl_order")
        self.q1_images = ((self.a, 1, 0), (self.c, 0, 1))
        self.affine_images: tuple[Affine, Affine] = (
            (self.a, 1, 0, (1, 0, 0)),
            (self.c, 0, 1, (1, 1, 1)),
        )
        self.pb3_b = affine_inv(affine_mul(self.affine_images[1], self.affine_images[0]))
        identity = (ID9, 0, 0, (0, 0, 0))
        require(affine_mul(affine_mul(self.affine_images[0], self.pb3_b),
                           self.affine_images[1]) == identity, "pb3_boundary")
        require(affine_inv(self.affine_images[0])[3] == (2, 0, 0), "marked_inverse_a")
        require(affine_inv(self.affine_images[1])[3] == (1, 2, 1), "marked_inverse_c")

        self.transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        self.inverse_transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        self.substitution_matrices: list[list[list[int]]] = []
        for left_word, right_word in OO:
            left = qeval(left_word, self.q1_images)
            right = qeval(right_word, self.q1_images)
            matrix = ((left[1], right[1]), (left[2], right[2]))
            inverse = None
            for aa in range(2):
                for ab in range(2):
                    for ba in range(2):
                        for bb in range(2):
                            candidate = ((aa, ab), (ba, bb))
                            if self.matrix_mul(matrix, candidate) == ((1, 0), (0, 1)) and self.matrix_mul(candidate, matrix) == ((1, 0), (0, 1)):
                                inverse = candidate
            require(inverse is not None, "occurrence_matrix_singular")
            mapping = {
                label: (label[0] * inverse[0][0] ^ label[1] * inverse[1][0],
                        label[0] * inverse[0][1] ^ label[1] * inverse[1][1])
                for label in CHARACTERS
            }
            self.transport.append(mapping)
            self.inverse_transport.append({target: source for source, target in mapping.items()})
            self.substitution_matrices.append([list(matrix[0]), list(matrix[1])])

        self.actor_source_q1 = {letter: qeval((letter,), self.q1_images)
                                for letter in ACTORS}
        self.actor_tags_affine = {
            letter: tuple(affine_eval(word_sub((letter,), *pair), self.affine_images)
                          for pair in OO)
            for letter in ACTORS
        }
        self.actor_tags_q1 = {
            letter: tuple((value[0], value[1], value[2])
                          for value in self.actor_tags_affine[letter])
            for letter in ACTORS
        }
        self.pure_source_affine: dict[tuple[int, int], Affine] = {}
        self.pure_tags_affine: dict[tuple[int, int], tuple[Affine, ...]] = {}
        for parity, word in PURE_Q1_WORDS.items():
            endpoint = qeval(word, self.q1_images)
            require(endpoint == (ID9, parity[0], parity[1]), "pure_q1_endpoint")
            self.pure_source_affine[parity] = affine_eval(word, self.affine_images)
            self.pure_tags_affine[parity] = tuple(
                affine_eval(word_sub(word, *pair), self.affine_images) for pair in OO
            )
        require(isinstance(words, dict), "word_input_shape")
        g760 = words.get("g760")
        require(isinstance(g760, list) and len(g760) == 760, "g760_shape")
        require(all(plain_int(x) and x in (-2, -1, 1, 2) for x in g760), "g760_letters")
        self.g760 = tuple(int(x) for x in g760)
        g_tags = tuple(affine_eval(word_sub(self.g760, *pair), self.affine_images) for pair in OO)
        self.physical_shifts = (
            identity, g_tags[2], g_tags[2],
            affine_mul(g_tags[5], affine_inv(g_tags[4])), g_tags[5], g_tags[5],
        )
        self.aggregate_table = ((0, 0, 1), (1, 0, -1), (2, 0, 1),
                                (3, 1, -1), (4, 1, -1), (5, 1, 1))
        self.psl_maps: dict[tuple[tuple[int, ...], str], np.ndarray] = {}

    @staticmethod
    def matrix_mul(left: tuple[tuple[int, int], tuple[int, int]],
                   right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            (left[0][0] * right[0][0] ^ left[0][1] * right[1][0],
             left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
            (left[1][0] * right[0][0] ^ left[1][1] * right[1][0],
             left[1][0] * right[0][1] ^ left[1][1] * right[1][1]),
        )

    def psl_map(self, permutation: tuple[int, ...]) -> np.ndarray:
        key = tuple(permutation), "left"
        if key not in self.psl_maps:
            self.psl_maps[key] = np.asarray(
                [self.psidx[perm_mul(permutation, value)] for value in self.psels],
                dtype=np.int32)
        return self.psl_maps[key]


def _add_mod3(destination: np.ndarray, source: np.ndarray, scalar: int = 1) -> None:
    c = scalar % 3
    if c:
        destination[:] = (destination.astype(np.uint16) + c * source.astype(np.uint16)) % 3


def _translated_psl(source: np.ndarray, mapping: np.ndarray, scalar: int) -> np.ndarray:
    out = np.zeros(504, dtype=np.uint8)
    out[mapping] = ((scalar % 3) * source.astype(np.uint16)) % 3
    return out


def qnorm_affine(word: Iterable[int], context: Context) -> tuple[list[tuple[int, Affine, int]], int]:
    gradient, endpoint = affine_fox(word, context.affine_images)
    require(endpoint == (ID9, 0, 0, (0, 0, 0)), "q1_literal_endpoint")
    out: dict[tuple[int, Affine], int] = {}
    augmentation = 0
    for (generator, prefix), coefficient in gradient.items():
        if generator == 0:
            augmentation = (augmentation + coefficient) % 3
            first = affine_mul(prefix, context.affine_images[0])
            second = affine_mul(first, context.pb3_b)
            for component, value in ((0, first), (1, second)):
                key = component, value
                out[key] = (out.get(key, 0) - coefficient) % 3
        else:
            key = 1, prefix
            out[key] = (out.get(key, 0) + coefficient) % 3
    return [(component, value, coefficient) for (component, value), coefficient in out.items() if coefficient], augmentation


def evaluate_occurrence_pair(word: tuple[int, ...], context: Context) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lower = np.zeros((4, SOURCE_BASE), dtype=np.uint8)
    grade = np.zeros((4, SOURCE_BLOCK), dtype=np.uint8)
    auxiliary = np.zeros(LOWER_AUX, dtype=np.uint8)
    for tag, pair in enumerate(OO):
        normal, augmentation = qnorm_affine(word_sub(word, *pair), context)
        auxiliary[tag] = augmentation
        for component, value, coefficient in normal:
            psl = context.psidx[value[0]]
            for source_index, source_label in enumerate(CHARACTERS):
                target_label = context.transport[tag][source_label]
                weight = coefficient * cv(target_label, value[1], value[2])
                lower[source_index, lower_coord(tag, component, psl)] = (
                    int(lower[source_index, lower_coord(tag, component, psl)]) + weight) % 3
                for monomial, monomial_coefficient in enumerate(value[3]):
                    if monomial_coefficient:
                        gi = grade_coord(tag, component, monomial, psl)
                        grade[source_index, gi] = (
                            int(grade[source_index, gi]) + weight * monomial_coefficient) % 3
    exponent = exponents(word)
    require(exponent[0] % 18 == 0 and exponent[1] % 18 == 0, "normalized_exponent_not_integral")
    auxiliary[6:] = ((exponent[0] // 18) % 3, (exponent[1] // 18) % 3)
    return lower, grade, auxiliary


def act_pair(context: Context, lower: np.ndarray, grade: np.ndarray,
             auxiliary: np.ndarray, source_actor: Affine,
             tag_actors: tuple[Affine, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    require(lower.shape == (4, SOURCE_BASE) and grade.shape == (4, SOURCE_BLOCK), "paired_shape")
    out_lower = np.zeros_like(lower)
    out_grade = np.zeros_like(grade)
    for source_index, source_label in enumerate(CHARACTERS):
        common_scalar = cv(source_label, source_actor[1], source_actor[2])
        for tag, actor in enumerate(tag_actors):
            mapping = context.psl_map(actor[0])
            target_label = context.transport[tag][source_label]
            for component in (0, 1):
                low_slice = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
                out_lower[source_index, low_slice] = _translated_psl(
                    lower[source_index, low_slice], mapping, common_scalar)
                for monomial in range(3):
                    grade_slice = slice(grade_coord(tag, component, monomial, 0), grade_coord(tag, component, monomial, 0) + 504)
                    _add_mod3(out_grade[source_index, grade_slice], _translated_psl(
                        grade[source_index, grade_slice], mapping, common_scalar))
                    kernel_coefficient = actor[3][monomial]
                    if kernel_coefficient:
                        output_target = xor_label(target_label, ETA[monomial])
                        output_source = context.inverse_transport[tag][output_target]
                        output_index = CHARACTERS.index(output_source)
                        induced_scalar = kernel_coefficient * cv(output_target, actor[1], actor[2])
                        _add_mod3(out_grade[output_index, grade_slice], _translated_psl(
                            lower[source_index, low_slice], mapping, induced_scalar))
    return out_lower, out_grade, auxiliary.copy()


def projected_seed_pair(context: Context,
                        base: tuple[np.ndarray, np.ndarray, np.ndarray],
                        label: tuple[int, int]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lower = np.zeros_like(base[0])
    grade = np.zeros_like(base[1])
    auxiliary = np.zeros_like(base[2])
    for parity in CHARACTERS:
        acted = act_pair(context, base[0], base[1], base[2],
                         context.pure_source_affine[parity],
                         context.pure_tags_affine[parity])
        coefficient = cv(label, parity[0], parity[1])
        _add_mod3(lower, acted[0], coefficient)
        _add_mod3(grade, acted[1], coefficient)
        _add_mod3(auxiliary, acted[2], coefficient)
    selected = CHARACTERS.index(label)
    require(not any(np.any(lower[index]) for index in range(4) if index != selected), "projector_lower_leak")
    require(label == (0, 0) or not np.any(auxiliary), "projector_auxiliary_leak")
    return lower, grade, auxiliary


def associated_lower_actor(context: Context, row: np.ndarray,
                           label: tuple[int, int], letter: int) -> np.ndarray:
    require(row.shape == (LOWER_WIDTH,), "lower_actor_shape")
    out = np.zeros_like(row)
    scalar = cv(label, context.actor_source_q1[letter][1], context.actor_source_q1[letter][2])
    for tag, actor in enumerate(context.actor_tags_q1[letter]):
        mapping = context.psl_map(actor[0])
        for component in (0, 1):
            block = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
            out[block] = _translated_psl(row[block], mapping, scalar)
    out[SOURCE_BASE:] = row[SOURCE_BASE:]
    return out


def exact_actor_on_old_lift(context: Context, lower_row: np.ndarray,
                            grade_flat: np.ndarray, label: tuple[int, int],
                            letter: int) -> np.ndarray:
    lower = np.zeros((4, SOURCE_BASE), dtype=np.uint8)
    lower[CHARACTERS.index(label)] = lower_row[:SOURCE_BASE]
    grade = grade_flat.reshape(4, SOURCE_BLOCK)
    source_value = context.actor_source_q1[letter]
    source_actor = (source_value[0], source_value[1], source_value[2],
                    affine_eval((letter,), context.affine_images)[3])
    _, acted, _ = act_pair(context, lower, grade, lower_row[SOURCE_BASE:],
                           source_actor, context.actor_tags_affine[letter])
    return acted.reshape(SOURCE_TOTAL)


def associated_grade_actor(context: Context, row: np.ndarray,
                           label: tuple[int, int], letter: int) -> np.ndarray:
    require(row.shape == (SOURCE_BLOCK,), "grade_actor_shape")
    out = np.zeros_like(row)
    scalar = cv(label, context.actor_source_q1[letter][1], context.actor_source_q1[letter][2])
    for tag, actor in enumerate(context.actor_tags_q1[letter]):
        mapping = context.psl_map(actor[0])
        for component in (0, 1):
            for monomial in range(3):
                block = slice(grade_coord(tag, component, monomial, 0), grade_coord(tag, component, monomial, 0) + 504)
                out[block] = _translated_psl(row[block], mapping, scalar)
    return out


def aggregate_pair(context: Context, lower: np.ndarray,
                   grade: np.ndarray, auxiliary: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    physical_lower = np.zeros(PHYSICAL_LOWER, dtype=np.uint8)
    physical_grade = np.zeros(PHYSICAL_GRADE, dtype=np.uint8)
    for source_index, source_label in enumerate(CHARACTERS):
        for tag, block, sign in context.aggregate_table:
            shift = context.physical_shifts[tag]
            mapping = context.psl_map(shift[0])
            target_label = context.transport[tag][source_label]
            target_index = CHARACTERS.index(target_label)
            scalar = sign * cv(target_label, shift[1], shift[2])
            for component in (0, 1):
                source_lower = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
                destination_lower = slice(physical_lower_coord(target_index, block, component, 0), physical_lower_coord(target_index, block, component, 0) + 504)
                _add_mod3(physical_lower[destination_lower], _translated_psl(lower[source_index, source_lower], mapping, scalar))
                for monomial in range(3):
                    source_grade = slice(grade_coord(tag, component, monomial, 0), grade_coord(tag, component, monomial, 0) + 504)
                    destination_grade = slice(physical_grade_coord(target_index, block, component, monomial, 0), physical_grade_coord(target_index, block, component, monomial, 0) + 504)
                    _add_mod3(physical_grade[destination_grade], _translated_psl(grade[source_index, source_grade], mapping, scalar))
                    kernel_coefficient = shift[3][monomial]
                    if kernel_coefficient:
                        output_label = xor_label(target_label, ETA[monomial])
                        output_index = CHARACTERS.index(output_label)
                        induced_destination = slice(physical_grade_coord(output_index, block, component, monomial, 0), physical_grade_coord(output_index, block, component, monomial, 0) + 504)
                        induced_scalar = sign * kernel_coefficient * cv(output_label, shift[1], shift[2])
                        _add_mod3(physical_grade[induced_destination], _translated_psl(lower[source_index, source_lower], mapping, induced_scalar))
    for tag, block, sign in context.aggregate_table:
        physical_lower[PHYSICAL_LOWER_REGULAR + block] = (int(physical_lower[PHYSICAL_LOWER_REGULAR + block]) + sign * int(auxiliary[tag])) % 3
    physical_lower[PHYSICAL_LOWER_REGULAR + 2:] = auxiliary[6:]
    return physical_lower, physical_grade


def aggregate_pure(context: Context, block: int, row: np.ndarray) -> np.ndarray:
    lower = np.zeros((4, SOURCE_BASE), dtype=np.uint8)
    grade = np.zeros((4, SOURCE_BLOCK), dtype=np.uint8)
    grade[block] = row
    return aggregate_pair(context, lower, grade, np.zeros(LOWER_AUX, dtype=np.uint8))[1]


# ---------------------------------------------------------------------------
# Independent packed F3 echelon and blob codecs

TRITS = np.asarray([[(value // (3 ** d)) % 3 for d in range(4)]
                    for value in range(81)], dtype=np.uint8)
WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.uint16)
PACKED_AXPY = np.zeros((3, 81, 81), dtype=np.uint8)
for scalar in range(3):
    for left in range(81):
        for right in range(81):
            PACKED_AXPY[scalar, left, right] = int(np.dot(
                (TRITS[left].astype(np.int16) - scalar * TRITS[right].astype(np.int16)) % 3,
                WEIGHTS))
PACKED_SCALE2 = np.asarray([
    int(np.dot((2 * TRITS[value]) % 3, WEIGHTS)) for value in range(81)
], dtype=np.uint8)
PACKED_FIRST = np.asarray([
    next((d for d, coefficient in enumerate(TRITS[value]) if coefficient), 4)
    for value in range(81)
], dtype=np.uint8)


def pack_trits(row: np.ndarray) -> np.ndarray:
    flat = np.asarray(row, dtype=np.uint8).reshape(-1)
    require(flat.size % 4 == 0 and not np.any(flat > 2), "pack_trits")
    return np.sum(flat.reshape(-1, 4).astype(np.uint16) * WEIGHTS,
                  axis=1).astype(np.uint8)


def unpack_trits(row: np.ndarray, width: int) -> np.ndarray:
    packed = np.asarray(row, dtype=np.uint8).reshape(-1)
    require(plain_int(width) and width > 0 and width % 4 == 0,
            "unpack_width")
    require(packed.size * 4 == width and not np.any(packed > 80),
            "packed_row_shape")
    return TRITS[packed].reshape(-1).copy()


def packed_matrix_bytes(matrix: np.ndarray) -> bytes:
    array = np.asarray(matrix, dtype=np.uint8)
    require(array.ndim in (1, 2), "packed_matrix_rank")
    flat = array.reshape(-1)
    require(flat.size % 4 == 0 and not np.any(flat > 2),
            "packed_matrix_trits")
    return pack_trits(flat).tobytes(order="C")


def sparse_digest(row: np.ndarray) -> str:
    encoded = [[int(index), int(row[index])] for index in np.flatnonzero(row)]
    return sha(json.dumps(encoded, separators=(",", ":")).encode("ascii"))


class PackedEchelon:
    """Packed row owner with literal reductions and normalized DAG nodes."""

    def __init__(self, width: int):
        require(plain_int(width) and width > 0 and width % 4 == 0,
                "echelon_width")
        self.width = width
        self.packed_width = width // 4
        self.rows: list[np.ndarray] = []
        self.leads: list[int] = []
        self.lead_to_pivot: dict[int, int] = {}

    @staticmethod
    def coefficient(row: np.ndarray, coordinate: int) -> int:
        require(plain_int(coordinate) and 0 <= coordinate < row.size * 4,
                "coefficient_coordinate")
        return int((int(row[coordinate // 4]) // (3 ** (coordinate % 4))) % 3)

    def reduce_packed(self, row: np.ndarray) -> tuple[np.ndarray, list[list[int]]]:
        work = np.asarray(row, dtype=np.uint8).reshape(-1).copy()
        require(work.shape == (self.packed_width,) and not np.any(work > 80),
                "echelon_input")
        reductions: list[list[int]] = []
        cursor = 0
        while cursor < self.packed_width:
            if int(work[cursor]) == 0:
                cursor += 1
                continue
            lead = 4 * cursor + int(PACKED_FIRST[int(work[cursor])])
            pivot = self.lead_to_pivot.get(lead)
            if pivot is None:
                break
            coefficient = self.coefficient(work, lead)
            work = PACKED_AXPY[coefficient, work, self.rows[pivot]].copy()
            reductions.append([pivot, coefficient])
            # Revisit the same byte after subtraction.  This preserves the
            # producer's packed Gaussian order without a dense row.
        return work, reductions

    def accept_remainder(self, remainder: np.ndarray,
                         reductions: list[list[int]]) -> dict[str, Any]:
        nonzero = np.flatnonzero(remainder)
        if not len(nonzero):
            return {"accepted": False, "reductions": reductions}
        byte_index = int(nonzero[0])
        lead = 4 * byte_index + int(PACKED_FIRST[int(remainder[byte_index])])
        leading_coefficient = self.coefficient(remainder, lead)
        require(leading_coefficient in (1, 2), "echelon_leading_coefficient")
        scale = 1 if leading_coefficient == 1 else 2
        normalized = remainder if scale == 1 else PACKED_SCALE2[remainder]
        pivot = len(self.rows)
        self.rows.append(np.asarray(normalized, dtype=np.uint8).copy())
        self.leads.append(lead)
        require(lead not in self.lead_to_pivot, "echelon_duplicate_lead")
        self.lead_to_pivot[lead] = pivot
        return {"accepted": True, "pivot": pivot, "lead": lead,
                "leading_coefficient": leading_coefficient, "scale": scale,
                "reductions": reductions}

    def insert(self, row: np.ndarray) -> dict[str, Any]:
        array = np.asarray(row, dtype=np.uint8).reshape(-1)
        packed = pack_trits(array) if array.shape == (self.width,) else array
        remainder, reductions = self.reduce_packed(packed)
        return self.accept_remainder(remainder, reductions)

    def dense_row(self, pivot: int) -> np.ndarray:
        require(plain_int(pivot) and 0 <= pivot < len(self.rows),
                "echelon_pivot")
        return unpack_trits(self.rows[pivot], self.width)

    def matrix_bytes(self) -> bytes:
        if not self.rows:
            return b""
        return np.stack(self.rows).astype(np.uint8, copy=False).tobytes(order="C")


def expression_from_insert(record: dict[str, Any]) -> list[list[int]]:
    expression = [list(pair) for pair in record["reductions"]]
    if record["accepted"]:
        expression.append([int(record["pivot"]), int(record["leading_coefficient"])])
    return expression


def compare_bytes(actual: bytes | bytearray, expected: bytes | bytearray,
                 reason: str) -> None:
    require(bytes(actual) == bytes(expected), reason)


def validate_expression(expression: Any, rank: int, reason: str,
                        *, earlier_than: int | None = None) -> None:
    require(isinstance(expression, list), reason + ":shape")
    bound = rank if earlier_than is None else earlier_than
    require(plain_int(bound) and 0 <= bound <= rank, reason + ":bound")
    for pair in expression:
        require(isinstance(pair, list) and len(pair) == 2
                and plain_int(pair[0]) and plain_int(pair[1])
                and 0 <= pair[0] < bound and pair[1] in (1, 2),
                reason + ":entry")


def validate_actor_order(order: Any) -> None:
    require(isinstance(order, list) and len(order) == 4
            and all(plain_int(x) for x in order)
            and tuple(order) == ACTORS, "actor_order")


def validate_prior_expression(expression: Any, pivot: int) -> None:
    validate_expression(expression, pivot, "prior_expression", earlier_than=pivot)


# ---------------------------------------------------------------------------
# Safe roots, canonical state envelopes, and authenticated blob streams

def is_reparse(info: os.stat_result) -> bool:
    return bool(getattr(info, "st_file_attributes", 0) & 0x400)


def stable_identity(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return (int(info.st_dev), int(info.st_ino), int(info.st_size),
            int(info.st_mtime_ns), int(info.st_ctime_ns))


def require_regular(path: Path) -> os.stat_result:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and not stat.S_ISLNK(info.st_mode)
            and not is_reparse(info), "unsafe_regular_file:" + path.name)
    return info


def safe_root(root: Path) -> tuple[Path, list[str]]:
    root = Path(root)
    info = root.lstat()
    require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode)
            and not is_reparse(info), "unsafe_root")
    resolved = root.resolve(strict=True)
    names: list[str] = []
    for member in resolved.iterdir():
        require_regular(member)
        names.append(member.name)
    require(len({name.casefold() for name in names}) == len(names),
            "root_case_collision")
    return resolved, names


def exact_roster(names: list[str], expected: Iterable[str]) -> None:
    expected_list = list(expected)
    require(all(isinstance(name, str) and Path(name).name == name
                for name in expected_list), "roster_basename")
    require(len(names) == len(expected_list) and set(names) == set(expected_list),
            "root_roster")


def read_canonical(path: Path) -> tuple[Any, bytes]:
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        fail("json:" + str(exc))
    require(raw == canonical(value), "noncanonical_json:" + path.name)
    return value, raw


def read_sealed(root: Path, stem: str, digest: str,
                parent: str | None) -> tuple[dict[str, Any], bytes]:
    head, head_raw = read_canonical(root / f"{stem}.HEAD")
    expected_head = {"body_sha256": digest, "parent_sha256": parent,
                     "schema": SEALED_HEAD_SCHEMA, "stem": stem}
    require(isinstance(head, dict) and set(head) == set(expected_head)
            and head == expected_head, "sealed_head:" + stem)
    body_path = root / f"{stem}.{digest}.json"
    body, body_raw = read_canonical(body_path)
    require(isinstance(body, dict) and sha(body_raw) == digest,
            "sealed_body_hash:" + stem)
    return body, body_raw


def validate_blob_receipt(root: Path, receipt: Any, rows: int,
                          width: int, *, read: bool = True) -> tuple[Path, bytes | None]:
    required = {"file", "bytes", "sha256", "rows", "width", "encoding"}
    require(isinstance(receipt, dict) and set(receipt) == required,
            "blob_receipt_shape")
    require(plain_int(rows) and rows >= 0 and plain_int(width) and width > 0
            and width % 4 == 0, "blob_expected_dimensions")
    filename = receipt["file"]
    expected_bytes = rows * (width // 4)
    require(isinstance(filename, str) and Path(filename).name == filename
            and re.fullmatch(r"[A-Za-z0-9_.-]+\.[0-9a-f]{64}\.bin", filename)
            and isinstance(receipt["sha256"], str)
            and re.fullmatch(r"[0-9a-f]{64}", receipt["sha256"]) is not None
            and filename.endswith("." + receipt["sha256"] + ".bin")
            and plain_int(receipt["rows"]) and plain_int(receipt["width"])
            and plain_int(receipt["bytes"])
            and receipt["rows"] == rows and receipt["width"] == width
            and receipt["bytes"] == expected_bytes
            and receipt["encoding"] == "base3-four-trits-per-byte",
            "blob_receipt_semantics")
    path = root / filename
    before = require_regular(path)
    before_identity = stable_identity(before)
    require(before.st_size == expected_bytes, "blob_size:" + filename)
    if not read:
        return path, None
    digest = hashlib.sha256()
    count = 0
    chunks: list[bytes] = []
    started = time.monotonic()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1 << 20)
            if not chunk:
                break
            require(max(chunk) <= 80, "packed_byte:" + filename)
            digest.update(chunk)
            count += len(chunk)
            chunks.append(chunk)
            guard(started, "blob-auth")
    after = require_regular(path)
    require(stable_identity(after) == before_identity,
            "blob_changed_during_authentication:" + filename)
    require(count == expected_bytes and digest.hexdigest() == receipt["sha256"],
            "blob_sha256:" + filename)
    return path, b"".join(chunks)


def authenticate_stream(path: Path, receipt: dict[str, Any],
                        *, expected_rows: int, expected_width: int) -> tuple[int, int, int, int, int]:
    # Receipt shape is checked here too so packet streams are independently
    # authenticated before any character range is consumed.
    validate_blob_receipt(path.parent, receipt, expected_rows, expected_width, read=False)
    before = stable_identity(require_regular(path))
    expected = expected_rows * (expected_width // 4)
    digest = hashlib.sha256()
    count = 0
    started = time.monotonic()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1 << 20)
            if not chunk:
                break
            require(max(chunk) <= 80, "packet_byte")
            digest.update(chunk)
            count += len(chunk)
            guard(started, "packet-auth")
    after = stable_identity(require_regular(path))
    require(count == expected and digest.hexdigest() == receipt["sha256"],
            "packet_digest")
    require(before == after, "packet_changed")
    return before


def packet_seek(stream: Any, begin: int, end: int, row_bytes: int,
                *, expected_begin: int | None = None) -> None:
    require(plain_int(begin) and plain_int(end) and 0 <= begin <= end,
            "packet_range")
    require(plain_int(row_bytes) and row_bytes > 0, "packet_row_bytes")
    if expected_begin is not None:
        require(begin == expected_begin, "packet_origin_offset")
    stream.seek(begin * row_bytes)
    require(stream.tell() == begin * row_bytes, "packet_seek")


def packet_finish(stream: Any, end: int, row_bytes: int,
                  *, eof: bool = False) -> None:
    require(stream.tell() == end * row_bytes, "packet_position")
    if eof:
        require(stream.read(1) == b"", "packet_trailing")


def read_exact(stream: Any, size: int, reason: str) -> bytes:
    raw = stream.read(size)
    require(len(raw) == size, reason + ":eof")
    require(max(raw, default=0) <= 80, reason + ":byte")
    return raw


def pinned_input_manifest() -> dict[str, dict[str, Any]]:
    receipt: dict[str, dict[str, Any]] = {}
    for relative, expected in INPUT_PINS.items():
        path = ROOT / relative
        raw = path.read_bytes()
        actual = sha(raw)
        require(actual == expected, "input_pin:" + relative)
        receipt[relative] = {"bytes": len(raw), "sha256": actual}
    # This extra gate binds the words used by all arithmetic, independently of
    # the producer's receipt.
    words_path = ROOT / "scratchpad/a0_paper_words_v1.json"
    words_raw = words_path.read_bytes()
    require(sha(words_raw) == WORDS_SHA, "word_input_pin")
    return receipt


def load_words() -> dict[str, Any]:
    path = ROOT / "scratchpad/a0_paper_words_v1.json"
    raw = path.read_bytes()
    require(sha(raw) == WORDS_SHA, "word_input_pin")
    try:
        words = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        fail("word_input_json:" + str(exc))
    require(isinstance(words, dict), "word_input_shape")
    relators = words.get("relators")
    require(isinstance(relators, list) and len(relators) == 44,
            "relator_count")
    for word in relators:
        require(isinstance(word, list) and all(plain_int(x) and x in (-2, -1, 1, 2)
                                               for x in word), "relator_word")
    return words


def projector_identity(context: Context) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return the producer-compatible projector and a fuller checker object."""
    entries = []
    for parity in CHARACTERS:
        source = context.pure_source_affine[parity]
        require(source[0] == ID9 and (source[1], source[2]) == parity,
                "projector_q1_endpoint")
        tags = []
        for value in context.pure_tags_affine[parity]:
            tags.append({"parity": [int(value[1]), int(value[2])],
                         "kernel": [int(x) for x in value[3]]})
        entries.append({
            "parity": list(parity),
            "word": list(PURE_Q1_WORDS[parity]),
            "q1_endpoint": {"psl_identity": True,
                            "parity": [int(source[1]), int(source[2])]},
            "q2_kernel": [int(x) for x in source[3]],
            "tag_values": tags,
        })
    table = [sum(cv(label, a, b) for label in CHARACTERS) % 3
             for a, b in CHARACTERS]
    require(table == [1, 0, 0, 0], "projector_walsh_table")
    pure_words = [[list(label), list(PURE_Q1_WORDS[label])] for label in CHARACTERS]
    peer = {
        "sum_chi_P_chi_mod3": 1,
        "seed_reconstruction_count": 44,
        "cv_sum_table": table,
        "cv_sum_table_sha256": sha(canonical(table)),
        "pure_words_sha256": sha(canonical(pure_words)),
    }
    full = {"pure_q1_projectors": entries, "walsh_sums": table,
            "walsh_sums_sha256": sha(canonical(table)),
            "pure_words_sha256": sha(canonical(pure_words))}
    return peer, full


def fixed_dimensions() -> dict[str, Any]:
    return {
        "characters": 4,
        "character_labels": [list(x) for x in CHARACTERS],
        "monomials": [list(x) for x in MONOMIALS],
        "monomials_coupled": True,
        "source_base": SOURCE_BASE,
        "source_per_character": SOURCE_BLOCK,
        "source_total": SOURCE_TOTAL,
        "physical_grade": PHYSICAL_GRADE,
        "physical_lower_regular": PHYSICAL_LOWER_REGULAR,
        "physical_lower_with_auxiliary": PHYSICAL_LOWER,
    }


def validate_fixed_dimensions(value: Any) -> None:
    expected = fixed_dimensions()
    require(isinstance(value, dict) and set(value) == set(expected),
            "dimensions_keys")
    require(plain_int(value["characters"]) and value["characters"] == 4,
            "dimensions_characters")
    require(value["character_labels"] == expected["character_labels"]
            and all(isinstance(label, list) and len(label) == 2
                    and all(plain_int(x) and x in (0, 1) for x in label)
                    for label in value["character_labels"]),
            "dimensions_character_labels")
    require(value["monomials"] == expected["monomials"]
            and all(isinstance(monomial, list) and len(monomial) == 3
                    and all(plain_int(x) for x in monomial)
                    for monomial in value["monomials"]),
            "dimensions_monomials")
    require(value["monomials_coupled"] is True, "dimensions_coupled")
    for key, want in (("source_base", SOURCE_BASE),
                      ("source_per_character", SOURCE_BLOCK),
                      ("source_total", SOURCE_TOTAL),
                      ("physical_grade", PHYSICAL_GRADE),
                      ("physical_lower_regular", PHYSICAL_LOWER_REGULAR),
                      ("physical_lower_with_auxiliary", PHYSICAL_LOWER)):
        require(plain_int(value[key]) and value[key] == want,
                "dimensions_" + key)


def validate_character(value: Any, expected: tuple[int, int], reason: str) -> None:
    require(isinstance(value, list) and len(value) == 2
            and all(plain_int(x) and x in (0, 1) for x in value)
            and value == list(expected), reason)


def validate_projector_entries(value: Any) -> None:
    require(isinstance(value, list) and len(value) == 4,
            "projector_entries_shape")
    for index, entry in enumerate(value):
        parity = CHARACTERS[index]
        require(isinstance(entry, dict) and set(entry) == {
            "parity", "word", "q1_endpoint", "q2_kernel", "tag_values"
        }, "projector_entry_keys")
        validate_character(entry["parity"], parity, "projector_entry_parity")
        require(tuple(entry["word"]) == PURE_Q1_WORDS[parity]
                and all(plain_int(x) and x in (-2, -1, 1, 2)
                        for x in entry["word"]), "projector_entry_word")
        endpoint = entry["q1_endpoint"]
        require(isinstance(endpoint, dict) and set(endpoint) == {
            "psl_identity", "parity"
        } and endpoint["psl_identity"] is True,
                "projector_entry_endpoint")
        validate_character(endpoint["parity"], parity,
                           "projector_entry_endpoint_parity")
        require(isinstance(entry["q2_kernel"], list)
                and len(entry["q2_kernel"]) == 3
                and all(plain_int(x) and 0 <= x < 3 for x in entry["q2_kernel"]),
                "projector_entry_kernel")
        tags = entry["tag_values"]
        require(isinstance(tags, list) and len(tags) == 6,
                "projector_entry_tags")
        for tag in tags:
            require(isinstance(tag, dict) and set(tag) == {"parity", "kernel"},
                    "projector_tag_keys")
            require(isinstance(tag["parity"], list) and len(tag["parity"]) == 2
                    and all(plain_int(x) and x in (0, 1) for x in tag["parity"]),
                    "projector_tag_parity")
            require(isinstance(tag["kernel"], list) and len(tag["kernel"]) == 3
                    and all(plain_int(x) and 0 <= x < 3 for x in tag["kernel"]),
                    "projector_tag_kernel")


def validate_downstream_flags(value: Any, reason: str) -> None:
    require(isinstance(value, dict) and set(value) == set(CLAIMS),
            reason + ":keys")
    for key in CLAIMS:
        require(value[key] is False, reason + ":" + key)


def validate_false_fields(value: dict[str, Any], reason: str,
                          *, independent: bool = False) -> None:
    for key in FALSE_FIELDS:
        if key == "independent_checker" and independent:
            continue
        require(value.get(key) is False, reason + ":" + key)


def validate_telemetry(value: dict[str, Any], reason: str) -> None:
    finite_float(value.get("elapsed_seconds"), reason + ":elapsed")
    peak = value.get("peak_rss_bytes")
    require(peak is None or (plain_int(peak) and peak >= 0),
            reason + ":peak")


def digest_string(value: Any, reason: str) -> None:
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
            reason)


def freely_reduce(word: Iterable[int]) -> tuple[int, ...]:
    reduced: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter in (-2, -1, 1, 2), "literal_word_letter")
        if reduced and reduced[-1] == -letter:
            reduced.pop()
        else:
            reduced.append(letter)
    return tuple(reduced)


def canonical_literal_terms(terms: Any) -> list[list[Any]]:
    require(isinstance(terms, list), "literal_terms_list")
    accumulator: dict[tuple[int, tuple[int, ...]], int] = {}
    for term in terms:
        require(isinstance(term, list) and len(term) == 3
                and plain_int(term[0]) and 1 <= term[0] <= 44
                and isinstance(term[1], list)
                and all(plain_int(x) for x in term[1])
                and plain_int(term[2]) and term[2] in (1, 2),
                "literal_term_shape")
        key = int(term[0]), freely_reduce(term[1])
        accumulator[key] = (accumulator.get(key, 0) + int(term[2])) % 3
    return [[seed, list(word), coefficient]
            for (seed, word), coefficient in sorted(accumulator.items())
            if coefficient]


def validate_expression_tree(expression: Any, rank: int, reason: str,
                             *, earlier_than: int | None = None) -> None:
    validate_expression(expression, rank, reason, earlier_than=earlier_than)


def validate_old_record(old: Any, index: int) -> None:
    rank = OLD_RANKS[index]
    require(isinstance(old, dict) and set(old) == {
        "character_index", "character", "rank", "record",
        "lower_basis_blob", "lifted_grade_blob", "defect_origin_range"
    }, "old_block_keys")
    require(plain_int(old["character_index"]) and old["character_index"] == index
            and isinstance(old["character"], list)
            and all(plain_int(x) for x in old["character"])
            and old["character"] == list(CHARACTERS[index])
            and plain_int(old["rank"]) and old["rank"] == rank,
            "old_block_metadata")
    record = old["record"]
    require(isinstance(record, dict) and set(record) == {
        "character", "rank", "attempts", "seed_reductions", "actor_order",
        "actor_transitions", "dag_nodes", "queue_exhausted"
    }, "old_record_keys")
    require(isinstance(record["character"], list)
            and all(plain_int(x) for x in record["character"])
            and record["character"] == list(CHARACTERS[index])
            and plain_int(record["rank"]) and record["rank"] == rank
            and plain_int(record["attempts"]) and record["attempts"] == 44 + 4 * rank
            and record["queue_exhausted"] is True, "old_record_metadata")
    validate_actor_order(record["actor_order"])
    seeds = record["seed_reductions"]
    transitions = record["actor_transitions"]
    nodes = record["dag_nodes"]
    require(isinstance(seeds, list) and len(seeds) == 44
            and isinstance(transitions, list) and len(transitions) == rank
            and isinstance(nodes, list) and len(nodes) == rank,
            "old_record_cardinality")
    for expression in seeds:
        validate_expression_tree(expression, rank, "old_seed_expression")
    for row in transitions:
        require(isinstance(row, list) and len(row) == 4, "old_actor_row")
        for expression in row:
            validate_expression_tree(expression, rank, "old_actor_expression")
    for pivot, node in enumerate(nodes):
        require(isinstance(node, dict) and set(node) == {
            "pivot", "lead", "scale", "origin", "reductions"
        }, "old_dag_keys")
        require(plain_int(node["pivot"]) and node["pivot"] == pivot
                and plain_int(node["lead"]) and 0 <= node["lead"] < LOWER_WIDTH
                and plain_int(node["scale"]) and node["scale"] in (1, 2),
                "old_dag_metadata")
        validate_expression_tree(node["reductions"], rank, "old_dag_reduction",
                                 earlier_than=pivot)
        origin = node["origin"]
        require(isinstance(origin, dict), "old_dag_origin_shape")
        if origin.get("kind") == "projected_seed":
            require(set(origin) == {"kind", "seed"}
                    and plain_int(origin["seed"]) and 1 <= origin["seed"] <= 44,
                    "old_seed_origin")
        elif origin.get("kind") == "actor":
            require(set(origin) == {"kind", "parent", "letter"}
                    and plain_int(origin["parent"]) and 0 <= origin["parent"] < pivot
                    and plain_int(origin["letter"]) and origin["letter"] in ACTORS,
                    "old_actor_origin")
        else:
            fail("old_dag_origin_kind")
    origin_range = old["defect_origin_range"]
    begin, end = ORIGIN_RANGES[index]
    require(isinstance(origin_range, list) and len(origin_range) == 2
            and all(plain_int(x) for x in origin_range)
            and origin_range == [begin, end], "old_origin_range")


def validate_prepare_body(body: Any, manifest: dict[str, Any]) -> None:
    required = {
        "schema", "phase", "fixture", "input_manifest", "input_manifest_sha256",
        "dimensions", "affine_convention", "substitution_matrices",
        "pure_q1_projectors", "canonical_solution", "old_blocks",
        "defect_origins", "defect_origin_sha256", "packets", "residual_blob",
        "residual_support", "residual_sha256", "paired_lower_presentation_complete",
        "elapsed_seconds", "peak_owner_bytes", "downstream_claim_flags",
    }
    require(isinstance(body, dict) and set(body) == required, "prepare_body_keys")
    require(body["schema"] == STATE_SCHEMA and body["phase"] == "prepare"
            and body["fixture"] is False and body["input_manifest"] == manifest
            and body["input_manifest_sha256"] == sha(canonical(manifest))
            and body["dimensions"] == fixed_dimensions()
            and body["affine_convention"] == "section-left-kernel-right"
            and body["paired_lower_presentation_complete"] is True,
            "prepare_body_metadata")
    validate_fixed_dimensions(body["dimensions"])
    validate_downstream_flags(body["downstream_claim_flags"], "prepare_body_flags")
    validate_telemetry(body, "prepare_body_telemetry")
    peak_owner = body["peak_owner_bytes"]
    require(isinstance(peak_owner, dict) and set(peak_owner) == {
        "old_lower_packed", "old_lift_dense", "packets_packed"
    } and all(plain_int(value) and value >= 0 for value in peak_owner.values()),
            "prepare_peak_owner")
    substitutions = body["substitution_matrices"]
    expected_substitutions = Context(load_words()).substitution_matrices
    require(isinstance(substitutions, list) and len(substitutions) == 6,
            "prepare_substitution_shape")
    require(all(isinstance(row, list) and len(row) == 2
                and all(plain_int(x) and x in (0, 1) for x in row)
                for matrix in substitutions for row in matrix),
            "prepare_substitution_types")
    require(substitutions == expected_substitutions,
            "prepare_substitution_matrices")
    pure = body["pure_q1_projectors"]
    validate_projector_entries(pure)
    context = Context(load_words())
    _, full = projector_identity(context)
    require(pure == full["pure_q1_projectors"], "prepare_projectors")

    canonical_solution = body["canonical_solution"]
    require(isinstance(canonical_solution, dict) and set(canonical_solution) == {
        "raw_terms", "raw_sha256", "canonical_terms", "canonical_sha256",
        "terms", "q1_raw_equals_canonical", "q1_target_replay",
        "pb3_augmentation", "normalized_exponent"
    }, "prepare_solution_keys")
    require(plain_int(canonical_solution["raw_terms"])
            and canonical_solution["raw_terms"] == 3936
            and plain_int(canonical_solution["canonical_terms"])
            and canonical_solution["canonical_terms"] == 2622
            and canonical_solution["raw_sha256"] == "3b902c612b2297c1144743620ac578f62d2c19e1f61cb76dfcdd18028dc2dd9e"
            and canonical_solution["q1_raw_equals_canonical"] is True
            and canonical_solution["q1_target_replay"] is True,
            "prepare_solution_metadata")
    terms = canonical_solution["terms"]
    require(isinstance(terms, list) and len(terms) == 2622,
            "prepare_solution_terms")
    for term in terms:
        require(isinstance(term, list) and len(term) == 3
                and plain_int(term[0]) and 1 <= term[0] <= 44
                and isinstance(term[1], list)
                and all(plain_int(letter) and letter in (-2, -1, 1, 2)
                        for letter in term[1])
                and plain_int(term[2]) and term[2] in (1, 2),
                "prepare_solution_term")
    require(canonical_literal_terms(terms) == terms,
            "prepare_solution_not_canonical")
    # The producer uses compact JSON without a newline for this term digest.
    require(sha(json.dumps(terms, separators=(",", ":")).encode("ascii"))
            == canonical_solution["canonical_sha256"], "prepare_solution_digest")
    for key in ("pb3_augmentation", "normalized_exponent"):
        require(isinstance(canonical_solution[key], list)
                and len(canonical_solution[key]) == 2
                and all(plain_int(x) and 0 <= x < 3 for x in canonical_solution[key]),
                "prepare_solution_" + key)

    old_blocks = body["old_blocks"]
    require(isinstance(old_blocks, list) and len(old_blocks) == 4,
            "prepare_old_blocks")
    for index, old in enumerate(old_blocks):
        validate_old_record(old, index)
    origins = body["defect_origins"]
    require(isinstance(origins, list) and len(origins) == 8232,
            "prepare_origins")
    require(body["defect_origin_sha256"] == sha(canonical(origins)),
            "prepare_origin_digest")
    expected_id = 0
    for character, (begin, end) in enumerate(ORIGIN_RANGES):
        for seed in range(1, 45):
            origin = origins[expected_id]
            require(isinstance(origin, dict) and set(origin) == {
                "id", "kind", "lower_character", "seed"
            } and plain_int(origin["id"]) and origin["id"] == expected_id
                and origin["kind"] == "seed"
                and plain_int(origin["lower_character"])
                and origin["lower_character"] == character
                and plain_int(origin["seed"]) and origin["seed"] == seed,
                    "prepare_seed_origin")
            expected_id += 1
        for pivot in range(OLD_RANKS[character]):
            for letter in ACTORS:
                origin = origins[expected_id]
                require(isinstance(origin, dict) and set(origin) == {
                    "id", "kind", "lower_character", "pivot", "letter"
                } and plain_int(origin["id"]) and origin["id"] == expected_id
                    and origin["kind"] == "transition"
                    and plain_int(origin["lower_character"])
                    and origin["lower_character"] == character
                    and plain_int(origin["pivot"]) and origin["pivot"] == pivot
                    and plain_int(origin["letter"]) and origin["letter"] == letter,
                        "prepare_transition_origin")
                expected_id += 1
        require(expected_id == end, "prepare_origin_range_count")
    require(expected_id == len(origins), "prepare_origin_count")
    packets = body["packets"]
    require(isinstance(packets, list) and len(packets) == 4, "prepare_packets")
    for index, packet in enumerate(packets):
        require(isinstance(packet, dict) and set(packet) == {
            "character", "blob", "origin_count", "zero_rows", "origin_sha256"
        } and isinstance(packet["character"], list)
            and all(plain_int(x) for x in packet["character"])
            and packet["character"] == list(CHARACTERS[index])
            and plain_int(packet["origin_count"]) and packet["origin_count"] == 8232
            and plain_int(packet["zero_rows"]) and 0 <= packet["zero_rows"] <= 8232
            and packet["origin_sha256"] == body["defect_origin_sha256"],
                "prepare_packet_metadata")
    require(plain_int(body["residual_support"]) and 0 <= body["residual_support"] <= PHYSICAL_GRADE,
            "prepare_residual_support")
    digest_string(body["residual_sha256"], "prepare_residual_sparse_digest")


BLOCK_BODY_KEYS = {
        "schema", "phase", "fixture", "parent_sha256", "character_index",
        "character", "dimensions", "packet_sha256", "origin_count", "rank",
        "attempts", "queue_exhausted", "pivot_leads", "basis_blob",
        "origin_reductions", "dag_nodes", "dag_sha256", "actor_order", "actor_transitions",
        "elapsed_seconds", "peak_owner_bytes", "downstream_claim_flags",
}


def validate_block_body_keys(body: Any) -> None:
    require(isinstance(body, dict) and set(body) == BLOCK_BODY_KEYS, "block_body_keys")


def validate_block_body(body: Any, prepare: dict[str, Any], index: int) -> None:
    rank = NEW_RANKS[index]
    validate_block_body_keys(body)
    require(body["schema"] == STATE_SCHEMA and body["phase"] == "block"
            and body["fixture"] is False
            and body["parent_sha256"] == PREPARE_DIGEST
            and plain_int(body["character_index"])
            and body["character_index"] == index
            and body["character"] == list(CHARACTERS[index])
            and body["dimensions"] == {"width": SOURCE_BLOCK, "monomials_coupled": 3}
            and body["packet_sha256"] == prepare["packets"][index]["blob"]["sha256"]
            and plain_int(body["origin_count"]) and body["origin_count"] == 8232
            and plain_int(body["rank"]) and body["rank"] == rank
            and plain_int(body["attempts"]) and body["attempts"] == 8232 + 4 * rank
            and body["queue_exhausted"] is True,
            "block_body_metadata")
    dimensions = body["dimensions"]
    require(isinstance(dimensions, dict) and set(dimensions) == {
        "width", "monomials_coupled"
    } and plain_int(dimensions["width"]) and dimensions["width"] == SOURCE_BLOCK
        and plain_int(dimensions["monomials_coupled"])
        and dimensions["monomials_coupled"] == 3, "block_dimensions")
    validate_character(body["character"], CHARACTERS[index], "block_character")
    validate_actor_order(body["actor_order"])
    validate_downstream_flags(body["downstream_claim_flags"], "block_body_flags")
    validate_telemetry(body, "block_body_telemetry")
    require(plain_int(body["peak_owner_bytes"]) and body["peak_owner_bytes"] >= 0,
            "block_peak_owner")
    leads = body["pivot_leads"]
    origins = body["origin_reductions"]
    transitions = body["actor_transitions"]
    nodes = body["dag_nodes"]
    require(isinstance(leads, list) and len(leads) == rank
            and all(plain_int(lead) and 0 <= lead < SOURCE_BLOCK for lead in leads)
            and len(set(leads)) == rank
            and isinstance(origins, list) and len(origins) == 8232
            and isinstance(transitions, list) and len(transitions) == rank
            and isinstance(nodes, list) and len(nodes) == rank,
            "block_body_cardinality")
    for expression in origins:
        validate_expression_tree(expression, rank, "block_origin_expression")
    for row in transitions:
        require(isinstance(row, list) and len(row) == 4, "block_actor_row")
        for expression in row:
            validate_expression_tree(expression, rank, "block_actor_expression")
    for pivot, node in enumerate(nodes):
        require(isinstance(node, dict) and set(node) == {
            "pivot", "lead", "scale", "origin", "reductions"
        }, "block_dag_keys")
        require(plain_int(node["pivot"]) and node["pivot"] == pivot
                and node["lead"] == leads[pivot]
                and plain_int(node["scale"]) and node["scale"] in (1, 2),
                "block_dag_metadata")
        validate_prior_expression(node["reductions"], pivot)
        origin = node["origin"]
        require(isinstance(origin, dict), "block_dag_origin_shape")
        kind = origin.get("kind")
        if kind == "defect":
            require(set(origin) == {"kind", "origin"}
                    and plain_int(origin["origin"])
                    and 0 <= origin["origin"] < 8232,
                    "block_defect_origin")
        elif kind == "actor":
            require(set(origin) == {"kind", "parent", "letter"}
                    and plain_int(origin["parent"]) and 0 <= origin["parent"] < pivot
                    and plain_int(origin["letter"]) and origin["letter"] in ACTORS,
                    "block_actor_origin")
        else:
            fail("block_origin_kind")
    digest_string(body["dag_sha256"], "block_dag_digest_shape")
    require(body["dag_sha256"] == sha(canonical(nodes)), "block_dag_digest")


def authenticate_prepare(root: Path) -> tuple[Path, dict[str, Any], bytes, dict[str, Any]]:
    safe, names = safe_root(root)
    body, body_raw = read_sealed(safe, "prepare", PREPARE_DIGEST, None)
    manifest = pinned_input_manifest()
    validate_prepare_body(body, manifest)
    expected_files = {"prepare.HEAD", f"prepare.{PREPARE_DIGEST}.json"}
    # Authenticate every referenced blob exactly once.  This pass also binds
    # all packet bytes before any range seek begins.
    residual_data = read_blob_data(safe, body["residual_blob"], 1, PHYSICAL_GRADE)
    residual_dense = unpack_trits(np.frombuffer(residual_data, dtype=np.uint8),
                                  PHYSICAL_GRADE)
    require(int(np.count_nonzero(residual_dense)) == body["residual_support"],
            "residual_support")
    require(sparse_digest(residual_dense) == body["residual_sha256"],
            "residual_sparse_digest")
    expected_files.add(body["residual_blob"]["file"])
    for old in body["old_blocks"]:
        for key, rows, width in (("lower_basis_blob", old["rank"], LOWER_WIDTH),
                                 ("lifted_grade_blob", old["rank"], SOURCE_TOTAL)):
            validate_blob_receipt(safe, old[key], rows, width)
            expected_files.add(old[key]["file"])
    packet_paths = []
    packet_identities = []
    for packet in body["packets"]:
        path, _ = validate_blob_receipt(safe, packet["blob"], 8232, SOURCE_BLOCK,
                                        read=False)
        require(path.name == packet["blob"]["file"], "packet_path_name")
        packet_identities.append(authenticate_stream(
            path, packet["blob"], expected_rows=8232,
            expected_width=SOURCE_BLOCK))
        packet_paths.append(path)
        expected_files.add(packet["blob"]["file"])
    exact_roster(names, expected_files)
    return safe, body, body_raw, {"manifest": manifest,
                                  "packet_paths": packet_paths,
                                  "packet_identities": packet_identities}


def authenticate_block(root: Path, index: int, prepare: dict[str, Any]) -> tuple[Path, dict[str, Any], bytes]:
    safe, names = safe_root(root)
    digest = PARENTS[index]
    body, body_raw = read_sealed(safe, f"block-{index}", digest, PREPARE_DIGEST)
    validate_block_body(body, prepare, index)
    basis = body["basis_blob"]
    require(basis["sha256"] == BASIS[index], "block_basis_pin")
    validate_blob_receipt(safe, basis, NEW_RANKS[index], SOURCE_BLOCK)
    exact_roster(names, {f"block-{index}.HEAD", f"block-{index}.{digest}.json", basis["file"]})
    return safe, body, body_raw


def packet_range_binding(begin: int, end: int, cursor: int,
                         expected_span: int) -> None:
    require(plain_int(begin) and plain_int(end) and plain_int(cursor)
            and plain_int(expected_span), "packet_range_types")
    require(end - begin == expected_span and begin == cursor,
            "packet_range_binding")


# ---------------------------------------------------------------------------
# Old closure, lift/DAG evaluation, packet component replay, and block FIFO

def close_lower_block(context: Context, label: tuple[int, int],
                      seed_rows: list[np.ndarray], *, started: float,
                      phase: str) -> tuple[PackedEchelon, dict[str, Any]]:
    owner = PackedEchelon(LOWER_WIDTH)
    nodes: list[dict[str, Any]] = []
    seed_reductions: list[list[list[int]]] = []
    transitions: list[list[list[list[int]] | None]] = []
    queue: deque[int] = deque()
    for seed, row in enumerate(seed_rows, 1):
        inserted = owner.insert(row)
        seed_reductions.append(expression_from_insert(inserted))
        if inserted["accepted"]:
            pivot = int(inserted["pivot"])
            node = {"pivot": pivot, "lead": int(inserted["lead"]),
                    "scale": int(inserted["scale"]),
                    "origin": {"kind": "projected_seed", "seed": seed},
                    "reductions": [list(pair) for pair in inserted["reductions"]]}
            nodes.append(node)
            transitions.append([None, None, None, None])
            queue.append(pivot)
    while queue:
        pivot = queue.popleft()
        parent = owner.dense_row(pivot)
        row_transitions: list[list[list[int]] | None] = [None] * 4
        for actor_index, letter in enumerate(ACTORS):
            child = associated_lower_actor(context, parent, label, letter)
            inserted = owner.insert(child)
            expression = expression_from_insert(inserted)
            row_transitions[actor_index] = expression
            if inserted["accepted"]:
                new_pivot = int(inserted["pivot"])
                nodes.append({
                    "pivot": new_pivot, "lead": int(inserted["lead"]),
                    "scale": int(inserted["scale"]),
                    "origin": {"kind": "actor", "parent": pivot, "letter": letter},
                    "reductions": [list(pair) for pair in inserted["reductions"]],
                })
                transitions.append([None, None, None, None])
                queue.append(new_pivot)
            if len(owner.rows) % 256 == 0:
                progress(phase, len(owner.rows), len(seed_rows) + 4 * len(owner.rows))
                guard(started, phase)
        transitions[pivot] = row_transitions
        guard(started, phase)
    require(all(isinstance(row, list) and len(row) == 4 and
                 all(value is not None for value in row) for row in transitions),
            "old_transition_incomplete")
    require(len(nodes) == len(owner.rows), "old_dag_rank")
    require(len(seed_reductions) == len(seed_rows), "old_seed_count")
    return owner, {
        "character": list(label), "rank": len(owner.rows),
        "attempts": len(seed_rows) + 4 * len(owner.rows),
        "seed_reductions": seed_reductions, "actor_order": list(ACTORS),
        "actor_transitions": transitions, "dag_nodes": nodes,
        "queue_exhausted": True,
    }


def evaluate_old_lifts(context: Context, label: tuple[int, int],
                       owner: PackedEchelon, record: dict[str, Any],
                       projected_grades: list[np.ndarray], *, started: float,
                       phase: str) -> np.ndarray:
    matrix = np.zeros((len(owner.rows), SOURCE_TOTAL), dtype=np.uint8)
    for pivot, node in enumerate(record["dag_nodes"]):
        require(plain_int(node["pivot"]) and node["pivot"] == pivot,
                "old_dag_order")
        origin = node["origin"]
        if origin["kind"] == "projected_seed":
            seed_index = int(origin["seed"]) - 1
            require(0 <= seed_index < len(projected_grades), "old_seed_index")
            work = projected_grades[seed_index].copy()
        else:
            parent = int(origin["parent"])
            require(parent < pivot, "old_dag_cycle")
            work = exact_actor_on_old_lift(context, owner.dense_row(parent),
                                           matrix[parent], label,
                                           int(origin["letter"]))
        for earlier, coefficient in node["reductions"]:
            require(int(earlier) < pivot, "old_dag_reduction_order")
            _add_mod3(work, matrix[int(earlier)], -int(coefficient))
        if int(node["scale"]) == 2:
            work[:] = (2 * work.astype(np.uint16)) % 3
        matrix[pivot] = work
        if (pivot + 1) % 256 == 0:
            progress(phase, pivot + 1, len(owner.rows))
            guard(started, phase)
    return matrix


def replay_block_kernel(context: Context, label: tuple[int, int],
                        packet_rows: Iterable[bytes | np.ndarray],
                        *, expected_origin_reductions: list[Any] | None = None,
                        expected_nodes: list[Any] | None = None,
                        expected_transitions: list[Any] | None = None,
                        expected_basis: bytes | None = None,
                        expected_rank: int | None = None,
                        started: float | None = None,
                        phase: str = "block") -> dict[str, Any]:
    """Replay packet insertion and the FIFO actor closure.

    The iterable is consumed exactly once.  In production it is a packet
    stream; in the bounded fixture it is a two-row in-memory stream.
    """
    started = time.monotonic() if started is None else started
    owner = PackedEchelon(SOURCE_BLOCK)
    origins: list[list[list[int]]] = []
    nodes: list[dict[str, Any]] = []
    transitions: list[list[list[list[int]] | None]] = []
    queue: deque[int] = deque()
    packet_count = 0
    expected_origin_count = (None if expected_origin_reductions is None
                             else len(expected_origin_reductions))
    for packet_count, packed in enumerate(packet_rows, 1):
        if isinstance(packed, (bytes, bytearray)):
            raw = bytes(packed)
            require(len(raw) == PACKED_WIDTH, "packet_row_size")
            row = np.frombuffer(raw, dtype=np.uint8).copy()
        else:
            row = np.asarray(packed, dtype=np.uint8).reshape(-1).copy()
            require(row.size == PACKED_WIDTH, "packet_row_size")
        require(not np.any(row > 80), "packet_row_byte")
        inserted = owner.insert(row)
        expression = expression_from_insert(inserted)
        origins.append(expression)
        if expected_origin_reductions is not None:
            origin_index = packet_count - 1
            require(origin_index < expected_origin_count, "packet_expression_count")
            compare_bytes(canonical(expression), canonical(expected_origin_reductions[origin_index]),
                          "packet_expression")
        if inserted["accepted"]:
            pivot = int(inserted["pivot"])
            node = {"pivot": pivot, "lead": int(inserted["lead"]),
                    "scale": int(inserted["scale"]),
                    "origin": {"kind": "defect", "origin": packet_count - 1},
                    "reductions": [list(pair) for pair in inserted["reductions"]]}
            nodes.append(node)
            if expected_nodes is not None:
                compare_bytes(canonical(node), canonical(expected_nodes[pivot]),
                              "packet_dag_node")
            transitions.append([None, None, None, None])
            queue.append(pivot)
        if packet_count % 256 == 0:
            progress(phase + "-packet", packet_count, packet_count)
            guard(started, phase)
    while queue:
        pivot = queue.popleft()
        parent = owner.dense_row(pivot)
        row_transitions: list[list[list[int]] | None] = [None] * 4
        for actor_index, letter in enumerate(ACTORS):
            child = associated_grade_actor(context, parent, label, letter)
            inserted = owner.insert(child)
            expression = expression_from_insert(inserted)
            row_transitions[actor_index] = expression
            if expected_transitions is not None:
                compare_bytes(canonical(expression), canonical(expected_transitions[pivot][actor_index]),
                              "actor_transition")
            if inserted["accepted"]:
                child_pivot = int(inserted["pivot"])
                node = {"pivot": child_pivot, "lead": int(inserted["lead"]),
                        "scale": int(inserted["scale"]),
                        "origin": {"kind": "actor", "parent": pivot, "letter": letter},
                        "reductions": [list(pair) for pair in inserted["reductions"]]}
                nodes.append(node)
                if expected_nodes is not None:
                    compare_bytes(canonical(node), canonical(expected_nodes[child_pivot]),
                                  "actor_dag_node")
                transitions.append([None, None, None, None])
                queue.append(child_pivot)
            guard(started, phase)
        transitions[pivot] = row_transitions
    require(all(isinstance(row, list) and len(row) == 4 and
                 all(value is not None for value in row) for row in transitions),
            "block_transition_incomplete")
    require(len(nodes) == len(owner.rows), "block_dag_rank")
    if expected_origin_reductions is not None:
        require(packet_count == expected_origin_count, "packet_expression_count")
    if expected_nodes is not None:
        require(nodes == expected_nodes, "block_node_replay")
    if expected_transitions is not None:
        require(transitions == expected_transitions, "block_transition_replay")
    if expected_rank is not None:
        require(len(owner.rows) == expected_rank, "block_rank")
    basis = owner.matrix_bytes()
    if expected_basis is not None:
        compare_bytes(basis, expected_basis, "block_basis_bytes")
    return {"owner": owner, "origins": origins, "nodes": nodes,
            "transitions": transitions, "basis": basis,
            "packet_count": packet_count,
            "attempts": packet_count + 4 * len(owner.rows)}


def validate_producer_source(path: Path, expected: str) -> str:
    require(path.is_file(), "producer_v5_source_missing")
    digest = sha(path.read_bytes())
    require(digest == expected, "producer_v5_source_digest")
    return digest


def producer_source_digest() -> str:
    # Reading a source file for a provenance digest is explicitly allowed by
    # the task; no module loader or executable producer helper is used.
    return validate_producer_source(PRODUCER_V5_SOURCE, PRODUCER_V5_SHA)


def read_blob_data(root: Path, receipt: dict[str, Any], rows: int,
                   width: int) -> bytes:
    _, data = validate_blob_receipt(root, receipt, rows, width, read=True)
    require(data is not None, "blob_data_missing")
    return data


def replay_prepare(root: Path, prepared: tuple[Path, dict[str, Any], bytes, dict[str, Any]] | None = None) -> dict[str, Any]:
    started = time.monotonic()
    safe, body, body_raw, auth = authenticate_prepare(root) if prepared is None else prepared
    words = load_words()
    context = Context(words)
    projector, projector_full = projector_identity(context)
    relators = [tuple(int(x) for x in word) for word in words["relators"]]
    base = [evaluate_occurrence_pair(word, context) for word in relators]
    require(len(base) == 44, "seed_count")

    streams = [path.open("rb") for path in auth["packet_paths"]]
    packet_hashers = [hashlib.sha256() for _ in range(4)]
    zero_counts = [0, 0, 0, 0]
    cursor = 0
    seed_count = 0
    actor_count = 0
    packet_halves = 0
    old_rank_total = 0
    dag_total = 0
    equality: list[dict[str, Any]] = []
    try:
        for character_index, label in enumerate(CHARACTERS):
            rank = OLD_RANKS[character_index]
            projected = [projected_seed_pair(context, pair, label) for pair in base]
            seed_rows: list[np.ndarray] = []
            projected_grades: list[np.ndarray] = []
            for lower, grade, auxiliary in projected:
                row = np.zeros(LOWER_WIDTH, dtype=np.uint8)
                selected = character_index
                row[:SOURCE_BASE] = lower[selected]
                row[SOURCE_BASE:] = auxiliary
                require(np.array_equal(row[SOURCE_BASE:], auxiliary), "shared_auxiliary")
                seed_rows.append(row)
                projected_grades.append(grade.reshape(SOURCE_TOTAL).copy())
            owner, record = close_lower_block(context, label, seed_rows,
                                              started=started, phase="old-closure")
            expected_old = body["old_blocks"][character_index]
            compare_bytes(canonical(record), canonical(expected_old["record"]),
                          "old_record_replay")
            lower_data = read_blob_data(safe, expected_old["lower_basis_blob"],
                                        rank, LOWER_WIDTH)
            compare_bytes(owner.matrix_bytes(), lower_data, "old_lower_bytes")
            lifts = evaluate_old_lifts(context, label, owner, record,
                                       projected_grades, started=started,
                                       phase="old-lifts")
            lifted_data = read_blob_data(safe, expected_old["lifted_grade_blob"],
                                         rank, SOURCE_TOTAL)
            compare_bytes(packed_matrix_bytes(lifts), lifted_data,
                          "old_lift_bytes")
            equality.append({
                "character_index": character_index,
                "record_sha256": sha(canonical(record)),
                "lower_sha256": sha(owner.matrix_bytes()),
                "lifted_sha256": sha(packed_matrix_bytes(lifts)),
            })

            begin, end = ORIGIN_RANGES[character_index]
            packet_range_binding(begin, end, cursor, 44 + 4 * rank)
            cursor = end
            row_bytes = SOURCE_BLOCK // 4
            for stream in streams:
                packet_seek(stream, begin, end, row_bytes,
                            expected_begin=begin)
            for seed_index in range(44):
                work = projected[seed_index][1].reshape(SOURCE_TOTAL).copy()
                for pivot, coefficient in record["seed_reductions"][seed_index]:
                    _add_mod3(work, lifts[int(pivot)], -int(coefficient))
                split = work.reshape(4, SOURCE_BLOCK)
                for packet_index, stream in enumerate(streams):
                    expected = pack_trits(split[packet_index]).tobytes()
                    got = read_exact(stream, row_bytes, "seed_packet")
                    compare_bytes(expected, got, "seed_packet_bytes")
                    packet_hashers[packet_index].update(got)
                    if not any(got):
                        zero_counts[packet_index] += 1
                    packet_halves += 1
                seed_count += 1
                progress("old-seed-packet", seed_count, 176)
            for pivot in range(rank):
                lower = owner.dense_row(pivot)
                for actor_index, letter in enumerate(ACTORS):
                    work = exact_actor_on_old_lift(context, lower, lifts[pivot],
                                                   label, letter)
                    for earlier, coefficient in record["actor_transitions"][pivot][actor_index]:
                        _add_mod3(work, lifts[int(earlier)], -int(coefficient))
                    split = work.reshape(4, SOURCE_BLOCK)
                    for packet_index, stream in enumerate(streams):
                        expected = pack_trits(split[packet_index]).tobytes()
                        got = read_exact(stream, row_bytes, "actor_packet")
                        compare_bytes(expected, got, "actor_packet_bytes")
                        packet_hashers[packet_index].update(got)
                        if not any(got):
                            zero_counts[packet_index] += 1
                        packet_halves += 1
                    actor_count += 1
                    progress("old-actor-packet", actor_count, 8056)
                    guard(started, "prepare-packets")
            for stream in streams:
                packet_finish(stream, end, row_bytes, eof=(character_index == 3))
            old_rank_total += rank
            dag_total += len(record["dag_nodes"])
            progress("prepare-character", character_index + 1, 4, force=True)
    finally:
        for stream in streams:
            stream.close()
    # The authenticated packet identity must remain stable for the entire
    # character-wise replay, not merely during the initial hash pass.
    for path, identity in zip(auth["packet_paths"], auth["packet_identities"]):
        require(stable_identity(require_regular(path)) == identity,
                "packet_changed_during_replay")
    require(cursor == 8232 and (old_rank_total, dag_total) == (2014, 2014),
            "prepare_old_totals")
    require((seed_count, actor_count, packet_halves) == (176, 8056, 32928),
            "prepare_exact_counts")
    for packet_index in range(4):
        require(packet_hashers[packet_index].hexdigest() ==
                body["packets"][packet_index]["blob"]["sha256"],
                "packet_replay_digest")
        require(zero_counts[packet_index] == body["packets"][packet_index]["zero_rows"],
                "packet_zero_rows")
    checker_digests = {
        "prepare_body_sha256": sha(body_raw),
        "equality_receipts_sha256": sha(canonical(equality)),
        "packet_component_sha256": sha(canonical([h.hexdigest() for h in packet_hashers])),
        "projector_full_sha256": sha(canonical(projector_full)),
    }
    return {
        "schema": "d972.r07.p1.componentwise.prepare.v1",
        "phase": "prepare",
        "producer_sha256": producer_source_digest(),
        "source_run": SOURCE_RUN, "source_attempt": SOURCE_ATTEMPT,
        "source_head": SOURCE_HEAD, "prepare_body_sha256": PREPARE_DIGEST,
        "input_manifest_sha256": sha(canonical(auth["manifest"])),
        "counts": {"old_ranks": 2014, "old_dag_nodes": 2014,
                   "old_seed_lower": seed_count, "old_actor_lower": actor_count,
                   "direct_packet_halves": packet_halves},
        "equality_receipts": equality,
        "equality_receipts_sha256": sha(canonical(equality)),
        "projector_identity": projector,
        "checker_digests": checker_digests,
        "downstream_claim_flags": dict(CLAIMS),
        "resident_global_matrix": False, "independent_checker": True,
        "precision2": False, "A0": False, "COMMON": False,
        "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
        "verified": False,
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_bytes": rss_bytes(),
    }


def rss_bytes() -> int | None:
    if resource is None:
        return None
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


def replay_block(prepared: tuple[Path, dict[str, Any], bytes, dict[str, Any]],
                 root: Path, index: int, *, started: float | None = None) -> dict[str, Any]:
    started = time.monotonic() if started is None else started
    prep_safe, prepare, _, auth = prepared
    safe, body, body_raw = authenticate_block(root, index, prepare)
    context = Context(load_words())
    packet_path = auth["packet_paths"][index]
    packet_identity = auth["packet_identities"][index]
    row_bytes = SOURCE_BLOCK // 4

    def packet_rows() -> Iterable[bytes]:
        with packet_path.open("rb") as stream:
            for origin in range(8232):
                yield read_exact(stream, row_bytes, "block_packet")
            require(stream.read(1) == b"", "block_packet_trailing")

    basis_data = read_blob_data(safe, body["basis_blob"], NEW_RANKS[index], SOURCE_BLOCK)
    result = replay_block_kernel(
        context, CHARACTERS[index], packet_rows(),
        expected_origin_reductions=body["origin_reductions"],
        expected_nodes=body["dag_nodes"],
        expected_transitions=body["actor_transitions"],
        expected_basis=basis_data, expected_rank=NEW_RANKS[index],
        started=started, phase=f"block-{index}")
    require(result["packet_count"] == 8232
            and result["attempts"] == 8232 + 4 * NEW_RANKS[index],
            "block_attempts")
    require(stable_identity(require_regular(packet_path)) == packet_identity,
            "packet_changed_during_block_replay")
    guard(started, f"block-{index}")
    return {
        "schema": "d972.r07.p1.componentwise.block.v1",
        "phase": "block", "producer_sha256": producer_source_digest(),
        "source_run": SOURCE_RUN, "source_attempt": SOURCE_ATTEMPT,
        "source_head": SOURCE_HEAD, "prepare_body_sha256": PREPARE_DIGEST,
        "block_index": index, "block_body_sha256": PARENTS[index],
        "basis_sha256": BASIS[index],
        "counts": {"packet_basis_halves": 8232,
                   "new_actor_identities": 4 * NEW_RANKS[index],
                   "new_dag_identities": NEW_RANKS[index],
                   "compound_obligations": 8232 + 4 * NEW_RANKS[index]},
        "rank": NEW_RANKS[index],
        "attempts": 8232 + 4 * NEW_RANKS[index],
        "dag_sha256": sha(canonical(result["nodes"])),
        "checker_digests": {
            "block_body_sha256": sha(body_raw),
            "basis_sha256": sha(result["basis"]),
            "origin_reductions_sha256": sha(canonical(result["origins"])),
            "actor_transitions_sha256": sha(canonical(result["transitions"])),
            "dag_sha256": sha(canonical(result["nodes"])),
        },
        "downstream_claim_flags": dict(CLAIMS),
        "resident_global_matrix": False, "independent_checker": True,
        "precision2": False, "A0": False, "COMMON": False,
        "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
        "verified": False,
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_bytes": rss_bytes(),
    }


# ---------------------------------------------------------------------------
# Peer receipt validation and exact five-artifact join

PREPARE_RECEIPT_KEYS = {
    "schema", "phase", "producer_sha256", "source_run", "source_attempt",
    "source_head", "prepare_body_sha256", "input_manifest_sha256", "counts",
    "equality_receipts", "equality_receipts_sha256", "projector_identity",
    "downstream_claim_flags", "resident_global_matrix", "independent_checker",
    "precision2", "A0", "COMMON", "COMPATIBLE_LIFT", "FAKE", "IHARA",
    "verified", "elapsed_seconds", "peak_rss_bytes",
}
BLOCK_RECEIPT_KEYS = {
    "schema", "phase", "producer_sha256", "source_run", "source_attempt",
    "source_head", "prepare_body_sha256", "block_index", "block_body_sha256",
    "basis_sha256", "counts", "rank", "attempts", "dag_sha256",
    "downstream_claim_flags", "resident_global_matrix", "independent_checker",
    "precision2", "A0", "COMMON", "COMPATIBLE_LIFT", "FAKE", "IHARA",
    "verified", "elapsed_seconds", "peak_rss_bytes",
}
JOIN_RECEIPT_KEYS = {
    "schema", "terminal", "global_relations", "old_ranks", "new_ranks",
    "dag_nodes", "old_local_relations", "direct_packet_halves",
    "packet_basis_halves", "new_actor_identities", "compound_obligations",
    "resident_global_matrix", "independent_checker", "precision2", "A0",
    "COMMON", "COMPATIBLE_LIFT", "FAKE", "IHARA", "verified",
    "producer_sha256",
}


def validate_equality_receipts(value: Any) -> None:
    require(isinstance(value, list) and len(value) == 4, "equality_records")
    for index, record in enumerate(value):
        require(isinstance(record, dict) and set(record) == {
            "character_index", "record_sha256", "lower_sha256", "lifted_sha256"
        }, "equality_record_keys")
        require(plain_int(record["character_index"])
                and record["character_index"] == index,
                "equality_record_index")
        for key in ("record_sha256", "lower_sha256", "lifted_sha256"):
            digest_string(record[key], "equality_" + key)


def validate_projector_receipt(value: Any) -> None:
    require(isinstance(value, dict) and set(value) == {
        "sum_chi_P_chi_mod3", "seed_reconstruction_count", "cv_sum_table",
        "cv_sum_table_sha256", "pure_words_sha256"
    }, "projector_receipt_keys")
    require(plain_int(value["sum_chi_P_chi_mod3"])
            and value["sum_chi_P_chi_mod3"] == 1,
            "projector_receipt_sum")
    require(plain_int(value["seed_reconstruction_count"])
            and value["seed_reconstruction_count"] == 44,
            "projector_receipt_seed_count")
    table = value["cv_sum_table"]
    require(isinstance(table, list) and len(table) == 4
            and all(plain_int(entry) for entry in table)
            and table == [1, 0, 0, 0],
            "projector_receipt_table")
    require(value["cv_sum_table_sha256"] == sha(canonical(table)),
            "projector_receipt_table_digest")
    digest_string(value["pure_words_sha256"], "projector_receipt_words_digest")


def validate_peer_common(value: dict[str, Any], phase: str,
                         producer: str) -> None:
    require(value.get("schema") ==
            f"d972.r07.p1.componentwise.{phase}.v1"
            and value.get("phase") == phase, "peer_receipt_phase")
    require(value.get("producer_sha256") == producer, "peer_producer_digest")
    require(value.get("source_run") == SOURCE_RUN
            and isinstance(value.get("source_run"), str), "peer_source_run")
    require(value.get("source_attempt") == SOURCE_ATTEMPT
            and isinstance(value.get("source_attempt"), str), "peer_source_attempt")
    require(value.get("source_head") == SOURCE_HEAD
            and isinstance(value.get("source_head"), str), "peer_source_head")
    require(value.get("prepare_body_sha256") == PREPARE_DIGEST,
            "peer_prepare_digest")
    validate_downstream_flags(value.get("downstream_claim_flags"),
                              "peer_downstream_claims")
    validate_false_fields(value, "peer_claims")
    validate_telemetry(value, "peer_telemetry")


def validate_peer_prepare(value: Any, producer: str,
                          expected_manifest: str) -> None:
    require(isinstance(value, dict) and set(value) == PREPARE_RECEIPT_KEYS,
            "peer_prepare_keys")
    validate_peer_common(value, "prepare", producer)
    require(value["input_manifest_sha256"] == expected_manifest,
            "peer_prepare_manifest")
    counts = value["counts"]
    expected = {"old_ranks": 2014, "old_dag_nodes": 2014,
                "old_seed_lower": 176, "old_actor_lower": 8056,
                "direct_packet_halves": 32928}
    require(isinstance(counts, dict) and set(counts) == set(expected),
            "peer_prepare_counts_keys")
    for key, want in expected.items():
        require(plain_int(counts[key]) and counts[key] == want,
                "peer_prepare_count:" + key)
    validate_equality_receipts(value["equality_receipts"])
    require(value["equality_receipts_sha256"] ==
            sha(canonical(value["equality_receipts"])),
            "peer_equality_digest")
    validate_projector_receipt(value["projector_identity"])


def validate_peer_block(value: Any, index: int, producer: str) -> None:
    require(isinstance(value, dict) and set(value) == BLOCK_RECEIPT_KEYS,
            "peer_block_keys")
    validate_peer_common(value, "block", producer)
    require(plain_int(value["block_index"]) and value["block_index"] == index,
            "peer_block_index")
    require(value["block_body_sha256"] == PARENTS[index]
            and value["basis_sha256"] == BASIS[index],
            "peer_block_ancestry")
    require(plain_int(value["rank"]) and value["rank"] == NEW_RANKS[index],
            "peer_block_rank")
    require(plain_int(value["attempts"])
            and value["attempts"] == 8232 + 4 * NEW_RANKS[index],
            "peer_block_attempts")
    digest_string(value["dag_sha256"], "peer_block_dag_digest")
    counts = value["counts"]
    expected = {"packet_basis_halves": 8232,
                "new_actor_identities": 4 * NEW_RANKS[index],
                "new_dag_identities": NEW_RANKS[index],
                "compound_obligations": 8232 + 4 * NEW_RANKS[index]}
    require(isinstance(counts, dict) and set(counts) == set(expected),
            "peer_block_counts_keys")
    for key, want in expected.items():
        require(plain_int(counts[key]) and counts[key] == want,
                "peer_block_count:" + key)


def read_peer_chain(phase_paths: list[Path], join_path: Path) -> tuple[
        dict[str, Any], list[dict[str, Any]], dict[str, Any], list[bytes]]:
    require(len(phase_paths) == 5, "peer_phase_receipt_count")
    parsed = [read_canonical(path) for path in phase_paths]
    join, join_raw = read_canonical(join_path)
    prepare = parsed[0][0]
    blocks = [item[0] for item in parsed[1:]]
    require(isinstance(prepare, dict) and all(isinstance(x, dict) for x in blocks)
            and isinstance(join, dict), "peer_chain_entries")
    return prepare, blocks, join, [item[1] for item in parsed] + [join_raw]


def validate_join_receipt(value: Any, producer: str,
                          prepare: dict[str, Any], blocks: list[dict[str, Any]]) -> None:
    require(isinstance(value, dict) and set(value) == JOIN_RECEIPT_KEYS,
            "peer_join_keys")
    expected = {
        "global_relations": 32280, "old_ranks": 2014, "new_ranks": 6045,
        "dag_nodes": 8059, "old_local_relations": 8232,
        "direct_packet_halves": 32928, "packet_basis_halves": 32928,
        "new_actor_identities": 24180, "compound_obligations": 65340,
    }
    require(value["schema"] == "d972.r07.p1.componentwise.v1"
            and value["terminal"] == "TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED"
            and value["producer_sha256"] == producer, "peer_join_identity")
    for key, wanted in expected.items():
        require(plain_int(value[key]) and value[key] == wanted, "peer_join_" + key)
    for key in ("resident_global_matrix", "independent_checker", "precision2",
                "A0", "COMMON", "COMPATIBLE_LIFT", "FAKE", "IHARA", "verified"):
        require(value[key] is False, "peer_join_claim:" + key)
    validate_obligation_totals(prepare, blocks)
    require(value["old_ranks"] == prepare["counts"]["old_ranks"]
            and value["new_ranks"] == sum(block["rank"] for block in blocks)
            and value["dag_nodes"] == prepare["counts"]["old_dag_nodes"]
               + sum(block["counts"]["new_dag_identities"] for block in blocks)
            and value["old_local_relations"] == prepare["counts"]["old_seed_lower"]
               + prepare["counts"]["old_actor_lower"]
            and value["direct_packet_halves"] == prepare["counts"]["direct_packet_halves"]
            and value["packet_basis_halves"] == sum(
                block["counts"]["packet_basis_halves"] for block in blocks)
            and value["new_actor_identities"] == sum(
                block["counts"]["new_actor_identities"] for block in blocks),
            "peer_join_phase_arithmetic")


def compare_semantic_receipts(ours_prepare: dict[str, Any],
                              ours_blocks: list[dict[str, Any]],
                              peer_prepare: dict[str, Any],
                              peer_blocks: list[dict[str, Any]]) -> None:
    # Compare every arithmetic family which has a canonical producer field;
    # checker-only digests stay separate and are never replaced by this join.
    for key in ("counts", "equality_receipts", "equality_receipts_sha256",
                "projector_identity", "prepare_body_sha256", "input_manifest_sha256"):
        require(ours_prepare[key] == peer_prepare[key], "prepare_peer_mismatch:" + key)
    for index, (ours, peer) in enumerate(zip(ours_blocks, peer_blocks)):
        for key in ("block_index", "block_body_sha256", "basis_sha256", "counts",
                    "rank", "attempts", "dag_sha256", "prepare_body_sha256"):
            require(ours[key] == peer[key], f"block_peer_mismatch:{index}:{key}")


def validate_obligation_totals(prepare: dict[str, Any],
                               blocks: list[dict[str, Any]]) -> None:
    require(prepare["counts"] == {
        "old_ranks": 2014, "old_dag_nodes": 2014, "old_seed_lower": 176,
        "old_actor_lower": 8056, "direct_packet_halves": 32928,
    }, "obligation_prepare_counts")
    require([block["block_index"] for block in blocks] == [0, 1, 2, 3],
            "obligation_block_order")
    require(sum(block["rank"] for block in blocks) == 6045,
            "obligation_new_rank")
    require(sum(block["counts"]["packet_basis_halves"] for block in blocks) == 32928,
            "obligation_packet_basis")
    require(sum(block["counts"]["new_actor_identities"] for block in blocks) == 24180,
            "obligation_new_actor")
    require(sum(block["counts"]["new_dag_identities"] for block in blocks) == 6045,
            "obligation_new_dag")
    require(sum(block["counts"]["compound_obligations"] for block in blocks) == 57108,
            "obligation_block_compound")
    require(8232 + 32928 + 24180 == 65340, "obligation_total")


def validate_producer_chain(peer_prepare: dict[str, Any],
                            peer_blocks: list[dict[str, Any]],
                            peer_join: dict[str, Any], producer: str,
                            expected_manifest: str) -> None:
    validate_peer_prepare(peer_prepare, producer, expected_manifest)
    require(len(peer_blocks) == 4, "peer_block_count")
    for index, value in enumerate(peer_blocks):
        validate_peer_block(value, index, producer)
    validate_join_receipt(peer_join, producer, peer_prepare, peer_blocks)


def run_actual_check(prepare_root: Path, block_roots: list[Path],
                     phase_paths: list[Path], join_path: Path,
                     output: Path) -> dict[str, Any]:
    require(len(block_roots) == 4, "five_artifact_roots")
    started = time.monotonic()
    producer = producer_source_digest()
    progress("prepare", 0, 1, force=True)
    prepared = authenticate_prepare(prepare_root)
    ours_prepare = replay_prepare(prepare_root, prepared)
    progress("prepare", 1, 1, force=True)
    ours_blocks = []
    for index, block_root in enumerate(block_roots):
        progress(f"block-{index}", 0, 1, force=True)
        ours_blocks.append(replay_block(prepared, block_root, index, started=started))
        progress(f"block-{index}", 1, 1, force=True)
    peer_prepare, peer_blocks, peer_join, peer_raws = read_peer_chain(
        phase_paths, join_path)
    expected_manifest = sha(canonical(prepared[3]["manifest"]))
    validate_producer_chain(peer_prepare, peer_blocks, peer_join, producer,
                            expected_manifest)
    require(peer_prepare["source_run"] == ours_prepare["source_run"]
            and peer_prepare["source_attempt"] == ours_prepare["source_attempt"]
            and peer_prepare["source_head"] == ours_prepare["source_head"],
            "peer_source_ancestry")
    require(all(value["prepare_body_sha256"] == PREPARE_DIGEST
                for value in peer_blocks), "peer_prepare_ancestry")
    compare_semantic_receipts(ours_prepare, ours_blocks, peer_prepare, peer_blocks)
    validate_obligation_totals(ours_prepare, ours_blocks)
    checker_digests = {
        "prepare": ours_prepare["checker_digests"],
        "blocks": [value["checker_digests"] for value in ours_blocks],
        "producer_receipts": {
            "prepare": sha(peer_raws[0]),
            "blocks": [sha(raw) for raw in peer_raws[1:5]],
            "join": sha(peer_raws[5]),
        },
        "semantic_family_sha256": sha(canonical({
            "prepare": ours_prepare["counts"],
            "equality": ours_prepare["equality_receipts"],
            "blocks": [value["counts"] for value in ours_blocks],
            "projector": ours_prepare["projector_identity"],
        })),
    }
    result = {
        "schema": CHECKER_SCHEMA,
        "terminal": "TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED_INDEPENDENTLY",
        "marker": MARKER,
        "source_run": SOURCE_RUN, "source_attempt": SOURCE_ATTEMPT,
        "source_head": SOURCE_HEAD, "prepare_body_sha256": PREPARE_DIGEST,
        "old_ranks": 2014, "new_ranks": 6045, "dag_nodes": 8059,
        "global_relations": 32280,
        "old_local_relations": 8232,
        "direct_packet_halves": 32928,
        "packet_basis_halves": 32928,
        "new_actor_identities": 24180,
        "compound_obligations": 65340,
        "prepare": ours_prepare,
        "blocks": ours_blocks,
        "producer_receipt_sha256": checker_digests["producer_receipts"],
        "producer_sha256": producer,
        "checker_digests": checker_digests,
        "resident_global_matrix": False,
        "independent_checker": True,
        "precision2": False, "A0": False, "COMMON": False,
        "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
        "verified": False,
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_bytes": rss_bytes(),
    }
    # All five artifact phases, all packet streams and peer receipt checks have
    # succeeded before this atomic write and success marker are reached.
    atomic_write(output, canonical(result))
    print(MARKER, flush=True)
    return result


def atomic_write(path: Path, data: bytes) -> None:
    require(data.endswith(b"\n") and canonical(json.loads(data.decode("utf-8"))) == data,
            "atomic_receipt_not_canonical")
    require(not path.exists(), "output_exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp",
                                     dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        require(path.read_bytes() == data, "atomic_receipt_eof")
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


# ---------------------------------------------------------------------------
# Bounded live fixtures.  These enter the same kernels used by the actual
# checker, but use tiny rows/streams and never construct a Task554-sized root.

def expect_reject(call: Any) -> int:
    try:
        call()
    except (RuntimeError, ValueError, OSError, AssertionError):
        return 1
    fail("fixture_accept")


def fixture_peer_receipts(producer: str, manifest_digest: str,
                          projector: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    equality = [{"character_index": index,
                 "record_sha256": f"{index + 1:064x}",
                 "lower_sha256": f"{index + 5:064x}",
                 "lifted_sha256": f"{index + 9:064x}"}
                for index in range(4)]
    prepare = {
        "schema": "d972.r07.p1.componentwise.prepare.v1", "phase": "prepare",
        "producer_sha256": producer, "source_run": SOURCE_RUN,
        "source_attempt": SOURCE_ATTEMPT, "source_head": SOURCE_HEAD,
        "prepare_body_sha256": PREPARE_DIGEST,
        "input_manifest_sha256": manifest_digest,
        "counts": {"old_ranks": 2014, "old_dag_nodes": 2014,
                    "old_seed_lower": 176, "old_actor_lower": 8056,
                    "direct_packet_halves": 32928},
        "equality_receipts": equality,
        "equality_receipts_sha256": sha(canonical(equality)),
        "projector_identity": projector,
        "downstream_claim_flags": dict(CLAIMS),
        "resident_global_matrix": False, "independent_checker": False,
        "precision2": False, "A0": False, "COMMON": False,
        "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
        "verified": False, "elapsed_seconds": 0.0,
        "peak_rss_bytes": 0,
    }
    blocks = []
    for index, rank in enumerate(NEW_RANKS):
        blocks.append({
            "schema": "d972.r07.p1.componentwise.block.v1", "phase": "block",
            "producer_sha256": producer, "source_run": SOURCE_RUN,
            "source_attempt": SOURCE_ATTEMPT, "source_head": SOURCE_HEAD,
            "prepare_body_sha256": PREPARE_DIGEST, "block_index": index,
            "block_body_sha256": PARENTS[index], "basis_sha256": BASIS[index],
            "counts": {"packet_basis_halves": 8232,
                        "new_actor_identities": 4 * rank,
                        "new_dag_identities": rank,
                        "compound_obligations": 8232 + 4 * rank},
            "rank": rank, "attempts": 8232 + 4 * rank,
            "dag_sha256": f"{index + 20:064x}",
            "downstream_claim_flags": dict(CLAIMS),
            "resident_global_matrix": False, "independent_checker": False,
            "precision2": False, "A0": False, "COMMON": False,
            "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
            "verified": False, "elapsed_seconds": 0.0,
            "peak_rss_bytes": 0,
        })
    return prepare, blocks


def fixture_join_receipt(producer: str) -> dict[str, Any]:
    return {
        "schema": "d972.r07.p1.componentwise.v1",
        "terminal": "TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED",
        "global_relations": 32280, "old_ranks": 2014, "new_ranks": 6045,
        "dag_nodes": 8059, "old_local_relations": 8232,
        "direct_packet_halves": 32928, "packet_basis_halves": 32928,
        "new_actor_identities": 24180, "compound_obligations": 65340,
        "resident_global_matrix": False, "independent_checker": False,
        "precision2": False, "A0": False, "COMMON": False,
        "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
        "verified": False, "producer_sha256": producer,
    }


def validate_projector_full(value: Any, expected: dict[str, Any]) -> None:
    require(value == expected, "projector_full")


def selftest() -> dict[str, Any]:
    accepted = 0
    rejected = 0
    live: list[str] = []
    table: dict[str, str] = {}

    # The actual quotient/affine/Fox context is deliberately initialized.
    words = load_words()
    context = Context(words)
    projector, projector_full = projector_identity(context)
    live.append("projector_identity")
    require(projector["cv_sum_table"] == [1, 0, 0, 0], "fixture_projector")
    accepted += 1

    # A toy safe root enters the exact non-following root and roster gate.
    with tempfile.TemporaryDirectory() as temporary:
        sealed_root = Path(temporary) / "sealed"
        sealed_root.mkdir()
        def write_fixture_head(stem, parent):
            body_raw = canonical({"fixture": stem})
            digest = sha(body_raw)
            (sealed_root / f"{stem}.HEAD").write_bytes(canonical({
                "body_sha256": digest,
                "parent_sha256": parent,
                "schema": "d972.r07.a0.first-rung-grade1.v3.state.head",
                "stem": stem,
            }))
            (sealed_root / f"{stem}.{digest}.json").write_bytes(body_raw)
            return digest
        prepare_fixture_digest = write_fixture_head("prepare", None)
        read_sealed(sealed_root, "prepare", prepare_fixture_digest, None)
        for index in range(4):
            stem = f"block-{index}"
            digest = write_fixture_head(stem, PREPARE_DIGEST)
            read_sealed(sealed_root, stem, digest, PREPARE_DIGEST)
        bad_head = json.loads((sealed_root / "prepare.HEAD").read_bytes())
        bad_head["schema"] = "d972.r07.a0.first-rung-grade1.v3.head"
        (sealed_root / "prepare.HEAD").write_bytes(canonical(bad_head))
        rejected += expect_reject(
            lambda: read_sealed(sealed_root, "prepare",
                                prepare_fixture_digest, None))
        live.append("sealed_head_schema")
        accepted += 1

        toy_root = Path(temporary) / "toy"
        toy_root.mkdir()
        (toy_root / "toy.bin").write_bytes(bytes([0, 80]))
        safe, names = safe_root(toy_root)
        exact_roster(names, ["toy.bin"])
        live.append("safe_root")
        accepted += 1
        rejected += expect_reject(lambda: safe_root(toy_root / "toy.bin"))

        # The segment kernel must honour the second-character offset and EOF.
        stream = io.BytesIO(bytes(range(20)))
        packet_seek(stream, 2, 5, 2, expected_begin=2)
        require(stream.read(6) == bytes(range(4, 10)), "fixture_packet_segment")
        packet_finish(stream, 5, 2)
        live.append("packet_segment")
        accepted += 1
        table["second_character_offset_reset"] = "REJECT" if expect_reject(
            lambda: packet_range_binding(0, 2056, 2064, 2056)) else "ACCEPT"
        trailing = io.BytesIO(b"\x00\x00\x01")
        trailing.seek(2)
        table["malformed_trailing_packet"] = "REJECT" if expect_reject(
            lambda: packet_finish(trailing, 1, 2, eof=True)) else "ACCEPT"
        rejected += 1
        rejected += 1

    # A small old row enters PackedEchelon closure, actor action, reduction,
    # DAG reconstruction, and exact negative-lift arithmetic.
    seed = np.zeros(LOWER_WIDTH, dtype=np.uint8)
    seed[0] = 1
    owner, record = close_lower_block(context, CHARACTERS[0], [seed],
                                      started=time.monotonic(), phase="fixture-old")
    lifts = evaluate_old_lifts(context, CHARACTERS[0], owner, record,
                               [np.zeros(SOURCE_TOTAL, dtype=np.uint8)],
                               started=time.monotonic(), phase="fixture-lift")
    require(lifts.shape == (len(owner.rows), SOURCE_TOTAL), "fixture_lift_shape")
    live.extend(["old_closure", "old_reduction", "old_lift_dag"])
    accepted += 1

    # Two distinct origins enter the production comparison branch in order.
    block_row = np.zeros(SOURCE_BLOCK, dtype=np.uint8)
    block_row[0] = 1
    block_row_2 = np.zeros(SOURCE_BLOCK, dtype=np.uint8)
    block_row_2[1] = 1
    packets = [pack_trits(block_row).tobytes(), pack_trits(block_row_2).tobytes()]
    block_result = replay_block_kernel(context, CHARACTERS[0],
                                       packets,
                                       started=time.monotonic(), phase="fixture-block")
    require(block_result["packet_count"] == 2
            and block_result["origins"][0] != block_result["origins"][1],
            "fixture_block_fifo")
    replay_block_kernel(context, CHARACTERS[0], packets,
                        expected_origin_reductions=block_result["origins"],
                        expected_nodes=block_result["nodes"],
                        expected_transitions=block_result["transitions"],
                        expected_basis=block_result["basis"],
                        expected_rank=len(block_result["owner"].rows),
                        phase="fixture-block-expected")
    live.append("block_fifo")
    accepted += 1

    # Canonical producer receipts enter the same strict peer validator and
    # obligation join used after the five real phases.
    manifest_digest = sha(canonical(pinned_input_manifest()))
    producer = producer_source_digest()
    peer_prepare, peer_blocks = fixture_peer_receipts(producer, manifest_digest,
                                                       projector)
    peer_join = fixture_join_receipt(producer)
    validate_producer_chain(peer_prepare, peer_blocks, peer_join, producer,
                            manifest_digest)
    ours_prepare = json.loads(json.dumps(peer_prepare))
    ours_prepare["independent_checker"] = True
    ours_blocks = json.loads(json.dumps(peer_blocks))
    for peer_block in ours_blocks:
        peer_block["independent_checker"] = True
    compare_semantic_receipts(ours_prepare, ours_blocks, peer_prepare, peer_blocks)
    live.append("receipt_comparison")
    accepted += 1

    # Required rejection table.  Every item is a live call into a production
    # parser, arithmetic comparator, or receipt gate.
    class FixtureOwner:
        rows = [None, None]
    grade0 = np.zeros(SOURCE_TOTAL, dtype=np.uint8)
    grade1 = np.zeros(SOURCE_TOTAL, dtype=np.uint8)
    grade0[0] = 1
    grade1[0] = 2
    lift_record = {"dag_nodes": [
        {"pivot": 0, "origin": {"kind": "projected_seed", "seed": 1},
         "reductions": [], "scale": 1},
        {"pivot": 1, "origin": {"kind": "projected_seed", "seed": 2},
         "reductions": [[0, 1]], "scale": 1},
    ]}
    signed_lifts = evaluate_old_lifts(
        context, CHARACTERS[0], FixtureOwner(), lift_record, [grade0, grade1],
        started=time.monotonic(), phase="fixture-signed-lift")
    wrong_sign = (grade1.astype(np.uint16) + grade0.astype(np.uint16)) % 3
    table["sign_flip"] = "REJECT" if expect_reject(
        lambda: compare_bytes(signed_lifts[1].tobytes(),
                              wrong_sign.astype(np.uint8).tobytes(),
                              "fixture_sign")) else "ACCEPT"
    table["swapped_packet_origins"] = "REJECT" if expect_reject(
        lambda: replay_block_kernel(
            context, CHARACTERS[0], packets,
            expected_origin_reductions=list(reversed(block_result["origins"])),
            phase="fixture-block-swapped")) else "ACCEPT"
    body_probe = {key: None for key in BLOCK_BODY_KEYS}
    validate_block_body_keys(body_probe)
    missing_origin = dict(body_probe)
    del missing_origin["origin_reductions"]
    table["missing_origin_reductions"] = "REJECT" if expect_reject(
        lambda: validate_block_body_keys(missing_origin)) else "ACCEPT"
    renamed_origin = dict(missing_origin)
    renamed_origin["origins"] = None
    table["renamed_origin_reductions"] = "REJECT" if expect_reject(
        lambda: validate_block_body_keys(renamed_origin)) else "ACCEPT"
    coefficient_probe = PackedEchelon(8).insert(
        np.asarray([0, 2, 0, 0, 0, 0, 0, 0], dtype=np.uint8))
    require(coefficient_probe["accepted"] and coefficient_probe["scale"] == 2,
            "fixture_coefficient_probe")
    table["coefficient_2_changed_to_1"] = "REJECT" if expect_reject(
        lambda: require(coefficient_probe["scale"] == 1, "fixture_scale")) else "ACCEPT"
    table["wrong_actor_order"] = "REJECT" if expect_reject(
        lambda: validate_actor_order([1, 2, -1, -2])) else "ACCEPT"
    table["word_reversal"] = "REJECT" if expect_reject(
        lambda: require(tuple(reversed(PURE_Q1_WORDS[(1, 0)])) == PURE_Q1_WORDS[(1, 0)],
                        "fixture_word_reversal")) else "ACCEPT"
    table["forward_dag_edge"] = "REJECT" if expect_reject(
        lambda: validate_prior_expression([[0, 1]], 0)) else "ACCEPT"
    table["wrong_block_basis_byte"] = "REJECT" if expect_reject(
        lambda: compare_bytes(b"\x00", b"\x01", "fixture_basis")) else "ACCEPT"
    table["projector_vector_mutation"] = "REJECT" if expect_reject(
        lambda: validate_projector_receipt({**projector, "cv_sum_table": [1, 1, 0, 0]})) else "ACCEPT"
    bool_projector = {**projector, "cv_sum_table": [True, False, False, False]}
    table["projector_bool_table"] = "REJECT" if expect_reject(
        lambda: validate_projector_receipt(bool_projector)) else "ACCEPT"
    altered_projector = json.loads(json.dumps(projector_full))
    altered_projector["pure_q1_projectors"][2]["word"].reverse()
    table["projector_word_reversal"] = "REJECT" if expect_reject(
        lambda: validate_projector_entries(altered_projector["pure_q1_projectors"])) else "ACCEPT"
    # Mutate one compound count while retaining the exact block roster.
    bad_blocks = json.loads(json.dumps(peer_blocks))
    bad_blocks[0]["counts"]["compound_obligations"] -= 1
    table["wrong_obligation_arithmetic"] = "REJECT" if expect_reject(
        lambda: validate_obligation_totals(peer_prepare, bad_blocks)) else "ACCEPT"
    table["bool_as_int"] = "REJECT" if expect_reject(
        lambda: require(plain_int(True), "fixture_bool")) else "ACCEPT"
    wrong_parent = json.loads(json.dumps(peer_blocks[0]))
    wrong_parent["block_body_sha256"] = "0" * 64
    table["wrong_parent_digest"] = "REJECT" if expect_reject(
        lambda: validate_peer_block(wrong_parent, 0, producer)) else "ACCEPT"
    bad_flags = json.loads(json.dumps(peer_blocks))
    bad_flags[0]["downstream_claim_flags"]["A0"] = True
    table["producer_claim_A0"] = "REJECT" if expect_reject(
        lambda: validate_peer_block(bad_flags[0], 0, producer)) else "ACCEPT"
    table["producer_claim_COMMON"] = "REJECT" if expect_reject(
        lambda: validate_downstream_flags({**CLAIMS, "COMMON": 0}, "fixture_claim")) else "ACCEPT"
    for field in ("COMMON", "COMPATIBLE_LIFT", "FAKE", "IHARA", "verified"):
        mutated = json.loads(json.dumps(peer_prepare))
        mutated[field] = True
        table["producer_claim_" + field] = "REJECT" if expect_reject(
            lambda value=mutated: validate_peer_prepare(
                value, producer, manifest_digest)) else "ACCEPT"

    for field, value in (("terminal", "WRONG"), ("compound_obligations", 65339),
                         ("FAKE", True)):
        mutated_join = json.loads(json.dumps(peer_join))
        mutated_join[field] = value
        table["join_" + field] = "REJECT" if expect_reject(
            lambda value=mutated_join: validate_join_receipt(
                value, producer, peer_prepare, peer_blocks)) else "ACCEPT"
    table["missing_join"] = "REJECT" if expect_reject(
        lambda: validate_join_receipt(None, producer, peer_prepare, peer_blocks)) else "ACCEPT"
    reordered = list(reversed(peer_blocks))
    table["reordered_phase_receipts"] = "REJECT" if expect_reject(
        lambda: validate_producer_chain(peer_prepare, reordered, peer_join,
                                        producer, manifest_digest)) else "ACCEPT"

    with tempfile.TemporaryDirectory() as temporary:
        altered_source = Path(temporary) / "producer.py"
        altered_source.write_bytes(PRODUCER_V5_SOURCE.read_bytes() + b"\n")
        table["producer_source_bytes"] = "REJECT" if expect_reject(
            lambda: validate_producer_source(altered_source, PRODUCER_V5_SHA)) else "ACCEPT"
        table["producer_source_sha"] = "REJECT" if expect_reject(
            lambda: validate_producer_source(PRODUCER_V5_SOURCE, "0" * 64)) else "ACCEPT"

    # Nested exact schema/type mutations are charged separately.
    altered = json.loads(json.dumps(peer_prepare))
    altered["counts"]["old_seed_lower"] = True
    table["nested_bool_count"] = "REJECT" if expect_reject(
        lambda: validate_peer_prepare(altered, producer, manifest_digest)) else "ACCEPT"
    altered = json.loads(json.dumps(peer_prepare))
    altered["equality_receipts"][0]["character_index"] = True
    table["nested_bool_index"] = "REJECT" if expect_reject(
        lambda: validate_peer_prepare(altered, producer, manifest_digest)) else "ACCEPT"
    altered = json.loads(json.dumps(peer_prepare))
    altered["source_head"] = "0" * 40
    table["wrong_source_head"] = "REJECT" if expect_reject(
        lambda: validate_peer_prepare(altered, producer, manifest_digest)) else "ACCEPT"
    altered = json.loads(json.dumps(peer_blocks))
    altered[1]["rank"] = False
    table["nested_bool_rank"] = "REJECT" if expect_reject(
        lambda: validate_peer_block(altered[1], 1, producer)) else "ACCEPT"
    altered = json.loads(json.dumps(peer_prepare))
    altered["elapsed_seconds"] = False
    table["nested_bool_telemetry"] = "REJECT" if expect_reject(
        lambda: validate_peer_prepare(altered, producer, manifest_digest)) else "ACCEPT"

    def cli(**changes: Any) -> argparse.Namespace:
        base = {"selftest": False, "check": None, "prepare_root": None,
                "block_roots": None, "phase_receipts": None,
                "join_receipt": None, "out": None}
        base.update(changes)
        return argparse.Namespace(**base)
    validate_cli(cli(selftest=True))
    validate_cli(cli(check=["x"] * 12))
    validate_cli(cli(prepare_root=Path("p"), block_roots=[Path("b")] * 4,
                     phase_receipts=[Path("r")] * 5,
                     join_receipt=Path("j"), out=Path("o")))
    table["mixed_cli"] = "REJECT" if expect_reject(
        lambda: validate_cli(cli(selftest=True, check=["x"] * 12))) else "ACCEPT"
    table["partial_named_cli"] = "REJECT" if expect_reject(
        lambda: validate_cli(cli(prepare_root=Path("p")))) else "ACCEPT"
    table["compact_named_cli"] = "REJECT" if expect_reject(
        lambda: validate_cli(cli(check=["x"] * 12, out=Path("o")))) else "ACCEPT"

    rejected += len(table)
    require(all(status == "REJECT" for status in table.values()), "fixture_rejection_table")
    result = {
        "status": "PASS", "fixture_accept": accepted,
        "rejections": rejected, "live_kernels": live,
        "rejection_table": table,
        "actual_five_artifact_check": "DEFERRED_TO_GHA",
        "verified": False,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")), flush=True)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--check", nargs=12,
                        metavar=("PREPARE_ROOT", "BLOCK0_ROOT", "BLOCK1_ROOT",
                                 "BLOCK2_ROOT", "BLOCK3_ROOT", "PREP_RECEIPT",
                                 "B0_RECEIPT", "B1_RECEIPT", "B2_RECEIPT",
                                 "B3_RECEIPT", "JOIN_RECEIPT", "OUTPUT"))
    parser.add_argument("--prepare-root", type=Path)
    parser.add_argument("--block-roots", nargs=4, type=Path)
    parser.add_argument("--phase-receipts", nargs=5, type=Path)
    parser.add_argument("--join-receipt", type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def validate_cli(args: argparse.Namespace) -> str:
    named_values = (args.prepare_root, args.block_roots, args.phase_receipts,
                    args.join_receipt, args.out)
    self_mode = args.selftest and args.check is None and all(
        value is None for value in named_values)
    compact_mode = (not args.selftest and args.check is not None
                    and len(args.check) == 12
                    and all(value is None for value in named_values))
    named_mode = (not args.selftest and args.check is None
                  and all(value is not None for value in named_values)
                  and len(args.block_roots) == 4
                  and len(args.phase_receipts) == 5)
    require(sum((self_mode, compact_mode, named_mode)) == 1, "usage_mode")
    return "selftest" if self_mode else ("compact" if compact_mode else "named")


def main() -> int:
    args = parse_args()
    try:
        mode = validate_cli(args)
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc),
                          "verified": False}, separators=(",", ":")),
              file=sys.stderr, flush=True)
        return 1
    if mode == "selftest":
        try:
            selftest()
            return 0
        except ResourceExhausted as exc:
            print(json.dumps({"status": "UNKNOWN_RESOURCE", "error": str(exc),
                              "verified": False}, separators=(",", ":")),
                  file=sys.stderr, flush=True)
            return 2
        except Exception as exc:
            print(json.dumps({"status": "REJECTED", "error": str(exc),
                              "verified": False}, separators=(",", ":")),
                  file=sys.stderr, flush=True)
            return 1
    try:
        if mode == "compact":
            prep = Path(args.check[0])
            blocks = [Path(x) for x in args.check[1:5]]
            phase_paths = [Path(x) for x in args.check[5:10]]
            join_path = Path(args.check[10])
            output = Path(args.check[11])
        else:
            prep, blocks = args.prepare_root, args.block_roots
            phase_paths, join_path, output = (args.phase_receipts,
                                               args.join_receipt, args.out)
        run_actual_check(prep, list(blocks), list(phase_paths), join_path, output)
        return 0
    except ResourceExhausted as exc:
        # No receipt or marker is written before all semantic phases, so this
        # branch can only expose UNKNOWN_RESOURCE.
        print(json.dumps({"status": "UNKNOWN_RESOURCE", "error": str(exc),
                          "verified": False}, separators=(",", ":")),
              file=sys.stderr, flush=True)
        return 2
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc),
                          "verified": False}, separators=(",", ":")),
              file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
