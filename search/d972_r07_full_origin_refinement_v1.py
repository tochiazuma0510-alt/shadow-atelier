#!/usr/bin/env python3
"""Task954: bounded full-origin refinement from accepted fixed44 v2.

Candidate only. Old base, saved deltas, canonical lifts and three packet
steps remain named premises. New complete scans and selected filtered actors
are computed here. ROOT_ORIGINS_ZERO is not a dual-closure certificate.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
from typing import Any
import uuid

import numpy as np

SCHEMA = "d972.r07.full-origin-refinement.v1"
SEARCH = Path(__file__).resolve().parent
ZERO_HEAD = "0" * 64
NSEEDS, P1_ROWS, TOP_WIDTH, TOP_BYTES = 44, 8059, 36288, 9072
LOWER_WIDTH, PHYSICAL_WIDTH, PHYSICAL_BYTES = 96776, 48384, 12096
ACTORS = (1, -1, 2, -2)
ORIGINS = NSEEDS + 4 * P1_ROWS
CAP = 32
START_RANK, START_GENERATION = 1359, 8064
START_HEAD = "7b7380a7ddb785910347df14f47ba4634cc5fa2fff7c32b722455a824d6cddda"
START_LAMBDA = "60ac649575400e98881c5de5d4ef2c6202d3cf577da1411042104254edb004e2"
START_TARGET = "0a466426db600e191e9ee5563066dbb729492ab74d869dbf0ceeadc2b2f7f686"
FIXED_MODULE = "d972_r07_fixed_root_packet_loop_v2.py"
FIXED_MODULE_SHA = "e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6"
PACKET_ARTIFACT = {"run": 33964709359, "attempt": 1,
    "head": "fff114c41bd8748ad0e708919fe0820335c9cce8", "id": 9969090590,
    "name": "d972-r07-fixed-root-packet-loop-v2-candidate-33964709359-1",
    "bytes": 1855391,
    "sha256": "sha256:b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428"}
PACKET_FILES = {
    "output/HEAD": (709, "c48e8f673b7da860b57b0d413a3f49e2035831ecabd4f790f964e6ba1a2f2fc2"),
    "output/result.json": (4493, "4cc9c95ac57db62de48095360e9f63056281176931f27ac184d2534a1d78d03b"),
    "checker-result.json": (4603, "b8308d60ca9332a02d2ca503753e7c72db54d6509c62b28a9aee648f44a2ca60"),
    "source-receipt.json": (2037, "513eea26bf5cf3288aaba3caaf4f8ca9095857d1af49154d4d7d69b23bd63886"),
    "output/start.json": (5025, "041d9dc7abcbddc81df490a2ab77acb40715c9bb0d7ca3a004d498d9efd00d6d"),
    "output/owner.json": (8274, "a8d206b0ae26f3bfcf102de2119f10bd7151d9dd9c6294d8e879656f1ced6f41"),
    "output/packet/manifest.json": (843, "d5e3ef0c0d691131b6bd1293d066d6e994c572086dc0c89a6e5ec766a8474199")}
SCOPE = {"characters": [0, 1, 2, 3], "seeds": 44, "p1_rows": 8059,
    "actors": list(ACTORS), "origins_per_character": ORIGINS, "total_origins": 4 * ORIGINS,
    "order": "character-major;seeds0..43;basis_i0..8058;actors1,-1,2,-2",
    "operational_append_cap": CAP, "mathematical_total_bound": None}
CLAIMS = {"FULL_ORIGIN_REFINEMENT_CANDIDATE": True, "GRADE2_MEMBER": "NOT_DECIDED",
    "GRADE2_NONMEMBER": "NOT_DECIDED", "DUAL_CLOSURES": "NOT_EXECUTED",
    "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
    "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False}
ASSURANCE = {"candidate": True, "cross_checked": False, "verified": False}
STARTED = time.monotonic()
DEADLINE: float | None = None
STOP_REQUESTED = False


class ResourceStop(RuntimeError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    require("schema" not in body and "sha256" not in body, "seal_reserved_keys")
    unsigned = {"schema": SCHEMA + "." + kind, **body}
    return {**unsigned, "sha256": sha(canonical(unsigned))}


def sealed_ok(value: Any, kind: str | None = None) -> bool:
    return (isinstance(value, dict) and (kind is None or value.get("schema") == SCHEMA + "." + kind)
        and value.get("sha256") == sha(canonical({k: v for k, v in value.items() if k != "sha256"})))


def check_deadline(phase: str) -> None:
    if STOP_REQUESTED or (DEADLINE is not None and time.monotonic() >= DEADLINE):
        raise ResourceStop(phase)


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"phase": phase, "elapsed_seconds": round(time.monotonic() - STARTED, 3),
                      **fields}, sort_keys=True), file=sys.stderr, flush=True)


def boundary(phase: str, **fields: Any) -> None:
    progress(phase, **fields)
    check_deadline(phase)


def receipt(name: str, raw: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def read_json(path: Path, kind: str | None = None) -> Any:
    require(path.is_file() and not path.is_symlink() and path.stat().st_size <= 1 << 28,
            "json_regular_file:" + path.name)
    raw = path.read_bytes()
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw and (kind is None or sealed_ok(value, kind)),
            "canonical_json:" + path.name)
    return value


def decoded(raw: bytes, kind: str) -> Any:
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw and sealed_ok(value, kind), "sealed_payload:" + kind)
    return value


def sync_directory(path: Path) -> None:
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def write_atomic(root: Path, name: str, raw: bytes, replace: bool = False) -> dict[str, Any]:
    require(Path(name).name == name and name not in ("", ".", "..") and
            not root.is_symlink() and not (root / name).is_symlink(), "output_file_name")
    target = root / name
    require(replace or not target.exists(), "fresh_file:" + name)
    pending = root / ("." + name + ".pending-" + uuid.uuid4().hex)
    with pending.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(pending, target)
    sync_directory(root)
    return receipt(name, raw)


def publish_directory(pending: Path, final: Path) -> None:
    require(pending.parent == final.parent and pending.is_dir() and not pending.is_symlink(),
            "publish_directory_parent")
    if final.exists():
        require(final.is_dir() and not final.is_symlink(), "orphan_directory")
        os.replace(final, final.parent / (".orphan-" + final.name + "-" + uuid.uuid4().hex))
    sync_directory(pending)
    os.replace(pending, final)
    sync_directory(final.parent)


def write_bundle(parent: Path, number: int, kind: str, fields: Any,
                 payloads: dict[str, bytes]) -> Any:
    pending = parent / (".pending-" + str(number).zfill(6) + "-" + uuid.uuid4().hex)
    pending.mkdir()
    files = [write_atomic(pending, name, payloads[name]) for name in sorted(payloads)]
    manifest = seal(kind, {**fields, "files": files})
    write_atomic(pending, "manifest.json", canonical(manifest))
    publish_directory(pending, parent / str(number).zfill(6))
    return manifest


def read_bundle(m: Any, directory: Path, kind: str, expected_sha: str | None = None) -> Any:
    require(directory.is_dir() and not directory.is_symlink(), "bundle_directory")
    manifest = read_json(m.safe_file(directory, "manifest.json"), kind)
    require(expected_sha is None or sha(canonical(manifest)) == expected_sha, "bundle_manifest_pin")
    records = manifest["files"]
    require(isinstance(records, list) and records == sorted(records, key=lambda x: x["file"]) and
            len(records) == len({x["file"] for x in records}) and
            {p.name for p in directory.iterdir()} == {x["file"] for x in records} | {"manifest.json"},
            "bundle_exact_roster")
    payloads = {x["file"]: m.read_exact(m.safe_file(directory, x["file"]),
                x["bytes"], x["sha256"], cap=1 << 28) for x in records}
    return manifest, payloads


def fixed_module() -> Any:
    path = SEARCH / FIXED_MODULE
    require(path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == FIXED_MODULE_SHA,
            "fixed_producer_source_pin")
    if str(SEARCH) not in sys.path:
        sys.path.insert(0, str(SEARCH))
    spec = importlib.util.spec_from_file_location("task954_own_fixed_v2", path)
    require(spec is not None and spec.loader is not None, "fixed_import_spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_packet_metadata(p2: Any, root: Path) -> Any:
    objects = p2.layout_objects(root, PACKET_FILES)
    bundles = []
    for step in range(1, 4):
        directory = root / "output" / "steps" / str(step).zfill(6)
        manifest = read_json(directory / "manifest.json")
        require(p2.sealed_ok(manifest, "step-manifest") and manifest["file_roster"] ==
                sorted({x["file"] for x in manifest["files"]} | {"manifest.json"}) and
                len(manifest["files"]) + 1 == len(manifest["file_roster"]) and
                {p.name for p in directory.iterdir()} == set(manifest["file_roster"]),
                "accepted_packet_step_roster")
        payloads = {x["file"]: p2.layout_fixed(directory, x["file"], (x["bytes"], x["sha256"]))
                    for x in manifest["files"]}
        result = json.loads(payloads["result.json"].decode("ascii"))
        instruction = json.loads(payloads["instruction.json"].decode("ascii"))
        require(canonical(result) == payloads["result.json"] and
                canonical(instruction) == payloads["instruction.json"], "accepted_packet_step_canonical")
        bundles.append({"manifest": manifest, "result": result,
                        "instruction": instruction, "payloads": payloads})
    return objects, bundles


def packet_parent_layout(p2: Any, objects: Any, bundles: Any) -> Any:
    """Actual old layout validator, shared by intake and metadata-only canary."""
    for name, pin in PACKET_FILES.items():
        require(len(canonical(objects[name])) == pin[0] and sha(canonical(objects[name])) == pin[1],
                "accepted_packet_entry_pin:" + name)
    head, result, checked = (objects[name] for name in
        ("output/HEAD", "output/result.json", "checker-result.json"))
    old_start, old_owner = objects["output/start.json"], objects["output/owner.json"]
    packet_sha = PACKET_FILES["output/packet/manifest.json"][1]
    require(all(p2.sealed_ok(value, kind) for value, kind in
                ((head, "head"), (result, "result"), (old_start, "start"), (old_owner, "owner"))) and
            checked["schema"] == p2.SCHEMA + ".checker-result" and checked["status"] == "PASS" and
            head["completed_steps"] == checked["prefix_steps_replayed"] == checked["completed_steps"] == 3 and
            result["terminal"] == checked["terminal"] == "ROOT_SEEDS_ZERO" and
            checked["packet_independently_rebuilt"] is True and
            all(value["cross_checked"] is False and value["verified"] is False for value in (result, checked)) and
            checked["result_sha256"] == PACKET_FILES["output/result.json"][1] and
            checked["head_sha256"] == result["head_sha256"] == PACKET_FILES["output/HEAD"][1] and
            head["packet_manifest_sha256"] == checked["packet_manifest_sha256"] == packet_sha and
            head["owner_sha256"] == checked["owner_sha256"] == PACKET_FILES["output/owner.json"][1] and
            head["producer_sha256"] == FIXED_MODULE_SHA and
            head["start_sha256"] == PACKET_FILES["output/start.json"][1], "accepted_packet_terminal_layout")
    source_files = {x["file"]: x for x in objects["source-receipt.json"]["files"]}
    require(source_files["search/" + FIXED_MODULE]["sha256"] == FIXED_MODULE_SHA and
            objects["source-receipt.json"]["data"] == p2.DATA_PINS, "accepted_packet_source_layout")
    require(len(bundles) == 3, "accepted_packet_three_steps")
    predecessor, prior_manifest, prior_target = p2.START_HEAD, None, p2.START_TARGET
    layouts = []
    for step, bundle in enumerate(bundles, 1):
        manifest, row, instruction, payloads = (bundle[k] for k in
            ("manifest", "result", "instruction", "payloads"))
        target = row["target"]
        unsigned = {k: v for k, v in instruction.items() if k != "rolling_sha256"}
        require(instruction.get("schema") == p2.SCHEMA + ".instruction" and
                "sha256" not in instruction and instruction["predecessor"] == predecessor and
                instruction["rolling_sha256"] == sha(bytes.fromhex(predecessor) + canonical(unsigned)),
                "accepted_packet_rolling_instruction")
        require(set(target) == {"parent_remainder_sha256", "remainder_sha256", "scalar"} and
                type(target["scalar"]) is int and target["scalar"] in (0, 1, 2) and
                target["parent_remainder_sha256"] == prior_target and
                target["remainder_sha256"] == sha(payloads["target-remainder.bin"]) and
                target["scalar"] == instruction["target_scalar"] and
                target["remainder_sha256"] == instruction["target_remainder_sha256"],
                "accepted_packet_plain_target")
        require(p2.sealed_ok(manifest, "step-manifest") and p2.sealed_ok(row, "step-result") and
                manifest["step"] == row["step"] == instruction["step"] == step and
                manifest["predecessor_step_manifest_sha256"] == prior_manifest and
                manifest["parent_state_head"] == row["parent_state_head"] == predecessor and
                manifest["state_head"] == row["state_head"] == instruction["rolling_sha256"] and
                manifest["rank"] == instruction["rank"] == row["rank_after"] == p2.START_RANK + step and
                manifest["generation"] == instruction["generation"] == row["generation_after"] == p2.START_GENERATION + step and
                instruction["offer"] == p2.START_GENERATION + step - 1 and
                manifest["kind"] == row["kind"] == "Separator" and
                manifest["packet_manifest_sha256"] == row["packet_manifest_sha256"] == packet_sha and
                row["separator"]["lambda_sha256"] == sha(payloads["lambda.bin"]) and
                sha(payloads["instruction.json"]) == sha(canonical(instruction)) and
                sha(payloads["result.json"]) == sha(canonical(row)), "accepted_packet_step_chain")
        layouts.append({"role": "packet-step-" + str(step), "step": step,
            "manifest_schema": manifest["schema"], "result_schema": row["schema"],
            "instruction_schema": instruction["schema"], "instruction_seal": "rolling_sha256",
            "target_seal": None, "target_keys": sorted(target), "target_scalar": target["scalar"],
            "manifest_sha256": sha(canonical(manifest)), "result_sha256": sha(canonical(row)),
            "instruction_sha256": sha(canonical(instruction)), "target_sha256": sha(canonical(target)),
            "state_head": manifest["state_head"], "parent_state_head": predecessor,
            "rank": manifest["rank"], "generation": manifest["generation"],
            "physical_normalized_sha256": sha(payloads["physical-normalized.bin"]),
            "lambda_sha256": sha(payloads["lambda.bin"]),
            "target_remainder_sha256": sha(payloads["target-remainder.bin"])})
        predecessor, prior_manifest, prior_target = (manifest["state_head"],
            sha(canonical(manifest)), target["remainder_sha256"])
    require(prior_manifest == head["step_manifest_sha256"] and predecessor == head["state_head"] ==
            checked["state_head"] == START_HEAD and head["rank"] == checked["rank"] == START_RANK and
            head["generation"] == checked["generation"] == START_GENERATION and
            layouts[-1]["lambda_sha256"] == START_LAMBDA and prior_target == START_TARGET,
            "accepted_packet_final_join")
    return seal("packet-parent-layout", {"artifact": PACKET_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]}
                        for name, pin in sorted(PACKET_FILES.items())],
        "steps": layouts, "rank": START_RANK, "generation": START_GENERATION,
        "state_head": START_HEAD, "lambda_sha256": START_LAMBDA,
        "target_remainder_sha256": START_TARGET, "old_target_history_replayed": False})


def load_start(p2: Any, m: Any, base: Any, descriptors: Any, args: Any) -> Any:
    objects, bundles = read_packet_metadata(p2, args.packet_root)
    layout = packet_parent_layout(p2, objects, bundles)
    boundary("accepted-packet-metadata")
    state, old_start = p2.load_start(m, args)
    old_owner, p1, task554, tables = p2.owner_and_tables(m, base, descriptors, args, state)
    require(old_start == objects["output/start.json"] and old_owner == objects["output/owner.json"],
            "accepted_packet_parent_owner_join")
    packet = p2.load_packet(m, args.packet_root / "output", sha(canonical(old_owner)), state,
                           PACKET_FILES["output/packet/manifest.json"][1])
    # This accepted loader only authenticates and attaches the saved three
    # rows/targets. It does not reconstruct or reduce any old packet row.
    p2.load_prefix(m, args.packet_root / "output", state, packet, sha(canonical(old_owner)),
                   old_start, {"producer_sha256": FIXED_MODULE_SHA}, objects["output/HEAD"])
    require((state["rank"], state["generation"], state["head"], sha(state["lambda_raw"]),
             sha(state["target_raw"])) ==
            (START_RANK, START_GENERATION, START_HEAD, START_LAMBDA, START_TARGET), "full_origin_actual_start")
    for item in layout["steps"]:
        state["accepted_target_derivation_parents"].append({key: item[key] for key in
            ("role", "manifest_sha256", "result_sha256", "target_sha256", "state_head")})
    state.update({"completed_steps": 0, "step_manifest_sha256": None,
                  "current_scan_manifest_sha256": None, "start_target_raw": state["target_raw"]})
    start = seal("start", {"rank": START_RANK, "generation": START_GENERATION,
        "state_head": START_HEAD, "lambda_sha256": START_LAMBDA,
        "target_remainder_sha256": START_TARGET, "parent_layout": state["parent_layout"],
        "packet_parent_layout": layout,
        "accepted_target_derivation_parents": state["accepted_target_derivation_parents"]})
    owner = seal("owner", {"formula_id": m.V541_FORMULA_ID, "scope": SCOPE,
        "accepted_packet_owner_sha256": sha(canonical(old_owner)),
        "accepted_packet_manifest_sha256": packet["manifest_sha256"],
        "p1_parent": old_owner["p1_parent"], "task554_parent": old_owner["task554_parent"],
        "task712_parent": old_owner["task712_parent"],
        "task712_manifest_sha256": old_owner["task712_manifest_sha256"],
        "word_dictionary_sha256": old_owner["word_dictionary_sha256"],
        "relator_dictionary_sha256": old_owner["relator_dictionary_sha256"]})
    boundary("accepted-start-direct-pairings", rows=state["rank"])
    return state, start, owner, p1, task554, tables, packet


def canonical_index(m: Any, p1: Any) -> Any:
    """Authenticate accepted instruction metadata once; decode no lift matrix."""
    references = []
    digest = hashlib.sha256()
    predecessor, offset = ZERO_HEAD, 0
    path = m.safe_file(p1["root"], p1["instruction"]["path"])
    with path.open("rb", buffering=1 << 20) as stream:
        for node in range(P1_ROWS):
            line = stream.readline()
            require(line.endswith(b"\n") and b"\r" not in line, "canonical_index_line")
            record = json.loads(line.decode("ascii"))
            require(set(record) == m.P1_INSTRUCTION_KEYS and canonical(record) == line and
                    record["node"] == node and record["offset"] == node * m.P1_ROW_BYTES and
                    record["length"] == m.P1_ROW_BYTES and record["predecessor"] == predecessor and
                    record["scale"] in (1, 2) and record["row_receipt"]["offset"] == node * m.P1_ROW_BYTES and
                    record["row_receipt"]["length"] == m.P1_ROW_BYTES, "canonical_index_record")
            unsigned = {k: v for k, v in record.items() if k != "ancestry_sha256"}
            require(record["ancestry_sha256"] == sha(bytes.fromhex(predecessor) + canonical(unsigned)),
                    "canonical_index_ancestry")
            references.append({"node": node, "instruction_offset": offset,
                "instruction_length": len(line), "instruction_sha256": sha(line),
                "ancestry_sha256": record["ancestry_sha256"], "predecessor": record["predecessor"],
                "p1_sha256": record["p1_sha256"], "row_sha256": record["row_receipt"]["sha256"],
                "origin_sha256": sha(canonical(record["origin"])),
                "reductions_sha256": sha(canonical(record["reductions"])), "scale": record["scale"],
                "literal_input_sha256": record["literal_input_sha256"]})
            predecessor = record["ancestry_sha256"]
            offset += len(line)
            digest.update(line)
            if (node + 1) % 512 == 0 or node + 1 == P1_ROWS:
                boundary("canonical-index", rows=node + 1, total=P1_ROWS)
        require(stream.read(1) == b"", "canonical_index_eof")
    require(offset == p1["instruction"]["bytes"] and digest.hexdigest() == p1["instruction"]["sha256"] and
            predecessor == p1["manifest"]["ancestry_sha256"], "canonical_index_terminal")
    return seal("canonical-p1-index", {"p1_manifest_sha256": p1["manifest_sha256"],
        "instruction_sha256": digest.hexdigest(), "cache_sha256": p1["cache"]["sha256"],
        "rows": P1_ROWS, "references": references})


def validate_index(index: Any, p1: Any, packet: Any) -> None:
    require(sealed_ok(index, "canonical-p1-index") and index["rows"] == P1_ROWS and
            index["p1_manifest_sha256"] == p1["manifest_sha256"] and
            index["instruction_sha256"] == p1["instruction"]["sha256"] and
            index["cache_sha256"] == p1["cache"]["sha256"] and
            [x["node"] for x in index["references"]] == list(range(P1_ROWS)), "canonical_index_pins")
    cursor, predecessor = 0, ZERO_HEAD
    for reference in index["references"]:
        require(reference["instruction_offset"] == cursor and reference["predecessor"] == predecessor and
                type(reference["instruction_length"]) is int and reference["instruction_length"] > 0 and
                reference["scale"] in (1, 2), "canonical_index_chain")
        cursor += reference["instruction_length"]
        predecessor = reference["ancestry_sha256"]
    require(cursor == p1["instruction"]["bytes"] and predecessor == p1["manifest"]["ancestry_sha256"],
            "canonical_index_final_head")
    for reference in packet["roots"]["roots"]:
        require(index["references"][reference["node"]] ==
                {k: v for k, v in reference.items() if k != "lift_components"},
                "canonical_index_accepted_packet_reference")


def fresh_vectors(base: Any, tables: Any, state: Any) -> list[list[np.ndarray]]:
    groups = []
    for character, table in enumerate(tables):
        q = base.ARITH.sparse_adjoint(table["forward"]["B"], TOP_WIDTH, PHYSICAL_WIDTH, state["lambda"])
        children = [base.ARITH.sparse_adjoint(table["forward"][actor], TOP_WIDTH, TOP_WIDTH, q)
                    for actor in ACTORS]
        require(all(x.shape == (TOP_WIDTH,) and not np.any(x > 2) for x in (q, *children)),
                "fresh_root_children_shape")
        groups.append([q, *children])
        boundary("fresh-root", step=state["completed_steps"], character=character,
                 support=int(np.count_nonzero(q)))
    return groups


def p1_contract(m: Any, base: Any, p1: Any, groups: Any) -> np.ndarray:
    """One buffered packed-cache pass, dynamic active characters, no stale pins."""
    values = np.zeros((4, 5, P1_ROWS), dtype=np.uint8)
    active = [bool(np.any(group[0])) for group in groups]
    projections = []
    for group in groups:
        projected = []
        for vector in group:
            positions = np.flatnonzero(vector)
            projected.append((positions // 4, positions % 4, vector[positions].astype(np.uint32)))
        projections.append(projected)
    digest = hashlib.sha256()
    buffer = bytearray(m.P1_ROW_BYTES * 256)
    path = m.safe_file(p1["root"], p1["cache"]["path"])
    with path.open("rb", buffering=1 << 20) as stream:
        cursor = 0
        while cursor < P1_ROWS:
            rows = min(256, P1_ROWS - cursor)
            size = rows * m.P1_ROW_BYTES
            view = memoryview(buffer)[:size]
            require(stream.readinto(view) == size, "dynamic_p1_chunk_eof")
            digest.update(view)
            packed = np.frombuffer(view, dtype=np.uint8).reshape(rows, m.P1_ROW_BYTES)
            require(not np.any(packed > 80), "dynamic_p1_packed_trits")
            for character in range(4):
                if active[character]:
                    result = base.vectorized_projection_chunk(packed, character * TOP_BYTES,
                                                               projections[character])
                    values[character, :, cursor:cursor + rows] = result.T
            cursor += rows
            boundary("dynamic-p1-pass", rows=cursor, total=P1_ROWS)
        require(stream.read(1) == b"", "dynamic_p1_trailing")
    require(digest.hexdigest() == p1["cache"]["sha256"], "dynamic_p1_cache_pin")
    return values


def actor_accumulator(m: Any, base: Any, parent: Any, values: np.ndarray,
                      lower_covectors: Any, character: int) -> Any:
    """Own v541 actor fold, releasing prepare before opening any new body."""
    require(values.shape == (5, P1_ROWS) and len(lower_covectors) == 4, "actor_accumulator_input")
    actors = values[1:].T.copy()
    lowers = np.zeros((P1_ROWS, 4), dtype=np.uint8)
    blobs = []
    relation_hash = base.relation_source_sha256()

    def subtract(value: int, expression: Any, offset: int, rank: int) -> int:
        return base._subtract_expression(value, expression, values[0], rank, offset, relation_hash, {})

    prepare = base._state_descriptor(parent["prepare"], -1, need_blobs=True)
    old = prepare["body"]["old_blocks"]
    for source, old_block in enumerate(old):
        lower_slices, grade_slices = base.old_covector_slices(lower_covectors, source)
        lower_part, lower_receipt = base.stream_packed_dots(prepare["root"], old_block["lower_basis_blob"],
            lower_slices, body_sha256=prepare["body_sha256"], role=f"old-{source}-lower")
        grade_part, grade_receipt = base.stream_packed_dots(prepare["root"], old_block["lifted_grade_blob"],
            grade_slices, body_sha256=prepare["body_sha256"], role=f"old-{source}-grade")
        offset, rank = m.OLD_OFFSETS[source], m.OLD_RANKS[source]
        lowers[offset:offset + rank] = (lower_part.astype(np.uint16) + grade_part.astype(np.uint16)) % 3
        actors[offset:offset + rank] = (actors[offset:offset + rank].astype(np.uint16) +
                                       lowers[offset:offset + rank].astype(np.uint16)) % 3
        blobs.extend((lower_receipt, grade_receipt))
        for local in range(rank):
            for slot in range(4):
                actors[offset + local, slot] = subtract(actors[offset + local, slot],
                    old_block["record"]["actor_transitions"][local][slot], offset, rank)
        boundary("actor-old-fold", character=character, source=source)
    # No surviving old_block/old/prepare reference may retain the old JSON
    # body while the first new block is loaded. Small blob receipts are safe.
    del old_block, old, prepare, lower_part, grade_part
    for target in range(4):
        block = base._state_descriptor(parent["blocks"][target], target, need_blobs=True)
        body = block["body"]
        offset, rank = m.NEW_OFFSETS[target], m.NEW_RANKS[target]
        lower_part, lower_receipt = base.stream_packed_dots(block["root"], body["basis_blob"],
            base.new_covector_slices(lower_covectors, target), body_sha256=block["body_sha256"],
            role=f"new-{target}-grade")
        lowers[offset:offset + rank] = lower_part
        actors[offset:offset + rank] = (actors[offset:offset + rank].astype(np.uint16) +
                                       lower_part.astype(np.uint16)) % 3
        blobs.append(lower_receipt)
        for source in range(4):
            for local in range(m.OLD_RANKS[source]):
                node = m.OLD_OFFSETS[source] + local
                for slot in range(4):
                    origin = m.ORIGIN_RANGES[source][0] + 44 + 4 * local + slot
                    actors[node, slot] = subtract(actors[node, slot], body["origin_reductions"][origin],
                                                  offset, rank)
        for local, transition in enumerate(body["actor_transitions"]):
            for slot in range(4):
                actors[offset + local, slot] = subtract(actors[offset + local, slot],
                                                        transition[slot], offset, rank)
        del transition, body, block, lower_part
        boundary("actor-new-fold", character=character, target=target)
    require(len(blobs) == 12 and sum(x["descriptor"]["bytes"] for x in blobs) == base.LOWER_BLOB_BYTES,
            "actor_twelve_blob_authentication")
    return actors, lowers


def first_hit(seed_values: np.ndarray, actor_values: np.ndarray) -> Any:
    require(seed_values.shape == (4, NSEEDS) and actor_values.shape == (4, P1_ROWS, 4) and
            not np.any(seed_values > 2) and not np.any(actor_values > 2), "full_array_shapes")
    for character in range(4):
        seeds = np.flatnonzero(seed_values[character])
        if len(seeds):
            seed = int(seeds[0])
            return {"character": character, "origin_id": seed, "index": character * ORIGINS + seed,
                "origin_kind": "seed", "seed": seed, "scalar": int(seed_values[character, seed])}
        actors = np.flatnonzero(actor_values[character].reshape(-1))
        if len(actors):
            position = int(actors[0])
            node, slot = divmod(position, 4)
            origin = NSEEDS + position
            return {"character": character, "origin_id": origin, "index": character * ORIGINS + origin,
                "origin_kind": "actor", "basis_i": node, "actor": ACTORS[slot], "actor_slot": slot,
                "scalar": int(actor_values[character, node, slot])}
    return None


def scan_payloads(m: Any, groups: Any, seeds: np.ndarray, actors: np.ndarray,
                  p1_values: np.ndarray, lower_values: np.ndarray) -> dict[str, bytes]:
    payloads = {}
    for character in range(4):
        payloads.update({f"root-c{character}.bin": m.pack(groups[character][0]),
            f"children-c{character}.bin": b"".join(m.pack(x) for x in groups[character][1:]),
            f"seeds-c{character}.u8": seeds[character].tobytes(),
            f"actors-c{character}.u8": actors[character].tobytes(),
            f"p1-c{character}.u8": p1_values[character].tobytes(),
            f"actor-lower-c{character}.u8": lower_values[character].tobytes()})
    return payloads


def scan_result(m: Any, base: Any, state: Any, tables: Any, owner_sha: str, index_sha: str,
                p1: Any, groups: Any, seeds: np.ndarray, actors: np.ndarray,
                payloads: Any) -> Any:
    roots, active = [], []
    for character, group in enumerate(groups):
        support = int(np.count_nonzero(group[0]))
        if support:
            active.append(character)
        else:
            require(all(not np.any(x) for x in group) and not np.any(seeds[character]) and
                    not np.any(actors[character]), "structural_zero_all_origins")
        roots.append({"character": character, "support": support,
            "packed_sha256": sha(payloads[f"root-c{character}.bin"]),
            "B_adj_identity": tables[character]["identity"]["adjoint:B"],
            "children": [{"actor": actor, "support": int(np.count_nonzero(child)),
                          "packed_sha256": sha(m.pack(child))} for actor, child in zip(ACTORS, group[1:])],
            "seed_values_sha256": sha(payloads[f"seeds-c{character}.u8"]),
            "actor_values_sha256": sha(payloads[f"actors-c{character}.u8"]),
            "p1_values_sha256": sha(payloads[f"p1-c{character}.u8"]),
            "actor_lower_values_sha256": sha(payloads[f"actor-lower-c{character}.u8"])})
    return seal("scan", {"scan": state["completed_steps"], "owner_sha256": owner_sha,
        "canonical_index_sha256": index_sha, "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"]), "roots": roots,
        "first_hit": first_hit(seeds, actors), "declared_pair_count": 4 * ORIGINS,
        "informative_pair_count": len(active) * ORIGINS, "structural_zero_pair_count": (4 - len(active)) * ORIGINS,
        "nonzero_pair_count": int(np.count_nonzero(seeds) + np.count_nonzero(actors)),
        "active_characters": active, "p1_pass": {"cache_passes": 1, "cache_rows": P1_ROWS,
            "cache_sha256": p1["cache"]["sha256"], "instruction_sha256": p1["instruction"]["sha256"],
            "active_pairings": 5 * len(active), "chunk_rows": 256},
        "lower_pass": {"body_reads": 5 * len(active), "blob_passes": 12 * len(active), "maximum_live_bodies": 1},
        "formula_id": m.V541_FORMULA_ID, **ASSURANCE})


def make_scan(m: Any, base: Any, p2: Any, state: Any, tables: Any, packet: Any, p1: Any,
              task554: Any, context: Any, owner_sha: str, index_sha: str, output: Path) -> Any:
    groups = fresh_vectors(base, tables, state)
    p1_values = p1_contract(m, base, p1, groups)
    seeds = np.zeros((4, NSEEDS), dtype=np.uint8)
    actors = np.zeros((4, P1_ROWS, 4), dtype=np.uint8)
    lower_values = np.zeros_like(actors)
    for character, group in enumerate(groups):
        if np.any(group[0]):
            for seed in range(NSEEDS):
                seeds[character, seed] = m.dot(group[0],
                    m.unpack(p2.packet_row(packet, character, seed), TOP_WIDTH))
            lower_covectors, _ = base.actor_adjoints(context, group[0], character, group[1:])
            boundary("full-actor-adjoints", character=character)
            actors[character], lower_values[character] = actor_accumulator(
                m, base, task554, p1_values[character], lower_covectors, character)
            del lower_covectors
        boundary("full-origin-character", character=character, step=state["completed_steps"])
    payloads = scan_payloads(m, groups, seeds, actors, p1_values, lower_values)
    result = scan_result(m, base, state, tables, owner_sha, index_sha, p1, groups, seeds, actors, payloads)
    payloads["result.json"] = canonical(result)
    manifest = write_bundle(output / "scans", state["completed_steps"], "scan-manifest",
        {"scan": state["completed_steps"], "owner_sha256": owner_sha, "canonical_index_sha256": index_sha,
         "rank": state["rank"], "generation": state["generation"], "state_head": state["head"],
         "lambda_sha256": sha(state["lambda_raw"])}, payloads)
    progress("scan-durable", scan=state["completed_steps"], first_hit=result["first_hit"])
    return {"manifest": manifest, "manifest_sha256": sha(canonical(manifest)), "result": result,
        "groups": groups, "seeds": seeds, "actors": actors, "p1_values": p1_values,
        "lower_values": lower_values}


def load_scan(m: Any, base: Any, output: Path, state: Any, tables: Any, p1: Any,
              owner_sha: str, index_sha: str, wanted_sha: str) -> Any:
    manifest, payloads = read_bundle(m, output / "scans" / str(state["completed_steps"]).zfill(6),
                                     "scan-manifest", wanted_sha)
    fields = {"scan": state["completed_steps"], "owner_sha256": owner_sha, "canonical_index_sha256": index_sha,
        "rank": state["rank"], "generation": state["generation"], "state_head": state["head"],
        "lambda_sha256": sha(state["lambda_raw"])}
    require(all(manifest[k] == v for k, v in fields.items()), "cached_scan_state_binding")
    result = decoded(payloads.pop("result.json"), "scan")
    groups, seeds, actors, p1_values, lower_values = [], [], [], [], []
    wanted_files = set()
    for character in range(4):
        root_name, children_name = f"root-c{character}.bin", f"children-c{character}.bin"
        wanted_files.update((root_name, children_name))
        children = payloads[children_name]
        require(len(children) == 4 * TOP_BYTES, "cached_children_width")
        groups.append([m.unpack(payloads[root_name], TOP_WIDTH),
                       *[m.unpack(children[i * TOP_BYTES:(i + 1) * TOP_BYTES], TOP_WIDTH) for i in range(4)]])
        for label, size, shape, destination in (("seeds", NSEEDS, (NSEEDS,), seeds),
                ("actors", P1_ROWS * 4, (P1_ROWS, 4), actors), ("p1", 5 * P1_ROWS, (5, P1_ROWS), p1_values),
                ("actor-lower", 4 * P1_ROWS, (P1_ROWS, 4), lower_values)):
            name = f"{label}-c{character}.u8"
            wanted_files.add(name)
            array = np.frombuffer(payloads[name], dtype=np.uint8)
            require(array.size == size and not np.any(array > 2), "cached_full_scalar_array")
            destination.append(array.reshape(shape))
        if not np.any(groups[-1][0]):
            require(not np.any(p1_values[-1]) and not np.any(lower_values[-1]), "cached_structural_zero_auxiliary_arrays")
    require(set(payloads) == wanted_files, "cached_scan_payload_roster")
    seeds, actors, p1_values, lower_values = map(np.asarray, (seeds, actors, p1_values, lower_values))
    require(result == scan_result(m, base, state, tables, owner_sha, index_sha, p1, groups, seeds, actors, payloads),
            "cached_scan_full_array_metadata")
    progress("scan-reused", scan=state["completed_steps"], state_head=state["head"])
    return {"manifest": manifest, "manifest_sha256": wanted_sha, "result": result,
        "groups": groups, "seeds": seeds, "actors": actors, "p1_values": p1_values,
        "lower_values": lower_values}


def actor_relation(m: Any, base: Any, parent: Any, selection: Any) -> Any:
    """Preserve literal event order before the numerical global F3 fold."""
    node, actor, slot = selection["basis_i"], selection["actor"], selection["actor_slot"]
    require(type(node) is int and 0 <= node < P1_ROWS and actor == ACTORS[slot], "selected_actor_range")
    old_input = node < m.NEW_OFFSETS[0]
    offsets, ranks = (m.OLD_OFFSETS, m.OLD_RANKS) if old_input else (m.NEW_OFFSETS, m.NEW_RANKS)
    owner = next(a for a in range(4) if offsets[a] <= node < offsets[a] + ranks[a])
    local = node - offsets[owner]
    origin = m.ORIGIN_RANGES[owner][0] + NSEEDS + 4 * local + slot if old_input else None
    events, segments = [], []

    def add(expression: Any, target: int | None, offset: int, body_sha: str) -> None:
        for ordinal, (index, coefficient) in enumerate(expression):
            global_index = offset + int(index)
            events.append({"node": global_index, "event_id": len(events),
                "body_role": "prepare-old" if target is None else "new-block",
                "task554_body_sha256": body_sha, "source_character": owner,
                "target_character": target, "origin_id": origin, "term_ordinal": ordinal,
                "local_index": int(index), "global_index": global_index, "coefficient": int(coefficient)})

    prepare = base._state_descriptor(parent["prepare"], -1, need_blobs=True)
    for source, old in enumerate(prepare["body"]["old_blocks"]):
        if old_input and owner == source:
            add(old["record"]["actor_transitions"][local][slot], None,
                m.OLD_OFFSETS[source], prepare["body_sha256"])
        segments.append({"kind": "old", "owner": source, "start": m.OLD_OFFSETS[source],
            "rows": m.OLD_RANKS[source], "root": prepare["root"], "body_sha256": prepare["body_sha256"],
            "lower_descriptor": copy.deepcopy(old["lower_basis_blob"]),
            "grade_descriptor": copy.deepcopy(old["lifted_grade_blob"])})
    del old, prepare
    boundary("selected-actor-relations", bodies=1)
    for target in range(4):
        block = base._state_descriptor(parent["blocks"][target], target, need_blobs=True)
        if old_input:
            add(block["body"]["origin_reductions"][origin], target,
                m.NEW_OFFSETS[target], block["body_sha256"])
        elif owner == target:
            add(block["body"]["actor_transitions"][local][slot], target,
                m.NEW_OFFSETS[target], block["body_sha256"])
        segments.append({"kind": "new", "owner": target, "start": m.NEW_OFFSETS[target],
            "rows": m.NEW_RANKS[target], "root": block["root"], "body_sha256": block["body_sha256"],
            "basis_descriptor": copy.deepcopy(block["body"]["basis_blob"])})
        del block
        boundary("selected-actor-relations", bodies=target + 2)
    coefficients = np.zeros(P1_ROWS, dtype=np.uint8)
    rolling = ZERO_HEAD
    for event in events:
        index, coefficient = event["global_index"], event["coefficient"]
        require(0 <= index < P1_ROWS and coefficient in (1, 2), "selected_actor_event_range")
        rolling = sha(bytes.fromhex(rolling) + canonical(event))
        event["rolling_sha256"] = rolling
        coefficients[index] = (int(coefficients[index]) + coefficient) % 3
    referenced = sorted({event["global_index"] for event in events})
    relation = seal("actor-relation", {"basis_i": node, "actor": actor, "actor_slot": slot,
        "raw_events": events, "raw_event_count": len(events), "raw_event_final_head": rolling,
        "final_coefficients": [[int(i), int(coefficients[i])] for i in np.flatnonzero(coefficients)],
        "referenced_nodes": referenced, "cancelled_nodes": [i for i in referenced if not coefficients[i]]})
    require(len(segments) == 8 and sum(s["rows"] for s in segments) == P1_ROWS, "selected_actor_segments")
    return relation, coefficients, segments


def empty_lift(m: Any) -> Any:
    return (np.zeros((4, m.SOURCE0C), dtype=np.uint8), np.zeros((4, m.SOURCE1C), dtype=np.uint8),
            np.zeros((4, TOP_WIDTH), dtype=np.uint8), np.zeros(8, dtype=np.uint8))


def component_receipts(m: Any, parts: Any) -> Any:
    return [m.component_receipt(name, part) for name, part in zip(("d0", "d1", "d2", "aux"), parts)]


def top_row(m: Any, stream: Any, index: Any, node: int) -> bytes:
    stream.seek(node * m.P1_ROW_BYTES)
    raw = stream.read(m.P1_ROW_BYTES)
    require(len(raw) == m.P1_ROW_BYTES and not np.any(np.frombuffer(raw, dtype=np.uint8) > 80) and
            sha(raw) == index["references"][node]["row_sha256"], "selected_canonical_top_row")
    return raw


def canonical_input(m: Any, p1: Any, index: Any, segments: Any, node: int) -> Any:
    parts = empty_lift(m)
    with m.safe_file(p1["root"], p1["cache"]["path"]).open("rb", buffering=1 << 20) as stream:
        parts[2][:] = m.unpack(top_row(m, stream, index, node), m.P1_ROW_TRITS).reshape(4, TOP_WIDTH)
    segment = next(s for s in segments if s["start"] <= node < s["start"] + s["rows"])
    local, owner = node - segment["start"], segment["owner"]
    if segment["kind"] == "old":
        lower, _ = m.scan_blob_selected(segment, segment["lower_descriptor"], {local}, "actor-input-old-lower")
        grade, _ = m.scan_blob_selected(segment, segment["grade_descriptor"], {local}, "actor-input-old-grade")
        dense = m.unpack(lower[local], m.SOURCE0C + 8)
        parts[0][owner] = dense[:m.SOURCE0C]
        parts[3][:] = dense[m.SOURCE0C:]
        parts[1][:] = m.unpack(grade[local], 4 * m.SOURCE1C).reshape(4, m.SOURCE1C)
    else:
        basis, _ = m.scan_blob_selected(segment, segment["basis_descriptor"], {local}, "actor-input-new-grade")
        parts[1][owner] = m.unpack(basis[local], m.SOURCE1C)
    boundary("selected-canonical-input", basis_i=node)
    return parts


def subtract_lifts(m: Any, p1: Any, index: Any, segments: Any, coefficients: np.ndarray,
                   reference_nodes: set[int], parts: Any) -> Any:
    """Stream selected tops and twelve lower blobs; retain small receipts only."""
    components = {node: [{"role": "p1-degree2", "bytes": m.P1_ROW_BYTES,
                          "sha256": index["references"][node]["row_sha256"]}] for node in reference_nodes}
    with m.safe_file(p1["root"], p1["cache"]["path"]).open("rb", buffering=1 << 20) as stream:
        for count, node in enumerate(sorted(reference_nodes), 1):
            raw = top_row(m, stream, index, node)
            coefficient = int(coefficients[node])
            if coefficient:
                m.add_scaled(parts[2], m.unpack(raw, m.P1_ROW_TRITS).reshape(4, TOP_WIDTH), 3 - coefficient)
            if count % 256 == 0:
                boundary("selected-actor-top-subtraction", rows=count, total=len(reference_nodes))
    blob_count = 0
    for segment in segments:
        owner = segment["owner"]
        descriptors = ((segment["lower_descriptor"], "old-lower"), (segment["grade_descriptor"], "old-grade")) \
            if segment["kind"] == "old" else ((segment["basis_descriptor"], "new-grade"),)
        for descriptor, role in descriptors:
            row_bytes = (descriptor["width"] + 3) // 4
            require(descriptor["rows"] == segment["rows"] and
                    descriptor["bytes"] == row_bytes * segment["rows"], "selected_lower_dimensions")
            digest = hashlib.sha256()
            with m.safe_file(segment["root"], descriptor["file"]).open("rb", buffering=1 << 20) as stream:
                for local in range(segment["rows"]):
                    raw = stream.read(row_bytes)
                    require(len(raw) == row_bytes and not np.any(np.frombuffer(raw, dtype=np.uint8) > 80),
                            "selected_lower_row")
                    digest.update(raw)
                    node = segment["start"] + local
                    coefficient = int(coefficients[node])
                    if coefficient:
                        dense = m.unpack(raw, descriptor["width"])
                        if role == "old-lower":
                            m.add_scaled(parts[0][owner], dense[:m.SOURCE0C], 3 - coefficient)
                            m.add_scaled(parts[3], dense[m.SOURCE0C:], 3 - coefficient)
                        elif role == "old-grade":
                            m.add_scaled(parts[1], dense.reshape(4, m.SOURCE1C), 3 - coefficient)
                        else:
                            m.add_scaled(parts[1][owner], dense, 3 - coefficient)
                    if node in reference_nodes:
                        components[node].append({"role": role, "bytes": len(raw), "sha256": sha(raw)})
                    if (local + 1) % 512 == 0:
                        boundary("selected-actor-lower-subtraction", owner=owner, role=role, rows=local + 1)
                require(stream.read(1) == b"", "selected_lower_eof")
            require(digest.hexdigest() == descriptor["sha256"], "selected_lower_blob_pin")
            blob_count += 1
            boundary("selected-actor-lower-blob", blobs=blob_count, total=12)
    require(blob_count == 12, "selected_actor_twelve_blobs")
    return [{"node": node, "components": components[node]} for node in sorted(reference_nodes)]


def actor_literal(packet: Any, tables: Any, selection: Any, relation: Any, index: Any,
                  source: bytes) -> Any:
    character, node = selection["character"], selection["basis_i"]
    return {"defect_operation": "ordered-product", "actor_conjugation": "t*W*t^-1",
        "basis_i": node, "actor": selection["actor"],
        "actor_input_p1_sha256": index["references"][node]["p1_sha256"],
        "relation_sha256": relation["sha256"], "canonical_index_sha256": sha(canonical(index)),
        "p1_factor_order": "event_id-ascending", "p1_exponent_rule": "(3-coefficient)%3",
        "literal_coefficient_collection": False, "character": character,
        "projector_receipt_sha256": sha(canonical(packet["receipts"]["premises"]["projectors"][character])),
        "actor_path": [], "forward_B": tables[character]["identity"]["forward:B"],
        "source_d_sha256": sha(source), "parent_state_ancestry_premise": True,
        "normalized_exponent_pair": "NOT_REPLAYED", "eleven_slot_replay": False,
        "full_A0_witness": False, "grade2_positive_terminal_complete": False}


def filtered_actor_source(base: Any, context: Any, parts: Any, actor: int) -> Any:
    require(actor in ACTORS, "filtered_actor_letter")
    direct = tuple(np.asarray(x, dtype=np.uint8).copy() for x in
        base.ARITH._seed_act(context, parts, base.actor_tag_values(context, actor)))
    require(all(x.shape == y.shape and not np.any(x > 2) for x, y in zip(direct, parts)) and
            np.array_equal(direct[3], parts[3]), "filtered_actor_full_components")
    return direct


def materialize_actor(m: Any, base: Any, packet: Any, tables: Any, p1: Any, task554: Any,
                      index: Any, context: Any, scan: Any) -> Any:
    selection = scan["result"]["first_hit"]
    character, node, slot = selection["character"], selection["basis_i"], selection["actor_slot"]
    relation, coefficients, segments = actor_relation(m, base, task554, selection)
    reference_nodes = set(relation["referenced_nodes"]) | {node}
    canonical_parts = canonical_input(m, p1, index, segments, node)
    input_components = component_receipts(m, canonical_parts)
    # Accepted v518 orientation is t W t^-1. The own v15 action is the full
    # filtered Fox/source actor and explicitly includes lower-to-top K_t b.
    direct = filtered_actor_source(base, context, canonical_parts, selection["actor"])
    require(np.array_equal(direct[3], canonical_parts[3]), "filtered_actor_shared_auxiliary")
    full_actor_components = component_receipts(m, direct)
    homogeneous = np.asarray([m.apply_sparse(tables[a]["forward"][selection["actor"]], TOP_WIDTH,
        TOP_WIDTH, canonical_parts[2][a]) for a in range(4)], dtype=np.uint8)
    lower_to_top = ((direct[2].astype(np.int16) - homogeneous.astype(np.int16)) % 3).astype(np.uint8)
    q = scan["groups"][character][0]
    homogeneous_value = m.dot(q, homogeneous[character])
    lower_value = m.dot(q, lower_to_top[character])
    full_value = m.dot(q, direct[2][character])
    require(homogeneous_value == int(scan["p1_values"][character, slot + 1, node]) and
            lower_value == int(scan["lower_values"][character, node, slot]) and
            full_value == (homogeneous_value + lower_value) % 3, "selected_filtered_direct_scalar_join")
    correction = sum(int(coefficient) * int(scan["p1_values"][character, 0, index_node])
                     for index_node, coefficient in relation["final_coefficients"]) % 3
    require((full_value - correction) % 3 == selection["scalar"], "selected_actred_scalar_join")
    input_receipt = {"basis_i": node, "p1_reference": index["references"][node],
        "components": input_components, "full_actor_components": full_actor_components,
        "homogeneous_top_sha256": sha(m.pack(homogeneous)), "lower_to_top_sha256": sha(m.pack(lower_to_top))}
    del canonical_parts, homogeneous, lower_to_top
    boundary("complete-filtered-actor", basis_i=node, actor=selection["actor"], lower_pairing=lower_value)
    lift_components = subtract_lifts(m, p1, index, segments, coefficients, reference_nodes, direct)
    lower = np.concatenate((direct[0].reshape(-1), direct[1].reshape(-1), direct[3]))
    require(lower.size == LOWER_WIDTH and not np.any(lower), "complete_actor_all96776_lower_zero")
    # V453 plain slicing is used only after complete lower cancellation.
    full_top, source = m.pack(direct[2]), m.pack(direct[2][character])
    require(m.dot(q, direct[2][character]) == selection["scalar"] and len(full_top) == 4 * TOP_BYTES,
            "selected_complete_defect_scalar")
    materialization = seal("materialization", {"selection": selection, "mode": "complete-filtered-actor",
        "source_d_sha256": sha(source), "source_full_top_sha256": sha(full_top), "lower_zero": True,
        "components": component_receipts(m, direct), "input": input_receipt, "relation": relation,
        "p1_references": [index["references"][n] for n in sorted(reference_nodes)],
        "lift_components": lift_components, "direct_pairing": {"homogeneous": homogeneous_value,
            "lower_to_top": lower_value, "full_direct": full_value, "correction": correction,
            "defect": selection["scalar"]},
        "literal": actor_literal(packet, tables, selection, relation, index, source)})
    return materialization, source, full_top


def materialize_seed(p2: Any, m: Any, packet: Any, tables: Any, index: Any, scan: Any) -> Any:
    selection = scan["result"]["first_hit"]
    seed, character = selection["seed"], selection["character"]
    source = p2.packet_row(packet, character, seed)
    full_top = b"".join(p2.packet_row(packet, a, seed) for a in range(4))
    relation = packet["relations"]["seeds"][seed]
    nodes = sorted({event["global_index"] for event in relation["raw_events"]})
    references = {x["node"]: x for x in packet["roots"]["roots"]}
    selected_refs = [{k: v for k, v in references[node].items() if k != "lift_components"} for node in nodes]
    require(all(reference == index["references"][reference["node"]] for reference in selected_refs),
            "seed_packet_canonical_roots_join")
    require(m.dot(scan["groups"][character][0], m.unpack(source, TOP_WIDTH)) == selection["scalar"],
            "selected_seed_packet_scalar")
    materialization = seal("materialization", {"selection": selection, "mode": "immutable-seed-packet",
        "source_d_sha256": sha(source), "source_full_top_sha256": sha(full_top), "lower_zero": True,
        "components": packet["receipts"]["seeds"][seed]["reduced_components"], "input": None,
        "relation": relation, "p1_references": selected_refs,
        "lift_components": [{"node": node, "components": references[node]["lift_components"]} for node in nodes],
        "direct_pairing": None, "literal": p2.literal_reference(packet, tables, selection, source)})
    return materialization, source, full_top


def materialize(m: Any, base: Any, p2: Any, packet: Any, tables: Any, p1: Any, task554: Any,
                index: Any, context: Any, scan: Any) -> Any:
    selection = scan["result"]["first_hit"]
    require(selection is not None and selection["scalar"] in (1, 2), "materializer_nonzero_selection")
    if selection["origin_kind"] == "seed":
        return materialize_seed(p2, m, packet, tables, index, scan)
    require(selection["origin_kind"] == "actor", "materializer_origin_kind")
    return materialize_actor(m, base, packet, tables, p1, task554, index, context, scan)


def derived_rho2(m: Any, state: Any, step: int) -> Any:
    return {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": m.RHO2_SHA256,
        "accepted_target_derivation_parents": state["accepted_target_derivation_parents"],
        "accepted_identity_convention": {
            "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",
            "packet_steps": "parent_remainder - child_remainder = target.scalar * accepted_packet_normalized_row"},
        "new_identity_convention": "parent_remainder - child_remainder = target.scalar * normalized_row",
        "newly_executed_target_steps": step}


def next_separator(m: Any, state: Any, normalized: bytes, lead: int, target: bytes, step: int) -> Any:
    free = m.first_nonzero(target, PHYSICAL_WIDTH)
    require(free is not None and free[0] not in set(state["leads"]) | {lead}, "next_free_coordinate")
    functional = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    functional[free[0]] = free[1]
    all_rows = [*state["rows"], normalized]
    all_records = [*state["records"], {"offer": state["generation"], "lead": lead}]
    for count, (record, raw) in enumerate(zip(reversed(all_records), reversed(all_rows)), 1):
        row = m.unpack(raw, PHYSICAL_WIDTH)
        coordinate = record["lead"]
        require(row[coordinate] == 1 and functional[coordinate] == 0, "next_lambda_pivot_coordinate")
        functional[coordinate] = (-m.dot(row, functional)) % 3
        require(m.dot(row, functional) == 0, "next_lambda_reverse_equation")
        if count % 256 == 0 or count == len(all_rows):
            boundary("new-lambda", step=step, rows=count, total=len(all_rows))
    direct = m.check_final_separator(functional, all_rows, state["target_raw"], target)
    raw_lambda = m.pack(functional)
    return {"free_coordinate": free[0], "free_value": free[1], "lambda_sha256": sha(raw_lambda),
            "direct_pairing": direct, "lambda_rho2": derived_rho2(m, state, step)}, raw_lambda


def head_record(state: Any, owner_sha: str, packet: Any, start: Any, source: Any, index_sha: str) -> Any:
    return seal("head", {"owner_sha256": owner_sha, "producer_sha256": source["producer_sha256"],
        "source_sha256": sha(canonical(source)), "start_sha256": sha(canonical(start)),
        "canonical_index_sha256": index_sha, "packet_manifest_sha256": packet["manifest_sha256"],
        "completed_steps": state["completed_steps"], "step_manifest_sha256": state["step_manifest_sha256"],
        "current_scan_manifest_sha256": state["current_scan_manifest_sha256"],
        "rank": state["rank"], "generation": state["generation"], "state_head": state["head"],
        "kind": state["kind"]})


def advance_state(m: Any, state: Any, manifest: Any, instruction: Any, normalized: bytes,
                  target: bytes, lambda_raw: bytes | None) -> None:
    state["records"].append({"offer": instruction["offer"], "lead": instruction["lead"],
        "physical_offset": instruction["physical_offset"], "rank": instruction["rank"],
        "rolling_sha256": instruction["rolling_sha256"]})
    state["rows"].append(normalized)
    state["leads"].append(instruction["lead"])
    state["previous_target_raw"] = state["target_raw"]
    state.update({"rank": manifest["rank"], "generation": manifest["generation"],
        "head": manifest["state_head"], "completed_steps": manifest["step"],
        "step_manifest_sha256": sha(canonical(manifest)), "current_scan_manifest_sha256": None,
        "target_raw": target, "lambda_raw": lambda_raw, "kind": manifest["kind"],
        "lambda": m.unpack(lambda_raw, PHYSICAL_WIDTH) if lambda_raw is not None else None})


def append_step(m: Any, state: Any, packet: Any, tables: Any, scan: Any,
                materialization: Any, source: bytes, full_top: bytes, owner_sha: str,
                index_sha: str, output: Path) -> None:
    """Compute one new pivot, seal its whole directory, then update RAM state."""
    selection = scan["result"]["first_hit"]
    require(selection is not None and selection["scalar"] in (1, 2) and
            state["completed_steps"] < CAP and state["kind"] == "Separator" and
            state["current_scan_manifest_sha256"] == scan["manifest_sha256"] and
            materialization["selection"] == selection, "append_selected_complete_scan")
    step, character = state["completed_steps"] + 1, selection["character"]
    dense = m.unpack(source, TOP_WIDTH)
    require(materialization["lower_zero"] is True and materialization["source_d_sha256"] == sha(source) and
            materialization["source_full_top_sha256"] == sha(full_top) and
            full_top[character * TOP_BYTES:(character + 1) * TOP_BYTES] == source,
            "append_complete_materialization_source")
    physical = m.apply_sparse(tables[character]["forward"]["B"], TOP_WIDTH, PHYSICAL_WIDTH, dense)
    q_d, lambda_g = m.dot(scan["groups"][character][0], dense), m.dot(state["lambda"], physical)
    require(q_d == lambda_g == selection["scalar"], "selected_physical_adjoint_pairing")
    physical_raw = m.pack(physical)
    remainder, reductions = m.physical_reduce(physical_raw, state["records"], state["rows"])
    require(m.dot(state["lambda"], m.unpack(remainder, PHYSICAL_WIDTH)) == q_d,
            "selected_physical_remainder_pairing")
    normalized, lead, scale = m.normalize_pivot(remainder, state["leads"])
    target, target_scalar = m.update_target(state["target_raw"], normalized, lead, state["leads"])
    kind = "Member" if m.first_nonzero(target, PHYSICAL_WIDTH) is None else "Separator"
    separator, lambda_raw = (None, None)
    if kind == "Separator":
        separator, lambda_raw = next_separator(m, state, normalized, lead, target, step)
    materialization_sha = sha(canonical(materialization))
    instruction = {"schema": SCHEMA + ".instruction", "step": step, "predecessor": state["head"],
        "offer": state["generation"], "generation": state["generation"] + 1,
        "rank": state["rank"] + 1, "lead": lead, "sigma": scale,
        "physical_offset": state["rank"] * PHYSICAL_BYTES, "selected": selection,
        "packet_manifest_sha256": packet["manifest_sha256"],
        "scan_manifest_sha256": scan["manifest_sha256"], "materialization_sha256": materialization_sha,
        "source_d_sha256": sha(source), "canonical_index_sha256": index_sha,
        "physical_reductions": reductions, "physical_sha256": sha(normalized),
        "target_scalar": target_scalar, "target_remainder_sha256": sha(target)}
    new_head = sha(bytes.fromhex(state["head"]) + canonical(instruction))
    instruction["rolling_sha256"] = new_head
    result = seal("step-result", {"step": step, "kind": kind, "owner_sha256": owner_sha,
        "packet_manifest_sha256": packet["manifest_sha256"], "parent_state_head": state["head"],
        "state_head": new_head, "rank_before": state["rank"], "rank_after": state["rank"] + 1,
        "generation_before": state["generation"], "generation_after": state["generation"] + 1,
        "selection": selection, "scan_manifest_sha256": scan["manifest_sha256"],
        "materialization_sha256": materialization_sha, "pairings": {"q_d": q_d, "lambda_G": lambda_g},
        "pivot": {"lead": lead, "scale": scale, "reductions": reductions, "normalized_sha256": sha(normalized)},
        "target": {"parent_remainder_sha256": sha(state["target_raw"]),
                   "remainder_sha256": sha(target), "scalar": target_scalar},
        "separator": separator, "literal": materialization["literal"], **ASSURANCE})
    payloads = {"physical-raw.bin": physical_raw, "physical-remainder.bin": remainder,
        "physical-normalized.bin": normalized, "target-remainder.bin": target,
        "source-d.bin": source, "source-full-top.bin": full_top, "materialization.json": canonical(materialization),
        "instruction.json": canonical(instruction), "result.json": canonical(result)}
    if lambda_raw is not None:
        payloads["lambda.bin"] = lambda_raw
    check_deadline("before-step-publication")
    manifest = write_bundle(output / "steps", step, "step-manifest", {"step": step, "owner_sha256": owner_sha,
        "packet_manifest_sha256": packet["manifest_sha256"],
        "predecessor_step_manifest_sha256": state["step_manifest_sha256"],
        "parent_state_head": state["head"], "state_head": new_head, "rank": state["rank"] + 1,
        "generation": state["generation"] + 1, "kind": kind, "scan_manifest_sha256": scan["manifest_sha256"]}, payloads)
    # No cooperative stop between durable step and caller's HEAD write.
    advance_state(m, state, manifest, instruction, normalized, target, lambda_raw)
    progress("step-durable", step=step, rank=state["rank"], kind=kind, selected=selection)


def validate_materialization_metadata(m: Any, p2: Any, packet: Any, tables: Any, index: Any,
                                      selection: Any, value: Any, source: bytes, full_top: bytes) -> None:
    character = selection["character"]
    require(sealed_ok(value, "materialization") and value["selection"] == selection and
            value["source_d_sha256"] == sha(source) and value["source_full_top_sha256"] == sha(full_top) and
            value["lower_zero"] is True and len(source) == TOP_BYTES and len(full_top) == 4 * TOP_BYTES and
            full_top[character * TOP_BYTES:(character + 1) * TOP_BYTES] == source,
            "resume_materialization_source")
    parts = empty_lift(m)
    parts[2][:] = m.unpack(full_top, 4 * TOP_WIDTH).reshape(4, TOP_WIDTH)
    require(value["components"] == component_receipts(m, parts), "resume_full_defect_components")
    relation = value["relation"]
    if selection["origin_kind"] == "seed":
        require(value["mode"] == "immutable-seed-packet" and value["input"] is None and
                value["direct_pairing"] is None and relation == packet["relations"]["seeds"][selection["seed"]] and
                source == p2.packet_row(packet, character, selection["seed"]) and
                value["literal"] == p2.literal_reference(packet, tables, selection, source), "resume_seed_reference")
        nodes = {event["global_index"] for event in relation["raw_events"]}
    else:
        require(selection["origin_kind"] == "actor" and value["mode"] == "complete-filtered-actor" and
                sealed_ok(relation, "actor-relation") and relation["basis_i"] == selection["basis_i"] and
                relation["actor"] == selection["actor"] == ACTORS[selection["actor_slot"]] and
                relation["actor_slot"] == selection["actor_slot"] and
                value["input"]["basis_i"] == selection["basis_i"] and value["input"]["p1_reference"] ==
                index["references"][selection["basis_i"]] and
                value["literal"] == actor_literal(packet, tables, selection, relation, index, source),
                "resume_actor_reference")
        rolling, coefficients = ZERO_HEAD, {}
        for ordinal, event in enumerate(relation["raw_events"]):
            unsigned = {k: v for k, v in event.items() if k != "rolling_sha256"}
            node, coefficient = event["global_index"], event["coefficient"]
            require(event["event_id"] == ordinal and event["node"] == node and 0 <= node < P1_ROWS and
                    coefficient in (1, 2), "resume_actor_event_metadata")
            rolling = sha(bytes.fromhex(rolling) + canonical(unsigned))
            require(event["rolling_sha256"] == rolling, "resume_actor_event_chain")
            coefficients[node] = (coefficients.get(node, 0) + coefficient) % 3
        require(relation["raw_event_count"] == len(relation["raw_events"]) and
                relation["raw_event_final_head"] == rolling and relation["referenced_nodes"] == sorted(coefficients) and
                relation["cancelled_nodes"] == [node for node in sorted(coefficients) if not coefficients[node]] and
                relation["final_coefficients"] == [[node, coefficients[node]] for node in sorted(coefficients)
                                                  if coefficients[node]], "resume_actor_global_coefficient_receipt")
        nodes = set(coefficients) | {selection["basis_i"]}
        pairings = value["direct_pairing"]
        require(pairings["defect"] == selection["scalar"] and pairings["full_direct"] ==
                (pairings["homogeneous"] + pairings["lower_to_top"]) % 3 and
                pairings["defect"] == (pairings["full_direct"] - pairings["correction"]) % 3,
                "resume_actor_direct_pairing_receipt")
    require(value["p1_references"] == [index["references"][node] for node in sorted(nodes)] and
            [x["node"] for x in value["lift_components"]] == sorted(nodes) and
            all(x["components"][0] == {"role": "p1-degree2", "bytes": m.P1_ROW_BYTES,
                "sha256": index["references"][x["node"]]["row_sha256"]} for x in value["lift_components"]),
            "resume_all_literal_references")


def load_prefix(m: Any, base: Any, p2: Any, output: Path, state: Any, packet: Any, tables: Any,
                p1: Any, index: Any, owner_sha: str, start: Any, source: Any, head: Any) -> Any:
    """Authenticate saved scans and rows; do not redo completed scans/inserts."""
    index_sha = sha(canonical(index))
    require(sealed_ok(head, "head") and head["owner_sha256"] == owner_sha and
            head["producer_sha256"] == source["producer_sha256"] and
            head["source_sha256"] == sha(canonical(source)) and head["start_sha256"] == sha(canonical(start)) and
            head["canonical_index_sha256"] == index_sha and head["packet_manifest_sha256"] == packet["manifest_sha256"] and
            type(head["completed_steps"]) is int and 0 <= head["completed_steps"] <= CAP, "resume_same_owner_head")
    for step in range(1, head["completed_steps"] + 1):
        require(state["kind"] == "Separator", "resume_step_after_member")
        manifest, payloads = read_bundle(m, output / "steps" / str(step).zfill(6), "step-manifest")
        require(manifest["step"] == step and manifest["owner_sha256"] == owner_sha and
                manifest["packet_manifest_sha256"] == packet["manifest_sha256"] and
                manifest["predecessor_step_manifest_sha256"] == state["step_manifest_sha256"] and
                manifest["parent_state_head"] == state["head"] and manifest["rank"] == state["rank"] + 1 and
                manifest["generation"] == state["generation"] + 1 and manifest["kind"] in ("Member", "Separator"),
                "resume_step_parent_chain")
        scan = load_scan(m, base, output, state, tables, p1, owner_sha, index_sha, manifest["scan_manifest_sha256"])
        selection = scan["result"]["first_hit"]
        require(selection is not None, "resume_selected_scan_hit")
        kind = manifest["kind"]
        wanted_files = {"physical-raw.bin", "physical-remainder.bin", "physical-normalized.bin",
            "target-remainder.bin", "source-d.bin", "source-full-top.bin", "materialization.json",
            "instruction.json", "result.json"} | ({"lambda.bin"} if kind == "Separator" else set())
        require(set(payloads) == wanted_files, "resume_step_payload_roster")
        instruction = json.loads(payloads["instruction.json"].decode("ascii"))
        unsigned = {k: v for k, v in instruction.items() if k != "rolling_sha256"}
        require(canonical(instruction) == payloads["instruction.json"] and instruction["schema"] == SCHEMA + ".instruction" and
                instruction["step"] == step and instruction["predecessor"] == state["head"] and
                instruction["rolling_sha256"] == manifest["state_head"] == sha(bytes.fromhex(state["head"]) + canonical(unsigned)) and
                instruction["offer"] == state["generation"] and instruction["generation"] == manifest["generation"] and
                instruction["rank"] == manifest["rank"] and instruction["physical_offset"] == state["rank"] * PHYSICAL_BYTES and
                instruction["packet_manifest_sha256"] == packet["manifest_sha256"] and
                instruction["scan_manifest_sha256"] == scan["manifest_sha256"] and
                instruction["canonical_index_sha256"] == index_sha and instruction["selected"] == selection and
                instruction["materialization_sha256"] == sha(payloads["materialization.json"]) and
                instruction["source_d_sha256"] == sha(payloads["source-d.bin"]), "resume_instruction_chain")
        materialization = decoded(payloads["materialization.json"], "materialization")
        validate_materialization_metadata(m, p2, packet, tables, index, selection, materialization,
                                          payloads["source-d.bin"], payloads["source-full-top.bin"])
        result = decoded(payloads["result.json"], "step-result")
        require(result["step"] == step and result["kind"] == kind and result["owner_sha256"] == owner_sha and
                all(result[k] == v for k, v in ASSURANCE.items()) and
                result["packet_manifest_sha256"] == packet["manifest_sha256"] and
                result["parent_state_head"] == state["head"] and result["state_head"] == manifest["state_head"] and
                result["rank_before"] == state["rank"] and result["rank_after"] == manifest["rank"] and
                result["generation_before"] == state["generation"] and result["generation_after"] == manifest["generation"] and
                result["selection"] == selection and result["scan_manifest_sha256"] == scan["manifest_sha256"] and
                result["materialization_sha256"] == instruction["materialization_sha256"] and
                result["literal"] == materialization["literal"] and
                result["pairings"] == {"q_d": selection["scalar"], "lambda_G": selection["scalar"]},
                "resume_step_result_join")
        normalized, target = payloads["physical-normalized.bin"], payloads["target-remainder.bin"]
        row, target_dense = m.unpack(normalized, PHYSICAL_WIDTH), m.unpack(target, PHYSICAL_WIDTH)
        lead = instruction["lead"]
        require(type(lead) is int and 0 <= lead < PHYSICAL_WIDTH and lead not in state["leads"] and
                m.first_nonzero(normalized, PHYSICAL_WIDTH) == (lead, 1) and
                all(row[i] == target_dense[i] == 0 for i in state["leads"]) and target_dense[lead] == 0 and
                instruction["sigma"] in (1, 2) and instruction["target_scalar"] in (0, 1, 2) and
                sha(normalized) == instruction["physical_sha256"] == result["pivot"]["normalized_sha256"] and
                result["pivot"]["lead"] == lead and result["pivot"]["scale"] == instruction["sigma"] and
                result["pivot"]["reductions"] == instruction["physical_reductions"] and
                result["target"] == {"parent_remainder_sha256": sha(state["target_raw"]),
                    "remainder_sha256": sha(target), "scalar": instruction["target_scalar"]} and
                sha(target) == instruction["target_remainder_sha256"] and bool(np.any(target_dense)) == (kind == "Separator"),
                "resume_normalized_target_metadata")
        lambda_raw = payloads.get("lambda.bin")
        if kind == "Separator":
            require(result["separator"]["lambda_sha256"] == sha(lambda_raw) and
                    result["separator"]["lambda_rho2"] == derived_rho2(m, state, step), "resume_derived_separator")
        else:
            require(result["separator"] is None, "resume_member_separator")
        advance_state(m, state, manifest, instruction, normalized, target, lambda_raw)
        progress("resume-step", step=step, rank=state["rank"])
        check_deadline("resume-prefix-loading")
    state["current_scan_manifest_sha256"] = head["current_scan_manifest_sha256"]
    require(head_record(state, owner_sha, packet, start, source, index_sha) == head, "resume_final_head_join")
    scan = None
    if state["kind"] == "Separator":
        m.check_final_separator(state["lambda"], state["rows"], state["previous_target_raw"], state["target_raw"])
        if state["current_scan_manifest_sha256"] is not None:
            scan = load_scan(m, base, output, state, tables, p1, owner_sha, index_sha,
                             state["current_scan_manifest_sha256"])
    else:
        require(state["current_scan_manifest_sha256"] is None, "member_has_no_current_scan")
    return scan


def quarantine_uncommitted(output: Path, state: Any) -> None:
    for name, count in (("steps", state["completed_steps"]),
            ("scans", state["completed_steps"] - (state["current_scan_manifest_sha256"] is None))):
        parent = output / name
        require(parent.is_dir() and not parent.is_symlink(), "prefix_directory")
        minimum = 1 if name == "steps" else 0
        for path in list(parent.iterdir()):
            require(path.is_dir() and not path.is_symlink(), "prefix_child_directory")
            if path.name.startswith((".pending-", ".orphan-")):
                continue
            require(len(path.name) == 6 and path.name.isascii() and path.name.isdigit() and
                    minimum <= int(path.name) <= CAP, "prefix_child_name")
            if int(path.name) > count:
                os.replace(path, parent / (".orphan-" + path.name + "-" + uuid.uuid4().hex))
        sync_directory(parent)


def terminal_for(scan: Any, completed_steps: int, cap: int, resource_stop: bool) -> str | None:
    if scan is not None and scan["first_hit"] is None:
        return "ROOT_ORIGINS_ZERO"
    if resource_stop:
        return "UNKNOWN_RESOURCE"
    if completed_steps >= cap:
        return "UNKNOWN_CAP"
    return None


def terminal_result(m: Any, state: Any, packet: Any, owner_sha: str, head: Any, scan: Any, terminal: str) -> Any:
    return seal("result", {"status": "PASS", "terminal": terminal, "head_sha256": sha(canonical(head)),
        "packet_manifest_sha256": packet["manifest_sha256"], "owner_sha256": owner_sha,
        "completed_steps": state["completed_steps"], "rank": state["rank"], "generation": state["generation"],
        "state_head": state["head"], "scan_manifest_sha256": state["current_scan_manifest_sha256"],
        "scan": scan["result"] if scan is not None else None,
        "lambda_rho2": derived_rho2(m, state, state["completed_steps"]) if state["kind"] == "Separator" else None,
        "scope": SCOPE, "claims": CLAIMS, **ASSURANCE})


def request_stop(_signal: int, _frame: Any) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def run_actual(args: Any) -> Any:
    global DEADLINE
    output = args.output_root.resolve()
    parents = [args.state_root, args.delta_root, args.seed34_root, args.packet_root, args.prepare_root,
               *args.block_root, args.p1_root, args.task712_root]
    require(not args.output_root.is_symlink(), "output_symlink")
    for path in parents:
        parent = path.resolve()
        require(path.is_dir() and output != parent and output not in parent.parents and parent not in output.parents,
                "disjoint_output_parents")
    require(args.resume == output.exists(), "existing_output_requires_resume")
    DEADLINE = STARTED + args.max_seconds
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, request_stop)
    p2 = fixed_module()
    m, base, descriptors = p2.dependencies()
    boundary("dependencies")
    state, start, owner, p1, task554, tables, packet = load_start(p2, m, base, descriptors, args)
    for table in tables:
        for actor in ACTORS:
            base.check_table_transpose(table["forward"][actor], table["adjoint"][actor])
    source = seal("source", {"producer_sha256": sha(Path(__file__).read_bytes()),
        "modules": {FIXED_MODULE: FIXED_MODULE_SHA, **p2.MODULE_PINS}, "data": p2.DATA_PINS,
        "python": sys.version, "numpy": np.__version__})
    owner_sha = sha(canonical(owner))
    if args.resume:
        for name, expected, kind in (("owner.json", owner, "owner"), ("start.json", start, "start"),
                                     ("source.json", source, "source")):
            require(read_json(m.safe_file(output, name), kind) == expected, "same_owner_resume:" + name)
    else:
        output.mkdir(parents=True)
        for name, value in (("owner.json", owner), ("start.json", start), ("source.json", source)):
            write_atomic(output, name, canonical(value))
        (output / "scans").mkdir()
        (output / "steps").mkdir()
        sync_directory(output)
    top_files = {"owner.json", "start.json", "source.json", "canonical-index.json", "HEAD", "result.json",
                 "resource-stop.json", "scans", "steps"}
    for path in output.iterdir():
        require(path.name in top_files or any(path.name.startswith("." + name + ".pending-")
                for name in top_files if name.endswith(".json") or name == "HEAD"), "output_unknown_file")
        require(not path.is_symlink(), "output_child_symlink")
    if (output / "canonical-index.json").exists():
        index = read_json(m.safe_file(output, "canonical-index.json"), "canonical-p1-index")
    else:
        require(not (output / "HEAD").exists(), "head_requires_canonical_index")
        index = canonical_index(m, p1)
        write_atomic(output, "canonical-index.json", canonical(index))
    validate_index(index, p1, packet)
    index_sha = sha(canonical(index))
    scan = None
    if (output / "HEAD").exists():
        head = read_json(m.safe_file(output, "HEAD"), "head")
        scan = load_prefix(m, base, p2, output, state, packet, tables, p1, index, owner_sha, start, source, head)
    else:
        head = head_record(state, owner_sha, packet, start, source, index_sha)
        write_atomic(output, "HEAD", canonical(head))
    quarantine_uncommitted(output, state)
    context = None
    try:
        while True:
            if state["kind"] == "Member":
                terminal = "MEMBER_CANDIDATE"
                break
            if scan is None:
                check_deadline("before-current-scan")
                if context is None:
                    context, _ = base.source_context()
                scan = make_scan(m, base, p2, state, tables, packet, p1, task554, context, owner_sha, index_sha, output)
                state["current_scan_manifest_sha256"] = scan["manifest_sha256"]
                head = head_record(state, owner_sha, packet, start, source, index_sha)
                write_atomic(output, "HEAD", canonical(head), replace=True)
            stopped = STOP_REQUESTED or time.monotonic() >= DEADLINE
            terminal = terminal_for(scan["result"], state["completed_steps"], args.max_appends, stopped)
            if terminal is not None:
                break
            if context is None:
                context, _ = base.source_context()
            materialization, selected_source, full_top = materialize(
                m, base, p2, packet, tables, p1, task554, index, context, scan)
            append_step(m, state, packet, tables, scan, materialization, selected_source, full_top,
                        owner_sha, index_sha, output)
            head = head_record(state, owner_sha, packet, start, source, index_sha)
            write_atomic(output, "HEAD", canonical(head), replace=True)
            scan = None
            progress("head-advanced", step=state["completed_steps"], rank=state["rank"], state_head=state["head"])
    except ResourceStop as exc:
        terminal = "UNKNOWN_RESOURCE"
        progress("resource-stop", phase_stopped=str(exc), completed_steps=state["completed_steps"])
    head = head_record(state, owner_sha, packet, start, source, index_sha)
    require(read_json(m.safe_file(output, "HEAD"), "head") == head, "terminal_head_join")
    result = terminal_result(m, state, packet, owner_sha, head, scan, terminal)
    write_atomic(output, "result.json", canonical(result), replace=(output / "result.json").exists())
    progress("terminal", terminal=terminal, completed_steps=state["completed_steps"], rank=state["rank"])
    return result


def expect_reject(action: Any, label: str) -> None:
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError("canary_mutation_accepted:" + label)


def parent_layout_selftest(args: Any) -> Any:
    p2 = fixed_module()
    accepted_old = p2.parent_layout_selftest(args)
    objects, bundles = read_packet_metadata(p2, args.packet_root)
    layout = packet_parent_layout(p2, objects, bundles)
    rejected = list(accepted_old["rejected_cases"])
    for name in ("packet-instruction-generic-seal", "packet-target-generic-seal", "packet-target-parent",
                 "packet-step-chain", "packet-final-head"):
        changed_objects, changed_bundles = copy.deepcopy(objects), copy.deepcopy(bundles)
        if name == "packet-instruction-generic-seal":
            changed_bundles[0]["instruction"]["sha256"] = ZERO_HEAD
        elif name == "packet-target-generic-seal":
            changed_bundles[0]["result"]["target"]["sha256"] = ZERO_HEAD
        elif name == "packet-target-parent":
            changed_bundles[2]["result"]["target"]["parent_remainder_sha256"] = ZERO_HEAD
        elif name == "packet-step-chain":
            changed_bundles[1]["manifest"]["predecessor_step_manifest_sha256"] = ZERO_HEAD
        else:
            changed_objects["output/HEAD"]["state_head"] = ZERO_HEAD
        expect_reject(lambda: packet_parent_layout(p2, changed_objects, changed_bundles), name)
        rejected.append(name)
    require(len(rejected) == 10 and layout["steps"][2]["target_scalar"] == 0,
            "actual_layout_mutation_roster_and_legal_zero")
    return {"schema": SCHEMA + ".parent-layout-selftest", "status": "PASS", "metadata_only": True,
        "parent_layout": accepted_old["parent_layout"], "accepted_packet_layout": layout,
        "rejected_cases": rejected, "cross_checked": False, "verified": False}


def selftest() -> Any:
    """Focused changed-interface tests, without actual historical scalar runs."""
    p2 = fixed_module()
    m, base, _ = p2.dependencies()
    context, _ = base.source_context()
    q = (np.arange(TOP_WIDTH, dtype=np.uint32) % 3).astype(np.uint8)
    chosen = None
    for actor in ACTORS:
        lower_adjoint, top_adjoint = base.actor_adjoint(context, q, 0, actor)
        if np.any(lower_adjoint):
            chosen = actor, lower_adjoint, top_adjoint
            break
    require(chosen is not None, "canary_nonzero_actor_lower_to_top")
    actor, lower_adjoint, top_adjoint = chosen
    lower_input = np.zeros(LOWER_WIDTH, dtype=np.uint8)
    lower_input[int(np.flatnonzero(lower_adjoint)[0])] = 1
    d0, d1, aux = base._split_lower(lower_input)
    zero_top = np.zeros((4, TOP_WIDTH), dtype=np.uint8)
    lower_parts = (d0, d1, zero_top, aux)
    lower_acted = filtered_actor_source(base, context, lower_parts, actor)
    lower_value = m.dot(q, lower_acted[2][0])
    require(lower_value == m.dot(lower_adjoint, lower_input) and lower_value in (1, 2),
            "canary_production_filtered_actor_lower_pairing")
    top_input = ((2 * np.arange(TOP_WIDTH, dtype=np.uint32) + 1) % 3).astype(np.uint8)
    mixed_top = zero_top.copy()
    mixed_top[0] = top_input
    mixed_acted = filtered_actor_source(base, context, (d0, d1, mixed_top, aux), actor)
    homogeneous_value = m.dot(top_adjoint, top_input)
    mixed_value = m.dot(q, mixed_acted[2][0])
    require(mixed_value == (lower_value + homogeneous_value) % 3 and mixed_value != homogeneous_value,
            "canary_homogeneous_only_consumer_rejected")

    top = bytearray(4 * NSEEDS * TOP_BYTES)
    vector1, vector3 = np.zeros(TOP_WIDTH, dtype=np.uint8), np.zeros(TOP_WIDTH, dtype=np.uint8)
    vector1[0], vector3[1] = 1, 1
    for character, seed, row in ((1, 2, vector1), (3, 7, vector3)):
        offset = (character * NSEEDS + seed) * TOP_BYTES
        top[offset:offset + TOP_BYTES] = m.pack(row)
    packet = {"manifest_sha256": sha(b"task954-synthetic-packet"), "tops": bytes(top),
        "relations": {"seeds": [p2.seal("seed-relation", {"seed": seed, "raw_events": [],
            "raw_event_count": 0, "raw_event_final_head": ZERO_HEAD, "final_coefficients": []}) for seed in range(NSEEDS)]},
        "roots": p2.seal("p1-roots", {"roots": []}),
        "receipts": {"raw_seeds": [{"compact_word_sha256": sha(b"fixture-word")}] * NSEEDS,
            "seeds": [], "premises": {"projectors": p2.projector_receipts(m, base)}}}
    for seed in range(NSEEDS):
        parts = empty_lift(m)
        parts[2][:] = np.asarray([m.unpack(p2.packet_row(packet, a, seed), TOP_WIDTH) for a in range(4)])
        packet["receipts"]["seeds"].append({"reduced_components": component_receipts(m, parts)})
    tables = [{"forward": {"B": [], **{actor: [] for actor in ACTORS}},
        "identity": {"forward:B": "fixture-B-" + str(a), "adjoint:B": "fixture-Badj-" + str(a)}} for a in range(4)]
    tables[1]["forward"]["B"] = [[0, 5, 1]]
    tables[3]["forward"]["B"] = [[1, 7, 1]]
    old, target, lam = (np.zeros(PHYSICAL_WIDTH, dtype=np.uint8) for _ in range(3))
    old[2], target[5], target[7], lam[5] = 1, 1, 1, 1
    initial = {"rows": [m.pack(old)], "records": [{"offer": 0, "lead": 2, "physical_offset": 0}],
        "leads": [2], "rank": 1, "generation": 1, "head": sha(b"task954-synthetic-start"),
        "lambda": lam, "lambda_raw": m.pack(lam), "target_raw": m.pack(target),
        "previous_target_raw": m.pack(target), "accepted_target_derivation_parents": [],
        "completed_steps": 0, "step_manifest_sha256": None, "current_scan_manifest_sha256": None, "kind": "Separator"}
    p1 = {"cache": {"sha256": sha(b"fixture-cache")}, "instruction": {"sha256": sha(b"fixture-instructions")}}
    index = seal("canonical-p1-index", {"synthetic_only": True, "references": []})
    index_sha, owner_sha = sha(canonical(index)), sha(b"fixture-owner")
    start = seal("start", {"synthetic_only": True})
    source = seal("source", {"producer_sha256": sha(b"fixture-producer")})

    def fixture_scan(state: Any, output: Path) -> Any:
        groups = fresh_vectors(base, tables, state)
        seeds = np.asarray([[m.dot(groups[a][0], m.unpack(p2.packet_row(packet, a, seed), TOP_WIDTH))
                             for seed in range(NSEEDS)] for a in range(4)], dtype=np.uint8)
        actors = np.zeros((4, P1_ROWS, 4), dtype=np.uint8)
        p1_values = np.zeros((4, 5, P1_ROWS), dtype=np.uint8)
        lowers = np.zeros_like(actors)
        payloads = scan_payloads(m, groups, seeds, actors, p1_values, lowers)
        result = scan_result(m, base, state, tables, owner_sha, index_sha, p1, groups, seeds, actors, payloads)
        payloads["result.json"] = canonical(result)
        manifest = write_bundle(output / "scans", state["completed_steps"], "scan-manifest", {
            "scan": state["completed_steps"], "owner_sha256": owner_sha, "canonical_index_sha256": index_sha,
            "rank": state["rank"], "generation": state["generation"], "state_head": state["head"],
            "lambda_sha256": sha(state["lambda_raw"])}, payloads)
        return {"manifest": manifest, "manifest_sha256": sha(canonical(manifest)), "result": result,
            "groups": groups, "seeds": seeds, "actors": actors, "p1_values": p1_values, "lower_values": lowers}

    with tempfile.TemporaryDirectory(prefix="task954-focused-canary-") as temporary:
        output = Path(temporary)
        (output / "steps").mkdir()
        (output / "scans").mkdir()
        produced = copy.deepcopy(initial)
        initial_head = head_record(produced, owner_sha, packet, start, source, index_sha)
        write_atomic(output, "HEAD", canonical(initial_head))
        before = fixture_scan(produced, output)
        require(read_json(output / "HEAD", "head") == initial_head, "canary_scan_durable_before_head")
        require(before["result"]["active_characters"] == [1] and before["result"]["first_hit"]["index"] == ORIGINS + 2 and
                terminal_for(before["result"], 0, 0, False) == "UNKNOWN_CAP" and
                terminal_for(before["result"], 0, CAP, True) == "UNKNOWN_RESOURCE", "canary_dynamic_selection_and_caps")
        produced["current_scan_manifest_sha256"] = before["manifest_sha256"]
        before_head = head_record(produced, owner_sha, packet, start, source, index_sha)
        write_atomic(output, "HEAD", canonical(before_head), replace=True)
        materialization, selected_source, full_top = materialize_seed(p2, m, packet, tables, index, before)
        append_step(m, produced, packet, tables, before, materialization, selected_source, full_top,
                    owner_sha, index_sha, output)
        require(read_json(output / "HEAD", "head") == before_head and
                (output / "steps" / "000001" / "manifest.json").is_file(), "canary_step_durable_before_head")
        head = head_record(produced, owner_sha, packet, start, source, index_sha)
        write_atomic(output, "HEAD", canonical(head), replace=True)
        after = fixture_scan(produced, output)
        produced["current_scan_manifest_sha256"] = after["manifest_sha256"]
        head = head_record(produced, owner_sha, packet, start, source, index_sha)
        write_atomic(output, "HEAD", canonical(head), replace=True)
        require(after["result"]["active_characters"] == [3] and after["result"]["first_hit"]["index"] == 3 * ORIGINS + 7 and
                terminal_for(after["result"], 1, 1, False) == "UNKNOWN_CAP", "canary_changed_character_terminal_scan")
        preserved = {str(path.relative_to(output)): path.read_bytes() for directory in (output / "scans", output / "steps")
                     for path in directory.rglob("*") if path.is_file()}
        (output / "steps" / ".pending-000002-synthetic").mkdir()
        (output / "scans" / ".orphan-000002-synthetic").mkdir()
        resumed = copy.deepcopy(initial)
        reused = load_prefix(m, base, p2, output, resumed, packet, tables, p1, index, owner_sha, start, source, head)
        quarantine_uncommitted(output, resumed)
        require(resumed["rows"] == produced["rows"] and resumed["target_raw"] == produced["target_raw"] and
                resumed["lambda_raw"] == produced["lambda_raw"] and reused["manifest_sha256"] == after["manifest_sha256"] and
                all((output / name).read_bytes() == raw for name, raw in preserved.items()), "canary_saved_scan_prefix_resume")
        bad_head = seal("head", {**{k: v for k, v in head.items() if k not in ("schema", "sha256")},
                                 "owner_sha256": sha(b"wrong-owner")})
        expect_reject(lambda: load_prefix(m, base, p2, output, copy.deepcopy(initial), packet, tables,
            p1, index, owner_sha, start, source, bad_head), "changed-owner")
        corrupt_path = output / "scans" / "000001" / "actors-c3.u8"
        corrupt = bytearray(corrupt_path.read_bytes())
        corrupt[-1] = 2
        corrupt_path.write_bytes(corrupt)
        expect_reject(lambda: load_scan(m, base, output, resumed, tables, p1, owner_sha, index_sha,
                                        after["manifest_sha256"]), "late-full-array-byte")
    return {"schema": SCHEMA + ".selftest", "status": "PASS", "synthetic_only": True,
        "tests": ["production-filtered-actor-nonzero-lower-to-top",
            "dynamic-characters-full-array-serialization-and-caps",
            "durable-scan-step-head-prefix-resume-cached-scan-and-corruption"],
        "actor_lower_to_top_pairing": lower_value, "actor_mixed_pairing": mixed_value,
        "cached_terminal_scan_sha256": after["manifest_sha256"], "cross_checked": False, "verified": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--parent-layout-selftest", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-appends", type=int, default=CAP)
    parser.add_argument("--max-seconds", type=float, default=1800.0)
    names = ("state-root", "delta-root", "seed34-root", "packet-root", "prepare-root", "p1-root", "task712-root")
    for name in names:
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--output", dest="output_root", type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    paths = [getattr(args, name.replace("-", "_")) for name in names] + [args.output_root]
    try:
        require(0 <= args.max_appends <= CAP and 0 < args.max_seconds < float("inf"), "bounded_resource_options")
        if args.parent_layout_selftest:
            require(not args.selftest and not args.resume and not args.block_root and
                    all(getattr(args, name) is not None for name in ("state_root", "delta_root", "seed34_root", "packet_root")) and
                    all(getattr(args, name) is None for name in ("prepare_root", "p1_root", "task712_root", "output_root")),
                    "parent_layout_only_actual_four_roots")
            result = parent_layout_selftest(args)
        elif args.selftest:
            require(not any(path is not None for path in paths) and not args.block_root and not args.resume,
                    "selftest_without_actual_parents")
            result = selftest()
        else:
            require(all(path is not None for path in paths) and len(args.block_root) == 4,
                    "actual_eleven_parent_paths_required")
            result = run_actual(args)
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 0
    except ResourceStop as exc:
        output = args.output_root.resolve() if args.output_root is not None else None
        head_raw = None
        if output is not None and (output / "HEAD").is_file() and not (output / "HEAD").is_symlink():
            head_raw = (output / "HEAD").read_bytes()
        diagnostic = seal("resource-stop", {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE",
            "phase": str(exc), "complete_prefix_present": head_raw is not None,
            "head_sha256": sha(head_raw) if head_raw is not None else None,
            "candidate": False, "cross_checked": False, "verified": False})
        if output is not None and output.is_dir() and not output.is_symlink():
            write_atomic(output, "resource-stop.json", canonical(diagnostic), replace=True)
        print(canonical(diagnostic).decode("ascii"), end="", flush=True)
        return 3
    except Exception as exc:
        progress("terminal", status="REJECTED", reason=str(exc), error_type=type(exc).__name__)
        print(canonical({"status": "REJECTED", "reason": str(exc), "cross_checked": False,
                         "verified": False}).decode("ascii"), end="", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
