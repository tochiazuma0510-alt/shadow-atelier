#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-native-registry.py

Receiver-held native-artifact registry (Sol 便88 P88-o / F88-3.2,
sol/sol_reply_88_math15.md; docs/notes/cert_shape_interpretation_addendum_o_v8.md;
test/production store separation + version-id hardening per Sol 便89
(sol/裁定_246_便89検収と定理CENT.md 差戻し3: "production registry を test が
上書きできる・version ID が任意・省略でも PASS", 修理は
docs/notes/cert_shape_interpretation_addendum_o_v9.md).

裁定239 §3 / Sol 便88 finding: 便87's v7 closed the unresolved-pointer
fallback attack, but left the receiver unable to distinguish "native_a/
native_b are the artifacts the receiver actually pinned ahead of time"
from "native_a/native_b are whatever a caller attached to this one raw
JSON blob" -- a producer who replaces certificate+native_a+native_b
wholesale, self-consistently, still reached PASS (F88-3.2's literal
probe). `native_registry_status` in search/ninfty-evidence-union.py was
an honest but NON-GATING "UNKNOWN" annotation; P88-o requires an actual
receiver-held registry that GATES overall PASS.

Sol 便89 v9 finding (3 further blockers in v8's registry, all closed
below):

  (1) test 用の provisioning (`write_entry`) and production `resolve()`
      shared the exact same physical directory (PRODUCTION_REGISTRY_DIR)
      -- a test process could silently overwrite/pollute the SAME store a
      real receiver's `resolve()` calls read from. FIX: `write_entry` now
      REQUIRES an explicit `registry_dir` keyword argument (no default at
      all -- a caller cannot forget to say which store it means), and
      REFUSES to write into `PRODUCTION_REGISTRY_DIR` unless the
      environment variable `NINFTY_EP_ALLOW_PRODUCTION_WRITE=1` is set (a
      future operator CLI would set this deliberately; test runs never
      do). `resolve()`/`index_exists()` still default to
      `PRODUCTION_REGISTRY_DIR` for real receiver use, but honor an
      explicit `registry_dir` override, or the `NINFTY_EP_REGISTRY_DIR`
      environment variable when no explicit override is given -- so a
      test process that sets this env var to an isolated tempdir (and
      passes the SAME dir explicitly to every `write_entry` call) never
      touches production, end to end, including through
      `search/ninfty-evidence-union.py`'s own `_registry().resolve(...)`
      call (which has no dir parameter of its own and therefore also
      honors the env var).
  (2) `version_id` was accepted as ANY value at all (not even type-
      checked) by `write_entry` -- an attacker (or a careless caller) who
      controls provisioning could register an entry under a version_id
      that is empty, `None`, or an arbitrary/malicious string. FIX:
      `write_entry` now requires `version_id` to be a non-empty string
      matching `VERSION_ID_RE` (`^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`) --
      anything else raises `ValueError` before any file is touched.
  (3) `search/ninfty-evidence-union.py`'s `_resolve_native_registry` only
      compared the raw evidence's CLAIMED `version_id` against the
      registry's pinned one when the claim was present at all
      (`if claimed_version is not None and claimed_version != ...`) -- a
      raw evidence artifact that simply OMITTED `version_id` from its
      `native_registry_refs` claim skipped the version check entirely and
      could still reach `native_registry_status=PASS`. FIX (in
      ninfty-evidence-union.py, not this file): `version_id` is now a
      REQUIRED, non-empty-string field of a well-shaped
      `native_registry_refs[...]` claim (alongside `artifact_id`/
      `whole_artifact_digest`) -- an omitted `version_id` is now `MISSING`
      (same bucket as an omitted `artifact_id`), and when present it is
      ALWAYS compared for exact equality against the registry's pinned
      `version_id` (no more "skip if absent" branch). `MISSING` is
      non-PASS, so an otherwise-PASS union is downgraded to
      `INTEGRITY_STOP` exactly as it already is for every other non-PASS
      `native_registry_status` value.

THIS MODULE IS THE PHYSICAL TRUST BOUNDARY. It is a plain file store,
entirely separate from any `raw` evidence artifact a caller supplies to
search/ninfty-evidence-union.py:

  * `resolve(artifact_id)` reads ONLY from files under a registry
    directory (production default: `PRODUCTION_REGISTRY_DIR` =
    search/certs/ep_registry/, located via this module's OWN file path
    (`os.path.dirname(__file__)`)), NEVER from any value inside a
    caller's `raw` blob. A caller can hand this module's consuming code
    (evidence-union.py) an arbitrarily forged `raw["native_a"]`/
    `raw["native_b"]` -- that forged content is never written here and
    never read back by `resolve`.
  * `write_entry(...)` is the ONLY way content enters a registry store --
    an explicit, receiver-side PROVISIONING call (used by this project's
    own test setup / a future operator tool), never invoked as part of
    processing untrusted `raw` evidence. search/ninfty-evidence-union.py
    does not import `write_entry` at all (grep-verifiable: it only calls
    `resolve`). `write_entry` REQUIRES its caller to say which physical
    directory it means (`registry_dir`, keyword-only, no default) and
    refuses production writes without explicit operator opt-in (see (1)
    above) -- physically separating test provisioning from the
    production store `resolve()` reads by default.
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

# Sol 便89 fix (2): version_id format gate -- non-empty, starts with an
# alphanumeric, restricted charset, bounded length. Rejects "" / None /
# whitespace / path-traversal-ish strings / anything else a careless or
# adversarial provisioning call might pass.
VERSION_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')

# The production store -- what a real receiver's resolve() call reads by
# default, and what write_entry() refuses to write into without explicit
# operator opt-in (Sol 便89 fix (1), see NINFTY_EP_ALLOW_PRODUCTION_WRITE
# below).
PRODUCTION_REGISTRY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs", "ep_registry")
# Backward-compat alias (some older call sites may still reference the
# pre-便89 name) -- always equal to PRODUCTION_REGISTRY_DIR.
REGISTRY_DIR = PRODUCTION_REGISTRY_DIR

# When set, resolve()/index_exists()/write_entry() use THIS directory
# instead of PRODUCTION_REGISTRY_DIR whenever no explicit `registry_dir`
# argument is given. A test process sets this to an isolated tempdir
# BEFORE importing/using this module's default-directory entry points --
# production code (real CLI/CI/mine usage) never sets it, so it always
# defaults to PRODUCTION_REGISTRY_DIR. This is a READ-default convenience
# only; it does NOT bypass write_entry's production-write guard (1) below
# -- that guard compares the RESOLVED directory, whichever way it was
# selected, against PRODUCTION_REGISTRY_DIR.
ENV_REGISTRY_DIR = "NINFTY_EP_REGISTRY_DIR"

# write_entry() refuses to write into PRODUCTION_REGISTRY_DIR unless this
# environment variable is exactly "1" -- never set by test runs; reserved
# for a future deliberate operator-provisioning CLI (Sol 便89 fix (1)).
ENV_ALLOW_PRODUCTION_WRITE = "NINFTY_EP_ALLOW_PRODUCTION_WRITE"

VALID_ROLES = ("native_a", "native_b")
VALID_STATUSES = ("ACTIVE", "REVOKED")


def _resolve_dir(registry_dir):
    """Picks the actual directory a call means: explicit `registry_dir`
    argument wins; otherwise the NINFTY_EP_REGISTRY_DIR env var (test
    isolation); otherwise PRODUCTION_REGISTRY_DIR. Never caches -- read
    fresh on every call, so a test that changes the env var mid-run is
    honored immediately."""
    if registry_dir is not None:
        return registry_dir
    env_dir = os.environ.get(ENV_REGISTRY_DIR)
    if env_dir:
        return env_dir
    return PRODUCTION_REGISTRY_DIR


def index_path(registry_dir=None):
    return os.path.join(_resolve_dir(registry_dir), "index.json")


# Backward-compat: PRODUCTION_REGISTRY_DIR's own index path, as a plain
# constant (some callers -- including this project's own test file --
# previously referenced the module-level INDEX_PATH directly; kept
# pointing at the PRODUCTION path for anything that still does, though
# 便89-era test code should call index_path(registry_dir=...) explicitly
# instead so it never silently means production).
INDEX_PATH = os.path.join(PRODUCTION_REGISTRY_DIR, "index.json")


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


def index_exists(registry_dir=None):
    """P88-o item 5(e) support: distinguishes 'the registry store itself
    is entirely absent' from 'the registry exists but this artifact_id
    is not registered in it' -- the two are reported as different
    statuses (MISSING vs UNKNOWN) by the evidence-union facade.
    `registry_dir` defaults per `_resolve_dir` (explicit arg ->
    NINFTY_EP_REGISTRY_DIR env var -> PRODUCTION_REGISTRY_DIR)."""
    return os.path.isfile(index_path(registry_dir))


def _load_index(registry_dir=None):
    if not index_exists(registry_dir):
        return None
    with open(index_path(registry_dir), "r", encoding="utf-8") as f:
        return json.load(f)


def resolve(artifact_id, registry_dir=None):
    """
    Looks up `artifact_id` in the receiver-held registry, reading straight
    from disk (the resolved index path + the per-artifact entry file) on
    EVERY call -- never cached, never from any caller-supplied value.
    Returns None if the registry store itself is absent, the artifact_id
    is not registered, or the entry file is missing/corrupted (index/file
    identity mismatch) -- all fail-closed, never a partial/best-effort
    result.

    `registry_dir`: explicit override; when omitted, defaults to the
    NINFTY_EP_REGISTRY_DIR environment variable if set, else
    PRODUCTION_REGISTRY_DIR (see `_resolve_dir`). search/ninfty-
    evidence-union.py's own call site never passes this, so it always
    reads whatever a real receiver process's environment designates --
    PRODUCTION_REGISTRY_DIR unless a test process has isolated itself via
    the env var (Sol 便89 fix (1)).

    On success, returns:
      {"role": "native_a"|"native_b", "status": "ACTIVE"|"REVOKED"|<other>,
       "version_id": <str>, "whole_artifact_digest": <64-hex, FRESHLY
       recomputed from the entry file's own 'content' -- never the file's
       self-reported digest field>, "content": <the pinned payload>}.
    """
    if not isinstance(artifact_id, str) or not artifact_id:
        return None
    index = _load_index(registry_dir)
    if index is None or not isinstance(index.get("artifacts"), dict):
        return None
    meta = index["artifacts"].get(artifact_id)
    if not isinstance(meta, dict):
        return None
    fname = meta.get("file")
    if not isinstance(fname, str) or not fname:
        return None
    path = os.path.join(_resolve_dir(registry_dir), fname)
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


def write_entry(artifact_id, role, version_id, content, status="ACTIVE", *, registry_dir):
    """
    PROVISIONING helper -- NOT part of the untrusted trust boundary and
    NEVER called while processing a caller-supplied `raw` evidence
    artifact. Used by this project's own test setup (and, in the future,
    an operator CLI) to pin a native artifact ahead of time, entirely out
    of band from any raw evidence that later arrives. Writes the
    per-artifact entry file and updates the index, both under
    `registry_dir`. Returns the freshly-computed whole_artifact_digest.

    Sol 便89 hardening (both REQUIRED, checked BEFORE any file is
    touched):

    `registry_dir` is now KEYWORD-ONLY and has NO DEFAULT -- every caller
    (test or otherwise) must say explicitly which physical store it means;
    there is no path where omitting it silently lands on the production
    store. If the RESOLVED `registry_dir` is (a path equal to)
    PRODUCTION_REGISTRY_DIR, this raises `PermissionError` unless the
    environment variable NINFTY_EP_ALLOW_PRODUCTION_WRITE is exactly "1"
    -- test code has no path to writing into the production store, even
    if it explicitly passes PRODUCTION_REGISTRY_DIR by mistake.

    `version_id` must be a non-empty string matching VERSION_ID_RE
    (^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$) -- anything else (missing, None,
    empty, wrong type, or out-of-pattern) raises `ValueError`.
    """
    if role not in VALID_ROLES:
        raise ValueError(f"write_entry: role must be one of {VALID_ROLES!r}, got {role!r}")
    if status not in VALID_STATUSES:
        raise ValueError(f"write_entry: status must be one of {VALID_STATUSES!r}, got {status!r}")
    if not isinstance(version_id, str) or not VERSION_ID_RE.match(version_id):
        raise ValueError(
            f"write_entry: version_id must be a non-empty string matching {VERSION_ID_RE.pattern!r}, "
            f"got {version_id!r} (Sol 便89 fix: version ID is no longer accepted as an arbitrary string)"
        )
    if registry_dir is None:
        raise ValueError(
            "write_entry: registry_dir is required (keyword-only, no default) -- a caller must state "
            "explicitly which physical store it means (Sol 便89 fix: test/production store separation)"
        )
    resolved_dir = os.path.abspath(registry_dir)
    if resolved_dir == os.path.abspath(PRODUCTION_REGISTRY_DIR) and os.environ.get(ENV_ALLOW_PRODUCTION_WRITE) != "1":
        raise PermissionError(
            f"write_entry: refusing to write into the PRODUCTION registry directory "
            f"({PRODUCTION_REGISTRY_DIR!r}) -- set {ENV_ALLOW_PRODUCTION_WRITE}=1 to explicitly opt in "
            "(never set by test runs; reserved for a deliberate future operator-provisioning CLI). "
            "Sol 便89 fix: test code must provision into a distinct registry_dir, never the production store."
        )
    os.makedirs(resolved_dir, exist_ok=True)
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
    with open(os.path.join(resolved_dir, fname), "w", encoding="utf-8") as f:
        f.write(canonical_serialize(entry))
    index = _load_index(resolved_dir)
    if not isinstance(index, dict) or not isinstance(index.get("artifacts"), dict):
        index = {"schema_id": "mb/ninfty-ep-registry/index/v1", "artifacts": {}}
    index["artifacts"][artifact_id] = {
        "file": fname, "role": role, "version_id": version_id,
        "status": status, "whole_artifact_digest": digest,
    }
    with open(index_path(resolved_dir), "w", encoding="utf-8") as f:
        f.write(canonical_serialize(index))
    return digest
