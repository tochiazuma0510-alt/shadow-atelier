#!/usr/bin/env python3
"""Production successor: lift the cap and bind resumable UNKNOWN receipts."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v13.py")
_BASE_BYTES = 147_409
_BASE_SHA256 = "4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a"
_REPLACEMENTS = (
    (b'"boundary_pairs": 8_000_000,',
     b'"boundary_pairs": 80_000_000,'),
    (b"                    selftest: dict[str, Any] | None) -> dict[str, Any]:",
     b"                    selftest: dict[str, Any] | None,\n"
     b"                    light_input_sha256: str | None = None) -> dict[str, Any]:"),
    (b'        "source": source, "source_snapshots": None if registry is None else registry.public(),\n'
     b'        "monitor": None if meter is None else meter.public(),',
     b'        "source": source, "source_snapshots": None if registry is None else registry.public(),\n'
     b'        "light_input_sha256": light_input_sha256,\n'
     b'        "monitor": None if meter is None else meter.public(),'),
    (b"            meter, None, None if search is None else search.boundary.public(), selftest)",
     b"            meter, None, None if search is None else search.boundary.public(), selftest,\n"
     b"            None if runtime is None else runtime.get(\"light_input_sha256\"))"),
    (b"                                  meter, reference, boundary_public, selftest)",
     b"                                  meter, reference, boundary_public, selftest,\n"
     b"                                  None if runtime is None else runtime.get(\"light_input_sha256\"))"),
)

_patched = _BASE.read_bytes()
if (len(_patched) != _BASE_BYTES or
        hashlib.sha256(_patched).hexdigest() != _BASE_SHA256):
    raise SystemExit("v15 frozen v13 owner drift")
for _old, _new in _REPLACEMENTS:
    if _patched.count(_old) != 1:
        raise SystemExit("v15 substitution cardinality")
    _patched = _patched.replace(_old, _new)
for _old, _new in _REPLACEMENTS:
    if _patched.count(_old) != 0:
        raise SystemExit("v15 substitution failed")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
