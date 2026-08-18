#!/usr/bin/env python3
"""Independent finite checker for the FC-8* A5^4 chief certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from collections import deque
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

SCHEMA = "d972-b4-fc8-a5four/v1"
TERMINAL = "FC8_A5_FOUR_CHIEF_CROSSCHECKED"
ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "core_producer": ("search/d972_d972core_c2six_intersection_v2.g",
        "577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c"),
    "deletion_fixture": ("search/certs/d972_b4_marity_reduction_maps_v1.json",
        "6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2"),
    "deletion_checker": ("search/check_d972_b4_marity_reduction_maps_v1.py",
        "eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032"),
    "a5_marking": ("certificates/A1.v2.json",
        "24c42967f260a4dad2fb89b52f5709388549bebb37664b798a1502a5ef6d8a02"),
    "a5_settled_extension": ("certificates/A1.v2.2.json",
        "a348b5044e98a7c64711b507d43015c780d16606a66482fe33ccd2bfd3eee8d6"),
    "t40_screening": ("docs/notes/fullverbal_tower_screening_v1.md",
        "9e69838f923a77385ce191244c57e88dc24d95b3c9ae9d5d0f9b0cd0c148cad8"),
}
LABELS = ["x12", "x13", "x14", "x23", "x24", "x34"]
EXPECTED_MAPS = [
    [[], [], [], [1], [2], [3]],
    [[], [1], [2], [], [], [3]],
    [[1], [], [2], [], [3], []],
    [[1], [2], [], [3], [], []],
]
ARTIN = [
    [[1], [-1, 4, 1], [-1, 5, 1], [2], [3], [6]],
    [[-4, 2, 4], [1], [3], [4], [-4, 6, 4], [5]],
    [[1], [-6, 3, 6], [2], [-6, 5, 6], [4], [6]],
]
SUPPORT_PAIRS = [(4, 6), (2, 6), (1, 5), (1, 4)]
SUPPORT_WORDS = [[-a, -b, a, b] for a, b in SUPPORT_PAIRS]


class Reject(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def sha_bytes(path: Path) -> tuple[str, int]:
    raw = path.read_bytes()
    return hashlib.sha256(raw).hexdigest(), len(raw)


def pinned_json(key: str) -> Any:
    rel, expected = PINS[key]
    path = ROOT / rel
    got, _ = sha_bytes(path)
    require(got == expected, f"pinned {key} SHA drift")
    return json.loads(path.read_text(encoding="utf-8"))


Perm = tuple[int, ...]


def one(n: int) -> Perm:
    return tuple(range(n))


def mul(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degree mismatch")
    return tuple(b[a[i]] for i in range(len(a)))


def inv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def conjugate(a: Perm, t: Perm) -> Perm:
    return mul(mul(inv(t), a), t)


def cycle(n: int, entries: Sequence[int]) -> Perm:
    out = list(range(n))
    e = [x - 1 for x in entries]
    for a, b in zip(e, e[1:] + e[:1]):
        out[a] = b
    return tuple(out)


def parity(a: Perm) -> int:
    return sum(a[i] > a[j] for i in range(len(a)) for j in range(i + 1, len(a))) % 2


def power(a: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return power(inv(a), -exponent)
    out, base = one(len(a)), a
    while exponent:
        if exponent & 1:
            out = mul(out, base)
        base = mul(base, base)
        exponent >>= 1
    return out


def order(a: Perm) -> int:
    out, k = one(len(a)), 0
    while True:
        k += 1
        out = mul(out, a)
        if out == one(len(a)):
            return k


def row(a: Perm) -> list[int]:
    return [x + 1 for x in a]


def from_row(raw: Sequence[int], degree: int) -> Perm:
    require(len(raw) == degree and set(raw) == set(range(1, degree + 1)),
            "invalid permutation row")
    return tuple(x - 1 for x in raw)


def evaluate(word: Sequence[int], generators: Sequence[Perm]) -> Perm:
    require(bool(generators), "empty generator list")
    out = one(len(generators[0]))
    for letter in word:
        require(letter and abs(letter) <= len(generators), "signed word alphabet")
        value = generators[abs(letter) - 1]
        out = mul(out, value if letter > 0 else inv(value))
    return out


def closure(generators: Sequence[Perm], cap: int) -> set[Perm]:
    require(bool(generators), "closure needs a generator")
    identity = one(len(generators[0]))
    steps = list(generators) + [inv(x) for x in generators]
    seen, queue = {identity}, deque([identity])
    while queue:
        a = queue.popleft()
        for g in steps:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                require(len(seen) <= cap, "bounded group enumeration cap")
                queue.append(b)
    return seen


def normal_closure(seed: Perm, ambient_generators: Sequence[Perm], cap: int) -> set[Perm]:
    seeds = [seed]
    subgroup = closure(seeds, cap)
    steps = list(ambient_generators) + [inv(x) for x in ambient_generators]
    while True:
        added = None
        for h in list(seeds):
            for g in steps:
                value = conjugate(h, g)
                if value not in subgroup:
                    added = value
                    break
            if added is not None:
                break
        if added is None:
            return subgroup
        seeds.append(added)
        subgroup = closure(seeds, cap)


def commutator(a: Perm, b: Perm) -> Perm:
    return mul(mul(mul(inv(a), inv(b)), a), b)


def derived_two(x: Perm, y: Perm, cap: int) -> set[Perm]:
    return normal_closure(commutator(x, y), (x, y), cap)


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(letter != 0, "zero free letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(letter and abs(letter) <= len(images), "free substitution alphabet")
        image = list(images[abs(letter) - 1])
        out.extend(reversed([-x for x in image]) if letter < 0 else image)
        out = free_reduce(out)
    return out


def artin_step(rank: int, letter: int) -> list[list[int]]:
    require(1 <= abs(letter) < rank, "Artin generator range")
    images = [[i] for i in range(1, rank + 1)]
    i = abs(letter) - 1
    if letter > 0:
        images[i], images[i + 1] = [i + 1, i + 2, -(i + 1)], [i + 1]
    else:
        images[i], images[i + 1] = [i + 2], [-(i + 2), i + 1, i + 2]
    return images


def artin_images(rank: int, braid_word: Sequence[int]) -> list[list[int]]:
    images = [[i] for i in range(1, rank + 1)]
    for letter in braid_word:
        step = artin_step(rank, letter)
        images = [substitute(w, step) for w in images]
    return images


def pairs(rank: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(1, rank) for j in range(i + 1, rank + 1)]


def aij_braid(i: int, j: int) -> list[int]:
    return list(range(j - 1, i, -1)) + [i, i] + [-k for k in range(i + 1, j)]


def expand_pure(rank: int, word: Sequence[int]) -> list[int]:
    return substitute(word, [aij_braid(i, j) for i, j in pairs(rank)])


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    ps, old = pairs(rank), pairs(rank - 1)
    index = {p: i + 1 for i, p in enumerate(ps)}
    map_old = [[index[p]] for p in old]
    rels = [substitute(w, map_old) for w in pure_relations(rank - 1)]
    kernel_map = [[index[(k, rank)]] for k in range(1, rank)]
    for p in old:
        g = index[p]
        action = artin_images(rank - 1, aij_braid(*p))
        for k in range(1, rank):
            h = index[(k, rank)]
            tail = substitute(action[k - 1], kernel_map)
            rels.append(free_reduce([-g, h, g] + list(reversed([-x for x in tail]))))
    return rels


def tuple_eval(word: Sequence[int], rows: Sequence[Sequence[Perm]]) -> tuple[Perm, ...]:
    return tuple(evaluate(word, [r[c] for r in rows]) for c in range(4))


def deletion_rows(target: Sequence[Perm]) -> tuple[tuple[Perm, ...], ...]:
    per_deletion = [[evaluate(w, target) for w in maps] for maps in EXPECTED_MAPS]
    return tuple(tuple(per_deletion[c][j] for c in range(4)) for j in range(6))


def basis_tuple(coordinate: int, value: Perm, identity: Perm) -> tuple[Perm, ...]:
    return tuple(value if i == coordinate else identity for i in range(4))


def apply_factor_auto(value: Sequence[Perm], source: Sequence[int],
                      conjugators: Sequence[Perm]) -> tuple[Perm, ...]:
    return tuple(conjugate(value[source[c] - 1], conjugators[c]) for c in range(4))


def rank_mod3(rows: Sequence[Sequence[int]]) -> int:
    matrix = [[x % 3 for x in r] for r in rows if any(x % 3 for x in r)]
    rank, col = 0, 0
    while rank < len(matrix) and col < (len(matrix[0]) if matrix else 0):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            col += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = 1 if matrix[rank][col] == 1 else 2
        matrix[rank] = [(scale * x) % 3 for x in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][col]:
                factor = matrix[i][col]
                matrix[i] = [(a - factor * b) % 3
                             for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
        col += 1
    return rank


GF8_MOD = 0b1011
P1 = tuple([(1, x) for x in range(8)] + [(0, 1)])


def gf8_mul(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= GF8_MOD
    return out & 7


def gf8_inv(a: int) -> int:
    return next(x for x in range(1, 8) if gf8_mul(a, x) == 1)


def matrix_action(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    out: list[int] = []
    for a, b in P1:
        x = gf8_mul(a, matrix[0][0]) ^ gf8_mul(b, matrix[1][0])
        y = gf8_mul(a, matrix[0][1]) ^ gf8_mul(b, matrix[1][1])
        line = (1, gf8_mul(y, gf8_inv(x))) if x else (0, 1)
        out.append(P1.index(line))
    return tuple(out)


def canonical_p() -> tuple[Perm, Perm, set[Perm]]:
    s = matrix_action(((1, 0), (1, 1)))
    t = matrix_action(((4, 3), (1, 5)))
    w = mul(s, inv(t))
    x = power(w, 2)
    y = mul(mul(inv(s), x), s)
    return x, y, closure((x, y), 504)


def make_g9() -> tuple[Perm, Perm, set[Perm]]:
    n = 9
    r = tuple(list(range(1, n)) + [0])
    s = tuple((n - j) % n for j in range(n))

    def translated(p: Perm, block: int) -> Perm:
        out = list(range(3 * n)); offset = block * n
        for i in range(n):
            out[offset + i] = offset + p[i]
        return tuple(out)

    sr = mul(s, r)
    x = mul(mul(translated(r, 0), translated(s, 1)), translated(s, 2))
    y = mul(mul(translated(sr, 0), translated(r, 1)), translated(sr, 2))
    return x, y, closure((x, y), 2916)


def quotient_image_order(group: set[Perm], derived: set[Perm],
                         tuple_generators: Sequence[Sequence[Perm]]) -> int:
    lookup: dict[Perm, int] = {}
    representatives: list[Perm] = []
    for g in group:
        if g in lookup:
            continue
        idx = len(representatives)
        representatives.append(g)
        for d in derived:
            lookup[mul(d, g)] = idx
    require(len(representatives) == 4 and len(lookup) == len(group), "G9 quotient cosets")
    table = [[lookup[mul(a, b)] for b in representatives] for a in representatives]
    gens = [tuple(lookup[x] for x in value) for value in tuple_generators]
    identity = tuple(lookup[one(27)] for _ in range(4))

    def tmul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(table[x][y] for x, y in zip(a, b))

    seen, queue = {identity}, deque([identity])
    while queue:
        a = queue.popleft()
        for g in gens:
            b = tmul(a, g)
            if b not in seen:
                seen.add(b); queue.append(b)
    return len(seen)


def h9_structure(hrows: Sequence[Sequence[Perm]], gx: Perm, gy: Perm,
                 ggroup: set[Perm]) -> dict[str, Any]:
    derived = derived_two(gx, gy, 2916)
    require(len(derived) == 729, "independent G9 derived order")
    dbasis: list[Perm] = []
    generated = {one(27)}
    for value in derived:
        if value in generated or order(value) != 9:
            continue
        trial = closure(dbasis + [value], 729)
        if len(trial) == 9 * len(generated):
            dbasis.append(value); generated = trial
        if len(generated) == 729:
            break
    require(len(dbasis) == 3 and generated == derived and
            all(mul(a, b) == mul(b, a) for a in dbasis for b in dbasis),
            "independent G9' = C9^3")
    coordinates: dict[Perm, tuple[int, int, int]] = {}
    for a, b, c in itertools.product(range(9), repeat=3):
        value = mul(mul(power(dbasis[0], a), power(dbasis[1], b)), power(dbasis[2], c))
        require(value not in coordinates, "G9 derived coordinate collision")
        coordinates[value] = (a, b, c)
    require(set(coordinates) == derived, "G9 derived coordinate coverage")

    tuples = [tuple(value) for value in hrows]

    def t_mul(a: Sequence[Perm], b: Sequence[Perm]) -> tuple[Perm, ...]:
        return tuple(mul(x, y) for x, y in zip(a, b))

    def t_inv(a: Sequence[Perm]) -> tuple[Perm, ...]:
        return tuple(inv(x) for x in a)

    def t_comm(a: Sequence[Perm], b: Sequence[Perm]) -> tuple[Perm, ...]:
        return t_mul(t_mul(t_mul(t_inv(a), t_inv(b)), a), b)

    def vector(a: Sequence[Perm]) -> tuple[int, ...]:
        require(all(x in coordinates for x in a), "H9 commutator outside (G9')^4")
        return tuple(v % 3 for x in a for v in coordinates[x])

    seeds = [t_comm(tuples[i], tuples[j]) for i in range(6) for j in range(i)]
    reps: list[tuple[Perm, ...]] = []
    vectors: list[tuple[int, ...]] = []
    queue: deque[tuple[Perm, ...]] = deque()
    for value in seeds:
        v = vector(value)
        if rank_mod3(vectors + [v]) > rank_mod3(vectors):
            reps.append(value); vectors.append(v); queue.append(value)
    attempts = 0
    while queue and rank_mod3(vectors) < 12:
        value = queue.popleft()
        for g in tuples:
            candidate = t_mul(t_mul(t_inv(g), value), g)
            attempts += 1
            require(attempts <= 72, "H9 Nakayama action cap")
            v = vector(candidate)
            if rank_mod3(vectors + [v]) > rank_mod3(vectors):
                reps.append(candidate); vectors.append(v); queue.append(candidate)
    require(rank_mod3(vectors) == 12, "H9 Nakayama rank")
    require(all(rank_mod3(vectors + [vector(t_mul(t_mul(t_inv(g), value), g))]) == 12
                for value in reps for g in tuples), "H9 module invariance")
    quotient_order = quotient_image_order(ggroup, derived, tuples)
    require(quotient_order == 32, "H9 abelian quotient image order")
    return {"derived_order": 3 ** 24, "quotient_order": quotient_order,
            "order": (3 ** 24) * quotient_order, "solvable": True,
            "nakayama_rank": 12, "attempts": attempts}


@lru_cache(maxsize=1)
def context() -> dict[str, Any]:
    maps = pinned_json("deletion_fixture")
    a1 = pinned_json("a5_marking")
    a12 = pinned_json("a5_settled_extension")
    require(maps["schema"] == "d972-b4-marity-reduction-maps/v1" and
            maps["status"] == "PROVED_BY_CANONICAL_STRAND_FORGETTING" and
            [x["generator_images"] for x in maps["maps"]] == EXPECTED_MAPS and
            [x["deleted_strand"] for x in maps["maps"]] == [1, 2, 3, 4],
            "frozen deletion fixture")
    require(a1["target_definition"]["marking"]["X"] == "a t^{-1} = (1 3 2 4 5)" and
            a1["target_definition"]["marking"]["Y"] == "t X t^{-1} = (1 3 4 5 2)" and
            a1["target_definition"]["quotient"] == "A5" and
            a12["aut_group"]["size"] == 120, "frozen A5 marking")
    for key, (rel, expected) in PINS.items():
        got, _ = sha_bytes(ROOT / rel)
        require(got == expected, f"{key} pin")

    x = cycle(5, (1, 3, 2, 4, 5)); y = cycle(5, (1, 3, 4, 5, 2))
    z = mul(inv(x), inv(y)); a5 = closure((x, y), 60)
    require(len(a5) == 60 and len(derived_two(x, y, 60)) == 60 and
            all(len(normal_closure(g, (x, y), 60)) == 60
                for g in a5 if g != one(5)), "A5 order/simple/perfect")
    rrows = deletion_rows((x, z, y))
    relations = pure_relations(4)
    require(len(relations) == 11 and all(
        artin_images(4, expand_pure(4, rel)) == [[i] for i in range(1, 5)]
        for rel in relations), "independent PB4 presentation")
    require(all(all(v == one(5) for v in tuple_eval(rel, rrows)) for rel in relations),
            "rhoA PB4 relation replay")

    s5 = list(itertools.permutations(range(5)))
    action_data = []
    for sigma, formulas in enumerate(ARTIN, 1):
        for j, p in enumerate(pairs(4)):
            lhs = artin_images(4, [-sigma] + aij_braid(*p) + [sigma])
            rhs = artin_images(4, expand_pure(4, formulas[j]))
            require(lhs == rhs, "faithful source Artin orientation")
        acted = [tuple_eval(w, rrows) for w in formulas]
        source: list[int] = []
        conjugators: list[Perm] = []
        for output in range(4):
            matches = [(source_coord + 1, t)
                       for source_coord in range(4) for t in s5
                       if all(acted[j][output] == conjugate(rrows[j][source_coord], t)
                              for j in range(6))]
            require(len(matches) == 1, "unique A5 factor transport")
            source.append(matches[0][0]); conjugators.append(matches[0][1])
        expected = list(range(1, 5)); expected[sigma - 1], expected[sigma] = expected[sigma], expected[sigma - 1]
        require(source == expected, "standard adjacent factor action")
        action_data.append({"source": source, "conjugators": conjugators, "acted": acted})

    basis = [basis_tuple(c, value, one(5)) for c in range(4) for value in (x, y)]
    for value in basis:
        phi = lambda k, v: apply_factor_auto(v, action_data[k]["source"], action_data[k]["conjugators"])
        require(phi(0, phi(1, phi(0, value))) == phi(1, phi(0, phi(1, value))), "factor braid 12")
        require(phi(1, phi(2, phi(1, value))) == phi(2, phi(1, phi(2, value))), "factor braid 23")
        require(phi(0, phi(2, value)) == phi(2, phi(0, value)), "factor commutation 13")

    px, py, pgroup = canonical_p(); pz = mul(inv(px), inv(py))
    gx, gy, ggroup = make_g9(); gz = mul(inv(gx), inv(gy))
    prows = deletion_rows((px, pz, py)); grows = deletion_rows((gx, gz, gy))
    require(len(pgroup) == 504 and len(derived_two(px, py, 504)) == 504, "PSL(2,8) factor")
    require(len(ggroup) == 2916, "G9 order")
    hstruct = h9_structure(grows, gx, gy, ggroup)
    return {"X": x, "Y": y, "Z": z, "A5": a5, "rho": rrows,
            "relations": relations, "actions": action_data,
            "PX": px, "PY": py, "PZ": pz, "P": pgroup, "prows": prows,
            "GX": gx, "GY": gy, "GZ": gz, "G9": ggroup, "grows": grows,
            "hstruct": hstruct}


def expected_support(rows: Sequence[Sequence[Perm]], ambient: Sequence[Perm],
                     cap: int, degree: int) -> list[dict[str, Any]]:
    out = []
    identity = one(degree)
    for coordinate, word in enumerate(SUPPORT_WORDS, 1):
        value = tuple_eval(word, rows)
        require(value[coordinate - 1] != identity and all(
            value[j] == identity for j in range(4) if j != coordinate - 1),
            "single-support value")
        norder = len(normal_closure(value[coordinate - 1], ambient, cap))
        require(norder == cap, "single-support normal closure")
        out.append({"coordinate": coordinate, "source_word": word,
                    "images": [row(x) for x in value], "nontrivial": True,
                    "normal_closure_order": norder})
    return out


def validate(data: dict[str, Any]) -> str:
    require(data.get("schema") == SCHEMA, "schema")
    expected_pins = {key: {"path": rel, "sha256": sha,
                           "bytes": sha_bytes(ROOT / rel)[1]}
                     for key, (rel, sha) in PINS.items()}
    require(data.get("pins") == expected_pins, "pinned source binding")
    token = data.get("terminal_token")
    unknown_phases = {
        "FC8_UNKNOWN_A5": {"A5"},
        "FC8_UNKNOWN_RHOA_RELATIONS": {"rhoA_relations"},
        "FC8_UNKNOWN_RHOA_SURJECTIVITY": {"rhoA_projections", "rhoA_single_support", "rhoA_normal_closure"},
        "FC8_UNKNOWN_B4_ACTION": {"faithful_Artin", "factor_transport", "factor_permutation",
                                  "induced_relations", "factor_transitivity"},
        "FC8_UNKNOWN_Q0_CONTRACT": {"Q0_factors", "Q0_P4_projection",
                                     "Q0_P4_single_support", "Q0_P4_normal_closure",
                                     "Q0_prime_support"},
        "FC8_UNKNOWN_CB3_COUPLING": {"FC8_double_star_CB3"},
    }
    if token != TERMINAL:
        require(token in unknown_phases and data.get("status") == token and
                data.get("terminal") is False and data.get("phase") in unknown_phases[token] and
                isinstance(data.get("detail"), str) and bool(data["detail"]) and
                data.get("chief_factor_claimed") is False and data.get("B4_B_claimed") is False and
                set(data) == {"schema", "status", "terminal_token", "terminal", "pins",
                              "phase", "detail", "chief_factor_claimed", "B4_B_claimed"},
                "precise fail-closed UNKNOWN receipt")
        return token
    require(data.get("status") == TERMINAL, "terminal relabel")
    ctx = context()

    source = data["source_contract"]
    require(source == {"group": "PB4", "generator_order": LABELS,
                       "deletion_target_order": ["y12", "y13", "y23"],
                       "free_A5_images": ["X", "X^-1 Y^-1", "Y"],
                       "deletion_maps": EXPECTED_MAPS}, "source/deletion contract")
    a5 = data["a5"]
    require(a5 == {"name": "A5", "degree": 5, "order": 60, "simple": True,
                   "perfect": True, "automorphism_group": "S5",
                   "automorphism_group_order": 120,
                   "X": row(ctx["X"]), "Y": row(ctx["Y"]), "Z": row(ctx["Z"])},
            "A5 receipt")

    pres = data["pb4_presentation"]
    require(pres["method"] == "recursive Fadell-Neuwirth presentation plus faithful Artin replay" and
            pres["pairs"] == [list(p) for p in pairs(4)] and
            pres["relation_count"] == 11 and pres["relations"] == ctx["relations"] and
            pres["relation_images_identity"] is True, "PB4 presentation receipt")
    expected_rho_rows = [[row(x) for x in values] for values in ctx["rho"]]
    rho = data["rhoA"]
    require(rho["marked_images"] == expected_rho_rows, "rhoA marked rows")
    projection_orders = [len(closure([values[c] for values in ctx["rho"]], 60)) for c in range(4)]
    require(rho["projection_orders"] == projection_orders == [60] * 4,
            "rhoA coordinate projections")
    support = expected_support(ctx["rho"], (ctx["X"], ctx["Y"]), 60, 5)
    require(rho["single_support_witnesses"] == support and
            rho["no_A5four_enumeration"] is True and rho["image_is_A5_four"] is True,
            "rhoA full direct-product certificate")

    action = data["b4_action"]
    require(action["orientation"] == "c_(sigma_i^-1): value maps to sigma_i^-1 value sigma_i" and
            action["faithful_source_action_replay"] is True and
            action["exact_transport_all_six_rows"] is True and
            action["induced_braid_relations"] is True and
            action["induced_distant_commutation"] is True and
            action["factor_action_group_order"] == 24 and
            action["factor_action_standard_S4"] is True and
            action["factor_action_transitive"] is True, "B4 action gates")
    require(len(action["generators"]) == 3, "B4 action generator count")
    character_pairs = []
    for sigma, (record, actual) in enumerate(zip(action["generators"], ctx["actions"]), 1):
        conjugators = actual["conjugators"]
        outer = [parity(x) for x in conjugators]
        factor = actual["source"]
        factor_bit = parity(tuple(x - 1 for x in factor))
        pair = [sum(outer) % 2, factor_bit]
        character_pairs.append(pair)
        require(record == {"sigma_index": sigma,
                           "orientation": "sigma_i^-1 * value * sigma_i",
                           "source_generator_images": ARTIN[sigma - 1],
                           "source_coordinate_by_output": factor,
                           "factor_permutation": factor,
                           "conjugators_S5": [row(x) for x in conjugators],
                           "exact_transport_images": [[row(x) for x in v]
                                                      for v in actual["acted"]],
                           "outer_A5_bits": outer,
                           "wreath_abelianization_pair": pair},
                f"Artin transport sigma{sigma}")
    nonzero = [tuple(x) for x in character_pairs if x != [0, 0]]
    cb_order = 1 if not nonzero else (2 if all(x == nonzero[0] for x in nonzero) else 4)
    require(cb_order <= 2, "independent CB-3 cyclicity")
    cb = data["fc8_double_star_cb3"]
    require(cb == {"target": "Out(A5)^4 semidirect S4 = C2 wreath S4",
                   "wreath_abelianization": "C2^2: total outer parity and S4 sign",
                   "generator_character_pairs": character_pairs,
                   "image_order": cb_order, "image_cyclic": True,
                   "characters_independent": False,
                   "q_abelianization_cyclic_premise": True,
                   "checker_must_recompute_parities": True}, "FC-8** CB-3 receipt")

    rho0 = data["rho0"]
    horder = ctx["hstruct"]["order"]
    qorder = (504 ** 4) * horder
    require(rho0["name"] == "frozen actual coarse B4 roof Q0=P^4 x H9" and
            int(rho0["order_decimal"]) == qorder and rho0["prime_support"] == [2, 3, 7],
            "Q0 order/prime support")
    require(rho0["P"] == {"name": "PSL(2,8)", "degree": 9, "order": 504,
                           "perfect": True, "simple": True, "prime_support": [2, 3, 7],
                           "X": row(ctx["PX"]), "Y": row(ctx["PY"])}, "P order/type")
    require(rho0["G9"] == {"degree": 27, "order": 2916, "solvable": True,
                            "derived_series_orders": [2916, 729, 1],
                            "X": row(ctx["GX"]), "Y": row(ctx["GY"])}, "G9 contract")
    expected_grows = [[row(x) for x in values] for values in ctx["grows"]]
    require(rho0["H9"] == {"degree": 108, "order_decimal": str(horder),
                            "solvable": True, "derived_order_decimal": str(3 ** 24),
                            "abelian_quotient_order": 32, "prime_support": [2, 3],
                            "marked_blocks": expected_grows,
                            "construction": "image of the six marked PB4 generators in G9^4",
                            "checker_method": "G9-derived C9^3 coordinates, mod-3 Nakayama rank 12, and quotient image order 32"},
            "H9 solvability/order/prime support")
    expected_prows = [[row(x) for x in values] for values in ctx["prows"]]
    p_support = expected_support(ctx["prows"], (ctx["PX"], ctx["PY"]), 504, 9)
    # P witness schema omits the redundant nontrivial boolean.
    for item in p_support:
        item.pop("nontrivial")
    p_projection_orders = [len(closure([values[c] for values in ctx["prows"]], 504))
                           for c in range(4)]
    require(rho0["P4"] == {"order_decimal": str(504 ** 4),
                            "projection_orders": p_projection_orders,
                            "marked_blocks": expected_prows,
                            "single_support_witnesses": p_support,
                            "perfect": True, "image_is_P_four": True}, "P4 full certificate")
    bindings = [{"source_generator": LABELS[j], "P4_blocks": expected_prows[j],
                 "H9_blocks": expected_grows[j], "A5_four_blocks": expected_rho_rows[j]}
                for j in range(6)]
    require(rho0["marked_same_source_bindings"] == bindings and
            rho0["B4_normal_kernel_frozen_roof_premise"] is True,
            "rho0/rhoA same-source binding")

    goursat = {"joint_map_source": "PB4 with the same six canonical marked generators",
               "rho0_surjective": True,
               "rho0_projection_P4_surjective_by_single_support": True,
               "rho0_projection_H9_surjective_by_definition": True,
               "rho0_P4_H9_common_quotient_trivial": True,
               "rho0_product_reason": "P^4 is perfect and H9 is solvable, so a common quotient is both perfect and solvable and hence trivial",
               "rhoA_surjective": True,
               "no_nontrivial_common_quotient_Q0_A5four": True,
               "no_common_reason": "every nontrivial quotient of A5^4 has order divisible by 5, while 5 does not divide |Q0|",
               "theorem": "Goursat subdirect-product lemma",
               "joint_image_is_full_Q0_times_A5four": True}
    require(rho0["product_certificate"] == goursat and data["goursat"] == goursat,
            "independent Goursat premises")
    require(qorder % 5 != 0 and all(len(normal_closure(
        tuple_eval(word, ctx["rho"])[c], (ctx["X"], ctx["Y"]), 60)) == 60
        for c, word in enumerate(SUPPORT_WORDS)), "no-common-quotient arithmetic")

    chief = data["chief_factor"]
    require(chief == {"K_definition": "K = ker(rho0) intersection ker(rhoA)",
                      "M_definition": "M = ker(rho0)",
                      "restriction_kernel": "ker(rhoA restricted to M) = K",
                      "restriction_surjective_by_joint_product": True,
                      "first_isomorphism": "M/K isomorphic to A5^4",
                      "S": "A5", "t": 4, "factor_order": 60,
                      "direct_power_normal_subgroup_lemma": "every normal subgroup of a direct power of a nonabelian simple group is a product of coordinate factors",
                      "finite_premises": {"nonabelian": True, "simple": True, "four_factors": True},
                      "B4_factor_action_transitive": True,
                      "B4_stable_factor_subsets": [[], [1, 2, 3, 4]],
                      "B4_chief": True,
                      "registered_factor_isolatedness_used_as_premise": False,
                      "isolated_audit_window_source": "Corollary 3.5 (FV-5); not computed here"},
            "B4-chief reconstruction")
    require(data["missing_ledger"] == {
        "FV5_registered_window_isolation_required": False,
        "FV5_audit_window_isolated_by_Corollary_3_5": True,
        "D4_five_primary_friendly": "MISSING", "D6_five_primary_friendly": "MISSING",
        "five_primary_reason": "5 divides |A5| and introduces a new friendly-condition prime",
        "K_isolatedness": "NOT_ESTABLISHED_AND_NOT_REQUIRED_BY_FV5",
        "OBS_NA": "NOT_SUPPLIED", "D1": "NOT_SUPPLIED", "NA_5": "NOT_SUPPLIED",
        "full_verbal_tower_switch": "NOT_RECOMMENDED_AND_NOT_USED"}, "missing ledger")
    perf = data["performance"]
    require(isinstance(perf["runtime_ms"], int) and perf["runtime_ms"] >= 0 and
            perf["Elements_A5four_calls"] == 0 and perf["A5four_Cayley_tables"] == 0 and
            perf["generic_A5four_group_size_calls"] == 0 and
            perf["closures_inside_A5"] == 4 and perf["closures_inside_P"] == 4 and
            perf["bounded_S5_elements"] == 120 and perf["coarse_core_reads"] == 1,
            "performance contract")
    require(data["implication"] ==
            "For K=M intersection ker(rhoA), M/K is a B4-chief factor A5^4; no B4-B conclusion",
            "implication boundary")
    return TERMINAL


def fixture() -> dict[str, Any]:
    """Build a valid checker-owned receipt; this never calls producer code."""
    ctx = context()
    pins = {key: {"path": rel, "sha256": sha, "bytes": sha_bytes(ROOT / rel)[1]}
            for key, (rel, sha) in PINS.items()}
    support_a = expected_support(ctx["rho"], (ctx["X"], ctx["Y"]), 60, 5)
    support_p = expected_support(ctx["prows"], (ctx["PX"], ctx["PY"]), 504, 9)
    for item in support_p:
        item.pop("nontrivial")
    action_rows = []
    chars = []
    for sigma, actual in enumerate(ctx["actions"], 1):
        outer = [parity(x) for x in actual["conjugators"]]
        pair = [sum(outer) % 2, parity(tuple(x - 1 for x in actual["source"]))]
        chars.append(pair)
        action_rows.append({"sigma_index": sigma,
            "orientation": "sigma_i^-1 * value * sigma_i",
            "source_generator_images": ARTIN[sigma - 1],
            "source_coordinate_by_output": actual["source"],
            "factor_permutation": actual["source"],
            "conjugators_S5": [row(x) for x in actual["conjugators"]],
            "exact_transport_images": [[row(x) for x in v] for v in actual["acted"]],
            "outer_A5_bits": outer, "wreath_abelianization_pair": pair})
    nz = [tuple(x) for x in chars if x != [0, 0]]
    cb_order = 1 if not nz else (2 if all(x == nz[0] for x in nz) else 4)
    prows = [[row(x) for x in v] for v in ctx["prows"]]
    grows = [[row(x) for x in v] for v in ctx["grows"]]
    arows = [[row(x) for x in v] for v in ctx["rho"]]
    horder = ctx["hstruct"]["order"]
    goursat = {"joint_map_source": "PB4 with the same six canonical marked generators",
        "rho0_surjective": True, "rho0_projection_P4_surjective_by_single_support": True,
        "rho0_projection_H9_surjective_by_definition": True,
        "rho0_P4_H9_common_quotient_trivial": True,
        "rho0_product_reason": "P^4 is perfect and H9 is solvable, so a common quotient is both perfect and solvable and hence trivial",
        "rhoA_surjective": True, "no_nontrivial_common_quotient_Q0_A5four": True,
        "no_common_reason": "every nontrivial quotient of A5^4 has order divisible by 5, while 5 does not divide |Q0|",
        "theorem": "Goursat subdirect-product lemma", "joint_image_is_full_Q0_times_A5four": True}
    return {"schema": SCHEMA, "status": TERMINAL, "terminal_token": TERMINAL, "pins": pins,
        "source_contract": {"group": "PB4", "generator_order": LABELS,
            "deletion_target_order": ["y12", "y13", "y23"],
            "free_A5_images": ["X", "X^-1 Y^-1", "Y"], "deletion_maps": EXPECTED_MAPS},
        "a5": {"name": "A5", "degree": 5, "order": 60, "simple": True, "perfect": True,
            "automorphism_group": "S5", "automorphism_group_order": 120,
            "X": row(ctx["X"]), "Y": row(ctx["Y"]), "Z": row(ctx["Z"])},
        "pb4_presentation": {"method": "recursive Fadell-Neuwirth presentation plus faithful Artin replay",
            "pairs": [list(p) for p in pairs(4)], "relation_count": 11,
            "relations": ctx["relations"], "relation_images_identity": True},
        "rhoA": {"marked_images": arows, "projection_orders": [60] * 4,
            "single_support_witnesses": support_a, "no_A5four_enumeration": True,
            "image_is_A5_four": True},
        "b4_action": {"orientation": "c_(sigma_i^-1): value maps to sigma_i^-1 value sigma_i",
            "generators": action_rows, "faithful_source_action_replay": True,
            "exact_transport_all_six_rows": True, "induced_braid_relations": True,
            "induced_distant_commutation": True, "factor_action_group_order": 24,
            "factor_action_standard_S4": True, "factor_action_transitive": True},
        "fc8_double_star_cb3": {"target": "Out(A5)^4 semidirect S4 = C2 wreath S4",
            "wreath_abelianization": "C2^2: total outer parity and S4 sign",
            "generator_character_pairs": chars, "image_order": cb_order, "image_cyclic": True,
            "characters_independent": False, "q_abelianization_cyclic_premise": True,
            "checker_must_recompute_parities": True},
        "rho0": {"name": "frozen actual coarse B4 roof Q0=P^4 x H9",
            "order_decimal": str((504 ** 4) * horder), "prime_support": [2, 3, 7],
            "P": {"name": "PSL(2,8)", "degree": 9, "order": 504, "perfect": True,
                "simple": True, "prime_support": [2, 3, 7], "X": row(ctx["PX"]), "Y": row(ctx["PY"])},
            "G9": {"degree": 27, "order": 2916, "solvable": True,
                "derived_series_orders": [2916, 729, 1], "X": row(ctx["GX"]), "Y": row(ctx["GY"])},
            "H9": {"degree": 108, "order_decimal": str(horder), "solvable": True,
                "derived_order_decimal": str(3 ** 24), "abelian_quotient_order": 32,
                "prime_support": [2, 3], "marked_blocks": grows,
                "construction": "image of the six marked PB4 generators in G9^4",
                "checker_method": "G9-derived C9^3 coordinates, mod-3 Nakayama rank 12, and quotient image order 32"},
            "P4": {"order_decimal": str(504 ** 4), "projection_orders": [504] * 4,
                "marked_blocks": prows, "single_support_witnesses": support_p,
                "perfect": True, "image_is_P_four": True},
            "marked_same_source_bindings": [{"source_generator": LABELS[j],
                "P4_blocks": prows[j], "H9_blocks": grows[j], "A5_four_blocks": arows[j]}
                for j in range(6)],
            "B4_normal_kernel_frozen_roof_premise": True, "product_certificate": goursat},
        "goursat": goursat,
        "chief_factor": {"K_definition": "K = ker(rho0) intersection ker(rhoA)",
            "M_definition": "M = ker(rho0)",
            "restriction_kernel": "ker(rhoA restricted to M) = K",
            "restriction_surjective_by_joint_product": True,
            "first_isomorphism": "M/K isomorphic to A5^4", "S": "A5", "t": 4,
            "factor_order": 60,
            "direct_power_normal_subgroup_lemma": "every normal subgroup of a direct power of a nonabelian simple group is a product of coordinate factors",
            "finite_premises": {"nonabelian": True, "simple": True, "four_factors": True},
            "B4_factor_action_transitive": True, "B4_stable_factor_subsets": [[], [1, 2, 3, 4]],
            "B4_chief": True, "registered_factor_isolatedness_used_as_premise": False,
            "isolated_audit_window_source": "Corollary 3.5 (FV-5); not computed here"},
        "missing_ledger": {"FV5_registered_window_isolation_required": False,
            "FV5_audit_window_isolated_by_Corollary_3_5": True,
            "D4_five_primary_friendly": "MISSING", "D6_five_primary_friendly": "MISSING",
            "five_primary_reason": "5 divides |A5| and introduces a new friendly-condition prime",
            "K_isolatedness": "NOT_ESTABLISHED_AND_NOT_REQUIRED_BY_FV5",
            "OBS_NA": "NOT_SUPPLIED", "D1": "NOT_SUPPLIED", "NA_5": "NOT_SUPPLIED",
            "full_verbal_tower_switch": "NOT_RECOMMENDED_AND_NOT_USED"},
        "performance": {"runtime_ms": 0, "Elements_A5four_calls": 0, "A5four_Cayley_tables": 0,
            "generic_A5four_group_size_calls": 0, "closures_inside_A5": 4,
            "closures_inside_P": 4, "bounded_S5_elements": 120, "coarse_core_reads": 1},
        "implication": "For K=M intersection ker(rhoA), M/K is a B4-chief factor A5^4; no B4-B conclusion"}


def self_test() -> None:
    good = fixture()
    validate(good)

    def swap_coordinate(d: dict[str, Any]) -> None:
        values = d["rhoA"]["marked_images"][0]
        values[0], values[2] = values[2], values[0]

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("deletion_letter", lambda d: d["source_contract"]["deletion_maps"][0][3].__setitem__(0, 2)),
        ("swapped_coordinate", swap_coordinate),
        ("support_image", lambda d: d["rhoA"]["single_support_witnesses"][0]["images"][0].__setitem__(0, 99)),
        ("artin_transport", lambda d: d["b4_action"]["generators"][0]["source_coordinate_by_output"].__setitem__(0, 1)),
        ("P_order", lambda d: d["rho0"]["P"].__setitem__("order", 503)),
        ("P_type", lambda d: d["rho0"]["P"].__setitem__("name", "A7")),
        ("H9_solvable", lambda d: d["rho0"]["H9"].__setitem__("solvable", False)),
        ("H9_order", lambda d: d["rho0"]["H9"].__setitem__("order_decimal", "1")),
        ("H9_prime", lambda d: d["rho0"]["H9"].__setitem__("prime_support", [2, 3, 5])),
        ("chief_t", lambda d: d["chief_factor"].__setitem__("t", 1)),
        ("cb3_character", lambda d: d["fc8_double_star_cb3"]["generator_character_pairs"].__setitem__(0, [1, 0])),
        ("terminal", lambda d: d.__setitem__("terminal_token", "FC8_UNKNOWN_MUTATED")),
    ]
    for name, mutate in mutations:
        bad = copy.deepcopy(good); mutate(bad)
        try:
            validate(bad)
        except Reject:
            continue
        raise AssertionError(f"mutation survived: {name}")
    print(f"D972_B4_FC8_CHECKER_SELFTEST_PASS mutations={len(mutations)} h9_nakayama_rank=12")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test(); return
    require(args.artifact is not None, "artifact path required")
    data = json.loads(Path(args.artifact).read_text(encoding="utf-8"))
    token = validate(data)
    if token == TERMINAL:
        print("FC8_A5_FOUR_CHECKER_PASS terminal=FC8_A5_FOUR_CHIEF_CROSSCHECKED "
              "S=A5 t=4 CB3=cyclic")
    else:
        print(f"FC8_A5_FOUR_CHECKER_PASS status={token} terminal=false")


if __name__ == "__main__":
    try:
        main()
    except (Reject, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"FC8_A5_FOUR_CHECKER_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
