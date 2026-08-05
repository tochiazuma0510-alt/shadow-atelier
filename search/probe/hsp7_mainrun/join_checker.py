#!/usr/bin/env python3
"""join_checker.py -- HS mainrun shard-manifest join checker.

司令塔発注(便104認可事項3, sol/sol_reply_104_math31.md F104-1.3 逐語指定)の
実装。**探索器と照合器の分離**を守るため、本ファイルは以下しか行わない:

  - 入力は人工(synthetic)の shard manifest JSON のみ。705,894 候補宇宙の
    実データは一切読み込まない・参照しない(候補鍵の値そのものに数学的
    意味を持たせない -- あくまで「manifest の構造的整合性」だけを検査する)。
  - GAP の探索コード(search/*.g)・candidate_key_lib.g 等の predicate 実装を
    import しない・呼ばない。ここは join の構造検査のみを行う独立実装。

F104-1.3 が指定する両縁 fixture(逐語):
  - 正常な完全分割は PASS。
  - shard 一個欠落、candidate key 一個欠落、重複、区間 overlap、
    別 pcgs/endian、同じ flat index に別 key、
    receipt の run_id/run_attempt/sha/driver_digest 欠落は全て STOP。
  - shard の並び替えだけは集合として PASS し、結果の canonical sort/hash は
    同一になる。

設計方針(check の独立性): index_range は「shard 境界の申告」として overlap/
coverage(欠落 shard 検出)だけに使う。candidate_keys の実エントリは
index_range への所属を強制しない -- そうしないと「区間 overlap」と「同じ
flat index に別 key」が常に同じ経路(range overlap)でしか再現できず、
F104-1.3 が要求する 8 種の欠陥それぞれに対応する独立な fixture が作れない。
両者を独立した検査対象にすることで、各欠陥類型が意図した reason code で
STOP することを個別に確認できる。

Manifest schema (人工):
{
  "universe": {"pcgs_id": str, "endian": str, "total_flat_indices": int},
  "shards": [
    {
      "shard_id": str,
      "index_range": [lo, hi],           # inclusive flat-index interval (申告のみ)
      "pcgs_id": str,
      "endian": str,
      "candidate_keys": [{"flat_index": int, "key": <hashable-json-value>}, ...],
      "receipt": {"run_id": str, "run_attempt": str|int, "sha": str, "driver_digest": str}
    }, ...
  ]
}

Verdict: {"verdict": "PASS"|"STOP", "reason": str, "detail": {...},
          "canonical_sort_hash": <sha256 hex, only when PASS>}
"""

from __future__ import annotations

import hashlib
import json
import sys
from typing import Any


class JoinCheckError(Exception):
    """Carries a (reason_code, detail) pair for a STOP verdict."""

    def __init__(self, reason: str, detail: dict[str, Any] | None = None):
        super().__init__(reason)
        self.reason = reason
        self.detail = detail or {}


REQUIRED_UNIVERSE_FIELDS = ("pcgs_id", "endian", "total_flat_indices")
REQUIRED_RECEIPT_FIELDS = ("run_id", "run_attempt", "sha", "driver_digest")
REQUIRED_SHARD_FIELDS = ("shard_id", "index_range", "pcgs_id", "endian", "candidate_keys", "receipt")


def _key_to_hashable(key: Any) -> Any:
    """Make an arbitrary JSON value hashable/orderable for set/dict use."""
    if isinstance(key, dict):
        return tuple(sorted((k, _key_to_hashable(v)) for k, v in key.items()))
    if isinstance(key, list):
        return tuple(_key_to_hashable(v) for v in key)
    return key


def _check_universe(manifest: dict) -> dict:
    universe = manifest.get("universe")
    if not isinstance(universe, dict):
        raise JoinCheckError("MISSING_UNIVERSE", {"note": "manifest.universe is absent or not an object"})
    missing = [f for f in REQUIRED_UNIVERSE_FIELDS if f not in universe or universe[f] in (None, "")]
    if missing:
        raise JoinCheckError("MISSING_UNIVERSE_FIELD", {"missing_fields": missing})
    if not isinstance(universe["total_flat_indices"], int) or universe["total_flat_indices"] <= 0:
        raise JoinCheckError("INVALID_UNIVERSE_SIZE", {"total_flat_indices": universe.get("total_flat_indices")})
    return universe


