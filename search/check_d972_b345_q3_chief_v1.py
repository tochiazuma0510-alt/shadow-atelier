#!/usr/bin/env python3
"""Independent checker for d972-b345-q-chief/v1.

The checker reconstructs the pure-braid presentations and all face/coface
words without importing the GAP producer.  GAP's ANUPQ maximal-quotient
algorithm remains an explicitly named external contract; the exported pc
collector and every homomorphism used downstream are replayed here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA = "d972-b345-q-chief/v1"
ROW18_SOURCE = Path("search/d972_b4_literal_row18_stage_v2.g")
ROW18_SHA = "8f8b429b5725b244a214cc6a4cf59daa186e4ee2d4d6eee6df18e580d88ef2a1"
ROW18_CHECKER = Path("search/check_d972_b4_literal_row18_stage_v2.py")
ROW18_CHECKER_SHA = "bf85cfd142f6c640e96af77aa5f580caa206439329d17ed18ac342ac6acdcd19"
PHASE2B = Path("search/certs/d972_phase2b_nonsplit_v1_20260813.json")
PHASE2B_SHA = "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9"
WORDS = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
CORE = Path("search/d972_d972core_c2six_intersection_v2.g")
CORE_SHA = "577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c"
FORMULA_SHA = "b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef"

ALLOWED_TERMINALS = {
    "B345_Q3_MANIFEST_READY_FOR_GHA",
    "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
    "B345_Q3_TYPED_SIGN_NONZERO_OBSTRUCTION",
    "B345_Q3_NO_ACTUAL_F3_CHIEF",
    "B345_Q3_MISSING_TYPED_M5",
    "B345_Q3_MISSING_TYPED_D2",
    "B345_Q3_MISSING_RELATIVE_HORN_EFFECTIVITY",
    "B345_Q3_MISSING_TYPED_COMPARISON_PHI",
    "B345_Q3_UNKNOWN_RESOURCE",
}


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


Perm = tuple[int, ...]


def perm_from_row(row: Sequence[int], degree: int) -> Perm:
    require(len(row) == degree and all(isinstance(x, int) for x in row),
            "permutation row width/type")
    p = tuple(x - 1 for x in row)
    require(set(p) == set(range(degree)), "permutation row is not bijective")
    return p


def perm_one(degree: int) -> Perm:
    return tuple(range(degree))


def perm_mul(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degree mismatch")
    # GAP right action: i^(a*b)=(i^a)^b.
    return tuple(b[a[i]] for i in range(len(a)))


def perm_inv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, image in enumerate(a):
        out[image] = i
    return tuple(out)


def perm_order(a: Perm) -> int:
    seen = [False] * len(a)
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


def elem_eval(word: Sequence[int], images: Sequence[Any], identity: Any,
              mul: Any, inverse: Any) -> Any:
    out = identity
    for letter in word:
        require(1 <= abs(letter) <= len(images), "element word index")
        value = images[abs(letter) - 1]
        out = mul(out, value if letter > 0 else inverse(value))
    return out


def elem_power(value: Any, exponent: int, identity: Any, mul: Any, inverse: Any) -> Any:
    if exponent < 0:
        return elem_power(inverse(value), -exponent, identity, mul, inverse)
    out, base, n = identity, value, exponent
    while n:
        if n & 1:
            out = mul(out, base)
        base = mul(base, base)
        n >>= 1
    return out


def rank_mod3(rows: Sequence[Sequence[int]]) -> int:
    a = [[x % 3 for x in row] for row in rows if any(x % 3 for x in row)]
    if not a:
        return 0
    rank, col = 0, 0
    width = len(a[0])
    while rank < len(a) and col < width:
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = 1 if a[rank][col] == 1 else 2
        a[rank] = [(inv * x) % 3 for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col]:
                c = a[i][col]
                a[i] = [(x - c * y) % 3 for x, y in zip(a[i], a[rank])]
        rank += 1
        col += 1
    return rank


def pp(values: Sequence[Any], identity: Any, mul: Any) -> Any:
    require(bool(values), "empty paper product")
    out = identity
    for value in reversed(values):
        out = mul(out, value)
    return out


def paper_conjugate(value: Any, y: Any, identity: Any, mul: Any, inverse: Any) -> Any:
    # GAP producer: PP([value^-1,y,value]); PP reverses the displayed list, so
    # the actual element is value*y*value^-1.
    return pp([inverse(value), y, value], identity, mul)


def context_cache(contexts: Sequence[Sequence[Any]], words: Sequence[Sequence[int]],
                  identity: Any, mul: Any, inverse: Any) -> list[list[Any]]:
    return [[elem_eval(word, pair, identity, mul, inverse) for word in words]
            for pair in contexts]


def context_base(word: Sequence[int], contexts: Sequence[Sequence[Any]],
                 identity: Any, mul: Any, inverse: Any) -> list[Any]:
    return [elem_eval(word, pair, identity, mul, inverse) for pair in contexts]


def context_values(base: Sequence[Any], correction: Sequence[Sequence[Any]],
                   index: int, mul: Any) -> list[Any]:
    return [mul(base[j], correction[j][index]) for j in range(len(base))]


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(isinstance(x, int) and x != 0, "invalid signed free letter")
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return reduce_word(-x for x in reversed(word))


def word_eval(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for x in word:
        require(1 <= abs(x) <= len(images), "signed map index out of range")
        out.extend(images[x - 1] if x > 0 else inv_word(images[-x - 1]))
        out = reduce_word(out)
    return out


def marked_sub(word: Sequence[int], left: Sequence[int], right: Sequence[int]) -> list[int]:
    return word_eval(word, [list(left), [], [], list(right), [], []])


def gt_compose_m0(left: Sequence[int], right: Sequence[int]) -> list[int]:
    x_image = [1]
    y_image = reduce_word(list(left) + [2] + inv_word(left))
    return reduce_word(word_eval(right, [x_image, y_image]) + list(left))


def source_words_m0(f: Sequence[int]) -> list[list[int]]:
    ff = word_eval(f, [[1], [4]])
    g = word_eval(f, [[1], [2]])
    gs = word_eval(f, [[4], [5]])
    f1234 = word_eval(f, [[4, 2], [6]])
    x123 = [2, 1]
    h = word_eval(f, [x123, [3]])
    middle = word_eval(f, [[2, 1], [6, 5]])
    return [
        [1],
        reduce_word(inv_word(g) + [2] + g),
        reduce_word(inv_word(ff) + inv_word(h) + [3] + h + ff),
        reduce_word(inv_word(ff) + [4] + ff),
        reduce_word(inv_word(ff) + inv_word(middle) + inv_word(gs) + [5] +
                    gs + middle + ff),
        reduce_word(inv_word(f1234) + [6] + f1234),
    ]


def dtilde_word(word: Sequence[int]) -> list[int]:
    marked = [(1 if n > 0 else -1) * (1, 4)[abs(n) - 1] for n in word]
    x15, x45 = [-3, -2, -1], [-6, -5, -3]
    a = marked_sub(marked, x45, [6])
    b = marked_sub(marked, [1], x15)
    c = marked_sub(marked, [4], [6])
    d = marked_sub(marked, x45, x15)
    e = marked_sub(marked, [1], [4])
    return reduce_word(inv_word(a) + inv_word(b) + c + d + e)


def f2_exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum(1 if x > 0 else -1 for x in word if abs(x) == i) for i in (1, 2)]


def exponent_matrix(words: Sequence[Sequence[int]], width: int) -> list[list[int]]:
    return [[sum(1 if x > 0 else -1 for x in word if abs(x) == j)
             for j in range(1, width + 1)] for word in words]


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    require(1 <= i < rank, "Artin generator out of range")
    images = [[j] for j in range(1, rank + 1)]
    if letter > 0:
        images[i - 1] = [i, i + 1, -i]
        images[i] = [i]
    else:
        images[i - 1] = [i + 1]
        images[i] = [-(i + 1), i, i + 1]
    return images


def artin_images(rank: int, braid_word: Sequence[int]) -> list[list[int]]:
    images = [[j] for j in range(1, rank + 1)]
    for letter in braid_word:
        step = artin_step(rank, letter)
        images = [word_eval(w, step) for w in images]
    return images


def artin_identity(rank: int, braid_word: Sequence[int]) -> bool:
    return artin_images(rank, braid_word) == [[j] for j in range(1, rank + 1)]


def pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i + 1, rank + 1)]


def pair_index(rank: int, pair: Sequence[int]) -> int:
    try:
        return pairs(rank).index(list(pair)) + 1
    except ValueError as exc:
        raise Reject(f"bad pair {pair} at rank {rank}") from exc


def aij_braid(i: int, j: int) -> list[int]:
    return list(range(j - 1, i, -1)) + [i, i] + [-k for k in range(i + 1, j)]


def expand_pure(rank: int, word: Sequence[int]) -> list[int]:
    return word_eval(word, [aij_braid(i, j) for i, j in pairs(rank)])


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    old_pairs = pairs(rank - 1)
    old_to_new = [[pair_index(rank, p)] for p in old_pairs]
    rels = [word_eval(w, old_to_new) for w in pure_relations(rank - 1)]
    kernel_images = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        g = pair_index(rank, [i, j])
        action = artin_images(rank - 1, aij_braid(i, j))
        for k in range(1, rank):
            h = pair_index(rank, [k, rank])
            rhs = word_eval(action[k - 1], kernel_images)
            rels.append(reduce_word([-g, h, g] + inv_word(rhs)))
    return rels


def braid_kernel_certificate(rank: int) -> dict[str, Any]:
    rels: list[list[int]] = []
    for i in range(1, rank - 1):
        rels.append([i, i + 1, i, -(i + 1), -i, -(i + 1)])
    for i in range(1, rank):
        for j in range(i + 2, rank):
            rels.append([i, j, -i, -j])
    adjacent = []
    for i in range(1, rank):
        row = list(range(1, rank + 1))
        row[i - 1], row[i] = row[i], row[i - 1]
        adjacent.append(row)
    pure_words = [aij_braid(i, j) for i, j in pairs(rank)]
    return {
        "rank": rank,
        "braid_generator_count": rank - 1,
        "braid_relations": rels,
        "symmetric_generator_images": adjacent,
        "symmetric_image_order": math.factorial(rank),
        "map_onto": True,
        "pure_Aij_braid_words": pure_words,
        "pure_Aij_permutations_identity": True,
        "kernel_identification": (
            "Artin pure braid kernel, presented independently by the replayed "
            "Fadell-Neuwirth semidirect presentation"
        ),
        "no_Reidemeister_Schreier_conversion": True,
    }


def presentation(rank: int) -> dict[str, Any]:
    ps = pairs(rank)
    rels = pure_relations(rank)
    require(all(artin_identity(rank, expand_pure(rank, w)) for w in rels),
            f"faithful Artin replay failed at PB{rank}")
    return {
        "pairs": ps,
        "labels": [f"a{i}{j}" for i, j in ps],
        "relations": rels,
        "artin_words": [aij_braid(i, j) for i, j in ps],
        "fp_unit_words": [[i] for i in range(1, len(ps) + 1)],
    }


def coface_generator(rank: int, slot: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if slot == 0:
        return [pair_index(rank + 1, [i + 1, j + 1])]
    if slot == rank + 1:
        return [pair_index(rank + 1, [i, j])]
    require(1 <= slot <= rank, "coface slot out of range")
    if i == slot:
        return [pair_index(rank + 1, [slot, j + 1]),
                pair_index(rank + 1, [slot + 1, j + 1])]
    if j == slot:
        return [pair_index(rank + 1, [i, slot]),
                pair_index(rank + 1, [i, slot + 1])]
    ii = i + (i > slot)
    jj = j + (j > slot)
    return [pair_index(rank + 1, [ii, jj])]


def cofaces(rank: int) -> list[list[list[int]]]:
    return [[coface_generator(rank, slot, p) for p in pairs(rank)]
            for slot in range(rank + 2)]


def deletion_generator(rank: int, strand: int, pair: Sequence[int]) -> list[int]:
    i, j = pair
    if strand in (i, j):
        return []
    i -= i > strand
    j -= j > strand
    return [pair_index(rank - 1, [i, j])]


def deletions(rank: int) -> list[list[list[int]]]:
    return [[deletion_generator(rank, strand, p) for p in pairs(rank)]
            for strand in range(1, rank + 1)]


def compose_maps(first: Sequence[Sequence[int]],
                 second: Sequence[Sequence[int]]) -> list[list[int]]:
    return [word_eval(w, second) for w in first]


def is_boundary_diagonal(d: Sequence[int]) -> bool:
    return d[1] == d[0] + 1 or list(d) == [1, 6]


def diagonals_cross(a: Sequence[int], b: Sequence[int]) -> bool:
    if set(a) & set(b):
        return False
    return (a[0] < b[0] < a[1] < b[1]) or (b[0] < a[0] < b[1] < a[1])


def edge_direction(cycle: Sequence[int], a: int, b: int) -> int:
    for i, x in enumerate(cycle):
        y = cycle[(i + 1) % len(cycle)]
        if (x, y) == (a, b):
            return 1
        if (x, y) == (b, a):
            return -1
    return 0


def build_k5() -> dict[str, Any]:
    ds = [[i, j] for i in range(1, 6) for j in range(i + 1, 7)
          if not is_boundary_diagonal([i, j])]
    verts: list[list[int]] = []
    for a in range(9):
        for b in range(a + 1, 9):
            for c in range(b + 1, 9):
                if not any(diagonals_cross(ds[x], ds[y])
                           for x, y in ((a, b), (a, c), (b, c))):
                    verts.append([a + 1, b + 1, c + 1])
    require(len(verts) == 14, "K5 vertex count")
    edges = [[a + 1, b + 1] for a in range(13) for b in range(a + 1, 14)
             if len(set(verts[a]) & set(verts[b])) == 2]
    require(len(edges) == 21, "K5 edge count")
    edge_set = {tuple(e) for e in edges}
    facets = [[v + 1 for v in range(14) if d + 1 in verts[v]] for d in range(9)]
    require(sorted(map(len, facets)) == [4, 4, 4, 5, 5, 5, 5, 5, 5],
            "K5 facet shape")
    raw: list[list[int]] = []
    for vs in facets:
        start = min(vs)
        cycle = [start]
        prev: int | None = None
        cur = start
        while True:
            candidates = [x for x in vs if x != cur and
                          tuple(sorted((cur, x))) in edge_set and x != prev]
            if len(cycle) == 1:
                nxt = min(candidates)
            else:
                candidates = [x for x in candidates if x == start or x not in cycle]
                require(bool(candidates), "K5 cycle walk stuck")
                nxt = min(candidates)
            if nxt == start:
                break
            cycle.append(nxt)
            prev, cur = cur, nxt
            require(len(cycle) <= len(vs), "K5 cycle overflow")
        require(len(cycle) == len(vs), "K5 facet is not one cycle")
        raw.append(cycle)
    signs = [0] * 9
    signs[0] = 1
    queue = [0]
    while queue:
        f = queue.pop(0)
        for g in range(9):
            common = sorted(set(facets[f]) & set(facets[g]))
            if g == f or len(common) != 2 or tuple(common) not in edge_set:
                continue
            df = edge_direction(raw[f], *common)
            dg = edge_direction(raw[g], *common)
            require(df and dg, "K5 facet cycle omitted an edge")
            wanted = -signs[f] * df * dg
            if signs[g] == 0:
                signs[g] = wanted
                queue.append(g)
            else:
                require(signs[g] == wanted, "K5 is not orientable")
    require(all(signs), "K5 facet graph disconnected")
    oriented = [cyc if sign == 1 else list(reversed(cyc))
                for cyc, sign in zip(raw, signs)]
    balance = [sum(edge_direction(cyc, *edge) for cyc in oriented) for edge in edges]
    require(balance == [0] * 21, "K5 boundary does not cancel")
    return {
        "diagonals": ds,
        "vertices": verts,
        "edges": edges,
        "facets": [{
            "diagonal_index": f + 1,
            "vertex_indices": facets[f],
            "kind": "pentagon" if len(facets[f]) == 5 else "square",
            "oriented_cycle": oriented[f],
        } for f in range(9)],
        "edge_boundary_coefficients": balance,
        "vertex_count": 14,
        "edge_count": 21,
        "pentagon_count": 6,
        "square_count": 3,
        "boundary_zero": True,
    }


def formula_manifest() -> dict[str, Any]:
    p3, p4, p5 = presentation(3), presentation(4), presentation(5)
    c34, c45 = cofaces(3), cofaces(4)
    d43, d54 = deletions(4), deletions(5)
    for source_rank, target_rank, maps in ((3, 4, c34), (4, 5, c45),
                                           (4, 3, d43), (5, 4, d54)):
        for mapping in maps:
            for rel in pure_relations(source_rank):
                image = word_eval(rel, mapping)
                require(artin_identity(target_rank, expand_pure(target_rank, image)),
                        "derived map is not a homomorphism")
    cosimp = []
    for i in range(5):
        for j in range(i + 1, 6):
            left = compose_maps(c34[i], c45[j])
            right = compose_maps(c34[j - 1], c45[i])
            for lhs, rhs in zip(left, right):
                require(artin_identity(5, expand_pure(5, reduce_word(lhs + inv_word(rhs)))),
                        "coface/coface identity failed")
            cosimp.append({"i": i, "j": j, "holds": True})
    retractions = []
    identity3 = [[i] for i in range(1, 4)]
    identity4 = [[i] for i in range(1, 7)]
    for slot in range(5):
        strand = 1 if slot == 0 else 4 if slot == 4 else slot
        require(compose_maps(c34[slot], d43[strand - 1]) == identity3,
                "PB3 primary retraction failed")
        retractions.append({"source_rank": 3, "slot": slot,
                            "deleted_strand": strand, "holds": True})
        if 0 < slot < 4:
            require(compose_maps(c34[slot], d43[slot]) == identity3,
                    "PB3 second retraction failed")
            retractions.append({"source_rank": 3, "slot": slot,
                                "deleted_strand": slot + 1, "holds": True})
    for slot in range(6):
        strand = 1 if slot == 0 else 5 if slot == 5 else slot
        require(compose_maps(c45[slot], d54[strand - 1]) == identity4,
                "PB4 primary retraction failed")
        retractions.append({"source_rank": 4, "slot": slot,
                            "deleted_strand": strand, "holds": True})
        if 0 < slot < 5:
            require(compose_maps(c45[slot], d54[slot]) == identity4,
                    "PB4 second retraction failed")
            retractions.append({"source_rank": 4, "slot": slot,
                                "deleted_strand": slot + 1, "holds": True})
    face_cosimp = []
    for rank in (3, 4):
        for slot in range(rank + 2):
            for deleted_zero in range(rank + 1):
                left = compose_maps(cofaces(rank)[slot], deletions(rank + 1)[deleted_zero])
                if deleted_zero in (slot - 1, slot):
                    right = [[i] for i in range(1, len(pairs(rank)) + 1)]
                    case = "identity"
                elif deleted_zero < slot - 1:
                    right = compose_maps(deletions(rank)[deleted_zero],
                                         cofaces(rank - 1)[slot - 1])
                    case = "d^(i-1)_after_s^j"
                else:
                    right = compose_maps(deletions(rank)[deleted_zero - 1],
                                         cofaces(rank - 1)[slot])
                    case = "d^i_after_s^(j-1)"
                for lhs, rhs in zip(left, right):
                    require(artin_identity(rank, expand_pure(
                        rank, reduce_word(lhs + inv_word(rhs)))),
                        "face/coface identity failed")
                face_cosimp.append({"source_rank": rank, "slot": slot,
                                    "deleted_strand": deleted_zero + 1,
                                    "case": case, "holds": True})
    a18 = [c34[s] for s in (4, 0, 1, 2, 3)]
    require([m[0] for m in a18] == [[1], [4], [2, 4], [1, 2], [1]],
            "literal A.18 x12 row mismatch")
    require([m[2] for m in a18] == [[4], [6], [6], [5, 6], [4, 5]],
            "literal A.18 x23 row mismatch")
    return {
        "convention": {
            "pair_order": "lexicographic_i_then_j",
            "artin_action": (
                "left_to_right; sigma_i: t_i->t_i*t_(i+1)*t_i^-1, "
                "t_(i+1)->t_i"
            ),
            "coface_slots": "0=left endpoint, 1..r=strand doubling, r+1=right endpoint",
            "deletion_strands": "one-based",
        },
        "braid_kernel_certificates": {
            "PB3": braid_kernel_certificate(3),
            "PB4": braid_kernel_certificate(4),
            "PB5": braid_kernel_certificate(5),
        },
        "presentations": {"PB3": p3, "PB4": p4, "PB5": p5},
        "cofaces_3_4": c34,
        "cofaces_4_5": c45,
        "deletions_4_3": d43,
        "deletions_5_4": d54,
        "coface_coface_identities": cosimp,
        "face_coface_identities": face_cosimp,
        "insertion_deletion_retractions": retractions,
        "a18_order": {
            "names": ["phi_123", "phi_234", "phi_12_3_4", "phi_1_23_4", "phi_1_2_34"],
            "slots": [4, 0, 1, 2, 3],
            "maps": a18,
        },
        "k5": build_k5(),
    }


def coords_word(coords: Sequence[int]) -> list[int]:
    out: list[int] = []
    for i, exponent in enumerate(coords, 1):
        require(isinstance(exponent, int) and exponent >= 0, "bad pc coordinate")
        out.extend([i] * exponent)
    return out


@dataclass
class PcCollector:
    receipt: dict[str, Any]

    def __post_init__(self) -> None:
        self.n = int(self.receipt["generator_count"])
        self.orders = list(self.receipt["relative_orders"])
        require(self.n == len(self.orders) and self.n <= 175, "pc generator count/cap")
        require(self.receipt["exponent"] == 3, "receipt is not exponent three")
        require(all(x == 3 for x in self.orders), "relative orders are not all three")
        self.powers = [self._coord(row) for row in self.receipt["power_relations"]]
        require(all(row == self.zero() for row in self.powers),
                "exponent-three power relation is nonidentity")
        self.inverses = [self._coord(row) for row in self.receipt["inverses"]]
        require(len(self.inverses) == self.n, "inverse row count")
        self.conjugates: dict[tuple[int, int], tuple[int, ...]] = {}
        for row in self.receipt["conjugate_relations"]:
            key = (row["i"], row["j"])
            require(key not in self.conjugates and 1 <= key[1] < key[0] <= self.n,
                    "bad/duplicate conjugate row")
            self.conjugates[key] = self._coord(row["coords"])
        require(len(self.conjugates) == self.n * (self.n - 1) // 2,
                "incomplete positive conjugate table")
        self.inverse_conjugates: dict[tuple[int, int], tuple[int, ...]] = {}
        for row in self.receipt["inverse_conjugate_relations"]:
            key = (row["i"], row["j"])
            require(key not in self.inverse_conjugates and 1 <= key[1] < key[0] <= self.n,
                    "bad/duplicate inverse-conjugate row")
            self.inverse_conjugates[key] = self._coord(row["coords"])
        require(set(self.inverse_conjugates) == set(self.conjugates),
                "incomplete inverse conjugate table")
        self._collect_cache: dict[tuple[int, ...], tuple[int, ...]] = {
            (): self.zero()
        }

    def _coord(self, row: Sequence[int]) -> tuple[int, ...]:
        require(len(row) == self.n and all(isinstance(x, int) for x in row),
                "pc coordinate width/type")
        require(all(0 <= x < self.orders[i] for i, x in enumerate(row)),
                "pc coordinate outside relative order")
        return tuple(row)

    def zero(self) -> tuple[int, ...]:
        return (0,) * self.n

    def unit(self, i: int) -> tuple[int, ...]:
        require(isinstance(i, int) and 1 <= i <= self.n, "pc unit index")
        row = [0] * self.n
        row[i - 1] = 1
        return tuple(row)

    def collect(self, signed_word: Sequence[int]) -> tuple[int, ...]:
        cache_key = tuple(signed_word)
        cached = self._collect_cache.get(cache_key)
        if cached is not None:
            return cached
        tokens: list[int] = []
        for x in signed_word:
            require(1 <= abs(x) <= self.n, "pc signed letter out of range")
            if x > 0:
                tokens.append(x)
            else:
                tokens.extend(coords_word(self.inverses[-x - 1]))
        steps = 0
        cap = max(10000, 1000 * (1 + len(tokens)) * (1 + self.n))
        while True:
            changed = False
            for pos in range(len(tokens) - 1):
                a, b = tokens[pos], tokens[pos + 1]
                if a > b:
                    replacement = [b] + coords_word(self.conjugates[(a, b)])
                    tokens[pos:pos + 2] = replacement
                    changed = True
                    break
            if changed:
                steps += 1
                require(steps <= cap, "pc collector rewrite cap")
                continue
            pos = 0
            while pos < len(tokens):
                i = tokens[pos]
                run = pos
                while run < len(tokens) and tokens[run] == i:
                    run += 1
                if run - pos >= self.orders[i - 1]:
                    tokens[pos:pos + self.orders[i - 1]] = coords_word(self.powers[i - 1])
                    changed = True
                    break
                pos = run
            if not changed:
                break
            steps += 1
            require(steps <= cap, "pc collector power cap")
        row = [0] * self.n
        last = 0
        for token in tokens:
            require(token >= last, "collector did not reach normal order")
            row[token - 1] += 1
            require(row[token - 1] < self.orders[token - 1], "uncollected pc power")
            last = token
        answer = tuple(row)
        # The checker never enumerates a group.  This cache contains only the
        # finitely many marked/collector words explicitly present in receipt.
        self._collect_cache[cache_key] = answer
        return answer

    def mul(self, a: Sequence[int], b: Sequence[int]) -> tuple[int, ...]:
        return self.collect(coords_word(a) + coords_word(b))

    def inverse(self, a: Sequence[int]) -> tuple[int, ...]:
        word: list[int] = []
        for i in range(self.n, 0, -1):
            for _ in range(a[i - 1]):
                word.extend(coords_word(self.inverses[i - 1]))
        return self.collect(word)

    def power(self, a: Sequence[int], exponent: int) -> tuple[int, ...]:
        if exponent < 0:
            return self.power(self.inverse(a), -exponent)
        out = self.zero()
        base = tuple(a)
        n = exponent
        while n:
            if n & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            n >>= 1
        return out

    def conjugate(self, a: Sequence[int], b: Sequence[int]) -> tuple[int, ...]:
        return self.mul(self.mul(self.inverse(b), a), b)

    def eval_coords_by_images(self, coords: Sequence[int],
                              target: "PcCollector",
                              images: Sequence[Sequence[int]]) -> tuple[int, ...]:
        out = target.zero()
        for i, exponent in enumerate(coords):
            out = target.mul(out, target.power(images[i], exponent))
        return out

    def validate(self) -> None:
        require(int(self.receipt["order_decimal"]) == math.prod(self.orders),
                "pc order does not equal relative-order product")
        require(0 <= self.receipt["nilpotency_class"] <= 3, "class exceeds terminal theorem")
        for i in range(1, self.n + 1):
            require(self.mul(self.unit(i), self.inverses[i - 1]) == self.zero(),
                    "pc inverse is not a right inverse")
            require(self.mul(self.inverses[i - 1], self.unit(i)) == self.zero(),
                    "pc inverse is not a left inverse")
        for (i, j), expected in self.inverse_conjugates.items():
            actual = self.conjugate(self.unit(i), self.inverses[j - 1])
            require(actual == expected, "inverse conjugate replay failed")
        marked = self.receipt["marked_generators"]
        expected_pairs = pairs(self.receipt["rank"])
        require([row["pair"] for row in marked] == expected_pairs, "marked pair order")
        require([row["label"] for row in marked] ==
                [f"a{i}{j}" for i, j in expected_pairs], "marked labels")
        for row in marked:
            coord = self._coord(row["coords"])
            inv = self._coord(row["inverse_coords"])
            require(self.mul(coord, inv) == self.zero() and self.mul(inv, coord) == self.zero(),
                    "marked inverse replay")
        require(len(self.receipt["original_relations"]) ==
                len(self.receipt["original_relator_images"]), "relator receipt length")
        for word, claimed in zip(self.receipt["original_relations"],
                                 self.receipt["original_relator_images"]):
            actual = eval_marked(word, marked, self)
            require(actual == self._coord(claimed) == self.zero(), "original relator replay")


def eval_marked(word: Sequence[int], marked: Sequence[dict[str, Any]],
                pc: PcCollector) -> tuple[int, ...]:
    out = pc.zero()
    for x in word:
        require(1 <= abs(x) <= len(marked), "marked word index")
        key = "coords" if x > 0 else "inverse_coords"
        out = pc.mul(out, marked[abs(x) - 1][key])
    return out


def eval_pc_relation_by_images(source: PcCollector, target: PcCollector,
                               images: Sequence[Sequence[int]],
                               coord: Sequence[int]) -> tuple[int, ...]:
    return source.eval_coords_by_images(coord, target, images)


def validate_hom(source: PcCollector, target: PcCollector,
                 images: Sequence[Sequence[int]]) -> None:
    require(len(images) == source.n, "source pc image count")
    images = [target._coord(row) for row in images]
    for i in range(source.n):
        lhs = target.power(images[i], source.orders[i])
        rhs = eval_pc_relation_by_images(source, target, images, source.powers[i])
        require(lhs == rhs, "homomorphism power relation")
    for row in source.receipt["conjugate_relations"]:
        i, j = row["i"], row["j"]
        lhs = target.conjugate(images[i - 1], images[j - 1])
        rhs = eval_pc_relation_by_images(source, target, images, row["coords"])
        require(lhs == rhs, "homomorphism conjugate relation")
    for row in source.receipt["inverse_conjugate_relations"]:
        i, j = row["i"], row["j"]
        lhs = target.conjugate(images[i - 1], target.inverse(images[j - 1]))
        rhs = eval_pc_relation_by_images(source, target, images, row["coords"])
        require(lhs == rhs, "homomorphism inverse-conjugate relation")


def validate_inverse_pc_maps(pc: PcCollector,
                             forward_rows: Sequence[Sequence[int]],
                             inverse_rows: Sequence[Sequence[int]]) \
        -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Replay two mutually inverse pc maps, including both composition orders."""
    forward = [pc._coord(row) for row in forward_rows]
    inverse = [pc._coord(row) for row in inverse_rows]
    validate_hom(pc, pc, forward)
    validate_hom(pc, pc, inverse)
    for idx in range(pc.n):
        expected = pc.unit(idx + 1)
        require(pc.eval_coords_by_images(forward[idx], pc, inverse) == expected and
                pc.eval_coords_by_images(inverse[idx], pc, forward) == expected,
                "pc inverse compositions")
    return forward, inverse


