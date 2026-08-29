#!/usr/bin/env python3
"""Independent validation-only v7 owner for the frozen v6 checker."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v6.py")
SOURCE_BYTES = 258847
SOURCE_SHA256 = "432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf"
OLD = b'result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'
NEW = b'isinstance(result.get("audit"), dict) and result["audit"].get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'


def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("v7 checker: frozen v6 source drift")
    if raw.count(OLD) != 1:
        raise SystemExit("v7 checker: audited correction site is not unique")
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
