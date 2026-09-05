#!/usr/bin/env python3
"""Task941: fixed current root seed, one rank1355 -> rank1356 candidate delta.

Adapted from the accepted seed30 checker without importing producer math.
The old state and seed30 delta derivations remain authenticated premises.
Only selected P1 support is replayed; no actors, old target solve or rho2 IO.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable

import numpy as np

SCHEMA = "d972.r07.actual-root-seed-materializer.v3"
WIDTH, ROW_BYTES, LOWER_WIDTH = 48384, 12096, 96776
OLD_OFFSETS = (0, 505, 1008, 1511)
NEW_OFFSETS = (2014, 3523, 5035, 6547)
ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
FORMULA = "r07.v541.formulas-2.1-2.2-4.1.raw-seed-plus-actor-lower-adjoint"
OLD_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"
CURRENT_HEAD = "36feb776736c6587ce9f64d6f5acb883385074a7cc2eed4c2ce7eb8675e71342"
CURRENT_LAMBDA = "f83bbaa503b8a4d5056f0779085ee4eced542eb1d78d3e35fa9df1c281960565"
CURRENT_REMAINDER = "f5040e3f29b42e71b86be047d40de5d538ddb7fc107cace219879bbc67238d3a"
ADAPTED_CHECKER = {"file": "check_d972_r07_actual_seed30_materializer_v1.py",
    "sha256": "f4f8ba2d342cb60e2c70b708b8847768a78ebde40dd0a52879f460cb558eab36"}
SOURCE_PINS = {
    "check_d972_r07_actual_grade2_root_scalar_batch_v2.py": "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6",
    "check_d972_r07_targeted_grade2_owner_generated_join_v15.py": "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662",
    "check_d972_r07_rank1355_root_seed_scalars_v1.py": "f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62",
}
for _name, _wanted in SOURCE_PINS.items():
    _file = Path(__file__).resolve().parent / _name
    if _file.is_symlink() or hashlib.sha256(_file.read_bytes()).hexdigest() != _wanted:
        raise ValueError("root_seed_v3_checker:source_pin:" + _name)
import check_d972_r07_actual_grade2_root_scalar_batch_v2 as BASE
# Only the successful fixed delta reader is called, never its scalar path.
import check_d972_r07_rank1355_root_seed_scalars_v1 as ROOTS

SCALAR_ARTIFACT = {
    "run": 33954712636, "attempt": 1, "head": "92c98486ab659f7e3358fc3c4afb53ab6b78293d",
    "id": 9966008518, "name": "d972-r07-rank1355-root-seed-scalars-v1-candidate-33954712636-1",
    "bytes": 31781, "sha256": "sha256:148b028ec8b17543a85a563a8d0275fc93361168adda85d8147cd1dbc41207b3",
}
SCALAR_FILES = {
    "output/manifest.json": (3204, "f60e9aa4d99d7c1a89512550314c3995d389b96b87e7a788b9d4e390572aed88"),
    "output/result.json": (36195, "02a814c5a7a2129302deca997fa3a5fb54982237c75b28e47da6205145cf07ea"),
    "checker-result.json": (2370, "46d7f1800977493ffb0e350dc5d0f52cc2464a4fde57c6b89718b93f29be0b48"),
    "source-receipt.json": (1128, "103a9e5d9ca67c9c6af2a10905dadf25ac0c94f02d58891fdf8196e0ac85b99e"),
}
STATE_FILES = {
    **ROOTS.STATE_FILES,
    "state/physical.bin": (16377984, "1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e"),
    "state/physical-p1-coeff.bin": (2728310, "a2d462ea6c8685a59e28f3f5d1c89656e2e942a65110a21184e33c6cb334826c"),
    "state/instructions.jsonl": (86919157, "a7cbe317ba92b0d4076623dfd5ea672d2ef4b154f5be2862e0dc232ba91309c2"),
}
CLAIMS = {
    "ACTUAL_ROOT_SEED_MATERIALIZATION_CANDIDATE": True,
    "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
    "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
    "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False,
}


def require(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError("root_seed_v3_checker:" + why)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(body: dict[str, Any]) -> dict[str, Any]:
    require("sha256" not in body, "double_seal")
    return {**body, "sha256": sha(canonical(body))}


def check_seal(value: Any) -> None:
    require(isinstance(value, dict) and "sha256" in value, "sealed_object")
    require(value == seal({k: v for k, v in value.items() if k != "sha256"}), "seal")


def same(actual: Any, expected: Any, reason: str) -> None:
    # Unlike Python equality, canonical bytes distinguish true from 1.
    require(canonical(actual) == canonical(expected), reason)


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def path(root: Path, name: str) -> Path:
    require(isinstance(name, str) and name and not Path(name).is_absolute() and
            ".." not in Path(name).parts and ":" not in name and "\\" not in name, "relative_path")
    root = root.resolve()
    candidate = root / name
    cursor = root
    for part in Path(name).parts:
        cursor /= part
        require(not cursor.is_symlink(), "symlink")
    require(candidate.is_file() and root in candidate.resolve().parents, "missing_or_escape")
    return candidate


def fixed(root: Path, name: str, identity: tuple[int, str]) -> bytes:
    item = path(root, name)
    require(item.stat().st_size == identity[0], "fixed_size:" + name)
    raw = item.read_bytes()
    fixed_bytes(raw, identity, name)
    return raw


def fixed_bytes(raw: bytes, identity: tuple[int, str], name: str) -> None:
    require(len(raw) == identity[0] and sha(raw) == identity[1], "fixed_hash:" + name)


def fixed_stream(root: Path, name: str, identity: tuple[int, str], packed: bool = False) -> None:
    item = path(root, name)
    require(item.stat().st_size == identity[0], "stream_size:" + name)
    digest = hashlib.sha256()
    count = 0
    with item.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
            count += len(chunk)
            if packed:
                require(not np.any(np.frombuffer(chunk, dtype=np.uint8) > 80), "packed_byte:" + name)
    require(count == identity[0] and digest.hexdigest() == identity[1], "stream_hash:" + name)


def json_bytes(raw: bytes, *, canonical_required: bool = True) -> Any:
    value = json.loads(raw.decode("ascii"))
    require(not canonical_required or canonical(value) == raw, "canonical_json")
    return value


def unpack(raw: bytes, width: int) -> np.ndarray:
    values = np.frombuffer(raw, dtype=np.uint8)
    require(len(raw) == (width + 3) // 4 and not np.any(values > 80), "packed_shape")
    decoded = ((values[:, None].astype(np.uint16) // np.array([1, 3, 9, 27], dtype=np.uint16)) % 3).reshape(-1)
    require(not np.any(decoded[width:]), "packed_padding")
    return decoded[:width].astype(np.uint8)


def pack(values: np.ndarray) -> bytes:
    vector = np.asarray(values).reshape(-1)
    require(not np.any(vector > 2) and not np.any(vector < 0), "trit_vector")
    padded = np.zeros((len(vector) + 3) // 4 * 4, dtype=np.uint16)
    padded[:len(vector)] = vector
    return (padded.reshape(-1, 4) @ np.array([1, 3, 9, 27], dtype=np.uint16)).astype(np.uint8).tobytes()


def dot(left: np.ndarray, right: np.ndarray) -> int:
    require(left.shape == right.shape, "dot_dimensions")
    return int(np.sum(left.astype(np.uint64) * right.astype(np.uint64), dtype=np.uint64) % 3)


def subtract(destination: np.ndarray, source: np.ndarray, coefficient: int) -> None:
    require(coefficient in (1, 2) and destination.shape == source.shape, "subtract_shape")
    destination[:] = (destination.astype(np.int16) - coefficient * source.astype(np.int16)) % 3


def blob_row(stream: Any, row: int, width: int) -> bytes:
    size = (width + 3) // 4
    stream.seek(row * size)
    raw = stream.read(size)
    require(len(raw) == size, "positioned_eof")
    return raw


def load_scalar(args: argparse.Namespace) -> dict[str, Any]:
    progress("parent_loading", parent="current_rank1355_root_scalars")
    objects = {name: json_bytes(fixed(args.scalar_root, name, identity))
               for name, identity in SCALAR_FILES.items()}
    manifest, result = objects["output/manifest.json"], objects["output/result.json"]
    checker, source = objects["checker-result.json"], objects["source-receipt.json"]
    for item in (manifest, result):
        check_seal(item)
    require(manifest["schema"] == ROOTS.SCHEMA + ".manifest" and
            manifest["candidate"] is True and result["status"] == checker["status"] == "PASS" and
            result["terminal"] == checker["terminal"] == "ROOT_SEED_VIOLATION" and
            checker["manifest_sha256"] == SCALAR_FILES["output/manifest.json"][1] and
            checker["result_sha256"] == SCALAR_FILES["output/result.json"][1] and
            all(item["verified"] is False and item["cross_checked"] is False
                for item in (manifest, result, checker, source)), "scalar_authority")
    for item in (result, checker):
        ROOTS.current_identity(item["separator_generation"], item["separator_rank"],
                               item["separator_head"], item["lambda_sha256"])
        require(item["actor_origins_executed"] == item["orbit_rows_executed"] == 0 and
                item["materialization_performed"] is False, "root_only_authority")
    require(checker["old_state_rows_checked"] == 1354 and checker["new_pivot_rows_checked"] == 1 and
            checker["lambda_pivots"] == 0 and checker["lambda_saved_remainder"] == 1,
            "current_allrows_checker_premise")
    output = args.scalar_root / "output"
    payloads = {item["file"]: fixed(output, item["file"], (item["bytes"], item["sha256"]))
                for item in manifest["files"]}
    require(sorted(item.name for item in output.iterdir()) == manifest["file_roster"] ==
            sorted([*payloads, "manifest.json"]), "scalar_roster")
    launch = json_bytes(payloads["launch.json"])
    check_seal(launch)
    require(sha(payloads["launch.json"]) == result["launch_sha256"] and
            launch["fixture_only"] is False and launch["verified"] is False and
            launch["cross_checked"] is False and launch["lineages"] == ROOTS.LINEAGES and
            launch["scope"] == result["scope"] == ROOTS.SCOPE,
            "current_launch_identity")
    source_files = {item["file"]: item["sha256"] for item in source["files"]}
    require(source_files["search/d972_r07_rank1355_root_seed_scalars_v1.py"] ==
            "973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb" and
            source_files["search/check_d972_r07_rank1355_root_seed_scalars_v1.py"] ==
            SOURCE_PINS["check_d972_r07_rank1355_root_seed_scalars_v1.py"], "scalar_source_identity")
    records, rolling = [], "0" * 64
    for index, line in enumerate(payloads["scalars.jsonl"].splitlines(keepends=True)):
        record = json_bytes(line)
        a, seed = divmod(index, 44)
        require(index < 176 and record["index"] == index and record["character"] == a and
                record["seed"] == record["origin_id"] == seed and record["origin_kind"] == "seed" and
                type(record["scalar"]) is int and record["scalar"] in (0, 1, 2), "scalar_stream_order")
        rolling = sha(bytes.fromhex(rolling) + canonical({key: value for key, value in record.items()
                                                        if key != "rolling_sha256"}))
        require(record["rolling_sha256"] == rolling and
                record["raw_dual_sha256"] == result["characters"][a]["raw_dual"]["sha256"] and
                record["scalar"] == payloads[f"seed-scalars-a{a}.bin"][seed], "scalar_stream_join")
        records.append(record)
    require(len(records) == checker["scalars"] == 176 and rolling == result["scalar_final_head"], "scalar_eof")
    first = next((record for record in records if record["scalar"]), None)
    require(first is not None, "selected_nonzero_root")
    violation = result["first_violation"]
    check_seal(violation)
    same(violation, checker["first_violation"], "checker_selected_violation")
    same({key: violation[key] for key in first}, first, "first_selected_record")
    a, seed, value = first["character"], first["seed"], first["scalar"]
    character = result["characters"][a]
    dual, relation = character["raw_dual"], result["relation_receipt"]["seed_records"][seed]
    for item in (character, dual, character["direct_receipt"], result["relation_receipt"], relation):
        check_seal(item)
    ROOTS.fresh_raw_identity(dual)
    require(violation["separator_generation"] == 8060 and violation["separator_head"] == CURRENT_HEAD and
            violation["lambda_sha256"] == CURRENT_LAMBDA and violation["delta_manifest_sha256"] ==
            ROOTS.DELTA_FILES["output/manifest.json"][1] and relation["seed"] == seed and
            violation["seed_relation_sha256"] == relation["sha256"] and
            violation["relation_receipt_sha256"] == result["relation_receipt"]["sha256"] and
            result["relation_receipt"]["task554_body_sha256"] == list(BASE.TASK554_BODY_DIGESTS) and
            violation["p1_manifest_sha256"] == BASE.P1_MANIFEST_SHA256 and
            violation["direct_receipt_sha256"] == character["direct_receipt"]["sha256"],
            "selected_root_relation_identity")
    q_raw, values_raw = payloads[f"q-a{a}-root.bin"], payloads[f"p1-values-a{a}.bin"]
    require(len(values_raw) == 8059 and max(values_raw) <= 2 and
            sha(values_raw) == violation["value_vector_sha256"] == result["cache_receipt"]["value_sha256"][a] and
            sha(q_raw) == dual["raw_q_packed_sha256"] == violation["raw_q_packed_sha256"],
            "current_q_values_identity")
    return {"launch": launch, "launch_receipt": file_receipt("launch.json", payloads["launch.json"]),
        "violation": violation, "source": source, "result": result, "character": character,
        "q": unpack(q_raw, 36288), "seed": seed, "character_id": a, "value": value,
        "relation": relation, "values": np.frombuffer(values_raw, dtype=np.uint8),
        "direct_value": payloads[f"direct-seeds-a{a}.bin"][seed]}


def load_task554(args: argparse.Namespace, launch: dict[str, Any], seed: int) -> list[dict[str, Any]]:
    parent = launch["task554_parent"]
    parent = {**parent, "prepare": {**parent["prepare"], "root": str(args.prepare_root.resolve())},
        "blocks": [{**descriptor, "root": str(root.resolve())}
                   for descriptor, root in zip(parent["blocks"], args.block_root)]}
    BASE.validate_task554(parent)
    parents = [parent["prepare"], *parent["blocks"]]
    roots = [args.prepare_root, *args.block_root]
    require(len(roots) == 5, "five_task554_roots")
    states = []
    for index, (descriptor, root) in enumerate(zip(parents, roots)):
        progress("parent_loading", parent="task554", body=index + 1, total=5)
        state = BASE.state_descriptor({**descriptor, "root": str(root.resolve())}, index - 1)
        # Accepted hashes bind the complete bodies; retain only the selected seed rows.
        # Never hold the four large parsed block bodies simultaneously.
        if index == 0:
            chosen = [item["record"]["seed_reductions"][seed]
                      for item in state["body"]["old_blocks"]]
        else:
            chosen = [state["body"]["origin_reductions"][start + seed]
                      for start, _ in ORIGIN_RANGES]
        states.append({"root": state["root"], "body_sha256": state["body_sha256"],
                       "expressions": chosen})
        del state
    return states


def combined_selected(states: list[dict[str, Any]], seed: int, expected_relation: dict[str, Any] | None = None
                      ) -> tuple[list[dict[str, Any]], list[list[int]]]:
    events: list[dict[str, Any]] = []
    def append(expression: Any, role: str, source: int, target: int | None,
               origin: int, offset: int, bound: int, body_sha: str) -> None:
        require(isinstance(expression, list), "seedred_expression")
        for ordinal, term in enumerate(expression):
            require(isinstance(term, list) and len(term) == 2 and
                    type(term[0]) is int and type(term[1]) is int and
                    0 <= term[0] < bound and term[1] in (1, 2), "seedred_term")
            local, coefficient = term
            index = offset + local
            events.append({"event_id": len(events), "body_role": role,
                "task554_body_sha256": body_sha, "source_character": source,
                "target_character": target, "origin_id": origin, "seed": seed, "term_ordinal": ordinal,
                "local_index": local, "global_index": index, "coefficient": coefficient})
    for source, offset in enumerate(OLD_OFFSETS):
        append(states[0]["expressions"][source], "prepare-old", source, None,
               ORIGIN_RANGES[source][0] + seed,
               offset, (505, 503, 503, 503)[source], states[0]["body_sha256"])
    for target, offset in enumerate(NEW_OFFSETS):
        block = states[target + 1]
        for source in range(4):
            origin = ORIGIN_RANGES[source][0] + seed
            append(block["expressions"][source], "new-block", source, target,
                   origin, offset, (1509, 1512, 1512, 1512)[target], block["body_sha256"])
    rolling = "0" * 64
    for event in events:
        rolling = sha(bytes.fromhex(rolling) + canonical(event))
        event["rolling_sha256"] = rolling
    if expected_relation is not None:
        require(expected_relation["seed"] == seed and expected_relation["raw_event_count"] == len(events) and
                expected_relation["raw_event_head"] == rolling, "selected_scalar_relation_head")
    # Nonabelian ancestry has been retained/sealed before coefficient collection.
    coefficients: dict[int, int] = {}
    for event in events:
        index = event["global_index"]
        coefficients[index] = (coefficients.get(index, 0) + event["coefficient"]) % 3
    final = [[index, value] for index, value in sorted(coefficients.items()) if value]
    return events, final


def p1_roots(args: argparse.Namespace, launch: dict[str, Any], events: list[dict[str, Any]]
             ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    progress("parent_loading", parent="canonical_p1")
    p1 = BASE.validate_p1({**launch["p1_parent"], "root": str(args.p1_root.resolve())})
    selected = {event["global_index"] for event in events}
    digest = hashlib.sha256()
    offset = 0
    ancestry = "0" * 64
    roots = []
    with path(args.p1_root, "instructions.jsonl").open("rb", buffering=1 << 20) as stream:
        for index in range(8059):
            line = stream.readline()
            require(line.endswith(b"\n"), "p1_instruction_eof")
            digest.update(line)
            item = json_bytes(line)
            require(item["node"] == index and item["offset"] == index * 36288 and
                    item["length"] == 36288 and item["predecessor"] == ancestry, "p1_instruction_order")
            require(item["ancestry_sha256"] == sha(bytes.fromhex(ancestry) +
                    canonical({k: v for k, v in item.items() if k != "ancestry_sha256"})), "p1_instruction_rolling")
            ancestry = item["ancestry_sha256"]
            if index in selected:
                require(item["row_receipt"]["offset"] == index * 36288 and
                        item["row_receipt"]["length"] == 36288, "p1_selected_position")
                roots.append({"node": index, "instruction_offset": offset,
                    "instruction_length": len(line), "instruction_sha256": sha(line),
                    "ancestry_sha256": ancestry, "predecessor": item["predecessor"],
                    "p1_sha256": item["p1_sha256"], "row_sha256": item["row_receipt"]["sha256"],
                    "origin_sha256": sha(canonical(item["origin"])),
                    "reductions_sha256": sha(canonical(item["reductions"])), "scale": item["scale"],
                    "literal_input_sha256": item["literal_input_sha256"]})
            offset += len(line)
            if (index + 1) % 1024 == 0:
                progress("parent_loading", parent="p1_instruction", rows=index + 1, total=8059)
        require(stream.read(1) == b"", "p1_instruction_trailing")
    require(offset == BASE.P1_INSTRUCTION_BYTES and digest.hexdigest() == BASE.P1_INSTRUCTION_SHA256 and
            ancestry == p1["manifest"]["ancestry_sha256"] and len(roots) == len(selected),
            "p1_instruction_identity")
    fixed_stream(args.p1_root, "degree2.cache.bin", (BASE.P1_CACHE_BYTES, BASE.P1_CACHE_SHA256), True)
    return p1, roots


def reconstruct_defect(args: argparse.Namespace, states: list[dict[str, Any]],
                       final: list[list[int]], roots: list[dict[str, Any]],
                       seed: int, character: int, scalar: dict[str, Any]) -> dict[str, Any]:
    progress("raw_seed_evaluation", seed=seed, character=character)
    context, words = BASE.checker_source_context()
    word = tuple(int(x) for x in words["relators"][seed])
    raw = BASE.ARITH._checker_seed_evaluate_seed(context, word)
    require([part.shape for part in raw] == [(4, 6048), (4, 18144), (4, 36288), (8,)],
            "raw_seed_dimensions")
    raw_row = raw[2][character]
    direct_receipt = scalar["character"]["direct_receipt"]
    raw_row_sha, raw_support, raw_scalar = sha(pack(raw_row)), int(np.count_nonzero(raw_row)), dot(scalar["q"], raw_row)
    require(raw_row_sha == direct_receipt["raw_row_packed_sha256"][seed] and
            raw_support == direct_receipt["raw_row_support"][seed] and
            raw_scalar == scalar["direct_value"], "selected_raw_row_receipt_join")
    selected_direct_receipt = {"character": character, "seed": seed, "packed_sha256": raw_row_sha,
        "support": raw_support, "scalar": raw_scalar, "direct_receipt_sha256": direct_receipt["sha256"]}
    defect = tuple(part.copy() for part in raw)
    descriptors: list[tuple[Path, dict[str, Any]]] = []
    for source in range(4):
        for descriptor in BASE.OLD_BLOB_PINS[source]:
            descriptors.append((states[0]["root"], descriptor))
    descriptors += [(states[t + 1]["root"], BASE.NEW_BLOB_PINS[t]) for t in range(4)]
    for root, descriptor in descriptors:
        fixed_stream(root, descriptor["file"], (descriptor["bytes"], descriptor["sha256"]), True)
    selected_lifts = []
    root_by_node = {root["node"]: root for root in roots}
    with ExitStack() as stack:
        streams = [stack.enter_context(path(root, descriptor["file"]).open("rb"))
                   for root, descriptor in descriptors]
        cache = stack.enter_context(path(args.p1_root, "degree2.cache.bin").open("rb"))
        for count, (index, coefficient) in enumerate(final, 1):
            root_ref = root_by_node[index]
            packed = blob_row(cache, index, 145152)
            require(sha(packed) == root_ref["row_sha256"], "selected_row_hash")
            subtract(defect[2], unpack(packed, 145152).reshape(4, 36288), coefficient)
            components = [{"role": "p1-degree2", "bytes": len(packed), "sha256": sha(packed)}]
            if index < 2014:
                owner = max(c for c, offset in enumerate(OLD_OFFSETS) if offset <= index)
                local = index - OLD_OFFSETS[owner]
                lower_raw = blob_row(streams[2 * owner], local, 6056)
                lower = unpack(lower_raw, 6056)
                subtract(defect[0][owner], lower[:6048], coefficient)
                subtract(defect[3], lower[6048:], coefficient)
                grade_raw = blob_row(streams[2 * owner + 1], local, 72576)
                grade = unpack(grade_raw, 72576).reshape(4, 18144)
                subtract(defect[1], grade, coefficient)
                components += [{"role": "old-lower", "bytes": len(lower_raw), "sha256": sha(lower_raw)},
                               {"role": "old-grade", "bytes": len(grade_raw), "sha256": sha(grade_raw)}]
                lower_kind = "old"
            else:
                owner = max(c for c, offset in enumerate(NEW_OFFSETS) if offset <= index)
                local = index - NEW_OFFSETS[owner]
                grade_raw = blob_row(streams[8 + owner], local, 18144)
                grade = unpack(grade_raw, 18144)
                subtract(defect[1][owner], grade, coefficient)
                components.append({"role": "new-grade", "bytes": len(grade_raw), "sha256": sha(grade_raw)})
                lower_kind = "new"
            selected_lifts.append({"selection_index": count - 1, "node": index,
                "coefficient": coefficient, "lower_kind": lower_kind,
                "owner_character": owner, "p1_sha256": root_ref["p1_sha256"], "components": components})
            if count % 64 == 0 or count == len(final):
                progress("selected_p1_subtraction", selected=count, total=len(final))
    require_lower_zero(defect)
    projected = BASE.ARITH._checker_seed_full_project(context, defect, CHARACTERS[character])
    require(all(not np.any(part) for part in (projected[0], projected[1], projected[3])) and
            np.array_equal(projected[2][character], defect[2][character]) and
            not np.any(np.delete(projected[2], character, axis=0)),
            "complete_filtered_projector")
    return {"word": list(word), "raw": raw, "defect": defect, "projected": projected,
            "d": defect[2][character].copy(), "descriptors": descriptors, "selected_lifts": selected_lifts,
            "selected_direct_receipt": selected_direct_receipt}


def require_lower_zero(defect: tuple[np.ndarray, ...]) -> None:
    require(sum(part.size for part in (defect[0], defect[1], defect[3])) == LOWER_WIDTH and
            all(not np.any(part) for part in (defect[0], defect[1], defect[3])), "complete_lower_zero")


def component_receipt(name: str, part: np.ndarray) -> dict[str, Any]:
    payload = pack(part)
    return {"name": name, "shape": list(part.shape), "trits": int(part.size),
            "support": int(np.count_nonzero(part)), "packed_bytes": len(payload),
            "packed_sha256": sha(payload)}


def expected_source_receipts(events: list[dict[str, Any]], final: list[list[int]],
        p1: dict[str, Any], roots: list[dict[str, Any]], arithmetic: dict[str, Any],
        table: dict[str, Any], seed: int, character: int, selected_relation: dict[str, Any]
        ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Serialize independently calculated values in the small public delta ABI."""
    body_hashes = list(BASE.TASK554_BODY_DIGESTS)
    blob_receipts = []
    for i, (_, descriptor) in enumerate(arithmetic["descriptors"]):
        if i < 8:
            owner, role = i // 2, "lower" if i % 2 == 0 else "grade"
            start, count = OLD_OFFSETS[owner], BASE.OLD_RANKS[owner]
            label, body_sha = f"old-{owner}-{role}", body_hashes[0]
        else:
            owner = i - 8
            start, count = NEW_OFFSETS[owner], BASE.NEW_RANKS[owner]
            label, body_sha = f"new-{owner}-grade", body_hashes[owner + 1]
        blob_receipts.append({"role": label, "task554_body_sha256": body_sha,
            "descriptor": descriptor, "selected_rows": sum(start <= node < start + count for node, _ in final),
            "full_file_authenticated": True})
    blob_pass = seal({"schema": SCHEMA + ".task554-blob-pass", "receipts": blob_receipts,
        "selected_rows": len(final), "full_blob_files": 12,
        "total_authenticated_bytes": sum(item["descriptor"]["bytes"] for item in blob_receipts)})
    names = ("d0", "d1", "d2", "aux")
    raw_seed = seal({"schema": SCHEMA + ".raw-seed", "seed": seed, "character": character,
        "selected_direct_receipt": arithmetic["selected_direct_receipt"],
        "compact_word": arithmetic["word"], "compact_word_sha256": sha(canonical(arithmetic["word"])),
        "word_dictionary_sha256": BASE.ARITH.WORD_SHA,
        "relator_dictionary_sha256": BASE.ARITH.WORD_RELATOR_SHA,
        # This is the producer's declared lineage, not the arithmetic used here.
        "shared_legacy_arithmetic_sha256": BASE.PRODUCER_ARITH_SHA256,
        "components": [component_receipt(name, part) for name, part in zip(names, arithmetic["raw"])]})
    subtraction = seal({"schema": SCHEMA + ".complete-subtraction", "formula_id": FORMULA,
        "seed": seed, "character": character, "raw_event_count": len(events), "final_selected_count": len(final),
        "arithmetic_coefficient_collection": "mod3-after-ordered-raw-events",
        "literal_coefficient_collection": False, "task554_blob_pass_sha256": blob_pass["sha256"],
        "p1_cache_sha256": BASE.P1_CACHE_SHA256,
        "selected_lift_receipt_sha256": sha(canonical(arithmetic["selected_lifts"])),
        "reduced_components": [component_receipt(name, part)
                               for name, part in zip(names, arithmetic["defect"])],
        "lower_width": LOWER_WIDTH, "lower_nonzero_count": 0, "lower_zero_count": LOWER_WIDTH,
        "lower_dense_sha256": sha(b"\0" * LOWER_WIDTH),
        "plain_character_source_sha256": sha(pack(arithmetic["d"])),
        "full_projector_character_source_sha256": sha(pack(arithmetic["projected"][2][character])),
        "full_projector_other_character_nonzero_count": 0,
        "full_projector_applied_to_complete_defect": True})
    factors = [{"label": list(label), "pure_word": list(BASE.ARITH.SEED_PURE_WORDS[label]),
        "pure_word_sha256": sha(canonical(list(BASE.ARITH.SEED_PURE_WORDS[label]))),
        "source_character_sign": 1 if sum(x * y for x, y in zip(CHARACTERS[character], label)) % 2 == 0 else 2} for label in CHARACTERS]
    literal = seal({"schema": SCHEMA + ".literal-word-dag", "v518_formulae": ["1.3", "2.2", "4.3"],
        "coefficient_convention": {"0": "identity", "1": "word", "2": "inverse"},
        "defect": {"operation": "ordered-product",
            "seed_factor": {"seed": seed, "exponent": 1, "compact_word_sha256": raw_seed["compact_word_sha256"]},
            "p1_factor_sequence": {"source": "raw_events", "order": "event_id-ascending",
                "root_field": "p1_sha256", "root_join": "raw_events.global_index=p1_roots.node",
                "exponent_rule": "(3-coefficient)%3", "coefficient_collection": False}},
        "projector": {"operation": "ordered-character-projector", "character": list(CHARACTERS[character]),
            "order": [list(label) for label in CHARACTERS], "factors": factors},
        "actor_path": [], "forward_B": table["identity"]["forward:B"], "six_source_tag_replay": True,
        "eleven_slot_replay": False, "full_A0_witness": False})
    ancestry = seal({"schema": SCHEMA + ".selected-seed-ancestry", "seed": seed, "character": character,
        "selected_seed_relation": selected_relation,
        "task554_body_sha256": body_hashes, "raw_event_count": len(events), "raw_events": events,
        "raw_event_final_head": events[-1]["rolling_sha256"] if events else "0" * 64, "final_support": len(final),
        "final_coefficients": final, "p1_roots": roots, "selected_lifts": arithmetic["selected_lifts"],
        "literal_word_dag": literal,
        "p1_parent": {"manifest_sha256": BASE.P1_MANIFEST_SHA256, "cache_sha256": BASE.P1_CACHE_SHA256,
            "instruction_sha256": BASE.P1_INSTRUCTION_SHA256,
            "instruction_final_head": p1["manifest"]["ancestry_sha256"], "rows": 8059,
            "cache_passes": 1, "instruction_passes": 1, "selected_arithmetic_rows": len(final),
            "selected_literal_roots": len(roots)},
        "task554_blob_pass": blob_pass})
    return raw_seed, subtraction, ancestry