def expected_map_words(kind: str, source_rank: int, target_rank: int,
                       extra: dict[str, Any]) -> list[list[int]]:
    if kind == "coface":
        require(target_rank == source_rank + 1, "coface rank")
        return cofaces(source_rank)[extra["slot"]]
    if kind == "deletion":
        require(source_rank == target_rank + 1, "deletion rank")
        return deletions(source_rank)[extra["strand"] - 1]
    raise Reject(f"unknown map kind {kind}")


def validate_map(record: dict[str, Any], groups: dict[str, PcCollector]) -> None:
    require(record["well_defined"] is True, "map not well-defined")
    source, target = groups[record["source"]], groups[record["target"]]
    words = expected_map_words(record["kind"], source.receipt["rank"],
                               target.receipt["rank"], record["extra"])
    require(record["generator_words"] == words, f"{record['name']}: word formula")
    marked_source = source.receipt["marked_generators"]
    marked_target = target.receipt["marked_generators"]
    actual_target = [eval_marked(w, marked_target, target) for w in words]
    require(actual_target == [target._coord(x) for x in record["target_marked_coords"]],
            f"{record['name']}: target marked coordinates")
    pc_images = [target._coord(x) for x in record["source_pc_images"]]
    validate_hom(source, target, pc_images)
    for source_mark, target_mark in zip(marked_source, actual_target):
        via_pc = source.eval_coords_by_images(source_mark["coords"], target, pc_images)
        require(via_pc == target_mark, f"{record['name']}: marked-vs-pc map")


