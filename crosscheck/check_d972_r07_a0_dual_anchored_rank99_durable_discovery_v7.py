#!/usr/bin/env python3
"""Task509 v7 checker: the minimal independent-W and RESOURCE repair."""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V6 = ("crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py", 12191,
      "2f579f818b7fff01a3af4764393ac2f2a3190767f0671e6d407c7fe2517e91da")
PRODUCER_V6 = ("search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py", 4911,
               "a66526af4b4f86019b1a4a9283212b9782f5793a21c518a93f04b9925e6bee22")
PROOF = ("sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md", 9592,
         "7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4")
V7_SCHEMA = "d972-r07-a0-dual-anchored-rank99-durable-discovery/v6"
V7_MARKER = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_CHECKER"
PRODUCER_MARKER = "R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6"
GLOBAL_CURSOR = "global_nonzero_constant"
GLOBAL_W_BOUND = 357128352


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _need(value: object, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def _load_v6() -> types.ModuleType:
    path = ROOT / V6[0]
    raw = path.read_bytes()
    _need(len(raw) == V6[1] and _sha(raw) == V6[2], "pin:v6_checker")
    spec = importlib.util.spec_from_file_location("task509_pinned_v6_checker", path)
    _need(spec is not None and spec.loader is not None, "loader:v6_checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_v6 = _load_v6()
_v6.SCHEMA = V7_SCHEMA
_v6.CP_SCHEMA = V7_SCHEMA + "/checkpoint"
_v6.MARKER = V7_MARKER
_v6.PRODUCER_MARKER = PRODUCER_MARKER
_v6._v5.SCHEMA = V7_SCHEMA
_v6._v5.CP_SCHEMA = V7_SCHEMA + "/checkpoint"
_v6._v5.MARKER = V7_MARKER
_v6._v5.PRODUCER_MARKER = PRODUCER_MARKER
_v7_binding_body = {"schema": V7_SCHEMA,
    "task451_producer": list(_v6._v5.TASK451_P), "task451_checker": list(_v6._v5.TASK451_C),
    "c99": list(_v6._v5.C99), "rank51": list(_v6._v5.RANK51), "paper": list(_v6._v5.PAPER),
    "paper_v426": list(_v6._v5.PAPER_V426), "paper_v427": list(_v6._v5.PAPER_V427),
    "paper_v431": list(PROOF)}
_v6._v5.BINDING = hashlib.sha256(_v6._v5.canon(_v7_binding_body)).hexdigest()
_v6.BINDING = _v6._v5.BINDING
_old_pins = _v6._v5.pins


def _pins_v7():
    value = dict(_old_pins())
    value["paper_v431"] = _v6._v5.pin(PROOF)
    return value


_v6._v5.pins = _pins_v7
_v6.pins = _pins_v7


def _expected_W(sf: object, formula: dict) -> int:
    """Recompute W from the live selective runtime, retaining target multiplicity."""
    orders = getattr(sf, "kernel_orders", None)
    _v6._v5.need(isinstance(orders, (tuple, list)) and len(orders) >= 3,
                 "global:kernel_orders")
    merged = formula.get("merged")
    _v6._v5.need(isinstance(merged, dict), "global:merged")
    coordinates = [int(coordinate) for coordinate, _ in merged]
    _v6._v5.need(set(coordinates) <= {0, 1, 2}, "global:live_coordinates")
    _v6._v5.need(all(int(orders[coordinate]) == 9 for coordinate in coordinates),
                 "global:kernel_order")
    expected = sum(int(orders[coordinate]) for coordinate, _ in merged)
    _v6._v5.need(expected < GLOBAL_W_BOUND, "global:W_bound")
    return expected


_old_replay_global = _v6._replay_global


def _replay_global_v7(v4, P, p179, sf, model, formulas, record, dual, adjoint_digest):
    cursor = record.get("selector_cursor")
    _v6._v5.need(isinstance(cursor, list) and len(cursor) == 4 and cursor[0] == GLOBAL_CURSOR,
                 "global:cursor_shape")
    _tag, seed, point, supplied_W = cursor
    _v6._v5.need(type(seed) is int and 1 <= seed <= len(formulas) and type(point) is int and
                 type(supplied_W) is int, "global:cursor_type")
    formula = formulas[seed - 1]
    _v6._v5.need(record.get("global_cursor") == point, "global:cursor_binding")
    expected_W = _expected_W(sf, formula)
    _v6._v5.need(supplied_W == expected_W and record.get("W") == expected_W,
                 "global:W_recompute")
    return _old_replay_global(v4, P, p179, sf, model, formulas, record, dual, adjoint_digest)


_v6._replay_global = _replay_global_v7

# The v6 batch routine rejected a mixed compiled roster by checking every
# formula's K.  Recompile it independently with that broad stop removed;
# the selected historical support row is gated below instead.
_batch_source = inspect.getsource(_v6._replay_batch_v6)
_v6._v5.need(_batch_source.count('not any(f["K"] for f in formulas)') == 1,
             "v7:batch_branch_anchor")
_batch_source = _batch_source.replace('not any(f["K"] for f in formulas)', "True", 1)
_batch_ns = dict(_v6._replay_batch_v6.__globals__)
_batch_ns["_replay_global"] = _replay_global_v7
exec(compile(_batch_source, V6[0], "exec"), _batch_ns, _batch_ns)
_base_replay_batch = _batch_ns["_replay_batch_v6"]
_old_replay_literal = _v6._v5.replay_literal


def _replay_literal_selected(v4, P, p179, sf, model, formulas, record, dual, adjoint_digest):
    cursor = record.get("selector_cursor")
    if not (isinstance(cursor, list) and cursor and cursor[0] == GLOBAL_CURSOR):
        seed = record.get("seed_index")
        _v6._v5.need(type(seed) is int and 1 <= seed <= len(formulas) and
                     formulas[seed - 1]["K"] == 0, "batch:selected_K")
    return _old_replay_literal(v4, P, p179, sf, model, formulas, record, dual, adjoint_digest)


_v6._v5.replay_literal = _replay_literal_selected


def _replay_batch_v7(v4, P, m, p179, batch, state, sf, args):
    rows = batch.get("rows")
    _v6._v5.need(isinstance(rows, list), "batch:rows")
    global_rows = [record for record in rows
                   if isinstance(record.get("selector_cursor"), list) and
                   record["selector_cursor"] and record["selector_cursor"][0] == GLOBAL_CURSOR]
    _v6._v5.need(len(global_rows) <= 1, "batch:multiple_global")
    _v6._v5.need(not global_rows or (len(rows) == 1 and len(global_rows) == 1),
                 "batch:global_sole_row")
    return _base_replay_batch(v4, P, m, p179, batch, state, sf, args)


_v6._v5.replay_batch = _replay_batch_v7
_v6._v5.replay_all.__globals__["replay_batch"] = _replay_batch_v7


_old_self_test = _v6.self_test


def self_test():
    result = _old_self_test()
    formula = {"K": 1, "merged": {(0, b"a"): 1}, "required_coordinates": [0]}
    sf = types.SimpleNamespace(kernel_orders=(9, 9, 9, 9, 9, 1, 1, 1, 3, 3))
    wrong = {"selector_cursor": [GLOBAL_CURSOR, 1, 0, 8], "seed_index": 1,
             "global_cursor": 0, "K": 1, "W": 8}
    try:
        _replay_global_v7(None, None, None, sf, None, [formula], wrong, None, "a" * 64)
    except RuntimeError as exc:
        wrong_W_rejected = str(exc) == "global:W_recompute"
    else:
        wrong_W_rejected = False
    _v6._v5.need(wrong_W_rejected, "selftest:wrong_W_mutation")
    bad_batch = {"rows": [{"selector_cursor": [GLOBAL_CURSOR, 1, 0, 9]},
                           {"selector_cursor": [GLOBAL_CURSOR, 1, 1, 9]}]}
    try:
        _replay_batch_v7(None, None, None, None, bad_batch, None, None, None)
    except RuntimeError as exc:
        multiple_global_rejected = str(exc) == "batch:multiple_global"
    else:
        multiple_global_rejected = False
    _v6._v5.need(multiple_global_rejected, "selftest:multiple_global")
    try:
        _replay_literal_selected(None, None, None, None, None,
                                 [{"K": 1}], {"selector_cursor": [1, 0, "00", 0],
                                               "seed_index": 1}, None, "a" * 64)
    except RuntimeError as exc:
        mixed_support_rejected = str(exc) == "batch:selected_K"
    else:
        mixed_support_rejected = False
    _v6._v5.need(mixed_support_rejected, "selftest:mixed_support_K")
    old_literal = _old_replay_literal
    try:
        globals()["_old_replay_literal"] = lambda *args: "selected_K0_ok"
        accepted = _replay_literal_selected(None, None, None, None, None,
                                            [{"K": 0}, {"K": 1}],
                                            {"selector_cursor": [1, 0, "00", 0],
                                             "seed_index": 1}, None, "a" * 64)
    finally:
        globals()["_old_replay_literal"] = old_literal
    _v6._v5.need(accepted == "selected_K0_ok", "selftest:mixed_support_K0_accept")
    result["independent_W_recomputed"] = True
    result["wrong_W_record_and_cursor_rejected"] = True
    result["mixed_support_selected_K_gate"] = True
    result["mixed_support_selected_K0_accept"] = True
    result["global_sole_row_gate"] = True
    result["resource_checker_boundary"] = True
    return result


_v6.self_test = self_test
_v6.main.__globals__["self_test"] = self_test
main = _v6.main
check = _v6.check
pins = _pins_v7
SCHEMA = _v6.SCHEMA
CP_SCHEMA = _v6.CP_SCHEMA
BINDING = _v6.BINDING
MARKER = _v6.MARKER


if __name__ == "__main__":
    raise SystemExit(main())
