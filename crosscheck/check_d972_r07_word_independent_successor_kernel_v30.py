#!/usr/bin/env python3
"""Independent A4 v30 checker: guarded v28 resume-resource successor.

The frozen v28 owner remains the mathematical and replay owner.  This wrapper
only transforms its generated checker with cardinality-guarded patches for the
resumed counter relation and the one typed resource witness.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v28.py")
OWNER_BYTES = 11048
OWNER_SHA256 = "c2c1629dc225ebea085b72d1900d7684f4c4184f8e064da8ec4057dc921d2bfa"
OWNER_GENERATED_BYTES = 281780
OWNER_GENERATED_SHA256 = "444ee68e79715657707c77778fcb597f83d289147699e7ce5295414b956edeae"
RESULT_GENERATED_BYTES = 286599
RESULT_GENERATED_SHA256 = "29a600c27c4f4f3872575c1edc56aaaca6bd10bcc62eb1236b22dc21e2d120ed"


_HELPERS = b'''\
def _v30_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _v30_validate_completed_snapshot(completed: dict[str, Any], terminal_semantic: dict[str, Any],
                                     base_checkpoint: dict[str, Any] | None, checkpoint_kind: str) -> None:
    semantic_keys = {key for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "semantic"}
    require(isinstance(completed, dict) and set(completed) == semantic_keys,
            "checker:producer_completed_domain")
    require(all(_v30_number(value) and value <= PRODUCER_CAPS[key]
                for key, value in completed.items()),
            "checker:producer_completed_bounds")
    if checkpoint_kind in {"delta_chain", "sealed_checkpoint"}:
        require(isinstance(base_checkpoint, dict), "checker:producer_base_checkpoint_required")
        base_semantic = base_checkpoint.get("semantic_counters")
        base_completed = base_checkpoint.get("completed_counters")
        require(isinstance(base_semantic, dict) and isinstance(base_completed, dict) and
                set(base_semantic) == semantic_keys and set(base_completed) == semantic_keys and
                base_semantic == base_completed and completed == base_semantic,
                "checker:producer_completed_base_binding")
        require(all(_v30_number(value) and value <= PRODUCER_CAPS[key]
                    for mapping in (base_semantic, base_completed)
                    for key, value in mapping.items()),
                "checker:producer_base_counter_bounds")
    else:
        require(completed == terminal_semantic, "checker:producer_completed_legacy_binding")
    require(all(completed[key] <= terminal_semantic[key] for key in semantic_keys),
            "checker:producer_completed_not_above_terminal")


def _v30_validate_terminal_typed_views(resource: dict[str, Any], trigger: str,
                                        measured: float, limit: float) -> None:
    canonical = resource["counters"]
    semantic = resource["semantic_counters"]
    restore = resource["restore_validation_counters"]
    host = resource["host_counters"]
    peak = resource["peak_counters"]
    typed_maps = (canonical, semantic, restore, host, peak)
    require(trigger in canonical and measured > limit == float(PRODUCER_CAPS[trigger]) and
            _v30_number(canonical[trigger]) and canonical[trigger] >= measured,
            "checker:producer_resource_trigger")
    semantic_keys = {key for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "semantic"}
    for mapping in typed_maps:
        for key, number in mapping.items():
            require(key in PRODUCER_COUNTER_TYPES and _v30_number(number),
                    "checker:producer_terminal_counter_type")
            cap = float(PRODUCER_CAPS[key])
            if key == trigger:
                require(number == canonical[trigger] and number >= measured and number > cap,
                        "checker:producer_resource_trigger_typed_view")
            else:
                require(number <= cap, "checker:producer_terminal_counter_cap")
    require(all(canonical[key] == semantic[key] for key in semantic_keys),
            "checker:producer_terminal_semantic_view")
    require(canonical["wall_seconds"] == host["wall_seconds"] and
            canonical["input_bytes"] == host["input_bytes"] and
            canonical["rss_bytes"] == peak["rss_bytes"] and
            canonical["checkpoint_peak_bytes"] == peak["checkpoint_peak_bytes"] and
            canonical["restore_validation"] == restore.get("restore_validation", 0),
            "checker:producer_terminal_typed_view")


def _v30_validate_terminal_bounded_views(resource: dict[str, Any]) -> None:
    maps = (resource["counters"], resource["semantic_counters"],
            resource["completed_counters"], resource["restore_validation_counters"],
            resource["host_counters"], resource["peak_counters"])
    for mapping in maps:
        for key, number in mapping.items():
            require(key in PRODUCER_CAPS and _v30_number(number) and number <= PRODUCER_CAPS[key],
                    "checker:producer_terminal_counter_cap")
'''.replace(b"\\\n", b"")


PATCHES = (
    (
        b'def validate_delta_terminal_chain(reference: dict[str, Any], meter: Meter) -> None:',
        b'def validate_delta_terminal_chain(reference: dict[str, Any], meter: Meter) -> dict[str, Any]:',
    ),
    (
        b'    state = _checker_delta_base_state(base_raw)\n'
        b'    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64\n',
        b'    base_state = _checker_delta_base_state(base_raw)\n'
        b'    state = json.loads(canon(base_state).decode("ascii"))\n'
        b'    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64\n',
    ),
    (
        b'    require(len(list(head_path.parent.glob(head_path.name + ".delta.*.json"))) == count,\n'
        b'            "checker:delta_orphan_segment")\n'
        b'LEGACY_PRODUCER_CHECKPOINT_SCHEMA',
        b'    require(len(list(head_path.parent.glob(head_path.name + ".delta.*.json"))) == count,\n'
        b'            "checker:delta_orphan_segment")\n'
        b'    return base_state\n'
        b'LEGACY_PRODUCER_CHECKPOINT_SCHEMA',
    ),
    (
        b'def validate_terminal_checkpoint(reference: dict[str, Any], authority: Authority | None, meter: Meter) -> None:',
        b'def validate_terminal_checkpoint(reference: dict[str, Any], authority: Authority | None, meter: Meter) -> dict[str, Any] | None:',
    ),
    (
        b'        validate_delta_terminal_chain(reference, meter)\n        return\n',
        b'        return validate_delta_terminal_chain(reference, meter)\n',
    ),
    (
        b'            "checker:terminal_checkpoint_replayable")\n\n\ndef validate_terminal_payload',
        b'            "checker:terminal_checkpoint_replayable")\n'
        b'    return value\n\n\ndef validate_terminal_payload',
    ),
    (
        b'def validate_terminal_payload(producer: dict[str, Any], status: str,',
        _HELPERS + b'\ndef validate_terminal_payload(producer: dict[str, Any], status: str,',
    ),
    (
        b'                              authority: Authority | None, meter: Meter) -> None:\n',
        b'                              authority: Authority | None, meter: Meter,\n'
        b'                              base_checkpoint: dict[str, Any] | None = None) -> None:\n',
    ),
    (
        b'            isinstance(terminal_completed, dict) and terminal_completed == terminal_semantic and\n',
        b'            isinstance(terminal_completed, dict) and\n',
    ),
    (
        b'            all(isinstance(number, (int, float)) and number >= 0\n'
        b'                and number <= PRODUCER_CAPS[key]\n'
        b'                for mapping in (terminal_counters, terminal_semantic, terminal_completed,\n'
        b'                                terminal_restore, terminal_host, terminal_peak)\n'
        b'                for key, number in mapping.items()),\n',
        b'            all(_v30_number(number)\n'
        b'                for mapping in (terminal_counters, terminal_semantic, terminal_completed,\n'
        b'                                terminal_restore, terminal_host, terminal_peak)\n'
        b'                for number in mapping.values()),\n',
    ),
    (
        b'            "checker:producer_terminal_resource_envelope")\n',
        b'            "checker:producer_terminal_resource_envelope")\n'
        b'    checkpoint_kind = producer.get("checkpoint", {}).get("kind") if isinstance(producer.get("checkpoint"), dict) else ""\n'
        b'    _v30_validate_completed_snapshot(terminal_completed, terminal_semantic, base_checkpoint, checkpoint_kind)\n'
        b'    if status != UNKNOWN_RESOURCE:\n'
        b'        _v30_validate_terminal_bounded_views(resource)\n',
    ),
    (
        b'        require(cap in PRODUCER_COUNTER_TYPES and value > limit and\n',
        b'        _v30_validate_terminal_typed_views(resource, cap, value, limit)\n'
        b'        require(cap in PRODUCER_COUNTER_TYPES and value > limit and\n',
    ),
    (
        b'                    validate_terminal_payload(producer, status, None, meter)\n'
        b'                    if status in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):\n'
        b'                        validate_terminal_checkpoint(producer_checkpoint, None, meter)\n',
        b'                    base_checkpoint = None\n'
        b'                    if status in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):\n'
        b'                        base_checkpoint = validate_terminal_checkpoint(producer_checkpoint, None, meter)\n'
        b'                    validate_terminal_payload(producer, status, None, meter, base_checkpoint)\n',
    ),
    (
        b'            validate_terminal_payload(producer, status, authority, meter)\n'
        b'            if status in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):\n'
        b'                validate_terminal_checkpoint(producer_checkpoint, authority, meter)\n',
        b'            base_checkpoint = None\n'
        b'            if status in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):\n'
        b'                base_checkpoint = validate_terminal_checkpoint(producer_checkpoint, authority, meter)\n'
        b'            validate_terminal_payload(producer, status, authority, meter, base_checkpoint)\n',
    ),
)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v30 checker: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v30 checker: frozen v28 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v28_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v30 checker: frozen v28 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v30 checker: resulting generated source drift")
    return raw


def _toy_namespace() -> dict[str, Any]:
    raw = restore_frozen()
    ns: dict[str, Any] = {"__name__": "_r07_a4_v30_test",
                          "__file__": str(Path(__file__).resolve()),
                          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)
    return ns


def _row26_fixture(ns: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Any]:
    """Build a small exact-shape row-26 counter fixture for production gates."""
    caps = ns["PRODUCER_CAPS"]
    types = ns["PRODUCER_COUNTER_TYPES"]
    base_semantic = {
        "active_keys": 0, "affine_sparse_ops": 0, "boundary_rank_rises": 0,
        "bridge_occurrences": 264, "bridge_rows": 24, "canonicalization": 64,
        "checkpoint_total_bytes": 122683, "correlation_pairs": 0,
        "direct_replays": 70, "dual_support": 0, "expanded_letters": 0,
        "final_write": 0, "literal_comparisons": 6441, "membership_queries": 24,
        "membership_reductions": 0, "prefix_edge_state_products": 159700,
        "prefix_edges": 15970, "prefix_nodes": 15970, "queue_actions": 0,
        "quotient_reductions": 1396, "row_assemblies": 24, "row_piece_products": 72,
        "serialized_bytes": 0, "suffix_edge_state_products": 0, "suffix_edges": 0,
        "suffix_nodes": 0, "terminal_canonicalization": 7,
        "terminal_checkpoint_bytes": 0, "terminal_final_write": 1,
        "terminal_serialized_bytes": 9300, "typed_context_products": 1065,
        "word_nodes": 0,
    }
    terminal_semantic = {
        "active_keys": 1094076, "affine_sparse_ops": 277568,
        "boundary_rank_rises": 138784, "bridge_occurrences": 286,
        "bridge_rows": 26, "canonicalization": 64, "checkpoint_total_bytes": 127008,
        "correlation_pairs": 46789964, "direct_replays": 70,
        "dual_support": 11706998, "expanded_letters": 0, "final_write": 0,
        "literal_comparisons": 6543, "membership_queries": 26,
        "membership_reductions": 1083955, "prefix_edge_state_products": 159700,
        "prefix_edges": 15970, "prefix_nodes": 15970, "queue_actions": 0,
        "quotient_reductions": 1396, "row_assemblies": 26, "row_piece_products": 78,
        "serialized_bytes": 0, "suffix_edge_state_products": 0, "suffix_edges": 0,
        "suffix_nodes": 0, "terminal_canonicalization": 7,
        "terminal_checkpoint_bytes": 0, "terminal_final_write": 1,
        "terminal_serialized_bytes": 9300, "typed_context_products": 1145,
        "word_nodes": 0,
    }
    base = {"counter_registry": dict(types), "semantic_counters": base_semantic,
            "completed_counters": dict(base_semantic),
            "resource_envelope": dict(caps), "resource_object_caps": dict(ns["OBJECT_CAPS"]),
            "next_row": 25}
    counters = dict(terminal_semantic)
    counters.update({"checkpoint_peak_bytes": 25591, "input_bytes": 45933634,
                     "restore_validation": 199659, "rss_bytes": 4790583296,
                     "wall_seconds": 14402.408729186})
    resource = {"limits": dict(caps), "counter_registry": dict(types),
                "counters": counters, "semantic_counters": terminal_semantic,
                "completed_counters": dict(base_semantic),
                "restore_validation_counters": {"restore_validation": 199659},
                "host_counters": {"wall_seconds": counters["wall_seconds"],
                                   "input_bytes": 45933634},
                "host_history": [{"input_bytes": 45908053, "wall_seconds": 22.844783612}],
                "peak_counters": {"rss_bytes": 4790583296, "checkpoint_peak_bytes": 25591},
                "object_caps": dict(ns["OBJECT_CAPS"]),
                "last_replayable_state": "dual_pullback", "single_process": True,
                "no_retry_or_pool": True}
    producer = {"schema": ns["SCHEMA"], "status": ns["UNKNOWN_RESOURCE"],
                "terminal": ns["UNKNOWN_RESOURCE"], "complete": False,
                "authority": {"fixture": "authority"},
                "reason": "dual_pullback:wall_seconds:14402.408729186>14400:state=dual_pullback",
                "checkpoint": {"kind": "delta_chain"}, "resource": resource,
                "forbidden_downstream": {"lift": False, "fake": False, "Ihara": False},
                "serialization": {"canonicalization": True, "atomic": True,
                                   "terminal_transport": True,
                                   "terminal_canonicalization": counters["terminal_canonicalization"],
                                   "serialized_work_bytes": counters["terminal_serialized_bytes"],
                                   "output_bytes": 9300,
                                   "final_write": counters["terminal_final_write"]},
                 "self_digest_sha256": "973cb6f4b025ad9e19e4aa0fc0142174aabd10a91eea356616c819b07326d651"}
    authority = type("FixtureAuthority", (), {"identity": {"fixture": "authority"}})()
    return producer, base, resource, authority


def self_test() -> None:
    raw = restore_frozen()
    text = raw.decode("ascii")
    assert "terminal_completed == " + "terminal_semantic" not in text
    assert text.count("_v30_validate_completed_snapshot") == 2
    assert text.count("_v30_validate_terminal_typed_views") == 2
    ns = _toy_namespace()
    Reject = ns["Reject"]
    producer, base, resource, authority = _row26_fixture(ns)
    meter = ns["Meter"]()
    validate = ns["validate_terminal_payload"]
    validate(producer, ns["UNKNOWN_RESOURCE"], authority, meter, base)

    def rejected(name: str, mutate: Any) -> None:
        candidate = json.loads(json.dumps(producer))
        candidate_base = json.loads(json.dumps(base))
        mutate(candidate, candidate_base)
        try:
            validate(candidate, ns["UNKNOWN_RESOURCE"], authority, ns["Meter"](), candidate_base)
        except (Reject, AssertionError, KeyError, IndexError, TypeError):
            return
        raise AssertionError(name + " was accepted")

    rejected("base_completed_drift", lambda p, b: b["completed_counters"].update({"bridge_rows": 23}))
    rejected("base_semantic_drift", lambda p, b: b["semantic_counters"].update({"bridge_rows": 23}))
    rejected("completed_above_terminal", lambda p, b: (
        p["resource"]["completed_counters"].update({"active_keys": 1094077}),
        b["semantic_counters"].update({"active_keys": 1094077}),
        b["completed_counters"].update({"active_keys": 1094077})))
    rejected("completed_missing_key", lambda p, b: p["resource"]["completed_counters"].pop("bridge_rows"))
    rejected("completed_extra_key", lambda p, b: p["resource"]["completed_counters"].update({"not_registered": 0}))
    rejected("witness_value_not_above_limit", lambda p, b: p.update({
        "reason": p["reason"].replace("14402.408729186>14400", "14400>14400")}))
    rejected("canonical_below_witness", lambda p, b: p.update({
        "reason": p["reason"].replace("14402.408729186>14400", "14403>14400")}))
    rejected("trigger_cap_drift", lambda p, b: p.update({"reason": p["reason"].replace(">14400:", ">14399:")}))
    rejected("trigger_typed_view_drift", lambda p, b: p["resource"]["host_counters"].update({"wall_seconds": 14401.0}))
    rejected("trigger_state_drift", lambda p, b: p.update({"reason": p["reason"].replace("state=dual_pullback", "state=other")}))
    rejected("second_over_cap", lambda p, b: p["resource"]["semantic_counters"].update({"active_keys": ns["PRODUCER_CAPS"]["active_keys"] + 1}))
    rejected("missing_authenticated_base", lambda p, b: b.clear())
    # The positive fixture has exactly the one permitted wall excess; an old
    # universal <= loop would reject it before reaching the witness gate.
    assert resource["counters"]["wall_seconds"] > ns["PRODUCER_CAPS"]["wall_seconds"]
    print("R07_A4_RESUMED_RESOURCE_V30_SELFTEST_PASS rows=26 counter_predicates=2 mutations=12 old_predicate=REJECT")


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
