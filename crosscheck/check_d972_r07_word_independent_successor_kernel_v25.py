#!/usr/bin/env python3
"""Independent A4 v25 checker: task410 v24 transport with canonical base pin."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v24.py")
OWNER_BYTES = 7508
OWNER_SHA256 = "3e10816d31a791695cf0b01fb1386ceb9c0dcd064dfcde63ab59e413278be2c6"
OWNER_GENERATED_BYTES = 272663
OWNER_GENERATED_SHA256 = "55f10d5a6339d3ababca981766aa7509933355d4a7054e6a742a68f5bfc333b6"
RESULT_GENERATED_BYTES = 272663
RESULT_GENERATED_SHA256 = "344168094ed6dd597b4a5d15bda87d2c348d4fa233e9de7ba1eb7426ef201493"

PATCHES = (
    (
        b"595213bab8936ef10e94ce90ccf526c105d02d871d4dc5d02b6c76cb51593445",
        b"595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445",
    ),
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v18.py"',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v19.py"',
    ),
    (
        b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v26"',
        b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v27"',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v25 checker: frozen v24 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v24_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v25 checker: frozen v24 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v25 checker: audited site is not unique")
        raw = raw.replace(old, new)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v25 checker: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
