#!/usr/bin/env python3
"""Independent v8 owner for the A3 checker reason-map repair."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name("check_d972_r07_pre_a0_single_target_a3_v6.py")
SOURCE_BYTES = 120097
SOURCE_SHA256 = "c38dfc6f392e3595d0ff00001ba19453b7a9022643ef1c9f06862d6f37934ab8"
PATCHES = (
    (
        b'mutant_owner["bar_epsilon_1"]["H1"] = []',
        b'mutant_owner["bar_epsilon_1"]["H1"] = None',
    ),
    (b'mutant_bar["H1"] = []', b'mutant_bar["H1"] = None'),
    (
        b'"task227 consumer ABI derived only from projection":\n                    "ABI seal/target"',
        b'"checker task227 consumer ABI derived only from projection":\n                    "ABI seal/target"',
    ),
)


def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("A3 v8 checker: frozen v6 source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("A3 v8 checker: audited repair site is not unique")
        raw = raw.replace(old, new)
    namespace = {
        "__name__": "__main__",
        "__file__": str(Path(__file__).resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(raw, str(SOURCE), "exec"), namespace, namespace)


if __name__ == "__main__":
    main()
