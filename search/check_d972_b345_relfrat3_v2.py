#!/usr/bin/env python3
"""Independent checker for d972-b345-relative-frattini3/v2.

No producer helper is imported.  The checker rebuilds the presentations,
cofaces, matched quotient arithmetic, Fox gradients, every shared-DAG leaf
and operation, and every accepted literal residual.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA = "d972-b345-relative-frattini3/v2"
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
OUTPUT_PATH = Path("ci/out/d972_b345_relfrat3_v2.json")
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
}
TERMINALS = {
    "B345_RELFRAT3_LITERAL_PAIR_PASS",
    "B345_RELFRAT3_SEARCH_INCOMPLETE",
    "B345_RELFRAT3_UNKNOWN_RESOURCE",
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
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        self.cache: dict[tuple[int, ...], Pc] = {(): self.identity()}

    def coord(self, row: Sequence[int]) -> Pc:
        require(len(row) == self.n and all(isinstance(x, int) and 0 <= x < 3
                                           for x in row), "collector coordinate")
        return tuple(row)

    def identity(self) -> Pc:
        return (0,)*self.n

    def collect(self, signed: Sequence[int]) -> Pc:
        key = tuple(signed)
        if key in self.cache:
            return self.cache[key]
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
        answer = tuple(row)
        self.cache[key] = answer
        return answer

    def mul(self, a: Pc, b: Pc) -> Pc:
        return self.collect(pc_word(a)+pc_word(b))

    def inverse(self, a: Pc) -> Pc:
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(a[i-1]):
                word.extend(pc_word(self.inverses[i-1]))
        return self.collect(word)

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
    seen = {()}
    queue: deque[list[int]] = deque([[]])
    steps = seeds + [inv_word(x) for x in seeds]
    while queue and len(words) < CAPS["candidate_correction_dictionary"]:
        prefix = queue.popleft()
        for step in steps:
            word = reduce_word(prefix+step)
            if tuple(word) not in seen:
                require(exponent_sums(word, 2) == [0, 0] and
                        e3.eval(embed_f2(word)) == e3.identity,
                        "dictionary coarse J_H/free-derived invariant")
                seen.add(tuple(word))
                words.append(word)
                queue.append(word)
                if len(words) == CAPS["candidate_correction_dictionary"]:
                    break
    return {"order": "identity, then breadth-first products of authenticated H3 commutator seeds and inverses",
            "source": "commutators with cubes of the frozen 27-word coarse-trivial exponent-three fibre",
            "words": words, "count": len(words),
            "cap": CAPS["candidate_correction_dictionary"],
            "all_words_in_H3": True, "all_words_in_coarse_J_H": True,
            "all_words_free_exponent_zero": True,
            "not_complete_for_all_H3": True,
            "membership_in_finer_J_Phi_required": False,
            "J_Phi_cosets_are_the_lift_freedom": True,
            "seed_words": seeds}


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
        require(row["id"] == expected_id and row["rank"] in quotients,
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


def evaluate_proof_dag(block: dict[str, Any], expected_names: Sequence[str],
                       leaf_resolver: Any) \
        -> tuple[dict[str, Vector], dict[str, int]]:
    payload_keys = {
        "field", "node_order", "translation_action", "nodes", "roots",
        "node_count", "edge_count", "leaf_count", "combination_node_count",
        "all_serialized_nodes_reachable_from_roots",
        "unreachable_search_nodes_pruned",
        "expanded_boundary_ledgers_serialized",
    }
    require(set(block) == payload_keys | {"dag_sha256"}, "proof DAG fields")
    payload = {key: block[key] for key in payload_keys}
    require(block["dag_sha256"] == digest_obj(payload), "proof DAG digest")
    nodes = block["nodes"]
    require(block["field"] == 3 and
            block["node_order"] == "one_based_topological" and
            block["translation_action"] == "left" and
            isinstance(nodes, list) and nodes and
            block["node_count"] == len(nodes) <= CAPS["provenance_dag_nodes"] and
            isinstance(block["unreachable_search_nodes_pruned"], int) and
            block["unreachable_search_nodes_pruned"] >= 0 and
            block["all_serialized_nodes_reachable_from_roots"] is True and
            block["expanded_boundary_ledgers_serialized"] is False,
            "proof DAG header")
    values: dict[int, Vector] = {}
    parents: dict[int, list[int]] = {}
    edge_count = 0
    leaf_count = 0
    for expected_id, node in enumerate(nodes, 1):
        require(node.get("id") == expected_id, "proof DAG node id/order")
        if node.get("kind") == "translated_relator_leaf":
            require(set(node) == {"id", "kind", "relator_index",
                                  "translation_element_id", "translation_action"} and
                    node["translation_action"] == "left",
                    "proof DAG leaf fields/orientation")
            values[expected_id] = leaf_resolver(node)
            parents[expected_id] = []
            leaf_count += 1
        else:
            require(node.get("kind") == "linear_combination" and
                    set(node) == {"id", "kind", "terms"} and
                    isinstance(node["terms"], list),
                    "proof DAG combination fields")
            vector: Vector = {}
            seen: set[int] = set()
            parent_rows: list[int] = []
            for term in node["terms"]:
                require(set(term) == {"node_id", "coefficient"} and
                        isinstance(term["node_id"], int) and
                        1 <= term["node_id"] < expected_id and
                        term["node_id"] not in seen and
                        term["coefficient"] in (1, 2),
                        "proof DAG backward reference/coefficient")
                seen.add(term["node_id"])
                parent_rows.append(term["node_id"])
                add_scaled(vector, values[term["node_id"]], term["coefficient"])
            require(bool(node["terms"]) or expected_id == 1,
                    "proof DAG empty combination placement")
            values[expected_id] = vector
            parents[expected_id] = parent_rows
            edge_count += len(parent_rows)
    roots = block["roots"]
    require(isinstance(roots, list) and
            [row.get("name") for row in roots] == list(expected_names) and
            all(set(row) == {"name", "node_id"} and
                isinstance(row["node_id"], int) and
                1 <= row["node_id"] <= len(nodes) for row in roots),
            "proof DAG roots/order")
    root_ids = {row["name"]: row["node_id"] for row in roots}
    require(len(root_ids) == len(roots), "proof DAG duplicate root name")
    reached: set[int] = set()
    pending = list(root_ids.values())
    while pending:
        node_id = pending.pop()
        if node_id not in reached:
            reached.add(node_id)
            pending.extend(parents[node_id])
    require(reached == set(range(1, len(nodes)+1)),
            "proof DAG unreachable node")
    require(block["edge_count"] == edge_count <= CAPS["provenance_dag_edges"] and
            block["leaf_count"] == leaf_count and
            block["combination_node_count"] == len(nodes)-leaf_count,
            "proof DAG accounting")
    return {name: values[node_id] for name, node_id in root_ids.items()}, root_ids


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
        if data["resource_stop"].get("candidate_local") is True:
            skipped = data["resource_stop"]["skipped_candidates"]
            counts: dict[str, int] = {}
            for row in skipped:
                require(isinstance(row["candidate_index"], int) and
                        1 <= row["candidate_index"] <=
                        CAPS["candidate_correction_dictionary"] and
                        row["phase"] in {"cheap_candidate_preparation",
                                         "inverse_or_gradient",
                                         "sparse_membership"} and
                        isinstance(row["reason"], str) and row["reason"],
                        "candidate resource row")
                counts[row["reason"]] = counts.get(row["reason"], 0) + 1
            require(skipped and
                    len(skipped) == len({row["candidate_index"] for row in skipped}) and
                    data["resource_stop"]["reason_counts"] == counts and
                    data["search"]["candidate_resource_skips"] == skipped and
                    "not treated as failures" in data["reason"],
                    "candidate resource receipt")


def validate_soft_timeout(data: dict[str, Any]) -> None:
    block = data["soft_timeout"]
    require(set(block) == {
                "seconds", "minutes", "external_job_limit_minutes",
                "safety_margin_minutes", "clock", "hit", "last_checked_phase",
                "check_count", "terminal_on_hit", "consulted_in_selftest",
            } and
            block["seconds"] == CAPS["producer_soft_timeout_seconds"] == 18_000 and
            block["minutes"] == 300 and
            block["external_job_limit_minutes"] == 330 and
            block["safety_margin_minutes"] == 30 and
            block["clock"] == "time.monotonic" and
            isinstance(block["hit"], bool) and
            isinstance(block["last_checked_phase"], str) and
            block["last_checked_phase"] and
            isinstance(block["check_count"], int) and block["check_count"] >= 0 and
            block["terminal_on_hit"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and
            block["consulted_in_selftest"] is False,
            "soft timeout contract")
    actual_soft_stop = (
        data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and
        data.get("resource_stop", {}).get("cap") == "producer_soft_timeout")
    require(block["hit"] is actual_soft_stop,
            "soft timeout hit/terminal equivalence")


def validate_receipt(data: dict[str, Any], q3: dict[str, Any], q3_path: Path,
                     repo: Path) -> None:
    require(data.get("schema") == SCHEMA and data.get("caps") == CAPS,
            "schema/caps")
    validate_terminal(data)
    validate_soft_timeout(data)
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
        "producer_sha256": digest_file(repo/"search/d972_b345_relfrat3_v2.py"),
        "checker_sha256": digest_file(Path(__file__)),
        "driver_sha256": digest_file(repo/"search/d972_b345_relfrat3_gha_driver_v2.g"),
    }
    require(data["source_hashes"] == local_sources, "new source SHA binding")
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
    if "search" not in data:
        stop = data["resource_stop"]
        require(data["terminal_token"] == "B345_RELFRAT3_UNKNOWN_RESOURCE" and
                stop.get("candidate_local") is not True and
                stop.get("cap") in {
                    "producer_soft_timeout", "single_word_or_section_length",
                    "total_sparse_group_ring_keys", "single_sparse_elimination_row",
                    "target_elimination_support", "sparse_pivot_rows",
                    "provenance_dag_nodes", "provenance_dag_edges",
                } and data["reason"] == stop["cap"],
                "global resource-only receipt")
        if "resource_accounting_at_stop" in data:
            accounting = data["resource_accounting_at_stop"]
            require(accounting["live_sparse_vector_entries"] <=
                    CAPS["total_sparse_group_ring_keys"] and
                    accounting["pivot_count"] <= CAPS["sparse_pivot_rows"] and
                    accounting["dag"]["live_nodes"] <= CAPS["provenance_dag_nodes"] and
                    accounting["dag"]["live_edges"] <= CAPS["provenance_dag_edges"],
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
    if "search" in data:
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

    toy_payload = {
        "field": 3,
        "node_order": "one_based_topological",
        "translation_action": "left",
        "nodes": [
            {"id": 1, "kind": "translated_relator_leaf", "relator_index": 1,
             "translation_element_id": 11, "translation_action": "left"},
            {"id": 2, "kind": "translated_relator_leaf", "relator_index": 2,
             "translation_element_id": 12, "translation_action": "left"},
            {"id": 3, "kind": "linear_combination",
             "terms": [{"node_id": 1, "coefficient": 1},
                       {"node_id": 2, "coefficient": 2}]},
        ],
        "roots": [{"name": "toy_root", "node_id": 3}],
        "node_count": 3,
        "edge_count": 2,
        "leaf_count": 2,
        "combination_node_count": 1,
        "all_serialized_nodes_reachable_from_roots": True,
        "unreachable_search_nodes_pruned": 7,
        "expanded_boundary_ledgers_serialized": False,
    }

    def seal(payload: dict[str, Any]) -> dict[str, Any]:
        clean = {key: value for key, value in payload.items()
                 if key != "dag_sha256"}
        return {**clean, "dag_sha256": digest_obj(clean)}

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

    toy = seal(toy_payload)
    audit_toy(toy)
    orientation = json.loads(json.dumps(toy))
    orientation["nodes"][0]["translation_action"] = "right"
    expect_reject(lambda: audit_toy(seal(orientation)), "DAG leaf orientation")
    coefficient = json.loads(json.dumps(toy))
    coefficient["nodes"][2]["terms"][1]["coefficient"] = 1
    expect_reject(lambda: audit_toy(seal(coefficient)), "DAG coefficient")
    wrong_leaf = json.loads(json.dumps(toy))
    wrong_leaf["nodes"][0]["relator_index"] = 2
    expect_reject(lambda: audit_toy(seal(wrong_leaf)), "DAG wrong leaf")
    forward = json.loads(json.dumps(toy))
    forward["nodes"][2]["terms"][0]["node_id"] = 3
    expect_reject(lambda: audit_toy(seal(forward)), "DAG forward reference")
    unreachable = json.loads(json.dumps(toy))
    unreachable["nodes"].append(
        {"id": 4, "kind": "translated_relator_leaf", "relator_index": 1,
         "translation_element_id": 11, "translation_action": "left"})
    unreachable["node_count"] = 4
    unreachable["leaf_count"] = 3
    expect_reject(lambda: audit_toy(seal(unreachable)), "DAG unreachable node")
    root_mutation = json.loads(json.dumps(toy))
    root_mutation["roots"][0]["node_id"] = 1
    expect_reject(lambda: audit_toy(seal(root_mutation)), "DAG root mutation")
    print("D972_B345_RELFRAT3_V2_CHECKER_SELFTEST_PASS "
          "mutations=11 fox_orientation_canaries=2 provenance_DAG_canaries=6")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("q3_artifact", nargs="?", type=Path)
    parser.add_argument("artifact", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        require(args.q3_artifact is None and args.artifact is None,
                "selftest paths")
        self_test()
        return 0
    require(args.q3_artifact is not None and args.artifact is not None,
            "q3 and relative artifacts required")
    q3_path, artifact = args.q3_artifact.resolve(), args.artifact.resolve()
    repo = Path(__file__).resolve().parents[1]
    require(q3_path == (repo/Q3_ARTIFACT_PATH).resolve() and
            artifact == (repo/OUTPUT_PATH).resolve(), "fixed checker paths")
    q3 = json.loads(q3_path.read_text(encoding="utf-8"))
    data = json.loads(artifact.read_text(encoding="utf-8"))
    validate_receipt(data, q3, q3_path, repo)
    print(f"B345_RELFRAT3_CHECKER_PASS terminal={data['terminal_token']} "
          f"claim_classification={data['claim_classification']} "
          f"artifact_sha256={digest_file(artifact)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(f"B345_RELFRAT3_CHECKER_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
