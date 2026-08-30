#!/usr/bin/env python3
"""Independent A4 v26 checker: v25 arithmetic pinned to producer v20."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v25.py")
OWNER_BYTES = 2540
OWNER_SHA256 = "4c04fd31fe4a27c96841ddc5931961cc6d2e4162f98f239df3577ee367a57317"
OWNER_GENERATED_BYTES = 272663
OWNER_GENERATED_SHA256 = "344168094ed6dd597b4a5d15bda87d2c348d4fa233e9de7ba1eb7426ef201493"
RESULT_GENERATED_BYTES = 272663
RESULT_GENERATED_SHA256 = "ffd53a2df28252feaf84fa5d96a3bc2bec8bf8d6e5ca31424be55ba8c24fb1dd"

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v19.py"',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v20.py"',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v26 checker: frozen v25 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v25_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v26 checker: frozen v25 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v26 checker: audited site is not unique")
        raw = raw.replace(old, new)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v26 checker: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
