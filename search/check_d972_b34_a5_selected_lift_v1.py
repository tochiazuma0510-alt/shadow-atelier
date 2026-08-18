#!/usr/bin/env python3
"""Independent checker for the complete q3 x A5 fixed-roof fibre."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


SCHEMA = "d972-b34-a5-selected-lift/v1"
POSITIVE = "B34_A5_LAYER_FIXED_OUTSIDE_ROOF_LIFT_CROSSCHECKED"
NEGATIVE = "B4_A_FIXED_OUTSIDE_ROOF_FIBRE_OBSTRUCTION_CROSSCHECKED"
UNKNOWN = "B34_A5_LAYER_UNKNOWN_RESOURCE"
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
FC8_PATH = Path("ci/out/d972_b4_fc8_a5four_v1.json")
WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
FC8_HISTORICAL_SHA = "558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
AXIS_SHA = "59c96e7d62a20af4207f715df8e2927a8fc373e1f12e8f3be70e535d8afe5347"
AXIS_PATH = Path("sol/luna_reply_157cp_c5_surgery_torsor_chief.md")
SOURCE_PINS = {
    "q3_producer": ("search/d972_b345_q3_chief_v1.g",
                    "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"),
    "q3_checker": ("search/check_d972_b345_q3_chief_v1.py",
                   "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"),
    "q3_driver": ("search/d972_b345_q3_gha_driver_v1.g",
                  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"),
    "fc8_producer": ("search/d972_b4_fc8_a5four_v1.g",
                     "d482315bb0abc54e9707651a8fb73e73a4a569f101f51c232b76a73fbf57e804"),
    "fc8_checker": ("search/check_d972_b4_fc8_a5four_v1.py",
                    "5b2f54b7adbddbff914fe2d28786327df9109d4e91fa53b1be03114eed5a65d4"),
    "fc8_driver": ("search/d972_b4_fc8_a5four_gha_driver_v1.g",
                   "806d8bfa32ecb1f24f0873147da9e13b56fa171294f081cdd321894b77c545af"),
    "frozen_words": ("search/certs/d972_b4_word_key_artifact_v1_20260816.json",
                     WORDS_SHA),
    "outside_classifier_source":
        ("sol/luna_reply_157cp_c5_surgery_torsor_chief.md", AXIS_SHA),
}
SELECTED_WORD = [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]
RECEIPT_FIELDS = {
    "schema", "status", "terminal_token", "terminal", "pins",
    "frozen_outside", "fine_layer_binding", "d1_preflight", "source_fibre",
    "composite_universe", "outer_q3_fibre", "scan", "performance",
    "proof_implication", "provenance", "runtime_ms",
}
SCAN_FIELDS = {
    "evaluated_candidates", "exhaustive", "counts", "rejection_rle",
    "rejection_stream_sha256", "selected", "settlement_is_acceptance_gate",
    "resource_skips",
}
PERFORMANCE_FIELDS = {
    "candidate_long_word_builds", "compact_candidates",
    "new_literal_gate_candidates", "full_universe_coordinates",
    "fixed_contexts_precomputed", "derived_slice_precomputed_before_acceptance_scan",
    "section_source_words_materialized_in_hot_loop",
    "selected_word_materializations_at_most_one", "new_onto_cache_entries",
    "new_onto_cache_upper_bound", "old_factor_onto_cache_entries",
    "settlement_calls", "ANUPQ_calls", "PB5_constructions",
    "Elements_A5four_calls", "generic_large_joint_kernel_calls",
}


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def comparison_stamp(value: Any) -> str:
    """Bounded diagnostic for exact producer/checker receipt comparisons."""
    if value is None or isinstance(value, (bool, int, str)):
        return repr(value)
    return f"sha256={digest_obj(value)}"


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise CheckError(f"{label} actual({comparison_stamp(actual)}) "
                         f"expected({comparison_stamp(expected)})")


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


Perm = tuple[int, ...]


def perm(row: Sequence[int]) -> Perm:
    require(all(isinstance(x, int) for x in row), "permutation entry type")
    p = tuple(x - 1 for x in row)
    require(set(p) == set(range(len(p))), "permutation is not bijective")
    return p


def one(n: int) -> Perm:
    return tuple(range(n))


def mul(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degree")
    return tuple(b[a[i]] for i in range(len(a)))


def inv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, v in enumerate(a):
        out[v] = i
    return tuple(out)


def power(a: Perm, n: int) -> Perm:
    if n < 0:
        return power(inv(a), -n)
    out, base = one(len(a)), a
    while n:
        if n & 1:
            out = mul(out, base)
        base = mul(base, base)
        n >>= 1
    return out


def order(a: Perm) -> int:
    seen = [False] * len(a)
    ans = 1
    for i in range(len(a)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = a[j]
            length += 1
        ans = math.lcm(ans, length)
    return ans


def block(perms: Sequence[Perm]) -> Perm:
    out: list[int] = []
    offset = 0
    for p in perms:
        out.extend(offset + x for x in p)
        offset += len(p)
    return tuple(out)


def rho_block_permutations(rows: Sequence[Sequence[Sequence[int]]]) -> list[Perm]:
    """Convert the frozen 6 x 4 x 5 rhoA rows to six degree-20 blocks."""
    require(len(rows) == 6 and all(len(value) == 4 for value in rows),
            "rhoA nested 6x4 shape")
    return [block([perm(component) for component in value]) for value in rows]


def restrict(p: Perm, offset: int, width: int) -> Perm:
    row = tuple(p[offset + i] - offset for i in range(width))
    require(set(row) == set(range(width)), "block restriction")
    return row


def outside_certificate(q3: dict[str, Any], words: dict[str, Any]) -> dict[str, Any]:
    """Rebuild row37=e1^2 and its S3-complement exclusion.

    The q3 outside boolean is intentionally not read.  The exponent label is
    bound to the authenticated normalized GT-compose orbit and every orbit
    key/word is rebound to the frozen 972-row artifact.
    """
    require(words["schema"] == "d972-b4-word-key-artifact/v1" and
            words["count"] == len(words["rows"]) == 972, "frozen 972 schema/count")
    require(len({canonical_bytes(row[1]) for row in words["rows"]}) == 972,
            "frozen 972 key uniqueness")
    powers = q3["canonical_roof_powers"]
    orbit = powers["normalized_orbit"]
    expected_rows = [1, 19, 37, 55, 73, 10, 28, 46, 64, 1]
    outside_exponents = [1, 2, 4, 5, 7, 8]
    outside_rows = [19, 37, 73, 10, 46, 64]
    require(powers["coarse_key_cache_size"] == 972 and
            powers["frozen_rows_evaluated_once"] is True and
            powers["canonicalized_each_step"] is True and
            powers["literal_power_words_retained"] is False and
            powers["normalized_orbit_first_repeat"] == 9 and
            powers["normalized_orbit_n0_n8_distinct"] is True and
            powers["normalized_orbit_n9_identity"] is True and
            powers["outside_residues_complete_mod9"] == outside_exponents and
            len(orbit) == 10, "normalized 972-key orbit contract")
    bindings: list[dict[str, Any]] = []
    for exponent, row_index in enumerate(expected_rows):
        entry = orbit[exponent]
        frozen = words["rows"][row_index - 1]
        require(entry["exponent"] == exponent and entry["row_index"] == row_index,
                "normalized orbit exponent/row")
        require(entry["key"] == frozen[1] and entry["word"] == frozen[2],
                "normalized orbit frozen binding")
        bindings.append({"exponent": exponent, "row_index": row_index,
                         "key_sha256": digest_obj(frozen[1]),
                         "word_sha256": digest_obj(frozen[2])})
    require(len({canonical_bytes(x["key"]) for x in orbit[:9]}) == 9 and
            orbit[9]["key"] == orbit[0]["key"], "normalized orbit closure")
    outside = powers["rows"]
    require([x["exponent"] for x in outside] == outside_exponents and
            [x["row_index"] for x in outside] == outside_rows, "outside orbit list")
    for entry, row_index in zip(outside, outside_rows):
        frozen = words["rows"][row_index - 1]
        require(entry["key"] == frozen[1] and entry["word"] == frozen[2],
                "outside orbit frozen binding")
    require(orbit[2]["word"] == SELECTED_WORD and
            orbit[2]["key"] == words["rows"][36][1], "row37 is normalized e1 square")

    c = perm([2, 3, 1])
    h = perm([2, 1, 3])
    c2 = power(c, 2)
    s3, _ = enumerate_group([c, h], 7)
    complement_generators = [conjugate(h, power(c, r)) for r in range(3)]
    complements = [set(enumerate_group([g], 3)[0]) for g in complement_generators]
    require(len(s3) == 6 and order(c2) == 3 and
            len({frozenset(x) for x in complements}) == 3 and
            all(c2 not in subgroup for subgroup in complements),
            "S3 pure-axis/complement replay")
    outside_bindings = [bindings[n] for n in outside_exponents]
    return {
        "method": "frozen normalized 972-key GT-compose orbit plus X/W=S3 x C6 pure-axis theorem",
        "theorem_source_sha256": AXIS_SHA,
        "producer_boolean_from_q3_used": False,
        "frozen_972_count": 972,
        "normalized_orbit_bindings": bindings,
        "normalized_orbit_row_indices": expected_rows,
        "normalized_orbit_first_repeat": 9,
        "outside_residues_complete_mod9": outside_exponents,
        "outside_orbit_bindings": outside_bindings,
        "base_axis_exponent": 1,
        "base_axis_row_index": 19,
        "selected_exponent": 2,
        "selected_row_index": 37,
        "row37_equals_e1_squared_by_orbit": True,
        "quotient_structure": "X/W ~= S3 x C6",
        "W_order": 27,
        "X_order": 972,
        "A_order": 324,
        "S3_axis_e1_row": [x + 1 for x in c],
        "S3_axis_e1_square_row": [x + 1 for x in c2],
        "S3_arithmetic_complement_generator_rows":
            [[x + 1 for x in g] for g in complement_generators],
        "S3_complement_orders": [2, 2, 2],
        "C6_sign_choices": 2,
        "C6_sign_irrelevant_to_S3_membership": True,
        "e1_square_in_any_arithmetic_complement": False,
        "exponent_not_divisible_by_three": True,
        "outside_A": True,
    }


def pp(values: Sequence[Any], identity: Any, operation: Callable[[Any, Any], Any]) -> Any:
    require(bool(values), "empty paper product")
    out = identity
    for value in reversed(values):
        out = operation(out, value)
    return out


def eval_word(word: Sequence[int], images: Sequence[Any], identity: Any,
              operation: Callable[[Any, Any], Any], inverse: Callable[[Any], Any]) -> Any:
    out = identity
    for letter in word:
        require(1 <= abs(letter) <= len(images), "word image index")
        value = images[abs(letter) - 1]
        out = operation(out, value if letter > 0 else inverse(value))
    return out


def reduce_word(word: Sequence[int]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(isinstance(x, int) and x != 0, "signed word")
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word([-x for x in reversed(word)])


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(1 <= abs(x) <= len(images), "substitution index")
        out.extend(images[x - 1] if x > 0 else inv_word(images[-x - 1]))
        out = reduce_word(out)
    return out


def enumerate_group(gens: Sequence[Perm], cap: int) -> tuple[list[Perm], dict[Perm, int]]:
    require(bool(gens), "empty group generators")
    identity = one(len(gens[0]))
    edges = list(gens) + [inv(g) for g in gens]
    values = [identity]
    index = {identity: 0}
    cursor = 0
    while cursor < len(values):
        current = values[cursor]
        for edge in edges:
            nxt = mul(current, edge)
            if nxt not in index:
                require(len(values) < cap, "group enumeration cap")
                index[nxt] = len(values)
                values.append(nxt)
        cursor += 1
    return values, index


def conjugate(a: Perm, b: Perm) -> Perm:
    return mul(mul(inv(b), a), b)


def commutator(a: Perm, b: Perm) -> Perm:
    return mul(mul(inv(a), inv(b)), mul(a, b))


def normal_generators(ambient_gens: Sequence[Perm], seeds: Sequence[Perm], cap: int) -> list[Perm]:
    selected = [x for x in seeds if x != one(len(x))]
    require(bool(selected), "empty normal seed")
    while True:
        _, subgroup = enumerate_group(selected, cap)
        added = False
        for value in list(selected):
            for actor in ambient_gens:
                candidate = conjugate(value, actor)
                if candidate not in subgroup:
                    selected.append(candidate)
                    added = True
                    break
            if added:
                break
        if not added:
            return selected


def derived_set(gens: Sequence[Perm], expected: int, ambient_cap: int) -> set[Perm]:
    seeds = [commutator(gens[i], gens[j])
             for i in range(len(gens)) for j in range(i + 1, len(gens))]
    ngens = normal_generators(gens, seeds, ambient_cap)
    values, _ = enumerate_group(ngens, expected + 1)
    require(len(values) == expected, "derived subgroup order")
    return set(values)


###############################################################################
# Literal cofaces/deletions.
###############################################################################


def pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i + 1, rank + 1)]


def pair_index(rank: int, pair: Sequence[int]) -> int:
    require(list(pair) in pairs(rank), "pair index")
    return pairs(rank).index(list(pair)) + 1


def coface_generator(rank: int, slot: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if slot == 0:
        return [pair_index(rank + 1, [i + 1, j + 1])]
    if slot == rank + 1:
        return [pair_index(rank + 1, [i, j])]
    require(1 <= slot <= rank, "coface slot")
    if i == slot:
        return [pair_index(rank + 1, [slot, j + 1]),
                pair_index(rank + 1, [slot + 1, j + 1])]
    if j == slot:
        return [pair_index(rank + 1, [i, slot]),
                pair_index(rank + 1, [i, slot + 1])]
    ii, jj = i + (i > slot), j + (j > slot)
    return [pair_index(rank + 1, [ii, jj])]


def cofaces(rank: int) -> list[list[list[int]]]:
    return [[coface_generator(rank, slot, p) for p in pairs(rank)]
            for slot in range(rank + 2)]


def delete_generator(rank: int, strand: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if strand in (i, j):
        return []
    if i > strand:
        i -= 1
    if j > strand:
        j -= 1
    return [pair_index(rank - 1, [i, j])]


def deletions(rank: int) -> list[list[list[int]]]:
    return [[delete_generator(rank, strand, p) for p in pairs(rank)]
            for strand in range(1, rank + 1)]


def compose_maps(first: Sequence[Sequence[int]],
                 second: Sequence[Sequence[int]]) -> list[list[int]]:
    return [substitute(word, second) for word in first]


def elem_pairs(g: Sequence[Any], identity: Any,
               operation: Callable[[Any, Any], Any]) -> list[list[Any]]:
    return [[g[0], g[3]], [g[3], g[5]],
            [pp([g[1], g[3]], identity, operation), g[5]],
            [pp([g[0], g[1]], identity, operation),
             pp([g[4], g[5]], identity, operation)],
            [g[0], pp([g[3], g[4]], identity, operation)]]


def hex_pairs(x: Any, y: Any, identity: Any,
              operation: Callable[[Any, Any], Any], inverse: Callable[[Any], Any]) -> list[list[Any]]:
    z = inverse(pp([x, y], identity, operation))
    u = inverse(pp([y, x], identity, operation))
    return [[x, y], [x, z], [y, z], [u, x], [u, y]]


def elem_power(a: Any, n: int, identity: Any,
               operation: Callable[[Any, Any], Any], inverse: Callable[[Any], Any]) -> Any:
    if n < 0:
        return elem_power(inverse(a), -n, identity, operation, inverse)
    out, base = identity, a
    while n:
        if n & 1:
            out = operation(out, base)
        base = operation(base, base)
        n >>= 1
    return out


def hex_from_values(values: Sequence[Any], m: int, x: Any, y: Any,
                    identity: Any, operation: Callable[[Any, Any], Any],
                    inverse: Callable[[Any], Any]) -> list[Any]:
    require(len(values) == 5, "hex width")
    z = inverse(pp([x, y], identity, operation))
    u = inverse(pp([y, x], identity, operation))
    fxy, fxz, fyz, fux, fuy = values
    return [pp([elem_power(y, m, identity, operation, inverse), fxy,
                elem_power(x, m, identity, operation, inverse), inverse(fxz),
                elem_power(z, m, identity, operation, inverse), fyz], identity, operation),
            pp([inverse(fux), elem_power(x, m, identity, operation, inverse),
                inverse(fxy), elem_power(y, m, identity, operation, inverse), fuy,
                elem_power(u, m, identity, operation, inverse)], identity, operation)]


def pent_from_values(values: Sequence[Any], identity: Any,
                     operation: Callable[[Any, Any], Any], inverse: Callable[[Any], Any]) -> Any:
    require(len(values) == 5, "pentagon width")
    return pp([inverse(pp([values[4], values[2]], identity, operation)),
               values[1], values[3], values[0]], identity, operation)


def context(word: Sequence[int], contexts: Sequence[Sequence[Any]], identity: Any,
            operation: Callable[[Any, Any], Any], inverse: Callable[[Any], Any]) -> list[Any]:
    return [eval_word(word, p, identity, operation, inverse) for p in contexts]


###############################################################################
# Independent pc collector copied from the public receipt contract, not GAP.
###############################################################################


def coords_word(coords: Sequence[int]) -> list[int]:
    out: list[int] = []
    for i, exponent in enumerate(coords, 1):
        require(isinstance(exponent, int) and exponent >= 0, "pc coordinate")
        out.extend([i] * exponent)
    return out


@dataclass
class PcCollector:
    receipt: dict[str, Any]

    def __post_init__(self) -> None:
        self.n = int(self.receipt["generator_count"])
        self.orders = list(self.receipt["relative_orders"])
        require(self.n == len(self.orders) <= 175, "pc width")
        require(self.receipt["exponent"] == 3 and all(x == 3 for x in self.orders),
                "pc exponent")
        self.powers = [self._coord(x) for x in self.receipt["power_relations"]]
        self.inverses = [self._coord(x) for x in self.receipt["inverses"]]
        self.conjugates = {(x["i"], x["j"]): self._coord(x["coords"])
                           for x in self.receipt["conjugate_relations"]}
        self.inverse_conjugates = {(x["i"], x["j"]): self._coord(x["coords"])
                                   for x in self.receipt["inverse_conjugate_relations"]}
        require(len(self.conjugates) == self.n * (self.n - 1) // 2 and
                set(self.conjugates) == set(self.inverse_conjugates), "pc conjugate table")
        self.cache: dict[tuple[int, ...], tuple[int, ...]] = {(): self.zero()}

    def _coord(self, row: Sequence[int]) -> tuple[int, ...]:
        require(len(row) == self.n and all(isinstance(x, int) for x in row), "pc row")
        require(all(0 <= x < self.orders[i] for i, x in enumerate(row)), "pc range")
        return tuple(row)

    def zero(self) -> tuple[int, ...]:
        return (0,) * self.n

    def unit(self, i: int) -> tuple[int, ...]:
        require(1 <= i <= self.n, "pc unit")
        row = [0] * self.n
        row[i - 1] = 1
        return tuple(row)

    def collect(self, signed_word: Sequence[int]) -> tuple[int, ...]:
        key = tuple(signed_word)
        if key in self.cache:
            return self.cache[key]
        tokens: list[int] = []
        for x in signed_word:
            require(1 <= abs(x) <= self.n, "pc letter")
            tokens.extend([x] if x > 0 else coords_word(self.inverses[-x - 1]))
        steps, cap = 0, max(10000, 1000 * (1 + len(tokens)) * (1 + self.n))
        while True:
            changed = False
            for pos in range(len(tokens) - 1):
                a, b = tokens[pos], tokens[pos + 1]
                if a > b:
                    tokens[pos:pos + 2] = [b] + coords_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if changed:
                steps += 1
                require(steps <= cap, "pc rewrite cap")
                continue
            pos = 0
            while pos < len(tokens):
                i = tokens[pos]
                end = pos
                while end < len(tokens) and tokens[end] == i:
                    end += 1
                if end - pos >= self.orders[i - 1]:
                    tokens[pos:pos + self.orders[i - 1]] = coords_word(self.powers[i - 1])
                    changed = True
                    break
                pos = end
            if not changed:
                break
            steps += 1
            require(steps <= cap, "pc power cap")
        row = [0] * self.n
        last = 0
        for token in tokens:
            require(token >= last, "pc collector normal order")
            row[token - 1] += 1
            require(row[token - 1] < self.orders[token - 1], "pc uncollected power")
            last = token
        answer = tuple(row)
        self.cache[key] = answer
        return answer

    def mul(self, a: Sequence[int], b: Sequence[int]) -> tuple[int, ...]:
        return self.collect(coords_word(a) + coords_word(b))

    def inverse(self, a: Sequence[int]) -> tuple[int, ...]:
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(a[i - 1]):
                word.extend(coords_word(self.inverses[i - 1]))
        return self.collect(word)

    def conjugate(self, a: Sequence[int], b: Sequence[int]) -> tuple[int, ...]:
        return self.mul(self.mul(self.inverse(b), a), b)

    def validate(self) -> None:
        require(int(self.receipt["order_decimal"]) == math.prod(self.orders), "pc order")
        require(0 <= self.receipt["nilpotency_class"] <= 3, "pc class")
        for i in range(1, self.n + 1):
            require(self.mul(self.unit(i), self.inverses[i - 1]) == self.zero() and
                    self.mul(self.inverses[i - 1], self.unit(i)) == self.zero(), "pc inverse")
        for key, expected in self.conjugates.items():
            i, j = key
            require(self.conjugate(self.unit(i), self.unit(j)) == expected,
                    "pc conjugate")
        for key, expected in self.inverse_conjugates.items():
            i, j = key
            require(self.conjugate(self.unit(i), self.inverses[j - 1]) == expected,
                    "pc inverse conjugate")
        marked = self.receipt["marked_generators"]
        expected_pairs = pairs(self.receipt["rank"])
        require([row["pair"] for row in marked] == expected_pairs and
                [row["label"] for row in marked] ==
                [f"a{i}{j}" for i, j in expected_pairs], "pc marked order")
        for row in marked:
            require(self.mul(row["coords"], row["inverse_coords"]) == self.zero() and
                    self.mul(row["inverse_coords"], row["coords"]) == self.zero(),
                    "pc marked inverse")
        require(len(self.receipt["original_relations"]) ==
                len(self.receipt["original_relator_images"]), "pc relator count")
        for word, claimed in zip(self.receipt["original_relations"],
                                 self.receipt["original_relator_images"]):
            require(pc_eval(word, marked, self) == tuple(claimed) == self.zero(),
                    "pc original relator")


def pc_eval(word: Sequence[int], marked: Sequence[dict[str, Any]],
            pc: PcCollector) -> tuple[int, ...]:
    out = pc.zero()
    for x in word:
        row = marked[abs(x) - 1]
        out = pc.mul(out, row["coords"] if x > 0 else row["inverse_coords"])
    return out


def f2_marked_generators(marked3: Sequence[dict[str, Any]]) \
        -> list[dict[str, Any]]:
    """Return the F2=<x12,x23> alphabet, excluding canonical PB3 x13."""
    require([row["pair"] for row in marked3] == [[1, 2], [1, 3], [2, 3]],
            "PB3/F2 marked-generator order")
    return [marked3[0], marked3[2]]


def pc_context(word: Sequence[int], contexts: Sequence[Sequence[tuple[int, ...]]],
               pc: PcCollector) -> list[tuple[int, ...]]:
    return [eval_word(word, p, pc.zero(), pc.mul, pc.inverse) for p in contexts]


def pc_group(marked: Sequence[tuple[int, ...]], pc: PcCollector,
             cap: int) -> set[tuple[int, ...]]:
    edges = list(marked) + [pc.inverse(x) for x in marked]
    values = [pc.zero()]
    found = {pc.zero()}
    cursor = 0
    while cursor < len(values):
        for edge in edges:
            value = pc.mul(values[cursor], edge)
            if value not in found:
                require(len(values) < cap, "pc subgroup cap")
                found.add(value)
                values.append(value)
        cursor += 1
    return found


def pc_derived(marked: Sequence[tuple[int, ...]], pc: PcCollector,
               expected: int) -> set[tuple[int, ...]]:
    def pc_comm(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        return pc.mul(pc.mul(pc.inverse(a), pc.inverse(b)), pc.mul(a, b))
    seeds = [pc_comm(marked[i], marked[j])
             for i in range(len(marked)) for j in range(i + 1, len(marked))]
    selected = [x for x in seeds if x != pc.zero()]
    while True:
        subgroup = pc_group(selected, pc, expected + 1)
        added = False
        for value in list(selected):
            for actor in marked:
                c = pc.mul(pc.mul(pc.inverse(actor), value), actor)
                if c not in subgroup:
                    selected.append(c)
                    added = True
                    break
            if added:
                break
        if not added:
            require(len(subgroup) == expected, "pc derived size")
            return subgroup


###############################################################################
# D1 and source sections.
###############################################################################


def build_d1(fc: dict[str, Any]) -> dict[str, Any]:
    x, y, z = perm(fc["a5"]["X"]), perm(fc["a5"]["Y"]), perm(fc["a5"]["Z"])
    require(mul(inv(x), inv(y)) == z, "A5 Z orientation")
    a5, _ = enumerate_group([x, y], 61)
    require(len(a5) == 60, "A5 order")
    identity5 = one(5)
    for value in a5:
        if value == identity5:
            continue
        normal = normal_generators([x, y], [value], 61)
        require(len(enumerate_group(normal, 61)[0]) == 60, "A5 simplicity")
    a18 = [cofaces(3)[s] for s in [4, 0, 1, 2, 3]]
    d4 = deletions(4)
    comps: list[dict[str, Any]] = []
    cyclic = [0, 0, 0]
    onto = 0
    for i, phi in enumerate(a18):
        for strand, deletion in enumerate(d4, 1):
            mapping = compose_maps(phi, deletion)
            images = [eval_word(w, [x, z, y], one(5), mul, inv) for w in mapping]
            group, _ = enumerate_group(images, 61)
            support = [j for j, value in enumerate(images) if value != one(5)]
            if len(group) == 60:
                require([images[0], images[2], images[1]] == [x, y, z],
                        "onto composite marking")
                onto += 1
            else:
                require(len(group) == 5 and len(support) == 1, "cyclic component")
                cyclic[support[0]] += 1
            comps.append({"coface_index": i + 1, "deletion_strand": strand,
                          "map": mapping, "image_order": len(group),
                          "support": [j + 1 for j in support],
                          "images": images})
    require(onto == 8 and cyclic == [4, 4, 4], "8/12 classification")
    full_marks = [block([r["images"][j] for r in comps]) for j in range(3)]
    c = perm([2, 3, 4, 5, 1])
    compact_marks = [block([x, c, one(5)]), block([z, one(5), one(5)]),
                     block([y, one(5), c])]
    compact, compact_index = enumerate_group([compact_marks[0], compact_marks[2]], 1501)
    derived = derived_set([compact_marks[0], compact_marks[2]], 60, 1501)
    require(len(compact) == 1500 and len(derived) == 60, "compact D_F")
    full_pb3_group, _ = enumerate_group(full_marks, 7501)
    full_f2_group, _ = enumerate_group([full_marks[0], full_marks[2]], 1501)
    require(len(full_pb3_group) == 7500 and len(full_f2_group) == 1500,
            "D/D_F counts")
    # The common source words give a bijection compact -> full.
    paired, _ = enumerate_group([block([compact_marks[0], full_marks[0]]),
                                 block([compact_marks[2], full_marks[2]])], 1501)
    require(len(paired) == 1500, "compact/full graph")
    pb4_components: list[list[Perm]] = []
    for generator in range(6):
        pb4_components.append([
            eval_word(deletion[generator], [x, z, y], one(5), mul, inv)
            for deletion in d4])
    expected_rho_nested = [[[v + 1 for v in component] for component in value]
                           for value in pb4_components]
    require(expected_rho_nested == fc["rhoA"]["marked_images"],
            "rhoA nested component replay")
    pb4_marks = [block(value) for value in pb4_components]
    require(pb4_marks == rho_block_permutations(fc["rhoA"]["marked_images"]),
            "rhoA nested-to-block convention")
    pb2_words = [row[0] for row in cofaces(2)]
    pb2_new = block([eval_word(w, full_marks, one(100), mul, inv) for w in pb2_words])
    require(order(pb2_new) == 5, "PB2 new factor")
    return {"x": x, "y": y, "z": z, "a18": a18, "d4": d4, "comps": comps,
            "full_marks": full_marks, "compact_marks": compact_marks,
            "compact": compact, "compact_index": compact_index, "derived": derived,
            "pb4_marks": pb4_marks, "pb2_words": pb2_words, "pb2_new": pb2_new,
            "onto": onto, "cyclic": cyclic}


def df_word_bfs(x: Perm, y: Perm) -> tuple[list[Perm], list[list[int]]]:
    states, words = [one(len(x))], [[]]
    index = {states[0]: 0}
    edges = [(1, x), (-1, inv(x)), (2, y), (-2, inv(y))]
    cursor = 0
    while cursor < len(states):
        for label, edge in edges:
            value = mul(states[cursor], edge)
            if value not in index:
                require(len(states) < 1500, "D_F BFS cap")
                index[value] = len(states)
                states.append(value)
                words.append(reduce_word(words[cursor] + [label]))
        cursor += 1
    require(len(states) == 1500, "D_F BFS coverage")
    return states, words


def select_normal_sections(d1: dict[str, Any], oldx: Perm, oldy: Perm,
                           old_contexts: list[tuple[str, Any]]) -> dict[str, Any]:
    require(order(oldx) == order(oldy) == 18, "old F_H generator orders")
    relators = [[1] * 18, [2] * 18]
    require(all(eval_word(w, [oldx, oldy], one(len(oldx)), mul, inv) == one(len(oldx))
                for w in relators), "old power relators")
    cx, cy = d1["compact_marks"][0], d1["compact_marks"][2]
    rel_values = [eval_word(w, [cx, cy], one(15), mul, inv) for w in relators]
    df_states, df_words = df_word_bfs(cx, cy)
    selected: list[dict[str, Any]] = []
    subgroup: set[Perm] = {one(15)}
    for conjugator_index, (actor, actor_word) in enumerate(zip(df_states, df_words), 1):
        for base, (relator, value) in enumerate(zip(relators, rel_values), 1):
            candidate = conjugate(value, actor)
            if candidate not in subgroup:
                word = reduce_word(inv_word(actor_word) + relator + actor_word)
                selected.append({"base_relator": base,
                                 "conjugator_index": conjugator_index,
                                 "word": word, "value": candidate})
                _, sub_index = enumerate_group([x["value"] for x in selected], 1501)
                subgroup = set(sub_index)
                require(len(selected) <= 20, "normal generator cap")
                if len(subgroup) == 1500:
                    break
        if len(subgroup) == 1500:
            break
    require(len(subgroup) == 1500, "tracked normal closure")
    # Replay every selected source word in every old/new context.
    for row in selected:
        values: dict[str, Any] = {}
        for name, spec in old_contexts:
            kind, contexts, identity, operation, inverse = spec
            values[name] = (context(row["word"], contexts, identity, operation, inverse)
                            if kind == "contexts" else
                            eval_word(row["word"], contexts, identity, operation, inverse))
        for name in ("old_q0_main", "old_b2_main"):
            require(values[name] == old_contexts[[x[0] for x in old_contexts].index(name)][1][2],
                    f"section {name}")
        for name in ("old_q0_hex", "old_b2_hex", "old_q4_pent", "old_pi4_pent"):
            identity = old_contexts[[x[0] for x in old_contexts].index(name)][1][2]
            require(all(x == identity for x in values[name]), f"section {name}")
        row["contexts"] = values
    # BFS by the registered normal-generator edge order.
    states = [one(15)]
    parents, edges = [0], [0]
    full_states = [one(100)]
    hex_states = [[one(100)] * 5]
    pent_states = [[one(20)] * 5]
    index = {states[0]: 0}
    edge_order = list(range(1, len(selected) + 1)) + list(range(-1, -len(selected) - 1, -1))
    cursor = 0
    while cursor < len(states):
        for label in edge_order:
            row = selected[abs(label) - 1]
            value = row["value"] if label > 0 else inv(row["value"])
            nxt = mul(states[cursor], value)
            if nxt in index:
                continue
            require(len(states) < 1500, "section BFS cap")
            index[nxt] = len(states)
            states.append(nxt)
            parents.append(cursor + 1)
            edges.append(label)
            full = row["contexts"]["new_full_main"]
            hx = row["contexts"]["new_full_hex"]
            pn = row["contexts"]["new_a5four_pent"]
            if label < 0:
                full, hx, pn = inv(full), [inv(x) for x in hx], [inv(x) for x in pn]
            full_states.append(mul(full_states[cursor], full))
            hex_states.append([mul(hex_states[cursor][i], hx[i]) for i in range(5)])
            pent_states.append([mul(pent_states[cursor][i], pn[i]) for i in range(5)])
        cursor += 1
    require(len(states) == 1500, "section coverage")
    records = [{"index": i + 1, "parent": parents[i], "edge": edges[i],
                "key": [x + 1 for x in states[i]]} for i in range(1500)]
    return {"selected": selected, "states": states, "records": records,
            "full_states": full_states, "hex_states": hex_states,
            "pent_states": pent_states, "relators": relators}


def expand_section(index: int, records: Sequence[dict[str, Any]],
                   generators: Sequence[dict[str, Any]]) -> list[int]:
    edges: list[int] = []
    i = index
    while i != 1:
        row = records[i - 1]
        require(1 <= row["parent"] < i, "section parent DAG")
        edges.append(row["edge"])
        i = row["parent"]
    word: list[int] = []
    for edge in reversed(edges):
        gword = generators[abs(edge) - 1]["word"]
        word = reduce_word(word + (gword if edge > 0 else inv_word(gword)))
    return word


###############################################################################
# Full audit and scan.
###############################################################################


def rle_add(rle: list[dict[str, Any]], code: str) -> None:
    if rle and rle[-1]["code"] == code:
        rle[-1]["count"] += 1
    else:
        rle.append({"code": code, "count": 1})


def derived_counts_from_current_layout(receipt: dict[str, Any]) -> list[int]:
    """The pinned producer stores derived totals in scan.counts, not top-level."""
    require("derived_slice" not in receipt, "unexpected top-level derived_slice")
    scan = receipt.get("scan")
    require(isinstance(scan, dict), "scan receipt layout")
    counts = scan.get("counts")
    require(isinstance(counts, dict) and
            isinstance(counts.get("derived_all"), int) and
            isinstance(counts.get("friendly_derived"), int),
            "derived counts missing from scan.counts")
    return [counts["derived_all"], counts["friendly_derived"]]


def validate_receipt(receipt: dict[str, Any]) -> str:
    require(receipt.get("schema") == SCHEMA, "schema")
    require(set(receipt) == RECEIPT_FIELDS and
            isinstance(receipt.get("runtime_ms"), int) and receipt["runtime_ms"] >= 0,
            "top-level receipt layout")
    require(set(receipt["scan"]) == SCAN_FIELDS, "scan receipt layout")
    require(set(receipt["performance"]) == PERFORMANCE_FIELDS,
            "performance receipt layout")
    require(receipt["provenance"] == {
        "producer": "search/d972_b34_a5_selected_lift_v1.g",
        "checker": "search/check_d972_b34_a5_selected_lift_v1.py",
    }, "provenance layout")
    terminal = receipt.get("terminal_token")
    require(terminal in (POSITIVE, NEGATIVE, UNKNOWN), "terminal token")
    require(digest_file(Q3_PATH) == Q3_SHA, "q3 artifact SHA")
    require(digest_file(FC8_PATH) == FC8_HISTORICAL_SHA, "FC8 artifact SHA")
    require(digest_file(WORDS_PATH) == WORDS_SHA, "word artifact SHA")
    require(digest_file(AXIS_PATH) == AXIS_SHA,
            "axis source SHA")
    q3 = json.loads(Q3_PATH.read_text(encoding="utf-8"))
    fc = json.loads(FC8_PATH.read_text(encoding="utf-8"))
    words = json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    pins = receipt["pins"]
    expected_sources: dict[str, dict[str, Any]] = {}
    for name, (path_text, expected_sha) in SOURCE_PINS.items():
        path = Path(path_text)
        require(digest_file(path) == expected_sha, f"{name} source SHA")
        expected_sources[name] = {"path": path_text, "sha256": expected_sha,
                                  "bytes": path.stat().st_size}
    require(pins["sources"] == expected_sources, "source pin table")
    require(pins["historical_q3_run"] == 32135808950 and
            pins["historical_fc8_run"] == 32153799126 and
            pins["historical_q3_artifact_sha256"] == Q3_SHA and
            pins["same_job_q3_artifact_sha256"] == digest_file(Q3_PATH), "q3 pins")
    require(pins["historical_fc8_artifact_sha256"] == FC8_HISTORICAL_SHA and
            pins["same_job_fc8_artifact_sha256"] == digest_file(FC8_PATH), "FC8 pins")
    normalization = pins["fc8_runtime_normalization"]
    require(normalization["normalized_nonsemantic_field"] == "performance.runtime_ms" and
            isinstance(normalization["observed_fresh_value"], int) and
            normalization["observed_fresh_value"] >= 0 and
            normalization["frozen_value"] == 598 and
            normalization["fresh_checker_passed_before_normalization"] is True and
            normalization["checker_passed_after_normalization"] is True and
            normalization["all_other_JSON_fields_equal"] is True and
            fc["performance"]["runtime_ms"] == 598, "FC8 runtime-only normalization")
    require(q3["terminal_token"] == "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" and
            fc["terminal_token"] == "FC8_A5_FOUR_CHIEF_CROSSCHECKED", "upstream terminals")
    selected = q3["selected_solution"]
    require(selected["exponent"] == 2 and selected["roof_row_index"] == 37 and
            selected["marking_m"] == 0 and selected["correction_index"] == 1 and
            selected["typed_source_word"] == SELECTED_WORD, "frozen selected q3 word")
    require(words["rows"][36][0] == 0 and words["rows"][36][2] == SELECTED_WORD,
            "row37 frozen word")
    require(selected["roof_key"] == words["rows"][36][1], "selected row37 roof key")

    d1 = build_d1(fc)
    d1r = receipt["d1_preflight"]
    require(d1r["a18_maps"] == d1["a18"] and d1r["deletion_maps"] == d1["d4"],
            "literal A18/deletions")
    require(d1r["onto_component_count"] == 8 and
            d1r["cyclic_source_class_counts"] == [4, 4, 4] and
            d1r["PB3_joint_image_order"] == 7500 and
            d1r["F2_image_order"] == 1500 and d1r["F2_derived_order"] == 60 and
            d1r["PB2_relative_factor_order"] == 5, "D1 structural counts")
    expected_comps = [{"coface_index": r["coface_index"],
                       "deletion_strand": r["deletion_strand"], "map": r["map"],
                       "image_order": r["image_order"], "support": r["support"],
                       "marked_rows": [[x + 1 for x in p] for p in r["images"]]}
                      for r in d1["comps"]]
    require(d1r["twenty_composites"] == expected_comps, "twenty composites")
    require(d1r["compact_marked_rows"] ==
            [[x + 1 for x in p] for p in d1["compact_marks"]] and
            d1r["full_F2_marked_rows"] ==
            [[x + 1 for x in p] for p in (d1["full_marks"][0], d1["full_marks"][2])] and
            d1r["full_PB3_marked_rows"] ==
            [[x + 1 for x in p] for p in d1["full_marks"]] and
            d1r["PB2_coface_words"] == d1["pb2_words"] and
            d1r["rhoA_marked_rows"] == [[x + 1 for x in p] for p in d1["pb4_marks"]] and
            d1r["compact_to_full_bijective"] is True,
            "D1 marked rows/rhoA")

    pc3, pc4 = PcCollector(q3["groups"]["PB3"]), PcCollector(q3["groups"]["PB4"])
    pc3.validate()
    pc4.validate()
    marked3, marked4 = q3["groups"]["PB3"]["marked_generators"], q3["groups"]["PB4"]["marked_generators"]
    f2marked3 = f2_marked_generators(marked3)
    b2x, b2y = tuple(f2marked3[0]["coords"]), tuple(f2marked3[1]["coords"])
    b2 = pc_group([b2x, b2y], pc3, 28)
    require(len(b2) == 27, "B(2,3) order")
    b2_derived = pc_derived([b2x, b2y], pc3, 3)
    q0marks = [perm(x) for x in q3["coarse_models"]["Q0"]["marked_permutations"]]
    q0x, q0y = q0marks
    pmarks = [perm(x) for x in q3["coarse_models"]["P"]["marked_permutations"]]
    gmarks = [perm(x) for x in q3["coarse_models"]["G9"]["marked_permutations"]]
    p_group, p_index = enumerate_group(pmarks, 505)
    g_group, g_index = enumerate_group(gmarks, 2917)
    require(len(p_group) == 504 and len(g_group) == 2916, "P/G9 orders")
    p_derived = derived_set(pmarks, 504, 505)
    g_derived = derived_set(gmarks, 729, 2917)
    require(len(p_derived) == 504 and len(g_derived) == 729, "P perfect/G9 derived")
    require(q0marks == [block([pmarks[i], gmarks[i]]) for i in range(2)],
            "Q0 marked subdirect blocks")
    q4marks = [perm(x) for x in q3["coarse_models"]["Q4"]["marked_permutations"]]
    pi4marks = [tuple(x["coords"]) for x in marked4]
    q4_order = int(q3["coarse_models"]["Q4"]["order_decimal"])
    pi4_order = int(q3["groups"]["PB4"]["order_decimal"])
    e4_order = q4_order * pi4_order
    require(q3["typed_relative_stage"]["q3_system_ready"] is True and
            q3["typed_relative_stage"]["pullback_certified"]["E3"] == "Q0 x Pi3[3]" and
            q3["typed_relative_stage"]["pullback_certified"]["E4"] == "Q4 x Pi4[3]" and
            q4_order == 583152628325845597028352 and pi4_order == 59049 and
            e4_order % 5 != 0, "fine E4 direct product/order")
    require(fc["goursat"]["joint_image_is_full_Q0_times_A5four"] is True and
            fc["goursat"]["rhoA_surjective"] is True and
            fc["chief_factor"]["B4_factor_action_transitive"] is True,
            "FC8 A5four surjection/action")
    expected_layer = {
        "old_fine_target": "E4 = Q4 x Pi4[3]",
        "Q4_order": q4_order,
        "Pi4_q3_order": pi4_order,
        "E4_order": e4_order,
        "E4_order_coprime_to_5": True,
        "A5four_order": 60 ** 4,
        "rho_E4_surjective": True,
        "rho_A5four_surjective": True,
        "every_nontrivial_A5four_quotient_order_divisible_by_5": True,
        "no_nontrivial_common_quotient_E4_A5four": True,
        "joint_target_full_E4_times_A5four_by_Goursat": True,
        "H_definition": "ker(PB4 -> E4)",
        "L_definition": "H intersection ker(rhoA)",
        "H_over_L": "A5^4",
        "H_over_L_order": 60 ** 4,
        "L_B4_normal_finite_index": True,
        "B4_factor_action_transitive": True,
        "L_isolated_assumed": False,
    }
    require(receipt["fine_layer_binding"] == expected_layer, "fine layer binding")

    # Complete q3 right fibre and the marking coordinate.
    qcorr = q3["correction_fibre"]["records"]
    require(len(qcorr) == 27 and qcorr[0]["word"] == [], "q3 fibre order")
    qcert = q3["correction_fibre"]["certificate"]
    require(qcert["enumerated_count"] == qcert["projection_kernel_order"] == 27 and
            qcert["direct_product"] is True, "q3 correction-fibre certificate")
    qvalues: list[tuple[int, ...]] = []
    for row in qcorr:
        require(eval_word(row["word"], q0marks, one(36), mul, inv) == one(36),
                "q3 correction coarse identity")
        value = pc_eval(row["word"], f2marked3, pc3)
        require(list(value) == row["ambient_Pi3_coords"], "q3 ambient coords")
        qvalues.append(value)
    require(set(qvalues) == b2 and len(set(qvalues)) == 27, "q3 fibre exact B2")
    require(order(q0x) == order(q0y) == 18, "coarse marking order")
    pb2_words = d1["pb2_words"]
    # canonical PB3 order is x12,x13,x23
    pb2_q = [eval_word(w, [q0x, one(36), q0y], one(36), mul, inv) for w in pb2_words]
    pb2_b = [pc_eval(w, marked3, pc3) for w in pb2_words]
    require(math.lcm(*(order(x) for x in pb2_q)) == 18, "coarse PB2 order")
    require(all(elem_power(x, 18, pc3.zero(), pc3.mul, pc3.inverse) == pc3.zero()
                for x in pb2_b), "q3 PB2 divides 18")
    require(order(d1["pb2_new"]) == 5 and math.lcm(18, 5) == 90,
            "new PB2 C5 kernel")

    # The exact old F_H is Q0 x B2: Q0 has abelianization order 4 and no
    # nontrivial 3-group quotient.  Sections are certified by source words.
    source = receipt["source_fibre"]
    require(source["F_H_order"] == 1469664 * 27 and
            source["F_H_prime_support"] == [2, 3, 7] and
            source["F_H_equals_Q0_times_B2"] is True and
            source["Q0_abelianization_order"] == 4 and
            source["projection_kernel_order"] == 1500 and
            source["joint_F2_target_full_direct_product"] is True,
            "F_H x D_F contract")
    expected_product_proof = {
        "Q0_marked_image_is_subdirect_P_times_G9": True,
        "P_order": 504,
        "P_perfect": len(p_derived) == 504,
        "G9_order": 2916,
        "G9_derived_order": 729,
        "G9_solvable": True,
        "Q0_full_by_perfect_versus_solvable_Goursat": True,
        "Q0_abelianization_reduced_to_G9_order": 4,
        "B2_is_3group_order": 27,
        "every_nontrivial_B2_quotient_has_C3_quotient": True,
        "Q0_has_no_C3_quotient": True,
        "F_H_full_by_Goursat": True,
    }
    require(source["direct_product_proof"] == expected_product_proof and
            len(g_group) // len(g_derived) == 4,
            "independent F_H direct-product proof")
    # Use an independent regular 27-point model for the marked B(2,3), rather
    # than any producer permutation realization.
    b2_list = sorted(b2)
    b2_pos = {v: i for i, v in enumerate(b2_list)}
    def pc_regular(value: tuple[int, ...]) -> Perm:
        return tuple(b2_pos[pc3.mul(a, value)] for a in b2_list)
    bx, by = pc_regular(b2x), pc_regular(b2y)
    oldx, oldy = block([q0x, bx]), block([q0y, by])
    require(order(oldx) == order(oldy) == 18, "actual F_H marked orders")

    q0_hex = hex_pairs(q0x, q0y, one(36), mul, inv)
    b2_hex = hex_pairs(b2x, b2y, pc3.zero(), pc3.mul, pc3.inverse)
    require(all(power(x, 18) == one(len(x)) for pair in q0_hex for x in pair) and
            all(elem_power(x, 18, pc3.zero(), pc3.mul, pc3.inverse) == pc3.zero()
                for pair in b2_hex for x in pair), "old hexagon marking period")
    q4_pent = elem_pairs(q4marks, one(144), mul)
    p4_pent = elem_pairs(pi4marks, pc4.zero(), pc4.mul)
    new_hex = hex_pairs(d1["full_marks"][0], d1["full_marks"][2], one(100), mul, inv)
    new_pent = elem_pairs(d1["pb4_marks"], one(20), mul)
    old_contexts: list[tuple[str, Any]] = [
        ("old_q0_main", ("main", q0marks, one(36), mul, inv)),
        ("old_b2_main", ("main", [b2x, b2y], pc3.zero(), pc3.mul, pc3.inverse)),
        ("old_q0_hex", ("contexts", q0_hex, one(36), mul, inv)),
        ("old_b2_hex", ("contexts", b2_hex, pc3.zero(), pc3.mul, pc3.inverse)),
        ("old_q4_pent", ("contexts", q4_pent, one(144), mul, inv)),
        ("old_pi4_pent", ("contexts", p4_pent, pc4.zero(), pc4.mul, pc4.inverse)),
        ("new_full_main", ("main", [d1["full_marks"][0], d1["full_marks"][2]], one(100), mul, inv)),
        ("new_full_hex", ("contexts", new_hex, one(100), mul, inv)),
        ("new_a5four_pent", ("contexts", new_pent, one(20), mul, inv)),
    ]
    sections = select_normal_sections(d1, oldx, oldy, old_contexts)
    expected_generators = [{"base_relator": x["base_relator"],
                            "conjugator_index": x["conjugator_index"],
                            "word": x["word"],
                            "compact_key": [v + 1 for v in x["value"]]}
                           for x in sections["selected"]]
    require(source["tracked_normal_generators"] == expected_generators,
            "tracked normal generators")
    require(source["D_F_structure"] == "A5_diag x C5^2" and
            source["D_F_order"] == source["projection_kernel_order"] == 1500 and
            source["every_nontrivial_D_F_quotient_has_order_divisible_by_5"] is True and
            source["no_common_quotient"] is True and
            source["power_relators"] == sections["relators"] and
            source["old_generator_orders"] == [18, 18] and
            source["normal_closure_order"] == 1500 and
            source["normal_generator_count"] == len(expected_generators) and
            source["section_order"] == "BFS edges +g1..+gr,-g1..-gr" and
            source["section_records"] == sections["records"] and
            source["section_coverage_sha256"] == digest_obj(sections["records"]),
            "section records/digest")

    # Independently bind row37 to e1^2 through the complete frozen 972-key
    # normalized orbit, then exclude it from each of the three actual C2
    # complements in S3.  The q3 outside boolean is never consulted.
    classifier = receipt["frozen_outside"]["classifier"]
    expected_classifier = outside_certificate(q3, words)
    require(classifier == expected_classifier and
            receipt["frozen_outside"]["exponent"] == 2 and
            receipt["frozen_outside"]["row_index"] == 37 and
            receipt["frozen_outside"]["roof_key"] == words["rows"][36][1],
            "pure-axis outside replay")

    # Precompute old outer gates and new context values.
    base = SELECTED_WORD
    outer_words = [reduce_word(base + row["word"]) for row in qcorr]
    outer_rows: list[dict[str, Any]] = []
    onto_p: dict[Perm, bool] = {}
    onto_g: dict[Perm, bool] = {}
    onto_b: dict[tuple[int, ...], bool] = {}
    for i, word in enumerate(outer_words):
        main_q = eval_word(word, q0marks, one(36), mul, inv)
        main_b = pc_eval(word, f2marked3, pc3)
        hq = context(word, q0_hex, one(36), mul, inv)
        hb = pc_context(word, b2_hex, pc3)
        pq = context(word, q4_pent, one(144), mul, inv)
        ppc = pc_context(word, p4_pent, pc4)
        roof = eval_word(qcorr[i]["word"], q0marks, one(36), mul, inv) == one(36)
        charm = restrict(main_q, 9, 27) in g_derived and main_b in b2_derived
        hex_ok = (all(x == one(36) for x in hex_from_values(hq, 0, q0x, q0y,
                                                            one(36), mul, inv)) and
                  all(x == pc3.zero() for x in hex_from_values(hb, 0, b2x, b2y,
                                                               pc3.zero(), pc3.mul, pc3.inverse)))
        pent_ok = (pent_from_values(pq, one(144), mul, inv) == one(144) and
                   pent_from_values(ppc, pc4.zero(), pc4.mul, pc4.inverse) == pc4.zero())
        pv, gv = restrict(main_q, 0, 9), restrict(main_q, 9, 27)
        if pv not in onto_p:
            yp = pp([inv(pv), pmarks[1], pv], one(9), mul)
            onto_p[pv] = len(enumerate_group([pmarks[0], yp], 505)[0]) == 504
        if gv not in onto_g:
            yg = pp([inv(gv), gmarks[1], gv], one(27), mul)
            onto_g[gv] = len(enumerate_group([gmarks[0], yg], 2917)[0]) == 2916
        if main_b not in onto_b:
            yb = pp([pc3.inverse(main_b), b2y, main_b], pc3.zero(), pc3.mul)
            onto_b[main_b] = len(pc_group([b2x, yb], pc3, 28)) == 27
        onto = onto_p[pv] and onto_g[gv] and onto_b[main_b]
        outer_rows.append({"index": i + 1, "q_coords": qcorr[i]["q_coords"],
                           "word_sha256": digest_obj(word), "old_roof": roof,
                           "old_charming": charm, "old_hexagon": hex_ok,
                           "old_pentagon": pent_ok, "old_onto": onto,
                           "main": eval_word(word, [d1["compact_marks"][0],
                                                     d1["compact_marks"][2]], one(15), mul, inv),
                           "hex": context(word, new_hex, one(100), mul, inv),
                           "pent": context(word, new_pent, one(20), mul, inv)})
    require(receipt["outer_q3_fibre"] == [{k: row[k] for k in
            ("index", "q_coords", "word_sha256", "old_roof", "old_charming",
             "old_hexagon", "old_pentagon", "old_onto")} for row in outer_rows],
            "outer gate table")

    m_values = [0, 18, 36, 54, 72]
    universe = receipt["composite_universe"]
    expected_coordinate_digest = digest_obj({
        "outer": [[r["q_coords"], r["word_sha256"]] for r in outer_rows],
        "m": m_values, "corrections": [r["key"] for r in sections["records"]]})
    new_shift_rows = [[x + 1 for x in power(d1["pb2_new"], m)] for m in m_values]
    require(all(all(elem_power(x, m, pc3.zero(), pc3.mul, pc3.inverse) == pc3.zero()
                    for x in pb2_b) and all(power(x, m) == one(36) for x in pb2_q)
                for m in m_values) and len({tuple(x) for x in new_shift_rows}) == 5,
            "five exact PB2 kernel shifts")
    require(universe["outer_count"] == 27 and universe["m_shift_count"] == 5 and
            universe["correction_count"] == 1500 and universe["total_count"] == 202500 and
            universe["m_values"] == m_values and universe["lambda_values"] == [1,37,73,109,145] and
            universe["q3_marking_order"] == universe["H_ord"] == 18 and
            universe["new_marking_order"] == universe["L_ord"] == 90 and
            universe["PB2_joint_image_order"] == 90 and
            universe["PB2_projection_kernel_order"] == 5 and
            universe["PB2_coprime_direct_product_proof"] is True and
            universe["PB2_old_shift_values_all_identity"] is True and
            universe["PB2_new_shift_value_rows"] == new_shift_rows and
            universe["PB2_new_shift_values_distinct"] is True and
            universe["friendly_shift_indices"] == [0, 1, 2, 3] and
            universe["unfriendly_shift_indices"] == [4] and
            universe["q3_outer_word_digest"] == digest_obj([r["word"] for r in qcorr]) and
            universe["coordinate_digest"] == expected_coordinate_digest and
            universe["coordinate_injectivity_proof"] ==
            "E3=Q0 x B(2,3), joint F_H x D_F, and coprime PB2 C5 kernel" and
            universe["no_duplicate_coordinates"] is True and
            universe["q3_fibre_complete"] is True and
            universe["F_H_times_D_F_kernel_exact"] is True and
            universe["PB2_C5_kernel_exact"] is True, "complete universe")

    counts = {"total": 0, "friendly": 0, "old_roof": 0, "old_charming": 0,
              "old_hexagon": 0, "old_pentagon": 0, "old_onto": 0,
              "new_charming": 0, "new_hexagon": 0, "new_pentagon": 0,
              "new_onto": 0, "derived_all": 0, "friendly_derived": 0,
              "accepted": 0, "materialized_words": 0, "resource_skips": 0}
    derived_flags: list[list[bool]] = []
    derived_indices: list[list[int]] = []
    for outer in outer_rows:
        flags = [mul(outer["main"], correction) in d1["derived"]
                 for correction in sections["states"]]
        derived_flags.append(flags)
        derived_indices.append([i + 1 for i, value in enumerate(flags) if value])
    derived_counts = [len(x) for x in derived_indices]
    counts["derived_all"] = 5 * sum(derived_counts)
    counts["friendly_derived"] = sum(math.gcd(2 * m + 1, 90) == 1
                                      for m in m_values) * sum(derived_counts)
    require(counts["derived_all"] <= 8100 and counts["friendly_derived"] <= 6480,
            "derived-slice bounds")
    require(derived_counts_from_current_layout(receipt) ==
            [counts["derived_all"], counts["friendly_derived"]],
            "derived totals in scan.counts")
    rle: list[dict[str, Any]] = []
    codes: list[str] = []
    selected_actual: dict[str, Any] | None = None
    onto_new: dict[tuple[Perm, int], bool] = {}
    evaluated = 0
    for oi, outer in enumerate(outer_rows):
        for shift, m in enumerate(m_values):
            u = 2 * m + 1
            for ci, correction in enumerate(sections["states"]):
                evaluated += 1
                counts["total"] += 1
                code = ""
                if math.gcd(u, 90) != 1:
                    code = "F"
                else:
                    counts["friendly"] += 1
                    for field, symbol, counter in (("old_roof", "R", "old_roof"),
                                                   ("old_charming", "C", "old_charming"),
                                                   ("old_hexagon", "H", "old_hexagon"),
                                                   ("old_pentagon", "P", "old_pentagon"),
                                                   ("old_onto", "O", "old_onto")):
                        if not outer[field]:
                            code = symbol
                            break
                        counts[counter] += 1
                if not code:
                    combined = mul(outer["main"], correction)
                    if not derived_flags[oi][ci]:
                        code = "c"
                    else:
                        counts["new_charming"] += 1
                        hv = [mul(outer["hex"][j], sections["hex_states"][ci][j])
                              for j in range(5)]
                        if not all(x == one(100) for x in hex_from_values(
                                hv, m, d1["full_marks"][0], d1["full_marks"][2],
                                one(100), mul, inv)):
                            code = "h"
                        else:
                            counts["new_hexagon"] += 1
                            pv = [mul(outer["pent"][j], sections["pent_states"][ci][j])
                                  for j in range(5)]
                            if pent_from_values(pv, one(20), mul, inv) != one(20):
                                code = "p"
                            else:
                                counts["new_pentagon"] += 1
                                key = (combined, shift)
                                if key not in onto_new:
                                    ix = power(d1["compact_marks"][0], u)
                                    iy = pp([inv(combined), power(d1["compact_marks"][2], u),
                                             combined], one(15), mul)
                                    onto_new[key] = len(enumerate_group([ix, iy], 1501)[0]) == 1500
                                if not onto_new[key]:
                                    code = "o"
                                else:
                                    counts["new_onto"] += 1
                                    code = "A"
                codes.append(code)
                rle_add(rle, code)
                if code == "A":
                    counts["accepted"] = 1
                    counts["materialized_words"] = 1
                    cword = expand_section(ci + 1, sections["records"], sections["selected"])
                    candidate = reduce_word(outer_words[oi] + cword)
                    dq = eval_word(candidate, q0marks, one(36), mul, inv)
                    db = pc_eval(candidate, f2marked3, pc3)
                    hq = context(candidate, q0_hex, one(36), mul, inv)
                    hb = pc_context(candidate, b2_hex, pc3)
                    pq = context(candidate, q4_pent, one(144), mul, inv)
                    ppc = pc_context(candidate, p4_pent, pc4)
                    nc = eval_word(candidate, [d1["compact_marks"][0],
                                                d1["compact_marks"][2]], one(15), mul, inv)
                    nf = eval_word(candidate, [d1["full_marks"][0],
                                                d1["full_marks"][2]], one(100), mul, inv)
                    nh = context(candidate, new_hex, one(100), mul, inv)
                    np = context(candidate, new_pent, one(20), mul, inv)
                    require(dq == eval_word(outer_words[oi], q0marks, one(36), mul, inv) and
                            db == pc_eval(outer_words[oi], f2marked3, pc3) and
                            hq == context(outer_words[oi], q0_hex, one(36), mul, inv) and
                            hb == pc_context(outer_words[oi], b2_hex, pc3) and
                            pq == context(outer_words[oi], q4_pent, one(144), mul, inv) and
                            ppc == pc_context(outer_words[oi], p4_pent, pc4) and
                            nc == combined, "materialized old/compact contexts")
                    expected_nf = mul(eval_word(outer_words[oi], [d1["full_marks"][0],
                                                                  d1["full_marks"][2]],
                                                one(100), mul, inv), sections["full_states"][ci])
                    expected_nh = [mul(outer["hex"][k], sections["hex_states"][ci][k])
                                   for k in range(5)]
                    expected_np = [mul(outer["pent"][k], sections["pent_states"][ci][k])
                                   for k in range(5)]
                    require(nf == expected_nf and nh == expected_nh and np == expected_np,
                            "materialized new contexts")
                    require(all(x == one(36) for x in hex_from_values(
                                hq, m, q0x, q0y, one(36), mul, inv)) and
                            all(x == pc3.zero() for x in hex_from_values(
                                hb, m, b2x, b2y, pc3.zero(), pc3.mul, pc3.inverse)) and
                            pent_from_values(pq, one(144), mul, inv) == one(144) and
                            pent_from_values(ppc, pc4.zero(), pc4.mul, pc4.inverse) == pc4.zero() and
                            all(x == one(100) for x in hex_from_values(
                                nh, m, d1["full_marks"][0], d1["full_marks"][2],
                                one(100), mul, inv)) and
                            pent_from_values(np, one(20), mul, inv) == one(20),
                            "materialized literal identities")
                    direct_payload = {
                        "m": m, "lambda": u,
                        "old_q0_main": [x + 1 for x in dq],
                        "old_b2_main": list(db),
                        "old_q0_hex": [[x + 1 for x in value] for value in hq],
                        "old_b2_hex": [list(value) for value in hb],
                        "old_q4_pent": [[x + 1 for x in value] for value in pq],
                        "old_pi4_pent": [list(value) for value in ppc],
                        "new_compact_main": [x + 1 for x in nc],
                        "new_full_main": [x + 1 for x in nf],
                        "new_hex": [[x + 1 for x in value] for value in nh],
                        "new_pent": [[x + 1 for x in value] for value in np],
                    }
                    direct_canary = {
                        "all_cached_contexts_match": True,
                        "old_hexagon_direct": True,
                        "old_pentagon_direct": True,
                        "new_hexagon_direct": True,
                        "new_pentagon_direct": True,
                        "settlement_used": False,
                        "context_sha256": digest_obj(direct_payload),
                    }
                    selected_actual = {"candidate_index": evaluated, "outer_index": oi + 1,
                                       "m_shift_index": shift, "m": m, "lambda": u,
                                       "correction_index": ci + 1,
                                       "typed_source_word": candidate,
                                       "source_word_sha256": digest_obj(candidate),
                                       "q3_correction_word": qcorr[oi]["word"],
                                       "a5_correction_word": cword,
                                       "charming": True, "friendly": True,
                                       "hexagon_exact": True, "pentagon_exact": True,
                                       "onto_exact": True, "reduces_to_fixed_roof": True,
                                       "settlement_required_for_acceptance": False,
                                       "settlement_diagnostic": "NOT_COMPUTED_NONISOLATED_L",
                                       "direct_materialization_replay": direct_canary}
                    break
            if selected_actual is not None:
                break
        if selected_actual is not None:
            break
    exhaustive = selected_actual is None and evaluated == 202500
    expected_terminal = POSITIVE if selected_actual is not None else (NEGATIVE if exhaustive else UNKNOWN)
    scan = receipt["scan"]
    # Keep every lossless scan component as an independent fail-closed gate.
    # Besides avoiding an opaque composite failure, the bounded stamps identify
    # representation drift without printing the candidate word or full RLE.
    require_equal(scan["evaluated_candidates"], evaluated,
                  "scan.evaluated_candidates")
    require_equal(scan["exhaustive"], exhaustive, "scan.exhaustive")
    require_equal(scan["counts"], counts, "scan.counts")
    require_equal(scan["rejection_rle"], rle, "scan.rejection_rle")
    require_equal(scan["rejection_stream_sha256"],
                  hashlib.sha256("".join(codes).encode()).hexdigest(),
                  "scan.rejection_stream_sha256")
    if selected_actual is None:
        require_equal(scan["selected"], None, "scan.selected")
    else:
        selected_receipt = scan["selected"]
        require(isinstance(selected_receipt, dict), "scan.selected layout")
        require(set(selected_receipt) == set(selected_actual),
                "scan.selected field set")
        for field in selected_actual:
            if field != "direct_materialization_replay":
                require_equal(selected_receipt[field], selected_actual[field],
                              f"scan.selected.{field}")
        direct_receipt = selected_receipt["direct_materialization_replay"]
        direct_expected = selected_actual["direct_materialization_replay"]
        require(isinstance(direct_receipt, dict) and
                set(direct_receipt) == set(direct_expected),
                "scan.selected.direct_materialization_replay field set")
        for field in direct_expected:
            require_equal(direct_receipt[field], direct_expected[field],
                          f"scan.selected.direct_materialization_replay.{field}")
    require_equal(scan["settlement_is_acceptance_gate"], False,
                  "scan.settlement_is_acceptance_gate")
    require_equal(scan["resource_skips"], 0, "scan.resource_skips")
    require(receipt["status"] == terminal and isinstance(receipt["terminal"], bool) and
            receipt["terminal"] == (terminal in (POSITIVE, NEGATIVE)),
            "status/terminal boolean")
    performance = receipt["performance"]
    require(performance["candidate_long_word_builds"] == counts["materialized_words"] and
            performance["compact_candidates"] == evaluated and
            performance["new_literal_gate_candidates"] == counts["new_charming"] and
            performance["full_universe_coordinates"] == 202500 and
            performance["fixed_contexts_precomputed"] is True and
            performance["derived_slice_precomputed_before_acceptance_scan"] is True and
            performance["section_source_words_materialized_in_hot_loop"] is False and
            performance["selected_word_materializations_at_most_one"] is True and
            performance["new_onto_cache_entries"] == len(onto_new) and
            performance["new_onto_cache_upper_bound"] == 240 and
            len(onto_new) <= 240 and
            performance["old_factor_onto_cache_entries"] ==
            [len(onto_p), len(onto_g), len(onto_b)] and
            performance["settlement_calls"] == 0 and
            performance["ANUPQ_calls"] == performance["PB5_constructions"] == 0 and
            performance["Elements_A5four_calls"] == 0 and
            performance["generic_large_joint_kernel_calls"] == 0,
            "performance/no-settlement contract")
    require(terminal == expected_terminal, "terminal/result equivalence")
    proof = receipt["proof_implication"]
    require(set(proof) == {"positive", "negative"} and
            set(proof["positive"]) == {"L_isolated_assumed", "implication",
                                         "remaining_boundary"} and
            set(proof["negative"]) == {"applicable", "corollary_3_13",
                                         "L_B4_normal_finite_index",
                                         "fixed_outside_roof_full_fibre_empty",
                                         "global_genuine_image_subgroup",
                                         "arithmetic_contained_in_genuine",
                                         "subgroup_chain", "index_X_A", "deduction",
                                         "isolated_fallback"},
            "proof implication layout")
    require(proof["positive"]["L_isolated_assumed"] is False and
            proof["positive"]["remaining_boundary"] ==
            "uniform/cofinal absorption of every later required chief layer" and
            isinstance(proof["negative"]["applicable"], bool) and
            proof["negative"]["applicable"] == (terminal == NEGATIVE) and
            proof["negative"]["corollary_3_13"] ==
            "a genuine roof element survives to every B4-normal finite-index window" and
            proof["negative"]["L_B4_normal_finite_index"] is True and
            proof["negative"]["global_genuine_image_subgroup"] is True and
            proof["negative"]["arithmetic_contained_in_genuine"] is True and
            proof["negative"]["subgroup_chain"] == "A <= P <= X" and
            proof["negative"]["index_X_A"] == 3,
            "paper implication contract")
    if terminal == NEGATIVE:
        require(exhaustive and evaluated == 202500 and selected_actual is None and
                receipt["proof_implication"]["negative"]["fixed_outside_roof_full_fibre_empty"] is True and
                receipt["proof_implication"]["negative"]["index_X_A"] == 3,
                "negative promotion gates")
    if terminal == POSITIVE:
        require(selected_actual is not None and
                receipt["proof_implication"]["positive"]["L_isolated_assumed"] is False,
                "positive implication scope")
    return terminal


###############################################################################
# Mutation self-test.  It exercises the fail-closed binding schema without
# requiring either full upstream artifact.
###############################################################################


def validate_fixture(obj: dict[str, Any]) -> None:
    require(obj["q3_words"] == [[], [1, -2]], "q3 fibre word")
    require(len(obj["q3_keys"]) == len(set(obj["q3_keys"])) == 2, "q3 duplicate/missing")
    require(obj["coface"] == [[1], [2, 4]], "coface")
    require(obj["deletion"] == [[], [1]], "deletion")
    require(obj["a5"] == [3, 4, 2, 5, 1], "A5 marking")
    require(obj["cyclic"] == [1, 0], "cyclic coordinate")
    require(obj["m"] == [0, 18, 36, 54, 72], "m shift")
    require(obj["kernel"] == 1500, "direct-product kernel")
    require(obj["charm"] == "derived_membership", "charming substitution")
    require(obj["residual"] == [0, 0], "literal residual")
    require(obj["outside"] == [2, 37] and
            obj["outside_key"] == digest_obj([0, [[4, 0], [5, 0], [0, 0]],
                                                list(range(1, 10))]), "outside roof key")
    require(obj["artifacts"] == [Q3_SHA, FC8_HISTORICAL_SHA], "artifact hash")
    require(obj["coverage"] == digest_obj([27, 5, 1500]), "coverage digest")
    require(obj["derived"] == derived_counts_from_current_layout(obj) == [8100, 6480],
            "derived totals live in scan.counts")
    require(obj["settlement_gate"] is False, "settlement gate")
    require(rho_block_permutations(obj["rho_nested"]) == [one(20)] * 6,
            "rhoA nested/block convention")
    require([row["tag"] for row in f2_marked_generators(obj["pb3_marked"])] ==
            ["x12", "x23"], "F2 excludes PB3 x13")
    require(obj["terminal"] == NEGATIVE, "terminal relabel")


def self_test() -> None:
    fixture = {"q3_words": [[], [1, -2]], "q3_keys": ["0", "1"],
               "coface": [[1], [2, 4]], "deletion": [[], [1]],
               "a5": [3, 4, 2, 5, 1], "cyclic": [1, 0],
               "m": [0, 18, 36, 54, 72], "kernel": 1500,
               "charm": "derived_membership", "residual": [0, 0],
               "outside": [2, 37],
               "outside_key": digest_obj([0, [[4, 0], [5, 0], [0, 0]],
                                             list(range(1, 10))]),
               "artifacts": [Q3_SHA, FC8_HISTORICAL_SHA],
               "coverage": digest_obj([27, 5, 1500]), "derived": [8100, 6480],
               "scan": {"counts": {"derived_all": 8100,
                                    "friendly_derived": 6480}},
               "settlement_gate": False,
               "rho_nested": [[[1, 2, 3, 4, 5] for _ in range(4)]
                              for _ in range(6)],
               "pb3_marked": [{"pair": [1, 2], "tag": "x12"},
                              {"pair": [1, 3], "tag": "x13"},
                              {"pair": [2, 3], "tag": "x23"}],
               "terminal": NEGATIVE}
    validate_fixture(fixture)
    mutations = [
        lambda x: x["q3_words"][1].append(2),
        lambda x: x.__setitem__("q3_keys", ["0", "0"]),
        lambda x: x["q3_keys"].pop(),
        lambda x: x["coface"][1].__setitem__(1, 3),
        lambda x: x["deletion"].__setitem__(1, [2]),
        lambda x: x["a5"].__setitem__(0, 4),
        lambda x: x["cyclic"].__setitem__(1, 1),
        lambda x: x["m"].__setitem__(4, 73),
        lambda x: x.__setitem__("kernel", 1499),
        lambda x: x.__setitem__("charm", "raw_exponent_sums"),
        lambda x: x["residual"].__setitem__(0, 1),
        lambda x: x.__setitem__("outside_key", "0" * 64),
        lambda x: x["artifacts"].__setitem__(0, "0" * 64),
        lambda x: x["artifacts"].__setitem__(1, "0" * 64),
        lambda x: x.__setitem__("coverage", "0" * 64),
        lambda x: x["derived"].__setitem__(0, 8099),
        lambda x: x.__setitem__("derived_slice", {"stale_location": True}),
        lambda x: x.__setitem__("settlement_gate", True),
        lambda x: x["rho_nested"][0].__setitem__(0, [2, 1, 3, 4, 5]),
        lambda x: x["pb3_marked"][2].__setitem__("pair", [1, 3]),
        lambda x: x.__setitem__("terminal", POSITIVE),
    ]
    for mutation in mutations:
        bad = copy.deepcopy(fixture)
        mutation(bad)
        try:
            validate_fixture(bad)
        except CheckError:
            continue
        raise CheckError("mutation unexpectedly accepted")
    try:
        require_equal({"total": 124}, {"total": 123}, "scan.counts")
    except CheckError as exc:
        require(str(exc).startswith("scan.counts actual(sha256="),
                "named scan diagnostic canary")
    else:
        raise CheckError("named scan diagnostic unexpectedly accepted")
    print(f"D972_B34_A5_SELECTED_LIFT_CHECKER_SELFTEST_PASS mutations={len(mutations)}")


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 2 and argv[1] == "--self-test":
            self_test()
            return 0
        require(len(argv) == 2, "usage: checker RECEIPT | --self-test")
        receipt = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        terminal = validate_receipt(receipt)
        print(f"B34_A5_SELECTED_LIFT_CHECKER_PASS terminal={terminal} "
              f"evaluated={receipt['scan']['evaluated_candidates']}")
        return 0
    except (CheckError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"B34_A5_SELECTED_LIFT_CHECKER_FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
