#!/usr/bin/env python3
"""Degree-four Magnus search for the raw A.18 B4 presentation.

This is deliberately a new lane: its presentation is the 18 K05 rows plus
the 140 literal A.18 images, and its 972 words are the unconditional
PENT-FORM' D-tilde words.  It never constructs the older reverse-rho norm.
The ordinary index-32 C2^5 Schreier presentation is reduced over F3.  A
nonzero degree-four dual functional is a finite obstruction candidate;
all-pass remains UNKNOWN and is never promoted to B.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
DEFAULT_WORDS = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"

SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
A18_ROWS_SHA = "1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722"
PRESENTATION_SHA = "783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305"
DTILDE_SHA = "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef"
DTILDE_RS_SHA = "418e88934210e726de0e7e1f375bac2e6151f465be84f913884c58129217259c"
RAW_RS_SHA = "db25c0268cdc774ef3205c9c1d1cf62cd013e6daaf73cf959e7972af5b3082bb"
RHO_SHA = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
GEN_BITS = (1, 2, 4, 8, 16, 31)
MAPS = (
    ("123", (1,), (4,)),
    ("234", (4,), (6,)),
    ("12,3,4", (2, 4), (6,)),
    ("1,23,4", (1, 2), (5, 6)),
    ("1,2,34", (1,), (4, 5)),
)

MOD = 3
D = 7
D2 = D * D
D3 = D2 * D
D4 = D3 * D
QDIM = 5
PARAM = QDIM * D2
WIDTH = 161


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        if letter == 0:
            raise ValueError("zero signed letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: list[int]) -> list[int]:
    return [-x for x in reversed(word)]


def marked_substitute(word: list[int], first: list[int], second: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if abs(letter) not in (1, 4):
            raise ValueError("marked F6 alphabet drift")
        image = first if abs(letter) == 1 else second
        out.extend(inverse_word(image) if letter < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2: list[int]) -> list[int]:
    marked: list[int] = []
    for letter in f2:
        if abs(letter) not in (1, 2):
            raise ValueError("roof F2 alphabet drift")
        marked.append((1 if letter > 0 else -1) if abs(letter) == 1
                      else (4 if letter > 0 else -4))
    x15, x45 = [-3, -2, -1], [-6, -5, -3]
    # W45^-1 W12^-1 W23 W51 W123, the unconditional PENT-FORM'.
    return free_reduce(
        inverse_word(marked_substitute(marked, x45, [6])) +
        inverse_word(marked_substitute(marked, [1], x15)) +
        marked_substitute(marked, [4], [6]) +
        marked_substitute(marked, x45, x15) +
        marked_substitute(marked, [1], [4]))


def load_inputs(source_path: Path, words_path: Path) -> tuple[list[list[int]], list[list[int]], str]:
    source_raw = source_path.read_bytes()
    if hashlib.sha256(source_raw).hexdigest() != SOURCE_SHA:
        raise ValueError("canonical source SHA drift")
    source = json.loads(source_raw.decode("utf-8"))
    if (source.get("schema") != "d972-b4-p2-magnus-input/v2" or
            source.get("relator_count") != 158 or
            source.get("rho_words") != [list(x) for x in RHO] or
            source.get("rho_words_source") != "universal_v2_canonical" or
            source.get("all_relators_sha256") != RELATOR_SHA):
        raise ValueError("canonical source contract drift")
    relators = [[int(x) for x in row] for row in source["all_relators"]]
    if len(relators) != 158 or digest(relators) != RELATOR_SHA:
        raise ValueError("canonical relator digest drift")
    seeds = relators[18:46]
    a18: list[list[int]] = []
    for _name, first, second in MAPS:
        a18.extend(marked_substitute(row, list(first), list(second)) for row in seeds)
    if len(a18) != 140 or digest(a18) != A18_ROWS_SHA:
        raise ValueError("raw A18 row digest drift")
    presentation = relators[:18] + a18
    if len(presentation) != 158 or digest(presentation) != PRESENTATION_SHA:
        raise ValueError("raw A18 presentation digest drift")

    words_raw = words_path.read_bytes()
    if hashlib.sha256(words_raw).hexdigest() != WORDS_SHA:
        raise ValueError("word artifact SHA drift")
    words = json.loads(words_raw.decode("utf-8"))
    if (words.get("schema") != "d972-b4-word-key-artifact/v1" or
            words.get("count") != 972 or len(words.get("rows", [])) != 972):
        raise ValueError("word artifact contract drift")
    f2_rows: list[list[int]] = []
    for index, row in enumerate(words["rows"]):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError("word row shape drift")
        word = row[2]
        if word == "":
            if index not in (0, 891):
                raise ValueError("unexpected legacy empty word")
            word = []
        if not isinstance(word, list):
            raise ValueError("word row type drift")
        f2_rows.append([int(x) for x in word])
    dtilde = [exact_dtilde(row) for row in f2_rows]
    if digest(dtilde) != DTILDE_SHA:
        raise ValueError("Dtilde digest drift")
    return presentation, dtilde, hashlib.sha256(words_raw).hexdigest()


def transversal(mask: int) -> list[int]:
    return [i + 1 for i in range(5) if mask & (1 << i)]


def toggle(mask: int, bit: int) -> int:
    return 31 - mask if bit == 31 else mask ^ bit


def schreier_pairs() -> tuple[dict[tuple[int, int], int | None], list[list[int]]]:
    pair_id: dict[tuple[int, int], int | None] = {}
    pair_words: list[list[int]] = []
    for mask in range(32):
        for gen, bit in enumerate(GEN_BITS, 1):
            word = free_reduce(transversal(mask) + [gen] +
                               inverse_word(transversal(toggle(mask, bit))))
            if word:
                pair_id[(mask, gen)] = len(pair_words) + 1
                pair_words.append(word)
            else:
                pair_id[(mask, gen)] = None
    if len(pair_words) != WIDTH:
        raise ValueError("Schreier generator count drift")
    return pair_id, pair_words


def rewrite(word: list[int], pair_id: dict[tuple[int, int], int | None], start: int = 0) -> tuple[list[int], int]:
    mask, out = start, []
    for letter in word:
        gen, bit = abs(letter), GEN_BITS[abs(letter) - 1]
        if letter > 0:
            ident = pair_id[(mask, gen)]
            if ident is not None:
                out.append(ident)
            mask = toggle(mask, bit)
        else:
            mask = toggle(mask, bit)
            ident = pair_id[(mask, gen)]
            if ident is not None:
                out.append(-ident)
    return free_reduce(out), mask


def build_rs(relators: list[list[int]]) -> tuple[list[list[int]], dict[tuple[int, int], int | None], list[list[int]]]:
    pair_id, pair_words = schreier_pairs()
    rows: list[list[int]] = []
    for start in range(32):
        for relator in relators:
            row, end = rewrite(relator, pair_id, start)
            if end != start:
                raise ValueError("presentation relator leaves C2^5")
            if row:
                rows.append(row)
    if len(rows) != 5056 or digest(rows) != RAW_RS_SHA:
        raise ValueError("raw A18 RS relator digest drift")
    return rows, pair_id, pair_words


def rewrite_words(words: list[list[int]], pair_id: dict[tuple[int, int], int | None]) -> list[list[int]]:
    result: list[list[int]] = []
    for word in words:
        row, end = rewrite(word, pair_id, 0)
        if end != 0:
            raise ValueError("Dtilde leaves C2^5")
        result.append(row)
    if len(result) != 972 or digest(result) != DTILDE_RS_SHA:
        raise ValueError("Dtilde RS digest drift")
    return result


def exponent_vector(word: list[int], width: int = WIDTH) -> list[int]:
    vector = [0] * width
    for letter in word:
        vector[abs(letter) - 1] = (vector[abs(letter) - 1] +
                                   (1 if letter > 0 else -1)) % MOD
    return vector


def sparse_basis(rows: list[list[int]], width: int) -> dict[int, dict[int, int]]:
    basis: dict[int, dict[int, int]] = {}
    for raw in rows:
        row = {i: int(value) % MOD for i, value in enumerate(raw) if int(value) % MOD}
        while row:
            pivot = min(row)
            prior = basis.get(pivot)
            if prior is None:
                inv = 1 if row[pivot] == 1 else 2
                basis[pivot] = {i: inv * value % MOD for i, value in row.items()}
                break
            factor = row[pivot]
            for i, value in prior.items():
                residue = (row.get(i, 0) - factor * value) % MOD
                if residue:
                    row[i] = residue
                else:
                    row.pop(i, None)
    return basis


def nullspace(basis: dict[int, dict[int, int]], width: int) -> list[list[int]]:
    pivots = sorted(basis)
    pivot_set = set(pivots)
    result: list[list[int]] = []
    for free in [i for i in range(width) if i not in pivot_set]:
        vector = [0] * width
        vector[free] = 1
        for pivot in reversed(pivots):
            vector[pivot] = (-sum(value * vector[i] for i, value in basis[pivot].items()
                                   if i > pivot)) % MOD
        result.append(vector)
    return result


def magnus3(word: list[int], columns: list[list[int]]) -> tuple[list[int], list[int], list[int]]:
    linear = [0] * D
    quadratic = [0] * D2
    cubic = [0] * D3
    for letter in word:
        p = columns[abs(letter) - 1]
        if letter < 0:
            for qindex, qvalue in enumerate(quadratic):
                if qvalue:
                    for j, pv in enumerate(p):
                        cubic[qindex * D + j] = (cubic[qindex * D + j] - qvalue * pv) % MOD
            for i, lv in enumerate(linear):
                if lv:
                    for j, a in enumerate(p):
                        if a:
                            for k, b in enumerate(p):
                                if b:
                                    cubic[(i * D + j) * D + k] = (
                                        cubic[(i * D + j) * D + k] + lv * a * b) % MOD
            for i, a in enumerate(p):
                if a:
                    for j, b in enumerate(p):
                        if b:
                            for k, c in enumerate(p):
                                if c:
                                    index = (i * D + j) * D + k
                                    cubic[index] = (cubic[index] - a * b * c) % MOD
            for i, lv in enumerate(linear):
                if lv:
                    for j, pv in enumerate(p):
                        quadratic[i * D + j] = (quadratic[i * D + j] - lv * pv) % MOD
            for i, a in enumerate(p):
                if a:
                    for j, b in enumerate(p):
                        if b:
                            quadratic[i * D + j] = (quadratic[i * D + j] + a * b) % MOD
            linear = [(a - b) % MOD for a, b in zip(linear, p)]
        else:
            for qindex, qvalue in enumerate(quadratic):
                if qvalue:
                    for j, pv in enumerate(p):
                        cubic[qindex * D + j] = (cubic[qindex * D + j] + qvalue * pv) % MOD
            for i, lv in enumerate(linear):
                if lv:
                    for j, pv in enumerate(p):
                        quadratic[i * D + j] = (quadratic[i * D + j] + lv * pv) % MOD
            linear = [(a + b) % MOD for a, b in zip(linear, p)]
    return linear, quadratic, cubic


def project3(cubic: list[int], q_perp: list[list[int]]) -> list[int]:
    return np.einsum("aij,ijk->ak", np.asarray(q_perp, dtype=np.int16).reshape(QDIM, D, D),
                     np.asarray(cubic, dtype=np.int16).reshape(D, D, D), optimize=True).astype(int).reshape(-1).tolist()


def prepare4(columns: list[list[int]], q_perp: list[list[int]]) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    qpa = np.asarray(q_perp, dtype=np.int16).reshape(QDIM, D, D)
    pvec = [np.asarray(x, dtype=np.int16) % MOD for x in columns]
    lmap = [np.einsum("aij,j->ai", qpa, p, optimize=True).astype(np.int16) for p in pvec]
    ppmap = [np.einsum("aij,i,j->a", qpa, p, p, optimize=True).astype(np.int16) for p in pvec]
    return pvec, lmap, ppmap


def collect4(word: list[int], q_perp: list[list[int]], pvec: list[np.ndarray],
             lmap: list[np.ndarray], ppmap: list[np.ndarray]) -> list[int]:
    qpa = np.asarray(q_perp, dtype=np.int16).reshape(QDIM, D2)
    linear = np.zeros(D, dtype=np.int16)
    quadratic = np.zeros(D2, dtype=np.int16)
    cubic = np.zeros(QDIM * D, dtype=np.int16)
    degree4 = np.zeros(PARAM, dtype=np.int16)
    for letter in word:
        p = pvec[abs(letter) - 1]
        lp = lmap[abs(letter) - 1] @ linear % MOD
        qproj = qpa @ quadratic % MOD
        pp = ppmap[abs(letter) - 1]
        p2 = np.outer(p, p) % MOD
        if letter > 0:
            degree4 = (degree4.reshape(QDIM, D, D) +
                       cubic.reshape(QDIM, D, 1) * p.reshape(1, 1, D)) % MOD
            cubic = (cubic.reshape(QDIM, D) +
                     qproj.reshape(QDIM, 1) * p.reshape(1, D)) % MOD
            quadratic = (quadratic + np.outer(linear, p).reshape(-1)) % MOD
            linear = (linear + p) % MOD
        else:
            degree4 = (degree4.reshape(QDIM, D, D) -
                       cubic.reshape(QDIM, D, 1) * p.reshape(1, 1, D) +
                       qproj.reshape(QDIM, 1, 1) * p2.reshape(1, D, D) -
                       lp.reshape(QDIM, 1, 1) * p2.reshape(1, D, D) +
                       pp.reshape(QDIM, 1, 1) * p2.reshape(1, D, D)) % MOD
            cubic = (cubic.reshape(QDIM, D) -
                     qproj.reshape(QDIM, 1) * p.reshape(1, D) +
                     lp.reshape(QDIM, 1) * p.reshape(1, D) -
                     pp.reshape(QDIM, 1) * p.reshape(1, D)) % MOD
            quadratic = (quadratic - np.outer(linear, p).reshape(-1) + p2.reshape(-1)) % MOD
            linear = (linear - p) % MOD
        cubic = cubic.reshape(-1)
        degree4 = degree4.reshape(-1)
    if np.any(linear):
        raise ValueError("degree-four collector linear drift")
    return degree4.astype(int).tolist()


def constraint_rows(q_basis: list[list[int]], q_perp: list[list[int]],
                    cubic_basis: list[list[int]]) -> list[list[int]]:
    qpa = np.asarray(q_perp, dtype=np.int16).reshape(QDIM, D, D)
    rows: list[list[int]] = []
    for i in range(D):
        for q in q_basis:
            contraction = np.einsum("ab,bj->aj", qpa[:, i, :],
                                    np.asarray(q, dtype=np.int16).reshape(D, D), optimize=True)
            for k in range(D):
                row = np.zeros((QDIM, D, D), dtype=np.int16)
                row[:, :, k] = contraction
                rows.append(row.reshape(-1).astype(int).tolist())
    for a in range(QDIM):
        for q in q_basis:
            row = [0] * PARAM
            row[a * D2:(a + 1) * D2] = [int(x) for x in q]
            rows.append(row)
    for cubic in cubic_basis:
        projected = project3(cubic, q_perp)
        for k in range(D):
            row = [0] * PARAM
            for j, value in enumerate(projected):
                row[(j // D) * D2 + (j % D) * D + k] = value
            rows.append(row)
    for cubic in cubic_basis:
        tensor = np.asarray(cubic, dtype=np.int16).reshape(D, D, D)
        for i in range(D):
            rows.append(np.einsum("ab,bjk->ajk", qpa[:, i, :], tensor,
                                  optimize=True).reshape(-1).astype(int).tolist())
    return rows


def selftest(source: Path, words: Path) -> None:
    presentation, dtilde, raw_sha = load_inputs(source, words)
    if len(presentation) != 158 or len(dtilde) != 972:
        raise ValueError("A18 count selftest drift")
    rs, pair_id, pairs = build_rs(presentation)
    dtilde_rs = rewrite_words(dtilde, pair_id)
    if len(pairs) != WIDTH or len(rs) != 5056 or digest(rs) != RAW_RS_SHA:
        raise ValueError("A18 RS selftest drift")
    if digest(dtilde_rs) != DTILDE_RS_SHA or not raw_sha:
        raise ValueError("A18 Dtilde RS selftest drift")
    print("D972_B4_U_MAGNUS4_A18_SELFTEST_PASS")


def run(presentation: list[list[int]], dtilde: list[list[int]]) -> dict[str, Any]:
    rs_words, pair_id, pair_words = build_rs(presentation)
    dtilde_rs = rewrite_words(dtilde, pair_id)
    rel_vectors = [exponent_vector(row) for row in rs_words]
    linear_basis = sparse_basis(rel_vectors, WIDTH)
    linear_null = nullspace(linear_basis, WIDTH)
    if len(linear_null) != D:
        raise ValueError("raw A18 linear dimension drift")
    columns = [[linear_null[j][i] for j in range(D)] for i in range(WIDTH)]
    rel_q: list[list[int]] = []
    rel_c: list[list[int]] = []
    for row in rs_words:
        linear, quadratic, cubic = magnus3(row, columns)
        if any(linear):
            raise ValueError("RS relator linear term drift")
        rel_q.append(quadratic)
        rel_c.append(cubic)
    norm_q: list[list[int]] = []
    for row in dtilde_rs:
        linear, quadratic, _ = magnus3(row, columns)
        if any(linear):
            raise ValueError("Dtilde linear term drift")
        norm_q.append(quadratic)
    q_basis = sparse_basis(rel_q, D2)
    q_perp = nullspace(q_basis, D2)
    if len(q_basis) != 44 or len(q_perp) != QDIM:
        raise ValueError("raw A18 degree-two dimensions drift")
    pvec, lmap, ppmap = prepare4(columns, q_perp)
    print("B4_MAGNUS4_A18_COLLECT_BEGIN relators=", len(rs_words),
          " norms=", len(dtilde_rs), flush=True)
    rel_d = [collect4(row, q_perp, pvec, lmap, ppmap) for row in rs_words]
    norm_d = [collect4(row, q_perp, pvec, lmap, ppmap) for row in dtilde_rs]
    cubic_basis_sparse = sparse_basis(rel_c, D3)
    cubic_basis: list[list[int]] = []
    for _, sparse_row in sorted(cubic_basis_sparse.items()):
        row = [0] * D3
        for index, value in sparse_row.items():
            row[index] = value
        cubic_basis.append(row)
    constraints = constraint_rows(q_basis, q_perp, cubic_basis)
    constraint_basis = sparse_basis(constraints, PARAM)
    constraint_null = nullspace(constraint_basis, PARAM)
    selected: tuple[int, list[int], list[int]] | None = None
    for basis_index, functional in enumerate(constraint_null):
        pairings = [sum(a * b for a, b in zip(row, functional)) % MOD for row in norm_d]
        witness = next((i for i, value in enumerate(pairings) if value), None)
        if witness is not None:
            selected = (basis_index, functional, pairings)
            break
    if selected is None:
        status = "UNKNOWN_ALLPASS_MAGNUS4_A18"
        basis_index = None
        functional: list[int] = []
        pairings = [0] * len(norm_d)
        witness = None
    else:
        basis_index, functional, pairings = selected
        witness = next(i for i, value in enumerate(pairings) if value)
        status = "B4_A_CANDIDATE_MAGNUS4_A18"
    print("B4_MAGNUS4_A18_CONSTRAINTS rank=", len(constraint_basis),
          " nullity=", len(constraint_null), " status=", status, flush=True)
    return {
        "schema": "d972-b4-u-magnus4-a18/v1",
        "status": status,
        "source_sha256": SOURCE_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "relator_sha256": RELATOR_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "raw_rs_sha256": RAW_RS_SHA,
        "dtilde_rs_sha256": DTILDE_RS_SHA,
        "rho_words_source": "universal_v2_canonical",
        "rho_words_sha256": RHO_SHA,
        "rho_words": [list(x) for x in RHO],
        "presentation_relator_count": len(presentation),
        "a18_row_count": 140,
        "norm_count": len(dtilde),
        "rs_generator_count": len(pair_words),
        "rs_relator_count": len(rs_words),
        "rs_pair_words_sha256": digest(pair_words),
        "linear_dimension": D,
        "linear_rank_mod3": len(linear_basis),
        "linear_nullity": len(linear_null),
        "magnus_generator_columns_sha256": digest(columns),
        "degree2_dimension": D2,
        "degree2_relator_rank_mod3": len(q_basis),
        "degree2_perp_dimension": len(q_perp),
        "degree2_relator_rows_sha256": digest(rel_q),
        "degree2_perp_sha256": digest(q_perp),
        "degree3_dimension": D3,
        "degree3_relator_rows_sha256": digest(rel_c),
        "degree3_relator_basis_rank_mod3": len(cubic_basis),
        "degree4_dimension": D4,
        "degree4_parameter_dimension": PARAM,
        "degree4_projected_relator_rows_sha256": digest(rel_d),
        "degree4_projected_dtilde_rows_sha256": digest(norm_d),
        "degree4_constraint_rank_mod3": len(constraint_basis),
        "degree4_functional_nullity": len(constraint_null),
        "degree4_null_basis": constraint_null,
        "degree4_null_basis_index": basis_index,
        "degree4_functional_projected": functional,
        "dtilde_pairings_mod3": pairings,
        "witness_index": None if witness is None else witness + 1,
        "witness_dtilde_word": None if witness is None else dtilde[witness],
        "witness_rs_word": None if witness is None else dtilde_rs[witness],
        "witness_pairing_mod3": None if witness is None else pairings[witness],
        "kernel_characteristic": False,
        "finite_U_quotient_via_core": True,
        "finite_quotient": "core_U(raw_A18_degree4_Magnus_kernel)",
        "terminal_claim": False,
        "proof_level": "FINITE_RAW_A18_MAGNUS4_REPLAY_REQUIRED",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--word-artifact", type=Path, default=DEFAULT_WORDS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    source = args.source.resolve()
    words = args.word_artifact.resolve()
    if args.selftest:
        selftest(source, words)
        return 0
    if args.output is None:
        parser.error("--output is required unless --selftest is used")
    presentation, dtilde, artifact_sha = load_inputs(source, words)
    result = run(presentation, dtilde)
    result["word_artifact_raw_sha256"] = artifact_sha
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "status", "linear_rank_mod3", "degree2_relator_rank_mod3",
        "degree4_constraint_rank_mod3", "degree4_functional_nullity",
        "witness_index")}, sort_keys=True))
    return 0 if result["status"] == "B4_A_CANDIDATE_MAGNUS4_A18" else 2


if __name__ == "__main__":
    raise SystemExit(main())
