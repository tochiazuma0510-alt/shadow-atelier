#!/usr/bin/env python3
"""DMTCP-resumable front end for the exact D972 dovetail producer.

Version 1 deliberately refused to certify its finite-extension engine because
GAP's MTC/fp-order and full 972-fibre scan did not expose serializable inner
cursors.  Version 2 keeps the reviewed v1 mathematics and state transitions,
but runs the *whole* Python/GAP process tree under DMTCP.  The external
workflow is the only clock: this module never applies a wall-clock timeout to
an in-flight GAP cell.  A DMTCP image therefore contains the Python cursor,
the current GAP/ACE process and all opaque algorithm state at one generation.

The ordinary CLI is intentionally identical to v1.  The workflow additionally
sets D972_DMTCP_ENABLED=1 and D972_DMTCP_CONTRACT_SHA256 to the frozen contract
digest in d972_dovetail_manifest_v2.json.  Direct, uncheckpointed campaign runs
fail closed.  ``--campaign-driver`` keeps the producer/checker pair in this
same checkpointed process alive until a terminal state or the external DMTCP
supervisor's checkpoint-kill; it never adds a per-cell wall-clock timeout.
``--self-test`` checks the wrapper without invoking GAP.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
LEGACY_PATH = ROOT / "search" / "d972_dovetail_producer_v1.py"
WORKER_V2 = ROOT / "search" / "d972_dovetail_worker_v2.g"
CHECKER_V2 = ROOT / "search" / "check_d972_dovetail_v2.py"
MANIFEST_V2 = ROOT / "search" / "d972_dovetail_manifest_v2.json"
ENVELOPE_SCHEMA_V2 = ROOT / "search" / "d972_dovetail_state_schema_v2.json"
WORKFLOW_V2 = ROOT / ".github" / "workflows" / "d972-dovetail-v2.yml"
SEMANTIC_M_CHECKER = ROOT / "search" / "check_d972_semantic_m_v1.py"
SEMANTIC_M_MANIFEST = ROOT / "search" / "d972_semantic_m_manifest_v1.json"

LEGACY_SEED_WORKFLOW_REBIND_SPEC = {
    "version": "d972-legacy-seed-workflow-rebind/v1",
    "scope": "fresh-genesis-seed-only",
    "precondition": {
        "path": ".github/workflows/d972-dovetail.yml",
        "required": True,
        "sha256": None,
    },
    "replacement": {
        "path": ".github/workflows/d972-dovetail-v2.yml",
        "required": True,
    },
    "existing_checkpoint_migration": False,
    "fail_closed_on_precondition_drift": True,
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def worker_authority_material(receipt: dict[str, Any]) -> str:
    compact = lambda value: json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    boolean = lambda value: "true" if value is True else "false"
    dmtcp = receipt["dmtcp"]
    parts = [
        ("schema", receipt["schema"]), ("mode", receipt["mode"]),
        ("status", receipt["status"]), ("universe_id", receipt["universe_id"]),
        ("input_digest", receipt["input_digest"]), ("task_digest", receipt["task_digest"]),
        ("payload_sha256", receipt["payload_sha256"]),
        ("cursor_before", compact(receipt["cursor_before"])),
        ("cursor_after", compact(receipt["cursor_after"])),
        ("radices", compact(receipt["radices"])),
        ("completed_range", compact(receipt["completed_range"])),
        ("cell_complete", boolean(receipt["cell_complete"])),
        ("classification_complete", boolean(receipt["classification_complete"])),
        ("outer_advance_authorized", boolean(receipt["outer_advance_authorized"])),
        ("exhausted", boolean(receipt["exhausted"])),
        ("h_exhausted", boolean(receipt["h_exhausted"])),
        ("terminal_A_eligible", boolean(receipt["terminal_A_eligible"])),
        ("workflow_resumable", boolean(receipt["workflow_resumable"])),
        ("dmtcp_contract_sha256", dmtcp["contract_sha256"]),
        ("dmtcp_generation", str(dmtcp["generation"])),
    ]
    return "|".join(f"{key}={value}" for key, value in parts)


def authority_material_diagnostic(
    receipt: dict[str, Any], material: str | None = None,
) -> str:
    """Return a non-authoritative, secret-free digest mismatch diagnostic.

    The GAP worker publishes the exact material it hashed only as a debugging
    aid.  The producer still rebuilds the material independently and refuses
    the envelope on either mismatch.  The material contains only schema,
    cursors, booleans, and digests; it never contains payload/task contents.
    """
    if material is None:
        material = worker_authority_material(receipt)
    claimed = receipt.get("checkpoint_sha256")
    observed = sha_bytes(material.encode("utf-8"))
    worker_material = receipt.get("authority_material_diagnostic")
    return (
        "claimed=" + repr(claimed) +
        " observed=" + observed +
        " python_material=" + repr(material) +
        " worker_material=" + repr(worker_material)
    )


def load_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_V2.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"DMTCP_CONTRACT_STOP manifest unreadable: {exc}") from exc
    contract = manifest.get("dmtcp_contract")
    if not isinstance(contract, dict):
        raise RuntimeError("DMTCP_CONTRACT_STOP dmtcp_contract absent")
    body = copy.deepcopy(contract)
    claimed = body.pop("contract_sha256", None)
    observed = sha_bytes(canonical_bytes(body))
    if claimed != observed:
        raise RuntimeError("DMTCP_CONTRACT_STOP contract digest mismatch")
    return manifest


def v2_code_receipt(manifest: dict[str, Any]) -> dict[str, Any]:
    rebind_spec = manifest["dmtcp_contract"].get("legacy_seed_workflow_rebind")
    if rebind_spec != LEGACY_SEED_WORKFLOW_REBIND_SPEC:
        raise RuntimeError("DMTCP_CONTRACT_STOP legacy seed workflow rebind drift")
    paths = {
        "producer_v2": Path(__file__).resolve(),
        "checker_v2": CHECKER_V2,
        "worker_v2": WORKER_V2,
        "workflow_v2": WORKFLOW_V2,
        "manifest_v2": MANIFEST_V2,
        "resume_envelope_schema_v2": ENVELOPE_SCHEMA_V2,
        "producer_v1_library": LEGACY_PATH,
        "checker_v1_library": ROOT / "search" / "check_d972_dovetail_v1.py",
        "worker_v1_library": ROOT / "search" / "d972_dovetail_worker_v1.g",
        "calibration_paper_premise": ROOT / "sol" / "sol_reply_143_typedfiber.md",
        "semantic_m_checker_v1": SEMANTIC_M_CHECKER,
        "semantic_m_manifest_v1": SEMANTIC_M_MANIFEST,
    }
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        raise RuntimeError("DMTCP_CONTRACT_STOP missing code: " + ",".join(missing))
    bindings = {
        name: {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha_file(path),
        }
        for name, path in paths.items()
    }
    binding_material = "".join(
        f"{row['path']}={row['sha256']}\n"
        for row in sorted(bindings.values(), key=lambda item: item["path"])
    ).encode("utf-8")
    return {
        "schema": "d972-dovetail-runtime-integrity/v2",
        "dmtcp_contract_sha256": manifest["dmtcp_contract"]["contract_sha256"],
        "bindings": bindings,
        "binding_set_sha256": sha_bytes(binding_material),
        "timeout_policy": "no subprocess wall timeout; external DMTCP supervisor only",
        "whole_process_tree_required": True,
        "legacy_seed_workflow_rebind": copy.deepcopy(rebind_spec),
    }


def require_dmtcp_contract(manifest: dict[str, Any]) -> None:
    if os.environ.get("D972_DMTCP_ENABLED") != "1":
        raise RuntimeError(
            "DMTCP_CONTRACT_STOP campaign producer must run under the v2 supervisor"
        )
    expected = manifest["dmtcp_contract"]["contract_sha256"]
    if os.environ.get("D972_DMTCP_CONTRACT_SHA256") != expected:
        raise RuntimeError("DMTCP_CONTRACT_STOP supervisor contract digest mismatch")
    # This token is injected only by dmtcp_launch/dmtcp_restart in the workflow.
    # The coordinator variables alone are not proof of a live coordinator, but
    # requiring them catches accidental direct invocation; the sealed external
    # envelope supplies the cryptographic/process evidence on resume.
    if not os.environ.get("DMTCP_COORD_HOST") or not os.environ.get("DMTCP_COORD_PORT"):
        raise RuntimeError("DMTCP_CONTRACT_STOP coordinator environment absent")


def unwrap_worker_envelope(
    raw_envelope: str, *, mode: str, manifest: dict[str, Any],
    task_digest: str, generation: str, expected_cursor: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Validate the v2 transport wrapper before exposing its v1 payload."""
    envelope = json.loads(raw_envelope)
    contract_sha = manifest["dmtcp_contract"]["contract_sha256"]
    if not (
        isinstance(envelope, dict)
        and envelope.get("schema") == "d972_dovetail_worker/v2"
        and envelope.get("mode") == mode
        and envelope.get("workflow_resumable") is True
        and envelope.get("universe_id") == manifest["universe_id"]
        and envelope.get("input_digest") == manifest["search_input_set_sha256"]
        and envelope.get("task_digest") == task_digest
        and envelope.get("dmtcp", {}).get("enabled") is True
        and envelope.get("dmtcp", {}).get("contract_ready") is True
        and envelope.get("dmtcp", {}).get("contract_sha256") == contract_sha
        and str(envelope.get("dmtcp", {}).get("generation")) == generation
        and isinstance(envelope.get("payload"), dict)
    ):
        raise ValueError("malformed/unbound v2 envelope")
    marker = ',"payload":'
    marker_pos = raw_envelope.rfind(marker)
    if marker_pos < 0 or not raw_envelope.endswith("}"):
        raise ValueError("v2 payload boundary absent")
    payload_text = raw_envelope[marker_pos + len(marker):-1]
    if envelope.get("payload_sha256") != sha_bytes(payload_text.encode("utf-8")):
        raise ValueError("v2 payload digest mismatch")
    material = worker_authority_material(envelope)
    worker_material = envelope.get("authority_material_diagnostic")
    if not isinstance(worker_material, str):
        raise ValueError(
            "v2 checkpoint authority material diagnostic absent: " +
            authority_material_diagnostic(envelope, material)
        )
    if worker_material != material or envelope.get("checkpoint_sha256") != sha_bytes(
        material.encode("utf-8")
    ):
        raise ValueError(
            "v2 checkpoint receipt digest mismatch: " +
            authority_material_diagnostic(envelope, material)
        )
    boolean_fields = (
        "cell_complete", "classification_complete", "outer_advance_authorized",
        "exhausted", "h_exhausted", "terminal_A_eligible", "workflow_resumable",
    )
    if not (all(isinstance(envelope.get(key), bool) for key in boolean_fields) and
            (envelope.get("radices") is None or isinstance(envelope.get("radices"), dict)) and
            isinstance(envelope.get("completed_range"), dict) and
            all(envelope.get(key) is None or isinstance(envelope.get(key), dict)
                for key in ("cursor_before", "cursor_after"))):
        raise ValueError("v2 authority-field types")
    payload = envelope["payload"]
    if not (payload.get("schema") == "d972_dovetail_worker/v1" and
            payload.get("mode") == mode):
        raise ValueError("v2/v1 payload schema-mode mismatch")
    if mode == "selftest":
        # The frozen v1 selftest predates the status field.  Permit only that
        # exact legacy shape; production modes retain strict status equality.
        expected_selftest_keys = {
            "schema", "mode", "table_group", "canonical", "aut_count",
            "split", "nonsplit", "shadow_formula_toy", "target_identity_key",
            "target_serializer_pass", "relative_extension_completeness_receipt",
            "all_pass",
        }
        if ("status" in payload or envelope.get("status") != "PASS" or
                payload.get("all_pass") is not True or
                set(payload) != expected_selftest_keys):
            raise ValueError("v2/v1 legacy selftest payload shape mismatch")
    elif payload.get("status") != envelope.get("status"):
        raise ValueError("v2/v1 payload schema-mode-status mismatch")
    if (envelope.get("outer_cursor_before") != envelope.get("cursor_before") or
            envelope.get("outer_cursor_after") != envelope.get("cursor_after")):
        raise ValueError("v2 duplicate cursor fields disagree")
    if expected_cursor is not None and envelope.get("cursor_before") != expected_cursor:
        raise ValueError("v2 worker cursor is not the task/current producer cursor")
    if envelope.get("cell_complete") is not True:
        raise ValueError("completed worker process lacks cell-complete receipt")
    terminal_a = payload.get("campaign_stop_first_empty_fiber") is True
    if envelope.get("terminal_A_eligible") is not terminal_a:
        raise ValueError("v2 terminal-A flag/payload mismatch")
    if terminal_a and not (
        mode == "shadow-fiber" and envelope.get("classification_complete") is True
        and envelope.get("outer_advance_authorized") is True
    ):
        raise ValueError("v2 terminal-A eligibility precedes complete shadow classification")
    if mode in {"candidate", "shadow-fiber"}:
        radices = envelope.get("radices")
        if not (isinstance(radices, dict) and
                all(isinstance(radices.get(key), int) and radices[key] > 0 for key in (
                    "automorphism_count", "automorphism_pair_count", "defect_count",
                    "extension_class_count", "marked_orbit_count",
                ))):
            raise ValueError("v2 finite-cell radices absent")
    if mode == "candidate":
        if payload.get("cursor") != expected_cursor:
            raise ValueError("v1 candidate cursor/task mismatch")
        accepted = payload.get("accepted_count") == 1
        if accepted:
            if not (envelope.get("classification_complete") is False and
                    envelope.get("outer_advance_authorized") is False and
                    envelope.get("cursor_after") == envelope.get("cursor_before")):
                raise ValueError("accepted candidate advanced before shadow classification")
        elif not (payload.get("accepted_count") == 0 and
                  envelope.get("classification_complete") is True and
                  envelope.get("outer_advance_authorized") is True and
                  envelope.get("cursor_after") == payload.get("next_cursor")):
            raise ValueError("rejected candidate completion/cursor mismatch")
    elif mode == "shadow-fiber" and not (
        envelope.get("classification_complete") is True and
        envelope.get("outer_advance_authorized") is True
    ):
        raise ValueError("shadow-fiber receipt did not authorize completed classification")
    result = copy.deepcopy(envelope["payload"])
    result["relative_extension_completeness_receipt"] = copy.deepcopy(
        envelope["relative_extension_completeness_receipt"]
    )
    result["v2_process_checkpoint_receipt"] = {
        key: copy.deepcopy(value) for key, value in envelope.items() if key != "payload"
    }
    return result


