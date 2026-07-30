#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-native-registry.py

Receiver-held native-artifact registry (Sol 便88 P88-o / F88-3.2,
sol/sol_reply_88_math15.md; docs/notes/cert_shape_interpretation_addendum_o_v8.md).

裁定239 §3 / Sol 便88 finding: 便87's v7 closed the unresolved-pointer
fallback attack, but left the receiver unable to distinguish "native_a/
native_b are the artifacts the receiver actually pinned ahead of time"
from "native_a/native_b are whatever a caller attached to this one raw
JSON blob" -- a producer who replaces certificate+native_a+native_b
wholesale, self-consistently, still reached PASS (F88-3.2's literal
probe). `native_registry_status` in search/ninfty-evidence-union.py was
an honest but NON-GATING "UNKNOWN" annotation; P88-o requires an actual
receiver-held registry that GATES overall PASS.

THIS MODULE IS THE PHYSICAL TRUST BOUNDARY. It is a plain file store,
entirely separate from any `raw` evidence artifact a caller supplies to
search/ninfty-evidence-union.py:

  * `resolve(artifact_id)` reads ONLY from files under REGISTRY_DIR
    (search/certs/ep_registry/), located via this module's OWN file path
    (`os.path.dirname(__file__)`), NEVER from any value inside a caller's
    `raw` blob. A caller can hand this module's consuming code (evidence-
    union.py) an arbitrarily forged `raw["native_a"]`/`raw["native_b"]` --
    that forged content is never written here and never read back by
    `resolve`.
  * `write_entry(...)` is the ONLY way content enters the registry -- an
    explicit, receiver-side PROVISIONING call (used by this project's own
    test setup / a future operator tool), never invoked as part of
    processing untrusted `raw` evidence. search/ninfty-evidence-union.py
    does not import `write_entry` at all (grep-verifiable: it only calls
    `resolve`).
  * every artifact's `whole_artifact_digest` returned by `resolve` is
    FRESHLY RECOMPUTED from the entry file's own `content` field on every
    call (never trusted from the index's cached copy, never trusted from
    any caller claim) -- a receiver-side integrity check, defense in
    depth against a corrupted or hand-edited registry file.
  * artifact_id -> filename mapping is DERIVED (sha256 of a canonical
    wrapper around artifact_id), never the artifact_id string used
    directly as a path component -- closes path-traversal by construction
    even though artifact_id in this codebase is always receiver-chosen at
    provisioning time, not attacker-chosen.

Registry entry schema (one JSON file per artifact, under REGISTRY_DIR):
  {
    "schema_id": "mb/ninfty-ep-registry/entry/v1",
    "artifact_id": <str>,
    "role": "native_a" | "native_b",   # which raw-evidence slot this
                                        # artifact is pinned to attest --
                                        # checked against the CALLER's
                                        # claimed slot at the
                                        # evidence-union facade layer
                                        # (A/B-swap guard, P88-o item 5(d)).
    "version_id": <str>,               # freeze/version identifier.
    "status": "ACTIVE" | "REVOKED",
    "whole_artifact_digest": <64-hex>, # self-reported in the file (NOT
                                        # trusted by resolve() -- see above,
                                        # resolve() always recomputes).
    "content": <the native artifact payload itself>,
  }

Index file (REGISTRY_DIR/index.json):
  {"schema_id": "mb/ninfty-ep-registry/index/v1",
   "artifacts": {<artifact_id>: {"file": <filename>, "role": ..., "version_id": ...,
                                  "status": ..., "whole_artifact_digest": ...}}}
The index is a lookup convenience only; `resolve` still opens the actual
entry file and recomputes its digest from `content` -- the index's own
copy of `whole_artifact_digest`/`role`/`status` is never trusted as
authoritative by itself.

