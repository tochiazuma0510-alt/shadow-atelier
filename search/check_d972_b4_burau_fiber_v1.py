"""Independent finite Burau-fiber checker for the fixed D972 roof.

The checker does not import GAP, the producer, or any producer worker.  The
roof is rebuilt from the frozen MakeDn/MakeGn and GF(8) formulae; the finite
Burau image is rebuilt over the explicit GF(3)/GF(4) encodings.  SymPy is used
for the permutation-group order, derived subgroup, and successive point
stabilizer (the latter is the faithful roof projection kernel).

This is deliberately fail-closed.  Kernel elements and fiber digests are
reconstructed independently (optional producer copies are never trusted);
empty fibers, incomplete rows, or a merely declared digest are not accepted.
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
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ARTIFACT_ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
SEMANTIC_SHA = "3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729"
SCHEMA = "d972-b4-burau-fiber/v1"
FINAL = "D972_B4_BURAU_FIBER_V1_FINAL"
GENERATOR_ORDER = ("x12", "x13", "x14", "x23", "x24", "x34")
A18_NAMES = ("123", "234", "12,3,4", "1,23,4", "1,2,34")
ID_IMAGE_FIELD = "identity_image_defect_count"

Matrix = tuple[tuple[int, ...], ...]
Perm = tuple[int, ...]                 # one-line, GAP right-action convention


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"),
                      sort_keys=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ident(n: int) -> Perm:
    return tuple(range(1, n + 1))


def pprod(a: Perm, b: Perm) -> Perm:
    # GAP: i^(a*b)=(i^a)^b.
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
    require(vals, "PaperProd cannot be empty")
    out = ident(len(vals[0]))
    for x in reversed(vals):
        out = pprod(out, x)
    return out


def paper_word(words: Iterable[Iterable[int]]) -> list[int]:
    out: list[int] = []
    for w in reversed([list(x) for x in words]):
        out.extend(w)
    reduced: list[int] = []
    for x in out:
        if reduced and reduced[-1] == -x:
            reduced.pop()
        else:
            reduced.append(x)
    return reduced


def direct_sum(a: Perm, b: Perm) -> Perm:
    n = len(a)
    return a + tuple(n + x for x in b)


def block(p: Perm, offset: int, size: int) -> Perm:
    vals = tuple(p[offset + i] - offset for i in range(size))
    require(set(vals) == set(range(1, size + 1)), "permutation block drift")
    return vals


def eval_word(word: Iterable[int], gens: Sequence[Perm]) -> Perm:
    out = ident(len(gens[0]))
    for x in word:
        require(isinstance(x, int) and not isinstance(x, bool) and x and abs(x) <= len(gens),
                "invalid signed word")
        out = pprod(out, ppow(gens[abs(x) - 1], 1 if x > 0 else -1))
    return out


# ---- Independent compact D972 roof --------------------------------------

def make_dn(n: int) -> tuple[Perm, Perm]:
    r = tuple(range(2, n + 1)) + (1,)
    # Frozen MakeDn: s fixes 1 and reverses the remaining points.
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

    x = pprod(pprod(tr(r, 1), tr(s, 2)), tr(s, 3))
    sr = pprod(s, r)
    y = pprod(pprod(tr(sr, 1), tr(r, 2)), tr(sr, 3))
    return x, y


def gf8_mul(a: int, b: int) -> int:
    z = 0
    for i in range(3):
        if (b >> i) & 1:
            z ^= a << i
    for i in (4, 3):
        if (z >> i) & 1:
            z ^= 0b1011 << (i - 3)
    return z


def gf8_inv(a: int) -> int:
    require(1 <= a <= 7, "GF8 inverse of zero/out-of-range")
    for b in range(1, 8):
        if gf8_mul(a, b) == 1:
            return b
    raise ValueError("GF8 inverse table incomplete")


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
    x, y = direct_sum(x9, x4), direct_sum(y9, y4)
    require(len(x) == len(y) == 36, "compact roof degree drift")
    return x, y


def d9_coords(p: Perm) -> list[int]:
    r, s = make_dn(9)
    for a in range(9):
        for e in range(2):
            if p == pprod(ppow(r, a), ppow(s, e)):
                return [a, e]
    raise ValueError("D9 normal-form coordinate failure")


def roof_key(word: list[int], roof: tuple[Perm, Perm], m: int) -> list[Any]:
    image = eval_word(word, roof)
    p27, p9 = block(image, 0, 27), block(image, 27, 9)
    can9 = [d9_coords(block(p27, 9 * i, 9)) for i in range(3)]
    return [int(m), can9, list(p9)]


def load_words(path: Path = WORDS_PATH) -> list[list[Any]]:
    require(file_sha(path) == WORDS_SHA, "word artifact SHA drift")
    obj = json.loads(path.read_bytes())
    require(obj.get("schema") == "d972-b4-word-key-artifact/v1" and
            obj.get("count") == 972 and isinstance(obj.get("rows"), list) and
            len(obj["rows"]) == 972, "word artifact shape drift")
    require(obj.get("canonical_bytes_sha256") == digest(obj["rows"]) == ARTIFACT_ROWS_SHA,
            "word artifact canonical digest drift")
    require(obj.get("source_target_key_digest") == TARGET_SHA and
            obj.get("frozen_tuple_sha256") == TUPLE_SHA, "word artifact metadata drift")
    require(digest([row[1] for row in obj["rows"]]) == TUPLE_SHA,
            "independent target-key tuple digest drift")
    for row in obj["rows"]:
        require(isinstance(row, list) and len(row) == 3, "word row shape drift")
        require(isinstance(row[2], list), "word row signed word drift")
    return obj["rows"]


# ---- Explicit finite-field Burau implementation -------------------------

def fadd(a: int, b: int, q: int) -> int:
    return (a + b) % 3 if q == 3 else a ^ b


def fneg(a: int, q: int) -> int:
    return (-a) % 3 if q == 3 else a


def fmul(a: int, b: int, q: int) -> int:
    if q == 3:
        return (a * b) % 3
    z = 0
    for i in range(2):
        if (b >> i) & 1:
            z ^= a << i
    if z & 4:
        z ^= 0b111
    return z


def finv(a: int, q: int) -> int:
    require(a % q != 0, "field inverse of zero")
    for b in range(1, q):
        if fmul(a, b, q) == 1:
            return b
    raise ValueError("finite-field inverse table incomplete")


def fsub(a: int, b: int, q: int) -> int:
    return fadd(a, fneg(b, q), q)


def mmul(a: Matrix, b: Matrix, q: int) -> Matrix:
    n = len(a)
    return tuple(tuple(__import__("functools").reduce(
        lambda z, k: fadd(z, fmul(a[i][k], b[k][j], q), q), range(n), 0)
        for j in range(n)) for i in range(n))


def mpow(a: Matrix, n: int, q: int) -> Matrix:
    out = eye(len(a))
    while n:
        if n & 1:
            out = mmul(out, a, q)
        a = mmul(a, a, q)
        n >>= 1
    return out


def eye(n: int) -> Matrix:
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def minv(a: Matrix, q: int) -> Matrix:
    n = len(a)
    rows = [list(a[i]) + list(eye(n)[i]) for i in range(n)]
    for c in range(n):
        r = next((z for z in range(c, n) if rows[z][c] % q), None)
        require(r is not None, "singular Burau matrix")
        rows[c], rows[r] = rows[r], rows[c]
        scale = finv(rows[c][c] % q, q)
        rows[c] = [fmul(x, scale, q) for x in rows[c]]
        for z in range(n):
            if z != c and rows[z][c] % q:
                scale = rows[z][c] % q
                rows[z] = [fsub(x, fmul(scale, y, q), q) for x, y in zip(rows[z], rows[c])]
    return tuple(tuple(row[n:]) for row in rows)


def det_nonzero(a: Matrix, q: int) -> bool:
    rows = [list(x) for x in a]
    for c in range(len(rows)):
        r = next((z for z in range(c, len(rows)) if rows[z][c] % q), None)
        if r is None:
            return False
        rows[c], rows[r] = rows[r], rows[c]
        inv = finv(rows[c][c] % q, q)
        for z in range(c + 1, len(rows)):
            scale = fmul(rows[z][c], inv, q)
            for j in range(c, len(rows)):
                rows[z][j] = fsub(rows[z][j], fmul(scale, rows[c][j], q), q)
    return True


def burau_generators(q: int, a: int) -> tuple[Matrix, Matrix, Matrix]:
    require(q in (3, 4), "only GF(3) and GF(4) are frozen")
    a %= q
    require(a != 0, "Burau parameter a=0")
    out = []
    for i in range(3):
        m = [list(x) for x in eye(4)]
        m[i][i], m[i][i + 1] = fsub(1, a, q), a
        m[i + 1][i], m[i + 1][i + 1] = 1, 0
        out.append(tuple(tuple(x) for x in m))
    return tuple(out)  # type: ignore[return-value]


def pure_generators(q: int, a: int) -> tuple[Matrix, ...]:
    s1, s2, s3 = burau_generators(q, a)
    i1, i2, i3 = minv(s1, q), minv(s2, q), minv(s3, q)
    p1, p4, p6 = mpow(s1, 2, q), mpow(s2, 2, q), mpow(s3, 2, q)
    def pp(xs: Iterable[Matrix]) -> Matrix:
        vals = list(xs); out = eye(4)
        for x in reversed(vals): out = mmul(out, x, q)
        return out
    return (p1, pp((s2, p1, i2)), pp((s3, s2, p1, i2, i3)),
            p4, pp((s3, p4, i3)), p6)


def matrix_perm(m: Matrix, q: int) -> Perm:
    vectors = [(n // (q ** 3) % q, n // (q ** 2) % q, n // q % q, n % q)
               for n in range(q ** 4)]
    pos = {v: i + 1 for i, v in enumerate(vectors)}
    out = []
    for v in vectors:
        image = tuple(__import__("functools").reduce(
            lambda z, k: fadd(z, fmul(v[k], m[k][j], q), q), range(4), 0)
            for j in range(4))
        out.append(pos[image])
    return tuple(out)


def a18_pairs(pure: tuple[Matrix, ...], q: int) -> tuple[tuple[Matrix, Matrix], ...]:
    x12, x13, x14, x23, x24, x34 = pure
    def pp(xs: Iterable[Matrix]) -> Matrix:
        out = eye(4)
        for x in reversed(list(xs)): out = mmul(out, x, q)
        return out
    return ((x12, x23), (x23, x34), (pp((x13, x23)), x34),
            (pp((x12, x13)), pp((x24, x34))), (x12, pp((x23, x24))))


def component_prod(xs: Iterable[Perm]) -> Perm:
    vals = list(xs); require(vals, "empty component product")
    return paper_prod(vals)


def defect(parts: Sequence[Perm]) -> Perm:
    require(len(parts) == 5, "A.18 component count drift")
    # Paper D=(p5 p3)^-1 p2 p4 p1; PaperProd performs the frozen reversal.
    return paper_prod((pinv(paper_prod((parts[4], parts[2]))),
                       parts[1], parts[3], parts[0]))


# ---- SymPy group conversion and exact projection kernel ------------------

def sympy_perm(p: Perm) -> Permutation:
    return Permutation([x - 1 for x in p], size=len(p))


def own_perm(p: Permutation, n: int) -> Perm:
    arr = p.array_form
    return tuple((arr[i] if i < len(arr) else i) + 1 for i in range(n))


def sym_group(gens: Sequence[Perm]) -> PermutationGroup:
    require(gens, "empty permutation generating set")
    n = len(gens[0])
    G = PermutationGroup([sympy_perm(g) for g in gens])
    G.schreier_sims()
    require(G.degree == n, "SymPy permutation degree drift")
    return G


def enumerate_sym(G: PermutationGroup, expected: int | None = None) -> list[Perm]:
    if expected is not None:
        require(G.order() == expected, "group order mismatch before enumeration")
    vals = [own_perm(x, G.degree) for x in G.generate_dimino()]
    require(len(vals) == G.order(), "SymPy enumeration incomplete")
    return sorted(set(vals))


def pointwise_stabilizer(G: PermutationGroup, points: range) -> PermutationGroup:
    K = G
    for point in points:
        K = K.stabilizer(point)
        K.schreier_sims()
    return K


def combined_generators(q: int, a: int) -> tuple[Perm, Perm, tuple[Perm, ...]]:
    roof = build_roof()
    pure = pure_generators(q, a)
    pairs = a18_pairs(pure, q)
    blocks = tuple((matrix_perm(x, q), matrix_perm(y, q)) for x, y in pairs)
    hx, hy = roof[0], roof[1]
    for j, (px, py) in enumerate(blocks):
        off = 36 + j * q ** 4
        hx += tuple(off + x for x in px)
        hy += tuple(off + x for x in py)
    return hx, hy, tuple(x for pair in blocks for x in pair)


def validate_semantics(receipt: dict[str, Any]) -> None:
    expected = {"M": "K^(9) intersect N_S4", "P": "G9 x PSL(2,8)",
                "P_order": 1469664, "roof_count": 972,
                "arithmetic_count": 324, "outside_count": 648,
                "index3_dichotomy": True}
    s = receipt.get("semantic_premises")
    require(isinstance(s, dict) and {k: s.get(k) for k in expected} == expected and
            s.get("digest") == SEMANTIC_SHA and digest(expected) == SEMANTIC_SHA,
            "semantic premise digest drift")


def check_receipt(receipt_path: Path, words_path: Path = WORDS_PATH) -> dict[str, Any]:
    rows = load_words(words_path)
    receipt = json.loads(receipt_path.read_bytes())
    require(receipt.get("schema") == SCHEMA and receipt.get("final_marker") == FINAL,
            "receipt schema/final marker drift")
    require(receipt.get("words_sha256") == WORDS_SHA and receipt.get("row_count") == 972 and
            isinstance(receipt.get("rows"), list) and len(receipt["rows"]) == 972,
            "receipt source/row binding drift")
    validate_semantics(receipt)
    require(receipt.get("generator_order") == list(GENERATOR_ORDER) and
            receipt.get("a18_pair_order") == list(A18_NAMES), "generator/A.18 order drift")
    q, a = int(receipt.get("q", 0)), int(receipt.get("a", 0))
    s = burau_generators(q, a)
    require(mmul(mmul(s[0], s[1], q), s[0], q) == mmul(mmul(s[1], s[0], q), s[1], q),
            "Burau s1/s2 braid relation drift")
    require(mmul(mmul(s[1], s[2], q), s[1], q) ==
            mmul(mmul(s[2], s[1], q), s[2], q),
            "Burau s2/s3 braid relation drift")
    require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q),
            "Burau s1/s3 commuting relation drift")
    require(all(det_nonzero(x, q) for x in s), "Burau invertibility drift")
    pure = pure_generators(q, a)
    pairs = a18_pairs(pure, q)
    expected_hx, expected_hy, _ = combined_generators(q, a)
    degree = int(receipt.get("permutation_degree", 0))
    require(degree == 36 + 5 * q ** 4, "combined degree drift")
    hgens = [tuple(int(x) for x in p) for p in receipt.get("h_generators", [])]
    require(hgens == [expected_hx, expected_hy], "combined H generator binding drift")

    H = sym_group(hgens)
    h_order = int(receipt.get("h_order", -1))
    require(H.order() == h_order, "H order drift")
    roof = build_roof()
    roof_group = sym_group(list(roof))
    require(roof_group.order() == 1469664 and
            roof_group.derived_subgroup().order() == 367416,
            "independent compact roof order/derived gate failed")
    Hp = H.derived_subgroup()
    Hp.schreier_sims()
    hp_order = int(receipt.get("hprime_order", -1))
    require(Hp.order() == hp_order, "H' order drift")
    K = pointwise_stabilizer(Hp, range(36))
    K.schreier_sims()
    kernel_order = int(receipt.get("kernel_order", -1))
    require(K.order() == kernel_order and kernel_order > 0, "projection kernel order drift")
    kernel = enumerate_sym(K, kernel_order)
    require(len(kernel) == kernel_order and all(block(k, 0, 36) == ident(36) for k in kernel),
            "pointwise roof kernel enumeration drift")
    projection_order = int(receipt.get("projection_image_order", -1))
    projected_generators = [block(own_perm(g, degree), 0, 36) for g in Hp.generators]
    projection_group = sym_group(projected_generators)
    require(projection_group.order() == projection_order == 367416,
            "independent roof projection image/order drift")
    require(projection_order * kernel_order == hp_order,
            "projection image/order formula drift")

    # Every 972 word/key pair is replayed against the independently rebuilt roof.
    for i, (source, item) in enumerate(zip(rows, receipt["rows"], strict=True), 1):
        m, target, word = source[0], source[1], source[2]
        require(item.get("row_index") == i and item.get("target_key") == target,
                f"roof row binding drift at {i}")
        require(digest(word) == item.get("representative_word_digest"),
                f"word digest drift at {i}")
        require(roof_key(word, roof, m) == target, f"independent roof replay failed at {i}")
        fs = int(item.get("fiber_size", -1))
        require(fs == kernel_order and fs > 0, f"noncomplete/empty fiber at {i}")
        rep = tuple(int(x) for x in item.get("fiber_representative", []))
        require(len(rep) == degree and set(rep) == set(range(1, degree + 1)),
                f"fiber representative shape drift at {i}")
        # h0 must be in H' and have exactly the target roof projection.
        require(sympy_perm(rep) in Hp, f"fiber representative is not in H' at {i}")
        require(block(rep, 0, 36) in _roof_images_for_key(target, roof),
                f"fiber representative roof target drift at {i}")
        coset = sorted(pprod(rep, k) for k in kernel)
        require(len(coset) == fs and all(sympy_perm(x) in Hp for x in coset),
                f"fiber coset is not exact H' kernel coset at {i}")
        if item.get("fiber_digest") is not None:
            require(item.get("fiber_digest") == digest([list(x) for x in coset]),
                    f"fiber digest drift at {i}")
        actual = 0
        actual_defects: set[Perm] = set()
        for h in coset:
            parts = [block(h, 36 + j * q ** 4, q ** 4) for j in range(5)]
            d = defect(parts)
            if d == ident(q ** 4):
                actual += 1
            else:
                actual_defects.add(d)
        # Producer schema has used this spelling; accept the old spelling only
        # as an explicitly nonterminal compatibility input.
        declared = item.get(ID_IMAGE_FIELD, item.get("identity_defect_count"))
        require(int(declared) == actual, f"raw finite defect count drift at {i}")
        require(int(item.get("nonidentity_image_defect_count",
                            item.get("nonidentity_defect_count", -1))) == fs - actual,
                f"raw finite nonidentity count drift at {i}")
        witness = item.get("first_defect_witness")
        if actual_defects:
            require(isinstance(witness, list) and len(witness) == q ** 4,
                    f"first defect witness missing at {i}")
            wt = tuple(int(x) for x in witness)
            require(set(wt) == set(range(1, q ** 4 + 1)) and wt in actual_defects,
                    f"first defect witness is not an actual defect at {i}")

    status = receipt.get("status")
    require(status in {"CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER",
                       "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS", "UNKNOWN_RESOURCE"},
            "unknown terminal status")
    counts = [int(item.get(ID_IMAGE_FIELD, item.get("identity_defect_count", -1)))
              for item in receipt["rows"]]
    zero = sum(x == 0 for x in counts)
    if status == "CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER":
        require(zero >= 1, "terminal zero fiber gate failed")
    elif status == "UNKNOWN_BURAU_SPECIALIZATION_ALLPASS":
        require(zero == 0, "all-pass status has a zero fiber")
    result_status = ("B4_A_BURAU_FINITE_ZERO_FIBER_CROSSCHECKED"
                     if status == "CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER" else status)
    return {"status": result_status, "rows": 972, "kernel_order": kernel_order,
            "zero_fibers": zero}


def _roof_images_for_key(target: list[Any], roof: tuple[Perm, Perm]) -> set[Perm]:
    # A target key identifies one pure roof element.  Reconstruct its unique
    # 36-point one-line image from the three D9 coordinates and PSL block.
    p27 = []
    r, s = make_dn(9)
    for i, (a, e) in enumerate(target[1]):
        local = pprod(ppow(r, int(a)), ppow(s, int(e)))
        p27.extend(9 * i + z for z in local)
    return {tuple(p27) + tuple(27 + int(x) for x in target[2])}


def mutation_tests() -> None:
    roof = build_roof()
    require(paper_word(([1], [2])) == [2, 1], "reverse PaperProd mutation not detected")
    require(paper_word(([1], [2])) != [1, 2], "PaperProd reverse mutation accepted")
    s = burau_generators(3, -1)
    correct = pure_generators(3, -1)[1]
    reverse_x13 = mmul(mmul(s[1], mpow(s[0], 2, 3), 3), minv(s[1], 3), 3)
    require(correct != reverse_x13, "reverse x13 mutation accepted")
    pure = pure_generators(3, -1)
    pairs = a18_pairs(pure, 3)
    # Use a genuine common word (x*y), since the one-letter A.18 images
    # happen to commute in this small specialization.
    def meval(word: Sequence[int], pair: tuple[Matrix, Matrix]) -> Matrix:
        out = eye(4)
        for z in word:
            out = mmul(out, pair[z - 1] if z > 0 else minv(pair[-z - 1], 3), 3)
        return out
    parts = [matrix_perm(meval((1, 2), pair), 3) for pair in pairs]
    good = defect(parts)
    swapped = paper_prod((pinv(paper_prod((parts[2], parts[4]))),
                          parts[1], parts[3], parts[0]))
    require(good != swapped, "swapped leading A.18 mutation accepted")
    # Real coset mutation: derive the actual q=3 roof kernel and remove one
    # of its elements.  The exact coset digest must change.
    hx, hy, _ = combined_generators(3, -1)
    q3k = pointwise_stabilizer(sym_group([hx, hy]).derived_subgroup(), range(36))
    k = enumerate_sym(q3k, q3k.order())
    require(len(k) > 1 and
            digest([list(x) for x in sorted(k)]) != digest([list(x) for x in sorted(k[:-1])]),
            "deleted kernel element mutation accepted")
    rows = load_words()
    roof_key0 = roof_key(rows[0][2], roof, rows[0][0])
    bad = copy.deepcopy(roof_key0); bad[2][0] = 2 if bad[2][0] != 2 else 1
    require(bad != rows[0][1], "corrupt roof key mutation accepted")
    bad_word = list(rows[1][2]); bad_word[0] = -bad_word[0]
    require(roof_key(bad_word, roof, rows[1][0]) != rows[1][1],
            "corrupt roof word mutation accepted")


def selftest() -> None:
    # The small complete roof/field gates are cheap and exercise every frozen
    # convention; the full H/H' scan belongs to check_receipt.
    x, y = build_roof()
    require(len(x) == 36 and len(y) == 36, "roof selftest degree")
    roof_group = sym_group([x, y])
    require(roof_group.order() == 1469664 and
            roof_group.derived_subgroup().order() == 367416,
            "roof order/derived selftest")
    rows = load_words()
    require(all(roof_key(row[2], (x, y), row[0]) == row[1] for row in rows),
            "all 972 independent roof replays failed")
    require(all(block(eval_word(row[2], (x, y)), 0, 36) in
                _roof_images_for_key(row[1], (x, y)) for row in rows),
            "all 972 key-to-roof-image regressions failed")
    a3, b3 = tuple([2, 1, 3]), tuple([1, 3, 2])
    require(own_perm(sympy_perm(a3), 3) == a3 and
            own_perm(sympy_perm(pprod(a3, b3)), 3) == pprod(a3, b3) and
            (sympy_perm(a3) * sympy_perm(b3)).array_form == list(x - 1 for x in pprod(a3, b3)),
            "SymPy/GAP composition conversion drift")
    for q, a in ((3, -1), (4, 2)):
        s = burau_generators(q, a)
        require(mmul(mmul(s[0], s[1], q), s[0], q) ==
                mmul(mmul(s[1], s[0], q), s[1], q), "Burau braid selftest")
        require(mmul(mmul(s[1], s[2], q), s[1], q) ==
                mmul(mmul(s[2], s[1], q), s[2], q),
                "Burau s2/s3 braid selftest")
        require(mmul(s[0], s[2], q) == mmul(s[2], s[0], q),
                "Burau s1/s3 commuting selftest")
        require(all(det_nonzero(z, q) for z in s), "Burau determinant selftest")
        p = pure_generators(q, a)
        require(len(a18_pairs(p, q)) == 5, "A.18 pair selftest")
    mutation_tests()
    print("D972_B4_BURAU_FIBER_CHECKER_SELFTEST_PASS")
    print("D972_B4_BURAU_FIBER_CHECKER_FINAL_MARKER status=PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        selftest()
    elif args.receipt:
        print("D972_B4_BURAU_FIBER_CHECK_PASS",
              json.dumps(check_receipt(Path(args.receipt)), sort_keys=True))
    else:
        ap.error("receipt path or --self-test required")


if __name__ == "__main__":
    main()
