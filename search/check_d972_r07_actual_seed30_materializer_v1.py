#!/usr/bin/env python3
"""Independent, fixed-parent seed30 / one-pivot delta checker (Task928).

The accepted checker-v15 affine-Fox seed lineage is reused explicitly.  New
SeedRed subtraction, B application, pivot elimination and target update are
implemented here, without importing or executing the new producer.  The old
rank1354 derivation is an authenticated external premise, never rebuilt.
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

SCHEMA = "d972.r07.actual-seed30-materializer.v1"
WIDTH = 48384
ROW_BYTES = 12096
LOWER_WIDTH = 96776
OLD_OFFSETS = (0, 505, 1008, 1511)
NEW_OFFSETS = (2014, 3523, 5035, 6547)
ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
FORMULA = "r07.v541.formulas-2.1-2.2-4.1.raw-seed-plus-actor-lower-adjoint"
OLD_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"
OLD_REMAINDER_SHA = "e0053fc6e745e4459e0324d26320bf9f5e434a2942fa4a519ebaf9e28df50011"
LAUNCH_SHA = "16adebd65d741efd473017f7a75e4ba394ae2d0cc57733d721baba6ddcf9828a"
VIOLATION_SHA = "cba44225c60f14e6203ea51a053f75a56b17e6cc33f146a9262609ac43c1c0f5"
SOURCE_PINS = {
    "check_d972_r07_actual_grade2_root_scalar_batch_v2.py": "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6",
    "check_d972_r07_targeted_grade2_owner_generated_join_v15.py": "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662",
    "check_d972_r07_grade2_physical_state_separator_v2.py": "bb5d0c0a51408a65c3200b552e6a1eac2f832abeeca8e19fcce64d570f0967f6",
}
# Authenticate every executable dependency before importing it.  In particular
# the new producer is neither imported nor executed by this checker.
for _name, _wanted in SOURCE_PINS.items():
    _source = Path(__file__).resolve().parent / _name
    if _source.is_symlink() or hashlib.sha256(_source.read_bytes()).hexdigest() != _wanted:
        raise ValueError("seed30_checker:source_pin:" + _name)
import check_d972_r07_actual_grade2_root_scalar_batch_v2 as BASE
import check_d972_r07_grade2_physical_state_separator_v2 as TARGET

SCALAR_ARTIFACT = {
    "run": 33941591417, "attempt": 1,
    "head": "2caaf1f33b6f36f8aa754f759ef0e5dccfaf5a74",
    "source_commit": "a68460cf0c1bdae9fde5d3a4fa6501d625d68388",
    "id": 9962060495, "name": "d972-r07-actual-root-scalar-batch-v2-candidate-33941591417-1",
    "bytes": 253544,
    "sha256": "sha256:1091f9946108ef6bf122143da58d32006eba54166ee995996efa177aa89a2ed2",
}
SCALAR_DIAGNOSTIC_ARTIFACT = {
    "run": 33941591417, "attempt": 1,
    "head": SCALAR_ARTIFACT["head"], "id": 9962060193,
    "name": "d972-r07-actual-root-scalar-batch-v2-diagnostics-33941591417-1",
    "bytes": 266309,
    "sha256": "sha256:78f087944047f170162587c413fcb1202bb5796b8d4fdff19da73e6e2fd321cf",
}
CLAIMS = {
    "ACTUAL_SEED30_MATERIALIZATION_CANDIDATE": True,
    "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
    "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
    "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED",
    "IHARA": "NOT_DECLARED", "verified": False,
}
SCALAR_FILES = {
    "output/manifest.json": (4447, "e9637fc60d0fd27df677960d941b365a7fa207c69c6519b6c3be7dc18c6696d0"),
    "output/result.json": (5147, "b62b2a65c5120cd9429a83750dbbc3d4e9a593e50f3bc41963b33ab979de6eaa"),
    "output/terminal.json": (1381, "8fea18c57a6a309b93f9b348b106ed2d3f3960d06d6707b9022214b420a354c2"),
    "output/character-a0.json": (16354, "cb8d8f75710628b7806f0d6f38ff7fcdda91c5b1ca55748aa86ea39631534557"),
    "checker-result.json": (318, "e87942af848f399660b34e08839937109ac0c2612b75590370194260c166f732"),
}
STATE_FILES = {
    "state/HEAD": (299, "f789ac352864ae662beced75f9004887fe677f81eee922eb9d9200dcaf6860ef"),
    "state/manifest.json": (7780, "d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b"),
    "state/physical.bin": (16377984, "1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e"),
    "state/physical-p1-coeff.bin": (2728310, "a2d462ea6c8685a59e28f3f5d1c89656e2e942a65110a21184e33c6cb334826c"),
    "state/instructions.jsonl": (86919157, "a7cbe317ba92b0d4076623dfd5ea672d2ef4b154f5be2862e0dc232ba91309c2"),
    "output/result.json": (457791, "d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968"),
    "output/terminal.json": (457656, "098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf"),
    "output/lambda.bin": (12096, "7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed"),
    "checker-result.json": (515, "2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433"),
}


def require(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError("seed30_checker:" + why)


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
    progress("parent_loading", parent="corrected_scalar")
    root = args.scalar_root.resolve()
    objects = {name: json_bytes(fixed(root, name, identity), canonical_required=name != "checker-result.json")
               for name, identity in SCALAR_FILES.items()}
    manifest = objects["output/manifest.json"]
    result = objects["output/result.json"]
    character = objects["output/character-a0.json"]
    for name in ("output/manifest.json", "output/result.json", "output/terminal.json", "output/character-a0.json"):
        check_seal(objects[name])
    require(objects["checker-result.json"]["status"] == "PASS" and
            objects["checker-result.json"]["verified"] is False, "scalar_checker")
    require(result["launch_sha256"] == LAUNCH_SHA and character["character"] == 0 and
            character["scalar"]["sha256"] == VIOLATION_SHA, "scalar_launch_violation")
    violation = character["scalar"]
    check_seal(violation)
    require(all(violation[k] == v for k, v in {"origin_id": 30, "seed": 30, "scalar": 1,
            "origin_kind": "seed", "character": 0}.items()), "fixed_seed30")
    require(manifest["candidate"] is True and manifest["verified"] is False, "scalar_candidate")
    for receipt in manifest["files"]:
        fixed(root / "output", receipt["file"], (receipt["bytes"], receipt["sha256"]))
    launch_path = path(args.scalar_diagnostics_root, "launch.json")
    launch_raw = launch_path.read_bytes()
    require(sha(launch_raw) == LAUNCH_SHA, "diagnostic_launch")
    launch = json_bytes(launch_raw)
    source = json_bytes(fixed(args.scalar_diagnostics_root, "receipts/source-receipt.json",
                             (797, "b600ae44e66ec70eaf192525561e8b5f2927a6bcf32088c1c0dd853d0e73c54c")))
    require(source["verified"] is False and launch["fixture_only"] is False and
            launch["mode"] == "actual" and launch["schema"] == BASE.SCHEMA + ".launch.v1" and
            launch["source_pin"]["checker"]["sha256"] == BASE.ARITH_SHA256 and
            launch["source_pin"]["producer"]["sha256"] == BASE.PRODUCER_ARITH_SHA256 and
            {item["path"].split("/")[-1]: item["sha256"] for item in source["files"]} == {
                "d972_r07_actual_grade2_root_scalar_batch_v2.py":
                    "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
                "check_d972_r07_actual_grade2_root_scalar_batch_v2.py": SOURCE_PINS[
                    "check_d972_r07_actual_grade2_root_scalar_batch_v2.py"],
                "d972_r07_targeted_grade2_owner_generated_join_v15.py": BASE.PRODUCER_ARITH_SHA256,
                "check_d972_r07_targeted_grade2_owner_generated_join_v15.py": BASE.ARITH_SHA256},
            "actual_source")
    dual = character["raw_dual"]
    check_seal(dual)
    require(dual["word_node"] == {"actors": [], "character": 0, "kind": "root"} and
            dual["raw_predecessor_sha256"] is None and dual["actor_table_identities_along_w"] == [] and
            dual["separator_generation"] == 8059 and dual["separator_s_head_sha256"] == OLD_HEAD and
            dual["lambda_sha256"] == STATE_FILES["output/lambda.bin"][1] and
            violation["raw_dual_sha256"] == dual["sha256"] and
            violation["word_node_sha256"] == sha(canonical(dual["word_node"])) and
            violation["p1_manifest_sha256"] == BASE.P1_MANIFEST_SHA256 and
            violation["global_relation_stream_sha256"] == BASE.relation_source_sha256() and
            character["v541_formula_id"] == FORMULA, "raw_root_join")
    scalars = path(root / "output", "seed-scalars-a0.bin").read_bytes()
    require(len(scalars) == 44 and max(scalars) <= 2 and not any(scalars[:30]) and scalars[30] == 1,
            "scalar_saved_vector")
    return {"launch": launch, "violation": violation, "source": source,
            "q": unpack(path(root / "output", "q-a0-root.bin").read_bytes(), 36288),
            "character": character, "result": result}


def load_task554(args: argparse.Namespace, launch: dict[str, Any]) -> list[dict[str, Any]]:
    BASE.validate_task554(launch["task554_parent"])
    parents = [launch["task554_parent"]["prepare"], *launch["task554_parent"]["blocks"]]
    roots = [args.prepare_root, *args.block_root]
    require(len(roots) == 5, "five_task554_roots")
    states = []
    for index, (descriptor, root) in enumerate(zip(parents, roots)):
        progress("parent_loading", parent="task554", body=index + 1, total=5)
        state = BASE.state_descriptor({**descriptor, "root": str(root.resolve())}, index - 1)
        # Accepted hashes bind the complete bodies; retain only seed30 rows.
        # Never hold the four large parsed block bodies simultaneously.
        if index == 0:
            chosen = [item["record"]["seed_reductions"][30]
                      for item in state["body"]["old_blocks"]]
        else:
            chosen = [state["body"]["origin_reductions"][start + 30]
                      for start, _ in ORIGIN_RANGES]
        states.append({"root": state["root"], "body_sha256": state["body_sha256"],
                       "expressions": chosen})
        del state
    return states


def combined_seed30(states: list[dict[str, Any]], *, expected_support: int = 902
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
                "target_character": target, "origin_id": origin, "term_ordinal": ordinal,
                "local_index": local, "global_index": index, "coefficient": coefficient})
    for source, offset in enumerate(OLD_OFFSETS):
        append(states[0]["expressions"][source], "prepare-old", source, None,
               ORIGIN_RANGES[source][0] + 30,
               offset, (505, 503, 503, 503)[source], states[0]["body_sha256"])
    for target, offset in enumerate(NEW_OFFSETS):
        block = states[target + 1]
        for source in range(4):
            origin = ORIGIN_RANGES[source][0] + 30
            append(block["expressions"][source], "new-block", source, target,
                   origin, offset, (1509, 1512, 1512, 1512)[target], block["body_sha256"])
    rolling = "0" * 64
    for event in events:
        rolling = sha(bytes.fromhex(rolling) + canonical(event))
        event["rolling_sha256"] = rolling
    # Nonabelian ancestry has been retained/sealed before coefficient collection.
    coefficients: dict[int, int] = {}
    for event in events:
        index = event["global_index"]
        coefficients[index] = (coefficients.get(index, 0) + event["coefficient"]) % 3
    final = [[index, value] for index, value in sorted(coefficients.items()) if value]
    require(len(final) == expected_support, "actual_seed30_support902")
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
    with path(args.p1_root, "instructions.jsonl").open("rb") as stream:
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
                       final: list[list[int]], roots: list[dict[str, Any]]) -> dict[str, Any]:
    progress("raw_seed_evaluation", seed=30)
    context, words = BASE.checker_source_context()
    word = tuple(int(x) for x in words["relators"][30])
    raw = BASE.ARITH._checker_seed_evaluate_seed(context, word)
    require([part.shape for part in raw] == [(4, 6048), (4, 18144), (4, 36288), (8,)],
            "raw_seed_dimensions")
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
            if count % 64 == 0 or count == 902:
                progress("selected_p1_subtraction", selected=count, total=902)
    require_lower_zero(defect)
    projected = BASE.ARITH._checker_seed_full_project(context, defect, (0, 0))
    require(all(not np.any(part) for part in (projected[0], projected[1], projected[3])) and
            np.array_equal(projected[2][0], defect[2][0]) and not np.any(projected[2][1:]),
            "complete_filtered_projector")
    return {"word": list(word), "raw": raw, "defect": defect, "projected": projected,
            "d": defect[2][0].copy(), "descriptors": descriptors, "selected_lifts": selected_lifts}


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
        table: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
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
    raw_seed = seal({"schema": SCHEMA + ".raw-seed", "seed": 30, "character": 0,
        "compact_word": arithmetic["word"], "compact_word_sha256": sha(canonical(arithmetic["word"])),
        "word_dictionary_sha256": BASE.ARITH.WORD_SHA,
        "relator_dictionary_sha256": BASE.ARITH.WORD_RELATOR_SHA,
        # This is the producer's declared lineage, not the arithmetic used here.
        "shared_legacy_arithmetic_sha256": BASE.PRODUCER_ARITH_SHA256,
        "components": [component_receipt(name, part) for name, part in zip(names, arithmetic["raw"])]})
    subtraction = seal({"schema": SCHEMA + ".complete-subtraction", "formula_id": FORMULA,
        "seed": 30, "character": 0, "raw_event_count": len(events), "final_selected_count": len(final),
        "arithmetic_coefficient_collection": "mod3-after-ordered-raw-events",
        "literal_coefficient_collection": False, "task554_blob_pass_sha256": blob_pass["sha256"],
        "p1_cache_sha256": BASE.P1_CACHE_SHA256,
        "selected_lift_receipt_sha256": sha(canonical(arithmetic["selected_lifts"])),
        "reduced_components": [component_receipt(name, part)
                               for name, part in zip(names, arithmetic["defect"])],
        "lower_width": LOWER_WIDTH, "lower_nonzero_count": 0, "lower_zero_count": LOWER_WIDTH,
        "lower_dense_sha256": sha(b"\0" * LOWER_WIDTH),
        "plain_character0_source_sha256": sha(pack(arithmetic["d"])),
        "full_projector_character0_source_sha256": sha(pack(arithmetic["projected"][2][0])),
        "full_projector_other_character_nonzero_count": 0,
        "full_projector_applied_to_complete_defect": True})
    factors = [{"label": list(label), "pure_word": list(BASE.ARITH.SEED_PURE_WORDS[label]),
        "pure_word_sha256": sha(canonical(list(BASE.ARITH.SEED_PURE_WORDS[label]))),
        "source_character_sign": 1} for label in CHARACTERS]
    literal = seal({"schema": SCHEMA + ".literal-word-dag", "v518_formulae": ["1.3", "2.2", "4.3"],
        "coefficient_convention": {"0": "identity", "1": "word", "2": "inverse"},
        "defect": {"operation": "ordered-product",
            "seed_factor": {"seed": 30, "exponent": 1, "compact_word_sha256": raw_seed["compact_word_sha256"]},
            "p1_factor_sequence": {"source": "raw_events", "order": "event_id-ascending",
                "root_field": "p1_sha256", "root_join": "raw_events.global_index=p1_roots.node",
                "exponent_rule": "(3-coefficient)%3", "coefficient_collection": False}},
        "projector": {"operation": "ordered-character-projector", "character": [0, 0],
            "order": [list(label) for label in CHARACTERS], "factors": factors},
        "actor_path": [], "forward_B": table["identity"]["forward:B"], "six_source_tag_replay": True,
        "eleven_slot_replay": False, "full_A0_witness": False})
    ancestry = seal({"schema": SCHEMA + ".seed30-ancestry", "seed": 30, "character": 0,
        "task554_body_sha256": body_hashes, "raw_event_count": len(events), "raw_events": events,
        "raw_event_final_head": events[-1]["rolling_sha256"], "final_support": len(final),
        "final_coefficients": final, "p1_roots": roots, "selected_lifts": arithmetic["selected_lifts"],
        "literal_word_dag": literal,
        "p1_parent": {"manifest_sha256": BASE.P1_MANIFEST_SHA256, "cache_sha256": BASE.P1_CACHE_SHA256,
            "instruction_sha256": BASE.P1_INSTRUCTION_SHA256,
            "instruction_final_head": p1["manifest"]["ancestry_sha256"], "rows": 8059,
            "cache_passes": 1, "instruction_passes": 1, "selected_arithmetic_rows": len(final),
            "selected_literal_roots": len(roots)},
        "task554_blob_pass": blob_pass})
    return raw_seed, subtraction, ancestry


def b_and_pairings(args: argparse.Namespace, scalar: dict[str, Any],
                   d: np.ndarray, old_lambda: np.ndarray) -> dict[str, Any]:
    progress("parent_loading", parent="task712", character=0)
    require(all({key: item[key] for key in BASE.TASK712_PARENT} == BASE.TASK712_PARENT
                for item in scalar["launch"]["task712_parents"]), "task712_launch_join")
    parent = {**scalar["launch"]["task712_parents"][0], "root": str(args.task712_root.resolve())}
    table = BASE.ARITH.read_task712_envelope(parent, 0)
    require(table["identity"] == scalar["character"]["task712_table_identities"] and
            table["identity"]["forward:B"] ==
            "B_fwd_a0.jsonl:763affaa7be5dea7a1d432fa5cf43e65177abb1b9fb4935dc4b2e5c37cb5fd67",
            "B_forward_identity")
    require(sorted((int(j), int(i), int(c)) for i, j, c in table["forward"]["B"]) ==
            sorted(tuple(int(x) for x in row) for row in table["adjoint"]["B"]), "B_transpose")
    entries = np.asarray(table["forward"]["B"], dtype=np.int64)
    require(entries.shape == (36288, 3), "B_entries")
    physical = np.zeros(WIDTH, dtype=np.int64)
    np.add.at(physical, entries[:, 1], entries[:, 2] * d[entries[:, 0]])
    physical = (physical % 3).astype(np.uint8)
    pulled = np.zeros(36288, dtype=np.int64)
    np.add.at(pulled, entries[:, 0], entries[:, 2] * old_lambda[entries[:, 1]])
    q = (pulled % 3).astype(np.uint8)
    require(np.array_equal(q, scalar["q"]) and dot(q, d) == 1 and dot(old_lambda, physical) == 1,
            "scalar_physical_pairings")
    return {"G": physical, "q": q, "table": table}


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


def load_state(args: argparse.Namespace, scalar: dict[str, Any]) -> dict[str, Any]:
    progress("parent_loading", parent="accepted_state", rank=1354)
    root = args.state_root.resolve()
    small = {}
    for name, identity in STATE_FILES.items():
        if name.endswith("instructions.jsonl"):
            continue
        if name.endswith("physical.bin") or name.endswith("physical-p1-coeff.bin"):
            fixed_stream(root, name, identity, True)
        else:
            raw = fixed(root, name, identity)
            small[name] = raw if name.endswith(".bin") else json_bytes(raw)
    state = small["state/manifest.json"]
    head = small["state/HEAD"]
    require(state["rank"] == head["rank"] == 1354 and state["generation"] == head["generation"] == 8059 and
            state["cursor"] == head["cursor"] == 8059 and head["rolling_head"] == OLD_HEAD,
            "accepted_state_fixed_scope")
    require(head["manifest_sha256"] == STATE_FILES["state/manifest.json"][1] and head["eof"] is True and
            state["instructions"]["final_head"] == OLD_HEAD and
            state["instructions"]["sha256"] == STATE_FILES["state/instructions.jsonl"][1] and
            state["physical"]["sha256"] == STATE_FILES["state/physical.bin"][1] and
            state["p1_companions"]["sha256"] == STATE_FILES["state/physical-p1-coeff.bin"][1],
            "state_head_payload_join")
    checker = small["checker-result.json"]
    require(checker["status"] == "PASS" and checker["physical_rank"] == 1354 and
            checker["target_reductions"] == 884 and checker["nonmonotone_insertion"] is True and
            checker["verified"] is False and checker["cross_checked"] is False, "old_state_checker_premise")
    require(state["p1_identity"]["manifest_sha256"] == BASE.P1_MANIFEST_SHA256 and
            state["p1_identity"]["cache_sha256"] == BASE.P1_CACHE_SHA256 and
            state["p1_identity"]["instruction"]["sha256"] == BASE.P1_INSTRUCTION_SHA256 and
            state["source_ancestry"]["prepare_body_sha256"] == BASE.TASK554_BODY_DIGESTS[0] and
            state["source_ancestry"]["parents"] == list(BASE.TASK554_BODY_DIGESTS[1:]) and
            state["task712"]["tables"]["manifest_sha256"] == BASE.ARITH.TASK712_MANIFEST_SHA,
            "state_parent_source_joins")
    parent = scalar["launch"]["separator_parent"]
    require(parent["manifest"]["sha256"] == STATE_FILES["state/manifest.json"][1] and
            parent["physical"]["sha256"] == STATE_FILES["state/physical.bin"][1] and
            parent["lambda"]["sha256"] == STATE_FILES["output/lambda.bin"][1], "scalar_state_join")
    identity = STATE_FILES["state/instructions.jsonl"]
    instruction = path(root, "state/instructions.jsonl")
    require(instruction.stat().st_size == identity[0], "old_instruction_size")
    digest = hashlib.sha256()
    total = 0
    rolling = "0" * 64
    pivots = []
    with instruction.open("rb") as stream:
        for offer in range(8059):
            line = stream.readline()
            require(line.endswith(b"\n"), "old_instruction_eof")
            digest.update(line)
            total += len(line)
            record = json_bytes(line)
            require(record["offer"] == offer and record["rolling_sha256"] ==
                    sha(bytes.fromhex(rolling) + canonical({k: v for k, v in record.items() if k != "rolling_sha256"})),
                    "old_instruction_rolling")
            rolling = record["rolling_sha256"]
            if record["kind"] == "physical_pivot":
                require(record["physical_offset"] == len(pivots) * ROW_BYTES and
                        record["coefficient_offset"] == len(pivots) * 2015 and
                        record["rank"] == len(pivots) + 1 and
                        type(record["lead"]) is int and 0 <= record["lead"] < WIDTH,
                        "old_pivot_position")
                pivots.append({"offer": offer, "lead": record["lead"],
                    "physical_offset": record["physical_offset"],
                    "coefficient_offset": record["coefficient_offset"],
                    "rolling_sha256": rolling})
            if (offer + 1) % 1024 == 0:
                progress("parent_loading", parent="state_instruction", rows=offer + 1, total=8059)
        require(stream.read(1) == b"", "old_instruction_trailing")
    require(total == identity[0] and digest.hexdigest() == identity[1] and rolling == OLD_HEAD and
            len(pivots) == 1354 and len({p["lead"] for p in pivots}) == 1354,
            "old_instruction_identity")
    reduction = small["output/result.json"]["target_reduction"]
    require(reduction == small["output/terminal.json"]["target_reduction"] and
            reduction["state_head"] == OLD_HEAD and reduction["state_rank"] == 1354 and
            len(reduction["reductions"]) == 884 and reduction["remainder_sha256"] == OLD_REMAINDER_SHA and
            reduction["rho2_sha256"] == TARGET.RHO2_PAYLOAD_RECEIPTS["rho2.bin"]["sha256"] and
            reduction["target_parent_manifest_sha256"] == TARGET.RHO2_MANIFEST["sha256"],
            "saved_target_receipt")
    require(type(reduction["remainder"]) is str and len(reduction["remainder"]) == 24192,
            "saved_target_hex_size")
    remainder_raw = bytes.fromhex(reduction["remainder"])
    require(sha(remainder_raw) == OLD_REMAINDER_SHA, "saved_target_hex_hash")
    remainder = unpack(remainder_raw, WIDTH)
    require(all(remainder[p["lead"]] == 0 for p in pivots), "saved_target_earlier_zero")
    return {"state": state, "head": head, "pivots": pivots, "old_target": reduction,
            "old_remainder": remainder, "lambda": unpack(small["output/lambda.bin"], WIDTH),
            "root": root}


def next_separator(target: np.ndarray, remainder: np.ndarray, pivots: list[dict[str, Any]],
                   normalized: np.ndarray, lead: int, row_reader: Callable[[int], bytes]) -> dict[str, Any]:
    free = np.flatnonzero(remainder)
    require(len(free) > 0, "separator_nonzero")
    free_coordinate = int(free[0])
    free_value = int(remainder[free_coordinate])
    require(free_coordinate not in {p["lead"] for p in pivots} | {lead}, "separator_free")
    width = len(remainder)
    functional = np.zeros(width, dtype=np.uint8)
    functional[free_coordinate] = free_value
    transcript = []
    all_pivots = pivots + [{"lead": lead, "offer": 8059}]
    for pivot_id in range(len(pivots), -1, -1):
        record = all_pivots[pivot_id]
        packed = pack(normalized) if pivot_id == len(pivots) else row_reader(pivot_id)
        row = normalized if pivot_id == len(pivots) else unpack(packed, width)
        require(row[record["lead"]] == 1 and functional[record["lead"]] == 0,
                "separator_pivot_coordinate")
        value = (-dot(row, functional)) % 3
        functional[record["lead"]] = value
        require(dot(row, functional) == 0, "separator_reverse_equation")
        transcript.append({"reverse_index": pivot_id, "pivot_id": pivot_id, "offer": record["offer"],
            "lead": record["lead"], "row_sha256": sha(packed), "lambda_value": value, "equation": 0})
        if len(transcript) % 256 == 0:
            progress("next_separator", rows=len(transcript), total=len(all_pivots))
    # Accepted insertion-triangular old rows plus checked new earlier zeros
    # preserve later equations during reverse substitution.  No old Conn replay.
    require(dot(functional, target) == 1 and dot(functional, normalized) == 0,
            "separator_target_pairing")
    return {"lambda": functional, "transcript": transcript,
            "free_coordinate": free_coordinate, "free_value": free_value}


def file_receipt(name: str, payload: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(payload), "sha256": sha(payload)}


def expected_parents(scalar: dict[str, Any], state: dict[str, Any], table: dict[str, Any],
                     target_manifest: dict[str, Any]) -> dict[str, Any]:
    launch = scalar["launch"]
    state_artifact = {"run": BASE.SEPARATOR_RUN, "attempt": BASE.SEPARATOR_ATTEMPT,
        "head": BASE.SEPARATOR_HEAD, "id": BASE.SEPARATOR_ARTIFACT,
        "name": BASE.SEPARATOR_ARTIFACT_NAME, "bytes": BASE.SEPARATOR_ARCHIVE_BYTES,
        "sha256": BASE.SEPARATOR_ARCHIVE_SHA256}
    same(launch["separator_parent"]["artifact"], state_artifact, "state_artifact_join")
    rho2_artifact = {"run": TARGET.RHO2_ACQUISITION["run_id"], "attempt": 1,
        "head": TARGET.RHO2_ACQUISITION["head_sha"], "id": TARGET.RHO2_ACQUISITION["artifact_id"],
        "name": TARGET.RHO2_ACQUISITION["artifact_name"],
        "bytes": TARGET.RHO2_ACQUISITION["artifact_archive_bytes"],
        "sha256": TARGET.RHO2_ACQUISITION["artifact_digest"]}
    return {
        "scalar": {"final_artifact": SCALAR_ARTIFACT, "diagnostic_artifact": SCALAR_DIAGNOSTIC_ARTIFACT,
            "launch": {"file": "launch.json", "bytes": 10342, "sha256": LAUNCH_SHA},
            "source": {"file": "source-receipt.json", "bytes": 797,
                       "sha256": "b600ae44e66ec70eaf192525561e8b5f2927a6bcf32088c1c0dd853d0e73c54c"},
            **{key + "_sha256": SCALAR_FILES[name][1] for key, name in (
                ("manifest", "output/manifest.json"), ("result", "output/result.json"),
                ("terminal", "output/terminal.json"), ("character", "output/character-a0.json"),
                ("checker", "checker-result.json"))},
            "violation_sha256": VIOLATION_SHA},
        "task554": {**{key: launch["task554_parent"][key]
                        for key in ("source_run", "source_attempt", "source_head", "artifacts")},
                    "body_sha256": list(BASE.TASK554_BODY_DIGESTS)},
        "p1": {key: value for key, value in launch["p1_parent"].items() if key != "root"},
        "task712": {"artifact": BASE.TASK712_PARENT, "manifest_sha256": table["manifest_sha256"],
                    "B_fwd_identity": table["identity"]["forward:B"]},
        "state": {"artifact": state_artifact, "manifest_sha256": STATE_FILES["state/manifest.json"][1],
            "head": OLD_HEAD, "generation": 8059, "rank": 1354,
            "physical_sha256": STATE_FILES["state/physical.bin"][1],
            "companion_sha256": STATE_FILES["state/physical-p1-coeff.bin"][1],
            "instruction_sha256": STATE_FILES["state/instructions.jsonl"][1],
            "checker_sha256": STATE_FILES["checker-result.json"][1],
            "result_sha256": STATE_FILES["output/result.json"][1],
            "target_sha256": sha(canonical(state["old_target"])), "old_derivation_accepted_as_premise": True},
        "rho2": {"artifact": rho2_artifact, "manifest_sha256": sha(canonical(target_manifest)),
                 "packed_sha256": TARGET.RHO2_PAYLOAD_RECEIPTS["rho2.bin"]["sha256"]},
        # These are declared producer-source receipts only.  This checker never
        # loads them; its executable checker-only dependencies are pinned above.
        "source_modules": {
            "d972_r07_actual_grade2_root_scalar_batch_v2.py":
                "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
            "d972_r07_targeted_grade2_owner_generated_join_v15.py": BASE.PRODUCER_ARITH_SHA256,
            "d972_r07_grade2_physical_state_separator_v2.py":
                "b068c9f3be153c5381f583b4a82448d5680777ce71ccb5250c2bbb972c8cff2e"},
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
        "parent_state_manifest_sha256": STATE_FILES["state/manifest.json"][1],
        "parent_state_head": OLD_HEAD, "state_head": instruction["rolling_sha256"],
        "rank_before": 1354, "rank_after": 1355, "result_sha256": sha(canonical(result)),
        "terminal": result["kind"], "parent_state_copied": False})
    manifest = json_bytes(fixed(candidate_root, "manifest.json",
                               (len(canonical(expected_manifest)), sha(canonical(expected_manifest)))))
    same(manifest, expected_manifest, "candidate_manifest")
    return {"manifest_sha256": sha(canonical(manifest)), "result_sha256": sha(canonical(result)),
            "instruction_sha256": sha(canonical(instruction))}


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    progress("parent_loading", parent="checker_source_lineage")
    scalar = load_scalar(args)
    state = load_state(args, scalar)
    states = load_task554(args, scalar["launch"])
    events, final = combined_seed30(states)
    p1, roots = p1_roots(args, scalar["launch"], events)
    arithmetic = reconstruct_defect(args, states, final, roots)
    maps = b_and_pairings(args, scalar, arithmetic["d"], state["lambda"])
    table = maps["table"]
    raw_seed, subtraction, ancestry = expected_source_receipts(events, final, p1, roots, arithmetic, table)
    progress("parent_loading", parent="task640_saved_target")
    target_packed, target_manifest = TARGET._target(args.rho2_root.resolve(), live_parent=True)
    require(sha(canonical(target_manifest)) == state["old_target"]["target_parent_manifest_sha256"],
            "old_target_manifest_join")
    target = unpack(target_packed.tobytes(), WIDTH)
    parents = expected_parents(scalar, state, table, target_manifest)
    source_raw, physical_raw = pack(arithmetic["d"]), pack(maps["G"])
    raw_materialization = seal({"schema": SCHEMA + ".raw-materialization",
        "violation_sha256": VIOLATION_SHA, "raw_dual_sha256": scalar["violation"]["raw_dual_sha256"],
        "lambda_sha256": STATE_FILES["output/lambda.bin"][1], "raw_q_sha256": sha(pack(maps["q"])),
        "raw_seed_sha256": raw_seed["sha256"], "source_ancestry_sha256": ancestry["sha256"],
        "lower_zero_receipt_sha256": subtraction["sha256"],
        "raw_word_sha256": ancestry["literal_word_dag"]["sha256"],
        "raw_source_sha256": sha(source_raw), "raw_physical_sha256": sha(physical_raw),
        "forward_B": table["identity"]["forward:B"], "actor_path": [], "q_d": 1, "lambda_G": 1})
    progress("physical_reduction", pivots=0, total=1354)
    with path(state["root"], "state/physical.bin").open("rb") as stream:
        def read_pivot(index: int) -> bytes:
            return blob_row(stream, index, WIDTH)
        remainder, reductions = reduce_dense(maps["G"], state["pivots"], read_pivot, verbose=True)
        normalized, lead, scale = normalize(remainder)
        require(lead not in {record["lead"] for record in state["pivots"]} and
                dot(state["lambda"], remainder) == 1 and dot(state["lambda"], normalized) == scale,
                "rank_gate_and_raw_normalized_pairing")
        remainder_raw, normalized_raw = pack(remainder), pack(normalized)
        normalized_word = seal({"schema": SCHEMA + ".normalized-word-dag", "v518_formula": "4.3",
            "raw_word_sha256": ancestry["literal_word_dag"]["sha256"],
            "operation": "ordered-product-then-scale", "parent_state_head": OLD_HEAD,
            "parent_state_manifest_sha256": STATE_FILES["state/manifest.json"][1],
            "reductions": [{"pivot_id": item["pivot_id"], "offer": item["offer"],
                "instruction_rolling_sha256": state["pivots"][item["pivot_id"]]["rolling_sha256"],
                "row_sha256": item["row_sha256"], "coefficient": item["scalar"],
                "literal_exponent": (-item["scalar"]) % 3} for item in reductions],
            "scale": scale, "coefficient_two_means": "inverse", "coefficient_collection": False})
        instruction_body = {"schema": SCHEMA + ".state-instruction", "kind": "physical_pivot",
            "offer": 8059, "generation": 8060, "predecessor": OLD_HEAD, "parent_state": parents["state"],
            "raw_materialization_sha256": raw_materialization["sha256"],
            "source_ancestry_sha256": ancestry["sha256"], "normalized_word_sha256": normalized_word["sha256"],
            "top": file_receipt("physical-raw.bin", physical_raw),
            "remainder": file_receipt("physical-remainder.bin", remainder_raw),
            "physical": file_receipt("physical-normalized.bin", normalized_raw),
            "reductions": reductions, "lead": lead, "sigma": scale, "lower_zero": True,
            "physical_zero": False, "rank": 1355, "physical_offset": 1354 * ROW_BYTES,
            "delta_physical_offset": 0, "coefficient_offset": None,
            "coefficient_representation": "parent-literal-DAG"}
        new_head = sha(bytes.fromhex(OLD_HEAD) + canonical(instruction_body))
        instruction = {**instruction_body, "rolling_sha256": new_head}
        pivot = seal({"schema": SCHEMA + ".physical-pivot",
            "raw_materialization_sha256": raw_materialization["sha256"], "offer": 8059, "pivot_id": 1354,
            "lead": lead, "scale": scale, "rank_before": 1354, "rank_after": 1355,
            "generation_before": 8059, "generation_after": 8060, "head_before": OLD_HEAD,
            "head_after": new_head, "instruction_sha256": sha(canonical(instruction)),
            "reductions": reductions, "raw_sha256": sha(physical_raw),
            "remainder_sha256": sha(remainder_raw), "normalized_sha256": sha(normalized_raw),
            "earlier_pivot_zero_count": 1354, "lambda_raw": 1, "lambda_remainder": 1,
            "lambda_normalized": scale, "literal_word_dag": normalized_word})
        progress("target_append", new_pivots=1, old_target_reductions=884, rank=1355)
        updated, target_scalar = next_target(state["old_remainder"], normalized, lead,
                                              [record["lead"] for record in state["pivots"]])
        updated_raw = pack(updated)
        kind = "Separator" if np.any(updated) else "ConnectionMemberCandidate"
        target_update = seal({"schema": SCHEMA + ".target-update",
            "parent_target_sha256": sha(canonical(state["old_target"])),
            "parent_result_sha256": STATE_FILES["output/result.json"][1],
            "old_remainder_sha256": OLD_REMAINDER_SHA, "old_reduction_count": 884,
            "rho2_sha256": TARGET.RHO2_PAYLOAD_RECEIPTS["rho2.bin"]["sha256"],
            "state_head": new_head, "state_rank": 1355, "scalar": target_scalar,
            "new_pivots_examined": 1, "new_reductions": [{"pivot_id": 1354, "offer": 8059,
                "lead": lead, "scalar": target_scalar, "physical_offset": 1354 * ROW_BYTES,
                "row_sha256": sha(normalized_raw)}] if target_scalar else [],
            "remainder_sha256": sha(updated_raw), "kind": kind, "old_target_history_copied": False})
        separator = None
        rows = {"source-d.bin": source_raw, "physical-raw.bin": physical_raw,
                "physical-remainder.bin": remainder_raw, "physical-normalized.bin": normalized_raw,
                "target-remainder.bin": updated_raw}
        if kind == "Separator":
            reverse = next_separator(target, updated, state["pivots"], normalized, lead, read_pivot)
            require(dot(reverse["lambda"], updated) == 1, "separator_updated_target")
            rows["lambda.bin"] = pack(reverse["lambda"])
            separator = {key: reverse[key] for key in ("free_coordinate", "free_value", "transcript")}
            separator.update({"lambda_sha256": sha(rows["lambda.bin"]),
                              "lambda_rho2": 1, "lambda_physical_pivots": 0})
    result = seal({"schema": SCHEMA + ".result", "status": "PASS", "kind": kind, "candidate": True,
        "verified": False, "cross_checked": False, "claims": CLAIMS, "parents": parents,
        "raw_seed": raw_seed, "subtraction": subtraction, "ancestry": ancestry,
        "raw_materialization": raw_materialization, "pairings": {"q_d": 1, "lambda_G": 1, "B_adjoint_q_equal": True},
        "pivot": pivot, "target": target_update, "separator": separator,
        "literal_replay": {"formal_graded_word_dag": True, "parent_state_ancestry_premise": True,
            "normalized_exponent_pair": "NOT_REPLAYED", "eleven_slot_replay": False,
            "full_A0_witness": False, "grade2_positive_terminal_complete": False}})
    progress("candidate_comparison", kind=kind)
    comparison = compare_candidate(args.candidate_root, result, instruction, rows)
    progress("terminal", status="PASS", kind=kind, rank=1355)
    return {"schema": SCHEMA + ".checker-result", "status": "PASS", "kind": kind,
        "rank_before": 1354, "rank_after": 1355, "selected_rows": 902,
        "raw_events": len(events), "literal_p1_roots": len(roots), "lower_zero_count": LOWER_WIDTH,
        "physical_reductions": len(reductions), "old_target_reductions": 884,
        "new_target_eliminations": int(target_scalar != 0), "new_pivots": 1,
        "state_head": new_head, **comparison, "old_state_derivation_premise": True,
        "checker_lineage": SOURCE_PINS, "claims": CLAIMS, "verified": False, "cross_checked": False}


def reject_test(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError("seed30_checker:selftest_did_not_reject:" + label)


def selftest() -> dict[str, Any]:
    """Finite synthetic canaries only: no parents, historical scans or actors."""
    progress("bounded_synthetic_tests")
    for width in range(1, 14):
        vector = (np.arange(width, dtype=np.uint8) * 2 + 1) % 3
        require(np.array_equal(unpack(pack(vector), width), vector), "selftest_packing")
    reject_test(lambda: unpack(b"\x51", 4), "invalid_packed_byte")
    reject_test(lambda: unpack(b"\x03", 1), "nonzero_padding")
    reject_test(lambda: json_bytes(b'{"x":1,"x":2}\n'), "duplicate_json_key")
    reject_test(lambda: same({"claim": True}, {"claim": 1}, "bool_int"), "boolean_integer")

    states = [{"expressions": [[], [], [], []], "body_sha256": str(i) * 64} for i in range(5)]
    states[0]["expressions"][0] = [[1, 1], [0, 2]]
    states[1]["expressions"][0] = [[2, 1], [1, 2]]
    states[1]["expressions"][1] = [[2, 2], [1, 2]]
    events, final = combined_seed30(states, expected_support=3)
    same(final, [[0, 2], [1, 1], [2015, 1]], "selftest_multiplicity")
    require([event["global_index"] for event in events] == [1, 0, 2016, 2015, 2016, 2015] and
            len({event["global_index"] for event in events}) == 4,
            "selftest_cancelled_literal_root_retained")
    reordered = seal({"events": list(reversed(events)), "final": final})
    reject_test(lambda: same(reordered, seal({"events": events, "final": final}), "raw_event_order"),
                "resealed_raw_ancestry_order")
    mutated = canonical({"parent": "other"})
    trusted = canonical({"parent": "fixed"})
    reject_test(lambda: fixed_bytes(mutated, (len(trusted), sha(trusted)), "parent"), "fixed_parent_mutation")

    lower = (np.zeros((4, 6048), dtype=np.uint8), np.zeros((4, 18144), dtype=np.uint8),
             np.zeros((4, 36288), dtype=np.uint8), np.zeros(8, dtype=np.uint8))
    require_lower_zero(lower)
    for part, coordinate in ((0, (3, 6047)), (1, (3, 18143)), (3, (7,))):
        lower[part][coordinate] = 1
        reject_test(lambda: require_lower_zero(lower), "complete_lower_tail")
        lower[part][coordinate] = 0

    rows = [np.array([0, 1, 1, 1, 0, 0], dtype=np.uint8),
            np.array([1, 0, 2, 1, 1, 0], dtype=np.uint8)]
    metadata = [{"lead": lead, "offer": 20 + i, "physical_offset": 2 * i}
                for i, lead in enumerate((1, 0))]
    reader = lambda i: pack(rows[i])
    vector = np.array([1, 2, 0, 0, 1, 2], dtype=np.uint8)
    remainder, reductions = reduce_dense(vector, metadata, reader)
    require(np.array_equal(remainder, np.array([0, 0, 2, 0, 0, 2], dtype=np.uint8)) and
            [item["pivot_id"] for item in reductions] == [0, 1] and
            [item["lead"] for item in reductions] == [1, 0] and
            [item["scalar"] for item in reductions] == [2, 1], "selftest_insertion_order")
    reject_test(lambda: reduce_dense(vector, [metadata[0], metadata[0]], reader), "duplicate_leads")
    normalized, lead, scale = normalize(remainder)
    require(lead == 2 and scale == 2 and not np.array_equal(remainder, normalized), "selftest_scale_two")
    reject_test(lambda: same(sha(pack(remainder)), sha(pack(normalized)), "raw_normalized"),
                "raw_normalized_swap")
    reject_test(lambda: normalize(np.zeros(6, dtype=np.uint8)), "dependent_pivot")
    old_target = np.array([0, 0, 1, 0, 2, 1], dtype=np.uint8)
    updated, scalar = next_target(old_target, normalized, lead, [1, 0])
    require(scalar == 1 and np.array_equal(updated, [0, 0, 0, 0, 2, 0]), "selftest_single_target_step")
    separator = next_separator(old_target, updated, metadata, normalized, lead, reader)
    require(separator["free_coordinate"] == 4 and separator["free_value"] == 2 and
            dot(separator["lambda"], old_target) == 1 and
            all(dot(separator["lambda"], row) == 0 for row in [*rows, normalized]),
            "selftest_reverse_separator")
    zero, coefficient = next_target(normalized, normalized, lead, [1, 0])
    require(coefficient == 1 and not np.any(zero), "selftest_member_candidate")
    unchanged, coefficient = next_target(updated, normalized, lead, [1, 0])
    require(coefficient == 0 and np.array_equal(unchanged, updated), "selftest_zero_target_coefficient")
    return {"schema": SCHEMA + ".checker-selftest", "status": "PASS", "fixture_only": True,
        "checks": ["packed_roundtrip13", "invalid_byte_padding", "canonical_json_and_boolean_type",
            "raw_order_and_mod3_multiplicity", "cancelled_literal_root_retained", "resealed_order_rejected",
            "fixed_parent_mutation_rejected", "complete96776_lower_tails", "nonmonotone_insertion_order",
            "duplicate_leads_rejected", "scale2_raw_normalized_distinction", "dependent_pivot_rejected",
            "one_target_elimination", "next_separator_reverse_substitution", "member_candidate",
            "zero_target_coefficient"], "verified": False, "cross_checked": False}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--selftest", action="store_true")
    for option in ("scalar-root", "scalar-diagnostics-root", "prepare-root", "p1-root",
                   "task712-root", "state-root", "rho2-root", "candidate-root", "output-root"):
        result.add_argument("--" + option, type=Path)
    result.add_argument("--block-root", action="append", type=Path, default=[])
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    inputs = ("scalar_root", "scalar_diagnostics_root", "prepare_root", "p1_root",
              "task712_root", "state_root", "rho2_root", "candidate_root")
    try:
        if args.selftest:
            require(not args.block_root and args.output_root is None and
                    all(getattr(args, name) is None for name in inputs), "selftest_not_actual")
            report = selftest()
        else:
            require(len(args.block_root) == 4 and all(getattr(args, name) is not None for name in inputs),
                    "actual_fixed_parent_paths_required")
            if args.output_root is not None:
                report_root = args.output_root.absolute()
                require(not report_root.exists() and not report_root.is_symlink(), "fresh_report_root")
                for parent in [*(getattr(args, name) for name in inputs), *args.block_root]:
                    require(report_root.resolve() != parent.resolve() and
                            parent.resolve() not in report_root.resolve().parents and
                            report_root.resolve() not in parent.resolve().parents, "report_parent_disjoint")
            report = check_actual(args)
            if args.output_root is not None:
                args.output_root.mkdir(parents=True, exist_ok=False)
                (args.output_root / "checker-result.json").write_bytes(canonical(report))
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
