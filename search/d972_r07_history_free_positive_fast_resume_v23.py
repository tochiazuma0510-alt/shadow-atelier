#!/usr/bin/env python3
"""A0 v23: pre-heavy replacement-worker fork over frozen v22."""
from __future__ import annotations

import hashlib
from pathlib import Path


_V22 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v22.py")
_V22_BYTES = 3280
_V22_SHA256 = "1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v23 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v23 " + label + " result cardinality")
    return result


_v22_raw = _V22.read_bytes()
if len(_v22_raw) != _V22_BYTES or hashlib.sha256(
        _v22_raw).hexdigest() != _V22_SHA256:
    raise SystemExit("v23 frozen v22 owner drift")

# Generate without running v22's production main.  The replacement owner is
# constructed and started after the light checkpoint, before build_heavy, so
# its forked children retain the light runtime while the parent builds heavy.
_v22_scope = {"__file__": str(_V22), "__name__": "_r07_v22_for_v23"}
exec(compile(_v22_raw, str(_V22), "exec"), _v22_scope, _v22_scope)
_patched = _v22_scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v23 v22 generated owner missing")

_patched = _swap(
    _patched,
    b'        self.write_checkpoint("last_safe_light_before_heavy", terminal_checkpoint=False)\n'
    b'        build_heavy(self.runtime, self.registry, self.meter)\n'
    b'        require(type(self.runtime.get("heavy_input_sha256")) is str and\n'
    b'                all(key in self.runtime for key in ("qstates", "qids", "parents",\n'
    b'                    "letters", "stores", "memberships", "emitted", "fibres")),\n'
    b'                "heavy digest publication boundary")\n'
    b'        if self.resume_expected_heavy_sha256 is not None:\n'
    b'            require(self.runtime["heavy_input_sha256"] ==\n'
    b'                    self.resume_expected_heavy_sha256,\n'
    b'                    "resumed heavy identity")\n'
    b'        self.heavy_built = True\n'
    b'        self.last_safe_phase = "heavy_complete"\n'
    b'        self.boundary = PersistentBoundaryOwner(self.runtime, self.meter,\n'
    b'                                                self.boundary.workers)\n'
    b'        self.boundary.start()\n',
    b'        self.write_checkpoint("last_safe_light_before_heavy", terminal_checkpoint=False)\n'
    b'        self.boundary = PersistentBoundaryOwner(self.runtime, self.meter,\n'
    b'                                                self.boundary.workers)\n'
    b'        self.boundary.start()\n'
    b'        build_heavy(self.runtime, self.registry, self.meter)\n'
    b'        require(type(self.runtime.get("heavy_input_sha256")) is str and\n'
    b'                all(key in self.runtime for key in ("qstates", "qids", "parents",\n'
    b'                    "letters", "stores", "memberships", "emitted", "fibres")),\n'
    b'                "heavy digest publication boundary")\n'
    b'        if self.resume_expected_heavy_sha256 is not None:\n'
    b'            require(self.runtime["heavy_input_sha256"] ==\n'
    b'                    self.resume_expected_heavy_sha256,\n'
    b'                    "resumed heavy identity")\n'
    b'        self.heavy_built = True\n'
    b'        self.last_safe_phase = "heavy_complete"\n',
    "pre-heavy replacement owner lifecycle",
)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
