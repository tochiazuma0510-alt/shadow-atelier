#!/usr/bin/env python3
"""Run only the registered HS fixtures through the production wrappers.

No SHARD mode is reachable from this preflight.  GAP preambles are created
in the operating-system temporary directory and bind every source digest
computed from the files that are actually about to be executed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from binding_gate_lib import (PCGS_BASIS_CONTRACT, lane_record_checks,
                              pcgs_basis_fingerprint,
                               pcgs_basis_material_checks)

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "search" / "certs"
SCHEMA = ROOT / "search" / "certs" / "hsp7_lane_cert_schema_v3.json"
CLASS_ID = "HS-NW7-CLASS-v3-draft"
PCGS_SOURCE_REL = "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"
PCGS_SOURCE = ROOT / PCGS_SOURCE_REL
AGG_OUT = OUT_DIR / "hsp7_registered_wrappers_preflight_pcgs_v3_20260805.json"
PROVENANCE_STOP_OUT = OUT_DIR / "hsp7_registered_wrappers_preflight_pcgs_v3_precommit_stop_20260805.json"
ORCHESTRATOR_REL = "search/probe/hsp7_mainrun/registered_preflight.py"
VALIDATOR_REL = "search/probe/hsp7_mainrun/binding_gate_lib.py"
GAP_WRAPPER_REL = "gap.ps1"

P5_SOURCES = [
    "search/probe/hsp7_mainrun/driver_conv_laneP_p5control_calib.g",
    "search/probe/hsp7_mainrun/predicate_lib_laneP_conv.g",
    "search/probe/wac_v1/gap_output_prelude.g",
    "search/probe/hsp7_cond4_laneP_p5control/PQ_OUTPUT_P5.g",
    "search/probe/hsp7_cond4_laneP_p5control/PQ_OUTPUT_Q5.g",
]

LANES = {
    "S": {
        "wrapper": "search/probe/hsp7_mainrun/lane_wrapper_S.g",
        "predicate": "search/probe/hsp7_mainrun/predicate_lib_laneS.g",
        "aux": ["search/probe/hsp7_mainrun/candidate_key_lib.g", "search/probe/hsp7_mainrun/cert_io.g",
                "search/probe/wac_v1/gap_output_prelude.g",
                "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"],
        "cert": "search/certs/hsp7_laneS_registered_preflight_pcgs_v3_20260805.json",
    },
    "V": {
        "wrapper": "search/probe/hsp7_mainrun/lane_wrapper_V.g",
        "predicate": "search/probe/hsp7_mainrun/predicate_lib_laneV_cf.g",
        "aux": ["search/probe/hsp7_mainrun/candidate_key_lib.g", "search/probe/hsp7_mainrun/cert_io.g",
                "search/probe/hsp7_mainrun/predicate_lib_laneV.g",
                "search/probe/hsp7_cond4_laneV/statemachine_lib.g",
                "search/probe/wac_v1/gap_output_prelude.g",
                "search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g", "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g"],
        "cert": "search/certs/hsp7_laneV_registered_preflight_pcgs_v3_20260805.json",
    },
    "P": {
        "wrapper": "search/probe/hsp7_mainrun/lane_wrapper_P.g",
        "predicate": "search/probe/hsp7_mainrun/predicate_lib_laneP.g",
        "aux": ["search/probe/hsp7_mainrun/predicate_lib_laneP_conv.g",
                "search/probe/hsp7_mainrun/candidate_key_lib.g", "search/probe/hsp7_mainrun/cert_io.g",
                "search/probe/wac_v1/gap_output_prelude.g",
                "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g",
                "search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g"],
        "cert": "search/certs/hsp7_laneP_registered_preflight_pcgs_v3_20260805.json",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle_digest(paths: list[Path]) -> str:
    payload = "".join(f"{digest(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in sorted(paths)).encode()
    return hashlib.sha256(payload).hexdigest()


def aggregate_digest(paths: list[Path]) -> str:
    return bundle_digest(paths)


def provenance_paths() -> list[str]:
    paths = {ORCHESTRATOR_REL, VALIDATOR_REL, GAP_WRAPPER_REL, *P5_SOURCES}
    for cfg in LANES.values():
        paths.update((cfg["wrapper"], cfg["predicate"], *cfg["aux"]))
    paths.add(SCHEMA.relative_to(ROOT).as_posix())
    return sorted(paths)


def source_commit_evidence() -> tuple[str, dict[str, str]]:
    """Require a commit that contains the exact bytes about to be executed."""
    commit = os.environ.get("HSP7_SOURCE_COMMIT_SHA", "")
    if re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", commit) is None:
        raise ValueError("HSP7_SOURCE_COMMIT_SHA must be an explicit 40/64-hex source commit")
    commit = commit.lower()
    rows: dict[str, str] = {}
    for rel in provenance_paths():
        live = (ROOT / rel).read_bytes()
        proc = subprocess.run(["git", "show", f"{commit}:{rel}"], cwd=ROOT,
                              capture_output=True, check=False)
        if proc.returncode != 0:
            raise ValueError(f"source commit does not contain {rel}")
        if proc.stdout != live:
            raise ValueError(f"source commit/live byte mismatch: {rel}")
        rows[rel] = hashlib.sha256(live).hexdigest()
    return commit, rows


def run_gap(preamble: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
         str(ROOT / "gap.ps1"), "-ScriptPath", str(preamble)],
        cwd=ROOT, text=True, capture_output=True, timeout=1800,
    )


def bounded_error_tail(proc: subprocess.CompletedProcess[str] | None,
                       limit: int = 4096) -> str | None:
    """Keep enough candidate-free GAP output to diagnose a STOP receipt."""
    if proc is None:
        return None
    combined = proc.stdout + "\n[stderr]\n" + proc.stderr
    return combined[-limit:] if combined else None


def validate_cert(lane: str, path: Path, source_sha: str,
                   bindings: dict[str, str], expected_fingerprint: str) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema") != "hsp7-lane-cert/v3" or obj.get("lane") != lane:
        raise ValueError("schema/lane mismatch")
    if obj.get("driver_done") is not True or obj.get("summary", {}).get("integrity_ok") is not True:
        raise ValueError("driver_done/integrity gate failed")
    if obj["source_bindings"]["source_bundle_sha256"] != source_sha:
        raise ValueError("source bundle digest mismatch")
    expected_source = {
        "source_bundle_sha256": bindings["SOURCE_BUNDLE_SHA256"],
        "wrapper_sha256": bindings["WRAPPER_SHA256"],
        "predicate_sha256": bindings["PREDICATE_SHA256"],
        "aux_sha256": bindings["AUX_SHA256"],
        "schema_sha256": bindings["SCHEMA_SHA256"],
    }
    if obj.get("source_bindings") != expected_source:
        raise ValueError("full source-binding mismatch")
    expected_run = {"run_id": bindings["RUN_ID"], "run_attempt": bindings["RUN_ATTEMPT"],
                    "commit_sha": bindings["COMMIT_SHA"]}
    if obj.get("run") != expected_run or obj.get("class_id") != bindings["CLASS_ID"]:
        raise ValueError("run/class binding mismatch")
    expected_axis = "f" if lane == "P" else "pair"
    expected_total = 117649 if lane == "P" else 705894
    expected_count = 8 if lane == "P" else 13
    if (obj.get("axis") != expected_axis or obj.get("universe_total") != expected_total
            or obj.get("evaluated_range") != [-1, -1]):
        raise ValueError("axis/universe/registered-range mismatch")
    material_checks = pcgs_basis_material_checks(
        obj.get("pcgs_basis_material"), lane, PCGS_SOURCE_REL, digest(PCGS_SOURCE))
    if not all(material_checks.values()):
        raise ValueError("pcgs material check(s): " + ",".join(
            k for k, ok in material_checks.items() if not ok))
    computed = pcgs_basis_fingerprint(obj["pcgs_basis_material"])
    if obj.get("pcgs_basis_fingerprint") != computed or computed != expected_fingerprint:
        raise ValueError("pcgs basis fingerprint self/expected mismatch")
    if obj["summary"]["evaluated_count"] != len(obj["records"]):
        raise ValueError("record count mismatch")
    if obj["summary"]["evaluated_count"] != expected_count:
        raise ValueError("registered fixture count mismatch")
    actual_unknown = sum(r.get("status") == "UNKNOWN" for r in obj["records"]
                         if isinstance(r, dict))
    if obj["summary"].get("unknown_count") != actual_unknown:
        raise ValueError("UNKNOWN count mismatch")
    record_checks = lane_record_checks(obj["records"], lane, [-1, -1])
    if not all(record_checks.values()):
        raise ValueError("lane record semantic check(s): " + ",".join(
            k for k, ok in record_checks.items() if not ok))
    return obj


def core_material(material: dict) -> dict:
    out = dict(material)
    out["s_to_v_bridge_coordinates"] = []
    return out


def expected_fixture_verdicts() -> dict[str, bool]:
    out = {f"h4t{t}": True for t in range(7)}
    out.update({"h3": False, "one-m1": False, "one-m2": False,
                "one-m4": False, "one-m5": False, "one-m6": True})
    return out


def main() -> int:
    try:
        commit, commit_files = source_commit_evidence()
    except (OSError, ValueError) as exc:
        receipt = {
            "schema": "hsp7-registered-wrapper-preflight/v3",
            "class_id": CLASS_ID,
            "candidate_universe_contact": 0,
            "registered_fixture_plan": {"S": 13, "V": 13, "P_production": 8,
                                        "P5_two_path": 5},
            "actual_evaluated": {}, "pcgs_basis_contract": PCGS_BASIS_CONTRACT,
            "pcgs_basis_fingerprints": {}, "pcgs_core_fingerprint": None,
            "source_commit_sha": None, "source_commit_files": {},
            "orchestrator": {
                "path": ORCHESTRATOR_REL, "sha256": digest(ROOT / ORCHESTRATOR_REL),
                "validator_path": VALIDATOR_REL,
                "validator_sha256": digest(ROOT / VALIDATOR_REL),
                "gap_wrapper_path": GAP_WRAPPER_REL,
                "gap_wrapper_sha256": digest(ROOT / GAP_WRAPPER_REL),
            },
            "rows": [], "comparisons": {}, "overall_pass": False,
            "provenance_error": str(exc),
            "note": "STOP before GAP; no registered or candidate fixture was evaluated.",
        }
        PROVENANCE_STOP_OUT.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1
    schema_sha = digest(SCHEMA)
    rows: list[dict] = []
    certs: dict[str, dict] = {}
    comparisons: dict[str, object] = {}
    overall = True
    for lane, cfg in LANES.items():
        wrapper = ROOT / cfg["wrapper"]
        predicate = ROOT / cfg["predicate"]
        aux_paths = [ROOT / p for p in cfg["aux"]]
        all_paths = [wrapper, predicate, *aux_paths, SCHEMA]
        source_sha = bundle_digest(all_paths)
        aux_sha = aggregate_digest(aux_paths)
        cert_path = ROOT / cfg["cert"]
        basis_path = Path(tempfile.gettempdir()) / f"hsp7_basis_material_{lane}.json"
        basis_path.unlink(missing_ok=True)
        basis_lines = ['RUN_MODE := "BASIS_ONLY";;',
                       f'OUT_BASIS_PATH := "{basis_path.as_posix()}";;',
                       f'PCGS_SOURCE_ARTIFACT_PATH := "{PCGS_SOURCE_REL}";;',
                       f'PCGS_SOURCE_ARTIFACT_SHA256 := "{digest(PCGS_SOURCE)}";;',
                       f'Read("{cfg["wrapper"]}");']
        with tempfile.NamedTemporaryFile("w", suffix=f"_hsp7_basis_{lane}.g",
                                         encoding="ascii", delete=False) as tmp:
            tmp.write("\n".join(basis_lines) + "\n")
            basis_driver = Path(tmp.name)
        basis_proc = None
        basis_log_sha = None
        material = None
        fingerprint = None
        basis_error = None
        try:
            basis_proc = run_gap(basis_driver)
            basis_log = (basis_proc.stdout + "\n[stderr]\n" + basis_proc.stderr).encode()
            basis_log_sha = hashlib.sha256(basis_log).hexdigest()
            if basis_proc.returncode != 0 or not basis_path.is_file():
                basis_error = (f"basis GAP exit={basis_proc.returncode}, "
                               f"material_exists={basis_path.is_file()}")
            else:
                material = json.loads(basis_path.read_text(encoding="utf-8"))
                material_checks = pcgs_basis_material_checks(
                    material, lane, PCGS_SOURCE_REL, digest(PCGS_SOURCE))
                if not all(material_checks.values()):
                    basis_error = "pcgs material check(s): " + ",".join(
                        k for k, ok in material_checks.items() if not ok)
                else:
                    fingerprint = pcgs_basis_fingerprint(material)
        except (subprocess.TimeoutExpired, OSError, ValueError, json.JSONDecodeError) as exc:
            basis_error = f"basis probe failed: {exc}"
        finally:
            basis_driver.unlink(missing_ok=True)
            basis_path.unlink(missing_ok=True)

        if basis_error is not None or fingerprint is None:
            rows.append({"lane": lane, "exit_code": None, "pass": False,
                         "error": basis_error or "basis fingerprint absent",
                         "basis_probe_exit_code": None if basis_proc is None else basis_proc.returncode,
                         "basis_probe_log_sha256": basis_log_sha,
                         "basis_probe_error_tail": bounded_error_tail(basis_proc),
                         "cert_path": cfg["cert"], "pcgs_basis_fingerprint": None,
                         "source_bundle_sha256": source_sha,
                         "source_files": {p.relative_to(ROOT).as_posix(): digest(p)
                                          for p in all_paths}})
            overall = False
            continue

        bindings = {
            "CLASS_ID": CLASS_ID, "RUN_ID": f"local-registered-{lane.lower()}",
            "RUN_ATTEMPT": "1", "COMMIT_SHA": commit,
            "SOURCE_BUNDLE_SHA256": source_sha, "WRAPPER_SHA256": digest(wrapper),
            "PREDICATE_SHA256": digest(predicate), "AUX_SHA256": aux_sha,
            "SCHEMA_SHA256": schema_sha,
            "PCGS_BASIS_FINGERPRINT": fingerprint,
            "PCGS_SOURCE_ARTIFACT_PATH": PCGS_SOURCE_REL,
            "PCGS_SOURCE_ARTIFACT_SHA256": digest(PCGS_SOURCE),
        }
        lines = ['RUN_MODE := "REGISTERED";;', f'OUT_CERT_PATH := "{cfg["cert"]}";;']
        lines += [f'{k} := "{v}";;' for k, v in bindings.items()]
        lines.append(f'Read("{cfg["wrapper"]}");')
        with tempfile.NamedTemporaryFile("w", suffix=f"_hsp7_{lane}.g", encoding="ascii", delete=False) as tmp:
            tmp.write("\n".join(lines) + "\n")
            tmp_path = Path(tmp.name)
        try:
            cert_path.unlink(missing_ok=True)
            proc = run_gap(tmp_path)
            log_bytes = (proc.stdout + "\n[stderr]\n" + proc.stderr).encode()
            log_sha = hashlib.sha256(log_bytes).hexdigest()
            ok = proc.returncode == 0 and cert_path.exists()
            error = None
            if ok:
                try:
                    certs[lane] = validate_cert(lane, cert_path, source_sha,
                                                bindings, fingerprint)
                except (ValueError, KeyError, json.JSONDecodeError) as exc:
                    ok = False
                    error = str(exc)
            else:
                error = f"gap exit={proc.returncode}, cert_exists={cert_path.exists()}"
            rows.append({"lane": lane, "exit_code": proc.returncode, "pass": ok,
                         "error": error, "log_sha256": log_sha,
                         "error_tail": None if ok else bounded_error_tail(proc),
                         "basis_probe_exit_code": basis_proc.returncode,
                         "basis_probe_log_sha256": basis_log_sha,
                         "basis_probe_error_tail": None,
                         "pcgs_basis_fingerprint": fingerprint,
                         "cert_path": cfg["cert"],
                         "cert_sha256": digest(cert_path) if cert_path.exists() else None,
                         "source_bundle_sha256": source_sha,
                         "source_files": {p.relative_to(ROOT).as_posix(): digest(p) for p in all_paths}})
            overall = overall and ok
        except subprocess.TimeoutExpired:
            rows.append({"lane": lane, "exit_code": None, "pass": False,
                         "error": "1800-second hard timeout", "cert_path": cfg["cert"]})
            overall = False
        finally:
            tmp_path.unlink(missing_ok=True)

    ## The frozen "18" calibration set is V's 13 named fixtures plus the
    ## p=5 control's five CONV-P/native fixtures.  This driver is read-only
    ## and prints the two-path counters; parse them fail-closed rather than
    ## substituting the p=7 production P fixtures for the p=5 control.
    p5_driver = ROOT / "search/probe/hsp7_mainrun/driver_conv_laneP_p5control_calib.g"
    p5_source_paths = [ROOT / p for p in P5_SOURCES]
    try:
        proc = run_gap(p5_driver)
        text = proc.stdout + "\n[stderr]\n" + proc.stderr
        parsed = {
            "connection_gate_mismatch": re.search(r"connection_gate_mismatch=(\d+)/7", text),
            "two_path_mismatch": re.search(r"two_path_mismatch=(\d+)/5", text),
            "pass_count": re.search(r"NWP7_pass_count=(\d+)/5", text),
            "done": "STAGE_FINAL_DONE" in text,
        }
        p5_ok = (proc.returncode == 0 and parsed["done"] and
                 parsed["connection_gate_mismatch"] is not None and parsed["connection_gate_mismatch"].group(1) == "0" and
                 parsed["two_path_mismatch"] is not None and parsed["two_path_mismatch"].group(1) == "0" and
                 parsed["pass_count"] is not None and parsed["pass_count"].group(1) == "5")
        rows.append({"lane": "P5", "exit_code": proc.returncode, "pass": p5_ok,
                     "error": None if p5_ok else "p5 connection/two-path/pass-count/done gate failed",
                     "log_sha256": hashlib.sha256(text.encode()).hexdigest(),
                     "driver_path": p5_driver.relative_to(ROOT).as_posix(),
                     "driver_sha256": digest(p5_driver),
                     "source_bundle_sha256": bundle_digest(p5_source_paths),
                     "source_files": {p.relative_to(ROOT).as_posix(): digest(p) for p in p5_source_paths}})
        comparisons["laneP5_CONV_native_5_equal"] = p5_ok
        overall = overall and p5_ok
    except subprocess.TimeoutExpired:
        rows.append({"lane": "P5", "exit_code": None, "pass": False,
                     "error": "1800-second hard timeout"})
        comparisons["laneP5_CONV_native_5_equal"] = False
        overall = False

    if "S" in certs and "V" in certs:
        sv_s = {r["fixture_id"]: r["verdict"] for r in certs["S"]["records"]}
        sv_v = {r["fixture_id"]: r["N"]["verdict"] for r in certs["V"]["records"]}
        expected = expected_fixture_verdicts()
        comparisons["laneS_laneV_13_equal"] = sv_s == sv_v
        comparisons["laneS_13_matches_registered"] = sv_s == expected
        comparisons["laneV_13_matches_registered"] = sv_v == expected
        comparisons["laneV_N_N0_all_equal"] = all(r["N_N0_agree"] for r in certs["V"]["records"])
    if "P" in certs:
        got_p = {r["fixture_id"]: r["pentagon_verdict"] for r in certs["P"]["records"]}
        expected_p = {"h4t0": True, **{f"h4t{t}": False for t in range(1, 7)}, "h3": False}
        comparisons["laneP_8_matches_registered"] = got_p == expected_p
    if "S" in certs and "P" in certs:
        comparisons["ordered_pcgs_core_S_P_equal"] = (
            certs["S"]["pcgs_basis_material"] == certs["P"]["pcgs_basis_material"])
    if "S" in certs and "V" in certs:
        comparisons["ordered_pcgs_core_S_V_equal"] = (
            certs["S"]["pcgs_basis_material"] ==
            core_material(certs["V"]["pcgs_basis_material"]))
    comparisons_ok = len(comparisons) == 8 and all(comparisons.values())
    overall = overall and comparisons_ok
    fingerprints = {lane: pcgs_basis_fingerprint(cert["pcgs_basis_material"])
                    for lane, cert in certs.items()}
    core_fingerprint = (pcgs_basis_fingerprint(certs["S"]["pcgs_basis_material"])
                        if "S" in certs else None)
    receipt = {
        "schema": "hsp7-registered-wrapper-preflight/v3",
        "class_id": CLASS_ID,
        "candidate_universe_contact": 0,
        "registered_fixture_plan": {"S": 13, "V": 13, "P_production": 8, "P5_two_path": 5},
        "actual_evaluated": {lane: len(cert.get("records", [])) for lane, cert in certs.items()},
        "pcgs_basis_contract": "hsp7-ordered-pcgs-material/v1",
        "pcgs_basis_fingerprints": fingerprints,
        "pcgs_core_fingerprint": core_fingerprint,
        "source_commit_sha": commit,
        "source_commit_files": commit_files,
        "orchestrator": {
            "path": ORCHESTRATOR_REL,
            "sha256": digest(ROOT / ORCHESTRATOR_REL),
            "validator_path": VALIDATOR_REL,
            "validator_sha256": digest(ROOT / VALIDATOR_REL),
            "gap_wrapper_path": GAP_WRAPPER_REL,
            "gap_wrapper_sha256": digest(ROOT / GAP_WRAPPER_REL),
        },
        "rows": rows,
        "comparisons": comparisons,
        "overall_pass": overall,
        "note": "Only named, previously registered fixtures were evaluated. SHARD mode was never invoked.",
    }
    AGG_OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
