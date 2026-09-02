#!/usr/bin/env python3
"""A4 v35: acceptance-route mutation fixture for the independent checker."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V34 = ("crosscheck/check_d972_r07_word_independent_successor_kernel_v34.py", 5838,
       "b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba")
V34_GENERATED = (312553, "2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _need(value: object, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def _load_v34() -> bytes:
    path = ROOT / V34[0]; raw = path.read_bytes()
    _need(len(raw) == V34[1] and _sha(raw) == V34[2], "v35:v34_pin")
    ns: dict[str, Any] = {"__name__": "task514_v34_owner", "__file__": str(path),
                           "__package__": None, "__cached__": None}
    saved = sys.argv[:]
    try:
        sys.argv = [str(path)]
        exec(compile(raw, str(path), "exec"), ns, ns)
    finally:
        sys.argv = saved
    generated = ns.get("_SOURCE")
    _need(isinstance(generated, bytes) and len(generated) == V34_GENERATED[0] and
          _sha(generated) == V34_GENERATED[1], "v35:v34_generated_pin")
    return generated


_SOURCE = _load_v34()


def _fixture() -> dict[str, Any]:
    ns: dict[str, Any] = {"__name__": "task514_checker_fixture", "__file__": str(ROOT / V34[0])}
    exec(compile(_SOURCE, str(ROOT / V34[0]), "exec"), ns, ns)
    original_validate = ns["validate_terminal_checkpoint"]
    original_physical = ns["_a4_v33_validate_physical_chain"]
    original_read_json = ns["_a4_v33_read_json"]
    calls = {"validate_terminal_checkpoint": 0, "_a4_v33_validate_physical_chain": 0,
             "_a4_v33_read_json": 0, "ordinary_materializer": 0}

    def validate(reference: dict[str, Any], authority: Any, meter: Any) -> Any:
        calls["validate_terminal_checkpoint"] += 1
        return original_validate(reference, authority, meter)

    def physical(reference: dict[str, Any], authority: Any, meter: Any) -> Any:
        calls["_a4_v33_validate_physical_chain"] += 1
        return original_physical(reference, authority, meter)

    ns["validate_terminal_checkpoint"] = validate
    ns["_a4_v33_validate_physical_chain"] = physical
    authority = object()
    with tempfile.TemporaryDirectory(prefix="task514_checker_") as td:
        area = Path(td); head_path = area / "fixture.head.json"
        shard_path = area / "shard.00000001.json"
        shard_path.write_bytes(b"fixture-placeholder")
        mode = {"name": "dual"}

        ordinary_base = {"next_row": 27, "live_duals": [{"query_id": "R:27"}],
                         "oracle_records": [], "query_event_chain": [], "dual_event_chain": [],
                         "insertion_events": [], "K_roster": [], "echelon_rebuild": {},
                         "semantic_counters": {"semantic": 1}, "epoch_digest": "e0"}

        def reseal_ordinary(dual_mutation: bool) -> dict[str, Any]:
            body = dict(ordinary_base)
            body["live_duals"] = ([{"query_id": "R:27"}, {"query_id": "R:27:dup"}]
                                  if dual_mutation else [{"query_id": "R:27"}])
            body["self_digest_sha256"] = ns["digest"](body)
            return body

        def materializer(reference: dict[str, Any], auth: Any, meter: Any) -> dict[str, Any]:
            calls["ordinary_materializer"] += 1
            body = dict(reference); claimed = body.pop("self_digest_sha256", None)
            ns["require"](claimed == ns["digest"](body), "fixture:ordinary_seal")
            return body

        def fake_base(auth: Any, base: dict[str, Any], meter: Any) -> tuple[Any, Any, dict[str, Any]]:
            class BoundaryStub:
                by_key: dict[Any, Any] = {}
            class BasisStub:
                class Space:
                    pivots: list[Any] = []
                bspace = Space()
            return BoundaryStub(), BasisStub(), {"semantic": 1}

        ns["_a4_v33_ordinary_state"] = materializer
        ns["_a4_v33_base_basis"] = fake_base
        ns["checkpoint_input"] = lambda path, label: (head_path if path.name == "fixture.head.json" else shard_path)
        # The pinned checker deliberately fails closed on Windows before its
        # same-handle primitive is available.  This bounded fixture replaces
        # only that transport read with an ordinary TEMP-file read; all
        # authenticated acceptance predicates remain generated code.
        ns["read_once"] = lambda path, expected, meter, label, terminal_transport=False: path.read_bytes()

        target = {}; word: list[int] = []; bridge = {}
        query = {"query_id": "R:27", "next_row": 27, "target": target,
                 "source_word": word, "target_digest": ns["digest"](target),
                 "word_digest": ns["digest"](word), "bridge": bridge,
                 "bridge_digest": ns["digest"](bridge), "row_cursor": 26,
                 "bridge_cursor": 26}
        shard_body: dict[str, Any] = {
            "schema": "d972-r07-word-independent-successor-kernel/v430/shard",
            "sequence": 1, "previous": None, "chain": "", "batch_offsets": [0, 0],
            "query": query, "candidate_count": 1, "candidate_prefix": [],
            "candidate_prefix_digest": ns["digest"]([]),
            "candidate_order_digest": ns["digest"]([]), "dual": [], "target_dot": {},
            "correlation": {"pair_count": 0, "accumulator_digest": ns["digest"]({})},
            "dual_digest": ns["digest"]({"query_id": "R:27", "dual": [],
                                             "target": target, "target_dot": {},
                                             "correlation": {"pair_count": 0, "accumulator_digest": ns["digest"]({})}}),
            "dual_event": {"index": 1, "query_id": "R:27", "digest": ""},
            "accepted_mask": [], "accepted_count": 0, "entries": [],
            "semantic_before": {"semantic": 99}, "semantic_after": {"semantic": 100},
            "counter_digest": "", "before": {}, "after": {},
            "epoch_before": "e0", "epoch_after": "e1"}
        shard_body["chain"] = ns["sha"]((str(None) + ns["digest"](
            {k: v for k, v in shard_body.items() if k != "chain"})).encode("ascii"))
        shard = dict(shard_body); shard["self_digest_sha256"] = ns["digest"](shard_body)
        head_body = {"schema": "d972-r07-word-independent-successor-kernel/v430/head",
                     "obsolete": False, "sequence": 1, "next_row": 27}
        head = dict(head_body); head["self_digest_sha256"] = ns["digest"](head_body)
        head_raw = ns["canon"](head); shard_raw = ns["canon"](shard)
        head_path.write_bytes(head_raw)
        head_id = {"path": "fixture.head.json", "bytes": len(head_raw), "sha256": ns["sha"](head_raw)}
        shard_id = {"path": "shard.00000001.json", "bytes": len(shard_raw), "sha256": ns["sha"](shard_raw)}
        shard_path.write_bytes(shard_raw)
        def read_json(identity: dict[str, Any], meter: Any, label: str) -> tuple[Path, dict[str, Any], bytes]:
            calls["_a4_v33_read_json"] += 1
            return original_read_json(identity, meter, label)
        ns["_a4_v33_read_json"] = read_json
        reference = {"kind": "physical_shard_chain", "owner": "producer", "ordinary": reseal_ordinary(True),
                     "physical_head": head_id, "shards": [shard_id], "sequence": 1,
                     "last_shard_sha256": "", "chain": "", "next_row": 27,
                     "open_query": query, "cumulative_examined": 1,
                     "cumulative_accepted": 0, "obsolete": False}

        mode["name"] = "dual"; reference["ordinary"] = reseal_ordinary(True)
        try: ns["validate_terminal_checkpoint"](reference, authority, ns["Meter"]())
        except Exception as exc: dual_reason = str(exc)
        else: raise RuntimeError("fixture:live_dual_mutation_accepted")
        _need("physical:live_dual_history" in dual_reason, "fixture:live_dual_reason:" + dual_reason)
        mode["name"] = "semantic"; reference["ordinary"] = reseal_ordinary(False)
        try: ns["validate_terminal_checkpoint"](reference, authority, ns["Meter"]())
        except Exception as exc: semantic_reason = str(exc)
        else: raise RuntimeError("fixture:semantic_mutation_accepted")
        _need("physical:semantic_counter_order" in semantic_reason, "fixture:semantic_reason:" + semantic_reason)
        _need(calls["validate_terminal_checkpoint"] == 2 and
              calls["_a4_v33_validate_physical_chain"] == 2 and
              calls["ordinary_materializer"] == 2 and calls["_a4_v33_read_json"] == 2,
              "fixture:actual_route_counts")
        return {"actual_validate_calls": calls["validate_terminal_checkpoint"],
                "actual_physical_calls": calls["_a4_v33_validate_physical_chain"],
                "actual_materializer_calls": calls["ordinary_materializer"],
                "actual_read_json_calls": calls["_a4_v33_read_json"],
                "live_dual_reason": dual_reason, "semantic_reason": semantic_reason,
                "live_dual_mutation_rejected": True, "semantic_mutation_rejected": True,
                "independent_of_v25": True}


def self_test() -> None:
    result = _fixture()
    print("R07_A4_PHYSICAL_SHARD_V35_SELFTEST_PASS fixture=" +
          json.dumps(result, sort_keys=True, separators=(",", ":")))


def main() -> None:
    if "--source-patch-info" in sys.argv[1:]:
        print(json.dumps({"owner": {"path": V34[0], "bytes": V34[1], "sha256": V34[2]},
                          "owner_generated": {"bytes": V34_GENERATED[0], "sha256": V34_GENERATED[1]},
                          "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)}},
                         sort_keys=True, separators=(",", ":"))); return
    if "--self-test" in sys.argv[1:]: self_test(); return
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(_SOURCE, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__": main()
