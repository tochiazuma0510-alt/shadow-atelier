#!/usr/bin/env python3
"""Checker successor pinned to the resumable v15 production wrapper."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v13.py")
_BASE_BYTES = 131_946
_BASE_SHA256 = "42e8f6df8d85169bf4039bc4195a0e47c284ad475a177414308ba28f99377b64"
_REPLACEMENTS = (
    (b"search/d972_r07_history_free_positive_fast_resume_v13.py",
     b"search/d972_r07_history_free_positive_fast_resume_v15.py"),
    (b"147409", b"2253"),
    (b"4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a",
     b"6412ea39f1b0559738c44fff0a9aa5f6c8366c55193b74f5c6df1ded977dc2a9"),
)

_patched = _BASE.read_bytes()
if (len(_patched) != _BASE_BYTES or
        hashlib.sha256(_patched).hexdigest() != _BASE_SHA256):
    raise SystemExit("v15 checker frozen v13 owner drift")
for _old, _new in _REPLACEMENTS:
    if _patched.count(_old) != 1:
        raise SystemExit("v15 checker producer-pin substitution cardinality")
    _patched = _patched.replace(_old, _new)
for _old, _new in _REPLACEMENTS:
    if _patched.count(_old) != 0:
        raise SystemExit("v15 checker producer-pin substitution failed")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
