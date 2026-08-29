#!/usr/bin/env python3
"""Production successor: lift only the stale boundary-pair resource cap."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v13.py")
_BASE_BYTES = 147_409
_BASE_SHA256 = "4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a"
_OLD = b'"boundary_pairs": 8_000_000,'
_NEW = b'"boundary_pairs": 80_000_000,'

_raw = _BASE.read_bytes()
if len(_raw) != _BASE_BYTES or hashlib.sha256(_raw).hexdigest() != _BASE_SHA256:
    raise SystemExit("v14 frozen v13 owner drift")
if _raw.count(_OLD) != 1 or _raw.count(_NEW) != 0:
    raise SystemExit("v14 boundary-pair substitution cardinality")
_patched = _raw.replace(_OLD, _NEW)
if _patched.count(_OLD) != 0 or _patched.count(_NEW) != 1:
    raise SystemExit("v14 boundary-pair substitution failed")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
