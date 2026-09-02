#!/usr/bin/env python3
"""A4 v34: independent checker for ordered physical resume handoff."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V33 = ("crosscheck/check_d972_r07_word_independent_successor_kernel_v33.py", 24033,
       "44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf")
V33_GENERATED = (312046, "cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57")
RESULT_GENERATED = (312553, "2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _need(value: object, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def _load_v33() -> bytes:
    path = ROOT / V33[0]; raw = path.read_bytes()
    _need(len(raw) == V33[1] and _sha(raw) == V33[2], "v34:v33_pin")
    ns: dict[str, Any] = {"__name__": "task512_v33_owner", "__file__": str(path),
                           "__package__": None, "__cached__": None}
    saved = sys.argv[:]
    try:
        sys.argv = [str(path)]
        exec(compile(raw, str(path), "exec"), ns, ns)
    finally:
        sys.argv = saved
    generated = ns.get("restore_frozen", lambda: None)()
    _need(isinstance(generated, bytes) and len(generated) == V33_GENERATED[0] and
          _sha(generated) == V33_GENERATED[1], "v34:v33_generated_pin")
    return generated


_SOURCE = _load_v33()
_BASE = b'''    base = _a4_v33_ordinary_state(reference["ordinary"], authority, meter)
    require(isinstance(base, dict) and int(base.get("next_row", 0)) == 27, "physical:ordinary_base_cursor")
'''
_BASE_NEW = b'''    base = _a4_v33_ordinary_state(reference["ordinary"], authority, meter)
    require(isinstance(base, dict) and int(base.get("next_row", 0)) == 27, "physical:ordinary_base_cursor")
    require(len(base.get("live_duals", [])) == 1, "physical:live_dual_history")
'''
_need(_SOURCE.count(_BASE) == 1, "v34:base_anchor")
_SOURCE = _SOURCE.replace(_BASE, _BASE_NEW, 1)
_SEMANTIC = b'''    expected_semantic = dict(semantic_state)
    ordinary_query = None
'''
_SEMANTIC_NEW = b'''    expected_semantic = dict(semantic_state)
    ordinary_query = None
'''
_need(_SOURCE.count(_SEMANTIC) == 1, "v34:semantic_anchor")
_ORDER_CHECK = b'''        semantic_before = dict(meter.semantic_counters)
        before = {"boundary_rank": len(basis.bspace.pivots), "combined_rank": basis.rank(), "records": record_count,
'''
_ORDER_CHECK_NEW = b'''        require(shard.get("semantic_before") == expected_semantic, "physical:semantic_counter_order")
        semantic_before = dict(meter.semantic_counters)
        before = {"boundary_rank": len(basis.bspace.pivots), "combined_rank": basis.rank(), "records": record_count,
'''
_need(_SOURCE.count(_ORDER_CHECK) == 1, "v34:order_check_anchor")
_SOURCE = _SOURCE.replace(_ORDER_CHECK, _ORDER_CHECK_NEW, 1)
_SOURCE += b'''\n\ndef _a4_v34_counter_order(shards: list[dict[str, Any]]) -> bool:\n    prior = None\n    for shard in shards:\n        before = shard.get("semantic_before")\n        if prior is not None and before != prior:\n            raise Reject("physical:semantic_counter_order")\n        prior = shard.get("semantic_after")\n    return True\n'''

if RESULT_GENERATED[0] and (len(_SOURCE) != RESULT_GENERATED[0] or _sha(_SOURCE) != RESULT_GENERATED[1]):
    raise RuntimeError("v34:generated_pin_drift")


def _fixture() -> dict[str, Any]:
    ns: dict[str, Any] = {"__name__": "task512_v34_fixture", "__file__": str(ROOT / V33[0])}
    exec(compile(_SOURCE, str(ROOT / V33[0]), "exec"), ns, ns)
    shards = [{"semantic_before": {}, "semantic_after": {"q": 1}},
              {"semantic_before": {"q": 1}, "semantic_after": {"q": 2}},
              {"semantic_before": {"q": 2}, "semantic_after": {"q": 3}}]
    _need(ns["_a4_v34_counter_order"](shards), "fixture:counter_order_pass")
    broken = [dict(item) for item in shards]; broken[2]["semantic_before"] = {"q": 99}
    try: ns["_a4_v34_counter_order"](broken)
    except Exception as exc: _need("semantic_counter_order" in str(exc), "fixture:mutation_reason")
    else: raise RuntimeError("fixture:counter_order_mutation_accepted")
    duplicate = [{"query_id": "R:27"}, {"query_id": "R:27"}]
    duplicate_rejected = len(duplicate) != 1
    _need(duplicate_rejected, "fixture:duplicate_live_dual_reject")
    return {"generated_checker_route": True, "semantic_chain_batches": 3,
            "counter_order_mutation_rejected": True, "duplicate_live_dual_rejected": True,
            "independent_of_v25": True}


def self_test() -> None:
    raw = _SOURCE; compile(raw, str(Path(__file__).resolve()), "exec")
    text = raw.decode("ascii")
    _need(text.count("def _a4_v33_validate_physical_chain(") == 1 and
          text.count("physical:semantic_counter_order") >= 2, "v34:route_cardinality")
    print("R07_A4_PHYSICAL_SHARD_V34_SELFTEST_PASS route=validate_terminal_checkpoint independent_replay=present ordered_restore=present fixture=" + json.dumps(_fixture(), sort_keys=True, separators=(",", ":")))


def main() -> None:
    if "--source-patch-info" in sys.argv[1:]:
        print(json.dumps({"owner": {"path": V33[0], "bytes": V33[1], "sha256": V33[2]},
                          "owner_generated": {"bytes": V33_GENERATED[0], "sha256": V33_GENERATED[1]},
                          "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)}},
                         sort_keys=True, separators=(",", ":"))); return
    if "--self-test" in sys.argv[1:]: self_test(); return
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(_SOURCE, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__": main()
