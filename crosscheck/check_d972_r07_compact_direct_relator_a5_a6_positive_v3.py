#!/usr/bin/env python3
"""Minimal independent checker contract successor of compact owner v2."""
from __future__ import annotations
import hashlib
from pathlib import Path

BASE = Path(__file__).with_name("check_d972_r07_compact_direct_relator_a5_a6_positive_v2.py")
BASE_BYTES = 7720
BASE_SHA256 = "535c7b8aa0983748204d0e381d367d3398380ea3097cd48ef374dfc3daf38c67"
GENERATED_V2_BYTES = 47815
GENERATED_V2_SHA256 = "ee826f1873e045574838e4fd478530edf2ef5986683c7f0ad72cf4958baac262"
PRODUCER_V3_BYTES = 2018
PRODUCER_V3_SHA256 = "7a7272eb553d5256bdad2a123ad6cad87b171fb5d23c2e6d81b7702c5842f244"


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _body() -> bytes:
    raw = BASE.read_bytes()
    if len(raw) != BASE_BYTES or _sha(raw) != BASE_SHA256:
        raise SystemExit("compact v2 checker pin drift")
    ns = {"__name__": "compact_v2_checker_source", "__file__": str(BASE)}
    exec(compile(raw, str(BASE), "exec"), ns, ns)
    value = ns.get("_BODY")
    if not isinstance(value, bytes) or len(value) != GENERATED_V2_BYTES or _sha(value) != GENERATED_V2_SHA256:
        raise SystemExit("compact v2 checker generated drift")
    replacements = [
        (b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v2", b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v3"),
        (b"/checker-verdict/v2", b"/checker-verdict/v3"),
        (b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2", b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3"),
        (b"PRODUCER_V2_BYTES", b"PRODUCER_V3_BYTES"),
        (b"PRODUCER_V2_SHA256", b"PRODUCER_V3_SHA256"),
        (b'    require(receipt.get("compact_relator_roster") == {"owner": "Task411", "count": COMPACT_COUNT, "sha256": COMPACT_SHA256}, "compact:owner")\n',
         b'    require(receipt.get("resumable") is False, "resumable")\n    require(receipt.get("compact_relator_roster") == {"owner": "Task411", "count": COMPACT_COUNT, "sha256": COMPACT_SHA256}, "compact:owner")\n'),
    ]
    for old, new in replacements:
        expected = 2 if old == b"/checker-verdict/v2" else 1
        if value.count(old) != expected or (new and value.count(new) != 0):
            raise SystemExit("compact v3 checker replacement cardinality")
        value = value.replace(old, new)
    return value


_BODY = _body()
GENERATED_V3_BYTES = 47875
GENERATED_V3_SHA256 = "9af8671d3cb2eb78f69a3d26cdd50e2b673943c4e9364468f8ade231f13b712c"
if len(_BODY) != GENERATED_V3_BYTES or _sha(_BODY) != GENERATED_V3_SHA256:
    raise SystemExit("compact v3 checker generated drift")
exec(compile(_BODY, str(Path(__file__).resolve()), "exec"), globals(), globals())
