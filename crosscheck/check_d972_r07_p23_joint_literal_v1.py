#!/usr/bin/env python3
"""Independent finite checker for the R07 p=2/p=3 joint literal word.

The two signed input words are pinned from the frozen authoritative row
artifacts.  This file is deliberately self-contained: it imports only the
Python standard library and never opens a producer, receipt, helper, verdict,
or any other repository file.  Prime-local source and PB4 quotients are
rebuilt through the Jennings embedding in F_p[G]/I^4; G36 and PSL(2,8) are
rebuilt from their public marked formulas.

Default mode performs the complete finite replay and writes one JSON result
under --out-dir.  --selftest checks the frozen words, CRT construction, and
static conventions without constructing any finite quotient.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import pathlib
import sys
import time
from collections import deque
from typing import Callable, Hashable, Iterable, Sequence, TypeVar


SCHEMA = "d972-r07-p23-joint-literal-independent-checker/v1"
RESULT_NAME = "d972_r07_p23_joint_literal_checker_v1.json"
FINAL_MARKER = "R07_P23_JOINT_CHECKER_FINAL"

# These are provenance pins, not runtime dependencies.  The words below are
# embedded so that a clean GHA checkout needs only this checker.
INPUT_PINS = (
    {
        "role": "P2R00004_authoritative_row_artifact",
        "path": "search/certs/d972_row36_pent_bridge_p2_prereg_v5_20260824.json",
        "bytes": 114_911,
        "sha256": "bf58d269fa587c693dd3ab9872129fdc695fe141e37d5c2582b858227bf056d9",
        "row_id": "P2R00004",
        "word_id": "W00004",
    },
    {
        "role": "P3R00023_authoritative_row_artifact",
        "path": "ci/row36_p3_outcome_artifacts_32675485659/d972_row36_pent_bridge_p3_prereg_v8_20260824.json",
        "bytes": 66_337_660,
        "sha256": "2d33542ba797440ec96d16e02f9f8d7ea537048eb84d02b2ce57153d147faea4",
        "row_id": "P3R00023",
        "word_id": "W00023",
    },
)

W2 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -2, 1, 1,
    2, 1, 1, -2, 1, 1, 2, 1, 1, 2, 1, 1, -2, 1, 1, -2, 1, 1,
    2, 2, -1, -1, -2, -1,
)
W3 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -1, -1, 2,
    -1, -1, -2, -2, 1, 1, 2, 1, 2, 2, 1, 2, 2, -1, 2, 2, 1, 2,
    1, 1, 2, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, -2, -1,
    -2, -2, 1, 2, 1, 1, -2, 1,
)
W2_SHA256 = "eec36b318e094eedadd575e231246043de8542657b80e6ec24f9e8eb8717f91a"
W3_SHA256 = "1af161dbc0bd96156d858867e959f305677a6ba145f7d4eb235a40fa9f12b3e4"
D_LENGTH = 72
D_SHA256 = "2e1d84946e458a7f73ef7e18838127e5cf0d9fbb3b18138a12d28bc3ccbe172a"
BALANCED_A = -8
W23_LENGTH = 616
W23_SHA256 = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"

# Artin pure-braid presentations, in the fixed generator order
# x12,x13,x14,x23,x24,x34.  They are used only to form the two-sided ideal
# in the truncated group algebra.
PB4_RELATORS = (
    (-1, 2, 1, 2, 4, -2, -4, -2),
    (-1, 4, 1, 2, -4, -2),
    (-1, 3, 1, 3, 5, -3, -5, -3),
    (-1, 5, 1, 3, -5, -3),
    (-1, 6, 1, -6),
    (-2, 3, 2, 3, 6, -3, -6, -3),
    (-2, 5, 2, 3, 6, -3, -6, -5, 6, 3, -6, -3),
    (-2, 6, 2, 3, -6, -3),
    (-4, 3, 4, -3),
    (-4, 5, 4, 5, 6, -5, -6, -5),
    (-4, 6, 4, 5, -6, -5),
)

# Each pair is (image of x, image of y).  The order here is the printed
# positive-factor order F,C,E,A,B only for labelling; PRINTED_A18 below fixes
# the actual noncommutative product B^-1 A^-1 F E C.
COFACES = (
    ("phi234", ((4,), (6,))),
    ("phi12_3_4", ((2, 4), (6,))),
    ("phi1_23_4", ((1, 2), (5, 6))),
    ("phi1_2_34", ((1,), (4, 5))),
    ("phi123", ((1,), (4,))),
)
PRINTED_A18 = (
    ("phi12_3_4", -1),
    ("phi1_2_34", -1),
    ("phi234", 1),
    ("phi1_23_4", 1),
    ("phi123", 1),
)
THETA = ((2,), (1,))
TAU = ((2,), (-1, -2))
TAU2 = ((-1, -2), (1,))

EXPECTED_G07 = ((4, 0), (32, 0), (0, 0))
X36 = ((1, 0), (0, 1), (0, 1))
Y36 = ((1, 1), (1, 0), (1, 1))
G36_ONE = ((0, 0), (0, 0), (0, 0))


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest_obj(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def require(condition: bool, token: str) -> None:
    if not condition:
        raise RuntimeError(token)


def inv_word(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-letter for letter in reversed(word))


def free_reduce(word: Iterable[int]) -> tuple[int, ...]:
    result: list[int] = []
    for letter in word:
        require(letter != 0 and abs(letter) >= 1, "INVALID_SIGNED_LETTER")
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)


def word_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return free_reduce(tuple(left) + tuple(right))


def word_power(word: Sequence[int], exponent: int) -> tuple[int, ...]:
    if exponent < 0:
        return word_power(inv_word(word), -exponent)
    result: tuple[int, ...] = ()
    base = free_reduce(word)
    n = exponent
    while n:
        if n & 1:
            result = word_mul(result, base)
        base = word_mul(base, base)
        n >>= 1
    return result


def substitute_word(word: Sequence[int], images: Sequence[Sequence[int]]) -> tuple[int, ...]:
    result: list[int] = []
    for letter in word:
        image = tuple(images[abs(letter) - 1])
        result.extend(image if letter > 0 else inv_word(image))
    return free_reduce(result)


def exponent_sums(word: Sequence[int]) -> tuple[int, int]:
    return tuple(sum(1 if x == g else -1 if x == -g else 0 for x in word) for g in (1, 2))  # type: ignore[return-value]


def construct_words() -> tuple[tuple[int, ...], tuple[int, ...]]:
    discrepancy = free_reduce(inv_word(W2) + W3)
    combined = word_mul(W2, word_power(discrepancy, BALANCED_A))
    return discrepancy, combined


def static_selftest() -> dict[str, object]:
    require(sys.version_info >= (3, 11), "PYTHON_TOO_OLD")
    require(free_reduce(W2) == W2 and free_reduce(W3) == W3, "INPUT_NOT_FREELY_REDUCED")
    require(digest_obj(list(W2)) == W2_SHA256, "W2_DIGEST_MISMATCH")
    require(digest_obj(list(W3)) == W3_SHA256, "W3_DIGEST_MISMATCH")
    discrepancy, combined = construct_words()
    require(len(discrepancy) == D_LENGTH and digest_obj(list(discrepancy)) == D_SHA256, "D_PIN_MISMATCH")
    require(len(combined) == W23_LENGTH and digest_obj(list(combined)) == W23_SHA256, "W23_PIN_MISMATCH")
    require(free_reduce(combined) == combined, "W23_NOT_FREELY_REDUCED")
    require(BALANCED_A % 2 == 0 and BALANCED_A % 9 == 1, "CRT_CONGRUENCE_MISMATCH")
    require(exponent_sums(combined) == (108, -36), "W23_EXPONENT_SUM_PIN_MISMATCH")
    require(len(COFACES) == 5 and len({name for name, _ in COFACES}) == 5, "COFACE_ROSTER_MISMATCH")
    require(tuple(name for name, _ in PRINTED_A18) == ("phi12_3_4", "phi1_2_34", "phi234", "phi1_23_4", "phi123"), "A18_ORDER_MISMATCH")
    # This tiny source-only construction exercises the independent algebra,
    # reduction, multiplication, inversion and enumeration code.  It does not
    # build either six-generator PB4 quotient.
    tiny = JenningsD4(2, 2, ())
    tiny_elements = enumerate_generated(tiny.one, tiny.generators, tiny.mul, tiny.inv)
    require(tiny.filtration_dimensions() == (1, 2, 4, 8), "SELFTEST_SOURCE_FILTRATION_MISMATCH")
    require(len(tiny_elements) == 128, "SELFTEST_SOURCE_ORDER_MISMATCH")
    return {
        "w2_length": len(W2), "w2_sha256": W2_SHA256,
        "w3_length": len(W3), "w3_sha256": W3_SHA256,
        "d_length": len(discrepancy), "d_sha256": D_SHA256,
        "a": BALANCED_A,
        "w23_length": len(combined), "w23_sha256": W23_SHA256,
        "exponent_sums_xy": list(exponent_sums(combined)),
        "tiny_source_order": len(tiny_elements),
    }


def rref(rows: Iterable[Sequence[int]], p: int, ncols: int) -> tuple[list[list[int]], list[int]]:
    work = [[entry % p for entry in row] for row in rows]
    work = [row for row in work if any(row)]
    pivots: list[int] = []
    active = 0
    for col in range(ncols):
        chosen = next((i for i in range(active, len(work)) if work[i][col]), None)
        if chosen is None:
            continue
        work[active], work[chosen] = work[chosen], work[active]
        scale = pow(work[active][col], -1, p)
        work[active] = [(scale * value) % p for value in work[active]]
        for row_index, row in enumerate(work):
            if row_index == active or not row[col]:
                continue
            coefficient = row[col]
            work[row_index] = [(a - coefficient * b) % p for a, b in zip(row, work[active])]
        pivots.append(col)
        active += 1
        if active == len(work):
            break
    return work[:active], pivots


def reduce_vector(vector: Sequence[int], rows: Sequence[Sequence[int]], pivots: Sequence[int], p: int) -> tuple[int, ...]:
    result = [entry % p for entry in vector]
    for row, pivot in zip(rows, pivots):
        coefficient = result[pivot]
        if coefficient:
            result = [(a - coefficient * b) % p for a, b in zip(result, row)]
    return tuple(result)


class JenningsD4:
    """Units generated by group generators in F_p[G]/I^4."""

    def __init__(self, p: int, rank: int, relators: Sequence[Sequence[int]]):
        self.p = p
        self.rank = rank
        self.monomials: list[tuple[int, ...]] = [()]
        for degree in range(1, 4):
            self.monomials.extend(itertools.product(range(rank), repeat=degree))
        self.index = {monomial: i for i, monomial in enumerate(self.monomials)}
        self.size = len(self.monomials)
        self.one = tuple([1] + [0] * (self.size - 1))
        self._free_generators = tuple(self._free_generator(i) for i in range(rank))

        ideal_rows: list[list[int]] = []
        for relator in relators:
            delta = list(self._eval_free(relator))
            delta[0] = (delta[0] - 1) % p
            support_degrees = [len(self.monomials[i]) for i, value in enumerate(delta) if value]
            if not support_degrees:
                continue
            minimum = min(support_degrees)
            for left in self.monomials:
                if len(left) > 3 - minimum:
                    continue
                for right in self.monomials:
                    if len(left) + minimum + len(right) > 3:
                        continue
                    row = [0] * self.size
                    for i, coefficient in enumerate(delta):
                        if coefficient:
                            monomial = left + self.monomials[i] + right
                            if len(monomial) <= 3:
                                j = self.index[monomial]
                                row[j] = (row[j] + coefficient) % p
                    if any(row):
                        ideal_rows.append(row)
        self.ideal_rows, self.ideal_pivots = rref(ideal_rows, p, self.size)
        pivot_set = set(self.ideal_pivots)
        self.free_columns = tuple(i for i in range(self.size) if i not in pivot_set)
        self.generators = tuple(self.reduce(g) for g in self._free_generators)

    def _free_generator(self, index: int) -> tuple[int, ...]:
        value = [0] * self.size
        value[0] = 1
        value[self.index[(index,)]] = 1
        return tuple(value)

    def _mul_free(self, left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        result = [0] * self.size
        left_support = [(i, value) for i, value in enumerate(left) if value]
        right_support = [(i, value) for i, value in enumerate(right) if value]
        for i, a in left_support:
            left_monomial = self.monomials[i]
            for j, b in right_support:
                monomial = left_monomial + self.monomials[j]
                if len(monomial) <= 3:
                    k = self.index[monomial]
                    result[k] = (result[k] + a * b) % self.p
        return tuple(result)

    def _inverse_free(self, value: Sequence[int]) -> tuple[int, ...]:
        augmentation = list(value)
        augmentation[0] = (augmentation[0] - 1) % self.p
        u = tuple(augmentation)
        u2 = self._mul_free(u, u)
        u3 = self._mul_free(u2, u)
        return tuple((self.one[i] - u[i] + u2[i] - u3[i]) % self.p for i in range(self.size))

    def _eval_free(self, word: Sequence[int]) -> tuple[int, ...]:
        inverses = tuple(self._inverse_free(g) for g in self._free_generators)
        result = self.one
        for letter in word:
            factor = self._free_generators[letter - 1] if letter > 0 else inverses[-letter - 1]
            result = self._mul_free(result, factor)
        return result

    def reduce(self, value: Sequence[int]) -> tuple[int, ...]:
        return reduce_vector(value, self.ideal_rows, self.ideal_pivots, self.p)

    def mul(self, left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        return self.reduce(self._mul_free(left, right))

    def inv(self, value: Sequence[int]) -> tuple[int, ...]:
        augmentation = list(value)
        augmentation[0] = (augmentation[0] - 1) % self.p
        u = tuple(augmentation)
        u2 = self.mul(u, u)
        u3 = self.mul(u2, u)
        return self.reduce(tuple((self.one[i] - u[i] + u2[i] - u3[i]) % self.p for i in range(self.size)))

    def power(self, value: Sequence[int], exponent: int) -> tuple[int, ...]:
        if exponent < 0:
            return self.power(self.inv(value), -exponent)
        result = self.one
        base = tuple(value)
        n = exponent
        while n:
            if n & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            n >>= 1
        return result

    def eval_word(self, word: Sequence[int], images: Sequence[Sequence[int]] | None = None) -> tuple[int, ...]:
        chosen = self.generators if images is None else tuple(tuple(value) for value in images)
        inverses = tuple(self.inv(value) for value in chosen)
        result = self.one
        for letter in word:
            factor = chosen[letter - 1] if letter > 0 else inverses[-letter - 1]
            result = self.mul(result, factor)
        return result

    def coords(self, value: Sequence[int]) -> tuple[int, ...]:
        reduced = self.reduce(value)
        return tuple(reduced[i] for i in self.free_columns)

    def filtration_dimensions(self) -> tuple[int, int, int, int]:
        return tuple(sum(1 for i in self.free_columns if len(self.monomials[i]) == degree) for degree in range(4))  # type: ignore[return-value]


T = TypeVar("T", bound=Hashable)


def enumerate_generated(one: T, generators: Sequence[T], mul: Callable[[T, T], T], inv: Callable[[T], T]) -> set[T]:
    steps = tuple(dict.fromkeys(tuple(generators) + tuple(inv(g) for g in generators)))
    seen = {one}
    queue = deque([one])
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = mul(current, step)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def evaluate_generic(word: Sequence[int], one: T, generators: Sequence[T], mul: Callable[[T, T], T], inv: Callable[[T], T]) -> T:
    inverses = tuple(inv(g) for g in generators)
    result = one
    for letter in word:
        factor = generators[letter - 1] if letter > 0 else inverses[-letter - 1]
        result = mul(result, factor)
    return result


def power_generic(value: T, exponent: int, one: T, mul: Callable[[T, T], T], inv: Callable[[T], T]) -> T:
    if exponent < 0:
        return power_generic(inv(value), -exponent, one, mul, inv)
    result = one
    base = value
    n = exponent
    while n:
        if n & 1:
            result = mul(result, base)
        base = mul(base, base)
        n >>= 1
    return result


def element_order(value: T, one: T, mul: Callable[[T, T], T], cap: int) -> int:
    current = one
    for order in range(1, cap + 1):
        current = mul(current, value)
        if current == one:
            return order
    raise RuntimeError("ELEMENT_ORDER_CAP_EXCEEDED")


def commutator(left: T, right: T, mul: Callable[[T, T], T], inv: Callable[[T], T]) -> T:
    return mul(mul(mul(inv(left), inv(right)), left), right)


def derived_subgroup(elements: set[T], one: T, generators: Sequence[T], mul: Callable[[T, T], T], inv: Callable[[T], T]) -> set[T]:
    basic = commutator(generators[0], generators[1], mul, inv)
    conjugates = [mul(mul(inv(g), basic), g) for g in elements]
    return enumerate_generated(one, conjugates, mul, inv)


def dmul(left: tuple[int, int], right: tuple[int, int], n: int = 36) -> tuple[int, int]:
    a, e = left
    b, f = right
    return ((a + (-b if e else b)) % n, (e + f) % 2)


def dinv(value: tuple[int, int], n: int = 36) -> tuple[int, int]:
    a, e = value
    return ((-a if e == 0 else a) % n, e)


def g36_mul(left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    return tuple(dmul(a, b) for a, b in zip(left, right))


def g36_inv(value: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    return tuple(dinv(a) for a in value)


# GF(8)=F_2[t]/(t^3+t+1), low-bit encoding.  The centre of SL(2,8) is
# trivial, so these 2x2 matrices model PSL(2,8) directly.
GF8_POLY = 0b1011
MATRIX_ONE = ((1, 0), (0, 1))
S_MATRIX = ((1, 0), (1, 1))
T_MATRIX = ((4, 3), (1, 5))


def gf8_mul(left: int, right: int) -> int:
    result = 0
    a, b = left, right
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= GF8_POLY
    return result & 7


def gf8_inv(value: int) -> int:
    require(value != 0, "GF8_ZERO_INVERSE")
    result = 1
    for _ in range(6):
        result = gf8_mul(result, value)
    return result


def matrix_mul(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(tuple(gf8_mul(left[i][0], right[0][j]) ^ gf8_mul(left[i][1], right[1][j]) for j in range(2)) for i in range(2))  # type: ignore[return-value]


def matrix_inv(value: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    determinant = gf8_mul(value[0][0], value[1][1]) ^ gf8_mul(value[0][1], value[1][0])
    scalar = gf8_inv(determinant)
    return (
        (gf8_mul(value[1][1], scalar), gf8_mul(value[0][1], scalar)),
        (gf8_mul(value[1][0], scalar), gf8_mul(value[0][0], scalar)),
    )


SIGMA1 = matrix_mul(matrix_inv(T_MATRIX), S_MATRIX)
SIGMA2 = matrix_mul(matrix_inv(SIGMA1), T_MATRIX)
X_PSL = matrix_mul(SIGMA1, SIGMA1)
Y_PSL = matrix_mul(SIGMA2, SIGMA2)


def relation_key(alg_source: JenningsD4, alg_pb4: JenningsD4, word: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    values = [alg_source.eval_word(word)]
    for _, images in COFACES:
        values.append(alg_pb4.eval_word(substitute_word(word, images)))
    return tuple(values)


def relation_key_orders(alg_source: JenningsD4, alg_pb4: JenningsD4, word: Sequence[int], cap: int) -> tuple[list[int], int]:
    values = relation_key(alg_source, alg_pb4, word)
    orders = [element_order(value, algebra.one, algebra.mul, cap) for value, algebra in [(values[0], alg_source)] + [(value, alg_pb4) for value in values[1:]]]
    return orders, math.lcm(*orders)


def printed_a18(alg_pb4: JenningsD4, word: Sequence[int]) -> tuple[tuple[int, ...], dict[str, tuple[int, ...]]]:
    coface_values = {
        name: alg_pb4.eval_word(substitute_word(word, images))
        for name, images in COFACES
    }
    result = alg_pb4.one
    for name, sign in PRINTED_A18:
        factor = coface_values[name]
        result = alg_pb4.mul(result, factor if sign > 0 else alg_pb4.inv(factor))
    return result, coface_values


def algebra_group_data(alg: JenningsD4, expected_order: int) -> tuple[set[tuple[int, ...]], set[tuple[int, ...]]]:
    elements = enumerate_generated(alg.one, alg.generators, alg.mul, alg.inv)
    require(len(elements) == expected_order, f"SOURCE_GROUP_ORDER_MISMATCH:{alg.p}:{len(elements)}")
    derived = derived_subgroup(elements, alg.one, alg.generators, alg.mul, alg.inv)
    return elements, derived


def run_full() -> dict[str, object]:
    started = time.perf_counter()
    static = static_selftest()
    discrepancy, combined = construct_words()
    print(
        "R07_P23_WORD_PASS "
        f"w2_len={len(W2)} w2_sha256={W2_SHA256} "
        f"w3_len={len(W3)} w3_sha256={W3_SHA256} "
        f"d_len={len(discrepancy)} d_sha256={D_SHA256} "
        f"w23_len={len(combined)} w23_sha256={W23_SHA256}",
        flush=True,
    )
    print("R07_P23_FIREWALL_PASS stdlib_only=true embedded_rows=true producer_receipt_reads=false", flush=True)

    source2 = JenningsD4(2, 2, ())
    source3 = JenningsD4(3, 2, ())
    pb42 = JenningsD4(2, 6, PB4_RELATORS)
    pb43 = JenningsD4(3, 6, PB4_RELATORS)
    require(source2.filtration_dimensions() == (1, 2, 4, 8), "SOURCE2_FILTRATION_MISMATCH")
    require(source3.filtration_dimensions() == (1, 2, 4, 8), "SOURCE3_FILTRATION_MISMATCH")
    require(pb42.filtration_dimensions() == (1, 6, 25, 90), "PB42_FILTRATION_MISMATCH")
    require(pb43.filtration_dimensions() == (1, 6, 25, 90), "PB43_FILTRATION_MISMATCH")
    print("R07_P23_JENNINGS_PASS source_dims=1,2,4,8 pb4_dims=1,6,25,90", flush=True)

    # Recheck the two theorem premises in their own relation-complete targets.
    key_w2_p2 = relation_key(source2, pb42, W2)
    key_w3_p3 = relation_key(source3, pb43, W3)
    require(all(value == algebra.one for value, algebra in [(key_w2_p2[0], source2)] + [(x, pb42) for x in key_w2_p2[1:]]), "P2_INPUT_RELATION_KEY_NONIDENTITY")
    require(all(value == algebra.one for value, algebra in [(key_w3_p3[0], source3)] + [(x, pb43) for x in key_w3_p3[1:]]), "P3_INPUT_RELATION_KEY_NONIDENTITY")
    print("R07_P23_INPUT_KEYS_PASS p2_components=6 p3_components=6", flush=True)

    orders2, order2 = relation_key_orders(source2, pb42, discrepancy, 16)
    orders3, order3 = relation_key_orders(source3, pb43, discrepancy, 27)
    require(order2 == 2 and order3 == 9, f"RELATION_KEY_ORDER_MISMATCH:{order2}:{order3}")
    require(BALANCED_A % order2 == 0 and BALANCED_A % order3 == 1, "SHARP_CRT_CONGRUENCE_MISMATCH")
    print(f"R07_P23_CRT_PASS order2={order2} order3={order3} a={BALANCED_A}", flush=True)

    # Direct relation-complete replay for the assembled word.
    key23_p2 = relation_key(source2, pb42, combined)
    key23_p3 = relation_key(source3, pb43, combined)
    require(all(value == algebra.one for value, algebra in [(key23_p2[0], source2)] + [(x, pb42) for x in key23_p2[1:]]), "W23_P2_RELATION_KEY_NONIDENTITY")
    require(all(value == algebra.one for value, algebra in [(key23_p3[0], source3)] + [(x, pb43) for x in key23_p3[1:]]), "W23_P3_RELATION_KEY_NONIDENTITY")
    a18_2, cofaces2 = printed_a18(pb42, combined)
    a18_3, cofaces3 = printed_a18(pb43, combined)
    require(all(value == pb42.one for value in cofaces2.values()), "P2_COFACE_NONIDENTITY")
    require(all(value == pb43.one for value in cofaces3.values()), "P3_COFACE_NONIDENTITY")
    require(a18_2 == pb42.one and a18_3 == pb43.one, "PRINTED_A18_NONIDENTITY")
    print(
        "R07_P23_COFACES_A18_PASS cofaces=10 "
        "order=phi12_3_4^-1,phi1_2_34^-1,phi234,phi1_23_4,phi123",
        flush=True,
    )

    g36_elements = enumerate_generated(G36_ONE, (X36, Y36), g36_mul, g36_inv)
    psl_elements = enumerate_generated(MATRIX_ONE, (X_PSL, Y_PSL), matrix_mul, matrix_inv)
    require(len(g36_elements) == 23_328, "G36_ORDER_MISMATCH")
    require(len(psl_elements) == 504, "PSL_ORDER_MISMATCH")

    g_w2 = evaluate_generic(W2, G36_ONE, (X36, Y36), g36_mul, g36_inv)
    g_w3 = evaluate_generic(W3, G36_ONE, (X36, Y36), g36_mul, g36_inv)
    g_w23 = evaluate_generic(combined, G36_ONE, (X36, Y36), g36_mul, g36_inv)
    s_w2 = evaluate_generic(W2, MATRIX_ONE, (X_PSL, Y_PSL), matrix_mul, matrix_inv)
    s_w3 = evaluate_generic(W3, MATRIX_ONE, (X_PSL, Y_PSL), matrix_mul, matrix_inv)
    s_w23 = evaluate_generic(combined, MATRIX_ONE, (X_PSL, Y_PSL), matrix_mul, matrix_inv)
    require(g_w2 == g_w3 == g_w23 == EXPECTED_G07, "COARSE_G36_MARK_MISMATCH")
    require(s_w2 == s_w3 == s_w23 == MATRIX_ONE, "COARSE_PSL_MARK_MISMATCH")
    require(source2.eval_word(combined) == source2.one and source3.eval_word(combined) == source3.one, "SOURCE_Q_IDENTITY_MISMATCH")
    print("R07_P23_MARK_PASS g36=[[4,0],[32,0],[0,0]] psl=1 q2=1 q3=1", flush=True)

    theta_word = word_mul(substitute_word(combined, THETA), combined)
    tau_word = word_mul(word_mul(combined, substitute_word(combined, TAU)), substitute_word(combined, TAU2))
    relation_models: tuple[tuple[str, object, tuple[object, object], Callable, Callable], ...] = (
        ("G36", G36_ONE, (X36, Y36), g36_mul, g36_inv),
        ("PSL2_8", MATRIX_ONE, (X_PSL, Y_PSL), matrix_mul, matrix_inv),
        ("Q2", source2.one, source2.generators, source2.mul, source2.inv),
        ("Q3", source3.one, source3.generators, source3.mul, source3.inv),
    )
    theta_components: dict[str, bool] = {}
    tau_components: dict[str, bool] = {}
    for name, one, generators, mul, inv in relation_models:
        theta_components[name] = evaluate_generic(theta_word, one, generators, mul, inv) == one
        tau_components[name] = evaluate_generic(tau_word, one, generators, mul, inv) == one
    require(all(theta_components.values()), "THETA_HEXAGON_FAILURE")
    require(all(tau_components.values()), "TAU_HEXAGON_FAILURE")
    print("R07_P23_HEXAGONS_PASS theta_components=4 tau_components=4", flush=True)

    source2_elements, source2_derived = algebra_group_data(source2, 128)
    source3_elements, source3_derived = algebra_group_data(source3, 2187)
    g36_derived = derived_subgroup(g36_elements, G36_ONE, (X36, Y36), g36_mul, g36_inv)
    psl_derived = derived_subgroup(psl_elements, MATRIX_ONE, (X_PSL, Y_PSL), matrix_mul, matrix_inv)
    sums = exponent_sums(combined)
    charming_components = {
        "exponent_sums_mod36": sums[0] % 36 == 0 and sums[1] % 36 == 0,
        "G36_derived_membership": g_w23 in g36_derived,
        "PSL2_8_derived_membership": s_w23 in psl_derived,
        "Q2_derived_membership": source2.eval_word(combined) in source2_derived,
        "Q3_derived_membership": source3.eval_word(combined) in source3_derived,
    }
    require(len(g36_derived) == 1458 and len(psl_derived) == 504, "COARSE_DERIVED_ORDER_MISMATCH")
    require(len(source2_derived) == 8 and len(source3_derived) == 27, "SOURCE_DERIVED_ORDER_MISMATCH")
    require(all(charming_components.values()), "CHARMING_FAILURE")
    print(f"R07_P23_CHARMING_PASS exponent_sums={sums[0]},{sums[1]} derived_orders=1458,504,8,27", flush=True)

    # m=0, hence u=2m+1=1 and the marked endomorphism is
    # x -> x, y -> f*y*f^-1 in every source factor.
    def conjugated_y(f_value: T, y_value: T, mul: Callable[[T, T], T], inv: Callable[[T], T]) -> T:
        return mul(mul(f_value, y_value), inv(f_value))

    onto_orders = {
        "G36": len(enumerate_generated(G36_ONE, (X36, conjugated_y(g_w23, Y36, g36_mul, g36_inv)), g36_mul, g36_inv)),
        "PSL2_8": len(enumerate_generated(MATRIX_ONE, (X_PSL, conjugated_y(s_w23, Y_PSL, matrix_mul, matrix_inv)), matrix_mul, matrix_inv)),
        "Q2": len(enumerate_generated(source2.one, (source2.generators[0], conjugated_y(source2.eval_word(combined), source2.generators[1], source2.mul, source2.inv)), source2.mul, source2.inv)),
        "Q3": len(enumerate_generated(source3.one, (source3.generators[0], conjugated_y(source3.eval_word(combined), source3.generators[1], source3.mul, source3.inv)), source3.mul, source3.inv)),
    }
    require(onto_orders == {"G36": 23_328, "PSL2_8": 504, "Q2": 128, "Q3": 2187}, f"ONTO_FACTOR_ORDER_MISMATCH:{onto_orders}")
    print("R07_P23_ONTO_PASS G36=23328 PSL2_8=504 Q2=128 Q3=2187", flush=True)

    result: dict[str, object] = {
        "schema": SCHEMA,
        "status": "PASS",
        "scope": {
            "finite_fixed_row36_joint_literal_canary_only": True,
            "cross_checked_claim_emitted": False,
            "verified": False,
            "fake_or_ihara_witness_claimed": False,
            "cofinal_or_all_prime_claimed": False,
        },
        "independence_firewall": {
            "stdlib_only": True,
            "producer_or_receipt_opened_or_imported": False,
            "repository_helper_opened_or_imported": False,
            "embedded_authoritative_words": True,
        },
        "input_pins": list(INPUT_PINS),
        "words": {
            **static,
            "d_signed_word": list(discrepancy),
            "w23_signed_word": list(combined),
            "crt_moduli": [order2, order3],
        },
        "relation_complete_orders": {
            "p2_component_orders_source_then_five_cofaces": orders2,
            "p2_tuple_order": order2,
            "p3_component_orders_source_then_five_cofaces": orders3,
            "p3_tuple_order": order3,
        },
        "quotients": {
            "source_filtration_dimensions": list(source2.filtration_dimensions()),
            "pb4_filtration_dimensions": list(pb42.filtration_dimensions()),
            "source_orders": {"Q2": len(source2_elements), "Q3": len(source3_elements)},
            "derived_orders": {"G36": len(g36_derived), "PSL2_8": len(psl_derived), "Q2": len(source2_derived), "Q3": len(source3_derived)},
        },
        "gates": {
            "A_mark": {"G36": [[a, e] for a, e in g_w23], "PSL2_8_identity": s_w23 == MATRIX_ONE},
            "Q2_identity": source2.eval_word(combined) == source2.one,
            "Q3_identity": source3.eval_word(combined) == source3.one,
            "cofaces": {"p2": {name: value == pb42.one for name, value in cofaces2.items()}, "p3": {name: value == pb43.one for name, value in cofaces3.items()}},
            "printed_A18": {
                "order": [f"{name}{'^-1' if sign < 0 else ''}" for name, sign in PRINTED_A18],
                "p2_identity": a18_2 == pb42.one,
                "p3_identity": a18_3 == pb43.one,
                "p2_coordinate_sha256": digest_obj(list(pb42.coords(a18_2))),
                "p3_coordinate_sha256": digest_obj(list(pb43.coords(a18_3))),
            },
            "theta": {"word_length": len(theta_word), "word_sha256": digest_obj(list(theta_word)), "components": theta_components},
            "tau": {"word_length": len(tau_word), "word_sha256": digest_obj(list(tau_word)), "components": tau_components},
            "charming": charming_components,
            "onto_factor_orders": onto_orders,
        },
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "terminal_token": "R07_P23_JOINT_LITERAL_INDEPENDENT_PASS__FINITE_SCOPE",
    }
    result["self_digest_sha256"] = digest_obj(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true", help="static quick test; no finite quotient construction")
    parser.add_argument("--out-dir", type=pathlib.Path, default=pathlib.Path("ci/out"))
    args = parser.parse_args()
    if args.selftest:
        payload = static_selftest()
        print("R07_P23_JOINT_CHECKER_SELFTEST status=PASS " + " ".join(f"{key}={value}" for key, value in payload.items() if key in ("d_length", "a", "w23_length")), flush=True)
        return 0

    result = run_full()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.out_dir / RESULT_NAME
    output_bytes = canonical_json_bytes(result) + b"\n"
    output_path.write_bytes(output_bytes)
    print(f"R07_P23_RESULT path={output_path.as_posix()} bytes={len(output_bytes)} sha256={hashlib.sha256(output_bytes).hexdigest()}", flush=True)
    print(f"{FINAL_MARKER} status=PASS terminal={result['terminal_token']}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"{FINAL_MARKER} status=FAIL reason={type(exc).__name__}:{exc}", file=sys.stderr, flush=True)
        raise
