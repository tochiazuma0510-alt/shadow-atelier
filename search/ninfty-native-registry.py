#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-native-registry.py

Receiver-held native-artifact registry -- RESOLVER (read-only) HALF.
(Sol 便88 P88-o / F88-3.2, sol/sol_reply_88_math15.md; docs/notes/
cert_shape_interpretation_addendum_o_v8.md; test/production store
separation + version-id hardening per Sol 便89 (sol/裁定_246_便89検収と定理CENT.md
差戻し3), docs/notes/cert_shape_interpretation_addendum_o_v9.md; Sol 便90
F90-4.1 (sol/sol_reply_90_math17.md) split this module into a
RESOLVER-ONLY module (THIS FILE) and a separate PROVISIONING module
(search/ninfty-native-registry-provisioning.py), docs/notes/
cert_shape_interpretation_addendum_o_v10.md).

Sol 便90 F90-4.1 finding (blocker 2 of the (o) 残 4 項, closed here):
v9's `write_entry` (provisioning) and `resolve`/`index_exists` (the
untrusted-input-adjacent read path `search/ninfty-evidence-union.py`
actually imports) lived in the SAME runtime module -- a facade that only
meant to import `resolve` still had `write_entry` one attribute-lookup
away, and a future refactor could accidentally wire provisioning into the
trust boundary without any import-level signal. FIX: `write_entry` (and
everything it alone needs -- the production-write env-var guard, the
artifact_id -> filename derivation, the locking/atomic-write machinery,
the overwrite/supersede policy) moved OUT of this file entirely, into
`search/ninfty-native-registry-provisioning.py`. THIS FILE now exposes
ONLY read-side functions (`resolve`, `index_exists`, `index_path`,
`production_snapshot_digest`) plus the shared low-level constants/helpers
both halves need (`canonical_serialize`, `_digest`, `_resolve_dir`,
`PRODUCTION_REGISTRY_DIR`, `VALID_ROLES`, `VALID_STATUSES`,
`VERSION_ID_RE`). `search/ninfty-evidence-union.py`'s own `_registry()`
loader (grep-verifiable) only ever calls `.resolve(...)` on the module it
loads from THIS file's path -- `write_entry` does not exist here anymore,
so there is no attribute to accidentally reach even by mistake.

Sol 便90 F90-4.1 finding (blocker 6, closed here): v9's `resolve()`/
`_load_index()` called `json.load` directly with no exception handling --
a corrupted/truncated entry file or index.json (malformed JSON, or an I/O
error mid-read) propagated a raw `json.JSONDecodeError`/`OSError` OUT of
`resolve()`, rather than falling into the documented "fail-closed, never a
partial/best-effort result" contract. FIX: both `_load_index` and
`resolve` now wrap their file reads in `try/except (OSError, ValueError)`
(`json.JSONDecodeError` is a `ValueError` subclass) and treat any such
failure exactly like "the store/entry is not resolvable" -- `resolve`
returns `None` (already documented, now actually enforced for this case
too), `_load_index`/`index_exists`-adjacent callers see "index absent".
This is defense in depth for a hand-corrupted or partially-written
registry file, on top of (and orthogonal to) the provisioning-side
atomic-write fix in the sibling module that is meant to prevent such
corruption from ever being produced by THIS project's own tooling in the
first place.

