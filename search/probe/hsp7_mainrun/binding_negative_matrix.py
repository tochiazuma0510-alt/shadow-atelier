#!/usr/bin/env python3
"""Pure synthetic negative matrix for frozen HS execution bindings.

This test imports no GAP code and constructs no group or candidate.  Its data
are deliberately synthetic strings and one-record dummy certificates.  Every
mutant must be rejected by a named fail-closed binding check.
"""

from __future__ import annotations

import copy
import gzip
import json
from pathlib import Path
from typing import Any, Callable

from binding_gate_lib import (PCGS_BASIS_CONTRACT, class_lane_capacity_checks,
                              class_lock_checks, collection_capacity_checks,
                              cert_binding_checks, manifest_binding_checks,
                              lane_record_checks, manifest_self_digest, pcgs_basis_fingerprint,
                              pcgs_basis_material_checks, receipt_binding_checks,
                              receipt_cert_checks, sha256_bytes)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "search/certs/hsp7_binding_negative_matrix_v2_20260805.json"
MANIFEST_PATH = "search/certs/synthetic_hsp7_laneS_manifest.json"
CLASS_PATH = "search/certs/synthetic_hsp7_class_manifest.json"
SOURCE_SHA = "1" * 64
WRAPPER_SHA = "2" * 64
PREDICATE_SHA = "3" * 64
AUX_SHA = "4" * 64
SCHEMA_SHA = "5" * 64
COMMIT_SHA = "6" * 40
PCGS_ID = "sha256:" + "7" * 64
PCGS_SOURCE_PATH = "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"
PCGS_SOURCE_SHA = "7" * 64
CLASS_ID = "HS-SYNTHETIC-BINDING-NEGATIVE-MATRIX"


def encoded(obj: dict[str, Any]) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()


def shards(total: int, size: int) -> list[dict[str, Any]]:
    return [{"name": f"shard_{i:05d}", "lo": lo,
             "hi": min(total - 1, lo + size - 1)}
            for i, lo in enumerate(range(0, total, size))]


def make_manifest() -> dict[str, Any]:
    rows = shards(705894, 3678)
    basis_fp = pcgs_basis_fingerprint(synthetic_basis_material("S"))
    obj = {
        "schema": "hsp7-mainrun-shard-manifest/v2",
        "lane": "S",
        "class_id": CLASS_ID,
        "source_bundle_sha256": SOURCE_SHA,
        "frozen_driver_digest": SOURCE_SHA,
        "pcgs_id": PCGS_ID,
        "pcgs_basis_contract": PCGS_BASIS_CONTRACT,
        "pcgs_basis_fingerprint": basis_fp,
        "pcgs_source_artifact_path": PCGS_SOURCE_PATH,
        "pcgs_source_artifact_sha256": PCGS_SOURCE_SHA,
        "total_candidates": 705894,
        "shard_size_target": 3678,
        "n_shards": len(rows),
        "timeout_min": 60,
        "max_parallel": 20,
        "max_jobs_per_workflow": 256,
        "key_semantics": {"radix": 7, "exponent_width": 6,
                          "m_values": [0, 1, 2, 4, 5, 6],
                          "f_total": 117649, "axis": "pair"},
        "endian": "big",
        "shards": rows,
    }
    obj["manifest_sha256"] = manifest_self_digest(obj)
    return obj


