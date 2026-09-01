#!/usr/bin/env python3
"""A4 v21 producer: exact v20 arithmetic with repaired delta transport."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v20.py")
OWNER_BYTES = 2239
OWNER_SHA256 = "c45d48ac27f462cf342912e17e619be02ca68322c62a21897fcdc3d524e07a6f"
OWNER_GENERATED_BYTES = 251799
OWNER_GENERATED_SHA256 = "b41728b707a21e9fd6487ce015fe4df2dfd6c0040f0d098a399143a55600b2ee"
RESULT_GENERATED_BYTES = 256315
RESULT_GENERATED_SHA256 = "e1005be315d97b5045965921ba93a72ea2a8c5024e3abf1dbda5459a09c99f76"

PATCHES = (
    (
        b'            "actions": len(actions), "action_events": len(action_events),\n'
        b'            "sample_keys": set(getattr(oracle, "sample_rows", {}).keys()),\n',
        b'            "actions": len(actions), "action_events": len(action_events),\n'
        b'            "matrix": {str(letter): dict(columns) for letter, columns in matrix.items()},\n'
        b'            "sample_keys": set(getattr(oracle, "sample_rows", {}).keys()),\n',
    ),
    (
        b'    """Append one delta and atomically advance HEAD; no prefix snapshot is made."""\n'
        b'    if not hasattr(meter, "_a4_delta_tracker"):\n'
        b'        meter._a4_delta_resume = getattr(meter, "_a4_delta_resume", {}) or {}\n'
        b'        phase = queue_phase or {}\n'
        b'        meter._a4_delta_tracker = _delta_tracker(oracle, words, queue,\n'
        b'                                                   list(phase.get("actions", [])),\n'
        b'                                                   list(phase.get("action_event_chain", [])),\n'
        b'                                                   dict(phase.get("matrix", {})), meter)\n'
        b'    tracker = meter._a4_delta_tracker; base = _delta_base_path(path)\n',
        b'    """Append one delta and atomically advance HEAD; no prefix snapshot is made."""\n'
        b'    require(hasattr(meter, "_a4_delta_tracker"), "delta:tracker_not_preloop_initialized")\n'
        b'    tracker = meter._a4_delta_tracker; base = _delta_base_path(path)\n',
    ),
    (
        b'    kind = "row" if int(next_row) <= ROWS else "queue"\n'
        b'    body = _delta_payload(authority, meter, next_row, oracle, words, queue, cursor,\n'
        b'                          queue_phase or {}, tracker, kind)\n'
        b'    seq = int(tracker["seq"]) + 1; body["sequence"] = seq\n',
        b'    expected_next_row = int(tracker.get("last_next_row", LEGACY_BASE_NEXT_ROW))\n'
        b'    kind = "row" if expected_next_row <= ROWS else "queue"\n'
        b'    body = _delta_payload(authority, meter, next_row, oracle, words, queue, cursor,\n'
        b'                          queue_phase or {}, tracker, kind)\n'
        b'    _delta_validate_segment(body, expected_next_row)\n'
        b'    seq = int(tracker["seq"]) + 1; body["sequence"] = seq\n',
    ),
    (
        b'        "actions": len(queue_phase.get("actions", [])) if queue_phase else tracker["actions"],\n'
        b'        "action_events": len(queue_phase.get("action_event_chain", [])) if queue_phase else tracker["action_events"],\n'
        b'        "sample_keys": set(oracle.sample_rows.keys()), "counters": dict(meter.counters),\n',
        b'        "actions": len(queue_phase.get("actions", [])) if queue_phase else tracker["actions"],\n'
        b'        "action_events": len(queue_phase.get("action_event_chain", [])) if queue_phase else tracker["action_events"],\n'
        b'        "matrix": {str(letter): dict(columns) for letter, columns in\n'
        b'                   (queue_phase.get("matrix", {}) if queue_phase else tracker["matrix"]).items()},\n'
        b'        "sample_keys": set(oracle.sample_rows.keys()), "counters": dict(meter.counters),\n',
    ),
    (
        b'def _delta_apply_dict(target: dict[str, Any], delta: dict[str, int]) -> None:\n',
        b'''def _delta_validate_segment(segment: dict[str, Any], expected_next_row: int) -> int:
    """Validate one transport step without assuming a K/queue rank rise."""
    expected = int(expected_next_row)
    list_fields = ("row_digests", "bridge_digests", "oracle_records", "query_event_chain",
                   "initial_terminal_records", "initial_terminal_chain", "K_roster",
                   "insertion_events", "queue_append")
    require(all(isinstance(segment.get(field), list) for field in list_fields),
            "delta:segment_list_shape")
    records = segment["oracle_records"]; events = segment["query_event_chain"]
    require(len(records) == len(events), "delta:oracle_event_delta_length")
    for record, event in zip(records, events):
        require(event.get("query_id") == record.get("query_id") and
                event.get("schema") == record.get("schema") and
                event.get("digest") == digest(record), "delta:oracle_event_delta_digest")
    terminals_r = [record for record in records if is_row_terminal(record)]
    terminals_e = [event for event in events if is_row_terminal(event)]
    if expected <= ROWS:
        query_id = "R:" + str(expected)
        require(segment.get("kind") == "row" and segment.get("ordinal") == expected and
                segment.get("next_row") == expected + 1,
                "delta:row_cursor_continuity")
        require(len(segment["row_digests"]) == 1 and
                len(segment["bridge_digests"]) == 1,
                "delta:one_row_one_bridge")
        require(len(terminals_r) == len(terminals_e) == 1 and
                terminals_r[0].get("query_id") == query_id and
                terminals_e[0].get("query_id") == query_id and
                records[-1] == terminals_r[0] and events[-1] == terminals_e[0] and
                segment["initial_terminal_records"] == terminals_r and
                segment["initial_terminal_chain"] == terminals_e,
                "delta:one_row_terminal_pair")
        return expected + 1
    require(expected == ROWS + 1 and segment.get("kind") == "queue" and
            segment.get("ordinal") == ROWS + 1 and segment.get("next_row") == ROWS + 1,
            "delta:queue_cursor_continuity")
    require(not segment["row_digests"] and not segment["bridge_digests"] and
            not terminals_r and not terminals_e and
            not segment["initial_terminal_records"] and
            not segment["initial_terminal_chain"], "delta:queue_has_row_payload")
    return ROWS + 1


def _delta_apply_dict(target: dict[str, Any], delta: dict[str, int]) -> None:
''',
    ),
    (
        b'    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64\n'
        b'    for sequence in range(1, count + 1):\n',
        b'    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64\n'
        b'    expected_next_row = LEGACY_BASE_NEXT_ROW\n'
        b'    for sequence in range(1, count + 1):\n',
    ),
    (
        b'        require(segment.get("chain") == chain, "delta:reference_chain"); previous = sha(segment_raw)\n'
        b'    require(head.get("last_sequence") == count and head.get("last_segment_sha256") == previous and\n',
        b'        require(segment.get("chain") == chain, "delta:reference_chain")\n'
        b'        expected_next_row = _delta_validate_segment(segment, expected_next_row)\n'
        b'        previous = sha(segment_raw)\n'
        b'    require(head.get("last_sequence") == count and head.get("last_segment_sha256") == previous and\n',
    ),
    (
        b'    count = int(head.get("segment_count", 0)); prev = None; chain = "0" * 64\n'
        b'    for seq in range(1, count + 1):\n',
        b'    count = int(head.get("segment_count", 0)); prev = None; chain = "0" * 64\n'
        b'    expected_next_row = int(state.get("next_row", 0))\n'
        b'    require(expected_next_row == LEGACY_BASE_NEXT_ROW, "delta:base_next_row")\n'
        b'    for seq in range(1, count + 1):\n',
    ),
    (
        b'        chain = _delta_chain_digest(segment, chain); require(segment.get("chain") == chain, "delta:chain_digest")\n'
        b'        _delta_apply_segment(state, segment); prev = sha(raw)\n',
        b'        chain = _delta_chain_digest(segment, chain); require(segment.get("chain") == chain, "delta:chain_digest")\n'
        b'        before_rows = len(state.get("row_digests", [])); before_bridges = len(state.get("bridge_digests", []))\n'
        b'        before_records = len(state.get("oracle_records", [])); prior_epoch = str(state.get("epoch_digest"))\n'
        b'        next_expected = _delta_validate_segment(segment, expected_next_row)\n'
        b'        for offset, event in enumerate(segment["query_event_chain"], 1):\n'
        b'            require(event.get("index") == before_records + offset, "delta:event_index_continuity")\n'
        b'        rebuilt_epoch = prior_epoch\n'
        b'        for record in segment["oracle_records"]:\n'
        b'            rebuilt_epoch = sha((rebuilt_epoch + digest(record)).encode("ascii"))\n'
        b'        require(rebuilt_epoch == segment.get("epoch_digest"), "delta:epoch_advance")\n'
        b'        _delta_apply_segment(state, segment)\n'
        b'        require(state.get("next_row") == next_expected, "delta:state_next_row_advance")\n'
        b'        if segment.get("kind") == "row":\n'
        b'            require(len(state["row_digests"]) == before_rows + 1 == int(segment["ordinal"]) and\n'
        b'                    len(state["bridge_digests"]) == before_bridges + 1 == int(segment["ordinal"]),\n'
        b'                    "delta:state_row_advance")\n'
        b'        else:\n'
        b'            require(len(state["row_digests"]) == before_rows and\n'
        b'                    len(state["bridge_digests"]) == before_bridges, "delta:state_queue_advance")\n'
        b'        expected_next_row = next_expected; prev = sha(raw)\n',
    ),
    (
        b'        checkpoint_writes_enabled = True\n'
        b'    for ordinal, row in enumerate(authority.rows[resume_row - 1:], resume_row):\n',
        b'        checkpoint_writes_enabled = True\n'
        b'        if resume_state.get("_delta_transport"):\n'
        b'            require(not hasattr(meter, "_a4_delta_tracker"), "delta:tracker_initialized_twice")\n'
        b'            meter._a4_delta_tracker = _delta_tracker(oracle, words, queue, actions,\n'
        b'                                                       action_event_chain, matrix, meter)\n'
        b'            meter._a4_delta_tracker["last_row"] = resume_row - 1\n'
        b'            meter._a4_delta_tracker["last_next_row"] = resume_row\n'
        b'    for ordinal, row in enumerate(authority.rows[resume_row - 1:], resume_row):\n',
    ),
)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v21 producer: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v21 producer: frozen v20 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v20_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v21 producer: frozen v20 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v21 producer: resulting generated source drift")
    return raw


def self_test() -> None:
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v20_owner_test",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    owner_raw = OWNER.read_bytes()
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    before = owner_ns["restore_frozen"]()
    after = _apply_patches(before)
    text = after.decode("ascii")
    assert text.count('meter._a4_delta_tracker = _delta_tracker(') == 1
    assert text.index('meter.install_completed(') < text.index('meter._a4_delta_tracker = _delta_tracker(')
    assert text.index('meter._a4_delta_tracker = _delta_tracker(') < text.index('for ordinal, row in enumerate(')
    assert 'delta:one_row_one_bridge' in text and 'delta:one_row_terminal_pair' in text
    print("R07_A4_DELTA_TRACKER_PRELOOP_V21_SELFTEST_PASS patches=%d" % len(PATCHES))


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
