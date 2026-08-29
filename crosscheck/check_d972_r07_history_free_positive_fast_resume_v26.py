#!/usr/bin/env python3
"""A0 v26 checker: frozen v25 checker with the exact v25 producer pin."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V25 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v25.py")
_V25_BYTES = 1979
_V25_SHA256 = "f0056fc956bbf39e270526afb539a9559a564804e0aef60ec59cb0fe2382ee9c"
_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_v25.py"
_PRODUCER_BYTES = 3870
_PRODUCER_SHA256 = "8aad1fb0eb0f00e63ffe59d33f71bb89f65a63731084b668f10be587ba343460"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v26 checker " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v26 checker " + label + " result cardinality")
    return result


_raw = _V25.read_bytes()
if len(_raw) != _V25_BYTES or hashlib.sha256(_raw).hexdigest() != _V25_SHA256:
    raise SystemExit("v26 checker frozen v25 owner drift")
_scope = {"__file__": str(_V25), "__name__": "_r07_v25_checker_for_v26"}
exec(compile(_raw, str(_V25), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v26 checker v25 generated owner missing")
_old = (b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v24.py",\n'
        b'                16956,\n'
        b'                "b151b6c858de556145bc58b13037ea8b193f068a93c3d0383c1769613c3cea74")')
_new = (f'PRODUCER_PIN = ("{_PRODUCER}",\n'
        f'                {_PRODUCER_BYTES},\n'
        f'                "{_PRODUCER_SHA256}")').encode("ascii")
_patched = _swap(_patched, _old, _new, "producer exact pin")
exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
