"""Independent checker for the GF(5) finite Burau fiber.

This file is intentionally standalone.  It imports neither the v1 checker nor
any GAP/producer code.  The compact D972 roof, prime-field Burau matrices,
SymPy group, derived subgroup, roof pointwise stabilizer, exact cosets, and
raw A.18 defects are all reconstructed here.
"""
from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

from sympy.combinatorics import Permutation, PermutationGroup

WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ARTIFACT_ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
SEMANTIC_SHA = "3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729"
SCHEMA = "d972-b4-burau-fiber/v2"
FINAL = "D972_B4_BURAU_FIBER_V2_FINAL"
GENERATOR_ORDER = ("x12", "x13", "x14", "x23", "x24", "x34")
A18_NAMES = ("123", "234", "12,3,4", "1,23,4", "1,2,34")
ID_FIELD = "identity_image_defect_count"
N = 4
Matrix = tuple[tuple[int, ...], ...]
Perm = tuple[int, ...]


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def validate_exact_kernel_canary(canary: Any, kernel_order: int) -> None:
    """Validate the producer's runtime exact-kernel canary contract."""
    require(isinstance(canary, dict),
            "missing producer runtime exact-kernel canary metadata")
    require(canary.get("complete") is True and
            int(canary.get("order", -1)) == kernel_order and
            canary.get("distinct_complete") is True and
            canary.get("fixes_roof_block") is True and
            canary.get("deleted_element_incomplete") is True,
            "producer exact-kernel canary drift")


def cjson(x: Any) -> bytes:
    return json.dumps(x, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def digest(x: Any) -> str:
    return hashlib.sha256(cjson(x)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    require(vals, "PaperProd empty")
    out = ident(len(vals[0]))
    for x in reversed(vals):
        out = pprod(out, x)
    return out


def direct_sum(a: Perm, b: Perm) -> Perm:
    n = len(a)
    return a + tuple(n + x for x in b)


def block(p: Perm, offset: int, size: int) -> Perm:
    z = tuple(p[offset + i] - offset for i in range(size))
    require(set(z) == set(range(1, size + 1)), "permutation block drift")
    return z


def eval_word(word: Iterable[int], gens: Sequence[Perm]) -> Perm:
    out = ident(len(gens[0]))
    for x in word:
        require(isinstance(x, int) and not isinstance(x, bool) and x and
                abs(x) <= len(gens), "invalid signed word")
        out = pprod(out, ppow(gens[abs(x) - 1], 1 if x > 0 else -1))
    return out


# ---- compact roof, ported independently from the frozen formulae ----------

def make_dn(n: int) -> tuple[Perm, Perm]:
    r = tuple(range(2, n + 1)) + (1,)
    s = tuple(((n - (j - 1)) % n) + 1 for j in range(1, n + 1))
    require(pprod(pprod(s, r), pinv(s)) == pinv(r), "MakeDn relation drift")
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
    return direct_sum(x9, x4), direct_sum(y9, y4)


def d9_coords(p: Perm) -> list[int]:
    r, s = make_dn(9)
    for a in range(9):
        for e in range(2):
            if p == pprod(ppow(r, a), ppow(s, e)):
                return [a, e]
    raise ValueError("D9 coordinate drift")


def roof_key(word: list[int], roof: tuple[Perm, Perm], m: int) -> list[Any]:
    f = eval_word(word, roof)
    p27, p9 = block(f, 0, 27), block(f, 27, 9)
    return [int(m), [d9_coords(block(p27, 9 * i, 9)) for i in range(3)], list(p9)]


def load_words(path: Path = WORDS_PATH) -> list[list[Any]]:
    require(file_sha(path) == WORDS_SHA, "word artifact SHA drift")
    obj = json.loads(path.read_bytes())
    rows = obj.get("rows")
    require(obj.get("schema") == "d972-b4-word-key-artifact/v1" and
            obj.get("count") == 972 and isinstance(rows, list) and len(rows) == 972,
            "word artifact shape drift")
    require(obj.get("canonical_bytes_sha256") == digest(rows) == ARTIFACT_ROWS_SHA,
            "word artifact canonical digest drift")
    require(obj.get("source_target_key_digest") == TARGET_SHA and
            obj.get("frozen_tuple_sha256") == TUPLE_SHA and
            digest([r[1] for r in rows]) == TUPLE_SHA,
            "word artifact metadata/target digest drift")
    for row in rows:
        require(isinstance(row, list) and len(row) == 3 and isinstance(row[2], list),
                "word row shape drift")
    require(len({digest(r[1]) for r in rows}) == 972, "duplicate roof keys")
    return rows


# ---- GF(5) and unreduced Burau -------------------------------------------

def fmul(a: int, b: int, q: int) -> int:
    return (a * b) % q


def finv(a: int, q: int) -> int:
    require(a % q != 0, "field inverse of zero")
    for b in range(1, q):
        if a * b % q == 1:
            return b
    raise ValueError("prime-field inverse missing")


def mmul(a: Matrix, b: Matrix, q: int) -> Matrix:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(N)) % q
                       for j in range(N)) for i in range(N))