def reduce_dense(vector: np.ndarray, pivots: list[dict[str, Any]],
                 row_reader: Callable[[int], bytes], *, verbose: bool = False) -> tuple[np.ndarray, list[dict[str, Any]]]:
    require(len({p["lead"] for p in pivots}) == len(pivots) and
            all(type(p["lead"]) is int and 0 <= p["lead"] < len(vector) for p in pivots),
            "insertion_pivot_leads")
    remainder = vector.copy()
    reductions = []
    for pivot_id, pivot in enumerate(pivots):
        coefficient = int(remainder[pivot["lead"]])
        if coefficient:
            packed = row_reader(pivot_id)
            row = unpack(packed, len(vector))
            require(row[pivot["lead"]] == 1, "old_normalized_lead")
            subtract(remainder, row, coefficient)
            reductions.append({"pivot_id": pivot_id, "offer": pivot["offer"], "lead": pivot["lead"],
                "scalar": coefficient, "physical_offset": pivot["physical_offset"], "row_sha256": sha(packed)})
        if verbose and (pivot_id + 1) % 128 == 0:
            progress("physical_reduction", pivots=pivot_id + 1, total=len(pivots))
    require(all(remainder[p["lead"]] == 0 for p in pivots), "earlier_pivot_zeros")
    return remainder, reductions


