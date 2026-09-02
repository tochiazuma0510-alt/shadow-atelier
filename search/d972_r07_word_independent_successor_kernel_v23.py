#!/usr/bin/env python3
"""A4 v23 producer: v22 mathematics plus intra-query physical shards."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v22.py")
OWNER_BYTES = 4055
OWNER_SHA256 = "0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2"
OWNER_GENERATED_BYTES = 256509
OWNER_GENERATED_SHA256 = "20fdeb66f70f428152e06f5e7a92b455dd211bd0e72d665c10d24d2ad0491e94"
RESULT_GENERATED_BYTES = 266117
RESULT_GENERATED_SHA256 = "d406f1128dc66bc526fe5babf0f9fee0b086d7fce348f1435a7516d8090b9ef6"

_ANCHOR = b"def _delta_payload(authority: AuthorityAdapter, meter: Meter, next_row: int,\n"

_SHARD_HELPER = b'''\
\ndef _a4_physical_digest(value: Any) -> str:
    return digest(value)


def _a4_normal_row(value: Any) -> dict[str, int]:
    require(isinstance(value, dict) and all(isinstance(k, str) and
             isinstance(v, int) and not isinstance(v, bool) and v % 3 for k, v in value.items()),
            "shard:row_shape")
    out = {k: int(v) % 3 for k, v in value.items() if int(v) % 3}
    require(all(v in (1, 2) for v in out.values()), "shard:row_coefficients")
    return out


def _a4_physical_entry(raw_identity: dict[str, Any], boundary: dict[str, Any],
                       combined: dict[str, Any], formals: dict[str, Any],
                       event: dict[str, Any], epoch_before: str, epoch_after: str) -> dict[str, Any]:
    require(isinstance(raw_identity, dict) and isinstance(raw_identity.get("row"), dict),
            "shard:raw_identity")
    raw_row = _a4_normal_row(raw_identity["row"])
    require(isinstance(boundary, dict) and isinstance(combined, dict) and
            isinstance(formals, dict) and isinstance(event, dict), "shard:entry_shape")
    entry = {"kind": "B", "raw_identity": dict(raw_identity),
             "raw_digest": digest(raw_row), "boundary": dict(boundary),
             "combined": dict(combined), "formals": dict(formals),
             "event": dict(event), "epoch_before": epoch_before, "epoch_after": epoch_after}
    require(entry["raw_digest"] == digest(raw_row), "shard:raw_digest")
    return entry


def _a4_validate_physical_entry(entry: dict[str, Any], prior_pivots: list[str]) -> None:
    require(isinstance(entry, dict) and entry.get("kind") == "B", "shard:entry")
    raw_identity = entry.get("raw_identity")
    require(isinstance(raw_identity, dict), "shard:raw_identity")
    raw_row = _a4_normal_row(raw_identity.get("row"))
    require(entry.get("raw_digest") == digest(raw_row), "shard:raw_identity_digest")
    for side in ("boundary", "combined"):
        detail = entry.get(side)
        require(isinstance(detail, dict) and isinstance(detail.get("pivot"), str) and
                isinstance(detail.get("row"), dict) and isinstance(detail.get("label"), str),
                "shard:" + side + "_detail")
        row = _a4_normal_row(detail["row"])
        require(row.get(detail["pivot"]) == 1 and
                all(pivot not in row for pivot in prior_pivots),
                "shard:" + side + "_chronology")
        require(detail.get("row_digest") == digest(row) and
                detail.get("label_digest") == digest(detail["label"]),
                "shard:" + side + "_digest")
    require(isinstance(entry.get("formals"), dict) and isinstance(entry.get("event"), dict) and
            isinstance(entry.get("epoch_before"), str) and isinstance(entry.get("epoch_after"), str),
            "shard:formal_event")


def _a4_direct_load_echelons(shards: list[dict[str, Any]]) -> dict[str, Any]:
    """Restore physical maps directly; no insertion/reduction is called."""
    boundary: dict[str, dict[str, int]] = {}; combined: dict[str, dict[str, int]] = {}
    formals: dict[str, Any] = {}; events: list[dict[str, Any]] = []
    for shard in shards:
        for entry in shard["entries"]:
            boundary[entry["boundary"]["pivot"]] = dict(entry["boundary"]["row"])
            combined[entry["combined"]["pivot"]] = dict(entry["combined"]["row"])
            formals[entry["combined"]["label"]] = dict(entry["formals"])
            events.append(dict(entry["event"]))
    return {"boundary": boundary, "combined": combined, "formals": formals, "events": events}


class _A4PhysicalShardStore:
    """Closed 64-candidate shard chain plus one sealed pending query."""
    def __init__(self, next_row: int = 27, root: Path | None = None):
        self.next_row = int(next_row); self.row_cursor = self.next_row - 1
        self.bridge_cursor = self.row_cursor; self.open_query = None
        self.root = root
        self.shards: list[dict[str, Any]] = []; self.head = {"sequence": 0, "next_row": self.next_row,
            "last_shard_sha256": None, "chain": "0" * 64}; self.terminal = None

    def prepare(self, source_word: list[int], target: dict[str, int], bridge: dict[str, Any],
                row_digest: str, sample: Any = None) -> dict[str, Any]:
        query_id = "R:" + str(self.next_row)
        require(self.open_query is None and self.row_cursor == self.next_row - 1 and
                self.bridge_cursor == self.next_row - 1, "query:prepare_cursor")
        self.open_query = {"query_id": query_id, "next_row": self.next_row,
                           "row_cursor": self.row_cursor, "bridge_cursor": self.bridge_cursor,
                           "source_word": list(source_word), "target": dict(target),
                           "target_digest": digest(target), "word_digest": digest(list(source_word)),
                           "bridge": dict(bridge), "bridge_digest": digest(bridge),
                           "row_digest": str(row_digest), "sample": sample}
        self.open_query["self_digest_sha256"] = digest(self.open_query)
        return dict(self.open_query)

    def close_batch(self, examined: list[dict[str, Any]]) -> dict[str, Any]:
        require(self.open_query is not None and len(examined) == 64, "shard:batch_size")
        prior = self.shards[-1]["self_digest_sha256"] if self.shards else None
        entries = list(examined); prior_pivots = [p for shard in self.shards
                                                   for entry in shard["entries"]
                                                   for p in [entry["combined"]["pivot"]]]
        for entry in entries:
            _a4_validate_physical_entry(entry, prior_pivots)
            prior_pivots.append(entry["combined"]["pivot"])
        sequence = len(self.shards) + 1
        body = {"schema": "d972-r07-word-independent-successor-kernel/v425/shard",
                "sequence": sequence, "previous": prior, "query": dict(self.open_query),
                "candidate_count": 64, "entries": entries,
                "batch_offsets": [0, len(entries)], "epoch_before": entries[0]["epoch_before"] if entries else self.open_query["query_id"],
                "epoch_after": entries[-1]["epoch_after"] if entries else self.open_query["query_id"]}
        body["chain"] = sha((str(prior) + digest(body)).encode("ascii"))
        body["self_digest_sha256"] = digest(body); self.shards.append(body)
        self.head = {"schema": "d972-r07-word-independent-successor-kernel/v425/head",
                     "sequence": sequence, "next_row": self.next_row,
                     "last_shard_sha256": body["self_digest_sha256"], "chain": body["chain"]}
        self.head["self_digest_sha256"] = digest(self.head)
        if self.root is not None:
            self.root.mkdir(parents=True, exist_ok=True)
            write_atomic(self.root / ("shard.%08d.json" % sequence), canon(body))
            write_atomic(self.root / "HEAD", canon(self.head))
        return body

    def query(self, candidates: list[dict[str, Any]], stop_after_batches: int | None = None) -> None:
        require(self.open_query is not None and len(candidates) % 64 == 0, "query:candidate_batches")
        for offset in range(0, len(candidates), 64):
            self.close_batch(candidates[offset:offset + 64])
            if stop_after_batches is not None and len(self.shards) >= stop_after_batches: return

    def commit(self, terminal: dict[str, Any]) -> dict[str, Any]:
        require(self.open_query is not None and self.terminal is None and
                terminal.get("query_id") == self.open_query["query_id"], "query:commit")
        self.terminal = dict(terminal); self.terminal["self_digest_sha256"] = digest(self.terminal)
        self.next_row += 1; self.row_cursor += 1; self.bridge_cursor += 1
        self.open_query = None; self.head["obsolete"] = True
        return dict(self.terminal)

    def export(self) -> dict[str, Any]:
        return {"next_row": self.next_row, "row_cursor": self.row_cursor,
                "bridge_cursor": self.bridge_cursor, "open_query": self.open_query,
                "shards": self.shards, "head": self.head, "terminal": self.terminal}

    @classmethod
    def restore(cls, payload: dict[str, Any]) -> "_A4PhysicalShardStore":
        out = cls(int(payload["next_row"])); out.row_cursor = int(payload["row_cursor"])
        out.bridge_cursor = int(payload["bridge_cursor"]); out.open_query = payload.get("open_query")
        out.shards = list(payload.get("shards", [])); out.head = dict(payload["head"])
        out.terminal = payload.get("terminal")
        previous = None; prior_pivots: list[str] = []
        for sequence, shard in enumerate(out.shards, 1):
            sealed = shard.get("self_digest_sha256"); body = dict(shard); body.pop("self_digest_sha256", None)
            require(sealed == digest(body) and shard.get("sequence") == sequence and
                    shard.get("previous") == previous and shard.get("candidate_count") == 64,
                    "resume:shard_order")
            require(shard.get("chain") == sha((str(previous) + digest({k: v for k, v in body.items()
                         if k != "chain"})).encode("ascii")), "resume:shard_chain")
            for entry in shard["entries"]:
                _a4_validate_physical_entry(entry, prior_pivots); prior_pivots.append(entry["combined"]["pivot"])
            previous = sealed
        require(out.head.get("sequence") == len(out.shards) and
                out.head.get("last_shard_sha256") == previous, "resume:head_ahead")
        out.loaded = _a4_direct_load_echelons(out.shards)
        return out
'''.replace(b"\\\n", b"")

PATCHES = ((_ANCHOR, _SHARD_HELPER + _ANCHOR),)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v23 producer: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v23 producer: frozen v22 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v22_owner", "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v23 producer: frozen v22 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v23 producer: resulting generated source drift")
    return raw


def self_test() -> None:
    raw = restore_frozen(); ns: dict[str, Any] = {"__name__": "_r07_a4_v23_test",
        "__file__": str(Path(__file__).resolve()), "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)
    Store = ns["_A4PhysicalShardStore"]
    def entry(index: int) -> dict[str, Any]:
        row = {"k:%d" % index: 1}; label = "B:%d" % index
        detail = {"pivot": "k:%d" % index, "row": row, "label": label,
                  "row_digest": ns["digest"](row), "label_digest": ns["digest"](label)}
        raw_identity = {"row": row, "source_word": [index], "target": "t:%d" % index}
        return ns["_a4_physical_entry"](raw_identity, detail, detail,
            {"boundary_reduction": {}, "combined_reduction": {}, "b_coefficients": {}, "b_formals": {}},
            {"schema": "BOUNDARY_RANK_RISE", "query_id": "R:27", "index": index},
            "e:%d" % index, "e:%d" % (index + 1))
    candidates = [entry(i) for i in range(192)]
    uninterrupted = Store(); uninterrupted.prepare([1, 2], {"x": 1}, {"trace": "b"}, "row")
    uninterrupted.query(candidates); uninterrupted.commit({"query_id": "R:27", "schema": "MEMBER"})
    interrupted = Store(); interrupted.prepare([1, 2], {"x": 1}, {"trace": "b"}, "row")
    interrupted.query(candidates, stop_after_batches=3)
    restored = Store.restore(interrupted.export()); restored.query(candidates[192:], stop_after_batches=None)
    restored.commit({"query_id": "R:27", "schema": "MEMBER"})
    assert uninterrupted.export() == restored.export(), "selftest:interrupt_equality"
    assert len(restored.shards) == 3 and restored.open_query is None and len(restored.loaded["combined"]) == 192
    broken = uninterrupted.export(); broken["head"] = dict(broken["head"], sequence=4)
    try: Store.restore(broken)
    except Exception: pass
    else: raise AssertionError("head-ahead accepted")
    broken = uninterrupted.export(); broken["shards"] = list(broken["shards"]); broken["shards"][0] = dict(broken["shards"][0]);
    broken["shards"][0]["entries"] = list(broken["shards"][0]["entries"]); broken["shards"][0]["entries"][0] = dict(broken["shards"][0]["entries"][0], raw_digest="0" * 64)
    try: Store.restore(broken)
    except Exception: pass
    else: raise AssertionError("raw-identity drift accepted")
    print("R07_A4_PHYSICAL_SHARD_V23_SELFTEST_PASS batches=3 candidates=192 interruption=PASS head_ahead=REJECT raw_identity_drift=REJECT")


def main() -> None:
    if sys.argv[1:] == ["--self-test"]:
        self_test(); return
    raw = restore_frozen(); ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
                                 "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
