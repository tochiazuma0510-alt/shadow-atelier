#!/usr/bin/env python3
"""A0 v25: exact checkpoint-key repair over the frozen streaming v24."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_V24 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v24.py")
_V24_BYTES = 16956
_V24_SHA256 = "b151b6c858de556145bc58b13037ea8b193f068a93c3d0383c1769613c3cea74"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v25 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v25 " + label + " result cardinality")
    return result


def _checkpoint_keys(source: bytes) -> tuple[str, ...]:
    tree = ast.parse(source.decode("ascii"))
    search = next(node for node in tree.body
                  if isinstance(node, ast.ClassDef) and node.name == "Search")
    body = next(node for node in search.body
                if isinstance(node, ast.FunctionDef) and node.name == "checkpoint_body")
    returns = [node for node in ast.walk(body)
               if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict)]
    if len(returns) != 1:
        raise SystemExit("v25 checkpoint_body return cardinality")
    keys = tuple(key.value for key in returns[0].value.keys
                 if isinstance(key, ast.Constant) and type(key.value) is str)
    if len(keys) != len(returns[0].value.keys) or len(keys) != len(set(keys)):
        raise SystemExit("v25 checkpoint_body literal key ownership")
    return tuple(sorted(keys + ("self_digest",)))


_v24_raw = _V24.read_bytes()
if len(_v24_raw) != _V24_BYTES or hashlib.sha256(_v24_raw).hexdigest() != _V24_SHA256:
    raise SystemExit("v25 frozen v24 owner drift")
_scope = {"__file__": str(_V24), "__name__": "_r07_v24_for_v25"}
exec(compile(_v24_raw, str(_V24), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v25 v24 generated owner missing")

_EXPECTED = ("P_rows", "P_rows_sha256", "boundary_owner", "claims",
    "coefficient_solution_node_ids", "correction_progress", "current_dual",
    "current_dual_sha256", "exact_cached_resume", "formal_ancestry",
    "formal_ancestry_sha256", "heavy_complete", "heavy_input_sha256",
    "heavy_rebuild_frontier", "heavy_reconstructible", "heuristic_discovery_only",
    "last_safe_phase", "light_input_sha256", "monitor", "new_records",
    "next_clean_boundary_epoch", "phase", "remainder", "schema", "self_digest",
    "selftest", "solution_node_id", "source", "source_snapshots", "target",
    "target_node_id", "triangular_certificate")
if _checkpoint_keys(_patched) != _EXPECTED:
    raise SystemExit("v25 frozen checkpoint-body/top-level key drift")

_patched = _swap(
    _patched,
    b'    "last_safe_phase", "light_input_sha256", "monitor", "new_records", "phase",\n'
    b'    "remainder", "schema", "self_digest", "selftest", "solution_node_id",',
    b'    "last_safe_phase", "light_input_sha256", "monitor", "new_records",\n'
    b'    "next_clean_boundary_epoch", "phase", "remainder", "schema", "self_digest",\n'
    b'    "selftest", "solution_node_id",',
    "streaming canonical top-level keys",
)

_tree = ast.parse(_patched.decode("ascii"))
_assignments = [node for node in _tree.body if isinstance(node, ast.Assign) and
                any(isinstance(target, ast.Name) and target.id == "_RESUME_TOP_KEYS"
                    for target in node.targets)]
if len(_assignments) != 1 or tuple(ast.literal_eval(_assignments[0].value)) != _EXPECTED:
    raise SystemExit("v25 generated transport key gate")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