def normalize(remainder: np.ndarray) -> tuple[np.ndarray, int, int]:
    support = np.flatnonzero(remainder)
    require(len(support) > 0, "new_rank_gate")
    lead = int(support[0])
    scale = int(remainder[lead])
    normalized = ((remainder.astype(np.uint16) * scale) % 3).astype(np.uint8)
    require(normalized[lead] == 1, "normalization")
    return normalized, lead, scale


def next_target(old: np.ndarray, normalized: np.ndarray, lead: int,
                old_leads: list[int]) -> tuple[np.ndarray, int]:
    require(all(old[index] == 0 and normalized[index] == 0 for index in old_leads), "target_old_leads")
    scalar = int(old[lead])
    output = old.copy()
    if scalar:
        subtract(output, normalized, scalar)
    require(output[lead] == 0 and all(output[index] == 0 for index in old_leads), "target_new_leads")
    return output, scalar


def b_and_pairings(args: argparse.Namespace, scalar: dict[str, Any],
                   arithmetic: dict[str, Any], current_lambda: np.ndarray,
                   final: list[list[int]]) -> dict[str, Any]:
    character, seed, expected = scalar["character_id"], scalar["seed"], scalar["value"]
    progress("parent_loading", parent="task712", character=character)
    require(scalar["launch"]["task712_parent"] == BASE.TASK712_PARENT, "task712_parent")
    table = BASE.ARITH.read_task712_envelope({**BASE.TASK712_PARENT,
                                             "root": str(args.task712_root.resolve())}, character)
    require(table["manifest_sha256"] == scalar["launch"]["task712_manifest_sha256"][character] and
            table["identity"]["adjoint:B"] == scalar["character"]["raw_dual"]["B_adj_table_identity"],
            "current_B_identity")
    BASE.check_table_transpose(table["forward"]["B"], table["adjoint"]["B"])
    entries = np.asarray(table["forward"]["B"], dtype=np.int64)
    require(entries.shape == (36288, 3), "B_entries")
    physical = np.zeros(WIDTH, dtype=np.int64)
    np.add.at(physical, entries[:, 1], entries[:, 2] * arithmetic["d"][entries[:, 0]])
    physical = (physical % 3).astype(np.uint8)
    pulled = np.zeros(36288, dtype=np.int64)
    np.add.at(pulled, entries[:, 0], entries[:, 2] * current_lambda[entries[:, 1]])
    q = (pulled % 3).astype(np.uint8)
    require(np.array_equal(q, scalar["q"]) and dot(q, arithmetic["d"]) == expected and
            dot(current_lambda, physical) == expected, "current_scalar_physical_pairings")
    raw_row = arithmetic["raw"][2][character]
    require(sha(pack(raw_row)) == scalar["character"]["direct_receipt"]["raw_row_packed_sha256"][seed] and
            dot(q, raw_row) == scalar["direct_value"] and
            (scalar["direct_value"] - sum(coefficient * int(scalar["values"][node])
                                           for node, coefficient in final)) % 3 == expected,
            "selected_direct_complete_relation_join")
    return {"G": physical, "q": q, "table": table}


