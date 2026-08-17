#!/usr/bin/env python3
"""Streaming/observable degree-6 Magnus shard merge.

This is a versioned execution wrapper around the audited v2 merge algebra.
It has the same shard schema, row-space operation, receipt schema, and
independent checker contract, but validates and merges one shard at a time
while emitting flushed progress records.  The previous v2 merge was silent
until its final receipt; on the 55,987-dimensional degree-6 lane that made a
long exact elimination indistinguishable from a hung process.

No mathematical shortcut is introduced here: every row from all 16 disjoint
shards is inserted into the same highest-pivot F2 basis before any roof is
evaluated.  The independent checker remains
``check_d972_b4_magnus_ideal_v1.py``.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Sequence


MERGE_PATH = Path(__file__).with_name("d972_b4_magnus_ideal_merge_v2.py")


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MERGE = import_module(MERGE_PATH, "d972_b4_magnus_ideal_merge_v2_for_stream")


def cj(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stream_load_shards(paths: Sequence[Path], degree: int, input_sha: str,
                       digests: dict[str, str]) -> tuple[dict[int, int], list[dict[str, object]]]:
    if not paths:
        raise ValueError("no shard files")
    common_count: int | None = None
    common_monomials = MERGE.SHARD.monomial_count(degree)
    seen: set[int] = set()
    coverage: list[int] = []
    basis: dict[int, int] = {}
    records: list[dict[str, object]] = []
    started = time.monotonic()
    dual: list[int] | None = None
    for shard_no, path in enumerate(paths, 1):
        print(json.dumps({"event": "shard_begin", "ordinal": shard_no,
                          "total": len(paths), "path": str(path)}, sort_keys=True),
              flush=True)
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj.get("schema") != "d972-b4-magnus-ideal-shard/v2":
            raise ValueError(f"shard schema drift: {path}")
        if obj.get("degree") != degree:
            raise ValueError(f"shard degree drift: {path}")
        count = obj.get("shard_count")
        index = obj.get("shard_index")
        if not isinstance(count, int) or not isinstance(index, int) or count < 1 or not 0 <= index < count:
            raise ValueError(f"invalid shard index/count: {path}")
        if common_count is None:
            common_count = count
        elif count != common_count:
            raise ValueError("shard-count mismatch")
        if index in seen:
            raise ValueError("duplicate shard index")
        seen.add(index)
        if obj.get("input_sha256") != input_sha or obj.get("input_digests") != digests:
            raise ValueError(f"shard input binding drift: {path}")
        if obj.get("monomial_count") != common_monomials:
            raise ValueError(f"shard monomial count drift: {path}")
        expected = MERGE.expected_indices(index, count)
        indices = obj.get("relator_indices")
        if indices != expected:
            raise ValueError(f"shard assignment drift: {path}")
        if obj.get("relator_indices_sha256") != sha(cj(expected)):
            raise ValueError(f"shard assignment digest drift: {path}")
        rows = obj.get("ideal_basis_hex")
        pivots = obj.get("ideal_basis_pivots")
        if not isinstance(rows, list) or not isinstance(pivots, list) or len(rows) != len(pivots):
            raise ValueError(f"shard basis shape drift: {path}")
        if obj.get("ideal_rank") != len(rows):
            raise ValueError(f"shard rank drift: {path}")
        row_count = len(rows)
        for row_no, (encoded, pivot) in enumerate(zip(rows, pivots), 1):
            row = MERGE.parse_row(encoded, common_monomials)
            if row.bit_length() - 1 != int(pivot):
                raise ValueError(f"shard pivot drift: {path} row {row_no}")
            if dual is None:
                MERGE.add_high_basis(basis, row)
            else:
                dual, independent = dual_insert(dual, row)
                if independent:
                    # The dual test rejects dependent rows without a costly
                    # full reduction.  Only new rows enter the receipt basis.
                    MERGE.add_high_basis(basis, row)
            if row_no % 10000 == 0:
                print(json.dumps({"event": "row_progress", "shard_index": index,
                                  "row": row_no, "rows": len(rows),
                                  "merged_rank": len(basis),
                                  "dual_nullity": len(dual) if dual is not None else None},
                             sort_keys=True), flush=True)
        coverage.extend(int(x) for x in indices)
        record = {"path": str(path), "sha256": sha(path.read_bytes()),
                  "shard_index": index, "shard_count": count,
                  "relator_count": len(indices), "ideal_rank": row_count}
        records.append(record)
        # A degree-6 shard carries tens of thousands of 7-KB Python integer
        # bitsets.  Do not retain the parsed JSON strings while the next
        # 100--300 MB shard is being loaded; otherwise Windows may terminate
        # the worker at an otherwise silent peak before an exception exists.
        del obj, rows, pivots, indices, expected
        gc.collect()
        if dual is None and common_monomials - len(basis) <= 512:
            dual = build_dual_nullspace(basis, common_monomials)
            print(json.dumps({"event": "dual_switch", "merged_rank": len(basis),
                              "dual_nullity": len(dual)}, sort_keys=True), flush=True)
        print(json.dumps({"event": "shard_done", "shard_index": index,
                          "shard_rank": row_count, "merged_rank": len(basis),
                          "elapsed_seconds": round(time.monotonic() - started, 3)},
                         sort_keys=True), flush=True)
    if common_count is None or seen != set(range(common_count)):
        raise ValueError(f"incomplete shard set: {sorted(seen)}")
    if sorted(coverage) != list(range(1, MERGE.RELATOR_COUNT + 1)):
        raise ValueError("shard relator coverage drift")
    return basis, sorted(records, key=lambda item: int(item["shard_index"]))


def discover(args: argparse.Namespace) -> list[Path]:
    return MERGE.discover_shards(args)


def build_dual_nullspace(basis: dict[int, int], dimension: int) -> list[int]:
    """Construct exact left-nullspace functionals for a high-pivot basis."""
    free = [i for i in range(dimension) if i not in basis]
    dual: list[int] = []
    for coordinate in free:
        functional = 1 << coordinate
        # Each row has only lower bits besides its own high pivot.  Solving
        # pivots from low to high therefore makes the functional annihilate
        # every row exactly over F2.
        for pivot in sorted(basis):
            if (basis[pivot] & functional).bit_count() & 1:
                functional |= 1 << pivot
        dual.append(functional)
    if any((row & functional).bit_count() & 1
           for row in basis.values() for functional in dual):
        raise ValueError("dual nullspace construction failed")
    return dual


def dual_syndrome(dual: Sequence[int], row: int) -> int:
    syndrome = 0
    for index, functional in enumerate(dual):
        if (row & functional).bit_count() & 1:
            syndrome |= 1 << index
    return syndrome


def dual_insert(dual: list[int], row: int) -> tuple[list[int], bool]:
    """Update the dual after a row; return whether the row was independent."""
    syndrome = dual_syndrome(dual, row)
    if syndrome == 0:
        return dual, False
    pivot = (syndrome & -syndrome).bit_length() - 1
    pivot_functional = dual[pivot]
    return [functional ^ pivot_functional
            if ((syndrome >> index) & 1) else functional
            for index, functional in enumerate(dual) if index != pivot], True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--shard", type=Path, action="append")
    parser.add_argument("--shard-dir", type=Path)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--pattern", default="d972_b4_magnus_d{count}_shard_{index}_of_{count}.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.degree < 1 or args.degree > MERGE.SHARD.MAX_DEGREE:
        raise ValueError("degree outside audited shard range")
    started = time.monotonic()
    obj, input_sha, digests = MERGE.load_input(args.input)
    paths = discover(args)
    print(json.dumps({"event": "merge_start", "degree": args.degree,
                      "shard_count": len(paths), "monomial_count": MERGE.SHARD.monomial_count(args.degree),
                      "input_sha256": input_sha}, sort_keys=True), flush=True)
    basis, records = stream_load_shards(paths, args.degree, input_sha, digests)
    print(json.dumps({"event": "basis_complete", "ideal_rank": len(basis),
                      "quotient_dimension": MERGE.SHARD.monomial_count(args.degree) - len(basis)},
                     sort_keys=True), flush=True)
    pairs, artifact_meta = MERGE.PRODUCER.load_word_key_pairs(args.artifact)
    if artifact_meta.get("legacy_empty_rows"):
        raise ValueError("legacy empty word-key rows rejected")
    row = MERGE.evaluate(obj, args.degree, basis, pairs, artifact_meta)
    result: dict[str, object] = {
        "schema": "d972-b4-magnus-ideal/v2",
        "status": "CANDIDATE_RECEIPT",
        "input_path": str(args.input), "input_sha256": input_sha,
        "input_digests": digests,
        "rho_words_source": obj.get("rho_words_source", "universal_v2_canonical"),
        "artifact": {"path": str(args.artifact), "error": None, "sha256": artifact_meta["sha256"]},
        "model": {"field": "F2", "generators": MERGE.NGEN,
                  "truncation": "all monomials of degree > d",
                  "inverse": "(1+X_i)^-1=sum_{k=0}^d X_i^k",
                  "ideal": "two-sided span of u*(E(r)-1)*v for all monomials u,v",
                  "finite_unit_group": "subgroup of units of finite-dimensional F2 algebra"},
        "shards": records,
        "source": {"merge_script": str(Path(__file__)), "merge_sha256": sha(Path(__file__).read_bytes()),
                   "base_merge_script": str(MERGE_PATH), "base_merge_sha256": sha(MERGE_PATH.read_bytes())},
        "degrees": {str(args.degree): row},
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if row["status"] == "DEFECT_CANDIDATE":
        result["status"] = "DEFECT_CANDIDATE_NEEDS_INDEPENDENT_CHECK"
    elif row["status"] == "ALLPASS_UNKNOWN":
        result["status"] = "ALLPASS_GRADING_UNKNOWN"
    elif row["status"] == "DEFECT_UNBOUND":
        result["status"] = "DEFECT_BUT_WORD_KEY_UNBOUND"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
                            encoding="utf-8")
    print(json.dumps({"event": "merge_done", "status": result["status"],
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
