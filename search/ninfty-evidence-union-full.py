#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-evidence-union-full.py

FULL evidence union = R1 | R2 | R3-NF, three SEPARATE columns
(Sol 便95 sol_reply_95_math22.md F95-2.2 / P95-2.2 item 3).

WHY A SEPARATE FILE (and not an edit to search/ninfty-evidence-union.py):
F95-2.2 requires that R1/R2 stay historical frozen routes with byte- and
semantics-identical behaviour ("R1/R2 は歴史的 frozen route として byte/
意味論を維持する"). This module therefore

  - IMPORTS the frozen facade's single public name
    (`evidence_union_from_raw_w6`) and calls it EXACTLY as any other
    production caller would -- it never reaches into that module's
    private helpers, never re-implements its composition, and cannot
    change any status it returns;
  - adds R3-NF as an INDEPENDENT third column resolved and evaluated
    here, by search/ninfty-verifier-w6-r3nf.py;
  - composes ONLY by intersection (see `_compose_full`): the full union
    reaches PASS iff ALL THREE columns are PASS. No column is ever a
    substitute for, or a fallback for, another -- an ABSENT R3-NF does
    not inherit R1/R2's verdict, and an ABSENT R1/R2 is not rescued by a
    PASS R3-NF.

FAIL-CLOSED, deliberately: R3-NF's inputs (`nf_registry_refs`) are
REQUIRED. A raw artifact that simply omits them yields R3-NF = ABSENT and
therefore overall_full != PASS. "Field not supplied" is never read as
"check not applicable" (Sol 便95 ★教材: green workflow != green test; the
same discipline applies to a missing input).

SAME-GENERATION FOUR-ROLE INVARIANT (司令塔裁定 2026-08-01 item 5, and the
existing registry design): all FOUR artifacts backing a full union --
native_a, native_b, nf_a, nf_b -- are resolved from ONE generation by a
SINGLE `resolve_bundle` call here (`_resolve_four_roles`), so a mixed-
generation four-tuple is structurally unreachable through this entry
point, not merely checked for afterwards. The frozen facade separately
resolves native_a/native_b for its own R1/R2 evaluation (unchanged); this
module additionally asserts that the generation IT resolved is the one
CURRENT names and that every one of the four claimed artifact_ids is
present in it with the correct pinned role/status/digest/version/freeze.

RAW ARTIFACT SHAPE (a superset of the frozen facade's raw shape -- the
extra key is ignored by that facade, which validates required keys and
tolerates additional ones):

  {
    "schema_id": "mb/ninfty-evidence-union/raw-w6-evidence/v1",
    "certificate": {...}, "native_a": {...}, "native_b": {...},
    "native_registry_refs": {"native_a": {...}, "native_b": {...}},
    "nf_registry_refs": {
       "nf_a": {"artifact_id": <str>, "whole_artifact_digest": <64hex>,
                "version_id": <non-empty str>, "freeze_id": <non-empty str>},
       "nf_b": {...}
    }
  }

TERMINOLOGY (Sol 便95 F95-2.3): everything this module produces is a
DIAGNOSTIC CONSTRUCTION -- a union report. Nothing here mints or
publishes an artifact; minting/publication happens only behind the NF
mint gate in the provisioning path
(search/ninfty-ep-genuine-provisioning.py).

CALIBRATION (P95-2.2 item 4): no positive control exists for the EP
detector, so every report this module emits carries
`calibrated_detector: false` and `ep_status: "uncalibrated/UNKNOWN"`. A
PASS here is a statement about THIS artifact set, never a claim that the
pipeline has been shown able to detect a planted fault.

COMPOSITION (Sol 便97 W97-2.1/P97-2.1, report schema v2): an INTEGRITY
FAULT outranks every route/registry verdict UNCONDITIONALLY. The old form
escalated an era mismatch to INTEGRITY_STOP only when the routes happened
to compose to PASS, so an era fault CONCURRENT with a FAIL/ABSENT/CONFLICT
column vanished from the headline. Now `integrity_gate` is its own emitted
column: it always names the faults and always carries the pre-override
mathematical composition (`route_composition_status`), so neither fact can
mask the other.

CLI: python search/ninfty-evidence-union-full.py <raw.json>
Prints the canonical JSON report; exit 0 iff overall_full == "PASS"
(fail-closed CLI, same convention as the frozen facade's main()).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HEX64 = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)

# v2 (Sol 便97 P97-2.1): the emitted report gained the `integrity_gate`
# column AND the composition semantics changed (an integrity fault now
# outranks the route lattice unconditionally). A changed meaning of
# `overall_full` is not an additive tweak, so the report schema is
# superseded by version rather than mutated in place: a consumer pinned to
# v1 must not silently read a v2 report as if the old rule still held.
FULL_UNION_SCHEMA_ID = "mb/ninfty-evidence-union/full-union-report/v2"
FULL_UNION_SCHEMA_ID_V1 = "mb/ninfty-evidence-union/full-union-report/v1"
ROUTE_COLUMNS = ("R1", "R2", "R3-NF")

__all__ = ["evidence_union_full_from_raw"]

_MODULES = {}


def _load(alias, filename):
    if alias not in _MODULES:
        path = os.path.join(HERE, filename)
        spec = importlib.util.spec_from_file_location(alias, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MODULES[alias] = mod
    return _MODULES[alias]


FROZEN_UNION_CLI = "ninfty-evidence-union.py"


def _run_frozen_union(raw):
    """
    Runs the FROZEN R1/R2 facade as a SEPARATE OS PROCESS through its own
    CLI, feeding `raw` on stdin and parsing the JSON it prints.

    WHY A SUBPROCESS AND NOT A DYNAMIC LOAD (this is a repair, 便95 修理
    バンドル・後任実装係): the first draft of this module loaded
    `ninfty-evidence-union.py` with `importlib` and called its public
    `evidence_union_from_raw_w6`. That turned
    `test_ninfty_evidence_union.py` §8 RED -- Sol 便86 P86-2 item 1
    (B86-o1) is enforced STRUCTURALLY there, by asserting that NO other
    file under search/ contains a load site for that module at all. The
    check is not about which attribute is touched; it is about the load
    site being the only mechanism by which any attribute (public or
    private) becomes reachable, so "we only call the public name" does
    not satisfy it.

    Weakening that test to admit a public-name-only caller was rejected:
    it is a Sol-mandated invariant, and F95-2.2 (add a third route) gives
    no authority to relax 便86 (do not reach into the frozen facade).
    Running the frozen CLI as its own process satisfies BOTH: the third
    column is composed here, and the frozen module's address space is
    never entered by this one. It is also the project's own 探索器/照合器
    separation discipline applied to two verifier routes -- the same
    pattern `ninfty-nf-crosscheck.py` already uses for the two lanes.

    A NONZERO EXIT CODE IS EXPECTED and is NOT an error: the frozen CLI
    exits nonzero for any overall_status != PASS, which is the normal
    case here. Only an unparseable stdout is a failure, and it is
    reported as such (never silently turned into an ABSENT/PASS).
    """
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, FROZEN_UNION_CLI), "-"],
        input=canonical_serialize(raw), capture_output=True, encoding="utf-8",
    )
    try:
        return json.loads(proc.stdout), None
    except (ValueError, TypeError) as exc:
        return None, {"reason": "the frozen R1/R2 union CLI did not emit parseable JSON",
                      "exception": f"{type(exc).__name__}: {exc}",
                      "process_exit_code": proc.returncode,
                      "stdout_head": (proc.stdout or "")[:400],
                      "stderr_head": (proc.stderr or "")[:400]}