def load_state(args: argparse.Namespace, scalar: dict[str, Any]) -> dict[str, Any]:
    progress("parent_loading", parent="current_state1354_plus_seed30_delta")
    delta = ROOTS.load_delta(args)
    launch_parent = scalar["launch"]["separator"]
    require(launch_parent["artifact"] == ROOTS.DELTA_ARTIFACT and
            launch_parent["generation"] == 8060 and launch_parent["rank"] == 1355 and
            launch_parent["head"] == CURRENT_HEAD and launch_parent["lambda_sha256"] == CURRENT_LAMBDA and
            launch_parent["files"] == [{"file": name, "bytes": pin[0], "sha256": pin[1]}
                                       for name, pin in sorted(ROOTS.DELTA_FILES.items())], "current_delta_join")
    same(scalar["launch"]["p1_parent"], delta["result"]["parents"]["p1"], "p1_delta_join")
    require(scalar["launch"]["task554_parent"]["artifacts"] ==
            delta["result"]["parents"]["task554"]["artifacts"] and
            list(BASE.TASK554_BODY_DIGESTS) == delta["result"]["parents"]["task554"]["body_sha256"] and
            scalar["launch"]["task712_parent"] == delta["result"]["parents"]["task712"]["artifact"],
            "unchanged_sources_join")
    root = args.state_root.resolve()
    small = {name: json_bytes(fixed(root, name, identity)) for name, identity in ROOTS.STATE_FILES.items()}
    for name in ("state/physical.bin", "state/physical-p1-coeff.bin"):
        fixed_stream(root, name, STATE_FILES[name], True)
    state, head = small["state/manifest.json"], small["state/HEAD"]
    require(state["rank"] == head["rank"] == 1354 and state["generation"] == head["generation"] == 8059 and
            state["cursor"] == head["cursor"] == 8059 and head["rolling_head"] == OLD_HEAD and
            head["manifest_sha256"] == STATE_FILES["state/manifest.json"][1] and
            state["instructions"]["final_head"] == OLD_HEAD and
            state["instructions"]["sha256"] == STATE_FILES["state/instructions.jsonl"][1] and
            state["physical"]["sha256"] == STATE_FILES["state/physical.bin"][1], "old_state_premise")
    checker = small["checker-result.json"]
    require(checker["status"] == "PASS" and checker["physical_rank"] == 1354 and
            checker["verified"] is False and checker["cross_checked"] is False and
            delta["result"]["parents"]["state"]["manifest_sha256"] == STATE_FILES["state/manifest.json"][1] and
            delta["result"]["parents"]["state"]["physical_sha256"] == STATE_FILES["state/physical.bin"][1],
            "old_current_parent_join")
    identity = STATE_FILES["state/instructions.jsonl"]
    instruction = path(root, "state/instructions.jsonl")
    require(instruction.stat().st_size == identity[0], "old_instruction_size")
    digest, total, rolling, pivots = hashlib.sha256(), 0, "0" * 64, []
    # Authentication and pivot metadata only; no old offers/Conn are rebuilt.
    with instruction.open("rb", buffering=1 << 20) as stream:
        for offer in range(8059):
            line = stream.readline()
            require(line.endswith(b"\n"), "old_instruction_eof")
            digest.update(line)
            total += len(line)
            record = json_bytes(line)
            require(record["offer"] == offer and record["rolling_sha256"] ==
                    sha(bytes.fromhex(rolling) + canonical({key: value for key, value in record.items()
                                                          if key != "rolling_sha256"})), "old_instruction_rolling")
            rolling = record["rolling_sha256"]
            if record["kind"] == "physical_pivot":
                require(record["physical_offset"] == len(pivots) * ROW_BYTES and
                        record["coefficient_offset"] == len(pivots) * 2015 and
                        record["rank"] == len(pivots) + 1 and type(record["lead"]) is int and
                        0 <= record["lead"] < WIDTH, "old_pivot_position")
                pivots.append({"offer": offer, "lead": record["lead"],
                    "physical_offset": record["physical_offset"],
                    "coefficient_offset": record["coefficient_offset"], "rolling_sha256": rolling})
            if (offer + 1) % 1024 == 0:
                progress("parent_loading", parent="old_instruction_metadata", rows=offer + 1, total=8059)
        require(stream.read(1) == b"", "old_instruction_trailing")
    require(total == identity[0] and digest.hexdigest() == identity[1] and rolling == OLD_HEAD and
            len(pivots) == 1354 and len({p["lead"] for p in pivots}) == 1354, "old_instruction_identity")
    saved = delta["result"]["pivot"]
    require(saved["pivot_id"] == len(pivots) and saved["offer"] == 8059 and
            saved["rank_before"] == 1354 and saved["rank_after"] == 1355 and
            saved["head_before"] == OLD_HEAD and saved["head_after"] == CURRENT_HEAD and
            saved["lead"] not in {p["lead"] for p in pivots} and
            all(delta["normalized"][p["lead"]] == 0 for p in pivots) and
            delta["normalized"][saved["lead"]] == 1, "saved_delta_pivot")
    pivots.append({"offer": saved["offer"], "lead": saved["lead"],
        "physical_offset": 1354 * ROW_BYTES, "coefficient_offset": None, "rolling_sha256": CURRENT_HEAD})
    target = delta["result"]["target"]
    require(target["state_head"] == CURRENT_HEAD and target["state_rank"] == 1355 and
            target["remainder_sha256"] == CURRENT_REMAINDER and
            all(delta["target"][p["lead"]] == 0 for p in pivots) and
            dot(delta["lambda"], delta["target"]) == 1, "saved_current_target")
    base_target = small["output/result.json"]["target_reduction"]
    require(base_target == small["output/terminal.json"]["target_reduction"] and
            delta["result"]["parents"]["state"]["target_sha256"] == sha(canonical(base_target)) and
            target["parent_target_sha256"] == sha(canonical(base_target)) and
            target["parent_result_sha256"] == STATE_FILES["output/result.json"][1], "target_parent_chain")
    parent = {"mode": "immutable-state-plus-one-accepted-delta",
        "base": delta["result"]["parents"]["state"],
        "delta": {"artifact": ROOTS.DELTA_ARTIFACT, "files": launch_parent["files"],
            "pivot_sha256": saved["sha256"], "target_sha256": sha(canonical(target)),
            "physical": file_receipt("physical-normalized.bin", pack(delta["normalized"])),
            "target_remainder": file_receipt("target-remainder.bin", pack(delta["target"])),
            "lambda": file_receipt("lambda.bin", pack(delta["lambda"]))},
        "manifest_sha256": ROOTS.DELTA_FILES["output/manifest.json"][1],
        "head": CURRENT_HEAD, "generation": 8060, "rank": 1355,
        "old_derivation_accepted_as_premise": True, "prior_delta_accepted_as_premise": True}
    return {"state": state, "head": head, "pivots": pivots, "root": root,
        "delta": delta, "old_target": target, "old_remainder": delta["target"],
        "lambda": delta["lambda"], "saved_pivot": pack(delta["normalized"]), "parent": parent,
        "base_target": base_target,
        "prior_target_reduction_count": len(base_target["reductions"]) + len(target["new_reductions"])}


