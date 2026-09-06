#!/usr/bin/env python3
"""Task1026: one k64 fixed-lambda batch with a private durable reduction prefix.

Frozen producer libraries are retained premises and arithmetic helpers. The
new batch selector, dependency decisions, target signs and final publication
are versioned here. No numerical consumer is called while loading old steps.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import signal
import stat
import sys
import time
import uuid
from typing import Any, Callable, Iterable

import numpy as np

SCHEMA = "d972.r07.fixed-lambda-cycle-batch.v2"
SEARCH = Path(__file__).resolve().parent
PROJECT = SEARCH.parent
L_FILE = "d972_r07_complete_oracle_cegar_continuation_v1.py"
L_SHA = "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"
C_FILE = "check_d972_r07_fixed_lambda_cycle_batch_v2.py"
N, EDGES, CHORDS = 54432, 108864, 54433
TOP, LOWER, PHYSICAL, PHYSICAL_LOWER, P1_ROWS = 36288, 96776, 48384, 32260, 8059
PHYSICAL_BYTES = 12096
BATCH_SIZE, MAX_BATCHES = 64, 1
POLICY = "CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX"
PARTIAL_POLICY = "PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY"
FORMULA = "v548-fixed-section;v547-signed-word;canonical-P1;four-B;batch-physical-reduction;single-final-separator"
ROLES = ("state", "delta", "seed34", "packet", "refinement", "oracle", "e", "prepare",
         "block-0", "block-1", "block-2", "block-3", "p1", "task712", "continuation")
SELECTION_PHASES = ("section", "cochain", "tree")
CANDIDATE_PHASES = ("raw", "source", "primal", "p1", "B", "reduction")
SCOPE = {"vertices": N, "edges": EDGES, "chords": CHORDS, "legality_rows": 5,
         "source_lower": LOWER, "physical_lower": PHYSICAL_LOWER, "physical": PHYSICAL,
         "p1_rows": P1_ROWS, "characters": [0, 1, 2, 3], "auxiliary_tests": 2,
         "batch_size": BATCH_SIZE, "max_batches": MAX_BATCHES}
FALSE_ASSURANCE = {"candidate": False, "cross_checked": False, "verified": False}
ASSURANCE = {"candidate": True, "cross_checked": False, "verified": False}
ANCHOR_ARTIFACT = {
    "run": 33990567016, "attempt": 1, "head": "c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70",
    "workflow": ".github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml",
    "id": 9977040548, "name": "d972-r07-complete-oracle-cegar-resume64-v1-candidate-33990567016-1",
    "bytes": 304642285, "sha256": "sha256:a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792",
    "repository_id": 1312092366, "conclusion": "success"}
ANCHOR_FIXED_FILES = {
    "output/owner.json": (8612, "e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b"),
    "output/source.json": (2423, "c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651"),
    "output/start.json": (54707, "87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b"),
    "output/fixed/manifest.json": (3159, "3ec178df5c2af9de7c55bb96075bb9e741111a241f7e02222ef5604587c87c41"),
    "output/HEAD": (964, "4614d5c3fc619007879f3a5062cde90ac0cab86552ddd17ff14306bc961ac2f4"),
    "output/result.json": (42785, "75f76ac43c86cfae998b0f4fe757a79b500727c2bfa847849fa57dbfa05293fd"),
    "checker-result.json": (330955, "ff55c51e90acead643b9683af6f82d492c503a92c83a504a97eeb3f62c31cc4d")}
LOOP_CHECKER_SHA = "e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"
STARTED = time.monotonic()
DEADLINE = math.inf
STOP_REQUESTED = False
CURRENT_PHASE = "initialization"
OUTPUT_CREATED: Path | None = None
SELFTEST_ROOT_CREATED: Path | None = None
COMPLETED_READONLY = False


class ResourceStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError("fixed_lambda_batch:" + message)


def integer(value: Any, low: int | None = None, high: int | None = None) -> bool:
    return type(value) is int and (low is None or low <= value) and (high is None or value <= high)


def trit(value: Any) -> bool:
    return integer(value, 0, 2)


def signrep(value: int) -> int:
    require(trit(value), "signed_trit_type")
    return (0, 1, -1)[value]


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(kind: str, body: Any) -> Any:
    require(isinstance(body, dict) and "schema" not in body and "sha256" not in body, "seal_reserved_fields")
    value = {"schema": SCHEMA + "." + kind, **copy.deepcopy(body)}
    return {**value, "sha256": sha(canonical(value))}


def check_seal(value: Any, kind: str | None = None) -> None:
    require(isinstance(value, dict) and isinstance(value.get("schema"), str) and
            (kind is None or value["schema"] == SCHEMA + "." + kind) and
            isinstance(value.get("sha256"), str) and
            value["sha256"] == sha(canonical({k: v for k, v in value.items() if k != "sha256"})), "canonical_object_seal")


def exact_keys(value: Any, keys: Iterable[str], label: str) -> None:
    require(isinstance(value, dict) and set(value) == set(keys), label)


def json_bytes(raw: bytes) -> Any:
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw, "sorted_ascii_json_with_final_LF")
    return value


def safe_name(name: Any) -> str:
    require(isinstance(name, str) and name and "\\" not in name and ":" not in name and
            not name.startswith("/") and all(part not in ("", ".", "..") for part in name.split("/")) and
            str(PurePosixPath(name)) == name, "safe_relative_path")
    return name


def safe_file(root: Path, name: str) -> Path:
    root = root.resolve()
    path = root.joinpath(*safe_name(name).split("/"))
    require(root in path.resolve().parents and path.is_file() and not path.is_symlink(), "regular_contained_file")
    for parent in path.parents:
        if parent == root:
            break
        require(not parent.is_symlink(), "no_symlink_parent")
    return path


def file_pin(path: Path, name: str | None = None) -> Any:
    require(path.is_file() and not path.is_symlink() and stat.S_ISREG(path.stat().st_mode), "pin_regular_file")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    body = {"bytes": path.stat().st_size, "sha256": digest}
    return {"file": safe_name(name), **body} if name is not None else body


def pin_type(entry: Any, *, binary: bool = False) -> None:
    exact_keys(entry, ("file", "bytes", "sha256", "dtype", "shape") if binary else
               ("file", "bytes", "sha256"), "exact_file_descriptor")
    safe_name(entry["file"])
    require(integer(entry["bytes"], 0) and isinstance(entry["sha256"], str) and
            re.fullmatch("[0-9a-f]{64}", entry["sha256"]) is not None, "file_descriptor_values")
    if binary:
        require(entry["dtype"] in ("packed3", "u8", "u32le") and isinstance(entry["shape"], list) and
                all(integer(x, 0) for x in entry["shape"]), "binary_descriptor_shape")


def read_json(root: Path, name: str, kind: str | None = None) -> Any:
    value = json_bytes(safe_file(root, name).read_bytes())
    if kind is not None:
        check_seal(value, kind)
    return value


def inventory(root: Path) -> Any:
    require(root.is_dir() and not root.is_symlink(), "inventory_regular_root")
    files, directories = [], []
    for index, path in enumerate(sorted(root.rglob("*"))):
        if index % 128 == 0:
            check_deadline("input_inventory")
        require(not path.is_symlink(), "inventory_no_symlink")
        name = safe_name(path.relative_to(root).as_posix())
        if path.is_dir():
            directories.append(name)
        else:
            files.append(file_pin(path, name))
    return {"files": sorted(files, key=lambda entry: entry["file"]), "directories": sorted(directories)}


def check_deadline(phase: str) -> None:
    global CURRENT_PHASE
    CURRENT_PHASE = phase
    if STOP_REQUESTED or time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)


def progress(phase: str, **fields: Any) -> None:
    check_deadline(phase)
    sys.stderr.write(canonical({"phase": phase, **fields}).decode("ascii"))
    sys.stderr.flush()


def request_stop(_signal: int, _frame: Any) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def sync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write(root: Path, name: str, raw: bytes, *, replace: bool = False) -> None:
    path = root.joinpath(*safe_name(name).split("/"))
    root.mkdir(parents=True, exist_ok=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not root.is_symlink() and not path.parent.is_symlink() and
            root.resolve() in path.resolve().parents and not path.is_symlink(), "atomic_contained_output")
    require(replace or not path.exists(), "atomic_no_overwrite")
    pending = path.parent / ("." + path.name + ".pending-" + uuid.uuid4().hex)
    with pending.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(pending, path)
    sync_directory(path.parent)


def write_once(root: Path, name: str, raw: bytes) -> None:
    path = root.joinpath(*safe_name(name).split("/"))
    if path.exists():
        require(not path.is_symlink() and path.read_bytes() == raw, "immutable_complete_payload")
    else:
        atomic_write(root, name, raw)


def own_dependencies() -> Any:
    path = safe_file(SEARCH, L_FILE)
    require(file_pin(path)["sha256"] == L_SHA, "frozen_own_L")
    spec = importlib.util.spec_from_file_location("task994_own_L", path)
    require(spec is not None and spec.loader is not None, "own_L_import_spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.check_deadline, module.progress = check_deadline, progress
    e, oracle, refinement, p2, m, base, descriptors = module.own_dependencies()
    for value in (e, oracle, refinement, p2, m, base):
        if hasattr(value, "check_deadline"):
            value.check_deadline = check_deadline
        if hasattr(value, "progress"):
            value.progress = progress
    return module, e, oracle, refinement, p2, m, base, descriptors


def encode_array(value: Any, dtype: str, shape: list[int] | None = None) -> tuple[bytes, str, Any]:
    if dtype == "json":
        require(shape is None, "JSON_has_no_array_shape")
        return canonical(value), dtype, None
    require(dtype in ("packed3", "u8", "u32le"), "registered_binary_dtype")
    data = np.asarray(value)
    require(data.dtype.kind in ("i", "u") and (shape is None or tuple(shape) == data.shape), "array_integer_shape")
    target_shape = list(data.shape)
    if dtype in ("packed3", "u8"):
        require(not np.any(data < 0) and not np.any(data > 2), "F3_array_trits")
        data = data.astype(np.uint8, copy=False)
        if dtype == "u8":
            return data.tobytes(order="C"), dtype, target_shape
        flat = data.reshape(-1)
        padded = np.zeros(((flat.size + 3) // 4) * 4, dtype=np.uint8)
        padded[:flat.size] = flat
        rows = padded.reshape(-1, 4).astype(np.uint16)
        packed = rows[:, 0] + 3 * rows[:, 1] + 9 * rows[:, 2] + 27 * rows[:, 3]
        return packed.astype(np.uint8).tobytes(), dtype, target_shape
    require(data.size == 0 or (0 <= int(np.min(data)) and int(np.max(data)) <= 4294967295),
            "u32_unsigned_range")
    return data.astype("<u4").tobytes(order="C"), dtype, target_shape


def decode_array(raw: bytes, dtype: str, shape: Any) -> Any:
    if dtype == "json":
        require(shape is None, "JSON_descriptor_null_shape")
        return json_bytes(raw)
    require(dtype in ("packed3", "u8", "u32le") and isinstance(shape, list) and
            all(integer(x, 0) for x in shape), "decode_array_shape")
    count = math.prod(shape)
    require(len(raw) == ((count + 3) // 4 if dtype == "packed3" else count * (4 if dtype == "u32le" else 1)),
            "binary_exact_EOF")
    if dtype == "u32le":
        return np.frombuffer(raw, dtype="<u4").copy().reshape(shape)
    packed = np.frombuffer(raw, dtype=np.uint8)
    if dtype == "u8":
        require(not np.any(packed > 2), "u8_exact_trit_range")
        return packed.copy().reshape(shape)
    require(not np.any(packed > 80), "base3_four_trit_byte_range")
    digits = ((packed[:, None].astype(np.uint16) // np.asarray([1, 3, 9, 27], dtype=np.uint16)) % 3).astype(np.uint8).reshape(-1)
    require(not np.any(digits[count:]), "packed_final_padding_zero")
    return digits[:count].copy().reshape(shape)


def process_measurement() -> Any:
    rss = None
    try:
        import resource
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    except (ImportError, OSError):
        pass
    io = None
    path = Path("/proc/self/io")
    if path.is_file():
        entries = {}
        for line in path.read_text(encoding="ascii").splitlines():
            key, value = line.split(":", 1)
            if key in ("rchar", "wchar", "read_bytes", "write_bytes"):
                entries[key] = int(value.strip())
        require(set(entries) == {"rchar", "wchar", "read_bytes", "write_bytes"} and
                all(integer(x, 0) for x in entries.values()), "proc_io_exact_fields")
        io = entries
    return {"process_ru_maxrss_kib": rss, "proc_io": io}


def phase_telemetry(phase: str, begun: float, before: Any, payload_bytes: int) -> Any:
    after = process_measurement()
    return seal("phase-telemetry", {"phase": phase, "elapsed_seconds": round(time.monotonic() - begun, 6),
        "process_ru_maxrss_kib": after["process_ru_maxrss_kib"],
        "proc_io_before": before["proc_io"], "proc_io_after": after["proc_io"],
        "payload_bytes": payload_bytes, "measurement_scope":
            "process-cumulative-rusage-and-proc-io;payload-bytes-are-output-only", "eof": True})


def validate_telemetry(value: Any, phase: str, payload_bytes: int) -> None:
    check_seal(value, "phase-telemetry")
    exact_keys(value, ("schema", "sha256", "phase", "elapsed_seconds", "process_ru_maxrss_kib",
        "proc_io_before", "proc_io_after", "payload_bytes", "measurement_scope", "eof"), "phase_telemetry_keys")
    require(value["phase"] == phase and type(value["elapsed_seconds"]) in (int, float) and
            math.isfinite(value["elapsed_seconds"]) and value["elapsed_seconds"] >= 0 and
            (value["process_ru_maxrss_kib"] is None or integer(value["process_ru_maxrss_kib"], 0)) and
            integer(value["payload_bytes"], 0) and value["payload_bytes"] == payload_bytes and value["eof"] is True and
            value["measurement_scope"] == "process-cumulative-rusage-and-proc-io;payload-bytes-are-output-only",
            "phase_telemetry_type")
    for key in ("proc_io_before", "proc_io_after"):
        item = value[key]
        if item is not None:
            exact_keys(item, ("rchar", "wchar", "read_bytes", "write_bytes"), "phase_IO_fields")
            require(all(integer(x, 0) for x in item.values()), "phase_IO_nonnegative_integers")


def f3_array(value: Any, shape: tuple[int, ...], label: str) -> np.ndarray:
    require(isinstance(value, np.ndarray) and value.shape == shape and value.dtype.kind in ("i", "u") and
            not np.any(value < 0) and not np.any(value > 2), label)
    return value


def classify_batch(oracle: Any, chords: np.ndarray, tau: np.ndarray, values: np.ndarray,
                   residuals: np.ndarray, basis: list[int], fit: np.ndarray, auxiliary: np.ndarray,
                   *, expected_chords: int = CHORDS, eof: bool = True) -> Any:
    """Complete roster first; candidate count never bounds the cochain test."""
    require(eof is True and integer(expected_chords, 5) and isinstance(chords, np.ndarray) and
            chords.shape == (expected_chords,) and chords.dtype.kind in ("i", "u") and
            all(0 <= int(x) < EDGES for x in chords) and
            np.all(np.diff(chords.astype(np.int64)) > 0), "complete_ascending_actual_chord_roster")
    f3_array(tau, (expected_chords, 5), "all_chord_tau")
    f3_array(values, (expected_chords,), "all_chord_values")
    f3_array(residuals, (expected_chords,), "all_chord_residuals")
    f3_array(fit, (5,), "five_fit_coefficients")
    f3_array(auxiliary, (2,), "both_auxiliary_values")
    require(isinstance(basis, list) and len(basis) == len(set(basis)) == 5 and
            all(integer(index, 0, expected_chords - 1) for index in basis), "five_registered_basis_indices")
    fitted = oracle.solve_five(tau[basis], values[basis])
    calculated = ((values.astype(np.int32) - tau.astype(np.int32) @ fit.astype(np.int32)) % 3).astype(np.uint8)
    require(np.array_equal(fitted, fit) and np.array_equal(calculated, residuals) and
            not np.any(residuals[basis]), "all_residuals_and_rank_five_fit")
    failed = np.flatnonzero(residuals).astype(np.uint32)
    failed_edges = chords[failed.astype(np.int64)].astype(np.uint32)
    matrix = tau[basis].T
    basis_edges = [int(chords[index]) for index in basis]
    witnesses = []
    if len(failed):
        for raw_index in failed[:BATCH_SIZE]:
            index = int(raw_index)
            d = oracle.solve_five(matrix, tau[index])
            tau_zero = ((tau[index].astype(np.int32) - matrix.astype(np.int32) @ d.astype(np.int32)) % 3).astype(np.uint8)
            scalar = (int(values[index]) - sum(int(d[j]) * int(values[basis[j]]) for j in range(5))) % 3
            require(not np.any(tau_zero) and scalar == int(residuals[index]) and scalar in (1, 2),
                    "candidate_six_cycle_tau_and_selection_scalar")
            witnesses.append({"kind": "chord", "roster_index": index, "edge": int(chords[index]),
                "coordinate": None, "failed_chord": int(chords[index]),
                "basis_chords": list(basis_edges), "basis_coefficients": [int(x) for x in d],
                "cycles": [{"edge": int(chords[index]), "coefficient": 1}] +
                    [{"edge": basis_edges[j], "coefficient": (-int(d[j])) % 3} for j in range(5)],
                "eta": [0, 0], "tau": [0] * 5, "scalar": scalar, "materialization": "MATERIALIZATION_PENDING"})
    else:
        nonzero_aux = np.flatnonzero(auxiliary)
        if len(nonzero_aux):
            coordinate = int(nonzero_aux[0])
            witnesses.append({"kind": "auxiliary", "roster_index": None, "edge": None,
                "coordinate": coordinate, "failed_chord": None, "basis_chords": [], "basis_coefficients": [],
                "cycles": [], "eta": [int(j == coordinate) for j in range(2)], "tau": [0] * 5,
                "scalar": int(auxiliary[coordinate]), "materialization": "MATERIALIZATION_PENDING"})
    terminal = "VIOLATION_CANDIDATE" if witnesses else "COMPLETE_ZERO_CANDIDATE"
    require((not len(failed) and not np.any(auxiliary)) == (terminal == "COMPLETE_ZERO_CANDIDATE"),
            "zero_requires_complete_chord_and_auxiliary_zero")
    require(len(witnesses) == (min(BATCH_SIZE, len(failed)) if len(failed) else int(np.any(auxiliary))),
            "fixed_roster_size_no_refill")
    return {"terminal": terminal, "witnesses": witnesses, "failed_indices": failed, "failed_edges": failed_edges,
        "failed_count": int(len(failed)), "first_failed_index": int(failed[0]) if len(failed) else None,
        "first_failed_edge": int(failed_edges[0]) if len(failed) else None,
        "basis_edges": basis_edges, "basis_tau": tau[basis].copy(), "fit": fit.copy(),
        "auxiliary": auxiliary.copy(), "full_chord_eof": True}


def current_batch_tree(oracle: Any, fixed: Any, cochain: Any) -> Any:
    geometry, f = fixed.geometry, cochain["f"]
    potential = oracle.integrate_tree(geometry["next"], geometry["parent"], geometry["parent_edge"], geometry["order"], f)
    chords, tau = geometry["chords"], fixed.values["chord-tau.u8"]
    values = oracle.chord_values(geometry["next"], chords, f, potential)
    basis = np.searchsorted(chords, fixed.values["selected-chords.u32"]).astype(np.int64).tolist()
    require(len(basis) == 5 and all(integer(index, 0, CHORDS - 1) for index in basis) and
            np.array_equal(chords[basis], fixed.values["selected-chords.u32"]), "fixed_basis_actual_chord_ids")
    fit = oracle.solve_five(tau[basis], values[basis])
    residuals = ((values.astype(np.int32) - tau.astype(np.int32) @ fit.astype(np.int32)) % 3).astype(np.uint8)
    selected = classify_batch(oracle, chords, tau, values, residuals, basis, fit, cochain["b_aux"])
    check_deadline("complete_fixed_lambda_all_chords")
    return {"potential": potential, "tau": tau, "values": values, "residuals": residuals,
        "fit": fit, "basis": basis, "selection": selected}


def make_reduction_state(anchor: Any, row_sources: list[Any]) -> Any:
    """Copy mutable history once; the immutable selection never follows this state."""
    require(anchor["kind"] == "Separator" and integer(anchor["rank"], 0, PHYSICAL) and
            len(anchor["records"]) == len(anchor["rows"]) == len(anchor["leads"]) ==
                len(row_sources) == anchor["rank"], "anchor_complete_physical_basis")
    return {"kind": "BatchReductionState", "rank": anchor["rank"], "generation": anchor["generation"],
        "head": anchor["head"], "target_raw": bytes(anchor["target_raw"]), "lambda": None, "lambda_raw": None,
        "records": copy.deepcopy(anchor["records"]), "rows": list(anchor["rows"]), "leads": list(anchor["leads"]),
        "row_sources": copy.deepcopy(row_sources), "selection_pairings": [0] * anchor["rank"],
        "anchor_rank": anchor["rank"], "anchor_generation": anchor["generation"],
        "processed_candidates": 0, "dependent_candidates": 0, "accepted_new_rows": 0,
        "last_candidate_manifest_sha256": None, "last_row_manifest_sha256": None,
        "target_parents": copy.deepcopy(anchor["target_parents"])}


def reduce_candidate_numeric(oracle: Any, m: Any, selection_lambda: np.ndarray, state: Any,
                             physical_raw: bytes, selection_scalar: int) -> Any:
    """The immutable selection scalar and the growing-span remainder are distinct."""
    f3_array(selection_lambda, (PHYSICAL,), "selection_lambda_exact_physical_trits")
    require(state["kind"] == "BatchReductionState" and state["lambda"] is None and state["lambda_raw"] is None and
            state["rank"] == state["anchor_rank"] + state["accepted_new_rows"] and
            state["generation"] == state["anchor_generation"] + state["accepted_new_rows"] and
            len(state["rows"]) == len(state["records"]) == len(state["leads"]) ==
                len(state["selection_pairings"]) == state["rank"], "private_growing_span_counts")
    require(integer(selection_scalar, 1, 2) and
            all(value == 0 for value in state["selection_pairings"][:state["anchor_rank"]]), "nonzero_selection_old_span_zero")
    dense_raw = decode_array(physical_raw, "packed3", [PHYSICAL])
    raw_pairing = oracle.dot(selection_lambda, dense_raw)
    require(raw_pairing == selection_scalar, "raw_row_fixed_selection_scalar")
    remainder, events = m.physical_reduce(physical_raw, state["records"], state["rows"])
    dense_remainder = decode_array(remainder, "packed3", [PHYSICAL])
    coefficients = np.zeros(state["rank"], dtype=np.uint8)
    previous = -1
    for item in events:
        index = item["pivot_id"]
        require(integer(index, previous + 1, state["rank"] - 1) and integer(item["scalar"], 1, 2) and
                item["offer"] == state["records"][index]["offer"] and item["lead"] == state["leads"][index] and
                item["row_sha256"] == sha(state["rows"][index]), "insertion_order_physical_event")
        coefficients[index], previous = item["scalar"], index
    subtracted_new = sum(int(coefficients[index]) * int(state["selection_pairings"][index])
                         for index in range(state["anchor_rank"], state["rank"])) % 3
    remainder_pairing = oracle.dot(selection_lambda, dense_remainder)
    require((raw_pairing - subtracted_new) % 3 == remainder_pairing and
            all(dense_remainder[lead] == 0 for lead in state["leads"]), "remainder_selection_identity_including_new_rows")
    dependent = not np.any(dense_remainder)
    if dependent:
        require(remainder_pairing == 0, "dependent_zero_pairing")
        return {"outcome": "DEPENDENT", "coefficients": coefficients, "events": copy.deepcopy(events),
            "remainder": remainder, "normalized": None, "lead": None, "sigma": None,
            "target": bytes(state["target_raw"]), "target_scalar": None, "normalized_pairing": None,
            "raw_pairing": raw_pairing, "remainder_pairing": remainder_pairing,
            "subtracted_new_pairing": subtracted_new}
    require(state["rank"] < PHYSICAL, "ambient_rank_upper_bound")
    normalized, lead, sigma = m.normalize_pivot(remainder, state["leads"])
    dense_normalized = decode_array(normalized, "packed3", [PHYSICAL])
    require(integer(lead, 0, PHYSICAL - 1) and integer(sigma, 1, 2) and
            dense_normalized[lead] == 1 and not np.any(dense_normalized[:lead]) and
            np.array_equal(dense_normalized, (sigma * dense_remainder.astype(np.uint16) % 3).astype(np.uint8)),
            "one_monic_scale_on_new_remainder")
    target, theta = m.update_target(state["target_raw"], normalized, lead, state["leads"])
    old_target = decode_array(state["target_raw"], "packed3", [PHYSICAL])
    new_target = decode_array(target, "packed3", [PHYSICAL])
    require(trit(theta) and theta == int(old_target[lead]) and
            np.array_equal((old_target.astype(np.int16) - new_target.astype(np.int16)) % 3,
                           theta * dense_normalized.astype(np.uint16) % 3), "target_minus_theta_normalized_sign")
    normalized_pairing = oracle.dot(selection_lambda, dense_normalized)
    require(normalized_pairing == sigma * remainder_pairing % 3, "normalized_fixed_lambda_pairing_may_be_zero")
    return {"outcome": "INDEPENDENT", "coefficients": coefficients, "events": copy.deepcopy(events),
        "remainder": remainder, "normalized": normalized, "lead": lead, "sigma": sigma,
        "target": target, "target_scalar": theta, "normalized_pairing": normalized_pairing,
        "raw_pairing": raw_pairing, "remainder_pairing": remainder_pairing,
        "subtracted_new_pairing": subtracted_new}


def advance_reduction_numeric(state: Any, numeric: Any, instruction: Any | None, row_source: Any | None,
                              target_parent: Any | None) -> Any:
    """Produce a new private state; publishing its metadata is a separate transaction."""
    updated = copy.deepcopy(state)
    updated["processed_candidates"] += 1
    if numeric["outcome"] == "DEPENDENT":
        require(instruction is row_source is target_parent is None and numeric["normalized"] is None and
                numeric["target"] == state["target_raw"] and numeric["target_scalar"] is None,
                "dependent_has_no_physical_append")
        updated["dependent_candidates"] += 1
    else:
        require(numeric["outcome"] == "INDEPENDENT" and instruction is not None and row_source is not None and
                target_parent is not None and instruction["predecessor"] == state["head"] and
                instruction["offer"] == state["generation"] and instruction["rank"] == state["rank"] + 1 and
                instruction["generation"] == state["generation"] + 1 and instruction["lead"] == numeric["lead"] and
                instruction["sigma"] == numeric["sigma"] and instruction["physical_sha256"] == sha(numeric["normalized"]),
                "new_physical_instruction_count_and_row")
        updated["records"].append({"offer": instruction["offer"], "rank": instruction["rank"], "lead": instruction["lead"],
            "physical_offset": state["rank"] * PHYSICAL_BYTES, "rolling_sha256": instruction["rolling_sha256"]})
        updated["rows"].append(numeric["normalized"])
        updated["leads"].append(numeric["lead"])
        updated["row_sources"].append(copy.deepcopy(row_source))
        updated["selection_pairings"].append(numeric["normalized_pairing"])
        updated["target_parents"].append(copy.deepcopy(target_parent))
        updated.update({"rank": state["rank"] + 1, "generation": state["generation"] + 1,
            "accepted_new_rows": state["accepted_new_rows"] + 1, "head": instruction["rolling_sha256"],
            "target_raw": numeric["target"]})
    require(updated["processed_candidates"] == updated["dependent_candidates"] + updated["accepted_new_rows"] and
            updated["rank"] == updated["anchor_rank"] + updated["accepted_new_rows"] and
            updated["generation"] == updated["anchor_generation"] + updated["accepted_new_rows"] and
            updated["kind"] == "BatchReductionState" and updated["lambda"] is None, "separate_candidate_and_row_cursors")
    return updated


def final_separator_numeric(oracle: Any, m: Any, state: Any, anchor_target: bytes) -> Any:
    """One reverse insertion solve after the selected prefix has finished."""
    target = decode_array(state["target_raw"], "packed3", [PHYSICAL])
    require(all(target[lead] == 0 for lead in state["leads"]), "final_target_all_pivot_coordinates_zero")
    positions = np.flatnonzero(target)
    if not len(positions):
        return {"kind": "LinearMembershipCandidate", "lambda": None, "direct_pairing": None}
    free = int(positions[0])
    require(free not in state["leads"], "final_separator_free_target_coordinate")
    functional = np.zeros(PHYSICAL, dtype=np.uint8)
    functional[free] = int(target[free])
    for index in range(state["rank"] - 1, -1, -1):
        row = decode_array(state["rows"][index], "packed3", [PHYSICAL])
        lead = state["leads"][index]
        require(row[lead] == 1 and functional[lead] == 0, "final_reverse_monic_unassigned_coordinate")
        functional[lead] = (-oracle.dot(row, functional)) % 3
        require(oracle.dot(row, functional) == 0, "final_reverse_row_equation")
        if index % 128 == 0:
            check_deadline("final_reverse_separator")
    direct = m.check_final_separator(functional, state["rows"], anchor_target, state["target_raw"])
    return {"kind": "Separator", "lambda": encode_array(functional, "packed3", [PHYSICAL])[0],
        "direct_pairing": direct}


def character_counts(values: np.ndarray, width: int) -> list[Any]:
    f3_array(values, (4, width), "four_character_count_rows")
    return [{"character": index, "offset": index * width, "trits": width,
             "support": int(np.count_nonzero(values[index])),
             "trit_counts": [int(np.count_nonzero(values[index] == scalar)) for scalar in range(3)]}
            for index in range(4)]

REGISTERED_ARTIFACTS = json.loads(r'''{
  "state": {
    "run": 33891714539,
    "attempt": 1,
    "head": "7b7b9de20faaa3b8f26e331bb738b374f6f5708c",
    "id": 9944214057,
    "name": "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1",
    "bytes": 107195261,
    "sha256": "sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017",
    "workflow": ".github/workflows/d972-r07-grade2-physical-state-separator-v2.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "delta": {
    "run": 33946247365,
    "attempt": 1,
    "head": "7f6dfaddf4150449e62a9b3e85def472fcb41c01",
    "id": 9963533999,
    "name": "d972-r07-actual-seed30-materializer-v1-candidate-33946247365-1",
    "bytes": 915410,
    "sha256": "sha256:f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6",
    "workflow": ".github/workflows/d972-r07-actual-seed30-materializer-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "seed34": {
    "run": 33956437467,
    "attempt": 1,
    "head": "b9ae78b0950b186463849c3ec874f6474f359851",
    "id": 9966542166,
    "name": "d972-r07-actual-root-seed-materializer-v3-candidate-33956437467-1",
    "bytes": 984053,
    "sha256": "sha256:a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc",
    "workflow": ".github/workflows/d972-r07-actual-root-seed-materializer-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "packet": {
    "run": 33964709359,
    "attempt": 1,
    "head": "fff114c41bd8748ad0e708919fe0820335c9cce8",
    "id": 9969090590,
    "name": "d972-r07-fixed-root-packet-loop-v2-candidate-33964709359-1",
    "bytes": 1855391,
    "sha256": "sha256:b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428",
    "workflow": ".github/workflows/d972-r07-fixed-root-packet-loop-v2.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "refinement": {
    "run": 33971897879,
    "attempt": 1,
    "head": "64475e1dfab1537a38d1b3131971bfed5fc3071c",
    "id": 9971466432,
    "name": "d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1",
    "bytes": 51943596,
    "sha256": "sha256:0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8",
    "workflow": ".github/workflows/d972-r07-full-origin-checker-completion-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "oracle": {
    "run": 33977701313,
    "attempt": 1,
    "head": "bbce98d8f95a845f36fe89c0f507b9360792666f",
    "id": 9972829869,
    "name": "d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1",
    "bytes": 2299772,
    "sha256": "sha256:1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d",
    "workflow": ".github/workflows/d972-r07-section-cochain-checker-completion-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "e": {
    "run": 33981657987,
    "attempt": 1,
    "head": "444c71c9e554ae8feb9c8ee54df57d3df19ed66f",
    "id": 9973974150,
    "name": "d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1",
    "bytes": 2816692,
    "sha256": "sha256:884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25",
    "workflow": ".github/workflows/d972-r07-selected-cycle-materializer-v1.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "prepare": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865061266,
    "name": "task554-grade1-v3-prepare-33677346616-1",
    "bytes": 204360988,
    "sha256": "sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-0": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865238399,
    "name": "task554-grade1-v3-state-block-0-33677346616-1",
    "bytes": 81729645,
    "sha256": "sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-1": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865242284,
    "name": "task554-grade1-v3-state-block-1-33677346616-1",
    "bytes": 82259824,
    "sha256": "sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-2": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865193269,
    "name": "task554-grade1-v3-state-block-2-33677346616-1",
    "bytes": 82200189,
    "sha256": "sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "block-3": {
    "run": 33677346616,
    "attempt": 1,
    "head": "22c6dddb43d107c05e65f53ad898823ae8ebe276",
    "id": 9865239848,
    "name": "task554-grade1-v3-state-block-3-33677346616-1",
    "bytes": 82266526,
    "sha256": "sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92",
    "workflow": ".github/workflows/d972-r07-a0-first-rung-grade1-v3.yml",
    "repository_id": 1312092366,
    "conclusion": "failure"
  },
  "p1": {
    "run": 33851744070,
    "attempt": 1,
    "head": "6673eb2ea15ca6022acc2ddc5a8a204a0380172f",
    "id": 9931437113,
    "name": "task809-canonical-p1-degree2-lift-v9-33851744070-1",
    "bytes": 641518300,
    "sha256": "sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c",
    "workflow": ".github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v9.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "task712": {
    "run": 33814194630,
    "attempt": 1,
    "head": "5ff2c5a30b604536df12acba8801828a5a7e5fe0",
    "id": 9915928157,
    "name": "d972-r07-grade2-maps-v4-33814194630-1",
    "bytes": 22404961,
    "sha256": "sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858",
    "workflow": ".github/workflows/d972-r07-grade2-maps-v4.yml",
    "repository_id": 1312092366,
    "conclusion": "success"
  },
  "continuation": {
    "run": 33990567016,
    "attempt": 1,
    "head": "c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70",
    "workflow": ".github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml",
    "id": 9977040548,
    "name": "d972-r07-complete-oracle-cegar-resume64-v1-candidate-33990567016-1",
    "bytes": 304642285,
    "sha256": "sha256:a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792",
    "repository_id": 1312092366,
    "conclusion": "success"
  }
}''')

ANCHOR_ENTRY_FILES = json.loads(r'''{
  "accepted-completion/checker-result.json": {
    "bytes": 176622,
    "sha256": "4ef33b2d174064e2542dd07d1c838b476b549606a8be0fb2ecc4b301b1382690"
  },
  "accepted-completion/completion-run-receipt.json": {
    "bytes": 5006,
    "sha256": "aaa5a9900d37f9d56e72419d7073da0bec291890e6ccf940109d01168e6e77f8"
  },
  "accepted-completion/coverage-receipt.json": {
    "bytes": 86586,
    "sha256": "e0ee8b681793567e422da95a6d73475ffc8e2c8b06e6d491938218336b6d7bad"
  },
  "accepted-completion/repair-source-receipt.json": {
    "bytes": 4137,
    "sha256": "3f2c68a359c3b9200f88850432372abd78207c1cfacc39a8aeb371e184774be8"
  },
  "accepted-completion/snapshot-isolation-selftest.json": {
    "bytes": 727,
    "sha256": "ac5c37d865ee8f85dc13ddbb78878071b7d6d6abbec827827190ccedc83337c0"
  },
  "all-parent-files-after.json": {
    "bytes": 593399,
    "sha256": "e89fe5fcac1ceb4bbc871d613774ac46ea00535536a891232eaf69af202d448c"
  },
  "all-parent-files-before.json": {
    "bytes": 593399,
    "sha256": "e89fe5fcac1ceb4bbc871d613774ac46ea00535536a891232eaf69af202d448c"
  },
  "before32/HEAD": {
    "bytes": 964,
    "sha256": "d489c06d40f1b06a8924558e8f751d08cd2b40259790de398b93c79f3657760b"
  },
  "before32/result.json": {
    "bytes": 28577,
    "sha256": "06c3053808179dd7706eb85fd30df8e1c360b5ee7f4640cd2a84581fe33a978a"
  },
  "checker-exit-code.txt": {
    "bytes": 2,
    "sha256": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"
  },
  "checker-result.json": {
    "bytes": 330955,
    "sha256": "ff55c51e90acead643b9683af6f82d492c503a92c83a504a97eeb3f62c31cc4d"
  },
  "checker-stdout.json": {
    "bytes": 330955,
    "sha256": "ff55c51e90acead643b9683af6f82d492c503a92c83a504a97eeb3f62c31cc4d"
  },
  "completion-intake-receipt.json": {
    "bytes": 4878,
    "sha256": "bbb04136ff7d2d53d7940969bb696869fd79cf983b8e23e3b7fb89a3fb333d07"
  },
  "copy-before-resume.json": {
    "bytes": 778467,
    "sha256": "1475c86bf11868a9611b8562d3aeca18afce14b86d741c208c04c332847110c8"
  },
  "live-parent-intake.json": {
    "bytes": 8509,
    "sha256": "ef88ea88a491837a8fe32e120e491191037ba5c168354fae1de1c52688d29180"
  },
  "output/fixed/manifest.json": {
    "bytes": 3159,
    "sha256": "3ec178df5c2af9de7c55bb96075bb9e741111a241f7e02222ef5604587c87c41"
  },
  "output/HEAD": {
    "bytes": 964,
    "sha256": "4614d5c3fc619007879f3a5062cde90ac0cab86552ddd17ff14306bc961ac2f4"
  },
  "output/invocations/2c723e694ab1425c91308e5281031d1d.json": {
    "bytes": 738,
    "sha256": "30ab799a0166bccca1e1bfc4e8bfb13ab0ebdf3bb9152a74afc20af7ed797421"
  },
  "output/invocations/654a02070b2e4a9a99698fd6080c6035.json": {
    "bytes": 737,
    "sha256": "e004e29cde9c88fc06a0ccdcc75ed8e484419a09344893d55eae3cf54b04c82b"
  },
  "output/invocations/c1f691934ec343f8ba2de4e2819d564f.json": {
    "bytes": 737,
    "sha256": "f9217280d1563a6a8c08cec0866d9ddd98b2851cc7817aa2d1041c6b6bce376f"
  },
  "output/owner.json": {
    "bytes": 8612,
    "sha256": "e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b"
  },
  "output/result.json": {
    "bytes": 42785,
    "sha256": "75f76ac43c86cfae998b0f4fe757a79b500727c2bfa847849fa57dbfa05293fd"
  },
  "output/source.json": {
    "bytes": 2423,
    "sha256": "c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651"
  },
  "output/start.json": {
    "bytes": 54707,
    "sha256": "87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b"
  },
  "preservation-result.json": {
    "bytes": 774326,
    "sha256": "178dc3c45a87fa848a94ed0a1c4e8b4074cb418b57892c74ffcda5197b743171"
  },
  "producer-output-before-checker.json": {
    "bytes": 774793,
    "sha256": "8ea7c0d5cdd0cef4bd7bf1beb9403041ca333a071fd4703fe90a656f993a9d02"
  },
  "producer-result.json": {
    "bytes": 42785,
    "sha256": "75f76ac43c86cfae998b0f4fe757a79b500727c2bfa847849fa57dbfa05293fd"
  },
  "resume-source-receipt.json": {
    "bytes": 4657,
    "sha256": "76c5cbd01fafb30e8ba503e27ae949f5a3e2dbb46e9108ca3d691d6d996369b0"
  },
  "run-receipt.json": {
    "bytes": 6883,
    "sha256": "ca9a42e10f207d2a57465ccdcf84b414d1a20b5170e04e38a645645fdb787694"
  },
  "source-receipt.json": {
    "bytes": 3643,
    "sha256": "3a50dd12025079a6089d15aac79573899e49692b61a53879adb9b0572342de6b"
  }
}''')

RETAINED_PRODUCER_PINS = json.loads(r'''{
  "search/d972_r07_complete_oracle_cegar_continuation_v1.py": [
    126940,
    "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"
  ],
  "search/d972_r07_selected_cycle_materializer_v1.py": [
    88929,
    "4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3"
  ],
  "search/d972_r07_section_cochain_oracle_v1.py": [
    73290,
    "4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb"
  ],
  "search/d972_r07_full_origin_refinement_v1.py": [
    97806,
    "d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa"
  ],
  "search/d972_r07_fixed_root_packet_loop_v2.py": [
    84173,
    "e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6"
  ],
  "search/d972_r07_actual_root_seed_materializer_v3.py": [
    86643,
    "36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332"
  ],
  "search/d972_r07_rank1355_root_seed_scalars_v1.py": [
    31578,
    "973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb"
  ],
  "search/d972_r07_actual_grade2_root_scalar_batch_v2.py": [
    118315,
    "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856"
  ],
  "search/d972_r07_targeted_grade2_owner_generated_join_v15.py": [
    126565,
    "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"
  ]
}''')

REGISTERED_RAW_PINS = json.loads(r'''{
  "scratchpad/a0_paper_words_v1.json": [
    115928,
    "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"
  ],
  "scratchpad/a0_v2_words.json": [
    106133,
    "fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"
  ],
  "scratchpad/fuda1_a0_rmax_data.g": [
    4709,
    "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"
  ]
}''')

# Root supplies the independently authored C closure as public metadata before release.
# No checker implementation is imported or read by this producer.
REGISTERED_CHECKER_PINS = json.loads(r'''{
  "search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py": [
    119619,
    "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6"
  ],
  "search/check_d972_r07_actual_root_seed_materializer_v3.py": [
    64626,
    "eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701"
  ],
  "search/check_d972_r07_complete_oracle_cegar_continuation_v2.py": [
    129557,
    "e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"
  ],
  "search/check_d972_r07_fixed_root_packet_loop_v2.py": [
    66251,
    "5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5"
  ],
  "search/check_d972_r07_full_origin_refinement_v1.py": [
    75083,
    "1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2"
  ],
  "search/check_d972_r07_rank1355_root_seed_scalars_v1.py": [
    36236,
    "f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62"
  ],
  "search/check_d972_r07_section_cochain_oracle_v1.py": [
    80740,
    "2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967"
  ],
  "search/check_d972_r07_section_cochain_oracle_v2.py": [
    84402,
    "a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d"
  ],
  "search/check_d972_r07_selected_cycle_materializer_v1.py": [
    103757,
    "a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4"
  ],
  "search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py": [
    141770,
    "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"
  ]
}''')
REGISTERED_RUNTIME = {"python": "3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]", "numpy": "2.5.1"}


def descriptor_list(pins: Any) -> list[Any]:
    return [{"file": name, "bytes": pair[0], "sha256": pair[1]} for name, pair in sorted(pins.items())]


def validate_input_inventory(value: Any) -> None:
    exact_keys(value, ("files", "directories"), "input_inventory_exact_keys")
    require(isinstance(value["files"], list) and isinstance(value["directories"], list), "input_inventory_lists")
    for item in value["files"]:
        pin_type(item)
    names = [item["file"] for item in value["files"]]
    directories = [safe_name(item) for item in value["directories"]]
    require(names == sorted(set(names)) and directories == sorted(set(directories)) and
            set(names).isdisjoint(directories), "input_inventory_sorted_unique_full_relative_POSIX")


def root_paths(args: Any) -> dict[str, Path]:
    require(len(args.block_root) == 4, "exact_four_block_roots")
    return {role: (args.block_root[int(role[-1])] if role.startswith("block-") else
                   getattr(args, role.replace("-", "_") + "_root")).resolve() for role in ROLES}


def checked_descriptor(root: Path, entry: Any, name: str | None = None) -> Any:
    pin_type(entry)
    require(name is None or entry["file"] == name, "registered_descriptor_path")
    require(file_pin(safe_file(root, entry["file"]), entry["file"]) == entry, "actual_whole_file_descriptor")
    return entry


def registered_policy() -> Any:
    return {"batch_size": BATCH_SIZE, "max_batches": MAX_BATCHES, "selection_policy": POLICY,
            "partial_policy": PARTIAL_POLICY, "refill": False,
            "producer_limits": {"max_seconds": 5400, "max_memory_mib": 7168},
            "checker_limits": {"max_seconds": 10800, "max_memory_mib": 7168}}


def authenticate_registration(value: Any, args: Any) -> None:
    expected = registered_policy()
    exact_keys(value, expected, "registered_policy_exact_keys")
    for key in ("batch_size", "max_batches"):
        require(integer(value[key]) and value[key] == expected[key], "strict_registered_batch_counts")
    require(value["refill"] is False and value["selection_policy"] == POLICY and
            value["partial_policy"] == PARTIAL_POLICY, "registered_no_refill_private_final_policy")
    for key in ("producer_limits", "checker_limits"):
        exact_keys(value[key], ("max_seconds", "max_memory_mib"), "registered_limit_keys")
        require(all(integer(number, 1) for number in value[key].values()) and value[key] == expected[key],
                "registered_limit_values")
    require(value == expected and integer(args.batch_size) and args.batch_size == BATCH_SIZE and
            integer(args.max_seconds) and integer(args.max_memory_mib) and
            value["producer_limits"] == {"max_seconds": args.max_seconds, "max_memory_mib": args.max_memory_mib},
            "actual_CLI_matches_registered_resource_and_batch")


def authenticate_code(code: Any) -> list[Any]:
    exact_keys(code, ("producer", "checker", "producer_dependencies", "checker_dependencies", "data"),
               "acceptance_code_exact_fields")
    checked_descriptor(PROJECT, code["producer"], "search/" + Path(__file__).name)
    checked_descriptor(PROJECT, code["checker"], "search/" + C_FILE)
    require(code["producer_dependencies"] == descriptor_list(RETAINED_PRODUCER_PINS),
            "retained_own_producer_exact_nine_closure")
    require(REGISTERED_CHECKER_PINS and code["checker_dependencies"] == descriptor_list(REGISTERED_CHECKER_PINS),
            "public_checker_closure_pins_required")
    require(code["data"] == descriptor_list(REGISTERED_RAW_PINS), "registered_actual_raw_union")
    union: dict[str, Any] = {}
    for entry in [code["producer"], code["checker"], *code["producer_dependencies"],
                  *code["checker_dependencies"], *code["data"]]:
        checked_descriptor(PROJECT, entry)
        require(entry["file"] not in union or union[entry["file"]] == entry, "no_conflicting_code_or_data_pin")
        union[entry["file"]] = copy.deepcopy(entry)
    return [union[name] for name in sorted(union)]


def authenticate_anchor_metadata(root: Path, anchor: Any, inv: Any) -> dict[str, Any]:
    names = {"head": "output/HEAD", "result": "output/result.json", "checker": "checker-result.json",
             "owner": "output/owner.json", "source": "output/source.json", "start": "output/start.json",
             "fixed": "output/fixed/manifest.json"}
    exact_keys(anchor, (*names, "invocations", "checker_prefix", "completed_steps", "rank", "generation",
               "kind", "state_head", "target_remainder_sha256", "lambda_sha256", "terminal"), "anchor_exact_keys")
    for name, pin in ANCHOR_ENTRY_FILES.items():
        require(file_pin(safe_file(root, name)) == pin, "registered_observed_anchor_entry:" + name)
    objects = {}
    for key, name in names.items():
        checked_descriptor(root, anchor[key], name)
        require((anchor[key]["bytes"], anchor[key]["sha256"]) == ANCHOR_FIXED_FILES[name], "anchor_fixed_seven_entry_pin")
        objects[key] = read_json(root, name)
        check_seal(objects[key])
    head, result, checked, start, source = (objects[name] for name in ("head", "result", "checker", "start", "source"))
    require(head["schema"] == "d972.r07.complete-oracle-cegar-continuation.v1.head" and
            checked["schema"] == "d972.r07.complete-oracle-cegar-continuation.v1.checker-result" and
            checked["status"] == "PASS" and checked["checker_sha256"] == LOOP_CHECKER_SHA and
            source["producer_sha256"] == L_SHA, "observed_saved_P971_Cv2_success")
    require({key: source[key] for key in ("python", "numpy")} == REGISTERED_RUNTIME ==
            {key: checked[key] for key in ("python", "numpy")}, "anchor_full_runtime_identity")
    for key, number in (("completed_steps", 64), ("rank", 1450), ("generation", 8155)):
        require(all(integer(value[key]) and value[key] == number for value in (anchor, head, result, checked)),
                "observed_anchor_strict_count:" + key)
    for key in ("kind", "state_head", "target_remainder_sha256", "lambda_sha256"):
        require(anchor[key] == head[key] == result[key] == checked[key], "anchor_head_result_checker:" + key)
    require(anchor["terminal"] == result["terminal"] == checked["terminal"] == "UNKNOWN_CAP" and
            head["kind"] == "Separator" and head["current_snapshot_sha256"] is None and
            head["current_checkpoint_sha256"] is None, "accepted_exact_current_64_no_partial_snapshot")
    for key, wanted in (("rank", 1386), ("generation", 8091), ("completed_steps", 0), ("external_e_attached", 1)):
        require(integer(start[key]) and start[key] == wanted, "original_start_strict_integer_not_bool:" + key)
    require(start["external_e_numerically_replayed"] is False, "old_external_E_not_numerically_replayed")
    for key in ("owner", "source", "start"):
        for value in (head, result, checked):
            require(value[key + "_sha256"] == anchor[key]["sha256"], "same_saved_owner_source_start")
    require(head["fixed_manifest_sha256"] == result["fixed_manifest_sha256"] ==
            checked["fixed_manifest_sha256"] == anchor["fixed"]["sha256"] and
            result["head_sha256"] == checked["head_sha256"] == anchor["head"]["sha256"] and
            checked["result_sha256"] == anchor["result"]["sha256"], "anchor_exact_final_file_chain")
    for key in ("all_new_committed_arrays_and_json_compared", "current_checkpoint_fully_compared",
                "full_four_character_scope", "ordinary27_actual_source", "all_four_B_summed_each_E"):
        require(checked[key] is True, "accepted_full_scope_flag:" + key)
    for key, number in (("prefix_steps_replayed", 64), ("section_equalities_each", P1_ROWS), ("chords_each", CHORDS),
            ("auxiliary_tests_each", 2), ("source_lower_trits_each_E", LOWER), ("literal_modulus", 54),
            ("external_e_attached", 1), ("old_scans_numerically_replayed", 0), ("old_inserts_numerically_replayed", 0),
            ("old_success_suites", 0)):
        require(integer(checked[key]) and checked[key] == number, "accepted_full_scope_count:" + key)
    require(result["lambda_rho2"] == checked["lambda_rho2"] and
            len(result["lambda_rho2"]["accepted_target_derivation_parents"]) == 97 and
            result["lambda_rho2"]["original_rho2_directly_read"] is False and
            result["lambda_rho2"]["mode"] == "derived" and result["lambda_rho2"]["value"] == 1,
            "entire_97_parent_derived_rho2_chain")
    prefix = anchor["checker_prefix"]
    exact_keys(prefix, ("steps", "snapshots", "steps_sha256", "snapshots_sha256", "invocations_sha256"),
               "checker_prefix_exact_keys")
    require(integer(prefix["steps"]) and integer(prefix["snapshots"]) and
            prefix["steps"] == prefix["snapshots"] == len(checked["steps"]) == len(checked["snapshots"]) == 64 and
            all(prefix[name + "_sha256"] == sha(canonical(checked[name])) for name in ("steps", "snapshots", "invocations")),
            "whole_saved_checker_prefix_lists")
    wanted_invocations = [item for item in inv["files"] if item["file"].startswith("output/invocations/")]
    require(anchor["invocations"] == wanted_invocations and len(wanted_invocations) == len(checked["invocations"]),
            "all_saved_invocation_files")
    actual_invocations = []
    for entry in wanted_invocations:
        checked_descriptor(root, entry)
        value = read_json(root, entry["file"])
        check_seal(value)
        require(value["schema"] == "d972.r07.complete-oracle-cegar-continuation.v1.invocation", "old_invocation_schema")
        actual_invocations.append({"sha256": entry["sha256"], **{key: item for key, item in value.items() if key != "sha256"}})
    require(sorted(actual_invocations, key=lambda value: value["sha256"]) ==
            sorted(checked["invocations"], key=lambda value: value["sha256"]), "all_saved_invocation_unsigned_fields")
    require(result["invocation_sha256"] in {item["sha256"] for item in actual_invocations}, "saved_result_actual_invocation")
    for value in (result, checked):
        require(value["cross_checked"] is False and value["verified"] is False and value["full_A0"] is False and
                value["grade2_member"] == value["grade2_nonmember"] == "NOT_DECIDED", "accepted_scope_not_upgraded")
    return objects


def authenticate_acceptance(args: Any) -> Any:
    value = json_bytes(args.acceptance.read_bytes())
    exact_keys(value, ("schema", "parents", "anchor", "code", "runtime", "registration"), "acceptance_six_plain_keys")
    require(value["schema"] == SCHEMA + ".acceptance", "new_batch_acceptance_schema")
    authenticate_registration(value["registration"], args)
    exact_keys(value["runtime"], ("python", "numpy"), "runtime_exact_keys")
    require(value["runtime"] == REGISTERED_RUNTIME == {"python": sys.version, "numpy": np.__version__},
            "actual_full_registered_runtime")
    paths, output = root_paths(args), args.output_root.resolve()
    require(not args.output_root.is_symlink() and isinstance(value["parents"], list) and
            len(value["parents"]) == len(ROLES), "fifteen_registered_roots")
    inventories, by_role = [], {}
    for role, item in zip(ROLES, value["parents"], strict=True):
        exact_keys(item, ("role", "path", "artifact", "files", "directories"), "parent_exact_keys")
        require(item["role"] == role and isinstance(item["path"], str) and Path(item["path"]).is_absolute() and
                Path(item["path"]).resolve() == paths[role] and not Path(item["path"]).is_symlink() and
                paths[role].is_dir(), "CLI_matches_actual_parent_root")
        artifact = item["artifact"]
        exact_keys(artifact, REGISTERED_ARTIFACTS[role], "exact_artifact_tuple_keys")
        require(all(integer(artifact[key], 1) for key in ("run", "attempt", "id", "bytes", "repository_id")) and
                artifact == REGISTERED_ARTIFACTS[role], "pre_registered_observed_artifact_tuple")
        root = paths[role]
        require(root != output and root not in output.parents and output not in root.parents,
                "separate_output_from_readonly_parent")
        for prior in by_role:
            require(root != paths[prior] and root not in paths[prior].parents and paths[prior] not in root.parents,
                    "disjoint_registered_parent_envelopes")
        expected = {key: item[key] for key in ("files", "directories")}
        validate_input_inventory(expected)
        observed = inventory(root)
        require(observed == expected, "all_actual_parent_files_bytes_and_directory_EOF:" + role)
        by_role[role] = observed
        inventories.append({"role": role, **copy.deepcopy(observed)})
        progress("admitted-parent", role=role, files=len(observed["files"]))
    code = authenticate_code(value["code"])
    objects = authenticate_anchor_metadata(paths["continuation"], value["anchor"], by_role["continuation"])
    portable = copy.deepcopy(value)
    for item in portable["parents"]:
        del item["path"]
    return {"acceptance": value, "portable": portable, "portable_sha256": sha(canonical(portable)),
        "acceptance_sha256": sha(args.acceptance.read_bytes()), "paths": paths,
        "parent_inventories": inventories, "inventories": by_role, "code_inventory": code, "anchor_objects": objects}

def accepted_oracle_top_metadata(l: Any, snapshot: Any, store: Any) -> Any:
    """Authenticate old A--D receipts without calling its mathematical restorers."""
    witness = store.values["tree"]["witness.json"]
    terminal = "VIOLATION_CANDIDATE"
    stages = {phase: store.hashes[index] for index, phase in enumerate(SELECTION_PHASES)}
    binding = store.binding
    expected_result = l.seal("oracle-result", {"status": "PASS", "terminal": terminal,
        **{key: binding[key] for key in ("owner_sha256", "source_sha256", "fixed_manifest_sha256", "snapshot_sha256")},
        **{key: snapshot[key] for key in ("step", "rank", "generation", "state_head", "lambda_sha256",
            "target_remainder_sha256", "lambda_rho2", "direct_pairing")},
        "stage_manifests": stages, "section_equalities": P1_ROWS, "chords_checked": CHORDS, "auxiliary_tests": 2,
        "witness_sha256": sha(canonical(witness)), "materialization": witness["materialization"],
        "new_physical_appends": 0, "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0,
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False, **ASSURANCE})
    expected_manifest = l.seal("oracle-manifest", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "fixed_manifest_sha256", "snapshot_sha256")},
        "stage_manifests": stages, "result_sha256": sha(canonical(expected_result)),
        "witness_sha256": sha(canonical(witness)), "terminal": terminal,
        "stage_eof": list(SELECTION_PHASES), **ASSURANCE})
    require(read_json(store.root, "oracle-result.json") == expected_result and
            read_json(store.root, "oracle-manifest.json") == expected_manifest,
            "saved_oracle_top_full_json_identity_without_numerical_replay")
    return {"oracle_result": expected_result, "oracle_manifest": expected_manifest, "tree": {"witness": witness}}


def parent_row_sources(admission: Any, state: Any) -> list[Any]:
    roots, all_inv = admission["paths"], admission["inventories"]
    result: list[Any] = []
    def append_file(role: str, name: str, *, many: bool = False) -> None:
        index = {item["file"]: item for item in all_inv[role]["files"]}
        require(name in index, "physical_parent_file_is_in_full_admitted_inventory")
        entry = index[name]
        require(entry["bytes"] > 0 and entry["bytes"] % PHYSICAL_BYTES == 0 and
                (many or entry["bytes"] == PHYSICAL_BYTES), "positioned_original_physical_file_width")
        with safe_file(roots[role], name).open("rb") as stream:
            for offset in range(0, entry["bytes"], PHYSICAL_BYTES):
                row = stream.read(PHYSICAL_BYTES)
                row_id = len(result)
                require(len(row) == PHYSICAL_BYTES and row_id < len(state["rows"]) and row == state["rows"][row_id],
                        "original_physical_ancestry_matches_insertion_row")
                result.append({"kind": "parent-row", "role": role, "file": name,
                    "file_bytes": entry["bytes"], "file_sha256": entry["sha256"], "offset": offset,
                    "length": PHYSICAL_BYTES, "row_sha256": sha(row)})
            require(stream.read(1) == b"", "positioned_parent_physical_EOF")
    append_file("state", "state/physical.bin", many=True)
    for role in ("delta", "seed34"):
        append_file(role, "output/physical-normalized.bin")
    for role in ("packet", "refinement"):
        head = read_json(roots[role], "output/HEAD")
        require(integer(head["completed_steps"], 1), "accepted_parent_completed_physical_steps")
        for step in range(1, head["completed_steps"] + 1):
            append_file(role, f"output/steps/{step:06d}/physical-normalized.bin")
    append_file("e", "output/physical-normalized.bin")
    for ordinal in range(admission["acceptance"]["anchor"]["completed_steps"]):
        append_file("continuation", f"output/snapshots/{ordinal:06d}/e/physical/physical-normalized.bin")
    require(len(result) == state["rank"], "all_original_parent_rows_have_exact_ancestry")
    return result


def thin_anchor(l: Any, e: Any, oracle: Any, refinement: Any, p2: Any, m: Any, base: Any,
                descriptors: Any, args: Any, admission: Any) -> Any:
    bundle = l.boot(e, oracle, refinement, p2, m, base, descriptors, args)
    state = bundle["state"]
    output = admission["paths"]["continuation"] / "output"
    old = admission["anchor_objects"]
    owner, source, start = l.loop_owner(bundle), l.loop_source(e, oracle, refinement, p2, bundle), l.loop_start(bundle)
    require(owner == old["owner"] and source == old["source"] and start == old["start"],
            "same_original_source_owner_start_from_actual_fourteen_parents")
    require(state["completed_steps"] == 0 and state["rank"] == 1386 and state["generation"] == 8091 and
            sha(state["target_raw"]) == start["target_remainder_sha256"], "original_external_E_start_not_renamed")
    previous_target = bytes(state["target_raw"])
    binding = {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)),
        "start_sha256": sha(canonical(start)), "fixed_manifest_sha256": None}
    require((output / "fixed/manifest.json").is_file(), "accepted_fixed_bundle_must_already_exist")
    fixed = l.FixedBundle(e, oracle, base, bundle, output, binding)
    binding["fixed_manifest_sha256"] = fixed.digest
    try:
        require(fixed.digest == admission["acceptance"]["anchor"]["fixed"]["sha256"], "accepted_fixed_exact_file")
        l.validate_output_directory(output, 64)
        l.validate_invocations(output, binding)
        require({path.name for path in (output / "snapshots").iterdir()} == {f"{i:06d}" for i in range(64)} and
                {path.name for path in (output / "steps").iterdir()} == {f"{i:06d}" for i in range(1, 65)},
                "accepted_exact_64_snapshot_and_step_directories")
        checked = old["checker"]
        for ordinal in range(64):
            snapshot, saved = l.snapshot_store(e, oracle, output, state, binding, create=False)
            require(len(saved.hashes) == 9, "accepted_all_nine_completed_phases")
            answer = accepted_oracle_top_metadata(l, snapshot, saved)
            values, raws = saved.values["physical"], saved.raws["physical"]
            row = {"instruction": values["instruction.json"], "result": values["result.json"],
                   "normalized": raws["physical-normalized.bin"], "target": raws["target-remainder.bin"],
                   "lambda": raws.get("lambda.bin")}
            answer["row"] = row
            manifest = read_json(output, f"steps/{ordinal + 1:06d}/manifest.json")
            require(manifest == l.step_manifest(state, binding, snapshot, saved, answer), "saved_step_full_manifest_chain")
            l.validate_checkpoints(saved, answer)
            c_snapshot, c_step = checked["snapshots"][ordinal], checked["steps"][ordinal]
            require(c_snapshot["step"] == ordinal and c_step["step"] == ordinal + 1 and
                    c_snapshot["snapshot_sha256"] == sha(canonical(snapshot)) and
                    c_snapshot["oracle_manifest_sha256"] == sha(canonical(answer["oracle_manifest"])) and
                    c_snapshot["oracle_terminal"] == "VIOLATION_CANDIDATE" and
                    c_snapshot["phase_manifests"] == manifest["phase_manifests"] and
                    c_step["manifest_sha256"] == sha(canonical(manifest)), "accepted_C_complete_snapshot_actual_files")
            require(all(c_step[key] == manifest[key] for key in ("rank", "generation", "state_head")) and
                    c_step["selected_scalar"] == row["result"]["selected_scalar"] and
                    c_step["target_scalar"] == row["result"]["target"]["scalar"],
                    "accepted_C_step_count_state_and_target_scalar")
            l.attach_step(e, oracle, state, manifest, row)
            # Completed old sections, cochains, raw words and insert solves are never called.
            del saved, answer, row, values, raws, snapshot
            check_deadline("thin_saved_physical_step")
        require(l.head_value(state, binding) == old["head"] and l.current_derived(state) == old["result"]["lambda_rho2"] ==
                old["checker"]["lambda_rho2"] and len(state["target_parents"]) == 97,
                "thin_all_64_and_97_target_parents_match_actual_final_receipts")
        row_sources = parent_row_sources(admission, state)
        direct = m.check_final_separator(state["lambda"], state["rows"], previous_target, state["target_raw"])
        require(integer(direct["rows"]) and direct["rows"] == state["rank"] == 1450 and
                direct["lambda_pivots"] == 0 and direct["lambda_parent_remainder"] == direct["lambda_new_remainder"] == 1,
                "selection_lambda_all_anchor_rows_and_original_start_current_targets")
        state["previous_target_raw"] = previous_target
        state["direct_pairing"] = direct
        return {"bundle": bundle, "state": state, "fixed": fixed, "row_sources": row_sources, "old_binding": binding,
                "old_owner": owner, "old_source": source, "old_start": start, "direct_pairing": direct}
    except Exception:
        fixed.close()
        raise


def outer_metadata(admission: Any, intake: Any) -> Any:
    acceptance, portable, state = admission["acceptance"], admission["portable"], intake["state"]
    code = acceptance["code"]
    layout = seal("parent-layout", {"portable_acceptance_sha256": admission["portable_sha256"],
        **{key: portable[key] for key in ("parents", "anchor", "code", "runtime", "registration")}})
    source = seal("source", {"producer": code["producer"], "retained_producer_dependencies": code["producer_dependencies"],
        "checker": code["checker"], "retained_checker_dependencies": code["checker_dependencies"], "data": code["data"],
        "runtime": acceptance["runtime"], "formula_id": FORMULA, "retained_TCB_independence_reproved": False})
    layout_sha, source_sha = sha(canonical(layout)), sha(canonical(source))
    owner = seal("owner", {"formula_id": FORMULA, "scope": SCOPE, "parent_layout_sha256": layout_sha,
        "source_sha256": source_sha, "portable_acceptance_sha256": admission["portable_sha256"],
        "registration": acceptance["registration"]})
    owner_sha = sha(canonical(owner))
    start = seal("start", {"owner_sha256": owner_sha, "source_sha256": source_sha,
        "parent_layout_sha256": layout_sha, "anchor_head_sha256": acceptance["anchor"]["head"]["sha256"],
        "anchor_result_sha256": acceptance["anchor"]["result"]["sha256"],
        "anchor_checker_sha256": acceptance["anchor"]["checker"]["sha256"],
        "anchor_completed_steps": state["completed_steps"], "rank": state["rank"], "generation": state["generation"],
        "kind": "Separator", "state_head": state["head"], "target_remainder_sha256": sha(state["target_raw"]),
        "previous_target_remainder_sha256": sha(state["previous_target_raw"]),
        "selection_lambda_sha256": sha(state["lambda_raw"]), "original_rho2_packed_sha256": state["original_rho2_sha256"],
        "accepted_target_derivation_parents": state["target_parents"], "anchor_pairing": intake["direct_pairing"],
        "anchor_pairing_rows": state["rank"], "old_snapshot_numeric_replays": 0, "old_insert_numeric_replays": 0,
        "external_e_attached": 1, "registration": acceptance["registration"]})
    start_sha = sha(canonical(start))
    old_fixed = intake["fixed"]
    entries = []
    for entry in old_fixed.manifest["files"]:
        exact_keys(entry, ("file", "bytes", "sha256", "dtype", "shape"), "retained_fixed_five_key_descriptor")
        if entry["dtype"] == "json":
            require(entry["shape"] is None, "retained_fixed_JSON_null_shape")
            projected = {key: entry[key] for key in ("file", "bytes", "sha256")}
            pin_type(projected)
        else:
            projected = copy.deepcopy(entry)
            pin_type(projected, binary=True)
        entries.append(projected)
    fixed_manifest = seal("fixed-manifest", {"owner_sha256": owner_sha, "source_sha256": source_sha,
        "start_sha256": start_sha, "accepted_fixed_manifest": acceptance["anchor"]["fixed"],
        "accepted_geometry_stage_sha256": intake["bundle"]["accepted_oracle"]["stages"]["geometry"],
        "files": entries, "fixed_values_independent_of_lambda": True})
    fixed_sha = sha(canonical(fixed_manifest))
    selection_start = seal("selection-start", {"owner_sha256": owner_sha, "source_sha256": source_sha,
        "start_sha256": start_sha, "fixed_manifest_sha256": fixed_sha,
        "anchor_completed_steps": state["completed_steps"], "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "target_remainder_sha256": sha(state["target_raw"]),
        "previous_target_remainder_sha256": sha(state["previous_target_raw"]),
        "selection_lambda_sha256": sha(state["lambda_raw"]), "selection_policy": POLICY,
        "batch_size": BATCH_SIZE, "max_batches": MAX_BATCHES})
    return {"parent-layout.json": layout, "source.json": source, "owner.json": owner, "start.json": start,
        "fixed/manifest.json": fixed_manifest, "selection/start.json": selection_start}

def binding_from_metadata(metadata: Any) -> Any:
    return {"owner_sha256": sha(canonical(metadata["owner.json"])),
        "source_sha256": sha(canonical(metadata["source.json"])), "start_sha256": sha(canonical(metadata["start.json"])),
        "fixed_manifest_sha256": sha(canonical(metadata["fixed/manifest.json"])),
        "selection_start_sha256": sha(canonical(metadata["selection/start.json"]))}


def phase_roster(l: Any, e: Any, phase: str, values: Any) -> Any:
    if phase in ("section", "cochain", "raw", "source", "primal", "p1", "B"):
        return l.registered_phase_roster(e, phase, values)
    if phase == "tree":
        count = values["tree.json"]["residual_nonzero"]
        require(integer(count, 0, CHORDS), "tree_full_failed_count")
        return {"potential-f.u8": ("u8", [N]), "potential-tau.u8": ("u8", [N, 5]),
            "chord-values.u8": ("u8", [CHORDS]), "chord-tau.u8": ("u8", [CHORDS, 5]),
            "chord-residuals.u8": ("u8", [CHORDS]), "selected-chords.u32": ("u32le", [5]),
            "fit.u8": ("u8", [5]), "basis-tau.u8": ("u8", [5, 5]),
            "failed-indices.u32": ("u32le", [count]), "failed-edges.u32": ("u32le", [count]),
            "tree.json": ("json", None), "witness-roster.json": ("json", None), "telemetry.json": ("json", None)}
    require(phase == "reduction", "registered_new_phase")
    rank = values["reduction.json"]["rank_before"]
    require(integer(rank, 0, PHYSICAL), "reduction_before_rank")
    roster = {"coefficients.u8": ("u8", [rank]), "physical-remainder.bin": ("packed3", [PHYSICAL]),
        "target-before.bin": ("packed3", [PHYSICAL]), "target-remainder.bin": ("packed3", [PHYSICAL]),
        "physical-literal.json": ("json", None), "reduction.json": ("json", None), "telemetry.json": ("json", None)}
    outcome = values["reduction.json"]["outcome"]
    require(outcome in ("INDEPENDENT", "DEPENDENT"), "reduction_typed_outcome")
    if outcome == "INDEPENDENT":
        roster.update({"physical-normalized.bin": ("packed3", [PHYSICAL]),
                       "instruction.json": ("json", None), "target.json": ("json", None)})
    return roster


def payload(value: Any, dtype: str, shape: list[int] | None = None) -> tuple[bytes, str, Any]:
    if isinstance(value, bytes):
        require(dtype != "json" and shape is not None, "raw_binary_has_explicit_shape")
        decode_array(value, dtype, shape)
        return value, dtype, list(shape)
    return encode_array(value, dtype, shape)


def serialize_arrays(arrays: Any) -> Any:
    return {name: payload(value, dtype) for name, (value, dtype) in arrays.items()}


def payload_descriptor(name: str, raw: bytes, dtype: str, shape: Any) -> Any:
    entry = {"file": safe_name(name), "bytes": len(raw), "sha256": sha(raw)}
    if dtype != "json":
        entry.update({"dtype": dtype, "shape": shape})
    pin_type(entry, binary=dtype != "json")
    return entry


def atomic_diagnostic(path: Path, names: Iterable[str]) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    return any(re.fullmatch(r"\." + re.escape(name) + r"\.pending-[0-9a-f]{32}", path.name) is not None for name in names)


def phase_manifest_body(binding: Any, phase: str, previous: str | None, selection_sha: str | None,
                        ordinal: int | None, witness_sha: str | None, files: Any) -> Any:
    return {**binding, "selection_sha256": selection_sha, "candidate_ordinal": ordinal,
        "witness_sha256": witness_sha, "phase": phase, "previous_phase_manifest_sha256": previous,
        "files": files, "eof": True}


class BatchPhaseStore:
    """A completed phase is immutable; the private HEAD selects its published prefix."""
    def __init__(self, l: Any, e: Any, root: Path, binding: Any, *,
                 selection_sha: str | None = None, ordinal: int | None = None,
                 witness_sha: str | None = None, initial_previous: str | None = None):
        self.l, self.e, self.root, self.binding = l, e, root, copy.deepcopy(binding)
        self.selection_sha, self.ordinal, self.witness_sha = selection_sha, ordinal, witness_sha
        self.initial_previous = initial_previous
        self.phases = SELECTION_PHASES if ordinal is None else CANDIDATE_PHASES
        self.values: dict[str, Any] = {}
        self.raws: dict[str, Any] = {}
        self.manifests: dict[str, Any] = {}
        self.hashes: dict[str, str] = {}

    def directory(self, phase: str) -> Path:
        require(phase in self.phases, "phase_in_current_store_scope")
        return self.root / phase if self.ordinal is None or phase == "reduction" else self.root / "e" / phase

    def previous(self) -> str | None:
        return self.hashes[self.phases[len(self.hashes) - 1]] if self.hashes else self.initial_previous

    def accept(self, phase: str, manifest: Any, values: Any, raws: Any) -> None:
        require(phase == self.phases[len(self.hashes)], "strict_completed_phase_prefix")
        check_seal(manifest, "phase-manifest")
        roster = phase_roster(self.l, self.e, phase, values)
        require([item["file"] for item in manifest["files"]] == sorted(roster), "complete_exact_registered_phase_roster")
        for entry in manifest["files"]:
            dtype, shape = roster[entry["file"]]
            require(entry == payload_descriptor(entry["file"], raws[entry["file"]], dtype, shape),
                    "phase_descriptor_dtype_shape_and_full_hash")
        require(manifest == seal("phase-manifest", phase_manifest_body(self.binding, phase, self.previous(),
                    self.selection_sha, self.ordinal, self.witness_sha, manifest["files"])),
                "phase_exact_same_owner_start_selection_witness_and_predecessor")
        validate_telemetry(values["telemetry.json"], phase,
                           sum(len(raw) for name, raw in raws.items() if name != "telemetry.json"))
        self.values[phase], self.raws[phase] = values, raws
        self.manifests[phase], self.hashes[phase] = manifest, sha(canonical(manifest))

    def load(self) -> None:
        gap = False
        for phase in self.phases:
            root = self.directory(phase)
            if not root.exists():
                gap = True
                continue
            require(not gap and root.is_dir() and not root.is_symlink(), "no_phase_hole_or_wrong_directory_type")
            manifest = read_json(root, "manifest.json", "phase-manifest")
            require(isinstance(manifest["files"], list), "phase_files_list")
            names = [item["file"] for item in manifest["files"]]
            require(names == sorted(set(names)) and all(Path(name).name == name for name in names),
                    "phase_basename_roster")
            values, raws = {}, {}
            for entry in manifest["files"]:
                binary = "dtype" in entry
                pin_type(entry, binary=binary)
                raw = safe_file(root, entry["file"]).read_bytes()
                require(len(raw) == entry["bytes"] and sha(raw) == entry["sha256"], "saved_phase_full_payload_pin")
                dtype, shape = (entry["dtype"], entry["shape"]) if binary else ("json", None)
                values[entry["file"]], raws[entry["file"]] = decode_array(raw, dtype, shape), raw
            allowed = {*names, "manifest.json"}
            require(all((path.name in allowed and path.is_file() and not path.is_symlink()) or
                        atomic_diagnostic(path, allowed) for path in root.iterdir()), "phase_full_EOF_and_named_atomic_tail")
            self.accept(phase, manifest, values, raws)
            check_deadline("load_new_completed_phase:" + phase)

    def commit(self, phase: str, payloads: Any, begun: float, measurement: Any) -> None:
        require(phase == self.phases[len(self.hashes)] and not self.directory(phase).exists(),
                "publish_only_next_fresh_phase")
        payloads = dict(payloads)
        require("telemetry.json" not in payloads, "reserved_new_phase_telemetry")
        root = self.directory(phase)
        root.parent.mkdir(parents=True, exist_ok=True)
        pending = root.parent / (".pending-" + phase + "-" + uuid.uuid4().hex)
        pending.mkdir()
        files, values, raws = [], {}, {}
        for name in sorted(payloads):
            raw, dtype, shape = payloads[name]
            require(Path(name).name == name, "phase_payload_basename")
            values[name], raws[name] = decode_array(raw, dtype, shape), raw
            atomic_write(pending, name, raw)
            files.append(payload_descriptor(name, raw, dtype, shape))
            check_deadline("prepare_phase_payload:" + phase)
        telemetry = phase_telemetry(phase, begun, measurement, sum(len(raw) for raw in raws.values()))
        raw = canonical(telemetry)
        atomic_write(pending, "telemetry.json", raw)
        files.append(payload_descriptor("telemetry.json", raw, "json", None))
        values["telemetry.json"], raws["telemetry.json"] = telemetry, raw
        files.sort(key=lambda entry: entry["file"])
        manifest = seal("phase-manifest", phase_manifest_body(self.binding, phase, self.previous(),
            self.selection_sha, self.ordinal, self.witness_sha, files))
        atomic_write(pending, "manifest.json", canonical(manifest))
        # Authenticate all typed payloads before making the completed phase visible.
        self.accept(phase, manifest, values, raws)
        check_deadline("before_phase_publication:" + phase)
        os.rename(pending, root)
        sync_directory(root.parent)
        # No cooperative stop between durable phase and its metadata/checkpoint publication.

    def ensure(self, phase: str, builder: Callable[[], Any]) -> bool:
        if phase in self.hashes:
            return False
        require(phase == self.phases[len(self.hashes)], "ensure_next_phase_only")
        check_deadline("before_fresh_phase_builder:" + phase)
        begun, measurement = time.monotonic(), process_measurement()
        self.commit(phase, builder(), begun, measurement)
        return True


def tree_payloads(oracle: Any, fixed: Any, cochain: Any, binding: Any) -> Any:
    numeric = current_batch_tree(oracle, fixed, cochain)
    selected = numeric["selection"]
    witnesses = [seal("witness", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "ordinal": ordinal, "selection_policy": POLICY, **fields})
        for ordinal, fields in enumerate(selected["witnesses"])]
    metadata = seal("tree", {"vertices": N, "tree_edges": N - 1, "chords": CHORDS,
        "independent_tau_columns": 5, "basis_chords": selected["basis_edges"],
        "fit": selected["fit"].tolist(), "aux_values": selected["auxiliary"].tolist(),
        "first_failed_index": selected["first_failed_index"], "first_failed_edge": selected["first_failed_edge"],
        "residual_nonzero": selected["failed_count"], "full_chord_eof": True, "selection_policy": POLICY})
    roster = seal("witness-roster", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")}, "witnesses": witnesses, "eof": True})
    return serialize_arrays({"potential-f.u8": (numeric["potential"], "u8"),
        "potential-tau.u8": (fixed.values["potential-tau.u8"], "u8"), "chord-values.u8": (numeric["values"], "u8"),
        "chord-tau.u8": (numeric["tau"], "u8"), "chord-residuals.u8": (numeric["residuals"], "u8"),
        "selected-chords.u32": (fixed.values["selected-chords.u32"], "u32le"), "fit.u8": (numeric["fit"], "u8"),
        "basis-tau.u8": (selected["basis_tau"], "u8"), "failed-indices.u32": (selected["failed_indices"], "u32le"),
        "failed-edges.u32": (selected["failed_edges"], "u32le"), "tree.json": (metadata, "json"),
        "witness-roster.json": (roster, "json")})


def saved_selection_values(oracle: Any, fixed: Any, store: BatchPhaseStore, cochain: Any) -> Any:
    """Check saved roster identities; never solve d or integrate the completed tree again."""
    require(list(store.hashes) == list(SELECTION_PHASES), "complete_selection_three_phases")
    values, binding = store.values["tree"], store.binding
    metadata, roster = values["tree.json"], values["witness-roster.json"]
    check_seal(metadata, "tree")
    check_seal(roster, "witness-roster")
    require(np.array_equal(values["potential-tau.u8"], fixed.values["potential-tau.u8"]) and
            np.array_equal(values["chord-tau.u8"], fixed.values["chord-tau.u8"]) and
            np.array_equal(values["selected-chords.u32"], fixed.values["selected-chords.u32"]),
            "restored_same_lambda_independent_geometry_and_carry")
    chords, residuals, tau, scores = (fixed.geometry["chords"], values["chord-residuals.u8"],
                                    values["chord-tau.u8"], values["chord-values.u8"])
    basis = np.searchsorted(chords, values["selected-chords.u32"]).astype(np.int64).tolist()
    failed = np.flatnonzero(residuals).astype(np.uint32)
    auxiliary = cochain["b_aux"]
    aux_hits = np.flatnonzero(auxiliary)
    count = min(BATCH_SIZE, len(failed)) if len(failed) else int(len(aux_hits) > 0)
    require(np.array_equal(values["failed-indices.u32"], failed) and
            np.array_equal(values["failed-edges.u32"], chords[failed]) and
            np.array_equal(values["basis-tau.u8"], tau[basis]) and
            np.array_equal((scores.astype(np.int16) - tau.astype(np.int32) @ values["fit.u8"].astype(np.int32)) % 3,
                           residuals), "saved_full_residual_roster_identity")
    witnesses = roster["witnesses"]
    require(isinstance(witnesses, list) and len(witnesses) == count and
            roster == seal("witness-roster", {**{key: binding[key] for key in
                ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
                "witnesses": witnesses, "eof": True}), "saved_same_start_exact_selected_witness_roster")
    basis_edges = [int(chords[index]) for index in basis]
    keys = ("schema", "sha256", "owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256",
            "ordinal", "selection_policy", "kind", "roster_index", "edge", "coordinate", "failed_chord",
            "basis_chords", "basis_coefficients", "cycles", "eta", "tau", "scalar", "materialization")
    for ordinal, witness in enumerate(witnesses):
        check_seal(witness, "witness")
        exact_keys(witness, keys, "saved_witness_exact_fields")
        require(all(witness[key] == binding[key] for key in
                    ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")) and
                integer(witness["ordinal"]) and witness["ordinal"] == ordinal and witness["selection_policy"] == POLICY and
                witness["materialization"] == "MATERIALIZATION_PENDING" and
                witness["tau"] == [0] * 5 and all(trit(value) for value in witness["tau"]) and
                integer(witness["scalar"], 1, 2), "saved_witness_bound_and_typed")
        require(isinstance(witness["eta"], list) and len(witness["eta"]) == 2 and
                all(trit(value) for value in witness["eta"]) and isinstance(witness["basis_chords"], list) and
                all(integer(edge, 0, EDGES - 1) for edge in witness["basis_chords"]) and
                isinstance(witness["cycles"], list), "saved_witness_nested_integer_lists")
        for cycle in witness["cycles"]:
            exact_keys(cycle, ("edge", "coefficient"), "saved_cycle_exact_keys")
            require(integer(cycle["edge"], 0, EDGES - 1) and trit(cycle["coefficient"]),
                    "saved_cycle_strict_edge_and_trit")
        if len(failed):
            require(all(integer(witness[key], 0, CHORDS - 1 if key == "roster_index" else EDGES - 1)
                        for key in ("roster_index", "edge", "failed_chord")), "saved_chord_strict_roster_and_edge")
            index = int(failed[ordinal])
            coefficients = witness["basis_coefficients"]
            require(isinstance(coefficients, list) and len(coefficients) == 5 and all(trit(x) for x in coefficients),
                    "saved_five_basis_coefficients")
            require(witness["kind"] == "chord" and witness["roster_index"] == index and
                    witness["edge"] == witness["failed_chord"] == int(chords[index]) and witness["coordinate"] is None and
                    witness["basis_chords"] == basis_edges and witness["eta"] == [0, 0] and
                    witness["cycles"] == [{"edge": int(chords[index]), "coefficient": 1}] +
                        [{"edge": basis_edges[j], "coefficient": (-coefficients[j]) % 3} for j in range(5)] and
                    witness["scalar"] == int(residuals[index]), "saved_full_ordered_six_cycles")
            # Check the stored coefficient identity without recomputing the solve.
            require(np.array_equal(tau[basis].T.astype(np.int32) @ np.asarray(coefficients, dtype=np.int32) % 3, tau[index]) and
                    (int(scores[index]) - sum(coefficients[j] * int(scores[basis[j]]) for j in range(5))) % 3 ==
                        witness["scalar"], "saved_six_cycle_tau_and_scalar_identity")
        else:
            coordinate = int(aux_hits[0])
            require(integer(witness["coordinate"], 0, 1), "saved_aux_strict_coordinate")
            require(witness["kind"] == "auxiliary" and witness["coordinate"] == coordinate and
                    all(witness[key] is None for key in ("roster_index", "edge", "failed_chord")) and
                    all(witness[key] == [] for key in ("basis_chords", "basis_coefficients", "cycles")) and
                    witness["eta"] == [int(j == coordinate) for j in range(2)] and
                    witness["scalar"] == int(auxiliary[coordinate]), "saved_first_aux_only_when_all_chords_zero")
    selected = {"terminal": "VIOLATION_CANDIDATE" if witnesses else "COMPLETE_ZERO_CANDIDATE",
        "failed_indices": failed, "failed_edges": chords[failed], "failed_count": int(len(failed)),
        "first_failed_index": int(failed[0]) if len(failed) else None,
        "first_failed_edge": int(chords[failed[0]]) if len(failed) else None, "basis_edges": basis_edges,
        "basis_tau": values["basis-tau.u8"], "fit": values["fit.u8"], "auxiliary": auxiliary}
    require(metadata == seal("tree", {"vertices": N, "tree_edges": N - 1, "chords": CHORDS,
        "independent_tau_columns": 5, "basis_chords": basis_edges, "fit": selected["fit"].tolist(),
        "aux_values": auxiliary.tolist(), "first_failed_index": selected["first_failed_index"],
        "first_failed_edge": selected["first_failed_edge"], "residual_nonzero": selected["failed_count"],
        "full_chord_eof": True, "selection_policy": POLICY}), "restored_complete_tree_metadata")
    return {"selection": selected, "witnesses": copy.deepcopy(witnesses)}

def publish_selection(output: Path, store: BatchPhaseStore, decoded: Any, state: Any, *,
                      documents: dict[str, bytes] | None = None) -> Any:
    def retain(name: str, raw: bytes) -> None:
        if documents is None:
            write_once(output, name, raw)
        else:
            require(name not in documents or documents[name] == raw, "selection_document_identity")
            documents[name] = raw
    binding, witnesses, selected = store.binding, decoded["witnesses"], decoded["selection"]
    rows = []
    for ordinal, witness in enumerate(witnesses):
        name = f"candidates/{ordinal:06d}/witness.json"
        raw = canonical(witness)
        retain(name, raw)
        rows.append({key: witness[key] for key in ("ordinal", "kind", "roster_index", "edge", "coordinate", "scalar")} |
                    {"witness": payload_descriptor(name, raw, "json", None)})
    files = {entry["file"]: entry for entry in store.manifests["tree"]["files"]}
    selection = seal("selection", {**binding, "phase_manifests": dict(store.hashes), "selection_policy": POLICY,
        "batch_size": BATCH_SIZE, "max_batches": MAX_BATCHES, "refill": False, "chords_checked": CHORDS,
        "auxiliary_tests": 2, "failed_count": selected["failed_count"], "first_failed_index": selected["first_failed_index"],
        "first_failed_edge": selected["first_failed_edge"], "failed_indices": files["failed-indices.u32"],
        "failed_edges": files["failed-edges.u32"], "selected_count": len(rows), "selected": rows,
        "aux_values": selected["auxiliary"].tolist(), "basis_chords": selected["basis_edges"],
        "basis_tau": selected["basis_tau"].tolist(), "fit": selected["fit"].tolist(),
        "terminal": selected["terminal"], "eof": True})
    retain("selection/selection.json", canonical(selection))
    selection_sha = sha(canonical(selection))
    for ordinal, witness in enumerate(witnesses):
        view = seal("oracle-view", {**binding, "selection_sha256": selection_sha, "ordinal": ordinal,
            "witness_sha256": sha(canonical(witness)), "geometry_manifest_sha256": binding["fixed_manifest_sha256"],
            "phase_manifests": dict(store.hashes), "anchor_state_head": state["head"],
            "selection_lambda_sha256": sha(state["lambda_raw"]), "terminal": "VIOLATION_CANDIDATE"})
        retain(f"candidates/{ordinal:06d}/oracle-view.json", canonical(view))
    return selection

def reduction_payloads(binding: Any, selection_sha: str, ordinal: int, witness_sha: str, state: Any,
                       corrected: Any, numeric: Any, selection_scalar: int) -> Any:
    coefficients = numeric["coefficients"]
    ordered = [{"row_id": index, "source": copy.deepcopy(state["row_sources"][index]),
                "lead": state["leads"][index], "coefficient": int(coefficients[index])}
               for index in range(state["rank"])]
    independent = numeric["outcome"] == "INDEPENDENT"
    literal = seal("physical-literal", {"candidate_ordinal": ordinal, "selection_sha256": selection_sha,
        "witness_sha256": witness_sha, "source_correction_sha256": sha(canonical(corrected["record"])),
        "p1_roots_sha256": sha(canonical(corrected["roots"])),
        "physical_factors": [{"row_id": item["row_id"], "source": item["source"], "coefficient": item["coefficient"],
                              "exponent": -signrep(item["coefficient"])} for item in ordered],
        "outer_exponent": signrep(numeric["sigma"]) if independent else None,
        "physical_lower_zero": True, "source_lower_zero": "NOT_ASSERTED", "normalized_word_available": independent})
    target, instruction = None, None
    if independent:
        target = {"parent_remainder_sha256": sha(state["target_raw"]), "remainder_sha256": sha(numeric["target"]),
                  "scalar": numeric["target_scalar"]}
        body = {"predecessor": state["head"], "offer": state["generation"], "global_row_id": state["rank"],
            "rank": state["rank"] + 1, "generation": state["generation"] + 1,
            "lead": numeric["lead"], "sigma": numeric["sigma"], "physical_offset": state["rank"] * PHYSICAL_BYTES,
            "local_row_offset": state["accepted_new_rows"], "candidate_ordinal": ordinal,
            "selection_sha256": selection_sha, "witness_sha256": witness_sha,
            "physical_sha256": sha(numeric["normalized"]), "literal_sha256": sha(canonical(literal)),
            "target_sha256": sha(canonical(target)), "target_scalar": numeric["target_scalar"],
            "coefficients_sha256": sha(coefficients.tobytes())}
        instruction = seal("physical-instruction", {**body,
            "rolling_sha256": sha(bytes.fromhex(state["head"]) + canonical(body))})
    reduction = seal("reduction", {"candidate_ordinal": ordinal, "selection_sha256": selection_sha,
        "witness_sha256": witness_sha, "selection_scalar": selection_scalar,
        "raw_pairing": numeric["raw_pairing"], "remainder_pairing": numeric["remainder_pairing"],
        "subtracted_new_pairing": numeric["subtracted_new_pairing"], "rank_before": state["rank"],
        "generation_before": state["generation"], "parent_state_head": state["head"],
        "target_before_sha256": sha(state["target_raw"]), "coefficients_sha256": sha(coefficients.tobytes()),
        "ordered_reductions": ordered, "remainder_sha256": sha(numeric["remainder"]), "remainder_zero": not independent,
        "outcome": numeric["outcome"], "lead": numeric["lead"], "sigma": numeric["sigma"],
        "normalized_sha256": sha(numeric["normalized"]) if independent else None, "target_scalar": numeric["target_scalar"],
        "target_after_sha256": sha(numeric["target"]), "rank_after": state["rank"] + int(independent),
        "generation_after": state["generation"] + int(independent),
        "state_head": instruction["rolling_sha256"] if independent else state["head"],
        "new_row_offset": state["accepted_new_rows"] if independent else None})
    payloads = {"coefficients.u8": payload(coefficients, "u8"), "physical-remainder.bin": payload(numeric["remainder"], "packed3", [PHYSICAL]),
        "target-before.bin": payload(state["target_raw"], "packed3", [PHYSICAL]),
        "target-remainder.bin": payload(numeric["target"], "packed3", [PHYSICAL]),
        "physical-literal.json": payload(literal, "json"), "reduction.json": payload(reduction, "json")}
    if independent:
        payloads.update({"physical-normalized.bin": payload(numeric["normalized"], "packed3", [PHYSICAL]),
                         "instruction.json": payload(instruction, "json"), "target.json": payload(target, "json")})
    return payloads


def restore_reduction(oracle: Any, state: Any, selection_lambda: np.ndarray, physical: Any, corrected: Any,
                      store: BatchPhaseStore, selection_scalar: int) -> Any:
    values, raws = store.values["reduction"], store.raws["reduction"]
    record = values["reduction.json"]
    check_seal(record, "reduction")
    coefficients = values["coefficients.u8"]
    require(coefficients.shape == (state["rank"],) and raws["target-before.bin"] == state["target_raw"],
            "saved_reduction_exact_before_basis_and_target")
    raw_dense = decode_array(physical["raw"], "packed3", [PHYSICAL])
    reconstructed = raw_dense.astype(np.int16)
    for index, coefficient in enumerate(coefficients):
        if int(coefficient):
            reconstructed -= int(coefficient) * decode_array(state["rows"][index], "packed3", [PHYSICAL]).astype(np.int16)
            reconstructed %= 3
    remainder = values["physical-remainder.bin"]
    require(np.array_equal(reconstructed % 3, remainder) and all(remainder[lead] == 0 for lead in state["leads"]),
            "saved_full_coefficient_remainder_identity")
    independent = bool(np.any(remainder))
    require(record["outcome"] == ("INDEPENDENT" if independent else "DEPENDENT") and
            record["remainder_zero"] is (not independent), "saved_dependence_is_full_physical_zero")
    raw_pairing, remainder_pairing = oracle.dot(selection_lambda, raw_dense), oracle.dot(selection_lambda, remainder)
    subtracted_new = sum(int(coefficients[index]) * state["selection_pairings"][index]
                         for index in range(state["anchor_rank"], state["rank"])) % 3
    require(raw_pairing == selection_scalar and (raw_pairing - subtracted_new) % 3 == remainder_pairing,
            "saved_selection_remainder_pairing_identity")
    normalized, normalized_pairing, lead, sigma, theta = None, None, None, None, None
    if independent:
        lead, sigma, theta = record["lead"], record["sigma"], record["target_scalar"]
        require(integer(lead, 0, PHYSICAL - 1) and lead not in state["leads"] and integer(sigma, 1, 2) and trit(theta),
                "saved_monic_pivot_and_target_types")
        normalized = raws["physical-normalized.bin"]
        normal = values["physical-normalized.bin"]
        target_before = decode_array(state["target_raw"], "packed3", [PHYSICAL])
        require(not np.any(remainder[:lead]) and remainder[lead] == sigma and
                np.array_equal(normal, sigma * remainder.astype(np.uint16) % 3) and normal[lead] == 1 and
                all(normal[x] == 0 for x in state["leads"]) and theta == int(target_before[lead]) and
                np.array_equal(values["target-remainder.bin"],
                    (target_before.astype(np.int16) - theta * normal.astype(np.int16)) % 3),
                "saved_one_scale_and_target_minus_sign")
        normalized_pairing = oracle.dot(selection_lambda, normal)
        require(normalized_pairing == sigma * remainder_pairing % 3, "saved_normalized_pairing_may_be_zero")
    else:
        require(raws["target-remainder.bin"] == state["target_raw"] and
                all(record[key] is None for key in ("lead", "sigma", "target_scalar", "normalized_sha256", "new_row_offset")),
                "dependent_preserves_target_and_has_no_normalized_row")
    numeric = {"outcome": "INDEPENDENT" if independent else "DEPENDENT", "coefficients": coefficients,
        "remainder": raws["physical-remainder.bin"], "normalized": normalized, "lead": lead, "sigma": sigma,
        "target": raws["target-remainder.bin"], "target_scalar": theta, "normalized_pairing": normalized_pairing,
        "raw_pairing": raw_pairing, "remainder_pairing": remainder_pairing, "subtracted_new_pairing": subtracted_new}
    expected = reduction_payloads(store.binding, store.selection_sha, store.ordinal, store.witness_sha,
                                  state, corrected, numeric, selection_scalar)
    require(set(expected) == set(raws) - {"telemetry.json"} and
            all(item[0] == raws[name] for name, item in expected.items()),
            "saved_reduction_all_arrays_literal_instructions_and_target_JSON")
    return numeric


def publish_candidate_decision(output: Path, store: BatchPhaseStore, state: Any, numeric: Any, *,
                               documents: dict[str, bytes] | None = None) -> Any:
    ordinal, binding = store.ordinal, store.binding
    require(integer(ordinal, 0, BATCH_SIZE - 1) and state["processed_candidates"] == ordinal and
            list(store.hashes) == list(CANDIDATE_PHASES), "complete_next_candidate_all_six_phases")
    values, raws = store.values["reduction"], store.raws["reduction"]
    reduction = values["reduction.json"]
    independent = numeric["outcome"] == "INDEPENDENT"
    row_manifest, row_source, target_parent = None, None, None
    if independent:
        local = state["accepted_new_rows"]
        instruction, target = values["instruction.json"], values["target.json"]
        row_payloads = {name: raws[name] for name in ("physical-normalized.bin", "instruction.json", "target.json")}
        row_files = [payload_descriptor(name, raw, "packed3" if name.endswith(".bin") else "json",
                         [PHYSICAL] if name.endswith(".bin") else None) for name, raw in sorted(row_payloads.items())]
        row_manifest = seal("row-manifest", {**{key: binding[key] for key in
            ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
            "selection_sha256": store.selection_sha, "local_row_offset": local, "global_row_id": state["rank"],
            "candidate_ordinal": ordinal, "predecessor_row_manifest_sha256": state["last_row_manifest_sha256"],
            "reduction_manifest_sha256": store.hashes["reduction"], "files": row_files,
            "state_head": instruction["rolling_sha256"], "rank": state["rank"] + 1, "generation": state["generation"] + 1,
            "target_literal_factor": {"row_id": state["rank"], "local_row_offset": local,
                "coefficient": target["scalar"], "exponent": signrep(target["scalar"]),
                "normalized_literal_sha256": sha(raws["physical-literal.json"])}, "eof": True})
        row_root = output / "rows" / f"{local:06d}"
        if documents is not None:
            for name, raw in {**row_payloads, "manifest.json": canonical(row_manifest)}.items():
                documents[f"rows/{local:06d}/" + name] = raw
        elif row_root.exists():
            require(row_root.is_dir() and not row_root.is_symlink() and
                    read_json(row_root, "manifest.json", "row-manifest") == row_manifest and
                    all(safe_file(row_root, name).read_bytes() == raw for name, raw in row_payloads.items()),
                    "durable_row_recovery_exact_same_bytes")
        else:
            row_root.parent.mkdir(parents=True, exist_ok=True)
            pending = row_root.parent / (f".pending-row-{local:06d}-" + uuid.uuid4().hex)
            pending.mkdir()
            for name, raw in row_payloads.items():
                atomic_write(pending, name, raw)
            atomic_write(pending, "manifest.json", canonical(row_manifest))
            os.rename(pending, row_root)
            sync_directory(row_root.parent)
        row_sha = sha(canonical(row_manifest))
        row_source = {"kind": "batch-row", "local_row_offset": local,
            "file": f"rows/{local:06d}/physical-normalized.bin", "bytes": PHYSICAL_BYTES,
            "sha256": sha(numeric["normalized"]), "row_manifest_sha256": row_sha}
        target_parent = {"role": "batch-row", "local_row_offset": local, "candidate_ordinal": ordinal,
            "row_manifest_sha256": row_sha, "instruction_sha256": sha(raws["instruction.json"]),
            "target_sha256": sha(raws["target.json"]), "state_head": instruction["rolling_sha256"], **target}
    else:
        instruction = None
        row_sha = None
    updated = advance_reduction_numeric(state, numeric, instruction, row_source, target_parent)
    candidate = seal("candidate-manifest", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "selection_sha256": store.selection_sha, "ordinal": ordinal, "witness_sha256": store.witness_sha,
        "oracle_view_sha256": store.initial_previous, "phase_manifests": dict(store.hashes),
        "predecessor_candidate_manifest_sha256": state["last_candidate_manifest_sha256"],
        "outcome": numeric["outcome"], "row_manifest_sha256": row_sha,
        "accepted_new_rows_before": state["accepted_new_rows"], "accepted_new_rows_after": updated["accepted_new_rows"],
        "rank_before": state["rank"], "rank_after": updated["rank"],
        "generation_before": state["generation"], "generation_after": updated["generation"],
        "parent_state_head": state["head"], "state_head": updated["head"],
        "target_before_sha256": sha(state["target_raw"]), "target_after_sha256": sha(updated["target_raw"]), "eof": True})
    candidate_name = f"candidates/{ordinal:06d}/manifest.json"
    if documents is None:
        write_once(output, candidate_name, canonical(candidate))
    else:
        documents[candidate_name] = canonical(candidate)
    updated["last_candidate_manifest_sha256"], updated["last_row_manifest_sha256"] = sha(canonical(candidate)), \
        row_sha if independent else state["last_row_manifest_sha256"]
    return updated, candidate, row_manifest

def checkpoint_value(binding: Any, state: Any, selection_phases: Any, selection_sha: str | None,
                     current: Any, predecessor: str | None) -> Any:
    require(list(selection_phases) == list(SELECTION_PHASES[:len(selection_phases)]), "checkpoint_selection_phase_prefix")
    require((len(selection_phases) == 3) == (selection_sha is not None), "checkpoint_completed_selection_identity")
    current_hashes = dict(current.hashes) if current is not None else {}
    current_ordinal = current.ordinal if current is not None else None
    require(current is None or (len(selection_phases) == 3 and current_ordinal == state["processed_candidates"] and
            1 <= len(current_hashes) <= 5 and list(current_hashes) == list(CANDIDATE_PHASES[:len(current_hashes)])),
            "checkpoint_current_candidate_has_only_incomplete_six_phase_prefix")
    sequence = len(selection_phases) if len(selection_phases) < 3 else \
        3 + 6 * state["processed_candidates"] + len(current_hashes)
    return seal("checkpoint", {**binding, "selection_sha256": selection_sha,
        "predecessor_checkpoint_sha256": predecessor, "sequence": sequence, "kind": "BatchReductionState",
        **{key: state[key] for key in ("processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation")},
        "reduction_state_head": state["head"], "target_remainder_sha256": sha(state["target_raw"]),
        "current_lambda_sha256": None, "current_candidate_ordinal": current_ordinal,
        "current_phase_manifests": current_hashes, "last_candidate_manifest_sha256": state["last_candidate_manifest_sha256"],
        "last_row_manifest_sha256": state["last_row_manifest_sha256"], "selection_phase_manifests": dict(selection_phases)})


def private_head(checkpoint: Any) -> Any:
    check_seal(checkpoint, "checkpoint")
    return seal("progress-head", {**{key: checkpoint[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256")}, "checkpoint_sha256": sha(canonical(checkpoint)),
        **{key: checkpoint[key] for key in ("sequence", "kind", "processed_candidates", "dependent_candidates",
            "accepted_new_rows", "rank", "generation", "reduction_state_head", "target_remainder_sha256", "current_lambda_sha256")}})


def publish_private_checkpoint(output: Path, checkpoint: Any) -> Any:
    raw = canonical(checkpoint)
    write_once(output, "progress/checkpoints/" + sha(raw) + ".json", raw)
    head = private_head(checkpoint)
    atomic_write(output, "progress/HEAD", canonical(head), replace=True)
    return head


def read_final(output: Path, oracle: Any, m: Any, metadata: Any, intake: Any, prefix: Any) -> Any | None:
    root = output / "final"
    if not root.exists():
        require(not (output / "HEAD").exists() and not (output / "result.json").exists(),
                "public_final_requires_durable_final_directory")
        return None
    require(prefix["complete_private"] and prefix["head_sequence"] == prefix["durable_sequence"] and
            root.is_dir() and not root.is_symlink(), "final_only_after_complete_committed_private_prefix")
    final = read_json(root, "manifest.json", "final-manifest")
    state, selection, binding = prefix["state"], prefix["selection"], prefix["binding"]
    terminal = ("COMPLETE_ZERO_CANDIDATE" if selection["terminal"] == "COMPLETE_ZERO_CANDIDATE" else
        "LINEAR_MEMBERSHIP_CANDIDATE" if not any(state["target_raw"]) else "BATCH_COMPLETE_CANDIDATE")
    kind = "LinearMembershipCandidate" if terminal == "LINEAR_MEMBERSHIP_CANDIDATE" else "Separator"
    roster = {"separator.json": ("json", None), "target-remainder.bin": ("packed3", [PHYSICAL]),
              "telemetry.json": ("json", None)}
    if kind == "Separator":
        roster["lambda.bin"] = ("packed3", [PHYSICAL])
    require(isinstance(final["files"], list) and [entry["file"] for entry in final["files"]] == sorted(roster),
            "saved_final_exact_typed_file_roster")
    values, raws = {}, {}
    for entry in final["files"]:
        name = entry["file"]
        dtype, shape = roster[name]
        raw = safe_file(root, name).read_bytes()
        same_json(entry, payload_descriptor(name, raw, dtype, shape), "saved_final_full_file_descriptor")
        values[name], raws[name] = decode_array(raw, dtype, shape), raw
    require(raws["target-remainder.bin"] == state["target_raw"], "saved_final_exact_current_target")
    require((terminal == "COMPLETE_ZERO_CANDIDATE" and state["processed_candidates"] == 0 and
             selection["selected_count"] == 0) or
            (state["processed_candidates"] > 0 and state["accepted_new_rows"] >= 1 and
             (kind == "LinearMembershipCandidate" or state["processed_candidates"] == selection["selected_count"])),
            "saved_final_selected_complete_or_Linear")
    direct = None
    if kind == "Separator":
        if terminal == "COMPLETE_ZERO_CANDIDATE":
            require(raws["lambda.bin"] == intake["state"]["lambda_raw"], "complete_zero_inherits_selection_lambda")
        direct = m.check_final_separator(values["lambda.bin"], state["rows"], intake["state"]["target_raw"], state["target_raw"])
    expected_separator = seal("separator", {"kind": kind,
        "selection_lambda_sha256": sha(intake["state"]["lambda_raw"]),
        "lambda_sha256": sha(raws["lambda.bin"]) if kind == "Separator" else None,
        "lambda_rho2": current_derived_rho2(metadata["start.json"], state) if kind == "Separator" else None,
        "direct_pairing": direct, "anchor_pairing_rows": state["anchor_rank"] if kind == "Separator" else None,
        "final_pairing_rows": state["rank"] if kind == "Separator" else None, "new_lambda_oracle": None,
        "source_lower_zero": "NOT_ASSERTED", "physical_lower_zero": True})
    same_json(values["separator.json"], expected_separator, "saved_final_full_direct_and_DERIVED_separator")
    validate_telemetry(values["telemetry.json"], "final",
                       sum(len(raw) for name, raw in raws.items() if name != "telemetry.json"))
    expected_final = final_manifest_value(binding, state, selection, terminal, kind, final["files"],
                                          sha(raws["lambda.bin"]) if kind == "Separator" else None)
    same_json(final, expected_final, "saved_final_manifest_all_counts_and_ancestry")
    files = {"final/manifest.json", *("final/" + name for name in roster)}
    prefix["files"].update(files)
    if (output / "HEAD").exists():
        head = read_json(output, "HEAD", "head")
        same_json(head, public_head_value(binding, final), "saved_public_HEAD_matches_whole_final")
        prefix["files"].add("HEAD")
    else:
        require(not (output / "result.json").exists(), "result_requires_actual_public_HEAD")
    return {"manifest": final, "values": values, "raws": raws}


def prepare_final(output: Path, oracle: Any, m: Any, metadata: Any, intake: Any, prefix: Any) -> Any:
    require(prefix["complete_private"] and not (output / "final").exists(), "prepare_only_fresh_complete_final")
    begun, measurement = time.monotonic(), process_measurement()
    terminal, kind, payloads = final_payloads(oracle, m, metadata, prefix["state"], prefix["selection"], intake["state"])
    values, raws, files = {}, {}, []
    pending = output / (".pending-final-" + uuid.uuid4().hex)
    pending.mkdir()
    for name, (raw, dtype, shape) in sorted(payloads.items()):
        values[name], raws[name] = decode_array(raw, dtype, shape), raw
        atomic_write(pending, name, raw)
        files.append(payload_descriptor(name, raw, dtype, shape))
        check_deadline("prepare_final_payload")
    telemetry = phase_telemetry("final", begun, measurement, sum(map(len, raws.values())))
    raw = canonical(telemetry)
    atomic_write(pending, "telemetry.json", raw)
    values["telemetry.json"], raws["telemetry.json"] = telemetry, raw
    files.append(payload_descriptor("telemetry.json", raw, "json", None))
    files.sort(key=lambda entry: entry["file"])
    manifest = final_manifest_value(prefix["binding"], prefix["state"], prefix["selection"], terminal, kind,
        files, sha(raws["lambda.bin"]) if kind == "Separator" else None)
    atomic_write(pending, "manifest.json", canonical(manifest))
    check_deadline("before_final_durable_publication")
    # The caller performs HEAD -> result without a deadline or signal check.
    os.rename(pending, output / "final")
    sync_directory(output)
    return {"manifest": manifest, "values": values, "raws": raws}


def inventory_documents(admission: Any) -> Any:
    return {"inputs/parents-before.json": canonical(admission["parent_inventories"]),
            "inputs/code-before.json": canonical(admission["code_inventory"])}


def authenticate_input_documents(output: Path, admission: Any, *, required_before: bool) -> set[str]:
    expected = inventory_documents(admission)
    read_only_documents(output, expected, missing_allowed=not required_before)
    files = set(expected)
    for category in ("parents", "code"):
        name = f"inputs/{category}-after.json"
        if (output / name).exists():
            raw = safe_file(output, name).read_bytes()
            require(raw == expected[f"inputs/{category}-before.json"], "saved_input_after_matches_immutable_before")
            files.add(name)
    return files


def finish_inputs(output: Path, admission: Any, args: Any) -> Any:
    observed = []
    for role in ROLES:
        observed.append({"role": role, **inventory(admission["paths"][role])})
    same_json(observed, admission["parent_inventories"], "all_fifteen_parent_file_and_directory_invariance")
    observed_code = authenticate_code(admission["acceptance"]["code"])
    same_json(observed_code, admission["code_inventory"], "all_code_and_raw_input_invariance")
    require(file_pin(args.acceptance)["sha256"] == admission["acceptance_sha256"], "actual_acceptance_file_unchanged")
    documents = {"inputs/parents-after.json": canonical(observed), "inputs/code-after.json": canonical(observed_code)}
    for name, raw in documents.items():
        write_once(output, name, raw)
    return input_preservation(output, admission, admission["acceptance_sha256"])


def input_preservation(output: Path, admission: Any, acceptance_sha: str) -> Any:
    expected = inventory_documents(admission)
    for category in ("parents", "code"):
        before = expected[f"inputs/{category}-before.json"]
        require(safe_file(output, f"inputs/{category}-before.json").read_bytes() == before and
                safe_file(output, f"inputs/{category}-after.json").read_bytes() == before,
                "complete_result_requires_all_four_inventory_files")
    return {**{key + "_" + when + "_sha256": file_pin(output / "inputs" / f"{category}-{when}.json")["sha256"]
        for key, category in (("parents", "parents"), ("code", "code")) for when in ("before", "after")},
        "portable_acceptance_sha256": admission["portable_sha256"], "acceptance_sha256": acceptance_sha,
        "all_parent_files_and_directories_unchanged": True, "all_code_and_raw_unchanged": True,
        "acceptance_unchanged": True}


WORKFLOW = ".github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml"
INVOCATION_KEYS = ("id", "portable_acceptance_sha256", "acceptance_sha256", "owner_sha256", "source_sha256",
    "start_sha256", "fixed_manifest_sha256", "selection_start_sha256", "registration", "resume", "batch_size",
    "max_batches", "max_seconds", "max_memory_mib", "progress_head_before_sha256", "physical_head_before_sha256",
    "processed_candidates_before", "accepted_new_rows_before", "started_utc", "launch", "host_paths")


def validate_launch(value: Any) -> None:
    exact_keys(value, ("run", "attempt", "head", "workflow"), "launch_exact_fields")
    require(integer(value["run"], 1) and integer(value["attempt"], 1) and
            isinstance(value["head"], str) and re.fullmatch("[0-9a-f]{40}", value["head"]) is not None and
            value["workflow"] == WORKFLOW, "launch_registered_positive_integer_GHA_identity")


def validate_host_paths(value: Any) -> None:
    exact_keys(value, ("parents", "acceptance", "output"), "host_paths_exact_fields")
    exact_keys(value["parents"], ROLES, "host_paths_exact_fifteen_roles")
    for name in (*value["parents"].values(), value["acceptance"], value["output"]):
        require(isinstance(name, str) and Path(name).is_absolute(), "host_metadata_absolute_path")


def validate_invocation_history(values: list[Any], output: Path, prefix: Any) -> None:
    fresh = 0
    bootstrap = 0
    for value in values:
        require(type(value["resume"]) is bool and integer(value["processed_candidates_before"], 0, BATCH_SIZE) and
                integer(value["accepted_new_rows_before"], 0, BATCH_SIZE), "invocation_origin_strict_types")
        fresh += int(value["resume"] is False)
        bootstrap += int(value["resume"] is True and value["progress_head_before_sha256"] is None and
            value["physical_head_before_sha256"] is None and value["processed_candidates_before"] == 0 and
            value["accepted_new_rows_before"] == 0)
    require(fresh <= 1, "at_most_one_regular_fresh_invocation")
    if values:
        require(fresh == 1 or bootstrap >= 1, "regular_invocation_history_has_fresh_or_bootstrap_origin")
    else:
        checkpoint_root = output / "progress/checkpoints"
        has_checkpoint = checkpoint_root.exists() and any(
            re.fullmatch(r"[0-9a-f]{64}\.json", path.name) is not None for path in checkpoint_root.iterdir())
        require(prefix["old_head"] is None and prefix["durable_sequence"] == 0 and
                not (output / "progress/HEAD").exists() and not has_checkpoint,
                "zero_regular_invocations_only_before_all_progress_publication")


def invocation_files(output: Path, admission: Any, prefix: Any, final: Any | None) -> tuple[list[Any], dict[str, Any]]:
    directory = output / "invocations"
    if not directory.exists():
        validate_invocation_history([], output, prefix)
        return [], {}
    require(directory.is_dir() and not directory.is_symlink(), "invocations_directory")
    histories = {sha(canonical(private_head(checkpoint))): checkpoint
                 for checkpoint in prefix["checkpoints"][:prefix["head_sequence"] + 1]}
    public_sha = file_pin(output / "HEAD")["sha256"] if final is not None and (output / "HEAD").is_file() else None
    entries, values = [], {}
    for path in sorted(directory.iterdir(), key=lambda path: path.name):
        match = re.fullmatch(r"([0-9a-f]{32})\.json", path.name)
        if match is None:
            require(atomic_diagnostic(path, {name for name in
                [path.name[1:].split(".pending-", 1)[0]] if re.fullmatch(r"[0-9a-f]{32}\.json", name)}),
                "invocation_filename_or_limited_atomic_diagnostic")
            continue
        value = read_json(directory, path.name, "invocation")
        exact_keys(value, ("schema", "sha256", *INVOCATION_KEYS), "invocation_exact_keys")
        require(value["id"] == match.group(1) and value["portable_acceptance_sha256"] == admission["portable_sha256"] and
                isinstance(value["acceptance_sha256"], str) and
                re.fullmatch("[0-9a-f]{64}", value["acceptance_sha256"]) is not None and
                type(value["resume"]) is bool and integer(value["batch_size"]) and value["batch_size"] == BATCH_SIZE and
                integer(value["max_batches"]) and value["max_batches"] == MAX_BATCHES and
                integer(value["max_seconds"]) and value["max_seconds"] == 5400 and
                integer(value["max_memory_mib"]) and value["max_memory_mib"] == 7168,
                "invocation_same_portable_input_and_registered_limits")
        same_json(value["registration"], admission["acceptance"]["registration"], "invocation_registration_unchanged")
        for key, expected in prefix["binding"].items():
            require(value[key] == expected, "invocation_same_owner_source_start_selection")
        validate_launch(value["launch"])
        validate_host_paths(value["host_paths"])
        original_acceptance = copy.deepcopy(admission["portable"])
        for parent in original_acceptance["parents"]:
            parent["path"] = value["host_paths"]["parents"][parent["role"]]
        require(sha(canonical(original_acceptance)) == value["acceptance_sha256"],
                "invocation_full_acceptance_reconstructed_from_portable_and_host_paths")
        require(isinstance(value["started_utc"], str) and
                re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", value["started_utc"]) is not None,
                "invocation_UTC_timestamp")
        require(integer(value["processed_candidates_before"], 0, BATCH_SIZE) and
                integer(value["accepted_new_rows_before"], 0, BATCH_SIZE), "invocation_before_count_integer")
        before = value["progress_head_before_sha256"]
        physical = value["physical_head_before_sha256"]
        if not value["resume"] or before is None:
            require(before is physical is None and
                    value["processed_candidates_before"] == value["accepted_new_rows_before"] == 0,
                    "fresh_or_bootstrap_before_has_no_HEAD")
        else:
            require(before in histories, "invocation_before_is_saved_private_history")
            checkpoint = histories[before]
            require(value["processed_candidates_before"] == checkpoint["processed_candidates"] and
                    value["accepted_new_rows_before"] == checkpoint["accepted_new_rows"] and
                    (physical is None or (public_sha is not None and physical == public_sha and
                     checkpoint["sequence"] == prefix["durable_sequence"])), "invocation_before_full_history_join")
        entry = file_pin(path, "invocations/" + path.name)
        entries.append(entry)
        values[entry["sha256"]] = value
    validate_invocation_history(list(values.values()), output, prefix)
    return entries, values


def begin_invocation(output: Path, admission: Any, prefix: Any, args: Any, public_head_sha: str | None) -> Any:
    def positive_environment(name: str) -> int:
        value = os.environ.get(name, "")
        require(re.fullmatch(r"[1-9][0-9]*", value) is not None, "positive_GHA_environment:" + name)
        return int(value)
    launch = {"run": positive_environment("GITHUB_RUN_ID"), "attempt": positive_environment("GITHUB_RUN_ATTEMPT"),
              "head": os.environ.get("GITHUB_SHA", ""), "workflow": WORKFLOW}
    workflow_ref = os.environ.get("GITHUB_WORKFLOW_REF", "")
    require("/" + WORKFLOW + "@" in workflow_ref, "actual_registered_workflow_ref")
    validate_launch(launch)
    old_head = prefix["old_head"] if args.resume else None
    host_paths = {"parents": {role: str(admission["paths"][role]) for role in ROLES},
                  "acceptance": str(args.acceptance.resolve()), "output": str(output)}
    validate_host_paths(host_paths)
    value = seal("invocation", {"id": uuid.uuid4().hex, "portable_acceptance_sha256": admission["portable_sha256"],
        "acceptance_sha256": admission["acceptance_sha256"], **prefix["binding"],
        "registration": admission["acceptance"]["registration"], "resume": args.resume,
        "batch_size": BATCH_SIZE, "max_batches": MAX_BATCHES, "max_seconds": args.max_seconds,
        "max_memory_mib": args.max_memory_mib,
        "progress_head_before_sha256": sha(canonical(old_head)) if old_head is not None else None,
        "physical_head_before_sha256": public_head_sha if args.resume else None,
        "processed_candidates_before": old_head["processed_candidates"] if old_head is not None else 0,
        "accepted_new_rows_before": old_head["accepted_new_rows"] if old_head is not None else 0,
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "launch": launch, "host_paths": host_paths})
    write_once(output, "invocations/" + value["id"] + ".json", canonical(value))
    return value



def candidate_view(output: Path, binding: Any, selection: Any, witness: Any, state: Any) -> Any:
    ordinal, selection_sha, witness_sha = witness["ordinal"], sha(canonical(selection)), sha(canonical(witness))
    view = seal("oracle-view", {**binding, "selection_sha256": selection_sha, "ordinal": ordinal,
        "witness_sha256": witness_sha, "geometry_manifest_sha256": binding["fixed_manifest_sha256"],
        "phase_manifests": selection["phase_manifests"], "anchor_state_head": state["head"],
        "selection_lambda_sha256": sha(state["lambda_raw"]), "terminal": "VIOLATION_CANDIDATE"})
    require(read_json(output, f"candidates/{ordinal:06d}/witness.json", "witness") == witness and
            read_json(output, f"candidates/{ordinal:06d}/oracle-view.json", "oracle-view") == view,
            "actual_candidate_immutable_selection_view")
    return view


def legacy_e_input(fixed: Any, state: Any, binding: Any, selection: Any, witness: Any,
                   view: Any, section: Any, cochain: Any) -> Any:
    require(view["selection_sha256"] == sha(canonical(selection)) and view["witness_sha256"] == sha(canonical(witness)) and
            view["anchor_state_head"] == state["head"] and view["selection_lambda_sha256"] == sha(state["lambda_raw"]),
            "fixed_selection_scalar_and_candidate_witness_binding")
    return {"geometry": fixed.geometry, "stages": {"geometry": binding["fixed_manifest_sha256"],
            **selection["phase_manifests"]},
        "layout": {"manifest_sha256": sha(canonical(view)), "witness_sha256": sha(canonical(witness)),
            "terminal": "VIOLATION_CANDIDATE", "snapshot_sha256": binding["selection_start_sha256"],
            "state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"])},
        "witness": copy.deepcopy(witness), "q": section["q"], "kappa": section["kappa"], "f": cochain["f"], "b_aux": cochain["b_aux"]}


def run_candidate_phases(l: Any, e: Any, oracle: Any, refinement: Any, m: Any, base: Any, intake: Any,
                         fixed: Any, selection_state: Any, current_state: Any, section: Any, cochain: Any,
                         accepted: Any, store: BatchPhaseStore, after_phase: Callable[[str, Any], None]) -> Any:
    """One candidate's fresh arrays; complete builders are never invoked again."""
    def finish_phase(phase: str, builder: Callable[[], Any]) -> None:
        if store.ensure(phase, builder):
            after_phase(phase, None)

    def raw_builder() -> Any:
        raw = e.selected_raw_word(oracle, base.ARITH, fixed.context, accepted)
        return {"raw-word.json": payload(raw["record"], "json"), "raw-chain.bin": payload(raw["chain"], "packed3")}
    finish_phase("raw", raw_builder)
    raw = l.restore_raw(e, oracle, fixed, accepted, store.values["raw"])

    def source_builder() -> Any:
        source = e.source_from_chain(oracle, refinement, m, base.ARITH, fixed.context, accepted, raw)
        return {**{"raw-source-" + name + ".bin": payload(part, "packed3")
            for name, part in zip(("d0", "d1", "d2", "aux"), source["parts"], strict=True)},
            "raw-source.json": payload(source["record"], "json")}
    finish_phase("source", source_builder)
    source = l.restore_source(e, oracle, refinement, m, accepted, raw, store.values["source"])

    def primal_builder() -> Any:
        primal = e.primal_section(fixed.proxy, m, fixed.segments, source["parts"])
        return {"p1-coefficients.u8": payload(primal["alpha"], "u8"), "p1-reductions.json": payload(primal["record"], "json"),
                "p1-exponent-residues.json": payload(fixed.residues, "json")}
    finish_phase("primal", primal_builder)
    primal = l.restore_primal(e, oracle, fixed, store.values["primal"])

    def correction_builder() -> Any:
        corrected = e.corrected_source(fixed.proxy, refinement, m, fixed.p1, fixed.index, fixed.segments,
                                       fixed.pairs, raw, source, primal)
        return {"p1-roots.json": payload(corrected["roots"], "json"),
            "source-lower-remainder.bin": payload(e.lower_row(corrected["parts"]), "packed3"),
            "source-top-corrected.bin": payload(corrected["parts"][2], "packed3"),
            "source-correction.json": payload(corrected["record"], "json")}
    finish_phase("p1", correction_builder)
    corrected = l.restore_corrected(e, oracle, refinement, m, fixed, raw, primal, store.values["p1"])

    def B_builder() -> Any:
        physical = e.four_B(oracle, m, intake["bundle"]["tables"], selection_state, accepted, corrected)
        return {"physical-by-character.bin": payload(physical["by_character"], "packed3"),
            "physical-raw.bin": payload(physical["raw"], "packed3", [PHYSICAL]),
            "B.json": payload(l.B_receipt(oracle, accepted, corrected, physical), "json")}
    finish_phase("B", B_builder)
    physical = l.restore_B(oracle, accepted, corrected, store.values["B"], store.raws["B"])

    def reduction_builder() -> Any:
        numeric = reduce_candidate_numeric(oracle, m, selection_state["lambda"], current_state,
                                           physical["raw"], accepted["witness"]["scalar"])
        return reduction_payloads(store.binding, store.selection_sha, store.ordinal, store.witness_sha,
                                  current_state, corrected, numeric, accepted["witness"]["scalar"])
    fresh = store.ensure("reduction", reduction_builder)
    numeric = restore_reduction(oracle, current_state, selection_state["lambda"], physical, corrected, store,
                                accepted["witness"]["scalar"])
    # The caller publishes row/candidate/checkpoint immediately; no stop check here.
    return {"numeric": numeric, "raw": raw, "source": source, "primal": primal, "corrected": corrected,
            "physical": physical, "fresh_reduction": fresh}