def make_class(manifest_bytes: bytes) -> dict[str, Any]:
    return {
        "schema": "hsp7-class-manifest-draft/v1",
        "status": "FROZEN_AUTHORIZED",
        "authorization": {"main_run": True, "workflow_dispatch": True},
        "capacity": {
            "per_lane_compressed_cap_bytes": {"S": 713031680, "V": 713031680,
                                                "P": 713031680},
            "per_lane_cap_sum_bytes": 2139095040,
            "whole_class_compressed_cap_bytes": 2147483648,
        },
        "class_id": CLASS_ID,
        "exact_universe": {"pcgs_id": PCGS_ID,
                           "pcgs_basis_contract": PCGS_BASIS_CONTRACT,
                           "pcgs_source_artifact_path": PCGS_SOURCE_PATH,
                           "pcgs_source_artifact_sha256": PCGS_SOURCE_SHA},
        "lanes": {
            "S": {
                "shard_manifest": MANIFEST_PATH,
                "shard_manifest_file_sha256": sha256_bytes(manifest_bytes),
                "source_bundle_sha256": SOURCE_SHA,
                "pcgs_basis_fingerprint": pcgs_basis_fingerprint(
                    synthetic_basis_material("S")),
                "compressed_cap_bytes": 713031680,
                "partition": {"total": 705894, "target_size": 3678,
                              "n_shards": 192, "timeout_min": 60,
                              "max_parallel": 20},
            }
        },
    }


def make_cert() -> dict[str, Any]:
    material = synthetic_basis_material("S")
    return {
        "schema": "hsp7-lane-cert/v3",
        "lane": "S",
        "axis": "pair",
        "class_id": CLASS_ID,
        "run": {"run_id": "123456", "run_attempt": "1",
                "commit_sha": COMMIT_SHA},
        "source_bindings": {
            "source_bundle_sha256": SOURCE_SHA,
            "wrapper_sha256": WRAPPER_SHA,
            "predicate_sha256": PREDICATE_SHA,
            "aux_sha256": AUX_SHA,
            "schema_sha256": SCHEMA_SHA,
        },
        "pcgs_basis_material": material,
        "pcgs_basis_fingerprint": pcgs_basis_fingerprint(material),
        "universe_total": 705894,
        "evaluated_range": [0, 0],
        "records": [{"pair_index": 0, "f_index": 0,
                     "candidate_key": {"m": 0, "e": [0, 0, 0, 0, 0, 0]},
                     "fixture_id": "synthetic-binding-row",
                     "status": "UNKNOWN", "unknown_reason": "synthetic"}],
        "summary": {"evaluated_count": 1, "unknown_count": 1,
                    "integrity_ok": True},
        "driver_done": True,
    }


def synthetic_basis_material(lane: str) -> dict[str, Any]:
    units = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    ambient_units = [[1 if i == j else 0 for j in range(8)] for i in range(8)]
    pairs = []
    for i in range(1, 7):
        for j in range(i + 1, 7):
            pairs.append({"i": i, "j": j, "coordinates": [0] * 6})
    return {
        "ambient_named_generator_coordinates": [
            {"name": "x", "coordinates": ambient_units[0]},
            {"name": "y", "coordinates": ambient_units[1]},
        ],
        "ambient_pcgs_relative_orders": [7] * 8,
        "contract": PCGS_BASIS_CONTRACT,
        "ordered_basis_in_ambient_coordinates": [
            {"i": i + 1, "coordinates": ambient_units[i + 2]} for i in range(6)],
        "relative_orders": [7] * 6,
        "pair_commutator_coordinates": pairs,
        "theta_image_coordinates": [
            {"i": i + 1, "coordinates": units[5 - i]} for i in range(6)],
        "tau_image_coordinates": [
            {"i": i + 1, "coordinates": units[(i + 1) % 6]} for i in range(6)],
        "s_to_v_bridge_coordinates": ([
            {"i": i + 1, "coordinates": units[i]} for i in range(6)]
            if lane == "V" else []),
        "source_artifact": {"path": PCGS_SOURCE_PATH, "sha256": PCGS_SOURCE_SHA},
    }


