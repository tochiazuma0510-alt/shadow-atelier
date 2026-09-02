#!/usr/bin/env python3
"""Task562 v4: exact first relative grade with merge hot-loop repair.

This producer is intentionally phase-oriented.  State is written body first
and authenticated by an atomic HEAD replacement.  Mathematical terminals are
fail closed: only a completed merge may emit MEMBER or NONMEMBER.
"""
from __future__ import annotations

import argparse
import ast
import bisect
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Iterator

import numpy as np

# Reuse the frozen Task542 primitives.  Its run() is deliberately neither
# called nor copied: Task554 owns the phase graph and the filtered arithmetic.
import d972_r07_a0_c2fourier_joint_floor_v1 as floor


ROOT = Path(__file__).resolve().parents[1]
# Deliberately retained: v4 consumes the sealed v3 prepare/block state chain.
SCHEMA = "d972.r07.a0.first-rung-grade1.v3"
STATE_SCHEMA = SCHEMA + ".state"
CHARACTER_LABELS = ((0, 0), (0, 1), (1, 0), (1, 1))
MONOMIALS_GRADE1 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
SOURCE_BASE_WIDTH = 6 * 2 * 504
SOURCE_BLOCK_WIDTH = SOURCE_BASE_WIDTH * len(MONOMIALS_GRADE1)
SOURCE_TOTAL_WIDTH = len(CHARACTER_LABELS) * SOURCE_BLOCK_WIDTH
PHYSICAL_BLOCK_WIDTH = 4 * 2016
PHYSICAL_GRADE_WIDTH = PHYSICAL_BLOCK_WIDTH * len(MONOMIALS_GRADE1)
LOWER_AUX_WIDTH = 8  # six occurrence PB3 augmentations + two normalized exponents
LOWER_ECHELON_WIDTH = SOURCE_BASE_WIDTH + LOWER_AUX_WIDTH
PHYSICAL_LOWER_REGULAR_WIDTH = 4 * 2 * 2 * 504
PHYSICAL_LOWER_AUX_WIDTH = 4  # two PB3 augmentations + two normalized exponents
PHYSICAL_LOWER_WIDTH = PHYSICAL_LOWER_REGULAR_WIDTH + PHYSICAL_LOWER_AUX_WIDTH
ACTORS = (1, -1, 2, -2)
ETA = ((0, 1), (1, 0), (1, 1))
PURE_Q1_WORDS = {
    (0, 0): (),
    (0, 1): (-2, -2, -2, -2, -2, -2, -2, -2, -2),
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}

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
    "scratchpad/a0_paper_words_v1.json": "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893",
    "scratchpad/fuda1_a0_rmax_data.g": "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba",
    "sol/proof_r07_first_rung_character_projector_word_repair_v447.md": "3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2",
    "sol/proof_r07_first_rung_six_grade_index_repair_v449.md": "0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9",
    "sol/sol_reply_555_audit_r07_a0_six_grade_schedule_v1.md": "8dcdfbb4825c65bff9698311b735e830c27d39f98405bcfb01af3411d97a2e45",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def load_pinned_inputs() -> tuple[dict[str, bytes], dict[str, dict[str, Any]]]:
    payloads: dict[str, bytes] = {}
    receipt: dict[str, dict[str, Any]] = {}
    for rel, expected in INPUT_PINS.items():
        path = ROOT / rel
        data = path.read_bytes()
        actual = sha256_bytes(data)
        if actual != expected:
            raise RuntimeError(f"frozen_hash_mismatch:{rel}:{actual}")
        payloads[rel] = data
        receipt[rel] = {"bytes": len(data), "sha256": actual}
    audit = payloads["sol/sol_reply_553_audit_r07_a0_character_blocks_coupled_monomials_v1.md"].decode("utf-8")
    if "FIRST_RUNG_CHARACTER_BLOCKS_PASS_AFTER_REPAIR" not in audit:
        raise RuntimeError("task553_gate_closed")
    return payloads, receipt


def freely_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        if letter not in (-2, -1, 1, 2):
            raise ValueError(f"bad_free_letter:{letter}")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def canonicalize_full_literal_terms(terms: Any) -> list[list[Any]]:
    """Canonical F3 sum by (seed, freely-reduced conjugator).

    The accepted Task542 certificate stores exactly the three-element arrays
    ``[seed, conjugator, coefficient]`` with one-based seed numbers.  Aliases
    are rejected: accepting a shape-shifted term here could silently change
    the literal map.  Output deliberately preserves the same array schema.
    """
    if not isinstance(terms, list):
        raise TypeError("full_literal_terms_not_list")
    acc: dict[tuple[int, tuple[int, ...]], int] = {}
    for pos, term in enumerate(terms):
        if not isinstance(term, list) or len(term) != 3:
            raise ValueError(f"full_literal_term_shape:{pos}")
        seed = int(term[0])
        if seed < 1 or seed > 44:
            raise ValueError(f"full_literal_seed:{pos}:{seed}")
        if not isinstance(term[1], list):
            raise ValueError(f"full_literal_conjugator:{pos}")
        conjugator = freely_reduce(term[1])
        coefficient = int(term[2])
        if coefficient not in (1, 2):
            raise ValueError(f"full_literal_coefficient:{pos}:{coefficient}")
        key = (seed, conjugator)
        acc[key] = (acc.get(key, 0) + coefficient) % 3
    return [
        [seed, list(conjugator), coefficient]
        for (seed, conjugator), coefficient in sorted(acc.items(), key=lambda item: (item[0][0], item[0][1]))
        if coefficient
    ]


def validate_fixed_layouts() -> None:
    if CHARACTER_LABELS != ((0, 0), (0, 1), (1, 0), (1, 1)):
        raise RuntimeError("character_layout_changed")
    if MONOMIALS_GRADE1 != ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        raise RuntimeError("monomial_layout_changed")
    if (SOURCE_BASE_WIDTH, SOURCE_BLOCK_WIDTH, SOURCE_TOTAL_WIDTH, PHYSICAL_GRADE_WIDTH) != (6048, 18144, 72576, 24192):
        raise RuntimeError("ambient_width_changed")


def cv(label: tuple[int, int], a: int, b: int) -> int:
    return 1 if ((label[0] * a + label[1] * b) & 1) == 0 else 2


def xor_label(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] ^ right[0], left[1] ^ right[1]


def lower_coord(tag: int, component: int, psl: int) -> int:
    return (tag * 2 + component) * 504 + psl


def grade_coord(tag: int, component: int, monomial: int, psl: int) -> int:
    return ((tag * 2 + component) * 3 + monomial) * 504 + psl


def physical_lower_coord(character: int, block: int, component: int, psl: int) -> int:
    return ((character * 2 + block) * 2 + component) * 504 + psl


def physical_grade_coord(character: int, block: int, component: int, monomial: int, psl: int) -> int:
    return (((character * 2 + block) * 2 + component) * 3 + monomial) * 504 + psl


Affine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]


