#!/usr/bin/env python3
"""A0 v23 checker: frozen v22 checks with the v23 producer exact pin."""
from __future__ import annotations

import hashlib
from pathlib import Path


_V22 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v22.py")
_V22_BYTES = 2066
_V22_SHA256 = "4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13"
_V23_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_v23.py"
_V23_PRODUCER_BYTES = 3729
_V23_PRODUCER_SHA256 = "0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v23 checker " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v23 checker " + label + " result cardinality")
    return result


_v22_raw = _V22.read_bytes()
if len(_v22_raw) != _V22_BYTES or hashlib.sha256(
        _v22_raw).hexdigest() != _V22_SHA256:
    raise SystemExit("v23 checker frozen v22 owner drift")
_v22_scope = {"__file__": str(_V22),
              "__name__": "_r07_v22_checker_for_v23"}
exec(compile(_v22_raw, str(_V22), "exec"), _v22_scope, _v22_scope)
_patched = _v22_scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v23 checker v22 generated owner missing")

_patched = _swap(
    _patched,
    b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v22.py",\n'
    b'                3280,\n'
    b'                "1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01")',
    b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v23.py",\n'
    b'                3729,\n'
    b'                "0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3")',
    "producer exact pin",
)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
