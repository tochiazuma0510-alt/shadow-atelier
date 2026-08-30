#!/usr/bin/env python3
"""Checker v29 pinning the raw-row replay repaired batch-64 producer."""
from __future__ import annotations

import hashlib
from pathlib import Path

_V28 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_batch64_v28.py")
_V28_BYTES = 8219
_V28_SHA256 = "0491b3b7ff68a839811869079c7da33cae751f58936c6eef7a4e5ab8724baa99"
_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_batch64_v29.py"
_PRODUCER_BYTES = 4999
_PRODUCER_SHA256 = "e3cf997b8aae78599e693652cf576083ae518b7a3690099c83b12d6e83039434"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("batch64 checker v29 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("batch64 checker v29 " + label + " result cardinality")
    return result


_raw = _V28.read_bytes()
if len(_raw) != _V28_BYTES or hashlib.sha256(_raw).hexdigest() != _V28_SHA256:
    raise SystemExit("batch64 checker v29 frozen v28 owner drift")
_scope = {"__file__": str(_V28), "__name__": "_r07_batch64_checker_v28_for_v29"}
exec(compile(_raw, str(_V28), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("batch64 checker v29 generated v28 owner missing")

_OLD_PIN = (b'PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_batch64_v28.py",\n'
            b'                19149,\n'
            b'                "ff26d11c23b45b70a1fc93d481bfd4f3dd66e6c106fd0afae140af81ec01ddf9")')
_NEW_PIN = (f'PRODUCER_PIN = ("{_PRODUCER}",\n'
            f'                {_PRODUCER_BYTES},\n'
            f'                "{_PRODUCER_SHA256}")').encode("ascii")
_patched = _swap(_patched, _OLD_PIN, _NEW_PIN, "producer pin")

if (_patched.count(b'PRODUCER_PIN = ("' + _PRODUCER.encode("ascii")) != 1 or
        _OLD_PIN in _patched or b'_BATCH_REPLAY_CACHE' in _patched or
        _patched.count(b'def validate_boundary_provenance') != 1):
    raise SystemExit("batch64 checker v29 generated owner gate")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
