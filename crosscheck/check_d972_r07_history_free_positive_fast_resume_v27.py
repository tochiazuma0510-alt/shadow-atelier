#!/usr/bin/env python3
"""A0 v27 checker: frozen v26 checker with the two-phase v26 producer pin."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V26 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v26.py")
_V26_BYTES = 1961
_V26_SHA256 = "68fc28166e848d22d8e3b2731636c186733ce545a5e3fc313c14a5d4ce0d2d95"
_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_v26.py"
_PRODUCER_BYTES = 5950
_PRODUCER_SHA256 = "4ae9de2eaf0ae337d48309f107fe7aef94afe3783ee2bde63b7c839364e1098e"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v27 checker " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v27 checker " + label + " result cardinality")
    return result


_raw = _V26.read_bytes()
if len(_raw) != _V26_BYTES or hashlib.sha256(_raw).hexdigest() != _V26_SHA256:
    raise SystemExit("v27 checker frozen v26 owner drift")
_scope = {"__file__": str(_V26), "__name__": "_r07_v26_checker_for_v27"}
exec(compile(_raw, str(_V26), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v27 checker v26 generated owner missing")
_old = (b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v25.py",\n'
        b'                3870,\n'
        b'                "8aad1fb0eb0f00e63ffe59d33f71bb89f65a63731084b668f10be587ba343460")')
_new = (f'PRODUCER_PIN = ("{_PRODUCER}",\n'
        f'                {_PRODUCER_BYTES},\n'
        f'                "{_PRODUCER_SHA256}")').encode("ascii")
_patched = _swap(_patched, _old, _new, "producer exact pin")
exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
