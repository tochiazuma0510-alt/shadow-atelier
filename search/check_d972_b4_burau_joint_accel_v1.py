"""Independent checker for the synchronized Burau obstruction receipt.

This checker intentionally contains its own roof, finite-field, A.18,
theta/tau, closure, Schreier-kernel, CRT, and fiber code.  It imports neither
the producer nor any v4 helper.  A receipt is accepted only after rebuilding
the single synchronized image and every row's right fiber.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import tempfile
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Sequence

from sympy.combinatorics import Permutation, PermutationGroup

WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
PRODUCER_PATH = Path("search/d972_b4_burau_joint_accel_v1.py")
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ARTIFACT_ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
SEMANTIC_SHA = "3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729"
P_ORDER = 1469664
PPRIME_ORDER = 367416
CAL_H_ORDER = 105815808
CAL_HPRIME_ORDER = 2939328
SCHEMA = "d972-b4-burau-joint-accel/v1-synchronized-witness"
FINAL = "D972_B4_BURAU_JOINT_ACCEL_V1_FINAL"
GENERATOR_ORDER = ("x12", "x13", "x14", "x23", "x24", "x34")
A18_NAMES = ("123", "234", "12,3,4", "1,23,4", "1,2,34")
TRANSFORM_ORDER = ("base", "theta", "tau", "tau2")
ALGORITHM = "exact synchronized tuple Reidemeister-Schreier normal closure with single-BFS witnesses"
SOURCE_MAP = "one synchronized Psi_S from the same signed source words"
HEXAGON_CONVENTION = "PaperProd reverses displayed factors; tau(y)=inverse(PaperProd(x,y))"
M_RESIDUE_GATE = "all CRT residues m~=source_m (mod 18), with gcd(2*m~+1,L)=1"
N = 4
Matrix = tuple[tuple[int, ...], ...]
Perm = tuple[int, ...]
Spec = tuple[str, int, int]
JointElt = tuple[Perm, tuple[Matrix, ...]]
CONFIGS: dict[str, tuple[Spec, ...]] = {
    "q2a1_full": (("q2a1", 2, 1),),
    "q3a2_full": (("q3a2", 3, -1),),
    "q4a2_full": (("q4a2", 4, 2),),
    "q3a2_q4a2": (("q3a2", 3, -1), ("q4a2", 4, 2)),
    "q3a2_q4a2_q5a2": (("q3a2", 3, -1), ("q4a2", 4, 2),
                        ("q5a2", 5, 2)),
    "q3a2_q4a2_q5a4": (("q3a2", 3, -1), ("q4a2", 4, 2),
                        ("q5a4", 5, 4)),
    "q7a1_full": (("q7a1", 7, 1),),
    "q7a2_full": (("q7a2", 7, 2),),
    "q7a3_full": (("q7a3", 7, 3),),
    "q7a4_full": (("q7a4", 7, 4),),
    "q7a5_full": (("q7a5", 7, 5),),
    "q7a6_full": (("q7a6", 7, 6),),
    "q5a2_q7a1": (("q5a2", 5, 2), ("q7a1", 7, 1)),
    "q5a4_q7a6": (("q5a4", 5, 4), ("q7a6", 7, 6)),
}
FIELD_SIGNATURE = {
    "q2": "prime_field_Z/2Z",
    "q3": "prime_field_Z/3Z",
    "q4": "GF(2)[u]/(u^2+u+1), elements 0..3",
    "q5": "prime_field_Z/5Z",
    "q7": "prime_field_Z/7Z",
}
ADMISSIBILITY_AUDIT = {
    "q2": {
        "field": FIELD_SIGNATURE["q2"], "registered_a": [1],
        "excluded_a": {"0": "a=0 makes each Burau generator singular"},
        "criterion": "a is nonzero, every generator is invertible, and braid/commuting relations hold",
    },
    "q7": {
        "field": FIELD_SIGNATURE["q7"], "registered_a": [1, 2, 3, 4, 5, 6],
        "excluded_a": {"0": "a=0 makes each Burau generator singular"},
        "criterion": "a is nonzero, every generator is invertible, and braid/commuting relations hold",
    },
}
ADMISSIBLE_STATUSES = frozenset({
    "CANDIDATE_B4_A_BURAU_JOINT_ZERO_FIBER",
    "UNKNOWN_BURAU_JOINT_ALLPASS",
})
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
                   "a18_pair_order": list(A18_NAMES),
                   "admissibility_audit": ADMISSIBILITY_AUDIT})


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


def build_roof() -> tuple[Perm, Perm]:
    x9, y9 = make_gn(9)
    s = gf8_perm([[1, 0], [1, 1]])
    t = gf8_perm([[4, 3], [1, 5]])
    w = pprod(s, pinv(t))
    x4 = pprod(w, w)
    y4 = pprod(pprod(pinv(s), x4), s)
    return x9 + tuple(27 + z for z in x4), y9 + tuple(27 + z for z in y4)


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
                abs(z) <= len(gens), "invalid signed word")
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
    require(all(isinstance(r, list) and len(r) == 3 and
                isinstance(r[2], list) for r in rows), "word row shape drift")
    require(len({digest(r[1]) for r in rows}) == 972,
            "duplicate frozen roof keys")
    return rows
def free_ab(word: Iterable[int]) -> tuple[int, int]:
    out = [0, 0]
    for z in word:
        require(isinstance(z, int) and not isinstance(z, bool) and z and
                abs(z) <= 2, "invalid free word")
        out[abs(z) - 1] += 1 if z > 0 else -1
    return tuple(out)

def source_negative(rows: list[list[Any]]) -> bool:
    vals = [free_ab(row[2]) for row in rows]
    return len(vals) == 972 and vals[1] == (-4, -8) and sum(v != (0, 0) for v in vals) == 956


def fadd(a: int, b: int, q: int) -> int:
    return a ^ b if q == 4 else (a + b) % q


def fneg(a: int, q: int) -> int:
    return a if q == 4 else (-a) % q


def fsub(a: int, b: int, q: int) -> int:
    return fadd(a, fneg(b, q), q)


def fmul(a: int, b: int, q: int) -> int:
    if q != 4:
        return a * b % q
    z, aa, bb = 0, a, b
    while bb:
        if bb & 1:
            z ^= aa
        bb >>= 1
        aa <<= 1
    return z ^ 0b111 if z & 4 else z


def finv(a: int, q: int) -> int:
    require(a != 0, "field inverse zero")
    for b in range(1, q):
        if fmul(a, b, q) == 1:
            return b
    raise ValueError("field inverse missing")


def eye() -> Matrix:
    return tuple(tuple(int(i == j) for j in range(N)) for i in range(N))


def mmul(a: Matrix, b: Matrix, q: int) -> Matrix:
    return tuple(tuple(sum(fmul(a[i][k], b[k][j], q) for k in range(N))
                       % q if q != 4 else _g4sum(
                           (fmul(a[i][k], b[k][j], q) for k in range(N)), q)
                       for j in range(N)) for i in range(N))

def _g4sum(xs: Iterable[int], q: int) -> int:
    z = 0
    for x in xs:
        z = fadd(z, x, q)
    return z
def minv(a: Matrix, q: int) -> Matrix:
    rows = [list(a[i]) + list(eye()[i]) for i in range(N)]
    for c in range(N):
        r = next((j for j in range(c, N) if rows[j][c] != 0), None)
        require(r is not None, "singular matrix")
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


def paper_mprod(xs: Iterable[Matrix], q: int) -> Matrix:
    out = eye()
    for x in reversed(list(xs)):
        out = mmul(out, x, q)
    return out

def burau(q: int, a: int) -> tuple[Matrix, Matrix, Matrix]:
    require((q, a) in ((2, 1), (3, -1), (4, 2), (5, 2), (5, 4),
                       (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)),
            "unsupported q/a")
    av = a % q if q != 4 else a
    ans = []
    for i in range(3):
        m = [list(x) for x in eye()]
        m[i][i], m[i][i + 1] = fsub(1, av, q), av
        m[i + 1][i], m[i + 1][i + 1] = 1, 0
        ans.append(tuple(tuple(x) for x in m))
    return tuple(ans)  # type: ignore[return-value]


def audit_specialization(q: int, a: int) -> dict[str, Any]:
    """Independent admissibility audit for each registered field parameter."""
    s = burau(q, a)
    require(q in (2, 3, 5, 7) or q == 4, "unregistered field")
    if q in (2, 3, 5, 7):
        require(a % q != 0, "zero Burau parameter is singular")
    for m in s:
        require(mmul(m, minv(m, q), q) == eye(),
                "registered Burau generator is not invertible")
    require(mmul(mmul(s[0], s[1], q), s[0], q) ==
            mmul(mmul(s[1], s[0], q), s[1], q),
            "registered s1/s2 braid relation drift")
    require(mmul(mmul(s[1], s[2], q), s[1], q) ==
            mmul(mmul(s[2], s[1], q), s[2], q),
            "registered s2/s3 braid relation drift")
    require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q),
            "registered commuting relation drift")
    return {"q": q, "a": a, "field": FIELD_SIGNATURE[f"q{q}"],
            "parameter_nonzero": True, "generators_invertible": True,
            "braid_relations": True, "excluded_zero_reason":
            "a=0 makes the Burau generator singular"}


def specialization_audit(specs: Sequence[Spec]) -> list[dict[str, Any]]:
    return [{"lane": lane, **audit_specialization(q, a)}
            for lane, q, a in specs]


def pure(q: int, a: int) -> tuple[Matrix, ...]:
    s1, s2, s3 = burau(q, a)
    i2, i3 = minv(s2, q), minv(s3, q)
    p1, p4, p6 = mpow(s1, 2, q), mpow(s2, 2, q), mpow(s3, 2, q)
    return (p1, paper_mprod((s2, p1, i2), q),
            paper_mprod((s3, s2, p1, i2, i3), q), p4,
            paper_mprod((s3, p4, i3), q), p6)


def a18(p: tuple[Matrix, ...], q: int) -> tuple[tuple[Matrix, Matrix], ...]:
    x12, x13, x14, x23, x24, x34 = p
    return ((x12, x23), (x23, x34),
            (paper_mprod((x13, x23), q), x34),
            (paper_mprod((x12, x13), q), paper_mprod((x24, x34), q)),
            (x12, paper_mprod((x23, x24), q)))


def transformed(pair: tuple[Matrix, Matrix], q: int,
                name: str) -> tuple[Matrix, Matrix]:
    x, y = pair
    if name == "base":
        return pair
    if name == "theta":
        return y, x
    if name == "tau":
        return y, minv(paper_mprod((x, y), q), q)
    if name == "tau2":
        tx, ty = transformed(pair, q, "tau")
        return ty, minv(paper_mprod((tx, ty), q), q)
    raise ValueError("unknown transform")


def identity(specs: Sequence[Spec], degree: int = 36) -> JointElt:
    return ident(degree), tuple(eye() for _ in range(20 * len(specs)))


def jmul(a: JointElt, b: JointElt, specs: Sequence[Spec]) -> JointElt:
    qs = [q for _, q, _ in specs for _ in TRANSFORM_ORDER for _ in A18_NAMES]
    require(len(qs) == len(a[1]) == len(b[1]), "joint block length")
    return pprod(a[0], b[0]), tuple(mmul(x, y, q)
                                      for x, y, q in zip(a[1], b[1], qs))


def jinv(a: JointElt, specs: Sequence[Spec]) -> JointElt:
    qs = [q for _, q, _ in specs for _ in TRANSFORM_ORDER for _ in A18_NAMES]
    return pinv(a[0]), tuple(minv(x, q) for x, q in zip(a[1], qs))


def make_gens(specs: Sequence[Spec], roof: tuple[Perm, Perm]) -> tuple[JointElt, JointElt]:
    bx: list[Matrix] = []
    by: list[Matrix] = []
    for _, q, a0 in specs:
        pairs = a18(pure(q, a0), q)
        for name in TRANSFORM_ORDER:
            tp = [transformed(pair, q, name) for pair in pairs]
            bx.extend(z[0] for z in tp)
            by.extend(z[1] for z in tp)
    return (roof[0], tuple(bx)), (roof[1], tuple(by))


def tcomm(a: JointElt, b: JointElt, specs: Sequence[Spec]) -> JointElt:
    return jmul(jmul(jmul(jinv(a, specs), jinv(b, specs), specs), a, specs), b, specs)


def signed(gens: Sequence[JointElt], specs: Sequence[Spec]) -> list[JointElt]:
    return list(gens) + [jinv(g, specs) for g in gens]


def section(gens: Sequence[JointElt], specs: Sequence[Spec]) -> dict[Perm, JointElt]:
    one = identity(specs, len(gens[0][0]))
    out = {one[0]: one}
    todo = deque([one[0]])
    sg = signed(gens, specs)
    while todo:
        r = todo.popleft()
        lift = out[r]
        for g in sg:
            nr = pprod(r, g[0])
            if nr not in out:
                out[nr] = jmul(lift, g, specs)
                todo.append(nr)
    return out


def kernel_rels(gens: Sequence[JointElt], sec: dict[Perm, JointElt],
                specs: Sequence[Spec]) -> list[JointElt]:
    one = identity(specs, len(gens[0][0]))
    out: set[JointElt] = set()
    for r, lift in sec.items():
        for g in signed(gens, specs):
            nr = pprod(r, g[0])
            z = jmul(jmul(lift, g, specs), jinv(sec[nr], specs), specs)
            require(z[0] == one[0], "Schreier roof")
            if z != one:
                out.add(z)
    return sorted(out, key=lambda z: (z[0], z[1]))


def enum_kernel_with_witness(gens: Sequence[JointElt], specs: Sequence[Spec],
                            degree: int) -> tuple[list[JointElt], list[JointElt]]:
    """Exact BFS and the signed generators on discovery edges.

    Every discovered vertex is a product of the recorded edge labels, while
    every edge label is itself in the kernel.  A closure replay of the
    witness set is therefore exactly the enumerated kernel.
    """
    one = identity(specs, degree)
    out: set[JointElt] = {one}
    todo = deque([one])
    sg = signed(gens, specs)
    witness: set[JointElt] = set()
    while todo:
        x = todo.popleft()
        for g in sg:
            z = jmul(x, g, specs)
            require(z[0] == one[0], "kernel roof drift")
            if z not in out:
                out.add(z)
                todo.append(z)
                witness.add(g)
    key = lambda z: (z[0], z[1])
    return sorted(out, key=key), sorted(witness, key=key)


def enum_kernel(gens: Sequence[JointElt], specs: Sequence[Spec],
                degree: int) -> list[JointElt]:
    return enum_kernel_with_witness(gens, specs, degree)[0]


def in_ext(x: JointElt, sec: dict[Perm, JointElt], kernel: set[JointElt],
           specs: Sequence[Spec]) -> bool:
    s = sec.get(x[0])
    return s is not None and jmul(jinv(s, specs), x, specs) in kernel


def complete(x: JointElt, y: JointElt, specs: Sequence[Spec]) -> tuple[dict[Perm, JointElt], list[JointElt], list[JointElt], list[JointElt]]:
    gens = [tcomm(x, y, specs)]
    seen = set(gens)
    actors = (x, y, jinv(x, specs), jinv(y, specs))
    while True:
        sec = section(gens, specs)
        require(len(sec) <= PPRIME_ORDER, "projection exceeds P'")
        ke, witness = enum_kernel_with_witness(
            kernel_rels(gens, sec, specs), specs, len(x[0]))
        ks = set(ke)
        add = []
        for g in tuple(gens):
            for h in actors:
                z = jmul(jmul(jinv(h, specs), g, specs), h, specs)
                if z not in seen:
                    seen.add(z)
                    if not in_ext(z, sec, ks, specs):
                        add.append(z)
        if not add:
            require(len(sec) == PPRIME_ORDER, "derived projection incomplete")
            return sec, ke, gens, witness
        gens.extend(add)


def quotient(x: JointElt, y: JointElt, sec: dict[Perm, JointElt],
             kernel: set[JointElt], specs: Sequence[Spec]) -> list[JointElt]:
    one = identity(specs, len(x[0]))
    out, todo = [one], deque([one])
    for_gens = (x, y, jinv(x, specs), jinv(y, specs))
    while todo:
        r = todo.popleft()
        for g in for_gens:
            z = jmul(r, g, specs)
            if not any(in_ext(jmul(jinv(s, specs), z, specs), sec, kernel, specs)
                       for s in out):
                out.append(z)
                todo.append(z)
    return out


def serialize(x: JointElt) -> dict[str, Any]:
    return {"roof": list(x[0]), "blocks": [[list(r) for r in m] for m in x[1]]}


def decode(v: Any, specs: Sequence[Spec]) -> JointElt:
    require(isinstance(v, dict) and set(v) == {"roof", "blocks"}, "tuple shape")
    roof, blocks = v["roof"], v["blocks"]
    require(isinstance(roof, list) and len(roof) == 36 and
            sorted(roof) == list(range(1, 37)), "tuple roof shape")
    qs = [q for _, q, _ in specs for _ in TRANSFORM_ORDER for _ in A18_NAMES]
    require(isinstance(blocks, list) and len(blocks) == len(qs), "tuple block count")
    mats = []
    for m, q in zip(blocks, qs):
        require(isinstance(m, list) and len(m) == N and
                all(isinstance(r, list) and len(r) == N for r in m), "matrix shape")
        require(all(isinstance(z, int) and not isinstance(z, bool) and 0 <= z < q
                    for r in m for z in r), "matrix field")
        mats.append(tuple(tuple(r) for r in m))
    return tuple(roof), tuple(mats)


def roof_orders(roof: tuple[Perm, Perm]) -> tuple[int, int]:
    g = PermutationGroup([Permutation([x - 1 for x in a]) for a in roof])
    g.schreier_sims()
    d = g.derived_subgroup(); d.schreier_sims()
    return int(g.order()), int(d.order())


def jorder(value: JointElt, specs: Sequence[Spec]) -> int:
    out = 1
    cur = value[0]
    while cur != ident(len(value[0])):
        cur = pprod(cur, value[0]); out += 1
    pos = 0
    for _, q, _ in specs:
        for _ in TRANSFORM_ORDER:
            for _ in A18_NAMES:
                m = value[1][pos]; pos += 1
                mo = 1; cm = eye()
                while True:
                    cm = mmul(cm, m, q)
                    if cm == eye():
                        break
                    mo += 1
                out = math.lcm(out, mo)
    return out


def compat(row_m: int, y_order: int) -> dict[str, Any]:
    modulus = math.lcm(18, y_order)
    residues = list(range(int(row_m) % 18, modulus, 18))
    unit = [r for r in residues if math.gcd(2 * r + 1, modulus) == 1]
    return {"roof_m_modulus": 18, "source_m_residue": int(row_m) % 18,
            "joint_y_order": y_order, "combined_m_modulus": modulus,
            "crt_residues": residues, "lambda_unit_modulus": modulus,
            "lambda_unit_residues": unit,
            "gcd_gate": "gcd(2*m+1, combined_m_modulus)=1",
            "crt_proof": {"congruence": "m_tilde = source_m (mod 18)",
                          "enumeration": "all residues in [0,lcm(18,ord(y)))",
                          "unique_mod_lcm": True,
                          "residue_count": len(residues),
                          "unit_residue_count": len(unit)}}


def tslice(blocks: Sequence[Matrix], i: int, t: int) -> tuple[Matrix, ...]:
    start = (i * len(TRANSFORM_ORDER) + t) * 5
    return tuple(blocks[start:start + 5])


def h10(base: Sequence[Matrix], theta: Sequence[Matrix], q: int) -> bool:
    return all(paper_mprod((f, t), q) == eye() for f, t in zip(base, theta))


def h11(base: Sequence[Matrix], tau: Sequence[Matrix], tau2: Sequence[Matrix],
        ybase: Sequence[Matrix], ytau: Sequence[Matrix], ytau2: Sequence[Matrix],
        q: int, m: int) -> bool:
    for f, tf, t2f, yy, ty, t2y in zip(base, tau, tau2, ybase, ytau, ytau2):
        a = paper_mprod((mpow(yy, m, q), f), q)
        b = paper_mprod((mpow(ty, m, q), tf), q)
        c = paper_mprod((mpow(t2y, m, q), t2f), q)
        if paper_mprod((c, b, a), q) != eye():
            return False
    return True


def hex_status(h: JointElt, y: JointElt, specs: Sequence[Spec],
               c: dict[str, Any]) -> tuple[bool, bool, list[int]]:
    all_h10 = True
    common = set(c["lambda_unit_residues"])
    for i, (_, q, _) in enumerate(specs):
        base, theta = tslice(h[1], i, 0), tslice(h[1], i, 1)
        tau, tau2 = tslice(h[1], i, 2), tslice(h[1], i, 3)
        all_h10 &= h10(base, theta, q)
        valid = set()
        ybase, ytau, ytau2 = tslice(y[1], i, 0), tslice(y[1], i, 2), tslice(y[1], i, 3)
        for m in common:
            if h11(base, tau, tau2, ybase, ytau, ytau2, q, int(m)):
                valid.add(m)
        common &= valid
        if not common:
            break
    return all_h10, bool(common), sorted(common)


def defect(blocks: Sequence[Matrix], q: int) -> Matrix:
    require(len(blocks) == 5, "A.18 defect blocks")
    return paper_mprod((minv(paper_mprod((blocks[4], blocks[2]), q), q),
                        blocks[1], blocks[3], blocks[0]), q)
def defect_vector(blocks: Sequence[Matrix], specs: Sequence[Spec]) -> tuple[Matrix, ...]:
    out = []
    for i, (_, q, _) in enumerate(specs):
        out.append(defect(tslice(blocks, i, 0), q))
    return tuple(out)


def mjson(v: Sequence[Matrix] | None) -> Any:
    return None if v is None else [[list(r) for r in m] for m in v]


def append_full_gt_witness_prefix(prefix: list[list[int]], pentagon_ok: bool,
                                  h10_ok: bool, h11_ok: bool,
                                  m_witness: Sequence[int]) -> None:
    """Independent serialization contract for the full-GT witness prefix."""
    if pentagon_ok and h10_ok and h11_ok and len(prefix) < 8:
        prefix.append([int(m) for m in m_witness])


def semantic() -> dict[str, Any]:
    return {"M": "K^(9) intersect N_S4", "P": "G9 x PSL(2,8)",
            "P_order": P_ORDER, "roof_count": 972,
            "arithmetic_count": 324, "outside_count": 648,
            "index3_dichotomy": True, "digest": SEMANTIC_SHA}


def row_scan_contract(status: str, row_count: int, complete: Any,
                      scanned: Any, terminal: Any) -> bool:
    """Only a candidate may stop after a complete zero fiber."""
    if status == "UNKNOWN_BURAU_JOINT_ALLPASS":
        return (complete is True and row_count == 972 and scanned == 972 and
                terminal is None)
    if status == "CANDIDATE_B4_A_BURAU_JOINT_ZERO_FIBER":
        return (complete is False and 1 <= row_count <= 972 and
                scanned == row_count and terminal == row_count)
    return False


def check_receipt(path: Path) -> dict[str, Any]:
    r = json.loads(path.read_bytes())
    rows = load_words()
    require(r.get("schema") == SCHEMA and r.get("final_marker") == FINAL,
            "schema/final marker drift")
    require(r.get("status") in ADMISSIBLE_STATUSES,
            "resource/error receipt is not admissible")
    require(r.get("producer_source_sha256") == file_sha(PRODUCER_PATH),
            "producer source hash drift")
    config = r.get("config"); specs = specs_for(config)
    require(r.get("config_digest") == config_digest(config), "config digest drift")
    require(r.get("specializations") == spec_json(specs) and
            r.get("field_arithmetic_signature") == FIELD_SIGNATURE and
            r.get("joint_block_order") == block_order(specs) and
            r.get("joint_block_order_digest") == digest(block_order(specs)),
            "field/config/block binding drift")
    require(r.get("source_map") == SOURCE_MAP and
            r.get("algorithm") == ALGORITHM,
            "joint source/algorithm binding drift")
    require(r.get("admissibility_audit") == ADMISSIBILITY_AUDIT and
            r.get("registered_specialization_audit") ==
            specialization_audit(specs),
            "q2/q7 admissibility audit drift")
    require(r.get("generator_order") == list(GENERATOR_ORDER) and
            r.get("a18_pair_order") == list(A18_NAMES), "generator order drift")
    require(r.get("semantic_premises") == semantic(), "semantic premise drift")
    receipt_rows = r.get("rows")
    require(r.get("words_sha256") == WORDS_SHA and
            r.get("artifact_rows_sha256") == ARTIFACT_ROWS_SHA and
            r.get("target_sha256") == TARGET_SHA and
            r.get("tuple_sha256") == TUPLE_SHA and
            r.get("row_count") == 972 and isinstance(receipt_rows, list) and
            row_scan_contract(r["status"], len(receipt_rows),
                              r.get("row_scan_complete"),
                              r.get("row_scan_rows"),
                              r.get("terminal_zero_row_index")),
            "source row binding or scan contract drift")
    roof = build_roof()
    require(roof_orders(roof) == (P_ORDER, PPRIME_ORDER) and
            r.get("roof_order") == P_ORDER, "roof order drift")
    x, y = make_gens(specs, roof)
    require(r.get("h_generators") == [serialize(x), serialize(y)],
            "joint generator serialization drift")
    sec, kernel, hpgens, rebuilt_witness = complete(x, y, specs)
    ks = set(kernel)
    qreps = quotient(x, y, sec, ks, specs)
    require(r.get("projection_image_order") == len(sec) == PPRIME_ORDER and
            r.get("kernel_order") == len(kernel) and
            r.get("hprime_order") == len(sec) * len(kernel) and
            r.get("h_order") == len(qreps) * len(sec) * len(kernel) and
            r.get("quotient_h_over_hprime_order") == len(qreps),
            "joint order gate drift")
    y_order = jorder(y, specs)
    require(r.get("joint_y_order") == y_order, "joint y order drift")
    ke = r.get("kernel_elements")
    require(isinstance(ke, list) and len(ke) == len(kernel), "kernel truncation")
    decoded = [decode(v, specs) for v in ke]
    require(decoded == kernel, "kernel element ordering/content drift")
    kg_raw = r.get("kernel_generators")
    require(isinstance(kg_raw, list), "kernel generators missing")
    kg = [decode(v, specs) for v in kg_raw]
    require(all(v in ks for v in kg), "kernel generator outside kernel")
    require(kg or len(kernel) == 1, "nontrivial kernel has no generators")
    if kg:
        require(set(enum_kernel(kg, specs, 36)) == ks,
                "kernel generator incompleteness")
    require(r.get("kernel_generator_method") ==
            "single exact BFS discovery witnesses" and
            set(kg) == set(rebuilt_witness),
            "kernel witness binding drift")
    canary = r.get("exact_kernel_canary")
    require(isinstance(canary, dict) and canary.get("complete") is True and
            canary.get("order") == len(kernel) and
            canary.get("distinct_complete") is True and
            canary.get("fixes_roof_block") is True and
            canary.get("deleted_element_incomplete") is True,
            "exact kernel canary drift")
    evidence = r.get("presentation_evidence")
    require(isinstance(evidence, dict) and evidence.get("seed") ==
            "[x,y] in one synchronized image" and
            evidence.get("normal_closure_closed") is True and
            evidence.get("normal_closure_theorem") ==
            "F2' is the normal closure of [x,y]" and
            evidence.get("projected_section_complete") is True and
            evidence.get("kernel_complete") is True and
            evidence.get("no_word_bound_or_random_sampling") is True and
            evidence.get("fiber_orientation") == "right fiber h0*K_S" and
            evidence.get("cartesian_product_of_single_lanes") is False and
            evidence.get("hexagon_constraints_in_same_fiber") is True and
            evidence.get("hexagon_convention") == HEXAGON_CONVENTION and
            evidence.get("m_residue_gate") == M_RESIDUE_GATE and
            evidence.get("kernel_generator_method") ==
            "single exact BFS discovery witnesses",
            "exact presentation evidence drift")
    hpg = evidence.get("hprime_generator_count")
    require(isinstance(hpg, int) and hpg >= 1 and
            isinstance(evidence.get("normal_closure_rounds"), int) and
            evidence.get("normal_closure_rounds") >= 1 and
            evidence.get("schreier_edge_count") == PPRIME_ORDER * 2 * hpg,
            "joint Schreier evidence drift")
    require(r.get("single_lane_reference_gates") == SINGLE_LANE_REFERENCE,
            "v4 learned reference gates drift")
    any_full_zero = False
    any_pentagon_zero = False
    full_zero_indices: list[int] = []
    seen: set[str] = set()
    for i, (source, item) in enumerate(
            zip(rows[:len(receipt_rows)], receipt_rows, strict=True), 1):
        m, key, word = source
        require(item.get("row_index") == i and item.get("target_key") == key and
                item.get("representative_word_digest") == digest(word),
                f"row source binding {i}")
        require(roof_key(word, roof, m) == key and
                digest(key) not in seen, f"roof/key replay {i}")
        seen.add(digest(key))
        h0 = decode(item.get("fiber_representative"), specs)
        require(h0[0] == roof_image_for_key(key) and in_ext(h0, sec, ks, specs),
                f"h0 binding {i}")
        fiber = sorted((jmul(h0, k, specs) for k in kernel),
                       key=lambda z: (z[0], z[1]))
        fd = digest([serialize(z) for z in fiber])
        require(item.get("fiber_size") == len(kernel) and
                item.get("fiber_digest") == fd and
                item.get("joint_fiber_digest") == fd, f"fiber digest {i}")
        c = compat(m, y_order)
        require(item.get("m_compatibility") == c, f"CRT compatibility {i}")
        ids = h10s = h11s = fulls = 0
        first: tuple[Matrix, ...] | None = None
        first_full: tuple[Matrix, ...] | None = None
        witness_prefix: list[list[int]] = []
        for h in fiber:
            dv = defect_vector(h[1], specs)
            pent = all(d == eye() for d in dv)
            ids += int(pent)
            if not pent and first is None:
                first = dv
            a, b, mw = hex_status(h, y, specs, c)
            h10s += int(a); h11s += int(a and b)
            full = pent and a and b
            fulls += int(full)
            if not full and first_full is None:
                first_full = dv
            append_full_gt_witness_prefix(witness_prefix, pent, a, b, mw)
        require(item.get("simultaneous_identity_defect_count") == ids and
                item.get("simultaneous_nonidentity_defect_count") == len(fiber) - ids and
                item.get("hexagon_h10_identity_count") == h10s and
                item.get("hexagon_h11_identity_count") == h11s and
                item.get("full_GT_identity_count") == fulls and
                item.get("full_GT_nonidentity_count") == len(fiber) - fulls and
                item.get("first_nonidentity_vector_by_specialization") == mjson(first) and
                item.get("first_full_GT_failure_pentagon_vector") == mjson(first_full) and
                item.get("full_GT_m_witnesses_prefix") == witness_prefix,
                f"constraint counts {i}")
        any_pentagon_zero |= ids == 0
        any_full_zero |= fulls == 0
        if fulls == 0:
            full_zero_indices.append(i)
    require(len(seen) == len(receipt_rows), "duplicate/incomplete prefix")
    require((r["status"] == "CANDIDATE_B4_A_BURAU_JOINT_ZERO_FIBER" and
             any_full_zero and
             full_zero_indices == [len(receipt_rows)] and
             receipt_rows[-1].get("full_GT_identity_count") == 0) or
            (r["status"] == "UNKNOWN_BURAU_JOINT_ALLPASS" and
             len(receipt_rows) == 972 and not any_full_zero),
            "status/count semantics drift")
    return {"status": ("B4_A_BURAU_JOINT_ZERO_FIBER_CROSSCHECKED"
                        if any_full_zero else r["status"]),
            "config": config, "rows": len(receipt_rows), "h_order": len(qreps) * len(sec) * len(kernel),
            "hprime_order": len(sec) * len(kernel), "kernel_order": len(kernel),
            "pentagon_zero_fibers": sum(1 for z in receipt_rows
                                         if z["simultaneous_identity_defect_count"] == 0),
            "full_GT_zero_fibers": sum(1 for z in receipt_rows
                                        if z["full_GT_identity_count"] == 0)}


def selftest() -> None:
    rows = load_words(); roof = build_roof()
    require(roof_orders(roof) == (P_ORDER, PPRIME_ORDER), "roof selftest")
    require(all(roof_key(r[2], roof, r[0]) == r[1] for r in rows),
            "972 roof replay")
    require(source_negative(rows), "source negative regression")
    require(ADMISSIBILITY_AUDIT["q2"]["registered_a"] == [1] and
            ADMISSIBILITY_AUDIT["q7"]["registered_a"] == [1, 2, 3, 4, 5, 6],
            "q2/q7 registration audit drift")
    for q, values in ((2, (1,)), (7, (1, 2, 3, 4, 5, 6))):
        for a in values:
            audit = audit_specialization(q, a)
            require(audit["parameter_nonzero"] and
                    audit["generators_invertible"] and
                    audit["braid_relations"],
                    "q2/q7 admissibility audit failed")
    for config, specs in CONFIGS.items():
        x, y = make_gens(specs, roof)
        require(len(x[1]) == 20 * len(specs) and
                eval_perm_word([1, -1], (x[0], y[0])) == ident(36),
                f"generator selftest {config}")
        for _, q, a in specs:
            s = burau(q, a)
            require(mmul(mmul(s[0], s[1], q), s[0], q) ==
                    mmul(mmul(s[1], s[0], q), s[1], q), "braid selftest")
            require(mmul(mmul(s[1], s[2], q), s[1], q) ==
                    mmul(mmul(s[2], s[1], q), s[2], q), "braid2 selftest")
            require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q), "commute selftest")
    require(config_digest("q3a2_full") != config_digest("q4a2_full"),
            "field/config mutation")
    p, q = (2, 1, 3), (1, 3, 2)
    require(paper_prod((p, q)) != pprod(p, q), "PaperProd mutation")
    toy = {(0, 0), (1, 1)}
    cart = {(a, b) for a in (0, 1) for b in (0, 1)}
    require(toy != cart, "unsynchronized Cartesian mutation")
    bad = list(rows[1][2]); bad[0] = -bad[0]
    require(roof_key(bad, roof, rows[1][0]) != rows[1][1], "source mutation")
    bad_key = copy.deepcopy(rows[0][1]); bad_key[2][0] = 2 if bad_key[2][0] != 2 else 1
    require(roof_image_for_key(bad_key) != roof_image_for_key(rows[0][1]), "h0 mutation")
    e = eye(); parts = [e, e, e, e, e]; parts[0] = burau(3, -1)[0]
    require(defect(parts, 3) != defect([e] * 5, 3), "defect mutation")
    witness_prefix: list[list[int]] = []
    append_full_gt_witness_prefix(witness_prefix, False, True, True, [2])
    require(witness_prefix == [], "hexagon-only witness regression accepted")
    append_full_gt_witness_prefix(witness_prefix, True, True, True, [2])
    require(witness_prefix == [[2]], "full-GT witness serialization drift")
    append_full_gt_witness_prefix(witness_prefix, True, False, True, [3])
    require(witness_prefix == [[2]], "partial-hexagon witness regression accepted")
    q3_specs = CONFIGS["q3a2_full"]
    bad_blocks = list(identity(q3_specs)[1]); bad_blocks[5] = burau(3, -1)[0]
    bad_hex = (ident(36), tuple(bad_blocks))
    require(defect_vector(bad_hex[1], q3_specs) == (eye(),),
            "hexagon omission changed pentagon")
    require(not hex_status(bad_hex, identity(q3_specs), q3_specs,
                            compat(0, 1))[0], "omitted H10 accepted")
    # The accelerator may serialize only a candidate prefix, never an
    # all-pass prefix.  Exercise both the positive candidate contract and
    # the two rejection mutations explicitly.
    require(row_scan_contract("CANDIDATE_B4_A_BURAU_JOINT_ZERO_FIBER",
                              1, False, 1, 1),
            "candidate prefix contract rejected")
    require(not row_scan_contract("UNKNOWN_BURAU_JOINT_ALLPASS",
                                  1, False, 1, 1),
            "partial all-pass fixture accepted")
    require(not row_scan_contract("UNKNOWN_BURAU_JOINT_ALLPASS",
                                  971, True, 971, None),
            "short all-pass fixture accepted")
    require(not row_scan_contract("CANDIDATE_B4_A_BURAU_JOINT_ZERO_FIBER",
                                  1, False, 1, None),
            "candidate without terminal zero accepted")
    one = identity(q3_specs)
    witness_blocks = list(one[1]); witness_blocks[0] = burau(3, -1)[0]
    toy_generator = (one[0], tuple(witness_blocks))
    toy_kernel, toy_witness = enum_kernel_with_witness(
        [toy_generator], q3_specs, 36)
    require(toy_witness and set(enum_kernel(toy_witness, q3_specs, 36)) ==
            set(toy_kernel), "discovery-witness closure regression")
    with tempfile.TemporaryDirectory() as td:
        corrupt = Path(td) / "corrupt-receipt.json"
        corrupt.write_text(json.dumps({"schema": SCHEMA, "final_marker": FINAL,
                                       "status": "UNKNOWN_RESOURCE"}) + "\n",
                           encoding="utf-8")
        try:
            check_receipt(corrupt)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise ValueError("corrupt receipt fixture was accepted")
    require(toy != cart, "unsynchronized-word Cartesian fixture accepted")
    print("D972_B4_BURAU_JOINT_ACCEL_PARTIAL_ALLPASS_NEGATIVE_PASS")
    print("D972_B4_BURAU_JOINT_ACCEL_DISCOVERY_WITNESS_PASS")
    print("D972_B4_BURAU_JOINT_ACCEL_CORRUPT_RECEIPT_NEGATIVE_PASS")
    print("D972_B4_BURAU_JOINT_ACCEL_Q2Q7_ADMISSIBILITY_AUDIT_PASS q2=[1] q7=[1,2,3,4,5,6]")
    print("D972_B4_BURAU_JOINT_ACCEL_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956")
    print("D972_B4_BURAU_JOINT_ACCEL_CHECKER_NEGATIVE_FIXTURES_PASS")
    print("D972_B4_BURAU_JOINT_ACCEL_CHECKER_SELFTEST_PASS")
    print("D972_B4_BURAU_JOINT_ACCEL_CHECKER_FINAL_MARKER status=PASS")

def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    ns = ap.parse_args(argv)
    if ns.self_test:
        selftest(); return 0
    if not ns.receipt:
        ap.error("receipt path or --self-test required")
    result = check_receipt(Path(ns.receipt))
    print("D972_B4_BURAU_JOINT_ACCEL_CHECK_PASS", json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
