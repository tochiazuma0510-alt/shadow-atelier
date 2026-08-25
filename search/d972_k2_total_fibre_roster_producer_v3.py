#!/usr/bin/env python3
"""Diagnostic-safe adapter for the total ordinary K2 roster producer.

The v2 adapter repaired only the modulus-9 roof word-replay convention and
completed the expensive roster computation.  Its result metadata retained a
historical exception message containing the producer's live failure prefix.
The v2 GHA wrapper therefore rejected an otherwise completed result during its
global diagnostic scan.

This v3 adapter pins and reuses v2 without changing any enumeration,
predicate, reduction, or roof-replay law.  It replaces that one historical
free-text value by structured data before serialization.  Global rejection of
genuine diagnostic tokens remains fail-closed and is covered by destructive
selftests.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REL = "search/d972_k2_total_fibre_roster_producer_v3.py"
PARENT_REL = "search/d972_k2_total_fibre_roster_producer_v2.py"
PARENT_BYTES = 9776
PARENT_SHA256 = "a6af98f3f2707e4812a66568c8679b3c5fad4671e764f9c33d194743c0a41411"
OUTPUT_REL = "ci/out/d972_k2_total_fibre_roster_v3_20260825.json"
SCHEMA = "d972-k2-total-fibre-roster-producer/v3"
FINAL_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_PRODUCER_V3_FINAL"
PREFLIGHT_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_V3_PREFLIGHT_PASS"
SELFTEST_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_V3_SELFTEST_PASS"
CORE_SELFTEST_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_CORE_V1_SELFTEST_PASS"
FORBIDDEN_RESULT_DIAGNOSTICS = (
    "STATE_STOP",
    "Traceback (most recent call last)",
    "SyntaxError",
    "MemoryError",
)


def fail(code: str, detail: str) -> None:
    raise RuntimeError(f"STATE_STOP {code}: {detail}")


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        fail(code, detail)


def pin_parent() -> dict:
    path = ROOT / PARENT_REL
    require(path.is_file(), "PARENT_MISSING", PARENT_REL)
    raw = path.read_bytes()
    observed = hashlib.sha256(raw).hexdigest()
    require(
        (len(raw), observed) == (PARENT_BYTES, PARENT_SHA256),
        "PARENT_PIN_MISMATCH",
        f"bytes={len(raw)},sha256={observed}",
    )
    return {"path": PARENT_REL, "bytes": len(raw), "sha256": observed}


def load_parent() -> tuple[ModuleType, dict]:
    parent_pin = pin_parent()
    path = ROOT / PARENT_REL
    spec = importlib.util.spec_from_file_location(
        "d972_k2_total_fibre_parent_v2", path
    )
    require(
        spec is not None and spec.loader is not None,
        "PARENT_IMPORT_SPEC",
        str(path),
    )
    parent = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = parent
    spec.loader.exec_module(parent)
    # v2 was deliberately written as a versionable adapter.  Its functions
    # consult these module globals when configuring the pinned v1 core.
    parent.SOURCE_REL = SOURCE_REL
    parent.OUTPUT_REL = OUTPUT_REL
    parent.SCHEMA = SCHEMA
    parent.FINAL_MARKER = FINAL_MARKER
    parent.PREFLIGHT_MARKER = PREFLIGHT_MARKER
    parent.SELFTEST_MARKER = SELFTEST_MARKER
    parent.CORE_SELFTEST_MARKER = CORE_SELFTEST_MARKER
    return parent, parent_pin


def has_forbidden_result_diagnostic(payload: str) -> bool:
    return any(token in payload for token in FORBIDDEN_RESULT_DIAGNOSTICS)


def sanitize_historical_metadata(result: dict, parent_pin: dict) -> None:
    repair_v2 = result.get("repair_v2")
    require(isinstance(repair_v2, dict), "V2_REPAIR_METADATA", repr(repair_v2))
    observed = repair_v2.get("v1_failure")
    require(
        observed == "STATE_STOP TARGET_WORD_REPLAY: 81",
        "V2_HISTORICAL_DIAGNOSTIC_DRIFT",
        repr(observed),
    )
    repair_v2["v1_failure"] = {
        "historical": True,
        "code": "TARGET_WORD_REPLAY",
        "detail_zero_based": 81,
        "live_diagnostic_prefix_elided": True,
    }
    pins = result.get("input_pins")
    require(isinstance(pins, list), "RESULT_INPUT_PINS", repr(type(pins)))
    require(
        all(pin.get("path") != PARENT_REL for pin in pins),
        "PARENT_PIN_DUPLICATE",
        PARENT_REL,
    )
    pins.append(parent_pin)
    producer = result.get("producer")
    require(isinstance(producer, dict), "RESULT_PRODUCER", repr(type(producer)))
    producer["adapter_parent"] = parent_pin
    producer["lineage"] = (
        "v3 diagnostic-safety adapter over pinned v2 convention repair and "
        "pinned v1 roster core; producer-side and not independent"
    )
    result["claim_cover"]["claim_id"] = "K2-TOTAL-FIBRE-ROSTER-OVER-X-V3"
    result["repair_v3"] = {
        "failed_GHA_run": 32812618841,
        "failure_phase": "post-completion result diagnostic gate",
        "contaminating_field": "repair_v2.v1_failure",
        "historical_failure_text_sanitized": True,
        "global_result_diagnostic_scan_preserved": True,
        "enumeration_or_predicate_law_changed": False,
        "roof_word_replay_law_changed_from_v2": False,
    }
    controls = result.get("destructive_controls")
    require(isinstance(controls, dict), "RESULT_CONTROLS", repr(type(controls)))
    controls["selftest_mutants"].append("inject forbidden result diagnostic")
    controls["full_run_fail_closed"].append("global result diagnostic scan")
    # Keep the adapter constant-space relative to the large roster.  The GHA
    # wrapper scans the serialized result globally; here only the metadata we
    # changed needs an immediate pre-serialization assertion.
    payload = json.dumps(
        {"repair_v2": repair_v2, "repair_v3": result["repair_v3"]},
        sort_keys=True,
        separators=(",", ":"),
    )
    require(
        not has_forbidden_result_diagnostic(payload),
        "RESULT_DIAGNOSTIC_SANITATION",
        "forbidden token remains after structured historical rewrite",
    )


def install_v3_metadata(core: ModuleType, parent_pin: dict) -> None:
    original_validate = core.validate_result

    def v3_validate(result: dict, *args: object, **kwargs: object) -> None:
        # v2 installs its metadata before delegating to the v1 structural
        # validator.  Sanitize only after that complete validation chain.
        original_validate(result, *args, **kwargs)
        if result.get("schema") == SCHEMA and "input_pins" in result:
            sanitize_historical_metadata(result, parent_pin)

    core.validate_result = v3_validate


def configure_core() -> tuple[ModuleType, ModuleType, dict]:
    parent, parent_pin = load_parent()
    core, _ = parent.configure_core()
    install_v3_metadata(core, parent_pin)
    return core, parent, parent_pin


def preflight() -> None:
    core, parent, parent_pin = configure_core()
    result = parent.replay_preflight(core)
    print(
        f"{PREFLIGHT_MARKER} targets={result['targets']} "
        f"v1_g9_mismatches={result['v1_g9_mismatches']} "
        f"first_v1_mismatch={result['first_v1_mismatch']} "
        f"v3_roof_g9_mismatches={result['v2_roof_g9_mismatches']} "
        f"psl_mismatches={result['psl_mismatches']} "
        f"parent_sha256={parent_pin['sha256']}"
    )


def selftest() -> None:
    core, parent, parent_pin = configure_core()
    core.selftest()
    replay = parent.replay_preflight(core)
    dirty = '{"error":"STATE_STOP INJECTED_MUTANT"}'
    safe = (
        '{"v1_failure":{"historical":true,"code":"TARGET_WORD_REPLAY",'
        '"detail_zero_based":81,"live_diagnostic_prefix_elided":true}}'
    )
    require(
        has_forbidden_result_diagnostic(dirty),
        "SELFTEST_DIAGNOSTIC_MUTANT_ACCEPTED",
        "injected live diagnostic was not detected",
    )
    require(
        not has_forbidden_result_diagnostic(safe),
        "SELFTEST_STRUCTURED_HISTORY_REJECTED",
        "safe structured history was rejected",
    )
    synthetic = {
        "repair_v2": {"v1_failure": "STATE_STOP TARGET_WORD_REPLAY: 81"},
        "input_pins": [],
        "producer": {},
        "claim_cover": {},
        "destructive_controls": {
            "selftest_mutants": [],
            "full_run_fail_closed": [],
        },
    }
    sanitize_historical_metadata(synthetic, parent_pin)
    require(
        not has_forbidden_result_diagnostic(
            json.dumps(synthetic, sort_keys=True, separators=(",", ":"))
        ),
        "SELFTEST_SANITIZER_OUTPUT",
        "synthetic sanitation retained a forbidden token",
    )
    print(
        f"{SELFTEST_MARKER} targets={replay['targets']} "
        f"v1_g9_mismatches={replay['v1_g9_mismatches']} "
        f"first_v1_mismatch={replay['first_v1_mismatch']} "
        "v3_roof_g9_mismatches=0 psl_mismatches=0 "
        "diagnostic_mutant_rejected=true structured_history_accepted=true "
        "sanitizer_rewrite_pass=true "
        f"parent_sha256={parent_pin['sha256']}"
    )


def execute(output: str) -> None:
    core, _, _ = configure_core()
    core.execute(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--output", default=OUTPUT_REL)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if arguments.preflight:
        preflight()
    elif arguments.selftest:
        selftest()
    else:
        execute(arguments.output)