def next_separator(remainder: np.ndarray, pivots: list[dict[str, Any]], normalized: np.ndarray,
                   lead: int, row_reader: Callable[[int], bytes], offer: int) -> dict[str, Any]:
    free = np.flatnonzero(remainder)
    require(len(free) > 0, "separator_nonzero")
    free_coordinate, free_value = int(free[0]), int(remainder[free[0]])
    require(free_coordinate not in {p["lead"] for p in pivots} | {lead}, "separator_free")
    width = len(remainder)
    functional = np.zeros(width, dtype=np.uint8)
    functional[free_coordinate] = free_value
    transcript = []
    all_pivots = pivots + [{"lead": lead, "offer": offer}]
    for pivot_id in range(len(pivots), -1, -1):
        record = all_pivots[pivot_id]
        packed = pack(normalized) if pivot_id == len(pivots) else row_reader(pivot_id)
        row = normalized if pivot_id == len(pivots) else unpack(packed, width)
        require(row[record["lead"]] == 1 and functional[record["lead"]] == 0, "separator_pivot_coordinate")
        value = (-dot(row, functional)) % 3
        functional[record["lead"]] = value
        require(dot(row, functional) == 0, "separator_reverse_equation")
        transcript.append({"reverse_index": pivot_id, "pivot_id": pivot_id, "offer": record["offer"],
            "lead": record["lead"], "row_sha256": sha(packed), "lambda_value": value, "equation": 0})
        if len(transcript) % 256 == 0:
            progress("next_separator", rows=len(transcript), total=len(all_pivots))
    # Check the FINAL vector against every old row and both delta pivots.
    for index in range(len(pivots)):
        require(dot(functional, unpack(row_reader(index), width)) == 0, "final_lambda_allrows")
        if (index + 1) % 256 == 0:
            progress("final_lambda_pairings", rows=index + 1, total=len(all_pivots))
    require(dot(functional, normalized) == 0 and dot(functional, remainder) == 1,
            "final_lambda_new_pivot_and_target")
    progress("final_lambda_pairings", rows=len(all_pivots), total=len(all_pivots))
    return {"lambda": functional, "transcript": transcript,
            "free_coordinate": free_coordinate, "free_value": free_value}


