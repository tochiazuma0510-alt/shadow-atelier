#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/certs/build_full_witness_evidence.py

Builds the FULL WITNESS-BEARING raw evidence artifact for the three-column
union (Sol 便95 P95-2.2 item 3: "genuine fixture から full witness-bearing
certificate を作り、registry resolution だけでなく R1/R2(および認可後の
R3-NF)が期待 status に達すること").

EVERY value in the output is MACHINE-GENERATED here -- no hand-copied
digest, no hand-written witness. Sources, all of them real:

  1. the genuine candidate fixture search/fixtures/ninfty/checker_pos_01.json
     (one of the three genuine fixtures the 2026-08-01 provisioning batch
     used; NOT search/certs/full_witness_fixture_01.json, which the
     2026-08-01 audit found to belong to a DIFFERENT, older lineage
     (裁定133/137 witness-gen era) and which is therefore not reused for
     anything here -- 司令塔裁定 2026-08-01 item 4);
  2. lane A's OWN real generateCertificate output, via
     search/certs/gen_full_cert_base.mjs (a node subprocess -- this script
     does not reimplement any lane);
  3. the receiver-held registry's CURRENT generation, via
     search/ninfty-native-registry.py's resolver-only `resolve_bundle`
     (ONE call, so all four roles come from ONE generation).

WHAT THIS SCRIPT REPLACES IN THE BASE CERTIFICATE, and why:

lane A's generator emits every ref as an INLINE-ONLY ref
(`makeRef` -> {artifact_id: 'mb/ninfty-lanea/inline-artifact/...', digest,
object_id, inline}) with NO `json_pointer`. Against the receiver-held
registry that is the LEGACY_UNVERIFIED_REF path (Sol 便88 P88-o item 5(f)):
an inline-only ref never dereferences into the pinned artifact, so it can
never certify native provenance, and the union's registry gate correctly
refuses to let such a certificate reach PASS. A full witness-bearing
certificate must therefore bind its W-6 map_refs to the REGISTRY artifacts
by `artifact_id` + `json_pointer`, with the digest recomputed by the
receiver from the dereferenced value. This script rewrites exactly the two
W-6 entries (searcher/checker) to that registry-bound form, and rebuilds
the checker-lane entry from the GENUINE lane-B native artifact (the base
generator passes lane A's native into both slots -- documented in
gen_full_cert_base.mjs's own comment -- which is not a cross-lane witness
at all).

Everything else in the base certificate is passed through UNCHANGED.

HONEST STATUS OF THE RESULT: this script does not choose, tune, or assert
what status R1/R2/R3-NF reach. It emits the artifact; the union CLI
reports the statuses. See the emitted `_note` field and the repair cert
for the machine-observed outcome.

Usage:
  python search/certs/build_full_witness_evidence.py [--fixture checker_pos_01]
      [--out search/certs/ep_ci_full_witness_evidence_20260801.json]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH = os.path.dirname(HERE)
REPO = os.path.dirname(SEARCH)

RAW_W6_EVIDENCE_SCHEMA_ID = "mb/ninfty-evidence-union/raw-w6-evidence/v1"


def _load(alias, path):
    spec = importlib.util.spec_from_file_location(alias, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _resolve_json_pointer(root, pointer):
    """RFC 6901, same algorithm the verifiers use (independent copy -- this
    script must compute the SAME digest the receiver will recompute)."""
    if pointer == "":
        return True, root
    node = root
    for step in pointer.split("/")[1:]:
        step = step.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            try:
                idx = int(step)
            except ValueError:
                return False, None
            if idx < 0 or idx >= len(node):
                return False, None
            node = node[idx]
            continue
        if not isinstance(node, dict) or step not in node:
            return False, None
        node = node[step]
    return True, node


def _registry_ref(artifact_id, entry):
    return {
        "artifact_id": artifact_id,
        "whole_artifact_digest": entry["whole_artifact_digest"],
        "version_id": entry["version_id"],
        "freeze_id": entry["freeze_id"],
    }


def _bound_map_ref(artifact_id, content, json_pointer):
    """A REGISTRY-BOUND ref: artifact_id names the pinned artifact,
    json_pointer locates the value inside it, digest is recomputed HERE
    from the dereferenced value (and will be recomputed again, independently,
    by the receiver). No `inline` key at all -- an inline copy alongside a
    json_pointer is only ever a cache, and omitting it makes it structurally
    impossible for this artifact to lean on the legacy inline path."""
    found, value = _resolve_json_pointer(content, json_pointer)
    return {
        "artifact_id": artifact_id,
        "json_pointer": json_pointer,
        "digest": sha256_of(value) if found else None,
        "_pointer_resolved_at_build_time": found,
    }, found, value


def _inline_ref(object_id, data):
    return {"artifact_id": f"mb/ninfty-full-witness/inline/{object_id}", "digest": sha256_of(data),
            "object_id": object_id, "inline": data}


def build(fixture_stem, out_path):
    registry = _load("ninfty_native_registry_build", os.path.join(SEARCH, "ninfty-native-registry.py"))

    ids = {role: f"ep-genuine-{fixture_stem}-{role.replace('_', '-')}"
           for role in ("native_a", "native_b", "nf_a", "nf_b")}
    bundle = registry.resolve_bundle(sorted(ids.values()))
    if bundle is None:
        raise SystemExit("registry did not resolve to a generation -- refusing to build (fail-closed)")
    missing = [i for i in ids.values() if i not in bundle["artifacts"]]
    if missing:
        raise SystemExit(f"registry CURRENT generation {bundle['generation_id']!r} is missing {missing!r} "
                         "-- refusing to build (fail-closed)")
    entries = {role: bundle["artifacts"][aid] for role, aid in ids.items()}
    for role, entry in entries.items():
        if entry.get("role") != role or entry.get("status") != "ACTIVE":
            raise SystemExit(f"registry entry for {ids[role]!r} has role={entry.get('role')!r} "
                             f"status={entry.get('status')!r} -- refusing to build (fail-closed)")

    # --- lane A's own real certificate generator (node subprocess) --------
    base_out = subprocess.run(
        ["node", os.path.join(HERE, "gen_full_cert_base.mjs")],
        capture_output=True, encoding="utf-8", cwd=REPO,
    )
    if base_out.returncode != 0:
        raise SystemExit(f"gen_full_cert_base.mjs failed: {base_out.stderr}")
    base = json.loads(base_out.stdout)
    cert = base["certificate"]

    native_a_content = entries["native_a"]["content"]
    native_b_content = entries["native_b"]["content"]

    # --- rebuild the two W-6 entries as REGISTRY-BOUND witnesses ----------
    # searcher lane: lane A's native represents the branch divisor by IDEAL
    # GENERATORS per locus; the only array-valued node in it is
    # /branch_divisor_on_P1_ref/components.
    # checker lane: lane B's native carries an explicit
    # /branch_divisor_on_P1 list of {branch_value, multiplicity}.
    s_map, s_found, s_value = _bound_map_ref(ids["native_a"], native_a_content,
                                             "/branch_divisor_on_P1_ref/components")
    c_map, c_found, c_value = _bound_map_ref(ids["native_b"], native_b_content,
                                             "/branch_divisor_on_P1")

    cert["pushforward_compatibility_witness"] = [
        {
            "native_side": "searcher",
            "ramification_ref": _inline_ref("searcher-pushforward-ramification",
                                            native_a_content["ramification_divisor_on_C_ref"]),
            "branch_ref": _inline_ref("searcher-pushforward-branch",
                                      native_a_content["branch_divisor_on_P1_ref"]),
            "map_ref": s_map,
            "witness_ref": _inline_ref("searcher-pushforward-witness", {
                "status": "ABSENT",
                "reason": ("lane A represents branch components by ideals, not explicit points -- no "
                           "point-level pushforward witness exists on this lane"),
                "points": [],
            }),
        },
        {
            "native_side": "checker",
            "ramification_ref": _inline_ref("checker-pushforward-ramification",
                                            native_b_content["ramification_divisor_on_C"]),
            "branch_ref": _inline_ref("checker-pushforward-branch",
                                      native_b_content["branch_divisor_on_P1"]),
            "map_ref": c_map,
            "witness_ref": _inline_ref("checker-pushforward-witness", {
                "status": "PRESENT",
                "reason": "lane B's native carries explicit point-level ramification data",
                "points": native_b_content["ramification_divisor_on_C"],
            }),
        },
    ]

    raw = {
        "schema_id": RAW_W6_EVIDENCE_SCHEMA_ID,
        "certificate": cert,
        # kept for raw-shape compatibility ONLY -- the union never reads
        # these as native-content authority (Sol 便88 P88-o item 1); the
        # registry-pinned content is what both verifiers actually receive.
        "native_a": {"_note": "not authority -- see native_registry_refs", "artifact_id": ids["native_a"]},
        "native_b": {"_note": "not authority -- see native_registry_refs", "artifact_id": ids["native_b"]},
        "native_registry_refs": {
            "native_a": _registry_ref(ids["native_a"], entries["native_a"]),
            "native_b": _registry_ref(ids["native_b"], entries["native_b"]),
        },
        "nf_registry_refs": {
            "nf_a": _registry_ref(ids["nf_a"], entries["nf_a"]),
            "nf_b": _registry_ref(ids["nf_b"], entries["nf_b"]),
        },
        "_provenance": {
            "generated_by": "search/certs/build_full_witness_evidence.py",
            "generated_from_fixture": f"search/fixtures/ninfty/{fixture_stem}.json",
            "certificate_base": "search/certs/gen_full_cert_base.mjs (lane A's own generateCertificate)",
            "registry_generation_id": bundle["generation_id"],
            "registry_freeze_id": bundle.get("freeze_id"),
            "all_values_machine_generated": True,
            "does_not_reuse": "search/certs/full_witness_fixture_01.json (different, older lineage)",
        },
        "_note": (
            "FULL witness-bearing raw evidence for the three-column union "
            "(search/ninfty-evidence-union-full.py). W-6 map_refs are REGISTRY-BOUND "
            "(artifact_id + json_pointer, digest recomputed from the dereferenced value, NO inline "
            "fallback), so this artifact exercises the pinned-artifact dereference path rather than "
            "the legacy inline path the earlier smoke fixture used. This file asserts NO status: run "
            "`python search/ninfty-evidence-union-full.py <this file>` and read the report."
        ),
        "_build_time_pointer_resolution": {
            "searcher_map_ref_resolved": s_found,
            "checker_map_ref_resolved": c_found,
            "searcher_map_ref_value_is_branch_value_multiplicity_list": bool(
                isinstance(s_value, list) and s_value
                and all(isinstance(e, dict) and "branch_value" in e and "multiplicity" in e for e in s_value)),
            "checker_map_ref_value_is_branch_value_multiplicity_list": bool(
                isinstance(c_value, list) and c_value
                and all(isinstance(e, dict) and "branch_value" in e and "multiplicity" in e for e in c_value)),
        },
    }

    text = json.dumps(raw, indent=2, ensure_ascii=False, sort_keys=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"wrote {out_path}")
    print(json.dumps(raw["_build_time_pointer_resolution"], indent=2))
    print("registry generation:", bundle["generation_id"])
    return raw


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default="checker_pos_01")
    ap.add_argument("--out", default=os.path.join(HERE, "ep_ci_full_witness_evidence_20260801.json"))
    a = ap.parse_args()
    build(a.fixture, a.out)
