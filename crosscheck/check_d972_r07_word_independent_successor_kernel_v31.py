#!/usr/bin/env python3
"""Independent A4 v31 checker: v30 with the narrow v429 transport relation.

The v30 owner is frozen and transformed in memory.  This successor changes
only the completed-counter relation: the three terminal transport counters are
the exact difference domain, while all row/accounting counters remain bound to
the authenticated base checkpoint.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v30.py")
OWNER_BYTES = 19871
OWNER_SHA256 = "660d71f34931d138a7d4fb9a4e3e2e17f7b10d3a73a32d59b90b85c9f2419529"
OWNER_GENERATED_BYTES = 286599
OWNER_GENERATED_SHA256 = "29a600c27c4f4f3872575c1edc56aaaca6bd10bcc62eb1236b22dc21e2d120ed"
RESULT_GENERATED_BYTES = 288650
RESULT_GENERATED_SHA256 = "89d8626f8c14972ccad21efa441de07e5e9cf1baf18f98a68751f8bc16e46744"


_V31_HELPER = b'''\
def _v31_validate_completed_snapshot(completed: dict[str, Any], terminal_semantic: dict[str, Any],
                                     terminal_counters: dict[str, Any], serialization: dict[str, Any] | None,
                                     base_checkpoint: dict[str, Any] | None, checkpoint_kind: str) -> None:
    semantic_keys = {key for key, kind in PRODUCER_COUNTER_TYPES.items() if kind == "semantic"}
    transport_keys = {"terminal_canonicalization", "terminal_serialized_bytes", "terminal_final_write"}
    require(transport_keys <= semantic_keys, "checker:producer_transport_domain")
    require(isinstance(completed, dict) and set(completed) == semantic_keys and
            isinstance(terminal_semantic, dict) and set(terminal_semantic) == semantic_keys and
            isinstance(terminal_counters, dict) and set(terminal_counters) == set(PRODUCER_COUNTER_TYPES),
            "checker:producer_completed_domain")
    require(all(_v30_number(number) and number <= PRODUCER_CAPS[key]
                for mapping in (completed, terminal_semantic)
                for key, number in mapping.items()),
            "checker:producer_completed_bounds")
    if checkpoint_kind in {"delta_chain", "sealed_checkpoint"}:
        require(isinstance(base_checkpoint, dict), "checker:producer_base_checkpoint_required")
        base_semantic = base_checkpoint.get("semantic_counters")
        base_completed = base_checkpoint.get("completed_counters")
        require(isinstance(base_semantic, dict) and isinstance(base_completed, dict) and
                set(base_semantic) == semantic_keys and set(base_completed) == semantic_keys and
                base_semantic == base_completed,
                "checker:producer_base_counter_binding")
        require(all(_v30_number(number) and number <= PRODUCER_CAPS[key]
                    for mapping in (base_semantic, base_completed)
                    for key, number in mapping.items()),
                "checker:producer_base_counter_bounds")
        require(base_checkpoint.get("next_row") == 25,
                "checker:producer_transport_cursor_binding")
        require(all(base_semantic[key] == 0 and base_completed[key] == 0
                    for key in transport_keys),
                "checker:producer_transport_base_zero")
        difference = {key for key in semantic_keys if completed[key] != base_semantic[key]}
        require(difference == transport_keys, "checker:producer_transport_difference_domain")
        require(all(completed[key] == base_semantic[key] == base_completed[key]
                    for key in semantic_keys - transport_keys),
                "checker:producer_completed_base_binding")
        require(isinstance(serialization, dict) and
                completed["terminal_canonicalization"] == terminal_semantic["terminal_canonicalization"] ==
                    terminal_counters["terminal_canonicalization"] == serialization.get("terminal_canonicalization") and
                completed["terminal_serialized_bytes"] == terminal_semantic["terminal_serialized_bytes"] ==
                    terminal_counters["terminal_serialized_bytes"] == serialization.get("serialized_work_bytes") and
                completed["terminal_final_write"] == terminal_semantic["terminal_final_write"] ==
                    terminal_counters["terminal_final_write"] == serialization.get("final_write"),
                "checker:producer_transport_terminal_binding")
    else:
        require(completed == terminal_semantic, "checker:producer_completed_legacy_binding")
    require(all(completed[key] <= terminal_semantic[key] for key in semantic_keys),
            "checker:producer_completed_not_above_terminal")
'''.replace(b"\\\n", b"")


_OLD_V30_COMPLETED = b'''def _v30_validate_completed_snapshot(completed: dict[str, Any], terminal_semantic: dict[str, Any],
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


'''


PATCHES = (
    (_OLD_V30_COMPLETED, _V31_HELPER),
    (
        b'    _v30_validate_completed_snapshot(terminal_completed, terminal_semantic, base_checkpoint, checkpoint_kind)\n',
        b'    _v31_validate_completed_snapshot(terminal_completed, terminal_semantic, terminal_counters,\n'
        b'                                    serialization, base_checkpoint, checkpoint_kind)\n',
    ),
)


def _apply_patches(raw: bytes) -> bytes:
    for index, (old, new) in enumerate(PATCHES, 1):
        if raw.count(old) != 1:
            raise SystemExit(f"v31 checker: patch {index} cardinality is not one")
        raw = raw.replace(old, new)
    return raw


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v31 checker: frozen v30 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v30_owner",
                                "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v31 checker: frozen v30 generated source drift")
    raw = _apply_patches(raw)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v31 checker: resulting generated source drift")
    return raw


# This JSON is the canonical map projection parsed from the immutable producer
# result and its authenticated row-24 base checkpoint.  No map is filled with
# a default value: the fixture compares every map and the raw projection hash.
_ROW26_PINNED_MAPS_JSON = r'''{"asset_sha256":"7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5","base_completed":{"active_keys":0,"affine_sparse_ops":0,"boundary_rank_rises":0,"bridge_occurrences":264,"bridge_rows":24,"canonicalization":64,"checkpoint_total_bytes":122683,"correlation_pairs":0,"direct_replays":70,"dual_support":0,"expanded_letters":0,"final_write":0,"literal_comparisons":6441,"membership_queries":24,"membership_reductions":0,"prefix_edge_state_products":159700,"prefix_edges":15970,"prefix_nodes":15970,"queue_actions":0,"quotient_reductions":1396,"row_assemblies":24,"row_piece_products":72,"serialized_bytes":0,"suffix_edge_state_products":0,"suffix_edges":0,"suffix_nodes":0,"terminal_canonicalization":0,"terminal_checkpoint_bytes":0,"terminal_final_write":0,"terminal_serialized_bytes":0,"typed_context_products":1065,"word_nodes":0},"base_next_row":25,"base_semantic":{"active_keys":0,"affine_sparse_ops":0,"boundary_rank_rises":0,"bridge_occurrences":264,"bridge_rows":24,"canonicalization":64,"checkpoint_total_bytes":122683,"correlation_pairs":0,"direct_replays":70,"dual_support":0,"expanded_letters":0,"final_write":0,"literal_comparisons":6441,"membership_queries":24,"membership_reductions":0,"prefix_edge_state_products":159700,"prefix_edges":15970,"prefix_nodes":15970,"queue_actions":0,"quotient_reductions":1396,"row_assemblies":24,"row_piece_products":72,"serialized_bytes":0,"suffix_edge_state_products":0,"suffix_edges":0,"suffix_nodes":0,"terminal_canonicalization":0,"terminal_checkpoint_bytes":0,"terminal_final_write":0,"terminal_serialized_bytes":0,"typed_context_products":1065,"word_nodes":0},"terminal_completed":{"active_keys":0,"affine_sparse_ops":0,"boundary_rank_rises":0,"bridge_occurrences":264,"bridge_rows":24,"canonicalization":64,"checkpoint_total_bytes":122683,"correlation_pairs":0,"direct_replays":70,"dual_support":0,"expanded_letters":0,"final_write":0,"literal_comparisons":6441,"membership_queries":24,"membership_reductions":0,"prefix_edge_state_products":159700,"prefix_edges":15970,"prefix_nodes":15970,"queue_actions":0,"quotient_reductions":1396,"row_assemblies":24,"row_piece_products":72,"serialized_bytes":0,"suffix_edge_state_products":0,"suffix_edges":0,"suffix_nodes":0,"terminal_canonicalization":7,"terminal_checkpoint_bytes":0,"terminal_final_write":1,"terminal_serialized_bytes":9300,"typed_context_products":1065,"word_nodes":0},"terminal_counters":{"active_keys":1094076,"affine_sparse_ops":277568,"boundary_rank_rises":138784,"bridge_occurrences":286,"bridge_rows":26,"canonicalization":64,"checkpoint_peak_bytes":25591,"checkpoint_total_bytes":127008,"correlation_pairs":46789964,"direct_replays":70,"dual_support":11706998,"expanded_letters":0,"final_write":0,"input_bytes":45933634,"literal_comparisons":6543,"membership_queries":26,"membership_reductions":1083955,"prefix_edge_state_products":159700,"prefix_edges":15970,"prefix_nodes":15970,"queue_actions":0,"quotient_reductions":1396,"restore_validation":199659,"row_assemblies":26,"row_piece_products":78,"rss_bytes":4790583296,"serialized_bytes":0,"suffix_edge_state_products":0,"suffix_edges":0,"suffix_nodes":0,"terminal_canonicalization":7,"terminal_checkpoint_bytes":0,"terminal_final_write":1,"terminal_serialized_bytes":9300,"typed_context_products":1145,"wall_seconds":14402.408729186,"word_nodes":0},"terminal_host":{"input_bytes":45933634,"wall_seconds":14402.408729186},"terminal_peak":{"checkpoint_peak_bytes":25591,"rss_bytes":4790583296},"terminal_restore":{"restore_validation":199659},"terminal_semantic":{"active_keys":1094076,"affine_sparse_ops":277568,"boundary_rank_rises":138784,"bridge_occurrences":286,"bridge_rows":26,"canonicalization":64,"checkpoint_total_bytes":127008,"correlation_pairs":46789964,"direct_replays":70,"dual_support":11706998,"expanded_letters":0,"final_write":0,"literal_comparisons":6543,"membership_queries":26,"membership_reductions":1083955,"prefix_edge_state_products":159700,"prefix_edges":15970,"prefix_nodes":15970,"queue_actions":0,"quotient_reductions":1396,"row_assemblies":26,"row_piece_products":78,"serialized_bytes":0,"suffix_edge_state_products":0,"suffix_edges":0,"suffix_nodes":0,"terminal_canonicalization":7,"terminal_checkpoint_bytes":0,"terminal_final_write":1,"terminal_serialized_bytes":9300,"typed_context_products":1145,"word_nodes":0},"terminal_serialization":{"atomic":true,"canonicalization":true,"final_write":1,"output_bytes":9300,"serialized_work_bytes":9300,"terminal_canonicalization":7,"terminal_transport":true}}'''
_ROW26_PINNED_MAPS_BYTES = 4520
_ROW26_PINNED_MAPS_SHA256 = "8651e982f7efc6a72d2b766cf452c3eeb98e315c76262e7e62b0344c2378bba5"


def _parse_pinned_maps() -> dict[str, Any]:
    raw = _ROW26_PINNED_MAPS_JSON.encode("ascii")
    if len(raw) != _ROW26_PINNED_MAPS_BYTES or hashlib.sha256(raw).hexdigest() != _ROW26_PINNED_MAPS_SHA256:
        raise AssertionError("v31 pinned map projection drift")
    value = json.loads(raw.decode("ascii"))
    if not isinstance(value, dict):
        raise AssertionError("v31 pinned map projection shape")
    return value


def _toy_namespace() -> dict[str, Any]:
    raw = restore_frozen()
    ns: dict[str, Any] = {"__name__": "_r07_a4_v31_test",
                          "__file__": str(Path(__file__).resolve()),
                          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)
    return ns


def _row26_fixture(ns: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Any, dict[str, Any]]:
    """Parse and use the exact pinned base/terminal map projection."""
    pinned = _parse_pinned_maps()
    types = ns["PRODUCER_COUNTER_TYPES"]
    caps = ns["PRODUCER_CAPS"]
    base_semantic = pinned["base_semantic"]
    base_completed = pinned["base_completed"]
    terminal_counters = pinned["terminal_counters"]
    terminal_semantic = pinned["terminal_semantic"]
    terminal_completed = pinned["terminal_completed"]
    base = {"counter_registry": dict(types), "semantic_counters": base_semantic,
            "completed_counters": base_completed, "resource_envelope": dict(caps),
            "resource_object_caps": dict(ns["OBJECT_CAPS"]), "next_row": pinned["base_next_row"]}
    resource = {"limits": dict(caps), "counter_registry": dict(types),
                "counters": terminal_counters, "semantic_counters": terminal_semantic,
                "completed_counters": terminal_completed,
                "restore_validation_counters": pinned["terminal_restore"],
                "host_counters": pinned["terminal_host"], "host_history": [],
                "peak_counters": pinned["terminal_peak"],
                "object_caps": dict(ns["OBJECT_CAPS"]), "last_replayable_state": "dual_pullback",
                "single_process": True, "no_retry_or_pool": True}
    producer = {"schema": ns["SCHEMA"], "status": ns["UNKNOWN_RESOURCE"],
                "terminal": ns["UNKNOWN_RESOURCE"], "complete": False,
                "authority": {"fixture": "authority"},
                "reason": "dual_pullback:wall_seconds:14402.408729186>14400:state=dual_pullback",
                "checkpoint": {"kind": "delta_chain"}, "resource": resource,
                "forbidden_downstream": {"lift": False, "fake": False, "Ihara": False},
                "serialization": pinned["terminal_serialization"],
                "self_digest_sha256": "973cb6f4b025ad9e19e4aa0fc0142174aabd10a91eea356616c819b07326d651"}
    authority = type("FixtureAuthority", (), {"identity": {"fixture": "authority"}})()
    return producer, base, resource, authority, pinned


def self_test() -> None:
    raw = restore_frozen()
    text = raw.decode("ascii")
    assert "_v30_validate_completed_snapshot" not in text
    assert text.count("_v31_validate_completed_snapshot") == 2
    ns = _toy_namespace()
    Reject = ns["Reject"]
    producer, base, resource, authority, pinned = _row26_fixture(ns)
    assert resource["counters"] == pinned["terminal_counters"]
    assert resource["semantic_counters"] == pinned["terminal_semantic"]
    assert resource["completed_counters"] == pinned["terminal_completed"]
    assert base["semantic_counters"] == pinned["base_semantic"]
    assert base["completed_counters"] == pinned["base_completed"]
    assert base["semantic_counters"] == base["completed_counters"]
    assert all(base["semantic_counters"][key] == 0 for key in
               ("terminal_canonicalization", "terminal_serialized_bytes", "terminal_final_write"))
    validate = ns["validate_terminal_payload"]
    validate(producer, ns["UNKNOWN_RESOURCE"], authority, ns["Meter"](), base)

    def rejected(name: str, mutate: Any) -> None:
        candidate = json.loads(json.dumps(producer))
        candidate_base = json.loads(json.dumps(base))
        mutate(candidate, candidate_base)
        try:
            validate(candidate, ns["UNKNOWN_RESOURCE"], authority, ns["Meter"](), candidate_base)
        except (Reject, AssertionError, KeyError, IndexError, TypeError):
            return
        raise AssertionError(name + " was accepted")

    rejected("base_semantic_drift", lambda p, b: b["semantic_counters"].update({"bridge_rows": 23}))
    rejected("base_completed_drift", lambda p, b: b["completed_counters"].update({"bridge_rows": 23}))
    rejected("base_transport_nonzero", lambda p, b: (
        b["semantic_counters"].update({"terminal_final_write": 1}),
        b["completed_counters"].update({"terminal_final_write": 1})))
    rejected("completed_non_transport_difference", lambda p, b: p["resource"]["completed_counters"].update({"active_keys": 1094076}))
    rejected("difference_domain_missing", lambda p, b: p["resource"]["completed_counters"].update({"terminal_final_write": 0}))
    rejected("difference_domain_extra", lambda p, b: p["resource"]["completed_counters"].update({"active_keys": 1}))
    rejected("transport_serialization_drift", lambda p, b: p["serialization"].update({"serialized_work_bytes": 9299}))
    rejected("completed_above_terminal", lambda p, b: (
        p["resource"]["completed_counters"].update({"active_keys": 1094077}),
        b["semantic_counters"].update({"active_keys": 1094077}),
        b["completed_counters"].update({"active_keys": 1094077})))
    rejected("second_over_cap_canonical_and_view", lambda p, b: (
        p["resource"]["counters"].update({"active_keys": ns["PRODUCER_CAPS"]["active_keys"] + 1}),
        p["resource"]["semantic_counters"].update({"active_keys": ns["PRODUCER_CAPS"]["active_keys"] + 1})))
    rejected("transport_advances_cursor", lambda p, b: b.update({"next_row": 27}))
    assert resource["counters"]["wall_seconds"] > ns["PRODUCER_CAPS"]["wall_seconds"]
    print("R07_A4_COUNTER_TRANSPORT_V31_SELFTEST_PASS rows=26 difference_domain=3 mutations=10 second_overcap=CANONICAL_AND_TYPED_VIEW")


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
