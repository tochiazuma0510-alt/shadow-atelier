#!/usr/bin/env python3
"""Resumable producer for the D972 relative-extension dovetail.

The mathematical enumeration is performed by ``d972_dovetail_worker_v1.g``.
This file owns only fail-closed input binding, deterministic state transitions,
the hash chain, and the normalized-table fallback used when the GAP
SmallGroups catalogue is not complete at a requested order.

Exit codes: 0 = PRELIGHT/UNKNOWN_RESUME/terminal written, 2 = STATE_STOP,
3 = ANCHOR_DRIFT or worker failure, 64 = command-line error.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from typing import Any, Iterable, Iterator, Sequence


SCHEMA_ID = "d972-dovetail-state/v1"
ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "search" / "d972_dovetail_worker_v1.g"
CHECKER = ROOT / "search" / "check_d972_dovetail_v1.py"
SCHEMA = ROOT / "search" / "d972_dovetail_state_schema_v1.json"
MANIFEST = ROOT / "search" / "d972_dovetail_manifest_v1.json"

ANCHORS: dict[str, str] = {
    "ops/inbox_codex/sol_task_148_dovetail.txt":
        "8890c29cf3c399da863e6705f3ccc434164c1c233ff82f648b965f99612e71f9",
    "docs/week1-定義ノート.md":
        "24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c",
    "docs/notes/d972_phase2_cofinal_execution_v1.md":
        "97998cac97611f10065b463efa8a417d5da200b23dd39ca7a8b2beed32de847e",
    "docs/notes/triad972_canonical_addendum_v2.md":
        "5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09ac2544c7659",
    "sol/sol_reply_143_typedfiber.md":
        "ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a",
    "search/certs/nf972_sourcemap_a_v3_20260804.json":
        "32e268c97c77446b85787c5d7750da758df67646de414eade709ca79baf98b37",
    "search/certs/nf972_sourcemap_b_v6_20260804.json":
        "e27a71fbf00295be9a74761ef11134e3a8f324ed57f523d11d44a67fb5a207de",
}

TARGET_A = ROOT / "search" / "certs" / "nf972_sourcemap_a_tuples_v2_20260804.json"
TARGET_B = ROOT / "search" / "certs" / "nf972_sourcemap_b_tuples_v3_20260804.json"
WORKER_STDERR: list[str] = []


class StateStop(RuntimeError):
    """A fail-closed state/input invariant failed."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp_name, path)
    finally:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(canonical_bytes(value).decode("utf-8") + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def verify_anchors() -> dict[str, str]:
    observed: dict[str, str] = {}
    failures: list[str] = []
    for relative, expected in ANCHORS.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing:{relative}")
            continue
        got = digest_file(path)
        observed[relative] = got
        if got != expected:
            failures.append(f"digest:{relative}:{got}:{expected}")
    if failures:
        raise StateStop("ANCHOR_DRIFT " + " ".join(failures))
    return observed


def serialize_target_tuple(row: Sequence[Any]) -> str:
    if not (
        isinstance(row, list)
        and len(row) == 3
        and isinstance(row[0], int)
        and isinstance(row[1], list)
        and len(row[1]) == 3
        and isinstance(row[2], list)
        and len(row[2]) == 9
    ):
        raise StateStop("TARGET_STOP malformed source-map-A tuple")
    can9: list[int] = []
    for pair in row[1]:
        if not isinstance(pair, list) or len(pair) != 2:
            raise StateStop("TARGET_STOP malformed can9 pair")
        can9.extend((int(pair[0]), int(pair[1])))
    values = [row[0], *can9, *(int(x) for x in row[2])]
    return f"({values[0]};{','.join(map(str, values[1:7]))};{','.join(map(str, values[7:]))})"


def target_receipt() -> dict[str, Any]:
    """Bind producer to source-map A; compare only to B's frozen tuple artefact."""
    a_doc = json.loads(TARGET_A.read_text(encoding="utf-8"))
    b_doc = json.loads(TARGET_B.read_text(encoding="utf-8"))
    a_rows = a_doc.get("tuples")
    b_rows = b_doc.get("tuples")
    if not isinstance(a_rows, list) or not isinstance(b_rows, list):
        raise StateStop("TARGET_STOP tuple arrays absent")
    a_keys = [serialize_target_tuple(row) for row in a_rows]
    if len(a_keys) != 972 or len(set(a_keys)) != 972:
        raise StateStop("TARGET_STOP source-map-A missing/duplicate keys")
    if len(b_rows) != 972 or len(set(b_rows)) != 972:
        raise StateStop("TARGET_STOP source-map-B missing/duplicate keys")
    if set(a_keys) != set(b_rows):
        raise StateStop("TARGET_STOP source-map A/B canonical sets disagree")
    return {
        "producer_source": str(TARGET_A.relative_to(ROOT)).replace("\\", "/"),
        "producer_source_sha256": digest_file(TARGET_A),
        "comparison_source": str(TARGET_B.relative_to(ROOT)).replace("\\", "/"),
        "comparison_source_sha256": digest_file(TARGET_B),
        "count": 972,
        "sorted_keys_sha256": digest_bytes(("\n".join(sorted(a_keys)) + "\n").encode("ascii")),
        # Source-map B is already in canonical sorted order.  Keep that exact
        # order: the GAP shadow classifier binds the LF-joined list to the
        # frozen 9c77... digest before it evaluates a single shadow.
        "keys": list(b_rows),
    }


def code_receipt() -> dict[str, str | None]:
    paths = {
        "producer": Path(__file__).resolve(),
        "worker": WORKER,
        "checker": CHECKER,
        "schema": SCHEMA,
        "manifest": MANIFEST,
    }
    return {name: digest_file(path) if path.is_file() else None for name, path in paths.items()}


def state_hash(state: dict[str, Any]) -> str:
    body = json.loads(json.dumps(state))
    body["hash_chain"]["checkpoint_sha256"] = "0" * 64
    return digest_bytes(canonical_bytes(body))


def _binding_set_digest(rows: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{path}={sha}\n" for path, sha in sorted(rows)).encode("utf-8")
    return digest_bytes(payload)


def _current_code_bindings(state: dict[str, Any]) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for name, row in state["integrity"]["code"].items():
        path = ROOT / row["path"]
        if not path.is_file():
            if row["required"] or name == "gap_worker":
                raise StateStop(f"STATE_STOP required code absent: {row['path']}")
            continue
        bindings[name] = digest_file(path)
    return bindings


def validate_state(state: dict[str, Any], *, bind_current: bool = True) -> None:
    if state.get("schema_version") != SCHEMA_ID:
        raise StateStop("STATE_STOP schema mismatch")
    chain = state.get("hash_chain")
    if not isinstance(chain, dict):
        raise StateStop("STATE_STOP hash_chain absent")
    claimed = chain.get("checkpoint_sha256")
    if not isinstance(claimed, str) or claimed != state_hash(state):
        raise StateStop("STATE_STOP state hash mismatch")
    status = state.get("status", {})
    if status.get("terminal") != (state.get("state_kind") == "TERMINAL"):
        raise StateStop("STATE_STOP terminal/state_kind mismatch")
    cursors = state.get("cursors", {})
    if cursors.get("exact_equal") != (
        cursors.get("producer") == cursors.get("checker") == cursors.get("agreed")
    ):
        raise StateStop("STATE_STOP cursor equality flag mismatch")
    if bind_current and state.get("integrity", {}).get("ready"):
        schema_sha = digest_file(SCHEMA)
        if state["integrity"]["schema"]["sha256"] != schema_sha:
            raise StateStop("STATE_STOP schema digest drift")
        observed = _current_code_bindings(state)
        for name, sha in observed.items():
            if state["integrity"]["code"][name]["sha256"] != sha:
                raise StateStop(f"STATE_STOP code digest drift: {name}")
        required_rows = [
            (row["path"], row["sha256"])
            for row in state["integrity"]["code"].values()
            if row["required"] or row["path"].endswith("d972_dovetail_worker_v1.g")
        ]
        if state["integrity"]["code_set_sha256"] != _binding_set_digest(required_rows):
            raise StateStop("STATE_STOP code-set digest mismatch")
        runtime = state.get("receipts", {}).get("runtime_integrity", {})
        if runtime.get("manifest_sha256") != digest_file(MANIFEST):
            raise StateStop("STATE_STOP manifest digest drift")


def _bind_seed_integrity(state: dict[str, Any]) -> None:
    observed = _current_code_bindings(state)
    for name, sha in observed.items():
        state["integrity"]["code"][name]["sha256"] = sha
    state["integrity"]["schema"]["sha256"] = digest_file(SCHEMA)
    required_rows = [
        (row["path"], row["sha256"])
        for row in state["integrity"]["code"].values()
        if row["required"] or row["path"].endswith("d972_dovetail_worker_v1.g")
    ]
    state["integrity"]["code_set_sha256"] = _binding_set_digest(required_rows)
    state["integrity"]["ready"] = all(sha for _, sha in required_rows)
    state["receipts"]["runtime_integrity"] = {
        "manifest_path": "search/d972_dovetail_manifest_v1.json",
        "manifest_sha256": digest_file(MANIFEST),
    }


def initial_state(anchor_observed: dict[str, str], target: dict[str, Any]) -> dict[str, Any]:
    state = json.loads(MANIFEST.read_text(encoding="utf-8"))
    state["state_kind"] = "CHECKPOINT"
    state["run"]["run_id"] = f"local-{time.time_ns()}"
    state["run"]["created_at_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    state["status"] = {
        "code": "CALIBRATION_PENDING", "terminal": False, "resumable": True,
        "reason": "Producer/checker k=1,2 calibration has not yet agreed.",
    }
    state["receipts"]["anchor_observed"] = anchor_observed
    state["receipts"]["target_keys"].update({
        "canonical_tuple_digest": target["sorted_keys_sha256"],
        "source_map_a_tuple_artifact_sha256": target["producer_source_sha256"],
        "source_map_b_tuple_artifact_sha256": target["comparison_source_sha256"],
    })
    _bind_seed_integrity(state)
    state["hash_chain"] = {
        "algorithm": "sha256",
        "canonicalization": "utf8-json-sort-keys-no-whitespace-v1",
        "digest_scope": "entire document with /hash_chain/checkpoint_sha256 replaced by 64 lowercase zeroes",
        "sequence": 0,
        "parent_checkpoint_sha256": None,
        "checkpoint_sha256": "0" * 64,
    }
    state["hash_chain"]["checkpoint_sha256"] = state_hash(state)
    return state


def _current_run_metadata() -> dict[str, Any]:
    """Bind a newly sealed checkpoint to the process that created it.

    Restored state is immutable input: this helper is called only by
    ``transition``.  Consequently a terminal no-op keeps its predecessor
    digest, while every real transition records the current workflow run.
    """
    run_id = os.environ.get("CURRENT_RUN_ID", "").strip()
    if not run_id:
        return {
            "run_id": f"local-{time.time_ns()}",
            "run_attempt": 0,
            "event": "local_seed",
            "commit_sha": None,
            "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "resume_run_id": None,
        }
    attempt_raw = os.environ.get("CURRENT_RUN_ATTEMPT", "")
    event = os.environ.get("CURRENT_EVENT", "")
    commit = os.environ.get("CURRENT_COMMIT", "").lower()
    source = os.environ.get("SOURCE_RUN_ID", "").strip() or None
    if not attempt_raw.isdigit() or event not in {"workflow_dispatch", "schedule"}:
        raise StateStop("STATE_STOP malformed current workflow run metadata")
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        raise StateStop("STATE_STOP malformed current workflow commit")
    if source is not None and (not source.isdigit() or source.startswith("0")):
        raise StateStop("STATE_STOP malformed source workflow run id")
    return {
        "run_id": run_id,
        "run_attempt": int(attempt_raw),
        "event": event,
        "commit_sha": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "resume_run_id": source,
    }


def transition(old: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    new = json.loads(json.dumps(old))
    old_hash = old["hash_chain"]["checkpoint_sha256"]
    for key, value in updates.items():
        new[key] = value
    new["run"] = _current_run_metadata()
    new["hash_chain"]["sequence"] = int(old["hash_chain"]["sequence"]) + 1
    new["hash_chain"]["parent_checkpoint_sha256"] = old_hash
    new["hash_chain"]["checkpoint_sha256"] = "0" * 64
    new["hash_chain"]["checkpoint_sha256"] = state_hash(new)
    return new


def _row_options(k: int, row: int) -> list[tuple[int, ...]]:
    remaining = tuple(x for x in range(k) if x != row)
    return [(row, *tail) for tail in itertools.permutations(remaining)]


def normalized_table_at(k: int, raw_index: int) -> list[list[int]]:
    """Decode one normalized Latin-table candidate in a fixed mixed radix."""
    if k < 1:
        raise ValueError("k must be positive")
    if k == 1:
        if raw_index != 0:
            raise IndexError(raw_index)
        return [[0]]
    radix = math.factorial(k - 1)
    total = radix ** (k - 1)
    if not 0 <= raw_index < total:
        raise IndexError(raw_index)
    digits: list[int] = []
    n = raw_index
    for _ in range(k - 1):
        digits.append(n % radix)
        n //= radix
    table = [list(range(k))]
    for row, digit in zip(range(1, k), digits):
        table.append(list(_row_options(k, row)[digit]))
    return table


def is_group_table(table: Sequence[Sequence[int]]) -> bool:
    k = len(table)
    universe = list(range(k))
    if k == 0 or list(table[0]) != universe:
        return False
    if any(len(row) != k or sorted(row) != universe for row in table):
        return False
    if any(table[i][0] != i for i in range(k)):
        return False
    if any(sorted(table[i][j] for i in range(k)) != universe for j in range(k)):
        return False
    return all(
        table[table[a][b]][c] == table[a][table[b][c]]
        for a in range(k) for b in range(k) for c in range(k)
    )


def relabel_table(table: Sequence[Sequence[int]], image: Sequence[int]) -> tuple[int, ...]:
    k = len(table)
    inv = [0] * k
    for old, new in enumerate(image):
        inv[new] = old
    return tuple(
        image[table[inv[a]][inv[b]]] for a in range(k) for b in range(k)
    )


def is_canonical_group_table(table: Sequence[Sequence[int]]) -> bool:
    k = len(table)
    flat = tuple(x for row in table for x in row)
    for tail in itertools.permutations(range(1, k)):
        image = (0, *tail)
        if relabel_table(table, image) < flat:
            return False
    return True


def next_fallback_table(k: int, start: int, deadline: float) -> tuple[int, list[list[int]] | None, bool]:
    """Return (next raw cursor, canonical table or None, exhausted)."""
    radix = math.factorial(max(0, k - 1))
    total = radix ** max(0, k - 1)
    cursor = start
    while cursor < total and time.monotonic() < deadline:
        table = normalized_table_at(k, cursor)
        cursor += 1
        if is_group_table(table) and is_canonical_group_table(table):
            return cursor, table, False
    return cursor, None, cursor >= total


def run_worker(mode: str, out_path: Path, env_extra: dict[str, str], timeout: float) -> dict[str, Any]:
    env = os.environ.copy()
    env.update({
        "D972_WORKER_MODE": mode,
        "D972_WORKER_OUTPUT": str(out_path.resolve()),
        "D972_MODE": mode,
        "D972_OUT": str(out_path.resolve()),
    })
    env.update(env_extra)
    if os.name == "nt":
        shell = shutil.which("powershell") or shutil.which("pwsh")
        if shell is None:
            raise StateStop("WORKER_STOP PowerShell not found on Windows")
        command = [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                   str((ROOT / "gap.ps1").resolve()), str(WORKER.resolve())]
    else:
        gap = shutil.which("gap")
        if gap is None:
            raise StateStop("WORKER_STOP GAP executable not found")
        command = [gap, "-q", "--quitonbreak", str(WORKER.resolve())]
    started = time.monotonic()
    completed = subprocess.run(
        command, cwd=ROOT, env=env, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=max(1.0, timeout), check=False,
    )
    if completed.stderr:
        WORKER_STDERR.append(f"[{mode}]\n{completed.stderr}")
    elapsed = time.monotonic() - started
    if completed.returncode != 0 or not out_path.is_file():
        raise StateStop(
            f"WORKER_STOP mode={mode} exit={completed.returncode} elapsed={elapsed:.3f} "
            f"stdout={completed.stdout[-2000:]!r} stderr={completed.stderr[-2000:]!r}"
        )
    result = json.loads(out_path.read_text(encoding="utf-8"))
    result["subprocess_receipt"] = {
        "exit_code": completed.returncode,
        "wall_seconds": round(elapsed, 6),
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
    }
    return result


def _calibration_observation(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    keys = ("marked_orbit_count", "gt_orders", "image_sizes", "zero_fiber_counts", "fiber_histograms")
    if any(key not in raw for key in keys):
        return None
    metrics = {key: raw[key] for key in keys}
    metrics["receipt_sha256"] = digest_bytes(canonical_bytes(metrics))
    return metrics


def _expected_metrics(case: dict[str, Any]) -> dict[str, Any]:
    return case["expected"]


def _valid_extension_completeness_receipt(raw: Any) -> bool:
    """Recognize the worker's mathematical coverage receipt, never infer it."""
    required_true = (
        "nonabelian_h_supported",
        "automorphism_pairs_exhaustive",
        "relator_defect_tuples_exhaustive",
        "marked_lift_pairs_exhaustive",
        "outer_buckets_prune_nothing",
    )
    return (
        isinstance(raw, dict)
        and all(raw.get(key) is True for key in required_true)
        and isinstance(raw.get("scope"), str)
        and "fixed labelled H" in raw["scope"]
        and isinstance(raw.get("exactness_gate"), str)
        and isinstance(raw.get("argument"), str)
        and len(raw["argument"]) > 40
    )


def preflight(state: dict[str, Any], out_dir: Path, seconds: int) -> dict[str, Any]:
    worker_out = out_dir / "worker_preflight.json"
    result = run_worker("base-audit", worker_out, {}, timeout=max(30, seconds))
    base = result.get("base", result)
    required = {
        "braid": True,
        "qbar_size": 8_817_984,
        "epsilon_kernel_size": 1_469_664,
        "fp_generator_count": 2,
    }
    for key, expected in required.items():
        if base.get(key) != expected:
            raise StateStop(f"PREFLIGHT_STOP {key}={base.get(key)!r} expected={expected!r}")
    fallback_cursor, c3_table, _ = next_fallback_table(3, 0, time.monotonic() + 10.0)
    if c3_table is None:
        raise StateStop("PREFLIGHT_STOP normalized table fallback failed to find C3")
    cases = json.loads(json.dumps(state["calibration_gate"]["cases"]))
    raw_cal = result.get("calibration", {})
    mismatch: str | None = None
    for case in cases:
        observation = _calibration_observation(raw_cal.get(case["case_id"]))
        if observation is not None:
            case["producer"] = observation
            if {k: observation[k] for k in _expected_metrics(case)} != _expected_metrics(case):
                mismatch = case["case_id"]
    selftest_out = out_dir / "worker_selftest.json"
    selftest = run_worker("selftest", selftest_out, {}, timeout=min(max(30, seconds), 600))
    if selftest.get("all_pass") is not True:
        raise StateStop("PREFLIGHT_STOP worker exact toy self-test failed")
    receipt = {
        "status": "PASS",
        "worker": result,
        "worker_selftest": selftest,
        "normalized_table_fixture": {
            "c3": c3_table,
            "next_raw_cursor": fallback_cursor,
            "fallback_algorithm": "normalized Latin rows; associativity; minimum under S_(k-1)",
        },
    }
    calibration_gate = json.loads(json.dumps(state["calibration_gate"]))
    calibration_gate["cases"] = cases
    receipts = json.loads(json.dumps(state["receipts"]))
    receipts["producer_preflight"] = receipt
    enumeration = json.loads(json.dumps(state["enumeration"]))
    # A self-test is not, by itself, a completeness theorem.  Upgrade only
    # when the worker explicitly emits its exhaustive factor-system receipt.
    worker_complete = selftest.get("relative_extension_completeness_receipt")
    blocked_noncheckpointable = (
        _valid_extension_completeness_receipt(worker_complete)
        and worker_complete.get("workflow_resumable") is False
    )
    if (
        _valid_extension_completeness_receipt(worker_complete)
        and worker_complete.get("workflow_resumable") is True
    ):
        complete_receipt = {
            "worker": worker_complete,
            "worker_sha256": digest_file(WORKER),
            "all_kernel_groups": {
                "smallgroups_accelerator_only": True,
                "fallback": (
                    "all normalized identity-zero Latin tables; associativity; "
                    "minimum under every relabeling fixing zero"
                ),
                "includes_nonabelian": True,
            },
        }
        complete_sha = digest_bytes(canonical_bytes(complete_receipt))
        receipts["relative_extension_completeness"] = {
            **complete_receipt, "receipt_sha256": complete_sha,
        }
        enumeration.update({
            "engine_status": "COMPLETE",
            "complete_relative_extensions": True,
            "includes_nonabelian": True,
            "engine_completeness_receipt_sha256": complete_sha,
        })
    else:
        enumeration.update({
            "engine_status": "BLOCKED" if blocked_noncheckpointable else "IMPLEMENTED_UNCALIBRATED",
            "complete_relative_extensions": False,
            "includes_nonabelian": True,
            "engine_completeness_receipt_sha256": None,
        })
        if blocked_noncheckpointable:
            receipts["relative_extension_blocker"] = {
                "subcode": "NONCHECKPOINTABLE_EXTENSION_CELL",
                "noncheckpointable_stages": worker_complete.get(
                    "noncheckpointable_stages", []
                ),
                "worker_receipt": worker_complete,
                "worker_sha256": digest_file(WORKER),
                "cursor_advance_authority": False,
            }
    if blocked_noncheckpointable:
        status = {
            "code": "BLOCKED_RELATIVE_EXTENSION_ENUMERATOR",
            "terminal": True,
            "resumable": False,
            "reason": (
                "NONCHECKPOINTABLE_EXTENSION_CELL: the exact worker exposes monolithic finite "
                "MTC/IsomorphismFpGroup and full shadow stages with no inner cursor; fixed-size "
                "workflow slices can retry forever without progress."
            ),
        }
        state_kind = "TERMINAL"
    elif mismatch is None:
        status = {
            "code": "CALIBRATION_PENDING", "terminal": False, "resumable": True,
            "reason": "Exact base preflight passed; independent k=1,2 checker agreement is pending.",
        }
        state_kind = "CHECKPOINT"
    else:
        calibration_gate["status"] = "FAILED"
        status = {
            "code": "CALIBRATION_STOP", "terminal": True, "resumable": False,
            "reason": f"Producer calibration disagreed with the frozen expectation: {mismatch}",
        }
        state_kind = "TERMINAL"
    next_state = transition(state, {
        "state_kind": state_kind,
        "status": status,
        "calibration_gate": calibration_gate,
        "enumeration": enumeration,
        "receipts": receipts,
    })
    atomic_json(out_dir / "preflight.json", receipt)
    return next_state


def _progress_of(state: dict[str, Any]) -> dict[str, Any]:
    default = {
        "k": state["cursors"]["producer"]["k"],
        "kernel_source": "auto",
        "kernel_index": state["cursors"]["producer"]["H"]["index"],
        "fallback_raw_index": 0,
        # For an order outside SmallGroups, the discovered canonical table is
        # retained until every action/defect/lift cell for that H is done.
        # Only then is it cleared and the raw table scan resumed strictly
        # after the table that produced it.
        "fallback_active_table": None,
        "automorphism_pair_index": state["cursors"]["producer"]["outer_action"]["index"],
        "defect_index": state["cursors"]["producer"]["extension_class"]["index"],
        "lift_pair_index": state["cursors"]["producer"]["marked_orbit"]["index"],
        "candidate_index": state["enumeration"]["semantic_key_count"],
    }
    saved = state.get("receipts", {}).get("enumeration_progress")
    if isinstance(saved, dict):
        default.update(saved)
    return default


def _schema_cursor(progress: dict[str, Any], stage: str = "candidate_evaluation") -> dict[str, Any]:
    k = int(progress["k"])
    h = int(progress["kernel_index"])
    a = int(progress["automorphism_pair_index"])
    d = int(progress["defect_index"])
    l = int(progress["lift_pair_index"])
    return {
        "k": k,
        "H": {"index": h, "semantic_key": f"k={k}/H={h}"},
        "outer_action": {"index": a, "semantic_key": f"k={k}/H={h}/A={a}"},
        "extension_class": {"index": d, "semantic_key": f"k={k}/H={h}/A={a}/D={d}"},
        "marked_orbit": {"index": l, "semantic_key": f"k={k}/H={h}/A={a}/D={d}/L={l}"},
        "stage": stage,
    }


def _gap_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _write_candidate_task(
    progress: dict[str, Any], table: list[list[int]], q_relators: list[list[int]],
    target_keys: list[str], *, smallgroups_complete: bool,
) -> Path:
    fd, name = tempfile.mkstemp(prefix="d972-task-", suffix=".g")
    os.close(fd)
    rows = [
        "D972_TASK := rec(",
        f"  k := {int(progress['k'])},",
        f"  kernel_source := {_gap_string(str(progress['kernel_source']))},",
        f"  h_index := {int(progress['kernel_index'])},",
        f"  aut_pair_index := {int(progress['automorphism_pair_index'])},",
        f"  defect_index := {int(progress['defect_index'])},",
        f"  lift_pair_index := {int(progress['lift_pair_index'])},",
        f"  candidate_index := {int(progress['candidate_index'])},",
        "  calibration_only := false,",
        f"  kernel_table := {json.dumps(table, separators=(',', ':'))},",
        f"  q_relators := {json.dumps(q_relators, separators=(',', ':'))},",
        f"  target_keys := {json.dumps(target_keys, ensure_ascii=True, separators=(',', ':'))},",
        "  q_order := 8817984,",
        f"  smallgroups_complete := {'true' if smallgroups_complete else 'false'}",
        ");;",
    ]
    Path(name).write_text("\n".join(rows) + "\n", encoding="ascii")
    return Path(name)


def _write_compare_task(left: dict[str, Any], right: dict[str, Any]) -> Path:
    fd, name = tempfile.mkstemp(prefix="d972-compare-", suffix=".g")
    os.close(fd)
    def cell_text(cell: dict[str, Any]) -> str:
        return "rec(" + ",".join((
            f"kernel_table:={json.dumps(cell['kernel_table'], separators=(',', ':'))}",
            f"q_relators:={json.dumps(cell['q_relators'], separators=(',', ':'))}",
            f"aut_pair_index:={int(cell['aut_pair_index'])}",
            f"defect_index:={int(cell['defect_index'])}",
            f"lift_pair_index:={int(cell['lift_pair_index'])}",
        )) + ")"
    Path(name).write_text(
        f"D972_TASK:=rec(left:={cell_text(left)},right:={cell_text(right)});;\n",
        encoding="ascii",
    )
    return Path(name)


def _compare_cells(left: dict[str, Any], right: dict[str, Any], out_dir: Path, seconds: int) -> bool:
    task = _write_compare_task(left, right)
    fd, out_name = tempfile.mkstemp(prefix="d972-compare-", suffix=".json", dir=out_dir)
    os.close(fd)
    out = Path(out_name)
    out.unlink(missing_ok=True)
    try:
        receipt = run_worker("compare", out, {"D972_TASK_G": str(task)}, timeout=seconds + 90)
        if receipt.get("status") != "PASS" or not isinstance(receipt.get("marked_over_base_isomorphic"), bool):
            raise StateStop("WORKER_STOP malformed exact compare receipt")
        return receipt["marked_over_base_isomorphic"]
    finally:
        task.unlink(missing_ok=True)
        out.unlink(missing_ok=True)


def _ledger_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise StateStop(f"STATE_STOP malformed producer ledger line {number}: {exc}") from exc
        if not isinstance(row, dict):
            raise StateStop(f"STATE_STOP non-object producer ledger line {number}")
        records.append(row)
    return records


def _ledger_binding(path: Path, records: list[dict[str, Any]], cursor: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return {"path": path.name, "sha256": None, "record_count": 0, "through_cursor_sha256": None}
    return {
        # Artifact bindings must survive extraction under a different runner
        # root.  The CLI/out-dir supplies the containing directory; recording
        # an absolute path here would make an otherwise identical resume fail.
        "path": path.name,
        "sha256": digest_file(path),
        "record_count": len(records),
        "through_cursor_sha256": digest_bytes(canonical_bytes(cursor)),
    }


def _candidate_semantic_key(k: int, table: list[list[int]], candidate: dict[str, Any]) -> str:
    material = {
        "k": k,
        "kernel_table": table,
        "fp_relators": candidate.get("fp_relators"),
        "lift_labels": candidate.get("lift_labels"),
        "factor_images": candidate.get("factor_images"),
    }
    return "d972:" + digest_bytes(canonical_bytes(material))


def _classification_records(path: Path) -> list[dict[str, Any]]:
    rows = _ledger_records(path)
    parent: str | None = None
    for index, row in enumerate(rows):
        if row.get("schema") != "d972-classification-ledger/v1":
            raise StateStop(f"STATE_STOP classification ledger schema at row {index}")
        if row.get("record_index") != index or row.get("parent_record_sha256") != parent:
            raise StateStop(f"STATE_STOP classification ledger gap/fork at row {index}")
        claimed = row.get("record_sha256")
        body = json.loads(json.dumps(row))
        body["record_sha256"] = "0" * 64
        if claimed != digest_bytes(canonical_bytes(body)):
            raise StateStop(f"STATE_STOP classification ledger digest at row {index}")
        parent = claimed
    return rows


def _append_classification_record(
    path: Path, rows: list[dict[str, Any]], record: dict[str, Any],
) -> dict[str, Any]:
    record = json.loads(json.dumps(record))
    record["schema"] = "d972-classification-ledger/v1"
    record["record_index"] = len(rows)
    record["parent_record_sha256"] = rows[-1]["record_sha256"] if rows else None
    record["record_sha256"] = "0" * 64
    record["record_sha256"] = digest_bytes(canonical_bytes(record))
    append_jsonl(path, record)
    rows.append(record)
    return record


def _classification_binding(
    path: Path, rows: list[dict[str, Any]], cursor: dict[str, Any],
) -> dict[str, Any]:
    return {
        "path": path.name,
        "sha256": digest_file(path),
        "record_count": len(rows),
        "representative_count": sum(row["record_kind"] == "REPRESENTATIVE" for row in rows),
        "duplicate_link_count": sum(row["record_kind"] == "EXACT_DUPLICATE_LINK" for row in rows),
        "through_cursor_sha256": digest_bytes(canonical_bytes(cursor)),
        "last_record_sha256": rows[-1]["record_sha256"] if rows else None,
    }


def _materialize_isolated_candidate(
    row: dict[str, Any], ledger_path: Path, candidates: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Idempotently materialize one isolated classification into its ledger."""
    candidate_id = row.get("eligible_candidate_id")
    if candidate_id is None:
        return None
    existing = next((x for x in candidates if x.get("candidate_id") == candidate_id), None)
    raw = row.get("raw_extension")
    shadow = row.get("shadow_receipt")
    if not isinstance(raw, dict) or not isinstance(shadow, dict):
        raise StateStop("STATE_STOP isolated classification lost its lossless payload")
    candidate = json.loads(json.dumps(raw))
    candidate.update({
        "cell": row["cell"],
        "k": row["cursor"]["k"],
        "candidate_id": candidate_id,
        "semantic_key": row["semantic_key"],
        "classification_status": "SHADOW_FIBER_CLASSIFIED",
        "ready_for_producer_ledger": True,
        "shadow_receipt": shadow,
    })
    if existing is not None:
        if existing != candidate:
            raise StateStop("STATE_STOP partial candidate/classification ledger disagreement")
        return existing
    expected_id = f"D972-k{row['cursor']['k']}-{len(candidates):08d}"
    if candidate_id != expected_id:
        raise StateStop("STATE_STOP candidate-id gap while reconciling classification journal")
    append_jsonl(ledger_path, candidate)
    candidates.append(candidate)
    return candidate


def one_slice(
    state: dict[str, Any], out_dir: Path, seconds: int, target_keys: list[str],
) -> dict[str, Any]:
    if state["calibration_gate"]["status"] != "PASSED":
        return preflight(state, out_dir, min(seconds, 600))
    enumeration_gate = state["enumeration"]
    if not (
        enumeration_gate.get("engine_status") == "COMPLETE"
        and enumeration_gate.get("complete_relative_extensions") is True
        and enumeration_gate.get("includes_nonabelian") is True
        and isinstance(enumeration_gate.get("engine_completeness_receipt_sha256"), str)
        and len(enumeration_gate["engine_completeness_receipt_sha256"]) == 64
    ):
        blocked_enum = json.loads(json.dumps(enumeration_gate))
        blocked_enum.update({
            "engine_status": "BLOCKED",
            "complete_relative_extensions": False,
            "engine_completeness_receipt_sha256": None,
        })
        return transition(state, {
            "state_kind": "TERMINAL",
            "status": {
                "code": "BLOCKED_RELATIVE_EXTENSION_ENUMERATOR",
                "terminal": True,
                "resumable": False,
                "reason": "Calibration unlocked without a bound exhaustive nonabelian relative-extension receipt.",
            },
            "enumeration": blocked_enum,
        })
    if not state["cursors"]["exact_equal"]:
        raise StateStop("STATE_STOP producer cannot advance beyond the last checker-agreed cursor")
    progress = _progress_of(state)
    current_k_row = next((row for row in state["enumeration"]["k_ledger"] if row["k"] == progress["k"]), None)
    if current_k_row is None:
        raise StateStop("STATE_STOP current k has no ledger row")
    opened_next_k = False
    if current_k_row and current_k_row["k_closed"]:
        progress.update({
            "k": int(progress["k"]) + 1, "kernel_source": "auto", "kernel_index": 0,
            "fallback_raw_index": 0, "fallback_active_table": None,
            "automorphism_pair_index": 0,
            "defect_index": 0, "lift_pair_index": 0,
        })
        opened_next_k = True
    receipts = json.loads(json.dumps(state["receipts"]))
    catalog = receipts.get("kernel_catalog")
    if not isinstance(catalog, dict) or catalog.get("k") != progress["k"]:
        catalog_out = out_dir / f"kernel_catalog_k{int(progress['k'])}.json"
        catalog = run_worker(
            "kernel-catalog", catalog_out, {"D972_K": str(progress["k"])},
            timeout=min(max(30, seconds), 600),
        )
        if catalog.get("status") != "PASS" or catalog.get("k") != progress["k"]:
            raise StateStop("WORKER_STOP malformed kernel-catalog receipt")
        receipts["kernel_catalog"] = catalog
    table: list[list[int]] | None = None
    smallgroups_complete = bool(catalog.get("smallgroups_complete"))
    if smallgroups_complete:
        tables = catalog.get("tables")
        if not isinstance(tables, list) or len(tables) != catalog.get("h_count") or not tables:
            raise StateStop("WORKER_STOP incomplete SmallGroups table catalogue")
        if progress["kernel_index"] >= len(tables):
            raise StateStop("STATE_STOP kernel index exceeds complete catalogue")
        table = tables[progress["kernel_index"]]
        progress["kernel_source"] = "smallgroups_complete"
    else:
        progress["kernel_source"] = "normalized_table_fallback"
        active = progress.get("fallback_active_table")
        if active is not None:
            if not isinstance(active, list):
                raise StateStop("STATE_STOP malformed persistent fallback kernel table")
            table = active
        else:
            deadline = time.monotonic() + max(0.1, seconds * 0.25)
            next_raw, table, exhausted = next_fallback_table(
                int(progress["k"]), int(progress["fallback_raw_index"]), deadline
            )
            progress["fallback_raw_index"] = next_raw
            if table is None:
                receipts["enumeration_progress"] = progress
                if not exhausted:
                    return transition(state, {
                        "status": {
                            "code": "UNKNOWN/RESUME", "terminal": False, "resumable": True,
                            "reason": "Normalized-table all-H scan paused at its exact raw cursor.",
                        },
                        "receipts": receipts,
                    })
                # Exhaustion here means the *entire* finite normalized table
                # space was scanned after the last completed H.  It never
                # follows merely from completing one H.
                producer_cursor = _schema_cursor(progress, "k_closure")
                cursors = json.loads(json.dumps(state["cursors"]))
                cursors.update({
                    "producer": producer_cursor, "exact_equal": False,
                    "agreement_receipt_sha256": None,
                })
                total_raw = math.factorial(max(0, int(progress["k"]) - 1)) ** max(
                    0, int(progress["k"]) - 1
                )
                closure = {
                    "h_count": int(progress["kernel_index"]),
                    "fallback_raw_table_count": total_raw,
                    "fallback_raw_cursor": int(progress["fallback_raw_index"]),
                    "all_normalized_tables_scanned": True,
                }
                receipts["pending_k_closure"] = {
                    "k": int(progress["k"]), "all_stages_exhausted": True,
                    "radices": closure,
                    "receipt_sha256": digest_bytes(canonical_bytes(closure)),
                }
                ledger_path = out_dir / "producer-ledger.jsonl"
                ledger_path.touch(exist_ok=True)
                closure_rows = _ledger_records(ledger_path)
                ledgers = json.loads(json.dumps(state["ledgers"]))
                ledgers["producer"] = _ledger_binding(
                    ledger_path, closure_rows, producer_cursor
                )
                classification_path = out_dir / "producer-classification-ledger.jsonl"
                classification_path.touch(exist_ok=True)
                classified = _classification_records(classification_path)
                receipts["classification_ledger"] = _classification_binding(
                    classification_path, classified, producer_cursor
                )
                receipts["classification_checker_required"] = True
                enumeration = json.loads(json.dumps(state["enumeration"]))
                if opened_next_k and not any(
                    row["k"] == progress["k"] for row in enumeration["k_ledger"]
                ):
                    enumeration["k_ledger"].append({
                        "k": int(progress["k"]), "status": "OPEN", "k_closed": False,
                        "enumerator_complete": False, "producer_checker_agree": True,
                        "remaining_items": None, "completeness_receipt_sha256": None,
                    })
                return transition(state, {
                    "status": {
                        "code": "CHECKER_PENDING", "terminal": False, "resumable": True,
                        "reason": "Producer exhausted the complete normalized all-H table space; checker closure is pending.",
                    },
                    "cursors": cursors, "enumeration": enumeration,
                    "ledgers": ledgers, "receipts": receipts,
                })
            progress["fallback_active_table"] = table
    if table is None or not is_group_table(table):
        raise StateStop("STATE_STOP selected kernel table failed producer group-law gate")
    if not smallgroups_complete and not is_canonical_group_table(table):
        raise StateStop("STATE_STOP fallback kernel table failed canonical relabeling gate")
    preflight_worker = state.get("receipts", {}).get("producer_preflight", {}).get("worker", {})
    q_relators = preflight_worker.get("q_relators")
    if not isinstance(q_relators, list) or not q_relators:
        raise StateStop("STATE_STOP exact base relators absent; run full preflight")
    task_path = _write_candidate_task(
        progress, table, q_relators, target_keys,
        smallgroups_complete=smallgroups_complete,
    )
    worker_out = out_dir / f"worker_slice_{int(state['hash_chain']['sequence']) + 1:08d}.json"
    try:
        try:
            result = run_worker("candidate", worker_out, {
                "D972_TASK_G": str(task_path), "D972_SLICE_SECONDS": str(seconds),
            }, timeout=seconds + 90)
        except subprocess.TimeoutExpired:
            receipts["enumeration_progress"] = progress
            receipts["last_retryable_stage"] = {
                "stage": "relative_extension_cell", "cursor": _schema_cursor(progress),
                "cursor_advance_authority": False,
            }
            return transition(state, {
                "status": {
                    "code": "UNKNOWN/RESUME", "terminal": False, "resumable": True,
                    "reason": "Relative-extension cell timed out; the exact same cell will retry.",
                },
                "receipts": receipts,
            })
        if result.get("status") in {"FAIL", "STOP", "INCONSISTENT_STOP"}:
            raise StateStop(f"WORKER_{result.get('status')} {result.get('reason', '')}")

        # Bind the generic factor-system coverage theorem emitted by the worker
        # to the already-approved engine receipt.  A cell receipt missing this
        # field has no cursor authority.
        cell_complete = result.get("relative_extension_completeness_receipt")
        if not _valid_extension_completeness_receipt(cell_complete):
            raise StateStop("WORKER_STOP candidate omitted exhaustive nonabelian receipt")
        bound_complete = state.get("receipts", {}).get(
            "relative_extension_completeness", {}
        ).get("worker")
        if bound_complete != cell_complete:
            raise StateStop("WORKER_STOP relative-extension completeness receipt drift")

        ledger_path = out_dir / "producer-ledger.jsonl"
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.touch(exist_ok=True)
        existing = _ledger_records(ledger_path)
        emitted = {row.get("semantic_key") for row in existing}
        classification_path = out_dir / "producer-classification-ledger.jsonl"
        classification_path.touch(exist_ok=True)
        classified = _classification_records(classification_path)
        candidates = result.get("candidates", [])
        if not isinstance(candidates, list) or len(candidates) > 1:
            raise StateStop("WORKER_STOP malformed raw candidate array")
        current_cell = {
            "kernel_table": table,
            "q_relators": q_relators,
            "aut_pair_index": progress["automorphism_pair_index"],
            "defect_index": progress["defect_index"],
            "lift_pair_index": progress["lift_pair_index"],
        }
        preadvance_cursor = _schema_cursor(progress)
        replay_rows = [
            row for row in classified
            if row.get("classification_terminal") is True
            and row.get("cursor") == preadvance_cursor
            and row.get("cell") == current_cell
        ]
        if len(replay_rows) > 1:
            raise StateStop("STATE_STOP multiple classification records for one exact cursor")
        shadow_summary: dict[str, Any] | None = None
        if replay_rows:
            replay = replay_rows[0]
            if replay.get("record_kind") == "REPRESENTATIVE":
                if replay.get("classification_status") == "ISOLATED_EXACT":
                    _materialize_isolated_candidate(replay, ledger_path, existing)
                    emitted = {row.get("semantic_key") for row in existing}
                elif replay.get("classification_status") != "NONISOLATED":
                    raise StateStop("STATE_STOP malformed replay representative status")
            elif not (
                replay.get("record_kind") == "EXACT_DUPLICATE_LINK"
                and replay.get("classification_status") == "EXACT_DUPLICATE"
            ):
                raise StateStop("STATE_STOP malformed replay duplicate status")
            # The journal is the write-ahead authority.  Do not classify or
            # append it again; finish the previously interrupted state move.
            candidates = []
            shadow_summary = {
                "status": "JOURNAL_REPLAY",
                "record_index": replay["record_index"],
                "cursor_advance_authority": True,
            }
        for candidate in candidates:
            if not isinstance(candidate, dict):
                raise StateStop("WORKER_STOP malformed raw candidate object")
            if not (
                candidate.get("relative_extension_only") is True
                and candidate.get("ready_for_producer_ledger") is False
            ):
                raise StateStop("WORKER_STOP candidate stage crossed the shadow boundary")
            raw_candidate = json.loads(json.dumps(candidate))
            raw_key = _candidate_semantic_key(int(progress["k"]), table, raw_candidate)

            duplicate = False
            for prior in classified:
                prior_shadow = prior.get("shadow_receipt")
                prior_terminal = (
                    prior.get("record_kind") == "REPRESENTATIVE"
                    and prior.get("classification_terminal") is True
                    and isinstance(prior_shadow, dict)
                    and prior_shadow.get("status") == "PASS"
                    and prior_shadow.get("classification_terminal") is True
                )
                if (
                    prior_terminal
                    and prior.get("cursor", {}).get("k") == progress["k"]
                    and isinstance(prior.get("cell"), dict)
                    and _compare_cells(prior["cell"], current_cell, out_dir, seconds)
                ):
                    duplicate = True
                    duplicate_receipt = {
                        "criterion": "unique marked-pair map is well-defined and bijective in both directions",
                        "marked_over_base_isomorphic": True,
                        "left_cell_sha256": digest_bytes(canonical_bytes(prior["cell"])),
                        "right_cell_sha256": digest_bytes(canonical_bytes(current_cell)),
                    }
                    _append_classification_record(classification_path, classified, {
                        "record_kind": "EXACT_DUPLICATE_LINK",
                        "cursor": _schema_cursor(progress),
                        "cell": current_cell,
                        "cell_sha256": digest_bytes(canonical_bytes(current_cell)),
                        "semantic_key": raw_key,
                        "classification_status": "EXACT_DUPLICATE",
                        "classification_terminal": True,
                        "raw_extension": raw_candidate,
                        "shadow_receipt": None,
                        "eligible_candidate_id": None,
                        "canonical_representative_record_index": prior["record_index"],
                        "canonical_semantic_key": prior["canonical_semantic_key"],
                        "exact_duplicate_receipt": duplicate_receipt,
                    })
                    shadow_summary = {
                        "status": "EXACT_DUPLICATE",
                        "canonical_representative_record_index": prior["record_index"],
                        "cursor_advance_authority": True,
                    }
                    break
            if duplicate:
                continue

            # The raw extension and shadow classifier form one transaction.
            # The task file remains live, with the frozen 972 keys, until this
            # second process returns a terminal classification receipt.
            shadow_out = out_dir / (
                f"shadow_slice_{int(state['hash_chain']['sequence']) + 1:08d}.json"
            )
            try:
                shadow = run_worker("shadow-fiber", shadow_out, {
                    "D972_TASK_G": str(task_path), "D972_SLICE_SECONDS": str(seconds),
                }, timeout=seconds + 90)
            except subprocess.TimeoutExpired:
                receipts["enumeration_progress"] = progress
                receipts["last_retryable_stage"] = {
                    "stage": "shadow_fiber", "cursor": _schema_cursor(progress),
                    "cursor_advance_authority": False,
                }
                return transition(state, {
                    "status": {
                        "code": "UNKNOWN/RESUME", "terminal": False, "resumable": True,
                        "reason": "Shadow/fiber classification timed out; no ledger write or cursor advance occurred.",
                    },
                    "receipts": receipts,
                })
            # Runtime timing/stdout is kept in the standalone artifact, not in
            # the mathematical ledger: replay must reproduce byte-identical
            # classification content after a crash between the two ledgers.
            shadow.pop("subprocess_receipt", None)
            if shadow.get("status") == "INCONSISTENT_STOP":
                receipts["inconsistent_shadow_receipt"] = shadow
                return transition(state, {
                    "state_kind": "TERMINAL",
                    "status": {
                        "code": "INCONSISTENT_STOP", "terminal": True, "resumable": False,
                        "reason": "Exact shadow reduction produced a forbidden image/fiber cardinality.",
                    },
                    "receipts": receipts,
                })
            if not (
                shadow.get("schema") == "d972_dovetail_worker/v1"
                and shadow.get("mode") == "shadow-fiber"
                and shadow.get("status") == "PASS"
                and shadow.get("runnable") is True
                and shadow.get("classification_terminal") is True
            ):
                receipts["enumeration_progress"] = progress
                receipts["last_retryable_stage"] = {
                    "stage": "shadow_fiber", "cursor": _schema_cursor(progress),
                    "cursor_advance_authority": False,
                    "worker_status": shadow.get("status"),
                }
                return transition(state, {
                    "status": {
                        "code": "UNKNOWN/RESUME", "terminal": False, "resumable": True,
                        "reason": "Shadow/fiber classifier did not return a terminal PASS receipt; the cell is unchanged.",
                    },
                    "receipts": receipts,
                })

            accept = shadow.get("accept_for_ledger") is True
            partial_candidate = next(
                (
                    row for row in existing
                    if row.get("semantic_key") == raw_key and row.get("cell") == current_cell
                ),
                None,
            )
            eligible_candidate_id = None
            if accept:
                eligible_candidate_id = (
                    partial_candidate["candidate_id"] if partial_candidate is not None
                    else f"D972-k{progress['k']}-{len(existing):08d}"
                )
            if accept:
                required_shadow_truth = (
                    "ready_for_producer_ledger", "relative_extension_rebuilt",
                    "factor_map_exact", "fp_permutation_isomorphism_exact",
                    "pure_extension_order_exact", "full_hexagon_3_3_literal",
                    "full_hexagon_3_4_literal", "shadow_surjectivity_exact",
                    "isolated", "all_shadows_settled", "frozen_target_digest_gate",
                    "image_subgroup_order_324_or_972", "fiber_uniform_on_image",
                    "equation_3_60_exact", "exact_972_fibers",
                )
                if not all(shadow.get(field) is True for field in required_shadow_truth):
                    raise StateStop("WORKER_STOP accepted shadow receipt lacks a truth gate")
                if not (
                    shadow.get("target_count") == 972
                    and shadow.get("target_key_count") == 972
                    and isinstance(shadow.get("fiber_counts"), list)
                    and len(shadow["fiber_counts"]) == 972
                    and isinstance(shadow.get("source_rows"), list)
                    and shadow.get("source_key_count") == len(shadow["source_rows"])
                ):
                    raise StateStop("WORKER_STOP accepted shadow receipt is not lossless/exact-972")
                candidate["cell"] = current_cell
                candidate["k"] = progress["k"]
                candidate["candidate_id"] = eligible_candidate_id
                key = raw_key
                candidate.update({
                    "semantic_key": key,
                    "classification_status": "SHADOW_FIBER_CLASSIFIED",
                    "ready_for_producer_ledger": True,
                    "shadow_receipt": shadow,
                })
                if key in emitted:
                    crash_row = next(
                        (row for row in existing if row.get("semantic_key") == key), None
                    )
                    if not (
                        isinstance(crash_row, dict)
                        and crash_row.get("candidate_id") == eligible_candidate_id
                        and crash_row.get("cell") == current_cell
                        and crash_row.get("shadow_receipt") == shadow
                    ):
                        raise StateStop("STATE_STOP semantic-key collision after exact pair-map dedup")
                else:
                    emitted.add(key)
                    append_jsonl(ledger_path, candidate)
                    existing.append(candidate)
            else:
                # A nonisolated extension is a completed classification, but
                # not a D972 candidate and therefore never enters the ledger.
                if not (
                    shadow.get("isolated") is False
                    and shadow.get("all_shadows_settled") is False
                    and shadow.get("ready_for_producer_ledger") is False
                    and shadow.get("exact_972_fibers") is False
                ):
                    raise StateStop("WORKER_STOP rejected shadow receipt is not a terminal nonisolated classification")
            representative_index = len(classified)
            _append_classification_record(classification_path, classified, {
                "record_kind": "REPRESENTATIVE",
                "cursor": _schema_cursor(progress),
                "cell": current_cell,
                "cell_sha256": digest_bytes(canonical_bytes(current_cell)),
                "semantic_key": raw_key,
                "classification_status": "ISOLATED_EXACT" if accept else "NONISOLATED",
                "classification_terminal": True,
                "raw_extension": raw_candidate,
                "shadow_receipt": shadow,
                "eligible_candidate_id": eligible_candidate_id,
                "canonical_representative_record_index": representative_index,
                "canonical_semantic_key": raw_key,
                "exact_duplicate_receipt": None,
            })
            shadow_summary = {
                key: value for key, value in shadow.items()
                if key not in {"source_rows", "fiber_counts", "zero_keys", "zero_indices"}
            }
    finally:
        task_path.unlink(missing_ok=True)
    aut_count = result.get("aut_count")
    counts = {
        "h_count": int(catalog["h_count"]) if smallgroups_complete else None,
        "automorphism_pair_count": aut_count * aut_count if isinstance(aut_count, int) else None,
        "defect_count": result.get("defect_count"),
        "lift_pair_count": result.get("lift_pair_count"),
    }
    needed = ("automorphism_pair_count", "defect_count", "lift_pair_count")
    if smallgroups_complete:
        needed = ("h_count", *needed)
    if any(not isinstance(counts.get(key), int) or counts[key] < 1 for key in needed):
        raise StateStop("WORKER_STOP incomplete tuple radices")
    # Advance exactly one mixed-radix cell; closure is left to the checker.
    progress["lift_pair_index"] += 1
    exhausted_k = False
    if progress["lift_pair_index"] >= counts["lift_pair_count"]:
        progress["lift_pair_index"] = 0
        progress["defect_index"] += 1
        if progress["defect_index"] >= counts["defect_count"]:
            progress["defect_index"] = 0
            progress["automorphism_pair_index"] += 1
            if progress["automorphism_pair_index"] >= counts["automorphism_pair_count"]:
                progress["automorphism_pair_index"] = 0
                progress["kernel_index"] += 1
                if smallgroups_complete:
                    if progress["kernel_index"] >= counts["h_count"]:
                        exhausted_k = True
                else:
                    # Completing one fallback H only releases that table.  The
                    # next slice resumes the raw normalized-table scan after
                    # it; only scan exhaustion at lines above can close k.
                    progress["fallback_active_table"] = None
    progress["candidate_index"] = len(existing)
    producer_cursor = _schema_cursor(progress, "k_closure" if exhausted_k else "candidate_evaluation")
    cursors = json.loads(json.dumps(state["cursors"]))
    cursors["producer"] = producer_cursor
    cursors["exact_equal"] = False
    cursors["agreement_receipt_sha256"] = None
    enumeration = json.loads(json.dumps(state["enumeration"]))
    if opened_next_k and not any(row["k"] == progress["k"] for row in enumeration["k_ledger"]):
        enumeration["k_ledger"].append({
            "k": int(progress["k"]), "status": "OPEN", "k_closed": False,
            "enumerator_complete": False, "producer_checker_agree": True,
            "remaining_items": None, "completeness_receipt_sha256": None,
        })
    enumeration["semantic_key_count"] = len(emitted)
    enumeration["semantic_key_set_sha256"] = digest_bytes(
        ("\n".join(sorted(str(x) for x in emitted)) + ("\n" if emitted else "")).encode("utf-8")
    ) if emitted else None
    receipts["enumeration_progress"] = progress
    receipts["last_worker_receipt"] = {k: v for k, v in result.items() if k not in {"candidates", "candidate"}}
    if shadow_summary is not None:
        receipts["last_shadow_classification"] = shadow_summary
    receipts["classification_ledger"] = _classification_binding(
        classification_path, classified, producer_cursor
    )
    receipts["classification_checker_required"] = True
    if exhausted_k:
        receipts["pending_k_closure"] = {
            "k": progress["k"],
            "all_stages_exhausted": True,
            "radices": counts,
            "receipt_sha256": digest_bytes(canonical_bytes(counts)),
        }
    ledgers = json.loads(json.dumps(state["ledgers"]))
    ledgers["producer"] = _ledger_binding(ledger_path, existing, producer_cursor)
    status = {
        "code": "CHECKER_PENDING", "terminal": False, "resumable": True,
        "reason": "Producer advanced one exact relative-extension cell; checker agreement is pending.",
    }
    return transition(state, {
        "status": status, "cursors": cursors, "enumeration": enumeration,
        "ledgers": ledgers, "receipts": receipts,
    })


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True, help="state JSON (created if absent)")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact directory")
    parser.add_argument("--slice-seconds", type=int, default=300, help="finite internal watchdog")
    parser.add_argument("--preflight-only", action="store_true", help="build and bind the exact base only")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.slice_seconds < 1:
        print("slice-seconds must be positive", file=sys.stderr)
        return 64
    state_path = args.state.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    stderr_lines: list[str] = []
    try:
        observed = verify_anchors()
        target = target_receipt()
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            validate_state(state)
            if state.get("receipts", {}).get("anchor_observed") != observed:
                raise StateStop("STATE_STOP observed anchors changed")
            target_receipt_saved = state.get("receipts", {}).get("target_keys", {})
            if target_receipt_saved.get("canonical_tuple_digest") != target["sorted_keys_sha256"]:
                raise StateStop("STATE_STOP canonical target changed")
        else:
            state = initial_state(observed, target)
        if state["status"]["terminal"]:
            atomic_json(state_path, state)
            print(f"{state['status']['code']} {state['hash_chain']['checkpoint_sha256']}")
            return 0
        if args.preflight_only:
            state = preflight(state, out_dir, args.slice_seconds)
        else:
            state = one_slice(state, out_dir, args.slice_seconds, target["keys"])
        validate_state(state)
        atomic_json(state_path, state)
        append_jsonl(out_dir / "state-chain.jsonl", {
            "sequence": state["hash_chain"]["sequence"],
            "parent_hash": state["hash_chain"]["parent_checkpoint_sha256"],
            "state_hash": state["hash_chain"]["checkpoint_sha256"],
            "status": state["status"]["code"],
            "cursor": state["cursors"]["producer"],
        })
        print(f"{state['status']['code']} {state['hash_chain']['checkpoint_sha256']}")
        return 0
    except StateStop as exc:
        stderr_lines.append(str(exc))
        receipt = {"status": "STATE_STOP", "reason": str(exc), "time_ns": time.time_ns()}
        atomic_json(out_dir / "state-stop.json", receipt)
        print(str(exc), file=sys.stderr)
        return 3 if str(exc).startswith(("ANCHOR_DRIFT", "WORKER_")) else 2
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        message = f"STATE_STOP unhandled infrastructure error: {type(exc).__name__}: {exc}"
        stderr_lines.append(message)
        atomic_json(out_dir / "state-stop.json", {"status": "STATE_STOP", "reason": message})
        print(message, file=sys.stderr)
        return 2
    finally:
        all_stderr = [*WORKER_STDERR, *stderr_lines]
        (out_dir / "stderr.log").write_text("\n".join(all_stderr) + ("\n" if all_stderr else ""), encoding="utf-8")
        files = [path for path in out_dir.rglob("*") if path.is_file()]
        atomic_json(out_dir / "resource_receipt.json", {
            "wall_seconds": round(time.monotonic() - started, 6),
            "artifact_file_count": len(files),
            "artifact_bytes_before_receipt": sum(path.stat().st_size for path in files),
            "pid": os.getpid(),
        })


if __name__ == "__main__":
    raise SystemExit(main())