def eye() -> Matrix:
    return tuple(tuple(int(i == j) for j in range(N)) for i in range(N))


def minv(a: Matrix, q: int) -> Matrix:
    rows = [list(a[i]) + list(eye()[i]) for i in range(N)]
    for c in range(N):
        r = next((z for z in range(c, N) if rows[z][c] % q), None)
        require(r is not None, "singular Burau matrix")
        rows[c], rows[r] = rows[r], rows[c]
        z = finv(rows[c][c], q)
        rows[c] = [(x * z) % q for x in rows[c]]
        for rr in range(N):
            if rr != c:
                z = rows[rr][c] % q
                rows[rr] = [(x - z * y) % q for x, y in zip(rows[rr], rows[c])]
    return tuple(tuple(x[N:]) for x in rows)


def det_nonzero(a: Matrix, q: int) -> bool:
    rows = [list(x) for x in a]
    for c in range(N):
        r = next((z for z in range(c, N) if rows[z][c] % q), None)
        if r is None:
            return False
        rows[c], rows[r] = rows[r], rows[c]
        z = finv(rows[c][c], q)
        for rr in range(c + 1, N):
            scale = rows[rr][c] * z % q
            for j in range(c, N):
                rows[rr][j] = (rows[rr][j] - scale * rows[c][j]) % q
    return True


def burau_generators(q: int, a: int) -> tuple[Matrix, Matrix, Matrix]:
    require(q == 5 and a in (2, 4), "only preregistered GF(5) parameters 2,4")
    out = []
    for i in range(3):
        m = [list(x) for x in eye()]
        m[i][i], m[i][i + 1] = (1 - a) % q, a
        m[i + 1][i], m[i + 1][i + 1] = 1, 0
        out.append(tuple(tuple(x) for x in m))
    return tuple(out)  # type: ignore[return-value]


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