def elem_pairs(g: Sequence[Any], identity: Any, mul: Any) -> list[list[Any]]:
    return [
        [g[0], g[3]], [g[3], g[5]], [pp([g[1], g[3]], identity, mul), g[5]],
        [pp([g[0], g[1]], identity, mul), pp([g[4], g[5]], identity, mul)],
        [g[0], pp([g[3], g[4]], identity, mul)],
    ]


def elem_hex_pairs(x: Any, y: Any, identity: Any, mul: Any, inverse: Any) -> list[list[Any]]:
    z = inverse(pp([x, y], identity, mul))
    u = inverse(pp([y, x], identity, mul))
    return [[x, y], [x, z], [y, z], [u, x], [u, y]]


def elem_hex(values: Sequence[Any], x: Any, y: Any, identity: Any,
             mul: Any, inverse: Any) -> list[Any]:
    require(len(values) == 5, "hex context width")
    z = inverse(pp([x, y], identity, mul))
    u = inverse(pp([y, x], identity, mul))
    return [pp([values[0], inverse(values[1]), values[2]], identity, mul),
            pp([inverse(values[3]), inverse(values[0]), values[4]], identity, mul)]


def elem_pent(values: Sequence[Any], identity: Any, mul: Any, inverse: Any) -> Any:
    require(len(values) == 5, "pentagon context width")
    return pp([inverse(pp([values[4], values[2]], identity, mul)),
               values[1], values[3], values[0]], identity, mul)


