#!/usr/bin/env python3
"""Plan sound degree-8 SAT shards for the exact B4 roof table.

The 972 archived rows contain each signed roof word twice.  A finite
permutation defect depends on the word, not on the duplicated target key, so
one representative per word is a mathematically lossless bounded search.
This planner is intentionally independent of the GAP producer and of the SAT
encoder: it authenticates the archived canonical digest, proves the
two-copies-per-word property, and emits deterministic original row indices.

An all-pass result for every shard is still only a bounded finite-image
UNKNOWN; a SAT model with a nonidentity roof defect is a B4-A candidate and
must be checked by the independent model checker.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

TARGET_DIGEST = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_DIGEST = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
ARTIFACT_DIGEST = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def load(path: Path) -> list[list[Any]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or obj.get("schema") != "d972-b4-word-key-artifact/v1":
        raise ValueError("word/key artifact schema drift")
    if obj.get("count") != 972 or obj.get("source_target_key_digest") != TARGET_DIGEST:
        raise ValueError("word/key artifact metadata drift")
    if obj.get("frozen_tuple_sha256") != TUPLE_DIGEST:
        raise ValueError("word/key tuple digest drift")
    rows = obj.get("rows")
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word/key artifact row count")
    if obj.get("canonical_bytes_sha256") != sha(rows) or sha(rows) != ARTIFACT_DIGEST:
        raise ValueError("word/key artifact canonical digest drift")
    for i, row in enumerate(rows):
        if (not isinstance(row, list) or len(row) != 3 or
                not isinstance(row[0], int) or not isinstance(row[1], list) or
                not isinstance(row[2], list) or
                any(not isinstance(x, int) or x == 0 or abs(x) > 6 for x in row[2])):
            raise ValueError(f"malformed word/key row {i}")
    return rows


def build(rows: list[list[Any]], shard_size: int,
          max_word_length: int | None = None) -> dict[str, Any]:
    if shard_size < 1:
        raise ValueError("shard size must be positive")
    if max_word_length is not None and max_word_length < 1:
        raise ValueError("max word length must be positive")
    by_word: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        by_word[tuple(row[2])].append(i)
    multiplicities = Counter(len(v) for v in by_word.values())
    if multiplicities != Counter({2: 486}):
        raise ValueError(f"expected 486 words with multiplicity two, got {multiplicities}")
    empty_rows = len(by_word.get((), []))
    if empty_rows != 2:
        raise ValueError(f"expected exactly two empty roof rows, got {empty_rows}")
    eligible = {
        word: indices for word, indices in by_word.items()
        if word and (max_word_length is None or len(word) <= max_word_length)
    }
    representatives = sorted(
        (indices[0] for indices in eligible.values()),
        key=lambda i: (len(rows[i][2]), tuple(rows[i][2]), i),
    )
    if len(set(representatives)) != len(representatives):
        raise ValueError("unique representative count drift")
    if any(not rows[i][2] for i in representatives):
        raise ValueError("empty roof selected")
    selected_histogram = Counter(len(rows[i][2]) for i in representatives)
    selected_word_count = len(representatives)
    nonempty_word_count = len(by_word) - 1
    max_selected_length = max(selected_histogram) if selected_histogram else 0
    shards = []
    for ordinal, start in enumerate(range(0, len(representatives), shard_size)):
        indices = representatives[start:start + shard_size]
        shards.append({
            "shard": ordinal,
            "row_indices": indices,
            "word_count": len(indices),
            "min_word_length": min(len(rows[i][2]) for i in indices),
            "max_word_length": max(len(rows[i][2]) for i in indices),
            "words": [rows[i][2] for i in indices],
        })
    return {
        "schema": "d972-b4-sat-unique-roof-shard-plan/v1",
        "bounded_status": "FINITE_CANDIDATE_ONLY",
        "artifact_sha256": ARTIFACT_DIGEST,
        "target_key_digest": TARGET_DIGEST,
        "frozen_tuple_sha256": TUPLE_DIGEST,
        "row_count": len(rows),
        "unique_word_count": selected_word_count,
        "total_nonempty_unique_word_count": nonempty_word_count,
        "empty_word_count": 1,
        "empty_rows_excluded": empty_rows,
        "duplicate_copies_excluded": sum(len(v) - 1 for v in by_word.values()),
        "max_word_length_filter": max_word_length,
        "word_length_histogram": {str(k): v for k, v in sorted(selected_histogram.items())},
        "max_selected_word_length": max_selected_length,
        "multiplicity_histogram": {str(k): v for k, v in sorted(multiplicities.items())},
        "representative_indices": representatives,
        "shard_size": shard_size,
        "shards": shards,
        "interpretation": "Empty roofs and duplicate copies are excluded. All shard UNSAT excludes only degree-bounded permutation images; any checked SAT defect is B4-A candidate.",
    }


def self_test() -> None:
    rows = [
        [0, [0], []], [0, [1], []],
        [0, [2], [1]], [0, [3], [1]],
        [0, [4], [1, -2]], [0, [5], [1, -2]],
        [0, [6], [2]], [0, [7], [2]],
    ]
    # The production multiplicity histogram is intentionally strict; this
    # fixture tests the selection logic without pretending to be the archive.
    by_word: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        by_word[tuple(row[2])].append(i)
    assert len(by_word[()]) == 2
    reps = sorted(
        (v[0] for word, v in by_word.items() if word),
        key=lambda i: (len(rows[i][2]), tuple(rows[i][2]), i),
    )
    assert [rows[i][2] for i in reps] == [[1], [2], [1, -2]]
    assert not any(not rows[i][2] for i in reps)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--artifact", type=Path)
    ap.add_argument("--shard-size", type=int, default=8)
    ap.add_argument("--max-word-length", type=int)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    if args.self_test:
        self_test()
        print("D972_B4_SAT_SHARD_PLANNER_SELFTEST_PASS")
        return 0
    if args.artifact is None:
        ap.error("--artifact is required unless --self-test is used")
    if args.output is None:
        ap.error("--output is required unless --self-test is used")
    plan = build(load(args.artifact), args.shard_size, args.max_word_length)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PLAN_PASS",
        "unique_word_count": plan["unique_word_count"],
        "total_nonempty_unique_word_count": plan["total_nonempty_unique_word_count"],
        "empty_rows_excluded": plan["empty_rows_excluded"],
        "duplicate_copies_excluded": plan["duplicate_copies_excluded"],
        "max_word_length_filter": plan["max_word_length_filter"],
        "shard_count": len(plan["shards"]),
        "artifact_sha256": plan["artifact_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
