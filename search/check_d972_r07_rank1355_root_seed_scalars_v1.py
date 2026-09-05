#!/usr/bin/env python3
"""Independent fixed rank1355 root-seed scalar checker (Task938).

Inputs: one accepted seed30 delta, old physical state, Task554/P1/Task712.
Output: exact 4*44 root scalars, never actors, orbits or a materialization.
Only the pinned checker v2/v15 arithmetic is reused.  The new producer is
neither imported nor executed, and old state/delta derivations are premises.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable

import numpy as np

SCHEMA = "d972.r07.rank1355.root-seed-scalars.v1"
LINEAGE = {
    "check_d972_r07_actual_grade2_root_scalar_batch_v2.py":
        "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6",
    "check_d972_r07_targeted_grade2_owner_generated_join_v15.py":
        "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662",
}
for _name, _wanted in LINEAGE.items():
    _path = Path(__file__).resolve().parent / _name
    if _path.is_symlink() or hashlib.sha256(_path.read_bytes()).hexdigest() != _wanted:
        raise ValueError("rank1355_checker:source_pin:" + _name)
import check_d972_r07_actual_grade2_root_scalar_batch_v2 as BASE

NEW_HEAD = "36feb776736c6587ce9f64d6f5acb883385074a7cc2eed4c2ce7eb8675e71342"
OLD_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"
LAMBDA_SHA = "f83bbaa503b8a4d5056f0779085ee4eced542eb1d78d3e35fa9df1c281960565"
TARGET_SHA = "f5040e3f29b42e71b86be047d40de5d538ddb7fc107cace219879bbc67238d3a"
DELTA_ARTIFACT = {
    "run": 33946247365, "attempt": 1,
    "head": "7f6dfaddf4150449e62a9b3e85def472fcb41c01",
    "id": 9963533999,
    "name": "d972-r07-actual-seed30-materializer-v1-candidate-33946247365-1",
    "bytes": 915410,
    "sha256": "sha256:f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6",
}
DELTA_FILES = {
    "output/manifest.json": (1810, "7673b3c0ba5b23080ab51490e1ab9e72fe92f8afe313bf1b465d3892e8836f7d"),
    "output/result.json": (2903961, "60e47f7c673942611647a69087d29bd0223e40394144b43aae9e0f55da10fb8b"),
    "output/instruction.json": (143336, "64396583ac9f991af40cd9997310a308c18facc0d2aaca336e2b508473b488d5"),
    "checker-result.json": (1383, "d9368b9ace442ef0d4bfb2099ace1c982b995eb428bfc8d46920633a198c4491"),
    "source-receipt.json": (1632, "f8932ca0b08d6dd7a42fb2560ee5c30adffe39c18d5eafd40a9d1e18ac3a6b30"),
}
STATE_FILES = {
    "state/HEAD": (299, "f789ac352864ae662beced75f9004887fe677f81eee922eb9d9200dcaf6860ef"),
    "state/manifest.json": (7780, "d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b"),
    "output/result.json": (457791, "d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968"),
    "output/terminal.json": (457656, "098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf"),
    "checker-result.json": (515, "2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433"),
}
BODY_BYTES = (15398340, 74883943, 75400514, 75340879, 75407216)
OLD_OFFSETS = (0, 505, 1008, 1511)
NEW_OFFSETS = (2014, 3523, 5035, 6547)
ZERO_HEAD = "0" * 64
WIDTH = 48384
ROW_BYTES = 12096
FORMULA = "r07.v541.formulas-2.1-2.2-4.1.raw-seed-plus-actor-lower-adjoint"
LINEAGES = {
    "producer": {
        "d972_r07_actual_grade2_root_scalar_batch_v2.py": "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
        "d972_r07_targeted_grade2_owner_generated_join_v15.py": "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632",
    },
    "checker": LINEAGE,
}
SCOPE = {"characters": [0, 1, 2, 3], "seeds": list(range(44)),
         "scalar_order": "character-major/seed0-through43", "scalar_count": 176,
         "actor_origins_executed": 0, "orbit_rows_executed": 0}
CLAIMS = {"ROOT_SEED_SCALARS_CANDIDATE": True, "GRADE2_MEMBER": "NOT_DECIDED",
          "GRADE2_NONMEMBER": "NOT_DECIDED", "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
          "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED",
          "verified": False}


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError("rank1355_checker:" + reason)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(body: dict[str, Any]) -> dict[str, Any]:
    require("sha256" not in body, "double_seal")
    return {**body, "sha256": sha(canonical(body))}


def same(actual: Any, expected: Any, reason: str) -> None:
    require(canonical(actual) == canonical(expected), reason)


def check_seal(value: dict[str, Any]) -> None:
    same(value, seal({key: item for key, item in value.items() if key != "sha256"}), "seal")


def json_bytes(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("ascii"))
    require(isinstance(value, dict) and canonical(value) == raw, "canonical_json")
    return value


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def safe_file(root: Path, name: str) -> Path:
    require(name and not Path(name).is_absolute() and ".." not in Path(name).parts and
            ":" not in name and "\\" not in name, "relative_path")
    require(not root.is_symlink(), "parent_symlink")
    root = root.resolve()
    item = root
    for component in Path(name).parts:
        item /= component
        require(not item.is_symlink(), "file_symlink")
    require(item.is_file() and root in item.resolve().parents, "file_missing_or_escape:" + name)
    return item


def fixed(root: Path, name: str, identity: tuple[int, str]) -> bytes:
    item = safe_file(root, name)
    require(item.stat().st_size == identity[0], "fixed_size:" + name)
    raw = item.read_bytes()
    require(len(raw) == identity[0] and sha(raw) == identity[1], "fixed_digest:" + name)
    return raw


def receipt(name: str, raw: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def pack(vector: np.ndarray) -> bytes:
    return BASE.ARITH.pack_trits(vector)


def unpack(raw: bytes, width: int) -> np.ndarray:
    return BASE.ARITH.unpack_trits(raw, width)


def dot(left: np.ndarray, right: np.ndarray) -> int:
    require(left.shape == right.shape, "dot_shape")
    return int(np.sum(left.astype(np.uint64) * right.astype(np.uint64), dtype=np.uint64) % 3)


def current_identity(generation: int, rank: int, head: str, lambda_sha: str) -> None:
    require(type(generation) is int and generation == 8060 and type(rank) is int and rank == 1355 and
            head == NEW_HEAD and lambda_sha == LAMBDA_SHA, "fresh_rank1355_separator")


def load_delta(args: argparse.Namespace) -> dict[str, Any]:
    progress("parent_loading", parent="rank1355_delta")
    raw = {name: fixed(args.delta_root, name, identity) for name, identity in DELTA_FILES.items()}
    objects = {name: json_bytes(data) for name, data in raw.items()}
    manifest, result = objects["output/manifest.json"], objects["output/result.json"]
    checker, source = objects["checker-result.json"], objects["source-receipt.json"]
    for obj in (manifest, result, result["pivot"], result["target"]):
        check_seal(obj)
    current_identity(result["pivot"]["generation_after"], manifest["rank_after"],
                     manifest["state_head"], result["separator"]["lambda_sha256"])
    require(checker["status"] == "PASS" and checker["kind"] == result["kind"] == "Separator" and
            checker["rank_after"] == 1355 and checker["state_head"] == NEW_HEAD and
            checker["manifest_sha256"] == DELTA_FILES["output/manifest.json"][1] and
            checker["result_sha256"] == DELTA_FILES["output/result.json"][1] and
            checker["verified"] is False and checker["cross_checked"] is False and
            result["verified"] is False and result["cross_checked"] is False,
            "delta_checker_result_join")
    source_by_name = {item["file"]: item for item in source["files"]}
    require(source["verified"] is False and source["cross_checked"] is False and
            source_by_name["search/d972_r07_actual_seed30_materializer_v1.py"]["sha256"] ==
            "3ce9293e05f06bf343bd2a54af0ab84ae67f4b922a428cd3c73e38944d6de55c" and
            source_by_name["search/check_d972_r07_actual_seed30_materializer_v1.py"]["sha256"] ==
            "f4f8ba2d342cb60e2c70b708b8847768a78ebde40dd0a52879f460cb558eab36",
            "executed_delta_source_join")
    payloads = {}
    for item in manifest["files"]:
        name = item["file"]
        payloads[name] = raw["output/result.json"] if name == "result.json" else fixed(
            args.delta_root / "output", name, (item["bytes"], item["sha256"]))
        require(receipt(name, payloads[name]) == item, "delta_payload_receipt")
    require(sorted(item.name for item in (args.delta_root / "output").iterdir()) ==
            manifest["file_roster"] and manifest["file_roster"] == sorted([*payloads, "manifest.json"]),
            "delta_roster")
    instruction = json_bytes(payloads["instruction.json"])
    unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
    require(instruction["predecessor"] == OLD_HEAD and instruction["offer"] == 8059 and
            instruction["generation"] == 8060 and instruction["rank"] == 1355 and
            instruction["lead"] == 1417 and instruction["sigma"] == 2 and
            instruction["rolling_sha256"] == sha(bytes.fromhex(OLD_HEAD) + canonical(unsigned)) == NEW_HEAD and
            checker["instruction_sha256"] == sha(payloads["instruction.json"]) ==
            result["pivot"]["instruction_sha256"] and
            result["pivot"]["head_before"] == OLD_HEAD and result["pivot"]["head_after"] == NEW_HEAD and
            result["pivot"]["normalized_sha256"] == sha(payloads["physical-normalized.bin"]),
            "delta_rolling_append")
    require(sha(payloads["lambda.bin"]) == LAMBDA_SHA and
            sha(payloads["target-remainder.bin"]) == TARGET_SHA == result["target"]["remainder_sha256"] and
            result["target"]["state_head"] == NEW_HEAD and result["target"]["state_rank"] == 1355,
            "new_separator_payloads")
    return {"manifest": manifest, "result": result, "checker": checker, "source": source,
            "lambda": unpack(payloads["lambda.bin"], WIDTH),
            "normalized": unpack(payloads["physical-normalized.bin"], WIDTH),
            "target": unpack(payloads["target-remainder.bin"], WIDTH)}


def state_dots(args: argparse.Namespace, delta: dict[str, Any]) -> dict[str, Any]:
    progress("parent_loading", parent="old_physical_rows_with_new_lambda")
    old = {name: fixed(args.state_root, name, identity) for name, identity in STATE_FILES.items()}
    state_raw = old["state/manifest.json"]
    state, head, checker = (json_bytes(old[name]) for name in
                            ("state/manifest.json", "state/HEAD", "checker-result.json"))
    identity = delta["result"]["parents"]["state"]
    require(identity["manifest_sha256"] == sha(state_raw) and identity["head"] == OLD_HEAD and
            identity["physical_sha256"] == BASE.SEPARATOR_PHYSICAL_SHA256 and
            state["generation"] == head["generation"] == 8059 and state["rank"] == head["rank"] == 1354 and
            head["manifest_sha256"] == sha(state_raw) and head["rolling_head"] == OLD_HEAD and
            checker["status"] == "PASS" and checker["physical_rank"] == 1354 and
            delta["manifest"]["parent_state_manifest_sha256"] == sha(state_raw) and
            state["instructions"]["final_head"] == OLD_HEAD and
            state["physical"]["sha256"] == BASE.SEPARATOR_PHYSICAL_SHA256 and
            state["p1_identity"]["manifest_sha256"] == BASE.P1_MANIFEST_SHA256 and
            state["p1_identity"]["cache_sha256"] == BASE.P1_CACHE_SHA256 and
            state["source_ancestry"]["prepare_body_sha256"] == BASE.TASK554_BODY_DIGESTS[0] and
            state["source_ancestry"]["parents"] == list(BASE.TASK554_BODY_DIGESTS[1:]) and
            state["task712"]["tables"]["manifest_sha256"] == BASE.ARITH.TASK712_MANIFEST_SHA,
            "delta_old_state_join")
    item = safe_file(args.state_root, "state/physical.bin")
    require(item.stat().st_size == BASE.SEPARATOR_PHYSICAL_BYTES, "physical_bytes")
    digest = hashlib.sha256()
    with item.open("rb", buffering=1 << 20) as stream:
        for index in range(1354):
            row = stream.read(ROW_BYTES)
            require(len(row) == ROW_BYTES, "physical_eof")
            digest.update(row)
            require(dot(delta["lambda"], unpack(row, WIDTH)) == 0, "new_lambda_old_row")
            if (index + 1) % 256 == 0:
                progress("separator_rows", checked=index + 1, total=1355)
        require(stream.read(1) == b"", "physical_trailing")
    require(digest.hexdigest() == BASE.SEPARATOR_PHYSICAL_SHA256 and
            dot(delta["lambda"], delta["normalized"]) == 0 and
            dot(delta["lambda"], delta["target"]) == 1, "new_lambda_pivot_and_target")
    progress("separator_rows", checked=1355, total=1355)
    return {"artifact": DELTA_ARTIFACT,
        "files": [{"file": name, "bytes": value[0], "sha256": value[1]}
                  for name, value in sorted(DELTA_FILES.items())],
        "generation": 8060, "rank": 1355, "head": NEW_HEAD, "lambda_sha256": LAMBDA_SHA,
        "old_state_derivation_premise": True,
        "old_state_manifest_sha256": sha(state_raw),
        "old_state_physical_sha256": digest.hexdigest(),
        "old_state_checker_sha256": sha(old["checker-result.json"]),
        "old_state_rows_checked": 1354, "new_pivot_rows_checked": 1,
        "lambda_pivots": 0, "lambda_saved_remainder": 1}


def task554_parent(args: argparse.Namespace) -> dict[str, Any]:
    descriptors = []
    for index, root in enumerate([args.prepare_root, *args.block_root]):
        stem = "prepare" if index == 0 else "block-" + str(index - 1)
        head = {"body_sha256": BASE.TASK554_BODY_DIGESTS[index],
            "parent_sha256": None if index == 0 else BASE.TASK554_BODY_DIGESTS[0],
            "schema": "d972.r07.a0.first-rung-grade1.v3.state.head", "stem": stem}
        head_receipt = receipt(stem + ".HEAD", canonical(head))
        body = {"file": stem + "." + BASE.TASK554_BODY_DIGESTS[index] + ".json",
                "bytes": BODY_BYTES[index], "sha256": BASE.TASK554_BODY_DIGESTS[index]}
        blobs = [d for group in BASE.OLD_BLOB_PINS for d in group] if index == 0 else [BASE.NEW_BLOB_PINS[index - 1]]
        descriptors.append({"root": str(root.resolve()), "head": head_receipt, "body": body,
            "files": [head_receipt, body] + [{key: d[key] for key in ("file", "bytes", "sha256")} for d in blobs]})
    parent = {"schema": BASE.SCHEMA + ".task554-parent.v1", "source_run": BASE.TASK554_RUN,
        "source_attempt": BASE.TASK554_ATTEMPT, "source_head": BASE.TASK554_HEAD,
        "artifacts": [{"id": a, "name": b, "bytes": c, "sha256": d} for a, b, c, d in BASE.TASK554_ARTIFACTS],
        "prepare": descriptors[0], "blocks": descriptors[1:]}
    BASE.validate_task554(parent)
    return parent


def fresh_roots(args: argparse.Namespace, delta: dict[str, Any]) -> tuple[list[dict[str, Any]], list[np.ndarray]]:
    current_identity(8060, 1355, NEW_HEAD, sha(pack(delta["lambda"])))
    tables, vectors = [], []
    for character in range(4):
        progress("fresh_B_adjoint_root", character=character, total=4)
        table = BASE.ARITH.read_task712_envelope({**BASE.TASK712_PARENT,
                                                "root": str(args.task712_root.resolve())}, character)
        BASE.check_table_transpose(table["forward"]["B"], table["adjoint"]["B"])
        vector = BASE.ARITH.sparse_adjoint(table["forward"]["B"], 36288, WIDTH, delta["lambda"])
        vectors.append(vector)
        tables.append({"identity": table["identity"], "manifest_sha256": table["manifest_sha256"]})
        progress("fresh_root_complete", character=character, support=int(np.count_nonzero(vector)))
        del table
    return tables, vectors


def projection_vectors(vectors: list[np.ndarray]) -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
    output = []
    for vector in vectors:
        support = np.flatnonzero(vector)
        output.append((support // 4, support % 4, vector[support].astype(np.uint32)))
    return output


def cache_contractions(args: argparse.Namespace, delta: dict[str, Any], vectors: list[np.ndarray]
                       ) -> tuple[dict[str, Any], np.ndarray]:
    progress("parent_loading", parent="fresh_P1_contractions")
    descriptor = {**delta["result"]["parents"]["p1"], "root": str(args.p1_root.resolve())}
    p1 = BASE.validate_p1(descriptor)
    digest = hashlib.sha256()
    with safe_file(args.p1_root, "instructions.jsonl").open("rb", buffering=1 << 20) as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    require(safe_file(args.p1_root, "instructions.jsonl").stat().st_size == BASE.P1_INSTRUCTION_BYTES and
            digest.hexdigest() == BASE.P1_INSTRUCTION_SHA256, "p1_instruction_receipt")
    values = np.zeros((4, 8059), dtype=np.uint8)
    projections = projection_vectors(vectors)
    digest = hashlib.sha256()
    cursor = 0
    with safe_file(args.p1_root, "degree2.cache.bin").open("rb", buffering=1 << 20) as stream:
        while cursor < 8059:
            count = min(256, 8059 - cursor)
            raw = stream.read(count * 36288)
            require(len(raw) == count * 36288, "p1_cache_eof")
            digest.update(raw)
            packed = np.frombuffer(raw, dtype=np.uint8).reshape(count, 36288)
            require(not np.any(packed > 80), "p1_cache_packing")
            for character, projection in enumerate(projections):
                values[character, cursor:cursor + count] = BASE.vectorized_projection_chunk(
                    packed, character * 9072, [projection])[:, 0]
            cursor += count
            progress("fresh_P1_contractions", rows=cursor, total=8059, root_vectors=4)
        require(stream.read(1) == b"", "p1_cache_trailing")
    require(digest.hexdigest() == BASE.P1_CACHE_SHA256, "p1_cache_hash")
    return p1, values


def direct_seeds(vectors: list[np.ndarray]) -> tuple[list[dict[str, Any]], np.ndarray]:
    context, words = BASE.checker_source_context()
    records, direct = [], np.zeros((4, 44), dtype=np.uint8)
    for character, vector in enumerate(vectors):
        progress("raw_direct_seeds", character=character, seeds=44)
        evaluated = BASE.checker_raw_seed_direct(context, words, vector, character, actual_pin=False)
        records.append(evaluated["receipt"])
        direct[character] = evaluated["values"]
        progress("raw_direct_seeds_complete", character=character, completed=44)
    return records, direct


def fold_expression(accum: np.ndarray, values: np.ndarray, expression: list[list[int]],
                    seed: int, offset: int) -> None:
    if not expression:
        return
    indices = np.array([offset + index for index, _ in expression], dtype=np.int64)
    weights = np.array([value for _, value in expression], dtype=np.int64)
    deduction = np.sum(values[:, indices].astype(np.int64) * weights, axis=1) % 3
    accum[:, seed] = (accum[:, seed].astype(np.int64) - deduction) % 3


def fold_seeds(parent: dict[str, Any], direct: np.ndarray, values: np.ndarray
                ) -> tuple[np.ndarray, list[str], list[int]]:
    require(direct.shape == (4, 44) and values.shape == (4, 8059), "seed_fold_shape")
    accum = direct.copy()
    heads, counts = [ZERO_HEAD] * 44, [0] * 44
    descriptors = [parent["prepare"], *parent["blocks"]]
    for block_index, descriptor in enumerate(descriptors):
        progress("seed_relations_body", body=block_index + 1, total=5)
        state = BASE.state_descriptor(descriptor, block_index - 1)
        for source in range(4):
            for seed in range(44):
                if block_index == 0:
                    expression = state["body"]["old_blocks"][source]["record"]["seed_reductions"][seed]
                    offset, target, role = OLD_OFFSETS[source], None, "prepare-old"
                else:
                    expression = state["body"]["origin_reductions"][BASE.ORIGIN_RANGES[source][0] + seed]
                    offset, target, role = NEW_OFFSETS[block_index - 1], block_index - 1, "new-block"
                for ordinal, (local, coefficient) in enumerate(expression):
                    event = {"event_id": counts[seed], "body_role": role,
                        "task554_body_sha256": state["body_sha256"], "source_character": source,
                        "target_character": target, "seed": seed,
                        "origin_id": BASE.ORIGIN_RANGES[source][0] + seed, "term_ordinal": ordinal,
                        "local_index": local, "global_index": offset + local, "coefficient": coefficient}
                    heads[seed] = sha(bytes.fromhex(heads[seed]) + canonical(event))
                    counts[seed] += 1
                fold_expression(accum, values, expression, seed, offset)
        del expression, state
        progress("seed_relations_body_complete", body=block_index + 1, total=5, seed_relations=44)
    return accum, heads, counts


def root_receipt(character: int, table: dict[str, Any], vector: np.ndarray) -> dict[str, Any]:
    require(vector.shape == (36288,) and not np.any(vector > 2), "fresh_q_shape")
    packed = pack(vector)
    return seal({"schema": BASE.ARITH.LIVE_SCHEMA + ".RawDual",
        "separator_generation": 8060, "separator_s_head_sha256": NEW_HEAD,
        "lambda_sha256": LAMBDA_SHA, "character": character,
        "B_adj_table_identity": table["identity"]["adjoint:B"],
        "word_node": {"kind": "root", "character": character, "actors": []},
        "actor_table_identities_along_w": [], "raw_q_packed_sha256": sha(packed),
        "raw_q_packed_offset": 0, "raw_q_packed_length": len(packed),
        "raw_predecessor_sha256": None})


def fresh_raw_identity(record: dict[str, Any]) -> None:
    check_seal(record)
    current_identity(record["separator_generation"], 1355,
                     record["separator_s_head_sha256"], record["lambda_sha256"])
    require(record["word_node"] == {"kind": "root", "character": record["character"], "actors": []} and
            record["actor_table_identities_along_w"] == [] and record["raw_predecessor_sha256"] is None,
            "root_only_raw_dual")


def scalar_records(scalars: np.ndarray, roots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    require(scalars.shape == (4, 44) and not np.any(scalars > 2) and len(roots) == 4,
            "fixed_176_scalar_scope")
    for root in roots:
        fresh_raw_identity(root)
    records, previous = [], ZERO_HEAD
    for index in range(176):
        character, seed = divmod(index, 44)
        unsigned = {"index": index, "character": character, "seed": seed, "origin_id": seed,
            "origin_kind": "seed", "scalar": int(scalars[character, seed]),
            "raw_dual_sha256": roots[character]["sha256"]}
        previous = sha(bytes.fromhex(previous) + canonical(unsigned))
        records.append({**unsigned, "rolling_sha256": previous})
    return records


def terminal_record(records: list[dict[str, Any]]) -> tuple[str, dict[str, Any] | None]:
    require(len(records) == 176, "root_seed_terminal_eof")
    for record in records:
        if record["scalar"]:
            return "ROOT_SEED_VIOLATION", record
    return "ROOT_SEEDS_ZERO", None


def path_independent(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: path_independent(item) for key, item in value.items() if key != "root"}
    if isinstance(value, list):
        return [path_independent(item) for item in value]
    return value


def expected_payloads(delta: dict[str, Any], separator: dict[str, Any], task554: dict[str, Any],
                      tables: list[dict[str, Any]], vectors: list[np.ndarray], values: np.ndarray,
                      direct_receipts: list[dict[str, Any]], direct: np.ndarray,
                      scalars: np.ndarray, heads: list[str], counts: list[int]
                      ) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Serialize independently computed values; no candidate receipt is an authority."""
    parents = delta["result"]["parents"]
    require(task554["artifacts"] == parents["task554"]["artifacts"] and
            list(BASE.TASK554_BODY_DIGESTS) == parents["task554"]["body_sha256"] and
            BASE.TASK712_PARENT == parents["task712"]["artifact"] and
            all(table["manifest_sha256"] == parents["task712"]["manifest_sha256"] for table in tables),
            "unchanged_parent_joins")
    launch = seal({"schema": SCHEMA + ".launch", "scope": SCOPE, "claims": CLAIMS,
        "lineages": LINEAGES, "separator": separator, "p1_parent": parents["p1"],
        "task554_parent": path_independent(task554), "task712_parent": dict(BASE.TASK712_PARENT),
        "task712_manifest_sha256": [table["manifest_sha256"] for table in tables],
        "fixture_only": False, "verified": False, "cross_checked": False})
    roots = [root_receipt(a, tables[a], vectors[a]) for a in range(4)]
    cache = {"rows": 8059, "cache_passes": 1, "instruction_hash_passes": 1,
        "cache_sha256": BASE.P1_CACHE_SHA256, "instruction_sha256": BASE.P1_INSTRUCTION_SHA256,
        "active_characters": [a for a, vector in enumerate(vectors) if np.any(vector)],
        "root_vectors": 4, "chunk_rows": 256, "value_sha256": [sha(row.tobytes()) for row in values]}
    relation = seal({"schema": SCHEMA + ".seed-relations",
        "task554_body_sha256": list(BASE.TASK554_BODY_DIGESTS),
        "old_offsets": list(OLD_OFFSETS), "new_offsets": list(NEW_OFFSETS),
        "event_order": "old-source,then-target/source,stored-term-order", "seed_count": 44,
        "body_passes": 5, "actor_origins_executed": 0,
        "seed_records": [seal({"schema": SCHEMA + ".seed-relation", "seed": seed,
            "raw_event_count": counts[seed], "raw_event_head": heads[seed]}) for seed in range(44)]})
    records = scalar_records(scalars, roots)
    stream_raw = b"".join(canonical(record) for record in records)
    payloads, characters = {}, []
    for character in range(4):
        items = [
            (f"q-a{character}-root.bin", pack(vectors[character])),
            (f"p1-values-a{character}.bin", values[character].tobytes()),
            (f"direct-seeds-a{character}.bin", direct[character].tobytes()),
            (f"seed-scalars-a{character}.bin", scalars[character].tobytes()),
        ]
        payloads.update(items)
        nonzero = np.flatnonzero(scalars[character])
        characters.append(seal({"schema": SCHEMA + ".character", "character": character,
            "character_label": list(BASE.CHARACTERS[character]), "raw_dual": roots[character],
            "root_support": int(np.count_nonzero(vectors[character])),
            "direct_receipt": direct_receipts[character],
            "files": [receipt(name, data) for name, data in items],
            "first_nonzero_seed": int(nonzero[0]) if len(nonzero) else None,
            "all_seeds_zero": len(nonzero) == 0}))
    terminal, first = terminal_record(records)
    violation = None
    if first is not None:
        character = first["character"]
        violation = seal({"schema": SCHEMA + ".RootSeedViolation", **first,
            "separator_generation": 8060, "separator_head": NEW_HEAD, "lambda_sha256": LAMBDA_SHA,
            "delta_manifest_sha256": DELTA_FILES["output/manifest.json"][1],
            "raw_q_packed_sha256": roots[character]["raw_q_packed_sha256"],
            "p1_manifest_sha256": BASE.P1_MANIFEST_SHA256,
            "value_vector_sha256": cache["value_sha256"][character],
            "direct_receipt_sha256": direct_receipts[character]["sha256"],
            "seed_relation_sha256": relation["seed_records"][first["seed"]]["sha256"],
            "relation_receipt_sha256": relation["sha256"], "materialization_performed": False})
    result = seal({"schema": SCHEMA + ".result", "status": "PASS", "terminal": terminal,
        "launch_sha256": sha(canonical(launch)), "scope": SCOPE, "claims": CLAIMS,
        "separator_generation": 8060, "separator_rank": 1355, "separator_head": NEW_HEAD,
        "lambda_sha256": LAMBDA_SHA, "formula_id": FORMULA, "characters": characters,
        "cache_receipt": cache, "relation_receipt": relation,
        "scalar_stream": receipt("scalars.jsonl", stream_raw),
        "scalar_final_head": records[-1]["rolling_sha256"], "first_violation": violation,
        "actor_origins_executed": 0, "orbit_rows_executed": 0, "materialization_performed": False,
        "old_derivation_premise": True, "shared_accepted_lineages": True,
        "verified": False, "cross_checked": False})
    payloads.update({"launch.json": canonical(launch), "scalars.jsonl": stream_raw,
                     "result.json": canonical(result)})
    manifest = seal({"schema": SCHEMA + ".manifest", "terminal": terminal, "candidate": True,
        "files": [receipt(name, payloads[name]) for name in sorted(payloads)],
        "file_roster": sorted([*payloads, "manifest.json"]),
        "result_sha256": sha(canonical(result)), "scope": SCOPE,
        "verified": False, "cross_checked": False})
    payloads["manifest.json"] = canonical(manifest)
    return payloads, result


