#!/usr/bin/env python3
"""Prepare a bounded, runner-generated B4 SAT job matrix.

The matrix is derived from the independently authenticated word/key archive.
The planner removes both copies of the empty roof and keeps exactly one row
for each nonempty signed word, ordered shortest-first.  Each matrix entry is
one degree/shard pair; no CNF is written by this preparation step.

This is finite exploration only.  An UNSAT shard excludes that degree and
shard, never the universal B4 statement.  A SAT result still requires the
independent model checker before it is a B4-A candidate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from plan_d972_b4_unique_roof_shards_v1 import build, load


def parse_int_list(raw: str, *, name: str, low: int, high: int) -> list[int]:
    values: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            value = int(part)
        except ValueError as exc:
            raise ValueError(f"{name} contains a non-integer: {part!r}") from exc
        if not low <= value <= high:
            raise ValueError(f"{name} value outside [{low},{high}]: {value}")
        values.append(value)
    if not values or len(set(values)) != len(values):
        raise ValueError(f"{name} must contain distinct values")
    return values


def parse_shards(raw: str, shard_count: int) -> list[int]:
    if raw.strip().lower() == "all":
        return list(range(shard_count))
    values = parse_int_list(raw, name="shards", low=0, high=max(0, shard_count - 1))
    return values


def prepare(rows: list[list[Any]], *, shard_size: int,
            max_word_length: int | None, degrees: list[int],
            shards_raw: str) -> dict[str, Any]:
    if shard_size < 2:
        raise ValueError("OR SAT shard-size must be at least two")
    plan = build(rows, shard_size, max_word_length)
    selected_shards = parse_shards(shards_raw, len(plan["shards"]))
    by_shard = {int(item["shard"]): item for item in plan["shards"]}
    matrix = []
    for shard in selected_shards:
        item = by_shard[shard]
        if int(item["word_count"]) < 2:
            raise ValueError(
                f"selected shard {shard} has fewer than two nonempty words")
        for degree in degrees:
            matrix.append({
                "degree": degree,
                "shard": shard,
                "word_count": item["word_count"],
                "min_word_length": item["min_word_length"],
                "max_word_length": item["max_word_length"],
            })
    if not matrix:
        raise ValueError("matrix is empty")
    return {
        "schema": "d972-b4-sat-matrix/v1",
        "bounded_status": "FINITE_CANDIDATE_ONLY",
        "shard_size": shard_size,
        "max_word_length": max_word_length,
        "degrees": degrees,
        "selected_shards": selected_shards,
        "plan": plan,
        "matrix": matrix,
        "interpretation": (
            "UNSAT is finite-degree/shard UNKNOWN; SAT requires the independent "
            "model checker and is only a B4-A candidate."
        ),
    }


def self_test() -> None:
    assert parse_int_list("2,4,8", name="degrees", low=2, high=8) == [2, 4, 8]
    assert parse_shards("all", 3) == [0, 1, 2]
    try:
        parse_int_list("2,2", name="degrees", low=2, high=8)
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate degree accepted")
    try:
        parse_shards("3", 3)
    except ValueError:
        pass
    else:
        raise AssertionError("out-of-range shard accepted")
    try:
        prepare([], shard_size=1, max_word_length=40, degrees=[8],
                shards_raw="all")
    except ValueError as exc:
        assert "shard-size" in str(exc)
    else:
        raise AssertionError("singleton OR shard-size accepted")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--artifact", type=Path)
    ap.add_argument("--shard-size", type=int, default=8)
    ap.add_argument("--max-word-length", type=int, default=40)
    ap.add_argument("--degrees", default="2,3,4,5,6,7,8")
    ap.add_argument("--shards", default="all")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    if args.self_test:
        self_test()
        print("D972_B4_SAT_MATRIX_SELFTEST_PASS")
        return 0
    if args.artifact is None or args.output is None:
        ap.error("--artifact and --output are required unless --self-test is used")
    if args.shard_size < 2:
        ap.error("--shard-size must be at least two for OR SAT")
    if args.max_word_length < 1:
        ap.error("--max-word-length must be positive")
    degrees = parse_int_list(args.degrees, name="degrees", low=2, high=8)
    result = prepare(
        load(args.artifact), shard_size=args.shard_size,
        max_word_length=args.max_word_length, degrees=degrees,
        shards_raw=args.shards,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "status": "MATRIX_PASS",
        "matrix_count": len(result["matrix"]),
        "shard_count": len(result["selected_shards"]),
        "unique_word_count": result["plan"]["unique_word_count"],
        "empty_rows_excluded": result["plan"]["empty_rows_excluded"],
        "duplicate_copies_excluded": result["plan"]["duplicate_copies_excluded"],
        "artifact_sha256": result["plan"]["artifact_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