def enumerate_generated(identity: Any, generators: Sequence[Any], mul: Any,
                        inverse: Any, cap: int) -> set[Any]:
    steps = list(generators) + [inverse(g) for g in generators]
    seen = {identity}
    queue = [identity]
    while queue:
        a = queue.pop()
        for g in steps:
            b = mul(a, g)
            if b not in seen:
                seen.add(b)
                require(len(seen) <= cap, "bounded subgroup enumeration cap")
                queue.append(b)
    return seen


def derived_from_two(identity: Any, x: Any, y: Any, mul: Any,
                     inverse: Any, group_cap: int) -> set[Any]:
    # In a two-generator group the derived subgroup is the normal closure of
    # [x,y].  Reclose only after a genuinely new conjugate is found.
    comm = mul(mul(mul(inverse(x), inverse(y)), x), y)
    seeds = [comm]
    subgroup = enumerate_generated(identity, seeds, mul, inverse, group_cap)
    while True:
        new_seed = None
        for h in list(seeds):
            for g in (x, y, inverse(x), inverse(y)):
                c = mul(mul(inverse(g), h), g)
                if c not in subgroup:
                    new_seed = c
                    break
            if new_seed is not None:
                break
        if new_seed is None:
            return subgroup
        seeds.append(new_seed)
        subgroup = enumerate_generated(identity, seeds, mul, inverse, group_cap)


def validate_perm_model(record: dict[str, Any], marked_count: int) -> list[Perm]:
    degree = record["degree"]
    require(isinstance(degree, int) and degree > 0, "permutation model degree")
    rows = record["marked_permutations"]
    require(len(rows) == marked_count, "permutation marked count")
    return [perm_from_row(row, degree) for row in rows]


def restrict_perm_block(p: Perm, offset: int, width: int) -> Perm:
    row = tuple(p[offset + i] - offset for i in range(width))
    require(set(row) == set(range(width)), "permutation block does not close")
    return row


def independent_h9_nakayama(h9: Sequence[Perm], g9: Sequence[Perm]) -> dict[str, Any]:
    one = perm_one(27)
    derived = derived_from_two(one, g9[0], g9[1], perm_mul, perm_inv, 2916)
    require(len(derived) == 729, "G9 derived order")
    # Greedily obtain three commuting order-nine generators of G9'.
    basis: list[Perm] = []
    generated = {one}
    for value in derived:
        if value in generated or perm_order(value) != 9:
            continue
        trial = enumerate_generated(one, basis + [value], perm_mul, perm_inv, 729)
        if len(trial) == 9 * len(generated):
            basis.append(value)
            generated = trial
        if len(generated) == 729:
            break
    require(len(basis) == 3 and len(generated) == 729 and
            all(perm_order(x) == 9 for x in basis) and
            all(perm_mul(x, y) == perm_mul(y, x) for x in basis for y in basis),
            "G9' is not certified C9^3")
    coordinates: dict[Perm, tuple[int, int, int]] = {}
    for a in range(9):
        for b in range(9):
            for c in range(9):
                value = perm_mul(perm_mul(elem_power(basis[0], a, one, perm_mul, perm_inv),
                                          elem_power(basis[1], b, one, perm_mul, perm_inv)),
                                 elem_power(basis[2], c, one, perm_mul, perm_inv))
                require(value not in coordinates, "G9' coordinate collision")
                coordinates[value] = (a, b, c)
    require(set(coordinates) == derived, "G9' coordinate coverage")

    htuples = [tuple(restrict_perm_block(g, 27 * j, 27) for j in range(4))
               for g in h9]
    one4 = (one, one, one, one)

    def mul4(a: tuple[Perm, ...], b: tuple[Perm, ...]) -> tuple[Perm, ...]:
        return tuple(perm_mul(x, y) for x, y in zip(a, b))

    def inv4(a: tuple[Perm, ...]) -> tuple[Perm, ...]:
        return tuple(perm_inv(x) for x in a)

    def comm4(a: tuple[Perm, ...], b: tuple[Perm, ...]) -> tuple[Perm, ...]:
        return mul4(mul4(mul4(inv4(a), inv4(b)), a), b)

    def vector(a: tuple[Perm, ...]) -> tuple[int, ...]:
        require(all(x in coordinates for x in a), "H9 commutator outside (G9')^4")
        return tuple(v % 3 for x in a for v in coordinates[x])

    reps: list[tuple[Perm, ...]] = []
    vectors: list[tuple[int, ...]] = []
    seeds = [comm4(htuples[i], htuples[j])
             for i in range(6) for j in range(i)]
    queue: list[tuple[Perm, ...]] = []
    for value in seeds:
        v = vector(value)
        if rank_mod3(vectors + [v]) > rank_mod3(vectors):
            reps.append(value)
            vectors.append(v)
            queue.append(value)
    attempts = 0
    while queue and rank_mod3(vectors) < 12:
        value = queue.pop(0)
        for g in htuples:
            conjugate = mul4(mul4(inv4(g), value), g)
            attempts += 1
            require(attempts <= 72, "H9 Nakayama module-action cap")
            v = vector(conjugate)
            if rank_mod3(vectors + [v]) > rank_mod3(vectors):
                reps.append(conjugate)
                vectors.append(v)
                queue.append(conjugate)
    require(rank_mod3(vectors) == 12, "H9' mod-three Nakayama rank")
    require(all(rank_mod3(vectors + [vector(
        mul4(mul4(inv4(g), value), g))]) == 12
        for value in reps for g in htuples),
        "H9 Nakayama span is not invariant under all six marked actions")
    return {"G9_derived_order": 729, "mod3_span_rank": 12,
            "orbit_witness_count": len(vectors), "orbit_attempts": attempts,
            "seed_commutator_count": len(seeds), "module_action_cap": 72,
            "invariant_under_all_six_marked_actions": True,
            "derived_elements": derived}


def validate_short_gate(data: dict[str, Any]) -> dict[str, Any]:
    gate = data["short_common_quotient_gate"]
    for name in ("H9", "G9", "Q4", "Q0"):
        row = gate[name]
        require(row["quotient_order"] == row["abelianization_order"] and
                row["coprime_to_3"] is True and row["quotient_order"] % 3 != 0 and
                row["three_primary_trivial"] is True and
                int(row["order_decimal"]) ==
                int(row["derived_order_decimal"]) * row["quotient_order"],
                f"{name} derived quotient")
    require(gate["Q4"]["quotient_order"] == gate["H9"]["quotient_order"] == 32 and
            gate["Q0"]["quotient_order"] == gate["G9"]["quotient_order"] == 4,
            "perfect-factor abelianization reductions")
    require(int(gate["H9"]["derived_order_decimal"]) == 3 ** 24 and
            int(gate["G9"]["derived_order_decimal"]) == 729 and
            int(gate["Q4"]["derived_order_decimal"]) == 504 ** 4 * 3 ** 24 and
            int(gate["Q0"]["derived_order_decimal"]) == 504 * 729,
            "derived-order reductions")
    require(gate["Q4_ab_reduced_to_H9_by_perfect_factor"] is True and
            gate["Q0_ab_reduced_to_G9_by_perfect_factor"] is True,
            "missing perfect-factor reduction certificate")
    require(gate["Q4_common_q3_quotient_trivial"] == gate["Q4"]["three_primary_trivial"] and
            gate["Q0_common_q3_quotient_trivial"] == gate["Q0"]["three_primary_trivial"],
            "common-q3 quotient flags")
    require(gate["abelian_invariants_calls"] == 0 and
            gate["derived_subgroup_calls"] == 1 and
            gate["G9_derived_series_reused_from_core"] is True and
            gate["repeated_group_reconstruction"] is False,
            "coarse shortcut performance contract")
    models = data["coarse_models"]
    q4 = validate_perm_model(models["Q4"], 6)
    h9 = validate_perm_model(models["H9"], 6)
    q0 = validate_perm_model(models["Q0"], 2)
    g9 = validate_perm_model(models["G9"], 2)
    p = validate_perm_model(models["P"], 2)
    require(models["P"]["perfect"] is True and int(models["P"]["order_decimal"]) == 504,
            "P perfect/order core contract")
    require(int(models["Q4"]["order_decimal"]) ==
            504 ** 4 * int(models["H9"]["order_decimal"]), "Q4=P^4*H9 order")
    require(int(models["Q0"]["order_decimal"]) ==
            504 * int(models["G9"]["order_decimal"]), "Q0=P*G9 order")
    for i in range(6):
        require(tuple(x - 36 for x in q4[i][36:]) == h9[i], "Q4/H9 marked block")
    for i in range(2):
        require(q0[i][:9] == p[i] and tuple(x - 9 for x in q0[i][9:]) == g9[i],
                "Q0=P*G9 marked block")
    p_group = enumerate_generated(perm_one(9), p, perm_mul, perm_inv, 504)
    g9_group = enumerate_generated(perm_one(27), g9, perm_mul, perm_inv, 2916)
    require(len(p_group) == 504 and len(g9_group) == 2916,
            "independent P/G9 factor orders")
    require(gate["all_6x4_Q4_P_blocks_in_P"] is True and all(
        restrict_perm_block(row, 9 * coordinate, 9) in p_group
        for row in q4 for coordinate in range(4)),
        "coarse Q4 marked P-block membership")
    require(gate["all_6x4_H9_blocks_in_G9"] is True and all(
        restrict_perm_block(row, 27 * coordinate, 27) in g9_group
        for row in h9 for coordinate in range(4)),
        "H9 marked G9-block membership")
    p_derived = derived_from_two(perm_one(9), p[0], p[1], perm_mul, perm_inv, 504)
    require(len(p_derived) == 504, "independent P perfectness")
    nak = independent_h9_nakayama(h9, g9)
    claimed_nak = gate["independent_nakayama_certificate"]
    require(claimed_nak["G9_derived_order"] == nak["G9_derived_order"] == 729 and
            claimed_nak["mod3_span_rank"] == nak["mod3_span_rank"] == 12 and
            claimed_nak["nakayama_full_Z9_module"] is True and
            claimed_nak["checker_seed_commutator_count"] ==
            nak["seed_commutator_count"] == 15 and
            claimed_nak["checker_module_action_cap"] ==
            nak["module_action_cap"] == 72 and
            claimed_nak["checker_requires_invariant_span"] is True and
            nak["invariant_under_all_six_marked_actions"] is True and
            claimed_nak["independently_reconstructed_from_marked_permutations_by_checker"] is True,
            "independent H9 Nakayama certificate")
    # Rank 12 modulo 3 and Nakayama give H9'=(G9')^4.  Hence H9/H9'
    # embeds in the 2-group (G9/G9')^4, proving Hom(H9,C3)=0 without trusting
    # GAP's AbelianInvariants(H9) output.
    return {"Q4": q4, "H9": h9, "Q0": q0, "G9": g9, "P": p,
            "_P_GROUP": p_group, "_G9_GROUP": g9_group,
            "_G9_DERIVED": nak["derived_elements"]}


