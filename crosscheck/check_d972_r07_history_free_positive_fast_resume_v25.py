#!/usr/bin/env python3
"""A0 v25 checker: frozen v24 checker with the bounded v24 producer pin."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V24 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v24.py")
_V24_BYTES = 1627
_V24_SHA256 = "7b35c39a3ab7204bfd3251740211c23addf130dc1f9bf9a5cbaf3d1162155ac0"
_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_v24.py"
_PRODUCER_BYTES = 16956
_PRODUCER_SHA256 = "b151b6c858de556145bc58b13037ea8b193f068a93c3d0383c1769613c3cea74"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v25 checker " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v25 checker " + label + " result cardinality")
    return result


_v24_raw = _V24.read_bytes()
if len(_v24_raw) != _V24_BYTES or hashlib.sha256(_v24_raw).hexdigest() != _V24_SHA256:
    raise SystemExit("v25 checker frozen v24 owner drift")
_scope = {"__file__": str(_V24), "__name__": "_r07_v24_checker_for_v25"}
exec(compile(_v24_raw, str(_V24), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v25 checker v24 generated owner missing")
_old = (b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v23.py",\n'
        b'                3729,\n'
        b'                "0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3")')
_new = (f'PRODUCER_PIN = ("{_PRODUCER}",\n'
        f'                {_PRODUCER_BYTES},\n'
        f'                "{_PRODUCER_SHA256}")').encode("ascii")
_patched = _swap(_patched, _old, _new, "producer exact pin")
exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
