#!/usr/bin/env python3
"""Task971: bounded, durable complete-oracle/E continuation on one owner.

The external E result must be observed and pinned before admission. New
phases remain candidates until the independent whole-prefix checker ends.
Only retained producer arithmetic is imported. No old prefix is replayed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import tempfile
import time
from typing import Any, Callable
import uuid

import numpy as np

SCHEMA = "d972.r07.complete-oracle-cegar-continuation.v1"
SEARCH = Path(__file__).resolve().parent
PROJECT = SEARCH.parent
E_MODULE = "d972_r07_selected_cycle_materializer_v1.py"
E_MODULE_SHA = "4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3"
# Observed successful E candidate; only metadata and exact bytes are admitted.
E_ARTIFACT = {"run": 33981657987, "attempt": 1, "head": "444c71c9e554ae8feb9c8ee54df57d3df19ed66f",
    "id": 9973974150, "name": "d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1",
    "bytes": 2816692, "sha256": "sha256:884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25"}
E_FILES = {
    "output/HEAD": (1051, "75d2a3280a4926bfb73ea6c0a8424680c73e049c6f3ac9e0e53cb6e8a190835c"),
    "output/manifest.json": (4903, "956a6d91fae2c6ddda6a9dc8ee6ab52ee57de90c6cee367a6a58a33aad28ac59"),
    "output/start.json": (50926, "0bd617bb70e58d25c9344226275bae590dae1a28aeb1457f61477475a6f8092c"),
    "output/owner.json": (8425, "bd5e24d274e37977c5c1004be79530941501cdd390c9a27b0bfd2c35b396fa29"),
    "output/source.json": (1481, "c7a91fce06d95e4efb3b73ae74f0b8d0eb1f31b9baa2cb72eb899a62d04db5de"),
    "output/result.json": (168139, "199502f235662a934493db81e79a91950fce3dba829b8acbe39b9c37dc6bc7c8"),
    "checker-result.json": (30071, "9f0d30a4481ea94f0aa1a4cd5aa120281dc3ebee1a0e8e1b01db162efbde7a77"),
    "source-receipt.json": (3130, "b824897c24960e757e844f435048c369479c68b2f7c5c9859acaa47def8b07db"),
    "oracle-intake-receipt.json": (7094, "c10de40bb415bfa518f3a04e1165471d7b6557e168e4e4fa1581d7e1a103de08"),
    "run-receipt.json": (1654, "7b8ac9c712d2c7a528c5c9c0fc39d260ca0755029c3519031f8fe00b6a804d2b")}
E_SNAPSHOT = {"terminal": "PIVOT_CANDIDATE", "kind": "Separator", "rank": 1386, "generation": 8091,
    "state_head": "5e760f6a7c04a5eaf800289ab5b05ae542dc33c09b502ab7f87958b5e836a6a8",
    "target_remainder_sha256": "e902cf3b2d9a5a58ac47459877e017fa4d6a44c5868751b8690543665ae269c1",
    "lambda_sha256": "a16f4c8289e78efa068cfe923f1ee9a0d7b71f8c71aede582ff0ff93cda0c8ad"}
E_CHECKER_SHA = "a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4"
E_WORKFLOW = {"file": ".github/workflows/d972-r07-selected-cycle-materializer-v1.yml", "bytes": 44334,
    "sha256": "def1e1813427ebd530210cc743c79dd3e3b983114bd689c6a94d6c1154c75483"}
N, EDGES, P1_ROWS, LOWER, TOP, PHYSICAL = 54432, 108864, 8059, 96776, 36288, 48384
PHYSICAL_BYTES = 12096
OLD_OFFSETS, NEW_OFFSETS = (0, 505, 1008, 1511), (2014, 3523, 5035, 6547)
OLD_RANKS, NEW_RANKS = (505, 503, 503, 503), (1509, 1512, 1512, 1512)
PHASES = ("section", "cochain", "tree", "raw", "source", "primal", "p1", "B", "physical")
E_PHASES = PHASES[3:]
ASSURANCE = {"candidate": True, "cross_checked": False, "verified": False}
FORMULA = "v548-complete-oracle;v547-ordered-word;canonical-P1;four-B;dynamic-one-row"
SCOPE = {"vertices": N, "edges": EDGES, "chords": 54433, "legality_rows": 5,
    "normalized_auxiliaries": 2, "source_tags": 6, "characters": [0, 1, 2, 3],
    "p1_rows": P1_ROWS, "source_lower_trits": LOWER, "physical_trits": PHYSICAL,
    "source_universe_changed": False, "external_e_counted_as_new_step": False,
    "whole_normalized_word_replay": False, "eleven_slot_replay": False}
STARTED = time.monotonic()
DEADLINE: float | None = None
STOP_REQUESTED = False
OUTPUT_CREATED = False
CURRENT_PHASE = "initialization"


class ResourceStop(RuntimeError):
    pass


def require(ok: Any, label: str) -> None:
    if not ok:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    require("schema" not in body and "sha256" not in body, "reserved_seal_fields")
    unsigned = {"schema": SCHEMA + "." + kind, **body}
    return {**unsigned, "sha256": sha(canonical(unsigned))}


def sealed_ok(value: Any, kind: str | None = None) -> bool:
    return isinstance(value, dict) and (kind is None or value.get("schema") == SCHEMA + "." + kind) and \
        value.get("sha256") == sha(canonical({key: item for key, item in value.items() if key != "sha256"}))


def check_deadline(phase: str) -> None:
    global CURRENT_PHASE
    CURRENT_PHASE = phase
    if STOP_REQUESTED or (DEADLINE is not None and time.monotonic() >= DEADLINE):
        raise ResourceStop(phase)


def progress(phase: str, **fields: Any) -> None:
    check_deadline(phase)
    print(json.dumps({"phase": phase, "elapsed_seconds": round(time.monotonic() - STARTED, 6), **fields},
                     sort_keys=True), file=sys.stderr, flush=True)


def safe_path(root: Path, name: str, *, exists: bool = True) -> Path:
    relative = Path(name)
    require(not relative.is_absolute() and name != "" and
            all(part not in ("", ".", "..") for part in relative.parts), "relative_payload_path")
    require(not root.is_symlink(), "root_symlink")
    current = root
    for part in relative.parts:
        current = current / part
        require(not current.is_symlink(), "payload_symlink")
    require(root.resolve() in current.resolve().parents, "payload_within_root")
    if exists:
        require(current.is_file(), "payload_regular_file:" + name)
    return current


def read_fixed(root: Path, name: str, pin: tuple[int, str]) -> bytes:
    path = safe_path(root, name)
    with path.open("rb") as stream:
        raw = stream.read(pin[0])
        require(len(raw) == pin[0] and stream.read(1) == b"", "payload_exact_eof:" + name)
    require(sha(raw) == pin[1], "payload_hash:" + name)
    return raw


def decode_json(raw: bytes) -> Any:
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw, "canonical_json_bytes")
    return value


def read_json(root: Path, name: str, kind: str | None = None) -> Any:
    value = decode_json(safe_path(root, name).read_bytes())
    if kind is not None:
        require(sealed_ok(value, kind), "json_seal:" + name)
    return value


def file_pin(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "fixed_regular_file")
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while True:
            raw = stream.read(1 << 20)
            if not raw:
                break
            digest.update(raw)
            count += len(raw)
            check_deadline("fixed-file-pin")
    return {"bytes": count, "sha256": digest.hexdigest()}


def sync_directory(path: Path) -> None:
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def write_atomic(root: Path, name: str, raw: bytes, *, replace: bool = False) -> None:
    require(Path(name).name == name and name not in ("", ".", ".."), "atomic_basename")
    path = safe_path(root, name, exists=False)
    require(replace or not path.exists(), "fresh_atomic_file")
    pending = root / ("." + name + ".pending-" + uuid.uuid4().hex)
    with pending.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(pending, path)
    sync_directory(root)


def write_once(root: Path, name: str, raw: bytes) -> None:
    path = safe_path(root, name, exists=False)
    if path.exists():
        require(path.read_bytes() == raw, "immutable_output_changed:" + name)
    else:
        write_atomic(root, name, raw)


def own_dependencies() -> Any:
    path = safe_path(SEARCH, E_MODULE)
    require(sha(path.read_bytes()) == E_MODULE_SHA, "retained_e_producer_pin")
    spec = importlib.util.spec_from_file_location("task971_own_e", path)
    require(spec is not None and spec.loader is not None, "own_e_import_spec")
    e = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = e
    spec.loader.exec_module(e)
    e.check_deadline, e.progress = check_deadline, progress
    oracle, refinement, p2, m, base, descriptors = e.own_dependencies()
    return e, oracle, refinement, p2, m, base, descriptors


def payload_bytes(oracle: Any, value: Any, dtype: str, shape: Any = None) -> tuple[bytes, str, Any]:
    if dtype == "json":
        return canonical(value), "json", None
    if isinstance(value, bytes):
        require(shape is not None, "raw_payload_shape")
        raw = value
    else:
        array = np.asarray(value)
        require(shape is None or list(array.shape) == shape, "array_shape")
        shape = list(array.shape)
        if dtype == "packed3":
            raw = oracle.pack(array)
        elif dtype == "u8":
            require(not np.any(array < 0) and not np.any(array > 2), "u8_trit_range")
            raw = array.astype(np.uint8).tobytes(order="C")
        else:
            require(dtype == "u32le" and array.dtype.kind in "iu", "u32_integer_type")
            wide = array.astype(np.int64)
            require(not np.any(wide < 0) and not np.any(wide > 4294967295), "u32_range")
            raw = wide.astype("<u4").tobytes(order="C")
    decode_payload(oracle, raw, dtype, shape)
    return raw, dtype, shape


def decode_payload(oracle: Any, raw: bytes, dtype: str, shape: Any) -> Any:
    if dtype == "json":
        require(shape is None, "json_shape")
        return decode_json(raw)
    require(isinstance(shape, list) and all(type(x) is int and x >= 0 for x in shape), "payload_dimensions")
    count = math.prod(shape)
    if dtype == "packed3":
        value = oracle.unpack(raw, count)
    elif dtype == "u8":
        require(len(raw) == count, "u8_exact_length")
        value = np.frombuffer(raw, dtype=np.uint8)
        require(not np.any(value > 2), "u8_exact_trits")
    else:
        require(dtype == "u32le" and len(raw) == count * 4, "u32_exact_length")
        value = np.frombuffer(raw, dtype="<u4")
    return value.reshape(tuple(shape))


def decode_manifest_files(oracle: Any, root: Path, manifest: Any) -> tuple[Any, Any]:
    items = manifest["files"]
    require(isinstance(items, list) and [item["file"] for item in items] ==
            sorted({item["file"] for item in items}), "manifest_sorted_unique_roster")
    expected = {item["file"] for item in items} | {"manifest.json"}
    require({path.name for path in root.iterdir()} == expected and
            all(path.is_file() and not path.is_symlink() for path in root.iterdir()), "manifest_exact_directory")
    decoded, raws = {}, {}
    for item in items:
        require(set(item) == {"file", "bytes", "sha256", "dtype", "shape"} and
                Path(item["file"]).name == item["file"], "manifest_file_fields")
        raw = read_fixed(root, item["file"], (item["bytes"], item["sha256"]))
        raws[item["file"]] = raw
        decoded[item["file"]] = decode_payload(oracle, raw, item["dtype"], item["shape"])
    return decoded, raws


def phase_fields(binding: Any, phase: str, previous: str | None) -> dict[str, Any]:
    require(phase in PHASES, "known_phase")
    return {"phase": phase, **{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "fixed_manifest_sha256", "snapshot_sha256")},
        "previous_phase_manifest_sha256": previous}


def validate_phase_manifest(manifest: Any, binding: Any, phase: str, previous: str | None) -> None:
    expected = phase_fields(binding, phase, previous)
    require(sealed_ok(manifest, "phase-manifest") and
            set(manifest) == {"schema", "sha256", "files", *expected} and
            all(manifest[key] == value for key, value in expected.items()), "phase_same_snapshot_source_chain")


class PhaseStore:
    """Immutable complete phases; the HEAD selects a checkpoint separately."""
    def __init__(self, oracle: Any, root: Path, binding: Any, e: Any = None):
        self.oracle, self.root, self.binding, self.e = oracle, root, binding, e
        self.manifests: list[Any] = []
        self.hashes: list[str] = []
        self.values: dict[str, Any] = {}
        self.raws: dict[str, Any] = {}

    def directory(self, phase: str) -> Path:
        require(phase in PHASES, "phase_directory")
        return self.root / phase if phase in PHASES[:3] else self.root / "e" / phase

    def accept(self, phase: str, manifest: Any, values: Any, raws: Any) -> None:
        require(phase == PHASES[len(self.hashes)], "phase_order")
        validate_phase_manifest(manifest, self.binding, phase, self.hashes[-1] if self.hashes else None)
        if self.e is not None:
            validate_roster(manifest, registered_phase_roster(self.e, phase, values))
        telemetry = values["telemetry.json"]
        require(sealed_ok(telemetry, "phase-telemetry") and telemetry["phase"] == phase and
                all(type(telemetry[key]) in (int, float) and math.isfinite(telemetry[key]) and telemetry[key] >= 0
                    for key in ("elapsed_seconds", "begun_elapsed_seconds", "ended_elapsed_seconds")) and
                telemetry["ended_elapsed_seconds"] >= telemetry["begun_elapsed_seconds"] and
                abs(telemetry["elapsed_seconds"] - telemetry["ended_elapsed_seconds"] +
                    telemetry["begun_elapsed_seconds"]) < 0.000003 and
                telemetry["eof"] is True and telemetry["payload_bytes"] ==
                    sum(len(raw) for name, raw in raws.items() if name != "telemetry.json"), "phase_telemetry")
        self.manifests.append(manifest)
        self.hashes.append(sha(canonical(manifest)))
        self.values[phase], self.raws[phase] = values, raws

    def load(self) -> None:
        gap = False
        for phase in PHASES:
            path = self.directory(phase)
            if not path.exists():
                gap = True
                continue
            require(not gap and path.is_dir() and not path.is_symlink(), "consecutive_complete_phase_directories")
            manifest = read_json(path, "manifest.json", "phase-manifest")
            values, raws = decode_manifest_files(self.oracle, path, manifest)
            self.accept(phase, manifest, values, raws)
            check_deadline("load-complete-phase:" + phase)

    def commit(self, phase: str, payloads: Any, begun: float) -> Any:
        require(phase == PHASES[len(self.hashes)], "commit_next_phase")
        final = self.directory(phase)
        require(not final.exists() and not final.is_symlink(), "fresh_phase_directory")
        final.parent.mkdir(parents=True, exist_ok=True)
        pending = final.parent / (".pending-" + phase + "-" + uuid.uuid4().hex)
        pending.mkdir()
        payloads = dict(payloads)
        require("telemetry.json" not in payloads, "reserved_phase_telemetry")
        ended = time.monotonic()
        telemetry = seal("phase-telemetry", {"phase": phase, "elapsed_seconds": round(ended - begun, 6),
            "begun_elapsed_seconds": round(begun - STARTED, 6), "ended_elapsed_seconds": round(ended - STARTED, 6),
            "payload_bytes": sum(len(item[0]) for item in payloads.values()), "eof": True})
        payloads["telemetry.json"] = (canonical(telemetry), "json", None)
        files, values, raws = [], {}, {}
        for name in sorted(payloads):
            raw, dtype, shape = payloads[name]
            values[name] = decode_payload(self.oracle, raw, dtype, shape)
            raws[name] = raw
            write_atomic(pending, name, raw)
            files.append({"file": name, "bytes": len(raw), "sha256": sha(raw), "dtype": dtype, "shape": shape})
            check_deadline("write-phase:" + phase)
        manifest = seal("phase-manifest", {**phase_fields(self.binding, phase, self.hashes[-1] if self.hashes else None),
                                            "files": files})
        write_atomic(pending, "manifest.json", canonical(manifest))
        check_deadline("before-phase-publication:" + phase)
        os.replace(pending, final)
        sync_directory(final.parent)
        self.accept(phase, manifest, values, raws)
        # Caller commits the physical step and HEAD without another stop check.
        return manifest

    def checkpoint(self, oracle_manifest: str | None, witness: str | None) -> Any:
        return seal("checkpoint", {"snapshot_sha256": self.binding["snapshot_sha256"],
            "physical_parent_head": self.binding["physical_parent_head"],
            "last_complete_phase": PHASES[len(self.hashes) - 1] if self.hashes else None,
            "phase_manifests": [{"phase": phase, "sha256": digest} for phase, digest in zip(PHASES, self.hashes)],
            "current_oracle_manifest_sha256": oracle_manifest, "witness_sha256": witness})


E_ROSTER = {
    "owner.json": ("json", None), "start.json": ("json", None), "source.json": ("json", None),
    "raw-word.json": ("json", None), "raw-chain.bin": ("packed3", [EDGES]),
    "raw-source-d0.bin": ("packed3", [4, 6048]), "raw-source-d1.bin": ("packed3", [4, 18144]),
    "raw-source-d2.bin": ("packed3", [4, TOP]), "raw-source-aux.bin": ("packed3", [8]),
    "raw-source.json": ("json", None), "p1-coefficients.u8": ("u8", [P1_ROWS]),
    "p1-reductions.json": ("json", None), "p1-exponent-residues.json": ("json", None),
    "p1-roots.json": ("json", None), "source-lower-remainder.bin": ("packed3", [LOWER]),
    "source-top-corrected.bin": ("packed3", [4, TOP]), "source-correction.json": ("json", None),
    "physical-by-character.bin": ("packed3", [4, PHYSICAL]), "physical-raw.bin": ("packed3", [PHYSICAL]),
    "physical-remainder.bin": ("packed3", [PHYSICAL]), "physical-normalized.bin": ("packed3", [PHYSICAL]),
    "physical-literal.json": ("json", None), "instruction.json": ("json", None),
    "target-remainder.bin": ("packed3", [PHYSICAL]), "telemetry.json": ("json", None), "result.json": ("json", None),
}


def external_e_snapshot(head: Any, result: Any) -> Any:
    return {"terminal": result["terminal"], **{key: head[key] for key in
        ("kind", "rank", "generation", "state_head", "target_remainder_sha256", "lambda_sha256")}}


def validate_external_e_metadata(e: Any, objects: Any, expected_snapshot: Any) -> None:
    head, manifest, result, checked = (objects[name] for name in
        ("output/HEAD", "output/manifest.json", "output/result.json", "checker-result.json"))
    require(external_e_snapshot(head, result) == expected_snapshot, "external_e_snapshot_pin")
    require(checked["status"] == result["status"] == "PASS" and
            checked["terminal"] == result["terminal"] in ("PIVOT_CANDIDATE", "LINEAR_MEMBERSHIP_CANDIDATE") and
            checked["kind"] == result["kind"] == head["kind"] in ("Separator", "LinearMembershipCandidate"),
            "external_e_completed_type")
    require(checked["rank"] == head["rank"] == result["rank_after"] and
            checked["generation"] == head["generation"] == result["generation_after"] and
            checked["state_head"] == head["state_head"] == manifest["state_head"] == result["state_head"],
            "external_e_dynamic_head_join")
    for field, name in (("owner_sha256", "output/owner.json"), ("start_sha256", "output/start.json"),
                        ("result_sha256", "output/result.json"), ("manifest_sha256", "output/manifest.json"),
                        ("head_sha256", "output/HEAD")):
        require(checked[field] == sha(canonical(objects[name])), "external_e_checker_file_join:" + field)
    require(all(checked[key] is True for key in ("all_arrays_and_json_compared", "ordinary27_actual_raw_source",
        "direct_raw_word_replay", "source_lower_zero", "all_four_B_summed")) and
        checked["physical_appends"] == result["physical_appends"] == 1 and
        checked["source_lower_trits"] == LOWER and checked["p1_rows"] == P1_ROWS and
        checked["p1_literal_exponents_modulus"] == 54 and checked["completed_stages"] == list(E_PHASES) and
        checked["old_scans_numerically_replayed"] == checked["old_inserts_numerically_replayed"] == 0 and
        checked["old_oracle_arithmetic_replayed"] is False and checked["full_normalized_word_replay"] is False and
        checked["eleven_slot_replay"] is False and
        all(value["candidate"] is True and value["cross_checked"] is False and value["verified"] is False
            for value in (manifest, result, checked)), "external_e_complete_independent_scope")
    require(head["completed_steps"] == 1 and manifest["stage_eof"] == list(E_PHASES) and
            checked["selected_scalar"] == result["selected_scalar"] in (1, 2) and
            checked["target_scalar"] == result["target"]["scalar"] and
            checked["separator"] == result["separator"] and checked["target_derivation"] == result["target_derivation"],
            "external_e_one_row_receipts")
    require(result["target_derivation"]["original_rho2_directly_read"] is False and
            result["target_derivation"]["mode"] == "derived" and
            result["target_derivation"]["identity"] ==
                "parent_remainder - new_remainder = target.scalar * new_normalized_row", "external_e_derived_identity")


def read_external_e(e: Any, oracle: Any, root: Path) -> Any:
    require(E_ARTIFACT and E_FILES and E_SNAPSHOT and E_CHECKER_SHA, "actual_external_e_acceptance_pins_pending")
    required = {"output/HEAD", "output/manifest.json", "output/start.json", "output/owner.json", "output/source.json",
                "output/result.json", "checker-result.json", "source-receipt.json"}
    require(required <= set(E_FILES), "external_e_entry_pin_roster")
    objects = {name: decode_json(read_fixed(root, name, pin)) for name, pin in E_FILES.items()}
    for name, kind in (("output/HEAD", "head"), ("output/manifest.json", "manifest"), ("output/start.json", "start"),
                       ("output/owner.json", "owner"), ("output/source.json", "source"),
                       ("output/result.json", "result"), ("checker-result.json", "checker-result")):
        require(e.sealed_ok(objects[name], kind), "external_e_sealed_type:" + name)
    validate_external_e_metadata(e, objects, E_SNAPSHOT)
    head, manifest, result, checked = (objects[name] for name in
        ("output/HEAD", "output/manifest.json", "output/result.json", "checker-result.json"))
    require(checked["checker_sha256"] == E_CHECKER_SHA and
            objects["output/source.json"]["producer_sha256"] == E_MODULE_SHA, "external_e_source_pair_pin")
    source_files = {item["file"]: item for item in objects["source-receipt.json"]["files"]}
    require(source_files["search/" + E_MODULE]["sha256"] == E_MODULE_SHA and
            any(item["sha256"] == E_CHECKER_SHA for item in source_files.values()), "external_e_source_receipt_closure")
    run, intake = objects["run-receipt.json"], objects["oracle-intake-receipt.json"]
    require(run["schema"] == e.SCHEMA + ".run-receipt" and run["status"] == "PASS" and
            run["launch"] == {key: E_ARTIFACT[key] for key in ("run", "attempt", "head")} and
            run["workflow"] == E_WORKFLOW and run["terminal"] == E_SNAPSHOT["terminal"] and
            run["producer_invocations"] == run["checker_invocations"] == run["physical_appends"] == 1 and
            run["producer_result_sha256"] == E_FILES["output/result.json"][1] and
            run["checker_result_sha256"] == E_FILES["checker-result.json"][1] and
            run["source_receipt_sha256"] == E_FILES["source-receipt.json"][1] and
            run["oracle_intake_sha256"] == E_FILES["oracle-intake-receipt.json"][1] and
            run["oracle_unchanged"] is True and run["source_unchanged"] is True and
            run["old_oracle_arithmetic_replayed"] is False and run["v2_checker_imported_or_executed"] is False and
            run["oracle_artifact"] == intake["artifact"] == e.ORACLE_ARTIFACT and
            intake["schema"] == e.SCHEMA + ".oracle-intake" and intake["status"] == "PASS" and
            intake["entry_files"] == [{"file": name, "bytes": pin[0], "sha256": pin[1]}
                for name, pin in sorted(e.ORACLE_FILES.items())], "external_e_actual_run_and_oracle_intake")
    wanted = dict(E_ROSTER)
    if head["kind"] == "Separator":
        wanted["lambda.bin"] = ("packed3", [PHYSICAL])
    items = manifest["files"]
    require([item["file"] for item in items] == sorted(wanted), "external_e_full_payload_roster")
    output = root / "output"
    require(output.is_dir() and not output.is_symlink() and
            {path.name for path in output.iterdir()} == set(wanted) | {"manifest.json", "HEAD"},
            "external_e_exact_output_directory")
    values, raws = {}, {}
    for item in items:
        require(set(item) == {"file", "bytes", "sha256", "dtype", "shape"} and
                (item["dtype"], item["shape"]) == wanted[item["file"]], "external_e_registered_payload_type")
        raw = read_fixed(output, item["file"], (item["bytes"], item["sha256"]))
        values[item["file"]] = decode_payload(oracle, raw, item["dtype"], item["shape"])
        raws[item["file"]] = raw
        check_deadline("external-e-payload")
    for name in ("owner.json", "start.json", "source.json", "result.json"):
        require(values[name] == objects["output/" + name], "external_e_top_duplicate_join")
    instruction = values["instruction.json"]
    require(instruction["schema"] == e.SCHEMA + ".instruction" and
            instruction["rolling_sha256"] == head["state_head"] == sha(bytes.fromhex(instruction["predecessor"]) +
                canonical({key: value for key, value in instruction.items() if key != "rolling_sha256"})) and
            sha(raws["instruction.json"]) == checked["instruction_sha256"] == result["instruction_sha256"] ==
                manifest["instruction_sha256"] == head["instruction_sha256"], "external_e_rolling_instruction")
    for field, name in (("owner_sha256", "owner.json"), ("source_sha256", "source.json"), ("start_sha256", "start.json")):
        require(head[field] == manifest[field] == result[field] == sha(raws[name]), "external_e_owner_source_start")
    require(head["manifest_sha256"] == sha(canonical(manifest)) and
            manifest["result_sha256"] == sha(raws["result.json"]) and
            head["physical_sha256"] == instruction["physical_sha256"] == sha(raws["physical-normalized.bin"]) and
            head["target_remainder_sha256"] == sha(raws["target-remainder.bin"]) and
            head["lambda_sha256"] == (sha(raws["lambda.bin"]) if "lambda.bin" in raws else None),
            "external_e_physical_and_head_payloads")
    layout = seal("external-e-layout", {"artifact": E_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(E_FILES.items())],
        "manifest_sha256": sha(canonical(manifest)), "head_sha256": sha(canonical(head)),
        "start_sha256": sha(raws["start.json"]), "owner_sha256": sha(raws["owner.json"]),
        "source_sha256": sha(raws["source.json"]), "result_sha256": sha(raws["result.json"]),
        "instruction_sha256": sha(raws["instruction.json"]), "checker_result_sha256": E_FILES["checker-result.json"][1],
        **E_SNAPSHOT, "old_arithmetic_replayed": False})
    return {"objects": objects, "values": values, "raws": raws, "layout": layout}


def attach_e_delta(e: Any, oracle: Any, state: Any, instruction: Any, result: Any,
                   normalized: bytes, target: bytes, lambda_raw: bytes | None,
                   parent_receipt: Any) -> None:
    """Authenticate one completed delta's type; do not re-eliminate it."""
    require(state["kind"] == "Separator" and result["parent_state_head"] == instruction["predecessor"] == state["head"] and
            instruction["offer"] == state["generation"] and
            instruction["rank"] == result["rank_after"] == state["rank"] + 1 and
            result["rank_before"] == state["rank"] and
            instruction["generation"] == result["generation_after"] == state["generation"] + 1 and
            result["generation_before"] == state["generation"] and
            instruction["physical_offset"] == state["rank"] * PHYSICAL_BYTES and
            instruction["rolling_sha256"] == result["state_head"] == sha(bytes.fromhex(state["head"]) +
                canonical({key: value for key, value in instruction.items() if key != "rolling_sha256"})),
            "attach_e_parent_and_rolling_chain")
    row, remainder = oracle.unpack(normalized, PHYSICAL), oracle.unpack(target, PHYSICAL)
    lead, scale = instruction["lead"], instruction["sigma"]
    require(type(lead) is int and 0 <= lead < PHYSICAL and lead not in state["leads"] and
            type(scale) is int and scale in (1, 2) and row[lead] == 1 and not np.any(row[:lead]) and
            all(row[index] == remainder[index] == 0 for index in state["leads"]) and remainder[lead] == 0 and
            sha(normalized) == instruction["physical_sha256"] == result["pivot"]["normalized_sha256"] and
            result["pivot"]["lead"] == lead and result["pivot"]["scale"] == scale and
            result["pivot"]["reductions"] == instruction["physical_reductions"], "attach_e_normalized_row_type")
    e.validate_plain_target(result["target"], sha(state["target_raw"]), sha(target), instruction["target_scalar"])
    derivation = {"mode": "derived", "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": state["original_rho2_sha256"],
        "accepted_target_derivation_parents": state["target_parents"],
        "new_delta": {"instruction_sha256": sha(canonical(instruction)), "state_head": instruction["rolling_sha256"],
            "normalized_sha256": sha(normalized), "target_sha256": sha(canonical(result["target"]))},
        "identity": "parent_remainder - new_remainder = target.scalar * new_normalized_row"}
    require(result["target_derivation"] == derivation, "attach_e_named_target_derivation")
    if np.any(remainder):
        require(result["kind"] == "Separator" and result["terminal"] == "PIVOT_CANDIDATE" and
                lambda_raw is not None and result["separator"]["lambda_sha256"] == sha(lambda_raw) and
                result["separator"]["lambda_rho2"] == {"mode": "derived", "value": 1,
                    "original_rho2_directly_read": False, "target_derivation": derivation, "new_target_steps_executed": 1},
                "attach_e_separator_type")
        functional = oracle.unpack(lambda_raw, PHYSICAL)
    else:
        require(result["kind"] == "LinearMembershipCandidate" and result["terminal"] == "LINEAR_MEMBERSHIP_CANDIDATE" and
                result["separator"] is None and lambda_raw is None and result["positive_readout"] == "TASK958_PENDING",
                "attach_e_linear_zero_type")
        functional = None
    state["records"].append({"offer": instruction["offer"], "lead": lead, "physical_offset": instruction["physical_offset"],
        "rank": instruction["rank"], "rolling_sha256": instruction["rolling_sha256"]})
    state["rows"].append(normalized)
    state["leads"].append(lead)
    state["previous_target_raw"] = state["target_raw"]
    state.update({"rank": instruction["rank"], "generation": instruction["generation"],
        "head": instruction["rolling_sha256"], "kind": result["kind"], "target_raw": target,
        "lambda_raw": lambda_raw, "lambda": functional, "direct_pairing":
            result["separator"]["direct_pairing"] if functional is not None else None})
    state["target_parents"] = [*state["target_parents"], parent_receipt]