def pc_eval(word: Sequence[int], images: Sequence[Sequence[int]], pc: PcCollector) -> tuple[int, ...]:
    return elem_eval(word, [pc._coord(x) for x in images], pc.zero(),
                     pc.mul, pc.inverse)


def try_two_generator_factor_auto(x: Perm, y: Perm, hx: Perm, hy: Perm,
                                  source_rows: Sequence[Perm],
                                  image_rows: Sequence[Perm], cap: int) -> bool:
    """Return False only for a candidate-local relation/bijectivity failure."""
    require(len(source_rows) == len(image_rows) == 6,
            "candidate factor marked-row width")
    identity = perm_one(len(x))
    steps = ((x, hx), (y, hy), (perm_inv(x), perm_inv(hx)),
             (perm_inv(y), perm_inv(hy)))
    mapping: dict[Perm, Perm] = {identity: identity}
    queue = [identity]
    while queue:
        a = queue.pop()
        ma = mapping[a]
        for g, hg in steps:
            b, mb = perm_mul(a, g), perm_mul(ma, hg)
            if b in mapping:
                if mapping[b] != mb:
                    return False
            else:
                mapping[b] = mb
                if len(mapping) > cap:
                    return False
                queue.append(b)
    if len(mapping) != cap or len(set(mapping.values())) != cap:
        return False
    return all(mapping[source] == image
               for source, image in zip(source_rows, image_rows))


def try_candidate_settlement(source_words: Sequence[Sequence[int]],
                             q4_images: Sequence[Perm],
                             p4_images: Sequence[Sequence[int]],
                             pc4: PcCollector, models: dict[str, Any],
                             p4_relations: Sequence[Sequence[int]]) -> bool:
    identity6 = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    # Each marked PB4 generator is sent to a conjugate of itself.  We replay
    # this rather than infer it from the producer's settlement boolean.
    require(exponent_matrix(source_words, 6) == identity6,
            "settlement source is not identity on PB4 abelianization")
    if any(pc_eval(rel, p4_images, pc4) != pc4.zero() for rel in p4_relations):
        return False
    q4_marks = models["Q4"]
    p, g9 = models["P"], models["G9"]
    for coordinate in range(4):
        source_p = [restrict_perm_block(g, 9 * coordinate, 9) for g in q4_marks]
        image_p = [restrict_perm_block(g, 9 * coordinate, 9) for g in q4_images]
        ix = [i for i, g in enumerate(source_p) if g == p[0]]
        iy = [i for i, g in enumerate(source_p) if g == p[1]]
        require(len(ix) == len(iy) == 1, "P coordinate marked X/Y selectors")
        if not try_two_generator_factor_auto(p[0], p[1], image_p[ix[0]],
                                             image_p[iy[0]], source_p,
                                             image_p, 504):
            return False
        source_g = [restrict_perm_block(g, 36 + 27 * coordinate, 27)
                    for g in q4_marks]
        image_g = [restrict_perm_block(g, 36 + 27 * coordinate, 27)
                   for g in q4_images]
        ix = [i for i, g in enumerate(source_g) if g == g9[0]]
        iy = [i for i, g in enumerate(source_g) if g == g9[1]]
        require(len(ix) == len(iy) == 1, "G9 coordinate marked X/Y selectors")
        if not try_two_generator_factor_auto(g9[0], g9[1], image_g[ix[0]],
                                             image_g[iy[0]], source_g,
                                             image_g, 2916):
            return False
    # q4_images are evaluations of source_words in the six H9 marked rows, so
    # the ambient factor automorphism preserves H9.  Its restriction is an
    # injective endomorphism of finite H9 and hence an automorphism.  The PB4
    # relation replay above gives an endomorphism of the exponent-three verbal
    # quotient Pi4; the identity map on PB4_ab mod 3 is the identity on
    # Pi4/Phi(Pi4), so Burnside's basis theorem makes it an automorphism.
    return True


