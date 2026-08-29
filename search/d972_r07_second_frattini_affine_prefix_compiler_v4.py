#!/usr/bin/env python3
"""Exact adapter-v5 pin successor of the accepted task193 compiler v3."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "d972_r07_second_frattini_affine_prefix_compiler_v3.py")
_BASE_BYTES = 2826
_BASE_SHA256 = "1ac65ca533e11ac39def79c84de0bbdcb018d463ac10bca6158db254a61da741"


def _swap(source: bytes, old: bytes, new: bytes, count: int, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != count:
        raise SystemExit("task193 v4 " + label + " source cardinality")
    result = source.replace(old, new)
    if result.count(new) != count:
        raise SystemExit("task193 v4 " + label + " result cardinality")
    return result


_patched = _BASE.read_bytes()
if len(_patched) != _BASE_BYTES or hashlib.sha256(
        _patched).hexdigest() != _BASE_SHA256:
    raise SystemExit("task193 v4 frozen v3 owner drift")

_changes = (
    (b'd972-r07-second-frattini-affine-prefix-compiler/v3',
     b'd972-r07-second-frattini-affine-prefix-compiler/v4', 1, "schema"),
    (b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V3',
     b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V4', 1, "terminal family"),
    (b'd972-r07-history-free-task193-compat-adapter/v4',
     b'd972-r07-history-free-task193-compat-adapter/v5', 1, "adapter schema"),
    (b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_A0_REPLAY',
     b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_A0_REPLAY', 1,
     "adapter accepted terminal"),
    (b'ADAPTER_CHECK_SCHEMA = ADAPTER_SCHEMA + "/checker-verdict/v4"',
     b'ADAPTER_CHECK_SCHEMA = ADAPTER_SCHEMA + "/checker-verdict/v5"', 1,
     "adapter checker schema"),
    (b"""b'    "search/d972_r07_history_free_task193_compat_adapter_v4.py", 2426,\\n'
     b'    "0174b1508f50708352e8607edfb0a210508680e58a295763b2d287fda32889b9")""",
     b"""b'    "search/d972_r07_history_free_task193_compat_adapter_v5.py", 2453,\\n'
     b'    "024fe7c5d5ac23f248b30275f4f97d4bf512980a4dc17e249b981fd18649355f")""",
     1, "adapter producer exact pin"),
    (b"""b'    "crosscheck/check_d972_r07_history_free_task193_compat_adapter_v4.py", 3105,\\n'
     b'    "4269368c006e19fa0cc71da78d12927f8fbd4c85087f0e5b5ca11688a8f58d06")""",
     b"""b'    "crosscheck/check_d972_r07_history_free_task193_compat_adapter_v5.py", 3145,\\n'
     b'    "4c7d89fdc3f4a5399f3abef0d5380a26958bcb48d5caab95ec27fc0c23a89556")""",
     1, "adapter checker exact pin"),
    (b'd972-r07-second-frattini-affine-prefix-compiler-checkpoint/v3',
     b'd972-r07-second-frattini-affine-prefix-compiler-checkpoint/v4', 1,
     "checkpoint schema"),
)
for _old, _new, _count, _label in _changes:
    _patched = _swap(_patched, _old, _new, _count, _label)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
