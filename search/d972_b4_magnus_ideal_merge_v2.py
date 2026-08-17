#!/usr/bin/env python3
"""Merge exact degree-6/7 Magnus ideal shards and evaluate B4 roof norms.

The shard files contain row spaces for disjoint subsets of the 158 relators.
This program authenticates the frozen input/digests, checks complete disjoint
coverage, merges the rows over F_2, and then writes the same lossless v2
receipt consumed by ``check_d972_b4_magnus_ideal_v1.py``.  Roof evaluation is
done only after the merged ideal is available, so a nonzero residue is a
genuine finite quotient candidate rather than a partial-shard artifact.

The accelerated chunk evaluator is algebraically the same monomial
permutation as the producer.  The independent checker intentionally uses a
different set-of-tuples implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
SHARD_PATH = Path(__file__).with_name("d972_b4_magnus_ideal_shard_v2.py")
PRODUCER_PATH = Path(__file__).with_name("d972_b4_magnus_ideal_v1.py")


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SHARD = import_module(SHARD_PATH, "d972_b4_magnus_ideal_shard_v2")
PRODUCER = import_module(PRODUCER_PATH, "d972_b4_magnus_ideal_v1")

NGEN = SHARD.NGEN
RELATOR_COUNT = SHARD.RELATOR_COUNT
ROOF_COUNT = SHARD.ROOF_COUNT
TARGET_KEY_DIGEST = SHARD.TARGET_KEY_DIGEST
CANONICAL_RHO = SHARD.CANONICAL_RHO


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_input(path: Path) -> tuple[dict[str, object], str, dict[str, str]]:
    # Reuse only the input gates from the accelerator; word evaluation itself
    # below remains explicit and receipt-oriented.
    return SHARD.load_input(path)


def expected_indices(index: int, count: int) -> list[int]:
    return [i + 1 for i in range(RELATOR_COUNT) if i % count == index]


def parse_row(value: object, monomial_count: int) -> int:
    if not isinstance(value, str) or not value or any(c not in "0123456789abcdefABCDEF" for c in value):
        raise ValueError("shard basis row is not a nonzero hexadecimal bitset")
    row = int(value, 16)
    if row.bit_length() > monomial_count:
        raise ValueError("shard basis row exceeds monomial dimension")
    return row


def add_high_basis(basis: dict[int, int], row: int) -> None:
    while row:
        pivot = row.bit_length() - 1
        old = basis.get(pivot)
        if old is None:
            basis[pivot] = row
            return
        row ^= old


def load_shards(paths: Sequence[Path], degree: int, input_sha: str,
                digests: dict[str, str]) -> tuple[dict[int, int], list[dict[str, object]]]:
    if not paths:
        raise ValueError("at least one shard is required")
    records: list[dict[str, object]] = []
    seen_shards: set[int] = set()
    common_count: int | None = None
    common_degree: int | None = None
    common_monomials = SHARD.monomial_count(degree)
    coverage: list[int] = []
    merged: dict[int, int] = {}
    for path in paths:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj.get("schema") != "d972-b4-magnus-ideal-shard/v2":
            raise ValueError(f"shard schema drift: {path}")
        if obj.get("degree") != degree:
            raise ValueError(f"shard degree mismatch: {path}")
        count = obj.get("shard_count")
        index = obj.get("shard_index")
        if not isinstance(count, int) or not isinstance(index, int) or count < 1 or not 0 <= index < count:
            raise ValueError(f"invalid shard index/count: {path}")
        if common_count is None:
            common_count = count
        elif count != common_count:
            raise ValueError("shard-count mismatch")
        if common_degree is None:
            common_degree = degree
        if index in seen_shards:
            raise ValueError("duplicate shard index")
        seen_shards.add(index)
        if obj.get("input_sha256") != input_sha:
            raise ValueError(f"shard input SHA mismatch: {path}")
        if obj.get("input_digests") != digests:
            raise ValueError(f"shard input digest mismatch: {path}")
        if obj.get("monomial_count") != common_monomials:
            raise ValueError(f"shard monomial count mismatch: {path}")
        expected = expected_indices(index, count)
        indices = obj.get("relator_indices")
        if indices != expected:
            raise ValueError(f"shard relator assignment mismatch: {path}")
        if obj.get("relator_indices_sha256") != sha_bytes(canonical_json(expected)):
            raise ValueError(f"shard relator-index digest mismatch: {path}")
        basis_hex = obj.get("ideal_basis_hex")
        pivots = obj.get("ideal_basis_pivots")
        if not isinstance(basis_hex, list) or not isinstance(pivots, list) or len(basis_hex) != len(pivots):
            raise ValueError(f"shard basis shape mismatch: {path}")
        rows = [parse_row(x, common_monomials) for x in basis_hex]
        if [row.bit_length() - 1 for row in rows] != [int(x) for x in pivots]:
            raise ValueError(f"shard pivot binding mismatch: {path}")
        if obj.get("ideal_rank") != len(rows):
            raise ValueError(f"shard rank metadata mismatch: {path}")
        for row in rows:
            add_high_basis(merged, row)
        coverage.extend(int(x) for x in indices)
        records.append({"path": str(path), "sha256": file_sha(path),
                        "shard_index": index, "shard_count": count,
                        "relator_count": len(indices), "ideal_rank": len(rows)})
    if common_count is None:
        raise ValueError("missing shard count")
    if seen_shards != set(range(common_count)):
        raise ValueError(f"incomplete shard set: got {sorted(seen_shards)} expected {list(range(common_count))}")
    if sorted(coverage) != list(range(1, RELATOR_COUNT + 1)):
        raise ValueError("shard relator coverage is not exact 1..158")
    return merged, sorted(records, key=lambda x: int(x["shard_index"]))


def quotient_evaluator(basis: dict[int, int], d: int):
    """Build exact quotient-coordinate actions for the six generators.

    The merged high-pivot basis leaves the non-pivot monomials as a
    coordinate complement.  Reducing a polynomial against the basis is
    therefore equivalent to retaining its non-pivot bits.  We precompute the
    action of X_g on those coordinates and evaluate all long roof words in
    the quotient directly.  This is an exact change of coordinates, not a
    probabilistic/hash compression; the returned ``to_poly`` map reconstructs
    the original monomial-bit residue expected by the lossless receipt.
    """
    powers, offsets = SHARD.powers_and_offsets(d)
    maps = SHARD.append_maps(d, powers, offsets)
    monomial_count = SHARD.monomial_count(d)
    nonpivots = [i for i in range(monomial_count) if i not in basis]
    coord_of = {index: bit for bit, index in enumerate(nonpivots)}
    qdim = len(nonpivots)
    if 0 not in coord_of:
        raise ValueError("constant monomial was killed by the ideal")

    def to_coord(poly: int) -> int:
        out = 0
        bits = poly
        while bits:
            low = bits & -bits
            index = low.bit_length() - 1
            bit = coord_of.get(index)
            if bit is None:
                raise ValueError("basis reduction left a pivot bit")
            out |= 1 << bit
            bits ^= low
        return out

    def reduce_high_full(row: int) -> int:
        """Fully reduce against high pivots, retaining only complement bits."""
        out = 0
        while row:
            pivot = row.bit_length() - 1
            old = basis.get(pivot)
            if old is None:
                out |= 1 << pivot
                row ^= 1 << pivot
            else:
                row ^= old
        return out

    def to_poly(coord: int) -> int:
        out = 0
        bits = coord
        while bits:
            low = bits & -bits
            bit = low.bit_length() - 1
            out |= 1 << nonpivots[bit]
            bits ^= low
        return out

    # image[g][bit] is the quotient coordinate of X_g times the bit-th
    # complement monomial.  Since the ideal is two-sided, this action is
    # independent of the chosen complement representative.
    images: list[list[int]] = []
    for g in range(NGEN):
        one_generator: list[int] = []
        for index in nonpivots:
            monomial = 1 << index
            shifted = SHARD.append_bits(monomial, maps[g])
            reduced = reduce_high_full(shifted)
            one_generator.append(to_coord(reduced))
        images.append(one_generator)

    # Four-bit XOR tables turn a q-dimensional linear action into at most
    # ceil(q/4) table lookups per letter.  q is only 32 in the canonical d=5
    # run, but this remains general for any finite quotient from this lane.
    chunk_bits = 4
    chunk_size = 1 << chunk_bits
    tables: list[list[list[int]]] = []
    for g in range(NGEN):
        by_chunk: list[list[int]] = []
        for first in range(0, qdim, chunk_bits):
            values = [0] * chunk_size
            for mask in range(1, chunk_size):
                low = mask & -mask
                bit = low.bit_length() - 1
                qbit = first + bit
                values[mask] = values[mask ^ low] ^ (images[g][qbit] if qbit < qdim else 0)
            by_chunk.append(values)
        tables.append(by_chunk)

    def apply_x(coord: int, g: int) -> int:
        out = 0
        for chunk, values in enumerate(tables[g]):
            mask = (coord >> (chunk * chunk_bits)) & (chunk_size - 1)
            if mask:
                out ^= values[mask]
        return out

    def eval_word(word: Sequence[int]) -> int:
        coord = 1 << coord_of[0]
        for raw in word:
            letter = int(raw)
            if letter == 0 or abs(letter) > NGEN:
                raise ValueError(f"invalid signed generator {letter}")
            g = abs(letter) - 1
            if letter > 0:
                coord ^= apply_x(coord, g)
            else:
                total = coord
                power = coord
                for _ in range(d):
                    power = apply_x(power, g)
                    total ^= power
                coord = total
        return to_poly(coord)

    return eval_word, qdim, nonpivots


def add_low_basis(basis: dict[int, int], row: int) -> None:
    while row:
        pivot = (row & -row).bit_length() - 1
        old = basis.get(pivot)
        if old is None:
            basis[pivot] = row
            return
        row ^= old


def reduce_low_receipt(basis: dict[int, int], row: int) -> int:
    """Match the independent checker's deliberately lowest-pivot reduction."""
    while row:
        pivot = (row & -row).bit_length() - 1
        old = basis.get(pivot)
        if old is None:
            return row
        row ^= old
    return 0