def sign_kernel(parity: tuple[int, int], vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((cv(ETA[i], parity[0], parity[1]) * vector[i]) % 3 for i in range(3))  # type: ignore[return-value]


def affine_mul(left: Affine, right: Affine) -> Affine:
    acted = sign_kernel((right[1], right[2]), left[3])
    return (
        floor.M(left[0], right[0]),
        left[1] ^ right[1],
        left[2] ^ right[2],
        tuple((acted[i] + right[3][i]) % 3 for i in range(3)),  # type: ignore[arg-type]
    )


def affine_inv(value: Affine) -> Affine:
    acted = sign_kernel((value[1], value[2]), value[3])
    return floor.inv(value[0]), value[1], value[2], tuple((-x) % 3 for x in acted)  # type: ignore[return-value]


def affine_eval(word: Iterable[int], images: tuple[Affine, Affine]) -> Affine:
    out: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for letter in word:
        out = affine_mul(out, images[abs(letter) - 1] if letter > 0 else inverses[abs(letter) - 1])
    return out


def affine_fox(word: Iterable[int], images: tuple[Affine, Affine]) -> tuple[dict[tuple[int, Affine], int], Affine]:
    out: dict[tuple[int, Affine], int] = {}
    prefix: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for letter in word:
        generator = abs(int(letter)) - 1
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


class Context:
    def __init__(self, words: dict[str, Any]):
        match = re.search(
            r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;",
            (ROOT / "scratchpad/fuda1_a0_rmax_data.g").read_text(encoding="utf-8"),
            re.S,
        )
        if match is None:
            raise RuntimeError("q0_marking_parse")
        q36 = tuple(tuple(x - 1 for x in ast.literal_eval(match.group(i))) for i in (1, 2))
        self.q36 = q36
        self.a, self.c = q36[0][:9], q36[1][:9]
        self.psels, self.psidx = floor.group((self.a, self.c))
        if len(self.psels) != 504:
            raise RuntimeError("psl_order")
        floor.psels, floor.psidx = self.psels, self.psidx
        self.q1_images = ((self.a, 1, 0), (self.c, 0, 1))
        floor.qb = floor.qinv(floor.qmul(self.q1_images[1], self.q1_images[0]))
        self.affine_images: tuple[Affine, Affine] = (
            (self.a, 1, 0, (1, 0, 0)),
            (self.c, 0, 1, (1, 1, 1)),
        )
        if self.affine_images[0] != affine_mul(self.affine_images[0], ((floor.ID9, 0, 0, (0, 0, 0)))):
            raise RuntimeError("affine_identity")
        if affine_inv(self.affine_images[0])[3] != (2, 0, 0) or affine_inv(self.affine_images[1])[3] != (1, 2, 1):
            raise RuntimeError("marked_inverse_gate")
        self.pb3_b = affine_inv(affine_mul(self.affine_images[1], self.affine_images[0]))
        if affine_mul(affine_mul(self.affine_images[0], self.pb3_b), self.affine_images[1]) != (floor.ID9, 0, 0, (0, 0, 0)):
            raise RuntimeError("pb3_boundary_word")
        self.transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        self.inverse_transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        self.substitution_matrices: list[list[list[int]]] = []
        for left_word, right_word in floor.OO:
            left = floor.qev(left_word, self.q1_images)
            right = floor.qev(right_word, self.q1_images)
            matrix = ((left[1], right[1]), (left[2], right[2]))
            inverse = None
            for aa in range(2):
                for ab in range(2):
                    for ba in range(2):
                        for bb in range(2):
                            candidate = ((aa, ab), (ba, bb))
                            if self._matrix_mul(matrix, candidate) == ((1, 0), (0, 1)) and self._matrix_mul(candidate, matrix) == ((1, 0), (0, 1)):
                                inverse = candidate
            if inverse is None:
                raise RuntimeError("occurrence_matrix_singular")
            mapping = {
                label: (
                    label[0] * inverse[0][0] ^ label[1] * inverse[1][0],
                    label[0] * inverse[0][1] ^ label[1] * inverse[1][1],
                )
                for label in CHARACTER_LABELS
            }
            self.transport.append(mapping)
            self.inverse_transport.append({target: source for source, target in mapping.items()})
            self.substitution_matrices.append([list(matrix[0]), list(matrix[1])])
        floor.TRANSPORT = self.transport
        self.actor_words = {letter: ((letter,),) for letter in ACTORS}
        self.actor_source_q1 = {letter: floor.qev((letter,), self.q1_images) for letter in ACTORS}
        self.actor_tags_affine = {
            letter: tuple(affine_eval(floor.sub((letter,), *pair), self.affine_images) for pair in floor.OO)
            for letter in ACTORS
        }
        self.actor_tags_q1 = {
            letter: tuple((value[0], value[1], value[2]) for value in self.actor_tags_affine[letter])
            for letter in ACTORS
        }
        self.pure_source_affine: dict[tuple[int, int], Affine] = {}
        self.pure_tags_affine: dict[tuple[int, int], tuple[Affine, ...]] = {}
        for parity, word in PURE_Q1_WORDS.items():
            q1_value = floor.qev(word, self.q1_images)
            if q1_value != (floor.ID9, parity[0], parity[1]):
                raise RuntimeError(f"pure_q1_word_endpoint:{parity}")
            self.pure_source_affine[parity] = affine_eval(word, self.affine_images)
            self.pure_tags_affine[parity] = tuple(
                affine_eval(floor.sub(word, *pair), self.affine_images) for pair in floor.OO
            )
        g760 = tuple(int(x) for x in words["g760"])
        self.g760 = g760
        g_tags = tuple(affine_eval(floor.sub(g760, *pair), self.affine_images) for pair in floor.OO)
        self.physical_shifts = (
            (floor.ID9, 0, 0, (0, 0, 0)),
            g_tags[2],
            g_tags[2],
            affine_mul(g_tags[5], affine_inv(g_tags[4])),
            g_tags[5],
            g_tags[5],
        )
        self.aggregate_table = ((0, 0, 1), (1, 0, 2), (2, 0, 1), (3, 1, 2), (4, 1, 2), (5, 1, 1))
        self.psl_maps: dict[tuple[tuple[int, ...], str], np.ndarray] = {}
        for family, values in (("actor", sum((list(v) for v in self.actor_tags_affine.values()), [])), ("shift", list(self.physical_shifts))):
            for value in values:
                key = value[0], family
                if key not in self.psl_maps:
                    self.psl_maps[key] = np.asarray([self.psidx[floor.M(value[0], p)] for p in self.psels], dtype=np.int32)

    @staticmethod
    def _matrix_mul(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            (left[0][0] * right[0][0] ^ left[0][1] * right[1][0], left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
            (left[1][0] * right[0][0] ^ left[1][1] * right[1][0], left[1][0] * right[0][1] ^ left[1][1] * right[1][1]),
        )

    def source_word_tags(self, word: tuple[int, ...]) -> tuple[Affine, ...]:
        return tuple(affine_eval(floor.sub(word, *pair), self.affine_images) for pair in floor.OO)

    def source_word_value(self, word: tuple[int, ...]) -> Affine:
        return affine_eval(word, self.affine_images)

    def psl_left_map(self, permutation: tuple[int, ...]) -> np.ndarray:
        key = permutation, "left"
        if key not in self.psl_maps:
            self.psl_maps[key] = np.asarray(
                [self.psidx[floor.M(permutation, value)] for value in self.psels], dtype=np.int32
            )
        return self.psl_maps[key]


def _add_mod3(destination: np.ndarray, source: np.ndarray, scalar: int = 1) -> None:
    if scalar % 3:
        destination[:] = (destination.astype(np.uint16) + (scalar % 3) * source.astype(np.uint16)) % 3


def _translated_psl(source: np.ndarray, pmap: np.ndarray, scalar: int) -> np.ndarray:
    out = np.zeros(504, dtype=np.uint8)
    out[pmap] = ((scalar % 3) * source.astype(np.uint16)) % 3
    return out


def qnorm_affine(word: tuple[int, ...], context: Context) -> tuple[list[tuple[int, Affine, int]], int]:
    gradient, endpoint = affine_fox(word, context.affine_images)
    if endpoint != (floor.ID9, 0, 0, (0, 0, 0)):
        raise RuntimeError("q2_literal_endpoint")
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
    """Evaluate one literal seed through degrees zero and one.

    Returns Fourier source-character coordinates, not four independently
    generated rows.  The final axis of the grade array keeps all three
    monomials coupled.
    """
    lower = np.zeros((4, SOURCE_BASE_WIDTH), dtype=np.uint8)
    grade = np.zeros((4, SOURCE_BLOCK_WIDTH), dtype=np.uint8)
    auxiliary = np.zeros(LOWER_AUX_WIDTH, dtype=np.uint8)
    for tag, pair in enumerate(floor.OO):
        substituted = tuple(floor.sub(word, *pair))
        normal, augmentation = qnorm_affine(substituted, context)
        auxiliary[tag] = augmentation
        for component, value, coefficient in normal:
            psl = context.psidx[value[0]]
            for source_index, source_label in enumerate(CHARACTER_LABELS):
                target_label = context.transport[tag][source_label]
                weight = coefficient * cv(target_label, value[1], value[2])
                li = lower_coord(tag, component, psl)
                lower[source_index, li] = (int(lower[source_index, li]) + weight) % 3
                for monomial, monomial_coefficient in enumerate(value[3]):
                    if monomial_coefficient:
                        gi = grade_coord(tag, component, monomial, psl)
                        grade[source_index, gi] = (
                            int(grade[source_index, gi]) + weight * monomial_coefficient
                        ) % 3
    exponent = floor.exps(word)
    if exponent[0] % 18 or exponent[1] % 18:
        raise RuntimeError("normalized_exponent_not_integral")
    auxiliary[6:] = ((exponent[0] // 18) % 3, (exponent[1] // 18) % 3)
    return lower, grade, auxiliary


def act_pair(
    context: Context,
    lower: np.ndarray,
    grade: np.ndarray,
    auxiliary: np.ndarray,
    source_actor: Affine,
    tag_actors: tuple[Affine, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if lower.shape != (4, SOURCE_BASE_WIDTH) or grade.shape != (4, SOURCE_BLOCK_WIDTH):
        raise ValueError("paired_shape")
    out_lower = np.zeros_like(lower)
    out_grade = np.zeros_like(grade)
    for source_index, source_label in enumerate(CHARACTER_LABELS):
        common_scalar = cv(source_label, source_actor[1], source_actor[2])
        for tag, actor in enumerate(tag_actors):
            pmap = context.psl_left_map(actor[0])
            target_label = context.transport[tag][source_label]
            for component in (0, 1):
                lower_slice = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
                translated_lower = _translated_psl(lower[source_index, lower_slice], pmap, common_scalar)
                out_lower[source_index, lower_slice] = translated_lower
                for monomial in range(3):
                    grade_slice = slice(
                        grade_coord(tag, component, monomial, 0),
                        grade_coord(tag, component, monomial, 0) + 504,
                    )
                    # Other source characters can already have contributed
                    # an induced kernel term to this character slice.  The
                    # direct term must add, not overwrite (v443 (3.1)).
                    _add_mod3(
                        out_grade[source_index, grade_slice],
                        _translated_psl(grade[source_index, grade_slice], pmap, common_scalar),
                    )
                    kernel_coefficient = actor[3][monomial]
                    if kernel_coefficient:
                        output_target = xor_label(target_label, ETA[monomial])
                        output_source = context.inverse_transport[tag][output_target]
                        output_index = CHARACTER_LABELS.index(output_source)
                        induced_scalar = kernel_coefficient * cv(output_target, actor[1], actor[2])
                        _add_mod3(
                            out_grade[output_index, grade_slice],
                            _translated_psl(lower[source_index, lower_slice], pmap, induced_scalar),
                        )
    return out_lower, out_grade, auxiliary.copy()


def act_source_word(
    context: Context,
    lower: np.ndarray,
    grade: np.ndarray,
    auxiliary: np.ndarray,
    word: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return act_pair(context, lower, grade, auxiliary, context.source_word_value(word), context.source_word_tags(word))


def projected_seed_pair(
    context: Context,
    base: tuple[np.ndarray, np.ndarray, np.ndarray],
    label: tuple[int, int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lower = np.zeros_like(base[0])
    grade = np.zeros_like(base[1])
    auxiliary = np.zeros_like(base[2])
    for parity in CHARACTER_LABELS:
        acted = act_pair(
            context,
            base[0],
            base[1],
            base[2],
            context.pure_source_affine[parity],
            context.pure_tags_affine[parity],
        )
        coefficient = cv(label, parity[0], parity[1])
        _add_mod3(lower, acted[0], coefficient)
        _add_mod3(grade, acted[1], coefficient)
        _add_mod3(auxiliary, acted[2], coefficient)
    selected = CHARACTER_LABELS.index(label)
    if any(np.any(lower[index]) for index in range(4) if index != selected):
        raise RuntimeError(f"projector_lower_leak:{label}")
    if label != (0, 0) and np.any(auxiliary):
        raise RuntimeError(f"projector_auxiliary_leak:{label}")
    return lower, grade, auxiliary


def associated_lower_actor(context: Context, row: np.ndarray, label: tuple[int, int], letter: int) -> np.ndarray:
    if row.shape != (LOWER_ECHELON_WIDTH,):
        raise ValueError("lower_actor_shape")
    out = np.zeros_like(row)
    scalar = cv(label, context.actor_source_q1[letter][1], context.actor_source_q1[letter][2])
    for tag, actor in enumerate(context.actor_tags_q1[letter]):
        pmap = context.psl_left_map(actor[0])
        for component in (0, 1):
            block = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
            out[block] = _translated_psl(row[block], pmap, scalar)
    out[SOURCE_BASE_WIDTH:] = row[SOURCE_BASE_WIDTH:]
    return out


def exact_actor_on_old_lift(
    context: Context,
    lower_row: np.ndarray,
    grade_flat: np.ndarray,
    label: tuple[int, int],
    letter: int,
) -> np.ndarray:
    lower = np.zeros((4, SOURCE_BASE_WIDTH), dtype=np.uint8)
    lower[CHARACTER_LABELS.index(label)] = lower_row[:SOURCE_BASE_WIDTH]
    grade = grade_flat.reshape(4, SOURCE_BLOCK_WIDTH)
    _, acted_grade, _ = act_pair(
        context,
        lower,
        grade,
        lower_row[SOURCE_BASE_WIDTH:],
        (context.actor_source_q1[letter][0], context.actor_source_q1[letter][1], context.actor_source_q1[letter][2], context.source_word_value((letter,))[3]),
        context.actor_tags_affine[letter],
    )
    return acted_grade.reshape(SOURCE_TOTAL_WIDTH)


def aggregate_pair(
    context: Context,
    lower: np.ndarray,
    grade: np.ndarray,
    auxiliary: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    physical_lower = np.zeros(PHYSICAL_LOWER_WIDTH, dtype=np.uint8)
    physical_grade = np.zeros(PHYSICAL_GRADE_WIDTH, dtype=np.uint8)
    for source_index, source_label in enumerate(CHARACTER_LABELS):
        for tag, block, sign in context.aggregate_table:
            shift = context.physical_shifts[tag]
            pmap = context.psl_left_map(shift[0])
            target_label = context.transport[tag][source_label]
            target_index = CHARACTER_LABELS.index(target_label)
            scalar = sign * cv(target_label, shift[1], shift[2])
            for component in (0, 1):
                source_lower = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
                destination_lower = slice(
                    physical_lower_coord(target_index, block, component, 0),
                    physical_lower_coord(target_index, block, component, 0) + 504,
                )
                _add_mod3(
                    physical_lower[destination_lower],
                    _translated_psl(lower[source_index, source_lower], pmap, scalar),
                )
                for monomial in range(3):
                    source_grade = slice(
                        grade_coord(tag, component, monomial, 0),
                        grade_coord(tag, component, monomial, 0) + 504,
                    )
                    destination_grade = slice(
                        physical_grade_coord(target_index, block, component, monomial, 0),
                        physical_grade_coord(target_index, block, component, monomial, 0) + 504,
                    )
                    _add_mod3(
                        physical_grade[destination_grade],
                        _translated_psl(grade[source_index, source_grade], pmap, scalar),
                    )
                    kernel_coefficient = shift[3][monomial]
                    if kernel_coefficient:
                        output_label = xor_label(target_label, ETA[monomial])
                        output_index = CHARACTER_LABELS.index(output_label)
                        induced_destination = slice(
                            physical_grade_coord(output_index, block, component, monomial, 0),
                            physical_grade_coord(output_index, block, component, monomial, 0) + 504,
                        )
                        induced_scalar = sign * kernel_coefficient * cv(output_label, shift[1], shift[2])
                        _add_mod3(
                            physical_grade[induced_destination],
                            _translated_psl(lower[source_index, source_lower], pmap, induced_scalar),
                        )
    for tag, block, sign in context.aggregate_table:
        physical_lower[PHYSICAL_LOWER_REGULAR_WIDTH + block] = (
            int(physical_lower[PHYSICAL_LOWER_REGULAR_WIDTH + block]) + sign * int(auxiliary[tag])
        ) % 3
    physical_lower[PHYSICAL_LOWER_REGULAR_WIDTH + 2 :] = auxiliary[6:]
    return physical_lower, physical_grade


def direct_physical_target(context: Context) -> tuple[np.ndarray, np.ndarray]:
    g = context.g760
    h1 = tuple(floor.wm(floor.sub(g, *floor.OO[2]), floor.wi(floor.sub(g, *floor.OO[1])), floor.sub(g, *floor.OO[0])))
    h2 = tuple(floor.wm(floor.sub(g, *floor.OO[5]), floor.wi(floor.sub(g, *floor.OO[4])), floor.wi(floor.sub(g, *floor.OO[3]))))
    if floor.exps(g) != (0, 0) or floor.exps(h1) != (0, 0) or floor.exps(h2) != (0, 0):
        raise RuntimeError("target_normalized_exponent")
    lower = np.zeros(PHYSICAL_LOWER_WIDTH, dtype=np.uint8)
    grade = np.zeros(PHYSICAL_GRADE_WIDTH, dtype=np.uint8)
    for block, word in ((0, h1), (1, h2)):
        normal, augmentation = qnorm_affine(word, context)
        lower[PHYSICAL_LOWER_REGULAR_WIDTH + block] = (-augmentation) % 3
        for component, value, coefficient0 in normal:
            coefficient = (-coefficient0) % 3
            psl = context.psidx[value[0]]
            for character_index, label in enumerate(CHARACTER_LABELS):
                weight = coefficient * cv(label, value[1], value[2])
                li = physical_lower_coord(character_index, block, component, psl)
                lower[li] = (int(lower[li]) + weight) % 3
                for monomial, monomial_coefficient in enumerate(value[3]):
                    if monomial_coefficient:
                        gi = physical_grade_coord(character_index, block, component, monomial, psl)
                        grade[gi] = (int(grade[gi]) + weight * monomial_coefficient) % 3
    return lower, grade


_TRIT_DECODE = np.asarray(
    [[(value // (3**position)) % 3 for position in range(4)] for value in range(81)],
    dtype=np.uint8,
)
_TRIT_ENCODE_WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.uint16)
_PACKED_AXPY = np.zeros((3, 81, 81), dtype=np.uint8)
for _coefficient in (0, 1, 2):
    for _left in range(81):
        for _right in range(81):
            _PACKED_AXPY[_coefficient, _left, _right] = int(
                np.dot(
                    (_TRIT_DECODE[_left].astype(np.int16) - _coefficient * _TRIT_DECODE[_right].astype(np.int16)) % 3,
                    _TRIT_ENCODE_WEIGHTS,
                )
            )
_PACKED_SCALE2 = np.asarray(
    [int(np.dot((2 * _TRIT_DECODE[value]) % 3, _TRIT_ENCODE_WEIGHTS)) for value in range(81)],
    dtype=np.uint8,
)
_PACKED_FIRST = np.asarray(
    [next((position for position, coefficient in enumerate(_TRIT_DECODE[value]) if coefficient), 4) for value in range(81)],
    dtype=np.uint8,
)


def pack_trits(row: np.ndarray) -> np.ndarray:
    flat = np.asarray(row, dtype=np.uint8).reshape(-1)
    if flat.size % 4:
        raise ValueError("packed_width_not_multiple_of_four")
    if np.any(flat > 2):
        raise ValueError("non_trit")
    return np.sum(flat.reshape(-1, 4).astype(np.uint16) * _TRIT_ENCODE_WEIGHTS, axis=1).astype(np.uint8)


def unpack_trits(row: np.ndarray, width: int) -> np.ndarray:
    packed = np.asarray(row, dtype=np.uint8).reshape(-1)
    if packed.size * 4 != width or np.any(packed > 80):
        raise ValueError("packed_row_shape")
    return _TRIT_DECODE[packed].reshape(-1).copy()


def sparse_digest(row: np.ndarray) -> str:
    encoded = [[int(index), int(row[index])] for index in np.flatnonzero(row)]
    return sha256_bytes(json.dumps(encoded, separators=(",", ":")).encode("ascii"))


class PackedEchelon:
    """One base-3-packed echelon owner with bounded dense scratch."""

    def __init__(self, width: int):
        if width % 4:
            raise ValueError("packed_echelon_width")
        self.width = width
        self.packed_width = width // 4
        self.rows: list[np.ndarray] = []
        self.leads: list[int] = []
        self.ordered_pivots: list[int] = []
        self._ordered_keys: list[tuple[int, int]] = []
        self.lead_to_pivot: dict[int, int] = {}

    def pivot_order(self) -> list[int]:
        return self.ordered_pivots

    @staticmethod
    def coefficient(row: np.ndarray, coordinate: int) -> int:
        return int((int(row[coordinate // 4]) // (3 ** (coordinate % 4))) % 3)

    def reduce_packed(self, row: np.ndarray) -> tuple[np.ndarray, list[list[int]]]:
        work = np.asarray(row, dtype=np.uint8).copy()
        if work.shape != (self.packed_width,) or np.any(work > 80):
            raise ValueError("packed_reduce_shape")
        reductions: list[list[int]] = []
        cursor = 0
        while cursor < self.packed_width:
            packed_value = int(work[cursor])
            if packed_value == 0:
                cursor += 1
                continue
            lead = 4 * cursor + int(_PACKED_FIRST[packed_value])
            pivot = self.lead_to_pivot.get(lead)
            if pivot is None:
                break
            coefficient = self.coefficient(work, lead)
            work = _PACKED_AXPY[coefficient, work, self.rows[pivot]]
            reductions.append([pivot, coefficient])
            # Revisit this byte: another nonzero trit can follow the lead.
        return work, reductions

    def _accept_remainder(
        self, remainder: np.ndarray, reductions: list[list[int]]
    ) -> dict[str, Any]:
        """Accept one already reduced packed row without reducing it again."""
        nonzero_bytes = np.flatnonzero(remainder)
        if not len(nonzero_bytes):
            return {"accepted": False, "reductions": reductions}
        byte_index = int(nonzero_bytes[0])
        lead = 4 * byte_index + int(_PACKED_FIRST[int(remainder[byte_index])])
        leading_coefficient = self.coefficient(remainder, lead)
        scale = 1 if leading_coefficient == 1 else 2
        normalized = remainder if scale == 1 else _PACKED_SCALE2[remainder]
        pivot = len(self.rows)
        self.rows.append(normalized.copy())
        self.leads.append(lead)
        position = bisect.bisect_left(self._ordered_keys, (lead, pivot))
        self._ordered_keys.insert(position, (lead, pivot))
        self.ordered_pivots.insert(position, pivot)
        self.lead_to_pivot[lead] = pivot
        return {
            "accepted": True,
            "pivot": pivot,
            "lead": lead,
            "leading_coefficient": leading_coefficient,
            "scale": scale,
            "reductions": reductions,
        }

    def insert(self, row: np.ndarray) -> dict[str, Any]:
        packed = pack_trits(row) if row.shape == (self.width,) else np.asarray(row, dtype=np.uint8)
        remainder, reductions = self.reduce_packed(packed)
        return self._accept_remainder(remainder, reductions)

    def dense_row(self, pivot: int) -> np.ndarray:
        return unpack_trits(self.rows[pivot], self.width)

    def matrix_bytes(self) -> bytes:
        if not self.rows:
            return b""
        return np.stack(self.rows).astype(np.uint8, copy=False).tobytes(order="C")

    @classmethod
    def from_bytes(cls, width: int, rows: int, data: bytes, leads: list[int]) -> "PackedEchelon":
        owner = cls(width)
        expected = rows * owner.packed_width
        if len(data) != expected or len(leads) != rows:
            raise RuntimeError("packed_matrix_size")
        matrix = np.frombuffer(data, dtype=np.uint8).reshape(rows, owner.packed_width)
        if np.any(matrix > 80):
            raise RuntimeError("packed_matrix_byte")
        owner.rows = [matrix[index].copy() for index in range(rows)]
        owner.leads = [int(x) for x in leads]
        owner._ordered_keys = sorted((lead, pivot) for pivot, lead in enumerate(owner.leads))
        owner.ordered_pivots = [pivot for _, pivot in owner._ordered_keys]
        owner.lead_to_pivot = {lead: pivot for pivot, lead in enumerate(owner.leads)}
        if len(owner.lead_to_pivot) != rows:
            raise RuntimeError("packed_matrix_duplicate_lead")
        for index, lead in enumerate(owner.leads):
            if owner.coefficient(owner.rows[index], lead) != 1:
                raise RuntimeError("packed_matrix_pivot")
        return owner

    def separating_dual(self, target: np.ndarray) -> tuple[np.ndarray, int]:
        remainder, _ = self.reduce_packed(pack_trits(target))
        dense_remainder = unpack_trits(remainder, self.width)
        support = np.flatnonzero(dense_remainder)
        if not len(support):
            return np.zeros(self.width, dtype=np.uint8), 0
        witness = int(support[0])
        dual = np.zeros(self.width, dtype=np.uint8)
        dual[witness] = 1
        for pivot in reversed(self.pivot_order()):
            dense = self.dense_row(pivot)
            lead = self.leads[pivot]
            dual[lead] = (-int(np.dot(dense.astype(np.int64), dual.astype(np.int64)))) % 3
        pair = int(np.dot(target.astype(np.int64), dual.astype(np.int64)) % 3)
        if pair == 0:
            raise RuntimeError("dual_zero_pair")
        return dual, pair


def rss_bytes() -> int:
    try:
        import psutil  # type: ignore[import-not-found]

        return int(psutil.Process(os.getpid()).memory_info().rss)
    except Exception:
        pass
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            class Counter(ctypes.Structure):
                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            counter = Counter()
            counter.cb = ctypes.sizeof(counter)
            ctypes.windll.psapi.GetProcessMemoryInfo(
                ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(counter), counter.cb
            )
            return int(counter.WorkingSetSize)
        except Exception:
            return 0
    try:
        import resource

        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        return value if sys.platform == "darwin" else value * 1024
    except Exception:
        return 0


def progress(phase: str, character: int | None, attempts: int, rank: int, queue: int, started: float) -> None:
    print(
        json.dumps(
            {
                "progress": phase,
                "character": character,
                "attempts": attempts,
                "retained_rank": rank,
                "queue_length": queue,
                "elapsed_seconds": time.monotonic() - started,
                "rss_bytes": rss_bytes(),
            },
            sort_keys=True,
        ),
        flush=True,
    )


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        try:
            os.unlink(name)
        except FileNotFoundError:
            pass


def write_blob(state_dir: Path, stem: str, data: bytes, **metadata: Any) -> dict[str, Any]:
    digest = sha256_bytes(data)
    filename = f"{stem}.{digest}.bin"
    _atomic_write(state_dir / filename, data)
    return {"file": filename, "bytes": len(data), "sha256": digest, **metadata}


_AUTHENTICATED_BLOBS: set[tuple[str, int, str, int, int]] = set()


def _plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_blob_receipt(
    state_dir: Path,
    receipt: Any,
    rows: int,
    width: int,
    *,
    authenticate: bool,
    retain: bool = False,
) -> bytes | None:
    """Validate an exact packed receipt with one fixed-chunk SHA pass."""
    required = {"file", "bytes", "sha256", "rows", "width", "encoding"}
    if not isinstance(receipt, dict) or set(receipt) != required:
        raise RuntimeError("blob_receipt_shape")
    filename = receipt["file"]
    if (
        not _plain_int(rows)
        or rows < 0
        or not _plain_int(width)
        or width <= 0
        or width % 4
    ):
        raise RuntimeError("blob_expected_dimensions")
    expected_bytes = rows * (width // 4)
    if (
        not isinstance(filename, str)
        or Path(filename).name != filename
        or not re.fullmatch(r"[A-Za-z0-9_.-]+\.[0-9a-f]{64}\.bin", filename)
        or not isinstance(receipt["sha256"], str)
        or not re.fullmatch(r"[0-9a-f]{64}", receipt["sha256"])
        or not filename.endswith(f".{receipt['sha256']}.bin")
        or receipt["rows"] != rows
        or receipt["width"] != width
        or receipt["encoding"] != "base3-four-trits-per-byte"
        or receipt["bytes"] != expected_bytes
    ):
        raise RuntimeError("blob_receipt_semantics")
    path = state_dir / filename
    stat_before = path.stat()
    if stat_before.st_size != expected_bytes:
        raise RuntimeError(f"blob_size:{filename}")
    key = (
        str(path.resolve()),
        expected_bytes,
        receipt["sha256"],
        stat_before.st_mtime_ns,
        stat_before.st_ino,
    )
    if not authenticate:
        return None
    if key in _AUTHENTICATED_BLOBS:
        if not retain:
            return None
        data = path.read_bytes()
        stat_after = path.stat()
        if (
            len(data) != expected_bytes
            or stat_after.st_mtime_ns != stat_before.st_mtime_ns
            or stat_after.st_ino != stat_before.st_ino
        ):
            raise RuntimeError(f"blob_changed_after_authentication:{filename}")
        return data
    hasher = hashlib.sha256()
    chunks: list[bytes] | None = [] if retain else None
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
            if chunks is not None:
                chunks.append(chunk)
    if hasher.hexdigest() != receipt["sha256"]:
        raise RuntimeError(f"blob_sha256:{filename}")
    stat_after = path.stat()
    if (
        stat_after.st_size != stat_before.st_size
        or stat_after.st_mtime_ns != stat_before.st_mtime_ns
        or stat_after.st_ino != stat_before.st_ino
    ):
        raise RuntimeError(f"blob_changed_during_authentication:{filename}")
    _AUTHENTICATED_BLOBS.add(key)
    return b"".join(chunks) if chunks is not None else None


def read_blob(state_dir: Path, receipt: dict[str, Any]) -> bytes:
    if not isinstance(receipt, dict):
        raise RuntimeError("blob_receipt_shape")
    rows = receipt.get("rows")
    width = receipt.get("width")
    if not _plain_int(rows) or not _plain_int(width):
        raise RuntimeError("blob_receipt_dimensions")
    data = validate_blob_receipt(
        state_dir, receipt, rows, width, authenticate=True, retain=True
    )
    if data is None:
        raise RuntimeError("blob_loader_internal")
    return data


def ensure_external_state_dir(state_dir: Path) -> Path:
    resolved = state_dir.resolve()
    root = ROOT.resolve()
    if resolved == root or root in resolved.parents:
        raise RuntimeError("state_dir_must_be_outside_repository")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


class BlobStreamWriter:
    def __init__(self, state_dir: Path, stem: str):
        self.state_dir = state_dir
        self.stem = stem
        fd, name = tempfile.mkstemp(prefix=stem + ".", suffix=".tmp", dir=state_dir)
        self.name = name
        self.stream = os.fdopen(fd, "wb")
        self.hasher = hashlib.sha256()
        self.size = 0

    def write(self, data: bytes) -> None:
        self.stream.write(data)
        self.hasher.update(data)
        self.size += len(data)

    def finish(self, **metadata: Any) -> dict[str, Any]:
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.stream.close()
        digest = self.hasher.hexdigest()
        filename = f"{self.stem}.{digest}.bin"
        os.replace(self.name, self.state_dir / filename)
        return {"file": filename, "bytes": self.size, "sha256": digest, **metadata}

    def abort(self) -> None:
        try:
            self.stream.close()
        finally:
            try:
                os.unlink(self.name)
            except FileNotFoundError:
                pass


def expression_from_insert(record: dict[str, Any]) -> list[list[int]]:
    expression = [list(pair) for pair in record["reductions"]]
    if record["accepted"]:
        expression.append([int(record["pivot"]), int(record["leading_coefficient"])])
    return expression


def enforce_resource(started: float, seconds: float, max_rss: int, phase: str) -> None:
    if time.monotonic() - started > seconds:
        raise RuntimeError(f"UNKNOWN_RESOURCE:{phase}:time_cap")
    current = rss_bytes()
    if current and current > max_rss:
        raise RuntimeError(f"UNKNOWN_RESOURCE:{phase}:rss_cap:{current}")


def close_lower_block(
    context: Context,
    label: tuple[int, int],
    seed_rows: list[np.ndarray],
    started: float,
    seconds_cap: float,
    rss_cap: int,
) -> tuple[PackedEchelon, dict[str, Any]]:
    owner = PackedEchelon(LOWER_ECHELON_WIDTH)
    nodes: list[dict[str, Any]] = []
    seed_reductions: list[list[list[int]]] = []
    transitions: list[list[list[list[int]] | None]] = []
    queue: deque[int] = deque()
    attempts = 0
    last_report = time.monotonic()
    for seed, row in enumerate(seed_rows, 1):
        inserted = owner.insert(row)
        attempts += 1
        seed_reductions.append(expression_from_insert(inserted))
        if inserted["accepted"]:
            pivot = int(inserted["pivot"])
            nodes.append(
                {
                    "pivot": pivot,
                    "lead": int(inserted["lead"]),
                    "scale": int(inserted["scale"]),
                    "origin": {"kind": "projected_seed", "seed": seed},
                    "reductions": inserted["reductions"],
                }
            )
            transitions.append([None, None, None, None])
            queue.append(pivot)
    while queue:
        pivot = queue.popleft()
        parent = owner.dense_row(pivot)
        for actor_index, letter in enumerate(ACTORS):
            child = associated_lower_actor(context, parent, label, letter)
            inserted = owner.insert(child)
            attempts += 1
            transitions[pivot][actor_index] = expression_from_insert(inserted)
            if inserted["accepted"]:
                new_pivot = int(inserted["pivot"])
                nodes.append(
                    {
                        "pivot": new_pivot,
                        "lead": int(inserted["lead"]),
                        "scale": int(inserted["scale"]),
                        "origin": {"kind": "actor", "parent": pivot, "letter": letter},
                        "reductions": inserted["reductions"],
                    }
                )
                transitions.append([None, None, None, None])
                queue.append(new_pivot)
            now = time.monotonic()
            if attempts % 256 == 0 or now - last_report >= 30:
                progress("prepare-lower", CHARACTER_LABELS.index(label), attempts, len(owner.rows), len(queue), started)
                last_report = now
            enforce_resource(started, seconds_cap, rss_cap, "prepare-lower")
    if any(any(value is None for value in row) for row in transitions):
        raise RuntimeError("lower_transition_incomplete")
    if attempts != 44 + 4 * len(owner.rows):
        raise RuntimeError("lower_queue_receipt")
    record = {
        "character": list(label),
        "rank": len(owner.rows),
        "attempts": attempts,
        "seed_reductions": seed_reductions,
        "actor_order": list(ACTORS),
        "actor_transitions": transitions,
        "dag_nodes": nodes,
        "queue_exhausted": True,
    }
    return owner, record


def evaluate_old_lifts(
    context: Context,
    label: tuple[int, int],
    owner: PackedEchelon,
    record: dict[str, Any],
    projected_grades: list[np.ndarray],
    started: float,
    seconds_cap: float,
    rss_cap: int,
) -> np.ndarray:
    matrix = np.zeros((len(owner.rows), SOURCE_TOTAL_WIDTH), dtype=np.uint8)
    for pivot, node in enumerate(record["dag_nodes"]):
        if int(node["pivot"]) != pivot:
            raise RuntimeError("old_dag_order")
        origin = node["origin"]
        if origin["kind"] == "projected_seed":
            work = projected_grades[int(origin["seed"]) - 1].copy()
        elif origin["kind"] == "actor":
            parent = int(origin["parent"])
            if parent >= pivot:
                raise RuntimeError("old_dag_cycle")
            work = exact_actor_on_old_lift(
                context, owner.dense_row(parent), matrix[parent], label, int(origin["letter"])
            )
        else:
            raise RuntimeError("old_dag_origin")
        for earlier, coefficient in node["reductions"]:
            if int(earlier) >= pivot:
                raise RuntimeError("old_dag_reduction_order")
            _add_mod3(work, matrix[int(earlier)], -int(coefficient))
        if int(node["scale"]) == 2:
            work[:] = (2 * work.astype(np.uint16)) % 3
        matrix[pivot] = work
        if (pivot + 1) % 256 == 0:
            progress("prepare-lifts", CHARACTER_LABELS.index(label), pivot + 1, pivot + 1, 0, started)
        enforce_resource(started, seconds_cap, rss_cap, "prepare-lifts")
    return matrix


def associated_grade_actor(context: Context, row: np.ndarray, label: tuple[int, int], letter: int) -> np.ndarray:
    if row.shape != (SOURCE_BLOCK_WIDTH,):
        raise ValueError("grade_actor_shape")
    out = np.zeros_like(row)
    scalar = cv(label, context.actor_source_q1[letter][1], context.actor_source_q1[letter][2])
    for tag, actor in enumerate(context.actor_tags_q1[letter]):
        pmap = context.psl_left_map(actor[0])
        for component in (0, 1):
            for monomial in range(3):
                block = slice(
                    grade_coord(tag, component, monomial, 0),
                    grade_coord(tag, component, monomial, 0) + 504,
                )
                out[block] = _translated_psl(row[block], pmap, scalar)
    return out


def project_pure_grade_by_words(context: Context, grade: np.ndarray, label: tuple[int, int]) -> np.ndarray:
    if grade.shape != (4, SOURCE_BLOCK_WIDTH):
        raise ValueError("pure_grade_project_shape")
    output = np.zeros_like(grade)
    zero_lower = np.zeros((4, SOURCE_BASE_WIDTH), dtype=np.uint8)
    zero_auxiliary = np.zeros(LOWER_AUX_WIDTH, dtype=np.uint8)
    for parity in CHARACTER_LABELS:
        _, acted, _ = act_pair(
            context,
            zero_lower,
            grade,
            zero_auxiliary,
            context.pure_source_affine[parity],
            context.pure_tags_affine[parity],
        )
        _add_mod3(output, acted, cv(label, parity[0], parity[1]))
    return output


def run_block_core(
    state_dir: Path,
    prepare: dict[str, Any],
    prepare_digest: str,
    block: int,
    started: float,
) -> tuple[dict[str, Any], str]:
    label = CHARACTER_LABELS[block]
    context = context_for_state(prepare)
    packet = prepare["packets"][block]
    data = read_blob(state_dir, packet["blob"])
    rows = int(packet["blob"]["rows"])
    packed_width = SOURCE_BLOCK_WIDTH // 4
    if len(data) != rows * packed_width or rows != len(prepare["defect_origins"]):
        raise RuntimeError("packet_shape")
    matrix = np.frombuffer(data, dtype=np.uint8).reshape(rows, packed_width)
    owner = PackedEchelon(SOURCE_BLOCK_WIDTH)
    dag_nodes: list[dict[str, Any]] = []
    origin_reductions: list[list[list[int]]] = []
    transitions: list[list[list[list[int]] | None]] = []
    queue: deque[int] = deque()
    attempts = 0
    last_report = time.monotonic()
    cap_seconds = float(os.environ.get("TASK554_BLOCK_SECONDS", "21600"))
    cap_rss = int(os.environ.get("TASK554_MAX_RSS", str(8 * 1024**3)))
    for origin, packed in enumerate(matrix):
        inserted = owner.insert(packed)
        attempts += 1
        origin_reductions.append(expression_from_insert(inserted))
        if inserted["accepted"]:
            pivot = int(inserted["pivot"])
            dag_nodes.append(
                {
                    "pivot": pivot,
                    "lead": int(inserted["lead"]),
                    "scale": int(inserted["scale"]),
                    "origin": {"kind": "defect", "origin": origin},
                    "reductions": inserted["reductions"],
                }
            )
            transitions.append([None, None, None, None])
            queue.append(pivot)
        now = time.monotonic()
        if attempts % 256 == 0 or now - last_report >= 30:
            progress("block-ingest", block, attempts, len(owner.rows), len(queue), started)
            last_report = now
        enforce_resource(started, cap_seconds, cap_rss, f"block-{block}-ingest")
    enforce_resource(started, cap_seconds, cap_rss, f"block-{block}-ingest")
    while queue:
        pivot = queue.popleft()
        parent = owner.dense_row(pivot)
        for actor_index, letter in enumerate(ACTORS):
            child = associated_grade_actor(context, parent, label, letter)
            inserted = owner.insert(child)
            attempts += 1
            transitions[pivot][actor_index] = expression_from_insert(inserted)
            if inserted["accepted"]:
                new_pivot = int(inserted["pivot"])
                dag_nodes.append(
                    {
                        "pivot": new_pivot,
                        "lead": int(inserted["lead"]),
                        "scale": int(inserted["scale"]),
                        "origin": {"kind": "actor", "parent": pivot, "letter": letter},
                        "reductions": inserted["reductions"],
                    }
                )
                transitions.append([None, None, None, None])
                queue.append(new_pivot)
            now = time.monotonic()
            if attempts % 256 == 0 or now - last_report >= 30:
                progress("block", block, attempts, len(owner.rows), len(queue), started)
                last_report = now
            enforce_resource(started, cap_seconds, cap_rss, f"block-{block}")
    if any(any(value is None for value in row) for row in transitions):
        raise RuntimeError("block_transition_incomplete")
    if attempts != rows + 4 * len(owner.rows):
        raise RuntimeError("block_queue_receipt")
    basis_blob = write_blob(
        state_dir,
        f"block-{block}-basis",
        owner.matrix_bytes(),
        rows=len(owner.rows),
        width=SOURCE_BLOCK_WIDTH,
        encoding="base3-four-trits-per-byte",
    )
    body = {
        "schema": STATE_SCHEMA,
        "phase": "block",
        "fixture": bool(prepare.get("fixture", False)),
        "parent_sha256": prepare_digest,
        "character_index": block,
        "character": list(label),
        "dimensions": {"width": SOURCE_BLOCK_WIDTH, "monomials_coupled": 3},
        "packet_sha256": packet["blob"]["sha256"],
        "origin_count": rows,
        "origin_reductions": origin_reductions,
        "rank": len(owner.rows),
        "attempts": attempts,
        "queue_exhausted": True,
        "pivot_leads": owner.leads,
        "basis_blob": basis_blob,
        "dag_nodes": dag_nodes,
        "dag_sha256": sha256_bytes(canonical_json(dag_nodes)),
        "actor_order": list(ACTORS),
        "actor_transitions": transitions,
        "elapsed_seconds": time.monotonic() - started,
        "peak_owner_bytes": len(owner.rows) * owner.packed_width,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(state_dir, f"block-{block}", body, prepare_digest)
    return body, digest


_CONTEXT_CACHE: tuple[str, Context] | None = None


def context_for_state(prepare: dict[str, Any]) -> Context:
    global _CONTEXT_CACHE
    key = prepare["input_manifest_sha256"]
    if _CONTEXT_CACHE is None or _CONTEXT_CACHE[0] != key:
        words = json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8"))
        _CONTEXT_CACHE = key, Context(words)
    return _CONTEXT_CACHE[1]


def false_claim_flags() -> dict[str, bool]:
    return {
        "ORDER_54432": False,
        "FULL_Q0": False,
        "A0": False,
        "COMMON": False,
        "COMPATIBLE_LIFT": False,
        "FAKE": False,
        "IHARA": False,
        "verified": False,
    }


def aggregate_pure_grade(context: Context, block: int, row: np.ndarray) -> np.ndarray:
    lower = np.zeros((4, SOURCE_BASE_WIDTH), dtype=np.uint8)
    grade = np.zeros((4, SOURCE_BLOCK_WIDTH), dtype=np.uint8)
    grade[block] = row
    _, physical = aggregate_pair(context, lower, grade, np.zeros(LOWER_AUX_WIDTH, dtype=np.uint8))
    return physical


def write_fixture_prepare(state_dir: Path) -> tuple[dict[str, Any], str]:
    _, input_receipt = load_pinned_inputs()
    input_digest = sha256_bytes(canonical_json(input_receipt))
    context = Context(json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8")))
    origins = [{"id": 0, "kind": "fixture-coupled-origin"}]
    packets = []
    residual = np.zeros(PHYSICAL_GRADE_WIDTH, dtype=np.uint8)
    for block in range(4):
        row = np.zeros(SOURCE_BLOCK_WIDTH, dtype=np.uint8)
        for psl in range(504):
            row[grade_coord(0, 0, 0, psl)] = 1
            row[grade_coord(0, 0, 1, psl)] = 1
        blob = write_blob(
            state_dir,
            f"fixture-packet-{block}",
            pack_trits(row).tobytes(),
            rows=1,
            width=SOURCE_BLOCK_WIDTH,
            encoding="base3-four-trits-per-byte",
        )
        packets.append({"character": list(CHARACTER_LABELS[block]), "blob": blob, "origin_count": 1})
        _add_mod3(residual, aggregate_pure_grade(context, block, row))
    residual_blob = write_blob(
        state_dir,
        "fixture-residual",
        pack_trits(residual).tobytes(),
        rows=1,
        width=PHYSICAL_GRADE_WIDTH,
        encoding="base3-four-trits-per-byte",
    )
    body = {
        "schema": STATE_SCHEMA,
        "phase": "prepare",
        "fixture": True,
        "input_manifest": input_receipt,
        "input_manifest_sha256": input_digest,
        "dimensions": fixed_dimensions(),
        "canonical_solution": {"raw_terms": 0, "canonical_terms": 0, "fixture": True},
        "old_blocks": [],
        "defect_origins": origins,
        "defect_origin_sha256": sha256_bytes(canonical_json(origins)),
        "packets": packets,
        "residual_blob": residual_blob,
        "residual_support": int(np.count_nonzero(residual)),
        "residual_sha256": sparse_digest(residual),
        "paired_lower_presentation_complete": True,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(state_dir, "prepare", body, None)
    return body, digest


def fixed_dimensions() -> dict[str, Any]:
    return {
        "characters": 4,
        "character_labels": [list(x) for x in CHARACTER_LABELS],
        "monomials": [list(x) for x in MONOMIALS_GRADE1],
        "monomials_coupled": True,
        "source_base": SOURCE_BASE_WIDTH,
        "source_per_character": SOURCE_BLOCK_WIDTH,
        "source_total": SOURCE_TOTAL_WIDTH,
        "physical_grade": PHYSICAL_GRADE_WIDTH,
        "physical_lower_regular": PHYSICAL_LOWER_REGULAR_WIDTH,
        "physical_lower_with_auxiliary": PHYSICAL_LOWER_WIDTH,
    }


def _validate_expression(
    expression: Any, rank: int, gate: str, *, earlier_than: int | None = None
) -> None:
    if not isinstance(expression, list):
        raise RuntimeError(f"{gate}:shape")
    bound = rank if earlier_than is None else earlier_than
    for pair in expression:
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or not _plain_int(pair[0])
            or pair[0] < 0
            or pair[0] >= bound
            or not _plain_int(pair[1])
            or pair[1] not in (1, 2)
        ):
            raise RuntimeError(f"{gate}:entry")


def _validate_input_binding(body: dict[str, Any], receipt: dict[str, dict[str, Any]]) -> None:
    if (
        body.get("input_manifest") != receipt
        or body.get("input_manifest_sha256") != sha256_bytes(canonical_json(receipt))
        or body.get("dimensions") != fixed_dimensions()
    ):
        raise RuntimeError("state_input_binding")


def validate_prepare_state(
    state_dir: Path,
    body: dict[str, Any],
    receipt: dict[str, dict[str, Any]],
    *,
    fixture: bool,
    authenticate_residual: bool = False,
    authenticate_old: bool = False,
    authenticate_packets: Iterable[int] = (),
) -> None:
    if body.get("phase") != "prepare" or body.get("fixture") is not fixture:
        raise RuntimeError("prepare_state_semantics")
    _validate_input_binding(body, receipt)
    if body.get("paired_lower_presentation_complete") is not True:
        raise RuntimeError("prepare_presentation_incomplete")
    validate_blob_receipt(
        state_dir,
        body.get("residual_blob"),
        1,
        PHYSICAL_GRADE_WIDTH,
        authenticate=authenticate_residual,
    )
    origins = body.get("defect_origins")
    old_blocks = body.get("old_blocks")
    packets = body.get("packets")
    if not isinstance(origins, list) or not isinstance(old_blocks, list) or not isinstance(packets, list):
        raise RuntimeError("prepare_roster_shape")
    if sha256_bytes(canonical_json(origins)) != body.get("defect_origin_sha256"):
        raise RuntimeError("prepare_origin_digest")
    if len(old_blocks) != (0 if fixture else 4) or len(packets) != 4:
        raise RuntimeError("prepare_roster_count")
    expected_origins = 1 if fixture else 0
    cursor = 0
    for character_index, old in enumerate(old_blocks):
        if (
            not isinstance(old, dict)
            or old.get("character_index") != character_index
            or old.get("character") != list(CHARACTER_LABELS[character_index])
            or not _plain_int(old.get("rank"))
            or old["rank"] < 0
        ):
            raise RuntimeError("prepare_old_metadata")
        rank = old["rank"]
        record = old.get("record")
        if (
            not isinstance(record, dict)
            or record.get("character") != list(CHARACTER_LABELS[character_index])
            or record.get("rank") != rank
            or record.get("attempts") != 44 + 4 * rank
            or record.get("actor_order") != list(ACTORS)
            or record.get("queue_exhausted") is not True
            or not isinstance(record.get("seed_reductions"), list)
            or len(record["seed_reductions"]) != 44
            or not isinstance(record.get("actor_transitions"), list)
            or len(record["actor_transitions"]) != rank
            or any(not isinstance(row, list) or len(row) != 4 for row in record["actor_transitions"])
            or not isinstance(record.get("dag_nodes"), list)
            or len(record["dag_nodes"]) != rank
        ):
            raise RuntimeError("prepare_old_record")
        for expression in record["seed_reductions"]:
            _validate_expression(expression, rank, "prepare_seed_reduction")
        for row in record["actor_transitions"]:
            for expression in row:
                _validate_expression(expression, rank, "prepare_actor_transition")
        for pivot, node in enumerate(record["dag_nodes"]):
            if (
                not isinstance(node, dict)
                or node.get("pivot") != pivot
                or not _plain_int(node.get("lead"))
                or not 0 <= node["lead"] < LOWER_ECHELON_WIDTH
                or node.get("scale") not in (1, 2)
            ):
                raise RuntimeError("prepare_old_dag")
            _validate_expression(
                node.get("reductions"), rank, "prepare_old_dag_reduction", earlier_than=pivot
            )
        validate_blob_receipt(
            state_dir,
            old.get("lower_basis_blob"),
            rank,
            LOWER_ECHELON_WIDTH,
            authenticate=authenticate_old,
        )
        validate_blob_receipt(
            state_dir,
            old.get("lifted_grade_blob"),
            rank,
            SOURCE_TOTAL_WIDTH,
            authenticate=authenticate_old,
        )
        expected_end = cursor + 44 + 4 * rank
        if old.get("defect_origin_range") != [cursor, expected_end]:
            raise RuntimeError("prepare_origin_range")
        cursor = expected_end
        expected_origins += 44 + 4 * rank
    if len(origins) != expected_origins:
        raise RuntimeError("prepare_origin_cardinality")
    for index, origin in enumerate(origins):
        if not isinstance(origin, dict) or origin.get("id") != index:
            raise RuntimeError("prepare_origin_identity")
    authenticate_set = set(authenticate_packets)
    if not authenticate_set.issubset(set(range(4))):
        raise RuntimeError("prepare_packet_selection")
    for packet_index, packet in enumerate(packets):
        if (
            not isinstance(packet, dict)
            or packet.get("character") != list(CHARACTER_LABELS[packet_index])
            or packet.get("origin_count") != len(origins)
        ):
            raise RuntimeError("prepare_packet_metadata")
        if not fixture and packet.get("origin_sha256") != body.get("defect_origin_sha256"):
            raise RuntimeError("prepare_packet_origin_digest")
        validate_blob_receipt(
            state_dir,
            packet.get("blob"),
            len(origins),
            SOURCE_BLOCK_WIDTH,
            authenticate=packet_index in authenticate_set,
        )


def validate_block_state(
    state_dir: Path,
    body: dict[str, Any],
    prepare: dict[str, Any],
    prepare_digest: str,
    block: int,
    *,
    authenticate_basis: bool,
) -> None:
    rank = body.get("rank")
    origin_count = body.get("origin_count")
    if (
        body.get("phase") != "block"
        or body.get("fixture") is not bool(prepare.get("fixture"))
        or body.get("parent_sha256") != prepare_digest
        or body.get("character_index") != block
        or body.get("character") != list(CHARACTER_LABELS[block])
        or body.get("dimensions") != {"width": SOURCE_BLOCK_WIDTH, "monomials_coupled": 3}
        or body.get("packet_sha256") != prepare["packets"][block]["blob"]["sha256"]
        or not _plain_int(origin_count)
        or origin_count != len(prepare["defect_origins"])
        or not _plain_int(rank)
        or rank < 0
        or body.get("attempts") != origin_count + 4 * rank
        or body.get("queue_exhausted") is not True
        or body.get("actor_order") != list(ACTORS)
    ):
        raise RuntimeError("block_state_semantics")
    origins = body.get("origin_reductions")
    transitions = body.get("actor_transitions")
    nodes = body.get("dag_nodes")
    leads = body.get("pivot_leads")
    if (
        not isinstance(origins, list)
        or len(origins) != origin_count
        or not isinstance(transitions, list)
        or len(transitions) != rank
        or any(not isinstance(row, list) or len(row) != 4 for row in transitions)
        or not isinstance(nodes, list)
        or len(nodes) != rank
        or not isinstance(leads, list)
        or len(leads) != rank
        or len(set(leads)) != rank
    ):
        raise RuntimeError("block_state_cardinality")
    for expression in origins:
        _validate_expression(expression, rank, "block_origin_reduction")
    for row in transitions:
        for expression in row:
            _validate_expression(expression, rank, "block_actor_transition")
    for pivot, node in enumerate(nodes):
        if (
            not isinstance(node, dict)
            or node.get("pivot") != pivot
            or node.get("lead") != leads[pivot]
            or not _plain_int(leads[pivot])
            or not 0 <= leads[pivot] < SOURCE_BLOCK_WIDTH
            or node.get("scale") not in (1, 2)
        ):
            raise RuntimeError("block_dag_node")
        _validate_expression(
            node.get("reductions"), rank, "block_dag_reduction", earlier_than=pivot
        )
    if sha256_bytes(canonical_json(nodes)) != body.get("dag_sha256"):
        raise RuntimeError("block_dag_digest")
    validate_blob_receipt(
        state_dir,
        body.get("basis_blob"),
        rank,
        SOURCE_BLOCK_WIDTH,
        authenticate=authenticate_basis,
    )


def validate_merge_state(
    state_dir: Path,
    body: dict[str, Any],
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    *,
    authenticate_basis: bool,
) -> None:
    block_digests = [digest for _, digest in blocks]
    fixture = bool(prepare.get("fixture"))
    terminals = (
        {"FIXTURE_MEMBER", "FIXTURE_NONMEMBER"}
        if fixture
        else {"MEMBER", "NONMEMBER", "FIRST_RUNG_GRADE1_MEMBER", "FIRST_RUNG_GRADE1_NONMEMBER"}
    )
    lower_rank = body.get("physical_lower_rank")
    grade_rank = body.get("physical_grade_rank")
    roster = body.get("physical_roster")
    if (
        body.get("phase") != "merge"
        or body.get("fixture") is not fixture
        or body.get("parent_sha256") != prepare_digest
        or body.get("block_sha256") != block_digests
        or body.get("dimensions") != fixed_dimensions()
        or body.get("source_blocks_exhausted") != 4
        or body.get("terminal") not in terminals
        or not _plain_int(lower_rank)
        or lower_rank < 0
        or not _plain_int(grade_rank)
        or grade_rank < 0
        or not isinstance(roster, list)
        or len(roster)
        != sum(old["rank"] for old in prepare["old_blocks"])
        + sum(block[0]["rank"] for block in blocks)
    ):
        raise RuntimeError("merge_state_semantics")
    if sha256_bytes(canonical_json(roster)) != body.get("physical_roster_sha256"):
        raise RuntimeError("merge_roster_digest")
    presentation = body.get("transition_presentation")
    if not isinstance(presentation, dict) or presentation.get("complete") is not True:
        raise RuntimeError("merge_transition_presentation")
    presentation_without_digest = dict(presentation)
    presentation_digest = presentation_without_digest.pop("sha256", None)
    if sha256_bytes(canonical_json(presentation_without_digest)) != presentation_digest:
        raise RuntimeError("merge_transition_digest")
    if body.get("downstream_claim_flags") != false_claim_flags():
        raise RuntimeError("merge_claim_boundary")
    lower_nodes = body.get("physical_lower_dag")
    grade_nodes = body.get("physical_grade_dag")
    leads = body.get("physical_grade_pivot_leads")
    if (
        not isinstance(lower_nodes, list)
        or len(lower_nodes) != lower_rank
        or not isinstance(grade_nodes, list)
        or len(grade_nodes) != grade_rank
        or not isinstance(leads, list)
        or len(leads) != grade_rank
        or len(set(leads)) != grade_rank
    ):
        raise RuntimeError("merge_dag_cardinality")
    for pivot, node in enumerate(lower_nodes):
        if not isinstance(node, dict) or node.get("pivot") != pivot or node.get("scale") not in (1, 2):
            raise RuntimeError("merge_lower_dag")
        _validate_expression(
            node.get("reductions"), lower_rank, "merge_lower_reduction", earlier_than=pivot
        )
    for pivot, node in enumerate(grade_nodes):
        if (
            not isinstance(node, dict)
            or node.get("pivot") != pivot
            or node.get("lead") != leads[pivot]
            or not _plain_int(leads[pivot])
            or not 0 <= leads[pivot] < PHYSICAL_GRADE_WIDTH
            or node.get("scale") not in (1, 2)
        ):
            raise RuntimeError("merge_grade_dag")
        _validate_expression(
            node.get("reductions"), grade_rank, "merge_grade_reduction", earlier_than=pivot
        )
    validate_blob_receipt(
        state_dir,
        body.get("physical_grade_basis_blob"),
        grade_rank,
        PHYSICAL_GRADE_WIDTH,
        authenticate=authenticate_basis,
    )
    if body["terminal"] in (
        "FIRST_RUNG_GRADE1_MEMBER",
        "FIRST_RUNG_GRADE1_NONMEMBER",
    ):
        if (
            not isinstance(body.get("provisional_merge_sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", body["provisional_merge_sha256"])
            or not isinstance(body.get("source_ancestry"), dict)
        ):
            raise RuntimeError("merge_final_fields")
        if body["terminal"] == "FIRST_RUNG_GRADE1_MEMBER":
            next_residual = body.get("next_degree2_residual")
            degree2_width = 4 * 2 * 2 * 6 * 504
            if (
                not isinstance(next_residual, dict)
                or next_residual.get("grade") != 2
                or next_residual.get("width") != degree2_width
            ):
                raise RuntimeError("merge_degree2_receipt")
            validate_blob_receipt(
                state_dir,
                next_residual.get("blob"),
                1,
                degree2_width,
                authenticate=authenticate_basis,
            )
        elif body.get("next_degree2_residual") is not None:
            raise RuntimeError("merge_nonmember_degree2")


def load_block_owner(state_dir: Path, block_body: dict[str, Any]) -> PackedEchelon:
    receipt = block_body["basis_blob"]
    return PackedEchelon.from_bytes(
        int(receipt["width"]), int(receipt["rows"]), read_blob(state_dir, receipt), block_body["pivot_leads"]
    )


def run_merge_core(
    state_dir: Path,
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    started: float,
) -> tuple[dict[str, Any], str]:
    context = context_for_state(prepare)
    for index, (body, digest) in enumerate(blocks):
        if body.get("character_index") != index or body.get("parent_sha256") != prepare_digest:
            raise RuntimeError("merge_block_parent")
        if not body.get("queue_exhausted"):
            raise RuntimeError("merge_unexhausted_block")
        if digest != sha256_bytes(canonical_json(body)):
            # State bodies are newline-canonical, so this equality binds the
            # value independently of its filename receipt.
            raise RuntimeError("merge_block_digest")
    grade_owner = PackedEchelon(PHYSICAL_GRADE_WIDTH)
    grade_nodes: list[dict[str, Any]] = []
    physical_roster: list[dict[str, Any]] = []
    lower_owner = PackedEchelon(PHYSICAL_LOWER_WIDTH)
    lower_grade_rows: list[np.ndarray] = []
    lower_nodes: list[dict[str, Any]] = []
    attempts = 0
    cap_seconds = float(os.environ.get("TASK554_MERGE_SECONDS", "21600"))
    cap_rss = int(os.environ.get("TASK554_MAX_RSS", str(8 * 1024**3)))
    # Production old lifts are processed lower-first.  The fixture has an
    # empty old roster but traverses the identical defect/target path.
    for old_block in prepare.get("old_blocks", []):
        char_index = int(old_block["character_index"])
        lower_receipt = old_block["lower_basis_blob"]
        lift_receipt = old_block["lifted_grade_blob"]
        lower_data = read_blob(state_dir, lower_receipt)
        lift_data = read_blob(state_dir, lift_receipt)
        rank = int(lower_receipt["rows"])
        lower_matrix = np.frombuffer(lower_data, dtype=np.uint8).reshape(rank, LOWER_ECHELON_WIDTH // 4)
        lift_matrix = np.frombuffer(lift_data, dtype=np.uint8).reshape(rank, SOURCE_TOTAL_WIDTH // 4)
        for pivot in range(rank):
            lower_row = unpack_trits(lower_matrix[pivot], LOWER_ECHELON_WIDTH)
            occurrence_lower = np.zeros((4, SOURCE_BASE_WIDTH), dtype=np.uint8)
            occurrence_lower[char_index] = lower_row[:SOURCE_BASE_WIDTH]
            occurrence_grade = unpack_trits(lift_matrix[pivot], SOURCE_TOTAL_WIDTH).reshape(4, SOURCE_BLOCK_WIDTH)
            physical_lower, physical_grade = aggregate_pair(
                context, occurrence_lower, occurrence_grade, lower_row[SOURCE_BASE_WIDTH:]
            )
            remainder, reductions = lower_owner.reduce_packed(pack_trits(physical_lower))
            grade_remainder = physical_grade.copy()
            for earlier, coefficient in reductions:
                _add_mod3(grade_remainder, lower_grade_rows[int(earlier)], -int(coefficient))
            dense_lower_remainder = unpack_trits(remainder, PHYSICAL_LOWER_WIDTH)
            if np.any(dense_lower_remainder):
                inserted = lower_owner._accept_remainder(remainder, reductions)
                if not inserted["accepted"] or inserted["reductions"] != reductions:
                    raise RuntimeError("lower_first_insert_disagreement")
                scale = int(inserted["scale"])
                if scale == 2:
                    grade_remainder[:] = (2 * grade_remainder.astype(np.uint16)) % 3
                lower_grade_rows.append(grade_remainder)
                lower_nodes.append(
                    {
                        "pivot": int(inserted["pivot"]),
                        "scale": scale,
                        "origin": {"kind": "old_basis", "character": char_index, "pivot": pivot},
                        "reductions": reductions,
                    }
                )
                physical_roster.append({"kind": "old-lower-pivot", "character": char_index, "pivot": pivot})
            else:
                inserted_grade = grade_owner.insert(grade_remainder)
                physical_roster.append({"kind": "old-connection", "character": char_index, "pivot": pivot})
                if inserted_grade["accepted"]:
                    grade_nodes.append(
                        {
                            "pivot": int(inserted_grade["pivot"]),
                            "lead": int(inserted_grade["lead"]),
                            "scale": int(inserted_grade["scale"]),
                            "origin": {
                                "kind": "old_connection",
                                "character": char_index,
                                "pivot": pivot,
                                "lower_reductions": reductions,
                            },
                            "reductions": inserted_grade["reductions"],
                        }
                    )
            attempts += 1
            enforce_resource(started, cap_seconds, cap_rss, "merge-old")
    for block, (block_body, _) in enumerate(blocks):
        owner = load_block_owner(state_dir, block_body)
        for pivot in range(len(owner.rows)):
            physical = aggregate_pure_grade(context, block, owner.dense_row(pivot))
            inserted = grade_owner.insert(physical)
            physical_roster.append({"kind": "coupled-defect", "character": block, "pivot": pivot})
            if inserted["accepted"]:
                grade_nodes.append(
                    {
                        "pivot": int(inserted["pivot"]),
                        "lead": int(inserted["lead"]),
                        "scale": int(inserted["scale"]),
                        "origin": {"kind": "block_basis", "character": block, "pivot": pivot},
                        "reductions": inserted["reductions"],
                    }
                )
            attempts += 1
            if attempts % 256 == 0:
                progress("merge-fibre", block, attempts, len(grade_owner.rows), 0, started)
            enforce_resource(started, cap_seconds, cap_rss, "merge-fibre")
    residual_receipt = prepare["residual_blob"]
    residual_data = read_blob(state_dir, residual_receipt)
    if len(residual_data) != PHYSICAL_GRADE_WIDTH // 4:
        raise RuntimeError("residual_blob_shape")
    residual = unpack_trits(np.frombuffer(residual_data, dtype=np.uint8), PHYSICAL_GRADE_WIDTH)
    remainder, member_coefficients = grade_owner.reduce_packed(pack_trits(residual))
    member = not np.any(remainder)
    dual = np.zeros(PHYSICAL_GRADE_WIDTH, dtype=np.uint8)
    dual_pair = 0
    if not member:
        dual, dual_pair = grade_owner.separating_dual(residual)
        for basis in grade_owner.rows:
            if int(np.dot(unpack_trits(basis, PHYSICAL_GRADE_WIDTH).astype(np.int64), dual.astype(np.int64)) % 3):
                raise RuntimeError("dual_annihilation")
    terminal = "FIXTURE_MEMBER" if prepare.get("fixture") and member else "FIXTURE_NONMEMBER" if prepare.get("fixture") else "MEMBER" if member else "NONMEMBER"
    basis_blob = write_blob(
        state_dir,
        "physical-grade-basis",
        grade_owner.matrix_bytes(),
        rows=len(grade_owner.rows),
        width=PHYSICAL_GRADE_WIDTH,
        encoding="base3-four-trits-per-byte",
    )
    body = {
        "schema": STATE_SCHEMA,
        "phase": "merge",
        "fixture": bool(prepare.get("fixture")),
        "parent_sha256": prepare_digest,
        "block_sha256": [digest for _, digest in blocks],
        "dimensions": fixed_dimensions(),
        "source_blocks_exhausted": 4,
        "physical_roster": physical_roster,
        "physical_roster_sha256": sha256_bytes(canonical_json(physical_roster)),
        "physical_lower_rank": len(lower_owner.rows),
        "physical_grade_rank": len(grade_owner.rows),
        "physical_grade_basis_blob": basis_blob,
        "physical_grade_pivot_leads": grade_owner.leads,
        "physical_lower_dag": lower_nodes,
        "physical_grade_dag": grade_nodes,
        "member_coefficients": member_coefficients if member else [],
        "remainder_sha256": sha256_bytes(remainder.tobytes()),
        "remainder_support": int(np.count_nonzero(unpack_trits(remainder, PHYSICAL_GRADE_WIDTH))),
        "dual": [[int(i), int(dual[i])] for i in np.flatnonzero(dual)],
        "dual_pair": dual_pair,
        "transition_presentation": build_transition_presentation(prepare, blocks),
        "terminal": terminal,
        "elapsed_seconds": time.monotonic() - started,
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(state_dir, "merge", body, prepare_digest)
    return body, digest


def build_transition_presentation(
    prepare: dict[str, Any], blocks: list[tuple[dict[str, Any], str]]
) -> dict[str, Any]:
    presentation = {
        "schema": STATE_SCHEMA + ".transition-presentation",
        "grade": 1,
        "old_blocks": [],
        "new_blocks": [],
        "seed_count": 44 if not prepare.get("fixture") else 0,
        "complete": True,
    }
    for old in prepare.get("old_blocks", []):
        presentation["old_blocks"].append(
            {
                "character_index": old["character_index"],
                "rank": old["rank"],
                "seed_reductions": old["record"]["seed_reductions"],
                "actor_transitions": old["record"]["actor_transitions"],
                "defect_origin_range": old["defect_origin_range"],
            }
        )
    for index, (body, digest) in enumerate(blocks):
        presentation["new_blocks"].append(
            {
                "character_index": index,
                "rank": body["rank"],
                "basis_sha256": body["basis_blob"]["sha256"],
                "origin_reductions": body["origin_reductions"],
                "actor_transitions": body["actor_transitions"],
                "dag_sha256": body["dag_sha256"],
                "state_sha256": digest,
            }
        )
    presentation["sha256"] = sha256_bytes(canonical_json(presentation))
    return presentation


def act_lower_word(
    context: Context,
    lower: np.ndarray,
    auxiliary: np.ndarray,
    source_actor: Affine,
    tag_actors: tuple[Affine, ...],
) -> tuple[np.ndarray, np.ndarray]:
    out = np.zeros_like(lower)
    for source_index, label in enumerate(CHARACTER_LABELS):
        scalar = cv(label, source_actor[1], source_actor[2])
        for tag, actor in enumerate(tag_actors):
            pmap = context.psl_left_map(actor[0])
            for component in (0, 1):
                block = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
                out[source_index, block] = _translated_psl(lower[source_index, block], pmap, scalar)
    return out, auxiliary.copy()


def aggregate_lower_only(context: Context, lower: np.ndarray, auxiliary: np.ndarray) -> np.ndarray:
    out = np.zeros(PHYSICAL_LOWER_WIDTH, dtype=np.uint8)
    for source_index, label in enumerate(CHARACTER_LABELS):
        for tag, block, sign in context.aggregate_table:
            shift = context.physical_shifts[tag]
            pmap = context.psl_left_map(shift[0])
            target_label = context.transport[tag][label]
            target_index = CHARACTER_LABELS.index(target_label)
            scalar = sign * cv(target_label, shift[1], shift[2])
            for component in (0, 1):
                source = slice(lower_coord(tag, component, 0), lower_coord(tag, component, 0) + 504)
                destination = slice(
                    physical_lower_coord(target_index, block, component, 0),
                    physical_lower_coord(target_index, block, component, 0) + 504,
                )
                _add_mod3(out[destination], _translated_psl(lower[source_index, source], pmap, scalar))
    for tag, block, sign in context.aggregate_table:
        out[PHYSICAL_LOWER_REGULAR_WIDTH + block] = (
            int(out[PHYSICAL_LOWER_REGULAR_WIDTH + block]) + sign * int(auxiliary[tag])
        ) % 3
    out[PHYSICAL_LOWER_REGULAR_WIDTH + 2 :] = auxiliary[6:]
    return out


def replay_lower_terms(
    context: Context,
    base_pairs: list[tuple[np.ndarray, np.ndarray, np.ndarray]],
    terms: list[list[Any]],
    started: float,
    seconds_cap: float,
    rss_cap: int,
    phase: str,
) -> np.ndarray:
    out = np.zeros(PHYSICAL_LOWER_WIDTH, dtype=np.uint8)
    actor_cache: dict[tuple[int, ...], tuple[Affine, tuple[Affine, ...]]] = {}
    last_report = time.monotonic()
    for index, (seed, word0, coefficient) in enumerate(terms):
        word = tuple(int(x) for x in word0)
        if word not in actor_cache:
            actor_cache[word] = context.source_word_value(word), context.source_word_tags(word)
        base = base_pairs[int(seed) - 1]
        acted = act_lower_word(context, base[0], base[2], *actor_cache[word])
        _add_mod3(out, aggregate_lower_only(context, acted[0], acted[1]), int(coefficient))
        now = time.monotonic()
        if (index + 1) % 256 == 0 or now - last_report >= 30:
            progress(phase, None, index + 1, 0, len(terms) - index - 1, started)
            enforce_resource(started, seconds_cap, rss_cap, phase)
            last_report = now
    enforce_resource(started, seconds_cap, rss_cap, phase)
    return out


def replay_precision_one_terms(
    context: Context,
    base_pairs: list[tuple[np.ndarray, np.ndarray, np.ndarray]],
    terms: list[list[Any]],
    started: float,
    seconds_cap: float,
    rss_cap: int,
) -> tuple[np.ndarray, np.ndarray]:
    lower = np.zeros(PHYSICAL_LOWER_WIDTH, dtype=np.uint8)
    grade = np.zeros(PHYSICAL_GRADE_WIDTH, dtype=np.uint8)
    actor_cache: dict[tuple[int, ...], tuple[Affine, tuple[Affine, ...]]] = {}
    last_report = time.monotonic()
    for index, (seed, word0, coefficient) in enumerate(terms):
        word = tuple(int(x) for x in word0)
        if word not in actor_cache:
            actor_cache[word] = context.source_word_value(word), context.source_word_tags(word)
        base = base_pairs[int(seed) - 1]
        acted = act_pair(context, base[0], base[1], base[2], *actor_cache[word])
        physical = aggregate_pair(context, acted[0], acted[1], acted[2])
        _add_mod3(lower, physical[0], int(coefficient))
        _add_mod3(grade, physical[1], int(coefficient))
        now = time.monotonic()
        if (index + 1) % 256 == 0 or now - last_report >= 30:
            progress("prepare-precision1-replay", None, index + 1, 0, len(terms) - index - 1, started)
            last_report = now
        enforce_resource(started, seconds_cap, rss_cap, "prepare-precision1-replay")
    return lower, grade


def packed_matrix_bytes(matrix: np.ndarray) -> bytes:
    if matrix.ndim != 2 or matrix.shape[1] % 4:
        raise ValueError("matrix_pack_shape")
    output = np.empty((matrix.shape[0], matrix.shape[1] // 4), dtype=np.uint8)
    for index in range(matrix.shape[0]):
        output[index] = pack_trits(matrix[index])
    return output.tobytes(order="C")


def build_real_prepare(state_dir: Path, started: float) -> tuple[dict[str, Any], str]:
    payloads, input_receipt = load_pinned_inputs()
    input_digest = sha256_bytes(canonical_json(input_receipt))
    words = json.loads(payloads["scratchpad/a0_paper_words_v1.json"].decode("utf-8"))
    certificate = json.loads(payloads["search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json"].decode("utf-8"))
    if certificate.get("terminal") != "ORDER_2016_JOINT_MEMBER" or certificate.get("source_ancestry", {}).get("literal_q1_replay") is not True:
        raise RuntimeError("order2016_member_gate")
    raw_terms = certificate["source_ancestry"]["full_literal_terms"]
    if len(raw_terms) != 3936:
        raise RuntimeError("order2016_raw_term_count")
    raw_digest = sha256_bytes(json.dumps(raw_terms, separators=(",", ":")).encode("ascii"))
    if raw_digest != "3b902c612b2297c1144743620ac578f62d2c19e1f61cb76dfcdd18028dc2dd9e":
        raise RuntimeError("order2016_raw_term_digest")
    canonical_terms = canonicalize_full_literal_terms(raw_terms)
    if len(canonical_terms) != 2622:
        raise RuntimeError(f"canonical_term_count:{len(canonical_terms)}")
    canonical_digest = sha256_bytes(json.dumps(canonical_terms, separators=(",", ":")).encode("ascii"))
    context = Context(words)
    cap_seconds = float(os.environ.get("TASK554_PREPARE_SECONDS", "900"))
    cap_rss = int(os.environ.get("TASK554_MAX_RSS", str(8 * 1024**3)))
    base_pairs: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
    for seed, raw_word in enumerate(words["relators"], 1):
        base_pairs.append(evaluate_occurrence_pair(tuple(int(x) for x in raw_word), context))
        if seed % 8 == 0:
            progress("prepare-seeds", None, seed, 0, 44 - seed, started)
            enforce_resource(started, cap_seconds, cap_rss, "prepare-seeds")
    enforce_resource(started, cap_seconds, cap_rss, "prepare-seeds")
    target_lower, target_grade = direct_physical_target(context)
    raw_lower = replay_lower_terms(
        context, base_pairs, raw_terms, started, cap_seconds, cap_rss, "prepare-q1-raw-replay"
    )
    canonical_lower = replay_lower_terms(
        context,
        base_pairs,
        canonical_terms,
        started,
        cap_seconds,
        cap_rss,
        "prepare-q1-canonical-replay",
    )
    if not np.array_equal(raw_lower, canonical_lower):
        raise RuntimeError("canonical_q1_replay_mismatch")
    if not np.array_equal(canonical_lower, target_lower):
        raise RuntimeError("order2016_target_replay")
    if np.any(canonical_lower[PHYSICAL_LOWER_REGULAR_WIDTH:]) or np.any(target_lower[PHYSICAL_LOWER_REGULAR_WIDTH:]):
        raise RuntimeError("lower_pb3_or_normalized_exponent_nonzero")
    precision_lower, precision_grade = replay_precision_one_terms(
        context, base_pairs, canonical_terms, started, cap_seconds, cap_rss
    )
    if not np.array_equal(precision_lower, target_lower):
        raise RuntimeError("precision1_lower_replay")
    residual = ((target_grade.astype(np.int16) - precision_grade.astype(np.int16)) % 3).astype(np.uint8)
    residual_blob = write_blob(
        state_dir,
        "grade1-residual",
        pack_trits(residual).tobytes(),
        rows=1,
        width=PHYSICAL_GRADE_WIDTH,
        encoding="base3-four-trits-per-byte",
    )
    projected: list[list[tuple[np.ndarray, np.ndarray, np.ndarray]]] = [[], [], [], []]
    for char_index, label in enumerate(CHARACTER_LABELS):
        for seed, base in enumerate(base_pairs, 1):
            projected[char_index].append(projected_seed_pair(context, base, label))
        progress("prepare-projectors", char_index, 44, 0, 0, started)
    lower_owners: list[PackedEchelon] = []
    lower_records: list[dict[str, Any]] = []
    lift_matrices: list[np.ndarray] = []
    old_blocks: list[dict[str, Any]] = []
    for char_index, label in enumerate(CHARACTER_LABELS):
        seed_rows = []
        projected_grades = []
        for pair in projected[char_index]:
            row = np.zeros(LOWER_ECHELON_WIDTH, dtype=np.uint8)
            row[:SOURCE_BASE_WIDTH] = pair[0][char_index]
            row[SOURCE_BASE_WIDTH:] = pair[2]
            seed_rows.append(row)
            projected_grades.append(pair[1].reshape(SOURCE_TOTAL_WIDTH))
        owner, record = close_lower_block(
            context, label, seed_rows, started, cap_seconds, cap_rss
        )
        lifts = evaluate_old_lifts(
            context, label, owner, record, projected_grades, started, cap_seconds, cap_rss
        )
        lower_blob = write_blob(
            state_dir,
            f"old-{char_index}-lower-basis",
            owner.matrix_bytes(),
            rows=len(owner.rows),
            width=LOWER_ECHELON_WIDTH,
            encoding="base3-four-trits-per-byte",
        )
        lift_blob = write_blob(
            state_dir,
            f"old-{char_index}-lifted-grade",
            packed_matrix_bytes(lifts),
            rows=len(owner.rows),
            width=SOURCE_TOTAL_WIDTH,
            encoding="base3-four-trits-per-byte",
        )
        lower_owners.append(owner)
        lower_records.append(record)
        lift_matrices.append(lifts)
        old_blocks.append(
            {
                "character_index": char_index,
                "character": list(label),
                "rank": len(owner.rows),
                "record": record,
                "lower_basis_blob": lower_blob,
                "lifted_grade_blob": lift_blob,
            }
        )
    writers = [BlobStreamWriter(state_dir, f"defect-packet-{index}") for index in range(4)]
    defect_origins: list[dict[str, Any]] = []
    zero_counts = [0, 0, 0, 0]
    try:
        for char_index, label in enumerate(CHARACTER_LABELS):
            begin = len(defect_origins)
            owner = lower_owners[char_index]
            record = lower_records[char_index]
            lifts = lift_matrices[char_index]
            for seed in range(44):
                work = projected[char_index][seed][1].reshape(SOURCE_TOTAL_WIDTH).copy()
                for pivot, coefficient in record["seed_reductions"][seed]:
                    _add_mod3(work, lifts[int(pivot)], -int(coefficient))
                defect_origins.append(
                    {"id": len(defect_origins), "kind": "seed", "lower_character": char_index, "seed": seed + 1}
                )
                for packet in range(4):
                    row = work.reshape(4, SOURCE_BLOCK_WIDTH)[packet]
                    if not np.any(row):
                        zero_counts[packet] += 1
                    writers[packet].write(pack_trits(row).tobytes())
            for pivot in range(len(owner.rows)):
                lower_row = owner.dense_row(pivot)
                for actor_index, letter in enumerate(ACTORS):
                    work = exact_actor_on_old_lift(context, lower_row, lifts[pivot], label, letter)
                    for earlier, coefficient in record["actor_transitions"][pivot][actor_index]:
                        _add_mod3(work, lifts[int(earlier)], -int(coefficient))
                    defect_origins.append(
                        {
                            "id": len(defect_origins),
                            "kind": "transition",
                            "lower_character": char_index,
                            "pivot": pivot,
                            "letter": letter,
                        }
                    )
                    for packet in range(4):
                        row = work.reshape(4, SOURCE_BLOCK_WIDTH)[packet]
                        if not np.any(row):
                            zero_counts[packet] += 1
                        writers[packet].write(pack_trits(row).tobytes())
                    if len(defect_origins) % 128 == 0:
                        progress("prepare-defects", char_index, len(defect_origins), 0, 0, started)
                    enforce_resource(started, cap_seconds, cap_rss, "prepare-defects")
            old_blocks[char_index]["defect_origin_range"] = [begin, len(defect_origins)]
        packets = []
        origin_digest = sha256_bytes(canonical_json(defect_origins))
        for packet, writer in enumerate(writers):
            receipt = writer.finish(
                rows=len(defect_origins),
                width=SOURCE_BLOCK_WIDTH,
                encoding="base3-four-trits-per-byte",
            )
            packets.append(
                {
                    "character": list(CHARACTER_LABELS[packet]),
                    "blob": receipt,
                    "origin_count": len(defect_origins),
                    "zero_rows": zero_counts[packet],
                    "origin_sha256": origin_digest,
                }
            )
    except Exception:
        for writer in writers:
            try:
                writer.abort()
            except Exception:
                pass
        raise
    pure_values = []
    for parity in CHARACTER_LABELS:
        value = context.pure_source_affine[parity]
        pure_values.append(
            {
                "parity": list(parity),
                "word": list(PURE_Q1_WORDS[parity]),
                "q1_endpoint": {"psl_identity": value[0] == floor.ID9, "parity": [value[1], value[2]]},
                "q2_kernel": list(value[3]),
                "tag_values": [
                    {"parity": [entry[1], entry[2]], "kernel": list(entry[3])}
                    for entry in context.pure_tags_affine[parity]
                ],
            }
        )
    body = {
        "schema": STATE_SCHEMA,
        "phase": "prepare",
        "fixture": False,
        "input_manifest": input_receipt,
        "input_manifest_sha256": input_digest,
        "dimensions": fixed_dimensions(),
        "affine_convention": "section-left-kernel-right",
        "substitution_matrices": context.substitution_matrices,
        "pure_q1_projectors": pure_values,
        "canonical_solution": {
            "raw_terms": len(raw_terms),
            "raw_sha256": raw_digest,
            "canonical_terms": len(canonical_terms),
            "canonical_sha256": canonical_digest,
            "terms": canonical_terms,
            "q1_raw_equals_canonical": True,
            "q1_target_replay": True,
            "pb3_augmentation": [int(x) for x in canonical_lower[PHYSICAL_LOWER_REGULAR_WIDTH : PHYSICAL_LOWER_REGULAR_WIDTH + 2]],
            "normalized_exponent": [int(x) for x in canonical_lower[-2:]],
        },
        "old_blocks": old_blocks,
        "defect_origins": defect_origins,
        "defect_origin_sha256": sha256_bytes(canonical_json(defect_origins)),
        "packets": packets,
        "residual_blob": residual_blob,
        "residual_support": int(np.count_nonzero(residual)),
        "residual_sha256": sparse_digest(residual),
        "paired_lower_presentation_complete": True,
        "elapsed_seconds": time.monotonic() - started,
        "peak_owner_bytes": {
            "old_lower_packed": sum(len(owner.rows) * owner.packed_width for owner in lower_owners),
            "old_lift_dense": sum(matrix.nbytes for matrix in lift_matrices),
            "packets_packed": sum(packet["blob"]["bytes"] for packet in packets),
        },
        "downstream_claim_flags": false_claim_flags(),
    }
    digest = write_sealed_state(state_dir, "prepare", body, None)
    return body, digest


TermMap = dict[tuple[int, tuple[int, ...]], int]


def term_map_add(target: TermMap, source: TermMap, scalar: int = 1, prefix: tuple[int, ...] = ()) -> None:
    multiplier = scalar % 3
    if not multiplier:
        return
    for (seed, word), coefficient in source.items():
        key = seed, tuple(floor.wm(prefix, word)) if prefix else word
        value = (target.get(key, 0) + multiplier * coefficient) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


class LiteralExpander:
    def __init__(
        self,
        prepare: dict[str, Any],
        blocks: list[tuple[dict[str, Any], str]],
        merge: dict[str, Any],
    ):
        self.prepare = prepare
        self.blocks = [body for body, _ in blocks]
        self.merge = merge

    def member_update(self) -> list[list[Any]]:
        """Flatten only selected roots, retaining one final leaf map.

        Pending DAG states are collected by (node,prefix); no pivot owns a
        fully expanded term dictionary.  This keeps the load-bearing MEMBER
        expansion bounded by the actual selected ancestry rather than by all
        discovery pivots.
        """
        pending: dict[tuple[Any, ...], int] = {}
        leaves: TermMap = {}
        started = time.monotonic()
        cap_seconds = float(os.environ.get("TASK554_ANCESTRY_SECONDS", "21600"))
        cap_rss = int(os.environ.get("TASK554_MAX_RSS", str(8 * 1024**3)))

        def push(kind: str, ids: tuple[int, ...], prefix: tuple[int, ...], coefficient: int) -> None:
            key = (kind, *ids, prefix)
            value = (pending.get(key, 0) + coefficient) % 3
            if value:
                pending[key] = value
            else:
                pending.pop(key, None)

        def leaf(seed: int, word: tuple[int, ...], coefficient: int) -> None:
            key = seed, word
            value = (leaves.get(key, 0) + coefficient) % 3
            if value:
                leaves[key] = value
            else:
                leaves.pop(key, None)

        def prepend(prefix: tuple[int, ...], suffix: tuple[int, ...]) -> tuple[int, ...]:
            return tuple(floor.wm(prefix, suffix))

        for pivot, coefficient in self.merge["member_coefficients"]:
            push("grade", (int(pivot),), (), int(coefficient))
        steps = 0
        while pending:
            state, coefficient = pending.popitem()
            kind, *rest = state
            prefix = rest.pop()
            ids = tuple(int(x) for x in rest)
            steps += 1
            if kind == "grade":
                node = self.merge["physical_grade_dag"][ids[0]]
                scale = int(node["scale"])
                origin = node["origin"]
                if origin["kind"] == "block_basis":
                    push("block", (int(origin["character"]), int(origin["pivot"])), prefix, coefficient * scale)
                elif origin["kind"] == "old_connection":
                    push("old", (int(origin["character"]), int(origin["pivot"])), prefix, coefficient * scale)
                    for earlier, value in origin["lower_reductions"]:
                        push("lower", (int(earlier),), prefix, -coefficient * scale * int(value))
                else:
                    raise RuntimeError("expand_grade_origin")
                for earlier, value in node["reductions"]:
                    push("grade", (int(earlier),), prefix, -coefficient * scale * int(value))
            elif kind == "lower":
                node = self.merge["physical_lower_dag"][ids[0]]
                scale = int(node["scale"])
                origin = node["origin"]
                push("old", (int(origin["character"]), int(origin["pivot"])), prefix, coefficient * scale)
                for earlier, value in node["reductions"]:
                    push("lower", (int(earlier),), prefix, -coefficient * scale * int(value))
            elif kind == "block":
                character, pivot = ids
                node = self.blocks[character]["dag_nodes"][pivot]
                scale = int(node["scale"])
                origin = node["origin"]
                if origin["kind"] == "defect":
                    label = CHARACTER_LABELS[character]
                    for parity in CHARACTER_LABELS:
                        push(
                            "defect",
                            (int(origin["origin"]),),
                            prepend(prefix, PURE_Q1_WORDS[parity]),
                            coefficient * scale * cv(label, parity[0], parity[1]),
                        )
                elif origin["kind"] == "actor":
                    push(
                        "block",
                        (character, int(origin["parent"])),
                        prepend(prefix, (int(origin["letter"]),)),
                        coefficient * scale,
                    )
                else:
                    raise RuntimeError("expand_block_origin")
                for earlier, value in node["reductions"]:
                    push("block", (character, int(earlier)), prefix, -coefficient * scale * int(value))
            elif kind == "defect":
                origin = self.prepare["defect_origins"][ids[0]]
                character = int(origin["lower_character"])
                old = self.prepare["old_blocks"][character]
                if origin["kind"] == "seed":
                    seed = int(origin["seed"])
                    label = CHARACTER_LABELS[character]
                    for parity in CHARACTER_LABELS:
                        leaf(seed, prepend(prefix, PURE_Q1_WORDS[parity]), coefficient * cv(label, parity[0], parity[1]))
                    expression = old["record"]["seed_reductions"][seed - 1]
                elif origin["kind"] == "transition":
                    pivot, letter = int(origin["pivot"]), int(origin["letter"])
                    push("old", (character, pivot), prepend(prefix, (letter,)), coefficient)
                    expression = old["record"]["actor_transitions"][pivot][ACTORS.index(letter)]
                else:
                    raise RuntimeError("expand_defect_origin")
                for pivot, value in expression:
                    push("old", (character, int(pivot)), prefix, -coefficient * int(value))
            elif kind == "old":
                character, pivot = ids
                node = self.prepare["old_blocks"][character]["record"]["dag_nodes"][pivot]
                scale = int(node["scale"])
                origin = node["origin"]
                if origin["kind"] == "projected_seed":
                    label = CHARACTER_LABELS[character]
                    for parity in CHARACTER_LABELS:
                        leaf(
                            int(origin["seed"]),
                            prepend(prefix, PURE_Q1_WORDS[parity]),
                            coefficient * scale * cv(label, parity[0], parity[1]),
                        )
                elif origin["kind"] == "actor":
                    push(
                        "old",
                        (character, int(origin["parent"])),
                        prepend(prefix, (int(origin["letter"]),)),
                        coefficient * scale,
                    )
                else:
                    raise RuntimeError("expand_old_origin")
                for earlier, value in node["reductions"]:
                    push("old", (character, int(earlier)), prefix, -coefficient * scale * int(value))
            else:
                raise RuntimeError("expand_task_kind")
            if steps % 4096 == 0:
                enforce_resource(started, cap_seconds, cap_rss, "member-ancestry")
        return [
            [seed, list(word), coefficient]
            for (seed, word), coefficient in sorted(leaves.items(), key=lambda item: (item[0][0], item[0][1]))
            if coefficient
        ]


MONOMIALS_LE2 = (
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (2, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (0, 2, 0),
    (0, 1, 1),
    (0, 0, 2),
)
MONOMIALS_DEG2 = MONOMIALS_LE2[4:]
MONOMIAL_LE2_INDEX = {monomial: index for index, monomial in enumerate(MONOMIALS_LE2)}
_POLY2_PRODUCTS: list[list[int]] = [[-1] * 10 for _ in range(10)]
for _left_index, _left_monomial in enumerate(MONOMIALS_LE2):
    for _right_index, _right_monomial in enumerate(MONOMIALS_LE2):
        _product = tuple(_left_monomial[i] + _right_monomial[i] for i in range(3))
        if max(_product) <= 2 and sum(_product) <= 2:
            _POLY2_PRODUCTS[_left_index][_right_index] = MONOMIAL_LE2_INDEX[_product]


def e_polynomial_degree2(vector: tuple[int, int, int]) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    for index, monomial in enumerate(MONOMIALS_LE2):
        coefficient = 1
        for value, exponent in zip(vector, monomial):
            coefficient *= 1 if exponent == 0 else value if exponent == 1 else int(value == 2)
        output[index] = coefficient % 3
    return output


def multiply_polynomial_degree2(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    for i in np.flatnonzero(left):
        for j in np.flatnonzero(right):
            target = _POLY2_PRODUCTS[int(i)][int(j)]
            if target >= 0:
                output[target] = (int(output[target]) + int(left[i]) * int(right[j])) % 3
    return output


RawDegree2 = dict[tuple[int, int, int, int, int], np.ndarray]


def evaluate_occurrence_degree2(word: tuple[int, ...], context: Context) -> RawDegree2:
    output: RawDegree2 = {}
    for tag, pair in enumerate(floor.OO):
        normal, _ = qnorm_affine(tuple(floor.sub(word, *pair)), context)
        for component, value, coefficient in normal:
            key = tag, component, context.psidx[value[0]], value[1], value[2]
            polynomial = output.setdefault(key, np.zeros(10, dtype=np.uint8))
            _add_mod3(polynomial, e_polynomial_degree2(value[3]), coefficient)
            if not np.any(polynomial):
                output.pop(key, None)
    return output


def physical_degree2_coord(character: int, block: int, component: int, monomial: int, psl: int) -> int:
    return (((character * 2 + block) * 2 + component) * 6 + monomial) * 504 + psl


def aggregate_acted_degree2(
    context: Context,
    raw: RawDegree2,
    tag_actors: tuple[Affine, ...],
) -> np.ndarray:
    width = 4 * 2 * 2 * 6 * 504
    output = np.zeros(width, dtype=np.uint8)
    combined = tuple(affine_mul(context.physical_shifts[tag], tag_actors[tag]) for tag in range(6))
    table = {tag: (block, sign) for tag, block, sign in context.aggregate_table}
    for (tag, component, psl, a, b), polynomial in raw.items():
        actor = combined[tag]
        final_psl = context.psidx[floor.M(actor[0], context.psels[psl])]
        final_a, final_b = actor[1] ^ a, actor[2] ^ b
        factor = e_polynomial_degree2(sign_kernel((a, b), actor[3]))
        product = multiply_polynomial_degree2(factor, polynomial)
        block, sign = table[tag]
        for character_index, label in enumerate(CHARACTER_LABELS):
            weight = sign * cv(label, final_a, final_b)
            for local_monomial, coefficient in enumerate(product[4:]):
                if coefficient:
                    coordinate = physical_degree2_coord(
                        character_index, block, component, local_monomial, final_psl
                    )
                    output[coordinate] = (int(output[coordinate]) + weight * int(coefficient)) % 3
    return output


def direct_target_degree2(context: Context) -> np.ndarray:
    width = 4 * 2 * 2 * 6 * 504
    output = np.zeros(width, dtype=np.uint8)
    g = context.g760
    words = (
        tuple(floor.wm(floor.sub(g, *floor.OO[2]), floor.wi(floor.sub(g, *floor.OO[1])), floor.sub(g, *floor.OO[0]))),
        tuple(floor.wm(floor.sub(g, *floor.OO[5]), floor.wi(floor.sub(g, *floor.OO[4])), floor.wi(floor.sub(g, *floor.OO[3])))),
    )
    for block, word in enumerate(words):
        normal, _ = qnorm_affine(word, context)
        for component, value, coefficient0 in normal:
            polynomial = e_polynomial_degree2(value[3])
            psl = context.psidx[value[0]]
            for character_index, label in enumerate(CHARACTER_LABELS):
                weight = -coefficient0 * cv(label, value[1], value[2])
                for local_monomial, coefficient in enumerate(polynomial[4:]):
                    if coefficient:
                        coordinate = physical_degree2_coord(
                            character_index, block, component, local_monomial, psl
                        )
                        output[coordinate] = (int(output[coordinate]) + weight * int(coefficient)) % 3
    return output


def replay_degree2_terms(
    context: Context,
    relators: list[list[int]],
    terms: list[list[Any]],
    started: float,
    seconds_cap: float,
    rss_cap: int,
) -> np.ndarray:
    output = np.zeros(4 * 2 * 2 * 6 * 504, dtype=np.uint8)
    seeds = [evaluate_occurrence_degree2(tuple(int(x) for x in word), context) for word in relators]
    actor_cache: dict[tuple[int, ...], tuple[Affine, ...]] = {}
    for index, (seed, raw_word, coefficient) in enumerate(terms):
        word = tuple(int(x) for x in raw_word)
        if word not in actor_cache:
            actor_cache[word] = context.source_word_tags(word)
        row = aggregate_acted_degree2(context, seeds[int(seed) - 1], actor_cache[word])
        _add_mod3(output, row, int(coefficient))
        if (index + 1) % 256 == 0:
            progress("merge-degree2-replay", None, index + 1, 0, len(terms) - index - 1, started)
            enforce_resource(started, seconds_cap, rss_cap, "merge-degree2-replay")
    return output


def build_terminal_certificate(
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    merge: dict[str, Any],
    merge_digest: str,
    input_receipt: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Construct the unique public certificate from an authenticated final state."""
    if merge.get("fixture") is not False or merge.get("terminal") not in (
        "FIRST_RUNG_GRADE1_MEMBER",
        "FIRST_RUNG_GRADE1_NONMEMBER",
    ):
        raise RuntimeError("certificate_nonfinal_terminal")
    if (
        prepare.get("input_manifest") != input_receipt
        or merge.get("parent_sha256") != prepare_digest
        or merge.get("block_sha256") != [digest for _, digest in blocks]
    ):
        raise RuntimeError("certificate_state_binding")
    return {
        "schema": SCHEMA + ".certificate",
        "producer_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "input_manifest": input_receipt,
        "input_manifest_sha256": prepare["input_manifest_sha256"],
        "state_chain": {
            "prepare_sha256": prepare_digest,
            "block_sha256": [digest for _, digest in blocks],
            "merge_sha256": merge_digest,
        },
        "dimensions": fixed_dimensions(),
        "canonical_solution": prepare["canonical_solution"],
        "pure_q1_projectors": prepare["pure_q1_projectors"],
        "source_closures": [
            {
                "character_index": index,
                "rank": body["rank"],
                "attempts": body["attempts"],
                "queue_exhausted": body["queue_exhausted"],
                "basis_sha256": body["basis_blob"]["sha256"],
                "dag_sha256": body["dag_sha256"],
            }
            for index, (body, _) in enumerate(blocks)
        ],
        "physical": {
            "roster_sha256": merge["physical_roster_sha256"],
            "roster": merge["physical_roster"],
            "lower_rank": merge["physical_lower_rank"],
            "grade_rank": merge["physical_grade_rank"],
            "basis_sha256": merge["physical_grade_basis_blob"]["sha256"],
            "residual_sha256": prepare["residual_sha256"],
            "remainder_sha256": merge["remainder_sha256"],
            "remainder_support": merge["remainder_support"],
            "dual": merge["dual"],
            "dual_pair": merge["dual_pair"],
        },
        "transition_presentation": merge["transition_presentation"],
        "source_ancestry": merge["source_ancestry"],
        "next_degree2_residual": merge["next_degree2_residual"],
        "terminal": merge["terminal"],
        "downstream_claim_flags": false_claim_flags(),
        "verified": False,
        "runtime_seconds": merge["elapsed_seconds"],
    }


def install_or_validate_terminal_certificate(
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    merge: dict[str, Any],
    merge_digest: str,
    input_receipt: dict[str, dict[str, Any]],
    certificate_path: Path | None = None,
) -> dict[str, Any]:
    certificate = build_terminal_certificate(
        prepare, prepare_digest, blocks, merge, merge_digest, input_receipt
    )
    encoded = canonical_json(certificate)
    if certificate_path is None:
        certificate_path = ROOT / "search/certs/d972_r07_a0_first_rung_grade1_v4.json"
    if certificate_path.exists():
        existing = certificate_path.read_bytes()
        if existing != encoded:
            raise RuntimeError("completed_merge_certificate_mismatch")
    else:
        _atomic_write(certificate_path, encoded)
    return certificate


def finalize_real_terminal(
    state_dir: Path,
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    merge: dict[str, Any],
    provisional_digest: str,
    started: float,
) -> tuple[dict[str, Any], str]:
    payloads, input_receipt = load_pinned_inputs()
    if prepare["input_manifest"] != input_receipt:
        raise RuntimeError("terminal_input_manifest")
    words = json.loads(payloads["scratchpad/a0_paper_words_v1.json"].decode("utf-8"))
    context = Context(words)
    source_ancestry: dict[str, Any]
    next_residual: dict[str, Any] | None = None
    if merge["terminal"] == "MEMBER":
        cap_seconds = float(os.environ.get("TASK554_MERGE_SECONDS", "21600"))
        cap_rss = int(os.environ.get("TASK554_MAX_RSS", str(8 * 1024**3)))
        expander = LiteralExpander(prepare, blocks, merge)
        update = expander.member_update()
        base_pairs = [
            evaluate_occurrence_pair(tuple(int(x) for x in word), context) for word in words["relators"]
        ]
        update_lower = replay_lower_terms(
            context,
            base_pairs,
            update,
            started,
            cap_seconds,
            cap_rss,
            "merge-update-lower-replay",
        )
        if np.any(update_lower):
            raise RuntimeError("member_update_lower_change")
        accumulated = canonicalize_full_literal_terms(prepare["canonical_solution"]["terms"] + update)
        replay_lower, replay_grade = replay_precision_one_terms(
            context, base_pairs, accumulated, started, cap_seconds, cap_rss
        )
        target_lower, target_grade = direct_physical_target(context)
        if not np.array_equal(replay_lower, target_lower) or not np.array_equal(replay_grade, target_grade):
            raise RuntimeError("member_direct_precision1_replay")
        degree2_replay = replay_degree2_terms(
            context, words["relators"], accumulated, started, cap_seconds, cap_rss
        )
        degree2_target = direct_target_degree2(context)
        degree2_residual = ((degree2_target.astype(np.int16) - degree2_replay.astype(np.int16)) % 3).astype(np.uint8)
        next_blob = write_blob(
            state_dir,
            "degree2-residual",
            pack_trits(degree2_residual).tobytes(),
            rows=1,
            width=len(degree2_residual),
            encoding="base3-four-trits-per-byte",
        )
        next_residual = {
            "grade": 2,
            "width": len(degree2_residual),
            "support": int(np.count_nonzero(degree2_residual)),
            "sha256": sparse_digest(degree2_residual),
            "blob": next_blob,
        }
        source_ancestry = {
            "grade1_update_terms": update,
            "grade1_update_count": len(update),
            "grade1_update_sha256": sha256_bytes(json.dumps(update, separators=(",", ":")).encode("ascii")),
            "accumulated_terms": accumulated,
            "accumulated_term_count": len(accumulated),
            "accumulated_sha256": sha256_bytes(json.dumps(accumulated, separators=(",", ":")).encode("ascii")),
            "zero_lower_change": True,
            "pb3_augmentation": [0, 0],
            "normalized_exponent": [0, 0],
            "direct_precision1_target_replay": True,
        }
        terminal = "FIRST_RUNG_GRADE1_MEMBER"
    elif merge["terminal"] == "NONMEMBER":
        if merge["dual_pair"] not in (1, 2) or not merge["dual"]:
            raise RuntimeError("nonmember_dual_gate")
        source_ancestry = {
            "grade1_update_terms": [],
            "accumulated_terms": prepare["canonical_solution"]["terms"],
            "direct_precision1_target_replay": False,
        }
        terminal = "FIRST_RUNG_GRADE1_NONMEMBER"
    else:
        raise RuntimeError("UNKNOWN_SEMANTIC:provisional_terminal")
    merge = dict(merge)
    merge.update(
        {
            "terminal": terminal,
            "source_ancestry": source_ancestry,
            "next_degree2_residual": next_residual,
            "provisional_merge_sha256": provisional_digest,
            "elapsed_seconds": time.monotonic() - started,
        }
    )
    final_digest = write_sealed_state(state_dir, "merge", merge, prepare_digest)
    install_or_validate_terminal_certificate(
        prepare, prepare_digest, blocks, merge, final_digest, input_receipt
    )
    return merge, final_digest


def write_sealed_state(state_dir: Path, stem: str, body: dict[str, Any], parent_digest: str | None) -> str:
    body_bytes = canonical_json(body)
    digest = sha256_bytes(body_bytes)
    _atomic_write(state_dir / f"{stem}.{digest}.json", body_bytes)
    head = {
        "schema": STATE_SCHEMA + ".head",
        "stem": stem,
        "body_sha256": digest,
        "parent_sha256": parent_digest,
    }
    _atomic_write(state_dir / f"{stem}.HEAD", canonical_json(head))
    return digest


def read_sealed_state(state_dir: Path, stem: str, parent_digest: str | None = None) -> tuple[dict[str, Any], str]:
    head_path = state_dir / f"{stem}.HEAD"
    head_bytes = head_path.read_bytes()
    head = json.loads(head_bytes)
    if (
        canonical_json(head) != head_bytes
        or set(head) != {"schema", "stem", "body_sha256", "parent_sha256"}
        or head.get("schema") != STATE_SCHEMA + ".head"
        or head.get("stem") != stem
        or not isinstance(head.get("body_sha256"), str)
        or not re.fullmatch(r"[0-9a-f]{64}", head["body_sha256"])
    ):
        raise RuntimeError(f"invalid_state_head:{stem}")
    if head["parent_sha256"] != parent_digest:
        raise RuntimeError(f"state_parent_mismatch:{stem}")
    digest = head["body_sha256"]
    body_bytes = (state_dir / f"{stem}.{digest}.json").read_bytes()
    if sha256_bytes(body_bytes) != digest:
        raise RuntimeError(f"state_body_hash_mismatch:{stem}")
    body = json.loads(body_bytes)
    if body.get("schema") != STATE_SCHEMA or canonical_json(body) != body_bytes:
        raise RuntimeError(f"state_schema_mismatch:{stem}")
    return body, digest


def phase_prepare(state_dir: Path) -> None:
    state_dir = ensure_external_state_dir(state_dir)
    try:
        existing, digest = read_sealed_state(state_dir, "prepare")
    except FileNotFoundError:
        existing = None
    if existing is not None:
        _, receipt = load_pinned_inputs()
        validate_prepare_state(
            state_dir,
            existing,
            receipt,
            fixture=False,
            authenticate_residual=True,
            authenticate_old=True,
            authenticate_packets=range(4),
        )
        print(json.dumps({"phase": "prepare", "resumed": True, "state_sha256": digest}, sort_keys=True))
        return
    started = time.monotonic()
    body, digest = build_real_prepare(state_dir, started)
    print(
        json.dumps(
            {
                "phase": "prepare",
                "resumed": False,
                "state_sha256": digest,
                "old_ranks": [block["rank"] for block in body["old_blocks"]],
                "defect_origins": len(body["defect_origins"]),
                "residual_support": body["residual_support"],
                "elapsed_seconds": body["elapsed_seconds"],
            },
            sort_keys=True,
        )
    )


def phase_block(state_dir: Path, block: int) -> None:
    state_dir = ensure_external_state_dir(state_dir)
    _, receipt = load_pinned_inputs()
    prepare, prepare_digest = read_sealed_state(state_dir, "prepare")
    fixture = bool(prepare.get("fixture"))
    validate_prepare_state(state_dir, prepare, receipt, fixture=fixture)
    try:
        existing, digest = read_sealed_state(state_dir, f"block-{block}", prepare_digest)
    except FileNotFoundError:
        existing = None
    if existing is not None:
        validate_prepare_state(
            state_dir,
            prepare,
            receipt,
            fixture=fixture,
            authenticate_packets=(block,),
        )
        validate_block_state(
            state_dir,
            existing,
            prepare,
            prepare_digest,
            block,
            authenticate_basis=True,
        )
        print(json.dumps({"phase": "block", "block": block, "resumed": True, "state_sha256": digest}, sort_keys=True))
        return
    started = time.monotonic()
    body, digest = run_block_core(state_dir, prepare, prepare_digest, block, started)
    print(
        json.dumps(
            {
                "phase": "block",
                "block": block,
                "resumed": False,
                "state_sha256": digest,
                "rank": body["rank"],
                "attempts": body["attempts"],
                "elapsed_seconds": body["elapsed_seconds"],
            },
            sort_keys=True,
        )
    )


def phase_merge(state_dir: Path) -> None:
    state_dir = ensure_external_state_dir(state_dir)
    _, receipt = load_pinned_inputs()
    prepare, prepare_digest = read_sealed_state(state_dir, "prepare")
    fixture = bool(prepare.get("fixture"))
    validate_prepare_state(state_dir, prepare, receipt, fixture=fixture)
    blocks = [read_sealed_state(state_dir, f"block-{index}", prepare_digest) for index in range(4)]
    for index, (block_body, _) in enumerate(blocks):
        validate_block_state(
            state_dir,
            block_body,
            prepare,
            prepare_digest,
            index,
            authenticate_basis=False,
        )
    try:
        existing, digest = read_sealed_state(state_dir, "merge", prepare_digest)
    except FileNotFoundError:
        existing = None
    started = time.monotonic()
    if existing is not None:
        validate_prepare_state(
            state_dir,
            prepare,
            receipt,
            fixture=fixture,
            authenticate_residual=True,
            authenticate_old=True,
            authenticate_packets=range(4),
        )
        for index, (block_body, _) in enumerate(blocks):
            validate_block_state(
                state_dir,
                block_body,
                prepare,
                prepare_digest,
                index,
                authenticate_basis=True,
            )
        validate_merge_state(
            state_dir,
            existing,
            prepare,
            prepare_digest,
            blocks,
            authenticate_basis=True,
        )
        terminal = existing.get("terminal")
        if prepare.get("fixture"):
            if terminal not in ("FIXTURE_MEMBER", "FIXTURE_NONMEMBER"):
                raise RuntimeError("fixture_merge_resume_terminal")
            print(json.dumps({"phase": "merge", "resumed": True, "state_sha256": digest, "terminal": terminal}, sort_keys=True))
            return
        if terminal in ("MEMBER", "NONMEMBER"):
            body, digest = finalize_real_terminal(
                state_dir, prepare, prepare_digest, blocks, existing, digest, started
            )
        elif terminal in ("FIRST_RUNG_GRADE1_MEMBER", "FIRST_RUNG_GRADE1_NONMEMBER"):
            install_or_validate_terminal_certificate(
                prepare, prepare_digest, blocks, existing, digest, receipt
            )
            print(json.dumps({"phase": "merge", "resumed": True, "state_sha256": digest, "terminal": terminal}, sort_keys=True))
            return
        else:
            raise RuntimeError("merge_resume_terminal")
    else:
        body, digest = run_merge_core(state_dir, prepare, prepare_digest, blocks, started)
        if not prepare.get("fixture"):
            if body.get("block_sha256") != [block_digest for _, block_digest in blocks]:
                raise RuntimeError("provisional_merge_block_binding")
            body, digest = finalize_real_terminal(state_dir, prepare, prepare_digest, blocks, body, digest, started)
    print(json.dumps({"phase": "merge", "resumed": False, "state_sha256": digest, "terminal": body["terminal"], "elapsed_seconds": body["elapsed_seconds"]}, sort_keys=True))


def phase_all(state_dir: Path) -> None:
    phase_prepare(state_dir)
    for block in range(4):
        phase_block(state_dir, block)
    phase_merge(state_dir)


def phase_fixture() -> None:
    started = time.monotonic()

    class V3ReferencePackedEchelon:
        """Tiny fixture-only copy of the frozen v3 reducer."""

        def __init__(self, width: int):
            self.width = width
            self.packed_width = width // 4
            self.rows: list[np.ndarray] = []
            self.leads: list[int] = []
            self.lead_to_pivot: dict[int, int] = {}

        @staticmethod
        def coefficient(row: np.ndarray, coordinate: int) -> int:
            return int((int(row[coordinate // 4]) // (3 ** (coordinate % 4))) % 3)

        def reduce_packed(self, row: np.ndarray) -> tuple[np.ndarray, list[list[int]]]:
            work = np.asarray(row, dtype=np.uint8).copy()
            if work.shape != (self.packed_width,) or np.any(work > 80):
                raise ValueError("reference_packed_reduce_shape")
            reductions: list[list[int]] = []
            cursor = 0
            while True:
                mask = work[cursor:] != 0
                if not bool(mask.any()):
                    break
                byte_index = cursor + int(mask.argmax())
                lead = 4 * byte_index + int(_PACKED_FIRST[int(work[byte_index])])
                pivot = self.lead_to_pivot.get(lead)
                if pivot is None:
                    break
                coefficient = self.coefficient(work, lead)
                work = _PACKED_AXPY[coefficient, work, self.rows[pivot]]
                reductions.append([pivot, coefficient])
                cursor = byte_index
            return work, reductions

        def insert(self, row: np.ndarray) -> dict[str, Any]:
            packed = pack_trits(row) if row.shape == (self.width,) else np.asarray(row, dtype=np.uint8)
            remainder, reductions = self.reduce_packed(packed)
            nonzero_bytes = np.flatnonzero(remainder)
            if not len(nonzero_bytes):
                return {"accepted": False, "reductions": reductions}
            byte_index = int(nonzero_bytes[0])
            lead = 4 * byte_index + int(_PACKED_FIRST[int(remainder[byte_index])])
            leading_coefficient = self.coefficient(remainder, lead)
            scale = 1 if leading_coefficient == 1 else 2
            normalized = remainder if scale == 1 else _PACKED_SCALE2[remainder]
            pivot = len(self.rows)
            self.rows.append(normalized.copy())
            self.leads.append(lead)
            self.lead_to_pivot[lead] = pivot
            return {
                "accepted": True,
                "pivot": pivot,
                "lead": lead,
                "leading_coefficient": leading_coefficient,
                "scale": scale,
                "reductions": reductions,
            }

        def matrix_bytes(self) -> bytes:
            if not self.rows:
                return b""
            return np.stack(self.rows).astype(np.uint8, copy=False).tobytes(order="C")

    reference = V3ReferencePackedEchelon(12)
    optimized = PackedEchelon(12)

    def compare_reduction(row: np.ndarray, gate: str) -> tuple[np.ndarray, list[list[int]]]:
        packed = pack_trits(row)
        reference_remainder, reference_reductions = reference.reduce_packed(packed)
        actual_remainder, actual_reductions = optimized.reduce_packed(packed)
        if not np.array_equal(actual_remainder, reference_remainder) or actual_reductions != reference_reductions:
            raise RuntimeError(f"fixture_reducer_equivalence:{gate}")
        return actual_remainder, actual_reductions

    def compare_insert(row: np.ndarray, gate: str, *, already_reduced: bool = False) -> dict[str, Any]:
        remainder, reductions = compare_reduction(row, gate)
        reference_record = reference.insert(row)
        actual_record = (
            optimized._accept_remainder(remainder, reductions)
            if already_reduced
            else optimized.insert(row)
        )
        if (
            actual_record != reference_record
            or optimized.leads != reference.leads
            or optimized.matrix_bytes() != reference.matrix_bytes()
        ):
            raise RuntimeError(f"fixture_insert_equivalence:{gate}")
        return actual_record

    zero = np.zeros(12, dtype=np.uint8)
    if compare_insert(zero, "zero")["accepted"]:
        raise RuntimeError("fixture_zero_acceptance")
    first_equivalence = np.zeros(12, dtype=np.uint8)
    first_equivalence[5] = 1
    first_equivalence[9] = 2
    missing_remainder, missing_reductions = compare_reduction(first_equivalence, "missing-pivot")
    if missing_reductions or not np.array_equal(missing_remainder, pack_trits(first_equivalence)):
        raise RuntimeError("fixture_missing_pivot")
    compare_insert(first_equivalence, "first-pivot")
    second_equivalence = np.zeros(12, dtype=np.uint8)
    second_equivalence[3] = 1
    second_equivalence[5] = 1
    compare_insert(second_equivalence, "nonmonotone")
    if optimized.leads != [5, 3]:
        raise RuntimeError("fixture_equivalence_nonmonotone")
    third_equivalence = np.zeros(12, dtype=np.uint8)
    third_equivalence[6] = 2
    coefficient_two = compare_insert(
        third_equivalence, "same-byte-coefficient-two", already_reduced=True
    )
    if coefficient_two["leading_coefficient"] != 2 or coefficient_two["scale"] != 2:
        raise RuntimeError("fixture_coefficient_two")
    dependent = (
        2 * optimized.dense_row(0).astype(np.uint16)
        + optimized.dense_row(1).astype(np.uint16)
        + 2 * optimized.dense_row(2).astype(np.uint16)
    ) % 3
    dependent_record = compare_insert(
        dependent.astype(np.uint8), "dependent", already_reduced=True
    )
    if dependent_record != {
        "accepted": False,
        "reductions": [[1, 1], [0, 2], [2, 2]],
    }:
        raise RuntimeError("fixture_dependent_record")

    # Non-monotone-lead canary: pivot ids remain insertion ordered while
    # reduction is ordered by lead coordinate.
    canary = PackedEchelon(8)
    first = np.zeros(8, dtype=np.uint8)
    first[5] = 1
    first[7] = 2
    second = np.zeros(8, dtype=np.uint8)
    second[3] = 1
    second[5] = 1
    if not canary.insert(first)["accepted"] or not canary.insert(second)["accepted"] or canary.leads != [5, 3]:
        raise RuntimeError("fixture_nonmonotone_setup")
    combination = (canary.dense_row(0).astype(np.uint16) + 2 * canary.dense_row(1).astype(np.uint16)) % 3
    remainder, _ = canary.reduce_packed(pack_trits(combination.astype(np.uint8)))
    if np.any(remainder):
        raise RuntimeError("fixture_nonmonotone_reduce")
    with tempfile.TemporaryDirectory(prefix="task562-fixture-") as temporary:
        state_dir = Path(temporary)
        prepare, prepare_digest = write_fixture_prepare(state_dir)
        _, fixture_receipt = load_pinned_inputs()
        validate_prepare_state(
            state_dir,
            prepare,
            fixture_receipt,
            fixture=True,
            authenticate_residual=True,
            authenticate_packets=range(4),
        )
        projector_context = context_for_state(prepare)
        # v443 (3.1) accumulation canary, minimized from frozen seed 3 under
        # conjugator Y^-1, occurrence tag 0.  The induced term from source
        # (0,0) and the direct term from source (0,1) both land here; their
        # coefficients 2+2 must be retained as 1, never overwritten as 2.
        action_lower = np.zeros((4, SOURCE_BASE_WIDTH), dtype=np.uint8)
        action_grade = np.zeros((4, SOURCE_BLOCK_WIDTH), dtype=np.uint8)
        for source_index, source_label in enumerate(CHARACTER_LABELS):
            coefficient = cv(source_label, 1, 0)
            action_lower[source_index, lower_coord(0, 0, 1)] = coefficient
            action_grade[source_index, grade_coord(0, 0, 0, 1)] = coefficient
        actor = projector_context.actor_tags_affine[-2][0]
        direct = affine_mul(actor, (projector_context.psels[1], 1, 0, (1, 0, 0)))
        acted_grade = act_pair(
            projector_context,
            action_lower,
            action_grade,
            np.zeros(LOWER_AUX_WIDTH, dtype=np.uint8),
            projector_context.source_word_value((-2,)),
            projector_context.actor_tags_affine[-2],
        )[1]
        if (
            projector_context.psidx[direct[0]] != 14
            or direct[1:] != (1, 1, (2, 1, 2))
            or int(acted_grade[1, grade_coord(0, 0, 0, 14)]) != 1
        ):
            raise RuntimeError("fixture_v443_actor_accumulation")
        projector_canary = np.zeros((4, SOURCE_BLOCK_WIDTH), dtype=np.uint8)
        for character in range(4):
            projector_canary[character, grade_coord(0, 0, 0, character)] = 1
            projector_canary[character, grade_coord(0, 0, 2, character + 7)] = 2
        selected_character = 2
        projected_canary = project_pure_grade_by_words(
            projector_context, projector_canary, CHARACTER_LABELS[selected_character]
        )
        if any(np.any(projected_canary[index]) for index in range(4) if index != selected_character) or not np.array_equal(
            projected_canary[selected_character], projector_canary[selected_character]
        ):
            raise RuntimeError("fixture_packet_projector_ancestry")
        blocks = [run_block_core(state_dir, prepare, prepare_digest, index, started) for index in range(4)]
        for index, (block_body, _) in enumerate(blocks):
            validate_block_state(
                state_dir,
                block_body,
                prepare,
                prepare_digest,
                index,
                authenticate_basis=True,
            )
        merged, merge_digest = run_merge_core(state_dir, prepare, prepare_digest, blocks, started)
        validate_merge_state(
            state_dir,
            merged,
            prepare,
            prepare_digest,
            blocks,
            authenticate_basis=True,
        )
        if merged["terminal"] != "FIXTURE_MEMBER" or merged["source_blocks_exhausted"] != 4:
            raise RuntimeError("fixture_merge_terminal")
        mutations = 0
        try:
            canonicalize_full_literal_terms([[0, [], 1]])
        except ValueError:
            mutations += 1
        try:
            read_sealed_state(state_dir, "block-0", "0" * 64)
        except RuntimeError:
            mutations += 1
        packet = bytearray(read_blob(state_dir, prepare["packets"][0]["blob"]))
        packet[0] ^= 1
        if sha256_bytes(bytes(packet)) != prepare["packets"][0]["blob"]["sha256"]:
            mutations += 1
        if mutations != 3:
            raise RuntimeError("fixture_mutations")
        recovery_prepare = dict(prepare)
        recovery_prepare["pure_q1_projectors"] = []
        recovery_merge = dict(merged)
        recovery_merge.update(
            {
                "fixture": False,
                "terminal": "FIRST_RUNG_GRADE1_NONMEMBER",
                "source_ancestry": {
                    "grade1_update_terms": [],
                    "accumulated_terms": [],
                    "direct_precision1_target_replay": False,
                },
                "next_degree2_residual": None,
                "elapsed_seconds": 12.5,
            }
        )
        recovery_path = state_dir / "fixture-terminal-certificate.json"
        first_certificate = install_or_validate_terminal_certificate(
            recovery_prepare,
            prepare_digest,
            blocks,
            recovery_merge,
            merge_digest,
            fixture_receipt,
            recovery_path,
        )
        second_certificate = install_or_validate_terminal_certificate(
            recovery_prepare,
            prepare_digest,
            blocks,
            recovery_merge,
            merge_digest,
            fixture_receipt,
            recovery_path,
        )
        if (
            first_certificate != second_certificate
            or first_certificate["runtime_seconds"] != 12.5
            or recovery_path.read_bytes() != canonical_json(first_certificate)
        ):
            raise RuntimeError("fixture_certificate_recovery")
        print(
            json.dumps(
                {
                    "fixture": "PASS",
                    "nonmonotone_leads": canary.leads,
                    "block_ranks": [body["rank"] for body, _ in blocks],
                    "physical_rank": merged["physical_grade_rank"],
                    "terminal": merged["terminal"],
                    "semantic_mutations_rejected": mutations,
                    "packet_projector_ancestry": "PASS",
                    "v443_actor_accumulation": "PASS",
                    "state_validators": "PASS",
                    "certificate_recovery": "PASS",
                    "reducer_equivalence": {
                        "cases": 6,
                        "dependent": "REJECTED",
                        "status": "PASS",
                    },
                    "merge_sha256": merge_digest,
                    "elapsed_seconds": time.monotonic() - started,
                },
                sort_keys=True,
            )
        )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare", metavar="STATE_DIR", type=Path)
    modes.add_argument("--block", metavar="N", type=int, choices=range(4))
    modes.add_argument("--merge", metavar="STATE_DIR", type=Path)
    modes.add_argument("--all", metavar="STATE_DIR", type=Path)
    modes.add_argument("--fixture", action="store_true")
    p.add_argument("--state-dir", type=Path)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    validate_fixed_layouts()
    if args.block is not None:
        if args.state_dir is None:
            parser().error("--block requires --state-dir")
        phase_block(args.state_dir, args.block)
    else:
        if args.state_dir is not None:
            parser().error("--state-dir is valid only with --block")
        if args.prepare is not None:
            phase_prepare(args.prepare)
        elif args.merge is not None:
            phase_merge(args.merge)
        elif args.all is not None:
            phase_all(args.all)
        elif args.fixture:
            phase_fixture()
        else:  # pragma: no cover - argparse makes this unreachable
            raise RuntimeError("fail_closed_phase_dispatch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
