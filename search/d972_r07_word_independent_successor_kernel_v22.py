#!/usr/bin/env python3
"""A4 v22 producer: exact v21 arithmetic with terminal-cursor advance."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v21.py")
OWNER_BYTES = 13268
OWNER_SHA256 = "23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236"
OWNER_GENERATED_BYTES = 256315
OWNER_GENERATED_SHA256 = "e1005be315d97b5045965921ba93a72ea2a8c5024e3abf1dbda5459a09c99f76"
RESULT_GENERATED_BYTES = 256509
RESULT_GENERATED_SHA256 = "20fdeb66f70f428152e06f5e7a92b455dd211bd0e72d665c10d24d2ad0491e94"

PATCHES = (
    (
        b'        "events": len(oracle.event_chain), "duals": len(oracle.live_duals), "dual_events": len(oracle.dual_chain),\n',
        b'        "events": len(oracle.event_chain),\n'
        b'        "initial_records": tracker["initial_records"] + len(body["initial_terminal_records"]),\n'
        b'        "initial_events": tracker["initial_events"] + len(body["initial_terminal_chain"]),\n'
        b'        "duals": len(oracle.live_duals), "dual_events": len(oracle.dual_chain),\n',
    ),
)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v22 producer: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v22 producer: frozen v21 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v21_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v22 producer: frozen v21 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v22 producer: resulting generated source drift")
    return raw


def self_test() -> None:
    raw = restore_frozen()
    text = raw.decode("ascii")
    record_advance = '"initial_records": tracker["initial_records"] + len(body["initial_terminal_records"])'
    event_advance = '"initial_events": tracker["initial_events"] + len(body["initial_terminal_chain"])'
    assert text.count(record_advance) == text.count(event_advance) == 1
    segment_write = text.index("write_atomic(segment, encoded)")
    head_write = text.index("write_atomic(path, head_encoded)")
    tracker_update = text.index("tracker.update({", head_write)
    assert segment_write < head_write < tracker_update

    tracker = {"initial_records": 24, "initial_events": 24}
    accepted = {"initial_terminal_records": [{"query_id": "R:25"}],
                "initial_terminal_chain": [{"query_id": "R:25"}]}
    tracker["initial_records"] += len(accepted["initial_terminal_records"])
    tracker["initial_events"] += len(accepted["initial_terminal_chain"])
    records = [{"query_id": f"R:{row}"} for row in range(1, 27)]
    events = [{"query_id": f"R:{row}"} for row in range(1, 27)]
    assert records[tracker["initial_records"]:] == [{"query_id": "R:26"}]
    assert events[tracker["initial_events"]:] == [{"query_id": "R:26"}]
    print("R07_A4_TERMINAL_CURSOR_V22_SELFTEST_PASS patches=%d rows=2" % len(PATCHES))


def main() -> None:
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
