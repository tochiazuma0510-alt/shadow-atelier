#!/usr/bin/env python3
"""A4 v20 producer: v19 delta transport with the restore-mode local bound."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v19.py")
OWNER_BYTES = 2388
OWNER_SHA256 = "c7add6648f53e4ec85eb40620e3469008349e5676ac7d9602a6699a52cb4c6c1"
OWNER_GENERATED_BYTES = 251746
OWNER_GENERATED_SHA256 = "223dd0b759780ed90b8d259311646a41425f40bf00b161e187a98cde73d7c796"
RESULT_GENERATED_BYTES = 251799
RESULT_GENERATED_SHA256 = "b41728b707a21e9fd6487ce015fe4df2dfd6c0040f0d098a399143a55600b2ee"

PATCHES = (
    (
        b'    boundary_state = state.get("boundary_echelon", {})\n',
        b'    delta_mode = bool(state.get("_delta_transport"))\n'
        b'    boundary_state = state.get("boundary_echelon", {})\n',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v20 producer: frozen v19 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v19_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v20 producer: frozen v19 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v20 producer: audited site is not unique")
        raw = raw.replace(old, new)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v20 producer: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
