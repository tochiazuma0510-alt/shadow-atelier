#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-manifest-compiler.py

Manifest compiler gate (裁定124, 司令塔便76修理1 = Sol P76-3).

PROBLEM THIS FIXES (sol/sol_reply_76_math3.md F76-5.1/5.2/5.3, F6 total FAIL):
  - F76-5.1: both lane manifests declared their TOP-LEVEL record as
    build_record_present=false with null build fields. dependency-manifest
    v13 sec.2.34 [branch-contract] has NO false branch for the top-level
    record -- D-3/D-4' preimage is unconditionally mandatory there (only
    manifest_entry records may be bootstrap leaves). A false top-level is a
    schema violation, not a legitimate QD-3 case.
  - F76-5.2: lane B's entries kept `build_root_id: null` (an explicit key
    with a null value) alongside build_record_present=false. [branch-contract]
    requires forbidden keys to be LITERALLY ABSENT (key not present at all);
    null is QD-4 ("nonempty"), i.e. digest-mismatch [12], not a legal false
    record.
  - F76-5.3: lane B's stdlib entries used symbolic strings
    ("stdlib:fractions" etc.) as content_digest, not an exact 64-hex digest
    of real bytes. No canonical binary-face set can be built from a string
    that is not a content digest.

ROLE: this compiler is NOT a lane implementation. It is a receiving-side
tool (P76-3) that takes the frozen [branch-contract] rules + real file
bytes it can read (both lanes' source files, python stdlib module files)
and MACHINE-GENERATES true/false records, then VALIDATES them before
anything downstream (ninfty-ep-runner.py) is allowed to invoke either
verifier. It does not edit lane A/B source files; it writes DRAFT manifest
files for the lane authors to review/adopt (task brief: "lane 実装には触
れない -- manifest だけ受領側で再構成し、lane 著者の確認に回す前提の draft").

Gate (P76-3, verbatim): after generation, check (a) forbidden-key literal
absence, (b) all digests are exact 64-hex, (c) top-level never uses the
false branch. If ANY record fails ANY of these, the gate FAILS and the
caller (ninfty-ep-runner.py) MUST NOT invoke the verifiers on this manifest
pair.

Usage: python search/ninfty-manifest-compiler.py
Output: prints gate results; writes
  search/certs/laneA_manifest_v2_draft.json
  search/certs/laneB_manifest_v2_draft.json
Exit code: 0 if both lanes' compiled manifests pass the gate, 1 otherwise.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ROOT / "search"
CERTS = SEARCH / "certs"

HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

# --- [branch-contract] literal, dependency-manifest v13 sec.2.34 -----------
# (encoded as rule sets, not a markdown parser; the RULES themselves are
# quoted verbatim in the module docstring segments below for cross-reference)

TRUE_REQUIRED_KEYS = [
    "build_record_present", "build_definition_blob_digest",
    "pinned_input_digests", "build_root_id", "subject_build_binding_digest",
    "source_artifact_digests", "toolchain_digest", "build_step_digests",
]
FALSE_REQUIRED_KEYS = [
    "build_record_present", "source_artifact_digests", "toolchain_digest", "build_step_digests",
]
FALSE_FORBIDDEN_KEYS = [
    "build_definition_blob_digest", "pinned_input_digests", "build_root_id", "subject_build_binding_digest",
]


# ---------------------------------------------------------------------------
# canonical serialize + D-1..D-4' (dependency-manifest v13 sec.2.2, frozen)
# ---------------------------------------------------------------------------

def canonical_serialize(obj):
    def sort(x):
        if isinstance(x, list):
            return [sort(y) for y in x]
        if isinstance(x, dict):
            return {k: sort(x[k]) for k in sorted(x.keys())}
        return x
    return json.dumps(sort(obj), separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def d1_source_closure(source_artifact_digests):
    return sha256_of(sorted(set(source_artifact_digests or [])))


def d2_implementation_lineage(source_artifact_digests, toolchain_digest, build_step_digests):
    return sha256_of({
        "source": sorted(set(source_artifact_digests or [])),
        "toolchain": toolchain_digest,
        "steps": list(build_step_digests or []),
    })


def d3_build_root_id(build_definition_blob_digest, pinned_input_digests):
    return sha256_of({
        "build_definition": build_definition_blob_digest,
        "pinned_inputs": sorted(set(pinned_input_digests or [])),
    })


def d4prime_subject_build_binding(subject, build_definition_blob_digest, pinned_input_digests):
    return sha256_of({
        "subject": subject,
        "build_definition": build_definition_blob_digest,
        "pinned_inputs": sorted(set(pinned_input_digests or [])),
    })


# ---------------------------------------------------------------------------
# real-byte content digest resolution
# ---------------------------------------------------------------------------

def file_digest(rel_path):
    p = ROOT / rel_path
    return sha256_bytes(p.read_bytes())


def python_stdlib_module_digest(modname):
    """Real content digest of a pure-python stdlib module's source file.
    Returns (digest_or_None, note). None means the module has no importable
    .py source (e.g. built-in C modules like `sys`) -- an honest UNKNOWN,
    not a fabricated digest."""
    try:
        mod = importlib.import_module(modname)
    except ImportError as e:
        return None, f"import failed: {e}"
    f = getattr(mod, "__file__", None)
    if f is None:
        return None, f"{modname} has no __file__ (built-in/compiled-in module; no separate source file to hash)"
    return sha256_bytes(Path(f).read_bytes()), f"real sha256 of {f}"


# ---------------------------------------------------------------------------
# record builders
# ---------------------------------------------------------------------------

def build_true_record(subject_digest, source_artifact_digests, toolchain_digest,
                       build_step_digests, build_definition_obj, pinned_input_digests):
    build_definition_blob_digest = sha256_of(build_definition_obj)
    pinned = sorted(set(pinned_input_digests or []))
    build_root_id = d3_build_root_id(build_definition_blob_digest, pinned)
    subject_build_binding_digest = d4prime_subject_build_binding(subject_digest, build_definition_blob_digest, pinned)
    return {
        "build_record_present": True,
        "build_definition_blob_digest": build_definition_blob_digest,
        "pinned_input_digests": pinned,
        "build_root_id": build_root_id,
        "subject_build_binding_digest": subject_build_binding_digest,
        "source_artifact_digests": sorted(set(source_artifact_digests or [])),
        "toolchain_digest": toolchain_digest,
        "build_step_digests": list(build_step_digests or []),
        "_build_definition_obj": build_definition_obj,  # kept for lane-author review, not a schema key
    }


def build_false_record(source_artifact_digests, toolchain_digest, build_step_digests):
    return {
        "build_record_present": False,
        "source_artifact_digests": sorted(set(source_artifact_digests or [])),
        "toolchain_digest": toolchain_digest,
        "build_step_digests": list(build_step_digests or []),
        # build_definition_blob_digest / pinned_input_digests / build_root_id /
        # subject_build_binding_digest are LITERALLY OMITTED (not set to None).
    }


# ---------------------------------------------------------------------------
# validation gate (P76-3)
# ---------------------------------------------------------------------------

def validate_record(record, *, is_top_level, label):
    violations = []
    is_true = record.get("build_record_present")

    if is_top_level and is_true is not True:
        violations.append(f"[F76-5.1] {label}: top-level record uses build_record_present={is_true!r}, "
                           f"but [branch-contract] has no false branch for the top level -- top-level "
                           f"D-3/D-4' preimage is unconditionally mandatory.")
        return violations  # nothing else is checkable meaningfully

    if is_true is True:
        for k in TRUE_REQUIRED_KEYS:
            if k not in record:
                violations.append(f"[schema] {label}: true-branch record missing required key {k!r}")
        for k in ("build_definition_blob_digest", "build_root_id", "subject_build_binding_digest", "toolchain_digest"):
            v = record.get(k)
            if v is not None and not HEX64_RE.match(v):
                violations.append(f"[F76-5.3] {label}: {k}={v!r} is not a 64-hex digest")
        for k in ("pinned_input_digests", "source_artifact_digests"):
            for item in record.get(k) or []:
                if not HEX64_RE.match(item):
                    violations.append(f"[F76-5.3] {label}: {k} contains non-64-hex item {item!r}")
    elif is_true is False:
        for k in FALSE_REQUIRED_KEYS:
            if k not in record:
                violations.append(f"[schema] {label}: false-branch record missing required key {k!r}")
        for k in FALSE_FORBIDDEN_KEYS:
            if k in record:
                violations.append(f"[F76-5.2] {label}: false-branch record has forbidden key {k!r} present "
                                   f"(value={record[k]!r}) -- must be LITERALLY ABSENT, not null/present.")
        toolchain = record.get("toolchain_digest")
        if toolchain is not None and not HEX64_RE.match(toolchain):
            violations.append(f"[F76-5.3] {label}: toolchain_digest={toolchain!r} is not a 64-hex digest")
        for k in ("source_artifact_digests", "build_step_digests"):
            for item in record.get(k) or []:
                if not HEX64_RE.match(item):
                    violations.append(f"[F76-5.3] {label}: {k} contains non-64-hex item {item!r}")
    else:
        violations.append(f"[schema] {label}: build_record_present={is_true!r} is neither true nor false")

    return violations


def validate_entry_content_digest(content_digest, label):
    if not HEX64_RE.match(content_digest or ""):
        return [f"[F76-5.3] {label}: content_digest={content_digest!r} is not an exact 64-hex content digest"]
    return []


# ---------------------------------------------------------------------------
# lane A compilation
# ---------------------------------------------------------------------------

def compile_lane_a():
    violations = []
    searcher_digest = file_digest("search/ninfty-searcher-v2.mjs")
    verifier_a_digest = file_digest("search/ninfty-verifier-a.mjs")
    fixtures_digest = file_digest("search/certs/fixtures-lanea.mjs")
    selftest_digest = file_digest("search/ninfty-selftest-lanea.mjs")
    ep_sample_path = SEARCH / "certs" / "laneA_ep_export_sample.json"
    entries_files = [
        ("search/ninfty-searcher-v2.mjs", searcher_digest, "math-helper"),
        ("search/ninfty-verifier-a.mjs", verifier_a_digest, "math-helper"),
        ("search/certs/fixtures-lanea.mjs", fixtures_digest, "data-table"),
        ("search/ninfty-selftest-lanea.mjs", selftest_digest, "build-tool"),
    ]
    if ep_sample_path.exists():
        entries_files.append(("search/certs/laneA_ep_export_sample.json", file_digest("search/certs/laneA_ep_export_sample.json"), "data-table"))

    # toolchain: node runtime binary digest is not resolvable from pure python
    # without shelling out to hash node.exe itself; node's own manifest entry
    # already carries a real-looking 64-hex value from the lane-A implementer.
    # We re-validate its FORM here (64-hex) but cannot independently confirm
    # it against the actual node.exe bytes from this script -- recorded as
    # UNKNOWN (not silently accepted as verified).
    toolchain_digest = "17eb1fb58bd26a28850ff0e39c4baa09054d45a819cf2ec3a0ed41917c549bb2"
    toolchain_note = ("UNKNOWN: not independently re-hashed against the actual node.exe binary by this "
                       "compiler (would require locating and hashing the node runtime binary itself); "
                       "form-validated as 64-hex only.")

    # subject_code_digest: this compiler defines it, for the top-level record,
    # as the composite of the two files that constitute the frozen
    # predicate+verifier logic (searcher-v2.mjs + verifier-a.mjs), NOT
    # reusing the previously hand-authored subject_code_digest (whose
    # derivation formula was undocumented). This is a MODELING CHOICE flagged
    # for lane-author confirmation, not a silent redefinition.
    subject_code_digest = sha256_of({"searcher": searcher_digest, "verifier_a": verifier_a_digest})

    build_definition_obj = {
        "kind": "direct-interpretation",
        "description": "single ES module files executed directly by the node runtime named in toolchain_digest; "
                        "no transpile/bundle/minify/codegen step exists for lane A.",
    }
    # pinned_input_digests for a no-transform build: the only input that
    # governs execution semantics is the toolchain itself. MODELING CHOICE,
    # flagged for lane-author confirmation.
    pinned_input_digests = [toolchain_digest]

    entry_records = []
    for src_ref, digest, role in entries_files:
        rec = build_false_record(
            source_artifact_digests=[],
            toolchain_digest=toolchain_digest,
            build_step_digests=[],
        )
        rec["content_digest"] = digest
        rec["role"] = role
        rec["provenance"] = {"source_ref": src_ref}
        d1, d2 = d1_source_closure(rec["source_artifact_digests"]), d2_implementation_lineage(
            rec["source_artifact_digests"], rec["toolchain_digest"], rec["build_step_digests"])
        rec["source_closure_digest"] = d1
        rec["implementation_lineage_digest"] = d2
        entry_records.append(rec)
        violations.extend(validate_record(rec, is_top_level=False, label=f"laneA entry {src_ref}"))
        violations.extend(validate_entry_content_digest(digest, f"laneA entry {src_ref}"))

    top_record = build_true_record(
        subject_digest=subject_code_digest,
        source_artifact_digests=[],
        toolchain_digest=toolchain_digest,
        build_step_digests=[],
        build_definition_obj=build_definition_obj,
        pinned_input_digests=pinned_input_digests,
    )
    top_record["subject_id"] = "lane-A/ninfty-searcher-v2+verifier-a"
    top_record["subject_code_digest"] = subject_code_digest
    violations.extend(validate_record(top_record, is_top_level=True, label="laneA top-level"))

    manifest = {
        "schema_id": "mb/dependency-manifest/v13",
        "schema_digest": "df59b25f75e8e48a4607ed39177e5aa15be5a3fd4c738391aec347d8f7c1cb3e",
        "_compiler_note": "MACHINE-GENERATED DRAFT by search/ninfty-manifest-compiler.py (裁定124/P76-3). "
                           "Top-level uses the TRUE branch (F76-5.1 fix): build_definition_blob_digest/"
                           "pinned_input_digests/build_root_id/subject_build_binding_digest are real "
                           "computed digests, not null. subject_code_digest and pinned_input_digests are "
                           "MODELING CHOICES (see build_definition/_build_definition_obj) pending lane-A "
                           "author confirmation -- this is a draft, not an authoritative replacement.",
                           "toolchain_digest_note": toolchain_note,
        **top_record,
        "entries": entry_records,
    }
    return manifest, violations


# ---------------------------------------------------------------------------
# lane B compilation
# ---------------------------------------------------------------------------

def compile_lane_b():
    violations = []
    verifier_b_digest = file_digest("search/ninfty-verifier-b.py")
    checker_digest = file_digest("search/ninfty-checker.py")

    toolchain_digest = sha256_bytes(Path(sys.executable).read_bytes())
    toolchain_note = f"real sha256 of the running CPython interpreter binary ({sys.executable})"

    subject_code_digest = verifier_b_digest  # matches the file's own real bytes (verified against disk)

    build_definition_obj = {
        "kind": "direct-interpretation",
        "description": "single interpreted .py files run directly by the CPython interpreter named in "
                        "toolchain_digest; no compile/link/codegen step exists for lane B.",
    }
    pinned_input_digests = [toolchain_digest]

    stdlib_entries = []
    stdlib_gap_notes = []
    for modname, role in [("fractions", "runtime"), ("hashlib", "hash-primitive"),
                          ("json", "serialization"), ("argparse", "runtime")]:
        digest, note = python_stdlib_module_digest(modname)
        stdlib_entries.append((modname, digest, role, note))
        if digest is None:
            stdlib_gap_notes.append(f"{modname}: {note}")

    # `sys` has no separate source file (built into the interpreter binary
    # itself). MODELING CHOICE: its content identity is bound to the
    # interpreter binary already tracked as toolchain_digest -- NOT a
    # fabricated separate digest, but an explicit equivalence, flagged for
    # lane-author confirmation.
    sys_digest = toolchain_digest
    sys_note = "no separate source file; sys is compiled into the CPython interpreter binary itself -- " \
               "content identity modeled as equal to toolchain_digest (compiler-side equivalence, flagged for review), not fabricated."

    entry_specs = [
        ("search/ninfty-verifier-b.py", verifier_b_digest, "math-helper", [verifier_b_digest]),
        ("search/ninfty-checker.py", checker_digest, "math-helper", [checker_digest]),
    ]
    for modname, digest, role, note in stdlib_entries:
        entry_specs.append((f"python stdlib: {modname}", digest, role, []))
    entry_specs.append(("python stdlib: sys (see note)", sys_digest, "runtime", []))

    entry_records = []
    for src_ref, digest, role, source_artifacts in entry_specs:
        rec = build_false_record(
            source_artifact_digests=source_artifacts,
            toolchain_digest=toolchain_digest,
            build_step_digests=[],
        )
        rec["content_digest"] = digest if digest is not None else "UNKNOWN-no-real-digest-available"
        rec["role"] = role
        rec["provenance"] = {"source_ref": src_ref}
        rec["_content_digest_note"] = sys_note if src_ref.startswith("python stdlib: sys") else (
            [n for m, d, r, n in stdlib_entries if f"python stdlib: {m}" == src_ref] or [None])[0]
        if digest is not None:
            d1, d2 = d1_source_closure(rec["source_artifact_digests"]), d2_implementation_lineage(
                rec["source_artifact_digests"], rec["toolchain_digest"], rec["build_step_digests"])
            rec["source_closure_digest"] = d1
            rec["implementation_lineage_digest"] = d2
        entry_records.append(rec)
        violations.extend(validate_record(rec, is_top_level=False, label=f"laneB entry {src_ref}"))
        violations.extend(validate_entry_content_digest(rec["content_digest"], f"laneB entry {src_ref}"))

    top_record = build_true_record(
        subject_digest=subject_code_digest,
        source_artifact_digests=[],
        toolchain_digest=toolchain_digest,
        build_step_digests=[],
        build_definition_obj=build_definition_obj,
        pinned_input_digests=pinned_input_digests,
    )
    top_record["subject_id"] = "search/ninfty-verifier-b.py"
    top_record["subject_code_digest"] = subject_code_digest
    violations.extend(validate_record(top_record, is_top_level=True, label="laneB top-level"))

    manifest = {
        "schema_id": "mb/dependency-manifest/v13",
        "schema_digest": "df59b25f75e8e48a4607ed39177e5aa15be5a3fd4c738391aec347d8f7c1cb3e",
        "_compiler_note": "MACHINE-GENERATED DRAFT by search/ninfty-manifest-compiler.py (裁定124/P76-3). "
                           "Top-level uses the TRUE branch (F76-5.1 fix). stdlib entries now carry REAL "
                           "64-hex content digests (F76-5.3 fix) for fractions/hashlib/json/argparse "
                           "(hashed directly from the running interpreter's stdlib files); `sys` has no "
                           "separate source file and is modeled as identical to toolchain_digest (flagged). "
                           "build_root_id is OMITTED (not null) from all false-branch entries (F76-5.2 fix).",
        "toolchain_digest_note": toolchain_note,
        "stdlib_gap_notes": stdlib_gap_notes,
        **top_record,
        "entries": entry_records,
    }
    return manifest, violations


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    overall_ok = True
    results = {}
    for lane_name, compile_fn, out_name in [
        ("laneA", compile_lane_a, "laneA_manifest_v2_draft.json"),
        ("laneB", compile_lane_b, "laneB_manifest_v2_draft.json"),
    ]:
        manifest, violations = compile_fn()
        gate_passed = len(violations) == 0
        overall_ok = overall_ok and gate_passed
        out_path = CERTS / out_name
        out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        results[lane_name] = {"gate_passed": gate_passed, "violations": violations, "draft_path": str(out_path)}
        print(f"=== {lane_name} compiler gate: {'PASS' if gate_passed else 'FAIL'} ===")
        for v in violations:
            print("  VIOLATION:", v)
        print(f"  wrote {out_path}")

    print(f"\noverall gate: {'PASS' if overall_ok else 'FAIL'}")
    if not overall_ok:
        print("GATE FAILED -- caller must NOT invoke verifiers against these manifests.")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
