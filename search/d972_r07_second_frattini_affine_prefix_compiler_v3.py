#!/usr/bin/env python3
"""Exact adapter-v4 pin successor of the accepted task193 compiler v2."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "d972_r07_second_frattini_affine_prefix_compiler_v2.py")
_BASE_BYTES = 22937
_BASE_SHA256 = "65a45189e120ae58f99310a9189fd4f88802e269d3c1a61bf5e68e879eebde88"


def _swap(source: bytes, old: bytes, new: bytes, count: int, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != count:
        raise SystemExit("task193 v3 " + label + " source cardinality")
    result = source.replace(old, new)
    if result.count(new) != count:
        raise SystemExit("task193 v3 " + label + " result cardinality")
    return result


_patched = _BASE.read_bytes()
if len(_patched) != _BASE_BYTES or hashlib.sha256(
        _patched).hexdigest() != _BASE_SHA256:
    raise SystemExit("task193 v3 frozen v2 owner drift")

_changes = (
    (b'd972-r07-second-frattini-affine-prefix-compiler/v2',
     b'd972-r07-second-frattini-affine-prefix-compiler/v3', 1, "schema"),
    (b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2',
     b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V3', 3, "terminal family"),
    (b'd972-r07-history-free-task193-compat-adapter/v3',
     b'd972-r07-history-free-task193-compat-adapter/v4', 1, "adapter schema"),
    (b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_A0_REPLAY',
     b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_A0_REPLAY', 1,
     "adapter accepted terminal"),
    (b'ADAPTER_CHECK_SCHEMA = ADAPTER_SCHEMA + "/checker-verdict/v3"',
     b'ADAPTER_CHECK_SCHEMA = ADAPTER_SCHEMA + "/checker-verdict/v4"', 1,
     "adapter checker schema"),
    (b'    "search/d972_r07_history_free_task193_compat_adapter_v3.py", 14038,\n'
     b'    "7be27b31f0c6e4acf0948341dfaae9d9d880b204774d04660a77982c0546245c")',
     b'    "search/d972_r07_history_free_task193_compat_adapter_v4.py", 2426,\n'
     b'    "0174b1508f50708352e8607edfb0a210508680e58a295763b2d287fda32889b9")',
     1, "adapter producer exact pin"),
    (b'    "crosscheck/check_d972_r07_history_free_task193_compat_adapter_v3.py", 16804,\n'
     b'    "f123daeec769aff9254bf913514f0792f20a2f32725aa19bd0020dc84e4c0c6f")',
     b'    "crosscheck/check_d972_r07_history_free_task193_compat_adapter_v4.py", 3105,\n'
     b'    "4269368c006e19fa0cc71da78d12927f8fbd4c85087f0e5b5ca11688a8f58d06")',
     1, "adapter checker exact pin"),
    (b'd972-r07-second-frattini-affine-prefix-compiler-checkpoint/v2',
     b'd972-r07-second-frattini-affine-prefix-compiler-checkpoint/v3', 1,
     "checkpoint schema"),
)
for _old, _new, _count, _label in _changes:
    _patched = _swap(_patched, _old, _new, _count, _label)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
