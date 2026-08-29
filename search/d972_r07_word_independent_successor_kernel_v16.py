#!/usr/bin/env python3
"""A4 v16 producer: v15 with compact live-basis storage and v24 checkpoints.

The row order, canonical pivots, complete ancestry and examined-candidate cap
are inherited byte-for-byte from v15.  The live echelon columns are stored as
pooled packed sparse rows (uint32 key ids plus uint8 coefficients), active-key
membership is pooled, and insertion events retain only the lossless owner
identity needed by the chronological restore replay.  Checkpoints written by
this owner use the v24 schema; the immediately preceding v1 checkpoint is
accepted as a one-way resume migration so the durable next_row=25 artifact can
continue without redoing completed rows.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v15.py")
OWNER_BYTES = 7417
OWNER_SHA256 = "964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7"
OWNER_GENERATED_BYTES = 226857
OWNER_GENERATED_SHA256 = "fe3c23ffb4c5c952f99eceba73cb8594885dbadd9d2c4bd50d8b28c173e46940"
RESULT_GENERATED_BYTES = 232872
RESULT_GENERATED_SHA256 = "01aaff4b64d39b8f56569d079b10df2dc12657a6a7c4a7cefb7449241d303863"

PACKED_BASIS_BLOCK = b'''\
\nclass _SparseKeyPool:
    """Intern row keys once; packed rows retain uint32 ids, not key objects."""
    __slots__ = ("ids", "values")

    def __init__(self):
        self.ids: dict[str, int] = {}
        self.values: list[str] = []

    def intern(self, key: str) -> int:
        require(type(key) is str, "packed:key_type")
        found = self.ids.get(key)
        if found is not None:
            return found
        ident = len(self.values)
        require(ident < 0xFFFFFFFF, "packed:key_pool_cap")
        self.ids[key] = ident; self.values.append(key)
        return ident

    def lookup(self, key: str) -> int:
        return self.ids.get(key, -1)


def _packed_pool_for(meter: Any) -> _SparseKeyPool:
    pool = getattr(meter, "_a4_sparse_key_pool", None)
    if pool is None:
        pool = _SparseKeyPool(); meter._a4_sparse_key_pool = pool
    return pool


class _PackedRow:
    """Immutable mod-3 sparse row: sorted uint32 ids and uint8 values."""
    __slots__ = ("pool", "keys", "values")

    def __init__(self, pool: _SparseKeyPool, keys: Any, values: Any):
        self.pool, self.keys, self.values = pool, keys, values

    @classmethod
    def from_dict(cls, row: dict[str, int], pool: _SparseKeyPool) -> "_PackedRow":
        pairs = []
        for key, value in row.items():
            coefficient = int(value) % 3
            if coefficient:
                pairs.append((pool.intern(key), coefficient))
        pairs.sort(key=lambda item: item[0])
        require(all(index > 0 or index == 0 for index, _ in pairs), "packed:key_id")
        return cls(pool, array("I", (index for index, _ in pairs)),
                   bytearray(value for _, value in pairs))

    def __len__(self) -> int:
        return len(self.keys)

    def __bool__(self) -> bool:
        return bool(self.keys)

    def __iter__(self):
        return (self.pool.values[index] for index in self.keys)

    def items(self):
        return ((self.pool.values[index], int(value))
                for index, value in zip(self.keys, self.values))

    def get(self, key: str, default: int = 0) -> int:
        index = self.pool.lookup(key)
        if index < 0:
            return default
        lo = 0; hi = len(self.keys)
        while lo < hi:
            mid = (lo + hi) // 2
            probe = self.keys[mid]
            if probe < index: lo = mid + 1
            else: hi = mid
        if lo < len(self.keys) and self.keys[lo] == index:
            return int(self.values[lo])
        return default

    def __contains__(self, key: str) -> bool:
        return self.get(key, 0) != 0

    def to_dict(self) -> dict[str, int]:
        return {key: value for key, value in self.items()}

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, _PackedRow):
            return self.to_dict() == other.to_dict()
        if isinstance(other, dict):
            return self.to_dict() == other
        return NotImplemented


class _PackedKeySet:
    """Set-like active registry backed by pooled integer ids."""
    __slots__ = ("pool", "ids")

    def __init__(self, pool: _SparseKeyPool):
        self.pool, self.ids = pool, set()

    def update(self, keys: Any) -> None:
        for key in keys:
            self.ids.add(self.pool.intern(key))

    def __contains__(self, key: str) -> bool:
        index = self.pool.lookup(key)
        return index >= 0 and index in self.ids

    def __len__(self) -> int:
        return len(self.ids)

    def __iter__(self):
        return (self.pool.values[index] for index in self.ids)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, _PackedKeySet):
            return self.ids == other.ids
        if isinstance(other, (set, list, tuple)):
            return len(self) == len(other) and all(key in self for key in other)
        return NotImplemented


def _canonicalize_compact(value: Any) -> Any:
    packed = globals().get("_PackedRow")
    if packed is not None and isinstance(value, packed):
        return value.to_dict()
    if isinstance(value, dict):
        return {key: _canonicalize_compact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_canonicalize_compact(item) for item in value]
    if isinstance(value, tuple):
        return [_canonicalize_compact(item) for item in value]
    if isinstance(value, set):
        return sorted(_canonicalize_compact(item) for item in value)
    return value
'''

PATCHES = (
    (
        b'from __future__ import annotations\n\nimport argparse',
        b'from __future__ import annotations\n\nfrom array import array\nimport argparse',
    ),
    (
        b'''def canon(value: Any) -> bytes:\n    return json.dumps(value, sort_keys=True, separators=(",", ":"),''',
        b'''def canon(value: Any) -> bytes:\n    return json.dumps(_canonicalize_compact(value), sort_keys=True, separators=(",", ":"),''',
    ),
    (
        b'''def jsonable(value: Any) -> Any:\n    if isinstance(value, bytes):''',
        b'''def jsonable(value: Any) -> Any:\n    packed = globals().get("_PackedRow")\n    if packed is not None and isinstance(value, packed):\n        return value.to_dict()\n    if isinstance(value, bytes):''',
    ),
    (
        b'''class Echelon:\n''',
        PACKED_BASIS_BLOCK + b'''\n\nclass Echelon:\n''',
    ),
    (
        b'''    def __init__(self, meter: Meter):\n        self.meter = meter; self.rows: dict[str, dict[str, int]] = {}; self.labels: dict[str, str] = {}''',
        b'''    def __init__(self, meter: Meter):\n        self.meter = meter; self._pool = _packed_pool_for(meter); self.rows: dict[str, dict[str, int]] = {}; self.labels: dict[str, str] = {}''',
    ),
    (
        b'''        stored = scale_row(rem, scale); self.rows[pivot] = stored; self.labels[pivot] = label''',
        b'''        stored = _PackedRow.from_dict(scale_row(rem, scale), self._pool); self.rows[pivot] = stored; self.labels[pivot] = label''',
    ),
    (
        b'''        self.active_registry: set[str] = set()''',
        b'''        self.active_registry = _PackedKeySet(_packed_pool_for(meter))''',
    ),
    (
        b'''        self.insertion_events.append({"kind": "B", "label": label, "column": column,\n                                      "raw_identity": raw_identity, "boundary_row": stored,\n                                      "combined_row": cdetail["row"], "boundary_pivot": pivot,\n                                      "boundary_scale": scale, "boundary_reduction": correction,\n                                      "combined_detail": cdetail})''',
        b'''        # The column and both echelon details are deterministically replayed\n        # from raw_identity; retaining them here made each B insertion several\n        # more dict-of-dicts copies.\n        self.insertion_events.append({"kind": "B", "label": label,\n                                      "raw_identity": raw_identity})''',
    ),
    (
        b'''        self.insertion_events.append({"kind": "K", "label": label, "row": row,\n                                      "combined_detail": detail})''',
        b'''        # K_roster owns the lossless normalized row and recurrence ancestry;\n        # the chronological event needs only its owner label.\n        self.insertion_events.append({"kind": "K", "label": label})''',
    ),
    (
        b'''    active = set(target) | set(basis.active_registry)\n    free = min(remainder); dual: dict[str, int] = {free: 1}''',
        b'''    # Do not copy the million-key registry for every dual pullback.\n    active = basis.active_registry\n    free = min(remainder); dual: dict[str, int] = {free: 1}''',
    ),
    (
        b'''    require(set(dual) <= active, "dual:active_registry")''',
        b'''    require(all(key in target or key in active for key in dual),\n            "dual:active_registry")''',
    ),
    (
        b'''    derived_active: set[str] = set()''',
        b'''    derived_active = _PackedKeySet(_packed_pool_for(basis.meter))''',
    ),
    (
        b'''            bdetail = rebuilt_boundary.insert(event.get("column", {}), label)\n            require(bdetail is not None and bdetail.get("pivot") == event.get("boundary_pivot") and\n                    bdetail.get("scale") == event.get("boundary_scale") and\n                    bdetail.get("row") == event.get("boundary_row") and\n                    bdetail.get("reduction") == event.get("boundary_reduction"),\n                    "checkpoint:boundary_event_replay")\n            cdetail = rebuilt_combined.insert(event.get("boundary_row", {}), label)\n            require(cdetail is not None and cdetail == event.get("combined_detail") and\n                    event.get("combined_row") == cdetail.get("row"),\n                    "checkpoint:combined_boundary_event_replay")''',
        b'''            event_column = event.get("column")\n            if event_column is None:\n                event_column = basis.ledger.psi({event["raw_identity"]: 1})\n            bdetail = rebuilt_boundary.insert(event_column, label)\n            require(bdetail is not None, "checkpoint:boundary_event_replay")\n            event_boundary_row = event.get("boundary_row", bdetail.get("row"))\n            event_boundary_reduction = event.get("boundary_reduction", bdetail.get("reduction"))\n            require(bdetail.get("pivot") == event.get("boundary_pivot", bdetail.get("pivot")) and\n                    bdetail.get("scale") == event.get("boundary_scale", bdetail.get("scale")) and\n                    bdetail.get("row") == event_boundary_row and\n                    bdetail.get("reduction") == event_boundary_reduction,\n                    "checkpoint:boundary_event_replay")\n            cdetail = rebuilt_combined.insert(event_boundary_row, label)\n            event_combined_detail = event.get("combined_detail")\n            require(cdetail is not None and\n                    (event_combined_detail is None or cdetail == event_combined_detail) and\n                    (event.get("combined_row") is None or event.get("combined_row") == cdetail.get("row")),\n                    "checkpoint:combined_boundary_event_replay")''',
    ),
    (
        b'''            require(basis.ledger.psi({event["raw_identity"]: 1}) == event.get("column"),\n                    "checkpoint:boundary_raw_identity")''',
        b'''            require(basis.ledger.psi({event["raw_identity"]: 1}) == event_column,\n                    "checkpoint:boundary_raw_identity")''',
    ),
    (
        b'''            item = saved_by_label[label]; cdetail = rebuilt_combined.insert(event.get("row", {}), label)\n            require(cdetail is not None and cdetail == event.get("combined_detail") and\n                    item.get("row") == cdetail.get("row") and''',
        b'''            item = saved_by_label[label]\n            event_row = event.get("row", item.get("row", {}))\n            cdetail = rebuilt_combined.insert(event_row, label)\n            event_combined_detail = event.get("combined_detail")\n            require(cdetail is not None and\n                    (event_combined_detail is None or cdetail == event_combined_detail) and\n                    item.get("row") == cdetail.get("row") and''',
    ),
    (
        b'''    require(value.get("schema") == SCHEMA + "/checkpoint/v1" and value.get("authority") == authority.identity and\n            value.get("owner") == "producer" and\n            value.get("code_sha256") == sha(Path(__file__).read_bytes()), "checkpoint:identity")''',
        b'''    checkpoint_schema = value.get("schema"); checkpoint_code_sha = value.get("code_sha256")\n    require(checkpoint_schema in (CHECKPOINT_SCHEMA, LEGACY_CHECKPOINT_SCHEMA) and\n            value.get("authority") == authority.identity and value.get("owner") == "producer" and\n            checkpoint_code_sha == (LEGACY_PRODUCER_CODE_SHA256 if\n                                    checkpoint_schema == LEGACY_CHECKPOINT_SCHEMA else\n                                    sha(Path(__file__).read_bytes())), "checkpoint:identity")''',
    ),
    (
        b'''        require(claimed == digest(body) and value.get("schema") == SCHEMA + "/checkpoint/v1" and\n                value.get("owner") == "producer" and isinstance(value.get("code_sha256"), str) and''',
        b'''        require(claimed == digest(body) and\n                value.get("schema") in (CHECKPOINT_SCHEMA, LEGACY_CHECKPOINT_SCHEMA) and\n                value.get("owner") == "producer" and isinstance(value.get("code_sha256"), str) and''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v16 producer: frozen v15 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v15_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if (len(raw) != OWNER_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256):
        raise SystemExit("v16 producer: frozen v15 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v16 producer: audited site is not unique")
        raw = raw.replace(old, new)
    schema_old = b'SCHEMA = "d972-r07-word-independent-successor-kernel/v6"\n'
    schema_new = (b'SCHEMA = "d972-r07-word-independent-successor-kernel/v6"\n'
                 b'CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v24"\n'
                 b'LEGACY_CHECKPOINT_SCHEMA = "d972-r07-word-independent-successor-kernel/v6/checkpoint/v1"\n'
                 b'LEGACY_PRODUCER_CODE_SHA256 = "964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7"\n')
    if raw.count(schema_old) != 1:
        raise SystemExit("v16 producer: checkpoint schema anchor is not unique")
    raw = raw.replace(schema_old, schema_new)
    checkpoint_expr = b'SCHEMA + "/checkpoint/v1"'
    if raw.count(checkpoint_expr) != 2:
        raise SystemExit("v16 producer: checkpoint schema occurrence drift")
    raw = raw.replace(checkpoint_expr, b"CHECKPOINT_SCHEMA")
    if (len(raw) != RESULT_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256):
        raise SystemExit("v16 producer: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(OWNER), "exec"), ns, ns)


if __name__ == "__main__":
    main()