def validate_direct_route(data: dict[str, Any], pc3: PcCollector,
                          pc4: PcCollector, models: dict[str, Any],
                          repo_root: Path) -> None:
    correction = data["correction_fibre"]
    cert = correction["certificate"]
    records = correction["records"]
    require(cert["order"] == cert["enumerated_count"] == 27 and
            cert["projection_kernel_order"] == 27 and cert["direct_product"] is True and
            cert["all_words_coarse_identity"] is True and
            cert["all_q3_coordinates_unique"] is True,
            "correction fibre certificate")
    require(1 <= cert["preimage_call_count"] <= cert["preimage_call_bound"] == 3,
            "compressed correction preimage calls")
    require(len(records) == 27, "correction record count")
    require(len({tuple(row["q_coords"]) for row in records}) == 27,
            "producer B2 coordinate diagnostic uniqueness")
    q0, g9, p = models["Q0"], models["G9"], models["P"]
    one_q0, one_g9, one_p = perm_one(36), perm_one(27), perm_one(9)
    marked3 = [row["coords"] for row in pc3.receipt["marked_generators"]]
    b2_images = [marked3[0], marked3[2]]
    q_values: list[tuple[int, ...]] = []
    q_perm_rows: list[tuple[int, ...]] = []
    for row in records:
        word = row["word"]
        require(elem_eval(word, q0, one_q0, perm_mul, perm_inv) == one_q0,
                "correction is not coarse identity")
        q = pc_eval(word, b2_images, pc3)
        require(q == pc3._coord(row["ambient_Pi3_coords"]),
                "correction ambient Pi3 coordinates")
        q_values.append(q)
        qp = perm_from_row(row["q_permutation"], len(row["q_permutation"]))
        q_perm_rows.append(qp)
    require(len(set(q_values)) == len(set(q_perm_rows)) == 27,
            "correction q3 coverage is not bijective")
    b2_group = enumerate_generated(pc3.zero(), b2_images, pc3.mul,
                                   pc3.inverse, 27)
    require(len(b2_group) == 27 and set(q_values) == b2_group,
            "correction q3 values are not the full marked B(2,3)")

    powers_block = data["canonical_roof_powers"]
    powers = powers_block["rows"]
    require(powers_block["frozen_rows_evaluated_once"] is True and
            powers_block["coarse_key_cache_size"] == 972 and
            powers_block["canonicalized_each_step"] is True and
            powers_block["literal_power_words_retained"] is False and
            powers_block["bounded_step_word_cap"] == 100000,
            "canonical cache/normalization receipt")
    require([r["exponent"] for r in powers] == [1, 2, 4, 5, 7, 8],
            "outside power universe")
    words_obj = json.loads((repo_root / WORDS).read_text(encoding="utf-8"))
    require(words_obj["schema"] == "d972-b4-word-key-artifact/v1" and
            words_obj["count"] == 972, "frozen word artifact metadata")
    base = words_obj["rows"][18][2]
    coarse_cache: dict[tuple[int, Perm, Perm], list[int]] = {}
    for row_index, frozen in enumerate(words_obj["rows"], 1):
        p_value = elem_eval(frozen[2], p, one_p, perm_mul, perm_inv)
        g_value = elem_eval(frozen[2], g9, one_g9, perm_mul, perm_inv)
        coarse_cache.setdefault((frozen[0], p_value, g_value), []).append(row_index)
    identity_matches = coarse_cache.get((0, one_p, one_g9), [])
    require(len(identity_matches) == 1, "frozen m=0 coarse identity row uniqueness")
    identity_index = identity_matches[0]
    identity_frozen = words_obj["rows"][identity_index - 1]
    base_key = (0,
                elem_eval(base, p, one_p, perm_mul, perm_inv),
                elem_eval(base, g9, one_g9, perm_mul, perm_inv))
    require(coarse_cache.get(base_key, []) == [19],
            "frozen row18 coarse key uniqueness")
    canonical_by_n: dict[int, list[int]] = {0: identity_frozen[2], 1: base}
    row_index_by_n = {0: identity_index, 1: 19}
    step_by_n: dict[int, list[int]] = {1: base}
    max_step_length = len(base)
    max_canonical_length = len(base)
    for n in range(2, 10):
        step = gt_compose_m0(base, canonical_by_n[n - 1])
        require(len(step) <= powers_block["bounded_step_word_cap"],
                f"bounded canonical step word cap n={n}")
        step_by_n[n] = step
        max_step_length = max(max_step_length, len(step))
        p_value = elem_eval(step, p, one_p, perm_mul, perm_inv)
        g_value = elem_eval(step, g9, one_g9, perm_mul, perm_inv)
        matches = coarse_cache.get((0, p_value, g_value), [])
        require(len(matches) == 1, f"normalized coarse row uniqueness n={n}")
        row_index_by_n[n] = matches[0]
        canonical_by_n[n] = words_obj["rows"][matches[0] - 1][2]
        if n <= 8:
            max_canonical_length = max(max_canonical_length,
                                       len(canonical_by_n[n]))
    require(len({row_index_by_n[n] for n in range(9)}) == 9 and
            row_index_by_n[9] == identity_index and
            words_obj["rows"][row_index_by_n[9] - 1] == identity_frozen,
            "normalized GT-compose orbit is not exactly order nine")
    expected_orbit = [{
        "exponent": n,
        "row_index": row_index_by_n[n],
        "key": words_obj["rows"][row_index_by_n[n] - 1][1],
        "word": words_obj["rows"][row_index_by_n[n] - 1][2],
    } for n in range(10)]
    require(powers_block["normalized_orbit"] == expected_orbit and
            powers_block["normalized_orbit_first_repeat"] == 9 and
            powers_block["normalized_orbit_n0_n8_distinct"] is True and
            powers_block["normalized_orbit_n9_identity"] is True and
            powers_block["outside_residues_complete_mod9"] == [1, 2, 4, 5, 7, 8] and
            powers_block["max_bounded_step_word_length"] == max_step_length and
            powers_block["max_canonical_word_length"] == max_canonical_length,
            "normalized GT-compose orbit receipt")
    marked_q3 = b2_images
    for row in powers:
        frozen = words_obj["rows"][row["row_index"] - 1]
        require(frozen[0] == 0 and frozen[1] == row["key"] and frozen[2] == row["word"],
                "canonical frozen row binding")
        require(row["row_index"] == row_index_by_n[row["exponent"]],
                "outside row is not the normalized orbit row")
        step, canon = step_by_n[row["exponent"]], row["word"]
        step_p = elem_eval(step, p, one_p, perm_mul, perm_inv)
        step_g = elem_eval(step, g9, one_g9, perm_mul, perm_inv)
        can_p = elem_eval(canon, p, one_p, perm_mul, perm_inv)
        can_g = elem_eval(canon, g9, one_g9, perm_mul, perm_inv)
        require((step_p, step_g) == (can_p, can_g),
                "bounded-step/canonical coarse roof mismatch")
        require(math.lcm(perm_order(can_p), perm_order(can_g)) == 9,
                "outside roof does not have order nine")
        step_q = pc_eval(step, marked_q3, pc3)
        can_q = pc_eval(canon, marked_q3, pc3)
        step_fibre = {pc3.mul(step_q, c) for c in q_values}
        can_fibre = {pc3.mul(can_q, c) for c in q_values}
        require(len(step_fibre) == len(can_fibre) == 27 and
                step_fibre == can_fibre,
                "bounded-step/canonical q3 fibre mismatch")
        shift = pc3.mul(pc3.inverse(can_q), step_q)
        idx = row["q3_shift_correction_index"] - 1
        require(0 <= idx < 27 and q_values[idx] == shift and
                pc3._coord(row["q3_shift_ambient_Pi3_coords"]) == shift and
                row["q3_step_fibre_rebased"] is True and
                row["q3_bounded_step_fibre_size"] ==
                row["q3_canonical_fibre_size"] == 27 and
                row["bounded_step_word_length"] == len(step) and
                row["canonical_word_length"] == len(canon),
                "q3 fibre rebasing receipt")

    # Small exact factor computations: P has 504 elements, G9 2916, and B2 27.
    p_group = models["_P_GROUP"]
    g9_group = models["_G9_GROUP"]
    require(len(p_group) == 504 and len(g9_group) == 2916, "coarse factor orders")
    g9_derived = models["_G9_DERIVED"]
    b2_derived = derived_from_two(pc3.zero(), b2_images[0], b2_images[1],
                                  pc3.mul, pc3.inverse, 27)

    scan = data["direct_word_scan"]
    evaluated = scan["evaluated_candidates"]
    require(scan["total_candidates"] == 162 and 1 <= evaluated <= 162,
            "direct scan universe/evaluated count")
    actual_gates = {name: [] for name in
                    ("roof", "charming", "hexagon", "pentagon", "dtilde_applicable",
                     "dtilde_pass", "onto", "settlement_tested", "settled")}
    onto_p_cache: dict[Perm, bool] = {}
    onto_g_cache: dict[Perm, bool] = {}
    onto_b_cache: dict[tuple[int, ...], bool] = {}
    settlement_cache: dict[tuple[tuple[Perm, ...],
                                 tuple[tuple[int, ...], ...]], bool] = {}
    p4_marked = [row["coords"] for row in pc4.receipt["marked_generators"]]
    p4_relations = pure_relations(4)
    settlement_contract = scan["settlement_crosscheck_contract"]
    identity6 = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    require(settlement_contract == {
        "checked_for_every_onto_candidate": True,
        "source_abelianization_matrix": identity6,
        "Pi4_frattini_quotient": "PB4_ab mod 3 = (C3)^6",
        "Pi4_automorphism_theorem": (
            "Burnside basis theorem: a finite p-group endomorphism inducing an "
            "automorphism on G/Phi(G) is an automorphism"),
        "Pi4_relation_count": 11,
        "Pi4_descent": (
            "PB4 relators replay in exponent-three Pi4, so the verbal quotient "
            "receives the endomorphism"),
        "Q4_factor_method": (
            "four P and four G9 marked factor automorphisms; H9 is invariant "
            "because all six images are H9 words"),
        "global_Q4_and_Pi4_assertions_at_most_once": True,
    }, "settlement cross-check theorem receipt")
    correction_words = [row["word"] for row in records]
    hex_q0_contexts = elem_hex_pairs(q0[0], q0[1], one_q0, perm_mul, perm_inv)
    hex_b_contexts = elem_hex_pairs(b2_images[0], b2_images[1],
                                    pc3.zero(), pc3.mul, pc3.inverse)
    pent_q4_contexts = elem_pairs(models["Q4"], perm_one(144), perm_mul)
    pent_p4_contexts = elem_pairs(p4_marked, pc4.zero(), pc4.mul)
    hex_q0_corrections = context_cache(hex_q0_contexts, correction_words,
                                       one_q0, perm_mul, perm_inv)
    hex_b_corrections = context_cache(hex_b_contexts, correction_words,
                                      pc3.zero(), pc3.mul, pc3.inverse)
    pent_q4_corrections = context_cache(pent_q4_contexts, correction_words,
                                        perm_one(144), perm_mul, perm_inv)
    pent_p4_corrections = context_cache(pent_p4_contexts, correction_words,
                                        pc4.zero(), pc4.mul, pc4.inverse)
    correction_exponents = [f2_exponent_sums(word) for word in correction_words]
    total = 0
    for power in powers:
        base_hex_q0 = context_base(power["word"], hex_q0_contexts,
                                   one_q0, perm_mul, perm_inv)
        base_q0 = base_hex_q0[0]
        base_hex_b = context_base(power["word"], hex_b_contexts,
                                  pc3.zero(), pc3.mul, pc3.inverse)
        base_pent_q4 = context_base(power["word"], pent_q4_contexts,
                                    perm_one(144), perm_mul, perm_inv)
        base_pent_p4 = context_base(power["word"], pent_p4_contexts,
                                    pc4.zero(), pc4.mul, pc4.inverse)
        power_exponents = f2_exponent_sums(power["word"])
        for correction_index, correction_row in enumerate(records):
            if total >= evaluated:
                break
            total += 1
            candidate: list[int] | None = None
            hex_q0_values = context_values(base_hex_q0, hex_q0_corrections,
                                            correction_index, perm_mul)
            hex_b_values = context_values(base_hex_b, hex_b_corrections,
                                           correction_index, pc3.mul)
            value_q0, value_b = hex_q0_values[0], hex_b_values[0]
            value_p = restrict_perm_block(value_q0, 0, 9)
            value_g = restrict_perm_block(value_q0, 9, 27)
            roof = value_q0 == base_q0
            if roof:
                actual_gates["roof"].append(total)
            charming = value_g in g9_derived and value_b in b2_derived
            if roof and charming:
                actual_gates["charming"].append(total)
            else:
                continue
            hex_ok = True
            if any(x != one_q0 for x in elem_hex(hex_q0_values, q0[0], q0[1],
                                                  one_q0, perm_mul, perm_inv)):
                hex_ok = False
            if any(x != pc3.zero() for x in elem_hex(
                    hex_b_values, b2_images[0], b2_images[1],
                    pc3.zero(), pc3.mul, pc3.inverse)):
                hex_ok = False
            if not hex_ok:
                continue
            actual_gates["hexagon"].append(total)
            pent_ok = True
            pent_q4_values = context_values(base_pent_q4, pent_q4_corrections,
                                             correction_index, perm_mul)
            pent_p4_values = context_values(base_pent_p4, pent_p4_corrections,
                                             correction_index, pc4.mul)
            if elem_pent(pent_q4_values, perm_one(144), perm_mul, perm_inv) != perm_one(144):
                pent_ok = False
            if elem_pent(pent_p4_values, pc4.zero(), pc4.mul, pc4.inverse) != pc4.zero():
                pent_ok = False
            if not pent_ok:
                continue
            actual_gates["pentagon"].append(total)
            candidate_exponents = [power_exponents[j] +
                                   correction_exponents[correction_index][j]
                                   for j in range(2)]
            if candidate_exponents == [0, 0]:
                actual_gates["dtilde_applicable"].append(total)
                candidate = reduce_word(power["word"] + correction_row["word"])
                dw = dtilde_word(candidate)
                d_ok = (elem_eval(dw, models["Q4"], perm_one(144), perm_mul, perm_inv) ==
                        perm_one(144) and
                        pc_eval(dw, p4_marked, pc4) == pc4.zero())
                if d_ok:
                    actual_gates["dtilde_pass"].append(total)
            conj_p = paper_conjugate(value_p, p[1], one_p, perm_mul, perm_inv)
            conj_g = paper_conjugate(value_g, g9[1], one_g9, perm_mul, perm_inv)
            if value_p not in onto_p_cache:
                onto_p_cache[value_p] = len(enumerate_generated(
                    one_p, [p[0], conj_p], perm_mul, perm_inv, 504)) == 504
            if value_g not in onto_g_cache:
                onto_g_cache[value_g] = len(enumerate_generated(
                    one_g9, [g9[0], conj_g], perm_mul, perm_inv, 2916)) == 2916
            conj_b = paper_conjugate(value_b, b2_images[1], pc3.zero(),
                                     pc3.mul, pc3.inverse)
            if value_b not in onto_b_cache:
                onto_b_cache[value_b] = len(enumerate_generated(
                    pc3.zero(), [b2_images[0], conj_b], pc3.mul, pc3.inverse, 27)) == 27
            onto_p, onto_g, onto_b = (onto_p_cache[value_p], onto_g_cache[value_g],
                                      onto_b_cache[value_b])
            if not (onto_p and onto_g and onto_b):
                continue
            actual_gates["onto"].append(total)
            actual_gates["settlement_tested"].append(total)
            if candidate is None:
                candidate = reduce_word(power["word"] + correction_row["word"])
            source_words = source_words_m0(candidate)
            require(exponent_matrix(source_words, 6) == identity6,
                    "candidate settlement abelianization matrix")
            q4_images = tuple(elem_eval(
                w, models["Q4"], perm_one(144), perm_mul, perm_inv)
                for w in source_words)
            p4_images = tuple(pc_eval(w, p4_marked, pc4) for w in source_words)
            settlement_key = (q4_images, p4_images)
            if settlement_key not in settlement_cache:
                settlement_cache[settlement_key] = try_candidate_settlement(
                    source_words, q4_images, p4_images, pc4, models, p4_relations)
            if settlement_cache[settlement_key]:
                actual_gates["settled"].append(total)
        if total >= evaluated:
            break
    claimed = scan["gate_pass_indices"]
    for name in actual_gates:
        require(claimed[name] == actual_gates[name], f"direct gate bitset {name}")
    require(claimed["settlement_tested"] == claimed["onto"], "settlement scheduling")
    require(scan["settlement_image_cache_size"] == len(settlement_cache),
            "settlement image cache size")
    settlement_perf = scan["settlement_performance"]
    require(settlement_perf["structural_settlement_tests"] == len(settlement_cache) and
            0 <= settlement_perf["small_factor_bijectivity_calls"] <=
            8 * len(settlement_cache) and
            0 <= settlement_perf["small_factor_cache_hits"] and
            settlement_perf["small_factor_bijectivity_calls"] +
            settlement_perf["small_factor_cache_hits"] <= 8 * len(settlement_cache) and
            settlement_perf["global_Q4_bijectivity_calls"] ==
            settlement_perf["global_Pi4_bijectivity_calls"] ==
            (1 if claimed["settled"] else 0),
            "bounded structural/global settlement counters")
    cursor = 0
    for power_record in scan["power_records"]:
        width = power_record["evaluated_candidates"]
        lo, hi = cursor + 1, cursor + width
        counts = power_record["progressive_counts"]
        require(counts["total"] == width and all(
            counts[name] == sum(lo <= i <= hi for i in claimed[name])
            for name in ("roof", "charming", "hexagon", "pentagon",
                         "dtilde_applicable", "dtilde_pass", "onto", "settled")),
            "per-power progressive counts")
        cursor = hi
    require(cursor == evaluated, "power-record evaluated coverage")
    solutions = scan["solutions"]
    require(scan["solution_count"] == len(solutions) == len(claimed["settled"]),
            "settled solution count")
    if solutions:
        require(len(solutions) == 1 and claimed["settled"] == [evaluated] and
                scan["exhaustive"] is False and scan["stop_reason"] == "FIRST_TYPED_WITNESS",
                "first-witness stop")
        sol = solutions[0]
        require(all(sol[name] is True for name in
                    ("roof_reduction_exact", "charming", "hexagon_exact",
                     "pentagon_exact", "onto_Q0", "onto_B2_q3",
                     "arithmetic_outside_by_index_three",
                     "exponent_not_divisible_by_three")) and
                sol["marking_m"] == 0 and sol["lambda"] == 1,
                "selected exact side gates")
        require(sol["typed_source_word"] == reduce_word(
            powers[[x["exponent"] for x in powers].index(sol["exponent"])]["word"] +
            records[sol["correction_index"] - 1]["word"]), "selected word reconstruction")
        diag = sol["dtilde_diagnostic"]
        applicable = f2_exponent_sums(sol["typed_source_word"]) == [0, 0]
        require(diag["applicable"] is applicable and diag["terminal_gate"] is False and
                diag["raw_exponent_sums"] == f2_exponent_sums(sol["typed_source_word"]),
                "nullable Dtilde diagnostic typing")
        if applicable:
            require(diag["word"] == dtilde_word(sol["typed_source_word"]) and
                    isinstance(diag["value"], bool), "applicable Dtilde diagnostic")
        else:
            require(diag["word"] is None and diag["value"] is None,
                    "nonapplicable Dtilde must be null")
        settlement = sol["settlement"]
        source_words = source_words_m0(sol["typed_source_word"])
        require(settlement["source_words"] == source_words and
                settlement["Q4_bijective"] is True and
                settlement["Pi4_q3_bijective"] is True and
                settlement["Pi4_frattini_matrix"] == identity6 and
                settlement["Pi4_frattini_quotient"] ==
                "PB4_ab mod 3 = (C3)^6" and
                settlement["Pi4_automorphism_theorem"] ==
                settlement_contract["Pi4_automorphism_theorem"],
                "settlement certificate/source words")
        q4_marks = models["Q4"]
        q4_images = [elem_eval(w, q4_marks, perm_one(144), perm_mul, perm_inv)
                     for w in source_words]
        # The structural factor/Frattini test above has already replayed this
        # candidate and reconstructed the settled bit.  The positive-only
        # records below independently bind the producer's inverse receipts;
        # they do not repeat the eight small-factor BFS computations.
        q4_inverse_words = settlement["Q4_inverse_words"]
        require(len(q4_inverse_words) == 6 and all(
            elem_eval(w, q4_images, perm_one(144), perm_mul, perm_inv) == q4_marks[i]
            for i, w in enumerate(q4_inverse_words)),
            "independent coarse settlement surjectivity")
        p4_marks = p4_marked
        p4_images = [pc_eval(w, p4_marks, pc4) for w in source_words]
        p4_inverse_words = settlement["Pi4_inverse_words"]
        require(len(p4_inverse_words) == 6 and all(
            pc_eval(w, p4_images, pc4) == pc4._coord(p4_marks[i])
            for i, w in enumerate(p4_inverse_words)),
            "independent Pi4 marked settlement surjectivity")
        forward, inverse = validate_inverse_pc_maps(
            pc4, settlement["Pi4_forward_pc_images"],
            settlement["Pi4_inverse_pc_images"])
        for source_mark, expected in zip(p4_marks, p4_images):
            require(pc4.eval_coords_by_images(source_mark, pc4, forward) == expected,
                    "Pi4 marked/pc settlement binding")
        require(claimed["settled"] == [evaluated],
                "independent first settled bitset")
    else:
        require(evaluated == 162 and scan["exhaustive"] is True and
                scan["stop_reason"] == "ALL_162_EXHAUSTED" and
                claimed["settled"] == [], "negative exhaustive scan")


