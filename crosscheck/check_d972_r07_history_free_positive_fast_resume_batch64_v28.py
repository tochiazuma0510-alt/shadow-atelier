#!/usr/bin/env python3
"""Independent checker v28 for the globally merged A0 batch-64 owner."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V27 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v27.py")
_V27_BYTES = 1964
_V27_SHA256 = "181553ce338d1ef65e9ca275a41b157c2e4f8f4a8ca8616a63f3b5a144a045a3"
_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_batch64_v28.py"
_PRODUCER_BYTES = 19149
_PRODUCER_SHA256 = "ff26d11c23b45b70a1fc93d481bfd4f3dd66e6c106fd0afae140af81ec01ddf9"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("batch64 checker v28 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("batch64 checker v28 " + label + " result cardinality")
    return result


def _replace_region(source: bytes, start: bytes, stop: bytes,
                    replacement: bytes, label: str) -> bytes:
    if source.count(start) != 1 or source.count(stop) != 1:
        raise SystemExit("batch64 checker v28 " + label + " boundary cardinality")
    left = source.index(start); right = source.index(stop, left)
    if right <= left:
        raise SystemExit("batch64 checker v28 " + label + " boundary order")
    return source[:left] + replacement + source[right:]


_raw = _V27.read_bytes()
if len(_raw) != _V27_BYTES or hashlib.sha256(_raw).hexdigest() != _V27_SHA256:
    raise SystemExit("batch64 checker v28 frozen v27 owner drift")
_scope = {"__file__": str(_V27), "__name__": "_r07_v27_checker_for_batch64_v28"}
exec(compile(_raw, str(_V27), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("batch64 checker v28 generated v27 owner missing")
_old_pin = (b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v26.py",\n'
            b'                5950,\n'
            b'                "4ae9de2eaf0ae337d48309f107fe7aef94afe3783ee2bde63b7c839364e1098e")')
_new_pin = (f'PRODUCER_PIN = ("{_PRODUCER}",\n'
            f'                {_PRODUCER_BYTES},\n'
            f'                "{_PRODUCER_SHA256}")').encode("ascii")
_patched = _swap(_patched, _old_pin, _new_pin, "producer pin")
_patched = _swap(
    _patched,
    b'    epoch = provenance.get("boundary_epoch")\n'
    b'    if epoch is not None:\n'
    b'        expected_epoch = independent_boundary_outcome(runtime, dual, workers,\n'
    b'                                                       int(epoch["epoch"]))\n'
    b'        require(epoch == expected_epoch, "selected boundary epoch replay")\n'
    b'    return row',
    b'    epoch = provenance.get("boundary_epoch")\n'
    b'    batch = provenance.get("batch_selection")\n'
    b'    require(not (epoch is not None and batch is not None),\n'
    b'            "exclusive boundary epoch provenance")\n'
    b'    if batch is not None:\n'
    b'        require(set(provenance) == {"family", "block",\n'
    b'                "base_relator_index", "translation_hex", "scalar",\n'
    b'                "complete_support_occurrence_accumulation",\n'
    b'                "left_translation_gate", "contributing_pairs",\n'
    b'                "batch_selection"} and type(batch) is dict and\n'
    b'                set(batch) == {"schema", "batch_cap", "epoch",\n'
    b'                    "dual_sha256", "global_active_index_count",\n'
    b'                    "selected_count", "selected_batch_sha256",\n'
    b'                    "expanded_pair_count", "parent_pair_visits",\n'
    b'                    "selected_position", "selected_index",\n'
    b'                    "selected_scalar"} and\n'
    b'                batch.get("schema") == SCHEMA + "/global-batch-selection/v28" and\n'
    b'                batch.get("batch_cap") == 64 and\n'
    b'                batch.get("dual_sha256") == sha_obj(public_sparse(dual)) and\n'
    b'                type(batch.get("epoch")) is int and batch["epoch"] >= 1 and\n'
    b'                type(batch.get("global_active_index_count")) is int and\n'
    b'                type(batch.get("selected_count")) is int and\n'
    b'                1 <= batch["selected_count"] <= 64 and\n'
    b'                batch["global_active_index_count"] >= batch["selected_count"] and\n'
    b'                type(batch.get("selected_batch_sha256")) is str and\n'
    b'                len(batch["selected_batch_sha256"]) == 64 and\n'
    b'                all(ch in "0123456789abcdef" for ch in\n'
    b'                    batch["selected_batch_sha256"]) and\n'
    b'                type(batch.get("expanded_pair_count")) is int and\n'
    b'                batch["expanded_pair_count"] > 0 and\n'
    b'                batch.get("parent_pair_visits") ==\n'
    b'                    batch["expanded_pair_count"] and\n'
    b'                type(batch.get("selected_position")) is int and\n'
    b'                0 <= batch["selected_position"] < batch["selected_count"] and\n'
    b'                batch.get("selected_index") ==\n'
    b'                    [block, provenance["translation_hex"], relator] and\n'
    b'                batch.get("selected_scalar") == record["dual_pairing"],\n'
    b'                "selected batch provenance shape")\n'
    b'    elif epoch is not None:\n'
    b'        expected_epoch = independent_boundary_outcome(runtime, dual, workers,\n'
    b'                                                       int(epoch["epoch"]))\n'
    b'        require(epoch == expected_epoch, "selected boundary epoch replay")\n'
    b'    return row',
    "batch provenance replay")

_ACCOUNTING = b'''def validate_batch_accounting(accounting):
    require(accounting.get("batch_cap") == 64 and
            type(accounting.get("selected_batch_sha256")) is str and
            len(accounting["selected_batch_sha256"]) == 64 and
            all(ch in "0123456789abcdef" for ch in
                accounting["selected_batch_sha256"]) and
            all(type(accounting.get(key)) is int and accounting[key] >= 0
                for key in ("global_active_index_count", "materialized_count",
                    "retained_independent_count", "dependent_count",
                    "dual_rebuild_count", "parent_pair_visits",
                    "last_parent_pair_visits")) and
            accounting["last_parent_pair_visits"] <=
                accounting["parent_pair_visits"] and
            accounting["materialized_count"] >=
                accounting["retained_independent_count"] +
                accounting["dependent_count"],
            "batch accounting")


'''
_patched = _swap(_patched, b'def validate_boundary_owner(runtime: dict[str, Any], value: Any) -> int:',
                 _ACCOUNTING + b'def validate_boundary_owner(runtime: dict[str, Any], value: Any) -> int:',
                 "batch accounting validator")
_patched = _swap(
    _patched,
    b'            "boundary accounting")\n'
    b'    require(accounting["formal_ancestry_entries"] >= 137926,',
    b'            "boundary accounting")\n'
    b'    validate_batch_accounting(accounting)\n'
    b'    require(accounting["formal_ancestry_entries"] >= 137926,',
    "COMMON batch accounting")
_patched = _swap(
    _patched,
    b'            "resource worker cleanup")\n'
    b'    require(accounting["formal_ancestry_entries"] == formal["entry_count"],',
    b'            "resource worker cleanup")\n'
    b'    validate_batch_accounting(accounting)\n'
    b'    require(accounting["formal_ancestry_entries"] == formal["entry_count"],',
    "resource batch accounting")

if (_patched.count(b'PRODUCER_PIN = ("' + _PRODUCER.encode("ascii")) != 1 or
        _patched.count(b'def validate_batch_accounting') != 1 or
        _patched.count(b'global-batch-selection/v28') != 1 or
        b'_BATCH_REPLAY_CACHE' in _patched or b'batch_cap=64' in _patched):
    raise SystemExit("batch64 checker v28 generated owner gate")
exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