def _check_shard_structure(shards: list) -> None:
    if not isinstance(shards, list) or len(shards) == 0:
        raise JoinCheckError("NO_SHARDS", {})
    for s in shards:
        if not isinstance(s, dict):
            raise JoinCheckError("MALFORMED_SHARD", {"shard": s})
        missing = [f for f in REQUIRED_SHARD_FIELDS if f not in s]
        if missing:
            raise JoinCheckError("MALFORMED_SHARD", {"shard_id": s.get("shard_id"), "missing_fields": missing})


def _check_receipts(shards: list) -> None:
    for s in shards:
        receipt = s.get("receipt")
        if not isinstance(receipt, dict):
            raise JoinCheckError("RECEIPT_FIELD_MISSING", {"shard_id": s["shard_id"], "note": "receipt is not an object"})
        missing = [f for f in REQUIRED_RECEIPT_FIELDS if f not in receipt or receipt[f] in (None, "")]
        if missing:
            raise JoinCheckError("RECEIPT_FIELD_MISSING", {"shard_id": s["shard_id"], "missing_fields": missing})


def _check_pcgs_endian(universe: dict, shards: list) -> None:
    for s in shards:
        if s.get("pcgs_id") != universe["pcgs_id"] or s.get("endian") != universe["endian"]:
            raise JoinCheckError(
                "PCGS_ENDIAN_MISMATCH",
                {
                    "shard_id": s["shard_id"],
                    "expected": {"pcgs_id": universe["pcgs_id"], "endian": universe["endian"]},
                    "actual": {"pcgs_id": s.get("pcgs_id"), "endian": s.get("endian")},
                },
            )


def _check_index_ranges(universe: dict, shards: list) -> None:
    """Range-only checks: overlap and full coverage of [0, n-1]. Deliberately
    does not look at candidate_keys content (see module docstring)."""
    n = universe["total_flat_indices"]
    intervals = []
    for s in shards:
        rng = s.get("index_range")
        if (
            not isinstance(rng, list)
            or len(rng) != 2
            or not all(isinstance(x, int) for x in rng)
            or rng[0] > rng[1]
            or rng[0] < 0
            or rng[1] >= n
        ):
            raise JoinCheckError("INVALID_INDEX_RANGE", {"shard_id": s["shard_id"], "index_range": rng})
        intervals.append((rng[0], rng[1], s["shard_id"]))

    by_lo = sorted(intervals, key=lambda t: (t[0], t[1]))
    for i in range(len(by_lo) - 1):
        lo1, hi1, id1 = by_lo[i]
        lo2, hi2, id2 = by_lo[i + 1]
        if lo2 <= hi1:
            raise JoinCheckError(
                "INDEX_RANGE_OVERLAP",
                {"shard_a": {"shard_id": id1, "range": [lo1, hi1]}, "shard_b": {"shard_id": id2, "range": [lo2, hi2]}},
            )

    covered = 0
    for lo, hi, _sid in by_lo:
        if lo != covered:
            raise JoinCheckError(
                "COVERAGE_GAP",
                {"expected_next_index": covered, "got_start": lo, "note": "likely a missing shard or hole in index_range coverage"},
            )
        covered = hi + 1
    if covered != n:
        raise JoinCheckError(
            "COVERAGE_GAP",
            {"expected_total": n, "got_covered_upto": covered, "note": "coverage ends before universe.total_flat_indices -- likely a missing shard"},
        )