runtime = python (stdlib only: hashlib, json, os, re).
"""
from __future__ import annotations
import hashlib
import json
import os
import re

HEX64 = re.compile(r'^[0-9a-f]{64}$', re.IGNORECASE)

REGISTRY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs", "ep_registry")
INDEX_PATH = os.path.join(REGISTRY_DIR, "index.json")

VALID_ROLES = ("native_a", "native_b")
VALID_STATUSES = ("ACTIVE", "REVOKED")


def canonical_serialize(obj):
    """Same canonical form as ninfty-evidence-union.py's own
    canonical_serialize -- UTF-8, sorted keys, no whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _artifact_id_to_filename(artifact_id):
    """Deterministic, filesystem-safe filename derived from a digest of
    artifact_id -- artifact_id is NEVER used directly as a path component
    (path-traversal defense in depth, even though in this codebase
    artifact_id is always receiver-chosen at provisioning time)."""
    return _digest({"artifact_id": artifact_id}) + ".json"


def index_exists():
    """P88-o item 5(e) support: distinguishes 'the registry store itself
    is entirely absent' from 'the registry exists but this artifact_id
    is not registered in it' -- the two are reported as different
    statuses (MISSING vs UNKNOWN) by the evidence-union facade."""
    return os.path.isfile(INDEX_PATH)


def _load_index():
    if not index_exists():
        return None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve(artifact_id):
    """
    Looks up `artifact_id` in the receiver-held registry, reading straight
    from disk (INDEX_PATH + the per-artifact entry file) on EVERY call --
    never cached, never from any caller-supplied value. Returns None if
    the registry store itself is absent, the artifact_id is not
    registered, or the entry file is missing/corrupted (index/file
    identity mismatch) -- all fail-closed, never a partial/best-effort
    result.

    On success, returns:
      {"role": "native_a"|"native_b", "status": "ACTIVE"|"REVOKED"|<other>,
       "version_id": <str>, "whole_artifact_digest": <64-hex, FRESHLY
       recomputed from the entry file's own 'content' -- never the file's
       self-reported digest field>, "content": <the pinned payload>}.
    """
    if not isinstance(artifact_id, str) or not artifact_id:
        return None
    index = _load_index()
    if index is None or not isinstance(index.get("artifacts"), dict):
        return None
    meta = index["artifacts"].get(artifact_id)
    if not isinstance(meta, dict):
        return None
    fname = meta.get("file")
    if not isinstance(fname, str) or not fname:
        return None
    path = os.path.join(REGISTRY_DIR, fname)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        entry = json.load(f)
    if not isinstance(entry, dict) or entry.get("artifact_id") != artifact_id:
        # index/file identity mismatch -- a corrupted or tampered registry
        # is treated as "not resolvable", never silently accepted.
        return None
    content = entry.get("content")
    return {
        "role": entry.get("role"),
        "status": entry.get("status"),
        "version_id": entry.get("version_id"),
        "whole_artifact_digest": _digest(content),
        "content": content,
    }


def write_entry(artifact_id, role, version_id, content, status="ACTIVE"):
    """
    PROVISIONING helper -- NOT part of the untrusted trust boundary and
    NEVER called while processing a caller-supplied `raw` evidence
    artifact. Used by this project's own test setup (and, in the future,
    an operator CLI) to pin a native artifact ahead of time, entirely out
    of band from any raw evidence that later arrives. Writes the
    per-artifact entry file and updates the index, both under
    REGISTRY_DIR. Returns the freshly-computed whole_artifact_digest.
    """
    if role not in VALID_ROLES:
        raise ValueError(f"write_entry: role must be one of {VALID_ROLES!r}, got {role!r}")
    if status not in VALID_STATUSES:
        raise ValueError(f"write_entry: status must be one of {VALID_STATUSES!r}, got {status!r}")
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    fname = _artifact_id_to_filename(artifact_id)
    digest = _digest(content)
    entry = {
        "schema_id": "mb/ninfty-ep-registry/entry/v1",
        "artifact_id": artifact_id,
        "role": role,
        "version_id": version_id,
        "status": status,
        "whole_artifact_digest": digest,
        "content": content,
    }
    with open(os.path.join(REGISTRY_DIR, fname), "w", encoding="utf-8") as f:
        f.write(canonical_serialize(entry))
    index = _load_index()
    if not isinstance(index, dict) or not isinstance(index.get("artifacts"), dict):
        index = {"schema_id": "mb/ninfty-ep-registry/index/v1", "artifacts": {}}
    index["artifacts"][artifact_id] = {
        "file": fname, "role": role, "version_id": version_id,
        "status": status, "whole_artifact_digest": digest,
    }
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(canonical_serialize(index))
    return digest
