#!/usr/bin/env python3
"""Sparse-DAG positive-semidecision at the relative mod-three Frattini stage.

The input is the frozen, independently checked 157da q=3 receipt.  This
program never constructs H=ker(PB4->E4).  It uses the equivariant Fox chain

    F3[E]^11 -> F3[E]^6 -> F3[E]

and emits a shared lossless provenance DAG for every positive Phi_3(H)
membership.  A bounded search miss is explicitly UNKNOWN.
"""

from __future__ import annotations

import argparse
import base64
import gc
import hashlib
import json
import math
import os
import sys
import time
from array import array
from collections import OrderedDict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

try:  # Linux production; the Windows selftest uses the documented fallback.
    import resource as _resource
except ImportError:  # pragma: no cover - exercised by the Windows selftest.
    _resource = None


SCHEMA = "d972-b345-relative-frattini3/v3"
Q3_SCHEMA = "d972-b345-q-chief/v1"
Q3_PRODUCER = Path("search/d972_b345_q3_chief_v1.g")
Q3_PRODUCER_SHA = "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
Q3_DRIVER = Path("search/d972_b345_q3_gha_driver_v1.g")
Q3_DRIVER_SHA = "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"
FORMULA_SHA = "b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef"
Q3_ARTIFACT_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
Q3_ARTIFACT_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
OUTPUT_PATH = Path("ci/out/d972_b345_relfrat3_v3.json")
V2_PRODUCER = Path("search/d972_b345_relfrat3_v2.py")
V2_PRODUCER_SHA = "fad364043926dbdc03e56accf089f454d625e0b315c98a7647bc891677313cc8"
V2_CHECKER = Path("search/check_d972_b345_relfrat3_v2.py")
V2_CHECKER_SHA = "3c8967bea6946b42cef08cd097eab4e9071aae203ee27ac38038c4d5adb83f07"
V2_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v2.g")
V2_DRIVER_SHA = "006e33e97c6f9ac1982887206c904dbcf423c95790ec2fe0c45d9a1b3a2e38aa"
V1_PRODUCER = Path("search/d972_b345_relfrat3_v1.py")
V1_PRODUCER_SHA = "4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e"
V1_CHECKER = Path("search/check_d972_b345_relfrat3_v1.py")
V1_CHECKER_SHA = "3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101"
V1_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v1.g")
V1_DRIVER_SHA = "fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b"
FIXED_WORD = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
              2, 2, 2, -1, -2, -2, 1, 1, 1, 1]

TERMINALS = {
    "B345_RELFRAT3_LITERAL_PAIR_PASS",
    "B345_RELFRAT3_SEARCH_INCOMPLETE",
    "B345_RELFRAT3_UNKNOWN_RESOURCE",
}

CAPS = {
    "small_representation_dimension": 64,
    "candidate_correction_dictionary": 4096,
    "coefficient_translates_per_relator": 32768,
    "total_sparse_group_ring_keys": 1_000_000,
    "sparse_pivot_rows": 1_000_000,
    "provenance_dag_nodes": 2_000_000,
    "provenance_dag_edges": 4_000_000,
    "single_word_or_section_length": 100_000,
    "affine_residual_dimension": 12,
    "explicit_affine_candidates": 531441,
    "ambient_PB5_ANUPQ": 1,
    "relative_ANUPQ_RS_full_Elements": 0,
    "producer_soft_timeout_seconds": 18_000,
    "producer_soft_rss_bytes": 4_831_838_208,
    "element_pool": 1_000_000,
    "element_product_cache": 262_144,
    "element_inverse_cache": 65_536,
    "pc_pair_product_cache": 65_536,
    "pc_inverse_cache": 16_384,
    "section_slp_nodes": 65_536,
    "compact_candidate_cache": 4_096,
    "compact_candidate_sparse_entries": 1_000_000,
    "progress_interval_seconds": 30,
}


class Reject(ValueError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def current_rss_bytes() -> int:
    """Current RSS on Linux; bounded portable fallback for the selftest."""
    status = Path("/proc/self/status")
    if status.exists():
        for line in status.read_text(encoding="ascii").splitlines():
            if line.startswith("VmRSS:"):
                fields = line.split()
                require(len(fields) >= 3 and fields[2] == "kB", "VmRSS format")
                return int(fields[1]) * 1024
    if _resource is not None:
        # ru_maxrss is a peak rather than current RSS, hence conservative.
        value = int(_resource.getrusage(_resource.RUSAGE_SELF).ru_maxrss)
        return value if sys.platform == "darwin" else value * 1024
    return 0


class ResourceMonitor:
    """Fail-closed wall/RSS monitor plus bounded live progress reporting."""

    def __init__(self, start: float, seconds: int,
                 rss_reader: Any = current_rss_bytes) -> None:
        require(seconds == CAPS["producer_soft_timeout_seconds"],
                "soft-timeout configuration")
        self.start = start
        self.seconds = seconds
        self.rss_limit = CAPS["producer_soft_rss_bytes"]
        self.rss_reader = rss_reader
        self.last_phase = "initializing"
        self.check_count = 0
        self.current_rss = 0
        self.peak_rss = 0
        self.last_progress = start
        self.accounting_supplier: Any = None
        self.hit_reason: str | None = None

    def bind_accounting(self, supplier: Any) -> None:
        self.accounting_supplier = supplier

    def _sample(self) -> None:
        value = int(self.rss_reader())
        require(value >= 0, "RSS sample")
        self.current_rss = value
        self.peak_rss = max(self.peak_rss, value)

    def _progress(self, force: bool = False) -> None:
        now = time.monotonic()
        if not force and now-self.last_progress < CAPS["progress_interval_seconds"]:
            return
        fields = {
            "translations": 0, "columns": 0, "pivots": 0,
            "live_sparse_entries": 0, "element_pool": 0,
            "dag_nodes": 0, "dag_edges": 0, "candidate_cache": 0,
            "pc_cache_hits": 0, "pc_cache_misses": 0,
            "pc_cache_evictions": 0,
        }
        if self.accounting_supplier is not None:
            fields.update(self.accounting_supplier())
        body = " ".join(f"{key}={fields[key]}" for key in fields)
        print("D972_B345_RELFRAT3_V3_PROGRESS "
              f"phase={self.last_phase} elapsed={now-self.start:.3f} "
              f"current_rss={self.current_rss} peak_rss={self.peak_rss} {body}",
              flush=True)
        self.last_progress = now

    def check(self, phase_name: str, force: bool = False) -> None:
        self.last_phase = phase_name
        self.check_count += 1
        now = time.monotonic()
        sampled = force or (self.check_count & 255) == 0 or \
            now-self.last_progress >= CAPS["progress_interval_seconds"]
        if sampled:
            self._sample()
            self._progress(force=force)
            if self.current_rss >= self.rss_limit:
                self.hit_reason = "producer_soft_rss"
                raise ResourceStop(self.hit_reason)
        if now-self.start >= self.seconds:
            self.hit_reason = "producer_soft_timeout"
            raise ResourceStop(self.hit_reason)

    def reserve(self, phase_name: str, additional_bytes: int) -> None:
        require(isinstance(additional_bytes, int) and additional_bytes >= 0,
                "RSS reservation")
        self.last_phase = phase_name
        self.check_count += 1
        self._sample()
        self._progress(force=True)
        if self.current_rss + additional_bytes >= self.rss_limit:
            self.hit_reason = "producer_soft_rss"
            raise ResourceStop(self.hit_reason)
        if time.monotonic()-self.start >= self.seconds:
            self.hit_reason = "producer_soft_timeout"
            raise ResourceStop(self.hit_reason)

    def receipt(self, hit: bool) -> dict[str, Any]:
        return {
            "seconds": self.seconds,
            "minutes": self.seconds // 60,
            "rss_bytes": self.rss_limit,
            "rss_gib": 4.5,
            "external_job_limit_minutes": 330,
            "safety_margin_minutes": 30,
            "clock": "time.monotonic",
            "rss_primary": "/proc/self/status VmRSS",
            "rss_portable_fallback": "getrusage peak or injected selftest reader",
            "hit": hit,
            "hit_reason": self.hit_reason,
            "last_checked_phase": self.last_phase,
            "check_count": self.check_count,
            "current_rss_bytes": self.current_rss,
            "peak_rss_bytes": self.peak_rss,
            "terminal_on_hit": "B345_RELFRAT3_UNKNOWN_RESOURCE",
            "consulted_in_selftest": False,
        }


# Keep the old annotation name out of the hot-path code while retaining the
# same method contract for frozen helper signatures.
SoftDeadline = ResourceMonitor


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def phase(label: str, start: float) -> float:
    now = time.monotonic()
    print(f"D972_B345_RELFRAT3_PHASE {label} elapsed_s={now-start:.6f}", flush=True)
    return now


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-relfrat3")
    try:
        encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"),
                                   ensure_ascii=True)
        expected_hash = hashlib.sha256()
        expected_bytes = 0
        with temporary.open("wb") as stream:
            for piece in encoder.iterencode(obj):
                raw_piece = piece.encode("ascii")
                stream.write(raw_piece)
                expected_hash.update(raw_piece)
                expected_bytes += len(raw_piece)
            stream.write(b"\n")
            expected_hash.update(b"\n")
            expected_bytes += 1
            stream.flush()
            os.fsync(stream.fileno())
        def streamed_digest(target: Path) -> tuple[int, str]:
            digest = hashlib.sha256()
            size = 0
            with target.open("rb") as source:
                while True:
                    chunk = source.read(1 << 20)
                    if not chunk:
                        break
                    digest.update(chunk)
                    size += len(chunk)
            return size, digest.hexdigest()
        expected = expected_hash.hexdigest()
        require(streamed_digest(temporary) == (expected_bytes, expected),
                "temporary output streamed readback")
        os.replace(temporary, path)
        require(streamed_digest(path) == (expected_bytes, expected),
                "final output streamed readback")
    finally:
        if temporary.exists():
            temporary.unlink()


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and letter != 0, "invalid signed word letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
        if len(out) > CAPS["single_word_or_section_length"]:
            raise ResourceStop("single_word_or_section_length")
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-letter for letter in reversed(word))


def word_substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(1 <= abs(letter) <= len(images), "word substitution index")
        out.extend(images[abs(letter)-1] if letter > 0 else inv_word(images[-letter-1]))
        out = reduce_word(out)
    return out


def pp_words(words: Sequence[Sequence[int]]) -> list[int]:
    require(bool(words), "empty paper-product word")
    return reduce_word(x for word in reversed(words) for x in word)


def commutator(a: Sequence[int], b: Sequence[int]) -> list[int]:
    return reduce_word(inv_word(a) + inv_word(b) + list(a) + list(b))


def exponent_sums(word: Sequence[int], width: int) -> list[int]:
    return [sum(1 if x > 0 else -1 for x in word if abs(x) == i)
            for i in range(1, width + 1)]


def derived_commutator_ledger(word: Sequence[int]) -> dict[str, Any]:
    """Losslessly bubble a zero-abelianization F2 word to the identity.

    If W=AabB and W'=AbaB, then W=[Aa^-1A^-1,Ab^-1A^-1] W'.
    Thus every swap is one explicit commutator and the product is literally W.
    """
    require(exponent_sums(word, 2) == [0, 0], "derived ledger exponent sums")
    current = reduce_word(word)
    factors: list[dict[str, Any]] = []
    while True:
        pos = next((i for i in range(len(current)-1)
                    if abs(current[i]) == 2 and abs(current[i+1]) == 1), None)
        if pos is None:
            break
        prefix = current[:pos]
        a, b = current[pos], current[pos+1]
        left = reduce_word(prefix + [-a] + inv_word(prefix))
        right = reduce_word(prefix + [-b] + inv_word(prefix))
        factors.append({"left": left, "right": right})
        current = reduce_word(current[:pos] + [b, a] + current[pos+2:])
    require(current == [], "derived bubble normal form is not identity")
    expanded: list[int] = []
    for row in factors:
        expanded = reduce_word(expanded + commutator(row["left"], row["right"]))
    require(expanded == reduce_word(word), "derived commutator product mismatch")
    return {"convention": "[a,b]=a^-1*b^-1*a*b",
            "factors": factors, "expanded_word": expanded,
            "factor_count": len(factors)}


###############################################################################
# Pure braid presentations and literal cofaces.
###############################################################################


def pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i+1, rank+1)]


def pair_index(rank: int, pair: Sequence[int]) -> int:
    try:
        return pairs(rank).index(list(pair)) + 1
    except ValueError as exc:
        raise Reject(f"bad PB{rank} pair {pair}") from exc


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    require(1 <= i < rank, "Artin letter")
    images = [[j] for j in range(1, rank+1)]
    if letter > 0:
        images[i-1], images[i] = [i, i+1, -i], [i]
    else:
        images[i-1], images[i] = [i+1], [-(i+1), i, i+1]
    return images


def artin_images(rank: int, braid: Sequence[int]) -> list[list[int]]:
    images = [[j] for j in range(1, rank+1)]
    for letter in braid:
        step = artin_step(rank, letter)
        images = [word_substitute(w, step) for w in images]
    return images


def aij_braid(i: int, j: int) -> list[int]:
    return list(range(j-1, i, -1)) + [i, i] + [-k for k in range(i+1, j)]


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    old_pairs = pairs(rank-1)
    old_map = [[pair_index(rank, p)] for p in old_pairs]
    rels = [word_substitute(w, old_map) for w in pure_relations(rank-1)]
    kernel = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        g = pair_index(rank, [i, j])
        action = artin_images(rank-1, aij_braid(i, j))
        for k in range(1, rank):
            h = pair_index(rank, [k, rank])
            rels.append(reduce_word([-g, h, g] +
                                    inv_word(word_substitute(action[k-1], kernel))))
    return rels


