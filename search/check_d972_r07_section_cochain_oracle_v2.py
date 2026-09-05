#!/usr/bin/env python3
"""Task968: Task960 oracle checker with explicit u32 root serialization.

The new source cochain uses a full 27-element cyclic difference basis and
finite-field inversion, not the producer's binomial/polynomial helper.
The accepted snapshot is bound to its completed independent checker receipt.
"""
from __future__ import annotations

import argparse
from collections import deque
from contextlib import ExitStack
import hashlib
from itertools import product
import json
from pathlib import Path
import re
import sys
import tempfile
import time
from typing import Any, Callable

import numpy as np

REFINE_CHECKER_SHA = "1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2"
_lineage_file = Path(__file__).resolve().with_name("check_d972_r07_full_origin_refinement_v1.py")
if _lineage_file.is_symlink() or hashlib.sha256(_lineage_file.read_bytes()).hexdigest() != REFINE_CHECKER_SHA:
    raise ValueError("section_cochain_checker:refinement_checker_pin")
import check_d972_r07_full_origin_refinement_v1 as REFINE

FIXED, LEGACY, BASE, ARITH = REFINE.FIXED, REFINE.LEGACY, REFINE.BASE, REFINE.ARITH
canonical, sha, seal, same = REFINE.canonical, REFINE.sha, REFINE.seal, REFINE.same
pack, unpack, dot, path, fixed = REFINE.pack, REFINE.unpack, REFINE.dot, REFINE.path, REFINE.fixed
SCHEMA = "d972.r07.section-cochain-oracle.v1"
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
KERNEL = tuple(product(range(3), repeat=3))
MONOMIALS = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0),
             (1, 1, 0), (1, 0, 1), (0, 2, 0), (0, 1, 1), (0, 0, 2))
VERTICES, EDGES, CHORDS = 54432, 108864, 54433
LOWER_WIDTH, SOURCE_WIDTH, WIDTH, ROW_BYTES = 96776, 36288, 48384, 12096
OLD_OFFSETS, NEW_OFFSETS = (0, 505, 1008, 1511), (2014, 3523, 5035, 6547)
# Completion artifact preserves the original producer/state/source bytes.
REFINEMENT_ARTIFACT: dict[str, Any] | None = {
    "run": 33971897879, "attempt": 1, "head": "64475e1dfab1537a38d1b3131971bfed5fc3071c",
    "id": 9971466432, "name": "d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1",
    "bytes": 51943596, "sha256": "sha256:0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8"}
REFINEMENT_FILES: dict[str, tuple[int, str]] = {
    "output/HEAD": (921, "6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba"),
    "output/start.json": (11011, "1a709c2853a6d0c239bc31d50ba6e03b0fb4707d93b625d291a487e6d43dc131"),
    "output/owner.json": (8432, "c4fd8b27590450d0b73e72efe9d45bf9319e111b5e21d1f3ff0b0ee23910f48c"),
    "output/source.json": (1139, "7e99018f58f3f49e371b55e6daab491b71855bb463c8c47cd872dffb57b5774f"),
    "output/canonical-index.json": (6078393, "452fe97a9229fa5188493256d1478ead1e684b495bbfed0db03a64f5acf4f00e"),
    "output/result.json": (3988, "04a88c1423f6d99f5e94ded601d20efa5b338ba2b4fae8e9f73023695cd69211"),
    "checker-result.json": (57583, "ccb0b3dd225587dde0e08edca5dfa66b1446b7db01091a3e8118c7aeb4ed2e9c"),
    "source-receipt.json": (2355, "5d65f4313aaed81f30354cba5c90ead201816f72f15fcd799606ed5feab43f3e"),
    "completion-run-receipt.json": (1849, "b1c653283593a2fdef835c938bcc0c8502248b53c92d264842a2133bd4561e57"),
    "preserved-input.json": (183567, "746e097f23c78418a3b43754348099a753639fcceac006e4f1d634ad3fb57298"),
}
REFINEMENT_PRODUCER_SHA = "d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa"
FORMULA = "v548:section-corrected-homogeneous-dual;v546:five-carry;v543:complete-tree"
SCOPE = {"vertices": VERTICES, "positive_edges": EDGES, "chords": CHORDS, "legality_rows": 5,
    "normalized_auxiliaries": 2, "p1_rows": 8059, "characters": [0, 1, 2, 3], "source_tags": 6,
    "snapshot_count": 1, "complete_finite_test": True, "physical_appends": 0}
BEGIN = time.monotonic()
DEADLINE: float | None = None
LAST_PHASE = "initialization"


class ResourceStop(Exception):
    pass


def require(ok: Any, label: str) -> None:
    if not ok:
        raise ValueError("section_cochain_checker:" + label)


def boundary(phase: str, **fields: Any) -> None:
    global LAST_PHASE
    LAST_PHASE = phase
    if DEADLINE is not None and time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)
    print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def inverse_matrix_mod3(matrix: np.ndarray) -> np.ndarray:
    """Independent Gauss-Jordan inversion for the 27-coordinate change of basis."""
    matrix = np.asarray(matrix, dtype=np.int64)
    require(matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1], "square_matrix")
    count = matrix.shape[0]
    augmented = np.column_stack((matrix % 3, np.eye(count, dtype=np.int64)))
    for column in range(count):
        rows = np.flatnonzero(augmented[column:, column])
        require(len(rows) > 0, "invertible_matrix")
        selected = column + int(rows[0])
        if selected != column:
            augmented[[column, selected]] = augmented[[selected, column]]
        augmented[column] = augmented[column] * int(augmented[column, column]) % 3
        for row in range(count):
            if row != column and augmented[row, column]:
                augmented[row] = (augmented[row] - int(augmented[row, column]) * augmented[column]) % 3
    require(np.array_equal(augmented[:, :count], np.eye(count, dtype=np.int64)), "matrix_inverse_identity")
    return augmented[:, count:]


def cyclic_difference_moments() -> tuple[np.ndarray, np.ndarray]:
    """Ordinary E^k coefficients -> augmentation monomials by cyclic differences.

    Start from the delta at identity in F3[C3^3]. Applying (E_i-1) is a
    cyclic roll minus the original vector. The entire 27-by-27 basis is
    inverted before selecting the ten degree<=2 coordinates. No binomial
    coefficient or accepted e_polynomial routine is used.
    """
    expansion = np.zeros((27, 27), dtype=np.int64)
    for row, exponent in enumerate(KERNEL):
        ordinary = np.zeros((3, 3, 3), dtype=np.int64)
        ordinary[0, 0, 0] = 1
        for axis, degree in enumerate(exponent):
            for _ in range(degree):
                ordinary = (np.roll(ordinary, 1, axis=axis) - ordinary) % 3
        expansion[row] = ordinary.reshape(-1)
    inverse = inverse_matrix_mod3(expansion)
    require(np.array_equal(expansion @ inverse % 3, np.eye(27, dtype=np.int64)), "cyclic_moment_complete_basis")
    selected = [KERNEL.index(monomial) for monomial in MONOMIALS]
    return expansion.astype(np.uint8), inverse[:, selected].astype(np.uint8)


