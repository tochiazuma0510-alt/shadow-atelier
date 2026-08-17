"""Independent checker for the exact D972 shadow power spectrum v3.

No GAP producer or group helper is imported.  The checker reconstructs the
degree-36 roof, replays all authenticated common words, recomputes the full
table, and independently derives powers, exponent, and associativity from the
generator-action composition law.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import deque
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "search/certs/d972_b4_word_key_artifact_v1_20260816.json"
ARTIFACT_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
SCHEMA = "d972-power-spectrum/v3"
RUNTIME_SOURCES = {
    "search/d972_dovetail_core_v2.g": "1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae",
    "search/probe/wac_v1/gap_output_prelude.g": "2e4da671ad9d018be1bc6f2f387f0e1d597e87c2c0e807eef40aeef3b92deece",
    "search/gaplib_common.g": "f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911",
    "search/week3-battery-common.g": "aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998",
    "search/week3-psl-common.g": "e48e50d55562983415b5691d07e3d893182620b1f73b8fe35ea77815ad9695c4",
}

Perm = tuple[int, ...]


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def cjson(x: Any) -> bytes:
    return json.dumps(x, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()


def digest(x: Any) -> str:
    return hashlib.sha256(cjson(x)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ident(n: int) -> Perm:
    return tuple(range(1, n + 1))


def pprod(a: Perm, b: Perm) -> Perm:
    require(len(a) == len(b), "permutation degree mismatch")
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
    require(vals, "empty paper product")
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


def build_factor_roof() -> tuple[Perm, Perm, Perm, Perm]:
    x9, y9 = make_gn(9)
    s = gf8_perm([[1, 0], [1, 1]])
    t = gf8_perm([[4, 3], [1, 5]])
    w = pprod(s, pinv(t))
    x4 = pprod(w, w)
    y4 = pprod(pprod(pinv(s), x4), s)
    return x9, y9, x4, y4


def build_roof() -> tuple[Perm, Perm]:
    x9, y9, x4, y4 = build_factor_roof()
    return direct_sum(x9, x4), direct_sum(y9, y4)


def enumerate_factor(g1: Perm, g2: Perm) -> tuple[list[Perm], dict[Perm, int], list[list[int]], list[list[int]]]:
    """Enumerate one finite factor Cayley graph exactly once.

    Edges use right multiplication by g1,g2,g1^-1,g2^-1.  The resulting
    vertex/index graph is later reused for every candidate action assignment.
    """
    gens = (g1, g2, pinv(g1), pinv(g2))
    elements = [ident(len(g1))]
    index = {elements[0]: 0}
    edges: list[list[int]] = [[]]
    words: list[list[int]] = [[]]
    letters = (1, 2, -1, -2)
    q: deque[int] = deque([0])
    while q:
        i = q.popleft()
        for k, g in enumerate(gens):
            h = pprod(elements[i], g)
            j = index.get(h)
            if j is None:
                j = len(elements)
                index[h] = j
                elements.append(h)
                edges.append([])
                words.append(words[i] + [letters[k]])
                q.append(j)
            edges[i].append(j)
    require(len(elements) == len(index), "factor enumeration index drift")
    return elements, index, edges, words


def generated_subgroup_size(gens: Iterable[Perm]) -> int:
    values = list(gens)
    if not values:
        return 1
    all_gens = values + [pinv(g) for g in values]
    one = ident(len(values[0]))
    seen = {one}
    q: deque[Perm] = deque([one])
    while q:
        cur = q.popleft()
        for g in all_gens:
            nxt = pprod(cur, g)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return len(seen)


def verify_direct_product_certificate(
    x9: Perm, y9: Perm,
    g9: list[Perm], idx9: dict[Perm, int], edges9: list[list[int]], words9: list[list[int]],
    x4: Perm, y4: Perm,
    g4: list[Perm], idx4: dict[Perm, int], edges4: list[list[int]],
) -> dict[str, int]:
    """Prove the compact roof is G9 x PSL, without enumerating that product.

    The section words for every G9 vertex lift through the compact generators.
    Each directed Cayley edge gives a Schreier relator with trivial G9
    projection.  Its PSL projection is evaluated independently; generation of
    all PSL by these kernel values proves the projection kernel is full PSL.
    Together with the two surjective factor projections this is the direct
    product criterion.
    """
    letters = (1, 2, -1, -2)
    kernel_values: list[Perm] = []
    for i, edges in enumerate(edges9):
        for k, j in enumerate(edges):
            relator = words9[i] + [letters[k]] + [-w for w in reversed(words9[j])]
            require(eval_word(relator, (x9, y9)) == ident(len(x9)),
                    "G9 Schreier relator projection is nontrivial")
            kernel_values.append(eval_word(relator, (x4, y4)))
    kernel_order = generated_subgroup_size(kernel_values)
    require(kernel_order == len(g4), "Schreier kernel does not generate PSL factor")
    return {
        "section_order": len(g9),
        "other_order": len(g4),
        "schreier_edge_count": len(kernel_values),
        "kernel_generated_order": kernel_order,
    }


def verify_factor_action(rows: list[dict[str, Any]], x9: Perm, y9: Perm,
                         x4: Perm, y4: Perm,
                         expected_certificate: Any = None) -> int:
    """Check descent/membership for all 972 actions without 972^3 work.

    For each row, images of both generators are required to lie in each
    independently enumerated factor.  Every directed Cayley edge is then
    replayed with those images; disagreement at a previously reached vertex
    is exactly a relation/well-definedness failure.
    """
    g9, idx9, edges9, words9 = enumerate_factor(x9, y9)
    g4, idx4, edges4, _ = enumerate_factor(x4, y4)
    require(len(g9) == 2916 and len(g4) == 504, "factor order enumeration drift")
    direct_product = verify_direct_product_certificate(
        x9, y9, g9, idx9, edges9, words9, x4, y4, g4, idx4, edges4)
    expected_direct_product = {
        "section_factor": "G9", "section_order": 2916, "other_order": 504,
        "schreier_edge_count": 11664, "kernel_generated_order": 504,
    }
    require(direct_product == {
        "section_order": expected_direct_product["section_order"],
        "other_order": expected_direct_product["other_order"],
        "schreier_edge_count": expected_direct_product["schreier_edge_count"],
        "kernel_generated_order": expected_direct_product["kernel_generated_order"],
    }, "direct-product Schreier certificate drift")
    require(expected_certificate == expected_direct_product,
            "serialized direct-product certificate drift")
    factor_specs = ((x9, y9, idx9, edges9), (x4, y4, idx4, edges4))
    checked = 0
    for row in rows:
        m = int(row["m"])
        f = tuple(int(v) for v in row["f"])
        f27, f9 = block(f, 0, 27), block(f, 27, 9)
        u = 2 * m + 1
        for a, b, idx, edges in factor_specs:
            ff = f27 if len(a) == 27 else f9
            ax = ppow(a, u)
            ay = paper_prod([pinv(ff), ppow(b, u), ff])
            require(ax in idx and ay in idx, "factor action image membership failure")
            target_gens = (ax, ay, pinv(ax), pinv(ay))
            images: list[Perm | None] = [None] * len(edges)
            images[0] = ident(len(a))
            q: deque[int] = deque([0])
            while q:
                i = q.popleft()
                require(images[i] is not None, "factor action image missing")
                for k, j in enumerate(edges[i]):
                    image = pprod(images[i], target_gens[k])
                    if images[j] is None:
                        images[j] = image
                        q.append(j)
                    else:
                        require(images[j] == image, "factor action edge inconsistency")
            require(all(image in idx for image in images if image is not None),
                    "factor action image left enumerated group")
        checked += 1
    return checked


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


def eval_word(word: Iterable[int], gens: tuple[Perm, Perm]) -> Perm:
    out = ident(len(gens[0]))
    for letter in word:
        require(isinstance(letter, int) and letter and abs(letter) <= 2, "bad signed word")
        g = gens[abs(letter) - 1]
        out = pprod(out, g if letter > 0 else pinv(g))
    return out


def key_for_word(word: list[int], x: Perm, y: Perm, m: int) -> list[Any]:
    f = eval_word(word, (x, y))
    p27, p9 = block(f, 0, 27), block(f, 27, 9)
    return [int(m), [d9_coords(block(p27, 9 * i, 9)) for i in range(3)], list(p9)]


def key_text(key: list[Any]) -> str:
    return "(" + str(int(key[0])) + ";" + ",".join(
        str(int(v)) for pair in key[1] for v in pair
    ) + ";" + ",".join(str(int(v)) for v in key[2]) + ")"


def load_artifact() -> list[list[Any]]:
    require(file_sha(ARTIFACT) == ARTIFACT_SHA, "artifact SHA drift")
    obj = json.loads(ARTIFACT.read_bytes())
    rows = obj.get("rows")
    require(obj.get("schema") == "d972-b4-word-key-artifact/v1" and
            obj.get("count") == 972 and isinstance(rows, list) and len(rows) == 972,
            "artifact shape drift")
    require(obj.get("canonical_bytes_sha256") == ROWS_SHA and digest(rows) == ROWS_SHA,
            "artifact row digest drift")
    require(obj.get("source_target_key_digest") == TARGET_SHA and
            obj.get("frozen_tuple_sha256") == TUPLE_SHA and
            digest([r[1] for r in rows]) == TUPLE_SHA, "artifact target digest drift")
    return rows


def search_authenticated_outside() -> str:
    for path in ROOT.joinpath("search", "certs").rglob("*.json"):
        try:
            obj = json.loads(path.read_bytes())
        except (OSError, ValueError):
            continue
        if isinstance(obj, dict) and obj.get("semantic_roof") == \
                "M=K^(9) intersect N_S4 via D972BuildBase; compact degree 36" and \
                obj.get("target_key_digest") == TARGET_SHA and \
                obj.get("source_artifact_sha256") == ARTIFACT_SHA and \
                isinstance(obj.get("outside_rows"), list) and \
                len(obj["outside_rows"]) == 648 and \
                obj.get("outside_rows_lossless") is True:
            return "AUTHENTICATED_LABEL_FOUND_BUT_NOT_CONSUMED_BY_V3"
    return "UNKNOWN_MISSING_AUTHENTICATED_LABEL"


def check_runtime_sources(receipt: dict[str, Any]) -> None:
    require(receipt.get("runtime_source_sha256") == RUNTIME_SOURCES,
            "runtime source manifest drift")
    for rel, expected in RUNTIME_SOURCES.items():
        path = ROOT / rel
        require(path.is_file() and file_sha(path) == expected,
                "runtime source hash drift: " + rel)


def compose_shadow(i: int, j: int, words: list[list[Any]], x: Perm, y: Perm) -> tuple[int, Perm]:
    m1, m2 = int(words[i][0]), int(words[j][0])
    f2 = eval_word(words[j][2], (x, y))
    u2 = 2 * m2 + 1
    a = ppow(x, u2)
    b = paper_prod([pinv(f2), ppow(y, u2), f2])
    substituted = eval_word(words[i][2], (a, b))
    return ((2 * m1 * m2 + m1 + m2) % 18, paper_prod([f2, substituted]))


def check_associativity_structure(table: list[list[int]], rows: list[dict[str, Any]],
                                  words: list[list[Any]], x: Perm, y: Perm) -> int:
    """Check h_(i*j) = h_j o h_i on both generators for every pair.

    This is the structure-derived associativity proof: h_j substitutes words,
    and the displayed equality makes the lambda/f multiplication associative.
    It does not trust the receipt's associativity fields.
    """
    n = len(rows)
    fs = [tuple(int(v) for v in row["f"]) for row in rows]
    us = [2 * int(row["m"]) + 1 for row in rows]
    actions = []
    for j in range(n):
        actions.append((ppow(x, us[j]),
                        paper_prod([pinv(fs[j]), ppow(y, us[j]), fs[j]])))
    count = 0
    for i in range(n):
        for j in range(n):
            substituted = eval_word(words[i][2], actions[j])
            p = table[i][j]
            require(us[p] % 18 == (us[i] * us[j]) % 18,
                    "associativity lambda arithmetic mismatch")
            require(ppow(x, us[p]) == ppow(actions[j][0], us[i]),
                    "associativity lambda-action mismatch")
            lhs_y = paper_prod([pinv(substituted), ppow(actions[j][1], us[i]), substituted])
            rhs_y = paper_prod([pinv(fs[p]), ppow(y, us[p]), fs[p]])
            require(lhs_y == rhs_y, "associativity generator-action mismatch")
            count += 1
    return count


def words_for_rows(rows: list[dict[str, Any]], words: list[list[Any]]) -> list[list[Any]]:
    by_key = {key_text(w[1]): w for w in words}
    return [[int(r["m"]), r["target_key"], by_key[r["target_key"]][2]] for r in rows]



def int_list_digest(values: Iterable[int]) -> str:
    payload = ",".join(str(int(v)) for v in values) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


def square_closure(
    table: list[list[int]], squares: list[int], identity: int
) -> tuple[list[int], list[list[int]]]:
    """Enumerate <squares> from identity using only the finite table."""
    n = len(table)
    require(0 <= identity < n, "square identity range")
    require(len(squares) == n, "square generator count drift")
    seen = {identity}
    queue: deque[int] = deque([identity])
    trace: list[list[int]] = []
    while queue:
        cur = queue.popleft()
        for gen in squares:
            require(0 <= int(gen) < n, "square generator range")
            nxt = int(table[cur][int(gen)])
            require(0 <= nxt < n, "square product range")
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
                trace.append([cur, int(gen), nxt])
    return sorted(seen), trace


def verify_square_subgroup(
    receipt: dict[str, Any], table: list[list[int]], square: list[int], identity: int
) -> str:
    """Authenticate the square set and the subgroup it generates independently."""
    members, trace = square_closure(table, square, identity)
    require(receipt.get("square_map") == square,
            "serialized square map mismatch")
    require(receipt.get("square_generators") == square,
            "serialized square generators mismatch")
    require(receipt.get("square_image_size") == len(set(square)),
            "square image size mismatch")
    require(receipt.get("square_generated_members") == members,
            "square generated member list mismatch")
    require(receipt.get("square_generated_order") == len(members),
            "square generated order scalar mismatch")
    require(receipt.get("square_member_digest_sha256") == int_list_digest(members),
            "square member digest mismatch")
    require(receipt.get("square_closure_seed") == identity,
            "square closure seed mismatch")
    require(receipt.get("square_closure_trace") == trace,
            "square closure witness mismatch")
    require(identity in members, "square subgroup identity missing")
    for a in members:
        inverse_ok = any(
            table[a][b] == identity and table[b][a] == identity
            for b in range(len(table))
        )
        require(inverse_ok and all(table[a][b] in members for b in members),
                "square subgroup inverse/product closure failed")
    observation = (
        "SQUARE_GENERATED_ORDER_243"
        if len(members) == 243
        else f"SQUARE_GENERATED_ORDER_OTHER_{len(members)}"
    )
    require(receipt.get("square_observation") == observation,
            "square generated order observation mismatch")
    return observation


def check(receipt_path: Path) -> dict[str, Any]:
    receipt = json.loads(receipt_path.read_bytes())
    require(receipt.get("schema") == SCHEMA, "schema gate failed")
    require(receipt.get("final_marker") == "D972_POWER_SPECTRUM_V3_GAP_FINAL" and
            receipt.get("status") == "POWER_SPECTRUM_V3_COMPLETE" and
            receipt.get("row_count") == 972, "producer completion gate failed")
    require(receipt.get("semantic_roof") ==
            "M=K^(9) intersect N_S4 via D972BuildBase; compact degree 36" and
            receipt.get("roof_order") == 1469664 and
            receipt.get("pure_quotient_order") == 1469664 and
            receipt.get("source_artifact_sha256") == ARTIFACT_SHA and
            receipt.get("source_artifact_rows_sha256") == ROWS_SHA,
            "semantic roof/source binding drift")
    check_runtime_sources(receipt)
    require(receipt.get("outside_label_status") == "UNKNOWN_MISSING_AUTHENTICATED_LABEL" and
            receipt.get("outside_rows") is None and receipt.get("outside_order_histogram") is None and
            receipt.get("outside_inference_forbidden") is True,
            "outside fail-closed gate failed")
    require(search_authenticated_outside() == "UNKNOWN_MISSING_AUTHENTICATED_LABEL",
            "outside label search found no consumable authenticated binding")
    marked = receipt.get("marked_full_compact_isomorphism")
    require(isinstance(marked, dict) and
            marked.get("source") == "Group(B.s1^2,B.s2^2)" and
            marked.get("target") == "B.compact_pure" and
            marked.get("source_generators") == ["B.s1^2", "B.s2^2"] and
            marked.get("target_images") == ["B.compact_x", "B.compact_y"] and
            marked.get("bijective") is True and
            marked.get("row_round_trip_count") == 972 and
            marked.get("block_restriction_on_full_rows") is False,
            "marked full/compact isomorphism gate failed")

    words = load_artifact()
    x9, y9, x4, y4 = build_factor_roof()
    x, y = direct_sum(x9, x4), direct_sum(y9, y4)
    rows = receipt.get("rows")
    require(isinstance(rows, list) and len(rows) == 972, "receipt rows missing")
    expected = {key_text(r[1]): (int(r[0]), r[2]) for r in words}
    require(len(expected) == 972, "artifact key collision")
    require(receipt.get("target_key_digest") == TARGET_SHA, "target digest metadata drift")
    frozen_keys = sorted(expected)
    require([r.get("target_key") for r in rows] == frozen_keys,
            "frozen row-key order drift")

    row_by_pair: dict[tuple[int, Perm], int] = {}
    row_lines: list[str] = []
    for i, row in enumerate(rows):
        require(row.get("row_index") == i and row.get("settled") is True,
                "row index/settled drift")
        key = row.get("target_key")
        require(key in expected, "unknown target key")
        m, word = expected[key]
        require(row.get("m") == m, "row m/key mismatch")
        f = tuple(int(v) for v in row.get("f", []))
        require(len(f) == 36 and set(f) == set(range(1, 37)), "lossless compact f drift")
        require(f == eval_word(word, (x, y)), "common-word roof replay mismatch")
        require(key_text(key_for_word(word, x, y, m)) == key,
                "frozen target key replay mismatch")
        row_by_pair[(m, f)] = i
        row_lines.append(f"{m}|{key}|[" + ",".join(str(v) for v in f) + "]")
    require(len(row_by_pair) == 972, "duplicate lossless shadow rows")
    factor_descent_count = verify_factor_action(
        rows, x9, y9, x4, y4, receipt.get("direct_product_certificate"))
    require(receipt.get("factor_roof_degrees") == [27, 9] and
            receipt.get("factor_group_orders") == [2916, 504] and
            receipt.get("factor_descent_count") == factor_descent_count == 972,
            "independent factor descent gate failed")

    table = receipt.get("product_table")
    require(isinstance(table, list) and len(table) == 972 and
            all(isinstance(r, list) and len(r) == 972 for r in table),
            "product table shape drift")
    row_words = words_for_rows(rows, words)
    computed: list[list[int]] = []
    for i in range(972):
        out: list[int] = []
        for j in range(972):
            m, f = compose_shadow(i, j, row_words, x, y)
            pos = row_by_pair.get((m, f))
            require(pos is not None, "independent product left row set")
            out.append(pos)
        computed.append(out)
    require(table == computed, "serialized product table mismatch")
    product_lines = [",".join(str(v) for v in r) for r in computed]
    require(receipt.get("row_digest_sha256") ==
            hashlib.sha256(("\n".join(row_lines) + "\n").encode()).hexdigest(),
            "row digest mismatch")
    require(receipt.get("product_table_sha256") ==
            hashlib.sha256(("\n".join(product_lines) + "\n").encode()).hexdigest(),
            "product digest mismatch")

    # Receipt/table indices and values are zero-based; GAP's source lists are
    # converted at the producer boundary.
    identity = int(receipt.get("identity_index", -1))
    require(0 <= identity < 972, "identity index range")
    require(all(table[identity][i] == i and table[i][identity] == i for i in range(972)),
            "identity multiplication mismatch")
    orders: list[int] = []
    inverses: list[int] = []
    for i in range(972):
        invs = [j for j, v in enumerate(table[i]) if v == identity and table[j][i] == identity]
        require(len(invs) == 1, "inverse uniqueness mismatch")
        inverses.append(invs[0])
        cur = identity
        order = None
        for n in range(1, 974):
            cur = table[cur][i]
            if cur == identity:
                order = n
                break
        require(order is not None, "exact order missing")
        orders.append(order)
    require(receipt.get("orders") == orders and receipt.get("inverse_indices") == inverses,
            "serialized order/inverse mismatch")
    require(receipt.get("order_histogram") ==
            [[int(k), int(v)] for k, v in sorted(Counter(orders).items())],
            "serialized order histogram mismatch")

    square = [table[i][i] for i in range(972)]
    cube = [table[square[i]][i] for i in range(972)]
    exponent = 1
    for order in orders:
        a, b = exponent, order
        while b:
            a, b = b, a % b
        exponent = exponent * order // a
    require(receipt.get("square_map") == square and receipt.get("cube_map") == cube and
            receipt.get("exponent") == exponent, "power-spectrum map/exponent mismatch")
    square_observation = verify_square_subgroup(receipt, table, square, identity)

    assoc_count = check_associativity_structure(table, rows, row_words, x, y)
    require(assoc_count == 972 * 972 and
            receipt.get("associativity_pair_count") == assoc_count,
            "independent associativity structure check mismatch")
    require(receipt.get("orientation_canaries") == {
        "paper_product_is_gap_reverse": True, "lambda_product": True, "identity": True
    }, "orientation canary metadata drift")
    return {"status": "D972_POWER_SPECTRUM_V3_CHECKER_PASS", "row_count": 972,
            "exponent": exponent, "square_observation": square_observation,
            "square_generated_order": len(set(receipt["square_generated_members"])),
            "outside_label_status": receipt["outside_label_status"]}


def self_test() -> None:
    p = (2, 3, 1)
    q = (1, 3, 2)
    require(paper_prod([p, q]) == pprod(q, p), "paper orientation self-test")
    require((2 * (2 * 1 * 2 + 1 + 2) + 1) % 18 ==
            ((2 * 1 + 1) * (2 * 2 + 1)) % 18, "lambda self-test")
    table = [[0, 1], [1, 0]]
    tiny_identity = 0
    tiny_orders = []
    for i in range(2):
        cur = tiny_identity
        for n in range(1, 3):
            cur = table[cur][i]
            if cur == tiny_identity:
                break
        require(cur == tiny_identity, "zero-based identity/order self-test")
        tiny_orders.append(n)
    require(tiny_orders == [1, 2], "zero-based order convention self-test")
    square = [table[i][i] for i in range(2)]
    cube = [table[square[i]][i] for i in range(2)]
    require(square == [0, 0] and cube == [0, 1], "power-map self-test")
    tiny = {
        "square_map": [0, 0],
        "square_generators": [0, 0],
        "square_image_size": 1,
        "square_generated_members": [0],
        "square_generated_order": 1,
        "square_member_digest_sha256": int_list_digest([0]),
        "square_closure_seed": 0,
        "square_closure_trace": [],
        "square_observation": "SQUARE_GENERATED_ORDER_OTHER_1",
    }
    verify_square_subgroup(tiny, table, square, tiny_identity)
    bad_square_map = copy.deepcopy(tiny)
    bad_square_map["square_map"][0] = 1
    try:
        verify_square_subgroup(bad_square_map, table, square, tiny_identity)
    except ValueError:
        pass
    else:
        raise AssertionError("square-map cell mutation accepted")
    bad_square = copy.deepcopy(tiny)
    bad_square["square_generators"][0] = 1
    try:
        verify_square_subgroup(bad_square, table, square, tiny_identity)
    except ValueError:
        pass
    else:
        raise AssertionError("square-map mutation accepted")
    bad_member = copy.deepcopy(tiny)
    bad_member["square_generated_members"] = [1]
    try:
        verify_square_subgroup(bad_member, table, square, tiny_identity)
    except ValueError:
        pass
    else:
        raise AssertionError("square-member mutation accepted")
    bad_table = copy.deepcopy(table)
    bad_table[0][0] = 1
    try:
        verify_square_subgroup(tiny, bad_table, square, tiny_identity)
    except ValueError:
        pass
    else:
        raise AssertionError("product-table mutation accepted")
    bad_order = copy.deepcopy(tiny)
    bad_order["square_generated_order"] = 2
    try:
        verify_square_subgroup(bad_order, table, square, tiny_identity)
    except ValueError:
        pass
    else:
        raise AssertionError("forged square order accepted")
    print("D972_POWER_SPECTRUM_V3_CHECKER_SELFTEST_PASS")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", type=Path, default=Path("ci/out/d972_power_spectrum_v3.json"))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    result = check(args.receipt)
    print(json.dumps(result, sort_keys=True))
    print("D972_POWER_SPECTRUM_V3_CHECKER_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