def file_receipt(name: str, payload: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(payload), "sha256": sha(payload)}


def expected_parents(scalar: dict[str, Any], state: dict[str, Any], table: dict[str, Any]) -> dict[str, Any]:
    launch, old = scalar["launch"], state["state"]
    require(old["p1_identity"]["manifest_sha256"] == BASE.P1_MANIFEST_SHA256 and
            old["p1_identity"]["cache_sha256"] == BASE.P1_CACHE_SHA256 and
            old["p1_identity"]["instruction"]["sha256"] == BASE.P1_INSTRUCTION_SHA256 and
            old["source_ancestry"]["prepare_body_sha256"] == BASE.TASK554_BODY_DIGESTS[0] and
            old["source_ancestry"]["parents"] == list(BASE.TASK554_BODY_DIGESTS[1:]) and
            old["task712"]["tables"]["manifest_sha256"] == table["manifest_sha256"], "source_parent_joins")
    rho2 = state["delta"]["result"]["parents"]["rho2"]
    require(rho2["packed_sha256"] == state["old_target"]["rho2_sha256"] ==
            "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e" and
            rho2["manifest_sha256"] == state["base_target"]["target_parent_manifest_sha256"],
            "retained_target_parent_join")
    return {
        "scalar": {"final_artifact": SCALAR_ARTIFACT, "launch": scalar["launch_receipt"],
            "source": {"file": "source-receipt.json", "bytes": SCALAR_FILES["source-receipt.json"][0],
                       "sha256": SCALAR_FILES["source-receipt.json"][1]},
            **{key + "_sha256": SCALAR_FILES[name][1] for key, name in (
                ("manifest", "output/manifest.json"), ("result", "output/result.json"),
                ("checker", "checker-result.json"))},
            "character_sha256": scalar["character"]["sha256"],
            "violation_sha256": scalar["violation"]["sha256"],
            "raw_dual_sha256": scalar["character"]["raw_dual"]["sha256"],
            "selected_seed_relation_sha256": scalar["relation"]["sha256"],
            "relation_receipt_sha256": scalar["result"]["relation_receipt"]["sha256"]},
        "task554": {**{key: launch["task554_parent"][key]
                        for key in ("source_run", "source_attempt", "source_head", "artifacts")},
                    "body_sha256": list(BASE.TASK554_BODY_DIGESTS)},
        "p1": launch["p1_parent"],
        "task712": {"artifact": BASE.TASK712_PARENT, "manifest_sha256": table["manifest_sha256"],
                    "B_fwd_identity": table["identity"]["forward:B"]},
        "state": state["parent"], "rho2": {**rho2, "target_derivation_accepted_as_premise": True},
        "source_modules": {
            "d972_r07_actual_grade2_root_scalar_batch_v2.py":
                "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
            "d972_r07_targeted_grade2_owner_generated_join_v15.py": BASE.PRODUCER_ARITH_SHA256},
    }


