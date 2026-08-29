#!/usr/bin/env python3
"""Checkpoint-accounting v10 owner for the frozen v6 A4 producer."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v6.py")
SOURCE_BYTES = 219187
SOURCE_SHA256 = "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a"
PATCHES = (
    (b'result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"',
     b'isinstance(result.get("audit"), dict) and result["audit"].get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'),
    (b'recovery_v1_claim == digest(recovery_v1_body)',
     b'digest(recovery_v1_body) == "0c7f6b03de740a1bbae02b2a5c7aeb48071369c6cd1a5e08c79c05dbf9edd289"'),
    (b'recovery_claim == digest(recovery_body)',
     b'digest(recovery_body) == "fd949d8eb6a3b22891177f19d41af8e61c3f28aefe41a073cf3a72f8979cb1a2"'),
    (b'(243, 26, 19, 288)', b'(243, 27, 19, 261)'),
    (b'literal == 114458', b'literal == 111404'),
    (b'require(desired >= charged, "serialize:fixed_point_shrunk")',
     b'if desired < charged: write_atomic(path, encoded); return'),
    (b'require(desired >= charged, "checkpoint:fixed_point_shrunk")',
     b'if desired < charged: write_atomic(path, encoded); return'),
)


def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("v10 producer: frozen v6 source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v10 producer: audited repair site is not unique")
        raw = raw.replace(old, new)
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(SOURCE), "exec"), ns, ns)


if __name__ == "__main__":
    main()