def target_parent(role: str, manifest_sha: str, instruction: Any, result: Any) -> Any:
    return {"role": role, "manifest_sha256": manifest_sha, "result_sha256": sha(canonical(result)),
        "instruction_sha256": sha(canonical(instruction)), "state_head": instruction["rolling_sha256"],
        "target_sha256": sha(canonical(result["target"]))}


def current_derived(state: Any) -> Any:
    if state["kind"] != "Separator":
        return None
    return {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": state["original_rho2_sha256"],
        "accepted_target_derivation_parents": state["target_parents"],
        "identity_convention": {"base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",
            "all_one_row_steps": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row"},
        "new_target_steps_executed": state["completed_steps"]}


def build_current_start(state: Any, binding: Any) -> Any:
    return seal("snapshot", {"owner_sha256": binding["owner_sha256"], "source_sha256": binding["source_sha256"],
        "start_sha256": binding["start_sha256"], "fixed_manifest_sha256": binding["fixed_manifest_sha256"],
        "step": state["completed_steps"], "kind": state["kind"], "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"]) if state["lambda_raw"] is not None else None,
        "target_remainder_sha256": sha(state["target_raw"]), "previous_target_remainder_sha256": sha(state["previous_target_raw"]),
        "accepted_target_derivation_parents": state["target_parents"], "lambda_rho2": current_derived(state),
        "direct_pairing": state["direct_pairing"]})