def compare_candidate(root: Path, payloads: dict[str, bytes]) -> None:
    require(root.is_dir() and not root.is_symlink(), "candidate_directory")
    require(sorted(item.name for item in root.iterdir()) == sorted(payloads), "candidate_exact_roster")
    for name in sorted(payloads):
        expected = payloads[name]
        actual = fixed(root, name, (len(expected), sha(expected)))
        require(actual == expected, "candidate_bytes:" + name)


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    require(args.candidate_root.is_dir(), "candidate_directory")
    for root in [args.delta_root, args.state_root, args.prepare_root, *args.block_root,
                 args.p1_root, args.task712_root]:
        require(root.is_dir() and not root.is_symlink() and
                root.resolve() != args.candidate_root.resolve() and
                root.resolve() not in args.candidate_root.resolve().parents and
                args.candidate_root.resolve() not in root.resolve().parents, "disjoint_candidate")
    delta = load_delta(args)
    separator = state_dots(args, delta)
    task554 = task554_parent(args)
    tables, vectors = fresh_roots(args, delta)
    _, values = cache_contractions(args, delta, vectors)
    receipts, direct = direct_seeds(vectors)
    scalars, heads, counts = fold_seeds(task554, direct, values)
    payloads, result = expected_payloads(delta, separator, task554, tables, vectors, values,
                                       receipts, direct, scalars, heads, counts)
    progress("candidate_comparison", files=len(payloads), scalars=176)
    compare_candidate(args.candidate_root, payloads)
    progress("terminal", status="PASS", terminal=result["terminal"], scalars=176,
             actor_origins=0, orbit_rows=0)
    return {"schema": SCHEMA + ".checker", "status": "PASS", "terminal": result["terminal"],
        "manifest_sha256": sha(payloads["manifest.json"]), "result_sha256": sha(payloads["result.json"]),
        "separator_generation": 8060, "separator_rank": 1355, "separator_head": NEW_HEAD,
        "lambda_sha256": LAMBDA_SHA, "files_compared": len(payloads), "scalars": 176,
        "first_violation": result["first_violation"], "cache_passes": 1, "root_vectors": 4,
        "old_state_rows_checked": 1354, "new_pivot_rows_checked": 1,
        "lambda_pivots": 0, "lambda_saved_remainder": 1,
        "actor_origins_executed": 0, "orbit_rows_executed": 0,
        "materialization_performed": False, "old_derivation_premise": True,
        "shared_accepted_lineages": True, "claims": CLAIMS,
        "verified": False, "cross_checked": False}