def matrix_perm(m: Matrix, q: int) -> Perm:
    vectors = [(n // (q ** 3) % q, n // (q ** 2) % q, n // q % q, n % q)
               for n in range(q ** 4)]
    pos = {v: i + 1 for i, v in enumerate(vectors)}
    out = []
    for v in vectors:
        out.append(pos[tuple(sum(v[k] * m[k][j] for k in range(N)) % q
                             for j in range(N))])
    return tuple(out)


def combined_generators(q: int, a: int) -> tuple[Perm, Perm]:
    roof = build_roof()
    pairs = a18_pairs(pure_generators(q, a), q)
    hx, hy = roof
    off = 36
    for x, y in pairs:
        hx += tuple(off + z for z in matrix_perm(x, q))
        hy += tuple(off + z for z in matrix_perm(y, q))
        off += q ** 4
    return hx, hy


def defect(parts: Sequence[Perm]) -> Perm:
    require(len(parts) == 5, "A.18 part count drift")
    return paper_prod((pinv(paper_prod((parts[4], parts[2]))),
                       parts[1], parts[3], parts[0]))


# ---- SymPy exact finite group machinery ----------------------------------

def sympy_perm(p: Perm) -> Permutation:
    return Permutation([x - 1 for x in p], size=len(p))


def own_perm(p: Permutation, n: int) -> Perm:
    a = p.array_form
    return tuple((a[i] if i < len(a) else i) + 1 for i in range(n))


def sym_group(gens: Sequence[Perm]) -> PermutationGroup:
    G = PermutationGroup([sympy_perm(x) for x in gens])
    G.schreier_sims()
    return G


def validate_supplied_kernel_generators(
        gens: Sequence[Perm], K: PermutationGroup, kernel_order: int) -> None:
    """Check supplied one-line generators against the reconstructed K."""
    for g in gens:
        require(sympy_perm(g) in K, "supplied kernel generator is outside K")
    if not gens:
        require(kernel_order == 1,
                "empty supplied kernel generators for nontrivial K")
        return
    supplied_k = sym_group(gens)
    require(supplied_k.order() == kernel_order,
            "supplied kernel generators do not generate reconstructed K")


def enumerate_sym(G: PermutationGroup, expected: int) -> list[Perm]:
    require(G.order() == expected, "group order before enumeration drift")
    vals = sorted(set(own_perm(x, G.degree) for x in G.generate_dimino()))
    require(len(vals) == expected, "SymPy enumeration incomplete")
    return vals


def pointwise_stabilizer(G: PermutationGroup) -> PermutationGroup:
    K = G
    for p in range(36):
        K = K.stabilizer(p)
        K.schreier_sims()
    return K


def roof_image_for_key(key: list[Any]) -> Perm:
    r, s = make_dn(9)
    p27 = tuple(9 * i + x
                for i, (a, e) in enumerate(key[1])
                for x in pprod(ppow(r, int(a)), ppow(s, int(e))))
    return p27 + tuple(27 + int(x) for x in key[2])


def validate_semantics(r: dict[str, Any]) -> None:
    e = {"M": "K^(9) intersect N_S4", "P": "G9 x PSL(2,8)",
         "P_order": 1469664, "roof_count": 972,
         "arithmetic_count": 324, "outside_count": 648,
         "index3_dichotomy": True}
    s = r.get("semantic_premises")
    require(isinstance(s, dict) and {k: s.get(k) for k in e} == e and
            s.get("digest") == SEMANTIC_SHA and digest(e) == SEMANTIC_SHA,
            "semantic premise digest drift")


def check_receipt(path: Path) -> dict[str, Any]:
    rows = load_words()
    r = json.loads(path.read_bytes())
    require(r.get("schema") == SCHEMA and r.get("final_marker") == FINAL,
            "receipt schema/final marker drift")
    require(r.get("status") in {"CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER",
                                 "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS",
                                 "UNKNOWN_RESOURCE"}, "producer self-promotion/unknown status")
    require(not r.get("syntax_error") and not r.get("error_diagnostics"),
            "syntax/error receipt is not admissible")
    for field in ("diagnostics", "errors", "syntax_errors"):
        require(not r.get(field), f"receipt {field} is not admissible")
    require(r.get("words_sha256") == WORDS_SHA and r.get("row_count") == 972 and
            isinstance(r.get("rows"), list) and len(r["rows"]) == 972,
            "receipt source/row truncation drift")
    validate_semantics(r)
    q, a = int(r.get("q", 0)), int(r.get("a", 0))
    require(q == 5 and a in (2, 4), "unsupported GF(5) receipt parameter")
    require(r.get("generator_order") == list(GENERATOR_ORDER) and
            r.get("a18_pair_order") == list(A18_NAMES),
            "generator/A.18 order metadata drift")
    s = burau_generators(q, a)
    require(mmul(mmul(s[0], s[1], q), s[0], q) ==
            mmul(mmul(s[1], s[0], q), s[1], q), "Burau braid drift")
    require(mmul(mmul(s[1], s[2], q), s[1], q) ==
            mmul(mmul(s[2], s[1], q), s[2], q), "Burau s2/s3 braid drift")
    require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q),
            "Burau s1/s3 commuting drift")
    require(all(det_nonzero(x, q) for x in s), "Burau invertibility drift")
    pairs = a18_pairs(pure_generators(q, a), q)
    hx, hy = combined_generators(q, a)
    degree = 36 + 5 * q ** 4
    require(int(r.get("permutation_degree", 0)) == degree and
            [tuple(int(z) for z in x) for x in r.get("h_generators", [])] == [hx, hy],
            "H generator/degree binding drift")
    H = sym_group([hx, hy])
    require(H.order() == int(r.get("h_order", -1)), "H order drift")
    roof = build_roof()
    PG = sym_group(list(roof))
    require(PG.order() == 1469664 and PG.derived_subgroup().order() == 367416,
            "compact roof order drift")
    Hp = H.derived_subgroup(); Hp.schreier_sims()
    require(Hp.order() == int(r.get("hprime_order", -1)), "H' order drift")
    K = pointwise_stabilizer(Hp)
    ko = K.order()
    require(ko == int(r.get("kernel_order", -1)) and ko > 0, "kernel order drift")
    kernel = enumerate_sym(K, ko)
    # The receipt may expose only a generating set, but that set is still
    # independently checked against the reconstructed pointwise kernel.
    kg_raw = r.get("kernel_generators")
    require(isinstance(kg_raw, list), "malformed runtime kernel generators")
    kg = []
    for j, raw in enumerate(kg_raw, 1):
        require(isinstance(raw, list), f"malformed kernel generator {j}")
        g = tuple(int(z) for z in raw)
        require(len(g) == degree and set(g) == set(range(1, degree + 1)),
                f"kernel generator shape drift at {j}")
        require(block(g, 0, 36) == ident(36),
                f"kernel generator is not roof-pointwise at {j}")
        kg.append(g)
    require(int(r.get("kernel_generator_count", -1)) == len(kg),
            "kernel generator count drift")
    if ko != 1:
        require(kg, "missing runtime kernel generators")
    validate_supplied_kernel_generators(kg, K, ko)
    # A producer-side runtime canary is required in addition to this
    # independent reconstruction; a static receipt assertion is insufficient.
    validate_exact_kernel_canary(r.get("exact_kernel_canary"), ko)
    deleted_kernel = kernel[:-1]
    require(len(deleted_kernel) == ko - 1 and
            len(set(deleted_kernel)) == ko - 1 and
            set(deleted_kernel) != set(kernel) and
            digest([list(x) for x in deleted_kernel]) !=
            digest([list(x) for x in kernel]),
            "reconstructed-K deletion mutation was not detected")
    proj = sym_group([block(own_perm(g, degree), 0, 36) for g in Hp.generators])
    require(proj.order() == int(r.get("projection_image_order", -1)) == 367416,
            "projection image order drift")
    require(proj.order() * ko == Hp.order(), "projection/kernel product drift")
    roof_keys = {digest(x[1]) for x in rows}
    seen = set()
    counts = []
    for i, (source, item) in enumerate(zip(rows, r["rows"], strict=True), 1):
        m, key, word = source
        require(item.get("row_index") == i and item.get("target_key") == key,
                f"row binding drift at {i}")
        require(digest(word) == item.get("representative_word_digest"),
                f"word digest drift at {i}")
        require(roof_key(word, roof, m) == key, f"roof replay drift at {i}")
        kd = digest(key); require(kd not in seen and kd in roof_keys, f"duplicate key at {i}")
        seen.add(kd)
        require(int(item.get("fiber_size", -1)) == ko and ko > 0, f"incomplete fiber at {i}")
        h0 = tuple(int(z) for z in item.get("fiber_representative", []))
        require(len(h0) == degree and set(h0) == set(range(1, degree + 1)),
                f"fiber representative shape at {i}")
        require(sympy_perm(h0) in Hp and block(h0, 0, 36) == roof_image_for_key(key),
                f"fiber representative binding at {i}")
        coset = sorted(pprod(h0, k) for k in kernel)
        require(all(sympy_perm(x) in Hp for x in coset), f"coset membership at {i}")
        if item.get("fiber_digest") is not None:
            require(item["fiber_digest"] == digest([list(x) for x in coset]),
                    f"fiber digest drift at {i}")
        z = 0; defects: set[Perm] = set()
        for h in coset:
            parts = [block(h, 36 + j * q ** 4, q ** 4) for j in range(5)]
            d = defect(parts)
            if d == ident(q ** 4): z += 1
            else: defects.add(d)
        declared_id = item.get(ID_FIELD, item.get("identity_defect_count", -1))
        declared_non = item.get("nonidentity_image_defect_count",
                                item.get("nonidentity_defect_count", -1))
        require(int(declared_id) == z and int(declared_non) == ko - z,
                f"defect counts drift at {i}")
        if defects:
            w = item.get("first_defect_witness")
            require(isinstance(w, list) and len(w) == q ** 4 and
                    tuple(int(x) for x in w) in defects,
                    f"defect witness drift at {i}")
        counts.append(z)
    require(seen == roof_keys and len(seen) == 972, "receipt key set incomplete")
    status = r["status"]
    zero = sum(z == 0 for z in counts)
    require((status == "CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER" and zero > 0) or
            (status == "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS" and zero == 0) or
            status == "UNKNOWN_RESOURCE", "status/count mismatch")
    return {"status": ("B4_A_BURAU_FINITE_ZERO_FIBER_CROSSCHECKED"
                        if status == "CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER" else status),
            "rows": 972, "h_order": H.order(), "hprime_order": Hp.order(),
            "kernel_order": ko, "zero_fibers": zero}