def boot(e: Any, oracle: Any, refinement: Any, p2: Any, m: Any, base: Any, descriptors: Any, args: Any) -> Any:
    external = read_external_e(e, oracle, args.e_root)
    accepted = e.read_oracle(oracle, args.oracle_root)
    state, anchor_start, anchor_owner, p1, task554, tables = oracle.accepted_snapshot(
        refinement, p2, m, base, descriptors, args)
    require(anchor_start == accepted["objects"]["output/start.json"] and
            anchor_owner == accepted["objects"]["output/owner.json"], "boot_same_anchor_snapshot")
    e_start, e_owner, e_source = (external["objects"]["output/" + name] for name in ("start.json", "owner.json", "source.json"))
    require(e_start == e.seal("start", {"kind": "Separator", "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"]), "target_remainder_sha256": sha(state["target_raw"]),
        "accepted_oracle_layout": accepted["layout"], **{key: anchor_start[key] for key in
            ("accepted_refinement_layout", "accepted_target_derivation_parents", "lambda_rho2", "direct_pairing")}}),
        "boot_external_e_start_exact_anchor")
    require(e_owner == e.seal("owner", {"formula_id": e.FORMULA, "scope": e.SCOPE,
        "oracle_owner_sha256": accepted["layout"]["owner_sha256"],
        "refinement_head_sha256": oracle.REFINEMENT_FILES["output/HEAD"][1],
        **{key: anchor_owner[key] for key in ("p1_parent", "task554_parent", "task712_parent",
             "task712_manifest_sha256", "word_dictionary_sha256", "relator_dictionary_sha256")}}), "boot_external_e_owner")
    expected_source = e.retained_source(oracle, refinement, p2)
    require(all(e_source[key] == expected_source[key] for key in ("producer_sha256", "modules", "data")) and
            external["objects"]["checker-result.json"]["accepted_oracle_layout"] == accepted["layout"],
            "boot_external_e_source_and_checker_parent")
    state["kind"] = "Separator"
    state["original_rho2_sha256"] = anchor_start["lambda_rho2"]["original_rho2_packed_sha256"]
    state["target_parents"] = copy.deepcopy(anchor_start["accepted_target_derivation_parents"])
    instruction, result = external["values"]["instruction.json"], external["values"]["result.json"]
    require(instruction["origin"]["oracle_manifest_sha256"] == accepted["layout"]["manifest_sha256"] and
            instruction["origin"]["witness_sha256"] == accepted["layout"]["witness_sha256"], "boot_e_same_oracle_witness")
    attach_e_delta(e, oracle, state, instruction, result, external["raws"]["physical-normalized.bin"],
        external["raws"]["target-remainder.bin"], external["raws"].get("lambda.bin"),
        target_parent("external-e", external["layout"]["manifest_sha256"], instruction, result))
    state["completed_steps"], state["last_step_manifest_sha256"] = 0, None
    if state["kind"] == "Separator":
        direct = m.check_final_separator(state["lambda"], state["rows"], state["previous_target_raw"], state["target_raw"])
        require(direct == state["direct_pairing"], "boot_e_current_direct_pairing")
    index = oracle.read_json(args.refinement_root, "output/canonical-index.json")
    return {"state": state, "anchor_start": anchor_start, "anchor_owner": anchor_owner,
        "accepted_oracle": accepted, "external_e": external, "p1": p1, "task554": task554,
        "tables": tables, "index": index}


def registered_phase_roster(e: Any, phase: str, values: Any) -> Any:
    if phase in PHASES[:3]:
        roster = dict(e.ORACLE_ROSTERS[phase])
    else:
        names = {
            "raw": ("raw-word.json", "raw-chain.bin"),
            "source": ("raw-source-d0.bin", "raw-source-d1.bin", "raw-source-d2.bin", "raw-source-aux.bin", "raw-source.json"),
            "primal": ("p1-coefficients.u8", "p1-reductions.json", "p1-exponent-residues.json"),
            "p1": ("p1-roots.json", "source-lower-remainder.bin", "source-top-corrected.bin", "source-correction.json"),
            "B": ("physical-by-character.bin", "physical-raw.bin"),
            "physical": ("physical-remainder.bin", "physical-normalized.bin", "target-remainder.bin",
                         "physical-literal.json", "instruction.json", "result.json")}[phase]
        roster = {name: E_ROSTER[name] for name in names}
        if phase == "B":
            roster["B.json"] = ("json", None)
        if phase == "physical" and values["result.json"]["kind"] == "Separator":
            roster["lambda.bin"] = ("packed3", [PHYSICAL])
    roster["telemetry.json"] = ("json", None)
    return roster


def validate_roster(manifest: Any, roster: Any) -> None:
    require([item["file"] for item in manifest["files"]] == sorted(roster) and
            all((item["dtype"], item["shape"]) == roster[item["file"]] for item in manifest["files"]),
            "registered_exact_payload_roster")


class BorrowedRows:
    def __init__(self, rows: Any):
        self.rows = rows

    def row(self, index: int) -> np.ndarray:
        return self.rows.row(index)

    def close(self) -> None:
        pass


class CachedOracle:
    """A narrow interface object; retained modules and their pins are immutable."""
    def __init__(self, oracle: Any, readers: Any, pins: Any):
        self.oracle, self.readers, self.pins = oracle, readers, pins

    def __getattr__(self, key: str) -> Any:
        return getattr(self.oracle, key)

    def PackedRows(self, root: Path, descriptor: Any) -> Any:
        key = (str(root.resolve()), descriptor["file"], descriptor["sha256"], descriptor["bytes"])
        require(key in self.readers, "only_registered_fixed_reader")
        return BorrowedRows(self.readers[key])

    def file_pin(self, path: Path) -> Any:
        key = str(path.resolve())
        require(key in self.pins, "only_registered_cached_file_pin")
        return dict(self.pins[key])


def fixed_roster(e: Any) -> Any:
    return {**e.ORACLE_ROSTERS["geometry"], "potential-tau.u8": ("u8", [N, 5]),
        "chord-tau.u8": ("u8", [54433, 5]), "selected-chords.u32": ("u32le", [5]),
        "canonical-index.json": ("json", None), "basis.json": ("json", None),
        "p1-exponent-residues.json": ("json", None)}


def fixed_manifest_body(binding: Any, accepted: Any, files: Any) -> Any:
    return {"owner_sha256": binding["owner_sha256"], "source_sha256": binding["source_sha256"],
        "scope": SCOPE, "accepted_geometry_stage_sha256": accepted["stages"]["geometry"],
        "fixed_values_independent_of_lambda": True, "files": files}


class FixedBundle:
    def __init__(self, e: Any, oracle: Any, base: Any, bundle: Any, output: Path, binding: Any):
        self.e, self.oracle, self.base = e, oracle, base
        self.readers, self.row_roles, self.pins = {}, {}, {}
        self.context, self.words = base.source_context()
        self.p1, self.task554, self.index = bundle["p1"], bundle["task554"], bundle["index"]
        accepted = bundle["accepted_oracle"]
        root = output / "fixed"
        roster = fixed_roster(e)
        if not root.exists():
            progress("fixed-basis-build-start", bodies=5)
            segments, _pairs, residues = e.basis_segments(oracle, base, self.task554, self.p1, self.index, self.words)
            serialized = [{key: value for key, value in segment.items() if key != "root"} for segment in segments]
            basis = seal("basis", {"segments": serialized, "rows": P1_ROWS, "lower_blobs": 12,
                "p1_manifest_sha256": self.p1["manifest_sha256"],
                "canonical_index_sha256": sha(canonical(self.index)),
                "lower_blob_pin_sha256": base.LOWER_BLOB_PIN_SHA256, "eof": True})
            values = {**accepted["arrays"]["geometry"], **{name: accepted["arrays"]["tree"][name] for name in
                ("potential-tau.u8", "chord-tau.u8", "selected-chords.u32")},
                "canonical-index.json": self.index, "basis.json": basis, "p1-exponent-residues.json": residues}
            pending = output / (".pending-fixed-" + uuid.uuid4().hex)
            pending.mkdir()
            entries = []
            for name in sorted(roster):
                raw, dtype, shape = payload_bytes(oracle, values[name], *roster[name])
                write_atomic(pending, name, raw)
                entries.append({"file": name, "bytes": len(raw), "sha256": sha(raw), "dtype": dtype, "shape": shape})
                check_deadline("fixed-payload-eof")
            manifest = seal("fixed-manifest", fixed_manifest_body(binding, accepted, entries))
            write_atomic(pending, "manifest.json", canonical(manifest))
            check_deadline("before-fixed-publication")
            os.rename(pending, root)
            sync_directory(output)
        require(root.is_dir() and not root.is_symlink(), "fixed_directory")
        self.manifest = read_json(root, "manifest.json", "fixed-manifest")
        require(self.manifest == seal("fixed-manifest", fixed_manifest_body(binding, accepted, self.manifest["files"])),
                "fixed_manifest_same_owner_and_sources")
        validate_roster(self.manifest, roster)
        self.values, self.raws = decode_manifest_files(oracle, root, self.manifest)
        self.digest = sha(canonical(self.manifest))
        for name in e.ORACLE_ROSTERS["geometry"]:
            require(self.raws[name] == payload_bytes(oracle, accepted["arrays"]["geometry"][name], *roster[name])[0],
                    "fixed_geometry_authenticated_original_bytes")
        for name in ("potential-tau.u8", "chord-tau.u8", "selected-chords.u32"):
            require(self.raws[name] == payload_bytes(oracle, accepted["arrays"]["tree"][name], *roster[name])[0],
                    "fixed_carry_authenticated_original_bytes")
        require(self.values["canonical-index.json"] == self.index, "fixed_canonical_index_parent")
        basis, residues = self.values["basis.json"], self.values["p1-exponent-residues.json"]
        require(sealed_ok(basis, "basis") and basis["rows"] == P1_ROWS and basis["lower_blobs"] == 12 and
                basis["eof"] is True and basis["p1_manifest_sha256"] == self.p1["manifest_sha256"] and
                basis["canonical_index_sha256"] == sha(canonical(self.index)) and
                basis["lower_blob_pin_sha256"] == base.LOWER_BLOB_PIN_SHA256, "fixed_basis_registered_parent")
        require(e.sealed_ok(residues, "p1-exponent-residues") and residues["rows"] == P1_ROWS and
                residues["modulus"] == 54 and residues["order"] == "canonical-row-id" and
                residues["method"] == "ordered-signed-DAG-exponent-mod54" and residues["eof"] is True and
                residues["p1_manifest_sha256"] == self.p1["manifest_sha256"] and
                residues["instruction_sha256"] == self.p1["instruction"]["sha256"] and
                len(residues["pairs"]) == P1_ROWS and all(isinstance(pair, list) and len(pair) == 2 and
                    all(type(value) is int and 0 <= value < 54 for value in pair) for pair in residues["pairs"]),
                "fixed_all8059_same_word_residue54")
        self.residues, self.pairs, self.segments = residues, residues["pairs"], copy.deepcopy(basis["segments"])
        require(len(self.segments) == 8, "fixed_eight_basis_segments")
        try:
            for index, segment in enumerate(self.segments):
                kind, owner = ("old", index) if index < 4 else ("new", index - 4)
                begin, rank = (OLD_OFFSETS[owner], OLD_RANKS[owner]) if kind == "old" else (NEW_OFFSETS[owner], NEW_RANKS[owner])
                parent = self.task554["prepare"] if kind == "old" else self.task554["blocks"][owner]
                require(segment["kind"] == kind and segment["owner"] == owner and segment["start"] == begin and
                        segment["body_sha256"] == parent["body"]["sha256"] and
                        segment["rows"] == rank and len(segment["leads"]) == rank and
                        len(set(segment["leads"])) == rank and
                        all(type(lead) is int and 0 <= lead < (6056 if kind == "old" else 18144) for lead in segment["leads"]),
                        "fixed_segment_type_and_leads")
                segment["root"] = Path(parent["root"]).resolve()
                descriptors = (("lower", segment["lower_descriptor"]), ("grade", segment["grade_descriptor"])) \
                    if kind == "old" else (("basis", segment["basis_descriptor"]),)
                for role, descriptor in descriptors:
                    width = {"lower": 6056, "grade": 72576, "basis": 18144}[role]
                    require(descriptor["rows"] == rank and descriptor["width"] == width, "fixed_blob_registered_dimensions")
                    reader = oracle.PackedRows(segment["root"], descriptor)
                    key = (str(segment["root"].resolve()), descriptor["file"], descriptor["sha256"], descriptor["bytes"])
                    require(key not in self.readers, "fixed_unique_blob_reader")
                    self.readers[key] = reader
                    self.row_roles[kind, owner, role] = reader
            require(len(self.readers) == 12, "all12_fixed_readers")
            instruction = oracle.safe_file(self.p1["root"], self.p1["instruction"]["path"])
            pin = file_pin(instruction)
            require(pin == {key: self.p1["instruction"][key] for key in ("bytes", "sha256")}, "fixed_p1_instruction_full_eof")
            self.pins[str(instruction.resolve())] = pin
        except Exception:
            self.close()
            raise
        self.proxy = CachedOracle(oracle, self.readers, self.pins)
        self.geometry = {"next": self.values["next-pos.u32"], "prev": self.values["prev-pos.u32"],
            "parent": self.values["parent.u32"], "parent_edge": self.values["parent-edge.u32"],
            "order": self.values["bfs-order.u32"], "phi": self.values["phi.u32"], "carry": self.values["carry.u8"],
            "chords": self.values["chord-edges.u32"], "chord_set": set(int(x) for x in self.values["chord-edges.u32"]),
            "tags": self.values["tag-fox.json"]["tags"], "maps": oracle.RightMaps(base.ARITH, self.context)}
        progress("fixed-bundle-ready", readers=12, rows=P1_ROWS)

    def row(self, kind: str, owner: int, role: str, local: int) -> np.ndarray:
        return self.row_roles[kind, owner, role].row(local)

    def close(self) -> None:
        for reader in self.readers.values():
            reader.close()
        self.readers.clear()


