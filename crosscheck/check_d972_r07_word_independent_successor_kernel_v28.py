#!/usr/bin/env python3
"""Independent A4 v28 checker: v27 replay with two-row cursor fixture."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v27.py")
OWNER_BYTES = 21489
OWNER_SHA256 = "79f42e751684f12814ac25dc7bd17ee5a6fa21b8ab9b8bdfc07c14bd37e4af2a"
OWNER_GENERATED_BYTES = 281781
OWNER_GENERATED_SHA256 = "5e0604a1c8560f79aed917f583162a896c788fd894ff192a7201c282c1276911"
RESULT_GENERATED_BYTES = 281780
RESULT_GENERATED_SHA256 = "444ee68e79715657707c77778fcb597f83d289147699e7ce5295414b956edeae"

PRODUCER_BYTES = 4055
PRODUCER_SHA256 = "0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2"

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v21.py"\n'
        b'PRODUCER_CODE_BYTES = 13268\n'
        b'PRODUCER_CODE_SHA256 = "23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236"\n',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v22.py"\n'
        b'PRODUCER_CODE_BYTES = 4055\n'
        b'PRODUCER_CODE_SHA256 = "0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2"\n',
    ),
)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v28 checker: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v28 checker: frozen v27 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v27_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v28 checker: frozen v27 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v28 checker: resulting generated source drift")
    return raw


def _toy_namespace() -> dict[str, Any]:
    raw = restore_frozen()
    ns: dict[str, Any] = {"__name__": "_r07_a4_v28_test",
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
    assert s26["row_digests"] == ["r26"] and s26["bridge_digests"] == ["b26"]
    assert [record["query_id"] for record in s26["oracle_records"]] == ["R:26"] and \
           [event["query_id"] for event in s26["query_event_chain"]] == ["R:26"]
    assert [record["query_id"] for record in s26["initial_terminal_records"]] == ["R:26"] and \
           [event["query_id"] for event in s26["initial_terminal_chain"]] == ["R:26"]
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
        if reorder:
            raws = list(reversed(raws))
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
    rejected("stale_terminal_record_cursor", lambda b: b[1]["initial_terminal_records"].insert(
             0, b[0]["initial_terminal_records"][0]))
    rejected("stale_terminal_event_cursor", lambda b: b[1]["initial_terminal_chain"].insert(
             0, b[0]["initial_terminal_chain"][0]))
    assert len(mutations) == 10
    print("R07_A4_DELTA_REPLAY_V28_SELFTEST_PASS rows=2 mutations=10 atomic_head=PASS")


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
