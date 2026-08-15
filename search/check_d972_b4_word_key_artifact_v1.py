"""Independent checker for the B4 exact roof word/key receipt.

This file deliberately does not import the GAP producer or source-map-A
driver.  It rebuilds the marked compact generators on 27+9 points, evaluates
the signed F2 word in the natural free-group order, and serializes the three
D9 blocks and the PSL(2,8) one-line independently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from typing import Any, Iterable


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FROZEN_PATH = os.path.join(ROOT, "search", "certs",
                           "nf972_sourcemap_a_tuples_v2_20260804.json")

FROZEN_TUPLE_SHA256 = (
    "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
)

# This remains empty until a GAP receipt and this checker agree.  An empty
# value is intentional fail-closed state, never a permission to adjudicate.
PINNED_ARTIFACT_SHA256 = ""


def cjson(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def identity(n: int) -> tuple[int, ...]:
    return tuple(range(1, n + 1))


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    # GAP convention: i^(p*q)=(i^p)^q.
    return tuple(q[p[i] - 1] for i in range(len(p)))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(p)
    for i, image in enumerate(p, 1):
        out[image - 1] = i
    return tuple(out)


def power(p: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    if exponent < 0:
        return power(inverse(p), -exponent)
    out = identity(len(p))
    for _ in range(exponent):
        out = compose(out, p)
    return out


def direct_sum(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    n = len(p)
    return tuple(p) + tuple(n + x for x in q)


def block(p: tuple[int, ...], offset: int, size: int) -> tuple[int, ...]:
    vals = tuple(p[offset + i] - offset for i in range(size))
    if set(vals) != set(range(1, size + 1)):
        raise ValueError("permutation does not preserve requested block")
    return vals


def make_dn(n: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    r = tuple(list(range(2, n + 1)) + [1])
    # Exact MakeDn from the marked GAP construction; s fixes point 1.
    s = tuple(((n - (j - 1)) % n) + 1 for j in range(1, n + 1))
    if compose(compose(s, r), inverse(s)) != inverse(r):
        raise AssertionError("D_n relation failed")
    return r, s


def make_gn(n: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    r, s = make_dn(n)

    def tr(p: tuple[int, ...], which: int) -> tuple[int, ...]:
        out = list(range(1, 3 * n + 1))
        off = (which - 1) * n
        for j in range(1, n + 1):
            out[off + j - 1] = off + p[j - 1]
        return tuple(out)

    x = compose(compose(tr(r, 1), tr(s, 2)), tr(s, 3))
    sr = compose(s, r)
    y = compose(compose(tr(sr, 1), tr(r, 2)), tr(sr, 3))
    return x, y


def gf8_add(a: int, b: int) -> int:
    return a ^ b


def gf8_mul(a: int, b: int) -> int:
    result = 0
    for i in range(3):
        if (b >> i) & 1:
            result ^= a << i
    for i in (4, 3):
        if (result >> i) & 1:
            result ^= 11 << (i - 3)  # X^3+X+1
    return result


def gf8_inv(a: int) -> int:
    if a == 0:
        raise ValueError("zero has no inverse")
    for b in range(1, 8):
        if gf8_mul(a, b) == 1:
            return b
    raise AssertionError("GF(8) inverse table incomplete")


def mat_perm(matrix: list[list[int]]) -> tuple[int, ...]:
    a, b = matrix[0]
    c, d = matrix[1]
    out = [0] * 9
    out[0] = 1 if c == 0 else 2 + gf8_mul(a, gf8_inv(c))
    for x in range(8):
        num = gf8_add(gf8_mul(a, x), b)
        den = gf8_add(gf8_mul(c, x), d)
        out[1 + x] = 1 if den == 0 else 2 + gf8_mul(num, gf8_inv(den))
    return tuple(out)


def build_compact_generators() -> tuple[tuple[int, ...], tuple[int, ...]]:
    g9x, g9y = make_gn(9)
    s = mat_perm([[1, 0], [1, 1]])
    t = mat_perm([[4, 3], [1, 5]])
    w = compose(s, inverse(t))
    x4 = compose(w, w)
    y4 = compose(compose(inverse(s), x4), s)
    return direct_sum(g9x, x4), direct_sum(g9y, y4)


def eval_raw_word(word: Iterable[int], gens: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    out = identity(len(gens[0]))
    for signed in word:
        if not isinstance(signed, int) or signed == 0 or abs(signed) > len(gens):
            raise ValueError("invalid signed F2 word letter")
        out = compose(out, power(gens[abs(signed) - 1], 1 if signed > 0 else -1))
    return out


def d9_coords(p: tuple[int, ...]) -> list[int]:
    r, s = make_dn(9)
    for a in range(9):
        for e in range(2):
            if p == compose(power(r, a), power(s, e)):
                return [a, e]
    raise ValueError("word image is outside the fixed D9 normal-form table")


def key_from_word(word: list[int], gens: tuple[tuple[int, ...], ...], m: int) -> list[Any]:
    image = eval_raw_word(word, gens)
    first = block(image, 0, 27)
    second = block(image, 27, 9)
    can9: list[list[int]] = []
    for i in range(3):
        can9.append(d9_coords(block(first, 9 * i, 9)))
    can4 = list(second)
    return [int(m), can9, can4]


def load_frozen() -> tuple[list[list[Any]], str]:
    with open(FROZEN_PATH, encoding="utf-8") as handle:
        obj = json.load(handle)
    tuples = obj.get("tuples")
    if not isinstance(tuples, list) or len(tuples) != 972:
        raise ValueError("frozen tuple file must contain exactly 972 tuples")
    got = sha(tuples)
    if got != FROZEN_TUPLE_SHA256:
        raise ValueError(f"frozen tuple digest mismatch: {got}")
    if obj.get("canonical_bytes_sha256") != FROZEN_TUPLE_SHA256:
        raise ValueError("frozen metadata digest mismatch")
    return tuples, got


def row_parts(row: Any) -> tuple[int, list[Any], list[int]]:
    if isinstance(row, list) and len(row) == 3:
        m, key, word = row
    elif isinstance(row, dict):
        m, key, word = row.get("m"), row.get("key"), row.get("word")
    else:
        raise ValueError("artifact row must be [m,key,word] or a named object")
    if not isinstance(m, int) or not isinstance(key, list) or not isinstance(word, list):
        raise ValueError("artifact row has invalid field types")
    if any(not isinstance(x, int) or x == 0 for x in word):
        raise ValueError("artifact word must be a nonzero signed integer list")
    return m, key, word


def check_artifact(path: str) -> dict[str, Any]:
    frozen, frozen_sha = load_frozen()
    with open(path, encoding="utf-8") as handle:
        obj = json.load(handle)
    rows = obj.get("rows") if isinstance(obj, dict) else obj
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word/key artifact must contain exactly 972 rows")
    canonical_sha = sha(rows)
    declared_sha = obj.get("canonical_bytes_sha256") if isinstance(obj, dict) else None
    if declared_sha != canonical_sha:
        raise ValueError("artifact declared digest is not its canonical rows digest")
    if PINNED_ARTIFACT_SHA256 and canonical_sha != PINNED_ARTIFACT_SHA256:
        raise ValueError("artifact digest is not the independently pinned digest")

    gens = build_compact_generators()
    target_keys = {json.dumps(x, separators=(",", ":"), ensure_ascii=True) for x in frozen}
    seen: set[str] = set()
    mismatches: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        m, supplied_key, word = row_parts(row)
        computed = key_from_word(word, gens, m)
        supplied_s = json.dumps(supplied_key, separators=(",", ":"), ensure_ascii=True)
        computed_s = json.dumps(computed, separators=(",", ":"), ensure_ascii=True)
        if supplied_s != computed_s or computed_s not in target_keys:
            mismatches.append({"index": index, "supplied": supplied_key,
                               "computed": computed})
        seen.add(computed_s)
    if not mismatches and seen != target_keys:
        raise ValueError("artifact computed-key set is not exactly the frozen set")
    if mismatches:
        raise ValueError(f"word/key mismatches: first={mismatches[0]}")
    return {"status": "PASS_UNPINNED" if not PINNED_ARTIFACT_SHA256 else "PASS",
            "count": len(rows), "frozen_tuple_sha256": frozen_sha,
            "artifact_sha256": canonical_sha,
            "generator_one_line_sha256": sha([list(g) for g in gens]),
            "pinned": bool(PINNED_ARTIFACT_SHA256)}


def selftest() -> None:
    gens = build_compact_generators()
    if len(gens[0]) != 36 or len(gens[1]) != 36:
        raise AssertionError("compact generators must act on 27+9 points")
    if eval_raw_word([], gens) != identity(36):
        raise AssertionError("empty word evaluation failed")
    if eval_raw_word([1, -1], gens) != identity(36):
        raise AssertionError("inverse signed word evaluation failed")
    # Regression for the D9 normal form and the negative-letter direction.
    r, s = make_dn(9)
    for a in range(9):
        for e in range(2):
            if d9_coords(compose(power(r, a), power(s, e))) != [a, e]:
                raise AssertionError("D9 coordinate round-trip failed")
    # Tamper gate: a producer cannot turn a fake 972-row receipt into a pass
    # merely by supplying its own declared digest.
    fake_rows = [[0, [0, [[0, 0], [0, 0], [0, 0]], list(range(1, 10))], []]
                 for _ in range(972)]
    fake = {"schema": "d972-b4-word-key-artifact/v1", "count": 972,
            "canonical_bytes_sha256": sha(fake_rows), "rows": fake_rows}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as handle:
        fake_path = handle.name
        json.dump(fake, handle, separators=(",", ":"))
    try:
        try:
            check_artifact(fake_path)
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError("tampered word/key artifact was accepted")
    finally:
        try:
            os.unlink(fake_path)
        except OSError:
            pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", nargs="?")
    args = parser.parse_args(argv)
    selftest()
    if args.artifact is None:
        print("WORD_KEY_CHECKER_SELFTEST_PASS")
        return 0
    result = check_artifact(os.path.abspath(args.artifact))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
