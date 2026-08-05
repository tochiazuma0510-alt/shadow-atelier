#!/usr/bin/env python3
"""join_fixtures_gen.py -- builds the artificial (synthetic) shard-manifest
fixtures required by sol/sol_reply_104_math31.md F104-1.3's join-fixture
spec, and the join_fixtures_run.py test runner asserts each against its
expected verdict via search/probe/hsp7_mainrun/join_checker.py.

宇宙は完全に人工(toy): total_flat_indices=5, candidate key = {"m": int,
"e1": int} (F104-1.3の pcgs 6-tuple 形式の縮小版 -- ここでは join の構造検査
だけが対象で候補の数学的中身は無関係なので、705,894 候補データは一切
使わない)。pcgs_id/endian は固定の識別子文字列。
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "join_fixtures"

UNIVERSE = {"pcgs_id": "toy_pcgs_v1", "endian": "big", "total_flat_indices": 5}

RECEIPT_A = {"run_id": "17012345678", "run_attempt": "1", "sha": "aaaa1111bbbb2222", "driver_digest": "driverA-sha256-0001"}
RECEIPT_B = {"run_id": "17012345679", "run_attempt": "1", "sha": "cccc3333dddd4444", "driver_digest": "driverB-sha256-0002"}

KEYS = [{"m": 0, "e1": i} for i in range(5)]  # flat_index i <-> KEYS[i]


def _shard(shard_id, lo, hi, entries, receipt, pcgs_id="toy_pcgs_v1", endian="big"):
    return {
        "shard_id": shard_id,
        "index_range": [lo, hi],
        "pcgs_id": pcgs_id,
        "endian": endian,
        "candidate_keys": entries,
        "receipt": receipt,
    }


def _entries(indices):
    return [{"flat_index": i, "key": KEYS[i]} for i in indices]


def build_good():
    """正常な完全分割: shard0=[0,2], shard1=[3,4], 全5件を過不足なく被覆。"""
    return {
        "universe": UNIVERSE,
        "shards": [
            _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
            _shard("shard1", 3, 4, _entries([3, 4]), RECEIPT_B),
        ],
    }


def build_reorder():
    """shard の並び替えだけ(shard1 が先・shard0 が後、各 shard 内の
    candidate_keys も逆順)。集合として good と同一 -> PASS かつ
    canonical_sort_hash が good と同一になるはず。"""
    good = build_good()
    shards = copy.deepcopy(good["shards"])
    shards.reverse()
    for s in shards:
        s["candidate_keys"] = list(reversed(s["candidate_keys"]))
    return {"universe": UNIVERSE, "shards": shards}


def build_missing_shard():
    """shard 一個欠落: shard1 がまるごと存在しない(shard0 のみ、
    universe.total_flat_indices=5 のまま)。"""
    return {
        "universe": UNIVERSE,
        "shards": [
            _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
        ],
    }


def build_missing_candidate_key():
    """candidate key 一個欠落: shard1 の flat_index=4 のエントリが抜けている
    (index_range は[3,4]のまま申告)。"""
    return {
        "universe": UNIVERSE,
        "shards": [
            _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
            _shard("shard1", 3, 4, _entries([3]), RECEIPT_B),
        ],
    }


def build_duplicate_key():
    """候補鍵の重複: 異なる flat_index (1 と 4) に全く同じ key 値
    {"m":0,"e1":1} を(誤って)割り当てている。"""
    shards = [
        _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
        _shard("shard1", 3, 4, [{"flat_index": 3, "key": KEYS[3]}, {"flat_index": 4, "key": KEYS[1]}], RECEIPT_B),
    ]
    return {"universe": UNIVERSE, "shards": shards}


def build_overlap():
    """区間overlap: shard0=[0,2], shard1=[2,4] (index=2が重複区間)。
    このfixtureは range メタデータのみで検出されるべきで、実際に
    candidate_keys の中身が食い違っているかどうかは無関係(shard1側は
    index=2を自分のリストに含めない=中身レベルでは無害でも、overlap
    そのものをrangeメタデータだけでSTOPさせる設計を確認する)。"""
    return {
        "universe": UNIVERSE,
        "shards": [
            _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
            _shard("shard1", 2, 4, _entries([3, 4]), RECEIPT_B),
        ],
    }


def build_pcgs_endian_mismatch():
    """別pcgs/endian: shard1が universe と異なる pcgs_id を申告。"""
    return {
        "universe": UNIVERSE,
        "shards": [
            _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
            _shard("shard1", 3, 4, _entries([3, 4]), RECEIPT_B, pcgs_id="toy_pcgs_v2_DIFFERENT", endian="little"),
        ],
    }


def build_same_flat_index_different_key():
    """同一 flat index に別 key: index_range は overlap しない(shard0=[0,2],
    shard1=[3,4])が、shard1 の candidate_keys に(バグにより)flat_index=2
    のエントリが混入し、shard0 が申告する key と異なる値を主張する。"""
    shards = [
        _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
        _shard(
            "shard1",
            3,
            4,
            [
                {"flat_index": 2, "key": {"m": 9, "e1": 9}},  # conflicts with shard0's key for flat_index=2
                {"flat_index": 3, "key": KEYS[3]},
                {"flat_index": 4, "key": KEYS[4]},
            ],
            RECEIPT_B,
        ),
    ]
    return {"universe": UNIVERSE, "shards": shards}


def build_receipt_missing_field():
    """receipt の run_id/run_attempt/sha/driver_digest 欠落: shard1 の
    receipt から 'sha' フィールドが欠落。"""
    bad_receipt = {k: v for k, v in RECEIPT_B.items() if k != "sha"}
    return {
        "universe": UNIVERSE,
        "shards": [
            _shard("shard0", 0, 2, _entries([0, 1, 2]), RECEIPT_A),
            _shard("shard1", 3, 4, _entries([3, 4]), bad_receipt),
        ],
    }


FIXTURES = {
    "good": (build_good, "PASS", None),
    "reorder": (build_reorder, "PASS", None),
    "missing_shard": (build_missing_shard, "STOP", "COVERAGE_GAP"),
    "missing_candidate_key": (build_missing_candidate_key, "STOP", "CANDIDATE_KEY_MISSING"),
    "duplicate_key": (build_duplicate_key, "STOP", "DUPLICATE_CANDIDATE_KEY"),
    "overlap": (build_overlap, "STOP", "INDEX_RANGE_OVERLAP"),
    "pcgs_endian_mismatch": (build_pcgs_endian_mismatch, "STOP", "PCGS_ENDIAN_MISMATCH"),
    "same_flat_index_different_key": (build_same_flat_index_different_key, "STOP", "FLAT_INDEX_KEY_CONFLICT"),
    "receipt_missing_field": (build_receipt_missing_field, "STOP", "RECEIPT_FIELD_MISSING"),
}


def write_all():
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    for name, (builder, _expected_verdict, _expected_reason) in FIXTURES.items():
        manifest = builder()
        path = FIXTURE_DIR / f"{name}.json"
        path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    write_all()
