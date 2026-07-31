#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-native-registry.py

Receiver-held native-artifact registry -- RESOLVER (read-only) HALF.
Sol 便91 P91-4 (sol/sol_reply_91_math18.md F91-6.2, docs/notes/
cert_shape_interpretation_addendum_o_v11.md) REPLACED the v9/v10
mutable-entry/mutable-index design with a GENERATION-COMMIT design: this
module now understands ONLY an immutable `generations/<generation_id>/`
tree plus a single `CURRENT.json` pointer file, and refuses (returns
None / False) on ANY structural doubt -- schema mismatch, path escape,
cross-file metadata disagreement, or a generation whose own bundle
receipt digest does not match what this module freshly recomputes.

Why the redesign (Sol 便91 F91-6.2, 11 numbered blockers in the mutable
v9/v10 design, all closed by this file + the sibling provisioning module
together):
  1. a corrupted "existing" entry could be silently treated as absent
     (fail-open) by the WRITE path -> eliminated: this design never reads
     or depends on any prior state to decide whether to write; every
     commit produces a BRAND NEW, never-before-existing generation
     directory (provisioning module refuses if the directory already
     exists), so there is no "existing entry" for a write to ever
     mis-treat as absent.
  2. entry updated before index, so a crash between the two left them
     out of sync, and the OLD resolver never cross-checked index vs
     entry metadata -> eliminated: a generation's files (all of them) are
     written once, all-at-once, into a FRESH directory before anything
     points at it; nothing already "current" is ever mutated in place.
     THIS module (see `_load_and_verify_generation`) additionally
     cross-checks every index-cached field against the entry file's own
     value, byte for byte, and fails closed on ANY disagreement.
  3. metadata drift (version_id/freeze_id/status changed while content
     digest stayed the same) used to be treated as idempotent-and-fine
     -> eliminated: there is no update-in-place at all any more, so
     there is no way for existing metadata to silently drift; a
     content/metadata change is always a NEW generation with its own id.
  4. entry/index pair was not committed as one transaction -> eliminated:
     see (2); additionally the single CURRENT-pointer swap (the only
     mutation of "what is live") is one atomic single-file replace, done
     only AFTER the whole new generation (all its files, cross-checked)
     has been built and self-verified off to the side.
  5. resolver did not check schema_id / role / status / version format /
     index-vs-entry metadata agreement at all -> closed here:
     `_load_and_verify_generation` checks ALL of it, unconditionally,
     before returning anything, for EVERY `resolve` call (never cached).
  6. index `file` field was joined onto the registry directory with no
     path-confinement check (absolute path / `..` could escape the
     registry) -> closed here: `_safe_join` requires a plain basename (no
     path separators, no `..`, non-empty) AND verifies the resolved
     realpath is actually contained under the expected parent directory,
     for both the `generations/<generation_id>` join and the per-entry
     `file` join within a generation directory.
  7. production-directory detection was a bare string/abspath comparison,
     bypassable via a symlink/junction alias -> closed here:
     `_is_production_dir` uses `os.path.samefile` when both paths exist
     (robust to symlinks/junctions/case-folding, compares the actual
     filesystem object identity) and falls back to `os.path.realpath`
     comparison only when one side does not exist yet.
  8. the old provisioning receipt was written into the SAME hash domain
     it was trying to pin (self-reference: recomputing "the same value"
     after the receipt existed included the receipt's own bytes) ->
     eliminated: `generation_digest(...)` (this module) is defined over
     EXACTLY THREE fixed-name files (index.json + every artifact entry
     file OTHER than `receipt.json`) -- `receipt.json` is written LAST,
     by the provisioning module, and is structurally excluded from the
     digest's own file set, so recomputing it later (from THIS module)
     never depends on the receipt's own bytes.
  9. the old receipt bound only a single artifact and lived outside any
     lock/transaction, so an A/B pair (and their shared freeze) was never
     jointly pinned in one place -> closed by the bundle receipt (written
     by the provisioning module, verified here): `receipt.json` records
     EVERY artifact in the generation (their artifact_id + freshly
     recomputed digest), the generation's single shared `freeze_id`, and
     the `generation_digest` -- `resolve()` requires the receipt to be
     present, well-shaped, and to agree with the freshly recomputed
     values on ALL of these before returning anything for ANY artifact in
     that generation.
  10. (consumer-side; see search/ninfty-evidence-union.py) native_a/
      native_b were never cross-checked to come from the SAME freeze --
      closed both structurally here (a generation has exactly one
      `freeze_id` shared by every artifact it contains -- there is no way
      for two artifacts resolved from the SAME `resolve()` call session
      to disagree on freeze unless they are literally in different
      generations, which `resolve()` cannot even reach since it only
      ever reads the CURRENT generation) and redundantly at the consumer
      layer (defense in depth, in case a future consumer resolves two
      artifact_ids against two DIFFERENT registry_dir/generation
      pointers by mistake).
  11. the (still-synthetic) production store's OLD flat index.json/entry
      files had no freeze_id and were resolvable anyway -> closed by
      construction: this module's `resolve()`/`index_exists()` no longer
      even look at that old flat-file shape at all (no `index.json`
      directly under the registry directory is read any more) -- they
      look ONLY for `CURRENT.json` + `generations/<id>/`, which does not
      exist yet in `PRODUCTION_REGISTRY_DIR` (the old files are inert
      leftovers of the pre-generation schema; production provisioning of
      a real artifact under the new scheme remains a separate, commander-
      gated decision, see the provisioning module's CLI).

THIS MODULE IS (the read half of) THE PHYSICAL TRUST BOUNDARY. It is a
plain file store, entirely separate from any `raw` evidence artifact a
caller supplies to search/ninfty-evidence-union.py -- see that module's
own docstring for the untrusted-input framing. Content ENTERS a registry
store ONLY via search/ninfty-native-registry-provisioning.py's
`commit_generation` -- an explicit, receiver-side PROVISIONING call, NOT
IMPORTABLE from this file at all (structural separation preserved from
便90 F90-4.1 blocker 2; this file still exposes ONLY read-side functions).

On-disk layout (under a registry directory -- production default
`PRODUCTION_REGISTRY_DIR`, or an isolated test directory via
`NINFTY_EP_REGISTRY_DIR` / an explicit `registry_dir=` argument):

  <registry_dir>/
    CURRENT.json                       # {"schema_id": CURRENT_SCHEMA_ID,
                                        #  "generation_id": <str>,
                                        #  "updated_at": <iso8601>}
                                        # the ONLY mutable file -- every
                                        # commit_generation call that
                                        # publishes replaces this ONE file
                                        # via os.replace (atomic).
    generations/
      <generation_id>/                 # IMMUTABLE once written -- never
                                        # touched again by any later commit.
        index.json                     # {"schema_id": GEN_INDEX_SCHEMA_ID,
                                        #  "generation_id": <str>,
                                        #  "freeze_id": <str>,        # ONE
                                        #    shared freeze for every
                                        #    artifact in this generation.
                                        #  "artifacts": {<artifact_id>: {
                                        #    "file": <basename>, "role":
                                        #    "native_a"|"native_b",
                                        #    "version_id": <str>,
                                        #    "freeze_id": <str>, "status":
                                        #    "ACTIVE"|"REVOKED",
                                        #    "whole_artifact_digest": <64hex>
                                        #  }, ...}}
        <artifact-entry-file>.json     # one per artifact, see
                                        # GEN_ENTRY_SCHEMA_ID below; the
                                        # "file" field in index.json for
                                        # that artifact_id names this file
                                        # by BASENAME ONLY.
        receipt.json                   # {"schema_id": GEN_RECEIPT_SCHEMA_ID,
                                        #  "generation_id": <str>,
                                        #  "freeze_id": <str>,
                                        #  "artifacts": [{"artifact_id":,
                                        #    "whole_artifact_digest":}, ...],
                                        #  "generation_digest": <64hex>,
                                        #  "issued_at": <iso8601>}
                                        # written LAST by provisioning,
                                        # EXCLUDED from generation_digest's
                                        # own file set (blocker 8).

Entry file schema (one JSON file per artifact, inside a generation dir):
  {
    "schema_id": "mb/ninfty-ep-registry/gen-entry/v2",
    "generation_id": <str>,            # must equal the containing dir.
    "artifact_id": <str>,
    "role": "native_a" | "native_b",
    "version_id": <str>,
    "freeze_id": <str>,                # REQUIRED, non-empty (v2: every
                                        # entry in a generation is bound to
                                        # a freeze by construction -- no
                                        # more optional/None freeze_id).
    "status": "ACTIVE" | "REVOKED",
    "whole_artifact_digest": <64-hex>, # self-reported (NOT trusted by
                                        # resolve() -- always recomputed
                                        # fresh from `content`).
    "content": <the native artifact payload itself>,
  }

runtime = python (stdlib only: hashlib, json, os, re).
"""
from __future__ import annotations
import hashlib
import json
import os
import re

HEX64 = re.compile(r'^[0-9a-f]{64}$', re.IGNORECASE)

# Shared identifier-format gate: non-empty, starts with an alphanumeric,
# restricted charset, bounded length. Used for version_id AND, since 便91
# P91-4, generation_id too (both are receiver-chosen identifiers that end
# up as either a JSON field or a filesystem path component, and both must
# reject "" / None / whitespace / path-traversal-ish strings the same
# way). freeze_id gets a slightly wider charset (colons allowed) in the
# provisioning module, mirrored here as FREEZE_ID_RE for resolver-side
# validation of what it reads back.
VERSION_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')
GENERATION_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$')
FREEZE_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$')

CURRENT_SCHEMA_ID = "mb/ninfty-ep-registry/current/v1"
GEN_INDEX_SCHEMA_ID = "mb/ninfty-ep-registry/gen-index/v2"
GEN_ENTRY_SCHEMA_ID = "mb/ninfty-ep-registry/gen-entry/v2"
GEN_RECEIPT_SCHEMA_ID = "mb/ninfty-ep-registry/gen-receipt/v1"

# The production store -- what a real receiver's resolve() call reads by
# default. There is no write path in this file at all (provisioning-only
# module owns that, see its own module docstring).
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

_GENERATIONS_SUBDIR = "generations"
_RECEIPT_FILENAME = "receipt.json"
_INDEX_FILENAME = "index.json"
_CURRENT_FILENAME = "CURRENT.json"


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


def current_path(registry_dir=None):
    return os.path.join(_resolve_dir(registry_dir), _CURRENT_FILENAME)


def generations_dir(registry_dir=None):
    return os.path.join(_resolve_dir(registry_dir), _GENERATIONS_SUBDIR)


# Backward-compat: previous callers referenced index_path()/INDEX_PATH for
# the (now retired) flat single-index-file shape. Kept as a function that
# points at the CURRENT-generation's index.json when resolvable, else the
# path a flat-shape index.json for that dir WOULD have had (so a stray
# caller doing pure path arithmetic still gets a string, not a crash) --
# no code in this codebase should rely on this for anything but display.
def index_path(registry_dir=None):
    gen_id = _read_current(registry_dir)
    if gen_id is not None:
        gen_dir = _safe_join(generations_dir(registry_dir), gen_id)
        if gen_dir is not None:
            return os.path.join(gen_dir, _INDEX_FILENAME)
    return os.path.join(_resolve_dir(registry_dir), _INDEX_FILENAME)


def canonical_serialize(obj):
    """Same canonical form as ninfty-evidence-union.py's own
    canonical_serialize -- UTF-8, sorted keys, no whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _is_nonempty_str(x):
    return isinstance(x, str) and len(x) > 0


def _safe_join(base_dir, name):
    """Path confinement (Sol 便91 F91-6.2 blocker 6): `name` must be a
    plain basename -- no path separators (either flavor), no '..'
    component, non-empty -- AND the resolved realpath of base_dir/name
    must actually be CONTAINED under the realpath of base_dir (defense in
    depth beyond the basename check, catching odd filesystem aliasing).
    Returns the joined path on success, None on ANY violation -- never
    raises for a hostile `name`."""
    if not _is_nonempty_str(name):
        return None
    if os.sep in name or (os.altsep and os.altsep in name) or "/" in name or "\\" in name:
        return None
    if name in (".", "..") or name.startswith(".."):
        return None
    candidate = os.path.join(base_dir, name)
    try:
        base_real = os.path.realpath(base_dir)
        cand_real = os.path.realpath(candidate)
    except OSError:
        return None
    # containment check: the resolved parent of the candidate must be
    # EXACTLY the resolved base directory -- rules out `name` itself being
    # a symlink/junction that points somewhere else on the filesystem
    # despite passing the basename-shape check above.
    if os.path.dirname(cand_real) != base_real:
        return None
    return candidate


def _read_json_file(path):
    """Fail-closed JSON read: any I/O error or malformed JSON yields None,
    never an exception escaping to the caller (Sol 便90 F90-4.1 blocker 6,
    preserved under the 便91 redesign)."""
    try:
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _read_raw_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return None


def _read_current(registry_dir=None):
    """Reads CURRENT.json and returns the generation_id it names, or None
    on ANY doubt (missing file, malformed JSON, wrong schema_id, missing/
    ill-shaped generation_id). This is the ONLY mutable file in the whole
    store; a corrupted CURRENT.json is treated exactly like an absent
    registry -- fail-closed, never a guess."""
    doc = _read_json_file(current_path(registry_dir))
    if not isinstance(doc, dict):
        return None
    if doc.get("schema_id") != CURRENT_SCHEMA_ID:
        return None
    gen_id = doc.get("generation_id")
    if not isinstance(gen_id, str) or not GENERATION_ID_RE.match(gen_id):
        return None
    return gen_id


def generation_digest(generation_dir):
    """
    Sol 便91 F91-6.2 blocker 8/9: a SINGLE receiver-recomputed digest over
    EXACTLY the generation's index.json plus every artifact entry file --
    `receipt.json` is excluded from this file set BY CONSTRUCTION (not by
    a name-pattern exclusion list -- this function only ever looks at
    `index.json`'s own `artifacts` mapping to learn which OTHER files
    exist, then hashes index.json + those files; it never lists the
    directory and never touches `receipt.json` at all), which is what
    lets `receipt.json` pin this value without ever hashing itself.

    Returns None if index.json is unreadable/malformed, or if any entry
    file `index.json` names is unreadable. `entries` in the returned
    digest domain are (name, sha256-of-raw-bytes) pairs, sorted by name,
    canonicalized the same way `production_snapshot_digest` already is.
    """
    index_fp = os.path.join(generation_dir, _INDEX_FILENAME)
    index_bytes = _read_raw_bytes(index_fp)
    if index_bytes is None:
        return None
    try:
        index_doc = json.loads(index_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(index_doc, dict) or not isinstance(index_doc.get("artifacts"), dict):
        return None
    file_entries = [{"name": _INDEX_FILENAME, "sha256": hashlib.sha256(index_bytes).hexdigest()}]
    seen_files = set()
    for meta in index_doc["artifacts"].values():
        if not isinstance(meta, dict):
            return None
        fname = meta.get("file")
        fpath = _safe_join(generation_dir, fname) if isinstance(fname, str) else None
        if fpath is None or fname in (_RECEIPT_FILENAME, _INDEX_FILENAME, _CURRENT_FILENAME):
            return None
        if fname in seen_files:
            continue
        seen_files.add(fname)
        raw = _read_raw_bytes(fpath)
        if raw is None:
            return None
        file_entries.append({"name": fname, "sha256": hashlib.sha256(raw).hexdigest()})
    file_entries.sort(key=lambda e: e["name"])
    return _digest({"files": file_entries})


def _load_and_verify_generation(registry_dir, generation_id):
    """
    The single choke point for reading a generation. Returns
    `{"freeze_id": <str>, "artifacts": {<artifact_id>: <full entry dict,
    with content>}}` on FULL success, or None if ANY of the following
    fails (fail-closed, Sol 便91 F91-6.2):
      - `generation_id` is not a well-formed identifier, or path
        confinement of `generations/<generation_id>` under
        `<registry_dir>/generations` fails (blocker 6).
      - index.json missing/malformed/wrong schema_id/wrong
        generation_id field/missing or ill-typed freeze_id (blocker 5).
      - any artifact's index-cached metadata is missing a required field
        or has the wrong type/format (blocker 5).
      - any artifact's index metadata does not share the generation's
        single freeze_id (blocker 10, structural half).
      - any artifact's `file` field fails path confinement within the
        generation directory (blocker 6).
      - the entry file itself is missing/malformed/wrong schema_id, or
        its own `generation_id`/`artifact_id`/`role`/`version_id`/
        `freeze_id`/`status` disagree with the index's cached copy
        (blocker 5, "index-entry metadata 完全一致").
      - `whole_artifact_digest` freshly recomputed from the entry's own
        `content` disagrees with the index's cached digest (blocker 3/5).
      - `receipt.json` is missing/malformed/wrong schema_id, or its
        `generation_id`/`freeze_id` disagree with the generation's own,
        or its per-artifact `artifacts` list disagrees (by artifact_id or
        digest) with what was just freshly recomputed, or its
        `generation_digest` disagrees with a FRESH call to
        `generation_digest(generation_dir)` (blocker 8/9).
    """
    if not isinstance(generation_id, str) or not GENERATION_ID_RE.match(generation_id):
        return None
    gens_dir = generations_dir(registry_dir)
    gen_dir = _safe_join(gens_dir, generation_id)
    if gen_dir is None or not os.path.isdir(gen_dir):
        return None

    index_doc = _read_json_file(os.path.join(gen_dir, _INDEX_FILENAME))
    if not isinstance(index_doc, dict):
        return None
    if index_doc.get("schema_id") != GEN_INDEX_SCHEMA_ID:
        return None
    if index_doc.get("generation_id") != generation_id:
        return None
    gen_freeze_id = index_doc.get("freeze_id")
    if not isinstance(gen_freeze_id, str) or not FREEZE_ID_RE.match(gen_freeze_id):
        return None
    artifacts_meta = index_doc.get("artifacts")
    if not isinstance(artifacts_meta, dict) or not artifacts_meta:
        return None

    resolved_artifacts = {}
    for artifact_id, meta in artifacts_meta.items():
        if not isinstance(artifact_id, str) or not artifact_id or not isinstance(meta, dict):
            return None
        role = meta.get("role")
        version_id = meta.get("version_id")
        freeze_id = meta.get("freeze_id")
        status = meta.get("status")
        whole_digest_cached = meta.get("whole_artifact_digest")
        fname = meta.get("file")
        if role not in VALID_ROLES:
            return None
        if not isinstance(version_id, str) or not VERSION_ID_RE.match(version_id):
            return None
        if freeze_id != gen_freeze_id:
            # blocker 10 (structural half): every artifact in a
            # generation must share the ONE generation-level freeze_id --
            # this alone makes an A/B "different freeze" pairing
            # unreachable via any single resolve() session, since a
            # disagreeing generation never validates at all.
            return None
        if status not in VALID_STATUSES:
            return None
        if not isinstance(whole_digest_cached, str) or not HEX64.match(whole_digest_cached):
            return None
        entry_path = _safe_join(gen_dir, fname) if isinstance(fname, str) else None
        if entry_path is None or fname in (_RECEIPT_FILENAME, _INDEX_FILENAME):
            return None

        entry = _read_json_file(entry_path)
        if not isinstance(entry, dict):
            return None
        if entry.get("schema_id") != GEN_ENTRY_SCHEMA_ID:
            return None
        if entry.get("generation_id") != generation_id:
            return None
        if entry.get("artifact_id") != artifact_id:
            return None
        if entry.get("role") != role:
            return None
        if entry.get("version_id") != version_id:
            return None
        if entry.get("freeze_id") != freeze_id:
            return None
        if entry.get("status") != status:
            return None
        content = entry.get("content")
        fresh_digest = _digest(content)
        if fresh_digest != whole_digest_cached:
            return None

        resolved_artifacts[artifact_id] = {
            "role": role,
            "status": status,
            "version_id": version_id,
            "freeze_id": freeze_id,
            "whole_artifact_digest": fresh_digest,
            "content": content,
        }

    # Bundle receipt (blocker 8/9): required, must agree with everything
    # just independently recomputed above, and must agree with a FRESH
    # generation_digest() call over index.json + entry files (receipt.json
    # itself is excluded from that digest's file set by construction).
    receipt = _read_json_file(os.path.join(gen_dir, _RECEIPT_FILENAME))
    if not isinstance(receipt, dict):
        return None
    if receipt.get("schema_id") != GEN_RECEIPT_SCHEMA_ID:
        return None
    if receipt.get("generation_id") != generation_id:
        return None
    if receipt.get("freeze_id") != gen_freeze_id:
        return None
    receipt_artifacts = receipt.get("artifacts")
    if not isinstance(receipt_artifacts, list) or len(receipt_artifacts) != len(resolved_artifacts):
        return None
    seen_in_receipt = set()
    for item in receipt_artifacts:
        if not isinstance(item, dict):
            return None
        aid = item.get("artifact_id")
        dig = item.get("whole_artifact_digest")
        if aid not in resolved_artifacts or aid in seen_in_receipt:
            return None
        if dig != resolved_artifacts[aid]["whole_artifact_digest"]:
            return None
        seen_in_receipt.add(aid)
    if seen_in_receipt != set(resolved_artifacts.keys()):
        return None
    stated_gen_digest = receipt.get("generation_digest")
    if not isinstance(stated_gen_digest, str) or not HEX64.match(stated_gen_digest):
        return None
    fresh_gen_digest = generation_digest(gen_dir)
    if fresh_gen_digest is None or fresh_gen_digest != stated_gen_digest:
        return None

    return {"freeze_id": gen_freeze_id, "artifacts": resolved_artifacts}


def index_exists(registry_dir=None):
    """P88-o item 5(e) support (preserved under 便91's redesign):
    distinguishes 'the registry store itself is entirely absent/unusable'
    from 'the registry exists but this artifact_id is not registered in
    it' -- the two are reported as different statuses (MISSING vs
    UNKNOWN) by the evidence-union facade. True iff CURRENT.json resolves
    to a generation whose index.json is at least structurally valid
    (schema_id/generation_id/freeze_id/artifacts all well-shaped) --
    intentionally a LIGHTER check than full `resolve()` (it does not
    require the bundle receipt to verify), matching this function's prior
    role as a coarse presence probe, not a full integrity gate."""
    gen_id = _read_current(registry_dir)
    if gen_id is None:
        return False
    gen_dir = _safe_join(generations_dir(registry_dir), gen_id)
    if gen_dir is None or not os.path.isdir(gen_dir):
        return False
    index_doc = _read_json_file(os.path.join(gen_dir, _INDEX_FILENAME))
    if not isinstance(index_doc, dict):
        return False
    if index_doc.get("schema_id") != GEN_INDEX_SCHEMA_ID:
        return False
    if index_doc.get("generation_id") != gen_id:
        return False
    freeze_id = index_doc.get("freeze_id")
    if not isinstance(freeze_id, str) or not FREEZE_ID_RE.match(freeze_id):
        return False
    return isinstance(index_doc.get("artifacts"), dict) and bool(index_doc["artifacts"])


def resolve_bundle(artifact_ids, registry_dir=None):
    """
    Sol 便92 P92-6 (docs/notes/cert_shape_interpretation_addendum_o_v12.md,
    W92-6/F92-6.1): resolves MULTIPLE artifact_ids from ONE single
    generation-load, closing a TOCTOU that `resolve()` (called once per
    artifact_id, by a consumer that wants an A/B *pair*) leaves open --
    each `resolve()` call independently re-reads `CURRENT.json`, so a
    publisher's atomic `CURRENT` replace landing BETWEEN two separate
    `resolve()` calls can hand the first call an artifact from generation
    G0 and the second an artifact from a *different* generation G1, with
    no receipt ever binding that specific (G0-artifact, G1-artifact) pair
    together. If G0 and G1 happen to share a `freeze_id` (nothing in the
    schema forbids two generations from reusing the same freeze_id), the
    resulting mixed pair passes a freeze-equality check that only compares
    the two `freeze_id` STRINGS, not the generations they actually came
    from -- this is exactly W92-6's "同一 freeze・異世代混成" reader-
    atomicity break, and it is not caught by any earlier "different
    freeze" negative test.

    This function closes it BY CONSTRUCTION rather than by an extra check:
    `CURRENT.json` is read exactly ONCE (a single `_read_current` call),
    the ONE generation_id that read names is captured into a local
    variable, and `_load_and_verify_generation` is then called exactly
    ONCE against that single captured generation_id -- every artifact this
    function can possibly return, for every id in `artifact_ids`, is
    necessarily looked up inside that ONE already-loaded-and-verified
    `generation["artifacts"]` dict. There is no second `CURRENT.json` read
    anywhere in this function's body, so a publisher swapping `CURRENT` at
    ANY point during (or after) this call's execution cannot change which
    generation the artifacts returned by THIS call came from -- a
    concurrent publish can only affect the NEXT call to `resolve_bundle`/
    `resolve`, never split the current call across two generations.

    `artifact_ids`: any iterable of artifact_id strings (list/tuple/set).
    Order is not significant; the same artifact_id may repeat (returned
    once, keyed by id, in the result).

    Returns `None` if `artifact_ids` is not a list/tuple/set, or if
    `CURRENT.json` fails to resolve to a generation_id (fail-closed, same
    as `resolve()`), or if that one generation fails
    `_load_and_verify_generation` (schema/path-confinement/receipt-digest
    failure, same fail-closed semantics as `resolve()`).

    On success, returns:
      {"generation_id": <str>,        # the ONE generation every artifact
                                       # below was resolved from -- Sol
                                       # 便92 P92-6's "返り値にも
                                       # generation ID を含める".
       "freeze_id": <str>,            # that generation's single shared
                                       # freeze_id (same value every
                                       # artifact in it carries).
       "artifacts": {<artifact_id>: <entry dict, see `resolve()`'s own
                      docstring for the entry shape> | None, ...}}
                                       # one key per `artifact_ids` input,
                                       # None for any id absent from this
                                       # ONE generation (mirrors
                                       # `resolve()`'s per-id None-on-
                                       # absent behavior -- a caller must
                                       # still check each value, but every
                                       # non-None value it gets back is
                                       # guaranteed to share the same
                                       # `generation_id`/`freeze_id` above).
    """
    if not isinstance(artifact_ids, (list, tuple, set, frozenset)):
        return None
    gen_id = _read_current(registry_dir)
    if gen_id is None:
        return None
    generation = _load_and_verify_generation(registry_dir, gen_id)
    if generation is None:
        return None
    artifacts = {aid: generation["artifacts"].get(aid) for aid in artifact_ids}
    return {"generation_id": gen_id, "freeze_id": generation["freeze_id"], "artifacts": artifacts}


def resolve(artifact_id, registry_dir=None):
    """
    Looks up `artifact_id` in the receiver-held registry, reading straight
    from disk on EVERY call -- never cached, never from any caller-
    supplied value. Resolution path (便91 P91-4 generation-commit design):

    CAUTION (Sol 便92 P92-6/W92-6): a caller that needs an A/B *pair*
    (or any set of artifacts that must all come from the SAME generation)
    must NOT call this function once per artifact_id -- each call
    independently re-reads `CURRENT.json`, so a publisher's atomic
    generation swap landing between two such calls can hand them artifacts
    from two DIFFERENT generations that merely happen to share a
    freeze_id (no receipt binds that specific cross-generation pair
    together -- see `resolve_bundle`'s own docstring for the full TOCTOU).
    Use `resolve_bundle(artifact_ids, registry_dir=...)` instead for any
    multi-artifact lookup that must be atomic against a concurrent
    publish; this single-id `resolve` remains correct and unchanged for
    genuinely single-artifact lookups.

      1. read CURRENT.json -> generation_id (fail-closed to None on any
         doubt about THIS file, see `_read_current`).
      2. fully load-and-verify that ONE generation (`_load_and_verify_
         generation`) -- schema, path confinement, index-vs-entry
         metadata agreement, shared freeze_id, and the bundle receipt's
         digest, ALL must check out, or the WHOLE generation resolves to
         nothing (not just the one artifact_id asked for).
      3. look up `artifact_id` in that generation's artifacts; None if
         absent.

    `registry_dir`: explicit override; when omitted, defaults to the
    NINFTY_EP_REGISTRY_DIR environment variable if set, else
    PRODUCTION_REGISTRY_DIR (see `_resolve_dir`). search/ninfty-
    evidence-union.py's own call site never passes this, so it always
    reads whatever a real receiver process's environment designates.

    On success, returns:
      {"role": "native_a"|"native_b", "status": "ACTIVE"|"REVOKED"|<other>,
       "version_id": <str>, "freeze_id": <str>,
       "whole_artifact_digest": <64-hex, FRESHLY recomputed from the entry
       file's own 'content' -- never a self-reported/cached digest>,
       "content": <the pinned payload>}.
    """
    if not isinstance(artifact_id, str) or not artifact_id:
        return None
    gen_id = _read_current(registry_dir)
    if gen_id is None:
        return None
    generation = _load_and_verify_generation(registry_dir, gen_id)
    if generation is None:
        return None
    return generation["artifacts"].get(artifact_id)


def production_snapshot_digest(registry_dir=None):
    """
    Sol 便90 F90-4.1 blocker 5/8 (preserved verbatim across the 便91
    generation-commit redesign -- this function is deliberately
    SCHEMA-AGNOSTIC, it does not care whether the directory holds the old
    flat shape or the new generations/ shape): a SINGLE receiver-
    recomputed digest over the ENTIRE registry directory's on-disk file
    set, recursively -- every regular file under the directory (including
    everything under generations/), each file's OWN bytes hashed, then a
    canonical digest taken over the sorted (relative path, per-file
    sha256) list. Two calls against an unmodified directory always agree;
    ANY byte-level change to ANY file (or an added/removed file) changes
    the result.

    Used by the test suite (search/test_ninfty_evidence_union.py) to
    assert PRODUCTION_REGISTRY_DIR is BYTE-IDENTICAL before and after a
    WHOLE test run.

    Lock files and temporary write-in-progress files (any name containing
    the literal substring '.tmp-', or named 'index.json.lock' /
    'CURRENT.json.lock') are excluded from the digest by construction.

    Returns None if `registry_dir` (resolved) does not exist at all.
    """
    d = _resolve_dir(registry_dir)
    if not os.path.isdir(d):
        return None
    entries = []
    for dirpath, dirnames, filenames in os.walk(d):
        dirnames.sort()
        for name in sorted(filenames):
            if ".tmp-" in name or name in ("index.json.lock", "CURRENT.json.lock") or name.startswith("."):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, d).replace(os.sep, "/")
            raw = _read_raw_bytes(full)
            if raw is None:
                return None
            entries.append({"name": rel, "sha256": hashlib.sha256(raw).hexdigest()})
    entries.sort(key=lambda e: e["name"])
    return _digest({"files": entries})
