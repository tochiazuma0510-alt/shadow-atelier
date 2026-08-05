#!/usr/bin/env python3
"""Read-only digest/partition/static audit for the blocked HS class draft."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from binding_gate_lib import (PCGS_BASIS_CONTRACT, class_lane_capacity_checks,
                              manifest_binding_checks,
                              pcgs_basis_fingerprint,
                              pcgs_basis_material_checks,
                              workflow_template_digest)  # noqa: E402
from build_class_manifest import load_pcgs_refresh  # noqa: E402

CLASS = ROOT / "search/certs/hsp7_class_manifest_v3_draft_20260805.json"
OUT = ROOT / "search/certs/hsp7_bundle_static_audit_v2_20260805.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle(paths: list[Path]) -> str:
    data = "".join(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in sorted(paths)).encode()
    return hashlib.sha256(data).hexdigest()


def digest_map_bundle(rows: dict[str, str]) -> str:
    data = "".join(f"{rows[p]}  {p}\n" for p in sorted(rows)).encode()
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    c = json.loads(CLASS.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    checks["draft_not_authorized"] = (c["status"].startswith("BLOCKED")
                                       or c["status"] == "READY_FOR_SOL_FREEZE_REVIEW") \
        and not any(c["authorization"].values())
    checks["component_hashes"] = all(sha(ROOT / p) == h for p, h in c["components"].items())
    workflow = c["workflow_installation"]
    workflow_source = ROOT / workflow["source_template_path"]
    normalized_sha = workflow_template_digest(workflow_source.read_bytes())
    virtual_key = workflow["virtual_component_key"]
    component_bundle = digest_map_bundle({**c["components"], virtual_key: normalized_sha})
    checks["component_bundle"] = component_bundle == c["class_component_bundle_sha256"]
    checks["class_id_derived"] = c["class_id"] == f"HS-NW7-CLASS-v3-draft-{component_bundle[:16]}"
    checks["workflow_normalized_template_bound"] = (
        workflow.get("installed_path") == ".github/workflows/hsp7-mainrun-class-v3.yml"
        and workflow.get("normalized_template_sha256") == normalized_sha
        and virtual_key == workflow["source_template_path"] + "#normalized-freeze-sentinels"
        and workflow["source_template_path"] not in c["components"])
    pcgs = c["exact_universe"]
    pcgs_refresh_pass = c["preflight"]["runtime_pcgs_refresh"]["overall_pass"] is True
    if pcgs_refresh_pass:
        checks["pcgs_runtime_fingerprint_bound"] = (
            c["status"] == "READY_FOR_SOL_FREEZE_REVIEW"
            and pcgs.get("pcgs_basis_contract") == PCGS_BASIS_CONTRACT
            and all(isinstance(pcgs.get("pcgs_basis_fingerprints", {}).get(lane), str)
                    for lane in ("S", "V", "P"))
            and isinstance(pcgs.get("pcgs_core_fingerprint"), str)
            and pcgs.get("pcgs_basis_fingerprint_status") ==
            "BOUND_TO_REGISTERED_RUNTIME_MATERIAL"
            and pcgs.get("pcgs_source_artifact_path") ==
            "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"
            and pcgs.get("pcgs_source_artifact_sha256") ==
            sha(ROOT / pcgs["pcgs_source_artifact_path"])
            and c["preflight"]["blockers"] == [])
    else:
        checks["pcgs_runtime_fingerprint_honestly_blocked"] = (
            c["status"] == "BLOCKED_RUNTIME_ORDERED_PCGS_RECEIPT_REFRESH"
            and pcgs.get("pcgs_id_kind") ==
            "legacy_source_artifact_anchor_not_runtime_basis_identity"
            and pcgs.get("pcgs_basis_contract") == PCGS_BASIS_CONTRACT
            and pcgs.get("pcgs_basis_fingerprints") == {"S": None, "V": None, "P": None}
            and pcgs.get("pcgs_core_fingerprint") is None
            and pcgs.get("pcgs_basis_fingerprint_status") ==
            "BLOCKER_PENDING_REGISTERED_RUNTIME_MATERIAL_REFRESH"
            and pcgs.get("pcgs_source_artifact_sha256") ==
            sha(ROOT / pcgs["pcgs_source_artifact_path"])
            and len(c["preflight"]["blockers"]) == 1)
    checks["class_lane_capacity_composition"] = all(
        class_lane_capacity_checks(c.get("capacity")).values())
    for lane, row in c["lanes"].items():
        source_paths = [ROOT / p for p in row["source_files"]]
        checks[f"lane_{lane}_source_files"] = all(sha(ROOT / p) == h for p, h in row["source_files"].items())
        checks[f"lane_{lane}_source_bundle"] = bundle(source_paths) == row["source_bundle_sha256"]
        checks[f"lane_{lane}_compressed_cap"] = (
            row.get("compressed_cap_bytes") ==
            c["capacity"]["per_lane_compressed_cap_bytes"].get(lane))
        mp = ROOT / row["shard_manifest"]
        m = json.loads(mp.read_text())
        checks[f"lane_{lane}_manifest_file"] = sha(mp) == row["shard_manifest_file_sha256"]
        binding = manifest_binding_checks(
            class_obj=c, manifest_obj=m, manifest_bytes=mp.read_bytes(),
            actual_manifest_path=row["shard_manifest"], lane=lane,
            live_source_bundle_sha256=bundle(source_paths))
        checks[f"lane_{lane}_all_manifest_bindings"] = all(binding.values())
        nxt = 0
        for i, s in enumerate(sorted(m["shards"], key=lambda x: x["lo"])):
            if s["name"] != f"shard_{i:05d}" or s["lo"] != nxt or s["hi"] < s["lo"]:
                nxt = -1
                break
            nxt = s["hi"] + 1
        checks[f"lane_{lane}_exact_cover"] = nxt == m["total_candidates"] and len(m["shards"]) == m["n_shards"]
    checks["join_mutants_pass"] = json.loads((ROOT / c["join"]["fixture_receipt"]).read_text())["overall_pass"] is True
    cap = json.loads((ROOT / c["capacity"]["receipt"]).read_text())
    checks["capacity_noncandidate_shape"] = (
        cap.get("schema") == "hsp7-capacity-noncontact/v2"
        and cap["candidate_universe_contact"] == 0
        and cap["production_record_shape_used"] is True
        and cap["retention_policy"]["per_lane_compressed_cap_bytes"] ==
        c["capacity"]["per_lane_compressed_cap_bytes"]
        and cap["retention_policy"]["per_lane_cap_sum_bytes"] ==
        c["capacity"]["per_lane_cap_sum_bytes"]
        and cap["retention_policy"]["whole_class_compressed_cap_bytes"] ==
        c["capacity"]["whole_class_compressed_cap_bytes"])
    binding_receipt_path = ROOT / c["negative_binding_matrix"]["receipt"]
    binding_receipt = json.loads(binding_receipt_path.read_text())
    checks["binding_matrix_digest"] = sha(binding_receipt_path) == c["negative_binding_matrix"]["receipt_sha256"]
    checks["binding_matrix_pure_pass"] = (
        binding_receipt["overall_pass"] is True
        and binding_receipt["candidate_universe_contact"] == 0
        and binding_receipt["gap_invocations"] == 0
        and binding_receipt["fixture_count"] == c["negative_binding_matrix"]["fixture_count"])
    calibration = c["preflight"]["registered_wrapper_calibration_v1"]
    registered_path = ROOT / calibration["receipt"]
    registered = json.loads(registered_path.read_text())
    registered_rows_ok = all(
        row.get("pass") is True
        and (ROOT / row["cert_path"]).is_file()
        and sha(ROOT / row["cert_path"]) == row["cert_sha256"]
        for row in registered["rows"] if row.get("lane") in ("S", "V", "P"))
    checks["registered_preflight_v1_historical_bound"] = (
        sha(registered_path) == calibration["receipt_sha256"]
        and registered["overall_pass"] is True
        and registered["candidate_universe_contact"] == 0
        and registered["actual_evaluated"] == {"S": 13, "V": 13, "P": 8}
        and registered_rows_ok
        and calibration["overall_pass"] is True
        and calibration["historical_only"] is True
        and calibration["class_calibration_closed"] is False)
    refresh_loader_ok, refresh_loader_fps, refresh_loader_core, _ = load_pcgs_refresh()
    checks["pcgs_refresh_full_live_revalidation"] = (
        refresh_loader_ok == pcgs_refresh_pass
        and c["preflight"]["runtime_pcgs_refresh"]["class_calibration_closed"]
        is pcgs_refresh_pass)
    if pcgs_refresh_pass:
        refresh_path = ROOT / c["preflight"]["runtime_pcgs_refresh"]["expected_receipt"]
        refresh = json.loads(refresh_path.read_text(encoding="utf-8"))
        refresh_certs = {lane: json.loads((ROOT / next(
            r["cert_path"] for r in refresh["rows"] if r.get("lane") == lane)).read_text(encoding="utf-8"))
                         for lane in ("S", "V", "P")}
        refresh_checks = []
        for lane, cert in refresh_certs.items():
            material_checks = pcgs_basis_material_checks(
                cert.get("pcgs_basis_material"), lane,
                pcgs["pcgs_source_artifact_path"], pcgs["pcgs_source_artifact_sha256"])
            fp = pcgs_basis_fingerprint(cert["pcgs_basis_material"])
            refresh_checks.append(all(material_checks.values())
                                  and cert.get("pcgs_basis_fingerprint") == fp
                                   and refresh["pcgs_basis_fingerprints"].get(lane) == fp
                                   and c["lanes"][lane]["pcgs_basis_fingerprint"] == fp
                                   and refresh_loader_fps.get(lane) == fp)
        checks["pcgs_refresh_artifacts_bound"] = (
            all(refresh_checks) and refresh_loader_core == pcgs.get("pcgs_core_fingerprint")
            and c["preflight"]["runtime_pcgs_refresh"].get("source_commit_sha") ==
            refresh.get("source_commit_sha"))
    runner_text = (ROOT / "search/probe/hsp7_mainrun/run_lane_job.py").read_text(encoding="utf-8")
    checks["runner_uses_shared_fail_closed_bindings"] = all(
        token in runner_text for token in (
            "manifest_binding_checks(", "cert_binding_checks(",
            'auth.get("main_run") is not True',
            'auth.get("workflow_dispatch") is not True',
            "class_lane_capacity_checks(", 'RUN_MODE := "BASIS_ONLY"',
            "PCGS_BASIS_FINGERPRINT_MISMATCH"))
    workflow_text = (ROOT / "search/probe/hsp7_mainrun/hsp7_mainrun_workflow_v3.yml").read_text(encoding="utf-8")
    checks["workflow_uses_shared_fail_closed_bindings"] = all(
        token in workflow_text for token in (
            "FROZEN_CLASS_MANIFEST_PATH", "FROZEN_CLASS_MANIFEST_SHA256",
            "class_lock_checks(", "manifest_binding_checks(", "receipt_cert_checks(",
            "receipt_binding_checks(", "cert_binding_checks(",
            "collection_capacity_checks(", "workflow_template_digest(",
            '["per_lane_compressed_cap_bytes"][lane]'))
    py_files = list((ROOT / "search/probe/hsp7_mainrun").glob("*.py"))
    for p in py_files:
        ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
    checks["python_ast_parse"] = True
    result = {"schema": "hsp7-bundle-static-audit/v2", "class_id": c["class_id"],
              "checks": checks, "overall_pass": all(checks.values()),
              "candidate_evaluations": 0}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
