#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-native-registry-provisioning.py

Receiver-held native-artifact registry -- PROVISIONING (write-only) HALF.
Sol 便91 P91-4 (sol/sol_reply_91_math18.md F91-6.2, docs/notes/
cert_shape_interpretation_addendum_o_v11.md) replaces the old
`write_entry` (mutable entry + mutable index, two separate files updated
in sequence) with `commit_generation`: builds one BRAND-NEW, immutable
`generations/<generation_id>/` directory (index.json + one entry file per
artifact + a bundle receipt.json), self-verifies it in full via the
sibling resolver module's OWN verification code path (so publishing and
reading always agree, by construction, on what "valid" means), and ONLY
THEN atomically replaces the single `CURRENT.json` pointer file -- the
one and only mutation of "what a `resolve()` call sees" that this module
ever performs. Nothing that was already live is ever opened for writing
again.

`search/ninfty-evidence-union.py` -- the untrusted-input-adjacent facade
-- loads ONLY the resolver module and never this one (grep-verifiable:
this filename does not appear anywhere in ninfty-evidence-union.py).

This file's `commit_generation` structurally eliminates the following
Sol 便91 F91-6.2 blockers (see the resolver module's own docstring for
the full 11-item list and how each is closed; the ones that are ELIMINATED
BY DESIGN here, as opposed to merely checked-for on the read side, are):
  1. fail-open on a corrupted "existing" entry: there is no "existing
     entry" concept for a write to consult at all -- `commit_generation`
     requires the target `generations/<generation_id>` directory to NOT
     already exist (raises `FileExistsError` otherwise) and never reads
     any prior generation's content to decide what to do.
  2. entry-before-index non-atomicity: all of a generation's files (index,
     every entry, the receipt) are written into the SAME fresh directory,
     in one call, before the CURRENT pointer -- the only thing any
     `resolve()` call can see -- is ever touched.
  3. silent metadata drift: impossible by construction -- there is no
     update-in-place path; a metadata change is always a new generation
     with its own id, never a mutation of one already committed.
  4. non-transactional entry/index commit: closed by writing everything
     into a directory nothing points at yet, THEN self-verifying with the
     resolver's OWN `_load_and_verify_generation` before publishing, THEN
     (and only then) atomically swapping the ONE pointer file.

runtime = python (stdlib only: hashlib, importlib.util, json, os, re, sys,
tempfile, time, uuid, argparse, datetime).
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_resolver():
    """Dynamically loads the sibling resolver-only module (hyphenated
    filename -- same importlib.util technique used throughout this
    codebase). This is the ONLY way this file touches the resolver's
    constants/helpers/verification logic -- it never re-implements them,
    so the two modules can never silently drift apart on what
    PRODUCTION_REGISTRY_DIR, the canonical serialization, or "a valid
    generation" actually mean. In particular, `commit_generation` below
    calls `_reg._load_and_verify_generation` to self-check its own freshly
    written generation BEFORE publishing it -- reusing the exact function
    `resolve()` itself will later call, so "passes provisioning's
    self-check" and "resolvable by a real receiver" are the SAME check,
    not two independently-maintained ones that could drift apart."""
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
GENERATION_ID_RE = _reg.GENERATION_ID_RE
CURRENT_SCHEMA_ID = _reg.CURRENT_SCHEMA_ID
GEN_INDEX_SCHEMA_ID = _reg.GEN_INDEX_SCHEMA_ID
GEN_ENTRY_SCHEMA_ID = _reg.GEN_ENTRY_SCHEMA_ID
GEN_RECEIPT_SCHEMA_ID = _reg.GEN_RECEIPT_SCHEMA_ID
canonical_serialize = _reg.canonical_serialize
_digest = _reg._digest
resolve = _reg.resolve
index_exists = _reg.index_exists
current_path = _reg.current_path
generations_dir = _reg.generations_dir
generation_digest = _reg.generation_digest
_load_and_verify_generation = _reg._load_and_verify_generation
_safe_join = _reg._safe_join
production_snapshot_digest = _reg.production_snapshot_digest

