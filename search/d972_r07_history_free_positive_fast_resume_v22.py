#!/usr/bin/env python3
"""A0 v22: terminal-checkpoint accounting repair over frozen v21."""
from __future__ import annotations

import hashlib
from pathlib import Path


_V21 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v21.py")
_V21_BYTES = 3035
_V21_SHA256 = "18aef3a1619b076b32002a9083ba9763116d984b761b7f8d181059293dbdf1fd"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v22 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v22 " + label + " result cardinality")
    return result


_v21_raw = _V21.read_bytes()
if len(_v21_raw) != _V21_BYTES or hashlib.sha256(
        _v21_raw).hexdigest() != _V21_SHA256:
    raise SystemExit("v22 frozen v21 owner drift")

# Generate without running v21's production main.  All arithmetic, search,
# worker, cleanup and resume code remains byte-for-byte v21 except the two
# checkpoint counter sites below.
_v21_scope = {"__file__": str(_V21), "__name__": "_r07_v21_for_v22"}
exec(compile(_v21_raw, str(_V21), "exec"), _v21_scope, _v21_scope)
_patched = _v21_scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v22 v21 generated owner missing")

_changes = (
    (
        b'        self.meter.bump("serialized_dag_bytes", estimated_json_size(checkpoint_body),\n'
        b'                        "checkpoint_serialization")\n',
        b'        serialized_estimate = estimated_json_size(checkpoint_body)\n'
        b'        serialized_total = (self.meter.counters["serialized_dag_bytes"] +\n'
        b'                            serialized_estimate)\n'
        b'        if serialized_total > self.meter.limits["serialized_dag_bytes"]:\n'
        b'            raise ResourceStop("checkpoint_serialization",\n'
        b'                               "serialized_dag_bytes", serialized_total,\n'
        b'                               self.meter.limits["serialized_dag_bytes"])\n'
        b'        self.meter.commit("serialized_dag_bytes", serialized_estimate)\n',
        "live terminal serialization bookkeeping",
    ),
    (
        b'    meter.bump("serialized_dag_bytes", estimated_json_size(body),\n'
        b'               "checkpoint_serialization")\n',
        b'    serialized_estimate = estimated_json_size(body)\n'
        b'    serialized_total = (meter.counters["serialized_dag_bytes"] +\n'
        b'                        serialized_estimate)\n'
        b'    if serialized_total > meter.limits["serialized_dag_bytes"]:\n'
        b'        raise ResourceStop("checkpoint_serialization",\n'
        b'                           "serialized_dag_bytes", serialized_total,\n'
        b'                           meter.limits["serialized_dag_bytes"])\n'
        b'    meter.commit("serialized_dag_bytes", serialized_estimate)\n',
        "prepool terminal serialization bookkeeping",
    ),
)
for _old, _new, _label in _changes:
    _patched = _swap(_patched, _old, _new, _label)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