def load_legacy() -> Any:
    spec = importlib.util.spec_from_file_location("d972_dovetail_producer_v1_lib", LEGACY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("DMTCP_CONTRACT_STOP cannot load v1 producer library")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install_v2_adapter(legacy: Any, manifest: dict[str, Any]) -> None:
    """Patch only orchestration hooks; all mathematical routines stay v1."""
    runtime_receipt = v2_code_receipt(manifest)
    legacy.WORKER = WORKER_V2

    original_initial_state = legacy.initial_state
    original_transition = legacy.transition
    original_validate_state = legacy.validate_state
    original_bind_seed_integrity = legacy._bind_seed_integrity

    def bind_fresh_seed_to_v2_workflow(state: dict[str, Any]) -> None:
        """Replace the deleted v1 supervisor only on an unbound genesis seed."""
        spec = manifest["dmtcp_contract"].get("legacy_seed_workflow_rebind")
        if spec != LEGACY_SEED_WORKFLOW_REBIND_SPEC:
            raise legacy.StateStop("STATE_STOP legacy seed workflow rebind contract drift")
        try:
            integrity = state["integrity"]
            row = integrity["code"]["workflow"]
        except (KeyError, TypeError) as exc:
            raise legacy.StateStop(
                "STATE_STOP legacy seed workflow binding row absent"
            ) from exc
        if (state.get("schema_version") != "d972-dovetail-state/v1" or
                integrity.get("ready") is not False or
                row != spec["precondition"]):
            raise legacy.StateStop(
                "STATE_STOP legacy seed workflow rebind precondition drift"
            )
        if not WORKFLOW_V2.is_file():
            raise legacy.StateStop("STATE_STOP v2 supervisor workflow absent")
        row["path"] = spec["replacement"]["path"]
        original_bind_seed_integrity(state)
        expected = {
            "path": spec["replacement"]["path"],
            "required": spec["replacement"]["required"],
            "sha256": sha_file(WORKFLOW_V2),
        }
        if row != expected:
            raise legacy.StateStop("STATE_STOP v2 supervisor workflow bind drift")

    def current_run_metadata() -> dict[str, Any]:
        path = ROOT / ".d972-runtime" / "current-run.json"
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise legacy.StateStop(f"STATE_STOP current-run metadata unreadable: {exc}") from exc
        required = {
            "run_id", "run_attempt", "event", "commit_sha", "created_at_utc",
            "resume_run_id",
        }
        if set(row) != required:
            raise legacy.StateStop("STATE_STOP current-run metadata fields")
        if not (isinstance(row["run_id"], str) and row["run_id"].isdigit() and
                isinstance(row["run_attempt"], int) and row["run_attempt"] >= 1 and
                row["event"] in {"workflow_dispatch", "schedule"} and
                isinstance(row["commit_sha"], str) and len(row["commit_sha"]) == 40 and
                all(ch in "0123456789abcdef" for ch in row["commit_sha"]) and
                (row["resume_run_id"] is None or
                 (isinstance(row["resume_run_id"], str) and row["resume_run_id"].isdigit()))):
            raise legacy.StateStop("STATE_STOP malformed current-run metadata")
        return row

    def bind_receipt(state: dict[str, Any]) -> None:
        receipts = state.setdefault("receipts", {})
        receipts["v2_runtime_integrity"] = copy.deepcopy(runtime_receipt)

    def initial_state(*args: Any, **kwargs: Any) -> dict[str, Any]:
        state = original_initial_state(*args, **kwargs)
        bind_receipt(state)
        state["hash_chain"]["checkpoint_sha256"] = "0" * 64
        state["hash_chain"]["checkpoint_sha256"] = legacy.state_hash(state)
        return state

    def transition(old: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
        patched = copy.deepcopy(updates)
        receipts = copy.deepcopy(patched.get("receipts", old.get("receipts", {})))
        receipts["v2_runtime_integrity"] = copy.deepcopy(runtime_receipt)
        patched["receipts"] = receipts
        return original_transition(old, patched)

    def validate_state(state: dict[str, Any], *, bind_current: bool = True) -> None:
        original_validate_state(state, bind_current=bind_current)
        if bind_current and state.get("receipts", {}).get("v2_runtime_integrity") != runtime_receipt:
            raise legacy.StateStop("STATE_STOP v2 runtime/code binding drift")

    original_next_fallback_table = legacy.next_fallback_table

    def next_fallback_table_without_deadline(
        k: int, start: int, deadline: float,
    ) -> tuple[int, list[list[int]] | None, bool]:
        # The legacy fallback accepts a deadline to support its standalone
        # finite-slice CLI.  Under DMTCP that would be an unauthorized inner
        # clock: let the external supervisor interrupt the exact loop instead.
        del deadline
        return original_next_fallback_table(k, start, float("inf"))

    def run_worker_without_timeout(
        mode: str, out_path: Path, env_extra: dict[str, str], timeout: float
    ) -> dict[str, Any]:
        """Run inherited worker modes with no downtime-sensitive deadline."""
        del timeout
        env = os.environ.copy()
        env.update({
            "D972_WORKER_MODE": mode,
            "D972_WORKER_OUTPUT": str(out_path.resolve()),
            "D972_MODE": mode,
            "D972_OUT": str(out_path.resolve()),
            "D972_DMTCP_ENABLED": "1",
            "D972_DMTCP_CONTRACT_SHA256": manifest["dmtcp_contract"]["contract_sha256"],
            "D972_DMTCP_VERSION": os.environ.get("D972_DMTCP_VERSION", "unbound"),
            "D972_DMTCP_GENERATION": os.environ.get("D972_DMTCP_GENERATION", "0"),
            "D972_UNIVERSE_ID": manifest["universe_id"],
            "D972_INPUT_DIGEST": manifest["search_input_set_sha256"],
            "D972_HEARTBEAT": str((out_path.parent / "worker-heartbeat.json").resolve()),
        })
        env.update(env_extra)
        task_path_raw = env.get("D972_TASK_G") or env.get("D972_TASK")
        task_digest = "unbound"
        expected_cursor: dict[str, int] | None = None
        if task_path_raw:
            task_path = Path(task_path_raw)
            if not task_path.is_file():
                raise legacy.StateStop("WORKER_STOP v2 task path absent")
            task_digest = sha_file(task_path)
            env["D972_TASK_DIGEST"] = task_digest
            task_text = task_path.read_text(encoding="ascii")
            cursor_fields = {}
            for name in ("aut_pair_index", "defect_index", "lift_pair_index"):
                match = re.search(rf"\b{name}\s*:=\s*([0-9]+)", task_text)
                if match is not None:
                    cursor_fields[name] = int(match.group(1))
            if len(cursor_fields) == 3:
                expected_cursor = cursor_fields
        gap = shutil.which("gap")
        if os.name == "nt" or gap is None:
            raise legacy.StateStop("WORKER_STOP v2 campaign requires POSIX GAP under DMTCP")
        command = [gap, "-q", "--quitonbreak", str(WORKER_V2.resolve())]
        started = time.monotonic()
        completed = subprocess.run(
            command, cwd=ROOT, env=env, text=True, encoding="utf-8",
            errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False,
        )
        if completed.stderr:
            legacy.WORKER_STDERR.append(f"[{mode}]\n{completed.stderr}")
        elapsed = time.monotonic() - started
        if completed.returncode != 0 or not out_path.is_file():
            raise legacy.StateStop(
                f"WORKER_STOP mode={mode} exit={completed.returncode} "
                f"stdout={completed.stdout[-2000:]!r} stderr={completed.stderr[-2000:]!r}"
            )
        raw_envelope = out_path.read_text(encoding="utf-8").strip()
        try:
            result = unwrap_worker_envelope(
                raw_envelope, mode=mode, manifest=manifest, task_digest=task_digest,
                generation=os.environ.get("D972_DMTCP_GENERATION", "0"),
                expected_cursor=expected_cursor,
            )
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise legacy.StateStop(f"WORKER_STOP {exc}") from exc
        result["subprocess_receipt"] = {
            "exit_code": completed.returncode,
            # This duration may include powered-off time after restore.  It is
            # diagnostic only and never has cursor or theorem authority.
            "wall_seconds_diagnostic": round(elapsed, 6),
            "timeout_applied": False,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
        }
        return result

    legacy.initial_state = initial_state
    legacy.transition = transition
    legacy.validate_state = validate_state
    legacy._bind_seed_integrity = bind_fresh_seed_to_v2_workflow
    legacy.run_worker = run_worker_without_timeout
    legacy.next_fallback_table = next_fallback_table_without_deadline
    legacy._current_run_metadata = current_run_metadata


def self_test() -> int:
    manifest = load_manifest()
    rewrites = manifest["dmtcp_contract"]["gap_4_12_materialized_rewrites"]
    base_rewrites = rewrites.get("base_permutation_groups", {})
    list_rewrites = rewrites.get("table_group", {})
    outer_rewrites = rewrites.get("outer_bucket_inner", {})
    parent_rewrites = rewrites.get("exact_parent_subgroups", {})
    if (rewrites.get("replacement_count_total") != 34 or
            base_rewrites.get("replacement_count") != 17 or
            list_rewrites.get("replacement_count") != 1 or
            outer_rewrites.get("replacement_count") != 1 or
            parent_rewrites.get("replacement_count") != 11 or
            parent_rewrites.get("fail_closed_on_count_drift") is not True or
            list_rewrites.get("needle") != "G := Group(perms);" or
            list_rewrites.get("replacement") !=
            "G := D972V2PermutationGroup(perms,n,\"table_group\");" or
            outer_rewrites.get("needle") != "I := Group(innerPerms);" or
            outer_rewrites.get("replacement") !=
            "I := D972V2PermutationGroup(innerPerms,k,\"outer_bucket_inner\");" or
            base_rewrites.get("helper") !=
            "D972V2PermutationGroup(generators, degree, stage) -> "
            "Subgroup(SymmetricGroup(degree), PermList images)" or
            base_rewrites.get("fail_closed_on_count_drift") is not True):
        raise RuntimeError("self-test GAP4.12 base permutation rewrite contract drift")
    receipt = v2_code_receipt(manifest)
    if receipt["whole_process_tree_required"] is not True:
        raise RuntimeError("self-test invariant failed")
    legacy = load_legacy()
    install_v2_adapter(legacy, manifest)
    seed_fixture = json.loads(
        (ROOT / manifest["mathematical_state"]["seed_manifest"]).read_text(
            encoding="utf-8"
        )
    )
    legacy._bind_seed_integrity(seed_fixture)
    workflow_row = seed_fixture["integrity"]["code"]["workflow"]
    if workflow_row != {
        "path": ".github/workflows/d972-dovetail-v2.yml",
        "required": True,
        "sha256": sha_file(WORKFLOW_V2),
    }:
        raise RuntimeError("self-test legacy seed workflow rebind failed")
    negative_fixture = json.loads(
        (ROOT / manifest["mathematical_state"]["seed_manifest"]).read_text(
            encoding="utf-8"
        )
    )
    negative_fixture["integrity"]["code"]["workflow"]["required"] = False
    try:
        legacy._bind_seed_integrity(negative_fixture)
    except legacy.StateStop as exc:
        if "rebind precondition drift" not in str(exc):
            raise RuntimeError(
                f"self-test workflow rebind negative-canary drifted: {exc}"
            ) from exc
    else:
        raise RuntimeError("self-test workflow rebind accepted a nonfrozen seed")
    payload_text = '{"schema":"d972_dovetail_worker/v1","mode":"candidate","status":"PASS","cursor":{"aut_pair_index":0,"defect_index":0,"lift_pair_index":0},"next_cursor":{"aut_pair_index":0,"defect_index":0,"lift_pair_index":1},"accepted_count":1,"candidates":[{"synthetic":true}]}'
    payload_sha = sha_bytes(payload_text.encode("utf-8"))
    cursor = {"aut_pair_index": 0, "defect_index": 0, "lift_pair_index": 0}
    contract = manifest["dmtcp_contract"]["contract_sha256"]
    task_digest = "1" * 64
    completeness = {
        "workflow_resumable": True, "worker_alone_resume_authority": False,
        "heartbeat_authoritative": False,
        "finite_cap_or_nontermination_is_terminal_B": False,
        "dmtcp_contract_sha256": contract,
    }
    prefix = {
        "schema": "d972_dovetail_worker/v2", "mode": "candidate", "status": "PASS",
        "universe_id": manifest["universe_id"],
        "input_digest": manifest["search_input_set_sha256"], "task_digest": task_digest,
        "payload_sha256": payload_sha, "cursor_before": cursor, "cursor_after": cursor,
        "outer_cursor_before": cursor, "outer_cursor_after": cursor,
        "radices": {"automorphism_count": 1, "automorphism_pair_count": 1,
                    "defect_count": 1, "extension_class_count": 1,
                    "marked_orbit_count": 2},
        "cell_complete": True, "classification_complete": False,
        "outer_advance_authorized": False, "terminal_A_eligible": False,
        "exhausted": False, "h_exhausted": False,
        "workflow_resumable": True,
        "dmtcp": {"enabled": True, "contract_ready": True, "version": "fixture",
                  "generation": "7", "contract_sha256": contract},
        "completed_range": {"relative_extension_complete": True,
                            "shadow_classification_complete": False,
                            "stage": "marked_orbit", "start": cursor, "stop": cursor},
        "relative_extension_completeness_receipt": completeness,
    }
    prefix["authority_material_diagnostic"] = worker_authority_material(prefix)
    prefix["checkpoint_sha256"] = sha_bytes(
        prefix["authority_material_diagnostic"].encode("utf-8")
    )
    synthetic_raw = json.dumps(prefix, separators=(",", ":"))[:-1] + ',"payload":' + payload_text + "}"
    unwrapped = unwrap_worker_envelope(
        synthetic_raw, mode="candidate", manifest=manifest,
        task_digest=task_digest, generation="7", expected_cursor=cursor,
    )
    if unwrapped.get("accepted_count") != 1 or len(unwrapped.get("candidates", [])) != 1:
        raise RuntimeError("self-test accepted payload was lost during v2 unwrap")
    tampered_material = copy.deepcopy(prefix)
    tampered_material["authority_material_diagnostic"] += "|tampered"
    tampered_raw = (
        json.dumps(tampered_material, separators=(",", ":"))[:-1] +
        ',"payload":' + payload_text + "}"
    )
    try:
        unwrap_worker_envelope(
            tampered_raw, mode="candidate", manifest=manifest,
            task_digest=task_digest, generation="7", expected_cursor=cursor,
        )
    except ValueError as exc:
        if not all(token in str(exc) for token in (
            "python_material=", "worker_material=", "claimed=", "observed=",
        )):
            raise RuntimeError(f"authority-material diagnostic drifted: {exc}") from exc
    else:
        raise RuntimeError("tampered authority material was accepted")
    missing_status_payload = json.loads(payload_text)
    missing_status_payload.pop("status", None)
    missing_status_text = json.dumps(missing_status_payload, separators=(",", ":"))
    missing_status = copy.deepcopy(prefix)
    missing_status["payload_sha256"] = sha_bytes(missing_status_text.encode("utf-8"))
    missing_status["checkpoint_sha256"] = sha_bytes(
        worker_authority_material(missing_status).encode("utf-8")
    )
    missing_status["authority_material_diagnostic"] = worker_authority_material(
        missing_status
    )
    missing_status_raw = (
        json.dumps(missing_status, separators=(",", ":"))[:-1] +
        ',"payload":' + missing_status_text + "}"
    )
    try:
        unwrap_worker_envelope(
            missing_status_raw, mode="candidate", manifest=manifest,
            task_digest=task_digest, generation="7", expected_cursor=cursor,
        )
    except ValueError as exc:
        if "schema-mode-status mismatch" not in str(exc):
            raise RuntimeError(f"candidate missing-status gate drifted: {exc}") from exc
    else:
        raise RuntimeError("candidate payload without status was accepted")
    taskless_payload_text = (
        '{"schema":"d972_dovetail_worker/v1","mode":"selftest",'
        '"table_group":true,"canonical":true,"aut_count":1,'
        '"split":{"h_embeds":true,"order":4,"marked_generates":false},'
        '"nonsplit":{"h_embeds":true,"order":4,"marked_generates":true},'
        '"shadow_formula_toy":{"n_ord":2,"derived_order":1,'
        '"full_hexagon_count":2,"shadow_count":2,"settled_count":2},'
        '"target_identity_key":"(0;0,0,0,0,0,0;1,2,3,4,5,6,7,8,9)",'
        '"target_serializer_pass":true,'
        '"relative_extension_completeness_receipt":{},"all_pass":true}'
    )
    taskless = copy.deepcopy(prefix)
    taskless.update({
        "mode": "selftest", "task_digest": "unbound",
        "payload_sha256": sha_bytes(taskless_payload_text.encode("utf-8")),
        "cursor_before": None, "cursor_after": None,
        "outer_cursor_before": None, "outer_cursor_after": None,
        "radices": None, "classification_complete": True,
        "outer_advance_authorized": True,
        "completed_range": {"complete": True, "stage": "selftest"},
    })
    taskless["authority_material_diagnostic"] = worker_authority_material(taskless)
    taskless["checkpoint_sha256"] = sha_bytes(
        taskless["authority_material_diagnostic"].encode("utf-8")
    )
    taskless_raw = (
        json.dumps(taskless, separators=(",", ":"))[:-1] +
        ',"payload":' + taskless_payload_text + "}"
    )
    taskless_unwrapped = unwrap_worker_envelope(
        taskless_raw, mode="selftest", manifest=manifest,
        task_digest="unbound", generation="7",
    )
    if taskless_unwrapped.get("all_pass") is not True:
        raise RuntimeError("self-test taskless/null-radices payload was lost")
    campaign_fixture = [
        None,
        {"status": {"code": "CALIBRATION_PENDING", "terminal": False}},
        {"status": {"code": "UNKNOWN/RESUME", "terminal": False}},
        {"status": {"code": "CHECKER_PENDING", "terminal": False}},
        {"status": {"code": "CONTINUE", "terminal": False}},
        {"status": {"code": "A_WITNESS_CROSSCHECKED", "terminal": True}},
    ]
    expected_phases = [
        "producer", "checker", "producer", "checker", "producer", "terminal",
    ]
    observed_phases = [campaign_phase(state) for state in campaign_fixture]
    if observed_phases != expected_phases:
        raise RuntimeError(
            f"campaign loop fixture drift: {observed_phases!r} != {expected_phases!r}"
        )
    print(json.dumps({
        "schema": "d972-dovetail-producer-selftest/v2",
        "status": "PASS",
        "contract_sha256": manifest["dmtcp_contract"]["contract_sha256"],
        "binding_set_sha256": receipt["binding_set_sha256"],
        "no_internal_worker_timeout": True,
        "synthetic_accepted_payload_unwrap": True,
        "taskless_null_radices_unwrap": True,
        "campaign_loop_fixture": "PASS",
        "legacy_seed_workflow_rebind": "PASS",
    }, sort_keys=True))
    return 0


CAMPAIGN_CHECKER_PENDING = frozenset({"CALIBRATION_PENDING", "CHECKER_PENDING"})
CAMPAIGN_PRODUCER_PHASE = frozenset({"INITIALIZED", "UNKNOWN/RESUME", "CONTINUE"})


def campaign_phase(state: dict[str, Any] | None) -> str:
    """Select the only legal next phase, including the fresh-launch phase."""
    if state is None:
        return "producer"
    status = state.get("status", {})
    if status.get("terminal"):
        return "terminal"
    code = status.get("code")
    if code in CAMPAIGN_CHECKER_PENDING:
        return "checker"
    if code in CAMPAIGN_PRODUCER_PHASE:
        return "producer"
    raise RuntimeError(f"STATE_STOP campaign status unexpected: {code!r}")


def campaign_driver(argv: Sequence[str]) -> int:
    """Run producer/checker iterations in one checkpointed process tree."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--checker-out-dir", type=Path, required=True)
    parser.add_argument("--slice-seconds", type=int, default=300)
    args = parser.parse_args(argv)
    producer_argv = [
        "--state", str(args.state), "--out-dir", str(args.out_dir),
        "--slice-seconds", str(args.slice_seconds),
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    producer_ledger = args.out_dir / "producer-ledger.jsonl"
    producer_ledger.touch(exist_ok=True)
    os.environ["D972_CHECKER_DMTCP_ENABLED"] = "1"
    os.environ["D972_DMTCP_PHASE_COMPLETE"] = "1"
    os.environ["D972_PENDING_ENVELOPE"] = str(
        (ROOT / ".d972-runtime" / "pending-envelope.json").resolve()
    )
    spec = importlib.util.spec_from_file_location("d972_checker_v2_driver", CHECKER_V2)
    if spec is None or spec.loader is None:
        raise RuntimeError("DMTCP_CONTRACT_STOP checker-v2 driver unavailable")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    checker_argv = [
        "--state", str(args.state), "--producer-ledger", str(producer_ledger),
        "--out-dir", str(args.checker_out_dir),
    ]
    while True:
        before = (
            json.loads(args.state.read_text(encoding="utf-8"))
            if args.state.exists() else None
        )
        phase = campaign_phase(before)
        if phase == "terminal":
            code = before.get("status", {}).get("code")
            return 0 if code == "A_WITNESS_CROSSCHECKED" else 3
        before_hash = None if before is None else before.get("hash_chain", {}).get("checkpoint_sha256")
        if before_hash is not None and (not isinstance(before_hash, str) or len(before_hash) != 64):
            raise RuntimeError("STATE_STOP campaign loop missing phase input hash")

        if phase == "producer":
            # The v2 adapter deliberately ignores the legacy worker timeout.
            # A single GAP cell therefore remains inside this DMTCP process
            # until it completes or the external supervisor checkpoints and
            # kills it.
            exit_code = main(producer_argv)
            if exit_code != 0:
                return exit_code
        else:
            checker_code = int(checker.main(checker_argv))
            if checker_code != 0:
                return checker_code

        after = json.loads(args.state.read_text(encoding="utf-8"))
        after_hash = after.get("hash_chain", {}).get("checkpoint_sha256")
        if not isinstance(after_hash, str) or len(after_hash) != 64:
            raise RuntimeError("STATE_STOP campaign phase produced no checkpoint hash")
        if before_hash is not None and after_hash == before_hash:
            raise RuntimeError(f"STATE_STOP campaign {phase} phase made no state progress")
        # Terminal state is the only natural return.  Every nonterminal state
        # is fed back through campaign_phase, which selects checker or producer
        # and rejects an unrecognised/STATE_STOP status fail-closed.


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--self-test"]:
        return self_test()
    if args and args[0] == "--campaign-driver":
        return campaign_driver(args[1:])
    manifest = load_manifest()
    require_dmtcp_contract(manifest)
    legacy = load_legacy()
    install_v2_adapter(legacy, manifest)
    # Materialize the immutable seed before entering a potentially long GAP
    # preflight.  A DMTCP checkpoint taken in that first call can then bind an
    # on-disk predecessor as well as the in-memory Python state.
    seed_parser = argparse.ArgumentParser(add_help=False)
    seed_parser.add_argument("--state", type=Path)
    seed_args, _ = seed_parser.parse_known_args(args)
    if seed_args.state is not None and not seed_args.state.exists():
        observed = legacy.verify_anchors()
        target = legacy.target_receipt()
        seed = legacy.initial_state(observed, target)
        legacy.validate_state(seed)
        legacy.atomic_json(seed_args.state.resolve(), seed)
    return int(legacy.main(args))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(3)
