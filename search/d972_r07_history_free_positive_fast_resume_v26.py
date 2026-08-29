#!/usr/bin/env python3
"""A0 v26: two-phase streamed restore over the frozen v25 key repair."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

_V25 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v25.py")
_V25_BYTES = 3870
_V25_SHA256 = "8aad1fb0eb0f00e63ffe59d33f71bb89f65a63731084b668f10be587ba343460"
_V13 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v13.py")
_V13_BYTES = 147409
_V13_SHA256 = "4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a"


def _swap(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v26 " + label + " source cardinality")
    result = source.replace(old, new, 1)
    if len(result) != len(source) - len(old) + len(new) or result.count(new) != 1:
        raise SystemExit("v26 " + label + " result cardinality")
    return result


_raw = _V25.read_bytes()
if len(_raw) != _V25_BYTES or hashlib.sha256(_raw).hexdigest() != _V25_SHA256:
    raise SystemExit("v26 frozen v25 owner drift")
_scope = {"__file__": str(_V25), "__name__": "_r07_v25_for_v26"}
exec(compile(_raw, str(_V25), "exec"), _scope, _scope)
_patched = _scope.get("_patched")
if type(_patched) is not bytes:
    raise SystemExit("v26 v25 generated owner missing")

_patched = _swap(_patched,
    b'def _stream_prepare(search, value):',
    b'def _stream_pre_records(search, value):',
    "pre-record phase name")
_patched = _swap(_patched,
    b'            prior_boundary.get("cleanup", {}).get("complete") is True and\n'
    b'            prior_boundary["cleanup"].get("live_pids_after_join") == [] and\n'
    b'            type(value.get("next_clean_boundary_epoch")) is int and value["next_clean_boundary_epoch"] >= 1,\n'
    b'            "v7 clean boundary resume owner")',
    b'            prior_boundary.get("cleanup", {}).get("complete") is True and\n'
    b'            prior_boundary["cleanup"].get("live_pids_after_join") == [],\n'
    b'            "v7 clean boundary pre-record owner")',
    "defer unread epoch")
_patched = _swap(_patched,
    b'    search.boundary.accounting = restored; search.boundary.epoch = int(value["next_clean_boundary_epoch"]) - 1\n',
    b'    search.boundary.accounting = restored\n',
    "pre-record accounting only")
_POST = b'''def _stream_post_parse(search, value):
    prior_boundary = value.get("boundary_owner")
    require(type(prior_boundary) is dict and
            type(value.get("next_clean_boundary_epoch")) is int and
            value["next_clean_boundary_epoch"] >= 1,
            "v26 post-parse boundary epoch")
    search.boundary.epoch = int(value["next_clean_boundary_epoch"]) - 1


'''
_patched = _swap(_patched,
    b'def _stream_record(search, record):',
    _POST + b'def _stream_record(search, record):',
    "post-parse phase insertion")
_patched = _swap(_patched,
    b'                            _stream_prepare(search, value); prepared = True',
    b'                            _stream_pre_records(search, value); prepared = True',
    "nonempty pre-record restore")
_patched = _swap(_patched,
    b'        require(prepared or ("new_records" in value and (_stream_prepare(search, value) or True)),\n'
    b'                "resume prepare")\n'
    b'        live = search.runtime["live"]; checkpoint_source = value.get("source")',
    b'        require("new_records" in value, "resume new_records ownership")\n'
    b'        if not prepared:\n'
    b'            _stream_pre_records(search, value); prepared = True\n'
    b'        _stream_post_parse(search, value)\n'
    b'        live = search.runtime["live"]; checkpoint_source = value.get("source")',
    "empty/nonempty two-phase restore")

_tree = ast.parse(_patched.decode("ascii"))
_names = {node.name for node in _tree.body if isinstance(node, ast.FunctionDef)}
if not {"_stream_pre_records", "_stream_post_parse", "_stream_resume"} <= _names:
    raise SystemExit("v26 two-phase function ownership")
if b'_stream_prepare' in _patched:
    raise SystemExit("v26 stale one-phase restore")
_search = next(node for node in _tree.body
               if isinstance(node, ast.ClassDef) and node.name == "Search")
_body = next(node for node in _search.body
             if isinstance(node, ast.FunctionDef) and node.name == "checkpoint_body")
_returns = [node for node in ast.walk(_body)
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict)]
_checkpoint_keys = tuple(sorted(
    tuple(key.value for key in _returns[0].value.keys) + ("self_digest",)))
_transport = next(node for node in _tree.body if isinstance(node, ast.Assign) and
                  any(isinstance(target, ast.Name) and target.id == "_RESUME_TOP_KEYS"
                      for target in node.targets))
_v13_raw = _V13.read_bytes()
if len(_v13_raw) != _V13_BYTES or hashlib.sha256(_v13_raw).hexdigest() != _V13_SHA256:
    raise SystemExit("v26 frozen v13 checkpoint owner drift")
_v13_tree = ast.parse(_v13_raw.decode("ascii"))
_v13_search = next(node for node in _v13_tree.body
                   if isinstance(node, ast.ClassDef) and node.name == "Search")
_v13_body = next(node for node in _v13_search.body
                 if isinstance(node, ast.FunctionDef) and node.name == "checkpoint_body")
_v13_returns = [node for node in ast.walk(_v13_body)
                if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict)]
_v13_keys = tuple(sorted(
    tuple(key.value for key in _v13_returns[0].value.keys) + ("self_digest",)))
if (len(_returns) != 1 or len(_v13_returns) != 1 or
        tuple(ast.literal_eval(_transport.value)) != _checkpoint_keys or
        _checkpoint_keys != _v13_keys):
    raise SystemExit("v26 checkpoint-body/transport exact key gate")

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
