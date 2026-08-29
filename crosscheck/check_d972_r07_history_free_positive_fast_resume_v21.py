#!/usr/bin/env python3
"""A0 v21 checker: frozen v20 checks with the v21 producer exact pin."""
from __future__ import annotations

import hashlib
from pathlib import Path


_V20 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v20.py")
_V20_BYTES = 5327
_V20_SHA256 = "7c0a1c8b862f8dd62224e0f4ebc0d50ae7ea2de86c63ffb67e025cba98d7c077"
_V21_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_v21.py"
_V21_PRODUCER_BYTES = 3035
_V21_PRODUCER_SHA256 = "18aef3a1619b076b32002a9083ba9763116d984b761b7f8d181059293dbdf1fd"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1:
        raise SystemExit("v21 checker " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v21 checker " + label + " result cardinality")
    return result


_v20_raw = _V20.read_bytes()
if len(_v20_raw) != _V20_BYTES or hashlib.sha256(
        _v20_raw).hexdigest() != _V20_SHA256:
    raise SystemExit("v21 checker frozen v20 owner drift")
_v20_scope = {"__file__": str(_V20), "__name__": "_r07_v20_checker_for_v21"}
exec(compile(_v20_raw, str(_V20), "exec"), _v20_scope, _v20_scope)
_patched = _v20_scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v21 checker v20 generated owner missing")

_patched = _swap(
    _patched,
    b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v20.py",\n'
    b'                10739,\n'
    b'                "cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7")',
    b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v21.py",\n'
    b'                3035,\n'
    b'                "18aef3a1619b076b32002a9083ba9763116d984b761b7f8d181059293dbdf1fd")',
    "producer exact pin",
)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
