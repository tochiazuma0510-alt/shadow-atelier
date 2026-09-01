#!/usr/bin/env python3
"""Independent A4 v27 checker: frozen v26 arithmetic plus delta replay."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v26.py")
OWNER_BYTES = 2216
OWNER_SHA256 = "b447bfc371090262a881db4b76261c534a8ef7a2b884edd65729aba1ea5fb2f4"
OWNER_GENERATED_BYTES = 272663
OWNER_GENERATED_SHA256 = "ffd53a2df28252feaf84fa5d96a3bc2bec8bf8d6e5ca31424be55ba8c24fb1dd"
RESULT_GENERATED_BYTES = 281781
RESULT_GENERATED_SHA256 = "5e0604a1c8560f79aed917f583162a896c788fd894ff192a7201c282c1276911"

PRODUCER_BYTES = 13268
PRODUCER_SHA256 = "23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236"

HELPERS = b'''def _checker_delta_base_state(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("ascii")); claimed = value.pop("self_digest_sha256", None)
    require(claimed == digest(value) and value.get("schema") == LEGACY_PRODUCER_CHECKPOINT_SCHEMA and
            value.get("owner") == "producer" and value.get("next_row") == 25 and
            value.get("row_cursor") == len(value.get("row_digests", [])) == 24 and
            value.get("bridge_cursor") == len(value.get("bridge_digests", [])) == 24,
            "checker:delta_canonical_base_state")
    records = value.get("oracle_records", []); events = value.get("query_event_chain", [])
    require(isinstance(records, list) and isinstance(events, list) and len(records) == len(events),
            "checker:delta_base_oracle_shape")
    epoch = "0" * 64
    for index, (record, event) in enumerate(zip(records, events), 1):
        require(event.get("index") == index and event.get("query_id") == record.get("query_id") and
                event.get("schema") == record.get("schema") and event.get("digest") == digest(record),
                "checker:delta_base_oracle_event")
        epoch = sha((epoch + digest(record)).encode("ascii"))
    require(epoch == value.get("epoch_digest"), "checker:delta_base_epoch")
    require(value.get("initial_terminal_records") == [record for record in records if is_row_terminal(record)] and
            value.get("initial_terminal_chain") == [event for event in events if is_row_terminal(event)] and
            len(value.get("initial_terminal_records", [])) == 24,
            "checker:delta_base_terminal_prefix")
    return value


def _checker_delta_apply(state: dict[str, Any], segment: dict[str, Any], expected_next_row: int) -> int:
    """Independently apply one segment and prove its row/cursor advance."""
    expected = int(expected_next_row)
    append_fields = ("row_digests", "bridge_digests", "row_chunks", "samples",
                     "oracle_records", "query_event_chain", "live_duals", "dual_event_chain",
                     "word_ledger_dag", "K_roster", "insertion_events",
                     "initial_terminal_records", "initial_terminal_chain")
    require(all(isinstance(segment.get(field), list) for field in append_fields) and
            isinstance(segment.get("queue_append"), list) and isinstance(segment.get("queue_phase"), dict),
            "checker:delta_segment_list_shape")
    records = segment["oracle_records"]; events = segment["query_event_chain"]
    require(len(records) == len(events), "checker:delta_oracle_event_length")
    record_start = len(state.get("oracle_records", [])); rebuilt_epoch = str(state.get("epoch_digest"))
    for offset, (record, event) in enumerate(zip(records, events), 1):
        require(event.get("index") == record_start + offset and
                event.get("query_id") == record.get("query_id") and
                event.get("schema") == record.get("schema") and
                event.get("digest") == digest(record), "checker:delta_oracle_event_digest")
        rebuilt_epoch = sha((rebuilt_epoch + digest(record)).encode("ascii"))
    require(segment.get("epoch_digest") == rebuilt_epoch, "checker:delta_epoch_advance")
    row_terminals = [record for record in records if is_row_terminal(record)]
    event_terminals = [event for event in events if is_row_terminal(event)]
    before_rows = len(state.get("row_digests", [])); before_bridges = len(state.get("bridge_digests", []))
    if expected <= ROWS:
        query_id = "R:" + str(expected)
        require(segment.get("kind") == "row" and segment.get("ordinal") == expected and
                segment.get("next_row") == expected + 1, "checker:delta_row_continuity")
        require(len(segment["row_digests"]) == len(segment["bridge_digests"]) == 1,
                "checker:delta_one_row_one_bridge")
        require(len(row_terminals) == len(event_terminals) == 1 and
                row_terminals[0].get("query_id") == query_id and
                event_terminals[0].get("query_id") == query_id and
                records[-1] == row_terminals[0] and events[-1] == event_terminals[0] and
                segment["initial_terminal_records"] == row_terminals and
                segment["initial_terminal_chain"] == event_terminals,
                "checker:delta_one_row_terminal_pair")
        advanced = expected + 1
    else:
        require(expected == ROWS + 1 and segment.get("kind") == "queue" and
                segment.get("ordinal") == ROWS + 1 and segment.get("next_row") == ROWS + 1,
                "checker:delta_queue_continuity")
        require(not segment["row_digests"] and not segment["bridge_digests"] and
                not row_terminals and not event_terminals and
                not segment["initial_terminal_records"] and not segment["initial_terminal_chain"],
                "checker:delta_queue_has_row_payload")
        advanced = ROWS + 1
    for field in append_fields:
        state.setdefault(field, []).extend(segment[field])
    state.setdefault("queue", []).extend(segment["queue_append"])
    for key, value in segment.get("sample_rows", {}).items():
        require(str(key) not in {str(old) for old in state.setdefault("sample_rows", {})},
                "checker:delta_sample_row_rewrite")
        state["sample_rows"][str(key)] = value
    phase = state.setdefault("queue_phase", {"actions": [], "action_event_chain": [],
                                              "matrix": {}, "inverse_laws": {}})
    add_actions = segment["queue_phase"].get("actions", [])
    add_events = segment["queue_phase"].get("action_event_chain", [])
    updates = segment["queue_phase"].get("matrix_updates", [])
    require(isinstance(add_actions, list) and isinstance(add_events, list) and isinstance(updates, list) and
            len(add_actions) == len(add_events) == len(updates), "checker:delta_action_delta_shape")
    action_start = len(phase.setdefault("actions", []))
    for offset, (action, event, update) in enumerate(zip(add_actions, add_events, updates), 1):
        require(event.get("index") == action_start + offset and event.get("digest") == digest(action) and
                update == {"letter": action.get("letter"), "parent": action.get("parent"),
                           "column": action.get("basis_column")},
                "checker:delta_action_event_update")
        phase.setdefault("matrix", {}).setdefault(str(update["letter"]), {})[update["parent"]] = update["column"]
    phase["actions"].extend(add_actions); phase.setdefault("action_event_chain", []).extend(add_events)
    phase.setdefault("inverse_laws", {}).update(segment["queue_phase"].get("inverse_laws", {}))
    phase["queue_head"] = int(segment.get("queue_head", phase.get("queue_head", 0)))
    phase["queue_length"] = len(state["queue"]); phase["action_count"] = len(phase["actions"])
    phase["matrix_digest"] = digest(phase["matrix"]); state["queue_head"] = phase["queue_head"]
    state["next_row"] = int(segment["next_row"]); state["row_cursor"] = len(state["row_digests"])
    state["bridge_cursor"] = len(state["bridge_digests"]); state["epoch_digest"] = rebuilt_epoch
    state["row_replay_sha256"] = digest(state["row_digests"])
    state["bridge_replay_sha256"] = digest(state["bridge_digests"])
    state["counters"] = dict(segment.get("counters", state.get("counters", {})))
    state["semantic_counters"] = dict(segment.get("semantic_counters", state.get("semantic_counters", {})))
    state["host_counters"] = dict(segment.get("host_counters", state.get("host_counters", {})))
    state["peak_counters"] = dict(segment.get("peak_counters", state.get("peak_counters", {})))
    state["restore_validation_counters"] = dict(segment.get("restore_validation_counters",
                                                              state.get("restore_validation_counters", {})))
    state.setdefault("host_history", []).extend(segment.get("host_history_append", []))
    if segment.get("kind") == "row":
        require(len(state["row_digests"]) == before_rows + 1 == int(segment["ordinal"]) and
                len(state["bridge_digests"]) == before_bridges + 1 == int(segment["ordinal"]) and
                state["next_row"] == advanced, "checker:delta_reconstructed_row_advance")
    else:
        require(len(state["row_digests"]) == before_rows and
                len(state["bridge_digests"]) == before_bridges and state["next_row"] == advanced,
                "checker:delta_reconstructed_queue_advance")
    return advanced


'''

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v20.py"\n'
        b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v27"\n',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v21.py"\n'
        b'PRODUCER_CODE_BYTES = 13268\n'
        b'PRODUCER_CODE_SHA256 = "23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236"\n'
        b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v27"\n',
    ),
    (
        b'def validate_delta_terminal_chain(reference: dict[str, Any], meter: Meter) -> None:\n',
        HELPERS + b'def validate_delta_terminal_chain(reference: dict[str, Any], meter: Meter) -> None:\n',
    ),
    (
        b'    base = head.get("base", {}); base_path = head_path.with_name(str(base.get("path", "")))\n'
        b'    base_raw = base_path.read_bytes()\n'
        b'    require(base == {"path": base_path.name, "bytes": len(base_raw), "sha256": sha(base_raw)} and\n',
        b'    producer_raw = (ROOT / PRODUCER_CODE_PATH).read_bytes()\n'
        b'    require(len(producer_raw) == PRODUCER_CODE_BYTES and sha(producer_raw) == PRODUCER_CODE_SHA256,\n'
        b'            "checker:delta_producer_pin")\n'
        b'    base = head.get("base", {}); base_path = head_path.with_name(str(base.get("path", "")))\n'
        b'    base_raw = base_path.read_bytes()\n'
        b'    require(base == {"path": base_path.name, "bytes": len(base_raw), "sha256": sha(base_raw)} and\n',
    ),
    (
        b'            "checker:delta_base_identity")\n'
        b'    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64\n',
        b'            "checker:delta_base_identity")\n'
        b'    state = _checker_delta_base_state(base_raw)\n'
        b'    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64\n'
        b'    expected_next_row = int(state["next_row"])\n',
    ),
    (
        b'        require(segment.get("chain") == chain, "checker:delta_chain_digest")\n'
        b'        previous = sha(segment_raw)\n',
        b'        require(segment.get("chain") == chain, "checker:delta_chain_digest")\n'
        b'        expected_next_row = _checker_delta_apply(state, segment, expected_next_row)\n'
        b'        previous = sha(segment_raw)\n',
    ),
    (
        b'            reference.get("next_row") == head.get("next_row") and reference.get("chain") == chain,\n'
        b'            "checker:delta_terminal_binding")\n',
        b'            reference.get("next_row") == head.get("next_row") and reference.get("chain") == chain and\n'
        b'            head.get("next_row") == expected_next_row and state.get("next_row") == expected_next_row,\n'
        b'            "checker:delta_terminal_binding")\n',
    ),
)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v27 checker: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v27 checker: frozen v26 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v26_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v27 checker: frozen v26 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v27 checker: resulting generated source drift")
    return raw


def _toy_namespace() -> dict[str, Any]:
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v26_owner_test",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    owner_raw = OWNER.read_bytes(); exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = _apply_patches(owner_ns["restore_frozen"]())
    ns: dict[str, Any] = {"__name__": "_r07_a4_v27_test",
                          "__file__": str(Path(__file__).resolve()),
                          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)
    return ns


def self_test() -> None:
    ns = _toy_namespace(); digest = ns["digest"]; sha = ns["sha"]; canon = ns["canon"]
    chain_digest = ns["_producer_delta_chain"]; apply = ns["_checker_delta_apply"]
    Reject = ns["Reject"]

    records = []
    events = []
    epoch = "0" * 64
    for ordinal in range(1, 25):
        record = {"schema": "MEMBER", "query_id": f"R:{ordinal}", "rank": 0,
                  "row_digest": f"base-row-{ordinal}", "terminal": True}
        records.append(record)
        events.append({"index": ordinal, "query_id": record["query_id"],
                       "schema": record["schema"], "digest": digest(record)})
        epoch = sha((epoch + digest(record)).encode("ascii"))
    base = {"next_row": 25, "row_digests": [f"r{i}" for i in range(1, 25)],
            "bridge_digests": [f"b{i}" for i in range(1, 25)], "row_chunks": [],
            "samples": [], "sample_rows": {}, "oracle_records": records,
            "query_event_chain": events, "live_duals": [], "dual_event_chain": [],
            "word_ledger_dag": [], "K_roster": [], "insertion_events": [], "queue": [],
            "initial_terminal_records": list(records), "initial_terminal_chain": list(events),
            "queue_phase": {"actions": [], "action_event_chain": [],
                            "matrix": {"1": {}, "-1": {}, "2": {}, "-2": {}},
                            "inverse_laws": {}}, "queue_head": 0, "epoch_digest": epoch,
            "counters": {}, "semantic_counters": {}, "host_counters": {},
            "peak_counters": {}, "restore_validation_counters": {}, "host_history": []}

    def segment_for(state: dict[str, Any], ordinal: int) -> dict[str, Any]:
        record = {"schema": "MEMBER", "query_id": f"R:{ordinal}", "rank": 0,
                  "row_digest": f"target-{ordinal}", "terminal": True}
        event = {"index": len(state["oracle_records"]) + 1, "query_id": record["query_id"],
                 "schema": record["schema"], "digest": digest(record)}
        next_epoch = sha((state["epoch_digest"] + digest(record)).encode("ascii"))
        return {"schema": ns["PRODUCER_DELTA_SCHEMA"], "owner": "producer", "kind": "row",
                "ordinal": ordinal, "next_row": ordinal + 1, "base": {"toy": True},
                "previous": None, "row_digests": [f"r{ordinal}"],
                "bridge_digests": [f"b{ordinal}"], "row_chunks": [], "samples": [],
                "sample_rows": {}, "oracle_records": [record], "query_event_chain": [event],
                "live_duals": [], "dual_event_chain": [], "initial_terminal_records": [record],
                "initial_terminal_chain": [event], "word_ledger_dag": [], "K_roster": [],
                "insertion_events": [], "queue_append": [], "queue_head": 0,
                "queue_phase": {"actions": [], "action_event_chain": [], "matrix_updates": [],
                                "inverse_laws": {}}, "epoch_digest": next_epoch,
                "counter_delta": {}, "counters": {}, "semantic_counters": {},
                "host_counters": {}, "peak_counters": {}, "restore_validation_counters": {},
                "host_history_append": []}

    state25 = json.loads(canon(base).decode("ascii")); s25 = segment_for(state25, 25)
    assert apply(state25, s25, 25) == 26
    s26 = segment_for(state25, 26)
    assert apply(state25, s26, 26) == 27 and state25["next_row"] == 27

    def sealed_chain(bodies: list[dict[str, Any]]) -> tuple[list[bytes], dict[str, Any]]:
        previous = None; chain = "0" * 64; raws = []
        for sequence, original in enumerate(bodies, 1):
            body = json.loads(canon(original).decode("ascii")); body["sequence"] = sequence
            body["previous"] = previous; body["chain"] = chain_digest(body, chain)
            body["self_digest_sha256"] = digest(body); raw = canon(body); raws.append(raw)
            previous = sha(raw); chain = body["chain"]
        last = json.loads(raws[-1].decode("ascii")) if raws else None
        head = {"last_sequence": len(raws), "segment_count": len(raws),
                "last_segment_sha256": previous, "chain": chain,
                "last_row": last["ordinal"] if last else 24,
                "next_row": last["next_row"] if last else 25}
        head["self_digest_sha256"] = digest(head)
        return raws, head

    def replay(bodies: list[dict[str, Any]], head_mutator: Any = None,
               reorder: bool = False) -> None:
        raws, head = sealed_chain(bodies)
        if reorder: raws = list(reversed(raws))
        if head_mutator is not None:
            head_mutator(head); head["self_digest_sha256"] = digest({k: v for k, v in head.items()
                                                                     if k != "self_digest_sha256"})
        claimed = head.pop("self_digest_sha256")
        ns["require"](claimed == digest(head), "toy:head_seal")
        state = json.loads(canon(base).decode("ascii")); previous = None; chain = "0" * 64; expected = 25
        for sequence, raw in enumerate(raws, 1):
            segment = json.loads(raw.decode("ascii")); seal = segment.pop("self_digest_sha256")
            ns["require"](seal == digest(segment) and segment.get("sequence") == sequence and
                          segment.get("previous") == previous, "toy:segment_order")
            chain = chain_digest(segment, chain); ns["require"](segment.get("chain") == chain, "toy:chain")
            expected = apply(state, segment, expected); previous = sha(raw)
        ns["require"](head["last_sequence"] == len(raws) and
                      head["last_segment_sha256"] == previous and head["chain"] == chain and
                      head["next_row"] == expected, "toy:head_ahead")

    s25 = segment_for(json.loads(canon(base).decode("ascii")), 25)
    tmp = json.loads(canon(base).decode("ascii")); apply(tmp, s25, 25)
    s26 = segment_for(tmp, 26); replay([s25, s26])
    mutations = {}

    def rejected(name: str, mutate: Any, head: Any = None, reorder: bool = False) -> None:
        bodies = [json.loads(canon(s25).decode("ascii")), json.loads(canon(s26).decode("ascii"))]
        mutate(bodies)
        try:
            replay(bodies, head, reorder)
        except (Reject, AssertionError, KeyError, IndexError):
            mutations[name] = "REJECT"
            return
        raise AssertionError(name + " was accepted")

    rejected("empty_first_row", lambda b: (b[0]["row_digests"].clear(), b[0]["bridge_digests"].clear()))
    rejected("skipped_row25", lambda b: b[0].update({"ordinal": 26, "next_row": 27}))
    rejected("forged_next_row27", lambda b: b[0].update({"next_row": 27}))
    rejected("row_digest_deletion", lambda b: b[0]["row_digests"].clear())
    rejected("bridge_deletion", lambda b: b[0]["bridge_digests"].clear())
    rejected("terminal_event_deletion", lambda b: b[0]["query_event_chain"].clear())
    rejected("reordered_segment", lambda b: None, reorder=True)
    rejected("head_ahead_of_segment", lambda b: None, head=lambda h: h.update({"next_row": 28}))
    assert len(mutations) == 8
    print("R07_A4_DELTA_REPLAY_V27_SELFTEST_PASS rows=2 mutations=8 atomic_head=PASS")


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
