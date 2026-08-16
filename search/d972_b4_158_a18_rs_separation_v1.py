#!/usr/bin/env python3
"""Finite Reidemeister--Schreier separation of literal A.18 from rho-tail.

The current 6/158 presentation is U = F6 / <<R0 union B0..B4>>.
This lane builds the regular C2^5 Schreier table, all 32*158 RS relator
rows, and the finite F3 quotient of the abelianized kernel obtained by
modding out those rows.  A raw A.18 row with nonzero image is a direct
presentation-level separation: it belongs to the literal A.18 normal
closure but not to the current rho-tail normal closure.

This is not a B4 A/B or Ihara conclusion.  The finite quotient is used only
to prove that the current 158 tail is not the literal A.18 presentation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
BITS = (1, 2, 4, 8, 16, 31)
MAPS = (
    ("123", [[1], [4]]),
    ("234", [[4], [6]]),
    ("12,3,4", [[2, 4], [6]]),
    ("1,23,4", [[1, 2], [5, 6]]),
    ("1,2,34", [[1], [4, 5]]),
)


def cjson(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def reduce_word(word: Iterable[int], width: int = 6) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        if n == 0 or abs(n) > width:
            raise ValueError("signed word alphabet drift")
        if out and out[-1] == -n:
            out.pop()
        else:
            out.append(n)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def rho_word(word: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        if n == 0 or abs(n) > 6:
            raise ValueError("rho alphabet drift")
        image = list(RHO[abs(n) - 1])
        out.extend(inverse_word(image) if n < 0 else image)
    return reduce_word(out)


def substitute_marked(word: Sequence[int], a: Sequence[int],
                      b: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        if n == 0 or abs(n) not in (1, 4):
            raise ValueError("marked F2 seed alphabet drift")
        image = list(a if abs(n) == 1 else b)
        out.extend(inverse_word(image) if n < 0 else image)
    return reduce_word(out)


def load_source(path: Path) -> tuple[list[list[int]], list[list[int]], list[list[list[int]]]]:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError("canonical source SHA drift")
    obj = json.loads(raw.decode("utf-8"))
    if obj.get("schema") != "d972-b4-p2-magnus-input/v2":
        raise ValueError("canonical schema drift")
    relators = [[int(x) for x in row] for row in obj.get("all_relators", [])]
    if len(relators) != 158 or obj.get("relator_count") != 158:
        raise ValueError("canonical 158 count drift")
    if obj.get("rho_words") != [list(x) for x in RHO]:
        raise ValueError("current rho drift")
    if obj.get("rho_words_source") != "universal_v2_canonical":
        raise ValueError("rho provenance drift")
    if obj.get("all_relators_sha256") != RELATOR_SHA or digest(relators) != RELATOR_SHA:
        raise ValueError("relator digest drift")
    seeds = [list(x) for x in relators[18:46]]
    blocks: list[list[list[int]]] = []
    for power in range(5):
        block = [list(x) for x in relators[18 + 28 * power:46 + 28 * power]]
        expected = [list(x) for x in seeds]
        for _ in range(power):
            expected = [rho_word(x) for x in expected]
        if block != expected:
            raise ValueError("current rho tail drift")
        blocks.append(block)
    return relators, seeds, blocks


def pair_ids() -> tuple[dict[tuple[int, int], int | None], int]:
    reps = [[i + 1 for i in range(5) if mask & (1 << i)]
            for mask in range(32)]
    pairs: dict[tuple[int, int], int | None] = {}
    count = 0
    for mask in range(32):
        for gen, bit in enumerate(BITS, start=1):
            token = reps[mask] + [gen] + inverse_word(reps[mask ^ bit])
            if reduce_word(token):
                count += 1
                pairs[(mask, gen)] = count
            else:
                pairs[(mask, gen)] = None
    if count != 161:
        raise ValueError("regular C2^5 Schreier generator count drift")
    return pairs, count


def rewrite(word: Sequence[int], pairs: dict[tuple[int, int], int | None],
            start: int = 0) -> tuple[list[int], int]:
    mask = start
    out: list[int] = []
    for raw in word:
        n = int(raw)
        gen = abs(n)
        bit = BITS[gen - 1]
        if n > 0:
            ident = pairs[(mask, gen)]
            if ident is not None:
                out.append(ident)
            mask ^= bit
        else:
            mask ^= bit
            ident = pairs[(mask, gen)]
            if ident is not None:
                out.append(-ident)
    return reduce_word(out, 161), mask


def exponent_vector(word: Sequence[int], width: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for raw in word:
        n = int(raw)
        index = abs(n) - 1
        value = (out.get(index, 0) + (1 if n > 0 else -1)) % 3
        if value:
            out[index] = value
        elif index in out:
            del out[index]
    return out


def echelon(rows: Iterable[dict[int, int]]) -> dict[int, dict[int, int]]:
    pivots: dict[int, dict[int, int]] = {}
    for source in rows:
        row = {int(k): int(v) % 3 for k, v in source.items() if int(v) % 3}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                if row[pivot] == 2:
                    row = {key: (-value) % 3 for key, value in row.items()}
                pivots[pivot] = row
                break
            coefficient = row[pivot]
            base = pivots[pivot]
            for key, value in base.items():
                result = (row.get(key, 0) - coefficient * value) % 3
                if result:
                    row[key] = result
                elif key in row:
                    del row[key]
    return pivots


def null_basis(pivots: dict[int, dict[int, int]], width: int) -> list[list[int]]:
    pivot_set = set(pivots)
    basis: list[list[int]] = []
    for free in range(width):
        if free in pivot_set:
            continue
        vector = [0] * width
        vector[free] = 1
        for pivot in sorted(pivots, reverse=True):
            row = pivots[pivot]
            vector[pivot] = (-sum(value * vector[key]
                                  for key, value in row.items()
                                  if key != pivot)) % 3
        basis.append(vector)
    return basis


def pairing(vector: dict[int, int], functional: Sequence[int]) -> int:
    return sum(int(functional[key]) * value for key, value in vector.items()) % 3


def build_receipt(source_path: Path) -> dict[str, Any]:
    relators, seeds, blocks = load_source(source_path)
    pairs, dimension = pair_ids()
    rs_rows: list[list[int]] = []
    rs_vectors: list[dict[int, int]] = []
    for start in range(32):
        for index, relator in enumerate(relators):
            row, end = rewrite(relator, pairs, start)
            if end != start:
                raise ValueError(f"RS relator endpoint drift at {start},{index}")
            rs_rows.append(row)
            rs_vectors.append(exponent_vector(row, dimension))
    if len(rs_rows) != 32 * 158:
        raise ValueError("RS relator count drift")
    pivots = echelon(rs_vectors)
    basis = null_basis(pivots, dimension)
    if not basis:
        raise ValueError("finite RS quotient has zero nullity")
    for functional in basis:
        if any(pairing(row, functional) for row in rs_vectors):
            raise ValueError("null functional failed relator replay")

    maps: list[dict[str, Any]] = []
    total_nonzero = 0
    first: dict[str, Any] | None = None
    for name, subst in MAPS:
        candidates = [substitute_marked(seed, subst[0], subst[1])
                      for seed in seeds]
        rows: list[dict[str, Any]] = []
        for row_index, candidate in enumerate(candidates):
            rs_word, end = rewrite(candidate, pairs, 0)
            if end != 0:
                raise ValueError(f"A18 row does not close in C2^5: {name},{row_index}")
            vector = exponent_vector(rs_word, dimension)
            witness_index = next(
                (j for j, functional in enumerate(basis)
                 if pairing(vector, functional) != 0), None)
            nonzero = witness_index is not None
            if nonzero:
                total_nonzero += 1
                if first is None:
                    functional = basis[witness_index]
                    first = {
                        "map": name,
                        "seed_row_zero_based": row_index,
                        "seed_row_one_based": row_index + 1,
                        "candidate_word": candidate,
                        "rs_word": rs_word,
                        "rs_exponent_vector": vector,
                        "functional_index": witness_index,
                        "functional": functional,
                        "pairing_mod3": pairing(vector, functional),
                    }
            rows.append({
                "seed_row": row_index + 1,
                "candidate_word": candidate,
                "rs_word": rs_word,
                "endpoint": end,
                "rs_exponent_vector": vector,
                "nonzero_in_quotient": nonzero,
                "functional_index": witness_index,
                "pairing_mod3": (
                    pairing(vector, basis[witness_index])
                    if witness_index is not None else 0
                ),
            })
        maps.append({
            "name": name,
            "substitution": subst,
            "candidate_rows": candidates,
            "rows": rows,
            "nonzero_count": sum(item["nonzero_in_quotient"] for item in rows),
        })

    current_checks: list[dict[str, Any]] = []
    for power, block in enumerate(blocks):
        for row_index, row in enumerate(block):
            rs_word, end = rewrite(row, pairs, 0)
            vector = exponent_vector(rs_word, dimension)
            pairings = [pairing(vector, functional) for functional in basis]
            if end != 0 or any(pairings):
                raise ValueError("current rho-tail row is nonzero in RS quotient")
            current_checks.append({
                "power": power,
                "seed_row": row_index + 1,
                "endpoint": end,
                "rs_word": rs_word,
                "all_functionals_zero": True,
            })

    status = ("B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT"
              if total_nonzero else "UNKNOWN_NO_RS_SEPARATION")
    return {
        "schema": "d972-b4-158-a18-rs-separation/v1",
        "status": status,
        "terminal_claim": False,
        "scope": "presentation_semantic_separation_only",
        "source_sha256": SOURCE_SHA,
        "relator_sha256": RELATOR_SHA,
        "rho_words": [list(x) for x in RHO],
        "relator_count": 158,
        "prefix_count": 18,
        "seed_count": 28,
        "block_count": 5,
        "map_count": len(MAPS),
        "generator_count": 6,
        "coset_count": 32,
        "rs_generator_count": dimension,
        "rs_relator_count": len(rs_rows),
        "rs_relator_words_sha256": digest(rs_rows),
        "rs_exponent_rows_sha256": digest(rs_vectors),
        "rs_rank_mod3": len(pivots),
        "rs_nullity_mod3": len(basis),
        "functional_basis_sha256": digest(basis),
        "current_tail_zero_count": len(current_checks),
        "current_tail_checks": current_checks,
        "maps": maps,
        "raw_a18_nonzero_count": total_nonzero,
        "first_separation": first,
        "separation_theorem": (
            "A nonzero F3 functional kills every 32-coset RS row of the "
            "current 158-relator normal closure, while pairing nontrivially "
            "with a raw A18 row in the C2^5 kernel. Hence N_A18 is not a "
            "subset of N_rho in F6."
        ),
        "b4_status": "NOT_ESTABLISHED",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path,
                        default=Path("search/certs/d972_b4_p2_magnus_input_v2_20260816.json"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    try:
        receipt = build_receipt(args.source.resolve())
        if args.selftest:
            if receipt["status"] != "B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT":
                raise ValueError("RS separation selftest did not separate")
            print(json.dumps({
                "status": "SELFTEST_PASS",
                "raw_a18_nonzero_count": receipt["raw_a18_nonzero_count"],
                "first_separation": receipt["first_separation"],
            }, sort_keys=True))
            return 0
        if args.output is None:
            parser.error("--output is required unless --selftest is used")
        args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
        args.output.resolve().write_bytes(cjson(receipt) + b"\n")
        print(json.dumps({
            "status": receipt["status"],
            "raw_a18_nonzero_count": receipt["raw_a18_nonzero_count"],
            "first_separation": receipt["first_separation"],
        }, sort_keys=True))
        return 0 if receipt["status"] == "B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT" else 2
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"A18_RS_SEPARATION_UNKNOWN: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