def _r3nf():
    return _load("ninfty_verifier_w6_r3nf", "ninfty-verifier-w6-r3nf.py")


def _registry():
    """Resolver-only registry module (no `write_entry` exists in it --
    provisioning lives in ninfty-native-registry-provisioning.py, Sol 便90
    F90-4.1 blocker 2)."""
    return _load("ninfty_native_registry_for_full_union", "ninfty-native-registry.py")


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _is_64hex(x):
    return isinstance(x, str) and bool(HEX64.match(x))


def _is_nonempty_str(x):
    return isinstance(x, str) and len(x) > 0


def _well_shaped_ref(ref):
    return (
        isinstance(ref, dict)
        and _is_nonempty_str(ref.get("artifact_id"))
        and _is_64hex(ref.get("whole_artifact_digest"))
        and _is_nonempty_str(ref.get("version_id"))
        and _is_nonempty_str(ref.get("freeze_id"))
    )


# Fixed priority for reporting ONE status when the four slots disagree
# (earlier wins). Every value here is non-operative for gating.
_SLOT_STATUS_PRIORITY = (
    "MALFORMED", "MISSING", "UNKNOWN", "REVOKED", "ROLE_MISMATCH", "STALE",
    "GENERATION_MISMATCH", "FREEZE_MISMATCH", "DOCS_ERA_UNBOUND",
)

# DOCS-ERA BINDING. A gen-receipt/v1 records only the generation's own
# artifacts: nothing in it says WHICH spec/contract/manifest era the
# generation was provisioned under, so a receiver cannot machine-bind "this
# EP generation belongs to the v19 docs trio" -- the same class of hole Sol
# names in W95-2.2 (a receipt not bound to the repo). gen-receipt/v2 adds a
# required `governing_docs` block pinning the three documents' exact
# sha256; the registry resolver validates its SHAPE (fail-closed in both
# directions, see ninfty-native-registry.py GEN_RECEIPT_SCHEMA_ID_V2) and
# deliberately does not compare it to any file, because a receiver may hold
# the registry without holding the docs tree. THIS consumer does hold the
# docs tree, so it recomputes all three from its own copies and requires
# agreement. A v1 receipt cannot reach PASS here: an absent binding is not
# a satisfied binding.
GOVERNING_DOC_PATHS = {
    "predicate_spec": "docs/week4-NInfty_stage2_spec_v19.md",
    "verifier_contract": "docs/mb_ninfty_verifier_contract_v14.md",
    "dependency_manifest": "docs/mb_dependency_manifest_v14.md",
}
GOVERNING_DOC_SLUGS = {
    "predicate_spec": "mb/ninfty-stage2-predicate/",
    "verifier_contract": "mb/ninfty-verifier-contract/",
    "dependency_manifest": "mb/dependency-manifest/",
}


def _receiver_docs():
    """Recomputes each governing document's sha256 from the receiver's OWN
    copy and reads the artifact id the document itself declares. The id is
    located STRUCTURALLY (id-assignment line, then H1 title) and never by
    scanning free prose -- each of these documents legitimately quotes
    SUPERSEDED ids in its own version-history table, so a prose scan would
    pick up whichever happened to appear first."""
    out, errors = {}, []
    repo_root = os.path.dirname(HERE)
    for key, rel in GOVERNING_DOC_PATHS.items():
        try:
            with open(os.path.join(repo_root, rel), "rb") as f:
                blob = f.read()
        except OSError as exc:
            errors.append(f"governing document {rel!r} unreadable by receiver: {exc}")
            continue
        text = blob.decode("utf-8", "replace")
        esc = re.escape(GOVERNING_DOC_SLUGS[key])
        m = (re.search(r'^\s*\w*id\s*=\s*"(' + esc + r'v\d+)"', text, re.M)
             or re.search(r"^#\s+`(" + esc + r"v\d+)`", text, re.M))
        if m is None:
            errors.append(f"governing document {rel!r} carries no structural artifact-id declaration "
                          f"matching {GOVERNING_DOC_SLUGS[key]!r}v<NN>")
        out[key] = {"path": rel, "sha256": hashlib.sha256(blob).hexdigest(),
                    "artifact_id": m.group(1) if m else None}
    return out, errors


