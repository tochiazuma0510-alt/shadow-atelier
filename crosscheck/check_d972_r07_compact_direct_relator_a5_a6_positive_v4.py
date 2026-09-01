#!/usr/bin/env python3
"""ABI-only independent checker successor of compact positive owner v3."""
from __future__ import annotations
import hashlib
from pathlib import Path

BASE = Path(__file__).with_name("check_d972_r07_compact_direct_relator_a5_a6_positive_v3.py")
BASE_BYTES = 2629
BASE_SHA256 = "8b32643fe4169b7b42fc6d144438e26ceaa38ed2d2825e9c61f82a79d4f14a8b"
GENERATED_V3_BYTES = 47875
GENERATED_V3_SHA256 = "9af8671d3cb2eb78f69a3d26cdd50e2b673943c4e9364468f8ade231f13b712c"
PRODUCER_V4_BYTES = 1876
PRODUCER_V4_SHA256 = "0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9"


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _body() -> bytes:
    raw = BASE.read_bytes()
    if len(raw) != BASE_BYTES or _sha(raw) != BASE_SHA256:
        raise SystemExit("compact v3 checker pin drift")
    ns = {"__name__": "compact_v3_checker_source", "__file__": str(BASE)}
    exec(compile(raw, str(BASE), "exec"), ns, ns)
    value = ns.get("_BODY")
    if not isinstance(value, bytes) or len(value) != GENERATED_V3_BYTES or _sha(value) != GENERATED_V3_SHA256:
        raise SystemExit("compact v3 checker generated drift")
    replacements = [
        (b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v3", b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v4"),
        (b"CHECK_SCHEMA = SCHEMA + \"/checker-verdict/v3\"\n", b"CHECK_SCHEMA = SCHEMA + \"/checker-verdict/v4\"\n"),
        (b"TASK193_CHECK_SCHEMA = TASK193_SCHEMA + \"/checker-verdict/v3\"\n", b"TASK193_CHECK_SCHEMA = TASK193_SCHEMA + \"/checker-verdict/v5\"\n"),
        (b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3", b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4"),
        (b"PRODUCER_V3_BYTES", b"PRODUCER_V4_BYTES"),
        (b"PRODUCER_V3_SHA256", b"PRODUCER_V4_SHA256"),
        (b"search/d972_r07_compact_direct_relator_a5_a6_positive_v2.py", b"search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py"),
    ]
    for old, new in replacements:
        expected = 1
        if value.count(old) != expected or value.count(new) != 0:
            raise SystemExit("compact v4 checker replacement cardinality")
        value = value.replace(old, new)
    return value


_BODY = _body()
GENERATED_V4_BYTES = 47875
GENERATED_V4_SHA256 = "c65f4e7a122f835f5c50b03d6c189ff26a319518ac8b525d6f3d0943b8412ed0"
if len(_BODY) != GENERATED_V4_BYTES or _sha(_BODY) != GENERATED_V4_SHA256:
    raise SystemExit("compact v4 checker generated drift")
exec(compile(_BODY, str(Path(__file__).resolve()), "exec"), globals(), globals())
