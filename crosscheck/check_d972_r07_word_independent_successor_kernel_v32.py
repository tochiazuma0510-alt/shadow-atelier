#!/usr/bin/env python3
"""Independent A4 v32 checker: v31 mathematics plus shard-chain gates."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v31.py")
OWNER_BYTES = 19483
OWNER_SHA256 = "7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e"
OWNER_GENERATED_BYTES = 288650
OWNER_GENERATED_SHA256 = "89d8626f8c14972ccad21efa441de07e5e9cf1baf18f98a68751f8bc16e46744"
RESULT_GENERATED_BYTES = 293042
RESULT_GENERATED_SHA256 = "80ac3ff80b106691f667840891e99904b1a9f2bc58dfe0b700b893904ad38440"
_ANCHOR = b"def validate_terminal_payload"

_CHECKER_HELPER = b'''\
\ndef _a4_checker_row(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and all(isinstance(k, str) and isinstance(v, int) and
             not isinstance(v, bool) and v % 3 for k, v in value.items()), "shard:row_shape")
    return {k: int(v) % 3 for k, v in value.items() if int(v) % 3}


def _a4_checker_validate_shards(head: dict[str, Any], shards: list[dict[str, Any]],
                                open_query: dict[str, Any] | None,
                                completed_records: list[dict[str, Any]],
                                completed_events: list[dict[str, Any]]) -> dict[str, Any]:
    require(isinstance(head, dict) and isinstance(shards, list), "shard:container")
    previous = None; chain = "0" * 64; pivots: list[str] = []
    for sequence, shard in enumerate(shards, 1):
        require(isinstance(shard, dict) and shard.get("schema", "").endswith("/shard") and
                shard.get("sequence") == sequence and shard.get("previous") == previous and
                shard.get("candidate_count") == 64 and isinstance(shard.get("entries"), list),
                "shard:order")
        claimed = shard.get("self_digest_sha256"); body = dict(shard); body.pop("self_digest_sha256", None)
        require(claimed == digest(body), "shard:seal")
        chain = sha((str(previous) + digest({k: v for k, v in body.items() if k != "chain"})).encode("ascii"))
        require(shard.get("chain") == chain and shard.get("batch_offsets") == [0, len(shard["entries"])],
                "shard:chain_offsets")
        query = shard.get("query"); require(isinstance(query, dict), "shard:query")
        require(query.get("query_id") == "R:" + str(query.get("next_row")) and
                query.get("target_digest") == digest(query.get("target")) and
                query.get("word_digest") == digest(query.get("source_word")) and
                query.get("bridge_digest") == digest(query.get("bridge")), "shard:pending_binding")
        for entry in shard["entries"]:
            require(isinstance(entry, dict) and entry.get("kind") == "B", "shard:entry")
            raw = entry.get("raw_identity"); require(isinstance(raw, dict), "shard:raw_identity")
            raw_row = _a4_checker_row(raw.get("row")); require(entry.get("raw_digest") == digest(raw_row), "shard:raw_drift")
            for side in ("boundary", "combined"):
                detail = entry.get(side); require(isinstance(detail, dict), "shard:detail")
                row = _a4_checker_row(detail.get("row")); pivot = detail.get("pivot")
                require(isinstance(pivot, str) and row.get(pivot) == 1 and pivot not in pivots and
                        detail.get("row_digest") == digest(row) and
                        detail.get("label_digest") == digest(detail.get("label")), "shard:physical_row")
            formals = entry.get("formals"); event = entry.get("event")
            require(isinstance(formals, dict) and all(isinstance(formals.get(k), dict) for k in
                    ("boundary_reduction", "combined_reduction", "b_coefficients", "b_formals")) and
                    isinstance(event, dict) and isinstance(entry.get("epoch_before"), str) and
                    isinstance(entry.get("epoch_after"), str), "shard:formal_event")
            pivots.append(entry["combined"]["pivot"])
        previous = claimed
    require(head.get("sequence") == len(shards) and head.get("last_shard_sha256") == previous and
            head.get("chain") == chain and head.get("next_row") == (open_query or {}).get("next_row", head.get("next_row")),
            "shard:head_ahead")
    if open_query is not None:
        require(open_query.get("query_id") not in {r.get("query_id") for r in completed_records} and
                open_query.get("query_id") not in {e.get("query_id") for e in completed_events} and
                open_query.get("row_cursor") == open_query.get("next_row") - 1 and
                open_query.get("bridge_cursor") == open_query.get("next_row") - 1 and
                open_query.get("target_digest") == digest(open_query.get("target")) and
                open_query.get("word_digest") == digest(open_query.get("source_word")) and
                open_query.get("bridge_digest") == digest(open_query.get("bridge")), "shard:open_query")
    return {"shards": len(shards), "physical_entries": len(pivots), "open_query": open_query is not None}
'''.replace(b"\\\n", b"")

PATCHES = ((_ANCHOR, _CHECKER_HELPER + _ANCHOR),)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v32 checker: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v32 checker: frozen v31 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v31_owner", "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v32 checker: frozen v31 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v32 checker: resulting generated source drift")
    return raw


def self_test() -> None:
    raw = restore_frozen(); ns: dict[str, Any] = {"__name__": "_r07_a4_v32_test",
        "__file__": str(Path(__file__).resolve()), "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)
    digest = ns["digest"]; checker = ns["_a4_checker_validate_shards"]
    entries = []
    for i in range(3):
        row = {"k:%d" % i: 1}; label = "B:%d" % i
        detail = {"pivot": "k:%d" % i, "row": row, "label": label,
                  "row_digest": digest(row), "label_digest": digest(label)}
        entries.append({"kind": "B", "raw_identity": {"row": row}, "raw_digest": digest(row),
            "boundary": detail, "combined": detail,
            "formals": {"boundary_reduction": {}, "combined_reduction": {}, "b_coefficients": {}, "b_formals": {}},
            "event": {"query_id": "R:27"}, "epoch_before": "e:%d" % i, "epoch_after": "e:%d" % (i + 1)})
    query = {"query_id": "R:27", "next_row": 27, "row_cursor": 26, "bridge_cursor": 26,
             "target": {"t": 1}, "source_word": [1], "bridge": {"trace": 1}}
    query.update({"target_digest": digest(query["target"]), "word_digest": digest(query["source_word"]),
                  "bridge_digest": digest(query["bridge"])})
    body = {"schema": "d972-r07-word-independent-successor-kernel/v425/shard", "sequence": 1,
            "previous": None, "query": query, "candidate_count": 64, "entries": entries,
            "batch_offsets": [0, 3], "epoch_before": "e:0", "epoch_after": "e:3"}
    body["chain"] = ns["sha"](("None" + digest(body)).encode("ascii")); body["self_digest_sha256"] = digest(body)
    head = {"schema": "d972-r07-word-independent-successor-kernel/v425/head", "sequence": 1,
            "next_row": 27, "last_shard_sha256": body["self_digest_sha256"], "chain": body["chain"]}
    head["self_digest_sha256"] = digest(head)
    completed = [{"query_id": "R:1"}]; events = [{"query_id": "R:1"}]
    checker(head, [body], query, completed, events)
    for name, mutation in (("head_ahead", lambda h, s: h.update({"sequence": 2})),
                           ("unsealed_shard", lambda h, s: s[0].pop("self_digest_sha256")),
                           ("raw_identity_drift", lambda h, s: s[0]["entries"][0].update({"raw_digest": "0" * 64})),
                           ("physical_pivot_drift", lambda h, s: s[0]["entries"][0]["combined"].update({"pivot": "k:99"})),
                           ("formal_ledger_drift", lambda h, s: s[0]["entries"][0]["formals"].update({"b_formals": {"B:99": {}}})),
                           ("pending_target_drift", lambda h, s: s[0]["query"].update({"target": {"t": 2}})),
                           ("open_query_prefix", lambda h, s: completed.append({"query_id": "R:27"})),
                           ("open_terminal_duplicate", lambda h, s: events.append({"query_id": "R:27"}))):
        h = dict(head); s = [dict(body)]; s[0]["entries"] = [dict(e) for e in body["entries"]]
        mutation(h, s)
        try: checker(h, s, query, completed, events)
        except Exception: pass
        else: raise AssertionError(name + " accepted")
    print("R07_A4_PHYSICAL_SHARD_V32_SELFTEST_PASS batches=1 physical_entries=3 mutations=8 head_ahead=REJECT raw_identity_drift=REJECT terminal_duplicate=REJECT")


def main() -> None:
    if sys.argv[1:] == ["--self-test"]:
        self_test(); return
    raw = restore_frozen(); ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
                                 "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
