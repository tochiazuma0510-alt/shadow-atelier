#!/usr/bin/env python3
"""Exact-pin A0-v20 successor of the accepted task193 adapter v3."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "d972_r07_history_free_task193_compat_adapter_v3.py")
_BASE_BYTES = 14038
_BASE_SHA256 = "7be27b31f0c6e4acf0948341dfaae9d9d880b204774d04660a77982c0546245c"


def _swap(source: bytes, old: bytes, new: bytes, count: int, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != count:
        raise SystemExit("adapter v4 " + label + " source cardinality")
    result = source.replace(old, new)
    if result.count(new) != count:
        raise SystemExit("adapter v4 " + label + " result cardinality")
    return result


_patched = _BASE.read_bytes()
if len(_patched) != _BASE_BYTES or hashlib.sha256(
        _patched).hexdigest() != _BASE_SHA256:
    raise SystemExit("adapter v4 frozen v3 owner drift")

_changes = (
    (b'd972-r07-history-free-task193-compat-adapter/v3',
     b'd972-r07-history-free-task193-compat-adapter/v4', 1, "schema"),
    (b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_A0_REPLAY',
     b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_A0_REPLAY', 1, "accepted"),
    (b'    "search/d972_r07_history_free_positive_fast_resume_v18.py", 2557,\n'
     b'    "55505c6b59ebc9cc61c12c0229668509a2fcf7530ca14dbd791a8b18a95c5433")',
     b'    "search/d972_r07_history_free_positive_fast_resume_v20.py", 10739,\n'
     b'    "cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7")',
     1, "A0 producer exact pin"),
    (b'    "crosscheck/check_d972_r07_history_free_positive_fast_resume_v18.py", 1317,\n'
     b'    "83ebfe5088388f5c84bbab9e52ef28cb8888fb944fbe417cf98041bab34bfaa9")',
     b'    "crosscheck/check_d972_r07_history_free_positive_fast_resume_v20.py", 5327,\n'
     b'    "7c0a1c8b862f8dd62224e0f4ebc0d50ae7ea2de86c63ffb67e025cba98d7c077")',
     1, "A0 checker exact pin"),
    (b'd972_r07_a0_v18_checker_for_adapter_v3',
     b'd972_r07_a0_v20_checker_for_adapter_v4', 1, "checker module label"),
    (b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_TERMINAL',
     b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_TERMINAL', 3, "terminal prefix"),
)
for _old, _new, _count, _label in _changes:
    _patched = _swap(_patched, _old, _new, _count, _label)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
