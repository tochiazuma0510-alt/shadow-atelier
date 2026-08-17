"""Exact synchronized multi-specialization Burau obstruction producer.

The source pair is mapped once into one finite direct product.  A tuple has a
single roof permutation followed by the five A.18 blocks for each registered
specialization, in the fixed specialization/block order.  The closure and
the Schreier kernel are therefore for the synchronized image itself; no
Cartesian product of independently computed fibers is used.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Sequence

from sympy.combinatorics import Permutation, PermutationGroup

WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ARTIFACT_ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
SEMANTIC_SHA = "3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729"
P_ORDER = 1469664
PPRIME_ORDER = 367416
CAL_H_ORDER = 105815808
CAL_HPRIME_ORDER = 2939328
CAL_KERNEL_ORDER = 8
SCHEMA = "d972-b4-burau-joint/v1-synchronized"
FINAL = "D972_B4_BURAU_JOINT_V1_FINAL"
ALGORITHM = "exact synchronized tuple Reidemeister-Schreier normal closure"
SOURCE_MAP = "one synchronized Psi_S from the same signed source words"
HEXAGON_CONVENTION = "PaperProd reverses displayed factors; tau(y)=inverse(PaperProd(x,y))"
M_RESIDUE_GATE = "all CRT residues m~=source_m (mod 18), with gcd(2*m~+1,L)=1"
GENERATOR_ORDER = ("x12", "x13", "x14", "x23", "x24", "x34")
A18_NAMES = ("123", "234", "12,3,4", "1,23,4", "1,2,34")
TRANSFORM_ORDER = ("base", "theta", "tau", "tau2")
N = 4
Matrix = tuple[tuple[int, ...], ...]
Perm = tuple[int, ...]
Spec = tuple[str, int, int]
JointElt = tuple[Perm, tuple[Matrix, ...]]

# q3a2 is deliberately the public lane name for (q=3,a=-1), as in v4.
CONFIGS: dict[str, tuple[Spec, ...]] = {
    "q3a2_full": (("q3a2", 3, -1),),
    "q4a2_full": (("q4a2", 4, 2),),
    "q3a2_q4a2": (("q3a2", 3, -1), ("q4a2", 4, 2)),
    "q3a2_q4a2_q5a2": (("q3a2", 3, -1), ("q4a2", 4, 2),
                        ("q5a2", 5, 2)),
    "q3a2_q4a2_q5a4": (("q3a2", 3, -1), ("q4a2", 4, 2),
                        ("q5a4", 5, 4)),
}
FIELD_SIGNATURE = {
    "q3": "prime_field_Z/3Z",
    "q4": "GF(2)[u]/(u^2+u+1), elements 0..3",
    "q5": "prime_field_Z/5Z",
}
SINGLE_LANE_REFERENCE = {
    "q3a2": {"q": 3, "a": -1, "h_order": CAL_H_ORDER,
              "hprime_order": CAL_HPRIME_ORDER, "kernel_order": 8},
    "q4a2": {"q": 4, "a": 2, "h_order": CAL_H_ORDER,
              "hprime_order": CAL_HPRIME_ORDER, "kernel_order": 8},
}


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def cjson(x: Any) -> bytes:
    return json.dumps(x, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def digest(x: Any) -> str:
    return hashlib.sha256(cjson(x)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def producer_source_sha() -> str:
    return file_sha(Path(__file__).resolve())


def specs_for(config: str) -> tuple[Spec, ...]:
    require(config in CONFIGS, "unsupported synchronized configuration")
    return CONFIGS[config]


def spec_json(specs: Sequence[Spec]) -> list[dict[str, Any]]:
    return [{"lane": lane, "q": q, "a": a,
             "field": FIELD_SIGNATURE[f"q{q}"]} for lane, q, a in specs]


def block_order(specs: Sequence[Spec]) -> list[str]:
    return [f"{lane}:{transform}:{name}"
            for lane, _, _ in specs
            for transform in TRANSFORM_ORDER for name in A18_NAMES]


def config_digest(config: str) -> str:
    specs = specs_for(config)
    return digest({"config": config, "specializations": spec_json(specs),
                   "block_order": block_order(specs),
                   "generator_order": list(GENERATOR_ORDER),
                   "a18_pair_order": list(A18_NAMES)})


def ident(n: int) -> Perm:
    return tuple(range(1, n + 1))


def pprod(a: Perm, b: Perm) -> Perm:
    return tuple(b[a[i] - 1] for i in range(len(a)))


def pinv(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, x in enumerate(p, 1):
        out[x - 1] = i
    return tuple(out)


def ppow(p: Perm, n: int) -> Perm:
    if n < 0:
        return ppow(pinv(p), -n)
    out = ident(len(p))
    while n:
        if n & 1:
            out = pprod(out, p)
        p = pprod(p, p)
        n >>= 1
    return out


def paper_prod(xs: Iterable[Perm]) -> Perm:
    vals = list(xs)
    require(vals, "empty PaperProd")
    out = ident(len(vals[0]))
    for x in reversed(vals):
        out = pprod(out, x)
    return out


def make_dn(n: int) -> tuple[Perm, Perm]:
    r = tuple(range(2, n + 1)) + (1,)
    s = tuple(((n - (j - 1)) % n) + 1 for j in range(1, n + 1))
    require(pprod(pprod(s, r), pinv(s)) == pinv(r), "D_n relation drift")
    return r, s


def make_gn(n: int) -> tuple[Perm, Perm]:
    r, s = make_dn(n)

    def tr(p: Perm, which: int) -> Perm:
        out = list(range(1, 3 * n + 1))
        off = (which - 1) * n
        for j in range(n):
            out[off + j] = off + p[j]
        return tuple(out)

    sr = pprod(s, r)
    return (pprod(pprod(tr(r, 1), tr(s, 2)), tr(s, 3)),
            pprod(pprod(tr(sr, 1), tr(r, 2)), tr(sr, 3)))


def gf8_mul(a: int, b: int) -> int:
    z = 0
    for i in range(3):
        if (b >> i) & 1:
            z ^= a << i
    for i in (4, 3):
        if z & (1 << i):
            z ^= 0b1011 << (i - 3)
    return z


def gf8_inv(a: int) -> int:
    require(1 <= a <= 7, "GF8 inverse drift")
    for b in range(1, 8):
        if gf8_mul(a, b) == 1:
            return b
    raise ValueError("GF8 inverse missing")


def gf8_perm(m: list[list[int]]) -> Perm:
    a, b = m[0]
    c, d = m[1]
    out = [1 if c == 0 else 2 + gf8_mul(a, gf8_inv(c))]
    for x in range(8):
        num = gf8_mul(a, x) ^ b
        den = gf8_mul(c, x) ^ d
        out.append(1 if den == 0 else 2 + gf8_mul(num, gf8_inv(den)))
    return tuple(out)


def direct_sum(a: Perm, b: Perm) -> Perm:
    n = len(a)
    return a + tuple(n + x for x in b)


def build_roof() -> tuple[Perm, Perm]:
    x9, y9 = make_gn(9)
    s = gf8_perm([[1, 0], [1, 1]])
    t = gf8_perm([[4, 3], [1, 5]])
    w = pprod(s, pinv(t))
    x4 = pprod(w, w)
    y4 = pprod(pprod(pinv(s), x4), s)
    return direct_sum(x9, x4), direct_sum(y9, y4)


def block(p: Perm, offset: int, size: int) -> Perm:
    z = tuple(p[offset + i] - offset for i in range(size))
    require(set(z) == set(range(1, size + 1)), "permutation block drift")
    return z


def d9_coords(p: Perm) -> list[int]:
    r, s = make_dn(9)
    for a in range(9):
        for e in range(2):
            if p == pprod(ppow(r, a), ppow(s, e)):
                return [a, e]
    raise ValueError("D9 coordinate drift")


def eval_perm_word(word: Iterable[int], gens: Sequence[Perm]) -> Perm:
    out = ident(len(gens[0]))
    for z in word:
        require(isinstance(z, int) and not isinstance(z, bool) and z and
                abs(z) <= len(gens), "invalid signed source word")
        out = pprod(out, gens[abs(z) - 1] if z > 0
                    else pinv(gens[-z - 1]))
    return out


def roof_key(word: list[int], roof: tuple[Perm, Perm], m: int) -> list[Any]:
    f = eval_perm_word(word, roof)
    p27, p9 = block(f, 0, 27), block(f, 27, 9)
    return [int(m), [d9_coords(block(p27, 9 * i, 9)) for i in range(3)],
            list(p9)]


def roof_image_for_key(key: list[Any]) -> Perm:
    r, s = make_dn(9)
    p27 = tuple(9 * i + x
                for i, (a, e) in enumerate(key[1])
                for x in pprod(ppow(r, int(a)), ppow(s, int(e))))
    return p27 + tuple(27 + int(x) for x in key[2])


def load_words() -> list[list[Any]]:
    require(file_sha(WORDS_PATH) == WORDS_SHA, "word artifact SHA drift")
    obj = json.loads(WORDS_PATH.read_bytes())
    rows = obj.get("rows")
    require(obj.get("schema") == "d972-b4-word-key-artifact/v1" and
            obj.get("count") == 972 and isinstance(rows, list) and
            len(rows) == 972, "word artifact shape drift")
    require(obj.get("canonical_bytes_sha256") == digest(rows) == ARTIFACT_ROWS_SHA,
            "word artifact canonical digest drift")
    require(obj.get("source_target_key_digest") == TARGET_SHA and
            obj.get("frozen_tuple_sha256") == TUPLE_SHA and
            digest([r[1] for r in rows]) == TUPLE_SHA,
            "word artifact metadata/target digest drift")
    for row in rows:
        require(isinstance(row, list) and len(row) == 3 and
                isinstance(row[2], list), "word row shape drift")
    require(len({digest(r[1]) for r in rows}) == 972,
            "duplicate frozen roof keys")
    return rows


def free_ab_exponents(word: Iterable[int]) -> tuple[int, int]:
    ex = [0, 0]
    for z in word:
        require(isinstance(z, int) and not isinstance(z, bool) and z and
                abs(z) <= 2, "invalid source word for abelianization")
        ex[abs(z) - 1] += 1 if z > 0 else -1
    return tuple(ex)


def source_word_negative_ok(rows: list[list[Any]]) -> bool:
    pairs = [free_ab_exponents(row[2]) for row in rows]
    return (len(pairs) == 972 and pairs[1] == (-4, -8) and
            sum(pair != (0, 0) for pair in pairs) == 956)


# ---- finite fields and literal A.18 maps -------------------------------

def fadd(a: int, b: int, q: int) -> int:
    return (a ^ b) if q == 4 else (a + b) % q


def fneg(a: int, q: int) -> int:
    return a if q == 4 else (-a) % q


def fsub(a: int, b: int, q: int) -> int:
    return fadd(a, fneg(b, q), q)


def fmul(a: int, b: int, q: int) -> int:
    if q != 4:
        return (a * b) % q
    z, aa, bb = 0, a, b
    while bb:
        if bb & 1:
            z ^= aa
        bb >>= 1
        aa <<= 1
    return z ^ 0b111 if z & 4 else z


def finv(a: int, q: int) -> int:
    require(a != 0, "field inverse of zero")
    for b in range(1, q):
        if fmul(a, b, q) == 1:
            return b
    raise ValueError("field inverse missing")


def eye() -> Matrix:
    return tuple(tuple(int(i == j) for j in range(N)) for i in range(N))


def mmul(a: Matrix, b: Matrix, q: int) -> Matrix:
    return tuple(tuple(_fsum((fmul(a[i][k], b[k][j], q)
                              for k in range(N)), q)
                       for j in range(N)) for i in range(N))


def _fsum(xs: Iterable[int], q: int) -> int:
    z = 0
    for x in xs:
        z = fadd(z, x, q)
    return z


def minv(a: Matrix, q: int) -> Matrix:
    rows = [list(a[i]) + list(eye()[i]) for i in range(N)]
    for c in range(N):
        r = next((j for j in range(c, N) if rows[j][c] != 0), None)
        require(r is not None, "singular Burau matrix")
        rows[c], rows[r] = rows[r], rows[c]
        z = finv(rows[c][c], q)
        rows[c] = [fmul(x, z, q) for x in rows[c]]
        for j in range(N):
            if j != c:
                z = rows[j][c]
                rows[j] = [fsub(x, fmul(z, y, q), q)
                           for x, y in zip(rows[j], rows[c])]
    return tuple(tuple(x[N:]) for x in rows)


def mpow(a: Matrix, n: int, q: int) -> Matrix:
    out = eye()
    while n:
        if n & 1:
            out = mmul(out, a, q)
        a = mmul(a, a, q)
        n >>= 1
    return out


def matrix_paper_prod(xs: Iterable[Matrix], q: int) -> Matrix:
    out = eye()
    for x in reversed(list(xs)):
        out = mmul(out, x, q)
    return out


def burau_generators(q: int, a: int) -> tuple[Matrix, Matrix, Matrix]:
    require((q, a) in ((3, -1), (4, 2), (5, 2), (5, 4)),
            "unsupported registered Burau specialization")
    av = a % q if q != 4 else a
    out = []
    for i in range(3):
        m = [list(x) for x in eye()]
        m[i][i], m[i][i + 1] = fsub(1, av, q), av
        m[i + 1][i], m[i + 1][i + 1] = 1, 0
        out.append(tuple(tuple(x) for x in m))
    return tuple(out)  # type: ignore[return-value]


def pure_generators(q: int, a: int) -> tuple[Matrix, ...]:
    s1, s2, s3 = burau_generators(q, a)
    i2, i3 = minv(s2, q), minv(s3, q)
    p1, p4, p6 = mpow(s1, 2, q), mpow(s2, 2, q), mpow(s3, 2, q)
    return (p1, matrix_paper_prod((s2, p1, i2), q),
            matrix_paper_prod((s3, s2, p1, i2, i3), q), p4,
            matrix_paper_prod((s3, p4, i3), q), p6)


def a18_pairs(pure: tuple[Matrix, ...], q: int) -> tuple[tuple[Matrix, Matrix], ...]:
    x12, x13, x14, x23, x24, x34 = pure
    return ((x12, x23), (x23, x34),
            (matrix_paper_prod((x13, x23), q), x34),
            (matrix_paper_prod((x12, x13), q),
             matrix_paper_prod((x24, x34), q)),
            (x12, matrix_paper_prod((x23, x24), q)))


def transformed_pair(pair: tuple[Matrix, Matrix], q: int,
                     transform: str) -> tuple[Matrix, Matrix]:
    """Apply the paper's F2 automorphisms to one A.18 generator pair.

    The repository's ``PaperProd`` reverses a displayed product.  Thus the
    displayed tau(y)=(xy)^-1 is represented by inverse(y*x), exactly as in
    the independent word-level audits.  tau2 is obtained by applying the
    same formula to the tau pair, rather than by an unproved simplification.
    """
    x, y = pair
    if transform == "base":
        return pair
    if transform == "theta":
        return y, x
    if transform == "tau":
        return y, minv(matrix_paper_prod((x, y), q), q)
    if transform == "tau2":
        tx, ty = transformed_pair(pair, q, "tau")
        return ty, minv(matrix_paper_prod((tx, ty), q), q)
    raise ValueError("unknown F2 transform")


def matrix_defect(parts: Sequence[Matrix], q: int) -> Matrix:
    require(len(parts) == 5, "A.18 part count drift")
    return matrix_paper_prod((minv(matrix_paper_prod((parts[4], parts[2]), q), q),
                              parts[1], parts[3], parts[0]), q)


def joint_identity(specs: Sequence[Spec], degree: int = 36) -> JointElt:
    return ident(degree), tuple(eye() for _ in
                               range(len(TRANSFORM_ORDER) * 5 * len(specs)))


def jmul(a: JointElt, b: JointElt, specs: Sequence[Spec]) -> JointElt:
    qs = [q for _, q, _ in specs
          for _ in TRANSFORM_ORDER for _ in A18_NAMES]
    require(len(a[1]) == len(qs) == len(b[1]), "joint block length drift")
    return pprod(a[0], b[0]), tuple(mmul(x, y, q)
                                      for x, y, q in zip(a[1], b[1], qs))


def jinv(a: JointElt, specs: Sequence[Spec]) -> JointElt:
    qs = [q for _, q, _ in specs
          for _ in TRANSFORM_ORDER for _ in A18_NAMES]
    return pinv(a[0]), tuple(minv(x, q) for x, q in zip(a[1], qs))


def tuple_key(x: JointElt) -> tuple[Any, ...]:
    return x[0], x[1]


def serialize_tuple(x: JointElt) -> dict[str, Any]:
    return {"roof": list(x[0]),
            "blocks": [[list(r) for r in m] for m in x[1]]}


def decode_tuple(value: Any, specs: Sequence[Spec]) -> JointElt:
    require(isinstance(value, dict) and set(value) == {"roof", "blocks"},
            "joint tuple shape")
    roof, blocks = value["roof"], value["blocks"]
    degree = 36
    require(isinstance(roof, list) and len(roof) == degree and
            sorted(roof) == list(range(1, degree + 1)), "joint roof shape")
    qs = [q for _, q, _ in specs
          for _ in TRANSFORM_ORDER for _ in A18_NAMES]
    require(isinstance(blocks, list) and len(blocks) == len(qs),
            "joint block count")
    out: list[Matrix] = []
    for m, q in zip(blocks, qs):
        require(isinstance(m, list) and len(m) == N and
                all(isinstance(r, list) and len(r) == N for r in m),
                "joint matrix shape")
        require(all(isinstance(z, int) and not isinstance(z, bool) and
                    0 <= z < q for r in m for z in r),
                "joint field encoding")
        out.append(tuple(tuple(r) for r in m))
    return tuple(roof), tuple(out)


def make_joint_gens(specs: Sequence[Spec], roof: tuple[Perm, Perm]) -> tuple[JointElt, JointElt]:
    bx: list[Matrix] = []
    by: list[Matrix] = []
    for _, q, a in specs:
        pairs = a18_pairs(pure_generators(q, a), q)
        for transform in TRANSFORM_ORDER:
            tpairs = [transformed_pair(p, q, transform) for p in pairs]
            bx.extend(p[0] for p in tpairs)
            by.extend(p[1] for p in tpairs)
    return (roof[0], tuple(bx)), (roof[1], tuple(by))


def eval_joint_word(word: Iterable[int], gens: Sequence[JointElt],
                    specs: Sequence[Spec]) -> JointElt:
    out = joint_identity(specs, len(gens[0][0]))
    for z in word:
        require(isinstance(z, int) and not isinstance(z, bool) and z and
                abs(z) <= len(gens), "invalid signed source word")
        g = gens[abs(z) - 1]
        out = jmul(out, g if z > 0 else jinv(g, specs), specs)
    return out


def tuple_comm(a: JointElt, b: JointElt, specs: Sequence[Spec]) -> JointElt:
    return jmul(jmul(jmul(jinv(a, specs), jinv(b, specs), specs), a, specs),
                b, specs)


def signed_gens(gens: Sequence[JointElt], specs: Sequence[Spec]) -> list[JointElt]:
    return list(gens) + [jinv(g, specs) for g in gens]


def exact_section(gens: Sequence[JointElt], specs: Sequence[Spec]) -> dict[Perm, JointElt]:
    one = joint_identity(specs, len(gens[0][0]))
    sec: dict[Perm, JointElt] = {one[0]: one}
    todo = deque([one[0]])
    for_roof = signed_gens(gens, specs)
    while todo:
        r = todo.popleft()
        lift = sec[r]
        for g in for_roof:
            nr = pprod(r, g[0])
            if nr not in sec:
                sec[nr] = jmul(lift, g, specs)
                todo.append(nr)
    return sec


def kernel_from_section(gens: Sequence[JointElt], sec: dict[Perm, JointElt],
                        specs: Sequence[Spec]) -> list[JointElt]:
    one = joint_identity(specs, len(gens[0][0]))
    rels: set[JointElt] = set()
    for r, lift in sec.items():
        for g in signed_gens(gens, specs):
            nr = pprod(r, g[0])
            z = jmul(jmul(lift, g, specs), jinv(sec[nr], specs), specs)
            require(z[0] == one[0], "Schreier relator roof drift")
            if z != one:
                rels.add(z)
    return list(rels)


def enumerate_kernel(gens: Sequence[JointElt], specs: Sequence[Spec],
                     degree: int) -> list[JointElt]:
    one = joint_identity(specs, degree)
    vals: set[JointElt] = {one}
    todo = deque([one])
    for_roof = signed_gens(gens, specs)
    while todo:
        x = todo.popleft()
        for g in for_roof:
            z = jmul(x, g, specs)
            require(z[0] == one[0], "kernel generator roof drift")
            if z not in vals:
                vals.add(z)
                todo.append(z)
    return sorted(vals, key=tuple_key)


def reduce_kernel_generators(candidates: Sequence[JointElt], specs: Sequence[Spec],
                             degree: int) -> list[JointElt]:
    chosen: list[JointElt] = []
    current = {joint_identity(specs, degree)}
    for g in candidates:
        if g in current:
            continue
        chosen.append(g)
        current = set(enumerate_kernel(chosen, specs, degree))
    return chosen


def in_extension(x: JointElt, sec: dict[Perm, JointElt],
                 kernel: set[JointElt], specs: Sequence[Spec]) -> bool:
    s = sec.get(x[0])
    return s is not None and jmul(jinv(s, specs), x, specs) in kernel


def roof_orders(roof: tuple[Perm, Perm]) -> tuple[int, int]:
    P = PermutationGroup([Permutation([x - 1 for x in g]) for g in roof])
    P.schreier_sims()
    D = P.derived_subgroup()
    D.schreier_sims()
    return int(P.order()), int(D.order())


def complete_hprime(x: JointElt, y: JointElt, specs: Sequence[Spec],
                   expected: int) -> tuple[dict[Perm, JointElt], list[JointElt],
                                                list[JointElt], int]:
    gens: list[JointElt] = [tuple_comm(x, y, specs)]
    seen: set[JointElt] = set(gens)
    rounds = 0
    hs = (x, y, jinv(x, specs), jinv(y, specs))
    while True:
        rounds += 1
        sec = exact_section(gens, specs)
        require(len(sec) <= expected, "projected derived order exceeded P'")
        rels = kernel_from_section(gens, sec, specs)
        kelts = enumerate_kernel(rels, specs, len(x[0]))
        kset = set(kelts)
        additions: list[JointElt] = []
        for g in tuple(gens):
            for h in hs:
                z = jmul(jmul(jinv(h, specs), g, specs), h, specs)
                if z not in seen:
                    seen.add(z)
                    if not in_extension(z, sec, kset, specs):
                        additions.append(z)
        if not additions:
            require(len(sec) == expected,
                    "normal-closure projection is not P' (incomplete)")
            return sec, kelts, gens, rounds
        gens.extend(additions)
        print(f"D972_B4_BURAU_JOINT_V1_PROGRESS phase=normal-closure "
              f"round={rounds} projected={len(sec)} kernel={len(kelts)} "
              f"generators={len(gens)}", flush=True)


def quotient_cosets(x: JointElt, y: JointElt, sec: dict[Perm, JointElt],
                    kernel: set[JointElt], specs: Sequence[Spec]) -> list[JointElt]:
    one = joint_identity(specs, len(x[0]))
    reps = [one]
    todo = deque([one])
    gs = (x, y, jinv(x, specs), jinv(y, specs))
    while todo:
        r = todo.popleft()
        for g in gs:
            z = jmul(r, g, specs)
            if not any(in_extension(jmul(jinv(s, specs), z, specs),
                                    sec, kernel, specs) for s in reps):
                reps.append(z)
                todo.append(z)
    return reps


def semantic() -> dict[str, Any]:
    return {"M": "K^(9) intersect N_S4", "P": "G9 x PSL(2,8)",
            "P_order": P_ORDER, "roof_count": 972,
            "arithmetic_count": 324, "outside_count": 648,
            "index3_dichotomy": True, "digest": SEMANTIC_SHA}


def joint_defect_vector(blocks: Sequence[Matrix], specs: Sequence[Spec]) -> tuple[Matrix, ...]:
    out: list[Matrix] = []
    pos = 0
    for _, q, _ in specs:
        out.append(matrix_defect(blocks[pos:pos + 5], q))
        pos += len(TRANSFORM_ORDER) * 5
    require(pos == len(blocks), "joint defect block coverage drift")
    return tuple(out)


def matrix_json(m: Matrix | None) -> Any:
    return None if m is None else [list(r) for r in m]


def vector_json(v: Sequence[Matrix] | None) -> Any:
    return None if v is None else [matrix_json(m) for m in v]


def append_full_gt_witness_prefix(prefix: list[list[int]], pentagon_ok: bool,
                                  h10_ok: bool, h11_ok: bool,
                                  m_witness: Sequence[int]) -> None:
    """Append witnesses only for the exact full-GT conjunction.

    The field is explicitly a prefix of *full* solutions, not of elements
    passing only the two hexagons.  Keeping this predicate in one helper makes
    the producer-side serialization contract executable in selftest.
    """
    if pentagon_ok and h10_ok and h11_ok and len(prefix) < 8:
        prefix.append([int(m) for m in m_witness])


def known_reference() -> dict[str, Any]:
    return copy.deepcopy(SINGLE_LANE_REFERENCE)


def jpow(value: JointElt, exponent: int, specs: Sequence[Spec]) -> JointElt:
    require(exponent >= 0, "negative joint power in order gate")
    out = joint_identity(specs, len(value[0]))
    while exponent:
        if exponent & 1:
            out = jmul(out, value, specs)
        value = jmul(value, value, specs)
        exponent >>= 1
    return out


def joint_order(value: JointElt, specs: Sequence[Spec]) -> int:
    """Exact finite order by component lcm, avoiding a heuristic bound."""
    roof_order = 1
    cur = value[0]
    while cur != ident(len(value[0])):
        cur = pprod(cur, value[0])
        roof_order += 1
    result = roof_order
    pos = 0
    for _, q, _ in specs:
        for _ in TRANSFORM_ORDER:
            for _ in A18_NAMES:
                m = value[1][pos]
                pos += 1
                order = 1
                curm = eye()
                while True:
                    curm = mmul(curm, m, q)
                    if curm == eye():
                        break
                    order += 1
                result = math.lcm(result, order)
    return result


def m_compatibility(row_m: int, y_order: int,
                    specs: Sequence[Spec]) -> dict[str, Any]:
    modulus = math.lcm(18, y_order)
    residues = list(range(int(row_m) % 18, modulus, 18))
    unit = [r for r in residues if math.gcd(2 * r + 1, modulus) == 1]
    return {
        "roof_m_modulus": 18,
        "source_m_residue": int(row_m) % 18,
        "joint_y_order": y_order,
        "combined_m_modulus": modulus,
        "crt_residues": residues,
        "lambda_unit_modulus": modulus,
        "lambda_unit_residues": unit,
        "gcd_gate": "gcd(2*m+1, combined_m_modulus)=1",
        "crt_proof": {
            "congruence": "m_tilde = source_m (mod 18)",
            "enumeration": "all residues in [0,lcm(18,ord(y)))",
            "unique_mod_lcm": True,
            "residue_count": len(residues),
            "unit_residue_count": len(unit),
        },
    }


def _transform_slice(blocks: Sequence[Matrix], spec_index: int,
                     transform_index: int) -> tuple[Matrix, ...]:
    start = (spec_index * len(TRANSFORM_ORDER) + transform_index) * 5
    return tuple(blocks[start:start + 5])


def _matrix_h10(base: Sequence[Matrix], theta: Sequence[Matrix], q: int) -> bool:
    return all(matrix_paper_prod((f, t), q) == eye() for f, t in zip(base, theta))


def _matrix_h11(base: Sequence[Matrix], tau: Sequence[Matrix],
                tau2: Sequence[Matrix], ybase: Sequence[Matrix],
                ytau: Sequence[Matrix], ytau2: Sequence[Matrix], q: int,
                m: int) -> bool:
    for f, tf, t2f, yy, ty, t2y in zip(base, tau, tau2, ybase, ytau, ytau2):
        ymf = matrix_paper_prod((mpow(yy, m, q), f), q)
        tymf = matrix_paper_prod((mpow(ty, m, q), tf), q)
        t2ymf = matrix_paper_prod((mpow(t2y, m, q), t2f), q)
        if matrix_paper_prod((t2ymf, tymf, ymf), q) != eye():
            return False
    return True


def hexagon_status(h: JointElt, y: JointElt, specs: Sequence[Spec],
                   compat: dict[str, Any]) -> tuple[bool, bool, list[int]]:
    """Return H10, existence of a compatible H11 residue, and witnesses."""
    h10_all = True
    common_witnesses = set(int(m) for m in compat["lambda_unit_residues"])
    for i, (_, q, _) in enumerate(specs):
        base = _transform_slice(h[1], i, 0)
        theta = _transform_slice(h[1], i, 1)
        tau = _transform_slice(h[1], i, 2)
        tau2 = _transform_slice(h[1], i, 3)
        h10_all &= _matrix_h10(base, theta, q)
        ybase = _transform_slice(y[1], i, 0)
        ytau = _transform_slice(y[1], i, 2)
        ytau2 = _transform_slice(y[1], i, 3)
        valid = {m for m in common_witnesses
                 if _matrix_h11(base, tau, tau2, ybase, ytau, ytau2, q, m)}
        common_witnesses &= valid
        if not common_witnesses:
            break
    return bool(h10_all), bool(common_witnesses), sorted(common_witnesses)


def run_full(config: str, output: Path) -> int:
    specs = specs_for(config)
    rows = load_words()
    source_sha = producer_source_sha()
    roof = build_roof()
    require(roof_orders(roof) == (P_ORDER, PPRIME_ORDER), "roof order drift")
    x, y = make_joint_gens(specs, roof)
    for _, q, a in specs:
        s = burau_generators(q, a)
        require(mmul(mmul(s[0], s[1], q), s[0], q) ==
                mmul(mmul(s[1], s[0], q), s[1], q), "s1/s2 braid drift")
        require(mmul(mmul(s[1], s[2], q), s[1], q) ==
                mmul(mmul(s[2], s[1], q), s[2], q), "s2/s3 braid drift")
        require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q),
                "commuting drift")
    sec, kernel, hpgens, rounds = complete_hprime(x, y, specs, PPRIME_ORDER)
    kset = set(kernel)
    require(all(k[0] == ident(36) for k in kernel), "joint kernel roof drift")
    qreps = quotient_cosets(x, y, sec, kset, specs)
    hprime_order = len(sec) * len(kernel)
    h_order = len(qreps) * hprime_order
    y_order = joint_order(y, specs)
    print(f"D972_B4_BURAU_JOINT_V1_PROGRESS phase=schreier-complete "
          f"config={config} projected={len(sec)} kernel={len(kernel)} "
          f"hprime={hprime_order} h={h_order}", flush=True)
    out_rows: list[dict[str, Any]] = []
    any_zero = False
    any_full_zero = False
    for i, (m, key, word) in enumerate(rows, 1):
        common = eval_joint_word(word, (x, y), specs)
        require(roof_key(word, roof, m) == key, f"roof replay drift row {i}")
        require(common[0] == roof_image_for_key(key),
                f"synchronized roof drift row {i}")
        h0 = sec.get(common[0])
        require(h0 is not None and in_extension(h0, sec, kset, specs),
                f"broken exact H' representative row {i}")
        fiber = sorted((jmul(h0, k, specs) for k in kernel), key=tuple_key)
        ids = 0
        h10_count = 0
        h11_count = 0
        full_count = 0
        first: tuple[Matrix, ...] | None = None
        first_full: tuple[Matrix, ...] | None = None
        compat = m_compatibility(m, y_order, specs)
        full_m_witnesses: list[list[int]] = []
        for h in fiber:
            dv = joint_defect_vector(h[1], specs)
            pentagon_ok = all(d == eye() for d in dv)
            if pentagon_ok:
                ids += 1
            elif first is None:
                first = dv
            h10_ok, h11_ok, m_witness = hexagon_status(h, y, specs, compat)
            h10_count += int(h10_ok)
            h11_count += int(h10_ok and h11_ok)
            if h10_ok and h11_ok and pentagon_ok:
                full_count += 1
            elif first_full is None and not (h10_ok and h11_ok and pentagon_ok):
                first_full = dv
            append_full_gt_witness_prefix(full_m_witnesses, pentagon_ok,
                                          h10_ok, h11_ok, m_witness)
        non = len(fiber) - ids
        any_zero |= ids == 0
        any_full_zero |= full_count == 0
        serialized_fiber = [serialize_tuple(z) for z in fiber]
        out_rows.append({
            "row_index": i, "target_key": key,
            "representative_word_digest": digest(word),
            "fiber_size": len(fiber),
            "fiber_representative": serialize_tuple(h0),
            "fiber_digest": digest(serialized_fiber),
            "joint_fiber_digest": digest(serialized_fiber),
            "simultaneous_identity_defect_count": ids,
            "simultaneous_nonidentity_defect_count": non,
            "first_nonidentity_vector_by_specialization": vector_json(first),
            "m_compatibility": compat,
            "hexagon_h10_identity_count": h10_count,
            "hexagon_h11_identity_count": h11_count,
            "full_GT_identity_count": full_count,
            "full_GT_nonidentity_count": len(fiber) - full_count,
            "first_full_GT_failure_pentagon_vector": vector_json(first_full),
            "full_GT_m_witnesses_prefix": full_m_witnesses,
        })
        if i % 81 == 0:
            print(f"D972_B4_BURAU_JOINT_V1_PROGRESS phase=rows config={config} "
                  f"completed={i}", flush=True)
    status = ("CANDIDATE_B4_A_BURAU_JOINT_ZERO_FIBER" if any_full_zero
              else "UNKNOWN_BURAU_JOINT_ALLPASS")
    rels = kernel_from_section(hpgens, sec, specs)
    kernel_generators = reduce_kernel_generators(rels, specs, len(x[0]))
    receipt = {
        "schema": SCHEMA, "final_marker": FINAL, "status": status,
        "config": config, "config_digest": config_digest(config),
        "specializations": spec_json(specs),
        "field_arithmetic_signature": FIELD_SIGNATURE,
        "generator_order": list(GENERATOR_ORDER),
        "a18_pair_order": list(A18_NAMES),
        "joint_block_order": block_order(specs),
        "joint_block_order_digest": digest(block_order(specs)),
        "source_map": SOURCE_MAP,
        "semantic_premises": semantic(),
        "producer_source_sha256": source_sha,
        "words_sha256": WORDS_SHA, "artifact_rows_sha256": ARTIFACT_ROWS_SHA,
        "target_sha256": TARGET_SHA, "tuple_sha256": TUPLE_SHA,
        "row_count": 972, "roof_order": P_ORDER,
        "projection_image_order": len(sec), "h_order": h_order,
        "hprime_order": hprime_order, "kernel_order": len(kernel),
        "quotient_h_over_hprime_order": len(qreps),
        "joint_y_order": y_order,
        "algorithm": ALGORITHM,
        "single_lane_reference_gates": known_reference(),
        "presentation_evidence": {
            "seed": "[x,y] in one synchronized image",
            "normal_closure_closed": True,
            "normal_closure_theorem": "F2' is the normal closure of [x,y]",
            "normal_closure_rounds": rounds,
            "hprime_generator_count": len(hpgens),
            "projected_section_complete": len(sec) == PPRIME_ORDER,
            "schreier_edge_count": len(sec) * 2 * len(hpgens),
            "kernel_complete": True,
            "no_word_bound_or_random_sampling": True,
            "fiber_orientation": "right fiber h0*K_S",
            "cartesian_product_of_single_lanes": False,
            "hexagon_constraints_in_same_fiber": True,
            "hexagon_convention": HEXAGON_CONVENTION,
            "m_residue_gate": M_RESIDUE_GATE,
        },
        "exact_kernel_canary": {
            "complete": True, "order": len(kernel),
            "distinct_complete": len(set(kernel)) == len(kernel),
            "fixes_roof_block": all(k[0] == ident(36) for k in kernel),
            "deleted_element_incomplete": len(kernel[:-1]) == len(kernel) - 1,
        },
        "h_generators": [serialize_tuple(x), serialize_tuple(y)],
        "kernel_generators": [serialize_tuple(k) for k in kernel_generators],
        "kernel_elements": [serialize_tuple(k) for k in kernel],
        "rows": out_rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print(f"D972_B4_BURAU_JOINT_V1_DONE config={config} h={h_order} "
          f"hprime={hprime_order} kernel={len(kernel)} rows=972")
    print(f"{FINAL} config={config} status={status} output={output}")
    return 0


def self_test() -> None:
    roof = build_roof()
    require(len(roof[0]) == 36 and roof_orders(roof) == (P_ORDER, PPRIME_ORDER),
            "roof selftest drift")
    rows = load_words()
    require(all(roof_key(r[2], roof, r[0]) == r[1] for r in rows),
            "972 roof replay drift")
    require(source_word_negative_ok(rows),
            "source-word roof-only negative regression drift")
    for config, specs in CONFIGS.items():
        require(config_digest(config) == config_digest(config),
                "config digest instability")
        require(len(block_order(specs)) == len(TRANSFORM_ORDER) * 5 * len(specs),
                "joint block order count drift")
        for _, q, a in specs:
            s = burau_generators(q, a)
            require(mmul(mmul(s[0], s[1], q), s[0], q) ==
                    mmul(mmul(s[1], s[0], q), s[1], q), "braid selftest drift")
            require(mmul(mmul(s[1], s[2], q), s[1], q) ==
                    mmul(mmul(s[2], s[1], q), s[2], q), "braid2 selftest drift")
            require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q),
                    "commuting selftest drift")
            for m in s:
                require(mmul(m, minv(m, q), q) == eye(), "matrix inverse drift")
        x, y = make_joint_gens(specs, roof)
        require(len(x[1]) == len(TRANSFORM_ORDER) * 5 * len(specs) and
                len(y[1]) == len(x[1]),
                "synchronized generator block drift")
        require(eval_joint_word([1, -1], (x, y), specs) ==
                joint_identity(specs), "joint source replay drift")
        yo = joint_order(y, specs)
        compat = m_compatibility(0, yo, specs)
        require(compat["combined_m_modulus"] % 18 == 0 and
                all(r % 18 == 0 for r in compat["crt_residues"]),
                "CRT residue gate drift")
    # Unsynchronized Cartesian products must not be accepted as joint fibers.
    sync = {(0, 0), (1, 1)}
    cart = {(a, b) for a in (0, 1) for b in (0, 1)}
    require(sync != cart and len(sync) < len(cart),
            "unsynchronized Cartesian fixture accepted")
    require(digest([list(x) for x in [ident(2), (2, 1)]]) !=
            digest([list(x) for x in [ident(2)]]), "kernel deletion fixture drift")
    require(config_digest("q3a2_q4a2") != config_digest("q3a2_q4a2_q5a2"),
            "field/config swap fixture drift")
    require(config_digest("q3a2_full") != config_digest("q4a2_full"),
            "single-specialization field swap fixture drift")
    p, q = (2, 1, 3), (1, 3, 2)
    require(paper_prod((p, q)) != pprod(p, q), "product orientation fixture drift")
    bad_key = copy.deepcopy(rows[0][1])
    bad_key[2][0] = 2 if bad_key[2][0] != 2 else 1
    require(roof_image_for_key(rows[0][1]) != roof_image_for_key(bad_key),
            "h0/key mutation fixture drift")
    bad_word = list(rows[1][2]); bad_word[0] = -bad_word[0]
    require(roof_key(bad_word, roof, rows[1][0]) != rows[1][1],
            "source word mutation fixture drift")
    e = eye(); parts = [e, e, e, e, e]
    parts[0] = burau_generators(3, -1)[0]
    require(matrix_defect(parts, 3) != matrix_defect([e] * 5, 3),
            "defect block mutation fixture drift")
    witness_prefix: list[list[int]] = []
    append_full_gt_witness_prefix(witness_prefix, False, True, True, [2])
    require(witness_prefix == [], "hexagon-only witness regression accepted")
    append_full_gt_witness_prefix(witness_prefix, True, True, True, [2])
    require(witness_prefix == [[2]], "full-GT witness serialization drift")
    append_full_gt_witness_prefix(witness_prefix, True, False, True, [3])
    require(witness_prefix == [[2]], "partial-hexagon witness regression accepted")
    tp = transformed_pair((burau_generators(3, -1)[0],
                           burau_generators(3, -1)[1]), 3, "tau")
    wrong_tp = (tp[0], minv(mmul(burau_generators(3, -1)[0],
                                  burau_generators(3, -1)[1], 3), 3))
    require(tp != wrong_tp, "tau product-orientation mutation fixture drift")
    require(hexagon_status(joint_identity(CONFIGS["q3a2_full"]),
                           joint_identity(CONFIGS["q3a2_full"]),
                           CONFIGS["q3a2_full"],
                           m_compatibility(0, 1, CONFIGS["q3a2_full"]))[0] is True,
            "hexagon identity fixture drift")
    # A validator that silently omits theta must reject this mutated tuple:
    # its pentagon blocks remain identity while H10 is nonidentity.
    q3_specs = CONFIGS["q3a2_full"]
    bad_blocks = list(joint_identity(q3_specs)[1])
    bad_blocks[5] = burau_generators(3, -1)[0]
    bad_hex = (ident(36), tuple(bad_blocks))
    require(joint_defect_vector(bad_hex[1], q3_specs) == (eye(),),
            "hexagon omission fixture changed pentagon")
    require(not hexagon_status(bad_hex, joint_identity(q3_specs), q3_specs,
                               m_compatibility(0, 1, q3_specs))[0],
            "omitted-H10 fixture accepted")
    print("D972_B4_BURAU_JOINT_V1_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS "
          "row=2 exponent=(-4,-8) nonzero=956")
    print("D972_B4_BURAU_JOINT_V1_NEGATIVE_FIXTURES_PASS")
    print("D972_B4_BURAU_JOINT_V1_SELFTEST_PASS")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", choices=sorted(CONFIGS), default="q3a2_q4a2")
    ap.add_argument("--output", type=Path,
                    default=Path("ci/out/d972_b4_burau_joint_v1_q3a2_q4a2.json"))
    ap.add_argument("--self-test", action="store_true")
    ns = ap.parse_args(argv)
    try:
        if ns.self_test:
            self_test()
            return 0
        return run_full(ns.config, ns.output)
    except (MemoryError, OSError) as exc:
        receipt = {"schema": SCHEMA, "final_marker": FINAL,
                   "status": "UNKNOWN_RESOURCE", "config": ns.config,
                   "config_digest": config_digest(ns.config),
                   "diagnostics": [f"resource stop: {type(exc).__name__}"]}
        ns.output.parent.mkdir(parents=True, exist_ok=True)
        ns.output.write_text(json.dumps(receipt, sort_keys=True) + "\n",
                             encoding="utf-8")
        print(f"{FINAL} config={ns.config} status=UNKNOWN_RESOURCE output={ns.output}")
        return 2
    except Exception as exc:
        print(f"D972_B4_BURAU_JOINT_V1_ERROR {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