# Sol 便89-era guard, unchanged in spirit under 便91: commit_generation()
# refuses to write into PRODUCTION_REGISTRY_DIR unless this environment
# variable is exactly "1" -- never set by test runs; reserved for a
# deliberate operator-provisioning CLI invocation (this file's own
# `main()` below).
ENV_ALLOW_PRODUCTION_WRITE = "NINFTY_EP_ALLOW_PRODUCTION_WRITE"

# freeze_id format: a freeze_id is a free-form identifier (e.g. an
# ep_run_id or a freeze-receipt id), not a 64-hex digest, so it gets a
# slightly wider charset than version_id/generation_id (colons allowed)
# but the same non-empty/alnum-led/bounded-length discipline.
FREEZE_ID_RE = _reg.FREEZE_ID_RE

_LOCK_FILENAME = "CURRENT.json.lock"


def _lock_path(registry_dir):
    return os.path.join(registry_dir, _LOCK_FILENAME)


class RegistryLockTimeout(RuntimeError):
    """Raised by _acquire_lock when the lock could not be obtained within
    the timeout -- a caller that cannot get the lock must not proceed to
    swap CURRENT, and must not silently block forever either."""


class _RegistryLock:
    """Exclusive, registry_dir-scoped lock via O_CREAT|O_EXCL (atomic
    "create if absent" on every platform this project targets, including
    Windows). Held ONLY around the CURRENT-pointer publish step of
    `commit_generation` (building the new generation directory itself
    needs no lock -- its directory name is unique per call and nothing
    else ever touches it) -- so two concurrent `commit_generation` calls
    against the same registry cannot interleave their "read CURRENT / stat
    the target generation dir / os.replace CURRENT" sequence."""

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
                        f"could not acquire registry publish lock {self.path!r} within {self.timeout}s "
                        "-- another commit_generation call appears to be in progress"
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
    """write-to-temp-then-rename. `os.replace` is atomic within the same
    filesystem/volume on both POSIX and Windows -- a crash or
    interruption mid-write can only ever leave the ORIGINAL file (if any)
    intact plus a stray `<path>.tmp-<pid>-<token>` file, never a
    half-written target file."""
    tmp_path = f"{path}.tmp-{os.getpid()}-{uuid.uuid4().hex[:12]}"
    with open(tmp_path, "wb") as f:
        f.write(data_bytes)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


def _atomic_write_json(path, obj):
    _atomic_write_bytes(path, canonical_serialize(obj).encode("utf-8"))


def _artifact_entry_filename(artifact_id):
    """Deterministic, filesystem-safe filename derived from a digest of
    artifact_id -- artifact_id is NEVER used directly as a path component
    (path-traversal defense in depth)."""
    return _digest({"artifact_id": artifact_id}) + ".json"


def _default_generation_id(freeze_id):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    token = uuid.uuid4().hex[:12]
    # freeze_id may contain ':' (allowed by FREEZE_ID_RE) which
    # GENERATION_ID_RE does NOT allow -- sanitize to '-' so an
    # auto-generated generation_id is always well-formed regardless of
    # the freeze_id's own shape.
    safe_freeze = re.sub(r'[^A-Za-z0-9._-]', '-', freeze_id)[:48]
    return f"{safe_freeze}-{stamp}-{token}"