def _check_docs_era(bundle):
    """Returns (ok, detail). Fail-closed on a v1 receipt, a missing block,
    or any digest/artifact_id disagreement with the receiver's own copies."""
    reg = _registry()
    receipt_schema_id = bundle.get("receipt_schema_id") if isinstance(bundle, dict) else None
    required = getattr(reg, "GEN_RECEIPT_SCHEMA_ID_V2", None)
    if receipt_schema_id != required:
        return False, {
            "ok": False,
            "receipt_schema_id": receipt_schema_id,
            "required_receipt_schema_id": required,
            "reason": ("the resolved generation's receipt does not pin the governing spec/contract/manifest "
                       "digests -- an absent binding is not a satisfied binding. Re-provision the generation "
                       "with `--governing-docs` (a gen-receipt/v2)."),
        }
    pinned = bundle.get("governing_docs") or {}
    mine, errors = _receiver_docs()
    per_doc = {}
    for key in sorted(GOVERNING_DOC_PATHS):
        claim, ours = pinned.get(key) or {}, mine.get(key) or {}
        digest_agrees = _is_64hex(claim.get("sha256")) and claim.get("sha256") == ours.get("sha256")
        id_agrees = claim.get("artifact_id") == ours.get("artifact_id")
        per_doc[key] = {"pinned_artifact_id": claim.get("artifact_id"),
                        "receiver_artifact_id": ours.get("artifact_id"),
                        "receiver_path": ours.get("path"),
                        "digest_agrees": digest_agrees, "artifact_id_agrees": id_agrees}
        if not digest_agrees:
            errors.append(f"governing_docs[{key!r}]: receipt-pinned sha256 does not match the receiver's own "
                          f"recomputation of {ours.get('path')!r}")
        if not id_agrees:
            errors.append(f"governing_docs[{key!r}]: receipt pins artifact_id {claim.get('artifact_id')!r}, "
                          f"the receiver's document declares {ours.get('artifact_id')!r}")
    ok = not errors
    return ok, {"ok": ok, "receipt_schema_id": receipt_schema_id, "documents": per_doc, "errors": errors}


# ---------------------------------------------------------------------------
# PAYLOAD-ERA MATRIX (Sol 便96 W96-2.2 / governing spec sec.5.3.4 /
# dependency manifest Y-3b).
#
# W96-2.2: `docs_era_binding_ok` only ever compared the RECEIPT's three
# control-plane document hashes with the receiver's own copies. It never
# looked at the version ids embedded in the PAYLOAD -- and those are v18:
# the certificate's predicate_spec_id/schema_id, both natives'
# native_schema_id, and the frozen verifier's own declared trio. So a green
# `docs_era_binding_ok` was being read as "the payload belongs to the v19
# era", which it never established.
#
# Sol offered two repairs and stated that the one consistent with keeping
# R1/R2 byte-frozen is (2): declare a versioned mixed-era compatibility
# matrix and have the consumer check the exact allowed combination PER
# PLANE. That is what this block does. The matrix itself is normative in
# governing spec sec.5.3.4; this is its consumer-side enforcement.
#
# Fail-closed everywhere: a plane whose era cannot be READ is FAIL, never
# "assumed compatible". An era NEWER than the matrix allows is equally
# FAIL -- no forward compatibility is declared anywhere.
# ---------------------------------------------------------------------------

FROZEN_ERA_DOC_PATHS = {
    "predicate_spec_id": "docs/week4-NInfty_stage2_spec_v18.md",
    "verifier_contract_id": "docs/mb_ninfty_verifier_contract_v13.md",
    "dependency_manifest_schema_id": "docs/mb_dependency_manifest_v13.md",
}
_ERA_KEY_SLUGS = {
    "predicate_spec_id": "mb/ninfty-stage2-predicate/",
    "verifier_contract_id": "mb/ninfty-verifier-contract/",
    "dependency_manifest_schema_id": "mb/dependency-manifest/",
}
# plane -> which era it must declare ("FROZEN" or "CURRENT"). BOTH eras are
# READ from files (the byte-frozen trio / the receiver's governing trio);
# no version number is typed in as a literal here.
PLANE_ERA = {
    "frozen_route_verifier": "FROZEN",
    "native_payload_schema": "FROZEN",
    "nf_route": "CURRENT",
    "decision_lane_predicate": "CURRENT",
    "control_plane": "CURRENT",
}
# Live (NON-frozen) sources carrying an `[ep-era-declaration]` marker. The
# frozen route verifier is deliberately absent: its bytes may not be
# touched, so its era is read from the EXPECTED_PINS block it already has.
ERA_MARKER_SOURCES = {
    "decision_lane_predicate": ["search/ninfty-checker.py", "search/ninfty-searcher-v2.mjs"],
    "nf_route": ["search/ninfty-verifier-w6-r3nf.py"],
    "native_payload_schema": ["search/ninfty-searcher-v2.mjs"],
}
_ERA_KEYS = ("predicate_spec_id", "verifier_contract_id", "dependency_manifest_schema_id")
_MARKER_RE = re.compile(
    r"\[ep-era-declaration\]\s+plane=(?P<plane>[a-z_]+)\s+"
    r"predicate_spec_id=(?P<predicate_spec_id>\S+)\s+"
    r"verifier_contract_id=(?P<verifier_contract_id>\S+)\s+"
    r"dependency_manifest_schema_id=(?P<dependency_manifest_schema_id>\S+)")