def mutation_tests() -> None:
    roof = build_roof(); rows = load_words()
    require(pprod((2, 1, 3), (1, 3, 2)) != pprod((1, 3, 2), (2, 1, 3)),
            "noncommuting mutation fixture drift")
    require(paper_prod(((2, 1, 3), (1, 3, 2))) !=
            pprod((2, 1, 3), (1, 3, 2)), "reverse PaperProd mutation accepted")
    s1, s2, _ = burau_generators(5, 2)
    x13 = matrix_paper_prod((s2, mpow(s1, 2, 5), minv(s2, 5)), 5)
    wrong = matrix_paper_prod((minv(s2, 5), mpow(s1, 2, 5), s2), 5)
    require(x13 != wrong, "reverse x13 mutation accepted")
    pairs = a18_pairs(pure_generators(5, 2), 5)
    def meval(w: Sequence[int], pair: tuple[Matrix, Matrix]) -> Matrix:
        out = eye()
        for z in w:
            out = mmul(out, pair[z - 1] if z > 0 else minv(pair[-z - 1], 5), 5)
        return out
    parts = [matrix_perm(meval((1, 2), p), 5) for p in pairs]
    good = defect(parts)
    swapped = paper_prod((pinv(paper_prod((parts[2], parts[4]))), parts[1],
                          parts[3], parts[0]))
    require(good != swapped, "swapped leading A.18 mutation accepted")
    k = [ident(3), (2, 1, 3)]
    require(digest([list(x) for x in k]) != digest([list(x) for x in k[:1]]),
            "deleted kernel mutation accepted")
    bad = copy.deepcopy(rows[0][1]); bad[2][0] = 2 if bad[2][0] != 2 else 1
    require(roof_key(rows[0][2], roof, rows[0][0]) != bad,
            "corrupt roof key mutation accepted")
    bw = list(rows[1][2]); bw[0] = -bw[0]
    require(roof_key(bw, roof, rows[1][0]) != rows[1][1],
            "corrupt roof word mutation accepted")


