#!/usr/bin/env python3
"""A0 v22 checker: frozen v21 checks with the v22 producer exact pin."""
from __future__ import annotations

import hashlib
from pathlib import Path


_V21 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v21.py")
_V21_BYTES = 2027
_V21_SHA256 = "a2d913328fef890477305ae5b2cec6978c0dc3882e7c47af35d3444ac16f7c22"
_V22_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_v22.py"
_V22_PRODUCER_BYTES = 3280
_V22_PRODUCER_SHA256 = "1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v22 checker " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v22 checker " + label + " result cardinality")
    return result


_v21_raw = _V21.read_bytes()
if len(_v21_raw) != _V21_BYTES or hashlib.sha256(
        _v21_raw).hexdigest() != _V21_SHA256:
    raise SystemExit("v22 checker frozen v21 owner drift")
_v21_scope = {"__file__": str(_V21),
              "__name__": "_r07_v21_checker_for_v22"}
exec(compile(_v21_raw, str(_V21), "exec"), _v21_scope, _v21_scope)
_patched = _v21_scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v22 checker v21 generated owner missing")

_patched = _swap(
    _patched,
    b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v21.py",\n'
    b'                3035,\n'
    b'                "18aef3a1619b076b32002a9083ba9763116d984b761b7f8d181059293dbdf1fd")',
    b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v22.py",\n'
    b'                3280,\n'
    b'                "1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01")',
    "producer exact pin",
)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