def commit_generation(artifacts, freeze_id, *, registry_dir, generation_id=None,
                       publish=True):
    """
    PROVISIONING helper -- NOT part of the untrusted trust boundary and
    NEVER called while processing a caller-supplied `raw` evidence
    artifact (this function does not exist in the module
    search/ninfty-evidence-union.py imports at all).

    `artifacts`: a non-empty list of
      {"artifact_id": <str>, "role": "native_a"|"native_b"|"nf_a"|"nf_b",
       "version_id": <str>, "content": <payload>, "status": <optional,
       default "ACTIVE">}
    all bound to the ONE `freeze_id` given -- this is the generalized
    A/B-bundle-plus-freeze receipt Sol 便91 F91-6.2 blocker 9 asked for
    (native_a and native_b are the two roles evidence-union.py actually
    consumes; a generation MAY hold additional artifacts of either role,
    e.g. a test fixture's alternate "native_b_alt", all still bound to the
    same freeze -- exactly what `resolve()` will later cross-check).

    `generation_id`: if omitted, auto-derived from `freeze_id` + a UTC
    timestamp + a random token (always well-formed). If given explicitly,
    it is validated the same way and the target directory MUST NOT already
    exist -- raises `FileExistsError` otherwise (generations are
    immutable; there is no "overwrite" concept any more).

    `publish`: if True (default), swaps CURRENT.json to point at this
    generation once it is built and self-verified. If False, the
    generation is built and self-verified but left un-published (a caller
    can inspect it, or explicitly `publish_generation(...)` it later) --
    supports staging a generation without making it live.

    Validation (checked BEFORE any file is written):
      - `registry_dir`: keyword-only, REQUIRED.
      - if the RESOLVED `registry_dir` is (by realpath/samefile,
        alias-bypass-resistant -- Sol 便91 F91-6.2 blocker 7)
        PRODUCTION_REGISTRY_DIR: ENV_ALLOW_PRODUCTION_WRITE must be
        exactly "1", else PermissionError.
      - `freeze_id`: non-empty string matching FREEZE_ID_RE -- REQUIRED
        UNCONDITIONALLY (not just for production writes any more: every
        generation, test or production, is freeze-bound by construction
        under the 便91 design).
      - `artifacts`: non-empty list; each item's `artifact_id` (non-empty
        str, unique within this call), `role` (in VALID_ROLES),
        `version_id` (VERSION_ID_RE), `status` (in VALID_STATUSES,
        default "ACTIVE") all validated; `content` may be any
        JSON-serializable value.

    Returns `{"generation_id": <str>, "freeze_id": <str>, "published":
    <bool>, "generation_digest": <64-hex>,
    "artifacts": {<artifact_id>: <64-hex digest>, ...}}`.

    Self-check (P91-4: "全 digest 検査後に CURRENT ポインタ1個だけを
    atomic replace"): after writing index.json + every entry file +
    receipt.json into the fresh generation directory, this function calls
    the RESOLVER's OWN `_load_and_verify_generation` against what it just
    wrote, pointed at the (still-unpublished) generation_id directly (not
    via CURRENT) -- if that self-check does not come back exactly matching
    what was intended, this raises `RuntimeError` and does NOT touch
    CURRENT.json at all (a bug in this function must never publish a
    generation that would not actually resolve).
    """
    resolved_dir = os.path.abspath(registry_dir) if registry_dir is not None else None
    if resolved_dir is None:
        raise ValueError(
            "commit_generation: registry_dir is required (keyword-only, no default) -- a caller must state "
            "explicitly which physical store it means"
        )
    if _is_production_dir(resolved_dir) and os.environ.get(ENV_ALLOW_PRODUCTION_WRITE) != "1":
        raise PermissionError(
            f"commit_generation: refusing to write into the PRODUCTION registry directory "
            f"({PRODUCTION_REGISTRY_DIR!r}) -- set {ENV_ALLOW_PRODUCTION_WRITE}=1 to explicitly opt in "
            "(never set by test runs; reserved for a deliberate operator-provisioning CLI invocation)."
        )
    if not isinstance(freeze_id, str) or not FREEZE_ID_RE.match(freeze_id):
        raise ValueError(
            f"commit_generation: freeze_id must be a non-empty string matching {FREEZE_ID_RE.pattern!r}, "
            f"got {freeze_id!r} (Sol 便91 P91-4: every generation is freeze-bound, test stores included)"
        )
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("commit_generation: artifacts must be a non-empty list")

    seen_ids = set()
    normalized = []
    for item in artifacts:
        if not isinstance(item, dict):
            raise ValueError(f"commit_generation: each artifacts[] item must be a dict, got {item!r}")
        artifact_id = item.get("artifact_id")
        role = item.get("role")
        version_id = item.get("version_id")
        status = item.get("status", "ACTIVE")
        if not isinstance(artifact_id, str) or not artifact_id:
            raise ValueError(f"commit_generation: artifact_id must be a non-empty string, got {artifact_id!r}")
        if artifact_id in seen_ids:
            raise ValueError(f"commit_generation: duplicate artifact_id {artifact_id!r} within one call")
        seen_ids.add(artifact_id)
        if role not in VALID_ROLES:
            raise ValueError(f"commit_generation: role must be one of {VALID_ROLES!r}, got {role!r}")
        if not isinstance(version_id, str) or not VERSION_ID_RE.match(version_id):
            raise ValueError(
                f"commit_generation: version_id must be a non-empty string matching {VERSION_ID_RE.pattern!r}, "
                f"got {version_id!r}"
            )
        if status not in VALID_STATUSES:
            raise ValueError(f"commit_generation: status must be one of {VALID_STATUSES!r}, got {status!r}")
        normalized.append({
            "artifact_id": artifact_id, "role": role, "version_id": version_id,
            "status": status, "content": item.get("content"),
        })

    if generation_id is None:
        generation_id = _default_generation_id(freeze_id)
    if not isinstance(generation_id, str) or not GENERATION_ID_RE.match(generation_id):
        raise ValueError(
            f"commit_generation: generation_id must be a non-empty string matching {GENERATION_ID_RE.pattern!r}, "
            f"got {generation_id!r}"
        )

    gens_dir = generations_dir(resolved_dir)
    os.makedirs(gens_dir, exist_ok=True)
    gen_dir = _safe_join(gens_dir, generation_id)
    if gen_dir is None:
        raise ValueError(f"commit_generation: generation_id {generation_id!r} fails path confinement")
    if os.path.exists(gen_dir):
        raise FileExistsError(
            f"commit_generation: generation {generation_id!r} already exists at {gen_dir!r} -- generations are "
            "immutable, choose a different generation_id (or omit it to auto-generate one)"
        )
    os.makedirs(gen_dir)  # fresh directory -- no exist_ok, must not already exist (double-checked above too)

    index_artifacts = {}
    receipt_artifacts = []
    for item in normalized:
        digest = _digest(item["content"])
        fname = _artifact_entry_filename(item["artifact_id"])
        entry = {
            "schema_id": GEN_ENTRY_SCHEMA_ID,
            "generation_id": generation_id,
            "artifact_id": item["artifact_id"],
            "role": item["role"],
            "version_id": item["version_id"],
            "freeze_id": freeze_id,
            "status": item["status"],
            "whole_artifact_digest": digest,
            "content": item["content"],
        }
        _atomic_write_bytes(os.path.join(gen_dir, fname), canonical_serialize(entry).encode("utf-8"))
        index_artifacts[item["artifact_id"]] = {
            "file": fname, "role": item["role"], "version_id": item["version_id"],
            "freeze_id": freeze_id, "status": item["status"], "whole_artifact_digest": digest,
        }
        receipt_artifacts.append({"artifact_id": item["artifact_id"], "whole_artifact_digest": digest})

    index_doc = {
        "schema_id": GEN_INDEX_SCHEMA_ID,
        "generation_id": generation_id,
        "freeze_id": freeze_id,
        "artifacts": index_artifacts,
    }
    _atomic_write_bytes(os.path.join(gen_dir, "index.json"), canonical_serialize(index_doc).encode("utf-8"))

    gen_digest = generation_digest(gen_dir)
    if gen_digest is None:
        raise RuntimeError(
            f"commit_generation: internal error -- generation_digest() over the just-written generation "
            f"{generation_id!r} returned None; refusing to write a receipt or publish"
        )
    receipt_artifacts.sort(key=lambda e: e["artifact_id"])
    receipt = {
        "schema_id": GEN_RECEIPT_SCHEMA_ID,
        "generation_id": generation_id,
        "freeze_id": freeze_id,
        "artifacts": receipt_artifacts,
        "generation_digest": gen_digest,
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
    _atomic_write_bytes(os.path.join(gen_dir, "receipt.json"), canonical_serialize(receipt).encode("utf-8"))

    # Self-check (P91-4): re-derive this generation the SAME way a real
    # resolve() call would, pointed directly at generation_id -- must
    # succeed and must exactly reproduce what we intended to write, or we
    # refuse to publish at all.
    verified = _load_and_verify_generation(resolved_dir, generation_id)
    if verified is None or verified["freeze_id"] != freeze_id or set(verified["artifacts"]) != seen_ids:
        raise RuntimeError(
            f"commit_generation: internal error -- self-check of freshly written generation {generation_id!r} "
            "failed (_load_and_verify_generation did not reproduce what was written); NOT publishing. This "
            "generation directory is left on disk, un-pointed-to by CURRENT, for forensic inspection."
        )
    for artifact_id, meta in verified["artifacts"].items():
        expected_digest = next(e["whole_artifact_digest"] for e in receipt_artifacts if e["artifact_id"] == artifact_id)
        if meta["whole_artifact_digest"] != expected_digest:
            raise RuntimeError(
                f"commit_generation: internal error -- self-check digest mismatch for {artifact_id!r}; NOT publishing."
            )

    published = False
    if publish:
        with _acquire_lock(resolved_dir):
            current_doc = {
                "schema_id": CURRENT_SCHEMA_ID,
                "generation_id": generation_id,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            _atomic_write_json(current_path(resolved_dir), current_doc)
        published = True

    return {
        "generation_id": generation_id,
        "freeze_id": freeze_id,
        "published": published,
        "generation_digest": gen_digest,
        "artifacts": {aid: meta["whole_artifact_digest"] for aid, meta in verified["artifacts"].items()},
    }


def publish_generation(generation_id, *, registry_dir):
    """Publishes an already-built-but-unpublished generation (one created
    via `commit_generation(..., publish=False)`) by re-running the same
    self-check and then swapping CURRENT.json. Kept separate from
    `commit_generation` so a caller can build+verify now and decide to
    publish later (or never) without re-deriving anything."""
    resolved_dir = os.path.abspath(registry_dir)
    if _is_production_dir(resolved_dir) and os.environ.get(ENV_ALLOW_PRODUCTION_WRITE) != "1":
        raise PermissionError(
            f"publish_generation: refusing to publish into the PRODUCTION registry directory "
            f"({PRODUCTION_REGISTRY_DIR!r}) -- set {ENV_ALLOW_PRODUCTION_WRITE}=1 to explicitly opt in."
        )
    verified = _load_and_verify_generation(resolved_dir, generation_id)
    if verified is None:
        raise RuntimeError(f"publish_generation: generation {generation_id!r} does not self-verify -- refusing to publish")
    with _acquire_lock(resolved_dir):
        current_doc = {
            "schema_id": CURRENT_SCHEMA_ID,
            "generation_id": generation_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        _atomic_write_json(current_path(resolved_dir), current_doc)
    return {"generation_id": generation_id, "published": True}


def _is_production_dir(resolved_dir):
    """Sol 便91 F91-6.2 blocker 7: production-directory detection by
    filesystem identity, not string comparison -- resistant to a
    symlink/junction alias pointing at PRODUCTION_REGISTRY_DIR under a
    different path string. Uses `os.path.samefile` (compares the actual
    filesystem object, robust to symlinks/junctions/case-folding) when
    BOTH paths already exist; falls back to `os.path.realpath` comparison
    when either side does not exist yet (samefile requires both to
    exist) -- realpath still resolves any symlink components that DO
    exist along the way."""
    try:
        if os.path.isdir(resolved_dir) and os.path.isdir(PRODUCTION_REGISTRY_DIR):
            return os.path.samefile(resolved_dir, PRODUCTION_REGISTRY_DIR)
    except OSError:
        pass
    try:
        return os.path.realpath(resolved_dir) == os.path.realpath(PRODUCTION_REGISTRY_DIR)
    except OSError:
        return False


def write_production_receipt(*args, **kwargs):
    """Removed under 便91 P91-4: the per-artifact 'production receipt'
    concept is superseded by the generation's own bundle `receipt.json`
    (written by `commit_generation` itself, covering ALL artifacts in the
    generation plus the shared freeze_id plus the generation_digest --
    Sol 便91 F91-6.2 blocker 9). Kept as a stub that raises, rather than
    silently removed, so any stale caller fails loudly instead of
    importing a now-nonexistent name."""
    raise NotImplementedError(
        "write_production_receipt was removed by Sol 便91 P91-4 -- commit_generation's own receipt.json (per "
        "generation, covering every artifact + the shared freeze_id + generation_digest) replaces it"
    )


def main(argv):
    """
    Operator CLI. Deliberately requires the SAME
    `NINFTY_EP_ALLOW_PRODUCTION_WRITE=1` opt-in as a direct
    `commit_generation(..., registry_dir=PRODUCTION_REGISTRY_DIR)` call
    would -- this CLI does not set the env var itself, an operator must
    export it in their own shell before invoking this tool.

    Takes one or more `--artifact` specs (repeatable) plus one
    `--freeze-id`, and commits (and, by default, publishes) a single new
    generation binding all of them together.

    IMPORTANT (honesty note, carried forward from the pre-便91 module):
    production provisioning of a REAL EP artifact remains a commander
    (司令塔) decision, not one this task makes on its own -- this CLI is a
    complete, tested MECHANISM; no artifact in this repository is
    registered under it by this task.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact", action="append", required=True,
                     help="artifact-id=...,role=...,version-id=...,content-file=...[,status=...] "
                          "(repeatable; at least one required)")
    ap.add_argument("--freeze-id", required=True)
    ap.add_argument("--generation-id", default=None)
    ap.add_argument("--production", action="store_true",
                     help="write into PRODUCTION_REGISTRY_DIR (requires NINFTY_EP_ALLOW_PRODUCTION_WRITE=1 "
                          "already set in the environment) instead of --registry-dir")
    ap.add_argument("--registry-dir", default=None, help="explicit non-production store (mutually exclusive with --production)")
    ap.add_argument("--no-publish", action="store_true", help="build and self-verify but do not swap CURRENT.json")
    args = ap.parse_args(argv)

    if args.production and args.registry_dir:
        print("error: --production and --registry-dir are mutually exclusive", file=sys.stderr)
        return 2
    if not args.production and not args.registry_dir:
        print("error: one of --production or --registry-dir is required", file=sys.stderr)
        return 2
    target_dir = PRODUCTION_REGISTRY_DIR if args.production else args.registry_dir

    artifacts = []
    for spec in args.artifact:
        fields = {}
        for part in spec.split(","):
            if "=" not in part:
                print(f"error: --artifact spec part {part!r} is not key=value", file=sys.stderr)
                return 2
            k, v = part.split("=", 1)
            fields[k.strip()] = v.strip()
        required = {"artifact-id", "role", "version-id", "content-file"}
        missing = required - set(fields)
        if missing:
            print(f"error: --artifact spec missing {sorted(missing)}: {spec!r}", file=sys.stderr)
            return 2
        with open(fields["content-file"], "r", encoding="utf-8") as f:
            content = json.load(f)
        artifacts.append({
            "artifact_id": fields["artifact-id"], "role": fields["role"],
            "version_id": fields["version-id"], "content": content,
            "status": fields.get("status", "ACTIVE"),
        })

    result = commit_generation(
        artifacts, args.freeze_id, registry_dir=target_dir,
        generation_id=args.generation_id, publish=not args.no_publish,
    )
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
