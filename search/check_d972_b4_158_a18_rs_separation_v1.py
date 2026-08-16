#!/usr/bin/env python3
"""Independent checker for the finite RS presentation-separation receipt.

The checker deliberately duplicates the signed-word, regular C2^5 Schreier,
and F3 row-reduction code.  It never imports the producer and never trusts a
digest or a claimed functional by itself: all 5056 current relator rows and
all 140 raw A.18 rows are rebuilt from the pinned 6/158 source and compared.

The result is only the finite presentation statement
N_A18 is not a subset of N_rho.  It is not a B4 A/B, cofinality, or Ihara
claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence


SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
BITS = (1, 2, 4, 8, 16, 31)
MAPS = (
    ("123", ((1,), (4,))),
    ("234", ((4,), (6,))),
    ("12,3,4", ((2, 4), (6,))),
    ("1,23,4", ((1, 2), (5, 6))),
    ("1,2,34", ((1,), (4, 5))),
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


def substitute_marked(word: Sequence[int], left: Sequence[int],
                      right: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        if n == 0 or abs(n) not in (1, 4):
            raise ValueError("marked F2 seed alphabet drift")
        image = list(left if abs(n) == 1 else right)
        out.extend(inverse_word(image) if n < 0 else image)
    return reduce_word(out)


def load_source(path: Path) -> tuple[list[list[int]], list[list[int]], list[list[list[int]]]]:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError("canonical source SHA drift")
    source = json.loads(raw.decode("utf-8"))
    if source.get("schema") != "d972-b4-p2-magnus-input/v2":
        raise ValueError("canonical schema drift")
    if source.get("relator_count") != 158 or len(source.get("all_relators", [])) != 158:
        raise ValueError("canonical relator count drift")
    if source.get("rho_words") != [list(x) for x in RHO]:
        raise ValueError("current rho drift")
    if source.get("rho_words_source") != "universal_v2_canonical":
        raise ValueError("rho provenance drift")
    relators = [[int(x) for x in row] for row in source["all_relators"]]
    if source.get("all_relators_sha256") != RELATOR_SHA or digest(relators) != RELATOR_SHA:
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
    reps = [[i + 1 for i in range(5) if mask & (1 << i)] for mask in range(32)]
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
        key = abs(n) - 1
        value = (out.get(key, 0) + (1 if n > 0 else -1)) % 3
        if value:
            out[key] = value
        else:
            out.pop(key, None)
    if any(key < 0 or key >= width for key in out):
        raise ValueError("RS vector width drift")
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
                reduced = (row.get(key, 0) - coefficient * value) % 3
                if reduced:
                    row[key] = reduced
                else:
                    row.pop(key, None)
    return pivots


def null_basis(pivots: dict[int, dict[int, int]], width: int) -> list[list[int]]:
    basis: list[list[int]] = []
    for free in range(width):
        if free in pivots:
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
    return sum(functional[key] * value for key, value in vector.items()) % 3


def build_expected(source: Path) -> dict[str, Any]:
    relators, seeds, blocks = load_source(source)
    pairs, dimension = pair_ids()
    rs_rows: list[list[int]] = []
    rs_vectors: list[dict[int, int]] = []
    for start in range(32):
        for relator in relators:
            row, end = rewrite(relator, pairs, start)
            if end != start:
                raise ValueError("RS relator endpoint drift")
            rs_rows.append(row)
            rs_vectors.append(exponent_vector(row, dimension))
    if len(rs_rows) != 5056:
        raise ValueError("RS relator count drift")
    pivots = echelon(rs_vectors)
    basis = null_basis(pivots, dimension)
    if not basis or any(pairing(row, f) for f in basis for row in rs_vectors):
        raise ValueError("F3 null-functional replay failed")

    maps: list[dict[str, Any]] = []
    nonzero_count = 0
    first: dict[str, Any] | None = None
    for name, substitution in MAPS:
        candidates = [substitute_marked(seed, substitution[0], substitution[1])
                      for seed in seeds]
        rows: list[dict[str, Any]] = []
        for row_index, candidate in enumerate(candidates):
            rs_word, end = rewrite(candidate, pairs, 0)
            if end != 0:
                raise ValueError("raw A.18 row does not close in C2^5")
            vector = exponent_vector(rs_word, dimension)
            witness = next((j for j, f in enumerate(basis)
                            if pairing(vector, f) != 0), None)
            nonzero = witness is not None
            if nonzero:
                nonzero_count += 1
                if first is None:
                    f = basis[witness]
                    first = {
                        "map": name,
                        "seed_row_zero_based": row_index,
                        "seed_row_one_based": row_index + 1,
                        "candidate_word": candidate,
                        "rs_word": rs_word,
                        "rs_exponent_vector": vector,
                        "functional_index": witness,
                        "functional": f,
                        "pairing_mod3": pairing(vector, f),
                    }
            rows.append({
                "seed_row": row_index + 1,
                "candidate_word": candidate,
                "rs_word": rs_word,
                "endpoint": end,
                "rs_exponent_vector": vector,
                "nonzero_in_quotient": nonzero,
                "functional_index": witness,
                "pairing_mod3": pairing(vector, basis[witness]) if witness is not None else 0,
            })
        maps.append({
            "name": name,
            "substitution": [list(substitution[0]), list(substitution[1])],
            "candidate_rows": candidates,
            "rows": rows,
            "nonzero_count": sum(int(row["nonzero_in_quotient"]) for row in rows),
        })

    current: list[dict[str, Any]] = []
    for power, block in enumerate(blocks):
        for row_index, row in enumerate(block):
            rs_word, end = rewrite(row, pairs, 0)
            vector = exponent_vector(rs_word, dimension)
            if end != 0 or any(pairing(vector, f) for f in basis):
                raise ValueError("current rho-tail row is not killed")
            current.append({
                "power": power,
                "seed_row": row_index + 1,
                "endpoint": end,
                "rs_word": rs_word,
                "all_functionals_zero": True,
            })

    status = ("B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT"
              if nonzero_count else "UNKNOWN_NO_RS_SEPARATION")
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
        "map_count": 5,
        "generator_count": 6,
        "coset_count": 32,
        "rs_generator_count": dimension,
        "rs_relator_count": len(rs_rows),
        "rs_relator_words_sha256": digest(rs_rows),
        "rs_exponent_rows_sha256": digest(rs_vectors),
        "rs_rank_mod3": len(pivots),
        "rs_nullity_mod3": len(basis),
        "functional_basis_sha256": digest(basis),
        "current_tail_zero_count": len(current),
        "current_tail_checks": current,
        "maps": maps,
        "raw_a18_nonzero_count": nonzero_count,
        "first_separation": first,
        "separation_theorem": (
            "A nonzero F3 functional kills every 32-coset RS row of the "
            "current 158-relator normal closure, while pairing nontrivially "
            "with a raw A18 row in the C2^5 kernel. Hence N_A18 is not a "
            "subset of N_rho in F6."
        ),
        "b4_status": "NOT_ESTABLISHED",
    }


def json_normalize(value: Any) -> Any:
    return json.loads(cjson(value).decode("ascii"))


def verify(receipt_path: Path, source_path: Path) -> dict[str, Any]:
    expected = json_normalize(build_expected(source_path))
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes.decode("utf-8"))
    for key in (
        "schema", "status", "terminal_claim", "scope", "source_sha256",
        "relator_sha256", "rho_words", "relator_count", "prefix_count",
        "seed_count", "block_count", "map_count", "generator_count",
        "coset_count", "rs_generator_count", "rs_relator_count",
        "rs_relator_words_sha256", "rs_exponent_rows_sha256", "rs_rank_mod3",
        "rs_nullity_mod3", "functional_basis_sha256", "current_tail_zero_count",
        "raw_a18_nonzero_count", "b4_status",
    ):
        if receipt.get(key) != expected.get(key):
            raise ValueError(f"receipt field drift: {key}")
    if receipt.get("current_tail_checks") != expected["current_tail_checks"]:
        raise ValueError("current rho-tail replay drift")
    if receipt.get("maps") != expected["maps"]:
        raise ValueError("raw A.18 map replay drift")
    if receipt.get("first_separation") != expected["first_separation"]:
        raise ValueError("first finite separation witness drift")
    if receipt.get("separation_theorem") != expected["separation_theorem"]:
        raise ValueError("theorem wording/scope drift")
    if expected["status"] != "B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT":
        raise ValueError("canonical source does not produce a separation")
    return {
        "schema": "d972-b4-158-a18-rs-separation-check/v1",
        "status": "B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT_CROSSCHECKED",
        "scope": "presentation_semantic_separation_only",
        "source_sha256": SOURCE_SHA,
        "relator_sha256": RELATOR_SHA,
        "raw_a18_nonzero_count": expected["raw_a18_nonzero_count"],
        "rs_generator_count": expected["rs_generator_count"],
        "rs_relator_count": expected["rs_relator_count"],
        "all_current_rows_replayed": True,
        "all_raw_a18_rows_replayed": True,
        "producer_receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "terminal_claim": False,
        "b4_status": "NOT_ESTABLISHED",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--source", type=Path,
                        default=Path("search/certs/d972_b4_p2_magnus_input_v2_20260816.json"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            expected = build_expected(args.source.resolve())
            if (expected["status"] != "B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT"
                    or expected["raw_a18_nonzero_count"] <= 0):
                raise ValueError("canonical finite separation selftest failed")
            print(json.dumps({
                "status": "SELFTEST_PASS",
                "raw_a18_nonzero_count": expected["raw_a18_nonzero_count"],
                "first_separation": expected["first_separation"],
            }, sort_keys=True))
            return 0
        if args.receipt is None:
            parser.error("--receipt is required unless --selftest is used")
        result = verify(args.receipt.resolve(), args.source.resolve())
        encoded = json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
        if args.output:
            args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
            args.output.resolve().write_text(encoded, encoding="utf-8")
        print(encoded, end="")
        return 0
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"B4_A18_RS_SEPARATION_CHECK_UNKNOWN {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