def compare_candidate(candidate_root: Path, result: dict[str, Any], instruction: dict[str, Any],
                      rows: dict[str, bytes]) -> dict[str, Any]:
    """Full strict comparison: self-consistent resealing cannot supply authority."""
    expected_payloads = {**rows, "result.json": canonical(result), "instruction.json": canonical(instruction)}
    roster = sorted([*expected_payloads, "manifest.json"])
    require(candidate_root.is_dir() and not candidate_root.is_symlink() and
            sorted(item.name for item in candidate_root.iterdir()) == roster, "candidate_exact_roster")
    for name, expected in expected_payloads.items():
        # Positioned/payload contents are checked against independently computed
        # bytes, not against the candidate manifest's own hashes.
        raw = fixed(candidate_root, name, (len(expected), sha(expected)))
        require(raw == expected, "candidate_exact_bytes:" + name)
    expected_manifest = seal({"schema": SCHEMA + ".manifest", "mode": "parent-plus-one-pivot-delta",
        "candidate": True, "verified": False, "cross_checked": False,
        "files": sorted([file_receipt(name, raw) for name, raw in expected_payloads.items()],
                        key=lambda item: item["file"]), "file_roster": roster,
        "parent_state_manifest_sha256": ROOTS.DELTA_FILES["output/manifest.json"][1],
        "parent_state_head": CURRENT_HEAD, "state_head": instruction["rolling_sha256"],
        "rank_before": 1355, "rank_after": 1356, "result_sha256": sha(canonical(result)),
        "terminal": result["kind"], "parent_state_copied": False})
    manifest = json_bytes(fixed(candidate_root, "manifest.json",
                               (len(canonical(expected_manifest)), sha(canonical(expected_manifest)))))
    same(manifest, expected_manifest, "candidate_manifest")
    return {"manifest_sha256": sha(canonical(manifest)), "result_sha256": sha(canonical(result)),
            "instruction_sha256": sha(canonical(instruction))}


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    progress("parent_loading", parent="checker_source_lineage")
    scalar = load_scalar(args)
    seed, character, value = scalar["seed"], scalar["character_id"], scalar["value"]
    state = load_state(args, scalar)
    states = load_task554(args, scalar["launch"], seed)
    events, final = combined_selected(states, seed, scalar["relation"])
    p1, roots = p1_roots(args, scalar["launch"], events)
    arithmetic = reconstruct_defect(args, states, final, roots, seed, character, scalar)
    maps = b_and_pairings(args, scalar, arithmetic, state["lambda"], final)
    table = maps["table"]
    raw_seed, subtraction, ancestry = expected_source_receipts(
        events, final, p1, roots, arithmetic, table, seed, character, scalar["relation"])
    parents = expected_parents(scalar, state, table)
    source_raw, physical_raw = pack(arithmetic["d"]), pack(maps["G"])
    raw_materialization = seal({"schema": SCHEMA + ".raw-materialization",
        "violation_sha256": scalar["violation"]["sha256"], "raw_dual_sha256": scalar["violation"]["raw_dual_sha256"],
        "lambda_sha256": CURRENT_LAMBDA, "raw_q_sha256": sha(pack(maps["q"])),
        "raw_seed_sha256": raw_seed["sha256"], "source_ancestry_sha256": ancestry["sha256"],
        "lower_zero_receipt_sha256": subtraction["sha256"],
        "raw_word_sha256": ancestry["literal_word_dag"]["sha256"],
        "raw_source_sha256": sha(source_raw), "raw_physical_sha256": sha(physical_raw),
        "forward_B": table["identity"]["forward:B"], "actor_path": [], "q_d": value, "lambda_G": value})
    progress("physical_reduction", pivots=0, total=1355)
    with path(state["root"], "state/physical.bin").open("rb") as stream:
        def read_pivot(index: int) -> bytes:
            return blob_row(stream, index, WIDTH) if index < 1354 else state["saved_pivot"]
        remainder, reductions = reduce_dense(maps["G"], state["pivots"], read_pivot, verbose=True)
        normalized, lead, scale = normalize(remainder)
        require(lead not in {record["lead"] for record in state["pivots"]} and
                dot(state["lambda"], remainder) == value and dot(state["lambda"], normalized) == (value * scale) % 3,
                "rank_gate_and_raw_normalized_pairing")
        remainder_raw, normalized_raw = pack(remainder), pack(normalized)
        normalized_word = seal({"schema": SCHEMA + ".normalized-word-dag", "v518_formula": "4.3",
            "raw_word_sha256": ancestry["literal_word_dag"]["sha256"],
            "operation": "ordered-product-then-scale", "parent_state_head": CURRENT_HEAD,
            "parent_state_manifest_sha256": ROOTS.DELTA_FILES["output/manifest.json"][1],
            "reductions": [{"pivot_id": item["pivot_id"], "offer": item["offer"],
                "instruction_rolling_sha256": state["pivots"][item["pivot_id"]]["rolling_sha256"],
                "row_sha256": item["row_sha256"], "coefficient": item["scalar"],
                "literal_exponent": (-item["scalar"]) % 3} for item in reductions],
            "scale": scale, "coefficient_two_means": "inverse", "coefficient_collection": False})
        instruction_body = {"schema": SCHEMA + ".state-instruction", "kind": "physical_pivot",
            "offer": 8060, "generation": 8061, "predecessor": CURRENT_HEAD, "parent_state": parents["state"],
            "raw_materialization_sha256": raw_materialization["sha256"],
            "source_ancestry_sha256": ancestry["sha256"], "normalized_word_sha256": normalized_word["sha256"],
            "top": file_receipt("physical-raw.bin", physical_raw),
            "remainder": file_receipt("physical-remainder.bin", remainder_raw),
            "physical": file_receipt("physical-normalized.bin", normalized_raw),
            "reductions": reductions, "lead": lead, "sigma": scale, "lower_zero": True,
            "physical_zero": False, "rank": 1356, "physical_offset": 1355 * ROW_BYTES,
            "delta_physical_offset": 0, "coefficient_offset": None,
            "coefficient_representation": "parent-literal-DAG"}
        new_head = sha(bytes.fromhex(CURRENT_HEAD) + canonical(instruction_body))
        instruction = {**instruction_body, "rolling_sha256": new_head}
        pivot = seal({"schema": SCHEMA + ".physical-pivot",
            "raw_materialization_sha256": raw_materialization["sha256"], "offer": 8060, "pivot_id": 1355,
            "lead": lead, "scale": scale, "rank_before": 1355, "rank_after": 1356,
            "generation_before": 8060, "generation_after": 8061, "head_before": CURRENT_HEAD,
            "head_after": new_head, "instruction_sha256": sha(canonical(instruction)),
            "reductions": reductions, "raw_sha256": sha(physical_raw),
            "remainder_sha256": sha(remainder_raw), "normalized_sha256": sha(normalized_raw),
            "earlier_pivot_zero_count": 1355, "lambda_raw": value, "lambda_remainder": value,
            "lambda_normalized": (value * scale) % 3, "literal_word_dag": normalized_word})
        progress("target_append", new_pivots=1, old_target_reductions=state["prior_target_reduction_count"], rank=1356)
        updated, target_scalar = next_target(state["old_remainder"], normalized, lead,
                                              [record["lead"] for record in state["pivots"]])
        updated_raw = pack(updated)
        kind = "Separator" if np.any(updated) else "ConnectionMemberCandidate"
        target_update = seal({"schema": SCHEMA + ".target-update",
            "parent_target_sha256": sha(canonical(state["old_target"])),
            "parent_result_sha256": ROOTS.DELTA_FILES["output/result.json"][1],
            "old_remainder_sha256": CURRENT_REMAINDER, "old_reduction_count": state["prior_target_reduction_count"],
            "rho2_sha256": state["old_target"]["rho2_sha256"],
            "state_head": new_head, "state_rank": 1356, "scalar": target_scalar,
            "new_pivots_examined": 1, "new_reductions": [{"pivot_id": 1355, "offer": 8060,
                "lead": lead, "scalar": target_scalar, "physical_offset": 1355 * ROW_BYTES,
                "row_sha256": sha(normalized_raw)}] if target_scalar else [],
            "remainder_sha256": sha(updated_raw), "kind": kind, "old_target_history_copied": False, "old_target_history_replayed": False})
        separator = None
        rows = {"source-d.bin": source_raw, "physical-raw.bin": physical_raw,
                "physical-remainder.bin": remainder_raw, "physical-normalized.bin": normalized_raw,
                "target-remainder.bin": updated_raw}
        if kind == "Separator":
            reverse = next_separator(updated, state["pivots"], normalized, lead, read_pivot, 8060)
            require(dot(reverse["lambda"], updated) == 1 and
                    dot(reverse["lambda"], state["old_remainder"]) == 1, "separator_updated_target")
            rows["lambda.bin"] = pack(reverse["lambda"])
            separator = {key: reverse[key] for key in ("free_coordinate", "free_value", "transcript")}
            separator.update({"lambda_sha256": sha(rows["lambda.bin"]),
                              "lambda_rho2": 1, "lambda_physical_pivots": 0,
                "lambda_rho2_basis": "accepted-parent-target-derivation",
                "direct_pairing": {"rows": 1356, "row_pairings_sha256": sha(b"\0" * 1356),
                    "lambda_pivots": 0, "lambda_parent_remainder": 1, "lambda_new_remainder": 1}})
    result = seal({"schema": SCHEMA + ".result", "status": "PASS", "kind": kind, "candidate": True,
        "verified": False, "cross_checked": False, "claims": CLAIMS, "parents": parents,
        "raw_seed": raw_seed, "subtraction": subtraction, "ancestry": ancestry,
        "raw_materialization": raw_materialization, "pairings": {"q_d": value, "lambda_G": value, "B_adjoint_q_equal": True},
        "pivot": pivot, "target": target_update, "separator": separator,
        "literal_replay": {"formal_graded_word_dag": True, "parent_state_ancestry_premise": True,
            "normalized_exponent_pair": "NOT_REPLAYED", "eleven_slot_replay": False,
            "full_A0_witness": False, "grade2_positive_terminal_complete": False}})
    progress("candidate_comparison", kind=kind)
    comparison = compare_candidate(args.candidate_root, result, instruction, rows)
    progress("terminal", status="PASS", kind=kind, rank=1356)
    return {"schema": SCHEMA + ".checker-result", "status": "PASS", "kind": kind,
        "rank_before": 1355, "rank_after": 1356, "selected_rows": len(final), "seed": seed, "character": character,
        "raw_events": len(events), "literal_p1_roots": len(roots), "lower_zero_count": LOWER_WIDTH,
        "physical_reductions": len(reductions), "old_target_reductions": state["prior_target_reduction_count"],
        "new_target_eliminations": int(target_scalar != 0), "new_pivots": 1,
        "state_head": new_head, **comparison, "old_state_derivation_premise": True,
        "checker_lineage": SOURCE_PINS, "adapted_checker_lineage": ADAPTED_CHECKER, "claims": CLAIMS, "verified": False, "cross_checked": False}