def validate_optional_typed(block: dict[str, Any]) -> None:
    if not block.get("executed", False):
        require(block.get("status") in
                ("MISSING_Q3_TYPED_D2", "BYPASSED_BY_EXACT_WORD_CORRECTION"),
                "unexecuted typed status drift")
        require(block.get("no_untwisted_replacement") is True, "untwisted substitution not blocked")
        if block.get("status") == "BYPASSED_BY_EXACT_WORD_CORRECTION":
            require(block.get("d2_bypassed_by_exact_word") is True and
                    block.get("word_correction_exact_replay") is True,
                    "false exact-word bypass")
        return
    matrices = block.get("chief_action_matrices")
    require(isinstance(matrices, list) and matrices, "missing chief action matrices")
    for matrix in matrices:
        require(isinstance(matrix, list) and matrix and all(len(row) == len(matrix) for row in matrix),
                "chief action matrix shape")
        require(all(x in (0, 1, 2) for row in matrix for x in row), "chief action field")
    require(block.get("chief_action_sha256") == digest_obj(matrices), "chief action digest")
    side = block.get("side_gate_rows")
    require(isinstance(side, list), "missing exact side-gate rows")
    require(block.get("side_gate_sha256") == digest_obj(side), "side-gate digest")


def validate_terminal(data: dict[str, Any]) -> None:
    token = data.get("terminal_token")
    require(token in ALLOWED_TERMINALS, "unregistered terminal token")
    if "direct_word_scan" in data:
        scan = data["direct_word_scan"]
        if scan.get("solution_count") == 1:
            expected = "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION"
        else:
            require(scan.get("solution_count") == 0 and
                    scan.get("exhaustive") is True and
                    scan.get("evaluated_candidates") == 162,
                    "direct-route terminal lacks exact positive or exhaustive negative")
            expected = "B345_Q3_MISSING_TYPED_D2"
        require(token == expected,
                "direct-route solution count and terminal token are not bidirectional")
    if token == "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION":
        chief = data.get("chief_fox", {})
        require(chief.get("executed") is False and
                chief.get("status") == "BYPASSED_BY_EXACT_WORD_CORRECTION" and
                chief.get("d2_bypassed_by_exact_word") is True and
                chief.get("word_correction_exact_replay") is True,
                "false exact terminal: no exact word bypass")
        require(data["direct_word_scan"]["solution_count"] == 1 and
                data["selected_solution"] == data["direct_word_scan"]["solutions"][0],
                "false exact terminal: selected direct solution")
    if token == "B345_Q3_MISSING_TYPED_D2":
        require(data["chief_fox"]["status"] == "MISSING_Q3_TYPED_D2",
                "missing-d2 token without exact boundary")
        require("Q3_TYPED_D2" in data["typed_relative_stage"]["first_missing_map"],
                "missing-d2 token lacks first missing map")
        require(data["direct_word_scan"]["solution_count"] == 0 and
                data["direct_word_scan"]["exhaustive"] is True and
                data["direct_word_scan"]["evaluated_candidates"] == 162,
                "missing-d2 promoted before exhaustive word fibre")
    if token == "B345_Q3_MISSING_RELATIVE_HORN_EFFECTIVITY":
        require(data.get("production_anupq_calls") == 0 and
                data.get("PB5_skipped_before_known_typed_stop") is True,
                "relative-horn stop did not precede ANUPQ")
    require(token != "B345_Q3_MISSING_TYPED_M5",
            "coarse M5 is not an allowed early stop for the updated 157da contract")


