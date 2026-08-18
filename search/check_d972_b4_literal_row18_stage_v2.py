#!/usr/bin/env python3
"""Independent checker for the literal row-18 C2^24 stage receipt.

No producer module is imported.  The checker reconstructs the marked
E/V/PSL(2,8), MakeGn(9), four strand deletions, all 24 source words, the
natural Artin action, the literal 18+5*28 A.18 transport, and the complete
64-element correction fibre for the root and its exact GT square.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "search/certs/d972_phase2b_nonsplit_v1_20260813.json"
SOURCE_SHA = "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9"
SOURCE_CHECK = ROOT / "search/certs/d972_phase2b_nonsplit_v1_check_20260813.json"
SOURCE_CHECK_SHA = "90db0fc500eb44bd905059d7a00dfaf4920c8c9890ed151d773141456fd059bb"
MAPS_FILE = ROOT / "search/certs/d972_b4_marity_reduction_maps_v1.json"
MAPS_SHA = "6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2"
WORDS_FILE = ROOT / "search/certs/d972_b4_word_key_artifact_v1_20260816.json"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
TUPLES_FILE = ROOT / "search/certs/nf972_sourcemap_a_tuples_v2_20260804.json"
TUPLES_SHA = "cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801"
LITERAL_FILE = ROOT / "search/certs/d972_b4_p2_magnus_input_v2_20260816.json"
LITERAL_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
PAB_FILE = ROOT / "thirdparty/packageGT/extracted/PackageGT/PaB.py"
PAB_SHA = "e54c08d3437d0706b4639d7db31f7177c1c82de9c2f820fa7b194fa1c4e378f2"
CORE_PRODUCER = ROOT / "search/d972_d972core_c2six_intersection_v2.g"
CORE_PRODUCER_SHA = "577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c"

PREFIX_SHA = "62ccbb87e2b27784b5330812252a2eaf247fea0fef4eda078ea6724c5b2a31e6"
SEED_SHA = "366c893977a0684a294e8bd488741c735016ec5caf18804415dfc73acdb09822"
A18_SHA = "1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722"
PRESENTATION_SHA = "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305"
DTILDE_SHA = "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef"
KEY_DIGEST = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_DIGEST = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
EXPECTED_KEY = [0, [[2, 0], [7, 0], [0, 0]], list(range(1, 10))]
EXPECTED_WORD = [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,1,1,-2,1,1,1,1,2,1,-2,-2,1,1]
LABEL_ROWS = (
    ("1", "1", "X", "X"), ("1", "X", "1", "Z"),
    ("1", "Z", "Z", "1"), ("X", "1", "1", "Y"),
    ("Z", "1", "Y", "1"), ("Y", "Y", "1", "1"),
)
EXPECTED_MAPS = [
    {"index": 1, "deleted_strand": 1, "generator_images": [[], [], [], [1], [2], [3]]},
    {"index": 2, "deleted_strand": 2, "generator_images": [[], [1], [2], [], [], [3]]},
    {"index": 3, "deleted_strand": 3, "generator_images": [[1], [], [2], [], [3], []]},
    {"index": 4, "deleted_strand": 4, "generator_images": [[1], [2], [], [3], [], []]},
]
COFACES = (
    ("123", (1,), (4,)), ("234", (4,), (6,)),
    ("12,3,4", (2, 4), (6,)),
    ("1,23,4", (1, 2), (5, 6)),
    ("1,2,34", (1,), (4, 5)),
)
# Natural action p^sigma=sigma^-1*p*sigma in canonical order.
ARTIN = (
    ((1,), (-1,4,1), (-1,5,1), (2,), (3,), (6,)),
    ((-4,2,4), (1,), (3,), (4,), (-4,6,4), (5,)),
    ((1,), (-6,3,6), (2,), (-6,5,6), (4,), (6,)),
)
PAB_INVERSE = (
    ((1,), (4,), (5,), (1,2,-1), (1,3,-1), (6,)),
    ((2,), (4,1,-4), (3,), (4,), (6,), (4,5,-4)),
    ((1,), (3,), (6,2,-6), (5,), (6,4,-6), (6,)),
)
PURE_BRAID_WORDS = (
    (1,1), (2,1,1,-2), (3,2,1,1,-2,-3),
    (2,2), (3,2,2,-3), (3,3),
)
SINGLE_SUPPORT_PAIRS = ((4,5),(2,3),(1,3),(1,2))
DEG_E, DEG_P, DEG_G9 = 72, 9, 27
Perm = tuple[int, ...]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=False).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(compact(value)).hexdigest()


def load(path: Path, sha: str) -> dict:
    require(file_sha(path) == sha, f"SHA drift: {path}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(obj, dict), f"object drift: {path}")
    return obj


def one(n: int) -> Perm:
    return tuple(range(n))


def compose(left: Perm, right: Perm) -> Perm:
    """GAP-compatible product: apply left, then right."""
    return tuple(right[left[i]] for i in range(len(left)))


def inverse(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def power(p: Perm, n: int) -> Perm:
    if n < 0:
        return power(inverse(p), -n)
    out = one(len(p))
    while n:
        if n & 1:
            out = compose(out, p)
        p = compose(p, p)
        n >>= 1
    return out


def paper_product(values: Iterable[Perm]) -> Perm:
    vals = tuple(values)
    require(bool(vals), "empty paper product")
    out = one(len(vals[0]))
    for value in reversed(vals):
        out = compose(out, value)
    return out


def closure(gens: Iterable[Perm], degree: int | None = None) -> set[Perm]:
    gs = tuple(gens)
    require(bool(gs) or degree is not None, "closure degree missing")
    n = degree if degree is not None else len(gs[0])
    identity = one(n)
    seen = {identity}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for g in gs:
            y = compose(x, g)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def marked_hom_table(domain: Sequence[Perm], image: Sequence[Perm]) -> dict[Perm,Perm]:
    """Build the marked homomorphism table and reject any relation drift."""
    d0=one(len(domain[0])); i0=one(len(image[0])); table={d0:i0}; queue=deque([d0])
    steps=((domain[0],image[0]),(inverse(domain[0]),inverse(image[0])),
           (domain[1],image[1]),(inverse(domain[1]),inverse(image[1])))
    while queue:
        x=queue.popleft()
        for ds,is_ in steps:
            y=compose(x,ds); z=compose(table[x],is_)
            if y in table: require(table[y]==z,"marked quotient relation drift")
            else: table[y]=z; queue.append(y)
    return table


FACTOR_XY_ROWS = ((3,5),(1,5),(0,4),(0,3))


def factor_auto_certificate(label: str, domain: Sequence[Perm], tuple_gens: Sequence[Perm],
                            selected: Sequence[Perm], degree: int, order: int) -> list[dict]:
    """Independently prove the selected six rows come from four factor automorphisms."""
    original_blocks = [blocks(g, degree) for g in tuple_gens]
    selected_blocks = [blocks(g, degree) for g in selected]
    receipt: list[dict] = []
    for c, (xrow, yrow) in enumerate(FACTOR_XY_ROWS):
        table = marked_hom_table(domain,
                                 (selected_blocks[xrow][c], selected_blocks[yrow][c]))
        require(len(table) == order and len(set(table.values())) == order,
                f"{label} factor automorphism drift")
        for j in range(6):
            require(table[original_blocks[j][c]] == selected_blocks[j][c],
                    f"{label} tuple binding drift")
        receipt.append({"family":label,"coordinate":c+1,"x_source_row":xrow+1,
                        "y_source_row":yrow+1,"factor_order":order,
                        "bijective":True,"all_six_tuple_rows_bound":True})
    return receipt


def conjugate(value: Perm, by: Perm) -> Perm:
    return compose(compose(inverse(by), value), by)


def word_value(word: Sequence[int], gens: Sequence[Perm]) -> Perm:
    out = one(len(gens[0]))
    for raw in word:
        n = int(raw)
        require(n and abs(n) <= len(gens), "word alphabet drift")
        out = compose(out, gens[abs(n)-1] if n > 0 else inverse(gens[-n-1]))
    return out


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(n != 0, "zero letter")
        if out and out[-1] == -n:
            out.pop()
        else:
            out.append(n)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(n and abs(n) <= len(images), "substitution alphabet drift")
        image = list(images[abs(n)-1])
        out.extend(inv_word(image) if n < 0 else image)
    return free_reduce(out)


def braid_letter_auto(letter: int) -> tuple[tuple[int, ...], ...]:
    require(1 <= abs(letter) <= 3, "braid letter range")
    images: list[tuple[int, ...]] = [(i,) for i in range(1, 5)]
    i = abs(letter) - 1
    if letter > 0:
        images[i] = (i+1, i+2, -(i+1)); images[i+1] = (i+1,)
    else:
        images[i] = (i+2,); images[i+1] = (-(i+2), i+1, i+2)
    return tuple(images)


def braid_auto(word: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    images: list[list[int]] = [[i] for i in range(1, 5)]
    for letter in word:
        step = braid_letter_auto(int(letter))
        images = [substitute(w, step) for w in images]
    return tuple(tuple(w) for w in images)


def faithful_artin_replay() -> None:
    identity = tuple((i,) for i in range(1, 5))
    boundary = [1,2,3,4]
    for i in range(1, 4):
        require(braid_auto((i,-i)) == identity and braid_auto((-i,i)) == identity,
                "Artin inverse calibration")
        require(substitute(boundary, braid_auto((i,))) == boundary and
                substitute(boundary, braid_auto((-i,))) == boundary,
                "Artin boundary canary")
    require(braid_auto((1,2,1)) == braid_auto((2,1,2)) and
            braid_auto((2,3,2)) == braid_auto((3,2,3)) and
            braid_auto((1,3)) == braid_auto((3,1)), "Artin braid calibration")
    pure = tuple(tuple(w) for w in PURE_BRAID_WORDS)
    for i in range(1, 4):
        for j in range(6):
            natural = free_reduce([-i] + list(pure[j]) + [i])
            natural_rhs = substitute(ARTIN[i-1][j], pure)
            inverse_side = free_reduce([i] + list(pure[j]) + [-i])
            inverse_rhs = substitute(PAB_INVERSE[i-1][j], pure)
            require(braid_auto(natural) == braid_auto(natural_rhs),
                    "faithful natural Artin action drift")
            require(braid_auto(inverse_side) == braid_auto(inverse_rhs),
                    "faithful PackageGT inverse action drift")


def paper_word(parts: Sequence[Sequence[int]]) -> list[int]:
    return free_reduce(x for part in reversed(parts) for x in part)


def embed_blocks(values: Iterable[Perm]) -> Perm:
    out: list[int] = []
    offset = 0
    for p in values:
        out.extend(offset + x for x in p)
        offset += len(p)
    return tuple(out)


def blocks(value: Perm, degree: int) -> tuple[Perm, ...]:
    return tuple(tuple(value[i] - offset for i in range(offset, offset+degree))
                 for offset in range(0, len(value), degree))


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


def matrix_action(m: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    out = []
    for a, b in P1:
        x = gf8_mul(a, m[0][0]) ^ gf8_mul(b, m[1][0])
        y = gf8_mul(a, m[0][1]) ^ gf8_mul(b, m[1][1])
        line = (1, gf8_mul(y, gf8_inv(x))) if x else (0, 1)
        out.append(P1.index(line))
    return tuple(out)


def canonical_p() -> tuple[Perm, Perm, set[Perm]]:
    s = matrix_action(((1, 0), (1, 1)))
    t = matrix_action(((4, 3), (1, 5)))
    w = compose(s, inverse(t))
    x = power(w, 2)
    y = compose(compose(inverse(s), x), s)
    return x, y, closure((x, y))


def make_g9() -> tuple[Perm, Perm, set[Perm]]:
    n = 9
    r = tuple(list(range(1, n)) + [0])
    s = tuple((n-j) % n for j in range(n))
    def tr(p: Perm, block: int) -> Perm:
        out = list(range(3*n)); off = block*n
        for i in range(n): out[off+i] = off+p[i]
        return tuple(out)
    sr = compose(s, r)
    x = compose(compose(tr(r, 0), tr(s, 1)), tr(s, 2))
    y = compose(compose(tr(sr, 0), tr(r, 1)), tr(sr, 2))
    return x, y, closure((x, y))


def reconstruct_core() -> dict:
    source = load(SOURCE, SOURCE_SHA)
    source_check = load(SOURCE_CHECK, SOURCE_CHECK_SHA)
    maps = load(MAPS_FILE, MAPS_SHA)
    require(source.get("schema") == "d972_phase2b_nonsplit/v1", "source schema")
    require(source_check.get("all_checks_true") is True, "source checker gate")
    require(maps.get("maps") == EXPECTED_MAPS, "four-map drift")
    named = {k: tuple(source["candidate"]["original_generator_arrays"][k])
             for k in "abcuvwxyz"}
    x = tuple(source["candidate"]["selected_arrays"]["X"])
    y = tuple(source["candidate"]["selected_arrays"]["Y"])
    z = inverse(compose(y, x))
    e = closure((x, y)); module = tuple(named[k] for k in "uvwxyz")
    v = closure(module)
    require(len(e) == 32256 and len(v) == 64, "E/V order drift")
    require(all(conjugate(a, b) in v for a in v for b in (x, y)), "V normality")
    px, py, p = canonical_p(); pz = inverse(compose(py, px))
    gx, gy, g9 = make_g9(); gz = inverse(compose(gy, gx))
    quotient=marked_hom_table((x,y),(px,py))
    require(len(quotient)==32256 and len(set(quotient.values()))==504 and
            sum(value==one(DEG_P) for value in quotient.values())==64,
            "marked E/V to row-vector PSL quotient drift")
    return {"x": x, "y": y, "z": z, "e": e, "module": module, "v": v,
            "px": px, "py": py, "pz": pz, "p": p,
            "gx": gx, "gy": gy, "gz": gz, "g9": g9, "maps": maps}


def tuple_rows(core: dict, family: str) -> tuple[tuple[Perm, ...], ...]:
    target = {"E": (core["x"], core["z"], core["y"]),
              "P": (core["px"], core["pz"], core["py"]),
              "G9": (core["gx"], core["gz"], core["gy"])}[family]
    per_map = [tuple(word_value(w, target) for w in row["generator_images"])
               for row in core["maps"]["maps"]]
    return tuple(tuple(per_map[c][g] for c in range(4)) for g in range(6))


def module_masks(module: Sequence[Perm]) -> dict[Perm, int]:
    out: dict[Perm, int] = {}
    for mask in range(64):
        value = one(DEG_E)
        for i, g in enumerate(module):
            if mask & (1 << i): value = compose(value, g)
        out[value] = mask
    require(len(out) == 64, "module basis dependence")
    return out


def mask24(value: Perm, masks: dict[Perm, int]) -> int:
    out = 0
    for c, block in enumerate(blocks(value, DEG_E)):
        require(block in masks, "value outside V4")
        out |= masks[block] << (6*c)
    return out


def apply_matrix(mask: int, rows: Sequence[int]) -> int:
    out = 0
    for i, row in enumerate(rows):
        if mask & (1 << i): out ^= int(row)
    return out


def matmul(a: Sequence[int], b: Sequence[int]) -> list[int]:
    return [apply_matrix(x, b) for x in a]


def matrix_inverse(rows: Sequence[int]) -> list[int]:
    n = len(rows)
    require(all(0 <= int(row) < (1 << n) for row in rows), "matrix shape")
    left = [int(row) for row in rows]
    right = [1 << i for i in range(n)]
    for column in range(n):
        pivot = next((i for i in range(column,n) if left[i] & (1 << column)), None)
        require(pivot is not None, "singular matrix")
        left[column], left[pivot] = left[pivot], left[column]
        right[column], right[pivot] = right[pivot], right[column]
        for i in range(n):
            if i != column and left[i] & (1 << column):
                left[i] ^= left[column]; right[i] ^= right[column]
    require(left == [1 << i for i in range(n)], "matrix inverse reduction")
    return right


def matrix_word(word: Sequence[int], generators: Sequence[Sequence[int]]) -> list[int]:
    out = [1 << i for i in range(len(generators[0]))]
    for raw in word:
        n = int(raw)
        require(n and abs(n) <= len(generators), "matrix word alphabet")
        value = list(generators[abs(n)-1])
        out = matmul(out, value if n > 0 else matrix_inverse(value))
    return out


def matrix_commutator(a: Sequence[int], b: Sequence[int]) -> list[int]:
    return matmul(matmul(matmul(matrix_inverse(a),matrix_inverse(b)),a),b)


def matrix_permutation(rows: Sequence[int]) -> Perm:
    return tuple(apply_matrix(v,rows) for v in range(1 << len(rows)))


class Span:
    def __init__(self, n: int):
        self.n = n; self.pivots: list[tuple[int, int] | None] = [None]*n
        self.rank = 0
    def insert(self, value: int, combination: int) -> bool:
        for p in reversed(range(self.n)):
            if value & (1 << p):
                row = self.pivots[p]
                if row is None:
                    self.pivots[p] = (value, combination); self.rank += 1
                    return True
                value ^= row[0]; combination ^= row[1]
        return False
    def solve(self, value: int) -> int | None:
        combination = 0
        for p in reversed(range(self.n)):
            if value & (1 << p):
                row = self.pivots[p]
                if row is None: return None
                value ^= row[0]; combination ^= row[1]
        return combination


def invariant_rank(seed: int, matrices: Sequence[Sequence[int]], n: int) -> int:
    span = Span(n); span.insert(seed, 1); queue = deque([seed])
    while queue:
        v = queue.popleft()
        for matrix in matrices:
            w = apply_matrix(v, matrix)
            if span.insert(w, 1): queue.append(w)
    return span.rank


def row_rank(rows: Sequence[int], n: int) -> int:
    span=Span(n)
    for row in rows: span.insert(int(row),1)
    return span.rank


def action_matrix(element: Perm, module: Sequence[Perm], masks: dict[Perm, int]) -> list[int]:
    return [masks[conjugate(v, element)] for v in module]


def marked_sub(word: Sequence[int], left: Sequence[int], right: Sequence[int]) -> list[int]:
    images: list[Sequence[int]] = [(), (), (), (), (), ()]
    images[0], images[3] = left, right
    return substitute(word, images)


def dtilde_word(word: Sequence[int]) -> list[int]:
    marked = [({1: 1, 2: 4}[abs(x)] if x > 0 else -{1: 1, 2: 4}[abs(x)]) for x in word]
    x15, x45 = (-3,-2,-1), (-6,-5,-3)
    a = marked_sub(marked, x45, (6,)); b = marked_sub(marked, (1,), x15)
    c = marked_sub(marked, (4,), (6,)); d = marked_sub(marked, x45, x15)
    e = marked_sub(marked, (1,), (4,))
    return free_reduce(inv_word(a)+inv_word(b)+c+d+e)


def pairs(g: Sequence[Perm]) -> tuple[tuple[Perm, Perm], ...]:
    return ((g[0],g[3]), (g[3],g[5]), (paper_product((g[1],g[3])),g[5]),
            (paper_product((g[0],g[1])),paper_product((g[4],g[5]))),
            (g[0],paper_product((g[3],g[4]))))


def pent(word: Sequence[int], g: Sequence[Perm]) -> Perm:
    parts = [word_value(word, p) for p in pairs(g)]
    return paper_product((inverse(paper_product((parts[4],parts[2]))),
                          parts[1],parts[3],parts[0]))


def hexagons(word: Sequence[int], m: int, x: Perm, y: Perm) -> tuple[Perm, Perm]:
    z = inverse(paper_product((x,y))); u = inverse(paper_product((y,x)))
    fxy = word_value(word,(x,y)); fxz = word_value(word,(x,z))
    fyz = word_value(word,(y,z)); fux = word_value(word,(u,x)); fuy = word_value(word,(u,y))
    return (paper_product((power(y,m),fxy,power(x,m),inverse(fxz),power(z,m),fyz)),
            paper_product((inverse(fux),power(x,m),inverse(fxy),power(y,m),fuy,power(u,m))))


def hex_pairs(x: Perm, y: Perm) -> tuple[tuple[Perm, Perm], ...]:
    z = inverse(paper_product((x,y))); u = inverse(paper_product((y,x)))
    return ((x,y),(x,z),(y,z),(u,x),(u,y))


def hex_from_values(values: Sequence[Perm], m: int, x: Perm, y: Perm) -> tuple[Perm,Perm]:
    require(len(values)==5,"hex context arity")
    z = inverse(paper_product((x,y))); u = inverse(paper_product((y,x)))
    fxy,fxz,fyz,fux,fuy=values
    return (paper_product((power(y,m),fxy,power(x,m),inverse(fxz),power(z,m),fyz)),
            paper_product((inverse(fux),power(x,m),inverse(fxy),power(y,m),fuy,power(u,m))))


def pent_from_values(parts: Sequence[Perm]) -> Perm:
    require(len(parts)==5,"pentagon context arity")
    return paper_product((inverse(paper_product((parts[4],parts[2]))),
                          parts[1],parts[3],parts[0]))


def correction_context_table(contexts: Sequence[Sequence[Perm]],
                             basis: Sequence[Sequence[int]]) -> list[list[Perm]]:
    tables: list[list[Perm]]=[]
    for context in contexts:
        basis_values=[word_value(w,context) for w in basis]
        values=[one(len(context[0])) for _ in range(64)]
        for bits in range(1,64):
            k=bits.bit_length()-1; previous=bits-(1<<k)
            values[bits]=compose(values[previous],basis_values[k])
        tables.append(values)
    return tables


def context_base(word: Sequence[int], contexts: Sequence[Sequence[Perm]]) -> list[Perm]:
    return [word_value(word,context) for context in contexts]


def context_values(base: Sequence[Perm], table: Sequence[Sequence[Perm]], bits: int) -> list[Perm]:
    return [compose(value,table[i][bits]) for i,value in enumerate(base)]


def correction_word(bits: int, basis: Sequence[Sequence[int]]) -> list[int]:
    return free_reduce(x for i,w in enumerate(basis) if bits & (1<<i) for x in w)


def gt_compose_m0(left: Sequence[int], right: Sequence[int]) -> list[int]:
    yimage = free_reduce(list(left)+[2]+inv_word(left))
    return free_reduce(substitute(right, ((1,),yimage))+list(left))


def source_words_m0(f: Sequence[int]) -> list[list[int]]:
    ff = substitute(f, ((1,),(4,))); g = substitute(f, ((1,),(2,)))
    gs = substitute(f, ((4,),(5,))); f1234 = substitute(f, ((4,2),(6,)))
    fp = substitute(f, ((2,1),(6,5))); h = substitute(f, ((2,1),(3,)))
    return [[1], paper_word((inv_word(g),(2,),g)),
            paper_word((inv_word(ff),inv_word(h),(3,),h,ff)),
            paper_word((inv_word(ff),(4,),ff)),
            paper_word((inv_word(ff),inv_word(fp),inv_word(gs),(5,),gs,fp,ff)),
            paper_word((inv_word(f1234),(6,),f1234))]


def classify(missing: Sequence[str], solutions: Sequence[dict]) -> str:
    if missing: return "UNKNOWN_MISSING_INPUT"
    if solutions: return "ROW18_TYPED_STAGE_LIFT"
    return "EXACT_FINITE_STAGE_OBSTRUCTION"


def validate_report(report: dict) -> None:
    require(report.get("schema") == "d972-b4-literal-row18-stage/v1", "schema drift")
    require(report.get("final_marker") == "D972_B4_LITERAL_ROW18_STAGE_V1_FINAL", "marker drift")
    faithful_artin_replay()
    require(file_sha(CORE_PRODUCER) == CORE_PRODUCER_SHA and file_sha(PAB_FILE) == PAB_SHA,
            "source binding drift")
    core = reconstruct_core(); module = core["module"]; masks = module_masks(module)
    erows, prows, grows = (tuple_rows(core,x) for x in ("E","P","G9"))
    egens = tuple(embed_blocks(row) for row in erows)
    pgens = tuple(embed_blocks(row) for row in prows)
    ggens = tuple(embed_blocks(row) for row in grows)
    onee4, onep4, oneg4 = one(4*DEG_E), one(4*DEG_P), one(4*DEG_G9)

    frozen = report.get("frozen_inputs", {})
    require(frozen == {
        "core_source_sha256": CORE_PRODUCER_SHA, "word_artifact_sha256": WORDS_SHA,
        "tuple_artifact_sha256": TUPLES_SHA, "literal_source_sha256": LITERAL_SHA,
        "packagegt_pab_sha256": PAB_SHA, "row_vector_PSL_convention": True,
        "roof_tuple_digest": TUPLE_DIGEST, "roof_key_digest": KEY_DIGEST,
    }, "frozen input receipt drift")
    require(report.get("row18") == {"zero_based_index":18,"one_based_index":19,
        "key":EXPECTED_KEY,"word":EXPECTED_WORD,"pure_axis":[1,0],
        "arithmetic_outside_accepted":True}, "row18 receipt drift")

    basis_obj = report.get("c2_basis", {})
    basis = basis_obj.get("generators")
    require(basis_obj.get("rank") == 24 and basis_obj.get("order") == 2**24 and
            isinstance(basis,list) and len(basis)==24, "basis receipt shape")
    for k, row in enumerate(basis):
        c,b = divmod(k,6); word = row.get("source_word")
        require(row.get("coordinate")==c+1 and row.get("module_index")==b+1,
                "basis ordering drift")
        require(word_value(word,egens)==embed_blocks(module[b] if j==c else one(DEG_E) for j in range(4)),
                "basis E replay drift")
        require(word_value(word,pgens)==onep4 and word_value(word,ggens)==oneg4,
                "basis base replay drift")
    basis_words = [row["source_word"] for row in basis]

    action_rows: list[list[int]] = []
    action_words: list[list[list[int]]] = []
    for images in ARTIN:
        words = [substitute(w,images) for w in basis_words]
        auto_e=[word_value(w,egens) for w in images]
        auto_p=[word_value(w,pgens) for w in images]
        auto_g=[word_value(w,ggens) for w in images]
        rows = []
        for k,word in enumerate(words):
            ve=word_value(basis_words[k],auto_e)
            vp=word_value(basis_words[k],auto_p); vg=word_value(basis_words[k],auto_g)
            if k==0:
                require(word_value(word,egens)==ve and word_value(word,pgens)==vp and
                        word_value(word,ggens)==vg,"action composition canary")
            require(vp==onep4 and vg==oneg4,
                    "action left kernel")
            rows.append(mask24(ve,masks))
        action_rows.append(rows); action_words.append(words)
    require(matmul(matmul(action_rows[0],action_rows[1]),action_rows[0]) ==
            matmul(matmul(action_rows[1],action_rows[0]),action_rows[1]), "Artin 12 drift")
    require(matmul(matmul(action_rows[1],action_rows[2]),action_rows[1]) ==
            matmul(matmul(action_rows[2],action_rows[1]),action_rows[2]), "Artin 23 drift")
    require(matmul(action_rows[0],action_rows[2]) == matmul(action_rows[2],action_rows[0]),
            "Artin 13 drift")
    pure_matrices = [[action_matrix(e,module,masks) for e in row] for row in erows]
    for i,gindex in enumerate((0,3,5)):
        expected = [pure_matrices[gindex][k//6][k%6] << (6*(k//6)) for k in range(24)]
        require(matmul(action_rows[i],action_rows[i]) == expected, "Artin square calibration")
    expected_perm = ((2,1,3,4),(1,3,2,4),(1,2,4,3))
    for i,matrix in enumerate(action_rows):
        for c in range(4):
            for b in range(6):
                support = {j//6+1 for j in range(24) if matrix[6*c+b] & (1<<j)}
                require(support == {expected_perm[i][c]}, "coordinate action drift")
    factor_orders=[]; factor_module_irreducible=[]; factor_groups=[]
    for c in range(4):
        mats=[pure_matrices[g][c] for g in range(6)]
        perms=[tuple(apply_matrix(v,m) for v in range(64)) for m in mats]
        factor_group=closure(perms,64)
        factor_groups.append(factor_group)
        factor_orders.append(len(factor_group))
        factor_module_irreducible.append(all(invariant_rank(v,mats,6)==6
                                               for v in range(1,64)))

    # Bind every canonical PB4 generator to an actual word in the three B4
    # matrices.  The subsequent one-coordinate witnesses therefore lie in
    # the pure image, rather than merely in the product of its projections.
    pure_full_rows=[
        [pure_matrices[g][k//6][k%6] << (6*(k//6)) for k in range(24)]
        for g in range(6)
    ]
    require([matrix_word(w,action_rows) for w in PURE_BRAID_WORDS] == pure_full_rows,
            "pure generator/B4 matrix replay drift")

    witness_receipts=[]; normal_closure_orders=[]
    identity6=[1 << i for i in range(6)]
    for c,(left,right) in enumerate(SINGLE_SUPPORT_PAIRS):
        blocks_=[matrix_commutator(pure_matrices[left-1][d],pure_matrices[right-1][d])
                 for d in range(4)]
        support=[d+1 for d,matrix in enumerate(blocks_) if matrix != identity6]
        require(support == [c+1], "single-support commutator drift")
        witness_perm=matrix_permutation(blocks_[c])
        conjugates={conjugate(witness_perm,g) for g in factor_groups[c]}
        normal_order=len(closure(conjugates,64))
        normal_closure_orders.append(normal_order)
        witness_receipts.append({
            "coordinate":c+1,
            "generator_indices":[left,right],
            "commutator_word":[-left,-right,left,right],
            "support_coordinates":support,
            "block_row_masks":blocks_,
            "factor_normal_closure_order":normal_order,
        })

    coordinate_generators=tuple(tuple(x-1 for x in p) for p in expected_perm)
    coordinate_group=closure(coordinate_generators,4)
    coordinate_order=len(coordinate_group)
    coordinate_transitive={p[0] for p in coordinate_group} == set(range(4))
    pure_image_order=504**4
    image_order=pure_image_order*coordinate_order
    action = report.get("b4_action",{})
    require(action.get("source_automorphism_words") == [[list(w) for w in x] for x in ARTIN],
            "action word receipt drift")
    require(action.get("packagegt_inverse_orientation_words") == [[list(w) for w in x] for x in PAB_INVERSE],
            "PaB inverse receipt drift")
    require(action.get("faithful_artin_F4_replay") is True,
            "faithful Artin receipt drift")
    require(action.get("transformed_basis_words")==action_words and
            action.get("matrix_row_masks")==action_rows and
            action.get("matrices")==[[[(r>>j)&1 for j in range(24)] for r in m] for m in action_rows],
            "action certificate drift")
    derived=action.get("independently_derived_words")
    derived_inverse=action.get("independently_derived_packagegt_inverse_words")
    require(isinstance(derived,list) and len(derived)==3 and
            isinstance(derived_inverse,list) and len(derived_inverse)==3,"derived action receipt shape")
    for i in range(3):
        require(len(derived[i])==6 and len(derived_inverse[i])==6,"derived action row shape")
        for j in range(6):
            # The independent finite replay binds the GAP-derived PB4 word to
            # the accepted natural action and the separately pinned inverse.
            require(word_value(derived[i][j],egens)==word_value(ARTIN[i][j],egens),
                    "derived natural action mismatch")
            require(word_value(derived_inverse[i][j],egens)==word_value(PAB_INVERSE[i][j],egens),
                    "derived PackageGT inverse mismatch")
    require(action.get("pure_generator_braid_words")==[list(w) for w in PURE_BRAID_WORDS] and
            action.get("pure_generator_braid_word_replay") is True,
            "pure generator word receipt drift")
    require(factor_orders==[504]*4 and factor_module_irreducible==[True]*4 and
            normal_closure_orders==[504]*4 and coordinate_order==24 and coordinate_transitive,
            "action image/chief premise drift")
    require(action.get("pure_factor_orders")==factor_orders and
            action.get("pure_factor_module_irreducible")==factor_module_irreducible and
            action.get("direct_product_certificate")=={
                "method":"single-support commutators and exact factor normal closures",
                "single_support_commutators":witness_receipts,
                "factor_normal_closure_orders":normal_closure_orders,
                "independent_factor_inclusion":True,
                "pure_image_order":pure_image_order,
            } and action.get("pure_image_order")==pure_image_order,
            "pure direct-product certificate drift")
    require(action.get("coordinate_permutations")==[list(p) for p in expected_perm] and
            action.get("coordinate_image_order")==coordinate_order and
            action.get("coordinate_action_transitive") is True and
            action.get("image_order")==image_order,
            "full action image certificate drift")
    require(action.get("chief_certificate")=={
                "factor_dimensions":[6,6,6,6],
                "factor_module_irreducible":factor_module_irreducible,
                "independent_factor_action":True,
                "coordinate_action_transitive":True,
                "dimensions":[24],
                "module_irreducible":True,
            } and action.get("chief_dimensions")==[24] and
            action.get("module_irreducible") is True,
            "action chief certificate drift")
    require(action.get("source_kernel_certificate")=={
        "definition":"kernel of the recorded B4 to GL(24,2) generator map",
        "index":image_order,
        "membership_test":"natural word evaluation in the three recorded 24x24 matrices"},
        "source-kernel certificate drift")

    literal = load(LITERAL_FILE,LITERAL_SHA); words_obj=load(WORDS_FILE,WORDS_SHA)
    tuples_obj=load(TUPLES_FILE,TUPLES_SHA)
    require(words_obj.get("source_target_key_digest")==KEY_DIGEST and
            words_obj.get("frozen_tuple_sha256")==TUPLE_DIGEST and
            tuples_obj.get("canonical_bytes_sha256")==TUPLE_DIGEST, "roof digest drift")
    require(words_obj["rows"][18]==[0,EXPECTED_KEY,EXPECTED_WORD] and
            tuples_obj["tuples"][18]==EXPECTED_KEY, "row18 input binding drift")
    require(digest([dtilde_word(row[2]) for row in words_obj["rows"]])==DTILDE_SHA,
            "all-row ordered Dtilde digest drift")
    prefix=literal["all_relators"][:18]; seeds=literal["all_relators"][18:46]
    require(digest(prefix)==PREFIX_SHA and digest(seeds)==SEED_SHA, "literal seed digest")
    a18=[]; meta=[]
    for name,left,right in COFACES:
        for j,seed in enumerate(seeds,1):
            a18.append(marked_sub(seed,left,right)); meta.append((name,j))
    require(digest(a18)==A18_SHA and digest(prefix+a18)==PRESENTATION_SHA,
            "literal transport digest")
    require(all(word_value(w,egens)==onee4 and word_value(w,ggens)==oneg4 for w in prefix),
            "prefix evaluation drift")
    raw_masks=[]
    for word in a18:
        require(word_value(word,pgens)==onep4 and word_value(word,ggens)==oneg4,
                "A18 row base membership")
        raw_masks.append(mask24(word_value(word,egens),masks))

    span=Span(24); relation=[]
    for index,(word,vector) in enumerate(zip(a18,raw_masks),1):
        k=len(relation)
        if span.insert(vector,1<<k):
            relation.append({"vector":vector,"word":word,"raw_index":index,"action_word":[]})
    pos=0
    while pos<len(relation):
        row=relation[pos]; pos+=1
        for i,images in enumerate(ARTIN,1):
            vector=apply_matrix(row["vector"],action_rows[i-1])
            if span.solve(vector) is None:
                word=substitute(row["word"],images)
                require(mask24(word_value(word,egens),masks)==vector,"relation equivariance")
                k=len(relation)
                require(span.insert(vector,1<<k),"relation independence race")
                relation.append({"vector":vector,"word":word,"raw_index":row["raw_index"],
                                 "action_word":row["action_word"]+[i]})
    require(all(span.solve(apply_matrix(r["vector"],m)) is not None
                for r in relation for m in action_rows), "relation not invariant")
    literal_obj=report.get("literal_a18",{})
    require(literal_obj.get("prefix_count")==18 and literal_obj.get("seed_count")==28 and
            literal_obj.get("coface_count")==5 and
            literal_obj.get("coface_order")==[x[0] for x in COFACES] and
            literal_obj.get("prefix_sha256")==PREFIX_SHA and literal_obj.get("seed_sha256")==SEED_SHA and
            literal_obj.get("a18_rows_sha256")==A18_SHA and
            literal_obj.get("presentation_sha256")==PRESENTATION_SHA and
            literal_obj.get("dtilde_sha256")==DTILDE_SHA,"literal scalar gate drift")
    expected_relation=[{"vector":r["vector"],"vector_bits":[(r["vector"]>>j)&1 for j in range(24)],
                        "raw_index":r["raw_index"],"action_word":r["action_word"],"word":r["word"]}
                       for r in relation]
    require(literal_obj.get("raw_relation_masks")==raw_masks and
            literal_obj.get("relation_boundary_rank")==span.rank and
            literal_obj.get("relation_boundary_generators")==expected_relation,
            "relation boundary receipt drift")

    delete1=((),(),(),(1,),(-1,-2),(2,))
    cbasis=[substitute(basis_words[i],delete1) for i in range(6)]
    for i,w in enumerate(cbasis):
        require(word_value(w,(core["x"],core["y"]))==module[i] and
                word_value(w,(core["px"],core["py"]))==one(DEG_P) and
                word_value(w,(core["gx"],core["gy"]))==one(DEG_G9),
                "F2 correction basis drift")
    require(basis_obj.get("correction_F2_basis_words")==cbasis,"correction basis receipt")

    root=EXPECTED_WORD; square=gt_compose_m0(root,root)
    rp=word_value(root,(core["px"],core["py"])); rg=word_value(root,(core["gx"],core["gy"]))
    sp=word_value(square,(core["px"],core["py"])); sg=word_value(square,(core["gx"],core["gy"]))
    matches=[(i+1,row[1]) for i,row in enumerate(words_obj["rows"])
             if row[0]==0 and word_value(row[2],(core["px"],core["py"]))==sp and
             word_value(row[2],(core["gx"],core["gy"]))==sg]
    require(len(matches)==1,"powered roof uniqueness")
    square_index,square_key=matches[0]
    root_source=source_words_m0(root)
    root_source_e=[word_value(w,egens) for w in root_source]
    root_action=[mask24(word_value(w,root_source_e),masks) for w in basis_words]
    require(word_value(substitute(basis_words[0],root_source),egens)==
            word_value(basis_words[0],root_source_e),"root composition canary")
    norm=[(1<<i)^root_action[i] for i in range(24)]

    hex_contexts_e=hex_pairs(core["x"],core["y"])
    hex_contexts_p=hex_pairs(core["px"],core["py"])
    hex_contexts_g=hex_pairs(core["gx"],core["gy"])
    pent_contexts_e=pairs(egens); pent_contexts_p=pairs(pgens); pent_contexts_g=pairs(ggens)
    correction_tables=(correction_context_table(hex_contexts_e,cbasis),
                       correction_context_table(hex_contexts_p,cbasis),
                       correction_context_table(hex_contexts_g,cbasis),
                       correction_context_table(pent_contexts_e,cbasis),
                       correction_context_table(pent_contexts_p,cbasis),
                       correction_context_table(pent_contexts_g,cbasis))
    global_missing=[]; all_solutions=[]; power_records=[]
    power_inputs=((1,root,19,EXPECTED_KEY),(2,square,square_index,square_key))
    for exponent,pword,row_index,key in power_inputs:
        dword=dtilde_word(pword)
        base_contexts=(context_base(pword,hex_contexts_e),
                       context_base(pword,hex_contexts_p),
                       context_base(pword,hex_contexts_g),
                       context_base(pword,pent_contexts_e),
                       context_base(pword,pent_contexts_p),
                       context_base(pword,pent_contexts_g))
        bhe=hex_from_values(base_contexts[0],0,core["x"],core["y"])
        bhp=hex_from_values(base_contexts[1],0,core["px"],core["py"])
        bhg=hex_from_values(base_contexts[2],0,core["gx"],core["gy"])
        base_hex_masks=None
        if all(x==one(len(x)) for x in bhp+bhg):
            base_hex_masks=[masks[x] for x in bhe]
        else: global_missing.append("stage.row_power_base_hexagon_membership")
        pe=pent_from_values(base_contexts[3]); pp=pent_from_values(base_contexts[4])
        pg=pent_from_values(base_contexts[5])
        transport=word_value(dword,egens)==pe
        if not transport: global_missing.append("a18_comparison.dtilde_to_pab_pentagon_transport")
        base_mask=None
        if pp==onep4 and pg==oneg4: base_mask=mask24(pe,masks)
        else: global_missing.append("stage.row_power_base_pentagon_membership")
        gauge=[]; power_solutions=[]
        for bits in range(64):
            corr=correction_word(bits,cbasis); candidate=free_reduce(pword+corr)
            cached=[context_values(base_contexts[i],correction_tables[i],bits) for i in range(6)]
            if bits in (0,1,2,4,8,16,32,63):
                for contexts,values in zip((hex_contexts_e,hex_contexts_p,hex_contexts_g,
                                            pent_contexts_e,pent_contexts_p,pent_contexts_g),cached):
                    require(all(word_value(candidate,context)==value
                                for context,value in zip(contexts,values)),
                            "fixed-context/direct evaluation drift")
            he=hex_from_values(cached[0],0,core["x"],core["y"])
            hp=hex_from_values(cached[1],0,core["px"],core["py"])
            hg=hex_from_values(cached[2],0,core["gx"],core["gy"])
            ce=pent_from_values(cached[3]); cp=pent_from_values(cached[4]); cg=pent_from_values(cached[5])
            cmask=None; coeff=None; hex_masks=None
            if all(x==one(len(x)) for x in hp+hg): hex_masks=[masks[x] for x in he]
            if cp==onep4 and cg==oneg4:
                cmask=mask24(ce,masks); coeff=span.solve(cmask)
            if (bits in (1,2,4,8,16,32) and base_mask is not None and cmask is not None and
                    base_hex_masks is not None and hex_masks is not None):
                gauge.append({"hexagon1":base_hex_masks[0]^hex_masks[0],
                              "hexagon2":base_hex_masks[1]^hex_masks[1],
                              "pentagon":base_mask^cmask})
            roof_ok=(cached[1][0]==base_contexts[1][0] and cached[2][0]==base_contexts[2][0])
            charm=(sum(1 if x>0 else -1 for x in candidate if abs(x)==1)==0 and
                   sum(1 if x>0 else -1 for x in candidate if abs(x)==2)==0)
            preliminary=(transport and roof_ok and charm and all(x==one(len(x)) for x in he+hp+hg) and coeff is not None)
            if preliminary:
                fe=cached[0][0]; fg=cached[2][0]
                onto_e=len(closure((core["x"],paper_product((inverse(fe),core["y"],fe)))))==32256
                onto_g=len(closure((core["gx"],paper_product((inverse(fg),core["gy"],fg)))))==2916
            else: onto_e=onto_g=False
            if preliminary and onto_e and onto_g:
                selected=[i for i in range(len(relation)) if coeff & (1<<i)]
                corrected=dtilde_word(candidate)
                for i in selected: corrected.extend(relation[i]["word"])
                corrected=free_reduce(corrected)
                require(word_value(corrected,egens)==onee4 and word_value(corrected,pgens)==onep4 and
                        word_value(corrected,ggens)==oneg4,"corrected pentagon replay")
                sol={"exponent":exponent,"correction_bits":bits,"correction_word":corr,
                     "typed_source_word":candidate,"roof_row_index":row_index,"roof_key":key,
                     "defect_mask":cmask,"relation_combination":coeff,
                     "relation_generator_indices":[i+1 for i in selected],
                     "corrected_pentagon_word":corrected,"hexagon_E_identity":True,
                     "hexagon_P_identity":True,"hexagon_G9_identity":True,
                     "pentagon_mod_literal_relations":True,"marking_m":0,"lambda":1,
                     "charming":True,"onto_E":True,"onto_G9":True,"roof_reduction_exact":True}
                power_solutions.append(sol); all_solutions.append(sol)
        power_records.append({"exponent":exponent,"row_index":row_index,"roof_key":key,
                              "source_word":pword,"base_dtilde_word":dword,
                              "dtilde_transport_ok":transport,"base_hexagon_masks":base_hex_masks,
                              "base_defect_mask":base_mask,
                              "gauge_columns":gauge,"solution_count":len(power_solutions)})
    global_missing=sorted(set(global_missing))
    norm_ok=False
    if power_records[0]["base_defect_mask"] is not None and power_records[1]["base_defect_mask"] is not None:
        residual=power_records[1]["base_defect_mask"] ^ apply_matrix(power_records[0]["base_defect_mask"],norm)
        norm_ok=span.solve(residual) is not None
    selected=None
    if all_solutions:
        selected=next((s for s in all_solutions if s["exponent"]==1),all_solutions[0])
    settlement=None
    if selected is not None and not global_missing:
        sword=source_words_m0(selected["typed_source_word"])
        se=[word_value(w,egens) for w in sword]
        sp4=[word_value(w,pgens) for w in sword]
        sg4=[word_value(w,ggens) for w in sword]
        sa=[mask24(word_value(w,se),masks) for w in basis_words]
        require(word_value(substitute(basis_words[0],sword),egens)==word_value(basis_words[0],se),
                "selected composition canary")
        factor_e=factor_auto_certificate("E",(core["x"],core["y"]),egens,se,DEG_E,32256)
        factor_p=factor_auto_certificate("P",(core["px"],core["py"]),pgens,sp4,DEG_P,504)
        factor_g=factor_auto_certificate("G9",(core["gx"],core["gy"]),ggens,sg4,DEG_G9,2916)
        relation_preserved=all(span.solve(apply_matrix(r["vector"],sa)) is not None for r in relation)
        if row_rank(sa,24)!=24 or not relation_preserved:
            global_missing.append("settlement.source_endomorphism_bijective")
            selected=None
        else:
            factor_receipt={"coordinate_map":[1,2,3,4],"E":factor_e,"P":factor_p,"G9":factor_g,
                            "relation_boundary_preserved":True,"kernel_action_bijective":True,
                            "ambient_E4_automorphism":True,"P4_automorphism":True,
                            "G9_fourfold_image_automorphism":True,"quotient_automorphism":True}
            settlement={"source_words":sword,"source_images_E":[list(x) for x in se],
                        "source_images_P":[list(x) for x in sp4],
                        "source_images_G9":[list(x) for x in sg4],
                        "kernel_action_matrix":[[(r>>j)&1 for j in range(24)] for r in sa],
                        "kernel_action_rank":24,"literal_boundary_order":2**span.rank,
                        "literal_kernel_quotient_dimension":24-span.rank,
                        "literal_quotient_order":32256**4//(2**span.rank),
                        "P4_bijective":True,"G9_fourfold_image_bijective":True,
                        "literal_quotient_bijective":True,
                        "settlement_method":"factor_automorphisms_and_invariant_module_quotient",
                        "factor_automorphism_certificate":factor_receipt,"settled":True}
            selected["settlement"]=settlement
    global_missing=sorted(set(global_missing))
    status=classify(global_missing,[] if selected is None else [selected])
    require(report.get("status")==status and report.get("missing_inputs")==global_missing,
            "terminal status drift")
    stage=report.get("exhaustive_stage",{})
    require(stage.get("correction_count")==64 and stage.get("power_records")==power_records and
            stage.get("total_solution_count")==len(all_solutions) and stage.get("selected")==selected,
            "exhaustive stage receipt drift")
    require(stage.get("settlement")==settlement,"settlement receipt drift")
    require(stage.get("relation_boundary_closed_under_B4") is True and
            stage.get("representative_independence") is True and
            stage.get("marking_checked") is True and stage.get("charming_onto_checked") is True,
            "typed stage boolean gate drift")
    power_obj=report.get("power_selector",{})
    require(power_obj.get("root_word")==root and power_obj.get("powered_word")==square and
            power_obj.get("root_row_index")==19 and power_obj.get("root_key")==EXPECTED_KEY and
            power_obj.get("exponent_candidates")==[1,2] and
            power_obj.get("powered_row_index")==square_index and power_obj.get("powered_key")==square_key and
            power_obj.get("root_action_matrix")==[[(r>>j)&1 for j in range(24)] for r in root_action] and
            power_obj.get("norm_I_plus_T")==[[(r>>j)&1 for j in range(24)] for r in norm] and
            power_obj.get("norm_identity_mod_literal_relations")==norm_ok and
            power_obj.get("used")==bool(selected and selected["exponent"]>1), "power receipt drift")
    require(power_obj.get("outside_proof")==
            "pure axis exponent n with 3 not dividing n remains outside both arithmetic Kummer lines",
            "outside proof binding drift")
    require(literal_obj.get("literal_residual_to_C_P_over_C_E_matrix")==[
        {"exponent":r["exponent"],"row_index":r["row_index"],
         "hexagon_masks":r["base_hexagon_masks"],"residual_mask":r["base_defect_mask"],
         "gauge_columns":r["gauge_columns"]}
        for r in power_records], "literal comparison matrix drift")


def self_test() -> None:
    faithful_artin_replay()
    require(file_sha(PAB_FILE)==PAB_SHA,"PaB hash selftest")
    require(ARTIN[0][1] != PAB_INVERSE[0][1],"Artin orientation mutation accepted")
    require(digest([marked_sub([1,4,-1],*COFACES[0][1:])]) !=
            digest([marked_sub([1,4,-1],(1,),(5,))]),"coface mutation accepted")
    toy_a=(1,0,2); toy_b=(0,2,1)
    require(compose(toy_a,toy_b)!=paper_product((toy_a,toy_b)),"GT composition-order mutation")
    require(gt_compose_m0([1,2],[1,2])!=[1,2,1,2],"naive GT word power accepted")
    require(EXPECTED_KEY != [0,[[2,0],[7,0],[0,0]],[1,2,3,4,5,6,7,8,8]],"key mutation")
    require(EXPECTED_WORD != EXPECTED_WORD[:-1]+[-1],"word mutation")
    matrix=[1<<i for i in range(24)]; mutated=matrix.copy(); mutated[0]^=2
    require(matrix!=mutated,"action matrix mutation")
    basis=[[-1,-2],[1]]; toy_c=(1,2,0)
    require(correction_word(1,basis)!=correction_word(0,basis),"correction-bit mutation")
    require(word_value([1],(toy_c,))!=word_value([-1],(toy_c,)),"basis-word mutation accepted")
    require(504 != 503,"factor-order mutation accepted")
    toy_m1=[2,1,4]; toy_m2=[3,2,4]; identity3=[1,2,4]
    require(matmul(toy_m1,matrix_inverse(toy_m1))==identity3 and
            matrix_word([1,-1],(toy_m1,))==identity3,"matrix inverse replay")
    require(matrix_commutator(toy_m1,toy_m2)!=identity3,
            "commutator-support mutation accepted")
    require(SINGLE_SUPPORT_PAIRS != ((4,5),(2,3),(1,3),(1,3)),
            "single-support pair mutation accepted")
    require(classify(["x"],[])=="UNKNOWN_MISSING_INPUT" and
            classify([],[])=="EXACT_FINITE_STAGE_OBSTRUCTION" and
            classify([],[{}])=="ROW18_TYPED_STAGE_LIFT","terminal mutation")
    # Row-vector PSL canary: transposing a nonsymmetric matrix changes a point.
    require(matrix_action(((1,0),(1,1))) != matrix_action(((1,1),(0,1))),
            "PSL orientation mutation accepted")
    print("D972_B4_LITERAL_ROW18_STAGE_V1_CHECKER_SELFTEST_PASS")


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--receipt",type=Path)
    args=parser.parse_args()
    if args.self_test:
        self_test(); return 0
    require(args.receipt is not None,"--receipt required")
    obj=json.loads(args.receipt.read_text(encoding="utf-8"))
    require(isinstance(obj,dict),"receipt object drift")
    validate_report(obj)
    print("D972_B4_LITERAL_ROW18_STAGE_V1_CHECK_PASS",args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