def discover_shards(args: argparse.Namespace) -> list[Path]:
    if args.shard and args.shard_dir:
        raise ValueError("use --shard or --shard-dir, not both")
    if args.shard:
        return list(args.shard)
    if args.shard_dir is None or args.shard_count is None:
        raise ValueError("--shard paths or --shard-dir/--shard-count are required")
    pattern = args.pattern.format(index="*", count=args.shard_count)
    paths = sorted(args.shard_dir.glob(pattern))
    expected = [args.shard_dir / args.pattern.format(index=i, count=args.shard_count)
                for i in range(args.shard_count)]
    if set(paths) != set(expected):
        raise ValueError(f"shard directory does not contain exactly expected files: {expected}")
    return expected


def evaluate(obj: dict[str, object], d: int, basis: dict[int, int],
             artifact_pairs: set[tuple[str, tuple[int, ...]]],
             artifact_meta: dict[str, object]) -> dict[str, object]:
    rels = [[int(x) for x in w] for w in obj["all_relators"]]  # type: ignore[index]
    rho = [[int(x) for x in w] for w in obj["rho_words"]]  # type: ignore[index]
    roofs = [[int(x) for x in w] for w in obj["roof_words"]]  # type: ignore[index]
    keys = [str(x) for x in obj["target_keys"]]  # type: ignore[index]
    eval_quotient, quotient_dimension, nonpivots = quotient_evaluator(basis, d)
    low_basis: dict[int, int] = {}
    for pivot in sorted(basis):
        add_low_basis(low_basis, basis[pivot])
    powers, offsets = SHARD.powers_and_offsets(d)
    maps = SHARD.append_maps(d, powers, offsets)

    def residue_fast(word: Sequence[int]) -> int:
        # eval_quotient returns the residue of E(word), so remove the unit
        # constant in F_2 exactly as the producer does.
        return eval_quotient(word) ^ 1

    def residue(word: Sequence[int]) -> int:
        # Most rows are zero and are settled by the quotient-coordinate
        # evaluator.  For a nonzero witness, replay just that word once in
        # the full encoded algebra and use the checker's exact lowest-pivot
        # normal form for byte-for-byte receipt compatibility.
        fast = residue_fast(word)
        if not fast:
            return 0
        # Replay only a nonzero candidate in the ordinary exact bitset map;
        # this avoids materializing the large degree-6/7 chunk tables.
        full = SHARD.eval_word(word, d, maps) ^ 1
        return reduce_low_receipt(low_basis, full)

    rel_bad = [i + 1 for i, w in enumerate(rels) if residue_fast(w)]
    rho_bad = [g for g in range(1, NGEN + 1)
               if residue_fast(PRODUCER.rho_power([g], rho, 5) + [-g])]
    rows: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    binding_bad = False
    for i, raw in enumerate(roofs, 1):
        signed = PRODUCER.signed_roof(raw)
        word = PRODUCER.norm_word(signed, rho)
        r = residue(word)
        requested = (keys[i - 1], tuple(raw))
        if requested not in artifact_pairs:
            binding_bad = True
        row: dict[str, object] = {
            "index": i,
            "input_target_key": keys[i - 1],
            "target_key": keys[i - 1] if requested in artifact_pairs else None,
            "residue_hex": format(r, "x"),
        }
        rows.append(row)
        if r:
            failure = dict(row)
            failure["norm_word"] = word
            failures.append(failure)
    input_pairs = {(key, tuple(raw)) for raw, key in zip(roofs, keys)}
    if input_pairs != artifact_pairs or len(input_pairs) != ROOF_COUNT:
        binding_bad = True
    if failures and not rel_bad and not rho_bad:
        status = "DEFECT_CANDIDATE" if not binding_bad else "DEFECT_UNBOUND"
    elif failures:
        status = "UNKNOWN_GATE_FAIL"
    elif binding_bad:
        status = "ALLPASS_UNBOUND"
    else:
        status = "ALLPASS_UNKNOWN"
    return {
        "degree": d,
        "monomial_count": SHARD.monomial_count(d),
        "ideal_rank": len(basis),
        "quotient_dimension": SHARD.monomial_count(d) - len(basis),
        "quotient_coordinate_dimension": quotient_dimension,
        "quotient_nonpivot_monomials": nonpivots,
        "relator_bad": rel_bad,
        "rho5_bad_generators": rho_bad,
        "roof_count": len(rows),
        "roof_defect_count": len(failures),
        "first_defect": failures[0] if failures else None,
        "rows": rows,
        "ideal_basis_hex": [format(basis[p], "x") for p in sorted(basis)],
        "ideal_basis_pivots": sorted(basis),
        "artifact_binding": {
            "available": True,
            "status": "PASS" if not binding_bad else "FAIL_OR_MISSING",
            "artifact_sha256": artifact_meta["sha256"],
            "legacy_empty_rows": artifact_meta.get("legacy_empty_rows", []),
        },
        "status": status,
        "method": "F2 noncommutative truncated algebra; merged complete two-sided monomial ideal v2",
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--degree", type=int, required=True)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--artifact", type=Path, required=True)
    ap.add_argument("--shard", type=Path, action="append")
    ap.add_argument("--shard-dir", type=Path)
    ap.add_argument("--shard-count", type=int)
    ap.add_argument("--pattern", default="d972_b4_magnus_d{count}_shard_{index}_of_{count}.json",
                    help="format string for --shard-dir; {index} and {count} are replaced")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    if args.degree < 1 or args.degree > SHARD.MAX_DEGREE:
        raise ValueError(f"degree must be in 1..{SHARD.MAX_DEGREE}")
    started = time.monotonic()
    obj, input_sha, digests = load_input(args.input)
    if obj.get("rho_words") != CANONICAL_RHO:
        raise ValueError("legacy rho map rejected; require universal_v2 canonical rho")
    paths = discover_shards(args)
    basis, shard_records = load_shards(paths, args.degree, input_sha, digests)
    artifact_pairs, artifact_meta = PRODUCER.load_word_key_pairs(args.artifact)
    if artifact_meta.get("legacy_empty_rows"):
        raise ValueError("legacy empty-string artifact rows rejected; use corrected archive")
    row = evaluate(obj, args.degree, basis, artifact_pairs, artifact_meta)
    result: dict[str, object] = {
        "schema": "d972-b4-magnus-ideal/v2",
        "status": "CANDIDATE_RECEIPT",
        "input_path": str(args.input),
        "input_sha256": input_sha,
        "input_digests": digests,
        "rho_words_source": obj.get("rho_words_source", "universal_v2_canonical"),
        "artifact": {"path": str(args.artifact), "error": None,
                     "sha256": artifact_meta["sha256"]},
        "model": {
            "field": "F2", "generators": NGEN,
            "truncation": "all monomials of degree > d",
            "inverse": "(1+X_i)^-1=sum_{k=0}^d X_i^k",
            "ideal": "two-sided span of u*(E(r)-1)*v for all monomials u,v",
            "finite_unit_group": "subgroup of units of finite-dimensional F2 algebra",
        },
        "shards": shard_records,
        "source": {"merge_script": str(Path(__file__)), "merge_sha256": file_sha(Path(__file__)),
                   "producer_script": str(PRODUCER_PATH), "producer_sha256": file_sha(PRODUCER_PATH),
                   "shard_script": str(SHARD_PATH), "shard_sha256": file_sha(SHARD_PATH)},
        "degrees": {str(args.degree): row},
    }
    status = row["status"]
    if status == "DEFECT_CANDIDATE":
        result["status"] = "DEFECT_CANDIDATE_NEEDS_INDEPENDENT_CHECK"
    elif status == "DEFECT_UNBOUND":
        result["status"] = "DEFECT_BUT_WORD_KEY_UNBOUND"
    elif status == "ALLPASS_UNKNOWN":
        result["status"] = "ALLPASS_GRADING_UNKNOWN"
    else:
        result["status"] = "CANDIDATE_RECEIPT"
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
                            encoding="utf-8")
    print(json.dumps({"status": result["status"], "degree": args.degree,
                      "ideal_rank": row["ideal_rank"], "roof_defect_count": row["roof_defect_count"],
                      "output": str(args.output), "elapsed_seconds": result["elapsed_seconds"]},
                     sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, sort_keys=True),
              file=sys.stderr, flush=True)
        raise