class Geometry:
    """Explicit marked section-left/kernel-right Q2 geometry.

    PSL permutations and their accepted ordering are common input premises.
    All new products, right successors and tag maps are constructed here.
    """
    def __init__(self, context: Any):
        self.context = context
        self.elements = context.psels
        self.positions = context.psidx
        self.psl_product = np.empty((504, 504), dtype=np.int32)
        for left_id, left in enumerate(self.elements):
            for right_id, right in enumerate(self.elements):
                self.psl_product[left_id, right_id] = self.positions[tuple(right[left[j]] for j in range(9))]
            if (left_id + 1) % 126 == 0:
                boundary("psl_product_index", rows=left_id + 1)
        self.parities = np.asarray(CHARACTERS, dtype=np.int64)
        self.kernel = np.asarray(KERNEL, dtype=np.int64)
        self.signs = np.array([[1 if parity[1] == 0 else -1, 1 if parity[0] == 0 else -1,
                               1 if (parity[0] ^ parity[1]) == 0 else -1] for parity in CHARACTERS], dtype=np.int64)
        vertex = np.arange(VERTICES, dtype=np.int64)
        self.psl = vertex % 504
        self.kernel_id = (vertex // 504) % 27
        self.parity_id = vertex // (504 * 27)
        self.coordinates = np.column_stack((self.psl, self.parities[self.parity_id], self.kernel[self.kernel_id])).astype(np.int32)
        self.generators = [self.affine_id(image) for image in context.images]
        self.successor = np.column_stack([self.multiply(vertex, generator) for generator in self.generators]).astype(np.int32)
        self.inverse_successor = np.empty_like(self.successor)
        for slot in range(2):
            require(np.array_equal(np.sort(self.successor[:, slot]), vertex), "right_generator_permutation")
            self.inverse_successor[self.successor[:, slot], slot] = vertex
        self.tree_parent, self.tree_edge, self.tree_order = self.positive_tree(self.successor)
        self.tag_images = np.asarray([[self.word_id(pair[slot]) for slot in range(2)] for pair in ARITH.SEED_OO], dtype=np.int32)
        self.tag_maps = np.empty((6, VERTICES), dtype=np.int32)
        self.tag_targets = np.empty((6, VERTICES, 2), dtype=np.int32)
        for tag in range(6):
            mapping = np.full(VERTICES, -1, dtype=np.int32); mapping[0] = 0
            for child in self.tree_order[1:]:
                child = int(child)
                parent, slot = int(self.tree_parent[child]), int(self.tree_edge[child]) % 2
                mapping[child] = self.multiply(int(mapping[parent]), int(self.tag_images[tag, slot]))
            require(np.array_equal(np.sort(mapping), vertex), "tag_vertex_bijection")
            for slot in range(2):
                targets = self.multiply(mapping, int(self.tag_images[tag, slot]))
                require(np.array_equal(targets, mapping[self.successor[:, slot]]), "all_tagged_generator_edges")
                self.tag_targets[tag, :, slot] = targets
            self.tag_maps[tag] = mapping
            boundary("tag_geometry", tag=tag, vertices=VERTICES, edges=EDGES)
        require(np.array_equal(self.tag_maps[0], vertex) and np.array_equal(self.tag_maps[4], vertex),
                "two_distinct_identity_occurrences")
        all_xb = self.multiply(self.multiply(vertex, self.generators[0]),
            self.inverse(self.multiply(self.generators[1], self.generators[0])))
        require(np.array_equal(all_xb, self.inverse_successor[:, 1]), "all_qnorm_right_XB_equals_Y_inverse")
        self.kernel9, self.rotation9 = self.actual_q0_marking()
        rotation = self.signs[self.parity_id] * self.kernel[self.kernel_id] % 3
        carry = np.zeros((VERTICES, 2, 5), dtype=np.uint8)
        for slot in range(2):
            integer_sum = rotation + self.signs[self.parity_id] * self.rotation9[slot]
            numerator = integer_sum - integer_sum % 3
            require(not np.any(numerator % 3), "integer_carry_division")
            carry[:, slot, :3] = (numerator // 3) % 3
            carry[:, slot, 3 + slot] = 1
        self.carry = carry.reshape(EDGES, 5)
        self.tree_mask = np.zeros(EDGES, dtype=np.uint8)
        self.tree_mask[self.tree_edge[self.tree_order[1:]]] = 1
        self.chords = np.flatnonzero(self.tree_mask == 0).astype(np.int32)
        require(len(self.chords) == CHORDS and int(self.tree_mask.sum()) == VERTICES - 1, "complete_graph_tree_chords")

    def affine_id(self, image: Any) -> int:
        parity = 2 * int(image[1]) + int(image[2])
        k = tuple(int(value) % 3 for value in image[3])
        return ((parity * 27 + 9 * k[0] + 3 * k[1] + k[2]) * 504 + self.positions[image[0]])

    def multiply(self, left: Any, right: Any) -> Any:
        left, right = np.asarray(left, dtype=np.int64), np.asarray(right, dtype=np.int64)
        lp, rp = left % 504, right % 504
        le, re = left // (504 * 27), right // (504 * 27)
        lk, rk = (left // 504) % 27, (right // 504) % 27
        k = (self.signs[re] * self.kernel[lk] + self.kernel[rk]) % 3
        p = self.psl_product[lp, rp]
        e = np.bitwise_xor(le, re)
        answer = ((e * 27 + k[..., 0] * 9 + k[..., 1] * 3 + k[..., 2]) * 504 + p)
        return int(answer) if answer.ndim == 0 else answer.astype(np.int32)

    def inverse(self, value: int) -> int:
        p, e, k = value % 504, value // (504 * 27), self.kernel[(value // 504) % 27]
        inverse_psl = int(np.flatnonzero(self.psl_product[p] == 0)[0])
        inverse_k = (-self.signs[e] * k) % 3
        result = ((e * 27 + inverse_k[0] * 9 + inverse_k[1] * 3 + inverse_k[2]) * 504 + inverse_psl)
        require(self.multiply(value, int(result)) == self.multiply(int(result), value) == 0, "affine_inverse")
        return int(result)

    def word_id(self, word: Any) -> int:
        value = 0
        for signed in word:
            letter = int(signed)
            generator = self.generators[abs(letter) - 1]
            value = self.multiply(value, generator if letter > 0 else self.inverse(generator))
        return value

    @staticmethod
    def positive_tree(successor: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        count = len(successor)
        parent, edge = np.full(count, -1, dtype=np.int32), np.full(count, -1, dtype=np.int32)
        seen = np.zeros(count, dtype=np.uint8); seen[0] = 1
        order = [0]
        for tail in order:
            for slot in range(2):
                head = int(successor[tail, slot])
                if not seen[head]:
                    seen[head], parent[head], edge[head] = 1, tail, 2 * tail + slot
                    order.append(head)
        require(len(order) == count and np.all(seen), "positive_bfs_complete")
        return parent, edge, np.asarray(order, dtype=np.int32)

    def actual_q0_marking(self) -> tuple[np.ndarray, np.ndarray]:
        """Read the three actual nine-point affine blocks from the pinned file."""
        marking_file = Path(__file__).resolve().parents[1] / "scratchpad/fuda1_a0_rmax_data.g"
        raw = marking_file.read_bytes()
        require(len(raw) == FIXED.DATA_PINS["scratchpad/fuda1_a0_rmax_data.g"]["bytes"] and
                sha(raw) == FIXED.DATA_PINS["scratchpad/fuda1_a0_rmax_data.g"]["sha256"], "q0_marking_raw_pin")
        text = raw.decode("utf-8")
        matched = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", text, re.S)
        require(matched is not None, "q0_marking_text")
        kernel9, rotation9 = np.empty((2, 3), dtype=np.int64), np.empty((2, 3), dtype=np.int64)
        for slot in range(2):
            image = np.asarray(json.loads(matched.group(slot + 1)), dtype=np.int64) - 1
            require(image.shape == (36,) and np.array_equal(np.sort(image), np.arange(36)), "q0_marking_36_permutation")
            e = self.generators[slot] // (504 * 27)
            reconstructed = list(self.elements[self.generators[slot] % 504])
            for axis in range(3):
                start = 9 + 9 * axis
                block = image[start:start + 9] - start
                k = int(block[0]); sign = int(self.signs[e, axis])
                require(np.array_equal(block, (sign * np.arange(9) + k) % 9) and
                        k % 3 == int(self.kernel[(self.generators[slot] // 504) % 27, axis]), "actual_q0_affine_block")
                kernel9[slot, axis], rotation9[slot, axis] = k, sign * k % 9
                reconstructed.extend((start + (sign * np.arange(9) + k) % 9).tolist())
            require(np.array_equal(image, reconstructed), "q0_marking_full36_reconstruction")
        return kernel9, rotation9


def source_scores(geometry: Geometry, roots: np.ndarray, kappa: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    require(roots.shape == (4, SOURCE_WIDTH) and kappa.shape == (LOWER_WIDTH,), "source_score_inputs")
    expansion, moments = cyclic_difference_moments()
    d0 = kappa[:24192].reshape(4, 6, 2, 504)
    d1 = kappa[24192:96768].reshape(4, 6, 2, 3, 504)
    d2 = roots.reshape(4, 6, 2, 6, 504)
    score = np.empty((6, 2, VERTICES), dtype=np.uint8)
    for tag in range(6):
        for component in range(2):
            functional = np.concatenate((-d0[:, tag, component, None].astype(np.int64),
                -d1[:, tag, component].astype(np.int64), d2[:, tag, component].astype(np.int64)), axis=1)
            for e, parity in enumerate(CHARACTERS):
                weights = np.asarray([1 if sum(x * y for x, y in zip(geometry.context.transport[tag][label], parity)) % 2 == 0 else 2
                                      for label in CHARACTERS], dtype=np.int64)
                by_monomial = np.tensordot(weights, functional, axes=(0, 0)) % 3
                values = moments.astype(np.int64) @ by_monomial % 3
                begin = e * 27 * 504
                score[tag, component, begin:begin + 27 * 504] = values.reshape(-1)
        boundary("ordinary_group_source_scores", tag=tag)
    return score, {"method": "full27-cyclic-difference-basis-inverse", "basis_rows": 27,
        "selected_monomials": [list(item) for item in MONOMIALS], "expansion_sha256": sha(expansion.tobytes()),
        "moments_sha256": sha(moments.tobytes()), "new_binomial_helper_used": False,
        "actual_raw_edge_path_uses_scores": True}


def linear_fox_terms(geometry: Geometry, word: Any) -> tuple[list[tuple[int, int, int]], int]:
    """Ordered signed Fox terms for a possibly NONCLOSED substituted edge."""
    prefix, terms = 0, []
    for signed in word:
        letter = int(signed)
        require(letter in (1, -1, 2, -2), "fox_signed_letter")
        slot = abs(letter) - 1
        if letter < 0:
            prefix = geometry.multiply(prefix, geometry.inverse(geometry.generators[slot]))
            terms.append((slot, prefix, 2))
        else:
            terms.append((slot, prefix, 1))
            prefix = geometry.multiply(prefix, geometry.generators[slot])
    combined: dict[tuple[int, int], int] = {}
    for slot, vertex, coefficient in terms:
        key = (slot, vertex)
        combined[key] = (combined.get(key, 0) + coefficient) % 3
    return [(slot, vertex, coefficient) for (slot, vertex), coefficient in combined.items() if coefficient], prefix


def raw_edge_cochain(geometry: Geometry, score: np.ndarray, kappa: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[Any]]:
    """Linear raw-chain PB3 normalization, including the six augmentation slots."""
    require(score.shape == (6, 2, VERTICES), "full_score_array")
    values = np.zeros((VERTICES, 2), dtype=np.int64)
    x = geometry.generators[0]
    b = geometry.inverse(geometry.multiply(geometry.generators[1], x))
    term_records = []
    for tag, pair in enumerate(ARITH.SEED_OO):
        for slot in range(2):
            terms, endpoint = linear_fox_terms(geometry, pair[slot])
            require(endpoint == int(geometry.tag_images[tag, slot]), "tagged_fox_endpoint")
            augmentation = 0
            for generator, prefix, coefficient in terms:
                # phi_j(q) acts on the LEFT of every Fox prefix.
                vertex = geometry.multiply(geometry.tag_maps[tag], prefix)
                if generator == 0:
                    right_x = geometry.multiply(vertex, x)
                    right_xb = geometry.multiply(right_x, b)
                    values[:, slot] -= coefficient * score[tag, 0, right_x].astype(np.int64)
                    values[:, slot] -= coefficient * score[tag, 1, right_xb].astype(np.int64)
                    augmentation = (augmentation + coefficient) % 3
                else:
                    values[:, slot] += coefficient * score[tag, 1, vertex].astype(np.int64)
            values[:, slot] -= int(kappa[96768 + tag]) * augmentation
            values[:, slot] %= 3
            term_records.append({"tag": tag, "slot": slot, "word": list(pair[slot]),
                "endpoint": endpoint, "terms": [[int(a), int(b), int(c)] for a, b, c in terms],
                "x_augmentation": augmentation})
        boundary("linear_source_edge_pullback", tag=tag, edges=EDGES)
    return values.reshape(-1).astype(np.uint8), ((-kappa[-2:].astype(np.int64)) % 3).astype(np.uint8), term_records


def document(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    return seal({"schema": SCHEMA + "." + kind, **body})


def current_roots_and_contractions(args: argparse.Namespace, state: dict[str, Any],
                                   tables: list[Any], functional: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Fresh four-character adjoints, followed by one complete packed cache pass."""
    roots = np.asarray([FIXED.pullback(table["entries"], functional) for table in tables], dtype=np.uint8)
    require(roots.shape == (4, SOURCE_WIDTH), "four_current_root_shapes")
    BASE.validate_p1({**state["launch"]["p1_parent"], "root": str(args.p1_root.resolve())})
    projections = []
    for vector in roots:
        nonzero = np.flatnonzero(vector)
        projections.append([(nonzero // 4, nonzero % 4, vector[nonzero].astype(np.uint32))])
    values = np.zeros((4, 8059), dtype=np.uint8)
    digest, read_bytes = hashlib.sha256(), 0
    with path(args.p1_root, "degree2.cache.bin").open("rb", buffering=1 << 20) as stream:
        for first in range(0, 8059, 256):
            count = min(256, 8059 - first)
            raw = stream.read(count * 36288)
            require(len(raw) == count * 36288, "current_p1_full_chunk")
            digest.update(raw); read_bytes += len(raw)
            rows = np.frombuffer(raw, dtype=np.uint8).reshape(count, 36288)
            require(not np.any(rows > 80), "current_p1_valid_packing")
            for character in range(4):
                values[character, first:first + count] = BASE.vectorized_projection_chunk(
                    rows, character * 9072, projections[character])[:, 0]
            boundary("current_p1_full_pass", rows=first + count)
        require(stream.read(1) == b"", "current_p1_exact_eof")
    require(read_bytes == BASE.P1_CACHE_BYTES and digest.hexdigest() == BASE.P1_CACHE_SHA256,
            "current_p1_complete_hash")
    return roots, values


def interpolate_rows(width: int, records: list[tuple[int, int]], rhs: np.ndarray,
                     read_row: Callable[[int], np.ndarray]) -> tuple[np.ndarray, list[int]]:
    """Dual solve by ORIGINAL embedded lead; row IDs are never renumbered."""
    require(len({lead for _, lead in records}) == len(records), "dual_original_lead_unique")
    result = np.zeros(width, dtype=np.uint8)
    order = []
    for row_id, lead in sorted(records, key=lambda item: item[1], reverse=True):
        row = np.asarray(read_row(row_id), dtype=np.uint8)
        require(row.shape == (width,) and not np.any(row > 2) and 0 <= lead < width and
                row[lead] == 1 and not np.any(row[:lead]) and result[lead] == 0,
                "dual_normalized_original_lead")
        result[lead] = (int(rhs[row_id]) - dot(result, row)) % 3
        order.append(row_id)
    return result, order


def current_section(args: argparse.Namespace, state: dict[str, Any], roots: np.ndarray,
                    p1_values: np.ndarray) -> dict[str, Any]:
    """Two-stage source interpolation; at most one Task554 JSON body is resident."""
    require(p1_values.shape == (4, 8059), "section_complete_p1_values")
    chi = (p1_values.sum(axis=0, dtype=np.uint16) % 3).astype(np.uint8)
    k1 = np.zeros((4, 18144), dtype=np.uint8)
    original, embedded = np.empty(8059, dtype=np.uint32), np.empty(8059, dtype=np.uint32)
    new_order, new_descriptors, old_descriptors = [], [], []
    for owner in range(4):
        boundary("section_new_original_leads", owner=owner)
        checked = BASE.state_descriptor(state["task554"]["blocks"][owner], owner)
        body, descriptor = checked["body"], checked["body"]["basis_blob"]
        offset = NEW_OFFSETS[owner]
        records = [(offset + local, int(node["lead"])) for local, node in enumerate(body["dag_nodes"])]
        require(len(records) == BASE.NEW_RANKS[owner] and
                all(body["pivot_leads"][local] == lead for local, (_, lead) in enumerate(records)), "section_new_original_ids")
        for row_id, lead in records:
            original[row_id], embedded[row_id] = lead, 24192 + owner * 18144 + lead
        with path(checked["root"], descriptor["file"]).open("rb") as stream:
            vector, order = interpolate_rows(18144, records, chi,
                lambda row_id: unpack(LEGACY.blob_row(stream, row_id - offset, 18144), 18144))
        k1[owner] = vector; new_order.extend(order)
        new_descriptors.append((checked["root"], descriptor, checked["body_sha256"]))
        del checked, body, descriptor
        boundary("section_new_solved", owner=owner)

    beta = chi[:2014].copy()
    old_records, locations = [], {}
    boundary("section_old_original_leads")
    checked = BASE.state_descriptor(state["task554"]["prepare"], -1)
    for owner, old in enumerate(checked["body"]["old_blocks"]):
        offset = OLD_OFFSETS[owner]
        for local, node in enumerate(old["record"]["dag_nodes"]):
            row_id, lead = offset + local, int(node["lead"])
            require(node["pivot"] == local and 0 <= lead < 6056, "section_old_original_id")
            small_lead = owner * 6048 + lead if lead < 6048 else 24192 + lead - 6048
            original[row_id] = lead
            embedded[row_id] = owner * 6048 + lead if lead < 6048 else 96768 + lead - 6048
            old_records.append((row_id, small_lead)); locations[row_id] = (owner, local, lead)
        grade_values, _ = BASE.checker_stream_dots(checked["root"], old["lifted_grade_blob"], [k1.reshape(-1)],
            body_sha256=checked["body_sha256"], role=f"section-beta-old-{owner}-grade")
        count = BASE.OLD_RANKS[owner]
        beta[offset:offset + count] = (beta[offset:offset + count].astype(np.int16) - grade_values[:, 0]) % 3
        old_descriptors.append((checked["root"], old["lower_basis_blob"], old["lifted_grade_blob"], checked["body_sha256"]))
        boundary("section_old_beta", owner=owner)
    del old, checked
    with ExitStack() as stack:
        streams = [stack.enter_context(path(root, lower["file"]).open("rb")) for root, lower, _, _ in old_descriptors]

        def embedded_old_row(row_id: int) -> np.ndarray:
            owner, local, lead = locations[row_id]
            row = unpack(LEGACY.blob_row(streams[owner], local, 6056), 6056)
            require(row[lead] == 1 and not np.any(row[:lead]), "old_local_original_lead")
            require(owner == 0 or not np.any(row[6048:]), "old_nontrivial_character_shared_aux_zero")
            result = np.zeros(24200, dtype=np.uint8)
            result[owner * 6048:(owner + 1) * 6048], result[24192:] = row[:6048], row[6048:]
            return result

        kE, old_order = interpolate_rows(24200, old_records, beta, embedded_old_row)
    kappa = np.concatenate((kE[:24192], k1.reshape(-1), kE[24192:]))
    equation_values = np.empty(8059, dtype=np.uint8)
    receipts = []
    for owner, (root, lower, grade, body_sha) in enumerate(old_descriptors):
        slice0, slice1 = BASE.checker_old_slices([kappa], owner)
        dots0, receipt0 = BASE.checker_stream_dots(root, lower, slice0, body_sha256=body_sha, role=f"section-final-old-{owner}-lower")
        dots1, receipt1 = BASE.checker_stream_dots(root, grade, slice1, body_sha256=body_sha, role=f"section-final-old-{owner}-grade")
        offset, count = OLD_OFFSETS[owner], BASE.OLD_RANKS[owner]
        equation_values[offset:offset + count] = (dots0[:, 0].astype(np.uint16) + dots1[:, 0]) % 3
        receipts.extend((receipt0, receipt1))
        boundary("section_final_equations_old", owner=owner)
    for owner, (root, descriptor, body_sha) in enumerate(new_descriptors):
        dots, receipt = BASE.checker_stream_dots(root, descriptor, BASE.checker_new_slices([kappa], owner),
            body_sha256=body_sha, role=f"section-final-new-{owner}")
        offset, count = NEW_OFFSETS[owner], BASE.NEW_RANKS[owner]
        equation_values[offset:offset + count] = dots[:, 0]
        receipts.append(receipt)
        boundary("section_final_equations_new", owner=owner)
    residuals = ((equation_values.astype(np.int16) - chi) % 3).astype(np.uint8)
    require(not np.any(residuals) and len(new_order) == 6045 and len(old_order) == 2014 and
            len(receipts) == 12 and kappa.shape == (LOWER_WIDTH,), "all_8059_section_equations")
    return {"roots": roots, "p1_values": p1_values, "chi": chi, "beta": beta, "kappa": kappa,
        "equation_values": equation_values, "equation_residuals": residuals,
        "original": original, "embedded": embedded, "new_order": np.asarray(new_order, dtype=np.uint32),
        "old_order": np.asarray(old_order, dtype=np.uint32), "blob_receipts": receipts}


def first_independent_columns(columns: np.ndarray) -> tuple[list[int], np.ndarray]:
    require(columns.ndim == 2 and columns.shape[1] == 5 and not np.any(columns > 2), "five_tau_coordinates")
    echelon: dict[int, np.ndarray] = {}
    selected = []
    for index, value in enumerate(columns):
        row = value.astype(np.int64).copy()
        for pivot in sorted(echelon):
            row = (row - int(row[pivot]) * echelon[pivot]) % 3
        nonzero = np.flatnonzero(row)
        if len(nonzero):
            pivot = int(nonzero[0])
            echelon[pivot] = row * int(row[pivot]) % 3
            selected.append(index)
            if len(selected) == 5:
                break
    require(len(selected) == 5, "tau_full_rank_five_prerequisite")
    return selected, inverse_matrix_mod3(columns[selected].astype(np.int64).T)


def complete_tree_test(geometry: Geometry, f: np.ndarray, b_aux: np.ndarray) -> dict[str, Any]:
    require(f.shape == (EDGES,) and b_aux.shape == (2,) and not np.any(f > 2) and not np.any(b_aux > 2), "tree_complete_input")
    potential_f = np.zeros(VERTICES, dtype=np.uint8)
    potential_tau = np.zeros((VERTICES, 5), dtype=np.uint8)
    for position, child in enumerate(geometry.tree_order[1:], 1):
        child = int(child); parent, edge = int(geometry.tree_parent[child]), int(geometry.tree_edge[child])
        require(edge // 2 == parent and int(geometry.successor[parent, edge % 2]) == child, "tree_path_edge_join")
        potential_f[child] = (int(potential_f[parent]) + int(f[edge])) % 3
        potential_tau[child] = (potential_tau[parent].astype(np.uint16) + geometry.carry[edge]) % 3
        if position % 12000 == 0:
            boundary("tree_potentials", vertices=position + 1)
    chord_edges = geometry.chords
    tails, slots = chord_edges // 2, chord_edges % 2
    heads = geometry.successor[tails, slots]
    chord_values = ((f[chord_edges].astype(np.int16) + potential_f[tails] - potential_f[heads]) % 3).astype(np.uint8)
    tau = ((geometry.carry[chord_edges].astype(np.int16) + potential_tau[tails] - potential_tau[heads]) % 3).astype(np.uint8)
    require(len(chord_edges) == CHORDS and len(np.unique(chord_edges)) == CHORDS, "tree_full_chord_eof")
    selected, inverse = first_independent_columns(tau)
    selected_edges = chord_edges[selected]
    fit = (chord_values[selected].astype(np.int64) @ inverse % 3).astype(np.uint8)
    fitted = tau.astype(np.int64) @ fit.astype(np.int64) % 3
    residuals = ((chord_values.astype(np.int64) - fitted) % 3).astype(np.uint8)
    failed = np.flatnonzero(residuals)
    nonzero_aux = np.flatnonzero(b_aux)
    first_failed = int(chord_edges[failed[0]]) if len(failed) else None
    if len(nonzero_aux):
        coordinate = int(nonzero_aux[0]); eta = [0, 0]; eta[coordinate] = 1
        witness = {"kind": "auxiliary", "coordinate": coordinate, "cycles": [], "eta": eta,
            "tau": [0] * 5, "scalar": int(b_aux[coordinate]), "materialization": "MATERIALIZATION_PENDING"}
    elif len(failed):
        index = int(failed[0])
        coefficients = inverse @ tau[index].astype(np.int64) % 3
        direct_tau = (tau[index].astype(np.int64) - coefficients @ tau[selected].astype(np.int64)) % 3
        scalar = int((int(chord_values[index]) - coefficients @ chord_values[selected].astype(np.int64)) % 3)
        require(not np.any(direct_tau) and scalar == int(residuals[index]) and scalar in (1, 2), "six_cycle_tau_zero_scalar_nonzero")
        cycles = [{"edge": int(chord_edges[index]), "coefficient": 1}] + [
            {"edge": int(edge), "coefficient": int(-coefficient % 3)} for edge, coefficient in zip(selected_edges, coefficients)]
        witness = {"kind": "chord", "failed_chord": int(chord_edges[index]), "basis_chords": selected_edges.tolist(),
            "basis_coefficients": coefficients.tolist(), "cycles": cycles, "eta": [0, 0],
            "tau": direct_tau.tolist(), "scalar": scalar, "materialization": "MATERIALIZATION_PENDING"}
    else:
        witness = {"kind": "none", "cycles": [], "eta": [0, 0], "tau": [0] * 5, "scalar": 0,
            "materialization": "NOT_NEEDED_FOR_ZERO_TEST"}
    terminal = "COMPLETE_ZERO_CANDIDATE" if witness["kind"] == "none" else "VIOLATION_CANDIDATE"
    boundary("complete_tree_eof", chords=CHORDS, auxiliary_count=2)
    metadata = document("tree", {"vertices": VERTICES, "tree_edges": VERTICES - 1, "chords": CHORDS,
        "independent_tau_columns": 5, "selection_order": "first-independent-chord;coordinate0-through4",
        "selected_chords": selected_edges.tolist(), "fit": fit.tolist(), "aux_values": b_aux.tolist(),
        "first_failed_chord": first_failed, "residual_nonzero": int(len(failed)), "full_chord_eof": True,
        "terminal": terminal, "materialization": witness["materialization"]})
    return {"potential_f": potential_f, "potential_tau": potential_tau, "chord_values": chord_values,
        "tau": tau, "selected_edges": selected_edges, "fit": fit, "residuals": residuals,
        "metadata": metadata, "witness": document("witness", witness)}


def typed_array(value: np.ndarray, dtype: str, shape: tuple[int, ...]) -> tuple[bytes, str, list[int]]:
    require(isinstance(value, np.ndarray) and value.shape == shape, "array_exact_shape")
    if dtype in ("u8", "packed3"):
        require(not np.any(value < 0) and not np.any(value > 2), "array_field_values")
        raw = pack(value.reshape(-1)) if dtype == "packed3" else value.astype(np.uint8).tobytes()
    else:
        require(dtype == "u32le" and not np.any(value < 0) and not np.any(value.astype(np.uint64) > 4294967295), "array_u32_values")
        raw = value.astype("<u4").tobytes()
    return raw, dtype, list(shape)


def json_payload(value: dict[str, Any]) -> tuple[bytes, str, None]:
    return canonical(value), "json", None


def rooted_indices_u32(values: np.ndarray, upper_bound: int) -> np.ndarray:
    """Encode the sole signed root sentinel without int32 scalar coercion.

    Bounds are checked before widening or casting. Only position zero may
    contain -1; every other entry is an actual parent or parent-edge index.
    The caller's signed array is never modified.
    """
    require(isinstance(values, np.ndarray) and values.ndim == 1 and values.size > 0 and
            values.dtype in (np.dtype(np.int32), np.dtype(np.int64)), "rooted_indices_signed_array")
    require(type(upper_bound) is int and 0 < upper_bound <= 4294967295, "rooted_indices_bound_type")
    require(int(values[0]) == -1 and not np.any(values[1:] < 0) and
            not np.any(values[1:] >= upper_bound), "rooted_indices_root_and_range")
    widened = values.astype(np.int64, copy=True)
    widened[0] = 4294967295
    return widened.astype("<u4")


def serialization_selftest() -> dict[str, Any]:
    """Only the production sentinel serializer and its byte/type boundaries."""
    cases = []
    for name, bound in (("parent", VERTICES), ("parent-edge", EDGES)):
        source = np.array([-1, 0, bound - 1], dtype=np.int32)
        original = source.copy()
        converted = rooted_indices_u32(source, bound)
        raw, dtype, shape = typed_array(converted, "u32le", (3,))
        expected = b"\xff\xff\xff\xff" + (0).to_bytes(4, "little") + (bound - 1).to_bytes(4, "little")
        require(raw == expected and dtype == "u32le" and shape == [3] and
                np.array_equal(source, original) and converted.dtype == np.dtype("<u4"),
                "serialization_little_endian_and_input_unchanged")
        cases.append(name + "-int32-root-and-last-index")
    bad_arrays = {
        "nonroot-negative-one": np.array([-1, -1], dtype=np.int32),
        "nonroot-negative-two": np.array([-1, -2], dtype=np.int32),
        "wrong-root": np.array([0, 1], dtype=np.int32),
        "upper-bound": np.array([-1, VERTICES], dtype=np.int32),
        "oversized-int64": np.array([-1, 4294967296], dtype=np.int64),
        "float-array": np.array([-1.0, 1.0]),
        "prewrapped-unsigned": np.array([4294967295, 1], dtype=np.uint32),
        "boolean-array": np.array([True, False]),
        "matrix": np.array([[-1, 1]], dtype=np.int32),
        "empty-array": np.array([], dtype=np.int32),
        "plain-list": [-1, 1],
    }
    for name, value in bad_arrays.items():
        rejected(lambda value=value: rooted_indices_u32(value, VERTICES), name)
        cases.append("reject-" + name)
    rejected(lambda: rooted_indices_u32(np.array([-1, EDGES], dtype=np.int32), EDGES), "edge-upper-bound")
    rejected(lambda: rooted_indices_u32(np.array([-1, 0], dtype=np.int32), float(VERTICES)), "noninteger-bound")
    cases.extend(("reject-edge-upper-bound", "reject-noninteger-bound"))
    return document("serialization-selftest", {"status": "PASS", "cases": cases,
        "production_helper": "rooted_indices_u32", "schema_unchanged": True,
        "old_selftests_executed": 0, "producer_invocations": 0,
        "python": sys.version, "numpy": np.__version__,
        "candidate": False, "cross_checked": False, "verified": False})


def geometry_payloads(geometry: Geometry) -> dict[str, tuple[bytes, str, Any]]:
    parent = rooted_indices_u32(geometry.tree_parent, VERTICES)
    parent_edge = rooted_indices_u32(geometry.tree_edge, EDGES)
    tags = []
    for tag, words in enumerate(ARITH.SEED_OO):
        fox, images = [], []
        for word in words:
            terms, endpoint = linear_fox_terms(geometry, word)
            fox.append([[int(a), int(b), int(c)] for a, b, c in terms]); images.append(endpoint)
        tags.append({"tag": tag, "words": [list(word) for word in words], "images": images, "fox": fox})
    metadata = document("geometry", {"vertices": VERTICES, "edges": EDGES, "tree_edges": VERTICES - 1,
        "chords": CHORDS, "characters": [list(item) for item in CHARACTERS], "actors": [1, 2],
        "qid_order": "parity,k-base3,psl-fastest", "edge_order": "2*q+slot", "tree_order": "positive-bfs-X,Y",
        "chord_order": "edge-id-ascending", "group_convention": "section-left/kernel-right;perm=right[left[i]]",
        "fox_convention": "left-prefix;positive-edge-right-product", "carry_convention": "rotation-left;integer-carry-before-mod3",
        "sentinel": 4294967295, "transport": [[list(geometry.context.transport[tag][label]) for label in CHARACTERS] for tag in range(6)],
        "q0_marking_sha256": FIXED.DATA_PINS["scratchpad/fuda1_a0_rmax_data.g"]["sha256"],
        "psl_elements_sha256": sha(canonical([list(item) for item in geometry.elements])),
        "full_vertex_eof": True, "full_edge_eof": True, "all_phi_edges_checked": True,
        "phi_bijections": 6, "qnorm_right_identity_checked": True})
    return {"next-pos.u32": typed_array(geometry.successor, "u32le", (VERTICES, 2)),
        "prev-pos.u32": typed_array(geometry.inverse_successor, "u32le", (VERTICES, 2)),
        "phi.u32": typed_array(geometry.tag_maps, "u32le", (6, VERTICES)),
        "parent.u32": typed_array(parent, "u32le", (VERTICES,)),
        "parent-edge.u32": typed_array(parent_edge, "u32le", (VERTICES,)),
        "bfs-order.u32": typed_array(geometry.tree_order, "u32le", (VERTICES,)),
        "carry.u8": typed_array(geometry.carry, "u8", (EDGES, 5)),
        "chord-edges.u32": typed_array(geometry.chords, "u32le", (CHORDS,)),
        "geometry.json": json_payload(metadata), "tag-fox.json": json_payload({"tags": tags})}


def section_payloads(section: dict[str, Any]) -> dict[str, tuple[bytes, str, Any]]:
    metadata = document("section", {"rows": 8059, "old_rows": 2014, "new_rows": 6045, "source_lower_trits": LOWER_WIDTH,
        "shared_auxiliaries": 8, "formula": "v548:chi=sum_a<B_a^*lambda,z_i[a]>;kappa(b_i)=chi_i",
        "solve_order": "new-owner-major-descending-original-lead;old-global-descending-embedded-original-lead",
        "free_coordinates": 0, "p1_cache_sha256": BASE.P1_CACHE_SHA256,
        "lower_blob_pin_sha256": BASE.LOWER_BLOB_PIN_SHA256, "p1_passes": 1, "all_equations_checked": 8059,
        "equation_eof": True, "old_arithmetic_replayed": False})
    return {"q.bin": typed_array(section["roots"], "packed3", (4, SOURCE_WIDTH)),
        "p1-values.u8": typed_array(section["p1_values"], "u8", (4, 8059)),
        "chi.u8": typed_array(section["chi"], "u8", (8059,)),
        "equation-values.u8": typed_array(section["equation_values"], "u8", (8059,)),
        "equation-residuals.u8": typed_array(section["equation_residuals"], "u8", (8059,)),
        "beta.u8": typed_array(section["beta"], "u8", (2014,)),
        "kappa.bin": typed_array(section["kappa"], "packed3", (LOWER_WIDTH,)),
        "lead-original.u32": typed_array(section["original"], "u32le", (8059,)),
        "lead-embedded.u32": typed_array(section["embedded"], "u32le", (8059,)),
        "new-solve-order.u32": typed_array(section["new_order"], "u32le", (6045,)),
        "old-solve-order.u32": typed_array(section["old_order"], "u32le", (2014,)),
        "section.json": json_payload(metadata)}


def cochain_payloads(score: np.ndarray, f: np.ndarray, b_aux: np.ndarray) -> dict[str, tuple[bytes, str, Any]]:
    metadata = document("cochain", {"formula": "v548:sum_a q_a Psi2[a]-kappa Psi1", "tags": 6, "components": 2,
        "vertices": VERTICES, "edges": EDGES, "score_eof": True, "edge_eof": True, "shared_eta": True,
        "normalized_aux_rule": "b_aux=-kappa_aux[6:8];no-mod3-division-by18",
        "raw_edge_adapter": "tagged-Fox-left;right-X-XB-qnorm", "physical_mixed_C_used": False})
    return {"score.u8": typed_array(score, "u8", (6, 2, VERTICES)),
        "f.u8": typed_array(f, "u8", (EDGES,)), "b-aux.u8": typed_array(b_aux, "u8", (2,)),
        "cochain.json": json_payload(metadata)}


def tree_payloads(tree: dict[str, Any]) -> dict[str, tuple[bytes, str, Any]]:
    return {"potential-f.u8": typed_array(tree["potential_f"], "u8", (VERTICES,)),
        "potential-tau.u8": typed_array(tree["potential_tau"], "u8", (VERTICES, 5)),
        "chord-values.u8": typed_array(tree["chord_values"], "u8", (CHORDS,)),
        "chord-tau.u8": typed_array(tree["tau"], "u8", (CHORDS, 5)),
        "chord-residuals.u8": typed_array(tree["residuals"], "u8", (CHORDS,)),
        "selected-chords.u32": typed_array(tree["selected_edges"], "u32le", (5,)),
        "fit.u8": typed_array(tree["fit"], "u8", (5,)),
        "witness.json": json_payload(tree["witness"]), "tree.json": json_payload(tree["metadata"])}


def stage_manifest(stage: str, owner_sha: str, snapshot_sha: str, inputs: dict[str, str],
                   payloads: dict[str, tuple[bytes, str, Any]]) -> dict[str, Any]:
    return document("stage-manifest", {"stage": stage, "owner_sha256": owner_sha, "snapshot_sha256": snapshot_sha,
        "inputs": inputs, "files": [{"file": name, "bytes": len(raw), "sha256": sha(raw), "dtype": dtype, "shape": shape}
            for name, (raw, dtype, shape) in sorted(payloads.items())]})


def compare_complete_stage(root: Path, payloads: dict[str, tuple[bytes, str, Any]], manifest: dict[str, Any]) -> list[str]:
    """Compare every full array, including the last chord, before reporting drift."""
    require(root.is_dir() and not root.is_symlink(), "stage_directory")
    errors = []
    expected = {name: raw for name, (raw, _, _) in payloads.items()}
    expected["manifest.json"] = canonical(manifest)
    if set(item.name for item in root.iterdir()) != set(expected):
        errors.append("exact-roster")
    for name, wanted in sorted(expected.items()):
        item = root / name
        if not item.is_file() or item.is_symlink():
            errors.append(name + ":missing-or-kind"); continue
        # Read at most the expected payload plus one byte; an extra byte is a
        # strict EOF failure, never an accepted shortened or extended array.
        with item.open("rb") as stream:
            actual = stream.read(len(wanted) + 1)
        if actual != wanted:
            errors.append(name + ":full-bytes-or-eof")
    return errors


def accepted_payloads(root: Path, manifest: dict[str, Any], expected_names: set[str]) -> dict[str, bytes]:
    REFINE.check_seal(manifest)
    files = manifest.get("files")
    require(isinstance(files, list) and [item["file"] for item in files] == sorted(expected_names) and
            set(item.name for item in root.iterdir()) == expected_names | {"manifest.json"}, "accepted_refinement_exact_payload_roster")
    return {item["file"]: fixed(root, item["file"], (item["bytes"], item["sha256"])) for item in files}


def refinement_semantics(metadata: dict[str, Any]) -> None:
    """Production and actual-parent canary share this schema-aware metadata join."""
    head, start, terminal, steps = [metadata[key] for key in ("head", "start", "terminal", "steps")]
    previous_head, previous_manifest, previous_target = start["state_head"], None, start["target_remainder_sha256"]
    count = head["completed_steps"]
    require(type(count) is int and 0 <= count <= 32 and len(steps) == count and head["kind"] == "Separator", "refinement_input_separator_prefix")
    for number, item in enumerate(steps, 1):
        manifest, result, instruction, payloads = [item[key] for key in ("manifest", "result", "instruction", "payloads")]
        require("sha256" not in instruction and "rolling_sha256" in instruction, "refinement_instruction_rolling_only")
        require(sorted(result["target"]) == ["parent_remainder_sha256", "remainder_sha256", "scalar"], "refinement_target_plain_keys")
        unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
        new_head = sha(bytes.fromhex(previous_head) + canonical(unsigned))
        require(manifest["step"] == result["step"] == instruction["step"] == number and
                manifest["parent_state_head"] == result["parent_state_head"] == instruction["predecessor"] == previous_head and
                manifest["state_head"] == result["state_head"] == instruction["rolling_sha256"] == new_head and
                manifest["predecessor_step_manifest_sha256"] == previous_manifest and
                manifest["owner_sha256"] == result["owner_sha256"] == head["owner_sha256"] and
                manifest["kind"] == result["kind"] == "Separator" and
                manifest["rank"] == result["rank_after"] == instruction["rank"] == start["rank"] + number and
                result["rank_before"] == start["rank"] + number - 1 and
                manifest["generation"] == result["generation_after"] == instruction["generation"] == start["generation"] + number and
                result["generation_before"] == instruction["offer"] == start["generation"] + number - 1,
                "refinement_step_state_chain")
        require(result["target"]["parent_remainder_sha256"] == previous_target and
                result["target"]["remainder_sha256"] == instruction["target_remainder_sha256"] == sha(payloads["target-remainder.bin"]) and
                result["target"]["scalar"] == instruction["target_scalar"] and instruction["target_scalar"] in (0, 1, 2) and
                result["separator"]["lambda_sha256"] == sha(payloads["lambda.bin"]) and
                result["pivot"]["normalized_sha256"] == instruction["physical_sha256"] == sha(payloads["physical-normalized.bin"]) and
                result["pivot"]["lead"] == instruction["lead"] and result["pivot"]["scale"] == instruction["sigma"] and
                result["pivot"]["reductions"] == instruction["physical_reductions"] and
                instruction["physical_offset"] == (start["rank"] + number - 1) * ROW_BYTES,
                "refinement_target_and_payload_chain")
        require(manifest["packet_manifest_sha256"] == result["packet_manifest_sha256"] == instruction["packet_manifest_sha256"] ==
                head["packet_manifest_sha256"] and instruction["canonical_index_sha256"] == head["canonical_index_sha256"] and
                result["selection"] == instruction["selected"] and
                result["materialization_sha256"] == instruction["materialization_sha256"] == item["payload_sha256"]["materialization.json"] and
                instruction["source_d_sha256"] == item["payload_sha256"]["source-d.bin"], "refinement_materialization_metadata")
        previous_head, previous_manifest, previous_target = new_head, item["manifest_sha256"], sha(payloads["target-remainder.bin"])
    require(head["state_head"] == terminal["state_head"] == previous_head and head["step_manifest_sha256"] == previous_manifest and
            head["rank"] == terminal["rank"] == start["rank"] + count and
            head["generation"] == terminal["generation"] == start["generation"] + count and
            terminal["completed_steps"] == count and head["rank"] >= 1359,
            "refinement_final_state_join")


def accepted_refinement_metadata(args: argparse.Namespace) -> dict[str, Any]:
    """Authenticated saved arrays and chains; no accepted scan/insert replay."""
    require(REFINEMENT_ARTIFACT is not None and REFINEMENT_FILES, "observed_refinement_pins_required")
    objects = {name: REFINE.json_bytes(fixed(args.refinement_root, name, pin)) for name, pin in REFINEMENT_FILES.items()}
    needed = ("output/HEAD", "output/start.json", "output/owner.json", "output/source.json", "output/canonical-index.json",
              "output/result.json", "checker-result.json", "source-receipt.json")
    require(all(name in objects for name in needed), "refinement_entry_pin_closure")
    head, start, owner, source, index, terminal, checker, source_receipt = [objects[name] for name in needed]
    for value, suffix in ((head, "head"), (start, "start"), (owner, "owner"), (source, "source"),
                          (index, "canonical-p1-index"), (terminal, "result")):
        REFINE.check_seal(value)
        require(value["schema"] == REFINE.SCHEMA + "." + suffix, "accepted_refinement_schema:" + suffix)
    require(head["kind"] == "Separator" and terminal["status"] == checker["status"] == "PASS" and
            terminal["terminal"] == checker["terminal"] and terminal["terminal"] in ("ROOT_ORIGINS_ZERO", "UNKNOWN_CAP", "UNKNOWN_RESOURCE") and
            checker["schema"] == REFINE.SCHEMA + ".checker-result" and
            head["completed_steps"] == checker["completed_steps"] == checker["prefix_steps_replayed"] and
            head["rank"] == checker["rank"] and head["generation"] == terminal["generation"] == checker["generation"] and
            head["state_head"] == checker["state_head"] and
            terminal["head_sha256"] == checker["head_sha256"] == REFINEMENT_FILES["output/HEAD"][1] and
            checker["result_sha256"] == REFINEMENT_FILES["output/result.json"][1] and
            head["owner_sha256"] == terminal["owner_sha256"] == checker["owner_sha256"] == REFINEMENT_FILES["output/owner.json"][1] and
            head["start_sha256"] == REFINEMENT_FILES["output/start.json"][1] and
            head["source_sha256"] == REFINEMENT_FILES["output/source.json"][1] and
            head["canonical_index_sha256"] == checker["canonical_index_sha256"] == REFINEMENT_FILES["output/canonical-index.json"][1] and
            head["producer_sha256"] == source["producer_sha256"] == REFINEMENT_PRODUCER_SHA and
            source["data"] == FIXED.DATA_PINS, "accepted_refinement_authority")
    require(all(value["cross_checked"] is False and value["verified"] is False for value in (terminal, checker, source_receipt)),
            "accepted_refinement_assurance")
    require(start["rank"] == REFINE.START_RANK and start["generation"] == REFINE.START_GENERATION and
            start["state_head"] == REFINE.START_HEAD and start["lambda_sha256"] == REFINE.START_LAMBDA and
            start["target_remainder_sha256"] == REFINE.START_TARGET, "accepted_refinement_base_snapshot")
    steps = []
    step_names = {"source-d.bin", "source-full-top.bin", "materialization.json", "physical-raw.bin", "physical-remainder.bin",
                  "physical-normalized.bin", "target-remainder.bin", "lambda.bin", "instruction.json", "result.json"}
    for number in range(1, head["completed_steps"] + 1):
        boundary("accepted_refinement_step_metadata", step=number)
        root = args.refinement_root / "output/steps" / f"{number:06d}"
        manifest = REFINE.read_json(root, "manifest.json")
        payloads = accepted_payloads(root, manifest, step_names)
        result, instruction = REFINE.json_bytes(payloads["result.json"]), REFINE.json_bytes(payloads["instruction.json"])
        REFINE.check_seal(result)
        require(manifest["schema"] == REFINE.SCHEMA + ".step-manifest" and result["schema"] == REFINE.SCHEMA + ".step-result" and
                instruction["schema"] == REFINE.SCHEMA + ".instruction", "accepted_refinement_step_schemas")
        require(all(len(payloads[name]) == ROW_BYTES for name in ("physical-raw.bin", "physical-remainder.bin", "physical-normalized.bin",
                "target-remainder.bin", "lambda.bin")) and len(payloads["source-d.bin"]) == 9072 and
                len(payloads["source-full-top.bin"]) == 36288, "accepted_refinement_payload_sizes")
        retained = {name: payloads[name] for name in ("physical-normalized.bin", "target-remainder.bin", "lambda.bin", "instruction.json", "result.json")}
        steps.append({"manifest": manifest, "manifest_sha256": sha(canonical(manifest)), "result": result,
            "result_sha256": sha(payloads["result.json"]), "instruction": instruction, "payloads": retained,
            "payload_sha256": {name: sha(raw) for name, raw in payloads.items()}})
        del payloads
    metadata = {"objects": objects, "head": head, "start": start, "owner": owner, "source": source, "index": index,
        "terminal": terminal, "checker": checker, "steps": steps}
    refinement_semantics(metadata)
    scan_names = {"result.json"} | {f"{stem}-c{a}.{extension}" for a in range(4) for stem, extension in
        (("root", "bin"), ("children", "bin"), ("seeds", "u8"), ("actors", "u8"), ("p1", "u8"), ("actor-lower", "u8"))}
    cached = head["current_scan_manifest_sha256"]
    last_scan = head["completed_steps"] if cached is not None else head["completed_steps"] - 1
    final_scan = None
    for number in range(last_scan + 1):
        root = args.refinement_root / "output/scans" / f"{number:06d}"
        manifest = REFINE.read_json(root, "manifest.json")
        payloads = accepted_payloads(root, manifest, scan_names)
        value = REFINE.json_bytes(payloads["result.json"]); REFINE.check_seal(value)
        expected_head = start["state_head"] if number == 0 else steps[number - 1]["manifest"]["state_head"]
        expected_lambda = start["lambda_sha256"] if number == 0 else sha(steps[number - 1]["payloads"]["lambda.bin"])
        require(manifest["schema"] == REFINE.SCHEMA + ".scan-manifest" and value["schema"] == REFINE.SCHEMA + ".scan" and
                manifest["scan"] == value["scan"] == number and manifest["state_head"] == value["state_head"] == expected_head and
                manifest["lambda_sha256"] == value["lambda_sha256"] == expected_lambda and
                manifest["owner_sha256"] == value["owner_sha256"] == head["owner_sha256"] and
                manifest["canonical_index_sha256"] == value["canonical_index_sha256"] == head["canonical_index_sha256"],
                "accepted_refinement_scan_metadata")
        digest = sha(canonical(manifest))
        if number < head["completed_steps"]:
            step = steps[number]
            require(digest == step["manifest"]["scan_manifest_sha256"] == step["result"]["scan_manifest_sha256"] ==
                    step["instruction"]["scan_manifest_sha256"] and value["first_hit"] == step["instruction"]["selected"],
                    "accepted_refinement_selected_scan_join")
        else:
            require(digest == cached == terminal["scan_manifest_sha256"] and value == terminal["scan"], "accepted_current_cached_scan")
            final_scan = {"manifest": manifest, "result": value,
                "roots": [payloads[f"root-c{a}.bin"] for a in range(4)], "p1_values": [payloads[f"p1-c{a}.u8"] for a in range(4)]}
        boundary("accepted_refinement_scan_hashes", scan=number)
    require(checker["complete_scans_replayed"] == last_scan + 1, "accepted_complete_scan_count")
    if cached is None:
        require(terminal["scan_manifest_sha256"] is None and terminal["scan"] is None, "accepted_absent_cached_scan")
    metadata["current_scan"] = final_scan
    return metadata


def refinement_layout(metadata: dict[str, Any]) -> dict[str, Any]:
    head, start = metadata["head"], metadata["start"]
    rows = []
    for item in metadata["steps"]:
        manifest, result, instruction, payloads = [item[key] for key in ("manifest", "result", "instruction", "payloads")]
        rows.append({"step": manifest["step"], "manifest_sha256": item["manifest_sha256"], "result_sha256": item["result_sha256"],
            "instruction_sha256": sha(payloads["instruction.json"]), "target_sha256": sha(canonical(result["target"])),
            "state_head": manifest["state_head"], "parent_state_head": manifest["parent_state_head"], "rank": manifest["rank"],
            "generation": manifest["generation"], "lead": instruction["lead"], "target_scalar": instruction["target_scalar"],
            "physical_normalized_sha256": sha(payloads["physical-normalized.bin"]), "lambda_sha256": sha(payloads["lambda.bin"]),
            "target_remainder_sha256": sha(payloads["target-remainder.bin"])})
    return document("refinement-parent-layout", {"artifact": REFINEMENT_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(REFINEMENT_FILES.items())],
        "completed_steps": head["completed_steps"], "terminal": metadata["terminal"]["terminal"], "rank": head["rank"],
        "generation": head["generation"], "state_head": head["state_head"],
        "lambda_sha256": rows[-1]["lambda_sha256"] if rows else start["lambda_sha256"],
        "target_remainder_sha256": rows[-1]["target_remainder_sha256"] if rows else start["target_remainder_sha256"],
        "steps": rows, "old_arithmetic_replayed": False})


def current_snapshot(args: argparse.Namespace, metadata: dict[str, Any]) -> dict[str, Any]:
    boundary("accepted_source_snapshot_load")
    state = REFINE.load_accepted_start(args)
    same(metadata["start"], REFINE.expected_start(state), "refinement_inherited_start")
    index = metadata["index"]
    require(index["rows"] == len(index["references"]) == 8059 and index["p1_manifest_sha256"] == BASE.P1_MANIFEST_SHA256 and
            index["cache_sha256"] == BASE.P1_CACHE_SHA256 and index["instruction_sha256"] == BASE.P1_INSTRUCTION_SHA256 and
            all(item["node"] == number for number, item in enumerate(index["references"])), "accepted_canonical_index_input")
    previous_target = state["start_target"].copy()
    for item in metadata["steps"]:
        instruction = item["instruction"]
        normalized = unpack(item["payloads"]["physical-normalized.bin"], WIDTH)
        require(type(instruction["lead"]) is int and 0 <= instruction["lead"] < WIDTH and normalized[instruction["lead"]] == 1 and
                all(normalized[pivot["lead"]] == 0 for pivot in state["pivots"]), "accepted_refinement_physical_triangularity")
        state["saved_rows"].append(item["payloads"]["physical-normalized.bin"])
        state["pivots"].append({"offer": instruction["offer"], "lead": instruction["lead"],
            "physical_offset": instruction["physical_offset"], "coefficient_offset": None, "rolling_sha256": instruction["rolling_sha256"]})
        previous_target = state["start_target"]
        state["start_target"] = unpack(item["payloads"]["target-remainder.bin"], WIDTH)
        state["start_lambda"] = unpack(item["payloads"]["lambda.bin"], WIDTH)
    functional, target = state["start_lambda"], state["start_target"]
    rank = metadata["head"]["rank"]
    require(len(state["pivots"]) == rank and len(state["saved_rows"]) == rank - 1354 and
            np.any(target) and all(target[pivot["lead"]] == 0 for pivot in state["pivots"]), "current_separator_snapshot_type")
    measured = []
    boundary("current_snapshot_all_row_sweep", rank=rank)
    with path(args.state_root, "state/physical.bin").open("rb", buffering=1 << 20) as stream:
        for row_id in range(1354):
            raw = stream.read(ROW_BYTES)
            require(len(raw) == ROW_BYTES, "current_base_row_eof")
            measured.append(dot(functional, unpack(raw, WIDTH)))
        require(stream.read(1) == b"", "current_base_exact_eof")
    measured.extend(dot(functional, unpack(raw, WIDTH)) for raw in state["saved_rows"])
    parent_dot, target_dot = dot(functional, previous_target), dot(functional, target)
    require(len(measured) == rank and not any(measured) and parent_dot == target_dot == 1, "current_all_rows_and_both_target_dots")
    state["direct_pairing"] = {"rows": rank, "row_pairings_sha256": sha(bytes(measured)), "lambda_pivots": 0,
        "lambda_parent_remainder": parent_dot, "lambda_new_remainder": target_dot}
    state["accepted_refinement"] = metadata
    boundary("current_snapshot_authenticated", rank=rank)
    return state


def start_and_owner(state: dict[str, Any], tables: list[Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    metadata = state["accepted_refinement"]
    same(metadata["owner"], REFINE.expected_owner(state, tables), "accepted_refinement_actual_owner")
    inherited = ("p1_parent", "task554_parent", "task712_parent", "task712_manifest_sha256",
                 "word_dictionary_sha256", "relator_dictionary_sha256")
    owner = document("owner", {"formula_id": FORMULA, "scope": SCOPE,
        "accepted_refinement_owner_sha256": REFINEMENT_FILES["output/owner.json"][1],
        "accepted_refinement_head_sha256": REFINEMENT_FILES["output/HEAD"][1],
        **{key: metadata["owner"][key] for key in inherited}})
    parents = list(metadata["start"]["accepted_target_derivation_parents"])
    for item in metadata["steps"]:
        parents.append({"role": "refinement-step-" + str(item["manifest"]["step"]), "manifest_sha256": item["manifest_sha256"],
            "result_sha256": item["result_sha256"], "target_sha256": sha(canonical(item["result"]["target"])),
            "state_head": item["manifest"]["state_head"]})
    derived = {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e",
        "accepted_target_derivation_parents": parents, "identity_convention": {
            "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",
            "packet_and_refinement_steps": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row"},
        "new_target_steps_executed": 0}
    start = document("start", {"kind": "Separator", "rank": metadata["head"]["rank"], "generation": metadata["head"]["generation"],
        "state_head": metadata["head"]["state_head"], "lambda_sha256": sha(pack(state["start_lambda"])),
        "target_remainder_sha256": sha(pack(state["start_target"])), "accepted_refinement_layout": refinement_layout(metadata),
        "accepted_target_derivation_parents": parents, "lambda_rho2": derived, "direct_pairing": state["direct_pairing"]})
    return start, owner


def producer_source_receipt() -> dict[str, Any]:
    directory = Path(__file__).resolve().parent
    modules = {**FIXED.PRODUCER_LINEAGE, "d972_r07_fixed_root_packet_loop_v2.py":
        "e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6",
        "d972_r07_full_origin_refinement_v1.py": REFINEMENT_PRODUCER_SHA}
    for name, expected in modules.items():
        item = directory / name
        require(item.is_file() and not item.is_symlink() and sha(item.read_bytes()) == expected, "producer_retained_module_pin")
    item = directory / "d972_r07_section_cochain_oracle_v1.py"
    require(item.is_file() and not item.is_symlink(), "producer_current_source_file")
    return document("source", {"producer_sha256": sha(item.read_bytes()), "modules": modules,
        "data": FIXED.DATA_PINS, "python": sys.version, "numpy": np.__version__})


def check_source_data() -> None:
    base = Path(__file__).resolve().parents[1]
    for name, descriptor in FIXED.DATA_PINS.items():
        raw = fixed(base, name, (descriptor["bytes"], descriptor["sha256"]))
        require(len(raw) == descriptor["bytes"], "exact_raw_source_data")


def expected_result(start: dict[str, Any], owner_sha: str, source_sha: str, stage_hashes: dict[str, str],
                    tree: dict[str, Any]) -> dict[str, Any]:
    terminal = tree["metadata"]["terminal"]
    return document("result", {"status": "PASS", "terminal": terminal, "materialization": tree["witness"]["materialization"],
        "owner_sha256": owner_sha, "snapshot_sha256": sha(canonical(start)), "source_sha256": source_sha,
        **{key: start[key] for key in ("state_head", "rank", "generation", "lambda_sha256", "target_remainder_sha256")},
        "stage_manifests": stage_hashes, "witness_sha256": sha(canonical(tree["witness"])), "lambda_rho2": start["lambda_rho2"],
        "direct_pairing": start["direct_pairing"], "complete_source_and_conn_premises_retained": True,
        "all8059_section_equalities": True, "all54433_chords_checked": True, "normalized_auxiliary_tests": 2,
        "physical_appends": 0, "grade2_member": "NOT_DECIDED",
        "grade2_nonmember": "CANDIDATE_ONLY" if terminal == "COMPLETE_ZERO_CANDIDATE" else "NOT_DECIDED",
        "full_A0": False, "candidate": True, "cross_checked": False, "verified": False})


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    root = args.candidate_root
    require(root.is_dir() and not root.is_symlink(), "candidate_directory")
    check_source_data()
    source = producer_source_receipt()
    metadata = accepted_refinement_metadata(args)
    state = current_snapshot(args, metadata)
    tables = REFINE.load_tables(args)
    start, owner = start_and_owner(state, tables)
    owner_sha, snapshot_sha, source_sha = sha(canonical(owner)), sha(canonical(start)), sha(canonical(source))
    context, _ = BASE.checker_source_context()
    boundary("geometry_begin")
    geometry = Geometry(context)
    roots, p1_values = current_roots_and_contractions(args, state, tables, state["start_lambda"])
    if metadata["current_scan"] is not None:
        for character in range(4):
            require(pack(roots[character]) == metadata["current_scan"]["roots"][character], "current_scan_fresh_root_join")
            previous = np.frombuffer(metadata["current_scan"]["p1_values"][character], dtype=np.uint8)
            require(previous.size == 5 * 8059 and np.array_equal(previous.reshape(5, 8059)[0], p1_values[character]),
                    "current_scan_fresh_P1_join")
    section = current_section(args, state, roots, p1_values)
    score, anchor = source_scores(geometry, roots, section["kappa"])
    f, b_aux, _ = raw_edge_cochain(geometry, score, section["kappa"])
    tree = complete_tree_test(geometry, f, b_aux)
    all_payloads = {"geometry": geometry_payloads(geometry), "section": section_payloads(section),
        "cochain": cochain_payloads(score, f, b_aux), "tree": tree_payloads(tree)}
    stage_hashes, errors = {}, []
    for name in ("geometry", "section", "cochain", "tree"):
        dependencies = () if name in ("geometry", "section") else (("geometry", "section") if name == "cochain" else ("geometry", "cochain"))
        manifest = stage_manifest(name, owner_sha, snapshot_sha, {key: stage_hashes[key] for key in dependencies}, all_payloads[name])
        stage_hashes[name] = sha(canonical(manifest))
        errors.extend(name + "/" + error for error in compare_complete_stage(root / name, all_payloads[name], manifest))
        boundary("full_stage_arrays_compared", stage=name, payloads=len(all_payloads[name]))
    result = expected_result(start, owner_sha, source_sha, stage_hashes, tree)
    top = {"owner.json": canonical(owner), "start.json": canonical(start), "source.json": canonical(source), "result.json": canonical(result)}
    manifest = document("manifest", {"owner_sha256": owner_sha, "snapshot_sha256": snapshot_sha, "source_sha256": source_sha,
        "result_sha256": sha(top["result.json"]), "stage_manifests": stage_hashes,
        "files": [{"file": name, "bytes": len(raw), "sha256": sha(raw)} for name, raw in sorted(top.items())],
        "file_roster": ["cochain", "geometry", "manifest.json", "owner.json", "result.json", "section", "source.json", "start.json", "tree"],
        "candidate": True, "cross_checked": False, "verified": False})



    require(sorted(item.name for item in root.iterdir()) == manifest["file_roster"], "complete_candidate_top_roster")
    top["manifest.json"] = canonical(manifest)
    for name, wanted in top.items():
        with path(root, name).open("rb") as stream:
            actual = stream.read(len(wanted) + 1)
        if actual != wanted:
            errors.append(name + ":full-bytes-or-eof")
    require(not errors, "all_array_and_metadata_comparison:" + ",".join(errors))
    boundary("terminal", status="PASS", terminal=result["terminal"])
    return document("checker-result", {"status": "PASS", "terminal": result["terminal"], "materialization": result["materialization"],
        "owner_sha256": owner_sha, "snapshot_sha256": snapshot_sha, "result_sha256": sha(canonical(result)),
        "manifest_sha256": sha(canonical(manifest)), "stage_manifests": stage_hashes, "rank": start["rank"],
        "generation": start["generation"], "state_head": start["state_head"], "lambda_rho2": start["lambda_rho2"],
        "direct_pairing": start["direct_pairing"], "all_stage_arrays_compared": True, "section_equalities": 8059,
        "chords_checked": CHORDS, "auxiliary_tests": 2, "new_physical_appends": 0, "old_scans_numerically_replayed": 0,
        "accepted_refinement_artifact": REFINEMENT_ARTIFACT, "source_score_anchor": anchor,
        "checker_sha256": sha(Path(__file__).read_bytes()), "checker_lineage": {**FIXED.LINEAGE,
            "check_d972_r07_fixed_root_packet_loop_v2.py": REFINE.FIXED_CHECKER_SHA,
            "check_d972_r07_full_origin_refinement_v1.py": REFINE_CHECKER_SHA},
        "source_data_pins": FIXED.DATA_PINS, "python": sys.version, "numpy": np.__version__,
        "candidate": True, "cross_checked": False, "verified": False})


def rejected(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError("section_cochain_checker:mutation_accepted:" + label)


def parent_layout_selftest(args: argparse.Namespace) -> dict[str, Any]:
    inherited = REFINE.parent_layout_selftest(args)
    metadata = accepted_refinement_metadata(args)
    same(metadata["start"]["parent_layout"], inherited["parent_layout"], "actual_refinement_legacy_layout")
    same(metadata["start"]["packet_parent_layout"], inherited["accepted_packet_layout"], "actual_refinement_packet_layout")
    steps = metadata["steps"]
    require(steps, "actual_refinement_nonempty_parent_fixture")
    first = steps[0]
    mutations = [
        ("refinement-instruction-generic-seal", {**metadata, "steps": [
            {**first, "instruction": {**first["instruction"], "sha256": "0" * 64}}, *steps[1:]]}),
        ("refinement-target-generic-seal", {**metadata, "steps": [
            {**first, "result": {**first["result"], "target": {**first["result"]["target"], "sha256": "0" * 64}}}, *steps[1:]]}),
        ("refinement-target-parent", {**metadata, "steps": [
            {**first, "result": {**first["result"], "target": {**first["result"]["target"], "parent_remainder_sha256": "0" * 64}}}, *steps[1:]]}),
        ("refinement-step-chain", {**metadata, "steps": [
            {**first, "manifest": {**first["manifest"], "parent_state_head": "0" * 64}}, *steps[1:]]}),
        ("refinement-final-head", {**metadata, "head": {**metadata["head"], "state_head": "0" * 64}}),
    ]
    names = list(inherited["rejected_cases"])
    for label, mutated in mutations:
        rejected(lambda: refinement_semantics(mutated), label); names.append(label)
    refinement_semantics(metadata)
    return document("parent-layout-selftest", {"status": "PASS", "metadata_only": True,
        "parent_layout": inherited["parent_layout"], "accepted_packet_layout": inherited["accepted_packet_layout"],
        "accepted_refinement_layout": refinement_layout(metadata), "rejected_cases": names,
        "cross_checked": False, "verified": False})


def retained_forward_edge_anchor(geometry: Geometry, edge: int, roots: np.ndarray, kappa: np.ndarray) -> int:
    """Canary-only retained forward source path, independent of new score lookup.

    This uses the accepted checker polynomial primitive solely to test the
    new ordinary-group route and raw-edge flattening. Production cochains
    never call this helper or the closed-word qnorm.
    """
    qid, slot = divmod(edge, 2)
    d0 = np.zeros((4, 6, 2, 504), dtype=np.int64)
    d1 = np.zeros((4, 6, 2, 3, 504), dtype=np.int64)
    d2 = np.zeros((4, 6, 2, 6, 504), dtype=np.int64)
    auxiliary = np.zeros(8, dtype=np.int64)
    x = geometry.context.images[0]
    b = ARITH._checker_seed_affine_inv(ARITH._checker_seed_affine_mul(geometry.context.images[1], x))
    for tag, words in enumerate(ARITH.SEED_OO):
        mapped = int(geometry.tag_maps[tag, qid]); e = mapped // (504 * 27)
        phi_q = (geometry.elements[mapped % 504], *CHARACTERS[e], KERNEL[(mapped // 504) % 27])
        terms, _ = ARITH._checker_seed_affine_fox(words[slot], geometry.context.images)
        normalized = []
        for (component, prefix), coefficient in terms.items():
            left = ARITH._checker_seed_affine_mul(phi_q, prefix)
            if component == 0:
                right_x = ARITH._checker_seed_affine_mul(left, x)
                normalized.extend(((0, right_x, -coefficient), (1, ARITH._checker_seed_affine_mul(right_x, b), -coefficient)))
                auxiliary[tag] += coefficient
            else:
                normalized.append((1, left, coefficient))
        for component, vertex, coefficient in normalized:
            polynomial = ARITH._checker_seed_e_poly(vertex[3]).astype(np.int64)
            p = geometry.positions[vertex[0]]
            for character, label in enumerate(CHARACTERS):
                transported = geometry.context.transport[tag][label]
                sign = 1 if (transported[0] * vertex[1] + transported[1] * vertex[2]) % 2 == 0 else -1
                d0[character, tag, component, p] += coefficient * sign * polynomial[0]
                d1[character, tag, component, :, p] += coefficient * sign * polynomial[1:4]
                d2[character, tag, component, :, p] += coefficient * sign * polynomial[4:]
    lower = np.concatenate((d0.reshape(-1), d1.reshape(-1), auxiliary)) % 3
    return int((np.sum(roots.astype(np.int64) * (d2.reshape(4, SOURCE_WIDTH) % 3), dtype=np.int64) -
                np.sum(kappa.astype(np.int64) * lower, dtype=np.int64)) % 3)


def selftest() -> dict[str, Any]:
    """Four changed-interface gates; no old closure/packet numerical suite."""
    rows = np.array([[0, 0, 1, 0, 0, 0, 1], [1, 0, 2, 0, 0, 0, 2],
                     [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0]], dtype=np.uint8)
    rhs = np.array([1, 0, 2, 1], dtype=np.uint8)
    records = [(0, 2), (1, 0), (2, 6), (3, 3)]
    solved, order = interpolate_rows(7, records, rhs, lambda row: rows[row])
    require(order == [2, 3, 0, 1] and np.array_equal(rows.astype(np.int64) @ solved % 3, rhs) and
            int(solved[6]) == 2 and not np.any(solved[[1, 4, 5]]), "nonmonotone_original_lead_shared_aux_canary")
    wrong = np.zeros(7, dtype=np.uint8)
    for row_id, lead in reversed(records):
        wrong[lead] = (int(rhs[row_id]) - dot(wrong, rows[row_id])) % 3
    require(not np.array_equal(rows.astype(np.int64) @ wrong % 3, rhs), "reverse_row_id_is_not_dual_solve")
    tests = [{"name": "nonmonotone-original-lead-and-one-shared-aux", "status": "PASS", "rows": 4, "solve_order": order}]
    check_source_data()
    context, _ = BASE.checker_source_context()
    geometry = Geometry(context)
    x, y = geometry.generators
    require(geometry.multiply(x, y) != geometry.multiply(y, x) and
            geometry.successor[x, 1] == geometry.multiply(x, y) and geometry.successor[y, 0] == geometry.multiply(y, x),
            "noncommuting_left_right_actual_geometry")
    tests.append({"name": "actual-right-graph-six-tags-and-full36-marking", "status": "PASS", "vertices": VERTICES, "edges": EDGES})
    roots = np.zeros((4, SOURCE_WIDTH), dtype=np.uint8)
    kappa = np.zeros(LOWER_WIDTH, dtype=np.uint8)
    for character in range(4):
        roots[character, 0] = 1 + (character & 1)
        kappa[character * 6048] = 1 + ((character >> 1) & 1)
        kappa[24192 + character * 18144] = 2 if character < 2 else 1
    kappa[96768] = 1; kappa[96774] = 2
    score, _ = source_scores(geometry, roots, kappa)
    f, b_aux, _ = raw_edge_cochain(geometry, score, kappa)
    lower_only = kappa.copy(); lower_only[-8:] = 0
    lower_score, _ = source_scores(geometry, np.zeros_like(roots), lower_only)
    lower_f, _, _ = raw_edge_cochain(geometry, lower_score, lower_only)
    require(np.any(lower_f) and b_aux.tolist() == [1, 0], "actual_raw_edge_lower_and_shared_eta_canary")
    sample = sorted({0, 1, 2 * x, 2 * x + 1, 2 * y, 2 * y + 1, EDGES - 1,
                     *[int(edge) for edge in np.flatnonzero(lower_f)[:3]],
                     *[2 * ((parity * 27 + 9 * k0) * 504 + geometry.inverse(x) % 504)
                       for parity in range(4) for k0 in range(3)]})
    for edge in sample:
        require(retained_forward_edge_anchor(geometry, edge, roots, kappa) == int(f[edge]), "actual_nonclosed_raw_edge_forward_pairing")
    cancellation, endpoint = linear_fox_terms(geometry, (1, -1, 2))
    require(endpoint == y and cancellation == [(1, 0, 1)], "nonclosed_signed_fox_cancellation")
    tests.append({"name": "ordinary27-mixed-source-nonclosed-edges-and-eta", "status": "PASS", "sample_edges": sample,
        "closed_word_qnorm_called": False, "retained_forward_anchor_only_in_canary": True})
    zero = complete_tree_test(geometry, geometry.carry[:, 0].copy(), np.zeros(2, dtype=np.uint8))
    require(zero["metadata"]["terminal"] == "COMPLETE_ZERO_CANDIDATE", "carry_functional_complete_zero_canary")
    selected_set = set(int(item) for item in zero["selected_edges"])
    chosen = next(int(edge) for edge in reversed(geometry.chords) if int(edge) not in selected_set)
    altered = geometry.carry[:, 0].copy(); altered[chosen] = (int(altered[chosen]) + 1) % 3
    violated = complete_tree_test(geometry, altered, np.zeros(2, dtype=np.uint8))
    require(violated["witness"]["kind"] == "chord" and violated["witness"]["failed_chord"] == chosen and
            violated["witness"]["scalar"] == 1 and len(violated["witness"]["cycles"]) == 6, "late_chord_six_cycle_witness")
    payloads = tree_payloads(zero)
    manifest = stage_manifest("tree", "0" * 64, "1" * 64, {"geometry": "2" * 64, "cochain": "3" * 64}, payloads)
    with tempfile.TemporaryDirectory(prefix="r07-section-cochain-checker-") as temporary:
        root = Path(temporary)
        for name, (raw, _, _) in payloads.items():
            (root / name).write_bytes(raw)
        (root / "manifest.json").write_bytes(canonical(manifest))
        require(not compare_complete_stage(root, payloads, manifest), "new_stage_serialization_roundtrip")
        tail = bytearray(payloads["chord-residuals.u8"][0]); tail[-1] = (tail[-1] + 1) % 3
        (root / "chord-residuals.u8").write_bytes(tail)
        (root / "chord-tau.u8").write_bytes(payloads["chord-tau.u8"][0][:-1])
        errors = compare_complete_stage(root, payloads, manifest)
        require("chord-residuals.u8:full-bytes-or-eof" in errors and "chord-tau.u8:full-bytes-or-eof" in errors,
                "both_late_mutation_and_false_eof_rejected")
    tests.append({"name": "all-chord-fit-witness-tail-mutation-and-false-EOF", "status": "PASS", "chords": CHORDS,
        "late_witness_edge": chosen, "simultaneous_array_errors_detected": len(errors)})
    return document("selftest", {"status": "PASS", "tests": tests, "candidate": True, "cross_checked": False, "verified": False})


def main() -> int:
    global BEGIN, DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("state-root", "delta-root", "seed34-root", "packet-root", "refinement-root", "prepare-root", "p1-root", "task712-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--candidate-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-seconds", type=float, default=1800.0)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--parent-layout-selftest", action="store_true")
    parser.add_argument("--serialization-selftest", action="store_true")
    args = parser.parse_args()
    BEGIN = time.monotonic()
    code = 0
    try:
        require(args.max_seconds > 0 and np.isfinite(args.max_seconds), "positive_finite_deadline")
        DEADLINE = BEGIN + args.max_seconds
        REFINE.DEADLINE = DEADLINE
        require(sum((args.selftest, args.parent_layout_selftest, args.serialization_selftest)) <= 1, "single_cli_mode")
        if args.serialization_selftest:
            require(not any(getattr(args, name.replace("-", "_")) is not None for name in
                ("state-root", "delta-root", "seed34-root", "packet-root", "refinement-root", "prepare-root", "p1-root", "task712-root")) and
                not args.block_root and args.candidate_root is None, "serialization_selftest_parent_free")
            result = serialization_selftest()
        elif args.selftest:
            require(not any(getattr(args, name.replace("-", "_")) is not None for name in
                ("state-root", "delta-root", "seed34-root", "packet-root", "refinement-root", "prepare-root", "p1-root", "task712-root")) and
                not args.block_root and args.candidate_root is None, "selftest_parent_free")
            result = selftest()
        else:
            require(all(getattr(args, name) is not None for name in ("state_root", "delta_root", "seed34_root", "packet_root", "refinement_root")),
                    "all_five_saved_parent_roots_required")
            if args.parent_layout_selftest:
                require(args.prepare_root is args.p1_root is args.task712_root is args.candidate_root is args.output is None and not args.block_root,
                        "parent_metadata_only_mode")
                result = parent_layout_selftest(args)
            else:
                require(len(args.block_root) == 4 and all(getattr(args, name) is not None for name in
                    ("prepare_root", "p1_root", "task712_root", "candidate_root")), "all_actual_oracle_roots_required")
                result = check_actual(args)
    except (ResourceStop, REFINE.ResourceStop) as error:
        code = 3
        result = document("checker-result", {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE",
            "phase": str(error) or LAST_PHASE, "all_stage_arrays_compared": False,
            "candidate": False, "cross_checked": False, "verified": False})
    except Exception as error:
        code = 1
        result = document("checker-result", {"status": "FAIL", "reason": type(error).__name__ + ":" + str(error),
            "phase": LAST_PHASE, "candidate": False, "cross_checked": False, "verified": False})
    raw = canonical(result)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
    sys.stdout.buffer.write(raw); sys.stdout.buffer.flush()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
