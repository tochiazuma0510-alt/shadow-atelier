#!/usr/bin/env python3
"""A0 batch-64 v29: replay raw streamed rows through the frozen reducer."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V28 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_batch64_v28.py")
_V28_BYTES = 19149
_V28_SHA256 = "ff26d11c23b45b70a1fc93d481bfd4f3dd66e6c106fd0afae140af81ec01ddf9"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("batch64 v29 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("batch64 v29 " + label + " result cardinality")
    return result


_raw = _V28.read_bytes()
if len(_raw) != _V28_BYTES or hashlib.sha256(_raw).hexdigest() != _V28_SHA256:
    raise SystemExit("batch64 v29 frozen v28 owner drift")
_scope = {"__file__": str(_V28), "__name__": "_r07_batch64_v28_for_v29"}
exec(compile(_raw, str(_V28), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("batch64 v29 generated v28 owner missing")

_OLD = b'''def _stream_record(search, record):
    live = search.runtime["live"]; expected = len(search.new_records) + 1
    require(record.get("symbol") == f"n:{expected:04d}" and record.get("family") in ("boundary", "correction"),
            "v7 new record order")
    row = live.parse_sparse(record["sparse_row"])
    require(live.public_sparse(row) == record["sparse_row"] and
            record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]), "v7 new row restore")
    pivot = bytes.fromhex(record["pivot_hex"]); pivot_node_id = int(record["pivot_node_id"])
    require(pivot_node_id in range(len(search.reducer.ancestry.nodes)), "v7 new pivot DAG binding")
    search.reducer.inject(pivot, row, {record["symbol"]: 1}, expression_node=pivot_node_id)
    search.new_records.append(record)

'''
_NEW = b'''def _stream_record(search, record):
    live = search.runtime["live"]; expected = len(search.new_records) + 1
    require(record.get("symbol") == f"n:{expected:04d}" and
            record.get("family") in ("boundary", "correction"),
            "v29 streamed raw record order")
    raw_row = live.parse_sparse(record["sparse_row"])
    require(live.public_sparse(raw_row) == record["sparse_row"] and
            record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]),
            "v29 streamed raw row authentication")
    stored_pivot = bytes.fromhex(record["pivot_hex"])
    stored_node = int(record["pivot_node_id"])
    require(stored_node in range(len(search.reducer.ancestry.nodes)),
            "v29 stored pivot DAG binding")
    before_rank = len(search.reducer.order)
    require(record.get("rank_before") == before_rank and
            record.get("rank_after") == before_rank + 1,
            "v29 streamed sequential rank")
    before_nodes = len(search.reducer.ancestry.nodes)
    before_dag_meter = search.meter.counters["dag_node_allocations"]
    before_formal = search.reducer.formal_entries
    before_support = search.reducer.dag_support_allocations
    owner_meter = search.reducer.meter
    search.reducer.meter = None
    try:
        derived_pivot, derived_node = search.reducer.add_actual(
            raw_row, record["symbol"])
    finally:
        search.reducer.meter = owner_meter
    require(len(search.reducer.ancestry.nodes) == before_nodes and
            search.meter.counters["dag_node_allocations"] == before_dag_meter,
            "v29 streamed replay allocated a fresh DAG node")
    require(derived_pivot == stored_pivot and derived_node == stored_node,
            "v29 streamed derived pivot/node binding")
    normalized = search.reducer.rows[derived_pivot]
    require(normalized and min(normalized) == derived_pivot and
            normalized[derived_pivot] == 1 and
            search.reducer.expr_ids[derived_pivot] == derived_node and
            len(search.reducer.order) == before_rank + 1 and
            search.reducer.formal_entries == before_formal + 1 and
            search.reducer.dag_support_allocations == before_support + 1,
            "v29 streamed normalized row/rank accounting")
    search.new_records.append(record)

'''
_patched = _swap(_patched, _OLD, _NEW, "raw streamed row replay")

if (_patched.count(b'def _stream_record') != 1 or
        _patched.count(b'derived_pivot, derived_node = search.reducer.add_actual') != 1 or
        _OLD in _patched or
        _patched.count(b'def _stream_pre_records') != 1 or
        _patched.count(b'def _stream_post_parse') != 1 or
        b'restore_checkpoint(search, resume_path)' in _patched or
        _patched.count(b'def materialize_batch') != 1):
    raise SystemExit("batch64 v29 generated owner gate")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
