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

FULL_UNION_SCHEMA_ID = "mb/ninfty-evidence-union/full-union-report/v1"
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
                         "reason": "the resolved generation is not bound to the receiver's governing "
                                   "spec/contract/manifest trio -- see docs_era_binding"}
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
        "docs_era_binding": docs_detail,
        "note": ("all four roles resolved from ONE resolve_bundle call (single CURRENT read) -- a "
                 "mixed-generation four-tuple is structurally unreachable through this entry point"),
    }
    return overall, contents, summary


def _compose_full(r1_status, r2_status, r3nf_status, registry_status):
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

    overall = _compose_full(columns["R1"]["status"], columns["R2"]["status"], r3_status, registry_status)

    return {
        "schema_id": FULL_UNION_SCHEMA_ID,
        "raw_evidence_digest": sha256_of(raw) if isinstance(raw, dict) else None,
        "columns": columns,
        "column_order": list(ROUTE_COLUMNS),
        "frozen_union_report": frozen,
        "native_registry_status": frozen.get("native_registry_status"),
        "four_role_registry_status": registry_detail,
        "overall_full": overall,
        "composition_rule": ("intersection only -- overall_full == PASS iff R1, R2 and R3-NF are ALL PASS "
                             "and the four-role registry resolution is PASS; no column substitutes for "
                             "another (Sol 便95 F95-2.2)"),
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
