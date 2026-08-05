#!/usr/bin/env python3
"""Build immutable HS class-manifest draft and exact lane manifests."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import run_lane_job  # noqa: E402
import registered_preflight  # noqa: E402
import shard_manifest_gen  # noqa: E402
from binding_gate_lib import (PCGS_BASIS_CONTRACT, lane_record_checks,
                              pcgs_basis_fingerprint, pcgs_basis_material_checks,
                              workflow_template_digest)  # noqa: E402

DATE = "20260805"
WORKFLOW_TEMPLATE = "search/probe/hsp7_mainrun/hsp7_mainrun_workflow_v3.yml"
WORKFLOW_INSTALL_PATH = ".github/workflows/hsp7-mainrun-class-v3.yml"
PCGS_SOURCE_REL = registered_preflight.PCGS_SOURCE_REL
LANE_GZIP_CAP = 680 * 1024 * 1024


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle(paths: list[Path]) -> str:
    payload = "".join(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in sorted(paths)).encode()
    return hashlib.sha256(payload).hexdigest()


def digest_map_bundle(rows: dict[str, str]) -> str:
    payload = "".join(f"{rows[p]}  {p}\n" for p in sorted(rows)).encode()
    return hashlib.sha256(payload).hexdigest()


CLASS_COMPONENTS = [
    "docs/notes/hsp7_mainrun_prereg_v3.md",
    "docs/notes/hsp7_mainrun_prereg_v2_appendixC_v3.md",
    "gap.ps1",
    "search/probe/hsp7_mainrun/candidate_key_lib.g",
    "search/probe/hsp7_mainrun/cert_io.g",
    "search/probe/hsp7_mainrun/lane_wrapper_S.g",
    "search/probe/hsp7_mainrun/lane_wrapper_V.g",
    "search/probe/hsp7_mainrun/lane_wrapper_P.g",
    "search/probe/hsp7_mainrun/predicate_lib_laneS.g",
    "search/probe/hsp7_mainrun/predicate_lib_laneV_cf.g",
    "search/probe/hsp7_mainrun/predicate_lib_laneP.g",
    "search/probe/hsp7_mainrun/predicate_lib_laneP_conv.g",
    "search/probe/hsp7_mainrun/binding_gate_lib.py",
    "search/probe/hsp7_mainrun/binding_negative_matrix.py",
    "search/probe/hsp7_mainrun/run_lane_job.py",
    "search/probe/hsp7_mainrun/shard_manifest_gen.py",
    "search/probe/hsp7_mainrun/cert_to_join_manifest.py",
    "search/probe/hsp7_mainrun/join_checker.py",
    "search/probe/hsp7_mainrun/join_fixtures_gen.py",
    "search/probe/hsp7_mainrun/join_fixtures_run.py",
    "search/probe/hsp7_mainrun/capacity_probe.py",
    "search/probe/hsp7_mainrun/registered_preflight.py",
    "search/probe/hsp7_mainrun/build_class_manifest.py",
    "search/probe/hsp7_mainrun/bundle_static_audit.py",
    "search/probe/wac_v1/gap_output_prelude.g",
    "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g",
    "search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g",
    "search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g",
    "search/certs/hsp7_lane_cert_schema_v3.json",
    "search/certs/hsp7_join_fixtures_v2_20260805.json",
    "search/probe/hsp7_mainrun/driver_cf_laneV_calib.g",
    "search/probe/hsp7_mainrun/driver_conv_laneP_p5control_calib.g",
    "search/probe/hsp7_cond4_laneP_p5control/PQ_OUTPUT_P5.g",
    "search/probe/hsp7_cond4_laneP_p5control/PQ_OUTPUT_Q5.g",
    "search/certs/hsp7_cf_calib_20260805.json",
    "search/certs/hsp7_capacity_noncontact_v2_20260805.json",
    "search/certs/hsp7_binding_negative_matrix_v2_20260805.json",
    "search/certs/hsp7_registered_wrappers_preflight_20260805.json",
    "search/certs/hsp7_laneS_registered_preflight_20260805.json",
    "search/certs/hsp7_laneV_registered_preflight_20260805.json",
    "search/certs/hsp7_laneP_registered_preflight_20260805.json",
]

PCGS_REFRESH_COMPONENTS = [
    "search/certs/hsp7_registered_wrappers_preflight_pcgs_v3_20260805.json",
    "search/certs/hsp7_laneS_registered_preflight_pcgs_v3_20260805.json",
    "search/certs/hsp7_laneV_registered_preflight_pcgs_v3_20260805.json",
    "search/certs/hsp7_laneP_registered_preflight_pcgs_v3_20260805.json",
]


def load_pcgs_refresh() -> tuple[bool, dict[str, str | None], str | None, str]:
    """Validate the candidate-free refresh against *live current* sources.

    A shallow aggregate PASS is insufficient: every certificate, source map,
    named outcome, PCGS anchor, comparison and the P5 row is re-derived here.
    """
    paths = [ROOT / p for p in PCGS_REFRESH_COMPONENTS]
    empty = {lane: None for lane in ("S", "V", "P")}
    if not all(p.is_file() for p in paths):
        return False, empty, None, "current-source v3 refresh artifacts absent"
    try:
        receipt = json.loads(paths[0].read_text(encoding="utf-8"))
        certs = {lane: json.loads(paths[i].read_text(encoding="utf-8"))
                 for i, lane in enumerate(("S", "V", "P"), start=1)}
        source_sha = sha(ROOT / PCGS_SOURCE_REL)
        schema_sha = sha(registered_preflight.SCHEMA)
        fingerprints: dict[str, str | None] = {}
        commits: set[str] = set()
        expected_counts = {"S": 13, "V": 13, "P": 8}
        expected_axes = {"S": "pair", "V": "pair", "P": "f"}
        expected_totals = {"S": 705894, "V": 705894, "P": 117649}

        aggregate_rows = receipt.get("rows")
        if not isinstance(aggregate_rows, list) or len(aggregate_rows) != 4:
            raise ValueError("aggregate rows must be exactly S,V,P,P5")
        if any(not isinstance(row, dict) for row in aggregate_rows):
            raise ValueError("aggregate row is not an object")
        if [row.get("lane") for row in aggregate_rows] != ["S", "V", "P", "P5"]:
            raise ValueError("aggregate row lane/order mismatch")
        rows_by_lane = {row["lane"]: row for row in aggregate_rows}

        for lane, cert_path in zip(("S", "V", "P"), paths[1:]):
            cert = certs[lane]
            cfg = registered_preflight.LANES[lane]
            wrapper = ROOT / cfg["wrapper"]
            predicate = ROOT / cfg["predicate"]
            aux_paths = [ROOT / p for p in cfg["aux"]]
            all_paths = [wrapper, predicate, *aux_paths, registered_preflight.SCHEMA]
            expected_source_files = {
                p.relative_to(ROOT).as_posix(): sha(p) for p in all_paths}
            expected_bundle = bundle(all_paths)
            expected_aux = bundle(aux_paths)
            expected_source_bindings = {
                "source_bundle_sha256": expected_bundle,
                "wrapper_sha256": sha(wrapper),
                "predicate_sha256": sha(predicate),
                "aux_sha256": expected_aux,
                "schema_sha256": schema_sha,
            }
            run = cert.get("run") if isinstance(cert.get("run"), dict) else {}
            commit = run.get("commit_sha")
            if not isinstance(commit, str) or re.fullmatch(
                    r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", commit) is None:
                raise ValueError(f"lane {lane} commit provenance shape")
            commits.add(commit.lower())
            summary = cert.get("summary") if isinstance(cert.get("summary"), dict) else {}
            if (cert.get("schema") != "hsp7-lane-cert/v3"
                    or cert.get("lane") != lane
                    or cert.get("axis") != expected_axes[lane]
                    or cert.get("class_id") != registered_preflight.CLASS_ID
                    or cert.get("universe_total") != expected_totals[lane]
                    or cert.get("evaluated_range") != [-1, -1]
                    or run.get("run_id") != f"local-registered-{lane.lower()}"
                    or run.get("run_attempt") != "1"
                    or cert.get("source_bindings") != expected_source_bindings
                    or summary != {"evaluated_count": expected_counts[lane],
                                   "unknown_count": 0, "integrity_ok": True}
                    or cert.get("driver_done") is not True
                    or not isinstance(cert.get("records"), list)
                    or len(cert["records"]) != expected_counts[lane]
                    or not all(lane_record_checks(cert["records"], lane, [-1, -1]).values())):
                raise ValueError(f"lane {lane} current-source cert/header/record gate")
            checks = pcgs_basis_material_checks(
                cert.get("pcgs_basis_material"), lane, PCGS_SOURCE_REL, source_sha)
            if not all(checks.values()):
                failed = ",".join(k for k, ok in checks.items() if not ok)
                raise ValueError(f"lane {lane} material gate: {failed}")
            fp = pcgs_basis_fingerprint(cert["pcgs_basis_material"])
            if cert.get("pcgs_basis_fingerprint") != fp:
                raise ValueError(f"lane {lane} self fingerprint")
            fingerprints[lane] = fp

            row = rows_by_lane[lane]
            if (row.get("lane") != lane or row.get("pass") is not True
                    or row.get("exit_code") != 0 or row.get("error") is not None
                    or row.get("basis_probe_exit_code") != 0
                    or row.get("pcgs_basis_fingerprint") != fp
                    or row.get("cert_path") != cfg["cert"]
                    or row.get("cert_sha256") != sha(cert_path)
                    or row.get("source_bundle_sha256") != expected_bundle
                    or row.get("source_files") != expected_source_files
                    or re.fullmatch(r"[0-9a-f]{64}", str(row.get("log_sha256"))) is None
                    or re.fullmatch(r"[0-9a-f]{64}", str(
                        row.get("basis_probe_log_sha256"))) is None):
                raise ValueError(f"aggregate lane {lane} live row gate")

        if len(commits) != 1:
            raise ValueError("registered lane cert commits disagree")
        source_commit = next(iter(commits))
        expected_commit_files = {
            rel: sha(ROOT / rel) for rel in registered_preflight.provenance_paths()}
        if (receipt.get("source_commit_sha") != source_commit
                or receipt.get("source_commit_files") != expected_commit_files):
            raise ValueError("aggregate source-commit/live-file map mismatch")
        for rel in expected_commit_files:
            proc = subprocess.run(["git", "show", f"{source_commit}:{rel}"], cwd=ROOT,
                                  capture_output=True, check=False)
            if proc.returncode != 0 or proc.stdout != (ROOT / rel).read_bytes():
                raise ValueError(f"aggregate source commit does not contain live bytes: {rel}")
        expected_orchestrator = {
            "path": registered_preflight.ORCHESTRATOR_REL,
            "sha256": sha(ROOT / registered_preflight.ORCHESTRATOR_REL),
            "validator_path": registered_preflight.VALIDATOR_REL,
            "validator_sha256": sha(ROOT / registered_preflight.VALIDATOR_REL),
            "gap_wrapper_path": registered_preflight.GAP_WRAPPER_REL,
            "gap_wrapper_sha256": sha(ROOT / registered_preflight.GAP_WRAPPER_REL),
        }
        if receipt.get("orchestrator") != expected_orchestrator:
            raise ValueError("aggregate orchestrator/validator/gap-wrapper live binding mismatch")
        core_s = certs["S"]["pcgs_basis_material"]
        core_v = dict(certs["V"]["pcgs_basis_material"])
        core_v["s_to_v_bridge_coordinates"] = []
        if core_s != certs["P"]["pcgs_basis_material"] or core_s != core_v:
            raise ValueError("S/P/V ordered basis core mismatch")
        core_fp = pcgs_basis_fingerprint(core_s)

        expected_s = registered_preflight.expected_fixture_verdicts()
        got_s = {r["fixture_id"]: r["verdict"] for r in certs["S"]["records"]}
        got_v = {r["fixture_id"]: r["N"]["verdict"] for r in certs["V"]["records"]}
        expected_p = {"h4t0": True,
                      **{f"h4t{t}": False for t in range(1, 7)}, "h3": False}
        got_p = {r["fixture_id"]: r["pentagon_verdict"]
                 for r in certs["P"]["records"]}
        if got_s != expected_s or got_v != expected_s or got_p != expected_p:
            raise ValueError("registered named outcome mismatch")
        if (not all(r.get("N_N0_agree") is True
                    and r.get("CF_baseline_agree") is True
                    for r in certs["V"]["records"])
                or not all(r.get("CONV_native_element_agree") is True
                           and r.get("CONV_native_verdict_agree") is True
                           for r in certs["P"]["records"])):
            raise ValueError("registered two-path agreement mismatch")

        p5_paths = [ROOT / p for p in registered_preflight.P5_SOURCES]
        p5_driver = ROOT / registered_preflight.P5_SOURCES[0]
        p5_row = rows_by_lane["P5"]
        p5_source_files = {p.relative_to(ROOT).as_posix(): sha(p) for p in p5_paths}
        if (p5_row.get("pass") is not True or p5_row.get("exit_code") != 0
                or p5_row.get("error") is not None
                or p5_row.get("driver_path") != p5_driver.relative_to(ROOT).as_posix()
                or p5_row.get("driver_sha256") != sha(p5_driver)
                or p5_row.get("source_bundle_sha256") != bundle(p5_paths)
                or p5_row.get("source_files") != p5_source_files
                or re.fullmatch(r"[0-9a-f]{64}", str(p5_row.get("log_sha256"))) is None):
            raise ValueError("P5 current-source aggregate row gate")

        expected_comparisons = {
            "laneP5_CONV_native_5_equal", "laneP_8_matches_registered",
            "laneS_13_matches_registered", "laneS_laneV_13_equal",
            "laneV_13_matches_registered", "laneV_N_N0_all_equal",
            "ordered_pcgs_core_S_P_equal", "ordered_pcgs_core_S_V_equal",
        }
        comparisons = receipt.get("comparisons")
        if (receipt.get("schema") != "hsp7-registered-wrapper-preflight/v3"
                or receipt.get("class_id") != registered_preflight.CLASS_ID
                or receipt.get("overall_pass") is not True
                or receipt.get("candidate_universe_contact") != 0
                or receipt.get("registered_fixture_plan") != {
                    "S": 13, "V": 13, "P_production": 8, "P5_two_path": 5}
                or receipt.get("actual_evaluated") != {"S": 13, "V": 13, "P": 8}
                or receipt.get("pcgs_basis_contract") != PCGS_BASIS_CONTRACT
                or receipt.get("pcgs_basis_fingerprints") != fingerprints
                or receipt.get("pcgs_core_fingerprint") != core_fp
                or not isinstance(comparisons, dict)
                or set(comparisons) != expected_comparisons
                or not all(value is True for value in comparisons.values())):
            raise ValueError("aggregate current-source runtime-PCGS receipt gate")
        return True, fingerprints, core_fp, "current-source v3 refresh receipt PASS"
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return False, empty, None, str(exc)


def main() -> int:
    pcgs_refresh_ok, pcgs_fingerprints, pcgs_core_fingerprint, pcgs_refresh_detail = load_pcgs_refresh()
    pcgs_refresh_source_commit = None
    if pcgs_refresh_ok:
        pcgs_refresh_source_commit = json.loads(
            (ROOT / PCGS_REFRESH_COMPONENTS[0]).read_text(encoding="utf-8"))["source_commit_sha"]
    component_rels = [*CLASS_COMPONENTS,
                      *(PCGS_REFRESH_COMPONENTS if pcgs_refresh_ok else [])]
    paths = [ROOT / p for p in component_rels]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("missing class component(s): " + ", ".join(missing))
    component_digests = {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}
    workflow_path = ROOT / WORKFLOW_TEMPLATE
    if not workflow_path.is_file():
        raise SystemExit(f"missing workflow template: {workflow_path}")
    workflow_normalized_sha = workflow_template_digest(workflow_path.read_bytes())
    virtual_workflow_key = WORKFLOW_TEMPLATE + "#normalized-freeze-sentinels"
    component_bundle = digest_map_bundle(
        {**component_digests, virtual_workflow_key: workflow_normalized_sha})
    class_id = f"HS-NW7-CLASS-v3-draft-{component_bundle[:16]}"
    pcgs_artifact = ROOT / "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"
    pcgs_artifact_rel = pcgs_artifact.relative_to(ROOT).as_posix()
    pcgs_artifact_sha = sha(pcgs_artifact)
    pcgs_id = "sha256:" + pcgs_artifact_sha
    lane_rows = {}
    for lane in ("S", "V", "P"):
        lane_paths = [ROOT / p for p in run_lane_job.LANE_SOURCES[lane]]
        source_digest = bundle(lane_paths)
        manifest = shard_manifest_gen.build_manifest(
            lane, shard_manifest_gen.FROZEN_SHARD_SIZES_V3[lane],
            shard_manifest_gen.FROZEN_TIMEOUT_MIN_V3, source_digest,
            20, 256, class_id, source_digest, pcgs_id,
            PCGS_BASIS_CONTRACT, pcgs_fingerprints[lane],
            pcgs_artifact_rel, pcgs_artifact_sha,
        )
        manifest["manifest_sha256"] = hashlib.sha256(shard_manifest_gen.canonical_bytes(manifest)).hexdigest()
        out = ROOT / f"search/certs/hsp7_shard_manifest_lane{lane}_v3_{DATE}.json"
        out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        lane_rows[lane] = {
            "source_bundle_sha256": source_digest,
            "pcgs_basis_fingerprint": pcgs_fingerprints[lane],
            "compressed_cap_bytes": LANE_GZIP_CAP,
            "source_files": {p.relative_to(ROOT).as_posix(): sha(p) for p in lane_paths},
            "shard_manifest": out.relative_to(ROOT).as_posix(),
            "shard_manifest_file_sha256": sha(out),
            "partition": {"total": manifest["total_candidates"], "target_size": manifest["shard_size_target"],
                          "n_shards": manifest["n_shards"], "timeout_min": manifest["timeout_min"],
                          "max_parallel": manifest["max_parallel"]},
        }
    join_receipt = ROOT / "search/certs/hsp7_join_fixtures_v2_20260805.json"
    capacity_receipt = ROOT / "search/certs/hsp7_capacity_noncontact_v2_20260805.json"
    binding_receipt = ROOT / "search/certs/hsp7_binding_negative_matrix_v2_20260805.json"
    registered_receipt = ROOT / "search/certs/hsp7_registered_wrappers_preflight_20260805.json"
    registered = json.loads(registered_receipt.read_text(encoding="utf-8"))
    obj = {
        "schema": "hsp7-class-manifest-draft/v1",
        "class_id": class_id,
        "class_component_bundle_sha256": component_bundle,
        "status": ("READY_FOR_SOL_FREEZE_REVIEW" if pcgs_refresh_ok else
                   "BLOCKED_RUNTIME_ORDERED_PCGS_RECEIPT_REFRESH"),
        "authorization": {"main_run": False, "calibration_shard": False, "workflow_dispatch": False,
                          "claim_grade_promotion": False},
        "components": component_digests,
        "workflow_installation": {
            "source_template_path": WORKFLOW_TEMPLATE,
            "installed_path": WORKFLOW_INSTALL_PATH,
            "normalized_template_sha256": workflow_normalized_sha,
            "normalization_contract": "canonical-LF; replace only FROZEN_CLASS_MANIFEST_PATH and FROZEN_CLASS_MANIFEST_SHA256 values with UNSET_REQUIRES_FREEZE",
            "virtual_component_key": virtual_workflow_key,
        },
        "exact_universe": {
            "pcgs_id": pcgs_id,
            "pcgs_id_kind": "legacy_source_artifact_anchor_not_runtime_basis_identity",
            "pcgs_basis_contract": PCGS_BASIS_CONTRACT,
            "pcgs_basis_fingerprints": pcgs_fingerprints,
            "pcgs_core_fingerprint": pcgs_core_fingerprint,
            "pcgs_source_artifact_path": pcgs_artifact_rel,
            "pcgs_source_artifact_sha256": pcgs_artifact_sha,
            "pcgs_basis_fingerprint_status": ("BOUND_TO_REGISTERED_RUNTIME_MATERIAL"
                                               if pcgs_refresh_ok else
                                               "BLOCKER_PENDING_REGISTERED_RUNTIME_MATERIAL_REFRESH"),
            "radix": 7, "exponent_width": 6,
            "m_values": [0, 1, 2, 4, 5, 6], "endian": "big",
            "lane_S_pair_indices": [0, 705893], "lane_V_pair_indices": [0, 705893],
            "lane_P_f_indices": [0, 117648],
            "lane_P_expansion": "pair_index=m_index*117649+f_index for m_index=0..5",
        },
        "lanes": lane_rows,
        "stop_unknown": {
            "hard_shard_timeout_min": 60,
            "runtime_pcgs_preflight_timeout_min": 15,
            "fatal_error_is_unknown": False,
            "unknown_is_explicit_record_only": True,
            "partial_or_missing_shard": "STOP",
            "automatic_retry": False,
        },
        "join": {
            "checker": "search/probe/hsp7_mainrun/join_checker.py",
            "independent_rederivation": ["flat-index-to-semantic-tuple", "P-f-key-to-all-pair-keys"],
            "fixture_receipt": join_receipt.relative_to(ROOT).as_posix(),
            "fixture_receipt_sha256": sha(join_receipt),
            "fixture_overall_pass": json.loads(join_receipt.read_text())["overall_pass"],
        },
        "exposure_negative_result": {
            "partial_distribution_updates_forbidden": True,
            "all_pass_fail_unknown_records_retained": True,
            "stop_and_superseded_retry_receipts_retained": True,
            "automatic_claim_promotion": False,
        },
        "capacity": {
            "receipt": capacity_receipt.relative_to(ROOT).as_posix(),
            "receipt_sha256": sha(capacity_receipt),
            "candidate_universe_contact": 0,
            "per_shard_uncompressed_cap_bytes": 20 * 1024 * 1024,
            "per_lane_compressed_cap_bytes": {lane: LANE_GZIP_CAP for lane in ("S", "V", "P")},
            "per_lane_cap_sum_bytes": 3 * LANE_GZIP_CAP,
            "whole_class_compressed_cap_bytes": 2 * 1024 * 1024 * 1024,
            "retention_days": 30,
        },
        "negative_binding_matrix": {
            "receipt": binding_receipt.relative_to(ROOT).as_posix(),
            "receipt_sha256": sha(binding_receipt),
            "fixture_count": json.loads(binding_receipt.read_text())["fixture_count"],
            "overall_pass": json.loads(binding_receipt.read_text())["overall_pass"],
            "candidate_universe_contact": 0,
        },
        "preflight": {
            "prior_cf_conv_registered_18_receipt": "search/certs/hsp7_cf_calib_20260805.json",
            "prior_cf_conv_registered_18_receipt_sha256": sha(ROOT / "search/certs/hsp7_cf_calib_20260805.json"),
            "registered_wrapper_calibration_v1": {
                "receipt": registered_receipt.relative_to(ROOT).as_posix(),
                "receipt_sha256": sha(registered_receipt),
                "overall_pass": registered.get("overall_pass") is True,
                "actual_evaluated": registered.get("actual_evaluated"),
                "historical_only": True,
                "class_calibration_closed": False,
            },
            "runtime_pcgs_refresh": {
                "expected_receipt": PCGS_REFRESH_COMPONENTS[0],
                "artifacts_present": all((ROOT / p).is_file() for p in PCGS_REFRESH_COMPONENTS),
                "overall_pass": pcgs_refresh_ok,
                "class_calibration_closed": pcgs_refresh_ok,
                "source_commit_sha": pcgs_refresh_source_commit,
                "detail": pcgs_refresh_detail,
            },
            "blockers": ([] if pcgs_refresh_ok else [
                "candidate-free registered rerun with ordered runtime PCGS material/fingerprint is absent or invalid",
            ]),
        },
        "re_gate_on_change": ["predicate", "wrapper", "conversion", "schema", "checker", "source-map",
                              "pcgs-artifact", "semantic-key", "universe/range", "sharding", "STOP/UNKNOWN",
                              "exposure/retention/cap", "new output type"],
        "note": ("The v1 registered receipt is historical evidence only after wrapper/schema v3 changes. "
                 "Class calibration closes only through the fully rebound candidate-free v3 refresh. "
                 "Main/production certificates are intentionally not a class-freeze prerequisite; "
                 "no candidate/main run was made."),
    }
    out = ROOT / f"search/certs/hsp7_class_manifest_v3_draft_{DATE}.json"
    out.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"class_id": class_id, "manifest": out.relative_to(ROOT).as_posix(),
                      "sha256": sha(out), "status": obj["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
