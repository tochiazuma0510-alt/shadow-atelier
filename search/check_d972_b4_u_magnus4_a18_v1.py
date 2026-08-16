#!/usr/bin/env python3
"""Independent replay checker for the raw-A.18 degree-four lane.

No producer module is imported.  The checker reconstructs the canonical
literal A.18 presentation, unconditional D-tilde ledger, regular C2^5
Schreier words, and the F3 degree-four constraints before accepting a
receipt.  A finite witness is a candidate A obstruction; all-pass is UNKNOWN.
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
QDIM = 5
PARAM = QDIM * D2
WIDTH = 161
SCHEMA = "d972-b4-u-magnus4-a18/v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter != 0, "zero signed letter")
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
        require(abs(letter) in (1, 4), "marked F6 alphabet drift")
        image = first if abs(letter) == 1 else second
        out.extend(inverse_word(image) if letter < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2: list[int]) -> list[int]:
    marked: list[int] = []
    for letter in f2:
        require(abs(letter) in (1, 2), "roof F2 alphabet drift")
        marked.append((1 if letter > 0 else -1) if abs(letter) == 1
                      else (4 if letter > 0 else -4))
    x15, x45 = [-3, -2, -1], [-6, -5, -3]
    return free_reduce(
        inverse_word(marked_substitute(marked, x45, [6])) +
        inverse_word(marked_substitute(marked, [1], x15)) +
        marked_substitute(marked, [4], [6]) +
        marked_substitute(marked, x45, x15) +
        marked_substitute(marked, [1], [4]))


def load_inputs(source_path: Path, words_path: Path) -> tuple[list[list[int]], list[list[int]], str]:
    source_raw = source_path.read_bytes()
    require(hashlib.sha256(source_raw).hexdigest() == SOURCE_SHA, "source SHA drift")
    source = json.loads(source_raw.decode("utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2" and
            source.get("relator_count") == 158 and
            source.get("rho_words") == [list(x) for x in RHO] and
            source.get("rho_words_source") == "universal_v2_canonical" and
            source.get("all_relators_sha256") == RELATOR_SHA,
            "source contract drift")
    relators = [[int(x) for x in row] for row in source["all_relators"]]
    require(len(relators) == 158 and digest(relators) == RELATOR_SHA, "relator digest drift")
    seeds = relators[18:46]
    a18: list[list[int]] = []
    for _name, first, second in MAPS:
        a18.extend(marked_substitute(row, list(first), list(second)) for row in seeds)
    require(len(a18) == 140 and digest(a18) == A18_ROWS_SHA, "A18 row digest drift")
    presentation = relators[:18] + a18
    require(len(presentation) == 158 and digest(presentation) == PRESENTATION_SHA,
            "presentation digest drift")
    words_raw = words_path.read_bytes()
    require(hashlib.sha256(words_raw).hexdigest() == WORDS_SHA, "word artifact SHA drift")
    words = json.loads(words_raw.decode("utf-8"))
    require(words.get("schema") == "d972-b4-word-key-artifact/v1" and
            words.get("count") == 972 and len(words.get("rows", [])) == 972,
            "word artifact contract drift")
    f2_rows: list[list[int]] = []
    for index, row in enumerate(words["rows"]):
        require(isinstance(row, list) and len(row) == 3, "word row shape drift")
        word = row[2]
        if word == "":
            require(index in (0, 891), "legacy empty word drift")
            word = []
        require(isinstance(word, list), "word row type drift")
        f2_rows.append([int(x) for x in word])
    dtilde = [exact_dtilde(row) for row in f2_rows]
    require(digest(dtilde) == DTILDE_SHA, "Dtilde digest drift")
    return presentation, dtilde, hashlib.sha256(words_raw).hexdigest()


def transversal(mask: int) -> list[int]:
    return [i + 1 for i in range(5) if mask & (1 << i)]


def toggle(mask: int, bit: int) -> int:
    return 31 - mask if bit == 31 else mask ^ bit


def build_rs(relators: list[list[int]]) -> tuple[list[list[int]], dict[tuple[int, int], int | None], list[list[int]]]:
    ids: dict[tuple[int, int], int | None] = {}
    pairs: list[list[int]] = []
    for mask in range(32):
        for gen, bit in enumerate(GEN_BITS, 1):
            word = free_reduce(transversal(mask) + [gen] +
                               inverse_word(transversal(toggle(mask, bit))))
            if word:
                ids[(mask, gen)] = len(pairs) + 1
                pairs.append(word)
            else:
                ids[(mask, gen)] = None
    require(len(pairs) == WIDTH, "Schreier width drift")

    def rewrite(word: list[int], start: int) -> tuple[list[int], int]:
        mask, out = start, []
        for letter in word:
            gen, bit = abs(letter), GEN_BITS[abs(letter) - 1]
            if letter > 0:
                ident = ids[(mask, gen)]
                if ident is not None:
                    out.append(ident)
                mask = toggle(mask, bit)
            else:
                mask = toggle(mask, bit)
                ident = ids[(mask, gen)]
                if ident is not None:
                    out.append(-ident)
        return free_reduce(out), mask

    rows: list[list[int]] = []
    for start in range(32):
        for relator in relators:
            row, end = rewrite(relator, start)
            require(end == start, "presentation relator endpoint drift")
            if row:
                rows.append(row)
    require(len(rows) == 5056 and digest(rows) == RAW_RS_SHA, "RS relator digest drift")
    return rows, ids, pairs


def rewrite_words(words: list[list[int]], ids: dict[tuple[int, int], int | None]) -> list[list[int]]:
    result: list[list[int]] = []
    for word in words:
        mask, out = 0, []
        for letter in word:
            gen, bit = abs(letter), GEN_BITS[abs(letter) - 1]
            if letter > 0:
                ident = ids[(mask, gen)]
                if ident is not None:
                    out.append(ident)
                mask = toggle(mask, bit)
            else:
                mask = toggle(mask, bit)
                ident = ids[(mask, gen)]
                if ident is not None:
                    out.append(-ident)
        require(mask == 0, "Dtilde endpoint drift")
        result.append(free_reduce(out))
    require(len(result) == 972 and digest(result) == DTILDE_RS_SHA, "Dtilde RS digest drift")
    return result


def exponent_vector(word: list[int]) -> list[int]:
    vector = [0] * WIDTH
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
            for qi, qv in enumerate(quadratic):
                if qv:
                    for j, pv in enumerate(p):
                        cubic[qi * D + j] = (cubic[qi * D + j] - qv * pv) % MOD
            for i, lv in enumerate(linear):
                if lv:
                    for j, a in enumerate(p):
                        if a:
                            for k, b in enumerate(p):
                                if b:
                                    index = (i * D + j) * D + k
                                    cubic[index] = (cubic[index] + lv * a * b) % MOD
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
            for qi, qv in enumerate(quadratic):
                if qv:
                    for j, pv in enumerate(p):
                        cubic[qi * D + j] = (cubic[qi * D + j] + qv * pv) % MOD
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
            cubic = (cubic.reshape(QDIM, D) + qproj.reshape(QDIM, 1) * p.reshape(1, D)) % MOD
            quadratic = (quadratic + np.outer(linear, p).reshape(-1)) % MOD
            linear = (linear + p) % MOD
        else:
            degree4 = (degree4.reshape(QDIM, D, D) -
                       cubic.reshape(QDIM, D, 1) * p.reshape(1, 1, D) +
                       qproj.reshape(QDIM, 1, 1) * p2.reshape(1, D, D) -
                       lp.reshape(QDIM, 1, 1) * p2.reshape(1, D, D) +
                       pp.reshape(QDIM, 1, 1) * p2.reshape(1, D, D)) % MOD
            cubic = (cubic.reshape(QDIM, D) - qproj.reshape(QDIM, 1) * p.reshape(1, D) +
                     lp.reshape(QDIM, 1) * p.reshape(1, D) -
                     pp.reshape(QDIM, 1) * p.reshape(1, D)) % MOD
            quadratic = (quadratic - np.outer(linear, p).reshape(-1) + p2.reshape(-1)) % MOD
            linear = (linear - p) % MOD
        cubic = cubic.reshape(-1)
        degree4 = degree4.reshape(-1)
    require(not np.any(linear), "degree-four linear drift")
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


def replay_receipt(receipt: dict[str, Any], presentation: list[list[int]],
                   dtilde: list[list[int]], artifact_sha: str) -> dict[str, Any]:
    require(receipt.get("schema") == SCHEMA, "receipt schema drift")
    require(receipt.get("status") in {"UNKNOWN_ALLPASS_MAGNUS4_A18",
                                       "B4_A_CANDIDATE_MAGNUS4_A18"},
            "receipt status drift")
    pins = {
        "source_sha256": SOURCE_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "relator_sha256": RELATOR_SHA,
        "a18_rows_sha256": A18_ROWS_SHA,
        "presentation_sha256": PRESENTATION_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "raw_rs_sha256": RAW_RS_SHA,
        "dtilde_rs_sha256": DTILDE_RS_SHA,
        "rho_words_sha256": RHO_SHA,
    }
    for key, expected in pins.items():
        require(receipt.get(key) == expected, key + " pin drift")
    require(receipt.get("rho_words") == [list(x) for x in RHO] and
            receipt.get("word_artifact_raw_sha256") == artifact_sha and
            receipt.get("terminal_claim") is False,
            "receipt canonical binding drift")
    require(receipt.get("presentation_relator_count") == 158 and
            receipt.get("a18_row_count") == 140 and receipt.get("norm_count") == 972,
            "receipt count drift")

    rs_words, ids, pairs = build_rs(presentation)
    dtilde_rs = rewrite_words(dtilde, ids)
    require(len(pairs) == WIDTH and len(rs_words) == 5056, "RS count drift")
    require(receipt.get("rs_generator_count") == WIDTH and
            receipt.get("rs_relator_count") == 5056 and
            receipt.get("rs_pair_words_sha256") == digest(pairs), "RS basis drift")
    rel_vectors = [exponent_vector(row) for row in rs_words]
    linear_basis = sparse_basis(rel_vectors, WIDTH)
    linear_null = nullspace(linear_basis, WIDTH)
    require(len(linear_basis) == 154 and len(linear_null) == D and
            receipt.get("linear_rank_mod3") == 154 and receipt.get("linear_nullity") == D,
            "linear dimension drift")
    columns = [[linear_null[j][i] for j in range(D)] for i in range(WIDTH)]
    require(receipt.get("magnus_generator_columns_sha256") == digest(columns), "column digest drift")
    rel_q: list[list[int]] = []
    rel_c: list[list[int]] = []
    for row in rs_words:
        linear, quadratic, cubic = magnus3(row, columns)
        require(not any(linear), "RS cubic linear drift")
        rel_q.append(quadratic)
        rel_c.append(cubic)
    for row in dtilde_rs:
        linear, _, _ = magnus3(row, columns)
        require(not any(linear), "Dtilde cubic linear drift")
    q_basis_sparse = sparse_basis(rel_q, D2)
    q_basis: list[list[int]] = []
    for _, sparse_row in sorted(q_basis_sparse.items()):
        row = [0] * D2
        for index, value in sparse_row.items():
            row[index] = value
        q_basis.append(row)
    q_perp = nullspace(q_basis_sparse, D2)
    require(len(q_basis) == 44 and len(q_perp) == QDIM and
            receipt.get("degree2_relator_rank_mod3") == 44 and
            receipt.get("degree2_perp_dimension") == QDIM and
            receipt.get("degree2_relator_rows_sha256") == digest(rel_q) and
            receipt.get("degree2_perp_sha256") == digest(q_perp), "degree-two drift")
    cubic_sparse = sparse_basis(rel_c, D3)
    cubic_basis: list[list[int]] = []
    for _, sparse_row in sorted(cubic_sparse.items()):
        row = [0] * D3
        for index, value in sparse_row.items():
            row[index] = value
        cubic_basis.append(row)
    pvec, lmap, ppmap = prepare4(columns, q_perp)
    rel_d = [collect4(row, q_perp, pvec, lmap, ppmap) for row in rs_words]
    norm_d = [collect4(row, q_perp, pvec, lmap, ppmap) for row in dtilde_rs]
    constraints = constraint_rows(q_basis, q_perp, cubic_basis)
    c_basis = sparse_basis(constraints, PARAM)
    c_null = nullspace(c_basis, PARAM)
    require(receipt.get("degree3_relator_rows_sha256") == digest(rel_c) and
            receipt.get("degree3_relator_basis_rank_mod3") == len(cubic_basis) and
            receipt.get("degree4_projected_relator_rows_sha256") == digest(rel_d) and
            receipt.get("degree4_projected_dtilde_rows_sha256") == digest(norm_d) and
            receipt.get("degree4_constraint_rank_mod3") == len(c_basis) and
            receipt.get("degree4_functional_nullity") == len(c_null),
            "degree-four row/rank drift")
    pairings_by_null = [[sum(a * b for a, b in zip(row, f)) % MOD for row in norm_d]
                        for f in c_null]
    status = receipt["status"]
    if status == "UNKNOWN_ALLPASS_MAGNUS4_A18":
        require(not c_null and receipt.get("degree4_null_basis") == [] and
                receipt.get("degree4_functional_projected") == [] and
                receipt.get("dtilde_pairings_mod3") == [0] * 972 and
                receipt.get("witness_index") is None,
                "all-pass witness fields drift")
        require(all(all(value == 0 for value in row) for row in pairings_by_null),
                "all-pass functional drift")
        out_status = "UNKNOWN_ALLPASS_MAGNUS4_A18_CROSSCHECKED"
    else:
        functional = receipt.get("degree4_functional_projected")
        pairings = receipt.get("dtilde_pairings_mod3")
        witness = receipt.get("witness_index")
        require(isinstance(functional, list) and len(functional) == PARAM and
                isinstance(pairings, list) and len(pairings) == 972 and
                isinstance(witness, int) and 1 <= witness <= 972 and
                pairings[witness - 1] % MOD != 0,
                "candidate witness shape drift")
        require(all(sum(a * b for a, b in zip(row, functional)) % MOD == 0
                    for row in constraints), "functional does not kill constraints")
        computed = [sum(a * b for a, b in zip(row, functional)) % MOD for row in norm_d]
        require(computed == [int(x) % MOD for x in pairings], "candidate pairing drift")
        out_status = "B4_A_CANDIDATE_MAGNUS4_A18_CROSSCHECKED"
    return {"schema": "d972-b4-u-magnus4-a18-independent/v1",
            "status": out_status, "producer_status": status,
            "rs_generator_count": WIDTH, "rs_relator_count": 5056,
            "norm_count": 972}


def selftest(source: Path, words: Path) -> None:
    presentation, dtilde, raw_sha = load_inputs(source, words)
    rs, ids, pairs = build_rs(presentation)
    dtilde_rs = rewrite_words(dtilde, ids)
    require(len(presentation) == 158 and len(dtilde) == 972 and len(pairs) == WIDTH,
            "A18 count selftest drift")
    require(len(rs) == 5056 and digest(rs) == RAW_RS_SHA and digest(dtilde_rs) == DTILDE_RS_SHA,
            "A18 digest selftest drift")
    require(raw_sha == WORDS_SHA, "word artifact raw SHA selftest drift")
    print("D972_B4_U_MAGNUS4_A18_CHECKER_SELFTEST_PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
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
    if args.receipt is None or args.output is None:
        parser.error("--receipt and --output are required unless --selftest is used")
    presentation, dtilde, artifact_sha = load_inputs(source, words)
    receipt_raw = args.receipt.resolve().read_bytes()
    result = replay_receipt(json.loads(receipt_raw.decode("utf-8")), presentation, dtilde, artifact_sha)
    result["producer_receipt_sha256"] = hashlib.sha256(receipt_raw).hexdigest()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"].startswith("B4_A_CANDIDATE") or result["status"].startswith("UNKNOWN_ALLPASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