def _read_declared_id(rel, slug, errors):
    """Structural id read (id-assignment line, then H1 title) -- never a
    prose scan, for the same reason `_receiver_docs` gives."""
    try:
        with open(os.path.join(os.path.dirname(HERE), rel), "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError as exc:
        errors.append("{0}: unreadable ({1})".format(rel, exc))
        return None
    esc = re.escape(slug)
    m = (re.search(r'^\s*\w*id\s*=\s*"(' + esc + r'v\d+)"', text, re.M)
         or re.search(r"^#\s+`(" + esc + r"v\d+)`", text, re.M))
    if m is None:
        errors.append("{0}: no structural artifact-id declaration matching {1!r}v<NN>".format(rel, slug))
        return None
    return m.group(1)


def _era_definitions():
    """(eras, errors). FROZEN comes from the three byte-frozen documents,
    CURRENT from the receiver's own governing trio."""
    errors = []
    frozen = {k: _read_declared_id(FROZEN_ERA_DOC_PATHS[k], _ERA_KEY_SLUGS[k], errors) for k in _ERA_KEYS}
    mine, doc_errors = _receiver_docs()
    errors.extend(doc_errors)
    current = {
        "predicate_spec_id": (mine.get("predicate_spec") or {}).get("artifact_id"),
        "verifier_contract_id": (mine.get("verifier_contract") or {}).get("artifact_id"),
        "dependency_manifest_schema_id": (mine.get("dependency_manifest") or {}).get("artifact_id"),
    }
    if any(v is None for v in list(frozen.values()) + list(current.values())):
        errors.append("one or more era ids could not be read -- the matrix cannot be evaluated (fail-closed)")
    elif frozen == current:
        errors.append("FROZEN and CURRENT resolved to the SAME trio -- the matrix would be vacuous; "
                      "refusing to report PASS on a check that cannot discriminate")
    return {"FROZEN": frozen, "CURRENT": current}, errors


def _frozen_verifier_declared_era(errors):
    """Reads search/ninfty-verifier-b.py's own EXPECTED_PINS block. That file
    is BYTE-FROZEN, so it carries no `[ep-era-declaration]` marker and must
    never be given one."""
    rel = "search/ninfty-verifier-b.py"
    try:
        with open(os.path.join(os.path.dirname(HERE), rel), "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError as exc:
        errors.append("{0}: unreadable ({1})".format(rel, exc))
        return None
    out = {}
    for key in _ERA_KEYS:
        m = re.search(r'"' + re.escape(key) + r'"\s*:\s*"([^"]+)"', text)
        if m is None:
            errors.append("{0}: EXPECTED_PINS carries no {1!r}".format(rel, key))
            return None
        out[key] = m.group(1)
    return out


def _marker_eras(rel, errors):
    """All `[ep-era-declaration]` markers in one live source, keyed by plane."""
    try:
        with open(os.path.join(os.path.dirname(HERE), rel), "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError as exc:
        errors.append("{0}: unreadable ({1})".format(rel, exc))
        return {}
    out = {}
    for m in _MARKER_RE.finditer(text):
        out.setdefault(m.group("plane"), []).append({k: m.group(k) for k in _ERA_KEYS})
    return out


def _payload_era_from_raw(raw):
    """The era ids the PAYLOAD itself declares: the certificate's
    predicate_spec_id, its schema_id anchor, and both natives'
    native_schema_id."""
    observed, errors = {}, []
    cert = (raw or {}).get("certificate") if isinstance(raw, dict) else None
    if not isinstance(cert, dict):
        errors.append("raw evidence carries no certificate object -- payload era unreadable (fail-closed)")
        return observed, errors
    observed["certificate.predicate_spec_id"] = cert.get("predicate_spec_id")
    schema_id = cert.get("schema_id")
    suffix = "#cert-schema"
    if isinstance(schema_id, str) and schema_id.endswith(suffix):
        observed["certificate.schema_id"] = schema_id[: -len(suffix)]
    else:
        observed["certificate.schema_id"] = schema_id
        errors.append("certificate.schema_id is not a <spec-id>#cert-schema anchor: {0!r}".format(schema_id))
    for side, label in (("searcher_native", "certificate.searcher_native.native_schema_id"),
                        ("checker_native", "certificate.checker_native.native_schema_id")):
        native = cert.get(side)
        nid = native.get("native_schema_id") if isinstance(native, dict) else None
        if isinstance(nid, str) and nid.endswith(suffix):
            observed[label] = nid[: -len(suffix)]
        else:
            observed[label] = nid
            errors.append("{0} is not a <spec-id>#cert-schema anchor: {1!r}".format(label, nid))
    return observed, errors


def _check_payload_era_matrix(raw, control_plane_detail):
    """Returns (ok, detail). Never raises."""
    errors = []
    eras, era_errors = _era_definitions()
    errors.extend(era_errors)
    planes = {}

    def _expected(plane):
        return eras[PLANE_ERA[plane]]

    declared = _frozen_verifier_declared_era(errors)
    exp = _expected("frozen_route_verifier")
    ok = declared is not None and declared == exp
    if declared is not None and not ok:
        errors.append("plane 'frozen_route_verifier': search/ninfty-verifier-b.py declares {0}, "
                      "the matrix requires {1}".format(declared, exp))
    planes["frozen_route_verifier"] = {
        "status": "PASS" if ok else "FAIL",
        "required_era": PLANE_ERA["frozen_route_verifier"], "required": exp, "declared": declared,
        "source": "search/ninfty-verifier-b.py EXPECTED_PINS (byte-frozen: no marker may be added)",
    }

    for plane in ("nf_route", "decision_lane_predicate", "native_payload_schema"):
        exp = _expected(plane)
        per_source, plane_ok = {}, True
        sources = ERA_MARKER_SOURCES.get(plane) or []
        if not sources:
            plane_ok = False
            errors.append("plane {0!r}: no era-declaring source registered (fail-closed)".format(plane))
        for rel in sources:
            found = _marker_eras(rel, errors).get(plane) or []
            if len(found) != 1:
                plane_ok = False
                errors.append("plane {0!r}: {1} carries {2} '[ep-era-declaration] plane={0}' markers, "
                              "expected exactly 1 (a missing marker is FAIL, never 'compatible')"
                              .format(plane, rel, len(found)))
                per_source[rel] = {"status": "FAIL", "markers_found": len(found)}
                continue
            got = found[0]
            src_ok = (got == exp)
            if not src_ok:
                plane_ok = False
                errors.append("plane {0!r}: {1} declares {2}, the matrix requires {3}".format(plane, rel, got, exp))
            per_source[rel] = {"status": "PASS" if src_ok else "FAIL", "declared": got}
        planes[plane] = {"status": "PASS" if plane_ok else "FAIL", "required_era": PLANE_ERA[plane],
                         "required": exp, "sources": per_source}

    observed, obs_errors = _payload_era_from_raw(raw)
    errors.extend(obs_errors)
    exp_spec = _expected("native_payload_schema")["predicate_spec_id"]
    artefact = {}
    artefact_ok = bool(observed) and not obs_errors
    for label in sorted(observed):
        got = observed[label]
        hit = (got == exp_spec)
        artefact[label] = {"status": "PASS" if hit else "FAIL", "declared": got}
        if not hit:
            artefact_ok = False
            errors.append("plane 'native_payload_schema': {0} declares {1!r}, the matrix requires {2!r} "
                          "(R1/R2 read a byte-frozen payload schema -- spec sec.5.3.4 M-2)"
                          .format(label, got, exp_spec))
    planes["native_payload_schema"]["artefact_declarations"] = artefact
    if not artefact_ok:
        planes["native_payload_schema"]["status"] = "FAIL"

    cp_ok = bool((control_plane_detail or {}).get("ok"))
    cp_ids = {}
    for key, doc_key in (("predicate_spec_id", "predicate_spec"),
                         ("verifier_contract_id", "verifier_contract"),
                         ("dependency_manifest_schema_id", "dependency_manifest")):
        cp_ids[key] = (((control_plane_detail or {}).get("documents") or {}).get(doc_key) or {}).get("pinned_artifact_id")
    exp = _expected("control_plane")
    ids_ok = (cp_ids == exp)
    if cp_ok and not ids_ok:
        errors.append("plane 'control_plane': the receipt pins {0}, the matrix requires {1}".format(cp_ids, exp))
    planes["control_plane"] = {
        "status": "PASS" if (cp_ok and ids_ok) else "FAIL",
        "required_era": PLANE_ERA["control_plane"], "required": exp, "receipt_pinned": cp_ids,
        "note": ("this plane's DIGEST agreement is the separate column "
                 "control_plane_docs_receipt_binding (manifest Y-3a); here only its ERA is checked (Y-3b)"),
    }

    overall_ok = (not errors) and all(v.get("status") == "PASS" for v in planes.values())
    return overall_ok, {
        "ok": overall_ok,
        "schema_ref": "governing spec sec.5.3.4 PAYLOAD_ERA_MATRIX / dependency manifest Y-3b",
        "eras": eras,
        "planes": planes,
        "errors": errors,
        "note": ("PASS means every plane's declared era EXACTLY matches that plane's single allowed era. "
                 "It is NOT interchangeable with control_plane_docs_receipt_binding, and neither may "
                 "substitute for the other (spec sec.5.3.4 M-4)."),
    }


def _resolve_four_roles(raw):
    """
    Resolves ALL FOUR roles (native_a, native_b, nf_a, nf_b) from ONE
    generation via a SINGLE `resolve_bundle` call, cross-checking each
    caller claim against the registry's own pinned values. Returns
    (overall_status, contents_by_role, detail).

    `contents_by_role` carries the registry-pinned `content` for each role
    that reached PASS, and is absent for any role that did not (the R3-NF
    predicate treats a missing NF content as ABSENT, fail-closed by
    construction -- it is not given a fabricated substitute).

    The caller's claims live in `raw["native_registry_refs"]` (already
    independently re-checked by the frozen facade for its own R1/R2
    evaluation -- re-checked here too, because THIS module's
    four-role/same-generation invariant is its own responsibility) and
    `raw["nf_registry_refs"]`.
    """
    detail = {}
    if not isinstance(raw, dict):
        d = {"status": "MALFORMED", "reason": "raw evidence artifact is not an object"}
        return "MALFORMED", {}, {r: dict(d) for r in ("native_a", "native_b", "nf_a", "nf_b")}

    native_refs = raw.get("native_registry_refs")
    nf_refs = raw.get("nf_registry_refs")
    claims = {}
    for role, src, key in (("native_a", native_refs, "native_a"), ("native_b", native_refs, "native_b"),
                           ("nf_a", nf_refs, "nf_a"), ("nf_b", nf_refs, "nf_b")):
        ref = src.get(key) if isinstance(src, dict) else None
        if not _well_shaped_ref(ref):
            detail[role] = {
                "status": "MISSING",
                "reason": (
                    f"no well-shaped registry ref for role {role!r} ({{'artifact_id': <str>, "
                    "'whole_artifact_digest': <64hex>, 'version_id': <non-empty str>, 'freeze_id': "
                    "<non-empty str>}}). For nf_a/nf_b this is the REQUIRED R3-NF input (Sol 便95 "
                    "F95-2.2: 同世代 nf_a/nf_b role と各 digest を必須入力にする) -- an omitted ref is "
                    "never read as 'this route does not apply'."
                ),
            }
            continue
        claims[role] = ref

    contents = {}
    bundle = None
    if claims:
        bundle = _registry().resolve_bundle(sorted({ref["artifact_id"] for ref in claims.values()}))

    generation_id = bundle.get("generation_id") if isinstance(bundle, dict) else None
    bundle_freeze = bundle.get("freeze_id") if isinstance(bundle, dict) else None

    for role, ref in claims.items():
        entry = bundle["artifacts"].get(ref["artifact_id"]) if isinstance(bundle, dict) else None
        if entry is None:
            if bundle is None or not _registry().index_exists():
                detail[role] = {"status": "MISSING",
                                "reason": "the receiver-held registry store did not resolve to a generation at all"}
            else:
                detail[role] = {"status": "UNKNOWN",
                                "reason": f"artifact_id {ref['artifact_id']!r} is not in the CURRENT generation "
                                          f"({generation_id!r})"}
            continue
        if entry.get("status") != "ACTIVE":
            detail[role] = {"status": "REVOKED",
                            "reason": f"artifact_id {ref['artifact_id']!r} has registry status "
                                      f"{entry.get('status')!r}, not ACTIVE"}
            continue
        if entry.get("role") != role:
            detail[role] = {"status": "ROLE_MISMATCH",
                            "reason": f"artifact_id {ref['artifact_id']!r} is pinned with role "
                                      f"{entry.get('role')!r} but was claimed for {role!r} (role-swap guard; "
                                      "for nf_a/nf_b this is also the both-producer guard)"}
            continue
        if entry.get("whole_artifact_digest") != ref["whole_artifact_digest"]:
            detail[role] = {"status": "STALE",
                            "reason": f"claimed whole_artifact_digest for {role!r} does not match the "
                                      "receiver's currently-pinned artifact digest"}
            continue
        if entry.get("version_id") != ref["version_id"]:
            detail[role] = {"status": "STALE",
                            "reason": f"claimed version_id {ref['version_id']!r} != pinned "
                                      f"{entry.get('version_id')!r}"}
            continue
        if entry.get("freeze_id") != ref["freeze_id"]:
            detail[role] = {"status": "STALE",
                            "reason": f"claimed freeze_id {ref['freeze_id']!r} != pinned "
                                      f"{entry.get('freeze_id')!r}"}
            continue
        detail[role] = {"status": "PASS",
                        "reason": "resolved against the pinned registry artifact",
                        "artifact_id": ref["artifact_id"],
                        "generation_id": generation_id,
                        "freeze_id": entry.get("freeze_id")}
        contents[role] = entry.get("content")

    # Same-generation invariant. `resolve_bundle` already guarantees ONE
    # generation by construction; this is the explicit, independent
    # consumer-side assertion that all four roles were actually found in
    # THAT generation and share its freeze_id (defence in depth, exactly
    # like the frozen facade's cross-side freeze check).
    passed = [r for r in ("native_a", "native_b", "nf_a", "nf_b") if detail.get(r, {}).get("status") == "PASS"]
    if len(passed) == 4:
        freezes = {detail[r]["freeze_id"] for r in passed}
        gens = {detail[r]["generation_id"] for r in passed}
        if len(freezes) != 1 or len(gens) != 1:
            reason = (f"four-role same-generation invariant violated: freeze_ids={sorted(map(str, freezes))} "
                      f"generation_ids={sorted(map(str, gens))}")
            for r in passed:
                detail[r] = {"status": "FREEZE_MISMATCH" if len(freezes) != 1 else "GENERATION_MISMATCH",
                             "reason": reason}
            contents = {}

    # Docs-era binding: applied only once every role otherwise resolved, so
    # a resolution failure is never masked by (nor masks) a docs mismatch.
    docs_ok, docs_detail = _check_docs_era(bundle) if bundle is not None else (
        False, {"ok": False, "reason": "no generation resolved"})
    if all(detail.get(r, {}).get("status") == "PASS" for r in ("native_a", "native_b", "nf_a", "nf_b")) \
            and not docs_ok:
        for r in ("native_a", "native_b", "nf_a", "nf_b"):
            detail[r] = {"status": "DOCS_ERA_UNBOUND",
                         "reason": "the resolved generation's CONTROL-PLANE receipt is not bound to the "
                                   "receiver's governing spec/contract/manifest trio -- see "
                                   "control_plane_docs_receipt_binding. This says nothing about the "
                                   "PAYLOAD era; that is a separate column (payload_era_matrix)."}
        contents = {}

    statuses = {v["status"] for v in detail.values()}
    if statuses == {"PASS"} and len(detail) == 4:
        overall = "PASS"
    else:
        overall = next((s for s in _SLOT_STATUS_PRIORITY if s in statuses), "MISSING")
    summary = {
        "status": overall,
        "generation_id": generation_id,
        "freeze_id": bundle_freeze,
        "roles": detail,
        # 便96 W96-2.2 / spec sec.5.3.4 M-3: RENAMED from `docs_era_binding`.
        # The old name was read as "the payload belongs to the v19 docs
        # era", which this check has never established -- it compares the
        # receipt's three CONTROL-PLANE document hashes against the
        # receiver's own copies and nothing else.
        "control_plane_docs_receipt_binding": docs_detail,
        "note": ("all four roles resolved from ONE resolve_bundle call (single CURRENT read) -- a "
                 "mixed-generation four-tuple is structurally unreachable through this entry point"),
    }
    return overall, contents, summary


def _compose_route_registry(r1_status, r2_status, r3nf_status, registry_status):
    """
    INTERSECTION ONLY. overall_full == "PASS" iff every column is "PASS"
    and the four-role registry resolution is "PASS". Otherwise the report
    states, in a fixed priority, WHY it is not PASS -- and never
    substitutes one column's verdict for another's.

      1. any column MALFORMED, or registry non-PASS  -> INTEGRITY_STOP
      2. any column FAIL                             -> FAIL
      3. any column ABSENT                           -> ABSENT
      4. all three PASS (and registry PASS)          -> PASS

    Rule 1 puts a non-PASS registry resolution in the same bucket the
    frozen facade already uses for its own registry gate (INTEGRITY_STOP),
    for the same reason: unresolvable provenance is an integrity problem,
    not a mathematical FAIL.
    """
    cols = (r1_status, r2_status, r3nf_status)
    if registry_status != "PASS" or "MALFORMED" in cols or "INTEGRITY_STOP" in cols:
        return "INTEGRITY_STOP"
    if "CONFLICT" in cols:
        return "CONFLICT"
    if "FAIL" in cols:
        return "FAIL"
    if "ABSENT" in cols:
        return "ABSENT"
    if all(c == "PASS" for c in cols):
        return "PASS"
    return "INTEGRITY_STOP"


# The ONE integrity gate name reported when the payload-era matrix does not
# hold. Named (not a bare boolean) so the emitted report always says WHICH
# integrity fault forced the status, even when the mathematical composition
# was already non-PASS for an unrelated reason.
ERA_INTEGRITY_FAULT = "payload_era_matrix"


def _compose_full(r1_status, r2_status, r3nf_status, registry_status, era_ok):
    """
    Sol 便97 W97-2.1 / P97-2.1 REPAIR.

    The previous form was

        overall = _compose_route_registry(...)
        if overall == "PASS" and not era_ok:
            overall = "INTEGRITY_STOP"

    which raised an era mismatch to INTEGRITY_STOP ONLY when the routes
    happened to compose to PASS. With R1 FAIL (or ABSENT, CONFLICT,
    INTEGRITY_STOP) the era fault was silently dropped from the headline
    status: an untrusted-provenance fault was masked by a mathematical one.

    An era mismatch means the routes were evaluated against payloads from
    an era nobody declared compatible. That is a provenance/integrity fault
    about the INPUTS, so it outranks every verdict computed FROM those
    inputs. It is therefore the FIRST rule, evaluated before the route and
    registry lattice, unconditionally.

    `era_ok` is a REQUIRED argument and is compared with `is True`: an
    absent/None/truthy-but-not-True value is treated as a fault, never as a
    satisfied gate (an undefined era result is never read as PASS).

    The mathematical composition is NOT discarded -- the caller reports it
    verbatim in `integrity_gate.route_composition_status`, so the two facts
    (which columns failed, and that the payload era is untrusted) are always
    visible in separate fields.
    """
    if era_ok is not True:
        return "INTEGRITY_STOP"
    return _compose_route_registry(r1_status, r2_status, r3nf_status, registry_status)


def evidence_union_full_from_raw(raw):
    """
    THE public entry point of the full three-column union. Never raises.

    Returns:
      {
        "schema_id": FULL_UNION_SCHEMA_ID,
        "columns": {"R1": {...}, "R2": {...}, "R3-NF": {...}},
        "frozen_union_report": <the frozen facade's own report, verbatim>,
        "four_role_registry_status": {...},
        "overall_full": <PASS|FAIL|ABSENT|CONFLICT|INTEGRITY_STOP>,
        "calibrated_detector": false,
        "ep_status": "uncalibrated/UNKNOWN",
        ...
      }
    """
    frozen, frozen_error = _run_frozen_union(raw)
    if frozen is None:
        # The frozen routes could not be evaluated AT ALL. Fail closed:
        # both columns become MALFORMED (a route whose verifier could not
        # be run is not an ABSENT input and is certainly not a PASS), and
        # the error is reported verbatim rather than summarized away.
        frozen = {"route1_status": "MALFORMED", "route1_detail": frozen_error,
                  "route2_status": "MALFORMED", "route2_detail": frozen_error,
                  "overall_status": "INTEGRITY_STOP",
                  "native_registry_status": {"status": "MALFORMED", "detail": frozen_error}}

    registry_status, contents, registry_detail = _resolve_four_roles(raw)
    r3_status, r3_detail = _r3nf().verify_R3_NF(contents.get("nf_a"), contents.get("nf_b"))

    columns = {
        "R1": {
            "status": frozen.get("route1_status"),
            "detail": frozen.get("route1_detail"),
            "source": "search/ninfty-evidence-union.py (frozen facade, R1 = recomputation route)",
            "implementation_source_digest": _file_sha256(os.path.join(HERE, "ninfty-verifier-b.py")),
        },
        "R2": {
            "status": frozen.get("route2_status"),
            "detail": frozen.get("route2_detail"),
            "source": "search/ninfty-evidence-union.py (frozen facade, R2 = witness-coverage route)",
            "implementation_source_digest": _file_sha256(os.path.join(HERE, "ninfty-verifier-w6-r2.py")),
        },
        "R3-NF": {
            "status": r3_status,
            "detail": r3_detail,
            "source": "search/ninfty-verifier-w6-r3nf.py (new route, Sol 便95 F95-2.2)",
            "implementation_source_digest": _file_sha256(os.path.join(HERE, "ninfty-verifier-w6-r3nf.py")),
        },
    }

    # Sol 便96 W96-2.2 / spec sec.5.3.4: the payload-era matrix is a SEPARATE
    # column from the control-plane receipt binding, and it participates in
    # the composition -- an era mismatch means the routes were evaluated
    # against payloads from an era nobody declared compatible, which is an
    # integrity fault, not a mathematical FAIL.
    era_ok, era_detail = _check_payload_era_matrix(
        raw, (registry_detail or {}).get("control_plane_docs_receipt_binding"))

    # 便97 W97-2.1: the era gate is now UNCONDITIONAL and outranks the route
    # lattice (see _compose_full). The pre-override mathematical composition
    # is kept and reported in its own field so that raising the headline to
    # INTEGRITY_STOP never erases which columns had failed, and a concurrent
    # column FAIL never hides the integrity fault.
    route_composition = _compose_route_registry(
        columns["R1"]["status"], columns["R2"]["status"], r3_status, registry_status)
    overall = _compose_full(columns["R1"]["status"], columns["R2"]["status"],
                            r3_status, registry_status, era_ok)
    integrity_faults = [] if era_ok is True else [ERA_INTEGRITY_FAULT]

    return {
        "schema_id": FULL_UNION_SCHEMA_ID,
        "raw_evidence_digest": sha256_of(raw) if isinstance(raw, dict) else None,
        "columns": columns,
        "column_order": list(ROUTE_COLUMNS),
        "frozen_union_report": frozen,
        "native_registry_status": frozen.get("native_registry_status"),
        "four_role_registry_status": registry_detail,
        "payload_era_matrix": era_detail,
        "overall_full": overall,
        # 便97 W97-2.1 / P97-2.1: the integrity gate is a SEPARATE column. It
        # is emitted on every run, PASS or not, so an integrity fault can
        # never be absorbed by (or absorb) a mathematical verdict.
        "integrity_gate": {
            "payload_era_matrix_ok": era_ok is True,
            "integrity_faults": integrity_faults,
            "route_composition_status": route_composition,
            "overall_full": overall,
            "rule": ("an integrity fault outranks every route/registry verdict UNCONDITIONALLY: "
                     "integrity_faults != [] => overall_full == INTEGRITY_STOP, whatever "
                     "route_composition_status is (Sol 便97 P97-2.1). route_composition_status is the "
                     "pre-override mathematical composition and is reported verbatim, so raising the "
                     "headline never erases which columns failed, and a FAIL/ABSENT/CONFLICT column "
                     "never hides the integrity fault. `payload_era_matrix_ok` is a strict `is True` "
                     "test: an undefined era result is a fault, not a PASS"),
        },
        "composition_rule": ("integrity first, then intersection: any integrity fault "
                             "(integrity_gate.integrity_faults -- currently payload_era_matrix) forces "
                             "overall_full == INTEGRITY_STOP REGARDLESS of the route/registry statuses "
                             "(Sol 便97 W97-2.1/P97-2.1: the old form only escalated when the routes "
                             "happened to compose to PASS, so an era fault concurrent with a FAIL/ABSENT/"
                             "CONFLICT column was masked). Otherwise intersection only -- overall_full == "
                             "PASS iff R1, R2 and R3-NF are ALL PASS, the four-role registry resolution "
                             "is PASS, AND payload_era_matrix.ok is true; "
                             "no column substitutes for another (Sol 便95 F95-2.2, 便96 W96-2.2). "
                             "control_plane_docs_receipt_binding (manifest Y-3a) and payload_era_matrix "
                             "(Y-3b) are DISTINCT: neither may be reported as the other, and neither "
                             "closes W-6 (便96 W96-2.3)"),
        "artifact_class": ("diagnostic construction (a union report) -- this module mints and publishes "
                           "nothing; minted/published artifacts come only from the NF-gated provisioning "
                           "path (Sol 便95 F95-2.3 terminology separation)"),
        "calibrated_detector": False,
        "ep_status": "uncalibrated/UNKNOWN",
        "calibration_note": ("no full-path positive control exists (Sol 便95 P95-2.2 item 4 remains open) -- "
                             "a PASS here is a statement about THIS artifact set, not evidence that the "
                             "pipeline can detect a planted fault"),
        "cross_checked_not_verified": True,
    }


def main(argv):
    ap = argparse.ArgumentParser(description="Full three-column (R1|R2|R3-NF) N∞ evidence union.")
    ap.add_argument("raw_evidence_json", help="path to a raw evidence artifact JSON, or '-' for stdin")
    args = ap.parse_args(argv)
    if args.raw_evidence_json == "-":
        raw = json.load(sys.stdin)
    else:
        with open(args.raw_evidence_json, "r", encoding="utf-8") as f:
            raw = json.load(f)
    result = evidence_union_full_from_raw(raw)
    print(canonical_serialize(result))
    return 0 if result.get("overall_full") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
