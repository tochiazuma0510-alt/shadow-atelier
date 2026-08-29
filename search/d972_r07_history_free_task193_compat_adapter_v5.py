#!/usr/bin/env python3
"""Exact-pin A0-v22 successor of the accepted task193 adapter v4."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "d972_r07_history_free_task193_compat_adapter_v4.py")
_BASE_BYTES = 2426
_BASE_SHA256 = "0174b1508f50708352e8607edfb0a210508680e58a295763b2d287fda32889b9"


def _swap(source: bytes, old: bytes, new: bytes, count: int, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != count:
        raise SystemExit("adapter v5 " + label + " source cardinality")
    result = source.replace(old, new)
    if result.count(new) != count:
        raise SystemExit("adapter v5 " + label + " result cardinality")
    return result


_patched = _BASE.read_bytes()
if len(_patched) != _BASE_BYTES or hashlib.sha256(
        _patched).hexdigest() != _BASE_SHA256:
    raise SystemExit("adapter v5 frozen v4 owner drift")

_changes = (
    (b'd972-r07-history-free-task193-compat-adapter/v4',
     b'd972-r07-history-free-task193-compat-adapter/v5', 1, "schema"),
    (b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_A0_REPLAY',
     b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_A0_REPLAY', 1, "accepted"),
    (b"""b'    "search/d972_r07_history_free_positive_fast_resume_v20.py", 10739,\\n'
     b'    "cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7")""",
     b"""b'    "search/d972_r07_history_free_positive_fast_resume_v22.py", 3280,\\n'
     b'    "1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01")""",
     1, "A0 producer exact pin"),
    (b"""b'    "crosscheck/check_d972_r07_history_free_positive_fast_resume_v20.py", 5327,\\n'
     b'    "7c0a1c8b862f8dd62224e0f4ebc0d50ae7ea2de86c63ffb67e025cba98d7c077")""",
     b"""b'    "crosscheck/check_d972_r07_history_free_positive_fast_resume_v22.py", 2066,\\n'
     b'    "4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13")""",
     1, "A0 checker exact pin"),
    (b'd972_r07_a0_v20_checker_for_adapter_v4',
     b'd972_r07_a0_v22_checker_for_adapter_v5', 1, "checker module label"),
    (b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V4_TERMINAL',
     b'R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V5_TERMINAL', 1, "terminal prefix"),
)
for _old, _new, _count, _label in _changes:
    _patched = _swap(_patched, _old, _new, _count, _label)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
