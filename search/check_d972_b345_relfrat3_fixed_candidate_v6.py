#!/usr/bin/env python3
"""Independent checker for cap-calibrated fixed-candidate v6.

No producer helper is imported.  The checker rebuilds the presentations,
cofaces, matched quotient arithmetic, Fox gradients, every shared-DAG leaf
and operation, and every accepted literal residual.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import sys
import time
from array import array
from collections import OrderedDict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA = "d972-b345-relative-frattini3-fixed-candidate-cap/v6"
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
OUTPUT_PATH = Path("ci/out/d972_b345_relfrat3_fixed_candidate_v6.json")
V5_PRODUCER = Path("search/d972_b345_relfrat3_fixed_candidate_v5.py")
V5_PRODUCER_SHA = "e4675906601714ee16219d747cf95ffef54b19e354228dd6e7d3cd99d59127ea"
V5_CHECKER = Path("search/check_d972_b345_relfrat3_fixed_candidate_v5.py")
V5_CHECKER_SHA = "0cb7e0173fe022f304010c64ef89b7200464f4ad8c1e1bc7c3ad4001ffe12246"
V5_DRIVER = Path("search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g")
V5_DRIVER_SHA = "3bcb19326bfff1e313870a64cca95840b0e581aa1f7c713ee18300faf149261d"
V4_PRODUCER = Path("search/d972_b345_relfrat3_v4.py")
V4_PRODUCER_SHA = "ff2e021647fdaf84697c91f741f2d039575036bc1f389d9dc59dee512e6ca7e1"
V4_CHECKER = Path("search/check_d972_b345_relfrat3_v4.py")
V4_CHECKER_SHA = "54308d8628cd434bbc6a4522fe86296d72d01b42de8db2bc72ea9a6961157c2b"
V4_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v4.g")
V4_DRIVER_SHA = "b717b6a214913d26207ba4683bbe0403123d5139b5aa45cd7bba62be2b885d56"
V3_PRODUCER = Path("search/d972_b345_relfrat3_v3.py")
V3_PRODUCER_SHA = "df60849f9fa4bb6a09e0d23d799e31473960544728db6eb5507a6fd54749343b"
V3_CHECKER = Path("search/check_d972_b345_relfrat3_v3.py")
V3_CHECKER_SHA = "11345a8db5ff6d08fa8395301c270532d0d96714cc8d77d98643dac04a6856cf"
V3_DRIVER = Path("search/d972_b345_relfrat3_gha_driver_v3.g")
V3_DRIVER_SHA = "fe7a76191a484194696931c5acb59ec6ee0115af75d543613281c28e4d6a4d7a"
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
CAPS = {
    "small_representation_dimension": 64,
    "candidate_correction_dictionary": 4096,
    "coefficient_translates_per_relator": 32768,
    "total_sparse_group_ring_keys": 4_194_304,
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
    "element_pool": 2_000_000,
    "element_product_cache": 262_144,
    "element_inverse_cache": 65_536,
    "pc_pair_product_cache": 65_536,
    "pc_inverse_cache": 16_384,
    "section_slp_nodes": 65_536,
    "persistent_candidate_gradient_entries": 0,
    "blocker_table": 4_096,
    "transaction_trace_records": 100_000,
    "cheap_contexts": 64,
    "progress_interval_seconds": 30,
}
V5_CAPS = {**CAPS,
           "total_sparse_group_ring_keys": 1_000_000,
           "element_pool": 1_000_000}
CAP_CALIBRATION = {
    "source_run": 32212335985,
    "source_receipt_sha256":
        "c9231ebb8fe65c47107556c6e06873fa68b74e148e1ab248cfada08a699975d4",
    "source_stop_reason": "total_sparse_group_ring_keys",
    "source_translations": 10809,
    "source_live_sparse_entries": 999999,
    "source_element_pool": 330011,
    "source_peak_RSS": 296407040,
    "old_sparse_cap": 1_000_000,
    "new_sparse_cap": 4_194_304,
    "old_pool_cap": 1_000_000,
    "new_pool_cap": 2_000_000,
    "semantics_changed": False,
    "resume_used": False,
}
TERMINALS = {
    "B345_RELFRAT3_FIXED_CANDIDATE_PASS",
    "B345_RELFRAT3_FIXED_CANDIDATE_INCOMPLETE",
    "B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE",
}
RESOURCE_REASONS = {
    "producer_soft_timeout", "producer_soft_rss", "blocker_table",
    "element_pool", "missing_bounded_inverse_representative",
    "provenance_dag_edges", "provenance_dag_nodes", "section_slp_nodes",
    "single_sparse_elimination_row", "single_word_or_section_length",
    "sparse_pivot_rows", "target_elimination_support",
    "total_sparse_group_ring_keys", "transaction_trace_records",
}


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


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


def current_rss_bytes() -> int:
    status = Path("/proc/self/status")
    if not status.exists():
        return 0
    for line in status.read_text(encoding="ascii").splitlines():
        if line.startswith("VmRSS:"):
            fields = line.split()
            require(len(fields) >= 3 and fields[2] == "kB", "checker VmRSS")
            return int(fields[1])*1024
    return 0


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(isinstance(x, int) and x != 0, "signed word letter")
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
        require(len(out) <= CAPS["single_word_or_section_length"], "word cap")
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-x for x in reversed(word))


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(1 <= abs(x) <= len(images), "substitution index")
        out = reduce_word(out +
                          list(images[x-1] if x > 0 else inv_word(images[-x-1])))
    return out


def pp(words: Sequence[Sequence[int]]) -> list[int]:
    require(bool(words), "empty paper product")
    return reduce_word(x for word in reversed(words) for x in word)


def commutator(a: Sequence[int], b: Sequence[int]) -> list[int]:
    return reduce_word(inv_word(a) + inv_word(b) + list(a) + list(b))


def exponent_sums(word: Sequence[int], width: int) -> list[int]:
    return [sum(1 if x > 0 else -1 for x in word if abs(x) == i)
            for i in range(1, width+1)]


def replay_derived_ledger(word: Sequence[int], block: dict[str, Any]) -> None:
    require(block["convention"] == "[a,b]=a^-1*b^-1*a*b", "commutator convention")
    expanded: list[int] = []
    for row in block["factors"]:
        expanded = reduce_word(expanded + commutator(row["left"], row["right"]))
    require(expanded == reduce_word(word) == block["expanded_word"] and
            len(block["factors"]) == block["factor_count"] and
            exponent_sums(word, 2) == [0, 0], "commutator-product witness")


###############################################################################
# Independent presentation and literal-formula reconstruction.
###############################################################################


def pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i+1, rank+1)]


def pair_index(rank: int, pair: Sequence[int]) -> int:
    require(list(pair) in pairs(rank), "pair index")
    return pairs(rank).index(list(pair)) + 1


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    require(1 <= i < rank, "Artin letter")
    rows = [[j] for j in range(1, rank+1)]
    if letter > 0:
        rows[i-1], rows[i] = [i, i+1, -i], [i]
    else:
        rows[i-1], rows[i] = [i+1], [-(i+1), i, i+1]
    return rows


def artin_images(rank: int, word: Sequence[int]) -> list[list[int]]:
    rows = [[i] for i in range(1, rank+1)]
    for letter in word:
        rows = [substitute(row, artin_step(rank, letter)) for row in rows]
    return rows


def aij(i: int, j: int) -> list[int]:
    return list(range(j-1, i, -1)) + [i, i] + [-k for k in range(i+1, j)]


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    old_pairs = pairs(rank-1)
    old_map = [[pair_index(rank, p)] for p in old_pairs]
    answer = [substitute(word, old_map) for word in pure_relations(rank-1)]
    kernel = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        g = pair_index(rank, [i, j])
        action = artin_images(rank-1, aij(i, j))
        for k in range(1, rank):
            h = pair_index(rank, [k, rank])
            answer.append(reduce_word([-g, h, g] +
                                      inv_word(substitute(action[k-1], kernel))))
    return answer


def coface_generator(rank: int, slot: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if slot == 0:
        return [pair_index(rank+1, [i+1, j+1])]
    if slot == rank+1:
        return [pair_index(rank+1, [i, j])]
    if i == slot:
        return [pair_index(rank+1, [slot, j+1]),
                pair_index(rank+1, [slot+1, j+1])]
    if j == slot:
        return [pair_index(rank+1, [i, slot]),
                pair_index(rank+1, [i, slot+1])]
    require(1 <= slot <= rank, "coface slot")
    return [pair_index(rank+1, [i+(i > slot), j+(j > slot)])]


def cofaces(rank: int) -> list[list[list[int]]]:
    return [[coface_generator(rank, s, p) for p in pairs(rank)]
            for s in range(rank+2)]


def formula_subset() -> dict[str, Any]:
    c34 = cofaces(3)
    return {
        "convention": {
            "pair_order": "lexicographic_i_then_j",
            "word_product": "left_to_right",
            "paper_product": "displayed_factors_multiplied_right_to_left",
            "coface_slots": "0=left endpoint,1..r=strand doubling,r+1=right endpoint",
        },
        "presentations": {f"PB{r}": {"pairs": pairs(r),
                                      "relations": pure_relations(r)}
                          for r in (3, 4, 5)},
        "cofaces_3_4": c34,
        "a18_order": {
            "names": ["phi_123", "phi_234", "phi_12_3_4",
                      "phi_1_23_4", "phi_1_2_34"],
            "slots": [4, 0, 1, 2, 3],
            "maps": [c34[i] for i in (4, 0, 1, 2, 3)],
        },
    }


def f2_sub(word: Sequence[int], x: Sequence[int], y: Sequence[int]) -> list[int]:
    return substitute(word, [x, y])


def hexagon_words(f: Sequence[int]) -> list[list[int]]:
    x, y = [1], [2]
    z, u = inv_word(pp([x, y])), inv_word(pp([y, x]))
    fxy, fxz, fyz = f2_sub(f, x, y), f2_sub(f, x, z), f2_sub(f, y, z)
    fux, fuy = f2_sub(f, u, x), f2_sub(f, u, y)
    return [pp([fxy, inv_word(fxz), fyz]),
            pp([inv_word(fux), inv_word(fxy), fuy])]


def embed_f2(word: Sequence[int]) -> list[int]:
    return substitute(word, [[1], [3]])


def pentagon_word(f: Sequence[int]) -> list[int]:
    g = [[i] for i in range(1, 7)]
    contexts = [[g[0], g[3]], [g[3], g[5]],
                [pp([g[1], g[3]]), g[5]],
                [pp([g[0], g[1]]), pp([g[4], g[5]])],
                [g[0], pp([g[3], g[4]])]]
    values = [f2_sub(f, x, y) for x, y in contexts]
    return pp([inv_word(pp([values[4], values[2]])),
               values[1], values[3], values[0]])


def source_words(f: Sequence[int]) -> list[list[int]]:
    ff, g, gs = substitute(f, [[1], [4]]), substitute(f, [[1], [2]]), \
        substitute(f, [[4], [5]])
    f1234 = substitute(f, [[4, 2], [6]])
    h = substitute(f, [[2, 1], [3]])
    middle = substitute(f, [[2, 1], [6, 5]])
    return [[1], reduce_word(inv_word(g)+[2]+g),
            reduce_word(inv_word(ff)+inv_word(h)+[3]+h+ff),
            reduce_word(inv_word(ff)+[4]+ff),
            reduce_word(inv_word(ff)+inv_word(middle)+inv_word(gs)+[5]+gs+middle+ff),
            reduce_word(inv_word(f1234)+[6]+f1234)]


###############################################################################
# Receipt-only finite arithmetic, implemented independently.
###############################################################################


Perm = tuple[int, ...]
Pc = tuple[int, ...]
Element = tuple[Perm, Pc]
VKey = tuple[int, Element]
Vector = dict[VKey, int]


def row_perm(row: Sequence[int], degree: int) -> Perm:
    require(len(row) == degree, "permutation width")
    value = tuple(x-1 for x in row)
    require(set(value) == set(range(degree)), "permutation bijection")
    return value


def p_one(degree: int) -> Perm:
    return tuple(range(degree))


def p_mul(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degrees")
    return tuple(b[a[i]] for i in range(len(a)))


def p_inv(a: Perm) -> Perm:
    out = [0]*len(a)
    for i, image in enumerate(a):
        out[image] = i
    return tuple(out)


def p_order(a: Perm) -> int:
    seen = [False]*len(a)
    answer = 1
    for i in range(len(a)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = a[j]
            length += 1
        answer = math.lcm(answer, length)
    return answer


def pc_word(coords: Sequence[int]) -> list[int]:
    return [i for i, exponent in enumerate(coords, 1) for _ in range(exponent)]


@dataclass
class Collector:
    data: dict[str, Any]

    def __post_init__(self) -> None:
        self.n = self.data["generator_count"]
        self.orders = list(self.data["relative_orders"])
        require(len(self.orders) == self.n <= 175 and all(x == 3 for x in self.orders),
                "collector rank/orders")
        self.powers = [self.coord(x) for x in self.data["power_relations"]]
        self.inverses = [self.coord(x) for x in self.data["inverses"]]
        self.conjugates = {(x["i"], x["j"]): self.coord(x["coords"])
                           for x in self.data["conjugate_relations"]}
        self.inv_conjugates = {(x["i"], x["j"]): self.coord(x["coords"])
                               for x in self.data["inverse_conjugate_relations"]}
        require(len(self.conjugates) == self.n*(self.n-1)//2 and
                set(self.conjugates) == set(self.inv_conjugates), "collector tables")
        self.pair_cache: OrderedDict[tuple[Pc, Pc], Pc] = OrderedDict()
        self.inverse_cache: OrderedDict[Pc, Pc] = OrderedDict()

    def coord(self, row: Sequence[int]) -> Pc:
        require(len(row) == self.n and all(isinstance(x, int) and 0 <= x < 3
                                           for x in row), "collector coordinate")
        return tuple(row)

    def identity(self) -> Pc:
        return (0,)*self.n

    def collect(self, signed: Sequence[int]) -> Pc:
        tokens: list[int] = []
        for x in signed:
            require(1 <= abs(x) <= self.n, "collector signed index")
            tokens.extend([x] if x > 0 else pc_word(self.inverses[-x-1]))
        cap = max(10000, 1000*(1+len(tokens))*(1+self.n))
        count = 0
        while True:
            changed = False
            for i in range(len(tokens)-1):
                if tokens[i] > tokens[i+1]:
                    a, b = tokens[i], tokens[i+1]
                    tokens[i:i+2] = [b] + pc_word(self.conjugates[(a, b)])
                    changed = True
                    break
            if not changed:
                i = 0
                while i < len(tokens):
                    j = i
                    while j < len(tokens) and tokens[j] == tokens[i]:
                        j += 1
                    if j-i >= 3:
                        tokens[i:i+3] = pc_word(self.powers[tokens[i]-1])
                        changed = True
                        break
                    i = j
            if not changed:
                break
            count += 1
            require(count <= cap, "collector rewrite cap")
        row = [0]*self.n
        last = 0
        for x in tokens:
            require(x >= last, "collector order")
            row[x-1] += 1
            require(row[x-1] < 3, "collector power")
            last = x
        return tuple(row)

    def mul(self, a: Pc, b: Pc) -> Pc:
        key = (a, b)
        if key in self.pair_cache:
            self.pair_cache.move_to_end(key)
            return self.pair_cache[key]
        answer = self.collect(pc_word(a)+pc_word(b))
        if len(self.pair_cache) >= CAPS["pc_pair_product_cache"]:
            self.pair_cache.popitem(last=False)
        self.pair_cache[key] = answer
        return answer

    def inverse(self, a: Pc) -> Pc:
        if a in self.inverse_cache:
            self.inverse_cache.move_to_end(a)
            return self.inverse_cache[a]
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(a[i-1]):
                word.extend(pc_word(self.inverses[i-1]))
        answer = self.collect(word)
        if len(self.inverse_cache) >= CAPS["pc_inverse_cache"]:
            self.inverse_cache.popitem(last=False)
        self.inverse_cache[a] = answer
        return answer

    def eval(self, word: Sequence[int], images: Sequence[Pc]) -> Pc:
        out = self.identity()
        for x in word:
            value = images[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out


@dataclass
class Quotient:
    rank: int
    degree: int
    collector: Collector
    generators: list[Element]

    def __post_init__(self) -> None:
        self.identity = (p_one(self.degree), self.collector.identity())
        self.inverse_generators = [self.inverse(x) for x in self.generators]

    def mul(self, a: Element, b: Element) -> Element:
        return p_mul(a[0], b[0]), self.collector.mul(a[1], b[1])

    def inverse(self, a: Element) -> Element:
        return p_inv(a[0]), self.collector.inverse(a[1])

    def eval(self, word: Sequence[int], images: Sequence[Element] | None = None) -> Element:
        marked = self.generators if images is None else images
        out = self.identity
        for x in word:
            value = marked[abs(x)-1]
            out = self.mul(out, value if x > 0 else self.inverse(value))
        return out


def reconstruct(data: dict[str, Any]) -> tuple[Quotient, Quotient]:
    c3, c4 = Collector(data["groups"]["PB3"]), Collector(data["groups"]["PB4"])
    fine3 = [c3.coord(x["coords"]) for x in data["groups"]["PB3"]["marked_generators"]]
    fine4 = [c4.coord(x["coords"]) for x in data["groups"]["PB4"]["marked_generators"]]
    q0r, q4r = data["coarse_models"]["Q0"], data["coarse_models"]["Q4"]
    q0 = [row_perm(x, q0r["degree"]) for x in q0r["marked_permutations"]]
    q4 = [row_perm(x, q4r["degree"]) for x in q4r["marked_permutations"]]
    z = p_inv(p_mul(q0[1], q0[0]))
    e3 = Quotient(3, q0r["degree"], c3,
                  [(q0[0], fine3[0]), (z, fine3[1]), (q0[1], fine3[2])])
    e4 = Quotient(4, q4r["degree"], c4, list(zip(q4, fine4)))
    require(all(e3.eval(r) == e3.identity for r in pure_relations(3)) and
            all(e4.eval(r) == e4.identity for r in pure_relations(4)),
            "matched presentation replay")
    return e3, e4


def add(vector: dict[Any, int], key: Any, coefficient: int) -> None:
    value = (vector.get(key, 0)+coefficient) % 3
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def add_scaled(target: dict[Any, int], source: dict[Any, int], scalar: int) -> None:
    for key, coefficient in source.items():
        add(target, key, scalar*coefficient)


def fox(word: Sequence[int], quotient: Quotient) -> tuple[Vector, Element]:
    prefix = quotient.identity
    out: Vector = {}
    for x in word:
        i = abs(x)
        if x > 0:
            add(out, (i, prefix), 1)
            prefix = quotient.mul(prefix, quotient.generators[i-1])
        else:
            prefix = quotient.mul(prefix, quotient.inverse_generators[i-1])
            add(out, (i, prefix), 2)
    return out, prefix


def boundary1(vector: Vector, quotient: Quotient) -> dict[Element, int]:
    out: dict[Element, int] = {}
    for (i, value), coefficient in vector.items():
        add(out, quotient.mul(value, quotient.generators[i-1]), coefficient)
        add(out, value, -coefficient)
    return out


def translate(vector: Vector, value: Element, quotient: Quotient) -> Vector:
    return {(i, quotient.mul(value, g)): coefficient
            for (i, g), coefficient in vector.items()}


def encode(vector: Vector, rank: int,
           element_to_id: dict[tuple[int, Element], int]) -> list[list[int]]:
    return [[i, element_to_id[(rank, value)], coefficient]
            for (i, value), coefficient in sorted(vector.items())]


def perm_eval(word: Sequence[int], images: Sequence[Perm]) -> Perm:
    out = p_one(len(images[0]))
    for x in word:
        value = images[abs(x)-1]
        out = p_mul(out, value if x > 0 else p_inv(value))
    return out


def enumerate_small(identity: Any, generators: Sequence[Any], mul: Any,
                    inverse: Any, cap: int) -> set[Any]:
    steps = list(generators)+[inverse(x) for x in generators]
    seen, queue = {identity}, [identity]
    while queue:
        a = queue.pop()
        for g in steps:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                require(len(seen) <= cap, "small group cap")
                queue.append(b)
    return seen


def paper_conj(value: Any, y: Any, mul: Any, inverse: Any) -> Any:
    return mul(mul(value, y), inverse(value))


def validate_base_replay(receipt: dict[str, Any], q3: dict[str, Any],
                         e3: Quotient, e4: Quotient) -> None:
    block = receipt["base_q3_replay"]
    selected = q3["selected_solution"]
    require(q3["schema"] == Q3_SCHEMA and q3["terminal_token"] ==
            "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" and
            selected["typed_source_word"] == FIXED_WORD and
            selected["correction_word"] == [] and selected["exponent"] == 2,
            "frozen q3 witness")
    require(block["fixed_word"] == FIXED_WORD and block["roof_exponent"] == 2 and
            block["roof_order"] == 9 and block["marking_m"] == 0 and
            block["lambda"] == 1 and block["replayed_not_copied"] is True,
            "base replay metadata")
    hexes = hexagon_words(FIXED_WORD)
    pent = pentagon_word(FIXED_WORD)
    require(block["hexagon_residual_words_F2"] == hexes and
            all(e3.eval(embed_f2(w)) == e3.identity for w in hexes),
            "base hexagon")
    require(block["pentagon_residual_word_PB4"] == pent and
            e4.eval(pent) == e4.identity, "base pentagon")
    replay_derived_ledger(FIXED_WORD, block["derived_membership"])
    q0_value = perm_eval(FIXED_WORD, [e3.generators[0][0], e3.generators[2][0]])
    require(p_order(q0_value) == 9, "base roof order")
    models = q3["coarse_models"]
    p = [row_perm(x, models["P"]["degree"]) for x in models["P"]["marked_permutations"]]
    g = [row_perm(x, models["G9"]["degree"]) for x in models["G9"]["marked_permutations"]]
    fp, fg = perm_eval(FIXED_WORD, p), perm_eval(FIXED_WORD, g)
    p_onto = len(enumerate_small(p_one(9), [p[0], paper_conj(fp, p[1], p_mul, p_inv)],
                                 p_mul, p_inv, 504)) == 504
    g_onto = len(enumerate_small(p_one(27), [g[0], paper_conj(fg, g[1], p_mul, p_inv)],
                                 p_mul, p_inv, 2916)) == 2916
    b = [e3.generators[0][1], e3.generators[2][1]]
    fb = e3.collector.eval(FIXED_WORD, b)
    b_onto = len(enumerate_small(e3.collector.identity(),
                                 [b[0], paper_conj(fb, b[1],
                                                   e3.collector.mul,
                                                   e3.collector.inverse)],
                                 e3.collector.mul, e3.collector.inverse, 27)) == 27
    require(block["onto_small_factors"] == {"P_order_504": p_onto,
                                             "G9_order_2916": g_onto,
                                             "B2_order_27": b_onto} and
            p_onto and g_onto and b_onto, "base onto factors")
    require(block["settled_source_words"] == source_words(FIXED_WORD),
            "base settlement source")


def rebuild_dictionary(q3: dict[str, Any], e3: Quotient) -> dict[str, Any]:
    base = [reduce_word(row["word"]*3) for row in q3["correction_fibre"]["records"]
            if row["word"]]
    base = list(dict.fromkeys(tuple(x) for x in base))
    seeds: list[list[int]] = []
    for raw in base:
        k = list(raw)
        require(e3.eval(embed_f2(k)) == e3.identity, "dictionary cube H3")
        for gen in ([1], [2]):
            for word in (commutator(k, gen), commutator(gen, k)):
                if word and word not in seeds:
                    require(exponent_sums(word, 2) == [0, 0] and
                            e3.eval(embed_f2(word)) == e3.identity,
                            "dictionary seed H3")
                    seeds.append(word)
    words: list[list[int]] = [[]]
    parent_indices = [0]
    signed_seed_edges = [0]
    seen = {()}
    queue: deque[int] = deque([1])
    steps = [(index+1, word) for index, word in enumerate(seeds)] + [
        (-(index+1), inv_word(word)) for index, word in enumerate(seeds)]
    require(all(e3.eval(embed_f2(word)) == e3.identity for word in seeds),
            "dictionary seed E3 kernel")
    while queue and len(words) < CAPS["candidate_correction_dictionary"]:
        parent_index = queue.popleft()
        prefix = words[parent_index-1]
        for signed_edge, step in steps:
            word = reduce_word(prefix+step)
            if tuple(word) not in seen:
                require(exponent_sums(word, 2) == [0, 0],
                        "dictionary free-derived invariant")
                seen.add(tuple(word))
                words.append(word)
                parent_indices.append(parent_index)
                signed_seed_edges.append(signed_edge)
                queue.append(len(words))
                if len(words) == CAPS["candidate_correction_dictionary"]:
                    break
    for index in range(1, len(words)):
        parent = parent_indices[index]
        edge = signed_seed_edges[index]
        step = seeds[abs(edge)-1]
        if edge < 0:
            step = inv_word(step)
        require(1 <= parent <= index and
                reduce_word(words[parent-1]+step) == words[index] and
                exponent_sums(words[index], 2) == [0, 0],
                "dictionary parent/edge reconstruction")
    provenance = {"parent_indices": parent_indices,
                  "signed_seed_edges": signed_seed_edges,
                  "word_sha256": [digest_obj(word) for word in words]}
    return {"order": "identity, then breadth-first products of authenticated H3 commutator seeds and inverses",
            "source": "commutators with cubes of the frozen 27-word coarse-trivial exponent-three fibre",
            "words": words, "count": len(words),
            "cap": CAPS["candidate_correction_dictionary"],
            "all_words_in_H3": True, "all_words_in_coarse_J_H": True,
            "all_words_free_exponent_zero": True,
            "not_complete_for_all_H3": True,
            "membership_in_finer_J_Phi_required": False,
            "J_Phi_cosets_are_the_lift_freedom": True,
            "seed_words": seeds,
            "parent_indices": parent_indices,
            "signed_seed_edges": signed_seed_edges,
            "identity_parent_edge": [0, 0],
            "all_parent_edges_reconstructed": True,
            "E3_kernel_proof": "identity plus authenticated kernel seeds, inverse/product closure",
            "all_words_E3_kernel_by_recurrence": True,
            "provenance_sha256": digest_obj(provenance)}


def q_product(q: Quotient, values: Sequence[Element]) -> Element:
    out = q.identity
    for value in values:
        out = q.mul(out, value)
    return out


def q_paper_product(q: Quotient, values: Sequence[Element]) -> Element:
    return q_product(q, list(reversed(values)))


def element_blob(value: Element) -> bytes:
    return bytes(value[0]) + bytes(value[1])


def direct_cheap_failures(candidate: Sequence[int], correction: Sequence[int],
                          e4: Quotient) -> list[str]:
    coarse: list[str] = []
    first: list[str] = []
    second: list[str] = []
    for slot, mapping in enumerate(cofaces(3)):
        x, y = e4.eval(mapping[0]), e4.eval(mapping[2])
        if e4.eval(correction, [x, y]) != e4.identity:
            coarse.append(f"correction_coarse_J_H_coface_{slot}")
        z = e4.inverse(q_paper_product(e4, [x, y]))
        u = e4.inverse(q_paper_product(e4, [y, x]))
        fxy = e4.eval(candidate, [x, y])
        fxz = e4.eval(candidate, [x, z])
        fyz = e4.eval(candidate, [y, z])
        fux = e4.eval(candidate, [u, x])
        fuy = e4.eval(candidate, [u, y])
        if q_paper_product(e4, [fxy, e4.inverse(fxz), fyz]) != e4.identity:
            first.append(f"hexagon_1_coface_{slot}")
        if q_paper_product(e4, [e4.inverse(fux), e4.inverse(fxy), fuy]) != \
                e4.identity:
            second.append(f"hexagon_2_coface_{slot}")
    bad = coarse + first + second
    g = e4.generators
    contexts = [
        [g[0], g[3]], [g[3], g[5]],
        [q_paper_product(e4, [g[1], g[3]]), g[5]],
        [q_paper_product(e4, [g[0], g[1]]),
         q_paper_product(e4, [g[4], g[5]])],
        [g[0], q_paper_product(e4, [g[3], g[4]])],
    ]
    parts = [e4.eval(candidate, context) for context in contexts]
    pent = q_paper_product(
        e4, [e4.inverse(q_paper_product(e4, [parts[4], parts[2]])),
             parts[1], parts[3], parts[0]])
    if pent != e4.identity:
        bad.append("ordered_A18_pentagon")
    source = source_words(candidate)
    for index, relation in enumerate(pure_relations(4), 1):
        if e4.eval(substitute(relation, source)) != e4.identity:
            bad.append(f"S_relation_{index}")
    return bad


def independent_context_registry(e4: Quotient) \
        -> tuple[list[tuple[Element, Element]], dict[str, int], dict[str, Any]]:
    contexts: list[tuple[Element, Element]] = []
    exact: dict[tuple[Element, Element], int] = {}
    named: list[dict[str, Any]] = []
    by_name: dict[str, int] = {}

    def register(name: str, left: Element, right: Element) -> None:
        require(name not in by_name, "duplicate independent context name")
        pair = (left, right)
        context_id = exact.get(pair)
        if context_id is None:
            context_id = len(contexts)+1
            exact[pair] = context_id
            contexts.append(pair)
        by_name[name] = context_id
        named.append({"name": name, "context_id": context_id})

    for slot, mapping in enumerate(cofaces(3)):
        x, y = e4.eval(mapping[0]), e4.eval(mapping[2])
        z = e4.inverse(q_paper_product(e4, [x, y]))
        u = e4.inverse(q_paper_product(e4, [y, x]))
        register(f"correction_coface_{slot}", x, y)
        register(f"hexagon_1_fxy_{slot}", x, y)
        register(f"hexagon_1_fxz_{slot}", x, z)
        register(f"hexagon_1_fyz_{slot}", y, z)
        register(f"hexagon_2_fux_{slot}", u, x)
        register(f"hexagon_2_fxy_{slot}", x, y)
        register(f"hexagon_2_fuy_{slot}", u, y)
    g = e4.generators
    pentagon = [
        (g[0], g[3]), (g[3], g[5]),
        (q_paper_product(e4, [g[1], g[3]]), g[5]),
        (q_paper_product(e4, [g[0], g[1]]),
         q_paper_product(e4, [g[4], g[5]])),
        (g[0], q_paper_product(e4, [g[3], g[4]])),
    ]
    for index, pair in enumerate(pentagon):
        register(f"pentagon_part_{index}", *pair)
    source_contexts = [
        ("source_ff", g[0], g[3]),
        ("source_g", g[0], g[1]),
        ("source_gs", g[3], g[4]),
        ("source_f1234", q_product(e4, [g[3], g[1]]), g[5]),
        ("source_h", q_product(e4, [g[1], g[0]]), g[2]),
        ("source_middle", q_product(e4, [g[1], g[0]]),
         q_product(e4, [g[5], g[4]])),
    ]
    for name, left, right in source_contexts:
        register(name, left, right)
    require(len(contexts) <= CAPS["cheap_contexts"], "context registry cap")
    rows = [{"context_id": index, "left_hex": element_blob(pair[0]).hex(),
             "right_hex": element_blob(pair[1]).hex()}
            for index, pair in enumerate(contexts, 1)]
    public = {"context_count": len(contexts), "contexts": rows,
              "named_uses": named, "named_use_count": len(named),
              "named_use_mapping_sha256": digest_obj(named),
              "context_rows_sha256": digest_obj(rows),
              "deduplication": "exact E4 pair equality"}
    return contexts, by_name, public


def independent_dp_failures(index: int,
                            correction_values: list[list[Element]],
                            base_values: list[Element], by_name: dict[str, int],
                            e4: Quotient) -> list[str]:
    def correction(name: str) -> Element:
        return correction_values[by_name[name]-1][index]

    def candidate(name: str) -> Element:
        context = by_name[name]-1
        return e4.mul(base_values[context], correction_values[context][index])

    coarse: list[str] = []
    first: list[str] = []
    second: list[str] = []
    for slot in range(5):
        if correction(f"correction_coface_{slot}") != e4.identity:
            coarse.append(f"correction_coarse_J_H_coface_{slot}")
        fxy = candidate(f"hexagon_1_fxy_{slot}")
        fxz = candidate(f"hexagon_1_fxz_{slot}")
        fyz = candidate(f"hexagon_1_fyz_{slot}")
        fux = candidate(f"hexagon_2_fux_{slot}")
        fxy2 = candidate(f"hexagon_2_fxy_{slot}")
        fuy = candidate(f"hexagon_2_fuy_{slot}")
        if q_paper_product(e4, [fxy, e4.inverse(fxz), fyz]) != e4.identity:
            first.append(f"hexagon_1_coface_{slot}")
        if q_paper_product(e4, [e4.inverse(fux), e4.inverse(fxy2), fuy]) != \
                e4.identity:
            second.append(f"hexagon_2_coface_{slot}")
    bad = coarse + first + second
    parts = [candidate(f"pentagon_part_{i}") for i in range(5)]
    pent = q_paper_product(
        e4, [e4.inverse(q_paper_product(e4, [parts[4], parts[2]])),
             parts[1], parts[3], parts[0]])
    if pent != e4.identity:
        bad.append("ordered_A18_pentagon")
    g = e4.generators
    ff = candidate("source_ff")
    gv = candidate("source_g")
    gs = candidate("source_gs")
    f1234 = candidate("source_f1234")
    h = candidate("source_h")
    middle = candidate("source_middle")
    source = [
        g[0], q_product(e4, [e4.inverse(gv), g[1], gv]),
        q_product(e4, [e4.inverse(ff), e4.inverse(h), g[2], h, ff]),
        q_product(e4, [e4.inverse(ff), g[3], ff]),
        q_product(e4, [e4.inverse(ff), e4.inverse(middle), e4.inverse(gs),
                       g[4], gs, middle, ff]),
        q_product(e4, [e4.inverse(f1234), g[5], f1234]),
    ]
    for relator_index, relation in enumerate(pure_relations(4), 1):
        if e4.eval(relation, source) != e4.identity:
            bad.append(f"S_relation_{relator_index}")
    return bad


def rebuild_fixed_context_dp(dictionary: dict[str, Any], e4: Quotient) \
        -> tuple[dict[str, Any], list[list[str]]]:
    contexts, by_name, context_public = independent_context_registry(e4)
    seeds = dictionary["seed_words"]
    signed = [(index+1, word) for index, word in enumerate(seeds)] + [
        (-(index+1), inv_word(word)) for index, word in enumerate(seeds)]
    seed_images: list[dict[int, Element]] = []
    seed_digest = hashlib.sha256()
    for context_index, pair in enumerate(contexts, 1):
        row: dict[int, Element] = {}
        for edge, word in signed:
            value = e4.eval(word, list(pair))
            row[edge] = value
            seed_digest.update(context_index.to_bytes(2, "little"))
            seed_digest.update(edge.to_bytes(2, "little", signed=True))
            seed_digest.update(element_blob(value))
        seed_images.append(row)
    correction_values: list[list[Element]] = []
    propagated = hashlib.sha256()
    for context_index in range(len(contexts)):
        values = [e4.identity]
        propagated.update(element_blob(e4.identity))
        for word_index in range(1, dictionary["count"]):
            parent = dictionary["parent_indices"][word_index]-1
            edge = dictionary["signed_seed_edges"][word_index]
            require(0 <= parent < word_index and edge in seed_images[context_index],
                    "independent DP parent/edge")
            value = e4.mul(values[parent], seed_images[context_index][edge])
            values.append(value)
            propagated.update(element_blob(value))
        correction_values.append(values)
    base_values = [e4.eval(FIXED_WORD, list(pair)) for pair in contexts]
    failures: list[list[str]] = []
    survivors: list[int] = []
    gate_names = [f"correction_coarse_J_H_coface_{i}" for i in range(5)] + \
        [f"hexagon_1_coface_{i}" for i in range(5)] + \
        [f"hexagon_2_coface_{i}" for i in range(5)] + \
        ["ordered_A18_pentagon"] + [f"S_relation_{i}" for i in range(1, 12)]
    gate_bits = {name: bytearray((dictionary["count"]+7)//8)
                 for name in gate_names}
    gate_counts = {name: 0 for name in gate_names}
    evaluated_prefix = hashlib.sha256()
    survivor_prefix = hashlib.sha256()
    for index in range(dictionary["count"]):
        bad = independent_dp_failures(index, correction_values, base_values,
                                      by_name, e4)
        failures.append(bad)
        if not bad:
            survivors.append(index+1)
            survivor_prefix.update((index+1).to_bytes(4, "little"))
        evaluated_prefix.update(canonical_bytes([index+1, bad]) + b"\n")
        for name in bad:
            gate_bits[name][index//8] |= 1 << (index % 8)
            gate_counts[name] += 1
    bitsets = []
    for name in gate_names:
        raw = bytes(gate_bits[name])
        bitsets.append({"gate": name, "failure_count": gate_counts[name],
                        "byte_length": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest(),
                        "base64": base64.b64encode(raw).decode("ascii")})
    semantic = {
        "complete": True, "evaluated": dictionary["count"],
        "current_candidate": None, "contexts": context_public,
        "signed_seed_count": len(signed),
        "signed_seed_images_sha256": seed_digest.hexdigest(),
        "propagated_correction_values_sha256": propagated.hexdigest(),
        "recurrence": "rho(c_i)=rho(c_parent)*rho(signed_seed)",
        "free_reduction_value_invariant": True,
        "failure_bitsets": bitsets,
        "failure_lists_sha256": digest_obj([[i+1, row]
                                             for i, row in enumerate(failures)]),
        "survivor_count": len(survivors), "survivor_indices": survivors,
        "survivor_indices_sha256": digest_obj(survivors),
        "evaluated_prefix_sha256": evaluated_prefix.hexdigest(),
        "survivor_prefix_sha256": survivor_prefix.hexdigest(),
        "per_gate_failure_counts": gate_counts,
        "direct_word_replay_required_for_full_lane": True,
    }
    return semantic, failures


def two_sided_residuals(source: Sequence[Sequence[int]],
                        inverse: Sequence[Sequence[int]]) \
        -> tuple[list[list[int]], list[list[int]]]:
    st = [reduce_word(substitute(inverse[i], source)+[-(i+1)]) for i in range(6)]
    ts = [reduce_word(substitute(source[i], inverse)+[-(i+1)]) for i in range(6)]
    return st, ts


def rebuild_normalized_inverse_fibre(q3: dict[str, Any], e4: Quotient) \
        -> tuple[dict[str, Any], tuple[Element, ...], list[list[int]]]:
    block = q3["canonical_roof_powers"]
    rows = block["rows"]
    require([row["exponent"] for row in rows] == [1, 2, 4, 5, 7, 8] and
            block["canonicalized_each_step"] is True and
            block["literal_power_words_retained"] is False,
            "normalized q3 power receipt")
    row7s = [row for row in rows if row["exponent"] == 7]
    row2s = [row for row in rows if row["exponent"] == 2]
    require(len(row7s) == len(row2s) == 1, "normalized exponent-two/seven rows")
    row7 = row7s[0]
    correction = q3["correction_fibre"]
    records = correction["records"]
    require(len(records) == 27 and correction["certificate"]["order"] == 27 and
            correction["certificate"]["enumerated_count"] == 27 and
            correction["certificate"]["all_words_coarse_identity"] is True,
            "normalized inverse correction fibre")
    selected_q3 = q3["selected_solution"]
    selected_index = selected_q3["correction_index"]
    require(selected_q3["exponent"] == 2 and 1 <= selected_index <= 27 and
            reduce_word(row2s[0]["word"] + records[selected_index-1]["word"]) ==
            FIXED_WORD,
            "fixed exponent-two tuple/canonical fibre binding")
    base_source = source_words(FIXED_WORD)
    base_key = tuple(e4.eval(word) for word in base_source)
    tested: list[int] = []
    passing: list[int] = []
    candidates: dict[int, tuple[list[int], list[list[int]]]] = {}
    for index, record in enumerate(records, 1):
        candidate = reduce_word(row7["word"] + record["word"])
        inverse = source_words(candidate)
        st, ts = two_sided_residuals(base_source, inverse)
        tested.append(index)
        if all(e4.eval(word) == e4.identity for word in st+ts):
            passing.append(index)
            candidates[index] = (candidate, inverse)
    require(tested == list(range(1, 28)) and passing,
            "normalized exponent-seven fibre has no E4 two-sided inverse")
    selected = passing[0]
    selected_candidate, selected_inverse = candidates[selected]
    maximum = max(map(len, selected_inverse))
    require(maximum <= CAPS["single_word_or_section_length"],
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
        "max_inverse_word_length": maximum,
        "raw_endomorphism_powering_used": False,
        "componentwise_Q4_Pi4_inverse_words_combined": False,
    }
    return public, base_key, selected_inverse


def rebuild_inverse(f: Sequence[int], e4: Quotient,
                    claimed: dict[str, Any], normalized: dict[str, Any],
                    base_key: tuple[Element, ...]) -> dict[str, Any]:
    source = source_words(f)
    require(tuple(e4.eval(word) for word in source) == base_key,
            "selected candidate lacks the bounded normalized inverse key")
    inverse = normalized["selected_inverse_words"]
    st, ts = two_sided_residuals(source, inverse)
    expected = {
        "normalized_exponent": 7,
        "normalized_roof_order": 9,
        "source_words": source,
        "inverse_words": inverse,
        "ST_residuals": st,
        "TS_residuals": ts,
        "construction": "finite normalized exponent-seven inverse from the pinned complete 27-fibre",
        "max_inverse_word_length": max(map(len, inverse)),
        "cache_hit": True,
        "cache_key_exact_six_E4_images": True,
        "cache_hit_two_sided_replay_in_E4": True,
        "candidate_acceptance_or_certificate_reused": False,
        "componentwise_Q4_Pi4_inverse_words_combined": False,
        "normalized_fibre_selected_correction_index":
            normalized["selected_correction_index"],
        "normalized_fibre_passing_indices": normalized["passing_indices"],
    }
    require(claimed == expected and
            all(e4.eval(word) == e4.identity for word in st+ts),
            "finite normalized inverse receipt")
    return expected


def expected_targets(selected: dict[str, Any], e4: Quotient,
                     normalized: dict[str, Any],
                     base_key: tuple[Element, ...]) \
        -> list[tuple[str, str, list[int]]]:
    f, correction = selected["selected_word"], selected["correction_word"]
    require(f == reduce_word(FIXED_WORD+correction), "selected word/correction")
    replay_derived_ledger(f, selected["derived_witness"])
    error = reduce_word(f+inv_word(selected["derived_witness"]["expanded_word"]))
    require(selected["charming_error_word"] == error, "charming error word")
    c34 = cofaces(3)
    coarse_jh = [substitute(embed_f2(correction), mapping) for mapping in c34]
    require(selected["correction_coarse_J_H_coface_words"] == coarse_jh and
            selected["correction_coarse_J_H_all_five"] is True and
            selected["correction_coarse_J_H_all_five_replayed"] is True and
            selected["correction_in_finer_J_Phi_required"] is False and
            selected["correction_finer_J_Phi_membership_not_required"] is True and
            selected["correction_J_Phi_coset_is_lift_freedom"] is True and
            "kernel" in selected["J_H_definition"] and
            "intersection" in selected["J_Phi_definition"] and
            selected["J_Phi_not_identified_with_Phi3_H3"] is True and
            all(e4.eval(word) == e4.identity for word in coarse_jh),
            "coarse J_H correction/finer J_Phi lift freedom")
    charm = [substitute(embed_f2(error), mapping) for mapping in c34]
    hexes = hexagon_words(f)
    require(selected["hexagon_words_F2"] == hexes and
            selected["pentagon_word_PB4"] == pentagon_word(f),
            "selected literal words")
    targets: list[tuple[str, str, list[int]]] = []
    targets += [(f"charming_error_coface_{i}", "charming", word)
                for i, word in enumerate(charm)]
    for hindex, h in enumerate(hexes, 1):
        for slot, mapping in enumerate(c34):
            targets.append((f"hexagon_{hindex}_coface_{slot}", "hexagon",
                            substitute(embed_f2(h), mapping)))
    targets.append(("ordered_A18_pentagon", "pentagon", pentagon_word(f)))
    inverse = rebuild_inverse(f, e4, selected["inverse"], normalized, base_key)
    for index, relator in enumerate(pure_relations(4), 1):
        targets.append((f"S_relation_{index}", "endomorphism_relation",
                        substitute(relator, inverse["source_words"])))
        targets.append((f"T_relation_{index}", "endomorphism_relation",
                        substitute(relator, inverse["inverse_words"])))
    targets += [(f"ST_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(inverse["ST_residuals"])]
    targets += [(f"TS_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(inverse["TS_residuals"])]
    require(all(e4.eval(word) == e4.identity for _, _, word in targets),
            "expected target outside H4")
    return targets


def validate_registry(rows: Sequence[dict[str, Any]],
                      quotients: dict[int, Quotient]) \
        -> tuple[dict[int, Element], dict[tuple[int, Element], int]]:
    by_id: dict[int, Element] = {}
    reverse: dict[tuple[int, Element], int] = {}
    for expected_id, row in enumerate(rows, 1):
        require(set(row) == {"id", "rank", "section_word",
                             "coarse_permutation", "fine_pc_coords"} and
                row["id"] == expected_id and row["rank"] in quotients and
                isinstance(row["section_word"], list) and
                len(row["section_word"]) <= CAPS["single_word_or_section_length"],
                "element registry id/rank")
        quotient = quotients[row["rank"]]
        value = (row_perm(row["coarse_permutation"], quotient.degree),
                 quotient.collector.coord(row["fine_pc_coords"]))
        require(quotient.eval(row["section_word"]) == value,
                "element registry section")
        require((row["rank"], value) not in reverse, "duplicate registry element")
        by_id[expected_id] = value
        reverse[(row["rank"], value)] = expected_id
    return by_id, reverse


def validate_fox_models(block: dict[str, Any], e3: Quotient, e4: Quotient,
                        reverse: dict[tuple[int, Element], int]) \
        -> dict[int, list[Vector]]:
    models: dict[int, list[Vector]] = {}
    for name, rank, quotient in (("PB3", 3, e3), ("PB4", 4, e4)):
        row = block[name]
        require(row["rank"] == rank and row["field"] == 3 and
                row["generator_count"] == len(pairs(rank)) and
                row["relator_count"] == len(pure_relations(rank)) and
                row["D1D2_zero"] is True and
                row["full_regular_matrix_constructed"] is False and
                row["H1_basis_or_rank_constructed"] is False,
                f"{name} Fox metadata")
        require(row["identity_element_id"] == reverse[(rank, quotient.identity)] and
                row["marked_element_ids"] ==
                [reverse[(rank, x)] for x in quotient.generators],
                f"{name} marked registry")
        convention = row["left_fox_convention"]
        require(convention == {
            "product_rule": "d(uv)=d(u)+u*d(v)",
            "positive_letter": "+prefix",
            "negative_letter": "advance prefix by x_i^-1, then -prefix",
            "D1": "sum_i coefficient*(q(x_i)-1) on the right",
            "translated_column": "left multiplication by the translation element",
        }, f"{name} Fox convention")
        columns: list[Vector] = []
        for index, (relator, claimed) in enumerate(
                zip(pure_relations(rank), row["relator_columns"]), 1):
            gradient, value = fox(relator, quotient)
            require(value == quotient.identity and boundary1(gradient, quotient) == {},
                    f"{name} D1D2 reconstruction")
            require(claimed["relator_index"] == index and claimed["word"] == relator and
                    claimed["quotient_identity"] is True and
                    claimed["D1_of_gradient_zero"] is True and
                    claimed["gradient"] == encode(gradient, rank, reverse),
                    f"{name} relator column {index}")
            columns.append(gradient)
        models[rank] = columns
    require(block["PB5"] == {"constructed": False,
                              "reason": "direct B3/B4 literal pair certified first"},
            "PB5 positive-first bypass")
    return models


def _decode_packed_array(block: dict[str, Any], expected_type: str,
                         typecode: str, cap: int) -> Sequence[int]:
    require(set(block) == {"type", "array_typecode", "endianness", "length",
                           "itemsize", "byte_length", "cap", "sha256", "base64"} and
            block["type"] == expected_type and
            block["array_typecode"] == typecode and
            block["endianness"] == "little" and block["cap"] == cap and
            isinstance(block["length"], int) and 0 <= block["length"] <= cap and
            isinstance(block["base64"], str), "packed array schema")
    try:
        raw = base64.b64decode(block["base64"], validate=True)
    except Exception as exc:
        raise Reject("packed array base64") from exc
    require(base64.b64encode(raw).decode("ascii") == block["base64"] and
            hashlib.sha256(raw).hexdigest() == block["sha256"] and
            block["byte_length"] == len(raw), "packed array bytes/SHA")
    if typecode == "B":
        require(block["itemsize"] == 1 and len(raw) == block["length"],
                "packed uint8 length")
        return raw
    values = array(typecode)
    require(block["itemsize"] == values.itemsize and
            len(raw) == block["length"]*values.itemsize,
            "packed integer byte length")
    values.frombytes(raw)
    if sys.byteorder != "little":
        values.byteswap()
    return values


def evaluate_proof_dag(block: dict[str, Any], expected_names: Sequence[str],
                       leaf_resolver: Any) \
        -> tuple[dict[str, Vector], dict[str, int]]:
    expected_keys = {
        "format", "field", "node_order", "translation_action", "arrays",
        "roots", "node_count", "edge_count", "leaf_count",
        "combination_node_count", "all_serialized_nodes_reachable_from_roots",
        "unreachable_search_nodes_pruned", "expanded_boundary_ledgers_serialized",
        "packed_manifest_sha256",
    }
    require(set(block) == expected_keys and
            block["format"] == "packed-parallel-arrays/v1" and
            block["field"] == 3 and
            block["node_order"] == "one_based_topological" and
            block["translation_action"] == "left" and
            isinstance(block["node_count"], int) and
            1 <= block["node_count"] <= CAPS["provenance_dag_nodes"] and
            isinstance(block["edge_count"], int) and
            0 <= block["edge_count"] <= CAPS["provenance_dag_edges"] and
            isinstance(block["unreachable_search_nodes_pruned"], int) and
            block["unreachable_search_nodes_pruned"] >= 0 and
            block["all_serialized_nodes_reachable_from_roots"] is True and
            block["expanded_boundary_ledgers_serialized"] is False,
            "packed proof DAG header")
    arrays = block["arrays"]
    require(set(arrays) == {"node_kind", "leaf_relator_index",
                            "leaf_translation_element_id", "edge_offsets",
                            "edge_parent_node_id", "edge_coefficient"},
            "packed proof DAG arrays")
    n, e = block["node_count"], block["edge_count"]
    kinds = _decode_packed_array(arrays["node_kind"], "uint8", "B",
                                 CAPS["provenance_dag_nodes"])
    relators = _decode_packed_array(arrays["leaf_relator_index"], "uint16", "H",
                                    CAPS["provenance_dag_nodes"])
    translations = _decode_packed_array(
        arrays["leaf_translation_element_id"], "uint32", "I",
        CAPS["provenance_dag_nodes"])
    offsets = _decode_packed_array(arrays["edge_offsets"], "uint32", "I",
                                   CAPS["provenance_dag_nodes"]+1)
    edge_parents = _decode_packed_array(
        arrays["edge_parent_node_id"], "uint32", "I",
        CAPS["provenance_dag_edges"])
    edge_coefficients = _decode_packed_array(
        arrays["edge_coefficient"], "uint8", "B", CAPS["provenance_dag_edges"])
    require(len(kinds) == len(relators) == len(translations) == n and
            len(offsets) == n+1 and len(edge_parents) ==
            len(edge_coefficients) == e and offsets[0] == 0 and offsets[-1] == e and
            all(offsets[i] <= offsets[i+1] for i in range(n)),
            "packed proof DAG dimensions")
    manifest = {
        name: {key: value for key, value in row.items() if key != "base64"}
        for name, row in arrays.items()
    }
    require(block["packed_manifest_sha256"] ==
            digest_obj({"arrays": manifest, "roots": block["roots"]}),
            "packed proof DAG manifest")

    roots = block["roots"]
    require(isinstance(roots, list) and
            [row.get("name") for row in roots] == list(expected_names) and
            all(set(row) == {"name", "node_id"} and
                isinstance(row["node_id"], int) and 1 <= row["node_id"] <= n
                for row in roots), "packed proof DAG roots/order")
    root_ids = {row["name"]: row["node_id"] for row in roots}
    require(len(root_ids) == len(roots), "packed proof DAG duplicate root")

    # First structural pass: exact backward references and future-use counts.
    use_count = array("I", [0]) * (n+1)
    leaf_count = 0
    for index in range(n):
        node_id = index+1
        start, stop = int(offsets[index]), int(offsets[index+1])
        if kinds[index] == 1:
            require(start == stop and relators[index] >= 1 and
                    translations[index] >= 1, "packed proof DAG leaf fields")
            leaf_count += 1
        else:
            require(kinds[index] == 2 and relators[index] == 0 and
                    translations[index] == 0 and (stop > start or node_id == 1),
                    "packed proof DAG linear fields")
            seen: set[int] = set()
            for position in range(start, stop):
                parent = int(edge_parents[position])
                coefficient = int(edge_coefficients[position])
                require(1 <= parent < node_id and parent not in seen and
                        coefficient in (1, 2),
                        "packed proof DAG backward reference/coefficient")
                seen.add(parent)
                use_count[parent] += 1
    for node_id in root_ids.values():
        use_count[node_id] += 1
    require(block["leaf_count"] == leaf_count and
            block["combination_node_count"] == n-leaf_count,
            "packed proof DAG accounting")

    # Independent root reachability uses a byte bitmap, never a Python set of
    # millions of IDs.
    reached = bytearray(n+1)
    pending = array("I", root_ids.values())
    reached_count = 0
    while pending:
        node_id = int(pending.pop())
        if reached[node_id]:
            continue
        reached[node_id] = 1
        reached_count += 1
        start, stop = int(offsets[node_id-1]), int(offsets[node_id])
        pending.extend(int(edge_parents[position])
                       for position in range(start, stop))
    require(reached_count == n and all(reached[1:]),
            "packed proof DAG unreachable node")

    # Streaming topological replay.  A parent vector is released immediately
    # after its last edge use; only root holds survive to the end.
    live: dict[int, Vector] = {}
    live_entries = 0
    peak_live_entries = 0
    peak_live_nodes = 0
    replay_start = time.monotonic()
    last_progress = replay_start
    for index in range(n):
        node_id = index+1
        start, stop = int(offsets[index]), int(offsets[index+1])
        if kinds[index] == 1:
            vector = leaf_resolver({
                "relator_index": int(relators[index]),
                "translation_element_id": int(translations[index]),
                "translation_action": "left",
            })
        else:
            vector = {}
            for position in range(start, stop):
                parent = int(edge_parents[position])
                require(parent in live, "packed proof DAG released parent")
                add_scaled(vector, live[parent], int(edge_coefficients[position]))
            for position in range(start, stop):
                parent = int(edge_parents[position])
                require(use_count[parent] > 0, "packed proof DAG use count")
                use_count[parent] -= 1
                if use_count[parent] == 0:
                    live_entries -= len(live[parent])
                    del live[parent]
        require(use_count[node_id] > 0, "packed proof DAG unreferenced inserted node")
        live[node_id] = vector
        live_entries += len(vector)
        peak_live_entries = max(peak_live_entries, live_entries)
        peak_live_nodes = max(peak_live_nodes, len(live))
        now = time.monotonic()
        if (node_id & 4095) == 0 or now-last_progress >= \
                CAPS["progress_interval_seconds"]:
            rss = current_rss_bytes()
            require(rss == 0 or rss < CAPS["producer_soft_rss_bytes"],
                    "checker packed DAG RSS guard")
            print("D972_B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_CHECKER_PROGRESS "
                  f"phase=packed_DAG_replay elapsed={now-replay_start:.3f} "
                  f"nodes={node_id} live_nodes={len(live)} "
                  f"live_sparse_entries={live_entries} peak_live_nodes={peak_live_nodes} "
                  f"peak_live_sparse_entries={peak_live_entries} current_rss={rss}",
                  flush=True)
            last_progress = now
    require(all(node_id in live for node_id in root_ids.values()),
            "packed proof DAG root lifetime")
    result = {name: live[node_id] for name, node_id in root_ids.items()}
    require(peak_live_nodes <= n and peak_live_entries >= 0,
            "packed proof DAG streaming accounting")
    return result, root_ids


def validate_certificates(certificates: Sequence[dict[str, Any]],
                          dag_block: dict[str, Any],
                          targets: Sequence[tuple[str, str, list[int]]],
                          e4: Quotient, pb4_columns: Sequence[Vector],
                          by_id: dict[int, Element],
                          reverse: dict[tuple[int, Element], int]) -> set[int]:
    names = [x[0] for x in targets]
    require([x["name"] for x in certificates] == names,
            "boundary certificate order/names")
    referenced: set[int] = set()

    def resolve_leaf(node: dict[str, Any]) -> Vector:
        relator = node["relator_index"]
        translation_id = node["translation_element_id"]
        require(isinstance(relator, int) and 1 <= relator <= len(pb4_columns) and
                translation_id in by_id and
                reverse.get((4, by_id[translation_id])) == translation_id,
                "proof DAG leaf typing")
        referenced.add(translation_id)
        return translate(pb4_columns[relator-1], by_id[translation_id], e4)

    root_vectors, root_ids = evaluate_proof_dag(dag_block, names, resolve_leaf)
    certificate_keys = {
        "name", "kind", "arity", "word", "quotient_identity", "gradient",
        "proof_root_node_id", "proof_system", "gradient_sha256", "fox_membership",
    }
    for cert, (name, kind, word) in zip(certificates, targets):
        require(set(cert) == certificate_keys and
                cert["name"] == name and cert["kind"] == kind and
                cert["arity"] == 4 and cert["word"] == word and
                cert["quotient_identity"] is True and
                cert["proof_root_node_id"] == root_ids[name] and
                cert["proof_system"] == "shared_topological_F3_provenance_DAG",
                f"{name}: typed DAG certificate header")
        gradient, value = fox(word, e4)
        require(value == e4.identity and boundary1(gradient, e4) == {},
                f"{name}: Fox cycle")
        expected_gradient = encode(gradient, 4, reverse)
        require(cert["gradient"] == expected_gradient and
                cert["gradient_sha256"] == digest_obj(expected_gradient) and
                root_vectors[name] == gradient,
                f"{name}: DAG root/gradient")
    return referenced


def validate_terminal(data: dict[str, Any]) -> None:
    token = data.get("terminal_token")
    require(token in TERMINALS and data.get("status") == token, "terminal/status")
    if token == "B345_RELFRAT3_LITERAL_PAIR_PASS":
        require(data.get("claim_classification") == "positive_certificate",
                "positive claim classification")
        require(data["direct_lane"] == {"literal_pair_found": True,
                                        "PB5_branch_constructed": False,
                                        "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"},
                "positive direct lane")
        require(bool(data.get("selected_pair")) and
                bool(data.get("boundary_certificates")) and
                bool(data.get("boundary_proof_dag")),
                "positive without pair/certificates")
    elif token == "B345_RELFRAT3_SEARCH_INCOMPLETE":
        search = data["search"]
        require(data.get("claim_classification") == "unknown_not_obstruction" and
                data["direct_lane"]["literal_pair_found"] is False and
                data["direct_lane"]["PB5_branch_constructed"] is False and
                search["translates_per_relator"] ==
                CAPS["coefficient_translates_per_relator"] and
                search["candidate_resource_skips"] == [] and
                search["bounded_failure_is_not_nonexistence"] is True and
                search["nonpositive_result_is_obstruction"] is False and
                "no obstruction or nonexistence" in data["reason"],
                "bounded search terminal")
        require("selected_pair" not in data and
                "boundary_certificates" not in data and
                "boundary_proof_dag" not in data,
                "search miss promoted to a pair")
    elif token == "B345_RELFRAT3_UNKNOWN_RESOURCE":
        require(data.get("claim_classification") == "unknown_not_obstruction" and
                data["resource_stop"]["no_mathematical_obstruction_claimed"] is True and
                "selected_pair" not in data and
                "boundary_certificates" not in data and
                "boundary_proof_dag" not in data,
                "resource stop promotion")
        require(isinstance(data["resource_stop"].get("candidate_local"), bool) and
                data["resource_stop"]["cap"] == data["reason"],
                "resource stop exact reason")


def validate_resource_guards(data: dict[str, Any]) -> None:
    block = data["resource_guards"]
    require(set(block) == {
                "seconds", "minutes", "rss_bytes", "rss_gib",
                "external_job_limit_minutes", "safety_margin_minutes", "clock",
                "rss_primary", "rss_portable_fallback", "hit", "hit_reason",
                "last_checked_phase", "check_count", "current_rss_bytes",
                "peak_rss_bytes", "terminal_on_hit", "consulted_in_selftest",
            } and
            block["seconds"] == CAPS["producer_soft_timeout_seconds"] == 18_000 and
            block["minutes"] == 300 and
            block["rss_bytes"] == CAPS["producer_soft_rss_bytes"] and
            block["rss_gib"] == 4.5 and
            block["external_job_limit_minutes"] == 330 and
            block["safety_margin_minutes"] == 30 and
            block["clock"] == "time.monotonic" and
            block["rss_primary"] == "/proc/self/status VmRSS" and
            isinstance(block["rss_portable_fallback"], str) and
            isinstance(block["hit"], bool) and
            (block["hit_reason"] is None or
             isinstance(block["hit_reason"], str) and block["hit_reason"]) and
            isinstance(block["last_checked_phase"], str) and
            block["last_checked_phase"] and
            isinstance(block["check_count"], int) and block["check_count"] >= 0 and
            isinstance(block["current_rss_bytes"], int) and
            isinstance(block["peak_rss_bytes"], int) and
            0 <= block["current_rss_bytes"] <= block["peak_rss_bytes"] and
            block["terminal_on_hit"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and
            block["consulted_in_selftest"] is False,
            "resource guard contract")
    actual_stop = data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE"
    require(block["hit"] is actual_stop and
            (not actual_stop and block["hit_reason"] is None or
             actual_stop and block["hit_reason"] == data["resource_stop"]["cap"]),
            "resource guard hit/terminal equivalence")


def validate_lru_accounting(row: dict[str, Any], capacity: int) -> None:
    require(set(row) == {"capacity", "size", "peak", "hits", "misses",
                         "evictions", "clears"} and row["capacity"] == capacity and
            all(isinstance(row[key], int) and row[key] >= 0
                for key in ("size", "peak", "hits", "misses", "evictions",
                            "clears")) and
            row["size"] <= row["peak"] <= capacity,
            "bounded LRU accounting")


def _validate_receipt_v3_reference(data: dict[str, Any], q3: dict[str, Any],
                                   q3_path: Path, repo: Path) -> None:
    required_top = {"schema", "status", "terminal_token", "reason", "pins",
                    "source_hashes", "input_q3_terminal", "output_path", "caps",
                    "representation_contract", "claim_classification",
                    "theorem_boundary", "prohibited_work", "resource_guards",
                    "performance"}
    optional_top = {"formula_sha256", "relevant_formula",
                    "relevant_formula_sha256", "matched_quotients",
                    "base_q3_replay", "correction_dictionary",
                    "normalized_inverse_fibre", "search", "direct_lane",
                    "resource_stop", "resource_accounting_at_stop",
                    "quotient_element_registry", "fox_models",
                    "boundary_proof_dag", "selected_pair",
                    "boundary_certificates", "literal_replay"}
    require(required_top <= set(data) and set(data) <= required_top | optional_top,
            "v3 top-level schema/key layout")
    require(data.get("schema") == SCHEMA and data.get("caps") == CAPS,
            "schema/caps")
    require(data["input_q3_terminal"] == q3.get("terminal_token") and
            data["output_path"] == str(OUTPUT_PATH).replace("\\", "/"),
            "input/output binding")
    validate_terminal(data)
    validate_resource_guards(data)
    pins = data["pins"]
    for key, path, sha in (("q3_producer", Q3_PRODUCER, Q3_PRODUCER_SHA),
                           ("q3_checker", Q3_CHECKER, Q3_CHECKER_SHA),
                           ("q3_driver", Q3_DRIVER, Q3_DRIVER_SHA)):
        require(pins[key] == {"path": str(path).replace("\\", "/"),
                              "sha256": sha} and digest_file(repo/path) == sha,
                f"pin {key}")
    require(pins["q3_artifact"] == {"path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                                    "sha256": Q3_ARTIFACT_SHA} and
            digest_file(q3_path) == Q3_ARTIFACT_SHA and
            pins["formula_sha256"] == FORMULA_SHA and
            digest_obj(q3["formulas"]) == FORMULA_SHA,
            "artifact/formula pins")
    semantic_v2 = pins["semantic_reference_v2"]
    require(semantic_v2 == {
                "producer": {"path": str(V2_PRODUCER).replace("\\", "/"),
                             "sha256": V2_PRODUCER_SHA},
                "checker": {"path": str(V2_CHECKER).replace("\\", "/"),
                            "sha256": V2_CHECKER_SHA},
                "driver": {"path": str(V2_DRIVER).replace("\\", "/"),
                           "sha256": V2_DRIVER_SHA},
                "role": "frozen v2 mathematics, universe, gates, and search order",
            } and digest_file(repo/V2_PRODUCER) == V2_PRODUCER_SHA and
            digest_file(repo/V2_CHECKER) == V2_CHECKER_SHA and
            digest_file(repo/V2_DRIVER) == V2_DRIVER_SHA,
            "frozen v2 semantic reference")
    semantic = pins["semantic_reference_v1"]
    require(semantic == {
                "producer": {"path": str(V1_PRODUCER).replace("\\", "/"),
                             "sha256": V1_PRODUCER_SHA},
                "checker": {"path": str(V1_CHECKER).replace("\\", "/"),
                            "sha256": V1_CHECKER_SHA},
                "driver": {"path": str(V1_DRIVER).replace("\\", "/"),
                           "sha256": V1_DRIVER_SHA},
                "role": "frozen semantic predicate and search-order reference",
            } and
            digest_file(repo/V1_PRODUCER) == V1_PRODUCER_SHA and
            digest_file(repo/V1_CHECKER) == V1_CHECKER_SHA and
            digest_file(repo/V1_DRIVER) == V1_DRIVER_SHA,
            "frozen v1 semantic reference")
    local_sources = {
        "producer_sha256": digest_file(repo/"search/d972_b345_relfrat3_v3.py"),
        "checker_sha256": digest_file(Path(__file__)),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v3.g"),
    }
    require(data["source_hashes"] == local_sources, "new source SHA binding")
    require(data["representation_contract"] == {
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
            }, "v3 representation contract")
    theorem = data["theorem_boundary"]
    require(theorem["Phi3_H4_isolation_required"] is False and
            set(theorem["not_covered"]) == {"nonabelian chief factors", "other primes",
                                              "deeper iteration", "uniform cofinal tower",
                                              "global B4-B"}, "theorem boundary")
    prohibited = data["prohibited_work"]
    require(prohibited == {"relative_ANUPQ_calls": 0,
                            "Reidemeister_Schreier": False,
                            "full_Elements": False,
                            "full_regular_matrices": False,
                            "full_H1_basis_or_rank": False}, "prohibited-work receipt")
    if data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and \
            data["resource_stop"].get("candidate_local") is False:
        stop = data["resource_stop"]
        require(stop.get("cap") in {
                    "producer_soft_timeout", "producer_soft_rss",
                    "single_word_or_section_length", "element_pool",
                    "compact_candidate_cache", "compact_candidate_sparse_entries",
                    "section_slp_nodes", "total_sparse_group_ring_keys",
                    "single_sparse_elimination_row", "target_elimination_support",
                    "sparse_pivot_rows", "provenance_dag_nodes",
                    "provenance_dag_edges",
                } and data["reason"] == stop["cap"] and
                stop.get("large_structures_released_before_write") is True and
                stop.get("no_mathematical_obstruction_claimed") is True,
                "global resource-only receipt")
        accounting = data["resource_accounting_at_stop"]
        require(set(accounting) >= {"live", "monitor", "candidate_cache_size",
                                   "candidate_sparse_entries"} and
                accounting["candidate_cache_size"] <=
                4_096 and
                accounting["candidate_sparse_entries"] <=
                1_000_000 and
                accounting["live"]["element_pool"] <= CAPS["element_pool"] and
                accounting["live"]["dag_nodes"] <= CAPS["provenance_dag_nodes"] and
                accounting["live"]["dag_edges"] <= CAPS["provenance_dag_edges"],
                "global resource accounting")
    if "search" not in data:
        stop = data["resource_stop"]
        require(data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and
                stop.get("candidate_local") is not True and
                stop.get("cap") in {
                    "producer_soft_timeout", "producer_soft_rss",
                    "single_word_or_section_length", "element_pool",
                    "compact_candidate_cache", "compact_candidate_sparse_entries",
                    "section_slp_nodes",
                    "total_sparse_group_ring_keys", "single_sparse_elimination_row",
                    "target_elimination_support", "sparse_pivot_rows",
                    "provenance_dag_nodes", "provenance_dag_edges",
                } and data["reason"] == stop["cap"] and
                stop.get("large_structures_released_before_write") is True and
                stop.get("no_mathematical_obstruction_claimed") is True,
                "global resource-only receipt")
        if "resource_accounting_at_stop" in data:
            accounting = data["resource_accounting_at_stop"]
            require(set(accounting) >= {"live", "monitor", "candidate_cache_size",
                                       "candidate_sparse_entries"} and
                    accounting["candidate_cache_size"] <=
                    4_096 and
                    accounting["candidate_sparse_entries"] <=
                    1_000_000 and
                    accounting["live"]["element_pool"] <= CAPS["element_pool"] and
                    accounting["live"]["dag_nodes"] <= CAPS["provenance_dag_nodes"] and
                    accounting["live"]["dag_edges"] <= CAPS["provenance_dag_edges"],
                    "resource-stop accounting")
        return
    formula = formula_subset()
    require(data.get("formula_sha256") == FORMULA_SHA and
            data.get("relevant_formula") == formula and
            data.get("relevant_formula_sha256") == digest_obj(formula),
            "relevant formula")
    e3, e4 = reconstruct(q3)
    matched = data["matched_quotients"]
    require(matched["E3"]["coarse_degree"] == e3.degree and
            matched["E4"]["coarse_degree"] == e4.degree and
            "kernel" in matched["J_H"]["definition"] and
            matched["J_Phi"]["identified_with_Phi3_H3"] is False and
            matched["J_Phi"]["correction_membership_required"] is False and
            matched["J_Phi"]["quotient_J_H_over_J_Phi_is_lift_freedom"] is True and
            "intersection" in matched["J_Phi"]["definition"],
            "matched J_H/J_Phi typing")
    validate_base_replay(data, q3, e3, e4)
    require(data["correction_dictionary"] == rebuild_dictionary(q3, e3),
            "correction dictionary/order")
    normalized_inverse, normalized_base_key, _ = \
        rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized_inverse,
            "normalized exponent-seven inverse fibre")
    # Frozen v2 accounting contract retained as a nonexecuting source-level
    # differential reference; v3's exact packed contract is checked below.
    if False and "search" in data:
        search = data["search"]
        survivor_indices = search["cheap_survivor_indices"]
        rejected_indices = [row["candidate_index"] for row in
                            search["cheap_rejected"]]
        prep_resource_indices = [row["candidate_index"] for row in
                                 search["candidate_resource_skips"]
                                 if row["phase"] == "cheap_candidate_preparation"]
        inverse_cache = search["quotient_inverse_cache"]
        missing_inverse_skips = [row for row in search["candidate_resource_skips"]
                                 if row["reason"] ==
                                 "missing_bounded_inverse_representative"]
        dag_accounting = search["provenance_DAG"]
        dag_accounting_keys = {
            "live_nodes", "live_edges", "peak_nodes", "peak_edges",
            "pivot_payload", "expanded_pivot_ledgers_stored",
            "failed_column_and_candidate_nodes_rolled_back",
            "positive_serialization",
        }
        if data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS":
            dag_accounting_keys |= {
                "serialized_reachable_nodes", "serialized_reachable_edges",
            }
        require(search["method"] ==
                "one shared incremental sparse Gaussian basis with immutable F3 provenance DAG" and
                set(dag_accounting) == dag_accounting_keys and
                search["basis_size"] == search["pivot_count"] and
                0 <= search["pivot_count"] <= CAPS["sparse_pivot_rows"] and
                0 <= search["live_sparse_vector_entries"] <=
                CAPS["total_sparse_group_ring_keys"] and
                0 <= search["max_pivot_vector_support"] <=
                CAPS["total_sparse_group_ring_keys"] and
                0 <= search["max_transient_vector_support"] <=
                CAPS["total_sparse_group_ring_keys"] and
                isinstance(search["elimination_operations"], int) and
                search["elimination_operations"] >= 0 and
                1 <= dag_accounting["live_nodes"] <=
                dag_accounting["peak_nodes"] <= CAPS["provenance_dag_nodes"] and
                0 <= dag_accounting["live_edges"] <=
                dag_accounting["peak_edges"] <= CAPS["provenance_dag_edges"] and
                dag_accounting["pivot_payload"] ==
                "one sparse vector plus one DAG node id" and
                dag_accounting["expanded_pivot_ledgers_stored"] is False and
                dag_accounting["failed_column_and_candidate_nodes_rolled_back"] is True and
                dag_accounting["positive_serialization"] ==
                "root-reachable union only" and
                "live_sparse_entries" not in search and
                "max_ledger_support" not in search and
                search["cheap_quotient_gates_precede_power_inverse"] is True and
                search["raw_power_inverse_removed"] is True and
                search["same_basis_reused_for_all_candidates"] is True and
                search["candidate_order"] ==
                "empty first, then registered correction dictionary order" and
                search["cheap_candidates_evaluated"] ==
                data["correction_dictionary"]["count"] and
                search["cheap_gate_evaluation"] ==
                "direct E4 values without substituted-word materialization" and
                search["full_words_materialized_only_for_cheap_survivors"] is True and
                survivor_indices == sorted(set(survivor_indices)) and
                rejected_indices == sorted(set(rejected_indices)) and
                prep_resource_indices == sorted(set(prep_resource_indices)) and
                set(survivor_indices).isdisjoint(rejected_indices) and
                set(survivor_indices).isdisjoint(prep_resource_indices) and
                set(rejected_indices).isdisjoint(prep_resource_indices) and
                set(survivor_indices + rejected_indices + prep_resource_indices) ==
                set(range(1, data["correction_dictionary"]["count"]+1)) and
                search["all_cheap_survivors_scheduled_from_checkpoint"] == 8 and
                all(x > 0 and (x & (x-1)) == 0
                    for x in search["geometric_translation_checkpoints"]) and
                search["settled_automorphism_order_cache_size"] == 1 and
                inverse_cache == {
                    "key": "exact ordered tuple of six E4 source images",
                    "entries": 1,
                    "hits": inverse_cache["hits"],
                    "misses": inverse_cache["misses"],
                    "tuple_match_count": inverse_cache["hits"],
                    "tuple_mismatch_count": inverse_cache["misses"],
                    "max_inverse_word_length":
                        normalized_inverse["max_inverse_word_length"],
                    "cached_datum": "one pinned normalized exponent-seven full inverse word tuple",
                    "cache_hit_replays_current_ST_TS_in_E4": True,
                    "different_tuple_is_candidate_local_UNKNOWN": True,
                    "raw_endomorphism_powering_fallback": False,
                    "candidate_relations_gradients_proof_roots_reused": False,
                    "componentwise_Q4_Pi4_inverse_words_combined": False,
                } and
                isinstance(inverse_cache["hits"], int) and
                isinstance(inverse_cache["misses"], int) and
                inverse_cache["hits"] >= 0 and inverse_cache["misses"] >= 0 and
                inverse_cache["misses"] == len(missing_inverse_skips) and
                search["nonpositive_result_is_obstruction"] is False,
                "search cache/performance contract")
    if "search" in data:
        search = data["search"]
        survivor_indices = search["cheap_survivor_indices"]
        rejected_indices = [row["candidate_index"] for row in search["cheap_rejected"]]
        prep_resource_indices = [row["candidate_index"] for row in
                                 search["candidate_resource_skips"]
                                 if row["phase"] == "cheap_candidate_preparation"]
        require(survivor_indices == sorted(set(survivor_indices)) and
                rejected_indices == sorted(set(rejected_indices)) and
                prep_resource_indices == sorted(set(prep_resource_indices)) and
                set(survivor_indices).isdisjoint(rejected_indices) and
                set(survivor_indices).isdisjoint(prep_resource_indices) and
                set(rejected_indices).isdisjoint(prep_resource_indices) and
                set(survivor_indices + rejected_indices + prep_resource_indices) ==
                set(range(1, data["correction_dictionary"]["count"]+1)),
                "packed cheap candidate partition/order")
        dag_accounting = search["provenance_DAG"]
        expected_dag_keys = {
            "live_nodes", "live_edges", "peak_nodes", "peak_edges",
            "packed_arrays", "node_payload_bytes", "edge_payload_bytes",
            "pivot_payload", "expanded_pivot_ledgers_stored",
            "failed_column_and_candidate_nodes_rolled_back", "positive_serialization",
        }
        if data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS":
            expected_dag_keys |= {"serialized_reachable_nodes",
                                  "serialized_reachable_edges"}
        require(set(dag_accounting) == expected_dag_keys and
                dag_accounting["packed_arrays"] is True and
                1 <= dag_accounting["live_nodes"] <= dag_accounting["peak_nodes"] <=
                CAPS["provenance_dag_nodes"] and
                0 <= dag_accounting["live_edges"] <= dag_accounting["peak_edges"] <=
                CAPS["provenance_dag_edges"] and
                dag_accounting["node_payload_bytes"] >= 0 and
                dag_accounting["edge_payload_bytes"] >= 0 and
                dag_accounting["pivot_payload"] ==
                "one packed sparse vector plus one packed DAG node id" and
                dag_accounting["expanded_pivot_ledgers_stored"] is False and
                dag_accounting["failed_column_and_candidate_nodes_rolled_back"] is True and
                dag_accounting["positive_serialization"] ==
                "root-reachable typed little-endian arrays only",
                "packed DAG accounting")
        element_pool = search["element_pool"]
        pool_integrity = search["element_pool_integrity"]
        require(element_pool["capacity"] == CAPS["element_pool"] and
                1 <= element_pool["size"] <= element_pool["peak"] <=
                CAPS["element_pool"] and
                element_pool["packed_width_bytes"] ==
                e4.degree+e4.collector.n and
                element_pool["packed_payload_bytes"] ==
                element_pool["size"]*element_pool["packed_width_bytes"] and
                isinstance(element_pool["hits"], int) and element_pool["hits"] >= 0 and
                isinstance(element_pool["misses"], int) and
                element_pool["misses"] >= element_pool["size"] and
                element_pool["exact_equality"] ==
                "canonical permutation bytes concatenated with PC-coordinate bytes" and
                element_pool["canonical_order"] ==
                "lexicographic canonical packed bytes, identical to EKey=(permutation,PC) tuple order" and
                element_pool["digest_used_as_equality"] is False,
                "exact element pool")
        for name, capacity in (("product_cache", CAPS["element_product_cache"]),
                               ("inverse_cache", CAPS["element_inverse_cache"])):
            row = element_pool[name]
            validate_lru_accounting(row, capacity)
        require(pool_integrity["size"] == pool_integrity["lookup_size"] ==
                element_pool["size"] and pool_integrity["all_unique"] is True and
                pool_integrity["fixed_width_bytes"] == element_pool["packed_width_bytes"] and
                isinstance(pool_integrity["ordered_canonical_payload_sha256"], str) and
                len(pool_integrity["ordered_canonical_payload_sha256"]) == 64 and
                all(ch in "0123456789abcdef" for ch in
                    pool_integrity["ordered_canonical_payload_sha256"]) and
                pool_integrity["digest_is_binding_only_not_equality"] is True and
                pool_integrity["exported_internal_IDs"] is False and
                pool_integrity["positive_external_IDs_are_mapped_by_quotient_element_registry"] is True,
                "element pool uniqueness/canonical encoding receipt")
        lazy = search["lazy_sections"]
        require(lazy["capacity"] == CAPS["section_slp_nodes"] and
                1 <= lazy["live_nodes"] <= lazy["peak_nodes"] <=
                CAPS["section_slp_nodes"] and
                search["translations_used"] <= lazy["bound_elements"] <=
                CAPS["coefficient_translates_per_relator"] and
                lazy["representation"] ==
                "parent element-section node plus signed generator letter",
                "lazy section accounting")
        pc = search["pc_caches"]
        require(pc["unbounded_full_token_word_cache"] is False and
                len(pc["collectors"]) == 2 and
                pc["hits"] == sum(row["hits"] for row in pc["collectors"]) and
                pc["misses"] == sum(row["misses"] for row in pc["collectors"]) and
                pc["evictions"] == sum(row["evictions"] for row in pc["collectors"]),
                "PC cache aggregate")
        for collector in pc["collectors"]:
            validate_lru_accounting(collector["pair_product"],
                                    CAPS["pc_pair_product_cache"])
            validate_lru_accounting(collector["inverse"],
                                    CAPS["pc_inverse_cache"])
            require(collector["unbounded_full_token_word_cache"] is False and
                    collector["policy"] ==
                    "bounded exact pair-product and inverse LRU; no full-word cache" and
                    collector["pair_product"]["capacity"] ==
                    CAPS["pc_pair_product_cache"] and
                    collector["inverse"]["capacity"] == CAPS["pc_inverse_cache"] and
                    0 <= collector["pair_product"]["size"] <=
                    collector["pair_product"]["peak"] <=
                    CAPS["pc_pair_product_cache"] and
                    0 <= collector["inverse"]["size"] <=
                    collector["inverse"]["peak"] <= CAPS["pc_inverse_cache"] and
                    collector["hits"] == collector["pair_product"]["hits"]+
                    collector["inverse"]["hits"] and
                    collector["misses"] == collector["pair_product"]["misses"]+
                    collector["inverse"]["misses"] and
                    collector["evictions"] == collector["pair_product"]["evictions"]+
                    collector["inverse"]["evictions"], "bounded PC collector")
        checkpoints: list[int] = []
        value = 1
        while value <= search["translations_used"]:
            checkpoints.append(value)
            value *= 2
        inverse_cache = search["quotient_inverse_cache"]
        missing_inverse_skips = [row for row in search["candidate_resource_skips"]
                                 if row["reason"] ==
                                 "missing_bounded_inverse_representative"]
        require(search["method"] ==
                "one shared incremental sparse Gaussian basis with packed exact IDs and packed provenance DAG" and
                search["translation_order"] == "BFS shortlex steps +1..+6,-1..-6" and
                search["pivot_order"] ==
                "component then canonical EKey bytes (v2 exact order), never insertion ID" and
                1 <= search["translations_used"] <=
                CAPS["coefficient_translates_per_relator"] and
                search["translates_per_relator"] == search["translations_used"] and
                search["columns_seen"] == 11*search["translations_used"] and
                search["basis_size"] == search["pivot_count"] and
                0 <= search["pivot_count"] <= CAPS["sparse_pivot_rows"] and
                0 <= search["live_sparse_vector_entries"] <=
                CAPS["total_sparse_group_ring_keys"] and
                search["same_basis_reused_for_all_candidates"] is True and
                search["candidate_order"] ==
                "empty first, then registered correction dictionary order" and
                search["cheap_candidates_evaluated"] == 4096 and
                search["cheap_gate_evaluation"] ==
                "direct E4 values without substituted-word retention" and
                search["full_words_materialized_only_transiently_for_cheap_survivors"] is True and
                search["candidate_section_maps_retained"] is False and
                search["compact_candidate_cache_size"] <=
                search["compact_candidate_cache_cap"] == 4_096 and
                search["compact_candidate_sparse_entries"] <=
                search["compact_candidate_sparse_entries_cap"] ==
                1_000_000 and
                search["compact_candidate_cache_payload"] ==
                "names,kinds,packed gradients,quotient value IDs,correction index" and
                isinstance(search["selected_candidate_regenerated_and_exactly_compared"], bool) and
                (data["terminal_token"] != "B345_RELFRAT3_LITERAL_PAIR_PASS" or
                 search["selected_candidate_regenerated_and_exactly_compared"] is True) and
                search["geometric_translation_checkpoints"] == checkpoints and
                search["all_cheap_survivors_scheduled_from_checkpoint"] == 8 and
                search["settled_automorphism_order_cache_size"] == 1 and
                inverse_cache["key"] ==
                "exact ordered tuple of six stable E4 element IDs" and
                inverse_cache["entries"] == inverse_cache["capacity"] == 1 and
                inverse_cache["tuple_match_count"] == inverse_cache["hits"] and
                inverse_cache["tuple_mismatch_count"] == inverse_cache["misses"] and
                inverse_cache["misses"] == len(missing_inverse_skips) and
                inverse_cache["max_inverse_word_length"] ==
                normalized_inverse["max_inverse_word_length"] and
                inverse_cache["raw_endomorphism_powering_fallback"] is False and
                search["cheap_quotient_gates_precede_power_inverse"] is True and
                search["raw_power_inverse_removed"] is True and
                search["bounded_failure_is_not_nonexistence"] is True and
                search["nonpositive_result_is_obstruction"] is False,
                "packed search/cache contract")

    if data["terminal_token"] != "B345_RELFRAT3_LITERAL_PAIR_PASS":
        require("serialized_reachable_nodes" not in
                data["search"]["provenance_DAG"] and
                "serialized_reachable_edges" not in
                data["search"]["provenance_DAG"],
                "nonpositive serialized proof DAG")
        return
    require(data["search"]["provenance_DAG"]["serialized_reachable_nodes"] ==
            data["boundary_proof_dag"]["node_count"] and
            data["search"]["provenance_DAG"]["serialized_reachable_edges"] ==
            data["boundary_proof_dag"]["edge_count"],
            "serialized proof DAG accounting")
    selected = data["selected_pair"]
    dictionary = data["correction_dictionary"]
    index = selected["correction_index"]
    require(1 <= index <= len(dictionary["words"]) and
            selected["correction_word"] == dictionary["words"][index-1] and
            index in data["search"]["cheap_survivor_indices"] and
            index not in {row["candidate_index"] for row in
                          data["search"]["full_quotient_rejected"]} and
            index not in {row["candidate_index"] for row in
                          data["search"]["candidate_resource_skips"]},
            "selected correction/order")
    targets = expected_targets(selected, e4, normalized_inverse,
                               normalized_base_key)
    require(selected["boundary_certificate_names"] == [x[0] for x in targets] and
            all(selected[x] is True for x in
                ("correction_coarse_J_H_all_five_replayed",
                 "correction_finer_J_Phi_membership_not_required",
                 "all_ten_hexagon_coface_memberships_certified",
                 "ordered_A18_pentagon_certified",
                 "S_and_T_relations_certified",
                 "ST_and_TS_generator_compositions_certified")),
            "selected completeness flags")
    by_id, reverse = validate_registry(data["quotient_element_registry"], {3: e3, 4: e4})
    models = validate_fox_models(data["fox_models"], e3, e4, reverse)
    validate_certificates(data["boundary_certificates"],
                          data["boundary_proof_dag"], targets, e4,
                          models[4], by_id, reverse)
    replay = data["literal_replay"]
    require(replay["correction_lift_freedom"] == {
                "coarse_J_H_all_five_cofaces_identity": True,
                "finer_J_Phi_membership_required": False,
                "J_H_mod_J_Phi_coset_is_varied": True,
            } and
            replay["hexagon"]["each_checked_in_all_five_cofaces"] is True and
            replay["pentagon"]["ordered_five_coface_A18_direct_PB4_residual"] is True and
            replay["charming"]["explicit_commutator_product"] is True and
            replay["charming"]["raw_exponent_sums_used_as_criterion"] is False and
            replay["onto"]["two_sided_inverse_on_six_marked_generators"] is True,
            "literal replay flags")


def require_sha256(value: Any, label: str) -> None:
    require(isinstance(value, str) and len(value) == 64 and
            all(ch in "0123456789abcdef" for ch in value), label)


def independent_gradient_binding(name: str, kind: str, gradient: Vector,
                                 value: Element) -> dict[str, Any]:
    digest = hashlib.sha256()
    for (component, element), coefficient in sorted(gradient.items()):
        blob = element_blob(element)
        digest.update(component.to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
    return {"name": name, "kind": kind, "entry_count": len(gradient),
            "quotient_value_hex": element_blob(value).hex(),
            "canonical_gradient_sha256": digest.hexdigest(),
            "canonical_order": "component then exact canonical E4 bytes",
            "digest_is_binding_only_not_element_equality": True}


def validate_search_prefix(prefix: dict[str, Any],
                           failures: list[list[str]] | None,
                           dictionary_count: int | None) -> None:
    require(set(prefix) == {"cheap", "current", "blocker", "transaction",
                            "structural_cap", "accounting"},
            "bounded prefix keys")
    cheap = prefix["cheap"]
    require(set(cheap) == {"evaluated", "completed", "survivor_count",
                           "survivor_indices_sha256",
                           "evaluated_prefix_sha256", "survivor_prefix_sha256",
                           "current_candidate"} and
            isinstance(cheap["evaluated"], int) and 0 <= cheap["evaluated"] <= 4096 and
            isinstance(cheap["completed"], bool) and
            isinstance(cheap["survivor_count"], int) and
            0 <= cheap["survivor_count"] <= cheap["evaluated"],
            "bounded cheap prefix")
    for key in ("survivor_indices_sha256", "evaluated_prefix_sha256",
                "survivor_prefix_sha256"):
        require_sha256(cheap[key], f"cheap prefix {key}")
    expected_current = None if cheap["completed"] else cheap["evaluated"]+1
    require(cheap["current_candidate"] == expected_current and
            (not cheap["completed"] or dictionary_count is not None and
             cheap["evaluated"] == dictionary_count),
            "cheap evaluated/current prefix")
    if failures is not None:
        count = cheap["evaluated"]
        survivors = [index+1 for index, row in enumerate(failures[:count]) if not row]
        evaluated_digest = hashlib.sha256()
        survivor_digest = hashlib.sha256()
        for index, row in enumerate(failures[:count], 1):
            evaluated_digest.update(canonical_bytes([index, row])+b"\n")
            if not row:
                survivor_digest.update(index.to_bytes(4, "little"))
        require(cheap["survivor_count"] == len(survivors) and
                cheap["survivor_indices_sha256"] == digest_obj(survivors) and
                cheap["evaluated_prefix_sha256"] == evaluated_digest.hexdigest() and
                cheap["survivor_prefix_sha256"] == survivor_digest.hexdigest(),
                "independent cheap evaluated prefix")
    else:
        require(cheap["evaluated"] == cheap["survivor_count"] == 0 and
                cheap["survivor_indices_sha256"] == digest_obj([]) and
                cheap["evaluated_prefix_sha256"] == hashlib.sha256(b"").hexdigest() and
                cheap["survivor_prefix_sha256"] == hashlib.sha256(b"").hexdigest(),
                "pre-dictionary empty cheap prefix")
    current = prefix["current"]
    require(set(current) == {"checkpoint", "correction_index", "target_ordinal",
                             "target_name"} and
            (current["checkpoint"] is None or
             isinstance(current["checkpoint"], int) and current["checkpoint"] > 0) and
            (current["correction_index"] is None or
             isinstance(current["correction_index"], int) and
             1 <= current["correction_index"] <= 4096) and
            (current["target_ordinal"] is None or
             isinstance(current["target_ordinal"], int) and
             current["target_ordinal"] > 0) and
            (current["target_name"] is None or
             isinstance(current["target_name"], str) and current["target_name"]),
            "current candidate prefix")
    blocker = prefix["blocker"]
    require(set(blocker) == {"count", "sha256"} and
            isinstance(blocker["count"], int) and
            0 <= blocker["count"] <= CAPS["blocker_table"],
            "blocker prefix")
    require_sha256(blocker["sha256"], "blocker prefix SHA")
    transaction = prefix["transaction"]
    require(set(transaction) == {"starts", "commits", "rollbacks"} and
            all(isinstance(transaction[key], int) and transaction[key] >= 0
                for key in transaction) and
            transaction["commits"] <= 1 and
            transaction["rollbacks"] <= transaction["starts"],
            "transaction prefix")
    structural = prefix["structural_cap"]
    require(set(structural) == {"hit", "reason", "source"} and
            isinstance(structural["hit"], bool) and
            (not structural["hit"] and structural["reason"] is None and
             structural["source"] is None or
             structural["hit"] and isinstance(structural["reason"], str) and
             structural["reason"] and structural["source"] in
             {"monitor", "registered_structural_cap"}),
            "structural cap prefix")
    accounting = prefix["accounting"]
    require(set(accounting) == {"translations", "basis_pivots",
                                "basis_live_entries", "pool_size", "DAG_nodes",
                                "DAG_edges", "section_nodes", "PC_cache_hits",
                                "PC_cache_misses", "PC_cache_evictions"} and
            all(isinstance(value, int) and value >= 0
                for value in accounting.values()),
            "bounded accounting prefix")


def validate_blocker_trace(search: dict[str, Any], element_width: int) -> None:
    table = search["blocker_table"]
    history = search["blocker_history"]
    introductions = search["pivot_introductions"]
    trace = search["checkpoint_trace"]
    require(len(table) <= CAPS["blocker_table"] and
            len(trace) <= CAPS["transaction_trace_records"] and
            table == sorted(table, key=lambda row: row["candidate_index"]) and
            len({row["candidate_index"] for row in table}) == len(table) and
            search["blocker_table_sha256"] == digest_obj(table) and
            search["blocker_history_sha256"] == digest_obj(history) and
            search["checkpoint_trace_sha256"] == digest_obj(trace),
            "blocker table/history/trace bindings")
    by_history: dict[int, dict[str, Any]] = {}
    for expected_id, row in enumerate(history, 1):
        require(row["history_id"] == expected_id and
                1 <= row["candidate_index"] <= 4096 and
                row["target_ordinal"] >= 1 and
                isinstance(row["target_name"], str) and row["target_name"] and
                1 <= row["component"] <= 6,
                "blocker history row")
        raw_element = bytes.fromhex(row["element_hex"])
        require(len(raw_element) == element_width and
                all(isinstance(x, int) and x > row["failed_checkpoint"]
                    for x in row["skip_checkpoints"]+row["retry_checkpoints"]),
                "blocker checkpoint lists")
        by_history[expected_id] = row
    for intro in introductions:
        require(set(intro) == {"component", "element_hex", "translation_ordinal",
                               "relator_index"} and
                1 <= intro["component"] <= 6 and intro["translation_ordinal"] >= 1 and
                1 <= intro["relator_index"] <= 11 and
                any(row["component"] == intro["component"] and
                    row["element_hex"] == intro["element_hex"] for row in history),
                "watched pivot introduction")
    active: dict[int, dict[str, Any]] = {}
    for row in trace:
        require(isinstance(row.get("checkpoint"), int) and row["checkpoint"] >= 1 and
                1 <= row.get("candidate_index", 0) <= 4096,
                "checkpoint trace row")
        event = row["event"]
        if event == "missing_pivot":
            source = by_history[row["blocker_history_id"]]
            require(source["candidate_index"] == row["candidate_index"] and
                    source["failed_checkpoint"] == row["checkpoint"] and
                    source["target_ordinal"] == row["target_ordinal"] and
                    source["target_name"] == row["target_name"] and
                    source["component"] == row["component"] and
                    source["element_hex"] == row["element_hex"],
                    "missing-pivot trace/history")
            active[row["candidate_index"]] = source
        elif event == "missing_pivot_skip":
            source = active.get(row["candidate_index"])
            require(source is by_history[row["blocker_history_id"]] and
                    row["checkpoint"] in source["skip_checkpoints"] and
                    isinstance(row["pool_element_present"], bool) and
                    row["basis_pivot_present"] is False,
                    "missing-pivot skip theorem")
        elif event == "exact_pivot_retry":
            source = active.get(row["candidate_index"])
            intro = row["matching_introduction"]
            require(source is by_history[row["blocker_history_id"]] and
                    row["checkpoint"] in source["retry_checkpoints"] and
                    source.get("matching_introduction") == intro and
                    intro in introductions and
                    source["failed_checkpoint"] < intro["translation_ordinal"] <=
                    row["checkpoint"] and intro["component"] == source["component"] and
                    intro["element_hex"] == source["element_hex"],
                    "mandatory exact-pivot retry")
            del active[row["candidate_index"]]
        elif event in {"full_quotient_reject", "selected_commit",
                       "permanent_full_quotient_reject_skip"}:
            pass
        else:
            raise Reject(f"unknown checkpoint trace event: {event}")
    require([active[index] for index in sorted(active)] == table,
            "final blocker table replay")


def validate_transaction_search(data: dict[str, Any], search: dict[str, Any],
                                dictionary: dict[str, Any], e4: Quotient,
                                expected_dp: dict[str, Any],
                                dp_failures: list[list[str]],
                                normalized_inverse: dict[str, Any]) -> None:
    actual_dp = search["fixed_context_cheap_DP"]
    require(actual_dp == data["fixed_context_cheap_DP"], "cheap DP duplicate binding")
    semantic_actual = {key: value for key, value in actual_dp.items()
                       if key not in {"runtime_seconds", "PC_cache_delta"}}
    require(semantic_actual == expected_dp and
            isinstance(actual_dp["runtime_seconds"], (int, float)) and
            actual_dp["runtime_seconds"] >= 0 and
            set(actual_dp["PC_cache_delta"]) == {"hits", "misses", "evictions"} and
            all(isinstance(value, int) for value in actual_dp["PC_cache_delta"].values()),
            "independent fixed-context DP")
    require(search["cheap_survivor_indices"] == expected_dp["survivor_indices"] and
            search["cheap_candidates_evaluated"] == dictionary["count"] == 4096,
            "cheap survivor universe")
    comparisons = search["direct_vs_DP_comparisons"]
    require(search["direct_word_replay_count"] == len(comparisons) and
            search["direct_vs_DP_all_equal"] is True,
            "direct replay count")
    for row in comparisons:
        index = row["candidate_index"]
        correction = dictionary["words"][index-1]
        direct = direct_cheap_failures(reduce_word(FIXED_WORD+correction),
                                       correction, e4)
        require(row == {"checkpoint": row["checkpoint"],
                        "candidate_index": index,
                        "DP_failed_gates": dp_failures[index-1],
                        "direct_failed_gates": direct,
                        "equal": True} and
                row["checkpoint"] > 0 and
                (row["checkpoint"] & (row["checkpoint"]-1)) == 0 and
                direct == dp_failures[index-1],
                "direct-versus-DP replay")
    validate_blocker_trace(search, e4.degree+e4.collector.n)
    transaction = search["transaction"]
    require(search["transaction_contract"] == {
                "snapshot_before_complete_candidate_and_first_candidate_pool_intern": True,
                "pool_and_DAG_suffix_rollback": True,
                "element_ID_LRUs_cleared_before_ID_reuse": True,
                "persistent_basis_and_lazy_sections_immutable_during_candidate": True,
                "persistent_generator_and_inverse_tuple_anchors_replayed": True,
                "PC_collector_caches_store_canonical_coordinates_not_pool_IDs": True,
                "failed_candidate_gradients_retained": False,
            }, "transaction implementation contract")
    require(set(transaction) == {"starts", "commits", "rollbacks",
                                 "blocker_skips", "blocker_retries",
                                 "target_gradients_generated",
                                 "early_target_failures",
                                 "full_quotient_rejections",
                                 "max_transient_sparse_entries",
                                 "total_transient_sparse_entries"} and
            all(isinstance(value, int) and value >= 0
                for value in transaction.values()),
            "transaction accounting keys")
    outcomes = [row for row in search["checkpoint_trace"]
                if row["event"] in {"missing_pivot", "full_quotient_reject",
                                    "selected_commit"}]
    require([(row["checkpoint"], row["candidate_index"]) for row in comparisons] ==
            [(row["checkpoint"], row["candidate_index"]) for row in outcomes] and
            transaction["starts"] == len(outcomes) == len(comparisons) and
            transaction["rollbacks"] ==
            sum(row["event"] != "selected_commit" for row in outcomes) and
            transaction["commits"] ==
            sum(row["event"] == "selected_commit" for row in outcomes) and
            transaction["early_target_failures"] ==
            sum(row["event"] == "missing_pivot" for row in outcomes) and
            transaction["full_quotient_rejections"] ==
            len(search["full_quotient_rejected"]) and
            transaction["target_gradients_generated"] ==
            sum(row["target_gradients_generated"] for row in outcomes) and
            transaction["total_transient_sparse_entries"] ==
            sum(row["transient_sparse_entries"] for row in outcomes) and
            transaction["max_transient_sparse_entries"] ==
            max([0]+[row["peak_transient_sparse_entries"] for row in outcomes]) and
            transaction["blocker_skips"] ==
            sum(row["event"] == "missing_pivot_skip"
                for row in search["checkpoint_trace"]) and
            transaction["blocker_retries"] ==
            sum(row["event"] == "exact_pivot_retry"
                for row in search["checkpoint_trace"]) and
            transaction["max_transient_sparse_entries"] <=
            transaction["total_transient_sparse_entries"],
            "transaction trace totals")
    checkpoints: list[int] = []
    value = 1
    while value <= search["translations_used"]:
        checkpoints.append(value)
        value *= 2
    require(search["method"] ==
            "shared incremental sparse basis plus candidate-local transactional target streaming" and
            search["translation_order"] == "BFS shortlex steps +1..+6,-1..-6" and
            search["pivot_order"] ==
            "component then canonical EKey bytes (v2 exact order), never insertion ID" and
            search["candidate_order"] ==
            "checkpoint-major; registered correction order within each checkpoint" and
            search["geometric_translation_checkpoints"] == checkpoints and
            search["all_cheap_survivors_scheduled_from_checkpoint"] == 8 and
            search["persistent_candidate_cache_size"] == 0 and
            search["persistent_candidate_gradient_entries"] == 0 ==
            CAPS["persistent_candidate_gradient_entries"] and
            search["candidate_target_streaming"] is True and
            search["candidate_resource_skips"] == [] and
            search["candidate_local_resource_stop_is_global_UNKNOWN"] is True and
            search["same_basis_reused_for_all_candidates"] is True and
            search["columns_seen"] == 11*search["translations_used"] and
            search["basis_size"] == search["pivot_count"] and
            0 <= search["pivot_count"] <= CAPS["sparse_pivot_rows"] and
            0 <= search["live_sparse_vector_entries"] <=
            CAPS["total_sparse_group_ring_keys"] and
            search["selected_candidate_regenerated_and_exactly_compared"] is
            (data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS") and
            search["bounded_failure_is_not_nonexistence"] is True and
            search["nonpositive_result_is_obstruction"] is False,
            "transactional search contract")
    inverse = search["quotient_inverse_cache"]
    require(search["settled_automorphism_order_cache_size"] == 1 and
            inverse["key"] == "exact ordered tuple of six stable E4 element IDs" and
            inverse["entries"] == inverse["capacity"] == 1 and
            inverse["tuple_match_count"] == inverse["hits"] and
            inverse["tuple_mismatch_count"] == inverse["misses"] and
            inverse["max_inverse_word_length"] ==
            normalized_inverse["max_inverse_word_length"] and
            inverse["raw_endomorphism_powering_fallback"] is False,
            "normalized inverse cache")


def validate_receipt(data: dict[str, Any], q3: dict[str, Any], q3_path: Path,
                     repo: Path) -> None:
    required_top = {"schema", "status", "terminal_token", "reason", "pins",
                    "source_hashes", "input_q3_terminal", "output_path", "caps",
                    "representation_contract", "claim_classification",
                    "theorem_boundary", "prohibited_work", "resource_guards",
                    "performance", "bounded_search_prefix"}
    optional_top = {"formula_sha256", "relevant_formula",
                    "relevant_formula_sha256", "matched_quotients",
                    "base_q3_replay", "correction_dictionary",
                    "normalized_inverse_fibre", "fixed_context_cheap_DP",
                    "search", "direct_lane", "resource_stop",
                    "resource_accounting_at_stop", "quotient_element_registry",
                    "fox_models", "boundary_proof_dag", "selected_pair",
                    "boundary_certificates", "literal_replay", "blocker_table",
                    "blocker_history", "checkpoint_trace",
                    "direct_vs_DP_comparisons"}
    require(required_top <= set(data) and set(data) <= required_top | optional_top,
            "v4 top-level schema/key layout")
    require(data["schema"] == SCHEMA and data["caps"] == CAPS and
            data["input_q3_terminal"] == q3.get("terminal_token") and
            data["output_path"] == str(OUTPUT_PATH).replace("\\", "/"),
            "v4 schema/caps/input/output")
    validate_terminal(data)
    validate_resource_guards(data)
    pins = data["pins"]
    for key, path, sha in (("q3_producer", Q3_PRODUCER, Q3_PRODUCER_SHA),
                           ("q3_checker", Q3_CHECKER, Q3_CHECKER_SHA),
                           ("q3_driver", Q3_DRIVER, Q3_DRIVER_SHA)):
        require(pins[key] == {"path": str(path).replace("\\", "/"),
                              "sha256": sha} and digest_file(repo/path) == sha,
                f"pin {key}")
    require(pins["q3_artifact"] == {
                "path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                "sha256": Q3_ARTIFACT_SHA} and
            digest_file(q3_path) == Q3_ARTIFACT_SHA and
            pins["formula_sha256"] == FORMULA_SHA and
            digest_obj(q3["formulas"]) == FORMULA_SHA,
            "q3 artifact/formula pins")
    for key, producer, producer_sha, checker, checker_sha, driver, driver_sha, role in (
            ("semantic_reference_v3", V3_PRODUCER, V3_PRODUCER_SHA,
             V3_CHECKER, V3_CHECKER_SHA, V3_DRIVER, V3_DRIVER_SHA,
             "frozen packed-v3 semantics and positive-certificate reference"),
            ("semantic_reference_v2", V2_PRODUCER, V2_PRODUCER_SHA,
             V2_CHECKER, V2_CHECKER_SHA, V2_DRIVER, V2_DRIVER_SHA,
             "frozen v2 mathematics, universe, gates, and search order"),
            ("semantic_reference_v1", V1_PRODUCER, V1_PRODUCER_SHA,
             V1_CHECKER, V1_CHECKER_SHA, V1_DRIVER, V1_DRIVER_SHA,
             "frozen semantic predicate and search-order reference")):
        expected = {"producer": {"path": str(producer).replace("\\", "/"),
                                  "sha256": producer_sha},
                    "checker": {"path": str(checker).replace("\\", "/"),
                                 "sha256": checker_sha},
                    "driver": {"path": str(driver).replace("\\", "/"),
                                "sha256": driver_sha}, "role": role}
        require(pins[key] == expected and digest_file(repo/producer) == producer_sha and
                digest_file(repo/checker) == checker_sha and
                digest_file(repo/driver) == driver_sha, f"{key} pin")
    local_sources = {
        "producer_sha256": digest_file(repo/"search/d972_b345_relfrat3_v4.py"),
        "checker_sha256": digest_file(Path(__file__)),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v4.g"),
    }
    require(data["source_hashes"] == local_sources, "v4 source SHA binding")
    representation = data["representation_contract"]
    require(representation == {
                "version": "transactional-packed-v4",
                "persistent_element_equality": "exact canonical bytes; never a digest",
                "sparse_keys": "component plus stable zero-based exact element-pool ID",
                "pivot_order": "component then canonical EKey bytes; never insertion ID",
                "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
                "candidate_sections_retained": False,
                "candidate_gradients_retained_across_checkpoints": False,
                "candidate_transaction": "exact element-pool and provenance-DAG suffix rollback",
                "missing_pivot_blocker": "target ordinal, component, canonical E4 bytes",
                "proof_DAG_in_memory": "packed parallel arrays",
                "positive_DAG_serialization": "reachable union as typed little-endian base64 arrays",
                "cache_eviction_semantics": "capacity and eviction order affect speed only, never canonical values or search order",
                "persistent_checkpoint_resume": False,
            }, "v4 representation contract")
    require(data["prohibited_work"] == {"relative_ANUPQ_calls": 0,
                                          "Reidemeister_Schreier": False,
                                          "full_Elements": False,
                                          "full_regular_matrices": False,
                                          "full_H1_basis_or_rank": False},
            "prohibited-work receipt")
    theorem = data["theorem_boundary"]
    require(theorem["Phi3_H4_isolation_required"] is False and
            "global B4-B" in theorem["not_covered"], "theorem boundary")

    dictionary: dict[str, Any] | None = None
    e3: Quotient | None = None
    e4: Quotient | None = None
    expected_dp: dict[str, Any] | None = None
    dp_failures: list[list[str]] | None = None
    if "correction_dictionary" in data:
        e3, e4 = reconstruct(q3)
        formula = formula_subset()
        require(data["formula_sha256"] == FORMULA_SHA and
                data["relevant_formula"] == formula and
                data["relevant_formula_sha256"] == digest_obj(formula),
                "relevant formula")
        validate_base_replay(data, q3, e3, e4)
        dictionary = rebuild_dictionary(q3, e3)
        require(data["correction_dictionary"] == dictionary,
                "dictionary provenance/order")
        expected_dp, dp_failures = rebuild_fixed_context_dp(dictionary, e4)
    validate_search_prefix(data["bounded_search_prefix"], dp_failures,
                           None if dictionary is None else dictionary["count"])

    if data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE":
        stop = data["resource_stop"]
        require(stop["cap"] in RESOURCE_REASONS and stop["cap"] == data["reason"] and
                stop["large_structures_released_before_write"] is True and
                stop["no_mathematical_obstruction_claimed"] is True and
                data["bounded_search_prefix"]["structural_cap"] == {
                    "hit": True, "reason": stop["cap"],
                    "source": ("monitor" if stop["cap"] in
                               {"producer_soft_timeout", "producer_soft_rss"}
                               else "registered_structural_cap")},
                "resource terminal/prefix")
        accounting = data["resource_accounting_at_stop"]
        require(set(accounting) >= {"live", "monitor", "transaction",
                                    "bounded_search_prefix"} and
                accounting["bounded_search_prefix"] ==
                data["bounded_search_prefix"] and
                accounting["live"]["element_pool"] <= CAPS["element_pool"] and
                accounting["live"]["dag_nodes"] <= CAPS["provenance_dag_nodes"] and
                accounting["live"]["dag_edges"] <= CAPS["provenance_dag_edges"] and
                data["bounded_search_prefix"]["blocker"] == {
                    "count": len(data["blocker_table"]),
                    "sha256": digest_obj(data["blocker_table"])},
                "resource bounded accounting")
        return

    require(dictionary is not None and e3 is not None and e4 is not None and
            expected_dp is not None and dp_failures is not None and
            data["fixed_context_cheap_DP"]["complete"] is True,
            "complete-search DP prerequisites")
    normalized_inverse, normalized_base_key, _ = \
        rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized_inverse,
            "normalized inverse fibre")
    search = data["search"]
    validate_transaction_search(data, search, dictionary, e4, expected_dp,
                                dp_failures, normalized_inverse)
    prefix = data["bounded_search_prefix"]
    require(prefix["cheap"]["completed"] is True and
            prefix["blocker"] == {"count": len(search["blocker_table"]),
                                   "sha256": digest_obj(search["blocker_table"])} and
            prefix["transaction"] == {
                "starts": search["transaction"]["starts"],
                "commits": search["transaction"]["commits"],
                "rollbacks": search["transaction"]["rollbacks"]} and
            prefix["structural_cap"] == {"hit": False, "reason": None,
                                          "source": None},
            "complete terminal prefix binding")
    dag_accounting = search["provenance_DAG"]
    expected_dag_keys = {"live_nodes", "live_edges", "peak_nodes", "peak_edges",
                         "packed_arrays", "node_payload_bytes", "edge_payload_bytes",
                         "pivot_payload", "expanded_pivot_ledgers_stored",
                         "failed_column_and_candidate_nodes_rolled_back",
                         "positive_serialization"}
    if data["terminal_token"] == "B345_RELFRAT3_LITERAL_PAIR_PASS":
        expected_dag_keys |= {"serialized_reachable_nodes", "serialized_reachable_edges"}
    require(set(dag_accounting) == expected_dag_keys and
            dag_accounting["packed_arrays"] is True and
            1 <= dag_accounting["live_nodes"] <= dag_accounting["peak_nodes"] <=
            CAPS["provenance_dag_nodes"] and
            0 <= dag_accounting["live_edges"] <= dag_accounting["peak_edges"] <=
            CAPS["provenance_dag_edges"] and
            dag_accounting["failed_column_and_candidate_nodes_rolled_back"] is True,
            "packed DAG accounting")
    pool = search["element_pool"]
    require(pool["capacity"] == CAPS["element_pool"] and
            1 <= pool["size"] <= pool["peak"] <= CAPS["element_pool"] and
            pool["packed_width_bytes"] == e4.degree+e4.collector.n and
            pool["packed_payload_bytes"] == pool["size"]*pool["packed_width_bytes"] and
            pool["transaction_rollbacks"] == search["transaction"]["rollbacks"] and
            pool["transaction_commits"] == search["transaction"]["commits"] and
            pool["rollback_lru_clears"] == 2*pool["transaction_rollbacks"] and
            pool["rollback_suffix_removed"] >= pool["max_rollback_suffix"] >= 0,
            "transactional element pool")
    validate_lru_accounting(pool["product_cache"], CAPS["element_product_cache"])
    validate_lru_accounting(pool["inverse_cache"], CAPS["element_inverse_cache"])
    integrity = search["element_pool_integrity"]
    require(integrity["size"] == integrity["lookup_size"] == pool["size"] and
            integrity["all_unique"] is True and
            integrity["fixed_width_bytes"] == pool["packed_width_bytes"],
            "pool integrity")
    require_sha256(integrity["ordered_canonical_payload_sha256"],
                   "pool binding SHA")
    lazy = search["lazy_sections"]
    require(lazy["capacity"] == CAPS["section_slp_nodes"] and
            1 <= lazy["live_nodes"] <= lazy["peak_nodes"] <= CAPS["section_slp_nodes"] and
            search["translations_used"] <= lazy["bound_elements"] <=
            CAPS["coefficient_translates_per_relator"], "lazy BFS sections")
    pc = search["pc_caches"]
    require(pc["unbounded_full_token_word_cache"] is False and
            len(pc["collectors"]) == 2 and
            pc["hits"] == sum(row["hits"] for row in pc["collectors"]) and
            pc["misses"] == sum(row["misses"] for row in pc["collectors"]) and
            pc["evictions"] == sum(row["evictions"] for row in pc["collectors"]),
            "PC cache aggregate")
    for collector in pc["collectors"]:
        validate_lru_accounting(collector["pair_product"], CAPS["pc_pair_product_cache"])
        validate_lru_accounting(collector["inverse"], CAPS["pc_inverse_cache"])

    if data["terminal_token"] != "B345_RELFRAT3_LITERAL_PAIR_PASS":
        require(search["translations_used"] == CAPS["coefficient_translates_per_relator"] and
                "serialized_reachable_nodes" not in dag_accounting and
                search["transaction"]["commits"] == 0,
                "exhausted incomplete search")
        return
    require(dag_accounting["serialized_reachable_nodes"] ==
            data["boundary_proof_dag"]["node_count"] and
            dag_accounting["serialized_reachable_edges"] ==
            data["boundary_proof_dag"]["edge_count"] and
            search["transaction"]["commits"] == 1,
            "positive DAG/commit")
    selected = data["selected_pair"]
    index = selected["correction_index"]
    require(1 <= index <= dictionary["count"] and
            selected["correction_word"] == dictionary["words"][index-1] and
            index in expected_dp["survivor_indices"] and
            index not in {row["candidate_index"]
                          for row in search["full_quotient_rejected"]},
            "selected correction/order")
    targets = expected_targets(selected, e4, normalized_inverse, normalized_base_key)
    require(selected["boundary_certificate_names"] == [row[0] for row in targets],
            "selected target names")
    by_id, reverse = validate_registry(data["quotient_element_registry"], {3: e3, 4: e4})
    models = validate_fox_models(data["fox_models"], e3, e4, reverse)
    validate_certificates(data["boundary_certificates"], data["boundary_proof_dag"],
                          targets, e4, models[4], by_id, reverse)
    bindings = []
    for name, kind, word in targets:
        gradient, value = fox(word, e4)
        bindings.append(independent_gradient_binding(name, kind, gradient, value))
    require(search["selected_gradient_bindings"] == bindings,
            "selected canonical gradient regeneration")
    replay = data["literal_replay"]
    require(replay["correction_lift_freedom"]["coarse_J_H_all_five_cofaces_identity"] is True and
            replay["hexagon"]["each_checked_in_all_five_cofaces"] is True and
            replay["pentagon"]["ordered_five_coface_A18_direct_PB4_residual"] is True and
            replay["charming"]["explicit_commutator_product"] is True and
            replay["onto"]["two_sided_inverse_on_six_marked_generators"] is True,
            "positive literal replay")


def fixed_targets(e4: Quotient, normalized: dict[str, Any]) \
        -> list[tuple[str, str, list[int]]]:
    f: list[int] = list(FIXED_WORD)
    c34 = cofaces(3)
    targets: list[tuple[str, str, list[int]]] = [
        (f"charming_error_coface_{i}", "charming", []) for i in range(5)]
    for hindex, residual in enumerate(hexagon_words(f), 1):
        source = embed_f2(residual)
        for slot, mapping in enumerate(c34):
            targets.append((f"hexagon_{hindex}_coface_{slot}", "hexagon",
                            substitute(source, mapping)))
    targets.append(("ordered_A18_pentagon", "pentagon", pentagon_word(f)))
    source_words_fixed = source_words(f)
    inverse_words = normalized["selected_inverse_words"]
    st, ts = two_sided_residuals(source_words_fixed, inverse_words)
    for index, relator in enumerate(pure_relations(4), 1):
        targets.append((f"S_relation_{index}", "endomorphism_relation",
                        substitute(relator, source_words_fixed)))
        targets.append((f"T_relation_{index}", "endomorphism_relation",
                        substitute(relator, inverse_words)))
    targets += [(f"ST_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(st)]
    targets += [(f"TS_generator_{i+1}", "onto_two_sided_inverse", word)
                for i, word in enumerate(ts)]
    require(len(targets) == 50 and targets[5][0] == "hexagon_1_coface_0" and
            all(e4.eval(word) == e4.identity for _, _, word in targets),
            "fixed target order/quotient identities")
    return targets


def validate_fixed_prefix(prefix: dict[str, Any], target_names: list[str]) -> None:
    require(set(prefix) == {"fixed_candidate", "current", "blocker",
                            "transaction", "structural_cap", "accounting"},
            "fixed bounded-prefix keys")
    fixed = prefix["fixed_candidate"]
    require(set(fixed) == {"correction_index", "correction_word",
                           "direct_gates_completed", "direct_gate_replay_count",
                           "target_count", "target_order_sha256"} and
            fixed["correction_index"] == 1 and fixed["correction_word"] == [] and
            fixed["direct_gates_completed"] is True and
            fixed["direct_gate_replay_count"] in {1, 2} and
            fixed["target_count"] == len(target_names) == 50 and
            fixed["target_order_sha256"] == digest_obj(target_names),
            "fixed prefix candidate binding")
    current = prefix["current"]
    require(set(current) == {"checkpoint", "correction_index",
                             "target_ordinal", "target_name"} and
            (current["checkpoint"] is None or
             isinstance(current["checkpoint"], int) and current["checkpoint"] > 0) and
            current["correction_index"] in {None, 1} and
            (current["target_ordinal"] is None or
             isinstance(current["target_ordinal"], int) and
             1 <= current["target_ordinal"] <= len(target_names)) and
            (current["target_name"] is None or
             current["target_ordinal"] is not None and
             current["target_name"] == target_names[current["target_ordinal"]-1]),
            "fixed current prefix")
    blocker = prefix["blocker"]
    require(set(blocker) == {"count", "sha256"} and
            blocker["count"] in {0, 1}, "fixed blocker prefix")
    require_sha256(blocker["sha256"], "fixed blocker prefix SHA")
    tx = prefix["transaction"]
    require(set(tx) == {"starts", "commits", "rollbacks"} and
            all(isinstance(x, int) and x >= 0 for x in tx.values()) and
            tx["commits"] in {0, 1} and tx["rollbacks"] <= tx["starts"],
            "fixed transaction prefix")
    structural = prefix["structural_cap"]
    require(set(structural) == {"hit", "reason", "source"} and
            (structural == {"hit": False, "reason": None, "source": None} or
             structural["hit"] is True and
             structural["source"] in {"monitor", "registered_structural_cap"} and
             structural["reason"] in RESOURCE_REASONS),
            "fixed structural prefix")
    accounting = prefix["accounting"]
    require(set(accounting) == {"translations", "basis_pivots",
                                "basis_live_entries", "pool_size", "DAG_nodes",
                                "DAG_edges", "section_nodes", "PC_cache_hits",
                                "PC_cache_misses", "PC_cache_evictions"} and
            all(isinstance(value, int) and value >= 0
                for value in accounting.values()),
            "fixed prefix accounting")


def validate_fixed_trace(search: dict[str, Any], width: int) -> None:
    validate_blocker_trace(search, width)
    history = search["blocker_history"]
    trace = search["checkpoint_trace"]
    require(history and history[0]["candidate_index"] == 1 and
            history[0]["failed_checkpoint"] == 1 and
            history[0]["target_ordinal"] == 6 and
            history[0]["target_name"] == "hexagon_1_coface_0" and
            history[0]["component"] == 4 and
            all(row["candidate_index"] == 1 for row in history) and
            all(row["candidate_index"] == 1 for row in trace),
            "reconstructed first fixed blocker")
    checkpoints = search["geometric_translation_checkpoints"]
    for row in history:
        retry = row["retry_checkpoints"][0] if row["retry_checkpoints"] else None
        expected_skips = [cp for cp in checkpoints
                          if row["failed_checkpoint"] < cp and
                          (retry is None or cp < retry)]
        require(row["skip_checkpoints"] == expected_skips and
                len(row["retry_checkpoints"]) <= 1,
                "complete fixed blocker skip schedule")
        if retry is not None:
            intro = row["matching_introduction"]
            expected_retry = next(cp for cp in checkpoints
                                  if cp >= intro["translation_ordinal"])
            require(retry == expected_retry,
                    "retry is first checkpoint after exact pivot")


def validate_fixed_claim_boundary(data: dict[str, Any]) -> None:
    """Bind the deliberately narrow, positive-only interpretation."""
    universe = data["registered_universe"]
    require(universe["kind"] == "fixed_positive_candidate" and
            universe["correction_indices"] == [1] and
            universe["correction_word"] == [] and
            universe["full_4096_universe_claimed"] is False and
            universe["earliest_global_candidate_claimed"] is False and
            universe["negative_completeness_claimed"] is False,
            "fixed positive-only universe/claim boundary")
    token = data["terminal_token"]
    if token != "B345_RELFRAT3_FIXED_CANDIDATE_PASS":
        require(data["claim_classification"] == "unknown_not_obstruction" and
                data["claim_scope"] == "fixed_candidate_only" and
                data["no_mathematical_obstruction_claimed"] is True,
                "fixed nonpositive claim boundary")


def validate_cap_utilization(block: dict[str, Any], *, live: int,
                             pool_peak: int, pivots: int, dag_nodes: int,
                             dag_edges: int, rss_peak: int) -> None:
    expected_values = {
        "live_sparse_entries": (live, CAPS["total_sparse_group_ring_keys"]),
        "element_pool_peak": (pool_peak, CAPS["element_pool"]),
        "sparse_pivots": (pivots, CAPS["sparse_pivot_rows"]),
        "DAG_nodes": (dag_nodes, CAPS["provenance_dag_nodes"]),
        "DAG_edges": (dag_edges, CAPS["provenance_dag_edges"]),
        "RSS_peak_bytes": (rss_peak, CAPS["producer_soft_rss_bytes"]),
    }
    require(set(block) == set(expected_values), "cap utilization keys")
    for key, (value, cap) in expected_values.items():
        require(block[key] == {"value": value, "cap": cap,
                               "ratio": value/cap},
                f"cap utilization {key}")


def validate_cap_calibration(record: dict[str, Any]) -> None:
    require(record == CAP_CALIBRATION,
            "exact fixed-candidate v6 cap-calibration record")


def validate_fixed_receipt(data: dict[str, Any], q3: dict[str, Any],
                           q3_path: Path, repo: Path) -> None:
    required = {"schema", "status", "terminal_token", "reason", "pins",
                "source_hashes", "input_q3_terminal", "output_path", "caps",
                "registered_universe", "representation_contract",
                "claim_classification", "claim_scope",
                "no_mathematical_obstruction_claimed", "theorem_boundary",
                "prohibited_work", "resource_guards", "performance",
                "cap_calibration",
                "bounded_search_prefix", "formula_sha256", "relevant_formula",
                "relevant_formula_sha256", "matched_quotients",
                "base_q3_replay", "normalized_inverse_fibre",
                "fixed_candidate_preflight"}
    optional = {"search", "direct_lane", "resource_stop",
                "resource_accounting_at_stop", "quotient_element_registry",
                "fox_models", "boundary_proof_dag", "selected_pair",
                "boundary_certificates", "literal_replay", "blocker_table",
                "blocker_history", "checkpoint_trace", "pivot_introductions",
                "direct_vs_preflight_comparisons"}
    require(required <= set(data) and set(data) <= required | optional,
            "fixed v6 top-level layout")
    require(data["schema"] == SCHEMA and data["caps"] == CAPS and
            data["output_path"] == str(OUTPUT_PATH).replace("\\", "/") and
            data["input_q3_terminal"] == q3.get("terminal_token"),
            "fixed schema/caps/input/output")
    changed_caps = {key for key in CAPS if CAPS[key] != V5_CAPS[key]}
    require(changed_caps == {"total_sparse_group_ring_keys", "element_pool"},
            "independent exact v5/v6 cap delta")
    validate_cap_calibration(data["cap_calibration"])
    token = data["terminal_token"]
    require(token in TERMINALS and data["status"] == token and
            data["claim_scope"] == "fixed_candidate_only" and
            data["no_mathematical_obstruction_claimed"] is True,
            "fixed terminal/scope")
    validate_fixed_claim_boundary(data)
    is_pass = token == "B345_RELFRAT3_FIXED_CANDIDATE_PASS"
    is_incomplete = token == "B345_RELFRAT3_FIXED_CANDIDATE_INCOMPLETE"
    is_unknown = token == "B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE"
    require(data["claim_classification"] ==
            ("positive_certificate" if is_pass else "unknown_not_obstruction"),
            "fixed claim classification")
    if not is_pass:
        require("selected_pair" not in data and
                "boundary_certificates" not in data and
                "boundary_proof_dag" not in data,
                "nonpositive promoted to certificate")

    pins = data["pins"]
    require(set(pins) == {"q3_producer", "q3_checker", "q3_driver",
                          "q3_artifact", "formula_sha256",
                          "semantic_reference_v1", "semantic_reference_v2",
                          "semantic_reference_v3", "semantic_reference_v4",
                          "semantic_reference_v5"},
            "fixed v6 pin key set")
    for key, path, sha in (("q3_producer", Q3_PRODUCER, Q3_PRODUCER_SHA),
                           ("q3_checker", Q3_CHECKER, Q3_CHECKER_SHA),
                           ("q3_driver", Q3_DRIVER, Q3_DRIVER_SHA)):
        require(pins[key] == {"path": str(path).replace("\\", "/"),
                              "sha256": sha} and digest_file(repo/path) == sha,
                f"fixed pin {key}")
    require(pins["q3_artifact"] == {
                "path": str(Q3_ARTIFACT_PATH).replace("\\", "/"),
                "sha256": Q3_ARTIFACT_SHA} and
            digest_file(q3_path) == Q3_ARTIFACT_SHA and
            pins["formula_sha256"] == FORMULA_SHA and
            digest_obj(q3["formulas"]) == FORMULA_SHA,
            "fixed q3/formula pins")
    references = (
        ("semantic_reference_v5", V5_PRODUCER, V5_PRODUCER_SHA,
         V5_CHECKER, V5_CHECKER_SHA, V5_DRIVER, V5_DRIVER_SHA,
         "frozen fixed-candidate v5 semantics and cap-stop reference"),
        ("semantic_reference_v4", V4_PRODUCER, V4_PRODUCER_SHA,
         V4_CHECKER, V4_CHECKER_SHA, V4_DRIVER, V4_DRIVER_SHA,
         "frozen transactional-v4 arithmetic, Fox, blocker, and packed-certificate reference"),
        ("semantic_reference_v3", V3_PRODUCER, V3_PRODUCER_SHA,
         V3_CHECKER, V3_CHECKER_SHA, V3_DRIVER, V3_DRIVER_SHA,
         "frozen packed-v3 semantics and positive-certificate reference"),
        ("semantic_reference_v2", V2_PRODUCER, V2_PRODUCER_SHA,
         V2_CHECKER, V2_CHECKER_SHA, V2_DRIVER, V2_DRIVER_SHA,
         "frozen v2 mathematics, universe, gates, and search order"),
        ("semantic_reference_v1", V1_PRODUCER, V1_PRODUCER_SHA,
         V1_CHECKER, V1_CHECKER_SHA, V1_DRIVER, V1_DRIVER_SHA,
         "frozen semantic predicate and search-order reference"),
    )
    for key, producer, psha, checker, csha, driver, dsha, role in references:
        require(pins[key] == {
                    "producer": {"path": str(producer).replace("\\", "/"),
                                 "sha256": psha},
                    "checker": {"path": str(checker).replace("\\", "/"),
                                "sha256": csha},
                    "driver": {"path": str(driver).replace("\\", "/"),
                               "sha256": dsha}, "role": role} and
                digest_file(repo/producer) == psha and
                digest_file(repo/checker) == csha and
                digest_file(repo/driver) == dsha, f"fixed {key}")
    require(data["source_hashes"] == {
                "producer_sha256": digest_file(
                    repo/"search/d972_b345_relfrat3_fixed_candidate_v6.py"),
                "checker_sha256": digest_file(Path(__file__)),
                "driver_sha256": digest_file(
                    repo/"search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g")},
            "fixed source hashes")
    require(data["representation_contract"] == {
                "version": "fixed-candidate-cap-calibrated-packed-v6",
                "persistent_element_equality": "exact canonical bytes; never a digest",
                "sparse_keys": "component plus stable zero-based exact element-pool ID",
                "pivot_order": "component then canonical EKey bytes; never insertion ID",
                "BFS_order": "+1..+6,-1..-6 first-seen shortlex",
                "candidate_sections_retained": False,
                "candidate_gradients_retained_across_checkpoints": False,
                "candidate_transaction": "exact element-pool and provenance-DAG suffix rollback",
                "missing_pivot_blocker": "target ordinal, component, canonical E4 bytes",
                "proof_DAG_in_memory": "packed parallel arrays",
                "positive_DAG_serialization": "reachable union as typed little-endian base64 arrays",
                "cache_eviction_semantics": "capacity and eviction order affect speed only, never canonical values or search order",
                "persistent_checkpoint_resume": False,
                "correction_dictionary_constructed": False,
                "fixed_context_cheap_DP_executed": False,
                "cap_calibration_only": True,
                "resume_or_checkpoint_imported": False,
            } and
            data["prohibited_work"]["omitted_corrections_evaluated"] == 0 and
            data["prohibited_work"]["all_dictionary_DP_executed"] is False,
            "fixed no-dictionary/DP contract")

    selected_q3 = q3["selected_solution"]
    require(selected_q3["roof_row_index"] == 37 and
            selected_q3["exponent"] == 2 and
            selected_q3["correction_index"] == 1 and
            selected_q3["marking_m"] == 0 and selected_q3["lambda"] == 1 and
            selected_q3["typed_source_word"] == FIXED_WORD,
            "fixed q3 selected roof")
    expected_universe = {
        "kind": "fixed_positive_candidate", "correction_indices": [1],
        "correction_word": [],
        "fixed_outside_roof": {
            "row_index": 37, "exponent": 2,
            "roof_key": selected_q3["roof_key"],
            "typed_source_word": list(FIXED_WORD),
            "arithmetic_outside_by_index_three":
                selected_q3["arithmetic_outside_by_index_three"],
            "source": "frozen q3 selected outside roof"},
        "full_4096_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
        "marking_m": 0, "lambda": 1,
    }
    require(data["registered_universe"] == expected_universe,
            "fixed registered universe")

    e3, e4 = reconstruct(q3)
    formula = formula_subset()
    require(data["formula_sha256"] == FORMULA_SHA and
            data["relevant_formula"] == formula and
            data["relevant_formula_sha256"] == digest_obj(formula),
            "fixed formula reconstruction")
    validate_base_replay(data, q3, e3, e4)
    normalized, base_key, _ = rebuild_normalized_inverse_fibre(q3, e4)
    require(data["normalized_inverse_fibre"] == normalized,
            "fixed normalized inverse")
    targets = fixed_targets(e4, normalized)
    target_names = [row[0] for row in targets]
    source_lengths = [len(word) for word in source_words(FIXED_WORD)]
    inverse_lengths = [len(word) for word in normalized["selected_inverse_words"]]
    target_lengths = [len(row[2]) for row in targets]
    require(data["fixed_candidate_preflight"] == {
                "correction_index": 1, "correction_word": [],
                "selected_word": list(FIXED_WORD),
                "selected_word_length": len(FIXED_WORD),
                "source_word_lengths": source_lengths,
                "inverse_word_lengths": inverse_lengths,
                "target_names": target_names,
                "target_word_lengths": target_lengths,
                "max_source_word_length": max(source_lengths),
                "max_inverse_word_length": max(inverse_lengths),
                "max_target_word_length": max(target_lengths),
                "all_direct_quotient_gates_pass": True,
                "direct_gate_replay_count_before_sparse_growth": 1,
                "marking_m": 0, "lambda": 1,
                "fixed_outside_roof": {"row_index": 37, "exponent": 2},
                "target_order_sha256": digest_obj(target_names),
                "word_representation": "flat freely reduced signed-generator lists",
                "single_word_or_section_length_cap":
                    CAPS["single_word_or_section_length"]},
            "fixed literal preflight")
    validate_fixed_prefix(data["bounded_search_prefix"], target_names)

    guard = data["resource_guards"]
    require(guard["seconds"] == 18_000 and guard["minutes"] == 300 and
            guard["rss_bytes"] == CAPS["producer_soft_rss_bytes"] and
            guard["terminal_on_hit"] ==
                "B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE" and
            guard["hit"] is is_unknown and
            (not is_unknown and guard["hit_reason"] is None or
             is_unknown and guard["hit_reason"] == data["resource_stop"]["cap"]),
            "fixed resource guard")
    require(isinstance(data["performance"].get("phase_timings_seconds"), dict),
            "fixed phase timings")

    if is_unknown:
        stop = data["resource_stop"]
        require(stop["cap"] in RESOURCE_REASONS and stop["cap"] == data["reason"] and
                stop["large_structures_released_before_write"] is True and
                stop["no_mathematical_obstruction_claimed"] is True and
                data["bounded_search_prefix"]["structural_cap"]["reason"] == stop["cap"],
                "fixed UNKNOWN resource")
        rows = {"blocker_table": data["blocker_table"],
                "blocker_history": data["blocker_history"],
                "pivot_introductions": data["pivot_introductions"],
                "checkpoint_trace": data["checkpoint_trace"],
                "blocker_table_sha256": digest_obj(data["blocker_table"]),
                "blocker_history_sha256": digest_obj(data["blocker_history"]),
                "checkpoint_trace_sha256": digest_obj(data["checkpoint_trace"]),
                "geometric_translation_checkpoints": [
                    1 << i for i in range(16)
                    if (1 << i) <= data["bounded_search_prefix"]["accounting"]["translations"]]}
        if rows["blocker_history"]:
            validate_fixed_trace(rows, e4.degree+e4.collector.n)
        stopped = data["resource_accounting_at_stop"]
        require(stopped["bounded_search_prefix"] ==
                data["bounded_search_prefix"], "fixed UNKNOWN prefix binding")
        basis_stop = stopped["basis"]
        validate_cap_utilization(
            data["performance"]["cap_utilization"],
            live=basis_stop["live_sparse_vector_entries"],
            pool_peak=stopped["element_pool"]["peak"],
            pivots=basis_stop["pivot_count"],
            dag_nodes=basis_stop["dag"]["peak_nodes"],
            dag_edges=basis_stop["dag"]["peak_edges"],
            rss_peak=guard["peak_rss_bytes"])
        return

    search = data["search"]
    require(search["registered_correction_indices"] == [1] and
            search["registered_correction_word"] == [] and
            search["other_corrections_constructed_or_evaluated"] == 0 and
            search["correction_dictionary_constructed"] is False and
            search["fixed_context_cheap_DP_executed"] is False and
            search["persistent_candidate_cache_size"] == 0 and
            search["persistent_candidate_gradient_entries"] == 0 and
            search["same_basis_reused_for_fixed_candidate_retries"] is True and
            search["fixed_candidate_scheduled_from_checkpoint"] == 1 and
            search["candidate_resource_skips"] == [] and
            search["direct_vs_preflight_all_equal"] is True and
            search["columns_seen"] == 11*search["translations_used"] and
            search["geometric_translation_checkpoints"] == [
                1 << i for i in range(16)
                if (1 << i) <= search["translations_used"]],
            "fixed search contract")
    validate_fixed_trace(search, e4.degree+e4.collector.n)
    comparisons = search["direct_vs_preflight_comparisons"]
    outcomes = [row for row in search["checkpoint_trace"]
                if row["event"] in {"missing_pivot", "selected_commit"}]
    require(search["direct_word_replay_count"] == len(comparisons) and
            [(row["checkpoint"], row["candidate_index"]) for row in comparisons] ==
            [(row["checkpoint"], row["candidate_index"]) for row in outcomes] and
            all(row == {"checkpoint": row["checkpoint"], "candidate_index": 1,
                        "direct_failed_gates": [],
                        "equal_to_preflight": True}
                for row in comparisons),
            "fixed direct replay schedule")
    tx = search["transaction"]
    require(tx["starts"] == len(outcomes) and
            tx["rollbacks"] == sum(row["event"] == "missing_pivot"
                                    for row in outcomes) and
            tx["commits"] == sum(row["event"] == "selected_commit"
                                  for row in outcomes) and
            tx["blocker_skips"] == sum(row["event"] == "missing_pivot_skip"
                                       for row in search["checkpoint_trace"]) and
            tx["blocker_retries"] == sum(row["event"] == "exact_pivot_retry"
                                         for row in search["checkpoint_trace"]),
            "fixed transaction accounting")
    pool = search["element_pool"]
    require(pool["transaction_rollbacks"] == tx["rollbacks"] and
            pool["transaction_commits"] == tx["commits"] and
            pool["rollback_lru_clears"] == 2*tx["rollbacks"],
            "fixed pool transactions")
    validate_lru_accounting(pool["product_cache"], CAPS["element_product_cache"])
    validate_lru_accounting(pool["inverse_cache"], CAPS["element_inverse_cache"])
    validate_cap_utilization(
        data["performance"]["cap_utilization"],
        live=search["live_sparse_vector_entries"], pool_peak=pool["peak"],
        pivots=search["pivot_count"],
        dag_nodes=search["provenance_DAG"]["peak_nodes"],
        dag_edges=search["provenance_DAG"]["peak_edges"],
        rss_peak=guard["peak_rss_bytes"])

    if is_incomplete:
        require(search["translations_used"] ==
                CAPS["coefficient_translates_per_relator"] and
                tx["commits"] == 0 and len(search["blocker_table"]) == 1 and
                data["direct_lane"]["literal_pair_found"] is False,
                "fixed INCOMPLETE terminal")
        return

    require(is_pass and tx["commits"] == 1 and
            data["bounded_search_prefix"]["fixed_candidate"]
                ["direct_gate_replay_count"] == 2 and
            data["direct_lane"] == {"literal_pair_found": True,
                                      "PB5_branch_constructed": False,
                                      "stop_reason": "FIRST_LITERAL_PAIR_AT_PHI"},
            "fixed PASS terminal")
    selected = data["selected_pair"]
    require(selected["correction_index"] == 1 and
            selected["correction_word"] == [] and
            selected["selected_word"] == FIXED_WORD and
            selected["boundary_certificate_names"] == target_names,
            "fixed selected pair")
    expected = expected_targets(selected, e4, normalized, base_key)
    require(expected == targets, "fixed selected target regeneration")
    by_id, reverse = validate_registry(data["quotient_element_registry"],
                                       {3: e3, 4: e4})
    models = validate_fox_models(data["fox_models"], e3, e4, reverse)
    validate_certificates(data["boundary_certificates"],
                          data["boundary_proof_dag"], targets, e4,
                          models[4], by_id, reverse)
    bindings = [independent_gradient_binding(name, kind, *fox(word, e4))
                for name, kind, word in targets]
    require(search["selected_gradient_bindings"] == bindings,
            "fixed PASS gradient bindings")


def expect_reject(action: Any, label: str) -> None:
    try:
        action()
    except (Reject, KeyError, IndexError, TypeError, ValueError):
        return
    raise AssertionError(f"mutation accepted: {label}")


def self_test() -> None:
    require([len(pure_relations(r)) for r in (3, 4, 5)] == [2, 11, 35],
            "selftest presentation")
    # Independent negative-letter Fox orientation canary in C3.
    cyclic = {"generator_count": 1, "relative_orders": [3],
              "power_relations": [[0]], "inverses": [[2]],
              "conjugate_relations": [], "inverse_conjugate_relations": []}
    pc = Collector(cyclic)
    # Collector intentionally has no producer-style unit helper; construct it directly.
    quotient = Quotient(2, 1, pc, [(p_one(1), (1,))])
    gradient, value = fox([-1], quotient)
    require(value == (p_one(1), (2,)) and list(gradient.values()) == [2],
            "negative Fox orientation")
    cube, cube_value = fox([1, 1, 1], quotient)
    require(cube_value == quotient.identity and boundary1(cube, quotient) == {},
            "C3 Fox cycle")
    mutated = dict(cube)
    first = next(iter(mutated))
    mutated[first] = 2 if mutated[first] == 1 else 1
    expect_reject(lambda: require(mutated == cube, "support coefficient"),
                  "Fox coefficient")
    fake = {"terminal_token": "B345_RELFRAT3_LITERAL_PAIR_PASS",
            "status": "B345_RELFRAT3_LITERAL_PAIR_PASS", "direct_lane": {}}
    expect_reject(lambda: validate_terminal(fake), "false positive terminal")
    unsupported = {"terminal_token": "B345_RELFRAT3_MISSING_MATCHED_CHAIN",
                   "status": "B345_RELFRAT3_MISSING_MATCHED_CHAIN"}
    expect_reject(lambda: validate_terminal(unsupported),
                  "unsupported missing-matched-chain terminal")
    projected = {"terminal_token": "B345_RELFRAT3_PROJECTED_OBSTRUCTION",
                 "status": "B345_RELFRAT3_PROJECTED_OBSTRUCTION",
                 "projection_certificate": {"independently_replayed": True}}
    expect_reject(lambda: validate_terminal(projected),
                  "unsupported projected-obstruction terminal")
    altered = formula_subset()
    altered = json.loads(json.dumps(altered))
    altered["cofaces_3_4"][1][0].reverse()
    expect_reject(lambda: require(altered == formula_subset(), "coface"),
                  "coface orientation")
    cache_row = {"capacity": 8, "size": 2, "peak": 3,
                 "hits": 5, "misses": 7, "evictions": 1, "clears": 2}
    validate_lru_accounting(cache_row, 8)
    bad_cache = dict(cache_row); bad_cache["peak"] = 9
    expect_reject(lambda: validate_lru_accounting(bad_cache, 8),
                  "LRU peak cap")
    bad_cache = dict(cache_row); bad_cache["capacity"] = 9
    expect_reject(lambda: validate_lru_accounting(bad_cache, 8),
                  "LRU capacity drift")

    # Independent bounded fixed-context recurrence versus literal evaluation.
    q4 = Quotient(4, 1, pc, [(p_one(1), (1,))] +
                  [(p_one(1), (0,)) for _ in range(5)])
    toy_dictionary = {
        "words": [[], [1], [-1], [1, 1]], "count": 4,
        "seed_words": [[1]], "parent_indices": [0, 1, 1, 2],
        "signed_seed_edges": [0, 1, -1, 1],
    }
    toy_dp, toy_failures = rebuild_fixed_context_dp(toy_dictionary, q4)
    toy_direct = [direct_cheap_failures(reduce_word(FIXED_WORD+word), word, q4)
                  for word in toy_dictionary["words"]]
    require(toy_failures == toy_direct and
            toy_dp["contexts"]["named_use_count"] == 46 and
            len(toy_dp["failure_bitsets"]) == 27,
            "independent fixed-context DP/direct")
    toy_prefix = {
        "cheap": {"evaluated": 4, "completed": True,
                  "survivor_count": toy_dp["survivor_count"],
                  "survivor_indices_sha256": toy_dp["survivor_indices_sha256"],
                  "evaluated_prefix_sha256": toy_dp["evaluated_prefix_sha256"],
                  "survivor_prefix_sha256": toy_dp["survivor_prefix_sha256"],
                  "current_candidate": None},
        "current": {"checkpoint": 4, "correction_index": None,
                    "target_ordinal": None, "target_name": None},
        "blocker": {"count": 0, "sha256": digest_obj([])},
        "transaction": {"starts": 0, "commits": 0, "rollbacks": 0},
        "structural_cap": {"hit": True, "reason": "toy_cap",
                           "source": "registered_structural_cap"},
        "accounting": {"translations": 4, "basis_pivots": 1,
                       "basis_live_entries": 1, "pool_size": 3,
                       "DAG_nodes": 2, "DAG_edges": 0, "section_nodes": 3,
                       "PC_cache_hits": 0, "PC_cache_misses": 0,
                       "PC_cache_evictions": 0},
    }
    validate_search_prefix(toy_prefix, toy_failures, 4)
    bad_prefix = json.loads(json.dumps(toy_prefix))
    bad_prefix["cheap"]["evaluated_prefix_sha256"] = "0"*64
    expect_reject(lambda: validate_search_prefix(bad_prefix, toy_failures, 4),
                  "cheap prefix digest mutation")

    blob = element_blob(q4.identity).hex()
    intro = {"component": 2, "element_hex": blob,
             "translation_ordinal": 3, "relator_index": 1}
    blocker = {"candidate_index": 2, "target_ordinal": 1,
               "target_name": "toy", "component": 2,
               "element_hex": blob, "failed_checkpoint": 1,
               "skip_checkpoints": [2], "retry_checkpoints": [4],
               "history_id": 1, "matching_introduction": intro}
    trace = [
        {"checkpoint": 1, "candidate_index": 2, "event": "missing_pivot",
         "target_ordinal": 1, "target_name": "toy", "component": 2,
         "element_hex": blob, "blocker_history_id": 1,
         "pool_suffix_removed": 1},
        {"checkpoint": 2, "candidate_index": 2, "event": "missing_pivot_skip",
         "blocker_history_id": 1, "pool_element_present": False,
         "basis_pivot_present": False},
        {"checkpoint": 4, "candidate_index": 2, "event": "exact_pivot_retry",
         "blocker_history_id": 1, "matching_introduction": intro},
    ]
    blocker_search = {"blocker_table": [],
                      "blocker_table_sha256": digest_obj([]),
                      "blocker_history": [blocker],
                      "blocker_history_sha256": digest_obj([blocker]),
                      "pivot_introductions": [intro],
                      "checkpoint_trace": trace,
                      "checkpoint_trace_sha256": digest_obj(trace)}
    validate_blocker_trace(blocker_search, len(bytes.fromhex(blob)))
    bad_blocker = json.loads(json.dumps(blocker_search))
    bad_blocker["checkpoint_trace"][2]["matching_introduction"][
        "translation_ordinal"] = 5
    bad_blocker["checkpoint_trace_sha256"] = digest_obj(
        bad_blocker["checkpoint_trace"])
    expect_reject(lambda: validate_blocker_trace(
        bad_blocker, len(bytes.fromhex(blob))), "retry before exact pivot")

    def seal_array(type_name: str, typecode: str, values: Sequence[int],
                   cap: int) -> dict[str, Any]:
        if typecode == "B":
            raw, itemsize = bytes(values), 1
        else:
            packed = array(typecode, values)
            if sys.byteorder != "little":
                packed.byteswap()
            raw, itemsize = packed.tobytes(), packed.itemsize
        return {"type": type_name, "array_typecode": typecode,
                "endianness": "little", "length": len(values),
                "itemsize": itemsize, "byte_length": len(raw), "cap": cap,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "base64": base64.b64encode(raw).decode("ascii")}

    def seal_toy(kinds: Sequence[int] = (1, 1, 2),
                 relators: Sequence[int] = (1, 2, 0),
                 translations: Sequence[int] = (11, 12, 0),
                 offsets: Sequence[int] = (0, 0, 0, 2),
                 parents: Sequence[int] = (1, 2),
                 coefficients: Sequence[int] = (1, 2),
                 roots: Sequence[dict[str, Any]] =
                 ({"name": "toy_root", "node_id": 3},)) -> dict[str, Any]:
        arrays = {
            "node_kind": seal_array("uint8", "B", kinds,
                                      CAPS["provenance_dag_nodes"]),
            "leaf_relator_index": seal_array("uint16", "H", relators,
                                               CAPS["provenance_dag_nodes"]),
            "leaf_translation_element_id": seal_array(
                "uint32", "I", translations, CAPS["provenance_dag_nodes"]),
            "edge_offsets": seal_array("uint32", "I", offsets,
                                         CAPS["provenance_dag_nodes"]+1),
            "edge_parent_node_id": seal_array(
                "uint32", "I", parents, CAPS["provenance_dag_edges"]),
            "edge_coefficient": seal_array(
                "uint8", "B", coefficients, CAPS["provenance_dag_edges"]),
        }
        root_rows = [dict(row) for row in roots]
        manifest = {name: {key: value for key, value in row.items()
                           if key != "base64"} for name, row in arrays.items()}
        leaf_count = sum(1 for value in kinds if value == 1)
        return {
            "format": "packed-parallel-arrays/v1", "field": 3,
            "node_order": "one_based_topological", "translation_action": "left",
            "arrays": arrays, "roots": root_rows, "node_count": len(kinds),
            "edge_count": len(parents), "leaf_count": leaf_count,
            "combination_node_count": len(kinds)-leaf_count,
            "all_serialized_nodes_reachable_from_roots": True,
            "unreachable_search_nodes_pruned": 7,
            "expanded_boundary_ledgers_serialized": False,
            "packed_manifest_sha256": digest_obj({"arrays": manifest,
                                                   "roots": root_rows}),
        }

    key_a: VKey = (1, ((0,), (0,)))
    key_b: VKey = (2, ((1,), (1,)))
    leaf_values = {(1, 11): {key_a: 1}, (2, 12): {key_b: 1}}
    expected_toy = {key_a: 1, key_b: 2}

    def audit_toy(block: dict[str, Any]) -> None:
        roots, _ = evaluate_proof_dag(
            block, ["toy_root"],
            lambda node: leaf_values[(node["relator_index"],
                                      node["translation_element_id"])])
        require(roots["toy_root"] == expected_toy, "toy DAG root")

    toy = seal_toy()
    audit_toy(toy)
    orientation = json.loads(json.dumps(toy))
    orientation["translation_action"] = "right"
    expect_reject(lambda: audit_toy(orientation), "packed DAG orientation")
    expect_reject(lambda: audit_toy(seal_toy(coefficients=(1, 1))),
                  "packed DAG coefficient")
    expect_reject(lambda: audit_toy(seal_toy(relators=(2, 2, 0))),
                  "packed DAG wrong leaf")
    expect_reject(lambda: audit_toy(seal_toy(parents=(3, 2))),
                  "packed DAG forward reference")
    expect_reject(lambda: audit_toy(seal_toy(
        kinds=(1, 1, 2, 1), relators=(1, 2, 0, 1),
        translations=(11, 12, 0, 11), offsets=(0, 0, 0, 2, 2))),
        "packed DAG unreachable node")
    expect_reject(lambda: audit_toy(seal_toy(
        roots=({"name": "toy_root", "node_id": 1},))),
        "packed DAG root mutation")
    bad_sha = json.loads(json.dumps(toy))
    bad_sha["arrays"]["node_kind"]["sha256"] = "0"*64
    expect_reject(lambda: audit_toy(bad_sha), "packed array SHA")
    bad_id = json.loads(json.dumps(toy))
    bad_id["arrays"]["leaf_translation_element_id"]["base64"] = "@@@="
    expect_reject(lambda: audit_toy(bad_id), "packed malformed base64")
    bad_cap = json.loads(json.dumps(toy))
    bad_cap["arrays"]["edge_parent_node_id"]["cap"] -= 1
    expect_reject(lambda: audit_toy(bad_cap), "packed array cap drift")
    print("D972_B345_RELFRAT3_V4_CHECKER_SELFTEST_PASS "
          "mutations=19 fox_orientation_canaries=2 packed_DAG_canaries=10 "
          "cheap_DP_direct=4 named_contexts=46 prefix_UNKNOWN=1 "
          "blocker_skip_retry=1 streaming_parent_release=1")


def self_test_fixed() -> None:
    """One bounded test of only the fixed-candidate v6 cap successor."""
    changed_caps = {key for key in CAPS if CAPS[key] != V5_CAPS[key]}
    require(changed_caps == {"total_sparse_group_ring_keys", "element_pool"} and
            all(CAPS[key] == V5_CAPS[key] for key in set(CAPS)-changed_caps),
            "checker cap-only v5/v6 delta")
    validate_cap_calibration(dict(CAP_CALIBRATION))
    for key in ("new_sparse_cap", "new_pool_cap", "resume_used",
                "semantics_changed", "source_receipt_sha256"):
        bad = dict(CAP_CALIBRATION)
        bad[key] = (not bad[key] if isinstance(bad[key], bool) else
                    0 if isinstance(bad[key], int) else "0"*64)
        expect_reject(lambda bad=bad: validate_cap_calibration(bad),
                      f"cap calibration {key}")
    stride = CAPS["element_pool"]
    ids = [0, 1, 29, stride-1]
    keys = [left*stride+right for left in ids for right in ids]
    require(len(set(keys)) == len(keys) and
            all(divmod(key, stride) == pair for key, pair in
                zip(keys, ((left, right) for left in ids for right in ids))),
            "checker pool pair-key stride")
    old_prefix_live = V5_CAPS["total_sparse_group_ring_keys"]+1
    require(old_prefix_live > V5_CAPS["total_sparse_group_ring_keys"] and
            old_prefix_live <= CAPS["total_sparse_group_ring_keys"],
            "checker old-cap prefix continuation")
    utilization = {
        "live_sparse_entries": {"value": old_prefix_live,
            "cap": CAPS["total_sparse_group_ring_keys"],
            "ratio": old_prefix_live/CAPS["total_sparse_group_ring_keys"]},
        "element_pool_peak": {"value": 7, "cap": CAPS["element_pool"],
            "ratio": 7/CAPS["element_pool"]},
        "sparse_pivots": {"value": 3, "cap": CAPS["sparse_pivot_rows"],
            "ratio": 3/CAPS["sparse_pivot_rows"]},
        "DAG_nodes": {"value": 4, "cap": CAPS["provenance_dag_nodes"],
            "ratio": 4/CAPS["provenance_dag_nodes"]},
        "DAG_edges": {"value": 2, "cap": CAPS["provenance_dag_edges"],
            "ratio": 2/CAPS["provenance_dag_edges"]},
        "RSS_peak_bytes": {"value": 11, "cap": CAPS["producer_soft_rss_bytes"],
            "ratio": 11/CAPS["producer_soft_rss_bytes"]},
    }
    validate_cap_utilization(utilization, live=old_prefix_live, pool_peak=7,
                             pivots=3, dag_nodes=4, dag_edges=2, rss_peak=11)
    bad_utilization = json.loads(json.dumps(utilization))
    bad_utilization["live_sparse_entries"]["ratio"] = 1.0
    expect_reject(lambda: validate_cap_utilization(
        bad_utilization, live=old_prefix_live, pool_peak=7, pivots=3,
        dag_nodes=4, dag_edges=2, rss_peak=11), "cap utilization ratio")
    class TrivialQ:
        identity = 0

        @staticmethod
        def eval(word: Sequence[int]) -> int:
            return 0

    normalized = {"selected_inverse_words": [[i] for i in range(1, 7)]}
    targets = fixed_targets(TrivialQ(), normalized)  # type: ignore[arg-type]
    names = [name for name, _, _ in targets]
    require(len(targets) == 50 and names[5] == "hexagon_1_coface_0" and
            fixed_targets(TrivialQ(), normalized) == targets,
            "fixed direct target order/PASS regeneration")

    universe = {
        "kind": "fixed_positive_candidate", "correction_indices": [1],
        "correction_word": [], "fixed_outside_roof": {},
        "full_4096_universe_claimed": False,
        "earliest_global_candidate_claimed": False,
        "negative_completeness_claimed": False,
    }
    claim = {
        "registered_universe": universe,
        "terminal_token": "B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE",
        "claim_classification": "unknown_not_obstruction",
        "claim_scope": "fixed_candidate_only",
        "no_mathematical_obstruction_claimed": True,
    }
    validate_fixed_claim_boundary(claim)
    for key in ("full_4096_universe_claimed",
                "earliest_global_candidate_claimed",
                "negative_completeness_claimed"):
        bad = json.loads(json.dumps(claim))
        bad["registered_universe"][key] = True
        expect_reject(lambda bad=bad: validate_fixed_claim_boundary(bad), key)
    for key, value in (("claim_classification", "obstruction"),
                       ("claim_scope", "global_B4-B"),
                       ("no_mathematical_obstruction_claimed", False)):
        bad = json.loads(json.dumps(claim)); bad[key] = value
        expect_reject(lambda bad=bad: validate_fixed_claim_boundary(bad), key)

    prefix = {
        "fixed_candidate": {
            "correction_index": 1, "correction_word": [],
            "direct_gates_completed": True, "direct_gate_replay_count": 1,
            "target_count": 50, "target_order_sha256": digest_obj(names),
        },
        "current": {"checkpoint": 8, "correction_index": None,
                    "target_ordinal": None, "target_name": None},
        "blocker": {"count": 1, "sha256": digest_obj(["fixed"])},
        "transaction": {"starts": 2, "commits": 0, "rollbacks": 2},
        "structural_cap": {"hit": True, "reason": "element_pool",
                           "source": "registered_structural_cap"},
        "accounting": {"translations": 8, "basis_pivots": 2,
                       "basis_live_entries": 2, "pool_size": 7,
                       "DAG_nodes": 2, "DAG_edges": 1, "section_nodes": 8,
                       "PC_cache_hits": 1, "PC_cache_misses": 1,
                       "PC_cache_evictions": 0},
    }
    validate_fixed_prefix(prefix, names)
    bad_prefix = json.loads(json.dumps(prefix))
    bad_prefix["fixed_candidate"]["correction_word"] = [1]
    expect_reject(lambda: validate_fixed_prefix(bad_prefix, names),
                  "fixed correction mutation")

    first = {"candidate_index": 1, "target_ordinal": 6,
             "target_name": "hexagon_1_coface_0", "component": 4,
             "element_hex": "00", "failed_checkpoint": 1,
             "skip_checkpoints": [2], "retry_checkpoints": [4],
             "history_id": 1,
             "matching_introduction": {"component": 4, "element_hex": "00",
                                        "translation_ordinal": 3,
                                        "relator_index": 1}}
    second = {"candidate_index": 1, "target_ordinal": 7,
              "target_name": "hexagon_1_coface_1", "component": 5,
              "element_hex": "01", "failed_checkpoint": 4,
              "skip_checkpoints": [8], "retry_checkpoints": [],
              "history_id": 2}
    trace = [
        {"checkpoint": 1, "candidate_index": 1, "event": "missing_pivot",
         "target_ordinal": 6, "target_name": "hexagon_1_coface_0",
         "component": 4, "element_hex": "00", "blocker_history_id": 1,
         "pool_suffix_removed": 1},
        {"checkpoint": 2, "candidate_index": 1,
         "event": "missing_pivot_skip", "blocker_history_id": 1,
         "pool_element_present": False, "basis_pivot_present": False},
        {"checkpoint": 4, "candidate_index": 1,
         "event": "exact_pivot_retry", "blocker_history_id": 1,
         "matching_introduction": first["matching_introduction"]},
        {"checkpoint": 4, "candidate_index": 1, "event": "missing_pivot",
         "target_ordinal": 7, "target_name": "hexagon_1_coface_1",
         "component": 5, "element_hex": "01", "blocker_history_id": 2,
         "pool_suffix_removed": 2},
        {"checkpoint": 8, "candidate_index": 1,
         "event": "missing_pivot_skip", "blocker_history_id": 2,
         "pool_element_present": True, "basis_pivot_present": False},
    ]
    search = {
        "blocker_table": [second], "blocker_history": [first, second],
        "pivot_introductions": [first["matching_introduction"]],
        "checkpoint_trace": trace,
        "blocker_table_sha256": digest_obj([second]),
        "blocker_history_sha256": digest_obj([first, second]),
        "checkpoint_trace_sha256": digest_obj(trace),
        "geometric_translation_checkpoints": [1, 2, 4, 8],
    }
    validate_fixed_trace(search, 1)
    bad_trace = json.loads(json.dumps(search))
    bad_trace["blocker_history"][0]["target_ordinal"] = 5
    bad_trace["blocker_history_sha256"] = digest_obj(bad_trace["blocker_history"])
    expect_reject(lambda: validate_fixed_trace(bad_trace, 1),
                  "checkpoint-1 blocker imported/drifted")

    def seal_array(type_name: str, typecode: str, values: Sequence[int],
                   cap: int) -> dict[str, Any]:
        if typecode == "B":
            raw, itemsize = bytes(values), 1
        else:
            packed = array(typecode, values)
            if sys.byteorder != "little":
                packed.byteswap()
            raw, itemsize = packed.tobytes(), packed.itemsize
        return {"type": type_name, "array_typecode": typecode,
                "endianness": "little", "length": len(values),
                "itemsize": itemsize, "byte_length": len(raw), "cap": cap,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "base64": base64.b64encode(raw).decode("ascii")}

    def packed_toy(coefficients: Sequence[int] = (1, 2)) -> dict[str, Any]:
        arrays = {
            "node_kind": seal_array("uint8", "B", (1, 1, 2),
                                      CAPS["provenance_dag_nodes"]),
            "leaf_relator_index": seal_array("uint16", "H", (1, 2, 0),
                                               CAPS["provenance_dag_nodes"]),
            "leaf_translation_element_id": seal_array(
                "uint32", "I", (11, 12, 0), CAPS["provenance_dag_nodes"]),
            "edge_offsets": seal_array("uint32", "I", (0, 0, 0, 2),
                                         CAPS["provenance_dag_nodes"]+1),
            "edge_parent_node_id": seal_array(
                "uint32", "I", (1, 2), CAPS["provenance_dag_edges"]),
            "edge_coefficient": seal_array(
                "uint8", "B", coefficients, CAPS["provenance_dag_edges"]),
        }
        roots = [{"name": "fixed_root", "node_id": 3}]
        manifest = {name: {key: value for key, value in row.items()
                           if key != "base64"} for name, row in arrays.items()}
        return {"format": "packed-parallel-arrays/v1", "field": 3,
                "node_order": "one_based_topological",
                "translation_action": "left", "arrays": arrays,
                "roots": roots, "node_count": 3, "edge_count": 2,
                "leaf_count": 2, "combination_node_count": 1,
                "all_serialized_nodes_reachable_from_roots": True,
                "unreachable_search_nodes_pruned": 0,
                "expanded_boundary_ledgers_serialized": False,
                "packed_manifest_sha256": digest_obj(
                    {"arrays": manifest, "roots": roots})}

    key_a: VKey = (1, ((0,), (0,)))
    key_b: VKey = (2, ((1,), (1,)))
    leaves = {(1, 11): {key_a: 1}, (2, 12): {key_b: 1}}
    def audit_packed(block: dict[str, Any]) -> None:
        roots, _ = evaluate_proof_dag(
            block, ["fixed_root"],
            lambda node: leaves[(node["relator_index"],
                                 node["translation_element_id"])])
        require(roots["fixed_root"] == {key_a: 1, key_b: 2},
                "packed PASS streaming replay")

    audit_packed(packed_toy())
    expect_reject(lambda: audit_packed(packed_toy((1, 1))),
        "packed coefficient mutation")
    require(TERMINALS == {
                "B345_RELFRAT3_FIXED_CANDIDATE_PASS",
                "B345_RELFRAT3_FIXED_CANDIDATE_INCOMPLETE",
                "B345_RELFRAT3_FIXED_CANDIDATE_UNKNOWN_RESOURCE"},
            "fixed terminal set")
    print("D972_B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_CHECKER_SELFTEST_PASS "
          "universe=1 dictionary_DP_calls=0 targets=50 blocker_ordinal=6 "
          "skip_retry_replace=1 prefix_UNKNOWN=1 packed_DAG_replay=1 "
          "claim_mutations=6 terminals=3 cap_delta=2 "
          "cap_mutations=6 stride_injective=1 old_cap_continue=1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("q3_artifact", nargs="?", type=Path)
    parser.add_argument("artifact", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        require(args.q3_artifact is None and args.artifact is None,
                "selftest paths")
        self_test_fixed()
        return 0
    require(args.q3_artifact is not None and args.artifact is not None,
            "q3 and relative artifacts required")
    q3_path, artifact = args.q3_artifact.resolve(), args.artifact.resolve()
    repo = Path(__file__).resolve().parents[1]
    require(q3_path == (repo/Q3_ARTIFACT_PATH).resolve() and
            artifact == (repo/OUTPUT_PATH).resolve(), "fixed checker paths")
    q3 = json.loads(q3_path.read_text(encoding="utf-8"))
    data = json.loads(artifact.read_text(encoding="utf-8"))
    validate_fixed_receipt(data, q3, q3_path, repo)
    print(f"B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_CHECKER_PASS "
          f"terminal={data['terminal_token']} "
          f"claim_classification={data['claim_classification']} "
          f"artifact_sha256={digest_file(artifact)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(f"B345_RELFRAT3_FIXED_CANDIDATE_CAP_V6_CHECKER_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
