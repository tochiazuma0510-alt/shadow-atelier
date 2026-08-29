#!/usr/bin/env python3
"""A0 v21: minimal actual-resume connection over the frozen v20 owner."""
from __future__ import annotations

import hashlib
from pathlib import Path


_V20 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v20.py")
_V20_BYTES = 10739
_V20_SHA256 = "cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1:
        raise SystemExit("v21 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v21 " + label + " result cardinality")
    return result


_v20_raw = _V20.read_bytes()
if len(_v20_raw) != _V20_BYTES or hashlib.sha256(
        _v20_raw).hexdigest() != _V20_SHA256:
    raise SystemExit("v21 frozen v20 owner drift")

# Generate, but do not run, v20's final frozen owner.  Its __main__ gate stays
# false in this private namespace; only the resulting source bytes are used.
_v20_scope = {"__file__": str(_V20), "__name__": "_r07_v20_for_v21"}
exec(compile(_v20_raw, str(_V20), "exec"), _v20_scope, _v20_scope)
_patched = _v20_scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v21 v20 generated owner missing")

_changes = (
    (b'    value.add_argument("--output", type=Path, required=True)\n'
     b'    value.add_argument("--seconds", type=float, required=True)',
     b'    value.add_argument("--output", type=Path, required=True)\n'
     b'    value.add_argument("--resume", type=Path)\n'
     b'    value.add_argument("--seconds", type=float, required=True)',
     "resume CLI"),
    (b"    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest\n"
     b"    if output.exists():\n",
     b"    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest\n"
     b"    resume_path = None if args.resume is None else (\n"
     b"        args.resume if args.resume.is_absolute() else ROOT / args.resume)\n"
     b"    if output.exists():\n",
     "resume path"),
    (b"        search = Search(runtime, registry, source_public, old_value, reducer, p_rows,\n"
     b"                        triangular, meter, output, args.workers, selftest)\n"
     b"        receipt = search.run()\n",
     b"        search = Search(runtime, registry, source_public, old_value, reducer, p_rows,\n"
     b"                        triangular, meter, output, args.workers, selftest,\n"
     b"                        defer_owner_start=resume_path is not None)\n"
     b"        if resume_path is not None:\n"
     b"            restore_checkpoint(search, resume_path)\n"
     b"        receipt = search.run()\n",
     "single restore call"),
)
for _old, _new, _label in _changes:
    _patched = _swap(_patched, _old, _new, _label)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
