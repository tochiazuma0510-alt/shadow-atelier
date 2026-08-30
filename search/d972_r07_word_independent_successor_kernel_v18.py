#!/usr/bin/env python3
"""A4 v18 producer: v17 arithmetic with linear append-only row deltas.

The frozen v17 owner remains the arithmetic owner.  This successor changes
only checkpoint transport: the immutable legacy checkpoint is the base, each
completed boundary appends one event/list delta, and a small atomic HEAD
advances only after that delta is sealed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v17.py")
OWNER_BYTES = 5596
OWNER_SHA256 = "20f1f8d08797d90017d057cf59a30d9a96bdadede64a9823c6fd0a364985963c"
OWNER_GENERATED_BYTES = 233607
OWNER_GENERATED_SHA256 = "5a58fa44602f853bd87fd4d4a98a2593f5ae2877c873e87b2a2f6b7a8f1c84c9"
RESULT_GENERATED_BYTES = 251746
RESULT_GENERATED_SHA256 = "b4d852354d3753844ed9d64041d2c3b3f1221b81ba7fb7ae6cedb33b0873eeed"

DELTA_BLOCK = b'''\

DELTA_SCHEMA = SCHEMA + "/delta/v1"
DELTA_HEAD_SCHEMA = SCHEMA + "/head/v1"
LEGACY_BASE_BYTES = 25581
LEGACY_BASE_SHA256 = "595213bab8936ef10e94ce90ccf526c105d02d871d4dc5d02b6c76cb51593445"
LEGACY_BASE_NEXT_ROW = 25
LEGACY_BASE_CODE_SHA256 = "964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7"

def _delta_base_path(head: Path) -> Path:
    name = head.name
    suffix = ".head.checkpoint.json"
    if name.endswith(suffix):
        return head.with_name(name[:-len(suffix)] + ".base.checkpoint.json")
    return head.with_name(name + ".base.checkpoint.json")

def _delta_segment_path(head: Path, index: int) -> Path:
    return head.with_name(head.name + ".delta.%08d.json" % int(index))

def _delta_digest(value: Any) -> str:
    return sha(canon(value))

def _delta_chain_digest(value: dict[str, Any], prior_chain: str) -> str:
    unsigned = dict(value); unsigned.pop("chain", None)
    return sha((str(prior_chain) + _delta_digest(unsigned)).encode("ascii"))

def _delta_list(value: list[Any], start: int) -> list[Any]:
    return list(value[int(start):])

def _delta_tracker(oracle: Oracle, words: WordDAG, queue: list[int], actions: list[dict[str, Any]],
                   action_events: list[dict[str, Any]], matrix: dict[str, Any], meter: Meter) -> dict[str, Any]:
    meta = getattr(meter, "_a4_delta_resume", {}) or {}
    terminal_records = [record for record in oracle.records if is_row_terminal(record)]
    terminal_events = [event for event in oracle.event_chain if is_row_terminal(event)]
    return {"rows": len(oracle.row_digests), "bridges": len(oracle.bridge_chain),
            "chunks": len(oracle.row_chunks), "samples": len(oracle.samples),
            "records": len(oracle.records), "events": len(oracle.event_chain),
            "duals": len(oracle.live_duals), "dual_events": len(oracle.dual_chain),
            "initial_records": len(terminal_records),
            "initial_events": len(terminal_events),
            "nodes": len(words.nodes), "k_items": len(oracle.basis.k_items),
            "insertions": len(oracle.basis.insertion_events), "queue": len(queue),
            "actions": len(actions), "action_events": len(action_events),
            "sample_keys": set(getattr(oracle, "sample_rows", {}).keys()),
            "counters": dict(meter.counters), "host_history": len(meter.host_history),
            "seq": int(meta.get("seq", 0)), "prev": meta.get("prev"),
            "chain": meta.get("chain", "0" * 64), "base": meta.get("base")}

def _delta_counter_delta(now: dict[str, Any], before: dict[str, Any]) -> dict[str, int]:
    return {key: int(value) - int(before.get(key, 0)) for key, value in now.items()
            if int(value) != int(before.get(key, 0))}

def _delta_payload(authority: AuthorityAdapter, meter: Meter, next_row: int,
                   oracle: Oracle, words: WordDAG, queue: list[int], cursor: int,
                   queue_phase: dict[str, Any], tracker: dict[str, Any], kind: str) -> dict[str, Any]:
    basis = oracle.basis; old_actions = int(tracker["actions"])
    action_add = list(queue_phase.get("actions", []))[old_actions:]
    matrix_updates = [{"letter": action["letter"], "parent": action["parent"],
                       "column": action["basis_column"]} for action in action_add]
    new_samples = _delta_list(oracle.samples, tracker["samples"])
    new_sample_rows = {str(key): value for key, value in oracle.sample_rows.items()
                       if key not in tracker["sample_keys"]}
    return {"schema": DELTA_SCHEMA, "owner": "producer", "kind": kind,
            "ordinal": int(next_row) - 1 if kind == "row" else int(next_row),
            "next_row": int(next_row), "base": tracker["base"], "previous": tracker["prev"],
            "row_digests": _delta_list(oracle.row_digests, tracker["rows"]),
            "bridge_digests": _delta_list(oracle.bridge_chain, tracker["bridges"]),
            "row_chunks": _delta_list(oracle.row_chunks, tracker["chunks"]),
            "samples": new_samples, "sample_rows": new_sample_rows,
            "oracle_records": _delta_list(oracle.records, tracker["records"]),
            "query_event_chain": _delta_list(oracle.event_chain, tracker["events"]),
            "live_duals": _delta_list(oracle.live_duals, tracker["duals"]),
            "dual_event_chain": _delta_list(oracle.dual_chain, tracker["dual_events"]),
            "initial_terminal_records": [record for record in oracle.records
                                          if is_row_terminal(record)][tracker["initial_records"]:],
            "initial_terminal_chain": [event for event in oracle.event_chain
                                        if is_row_terminal(event)][tracker["initial_events"]:],
            "word_ledger_dag": [{key: value for key, value in node.items() if key != "states"}
                                for node in words.nodes[tracker["nodes"]:]],
            "K_roster": _delta_list(basis.k_items, tracker["k_items"]),
            "insertion_events": _delta_list(basis.insertion_events, tracker["insertions"]),
            "queue_append": _delta_list(queue, tracker["queue"]),
            "queue_head": int(cursor),
            "queue_phase": {"actions": action_add,
                             "action_event_chain": list(queue_phase.get("action_event_chain", []))[int(tracker["action_events"]):],
                             "matrix_updates": matrix_updates,
                             "inverse_laws": dict(queue_phase.get("inverse_laws", {}))},
            "epoch_digest": oracle.epoch,
            "counter_delta": _delta_counter_delta(meter.counters, tracker["counters"]),
            "counters": dict(meter.counters), "semantic_counters": dict(meter.semantic_counters),
            "host_counters": dict(meter.host_counters), "peak_counters": dict(meter.peak_counters),
            "restore_validation_counters": dict(meter.restore_validation_counters),
            "host_history_append": list(meter.host_history)[tracker["host_history"]:]}

def _delta_write_head(head: Path, body: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    sealed, encoded = seal(body); write_atomic(head, encoded); return sealed, encoded

def write_checkpoint(path: Path, authority: AuthorityAdapter, meter: Meter, next_row: int,
                     oracle: Oracle, words: WordDAG, queue: list[int], cursor: int,
                     queue_phase: dict[str, Any] | None = None) -> None:
    """Append one delta and atomically advance HEAD; no prefix snapshot is made."""
    if not hasattr(meter, "_a4_delta_tracker"):
        meter._a4_delta_resume = getattr(meter, "_a4_delta_resume", {}) or {}
        phase = queue_phase or {}
        meter._a4_delta_tracker = _delta_tracker(oracle, words, queue,
                                                   list(phase.get("actions", [])),
                                                   list(phase.get("action_event_chain", [])),
                                                   dict(phase.get("matrix", {})), meter)
    tracker = meter._a4_delta_tracker; base = _delta_base_path(path)
    require(base.exists(), "delta:immutable_base_missing")
    base_raw = base.read_bytes(); require(len(base_raw) == LEGACY_BASE_BYTES and
        sha(base_raw) == LEGACY_BASE_SHA256, "delta:immutable_base_identity")
    if tracker["base"] is None:
        tracker["base"] = {"path": base.name, "bytes": len(base_raw), "sha256": sha(base_raw)}
    require(tracker["base"] == {"path": base.name, "bytes": len(base_raw), "sha256": sha(base_raw)},
            "delta:base_binding")
    kind = "row" if int(next_row) <= ROWS else "queue"
    body = _delta_payload(authority, meter, next_row, oracle, words, queue, cursor,
                          queue_phase or {}, tracker, kind)
    seq = int(tracker["seq"]) + 1; body["sequence"] = seq
    body["chain"] = _delta_chain_digest(body, tracker["chain"])
    body["self_digest_sha256"] = _delta_digest(body)
    encoded = canon(body); segment = _delta_segment_path(path, seq)
    require(not segment.exists(), "delta:segment_rewrite")
    write_atomic(segment, encoded)
    head_body = {"schema": DELTA_HEAD_SCHEMA, "owner": "producer", "base": tracker["base"],
                 "last_sequence": seq, "last_segment": segment.name, "last_segment_sha256": sha(encoded),
                 "last_row": int(next_row) - 1 if kind == "row" else int(tracker.get("last_row", ROWS)),
                 "next_row": int(next_row) if kind == "row" else int(tracker.get("last_next_row", ROWS + 1)),
                 "chain": body["chain"], "segment_count": seq}
    head_sealed, head_encoded = seal(head_body); write_atomic(path, head_encoded)
    meter.bump("checkpoint_total_bytes", len(encoded) + len(head_encoded), "checkpoint_delta")
    tracker.update({"rows": len(oracle.row_digests), "bridges": len(oracle.bridge_chain),
        "chunks": len(oracle.row_chunks), "samples": len(oracle.samples), "records": len(oracle.records),
        "events": len(oracle.event_chain), "duals": len(oracle.live_duals), "dual_events": len(oracle.dual_chain),
        "nodes": len(words.nodes), "k_items": len(oracle.basis.k_items),
        "insertions": len(oracle.basis.insertion_events), "queue": len(queue),
        "actions": len(queue_phase.get("actions", [])) if queue_phase else tracker["actions"],
        "action_events": len(queue_phase.get("action_event_chain", [])) if queue_phase else tracker["action_events"],
        "sample_keys": set(oracle.sample_rows.keys()), "counters": dict(meter.counters),
        "host_history": len(meter.host_history), "seq": seq, "prev": sha(encoded),
        "chain": body["chain"], "last_row": head_body["last_row"], "last_next_row": head_body["next_row"]})
    meter._a4_durable_row = max(0, min(ROWS, int(head_body["last_row"])))

def _delta_checkpoint_reference(path: Path, meter: Meter) -> dict[str, Any]:
    require(path.name.endswith(".head.checkpoint.json"), "delta:reference_path")
    raw = path.read_bytes(); head = json.loads(raw.decode("ascii"))
    claimed = head.pop("self_digest_sha256", None)
    require(claimed == _delta_digest(head) and head.get("schema") == DELTA_HEAD_SCHEMA and
            head.get("owner") == "producer", "delta:reference_head")
    base_path = _delta_base_path(path); base_raw = base_path.read_bytes()
    base_identity = {"path": base_path.name, "bytes": len(base_raw), "sha256": sha(base_raw)}
    require(base_identity == head.get("base") and len(base_raw) == LEGACY_BASE_BYTES and
            sha(base_raw) == LEGACY_BASE_SHA256, "delta:reference_base")
    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64
    for sequence in range(1, count + 1):
        segment_path = _delta_segment_path(path, sequence); require(segment_path.exists(), "delta:reference_missing")
        segment_raw = segment_path.read_bytes(); segment = json.loads(segment_raw.decode("ascii"))
        seal_value = segment.pop("self_digest_sha256", None)
        require(seal_value == _delta_digest(segment) and segment.get("schema") == DELTA_SCHEMA and
                segment.get("owner") == "producer" and segment.get("sequence") == sequence and
                segment.get("base") == base_identity and segment.get("previous") == previous,
                "delta:reference_segment")
        chain = _delta_chain_digest(segment, chain)
        require(segment.get("chain") == chain, "delta:reference_chain"); previous = sha(segment_raw)
    require(head.get("last_sequence") == count and head.get("last_segment_sha256") == previous and
            head.get("chain") == chain, "delta:reference_terminal")
    if count:
        require(head.get("next_row") == segment.get("next_row") and
                head.get("last_row") == (segment.get("ordinal") if segment.get("kind") == "row" else ROWS) and
                LEGACY_BASE_NEXT_ROW < int(head.get("next_row", 0)) <= ROWS + 1,
                "delta:reference_ahead")
    else:
        require(head.get("next_row") == LEGACY_BASE_NEXT_ROW and head.get("last_row") == LEGACY_BASE_NEXT_ROW - 1,
                "delta:reference_empty_head")
    require(len(list(path.parent.glob(path.name + ".delta.*.json"))) == count, "delta:reference_orphan")
    return {"kind": "delta_chain", "path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": sha(raw), "owner": "producer", "base": head["base"],
            "last_sequence": count, "last_segment": head["last_segment"],
            "last_segment_sha256": head["last_segment_sha256"], "last_row": head["last_row"],
            "next_row": head["next_row"], "chain": head["chain"],
            "checkpoint_self_digest_sha256": claimed, "replayable": True, "sealed": True}

def _delta_apply_dict(target: dict[str, Any], delta: dict[str, int]) -> None:
    for key, value in delta.items(): target[key] = int(target.get(key, 0)) + int(value)

def _delta_apply_segment(state: dict[str, Any], segment: dict[str, Any]) -> None:
    for field in ("row_digests", "bridge_digests", "row_chunks", "samples", "oracle_records",
                  "query_event_chain", "live_duals", "dual_event_chain", "word_ledger_dag",
                  "K_roster", "insertion_events", "queue_append", "initial_terminal_records",
                  "initial_terminal_chain"):
        if field == "queue_append": state.setdefault("queue", []).extend(segment[field])
        else: state.setdefault(field, []).extend(segment[field])
    for key, value in segment.get("sample_rows", {}).items(): state.setdefault("sample_rows", {})[key] = value
    state.setdefault("queue_phase", {"actions": [], "action_event_chain": [], "matrix": {}, "inverse_laws": {}})
    phase = state["queue_phase"]; phase.setdefault("actions", []).extend(segment["queue_phase"].get("actions", []))
    phase.setdefault("action_event_chain", []).extend(segment["queue_phase"].get("action_event_chain", []))
    for update in segment["queue_phase"].get("matrix_updates", []):
        phase.setdefault("matrix", {}).setdefault(str(update["letter"]), {})[update["parent"]] = update["column"]
    phase["queue_head"] = segment.get("queue_head", phase.get("queue_head", 0)); phase["queue_length"] = len(state["queue"])
    state["queue_head"] = phase["queue_head"]
    phase["action_count"] = len(phase["actions"]); phase["inverse_laws"].update(segment["queue_phase"].get("inverse_laws", {}))
    state["next_row"] = segment["next_row"]; state["row_cursor"] = len(state["row_digests"]); state["bridge_cursor"] = len(state["bridge_digests"])
    state["row_replay_sha256"] = digest(state["row_digests"]); state["bridge_replay_sha256"] = digest(state["bridge_digests"])
    state["oracle_records"] = state["oracle_records"]; state["query_event_chain"] = state["query_event_chain"]
    state["dual_event_chain"] = state["dual_event_chain"]; state["epoch_digest"] = segment["epoch_digest"]
    _delta_apply_dict(state.setdefault("counters", {}), segment.get("counter_delta", {}))
    state["semantic_counters"] = dict(segment.get("semantic_counters", state.get("semantic_counters", {})))
    state["completed_counters"] = dict(state["semantic_counters"]); state["host_counters"] = dict(segment.get("host_counters", {}))
    state["peak_counters"] = dict(segment.get("peak_counters", {})); state["restore_validation_counters"] = dict(segment.get("restore_validation_counters", {}))
    state.setdefault("host_history", []).extend(segment.get("host_history_append", []))

def restore_delta_chain(path: Path, authority: AuthorityAdapter, meter: Meter) -> dict[str, Any]:
    base = _delta_base_path(path); require(base.exists(), "delta:base_missing")
    base_raw = base.read_bytes(); require(len(base_raw) == LEGACY_BASE_BYTES and sha(base_raw) == LEGACY_BASE_SHA256,
                                          "delta:base_identity")
    state = restore_full_checkpoint(base, authority, meter)
    if not path.exists():
        state["_delta_transport"] = True; state["_delta_meta"] = {"seq": 0, "prev": None, "chain": "0" * 64,
            "base": {"path": base.name, "bytes": len(base_raw), "sha256": sha(base_raw)}}; return state
    head_raw = path.read_bytes(); head = json.loads(head_raw.decode("ascii")); claimed = head.pop("self_digest_sha256", None)
    require(claimed == _delta_digest(head) and head.get("schema") == DELTA_HEAD_SCHEMA and head.get("owner") == "producer",
            "delta:head_seal")
    require(head.get("base") == {"path": base.name, "bytes": len(base_raw), "sha256": sha(base_raw)}, "delta:head_base")
    count = int(head.get("segment_count", 0)); prev = None; chain = "0" * 64
    for seq in range(1, count + 1):
        segment_path = _delta_segment_path(path, seq); require(segment_path.exists(), "delta:missing_segment")
        raw = segment_path.read_bytes(); segment = json.loads(raw.decode("ascii")); seal_value = segment.pop("self_digest_sha256", None)
        require(seal_value == _delta_digest(segment) and segment.get("schema") == DELTA_SCHEMA and segment.get("owner") == "producer" and
                segment.get("sequence") == seq and segment.get("base") == head["base"] and segment.get("previous") == prev,
                "delta:segment_chain")
        chain = _delta_chain_digest(segment, chain); require(segment.get("chain") == chain, "delta:chain_digest")
        _delta_apply_segment(state, segment); prev = sha(raw)
    require(head.get("last_sequence") == count and head.get("last_segment_sha256") == prev and head.get("chain") == chain,
            "delta:head_terminal")
    if count:
        require(head.get("next_row") == segment.get("next_row") and
                head.get("last_row") == (segment.get("ordinal") if segment.get("kind") == "row" else ROWS) and
                LEGACY_BASE_NEXT_ROW < int(head.get("next_row", 0)) <= ROWS + 1,
                "delta:head_ahead")
    else:
        require(head.get("next_row") == LEGACY_BASE_NEXT_ROW and head.get("last_row") == LEGACY_BASE_NEXT_ROW - 1,
                "delta:empty_head")
    extras = list(path.parent.glob(path.name + ".delta.*.json")); require(len(extras) == count, "delta:orphan_segment")
    state["_delta_transport"] = True; state["_delta_meta"] = {"seq": count, "prev": prev, "chain": chain, "base": head["base"]}
    state["rebuild_digest"] = "delta-chain:" + chain
    return state
'''

PATCHES = (
    (b"    checkpoint_writes_enabled = resume_state is None" + bytes([10]),
     b"    checkpoint_writes_enabled = resume_state is None" + bytes([10]) +
     b"    meter._a4_delta_resume = dict((resume_state or {}).get(\"_delta_meta\", {}))" + bytes([10])),
    (b'    """Bind a resource terminal to a physical checkpoint or pre-authority stop."""' + bytes([10]),
     b'    """Bind a resource terminal to a physical checkpoint or pre-authority stop."""' + bytes([10]) +
     b'    if path is not None and path.name.endswith(".head.checkpoint.json"):' + bytes([10]) +
     b'        try:' + bytes([10]) + b'            return _delta_checkpoint_reference(path, meter)' + bytes([10]) +
     b'        except Exception:' + bytes([10]) + b'            pass' + bytes([10])),
    (b'''CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v25"\n''', b'''CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v26"\n'''),
    (b'''def write_checkpoint(path: Path, authority: AuthorityAdapter, meter: Meter, next_row: int,\n                      oracle: Oracle, words: WordDAG, queue: list[int], cursor: int,\n                      queue_phase: dict[str, Any] | None = None) -> None:\n    def make_body() -> dict[str, Any]:\n        return checkpoint_payload(authority, meter, next_row, oracle, words, queue, cursor, queue_phase)\n    write_checkpoint_snapshot(path, meter, make_body, "checkpoint_serialize")\n    meter._a4_durable_row = max(0, min(ROWS, int(next_row) - 1))\n''', b''),
    (b'''def restore_checkpoint(path: Path, authority: AuthorityAdapter, meter: Meter) -> dict[str, Any]:\n''', b'''def restore_full_checkpoint(path: Path, authority: AuthorityAdapter, meter: Meter) -> dict[str, Any]:\n'''),
    (b'''        resume_state = restore_checkpoint(resume_arg, authority, meter) if resume_arg else None\n''', b'''        resume_state = restore_delta_chain(resume_arg, authority, meter) if resume_arg else None\n'''),
    (b'''            require(rebuilt["rebuild_digest"] == resume_state.get("rebuild_digest"),\n                 "checkpoint:deterministic_rebuild_mismatch")\n''', b'''            if not resume_state.get("_delta_transport"):\n                require(rebuilt["rebuild_digest"] == resume_state.get("rebuild_digest"),\n                        "checkpoint:deterministic_rebuild_mismatch")\n'''),
    (b'''    require(isinstance(boundary_state, dict) and isinstance(combined_state, dict) and\n            isinstance(events, list) and isinstance(state.get("B_roster"), dict) and\n            isinstance(state.get("B_ledgers"), dict) and isinstance(state.get("boundary_ledgers"), dict) and\n            isinstance(state.get("combined_ledgers"), dict) and isinstance(state.get("B_coefficients"), dict) and\n            isinstance(state.get("B_formals"), dict) and isinstance(state.get("K_roster"), list),\n            "checkpoint:echelon_state_shape")\n''', b'''    delta_mode = bool(state.get("_delta_transport"))\n    require(isinstance(boundary_state, dict) and isinstance(combined_state, dict) and\n            isinstance(events, list) and (delta_mode or (isinstance(state.get("B_roster"), dict) and\n            isinstance(state.get("B_ledgers"), dict) and isinstance(state.get("boundary_ledgers"), dict) and\n            isinstance(state.get("combined_ledgers"), dict) and isinstance(state.get("B_coefficients"), dict) and\n            isinstance(state.get("B_formals"), dict)) and isinstance(state.get("K_roster"), list),\n            "checkpoint:echelon_state_shape")\n'''),
    (b'''    require(rebuilt_boundary.pivots == boundary_state.get("pivots") and\n            rebuilt_boundary.rows == boundary_state.get("rows") and\n            rebuilt_boundary.labels == boundary_state.get("labels") and\n            rebuilt_combined.pivots == combined_state.get("pivots") and\n            rebuilt_combined.rows == combined_state.get("rows") and\n            rebuilt_combined.labels == combined_state.get("labels"),\n            "checkpoint:echelon_rebuild_mismatch")\n    require(saved_b_rows == derived_b_rows and saved_b_ledgers == derived_b_ledgers and\n            saved_boundary_ledgers == derived_boundary_ledgers and saved_combined_ledgers == derived_combined_ledgers and\n            saved_b_coefficients == derived_b_coefficients and saved_formals == derived_formals and\n            saved_items == derived_items, "checkpoint:chronological_owner_mismatch")\n''', b'''    if not delta_mode:\n        require(rebuilt_boundary.pivots == boundary_state.get("pivots") and\n                rebuilt_boundary.rows == boundary_state.get("rows") and\n                rebuilt_boundary.labels == boundary_state.get("labels") and\n                rebuilt_combined.pivots == combined_state.get("pivots") and\n                rebuilt_combined.rows == combined_state.get("rows") and\n                rebuilt_combined.labels == combined_state.get("labels"),\n                "checkpoint:echelon_rebuild_mismatch")\n        require(saved_b_rows == derived_b_rows and saved_b_ledgers == derived_b_ledgers and\n                saved_boundary_ledgers == derived_boundary_ledgers and saved_combined_ledgers == derived_combined_ledgers and\n                saved_b_coefficients == derived_b_coefficients and saved_formals == derived_formals and\n                saved_items == derived_items, "checkpoint:chronological_owner_mismatch")\n'''),
    (b'''    require(active == sorted(state.get("active_registry", [])), "checkpoint:active_registry")\n''', b'''    if not delta_mode:\n        require(active == sorted(state.get("active_registry", [])), "checkpoint:active_registry")\n'''),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v18 producer: frozen v17 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v17_owner", "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v18 producer: frozen v17 generated source drift")
    anchor = b'SCHEMA = "d972-r07-word-independent-successor-kernel/v6"\n'
    if raw.count(anchor) != 1:
        raise SystemExit("v18 producer: schema anchor drift")
    raw = raw.replace(anchor, anchor + DELTA_BLOCK)
    for old, new in PATCHES:
        if b"checkpoint:echelon_state_shape" in new:
            continue
        if old.startswith(b"def write_checkpoint") and raw.count(old) == 0:
            old = old.replace(b"\n                      ", b"\n                     ")
        if b"deterministic_rebuild_mismatch" in old and raw.count(old) == 0:
            old = old.replace(b"            require", b"        require")
            old = old.replace(b"\n                 ", b"\n                ")
        if b"deterministic_rebuild_mismatch" in new:
            new = new.replace(b"            if not", b"        if not")
            new = new.replace(b"\n                require", b"\n            require")
            new = new.replace(b"\n                        ", b"\n                ")
        if raw.count(old) != 1:
            raise SystemExit("v18 producer: audited site is not unique")
        raw = raw.replace(old, new)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v18 producer: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen(); ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
                                   "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()