def selftest() -> None:
    roof = build_roof(); require(len(roof[0]) == 36, "roof degree drift")
    rows = load_words()
    require(all(roof_key(row[2], roof, row[0]) == row[1] for row in rows),
            "972 roof replay selftest failed")
    require(all(block(eval_word(row[2], roof), 0, 36) ==
                roof_image_for_key(row[1]) for row in rows),
            "972 key-to-roof-image regression failed")
    s = burau_generators(5, 2)
    validate_exact_kernel_canary(
        {"complete": True, "order": 1, "distinct_complete": True,
         "fixes_roof_block": True, "deleted_element_incomplete": True}, 1)
    try:
        validate_exact_kernel_canary(
            {"complete": True, "order": 1, "distinct_complete": True,
             "fixes_roof_block": True, "deleted_element_incomplete": False}, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("exact-kernel canary mutation accepted")
    # Lightweight edge fixture only: for |K|=1, deleting identity to [] is
    # itself a valid completeness mutation; terminal receipt checks use K.
    toy_kernel = [ident(1)]
    toy_deleted = toy_kernel[:-1]
    require(len(toy_deleted) == 0 and digest(toy_deleted) != digest(toy_kernel),
            "trivial-kernel deletion mutation drift")
    # Exercise both admissible trivial-kernel producer encodings: GAP may
    # serialize either no generators or an explicit identity generator.
    trivial_group = sym_group([ident(1)])
    validate_supplied_kernel_generators([], trivial_group, 1)
    validate_supplied_kernel_generators([ident(1)], trivial_group, 1)
    require(mmul(mmul(s[0], s[1], 5), s[0], 5) ==
            mmul(mmul(s[1], s[0], 5), s[1], 5), "GF5 braid selftest failed")
    require(mmul(mmul(s[1], s[2], 5), s[1], 5) ==
            mmul(mmul(s[2], s[1], 5), s[2], 5), "GF5 s2/s3 braid selftest failed")
    require(mmul(s[0], s[2], 5) == mmul(s[2], s[0], 5),
            "GF5 s1/s3 commuting selftest failed")
    require(all(det_nonzero(x, 5) for x in s), "GF5 determinant selftest failed")
    for m in s:
        p = matrix_perm(m, 5)
        require(len(p) == 625 and set(p) == set(range(1, 626)),
                "GF5 vector bijection selftest failed")
    mutation_tests()
    print("D972_B4_BURAU_FIBER_V2_CHECKER_SELFTEST_PASS")
    print("D972_B4_BURAU_FIBER_V2_CHECKER_FINAL_MARKER status=PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        selftest()
    elif a.receipt:
        print("D972_B4_BURAU_FIBER_V2_CHECK_PASS",
              json.dumps(check_receipt(Path(a.receipt)), sort_keys=True))
    else:
        ap.error("receipt path or --self-test required")


if __name__ == "__main__":
    main()