def current_section_cached(oracle: Any, base: Any, tables: Any, state: Any, fixed: FixedBundle) -> Any:
    q, values = oracle.current_roots_and_values(base, tables, state, fixed.p1)
    chi = (np.sum(values, axis=0, dtype=np.uint32) % 3).astype(np.uint8)
    k1 = np.zeros((4, 18144), dtype=np.uint8)
    original, embedded = np.zeros(P1_ROWS, dtype=np.uint32), np.zeros(P1_ROWS, dtype=np.uint32)
    new_order = []
    for owner, segment in enumerate(fixed.segments[4:]):
        begin, leads = NEW_OFFSETS[owner], segment["leads"]
        k1[owner], order = oracle.interpolate_rows(18144, leads, chi[begin:begin + len(leads)],
            lambda local, owner=owner: fixed.row("new", owner, "basis", local))
        for local, lead in enumerate(leads):
            original[begin + local], embedded[begin + local] = lead, 24192 + owner * 18144 + lead
        new_order.extend(begin + local for local in order)
        progress("current-section-new", owner=owner, rows=len(leads))
    beta = np.empty(2014, dtype=np.uint8)
    old_leads, old_owner_local = [0] * 2014, [None] * 2014
    for owner, segment in enumerate(fixed.segments[:4]):
        for local, lead in enumerate(segment["leads"]):
            index = OLD_OFFSETS[owner] + local
            beta[index] = (int(chi[index]) - oracle.dot(k1, fixed.row("old", owner, "grade", local))) % 3
            old_leads[index] = owner * 6048 + lead if lead < 6048 else 24192 + lead - 6048
            original[index] = lead
            embedded[index] = owner * 6048 + lead if lead < 6048 else 96768 + lead - 6048
            old_owner_local[index] = owner, local
            if (local + 1) % 128 == 0:
                check_deadline("old-grade-beta")

    def old_row(index: int) -> np.ndarray:
        owner, local = old_owner_local[index]
        row = fixed.row("old", owner, "lower", local)
        lead = int(original[index])
        require(row[lead] == 1 and not np.any(row[:lead]) and (owner == 0 or not np.any(row[6048:])),
                "old_shared_aux_original_lead")
        embedded_row = np.zeros(24200, dtype=np.uint8)
        embedded_row[owner * 6048:(owner + 1) * 6048] = row[:6048]
        embedded_row[24192:] = row[6048:]
        return embedded_row

    kE, old_order = oracle.interpolate_rows(24200, old_leads, beta, old_row)
    kappa = np.concatenate((kE[:24192], k1.reshape(-1), kE[24192:]))
    require(kappa.shape == (LOWER,), "joint_kappa_shape")
    equations = np.empty(P1_ROWS, dtype=np.uint8)
    for owner, segment in enumerate(fixed.segments[:4]):
        for local in range(segment["rows"]):
            index = OLD_OFFSETS[owner] + local
            equations[index] = (oracle.dot(kE, old_row(index)) + oracle.dot(k1, fixed.row("old", owner, "grade", local))) % 3
            if (local + 1) % 128 == 0:
                check_deadline("final-old-kappa-equalities")
    for owner, segment in enumerate(fixed.segments[4:]):
        for local in range(segment["rows"]):
            equations[NEW_OFFSETS[owner] + local] = oracle.dot(k1[owner], fixed.row("new", owner, "basis", local))
            if (local + 1) % 256 == 0:
                check_deadline("final-new-kappa-equalities")
    residuals = ((equations.astype(np.int16) - chi.astype(np.int16)) % 3).astype(np.uint8)
    require(not np.any(residuals) and len(new_order) == 6045 and len(old_order) == 2014 and
            len(set(int(x) for x in embedded)) == P1_ROWS, "all8059_joint_kappa_equalities")
    metadata = oracle.seal("section", {"rows": P1_ROWS, "old_rows": 2014, "new_rows": 6045,
        "source_lower_trits": LOWER, "shared_auxiliaries": 8,
        "formula": "v548:chi=sum_a<B_a^*lambda,z_i[a]>;kappa(b_i)=chi_i",
        "solve_order": "new-owner-major-descending-original-lead;old-global-descending-embedded-original-lead",
        "free_coordinates": 0, "p1_cache_sha256": fixed.p1["cache"]["sha256"],
        "lower_blob_pin_sha256": base.LOWER_BLOB_PIN_SHA256, "p1_passes": 1,
        "all_equations_checked": P1_ROWS, "equation_eof": True, "old_arithmetic_replayed": False})
    arrays = {"q.bin": (q, "packed3"), "p1-values.u8": (values, "u8"), "chi.u8": (chi, "u8"),
        "equation-values.u8": (equations, "u8"), "equation-residuals.u8": (residuals, "u8"),
        "beta.u8": (beta, "u8"), "kappa.bin": (kappa, "packed3"), "lead-original.u32": (original, "u32le"),
        "lead-embedded.u32": (embedded, "u32le"), "new-solve-order.u32": (np.asarray(new_order), "u32le"),
        "old-solve-order.u32": (np.asarray(old_order), "u32le"), "section.json": (metadata, "json")}
    progress("current-section-complete", equations=P1_ROWS)
    return {"arrays": arrays, "q": q, "kappa": kappa}


def loop_source(e: Any, oracle: Any, refinement: Any, p2: Any, bundle: Any) -> Any:
    retained = e.retained_source(oracle, refinement, p2)
    return seal("source", {"producer_sha256": sha(Path(__file__).read_bytes()),
        "modules": {E_MODULE: E_MODULE_SHA, **retained["modules"]}, "data": retained["data"],
        "python": sys.version, "numpy": np.__version__, "parent_provenance": {
            "oracle_source_sha256": e.ORACLE_FILES["output/source.json"][1],
            "oracle_original_source_receipt_sha256": e.ORACLE_FILES["source-receipt.json"][1],
            "oracle_completion_checker_result_sha256": e.ORACLE_FILES["checker-result.json"][1],
            "oracle_completion_receipt_sha256": e.ORACLE_FILES["completion-run-receipt.json"][1],
            "external_e_source_sha256": E_FILES["output/source.json"][1],
            "external_e_source_receipt_sha256": E_FILES["source-receipt.json"][1],
            "external_e_checker_result_sha256": E_FILES["checker-result.json"][1],
            "external_e_checker_sha256": E_CHECKER_SHA}})


def loop_owner(bundle: Any) -> Any:
    anchor = bundle["anchor_owner"]
    return seal("owner", {"formula_id": FORMULA, "scope": SCOPE,
        "external_e_owner_sha256": bundle["external_e"]["layout"]["owner_sha256"],
        "external_e_layout_sha256": sha(canonical(bundle["external_e"]["layout"])),
        "oracle_owner_sha256": bundle["accepted_oracle"]["layout"]["owner_sha256"],
        **{key: anchor[key] for key in ("p1_parent", "task554_parent", "task712_parent",
            "task712_manifest_sha256", "word_dictionary_sha256", "relator_dictionary_sha256")}})


def loop_start(bundle: Any) -> Any:
    state = bundle["state"]
    return seal("start", {"kind": state["kind"], "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "completed_steps": 0,
        "lambda_sha256": sha(state["lambda_raw"]) if state["lambda_raw"] is not None else None,
        "target_remainder_sha256": sha(state["target_raw"]),
        "previous_target_remainder_sha256": sha(state["previous_target_raw"]),
        "accepted_external_e_layout": bundle["external_e"]["layout"],
        "accepted_oracle_layout": bundle["accepted_oracle"]["layout"],
        "accepted_refinement_layout": bundle["anchor_start"]["accepted_refinement_layout"],
        "accepted_target_derivation_parents": state["target_parents"], "lambda_rho2": current_derived(state),
        "direct_pairing": state["direct_pairing"], "external_e_attached": 1, "external_e_numerically_replayed": False})


def head_value(state: Any, binding: Any, snapshot: Any = None, checkpoint: Any = None) -> Any:
    require((snapshot is None) == (checkpoint is None), "head_snapshot_checkpoint_pair")
    return seal("head", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256")},
        "completed_steps": state["completed_steps"], "last_step_manifest_sha256": state["last_step_manifest_sha256"],
        "kind": state["kind"], "rank": state["rank"], "generation": state["generation"], "state_head": state["head"],
        "target_remainder_sha256": sha(state["target_raw"]),
        "lambda_sha256": sha(state["lambda_raw"]) if state["lambda_raw"] is not None else None,
        "current_snapshot_sha256": sha(canonical(snapshot)) if snapshot is not None else None,
        "current_checkpoint_sha256": sha(canonical(checkpoint)) if checkpoint is not None else None})


def publish_checkpoint(output: Path, state: Any, binding: Any, snapshot: Any, store: PhaseStore,
                       oracle_manifest: Any = None, witness: Any = None) -> Any:
    checkpoint = store.checkpoint(sha(canonical(oracle_manifest)) if oracle_manifest is not None else None,
                                  sha(canonical(witness)) if witness is not None else None)
    directory = store.root / "checkpoints"
    directory.mkdir(exist_ok=True)
    require(not directory.is_symlink(), "checkpoint_directory")
    write_once(directory, sha(canonical(checkpoint)) + ".json", canonical(checkpoint))
    head = head_value(state, binding, snapshot, checkpoint)
    write_atomic(output, "HEAD", canonical(head), replace=True)
    return head


def oracle_completion(snapshot: Any, binding: Any, store: PhaseStore, terminal: str, witness: Any) -> Any:
    require(len(store.hashes) >= 3 and terminal in ("COMPLETE_ZERO_CANDIDATE", "VIOLATION_CANDIDATE"),
            "only_completed_current_oracle")
    stages = {phase: store.hashes[index] for index, phase in enumerate(PHASES[:3])}
    result = seal("oracle-result", {"status": "PASS", "terminal": terminal,
        **{key: binding[key] for key in ("owner_sha256", "source_sha256", "fixed_manifest_sha256", "snapshot_sha256")},
        **{key: snapshot[key] for key in ("step", "rank", "generation", "state_head", "lambda_sha256",
             "target_remainder_sha256", "lambda_rho2", "direct_pairing")},
        "stage_manifests": stages, "section_equalities": P1_ROWS, "chords_checked": 54433, "auxiliary_tests": 2,
        "witness_sha256": sha(canonical(witness)), "materialization": witness["materialization"],
        "new_physical_appends": 0, "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0,
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False, **ASSURANCE})
    manifest = seal("oracle-manifest", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "fixed_manifest_sha256", "snapshot_sha256")},
        "stage_manifests": stages, "result_sha256": sha(canonical(result)),
        "witness_sha256": sha(canonical(witness)), "terminal": terminal, "stage_eof": list(PHASES[:3]), **ASSURANCE})
    write_once(store.root, "oracle-result.json", canonical(result))
    write_once(store.root, "oracle-manifest.json", canonical(manifest))
    return result, manifest


def restore_section(oracle: Any, fixed: FixedBundle, values: Any) -> Any:
    meta = values["section.json"]
    require(oracle.sealed_ok(meta, "section") and meta["rows"] == meta["all_equations_checked"] == P1_ROWS and
            meta["old_rows"] == 2014 and meta["new_rows"] == 6045 and meta["source_lower_trits"] == LOWER and
            meta["shared_auxiliaries"] == 8 and meta["equation_eof"] is True and meta["p1_passes"] == 1 and
            meta["p1_cache_sha256"] == fixed.p1["cache"]["sha256"] and
            meta["lower_blob_pin_sha256"] == fixed.base.LOWER_BLOB_PIN_SHA256 and
            not np.any(values["equation-residuals.u8"]) and
            np.array_equal(values["equation-values.u8"], values["chi.u8"]), "restored_complete_section_type")
    require(len(set(int(x) for x in values["lead-embedded.u32"])) == P1_ROWS and
            set(int(x) for x in values["new-solve-order.u32"]) == set(range(2014, P1_ROWS)) and
            set(int(x) for x in values["old-solve-order.u32"]) == set(range(2014)), "restored_section_full_orders")
    for segment in fixed.segments:
        start, rank = segment["start"], segment["rows"]
        require(values["lead-original.u32"][start:start + rank].tolist() == segment["leads"],
                "restored_same_fixed_original_leads")
    return {"q": values["q.bin"], "kappa": values["kappa.bin"]}


def restore_cochain(oracle: Any, values: Any) -> Any:
    meta = values["cochain.json"]
    require(oracle.sealed_ok(meta, "cochain") and meta["tags"] == 6 and meta["components"] == 2 and
            meta["vertices"] == N and meta["edges"] == EDGES and meta["score_eof"] is True and
            meta["edge_eof"] is True and meta["shared_eta"] is True and meta["physical_mixed_C_used"] is False,
            "restored_complete_cochain_type")
    return {"f": values["f.u8"], "b_aux": values["b-aux.u8"]}


def restore_tree(oracle: Any, fixed: FixedBundle, cochain: Any, values: Any) -> Any:
    meta, witness = values["tree.json"], values["witness.json"]
    require(oracle.sealed_ok(meta, "tree") and oracle.sealed_ok(witness, "witness") and
            meta["vertices"] == N and meta["tree_edges"] == N - 1 and meta["chords"] == 54433 and
            meta["independent_tau_columns"] == 5 and meta["full_chord_eof"] is True and
            meta["selected_chords"] == values["selected-chords.u32"].tolist() and
            meta["fit"] == values["fit.u8"].tolist() and meta["aux_values"] == cochain["b_aux"].tolist() and
            meta["materialization"] == witness["materialization"], "restored_complete_tree_type")
    for name in ("potential-tau.u8", "chord-tau.u8", "selected-chords.u32"):
        require(np.array_equal(values[name], fixed.values[name]), "restored_tree_fixed_carry")
    failed = np.flatnonzero(values["chord-residuals.u8"])
    require(meta["residual_nonzero"] == len(failed) and meta["first_failed_chord"] ==
            (int(fixed.geometry["chords"][int(failed[0])]) if len(failed) else None), "restored_tree_complete_failure_roster")
    if meta["terminal"] == "COMPLETE_ZERO_CANDIDATE":
        require(witness["kind"] == "none" and witness["scalar"] == 0 and witness["cycles"] == [] and
                witness["eta"] == [0, 0] and witness["tau"] == [0] * 5 and len(failed) == 0 and
                not np.any(cochain["b_aux"]) and witness["materialization"] == "NOT_NEEDED_FOR_ZERO_TEST",
                "restored_complete_zero_not_unknown")
    else:
        require(meta["terminal"] == "VIOLATION_CANDIDATE" and witness["kind"] in ("chord", "auxiliary") and
                type(witness["scalar"]) is int and witness["scalar"] in (1, 2) and
                witness["tau"] == [0] * 5 and witness["materialization"] == "MATERIALIZATION_PENDING",
                "restored_violation_type")
        if witness["kind"] == "chord":
            require(witness["failed_chord"] == meta["first_failed_chord"] and witness["eta"] == [0, 0] and
                    witness["basis_chords"] == meta["selected_chords"] and len(witness["basis_coefficients"]) == 5 and
                    witness["cycles"] == [{"edge": witness["failed_chord"], "coefficient": 1}] +
                        [{"edge": edge, "coefficient": (-coefficient) % 3} for edge, coefficient in
                            zip(witness["basis_chords"], witness["basis_coefficients"])], "restored_all_six_cycle_ancestry")
        else:
            coordinate = witness["coordinate"]
            require(type(coordinate) is int and coordinate in (0, 1) and witness["cycles"] == [] and
                    witness["eta"] == [int(index == coordinate) for index in range(2)] and
                    witness["scalar"] == int(cochain["b_aux"][coordinate]), "restored_auxiliary_witness")
    return {"terminal": meta["terminal"], "witness": witness, "metadata": meta}