def coface_generator(rank: int, slot: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if slot == 0:
        return [pair_index(rank+1, [i+1, j+1])]
    if slot == rank+1:
        return [pair_index(rank+1, [i, j])]
    require(1 <= slot <= rank, "coface slot")
    if i == slot:
        return [pair_index(rank+1, [slot, j+1]),
                pair_index(rank+1, [slot+1, j+1])]
    if j == slot:
        return [pair_index(rank+1, [i, slot]),
                pair_index(rank+1, [i, slot+1])]
    return [pair_index(rank+1, [i + (i > slot), j + (j > slot)])]


def cofaces(rank: int) -> list[list[list[int]]]:
    return [[coface_generator(rank, slot, p) for p in pairs(rank)]
            for slot in range(rank+2)]


def relevant_formula() -> dict[str, Any]:
    c34 = cofaces(3)
    return {
        "convention": {
            "pair_order": "lexicographic_i_then_j",
            "word_product": "left_to_right",
            "paper_product": "displayed_factors_multiplied_right_to_left",
            "coface_slots": "0=left endpoint,1..r=strand doubling,r+1=right endpoint",
        },
        "presentations": {
            f"PB{r}": {"pairs": pairs(r), "relations": pure_relations(r)}
            for r in (3, 4, 5)
        },
        "cofaces_3_4": c34,
        "a18_order": {
            "names": ["phi_123", "phi_234", "phi_12_3_4",
                      "phi_1_23_4", "phi_1_2_34"],
            "slots": [4, 0, 1, 2, 3],
            "maps": [c34[i] for i in (4, 0, 1, 2, 3)],
        },
    }


###############################################################################
# Independent finite quotient arithmetic from the receipt.
###############################################################################


Perm = bytes
Pc = bytes
EKey = tuple[Perm, Pc]
VectorKey = tuple[int, EKey]
SparseVector = dict[VectorKey, int]


def perm_from_row(row: Sequence[int], degree: int) -> Perm:
    require(len(row) == degree and all(isinstance(x, int) for x in row),
            "permutation row")
    value = bytes(x-1 for x in row)
    require(set(value) == set(range(degree)), "permutation is not bijective")
    return value


def perm_one(degree: int) -> Perm:
    require(degree <= 256, "packed permutation degree")
    return bytes(range(degree))


def perm_mul(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degree")
    return bytes(b[a[i]] for i in range(len(a)))


def perm_inv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, image in enumerate(a):
        out[image] = i
    return bytes(out)


def perm_order(value: Perm) -> int:
    seen = [False] * len(value)
    answer = 1
    for i in range(len(value)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = value[j]
            length += 1
        answer = math.lcm(answer, length)
    return answer


def coords_word(coords: Sequence[int]) -> list[int]:
    return [i for i, exponent in enumerate(coords, 1) for _ in range(exponent)]


class BoundedLRU:
    """Exact bounded cache; eviction is semantics-neutral."""

    def __init__(self, capacity: int) -> None:
        require(isinstance(capacity, int) and capacity > 0, "LRU capacity")
        self.capacity = capacity
        self.data: OrderedDict[Any, Any] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.peak = 0

    def get(self, key: Any) -> Any | None:
        if key not in self.data:
            self.misses += 1
            return None
        self.hits += 1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self.data:
            self.data[key] = value
            self.data.move_to_end(key)
            return
        if len(self.data) >= self.capacity:
            self.data.popitem(last=False)
            self.evictions += 1
        self.data[key] = value
        self.peak = max(self.peak, len(self.data))

    def clear(self) -> None:
        self.data.clear()

    def accounting(self) -> dict[str, int]:
        return {"capacity": self.capacity, "size": len(self.data),
                "peak": self.peak, "hits": self.hits,
                "misses": self.misses, "evictions": self.evictions}


@dataclass
class PcCollector:
    receipt: dict[str, Any]

    def __post_init__(self) -> None:
        self.n = int(self.receipt["generator_count"])
        self.orders = list(self.receipt["relative_orders"])
        require(self.n == len(self.orders) and self.n <= 175 and
                all(x == 3 for x in self.orders), "pc rank/orders")
        self.powers = [self.coord(x) for x in self.receipt["power_relations"]]
        self.inverses = [self.coord(x) for x in self.receipt["inverses"]]
        self.conjugates = {(x["i"], x["j"]): self.coord(x["coords"])
                           for x in self.receipt["conjugate_relations"]}
        self.inverse_conjugates = {
            (x["i"], x["j"]): self.coord(x["coords"])
            for x in self.receipt["inverse_conjugate_relations"]}
        require(len(self.conjugates) == self.n*(self.n-1)//2 and
                set(self.conjugates) == set(self.inverse_conjugates),
                "pc conjugate tables")
        self.pair_cache = BoundedLRU(CAPS["pc_pair_product_cache"])
        self.inverse_cache = BoundedLRU(CAPS["pc_inverse_cache"])

    def coord(self, row: Sequence[int]) -> Pc:
        require(len(row) == self.n and all(isinstance(x, int) for x in row) and
                all(0 <= x < 3 for x in row), "pc coordinate")
        return bytes(row)

    def one(self) -> Pc:
        return bytes(self.n)

    def unit(self, index: int) -> Pc:
        require(1 <= index <= self.n, "pc unit")
        row = [0] * self.n
        row[index-1] = 1
        return bytes(row)

    def collect_uncached(self, word: Sequence[int]) -> Pc:
        tokens: list[int] = []
        for x in word:
            require(1 <= abs(x) <= self.n, "pc letter")
            tokens.extend([x] if x > 0 else coords_word(self.inverses[-x-1]))
        steps = 0
        cap = max(10000, 1000*(1+len(tokens))*(1+self.n))
        while True:
            changed = False
            for pos in range(len(tokens)-1):
                a, b = tokens[pos], tokens[pos+1]
                if a > b:
                    tokens[pos:pos+2] = [b] + coords_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if not changed:
                pos = 0
                while pos < len(tokens):
                    i, run = tokens[pos], pos
                    while run < len(tokens) and tokens[run] == i:
                        run += 1
                    if run-pos >= 3:
                        tokens[pos:pos+3] = coords_word(self.powers[i-1])
                        changed = True
                        break
                    pos = run
            if not changed:
                break
            steps += 1
            require(steps <= cap, "pc collection cap")
        row = [0] * self.n
        last = 0
        for x in tokens:
            require(x >= last, "pc order")
            row[x-1] += 1
            require(row[x-1] < 3, "pc power")
            last = x
        return bytes(row)

    def collect(self, word: Sequence[int]) -> Pc:
        # Arbitrary full-token words are deliberately never retained.
        return self.collect_uncached(word)

    def mul(self, a: Pc, b: Pc) -> Pc:
        require(len(a) == len(b) == self.n, "pc product width")
        key = a + b
        cached = self.pair_cache.get(key)
        if cached is not None:
            return cached
        answer = self.collect_uncached(coords_word(a) + coords_word(b))
        self.pair_cache.put(key, answer)
        return answer

    def inverse(self, a: Pc) -> Pc:
        require(len(a) == self.n, "pc inverse width")
        cached = self.inverse_cache.get(a)
        if cached is not None:
            return cached
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(a[i-1]):
                word.extend(coords_word(self.inverses[i-1]))
        answer = self.collect_uncached(word)
        self.inverse_cache.put(a, answer)
        return answer

    def eval(self, word: Sequence[int], images: Sequence[Pc]) -> Pc:
        out = self.one()
        for x in word:
            value = images[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out

    def cache_accounting(self) -> dict[str, Any]:
        pair = self.pair_cache.accounting()
        inverse = self.inverse_cache.accounting()
        return {
            "policy": "bounded exact pair-product and inverse LRU; no full-word cache",
            "pair_product": pair,
            "inverse": inverse,
            "hits": pair["hits"] + inverse["hits"],
            "misses": pair["misses"] + inverse["misses"],
            "evictions": pair["evictions"] + inverse["evictions"],
            "unbounded_full_token_word_cache": False,
        }

    def clear_caches(self) -> None:
        self.pair_cache.clear()
        self.inverse_cache.clear()


@dataclass
class MatchedQuotient:
    rank: int
    degree: int
    pc: PcCollector
    generators: list[EKey]

    def __post_init__(self) -> None:
        require(len(self.generators) == len(pairs(self.rank)), "matched marked width")
        self.identity: EKey = (perm_one(self.degree), self.pc.one())
        self.inverse_generators = [self.inverse(g) for g in self.generators]

    def mul(self, a: EKey, b: EKey) -> EKey:
        return perm_mul(a[0], b[0]), self.pc.mul(a[1], b[1])

    def inverse(self, a: EKey) -> EKey:
        return perm_inv(a[0]), self.pc.inverse(a[1])

    def eval(self, word: Sequence[int], images: Sequence[EKey] | None = None) -> EKey:
        marked = self.generators if images is None else images
        out = self.identity
        for x in word:
            value = marked[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out


def eval_perm_word(word: Sequence[int], images: Sequence[Perm]) -> Perm:
    out = perm_one(len(images[0]))
    for x in word:
        value = images[abs(x)-1]
        out = perm_mul(out, value if x > 0 else perm_inv(value))
    return out


def enumerate_generated(identity: Any, generators: Sequence[Any], mul: Any,
                        inverse: Any, cap: int) -> set[Any]:
    steps = list(generators) + [inverse(x) for x in generators]
    seen = {identity}
    queue = [identity]
    while queue:
        a = queue.pop()
        for g in steps:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                require(len(seen) <= cap, "small subgroup cap")
                queue.append(b)
    return seen


def paper_conjugate(value: Any, y: Any, identity: Any, mul: Any, inverse: Any) -> Any:
    # PP([value^-1,y,value]) = value*y*value^-1.
    return mul(mul(value, y), inverse(value))


###############################################################################
# Literal B3/B4 words.
###############################################################################


def f2_substitute(word: Sequence[int], x: Sequence[int], y: Sequence[int]) -> list[int]:
    return word_substitute(word, [x, y])


def hexagon_words(f: Sequence[int]) -> list[list[int]]:
    x, y = [1], [2]
    z = inv_word(pp_words([x, y]))
    u = inv_word(pp_words([y, x]))
    fxy = f2_substitute(f, x, y)
    fxz = f2_substitute(f, x, z)
    fyz = f2_substitute(f, y, z)
    fux = f2_substitute(f, u, x)
    fuy = f2_substitute(f, u, y)
    return [pp_words([fxy, inv_word(fxz), fyz]),
            pp_words([inv_word(fux), inv_word(fxy), fuy])]


def embed_f2_pb3(word: Sequence[int]) -> list[int]:
    # PB3 pair order is A12,A13,A23.
    return word_substitute(word, [[1], [3]])


def pentagon_word(f: Sequence[int]) -> list[int]:
    g = [[i] for i in range(1, 7)]
    contexts = [
        [g[0], g[3]],
        [g[3], g[5]],
        [pp_words([g[1], g[3]]), g[5]],
        [pp_words([g[0], g[1]]), pp_words([g[4], g[5]])],
        [g[0], pp_words([g[3], g[4]])],
    ]
    parts = [f2_substitute(f, x, y) for x, y in contexts]
    return pp_words([inv_word(pp_words([parts[4], parts[2]])),
                     parts[1], parts[3], parts[0]])


def source_words_m0(f: Sequence[int]) -> list[list[int]]:
    ff = word_substitute(f, [[1], [4]])
    g = word_substitute(f, [[1], [2]])
    gs = word_substitute(f, [[4], [5]])
    f1234 = word_substitute(f, [[4, 2], [6]])
    h = word_substitute(f, [[2, 1], [3]])
    middle = word_substitute(f, [[2, 1], [6, 5]])
    return [
        [1],
        reduce_word(inv_word(g) + [2] + g),
        reduce_word(inv_word(ff) + inv_word(h) + [3] + h + ff),
        reduce_word(inv_word(ff) + [4] + ff),
        reduce_word(inv_word(ff) + inv_word(middle) + inv_word(gs) + [5] +
                    gs + middle + ff),
        reduce_word(inv_word(f1234) + [6] + f1234),
    ]


def two_sided_residuals(source: Sequence[Sequence[int]],
                        inverse_words: Sequence[Sequence[int]]) \
        -> tuple[list[list[int]], list[list[int]]]:
    forward_residuals = [reduce_word(word_substitute(inverse_words[i], source) +
                                     [-(i+1)]) for i in range(6)]
    inverse_residuals = [reduce_word(word_substitute(source[i], inverse_words) +
                                     [-(i+1)]) for i in range(6)]
    return forward_residuals, inverse_residuals


def normalized_inverse_fibre(data: dict[str, Any], quotient: MatchedQuotient) \
        -> tuple[dict[str, Any], tuple[EKey, ...], list[list[int]]]:
    powers = data["canonical_roof_powers"]
    rows = powers["rows"]
    require([row["exponent"] for row in rows] == [1, 2, 4, 5, 7, 8] and
            powers["canonicalized_each_step"] is True and
            powers["literal_power_words_retained"] is False,
            "normalized q3 power receipt")
    row7s = [row for row in rows if row["exponent"] == 7]
    row2s = [row for row in rows if row["exponent"] == 2]
    require(len(row7s) == len(row2s) == 1, "normalized exponent-two/seven rows")
    row7 = row7s[0]
    corrections = data["correction_fibre"]
    records = corrections["records"]
    require(len(records) == 27 and corrections["certificate"]["order"] == 27 and
            corrections["certificate"]["enumerated_count"] == 27 and
            corrections["certificate"]["all_words_coarse_identity"] is True,
            "normalized inverse correction fibre")
    selected_q3 = data["selected_solution"]
    selected_index = selected_q3["correction_index"]
    require(selected_q3["exponent"] == 2 and 1 <= selected_index <= 27 and
            reduce_word(row2s[0]["word"] + records[selected_index-1]["word"]) ==
            FIXED_WORD,
            "fixed exponent-two tuple/canonical fibre binding")
    base_source = source_words_m0(FIXED_WORD)
    base_key = tuple(quotient.eval(word) for word in base_source)
    tested: list[int] = []
    passing: list[int] = []
    candidates: dict[int, tuple[list[int], list[list[int]]]] = {}
    for index, record in enumerate(records, 1):
        candidate = reduce_word(row7["word"] + record["word"])
        inverse_words = source_words_m0(candidate)
        st, ts = two_sided_residuals(base_source, inverse_words)
        tested.append(index)
        if all(quotient.eval(word) == quotient.identity for word in st + ts):
            passing.append(index)
            candidates[index] = (candidate, inverse_words)
    require(tested == list(range(1, 28)) and passing,
            "normalized exponent-seven fibre has no E4 two-sided inverse")
    selected = passing[0]
    selected_candidate, selected_inverse = candidates[selected]
    max_length = max(map(len, selected_inverse))
    require(max_length <= CAPS["single_word_or_section_length"],
            "normalized inverse word cap")
    public = {
        "source": "pinned q3 canonical exponent-seven row times the complete authenticated 27-element correction fibre",
        "normalized_exponent": 7,
        "normalized_roof_order": 9,
        "normalized_power_row": row7,
        "correction_fibre_size": 27,
        "tested_indices": tested,
        "passing_indices": passing,
        "selection_policy": ("unique" if len(passing) == 1 else
                             "deterministic first; full passing set retained"),
        "selected_correction_index": selected,
        "selected_correction_word": records[selected-1]["word"],
        "selected_inverse_candidate_word": selected_candidate,
        "selected_inverse_words": selected_inverse,
        "max_inverse_word_length": max_length,
        "raw_endomorphism_powering_used": False,
        "componentwise_Q4_Pi4_inverse_words_combined": False,
    }
    return public, base_key, selected_inverse


def finite_normalized_inverse(
        f: Sequence[int], quotient: MatchedQuotient,
        pool: "ElementPool",
        inverse_cache: dict[tuple[int, ...], list[list[int]]],
        cache_stats: dict[str, int], normalized: dict[str, Any]) -> dict[str, Any]:
    source = source_words_m0(f)
    source_key = tuple(pool.intern(quotient.eval(word)) for word in source)
    cached = inverse_cache.get(source_key)
    if cached is None:
        cache_stats["misses"] += 1
        raise ResourceStop("missing_bounded_inverse_representative")
    cache_stats["hits"] += 1
    inverse_words = [list(word) for word in cached]
    forward_residuals, inverse_residuals = two_sided_residuals(
        source, inverse_words)
    require(all(quotient.eval(w) == quotient.identity
                for w in forward_residuals + inverse_residuals),
            "normalized cached inverse does not compose with current S on E4")
    max_length = max(map(len, inverse_words))
    cache_stats["max_inverse_word_length"] = max(
        cache_stats["max_inverse_word_length"], max_length)
    return {
        "normalized_exponent": 7,
        "normalized_roof_order": 9,
        "source_words": source,
        "inverse_words": inverse_words,
        "ST_residuals": forward_residuals,
        "TS_residuals": inverse_residuals,
        "construction": "finite normalized exponent-seven inverse from the pinned complete 27-fibre",
        "max_inverse_word_length": max_length,
        "cache_hit": True,
        "cache_key_exact_six_E4_images": True,
        "cache_hit_two_sided_replay_in_E4": True,
        "candidate_acceptance_or_certificate_reused": False,
        "componentwise_Q4_Pi4_inverse_words_combined": False,
        "normalized_fibre_selected_correction_index":
            normalized["selected_correction_index"],
        "normalized_fibre_passing_indices": normalized["passing_indices"],
    }


###############################################################################
# Sparse left-Fox calculus and translated-relator Gaussian search.
###############################################################################


def add_term(vector: SparseVector, key: VectorKey, coefficient: int) -> None:
    coefficient %= 3
    if not coefficient:
        return
    value = (vector.get(key, 0) + coefficient) % 3
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def add_scaled(target: dict[Any, int], source: dict[Any, int], scalar: int) -> None:
    scalar %= 3
    if not scalar:
        return
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scalar*coefficient) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def scaled(source: dict[Any, int], scalar: int) -> dict[Any, int]:
    scalar %= 3
    return {key: (scalar*value) % 3 for key, value in source.items()
            if (scalar*value) % 3}


def fox_gradient(word: Sequence[int], quotient: MatchedQuotient) \
        -> tuple[SparseVector, EKey, dict[EKey, list[int]]]:
    prefix = quotient.identity
    prefix_word: list[int] = []
    gradient: SparseVector = {}
    sections: dict[EKey, list[int]] = {prefix: []}
    for letter in word:
        index = abs(letter)
        require(1 <= index <= len(quotient.generators), "Fox generator index")
        if letter > 0:
            add_term(gradient, (index, prefix), 1)
            prefix = quotient.mul(prefix, quotient.generators[index-1])
            prefix_word = reduce_word(prefix_word + [index])
        else:
            prefix = quotient.mul(prefix, quotient.inverse_generators[index-1])
            prefix_word = reduce_word(prefix_word + [-index])
            add_term(gradient, (index, prefix), 2)
        sections.setdefault(prefix, list(prefix_word))
    return gradient, prefix, sections


def d1(vector: SparseVector, quotient: MatchedQuotient) -> dict[EKey, int]:
    out: dict[EKey, int] = {}
    for (index, element), coefficient in vector.items():
        add_scaled(out, {quotient.mul(element, quotient.generators[index-1]): 1,
                         element: 2}, coefficient)
    return out


def translate_vector(vector: SparseVector, translation: EKey,
                     quotient: MatchedQuotient) -> SparseVector:
    out: SparseVector = {}
    for (component, element), coefficient in vector.items():
        add_term(out, (component, quotient.mul(translation, element)), coefficient)
    return out


class _V2ReferenceProvenanceDAG:
    """Shared immutable F3 straight-line program for boundary witnesses."""

    def __init__(self, deadline: SoftDeadline | None = None) -> None:
        # Node ids are one-based and list order is topological.  The empty
        # linear combination is the unique zero node.
        self.nodes: list[dict[str, Any]] = [
            {"kind": "linear_combination", "terms": []},
        ]
        self.edge_count = 0
        self.max_nodes = 1
        self.max_edges = 0
        self.deadline = deadline

    def checkpoint(self) -> tuple[int, int]:
        return len(self.nodes), self.edge_count

    def rollback(self, checkpoint: tuple[int, int]) -> None:
        node_count, edge_count = checkpoint
        require(1 <= node_count <= len(self.nodes) and
                0 <= edge_count <= self.edge_count, "DAG rollback checkpoint")
        del self.nodes[node_count:]
        self.edge_count = edge_count

    def _append(self, node: dict[str, Any], edges: int) -> int:
        if len(self.nodes) + 1 > CAPS["provenance_dag_nodes"]:
            raise ResourceStop("provenance_dag_nodes")
        if self.edge_count + edges > CAPS["provenance_dag_edges"]:
            raise ResourceStop("provenance_dag_edges")
        self.nodes.append(node)
        self.edge_count += edges
        self.max_nodes = max(self.max_nodes, len(self.nodes))
        self.max_edges = max(self.max_edges, self.edge_count)
        if self.deadline is not None and (len(self.nodes) & 1023) == 0:
            self.deadline.check("provenance_dag_growth")
        return len(self.nodes)

    def leaf(self, relator_index: int, translation: EKey) -> int:
        require(relator_index >= 1, "DAG leaf relator index")
        return self._append({
            "kind": "translated_relator_leaf",
            "relator_index": relator_index,
            "translation": translation,
            "translation_action": "left",
        }, 0)

    def linear(self, terms: Sequence[tuple[int, int]]) -> int:
        merged: dict[int, int] = {}
        for node_id, coefficient in terms:
            require(1 <= node_id <= len(self.nodes), "DAG backward reference")
            if node_id == 1:
                continue
            coefficient %= 3
            if coefficient:
                value = (merged.get(node_id, 0) + coefficient) % 3
                if value:
                    merged[node_id] = value
                else:
                    merged.pop(node_id, None)
        ordered = sorted(merged.items())
        if not ordered:
            return 1
        if len(ordered) == 1 and ordered[0][1] == 1:
            return ordered[0][0]
        return self._append({
            "kind": "linear_combination",
            "terms": ordered,
        }, len(ordered))

    def accounting(self) -> dict[str, int]:
        return {
            "live_nodes": len(self.nodes),
            "live_edges": self.edge_count,
            "peak_nodes": self.max_nodes,
            "peak_edges": self.max_edges,
        }

    def reachable(self, roots: Sequence[int]) -> set[int]:
        pending = list(roots)
        reached: set[int] = set()
        while pending:
            node_id = pending.pop()
            require(1 <= node_id <= len(self.nodes), "DAG root/reference range")
            if node_id in reached:
                continue
            reached.add(node_id)
            node = self.nodes[node_id-1]
            if node["kind"] == "linear_combination":
                pending.extend(parent for parent, _ in node["terms"])
        return reached


class _V2ReferenceSparseBoundaryBasis:
    def __init__(self, quotient: MatchedQuotient,
                 relator_columns: list[SparseVector], dag: _V2ReferenceProvenanceDAG,
                 deadline: SoftDeadline | None = None) -> None:
        self.quotient = quotient
        self.relator_columns = relator_columns
        self.dag = dag
        self.deadline = deadline
        self.rows: dict[VectorKey, tuple[SparseVector, int]] = {}
        self.translation_sections: dict[EKey, list[int]] = {quotient.identity: []}
        self.columns_seen = 0
        self.dependent_columns = 0
        self.max_vector_support = 0
        self.max_transient_vector_support = 0
        self.live_vector_entries = 0
        self.elimination_operations = 0

    @staticmethod
    def pivot(vector: SparseVector) -> VectorKey:
        return min(vector)

    def _resource_gate(self) -> None:
        if self.live_vector_entries > CAPS["total_sparse_group_ring_keys"]:
            raise ResourceStop("total_sparse_group_ring_keys")
        if len(self.rows) > CAPS["sparse_pivot_rows"]:
            raise ResourceStop("sparse_pivot_rows")

    def accounting(self) -> dict[str, Any]:
        return {
            "live_sparse_vector_entries": self.live_vector_entries,
            "pivot_count": len(self.rows),
            "max_pivot_vector_support": self.max_vector_support,
            "max_transient_vector_support": self.max_transient_vector_support,
            "elimination_operations": self.elimination_operations,
            "dag": self.dag.accounting(),
        }

    def _deadline_gate(self, phase_name: str) -> None:
        self.elimination_operations += 1
        if self.deadline is not None and \
                (self.elimination_operations & 1023) == 0:
            self.deadline.check(phase_name)

    def add_column(self, relator_index: int, translation: EKey,
                   translation_word: Sequence[int]) -> None:
        checkpoint = self.dag.checkpoint()
        vector = translate_vector(self.relator_columns[relator_index-1],
                                  translation, self.quotient)
        node_id = self.dag.leaf(relator_index, translation)
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop("single_sparse_elimination_row")
                pivot = self.pivot(vector)
                if pivot not in self.rows:
                    coefficient = vector[pivot]
                    inverse = 1 if coefficient == 1 else 2
                    vector = scaled(vector, inverse)
                    node_id = self.dag.linear([(node_id, inverse)])
                    if self.live_vector_entries + len(vector) > \
                            CAPS["total_sparse_group_ring_keys"]:
                        raise ResourceStop("total_sparse_group_ring_keys")
                    if len(self.rows) + 1 > CAPS["sparse_pivot_rows"]:
                        raise ResourceStop("sparse_pivot_rows")
                    self.rows[pivot] = (vector, node_id)
                    self.live_vector_entries += len(vector)
                    self.max_vector_support = max(self.max_vector_support, len(vector))
                    self.translation_sections.setdefault(translation,
                                                         list(translation_word))
                    self.columns_seen += 1
                    self._resource_gate()
                    return
                coefficient = vector[pivot]
                basis_vector, basis_node = self.rows[pivot]
                add_scaled(vector, basis_vector, -coefficient)
                node_id = self.dag.linear([(node_id, 1),
                                           (basis_node, -coefficient)])
                self._deadline_gate("pivot_column_elimination")
            self.dag.rollback(checkpoint)
            self.columns_seen += 1
            self.dependent_columns += 1
        except Exception:
            self.dag.rollback(checkpoint)
            raise

    def solve(self, target: SparseVector) -> int | None:
        checkpoint = self.dag.checkpoint()
        vector = dict(target)
        answer_node = 1
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                pivot = self.pivot(vector)
                row = self.rows.get(pivot)
                if row is None:
                    self.dag.rollback(checkpoint)
                    return None
                coefficient = vector[pivot]
                add_scaled(vector, row[0], -coefficient)
                answer_node = self.dag.linear([(answer_node, 1),
                                               (row[1], coefficient)])
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop("target_elimination_support")
                self._deadline_gate("target_sparse_elimination")
            return answer_node
        except Exception:
            self.dag.rollback(checkpoint)
            raise


def _v2_reference_translation_bfs(quotient: MatchedQuotient, cap: int) \
        -> Iterator[tuple[EKey, list[int]]]:
    steps = list(enumerate(quotient.generators, 1)) + [
        (-i, quotient.inverse_generators[i-1]) for i in range(1, 7)]
    seen = {quotient.identity}
    queue: deque[tuple[EKey, list[int]]] = deque([(quotient.identity, [])])
    while queue and len(seen) <= cap:
        element, word = queue.popleft()
        yield element, word
        if len(seen) == cap:
            continue
        for letter, step in steps:
            value = quotient.mul(element, step)
            if value not in seen:
                seen.add(value)
                queue.append((value, reduce_word(word + [letter])))
                if len(seen) == cap:
                    break


PackedSparseVector = dict[int, int]


def pack_vector_key(component: int, element_id: int) -> int:
    require(1 <= component <= 6 and 0 <= element_id < CAPS["element_pool"],
            "packed vector key")
    return element_id * 8 + component - 1


def unpack_vector_key(key: int) -> tuple[int, int]:
    require(isinstance(key, int) and key >= 0 and key % 8 < 6,
            "packed vector key decode")
    return key % 8 + 1, key // 8


class ElementPool:
    """Exact compact interning for all persistent E4 elements."""

    def __init__(self, quotient: MatchedQuotient) -> None:
        self.quotient = quotient
        self.width = quotient.degree + quotient.pc.n
        self.values: list[bytes] = []
        self.ids: dict[bytes, int] = {}
        self.hits = 0
        self.misses = 0
        self.peak = 0
        self.product_cache = BoundedLRU(CAPS["element_product_cache"])
        self.inverse_cache = BoundedLRU(CAPS["element_inverse_cache"])
        self.identity_id = self.intern(quotient.identity)
        self.generator_ids = [self.intern(x) for x in quotient.generators]
        self.inverse_generator_ids = [self.inverse_id(x)
                                      for x in self.generator_ids]

    def pack(self, value: EKey) -> bytes:
        require(len(value[0]) == self.quotient.degree and
                len(value[1]) == self.quotient.pc.n, "element packing width")
        blob = value[0] + value[1]
        require(len(blob) == self.width, "element packed width")
        return blob

    def unpack(self, blob: bytes) -> EKey:
        require(isinstance(blob, bytes) and len(blob) == self.width,
                "canonical packed element")
        return blob[:self.quotient.degree], blob[self.quotient.degree:]

    def intern(self, value: EKey) -> int:
        blob = self.pack(value)
        existing = self.ids.get(blob)
        if existing is not None:
            self.hits += 1
            return existing
        self.misses += 1
        if len(self.values) >= CAPS["element_pool"]:
            raise ResourceStop("element_pool")
        identifier = len(self.values)
        # The same immutable bytes object is retained by the list and dict;
        # no second canonical payload is allocated.
        self.values.append(blob)
        self.ids[blob] = identifier
        self.peak = max(self.peak, len(self.values))
        return identifier

    def blob(self, identifier: int) -> bytes:
        require(0 <= identifier < len(self.values), "element id range")
        return self.values[identifier]

    def value(self, identifier: int) -> EKey:
        return self.unpack(self.blob(identifier))

    def mul_id(self, left: int, right: int) -> int:
        require(0 <= left < len(self.values) and 0 <= right < len(self.values),
                "element product ids")
        key = left * CAPS["element_pool"] + right
        cached = self.product_cache.get(key)
        if cached is not None:
            return int(cached)
        answer = self.intern(self.quotient.mul(self.value(left), self.value(right)))
        self.product_cache.put(key, answer)
        return answer

    def inverse_id(self, identifier: int) -> int:
        require(0 <= identifier < len(self.values), "element inverse id")
        cached = self.inverse_cache.get(identifier)
        if cached is not None:
            return int(cached)
        answer = self.intern(self.quotient.inverse(self.value(identifier)))
        self.inverse_cache.put(identifier, answer)
        return answer

    def eval_id(self, word: Sequence[int], images: Sequence[int] | None = None) -> int:
        marked = self.generator_ids if images is None else images
        out = self.identity_id
        for letter in word:
            require(1 <= abs(letter) <= len(marked), "packed evaluation letter")
            value = marked[abs(letter)-1]
            if letter < 0:
                value = self.inverse_id(value)
            out = self.mul_id(out, value)
        return out

    def pivot_order(self, packed_key: int) -> tuple[int, bytes]:
        component, identifier = unpack_vector_key(packed_key)
        return component, self.blob(identifier)

    def accounting(self) -> dict[str, Any]:
        return {
            "capacity": CAPS["element_pool"],
            "size": len(self.values),
            "peak": self.peak,
            "packed_width_bytes": self.width,
            "packed_payload_bytes": len(self.values) * self.width,
            "hits": self.hits,
            "misses": self.misses,
            "exact_equality": "canonical permutation bytes concatenated with PC-coordinate bytes",
            "canonical_order": "lexicographic canonical packed bytes, identical to EKey=(permutation,PC) tuple order",
            "digest_used_as_equality": False,
            "product_cache": self.product_cache.accounting(),
            "inverse_cache": self.inverse_cache.accounting(),
        }

    def clear_caches(self) -> None:
        self.product_cache.clear()
        self.inverse_cache.clear()

    def clear_large(self) -> None:
        self.clear_caches()
        self.ids.clear()
        self.values.clear()


class LazySectionSLP:
    """First-seen freely reduced BFS sections as parent plus signed letter."""

    def __init__(self, identity_id: int) -> None:
        self.parent = array("I", [0])
        self.letter = array("b", [0])
        self.last = array("b", [0])
        self.depth = array("I", [0])
        self.by_element: dict[int, int] = {identity_id: 0}
        self.peak = 1

    def append(self, parent: int, letter: int) -> int:
        require(0 <= parent < len(self.parent) and 1 <= abs(letter) <= 6,
                "section SLP append")
        if self.last[parent] == -letter:
            return int(self.parent[parent])
        if len(self.parent) >= CAPS["section_slp_nodes"]:
            raise ResourceStop("section_slp_nodes")
        self.parent.append(parent)
        self.letter.append(letter)
        self.last.append(letter)
        self.depth.append(self.depth[parent] + 1)
        self.peak = max(self.peak, len(self.parent))
        return len(self.parent)-1

    def bind(self, element_id: int, node_id: int) -> None:
        require(element_id not in self.by_element and
                0 <= node_id < len(self.parent), "section binding")
        self.by_element[element_id] = node_id

    def node_for(self, element_id: int) -> int:
        require(element_id in self.by_element, "missing lazy section")
        return self.by_element[element_id]

    def materialize(self, node_id: int) -> list[int]:
        require(0 <= node_id < len(self.parent), "section node range")
        out: list[int] = []
        cursor = node_id
        while cursor:
            out.append(int(self.letter[cursor]))
            cursor = int(self.parent[cursor])
        out.reverse()
        require(len(out) == self.depth[node_id], "section SLP depth")
        return out

    def accounting(self) -> dict[str, Any]:
        return {"capacity": CAPS["section_slp_nodes"],
                "live_nodes": len(self.parent), "peak_nodes": self.peak,
                "bound_elements": len(self.by_element),
                "representation": "parent element-section node plus signed generator letter"}

    def clear(self) -> None:
        self.by_element.clear()
        del self.parent[:]
        del self.letter[:]
        del self.last[:]
        del self.depth[:]


def add_packed_term(vector: PackedSparseVector, key: int, coefficient: int) -> None:
    coefficient %= 3
    if not coefficient:
        return
    value = (vector.get(key, 0) + coefficient) % 3
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def fox_gradient_packed(word: Sequence[int], pool: ElementPool) \
        -> tuple[PackedSparseVector, int]:
    prefix = pool.identity_id
    gradient: PackedSparseVector = {}
    for letter in word:
        component = abs(letter)
        require(1 <= component <= len(pool.generator_ids), "packed Fox index")
        if letter > 0:
            add_packed_term(gradient, pack_vector_key(component, prefix), 1)
            prefix = pool.mul_id(prefix, pool.generator_ids[component-1])
        else:
            prefix = pool.mul_id(prefix, pool.inverse_generator_ids[component-1])
            add_packed_term(gradient, pack_vector_key(component, prefix), 2)
    return gradient, prefix


def d1_packed(vector: PackedSparseVector, pool: ElementPool) -> dict[int, int]:
    out: dict[int, int] = {}
    for key, coefficient in vector.items():
        component, element = unpack_vector_key(key)
        add_packed_term(out, pool.mul_id(element, pool.generator_ids[component-1]),
                        coefficient)
        add_packed_term(out, element, -coefficient)
    return out


def translate_vector_packed(vector: PackedSparseVector, translation: int,
                            pool: ElementPool) -> PackedSparseVector:
    out: PackedSparseVector = {}
    for key, coefficient in vector.items():
        component, element = unpack_vector_key(key)
        add_packed_term(out, pack_vector_key(
            component, pool.mul_id(translation, element)), coefficient)
    return out


def intern_raw_vector(vector: SparseVector, pool: ElementPool) -> PackedSparseVector:
    out: PackedSparseVector = {}
    for (component, element), coefficient in vector.items():
        add_packed_term(out, pack_vector_key(component, pool.intern(element)),
                        coefficient)
    return out


class ProvenanceDAG:
    """Packed parallel-array F3 straight-line program."""

    ZERO = 0
    LEAF = 1
    LINEAR = 2

    def __init__(self, deadline: SoftDeadline | None = None) -> None:
        self.kind = bytearray([self.LINEAR])
        self.leaf_relator = array("H", [0])
        self.leaf_translation = array("I", [0])
        self.edge_start = array("I", [0])
        self.edge_length = array("I", [0])
        self.edge_parent = array("I")
        self.edge_coefficient = bytearray()
        self.max_nodes = 1
        self.max_edges = 0
        self.deadline = deadline

    @property
    def node_count(self) -> int:
        return len(self.kind)

    @property
    def edge_count(self) -> int:
        return len(self.edge_parent)

    def checkpoint(self) -> tuple[int, int]:
        return self.node_count, self.edge_count

    def rollback(self, checkpoint: tuple[int, int]) -> None:
        nodes, edges = checkpoint
        require(1 <= nodes <= self.node_count and 0 <= edges <= self.edge_count,
                "packed DAG rollback checkpoint")
        del self.kind[nodes:]
        del self.leaf_relator[nodes:]
        del self.leaf_translation[nodes:]
        del self.edge_start[nodes:]
        del self.edge_length[nodes:]
        del self.edge_parent[edges:]
        del self.edge_coefficient[edges:]

    def _append_node(self, kind: int, relator: int, translation: int,
                     terms: Sequence[tuple[int, int]]) -> int:
        if self.node_count + 1 > CAPS["provenance_dag_nodes"]:
            raise ResourceStop("provenance_dag_nodes")
        if self.edge_count + len(terms) > CAPS["provenance_dag_edges"]:
            raise ResourceStop("provenance_dag_edges")
        start = self.edge_count
        self.kind.append(kind)
        self.leaf_relator.append(relator)
        self.leaf_translation.append(translation)
        self.edge_start.append(start)
        self.edge_length.append(len(terms))
        for parent, coefficient in terms:
            self.edge_parent.append(parent)
            self.edge_coefficient.append(coefficient)
        self.max_nodes = max(self.max_nodes, self.node_count)
        self.max_edges = max(self.max_edges, self.edge_count)
        if self.deadline is not None and (self.node_count & 1023) == 0:
            self.deadline.check("packed_provenance_dag_growth")
        return self.node_count

    def leaf(self, relator_index: int, translation_id: int) -> int:
        require(relator_index >= 1 and translation_id >= 0, "packed DAG leaf")
        return self._append_node(self.LEAF, relator_index, translation_id, [])

    def terms(self, node_id: int) -> list[tuple[int, int]]:
        require(1 <= node_id <= self.node_count, "packed DAG node")
        index = node_id-1
        start = int(self.edge_start[index])
        stop = start + int(self.edge_length[index])
        return [(int(self.edge_parent[i]), int(self.edge_coefficient[i]))
                for i in range(start, stop)]

    def linear(self, terms: Sequence[tuple[int, int]]) -> int:
        merged: dict[int, int] = {}
        for node_id, coefficient in terms:
            require(1 <= node_id <= self.node_count, "packed DAG backward reference")
            if node_id == 1:
                continue
            coefficient %= 3
            if coefficient:
                value = (merged.get(node_id, 0) + coefficient) % 3
                if value:
                    merged[node_id] = value
                else:
                    merged.pop(node_id, None)
        ordered = sorted(merged.items())
        if not ordered:
            return 1
        if len(ordered) == 1 and ordered[0][1] == 1:
            return ordered[0][0]
        return self._append_node(self.LINEAR, 0, 0, ordered)

    def accounting(self) -> dict[str, Any]:
        return {
            "live_nodes": self.node_count, "live_edges": self.edge_count,
            "peak_nodes": self.max_nodes, "peak_edges": self.max_edges,
            "packed_arrays": True,
            "node_payload_bytes": (len(self.kind) + self.leaf_relator.itemsize *
                len(self.leaf_relator) + self.leaf_translation.itemsize *
                len(self.leaf_translation) + self.edge_start.itemsize *
                len(self.edge_start) + self.edge_length.itemsize *
                len(self.edge_length)),
            "edge_payload_bytes": (self.edge_parent.itemsize * len(self.edge_parent) +
                                   len(self.edge_coefficient)),
        }

    def reachable(self, roots: Sequence[int]) -> set[int]:
        pending = list(roots)
        reached: set[int] = set()
        while pending:
            node_id = pending.pop()
            require(1 <= node_id <= self.node_count, "packed DAG reference range")
            if node_id in reached:
                continue
            reached.add(node_id)
            if self.kind[node_id-1] == self.LINEAR:
                pending.extend(parent for parent, _ in self.terms(node_id))
        return reached

    def clear(self) -> None:
        del self.kind[:]
        del self.leaf_relator[:]
        del self.leaf_translation[:]
        del self.edge_start[:]
        del self.edge_length[:]
        del self.edge_parent[:]
        del self.edge_coefficient[:]


class SparseBoundaryBasis:
    def __init__(self, pool: ElementPool,
                 relator_columns: list[PackedSparseVector], dag: ProvenanceDAG,
                 sections: LazySectionSLP,
                 deadline: SoftDeadline | None = None) -> None:
        self.pool = pool
        self.relator_columns = relator_columns
        self.dag = dag
        self.sections = sections
        self.deadline = deadline
        self.rows: dict[int, tuple[PackedSparseVector, int]] = {}
        self.columns_seen = 0
        self.dependent_columns = 0
        self.max_vector_support = 0
        self.max_transient_vector_support = 0
        self.live_vector_entries = 0
        self.elimination_operations = 0

    def pivot(self, vector: PackedSparseVector) -> int:
        # Never use insertion-order element IDs: this is exactly v2's
        # (component,EKey) canonical order.
        return min(vector, key=self.pool.pivot_order)

    def _resource_gate(self) -> None:
        if self.live_vector_entries > CAPS["total_sparse_group_ring_keys"]:
            raise ResourceStop("total_sparse_group_ring_keys")
        if len(self.rows) > CAPS["sparse_pivot_rows"]:
            raise ResourceStop("sparse_pivot_rows")

    def accounting(self) -> dict[str, Any]:
        return {
            "live_sparse_vector_entries": self.live_vector_entries,
            "pivot_count": len(self.rows),
            "max_pivot_vector_support": self.max_vector_support,
            "max_transient_vector_support": self.max_transient_vector_support,
            "elimination_operations": self.elimination_operations,
            "dag": self.dag.accounting(),
            "element_pool": self.pool.accounting(),
            "lazy_sections": self.sections.accounting(),
        }

    def _cadence(self, phase_name: str) -> None:
        self.elimination_operations += 1
        if self.deadline is not None and (self.elimination_operations & 1023) == 0:
            self.deadline.check(phase_name)

    def add_column(self, relator_index: int, translation_id: int,
                   section_node: int) -> None:
        require(self.sections.node_for(translation_id) == section_node,
                "translation/section binding")
        checkpoint = self.dag.checkpoint()
        vector = translate_vector_packed(
            self.relator_columns[relator_index-1], translation_id, self.pool)
        node_id = self.dag.leaf(relator_index, translation_id)
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop("single_sparse_elimination_row")
                pivot = self.pivot(vector)
                if pivot not in self.rows:
                    coefficient = vector[pivot]
                    factor = 1 if coefficient == 1 else 2
                    vector = scaled(vector, factor)
                    node_id = self.dag.linear([(node_id, factor)])
                    if self.live_vector_entries + len(vector) > \
                            CAPS["total_sparse_group_ring_keys"]:
                        raise ResourceStop("total_sparse_group_ring_keys")
                    if len(self.rows) + 1 > CAPS["sparse_pivot_rows"]:
                        raise ResourceStop("sparse_pivot_rows")
                    self.rows[pivot] = (vector, node_id)
                    self.live_vector_entries += len(vector)
                    self.max_vector_support = max(self.max_vector_support, len(vector))
                    self.columns_seen += 1
                    self._resource_gate()
                    return
                coefficient = vector[pivot]
                basis_vector, basis_node = self.rows[pivot]
                add_scaled(vector, basis_vector, -coefficient)
                node_id = self.dag.linear([(node_id, 1),
                                           (basis_node, -coefficient)])
                self._cadence("packed_pivot_column_elimination")
            self.dag.rollback(checkpoint)
            self.columns_seen += 1
            self.dependent_columns += 1
        except Exception:
            self.dag.rollback(checkpoint)
            raise

    def solve(self, target: PackedSparseVector) -> int | None:
        checkpoint = self.dag.checkpoint()
        vector = dict(target)
        answer_node = 1
        try:
            while vector:
                self.max_transient_vector_support = max(
                    self.max_transient_vector_support, len(vector))
                pivot = self.pivot(vector)
                row = self.rows.get(pivot)
                if row is None:
                    self.dag.rollback(checkpoint)
                    return None
                coefficient = vector[pivot]
                add_scaled(vector, row[0], -coefficient)
                answer_node = self.dag.linear([(answer_node, 1),
                                               (row[1], coefficient)])
                if len(vector) > CAPS["total_sparse_group_ring_keys"]:
                    raise ResourceStop("target_elimination_support")
                self._cadence("packed_target_sparse_elimination")
            return answer_node
        except Exception:
            self.dag.rollback(checkpoint)
            raise

    def clear(self) -> None:
        self.rows.clear()
        self.relator_columns.clear()


def translation_bfs(pool: ElementPool, sections: LazySectionSLP, cap: int) \
        -> Iterator[tuple[int, int]]:
    steps = list(zip(range(1, 7), pool.generator_ids)) + \
        list(zip(range(-1, -7, -1), pool.inverse_generator_ids))
    seen = {pool.identity_id}
    queue: deque[int] = deque([pool.identity_id])
    while queue and len(seen) <= cap:
        element_id = queue.popleft()
        section_node = sections.node_for(element_id)
        yield element_id, section_node
        if len(seen) == cap:
            continue
        for letter, step_id in steps:
            value_id = pool.mul_id(element_id, step_id)
            if value_id not in seen:
                seen.add(value_id)
                child = sections.append(section_node, letter)
                sections.bind(value_id, child)
                queue.append(value_id)
                if len(seen) == cap:
                    break


def packed_fox_model(rank: int, pool: ElementPool) -> dict[str, Any]:
    require(rank == pool.quotient.rank, "packed Fox rank")
    relations = pure_relations(rank)
    columns: list[PackedSparseVector] = []
    for relator in relations:
        gradient, value = fox_gradient_packed(relator, pool)
        require(value == pool.identity_id, f"PB{rank} packed relator quotient image")
        require(d1_packed(gradient, pool) == {}, f"PB{rank} packed D1D2")
        columns.append(gradient)
    return {"rank": rank, "relations": relations, "columns": columns,
            "D1D2_zero": True}


def fox_model(rank: int, quotient: MatchedQuotient) -> dict[str, Any]:
    relators = pure_relations(rank)
    columns: list[SparseVector] = []
    sections: list[dict[EKey, list[int]]] = []
    for relator in relators:
        gradient, value, support_sections = fox_gradient(relator, quotient)
        require(value == quotient.identity, f"PB{rank} relator quotient image")
        require(d1(gradient, quotient) == {}, f"PB{rank} D1D2")
        columns.append(gradient)
        sections.append(support_sections)
    return {"rank": rank, "relations": relators, "columns": columns,
            "sections": sections, "D1D2_zero": True}


###############################################################################
# Frozen q=3 reconstruction and base-gate replay.
###############################################################################


def marked_pc(receipt: dict[str, Any]) -> list[Pc]:
    pc = PcCollector(receipt)
    return [pc.coord(row["coords"]) for row in receipt["marked_generators"]]


def reconstruct_quotients(data: dict[str, Any]) \
        -> tuple[MatchedQuotient, MatchedQuotient, dict[str, Any]]:
    pc3 = PcCollector(data["groups"]["PB3"])
    pc4 = PcCollector(data["groups"]["PB4"])
    p3 = [pc3.coord(row["coords"]) for row in
          data["groups"]["PB3"]["marked_generators"]]
    p4 = [pc4.coord(row["coords"]) for row in
          data["groups"]["PB4"]["marked_generators"]]
    q0_model = data["coarse_models"]["Q0"]
    q4_model = data["coarse_models"]["Q4"]
    q0 = [perm_from_row(row, q0_model["degree"])
          for row in q0_model["marked_permutations"]]
    q4 = [perm_from_row(row, q4_model["degree"])
          for row in q4_model["marked_permutations"]]
    require(len(q0) == 2 and len(q4) == 6, "coarse marked widths")
    # In the m=0 PB3 source, A13 is z=(A23*A12)^-1, exactly the hexagon z.
    q0z = perm_inv(perm_mul(q0[1], q0[0]))
    e3 = MatchedQuotient(3, q0_model["degree"], pc3,
                         [(q0[0], p3[0]), (q0z, p3[1]), (q0[1], p3[2])])
    e4 = MatchedQuotient(4, q4_model["degree"], pc4,
                         list(zip(q4, p4)))
    for rank, quotient in ((3, e3), (4, e4)):
        require(all(quotient.eval(r) == quotient.identity for r in pure_relations(rank)),
                f"PB{rank} matched presentation")
    return e3, e4, {"pc3": pc3, "pc4": pc4, "q0": q0, "q4": q4}


def replay_base_q3(data: dict[str, Any], e3: MatchedQuotient,
                   e4: MatchedQuotient) -> dict[str, Any]:
    require(data["schema"] == Q3_SCHEMA and
            data["terminal_token"] ==
            "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
            "frozen q3 terminal")
    selected = data["selected_solution"]
    require(selected == data["direct_word_scan"]["solutions"][0] and
            data["direct_word_scan"]["solution_count"] == 1,
            "frozen q3 selected solution")
    require(selected["typed_source_word"] == FIXED_WORD and
            selected["correction_word"] == [] and
            selected["correction_index"] == 1 and selected["exponent"] == 2,
            "fixed outside word/empty correction")
    require(exponent_sums(FIXED_WORD, 2) == [0, 0], "fixed word abelianization")
    hex_words = hexagon_words(FIXED_WORD)
    hex_pb3 = [embed_f2_pb3(w) for w in hex_words]
    hex_values = [e3.eval(w) for w in hex_pb3]
    require(hex_values == [e3.identity, e3.identity], "base q3 hexagon replay")
    pent = pentagon_word(FIXED_WORD)
    require(e4.eval(pent) == e4.identity, "base q3 pentagon replay")
    derived = derived_commutator_ledger(FIXED_WORD)

    models = data["coarse_models"]
    p_rows = [perm_from_row(row, models["P"]["degree"])
              for row in models["P"]["marked_permutations"]]
    g_rows = [perm_from_row(row, models["G9"]["degree"])
              for row in models["G9"]["marked_permutations"]]
    p_one, g_one = perm_one(9), perm_one(27)
    f_p = eval_perm_word(FIXED_WORD, p_rows)
    f_g = eval_perm_word(FIXED_WORD, g_rows)
    p_onto = len(enumerate_generated(
        p_one, [p_rows[0], paper_conjugate(f_p, p_rows[1], p_one,
                                            perm_mul, perm_inv)],
        perm_mul, perm_inv, 504)) == 504
    g_onto = len(enumerate_generated(
        g_one, [g_rows[0], paper_conjugate(f_g, g_rows[1], g_one,
                                            perm_mul, perm_inv)],
        perm_mul, perm_inv, 2916)) == 2916
    b2 = [e3.generators[0][1], e3.generators[2][1]]
    f_b = e3.pc.eval(FIXED_WORD, b2)
    b_onto = len(enumerate_generated(
        e3.pc.one(), [b2[0], paper_conjugate(f_b, b2[1], e3.pc.one(),
                                              e3.pc.mul, e3.pc.inverse)],
        e3.pc.mul, e3.pc.inverse, 27)) == 27
    require(p_onto and g_onto and b_onto, "base q3 onto replay")
    q0_value = eval_perm_word(FIXED_WORD,
                              [e3.generators[0][0], e3.generators[2][0]])
    require(perm_order(q0_value) == 9 and selected["roof_reduction_exact"] is True,
            "outside roof/order replay")
    settlement = selected["settlement"]
    source = source_words_m0(FIXED_WORD)
    require(settlement["source_words"] == source and
            settlement["Q4_bijective"] is True and
            settlement["Pi4_q3_bijective"] is True,
            "base settled map binding")
    require([e4.eval(w) for w in source] != [], "source map evaluation")
    return {
        "fixed_word": FIXED_WORD,
        "roof_exponent": 2,
        "roof_order": 9,
        "arithmetic_outside_by_index_three": True,
        "marking_m": 0,
        "lambda": 1,
        "hexagon_residual_words_F2": hex_words,
        "pentagon_residual_word_PB4": pent,
        "derived_membership": derived,
        "onto_small_factors": {"P_order_504": p_onto,
                                 "G9_order_2916": g_onto,
                                 "B2_order_27": b_onto},
        "settled_source_words": source,
        "replayed_not_copied": True,
    }


def correction_dictionary(data: dict[str, Any], e3: MatchedQuotient) -> dict[str, Any]:
    base_words = [reduce_word(row["word"] * 3)
                  for row in data["correction_fibre"]["records"]
                  if row["word"]]
    base_words = list(dict.fromkeys(tuple(w) for w in base_words))
    seeds: list[list[int]] = []
    for raw in base_words:
        k = list(raw)
        require(e3.eval(embed_f2_pb3(k)) == e3.identity,
                "authenticated cube is not in H3")
        for generator in ([1], [2]):
            for word in (commutator(k, generator), commutator(generator, k)):
                if word and exponent_sums(word, 2) == [0, 0] and word not in seeds:
                    require(e3.eval(embed_f2_pb3(word)) == e3.identity,
                            "commutator correction is not H3")
                    seeds.append(word)
    # Complete preregistered shortlex-by-construction universe.  Only
    # exponent-zero H3 words are admitted, so every candidate has an explicit
    # free-derived representative; this is a bounded positive lane, not a
    # completeness claim for all H3 corrections.
    words: list[list[int]] = [[]]
    seen = {()}
    queue: deque[list[int]] = deque([[]])
    steps = seeds + [inv_word(w) for w in seeds]
    while queue and len(words) < CAPS["candidate_correction_dictionary"]:
        prefix = queue.popleft()
        for step in steps:
            word = reduce_word(prefix + step)
            key = tuple(word)
            if key not in seen:
                require(exponent_sums(word, 2) == [0, 0] and
                        e3.eval(embed_f2_pb3(word)) == e3.identity,
                        "dictionary H3/derived invariant")
                seen.add(key)
                words.append(word)
                queue.append(word)
                if len(words) == CAPS["candidate_correction_dictionary"]:
                    break
    return {
        "order": "identity, then breadth-first products of authenticated H3 commutator seeds and inverses",
        "source": "commutators with cubes of the frozen 27-word coarse-trivial exponent-three fibre",
        "words": words,
        "count": len(words),
        "cap": CAPS["candidate_correction_dictionary"],
        "all_words_in_H3": True,
        "all_words_in_coarse_J_H": True,
        "all_words_free_exponent_zero": True,
        "not_complete_for_all_H3": True,
        "membership_in_finer_J_Phi_required": False,
        "J_Phi_cosets_are_the_lift_freedom": True,
        "seed_words": seeds,
    }


def quotient_product(quotient: MatchedQuotient,
                     values: Sequence[EKey]) -> EKey:
    out = quotient.identity
    for value in values:
        out = quotient.mul(out, value)
    return out


def quotient_paper_product(quotient: MatchedQuotient,
                           values: Sequence[EKey]) -> EKey:
    return quotient_product(quotient, list(reversed(values)))


def cheap_candidate_bad(candidate: Sequence[int], correction: Sequence[int],
                        e4: MatchedQuotient) -> list[str]:
    """Evaluate the fixed literal equations without expanding substituted words."""
    coarse_bad: list[str] = []
    hex1_bad: list[str] = []
    hex2_bad: list[str] = []
    for slot, mapping in enumerate(cofaces(3)):
        x = e4.eval(mapping[0])
        y = e4.eval(mapping[2])
        if e4.eval(correction, [x, y]) != e4.identity:
            coarse_bad.append(f"correction_coarse_J_H_coface_{slot}")
        z = e4.inverse(quotient_paper_product(e4, [x, y]))
        u = e4.inverse(quotient_paper_product(e4, [y, x]))
        fxy = e4.eval(candidate, [x, y])
        fxz = e4.eval(candidate, [x, z])
        fyz = e4.eval(candidate, [y, z])
        fux = e4.eval(candidate, [u, x])
        fuy = e4.eval(candidate, [u, y])
        h1 = quotient_paper_product(
            e4, [fxy, e4.inverse(fxz), fyz])
        h2 = quotient_paper_product(
            e4, [e4.inverse(fux), e4.inverse(fxy), fuy])
        if h1 != e4.identity:
            hex1_bad.append(f"hexagon_1_coface_{slot}")
        if h2 != e4.identity:
            hex2_bad.append(f"hexagon_2_coface_{slot}")

    bad = coarse_bad + hex1_bad + hex2_bad

    g = e4.generators
    contexts = [
        [g[0], g[3]],
        [g[3], g[5]],
        [quotient_paper_product(e4, [g[1], g[3]]), g[5]],
        [quotient_paper_product(e4, [g[0], g[1]]),
         quotient_paper_product(e4, [g[4], g[5]])],
        [g[0], quotient_paper_product(e4, [g[3], g[4]])],
    ]
    parts = [e4.eval(candidate, context) for context in contexts]
    pent = quotient_paper_product(
        e4, [e4.inverse(quotient_paper_product(e4, [parts[4], parts[2]])),
             parts[1], parts[3], parts[0]])
    if pent != e4.identity:
        bad.append("ordered_A18_pentagon")

    ff = e4.eval(candidate, [g[0], g[3]])
    gv = e4.eval(candidate, [g[0], g[1]])
    gs = e4.eval(candidate, [g[3], g[4]])
    f1234 = e4.eval(candidate, [quotient_product(e4, [g[3], g[1]]), g[5]])
    h = e4.eval(candidate, [quotient_product(e4, [g[1], g[0]]), g[2]])
    middle = e4.eval(candidate, [quotient_product(e4, [g[1], g[0]]),
                                 quotient_product(e4, [g[5], g[4]])])
    source = [
        g[0],
        quotient_product(e4, [e4.inverse(gv), g[1], gv]),
        quotient_product(e4, [e4.inverse(ff), e4.inverse(h), g[2], h, ff]),
        quotient_product(e4, [e4.inverse(ff), g[3], ff]),
        quotient_product(e4, [e4.inverse(ff), e4.inverse(middle),
                              e4.inverse(gs), g[4], gs, middle, ff]),
        quotient_product(e4, [e4.inverse(f1234), g[5], f1234]),
    ]
    for index, relator in enumerate(pure_relations(4), 1):
        if e4.eval(relator, source) != e4.identity:
            bad.append(f"S_relation_{index}")
    return bad


def prepare_candidate(candidate: Sequence[int], correction: Sequence[int],
                      e4: MatchedQuotient) -> dict[str, Any]:
    f = reduce_word(candidate)
    require(exponent_sums(f, 2) == [0, 0],
            "candidate free-derived precondition")
    bad = cheap_candidate_bad(f, correction, e4)
    return {"selected_word": f, "correction_word": list(correction),
            "inverse": None, "targets": [], "quotient_bad": bad,
            "_cheap_direct_evaluation": True, "_materialized": False}


def materialize_candidate(base: dict[str, Any], e4: MatchedQuotient) \
        -> dict[str, Any]:
    candidate = base["selected_word"]
    correction = base["correction_word"]
    c34 = cofaces(3)
    coarse_jh_words = [word_substitute(embed_f2_pb3(correction), mapping)
                       for mapping in c34]
    coarse_jh_bad = [f"correction_coarse_J_H_coface_{slot}"
                     for slot, word in enumerate(coarse_jh_words)
                     if e4.eval(word) != e4.identity]
    f = reduce_word(candidate)
    derived = derived_commutator_ledger(f)
    charming_error = reduce_word(f + inv_word(derived["expanded_word"]))
    charming_words = [word_substitute(embed_f2_pb3(charming_error), mapping)
                      for mapping in c34]
    hex_f2 = hexagon_words(f)
    hex_cofaces: list[tuple[str, list[int]]] = []
    for hindex, residual in enumerate(hex_f2, 1):
        source = embed_f2_pb3(residual)
        for slot, mapping in enumerate(c34):
            hex_cofaces.append((f"hexagon_{hindex}_coface_{slot}",
                                word_substitute(source, mapping)))
    pent = pentagon_word(f)
    source = source_words_m0(f)
    source_relations = [(f"S_relation_{index}", word_substitute(relator, source))
                        for index, relator in enumerate(pure_relations(4), 1)]
    cheap_targets: list[tuple[str, str, list[int]]] = []
    cheap_targets.extend((f"charming_error_coface_{slot}", "charming", word)
                         for slot, word in enumerate(charming_words))
    cheap_targets.extend((name, "hexagon", word) for name, word in hex_cofaces)
    cheap_targets.append(("ordered_A18_pentagon", "pentagon", pent))
    cheap_targets.extend((name, "endomorphism_relation", word)
                         for name, word in source_relations)
    quotient_bad = coarse_jh_bad + [name for name, _, word in cheap_targets
                                    if e4.eval(word) != e4.identity]
    materialized = {
        "selected_word": f,
        "correction_word": list(correction),
        "correction_coarse_J_H_coface_words": coarse_jh_words,
        "correction_coarse_J_H_all_five": not coarse_jh_bad,
        "correction_in_finer_J_Phi_required": False,
        "correction_J_Phi_coset_is_lift_freedom": True,
        "derived_witness": derived,
        "charming_error_word": charming_error,
        "hexagon_words_F2": hex_f2,
        "pentagon_word_PB4": pent,
        "marking_residuals": [],
        "representative_residuals": [],
        "marking_reason": "m=0,lambda=1 has no additional literal generator equality",
        "inverse": None,
        "targets": cheap_targets,
        "quotient_bad": quotient_bad,
        "_source_words": source,
        "_source_relations": source_relations,
        "J_H_definition": "kernel of the authenticated coarse source E3 map, gated again by all five coface images in H4",
        "J_Phi_definition": "intersection of all five PB3-to-PB4 coface preimages of Phi4",
        "J_Phi_not_identified_with_Phi3_H3": True,
    }
    require(materialized["quotient_bad"] == base["quotient_bad"],
            "direct cheap/full quotient gate drift")
    base.update(materialized)
    base["_cheap_direct_evaluation"] = True
    base["_materialized"] = True
    return base


def complete_candidate(base: dict[str, Any], e4: MatchedQuotient,
                       pool: ElementPool,
                       inverse_cache: dict[tuple[int, ...], list[list[int]]],
                       inverse_cache_stats: dict[str, int],
                       normalized_inverse: dict[str, Any]) \
        -> dict[str, Any]:
    if not base["_materialized"]:
        base = materialize_candidate(base, e4)
    if base["quotient_bad"]:
        return base
    source = base["_source_words"]
    source_relations = base["_source_relations"]
    inverse = finite_normalized_inverse(
        base["selected_word"], e4, pool, inverse_cache, inverse_cache_stats,
        normalized_inverse)
    twords = inverse["inverse_words"]
    relation_residuals: list[tuple[str, list[int]]] = []
    for index, relator in enumerate(pure_relations(4), 1):
        relation_residuals.append((f"S_relation_{index}",
                                   source_relations[index-1][1]))
        relation_residuals.append((f"T_relation_{index}",
                                   word_substitute(relator, twords)))
    onto_residuals = [(f"ST_generator_{i+1}", word)
                      for i, word in enumerate(inverse["ST_residuals"])] + [
        (f"TS_generator_{i+1}", word)
        for i, word in enumerate(inverse["TS_residuals"])]
    targets = base["targets"][:-len(source_relations)]
    targets.extend((name, "endomorphism_relation", word)
                   for name, word in relation_residuals)
    targets.extend((name, "onto_two_sided_inverse", word)
                   for name, word in onto_residuals)
    base["inverse"] = inverse
    base["targets"] = targets
    base["quotient_bad"] = [name for name, _, word in targets
                            if e4.eval(word) != e4.identity]
    return base


###############################################################################
# Lossless receipt encoding.
###############################################################################


class ElementRegistry:
    def __init__(self, quotients: dict[int, MatchedQuotient]) -> None:
        self.quotients = quotients
        self.ids: dict[tuple[int, EKey], int] = {}
        self.rows: list[dict[str, Any]] = []

    def add(self, rank: int, element: EKey, section: Sequence[int]) -> int:
        key = (rank, element)
        if key in self.ids:
            return self.ids[key]
        quotient = self.quotients[rank]
        require(quotient.eval(section) == element, "registry section evaluation")
        if len(section) > CAPS["single_word_or_section_length"]:
            raise ResourceStop("single_word_or_section_length")
        identifier = len(self.rows) + 1
        self.ids[key] = identifier
        self.rows.append({
            "id": identifier,
            "rank": rank,
            "section_word": list(section),
            "coarse_permutation": [x+1 for x in element[0]],
            "fine_pc_coords": list(element[1]),
        })
        return identifier


def encode_vector(rank: int, vector: SparseVector,
                  sections: dict[EKey, list[int]],
                  registry: ElementRegistry) -> list[list[int]]:
    rows = []
    for (component, element), coefficient in sorted(vector.items()):
        require(element in sections, "missing vector support section")
        rows.append([component, registry.add(rank, element, sections[element]), coefficient])
    return rows


def boundary_certificate(name: str, kind: str, word: Sequence[int],
                         quotient: MatchedQuotient, proof_root_node_id: int,
                         registry: ElementRegistry) -> dict[str, Any]:
    gradient, value, sections = fox_gradient(word, quotient)
    require(value == quotient.identity, f"{name}: quotient identity")
    encoded_gradient = encode_vector(4, gradient, sections, registry)
    return {
        "name": name,
        "kind": kind,
        "arity": 4,
        "word": list(word),
        "quotient_identity": True,
        "gradient": encoded_gradient,
        "proof_root_node_id": proof_root_node_id,
        "proof_system": "shared_topological_F3_provenance_DAG",
        "gradient_sha256": digest_obj(encoded_gradient),
        "fox_membership": "word in Phi_3(H4) iff its evaluated Fox gradient lies in image(D2)",
    }


def _packed_array_block(type_name: str, typecode: str,
                        values: Sequence[int] | bytes | bytearray,
                        cap: int, monitor: ResourceMonitor | None = None) -> dict[str, Any]:
    estimated_itemsize = 1 if typecode == "B" else array(typecode).itemsize
    if monitor is not None:
        monitor.reserve("proof_DAG_array_bytes",
                        len(values)*estimated_itemsize*2 + 1_048_576)
    if typecode == "B":
        raw = bytes(values)
        length = len(raw)
        itemsize = 1
    else:
        packed = values if isinstance(values, array) and values.typecode == typecode \
            else array(typecode, values)
        if sys.byteorder != "little":
            packed = array(typecode, packed)
            packed.byteswap()
        raw = packed.tobytes()
        length = len(packed)
        itemsize = packed.itemsize
    require(length <= cap, "packed certificate array cap")
    if monitor is not None:
        monitor.reserve("proof_DAG_base64",
                        len(raw) + ((len(raw)+2)//3)*4 + 1_048_576)
    encoded = base64.b64encode(raw).decode("ascii")
    if monitor is not None:
        monitor.check("proof_DAG_base64_complete", force=True)
    return {
        "type": type_name,
        "array_typecode": typecode,
        "endianness": "little",
        "length": length,
        "itemsize": itemsize,
        "byte_length": len(raw),
        "cap": cap,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "base64": encoded,
    }


def serialize_proof_dag(dag: ProvenanceDAG, roots: dict[str, int],
                        basis: SparseBoundaryBasis,
                        registry: ElementRegistry) \
        -> tuple[dict[str, Any], dict[int, int]]:
    require(bool(roots), "proof DAG roots")
    if basis.deadline is not None:
        basis.deadline.check("proof_DAG_pre_serialization_RSS", force=True)
    if basis.deadline is not None:
        basis.deadline.reserve("proof_DAG_reachability",
                               (dag.node_count+1)*16 + dag.edge_count*6 +
                               67_108_864)
    reached = bytearray(dag.node_count+1)
    pending = array("I", roots.values())
    reached_count = 0
    while pending:
        old_id = int(pending.pop())
        require(1 <= old_id <= dag.node_count, "proof DAG root/reference range")
        if reached[old_id]:
            continue
        reached[old_id] = 1
        reached_count += 1
        if dag.kind[old_id-1] == dag.LINEAR:
            pending.extend(parent for parent, _ in dag.terms(old_id))
        if basis.deadline is not None and (reached_count & 4095) == 0:
            basis.deadline.check("proof_DAG_reachability")
    renumber = array("I", [0]) * (dag.node_count+1)
    next_id = 0
    for old_id in range(1, dag.node_count+1):
        if reached[old_id]:
            next_id += 1
            renumber[old_id] = next_id
    kinds = bytearray()
    relators = array("H")
    translations = array("I")
    offsets = array("I", [0])
    parents = array("I")
    coefficients = bytearray()
    leaf_count = 0
    for old_id in range(1, dag.node_count+1):
        if not reached[old_id]:
            continue
        new_id = int(renumber[old_id])
        if basis.deadline is not None and new_id % 1024 == 0:
            basis.deadline.check("proof_DAG_compact_serialization")
        kind = dag.kind[old_id-1]
        if kind == dag.LEAF:
            internal_id = int(dag.leaf_translation[old_id-1])
            section_node = basis.sections.node_for(internal_id)
            section = basis.sections.materialize(section_node)
            require(basis.pool.eval_id(section) == internal_id,
                    "materialized lazy section evaluation")
            external_id = registry.add(4, basis.pool.value(internal_id), section)
            kinds.append(1)
            relators.append(int(dag.leaf_relator[old_id-1]))
            translations.append(external_id)
            leaf_count += 1
        else:
            require(kind == dag.LINEAR, "packed proof DAG node kind")
            kinds.append(2)
            relators.append(0)
            translations.append(0)
            for parent, coefficient in dag.terms(old_id):
                require(reached[parent] and 0 < renumber[parent] < new_id and
                        coefficient in (1, 2), "proof DAG topological term")
                parents.append(int(renumber[parent]))
                coefficients.append(coefficient)
        offsets.append(len(parents))
    root_rows = [{"name": name, "node_id": int(renumber[node_id])}
                 for name, node_id in roots.items()]
    arrays = {
        "node_kind": _packed_array_block("uint8", "B", kinds,
                                          CAPS["provenance_dag_nodes"],
                                          basis.deadline),
        "leaf_relator_index": _packed_array_block(
            "uint16", "H", relators, CAPS["provenance_dag_nodes"],
            basis.deadline),
        "leaf_translation_element_id": _packed_array_block(
            "uint32", "I", translations, CAPS["provenance_dag_nodes"],
            basis.deadline),
        "edge_offsets": _packed_array_block(
            "uint32", "I", offsets, CAPS["provenance_dag_nodes"]+1,
            basis.deadline),
        "edge_parent_node_id": _packed_array_block(
            "uint32", "I", parents, CAPS["provenance_dag_edges"],
            basis.deadline),
        "edge_coefficient": _packed_array_block(
            "uint8", "B", coefficients, CAPS["provenance_dag_edges"],
            basis.deadline),
    }
    manifest = {
        name: {key: value for key, value in block.items() if key != "base64"}
        for name, block in arrays.items()
    }
    payload = {
        "format": "packed-parallel-arrays/v1",
        "field": 3,
        "node_order": "one_based_topological",
        "translation_action": "left",
        "arrays": arrays,
        "roots": root_rows,
        "node_count": reached_count,
        "edge_count": len(parents),
        "leaf_count": leaf_count,
        "combination_node_count": reached_count-leaf_count,
        "all_serialized_nodes_reachable_from_roots": True,
        "unreachable_search_nodes_pruned": dag.node_count-reached_count,
        "expanded_boundary_ledgers_serialized": False,
        "packed_manifest_sha256": digest_obj({"arrays": manifest,
                                               "roots": root_rows}),
    }
    return payload, {old: int(renumber[old]) for old in roots.values()}


def encode_fox_model(model: dict[str, Any], quotient: MatchedQuotient,
                     registry: ElementRegistry) -> dict[str, Any]:
    rank = model["rank"]
    identity_id = registry.add(rank, quotient.identity, [])
    marked_ids = [registry.add(rank, value, [i])
                  for i, value in enumerate(quotient.generators, 1)]
    relator_rows = []
    for index, (word, gradient, sections) in enumerate(
            zip(model["relations"], model["columns"], model["sections"]), 1):
        relator_rows.append({
            "relator_index": index,
            "word": word,
            "quotient_identity": True,
            "gradient": encode_vector(rank, gradient, sections, registry),
            "D1_of_gradient_zero": True,
        })
    return {
        "rank": rank,
        "field": 3,
        "left_fox_convention": {
            "product_rule": "d(uv)=d(u)+u*d(v)",
            "positive_letter": "+prefix",
            "negative_letter": "advance prefix by x_i^-1, then -prefix",
            "D1": "sum_i coefficient*(q(x_i)-1) on the right",
            "translated_column": "left multiplication by the translation element",
        },
        "generator_count": len(quotient.generators),
        "relator_count": len(model["relations"]),
        "identity_element_id": identity_id,
        "marked_element_ids": marked_ids,
        "relator_columns": relator_rows,
        "D1D2_zero": True,
        "full_regular_matrix_constructed": False,
        "H1_basis_or_rank_constructed": False,
    }


@dataclass
class CompactCandidate:
    correction_index: int
    names: tuple[str, ...]
    kinds: tuple[str, ...]
    gradients: tuple[PackedSparseVector, ...]
    quotient_value_ids: tuple[int, ...]

    def accounting(self) -> dict[str, int]:
        return {"target_count": len(self.names),
                "sparse_entries": sum(len(row) for row in self.gradients)}


def candidate_gradients(candidate: dict[str, Any], pool: ElementPool,
                        correction_index: int) -> CompactCandidate:
    names: list[str] = []
    kinds: list[str] = []
    gradients: list[PackedSparseVector] = []
    values: list[int] = []
    for name, kind, word in candidate["targets"]:
        gradient, value = fox_gradient_packed(word, pool)
        require(value == pool.identity_id, f"candidate target not in H4: {name}")
        names.append(name)
        kinds.append(kind)
        gradients.append(gradient)
        values.append(value)
    return CompactCandidate(correction_index, tuple(names), tuple(kinds),
                            tuple(gradients), tuple(values))


def solve_candidate(candidate: CompactCandidate, basis: SparseBoundaryBasis) \
        -> dict[str, int] | None:
    checkpoint = basis.dag.checkpoint()
    answer: dict[str, int] = {}
    try:
        for name, gradient in zip(candidate.names, candidate.gradients):
            root = basis.solve(gradient)
            if root is None:
                basis.dag.rollback(checkpoint)
                return None
            answer[name] = root
        return answer
    except Exception:
        basis.dag.rollback(checkpoint)
        raise


def make_base_receipt(q3_path: Path, output_path: Path, q3_data: dict[str, Any],
                      source_hashes: dict[str, str], status: str,
                      reason: str) -> dict[str, Any]:
    require(status in TERMINALS, "terminal")
    return {
        "schema": SCHEMA,
        "status": status,
        "terminal_token": status,
        "reason": reason,
        "pins": {
            "q3_producer": {"path": str(Q3_PRODUCER).replace("\\", "/"),
                            "sha256": Q3_PRODUCER_SHA},
            "q3_checker": {"path": str(Q3_CHECKER).replace("\\", "/"),
                           "sha256": Q3_CHECKER_SHA},
            "q3_driver": {"path": str(Q3_DRIVER).replace("\\", "/"),
                          "sha256": Q3_DRIVER_SHA},
            "q3_artifact": {"path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                            "sha256": Q3_ARTIFACT_SHA},
            "semantic_reference_v2": {
                "producer": {"path": str(V2_PRODUCER).replace("\\", "/"),
                             "sha256": V2_PRODUCER_SHA},
                "checker": {"path": str(V2_CHECKER).replace("\\", "/"),
                            "sha256": V2_CHECKER_SHA},
                "driver": {"path": str(V2_DRIVER).replace("\\", "/"),
                           "sha256": V2_DRIVER_SHA},
                "role": "frozen v2 mathematics, universe, gates, and search order",
            },
            "semantic_reference_v1": {
                "producer": {"path": str(V1_PRODUCER).replace("\\", "/"),
                             "sha256": V1_PRODUCER_SHA},
                "checker": {"path": str(V1_CHECKER).replace("\\", "/"),
                            "sha256": V1_CHECKER_SHA},
                "driver": {"path": str(V1_DRIVER).replace("\\", "/"),
                           "sha256": V1_DRIVER_SHA},
                "role": "frozen semantic predicate and search-order reference",
            },
            "formula_sha256": FORMULA_SHA,
        },
        "source_hashes": source_hashes,
        "input_q3_terminal": q3_data.get("terminal_token"),
        "output_path": str(OUTPUT_PATH).replace("\\", "/"),
        "caps": CAPS,
        "representation_contract": {
            "version": "packed-v3",
            "persistent_element_equality": "exact canonical bytes; never a digest",
            "sparse_keys": "component plus stable zero-based exact element-pool ID",
            "pivot_order": "component then canonical EKey bytes; never insertion ID",
            "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
            "candidate_sections_retained": False,
            "proof_DAG_in_memory": "packed parallel arrays",
            "positive_DAG_serialization": "reachable union as typed little-endian base64 arrays",
            "cache_eviction_semantics": "capacity and eviction order affect speed only, never canonical values or search order",
            "persistent_checkpoint_resume": False,
        },
        "claim_classification": "unknown_not_obstruction",
        "theorem_boundary": {
            "proved_if_PASS": "one literal charming/onto outside pair survives every isolated elementary-F3 chief refinement L with Phi3(H4)<=L<=H4",
            "Phi3_H4_isolation_required": False,
            "covered": "all isolated elementary-F3 next-chief refinements immediately below current H4",
            "not_covered": ["nonabelian chief factors", "other primes",
                            "deeper iteration", "uniform cofinal tower", "global B4-B"],
        },
        "prohibited_work": {
            "relative_ANUPQ_calls": 0,
            "Reidemeister_Schreier": False,
            "full_Elements": False,
            "full_regular_matrices": False,
            "full_H1_basis_or_rank": False,
        },
    }


def _v2_reference_run(q3_path: Path, output_path: Path) -> dict[str, Any]:
    run_start = time.monotonic()
    phase_start = run_start
    deadline = SoftDeadline(run_start, CAPS["producer_soft_timeout_seconds"])
    basis: SparseBoundaryBasis | None = None
    repo = Path(__file__).resolve().parents[1]
    require(q3_path.resolve() == (repo/Q3_ARTIFACT_PATH).resolve() and
            output_path.resolve() == (repo/OUTPUT_PATH).resolve(),
            "production paths must be the fixed ci/out paths")
    for path, sha, label in ((repo/Q3_PRODUCER, Q3_PRODUCER_SHA, "q3 producer"),
                             (repo/Q3_CHECKER, Q3_CHECKER_SHA, "q3 checker"),
                             (repo/Q3_DRIVER, Q3_DRIVER_SHA, "q3 driver"),
                             (repo/V1_PRODUCER, V1_PRODUCER_SHA, "v1 producer"),
                             (repo/V1_CHECKER, V1_CHECKER_SHA, "v1 checker"),
                             (repo/V1_DRIVER, V1_DRIVER_SHA, "v1 driver")):
        require(digest_file(path) == sha, f"{label} SHA")
    require(digest_file(q3_path) == Q3_ARTIFACT_SHA, "q3 artifact SHA")
    q3_data = json.loads(q3_path.read_text(encoding="utf-8"))
    source_hashes = {
        "producer_sha256": digest_file(Path(__file__)),
        "checker_sha256": digest_file(repo/"search/check_d972_b345_relfrat3_v2.py"),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v2.g"),
    }
    receipt = make_base_receipt(q3_path, output_path, q3_data, source_hashes,
                                "B345_RELFRAT3_UNKNOWN_RESOURCE",
                                "initializing")
    receipt["soft_timeout"] = deadline.receipt(False)
    try:
        deadline.check("formula_reconstruction")
        require(digest_obj(q3_data["formulas"]) == FORMULA_SHA,
                "q3 full formula digest")
        formula = relevant_formula()
        q3_formula = q3_data["formulas"]
        require(formula["presentations"]["PB3"]["relations"] ==
                q3_formula["presentations"]["PB3"]["relations"] and
                formula["presentations"]["PB4"]["relations"] ==
                q3_formula["presentations"]["PB4"]["relations"] and
                formula["presentations"]["PB5"]["relations"] ==
                q3_formula["presentations"]["PB5"]["relations"] and
                formula["cofaces_3_4"] == q3_formula["cofaces_3_4"] and
                formula["a18_order"]["maps"] == q3_formula["a18_order"]["maps"],
                "relevant formula reconstruction")
        e3, e4, context = reconstruct_quotients(q3_data)
        receipt["formula_sha256"] = FORMULA_SHA
        receipt["relevant_formula"] = formula
        receipt["relevant_formula_sha256"] = digest_obj(formula)
        receipt["matched_quotients"] = {
            "E3": {"coarse_degree": e3.degree, "fine_pc_rank": e3.pc.n,
                   "definition": "Q0 x Pi3[3]; its kernel J_H is the authenticated coarse source correction kernel"},
            "E4": {"coarse_degree": e4.degree, "fine_pc_rank": e4.pc.n,
                   "definition": "Q4 x Pi4[3] from the frozen no-common-C3 gate"},
            "J_H": {"definition": "kernel(PB3 -> E3), with every selected correction also replayed through all five cofaces into H4"},
            "J_Phi": {
                "definition": "intersection_{j=0}^4 (coface_j)^-1 Phi3(H4)",
                "identified_with_Phi3_H3": False,
                "correction_membership_required": False,
                "quotient_J_H_over_J_Phi_is_lift_freedom": True,
            },
        }
        phase_start = phase("matched_quotients", phase_start)
        deadline.check("base_replay_dictionary")
        base_replay = replay_base_q3(q3_data, e3, e4)
        receipt["base_q3_replay"] = base_replay
        dictionary = correction_dictionary(q3_data, e3)
        receipt["correction_dictionary"] = dictionary
        phase_start = phase("base_replay_dictionary", phase_start)

        model3 = fox_model(3, e3)
        model4 = fox_model(4, e4)
        dag = ProvenanceDAG(deadline)
        basis = SparseBoundaryBasis(e4, model4["columns"], dag, deadline)
        normalized_inverse, base_source_key, finite_inverse_words = \
            normalized_inverse_fibre(q3_data, e4)
        receipt["normalized_inverse_fibre"] = normalized_inverse
        inverse_cache: dict[tuple[EKey, ...], list[list[int]]] = {
            base_source_key: finite_inverse_words,
        }
        inverse_cache_stats = {"hits": 0, "misses": 0,
                               "max_inverse_word_length":
                                   normalized_inverse["max_inverse_word_length"]}
        prepared: list[tuple[int, dict[str, Any]]] = []
        cheap_rejected: list[dict[str, Any]] = []
        resource_skips: list[dict[str, Any]] = []
        for correction_index, correction in enumerate(dictionary["words"], 1):
            deadline.check("cheap_candidate_preparation")
            try:
                candidate = prepare_candidate(
                    reduce_word(FIXED_WORD + correction), correction, e4)
            except ResourceStop as exc:
                if exc.reason == "producer_soft_timeout":
                    raise
                resource_skips.append({"candidate_index": correction_index,
                                       "phase": "cheap_candidate_preparation",
                                       "reason": exc.reason})
                continue
            if candidate["quotient_bad"]:
                cheap_rejected.append({"candidate_index": correction_index,
                                       "failed_gates": candidate["quotient_bad"]})
            else:
                prepared.append((correction_index, candidate))
        require(not any(row["candidate_index"] == 1 for row in cheap_rejected),
                "empty correction failed the exact cheap quotient gates")
        selected_candidate: dict[str, Any] | None = None
        selected_rows: list[tuple[str, str, list[int], SparseVector,
                                  dict[EKey, list[int]]]] = []
        selected_roots: dict[str, int] | None = None
        candidate_cache: dict[int, tuple[dict[str, Any],
                                         list[tuple[str, str, list[int], SparseVector,
                                                    dict[EKey, list[int]]]]]] = {}
        unusable_candidates: set[int] = set()
        full_quotient_rejected: list[dict[str, Any]] = []
        geometric_checkpoints: list[int] = []
        translations_used = 0
        tests = 0
        translate_cap = CAPS["coefficient_translates_per_relator"]
        for translation, section in translation_bfs(e4, translate_cap):
            deadline.check("translation_BFS")
            translations_used += 1
            for relator_index in range(1, len(model4["columns"])+1):
                basis.add_column(relator_index, translation, section)
            if (translations_used & (translations_used-1)) == 0:
                geometric_checkpoints.append(translations_used)
                # Empty stays first.  Starting at checkpoint 8, every cheap
                # survivor is tried in the registered dictionary order; no
                # survivor waits for the final 32768-column cap.
                checkpoint_candidates = prepared if translations_used >= 8 else prepared[:1]
                for correction_index, candidate in checkpoint_candidates:
                    deadline.check("geometric_candidate_checkpoint")
                    if correction_index in unusable_candidates:
                        continue
                    if correction_index not in candidate_cache:
                        try:
                            candidate = complete_candidate(
                                candidate, e4, inverse_cache,
                                inverse_cache_stats, normalized_inverse)
                            if candidate["quotient_bad"]:
                                full_quotient_rejected.append({
                                    "candidate_index": correction_index,
                                    "failed_gates": candidate["quotient_bad"],
                                })
                                unusable_candidates.add(correction_index)
                                continue
                            rows = candidate_gradients(candidate, e4)
                            candidate_cache[correction_index] = (candidate, rows)
                        except ResourceStop as exc:
                            if exc.reason == "producer_soft_timeout":
                                raise
                            resource_skips.append({
                                "candidate_index": correction_index,
                                "phase": "inverse_or_gradient",
                                "reason": exc.reason,
                            })
                            unusable_candidates.add(correction_index)
                            continue
                    candidate, rows = candidate_cache[correction_index]
                    tests += 1
                    try:
                        roots = solve_candidate(rows, basis)
                    except ResourceStop as exc:
                        if exc.reason == "producer_soft_timeout":
                            raise
                        resource_skips.append({
                            "candidate_index": correction_index,
                            "phase": "sparse_membership",
                            "reason": exc.reason,
                        })
                        unusable_candidates.add(correction_index)
                        candidate_cache.pop(correction_index, None)
                        continue
                    if roots is not None:
                        selected_candidate, selected_rows = candidate, rows
                        selected_roots = roots
                        selected_candidate["correction_index"] = correction_index
                        break
                if selected_candidate is not None:
                    break
            if translations_used % 128 == 0:
                print("D972_B345_RELFRAT3_SEARCH "
                      f"translations={translations_used} basis={len(basis.rows)} "
                      f"live_vectors={basis.live_vector_entries} "
                      f"dag_nodes={len(dag.nodes)} dag_edges={dag.edge_count}",
                      flush=True)

        receipt["search"] = {
            "method": "one shared incremental sparse Gaussian basis with immutable F3 provenance DAG",
            "translation_order": "BFS shortlex steps +1..+6,-1..-6",
            "translations_used": translations_used,
            "translates_per_relator": translations_used,
            "columns_seen": basis.columns_seen,
            "dependent_columns": basis.dependent_columns,
            "basis_size": len(basis.rows),
            "pivot_count": len(basis.rows),
            "live_sparse_vector_entries": basis.live_vector_entries,
            "max_pivot_vector_support": basis.max_vector_support,
            "max_transient_vector_support": basis.max_transient_vector_support,
            "elimination_operations": basis.elimination_operations,
            "provenance_DAG": {
                **dag.accounting(),
                "pivot_payload": "one sparse vector plus one DAG node id",
                "expanded_pivot_ledgers_stored": False,
                "failed_column_and_candidate_nodes_rolled_back": True,
                "positive_serialization": "root-reachable union only",
            },
            "candidate_membership_tests": tests,
            "same_basis_reused_for_all_candidates": True,
            "candidate_order": "empty first, then registered correction dictionary order",
            "cheap_candidates_evaluated": len(dictionary["words"]),
            "cheap_gate_evaluation": "direct E4 values without substituted-word materialization",
            "full_words_materialized_only_for_cheap_survivors": True,
            "cheap_survivor_indices": [index for index, _ in prepared],
            "cheap_rejected": cheap_rejected,
            "full_candidate_cache_size": len(candidate_cache),
            "full_quotient_rejected": full_quotient_rejected,
            "geometric_translation_checkpoints": geometric_checkpoints,
            "all_cheap_survivors_scheduled_from_checkpoint": 8,
            "candidate_resource_skips": resource_skips,
            "settled_automorphism_order_cache_size": len(inverse_cache),
            "quotient_inverse_cache": {
                "key": "exact ordered tuple of six E4 source images",
                "entries": len(inverse_cache),
                "hits": inverse_cache_stats["hits"],
                "misses": inverse_cache_stats["misses"],
                "tuple_match_count": inverse_cache_stats["hits"],
                "tuple_mismatch_count": inverse_cache_stats["misses"],
                "max_inverse_word_length":
                    inverse_cache_stats["max_inverse_word_length"],
                "cached_datum": "one pinned normalized exponent-seven full inverse word tuple",
                "cache_hit_replays_current_ST_TS_in_E4": True,
                "different_tuple_is_candidate_local_UNKNOWN": True,
                "raw_endomorphism_powering_fallback": False,
                "candidate_relations_gradients_proof_roots_reused": False,
                "componentwise_Q4_Pi4_inverse_words_combined": False,
            },
            "cheap_quotient_gates_precede_power_inverse": True,
            "raw_power_inverse_removed": True,
            "small_projection_used": False,
            "affine_candidates_used": 0,
            "bounded_failure_is_not_nonexistence": True,
            "nonpositive_result_is_obstruction": False,
        }
        if selected_candidate is None:
            if resource_skips:
                receipt["status"] = receipt["terminal_token"] = \
                    "B345_RELFRAT3_UNKNOWN_RESOURCE"
                reason_counts: dict[str, int] = {}
                for row in resource_skips:
                    reason_counts[row["reason"]] = reason_counts.get(row["reason"], 0) + 1
                receipt["reason"] = (
                    "one or more registered candidates hit a local resource cap; "
                    "the skipped candidates are not treated as failures")
                receipt["resource_stop"] = {
                    "candidate_local": True,
                    "reason_counts": reason_counts,
                    "skipped_candidates": resource_skips,
                    "no_mathematical_obstruction_claimed": True,
                }
            else:
                receipt["status"] = receipt["terminal_token"] = \
                    "B345_RELFRAT3_SEARCH_INCOMPLETE"
                receipt["reason"] = (
                    "registered translated-relator and correction caps exhausted without a full "
                    "proof root; no obstruction or nonexistence is claimed")
            receipt["direct_lane"] = {
                "literal_pair_found": False,
                "PB5_branch_constructed": False,
                "PB5_reason": "direct sparse membership itself remained incomplete, so B5 was not used to turn a search miss into a negative",
            }
            receipt["claim_classification"] = "unknown_not_obstruction"
            receipt["soft_timeout"] = deadline.receipt(False)
            receipt["performance"] = {"runtime_seconds": time.monotonic()-run_start,
                                      "phase_complete": "bounded_search"}
            return receipt

        require(selected_roots is not None, "selected proof roots missing")
        registry = ElementRegistry({3: e3, 4: e4})
        encoded_models = {
            "PB3": encode_fox_model(model3, e3, registry),
            "PB4": encode_fox_model(model4, e4, registry),
            "PB5": {"constructed": False,
                    "reason": "direct B3/B4 literal pair certified first"},
        }
        ordered_roots = {name: selected_roots[name]
                         for name, _, _, _, _ in selected_rows}
        proof_dag, root_renumber = serialize_proof_dag(
            dag, ordered_roots, basis, registry)
        certificates = []
        for name, kind, word, _, _ in selected_rows:
            deadline.check("boundary_certificate_serialization")
            certificates.append(boundary_certificate(
                name, kind, word, e4,
                root_renumber[selected_roots[name]], registry))
        receipt["quotient_element_registry"] = registry.rows
        receipt["fox_models"] = encoded_models
        receipt["boundary_proof_dag"] = proof_dag
        receipt["search"]["provenance_DAG"]["serialized_reachable_nodes"] = \
            proof_dag["node_count"]
        receipt["search"]["provenance_DAG"]["serialized_reachable_edges"] = \
            proof_dag["edge_count"]
        correction_index = selected_candidate.get("correction_index", 1)
        selected_public = {key: value for key, value in selected_candidate.items()
                           if key not in ("targets", "quotient_bad") and
                           not key.startswith("_")}
        selected_public["correction_index"] = correction_index
        selected_public["boundary_certificate_names"] = [x["name"] for x in certificates]
        selected_public["correction_coarse_J_H_all_five_replayed"] = True
        selected_public["correction_finer_J_Phi_membership_not_required"] = True
        selected_public["all_ten_hexagon_coface_memberships_certified"] = True
        selected_public["ordered_A18_pentagon_certified"] = True
        selected_public["S_and_T_relations_certified"] = True
        selected_public["ST_and_TS_generator_compositions_certified"] = True
        receipt["selected_pair"] = selected_public
        receipt["boundary_certificates"] = certificates
        receipt["literal_replay"] = {
            "correction_lift_freedom": {
                "coarse_J_H_all_five_cofaces_identity": True,
                "finer_J_Phi_membership_required": False,
                "J_H_mod_J_Phi_coset_is_varied": True,
            },
            "hexagon": {"two_source_residuals": True,
                         "each_checked_in_all_five_cofaces": True},
            "pentagon": {"ordered_five_coface_A18_direct_PB4_residual": True},
            "charming": {"explicit_commutator_product": True,
                          "error_checked_in_all_five_cofaces": True,
                          "raw_exponent_sums_used_as_criterion": False},
            "marking": {"m": 0, "lambda": 1, "additional_residuals": []},
            "onto": {"two_sided_inverse_on_six_marked_generators": True,
                     "PB4_relations_for_both_maps": True},
        }
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_LITERAL_PAIR_PASS"
        receipt["claim_classification"] = "positive_certificate"
        receipt["reason"] = "one coarse-J_H correction coset gives literal hexagon, pentagon, charming, and two-sided onto residuals with an exact shared sparse Phi3(H4) provenance DAG"
        receipt["direct_lane"] = {"literal_pair_found": True,
                                  "PB5_branch_constructed": False,
                                  "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"}
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "literal_pair",
            "quotient_registry_size": len(registry.rows),
            "cache_policy": "quotient values, Fox gradients, translated columns, sparse pivots, shared DAG nodes, and sections cached",
        }
        receipt["soft_timeout"] = deadline.receipt(False)
        return receipt
    except ResourceStop as exc:
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.reason
        receipt["resource_stop"] = {"cap": exc.reason,
                                    "no_mathematical_obstruction_claimed": True}
        if basis is not None:
            receipt["resource_accounting_at_stop"] = basis.accounting()
        receipt["claim_classification"] = "unknown_not_obstruction"
        receipt["soft_timeout"] = deadline.receipt(
            exc.reason == "producer_soft_timeout")
        receipt["performance"] = {"runtime_seconds": time.monotonic()-run_start,
                                  "phase_complete": "resource_stop"}
        return receipt


def _pool_order_digest(pool: ElementPool,
                       monitor: ResourceMonitor | None = None) -> str:
    digest = hashlib.sha256()
    for index, blob in enumerate(pool.values, 1):
        require(len(blob) == pool.width, "pool digest width")
        digest.update(blob)
        if monitor is not None and (index & 4095) == 0:
            monitor.check("element_pool_binding_digest")
    return digest.hexdigest()


def _combined_pc_cache(e3: MatchedQuotient | None,
                       e4: MatchedQuotient | None) -> dict[str, Any]:
    rows = [] if e3 is None or e4 is None else [e3.pc.cache_accounting(),
                                                e4.pc.cache_accounting()]
    return {
        "collectors": rows,
        "hits": sum(row["hits"] for row in rows),
        "misses": sum(row["misses"] for row in rows),
        "evictions": sum(row["evictions"] for row in rows),
        "unbounded_full_token_word_cache": False,
    }


def run(q3_path: Path, output_path: Path) -> dict[str, Any]:
    run_start = time.monotonic()
    phase_start = run_start
    monitor = ResourceMonitor(run_start, CAPS["producer_soft_timeout_seconds"])
    repo = Path(__file__).resolve().parents[1]
    basis: SparseBoundaryBasis | None = None
    dag: ProvenanceDAG | None = None
    pool: ElementPool | None = None
    sections: LazySectionSLP | None = None
    e3: MatchedQuotient | None = None
    e4: MatchedQuotient | None = None
    candidate_cache: dict[int, CompactCandidate] = {}
    candidate_sparse_entries = 0
    proof_dag: dict[str, Any] | None = None
    registry: ElementRegistry | None = None
    state = {"translations": 0, "candidate_cache": 0}

    def live_accounting() -> dict[str, int]:
        pc = _combined_pc_cache(e3, e4)
        return {
            "translations": state["translations"],
            "columns": 0 if basis is None else basis.columns_seen,
            "pivots": 0 if basis is None else len(basis.rows),
            "live_sparse_entries": 0 if basis is None else basis.live_vector_entries,
            "element_pool": 0 if pool is None else len(pool.values),
            "dag_nodes": 0 if dag is None else dag.node_count,
            "dag_edges": 0 if dag is None else dag.edge_count,
            "candidate_cache": state["candidate_cache"],
            "pc_cache_hits": pc["hits"],
            "pc_cache_misses": pc["misses"],
            "pc_cache_evictions": pc["evictions"],
        }

    monitor.bind_accounting(live_accounting)
    require(q3_path.resolve() == (repo/Q3_ARTIFACT_PATH).resolve() and
            output_path.resolve() == (repo/OUTPUT_PATH).resolve(),
            "production paths must be the fixed ci/out paths")
    for path, sha, label in (
            (repo/Q3_PRODUCER, Q3_PRODUCER_SHA, "q3 producer"),
            (repo/Q3_CHECKER, Q3_CHECKER_SHA, "q3 checker"),
            (repo/Q3_DRIVER, Q3_DRIVER_SHA, "q3 driver"),
            (repo/V2_PRODUCER, V2_PRODUCER_SHA, "v2 producer"),
            (repo/V2_CHECKER, V2_CHECKER_SHA, "v2 checker"),
            (repo/V2_DRIVER, V2_DRIVER_SHA, "v2 driver"),
            (repo/V1_PRODUCER, V1_PRODUCER_SHA, "v1 producer"),
            (repo/V1_CHECKER, V1_CHECKER_SHA, "v1 checker"),
            (repo/V1_DRIVER, V1_DRIVER_SHA, "v1 driver")):
        require(digest_file(path) == sha, f"{label} SHA")
    require(digest_file(q3_path) == Q3_ARTIFACT_SHA, "q3 artifact SHA")
    q3_data = json.loads(q3_path.read_text(encoding="utf-8"))
    source_hashes = {
        "producer_sha256": digest_file(Path(__file__)),
        "checker_sha256": digest_file(repo/"search/check_d972_b345_relfrat3_v3.py"),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v3.g"),
    }
    receipt = make_base_receipt(q3_path, output_path, q3_data, source_hashes,
                                "B345_RELFRAT3_UNKNOWN_RESOURCE", "initializing")
    receipt["resource_guards"] = monitor.receipt(False)
    try:
        monitor.check("formula_reconstruction", force=True)
        require(digest_obj(q3_data["formulas"]) == FORMULA_SHA,
                "q3 full formula digest")
        formula = relevant_formula()
        q3_formula = q3_data["formulas"]
        require(formula["presentations"]["PB3"]["relations"] ==
                q3_formula["presentations"]["PB3"]["relations"] and
                formula["presentations"]["PB4"]["relations"] ==
                q3_formula["presentations"]["PB4"]["relations"] and
                formula["presentations"]["PB5"]["relations"] ==
                q3_formula["presentations"]["PB5"]["relations"] and
                formula["cofaces_3_4"] == q3_formula["cofaces_3_4"] and
                formula["a18_order"]["maps"] == q3_formula["a18_order"]["maps"],
                "relevant formula reconstruction")
        e3, e4, context = reconstruct_quotients(q3_data)
        pool = ElementPool(e4)
        sections = LazySectionSLP(pool.identity_id)
        receipt["formula_sha256"] = FORMULA_SHA
        receipt["relevant_formula"] = formula
        receipt["relevant_formula_sha256"] = digest_obj(formula)
        receipt["matched_quotients"] = {
            "E3": {"coarse_degree": e3.degree, "fine_pc_rank": e3.pc.n,
                   "definition": "Q0 x Pi3[3]; authenticated coarse source kernel"},
            "E4": {"coarse_degree": e4.degree, "fine_pc_rank": e4.pc.n,
                   "definition": "Q4 x Pi4[3] from the frozen no-common-C3 gate"},
            "J_H": {"definition": "kernel(PB3 -> E3), with each correction replayed through all five cofaces into H4"},
            "J_Phi": {
                "definition": "intersection_{j=0}^4 (coface_j)^-1 Phi3(H4)",
                "identified_with_Phi3_H3": False,
                "correction_membership_required": False,
                "quotient_J_H_over_J_Phi_is_lift_freedom": True,
            },
        }
        phase_start = phase("matched_quotients_packed_pool", phase_start)

        monitor.check("base_replay_dictionary")
        receipt["base_q3_replay"] = replay_base_q3(q3_data, e3, e4)
        dictionary = correction_dictionary(q3_data, e3)
        receipt["correction_dictionary"] = dictionary
        phase_start = phase("base_replay_dictionary", phase_start)

        # Raw models are small and retained solely for the positive external
        # certificate.  Every hot translated column uses the packed model.
        model3 = fox_model(3, e3)
        model4 = fox_model(4, e4)
        packed_model4 = packed_fox_model(4, pool)
        dag = ProvenanceDAG(monitor)
        basis = SparseBoundaryBasis(pool, packed_model4["columns"], dag,
                                    sections, monitor)
        normalized_inverse, raw_base_source_key, finite_inverse_words = \
            normalized_inverse_fibre(q3_data, e4)
        receipt["normalized_inverse_fibre"] = normalized_inverse
        base_source_key = tuple(pool.intern(value) for value in raw_base_source_key)
        inverse_cache: dict[tuple[int, ...], list[list[int]]] = {
            base_source_key: finite_inverse_words,
        }
        inverse_cache_stats = {
            "hits": 0, "misses": 0,
            "max_inverse_word_length": normalized_inverse["max_inverse_word_length"],
        }

        cheap_survivor_indices: list[int] = []
        cheap_rejected: list[dict[str, Any]] = []
        resource_skips: list[dict[str, Any]] = []
        for correction_index, correction in enumerate(dictionary["words"], 1):
            monitor.check("cheap_candidate_preparation")
            try:
                temporary = prepare_candidate(
                    reduce_word(FIXED_WORD + correction), correction, e4)
            except ResourceStop as exc:
                if exc.reason in {"producer_soft_timeout", "producer_soft_rss",
                                  "element_pool"}:
                    raise
                resource_skips.append({"candidate_index": correction_index,
                                       "phase": "cheap_candidate_preparation",
                                       "reason": exc.reason})
                continue
            if temporary["quotient_bad"]:
                cheap_rejected.append({"candidate_index": correction_index,
                                       "failed_gates": temporary["quotient_bad"]})
            else:
                cheap_survivor_indices.append(correction_index)
            del temporary
        require(not any(row["candidate_index"] == 1 for row in cheap_rejected),
                "empty correction failed exact cheap quotient gates")

        selected_candidate: dict[str, Any] | None = None
        selected_compact: CompactCandidate | None = None
        selected_roots: dict[str, int] | None = None
        unusable_candidates: set[int] = set()
        full_quotient_rejected: list[dict[str, Any]] = []
        geometric_checkpoints: list[int] = []
        tests = 0
        translate_cap = CAPS["coefficient_translates_per_relator"]

        for translation_id, section_node in translation_bfs(
                pool, sections, translate_cap):
            state["translations"] += 1
            monitor.check("translation_BFS")
            for relator_index in range(1, len(packed_model4["columns"])+1):
                basis.add_column(relator_index, translation_id, section_node)
            used = state["translations"]
            if (used & (used-1)) == 0:
                geometric_checkpoints.append(used)
                monitor.check("geometric_candidate_checkpoint", force=True)
                scheduled = (cheap_survivor_indices if used >= 8 else
                             cheap_survivor_indices[:1])
                for correction_index in scheduled:
                    monitor.check("geometric_candidate_checkpoint")
                    if correction_index in unusable_candidates:
                        continue
                    compact = candidate_cache.get(correction_index)
                    if compact is None:
                        correction = dictionary["words"][correction_index-1]
                        try:
                            temporary = prepare_candidate(
                                reduce_word(FIXED_WORD + correction), correction, e4)
                            temporary = complete_candidate(
                                temporary, e4, pool, inverse_cache,
                                inverse_cache_stats, normalized_inverse)
                            if temporary["quotient_bad"]:
                                full_quotient_rejected.append({
                                    "candidate_index": correction_index,
                                    "failed_gates": temporary["quotient_bad"],
                                })
                                unusable_candidates.add(correction_index)
                                del temporary
                                continue
                            compact = candidate_gradients(
                                temporary, pool, correction_index)
                            new_entries = sum(len(row) for row in compact.gradients)
                            if len(candidate_cache)+1 > CAPS["compact_candidate_cache"]:
                                raise ResourceStop("compact_candidate_cache")
                            if candidate_sparse_entries + new_entries > \
                                    CAPS["compact_candidate_sparse_entries"]:
                                raise ResourceStop("compact_candidate_sparse_entries")
                            candidate_sparse_entries += new_entries
                            candidate_cache[correction_index] = compact
                            state["candidate_cache"] = len(candidate_cache)
                            del temporary
                        except ResourceStop as exc:
                            if exc.reason in {"producer_soft_timeout",
                                              "producer_soft_rss", "element_pool",
                                              "compact_candidate_cache",
                                              "compact_candidate_sparse_entries"}:
                                raise
                            resource_skips.append({
                                "candidate_index": correction_index,
                                "phase": "inverse_or_gradient",
                                "reason": exc.reason,
                            })
                            unusable_candidates.add(correction_index)
                            continue
                    tests += 1
                    try:
                        roots = solve_candidate(compact, basis)
                    except ResourceStop as exc:
                        if exc.reason in {"producer_soft_timeout", "producer_soft_rss",
                                          "element_pool", "provenance_dag_nodes",
                                          "provenance_dag_edges",
                                          "total_sparse_group_ring_keys",
                                          "sparse_pivot_rows"}:
                            raise
                        resource_skips.append({
                            "candidate_index": correction_index,
                            "phase": "sparse_membership", "reason": exc.reason,
                        })
                        unusable_candidates.add(correction_index)
                        removed = candidate_cache.pop(correction_index, None)
                        if removed is not None:
                            candidate_sparse_entries -= sum(
                                len(row) for row in removed.gradients)
                        state["candidate_cache"] = len(candidate_cache)
                        continue
                    if roots is not None:
                        correction = dictionary["words"][correction_index-1]
                        rebuilt = prepare_candidate(
                            reduce_word(FIXED_WORD + correction), correction, e4)
                        rebuilt = complete_candidate(
                            rebuilt, e4, pool, inverse_cache,
                            inverse_cache_stats, normalized_inverse)
                        rebuilt_compact = candidate_gradients(
                            rebuilt, pool, correction_index)
                        require(rebuilt_compact == compact,
                                "selected compact candidate regeneration drift")
                        selected_candidate = rebuilt
                        selected_candidate["correction_index"] = correction_index
                        selected_compact = compact
                        selected_roots = roots
                        break
                if selected_candidate is not None:
                    break

        pc_cache = _combined_pc_cache(e3, e4)
        pool_accounting = pool.accounting()
        pool_integrity = {
            "size": len(pool.values), "lookup_size": len(pool.ids),
            "all_unique": len(pool.values) == len(pool.ids),
            "fixed_width_bytes": pool.width,
            "ordered_canonical_payload_sha256": _pool_order_digest(pool, monitor),
            "digest_is_binding_only_not_equality": True,
            "exported_internal_IDs": False,
            "positive_external_IDs_are_mapped_by_quotient_element_registry": True,
        }
        search_accounting = {
            "method": "one shared incremental sparse Gaussian basis with packed exact IDs and packed provenance DAG",
            "translation_order": "BFS shortlex steps +1..+6,-1..-6",
            "pivot_order": "component then canonical EKey bytes (v2 exact order), never insertion ID",
            "translations_used": state["translations"],
            "translates_per_relator": state["translations"],
            "columns_seen": basis.columns_seen,
            "dependent_columns": basis.dependent_columns,
            "basis_size": len(basis.rows), "pivot_count": len(basis.rows),
            "live_sparse_vector_entries": basis.live_vector_entries,
            "max_pivot_vector_support": basis.max_vector_support,
            "max_transient_vector_support": basis.max_transient_vector_support,
            "elimination_operations": basis.elimination_operations,
            "element_pool": pool_accounting,
            "element_pool_integrity": pool_integrity,
            "lazy_sections": sections.accounting(),
            "pc_caches": pc_cache,
            "provenance_DAG": {
                **dag.accounting(),
                "pivot_payload": "one packed sparse vector plus one packed DAG node id",
                "expanded_pivot_ledgers_stored": False,
                "failed_column_and_candidate_nodes_rolled_back": True,
                "positive_serialization": "root-reachable typed little-endian arrays only",
            },
            "candidate_membership_tests": tests,
            "same_basis_reused_for_all_candidates": True,
            "candidate_order": "empty first, then registered correction dictionary order",
            "cheap_candidates_evaluated": len(dictionary["words"]),
            "cheap_gate_evaluation": "direct E4 values without substituted-word retention",
            "full_words_materialized_only_transiently_for_cheap_survivors": True,
            "candidate_section_maps_retained": False,
            "cheap_survivor_indices": cheap_survivor_indices,
            "cheap_rejected": cheap_rejected,
            "compact_candidate_cache_size": len(candidate_cache),
            "compact_candidate_sparse_entries": candidate_sparse_entries,
            "compact_candidate_cache_cap": CAPS["compact_candidate_cache"],
            "compact_candidate_sparse_entries_cap": CAPS["compact_candidate_sparse_entries"],
            "compact_candidate_cache_payload": "names,kinds,packed gradients,quotient value IDs,correction index",
            "selected_candidate_regenerated_and_exactly_compared": selected_candidate is not None,
            "full_quotient_rejected": full_quotient_rejected,
            "geometric_translation_checkpoints": geometric_checkpoints,
            "all_cheap_survivors_scheduled_from_checkpoint": 8,
            "candidate_resource_skips": resource_skips,
            "settled_automorphism_order_cache_size": len(inverse_cache),
            "quotient_inverse_cache": {
                "key": "exact ordered tuple of six stable E4 element IDs",
                "entries": len(inverse_cache),
                "capacity": 1,
                "hits": inverse_cache_stats["hits"],
                "misses": inverse_cache_stats["misses"],
                "tuple_match_count": inverse_cache_stats["hits"],
                "tuple_mismatch_count": inverse_cache_stats["misses"],
                "max_inverse_word_length": inverse_cache_stats["max_inverse_word_length"],
                "cached_datum": "one pinned normalized exponent-seven full inverse word tuple",
                "cache_hit_replays_current_ST_TS_in_E4": True,
                "different_tuple_is_candidate_local_UNKNOWN": True,
                "raw_endomorphism_powering_fallback": False,
                "candidate_relations_gradients_proof_roots_reused": False,
                "componentwise_Q4_Pi4_inverse_words_combined": False,
            },
            "cheap_quotient_gates_precede_power_inverse": True,
            "raw_power_inverse_removed": True,
            "small_projection_used": False, "affine_candidates_used": 0,
            "bounded_failure_is_not_nonexistence": True,
            "nonpositive_result_is_obstruction": False,
        }
        receipt["search"] = search_accounting

        if selected_candidate is None:
            if resource_skips:
                receipt["status"] = receipt["terminal_token"] = \
                    "B345_RELFRAT3_UNKNOWN_RESOURCE"
                reason_counts: dict[str, int] = {}
                for row in resource_skips:
                    reason_counts[row["reason"]] = reason_counts.get(row["reason"], 0)+1
                receipt["reason"] = "registered candidates hit local resource caps and are not treated as failures"
                receipt["resource_stop"] = {
                    "candidate_local": True, "reason_counts": reason_counts,
                    "skipped_candidates": resource_skips,
                    "no_mathematical_obstruction_claimed": True,
                }
            else:
                receipt["status"] = receipt["terminal_token"] = \
                    "B345_RELFRAT3_SEARCH_INCOMPLETE"
                receipt["reason"] = "registered translated-relator and correction caps exhausted without a proof root; no obstruction or nonexistence is claimed"
            receipt["direct_lane"] = {
                "literal_pair_found": False, "PB5_branch_constructed": False,
                "PB5_reason": "bounded direct sparse membership remained incomplete",
            }
            receipt["claim_classification"] = "unknown_not_obstruction"
            monitor.check("bounded_search_complete", force=True)
            receipt["resource_guards"] = monitor.receipt(False)
            receipt["performance"] = {
                "runtime_seconds": time.monotonic()-run_start,
                "phase_complete": "bounded_search",
            }
            return receipt

        require(selected_roots is not None and selected_compact is not None,
                "selected packed proof roots")
        monitor.check("positive_certificate_reconstruction", force=True)
        selected_rows: list[tuple[str, str, list[int], SparseVector,
                                  dict[EKey, list[int]]]] = []
        for name, kind, word in selected_candidate["targets"]:
            gradient, value, support_sections = fox_gradient(word, e4)
            require(value == e4.identity, f"selected target quotient: {name}")
            selected_rows.append((name, kind, word, gradient, support_sections))
        require(tuple(row[0] for row in selected_rows) == selected_compact.names and
                tuple(row[1] for row in selected_rows) == selected_compact.kinds and
                tuple(intern_raw_vector(row[3], pool) for row in selected_rows) ==
                selected_compact.gradients,
                "selected raw/packed target regeneration")

        registry = ElementRegistry({3: e3, 4: e4})
        encoded_models = {
            "PB3": encode_fox_model(model3, e3, registry),
            "PB4": encode_fox_model(model4, e4, registry),
            "PB5": {"constructed": False,
                    "reason": "direct B3/B4 literal pair certified first"},
        }
        ordered_roots = {name: selected_roots[name]
                         for name, _, _, _, _ in selected_rows}
        proof_dag, root_renumber = serialize_proof_dag(
            dag, ordered_roots, basis, registry)
        certificates = []
        for name, kind, word, _, _ in selected_rows:
            monitor.check("boundary_certificate_serialization")
            certificates.append(boundary_certificate(
                name, kind, word, e4,
                root_renumber[selected_roots[name]], registry))
        monitor.check("positive_certificate_final_RSS", force=True)
        receipt["quotient_element_registry"] = registry.rows
        receipt["fox_models"] = encoded_models
        receipt["boundary_proof_dag"] = proof_dag
        receipt["search"]["provenance_DAG"]["serialized_reachable_nodes"] = \
            proof_dag["node_count"]
        receipt["search"]["provenance_DAG"]["serialized_reachable_edges"] = \
            proof_dag["edge_count"]
        correction_index = selected_candidate["correction_index"]
        selected_public = {key: value for key, value in selected_candidate.items()
                           if key not in ("targets", "quotient_bad") and
                           not key.startswith("_")}
        selected_public["correction_index"] = correction_index
        selected_public["boundary_certificate_names"] = [x["name"] for x in certificates]
        selected_public["correction_coarse_J_H_all_five_replayed"] = True
        selected_public["correction_finer_J_Phi_membership_not_required"] = True
        selected_public["all_ten_hexagon_coface_memberships_certified"] = True
        selected_public["ordered_A18_pentagon_certified"] = True
        selected_public["S_and_T_relations_certified"] = True
        selected_public["ST_and_TS_generator_compositions_certified"] = True
        receipt["selected_pair"] = selected_public
        receipt["boundary_certificates"] = certificates
        receipt["literal_replay"] = {
            "correction_lift_freedom": {
                "coarse_J_H_all_five_cofaces_identity": True,
                "finer_J_Phi_membership_required": False,
                "J_H_mod_J_Phi_coset_is_varied": True,
            },
            "hexagon": {"two_source_residuals": True,
                         "each_checked_in_all_five_cofaces": True},
            "pentagon": {"ordered_five_coface_A18_direct_PB4_residual": True},
            "charming": {"explicit_commutator_product": True,
                          "error_checked_in_all_five_cofaces": True,
                          "raw_exponent_sums_used_as_criterion": False},
            "marking": {"m": 0, "lambda": 1, "additional_residuals": []},
            "onto": {"two_sided_inverse_on_six_marked_generators": True,
                     "PB4_relations_for_both_maps": True},
        }
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_LITERAL_PAIR_PASS"
        receipt["claim_classification"] = "positive_certificate"
        receipt["reason"] = "one coarse-J_H correction coset gives all registered literal gates with an exact packed shared sparse Phi3(H4) provenance DAG"
        receipt["direct_lane"] = {"literal_pair_found": True,
                                  "PB5_branch_constructed": False,
                                  "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"}
        require(len(pool.values) == pool_integrity["size"],
                "positive certificate introduced an unregistered pool value")
        receipt["search"]["element_pool"] = pool.accounting()
        receipt["search"]["pc_caches"] = _combined_pc_cache(e3, e4)
        receipt["resource_guards"] = monitor.receipt(False)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "literal_pair",
            "quotient_registry_size": len(registry.rows),
            "cache_policy": "bounded exact LRU caches, packed element IDs, compact candidates, packed reachable DAG",
        }
        return receipt
    except ResourceStop as exc:
        accounting: dict[str, Any] = {
            "live": live_accounting(),
            "monitor": monitor.receipt(True),
        }
        if basis is not None:
            accounting["basis"] = basis.accounting()
        if pool is not None:
            accounting["element_pool"] = pool.accounting()
        accounting["candidate_cache_size"] = len(candidate_cache)
        accounting["candidate_sparse_entries"] = candidate_sparse_entries
        # Release the structures which caused v2's hosted-runner loss before
        # constructing or writing even the bounded UNKNOWN receipt.
        candidate_cache.clear()
        if proof_dag is not None:
            proof_dag.clear()
        if registry is not None:
            registry.ids.clear()
            registry.rows.clear()
        if basis is not None:
            basis.clear()
        if dag is not None:
            dag.clear()
        if sections is not None:
            sections.clear()
        if pool is not None:
            pool.clear_large()
        if e3 is not None:
            e3.pc.clear_caches()
        if e4 is not None:
            e4.pc.clear_caches()
        gc.collect()
        receipt["status"] = receipt["terminal_token"] = \
            "B345_RELFRAT3_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.reason
        receipt["resource_stop"] = {
            "cap": exc.reason,
            "candidate_local": False,
            "large_structures_released_before_write": True,
            "no_mathematical_obstruction_claimed": True,
        }
        receipt["resource_accounting_at_stop"] = accounting
        receipt["claim_classification"] = "unknown_not_obstruction"
        receipt["resource_guards"] = monitor.receipt(True)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic()-run_start,
            "phase_complete": "resource_stop",
        }
        return receipt


def self_test() -> None:
    require([len(pure_relations(r)) for r in (3, 4, 5)] == [2, 11, 35],
            "presentation counts")
    ledger = derived_commutator_ledger(FIXED_WORD)
    require(ledger["expanded_word"] == FIXED_WORD and ledger["factor_count"] > 0,
            "derived ledger")
    h = hexagon_words([])
    require(h == [[], []] and pentagon_word([]) == [], "trivial literal formulas")
    require(len(cofaces(3)) == 5 and
            [m[0] for m in [cofaces(3)[i] for i in (4, 0, 1, 2, 3)]] ==
            [[1], [4], [2, 4], [1, 2], [1]], "A18 coface order")
    class TrivialE4:
        identity = 0
        generators = [0] * 6

        @staticmethod
        def eval(word: Sequence[int], images: Sequence[int] | None = None) -> int:
            return 0

    toy = TrivialE4()
    toy_key = tuple(toy.generators)
    toy_cache = {toy_key: [[i] for i in range(1, 7)]}
    toy_stats = {"hits": 0, "misses": 0, "max_inverse_word_length": 0}
    toy_normalized = {"selected_correction_index": 1, "passing_indices": [1]}
    class TrivialPool:
        @staticmethod
        def intern(value: int) -> int:
            return value

    first = finite_normalized_inverse([], toy, TrivialPool(), toy_cache,
                                      toy_stats, toy_normalized)
    second = finite_normalized_inverse([1], toy, TrivialPool(), toy_cache,
                                       toy_stats, toy_normalized)
    require(first["source_words"] != second["source_words"] and
            toy_stats == {"hits": 2, "misses": 0,
                          "max_inverse_word_length": 1},
            "same E4 tuple/distinct free representative cache-hit canary")
    pc_receipt = {
        "generator_count": 1,
        "relative_orders": [3],
        "power_relations": [[0]],
        "inverses": [[2]],
        "conjugate_relations": [],
        "inverse_conjugate_relations": [],
    }
    pc = PcCollector(pc_receipt)
    one, a, b = pc.coord([0]), pc.coord([1]), pc.coord([2])
    corpus = [one, a, b]
    require(all(pc.mul(left, right) ==
                pc.collect_uncached(coords_word(left)+coords_word(right))
                for left in corpus for right in corpus) and
            all(pc.mul(left, right) ==
                pc.collect_uncached(coords_word(left)+coords_word(right))
                for left in corpus for right in corpus) and
            pc.cache_accounting()["hits"] >= 9,
            "bounded cached/uncached PC canary")

    class ToyPC:
        n = 1

    class ToyQuotient:
        rank = 4
        degree = 3
        pc = ToyPC()
        identity = (bytes(range(3)), bytes([0]))
        generators = [(bytes(range(3)), bytes([1]))] + [identity] * 5
        inverse_generators = [(bytes(range(3)), bytes([2]))] + [identity] * 5

        @staticmethod
        def mul(left: EKey, right: EKey) -> EKey:
            return bytes(range(3)), bytes([(left[1][0]+right[1][0]) % 3])

        @staticmethod
        def inverse(value: EKey) -> EKey:
            return bytes(range(3)), bytes([(-value[1][0]) % 3])

        def eval(self, word: Sequence[int], images: Sequence[EKey] | None = None) -> EKey:
            marked = self.generators if images is None else images
            out = self.identity
            for letter in word:
                value = marked[abs(letter)-1]
                out = self.mul(out, value if letter > 0 else self.inverse(value))
            return out

    tq = ToyQuotient()
    epool = ElementPool(tq)  # type: ignore[arg-type]
    require(epool.intern(tq.generators[0]) == epool.generator_ids[0] and
            len(epool.values) == len(epool.ids) == 3,
            "exact interning canary")
    slp = LazySectionSLP(epool.identity_id)
    packed_bfs = list(translation_bfs(epool, slp, 3))
    reference_bfs = list(_v2_reference_translation_bfs(tq, 3))
    require([epool.value(eid) for eid, _ in packed_bfs] ==
            [value for value, _ in reference_bfs] and
            [slp.materialize(node) for _, node in packed_bfs] ==
            [word for _, word in reference_bfs],
            "lazy/reference BFS order and section canary")
    raw_gradient, raw_value, _ = fox_gradient([1, 1, 1], tq)  # type: ignore[arg-type]
    packed_gradient, packed_value = fox_gradient_packed([1, 1, 1], epool)
    require(raw_value == tq.identity and packed_value == epool.identity_id and
            intern_raw_vector(raw_gradient, epool) == packed_gradient and
            d1(raw_gradient, tq) == {} and d1_packed(packed_gradient, epool) == {},
            "v2/reference versus packed Fox column differential")

    toy_dag = ProvenanceDAG()
    leaf_a = toy_dag.leaf(1, epool.identity_id)
    leaf_b = toy_dag.leaf(2, epool.generator_ids[0])
    root = toy_dag.linear([(leaf_a, 1), (leaf_b, 2)])
    checkpoint = toy_dag.checkpoint()
    toy_dag.linear([(root, 2), (leaf_a, 1)])
    toy_dag.rollback(checkpoint)
    require(root == 4 and toy_dag.terms(root) ==
            [(leaf_a, 1), (leaf_b, 2)] and toy_dag.reachable([root]) ==
            {leaf_a, leaf_b, root}, "shared provenance DAG/rollback canary")

    toy_sections = LazySectionSLP(epool.identity_id)
    first_node = toy_sections.append(0, 1)
    toy_sections.bind(epool.generator_ids[0], first_node)
    relator_column = {pack_vector_key(1, epool.identity_id): 1}
    toy_basis = SparseBoundaryBasis(epool, [relator_column], ProvenanceDAG(),
                                    toy_sections)
    toy_basis.add_column(1, epool.identity_id, 0)
    require(toy_basis.solve(relator_column) is not None and
            toy_basis.pivot({pack_vector_key(2, epool.generator_ids[0]): 1,
                             pack_vector_key(1, epool.inverse_generator_ids[0]): 1}) ==
            pack_vector_key(1, epool.inverse_generator_ids[0]),
            "packed translated-column/basis/pivot-order canary")

    guard = ResourceMonitor(time.monotonic(), CAPS["producer_soft_timeout_seconds"],
                            rss_reader=lambda: CAPS["producer_soft_rss_bytes"])
    try:
        guard.check("selftest_RSS", force=True)
        raise Reject("RSS guard did not stop")
    except ResourceStop as exc:
        require(exc.reason == "producer_soft_rss", "RSS UNKNOWN canary")
    require(TERMINALS == {"B345_RELFRAT3_LITERAL_PAIR_PASS",
                          "B345_RELFRAT3_SEARCH_INCOMPLETE",
                          "B345_RELFRAT3_UNKNOWN_RESOURCE"},
            "terminal mutation canary")
    print("D972_B345_RELFRAT3_V3_PRODUCER_SELFTEST_PASS "
          f"relevant_formula_sha256={digest_obj(relevant_formula())} "
          "interning=1 pc_cache_differential=1 bfs_differential=1 "
          "packed_basis_checkpoints=1 packed_DAG_rollback=1 RSS_UNKNOWN=1 "
          "terminal_mutations=3")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("q3_artifact", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        require(args.q3_artifact is None and args.output is None,
                "selftest accepts no paths")
        self_test()
        return 0
    require(args.q3_artifact is not None and args.output is not None,
            "q3 artifact and output paths required")
    receipt = run(args.q3_artifact.resolve(), args.output)
    checked_write(args.output, receipt)
    print(f"{receipt['terminal_token']} output={args.output} "
          f"receipt_sha256={digest_file(args.output)}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(f"B345_RELFRAT3_PRODUCER_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
