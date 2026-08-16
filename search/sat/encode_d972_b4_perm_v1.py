#!/usr/bin/env python3
"""Encode one bounded permutation-action B4 roof target as DIMACS CNF.

The encoder is deliberately data-driven: the 158 signed U_M relators and the
independently produced 972-row word/key artifact are required inputs.  It does
not import GAP or the producer.  A missing or malformed artifact is a hard
error, never an implicit empty target.  The CNF uses six d-by-d permutation
matrices, relator identity constraints, rho^5 constraints, and one selected
roof row (or a distinct-row OR shard) with a non-identity defect disjunction.

This is a bounded finite-image candidate search.  SAT/UNSAT at degree d has no
implication for the universal A/B question beyond that degree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Iterable, Sequence

RELATOR_SHA256 = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
TARGET_KEY_SHA256 = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
FROZEN_TUPLE_SHA256 = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
P2_INPUT_SCHEMA = "d972-b4-p2-magnus-input/v2"
P2_INPUT_SHA256 = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RHO_WORDS_SOURCE = "universal_v2_canonical"
RHO_WORDS_SHA256 = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
RHO = [
    [-6, -5, -3], [3], [5], [-3, -2, -1], [-5, -4, -1], [1]
]


def cjson(x: object) -> bytes:
    return json.dumps(x, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha(x: object) -> str:
    return hashlib.sha256(cjson(x)).hexdigest()


def check_word(w: object, where: str) -> list[int]:
    if not isinstance(w, list) or any(not isinstance(x, int) or x == 0 or abs(x) > 6 for x in w):
        raise ValueError(f"{where}: expected signed F2 letters in [-6,-1] U [1,6]")
    return list(w)


def load_relators(path: Path) -> tuple[list[list[int]], str]:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != P2_INPUT_SHA256:
        raise ValueError("relator input file SHA-256 is not the pinned v2 artifact")
    obj = json.loads(raw.decode("utf-8"))
    if (not isinstance(obj, dict) or obj.get("schema") != P2_INPUT_SCHEMA or
            obj.get("rho_words_source") != RHO_WORDS_SOURCE or
            obj.get("rho_words") != RHO):
        raise ValueError("relator input schema/rho source is not canonical v2")
    rows = obj.get("relators", obj.get("all_relators"))
    if not isinstance(rows, list) or len(rows) != 158:
        raise ValueError("relator input must contain exactly 158 relators")
    rels = [check_word(w, f"relator[{i}]") for i, w in enumerate(rows)]
    digest = sha(rels)
    if digest != RELATOR_SHA256:
        raise ValueError(f"relator digest mismatch: {digest}")
    return rels, digest


def load_word_keys(path: Path) -> tuple[list[list[object]], str, str]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    rows = obj.get("rows") if isinstance(obj, dict) else obj
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word/key artifact must contain exactly 972 rows")
    canonical = sha(rows)
    declared = obj.get("canonical_bytes_sha256") if isinstance(obj, dict) else None
    if declared != canonical:
        raise ValueError("word/key artifact canonical digest mismatch")
    target_digest = obj.get("source_target_key_digest") if isinstance(obj, dict) else None
    if target_digest != TARGET_KEY_SHA256:
        raise ValueError("word/key artifact is not bound to the frozen 972 target set")
    if obj.get("frozen_tuple_sha256") != FROZEN_TUPLE_SHA256:
        raise ValueError("word/key artifact frozen tuple digest mismatch")
    out: list[list[object]] = []
    for i, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"word/key row {i}: expected [m,key,word]")
        m, key, word = row
        if not isinstance(m, int) or not isinstance(key, list):
            raise ValueError(f"word/key row {i}: malformed m/key")
        out.append([m, key, check_word(word, f"word-key[{i}]")])
    return out, canonical, target_digest


def substitute(word: Sequence[int], rho: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        atom = list(rho[abs(letter) - 1])
        if letter < 0:
            atom = [-x for x in reversed(atom)]
        out.extend(atom)
    return out


def rho_power_words(t: int) -> list[list[int]]:
    out = [[i] for i in range(1, 7)]
    for _ in range(t):
        out = [substitute(w, RHO) for w in out]
    return out


class CNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def add(self, *lits: int) -> None:
        self.clauses.append(list(lits))

    def unit(self, lit: int) -> None:
        self.add(lit)

    def exactly_one(self, xs: Sequence[int]) -> None:
        if not xs:
            self.add()
            return
        self.add(*xs)
        for i in range(len(xs)):
            for j in range(i):
                self.add(-xs[i], -xs[j])

    def write(self, path: Path, comments: Iterable[str]) -> None:
        with path.open("w", encoding="ascii", newline="\n") as f:
            for line in comments:
                f.write(f"c {line}\n")
            f.write(f"p cnf {self.nvars} {len(self.clauses)}\n")
            for clause in self.clauses:
                f.write(" ".join(str(x) for x in clause) + " 0\n")


class PermEncoding:
    def __init__(self, degree: int, cnf: CNF) -> None:
        self.d = degree
        self.c = cnf
        self.x = [[[cnf.var() for _ in range(degree)] for _ in range(degree)] for _ in range(6)]
        for g in range(6):
            for i in range(degree):
                cnf.exactly_one(self.x[g][i])
            for j in range(degree):
                cnf.exactly_one([self.x[g][i][j] for i in range(degree)])

    def transition(self, prev: list[int], letter: int) -> list[int]:
        """One-hot state transition from a permutation-table row.

        The reverse table implication is redundant: ``prev`` and ``nxt`` are
        one-hot, and each generator row (or inverse column) is one-hot.  The
        forward implications therefore force exactly the unique next state;
        omitting the duplicate implication roughly halves the degree-8 CNF
        while preserving the relation exactly.
        """
        nxt = [self.c.var() for _ in range(self.d)]
        g = self.x[abs(letter) - 1]
        for a in range(self.d):
            for b in range(self.d):
                edge = g[a][b] if letter > 0 else g[b][a]
                # prev[a] & edge => nxt[b].
                self.c.add(-prev[a], -edge, nxt[b])
        return nxt

    def word_paths(self, word: Sequence[int], force_identity: bool = False) -> list[list[int]]:
        """Return final one-hot rows, one for each starting point."""
        finals: list[list[int]] = []
        for src in range(self.d):
            state = [self.c.var() for _ in range(self.d)]
            self.c.exactly_one(state)
            self.c.unit(state[src])
            for letter in word:
                state = self.transition(state, letter)
                self.c.exactly_one(state)
            finals.append(state)
            if force_identity:
                for dst, bit in enumerate(state):
                    self.c.unit(bit if dst == src else -bit)
        return finals

    def force_word_identity(self, word: Sequence[int]) -> None:
        self.word_paths(word, force_identity=True)

    def defect_word(self, word: Sequence[int]) -> list[list[int]]:
        return self.word_paths(word, force_identity=False)


def embed_f2_word(target_word: Sequence[int]) -> list[int]:
    """Mark the F2 roof word into U_M: j(x)=U_1 and j(y)=U_4."""
    out: list[int] = []
    for letter in target_word:
        if letter == 1:
            out.append(1)
        elif letter == -1:
            out.append(-1)
        elif letter == 2:
            out.append(4)
        elif letter == -2:
            out.append(-4)
        else:
            raise ValueError(f"F2 roof word has invalid letter {letter}")
    return out


def selected_roof_word(target_word: Sequence[int]) -> list[int]:
    factors: list[int] = []
    # q∘rho^4, ..., q∘rho^0; composition in the GAP/right-action order is
    # represented by concatenating the five substituted F2 words in order.
    marked_word = embed_f2_word(target_word)
    for t in reversed(range(5)):
        factors.extend(substitute(marked_word, rho_power_words(t)))
    return factors


def _validate_target_indices(rows: list[list[object]], target_indices: Sequence[int]) -> list[int]:
    indices = [int(x) for x in target_indices]
    if not indices:
        raise ValueError("target index list must not be empty")
    if len(set(indices)) != len(indices):
        raise ValueError("target index list contains duplicates")
    if any(not 0 <= i < len(rows) for i in indices):
        raise ValueError("target index outside word-key artifact")
    return indices


def encode_targets(
    degree: int,
    relators: list[list[int]],
    rows: list[list[object]],
    target_indices: Sequence[int],
) -> tuple[CNF, dict[str, object]]:
    if degree < 2 or degree > 8:
        raise ValueError("degree must be in [2,8]")
    indices = _validate_target_indices(rows, target_indices)
    c = CNF()
    p = PermEncoding(degree, c)
    for rel in relators:
        p.force_word_identity(rel)
    # rho^5(g_i)=g_i is checked on all points for each named generator.
    for i in range(6):
        p.force_word_identity(rho_power_words(5)[i] + [-(i + 1)])
    moved: list[int] = []
    roofs: list[list[int]] = []
    selected_words: list[list[int]] = []
    for target_index in indices:
        target_word = rows[target_index][2]
        assert isinstance(target_word, list)
        selected_words.append(target_word)
        roof = selected_roof_word(target_word)
        roofs.append(roof)
        final = p.defect_word(roof)
        moved.extend(final[src][dst] for src in range(degree)
                     for dst in range(degree) if dst != src)
    if len({tuple(word) for word in selected_words}) != len(selected_words):
        raise ValueError("OR target indices must represent distinct roof words")
    c.add(*moved)
    manifest: dict[str, object] = {
        "schema": ("d972-b4-permutation-sat-or/v1" if len(indices) > 1
                    else "d972-b4-permutation-sat/v1"),
        "degree": degree, "relator_count": len(relators),
        "relator_sha256": sha(relators), "target_row_count": len(rows),
        "target_indices": indices,
        "target_keys": [rows[i][1] for i in indices],
        "target_words": [rows[i][2] for i in indices],
        "target_count": len(indices),
        "target_artifact_sha256": sha(rows),
        "target_key_digest": TARGET_KEY_SHA256, "rho_words": RHO,
        "rho_words_source": RHO_WORDS_SOURCE,
        "rho_words_sha256": RHO_WORDS_SHA256,
        "p2_input_schema": P2_INPUT_SCHEMA,
        "p2_input_file_sha256": P2_INPUT_SHA256,
        "frozen_tuple_sha256": FROZEN_TUPLE_SHA256,
        "roof_order": [4, 3, 2, 1, 0], "roof_words": roofs,
        "nvars": c.nvars, "clauses": len(c.clauses),
        "interpretation": "SAT is a finite-degree candidate; UNSAT excludes only this degree and selected roof shard.",
    }
    if len(indices) == 1:
        manifest["target_index"] = indices[0]
        manifest["target_key"] = rows[indices[0]][1]
        manifest["target_word"] = rows[indices[0]][2]
        manifest["roof_word"] = roofs[0]
    return c, manifest


def encode(degree: int, relators: list[list[int]], rows: list[list[object]], target_index: int) -> tuple[CNF, dict[str, object]]:
    return encode_targets(degree, relators, rows, [target_index])


def _tiny_eval(word: Sequence[int], gens: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
    out = tuple(range(1, len(gens[0]) + 1))
    for x in word:
        g = gens[abs(x) - 1]
        if x < 0:
            inv = [0] * len(g)
            for i, y in enumerate(g, 1):
                inv[y - 1] = i
            g = tuple(inv)
        out = tuple(g[y - 1] for y in out)
    return out


def self_test() -> None:
    """Small semantic regression test; no artifact or solver is needed."""
    gens = [(2, 1)] * 6
    rho5 = rho_power_words(5)
    assert all(_tiny_eval(w, gens) == gens[i] for i, w in enumerate(rho5))
    # Regression: rho^5(g_i) is not generally identity; the encoded relation
    # must append g_i^-1.  The old bare-word bug fails this assertion.
    assert _tiny_eval(rho5[0], gens) != (1, 2)
    assert _tiny_eval(rho5[0] + [-1], gens) == (1, 2)
    assert _tiny_eval(selected_roof_word([1]), gens) == (2, 1)
    assert embed_f2_word([1, -2, 2, -1]) == [1, -4, 4, -1]
    asymmetric = [(2, 1, 3), (1, 3, 2), (2, 3, 1),
                  (3, 2, 1), (1, 2, 3), (3, 1, 2)]
    expected_y: list[int] = []
    old_y: list[int] = []
    for t in reversed(range(5)):
        expected_y.extend(substitute([4], rho_power_words(t)))
        old_y.extend(substitute([2], rho_power_words(t)))
    assert selected_roof_word([2]) == expected_y
    assert selected_roof_word([2]) != old_y
    assert _tiny_eval(selected_roof_word([1]), asymmetric) != \
        _tiny_eval(selected_roof_word([2]), asymmetric)
    c, m = encode(2, [], [[0, [], [1]]], 0)
    assert c.nvars == 1648 and len(c.clauses) == 4903
    assert m["roof_order"] == [4, 3, 2, 1, 0]
    c_or, m_or = encode_targets(2, [], [[0, [], [1]], [0, [], [2]]], [0, 1])
    assert m_or["schema"] == "d972-b4-permutation-sat-or/v1"
    assert m_or["target_indices"] == [0, 1]
    assert len(c_or.clauses) > len(c.clauses)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--degree", type=int, default=6)
    ap.add_argument("--relators", type=Path)
    ap.add_argument("--word-key-artifact", type=Path)
    ap.add_argument("--target-index", type=int, default=0)
    ap.add_argument("--target-indices", help="comma-separated target row indices for a sound OR shard")
    ap.add_argument("--out-prefix", type=Path)
    args = ap.parse_args(argv)
    if args.self_test:
        self_test()
        print("D972_B4_SAT_ENCODER_SELFTEST_PASS")
        return 0
    if args.relators is None or args.word_key_artifact is None:
        ap.error("--relators and --word-key-artifact are required unless --self-test is used")
    if args.out_prefix is None:
        ap.error("--out-prefix is required unless --self-test is used")
    rels, rel_sha = load_relators(args.relators)
    rows, artifact_sha, _ = load_word_keys(args.word_key_artifact)
    if args.target_indices is None:
        target_indices = [args.target_index]
    else:
        try:
            target_indices = [int(x) for x in args.target_indices.split(",") if x.strip()]
        except ValueError as exc:
            raise ValueError("--target-indices must be comma-separated integers") from exc
    cnf, manifest = encode_targets(args.degree, rels, rows, target_indices)
    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    cnf_path = args.out_prefix.with_suffix(".cnf")
    manifest_path = args.out_prefix.with_suffix(".manifest.json")
    cnf.write(cnf_path, [str(manifest["schema"]), json.dumps(manifest, sort_keys=True)])
    manifest["cnf_sha256"] = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"cnf": str(cnf_path), "manifest": str(manifest_path),
                      "cnf_sha256": manifest["cnf_sha256"], "nvars": cnf.nvars,
                      "clauses": len(cnf.clauses), "relator_sha256": rel_sha,
                      "artifact_sha256": artifact_sha}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