def rejects(action: Callable[[], Any], name: str) -> None:
    try:
        action()
    except (ValueError, KeyError, TypeError):
        return
    raise ValueError("rank1355_checker:canary_accepted:" + name)


def selftest() -> dict[str, Any]:
    """Five bounded synthetic checks, with no parent or old workflow execution."""
    vectors = [np.zeros(36288, dtype=np.uint8) for _ in range(4)]
    vectors[1][1], vectors[2][7] = 2, 1
    packed = np.zeros((2, 36288), dtype=np.uint8)
    packed[:, 9072] = [6, 3]
    packed[:, 18145] = [27, 54]
    projected = np.vstack([BASE.vectorized_projection_chunk(packed, a * 9072, [projection])[:, 0]
                           for a, projection in enumerate(projection_vectors(vectors))])
    require(projected.tolist() == [[0, 0], [1, 2], [1, 2], [0, 0]], "dynamic_roots_canary")
    table = {"identity": {"adjoint:B": "synthetic-B-adjoint"}}
    roots = [root_receipt(a, table, vector) for a, vector in enumerate(vectors)]
    stale = seal({**{key: value for key, value in roots[1].items() if key != "sha256"},
                  "separator_s_head_sha256": OLD_HEAD})
    rejects(lambda: fresh_raw_identity(stale), "coherently_sealed_stale_head")
    direct, values = np.zeros((4, 44), dtype=np.uint8), np.zeros((4, 8059), dtype=np.uint8)
    direct[:, 6] = [1, 2, 0, 1]
    values[:, 7] = [2, 1, 2, 1]
    values[:, 8] = [2, 0, 1, 2]
    fold_expression(direct, values, [[1, 2], [0, 1], [0, 2]], 6, 7)
    require(direct[:, 6].tolist() == [0, 2, 1, 0], "stored_duplicates_and_global_offset_canary")
    scalars = np.zeros((4, 44), dtype=np.uint8)
    scalars[2, 3], scalars[3, 0] = 2, 1
    records = scalar_records(scalars, roots)
    terminal, first = terminal_record(records)
    require(terminal == "ROOT_SEED_VIOLATION" and first is not None and first["index"] == 91 and
            first["character"] == 2 and first["seed"] == 3 and
            all(record["origin_kind"] == "seed" and record["origin_id"] == record["seed"] and
                (record["character"], record["seed"]) == divmod(record["index"], 44) for record in records),
            "fixed_176_seed_order_canary")
    zero_records = scalar_records(np.zeros_like(scalars), roots)
    require(terminal_record(zero_records) == ("ROOT_SEEDS_ZERO", None) and
            SCOPE["actor_origins_executed"] == SCOPE["orbit_rows_executed"] == 0 and
            CLAIMS["GRADE2_MEMBER"] == CLAIMS["GRADE2_NONMEMBER"] == "NOT_DECIDED",
            "root_seeds_zero_only_canary")
    return {"status": "PASS", "synthetic_only": True,
        "tests": ["dynamic-four-root-projections", "coherently-sealed-stale-head",
                  "stored-duplicates-global-offset", "176-seed-order-first-hit", "root-seeds-zero-only"],
        "verified": False, "cross_checked": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    fields = ("delta_root", "state_root", "prepare_root", "p1_root", "task712_root", "candidate_root")
    for field in fields:
        parser.add_argument("--" + field.replace("_", "-"), type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    try:
        if args.selftest:
            require(not args.block_root and all(getattr(args, field) is None for field in fields),
                    "synthetic_without_parents")
            result = selftest()
        else:
            require(len(args.block_root) == 4 and all(getattr(args, field) is not None for field in fields),
                    "fixed_parent_paths_required")
            result = check_actual(args)
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 0
    except Exception as exc:
        progress("terminal", status="REJECTED", reason=str(exc), error_type=type(exc).__name__)
        print(canonical({"status": "REJECTED", "reason": str(exc), "verified": False,
                         "cross_checked": False}).decode("ascii"), end="", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
