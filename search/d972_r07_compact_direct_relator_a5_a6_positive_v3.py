#!/usr/bin/env python3
"""Minimal contract successor of the actual compact positive owner v2."""
from __future__ import annotations
import hashlib
from pathlib import Path

BASE = Path(__file__).with_name("d972_r07_compact_direct_relator_a5_a6_positive_v2.py")
BASE_BYTES = 7707
BASE_SHA256 = "47cc53c0b59cbca0981983373d30604cbffd874cfa01d2d2adef599e505a21d3"
GENERATED_V2_BYTES = 61341
GENERATED_V2_SHA256 = "289dbff63af59daec0478bdc6eee376b711c4b944fee08d671b3e10a323b5539"


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _body() -> bytes:
    raw = BASE.read_bytes()
    if len(raw) != BASE_BYTES or _sha(raw) != BASE_SHA256:
        raise SystemExit("compact v2 producer pin drift")
    ns = {"__name__": "compact_v2_producer_source", "__file__": str(BASE)}
    exec(compile(raw, str(BASE), "exec"), ns, ns)
    value = ns.get("_BODY")
    if not isinstance(value, bytes) or len(value) != GENERATED_V2_BYTES or _sha(value) != GENERATED_V2_SHA256:
        raise SystemExit("compact v2 producer generated drift")
    replacements = [
        (b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v2", b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v3"),
        (b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2", b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3"),
        (b"    return _compact_seal(value)\n", b"        value[\"resumable\"] = False\n    return _compact_seal(value)\n"),
    ]
    for old, new in replacements:
        if value.count(old) != 1 or (new and value.count(new) != 0):
            raise SystemExit("compact v3 producer replacement cardinality")
        value = value.replace(old, new)
    return value


_BODY = _body()
GENERATED_V3_BYTES = 61376
GENERATED_V3_SHA256 = "fa930244c2316dda7c547f433f3c5065736f1e276b68a0fda66d8a6753116d98"
if len(_BODY) != GENERATED_V3_BYTES or _sha(_BODY) != GENERATED_V3_SHA256:
    raise SystemExit("compact v3 generated drift")
exec(compile(_BODY, str(Path(__file__).resolve()), "exec"), globals(), globals())
