"""Independent checker for D972's matrix-56 Burau receipts.

This is deliberately self contained: the GAP producer and every producer
helper are treated as untrusted input.  The compact roof, field arithmetic,
Burau/A.18 matrices, word artifact, matrix-to-vector action, and exact finite
permutation groups are reconstructed here.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

from sympy.combinatorics import Permutation, PermutationGroup

WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
PRODUCER_PATH = Path("search/d972_b4_burau_matrix_v1.g")
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ARTIFACT_ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
SEMANTIC_SHA = "3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729"
SCHEMA = "d972-b4-burau-matrix56/v1"
FINAL = "D972_B4_BURAU_MATRIX56_FINAL"
GENERATOR_ORDER = ("x12", "x13", "x14", "x23", "x24", "x34")
A18_ORDER = ("123", "234", "12,3,4", "1,23,4", "1,2,34")
CAL_QA = {(3, -1), (4, 2)}
CAL_H = 105815808
CAL_HP = 2939328
CAL_K = 8
ALGORITHM_KEYS = (
    "faithful_full_roof_module", "matrix_group_h_exact",
    "derived_subgroup_exact", "normal_closure_equals_hprime",
    "projection_surjective_to_pprime", "kernel_exact",
    "kernel_elements_complete", "signed_word_replay",
    "all_common_words_in_hprime", "no_word_bound_or_sampling",
)
Perm = tuple[int, ...]
Matrix = tuple[tuple[int, ...], ...]


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


def block(p: Perm, offset: int, size: int) -> Perm:
    z = tuple(p[offset + i] - offset for i in range(size))
    require(set(z) == set(range(1, size + 1)), "permutation block drift")
    return z


def direct_sum(a: Perm, b: Perm) -> Perm:
    n = len(a)
    return a + tuple(n + x for x in b)


def eval_word(word: Iterable[int], gens: Sequence[Perm]) -> Perm:
    out = ident(len(gens[0]))
    for x in word:
        require(isinstance(x, int) and not isinstance(x, bool) and x and
                abs(x) <= len(gens), "invalid signed word")
        out = pprod(out, ppow(gens[abs(x) - 1], 1 if x > 0 else -1))
    return out


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
    require(len({digest(r[1]) for r in rows}) == 972, "duplicate roof keys")
    for row in rows:
        require(isinstance(row, list) and len(row) == 3 and isinstance(row[2], list),
                "word row shape drift")
    return rows


# ---- independent finite-field matrix implementation ----------------------
def fadd(a: int, b: int, q: int) -> int:
    return (a ^ b) if q == 4 else (a + b) % q


def fneg(a: int, q: int) -> int:
    return a if q == 4 else (-a) % q


def fmul(a: int, b: int, q: int) -> int:
    if q != 4:
        return a * b % q
    z = 0
    aa, bb = a, b
    while bb:
        if bb & 1:
            z ^= aa
        bb >>= 1
        aa <<= 1
        if aa & 4:
            aa ^= 0b111
    return z & 3


def finv(a: int, q: int) -> int:
    require(a % q != 0 if q != 4 else a != 0, "field inverse of zero")
    for b in range(1, q):
        if fmul(a, b, q) == 1:
            return b
    raise ValueError("finite-field inverse missing")


def fsub(a: int, b: int, q: int) -> int:
    return fadd(a, fneg(b, q), q)


def eye(n: int = 4) -> Matrix:
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def mmul(a: Matrix, b: Matrix, q: int) -> Matrix:
    n = len(a)
    return tuple(tuple(sum_field((fmul(a[i][k], b[k][j], q) for k in range(n)), q)
                       for j in range(n)) for i in range(n))


def sum_field(xs: Iterable[int], q: int) -> int:
    out = 0
    for x in xs:
        out = fadd(out, x, q)
    return out


def minv(a: Matrix, q: int) -> Matrix:
    n = len(a)
    rows = [list(a[i]) + list(eye(n)) for i in range(n)]
    for c in range(n):
        r = next((z for z in range(c, n)
                  if rows[z][c] != 0), None)
        require(r is not None, "singular finite-field matrix")
        rows[c], rows[r] = rows[r], rows[c]
        z = finv(rows[c][c], q)
        rows[c] = [fmul(x, z, q) for x in rows[c]]
        for rr in range(n):
            if rr != c:
                z = rows[rr][c]
                rows[rr] = [fsub(x, fmul(z, y, q), q)
                            for x, y in zip(rows[rr], rows[c])]
    return tuple(tuple(x[n:]) for x in rows)


def burau_generators(q: int, a: int) -> tuple[Matrix, Matrix, Matrix]:
    require((q, a) in {(3, -1), (4, 2), (5, 2), (5, 4)},
            "unsupported registered (q,a)")
    t = a % q if q != 4 else a
    out = []
    for i in range(3):
        m = [list(x) for x in eye()]
        m[i][i], m[i][i + 1] = fsub(1, t, q), t
        m[i + 1][i], m[i + 1][i + 1] = 1, 0
        out.append(tuple(tuple(x) for x in m))
    return tuple(out)  # type: ignore[return-value]


def mpow(a: Matrix, n: int, q: int) -> Matrix:
    out = eye(len(a))
    while n:
        if n & 1:
            out = mmul(out, a, q)
        a = mmul(a, a, q)
        n >>= 1
    return out


def matrix_paper_prod(xs: Iterable[Matrix], q: int) -> Matrix:
    vals = list(xs)
    require(vals, "PaperProd empty")
    out = eye(len(vals[0]))
    for x in reversed(vals):
        out = mmul(out, x, q)
    return out


def pure_generators(q: int, a: int) -> tuple[Matrix, ...]:
    s1, s2, s3 = burau_generators(q, a)
    p1, p4, p6 = mpow(s1, 2, q), mpow(s2, 2, q), mpow(s3, 2, q)
    return (p1, matrix_paper_prod((s2, p1, minv(s2, q)), q),
            matrix_paper_prod((s3, s2, p1, minv(s2, q), minv(s3, q)), q),
            p4, matrix_paper_prod((s3, p4, minv(s3, q)), q), p6)


def a18_pairs(pure: tuple[Matrix, ...], q: int) -> tuple[tuple[Matrix, Matrix], ...]:
    x12, x13, x14, x23, x24, x34 = pure
    return ((x12, x23), (x23, x34),
            (matrix_paper_prod((x13, x23), q), x34),
            (matrix_paper_prod((x12, x13), q),
             matrix_paper_prod((x24, x34), q)),
            (x12, matrix_paper_prod((x23, x24), q)))


def vectors(q: int) -> list[tuple[int, ...]]:
    return [tuple((n // (q ** (3 - i))) % q for i in range(4))
            for n in range(q ** 4)]


def matrix_perm(m: Matrix, q: int) -> Perm:
    vs = vectors(q)
    pos = {v: i + 1 for i, v in enumerate(vs)}
    out = []
    for v in vs:
        w = tuple(sum_field((fmul(v[k], m[k][j], q) for k in range(4)), q)
                  for j in range(4))
        out.append(pos[w])
    require(set(out) == set(range(1, q ** 4 + 1)), "matrix action not bijective")
    return tuple(out)


def perm_to_matrix(p: Perm, q: int) -> Matrix:
    vs = vectors(q)
    require(len(p) == q ** 4 and p[0] == 1, "nonlinear vector action")
    rows = []
    for i in range(4):
        image = vs[p[1 << (3 - i)] - 1]
        rows.append(image)
    m = tuple(tuple(x) for x in rows)
    require(matrix_perm(m, q) == p, "vector action is not linear")
    return m


def perm_matrix(p: Perm, q: int) -> Matrix:
    out = [[0] * len(p) for _ in p]
    for i, j in enumerate(p):
        out[i][j - 1] = 1
    return tuple(tuple(x) for x in out)


def expected_blocks(q: int, a: int) -> tuple[tuple[Matrix, ...], tuple[Matrix, ...]]:
    s = burau_generators(q, a)
    pairs = a18_pairs(pure_generators(q, a), q)
    return tuple(x[0] for x in pairs), tuple(x[1] for x in pairs)


def expected_generators(q: int, a: int) -> tuple[Perm, Perm]:
    roof = build_roof()
    bx, by = expected_blocks(q, a)
    hx, hy = roof[0], roof[1]
    for x, y in zip(bx, by):
        hx += tuple(36 + z for z in matrix_perm(x, q))
        hy += tuple(36 + z for z in matrix_perm(y, q))
    return hx, hy


def decode_matrix(raw: Any, q: int) -> tuple[Matrix, tuple[Matrix, ...], Perm]:
    require(isinstance(raw, list) and len(raw) == 56 and
            all(isinstance(r, list) and len(r) == 56 for r in raw),
            "matrix-56 shape drift")
    require(all(isinstance(x, int) and 0 <= x < q for r in raw for x in r),
            "field encoding drift")
    m = tuple(tuple(x) for x in raw)
    roof = m[:36]
    for i in range(36):
        require(sum(roof[i][j] == 1 for j in range(36)) == 1 and
                all(roof[i][j] == 0 for j in range(36) if roof[i][j] != 1),
                "roof block is not a permutation matrix")
    rp = tuple(next(j + 1 for j in range(36) if roof[i][j] == 1)
               for i in range(36))
    require(set(rp) == set(range(1, 37)), "roof columns are not unique")
    for i in range(36):
        require(all(m[i][j] == 0 for j in range(36, 56)), "off-block roof drift")
    blocks: list[Matrix] = []
    for b in range(5):
        off = 36 + 4 * b
        blocks.append(tuple(tuple(m[off + i][off + j] for j in range(4))
                            for i in range(4)))
        require(all(all(m[off + i][j] == 0 for j in range(56)
                        if not (off <= j < off + 4)) for i in range(4)),
                "off-block Burau drift")
        minv(blocks[-1], q)
    vec: Perm = rp
    off = 36
    for b in blocks:
        vec += tuple(off + z for z in matrix_perm(b, q))
        off += q ** 4
    return m, tuple(blocks), vec


def roof_image_for_key(key: list[Any]) -> Perm:
    r, s = make_dn(9)
    p27 = tuple(9 * i + x
                for i, (a, e) in enumerate(key[1])
                for x in pprod(ppow(r, int(a)), ppow(s, int(e))))
    return p27 + tuple(27 + int(x) for x in key[2])


def sympy_perm(p: Perm) -> Permutation:
    return Permutation([x - 1 for x in p], size=len(p))


def own_perm(p: Permutation, n: int) -> Perm:
    a = p.array_form
    return tuple((a[i] if i < len(a) else i) + 1 for i in range(n))


def sym_group(gens: Sequence[Perm]) -> PermutationGroup:
    g = PermutationGroup([sympy_perm(x) for x in gens])
    g.schreier_sims()
    return g


def pointwise_stabilizer(g: PermutationGroup) -> PermutationGroup:
    k = g
    for p in range(36):
        k = k.stabilizer(p)
        k.schreier_sims()
    return k


def enumerate_sym(g: PermutationGroup, expected: int) -> list[Perm]:
    require(g.order() == expected, "group order before enumeration drift")
    vals = sorted(set(own_perm(x, g.degree) for x in g.generate_dimino()))
    require(len(vals) == expected, "exact group enumeration incomplete")
    return vals


def validate_semantics(r: dict[str, Any]) -> None:
    e = {"M": "K^(9) intersect N_S4", "P": "G9 x PSL(2,8)",
         "P_order": 1469664, "roof_count": 972,
         "arithmetic_count": 324, "outside_count": 648,
         "index3_dichotomy": True}
    s = r.get("semantic_premises")
    require(isinstance(s, dict) and {k: s.get(k) for k in e} == e and
            s.get("digest") == SEMANTIC_SHA and digest(e) == SEMANTIC_SHA,
            "semantic premise digest drift")


def require_schema_contract(r: dict[str, Any]) -> None:
    required = {
        "algorithm_evidence", "generator_order", "a18_pair_order",
        "kernel_generator_count", "exact_kernel_canary",
        "source_target_key_digest", "producer_source_sha256",
    }
    missing = sorted(k for k in required if k not in r)
    if missing:
        raise ValueError("BLOCKER_SCHEMA_MISSING: " + ", ".join(missing))
    require(r["generator_order"] == list(GENERATOR_ORDER),
            "generator ordering drift")
    require(r["a18_pair_order"] == list(A18_ORDER), "A.18 ordering drift")
    require("permutation_degree" not in r,
            "permutation-degree substitution is not admissible")
    require(isinstance(r["algorithm_evidence"], dict),
            "algorithm evidence is not structured")
    ae = r["algorithm_evidence"]
    require(set(ae) == set(ALGORITHM_KEYS),
            "algorithm evidence key contract drift")
    for key in ALGORITHM_KEYS:
        require(ae.get(key) is True, f"algorithm evidence missing: {key}")
    require(r["source_target_key_digest"] == TARGET_SHA,
            "source target digest drift")
    require(r["producer_source_sha256"] == file_sha(PRODUCER_PATH),
            "producer source SHA drift")


def validate_canary(c: Any, order: int) -> None:
    require(isinstance(c, dict) and c.get("complete") is True and
            int(c.get("order", -1)) == order and
            c.get("distinct_complete") is True and
            c.get("fixes_roof_block") is True and
            c.get("deleted_element_incomplete") is True,
            "exact-kernel canary drift")


def expected_status(zero: int, empty: bool) -> str:
    if empty:
        return "UNKNOWN_RESOURCE"
    if zero:
        return "CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER"
    return "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS"


def validate_calibration_binding(q: int, a: int, status: str) -> None:
    if status == "CALIBRATION_PASS":
        require((q, a) in CAL_QA, "q5 calibration-value injection")
    elif (q, a) not in CAL_QA:
        require(status != "CALIBRATION_PASS", "q5 calibration-value injection")


def matrix_defect(parts: Sequence[Matrix], q: int) -> Matrix:
    return matrix_paper_prod((minv(matrix_paper_prod((parts[4], parts[2]), q), q),
                              parts[1], parts[3], parts[0]), q)


def check_receipt(path: Path) -> dict[str, Any]:
    rows = load_words()
    r = json.loads(path.read_bytes())
    require(r.get("schema") == SCHEMA and r.get("final_marker") == FINAL,
            "receipt schema/final marker drift")
    require(r.get("status") in {"CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER",
                                 "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS",
                                 "UNKNOWN_RESOURCE", "CALIBRATION_PASS"},
            "producer status is not candidate/unknown")
    require(r.get("q") in (3, 4, 5), "unsupported receipt field")
    q, a = int(r["q"]), int(r["a"])
    burau_generators(q, a)
    require(r.get("matrix_dimension") == 56 and
            r.get("block_layout") == [36, 4, 4, 4, 4, 4],
            "matrix block layout drift")
    require(r.get("field_encoding") ==
            "GF(q) canonical; GF(4) 0,1,Z(4),Z(4)^2",
            "field encoding metadata drift")
    require(r.get("words_sha256") == WORDS_SHA and
            r.get("target_key_sha256") == TARGET_SHA and
            r.get("tuple_sha256") == TUPLE_SHA and
            r.get("row_count") == 972 and isinstance(r.get("rows"), list) and
            len(r["rows"]) == 972, "source/frozen hash drift")
    require_schema_contract(r)
    validate_semantics(r)
    roof = build_roof()
    hx_expected, hy_expected = expected_generators(q, a)
    hg_raw = r.get("h_generators")
    require(isinstance(hg_raw, list) and len(hg_raw) == 2,
            "missing H generator matrices")
    decoded_h = [decode_matrix(x, q) for x in hg_raw]
    require(decoded_h[0][2] == hx_expected and decoded_h[1][2] == hy_expected,
            "H generator matrix/roof/A.18 binding drift")
    H = sym_group([decoded_h[0][2], decoded_h[1][2]])
    require(H.order() == int(r.get("h_order", -1)), "H order drift")
    Hp = H.derived_subgroup(); Hp.schreier_sims()
    require(Hp.order() == int(r.get("hprime_order", -1)), "H' order drift")
    roof_group = sym_group(list(roof))
    require(roof_group.order() == 1469664 and
            roof_group.derived_subgroup().order() == 367416,
            "independent roof order drift")
    K = pointwise_stabilizer(Hp)
    ko = K.order()
    require(ko == int(r.get("kernel_order", -1)) > 0, "kernel order drift")
    kelts = enumerate_sym(K, ko)
    require(len(kelts) == ko and len(set(kelts)) == ko and
            all(block(k, 0, 36) == ident(36) for k in kelts),
            "complete roof kernel gate failed")
    validate_canary(r.get("exact_kernel_canary"), ko)
    kg_raw = r.get("kernel_generators")
    require(isinstance(kg_raw, list) and
            int(r["kernel_generator_count"]) == len(kg_raw),
            "kernel generator reconstructability drift")
    kg = [decode_matrix(x, q)[2] for x in kg_raw]
    if ko > 1:
        require(kg, "nontrivial kernel generator list missing")
    if kg:
        require(sym_group(kg).order() == ko and all(k in K for k in kg),
                "supplied kernel generators do not generate K")
    proj = sym_group([block(own_perm(g, H.degree), 0, 36)
                      for g in Hp.generators])
    require(proj.order() == int(r.get("projection_image_order", -1)) == 367416 and
            proj.order() * ko == Hp.order(), "projection/kernel order drift")
    deleted = kelts[:-1]
    require(len(deleted) == ko - 1 and len(set(deleted)) == ko - 1 and
            digest([list(x) for x in deleted]) != digest([list(x) for x in kelts]),
            "kernel deletion mutation was not detected")
    seen: set[str] = set(); zero = 0; empty = False
    for i, (src, item) in enumerate(zip(rows, r["rows"], strict=True), 1):
        m, key, word = src
        require(isinstance(item, dict) and item.get("row_index") == i and
                item.get("target_key") == key and
                item.get("representative_word_digest") == digest(word),
                f"row source binding drift at {i}")
        require(roof_key(word, roof, m) == key, f"roof replay drift at {i}")
        kd = digest(key); require(kd not in seen, f"duplicate key at {i}"); seen.add(kd)
        _, _, h0 = decode_matrix(item.get("fiber_representative_matrix"), q)
        require(sympy_perm(h0) in Hp and block(h0, 0, 36) == roof_image_for_key(key),
                f"fiber representative binding at {i}")
        coset = sorted(pprod(h0, k) for k in kelts)
        require(int(item.get("fiber_size", -1)) == ko and coset, f"fiber completeness at {i}")
        ids = 0; non = 0; defects: set[Matrix] = set(); identities: list[Perm] = []
        for h in coset:
            parts = [perm_to_matrix(block(h, 36 + j * q ** 4, q ** 4), q)
                     for j in range(5)]
            d = matrix_defect(parts, q)
            if d == eye():
                ids += 1; identities.append(h)
            else:
                non += 1; defects.add(d)
        require(int(item.get("identity_image_defect_count", -1)) == ids and
                int(item.get("nonidentity_image_defect_count", -1)) == non and
                ids + non == ko, f"A.18 count drift at {i}")
        fw = item.get("first_defect_matrix")
        if defects:
            require(isinstance(fw, list) and tuple(tuple(int(x) for x in z) for z in fw)
                    in defects, f"defect witness drift at {i}")
        else:
            require(fw is None, f"unexpected defect witness at {i}")
        fi = item.get("first_identity_fiber_element_matrix")
        if identities:
            if fi is not None:
                _, _, fp = decode_matrix(fi, q)
                require(fp in set(coset) and fp in identities,
                        f"identity witness drift at {i}")
        else:
            require(fi is None, f"unexpected identity witness at {i}")
        if ids == 0: zero += 1
    require(len(seen) == 972, "receipt key set incomplete")
    validate_calibration_binding(q, a, r["status"])
    if r["status"] == "CALIBRATION_PASS":
        require((int(r["h_order"]), int(r["hprime_order"]), ko) ==
                (CAL_H, CAL_HP, CAL_K) and all(
                    x["fiber_size"] == 8 and x["identity_image_defect_count"] == 1 and
                    x["nonidentity_image_defect_count"] == 7
                    for x in r["rows"]), "frozen calibration mismatch")
    expected = expected_status(zero, empty)
    require(r["status"] == "CALIBRATION_PASS" or r["status"] == expected,
            "status/count mismatch")
    return {"status": ("B4_A_BURAU_FINITE_ZERO_FIBER_CROSSCHECKED" if zero
                        else r["status"]), "rows": 972, "h_order": H.order(),
            "hprime_order": Hp.order(), "kernel_order": ko, "zero_fibers": zero}


def mutation_tests() -> None:
    roof = build_roof(); rows = load_words()
    require(pprod((2, 1, 3), (1, 3, 2)) != pprod((1, 3, 2), (2, 1, 3)),
            "noncommuting fixture drift")
    require(paper_prod(((2, 1, 3), (1, 3, 2))) !=
            pprod((2, 1, 3), (1, 3, 2)), "reversed product mutation accepted")
    bad = copy.deepcopy(rows[0][1]); bad[2][0] = 2 if bad[2][0] != 2 else 1
    require(roof_key(rows[0][2], roof, rows[0][0]) != bad,
            "duplicate/bad key mutation accepted")
    s = burau_generators(4, 2)
    require(matrix_perm(s[0], 4) != matrix_perm(s[1], 4), "GF4 action fixture drift")
    good = [list(x) for x in eye(56)]
    badm = copy.deepcopy(good); badm[0][1] = 1
    try:
        decode_matrix(badm, 5)
    except ValueError:
        pass
    else:
        raise AssertionError("bad matrix block mutation accepted")
    try:
        validate_canary({"complete": True, "order": 2,
                         "distinct_complete": True, "fixes_roof_block": True,
                         "deleted_element_incomplete": True}, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("truncated kernel mutation accepted")
    duplicate_rows = [rows[0][1], rows[0][1]]
    try:
        require(len({digest(x) for x in duplicate_rows}) == len(duplicate_rows),
                "duplicate roof keys")
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate key mutation accepted")
    try:
        require(expected_status(1, False) == "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS",
                "forged count/status")
    except ValueError:
        pass
    else:
        raise AssertionError("forged count/status mutation accepted")
    try:
        validate_calibration_binding(5, 2, "CALIBRATION_PASS")
    except ValueError:
        pass
    else:
        raise AssertionError("q5 calibration injection accepted")
    base_contract = {
        "algorithm_evidence": {key: True for key in ALGORITHM_KEYS},
        "generator_order": list(GENERATOR_ORDER),
        "a18_pair_order": list(A18_ORDER),
        "kernel_generator_count": 1,
        "exact_kernel_canary": {"complete": True, "order": 1,
            "distinct_complete": True, "fixes_roof_block": True,
            "deleted_element_incomplete": True},
        "source_target_key_digest": TARGET_SHA,
        "producer_source_sha256": file_sha(PRODUCER_PATH),
    }
    require_schema_contract(base_contract)
    false_independence = copy.deepcopy(base_contract)
    false_independence["algorithm_evidence"]["h_reconstructed_independently"] = True
    try:
        require_schema_contract(false_independence)
    except ValueError:
        pass
    else:
        raise AssertionError("producer-independence metadata mutation accepted")
    wrong_source = copy.deepcopy(base_contract)
    wrong_source["producer_source_sha256"] = "0" * 64
    try:
        require_schema_contract(wrong_source)
    except ValueError:
        pass
    else:
        raise AssertionError("wrong producer source hash accepted")
    missing_canary = copy.deepcopy(base_contract)
    del missing_canary["exact_kernel_canary"]
    try:
        require_schema_contract(missing_canary)
    except ValueError:
        pass
    else:
        raise AssertionError("missing deletion canary accepted")
    misleading_degree = copy.deepcopy(base_contract)
    misleading_degree["permutation_degree"] = 3161
    try:
        require_schema_contract(misleading_degree)
    except ValueError:
        pass
    else:
        raise AssertionError("permutation-degree substitution accepted")


def selftest() -> None:
    roof = build_roof(); require(len(roof[0]) == 36, "roof degree drift")
    rows = load_words()
    require(all(roof_key(x[2], roof, x[0]) == x[1] for x in rows),
            "972 roof replay selftest failed")
    require(all(block(eval_word(x[2], roof), 0, 36) == roof_image_for_key(x[1])
                for x in rows), "word/key roof binding selftest failed")
    require(all(fmul(x, finv(x, 4), 4) == 1 for x in (1, 2, 3)),
            "GF4 arithmetic selftest failed")
    for q, a in ((3, -1), (4, 2), (5, 2)):
        s = burau_generators(q, a)
        require(mmul(mmul(s[0], s[1], q), s[0], q) ==
                mmul(mmul(s[1], s[0], q), s[1], q), "Artin braid selftest failed")
        require(mmul(mmul(s[1], s[2], q), s[1], q) ==
                mmul(mmul(s[2], s[1], q), s[2], q), "Artin braid selftest failed")
        require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q),
                "Artin commuting selftest failed")
        require(all(set(matrix_perm(x, q)) == set(range(1, q ** 4 + 1)) for x in s),
                "finite-field vector action selftest failed")
    mutation_tests()
    print("D972_B4_BURAU_MATRIX56_CHECKER_SELFTEST_PASS")
    print("D972_B4_BURAU_MATRIX56_CHECKER_FINAL_MARKER status=PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    ns = ap.parse_args()
    if ns.self_test:
        selftest()
    elif ns.receipt:
        print("D972_B4_BURAU_MATRIX56_CHECK_PASS",
              json.dumps(check_receipt(Path(ns.receipt)), sort_keys=True))
    else:
        ap.error("receipt path or --self-test required")


if __name__ == "__main__":
    main()
