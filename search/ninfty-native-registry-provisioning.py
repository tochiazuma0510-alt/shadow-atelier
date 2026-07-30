#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-native-registry-provisioning.py

Receiver-held native-artifact registry -- PROVISIONING (write-only) HALF.
Sol 便90 F90-4.1 (sol/sol_reply_90_math17.md; docs/notes/
cert_shape_interpretation_addendum_o_v10.md) split the previous single
`search/ninfty-native-registry.py` module into this file (provisioning:
`write_entry`, the operator CLI) and the sibling resolver-only
`search/ninfty-native-registry.py` (`resolve`, `index_exists`,
`production_snapshot_digest`). `search/ninfty-evidence-union.py` -- the
untrusted-input-adjacent facade -- loads ONLY the resolver module and
never this one (grep-verifiable: this filename does not appear anywhere
in ninfty-evidence-union.py).

This file closes FOUR of the (o) v9 blockers Sol 便90 F90-4.1 listed
(the "(o) 残 4 項" the 便90 task singled out):

  1. (実体化 / real-artifact provisioning): `write_entry` now REQUIRES a
     `freeze_id` (non-empty str, format-checked like `version_id`) for any
     write that resolves to `PRODUCTION_REGISTRY_DIR` -- an entry can no
     longer be pinned into production with no record of WHICH freeze/EP
     run its content came from (closes v9 blocker 7: "role/schema/status/
     whole digest と実 freeze ID を束ねた production provisioning がない").
     `write_production_receipt` (new) writes a receipt file recording the
     artifact_id/role/version_id/freeze_id/whole_artifact_digest just
     written PLUS `ninfty-native-registry.production_snapshot_digest()`
     immediately after the write -- a single fixed value future auditors
     can recompute and compare (closes v9 blocker 5: "production snapshot
     digest を固定した receipt がない"). The `main()` CLI below is the
     operator entry point a human (or a future automated provisioning
     step) actually runs to register a real artifact; see its docstring
     for why this codebase currently has NO artifact that can be
     registered under it without a commander decision -- the search
     conducted while writing this module found no artifact in this repo
     that is BOTH (a) genuinely EP-v7-real (not a synthetic placeholder)
     and (b) already declared by prior provenance as "the" pinned native_a/
     native_b content; `search/certs/full_witness_fixture_01.json` is the
     closest candidate (real lane-A `generateCertificate()` output on a
     genuine Pell fixture, per its own `_description`) but is documented
     as a FIXTURE, and `provenance/ninfty_freeze_receipt_sol75.md` itself
     states EP wiring was NOT YET AUTHORIZED at that freeze -- so this
     module ships the MECHANISM, not a guessed real registration.
  2. (resolver/provisioning 分離): this file, see module-level split above.
  3. (同一 ID 上書きの既定拒否): `write_entry` now REFUSES (raises
     `ValueError`) to overwrite an EXISTING entry for the same
     `artifact_id` with DIFFERENT content (different role, or different
     `whole_artifact_digest` of `content`) unless the caller passes
     `supersede=True`. Passing `supersede=True` does NOT delete the old
     version: the prior entry file's bytes are copied, byte-for-byte, into
     `<registry_dir>/_superseded/<artifact_id-digest>-<old_digest[:16]>.json`
     BEFORE the new content is written, and a summary of the superseded
     entry (file, whole_artifact_digest, version_id, freeze_id,
     superseded_at) is appended to `index["artifacts"][artifact_id]
     ["superseded"]` (a list, oldest first) -- so `resolve(artifact_id)`
     always returns the CURRENT entry, but the full history remains on
     disk and in the index for audit. Re-writing the SAME artifact_id with
     IDENTICAL content (same role AND same whole_artifact_digest) is
     always allowed with no supersede flag and no history entry appended
     (idempotent re-provisioning, not a content change).
  4. (atomic / locked 更新): every `write_entry` call that will touch disk
     acquires an exclusive, `registry_dir`-scoped lock file
     (`_acquire_lock`, `O_CREAT|O_EXCL`-based, cross-platform, retries with
     a bounded timeout) around its ENTIRE read-check-write sequence (so
     two concurrent `write_entry` calls against the same directory cannot
     interleave their overwrite-check and their write), and every actual
     file write (entry file, archived-superseded copy, index.json) goes
     through `_atomic_write_bytes`: write to a sibling `<path>.tmp-<pid>-
     <token>` file, `f.flush(); os.fsync(...)`, then `os.replace(tmp,
     path)` -- `os.replace` is atomic on both POSIX and Windows for a
     rename within the same volume, so a crash mid-write can only ever
     leave a stray `.tmp-*` file behind (never a half-written `index.json`
     or entry file); `production_snapshot_digest` (resolver module)
     already excludes `.tmp-*` names by construction.

runtime = python (stdlib only: hashlib, importlib.util, json, os, re,
sys, tempfile, time, uuid, shutil, argparse, datetime).
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
import time
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_resolver():
    """Dynamically loads the sibling resolver-only module (hyphenated
    filename -- same importlib.util technique used throughout this
    codebase). This is the ONLY way this file touches the resolver's
    constants/helpers -- it never re-implements them, so the two modules
    can never silently drift apart on e.g. what PRODUCTION_REGISTRY_DIR
    or the canonical serialization actually is."""
    path = os.path.join(HERE, "ninfty-native-registry.py")
    spec = importlib.util.spec_from_file_location("ninfty_native_registry_resolver_for_provisioning", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_reg = _load_resolver()

PRODUCTION_REGISTRY_DIR = _reg.PRODUCTION_REGISTRY_DIR
VALID_ROLES = _reg.VALID_ROLES
VALID_STATUSES = _reg.VALID_STATUSES
VERSION_ID_RE = _reg.VERSION_ID_RE
canonical_serialize = _reg.canonical_serialize
_digest = _reg._digest
resolve = _reg.resolve
index_path = _reg.index_path
_resolve_dir = _reg._resolve_dir
_load_index = _reg._load_index
production_snapshot_digest = _reg.production_snapshot_digest

# Sol 便89-era guard (moved here wholesale per 便90 F90-4.1 blocker 2 --
# this env var only means anything to the WRITE path, which now lives
# entirely in this file): write_entry() refuses to write into
# PRODUCTION_REGISTRY_DIR unless this environment variable is exactly
# "1" -- never set by test runs; reserved for a deliberate operator-
# provisioning CLI invocation (this file's own `main()` below).
ENV_ALLOW_PRODUCTION_WRITE = "NINFTY_EP_ALLOW_PRODUCTION_WRITE"

# Sol 便90 F90-4.1 blocker 7 (item 1): freeze_id format -- same shape
# discipline as VERSION_ID_RE (non-empty, alphanumeric-led, bounded); a
# freeze_id is a free-form identifier (e.g. an ep_run_id or a freeze-
# receipt id), not a 64-hex digest, so no stronger structural check is
# imposed here than the one already governing version_id.
FREEZE_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$')

_LOCK_FILENAME = "index.json.lock"


def _artifact_id_to_filename(artifact_id):
    """Deterministic, filesystem-safe filename derived from a digest of
    artifact_id -- artifact_id is NEVER used directly as a path component
    (path-traversal defense in depth, even though in this codebase
    artifact_id is always receiver-chosen at provisioning time, not
    attacker-chosen). Unchanged from the pre-split module."""
    return _digest({"artifact_id": artifact_id}) + ".json"


def _lock_path(registry_dir):
    return os.path.join(registry_dir, _LOCK_FILENAME)


class RegistryLockTimeout(RuntimeError):
    """Raised by _acquire_lock when the lock could not be obtained within
    the timeout -- Sol 便90 F90-4.1 blocker 4 (atomic/locked updates):
    a caller that cannot get the lock must not proceed to write, and must
    not silently block forever either."""


class _RegistryLock:
    """Exclusive, registry_dir-scoped lock via O_CREAT|O_EXCL (atomic
    "create if absent" on every platform this project targets, including
    Windows). Held for the ENTIRE read-check-write sequence of a single
    write_entry call, so two concurrent provisioning calls against the
    same directory cannot interleave their overwrite-check and their
    actual write (the specific race this closes: process A reads 'no
    existing entry', process B reads 'no existing entry', both proceed to
    write -- with the lock held across both the read-check and the write,
    only one of A/B can be inside that critical section at a time)."""

    def __init__(self, registry_dir, timeout=10.0, poll=0.05):
        self.path = _lock_path(registry_dir)
        self.timeout = timeout
        self.poll = poll
        self._fd = None

    def __enter__(self):
        deadline = time.time() + self.timeout
        while True:
            try:
                self._fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(self._fd, str(os.getpid()).encode("ascii"))
                return self
            except FileExistsError:
                if time.time() >= deadline:
                    raise RegistryLockTimeout(
                        f"could not acquire registry write lock {self.path!r} within {self.timeout}s "
                        "-- another write_entry call appears to be in progress (Sol 便90 F90-4.1 blocker 4)"
                    )
                time.sleep(self.poll)

    def __exit__(self, exc_type, exc, tb):
        if self._fd is not None:
            try:
                os.close(self._fd)
            except OSError:
                pass
        try:
            os.remove(self.path)
        except OSError:
            pass
        return False


def _acquire_lock(registry_dir, timeout=10.0, poll=0.05):
    return _RegistryLock(registry_dir, timeout=timeout, poll=poll)


def _atomic_write_bytes(path, data_bytes):
    """Sol 便90 F90-4.1 blocker 4: write-to-temp-then-rename. `os.replace`
    is atomic within the same filesystem/volume on both POSIX and Windows
    -- a crash or interruption mid-write can only ever leave the ORIGINAL
    file (if any) intact plus a stray `<path>.tmp-<pid>-<token>` file
    (excluded from `production_snapshot_digest` by name pattern), never a
    half-written target file."""
    tmp_path = f"{path}.tmp-{os.getpid()}-{uuid.uuid4().hex[:12]}"
    with open(tmp_path, "wb") as f:
        f.write(data_bytes)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


def _atomic_write_json(path, obj):
    _atomic_write_bytes(path, canonical_serialize(obj).encode("utf-8"))


def write_entry(artifact_id, role, version_id, content, status="ACTIVE", *, registry_dir,
                 freeze_id=None, supersede=False):
    """
    PROVISIONING helper -- NOT part of the untrusted trust boundary and
    NEVER called while processing a caller-supplied `raw` evidence
    artifact (this function does not exist in the module
    search/ninfty-evidence-union.py imports at all, see this file's
    module docstring, item 2). Used by this project's own test setup
    (and, via `main()` below, a future operator invocation) to pin a
    native artifact ahead of time, entirely out of band from any raw
    evidence that later arrives. Returns
    `{"whole_artifact_digest": <64-hex>, "superseded": <bool>}`.

    Validation (checked BEFORE the lock is acquired and BEFORE any file is
    touched, in this order):
      - `role` in VALID_ROLES, `status` in VALID_STATUSES.
      - `version_id`: non-empty string matching VERSION_ID_RE (Sol 便89).
      - `registry_dir`: keyword-only, REQUIRED (Sol 便89).
      - if the RESOLVED `registry_dir` equals PRODUCTION_REGISTRY_DIR:
          * ENV_ALLOW_PRODUCTION_WRITE must be exactly "1", else
            PermissionError (Sol 便89, unchanged).
          * `freeze_id` is now REQUIRED (non-empty string matching
            FREEZE_ID_RE) -- Sol 便90 F90-4.1 blocker 7: a production
            entry with no record of which freeze/EP run it came from is
            no longer accepted. `ValueError` if missing/ill-shaped.
        (For a non-production `registry_dir` -- i.e. any test store --
        `freeze_id` remains OPTIONAL, default None: test fixtures are not
        claiming to be a real freeze.)

    Overwrite policy (Sol 便90 F90-4.1 blocker 3, checked AFTER the lock is
    held, so this check and the subsequent write are atomic together):
      - no existing entry for `artifact_id` in this store -> plain write.
      - existing entry with the SAME role AND the SAME whole_artifact_digest
        of `content` -> idempotent re-write, allowed with no supersede flag,
        no history entry appended (this is "provisioning the same fact
        again", not a content change).
      - existing entry that DIFFERS (role and/or content digest) ->
        raises ValueError UNLESS `supersede=True`. With `supersede=True`,
        the OLD entry file's bytes are archived verbatim into
        `<registry_dir>/_superseded/` before the new content is written,
        and a summary is appended to the index's per-artifact
        `superseded` history list (oldest first) -- the old version is
        never deleted, only superseded.
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
    is_production = resolved_dir == os.path.abspath(PRODUCTION_REGISTRY_DIR)
    if is_production and os.environ.get(ENV_ALLOW_PRODUCTION_WRITE) != "1":
        raise PermissionError(
            f"write_entry: refusing to write into the PRODUCTION registry directory "
            f"({PRODUCTION_REGISTRY_DIR!r}) -- set {ENV_ALLOW_PRODUCTION_WRITE}=1 to explicitly opt in "
            "(never set by test runs; reserved for a deliberate operator-provisioning CLI invocation). "
            "Sol 便89 fix: test code must provision into a distinct registry_dir, never the production store."
        )
    if is_production:
        if not isinstance(freeze_id, str) or not FREEZE_ID_RE.match(freeze_id):
            raise ValueError(
                f"write_entry: production writes require a non-empty freeze_id matching "
                f"{FREEZE_ID_RE.pattern!r} (which freeze/EP run this content came from), got {freeze_id!r} "
                "(Sol 便90 F90-4.1 blocker 7)"
            )

    os.makedirs(resolved_dir, exist_ok=True)
    fname = _artifact_id_to_filename(artifact_id)
    digest = _digest(content)
    entry_path = os.path.join(resolved_dir, fname)

    with _acquire_lock(resolved_dir):
        existing_raw = None
        if os.path.isfile(entry_path):
            try:
                with open(entry_path, "r", encoding="utf-8") as f:
                    existing_raw = json.load(f)
            except (OSError, ValueError):
                existing_raw = None  # treat an unreadable prior entry as absent -- fail open to "plain write"

        superseded = False
        if isinstance(existing_raw, dict) and existing_raw.get("artifact_id") == artifact_id:
            same_role = existing_raw.get("role") == role
            same_digest = _digest(existing_raw.get("content")) == digest
            if not (same_role and same_digest):
                if not supersede:
                    raise ValueError(
                        f"write_entry: artifact_id {artifact_id!r} is already registered in {resolved_dir!r} "
                        f"with different content (role={existing_raw.get('role')!r} vs {role!r}, existing "
                        f"whole_artifact_digest={_digest(existing_raw.get('content'))!r} vs new {digest!r}) -- "
                        "refusing to overwrite by default; pass supersede=True to archive the prior version "
                        "and register the new content (Sol 便90 F90-4.1 blocker 3)"
                    )
                superseded = True
                archive_dir = os.path.join(resolved_dir, "_superseded")
                os.makedirs(archive_dir, exist_ok=True)
                old_digest = _digest(existing_raw.get("content"))
                archive_name = f"{fname[:-5]}-{old_digest[:16]}.json"
                archive_path = os.path.join(archive_dir, archive_name)
                if not os.path.isfile(archive_path):
                    with open(entry_path, "rb") as f:
                        _atomic_write_bytes(archive_path, f.read())

        entry = {
            "schema_id": "mb/ninfty-ep-registry/entry/v1",
            "artifact_id": artifact_id,
            "role": role,
            "version_id": version_id,
            "freeze_id": freeze_id,
            "status": status,
            "whole_artifact_digest": digest,
            "content": content,
        }
        _atomic_write_json(entry_path, entry)

        index = _load_index(resolved_dir)
        if not isinstance(index, dict) or not isinstance(index.get("artifacts"), dict):
            index = {"schema_id": "mb/ninfty-ep-registry/index/v1", "artifacts": {}}
        prior_meta = index["artifacts"].get(artifact_id)
        # Sol 便90 F90-4.1 blocker 3 fix (idempotent-rewrite regression):
        # ANY re-write of an existing artifact_id (superseding or not, e.g.
        # a plain idempotent same-content re-write) must carry the PRIOR
        # 'superseded' history forward -- only a genuinely NEW supersede
        # event appends to it. Losing prior history on a later idempotent
        # write would silently erase the audit trail this feature exists
        # to keep.
        prior_history = (
            prior_meta.get("superseded") if isinstance(prior_meta, dict) and isinstance(prior_meta.get("superseded"), list) else []
        )
        new_meta = {
            "file": fname, "role": role, "version_id": version_id, "freeze_id": freeze_id,
            "status": status, "whole_artifact_digest": digest,
        }
        if superseded:
            history = list(prior_history)
            history.append({
                "file": prior_meta.get("file"), "role": prior_meta.get("role"),
                "version_id": prior_meta.get("version_id"), "freeze_id": prior_meta.get("freeze_id"),
                "whole_artifact_digest": prior_meta.get("whole_artifact_digest"),
                "superseded_at": datetime.now(timezone.utc).isoformat(),
            })
            new_meta["superseded"] = history
        elif prior_history:
            new_meta["superseded"] = prior_history
        index["artifacts"][artifact_id] = new_meta
        _atomic_write_json(index_path(resolved_dir), index)

    return {"whole_artifact_digest": digest, "superseded": superseded}


def write_production_receipt(artifact_id, receipt_path=None):
    """
    Sol 便90 F90-4.1 blocker 5 (item 1): writes a small, machine-generated
    receipt recording (a) the artifact_id/role/version_id/freeze_id/
    whole_artifact_digest of the entry just provisioned into
    PRODUCTION_REGISTRY_DIR (read back via `resolve`, never re-derived
    from caller-supplied values) and (b)
    `ninfty-native-registry.production_snapshot_digest()` computed
    IMMEDIATELY AFTER, over the whole production directory -- a single
    fixed value a future auditor can recompute (same function, same
    directory) and compare byte-for-byte. Must be called AFTER a
    successful production `write_entry` call, in the SAME process (so the
    env var opt-in is still in effect for the `resolve` call, which
    itself needs no opt-in but is being pointed at PRODUCTION_REGISTRY_DIR
    explicitly here).

    Returns the receipt dict; also writes it to `receipt_path` (default:
    `<PRODUCTION_REGISTRY_DIR>/PRODUCTION_RECEIPT.json`) via
    `_atomic_write_json`.
    """
    entry = resolve(artifact_id, registry_dir=PRODUCTION_REGISTRY_DIR)
    if entry is None:
        raise ValueError(f"write_production_receipt: {artifact_id!r} does not resolve against PRODUCTION_REGISTRY_DIR")
    snapshot_digest = production_snapshot_digest(registry_dir=PRODUCTION_REGISTRY_DIR)
    receipt = {
        "schema_id": "mb/ninfty-ep-registry/production-receipt/v1",
        "artifact_id": artifact_id,
        "role": entry.get("role"),
        "version_id": entry.get("version_id"),
        "freeze_id": entry.get("freeze_id"),
        "whole_artifact_digest": entry.get("whole_artifact_digest"),
        "production_snapshot_digest": snapshot_digest,
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
    if receipt_path is None:
        receipt_path = os.path.join(PRODUCTION_REGISTRY_DIR, "PRODUCTION_RECEIPT.json")
    _atomic_write_json(receipt_path, receipt)
    return receipt


def main(argv):
    """
    Operator CLI -- the "future operator CLI" this codebase's write-guard
    comments have referred to since Sol 便89. Deliberately requires the
    SAME `NINFTY_EP_ALLOW_PRODUCTION_WRITE=1` opt-in as a direct
    `write_entry(..., registry_dir=PRODUCTION_REGISTRY_DIR)` call would --
    this CLI does not set the env var itself, an operator must export it
    in their own shell before invoking this tool, exactly as the
    docstrings elsewhere in this codebase have always described.

    IMPORTANT (honesty note, per this file's own module docstring item 1):
    this CLI is shipped as a COMPLETE, TESTED MECHANISM (see
    search/test_ninfty_evidence_union.py section 15 for its exercise
    against an isolated test store). It has NOT been run against
    PRODUCTION_REGISTRY_DIR by this implementation task -- no artifact in
    this repository could be identified, from the artifacts and provenance
    files searched, as an already-designated "the real EP v7 native_a /
    native_b content, ready to pin". Running this CLI with --production
    against a real candidate is a commander (司令塔) decision, not one
    this task makes on its own.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact-id", required=True)
    ap.add_argument("--role", required=True, choices=list(VALID_ROLES))
    ap.add_argument("--version-id", required=True)
    ap.add_argument("--content-file", required=True, help="path to a JSON file holding the native artifact payload")
    ap.add_argument("--status", default="ACTIVE", choices=list(VALID_STATUSES))
    ap.add_argument("--freeze-id", default=None, help="required with --production")
    ap.add_argument("--production", action="store_true",
                     help="write into PRODUCTION_REGISTRY_DIR (requires NINFTY_EP_ALLOW_PRODUCTION_WRITE=1 "
                          "already set in the environment) instead of --registry-dir")
    ap.add_argument("--registry-dir", default=None, help="explicit non-production store (mutually exclusive with --production)")
    ap.add_argument("--supersede", action="store_true")
    ap.add_argument("--no-receipt", action="store_true", help="skip writing a production receipt (production writes only)")
    args = ap.parse_args(argv)

    if args.production and args.registry_dir:
        print("error: --production and --registry-dir are mutually exclusive", file=sys.stderr)
        return 2
    if not args.production and not args.registry_dir:
        print("error: one of --production or --registry-dir is required", file=sys.stderr)
        return 2
    target_dir = PRODUCTION_REGISTRY_DIR if args.production else args.registry_dir

    with open(args.content_file, "r", encoding="utf-8") as f:
        content = json.load(f)

    result = write_entry(
        args.artifact_id, args.role, args.version_id, content, status=args.status,
        registry_dir=target_dir, freeze_id=args.freeze_id, supersede=args.supersede,
    )
    print(canonical_serialize(result))

    if args.production and not args.no_receipt:
        receipt = write_production_receipt(args.artifact_id)
        print(canonical_serialize(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
