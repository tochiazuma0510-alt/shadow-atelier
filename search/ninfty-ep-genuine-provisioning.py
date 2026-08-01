#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-ep-genuine-provisioning.py

EP registry re-activation, production provisioning driver (2026-08-01,
司令塔指示 "EP 再発効の機械的最終列" item 1-2, 裁定 (a)-強化版).

For each of the 3 genuine fixtures (search/fixtures/ninfty/checker_pos_0{1,2,3}.json
-- the only fixtures with NF status PRESENT and lane A/B nf_digest already
confirmed identical, per search/certs/ep_nf_20260801.json), this script:

  1. computes native_a content (search/ninfty-native-a-cli.mjs, i.e.
     buildSearcherNative -- the FROZEN, sol75-approved lane A native schema:
     ramification_divisor_on_C_ref / branch_divisor_on_P1_ref);
  2. computes native_b content (search/ninfty-native-b-cli.py, i.e.
     construct_native_from_scratch -- the FROZEN lane B native schema:
     ramification_divisor_on_C / branch_divisor_on_P1 / ...);
  3. computes nf_a content (search/ninfty-nf-lanea-cli.mjs, computeNormalFormLaneA);
  4. computes nf_b content (search/ninfty-nf-laneb.py, compute_normal_form_lane_b);
  5. asserts nf_a.status == nf_b.status == "PRESENT" and
     nf_a.nf_digest == nf_b.nf_digest (the genuine-fixture invariant this
     whole batch is conditioned on -- refuses to provision a fixture that
     does not satisfy it).

All 4*3 = 12 artifacts are bound into ONE generation under a SINGLE new
freeze_id via search/ninfty-native-registry-provisioning.py's
commit_generation -- 司令塔裁定 (2026-08-01, EP再発効 items 1-2, "(a) の
強化版"): NF is NOT substituted into the native_a/native_b role (those keep
their FROZEN, sol75/R1/R2-consumed schema, untouched) -- NF is stored
alongside as two NEW roles (nf_a/nf_b) in the SAME generation/freeze_id,
per the F92-6.2 addendum's already-approved generalization ("同一 freeze の
任意個 artifacts").

This file does NOT run automatically as an import; provisioning only
happens via main() below, gated the same way
ninfty-native-registry-provisioning.py's own CLI is (NINFTY_EP_ALLOW_
PRODUCTION_WRITE=1 required, --production flag).

runtime: python3 (subprocess + importlib.util only, stdlib).
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
ROOT = os.path.dirname(HERE)
FIXTURES_DIR = os.path.join(HERE, "fixtures", "ninfty")
GENUINE_FIXTURES = ["checker_pos_01.json", "checker_pos_02.json", "checker_pos_03.json"]

NODE = "node"
PYTHON = sys.executable or "python"

NATIVE_A_CLI = os.path.join(HERE, "ninfty-native-a-cli.mjs")
NATIVE_B_CLI = os.path.join(HERE, "ninfty-native-b-cli.py")
NF_A_CLI = os.path.join(HERE, "ninfty-nf-lanea-cli.mjs")
NF_B_CLI = os.path.join(HERE, "ninfty-nf-laneb.py")


def _load_provisioning():
    path = os.path.join(HERE, "ninfty-native-registry-provisioning.py")
    spec = importlib.util.spec_from_file_location("ninfty_native_registry_provisioning_for_genuine", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_json(cmd, cwd=ROOT):
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {cmd!r}\nstdout={proc.stdout!r}\nstderr={proc.stderr!r}")
    stdout = proc.stdout.strip()
    if not stdout:
        raise RuntimeError(f"command produced no stdout: {cmd!r}\nstderr={proc.stderr!r}")
    return json.loads(stdout)


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def compute_bundle_for_fixture(fixture_path):
    native_a = _run_json([NODE, NATIVE_A_CLI, fixture_path])
    native_b = _run_json([PYTHON, NATIVE_B_CLI, fixture_path])
    nf_a = _run_json([NODE, NF_A_CLI, fixture_path])
    nf_b = _run_json([PYTHON, NF_B_CLI, fixture_path])

    if nf_a.get("status") != "PRESENT" or nf_b.get("status") != "PRESENT":
        raise RuntimeError(f"{fixture_path}: NF mint gate did not reach PRESENT on both lanes "
                            f"(lane_a={nf_a.get('status')!r}, lane_b={nf_b.get('status')!r}) -- refusing to provision")
    if nf_a.get("nf_digest") != nf_b.get("nf_digest"):
        raise RuntimeError(f"{fixture_path}: nf_digest mismatch between lane A ({nf_a.get('nf_digest')!r}) "
                            f"and lane B ({nf_b.get('nf_digest')!r}) -- refusing to provision")
    if native_b.get("status") != "ok":
        raise RuntimeError(f"{fixture_path}: native_b (checker_native) construction did not reach status='ok' "
                            f"(got {native_b.get('status')!r}) -- refusing to provision")

    return {"native_a": native_a, "native_b": native_b, "nf_a": nf_a, "nf_b": nf_b}


def build_artifacts(freeze_id):
    """Returns (artifacts_list_for_commit_generation, per_fixture_summary)."""
    artifacts = []
    summary = {}
    for fname in GENUINE_FIXTURES:
        fpath = os.path.join(FIXTURES_DIR, fname)
        stem = fname[:-len(".json")]
        bundle = compute_bundle_for_fixture(fpath)
        fixture_summary = {}
        for role in ("native_a", "native_b", "nf_a", "nf_b"):
            content = bundle[role]
            artifact_id = f"ep-genuine-{stem}-{role.replace('_', '-')}"
            artifacts.append({
                "artifact_id": artifact_id,
                "role": role,
                "version_id": "v1",
                "content": content,
                "status": "ACTIVE",
            })
            fixture_summary[role] = {
                "artifact_id": artifact_id,
                "content_digest": _digest(content),
            }
        summary[stem] = fixture_summary
    return artifacts, summary


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--production", action="store_true",
                     help="write into PRODUCTION_REGISTRY_DIR (requires NINFTY_EP_ALLOW_PRODUCTION_WRITE=1)")
    ap.add_argument("--registry-dir", default=None, help="explicit non-production store (mutually exclusive with --production)")
    ap.add_argument("--freeze-id", required=True)
    ap.add_argument("--generation-id", default=None)
    ap.add_argument("--no-publish", action="store_true")
    ap.add_argument("--summary-out", default=None, help="write the per-fixture artifact_id/digest summary JSON here")
    args = ap.parse_args(argv)

    if args.production and args.registry_dir:
        print("error: --production and --registry-dir are mutually exclusive", file=sys.stderr)
        return 2
    if not args.production and not args.registry_dir:
        print("error: one of --production or --registry-dir is required", file=sys.stderr)
        return 2

    prov = _load_provisioning()
    target_dir = prov.PRODUCTION_REGISTRY_DIR if args.production else args.registry_dir

    artifacts, summary = build_artifacts(args.freeze_id)
    result = prov.commit_generation(
        artifacts, args.freeze_id, registry_dir=target_dir,
        generation_id=args.generation_id, publish=not args.no_publish,
    )
    out = {"commit_result": result, "fixture_summary": summary}
    print(canonical_serialize(out))
    if args.summary_out:
        with open(args.summary_out, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False, sort_keys=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