def current_derived_rho2(start: Any, state: Any) -> Any:
    require(state["target_parents"][:97] == start["accepted_target_derivation_parents"] and
            len(state["target_parents"]) == 97 + state["accepted_new_rows"],
            "all97_accepted_parents_and_only_new_accepted_target_rows")
    return {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": start["original_rho2_packed_sha256"],
        "accepted_target_derivation_parents": copy.deepcopy(state["target_parents"]),
        "identity_convention": {
            "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",
            "all_one_row_steps": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row",
            "batch_rows": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row; correction appends normalized_word^sr(target.scalar)"},
        "anchor_completed_steps": start["anchor_completed_steps"], "new_batch_target_steps_executed": state["accepted_new_rows"]}



def phase_telemetry_descriptor(output: Path, store: BatchPhaseStore, phase: str) -> Any:
    root = store.directory(phase)
    return file_pin(root / "telemetry.json", (root / "telemetry.json").relative_to(output).as_posix())


def selection_readout(store: BatchPhaseStore, selection: Any, selection_lambda: np.ndarray) -> Any:
    section, cochain = store.values["section"], store.values["cochain"]
    kappa, score = section["kappa.bin"], cochain["score.u8"]
    f3_array(kappa, (LOWER,), "readout_full_kappa")
    f3_array(score, (6, 2, N), "readout_full_six_tag_score")
    degree0 = kappa[:24192].reshape(4, 6, 2, 504)
    degree1 = kappa[24192:96768].reshape(4, 6, 2, 3, 504)
    d0 = [[int(np.count_nonzero(degree0[a, tag])) for tag in range(6)] for a in range(4)]
    d1 = [[int(np.count_nonzero(degree1[a, tag])) for tag in range(6)] for a in range(4)]
    aux = [int(value) for value in kappa[96768:]]
    kappa_support = {"total": int(np.count_nonzero(kappa)), "degree0_by_character_tag": d0,
        "degree1_by_character_tag": d1, "aux_values": aux}
    require(kappa_support["total"] == sum(map(sum, d0)) + sum(map(sum, d1)) + sum(value != 0 for value in aux),
            "full_kappa_tag_and_aux_support_sum")
    return {**{key: selection[key] for key in
        ("failed_count", "first_failed_index", "first_failed_edge", "failed_indices", "failed_edges", "aux_values")},
        "q_characters": character_counts(section["q.bin"], TOP),
        "lambda_characters": character_counts(selection_lambda.reshape(4, PHYSICAL // 4), PHYSICAL // 4),
        "score_support": {"total": int(np.count_nonzero(score)),
                          "by_tag": [int(np.count_nonzero(score[tag])) for tag in range(6)]},
        "kappa_support": kappa_support, "p1_equation_residual_support": int(np.count_nonzero(section["equation-residuals.u8"]))}


def candidate_readout(output: Path, witness: Any, store: BatchPhaseStore | None,
                      manifest: Any | None, row_manifest: Any | None) -> Any:
    entry = {"ordinal": witness["ordinal"], "kind": witness["kind"],
        "witness_sha256": sha(canonical(witness)), "selection_scalar": witness["scalar"]}
    if store is None:
        require(manifest is row_manifest is None, "skipped_candidate_has_no_decision")
        return {**entry, "outcome": "SKIPPED_AFTER_LINEAR",
            **{key: None for key in ("candidate_manifest_sha256", "row_manifest_sha256", "lead", "sigma", "target_scalar",
                                    "rank_before", "rank_after", "generation_before", "generation_after", "raw_readout")},
            "phase_telemetry": {phase: None for phase in CANDIDATE_PHASES}}
    require(list(store.hashes) == list(CANDIDATE_PHASES) and manifest is not None, "completed_candidate_readout")
    reduction = store.values["reduction"]["reduction.json"]
    raw, source = store.values["raw"]["raw-word.json"], store.values["source"]["raw-source.json"]
    nodes, receipts = ({item["id"]: item for item in raw[key]} for key in ("nodes", "node_values"))
    unrepaired = receipts["w"]
    repair = [nodes[name]["exponent"] for name in ("repair-x", "repair-y", "repair-central")] \
        if witness["kind"] == "chord" else None
    require(all(integer(x) for x in unrepaired["exponent"]) and trit(unrepaired["omega"]) and
            (repair is None or all(integer(x) for x in repair)), "raw_readout_ordinary_signed_exponents")
    return {**entry, "outcome": reduction["outcome"], "candidate_manifest_sha256": sha(canonical(manifest)),
        "row_manifest_sha256": sha(canonical(row_manifest)) if row_manifest is not None else None,
        **{key: reduction[key] for key in ("lead", "sigma", "target_scalar", "rank_before", "rank_after",
                                          "generation_before", "generation_after")},
        "phase_telemetry": {phase: phase_telemetry_descriptor(output, store, phase) for phase in CANDIDATE_PHASES},
        "raw_readout": {"epsilon_unrepaired": list(unrepaired["exponent"]), "omega_unrepaired": unrepaired["omega"],
            "repair_exponents": repair, "raw_slp_letters": raw["word_stream"]["letters"],
            "source_homogeneous_scalar": source["homogeneous_scalar"], "section_scalar": source["section_scalar"],
            "selection_scalar": witness["scalar"], "alpha_support": int(np.count_nonzero(store.values["primal"]["p1-coefficients.u8"]))}}


def final_payloads(oracle: Any, m: Any, metadata: Any, state: Any, selection: Any, anchor_state: Any) -> Any:
    terminal = ("COMPLETE_ZERO_CANDIDATE" if selection["terminal"] == "COMPLETE_ZERO_CANDIDATE" else
                "LINEAR_MEMBERSHIP_CANDIDATE" if not any(state["target_raw"]) else "BATCH_COMPLETE_CANDIDATE")
    if terminal == "COMPLETE_ZERO_CANDIDATE":
        require(state["processed_candidates"] == state["accepted_new_rows"] == 0 and selection["selected_count"] == 0,
                "complete_zero_only_before_materialization")
        value = {"kind": "Separator", "lambda": bytes(anchor_state["lambda_raw"]),
            "direct_pairing": m.check_final_separator(anchor_state["lambda"], state["rows"],
                                                      anchor_state["target_raw"], state["target_raw"])}
    else:
        require(state["processed_candidates"] > 0 and state["accepted_new_rows"] >= 1 and
                (terminal == "LINEAR_MEMBERSHIP_CANDIDATE" or state["processed_candidates"] == selection["selected_count"]),
                "nonempty_batch_final_has_an_accepted_row_and_complete_or_linear_prefix")
        value = final_separator_numeric(oracle, m, state, anchor_state["target_raw"])
    require((value["kind"] == "LinearMembershipCandidate") == (terminal == "LINEAR_MEMBERSHIP_CANDIDATE"),
            "final_terminal_matches_full_target_zero")
    nonzero = value["lambda"] is not None
    separator = seal("separator", {"kind": value["kind"], "selection_lambda_sha256": sha(anchor_state["lambda_raw"]),
        "lambda_sha256": sha(value["lambda"]) if nonzero else None,
        "lambda_rho2": current_derived_rho2(metadata["start.json"], state) if nonzero else None,
        "direct_pairing": value["direct_pairing"], "anchor_pairing_rows": state["anchor_rank"] if nonzero else None,
        "final_pairing_rows": state["rank"] if nonzero else None, "new_lambda_oracle": None,
        "source_lower_zero": "NOT_ASSERTED", "physical_lower_zero": True})
    payloads = {"target-remainder.bin": payload(state["target_raw"], "packed3", [PHYSICAL]),
                "separator.json": payload(separator, "json")}
    if nonzero:
        payloads["lambda.bin"] = payload(value["lambda"], "packed3", [PHYSICAL])
    return terminal, value["kind"], payloads


def final_manifest_value(binding: Any, state: Any, selection: Any, terminal: str, kind: str,
                         files: Any, lambda_sha: str | None) -> Any:
    return seal("final-manifest", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "selection_sha256": sha(canonical(selection)), "terminal": terminal, "kind": kind,
        "anchor_completed_steps": 64, "selected_count": selection["selected_count"],
        **{key: state[key] for key in ("processed_candidates", "dependent_candidates", "accepted_new_rows")},
        "skipped_after_linear": list(range(state["processed_candidates"], selection["selected_count"])) \
            if kind == "LinearMembershipCandidate" else [],
        "rank": state["rank"], "generation": state["generation"], "state_head": state["head"],
        "target_remainder_sha256": sha(state["target_raw"]), "lambda_sha256": lambda_sha,
        "last_candidate_manifest_sha256": state["last_candidate_manifest_sha256"],
        "last_row_manifest_sha256": state["last_row_manifest_sha256"], "files": files, "eof": True})


def public_head_value(binding: Any, final: Any) -> Any:
    check_seal(final, "final-manifest")
    return seal("head", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "selection_sha256": final["selection_sha256"], "final_manifest_sha256": sha(canonical(final)),
        **{key: final[key] for key in ("terminal", "kind", "anchor_completed_steps", "selected_count",
            "processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation", "state_head",
            "target_remainder_sha256", "lambda_sha256")}, "new_lambda_oracle": None})


def same_json(actual: Any, expected: Any, label: str) -> None:
    """Canonical comparison also distinguishes true/false from integer one/zero."""
    require(canonical(actual) == canonical(expected), label)


def phase_prefix(store: BatchPhaseStore, length: int) -> Any:
    value = copy.copy(store)
    value.hashes = {name: store.hashes[name] for name in store.phases[:length]}
    return value


def sequence_scope(head_sequence: Any, durable_sequence: int) -> None:
    require(integer(head_sequence, 0, 3 + 6 * BATCH_SIZE) and
            integer(durable_sequence, 0, 3 + 6 * BATCH_SIZE) and
            head_sequence <= durable_sequence <= head_sequence + 1,
            "only_the_immediate_durable_phase_beyond_private_HEAD")


def diagnostic_subtree(path: Path) -> None:
    require(not path.is_symlink() and path.is_dir(), "diagnostic_directory_type")
    for root, directories, files in os.walk(path, followlinks=False):
        for name in directories + files:
            item = Path(root) / name
            require(not item.is_symlink() and
                    (item.is_dir() or (item.is_file() and stat.S_ISREG(item.stat().st_mode))),
                    "diagnostic_subtree_no_symlink_or_special_file")


def pending_directory(relative: str) -> bool:
    parts = relative.split("/")
    name = parts[-1]
    if len(parts) == 1:
        return re.fullmatch(r"\.pending-final-[0-9a-f]{32}", name) is not None
    if parts[:-1] == ["selection"]:
        phases = SELECTION_PHASES
    elif len(parts) == 4 and parts[0] == "candidates" and re.fullmatch(r"\d{6}", parts[1]) and parts[2] == "e":
        require(int(parts[1]) < BATCH_SIZE, "diagnostic_candidate_ordinal")
        phases = CANDIDATE_PHASES[:-1]
    elif len(parts) == 3 and parts[0] == "candidates" and re.fullmatch(r"\d{6}", parts[1]):
        require(int(parts[1]) < BATCH_SIZE, "diagnostic_reduction_ordinal")
        phases = ("reduction",)
    elif parts[:-1] == ["rows"]:
        match = re.fullmatch(r"\.pending-row-(\d{6})-[0-9a-f]{32}", name)
        return match is not None and int(match.group(1)) < BATCH_SIZE
    else:
        return False
    return any(re.fullmatch(r"\.(?:pending|orphan)-" + re.escape(phase) + r"-[0-9a-f]{32}", name)
               for phase in phases)


def authenticate_output_roster(output: Path, files: set[str], candidate_count: int) -> None:
    """Every ordinary file is derived from the admitted prefix, including EOF."""
    directories = {"fixed", "selection", "candidates", "rows", "final", "progress",
                   "progress/checkpoints", "invocations", "inputs"}
    for ordinal in range(candidate_count):
        directories.update((f"candidates/{ordinal:06d}", f"candidates/{ordinal:06d}/e"))
    for name in files:
        safe_name(name)
        parent = PurePosixPath(name).parent
        while str(parent) != ".":
            directories.add(str(parent))
            parent = parent.parent
    for root, child_dirs, child_files in os.walk(output, followlinks=False):
        root_path = Path(root)
        relative_root = root_path.relative_to(output).as_posix()
        prefix = "" if relative_root == "." else relative_root + "/"
        for name in list(child_dirs):
            item, relative = root_path / name, prefix + name
            require(not item.is_symlink() and item.is_dir(), "output_directory_type")
            if pending_directory(relative):
                diagnostic_subtree(item)
                child_dirs.remove(name)
            else:
                require(relative in directories, "unregistered_ordinary_output_directory:" + relative)
        allowed_basenames = {PurePosixPath(name).name for name in files
                             if str(PurePosixPath(name).parent) == relative_root}
        if relative_root == ".":
            allowed_basenames.update(("HEAD", "result.json", "resource-stop.json", "rejected.json"))
        elif relative_root == "progress":
            allowed_basenames.add("HEAD")
        elif relative_root == "inputs":
            allowed_basenames.update(("parents-before.json", "parents-after.json", "code-before.json", "code-after.json"))
        elif relative_root == "invocations":
            for name in child_files:
                match = re.fullmatch(r"\.([0-9a-f]{32}\.json)\.pending-[0-9a-f]{32}", name)
                if match is not None:
                    allowed_basenames.add(match.group(1))
        for name in child_files:
            item, relative = root_path / name, prefix + name
            require(not item.is_symlink() and item.is_file() and stat.S_ISREG(item.stat().st_mode),
                    "output_file_type")
            require(relative in files or atomic_diagnostic(item, allowed_basenames),
                    "unregistered_ordinary_output_file:" + relative)


def phase_files(output: Path, store: BatchPhaseStore) -> set[str]:
    names = set()
    for phase, manifest in store.manifests.items():
        prefix = store.directory(phase).relative_to(output).as_posix() + "/"
        names.update(prefix + entry["file"] for entry in manifest["files"])
        names.add(prefix + "manifest.json")
    return names


def read_only_documents(output: Path, documents: Any, *, missing_allowed: bool) -> None:
    for name, raw in documents.items():
        path = output / name
        if path.exists():
            require(safe_file(output, name).read_bytes() == raw, "saved_exact_metadata_document:" + name)
        else:
            require(missing_allowed, "committed_metadata_document_missing:" + name)


def restoration_store(l: Any, e: Any, output: Path, binding: Any, selection: Any, witness: Any,
                      view: Any) -> BatchPhaseStore:
    return BatchPhaseStore(l, e, output / "candidates" / f"{witness['ordinal']:06d}", binding,
        selection_sha=sha(canonical(selection)), ordinal=witness["ordinal"],
        witness_sha=sha(canonical(witness)), initial_previous=sha(canonical(view)))


def load_private_prefix(l: Any, e: Any, oracle: Any, refinement: Any, m: Any, base: Any,
                        admission: Any, intake: Any, metadata: Any, output: Path) -> Any:
    """Read all committed bytes plus at most one durable phase; do not publish."""
    binding, anchor = binding_from_metadata(metadata), intake["state"]
    fixed = copy.copy(intake["fixed"])
    fixed.digest = binding["fixed_manifest_sha256"]
    state = make_reduction_state(anchor, intake["row_sources"])
    expected: dict[str, bytes] = {name: canonical(value) for name, value in metadata.items()}
    files = set(expected)
    private_exists = (output / "progress/HEAD").exists()
    head = read_json(output, "progress/HEAD", "progress-head") if private_exists else None
    head_sequence = head["sequence"] if head is not None else 0
    require(integer(head_sequence, 0, 3 + 6 * BATCH_SIZE), "saved_private_HEAD_sequence_type")
    read_only_documents(output, expected, missing_allowed=not private_exists)
    checkpoints: list[Any] = [checkpoint_value(binding, state, {}, None, None, None)]
    selection_store = BatchPhaseStore(l, e, output / "selection", binding)
    selection_store.load()
    require(private_exists or not selection_store.hashes, "initial_HEAD_before_any_completed_phase")
    files.update(phase_files(output, selection_store))
    section = l.restore_section(oracle, fixed, selection_store.values["section"]) \
        if "section" in selection_store.hashes else None
    cochain = l.restore_cochain(oracle, selection_store.values["cochain"]) \
        if "cochain" in selection_store.hashes else None
    decoded, selection, selection_documents = None, None, {}
    if "tree" in selection_store.hashes:
        decoded = saved_selection_values(oracle, fixed, selection_store, cochain)
        selection = publish_selection(output, selection_store, decoded, anchor, documents=selection_documents)
        read_only_documents(output, selection_documents, missing_allowed=head_sequence < 3)
        expected.update(selection_documents)
        files.update(selection_documents)
    for length in range(1, len(selection_store.hashes) + 1):
        phases = phase_prefix(selection_store, length).hashes
        checkpoints.append(checkpoint_value(binding, state, phases,
            sha(canonical(selection)) if length == 3 else None, None, sha(canonical(checkpoints[-1]))))
    decisions, readings, current, tail_decision = [], [], None, None
    witnesses = decoded["witnesses"] if decoded is not None else []
    for ordinal, witness in enumerate(witnesses):
        view = json_bytes(selection_documents[f"candidates/{ordinal:06d}/oracle-view.json"])
        store = restoration_store(l, e, output, binding, selection, witness, view)
        store.load()
        files.update(phase_files(output, store))
        if not store.hashes:
            require(not (output / f"candidates/{ordinal:06d}/manifest.json").exists(),
                    "unprocessed_candidate_has_no_decision")
            continue
        require(ordinal == state["processed_candidates"] and current is None and any(state["target_raw"]),
                "candidate_phases_have_no_hole_or_post_Linear_tail")
        for length in range(1, min(5, len(store.hashes)) + 1):
            checkpoints.append(checkpoint_value(binding, state, selection_store.hashes, sha(canonical(selection)),
                phase_prefix(store, length), sha(canonical(checkpoints[-1]))))
        if len(store.hashes) < 6:
            current = store
            continue
        accepted = legacy_e_input(fixed, anchor, binding, selection, witness, view, section, cochain)
        def no_builder_or_publication(phase: str, unused: Any) -> None:
            raise ValueError("completed_candidate_builder_must_not_run:" + phase)
        restored = run_candidate_phases(l, e, oracle, refinement, m, base, intake, fixed, anchor, state,
            section, cochain, accepted, store, no_builder_or_publication)
        require(restored["fresh_reduction"] is False, "saved_reduction_was_not_recomputed")
        documents: dict[str, bytes] = {}
        before = state
        state, candidate, row = publish_candidate_decision(output, store, before, restored["numeric"],
                                                            documents=documents)
        sequence = 3 + 6 * state["processed_candidates"]
        require(sequence == len(checkpoints), "candidate_phase_sequence_from_saved_counts")
        read_only_documents(output, documents, missing_allowed=sequence > head_sequence)
        expected.update(documents)
        files.update(documents)
        decisions.append({"ordinal": ordinal, "candidate": candidate, "row": row})
        readings.append(candidate_readout(output, witness, store, candidate, row))
        checkpoints.append(checkpoint_value(binding, state, selection_store.hashes, sha(canonical(selection)),
                                             None, sha(canonical(checkpoints[-1]))))
        if sequence > head_sequence:
            tail_decision = (before, store, restored["numeric"])
        del restored
    durable_sequence = len(checkpoints) - 1
    sequence_scope(head_sequence, durable_sequence)
    if head is not None:
        same_json(head, private_head(checkpoints[head_sequence]), "private_HEAD_full_state_and_checkpoint_binding")
    checkpoint_names = set()
    for index, checkpoint in enumerate(checkpoints):
        name = "progress/checkpoints/" + sha(canonical(checkpoint)) + ".json"
        checkpoint_names.add(name)
        read_only_documents(output, {name: canonical(checkpoint)}, missing_allowed=index > head_sequence or head is None)
    files.update(checkpoint_names)
    if head is not None:
        files.add("progress/HEAD")
    complete_private = (selection is not None and current is None and
        (state["processed_candidates"] == selection["selected_count"] or not any(state["target_raw"])))
    return {"binding": binding, "fixed": fixed, "state": state, "selection_store": selection_store,
        "section": section, "cochain": cochain, "decoded": decoded, "selection": selection,
        "witnesses": witnesses, "current": current, "decisions": decisions, "readings": readings,
        "checkpoints": checkpoints, "old_head": head, "head_sequence": head_sequence,
        "durable_sequence": durable_sequence, "files": files, "documents": expected,
        "selection_documents": selection_documents, "tail_decision": tail_decision,
        "complete_private": complete_private}


def recover_private_metadata(output: Path, prefix: Any, metadata: Any) -> Any:
    """Called only after the entire ordinary roster and all saved joins pass."""
    for name, value in metadata.items():
        write_once(output, name, canonical(value))
    if prefix["selection"] is not None:
        # Restore only external witness/view copies of the completed tree payload.
        for name, raw in prefix["selection_documents"].items():
            write_once(output, name, raw)
    tail = prefix["tail_decision"]
    if tail is not None:
        before, store, numeric = tail
        updated, candidate, row = publish_candidate_decision(output, store, before, numeric)
        require(updated["head"] == prefix["state"]["head"] and
                updated["processed_candidates"] == prefix["state"]["processed_candidates"],
                "one_saved_tail_recovered_without_second_append")
        prefix["tail_decision"] = None
    for index, checkpoint in enumerate(prefix["checkpoints"]):
        write_once(output, "progress/checkpoints/" + sha(canonical(checkpoint)) + ".json", canonical(checkpoint))
    head = private_head(prefix["checkpoints"][-1])
    if prefix["old_head"] is None or prefix["head_sequence"] != prefix["durable_sequence"]:
        atomic_write(output, "progress/HEAD", canonical(head), replace=True)
    return head


def completion_log(phase: str, **fields: Any) -> None:
    """Final publication and authenticated read-only reception have no stop gate."""
    sys.stderr.write(canonical({"phase": phase, **fields}).decode("ascii"))
    sys.stderr.flush()


def result_value(output: Path, admission: Any, intake: Any, prefix: Any, final: Any,
                 invocations: Any, invocation: Any, elapsed: Any) -> Any:
    require(type(elapsed) in (int, float) and math.isfinite(elapsed) and elapsed >= 0,
            "result_elapsed_finite_nonnegative_measurement")
    manifest, binding = final["manifest"], prefix["binding"]
    candidates = list(prefix["readings"])
    for witness in prefix["witnesses"][len(candidates):]:
        require(manifest["kind"] == "LinearMembershipCandidate", "unprocessed_tail_only_after_Linear")
        candidates.append(candidate_readout(output, witness, None, None, None))
    require(len(candidates) == manifest["selected_count"], "full_selected_candidate_readout")
    selection_store = prefix["selection_store"]
    return seal("result", {"status": "PASS", **{key: manifest[key] for key in
        ("terminal", "kind", "anchor_completed_steps", "selected_count", "processed_candidates",
         "dependent_candidates", "accepted_new_rows", "skipped_after_linear", "rank", "generation",
         "state_head", "target_remainder_sha256", "lambda_sha256")},
        **{key: binding[key] for key in ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "parent_layout_sha256": sha(canonical(outer_metadata(admission, intake)["parent-layout.json"])),
        "selection_sha256": sha(canonical(prefix["selection"])),
        "head_sha256": sha(canonical(public_head_value(binding, manifest))),
        "final_manifest_sha256": sha(canonical(manifest)), "new_lambda_oracle": None,
        "selection_readout": selection_readout(selection_store, prefix["selection"], intake["state"]["lambda"]),
        "final_lambda_characters": character_counts(final["values"]["lambda.bin"].reshape(4, PHYSICAL // 4),
            PHYSICAL // 4) if "lambda.bin" in final["values"] else None,
        "candidates": candidates, "selection_telemetry": {
            phase: phase_telemetry_descriptor(output, selection_store, phase) for phase in SELECTION_PHASES},
        "final_telemetry": file_pin(output / "final/telemetry.json", "final/telemetry.json"),
        "invocation_sha256": sha(canonical(invocation)), "invocations": invocations,
        "input_preservation": input_preservation(output, admission, invocation["acceptance_sha256"]),
        "elapsed_seconds": elapsed, "old_snapshot_numeric_replays": 0, "old_insert_numeric_replays": 0,
        "old_success_suites": 0, "positive_readout": "NEW_BATCH_SAME_WORD_ADAPTER_PENDING"
            if manifest["kind"] == "LinearMembershipCandidate" else "NOT_APPLICABLE",
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False, **ASSURANCE})


def authenticate_completed_result(output: Path, admission: Any, intake: Any, prefix: Any,
                                  final: Any, invocations: Any, invocation_values: Any) -> bytes:
    require(final is not None and (output / "HEAD").is_file() and (output / "result.json").is_file(),
            "completed_resume_requires_both_public_HEAD_and_result")
    raw = safe_file(output, "result.json").read_bytes()
    result = json_bytes(raw)
    check_seal(result, "result")
    require(isinstance(result.get("invocation_sha256"), str) and
            result["invocation_sha256"] in invocation_values, "completed_result_actual_invocation")
    expected = result_value(output, admission, intake, prefix, final, invocations,
        invocation_values[result["invocation_sha256"]], result["elapsed_seconds"])
    require(raw == canonical(expected), "completed_result_all_saved_arrays_receipts_and_public_HEAD")
    return raw


def append_checkpoint(output: Path, prefix: Any, current: Any | None) -> None:
    checkpoint = checkpoint_value(prefix["binding"], prefix["state"], prefix["selection_store"].hashes,
        sha(canonical(prefix["selection"])) if prefix["selection"] is not None else None,
        current, sha(canonical(prefix["checkpoints"][-1])))
    require(checkpoint["sequence"] == len(prefix["checkpoints"]), "one_phase_advances_one_private_sequence")
    publish_private_checkpoint(output, checkpoint)
    prefix["checkpoints"].append(checkpoint)
    prefix["head_sequence"] = prefix["durable_sequence"] = checkpoint["sequence"]
    prefix["files"].update(("progress/HEAD", "progress/checkpoints/" + sha(canonical(checkpoint)) + ".json"))


def run_selection(l: Any, e: Any, oracle: Any, base: Any, intake: Any, prefix: Any, output: Path) -> None:
    store, fixed = prefix["selection_store"], prefix["fixed"]
    for phase in SELECTION_PHASES:
        if phase in store.hashes:
            continue
        if phase == "section":
            builder = lambda: serialize_arrays(l.current_section_cached(
                oracle, base, intake["bundle"]["tables"], intake["state"], fixed)["arrays"])
        elif phase == "cochain":
            builder = lambda: serialize_arrays(oracle.source_cochain(base.ARITH, fixed.context,
                fixed.geometry, prefix["section"])["arrays"])
        else:
            builder = lambda: tree_payloads(oracle, fixed, prefix["cochain"], prefix["binding"])
        require(store.ensure(phase, builder), "fresh_selection_phase_published_once")
        if phase == "section":
            prefix["section"] = l.restore_section(oracle, fixed, store.values[phase])
        elif phase == "cochain":
            prefix["cochain"] = l.restore_cochain(oracle, store.values[phase])
        else:
            prefix["decoded"] = saved_selection_values(oracle, fixed, store, prefix["cochain"])
            prefix["witnesses"] = prefix["decoded"]["witnesses"]
            prefix["selection"] = publish_selection(output, store, prefix["decoded"], intake["state"])
            documents: dict[str, bytes] = {}
            publish_selection(output, store, prefix["decoded"], intake["state"], documents=documents)
            prefix["files"].update(documents)
            prefix["selection_documents"] = documents
        append_checkpoint(output, prefix, None)
        prefix["files"].update(phase_files(output, store))
        check_deadline("after_selection_phase_checkpoint:" + phase)


def run_candidates(l: Any, e: Any, oracle: Any, refinement: Any, m: Any, base: Any,
                   intake: Any, prefix: Any, output: Path) -> None:
    selection, binding = prefix["selection"], prefix["binding"]
    fixed, anchor = prefix["fixed"], intake["state"]
    for ordinal in range(prefix["state"]["processed_candidates"], selection["selected_count"]):
        if not any(prefix["state"]["target_raw"]):
            break
        check_deadline("before_selected_candidate")
        witness = prefix["witnesses"][ordinal]
        view = candidate_view(output, binding, selection, witness, anchor)
        accepted = legacy_e_input(fixed, anchor, binding, selection, witness, view, prefix["section"], prefix["cochain"])
        store = prefix["current"] if prefix["current"] is not None else \
            restoration_store(l, e, output, binding, selection, witness, view)
        require(store.ordinal == ordinal and len(store.hashes) <= 5, "resume_current_candidate_exact_cursor")
        def after_phase(phase: str, unused: Any) -> None:
            append_checkpoint(output, prefix, store)
            prefix["files"].update(phase_files(output, store))
            check_deadline("after_candidate_phase_checkpoint:" + phase)
        result = run_candidate_phases(l, e, oracle, refinement, m, base, intake, fixed, anchor, prefix["state"],
            prefix["section"], prefix["cochain"], accepted, store, after_phase)
        before = prefix["state"]
        updated, candidate, row = publish_candidate_decision(output, store, before, result["numeric"])
        prefix["state"] = updated
        prefix["readings"].append(candidate_readout(output, witness, store, candidate, row))
        prefix["decisions"].append({"ordinal": ordinal, "candidate": candidate, "row": row})
        documents: dict[str, bytes] = {}
        publish_candidate_decision(output, store, before, result["numeric"], documents=documents)
        prefix["files"].update(documents)
        prefix["files"].update(phase_files(output, store))
        prefix["current"] = None
        append_checkpoint(output, prefix, None)
        del result, store, accepted, before
        check_deadline("after_candidate_decision_checkpoint")
    prefix["complete_private"] = (prefix["state"]["processed_candidates"] == selection["selected_count"] or
                                  not any(prefix["state"]["target_raw"]))
    require(prefix["complete_private"], "one_batch_selected_roster_complete_or_Linear")


DIAGNOSTIC_KEYS = ("status", "terminal", "phase", "reason", "partial", "owner_sha256", "source_sha256",
    "start_sha256", "selection_start_sha256", "selection_sha256", "invocation_sha256", "progress_head_sha256",
    "checkpoint_sha256", "public_head_sha256", "final_manifest_sha256", "processed_candidates", "dependent_candidates",
    "accepted_new_rows", "rank", "generation", "max_seconds", "max_memory_mib", "elapsed_seconds",
    "candidate", "cross_checked", "verified")
ACTIVE_INVOCATION: Any = None


def admit_diagnostics(output: Path, admission: Any, prefix: Any, invocations: Any, final: Any | None) -> set[str]:
    files = set()
    histories = {sha(canonical(private_head(cp))): cp
                 for cp in prefix["checkpoints"][:prefix["head_sequence"] + 1]}
    binding = prefix["binding"]
    selection_sha = sha(canonical(prefix["selection"])) if prefix["selection"] is not None else None
    final_sha = sha(canonical(final["manifest"])) if final is not None else None
    public_sha = file_pin(output / "HEAD")["sha256"] if (output / "HEAD").is_file() else None
    limits = admission["acceptance"]["registration"]["producer_limits"]
    for name, kind, status, terminal in (("resource-stop.json", "resource-stop", "UNKNOWN_RESOURCE", "UNKNOWN_RESOURCE"),
                                       ("rejected.json", "rejected", "FAIL", "REJECTED")):
        if not (output / name).exists():
            continue
        value = read_json(output, name, kind)
        exact_keys(value, ("schema", "sha256", *DIAGNOSTIC_KEYS), "diagnostic_exact_fields")
        require(value["status"] == status and value["terminal"] == terminal and value["partial"] is True and
                all(value[key] is False for key in FALSE_ASSURANCE) and isinstance(value["phase"], str) and
                isinstance(value["reason"], str) and integer(value["max_seconds"], 1) and
                integer(value["max_memory_mib"], 1) and value["max_seconds"] == limits["max_seconds"] and
                value["max_memory_mib"] == limits["max_memory_mib"] and
                type(value["elapsed_seconds"]) in (int, float) and math.isfinite(value["elapsed_seconds"]) and
                value["elapsed_seconds"] >= 0, "diagnostic_typed_non_candidate_registered_scope")
        for key, file in (("owner_sha256", "owner.json"), ("source_sha256", "source.json"),
                          ("start_sha256", "start.json"), ("selection_start_sha256", "selection/start.json")):
            if value[key] is not None:
                require(value[key] == binding[key] and file_pin(safe_file(output, file))["sha256"] == value[key],
                        "diagnostic_nonnull_binding_is_actual_saved_file")
        if value["selection_sha256"] is not None:
            require(selection_sha is not None and value["selection_sha256"] == selection_sha and
                    file_pin(safe_file(output, "selection/selection.json"))["sha256"] == selection_sha,
                    "diagnostic_actual_complete_selection")
        if value["invocation_sha256"] is not None:
            require(value["invocation_sha256"] in invocations, "diagnostic_actual_regular_invocation")
        before = value["progress_head_sha256"]
        if before is None:
            require(all(value[key] is None for key in ("checkpoint_sha256", "processed_candidates",
                "dependent_candidates", "accepted_new_rows", "rank", "generation")), "pre_HEAD_diagnostic_has_no_counts")
        else:
            require(before in histories, "diagnostic_only_committed_private_checkpoint_history")
            checkpoint = histories[before]
            require(value["checkpoint_sha256"] == sha(canonical(checkpoint)) and
                    safe_file(output, "progress/checkpoints/" + value["checkpoint_sha256"] + ".json").read_bytes() ==
                        canonical(checkpoint), "diagnostic_exact_saved_checkpoint_hash")
            for key in ("processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation"):
                require(type(value[key]) is int and value[key] == checkpoint[key], "diagnostic_committed_counts_only")
        if value["final_manifest_sha256"] is not None:
            require(final_sha is not None and value["final_manifest_sha256"] == final_sha,
                    "diagnostic_actual_final_manifest")
        if value["public_head_sha256"] is not None:
            require(public_sha is not None and value["public_head_sha256"] == public_sha and
                    value["final_manifest_sha256"] == final_sha and final_sha is not None,
                    "diagnostic_actual_public_HEAD_and_final")
        files.add(name)
    return files


def output_path_gate(args: Any) -> Path:
    """Authorize a disjoint destination before mkdir or diagnostic write access."""
    output = args.output_root.resolve()
    require(not args.output_root.is_symlink(), "output_is_not_a_symlink")
    for root in root_paths(args).values():
        require(output != root and output not in root.parents and root not in output.parents,
                "output_disjoint_from_every_readonly_parent_before_write")
    protected = [args.acceptance.resolve(), (SEARCH / Path(__file__).name).resolve(), (SEARCH / C_FILE).resolve()]
    protected.extend((PROJECT / name).resolve()
        for pins in (RETAINED_PRODUCER_PINS, REGISTERED_CHECKER_PINS, REGISTERED_RAW_PINS) for name in pins)
    require(all(output != path and output not in path.parents for path in protected),
            "output_cannot_contain_acceptance_or_registered_code_and_raw")
    return output


def run_actual(args: Any) -> bytes:
    global OUTPUT_CREATED, ACTIVE_INVOCATION, COMPLETED_READONLY
    OUTPUT_CREATED, ACTIVE_INVOCATION, COMPLETED_READONLY = None, None, False
    output = output_path_gate(args)
    if args.resume:
        require(output.is_dir() and not args.output_root.is_symlink(), "resume_existing_output_only")
    else:
        require(not output.exists(), "fresh_output_must_not_exist")
        output.mkdir(parents=True)
    OUTPUT_CREATED = output
    admission = authenticate_acceptance(args)
    l, e, oracle, refinement, p2, m, base, descriptors = own_dependencies()
    intake = None
    try:
        intake = thin_anchor(l, e, oracle, refinement, p2, m, base, descriptors, args, admission)
        metadata = outer_metadata(admission, intake)
        prefix = load_private_prefix(l, e, oracle, refinement, m, base, admission, intake, metadata, output)
        final = read_final(output, oracle, m, metadata, intake, prefix)
        invocations, invocation_values = invocation_files(output, admission, prefix, final)
        prefix["files"].update(entry["file"] for entry in invocations)
        prefix["files"].update(authenticate_input_documents(output, admission, required_before=prefix["old_head"] is not None))
        prefix["files"].update(admit_diagnostics(output, admission, prefix, invocation_values, final))
        if (output / "result.json").exists():
            require(args.resume and final is not None, "existing_result_only_completed_resume")
            prefix["files"].add("result.json")
            authenticate_output_roster(output, prefix["files"], len(prefix["witnesses"]))
            raw = authenticate_completed_result(output, admission, intake, prefix, final, invocations, invocation_values)
            COMPLETED_READONLY = True
            # Re-authenticate actual inputs after reading every saved payload. Existing
            # after files are read-only through write_once; no invocation/result changes.
            finish_inputs(output, admission, args)
            completion_log("completed-readonly-resume", processed=prefix["state"]["processed_candidates"],
                           accepted=prefix["state"]["accepted_new_rows"])
            return raw
        authenticate_output_roster(output, prefix["files"], len(prefix["witnesses"]))
        public_before = file_pin(output / "HEAD")["sha256"] if (output / "HEAD").exists() else None
        invocation = begin_invocation(output, admission, prefix, args, public_before)
        ACTIVE_INVOCATION = invocation
        prefix["files"].add("invocations/" + invocation["id"] + ".json")
        for name, raw in inventory_documents(admission).items():
            write_once(output, name, raw)
        recover_private_metadata(output, prefix, metadata)
        prefix["head_sequence"] = prefix["durable_sequence"]
        prefix["files"].add("progress/HEAD")
        if final is None:
            run_selection(l, e, oracle, base, intake, prefix, output)
            run_candidates(l, e, oracle, refinement, m, base, intake, prefix, output)
        finish_inputs(output, admission, args)
        prefix["files"].update(("inputs/parents-after.json", "inputs/code-after.json"))
        authenticate_output_roster(output, prefix["files"], len(prefix["witnesses"]))
        if final is None:
            final = prepare_final(output, oracle, m, metadata, intake, prefix)
        # No cooperative stop from durable final through public HEAD and result.
        head = public_head_value(prefix["binding"], final["manifest"])
        write_once(output, "HEAD", canonical(head))
        invocations, invocation_values = invocation_files(output, admission, prefix, final)
        result = result_value(output, admission, intake, prefix, final, invocations, invocation,
                              round(time.monotonic() - STARTED, 6))
        raw = canonical(result)
        write_once(output, "result.json", raw)
        completion_log("batch-completed", terminal=result["terminal"], processed=result["processed_candidates"],
                 dependent=result["dependent_candidates"], accepted=result["accepted_new_rows"],
                 rank=result["rank"], generation=result["generation"])
        return raw
    finally:
        if intake is not None:
            intake["fixed"].close()


def canary_reject(name: str, action: Callable[[], Any], rejected: list[str]) -> None:
    try:
        action()
    except ValueError:
        rejected.append(name)
    else:
        raise ValueError("canary_did_not_reject:" + name)


def canary_binding() -> Any:
    return {key: sha(("synthetic:" + key).encode("ascii")) for key in
            ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256", "selection_start_sha256")}


def canary_selection_fixture(l: Any, e: Any, oracle: Any, binding: Any,
                             hits: list[int], auxiliary: list[int]) -> Any:
    """Full roster length, synthetic linear data; no actual Omega admission."""
    from types import SimpleNamespace
    chords = np.arange(CHORDS, dtype=np.uint32)
    tau = np.zeros((CHORDS, 5), dtype=np.uint8)
    tau[:5] = np.eye(5, dtype=np.uint8)
    tau[5] = [1, 2, 0, 2, 1]
    values, fit = np.zeros(CHORDS, dtype=np.uint8), np.zeros(5, dtype=np.uint8)
    values[hits] = 1
    residuals, aux = values.copy(), np.asarray(auxiliary, dtype=np.uint8)
    selected = classify_batch(oracle, chords, tau, values, residuals, list(range(5)), fit, aux)
    witnesses = [seal("witness", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "ordinal": ordinal, "selection_policy": POLICY, **entry})
        for ordinal, entry in enumerate(selected["witnesses"])]
    metadata = seal("tree", {"vertices": N, "tree_edges": N - 1, "chords": CHORDS,
        "independent_tau_columns": 5, "basis_chords": list(range(5)), "fit": fit.tolist(),
        "aux_values": auxiliary, "first_failed_index": selected["first_failed_index"],
        "first_failed_edge": selected["first_failed_edge"], "residual_nonzero": selected["failed_count"],
        "full_chord_eof": True, "selection_policy": POLICY})
    roster = seal("witness-roster", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")},
        "witnesses": witnesses, "eof": True})
    arrays = {"potential-f.u8": np.zeros(N, dtype=np.uint8),
        "potential-tau.u8": np.zeros((N, 5), dtype=np.uint8), "chord-values.u8": values,
        "chord-tau.u8": tau, "chord-residuals.u8": residuals,
        "selected-chords.u32": np.arange(5, dtype=np.uint32), "fit.u8": fit, "basis-tau.u8": tau[:5].copy(),
        "failed-indices.u32": selected["failed_indices"], "failed-edges.u32": selected["failed_edges"],
        "tree.json": metadata, "witness-roster.json": roster}
    fixed = SimpleNamespace(geometry={"chords": chords}, values={name: arrays[name] for name in
        ("potential-tau.u8", "chord-tau.u8", "selected-chords.u32")})
    store = BatchPhaseStore(l, e, Path("synthetic-selection-not-an-admitted-parent"), binding)
    store.hashes = {phase: sha(("synthetic-" + phase).encode()) for phase in SELECTION_PHASES}
    store.values = {"tree": arrays}
    return fixed, store, {"b_aux": aux}, selected


def selftest_root_path(path: Path) -> Path:
    require(path.is_absolute(), "selftest_root_absolute")
    require(not path.exists() and not path.is_symlink(), "selftest_root_fresh")
    for item in (path, *path.parents):
        require(not item.is_symlink() and not getattr(item, "is_junction", lambda: False)(),
                "selftest_root_no_link_ancestor")
        if item.exists():
            require(item.is_dir() and stat.S_ISDIR(item.stat().st_mode), "selftest_root_directory_ancestor")
    require(path.parent.is_dir(), "selftest_root_existing_parent")
    resolved = path.resolve()
    require(resolved != PROJECT and PROJECT not in resolved.parents and resolved not in PROJECT.parents,
            "selftest_root_outside_source_tree")
    temporary = []
    for key in ("RUNNER_TEMP", "TEMP"):
        value = os.environ.get(key)
        if value:
            root = Path(value)
            if root.is_absolute() and root.is_dir() and not root.is_symlink():
                temporary.append(root.resolve())
    require(any(root in resolved.parents for root in temporary), "selftest_root_inside_registered_TEMP")
    return resolved


def k64_reject(root: Path, name: str, action: Callable[[], Any], expected: str, rejected: list[str]) -> None:
    try:
        action()
    except ValueError as exc:
        require(expected in str(exc), "k64_rejection_reached_expected_gate:" + name + ":" + str(exc))
        write_once(root, name + "/rejection.json", canonical({
            "fixture_scope": "UNADMITTED_SYNTHETIC_INTERFACE_INPUT", "name": name,
            "expected_gate": expected, "observed_error": str(exc)}))
        rejected.append(name)
    else:
        raise ValueError("k64_canary_did_not_reject:" + name)


def k64_registration_canary(root: Path) -> Any:
    from types import SimpleNamespace
    rejected = []
    args = SimpleNamespace(batch_size=BATCH_SIZE, max_seconds=5400, max_memory_mib=7168)
    registration = registered_policy()
    write_once(root, "valid-registration.json", canonical(registration))
    authenticate_registration(read_json(root, "valid-registration.json"), args)
    for label, number in (("32", 32), ("33", 33), ("63", 63), ("65", 65), ("128", 128),
                          ("float", 64.0), ("string", "64"), ("bool", True)):
        name = "batch-" + label
        value = copy.deepcopy(registration)
        value["batch_size"] = number
        write_once(root, name + "/registration.json", canonical(value))
        k64_reject(root, name,
            lambda name=name: authenticate_registration(read_json(root, name + "/registration.json"), args),
            "strict_registered_batch_counts", rejected)
    for label, number in (("two", 2), ("bool", True), ("float", 1.0)):
        name = "max-batches-" + label
        value = copy.deepcopy(registration)
        value["max_batches"] = number
        write_once(root, name + "/registration.json", canonical(value))
        k64_reject(root, name,
            lambda name=name: authenticate_registration(read_json(root, name + "/registration.json"), args),
            "strict_registered_batch_counts", rejected)
    for label, number in (("true", True), ("integer-zero", 0)):
        name = "refill-" + label
        value = copy.deepcopy(registration)
        value["refill"] = number
        write_once(root, name + "/registration.json", canonical(value))
        k64_reject(root, name,
            lambda name=name: authenticate_registration(read_json(root, name + "/registration.json"), args),
            "registered_no_refill_private_final_policy", rejected)
    value = copy.deepcopy(registration)
    value["selection_policy"] = "CHORD_FIRST_ROSTER_32_THEN_FIRST_AUX"
    write_once(root, "old-policy/registration.json", canonical(value))
    k64_reject(root, "old-policy",
        lambda: authenticate_registration(read_json(root, "old-policy/registration.json"), args),
        "registered_no_refill_private_final_policy", rejected)
    value = copy.deepcopy(registration)
    value["producer_limits"]["max_seconds"] = True
    write_once(root, "bool-resource/registration.json", canonical(value))
    k64_reject(root, "bool-resource",
        lambda: authenticate_registration(read_json(root, "bool-resource/registration.json"), args),
        "registered_limit_values", rejected)
    old_acceptance = {"schema": "d972.r07.fixed-lambda-cycle-batch.v1.acceptance", "parents": [],
                      "anchor": {}, "code": {}, "runtime": {}, "registration": registration}
    write_once(root, "old-acceptance/input.json", canonical(old_acceptance))
    k64_reject(root, "old-acceptance",
        lambda: authenticate_acceptance(SimpleNamespace(acceptance=root / "old-acceptance/input.json")),
        "new_batch_acceptance_schema", rejected)

    binding = canary_binding()
    source_fixture = {"fixture_scope": "UNADMITTED_SYNTHETIC_INTERFACE_INPUT",
                      "producer": file_pin(Path(__file__), "search/" + Path(__file__).name),
                      "registration": registration}
    binding["source_sha256"] = sha(canonical(source_fixture))
    owner_fixture = seal("owner", {"fixture_scope": "UNADMITTED_SYNTHETIC_INTERFACE_INPUT",
        "source_sha256": binding["source_sha256"], "registration": registration})
    binding["owner_sha256"] = sha(canonical(owner_fixture))
    write_once(root, "source-binding-input.json", canonical(source_fixture))
    write_once(root, "new-owner/input.json", canonical(owner_fixture))
    read_json(root, "new-owner/input.json", "owner")
    old_owner = {key: value for key, value in owner_fixture.items() if key != "sha256"}
    old_owner["schema"] = "d972.r07.fixed-lambda-cycle-batch.v1.owner"
    old_owner["sha256"] = sha(canonical(old_owner))
    write_once(root, "old-owner-schema/input.json", canonical(old_owner))
    k64_reject(root, "old-owner-schema", lambda: read_json(root, "old-owner-schema/input.json", "owner"),
               "canonical_object_seal", rejected)

    portable = {"schema": SCHEMA + ".acceptance",
        "parents": [{"role": role, "artifact": {}, "files": [], "directories": []} for role in ROLES],
        "anchor": {}, "code": {}, "runtime": copy.deepcopy(REGISTERED_RUNTIME), "registration": registration}
    current_acceptances = []
    outputs = [root / "bootstrap-original/packet", root / "bootstrap-reroot/packet"]
    for index, output in enumerate(outputs):
        host = {"parents": {}, "acceptance": str((root / ("host-" + str(index)) / "acceptance.json").resolve()),
                "output": str(output.resolve())}
        accepted = copy.deepcopy(portable)
        for item in accepted["parents"]:
            directory = root / ("host-" + str(index)) / "parents" / item["role"]
            directory.mkdir(parents=True)
            item["path"] = host["parents"][item["role"]] = str(directory.resolve())
        write_once(root, "host-" + str(index) + "/acceptance.json", canonical(accepted))
        current_acceptances.append((accepted, host))
    original, host = current_acceptances[0]
    receipt = seal("invocation", {
        "id": "1" * 32, "portable_acceptance_sha256": sha(canonical(portable)),
        "acceptance_sha256": sha(canonical(original)), **binding, "registration": registration,
        "resume": True, "batch_size": BATCH_SIZE, "max_batches": MAX_BATCHES,
        "max_seconds": 5400, "max_memory_mib": 7168, "progress_head_before_sha256": None,
        "physical_head_before_sha256": None, "processed_candidates_before": 0, "accepted_new_rows_before": 0,
        "started_utc": "2000-01-01T00:00:00Z",
        "launch": {"run": 1, "attempt": 1, "head": "a" * 40, "workflow": WORKFLOW}, "host_paths": host})
    prefix = {"files": {"invocations/" + receipt["id"] + ".json"}, "binding": binding,
              "old_head": None, "head_sequence": 0, "durable_sequence": 0, "checkpoints": []}
    for index, output in enumerate(outputs):
        write_once(output, "invocations/" + receipt["id"] + ".json", canonical(receipt))
        admission = {"portable": portable, "portable_sha256": sha(canonical(portable)),
                     "acceptance": current_acceptances[index][0]}
        entries, values = invocation_files(output, admission, prefix, None)
        require(len(entries) == len(values) == 1 and next(iter(values.values()))["resume"] is True,
                "k64_strict_zero_bootstrap_and_same_owner_reroot")
        authenticate_output_roster(output, prefix["files"], 0)
    require((outputs[0] / ("invocations/" + receipt["id"] + ".json")).read_bytes() ==
            (outputs[1] / ("invocations/" + receipt["id"] + ".json")).read_bytes(),
            "k64_reroot_preserves_exact_old_host_invocation")
    admission = {"portable": portable, "portable_sha256": sha(canonical(portable)),
                 "acceptance": current_acceptances[1][0]}
    for name, field, replacement, expected in (
            ("old-owner-binding", "owner_sha256", sha(canonical(old_owner)), "invocation_same_owner_source_start_selection"),
            ("old-source-binding", "source_sha256", sha(b"unadmitted-v1-source"), "invocation_same_owner_source_start_selection"),
            ("old-invocation-k32", "batch_size", 32, "invocation_same_portable_input_and_registered_limits"),
            ("bool-bootstrap-count", "processed_candidates_before", False, "invocation_before_count_integer"),
            ("old-invocation-schema", "schema", "d972.r07.fixed-lambda-cycle-batch.v1.invocation", "canonical_object_seal")):
        changed = {key: copy.deepcopy(value) for key, value in receipt.items() if key != "sha256"}
        changed[field] = replacement
        changed["sha256"] = sha(canonical(changed))
        output = root / name / "packet"
        write_once(output, "invocations/" + receipt["id"] + ".json", canonical(changed))
        k64_reject(root, name, lambda output=output: invocation_files(output, admission, prefix, None),
                   expected, rejected)

    sequence_scope(387, 387)
    sequence_scope(386, 387)
    for name, pair in (("sequence-388", [388, 388]), ("two-phases-ahead", [385, 387]),
                       ("bool-sequence", [True, 1])):
        write_once(root, name + "/input.json", canonical(pair))
        k64_reject(root, name, lambda name=name: sequence_scope(*read_json(root, name + "/input.json")),
                   "only_the_immediate_durable_phase_beyond_private_HEAD", rejected)
    nonce = "8" * 32
    for ordinal in (63, 64):
        output = root / ("candidate-ordinal-" + str(ordinal)) / "packet"
        name = "candidates/" + f"{ordinal:06d}" + "/e/.pending-raw-" + nonce
        write_once(output, name + "/partial.bin", b"unadmitted synthetic phase tail\n")
        if ordinal == 63:
            require(pending_directory(name), "k64_ordinal63_pending")
            authenticate_output_roster(output, set(), BATCH_SIZE)
        else:
            k64_reject(root, "candidate-ordinal-64",
                lambda output=output: authenticate_output_roster(output, set(), BATCH_SIZE),
                "unregistered_ordinary_output_directory", rejected)
    for ordinal in (63, 64):
        output = root / ("row-ordinal-" + str(ordinal)) / "packet"
        name = "rows/.pending-row-" + f"{ordinal:06d}" + "-" + nonce
        write_once(output, name + "/partial.bin", b"unadmitted synthetic row tail\n")
        if ordinal == 63:
            require(pending_directory(name), "k64_row63_pending")
            authenticate_output_roster(output, set(), 0)
        else:
            k64_reject(root, "row-ordinal-64",
                lambda output=output: authenticate_output_roster(output, set(), 0),
                "unregistered_ordinary_output_directory", rejected)
    for name, path, expected in (
            ("existing-selftest-root", root.parent, "selftest_root_fresh"),
            ("relative-selftest-root", Path("unadmitted-relative-root"), "selftest_root_absolute"),
            ("missing-selftest-parent", root / "not-created" / "child", "selftest_root_existing_parent")):
        write_once(root, name + "/input.json", canonical({"requested_path": str(path)}))
        k64_reject(root, name, lambda path=path: selftest_root_path(path), expected, rejected)
    return {"name": "k64-version-registration-and-types", "status": "PASS", "rejected_cases": rejected}


def k64_tree_commit(l: Any, e: Any, case: Path, binding: Any, values: Any, prior: Any) -> BatchPhaseStore:
    write_once(case, "fixture-context.json", canonical({
        "fixture_scope": "UNADMITTED_SYNTHETIC_INTERFACE_INPUT", "binding": binding,
        "prior_phase_hashes": prior, "actual_section_or_cochain_replayed": False}))
    store = BatchPhaseStore(l, e, case / "packet/selection", binding)
    store.hashes = copy.deepcopy(prior)
    roster = phase_roster(l, e, "tree", values)
    payloads = {name: encode_array(value, roster[name][0]) for name, value in values.items()
                if name != "telemetry.json"}
    require(store.ensure("tree", lambda: payloads), "k64_fixture_actual_tree_publication")
    return store


def k64_tree_reload(l: Any, e: Any, oracle: Any, case: Path, binding: Any, fixed: Any, cochain: Any) -> tuple[Any, Any]:
    context = read_json(case, "fixture-context.json")
    require(context["fixture_scope"] == "UNADMITTED_SYNTHETIC_INTERFACE_INPUT" and
            context["binding"] == binding and context["actual_section_or_cochain_replayed"] is False and
            set(context["prior_phase_hashes"]) == set(SELECTION_PHASES[:2]), "k64_saved_synthetic_context")
    store = BatchPhaseStore(l, e, case / "packet/selection", binding)
    store.hashes = {phase: context["prior_phase_hashes"][phase] for phase in SELECTION_PHASES[:2]}
    directory = store.directory("tree")
    manifest = read_json(directory, "manifest.json", "phase-manifest")
    values, raws = {}, {}
    for entry in manifest["files"]:
        binary = "dtype" in entry
        pin_type(entry, binary=binary)
        raw = safe_file(directory, entry["file"]).read_bytes()
        require(len(raw) == entry["bytes"] and sha(raw) == entry["sha256"], "k64_saved_full_payload_pin")
        dtype, shape = (entry["dtype"], entry["shape"]) if binary else ("json", None)
        values[entry["file"]], raws[entry["file"]] = decode_array(raw, dtype, shape), raw
    require({path.name for path in directory.iterdir()} == {*raws, "manifest.json"},
            "k64_saved_exact_tree_directory_EOF")
    store.accept("tree", manifest, values, raws)
    return store, saved_selection_values(oracle, fixed, store, cochain)


def k64_selection_canary(l: Any, e: Any, oracle: Any, root: Path) -> Any:
    rejected, binding = [], canary_binding()
    prior = {phase: sha(("unadmitted-k64-" + phase).encode("ascii")) for phase in SELECTION_PHASES[:2]}
    cases = [(32, 32), (33, 33), (63, 63), (64, 64), (65, 64)]
    retained = None
    for failures, wanted in cases:
        hits = list(range(5, 5 + failures - 1)) + [CHORDS - 1]
        fixed, synthetic, cochain, selected = canary_selection_fixture(l, e, oracle, binding, hits, [2, 1])
        case = root / ("m" + str(failures))
        write_once(case, "input.json", canonical({"failed_indices": hits, "auxiliary": [2, 1],
                   "expected_failed_count": failures, "expected_selected_count": wanted}))
        built = k64_tree_commit(l, e, case, binding, synthetic.values["tree"], prior)
        restored, decoded = k64_tree_reload(l, e, oracle, case, binding, fixed, cochain)
        require(restored.hashes == built.hashes and selected["failed_count"] == failures and
                len(decoded["witnesses"]) == wanted and
                [item["roster_index"] for item in decoded["witnesses"]] == hits[:wanted] and
                [int(x) for x in restored.values["tree"]["failed-indices.u32"]] == hits and
                all(item["kind"] == "chord" and len(item["cycles"]) == 6 for item in decoded["witnesses"]) and
                any(item["coefficient"] == 0 for item in decoded["witnesses"][0]["cycles"]) and
                any(decoded["witnesses"][0]["basis_coefficients"]), "k64_all_failed_cutoff_six_cycle_boundary")
        if failures <= 64:
            require(decoded["witnesses"][-1]["roster_index"] == CHORDS - 1, "k64_selected_includes_last_chord")
        else:
            require(decoded["witnesses"][-1]["roster_index"] != CHORDS - 1 and
                    int(restored.values["tree"]["failed-indices.u32"][-1]) == CHORDS - 1,
                    "k64_unselected_65th_failure_still_saved")
        before = inventory(case / "packet/selection/tree")
        selection = publish_selection(case / "packet", restored, decoded,
            {"head": sha(b"unadmitted-k64-anchor"), "lambda_raw": bytes(PHYSICAL_BYTES)})
        require(selection["selected_count"] == wanted and selection["failed_count"] == failures and
                len(selection["selected"]) == wanted and inventory(case / "packet/selection/tree") == before,
                "k64_saved_tree_metadata_publication_no_overwrite")
        docs: dict[str, bytes] = {}
        publish_selection(case / "packet", restored, decoded,
            {"head": sha(b"unadmitted-k64-anchor"), "lambda_raw": bytes(PHYSICAL_BYTES)}, documents=docs)
        require(all(safe_file(case / "packet", name).read_bytes() == raw for name, raw in docs.items()),
                "k64_selection_outer_documents_exact_full_bytes")
        if failures == 65:
            retained = (fixed, cochain, copy.deepcopy(restored.values["tree"]))
        del built, restored, synthetic, decoded, selected, before
    for name, auxiliary in (("auxiliary-only", [1, 2]), ("complete-zero", [0, 0])):
        fixed, synthetic, cochain, selected = canary_selection_fixture(l, e, oracle, binding, [], auxiliary)
        case = root / name
        write_once(case, "input.json", canonical({"failed_indices": [], "auxiliary": auxiliary}))
        k64_tree_commit(l, e, case, binding, synthetic.values["tree"], prior)
        restored, decoded = k64_tree_reload(l, e, oracle, case, binding, fixed, cochain)
        if any(auxiliary):
            require(len(decoded["witnesses"]) == 1 and decoded["witnesses"][0]["coordinate"] == 0 and
                    decoded["witnesses"][0]["eta"] == [1, 0], "k64_only_first_aux_after_all_chords_zero")
        else:
            require(decoded["witnesses"] == [] and selected["terminal"] == "COMPLETE_ZERO_CANDIDATE",
                    "k64_all_zero_includes_both_aux")
        publish_selection(case / "packet", restored, decoded,
            {"head": sha(b"unadmitted-k64-anchor"), "lambda_raw": bytes(PHYSICAL_BYTES)})
        del synthetic, restored, decoded
    require(retained is not None, "k64_retained_65_case")
    fixed, cochain, template = retained
    for name, expected in (
            ("overfull-65-witnesses", "saved_same_start_exact_selected_witness_roster"),
            ("old-32-witness-cutoff", "saved_same_start_exact_selected_witness_roster"),
            ("last-selected-index", "saved_full_ordered_six_cycles"),
            ("last-selected-coefficient", "saved_six_cycle_tau_and_scalar_identity"),
            ("selected-tail-order", "saved_full_ordered_six_cycles"),
            ("bool-selected-ordinal", "saved_witness_bound_and_typed")):
        values = copy.deepcopy(template)
        roster = values["witness-roster.json"]
        witnesses = roster["witnesses"]
        if name == "overfull-65-witnesses":
            last = copy.deepcopy(witnesses[-1])
            last.update({"ordinal": 64, "roster_index": CHORDS - 1, "edge": CHORDS - 1,
                         "failed_chord": CHORDS - 1})
            last["cycles"][0]["edge"] = CHORDS - 1
            witnesses.append(last)
        elif name == "old-32-witness-cutoff":
            del witnesses[32:]
        elif name == "last-selected-index":
            witnesses[-1].update({"roster_index": CHORDS - 1, "edge": CHORDS - 1, "failed_chord": CHORDS - 1})
            witnesses[-1]["cycles"][0]["edge"] = CHORDS - 1
        elif name == "last-selected-coefficient":
            witnesses[-1]["basis_coefficients"][0] = 1
            witnesses[-1]["cycles"][1]["coefficient"] = 2
        elif name == "selected-tail-order":
            witnesses[-2], witnesses[-1] = witnesses[-1], witnesses[-2]
            witnesses[-2]["ordinal"], witnesses[-1]["ordinal"] = 62, 63
        else:
            witnesses[-1]["ordinal"] = True
        roster["witnesses"] = [seal("witness", {key: value for key, value in witness.items()
                                             if key not in ("schema", "sha256")}) for witness in witnesses]
        values["witness-roster.json"] = seal("witness-roster", {
            key: value for key, value in roster.items() if key not in ("schema", "sha256")})
        case = root / name
        k64_tree_commit(l, e, case, binding, values, prior)
        k64_reject(root, name, lambda case=case: k64_tree_reload(l, e, oracle, case, binding, fixed, cochain),
                   expected, rejected)
    values = copy.deepcopy(template)
    values["chord-residuals.u8"] = values["chord-residuals.u8"][:-1]
    k64_reject(root, "truncated-last-residual",
        lambda: k64_tree_commit(l, e, root / "truncated-last-residual", binding, values, prior),
        "phase_descriptor_dtype_shape_and_full_hash", rejected)
    case = root / "early-eof"
    write_once(case, "input.json", canonical({"source_case": "m65", "eof": False}))
    k64_reject(root, "early-eof", lambda: classify_batch(oracle, fixed.geometry["chords"],
        template["chord-tau.u8"], template["chord-values.u8"], template["chord-residuals.u8"],
        [0, 1, 2, 3, 4], template["fit.u8"], cochain["b_aux"], eof=False),
        "complete_ascending_actual_chord_roster", rejected)
    return {"name": "k64-full-roster-cutoff-and-restoration", "status": "PASS", "rejected_cases": rejected}


def selftest(args: Any) -> Any:
    global SELFTEST_ROOT_CREATED
    SELFTEST_ROOT_CREATED = None
    require(integer(args.max_seconds) and args.max_seconds == 300 and
            integer(args.max_memory_mib) and args.max_memory_mib == 7168 and
            integer(args.batch_size) and args.batch_size == BATCH_SIZE and args.resume is False,
            "new_k64_interface_selftest_registered_limits")
    root = selftest_root_path(args.selftest_root)
    root.mkdir()
    SELFTEST_ROOT_CREATED = root
    completion_log("k64-selftest-root-created", selftest_root=str(root))
    try:
        l, e, oracle, refinement, p2, m, base, descriptors = own_dependencies()
        first = k64_registration_canary(root / "registration")
        second = k64_selection_canary(l, e, oracle, root / "selection")
        return seal("selftest", {"status": "PASS", "tests": [first, second],
            "fixture_scope": "preserved synthetic k64 registration, bootstrap and full-length chord roster; no actual Omega, rank1450 or candidate E arithmetic",
            "production_interfaces_used": ["selftest_root_path", "authenticate_acceptance", "authenticate_registration",
                "read_json", "check_seal", "invocation_files", "validate_invocation_history", "sequence_scope",
                "pending_directory", "authenticate_output_roster", "classify_batch", "BatchPhaseStore.ensure",
                "BatchPhaseStore.accept", "saved_selection_values", "publish_selection"],
            "old_success_suites": 0, "actual_anchor_arithmetic_replayed": False, **FALSE_ASSURANCE})
    finally:
        completion_log("k64-selftest-fixtures-retained", selftest_root=str(root))


def diagnostic(args: Any, status: str, reason: str) -> Any:
    kind, terminal = ("resource-stop", "UNKNOWN_RESOURCE") if status == "UNKNOWN_RESOURCE" else ("rejected", "REJECTED")
    output = OUTPUT_CREATED
    binding = {key: None for key in ("owner_sha256", "source_sha256", "start_sha256", "selection_start_sha256")}
    selection_sha, private, checkpoint, public_sha, final_sha = None, None, None, None, None
    if output is not None:
        try:
            for key, name, schema in (("owner_sha256", "owner.json", "owner"), ("source_sha256", "source.json", "source"),
                                      ("start_sha256", "start.json", "start"),
                                      ("selection_start_sha256", "selection/start.json", "selection-start")):
                if (output / name).is_file():
                    binding[key] = sha(canonical(read_json(output, name, schema)))
            if (output / "selection/selection.json").is_file():
                selection_sha = sha(canonical(read_json(output, "selection/selection.json", "selection")))
            if (output / "progress/HEAD").is_file():
                value = read_json(output, "progress/HEAD", "progress-head")
                require(isinstance(value.get("checkpoint_sha256"), str) and
                        re.fullmatch("[0-9a-f]{64}", value["checkpoint_sha256"]) is not None, "diagnostic_checkpoint_name")
                cp = read_json(output, "progress/checkpoints/" + value["checkpoint_sha256"] + ".json", "checkpoint")
                same_json(value, private_head(cp), "diagnostic_direct_private_checkpoint_join")
                require(all(integer(value[key], 0) for key in ("processed_candidates", "dependent_candidates",
                    "accepted_new_rows", "rank", "generation")), "diagnostic_saved_strict_counts")
                private, checkpoint = value, cp
            if (output / "final/manifest.json").is_file():
                final_sha = sha(canonical(read_json(output, "final/manifest.json", "final-manifest")))
            if (output / "HEAD").is_file():
                public = read_json(output, "HEAD", "head")
                require(public["final_manifest_sha256"] == final_sha, "diagnostic_actual_public_final_binding")
                public_sha = sha(canonical(public))
        except (ValueError, KeyError, TypeError, OSError):
            # Do not turn an unauthenticated or absent private state into counts.
            private, checkpoint = None, None
    value = seal(kind, {"status": status, "terminal": terminal, "phase": CURRENT_PHASE,
        "reason": reason, "partial": True, **binding, "selection_sha256": selection_sha,
        "invocation_sha256": sha(canonical(ACTIVE_INVOCATION)) if ACTIVE_INVOCATION is not None else None,
        "progress_head_sha256": sha(canonical(private)) if private is not None else None,
        "checkpoint_sha256": sha(canonical(checkpoint)) if checkpoint is not None else None,
        "public_head_sha256": public_sha, "final_manifest_sha256": final_sha,
        **{key: private[key] if private is not None else None for key in
            ("processed_candidates", "dependent_candidates", "accepted_new_rows", "rank", "generation")},
        "max_seconds": args.max_seconds, "max_memory_mib": args.max_memory_mib,
        "elapsed_seconds": round(time.monotonic() - STARTED, 6), **FALSE_ASSURANCE})
    if output is not None and not COMPLETED_READONLY:
        atomic_write(output, kind + ".json", canonical(value), replace=True)
    if args.selftest:
        completion_log("k64-selftest-diagnostic", status=status,
            selftest_root=str(args.selftest_root), created=SELFTEST_ROOT_CREATED is not None)
        if SELFTEST_ROOT_CREATED is not None:
            atomic_write(SELFTEST_ROOT_CREATED, kind + ".json", canonical(value), replace=True)
    return value


def cli() -> Any:
    parser = argparse.ArgumentParser(description=__doc__)
    for role in ROLES:
        if not role.startswith("block-"):
            parser.add_argument("--" + role + "-root", type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--acceptance", type=Path)
    parser.add_argument("--output", dest="output_root", type=Path)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--max-seconds", type=int, default=5400)
    parser.add_argument("--max-memory-mib", type=int, default=7168)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--selftest-root", type=Path)
    args = parser.parse_args()
    require(integer(args.max_seconds, 1) and integer(args.max_memory_mib, 1) and
            integer(args.batch_size) and args.batch_size == BATCH_SIZE, "CLI_positive_limits_and_fixed_batch_size")
    if args.selftest:
        require(args.selftest_root is not None and args.output_root is None and args.acceptance is None and not args.block_root and
                all(getattr(args, role.replace("-", "_") + "_root") is None for role in ROLES if not role.startswith("block-")),
                "selftest_has_no_actual_parent_or_output")
    else:
        require(args.selftest_root is None and args.output_root is not None and args.acceptance is not None and len(args.block_root) == 4 and
                all(getattr(args, role.replace("-", "_") + "_root") is not None for role in ROLES if not role.startswith("block-")),
                "production_requires_exact_fifteen_roots_acceptance_and_output")
    return args


def main() -> int:
    global STARTED, DEADLINE
    args = cli()
    STARTED, DEADLINE = time.monotonic(), time.monotonic() + args.max_seconds
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    try:
        import resource
        ceiling = args.max_memory_mib * 1024 * 1024
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        require(hard == resource.RLIM_INFINITY or hard >= ceiling, "runtime_address_space_limit_available")
        resource.setrlimit(resource.RLIMIT_AS, (ceiling, hard))
        raw = canonical(selftest(args)) if args.selftest else run_actual(args)
        sys.stdout.buffer.write(raw)
        sys.stdout.buffer.flush()
        return 0
    except (ResourceStop, MemoryError) as exc:
        sys.stdout.buffer.write(canonical(diagnostic(args, "UNKNOWN_RESOURCE", type(exc).__name__ + ":" + str(exc))))
        sys.stdout.buffer.flush()
        return 3
    except Exception as exc:
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stdout.buffer.write(canonical(diagnostic(args, "FAIL", type(exc).__name__ + ":" + str(exc))))
        sys.stdout.buffer.flush()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
