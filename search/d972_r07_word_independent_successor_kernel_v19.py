#!/usr/bin/env python3
"""A4 v19 producer: task410 v18 delta transport with canonical base pin."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v18.py")
OWNER_BYTES = 27094
OWNER_SHA256 = "6d8b53755fc0c9e35aad6f04959f828a6ce5108767ffc57edfaa896366673f5a"
OWNER_GENERATED_BYTES = 251746
OWNER_GENERATED_SHA256 = "b4d852354d3753844ed9d64041d2c3b3f1221b81ba7fb7ae6cedb33b0873eeed"
RESULT_GENERATED_BYTES = 251746
RESULT_GENERATED_SHA256 = "223dd0b759780ed90b8d259311646a41425f40bf00b161e187a98cde73d7c796"

PATCHES = (
    (
        b"595213bab8936ef10e94ce90ccf526c105d02d871d4dc5d02b6c76cb51593445",
        b"595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445",
    ),
    (
        b'CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v26"',
        b'CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v27"',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v19 producer: frozen v18 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v18_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v19 producer: frozen v18 generated source drift")
    for index, (old, new) in enumerate(PATCHES):
        expected = 2 if index == 0 else 1
        if raw.count(old) != expected:
            raise SystemExit("v19 producer: audited site is not unique")
        raw = raw.replace(old, new)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v19 producer: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
