#!/usr/bin/env python3
"""Task951: independent fixed44 primal packet and complete-prefix checker.

Only accepted checker arithmetic is imported. The packet, all changing
B-adjoint pairings and newly committed steps are independently reconstructed.
Old state/lift/target derivations remain named premises; rho2 is never read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import time
from typing import Any, Callable

import numpy as np

SCHEMA = "d972.r07.fixed-root-packet-loop.v2"
LINEAGE = {
    "check_d972_r07_actual_root_seed_materializer_v3.py":
        "eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701",
    "check_d972_r07_rank1355_root_seed_scalars_v1.py":
        "f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62",
    "check_d972_r07_actual_grade2_root_scalar_batch_v2.py":
        "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6",
    "check_d972_r07_targeted_grade2_owner_generated_join_v15.py":
        "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662",
}
for _name, _digest in LINEAGE.items():
    _file = Path(__file__).resolve().parent / _name
    if _file.is_symlink() or hashlib.sha256(_file.read_bytes()).hexdigest() != _digest:
        raise ValueError("fixed_packet_checker:source_pin:" + _name)
DATA_PINS = {
    "scratchpad/fuda1_a0_rmax_data.g": {"bytes": 4709,
        "sha256": "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"},
    "scratchpad/a0_paper_words_v1.json": {"bytes": 115928,
        "sha256": "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"},
}
for _name, _identity in DATA_PINS.items():
    _file = Path(__file__).resolve().parents[1] / _name
    if _file.is_symlink() or _file.stat().st_size != _identity["bytes"] or \
            hashlib.sha256(_file.read_bytes()).hexdigest() != _identity["sha256"]:
        raise ValueError("fixed_packet_checker:data_pin:" + _name)
import check_d972_r07_actual_root_seed_materializer_v3 as LEGACY

BASE, ROOTS = LEGACY.BASE, LEGACY.ROOTS
WIDTH, ROW_BYTES, SOURCE_WIDTH, SOURCE_BYTES = 48384, 12096, 36288, 9072
START_HEAD = "d467e4e60b8bff88272cddd4b01d630d763e863b4500015c7c6c077b23ddf26b"
START_LAMBDA = "f7406d70211ab02acf08a895d127d17e7dab179454916a90ea40cb11152e12dd"
START_TARGET = "46a6b8281587a13236fd9af00eab9825a2d956dd878613af14182b5f9ae94c49"
SEED34_ARTIFACT = {
    "run": 33956437467, "attempt": 1, "head": "b9ae78b0950b186463849c3ec874f6474f359851",
    "id": 9966542166,
    "name": "d972-r07-actual-root-seed-materializer-v3-candidate-33956437467-1",
    "bytes": 984053,
    "sha256": "sha256:a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc",
}
SEED34_FILES = {
    "output/manifest.json": (1813, "0acac7c5cbe15375c25ccc4c9109dad449ed38e60898b68ca0b7b3cda4fcda52"),
    "output/result.json": (3135681, "3a8357365f4e5f3f7d281b811d36d49e4f334cbec3828c82833ae1b1d5af0242"),
    "output/instruction.json": (147200, "790af5b3556c78ec2b81f45602aa50779435f46ddde57a8e5b5414566813dc7f"),
    "checker-result.json": (1570, "0e514b8833c37333ec9643775f5d752958a1a1a35dd6673ff65fdb620b6a556c"),
    "source-receipt.json": (1304, "0a037063a25b161566791638e025d301bc2275b50f4896176897271f528f9451"),
}
START_RANK, START_GENERATION, MAX_APPENDS = 1356, 8061, 176
SCOPE = {"characters": [0, 1, 2, 3], "seeds": list(range(44)), "order": "character-major/seed0-through43",
         "declared_pair_count": 176, "max_appends": 176, "actor_origins_executed": 0, "orbit_rows_executed": 0}
CLAIMS = {"FIXED_ROOT_PACKET_LOOP_CANDIDATE": True, "GRADE2_MEMBER": "NOT_DECIDED",
          "GRADE2_NONMEMBER": "NOT_DECIDED", "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
          "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False}
PRODUCER_LINEAGE = {
    "d972_r07_actual_root_seed_materializer_v3.py":
        "36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332",
    "d972_r07_rank1355_root_seed_scalars_v1.py":
        "973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb",
    "d972_r07_actual_grade2_root_scalar_batch_v2.py":
        "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
    "d972_r07_targeted_grade2_owner_generated_join_v15.py":
        "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632",
}
BEGIN = time.monotonic()
DEADLINE: float | None = None
LAST_PHASE = "initialization"
REPLAYED_STEPS = 0


class ResourceStop(Exception):
    pass


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError("fixed_packet_checker:" + reason)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    require("sha256" not in value, "already_sealed")
    return {**value, "sha256": sha(canonical(value))}


def same(actual: Any, expected: Any, reason: str) -> None:
    require(canonical(actual) == canonical(expected), reason)


def check_seal(value: Any) -> None:
    require(isinstance(value, dict) and "sha256" in value, "sealed_object")
    same(value, seal({key: item for key, item in value.items() if key != "sha256"}), "seal")


def progress(phase: str, **fields: Any) -> None:
    global LAST_PHASE
    LAST_PHASE = phase
    if DEADLINE is not None and time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)
    print(json.dumps({"phase": phase, "elapsed_seconds": round(time.monotonic() - BEGIN, 3),
                      **fields}, sort_keys=True), file=sys.stderr, flush=True)


pack, unpack, dot = LEGACY.pack, LEGACY.unpack, LEGACY.dot
subtract, file_receipt = LEGACY.subtract, LEGACY.file_receipt
fixed, path, json_bytes = LEGACY.fixed, LEGACY.path, LEGACY.json_bytes


def validate_parent_generations(base: dict[str, Any], seed30: dict[str, Any],
                                seed34: dict[str, Any]) -> dict[str, Any]:
    """Metadata semantics shared by production and the actual-parent regression.

    Callers authenticate complete accepted result bytes first. This validator
    does not modify the parents or infer the absent legacy flag's value.
    """
    require(base["schema"] == "d972.r07.physical-state.Separator.v1" and
            base["target_reduction"]["schema"] == "d972.r07.physical-state.target-reduction.v1",
            "base_parent_schema")
    require(seed30["schema"] == "d972.r07.actual-seed30-materializer.v1.result" and
            seed30["target"]["schema"] == "d972.r07.actual-seed30-materializer.v1.target-update",
            "legacy_parent_schema")
    require(seed34["schema"] == "d972.r07.actual-root-seed-materializer.v3.result" and
            seed34["target"]["schema"] == "d972.r07.actual-root-seed-materializer.v3.target-update",
            "v3_parent_schema")
    flag = "target_derivation_accepted_as_premise"
    legacy_rho2, v3_rho2 = seed30["parents"]["rho2"], seed34["parents"]["rho2"]
    require(flag not in legacy_rho2 and set(legacy_rho2) == {"artifact", "manifest_sha256", "packed_sha256"},
            "exact_legacy_no_flag_shape")
    require(flag in v3_rho2 and v3_rho2[flag] is True and
            set(v3_rho2) == {"artifact", "manifest_sha256", "packed_sha256", flag}, "required_v3_true_flag")
    same(legacy_rho2, {key: value for key, value in v3_rho2.items() if key != flag}, "same_original_rho2_parent")
    base_target, old_target, new_target = base["target_reduction"], seed30["target"], seed34["target"]
    require(legacy_rho2["packed_sha256"] == v3_rho2["packed_sha256"] == base_target["rho2_sha256"] ==
            old_target["rho2_sha256"] == new_target["rho2_sha256"] ==
            "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e" and
            legacy_rho2["manifest_sha256"] == v3_rho2["manifest_sha256"] ==
            base_target["target_parent_manifest_sha256"] ==
            "55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488", "original_rho2_base_manifest_join")
    require(old_target["parent_result_sha256"] == ROOTS.STATE_FILES["output/result.json"][1] and
            old_target["parent_target_sha256"] == sha(canonical(base_target)) and
            old_target["old_remainder_sha256"] == base_target["remainder_sha256"] and
            new_target["parent_result_sha256"] == ROOTS.DELTA_FILES["output/result.json"][1] and
            new_target["parent_target_sha256"] == sha(canonical(old_target)) and
            new_target["old_remainder_sha256"] == old_target["remainder_sha256"] and
            old_target["remainder_sha256"] == LEGACY.CURRENT_REMAINDER and
            new_target["remainder_sha256"] == START_TARGET and
            base_target["state_head"] == LEGACY.OLD_HEAD and old_target["state_head"] == LEGACY.CURRENT_HEAD and
            new_target["state_head"] == START_HEAD, "accepted_target_identity_chain")
    return {"base": base, "seed30": seed30, "seed34": seed34,
            "targets": [base_target, old_target, new_target]}


def load_parent_layout_inputs(args: argparse.Namespace,
                              saved_seed34: dict[str, Any] | None = None) -> dict[str, Any]:
    """Read only pinned JSON and payload byte receipts, with no vector decoding."""
    groups = [
        ("base", args.state_root, ROOTS.STATE_FILES),
        ("seed30", args.delta_root, ROOTS.DELTA_FILES),
        ("seed34", args.seed34_root, SEED34_FILES),
    ]
    loaded = {}
    for role, root, pins in groups:
        objects = saved_seed34 if role == "seed34" and saved_seed34 is not None else {
            name: json_bytes(fixed(root, name, identity)) for name, identity in pins.items()}
        loaded[role] = objects
        result = objects["output/result.json"]
        if role == "base":
            same(result["target_reduction"], objects["output/terminal.json"]["target_reduction"],
                 "metadata_base_target_pair")
            continue
        manifest = objects["output/manifest.json"]
        for item in (manifest, result, result["target"]):
            check_seal(item)
        require(objects["checker-result.json"]["status"] == "PASS" and
                objects["checker-result.json"]["result_sha256"] == pins["output/result.json"][1],
                "metadata_saved_checker_join")
        for item in manifest["files"]:
            raw = fixed(root / "output", item["file"], (item["bytes"], item["sha256"]))
            require(file_receipt(item["file"], raw) == item, "metadata_saved_payload_receipt")
        require(sorted(item.name for item in (root / "output").iterdir()) == manifest["file_roster"],
                "metadata_saved_payload_roster")
    facts = validate_parent_generations(*(loaded[role]["output/result.json"] for role in ("base", "seed30", "seed34")))
    return {"objects": loaded, "facts": facts}


def parent_layout_receipt(facts: dict[str, Any]) -> dict[str, Any]:
    base = facts["base"]
    base_target = base["target_reduction"]
    base_record = {"result_schema": base["schema"], "target_schema": base_target["schema"],
        "state_manifest_sha256": ROOTS.STATE_FILES["state/manifest.json"][1],
        "result_sha256": ROOTS.STATE_FILES["output/result.json"][1],
        "target_sha256": sha(canonical(base_target)), "rho2_sha256": base_target["rho2_sha256"]}
    deltas = []
    flag = "target_derivation_accepted_as_premise"
    for role, pins in (("seed30", ROOTS.DELTA_FILES), ("seed34", SEED34_FILES)):
        result = facts[role]
        target, rho2 = result["target"], result["parents"]["rho2"]
        deltas.append({"role": role, "result_schema": result["schema"], "target_schema": target["schema"],
            "manifest_sha256": pins["output/manifest.json"][1], "result_sha256": pins["output/result.json"][1],
            "target_sha256": sha(canonical(target)),
            "rho2_identity": {key: rho2[key] for key in ("artifact", "manifest_sha256", "packed_sha256")},
            "target_derivation_flag_present": flag in rho2,
            "target_derivation_flag_value": rho2[flag] if flag in rho2 else None,
            "admission": "exact-accepted-legacy-target-chain" if role == "seed30" else "exact-accepted-v3-explicit-target-premise",
            "payloads": {"source_d_sha256": result["raw_materialization"]["raw_source_sha256"],
                "physical_normalized_sha256": result["pivot"]["normalized_sha256"],
                "target_remainder_sha256": target["remainder_sha256"]}})
    return seal({"schema": SCHEMA + ".parent-layout", "base": base_record, "deltas": deltas,
                 "derivation_mode": "derived", "original_rho2_directly_read": False, "old_target_history_replayed": False})


def parent_layout_selftest(args: argparse.Namespace) -> dict[str, Any]:
    metadata = load_parent_layout_inputs(args)
    facts = metadata["facts"]
    base, seed30, seed34 = (facts[role] for role in ("base", "seed30", "seed34"))
    layout = parent_layout_receipt(facts)
    flag = "target_derivation_accepted_as_premise"
    original = seed34["parents"]["rho2"]
    def with_v3_rho2(rho2: dict[str, Any]) -> dict[str, Any]:
        return {**seed34, "parents": {**seed34["parents"], "rho2": rho2}}
    mutations = [
        ("v3-flag-false", base, seed30, with_v3_rho2({**original, flag: False})),
        ("v3-flag-missing", base, seed30, with_v3_rho2({key: value for key, value in original.items() if key != flag})),
        ("rho2-packed-identity", base, seed30, with_v3_rho2({**original, "packed_sha256": "0" * 64})),
        ("unexpected-parent-schema", base, {**seed30, "schema": "unexpected-parent-schema"}, seed34),
        ("base-target-manifest", {**base, "target_reduction": {**base["target_reduction"],
                                 "target_parent_manifest_sha256": "0" * 64}}, seed30, seed34),
    ]
    rejected = []
    for label, wrong_base, wrong_seed30, wrong_seed34 in mutations:
        reject_test(lambda: validate_parent_generations(wrong_base, wrong_seed30, wrong_seed34), label)
        rejected.append(label)
    # No mutation touched the authenticated originals or inserted a legacy flag.
    same(parent_layout_receipt(validate_parent_generations(base, seed30, seed34)), layout,
         "actual_parent_metadata_immutable")
    return {"schema": SCHEMA + ".parent-layout-selftest", "status": "PASS", "metadata_only": True,
        "parent_layout": layout, "rejected_cases": rejected,
        "fixtures": [{"role": role, "files": [{"file": name, "bytes": identity[0], "sha256": identity[1]}
                        for name, identity in sorted(pins.items())]} for role, pins in
                     (("base", ROOTS.STATE_FILES), ("seed30", ROOTS.DELTA_FILES), ("seed34", SEED34_FILES))],
        "physical_rows_replayed": 0, "raw_seeds_evaluated": 0,
        "original_rho2_directly_read": False, "cross_checked": False, "verified": False}


def load_start(args: argparse.Namespace) -> dict[str, Any]:
    """Authenticate the immutable 1354 base and both accepted actual deltas."""
    progress("parent_loading", parent="seed34")
    objects = {name: json_bytes(fixed(args.seed34_root, name, identity))
               for name, identity in SEED34_FILES.items()}
    parent_metadata = load_parent_layout_inputs(args, objects)
    result, manifest, checker, instruction, source = (objects[name] for name in
        ("output/result.json", "output/manifest.json", "checker-result.json",
         "output/instruction.json", "source-receipt.json"))
    for item in (result, manifest, result["pivot"], result["target"]):
        check_seal(item)
    require(result["status"] == checker["status"] == "PASS" and
            result["kind"] == checker["kind"] == "Separator" and
            checker["manifest_sha256"] == SEED34_FILES["output/manifest.json"][1] and
            checker["result_sha256"] == SEED34_FILES["output/result.json"][1] and
            checker["instruction_sha256"] == SEED34_FILES["output/instruction.json"][1] and
            manifest["state_head"] == checker["state_head"] == START_HEAD and
            manifest["rank_after"] == checker["rank_after"] == START_RANK and
            all(item["verified"] is False and item["cross_checked"] is False
                for item in (result, manifest, checker, source)), "accepted_seed34_authority")
    source_files = {item["file"]: item["sha256"] for item in source["files"]}
    require(source_files["search/d972_r07_actual_root_seed_materializer_v3.py"] ==
            "36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332" and
            source_files["search/check_d972_r07_actual_root_seed_materializer_v3.py"] ==
            LINEAGE["check_d972_r07_actual_root_seed_materializer_v3.py"], "seed34_executed_sources")
    payloads = {item["file"]: fixed(args.seed34_root / "output", item["file"],
                                   (item["bytes"], item["sha256"])) for item in manifest["files"]}
    require(sorted(item.name for item in (args.seed34_root / "output").iterdir()) ==
            manifest["file_roster"] == sorted([*payloads, "manifest.json"]), "seed34_roster")
    unsigned = {key: item for key, item in instruction.items() if key != "rolling_sha256"}
    require(instruction["predecessor"] == LEGACY.CURRENT_HEAD and
            instruction["offer"] == 8060 and instruction["generation"] == START_GENERATION and
            instruction["rank"] == START_RANK and
            instruction["rolling_sha256"] == sha(bytes.fromhex(LEGACY.CURRENT_HEAD) + canonical(unsigned)) ==
            START_HEAD, "seed34_instruction_chain")
    task554 = ROOTS.task554_parent(args)
    launch = {"separator": {"artifact": ROOTS.DELTA_ARTIFACT, "generation": 8060, "rank": 1355,
        "head": LEGACY.CURRENT_HEAD, "lambda_sha256": LEGACY.CURRENT_LAMBDA,
        "files": [{"file": name, "bytes": item[0], "sha256": item[1]}
                  for name, item in sorted(ROOTS.DELTA_FILES.items())]},
        "p1_parent": result["parents"]["p1"], "task554_parent": task554,
        "task712_parent": BASE.TASK712_PARENT}
    state = LEGACY.load_state(args, {"launch": launch})
    same(result["parents"]["state"], state["parent"], "seed34_saved_parent_state")
    pivot, target = result["pivot"], result["target"]
    normalized = unpack(payloads["physical-normalized.bin"], WIDTH)
    current_target, functional = (unpack(payloads[name], WIDTH)
                                  for name in ("target-remainder.bin", "lambda.bin"))
    require(pivot["pivot_id"] == 1355 and pivot["head_before"] == LEGACY.CURRENT_HEAD and
            pivot["head_after"] == START_HEAD and pivot["rank_before"] == 1355 and
            pivot["rank_after"] == START_RANK and pivot["generation_after"] == START_GENERATION and
            pivot["lead"] == instruction["lead"] == 1418 and
            pivot["normalized_sha256"] == sha(payloads["physical-normalized.bin"]) ==
            "a17e774a0641d009f804812c4ca1c5252db785afa821105ca6f331fa26995578" and
            all(normalized[item["lead"]] == 0 for item in state["pivots"]) and
            normalized[pivot["lead"]] == 1, "saved_seed34_pivot")
    require(target["parent_result_sha256"] == ROOTS.DELTA_FILES["output/result.json"][1] and
            target["parent_target_sha256"] == sha(canonical(state["old_target"])) and
            target["old_remainder_sha256"] == LEGACY.CURRENT_REMAINDER and
            target["remainder_sha256"] == sha(payloads["target-remainder.bin"]) == START_TARGET and
            target["state_head"] == START_HEAD and target["state_rank"] == START_RANK and
            result["separator"]["lambda_sha256"] == sha(payloads["lambda.bin"]) == START_LAMBDA,
            "seed34_target_chain")
    rho2 = result["parents"]["rho2"]
    require(rho2["packed_sha256"] == target["rho2_sha256"] == state["old_target"]["rho2_sha256"] ==
            "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e" and
            rho2["manifest_sha256"] == state["base_target"]["target_parent_manifest_sha256"],
            "accepted_original_rho2_base_target_identity")
    state["pivots"].append({"offer": 8060, "lead": pivot["lead"], "physical_offset": 1355 * ROW_BYTES,
                            "coefficient_offset": None, "rolling_sha256": START_HEAD})
    require(all(current_target[item["lead"]] == 0 for item in state["pivots"]), "start_target_normal_form")
    state.update({"seed34": {"result": result, "manifest": manifest, "checker": checker,
                            "payloads": payloads}, "start_lambda": functional,
        "start_target": current_target, "task554": task554, "launch": launch,
        "saved_rows": [state["saved_pivot"], payloads["physical-normalized.bin"]],
        "parent_layout": parent_layout_receipt(parent_metadata["facts"])})
    with path(args.state_root, "state/physical.bin").open("rb", buffering=1 << 20) as stream:
        for index in range(1354):
            row = stream.read(ROW_BYTES)
            require(len(row) == ROW_BYTES and dot(functional, unpack(row, WIDTH)) == 0,
                    "start_lambda_base_rows")
        require(stream.read(1) == b"", "base_rows_trailing")
    require(all(dot(functional, unpack(row, WIDTH)) == 0 for row in state["saved_rows"]) and
            dot(functional, current_target) == dot(functional, state["old_remainder"]) == 1,
            "start_lambda_saved_rows_targets")
    progress("start_authenticated", generation=START_GENERATION, rank=START_RANK, step=0)
    return state


def collect_relations(args: argparse.Namespace, task554: dict[str, Any]) -> tuple[list[Any], np.ndarray]:
    """Retain ordered literal events before collecting any numerical coefficients."""
    bodies = []
    for index, descriptor in enumerate([task554["prepare"], *task554["blocks"]]):
        progress("packet_task554", body=index + 1, total=5)
        state = BASE.state_descriptor(descriptor, index - 1)
        if index == 0:
            expressions = [[old["record"]["seed_reductions"][seed] for old in state["body"]["old_blocks"]]
                           for seed in range(44)]
        else:
            expressions = [[state["body"]["origin_reductions"][start + seed]
                            for start, _ in LEGACY.ORIGIN_RANGES] for seed in range(44)]
        bodies.append({"expressions": expressions, "body_sha256": state["body_sha256"]})
        del state
    relations = []
    coefficients = np.zeros((44, 8059), dtype=np.uint8)
    for seed in range(44):
        selected = [{"expressions": body["expressions"][seed], "body_sha256": body["body_sha256"]}
                    for body in bodies]
        events, final = LEGACY.combined_selected(selected, seed)
        for node, value in final:
            coefficients[seed, node] = value
        relations.append({"seed": seed, "events": events, "coefficients": final})
    return relations, coefficients


def p1_packet_pass(args: argparse.Namespace, state: dict[str, Any], coefficients: np.ndarray,
                   tops: np.ndarray, selected: set[int]) -> tuple[dict[str, Any], list[Any]]:
    """One instruction/cache pass with one decoded row and per-seed scratch."""
    p1 = BASE.validate_p1({**state["launch"]["p1_parent"], "root": str(args.p1_root.resolve())})
    roots, offset, ancestry = [], 0, "0" * 64
    instructions_digest, cache_digest = hashlib.sha256(), hashlib.sha256()
    with path(args.p1_root, "instructions.jsonl").open("rb", buffering=1 << 20) as instructions, \
            path(args.p1_root, "degree2.cache.bin").open("rb", buffering=1 << 20) as cache:
        for node in range(8059):
            line, packed = instructions.readline(), cache.read(36288)
            require(line.endswith(b"\n") and len(packed) == 36288, "packet_p1_eof")
            instructions_digest.update(line)
            cache_digest.update(packed)
            item = json_bytes(line)
            require(item["node"] == node and item["offset"] == node * 36288 and item["length"] == 36288 and
                    item["predecessor"] == ancestry and item["row_receipt"]["offset"] == node * 36288 and
                    item["row_receipt"]["length"] == 36288 and item["row_receipt"]["sha256"] == sha(packed),
                    "packet_p1_row_join")
            require(item["ancestry_sha256"] == sha(bytes.fromhex(ancestry) +
                    canonical({key: value for key, value in item.items() if key != "ancestry_sha256"})),
                    "packet_p1_rolling")
            ancestry = item["ancestry_sha256"]
            if node in selected:
                roots.append({"node": node, "instruction_offset": offset, "instruction_length": len(line),
                    "instruction_sha256": sha(line), "ancestry_sha256": ancestry,
                    "predecessor": item["predecessor"], "p1_sha256": item["p1_sha256"],
                    "row_sha256": item["row_receipt"]["sha256"],
                    "origin_sha256": sha(canonical(item["origin"])),
                    "reductions_sha256": sha(canonical(item["reductions"])), "scale": item["scale"],
                    "literal_input_sha256": item["literal_input_sha256"],
                    "lift_components": [{"role": "p1-degree2", "bytes": len(packed), "sha256": sha(packed)}]})
            row = unpack(packed, 145152).reshape(4, SOURCE_WIDTH)
            for seed in np.flatnonzero(coefficients[:, node]):
                subtract(tops[int(seed)], row, int(coefficients[seed, node]))
            offset += len(line)
            if (node + 1) % 1024 == 0:
                progress("packet_p1_pass", rows=node + 1, total=8059)
        require(instructions.read(1) == cache.read(1) == b"", "packet_p1_trailing")
    require(offset == BASE.P1_INSTRUCTION_BYTES and instructions_digest.hexdigest() == BASE.P1_INSTRUCTION_SHA256
            and cache_digest.hexdigest() == BASE.P1_CACHE_SHA256 and ancestry == p1["manifest"]["ancestry_sha256"]
            and len(roots) == len(selected), "packet_p1_complete_identity")
    return p1, roots


def lower_packet_pass(args: argparse.Namespace, coefficients: np.ndarray,
                      lower0: np.ndarray, lower1: np.ndarray, aux: np.ndarray,
                      roots: list[Any]) -> list[Any]:
    receipts = []
    by_node = {root["node"]: root for root in roots}
    for slot in range(12):
        if slot < 8:
            owner, component = divmod(slot, 2)
            descriptor = BASE.OLD_BLOB_PINS[owner][component]
            root, start = args.prepare_root, LEGACY.OLD_OFFSETS[owner]
        else:
            owner, component = slot - 8, 2
            descriptor = BASE.NEW_BLOB_PINS[owner]
            root, start = args.block_root[owner], LEGACY.NEW_OFFSETS[owner]
        digest, size = hashlib.sha256(), (descriptor["width"] + 3) // 4
        item = path(root, descriptor["file"])
        require(item.stat().st_size == descriptor["bytes"], "lower_blob_size")
        with item.open("rb", buffering=1 << 20) as stream:
            for local in range(descriptor["rows"]):
                packed = stream.read(size)
                require(len(packed) == size, "lower_blob_eof")
                digest.update(packed)
                if start + local in by_node:
                    by_node[start + local]["lift_components"].append({
                        "role": ("old-lower", "old-grade", "new-grade")[component],
                        "bytes": len(packed), "sha256": sha(packed)})
                row = unpack(packed, descriptor["width"])
                for seed in np.flatnonzero(coefficients[:, start + local]):
                    seed, value = int(seed), int(coefficients[seed, start + local])
                    if component == 0:
                        subtract(lower0[seed, owner], row[:6048], value)
                        subtract(aux[seed], row[6048:], value)
                    elif component == 1:
                        subtract(lower1[seed], row.reshape(4, 18144), value)
                    else:
                        subtract(lower1[seed, owner], row, value)
            require(stream.read(1) == b"", "lower_blob_trailing")
        require(digest.hexdigest() == descriptor["sha256"], "lower_blob_identity")
        receipts.append(descriptor)
        progress("packet_lower_pass", blob=slot + 1, total=12)
    return receipts


def rebuild_packet(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    relations, coefficients = collect_relations(args, state["task554"])
    selected = {event["global_index"] for relation in relations for event in relation["events"]}
    context, words = BASE.checker_source_context()
    require(len(words["relators"]) == 44, "registered_seed_count")
    lower0, lower1 = np.zeros((44, 4, 6048), dtype=np.uint8), np.zeros((44, 4, 18144), dtype=np.uint8)
    tops, aux = np.zeros((44, 4, SOURCE_WIDTH), dtype=np.uint8), np.zeros((44, 8), dtype=np.uint8)
    raw_receipts, compact_words = [], []
    for seed, relator in enumerate(words["relators"]):
        word = [int(letter) for letter in relator]
        raw = BASE.ARITH._checker_seed_evaluate_seed(context, tuple(word))
        require([part.shape for part in raw] == [(4, 6048), (4, 18144), (4, 36288), (8,)], "raw_seed_shape")
        if seed == 2:
            require(sha(pack(raw[2][0])) == BASE.SEED2_RAW_PACKED_SHA256 and
                    int(np.count_nonzero(raw[2][0])) == 568, "lambda_independent_seed2_raw_pin")
        for destination, source in zip((lower0, lower1, tops, aux), raw):
            destination[seed] = source
        raw_receipts.append([LEGACY.component_receipt(name, part)
                             for name, part in zip(("d0", "d1", "d2", "aux"), raw)])
        compact_words.append(word)
        del raw
        progress("packet_raw_seed", seed=seed, evaluated=seed + 1, total=44)
    p1, roots = p1_packet_pass(args, state, coefficients, tops, selected)
    blobs = lower_packet_pass(args, coefficients, lower0, lower1, aux, roots)
    reduced_receipts = []
    for seed in range(44):
        parts = (lower0[seed], lower1[seed], tops[seed], aux[seed])
        LEGACY.require_lower_zero(parts)
        reduced_receipts.append([LEGACY.component_receipt(name, part)
                                 for name, part in zip(("d0", "d1", "d2", "aux"), parts)])
    # Accepted v453 slicing applies here, after the COMPLETE lower part vanished.
    # No mixed raw-seed projector or extra structural closure is executed.
    raw_packet = b"".join(pack(tops[seed, character]) for character in range(4) for seed in range(44))
    require(len(raw_packet) == 1596672, "packet_size")
    seed30 = fixed(args.delta_root / "output", "source-d.bin", (SOURCE_BYTES,
        state["delta"]["result"]["raw_materialization"]["raw_source_sha256"]))
    seed34 = state["seed34"]["payloads"]["source-d.bin"]
    require(pack(tops[30, 0]) == seed30 and pack(tops[34, 0]) == seed34 and
            sha(seed34) == "e96170bf6812d7143feb9b77f9aa6d89313fdbf1b4e1c99aa3f7c50a8fc89f60",
            "packet_saved_source_regressions")
    arithmetic_rows = int(np.count_nonzero(np.any(coefficients, axis=0)))
    del lower0, lower1, aux, coefficients, context
    return {"tops": tops, "tops_raw": raw_packet, "relations": relations, "p1_roots": roots,
        "p1": p1, "raw_receipts": raw_receipts, "reduced_receipts": reduced_receipts,
        "compact_words": compact_words, "blobs": blobs, "arithmetic_rows": arithmetic_rows}


def load_tables(args: argparse.Namespace) -> list[dict[str, Any]]:
    tables = []
    for character in range(4):
        table = BASE.ARITH.read_task712_envelope({**BASE.TASK712_PARENT,
                                                "root": str(args.task712_root.resolve())}, character)
        BASE.check_table_transpose(table["forward"]["B"], table["adjoint"]["B"])
        entries = np.asarray(table["forward"]["B"], dtype=np.int64)
        require(entries.shape == (36288, 3), "B_table_shape")
        tables.append({"identity": table["identity"], "manifest_sha256": table["manifest_sha256"],
                       "entries": entries})
    return tables


def pullback(entries: np.ndarray, functional: np.ndarray, source_width: int = SOURCE_WIDTH) -> np.ndarray:
    pulled = np.zeros(source_width, dtype=np.int64)
    np.add.at(pulled, entries[:, 0], entries[:, 2] * functional[entries[:, 1]])
    return (pulled % 3).astype(np.uint8)


def pushforward(entries: np.ndarray, source: np.ndarray, physical_width: int = WIDTH) -> np.ndarray:
    physical = np.zeros(physical_width, dtype=np.int64)
    np.add.at(physical, entries[:, 1], entries[:, 2] * source[entries[:, 0]])
    return (physical % 3).astype(np.uint8)


def evaluate_roots(tables: list[Any], tops: np.ndarray, functional: np.ndarray) -> tuple[list[np.ndarray], list[int]]:
    roots, values = [], []
    for character, table in enumerate(tables):
        q = pullback(table["entries"], functional)
        roots.append(q)
        for seed in range(44):
            values.append(dot(q, tops[seed, character]))
    require(len(values) == 176, "declared_root_pair_count")
    return roots, values


def strip_roots(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: strip_roots(item) for key, item in value.items() if key != "root"}
    if isinstance(value, list):
        return [strip_roots(item) for item in value]
    return value


def expected_start(state: dict[str, Any]) -> dict[str, Any]:
    parents = []
    targets = [state["base_target"], state["old_target"], state["seed34"]["result"]["target"]]
    manifests = [LEGACY.STATE_FILES["state/manifest.json"][1], ROOTS.DELTA_FILES["output/manifest.json"][1],
                 SEED34_FILES["output/manifest.json"][1]]
    results = [LEGACY.STATE_FILES["output/result.json"][1], ROOTS.DELTA_FILES["output/result.json"][1],
               SEED34_FILES["output/result.json"][1]]
    for role, target, manifest, result, state_head in zip(
            ("base", "seed30", "seed34"), targets, manifests, results,
            (LEGACY.OLD_HEAD, LEGACY.CURRENT_HEAD, START_HEAD)):
        parents.append({"role": role, "manifest_sha256": manifest, "result_sha256": result,
                        "target_sha256": sha(canonical(target)), "state_head": state_head})
    return seal({"schema": SCHEMA + ".start", "rank": START_RANK, "generation": START_GENERATION,
        "state_head": START_HEAD, "lambda_sha256": START_LAMBDA, "target_remainder_sha256": START_TARGET,
        "base_manifest_sha256": manifests[0], "seed30_manifest_sha256": manifests[1],
        "seed34_manifest_sha256": manifests[2], "accepted_target_derivation_parents": parents,
        "parent_layout": state["parent_layout"]})


def rho2_derivation(start: dict[str, Any], completed: int) -> dict[str, Any]:
    return {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
        "accepted_target_derivation_parents": start["accepted_target_derivation_parents"],
        "newly_executed_target_steps": completed,
        "original_rho2_packed_sha256": "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e",
        "accepted_identity_convention": {
            "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)"},
        "new_identity_convention": "parent_remainder - child_remainder = target.scalar * normalized_row"}


def expected_owner(state: dict[str, Any], tables: list[Any]) -> dict[str, Any]:
    return seal({"schema": SCHEMA + ".owner", "formula_id": LEGACY.FORMULA, "scope": SCOPE,
        "p1_parent": strip_roots(state["launch"]["p1_parent"]),
        "task554_parent": strip_roots(state["task554"]), "task712_parent": BASE.TASK712_PARENT,
        "task712_manifest_sha256": [table["manifest_sha256"] for table in tables],
        "word_dictionary_sha256": BASE.ARITH.WORD_SHA, "relator_dictionary_sha256": BASE.ARITH.WORD_RELATOR_SHA})


def projector_records() -> list[dict[str, Any]]:
    projectors = []
    for character, label in enumerate(LEGACY.CHARACTERS):
        factors = [{"label": list(conjugator), "pure_word": list(BASE.ARITH.SEED_PURE_WORDS[conjugator]),
            "pure_word_sha256": sha(canonical(list(BASE.ARITH.SEED_PURE_WORDS[conjugator]))),
            "source_character_sign": 1 if sum(x * y for x, y in zip(label, conjugator)) % 2 == 0 else 2}
            for conjugator in LEGACY.CHARACTERS]
        projectors.append({"character": character, "character_label": list(label), "factors": factors})
    return projectors


def packet_payloads(packet: dict[str, Any], owner_sha: str) -> tuple[dict[str, bytes], dict[str, Any]]:
    relations = seal({"schema": SCHEMA + ".relations",
        "event_order": "old-source,then-target/source,stored-term-order",
        "seeds": [seal({"schema": SCHEMA + ".seed-relation", "seed": item["seed"],
            "raw_events": item["events"], "raw_event_count": len(item["events"]),
            "raw_event_final_head": item["events"][-1]["rolling_sha256"] if item["events"] else "0" * 64,
            "final_coefficients": item["coefficients"]}) for item in packet["relations"]]})
    roots = seal({"schema": SCHEMA + ".p1-roots", "roots": packet["p1_roots"]})
    raw_seeds, seeds = [], []
    for seed in range(44):
        word = packet["compact_words"][seed]
        raw_seeds.append(seal({"schema": SCHEMA + ".raw-seed", "seed": seed, "compact_word": word,
            "compact_word_sha256": sha(canonical(word)), "word_dictionary_sha256": BASE.ARITH.WORD_SHA,
            "relator_dictionary_sha256": BASE.ARITH.WORD_RELATOR_SHA, "components": packet["raw_receipts"][seed]}))
        top_rows = [{"character": a, "seed": seed, "offset": (a * 44 + seed) * SOURCE_BYTES,
            "length": SOURCE_BYTES, "sha256": sha(pack(packet["tops"][seed, a])),
            "support": int(np.count_nonzero(packet["tops"][seed, a]))} for a in range(4)]
        seeds.append({"seed": seed, "lower_width": 96776, "lower_nonzero_count": 0,
            "lower_zero_count": 96776, "lower_dense_sha256": sha(b"\0" * 96776),
            "reduced_components": packet["reduced_receipts"][seed], "top_rows": top_rows})
    lower = []
    for slot, descriptor in enumerate(packet["blobs"]):
        if slot < 8:
            a, kind = divmod(slot, 2)
            role = f"old-{a}-" + ("lower" if kind == 0 else "grade")
            body_sha = BASE.TASK554_BODY_DIGESTS[0]
        else:
            a, role = slot - 8, f"new-{slot - 8}-grade"
            body_sha = BASE.TASK554_BODY_DIGESTS[a + 1]
        lower.append({"role": role, "task554_body_sha256": body_sha, "descriptor": descriptor,
                      "full_file_authenticated": True})
    receipts = seal({"schema": SCHEMA + ".packet-receipts", "raw_seeds": raw_seeds, "seeds": seeds,
        "p1_pass": {"manifest_sha256": BASE.P1_MANIFEST_SHA256, "cache_sha256": BASE.P1_CACHE_SHA256,
            "instruction_sha256": BASE.P1_INSTRUCTION_SHA256,
            "instruction_final_head": packet["p1"]["manifest"]["ancestry_sha256"], "rows": 8059,
            "cache_passes": 1, "instruction_passes": 1, "referenced_roots": len(packet["p1_roots"]),
            "arithmetic_rows": packet["arithmetic_rows"]},
        "lower_pass": {"receipts": lower, "full_blob_files": 12, "blob_passes": 12,
            "total_authenticated_bytes": sum(item["bytes"] for item in packet["blobs"])},
        "regression": {"seed2_char0_raw": {"seed": 2, "character": 0,
            "packed_sha256": BASE.SEED2_RAW_PACKED_SHA256, "support": 568,
            "lambda_independent": True, "scalar_assertion_retired": True},
            "saved_sources": [{"seed": seed, "character": 0, "bytes": SOURCE_BYTES,
                               "sha256": sha(pack(packet["tops"][seed, 0]))} for seed in (30, 34)]},
        "premises": {"complete_defect_lower_zero_executed": True, "v453_direct_slice_after_complete_lower_zero": True,
            "structural_slicing_retained_as_premise": True, "word_projector_replayed": False,
            "projector_order": [list(label) for label in LEGACY.CHARACTERS], "projectors": projector_records()}})
    payloads = {"tops.bin": packet["tops_raw"], "relations.json": canonical(relations),
                "p1-roots.json": canonical(roots), "receipts.json": canonical(receipts)}
    manifest = seal({"schema": SCHEMA + ".packet-manifest", "owner_sha256": owner_sha,
        "files": [file_receipt(name, raw) for name, raw in sorted(payloads.items())],
        "file_roster": sorted([*payloads, "manifest.json"]),
        "candidate": True, "cross_checked": False, "verified": False})
    packet.update({"relation_certificate": relations, "roots_certificate": roots,
                   "receipt_certificate": receipts, "manifest": manifest})
    return payloads, manifest


def producer_source_receipt() -> dict[str, Any]:
    directory = Path(__file__).resolve().parent
    for name, expected in PRODUCER_LINEAGE.items():
        item = directory / name
        require(not item.is_symlink() and sha(item.read_bytes()) == expected, "producer_source_metadata_pin")
    producer = directory / "d972_r07_fixed_root_packet_loop_v2.py"
    require(producer.is_file() and not producer.is_symlink(), "producer_source_metadata_file")
    return seal({"schema": SCHEMA + ".source", "producer_sha256": sha(producer.read_bytes()),
                 "modules": PRODUCER_LINEAGE, "data": DATA_PINS,
                 "python": sys.version, "numpy": np.__version__})


def compare_directory(root: Path, payloads: dict[str, bytes], manifest: dict[str, Any]) -> str:
    expected = {**payloads, "manifest.json": canonical(manifest)}
    require(root.is_dir() and not root.is_symlink() and
            sorted(item.name for item in root.iterdir()) == sorted(expected), "exact_directory_roster")
    for name, raw in expected.items():
        require(fixed(root, name, (len(raw), sha(raw))) == raw, "independent_payload:" + name)
    return sha(expected["manifest.json"])


def audit_steps_directory(root: Path, completed: int) -> None:
    if not root.exists():
        require(completed == 0, "missing_committed_steps")
        return
    require(root.is_dir() and not root.is_symlink(), "steps_directory")
    for item in root.iterdir():
        require(item.is_dir() and not item.is_symlink(), "step_directory_kind")
        if re.fullmatch(r"\.(?:pending|orphan)-[0-9]{6}-[A-Za-z0-9-]+", item.name):
            continue
        require(re.fullmatch(r"[0-9]{6}", item.name) is not None and int(item.name) > 0,
                "step_directory_name")
        # Numbered directories beyond HEAD also remain uncommitted tails.
    for step in range(1, completed + 1):
        require((root / f"{step:06d}").is_dir(), "missing_committed_step")


def terminal_for_state(kind: str, target: np.ndarray, scan: dict[str, Any] | None,
                       declared: str | None) -> str:
    if kind == "Member":
        require(not np.any(target) and scan is None, "member_target_zero")
        return "MEMBER_CANDIDATE"
    require(kind == "Separator" and np.any(target) and scan is not None, "separator_target_nonzero")
    if scan["first_hit"] is None:
        return "ROOT_SEEDS_ZERO"
    require(declared in ("UNKNOWN_CAP", "UNKNOWN_RESOURCE"), "nonzero_root_cannot_claim_empty")
    return declared


def read_candidate_json(root: Path, name: str, cap: int = 32 << 20) -> dict[str, Any]:
    item = path(root, name)
    require(item.stat().st_size <= cap, "json_size_cap:" + name)
    value = json_bytes(item.read_bytes())
    require(isinstance(value, dict), "candidate_json_object")
    return value


def scan_certificate(tables: list[Any], tops: np.ndarray, functional: np.ndarray,
                     completed: int, state_head: str) -> dict[str, Any]:
    q, values = evaluate_roots(tables, tops, functional)
    nonzero_blocks = [character for character, root in enumerate(q) if np.any(root)]
    first_index = next((index for index, value in enumerate(values) if value), None)
    selected = None if first_index is None else {"character": first_index // 44, "seed": first_index % 44,
                                               "index": first_index, "scalar": values[first_index]}
    return seal({"schema": SCHEMA + ".root-scan", "generation": START_GENERATION + completed,
        "rank": START_RANK + completed, "state_head": state_head, "lambda_sha256": sha(pack(functional)),
        "roots": [{"character": a, "support": int(np.count_nonzero(root)), "packed_sha256": sha(pack(root)),
                   "B_adj_identity": tables[a]["identity"]["adjoint:B"]} for a, root in enumerate(q)],
        "values": [values[a * 44:(a + 1) * 44] for a in range(4)], "declared_pair_count": 176,
        "nonzero_root_blocks": nonzero_blocks, "nonzero_root_block_count": len(nonzero_blocks),
        "informative_pair_count": 44 * len(nonzero_blocks),
        "nonzero_pair_count": sum(value != 0 for value in values), "first_hit": selected})


def literal_certificate(packet: dict[str, Any], table: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any]:
    seed, character = selection["seed"], selection["character"]
    relation = packet["relation_certificate"]["seeds"][seed]
    return {"defect_operation": "ordered-product", "seed": seed,
        "seed_relation_sha256": relation["sha256"],
        "p1_roots_sha256": sha(canonical(packet["roots_certificate"])),
        "compact_word_sha256": sha(canonical(packet["compact_words"][seed])),
        "p1_factor_order": "event_id-ascending", "p1_exponent_rule": "(3-coefficient)%3",
        "literal_coefficient_collection": False, "character": character,
        "projector_receipt_sha256": sha(canonical(packet["receipt_certificate"]["premises"]["projectors"][character])),
        "actor_path": [], "forward_B": table["identity"]["forward:B"],
        "source_d_sha256": sha(pack(packet["tops"][seed, character])),
        "parent_state_ancestry_premise": True, "normalized_exponent_pair": "NOT_REPLAYED",
        "eleven_slot_replay": False, "full_A0_witness": False, "grade2_positive_terminal_complete": False}


def rebuild_step(packet: dict[str, Any], tables: list[Any], start: dict[str, Any], owner_sha: str,
                 packet_sha: str, step: int, current_head: str, previous_manifest_sha: str | None,
                 current_target: np.ndarray, functional: np.ndarray, pivots: list[Any],
                 row_reader: Callable[[int], bytes]) -> dict[str, Any]:
    scan = scan_certificate(tables, packet["tops"], functional, step - 1, current_head)
    selection = scan["first_hit"]
    require(selection is not None, "prefix_after_ROOT_SEEDS_ZERO")
    character, seed, scalar = selection["character"], selection["seed"], selection["scalar"]
    raw = pushforward(tables[character]["entries"], packet["tops"][seed, character])
    require(dot(functional, raw) == scalar, "selected_forward_adjoint_pairing")
    remainder, reductions = LEGACY.reduce_dense(raw, pivots, row_reader)
    normalized, lead, scale = LEGACY.normalize(remainder)
    require(lead not in {item["lead"] for item in pivots} and dot(functional, remainder) == scalar and
            dot(functional, normalized) == scalar * scale % 3, "append_rank_gate")
    updated, target_scalar = LEGACY.next_target(current_target, normalized, lead, [item["lead"] for item in pivots])
    old_rank, old_generation = START_RANK + step - 1, START_GENERATION + step - 1
    require(len(pivots) == old_rank, "append_prefix_rank")
    rows = {"physical-raw.bin": pack(raw), "physical-remainder.bin": pack(remainder),
            "physical-normalized.bin": pack(normalized), "target-remainder.bin": pack(updated)}
    instruction_body = {"schema": SCHEMA + ".instruction", "step": step, "predecessor": current_head,
        "offer": old_generation, "generation": old_generation + 1, "rank": old_rank + 1,
        "lead": lead, "sigma": scale, "physical_offset": old_rank * ROW_BYTES, "selected": selection,
        "packet_manifest_sha256": packet_sha,
        "relation_sha256": packet["relation_certificate"]["seeds"][seed]["sha256"],
        "p1_roots_sha256": sha(canonical(packet["roots_certificate"])),
        "physical_reductions": reductions, "physical_sha256": sha(rows["physical-normalized.bin"]),
        "target_scalar": target_scalar, "target_remainder_sha256": sha(rows["target-remainder.bin"])}
    new_head = sha(bytes.fromhex(current_head) + canonical(instruction_body))
    instruction = {**instruction_body, "rolling_sha256": new_head}
    kind, separator, next_functional = "Member", None, None
    if np.any(updated):
        kind = "Separator"
        reverse = LEGACY.next_separator(updated, pivots, normalized, lead, row_reader, old_generation)
        next_functional = reverse["lambda"]
        # The final sweep is executed by next_separator, then both directly
        # available target remainders are independently paired here.
        require(dot(next_functional, updated) == dot(next_functional, current_target) == 1,
                "final_separator_direct_targets")
        rows["lambda.bin"] = pack(next_functional)
        separator = {"free_coordinate": reverse["free_coordinate"], "free_value": reverse["free_value"],
            "lambda_sha256": sha(rows["lambda.bin"]),
            "direct_pairing": {"rows": old_rank + 1, "row_pairings_sha256": sha(b"\0" * (old_rank + 1)),
                "lambda_pivots": 0, "lambda_parent_remainder": 1, "lambda_new_remainder": 1},
            "lambda_rho2": rho2_derivation(start, step)}
    literal = literal_certificate(packet, tables[character], selection)
    result = seal({"schema": SCHEMA + ".step-result", "step": step, "kind": kind,
        "owner_sha256": owner_sha, "packet_manifest_sha256": packet_sha,
        "parent_state_head": current_head, "state_head": new_head,
        "rank_before": old_rank, "rank_after": old_rank + 1,
        "generation_before": old_generation, "generation_after": old_generation + 1,
        "selection": selection, "scan": scan, "pairings": {"q_d": scalar, "lambda_G": scalar},
        "pivot": {"lead": lead, "scale": scale, "reductions": reductions,
                  "normalized_sha256": sha(rows["physical-normalized.bin"])},
        "target": {"parent_remainder_sha256": sha(pack(current_target)),
                   "remainder_sha256": sha(rows["target-remainder.bin"]), "scalar": target_scalar},
        "separator": separator, "literal": literal, "candidate": True, "cross_checked": False, "verified": False})
    payloads = {**rows, "instruction.json": canonical(instruction), "result.json": canonical(result)}
    manifest = seal({"schema": SCHEMA + ".step-manifest", "step": step, "owner_sha256": owner_sha,
        "packet_manifest_sha256": packet_sha, "predecessor_step_manifest_sha256": previous_manifest_sha,
        "parent_state_head": current_head, "state_head": new_head, "rank": old_rank + 1,
        "generation": old_generation + 1, "kind": kind,
        "files": [file_receipt(name, data) for name, data in sorted(payloads.items())],
        "file_roster": sorted([*payloads, "manifest.json"]), "candidate": True,
        "cross_checked": False, "verified": False})
    progress("prefix_step_rebuilt", step=step, character=character, seed=seed, rank=old_rank + 1, kind=kind)
    return {"payloads": payloads, "manifest": manifest, "head": new_head, "target": updated,
            "lambda": next_functional, "kind": kind, "normalized": rows["physical-normalized.bin"],
            "pivot": {"offer": old_generation, "lead": lead, "physical_offset": old_rank * ROW_BYTES,
                      "coefficient_offset": None, "rolling_sha256": new_head}}


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    global REPLAYED_STEPS
    root = args.candidate_root
    require(root.is_dir() and not root.is_symlink(), "candidate_root")
    entries = list(root.iterdir())
    diagnostic_names = set()
    for item in entries:
        if item.name == "resource-stop.json":
            require(item.is_file() and not item.is_symlink(), "resource_diagnostic_file")
            diagnostic_names.add(item.name)
        elif re.fullmatch(r"\.packet-pending-[A-Za-z0-9-]+", item.name):
            require(item.is_dir() and not item.is_symlink(), "packet_diagnostic_directory")
            diagnostic_names.add(item.name)
        elif re.fullmatch(r"\.(?:HEAD|owner\.json|start\.json|source\.json|result\.json|resource-stop\.json)\.pending-[A-Za-z0-9-]+", item.name):
            require(item.is_file() and not item.is_symlink(), "atomic_diagnostic_file")
            diagnostic_names.add(item.name)
    require(set(item.name for item in entries) - diagnostic_names in
            ({"HEAD", "owner.json", "start.json", "source.json", "packet", "steps", "result.json"},
             {"HEAD", "owner.json", "start.json", "source.json", "packet", "result.json"}), "candidate_top_roster")
    candidate_head = read_candidate_json(root, "HEAD", 1 << 20)
    check_seal(candidate_head)
    completed = candidate_head.get("completed_steps")
    require(type(completed) is int and 0 <= completed <= MAX_APPENDS, "bounded_complete_prefix")
    source = producer_source_receipt()
    same(read_candidate_json(root, "source.json"), source, "source_runtime_freeze")
    state = load_start(args)
    tables = load_tables(args)
    owner, start = expected_owner(state, tables), expected_start(state)
    same(read_candidate_json(root, "owner.json"), owner, "fixed_owner")
    same(read_candidate_json(root, "start.json"), start, "fixed_start")
    owner_sha, start_sha = sha(canonical(owner)), sha(canonical(start))
    require(candidate_head["owner_sha256"] == owner_sha and candidate_head["start_sha256"] == start_sha and
            candidate_head["producer_sha256"] == source["producer_sha256"], "head_owner_start_source")
    packet = rebuild_packet(args, state)
    payloads, manifest = packet_payloads(packet, owner_sha)
    packet_sha = compare_directory(root / "packet", payloads, manifest)
    require(candidate_head["packet_manifest_sha256"] == packet_sha, "head_packet_join")
    progress("packet_independent_comparison", status="PASS", seeds=44, lower_coordinates_per_seed=96776)
    current_target, functional = state["start_target"], state["start_lambda"]
    current_head, previous_manifest_sha, kind = START_HEAD, None, "Separator"
    pivots, saved_rows = list(state["pivots"]), list(state["saved_rows"])
    steps_root = root / "steps"
    audit_steps_directory(steps_root, completed)
    with path(args.state_root, "state/physical.bin").open("rb", buffering=1 << 20) as stream:
        def read_pivot(index: int) -> bytes:
            require(0 <= index < len(pivots), "pivot_index")
            return LEGACY.blob_row(stream, index, WIDTH) if index < 1354 else saved_rows[index - 1354]
        for step in range(1, completed + 1):
            require(kind == "Separator" and functional is not None, "prefix_after_MEMBER_CANDIDATE")
            rebuilt = rebuild_step(packet, tables, start, owner_sha, packet_sha, step, current_head,
                                   previous_manifest_sha, current_target, functional, pivots, read_pivot)
            previous_manifest_sha = compare_directory(steps_root / f"{step:06d}",
                                                       rebuilt["payloads"], rebuilt["manifest"])
            REPLAYED_STEPS = step
            current_head, current_target = rebuilt["head"], rebuilt["target"]
            functional, kind = rebuilt["lambda"], rebuilt["kind"]
            pivots.append(rebuilt["pivot"])
            saved_rows.append(rebuilt["normalized"])
    expected_head = seal({"schema": SCHEMA + ".head", "owner_sha256": owner_sha,
        "producer_sha256": source["producer_sha256"], "packet_manifest_sha256": packet_sha,
        "start_sha256": start_sha, "completed_steps": completed, "step_manifest_sha256": previous_manifest_sha,
        "rank": START_RANK + completed, "generation": START_GENERATION + completed,
        "state_head": current_head, "kind": kind})
    same(candidate_head, expected_head, "complete_prefix_head")
    actual_result = read_candidate_json(root, "result.json")
    scan = None if kind == "Member" else scan_certificate(tables, packet["tops"], functional, completed, current_head)
    terminal = terminal_for_state(kind, current_target, scan, actual_result.get("terminal"))
    result = seal({"schema": SCHEMA + ".result", "status": "PASS", "terminal": terminal,
        "head_sha256": sha(canonical(expected_head)), "packet_manifest_sha256": packet_sha,
        "owner_sha256": owner_sha, "completed_steps": completed, "rank": START_RANK + completed,
        "generation": START_GENERATION + completed, "state_head": current_head, "scan": scan,
        "lambda_rho2": None if kind == "Member" else rho2_derivation(start, completed),
        "scope": SCOPE, "claims": CLAIMS, "candidate": True, "cross_checked": False, "verified": False})
    same(actual_result, result, "terminal_after_fresh_root_scan")
    progress("terminal", status="PASS", terminal=terminal, step=completed, rank=START_RANK + completed)
    return {"schema": SCHEMA + ".checker-result", "status": "PASS", "terminal": terminal,
        "completed_steps": completed, "rank": START_RANK + completed, "generation": START_GENERATION + completed,
        "state_head": current_head, "head_sha256": sha(canonical(expected_head)),
        "packet_manifest_sha256": packet_sha, "result_sha256": sha(canonical(result)),
        "owner_sha256": owner_sha, "packet_independently_rebuilt": True, "prefix_steps_replayed": completed,
        "raw_seeds_evaluated": 44, "lower_coordinates_per_seed": 96776, "declared_pair_count": 176,
        "nonzero_root_blocks": None if scan is None else scan["nonzero_root_blocks"],
        "informative_pair_count": None if scan is None else scan["informative_pair_count"],
        "lambda_rho2": result["lambda_rho2"], "checker_lineage": LINEAGE,
        "source_data_pins": DATA_PINS,
        "old_state_derivation_premise": True, "accepted_target_derivation_parents": start["accepted_target_derivation_parents"],
        "claims": CLAIMS, "candidate": True, "cross_checked": False, "verified": False}


def reject_test(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError("fixed_packet_checker:canary_not_rejected:" + label)


def selftest() -> dict[str, Any]:
    """Four changed-interface canaries; no historical source or raw-seed run."""
    states = [{"expressions": [[], [], [], []], "body_sha256": str(index) * 64} for index in range(5)]
    states[0]["expressions"][0] = [[1, 1], [1, 2], [0, 2]]
    events, final = LEGACY.combined_selected(states, 3)
    require(len(events) == 3 and final == [[0, 2]] and
            {event["global_index"] for event in events} == {0, 1}, "cancelled_literal_root_preserved")
    target_parents = {"base_target": {"reductions": []}, "old_target": {"new_reductions": []},
                      "parent_layout": {"fixture_only": True},
                      "seed34": {"result": {"target": {"new_reductions": [[1355, 1]]}}}}
    start = expected_start(target_parents)
    check_seal(start)
    require(start["rank"] == 1356 and start["generation"] == 8061 and start["state_head"] == START_HEAD and
            [parent["role"] for parent in start["accepted_target_derivation_parents"]] == ["base", "seed30", "seed34"],
            "actual_start_shape")
    derivation = rho2_derivation(start, 2)
    require(derivation["mode"] == "derived" and derivation["original_rho2_directly_read"] is False and
            derivation["newly_executed_target_steps"] == 2 and
            derivation["accepted_target_derivation_parents"][2]["target_sha256"] ==
            sha(canonical(target_parents["seed34"]["result"]["target"])), "derived_target_parent_binding")
    reject_test(lambda: check_seal({**start, "rank": 1355}), "stale_start_rank")
    tops = np.zeros((44, 4, SOURCE_WIDTH), dtype=np.uint8)
    tops[43, 1, 0], tops[0, 2, 0] = 1, 2
    tables = [{"entries": np.array([[0, a, 1]], dtype=np.int64),
               "identity": {"adjoint:B": f"fixture-B{a}"}} for a in range(4)]
    functional = np.zeros(WIDTH, dtype=np.uint8)
    functional[1] = 1
    scan1 = scan_certificate(tables, tops, functional, 0, START_HEAD)
    functional[1], functional[2] = 0, 1
    scan2 = scan_certificate(tables, tops, functional, 1, "a" * 64)
    require(scan1["first_hit"]["index"] == 87 and scan1["nonzero_root_blocks"] == [1] and
            scan2["first_hit"]["index"] == 88 and scan2["nonzero_root_blocks"] == [2] and
            scan2["declared_pair_count"] == 176 and scan2["informative_pair_count"] == 44,
            "fresh_all_four_root_order")
    require(terminal_for_state("Separator", functional, scan2, "UNKNOWN_CAP") == "UNKNOWN_CAP", "nonempty_cap")
    reject_test(lambda: terminal_for_state("Separator", functional, scan2, "ROOT_SEEDS_ZERO"), "cap_not_empty")
    empty_components = [LEGACY.component_receipt(name, part) for name, part in zip(("d0", "d1", "d2", "aux"),
        (np.zeros((4, 6048), dtype=np.uint8), np.zeros((4, 18144), dtype=np.uint8),
         np.zeros((4, SOURCE_WIDTH), dtype=np.uint8), np.zeros(8, dtype=np.uint8)))]
    packet = {"tops": tops, "tops_raw": b"".join(pack(tops[s, a]) for a in range(4) for s in range(44)),
        "relations": [{"seed": s, "events": events if s == 3 else [], "coefficients": final if s == 3 else []}
                      for s in range(44)], "p1_roots": [], "raw_receipts": [empty_components] * 44,
        "reduced_receipts": [empty_components] * 44, "compact_words": [[] for _ in range(44)],
        "blobs": [item for pair in BASE.OLD_BLOB_PINS for item in pair] + list(BASE.NEW_BLOB_PINS),
        "p1": {"manifest": {"ancestry_sha256": "b" * 64}}, "arithmetic_rows": 1}
    payloads, manifest = packet_payloads(packet, "c" * 64)
    with tempfile.TemporaryDirectory(prefix="fixed-packet-checker-canary-") as directory:
        root = Path(directory)
        for name, raw in {**payloads, "manifest.json": canonical(manifest)}.items():
            (root / name).write_bytes(raw)
        compare_directory(root, payloads, manifest)
        # A self-consistent forged packet manifest is not arithmetic authority.
        damaged = dict(payloads)
        damaged["tops.bin"] = bytes([1]) + payloads["tops.bin"][1:]
        changed_manifest = seal({**{key: value for key, value in manifest.items() if key != "sha256"},
            "files": [file_receipt(name, raw) for name, raw in sorted(damaged.items())]})
        (root / "tops.bin").write_bytes(damaged["tops.bin"])
        (root / "manifest.json").write_bytes(canonical(changed_manifest))
        reject_test(lambda: compare_directory(root, payloads, manifest), "resealed_packet_corruption")
        steps = root / "steps"
        steps.mkdir()
        for name in ("000001", "000002", ".pending-000002-a", ".orphan-000002-b"):
            (steps / name).mkdir()
        audit_steps_directory(steps, 1)
        reject_test(lambda: audit_steps_directory(steps, 3), "missing_committed_prefix")
    return {"schema": SCHEMA + ".checker-selftest", "status": "PASS", "canaries": 4,
            "interfaces": ["ordered-relation-and-start-derived-parents", "fresh-four-roots-and-cap",
                           "packet-exact-bytes-resealed-rejection", "committed-prefix-and-diagnostic-tails"],
            "fixture_only": True, "cross_checked": False, "verified": False}


def main() -> int:
    global DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("state-root", "delta-root", "seed34-root", "prepare-root", "p1-root", "task712-root", "candidate-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-seconds", type=float, default=1800)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--parent-layout-selftest", action="store_true")
    args = parser.parse_args()
    try:
        require(not (args.selftest and args.parent_layout_selftest), "exclusive_selftest_modes")
        if args.parent_layout_selftest:
            require(all(getattr(args, name) is not None for name in ("state_root", "delta_root", "seed34_root")),
                    "actual_parent_layout_arguments")
            result = parent_layout_selftest(args)
        elif args.selftest:
            result = selftest()
        else:
            require(args.max_seconds > 0 and np.isfinite(args.max_seconds), "positive_resource_deadline")
            DEADLINE = time.monotonic() + args.max_seconds
            require(all(getattr(args, name) is not None for name in
                        ("state_root", "delta_root", "seed34_root", "prepare_root", "p1_root", "task712_root", "candidate_root"))
                    and len(args.block_root) == 4, "actual_parent_arguments")
            result = check_actual(args)
        raw = canonical(result)
        if args.output:
            args.output.write_bytes(raw)
        sys.stdout.buffer.write(raw)
        return 0
    except ResourceStop as error:
        result = {"schema": SCHEMA + ".checker-result", "status": "UNKNOWN", "terminal": "UNKNOWN_RESOURCE",
            "phase": str(error), "prefix_steps_replayed": REPLAYED_STEPS,
            "elapsed_seconds": round(time.monotonic() - BEGIN, 3), "max_seconds": args.max_seconds,
            "candidate_accepted": False, "producer_complete_prefix_preserved": True,
            "cross_checked": False, "verified": False}
        raw = canonical(result)
        if args.output:
            args.output.write_bytes(raw)
        sys.stdout.buffer.write(raw)
        return 2
    except Exception as error:
        failure = {"schema": SCHEMA + ".checker-result", "status": "FAIL", "error": str(error),
                   "cross_checked": False, "verified": False}
        raw = canonical(failure)
        if args.output:
            args.output.write_bytes(raw)
        sys.stdout.buffer.write(raw)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
