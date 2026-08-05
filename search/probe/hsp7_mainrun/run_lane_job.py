#!/usr/bin/env python3
"""Fail-closed Linux/GHA runner for one frozen HS shard.

This script is implementation plumbing only.  It never chooses a manifest
or candidate range: both must already exist in the immutable class manifest.
It enforces a hard shard timeout around GAP, validates the emitted cert, and
writes a receipt whose PASS requires exit=0, exact source binding, exact
range/count, integrity_ok=true, and driver_done=true.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from binding_gate_lib import (cert_binding_checks, class_lane_capacity_checks,
                              manifest_binding_checks, pcgs_basis_fingerprint,
                              pcgs_basis_material_checks)

ROOT = Path(__file__).resolve().parents[3]

LANE_SOURCES = {
    "S": ["search/probe/hsp7_mainrun/run_lane_job.py",
          "search/probe/hsp7_mainrun/binding_gate_lib.py",
          "search/probe/hsp7_mainrun/lane_wrapper_S.g",
          "search/probe/hsp7_mainrun/predicate_lib_laneS.g",
          "search/probe/hsp7_mainrun/candidate_key_lib.g",
          "search/probe/hsp7_mainrun/cert_io.g",
          "search/certs/hsp7_lane_cert_schema_v3.json",
          "search/probe/wac_v1/gap_output_prelude.g",
          "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"],
    "V": ["search/probe/hsp7_mainrun/run_lane_job.py",
          "search/probe/hsp7_mainrun/binding_gate_lib.py",
          "search/probe/hsp7_mainrun/lane_wrapper_V.g",
          "search/probe/hsp7_mainrun/predicate_lib_laneV_cf.g",
          "search/probe/hsp7_mainrun/candidate_key_lib.g",
          "search/probe/hsp7_mainrun/cert_io.g",
          "search/certs/hsp7_lane_cert_schema_v3.json",
          "search/probe/wac_v1/gap_output_prelude.g",
          "search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g",
          "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"],
    "P": ["search/probe/hsp7_mainrun/run_lane_job.py",
          "search/probe/hsp7_mainrun/binding_gate_lib.py",
          "search/probe/hsp7_mainrun/lane_wrapper_P.g",
          "search/probe/hsp7_mainrun/predicate_lib_laneP.g",
          "search/probe/hsp7_mainrun/predicate_lib_laneP_conv.g",
          "search/probe/hsp7_mainrun/candidate_key_lib.g",
          "search/probe/hsp7_mainrun/cert_io.g",
          "search/certs/hsp7_lane_cert_schema_v3.json",
          "search/probe/wac_v1/gap_output_prelude.g",
          "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g",
          "search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g"],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle(paths: list[Path]) -> str:
    data = "".join(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in sorted(paths)).encode()
    return hashlib.sha256(data).hexdigest()


def write_receipt(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--class-manifest", required=True)
    ap.add_argument("--shard", required=True)
    ap.add_argument("--cert", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--gap-command", default="gap")
    ap.add_argument("--preflight-only", action="store_true")
    args = ap.parse_args()
    receipt_path, log_path, cert_path = Path(args.receipt), Path(args.log), Path(args.cert)
    base = {"schema": "hsp7-lane-job-receipt/v1", "manifest": args.manifest,
            "shard_id": args.shard, "cert_path": args.cert}
    try:
        class_path = Path(args.class_manifest)
        class_manifest = json.loads(class_path.read_text(encoding="utf-8"))
        if class_manifest.get("schema") != "hsp7-class-manifest-draft/v1":
            raise ValueError("class manifest schema mismatch")
        if class_manifest.get("status") != "FROZEN_AUTHORIZED":
            if not args.preflight_only:
                raise ValueError("class manifest is not FROZEN_AUTHORIZED")
        if not args.preflight_only:
            auth = class_manifest.get("authorization", {})
            if auth.get("main_run") is not True or auth.get("workflow_dispatch") is not True:
                raise ValueError("class main_run/workflow_dispatch authorization is not true")
        capacity_checks = class_lane_capacity_checks(class_manifest.get("capacity"))
        if not all(capacity_checks.values()):
            raise ValueError("class capacity gate(s): " + ",".join(
                k for k, ok in capacity_checks.items() if not ok))
        manifest_path = Path(args.manifest)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        lane = manifest.get("lane")
        if lane not in LANE_SOURCES:
            raise ValueError("unknown lane")
        class_lane = class_manifest.get("lanes", {}).get(lane)
        if not isinstance(class_lane, dict):
            raise ValueError("lane absent from class manifest")
        source_paths = [ROOT / p for p in LANE_SOURCES[lane]]
        actual_bundle = bundle(source_paths)
        manifest_checks = manifest_binding_checks(
            class_obj=class_manifest,
            manifest_obj=manifest,
            manifest_bytes=manifest_path.read_bytes(),
            actual_manifest_path=manifest_path.as_posix(),
            lane=lane,
            live_source_bundle_sha256=actual_bundle,
        )
        if not all(manifest_checks.values()):
            failed = sorted(k for k, ok in manifest_checks.items() if not ok)
            raise ValueError("manifest fail-closed binding check(s): " + ",".join(failed))
        matches = [s for s in manifest["shards"] if s["name"] == args.shard]
        if len(matches) != 1:
            raise ValueError("shard name absent or duplicated")
        shard = matches[0]
        base.update({"lane": lane, "class_id": manifest["class_id"],
                     "class_manifest": args.class_manifest, "class_manifest_sha256": sha(class_path),
                     "manifest_sha256": sha(manifest_path), "source_bundle_sha256": actual_bundle,
                     "index_range": [shard["lo"], shard["hi"]]})
        if args.preflight_only:
            base.update({"status": "PASS", "reason": "source-and-manifest-preflight-only",
                         "candidate_evaluations": 0})
            write_receipt(receipt_path, base)
            return 0
        wrapper = ROOT / f"search/probe/hsp7_mainrun/lane_wrapper_{lane}.g"
        predicate = ROOT / ("search/probe/hsp7_mainrun/predicate_lib_laneV_cf.g" if lane == "V" else
                            f"search/probe/hsp7_mainrun/predicate_lib_lane{lane}.g")
        aux_paths = [p for p in source_paths if p not in (wrapper, predicate)]
        run_id = os.environ.get("GITHUB_RUN_ID")
        run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
        commit_sha = os.environ.get("GITHUB_SHA")
        if None in (run_id, run_attempt, commit_sha):
            raise ValueError("GITHUB_RUN_ID/GITHUB_RUN_ATTEMPT/GITHUB_SHA binding missing")
        if cert_path.exists():
            raise ValueError("cert output path already exists; stale-cert reuse is forbidden")
        basis_fingerprint = manifest.get("pcgs_basis_fingerprint")
        if not isinstance(basis_fingerprint, str):
            raise ValueError("frozen pcgs basis fingerprint is absent")
        pcgs_source_path = class_manifest.get("exact_universe", {}).get("pcgs_source_artifact_path")
        pcgs_source_sha = class_manifest.get("exact_universe", {}).get("pcgs_source_artifact_sha256")
        if not isinstance(pcgs_source_path, str) or not isinstance(pcgs_source_sha, str):
            raise ValueError("frozen authoritative pcgs source artifact binding is absent")
        basis_timeout_min = class_manifest.get("stop_unknown", {}).get(
            "runtime_pcgs_preflight_timeout_min")
        if basis_timeout_min != 15:
            raise ValueError("runtime PCGS preflight timeout is not frozen at 15 minutes")
        basis_log_text = ""
        with tempfile.TemporaryDirectory(prefix="hsp7_basis_gate_") as td:
            basis_out = Path(td) / f"basis_{lane}.json"
            basis_driver = Path(td) / f"basis_{lane}.g"
            basis_driver.write_text("\n".join([
                'RUN_MODE := "BASIS_ONLY";;',
                f'OUT_BASIS_PATH := "{basis_out.as_posix()}";;',
                f'PCGS_SOURCE_ARTIFACT_PATH := "{pcgs_source_path}";;',
                f'PCGS_SOURCE_ARTIFACT_SHA256 := "{pcgs_source_sha}";;',
                f'Read("{wrapper.relative_to(ROOT).as_posix()}");',
            ]) + "\n", encoding="ascii")
            try:
                basis_proc = subprocess.run(
                    [args.gap_command, "-q", "--quitonbreak", "-o", "4g", str(basis_driver)],
                    cwd=ROOT, text=True, capture_output=True,
                    timeout=basis_timeout_min * 60)
            except subprocess.TimeoutExpired as exc:
                basis_log_text = ((exc.stdout or "") + "\n[stderr]\n" +
                                  (exc.stderr or "") + "\n[PCGS_BASIS_PREFLIGHT_TIMEOUT]\n")
                log_path.write_text(basis_log_text, encoding="utf-8")
                base.update({"status": "STOP", "reason": "PCGS_BASIS_PREFLIGHT_TIMEOUT",
                             "candidate_evaluations": 0, "log_sha256": sha(log_path)})
                write_receipt(receipt_path, base)
                return 1
            basis_log_text = ("[PCGS_BASIS_PREFLIGHT]\n" + basis_proc.stdout
                              + "\n[stderr]\n" + basis_proc.stderr + "\n")
            if basis_proc.returncode != 0 or not basis_out.is_file():
                log_path.write_text(basis_log_text, encoding="utf-8")
                base.update({"status": "STOP", "reason": "PCGS_BASIS_PREFLIGHT_FAILED",
                             "candidate_evaluations": 0,
                             "basis_exit_code": basis_proc.returncode,
                             "log_sha256": sha(log_path)})
                write_receipt(receipt_path, base)
                return 1
            material = json.loads(basis_out.read_text(encoding="utf-8"))
            material_checks = pcgs_basis_material_checks(
                material, lane, pcgs_source_path, pcgs_source_sha)
            measured_fp = pcgs_basis_fingerprint(material)
            if not all(material_checks.values()) or measured_fp != basis_fingerprint:
                log_path.write_text(basis_log_text, encoding="utf-8")
                base.update({"status": "STOP", "reason": "PCGS_BASIS_FINGERPRINT_MISMATCH",
                             "candidate_evaluations": 0,
                             "pcgs_basis_checks": material_checks,
                             "measured_pcgs_basis_fingerprint": measured_fp,
                             "expected_pcgs_basis_fingerprint": basis_fingerprint,
                             "log_sha256": sha(log_path)})
                write_receipt(receipt_path, base)
                return 1
            base.update({"runtime_pcgs_preflight": "PASS",
                         "measured_pcgs_basis_fingerprint": measured_fp,
                         "basis_probe_log_sha256": hashlib.sha256(
                             basis_log_text.encode()).hexdigest()})
        lines = [f'RUN_MODE := "SHARD";;', f'OUT_CERT_PATH := "{cert_path.as_posix()}";;',
                 f'CLASS_ID := "{manifest["class_id"]}";;', f'RUN_ID := "{run_id}";;',
                 f'RUN_ATTEMPT := "{run_attempt}";;', f'COMMIT_SHA := "{commit_sha}";;',
                 f'SOURCE_BUNDLE_SHA256 := "{actual_bundle}";;',
                 f'WRAPPER_SHA256 := "{sha(wrapper)}";;', f'PREDICATE_SHA256 := "{sha(predicate)}";;',
                 f'AUX_SHA256 := "{bundle(aux_paths)}";;',
                 f'SCHEMA_SHA256 := "{sha(ROOT / "search/certs/hsp7_lane_cert_schema_v3.json")}";;',
                 f'PCGS_BASIS_FINGERPRINT := "{basis_fingerprint}";;',
                 f'PCGS_SOURCE_ARTIFACT_PATH := "{pcgs_source_path}";;',
                 f'PCGS_SOURCE_ARTIFACT_SHA256 := "{pcgs_source_sha}";;']
        if lane == "P":
            lines += [f"SHARD_LO_F := {shard['lo']};;", f"SHARD_HI_F := {shard['hi']};;"]
        else:
            lines += [f"SHARD_LO := {shard['lo']};;", f"SHARD_HI := {shard['hi']};;"]
        lines.append(f'Read("{wrapper.relative_to(ROOT).as_posix()}");')
        with tempfile.NamedTemporaryFile("w", suffix=".g", encoding="ascii", delete=False) as tmp:
            tmp.write("\n".join(lines) + "\n")
            tmp_path = Path(tmp.name)
        try:
            proc = subprocess.run([args.gap_command, "-q", "--quitonbreak", "-o", "4g", str(tmp_path)],
                                  cwd=ROOT, text=True, capture_output=True,
                                  timeout=int(manifest["timeout_min"]) * 60)
            log_path.write_text(basis_log_text + "[SHARD]\n" + proc.stdout
                                + "\n[stderr]\n" + proc.stderr, encoding="utf-8")
        except subprocess.TimeoutExpired as exc:
            log_path.write_text(basis_log_text + "[SHARD]\n" + (exc.stdout or "")
                                + "\n[HARD_TIMEOUT]\n" + (exc.stderr or ""), encoding="utf-8")
            base.update({"status": "STOP", "reason": "HARD_SHARD_TIMEOUT",
                         "timeout_min": manifest["timeout_min"], "log_sha256": sha(log_path)})
            write_receipt(receipt_path, base)
            return 1
        finally:
            tmp_path.unlink(missing_ok=True)
        if proc.returncode != 0:
            base.update({"status": "STOP", "reason": "GAP_NONZERO_EXIT", "exit_code": proc.returncode,
                         "log_sha256": sha(log_path)})
            write_receipt(receipt_path, base)
            return 1
        cert = json.loads(cert_path.read_text(encoding="utf-8"))
        expected_count = shard["hi"] - shard["lo"] + 1
        schema_path = ROOT / "search/certs/hsp7_lane_cert_schema_v3.json"
        checks = cert_binding_checks(
            cert=cert,
            lane=lane,
            axis="f" if lane == "P" else "pair",
            universe_total=117649 if lane == "P" else 705894,
            class_id=manifest["class_id"],
            run_id=run_id,
            run_attempt=run_attempt,
            commit_sha=commit_sha,
            source_bundle_sha256=actual_bundle,
            wrapper_sha256=sha(wrapper),
            predicate_sha256=sha(predicate),
            aux_sha256=bundle(aux_paths),
            schema_sha256=sha(schema_path),
            index_range=[shard["lo"], shard["hi"]],
            expected_count=expected_count,
            expected_pcgs_basis_fingerprint=basis_fingerprint,
            expected_pcgs_source_artifact_path=pcgs_source_path,
            expected_pcgs_source_artifact_sha256=pcgs_source_sha,
        )
        if not all(checks.values()):
            base.update({"status": "STOP", "reason": "CERT_FAIL_CLOSED_CHECK", "checks": checks,
                         "exit_code": proc.returncode, "log_sha256": sha(log_path)})
            write_receipt(receipt_path, base)
            return 1
        raw_bytes = cert_path.stat().st_size
        gzip_bytes = len(gzip.compress(cert_path.read_bytes(), compresslevel=6, mtime=0))
        shard_cap = class_manifest["capacity"]["per_shard_uncompressed_cap_bytes"]
        if raw_bytes > shard_cap:
            cert_sha = sha(cert_path)
            cert_path.unlink()
            base.update({"status": "STOP", "reason": "PER_SHARD_CAP_EXCEEDED",
                         "raw_bytes": raw_bytes, "gzip_bytes": gzip_bytes,
                         "cap_bytes": shard_cap, "discarded_cert_sha256": cert_sha,
                         "log_sha256": sha(log_path)})
            write_receipt(receipt_path, base)
            return 1
        base.update({"status": "PASS", "reason": "exact-shard-complete", "checks": checks,
                     "exit_code": 0, "cert_sha256": sha(cert_path), "log_sha256": sha(log_path),
                     "evaluated_count": expected_count, "raw_bytes": raw_bytes,
                     "gzip_bytes": gzip_bytes})
        write_receipt(receipt_path, base)
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError,
            IndexError, json.JSONDecodeError) as exc:
        base.update({"status": "STOP", "reason": "PREFLIGHT_OR_IO_ERROR", "detail": str(exc)})
        write_receipt(receipt_path, base)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