def dynamic_oracle_input(fixed: FixedBundle, snapshot: Any, binding: Any, store: PhaseStore,
                         section: Any, cochain: Any, tree: Any, manifest: Any) -> Any:
    require(manifest["snapshot_sha256"] == binding["snapshot_sha256"] == sha(canonical(snapshot)) and
            manifest["witness_sha256"] == sha(canonical(tree["witness"])) and
            manifest["terminal"] == tree["terminal"], "dynamic_oracle_same_current_witness")
    return {"geometry": fixed.geometry, "stages": {"geometry": fixed.digest,
        **{phase: store.hashes[index] for index, phase in enumerate(PHASES[:3])}},
        "layout": {"manifest_sha256": sha(canonical(manifest)), "witness_sha256": manifest["witness_sha256"],
            "terminal": tree["terminal"], "snapshot_sha256": binding["snapshot_sha256"],
            "state_head": snapshot["state_head"], "lambda_sha256": snapshot["lambda_sha256"]},
        "witness": tree["witness"], "q": section["q"], "kappa": section["kappa"],
        "f": cochain["f"], "b_aux": cochain["b_aux"]}


def check_current_witness(state: Any, snapshot: Any, accepted: Any) -> None:
    require(state["kind"] == "Separator" and state["head"] == snapshot["state_head"] == accepted["layout"]["state_head"] and
            sha(state["lambda_raw"]) == snapshot["lambda_sha256"] == accepted["layout"]["lambda_sha256"] and
            state["completed_steps"] == snapshot["step"] and sha(canonical(snapshot)) == accepted["layout"]["snapshot_sha256"] and
            accepted["layout"]["witness_sha256"] == sha(canonical(accepted["witness"])) and
            accepted["layout"]["terminal"] == "VIOLATION_CANDIDATE" and accepted["witness"]["scalar"] in (1, 2),
            "fresh_current_lambda_witness_required")


