#!/usr/bin/env python3
"""Task955: independent full-origin scans and complete selected-actor replay.

The accepted fixed44 prefix is an arithmetic premise. New actor evaluation
uses ordinary coefficients in F3[C3^3], not the producer's polynomial actor.
Only checker-owned arithmetic lineage is imported.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import re
import sys
import tempfile
import time
from typing import Any, Callable

import numpy as np

FIXED_CHECKER_SHA = "5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5"
_fixed_file = Path(__file__).resolve().with_name("check_d972_r07_fixed_root_packet_loop_v2.py")
if _fixed_file.is_symlink() or hashlib.sha256(_fixed_file.read_bytes()).hexdigest() != FIXED_CHECKER_SHA:
    raise ValueError("full_origin_checker:fixed_checker_source_pin")
import check_d972_r07_fixed_root_packet_loop_v2 as FIXED

LEGACY, BASE, ROOTS = FIXED.LEGACY, FIXED.BASE, FIXED.ROOTS
ARITH = BASE.ARITH
canonical, sha, pack, unpack, dot = FIXED.canonical, FIXED.sha, FIXED.pack, FIXED.unpack, FIXED.dot
seal, same, check_seal = FIXED.seal, FIXED.same, FIXED.check_seal
path, fixed, json_bytes = FIXED.path, FIXED.fixed, FIXED.json_bytes
subtract, file_receipt = FIXED.subtract, FIXED.file_receipt
SCHEMA = "d972.r07.full-origin-refinement.v1"
WIDTH, ROW_BYTES, SOURCE_WIDTH, SOURCE_BYTES = 48384, 12096, 36288, 9072
START_RANK, START_GENERATION, MAX_APPENDS = 1359, 8064, 32
ACTORS = (1, -1, 2, -2)
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
OLD_OFFSETS, NEW_OFFSETS = (0, 505, 1008, 1511), (2014, 3523, 5035, 6547)
ORIGINS_PER_CHARACTER = 32280
START_HEAD = "7b7380a7ddb785910347df14f47ba4634cc5fa2fff7c32b722455a824d6cddda"
START_LAMBDA = "60ac649575400e98881c5de5d4ef2c6202d3cf577da1411042104254edb004e2"
START_TARGET = "0a466426db600e191e9ee5563066dbb729492ab74d869dbf0ceeadc2b2f7f686"
PACKET_ARTIFACT = {"run": 33964709359, "attempt": 1,
    "head": "fff114c41bd8748ad0e708919fe0820335c9cce8", "id": 9969090590,
    "name": "d972-r07-fixed-root-packet-loop-v2-candidate-33964709359-1", "bytes": 1855391,
    "sha256": "sha256:b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428"}
PACKET_FILES = {
    "output/HEAD": (709, "c48e8f673b7da860b57b0d413a3f49e2035831ecabd4f790f964e6ba1a2f2fc2"),
    "output/result.json": (4493, "4cc9c95ac57db62de48095360e9f63056281176931f27ac184d2534a1d78d03b"),
    "checker-result.json": (4603, "b8308d60ca9332a02d2ca503753e7c72db54d6509c62b28a9aee648f44a2ca60"),
    "source-receipt.json": (2037, "513eea26bf5cf3288aaba3caaf4f8ca9095857d1af49154d4d7d69b23bd63886"),
    "output/start.json": (5025, "041d9dc7abcbddc81df490a2ab77acb40715c9bb0d7ca3a004d498d9efd00d6d"),
    "output/owner.json": (8274, "a8d206b0ae26f3bfcf102de2119f10bd7151d9dd9c6294d8e879656f1ced6f41"),
    "output/packet/manifest.json": (843, "d5e3ef0c0d691131b6bd1293d066d6e994c572086dc0c89a6e5ec766a8474199"),
}
SCOPE = {"characters": [0, 1, 2, 3], "seeds": 44, "p1_rows": 8059, "actors": list(ACTORS),
    "origins_per_character": 32280, "total_origins": 129120,
    "order": "character-major;seeds0..43;basis_i0..8058;actors1,-1,2,-2",
    "operational_append_cap": 32, "mathematical_total_bound": None}
CLAIMS = {"FULL_ORIGIN_REFINEMENT_CANDIDATE": True, "GRADE2_MEMBER": "NOT_DECIDED",
    "GRADE2_NONMEMBER": "NOT_DECIDED", "DUAL_CLOSURES": "NOT_EXECUTED", "A0": "NOT_DECLARED",
    "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED",
    "IHARA": "NOT_DECLARED", "verified": False}
BEGIN = time.monotonic()
DEADLINE: float | None = None
LAST_PHASE = "initialization"
REPLAYED_STEPS = 0
REPLAYED_SCANS = 0


class ResourceStop(Exception):
    pass


def require(ok: Any, label: str) -> None:
    if not ok:
        raise ValueError("full_origin_checker:" + label)


def boundary(phase: str, **fields: Any) -> None:
    global LAST_PHASE
    LAST_PHASE = phase
    print("R07_FULL_ORIGIN_CHECKER " + json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)
    if DEADLINE is not None and time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)


def read_json(root: Path, name: str, cap: int = 32 << 20) -> dict[str, Any]:
    item = path(root, name)
    require(item.stat().st_size <= cap, "json_cap:" + name)
    value = json_bytes(item.read_bytes())
    require(isinstance(value, dict), "json_object:" + name)
    return value


def authenticated_directory(root: Path, manifest: dict[str, Any]) -> dict[str, bytes]:
    check_seal(manifest)
    require(isinstance(manifest.get("files"), list), "manifest_files")
    names = [item["file"] for item in manifest["files"]]
    require(len(names) == len(set(names)) and sorted(names) == names, "manifest_file_order")
    require(manifest["file_roster"] == sorted([*names, "manifest.json"]) ==
            sorted(item.name for item in root.iterdir()), "manifest_roster")
    return {item["file"]: fixed(root, item["file"], (item["bytes"], item["sha256"]))
            for item in manifest["files"]}


def accepted_packet_metadata(args: argparse.Namespace) -> dict[str, Any]:
    """Exact JSON/byte/hash joins; no old insertion or packet reconstruction."""
    objects = {name: json_bytes(fixed(args.packet_root, name, pin)) for name, pin in PACKET_FILES.items()}
    head, terminal, checker, start, owner, packet_manifest = [objects[name] for name in
        ("output/HEAD", "output/result.json", "checker-result.json", "output/start.json",
         "output/owner.json", "output/packet/manifest.json")]
    for item, suffix in ((head, "head"), (terminal, "result"), (start, "start"), (owner, "owner"),
                         (packet_manifest, "packet-manifest")):
        check_seal(item)
        require(item["schema"] == FIXED.SCHEMA + "." + suffix, "accepted_packet_schema:" + suffix)
    require(head["completed_steps"] == terminal["completed_steps"] == checker["completed_steps"] == 3 and
            head["state_head"] == terminal["state_head"] == checker["state_head"] == START_HEAD and
            head["rank"] == terminal["rank"] == checker["rank"] == START_RANK and
            head["generation"] == terminal["generation"] == START_GENERATION and
            terminal["status"] == checker["status"] == "PASS" and
            terminal["terminal"] == checker["terminal"] == "ROOT_SEEDS_ZERO" and
            checker["schema"] == FIXED.SCHEMA + ".checker-result" and
            checker["head_sha256"] == terminal["head_sha256"] == PACKET_FILES["output/HEAD"][1] and
            checker["result_sha256"] == PACKET_FILES["output/result.json"][1] and
            head["owner_sha256"] == terminal["owner_sha256"] == packet_manifest["owner_sha256"] ==
            PACKET_FILES["output/owner.json"][1] and
            head["start_sha256"] == PACKET_FILES["output/start.json"][1] and
            head["packet_manifest_sha256"] == terminal["packet_manifest_sha256"] ==
            PACKET_FILES["output/packet/manifest.json"][1], "accepted_packet_authority")
    require(all(item["cross_checked"] is False and item["verified"] is False
                for item in (terminal, checker, packet_manifest, objects["source-receipt.json"])),
            "accepted_packet_assurance_flags")
    require(head["producer_sha256"] == "e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6",
            "accepted_packet_producer")
    packet_payloads = authenticated_directory(args.packet_root / "output/packet", packet_manifest)
    packet = {name: json_bytes(raw) for name, raw in packet_payloads.items() if name.endswith(".json")}
    for name, suffix in (("relations.json", "relations"), ("receipts.json", "packet-receipts"),
                         ("p1-roots.json", "p1-roots")):
        check_seal(packet[name]); require(packet[name]["schema"] == FIXED.SCHEMA + "." + suffix,
                                        "accepted_packet_document_schema")
    require(len(packet_payloads["tops.bin"]) == 176 * SOURCE_BYTES and
            len(packet["relations.json"]["seeds"]) == len(packet["receipts.json"]["seeds"]) == 44,
            "accepted_packet_dimensions")
    previous_head, previous_manifest, previous_target = FIXED.START_HEAD, None, FIXED.START_TARGET
    steps = []
    for number in range(1, 4):
        directory = args.packet_root / "output/steps" / f"{number:06d}"
        manifest = read_json(directory, "manifest.json")
        payloads = authenticated_directory(directory, manifest)
        result, instruction = json_bytes(payloads["result.json"]), json_bytes(payloads["instruction.json"])
        check_seal(result)
        require(manifest["schema"] == FIXED.SCHEMA + ".step-manifest" and
                result["schema"] == FIXED.SCHEMA + ".step-result" and
                instruction["schema"] == FIXED.SCHEMA + ".instruction", "accepted_step_schema")
        unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
        new_head = sha(bytes.fromhex(previous_head) + canonical(unsigned))
        require(manifest["step"] == result["step"] == instruction["step"] == number and
                manifest["parent_state_head"] == result["parent_state_head"] == instruction["predecessor"] == previous_head and
                manifest["state_head"] == result["state_head"] == instruction["rolling_sha256"] == new_head and
                manifest["predecessor_step_manifest_sha256"] == previous_manifest and
                manifest["kind"] == result["kind"] == "Separator" and
                manifest["owner_sha256"] == result["owner_sha256"] == head["owner_sha256"] and
                manifest["packet_manifest_sha256"] == result["packet_manifest_sha256"] ==
                instruction["packet_manifest_sha256"] == head["packet_manifest_sha256"] and
                manifest["rank"] == result["rank_after"] == instruction["rank"] == 1356 + number and
                result["rank_before"] == 1355 + number and
                manifest["generation"] == result["generation_after"] == instruction["generation"] == 8061 + number and
                result["generation_before"] == instruction["offer"] == 8060 + number and
                result["target"]["parent_remainder_sha256"] == previous_target and
                result["target"]["remainder_sha256"] == instruction["target_remainder_sha256"] ==
                sha(payloads["target-remainder.bin"]) and
                result["pivot"]["normalized_sha256"] == instruction["physical_sha256"] ==
                sha(payloads["physical-normalized.bin"]) and
                result["separator"]["lambda_sha256"] == sha(payloads["lambda.bin"]) and
                result["target"]["scalar"] == instruction["target_scalar"] and
                result["pivot"]["lead"] == instruction["lead"] and
                result["pivot"]["scale"] == instruction["sigma"] and
                result["pivot"]["reductions"] == instruction["physical_reductions"], "accepted_step_chain")
        same(result["selection"], instruction["selected"], "accepted_selection_join")
        require(result["selection"]["character"] == 0 and result["selection"]["seed"] == 34 + number,
                "accepted_seed35_36_37")
        previous_head, previous_target = new_head, sha(payloads["target-remainder.bin"])
        previous_manifest = sha(canonical(manifest))
        steps.append({"manifest": manifest, "manifest_sha256": previous_manifest,
            "result": result, "result_sha256": sha(payloads["result.json"]), "instruction": instruction,
            "payloads": payloads})
    require(previous_head == START_HEAD and previous_manifest == head["step_manifest_sha256"] and
            previous_target == START_TARGET and sha(steps[-1]["payloads"]["lambda.bin"]) == START_LAMBDA,
            "accepted_final_head")
    packet_semantics(head, steps)
    return {"objects": objects, "head": head, "start": start, "owner": owner,
            "packet": packet, "packet_payloads": packet_payloads, "steps": steps}


def packet_semantics(head: dict[str, Any], steps: list[dict[str, Any]]) -> None:
    """Production metadata join reused by the actual-parent refusal canary."""
    previous, target = FIXED.START_HEAD, FIXED.START_TARGET
    require(len(steps) == 3, "metadata_packet_step_count")
    for step in steps:
        result, instruction, manifest = step["result"], step["instruction"], step["manifest"]
        require("sha256" not in instruction and "rolling_sha256" in instruction,
                "packet_instruction_uses_rolling_seal")
        require(sorted(result["target"]) == ["parent_remainder_sha256", "remainder_sha256", "scalar"],
                "packet_target_is_plain")
        require(result["target"]["parent_remainder_sha256"] == target, "packet_plain_target_parent")
        require(manifest["parent_state_head"] == result["parent_state_head"] == instruction["predecessor"] == previous,
                "packet_step_state_parent")
        previous, target = instruction["rolling_sha256"], result["target"]["remainder_sha256"]
    require(head["state_head"] == previous == START_HEAD and head["rank"] == 1359 and
            head["generation"] == 8064 and target == START_TARGET, "packet_final_state_join")


def packet_layout(metadata: dict[str, Any]) -> dict[str, Any]:
    steps = []
    for number, item in enumerate(metadata["steps"], 1):
        result, instruction, manifest, payloads = item["result"], item["instruction"], item["manifest"], item["payloads"]
        steps.append({"role": f"packet-step-{number}", "step": number, "manifest_schema": manifest["schema"],
            "result_schema": result["schema"], "instruction_schema": instruction["schema"],
            "instruction_seal": "rolling_sha256", "target_seal": None,
            "target_keys": sorted(result["target"]), "target_scalar": result["target"]["scalar"],
            "manifest_sha256": item["manifest_sha256"], "result_sha256": item["result_sha256"],
            "instruction_sha256": sha(payloads["instruction.json"]), "target_sha256": sha(canonical(result["target"])),
            "state_head": manifest["state_head"], "parent_state_head": manifest["parent_state_head"],
            "rank": manifest["rank"], "generation": manifest["generation"],
            "physical_normalized_sha256": sha(payloads["physical-normalized.bin"]),
            "lambda_sha256": sha(payloads["lambda.bin"]), "target_remainder_sha256": sha(payloads["target-remainder.bin"])})
    return seal({"schema": SCHEMA + ".packet-parent-layout", "artifact": PACKET_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(PACKET_FILES.items())],
        "steps": steps, "rank": START_RANK, "generation": START_GENERATION, "state_head": START_HEAD,
        "lambda_sha256": START_LAMBDA, "target_remainder_sha256": START_TARGET, "old_target_history_replayed": False})


def expected_start(state: dict[str, Any]) -> dict[str, Any]:
    metadata = state["accepted_packet"]
    parents = list(metadata["start"]["accepted_target_derivation_parents"])
    for number, item in enumerate(metadata["steps"], 1):
        parents.append({"role": f"packet-step-{number}", "manifest_sha256": item["manifest_sha256"],
            "result_sha256": item["result_sha256"], "target_sha256": sha(canonical(item["result"]["target"])),
            "state_head": item["manifest"]["state_head"]})
    return seal({"schema": SCHEMA + ".start", "rank": START_RANK, "generation": START_GENERATION,
        "state_head": START_HEAD, "lambda_sha256": START_LAMBDA, "target_remainder_sha256": START_TARGET,
        "parent_layout": state["parent_layout"], "packet_parent_layout": packet_layout(metadata),
        "accepted_target_derivation_parents": parents})


def expected_owner(state: dict[str, Any], tables: list[Any]) -> dict[str, Any]:
    old = state["accepted_packet"]["owner"]
    same(old, FIXED.expected_owner(state, tables), "old_owner_actual_parent_join")
    return seal({"schema": SCHEMA + ".owner", **{k: v for k, v in old.items() if k not in ("schema", "sha256", "scope")},
        "scope": SCOPE, "accepted_packet_owner_sha256": PACKET_FILES["output/owner.json"][1],
        "accepted_packet_manifest_sha256": PACKET_FILES["output/packet/manifest.json"][1]})


def producer_source_receipt() -> dict[str, Any]:
    directory = Path(__file__).resolve().parent
    modules = {**FIXED.PRODUCER_LINEAGE, "d972_r07_fixed_root_packet_loop_v2.py":
               "e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6"}
    for name, expected in modules.items():
        item = directory / name
        require(item.is_file() and not item.is_symlink() and sha(item.read_bytes()) == expected, "producer_module_metadata")
    item = directory / "d972_r07_full_origin_refinement_v1.py"
    require(item.is_file() and not item.is_symlink(), "producer_main_source")
    return seal({"schema": SCHEMA + ".source", "producer_sha256": sha(item.read_bytes()),
        "modules": modules, "data": FIXED.DATA_PINS, "python": sys.version, "numpy": np.__version__})


def load_accepted_start(args: argparse.Namespace) -> dict[str, Any]:
    boundary("accepted_parent_metadata")
    metadata = accepted_packet_metadata(args)
    boundary("accepted_base_and_deltas")
    state = FIXED.load_start(args)
    same(metadata["start"], FIXED.expected_start(state), "accepted_fixed_start_join")
    state["accepted_packet"] = metadata
    for item in metadata["steps"]:
        instruction, packed = item["instruction"], item["payloads"]["physical-normalized.bin"]
        normalized = unpack(packed, WIDTH)
        require(normalized[instruction["lead"]] == 1 and
                all(normalized[pivot["lead"]] == 0 for pivot in state["pivots"]), "accepted_packet_triangular_row")
        state["saved_rows"].append(packed)
        state["pivots"].append({"offer": instruction["offer"], "lead": instruction["lead"],
            "physical_offset": instruction["physical_offset"], "coefficient_offset": None,
            "rolling_sha256": instruction["rolling_sha256"]})
    state["start_lambda"] = unpack(metadata["steps"][-1]["payloads"]["lambda.bin"], WIDTH)
    state["start_target"] = unpack(metadata["steps"][-1]["payloads"]["target-remainder.bin"], WIDTH)
    state["tops"] = unpack(metadata["packet_payloads"]["tops.bin"], 176 * SOURCE_WIDTH).reshape(4, 44, SOURCE_WIDTH)
    require(len(state["pivots"]) == START_RANK and
            all(state["start_target"][pivot["lead"]] == 0 for pivot in state["pivots"]), "accepted_start_rank")
    boundary("accepted_current_lambda_sweep")
    with path(args.state_root, "state/physical.bin").open("rb", buffering=1 << 20) as stream:
        for _ in range(1354):
            row = stream.read(ROW_BYTES)
            require(len(row) == ROW_BYTES and dot(state["start_lambda"], unpack(row, WIDTH)) == 0,
                    "accepted_current_lambda_base_row")
        require(stream.read(1) == b"", "accepted_base_eof")
    require(all(dot(state["start_lambda"], unpack(row, WIDTH)) == 0 for row in state["saved_rows"]) and
            dot(state["start_lambda"], state["start_target"]) == 1, "accepted_current_lambda_saved_targets")
    boundary("accepted_start_complete", rank=START_RANK)
    return state


MONOMIALS = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0),
             (1, 1, 0), (1, 0, 1), (0, 2, 0), (0, 1, 1), (0, 0, 2))
KERNEL = tuple(product(range(3), repeat=3))


def finite27_matrices() -> tuple[np.ndarray, np.ndarray]:
    """Expand (E-1)^mu and extract [u^mu]E^k in ordinary group basis."""
    expansion = np.zeros((10, 27), dtype=np.int64)
    extraction = np.zeros((27, 10), dtype=np.int64)
    for m, mu in enumerate(MONOMIALS):
        for j, k in enumerate(KERNEL):
            expand, extract = 1, 1
            for alpha, exponent in zip(mu, k):
                expand *= comb(alpha, exponent) * (-1) ** (alpha - exponent) if exponent <= alpha else 0
                extract *= comb(exponent, alpha) if alpha <= exponent else 0
            expansion[m, j], extraction[j, m] = expand % 3, extract % 3
    require(np.array_equal((expansion @ extraction) % 3, np.eye(10, dtype=np.int64)),
            "finite27_basis_roundtrip")
    return expansion, extraction


def zero_source() -> tuple[np.ndarray, ...]:
    return (np.zeros((4, 6048), dtype=np.uint8), np.zeros((4, 18144), dtype=np.uint8),
            np.zeros((4, 36288), dtype=np.uint8), np.zeros(8, dtype=np.uint8))


def source_components(source: tuple[np.ndarray, ...]) -> list[dict[str, Any]]:
    return [LEGACY.component_receipt(name, part) for name, part in zip(("d0", "d1", "d2", "aux"), source)]


def finite27_actor(context: Any, source: tuple[np.ndarray, ...], actor: int) -> tuple[np.ndarray, ...]:
    """Actual selected complete actor: affine permutation of 27 group slots.

    All degree0/1/2 components participate before any projection or subtraction.
    Translation preserves I^3, so the canonical degree<=2 lift suffices. The
    inverse Fourier factor is 1 because four equals one in F3. No call to the
    accepted polynomial forward actor is made here.
    """
    require([part.shape for part in source] == [(4, 6048), (4, 18144), (4, 36288), (8,)] and
            all(not np.any(part > 2) for part in source), "finite27_source_shape")
    expansion, extraction = finite27_matrices()
    out = zero_source()
    input0, input1, input2 = source[0].reshape(4, 6, 2, 504), source[1].reshape(4, 6, 2, 3, 504), source[2].reshape(4, 6, 2, 6, 504)
    output0, output1, output2 = out[0].reshape(4, 6, 2, 504), out[1].reshape(4, 6, 2, 3, 504), out[2].reshape(4, 6, 2, 6, 504)
    kernel_index = {k: index for index, k in enumerate(KERNEL)}
    for tag, image in enumerate(BASE.checker_actor_tags(context, actor)):
        fourier = np.concatenate((input0[:, tag, :, None, :], input1[:, tag], input2[:, tag]), axis=2).astype(np.int64)
        weights = np.array([[1 if sum(x * y for x, y in zip(context.transport[tag][label], parity)) % 2 == 0 else 2
                             for label in CHARACTERS] for parity in CHARACTERS], dtype=np.int64)
        parity_polynomials = (weights @ fourier.reshape(4, -1)).reshape(4, 2, 10, 504) % 3
        ordinary = (parity_polynomials.transpose(0, 1, 3, 2) @ expansion).transpose(0, 1, 3, 2) % 3
        acted = np.zeros_like(ordinary)
        pmap = np.asarray(context.pmap(image[0]), dtype=np.int64)
        require(sorted(pmap.tolist()) == list(range(504)), "finite27_psl_permutation")
        for e, parity in enumerate(CHARACTERS):
            moved_parity = (parity[0] ^ image[1], parity[1] ^ image[2])
            target_e = CHARACTERS.index(moved_parity)
            signs = (1 if parity[1] == 0 else -1, 1 if parity[0] == 0 else -1,
                     1 if (parity[0] ^ parity[1]) == 0 else -1)
            kmap = np.asarray([kernel_index[tuple((k[j] + signs[j] * image[3][j]) % 3 for j in range(3))]
                               for k in KERNEL], dtype=np.int64)
            acted[target_e][np.ix_(np.arange(2), kmap, pmap)] = ordinary[e]
        extracted = (acted.transpose(0, 1, 3, 2) @ extraction).transpose(0, 1, 3, 2) % 3
        final = ((weights.T @ extracted.reshape(4, -1)) % 3).reshape(4, 2, 10, 504).astype(np.uint8)
        output0[:, tag], output1[:, tag], output2[:, tag] = final[:, :, 0], final[:, :, 1:4], final[:, :, 4:]
    out[3][:] = source[3]
    return out


def load_tables(args: argparse.Namespace) -> list[dict[str, Any]]:
    tables = []
    for character in range(4):
        boundary("task712_tables", character=character)
        table = ARITH.read_task712_envelope({**BASE.TASK712_PARENT, "root": str(args.task712_root.resolve())}, character)
        for key in ("B", *ACTORS):
            BASE.check_table_transpose(table["forward"][key], table["adjoint"][key])
        table["entries"] = np.asarray(table["forward"]["B"], dtype=np.int64).reshape(-1, 3)
        tables.append(table)
    return tables


def dynamic_p1(args: argparse.Namespace, state: dict[str, Any], vectors: list[list[np.ndarray]]) -> dict[str, Any]:
    p1 = BASE.validate_p1({**state["launch"]["p1_parent"], "root": str(args.p1_root.resolve())})
    values = np.zeros((4, 5, 8059), dtype=np.uint8)
    active = [a for a in range(4) if np.any(vectors[a][0])]
    projections = []
    for group in vectors:
        result = []
        for vector in group:
            index = np.flatnonzero(vector)
            result.append((index // 4, index % 4, vector[index].astype(np.uint32)))
        projections.append(result)
    digest, offset = hashlib.sha256(), 0
    with path(args.p1_root, "degree2.cache.bin").open("rb", buffering=1 << 20) as stream:
        for begin in range(0, 8059, 256):
            count = min(256, 8059 - begin)
            raw = stream.read(count * 36288)
            require(len(raw) == count * 36288, "p1_chunk_eof")
            digest.update(raw); offset += len(raw)
            packed = np.frombuffer(raw, dtype=np.uint8).reshape(count, 36288)
            require(not np.any(packed > 80), "p1_chunk_packing")
            for a in active:
                values[a, :, begin:begin + count] = BASE.vectorized_projection_chunk(packed, a * SOURCE_BYTES, projections[a]).T
            boundary("p1_scan", rows=begin + count)
        require(stream.read(1) == b"", "p1_chunk_trailing")
    require(offset == BASE.P1_CACHE_BYTES and digest.hexdigest() == BASE.P1_CACHE_SHA256, "p1_scan_hash")
    return {"values": values, "p1": p1, "active": active}


def full_actor_values(args: argparse.Namespace, state: dict[str, Any], p1_values: np.ndarray,
                      lower: list[list[np.ndarray]], active: list[int]) -> tuple[np.ndarray, np.ndarray]:
    """One large Task554 JSON body resident at a time; all active roots folded."""
    answer = p1_values[:, 1:, :].transpose(0, 2, 1).copy()
    lower_values = np.zeros((4, 8059, 4), dtype=np.uint8)
    if not active:
        return answer, lower_values
    covectors = [lower[a][slot] for a in active for slot in range(4)]

    def reduce_value(a: int, global_row: int, slot: int, expression: Any, offset: int) -> None:
        value = int(answer[a, global_row, slot])
        for index, coefficient in expression:
            value -= coefficient * int(p1_values[a, 0, offset + index])
        answer[a, global_row, slot] = value % 3

    boundary("full_origin_prepare")
    checked = BASE.state_descriptor(state["task554"]["prepare"], -1)
    for owner, old in enumerate(checked["body"]["old_blocks"]):
        left, right = BASE.checker_old_slices(covectors, owner)
        part0, _ = BASE.checker_stream_dots(checked["root"], old["lower_basis_blob"], left,
            body_sha256=checked["body_sha256"], role=f"old-{owner}-lower")
        boundary("old_lower_stream", character=owner)
        part1, _ = BASE.checker_stream_dots(checked["root"], old["lifted_grade_blob"], right,
            body_sha256=checked["body_sha256"], role=f"old-{owner}-grade")
        combined = ((part0.astype(np.uint16) + part1.astype(np.uint16)) % 3).reshape(BASE.OLD_RANKS[owner], len(active), 4)
        for index, a in enumerate(active):
            start, stop = OLD_OFFSETS[owner], OLD_OFFSETS[owner] + BASE.OLD_RANKS[owner]
            lower_values[a, start:stop] = combined[:, index]
            answer[a, start:stop] = (answer[a, start:stop].astype(np.uint16) + combined[:, index]) % 3
            for local, row in enumerate(old["record"]["actor_transitions"]):
                for slot, expression in enumerate(row):
                    reduce_value(a, start + local, slot, expression, start)
        del part0, part1, combined, left, right, old
        boundary("old_actor_fold", character=owner)
    del checked
    for owner in range(4):
        boundary("full_origin_new_body", character=owner)
        checked = BASE.state_descriptor(state["task554"]["blocks"][owner], owner)
        body = checked["body"]
        part, _ = BASE.checker_stream_dots(checked["root"], body["basis_blob"],
            BASE.checker_new_slices(covectors, owner), body_sha256=checked["body_sha256"], role=f"new-{owner}-grade")
        part = part.reshape(BASE.NEW_RANKS[owner], len(active), 4)
        for index, a in enumerate(active):
            start, stop = NEW_OFFSETS[owner], NEW_OFFSETS[owner] + BASE.NEW_RANKS[owner]
            lower_values[a, start:stop] = part[:, index]
            answer[a, start:stop] = (answer[a, start:stop].astype(np.uint16) + part[:, index]) % 3
            for source in range(4):
                for local in range(BASE.OLD_RANKS[source]):
                    for slot in range(4):
                        origin = BASE.ORIGIN_RANGES[source][0] + 44 + 4 * local + slot
                        reduce_value(a, OLD_OFFSETS[source] + local, slot, body["origin_reductions"][origin], start)
            for local, row in enumerate(body["actor_transitions"]):
                for slot, expression in enumerate(row):
                    reduce_value(a, start + local, slot, expression, start)
        del part, body, checked
        boundary("new_actor_fold", character=owner)
    return answer, lower_values


def scan_arithmetic(args: argparse.Namespace, state: dict[str, Any], tables: list[Any],
                    context: Any, functional: np.ndarray) -> dict[str, Any]:
    vectors, lower, covector_receipts = [], [], []
    for a, table in enumerate(tables):
        boundary("fresh_roots", character=a)
        q = FIXED.pullback(table["entries"], functional)
        children = [ARITH.sparse_adjoint(table["forward"][actor], SOURCE_WIDTH, SOURCE_WIDTH, q) for actor in ACTORS]
        vectors.append([q, *children])
        if np.any(q):
            covectors, receipt = BASE.checker_actor_adjoints(context, q, a, children)
        else:
            covectors, receipt = [np.zeros(96776, dtype=np.uint8) for _ in ACTORS], None
        lower.append(covectors); covector_receipts.append(receipt)
    p1 = dynamic_p1(args, state, vectors)
    seeds = np.zeros((4, 44), dtype=np.uint8)
    for a in p1["active"]:
        for seed in range(44):
            seeds[a, seed] = dot(vectors[a][0], state["tops"][a, seed])
    actors, lower_values = full_actor_values(args, state, p1["values"], lower, p1["active"])
    require(seeds.shape == (4, 44) and actors.shape == (4, 8059, 4), "full_arrays_shape")
    return {"vectors": vectors, "lower": lower, "covector_receipts": covector_receipts,
            "p1": p1, "seeds": seeds, "actors": actors, "lower_values": lower_values}


def canonical_index(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    """One authenticated instruction pass; selected consumers retain references."""
    p1 = BASE.validate_p1({**state["launch"]["p1_parent"], "root": str(args.p1_root.resolve())})
    references, previous, offset = [], "0" * 64, 0
    digest = hashlib.sha256()
    with path(args.p1_root, "instructions.jsonl").open("rb", buffering=1 << 20) as stream:
        for node in range(8059):
            line = stream.readline()
            require(line.endswith(b"\n"), "canonical_instruction_eof")
            item = json_bytes(line)
            digest.update(line)
            require(item["node"] == node and item["offset"] == node * 36288 and item["length"] == 36288 and
                    item["predecessor"] == previous and item["row_receipt"]["offset"] == node * 36288 and
                    item["row_receipt"]["length"] == 36288 and item["ancestry_sha256"] ==
                    sha(bytes.fromhex(previous) + canonical({k: v for k, v in item.items() if k != "ancestry_sha256"})),
                    "canonical_instruction_chain")
            if item["origin"]["kind"] == "actor":
                require(item["origin"]["letter"] in ACTORS and item["literal_input_sha256"] ==
                        sha(canonical({"kind": "actor", "letter": item["origin"]["letter"], "actor_order": list(ACTORS)})),
                        "accepted_actor_literal_orientation_receipt")
            references.append({"node": node, "instruction_offset": offset, "instruction_length": len(line),
                "instruction_sha256": sha(line), "ancestry_sha256": item["ancestry_sha256"], "predecessor": previous,
                "p1_sha256": item["p1_sha256"], "row_sha256": item["row_receipt"]["sha256"],
                "origin_sha256": sha(canonical(item["origin"])), "reductions_sha256": sha(canonical(item["reductions"])),
                "scale": item["scale"], "literal_input_sha256": item["literal_input_sha256"]})
            previous, offset = item["ancestry_sha256"], offset + len(line)
            if (node + 1) % 2048 == 0:
                boundary("canonical_index", rows=node + 1)
        require(stream.read(1) == b"", "canonical_instruction_trailing")
    require(offset == BASE.P1_INSTRUCTION_BYTES and digest.hexdigest() == BASE.P1_INSTRUCTION_SHA256 and
            previous == p1["manifest"]["ancestry_sha256"], "canonical_instruction_identity")
    return seal({"schema": SCHEMA + ".canonical-p1-index", "p1_manifest_sha256": BASE.P1_MANIFEST_SHA256,
        "instruction_sha256": BASE.P1_INSTRUCTION_SHA256, "cache_sha256": BASE.P1_CACHE_SHA256,
        "rows": 8059, "references": references})


def first_hit(seeds: np.ndarray, actors: np.ndarray) -> dict[str, Any] | None:
    require(seeds.shape == (4, 44) and actors.shape == (4, 8059, 4) and
            not np.any(seeds > 2) and not np.any(actors > 2), "selection_arrays")
    for a in range(4):
        for seed, value in enumerate(seeds[a]):
            if value:
                return {"character": a, "origin_id": seed, "index": a * ORIGINS_PER_CHARACTER + seed,
                        "origin_kind": "seed", "scalar": int(value), "seed": seed}
        for flat in np.flatnonzero(actors[a].reshape(-1)):
            basis, slot = divmod(int(flat), 4)
            origin = 44 + int(flat)
            return {"character": a, "origin_id": origin, "index": a * ORIGINS_PER_CHARACTER + origin,
                    "origin_kind": "actor", "scalar": int(actors[a, basis, slot]),
                    "basis_i": basis, "actor": ACTORS[slot], "actor_slot": slot}
    return None


def scan_payloads(arithmetic: dict[str, Any], tables: list[Any], functional: np.ndarray,
                  number: int, current_head: str, owner_sha: str, index_sha: str) -> tuple[dict[str, bytes], dict[str, Any]]:
    payloads, root_records = {}, []
    for a in range(4):
        vectors = arithmetic["vectors"][a]
        payloads[f"root-c{a}.bin"] = pack(vectors[0])
        payloads[f"children-c{a}.bin"] = b"".join(pack(child) for child in vectors[1:])
        for name, values in (("seeds", arithmetic["seeds"][a]), ("actors", arithmetic["actors"][a]),
                             ("p1", arithmetic["p1"]["values"][a]), ("actor-lower", arithmetic["lower_values"][a])):
            payloads[f"{name}-c{a}.u8"] = values.tobytes(order="C")
        root_records.append({"character": a, "support": int(np.count_nonzero(vectors[0])),
            "packed_sha256": sha(pack(vectors[0])), "B_adj_identity": tables[a]["identity"]["adjoint:B"],
            "children": [{"actor": actor, "support": int(np.count_nonzero(vectors[slot + 1])),
                          "packed_sha256": sha(pack(vectors[slot + 1]))} for slot, actor in enumerate(ACTORS)],
            "seed_values_sha256": sha(payloads[f"seeds-c{a}.u8"]),
            "actor_values_sha256": sha(payloads[f"actors-c{a}.u8"]),
            "p1_values_sha256": sha(payloads[f"p1-c{a}.u8"]),
            "actor_lower_values_sha256": sha(payloads[f"actor-lower-c{a}.u8"])})
    active = arithmetic["p1"]["active"]
    result = seal({"schema": SCHEMA + ".scan", "scan": number, "owner_sha256": owner_sha,
        "canonical_index_sha256": index_sha, "rank": START_RANK + number, "generation": START_GENERATION + number,
        "state_head": current_head, "lambda_sha256": sha(pack(functional)), "roots": root_records,
        "first_hit": first_hit(arithmetic["seeds"], arithmetic["actors"]), "declared_pair_count": 129120,
        "informative_pair_count": len(active) * ORIGINS_PER_CHARACTER,
        "structural_zero_pair_count": (4 - len(active)) * ORIGINS_PER_CHARACTER,
        "nonzero_pair_count": int(np.count_nonzero(arithmetic["seeds"]) + np.count_nonzero(arithmetic["actors"])),
        "active_characters": active,
        "p1_pass": {"cache_passes": 1, "cache_rows": 8059, "cache_sha256": BASE.P1_CACHE_SHA256,
            "instruction_sha256": BASE.P1_INSTRUCTION_SHA256, "active_pairings": 5 * len(active), "chunk_rows": 256},
        "lower_pass": {"body_reads": 5 * len(active), "blob_passes": 12 * len(active), "maximum_live_bodies": 1},
        "formula_id": BASE.V541_FORMULA_ID, "candidate": True, "cross_checked": False, "verified": False})
    payloads["result.json"] = canonical(result)
    manifest = seal({"schema": SCHEMA + ".scan-manifest", "scan": number, "owner_sha256": owner_sha,
        "canonical_index_sha256": index_sha, "rank": START_RANK + number, "generation": START_GENERATION + number,
        "state_head": current_head, "lambda_sha256": sha(pack(functional)),
        "files": [file_receipt(name, raw) for name, raw in sorted(payloads.items())]})
    return payloads, manifest


def actor_relation(state: dict[str, Any], selected: dict[str, Any]) -> dict[str, Any]:
    basis, actor, slot = selected["basis_i"], selected["actor"], selected["actor_slot"]
    require(0 <= basis < 8059 and actor == ACTORS[slot], "actor_relation_selection")
    events = []

    def append(expression: Any, role: str, source: int, target: int | None, origin: int | None,
               offset: int, bound: int, body_sha: str) -> None:
        require(isinstance(expression, list), "actred_expression")
        for ordinal, term in enumerate(expression):
            require(isinstance(term, list) and len(term) == 2 and type(term[0]) is int and
                    type(term[1]) is int and 0 <= term[0] < bound and term[1] in (1, 2), "actred_term")
            node, coefficient = offset + term[0], term[1]
            events.append({"event_id": len(events), "node": node, "body_role": role,
                "task554_body_sha256": body_sha, "source_character": source, "target_character": target,
                "origin_id": origin, "term_ordinal": ordinal, "local_index": term[0],
                "global_index": node, "coefficient": coefficient})

    if basis < 2014:
        owner = max(a for a, begin in enumerate(OLD_OFFSETS) if begin <= basis)
        local = basis - OLD_OFFSETS[owner]
        origin = BASE.ORIGIN_RANGES[owner][0] + 44 + 4 * local + slot
        checked = BASE.state_descriptor(state["task554"]["prepare"], -1)
        append(checked["body"]["old_blocks"][owner]["record"]["actor_transitions"][local][slot],
               "prepare-old", owner, None, origin, OLD_OFFSETS[owner], BASE.OLD_RANKS[owner], checked["body_sha256"])
        del checked
        boundary("selected_actred_prepare", basis_i=basis)
        for target in range(4):
            checked = BASE.state_descriptor(state["task554"]["blocks"][target], target)
            append(checked["body"]["origin_reductions"][origin], "new-block", owner, target, origin,
                   NEW_OFFSETS[target], BASE.NEW_RANKS[target], checked["body_sha256"])
            del checked
            boundary("selected_actred_block", character=target)
    else:
        owner = max(a for a, begin in enumerate(NEW_OFFSETS) if begin <= basis)
        local = basis - NEW_OFFSETS[owner]
        checked = BASE.state_descriptor(state["task554"]["blocks"][owner], owner)
        append(checked["body"]["actor_transitions"][local][slot], "new-block", owner, owner, None,
               NEW_OFFSETS[owner], BASE.NEW_RANKS[owner], checked["body_sha256"])
        del checked
        boundary("selected_actred_block", character=owner)
    previous = "0" * 64
    for event in events:
        previous = sha(bytes.fromhex(previous) + canonical(event))
        event["rolling_sha256"] = previous
    coefficients: dict[int, int] = {}
    for event in events:
        node = event["global_index"]
        coefficients[node] = (coefficients.get(node, 0) + event["coefficient"]) % 3
    return seal({"schema": SCHEMA + ".actor-relation", "basis_i": basis, "actor": actor, "actor_slot": slot,
        "raw_events": events, "raw_event_count": len(events), "raw_event_final_head": previous,
        "final_coefficients": [[node, coefficient] for node, coefficient in sorted(coefficients.items()) if coefficient],
        "referenced_nodes": sorted(coefficients), "cancelled_nodes": sorted(node for node, coefficient in coefficients.items() if not coefficient)})


def source_lift(args: argparse.Namespace, streams: list[Any], cache: Any, reference: dict[str, Any]) -> tuple[tuple[np.ndarray, ...], list[dict[str, Any]]]:
    node = reference["node"]
    source = zero_source()
    top = LEGACY.blob_row(cache, node, 145152)
    require(sha(top) == reference["row_sha256"], "selected_canonical_top_hash")
    source[2][:] = unpack(top, 145152).reshape(4, SOURCE_WIDTH)
    components = [{"role": "p1-degree2", "bytes": len(top), "sha256": sha(top)}]
    if node < 2014:
        owner = max(a for a, begin in enumerate(OLD_OFFSETS) if begin <= node)
        local = node - OLD_OFFSETS[owner]
        raw_lower, raw_grade = LEGACY.blob_row(streams[2 * owner], local, 6056), LEGACY.blob_row(streams[2 * owner + 1], local, 72576)
        lower = unpack(raw_lower, 6056)
        source[0][owner], source[3][:] = lower[:6048], lower[6048:]
        source[1][:] = unpack(raw_grade, 72576).reshape(4, 18144)
        components.extend(({"role": "old-lower", "bytes": len(raw_lower), "sha256": sha(raw_lower)},
                           {"role": "old-grade", "bytes": len(raw_grade), "sha256": sha(raw_grade)}))
    else:
        owner = max(a for a, begin in enumerate(NEW_OFFSETS) if begin <= node)
        raw_grade = LEGACY.blob_row(streams[8 + owner], node - NEW_OFFSETS[owner], 18144)
        source[1][owner] = unpack(raw_grade, 18144)
        components.append({"role": "new-grade", "bytes": len(raw_grade), "sha256": sha(raw_grade)})
    return source, components


def actor_literal(selected: dict[str, Any], relation: dict[str, Any], index: dict[str, Any],
                  table: dict[str, Any], d: np.ndarray) -> dict[str, Any]:
    a, basis = selected["character"], selected["basis_i"]
    return {"defect_operation": "ordered-product", "actor_conjugation": "t*W*t^-1", "basis_i": basis,
        "actor": selected["actor"], "actor_input_p1_sha256": index["references"][basis]["p1_sha256"],
        "relation_sha256": relation["sha256"], "canonical_index_sha256": sha(canonical(index)),
        "p1_factor_order": "event_id-ascending", "p1_exponent_rule": "(3-coefficient)%3",
        "literal_coefficient_collection": False, "character": a,
        "projector_receipt_sha256": sha(canonical(FIXED.projector_records()[a])),
        "actor_path": [], "forward_B": table["identity"]["forward:B"], "source_d_sha256": sha(pack(d)),
        "parent_state_ancestry_premise": True, "normalized_exponent_pair": "NOT_REPLAYED",
        "eleven_slot_replay": False, "full_A0_witness": False, "grade2_positive_terminal_complete": False}


def materialize_actor(args: argparse.Namespace, state: dict[str, Any], tables: list[Any], context: Any,
                      index: dict[str, Any], selected: dict[str, Any], arithmetic: dict[str, Any]) -> dict[str, Any]:
    a, basis, actor, slot = selected["character"], selected["basis_i"], selected["actor"], selected["actor_slot"]
    boundary("selected_complete_actor", basis_i=basis, actor=actor, character=a)
    relation = actor_relation(state, selected)
    nodes = sorted(set(relation["referenced_nodes"]) | {basis})
    coefficients = dict(relation["final_coefficients"])
    descriptors = [(args.prepare_root, descriptor) for owner in range(4) for descriptor in BASE.OLD_BLOB_PINS[owner]]
    descriptors += [(args.block_root[owner], BASE.NEW_BLOB_PINS[owner]) for owner in range(4)]
    lift_components = []
    with ExitStack() as stack:
        streams = [stack.enter_context(path(root, descriptor["file"]).open("rb")) for root, descriptor in descriptors]
        cache = stack.enter_context(path(args.p1_root, "degree2.cache.bin").open("rb"))
        source, input_lifts = source_lift(args, streams, cache, index["references"][basis])
        full_actor = finite27_actor(context, source, actor)
        homogeneous = np.stack([FIXED.pushforward(np.asarray(tables[c]["forward"][actor], dtype=np.int64), source[2][c], SOURCE_WIDTH)
                                for c in range(4)])
        lower_to_top = ((full_actor[2].astype(np.int16) - homogeneous.astype(np.int16)) % 3).astype(np.uint8)
        q = arithmetic["vectors"][a][0]
        homogeneous_value, mixed_value = dot(q, homogeneous[a]), dot(q, lower_to_top[a])
        direct_value = dot(q, full_actor[2][a])
        require(homogeneous_value == int(arithmetic["p1"]["values"][a, slot + 1, basis]) and
                mixed_value == int(arithmetic["lower_values"][a, basis, slot]) and
                direct_value == (homogeneous_value + mixed_value) % 3, "finite27_full_actor_adjoint_anchor")
        defect = tuple(part.copy() for part in full_actor)
        correction = 0
        for count, node in enumerate(nodes):
            lift, components = (source, input_lifts) if node == basis else source_lift(args, streams, cache, index["references"][node])
            lift_components.append({"node": node, "components": components})
            coefficient = coefficients.get(node, 0)
            if coefficient:
                correction = (correction + coefficient * dot(q, lift[2][a])) % 3
                for destination, component in zip(defect, lift):
                    subtract(destination, component, coefficient)
            if node != basis:
                del lift
            if (count + 1) % 128 == 0:
                boundary("selected_complete_p1_subtraction", references=count + 1)
    LEGACY.require_lower_zero(defect)
    d = defect[2][a].copy()
    require(dot(q, d) == selected["scalar"] == (direct_value - correction) % 3,
            "selected_full_defect_scalar")
    reference = index["references"][basis]
    receipt = seal({"schema": SCHEMA + ".materialization", "selection": selected,
        "mode": "complete-filtered-actor", "source_d_sha256": sha(pack(d)),
        "source_full_top_sha256": sha(pack(defect[2])), "lower_zero": True, "components": source_components(defect),
        "input": {"basis_i": basis, "p1_reference": reference, "components": source_components(source),
            "full_actor_components": source_components(full_actor), "homogeneous_top_sha256": sha(pack(homogeneous)),
            "lower_to_top_sha256": sha(pack(lower_to_top))}, "relation": relation,
        "p1_references": [index["references"][node] for node in nodes], "lift_components": lift_components,
        "direct_pairing": {"homogeneous": homogeneous_value, "lower_to_top": mixed_value,
            "full_direct": direct_value, "correction": correction, "defect": selected["scalar"]},
        "literal": actor_literal(selected, relation, index, tables[a], d)})
    anchor = {"basis_i": basis, "actor": actor, "character": a, "method": "finite27-ordinary-group-coefficients",
        "complete_actual_source": True, "source_components": source_components(source),
        "acted_components": source_components(full_actor), "mixed_top_support": int(np.count_nonzero(lower_to_top)),
        "homogeneous_scalar": homogeneous_value, "mixed_scalar": mixed_value, "actual_complete_scalar": direct_value,
        "producer_polynomial_forward_called": False, "accepted_group_index_inputs": True,
        "new_full_word_replay": False, "cross_checked": False, "verified": False}
    return {"d": d, "full_top": defect[2], "receipt": receipt, "anchor": anchor}


def materialize_seed(state: dict[str, Any], tables: list[Any], selected: dict[str, Any]) -> dict[str, Any]:
    seed, a = selected["seed"], selected["character"]
    accepted = state["accepted_packet"]["packet"]
    relation = accepted["relations.json"]["seeds"][seed]
    nodes = sorted({event["global_index"] for event in relation["raw_events"]})
    old_roots = {item["node"]: item for item in accepted["p1-roots.json"]["roots"]}
    top, d = state["tops"][:, seed], state["tops"][a, seed]
    packet = {"relation_certificate": accepted["relations.json"], "roots_certificate": accepted["p1-roots.json"],
        "compact_words": [item["compact_word"] for item in accepted["receipts.json"]["raw_seeds"]],
        "receipt_certificate": accepted["receipts.json"], "tops": state["tops"].transpose(1, 0, 2)}
    receipt = seal({"schema": SCHEMA + ".materialization", "selection": selected,
        "mode": "immutable-seed-packet", "source_d_sha256": sha(pack(d)), "source_full_top_sha256": sha(pack(top)),
        "lower_zero": True, "components": accepted["receipts.json"]["seeds"][seed]["reduced_components"], "input": None,
        "relation": relation, "p1_references": [{k: v for k, v in old_roots[node].items() if k != "lift_components"} for node in nodes],
        "lift_components": [{"node": node, "components": old_roots[node]["lift_components"]} for node in nodes],
        "direct_pairing": None, "literal": FIXED.literal_certificate(packet, tables[a], selected)})
    return {"d": d, "full_top": top, "receipt": receipt, "anchor": None}


def rho2_derivation(start: dict[str, Any], steps: int) -> dict[str, Any]:
    result = FIXED.rho2_derivation(start, steps)
    result["accepted_identity_convention"]["packet_steps"] = \
        "parent_remainder - child_remainder = target.scalar * accepted_packet_normalized_row"
    return result


def rebuild_step(args: argparse.Namespace, state: dict[str, Any], tables: list[Any], context: Any,
                 index: dict[str, Any], start: dict[str, Any], owner_sha: str, number: int,
                 previous_manifest: str | None, current_head: str, functional: np.ndarray,
                 target: np.ndarray, pivots: list[Any], row_reader: Callable[[int], bytes],
                 scan: dict[str, Any], scan_sha: str, arithmetic: dict[str, Any]) -> dict[str, Any]:
    selected = scan["first_hit"]
    require(selected is not None, "append_without_nonzero_origin")
    source = materialize_actor(args, state, tables, context, index, selected, arithmetic) if selected["origin_kind"] == "actor" \
        else materialize_seed(state, tables, selected)
    scalar, a = selected["scalar"], selected["character"]
    raw = FIXED.pushforward(tables[a]["entries"], source["d"])
    require(dot(functional, raw) == dot(arithmetic["vectors"][a][0], source["d"]) == scalar,
            "physical_full_source_scalar")
    boundary("physical_insertion", step=number)
    remainder, reductions = LEGACY.reduce_dense(raw, pivots, row_reader)
    normalized, lead, scale = LEGACY.normalize(remainder)
    require(lead not in {pivot["lead"] for pivot in pivots} and dot(functional, remainder) == scalar and
            dot(functional, normalized) == scalar * scale % 3, "new_origin_rank_gate")
    updated, target_scalar = LEGACY.next_target(target, normalized, lead, [pivot["lead"] for pivot in pivots])
    old_rank, old_generation = START_RANK + number - 1, START_GENERATION + number - 1
    require(len(pivots) == old_rank, "new_prefix_rank")
    packet_sha, index_sha = PACKET_FILES["output/packet/manifest.json"][1], sha(canonical(index))
    payloads = {"source-d.bin": pack(source["d"]), "source-full-top.bin": pack(source["full_top"]),
        "materialization.json": canonical(source["receipt"]), "physical-raw.bin": pack(raw),
        "physical-remainder.bin": pack(remainder), "physical-normalized.bin": pack(normalized),
        "target-remainder.bin": pack(updated)}
    material_sha = sha(payloads["materialization.json"])
    instruction_body = {"schema": SCHEMA + ".instruction", "step": number, "predecessor": current_head,
        "offer": old_generation, "generation": old_generation + 1, "rank": old_rank + 1,
        "lead": lead, "sigma": scale, "physical_offset": old_rank * ROW_BYTES, "selected": selected,
        "packet_manifest_sha256": packet_sha, "scan_manifest_sha256": scan_sha,
        "materialization_sha256": material_sha, "source_d_sha256": sha(payloads["source-d.bin"]),
        "canonical_index_sha256": index_sha, "physical_reductions": reductions,
        "physical_sha256": sha(payloads["physical-normalized.bin"]), "target_scalar": target_scalar,
        "target_remainder_sha256": sha(payloads["target-remainder.bin"])}
    new_head = sha(bytes.fromhex(current_head) + canonical(instruction_body))
    instruction = {**instruction_body, "rolling_sha256": new_head}
    kind, separator, next_functional = "Member", None, None
    if np.any(updated):
        kind = "Separator"
        boundary("fresh_separator", step=number)
        reverse = LEGACY.next_separator(updated, pivots, normalized, lead, row_reader, old_generation)
        next_functional = reverse["lambda"]
        require(dot(next_functional, target) == dot(next_functional, updated) == 1, "new_separator_both_targets")
        payloads["lambda.bin"] = pack(next_functional)
        separator = {"free_coordinate": reverse["free_coordinate"], "free_value": reverse["free_value"],
            "lambda_sha256": sha(payloads["lambda.bin"]),
            "direct_pairing": {"rows": old_rank + 1, "row_pairings_sha256": sha(b"\0" * (old_rank + 1)),
                "lambda_pivots": 0, "lambda_parent_remainder": 1, "lambda_new_remainder": 1},
            "lambda_rho2": rho2_derivation(start, number)}
    result = seal({"schema": SCHEMA + ".step-result", "step": number, "kind": kind,
        "owner_sha256": owner_sha, "packet_manifest_sha256": packet_sha,
        "parent_state_head": current_head, "state_head": new_head,
        "rank_before": old_rank, "rank_after": old_rank + 1,
        "generation_before": old_generation, "generation_after": old_generation + 1,
        "selection": selected, "scan_manifest_sha256": scan_sha, "materialization_sha256": material_sha,
        "pairings": {"q_d": scalar, "lambda_G": scalar},
        "pivot": {"lead": lead, "scale": scale, "reductions": reductions,
                  "normalized_sha256": sha(payloads["physical-normalized.bin"])},
        "target": {"parent_remainder_sha256": sha(pack(target)), "remainder_sha256": sha(payloads["target-remainder.bin"]),
                   "scalar": target_scalar}, "separator": separator, "literal": source["receipt"]["literal"],
        "candidate": True, "cross_checked": False, "verified": False})
    payloads.update({"instruction.json": canonical(instruction), "result.json": canonical(result)})
    manifest = seal({"schema": SCHEMA + ".step-manifest", "step": number, "owner_sha256": owner_sha,
        "packet_manifest_sha256": packet_sha, "predecessor_step_manifest_sha256": previous_manifest,
        "parent_state_head": current_head, "state_head": new_head, "rank": old_rank + 1,
        "generation": old_generation + 1, "kind": kind, "scan_manifest_sha256": scan_sha,
        "files": [file_receipt(name, raw) for name, raw in sorted(payloads.items())]})
    boundary("whole_step_replayed", step=number, kind=kind, rank=old_rank + 1)
    return {"payloads": payloads, "manifest": manifest, "head": new_head, "target": updated,
        "lambda": next_functional, "kind": kind, "anchor": source["anchor"],
        "normalized": payloads["physical-normalized.bin"],
        "pivot": {"offer": old_generation, "lead": lead, "physical_offset": old_rank * ROW_BYTES,
                  "coefficient_offset": None, "rolling_sha256": new_head}}


def compare_directory(root: Path, payloads: dict[str, bytes], manifest: dict[str, Any]) -> str:
    return FIXED.compare_directory(root, payloads, manifest)


def audit_prefix_directory(root: Path, first: int, last: int) -> None:
    require(root.is_dir() and not root.is_symlink(), "prefix_directory")
    for item in root.iterdir():
        require(item.is_dir() and not item.is_symlink(), "prefix_child_kind")
        if re.fullmatch(r"\.(?:pending|orphan)-[0-9]{6}-[A-Za-z0-9-]+", item.name):
            continue
        require(re.fullmatch(r"[0-9]{6}", item.name) is not None and int(item.name) >= first, "prefix_child_name")
    for number in range(first, last + 1):
        require((root / f"{number:06d}").is_dir(), "missing_committed_prefix")


def terminal_for_state(kind: str, target: np.ndarray, scan: dict[str, Any] | None, declared: str) -> str:
    if kind == "Member":
        require(not np.any(target) and scan is None, "member_terminal_target")
        return "MEMBER_CANDIDATE"
    require(kind == "Separator" and np.any(target), "separator_terminal_target")
    if scan is None:
        require(declared == "UNKNOWN_RESOURCE", "missing_scan_terminal")
        return declared
    if scan["first_hit"] is None:
        return "ROOT_ORIGINS_ZERO"
    require(declared in ("UNKNOWN_CAP", "UNKNOWN_RESOURCE"), "nonzero_origin_terminal")
    return declared


def head_record(source: dict[str, Any], owner_sha: str, start_sha: str, index_sha: str,
                completed: int, previous_manifest: str | None, scan_sha: str | None,
                state_head: str, kind: str) -> dict[str, Any]:
    return seal({"schema": SCHEMA + ".head", "owner_sha256": owner_sha,
        "producer_sha256": source["producer_sha256"], "source_sha256": sha(canonical(source)),
        "start_sha256": start_sha, "canonical_index_sha256": index_sha,
        "packet_manifest_sha256": PACKET_FILES["output/packet/manifest.json"][1],
        "completed_steps": completed, "step_manifest_sha256": previous_manifest,
        "current_scan_manifest_sha256": scan_sha, "rank": START_RANK + completed,
        "generation": START_GENERATION + completed, "state_head": state_head, "kind": kind})


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    global REPLAYED_STEPS, REPLAYED_SCANS
    root = args.candidate_root
    require(root.is_dir() and not root.is_symlink(), "candidate_root")
    expected_names = {"owner.json", "start.json", "source.json", "canonical-index.json", "HEAD", "result.json", "steps", "scans"}
    actual_names = set()
    for item in root.iterdir():
        require(not item.is_symlink(), "candidate_symlink")
        if item.name == "resource-stop.json":
            require(item.is_file(), "resource_diagnostic_kind")
        elif re.fullmatch(r"\.(?:HEAD|owner\.json|start\.json|source\.json|canonical-index\.json|result\.json|resource-stop\.json)\.pending-[A-Za-z0-9-]+", item.name):
            require(item.is_file(), "atomic_diagnostic_kind")
        elif re.fullmatch(r"\.packet-pending-[A-Za-z0-9-]+", item.name):
            require(item.is_dir(), "packet_diagnostic_kind")
        else:
            actual_names.add(item.name)
    require(actual_names == expected_names, "candidate_top_roster")
    candidate_head = read_json(root, "HEAD", 1 << 20)
    check_seal(candidate_head)
    completed = candidate_head.get("completed_steps")
    require(type(completed) is int and 0 <= completed <= MAX_APPENDS, "bounded_complete_prefix")
    source = producer_source_receipt()
    same(read_json(root, "source.json"), source, "source_runtime_freeze")
    state = load_accepted_start(args)
    tables = load_tables(args)
    index = canonical_index(args, state)
    same(read_json(root, "canonical-index.json"), index, "canonical_p1_metadata_index")
    owner, start = expected_owner(state, tables), expected_start(state)
    same(read_json(root, "owner.json"), owner, "registered_owner")
    same(read_json(root, "start.json"), start, "registered_start")
    owner_sha, start_sha, index_sha = sha(canonical(owner)), sha(canonical(start)), sha(canonical(index))
    require(candidate_head["owner_sha256"] == owner_sha and candidate_head["start_sha256"] == start_sha and
            candidate_head["canonical_index_sha256"] == index_sha and candidate_head["source_sha256"] == sha(canonical(source)),
            "head_immutable_metadata")
    context, _ = BASE.checker_source_context()
    current_head, previous_manifest, kind = START_HEAD, None, "Separator"
    target, functional = state["start_target"], state["start_lambda"]
    pivots, rows = list(state["pivots"]), list(state["saved_rows"])
    anchors, scan_io = [], []
    cached_scan = candidate_head["current_scan_manifest_sha256"]
    require(cached_scan is None or isinstance(cached_scan, str) and re.fullmatch(r"[0-9a-f]{64}", cached_scan), "cached_scan_reference")
    audit_prefix_directory(root / "steps", 1, completed)
    audit_prefix_directory(root / "scans", 0, completed if cached_scan is not None else completed - 1)

    def replay_scan(number: int) -> tuple[dict[str, Any], str, dict[str, Any]]:
        global REPLAYED_SCANS
        require(functional is not None, "scan_without_separator")
        boundary("new_full_scan_replay", scan=number)
        arithmetic = scan_arithmetic(args, state, tables, context, functional)
        payloads, manifest = scan_payloads(arithmetic, tables, functional, number, current_head, owner_sha, index_sha)
        manifest_sha = compare_directory(root / "scans" / f"{number:06d}", payloads, manifest)
        scan = json_bytes(payloads["result.json"])
        REPLAYED_SCANS += 1
        active = arithmetic["p1"]["active"]
        scan_io.append({"scan": number, "active_characters": active, "p1_cache_passes": 1,
            "task554_body_reads": 5 if active else 0, "lower_blob_passes": 12 if active else 0,
            "maximum_live_bodies": 1, "stored_origin_scalars": 129120,
            "actually_paired_origins": len(active) * ORIGINS_PER_CHARACTER,
            "structural_zero_origins": (4 - len(active)) * ORIGINS_PER_CHARACTER,
            "producer_declared_lower_pass": scan["lower_pass"]})
        return scan, manifest_sha, arithmetic

    with path(args.state_root, "state/physical.bin").open("rb", buffering=1 << 20) as stream:
        def read_pivot(number: int) -> bytes:
            require(0 <= number < len(pivots), "physical_pivot_index")
            return LEGACY.blob_row(stream, number, WIDTH) if number < 1354 else rows[number - 1354]
        for number in range(1, completed + 1):
            require(kind == "Separator" and functional is not None, "prefix_after_member")
            scan, scan_sha, arithmetic = replay_scan(number - 1)
            rebuilt = rebuild_step(args, state, tables, context, index, start, owner_sha, number, previous_manifest,
                current_head, functional, target, pivots, read_pivot, scan, scan_sha, arithmetic)
            previous_manifest = compare_directory(root / "steps" / f"{number:06d}", rebuilt["payloads"], rebuilt["manifest"])
            current_head, target, functional, kind = rebuilt["head"], rebuilt["target"], rebuilt["lambda"], rebuilt["kind"]
            pivots.append(rebuilt["pivot"]); rows.append(rebuilt["normalized"])
            if rebuilt["anchor"] is not None:
                anchors.append({"step": number, **rebuilt["anchor"]})
            REPLAYED_STEPS = number
            del arithmetic, rebuilt
    scan, scan_sha = None, None
    if cached_scan is not None:
        require(kind == "Separator", "member_cannot_have_scan")
        scan, scan_sha, arithmetic = replay_scan(completed)
        require(scan_sha == cached_scan, "head_cached_scan_join")
        del arithmetic
    expected_head = head_record(source, owner_sha, start_sha, index_sha, completed, previous_manifest,
                                scan_sha, current_head, kind)
    same(candidate_head, expected_head, "entire_new_prefix_head")
    actual_result = read_json(root, "result.json")
    terminal = terminal_for_state(kind, target, scan, actual_result.get("terminal"))
    result = seal({"schema": SCHEMA + ".result", "status": "PASS", "terminal": terminal,
        "head_sha256": sha(canonical(expected_head)), "packet_manifest_sha256": PACKET_FILES["output/packet/manifest.json"][1],
        "owner_sha256": owner_sha, "completed_steps": completed, "rank": START_RANK + completed,
        "generation": START_GENERATION + completed, "state_head": current_head, "scan_manifest_sha256": scan_sha,
        "scan": scan, "lambda_rho2": None if kind == "Member" else rho2_derivation(start, completed),
        "scope": SCOPE, "claims": CLAIMS, "candidate": True, "cross_checked": False, "verified": False})
    same(actual_result, result, "terminal_complete_scan_join")
    boundary("terminal", status="PASS", terminal=terminal, steps=completed, scans=REPLAYED_SCANS)
    return {"schema": SCHEMA + ".checker-result", "status": "PASS", "terminal": terminal,
        "completed_steps": completed, "prefix_steps_replayed": REPLAYED_STEPS, "complete_scans_replayed": REPLAYED_SCANS,
        "rank": START_RANK + completed, "generation": START_GENERATION + completed, "state_head": current_head,
        "head_sha256": sha(canonical(expected_head)), "result_sha256": sha(canonical(result)),
        "owner_sha256": owner_sha, "canonical_index_sha256": index_sha,
        "accepted_packet_artifact": PACKET_ARTIFACT, "packet_manifest_sha256": PACKET_FILES["output/packet/manifest.json"][1],
        "accepted_packet_arithmetic_premise": True, "old_packet_rebuilt": False, "old_packet_steps_numerically_replayed": 0,
        "initial_current_lambda_row_pairings": 1359, "all_new_scalar_arrays_compared": True,
        "scan_io": scan_io, "finite27_actor_anchors": anchors, "complete_actor_evaluations": len(anchors),
        "lower_coordinates_per_selected_actor": 96776, "lambda_rho2": result["lambda_rho2"],
        "checker_lineage": {**FIXED.LINEAGE, "check_d972_r07_fixed_root_packet_loop_v2.py": FIXED_CHECKER_SHA},
        "source_data_pins": FIXED.DATA_PINS, "claims": CLAIMS,
        "candidate": True, "cross_checked": False, "verified": False}


def reject_test(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError("full_origin_checker:mutation_accepted:" + label)


def parent_layout_selftest(args: argparse.Namespace) -> dict[str, Any]:
    old = FIXED.parent_layout_selftest(args)
    metadata = accepted_packet_metadata(args)
    steps = metadata["steps"]
    first = steps[0]
    mutations = [
        ("packet-instruction-generic-seal", metadata["head"],
         [{**first, "instruction": {**first["instruction"], "sha256": "0" * 64}}, *steps[1:]]),
        ("packet-target-generic-seal", metadata["head"],
         [{**first, "result": {**first["result"], "target": {**first["result"]["target"], "sha256": "0" * 64}}}, *steps[1:]]),
        ("packet-target-parent", metadata["head"],
         [{**first, "result": {**first["result"], "target": {**first["result"]["target"], "parent_remainder_sha256": "0" * 64}}}, *steps[1:]]),
        ("packet-step-chain", metadata["head"],
         [{**first, "manifest": {**first["manifest"], "parent_state_head": "0" * 64}}, *steps[1:]]),
        ("packet-final-head", {**metadata["head"], "state_head": "0" * 64}, steps),
    ]
    rejected = list(old["rejected_cases"])
    for label, head, wrong_steps in mutations:
        reject_test(lambda: packet_semantics(head, wrong_steps), label)
        rejected.append(label)
    packet_semantics(metadata["head"], steps)
    return {"schema": SCHEMA + ".parent-layout-selftest", "status": "PASS", "metadata_only": True,
        "parent_layout": old["parent_layout"], "accepted_packet_layout": packet_layout(metadata),
        "rejected_cases": rejected, "cross_checked": False, "verified": False}


def selftest() -> dict[str, Any]:
    """Small new-interface gates; no historical source/P1 closure replay."""
    context, _ = BASE.checker_source_context()
    mixed_cases = []
    for degree in (0, 1):
        source = zero_source()
        if degree == 0:
            source[0][0, 0] = 1
        else:
            source[1][0, 0] = 1
        source[3][6] = 2
        acted = finite27_actor(context, source, 2)
        require(np.any(acted[2]) and np.array_equal(acted[3], source[3]), "canary_nonzero_lower_to_top")
        restored = finite27_actor(context, acted, -2)
        require(all(np.array_equal(left, right) for left, right in zip(restored, source)), "finite27_actor_inverse")
        lower_source = np.concatenate((source[0].reshape(-1), source[1].reshape(-1), source[3]))
        a = next(index for index in range(4) if np.any(acted[2][index]))
        coordinate = int(np.flatnonzero(acted[2][a])[0])
        q = np.zeros(SOURCE_WIDTH, dtype=np.uint8); q[coordinate] = 1
        low, top = BASE.checker_actor_adjoint(context, q, a, 2)
        direct = dot(q, acted[2][a])
        require(direct != 0 and direct == (dot(low, lower_source) + dot(top, source[2][a])) % 3,
                "finite27_mixed_adjoint_canary")
        mixed_cases.append({"input_degree": degree, "actor": 2, "character": a,
            "top_support": int(np.count_nonzero(acted[2])), "nonzero_pairing": direct,
            "inverse_roundtrip": True, "complete_source": True})
    seeds = np.zeros((4, 44), dtype=np.uint8)
    actors = np.zeros((4, 8059, 4), dtype=np.uint8)
    seeds[1, 43] = 1; actors[3, 8058, 3] = 2
    require(first_hit(seeds, actors) == {"character": 1, "origin_id": 43, "index": 32323,
            "origin_kind": "seed", "scalar": 1, "seed": 43}, "first_hit_seed_order")
    seeds[:] = 0
    hit = first_hit(seeds, actors)
    require(hit == {"character": 3, "origin_id": 32279, "index": 129119,
            "origin_kind": "actor", "scalar": 2, "basis_i": 8058, "actor": -2, "actor_slot": 3}, "first_hit_last_origin")
    target = np.zeros(WIDTH, dtype=np.uint8); target[1] = 1
    require(terminal_for_state("Separator", target, {"first_hit": hit}, "UNKNOWN_CAP") == "UNKNOWN_CAP", "cap_with_nonzero_origin")
    reject_test(lambda: terminal_for_state("Separator", target, {"first_hit": hit}, "ROOT_ORIGINS_ZERO"), "false_root_origin_eof")
    vectors = [[np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
    vectors[3][0][0] = 1
    tables = [{"identity": {"adjoint:B": f"fixture-B{a}"}} for a in range(4)]
    arithmetic = {"vectors": vectors, "seeds": seeds, "actors": actors,
        "p1": {"values": np.zeros((4, 5, 8059), dtype=np.uint8), "active": [3]},
        "lower_values": np.zeros((4, 8059, 4), dtype=np.uint8)}
    payloads, manifest = scan_payloads(arithmetic, tables, target, 1, "a" * 64, "b" * 64, "c" * 64)
    with tempfile.TemporaryDirectory(prefix="full-origin-checker-canary-") as temp:
        root = Path(temp)
        scans = root / "scans"; scans.mkdir()
        directory = scans / "000001"; directory.mkdir()
        for name, raw in {**payloads, "manifest.json": canonical(manifest)}.items():
            (directory / name).write_bytes(raw)
        manifest_sha = compare_directory(directory, payloads, manifest)
        (scans / ".pending-000002-canary").mkdir()
        (scans / ".orphan-000003-canary").mkdir()
        audit_prefix_directory(scans, 1, 1)
        # A complete scan must be compared beyond an already selected prefix.
        wrong = bytearray(payloads["actors-c0.u8"]); wrong[-1] = 1
        (directory / "actors-c0.u8").write_bytes(wrong)
        reject_test(lambda: compare_directory(directory, payloads, manifest), "full_array_tail_corruption")
        (directory / "actors-c0.u8").write_bytes(payloads["actors-c0.u8"])
        source = {"producer_sha256": "d" * 64}
        head = head_record(source, "b" * 64, "e" * 64, "c" * 64, 1, "f" * 64, manifest_sha, "a" * 64, "Separator")
        check_seal(head)
        require(head["current_scan_manifest_sha256"] == manifest_sha and head["completed_steps"] == 1,
                "cached_scan_head_interface")
        wrong_head = {**head, "owner_sha256": "0" * 64}
        reject_test(lambda: check_seal(wrong_head), "wrong_owner_head_seal")
        changed = head_record(source, "b" * 64, "e" * 64, "c" * 64, 2, "f" * 64, None, "1" * 64, "Separator")
        require(changed["current_scan_manifest_sha256"] is None and changed["state_head"] != head["state_head"],
                "new_state_clears_cached_scan")
    return {"schema": SCHEMA + ".selftest", "status": "PASS", "gates": ["finite27-complete-mixed-actor",
        "all-four-character-origin-order-and-cap", "full-scan-tail-and-cached-head-interface"],
        "mixed_cases": mixed_cases, "producer_imported": False, "old_success_suites_run": False,
        "cross_checked": False, "verified": False}


def main() -> int:
    global DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("state-root", "delta-root", "seed34-root", "packet-root", "prepare-root", "p1-root", "task712-root", "candidate-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-seconds", type=float, default=1800)
    parser.add_argument("--parent-layout-selftest", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    try:
        require(args.max_seconds > 0, "positive_resource_budget")
        DEADLINE = BEGIN + args.max_seconds
        if args.selftest:
            require(not args.parent_layout_selftest, "distinct_modes")
            result = selftest()
        elif args.parent_layout_selftest:
            require(all(getattr(args, name) is not None for name in ("state_root", "delta_root", "seed34_root", "packet_root")), "parent_metadata_roots")
            result = parent_layout_selftest(args)
        else:
            require(all(getattr(args, name) is not None for name in ("state_root", "delta_root", "seed34_root", "packet_root",
                    "prepare_root", "p1_root", "task712_root", "candidate_root")) and len(args.block_root) == 4, "actual_parent_roots")
            result = check_actual(args)
        code = 0
    except ResourceStop as exc:
        result = {"schema": SCHEMA + ".checker-result", "status": "UNKNOWN", "terminal": "UNKNOWN_RESOURCE",
            "phase": str(exc), "prefix_steps_replayed": REPLAYED_STEPS, "complete_scans_replayed": REPLAYED_SCANS,
            "elapsed_seconds": round(time.monotonic() - BEGIN, 3), "candidate": False,
            "cross_checked": False, "verified": False}
        code = 3
    except Exception as exc:
        result = {"schema": SCHEMA + ".checker-result", "status": "FAIL", "reason": str(exc), "phase": LAST_PHASE,
            "prefix_steps_replayed": REPLAYED_STEPS, "complete_scans_replayed": REPLAYED_SCANS,
            "candidate": False, "cross_checked": False, "verified": False}
        code = 2
    if args.output is not None:
        require(not args.output.is_symlink(), "output_symlink")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(canonical(result))
    sys.stdout.buffer.write(canonical(result)); sys.stdout.buffer.flush()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