Sol 便90 F90-4.1 finding (blocker 5/8, partially addressed here):
`production_snapshot_digest(registry_dir=None)` (new) computes ONE
receiver-recomputed digest over the ENTIRE registry directory's file set
(every `*.json` file's own bytes, sorted by filename, canonicalized) --
usable both by a future production-provisioning receipt (item 5: "a
receipt that pins the production snapshot digest") and by the test suite
to assert the production tree is BYTE-IDENTICAL before/after a whole test
run (item 8: replacing the old, weaker "before/after FILE-NAME list"
comparison in test negative 14a with a full content-digest comparison
across the WHOLE suite run, see search/test_ninfty_evidence_union.py
section 15).

THIS MODULE IS (the read half of) THE PHYSICAL TRUST BOUNDARY. It is a
plain file store, entirely separate from any `raw` evidence artifact a
caller supplies to search/ninfty-evidence-union.py:

  * `resolve(artifact_id)` reads ONLY from files under a registry
    directory (production default: `PRODUCTION_REGISTRY_DIR` =
    search/certs/ep_registry/, located via this module's OWN file path
    (`os.path.dirname(__file__)`)), NEVER from any value inside a
    caller's `raw` blob. A caller can hand this module's consuming code
    (evidence-union.py) an arbitrarily forged `raw["native_a"]`/
    `raw["native_b"]` -- that forged content is never written here and
    never read back by `resolve`.
  * Content ENTERS a registry store ONLY via
    `search/ninfty-native-registry-provisioning.py`'s `write_entry` -- an
    explicit, receiver-side PROVISIONING call (used by this project's own
    test setup / a future operator tool), never invoked as part of
    processing untrusted `raw` evidence, and NOT IMPORTABLE from this
    file at all (structural separation, not merely documentation --
    Sol 便90 F90-4.1 blocker 2). search/ninfty-evidence-union.py does not
    import the provisioning module at all (grep-verifiable: it only loads
    THIS file and calls `resolve`).
  * every artifact's `whole_artifact_digest` returned by `resolve` is
    FRESHLY RECOMPUTED from the entry file's own `content` field on every
    call (never trusted from the index's cached copy, never trusted from
    any caller claim) -- a receiver-side integrity check, defense in
    depth against a corrupted or hand-edited registry file.
  * artifact_id -> filename mapping is DERIVED (sha256 of a canonical
    wrapper around artifact_id, computed by the provisioning module at
    write time), never the artifact_id string used directly as a path
    component -- closes path-traversal by construction even though
    artifact_id in this codebase is always receiver-chosen at
    provisioning time, not attacker-chosen. `resolve` never recomputes
    this mapping itself -- it trusts the index's `file` entry only to the
    extent of opening that (already-validated-at-write-time) filename
    under the resolved directory; the entry file's own `artifact_id`
    field is still cross-checked against the requested id before any
    content is returned (identity mismatch -> None, unchanged from v9).

Registry entry schema (one JSON file per artifact, under REGISTRY_DIR) --
Sol 便90 F90-4.1 blocker 7 (`freeze_id`, new, see the provisioning module
for where it is written/required):
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
    "freeze_id": <str or None>,        # NEW (便90 F90-4.1 item 7): the
                                        # freeze/EP-run identifier this
                                        # content was pinned FROM (e.g. an
                                        # ep_run_id / freeze-receipt id).
                                        # REQUIRED (non-empty) for entries
                                        # written into PRODUCTION_REGISTRY_DIR
                                        # (enforced by the provisioning
                                        # module, not by resolve() here --
                                        # resolve() reads it back verbatim,
                                        # whatever it is, for any store).
    "status": "ACTIVE" | "REVOKED",
    "whole_artifact_digest": <64-hex>, # self-reported in the file (NOT
                                        # trusted by resolve() -- see above,
                                        # resolve() always recomputes).
    "content": <the native artifact payload itself>,
  }

Index file (REGISTRY_DIR/index.json):
  {"schema_id": "mb/ninfty-ep-registry/index/v1",
   "artifacts": {<artifact_id>: {"file": <filename>, "role": ..., "version_id": ...,
                                  "status": ..., "whole_artifact_digest": ...,
                                  "freeze_id": ...,
                                  "superseded": [ {...prior entry summaries...} ]}}}
The index is a lookup convenience only; `resolve` still opens the actual
entry file and recomputes its digest from `content` -- the index's own
copy of `whole_artifact_digest`/`role`/`status` is never trusted as
authoritative by itself. `superseded` (new, written only by the
provisioning module's supersede path) is a history list of prior entry
summaries for the same artifact_id -- `resolve` never reads it (only the
CURRENT entry file matters for a `resolve` call), it exists purely as an
audit trail.

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
# adversarial provisioning call might pass. Shared with the provisioning
# module (which is what actually enforces it at write time); kept here
# too since it is a SCHEMA fact about this store's entries, not merely a
# provisioning-time input-validation detail.
VERSION_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')

# The production store -- what a real receiver's resolve() call reads by
# default. Sol 便90 F90-4.1 blocker 2: the write-side guard
# (ENV_ALLOW_PRODUCTION_WRITE / the PermissionError it triggers) now lives
# ENTIRELY in the provisioning module -- this file has no write path at
# all, so there is nothing here left to guard.
PRODUCTION_REGISTRY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs", "ep_registry")
# Backward-compat alias (some older call sites may still reference the
# pre-便89 name) -- always equal to PRODUCTION_REGISTRY_DIR.
REGISTRY_DIR = PRODUCTION_REGISTRY_DIR

# When set, resolve()/index_exists() use THIS directory instead of
# PRODUCTION_REGISTRY_DIR whenever no explicit `registry_dir` argument is
# given. A test process sets this to an isolated tempdir BEFORE
# importing/using this module's default-directory entry points --
# production code (real CLI/CI/mine usage) never sets it, so it always
# defaults to PRODUCTION_REGISTRY_DIR.
ENV_REGISTRY_DIR = "NINFTY_EP_REGISTRY_DIR"

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


def index_exists(registry_dir=None):
    """P88-o item 5(e) support: distinguishes 'the registry store itself
    is entirely absent' from 'the registry exists but this artifact_id
    is not registered in it' -- the two are reported as different
    statuses (MISSING vs UNKNOWN) by the evidence-union facade.
    `registry_dir` defaults per `_resolve_dir` (explicit arg ->
    NINFTY_EP_REGISTRY_DIR env var -> PRODUCTION_REGISTRY_DIR).
    Sol 便90 F90-4.1 blocker 6: an existing-but-unreadable index file
    (I/O error) is treated the same as "not a file" -- fail-closed, never
    an uncaught exception."""
    path = index_path(registry_dir)
    try:
        return os.path.isfile(path)
    except OSError:
        return False


def _load_index(registry_dir=None):
    """Sol 便90 F90-4.1 blocker 6: malformed JSON or an I/O error reading
    index.json is now caught HERE and treated as 'no index' (returns
    None), rather than propagating a raw exception out of every caller
    (resolve() in particular) -- fail-closed, matching this module's own
    documented 'never a partial/best-effort result' contract."""
    if not index_exists(registry_dir):
        return None
    try:
        with open(index_path(registry_dir), "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        # ValueError covers json.JSONDecodeError; a corrupted/truncated
        # index.json is "not resolvable", never a crash.
        return None


def resolve(artifact_id, registry_dir=None):
    """
    Looks up `artifact_id` in the receiver-held registry, reading straight
    from disk (the resolved index path + the per-artifact entry file) on
    EVERY call -- never cached, never from any caller-supplied value.
    Returns None if the registry store itself is absent, the artifact_id
    is not registered, the entry file is missing/corrupted (index/file
    identity mismatch), OR the entry file's own JSON is malformed / an I/O
    error occurs while reading it (Sol 便90 F90-4.1 blocker 6) -- all
    fail-closed, never a partial/best-effort result and never an
    exception escaping this function for these input-corruption cases.

    `registry_dir`: explicit override; when omitted, defaults to the
    NINFTY_EP_REGISTRY_DIR environment variable if set, else
    PRODUCTION_REGISTRY_DIR (see `_resolve_dir`). search/ninfty-
    evidence-union.py's own call site never passes this, so it always
    reads whatever a real receiver process's environment designates --
    PRODUCTION_REGISTRY_DIR unless a test process has isolated itself via
    the env var (Sol 便89 fix (1)).

    On success, returns:
      {"role": "native_a"|"native_b", "status": "ACTIVE"|"REVOKED"|<other>,
       "version_id": <str>, "freeze_id": <str or None>,
       "whole_artifact_digest": <64-hex, FRESHLY recomputed from the entry
       file's own 'content' -- never the file's self-reported digest
       field>, "content": <the pinned payload>}.
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
    try:
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            entry = json.load(f)
    except (OSError, ValueError):
        # Sol 便90 F90-4.1 blocker 6: a corrupted/truncated entry file (or
        # an I/O error mid-read) is "not resolvable", never a crash.
        return None
    if not isinstance(entry, dict) or entry.get("artifact_id") != artifact_id:
        # index/file identity mismatch -- a corrupted or tampered registry
        # is treated as "not resolvable", never silently accepted.
        return None
    content = entry.get("content")
    return {
        "role": entry.get("role"),
        "status": entry.get("status"),
        "version_id": entry.get("version_id"),
        "freeze_id": entry.get("freeze_id"),
        "whole_artifact_digest": _digest(content),
        "content": content,
    }


def production_snapshot_digest(registry_dir=None):
    """
    Sol 便90 F90-4.1 blocker 5/8 (new): a SINGLE receiver-recomputed digest
    over the ENTIRE registry directory's on-disk file set -- every regular
    file directly under the directory (index.json, every per-artifact
    entry file; a future lock/tmp file is EXCLUDED by name pattern, see
    below), each file's OWN bytes hashed, then a canonical digest taken
    over the sorted (relative filename, per-file sha256) list. Two calls
    against an unmodified directory always agree; ANY byte-level change
    to ANY file (or an added/removed file) changes the result.

    Used by:
      - a future production-provisioning receipt (item 5: pin this value
        as "the production snapshot digest at the moment of writing this
        receipt" -- see the provisioning module's `write_production_receipt`).
      - the test suite (search/test_ninfty_evidence_union.py section 15),
        to assert PRODUCTION_REGISTRY_DIR is BYTE-IDENTICAL before and
        after a WHOLE test run -- a strictly stronger check than v9's
        negative 14a, which only compared the sorted FILE-NAME list (a
        same-named file with silently mutated bytes would not have been
        caught by that check; it IS caught by this one).

    Lock files (see the provisioning module's `_LOCK_FILENAME`) and
    temporary write-in-progress files (any name containing the literal
    substring '.tmp-') are excluded from the digest by construction -- a
    lock briefly created and removed during an unrelated concurrent
    provisioning call must not make this function's result depend on
    timing.

    Returns None if `registry_dir` (resolved) does not exist at all.
    """
    d = _resolve_dir(registry_dir)
    if not os.path.isdir(d):
        return None
    entries = []
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return None
    for name in names:
        if ".tmp-" in name or name == "index.json.lock" or name.startswith("."):
            continue
        full = os.path.join(d, name)
        if not os.path.isfile(full):
            continue
        try:
            with open(full, "rb") as f:
                file_digest = hashlib.sha256(f.read()).hexdigest()
        except OSError:
            return None
        entries.append({"name": name, "sha256": file_digest})
    return _digest({"files": entries})
