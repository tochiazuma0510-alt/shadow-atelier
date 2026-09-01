#!/usr/bin/env python3
"""ABI-only successor of the actual compact positive owner v3."""
from __future__ import annotations
import hashlib
from pathlib import Path

BASE = Path(__file__).with_name("d972_r07_compact_direct_relator_a5_a6_positive_v3.py")
BASE_BYTES = 2018
BASE_SHA256 = "7a7272eb553d5256bdad2a123ad6cad87b171fb5d23c2e6d81b7702c5842f244"
GENERATED_V3_BYTES = 61376
GENERATED_V3_SHA256 = "fa930244c2316dda7c547f433f3c5065736f1e276b68a0fda66d8a6753116d98"


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _body() -> bytes:
    raw = BASE.read_bytes()
    if len(raw) != BASE_BYTES or _sha(raw) != BASE_SHA256:
        raise SystemExit("compact v3 producer pin drift")
    ns = {"__name__": "compact_v3_producer_source", "__file__": str(BASE)}
    exec(compile(raw, str(BASE), "exec"), ns, ns)
    value = ns.get("_BODY")
    if not isinstance(value, bytes) or len(value) != GENERATED_V3_BYTES or _sha(value) != GENERATED_V3_SHA256:
        raise SystemExit("compact v3 producer generated drift")
    replacements = [
        (b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v3", b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v4"),
        (b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3", b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4"),
    ]
    for old, new in replacements:
        if value.count(old) != 1 or value.count(new) != 0:
            raise SystemExit("compact v4 producer replacement cardinality")
        value = value.replace(old, new)
    return value


_BODY = _body()
GENERATED_V4_BYTES = 61376
GENERATED_V4_SHA256 = "d9a5a136d875d2fb7f5d596966abf094b7c555a0e4eb4ac6576c72071f734b84"
if len(_BODY) != GENERATED_V4_BYTES or _sha(_BODY) != GENERATED_V4_SHA256:
    raise SystemExit("compact v4 generated drift")
exec(compile(_BODY, str(Path(__file__).resolve()), "exec"), globals(), globals())