def make_receipt(cert_bytes: bytes, shard_id: str = "shard_00000") -> dict[str, Any]:
    return {
        "schema": "hsp7-lane-job-receipt/v1",
        "status": "PASS",
        "reason": "exact-shard-complete",
        "lane": "S",
        "class_id": CLASS_ID,
        "class_manifest": CLASS_PATH,
        "class_manifest_sha256": "8" * 64,
        "manifest": MANIFEST_PATH,
        "manifest_sha256": "9" * 64,
        "source_bundle_sha256": SOURCE_SHA,
        "runtime_pcgs_preflight": "PASS",
        "measured_pcgs_basis_fingerprint": pcgs_basis_fingerprint(
            synthetic_basis_material("S")),
        "shard_id": shard_id,
        "index_range": [0, 0],
        "cert_path": f"out/S_{shard_id}.json",
        "cert_sha256": sha256_bytes(cert_bytes),
        "raw_bytes": len(cert_bytes),
        "gzip_bytes": len(gzip.compress(cert_bytes, compresslevel=6, mtime=0)),
    }


def record(rows: list[dict[str, Any]], fixture: str, gate: str,
           checks: dict[str, bool], expected: str,
           must_fail: str | None = None) -> None:
    observed = "PASS" if all(checks.values()) else "STOP"
    failed = sorted(k for k, ok in checks.items() if not ok)
    ok = observed == expected and (must_fail is None or must_fail in failed)
    rows.append({"fixture": fixture, "gate": gate, "expected": expected,
                 "observed": observed, "must_fail": must_fail,
                 "failed_checks": failed, "pass": ok})


