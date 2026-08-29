#!/usr/bin/env python3
"""Checker successor pinned to the replayable v18 production wrapper."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v13.py")
_BASE_BYTES = 131_946
_BASE_SHA256 = "42e8f6df8d85169bf4039bc4195a0e47c284ad475a177414308ba28f99377b64"
_REPLACEMENTS = (
    (b"search/d972_r07_history_free_positive_fast_resume_v13.py",
     b"search/d972_r07_history_free_positive_fast_resume_v18.py"),
    (b"147409", b"2557"),
    (b"4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a",
     b"55505c6b59ebc9cc61c12c0229668509a2fcf7530ca14dbd791a8b18a95c5433"),
)

_patched = _BASE.read_bytes()
if (len(_patched) != _BASE_BYTES or
        hashlib.sha256(_patched).hexdigest() != _BASE_SHA256):
    raise SystemExit("v18 checker frozen v13 owner drift")
for _old, _new in _REPLACEMENTS:
    if _patched.count(_old) != 1:
        raise SystemExit("v18 checker producer-pin substitution cardinality")
    _patched = _patched.replace(_old, _new)
for _old, _new in _REPLACEMENTS:
    if _patched.count(_old) != 0:
        raise SystemExit("v18 checker producer-pin substitution failed")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
