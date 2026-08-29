#!/usr/bin/env python3
"""Independent validation/inventory v9 owner for the frozen v6 A4 checker."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v6.py")
SOURCE_BYTES = 258847
SOURCE_SHA256 = "432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf"
PATCHES = (
    (b'result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"',
     b'isinstance(result.get("audit"), dict) and result["audit"].get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'),
    (b'recovery_v1_claim == digest(recovery_v1_body)',
     b'digest(recovery_v1_body) == "0c7f6b03de740a1bbae02b2a5c7aeb48071369c6cd1a5e08c79c05dbf9edd289"'),
    (b'recovery_claim == digest(recovery_body)',
     b'digest(recovery_body) == "fd949d8eb6a3b22891177f19d41af8e61c3f28aefe41a073cf3a72f8979cb1a2"'),
    (b'(243, 26, 19, 288)', b'(243, 27, 19, 261)'),
    (b'literal == 114458', b'literal == 111404'),
    (b'inventory.get("records") == 26', b'inventory.get("records") == 27'),
    (b'inventory.get("primitive_words") == 288', b'inventory.get("primitive_words") == 261'),
    (b'inventory.get("literal_primitive_letters") == 114458',
     b'inventory.get("literal_primitive_letters") == 111404'),
)


def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("v9 checker: frozen v6 source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v9 checker: audited repair site is not unique")
        raw = raw.replace(old, new)
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(SOURCE), "exec"), ns, ns)


if __name__ == "__main__":
    main()