def mutate(base: dict[str, Any], fn: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    obj = copy.deepcopy(base)
    fn(obj)
    return obj


def main() -> int:
    rows: list[dict[str, Any]] = []
    manifest = make_manifest()
    manifest_bytes = encoded(manifest)
    class_obj = make_class(manifest_bytes)
    class_bytes = encoded(class_obj)

    def lock(obj: dict[str, Any], actual_path: str = CLASS_PATH,
             expected_path: str = CLASS_PATH, expected_sha: str | None = None) -> dict[str, bool]:
        data = encoded(obj)
        return class_lock_checks(
            class_bytes=data, class_obj=obj, actual_path=actual_path,
            expected_path=expected_path,
            expected_sha256=sha256_bytes(data) if expected_sha is None else expected_sha,
            required_status="FROZEN_AUTHORIZED")

    record(rows, "class-positive", "class-lock", lock(class_obj), "PASS")
    record(rows, "class-wrong-digest", "class-lock",
           lock(class_obj, expected_sha="0" * 64), "STOP", "class_sha256")
    record(rows, "class-wrong-path", "class-lock",
           lock(class_obj, actual_path="search/certs/attacker.json"),
           "STOP", "class_path")
    record(rows, "class-wrong-status", "class-lock",
           lock(mutate(class_obj, lambda x: x.update(status="BLOCKED"))),
           "STOP", "class_status")
    record(rows, "class-wrong-schema", "class-lock",
           lock(mutate(class_obj, lambda x: x.update(schema="hsp7-class-manifest-draft/v0"))),
           "STOP", "class_schema")
    record(rows, "class-main-run-not-authorized", "class-lock",
           lock(mutate(class_obj, lambda x: x["authorization"].update(main_run=False))),
           "STOP", "class_authorization_main_run")
    record(rows, "class-workflow-not-authorized", "class-lock",
           lock(mutate(class_obj, lambda x: x["authorization"].update(workflow_dispatch=False))),
           "STOP", "class_authorization_workflow_dispatch")

    def manifest_checks(m: dict[str, Any], c: dict[str, Any] | None = None,
                        live_sha: str = SOURCE_SHA,
                        actual_path: str = MANIFEST_PATH,
                        frozen_file_sha: str | None = None) -> dict[str, bool]:
        data = encoded(m)
        co = copy.deepcopy(class_obj if c is None else c)
        co["lanes"]["S"]["shard_manifest_file_sha256"] = (
            sha256_bytes(data) if frozen_file_sha is None else frozen_file_sha)
        return manifest_binding_checks(
            class_obj=co, manifest_obj=m, manifest_bytes=data,
            actual_manifest_path=actual_path, lane="S",
            live_source_bundle_sha256=live_sha)

    record(rows, "manifest-positive", "workflow-manifest",
           manifest_checks(manifest), "PASS")
    record(rows, "manifest-class-file-digest", "workflow-manifest",
           manifest_checks(manifest, frozen_file_sha="0" * 64),
           "STOP", "manifest_file_sha256")
    bad = mutate(manifest, lambda x: x.update(manifest_sha256="0" * 64))
    record(rows, "manifest-self-digest", "workflow-manifest",
           manifest_checks(bad), "STOP", "manifest_self_sha256")
    record(rows, "manifest-live-source", "workflow-manifest",
           manifest_checks(manifest, live_sha="a" * 64),
           "STOP", "source_bundle_live")
    bad_class = mutate(class_obj, lambda x: x["lanes"]["S"].update(source_bundle_sha256="a" * 64))
    record(rows, "manifest-class-source", "workflow-manifest",
           manifest_checks(manifest, bad_class), "STOP", "source_bundle_class")
    bad = mutate(manifest, lambda x: x["key_semantics"].update(axis="f"))
    bad["manifest_sha256"] = manifest_self_digest(bad)
    record(rows, "manifest-key-semantics", "workflow-manifest",
           manifest_checks(bad), "STOP", "key_semantics")
    bad = mutate(manifest, lambda x: x.update(pcgs_id="sha256:" + "a" * 64))
    bad["manifest_sha256"] = manifest_self_digest(bad)
    record(rows, "manifest-pcgs-source-id", "workflow-manifest",
           manifest_checks(bad), "STOP", "pcgs_source_artifact")
    bad = mutate(manifest, lambda x: x.update(pcgs_basis_fingerprint="a" * 64))
    bad["manifest_sha256"] = manifest_self_digest(bad)
    record(rows, "manifest-pcgs-runtime-fingerprint", "workflow-manifest",
           manifest_checks(bad), "STOP", "pcgs_basis_fingerprint")
    bad = mutate(manifest, lambda x: x["shards"][1].update(lo=3679))
    bad["manifest_sha256"] = manifest_self_digest(bad)
    record(rows, "manifest-coverage-gap", "workflow-manifest",
           manifest_checks(bad), "STOP", "shard_exact_cover")
    bad = mutate(manifest, lambda x: x["shards"][1].update(name="shard_00000"))
    bad["manifest_sha256"] = manifest_self_digest(bad)
    record(rows, "manifest-duplicate-shard", "workflow-manifest",
           manifest_checks(bad), "STOP", "shard_names_unique")
    record(rows, "manifest-wrong-path", "workflow-manifest",
           manifest_checks(manifest, actual_path="search/certs/attacker.json"),
           "STOP", "manifest_path")

    cert = make_cert()

    def cert_checks(obj: dict[str, Any]) -> dict[str, bool]:
        return cert_binding_checks(
            cert=obj, lane="S", axis="pair", universe_total=705894,
            class_id=CLASS_ID, run_id="123456", run_attempt="1",
            commit_sha=COMMIT_SHA, source_bundle_sha256=SOURCE_SHA,
            wrapper_sha256=WRAPPER_SHA, predicate_sha256=PREDICATE_SHA,
            aux_sha256=AUX_SHA, schema_sha256=SCHEMA_SHA,
            index_range=[0, 0], expected_count=1,
            expected_pcgs_basis_fingerprint=pcgs_basis_fingerprint(
                synthetic_basis_material("S")),
            expected_pcgs_source_artifact_path=PCGS_SOURCE_PATH,
            expected_pcgs_source_artifact_sha256=PCGS_SOURCE_SHA)

    record(rows, "cert-positive", "runner-cert", cert_checks(cert), "PASS")
    cert_mutants = [
        ("cert-axis", "axis", lambda x: x.update(axis="f")),
        ("cert-universe-total", "universe_total", lambda x: x.update(universe_total=117649)),
        ("cert-run-id", "run_id", lambda x: x["run"].update(run_id="other")),
        ("cert-run-attempt", "run_attempt", lambda x: x["run"].update(run_attempt="2")),
        ("cert-commit", "commit_sha", lambda x: x["run"].update(commit_sha="a" * 40)),
        ("cert-source-bundle", "source_bundle_sha256", lambda x: x["source_bindings"].update(source_bundle_sha256="a" * 64)),
        ("cert-wrapper", "wrapper_sha256", lambda x: x["source_bindings"].update(wrapper_sha256="a" * 64)),
        ("cert-predicate", "predicate_sha256", lambda x: x["source_bindings"].update(predicate_sha256="a" * 64)),
        ("cert-aux", "aux_sha256", lambda x: x["source_bindings"].update(aux_sha256="a" * 64)),
        ("cert-schema-digest", "schema_sha256", lambda x: x["source_bindings"].update(schema_sha256="a" * 64)),
        ("cert-pcgs-fingerprint", "pcgs_basis_fingerprint_self", lambda x: x.update(pcgs_basis_fingerprint="a" * 64)),
        ("cert-pcgs-commutator-coordinate", "pcgs_pair_rows_identity_expected", lambda x: x["pcgs_basis_material"]["pair_commutator_coordinates"][0]["coordinates"].__setitem__(3, 2)),
        ("cert-pcgs-theta-order", "pcgs_theta_rows_shape", lambda x: x["pcgs_basis_material"]["theta_image_coordinates"].reverse()),
        ("cert-pcgs-ambient-basis", "pcgs_basis_fingerprint_self", lambda x: x["pcgs_basis_material"]["ordered_basis_in_ambient_coordinates"][0]["coordinates"].__setitem__(2, 2)),
        ("cert-pcgs-source-artifact", "pcgs_source_artifact_expected", lambda x: x["pcgs_basis_material"]["source_artifact"].update(sha256="a" * 64)),
        ("cert-unknown-count", "unknown_count_consistency", lambda x: x["summary"].update(unknown_count=0)),
        ("cert-axis-record-arithmetic", "axis_record_shape", lambda x: x["records"][0].update(f_index=1)),
        ("cert-range", "range", lambda x: x.update(evaluated_range=[1, 1])),
        ("cert-driver-done", "driver_done", lambda x: x.update(driver_done=False)),
    ]
    for name, failed, fn in cert_mutants:
        record(rows, name, "runner-cert", cert_checks(mutate(cert, fn)),
               "STOP", failed)

    v_material = synthetic_basis_material("V")
    record(rows, "pcgs-v-bridge-positive", "pcgs-material",
           pcgs_basis_material_checks(v_material, "V"), "PASS")
    bad_v_material = copy.deepcopy(v_material)
    bad_v_material["s_to_v_bridge_coordinates"][0]["coordinates"] = [0, 1, 0, 0, 0, 0]
    record(rows, "pcgs-v-bridge-permutation", "pcgs-material",
           pcgs_basis_material_checks(bad_v_material, "V"),
           "STOP", "pcgs_bridge_pointwise_units")

    zero_key = {"m": 0, "e": [0, 0, 0, 0, 0, 0]}
    s_record = {"pair_index": 0, "f_index": 0, "candidate_key": zero_key,
                "fixture_id": "synthetic-S", "hex310": True,
                "hex311": False, "verdict": False}
    v_record = {"pair_index": 0, "f_index": 0, "candidate_key": zero_key,
                "fixture_id": "synthetic-V",
                "N": {"hex33": True, "hex34": False, "verdict": False},
                "N0": {"hex33": True, "hex34": False, "verdict": False},
                "N_N0_agree": True, "CF_baseline_agree": True}
    p_record = {"f_index": 0, "f_key": {"e": [0, 0, 0, 0, 0, 0]},
                "joined_pair_indices": [i * 117649 for i in range(6)],
                "fixture_id": "synthetic-P", "pentagon_verdict": False,
                "CONV_native_element_agree": True,
                "CONV_native_verdict_agree": True}
    for lane, row in (("S", s_record), ("V", v_record), ("P", p_record)):
        record(rows, f"axis-{lane}-positive", "axis-record",
               lane_record_checks([row], lane, [0, 0]), "PASS")
    record(rows, "axis-S-verdict-inconsistent", "axis-record",
           lane_record_checks([mutate(s_record, lambda x: x.update(verdict=True))],
                              "S", [0, 0]), "STOP", "axis_record_shape")
    record(rows, "axis-V-agreement-false", "axis-record",
           lane_record_checks([mutate(v_record, lambda x: x.update(N_N0_agree=False))],
                              "V", [0, 0]), "STOP", "axis_record_shape")
    record(rows, "axis-P-join-permutation", "axis-record",
           lane_record_checks([mutate(p_record, lambda x: x["joined_pair_indices"].reverse())],
                              "P", [0, 0]), "STOP", "axis_record_shape")

    cert_bytes = encoded(cert)
    receipt = make_receipt(cert_bytes)

    def receipt_relation(obj: dict[str, Any] | None, data: bytes | None = cert_bytes,
                         cap: int | None = None) -> dict[str, bool]:
        return receipt_cert_checks(
            receipt=obj, cert_bytes=data,
            per_shard_raw_cap=len(cert_bytes) if cap is None else cap)

    def receipt_binding(obj: dict[str, Any]) -> dict[str, bool]:
        return receipt_binding_checks(
            receipt=obj, lane="S", class_id=CLASS_ID,
            class_manifest_path=CLASS_PATH, class_manifest_sha256="8" * 64,
            manifest_path=MANIFEST_PATH, manifest_sha256="9" * 64,
            source_bundle_sha256=SOURCE_SHA, shard_id="shard_00000",
            index_range=[0, 0],
            expected_pcgs_basis_fingerprint=pcgs_basis_fingerprint(
                synthetic_basis_material("S")))

    record(rows, "receipt-positive", "receipt-cert",
           receipt_relation(receipt), "PASS")
    record(rows, "receipt-missing", "receipt-cert",
           receipt_relation(None), "STOP", "receipt_present")
    record(rows, "receipt-stop-status", "receipt-cert",
           receipt_relation(mutate(receipt, lambda x: x.update(status="STOP"))),
           "STOP", "receipt_pass")
    record(rows, "receipt-cert-missing", "receipt-cert",
           receipt_relation(receipt, data=None), "STOP", "cert_present")
    record(rows, "receipt-cert-hash", "receipt-cert",
           receipt_relation(mutate(receipt, lambda x: x.update(cert_sha256="a" * 64))),
           "STOP", "cert_sha256")
    record(rows, "receipt-raw-size", "receipt-cert",
           receipt_relation(mutate(receipt, lambda x: x.update(raw_bytes=x["raw_bytes"] + 1))),
           "STOP", "raw_bytes_receipt")
    record(rows, "receipt-gzip-size", "receipt-cert",
           receipt_relation(mutate(receipt, lambda x: x.update(gzip_bytes=x["gzip_bytes"] + 1))),
           "STOP", "gzip_bytes_receipt")
    record(rows, "receipt-raw-cap", "receipt-cert",
           receipt_relation(receipt, cap=len(cert_bytes) - 1),
           "STOP", "per_shard_raw_cap")
    record(rows, "receipt-binding-positive", "receipt-binding",
           receipt_binding(receipt), "PASS")
    record(rows, "receipt-class-digest", "receipt-binding",
           receipt_binding(mutate(receipt, lambda x: x.update(class_manifest_sha256="a" * 64))),
           "STOP", "receipt_class_manifest_sha256")
    record(rows, "receipt-manifest-path", "receipt-binding",
           receipt_binding(mutate(receipt, lambda x: x.update(manifest="search/certs/attacker.json"))),
           "STOP", "receipt_manifest_path")
    record(rows, "receipt-source-bundle", "receipt-binding",
           receipt_binding(mutate(receipt, lambda x: x.update(source_bundle_sha256="a" * 64))),
           "STOP", "receipt_source_bundle_sha256")
    record(rows, "receipt-shard", "receipt-binding",
           receipt_binding(mutate(receipt, lambda x: x.update(shard_id="shard_00001"))),
           "STOP", "receipt_shard_id")
    record(rows, "receipt-index-range", "receipt-binding",
           receipt_binding(mutate(receipt, lambda x: x.update(index_range=[1, 1]))),
           "STOP", "receipt_index_range")
    record(rows, "receipt-runtime-pcgs-preflight", "receipt-binding",
           receipt_binding(mutate(receipt, lambda x: x.update(runtime_pcgs_preflight="STOP"))),
           "STOP", "receipt_runtime_pcgs_preflight")
    record(rows, "receipt-runtime-pcgs-fingerprint", "receipt-binding",
           receipt_binding(mutate(receipt, lambda x: x.update(
               measured_pcgs_basis_fingerprint="a" * 64))),
           "STOP", "receipt_runtime_pcgs_fingerprint")

    receipt2 = make_receipt(cert_bytes, "shard_00001")
    receipt2["index_range"] = [1, 1]
    expected_ids = {"shard_00000", "shard_00001"}

    def collection(items: list[dict[str, Any]], cap: int | None = None) -> dict[str, bool]:
        actual_cap = (receipt["gzip_bytes"] + receipt2["gzip_bytes"]
                      if cap is None else cap)
        return collection_capacity_checks(
            receipts=items, expected_receipt_count=2,
            collection_gzip_cap=actual_cap,
            expected_shard_ids=expected_ids)

    record(rows, "collection-positive", "workflow-collection",
           collection([receipt, receipt2]), "PASS")
    record(rows, "collection-missing-receipt", "workflow-collection",
           collection([receipt]), "STOP", "receipt_count")
    record(rows, "collection-duplicate-shard", "workflow-collection",
           collection([receipt, copy.deepcopy(receipt)]),
           "STOP", "exact_unique_shard_set")
    record(rows, "collection-stop-receipt", "workflow-collection",
           collection([receipt, mutate(receipt2, lambda x: x.update(status="STOP"))]),
           "STOP", "all_receipts_pass")
    record(rows, "collection-negative-gzip", "workflow-collection",
           collection([receipt, mutate(receipt2, lambda x: x.update(gzip_bytes=-1))]),
           "STOP", "gzip_values_nonnegative")
    record(rows, "collection-lane-cap", "workflow-collection",
           collection([receipt, receipt2], cap=receipt["gzip_bytes"] + receipt2["gzip_bytes"] - 1),
           "STOP", "collection_gzip_cap")

    capacity = class_obj["capacity"]
    record(rows, "class-lane-cap-positive", "class-capacity",
           class_lane_capacity_checks(capacity), "PASS")
    record(rows, "class-lane-cap-overallocation", "class-capacity",
           class_lane_capacity_checks(mutate(
               capacity, lambda x: x["per_lane_compressed_cap_bytes"].update(S=2147483648))),
           "STOP", "lane_cap_sum_within_class")
    record(rows, "class-lane-cap-sum-lie", "class-capacity",
           class_lane_capacity_checks(mutate(
               capacity, lambda x: x.update(per_lane_cap_sum_bytes=1))),
           "STOP", "lane_cap_sum_recorded")

    result = {
        "schema": "hsp7-binding-negative-matrix/v2",
        "scope": "pure synthetic class/workflow/cert/receipt/cap bindings",
        "candidate_universe_contact": 0,
        "gap_invocations": 0,
        "fixture_count": len(rows),
        "positive_count": sum(r["expected"] == "PASS" for r in rows),
        "negative_count": sum(r["expected"] == "STOP" for r in rows),
        "expectation_match_count": sum(r["pass"] for r in rows),
        "rows": rows,
        "overall_pass": all(r["pass"] for r in rows),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("fixture_count", "positive_count",
                                             "negative_count", "expectation_match_count",
                                             "overall_pass")}, indent=2))
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