def reject_test(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError("root_seed_v3_checker:selftest_did_not_reject:" + label)


def selftest() -> dict[str, Any]:
    """Only changed-interface canaries; no old suite or parent arithmetic."""
    states = [{"expressions": [[], [], [], []], "body_sha256": str(i) * 64} for i in range(5)]
    states[0]["expressions"][0] = [[1, 1], [0, 2]]
    states[1]["expressions"][0] = [[2, 1], [1, 2]]
    states[1]["expressions"][1] = [[2, 2], [1, 2]]
    events, coefficients = combined_selected(states, 17)
    require(coefficients == [[0, 2], [1, 1], [2015, 1]] and
            all(event["seed"] == 17 for event in events) and
            len({event["global_index"] for event in events}) == 4,
            "dynamic_selected_support_canary")
    relation = {"seed": 17, "raw_event_count": len(events), "raw_event_head": events[-1]["rolling_sha256"]}
    same(combined_selected(states, 17, relation), (events, coefficients), "relation_receipt_canary")
    reject_test(lambda: combined_selected(states, 18, relation), "stale_selected_seed")
    reject_test(lambda: ROOTS.current_identity(8059, 1354, OLD_HEAD, CURRENT_LAMBDA), "stale_parent_head")
    rows = [np.array([0, 1, 1, 1, 0, 0], dtype=np.uint8),
            np.array([1, 0, 2, 1, 1, 0], dtype=np.uint8),
            np.array([0, 0, 1, 0, 0, 1], dtype=np.uint8)]
    pivots = [{"lead": lead, "offer": 10 + index, "physical_offset": 2 * index}
              for index, lead in enumerate((1, 0, 2))]
    old_rows, saved_delta = rows[:2], pack(rows[2])
    reader = lambda index: pack(old_rows[index]) if index < 2 else saved_delta
    tail = np.array([0, 0, 0, 2, 0, 1], dtype=np.uint8)
    raw = (rows[0] + 2 * rows[1] + rows[2] + tail) % 3
    remainder, reductions = reduce_dense(raw, pivots, reader)
    normalized, lead, scale = normalize(remainder)
    require(np.array_equal(remainder, tail) and [item["pivot_id"] for item in reductions] == [0, 1, 2] and
            lead == 3 and scale == 2, "parent_plus_saved_delta_order_canary")
    current_target = np.array([0, 0, 0, 1, 2, 0], dtype=np.uint8)
    updated, scalar = next_target(current_target, normalized, lead, [1, 0, 2])
    require(scalar == 1 and updated.tolist() == [0, 0, 0, 0, 2, 1], "single_current_target_step_canary")
    reverse = next_separator(updated, pivots, normalized, lead, reader, 13)
    require(dot(reverse["lambda"], updated) == 1 and
            all(dot(reverse["lambda"], row) == 0 for row in [*rows, normalized]), "final_allrows_canary")
    reads = [0, 0, 0]
    def changed_after_reverse(index: int) -> bytes:
        reads[index] += 1
        if index == 0 and reads[index] == 2:
            damaged = rows[0].copy()
            damaged[4] = 1
            return pack(damaged)
        return reader(index)
    reject_test(lambda: next_separator(updated, pivots, normalized, lead, changed_after_reverse, 13),
                "bad_row_in_final_lambda_pass")
    zero, scalar = next_target(normalized, normalized, lead, [1, 0, 2])
    require(scalar == 1 and not np.any(zero), "member_candidate_one_step_canary")
    return {"schema": SCHEMA + ".checker-selftest", "status": "PASS", "fixture_only": True,
        "checks": ["selected-seed-relation-dynamic-support", "stale-head-rejected",
                   "split-state-one-target-step", "final-lambda-bad-row-rejected"],
        "verified": False, "cross_checked": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    names = ("scalar_root", "delta_root", "state_root", "prepare_root", "p1_root", "task712_root", "candidate_root")
    for name in names:
        parser.add_argument("--" + name.replace("_", "-"), type=Path)
    parser.add_argument("--block-root", action="append", type=Path, default=[])
    args = parser.parse_args()
    try:
        if args.selftest:
            require(not args.block_root and all(getattr(args, name) is None for name in names), "selftest_not_actual")
            report = selftest()
        else:
            require(len(args.block_root) == 4 and all(getattr(args, name) is not None for name in names),
                    "actual_fixed_parent_paths_required")
            candidate = args.candidate_root.resolve()
            require(args.candidate_root.is_dir() and not args.candidate_root.is_symlink(), "candidate_directory")
            for parent in [*(getattr(args, name) for name in names if name != "candidate_root"), *args.block_root]:
                require(parent.is_dir() and not parent.is_symlink() and candidate != parent.resolve() and
                        candidate not in parent.resolve().parents and parent.resolve() not in candidate.parents,
                        "candidate_parent_disjoint")
            report = check_actual(args)
        sys.stdout.buffer.write(canonical(report))
        sys.stdout.buffer.flush()
        return 0
    except Exception as exc:
        status = "UNKNOWN_RESOURCE" if isinstance(exc, MemoryError) else "REJECTED"
        progress("terminal", status=status, reason=str(exc), error_type=type(exc).__name__)
        sys.stdout.buffer.write(canonical({"schema": SCHEMA + ".checker-result", "status": status,
            "reason": str(exc), "error_type": type(exc).__name__, "verified": False, "cross_checked": False}))
        sys.stdout.buffer.flush()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
