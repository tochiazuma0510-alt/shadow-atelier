#!/usr/bin/env python3
"""Fixed rank1355 separator -> 176 corrected root-seed scalars, candidate only.

The accepted old state and one seed30 delta are premises.  Only fresh root
covectors, fresh P1 contractions and seed relations are evaluated here.  No
actor origin, orbit, state construction or source-word materializer runs.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any

import numpy as np


SCHEMA = "d972.r07.rank1355.root-seed-scalars.v1"
SEARCH = Path(__file__).resolve().parent
ZERO_HEAD = "0" * 64
NEW_GENERATION = 8060
NEW_RANK = 1355
NEW_HEAD = "36feb776736c6587ce9f64d6f5acb883385074a7cc2eed4c2ce7eb8675e71342"
NEW_LAMBDA = "f83bbaa503b8a4d5056f0779085ee4eced542eb1d78d3e35fa9df1c281960565"
OLD_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"
BODY_BYTES = (15398340, 74883943, 75400514, 75340879, 75407216)
OLD_OFFSETS = (0, 505, 1008, 1511)
NEW_OFFSETS = (2014, 3523, 5035, 6547)
FORMULA = "r07.v541.formulas-2.1-2.2-4.1.raw-seed-plus-actor-lower-adjoint"
LINEAGES = {
    "producer": {
        "d972_r07_actual_grade2_root_scalar_batch_v2.py": "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
        "d972_r07_targeted_grade2_owner_generated_join_v15.py": "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632",
    },
    "checker": {
        "check_d972_r07_actual_grade2_root_scalar_batch_v2.py": "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6",
        "check_d972_r07_targeted_grade2_owner_generated_join_v15.py": "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662",
    },
}
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
SCOPE = {"characters": [0, 1, 2, 3], "seeds": list(range(44)),
         "scalar_order": "character-major/seed0-through43", "scalar_count": 176,
         "actor_origins_executed": 0, "orbit_rows_executed": 0}
CLAIMS = {"ROOT_SEED_SCALARS_CANDIDATE": True, "GRADE2_MEMBER": "NOT_DECIDED",
          "GRADE2_NONMEMBER": "NOT_DECIDED", "A0": "NOT_DECLARED",
          "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
          "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sealed(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    value = {"schema": SCHEMA + "." + kind, **body}
    require("sha256" not in value, "double_seal")
    return {**value, "sha256": sha(canonical(value))}


def check_seal(value: Any) -> None:
    require(isinstance(value, dict) and value.get("sha256") == sha(canonical(
        {key: item for key, item in value.items() if key != "sha256"})), "object_seal")


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def safe_file(root: Path, name: str) -> Path:
    require(isinstance(name, str) and name and not Path(name).is_absolute() and
            ".." not in Path(name).parts and ":" not in name and "\\" not in name, "relative_path")
    base = root.resolve()
    path = base
    for part in Path(name).parts:
        path /= part
        require(not path.is_symlink(), "symlink")
    require(path.is_file() and base in path.resolve().parents, "file_escape_or_missing")
    return path


def receipt(name: str, raw: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def fixed(root: Path, name: str, pin: tuple[int, str]) -> bytes:
    path = safe_file(root, name)
    require(path.stat().st_size == pin[0], "fixed_size:" + name)
    raw = path.read_bytes()
    require(len(raw) == pin[0] and sha(raw) == pin[1], "fixed_hash:" + name)
    return raw


def json_value(raw: bytes) -> Any:
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw, "canonical_json")
    return value


def load_base() -> Any:
    for name, wanted in LINEAGES["producer"].items():
        require(sha(safe_file(SEARCH, name).read_bytes()) == wanted, "producer_lineage_pin:" + name)
    if str(SEARCH) not in sys.path:
        sys.path.insert(0, str(SEARCH))
    path = SEARCH / "d972_r07_actual_grade2_root_scalar_batch_v2.py"
    spec = importlib.util.spec_from_file_location("task937_accepted_root_v2", path)
    require(spec is not None and spec.loader is not None, "base_spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.verify_source_pin()
    return module


def pinned_parent_descriptors(base: Any, args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    p1 = {
        "root": str(args.p1_root.resolve()), "run": base.P1_RUN, "attempt": base.P1_ATTEMPT,
        "head": base.P1_HEAD, "artifact": base.P1_ARTIFACT, "artifact_name": base.P1_ARTIFACT_NAME,
        "archive_bytes": base.P1_ARCHIVE_BYTES, "archive_sha256": base.P1_ARCHIVE_SHA256,
        "manifest": {"file": "manifest.json", "bytes": base.P1_MANIFEST_BYTES,
                     "sha256": base.P1_MANIFEST_SHA256},
        "files": [{"file": "degree2.cache.bin", "bytes": base.P1_CACHE_BYTES,
                   "sha256": base.P1_CACHE_SHA256},
                  {"file": "instructions.jsonl", "bytes": base.P1_INSTRUCTION_BYTES,
                   "sha256": base.P1_INSTRUCTION_SHA256}],
    }
    states = []
    for index, root in enumerate([args.prepare_root, *args.block_root]):
        stem = "prepare" if index == 0 else "block-" + str(index - 1)
        head_raw = canonical({"body_sha256": base.TASK554_BODY_DIGESTS[index],
            "parent_sha256": None if index == 0 else base.TASK554_BODY_DIGESTS[0],
            "schema": "d972.r07.a0.first-rung-grade1.v3.state.head", "stem": stem})
        head = receipt(stem + ".HEAD", head_raw)
        body = {"file": stem + "." + base.TASK554_BODY_DIGESTS[index] + ".json",
                "bytes": BODY_BYTES[index], "sha256": base.TASK554_BODY_DIGESTS[index]}
        blobs = ([blob for pair in base.OLD_BLOB_PINS for blob in pair]
                 if index == 0 else [base.NEW_BLOB_PINS[index - 1]])
        states.append({"root": str(root.resolve()), "head": head, "body": body,
                       "files": [head, body] + [{key: blob[key] for key in ("file", "bytes", "sha256")}
                                                for blob in blobs]})
    task554 = {"schema": base.SCHEMA + ".task554-parent.v1",
               "source_run": base.TASK554_RUN, "source_attempt": base.TASK554_ATTEMPT,
               "source_head": base.TASK554_HEAD,
               "artifacts": [{"id": item[0], "name": item[1], "bytes": item[2], "sha256": item[3]}
                             for item in base.TASK554_ARTIFACTS],
               "prepare": states[0], "blocks": states[1:]}
    tables = [{**base.TASK712_PARENT, "root": str(args.task712_root.resolve())} for _ in range(4)]
    return p1, task554, tables


def load_separator(base: Any, args: argparse.Namespace) -> dict[str, Any]:
    progress("parent-loading", parent="rank1355-delta")
    objects = {name: json_value(fixed(args.delta_root, name, pin)) for name, pin in DELTA_FILES.items()}
    manifest = objects["output/manifest.json"]
    result = objects["output/result.json"]
    instruction = objects["output/instruction.json"]
    checker = objects["checker-result.json"]
    for item in (manifest, result, result["pivot"], result["target"]):
        check_seal(item)
    require(manifest["mode"] == "parent-plus-one-pivot-delta" and
            manifest["parent_state_head"] == OLD_HEAD and manifest["state_head"] == NEW_HEAD and
            manifest["rank_before"] == 1354 and manifest["rank_after"] == NEW_RANK and
            manifest["terminal"] == result["kind"] == checker["kind"] == "Separator" and
            checker["status"] == "PASS" and checker["manifest_sha256"] == DELTA_FILES["output/manifest.json"][1] and
            checker["result_sha256"] == DELTA_FILES["output/result.json"][1] and
            checker["state_head"] == NEW_HEAD and checker["rank_after"] == NEW_RANK and
            checker["new_pivots"] == 1 and checker["old_state_derivation_premise"] is True and
            all(item["verified"] is False and item["cross_checked"] is False
                for item in (manifest, result, checker, objects["source-receipt.json"])), "delta_authority")
    output = args.delta_root / "output"
    require(set(manifest["file_roster"]) == {p.name for p in output.iterdir()}, "delta_roster")
    payloads: dict[str, bytes] = {}
    for item in manifest["files"]:
        key = "output/" + item["file"]
        if key in DELTA_FILES:
            require((item["bytes"], item["sha256"]) == DELTA_FILES[key], "delta_embedded_receipt")
        else:
            payloads[item["file"]] = fixed(output, item["file"], (item["bytes"], item["sha256"]))
    unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
    require(instruction["predecessor"] == OLD_HEAD and instruction["rolling_sha256"] == NEW_HEAD and
            sha(bytes.fromhex(OLD_HEAD) + canonical(unsigned)) == NEW_HEAD and
            instruction["generation"] == result["pivot"]["generation_after"] == NEW_GENERATION and
            instruction["rank"] == NEW_RANK and instruction["lead"] == 1417 and instruction["sigma"] == 2 and
            checker["instruction_sha256"] == DELTA_FILES["output/instruction.json"][1] and
            result["pivot"]["head_after"] == NEW_HEAD and
            result["target"]["state_head"] == NEW_HEAD, "delta_single_append")
    require(sha(payloads["lambda.bin"]) == NEW_LAMBDA == result["separator"]["lambda_sha256"] and
            sha(payloads["physical-normalized.bin"]) == result["pivot"]["normalized_sha256"] and
            sha(payloads["target-remainder.bin"]) == result["target"]["remainder_sha256"], "delta_new_rows")
    lam = base.ARITH.unpack_trits(payloads["lambda.bin"], 48384)
    new_row = base.ARITH.unpack_trits(payloads["physical-normalized.bin"], 48384)
    remainder = base.ARITH.unpack_trits(payloads["target-remainder.bin"], 48384)
    require(base.ARITH.dot_mod3(lam, new_row) == 0 and
            base.ARITH.dot_mod3(lam, remainder) == 1, "new_separator_delta_pairings")
    old = {name: json_value(fixed(args.state_root, name, pin)) for name, pin in STATE_FILES.items()}
    state = old["state/manifest.json"]
    head = old["state/HEAD"]
    old_checker = old["checker-result.json"]
    require(state["rank"] == head["rank"] == 1354 and state["generation"] == head["generation"] == 8059 and
            head["rolling_head"] == OLD_HEAD and state["instructions"]["final_head"] == OLD_HEAD and
            head["manifest_sha256"] == STATE_FILES["state/manifest.json"][1] and
            old_checker["status"] == "PASS" and old_checker["physical_rank"] == 1354 and
            result["parents"]["state"]["manifest_sha256"] == STATE_FILES["state/manifest.json"][1] and
            result["parents"]["state"]["head"] == OLD_HEAD and
            result["parents"]["state"]["physical_sha256"] == base.SEPARATOR_PHYSICAL_SHA256 and
            manifest["parent_state_manifest_sha256"] == STATE_FILES["state/manifest.json"][1], "old_state_premise_join")
    physical = safe_file(args.state_root, "state/physical.bin")
    require(physical.stat().st_size == base.SEPARATOR_PHYSICAL_BYTES, "old_physical_size")
    digest = hashlib.sha256()
    with physical.open("rb", buffering=1 << 20) as stream:
        for index in range(1354):
            packed = stream.read(12096)
            require(len(packed) == 12096, "old_physical_eof")
            digest.update(packed)
            row = base.ARITH.unpack_trits(packed, 48384)
            require(base.ARITH.dot_mod3(lam, row) == 0, "new_lambda_old_row")
            if (index + 1) % 256 == 0 or index == 1353:
                progress("parent-loading", parent="old-physical-new-lambda", rows=index + 1, total=1354)
        require(stream.read(1) == b"", "old_physical_trailing")
    require(digest.hexdigest() == base.SEPARATOR_PHYSICAL_SHA256 == state["physical"]["sha256"], "old_physical_hash")
    return {"lambda": lam, "delta_result": result, "old_manifest": state,
            "receipt": {"artifact": DELTA_ARTIFACT,
                "files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(DELTA_FILES.items())],
                "generation": NEW_GENERATION, "rank": NEW_RANK, "head": NEW_HEAD,
                "lambda_sha256": NEW_LAMBDA, "old_state_derivation_premise": True,
                "old_state_manifest_sha256": STATE_FILES["state/manifest.json"][1],
                "old_state_physical_sha256": digest.hexdigest(),
                "old_state_checker_sha256": STATE_FILES["checker-result.json"][1],
                "old_state_rows_checked": 1354, "new_pivot_rows_checked": 1,
                "lambda_pivots": 0, "lambda_saved_remainder": 1}}


def new_roots(base: Any, table_parents: list[dict[str, Any]], lam: np.ndarray) -> tuple[list[Any], list[np.ndarray]]:
    tables = []
    roots = []
    for character in range(4):
        table = base.ARITH.read_task712_envelope(table_parents[character], character)
        base.check_table_transpose(table["forward"]["B"], table["adjoint"]["B"])
        q = base.ARITH.sparse_adjoint(table["forward"]["B"], 36288, 48384, lam)
        require(q.shape == (36288,) and not np.any(q > 2), "new_root_shape")
        tables.append(table)
        roots.append(q)
        progress("fresh-root", character=character, support=int(np.count_nonzero(q)))
    return tables, roots


def root_record(base: Any, character: int, table: Any, q: np.ndarray) -> dict[str, Any]:
    raw = base.ARITH.pack_trits(q)
    body = {"schema": base.ARITH.LIVE_SCHEMA + ".RawDual",
        "separator_generation": NEW_GENERATION, "separator_s_head_sha256": NEW_HEAD,
        "lambda_sha256": NEW_LAMBDA, "character": character,
        "B_adj_table_identity": table["identity"]["adjoint:B"],
        "word_node": {"kind": "root", "character": character, "actors": []},
        "actor_table_identities_along_w": [], "raw_q_packed_sha256": sha(raw),
        "raw_q_packed_offset": 0, "raw_q_packed_length": len(raw), "raw_predecessor_sha256": None}
    return {**body, "sha256": sha(canonical(body))}


def p1_root_values(base: Any, p1: Any, roots: list[np.ndarray]) -> tuple[np.ndarray, dict[str, Any]]:
    progress("p1-contractions", rows=0, total=8059)
    instruction = safe_file(p1["root"], p1["instruction"]["path"])
    _, instruction_sha = base.file_hash(instruction, base.P1_INSTRUCTION_BYTES, 1 << 30)
    require(instruction_sha == base.P1_INSTRUCTION_SHA256, "p1_instruction_pin")
    active = [a for a, root in enumerate(roots) if np.any(root)]
    projections = []
    for root in roots:
        indices = np.flatnonzero(root)
        projections.append([(indices // 4, indices % 4, root[indices].astype(np.uint32))])
    values = np.zeros((4, 8059), dtype=np.uint8)
    digest = hashlib.sha256()
    buffer = bytearray(base.P1_ROW_BYTES * 256)
    with safe_file(p1["root"], p1["cache"]["path"]).open("rb", buffering=1 << 20) as stream:
        for cursor in range(0, 8059, 256):
            rows = min(256, 8059 - cursor)
            count = rows * base.P1_ROW_BYTES
            require(stream.readinto(memoryview(buffer)[:count]) == count, "p1_cache_eof")
            chunk = memoryview(buffer)[:count]
            digest.update(chunk)
            packed = np.frombuffer(chunk, dtype=np.uint8).reshape(rows, base.P1_ROW_BYTES)
            require(not np.any(packed > 80), "p1_packed_bytes")
            for character in active:
                values[character, cursor:cursor + rows] = base.vectorized_projection_chunk(
                    packed, character * 9072, projections[character])[:, 0]
            progress("p1-contractions", rows=cursor + rows, total=8059)
        require(stream.read(1) == b"", "p1_cache_trailing")
    require(digest.hexdigest() == base.P1_CACHE_SHA256, "p1_cache_pin")
    return values, {"rows": 8059, "cache_passes": 1, "instruction_hash_passes": 1,
                    "cache_sha256": digest.hexdigest(), "instruction_sha256": instruction_sha,
                    "active_characters": active, "root_vectors": 4, "chunk_rows": 256,
                    "value_sha256": [sha(row.tobytes()) for row in values]}


def seed_only_fold(base: Any, parent: Any, direct: np.ndarray,
                   values: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    require(direct.shape == (4, 44) and values.shape == (4, 8059), "seed_fold_shape")
    scalars = direct.copy()
    heads = [ZERO_HEAD] * 44
    counts = [0] * 44

    def fold(expression: list[Any], source: int, target: int | None,
             seed: int, offset: int, body_sha: str) -> None:
        for ordinal, (local, coefficient) in enumerate(expression):
            node = offset + local
            event = {"event_id": counts[seed], "body_role": "prepare-old" if target is None else "new-block",
                "task554_body_sha256": body_sha, "source_character": source,
                "target_character": target, "seed": seed,
                "origin_id": base.ORIGIN_RANGES[source][0] + seed,
                "term_ordinal": ordinal, "local_index": local, "global_index": node,
                "coefficient": coefficient}
            heads[seed] = sha(bytes.fromhex(heads[seed]) + canonical(event))
            counts[seed] += 1
            scalars[:, seed] = (scalars[:, seed].astype(np.uint16) +
                               (3 - coefficient) * values[:, node].astype(np.uint16)) % 3

    progress("seed-relations", body="prepare", completed=0, total=5)
    prepare = base._state_descriptor(parent["prepare"], -1, need_blobs=True)
    for source, old in enumerate(prepare["body"]["old_blocks"]):
        for seed in range(44):
            fold(old["record"]["seed_reductions"][seed], source, None, seed,
                 OLD_OFFSETS[source], prepare["body_sha256"])
    del old, prepare
    for target in range(4):
        progress("seed-relations", body="block-" + str(target), completed=target + 1, total=5)
        block = base._state_descriptor(parent["blocks"][target], target, need_blobs=True)
        for source in range(4):
            for seed in range(44):
                fold(block["body"]["origin_reductions"][base.ORIGIN_RANGES[source][0] + seed],
                     source, target, seed, NEW_OFFSETS[target], block["body_sha256"])
        del block
    progress("seed-relations", completed=5, total=5)
    relation = sealed("seed-relations", {
        "task554_body_sha256": list(base.TASK554_BODY_DIGESTS),
        "old_offsets": list(OLD_OFFSETS), "new_offsets": list(NEW_OFFSETS),
        "event_order": "old-source,then-target/source,stored-term-order",
        "seed_count": 44, "body_passes": 5, "actor_origins_executed": 0,
        "seed_records": [sealed("seed-relation", {"seed": seed, "raw_event_count": counts[seed],
                          "raw_event_head": heads[seed]}) for seed in range(44)]})
    return scalars, relation


def scalar_stream(scalars: np.ndarray, raw_roots: list[dict[str, Any]]) -> tuple[bytes, list[dict[str, Any]]]:
    require(scalars.shape == (4, 44) and not np.any(scalars > 2), "176_scalar_shape")
    rolling = ZERO_HEAD
    records = []
    for character in range(4):
        for seed in range(44):
            record = {"index": len(records), "character": character, "seed": seed,
                      "origin_id": seed, "origin_kind": "seed", "scalar": int(scalars[character, seed]),
                      "raw_dual_sha256": raw_roots[character]["sha256"]}
            rolling = sha(bytes.fromhex(rolling) + canonical(record))
            records.append({**record, "rolling_sha256": rolling})
    return b"".join(canonical(record) for record in records), records


def without_roots(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: without_roots(item) for key, item in value.items() if key != "root"}
    if isinstance(value, list):
        return [without_roots(item) for item in value]
    return value


def write_file(root: Path, name: str, raw: bytes) -> dict[str, Any]:
    require(Path(name).name == name and not (root / name).exists(), "fresh_output_file")
    temporary = root / (name + ".tmp-" + str(os.getpid()))
    require(not temporary.exists(), "fresh_temporary")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, root / name)
    return receipt(name, raw)


def run_actual(args: argparse.Namespace) -> dict[str, Any]:
    require(not args.output_root.exists(), "fresh_output_root")
    parents = [args.delta_root, args.state_root, args.prepare_root, *args.block_root,
               args.p1_root, args.task712_root]
    for root in parents:
        require(root.is_dir() and args.output_root.resolve() != root.resolve() and
                root.resolve() not in args.output_root.resolve().parents and
                args.output_root.resolve() not in root.resolve().parents, "disjoint_output")
    base = load_base()
    p1_parent, task554, table_parents = pinned_parent_descriptors(base, args)
    p1 = base.validate_p1(p1_parent)
    base.validate_task554(task554)
    separator = load_separator(base, args)
    delta = separator["delta_result"]
    require(without_roots(p1_parent) == delta["parents"]["p1"] and
            task554["artifacts"] == delta["parents"]["task554"]["artifacts"] and
            list(base.TASK554_BODY_DIGESTS) == delta["parents"]["task554"]["body_sha256"] and
            base.TASK712_PARENT == delta["parents"]["task712"]["artifact"], "unchanged_parent_joins")
    tables, roots = new_roots(base, table_parents, separator["lambda"])
    require(all(table["manifest_sha256"] == delta["parents"]["task712"]["manifest_sha256"]
                for table in tables), "task712_manifest_join")
    launch = sealed("launch", {"scope": SCOPE, "claims": CLAIMS, "lineages": LINEAGES,
        "separator": separator["receipt"], "p1_parent": without_roots(p1_parent),
        "task554_parent": without_roots(task554),
        "task712_parent": dict(base.TASK712_PARENT),
        "task712_manifest_sha256": [table["manifest_sha256"] for table in tables],
        "fixture_only": False, "verified": False, "cross_checked": False})
    values, cache = p1_root_values(base, p1, roots)
    context, words = base.source_context()
    direct_results = []
    for character in range(4):
        progress("raw-seeds", character=character, seeds=44)
        direct_results.append(base.raw_seed_direct(context, words, roots[character],
                                                   character, actual_pin=False))
    direct = np.asarray([item["values"] for item in direct_results], dtype=np.uint8)
    scalars, relation = seed_only_fold(base, task554, direct, values)
    raw_roots = [root_record(base, a, tables[a], roots[a]) for a in range(4)]
    stream_raw, records = scalar_stream(scalars, raw_roots)
    payloads = []
    characters = []
    for character in range(4):
        q_raw = base.ARITH.pack_trits(roots[character])
        files = [(f"q-a{character}-root.bin", q_raw),
                 (f"p1-values-a{character}.bin", values[character].tobytes()),
                 (f"direct-seeds-a{character}.bin", direct[character].tobytes()),
                 (f"seed-scalars-a{character}.bin", scalars[character].tobytes())]
        payloads.extend(files)
        positions = np.flatnonzero(scalars[character])
        characters.append(sealed("character", {"character": character,
            "character_label": list(base.CHARACTERS[character]), "raw_dual": raw_roots[character],
            "root_support": int(np.count_nonzero(roots[character])),
            "direct_receipt": direct_results[character]["receipt"],
            "files": [receipt(name, raw) for name, raw in files],
            "first_nonzero_seed": int(positions[0]) if len(positions) else None,
            "all_seeds_zero": len(positions) == 0}))
    hit = next((record for record in records if record["scalar"]), None)
    terminal = "ROOT_SEED_VIOLATION" if hit is not None else "ROOT_SEEDS_ZERO"
    violation = None
    if hit is not None:
        character = hit["character"]
        violation = sealed("RootSeedViolation", {
            **hit, "separator_generation": NEW_GENERATION, "separator_head": NEW_HEAD,
            "lambda_sha256": NEW_LAMBDA, "delta_manifest_sha256": DELTA_FILES["output/manifest.json"][1],
            "raw_q_packed_sha256": raw_roots[character]["raw_q_packed_sha256"],
            "p1_manifest_sha256": base.P1_MANIFEST_SHA256,
            "value_vector_sha256": cache["value_sha256"][character],
            "direct_receipt_sha256": direct_results[character]["receipt"]["sha256"],
            "seed_relation_sha256": relation["seed_records"][hit["seed"]]["sha256"],
            "relation_receipt_sha256": relation["sha256"],
            "materialization_performed": False})
    result = sealed("result", {"status": "PASS", "terminal": terminal,
        "launch_sha256": sha(canonical(launch)), "scope": SCOPE, "claims": CLAIMS,
        "separator_generation": NEW_GENERATION, "separator_rank": NEW_RANK,
        "separator_head": NEW_HEAD, "lambda_sha256": NEW_LAMBDA,
        "formula_id": FORMULA, "characters": characters, "cache_receipt": cache,
        "relation_receipt": relation, "scalar_stream": receipt("scalars.jsonl", stream_raw),
        "scalar_final_head": records[-1]["rolling_sha256"], "first_violation": violation,
        "actor_origins_executed": 0, "orbit_rows_executed": 0,
        "materialization_performed": False, "old_derivation_premise": True,
        "shared_accepted_lineages": True, "verified": False, "cross_checked": False})
    args.output_root.mkdir(parents=True, exist_ok=False)
    files = [write_file(args.output_root, name, raw) for name, raw in payloads]
    files.append(write_file(args.output_root, "launch.json", canonical(launch)))
    files.append(write_file(args.output_root, "scalars.jsonl", stream_raw))
    files.append(write_file(args.output_root, "result.json", canonical(result)))
    manifest = sealed("manifest", {"terminal": terminal, "candidate": True,
        "files": sorted(files, key=lambda item: item["file"]),
        "file_roster": sorted([item["file"] for item in files] + ["manifest.json"]),
        "result_sha256": sha(canonical(result)), "scope": SCOPE,
        "verified": False, "cross_checked": False})
    manifest_receipt = write_file(args.output_root, "manifest.json", canonical(manifest))
    progress("terminal", terminal=terminal, scalars=176, actor_origins=0, orbit_rows=0)
    return {"status": "PASS", "terminal": terminal, "scalars": 176,
            "manifest_sha256": manifest_receipt["sha256"], "first_violation": violation,
            "verified": False, "cross_checked": False}


def selftest() -> dict[str, Any]:
    base = load_base()
    q = np.zeros(36288, dtype=np.uint8)
    q[4] = 2
    roots = [np.zeros_like(q), q, np.zeros_like(q), q.copy()]
    require([a for a, root in enumerate(roots) if np.any(root)] == [1, 3], "dynamic_root_canary")
    table = {"identity": {"adjoint:B": "synthetic-B-adjoint"}}
    records = [root_record(base, a, table, root) for a, root in enumerate(roots)]
    require(all(item["separator_generation"] == 8060 and item["separator_s_head_sha256"] == NEW_HEAD and
                item["separator_s_head_sha256"] != OLD_HEAD for item in records), "fresh_head_canary")
    scalars = np.zeros((4, 44), dtype=np.uint8)
    scalars[1, 2] = 2
    raw, stream = scalar_stream(scalars, records)
    require(len(stream) == raw.count(b"\n") == 176 and
            next(item["index"] for item in stream if item["scalar"]) == 46 and
            all(item["origin_kind"] == "seed" and 0 <= item["seed"] < 44 for item in stream), "seed_only_canary")
    zero_raw, zero_stream = scalar_stream(np.zeros((4, 44), dtype=np.uint8), records)
    require(zero_raw.count(b"\n") == 176 and not any(item["scalar"] for item in zero_stream), "root_seeds_zero_canary")
    sealed_value = sealed("synthetic", {"head": NEW_HEAD})
    try:
        check_seal({**sealed_value, "head": OLD_HEAD})
    except RuntimeError:
        pass
    else:
        raise RuntimeError("stale_head_mutation_not_rejected")
    return {"status": "PASS", "synthetic_only": True,
            "tests": ["dynamic-roots", "fresh-head", "176-seed-only-order", "root-seeds-zero", "stale-head-mutation"],
            "verified": False, "cross_checked": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    for name in ("delta-root", "state-root", "prepare-root", "p1-root", "task712-root", "output-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    paths = [getattr(args, name) for name in ("delta_root", "state_root", "prepare_root", "p1_root", "task712_root", "output_root")]
    try:
        if args.selftest:
            require(not args.block_root and not any(path is not None for path in paths), "synthetic_without_parents")
            summary = selftest()
        else:
            require(len(args.block_root) == 4 and all(path is not None for path in paths), "fixed_parent_paths_required")
            summary = run_actual(args)
        print(canonical(summary).decode("ascii"), end="", flush=True)
        return 0
    except Exception as exc:
        progress("terminal", status="REJECTED", reason=str(exc), error_type=type(exc).__name__)
        print(canonical({"status": "REJECTED", "reason": str(exc), "verified": False,
                         "cross_checked": False}).decode("ascii"), end="", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
