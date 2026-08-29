#!/usr/bin/env python3
"""Independent v12 owner: v11 arithmetic plus the actual producer code pin."""

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
    (b'require(desired >= charged, "checker:serialize_fixed_point_shrunk")',
     b'if desired < charged: atomic_write(path, raw); return'),
    (b'require(desired >= charged, "checker:checkpoint_fixed_point_shrunk")',
     b'if desired < charged: atomic_write(path, encoded); return'),
    (b'CHECKER_BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 0, 4), (5,), (6,), (7,), (8,), (9,))',
     b'CHECKER_BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 4, 5), (6,), (7,), (8,), (9,), (10,))'),
    (b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v6.py"',
     b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v11.py"'),
)


def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("v12 checker: frozen v6 source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v12 checker: audited repair site is not unique")
        raw = raw.replace(old, new)
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(SOURCE), "exec"), ns, ns)


if __name__ == "__main__":
    main()
