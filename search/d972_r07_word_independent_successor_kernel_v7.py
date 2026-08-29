#!/usr/bin/env python3
"""Validation-only v7 owner for the frozen v6 producer.

The mathematical implementation remains byte-for-byte frozen in v6.  This
owner authenticates it, applies the single audited JSON-pointer correction in
memory, and then executes it with this v7 file as the checkpoint identity.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v6.py")
SOURCE_BYTES = 219187
SOURCE_SHA256 = "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a"
OLD = b'result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'
NEW = b'isinstance(result.get("audit"), dict) and result["audit"].get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'


def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("v7 producer: frozen v6 source drift")
    if raw.count(OLD) != 1:
        raise SystemExit("v7 producer: audited correction site is not unique")
    patched = raw.replace(OLD, NEW)
    namespace = {
        "__name__": "__main__",
        "__file__": str(Path(__file__).resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(patched, str(SOURCE), "exec"), namespace, namespace)


if __name__ == "__main__":
    main()
