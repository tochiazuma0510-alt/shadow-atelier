#!/usr/bin/env python3
"""Independent A4 v23 checker: v22 pinned to the v17 producer.

Only the producer code path and producer checkpoint schema pins advance.  The
independent arithmetic, terminal vocabulary, and checker checkpoint rules
remain the frozen v22 implementation.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v22.py")
OWNER_BYTES = 6579
OWNER_SHA256 = "91ae327d9a983136cc5a1ac9188dc1ea11f9e553aef606e8bc4bf45cb9bd819a"
OWNER_GENERATED_BYTES = 268101
OWNER_GENERATED_SHA256 = "28cba6455e249edac835babb63b099940d91965d4e7c0f1d6a5310c57d569d18"
RESULT_GENERATED_BYTES = 268101
RESULT_GENERATED_SHA256 = "6bee9fe57b9d10af5e9ef024a8510cc94a7733869b5a88cb04ecd494eef5c786"

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v16.py"',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v17.py"',
    ),
    (
        b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v24"',
        b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v25"',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v23 checker: frozen v22 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v22_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if (len(raw) != OWNER_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256):
        raise SystemExit("v23 checker: frozen v22 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v23 checker: audited site is not unique")
        raw = raw.replace(old, new)
    if (len(raw) != RESULT_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256):
        raise SystemExit("v23 checker: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