def _check_candidate_keys(universe: dict, shards: list) -> dict[int, Any]:
    """Content-only checks over the union of all shards' candidate_keys
    entries: same flat_index claimed with two different keys, the same key
    value claimed at two different flat indices, and global under-coverage
    of the flat-index space. Deliberately independent of index_range (see
    module docstring)."""
    n = universe["total_flat_indices"]
    flat_index_to_key: dict[int, Any] = {}
    flat_index_to_shard: dict[int, str] = {}
    key_to_flat_indices: dict[Any, list[int]] = {}

    for s in shards:
        sid = s["shard_id"]
        for entry in s.get("candidate_keys", []):
            if not isinstance(entry, dict) or "flat_index" not in entry or "key" not in entry:
                raise JoinCheckError("MALFORMED_CANDIDATE_KEY_ENTRY", {"shard_id": sid, "entry": entry})
            fi = entry["flat_index"]
            key = entry["key"]
            hashable_key = _key_to_hashable(key)

            if fi in flat_index_to_key:
                if _key_to_hashable(flat_index_to_key[fi]) != hashable_key:
                    raise JoinCheckError(
                        "FLAT_INDEX_KEY_CONFLICT",
                        {
                            "flat_index": fi,
                            "shard_a": {"shard_id": flat_index_to_shard[fi], "key": flat_index_to_key[fi]},
                            "shard_b": {"shard_id": sid, "key": key},
                        },
                    )
                # identical (flat_index, key) reported twice is also a
                # structural defect (redundant/duplicated entry).
                raise JoinCheckError(
                    "DUPLICATE_CANDIDATE_KEY",
                    {"flat_index": fi, "shard_a": flat_index_to_shard[fi], "shard_b": sid, "note": "same (flat_index, key) entry reported more than once"},
                )
            flat_index_to_key[fi] = key
            flat_index_to_shard[fi] = sid
            key_to_flat_indices.setdefault(hashable_key, []).append(fi)

    dup_keys = {k: v for k, v in key_to_flat_indices.items() if len(v) > 1}
    if dup_keys:
        raise JoinCheckError(
            "DUPLICATE_CANDIDATE_KEY",
            {"note": "same candidate key value assigned to two different flat indices", "duplicated_keys_flat_indices": {str(k): v for k, v in dup_keys.items()}},
        )

    if len(flat_index_to_key) != n:
        missing = sorted(set(range(n)) - set(flat_index_to_key))
        raise JoinCheckError(
            "CANDIDATE_KEY_MISSING",
            {"expected_total": n, "got_total": len(flat_index_to_key), "missing_flat_indices": missing},
        )

    return flat_index_to_key


def _canonical_form(universe: dict, shards: list) -> dict:
    """Canonical representation: independent of shard list order and of
    candidate_keys entry order within a shard. Sorting key is (index_range
    start) for shards and flat_index for entries -- NOT any GAP-internal
    Elements()/BFS order (Sol F104-1.2 item 4 admonition, carried into the
    join layer for consistency)."""
    canon_shards = []
    for s in sorted(shards, key=lambda s: (s["index_range"][0], s["shard_id"])):
        canon_shards.append(
            {
                "shard_id": s["shard_id"],
                "index_range": s["index_range"],
                "pcgs_id": s["pcgs_id"],
                "endian": s["endian"],
                "candidate_keys": sorted(
                    ({"flat_index": e["flat_index"], "key": e["key"]} for e in s["candidate_keys"]),
                    key=lambda e: e["flat_index"],
                ),
                "receipt": {k: s["receipt"][k] for k in REQUIRED_RECEIPT_FIELDS},
            }
        )
    return {
        "universe": {k: universe[k] for k in REQUIRED_UNIVERSE_FIELDS},
        "shards": canon_shards,
    }


def check_join(manifest: dict) -> dict:
    """Run the full join check. STOP conditions are returned as a verdict
    dict (never raised) so callers can batch many fixtures uniformly."""
    try:
        universe = _check_universe(manifest)
        shards = manifest.get("shards")
        _check_shard_structure(shards)
        _check_receipts(shards)
        _check_pcgs_endian(universe, shards)
        _check_index_ranges(universe, shards)
        _check_candidate_keys(universe, shards)
        canon = _canonical_form(universe, shards)
        canon_bytes = json.dumps(canon, sort_keys=True, ensure_ascii=True).encode("utf-8")
        canon_hash = hashlib.sha256(canon_bytes).hexdigest()
        return {
            "verdict": "PASS",
            "reason": "complete_partition_no_conflicts",
            "detail": {"total_flat_indices": universe["total_flat_indices"], "shard_count": len(shards)},
            "canonical_sort_hash": canon_hash,
        }
    except JoinCheckError as e:
        return {"verdict": "STOP", "reason": e.reason, "detail": e.detail}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: join_checker.py <manifest.json>", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        manifest = json.load(f)
    result = check_join(manifest)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