def restore_raw(e: Any, oracle: Any, fixed: FixedBundle, accepted: Any, values: Any) -> Any:
    record = values["raw-word.json"]
    require(e.sealed_ok(record, "raw-word") and record["grammar"] == "ordered-slp-v1" and record["root"] == "raw-root" and
            record["geometry_manifest_sha256"] == fixed.digest and
            record["witness_sha256"] == accepted["layout"]["witness_sha256"] and
            record["cycles"] == accepted["witness"]["cycles"] and record["eta"] == accepted["witness"]["eta"] and
            record["word_stream"]["full_eof"] is True and
            record["word_stream"]["letters"] == record["word_stream"]["bytes"] == record["word_bound"]["actual_slp_length"],
            "restored_raw_same_witness_and_eof")
    legality = record["legality"]
    require(all(legality[key] is True for key in ("q0_identity", "q2_identity", "epsilon_divisible18", "omega_zero",
                "normalizer_Q2_Fox_zero", "raw_chain_matches_witness")) and
            legality["tau"] == [0] * 5 and legality["normalized_pair"] == record["eta"] and legality["omega"] == 0,
            "restored_raw_legality_receipt")
    normalizers, normalizer_receipt = e.normalizer_dictionary(oracle)
    require(record["normalizers"] == normalizer_receipt, "restored_same_normalizer_dictionary")
    # Rehydrate typed evaluated nodes. No add/product/Fox evaluation of the
    # completed raw phase runs here; a subsequent source phase emits its word.
    slp = object.__new__(e.RawSLP)
    slp.oracle, slp.arith, slp.context, slp.geometry = oracle, fixed.base.ARITH, fixed.context, fixed.geometry
    slp.normalizers, slp.q0_identity, slp.q0 = normalizers, tuple(range(36)), None
    slp.nodes, slp.records, slp.values, slp.refs = record["nodes"], {}, {}, {}
    receipts = record["node_values"]
    require(len(receipts) == len(slp.nodes) and [item["id"] for item in receipts] == [item["id"] for item in slp.nodes],
            "restored_all_raw_node_receipts")
    for node, receipt in zip(slp.nodes, receipts):
        name, operation = node["id"], node["op"]
        require(isinstance(name, str) and name not in slp.records and
                set(receipt) == {"id", "exponent", "omega", "length", "q0", "q2"} and
                len(receipt["exponent"]) == 2 and all(type(item) is int for item in receipt["exponent"]) and
                type(receipt["omega"]) is int and receipt["omega"] in (0, 1, 2) and
                type(receipt["length"]) is int and receipt["length"] >= 0 and
                type(receipt["q2"]) is int and 0 <= receipt["q2"] < N and
                sorted(receipt["q0"]) == list(range(36)), "restored_raw_node_typed_value")
        if operation == "Ref":
            require(set(node) == {"id", "op", "namespace", "key"}, "restored_ref_fields")
            if node["namespace"] == "oracle-tree":
                require(type(node["key"]) is int and 0 <= node["key"] < N, "restored_tree_ref_key")
                slp.refs[name] = slp.tree_word(node["key"])
            else:
                require(node["namespace"] == "normalizer-v459" and node["key"] in ("r_x", "r_y"), "restored_normalizer_ref")
                slp.refs[name] = normalizers[node["key"]]
            require(receipt["length"] == len(slp.refs[name]), "restored_reference_length")
        elif operation == "OrderedProduct":
            require(set(node) == {"id", "op", "factors"} and all(child in slp.records for child in node["factors"]),
                    "restored_ordered_prior_nodes")
        elif operation in ("Inverse", "IntegerPower"):
            require(set(node) == ({"id", "op", "node"} if operation == "Inverse" else {"id", "op", "node", "exponent"}) and
                    node["node"] in slp.records and (operation == "Inverse" or type(node["exponent"]) is int),
                    "restored_signed_prior_node")
        elif operation == "Letter":
            require(set(node) == {"id", "op", "letter"} and type(node["letter"]) is int and node["letter"] in (-2, -1, 1, 2),
                    "restored_signed_letter")
        else:
            require(operation == "Identity" and set(node) == {"id", "op"}, "restored_identity_node")
        slp.records[name] = node
        slp.values[name] = {"scalar": (*receipt["exponent"], receipt["omega"]), "length": receipt["length"],
            "q0": tuple(receipt["q0"]), "q2": e.q2_value(fixed.context, receipt["q2"])}
    require(slp.nodes[-1]["id"] == "raw-root" and slp.values["raw-root"]["length"] == record["word_stream"]["letters"] and
            slp.values["raw-root"]["q0"] == slp.q0_identity and
            slp.values["raw-root"]["q2"] == fixed.base.ARITH.SEED_AFFINE_IDENTITY and
            slp.values["raw-root"]["scalar"][2] == 0 and
            all(value % 18 == 0 for value in slp.values["raw-root"]["scalar"][:2]) and
            [value // 18 % 3 for value in slp.values["raw-root"]["scalar"][:2]] == record["eta"],
            "restored_raw_root_same_legal_value")
    return {"slp": slp, "record": record, "chain": values["raw-chain.bin"], "eta": record["eta"]}


def restore_source(e: Any, oracle: Any, refinement: Any, m: Any, accepted: Any, raw: Any, values: Any) -> Any:
    parts = tuple(values["raw-source-" + name + ".bin"] for name in ("d0", "d1", "d2", "aux"))
    record = values["raw-source.json"]
    require(e.sealed_ok(record, "raw-source") and record["components"] == refinement.component_receipts(m, parts) and
            record["raw_word_sha256"] == sha(canonical(raw["record"])) and record["chain_sha256"] == sha(oracle.pack(raw["chain"])) and
            record["eta"] == raw["eta"] == parts[3][6:].tolist() and
            record["source_lower_sha256"] == sha(oracle.pack(e.lower_row(parts))) and
            record["source_full_top_sha256"] == sha(oracle.pack(parts[2])) and
            record["direct_raw_word_replay"] is True and record["full_tag_eof"] is True and
            [item["tag"] for item in record["tag_chain_receipts"]] == list(range(6)) and
            all(item["direct_fox_same"] is True and item["q2_endpoint"] == 0 for item in record["tag_chain_receipts"]) and
            record["witness_scalar"] == accepted["witness"]["scalar"] ==
                (record["homogeneous_scalar"] - record["section_scalar"]) % 3, "restored_same_complete_six_tag_source")
    return {"parts": parts, "record": record, "homogeneous": record["homogeneous_scalar"], "section": record["section_scalar"]}


def restore_primal(e: Any, oracle: Any, fixed: FixedBundle, values: Any) -> Any:
    alpha, record = values["p1-coefficients.u8"], values["p1-reductions.json"]
    require(e.sealed_ok(record, "p1-reductions") and record["rows"] == P1_ROWS and record["eof"] is True and
            record["order"] == "old-global-ascending-embedded-original-lead;new-owner-major-ascending-original-lead" and
            record["coefficients_sha256"] == sha(alpha.tobytes()) and
            values["p1-exponent-residues.json"] == fixed.residues, "restored_primal_same_alpha_and_word_residues")
    events = record["events"]
    nodes, order = [], []
    for index, event in enumerate(events):
        kind, owner, local, node = (event[key] for key in ("kind", "owner", "local", "node"))
        require(kind in ("old", "new") and type(owner) is int and 0 <= owner < 4 and type(local) is int,
                "restored_primal_event_owner")
        segment = fixed.segments[owner + (4 if kind == "new" else 0)]
        require(0 <= local < segment["rows"] and node == segment["start"] + local and event["event"] == index and
                event["original_lead"] == segment["leads"][local] and event["coefficient"] == int(alpha[node]) in (1, 2) and
                event["literal_exponent"] == -e.signrep(event["coefficient"]), "restored_primal_ordered_event")
        lead = event["original_lead"]
        embedded = (owner * 6048 + lead if lead < 6048 else 96768 + lead - 6048) if kind == "old" else 24192 + owner * 18144 + lead
        require(event["embedded_lead"] == embedded, "restored_primal_original_lead_embedding")
        nodes.append(node)
        order.append((0, embedded) if kind == "old" else (1 + owner, lead))
    require(len(set(nodes)) == len(nodes) and set(nodes) == set(int(x) for x in np.flatnonzero(alpha)) and order == sorted(order),
            "restored_primal_complete_nonzero_order")
    lower = np.zeros(LOWER, dtype=np.uint8)
    require(record["lower_zero"] == {"trits": LOWER, "packed_sha256": sha(oracle.pack(lower))}, "restored_primal_full_zero_receipt")
    return {"alpha": alpha, "events": events, "lower": lower, "record": record}


def restore_corrected(e: Any, oracle: Any, refinement: Any, m: Any, fixed: FixedBundle, raw: Any, primal: Any, values: Any) -> Any:
    lower, top = values["source-lower-remainder.bin"], values["source-top-corrected.bin"]
    parts = (lower[:24192].reshape(4, 6048), lower[24192:96768].reshape(4, 18144), top, lower[96768:])
    roots, record = values["p1-roots.json"], values["source-correction.json"]
    require(e.sealed_ok(roots, "p1-roots") and roots["p1_manifest_sha256"] == fixed.p1["manifest_sha256"] and
            roots["instruction_sha256"] == fixed.p1["instruction"]["sha256"] and roots["cache_sha256"] == fixed.p1["cache"]["sha256"] and
            roots["canonical_index_sha256"] == sha(canonical(fixed.index)) and roots["all_references_authenticated"] is True and
            [item["node"] for item in roots["roots"]] == sorted(int(x) for x in np.flatnonzero(primal["alpha"])),
            "restored_all_selected_p1_references")
    require(e.sealed_ok(record, "source-correction") and record["raw_word_sha256"] == sha(canonical(raw["record"])) and
            record["p1_roots_sha256"] == sha(canonical(roots)) and record["coefficients_sha256"] == sha(primal["alpha"].tobytes()) and
            record["components"] == refinement.component_receipts(m, parts) and not np.any(lower) and
            record["source_lower_zero"] == {"trits": LOWER, "packed_sha256": sha(oracle.pack(lower))} and
            record["source_lower_equality"] is True and record["top_characters"] == [0, 1, 2, 3] and
            record["normalized_pair"] == [0, 0] and record["exponent_residue_mod54"] == [0, 0] and
            record["canonical_p1_source_replay"] is True, "restored_full_corrected_source")
    return {"parts": parts, "roots": roots, "record": record}


def B_receipt(oracle: Any, accepted: Any, corrected: Any, physical: Any) -> Any:
    return seal("B", {"characters": [0, 1, 2, 3], "physical_trits": PHYSICAL,
        "source_correction_sha256": sha(canonical(corrected["record"])), "witness_sha256": accepted["layout"]["witness_sha256"],
        "corrected_scalar": physical["corrected_scalar"], "physical_scalar": physical["physical_scalar"],
        "raw_sha256": sha(physical["raw"]), "by_character_sha256": sha(oracle.pack(physical["by_character"])),
        "all_four_summed": True, "eof": True})


def restore_B(oracle: Any, accepted: Any, corrected: Any, values: Any, raws: Any) -> Any:
    record = values["B.json"]
    physical = {"by_character": values["physical-by-character.bin"], "raw": raws["physical-raw.bin"],
        "corrected_scalar": record["corrected_scalar"], "physical_scalar": record["physical_scalar"]}
    require(record == B_receipt(oracle, accepted, corrected, physical) and
            physical["corrected_scalar"] == physical["physical_scalar"] == accepted["witness"]["scalar"] in (1, 2),
            "restored_all_four_B_complete_receipt")
    return physical


def restore_physical(e: Any, state: Any, snapshot: Any, owner: Any, source_pin: Any, accepted: Any,
                     raw: Any, source: Any, primal: Any, corrected: Any, physical: Any, values: Any, raws: Any) -> Any:
    check_current_witness(state, snapshot, accepted)
    result, instruction, literal = (values[name] for name in ("result.json", "instruction.json", "physical-literal.json"))
    require(e.sealed_ok(result, "result") and e.sealed_ok(literal, "physical-literal") and result["status"] == "PASS" and
            result["owner_sha256"] == sha(canonical(owner)) and result["start_sha256"] == sha(canonical(snapshot)) and
            result["source_sha256"] == sha(canonical(source_pin)) and result["parent_state_head"] == state["head"] and
            instruction["schema"] == e.SCHEMA + ".instruction" and instruction["predecessor"] == state["head"] and
            instruction["origin"] == {"kind": "v548-cycle" if accepted["witness"]["kind"] == "chord" else "v548-aux",
                "oracle_manifest_sha256": accepted["layout"]["manifest_sha256"],
                "witness_sha256": accepted["layout"]["witness_sha256"], "raw_word_sha256": sha(canonical(raw["record"]))},
            "restored_physical_exact_current_inputs")
    for key, digest in (("raw_word_sha256", sha(canonical(raw["record"]))),
        ("source_correction_sha256", sha(canonical(corrected["record"]))),
        ("physical_literal_sha256", sha(canonical(literal))), ("p1_roots_sha256", sha(canonical(corrected["roots"]))),
        ("instruction_sha256", sha(canonical(instruction)))):
        require(result[key] == digest, "restored_physical_result_ref:" + key)
    require(instruction["source_correction_sha256"] == result["source_correction_sha256"] and
            instruction["physical_literal_sha256"] == result["physical_literal_sha256"] and
            instruction["p1_roots_sha256"] == result["p1_roots_sha256"] and
            instruction["p1_reductions_sha256"] == sha(canonical(primal["record"])) and
            result["homogeneous_scalar"] == source["homogeneous"] and result["section_scalar"] == source["section"] and
            result["corrected_scalar"] == physical["corrected_scalar"] and
            result["selected_scalar"] == result["physical_scalar"] == result["remainder_scalar"] ==
                instruction["selected_scalar"] == physical["physical_scalar"] == accepted["witness"]["scalar"] in (1, 2) and
            result["physical_appends"] == 1 and all(result[key] == value for key, value in ASSURANCE.items()),
            "restored_physical_full_scalar_and_literal_chain")
    return {"remainder": raws["physical-remainder.bin"], "normalized": raws["physical-normalized.bin"],
        "target": raws["target-remainder.bin"], "lambda": raws.get("lambda.bin"),
        "literal": literal, "instruction": instruction, "result": result}


def current_tree_cached(oracle: Any, fixed: FixedBundle, cochain: Any) -> Any:
    geometry, f = fixed.geometry, cochain["f"]
    potential = oracle.integrate_tree(geometry["next"], geometry["parent"], geometry["parent_edge"], geometry["order"], f)
    chords, tau = geometry["chords"], fixed.values["chord-tau.u8"]
    values = oracle.chord_values(geometry["next"], chords, f, potential)
    selected = np.searchsorted(chords, fixed.values["selected-chords.u32"]).astype(np.int64).tolist()
    require(len(selected) == 5 and all(index < 54433 for index in selected) and
            np.array_equal(chords[selected], fixed.values["selected-chords.u32"]), "fixed_selected_actual_chord_ids")
    fit = oracle.solve_five(tau[selected], values[selected])
    residuals = ((values.astype(np.int32) - tau.astype(np.int32) @ fit.astype(np.int32)) % 3).astype(np.uint8)
    check_deadline("all-current-chord-residuals-complete")
    terminal, witness, metadata = oracle.classify_complete(chords, tau, values, residuals, selected, fit,
        cochain["b_aux"], 54433, True)
    arrays = {"potential-f.u8": (potential, "u8"), "potential-tau.u8": (fixed.values["potential-tau.u8"], "u8"),
        "chord-values.u8": (values, "u8"), "chord-tau.u8": (tau, "u8"), "chord-residuals.u8": (residuals, "u8"),
        "selected-chords.u32": (fixed.values["selected-chords.u32"], "u32le"), "fit.u8": (fit, "u8"),
        "witness.json": (witness, "json"), "tree.json": (metadata, "json")}
    progress("complete-current-tree", chords=54433, terminal=terminal)
    return {"arrays": arrays, "terminal": terminal, "witness": witness, "metadata": metadata}


def serialize_arrays(oracle: Any, arrays: Any) -> Any:
    return {name: payload_bytes(oracle, value, dtype) for name, (value, dtype) in arrays.items()}


def ensure_phase(store: PhaseStore, phase: str, builder: Callable[[], Any]) -> bool:
    if phase in store.values:
        return False
    begun = time.monotonic()
    progress("phase-start", phase_name=phase)
    payloads = builder()
    store.commit(phase, payloads, begun)
    return True


def restore_snapshot(e: Any, oracle: Any, refinement: Any, m: Any, fixed: FixedBundle, state: Any,
                     snapshot: Any, owner: Any, source_pin: Any, store: PhaseStore, *, committed: bool = False) -> Any:
    answer: dict[str, Any] = {}
    if "section" in store.values:
        answer["section"] = restore_section(oracle, fixed, store.values["section"])
    if "cochain" in store.values:
        answer["cochain"] = restore_cochain(oracle, store.values["cochain"])
    if "tree" in store.values:
        answer["tree"] = restore_tree(oracle, fixed, answer["cochain"], store.values["tree"])
        if committed:
            require(all((store.root / name).is_file() for name in ("oracle-result.json", "oracle-manifest.json")),
                    "committed_oracle_metadata_must_exist")
        answer["oracle_result"], answer["oracle_manifest"] = oracle_completion(snapshot, store.binding, store,
            answer["tree"]["terminal"], answer["tree"]["witness"])
        answer["accepted"] = dynamic_oracle_input(fixed, snapshot, store.binding, store, answer["section"],
            answer["cochain"], answer["tree"], answer["oracle_manifest"])
    if "raw" in store.values:
        check_current_witness(state, snapshot, answer["accepted"])
        answer["raw"] = restore_raw(e, oracle, fixed, answer["accepted"], store.values["raw"])
    if "source" in store.values:
        answer["source"] = restore_source(e, oracle, refinement, m, answer["accepted"], answer["raw"], store.values["source"])
    if "primal" in store.values:
        answer["primal"] = restore_primal(e, oracle, fixed, store.values["primal"])
    if "p1" in store.values:
        answer["corrected"] = restore_corrected(e, oracle, refinement, m, fixed, answer["raw"], answer["primal"], store.values["p1"])
    if "B" in store.values:
        answer["physical"] = restore_B(oracle, answer["accepted"], answer["corrected"], store.values["B"], store.raws["B"])
    if "physical" in store.values:
        answer["row"] = restore_physical(e, state, snapshot, owner, source_pin, answer["accepted"], answer["raw"],
            answer["source"], answer["primal"], answer["corrected"], answer["physical"], store.values["physical"], store.raws["physical"])
    return answer


def finish_snapshot(e: Any, oracle: Any, refinement: Any, m: Any, base: Any, bundle: Any, fixed: FixedBundle,
                    output: Path, state: Any, binding: Any, snapshot: Any, owner: Any, source_pin: Any,
                    store: PhaseStore) -> Any:
    ensure_phase(store, "section", lambda: serialize_arrays(oracle,
        current_section_cached(oracle, base, bundle["tables"], state, fixed)["arrays"]))
    section = restore_section(oracle, fixed, store.values["section"])
    if len(store.hashes) == 1:
        publish_checkpoint(output, state, binding, snapshot, store)
    ensure_phase(store, "cochain", lambda: serialize_arrays(oracle,
        oracle.source_cochain(base.ARITH, fixed.context, fixed.geometry, section)["arrays"]))
    cochain = restore_cochain(oracle, store.values["cochain"])
    if len(store.hashes) == 2:
        publish_checkpoint(output, state, binding, snapshot, store)
    ensure_phase(store, "tree", lambda: serialize_arrays(oracle, current_tree_cached(oracle, fixed, cochain)["arrays"]))
    tree = restore_tree(oracle, fixed, cochain, store.values["tree"])
    oracle_result, oracle_manifest = oracle_completion(snapshot, store.binding, store, tree["terminal"], tree["witness"])
    accepted = dynamic_oracle_input(fixed, snapshot, store.binding, store, section, cochain, tree, oracle_manifest)
    if len(store.hashes) == 3:
        publish_checkpoint(output, state, binding, snapshot, store, oracle_manifest, tree["witness"])
    if tree["terminal"] == "COMPLETE_ZERO_CANDIDATE":
        require(len(store.hashes) == 3, "zero_oracle_has_no_materialization_phase")
        return {"oracle_result": oracle_result, "oracle_manifest": oracle_manifest, "tree": tree}
    check_current_witness(state, snapshot, accepted)

    def raw_payloads() -> Any:
        raw = e.selected_raw_word(oracle, base.ARITH, fixed.context, accepted)
        return {"raw-word.json": payload_bytes(oracle, raw["record"], "json"),
                "raw-chain.bin": payload_bytes(oracle, raw["chain"], "packed3")}

    ensure_phase(store, "raw", raw_payloads)
    raw = restore_raw(e, oracle, fixed, accepted, store.values["raw"])
    if len(store.hashes) == 4:
        publish_checkpoint(output, state, binding, snapshot, store, oracle_manifest, tree["witness"])

    def source_payloads() -> Any:
        source = e.source_from_chain(oracle, refinement, m, base.ARITH, fixed.context, accepted, raw)
        return {**{"raw-source-" + name + ".bin": payload_bytes(oracle, part, "packed3")
                    for name, part in zip(("d0", "d1", "d2", "aux"), source["parts"])},
                "raw-source.json": payload_bytes(oracle, source["record"], "json")}

    ensure_phase(store, "source", source_payloads)
    source = restore_source(e, oracle, refinement, m, accepted, raw, store.values["source"])
    if len(store.hashes) == 5:
        publish_checkpoint(output, state, binding, snapshot, store, oracle_manifest, tree["witness"])

    def primal_payloads() -> Any:
        primal = e.primal_section(fixed.proxy, m, fixed.segments, source["parts"])
        return {"p1-coefficients.u8": payload_bytes(oracle, primal["alpha"], "u8"),
            "p1-reductions.json": payload_bytes(oracle, primal["record"], "json"),
            "p1-exponent-residues.json": payload_bytes(oracle, fixed.residues, "json")}

    ensure_phase(store, "primal", primal_payloads)
    primal = restore_primal(e, oracle, fixed, store.values["primal"])
    if len(store.hashes) == 6:
        publish_checkpoint(output, state, binding, snapshot, store, oracle_manifest, tree["witness"])

    def correction_payloads() -> Any:
        corrected = e.corrected_source(fixed.proxy, refinement, m, fixed.p1, fixed.index, fixed.segments,
            fixed.pairs, raw, source, primal)
        return {"p1-roots.json": payload_bytes(oracle, corrected["roots"], "json"),
            "source-lower-remainder.bin": payload_bytes(oracle, e.lower_row(corrected["parts"]), "packed3"),
            "source-top-corrected.bin": payload_bytes(oracle, corrected["parts"][2], "packed3"),
            "source-correction.json": payload_bytes(oracle, corrected["record"], "json")}

    ensure_phase(store, "p1", correction_payloads)
    corrected = restore_corrected(e, oracle, refinement, m, fixed, raw, primal, store.values["p1"])
    if len(store.hashes) == 7:
        publish_checkpoint(output, state, binding, snapshot, store, oracle_manifest, tree["witness"])

    def B_payloads() -> Any:
        physical = e.four_B(oracle, m, bundle["tables"], state, accepted, corrected)
        return {"physical-by-character.bin": payload_bytes(oracle, physical["by_character"], "packed3"),
            "physical-raw.bin": payload_bytes(oracle, physical["raw"], "packed3", [PHYSICAL]),
            "B.json": payload_bytes(oracle, B_receipt(oracle, accepted, corrected, physical), "json")}

    ensure_phase(store, "B", B_payloads)
    physical = restore_B(oracle, accepted, corrected, store.values["B"], store.raws["B"])
    if len(store.hashes) == 8:
        publish_checkpoint(output, state, binding, snapshot, store, oracle_manifest, tree["witness"])

    def physical_payloads() -> Any:
        check_current_witness(state, snapshot, accepted)
        row = e.one_physical_row(oracle, m, state, snapshot, owner, source_pin, accepted, raw, source, primal, corrected, physical)
        payloads = {name: payload_bytes(oracle, row[key], "packed3", [PHYSICAL]) for name, key in
            (("physical-remainder.bin", "remainder"), ("physical-normalized.bin", "normalized"),
             ("target-remainder.bin", "target"), ("lambda.bin", "lambda")) if row[key] is not None}
        payloads.update({name: payload_bytes(oracle, row[key], "json") for name, key in
            (("physical-literal.json", "literal"), ("instruction.json", "instruction"), ("result.json", "result"))})
        return payloads

    ensure_phase(store, "physical", physical_payloads)
    # Deliberately no cooperative deadline between complete physical publication
    # and commit_step's step manifest/HEAD publication in the caller.
    row = restore_physical(e, state, snapshot, owner, source_pin, accepted, raw, source, primal, corrected, physical,
        store.values["physical"], store.raws["physical"])
    return {"row": row, "oracle_result": oracle_result, "oracle_manifest": oracle_manifest, "tree": tree}


def step_manifest(state: Any, binding: Any, snapshot: Any, store: PhaseStore, answer: Any) -> Any:
    row, result, instruction = answer["row"], answer["row"]["result"], answer["row"]["instruction"]
    require(len(store.hashes) == len(PHASES) and result["parent_state_head"] == state["head"], "all_phases_before_step")
    return seal("step-manifest", {**{key: binding[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256")},
        "step": state["completed_steps"] + 1, "snapshot_sha256": sha(canonical(snapshot)),
        "oracle_manifest_sha256": sha(canonical(answer["oracle_manifest"])),
        "witness_sha256": sha(canonical(answer["tree"]["witness"])),
        "predecessor_step_manifest_sha256": state["last_step_manifest_sha256"],
        "parent_state_head": state["head"], "state_head": instruction["rolling_sha256"],
        "rank": result["rank_after"], "generation": result["generation_after"], "kind": result["kind"],
        "instruction_sha256": sha(canonical(instruction)), "result_sha256": sha(canonical(result)),
        "physical_normalized_sha256": sha(row["normalized"]), "target_remainder_sha256": sha(row["target"]),
        "lambda_sha256": sha(row["lambda"]) if row["lambda"] is not None else None,
        "phase_manifests": {phase: store.hashes[index] for index, phase in enumerate(PHASES)},
        "phase_eof": list(PHASES), **ASSURANCE})


def attach_step(e: Any, oracle: Any, state: Any, manifest: Any, row: Any) -> None:
    step = state["completed_steps"] + 1
    require(manifest["step"] == step and manifest["predecessor_step_manifest_sha256"] == state["last_step_manifest_sha256"],
            "next_step_not_reset")
    digest = sha(canonical(manifest))
    attach_e_delta(e, oracle, state, row["instruction"], row["result"], row["normalized"], row["target"], row["lambda"],
        target_parent("loop-e-" + format(step, "06d"), digest, row["instruction"], row["result"]))
    state["completed_steps"], state["last_step_manifest_sha256"] = step, digest


def commit_step(e: Any, oracle: Any, output: Path, state: Any, binding: Any, snapshot: Any,
                store: PhaseStore, answer: Any) -> Any:
    manifest = step_manifest(state, binding, snapshot, store, answer)
    publish_step_manifest(output, manifest)
    attach_step(e, oracle, state, manifest, answer["row"])
    head = head_value(state, binding)
    publish_committed_head(output, head)
    return head


def publish_step_manifest(output: Path, manifest: Any) -> None:
    require(sealed_ok(manifest, "step-manifest"), "step_manifest_seal_before_publication")
    root = output / "steps" / format(manifest["step"], "06d")
    root.mkdir(parents=True, exist_ok=True)
    require(not root.is_symlink() and all(path.name == "manifest.json" or pending_file(path) for path in root.iterdir()),
            "step_directory_only_manifest")
    write_once(root, "manifest.json", canonical(manifest))


def publish_committed_head(output: Path, head: Any) -> None:
    require(sealed_ok(head, "head"), "head_seal_before_publication")
    write_atomic(output, "HEAD", canonical(head), replace=True)


def cap_reached(completed: int, limit: int) -> bool:
    require(type(completed) is int and completed >= 0 and type(limit) is int and limit >= 0, "absolute_cap_integer")
    return completed >= limit


def pending_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink() and re.fullmatch(r"\.[A-Za-z0-9_.-]+\.pending-[0-9a-f]{32}", path.name) is not None


def pending_directory(path: Path, names: Any) -> bool:
    return path.is_dir() and not path.is_symlink() and any(
        re.fullmatch(r"\.pending-" + re.escape(name) + r"-[0-9a-f]{32}", path.name) is not None for name in names)


def validate_snapshot_directory(root: Path) -> None:
    require(root.is_dir() and not root.is_symlink(), "snapshot_regular_directory")
    files = {"start.json", "oracle-result.json", "oracle-manifest.json"}
    directories = {"section", "cochain", "tree", "e", "checkpoints"}
    for path in root.iterdir():
        require(not path.is_symlink(), "snapshot_no_symlink")
        if path.name in files:
            require(path.is_file(), "snapshot_top_file_type")
        elif path.name in directories:
            require(path.is_dir(), "snapshot_child_directory_type")
        else:
            require((pending_file(path) and any(path.name.startswith("." + name + ".pending-") for name in files)) or
                    pending_directory(path, PHASES[:3]), "snapshot_named_diagnostic_only")
    e_root = root / "e"
    if e_root.exists():
        for path in e_root.iterdir():
            require((path.name in E_PHASES and path.is_dir() and not path.is_symlink()) or
                    pending_directory(path, E_PHASES), "e_phase_or_named_diagnostic_only")


def validate_output_directory(output: Path, completed: int | None) -> None:
    files = {"owner.json", "source.json", "start.json", "HEAD", "result.json", "resource-stop.json", "rejected.json"}
    directories = {"fixed", "snapshots", "steps", "invocations"}
    for path in output.iterdir():
        require(not path.is_symlink(), "output_no_symlink")
        if path.name in files:
            require(path.is_file(), "output_file_type")
        elif path.name in directories:
            require(path.is_dir(), "output_directory_type")
        else:
            require((pending_file(path) and any(path.name.startswith("." + name + ".pending-") for name in files)) or
                    pending_directory(path, ("fixed",)), "output_named_diagnostic_only")
    for name, first, extra in (("snapshots", 0, 0), ("steps", 1, 1)):
        root = output / name
        if not root.exists():
            continue
        for path in root.iterdir():
            require(path.is_dir() and not path.is_symlink() and re.fullmatch(r"[0-9]{6}", path.name) is not None,
                    "only_numbered_snapshot_or_step")
            require(completed is not None and first <= int(path.name) <= completed + extra,
                    "unreachable_numbered_tail_rejected")
    root = output / "invocations"
    if root.exists():
        for path in root.iterdir():
            require((path.is_file() and not path.is_symlink() and re.fullmatch(r"[0-9a-f]{32}\.json", path.name) is not None) or
                    pending_file(path), "invocation_named_receipt_only")


def snapshot_store(e: Any, oracle: Any, output: Path, state: Any, binding: Any, *, create: bool) -> Any:
    root = output / "snapshots" / format(state["completed_steps"], "06d")
    snapshot = build_current_start(state, binding)
    if create:
        root.mkdir(parents=True, exist_ok=True)
        validate_snapshot_directory(root)
        write_once(root, "start.json", canonical(snapshot))
    else:
        validate_snapshot_directory(root)
        require(read_json(root, "start.json", "snapshot") == snapshot, "committed_snapshot_exact_current_state")
    phase_binding = {**binding, "snapshot_sha256": sha(canonical(snapshot)), "physical_parent_head": state["head"]}
    store = PhaseStore(oracle, root, phase_binding, e)
    store.load()
    return snapshot, store


def expected_checkpoint(store: PhaseStore, count: int, answer: Any) -> Any:
    require(type(count) is int and 0 <= count <= len(store.hashes), "checkpoint_complete_prefix_length")
    return seal("checkpoint", {"snapshot_sha256": store.binding["snapshot_sha256"],
        "physical_parent_head": store.binding["physical_parent_head"],
        "last_complete_phase": PHASES[count - 1] if count else None,
        "phase_manifests": [{"phase": phase, "sha256": digest} for phase, digest in zip(PHASES[:count], store.hashes[:count])],
        "current_oracle_manifest_sha256": sha(canonical(answer["oracle_manifest"])) if count >= 3 else None,
        "witness_sha256": sha(canonical(answer["tree"]["witness"])) if count >= 3 else None})


def validate_checkpoints(store: PhaseStore, answer: Any) -> dict[str, Any]:
    root, values = store.root / "checkpoints", {}
    if not root.exists():
        return values
    require(root.is_dir() and not root.is_symlink(), "checkpoint_directory_type")
    for path in root.iterdir():
        if pending_file(path):
            continue
        require(path.is_file() and not path.is_symlink() and re.fullmatch(r"[0-9a-f]{64}\.json", path.name) is not None,
                "checkpoint_content_hash_filename")
        checkpoint = read_json(root, path.name, "checkpoint")
        count = len(checkpoint["phase_manifests"])
        require(checkpoint == expected_checkpoint(store, count, answer) and
                path.name == sha(canonical(checkpoint)) + ".json", "checkpoint_same_authenticated_phase_prefix")
        values[path.stem] = checkpoint
    return values


def validate_head_binding(head: Any, state: Any, binding: Any, snapshot: Any = None, checkpoints: Any = None) -> None:
    if head["current_snapshot_sha256"] is None:
        require(head == head_value(state, binding), "head_exact_attached_prefix")
    else:
        require(snapshot is not None and checkpoints is not None and
                head["current_checkpoint_sha256"] in checkpoints, "head_references_existing_complete_checkpoint")
        require(head == head_value(state, binding, snapshot, checkpoints[head["current_checkpoint_sha256"]]),
                "head_current_snapshot_checkpoint_binding")


def check_state_separator(m: Any, state: Any) -> None:
    if state["kind"] == "Separator":
        direct = m.check_final_separator(state["lambda"], state["rows"], state["previous_target_raw"], state["target_raw"])
        require(direct == state["direct_pairing"], "resumed_all_rows_and_both_targets")
    else:
        require(state["kind"] == "LinearMembershipCandidate" and state["lambda_raw"] is None and
                state["lambda"] is None and not any(state["target_raw"]), "linear_target_zero_without_separator")


def load_prefix(e: Any, oracle: Any, refinement: Any, m: Any, fixed: Any, output: Path, bundle: Any,
                binding: Any, owner: Any, source_pin: Any, head: Any) -> Any:
    state = bundle["state"]
    require(sealed_ok(head, "head") and type(head["completed_steps"]) is int and head["completed_steps"] >= 0,
            "head_typed_complete_count")
    validate_output_directory(output, head["completed_steps"])
    require(head["fixed_manifest_sha256"] == binding["fixed_manifest_sha256"], "resumed_same_fixed_manifest")
    for step in range(1, head["completed_steps"] + 1):
        require(fixed is not None and state["kind"] == "Separator", "only_separator_has_next_committed_step")
        snapshot, store = snapshot_store(e, oracle, output, state, binding, create=False)
        require(len(store.hashes) == 9, "committed_step_all_nine_phases")
        answer = restore_snapshot(e, oracle, refinement, m, fixed, state, snapshot, owner, source_pin, store, committed=True)
        validate_checkpoints(store, answer)
        root = output / "steps" / format(step, "06d")
        require(root.is_dir() and not root.is_symlink() and
                all(path.name == "manifest.json" or pending_file(path) for path in root.iterdir()), "committed_step_directory")
        manifest = read_json(root, "manifest.json", "step-manifest")
        require(manifest == step_manifest(state, binding, snapshot, store, answer), "committed_step_exact_phase_and_rolling_chain")
        attach_step(e, oracle, state, manifest, answer["row"])
        del store, answer, snapshot
        progress("completed-prefix-attached", steps=step, numerical_old_replay=0)
    current_root = output / "snapshots" / format(state["completed_steps"], "06d")
    snapshot, store, answer = None, None, {}
    if current_root.exists():
        require(fixed is not None and state["kind"] == "Separator", "no_oracle_after_linear_target_zero")
        snapshot, store = snapshot_store(e, oracle, output, state, binding,
            create=head["current_snapshot_sha256"] is None)
        answer = restore_snapshot(e, oracle, refinement, m, fixed, state, snapshot, owner, source_pin, store)
        checkpoints = validate_checkpoints(store, answer)
        validate_head_binding(head, state, binding, snapshot, checkpoints)
    else:
        validate_head_binding(head, state, binding)
        require(not (output / "steps" / format(state["completed_steps"] + 1, "06d")).exists(),
                "no_step_without_preceding_complete_snapshot")
    check_state_separator(m, state)
    if store is not None:
        if "physical" in store.values:
            # Durable physical may be ahead of HEAD. Reuse it; do not call E.
            head = commit_step(e, oracle, output, state, binding, snapshot, store, answer)
            check_state_separator(m, state)
            snapshot, store, answer = None, None, {}
        else:
            require(not (output / "steps" / format(state["completed_steps"] + 1, "06d")).exists(),
                    "step_manifest_requires_completed_physical")
            head = publish_checkpoint(output, state, binding, snapshot, store, answer.get("oracle_manifest"),
                answer["tree"]["witness"] if "tree" in answer else None)
    return state, head, snapshot, store, answer


def current_result(state: Any, binding: Any, head: Any, terminal: str, args: Any, *, oracle_result: Any = None) -> Any:
    require(terminal in ("COMPLETE_ZERO_CANDIDATE", "LINEAR_MEMBERSHIP_CANDIDATE", "UNKNOWN_CAP", "UNKNOWN_RESOURCE"),
            "registered_terminal_type")
    if terminal == "COMPLETE_ZERO_CANDIDATE":
        require(oracle_result is not None and oracle_result["terminal"] == terminal and state["kind"] == "Separator" and
                oracle_result["state_head"] == state["head"] and oracle_result["lambda_sha256"] == sha(state["lambda_raw"]),
                "complete_zero_requires_current_full_oracle")
    if terminal == "LINEAR_MEMBERSHIP_CANDIDATE":
        require(state["kind"] == "LinearMembershipCandidate" and state["lambda_raw"] is None and not any(state["target_raw"]),
                "linear_zero_is_not_group_membership")
    return seal("result", {"status": "PASS" if terminal.endswith("CANDIDATE") else terminal, "terminal": terminal,
        **{key: binding[key] for key in ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256")},
        "head_sha256": sha(canonical(head)), "invocation_sha256": args.invocation_sha256,
        "completed_steps": state["completed_steps"],
        "last_step_manifest_sha256": state["last_step_manifest_sha256"], "kind": state["kind"], "rank": state["rank"],
        "generation": state["generation"], "state_head": state["head"], "target_remainder_sha256": sha(state["target_raw"]),
        "lambda_sha256": sha(state["lambda_raw"]) if state["lambda_raw"] is not None else None,
        "lambda_rho2": current_derived(state), "direct_pairing": state["direct_pairing"],
        "current_snapshot_sha256": head["current_snapshot_sha256"], "current_checkpoint_sha256": head["current_checkpoint_sha256"],
        "complete_zero_oracle_result_sha256": sha(canonical(oracle_result)) if terminal == "COMPLETE_ZERO_CANDIDATE" else None,
        "new_physical_appends": state["completed_steps"], "external_e_attached": 1,
        "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0, "external_e_numerically_replayed": False,
        "positive_readout": "TASK958_PENDING" if terminal == "LINEAR_MEMBERSHIP_CANDIDATE" else "NOT_APPLICABLE",
        "separator_premises": "v548-Conn-same-source-map" if terminal == "COMPLETE_ZERO_CANDIDATE" else None,
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "max_appends_this_invocation": args.max_appends, "max_seconds_this_invocation": args.max_seconds,
        "elapsed_seconds": round(time.monotonic() - STARTED, 6), **ASSURANCE})


def run_loop(e: Any, oracle: Any, refinement: Any, m: Any, base: Any, fixed: Any, bundle: Any, args: Any,
             output: Path, binding: Any, owner: Any, source_pin: Any, head: Any) -> Any:
    state, head, snapshot, store, answer = load_prefix(e, oracle, refinement, m, fixed, output, bundle, binding, owner, source_pin, head)
    try:
        while True:
            if state["kind"] == "LinearMembershipCandidate":
                result = current_result(state, binding, head, "LINEAR_MEMBERSHIP_CANDIDATE", args)
                break
            if answer.get("tree", {}).get("terminal") == "COMPLETE_ZERO_CANDIDATE":
                result = current_result(state, binding, head, "COMPLETE_ZERO_CANDIDATE", args, oracle_result=answer["oracle_result"])
                break
            if cap_reached(state["completed_steps"], args.max_appends):
                result = current_result(state, binding, head, "UNKNOWN_CAP", args)
                break
            check_deadline("before-current-snapshot")
            if store is None:
                snapshot, store = snapshot_store(e, oracle, output, state, binding, create=True)
                require(not store.hashes, "fresh_next_snapshot_no_unreachable_phases")
                head = publish_checkpoint(output, state, binding, snapshot, store)
            answer = finish_snapshot(e, oracle, refinement, m, base, bundle, fixed, output, state, binding,
                snapshot, owner, source_pin, store)
            if "row" in answer:
                head = commit_step(e, oracle, output, state, binding, snapshot, store, answer)
                # The only cooperative stop below is after the durable HEAD.
                snapshot, store, answer = None, None, {}
                if state["kind"] == "Separator" and not cap_reached(state["completed_steps"], args.max_appends):
                    progress("new-E-committed", completed_steps=state["completed_steps"], rank=state["rank"], generation=state["generation"])
            else:
                head = read_json(output, "HEAD", "head")
    except ResourceStop:
        # A completed phase may be ahead of this invocation's cached `head`.
        # Physical publication cannot reach here before commit_step updates it.
        head = read_json(output, "HEAD", "head")
        result = current_result(state, binding, head, "UNKNOWN_RESOURCE", args)
    write_atomic(output, "result.json", canonical(result), replace=True)
    return result


def run_actual(args: Any) -> Any:
    global OUTPUT_CREATED
    e, oracle, refinement, p2, m, base, descriptors = own_dependencies()
    output = args.output_root.resolve()
    roots = [getattr(args, name) for name in ("state_root", "delta_root", "seed34_root", "packet_root", "refinement_root",
        "oracle_root", "e_root", "prepare_root", "p1_root", "task712_root")] + args.block_root
    require(not args.output_root.is_symlink() and (args.resume or not output.exists()), "same_output_requires_resume")
    require(not args.resume or (output.is_dir() and not output.is_symlink()), "resume_existing_output_directory")
    for parent in roots:
        resolved = parent.resolve()
        require(parent.is_dir() and not parent.is_symlink() and resolved != output and
                resolved not in output.parents and output not in resolved.parents, "loop_disjoint_parent_output")
    bundle = boot(e, oracle, refinement, p2, m, base, descriptors, args)
    owner, source_pin, start = loop_owner(bundle), loop_source(e, oracle, refinement, p2, bundle), loop_start(bundle)
    head = None
    if output.exists():
        head = read_json(output, "HEAD", "head") if (output / "HEAD").exists() else None
        validate_output_directory(output, head["completed_steps"] if head is not None else None)
        for name, value in (("owner.json", owner), ("source.json", source_pin), ("start.json", start)):
            path = output / name
            if path.exists():
                require(path.read_bytes() == canonical(value), "same_owner_source_start_on_resume:" + name)
            else:
                require(head is None, "committed_output_missing_immutable_metadata")
    check_deadline("before-loop-output-admission")
    output.mkdir(parents=True, exist_ok=True)
    OUTPUT_CREATED = True
    for name, value in (("owner.json", owner), ("source.json", source_pin), ("start.json", start)):
        write_once(output, name, canonical(value))
    binding = {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source_pin)),
        "start_sha256": sha(canonical(start)), "fixed_manifest_sha256": None}
    fixed = None
    try:
        if bundle["state"]["kind"] == "Separator":
            fixed = FixedBundle(e, oracle, base, bundle, output, binding)
            binding["fixed_manifest_sha256"] = fixed.digest
        else:
            require(not (output / "fixed").exists(), "no_fixed_arithmetic_after_external_linear_zero")
        if head is None:
            head = head_value(bundle["state"], binding)
            write_atomic(output, "HEAD", canonical(head))
        validate_invocations(output, binding)
        invocation_id = uuid.uuid4().hex
        invocation = seal("invocation", {"invocation": invocation_id, **{key: binding[key] for key in
            ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256")},
            "head_before_sha256": sha(canonical(head)), "completed_steps_before": head["completed_steps"],
            "resume": args.resume, "max_appends": args.max_appends, "max_seconds": args.max_seconds,
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        invocations = output / "invocations"
        invocations.mkdir(exist_ok=True)
        write_atomic(invocations, invocation_id + ".json", canonical(invocation))
        args.invocation_sha256 = sha(canonical(invocation))
        return run_loop(e, oracle, refinement, m, base, fixed, bundle, args, output, binding, owner, source_pin, head)
    finally:
        if fixed is not None:
            fixed.close()


def validate_invocations(output: Path, binding: Any) -> None:
    root = output / "invocations"
    if not root.exists():
        return
    digests = set()
    for path in root.iterdir():
        if pending_file(path):
            continue
        value = read_json(root, path.name, "invocation")
        require(value["invocation"] + ".json" == path.name and
                all(value[key] == binding[key] for key in ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256")) and
                isinstance(value["head_before_sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", value["head_before_sha256"]) is not None and
                type(value["completed_steps_before"]) is int and value["completed_steps_before"] >= 0 and
                type(value["resume"]) is bool and type(value["max_appends"]) is int and 0 <= value["max_appends"] < 999999 and
                type(value["max_seconds"]) in (int, float) and math.isfinite(value["max_seconds"]) and value["max_seconds"] > 0 and
                re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value["started_utc"]) is not None,
                "retained_invocation_same_owner_and_finite_limits")
        digests.add(sha(canonical(value)))
    if (output / "result.json").exists():
        result = read_json(output, "result.json", "result")
        require(result["invocation_sha256"] in digests and
                all(result[key] == binding[key] for key in ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256")),
                "retained_result_references_existing_invocation")


def expect_reject(action: Any, name: str) -> None:
    try:
        action()
    except ResourceStop:
        raise
    except Exception:
        return
    raise RuntimeError("mutation_accepted:" + name)


def parent_layout_selftest(args: Any) -> Any:
    e, oracle, _refinement, _p2, _m, _base, _descriptors = own_dependencies()
    accepted = e.read_oracle(oracle, args.oracle_root)
    external = read_external_e(e, oracle, args.e_root)
    cases = ("external-e-kind", "external-e-checker-incomplete", "external-e-target-parent",
             "external-e-ordinary-rho2-claim", "external-e-current-head")
    for name in cases:
        objects = copy.deepcopy(external["objects"])
        if name == "external-e-kind":
            objects["output/HEAD"]["kind"] = "MEMBER"
        elif name == "external-e-checker-incomplete":
            objects["checker-result.json"]["all_arrays_and_json_compared"] = False
        elif name == "external-e-target-parent":
            objects["output/result.json"]["target"]["parent_remainder_sha256"] = "0" * 64
        elif name == "external-e-ordinary-rho2-claim":
            objects["output/result.json"]["target_derivation"]["original_rho2_directly_read"] = True
        else:
            objects["output/HEAD"]["state_head"] = "0" * 64
        expect_reject(lambda: validate_external_e_metadata(e, objects, E_SNAPSHOT), name)
    return {"schema": SCHEMA + ".parent-layout-selftest", "status": "PASS", "metadata_only": True,
        "accepted_oracle_layout": accepted["layout"], "accepted_external_e_layout": external["layout"],
        "rejected_cases": list(cases), "old_success_suites": 0, "cross_checked": False, "verified": False}


def selftest() -> Any:
    e, _oracle, _refinement, _p2, _m, _base, _descriptors = own_dependencies()
    require(cap_reached(1, 1) and not cap_reached(1, 32) and cap_reached(32, 32) and cap_reached(2, 1),
            "absolute_cap_carries_across_resume")
    expect_reject(lambda: cap_reached(True, 32), "boolean_completed_count")
    binding = {"owner_sha256": "1" * 64, "source_sha256": "2" * 64, "start_sha256": "3" * 64,
               "fixed_manifest_sha256": "4" * 64}
    # These short byte strings are metadata protocol probes, not physical
    # arrays or a synthetic full-size arithmetic success certificate.
    state = {"kind": "Separator", "rank": 1, "generation": 1, "head": "5" * 64,
        "target_raw": b"\x01", "previous_target_raw": b"\x01", "lambda_raw": b"\x01",
        "completed_steps": 0, "last_step_manifest_sha256": None, "direct_pairing": {},
        "target_parents": [], "original_rho2_sha256": "6" * 64}
    snapshot = build_current_start(state, binding)
    witness = {"kind": "chord", "scalar": 1}
    accepted = {"witness": witness, "layout": {"state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"]),
        "snapshot_sha256": sha(canonical(snapshot)), "witness_sha256": sha(canonical(witness)), "terminal": "VIOLATION_CANDIDATE"}}
    check_current_witness(state, snapshot, accepted)
    changed_state = {**state, "lambda_raw": b"\x02"}
    expect_reject(lambda: check_current_witness(changed_state, snapshot, accepted), "stale_current_lambda")
    changed_input = copy.deepcopy(accepted)
    changed_input["witness"]["scalar"] = 2
    expect_reject(lambda: check_current_witness(state, snapshot, changed_input), "stale_current_witness")
    target = {"parent_remainder_sha256": sha(b"target"), "remainder_sha256": sha(b"target"), "scalar": 0}
    e.validate_plain_target(target, sha(b"target"), sha(b"target"), 0)
    expect_reject(lambda: e.validate_plain_target({**target, "sha256": "0" * 64}, sha(b"target"), sha(b"target"), 0),
                  "plain_target_not_generic_sealed")
    expect_reject(lambda: e.validate_plain_target({**target, "scalar": False}, sha(b"target"), sha(b"target"), 0),
                  "plain_target_scalar_boolean")
    groups = [{"name": "absolute-cap-and-current-witness", "status": "PASS",
               "checks": ["cap1-to-resume32-carry", "stale-lambda-rejected", "stale-witness-rejected"]}]
    with tempfile.TemporaryDirectory(prefix="r07-cegar-interface-") as temporary:
        output = Path(temporary)
        for name, value in (("owner.json", seal("owner", {"fixture": "metadata-only"})),
                            ("source.json", seal("source", {"fixture": "metadata-only"})),
                            ("start.json", seal("start", {"fixture": "metadata-only"}))):
            write_atomic(output, name, canonical(value))
        initial = head_value(state, binding)
        write_atomic(output, "HEAD", canonical(initial))
        probe_snapshot, store = snapshot_store(None, None, output, state, binding, create=True)
        publish_checkpoint(output, state, binding, probe_snapshot, store)
        initial_head_bytes = (output / "HEAD").read_bytes()
        for phase in PHASES:
            ensure_phase(store, phase, lambda phase=phase: {"probe.json":
                (canonical({"phase": phase, "fixture": "metadata-only"}), "json", None)})
        saved = {phase: (store.directory(phase) / "manifest.json").read_bytes() for phase in PHASES}
        manifest = seal("step-manifest", {"step": 1, "fixture": "metadata-only-publication-protocol",
            "phase_manifests": {phase: store.hashes[index] for index, phase in enumerate(PHASES)}})
        publish_step_manifest(output, manifest)
        # Simulated process loss here: physical is durable and the step file
        # exists, while the old HEAD has not been replaced.
        require((output / "HEAD").read_bytes() == initial_head_bytes, "step_before_head_does_not_advance_count")
        _same_snapshot, resumed = snapshot_store(None, None, output, state, binding, create=False)
        require(resumed.hashes == store.hashes, "all_completed_phases_restored_after_head_gap")

        def forbidden_rebuild() -> Any:
            raise RuntimeError("completed_phase_was_recomputed")

        for phase in PHASES:
            require(ensure_phase(resumed, phase, forbidden_rebuild) is False, "resume_reuses_completed_phase")
        publish_step_manifest(output, manifest)
        state = {**state, "completed_steps": 1, "last_step_manifest_sha256": sha(canonical(manifest))}
        committed_head = head_value(state, binding)
        publish_committed_head(output, committed_head)
        require(read_json(output, "HEAD", "head")["completed_steps"] == 1 and not cap_reached(1, 32) and
                all((store.directory(phase) / "manifest.json").read_bytes() == saved[phase] for phase in PHASES),
                "resumed_publication_preserves_completed_bytes_and_count")
        for key in ("source_sha256", "owner_sha256"):
            altered = {**store.binding, key: "f" * 64}
            expect_reject(lambda altered=altered: PhaseStore(None, store.root, altered).load(), "changed_" + key)
        expect_reject(lambda: validate_roster(store.manifests[0], registered_phase_roster(e, "section", store.values["section"])),
                      "metadata_probe_is_not_an_arithmetic_section_certificate")
        pending = store.root / (".pending-section-" + "a" * 32)
        pending.mkdir()
        write_atomic(pending, "unfinished.json", canonical({"eof": False}))
        validate_snapshot_directory(store.root)
        (store.root / "unknown-tail").mkdir()
        expect_reject(lambda: validate_snapshot_directory(store.root), "unregistered_tail_directory")
        groups.append({"name": "durable-phase-and-head-publication", "status": "PASS", "arithmetic_fixture": False,
            "checks": ["complete-phase-before-head-crash", "typed-phase-reuse-without-builder", "step-manifest-idempotent",
                "head-count-preserved", "source-and-owner-change-rejected", "only-named-pending-tail",
                "metadata-probe-rejected-by-production-array-roster"]})
    zero_state = {**state, "kind": "LinearMembershipCandidate", "target_raw": b"\0", "lambda_raw": None,
                  "direct_pairing": None}
    zero_head = head_value(zero_state, binding)
    limits = argparse.Namespace(max_appends=32, max_seconds=60.0, invocation_sha256="7" * 64)
    zero = current_result(zero_state, binding, zero_head, "LINEAR_MEMBERSHIP_CANDIDATE", limits)
    require(zero["positive_readout"] == "TASK958_PENDING" and zero["grade2_member"] == "NOT_DECIDED" and
            zero["lambda_rho2"] is None and zero["separator_premises"] is None and zero["full_A0"] is False and
            zero["verified"] is False, "linear_zero_is_only_positive_readout_pending")
    expect_reject(lambda: current_result(state, binding, head_value(state, binding), "COMPLETE_ZERO_CANDIDATE", limits),
                  "missing_complete_oracle_cannot_be_zero")
    groups.append({"name": "plain-zero-scalar-and-terminal-types", "status": "PASS",
        "checks": ["plain-target-scalar0-accepted", "plain-target-seal-and-bool-rejected", "linear-zero-not-member",
                   "complete-zero-needs-current-complete-oracle"]})
    return {"schema": SCHEMA + ".selftest", "status": "PASS", "groups": groups, "old_success_suites": 0,
        "full_arithmetic_fixture": False, "candidate": True, "cross_checked": False, "verified": False}


def request_stop(_signum: int, _frame: Any) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def diagnostic(args: Any, status: str, reason: str) -> Any:
    head_sha = None
    output = args.output_root.resolve() if args.output_root is not None else None
    if OUTPUT_CREATED and output is not None and (output / "HEAD").is_file():
        head_sha = sha((output / "HEAD").read_bytes())
    value = seal("diagnostic", {"status": status, "terminal": status, "phase": CURRENT_PHASE, "reason": reason,
        "head_sha256": head_sha, "diagnostic_only": True, "elapsed_seconds": round(time.monotonic() - STARTED, 6),
        "candidate": False, "cross_checked": False, "verified": False})
    if OUTPUT_CREATED and output is not None:
        name = "resource-stop.json" if status == "UNKNOWN_RESOURCE" else "rejected.json"
        write_atomic(output, name, canonical(value), replace=True)
    return value


def main() -> int:
    global DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    tests = parser.add_mutually_exclusive_group()
    tests.add_argument("--selftest", action="store_true")
    tests.add_argument("--parent-layout-selftest", action="store_true")
    for name in ("state-root", "delta-root", "seed34-root", "packet-root", "refinement-root", "oracle-root", "e-root",
                 "prepare-root", "p1-root", "task712-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--output", dest="output_root", type=Path)
    parser.add_argument("--max-appends", type=int, default=32)
    parser.add_argument("--max-seconds", type=float, default=5400.0)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    try:
        require(0 <= args.max_appends < 999999 and math.isfinite(args.max_seconds) and args.max_seconds > 0,
                "finite_positive_resource_limit_and_nonnegative_cap")
        DEADLINE = STARTED + args.max_seconds
        for name in ("SIGINT", "SIGTERM"):
            if hasattr(signal, name):
                signal.signal(getattr(signal, name), request_stop)
        parent_names = ("state_root", "delta_root", "seed34_root", "packet_root", "refinement_root", "oracle_root", "e_root")
        other_names = ("prepare_root", "p1_root", "task712_root", "output_root")
        if args.selftest:
            require(not args.resume and not args.block_root and
                    all(getattr(args, name) is None for name in (*parent_names, *other_names)), "selftest_has_no_parent_or_output")
            result = selftest()
        elif args.parent_layout_selftest:
            require(not args.resume and not args.block_root and all(getattr(args, name) is not None for name in parent_names) and
                    all(getattr(args, name) is None for name in other_names), "metadata_selftest_seven_parent_roots_only")
            result = parent_layout_selftest(args)
        else:
            require(len(args.block_root) == 4 and all(getattr(args, name) is not None for name in (*parent_names, *other_names)),
                    "production_all_fourteen_parents_and_output")
            result = run_actual(args)
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 0
    except ResourceStop as exc:
        result = diagnostic(args, "UNKNOWN_RESOURCE", str(exc))
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 3
    except Exception as exc:
        result = diagnostic(args, "REJECTED", type(exc).__name__ + ":" + str(exc))
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
