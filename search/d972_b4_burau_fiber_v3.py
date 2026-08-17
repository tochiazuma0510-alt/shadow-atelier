"""Exact low-memory Burau fiber producer.

The finite extension is represented by ``(roof permutation, five 4x4
matrices)`` tuples.  The projected derived group is traversed exactly and a
Reidemeister--Schreier edge set generates the matrix-only kernel.  No
q**4-point Burau action, and in particular no 3161-point permutation group,
is constructed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
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
SCHEMA = "d972-b4-burau-fiber/v3-lowmem"
FINAL = "D972_B4_BURAU_FIBER_V3_FINAL"
PRESENTATION_ALGORITHM = "exact tuple Reidemeister-Schreier normal closure"
COMMON_WORD_PROVENANCE = "exact direct replay in tuple H; H' via Schreier section"
GENERATOR_ORDER = ("x12", "x13", "x14", "x23", "x24", "x34")
A18_NAMES = ("123", "234", "12,3,4", "1,23,4", "1,2,34")
N = 4
Matrix = tuple[tuple[int, ...], ...]
Perm = tuple[int, ...]
TupleElt = tuple[Perm, tuple[Matrix, ...]]


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
    """Hash the exact producer being executed, binding calibrations to it."""
    return file_sha(Path(__file__).resolve())


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


# ---- frozen compact roof -------------------------------------------------

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
    require(1 <= a <= 7, "GF(8) inverse drift")
    for b in range(1, 8):
        if gf8_mul(a, b) == 1:
            return b
    raise ValueError("GF(8) inverse missing")


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


def d9_coords(p: Perm) -> list[int]:
    r, s = make_dn(9)
    for a in range(9):
        for e in range(2):
            if p == pprod(ppow(r, a), ppow(s, e)):
                return [a, e]
    raise ValueError("D9 coordinate drift")


def block(p: Perm, offset: int, size: int) -> Perm:
    z = tuple(p[offset + i] - offset for i in range(size))
    require(set(z) == set(range(1, size + 1)), "roof block drift")
    return z


def roof_key(word: list[int], roof: tuple[Perm, Perm], m: int) -> list[Any]:
    f = eval_word(word, roof)
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


def eval_word(word: Iterable[int], gens: Sequence[Any]) -> Any:
    out = gens[0][0] if False else None
    # The caller supplies either two permutations or two tuple elements.
    if isinstance(gens[0], tuple) and len(gens[0]) == 2 and isinstance(gens[0][1], tuple):
        out = tuple_identity(len(gens[0][0]), len(gens[0][1]), 5)
        for x in word:
            require(isinstance(x, int) and not isinstance(x, bool) and x and
                    abs(x) <= len(gens), "invalid signed word")
            g = gens[abs(x) - 1]
            out = tmul(out, g if x > 0 else tinv(g))
        return out
    outp = ident(len(gens[0]))
    for x in word:
        require(isinstance(x, int) and not isinstance(x, bool) and x and
                abs(x) <= len(gens), "invalid signed word")
        g = gens[abs(x) - 1]
        outp = pprod(outp, g if x > 0 else pinv(g))
    return outp


# ---- finite-field 4x4 Burau blocks --------------------------------------

def fadd(a: int, b: int, q: int) -> int:
    return (a ^ b) if q == 4 else (a + b) % q


def fneg(a: int, q: int) -> int:
    return a if q == 4 else (-a) % q


def fsub(a: int, b: int, q: int) -> int:
    return fadd(a, fneg(b, q), q)


def fmul(a: int, b: int, q: int) -> int:
    if q != 4:
        return (a * b) % q
    z = 0
    aa, bb = a, b
    while bb:
        if bb & 1:
            z ^= aa
        bb >>= 1
        aa <<= 1
    if z & 4:
        z ^= 0b111
    return z


def finv(a: int, q: int) -> int:
    require(a != 0, "field inverse of zero")
    for b in range(1, q):
        if fmul(a, b, q) == 1:
            return b
    raise ValueError("field inverse missing")


def eye() -> Matrix:
    return tuple(tuple(int(i == j) for j in range(N)) for i in range(N))


def mmul(a: Matrix, b: Matrix, q: int) -> Matrix:
    return tuple(tuple(
        _fsum((fmul(a[i][k], b[k][j], q) for k in range(N)), q)
        for j in range(N)) for i in range(N))


def _fsum(xs: Iterable[int], q: int) -> int:
    z = 0
    for x in xs:
        z = fadd(z, x, q)
    return z


def minv(a: Matrix, q: int) -> Matrix:
    rows = [list(a[i]) + list(eye()[i]) for i in range(N)]
    for c in range(N):
        r = next((z for z in range(c, N) if rows[z][c] != 0), None)
        require(r is not None, "singular Burau matrix")
        rows[c], rows[r] = rows[r], rows[c]
        z = finv(rows[c][c], q)
        rows[c] = [fmul(x, z, q) for x in rows[c]]
        for rr in range(N):
            if rr != c:
                z = rows[rr][c]
                rows[rr] = [fsub(x, fmul(z, y, q), q)
                            for x, y in zip(rows[rr], rows[c])]
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


def matrix_defect(parts: Sequence[Matrix], q: int) -> Matrix:
    require(len(parts) == 5, "A.18 part count drift")
    return matrix_paper_prod((minv(matrix_paper_prod((parts[4], parts[2]), q), q),
                              parts[1], parts[3], parts[0]), q)


# ---- tuple extension and exact Schreier machinery -----------------------

def tuple_identity(roof_degree: int, blocks: int, q: int) -> TupleElt:
    del q
    return ident(roof_degree), tuple(eye() for _ in range(blocks))


def tmul(a: TupleElt, b: TupleElt, q: int | None = None) -> TupleElt:
    # q is inferred by matrix entries only for identity-free multiplication;
    # callers pass the globally selected field through TQ.
    z = TQ if q is None else q
    return pprod(a[0], b[0]), tuple(mmul(x, y, z) for x, y in zip(a[1], b[1]))


def tinv(a: TupleElt, q: int | None = None) -> TupleElt:
    z = TQ if q is None else q
    return pinv(a[0]), tuple(minv(x, z) for x in a[1])


TQ = 5


def tuple_key(x: TupleElt) -> tuple[Any, ...]:
    return (x[0], x[1])


def serialize_tuple(x: TupleElt) -> dict[str, Any]:
    return {"roof": list(x[0]), "blocks": [[list(r) for r in m] for m in x[1]]}


def make_tuple_gens(q: int, a: int, roof: tuple[Perm, Perm]) -> tuple[TupleElt, TupleElt]:
    pairs = a18_pairs(pure_generators(q, a), q)
    return (roof[0], tuple((m if True else m) for m in
                           (pairs[i][0] for i in range(5)))), \
           (roof[1], tuple(pairs[i][1] for i in range(5)))


def tuple_comm(a: TupleElt, b: TupleElt) -> TupleElt:
    return tmul(tmul(tmul(tinv(a), tinv(b)), a), b)


def signed_gens(gens: Sequence[TupleElt]) -> list[TupleElt]:
    return list(gens) + [tinv(g) for g in gens]


def exact_section(gens: Sequence[TupleElt], q: int) -> dict[Perm, TupleElt]:
    one = tuple_identity(len(gens[0][0]), len(gens[0][1]), q)
    sg = signed_gens(gens)
    sec: dict[Perm, TupleElt] = {one[0]: one}
    todo = deque([one[0]])
    while todo:
        r = todo.popleft()
        lift = sec[r]
        for g in sg:
            nr = pprod(r, g[0])
            if nr not in sec:
                sec[nr] = tmul(lift, g, q)
                todo.append(nr)
    return sec


def kernel_from_section(gens: Sequence[TupleElt], sec: dict[Perm, TupleElt],
                        q: int) -> list[TupleElt]:
    one = tuple_identity(len(gens[0][0]), len(gens[0][1]), q)
    rels: set[TupleElt] = set()
    for r, lift in sec.items():
        for g in signed_gens(gens):
            nr = pprod(r, g[0])
            rel = tmul(tmul(lift, g, q), tinv(sec[nr], q), q)
            require(rel[0] == one[0], "Schreier relator roof drift")
            if rel != one:
                rels.add(rel)
    return list(rels)


def enumerate_kernel(gens: Sequence[TupleElt], q: int, degree: int) -> list[TupleElt]:
    one = tuple_identity(degree, 5, q)
    vals: set[TupleElt] = {one}
    todo = deque([one])
    sg = signed_gens(gens)
    while todo:
        x = todo.popleft()
        for g in sg:
            y = tmul(x, g, q)
            require(y[0] == one[0], "kernel generator roof drift")
            if y not in vals:
                vals.add(y)
                todo.append(y)
    return sorted(vals, key=tuple_key)


def reduce_kernel_generators(candidates: Sequence[TupleElt], q: int,
                             degree: int) -> list[TupleElt]:
    """Keep an exact generating subset; no heuristic or order cap is used."""
    chosen: list[TupleElt] = []
    current = {tuple_identity(degree, 5, q)}
    for g in candidates:
        if g in current:
            continue
        chosen.append(g)
        current = set(enumerate_kernel(chosen, q, degree))
    return chosen


def in_extension(x: TupleElt, sec: dict[Perm, TupleElt], kernel: set[TupleElt],
                 q: int) -> bool:
    s = sec.get(x[0])
    if s is None:
        return False
    return tmul(tinv(s, q), x, q) in kernel


def roof_orders(roof: tuple[Perm, Perm]) -> tuple[int, int]:
    P = PermutationGroup([Permutation([x - 1 for x in g]) for g in roof])
    P.schreier_sims()
    D = P.derived_subgroup()
    D.schreier_sims()
    return int(P.order()), int(D.order())


def complete_hprime(x: TupleElt, y: TupleElt, q: int,
                   pprime_order: int) -> tuple[dict[Perm, TupleElt], list[TupleElt],
                                                  list[TupleElt], int]:
    seed = tuple_comm(x, y)
    gens: list[TupleElt] = [seed]
    seen: set[TupleElt] = {seed}
    rounds = 0
    hs = (x, y, tinv(x, q), tinv(y, q))
    while True:
        rounds += 1
        sec = exact_section(gens, q)
        require(len(sec) <= pprime_order, "projected derived order exceeded P'")
        kgen = kernel_from_section(gens, sec, q)
        kelts = enumerate_kernel(kgen, q, len(x[0]))
        kset = set(kelts)
        additions: list[TupleElt] = []
        for g in tuple(gens):
            for h in hs:
                z = tmul(tmul(tinv(h, q), g, q), h, q)
                if z not in seen:
                    seen.add(z)
                    if not in_extension(z, sec, kset, q):
                        additions.append(z)
        if not additions:
            require(len(sec) == pprime_order,
                    "normal-closure projection is not P' (incomplete)")
            # Every tested conjugate of every generator lies in L; hence L is
            # normal in <x,y>, contains [x,y], and equals the derived group.
            return sec, kelts, gens, rounds
        gens.extend(additions)
        print(f"D972_B4_BURAU_V3_PROGRESS phase=normal-closure round={rounds} "
              f"projected={len(sec)} kernel={len(kelts)} generators={len(gens)}",
              flush=True)


def quotient_cosets(x: TupleElt, y: TupleElt, sec: dict[Perm, TupleElt],
                    kernel: set[TupleElt], q: int) -> list[TupleElt]:
    one = tuple_identity(len(x[0]), 5, q)
    reps = [one]
    todo = deque([one])
    gs = (x, y, tinv(x, q), tinv(y, q))
    while todo:
        r = todo.popleft()
        for g in gs:
            z = tmul(r, g, q)
            if not any(in_extension(tmul(tinv(s, q), z, q), sec, kernel, q)
                       for s in reps):
                reps.append(z)
                todo.append(z)
    return reps


# ---- receipt and checks --------------------------------------------------

def semantic() -> dict[str, Any]:
    return {"M": "K^(9) intersect N_S4", "P": "G9 x PSL(2,8)",
            "P_order": P_ORDER, "roof_count": 972, "arithmetic_count": 324,
            "outside_count": 648, "index3_dichotomy": True,
            "digest": SEMANTIC_SHA}


def _is_digest(x: Any) -> bool:
    return (isinstance(x, str) and len(x) == 64 and
            all(c in "0123456789abcdef" for c in x))


def _matrix_json_ok(x: Any) -> bool:
    return (isinstance(x, list) and len(x) == N and
            all(isinstance(row, list) and len(row) == N and
                all(isinstance(v, int) and not isinstance(v, bool)
                    for v in row) for row in x))


def _serialized_tuple_ok(x: Any, q: int) -> bool:
    if not isinstance(x, dict) or set(x) != {"roof", "blocks"}:
        return False
    roof = x["roof"]
    blocks = x["blocks"]
    if (not isinstance(roof, list) or len(roof) != 36 or
            sorted(roof) != list(range(1, 37)) or
            not isinstance(blocks, list) or len(blocks) != 5):
        return False
    for m in blocks:
        if (not isinstance(m, list) or len(m) != N or
                any(not isinstance(row, list) or len(row) != N for row in m)):
            return False
        if any((not isinstance(v, int) or isinstance(v, bool) or
                not 0 <= v < q) for row in m for v in row):
            return False
    return True


def _calibration_fixture_rows(frozen_rows: list[list[Any]]) -> list[dict[str, Any]]:
    """Make structurally complete rows for validator-only negative tests."""
    one = serialize_tuple(tuple_identity(36, 5, 3))
    return [{
        "row_index": i,
        "target_key": row[1],
        "representative_word_digest": digest(row[2]),
        "common_word_in_hprime": True,
        "fiber_size": 8,
        "fiber_representative": one,
        "fiber_digest": "0" * 64,
        "identity_image_defect_count": 1,
        "nonidentity_image_defect_count": 7,
        "first_nonidentity_image_defect": [list(r) for r in eye()],
    } for i, row in enumerate(frozen_rows, 1)]


def _calibration_fixture(frozen_rows: list[list[Any]], q: int, a: int,
                         source_sha: str) -> dict[str, Any]:
    rows = _calibration_fixture_rows(frozen_rows)
    kernel_elements = []
    for i in range(CAL_KERNEL_ORDER):
        k = copy.deepcopy(serialize_tuple(tuple_identity(36, 5, q)))
        value = i
        for j in range(3):
            k["blocks"][0][j // N][j % N] = value % q
            value //= q
        kernel_elements.append(k)
    return {
        "schema": SCHEMA, "final_marker": FINAL,
        "status": "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS", "q": q, "a": a,
        "producer_source_sha256": source_sha,
        "words_sha256": WORDS_SHA, "artifact_rows_sha256": ARTIFACT_ROWS_SHA,
        "target_sha256": TARGET_SHA, "tuple_sha256": TUPLE_SHA,
        "semantic_premises": semantic(), "generator_order": list(GENERATOR_ORDER),
        "a18_pair_order": list(A18_NAMES), "roof_order": P_ORDER,
        "projection_image_order": PPRIME_ORDER, "h_order": CAL_H_ORDER,
        "hprime_order": CAL_HPRIME_ORDER, "kernel_order": CAL_KERNEL_ORDER,
        "quotient_h_over_hprime_order": 36, "row_count": 972,
        "algorithm": PRESENTATION_ALGORITHM,
        "presentation_evidence": {
            "seed": "[x,y]", "normal_closure_closed": True,
            "normal_closure_theorem": "F2' is the normal closure of [x,y]",
            "normal_closure_rounds": 1,
            "hprime_generator_count": 1,
            "projected_section_complete": True,
            "schreier_edge_count": PPRIME_ORDER * 2,
            "kernel_complete": True,
            "no_word_bound_or_random_sampling": True,
        },
        "common_word_provenance": COMMON_WORD_PROVENANCE,
        "e_f2prime_equals_hprime": True,
        "kernel_generators": [kernel_elements[1]],
        "kernel_elements": kernel_elements,
        "rows": rows,
    }


def calibration_ok(path: Path, q: int, a: int, expected_source_sha: str,
                   frozen_rows: list[list[Any]] | None = None) -> bool:
    """Authenticate an entire calibration receipt, not its aggregates."""
    if not path.is_file():
        return False
    try:
        r = json.loads(path.read_bytes())
        rows = r.get("rows")
        if frozen_rows is None:
            frozen_rows = load_words()
        if (r.get("schema") != SCHEMA or r.get("final_marker") != FINAL or
                r.get("status") != "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS" or
                r.get("q") != q or r.get("a") != a or
                r.get("producer_source_sha256") != expected_source_sha or
                r.get("words_sha256") != WORDS_SHA or
                r.get("artifact_rows_sha256") != ARTIFACT_ROWS_SHA or
                r.get("target_sha256") != TARGET_SHA or
                r.get("tuple_sha256") != TUPLE_SHA or
                r.get("semantic_premises") != semantic() or
                r.get("generator_order") != list(GENERATOR_ORDER) or
                r.get("a18_pair_order") != list(A18_NAMES) or
                r.get("roof_order") != P_ORDER or
                r.get("projection_image_order") != PPRIME_ORDER or
                r.get("h_order") != CAL_H_ORDER or
                r.get("hprime_order") != CAL_HPRIME_ORDER or
                r.get("kernel_order") != CAL_KERNEL_ORDER or
                r.get("quotient_h_over_hprime_order") != 36 or
                r.get("algorithm") != PRESENTATION_ALGORITHM or
                r.get("common_word_provenance") != COMMON_WORD_PROVENANCE or
                r.get("e_f2prime_equals_hprime") is not True or
                r.get("row_count") != 972 or
                not isinstance(rows, list) or len(rows) != 972 or
                len(frozen_rows) != 972):
            return False
        evidence = r.get("presentation_evidence")
        if not isinstance(evidence, dict):
            return False
        hpg = evidence.get("hprime_generator_count")
        if (evidence.get("seed") != "[x,y]" or
                evidence.get("normal_closure_closed") is not True or
                evidence.get("normal_closure_theorem") !=
                "F2' is the normal closure of [x,y]" or
                not isinstance(evidence.get("normal_closure_rounds"), int) or
                evidence["normal_closure_rounds"] < 1 or
                not isinstance(hpg, int) or hpg < 1 or
                evidence.get("projected_section_complete") is not True or
                evidence.get("schreier_edge_count") != PPRIME_ORDER * 2 * hpg or
                evidence.get("kernel_complete") is not True or
                evidence.get("no_word_bound_or_random_sampling") is not True):
            return False
        kernel_elements = r.get("kernel_elements")
        kernel_generators = r.get("kernel_generators")
        if (not isinstance(kernel_elements, list) or
                len(kernel_elements) != CAL_KERNEL_ORDER or
                len({digest(k) for k in kernel_elements}) != CAL_KERNEL_ORDER or
                not all(_serialized_tuple_ok(k, q) for k in kernel_elements) or
                not isinstance(kernel_generators, list) or
                len(kernel_generators) < 1 or
                not all(_serialized_tuple_ok(k, q) for k in kernel_generators)):
            return False
        seen_keys: set[str] = set()
        for i, (row, frozen) in enumerate(zip(rows, frozen_rows), 1):
            if (not isinstance(row, dict) or row.get("row_index") != i or
                    row.get("target_key") != frozen[1] or
                    row.get("representative_word_digest") != digest(frozen[2]) or
                    row.get("common_word_in_hprime") is not True or
                    row.get("fiber_size") != 8 or
                    row.get("identity_image_defect_count") != 1 or
                    row.get("nonidentity_image_defect_count") != 7 or
                    not _serialized_tuple_ok(row.get("fiber_representative"), q) or
                    not _is_digest(row.get("fiber_digest")) or
                    not _matrix_json_ok(row.get("first_nonidentity_image_defect"))):
                return False
            key_digest = digest(row["target_key"])
            if key_digest in seen_keys:
                return False
            seen_keys.add(key_digest)
        return len(seen_keys) == 972
    except (OSError, ValueError, TypeError, json.JSONDecodeError, KeyError):
        return False


def matrix_json(m: Matrix | None) -> Any:
    return None if m is None else [list(r) for r in m]


def run_full(q: int, a: int, output: Path, cal_q3: Path, cal_q4: Path) -> int:
    global TQ
    TQ = q
    rows = load_words()
    source_sha = producer_source_sha()
    calibration_bindings: dict[str, Any] | None = None
    if q == 5:
        cal3_sha = file_sha(cal_q3) if cal_q3.is_file() else None
        cal4_sha = file_sha(cal_q4) if cal_q4.is_file() else None
        cal3_ok = calibration_ok(cal_q3, 3, -1, source_sha, rows)
        cal4_ok = calibration_ok(cal_q4, 4, 2, source_sha, rows)
        if not (cal3_ok and cal4_ok):
            receipt = {"schema": SCHEMA, "final_marker": FINAL,
                       "status": "UNKNOWN_RESOURCE", "q": q, "a": a,
                       "producer_source_sha256": source_sha,
                       "diagnostics": ["q3/q4 calibration receipts required"]}
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
            print(f"{FINAL} status=UNKNOWN_RESOURCE output={output}")
            return 2
        calibration_bindings = {"q3_sha256": cal3_sha, "q4_sha256": cal4_sha}
    roof = build_roof()
    require(roof_orders(roof) == (P_ORDER, PPRIME_ORDER), "roof order drift")
    x, y = make_tuple_gens(q, a, roof)
    s = burau_generators(q, a)
    require(mmul(mmul(s[0], s[1], q), s[0], q) ==
            mmul(mmul(s[1], s[0], q), s[1], q), "s1/s2 braid drift")
    require(mmul(mmul(s[1], s[2], q), s[1], q) ==
            mmul(mmul(s[2], s[1], q), s[2], q), "s2/s3 braid drift")
    require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q), "commuting drift")
    sec, kernel, hpgens, rounds = complete_hprime(x, y, q, PPRIME_ORDER)
    kset = set(kernel)
    require(all(k[0] == ident(36) for k in kernel), "kernel roof drift")
    qreps = quotient_cosets(x, y, sec, kset, q)
    hprime_order = len(sec) * len(kernel)
    h_order = len(qreps) * hprime_order
    print(f"D972_B4_BURAU_V3_PROGRESS phase=schreier-complete projected={len(sec)} "
          f"kernel={len(kernel)} hprime={hprime_order} h={h_order}", flush=True)
    out_rows = []
    any_zero = False
    for i, (m, key, word) in enumerate(rows, 1):
        common = eval_word(word, (x, y))
        require(roof_key(word, roof, m) == key, f"roof replay drift row {i}")
        require(common[0] == roof_image_for_key(key), f"common roof drift row {i}")
        common_word_in_hprime = in_extension(common, sec, kset, q)
        require(common_word_in_hprime,
                f"common word outside exact H' row {i}")
        h0 = sec.get(common[0])
        require(h0 is not None, f"empty exact H' fiber row {i}")
        fiber = sorted((tmul(h0, k, q) for k in kernel), key=tuple_key)
        ids = 0
        first = None
        for h in fiber:
            d = matrix_defect(h[1], q)
            if d == eye():
                ids += 1
            elif first is None:
                first = d
        non = len(fiber) - ids
        if ids == 0:
            any_zero = True
        out_rows.append({
            "row_index": i, "target_key": key,
            "representative_word_digest": digest(word),
            "common_word_in_hprime": common_word_in_hprime,
            "fiber_size": len(fiber),
            "fiber_representative": serialize_tuple(h0),
            "fiber_digest": digest([serialize_tuple(z) for z in fiber]),
            "identity_image_defect_count": ids,
            "nonidentity_image_defect_count": non,
            "first_nonidentity_image_defect": matrix_json(first),
        })
        if i % 81 == 0:
            print(f"D972_B4_BURAU_V3_PROGRESS phase=rows completed={i}", flush=True)
    calibration_match = True
    if q in (3, 4):
        calibration_match = (h_order == CAL_H_ORDER and
                             hprime_order == CAL_HPRIME_ORDER and
                             len(kernel) == CAL_KERNEL_ORDER and
                             all(row["fiber_size"] == 8 and
                                 row["identity_image_defect_count"] == 1
                                 for row in out_rows))
    status = ("UNKNOWN_RESOURCE" if not calibration_match else
              ("CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER" if any_zero
               else "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS"))
    schreier_relators = kernel_from_section(hpgens, sec, q)
    kernel_generators = reduce_kernel_generators(schreier_relators, q, len(x[0]))
    receipt = {
        "schema": SCHEMA, "final_marker": FINAL, "status": status,
        "q": q, "a": a, "producer_source_sha256": source_sha,
        "words_sha256": WORDS_SHA, "row_count": 972,
        "artifact_rows_sha256": ARTIFACT_ROWS_SHA, "target_sha256": TARGET_SHA,
        "tuple_sha256": TUPLE_SHA, "semantic_premises": semantic(),
        "generator_order": list(GENERATOR_ORDER), "a18_pair_order": list(A18_NAMES),
        "roof_order": P_ORDER, "projection_image_order": len(sec),
        "h_order": h_order, "hprime_order": hprime_order,
        "kernel_order": len(kernel), "quotient_h_over_hprime_order": len(qreps),
        "algorithm": PRESENTATION_ALGORITHM,
        "presentation_evidence": {
            "seed": "[x,y]", "normal_closure_closed": True,
            "normal_closure_theorem": "F2' is the normal closure of [x,y]",
            "normal_closure_rounds": rounds,
            "hprime_generator_count": len(hpgens),
            "projected_section_complete": len(sec) == PPRIME_ORDER,
            "schreier_edge_count": len(sec) * 2 * len(hpgens),
            "kernel_complete": True,
            "no_word_bound_or_random_sampling": True,
        },
        "common_word_provenance": COMMON_WORD_PROVENANCE,
        "e_f2prime_equals_hprime": True,
        "kernel_generators": [serialize_tuple(k) for k in kernel_generators],
        "kernel_elements": [serialize_tuple(k) for k in kernel],
        "calibration_gate": {"required_for_q5": True,
                             "frozen_q3_q4_match": calibration_match,
                             "accepted_receipt_sha256": calibration_bindings},
        "rows": out_rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print(f"D972_B4_BURAU_V3_DONE q={q} a={a} h={h_order} "
          f"hprime={hprime_order} kernel={len(kernel)} rows=972")
    print(f"{FINAL} status={status} output={output}")
    return 0


def self_test() -> None:
    global TQ
    TQ = 5
    roof = build_roof()
    require(len(roof[0]) == 36 and roof_orders(roof) == (P_ORDER, PPRIME_ORDER),
            "roof selftest drift")
    rows = load_words()
    require(all(roof_key(r[2], roof, r[0]) == r[1] for r in rows[:12]),
            "lightweight roof replay drift")
    for q, a in ((3, -1), (4, 2), (5, 2), (5, 4)):
        TQ = q
        s = burau_generators(q, a)
        require(mmul(mmul(s[0], s[1], q), s[0], q) ==
                mmul(mmul(s[1], s[0], q), s[1], q), "braid selftest drift")
        require(mmul(mmul(s[1], s[2], q), s[1], q) ==
                mmul(mmul(s[2], s[1], q), s[2], q), "braid selftest drift")
        require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q), "commuting selftest drift")
        for m in s:
            require(mmul(m, minv(m, q), q) == eye(), "matrix inverse drift")
    source_sha = producer_source_sha()
    fixture = _calibration_fixture(rows, 3, -1, source_sha)

    class MemoryReceipt:
        def __init__(self, value: dict[str, Any]) -> None:
            self.value = value

        def is_file(self) -> bool:
            return True

        def read_bytes(self) -> bytes:
            return json.dumps(self.value).encode("utf-8")

    def check_fixture(value: dict[str, Any], label: str) -> None:
        require(not calibration_ok(MemoryReceipt(value), 3, -1,
                                   source_sha, rows),
                f"negative calibration fixture accepted: {label}")

    require(calibration_ok(MemoryReceipt(fixture), 3, -1, source_sha, rows),
            "complete calibration fixture rejected")
    bad = copy.deepcopy(fixture)
    bad["schema"] = "wrong-schema"
    check_fixture(bad, "schema")
    bad = copy.deepcopy(fixture)
    bad["producer_source_sha256"] = "0" * 64
    check_fixture(bad, "source hash")
    bad = copy.deepcopy(fixture)
    bad["rows"][1]["target_key"] = bad["rows"][0]["target_key"]
    check_fixture(bad, "duplicate key")
    bad = copy.deepcopy(fixture)
    del bad["presentation_evidence"]["kernel_complete"]
    check_fixture(bad, "incomplete evidence")
    bad = copy.deepcopy(fixture)
    bad["rows"][7]["row_index"] = 999
    check_fixture(bad, "wrong row index")
    bad = copy.deepcopy(fixture)
    bad["row_count"] = 971
    check_fixture(bad, "wrong row count")
    aggregate_only = {
        "status": fixture["status"], "q": 3, "a": -1,
        "h_order": CAL_H_ORDER, "hprime_order": CAL_HPRIME_ORDER,
        "kernel_order": CAL_KERNEL_ORDER,
        "projection_image_order": PPRIME_ORDER, "row_count": 972,
    }
    check_fixture(aggregate_only, "aggregate-only forged receipt")
    print("D972_B4_BURAU_V3_NEGATIVE_FIXTURES_PASS")
    TQ = 5
    print("D972_B4_BURAU_FIBER_V3_SELFTEST_PASS")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=5)
    ap.add_argument("--a", type=int, default=2)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--output", type=Path,
                    default=Path("ci/out/d972_b4_burau_fiber_v3.json"))
    ap.add_argument("--calibration-q3", type=Path,
                    default=Path("ci/out/d972_b4_burau_fiber_v3_q3.json"))
    ap.add_argument("--calibration-q4", type=Path,
                    default=Path("ci/out/d972_b4_burau_fiber_v3_q4.json"))
    ns = ap.parse_args(argv)
    try:
        if ns.self_test:
            self_test()
            return 0
        require((ns.q, ns.a) in ((3, -1), (4, 2), (5, 2), (5, 4)),
                "unsupported registered q/a")
        return run_full(ns.q, ns.a, ns.output, ns.calibration_q3, ns.calibration_q4)
    except (MemoryError, OSError) as exc:
        receipt = {"schema": SCHEMA, "final_marker": FINAL,
                   "status": "UNKNOWN_RESOURCE", "q": ns.q, "a": ns.a,
                   "diagnostics": [f"resource stop: {type(exc).__name__}"]}
        ns.output.parent.mkdir(parents=True, exist_ok=True)
        ns.output.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
        print(f"{FINAL} status=UNKNOWN_RESOURCE output={ns.output}")
        return 2
    except Exception as exc:
        print(f"D972_B4_BURAU_V3_ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
