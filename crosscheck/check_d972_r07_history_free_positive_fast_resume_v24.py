#!/usr/bin/env python3
"""A0 v24 checker: frozen v23 checks with the corrected predicate."""
from __future__ import annotations

import hashlib
from pathlib import Path


_V23 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v23.py")
_V23_BYTES = 2066
_V23_SHA256 = "b0e6f447c92cf76f7735c56ce7dc71b2fa7c3a2247abab3962d50ba9e9bb926c"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v24 checker " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v24 checker " + label + " result cardinality")
    return result


_v23_raw = _V23.read_bytes()
if len(_v23_raw) != _V23_BYTES or hashlib.sha256(
        _v23_raw).hexdigest() != _V23_SHA256:
    raise SystemExit("v24 checker frozen v23 owner drift")
_v23_scope = {"__file__": str(_V23),
              "__name__": "_r07_v23_checker_for_v24"}
exec(compile(_v23_raw, str(_V23), "exec"), _v23_scope, _v23_scope)
_patched = _v23_scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v24 checker v23 generated owner missing")

_patched = _swap(
    _patched,
    b'not heavy_complete and checkpoint.get("heavy_reconstructible") is bool',
    b'not heavy_complete and type(checkpoint.get("heavy_reconstructible")) is bool',
    "heavy_reconstructible type",
)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
