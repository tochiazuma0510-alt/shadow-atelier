#!/usr/bin/env python3
"""Independent production v7 owner for the frozen A3 v6 checker."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name("check_d972_r07_pre_a0_single_target_a3_v6.py")
SOURCE_BYTES = 120097
SOURCE_SHA256 = "c38dfc6f392e3595d0ff00001ba19453b7a9022643ef1c9f06862d6f37934ab8"
OLD_TARGET = b'mutant_owner["bar_epsilon_1"]["H1"] = []'
NEW_TARGET = b'mutant_owner["bar_epsilon_1"]["H1"] = None'
OLD_ABI = b'mutant_bar["H1"] = []'
NEW_ABI = b'mutant_bar["H1"] = None'


def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("A3 v7 checker: frozen v6 source drift")
    if raw.count(OLD_TARGET) != 1 or raw.count(OLD_ABI) != 1:
        raise SystemExit("A3 v7 checker: stale mutation sites")
    patched = raw.replace(OLD_TARGET, NEW_TARGET).replace(OLD_ABI, NEW_ABI)
    namespace = {
        "__name__": "__main__",
        "__file__": str(Path(__file__).resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(patched, str(SOURCE), "exec"), namespace, namespace)


if __name__ == "__main__":
    main()