def validate_receipt(data: dict[str, Any], repo_root: Path) -> None:
    require(data.get("schema") == SCHEMA, "schema")
    require(data.get("terminal_token") in ALLOWED_TERMINALS, "unregistered terminal token")
    require(data.get("status") == data.get("terminal_token"), "status/token drift")
    require(data.get("q_level") == 3, "q level")
    expected_pins = {
        "row18_producer": (ROW18_SOURCE, ROW18_SHA),
        "row18_checker": (ROW18_CHECKER, ROW18_CHECKER_SHA),
        "phase2b_receipt": (PHASE2B, PHASE2B_SHA),
        "frozen_word_artifact": (WORDS, WORDS_SHA),
        "row18_core": (CORE, CORE_SHA),
    }
    for key, (path, sha) in expected_pins.items():
        row = data["pins"][key]
        require(row == {"path": str(path).replace("\\", "/"), "sha256": sha}, f"pin {key}")
        require(digest_file(repo_root / path) == sha, f"local pin SHA {key}")
    formulas = formula_manifest()
    require(digest_obj(formulas) == FORMULA_SHA, "checker formula digest drift")
    require(data["formulas"] == formulas, "formula manifest differs from independent reconstruction")
    require(data["formula_sha256"] == FORMULA_SHA, "formula SHA")
    models = validate_short_gate(data)
    token = data["terminal_token"]
    if token == "B345_Q3_MISSING_RELATIVE_HORN_EFFECTIVITY":
        gate = data["short_common_quotient_gate"]
        require(not (gate["Q4_common_q3_quotient_trivial"] and
                     gate["Q0_common_q3_quotient_trivial"]),
                "spurious nontrivial-common-quotient stop")
        require(data.get("roof_power_a_mod_9") is None, "early stop roof power")
        validate_terminal(data)
        return
    if token == "B345_Q3_UNKNOWN_RESOURCE":
        require(data.get("phase") == "PB5_ANUPQ" and
                data.get("production_anupq_calls") == 1 and
                data.get("no_mathematical_obstruction_claimed") is True and
                isinstance(data.get("reason"), str), "resource-stop receipt")
        require(data.get("roof_power_a_mod_9") is None, "resource stop roof power")
        validate_terminal(data)
        return
    require(data["short_common_quotient_gate"]["Q4_common_q3_quotient_trivial"] is True and
            data["short_common_quotient_gate"]["Q0_common_q3_quotient_trivial"] is True,
            "direct-product pullback gate")
    c = data["construction"]
    require(c["anupq_calls"] == 1 and c["anupq_group"] == "PB5 only", "ANUPQ call budget")
    require(c["anupq_version"] == "3.3.3", "ANUPQ version")
    require(c["class_bound_requested"] == 4 and c["exponent_law"] == 3,
            "ANUPQ terminal parameters")
    require(c["terminal_not_truncated"] is True and c["observed_PB5_class"] <= 3,
            "class-four request did not terminate at class <=3")
    require(c["large_group_full_element_enumeration"] is False and
            c["bounded_kernel_enumeration_order"] == 27 and c["cayley_tables"] is False,
            "forbidden enumeration/table")
    require(c["coarse_M5"] is False, "forbidden coarse M5")
    expect_full_pb5 = token == "B345_Q3_MISSING_TYPED_D2"
    require(c["direct_scan_precedes_full_PB5_collector"] is True and
            c["full_PB5_collector_built"] is expect_full_pb5 and
            c["PB5_map_bundle_built"] is expect_full_pb5,
            "PB5 post-scan construction order")
    require("does not rerun ANUPQ" in c["independent_checker_anupq_contract"] and
            "Levi-van der Waerden" in c["independent_checker_anupq_contract"],
            "ANUPQ maximality contract not explicit")
    group_receipts = data["groups"]
    groups: dict[str, PcCollector] = {}
    for key, expected_rank in (("PB3", 3), ("PB4", 4)):
        rec = group_receipts[key]
        require(rec["rank"] == expected_rank and rec["name"] == f"Pi{expected_rank}[3]",
                f"group identity {key}")
        pc = PcCollector(rec)
        pc.validate()
        groups[rec["name"]] = pc
    if expect_full_pb5:
        rec = group_receipts["PB5"]
        require(rec["rank"] == 5 and rec["name"] == "Pi5[3]", "PB5 identity")
        pc = PcCollector(rec)
        pc.validate()
        groups["Pi5[3]"] = pc
    else:
        rec = group_receipts["PB5"]
        require(rec["name"] == "Pi5[3]" and rec["rank"] == 5 and
                rec["summary_only"] is True and rec["exponent"] == 3 and
                rec["nilpotency_class"] <= 3 and
                rec["full_collector_and_maps_bypassed_by_exact_word"] is True,
                "PB5 exact-word summary")
    maps = data["maps"]
    if expect_full_pb5:
        require(len(maps["cofaces_3_4"]) == 5 and len(maps["cofaces_4_5"]) == 6,
                "coface counts")
        require(len(maps["deletions_4_3"]) == 4 and len(maps["deletions_5_4"]) == 5,
                "deletion counts")
        for family in maps.values():
            for record in family:
                validate_map(record, groups)
        endpoints = data["endpoint_retractions"]
        require(endpoints["status"] == "REUSED_DELETION_RECORDS" and
                endpoints["PB5_to_PB4"] == maps["deletions_5_4"][-1] and
                endpoints["PB4_to_PB3"] == maps["deletions_4_3"][-1],
                "endpoint retractions do not reuse the terminal deletion records")
    else:
        require(maps["status"] == "BYPASSED_BY_EXACT_WORD_CORRECTION" and
                all(maps[k] == [] for k in ("cofaces_3_4", "cofaces_4_5",
                                             "deletions_4_3", "deletions_5_4")) and
                data["endpoint_retractions"]["status"] ==
                "BYPASSED_BY_EXACT_WORD_CORRECTION", "exact-word map bypass")
    validate_direct_route(data, groups["Pi3[3]"], groups["Pi4[3]"], models, repo_root)
    typed = data["typed_relative_stage"]
    require(typed["coarse_M5_required"] is False and typed["fine_syzygy_target"] == "Pi5[3]",
            "updated relative-stage typing")
    require(typed["q3_system_ready"] is True, "q3 system not ready")
    require(typed["common_quotient_C4_trivial"] is True and
            typed["pullback_certified"]["E4"] == "Q4 x Pi4[3]" and
            typed["pullback_certified"]["V_to_Pi4_injective"] is True and
            typed["actual_coarse_trivial_correction_fibre_order"] == 27,
            "resolved direct-product pullback")
    row18_typing = typed["frozen_row18_v2_typing"]
    require(row18_typing["producer_sha256"] == ROW18_SHA and
            "not the ambient E^4 source" in row18_typing["coarse_Q4_candidate"] and
            row18_typing["runtime_pullback_receipt_available_here"] is True,
            "row18-v2 Q4 typing boundary")
    validate_optional_typed(data["chief_fox"])
    require(data["coset_sign_comparison"]["executed"] is False,
            "comparison promoted before typed d2")
    p = data["performance"]
    require(p["one_gap_process"] is True and p["anupq_calls"] == 1 and
            p["large_group_full_enumeration"] is False and
            p["bounded_order27_enumeration"] is True and
            p["frozen_972_rows_evaluated_once"] is True and
            p["settlement_image_cache"] is True and p["pc_generator_cap"] == 175,
            "performance contract")
    if token == "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION":
        require(data["roof_power_a_mod_9"] in (1, 2, 4, 5, 7, 8), "selected roof power")
    else:
        require(data["roof_power_a_mod_9"] is None, "negative terminal roof power")
    validate_terminal(data)


def expect_reject(fn: Any, label: str) -> None:
    try:
        fn()
    except (Reject, KeyError, IndexError, TypeError, ValueError):
        return
    raise AssertionError(f"mutation was accepted: {label}")


def self_test() -> None:
    formulas = formula_manifest()
    require(digest_obj(formulas) == FORMULA_SHA, "selftest formula digest drift")
    v, y, one3 = (1, 2, 0), (1, 0, 2), perm_one(3)
    literal_conjugate = paper_conjugate(v, y, one3, perm_mul, perm_inv)
    require(literal_conjugate == perm_mul(perm_mul(v, y), perm_inv(v)) and
            literal_conjugate != perm_mul(perm_mul(perm_inv(v), y), v),
            "paper-product conjugation orientation")
    expect_reject(lambda: validate_terminal({
        "terminal_token": "B345_Q3_NO_ACTUAL_F3_CHIEF",
        "direct_word_scan": {"solution_count": 1, "exhaustive": False,
                             "evaluated_candidates": 7},
    }), "direct-route terminal relabel")
    require([len(formulas["presentations"][x]["relations"]) for x in ("PB3", "PB4", "PB5")]
            == [2, 11, 35], "presentation relation counts")
    mutated = json.loads(json.dumps(formulas))
    mutated["cofaces_3_4"][1][0] = list(reversed(mutated["cofaces_3_4"][1][0]))
    expect_reject(lambda: require(mutated == formula_manifest(), "coface orientation"),
                  "coface orientation")
    cyclic = {
        "name": "Pi1[3]", "rank": 1, "order_decimal": "3", "exponent": 3,
        "nilpotency_class": 1, "generator_count": 1, "relative_orders": [3],
        "power_relations": [[0]], "inverses": [[2]], "conjugate_relations": [],
        "inverse_conjugate_relations": [], "marked_generators": [],
        "original_relations": [], "original_relator_images": [],
    }
    PcCollector(cyclic).validate()
    bad_pc = json.loads(json.dumps(cyclic))
    bad_pc["power_relations"][0][0] = 1
    expect_reject(lambda: PcCollector(bad_pc), "pc relation")
    rank2_elementary = {
        "name": "E2[3]", "rank": 2, "order_decimal": "9", "exponent": 3,
        "nilpotency_class": 1, "generator_count": 2,
        "relative_orders": [3, 3], "power_relations": [[0, 0], [0, 0]],
        "inverses": [[2, 0], [0, 2]],
        "conjugate_relations": [{"i": 2, "j": 1, "coords": [0, 1]}],
        "inverse_conjugate_relations": [{"i": 2, "j": 1, "coords": [0, 1]}],
    }
    e2 = PcCollector(rank2_elementary)
    e2_identity = [e2.unit(1), e2.unit(2)]
    validate_inverse_pc_maps(e2, e2_identity, e2_identity)
    expect_reject(lambda: e2.unit(0), "pc unit index")
    e2_swapped = [e2.unit(2), e2.unit(1)]
    expect_reject(lambda: validate_inverse_pc_maps(e2, e2_identity, e2_swapped),
                  "rank-2 noninverse pair")
    typed = {
        "executed": True,
        "chief_action_matrices": [[[1, 0], [0, 1]]],
        "chief_action_sha256": digest_obj([[[1, 0], [0, 1]]]),
        "side_gate_rows": [[1, 0]],
        "side_gate_sha256": digest_obj([[1, 0]]),
    }
    validate_optional_typed(typed)
    bad_action = json.loads(json.dumps(typed))
    bad_action["chief_action_matrices"][0][0][0] = 2
    expect_reject(lambda: validate_optional_typed(bad_action), "chief action entry")
    bad_side = json.loads(json.dumps(typed))
    bad_side["side_gate_rows"][0][0] = 2
    expect_reject(lambda: validate_optional_typed(bad_side), "side-gate row")
    bad_k5 = json.loads(json.dumps(formulas["k5"]))
    square = next(f for f in bad_k5["facets"] if f["kind"] == "square")
    square["oriented_cycle"][0], square["oriented_cycle"][1] = (
        square["oriented_cycle"][1], square["oriented_cycle"][0])
    expect_reject(lambda: require(bad_k5 == build_k5(), "square face"), "square face")
    false_terminal = {
        "terminal_token": "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
        "chief_fox": {"executed": False},
    }
    expect_reject(lambda: validate_terminal(false_terminal), "false terminal")
    print("D972_B345_Q3_CHECKER_SELFTEST_PASS mutations=9 orientation_canaries=1 "
          "rank2_pc_inverse_canaries=2 "
          f"formula_sha256={digest_obj(formulas)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        require(args.artifact is None, "--self-test does not accept an artifact")
        self_test()
        return 0
    require(args.artifact is not None, "artifact path is required")
    data = json.loads(args.artifact.read_text(encoding="utf-8"))
    repo_root = Path(__file__).resolve().parents[1]
    validate_receipt(data, repo_root)
    pb5_order = data.get("groups", {}).get("PB5", {}).get("order_decimal", "SKIPPED")
    print("B345_Q3_CHECKER_PASS "
          f"terminal={data['terminal_token']} formula_sha256={data['formula_sha256']} "
          f"PB5_order={pb5_order}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(f"B345_Q3_CHECKER_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
