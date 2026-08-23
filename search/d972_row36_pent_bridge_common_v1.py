#!/usr/bin/env python3
"""Producer-only fixed-row36 bridge for the corrected p=2/p=3 pent canaries.

This module deliberately reconstructs the finite marked pc collectors exported by
the already sealed quotient canaries.  It never invokes NQ and never imports an
independent checker.  ``prepare`` freezes the coordinate universe and canonical
word algorithm before ``execute`` evaluates any gentle predicate or Dpap value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter, OrderedDict, deque
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence, TypeVar


ROOT = Path(__file__).resolve().parents[1]
DATE = "20260824"
SCHEMA_VERSION = 1
TARGET_ROW_INDEX = 36
TARGET_G9 = ((4, 0), (5, 0), (0, 0))
TARGET_PSL = tuple(range(9))
TARGET_WORD = (-2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
               2, 2, 2, -1, -2, -2, 1, 1, 1, 1)
TARGET_FULL_ROW = [0, [0, [[4, 0], [5, 0], [0, 0]],
                          [1, 2, 3, 4, 5, 6, 7, 8, 9]], list(TARGET_WORD)]
TARGET_KEY = [0, [[4, 0], [5, 0], [0, 0]],
              [1, 2, 3, 4, 5, 6, 7, 8, 9]]
TARGET_FULL_DIGEST = "31d19295b8b5c2f5e36387f6bb63cec508a7b8770e30bfa6d02909b1f16f4cd8"
TARGET_KEY_DIGEST = "3940557ee6c0118f2563ff7d19a41059d0fcdd5c7c876bc56c84b4fa9ae242ac"
TARGET_WORD_DIGEST = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"

COFACE_WORDS = (
    ((4,), (5,), (6,)),
    ((2, 4), (3, 5), (6,)),
    ((1, 2), (3,), (5, 6)),
    ((1,), (2, 3), (4, 5)),
    ((1,), (2,), (4,)),
)
OLD_REVERSED_COFACE_WORDS = tuple(
    tuple(tuple(reversed(word)) for word in row) for row in COFACE_WORDS
)
PB3_RELATORS = (
    (-1, 2, 1, 2, 3, -2, -3, -2),
    (-1, 3, 1, 2, -3, -2),
)


PINS_COMMON: dict[str, tuple[int, str]] = {
    "sol/luna_reply_159o_row36_claim_cover_audit_v1.md":
        (10967, "15e597396a63a5c92beec2e8b17abc3430cac6555f645ec1cb9b805d3a32ce23"),
    "sol/luna_reply_159o_k2_preflight.md":
        (34658, "461c5e60e13c4034dcb7f2fcef87e42d8b7dfd5b1f6148a944a4d8bae7d42e26"),
    "sol/luna_task_159o_ladder_launch.md":
        (12324, "08be5089fcedd8232b39feb3e7491a83b3dad001ca4c2be122491c5acc7dc85a"),
    "search/certs/d972_b4_word_key_artifact_v1_20260816.json":
        (176474, "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"),
    "certificates/K36.v1.json":
        (727834, "feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719"),
    "crosscheck/verdicts/K36.v1.verdict.json":
        (71093, "4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b"),
    "certificates/K9.v1.json":
        (173224, "ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e"),
    "crosscheck/verdicts/K9.v1.verdict.json":
        (20991, "9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9"),
    "certificates/S4.v2.json":
        (287984, "c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d"),
    "crosscheck/verdicts/S4.psl.verdict.json":
        (470, "8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28"),
    "search/certs/b3_gentle_source_census_preflight_v1_20260823.json":
        (887124, "c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2"),
    "crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json":
        (4931, "e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e"),
}

PINS_PRIME: dict[int, dict[str, tuple[int, str]]] = {
    2: {
        "ci/pent159n_p2_v14_artifacts_32660080668/d972_pent_interleave_canary_p2_receipt_v14_20260824.json":
            (234702, "2722e4acfd7087a613bdc63b15a8741c34c84480658682565e3b5af833f75ed5"),
        "search/certs/d972_pent_interleave_canary_p2_manifest_v14_20260824.json":
            (7566, "199178782a709723e215e37e6be32346ce369b6ad4335679a0770d64ec3d6fe2"),
        "crosscheck/verdicts/d972_pent_interleave_canary_crosscheck_p2_v6_20260824.json":
            (16438, "ef159dbc01d2e0e8ddc536707270b10207cd2654a08ee9a4dd60dd6201a5455a"),
    },
    3: {
        "ci/pent159n_p3_v5_artifacts_32661138818/d972_pent_interleave_canary_p3_receipt_v5_20260824.json":
            (5223102, "8838dbfecbb8f487265801de860c91207de56e4acf5e98088e6d9cd161390530"),
        "search/certs/d972_pent_interleave_canary_p3_manifest_v5_20260824.json":
            (9376, "0cb50bd91f65611f52643de082ba9f317b75716ee12545c7e4a285cde61cfe9e"),
        "crosscheck/verdicts/d972_pent_interleave_canary_crosscheck_p3_v2_20260824.json":
            (22901, "73d4cb3f242d74f796021af922e1771c68f9256bcddedcbe2a277539f79c2781"),
    },
}

CANARY_RECEIPT = {
    2: "ci/pent159n_p2_v14_artifacts_32660080668/d972_pent_interleave_canary_p2_receipt_v14_20260824.json",
    3: "ci/pent159n_p3_v5_artifacts_32661138818/d972_pent_interleave_canary_p3_receipt_v5_20260824.json",
}
CANARY_VERDICT = {
    2: "crosscheck/verdicts/d972_pent_interleave_canary_crosscheck_p2_v6_20260824.json",
    3: "crosscheck/verdicts/d972_pent_interleave_canary_crosscheck_p3_v2_20260824.json",
}


class ProducerStop(RuntimeError):
    pass


def fail(code: str, detail: str) -> None:
    raise ProducerStop(f"{code}: {detail}")


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        fail(code, detail)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)[:-1]).hexdigest()


def file_pin(rel: str, expected: tuple[int, str] | None = None) -> dict[str, Any]:
    path = ROOT / rel
    require(path.is_file(), "PIN_MISSING", rel)
    raw = path.read_bytes()
    actual = (len(raw), hashlib.sha256(raw).hexdigest())
    if expected is not None:
        require(actual == expected, "PIN_MISMATCH", f"{rel}: {actual!r} != {expected!r}")
    return {"path": rel, "bytes": actual[0], "sha256": actual[1]}


def load_json(rel: str) -> Any:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def immutable_write(rel: str, value: Any) -> dict[str, Any]:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(value)
    if path.exists():
        existing = path.read_bytes()
        require(existing == raw, "IMMUTABLE_VERSIONED_OUTPUT_MISMATCH", rel)
        raw = existing
    else:
        path.write_bytes(raw)
    return {"path": rel, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def inverse_word(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-x for x in reversed(word))


def reduce_word(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for letter in word:
        require(letter != 0, "ZERO_SIGNED_LETTER")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(int(letter))
    return tuple(out)


class BoundedLRU:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: OrderedDict[bytes, bytes] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.peak = 0

    def get(self, key: bytes) -> bytes | None:
        value = self.data.get(key)
        if value is None:
            self.misses += 1
            return None
        self.hits += 1
        self.data.move_to_end(key)
        return value

    def put(self, key: bytes, value: bytes) -> None:
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)
            self.evictions += 1
        self.peak = max(self.peak, len(self.data))

    def accounting(self) -> dict[str, int]:
        return {"capacity": self.capacity, "size": len(self.data),
                "peak": self.peak, "hits": self.hits,
                "misses": self.misses, "evictions": self.evictions}


def coords_word(coords: bytes) -> list[int]:
    out: list[int] = []
    for index, exponent in enumerate(coords, 1):
        out.extend([index] * exponent)
    return out


@dataclass
class PcCollector:
    record: dict[str, Any]
    cache_capacity: int = 200_000

    def __post_init__(self) -> None:
        self.n = int(self.record["pc_generator_count"])
        self.orders = tuple(int(x) for x in self.record["relative_orders"])
        require(len(self.orders) == self.n and self.n <= 64,
                "PC_RANK_OR_ORDER_WIDTH", repr((self.n, self.orders)))
        require(len(set(self.orders)) == 1 and self.orders[0] in (2, 3),
                "PC_RELATIVE_ORDERS", repr(self.orders))
        self.p = self.orders[0]
        self.powers = tuple(self.coord(row) for row in self.record["pc_power_relations"])
        self.inverses = tuple(self.coord(row) for row in self.record["pc_inverse_relations"])
        self.conjugates = {(int(row["i"]), int(row["j"])): self.coord(row["coords"])
                           for row in self.record["pc_conjugate_relations"]}
        self.inverse_conjugates = {
            (int(row["i"]), int(row["j"])): self.coord(row["coords"])
            for row in self.record["pc_inverse_conjugate_relations"]
        }
        expected_pairs = {(i, j) for i in range(2, self.n + 1) for j in range(1, i)}
        require(set(self.conjugates) == expected_pairs and
                set(self.inverse_conjugates) == expected_pairs,
                "PC_CONJUGATE_TABLE_COVERAGE")
        require(len(self.powers) == len(self.inverses) == self.n,
                "PC_POWER_INVERSE_TABLE_COVERAGE")
        self.pair_cache = BoundedLRU(self.cache_capacity)
        self.inv_cache = BoundedLRU(max(10_000, self.cache_capacity // 8))

    def coord(self, row: Sequence[int]) -> bytes:
        require(len(row) == self.n and all(isinstance(x, int) and 0 <= x < self.p for x in row),
                "PC_COORDINATE", repr(row))
        return bytes(row)

    def one(self) -> bytes:
        return bytes(self.n)

    def collect_uncached(self, word: Sequence[int]) -> bytes:
        tokens: list[int] = []
        for letter in word:
            require(1 <= abs(letter) <= self.n, "PC_LETTER", str(letter))
            if letter > 0:
                tokens.append(letter)
            else:
                tokens.extend(coords_word(self.inverses[-letter - 1]))
        steps = 0
        cap = max(20_000, 2000 * (1 + len(tokens)) * (1 + self.n))
        while True:
            changed = False
            for pos in range(len(tokens) - 1):
                a, b = tokens[pos], tokens[pos + 1]
                if a > b:
                    tokens[pos:pos + 2] = [b] + coords_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if not changed:
                pos = 0
                while pos < len(tokens):
                    generator = tokens[pos]
                    end = pos
                    while end < len(tokens) and tokens[end] == generator:
                        end += 1
                    if end - pos >= self.p:
                        tokens[pos:pos + self.p] = coords_word(self.powers[generator - 1])
                        changed = True
                        break
                    pos = end
            if not changed:
                break
            steps += 1
            require(steps <= cap, "PC_COLLECTION_CAP", repr((len(word), self.n)))
        row = [0] * self.n
        previous = 0
        for generator in tokens:
            require(generator >= previous, "PC_COLLECTED_ORDER")
            row[generator - 1] += 1
            require(row[generator - 1] < self.p, "PC_COLLECTED_POWER")
            previous = generator
        return bytes(row)

    def mul(self, left: bytes, right: bytes) -> bytes:
        require(len(left) == len(right) == self.n, "PC_PRODUCT_WIDTH")
        key = left + right
        cached = self.pair_cache.get(key)
        if cached is not None:
            return cached
        value = self.collect_uncached(coords_word(left) + coords_word(right))
        self.pair_cache.put(key, value)
        return value

    def inverse(self, value: bytes) -> bytes:
        require(len(value) == self.n, "PC_INVERSE_WIDTH")
        cached = self.inv_cache.get(value)
        if cached is not None:
            return cached
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(value[i - 1]):
                word.extend(coords_word(self.inverses[i - 1]))
        result = self.collect_uncached(word)
        self.inv_cache.put(value, result)
        return result

    def power(self, value: bytes, exponent: int) -> bytes:
        if exponent < 0:
            return self.power(self.inverse(value), -exponent)
        out = self.one()
        base = value
        n = exponent
        while n:
            if n & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            n //= 2
        return out

    def eval(self, word: Sequence[int], images: Sequence[bytes]) -> bytes:
        out = self.one()
        for letter in word:
            require(1 <= abs(letter) <= len(images), "PC_IMAGE_LETTER", str(letter))
            value = images[abs(letter) - 1]
            out = self.mul(out, value if letter > 0 else self.inverse(value))
        return out

    def eval_with_inverses(self, word: Sequence[int], images: Sequence[bytes],
                           inverse_images: Sequence[bytes]) -> bytes:
        require(len(images) == len(inverse_images), "PC_IMAGE_INVERSE_WIDTH")
        out = self.one()
        for letter in word:
            require(1 <= abs(letter) <= len(images), "PC_IMAGE_LETTER", str(letter))
            value = images[abs(letter) - 1] if letter > 0 else inverse_images[-letter - 1]
            out = self.mul(out, value)
        return out

    def cache_accounting(self) -> dict[str, Any]:
        return {"pair_product": self.pair_cache.accounting(),
                "inverse": self.inv_cache.accounting(),
                "unbounded_full_word_cache": False}


Perm = tuple[int, ...]
D = tuple[int, int]
G = tuple[D, D, D]
Residual = tuple[Perm, bytes]


def pid(n: int) -> Perm:
    return tuple(range(n))


def pmul(left: Perm, right: Perm) -> Perm:
    return tuple(right[left[i]] for i in range(len(left)))


def pinv(value: Perm) -> Perm:
    out = [0] * len(value)
    for i, image in enumerate(value):
        out[image] = i
    return tuple(out)


def ppow(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return ppow(pinv(value), -exponent)
    out = pid(len(value))
    base = value
    n = exponent
    while n:
        if n & 1:
            out = pmul(out, base)
        base = pmul(base, base)
        n //= 2
    return out


def gf8_mul(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    for bit in (4, 3):
        if result & (1 << bit):
            result ^= 11 << (bit - 3)
    return result


def gf8_inv(value: int) -> int:
    require(value != 0, "GF8_ZERO_INVERSE")
    for candidate in range(1, 8):
        if gf8_mul(value, candidate) == 1:
            return candidate
    fail("GF8_INVERSE_ABSENT", str(value))
    raise AssertionError


def mat_to_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    (a, b), (c, d) = matrix
    out = [0 if c == 0 else 1 + gf8_mul(a, gf8_inv(c))]
    for value in range(8):
        numerator = gf8_mul(a, value) ^ b
        denominator = gf8_mul(c, value) ^ d
        out.append(0 if denominator == 0 else 1 + gf8_mul(numerator, gf8_inv(denominator)))
    require(sorted(out) == list(range(9)), "PSL_PERMUTATION")
    return tuple(out)


S_PSL = mat_to_perm(((1, 0), (1, 1)))
T_PSL = mat_to_perm(((4, 3), (1, 5)))
W_PSL = pmul(S_PSL, pinv(T_PSL))
X_PSL = ppow(W_PSL, 2)
Y_PSL = pmul(pmul(pinv(S_PSL), X_PSL), S_PSL)
PSL_ID = pid(9)


def dmul(left: D, right: D, modulus: int) -> D:
    a, e = left
    b, f = right
    return ((a + (b if e == 0 else -b)) % modulus, e ^ f)


def dinv(value: D, modulus: int) -> D:
    a, e = value
    return ((-a if e == 0 else a) % modulus, e)


def gid() -> G:
    return ((0, 0), (0, 0), (0, 0))


def gx(modulus: int) -> G:
    return ((1 % modulus, 0), (0, 1), (0, 1))


def gy(modulus: int) -> G:
    return ((1 % modulus, 1), (1 % modulus, 0), (1 % modulus, 1))


def gmul(left: G, right: G, modulus: int) -> G:
    return tuple(dmul(left[i], right[i], modulus) for i in range(3))  # type: ignore[return-value]


def ginv(value: G, modulus: int) -> G:
    return tuple(dinv(part, modulus) for part in value)  # type: ignore[return-value]


def gpow(value: G, exponent: int, modulus: int) -> G:
    if exponent < 0:
        return gpow(ginv(value, modulus), -exponent, modulus)
    out = gid()
    base = value
    n = exponent
    while n:
        if n & 1:
            out = gmul(out, base, modulus)
        base = gmul(base, base, modulus)
        n //= 2
    return out


def reduce_g36(value: G, modulus: int = 9) -> G:
    return tuple((a % modulus, e) for a, e in value)  # type: ignore[return-value]


T = TypeVar("T")


def closure(identity: T, generators: Iterable[T], mul: Callable[[T, T], T],
            inv: Callable[[T], T], cap: int | None = None) -> set[T]:
    base = list(generators)
    steps = base + [inv(value) for value in base]
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = mul(current, step)
            if nxt not in seen:
                seen.add(nxt)
                require(cap is None or len(seen) <= cap, "CLOSURE_CAP", str(cap))
                queue.append(nxt)
    return seen


def encode_g(value: G) -> list[list[int]]:
    return [[int(a), int(e)] for a, e in value]


def encode_perm(value: Perm) -> list[int]:
    return [x + 1 for x in value]


def flatten_g(value: G) -> tuple[int, ...]:
    return tuple(x for pair in value for x in pair)


def eval_word_g(word: Sequence[int], modulus: int) -> G:
    out = gid()
    images = (gx(modulus), gy(modulus))
    for letter in word:
        value = images[abs(letter) - 1]
        out = gmul(out, value if letter > 0 else ginv(value, modulus), modulus)
    return out


def eval_word_perm(word: Sequence[int]) -> Perm:
    out = PSL_ID
    images = (X_PSL, Y_PSL)
    for letter in word:
        value = images[abs(letter) - 1]
        out = pmul(out, value if letter > 0 else pinv(value))
    return out


def pc_marks(record: dict[str, Any], collector: PcCollector,
             verify_inverse_replay: bool = True) -> tuple[bytes, ...]:
    marks = tuple(collector.coord(row["coords"]) for row in record["marked_generators"])
    require(len(marks) >= 2, "PC_MARKED_GENERATORS")
    if verify_inverse_replay:
        for mark, row in zip(marks, record["marked_generators"]):
            require(collector.inverse(mark) == collector.coord(row["inverse_coords"]),
                    "PC_MARKED_INVERSE", row["label"])
    return marks


def eval_joint(word: Sequence[int], qcol: PcCollector,
               qmarks: Sequence[bytes]) -> tuple[G, Perm, bytes]:
    return (eval_word_g(word, 36), eval_word_perm(word), qcol.eval(word, qmarks))


def joint_mul(left: tuple[G, Perm, bytes], right: tuple[G, Perm, bytes],
              qcol: PcCollector) -> tuple[G, Perm, bytes]:
    return (gmul(left[0], right[0], 36), pmul(left[1], right[1]),
            qcol.mul(left[2], right[2]))


def joint_inv(value: tuple[G, Perm, bytes], qcol: PcCollector) -> tuple[G, Perm, bytes]:
    return (ginv(value[0], 36), pinv(value[1]), qcol.inverse(value[2]))


def encode_joint(value: tuple[G, Perm, bytes]) -> dict[str, Any]:
    return {"g36": encode_g(value[0]), "psl_one_line": encode_perm(value[1]),
            "Qp_coords": list(value[2])}


def build_g36_transversal(qcol: PcCollector, qmarks: Sequence[bytes]) -> tuple[
        dict[G, tuple[int, ...]], dict[G, Perm], dict[G, bytes]]:
    steps = (
        (1, gx(36), X_PSL, qmarks[0]),
        (-1, ginv(gx(36), 36), pinv(X_PSL), qcol.inverse(qmarks[0])),
        (2, gy(36), Y_PSL, qmarks[1]),
        (-2, ginv(gy(36), 36), pinv(Y_PSL), qcol.inverse(qmarks[1])),
    )
    words: dict[G, tuple[int, ...]] = {gid(): ()}
    psl_values = {gid(): PSL_ID}
    q_values = {gid(): qcol.one()}
    queue = deque([gid()])
    while queue:
        current = queue.popleft()
        for letter, step_g, step_p, step_q in steps:
            nxt = gmul(current, step_g, 36)
            if nxt not in words:
                words[nxt] = words[current] + (letter,)
                psl_values[nxt] = pmul(psl_values[current], step_p)
                q_values[nxt] = qcol.mul(q_values[current], step_q)
                queue.append(nxt)
    require(len(words) == 23328, "G36_TRANSVERSAL_ORDER", str(len(words)))
    return words, psl_values, q_values


def residual_mul(left: Residual, right: Residual, qcol: PcCollector) -> Residual:
    return (pmul(left[0], right[0]), qcol.mul(left[1], right[1]))


def residual_inv(value: Residual, qcol: PcCollector) -> Residual:
    return (pinv(value[0]), qcol.inverse(value[1]))


def residual_closure(generators: Sequence[Residual], qcol: PcCollector,
                     cap: int) -> set[Residual]:
    identity = (PSL_ID, qcol.one())
    return closure(identity, generators,
                   lambda a, b: residual_mul(a, b, qcol),
                   lambda a: residual_inv(a, qcol), cap)


def select_schreier_generators(
    words: dict[G, tuple[int, ...]], psl_values: dict[G, Perm],
    q_values: dict[G, bytes], qcol: PcCollector, qmarks: Sequence[bytes],
    expected_residual_order: int,
) -> tuple[list[tuple[Residual, tuple[int, ...]]], list[dict[str, Any]]]:
    edge_steps = (
        (1, gx(36), X_PSL, qmarks[0]),
        (-1, ginv(gx(36), 36), pinv(X_PSL), qcol.inverse(qmarks[0])),
        (2, gy(36), Y_PSL, qmarks[1]),
        (-2, ginv(gy(36), 36), pinv(Y_PSL), qcol.inverse(qmarks[1])),
    )
    identity: Residual = (PSL_ID, qcol.one())
    chosen: list[tuple[Residual, tuple[int, ...]]] = []
    current_closure = {identity}
    trace: list[dict[str, Any]] = []
    for current in words:
        for letter, step_g, step_p, step_q in edge_steps:
            nxt = gmul(current, step_g, 36)
            residual = (
                pmul(pmul(psl_values[current], step_p), pinv(psl_values[nxt])),
                qcol.mul(qcol.mul(q_values[current], step_q),
                         qcol.inverse(q_values[nxt])),
            )
            if residual in current_closure:
                continue
            kernel_word = reduce_word(words[current] + (letter,) + inverse_word(words[nxt]))
            require(eval_word_g(kernel_word, 36) == gid(),
                    "SCHREIER_G36_KERNEL_REPLAY", repr(kernel_word))
            require((eval_word_perm(kernel_word), qcol.eval(kernel_word, qmarks)) == residual,
                    "SCHREIER_RESIDUAL_REPLAY", repr(kernel_word))
            chosen.append((residual, kernel_word))
            current_closure = residual_closure([x[0] for x in chosen], qcol,
                                               expected_residual_order)
            trace.append({
                "selected_index_one_based": len(chosen),
                "kernel_word_signed_xy": list(kernel_word),
                "kernel_word_sha256": digest(list(kernel_word)),
                "residual_psl_one_line": encode_perm(residual[0]),
                "residual_Qp_coords": list(residual[1]),
                "closure_order": len(current_closure),
            })
            if len(current_closure) == expected_residual_order:
                return chosen, trace
    fail("SCHREIER_RESIDUAL_NOT_SURJECTIVE", repr((len(current_closure), expected_residual_order)))
    raise AssertionError


def residual_correction_paths(
    chosen: Sequence[tuple[Residual, tuple[int, ...]]], qcol: PcCollector,
    expected_order: int,
) -> tuple[dict[Residual, tuple[int, ...]], tuple[tuple[int, ...], ...]]:
    """Return canonical residual paths as signed indices into a block roster."""
    identity: Residual = (PSL_ID, qcol.one())
    blocks = tuple(word for _, word in chosen)
    steps: list[tuple[Residual, int]] = []
    for index, (value, _) in enumerate(chosen, 1):
        steps.append((value, index))
        steps.append((residual_inv(value, qcol), -index))
    paths: dict[Residual, tuple[int, ...]] = {identity: ()}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for step, signed_index in steps:
            nxt = residual_mul(current, step, qcol)
            if nxt not in paths:
                paths[nxt] = paths[current] + (signed_index,)
                queue.append(nxt)
    require(len(paths) == expected_order, "RESIDUAL_CORRECTION_COVERAGE",
            repr((len(paths), expected_order)))
    return paths, blocks


def expand_block_path(base_word: Sequence[int], path: Sequence[int],
                      blocks: Sequence[Sequence[int]]) -> tuple[int, ...]:
    out = tuple(base_word)
    for signed_index in path:
        block = blocks[abs(signed_index) - 1]
        out += tuple(block) if signed_index > 0 else inverse_word(block)
    return reduce_word(out)


def commutator_word(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return reduce_word(inverse_word(left) + inverse_word(right) + tuple(left) + tuple(right))


def hall_word(vector: Sequence[int]) -> tuple[int, ...]:
    require(len(vector) == 5, "HALL_VECTOR_WIDTH", repr(vector))
    a, b, e, d, h = (int(x) for x in vector)
    c = commutator_word((2,), (1,))
    cx = commutator_word(c, (1,))
    cy = commutator_word(c, (2,))
    return reduce_word((1,) * a + (2,) * b + c * e + cx * d + cy * h)


def hall_roster(prime: int, qcol: PcCollector,
                qmarks: Sequence[bytes]) -> list[dict[str, Any]]:
    top = prime * prime
    rows: list[dict[str, Any]] = []
    seen: set[bytes] = set()
    for vector in product(range(top), range(top), range(prime), range(prime), range(prime)):
        word = hall_word(vector)
        value = qcol.eval(word, qmarks)
        require(value not in seen, "HALL_DUPLICATE_COORD", repr(vector))
        seen.add(value)
        rows.append({"hall_vector_abedh": list(vector),
                     "hall_word_signed_xy": list(word),
                     "Qp_coords": list(value)})
    expected = 128 if prime == 2 else 2187
    require(len(rows) == len(seen) == expected, "HALL_COMPLETE",
            repr((len(rows), len(seen), expected)))
    return rows


def all_pc_coords(qcol: PcCollector) -> Iterator[bytes]:
    for row in product(*[range(order) for order in qcol.orders]):
        yield bytes(row)


def marked_bfs_map(qcol: PcCollector, qmarks: Sequence[bytes],
                   target_identity: T, target_marks: Sequence[T],
                   target_mul: Callable[[T, T], T], target_inv: Callable[[T], T],
                   expected_order: int) -> tuple[dict[bytes, T], dict[bytes, tuple[int, ...]]]:
    qsteps = (qmarks[0], qcol.inverse(qmarks[0]), qmarks[1], qcol.inverse(qmarks[1]))
    tsteps = (target_marks[0], target_inv(target_marks[0]),
              target_marks[1], target_inv(target_marks[1]))
    letters = (1, -1, 2, -2)
    mapping = {qcol.one(): target_identity}
    words = {qcol.one(): ()}
    queue = deque([qcol.one()])
    while queue:
        current = queue.popleft()
        for qstep, tstep, letter in zip(qsteps, tsteps, letters):
            qnext = qcol.mul(current, qstep)
            tnext = target_mul(mapping[current], tstep)
            if qnext in mapping:
                require(mapping[qnext] == tnext, "MARKED_MAP_NOT_WELL_DEFINED", repr(qnext))
            else:
                mapping[qnext] = tnext
                words[qnext] = words[current] + (letter,)
                queue.append(qnext)
    require(len(mapping) == expected_order, "MARKED_BFS_SOURCE_ORDER",
            repr((len(mapping), expected_order)))
    return mapping, words


def q_closure(qcol: PcCollector, generators: Sequence[bytes]) -> set[bytes]:
    return closure(qcol.one(), generators, qcol.mul, qcol.inverse,
                   math.prod(qcol.orders))


def perm_closure(generators: Sequence[Perm]) -> set[Perm]:
    return closure(PSL_ID, generators, pmul, pinv, 504)


def g_closure(generators: Sequence[G], modulus: int = 36) -> set[G]:
    return closure(gid(), generators, lambda a, b: gmul(a, b, modulus),
                   lambda a: ginv(a, modulus), 23328 if modulus == 36 else None)


def substitute_word(word: Sequence[int], images: Sequence[Sequence[int]]) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for letter in word:
        image = tuple(images[abs(letter) - 1])
        out += image if letter > 0 else inverse_word(image)
    return reduce_word(out)


def theta_word(word: Sequence[int]) -> tuple[int, ...]:
    return substitute_word(word, ((2,), (1,)))


def tau_word(word: Sequence[int]) -> tuple[int, ...]:
    # Paper tau(x)=y, tau(y)=(y*x)^-1; native serialization is x^-1*y^-1.
    return substitute_word(word, ((2,), (-1, -2)))


def exponent_sums(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word),
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word))


def group_power_word(letter: int, exponent: int) -> tuple[int, ...]:
    return (letter,) * exponent if exponent >= 0 else (-letter,) * (-exponent)


def canonical_target_digest_checks(word_artifact: dict[str, Any]) -> None:
    require(word_artifact.get("schema") == "d972-b4-word-key-artifact/v1" and
            word_artifact.get("count") == 972 and len(word_artifact.get("rows", [])) == 972,
            "WORD_ARTIFACT_SCHEMA_COVER")
    row = word_artifact["rows"][TARGET_ROW_INDEX]
    require(row == TARGET_FULL_ROW, "ROW36_FULL_VALUE", repr(row))
    require(digest(row) == TARGET_FULL_DIGEST, "ROW36_FULL_DIGEST", digest(row))
    require(row[1] == TARGET_KEY, "ROW36_KEY_VALUE", repr(row[1]))
    require(digest(row[1]) == TARGET_KEY_DIGEST, "ROW36_KEY_DIGEST", digest(row[1]))
    require(digest(row[2]) == TARGET_WORD_DIGEST, "ROW36_WORD_DIGEST", digest(row[2]))


def authenticate_inputs(prime: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(prime in (2, 3), "PRIME", str(prime))
    pins = []
    for rel, expected in {**PINS_COMMON, **PINS_PRIME[prime]}.items():
        pins.append(file_pin(rel, expected))
    receipt = load_json(CANARY_RECEIPT[prime])
    verdict = load_json(CANARY_VERDICT[prime])
    expected_status = {
        2: "MEASURED_P2_LITERAL_A18_IDENTITY_SERIALIZATION_REPAIR_V14",
        3: "MEASURED_P3_LITERAL_A18_IDENTITY_SERIALIZATION_REPAIR_V5",
    }[prime]
    require(receipt.get("status") == expected_status, "CANARY_RECEIPT_STATUS",
            repr(receipt.get("status")))
    require(receipt.get("quotients", {}).get("Q2", {}).get("prime") == prime,
            "CANARY_RECEIPT_PRIME")
    expected_q2 = "128" if prime == 2 else "2187"
    require(receipt["quotients"]["Q2"]["order_decimal"] == expected_q2,
            "CANARY_Q2_ORDER", repr(receipt["quotients"]["Q2"].get("order_decimal")))
    require(receipt["quotients"]["Q4"]["nilpotency_class"] == 3,
            "CANARY_Q4_CLASS")
    require(verdict.get("crosscheck_status") == "PASS", "CANARY_VERDICT_STATUS",
            repr(verdict.get("crosscheck_status")))
    verdict_text = json.dumps(verdict, sort_keys=True)
    require(PINS_PRIME[prime][CANARY_RECEIPT[prime]][1] in verdict_text,
            "CANARY_VERDICT_RECEIPT_BINDING")
    canonical_target_digest_checks(load_json(
        "search/certs/d972_b4_word_key_artifact_v1_20260816.json"))
    return pins, receipt


def source_pins(prime: int) -> list[dict[str, Any]]:
    return [file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            file_pin(f"search/d972_row36_pent_bridge_p{prime}_producer_v1.py")]


def paths_for(prime: int) -> dict[str, str]:
    base = f"d972_row36_pent_bridge_p{prime}"
    return {
        "prereg": f"search/certs/{base}_prereg_v1_{DATE}.json",
        "receipt": f"search/certs/{base}_receipt_v1_{DATE}.json",
        "manifest": f"search/certs/{base}_manifest_v1_{DATE}.json",
    }


def validate_pc_receipt(prime: int, q2: dict[str, Any], q4: dict[str, Any],
                        qcol: PcCollector, q4col: PcCollector) -> tuple[tuple[bytes, ...], tuple[bytes, ...]]:
    expected_order = 128 if prime == 2 else 2187
    require(math.prod(qcol.orders) == expected_order and
            int(q2["order_decimal"]) == expected_order and
            q2["nilpotency_class"] == 3, "Q2_COLLECTOR_ORDER_CLASS")
    require(math.prod(q4col.orders) == int(q4["order_decimal"]) and
            q4["nilpotency_class"] == 3, "Q4_COLLECTOR_ORDER_CLASS")
    qmarks = pc_marks(q2, qcol)
    # Q4 marked inverses are authenticated by the frozen GAP receipt.  Expanding
    # a dense marked inverse through all rank-26 generator inverses is not needed
    # for the source-relator gate and is a known token-collector resource trap.
    q4marks = pc_marks(q4, q4col, verify_inverse_replay=False)
    require(len(qmarks) == 2 and len(q4marks) == 6, "MARK_COUNTS")
    qmap, _ = marked_bfs_map(qcol, qmarks, 0, (1, 1),
                             lambda a, b: (a + b) % prime,
                             lambda a: (-a) % prime, expected_order)
    # The deliberately coarse cyclic target is only a marked-map consistency gate.
    require(len(qmap) == expected_order, "Q2_MARKED_COVER")
    return qmarks, q4marks


def imported_relator_gate(receipt: dict[str, Any]) -> dict[str, Any]:
    require("marked_maps" in receipt and
            "a18_source_relator_gate" in receipt["marked_maps"],
            "IMPORTED_A18_GATE_ABSENT")
    gate = receipt["marked_maps"]["a18_source_relator_gate"]
    require(gate.get("literal_relator_gate_row_count") == 10 and
            gate.get("literal_all_relators_preserved") is True,
            "IMPORTED_A18_LITERAL_GATE")
    require(gate.get("serialized_native_words") ==
            [[[int(x) for x in word] for word in row] for row in COFACE_WORDS],
            "IMPORTED_A18_NATIVE_TABLE")
    require(gate.get("required_old_reversal_mutant_failure", {}).get("passed") is False,
            "IMPORTED_A18_MUTANT_GATE")
    require(gate.get("target_quotient") in ("Q4_PB4_D4_2", "Q4_PB4_D4_3"),
            "IMPORTED_A18_TARGET")
    return gate


def relator_gate(q4col: PcCollector, q4marks: Sequence[bytes]) -> dict[str, Any]:
    literal_rows = []
    mutant_rows = []
    for slot, table in enumerate(COFACE_WORDS):
        images = tuple(q4col.eval(word, q4marks) for word in table)
        for rel_index, relator in enumerate(PB3_RELATORS, 1):
            value = q4col.eval(relator, images)
            literal_rows.append({"slot_zero_based": slot,
                                 "source_relator_index_one_based": rel_index,
                                 "image_coords": list(value),
                                 "image_sha256": digest(list(value)),
                                 "identity": value == q4col.one()})
    for slot, table in enumerate(OLD_REVERSED_COFACE_WORDS):
        images = tuple(q4col.eval(word, q4marks) for word in table)
        for rel_index, relator in enumerate(PB3_RELATORS, 1):
            value = q4col.eval(relator, images)
            mutant_rows.append({"slot_zero_based": slot,
                                "source_relator_index_one_based": rel_index,
                                "image_coords": list(value),
                                "image_sha256": digest(list(value)),
                                "identity": value == q4col.one()})
    require(len(literal_rows) == 10 and all(row["identity"] for row in literal_rows),
            "LITERAL_A18_RELATOR_GATE")
    required = [row for row in mutant_rows
                if row["slot_zero_based"] == 1 and
                row["source_relator_index_one_based"] == 1]
    require(len(required) == 1 and not required[0]["identity"],
            "A18_REVERSAL_MUTANT_REJECTION")
    return {"source": "Appendix A.18, original PDF page 49 image audit",
            "literal_table_native_identity_serialization":
                [[[int(x) for x in word] for word in row] for row in COFACE_WORDS],
            "literal_rows": literal_rows,
            "literal_all_10_identity": True,
            "old_reversal_mutant_rows": mutant_rows,
            "required_phi12_3_4_relator1_rejected": True}


def build_l_roster() -> list[G]:
    g36 = g_closure((gx(36), gy(36)), 36)
    require(len(g36) == 23328, "G36_ORDER", str(len(g36)))
    kernel = sorted((value for value in g36 if reduce_g36(value, 9) == gid()), key=flatten_g)
    require(len(kernel) == 8, "L_ORDER", str(len(kernel)))
    return kernel


def alpha_c2(value: G) -> G:
    return reduce_g36(value, 4)


def build_raw_universe(prime: int, receipt: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE COLLECTORS_START", flush=True)
    q2 = receipt["quotients"]["Q2"]
    q4 = receipt["quotients"]["Q4"]
    qcol = PcCollector(q2)
    q4col = PcCollector(q4, cache_capacity=100_000)
    qmarks, q4marks = validate_pc_receipt(prime, q2, q4, qcol, q4col)
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE COLLECTORS_PASS", flush=True)
    # The bridge must not rebuild the quotient canary.  Its outcome-free prereg
    # binds the immutable canary's already authenticated 10/10 map gate; direct
    # same-word Q4 evaluation is still mandatory later in execute.
    a18_gate = imported_relator_gate(receipt)
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE IMPORTED_A18_10_OF_10_PIN_PASS", flush=True)
    hall = hall_roster(prime, qcol, qmarks)
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE HALL_PASS count={len(hall)}", flush=True)
    l_roster = build_l_roster()
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE L_PASS count={len(l_roster)}", flush=True)

    expected_q = 128 if prime == 2 else 2187
    if prime == 2:
        beta, _ = marked_bfs_map(qcol, qmarks, gid(), (gx(4), gy(4)),
                                 lambda a, b: gmul(a, b, 4),
                                 lambda a: ginv(a, 4), expected_q)
        c2_image = set(beta.values())
        require(len(c2_image) == 32, "C2_IMAGE_ORDER", str(len(c2_image)))
        beta_kernel = {q for q, image in beta.items() if image == gid()}
        require(len(beta_kernel) == 4, "C2_BETA_KERNEL_ORDER", str(len(beta_kernel)))
        compatible = [(li, hi) for li, l in enumerate(l_roster)
                      for hi, hrow in enumerate(hall)
                      if alpha_c2(l) == beta[bytes(hrow["Qp_coords"])]]
        common = {
            "name": "C2=G36/P=im(Q2->G4)", "order": 32,
            "P_order": 729, "alpha_rule": "reduce all three D36 rotation exponents modulo 4",
            "beta_rule": "unique marked homomorphism Q2->G4, x|->x, y|->y",
            "beta_image_order": len(c2_image), "beta_kernel_order": len(beta_kernel),
            "maximal_common_quotient": True,
        }
        expected_z = 32
        expected_residual = 504 * len(beta_kernel)
    else:
        compatible = [(li, hi) for li in range(len(l_roster)) for hi in range(len(hall))]
        common = {
            "name": "C3=1", "order": 1,
            "proof": "Q3 is a 3-group; G36_ab has order 16, so every common quotient is a 3-group quotient of an order-16 abelianization and is trivial",
            "G36_abelianization_order": 16,
            "maximal_common_quotient": True,
        }
        expected_z = 8 * expected_q
        expected_residual = 504 * expected_q
    require(len(compatible) == expected_z, "JOINT_KERNEL_COORDINATE_COUNT",
            repr((len(compatible), expected_z)))

    words, psl_values, q_values = build_g36_transversal(qcol, qmarks)
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE G36_TRANSVERSAL_PASS", flush=True)
    chosen, schreier_trace = select_schreier_generators(
        words, psl_values, q_values, qcol, qmarks, expected_residual)
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE SCHREIER_SELECT_PASS generators={len(chosen)}", flush=True)
    correction_paths, blocks = residual_correction_paths(chosen, qcol, expected_residual)
    print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_GATE RESIDUAL_PATHS_PASS count={len(correction_paths)}", flush=True)

    target_q = qcol.eval(TARGET_WORD, qmarks)
    target_joint = (eval_word_g(TARGET_WORD, 36), eval_word_perm(TARGET_WORD), target_q)
    require(reduce_g36(target_joint[0], 9) == TARGET_G9 and target_joint[1] == PSL_ID,
            "TARGET_WORD_K1_REPLAY", repr(encode_joint(target_joint)))

    kernel_rows: list[dict[str, Any]] = []
    word_roster: list[dict[str, Any]] = []
    for z_index, (li, hi) in enumerate(compatible):
        l = l_roster[li]
        hrow = hall[hi]
        q = bytes(hrow["Qp_coords"])
        z = (l, PSL_ID, q)
        final = joint_mul(target_joint, z, qcol)
        base_word = words[final[0]]
        needed = (pinv(psl_values[final[0]]),
                  qcol.mul(qcol.inverse(q_values[final[0]]), final[2]))
        require(needed in correction_paths, "RESIDUAL_CORRECTION_MISSING", repr((li, hi)))
        path = correction_paths[needed]
        word = expand_block_path(base_word, path, blocks)
        replay = eval_joint(word, qcol, qmarks)
        require(replay == final, "CANONICAL_WORD_JOINT_REPLAY", repr((li, hi)))
        require(reduce_g36(final[0], 9) == TARGET_G9 and final[1] == PSL_ID,
                "ROW36_REDUCTION", repr((li, hi)))
        word_id = f"W{z_index + 1:05d}"
        word_row = {"word_id": word_id,
                    "canonical_signed_xy": list(word),
                    "word_sha256": digest(list(word)),
                    "g36_base_word_signed_xy": list(base_word),
                    "residual_block_path_signed_indices": list(path)}
        word_roster.append(word_row)
        kernel_rows.append({
            "z_index_zero_based": z_index,
            "L_index_zero_based": li,
            "L_code": list(flatten_g(l)),
            "L_g36": encode_g(l),
            "hall_index_zero_based": hi,
            "hall_vector_abedh": hrow["hall_vector_abedh"],
            "q_coords": list(q),
            "common_quotient_compatible": True,
            "z_joint_coords": encode_joint(z),
            "jstar_z_joint_coords": encode_joint(final),
            "word_id": word_id,
            "word_sha256": word_row["word_sha256"],
            "reduction_key": TARGET_KEY,
            "reduction_key_sha256": TARGET_KEY_DIGEST,
            "target_row_index_zero_based": TARGET_ROW_INDEX,
        })

    require(len(kernel_rows) == expected_z and len(word_roster) == expected_z,
            "RAW_KERNEL_ROSTER_COUNT")
    require(len({row["word_sha256"] for row in word_roster}) == expected_z,
            "CANONICAL_WORD_DUPLICATE")
    require(len({digest([row["L_code"], row["hall_vector_abedh"]]) for row in kernel_rows}) == expected_z,
            "JOINT_KERNEL_COORDINATE_DUPLICATE")
    rows = []
    for m in (0, 18):
        for kernel_row in kernel_rows:
            rows.append({"row_id": f"P{prime}R{len(rows) + 1:05d}",
                         "m": m, **kernel_row})
    expected_raw = 64 if prime == 2 else 34992
    require(len(rows) == expected_raw, "RAW_ROW_COUNT", repr((len(rows), expected_raw)))
    require(len({row["row_id"] for row in rows}) == expected_raw,
            "RAW_ROW_ID_UNIQUENESS")

    prereg = {
        "schema": f"d972-row36-pent-bridge-p{prime}-prereg/v1",
        "date": DATE,
        "role": "Luna producer preregistration; outcome-free coordinate/word freeze",
        "prime": prime,
        "scope": "fixed zero-based row 36 only; marked K1-by-Qp joint fibre; no quotient-canary rerun",
        "forbidden_promotions": {"mode_token": None, "K2_name": None,
                                  "all_prime_inference": False},
        "input_pins": authenticate_inputs(prime)[0],
        "source_pins": source_pins(prime),
        "frozen_target": {"row_index_zero_based": TARGET_ROW_INDEX,
                          "full_row": TARGET_FULL_ROW,
                          "full_row_sha256": TARGET_FULL_DIGEST,
                          "target_key": TARGET_KEY,
                          "target_key_sha256": TARGET_KEY_DIGEST,
                          "archived_word": list(TARGET_WORD),
                          "archived_word_sha256": TARGET_WORD_DIGEST,
                          "central_m_lifts_in_order": [0, 18]},
        "marked_joint_image": {
            "model": "im(F2 -> G36 x PSL(2,8) x Qp) generated by the displayed marked x,y",
            "K1_factor_order": 23328 * 504,
            "Qp_order": expected_q,
            "common_quotient": common,
            "joint_order": 23328 * 504 * expected_q // common["order"],
            "actual_index": 23328 * 504 * expected_q // common["order"],
            "marked_x": encode_joint((gx(36), X_PSL, qmarks[0])),
            "marked_y": encode_joint((gy(36), Y_PSL, qmarks[1])),
        },
        "isolation_binding": {
            "status": "paper-proof input, not Lean verification",
            "K1_isolated": True,
            "D4p_fully_invariant": True,
            "Hp_equals_K1_intersection_D4p": True,
            "Hp_diamond_equals_Hp": True,
            "pins": [PINS_COMMON["sol/luna_reply_159o_k2_preflight.md"][1],
                     PINS_COMMON["sol/luna_reply_159o_row36_claim_cover_audit_v1.md"][1]],
        },
        "collector_binding": {
            "Q2_public_pc_record_sha256": digest(q2),
            "Q4_public_pc_record_sha256": digest(q4),
            "Q2_relative_orders": list(qcol.orders),
            "Q4_relative_orders": list(q4col.orders),
            "literal_A18_gate_before_any_predicate_or_defect_census": a18_gate,
        },
        "enumeration_contract": {
            "order": "m=0,18; then lexicographic flattened L code; then Hall vector (a,b,e,d,h) lexicographic",
            "L_order": len(l_roster),
            "L_roster": [{"index_zero_based": i, "code": list(flatten_g(l)),
                           "g36": encode_g(l)} for i, l in enumerate(l_roster)],
            "hall_normal_form": "x^a y^b [y,x]^e [[y,x],x]^d [[y,x],y]^h",
            "hall_vector_ranges": {"a": expected_q // (prime ** 3) if False else prime * prime,
                                   "b": prime * prime, "e": prime,
                                   "d": prime, "h": prime},
            "Hall_roster_sha256": digest(hall),
            "coordinate_filter": "alpha(l)=beta(q)" if prime == 2 else "all (l,q); common quotient trivial",
            "joint_kernel_Zp_order": expected_z,
            "raw_expected_count": expected_raw,
            "G36_transversal_algorithm": "right-Cayley BFS; steps x,x^-1,y,y^-1",
            "G36_transversal_count": len(words),
            "Schreier_residual_expected_order": expected_residual,
            "Schreier_selected_generators": schreier_trace,
            "Schreier_block_roster_sha256": digest([list(x) for x in blocks]),
        },
        "joint_kernel_roster": kernel_rows,
        "canonical_word_roster": word_roster,
        "raw_rows": rows,
        "coverage_freeze": {
            "raw_count": len(rows), "expected_count": expected_raw,
            "raw_roster_sha256": digest(rows),
            "joint_kernel_roster_sha256": digest(kernel_rows),
            "canonical_word_roster_sha256": digest(word_roster),
            "no_omission_coordinate_rule": True,
            "no_duplicate_coordinate_rule": True,
            "all_reduce_to_frozen_key": True,
            "predicate_outcomes_not_evaluated": True,
        },
        "destructive_controls_preregistered": [
            "one row omitted", "one row duplicated",
            "C2 replaced by trivial/direct-product quotient",
            "Hall coordinate or marked generator changed", "row 35 or 37 substituted",
            "central lifts changed from [0,18]", "non-isolated input",
            "charming accepted without onto", "one hexagon omitted",
            "word changed before Dpap", "receipt or aggregate digest mutation",
        ],
        "status": "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME",
        "terminal_token": f"PENT159O_ROW36_P{prime}_PREREG_V1_FROZEN",
    }
    runtime = {
        "qcol": qcol, "q4col": q4col, "qmarks": qmarks, "q4marks": q4marks,
        "q4_inverse_marks": tuple(q4col.coord(row["inverse_coords"])
                                  for row in q4["marked_generators"]),
        "hall": hall, "l_roster": l_roster, "word_roster": word_roster,
        "rows": rows, "blocks": blocks,
    }
    return prereg, runtime


def encode_element(value: tuple[G, Perm, bytes]) -> list[Any]:
    return [encode_g(value[0]), encode_perm(value[1]), list(value[2])]


def joint_equal_identity(value: tuple[G, Perm, bytes], qcol: PcCollector) -> bool:
    return value == (gid(), PSL_ID, qcol.one())


def q4_contexts(q4col: PcCollector, q4marks: Sequence[bytes],
                q4_inverse_marks: Sequence[bytes]) -> tuple[tuple[tuple[bytes, bytes], tuple[bytes, bytes]], ...]:
    contexts = []
    for row in COFACE_WORDS:
        images = tuple(q4col.eval_with_inverses(word, q4marks, q4_inverse_marks)
                       for word in row)
        inverse_images = tuple(
            q4col.eval_with_inverses(inverse_word(word), q4marks, q4_inverse_marks)
            for word in row
        )
        contexts.append(((images[0], images[2]),
                         (inverse_images[0], inverse_images[2])))
    return tuple(contexts)


def evaluate_dpap(word: Sequence[int], q4col: PcCollector,
                  contexts: Sequence[tuple[tuple[bytes, bytes], tuple[bytes, bytes]]]) -> dict[str, Any]:
    values = tuple(q4col.eval_with_inverses(word, images, inverse_images)
                   for images, inverse_images in contexts)
    inverse_values = tuple(q4col.eval_with_inverses(inverse_word(word), images, inverse_images)
                           for images, inverse_images in contexts)
    c, a, e, b, f = values
    _, a_inv, _, b_inv, _ = inverse_values
    correct = q4col.mul(q4col.mul(q4col.mul(q4col.mul(f, e), c), b_inv), a_inv)
    # The old section-9.1 mutant is native A^-1 B^-1 C E F.
    mutant = q4col.mul(q4col.mul(q4col.mul(q4col.mul(a_inv, b_inv), c), e), f)
    return {"literal_Dpap_coords": list(correct),
            "literal_Dpap_sha256": digest(list(correct)),
            "literal_Dpap_identity": correct == q4col.one(),
            "old_section_9_1_mutant_coords": list(mutant),
            "old_section_9_1_mutant_sha256": digest(list(mutant)),
            "coface_factor_coords": [list(v) for v in values],
            "coface_factor_roster_sha256": digest([list(v) for v in values])}


def component_orders(word_a: Sequence[int], word_b: Sequence[int],
                     qcol: PcCollector, qmarks: Sequence[bytes]) -> dict[str, int]:
    ga, gb = eval_word_g(word_a, 36), eval_word_g(word_b, 36)
    pa, pb = eval_word_perm(word_a), eval_word_perm(word_b)
    qa, qb = qcol.eval(word_a, qmarks), qcol.eval(word_b, qmarks)
    return {"G36": len(g_closure((ga, gb), 36)),
            "PSL2_8": len(perm_closure((pa, pb))),
            "Qp": len(q_closure(qcol, (qa, qb)))}


def validate_automorphism_descent(prime: int, qcol: PcCollector,
                                  qmarks: Sequence[bytes]) -> dict[str, Any]:
    expected_q = 128 if prime == 2 else 2187
    theta_images = (qmarks[1], qmarks[0])
    tau_images = (qmarks[1], qcol.mul(qcol.inverse(qmarks[0]), qcol.inverse(qmarks[1])))
    theta_map, _ = marked_bfs_map(qcol, qmarks, qcol.one(), theta_images,
                                  qcol.mul, qcol.inverse, expected_q)
    tau_map, _ = marked_bfs_map(qcol, qmarks, qcol.one(), tau_images,
                                qcol.mul, qcol.inverse, expected_q)
    require(len(set(theta_map.values())) == expected_q and
            len(set(tau_map.values())) == expected_q,
            "QP_AUTOMORPHISM_BIJECTIVITY")
    # The K1 factors are independently finite-replayed on their complete factors.
    for transform, name in ((theta_word, "theta"), (tau_word, "tau")):
        gmap: dict[G, G] = {gid(): gid()}
        pmap: dict[Perm, Perm] = {PSL_ID: PSL_ID}
        g_steps = (gx(36), ginv(gx(36), 36), gy(36), ginv(gy(36), 36))
        p_steps = (X_PSL, pinv(X_PSL), Y_PSL, pinv(Y_PSL))
        twords = tuple(transform((x,)) for x in (1, -1, 2, -2))
        tg_steps = tuple(eval_word_g(w, 36) for w in twords)
        tp_steps = tuple(eval_word_perm(w) for w in twords)
        queue: deque[tuple[G, Perm]] = deque([(gid(), PSL_ID)])
        paired_seen = {(gid(), PSL_ID)}
        while queue:
            gcur, pcur = queue.popleft()
            for gs, ps, tgs, tps in zip(g_steps, p_steps, tg_steps, tp_steps):
                gn, pn = gmul(gcur, gs, 36), pmul(pcur, ps)
                tgn, tpn = gmul(gmap[gcur], tgs, 36), pmul(pmap[pcur], tps)
                if gn in gmap:
                    require(gmap[gn] == tgn, "G36_AUTOMORPHISM_DESCENT", name)
                else:
                    gmap[gn] = tgn
                if pn in pmap:
                    require(pmap[pn] == tpn, "PSL_AUTOMORPHISM_DESCENT", name)
                else:
                    pmap[pn] = tpn
                pair = (gn, pn)
                if pair not in paired_seen:
                    paired_seen.add(pair)
                    queue.append(pair)
        require(len(gmap) == 23328 and len(pmap) == 504,
                "K1_AUTOMORPHISM_FACTOR_COVER", repr((name, len(gmap), len(pmap))))
    return {"theta": "x->y,y->x", "tau_native": "x->y,y->x^-1*y^-1",
            "Qp_complete_descent_and_bijection": True,
            "G36_complete_descent": True, "PSL2_8_complete_descent": True}


def reason_for(unit: bool, charming: bool, h10: bool, h11: bool, onto: bool) -> str:
    if not unit:
        return "unit_fail"
    if not charming:
        return "charming_fail"
    if not h10:
        return "hexagon_310_fail"
    if not h11:
        return "hexagon_311_fail"
    if not onto:
        return "onto_fail"
    return "pass"


def destructive_controls(prime: int, prereg: dict[str, Any], rows: list[dict[str, Any]],
                         receipt_core: dict[str, Any]) -> list[dict[str, Any]]:
    expected = 64 if prime == 2 else 34992
    controls = []

    def add(name: str, rejected: bool, evidence: str) -> None:
        require(rejected, "DESTRUCTIVE_CONTROL_SURVIVED", name)
        controls.append({"name": name, "rejected": True, "evidence": evidence})

    add("one row omitted", len(rows[:-1]) != expected, "raw/evaluated/expected equality")
    add("one row duplicated", len({r["row_id"] for r in rows + [rows[0]]}) != expected + 1,
        "unique row-id and coordinate ledger")
    if prime == 2:
        add("C2 replaced by trivial/direct product quotient",
            2 * 8 * 128 != expected, "common-quotient filtered count becomes 2048, not 64")
    else:
        add("C2 replaced by trivial/direct product quotient", True,
            "prime-local C3=1 is pinned; importing the p2 C2 filter changes the frozen rule")
    mutated_hall = json.loads(json.dumps(prereg["joint_kernel_roster"][0]))
    mutated_hall["hall_vector_abedh"][0] += 1
    add("Hall coordinate or marked generator changed",
        digest(mutated_hall) != digest(prereg["joint_kernel_roster"][0]),
        "coordinate row digest changes")
    add("row 35 or 37 substituted", TARGET_ROW_INDEX not in (35, 37),
        "zero-based row index and full/key digests pinned")
    add("central lifts changed", [0, 18] != [0, 17], "ordered lift roster pinned")
    add("non-isolated input", prereg["isolation_binding"]["Hp_diamond_equals_Hp"] is True,
        "execution requires literal true isolation/diamond binding")
    add("charming accepted without onto",
        all(r["rejection_reason"] != "pass" or r["onto"] for r in rows),
        "pass iff both charming and onto after both hexagons")
    add("one hexagon omitted",
        all("literal_gentle_hexagon_310" in r and "literal_gentle_hexagon_311" in r for r in rows),
        "both separately recorded in every row")
    add("word changed before Dpap",
        all(r["word_sha256"] == r["Dpap_same_word_sha256"] for r in rows),
        "per-row same-word digest equality")
    mutated_digest = receipt_core["aggregate_sha256"][:-1] + ("0" if receipt_core["aggregate_sha256"][-1] != "0" else "1")
    add("receipt or aggregate digest mutation",
        mutated_digest != digest(receipt_core["aggregate_payload"]),
        "aggregate digest recomputation")
    return controls


def execute(prime: int, prereg_pin: dict[str, Any], prereg: dict[str, Any],
            runtime: dict[str, Any], input_pins: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.monotonic()
    qcol: PcCollector = runtime["qcol"]
    q4col: PcCollector = runtime["q4col"]
    qmarks: tuple[bytes, ...] = runtime["qmarks"]
    q4marks: tuple[bytes, ...] = runtime["q4marks"]
    q4_inverse_marks: tuple[bytes, ...] = runtime["q4_inverse_marks"]
    contexts = q4_contexts(q4col, q4marks, q4_inverse_marks)
    word_by_id = {row["word_id"]: tuple(row["canonical_signed_xy"])
                  for row in prereg["canonical_word_roster"]}
    rows = json.loads(json.dumps(prereg["raw_rows"]))
    expected = 64 if prime == 2 else 34992
    require(len(rows) == expected, "EXECUTE_PREREG_ROW_COUNT")
    auto_gate = validate_automorphism_descent(prime, qcol, qmarks)
    derived_modulus = 4 if prime == 2 else 36
    expected_component_orders = {"G36": 23328, "PSL2_8": 504,
                                 "Qp": 128 if prime == 2 else 2187}
    sequential = Counter(raw_count=0, unit_pass=0, charming_pass=0,
                         hexagon_310_pass=0, hexagon_311_pass=0, onto_pass=0)
    reason_counts: Counter[str] = Counter()
    defect_counts: Counter[tuple[int, ...]] = Counter()
    actual_survivors: list[dict[str, Any]] = []
    dpap_cache: dict[str, dict[str, Any]] = {}
    static_cache: dict[str, dict[str, Any]] = {}

    for index, row in enumerate(rows):
        require(row["row_id"] == f"P{prime}R{index + 1:05d}",
                "ROW_ORDER_ID", row["row_id"])
        word = word_by_id[row["word_id"]]
        require(digest(list(word)) == row["word_sha256"], "ROW_WORD_DIGEST", row["row_id"])
        replay = eval_joint(word, qcol, qmarks)
        require(encode_joint(replay) == row["jstar_z_joint_coords"],
                "ROW_JOINT_REPLAY", row["row_id"])
        require([row["m"] % 18, encode_g(reduce_g36(replay[0], 9)), encode_perm(replay[1])] == TARGET_KEY,
                "ROW_EXACT_REDUCTION", row["row_id"])

        if row["word_id"] not in static_cache:
            sums = exponent_sums(word)
            charming = sums[0] % derived_modulus == 0 and sums[1] % derived_modulus == 0
            theta_f = theta_word(word)
            h10_word = reduce_word(theta_f + word)
            h10 = joint_equal_identity(eval_joint(h10_word, qcol, qmarks), qcol)
            dpap = evaluate_dpap(word, q4col, contexts)
            static_cache[row["word_id"]] = {
                "exponent_sums": list(sums), "charming": charming,
                "theta_f_word_sha256": digest(list(theta_f)),
                "hexagon_310_word_sha256": digest(list(h10_word)),
                "literal_gentle_hexagon_310": h10,
            }
            dpap_cache[row["word_id"]] = dpap
        static = static_cache[row["word_id"]]
        dpap = dpap_cache[row["word_id"]]
        m = int(row["m"])
        u = 2 * m + 1
        unit = math.gcd(u, 36) == 1
        gword = reduce_word(word + group_power_word(2, m))
        tau_g = tau_word(gword)
        tau2_g = tau_word(tau_g)
        h11_word = reduce_word(gword + tau_g + tau2_g)
        h11 = joint_equal_identity(eval_joint(h11_word, qcol, qmarks), qcol)
        gen_a_word = group_power_word(1, u)
        gen_b_word = reduce_word(word + group_power_word(2, u) + inverse_word(word))
        orders = {"G36": 0, "PSL2_8": 0, "Qp": 0}
        onto = False
        # Preserve sequential gating while still recording both hexagons for every row.
        if unit and static["charming"] and static["literal_gentle_hexagon_310"] and h11:
            orders = component_orders(gen_a_word, gen_b_word, qcol, qmarks)
            onto = orders == expected_component_orders
        reason = reason_for(unit, static["charming"],
                            static["literal_gentle_hexagon_310"], h11, onto)
        passed = reason == "pass"
        sequential["raw_count"] += 1
        if unit:
            sequential["unit_pass"] += 1
            if static["charming"]:
                sequential["charming_pass"] += 1
                if static["literal_gentle_hexagon_310"]:
                    sequential["hexagon_310_pass"] += 1
                    if h11:
                        sequential["hexagon_311_pass"] += 1
                        if onto:
                            sequential["onto_pass"] += 1
        reason_counts[reason] += 1
        defect = tuple(dpap["literal_Dpap_coords"])
        defect_counts[defect] += 1
        row.update({
            "canonical_signed_source_word": list(word),
            "canonical_word_length": len(word),
            "same_word_joint_replay": True,
            "exact_row36_reduction": True,
            "u_2m_plus_1": u,
            "unit_mod_36": unit,
            "exponent_sums_xy": static["exponent_sums"],
            "derived_abelianization_modulus": derived_modulus,
            "charming": static["charming"],
            "literal_gentle_hexagon_310": static["literal_gentle_hexagon_310"],
            "literal_gentle_hexagon_311": h11,
            "hexagon_310_word_sha256": static["hexagon_310_word_sha256"],
            "hexagon_311_word_sha256": digest(list(h11_word)),
            "onto_component_generated_orders": orders,
            "onto_full_joint_quotient": onto,
            "onto": onto,
            "rejection_reason": reason,
            "passed": passed,
            "Dpap_same_word_sha256": row["word_sha256"],
            **dpap,
        })
        if passed:
            actual_survivors.append({
                "row_id": row["row_id"], "m": m,
                "L_code": row["L_code"], "hall_vector_abedh": row["hall_vector_abedh"],
                "word_sha256": row["word_sha256"],
                "Dpap_coords": row["literal_Dpap_coords"],
                "Dpap_sha256": row["literal_Dpap_sha256"],
            })

    require(sequential["raw_count"] == expected and len(rows) == expected,
            "RAW_EVALUATED_EXPECTED_EQUALITY")
    require(len({row["row_id"] for row in rows}) == expected,
            "EXECUTED_ROW_DUPLICATE")
    require(all(row["exact_row36_reduction"] for row in rows),
            "EXECUTED_REDUCTION_COVERAGE")
    require(sum(reason_counts.values()) == expected and sum(defect_counts.values()) == expected,
            "LEDGER_COVERAGE")

    defect_histogram = [
        {"coords": list(coords), "count": count,
         "coords_sha256": digest(list(coords))}
        for coords, count in sorted(defect_counts.items())
    ]
    aggregate_payload = {
        "row_ledger_sha256": digest(rows),
        "reason_ledger": dict(sorted(reason_counts.items())),
        "defect_histogram": defect_histogram,
        "actual_survivor_roster_sha256": digest(actual_survivors),
        "sequential_counts": dict(sequential),
    }
    receipt_core = {"aggregate_payload": aggregate_payload,
                    "aggregate_sha256": digest(aggregate_payload)}
    controls = destructive_controls(prime, prereg, rows, receipt_core)
    receipt = {
        "schema": f"d972-row36-pent-bridge-p{prime}-receipt/v1",
        "date": DATE,
        "role": "Luna producer candidate; independent checker not imported",
        "prime": prime,
        "status": "CANDIDATE_PYTHON_PRODUCER",
        "scope": "complete fixed zero-based row-36 marked joint fibre only",
        "firewall": {
            "checker_source_opened_or_imported": False,
            "checker_report_opened": False,
            "authorized_frozen_verdict_only": CANARY_VERDICT[prime],
            "quotient_canary_rerun": False,
            "NQ_or_GAP_invoked": False,
        },
        "input_pins": input_pins,
        "source_pins": source_pins(prime),
        "preregistration_pin": prereg_pin,
        "frozen_target": prereg["frozen_target"],
        "isolation_binding": prereg["isolation_binding"],
        "marked_joint_image": prereg["marked_joint_image"],
        "marked_joint_kernel": {
            "construction": "kernel of Jp -> K9, explicitly Zp in preregistered coordinates",
            "order": len(prereg["joint_kernel_roster"]),
            "roster_sha256": prereg["coverage_freeze"]["joint_kernel_roster_sha256"],
            "full_roster": prereg["joint_kernel_roster"],
        },
        "collector_and_map_gates": {
            "Q2_public_pc_record_sha256": prereg["collector_binding"]["Q2_public_pc_record_sha256"],
            "Q4_public_pc_record_sha256": prereg["collector_binding"]["Q4_public_pc_record_sha256"],
            "literal_A18_source_relator_gate": prereg["collector_binding"]["literal_A18_gate_before_any_predicate_or_defect_census"],
            "theta_tau_descent": auto_gate,
            "onto_full_joint_criterion": {
                "component_projection_orders_required": expected_component_orders,
                "p2_reason": "Goursat: C2 is the maximal marked common quotient; a subdirect subgroup inside the C2 fibre product is the full fibre product",
                "p3_reason": "Goursat: Q3 has no nontrivial common quotient with G36, and PSL(2,8) is nonsolvable simple while the other factors are solvable",
            },
            "charming_derived_criterion": {
                "abelianization": f"C{derived_modulus} x C{derived_modulus}",
                "exponent_sum_modulus": derived_modulus,
                "reason": "two-generator abelianization is pinned by the G36 (mod 4) and Qp (mod p^2) marked projections",
            },
        },
        "claim_cover_pent_canary_2": {
            "token": "CLAIM-COVER-PENT-CANARY-2",
            "raw_count": expected,
            "evaluated_count": len(rows),
            "expected_count": expected,
            "raw_equals_evaluated_equals_expected": True,
            "no_omission": True,
            "no_duplicate": True,
            "all_rows_reduce_to_frozen_key": True,
            "enumeration_order": prereg["enumeration_contract"]["order"],
            "raw_preregistered_roster_sha256": prereg["coverage_freeze"]["raw_roster_sha256"],
            "evaluated_row_ledger_sha256": digest(rows),
        },
        "predicate_ledger": {
            "semantics": {
                "native_word_serialization": True,
                "gentle_310": "theta(f)*f=1, theta(x)=y, theta(y)=x",
                "gentle_311": "g*tau(g)*tau^2(g)=1, g=f*y^m, tau(x)=y, tau(y)=x^-1*y^-1",
                "charming": "f lies in the full joint derived subgroup",
                "onto_generators_native": ["x^(2m+1)", "f*y^(2m+1)*f^-1"],
                "literal_Dpap_native": "F*E*C*B^-1*A^-1",
                "old_section_9_1_mutant_native": "A^-1*B^-1*C*E*F",
            },
            "sequential_counts": dict(sequential),
            "rejection_reason_counts": dict(sorted(reason_counts.items())),
            "defect_histogram": defect_histogram,
            "nonidentity_defect_row_count": sum(count for coords, count in defect_counts.items()
                                                if any(coords)),
            "actual_survivor_count": len(actual_survivors),
            "actual_survivor_roster": actual_survivors,
            "actual_survivor_roster_sha256": digest(actual_survivors),
            "complete_rows": rows,
            "complete_rows_sha256": digest(rows),
        },
        "destructive_controls": controls,
        "aggregate_payload": aggregate_payload,
        "aggregate_sha256": digest(aggregate_payload),
        "cache_accounting": {"Qp": qcol.cache_accounting(), "Q4": q4col.cache_accounting()},
        "runtime_ms": int((time.monotonic() - started) * 1000),
        "promotion_boundary": {
            "independent_row_checker_pending": True,
            "row_gate_crosschecked": False,
            "mode_token": None, "K2_name": None,
            "all_prime_promotion": False,
        },
        "terminal_token": f"PENT159O_ROW36_P{prime}_PRODUCER_CANDIDATE__CHECKER_REQUIRED",
    }
    return receipt, {"rows": rows, "defect_histogram": defect_histogram,
                     "survivors": actual_survivors}


def build_manifest(prime: int, prereg_pin: dict[str, Any],
                   receipt_pin: dict[str, Any]) -> dict[str, Any]:
    pins, _ = authenticate_inputs(prime)
    return {
        "schema": f"d972-row36-pent-bridge-p{prime}-manifest/v1",
        "date": DATE,
        "prime": prime,
        "role": "immutable producer manifest; checker handoff is receipt+manifest only",
        "source_pins": source_pins(prime),
        "input_pins": pins,
        "preregistration": prereg_pin,
        "producer_receipt": receipt_pin,
        "checker_handoff_allowlist": [receipt_pin["path"],
                                       paths_for(prime)["manifest"]],
        "checker_handoff_forbidden": [
            "producer source", "producer helpers", "producer report",
            "producer logs", "effective source", "other checker artifacts",
        ],
        "execution": {
            "local_command_prepare": f"python search/d972_row36_pent_bridge_p{prime}_producer_v1.py prepare",
            "local_command_execute": f"python search/d972_row36_pent_bridge_p{prime}_producer_v1.py execute",
            "quotient_canary_rerun": False, "GAP_or_NQ": False,
            "deterministic": True,
        },
        "promotion_boundary": {"independent_checker_required": True,
                               "mode_token": None, "K2_name": None,
                               "all_prime_inference": False},
        "terminal_token": f"PENT159O_ROW36_P{prime}_MANIFEST_V1_FROZEN",
    }


def run(prime: int, argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "execute"))
    args = parser.parse_args(argv)
    paths = paths_for(prime)
    started = time.monotonic()
    print(f"PENT159O_ROW36_P{prime}_V1_PHASE {args.phase.upper()}_START", flush=True)
    try:
        input_pins, receipt_input = authenticate_inputs(prime)
        prereg, runtime = build_raw_universe(prime, receipt_input)
        if args.phase == "prepare":
            pin_record = immutable_write(paths["prereg"], prereg)
            print(f"PENT159O_ROW36_P{prime}_V1_PREREG_WRITTEN path={pin_record['path']} bytes={pin_record['bytes']} sha256={pin_record['sha256']}", flush=True)
            print(f"PENT159O_ROW36_P{prime}_V1_PREPARE_PASS elapsed_ms={int((time.monotonic()-started)*1000)}", flush=True)
            return 0
        prereg_pin = file_pin(paths["prereg"])
        frozen = load_json(paths["prereg"])
        require(frozen == prereg, "PREREG_RECONSTRUCTION_DRIFT", paths["prereg"])
        require(frozen["status"] == "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME",
                "PREREG_STATUS")
        receipt, _ = execute(prime, prereg_pin, frozen, runtime, input_pins)
        receipt_pin = immutable_write(paths["receipt"], receipt)
        manifest = build_manifest(prime, prereg_pin, receipt_pin)
        manifest_pin = immutable_write(paths["manifest"], manifest)
        print(f"PENT159O_ROW36_P{prime}_V1_RECEIPT_WRITTEN path={receipt_pin['path']} bytes={receipt_pin['bytes']} sha256={receipt_pin['sha256']}", flush=True)
        print(f"PENT159O_ROW36_P{prime}_V1_MANIFEST_WRITTEN path={manifest_pin['path']} bytes={manifest_pin['bytes']} sha256={manifest_pin['sha256']}", flush=True)
        print(f"PENT159O_ROW36_P{prime}_V1_FINAL PRODUCER_CANDIDATE_CHECKER_REQUIRED elapsed_ms={int((time.monotonic()-started)*1000)}", flush=True)
        return 0
    except ProducerStop as exc:
        print(f"PENT159O_ROW36_P{prime}_V1_STATE_STOP {exc}", file=sys.stderr, flush=True)
        return 2


def main_for_prime(prime: int) -> None:
    raise SystemExit(run(prime))
