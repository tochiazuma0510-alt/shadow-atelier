#!/usr/bin/env python3
"""Materialize one selected root seed over the accepted rank1355 state.

The immutable Task904 state plus the accepted seed30 delta are premises.
The current root-seed authority selects one seed and character.  Replay only
its complete P1 subtraction, append one normalized pivot, and apply only
that pivot to the saved current target remainder.  No historical connection,
target reduction, actor orbit, retired scalar or rho2 parent is replayed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "search"
SCHEMA = "d972.r07.actual-root-seed-materializer.v3"
SCALAR_SCHEMA = "d972.r07.rank1355.root-seed-scalars.v1"
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
SOURCE0C = 6048
SOURCE1C = 18144
SOURCE2C = 36288
LOWER_WIDTH = 96776
P1_ROWS = 8059
P1_ROW_TRITS = 145152
P1_ROW_BYTES = 36288
PHYSICAL_WIDTH = 48384
PHYSICAL_BYTES = 12096
OLD_RANKS = (505, 503, 503, 503)
NEW_RANKS = (1509, 1512, 1512, 1512)
OLD_OFFSETS = (0, 505, 1008, 1511)
NEW_OFFSETS = (2014, 3523, 5035, 6547)
ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
ZERO_HEAD = "0" * 64
V541_FORMULA_ID = "r07.v541.formulas-2.1-2.2-4.1.raw-seed-plus-actor-lower-adjoint"

ROOT_V2_PATH = SEARCH / "d972_r07_actual_grade2_root_scalar_batch_v2.py"
ROOT_V2_SHA256 = "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856"
LEGACY_ARITH_PATH = SEARCH / "d972_r07_targeted_grade2_owner_generated_join_v15.py"
LEGACY_ARITH_SHA256 = "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"
SCALAR_FINAL_ARTIFACT = {
    "run": 33954712636, "attempt": 1,
    "head": "92c98486ab659f7e3358fc3c4afb53ab6b78293d",
    "id": 9966008518,
    "name": "d972-r07-rank1355-root-seed-scalars-v1-candidate-33954712636-1",
    "bytes": 31781,
    "sha256": "sha256:148b028ec8b17543a85a563a8d0275fc93361168adda85d8147cd1dbc41207b3",
}
SCALAR_FILE_PINS = {
    "output/manifest.json": (3204, "f60e9aa4d99d7c1a89512550314c3995d389b96b87e7a788b9d4e390572aed88"),
    "output/result.json": (36195, "02a814c5a7a2129302deca997fa3a5fb54982237c75b28e47da6205145cf07ea"),
    "output/launch.json": (10347, "75bd0fc5c54b773c65532276e0eb087bcbea76c9f9b55c7c90496089c0a5d1a9"),
    "checker-result.json": (2370, "46d7f1800977493ffb0e350dc5d0f52cc2464a4fde57c6b89718b93f29be0b48"),
    "source-receipt.json": (1128, "103a9e5d9ca67c9c6af2a10905dadf25ac0c94f02d58891fdf8196e0ac85b99e"),
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
CURRENT_RANK = 1355
CURRENT_GENERATION = 8060
CURRENT_HEAD = "36feb776736c6587ce9f64d6f5acb883385074a7cc2eed4c2ce7eb8675e71342"
CURRENT_LAMBDA_SHA256 = "f83bbaa503b8a4d5056f0779085ee4eced542eb1d78d3e35fa9df1c281960565"
CURRENT_TARGET_REMAINDER_SHA256 = "f5040e3f29b42e71b86be047d40de5d538ddb7fc107cace219879bbc67238d3a"

STATE_ARTIFACT = {
    "run": 33891714539, "attempt": 1,
    "head": "7b7b9de20faaa3b8f26e331bb738b374f6f5708c",
    "id": 9944214057,
    "name": "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1",
    "bytes": 107195261,
    "sha256": "sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017",
}
STATE_MANIFEST_SHA256 = "d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b"
STATE_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"
STATE_GENERATION = 8059
STATE_RANK = 1354
STATE_PHYSICAL_SHA256 = "1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e"
STATE_COMPANION_SHA256 = "a2d462ea6c8685a59e28f3f5d1c89656e2e942a65110a21184e33c6cb334826c"
STATE_INSTRUCTION_SHA256 = "a7cbe317ba92b0d4076623dfd5ea672d2ef4b154f5be2862e0dc232ba91309c2"
STATE_RESULT_PIN = (457791, "d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968")
STATE_TERMINAL_PIN = (457656, "098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf")
STATE_CHECKER_PIN = (515, "2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433")
RHO2_SHA256 = "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"

P1_INSTRUCTION_KEYS = {
    "node", "origin", "reductions", "scale", "raw_origin_sha256",
    "raw_origin_components_sha256", "literal_input_sha256",
    "old_defect_literal_input_sha256", "parent_row_sha256", "packet_sha256",
    "packet_row_sha256", "reduction_parent_sha256", "p1_sha256", "offset",
    "length", "row_receipt", "predecessor", "ancestry_sha256",
}

CLAIMS = {
    "ACTUAL_ROOT_SEED_MATERIALIZATION_CANDIDATE": True,
    "GRADE2_MEMBER": "NOT_DECIDED",
    "GRADE2_NONMEMBER": "NOT_DECIDED",
    "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
    "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED",
    "IHARA": "NOT_DECLARED", "verified": False,
}


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def digest(value: Any, reason: str) -> None:
    require(isinstance(value, str) and len(value) == 64 and
            all(character in "0123456789abcdef" for character in value), reason)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def sealed(schema: str, body: dict[str, Any]) -> dict[str, Any]:
    unsigned = {"schema": schema, **body}
    return {**unsigned, "sha256": sha(canonical(unsigned))}


def sealed_ok(value: Any) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("sha256"), str):
        return False
    unsigned = dict(value)
    claimed = unsigned.pop("sha256")
    return claimed == sha(canonical(unsigned))


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"progress": phase, **fields}, sort_keys=True),
          file=sys.stderr, flush=True)


def safe_file(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute()
            and ".." not in Path(relative).parts and ":" not in relative
            and "\\" not in relative,
            "relative_file")
    base = root.resolve()
    cursor = base
    for part in Path(relative).parts:
        cursor /= part
        require(not cursor.is_symlink(), "symlink_file:" + relative)
    path = (base / relative).resolve()
    require(base in path.parents and path.is_file() and not path.is_symlink(),
            "unsafe_file:" + relative)
    return path


def file_sha(path: Path, expected_bytes: int | None = None,
             expected_sha: str | None = None, cap: int = 1 << 30) -> tuple[int, str]:
    require(path.is_file() and not path.is_symlink(), "regular_file")
    size = path.stat().st_size
    require(0 <= size <= cap and (expected_bytes is None or size == expected_bytes),
            "file_size:" + path.name)
    hasher = hashlib.sha256()
    total = 0
    with path.open("rb", buffering=0) as stream:
        while True:
            chunk = stream.read(1 << 20)
            if not chunk:
                break
            hasher.update(chunk)
            total += len(chunk)
    actual = hasher.hexdigest()
    require(total == size and (expected_sha is None or actual == expected_sha),
            "file_digest:" + path.name)
    return size, actual


def read_exact(path: Path, expected_bytes: int, expected_sha: str,
               cap: int = 1 << 30) -> bytes:
    require(path.is_file() and not path.is_symlink() and
            0 <= expected_bytes <= cap and path.stat().st_size == expected_bytes,
            "exact_size:" + path.name)
    raw = path.read_bytes()
    require(len(raw) == expected_bytes and sha(raw) == expected_sha,
            "exact_read:" + path.name)
    return raw


def read_json_exact(path: Path, expected_bytes: int, expected_sha: str,
                    cap: int = 1 << 28, *,
                    canonical_required: bool = True) -> tuple[Any, bytes]:
    raw = read_exact(path, expected_bytes, expected_sha, cap)
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeError, ValueError) as exc:
        raise RuntimeError("json_decode:" + path.name) from exc
    require(not canonical_required or canonical(value) == raw,
            "json_canonical:" + path.name)
    return value, raw


def receipt(name: str, raw: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def atomic_write(root: Path, name: str, raw: bytes) -> dict[str, Any]:
    require(Path(name).name == name, "output_name")
    target = root / name
    temporary = root / (name + ".tmp-" + str(os.getpid()))
    require(not target.exists() and not temporary.exists(), "fresh_output_file")
    with temporary.open("wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, target)
    return receipt(name, raw)


def atomic_json(root: Path, name: str, value: Any) -> dict[str, Any]:
    return atomic_write(root, name, canonical(value))


def load_pinned_module(name: str, path: Path, expected_sha: str) -> ModuleType:
    file_sha(path, expected_sha=expected_sha, cap=1 << 28)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module_spec:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def dependencies() -> ModuleType:
    # Pin the own accepted arithmetic import edge before loading it.
    file_sha(LEGACY_ARITH_PATH, expected_sha=LEGACY_ARITH_SHA256, cap=1 << 28)
    if str(SEARCH) not in sys.path:
        sys.path.insert(0, str(SEARCH))
    root_v2 = load_pinned_module("task940_root_v2", ROOT_V2_PATH, ROOT_V2_SHA256)
    root_v2.verify_source_pin()
    return root_v2


def _digits(value: int) -> tuple[int, int, int, int]:
    require(0 <= value <= 80, "packed_byte")
    return value % 3, value // 3 % 3, value // 9 % 3, value // 27 % 3


DIGITS = np.asarray([_digits(value) for value in range(81)], dtype=np.uint8)
PACKED_AXPY = np.empty((2, 81, 81), dtype=np.uint8)
for _scalar in (1, 2):
    for _left in range(81):
        for _right in range(81):
            PACKED_AXPY[_scalar - 1, _left, _right] = sum(
                ((int(DIGITS[_left, slot]) -
                  _scalar * int(DIGITS[_right, slot])) % 3) * 3 ** slot
                for slot in range(4))


def pack(values: Sequence[int] | np.ndarray) -> bytes:
    dense = np.asarray(values, dtype=np.uint8).reshape(-1)
    require(not np.any(dense > 2), "pack_trits")
    output = np.zeros((dense.size + 3) // 4, dtype=np.uint8)
    for slot in range(4):
        output[:dense[slot::4].size] += dense[slot::4] * (3 ** slot)
    return output.tobytes()


def validate_packed(raw: bytes | np.ndarray, width: int) -> None:
    view = (raw.reshape(-1) if isinstance(raw, np.ndarray)
            else np.frombuffer(raw, dtype=np.uint8))
    require(view.size == (width + 3) // 4 and not np.any(view > 80),
            "packed_shape")
    if width % 4:
        require(all(value == 0 for value in DIGITS[int(view[-1]), width % 4:]),
                "packed_padding")


def unpack(raw: bytes | np.ndarray, width: int) -> np.ndarray:
    validate_packed(raw, width)
    packed = raw if isinstance(raw, np.ndarray) else np.frombuffer(raw, dtype=np.uint8)
    result = np.empty(width, dtype=np.uint8)
    for slot in range(4):
        result[slot::4] = DIGITS[packed, slot][:result[slot::4].size]
    return result


def packed_trit(raw: np.ndarray, coordinate: int) -> int:
    require(raw.dtype == np.uint8 and raw.size == PHYSICAL_BYTES and
            0 <= coordinate < PHYSICAL_WIDTH, "packed_trit")
    return int(DIGITS[int(raw[coordinate // 4]), coordinate % 4])


def packed_subtract(destination: np.ndarray, source: np.ndarray, scalar: int) -> None:
    require(destination.dtype == source.dtype == np.uint8 and
            destination.shape == source.shape and scalar in (1, 2), "packed_axpy")
    destination[:] = PACKED_AXPY[scalar - 1, destination, source]


def first_nonzero(raw: bytes | np.ndarray, width: int) -> tuple[int, int] | None:
    dense = unpack(raw, width)
    positions = np.flatnonzero(dense)
    if not len(positions):
        return None
    coordinate = int(positions[0])
    return coordinate, int(dense[coordinate])


def add_scaled(destination: np.ndarray, source: np.ndarray, coefficient: int) -> None:
    require(destination.shape == source.shape and coefficient in (1, 2), "dense_axpy")
    destination[:] = ((destination.astype(np.uint16) +
                       coefficient * source.astype(np.uint16)) % 3).astype(np.uint8)


def dot(left: np.ndarray, right: np.ndarray) -> int:
    a = np.asarray(left, dtype=np.uint8).reshape(-1)
    b = np.asarray(right, dtype=np.uint8).reshape(-1)
    require(a.shape == b.shape and not np.any(a > 2) and not np.any(b > 2),
            "dot_shape")
    return int(np.dot(a.astype(np.uint64), b.astype(np.uint64)) % 3)


def apply_sparse(entries: Iterable[Iterable[int]], source_width: int,
                 destination_width: int, source: np.ndarray) -> np.ndarray:
    value = np.asarray(source, dtype=np.uint8).reshape(-1)
    require(value.size == source_width and not np.any(value > 2), "sparse_source")
    output = np.zeros(destination_width, dtype=np.uint8)
    for raw_source, raw_destination, raw_coefficient in entries:
        src = int(raw_source)
        dst = int(raw_destination)
        coefficient = int(raw_coefficient)
        require(0 <= src < source_width and 0 <= dst < destination_width and
                coefficient in (1, 2), "sparse_entry")
        output[dst] = (int(output[dst]) + coefficient * int(value[src])) % 3
    return output


def component_receipt(name: str, value: np.ndarray) -> dict[str, Any]:
    dense = np.asarray(value, dtype=np.uint8)
    raw = pack(dense.reshape(-1))
    return {"name": name, "shape": list(dense.shape), "trits": dense.size,
            "support": int(np.count_nonzero(dense)), "packed_bytes": len(raw),
            "packed_sha256": sha(raw)}


def validate_scalar_parent(candidate_root: Path) -> dict[str, Any]:
    progress("parent-loading", parent="current-root-seed-authority")
    root = candidate_root.resolve()
    require(root.is_dir(), "scalar_parent_root")
    objects: dict[str, Any] = {}
    raw_objects: dict[str, bytes] = {}
    for name, pin in SCALAR_FILE_PINS.items():
        objects[name], raw_objects[name] = read_json_exact(safe_file(root, name), *pin)
    manifest = objects["output/manifest.json"]
    result = objects["output/result.json"]
    launch = objects["output/launch.json"]
    checker = objects["checker-result.json"]
    require(all(sealed_ok(value) for value in (manifest, result, launch)) and
            manifest["schema"] == SCALAR_SCHEMA + ".manifest" and
            result["schema"] == SCALAR_SCHEMA + ".result" and
            launch["schema"] == SCALAR_SCHEMA + ".launch" and
            result["status"] == checker["status"] == "PASS" and
            result["terminal"] == checker["terminal"] == manifest["terminal"] ==
            "ROOT_SEED_VIOLATION" and launch["fixture_only"] is False and
            all(value["verified"] is False and value["cross_checked"] is False
                for value in (manifest, result, launch, checker,
                              objects["source-receipt.json"])) and
            result["launch_sha256"] == SCALAR_FILE_PINS["output/launch.json"][1] and
            manifest["result_sha256"] == checker["result_sha256"] ==
            SCALAR_FILE_PINS["output/result.json"][1] and
            checker["manifest_sha256"] == SCALAR_FILE_PINS["output/manifest.json"][1],
            "scalar_authority")
    require(result["separator_generation"] == checker["separator_generation"] ==
            CURRENT_GENERATION and result["separator_rank"] == checker["separator_rank"] ==
            CURRENT_RANK and result["separator_head"] == checker["separator_head"] ==
            CURRENT_HEAD and result["lambda_sha256"] == checker["lambda_sha256"] ==
            CURRENT_LAMBDA_SHA256 and checker["scalars"] == 176 and
            checker["old_state_rows_checked"] == STATE_RANK and
            checker["new_pivot_rows_checked"] == 1 and
            checker["lambda_pivots"] == 0 and checker["lambda_saved_remainder"] == 1 and
            checker["old_derivation_premise"] is True and
            result["actor_origins_executed"] == checker["actor_origins_executed"] == 0 and
            result["orbit_rows_executed"] == checker["orbit_rows_executed"] == 0 and
            result["materialization_performed"] is checker["materialization_performed"] is False,
            "current_scalar_separator_premise")
    output = root / "output"
    require(set(manifest["file_roster"]) == {path.name for path in output.iterdir()} and
            len(manifest["file_roster"]) == 20 and len(manifest["files"]) == 19,
            "scalar_output_roster")
    payloads: dict[str, bytes] = {}
    for item in manifest["files"]:
        require(set(item) == {"file", "bytes", "sha256"}, "scalar_file_receipt")
        payloads[item["file"]] = read_exact(safe_file(output, item["file"]),
                                            item["bytes"], item["sha256"], 1 << 24)
    violation = result["first_violation"]
    require(sealed_ok(violation) and violation == checker["first_violation"] and
            violation["schema"] == SCALAR_SCHEMA + ".RootSeedViolation" and
            violation["origin_kind"] == "seed" and
            plain_int(violation["seed"]) and 0 <= violation["seed"] < 44 and
            plain_int(violation["character"]) and 0 <= violation["character"] < 4 and
            violation["origin_id"] == violation["seed"] and
            violation["scalar"] in (1, 2) and
            violation["separator_generation"] == CURRENT_GENERATION and
            violation["separator_head"] == CURRENT_HEAD and
            violation["lambda_sha256"] == CURRENT_LAMBDA_SHA256 and
            violation["delta_manifest_sha256"] == DELTA_FILES["output/manifest.json"][1] and
            violation["materialization_performed"] is False, "selected_root_violation")
    seed, character = violation["seed"], violation["character"]
    character_record = result["characters"][character]
    raw_dual = character_record["raw_dual"]
    require(sealed_ok(character_record) and sealed_ok(raw_dual) and
            character_record["character"] == character == raw_dual["character"] and
            raw_dual["sha256"] == violation["raw_dual_sha256"] and
            raw_dual["separator_generation"] == CURRENT_GENERATION and
            raw_dual["separator_s_head_sha256"] == CURRENT_HEAD and
            raw_dual["lambda_sha256"] == CURRENT_LAMBDA_SHA256 and
            raw_dual["word_node"] == {"kind": "root", "character": character, "actors": []} and
            raw_dual["actor_table_identities_along_w"] == [] and
            raw_dual["raw_predecessor_sha256"] is None, "selected_current_raw_dual")
    q_name, value_name = f"q-a{character}-root.bin", f"p1-values-a{character}.bin"
    seed_name, direct_name = f"seed-scalars-a{character}.bin", f"direct-seeds-a{character}.bin"
    q_raw, values = payloads[q_name], payloads[value_name]
    seed_values, direct = payloads[seed_name], payloads[direct_name]
    require(len(q_raw) == 9072 and sha(q_raw) ==
            raw_dual["raw_q_packed_sha256"] == violation["raw_q_packed_sha256"] and
            len(values) == P1_ROWS and sha(values) == violation["value_vector_sha256"] and
            len(seed_values) == len(direct) == 44 and
            max(values + seed_values + direct) < 3 and seed_values[seed] == violation["scalar"],
            "selected_scalar_arrays")
    relation = result["relation_receipt"]
    selected_relation = relation["seed_records"][seed]
    require(sealed_ok(relation) and sealed_ok(selected_relation) and
            relation["sha256"] == violation["relation_receipt_sha256"] and
            selected_relation["sha256"] == violation["seed_relation_sha256"] and
            selected_relation["seed"] == seed and
            relation["old_offsets"] == list(OLD_OFFSETS) and
            relation["new_offsets"] == list(NEW_OFFSETS) and
            relation["actor_origins_executed"] == 0 and
            character_record["direct_receipt"]["sha256"] == violation["direct_receipt_sha256"] and
            sealed_ok(character_record["direct_receipt"]) and
            character_record["direct_receipt"]["formula_id"] == V541_FORMULA_ID,
            "selected_relation_join")
    # Authenticate chronology, without recomputing any of the 176 scalars.
    rolling = ZERO_HEAD
    first = None
    lines = payloads["scalars.jsonl"].splitlines(keepends=True)
    require(len(lines) == 176, "scalar_stream_count")
    for index, line in enumerate(lines):
        record = json.loads(line.decode("ascii"))
        body = {key: value for key, value in record.items() if key != "rolling_sha256"}
        rolling = sha(bytes.fromhex(rolling) + canonical(body))
        a, j = divmod(index, 44)
        require(canonical(record) == line and record == {
            "index": index, "character": a, "seed": j, "origin_id": j,
            "origin_kind": "seed", "scalar": payloads[f"seed-scalars-a{a}.bin"][j],
            "raw_dual_sha256": result["characters"][a]["raw_dual"]["sha256"],
            "rolling_sha256": rolling}, "scalar_chronology")
        if first is None and record["scalar"]:
            first = record
    require(first is not None and all(violation[key] == value for key, value in first.items()) and
            rolling == result["scalar_final_head"], "first_nonzero_authority")
    progress("selected-root", character=character, seed=seed, scalar=violation["scalar"])
    return {
        "launch": launch, "launch_receipt": receipt("launch.json", raw_objects["output/launch.json"]),
        "source_receipt": receipt("source-receipt.json", raw_objects["source-receipt.json"]),
        "manifest_sha256": SCALAR_FILE_PINS["output/manifest.json"][1],
        "result_sha256": SCALAR_FILE_PINS["output/result.json"][1],
        "checker_sha256": SCALAR_FILE_PINS["checker-result.json"][1],
        "character": character, "seed": seed, "value": violation["scalar"],
        "character_record": character_record, "raw_dual": raw_dual, "violation": violation,
        "q": unpack(q_raw, SOURCE2C), "q_receipt": receipt(q_name, q_raw),
        "seed_scalars_receipt": receipt(seed_name, seed_values),
        "values": values, "direct_value": direct[seed],
        "selected_relation": selected_relation,
        "relation_receipt_sha256": relation["sha256"],
    }


def _runtime_parent(descriptor: dict[str, Any], root: Path) -> dict[str, Any]:
    value = copy.deepcopy(descriptor)
    value["root"] = str(root.resolve())
    return value


def collect_selected_seedred(root_v2: ModuleType, scalar: dict[str, Any],
                      prepare_root: Path, block_roots: list[Path]
                      ) -> dict[str, Any]:
    launch, seed = scalar["launch"], scalar["seed"]
    progress("parent-loading", parent="task554", bodies=5, seed=seed)
    require(len(block_roots) == 4, "four_task554_blocks")
    parent = copy.deepcopy(launch.get("task554_parent"))
    require(isinstance(parent, dict), "task554_launch_parent")
    parent["prepare"] = _runtime_parent(parent["prepare"], prepare_root)
    parent["blocks"] = [_runtime_parent(parent["blocks"][index], block_roots[index])
                        for index in range(4)]
    root_v2.validate_task554(parent)
    raw_events: list[dict[str, Any]] = []
    coefficients = np.zeros(P1_ROWS, dtype=np.uint8)
    segments: list[dict[str, Any]] = []

    def append_expression(expression: Any, *, body_role: str, body_sha256: str,
                          source: int, target: int | None, origin_id: int,
                          global_offset: int) -> None:
        for ordinal, item in enumerate(expression):
            local_index = int(item[0])
            coefficient = int(item[1])
            global_index = global_offset + local_index
            event = {
                "event_id": len(raw_events), "body_role": body_role,
                "task554_body_sha256": body_sha256,
                "source_character": source, "target_character": target,
                "seed": seed, "origin_id": origin_id, "term_ordinal": ordinal,
                "local_index": local_index, "global_index": global_index,
                "coefficient": coefficient,
            }
            raw_events.append(event)

    prepare = root_v2._state_descriptor(parent["prepare"], -1, need_blobs=True)
    for source, old in enumerate(prepare["body"]["old_blocks"]):
        append_expression(
            old["record"]["seed_reductions"][seed], body_role="prepare-old",
            body_sha256=prepare["body_sha256"], source=source, target=None,
            origin_id=ORIGIN_RANGES[source][0] + seed,
            global_offset=OLD_OFFSETS[source])
        segments.append({
            "kind": "old", "owner": source, "start": OLD_OFFSETS[source],
            "rows": OLD_RANKS[source], "root": prepare["root"],
            "body_sha256": prepare["body_sha256"],
            "lower_descriptor": copy.deepcopy(old["lower_basis_blob"]),
            "grade_descriptor": copy.deepcopy(old["lifted_grade_blob"]),
        })
    del old, prepare

    for target in range(4):
        block = root_v2._state_descriptor(parent["blocks"][target], target,
                                          need_blobs=True)
        body = block["body"]
        for source in range(4):
            origin_id = ORIGIN_RANGES[source][0] + seed
            append_expression(
                body["origin_reductions"][origin_id], body_role="new-block",
                body_sha256=block["body_sha256"], source=source, target=target,
                origin_id=origin_id, global_offset=NEW_OFFSETS[target])
        segments.append({
            "kind": "new", "owner": target, "start": NEW_OFFSETS[target],
            "rows": NEW_RANKS[target], "root": block["root"],
            "body_sha256": block["body_sha256"],
            "basis_descriptor": copy.deepcopy(body["basis_blob"]),
        })
        del body, block

    require([item["start"] for item in segments] ==
            [*OLD_OFFSETS, *NEW_OFFSETS] and
            sum(item["rows"] for item in segments) == P1_ROWS,
            "task554_global_segments")
    rolling = ZERO_HEAD
    sealed_events: list[dict[str, Any]] = []
    for event in raw_events:
        rolling = sha(bytes.fromhex(rolling) + canonical(event))
        sealed_events.append({**event, "rolling_sha256": rolling})
    require(len(sealed_events) == scalar["selected_relation"]["raw_event_count"] and
            rolling == scalar["selected_relation"]["raw_event_head"],
            "selected_relation_ordered_seal")
    # Seal the ordered nonabelian ancestry before collecting F3 coefficients.
    for event in sealed_events:
        node = event["global_index"]
        coefficients[node] = (int(coefficients[node]) + event["coefficient"]) % 3
    final_coefficients = [[int(node), int(coefficients[node])]
                          for node in np.flatnonzero(coefficients)]
    require(all(0 <= node < P1_ROWS and value in (1, 2)
                for node, value in final_coefficients), "selected_coefficients")
    progress("selected-support", seed=seed, raw_events=len(sealed_events),
             selected_rows=len(final_coefficients))
    return {
        "parent": parent, "raw_events": sealed_events,
        "selected_relation": scalar["selected_relation"],
        "raw_event_final_head": rolling,
        "final_coefficients": final_coefficients, "segments": segments,
        "body_sha256": list(root_v2.TASK554_BODY_DIGESTS),
        "artifacts": copy.deepcopy(parent["artifacts"]),
    }


def scan_blob_selected(segment: dict[str, Any], descriptor: dict[str, Any],
                       wanted_local: set[int], role: str) -> tuple[dict[int, bytes], dict[str, Any]]:
    width = int(descriptor["width"])
    rows = int(descriptor["rows"])
    row_bytes = (width + 3) // 4
    require(rows == segment["rows"] and descriptor["bytes"] == rows * row_bytes and
            all(0 <= index < rows for index in wanted_local), "blob_dimensions")
    path = safe_file(segment["root"], descriptor["file"])
    hasher = hashlib.sha256()
    selected: dict[int, bytes] = {}
    total = 0
    with path.open("rb", buffering=0) as stream:
        for local in range(rows):
            raw = stream.read(row_bytes)
            require(len(raw) == row_bytes and
                    not np.any(np.frombuffer(raw, dtype=np.uint8) > 80),
                    "task554_blob_row")
            hasher.update(raw)
            total += len(raw)
            if local in wanted_local:
                selected[local] = raw
        require(stream.read(1) == b"", "task554_blob_trailing")
    require(total == descriptor["bytes"] and hasher.hexdigest() == descriptor["sha256"] and
            set(selected) == wanted_local, "task554_blob_receipt")
    return selected, {
        "role": role, "task554_body_sha256": segment["body_sha256"],
        "descriptor": descriptor, "selected_rows": len(selected),
        "full_file_authenticated": True,
    }


def load_selected_lower(seedred: dict[str, Any]) -> dict[str, Any]:
    selected_nodes = {node for node, _ in seedred["final_coefficients"]}
    rows: dict[int, dict[str, Any]] = {}
    blob_receipts: list[dict[str, Any]] = []
    for segment in seedred["segments"]:
        start = segment["start"]
        wanted = {node - start for node in selected_nodes
                  if start <= node < start + segment["rows"]}
        if segment["kind"] == "old":
            lower, lower_receipt = scan_blob_selected(
                segment, segment["lower_descriptor"], wanted,
                f"old-{segment['owner']}-lower")
            grade, grade_receipt = scan_blob_selected(
                segment, segment["grade_descriptor"], wanted,
                f"old-{segment['owner']}-grade")
            blob_receipts.extend((lower_receipt, grade_receipt))
            for local in wanted:
                rows[start + local] = {
                    "kind": "old", "owner": segment["owner"],
                    "lower": lower[local], "grade": grade[local],
                }
        else:
            basis, basis_receipt = scan_blob_selected(
                segment, segment["basis_descriptor"], wanted,
                f"new-{segment['owner']}-grade")
            blob_receipts.append(basis_receipt)
            for local in wanted:
                rows[start + local] = {
                    "kind": "new", "owner": segment["owner"],
                    "basis": basis[local],
                }
    require(set(rows) == selected_nodes and len(blob_receipts) == 12,
            "selected_lower_eof")
    body = {
        "schema": SCHEMA + ".task554-blob-pass",
        "receipts": blob_receipts,
        "selected_rows": len(rows), "full_blob_files": 12,
        "total_authenticated_bytes": sum(
            item["descriptor"]["bytes"] for item in blob_receipts),
    }
    return {"rows": rows, "receipt": {**body, "sha256": sha(canonical(body))}}


def validate_p1_instruction(record: Any, node: int, line: bytes, raw_row: bytes,
                            predecessor: str, p1_sha: list[str], row_sha: list[str]
                            ) -> str:
    require(isinstance(record, dict) and set(record) == P1_INSTRUCTION_KEYS and
            record["node"] == node and record["offset"] == node * P1_ROW_BYTES and
            record["length"] == P1_ROW_BYTES and record["predecessor"] == predecessor and
            record["scale"] in (1, 2), "p1_instruction_shape")
    row_receipt = record["row_receipt"]
    require(isinstance(row_receipt, dict) and
            set(row_receipt) == {"offset", "length", "sha256"} and
            row_receipt["offset"] == node * P1_ROW_BYTES and
            row_receipt["length"] == P1_ROW_BYTES and
            row_receipt["sha256"] == sha(raw_row), "p1_row_receipt")
    reductions = record["reductions"]
    require(isinstance(reductions, list), "p1_reductions")
    base = max(offset for offset in (*OLD_OFFSETS, *NEW_OFFSETS) if offset <= node)
    local_bound = node - base
    seen: set[int] = set()
    for item in reductions:
        require(isinstance(item, list) and len(item) == 2 and
                plain_int(item[0]) and 0 <= item[0] < local_bound and
                item[0] not in seen and item[1] in (1, 2),
                "p1_reduction_entry")
        seen.add(item[0])
    reduction_roots = record["reduction_parent_sha256"]
    parent_rows = record["parent_row_sha256"]
    require(isinstance(reduction_roots, list) and isinstance(parent_rows, list) and
            len(reduction_roots) == len(reductions) and
            all(reduction_roots[index] == row_sha[base + item[0]]
                for index, item in enumerate(reductions)) and
            all(isinstance(value, str) and len(value) == 64 for value in parent_rows),
            "p1_reduction_parents")
    for key in ("p1_sha256", "raw_origin_sha256", "ancestry_sha256"):
        digest(record[key], "p1_digest:" + key)
    if record["literal_input_sha256"] is not None:
        digest(record["literal_input_sha256"], "p1_digest:literal_input_sha256")
    components = record["raw_origin_components_sha256"]
    require(isinstance(components, dict) and
            all(isinstance(value, str) and len(value) == 64
                for value in components.values()), "p1_origin_components")
    unsigned = dict(record)
    ancestry = unsigned.pop("ancestry_sha256")
    expected = sha(bytes.fromhex(predecessor) + canonical(unsigned))
    require(ancestry == expected and canonical(record) == line,
            "p1_instruction_rolling")
    return ancestry


def load_selected_p1(root_v2: ModuleType, launch: dict[str, Any], p1_root: Path,
                     reference_nodes: set[int], arithmetic_nodes: set[int]
                     ) -> dict[str, Any]:
    progress("parent-loading", parent="canonical-p1", rows=P1_ROWS)
    parent = _runtime_parent(launch["p1_parent"], p1_root)
    p1 = root_v2.validate_p1(parent)
    cache_path = safe_file(p1["root"], p1["cache"]["path"])
    instruction_path = safe_file(p1["root"], p1["instruction"]["path"])
    cache_hash = hashlib.sha256()
    instruction_hash = hashlib.sha256()
    predecessor = ZERO_HEAD
    instruction_offset = 0
    selected_rows: dict[int, bytes] = {}
    references: dict[int, dict[str, Any]] = {}
    p1_sha: list[str] = []
    row_sha: list[str] = []
    with cache_path.open("rb", buffering=0) as cache_stream, \
            instruction_path.open("rb", buffering=1 << 20) as instruction_stream:
        for node in range(P1_ROWS):
            raw_row = cache_stream.read(P1_ROW_BYTES)
            line = instruction_stream.readline()
            require(len(raw_row) == P1_ROW_BYTES and line.endswith(b"\n") and
                    b"\r" not in line and
                    not np.any(np.frombuffer(raw_row, dtype=np.uint8) > 80),
                    "p1_stream_row")
            try:
                record = json.loads(line.decode("ascii"))
            except (UnicodeError, ValueError) as exc:
                raise RuntimeError("p1_instruction_json") from exc
            predecessor = validate_p1_instruction(
                record, node, line, raw_row, predecessor, p1_sha, row_sha)
            p1_sha.append(record["p1_sha256"])
            row_sha.append(record["row_receipt"]["sha256"])
            if node in arithmetic_nodes:
                selected_rows[node] = raw_row
            if node in reference_nodes:
                references[node] = {
                    "node": node, "instruction_offset": instruction_offset,
                    "instruction_length": len(line),
                    "instruction_sha256": sha(line),
                    "ancestry_sha256": record["ancestry_sha256"],
                    "predecessor": record["predecessor"],
                    "p1_sha256": record["p1_sha256"],
                    "row_sha256": record["row_receipt"]["sha256"],
                    "origin_sha256": sha(canonical(record["origin"])),
                    "reductions_sha256": sha(canonical(record["reductions"])),
                    "scale": record["scale"],
                    "literal_input_sha256": record["literal_input_sha256"],
                }
            cache_hash.update(raw_row)
            instruction_hash.update(line)
            instruction_offset += len(line)
            if (node + 1) % 1024 == 0 or node + 1 == P1_ROWS:
                progress("parent-loading", parent="canonical-p1",
                         rows=node + 1, total=P1_ROWS)
        require(cache_stream.read(1) == b"" and instruction_stream.read(1) == b"",
                "p1_stream_trailing")
    require(cache_hash.hexdigest() == p1["cache"]["sha256"] and
            instruction_hash.hexdigest() == p1["instruction"]["sha256"] and
            instruction_offset == p1["instruction"]["bytes"] and
            predecessor == p1["manifest"]["ancestry_sha256"] and
            set(selected_rows) == arithmetic_nodes and set(references) == reference_nodes,
            "p1_stream_terminal")
    return {
        "parent": parent, "p1": p1, "rows": selected_rows,
        "references": references,
        "receipt": {
            "manifest_sha256": p1["manifest_sha256"],
            "cache_sha256": cache_hash.hexdigest(),
            "instruction_sha256": instruction_hash.hexdigest(),
            "instruction_final_head": predecessor,
            "rows": P1_ROWS, "cache_passes": 1, "instruction_passes": 1,
            "selected_arithmetic_rows": len(selected_rows),
            "selected_literal_roots": len(references),
        },
    }


def load_task712(root_v2: ModuleType, launch: dict[str, Any], task712_root: Path,
                 character: int) -> dict[str, Any]:
    progress("parent-loading", parent="task712", character=character)
    require(launch["task712_parent"] == root_v2.TASK712_PARENT, "task712_parent")
    descriptor = _runtime_parent(launch["task712_parent"], task712_root)
    tables = root_v2.ARITH.read_task712_envelope(descriptor, character)
    root_v2.check_table_transpose(tables["forward"]["B"], tables["adjoint"]["B"])
    require(tables["manifest_sha256"] == launch["task712_manifest_sha256"][character],
            "task712_manifest_join")
    return {"descriptor": descriptor, "tables": tables,
            "manifest_sha256": tables["manifest_sha256"]}


def replay_selected_seed(root_v2: ModuleType, seedred: dict[str, Any],
                  lower: dict[str, Any], p1: dict[str, Any],
                  task712: dict[str, Any], scalar: dict[str, Any]) -> dict[str, Any]:
    seed, character, q = scalar["seed"], scalar["character"], scalar["q"]
    progress("raw-seed-evaluation", seed=seed, character=character)
    context, words = root_v2.source_context()
    relator = tuple(int(value) for value in words["relators"][seed])
    raw_parts = root_v2.ARITH._seed_evaluate_seed(context, relator)
    d0, d1, d2, auxiliary = tuple(
        np.asarray(part, dtype=np.uint8).copy() for part in raw_parts)
    require(d0.shape == (4, SOURCE0C) and d1.shape == (4, SOURCE1C) and
            d2.shape == (4, SOURCE2C) and auxiliary.shape == (8,),
            "raw_seed_component_shapes")
    direct_receipt = scalar["character_record"]["direct_receipt"]
    raw_selected = pack(d2[character])
    direct_value = dot(q, d2[character])
    selected_direct = {
        "character": character, "seed": seed, "packed_sha256": sha(raw_selected),
        "support": int(np.count_nonzero(d2[character])), "scalar": direct_value,
        "direct_receipt_sha256": direct_receipt["sha256"],
    }
    require(selected_direct["packed_sha256"] == direct_receipt["raw_row_packed_sha256"][seed] and
            selected_direct["support"] == direct_receipt["raw_row_support"][seed] and
            direct_value == scalar["direct_value"], "selected_raw_direct_receipt_join")
    raw_receipt = sealed(SCHEMA + ".raw-seed", {
        "seed": seed, "character": character,
        "selected_direct_receipt": selected_direct,
        "compact_word": list(relator),
        "compact_word_sha256": sha(canonical(list(relator))),
        "word_dictionary_sha256": root_v2.ARITH.WORD_SHA,
        "relator_dictionary_sha256": root_v2.ARITH.WORD_RELATOR_SHA,
        "shared_legacy_arithmetic_sha256": LEGACY_ARITH_SHA256,
        "components": [
            component_receipt("d0", d0), component_receipt("d1", d1),
            component_receipt("d2", d2), component_receipt("aux", auxiliary),
        ],
    })
    selected_lifts: list[dict[str, Any]] = []
    total_selected = len(seedred["final_coefficients"])
    for count, (node, coefficient) in enumerate(seedred["final_coefficients"], start=1):
        p1_raw = p1["rows"][node]
        p1_dense = unpack(p1_raw, P1_ROW_TRITS).reshape(4, SOURCE2C)
        add_scaled(d2, p1_dense, 3 - coefficient)
        lower_row = lower["rows"][node]
        lift_components: list[dict[str, Any]] = [
            {"role": "p1-degree2", "bytes": len(p1_raw), "sha256": sha(p1_raw)}]
        if lower_row["kind"] == "old":
            old = unpack(lower_row["lower"], SOURCE0C + 8)
            grade = unpack(lower_row["grade"], 4 * SOURCE1C).reshape(4, SOURCE1C)
            add_scaled(d0[lower_row["owner"]], old[:SOURCE0C], 3 - coefficient)
            add_scaled(auxiliary, old[SOURCE0C:], 3 - coefficient)
            add_scaled(d1, grade, 3 - coefficient)
            lift_components.extend((
                {"role": "old-lower", "bytes": len(lower_row["lower"]),
                 "sha256": sha(lower_row["lower"])},
                {"role": "old-grade", "bytes": len(lower_row["grade"]),
                 "sha256": sha(lower_row["grade"])},
            ))
        else:
            basis = unpack(lower_row["basis"], SOURCE1C)
            add_scaled(d1[lower_row["owner"]], basis, 3 - coefficient)
            lift_components.append(
                {"role": "new-grade", "bytes": len(lower_row["basis"]),
                 "sha256": sha(lower_row["basis"])})
        selected_lifts.append({
            "selection_index": count - 1, "node": node,
            "coefficient": coefficient, "lower_kind": lower_row["kind"],
            "owner_character": lower_row["owner"],
            "p1_sha256": p1["references"][node]["p1_sha256"],
            "components": lift_components,
        })
        if count % 100 == 0 or count == total_selected:
            progress("selected-p1-subtraction", completed=count,
                     total=total_selected)
    lower_dense = np.concatenate((d0.reshape(-1), d1.reshape(-1), auxiliary))
    require(lower_dense.size == LOWER_WIDTH and not np.any(lower_dense),
            "complete_selected_seed_lower_zero")
    reduced_components = [
        component_receipt("d0", d0), component_receipt("d1", d1),
        component_receipt("d2", d2), component_receipt("aux", auxiliary),
    ]
    projected = root_v2.ARITH._seed_full_project(
        context, (d0, d1, d2, auxiliary), CHARACTERS[character])
    projected = tuple(np.asarray(part, dtype=np.uint8) for part in projected)
    require(not np.any(projected[0]) and not np.any(projected[1]) and
            not np.any(projected[3]) and
            np.array_equal(projected[2][character], d2[character]) and
            all(not np.any(projected[2][index]) for index in range(4) if index != character),
            "complete_lower_zero_projector_match")
    source = d2[character].copy()
    tables = task712["tables"]
    physical = apply_sparse(tables["forward"]["B"], SOURCE2C,
                            PHYSICAL_WIDTH, source)
    q_pair = dot(q, source)
    require(q_pair == scalar["value"], "q_dot_selected_source")
    subtraction = sealed(SCHEMA + ".complete-subtraction", {
        "formula_id": V541_FORMULA_ID,
        "seed": seed, "character": character,
        "raw_event_count": len(seedred["raw_events"]),
        "final_selected_count": total_selected,
        "arithmetic_coefficient_collection": "mod3-after-ordered-raw-events",
        "literal_coefficient_collection": False,
        "task554_blob_pass_sha256": lower["receipt"]["sha256"],
        "p1_cache_sha256": p1["receipt"]["cache_sha256"],
        "selected_lift_receipt_sha256": sha(canonical(selected_lifts)),
        "reduced_components": reduced_components,
        "lower_width": LOWER_WIDTH, "lower_nonzero_count": 0,
        "lower_zero_count": LOWER_WIDTH,
        "lower_dense_sha256": sha(lower_dense.tobytes()),
        "plain_character_source_sha256": sha(pack(source)),
        "full_projector_character_source_sha256": sha(pack(projected[2][character])),
        "full_projector_other_character_nonzero_count": 0,
        "full_projector_applied_to_complete_defect": True,
    })
    projector_factors = []
    for label in CHARACTERS:
        sign = int(root_v2.ARITH._seed_cv(CHARACTERS[character], label))
        require(sign in (1, 2), "selected_character_projector_sign")
        pure_word = list(root_v2.ARITH.SEED_PURE_WORDS[label])
        projector_factors.append({
            "label": list(label), "pure_word": pure_word,
            "pure_word_sha256": sha(canonical(pure_word)),
            "source_character_sign": sign,
        })
    literal_word_dag = sealed(SCHEMA + ".literal-word-dag", {
        "v518_formulae": ["1.3", "2.2", "4.3"],
        "coefficient_convention": {"0": "identity", "1": "word", "2": "inverse"},
        "defect": {
            "operation": "ordered-product",
            "seed_factor": {"seed": seed, "exponent": 1,
                            "compact_word_sha256": raw_receipt["compact_word_sha256"]},
            "p1_factor_sequence": {
                "source": "raw_events", "order": "event_id-ascending",
                "root_join": "raw_events.global_index=p1_roots.node",
                "root_field": "p1_sha256",
                "exponent_rule": "(3-coefficient)%3",
                "coefficient_collection": False,
            },
        },
        "projector": {
            "operation": "ordered-character-projector",
            "character": list(CHARACTERS[character]),
            "order": [list(label) for label in CHARACTERS],
            "factors": projector_factors,
        },
        "actor_path": [],
        "forward_B": tables["identity"]["forward:B"],
        "six_source_tag_replay": True,
        "eleven_slot_replay": False,
        "full_A0_witness": False,
    })
    ancestry = sealed(SCHEMA + ".selected-seed-ancestry", {
        "seed": seed, "character": character,
        "task554_body_sha256": seedred["body_sha256"],
        "selected_seed_relation": seedred["selected_relation"],
        "raw_event_count": len(seedred["raw_events"]),
        "raw_events": seedred["raw_events"],
        "raw_event_final_head": seedred["raw_event_final_head"],
        "final_support": total_selected,
        "final_coefficients": seedred["final_coefficients"],
        "p1_roots": [p1["references"][node]
                     for node in sorted(p1["references"])],
        "selected_lifts": selected_lifts,
        "literal_word_dag": literal_word_dag,
        "p1_parent": p1["receipt"],
        "task554_blob_pass": lower["receipt"],
    })
    return {
        "raw_seed": raw_receipt, "subtraction": subtraction,
        "ancestry": ancestry, "literal_word_dag": literal_word_dag,
        "source": source, "physical": physical, "q_pair": q_pair,
        "task712_identity": tables["identity"],
    }


def validate_old_state(state_root: Path
                          ) -> dict[str, Any]:
    progress("parent-loading", parent="task904-state", rank=STATE_RANK)
    root = state_root.resolve()
    require(root.is_dir(), "state_artifact_root")
    state_manifest, state_manifest_raw = read_json_exact(
        safe_file(root, "state/manifest.json"), 7780, STATE_MANIFEST_SHA256, 1 << 20)
    state_result, state_result_raw = read_json_exact(
        safe_file(root, "output/result.json"), *STATE_RESULT_PIN, 1 << 24)
    state_terminal, state_terminal_raw = read_json_exact(
        safe_file(root, "output/terminal.json"), *STATE_TERMINAL_PIN, 1 << 24)
    checker, checker_raw = read_json_exact(
        safe_file(root, "checker-result.json"), *STATE_CHECKER_PIN, 1 << 20)
    require(checker.get("status") == "PASS" and checker.get("verified") is False and
            state_result.get("kind") == "Separator" and
            state_terminal.get("kind") == "Separator" and
            state_result.get("state_manifest_sha256") == STATE_MANIFEST_SHA256 and
            state_terminal.get("state_manifest_sha256") == STATE_MANIFEST_SHA256 and
            state_result.get("target_reduction") == state_terminal.get("target_reduction"),
            "state_result_checker_join")
    target = state_result["target_reduction"]
    require(target.get("schema") ==
            "d972.r07.physical-state.target-reduction.v1" and
            target.get("kind") == "Separator" and
            target.get("state_generation") == STATE_GENERATION and
            target.get("state_head") == STATE_HEAD and
            target.get("state_rank") == STATE_RANK and
            target.get("rho2_sha256") == RHO2_SHA256 and
            len(target.get("reductions", [])) == 884 and
            isinstance(target.get("remainder"), str) and
            len(target["remainder"]) == 2 * PHYSICAL_BYTES,
            "old_target_reduction_shape")
    head, _ = read_json_exact(
        safe_file(root, "state/HEAD"), 299,
        "f789ac352864ae662beced75f9004887fe677f81eee922eb9d9200dcaf6860ef", 1 << 20)
    state = state_manifest
    require(state["generation"] == head["generation"] == STATE_GENERATION and
            state["cursor"] == head["cursor"] == STATE_GENERATION and
            state["rank"] == head["rank"] == STATE_RANK and
            state["instructions"]["final_head"] == head["rolling_head"] == STATE_HEAD and
            head["manifest_sha256"] == STATE_MANIFEST_SHA256 and head["eof"] is True and
            state["physical"]["sha256"] == STATE_PHYSICAL_SHA256 and
            state["p1_companions"]["sha256"] == STATE_COMPANION_SHA256 and
            state["instructions"]["sha256"] == STATE_INSTRUCTION_SHA256,
            "state_fixed_manifest")
    require(checker.get("physical_rank") == STATE_RANK and
            checker.get("target_reductions") == 884 and
            checker.get("nonmonotone_insertion") is True and
            checker.get("cross_checked") is False,
            "state_accepted_checker_premise")
    require({item.name for item in (root / "state").iterdir()} ==
            set(state["candidate_roster"]), "state_exact_roster")
    # The accepted derivation is a premise.  Hash/parse the instruction file
    # once, retaining only positioned pivot roots, never its 610996 reductions.
    instruction_path = safe_file(root, "state/instructions.jsonl")
    require(instruction_path.stat().st_size == state["instructions"]["bytes"],
            "state_instruction_size")
    instruction_hash = hashlib.sha256()
    instruction_bytes = 0
    rolling = ZERO_HEAD
    pivots: list[dict[str, Any]] = []
    leads: list[int] = []
    with instruction_path.open("rb", buffering=1 << 20) as stream:
        for offer in range(STATE_GENERATION):
            line = stream.readline()
            require(line.endswith(b"\n") and b"\r" not in line,
                    "state_instruction_eof")
            record = json.loads(line.decode("ascii"))
            unsigned = {key: value for key, value in record.items()
                        if key != "rolling_sha256"}
            rolling = sha(bytes.fromhex(rolling) + canonical(unsigned))
            require(canonical(record) == line and record["offer"] == offer and
                    record["rolling_sha256"] == rolling, "state_instruction_rolling")
            instruction_hash.update(line)
            instruction_bytes += len(line)
            if record["kind"] == "physical_pivot":
                require(record["physical_offset"] == len(pivots) * PHYSICAL_BYTES and
                        record["coefficient_offset"] == len(pivots) * 2015 and
                        record["rank"] == len(pivots) + 1 and
                        plain_int(record["lead"]) and
                        0 <= record["lead"] < PHYSICAL_WIDTH and
                        record["lead"] not in leads and record["sigma"] in (1, 2) and
                        record["lower_zero"] is True, "state_pivot_metadata")
                pivots.append({key: record[key] for key in (
                    "offer", "lead", "physical_offset", "coefficient_offset",
                    "rank", "rolling_sha256")})
                leads.append(record["lead"])
            else:
                require(record["kind"] == "skipped", "state_nonpivot_kind")
            if (offer + 1) % 2048 == 0 or offer + 1 == STATE_GENERATION:
                progress("parent-loading", parent="task904-instructions",
                         records=offer + 1, total=STATE_GENERATION)
        require(stream.read(1) == b"", "state_instruction_trailing")
    require(instruction_bytes == state["instructions"]["bytes"] and
            instruction_hash.hexdigest() == STATE_INSTRUCTION_SHA256 and
            rolling == STATE_HEAD and len(pivots) == STATE_RANK,
            "state_instruction_terminal")
    physical_raw = read_exact(safe_file(root, "state/physical.bin"),
                              STATE_RANK * PHYSICAL_BYTES, STATE_PHYSICAL_SHA256)
    require(not np.any(np.frombuffer(physical_raw, dtype=np.uint8) > 80),
            "state_physical_packing")
    packed_rows = [physical_raw[start:start + PHYSICAL_BYTES]
                   for start in range(0, len(physical_raw), PHYSICAL_BYTES)]
    file_sha(safe_file(root, "state/physical-p1-coeff.bin"),
             STATE_RANK * 2015, STATE_COMPANION_SHA256)
    return {
        "root": root, "manifest": state_manifest,
        "manifest_sha256": sha(state_manifest_raw), "records": pivots,
        "packed_rows": packed_rows, "leads": leads,
        "target": target, "target_sha256": sha(canonical(target)),
        "result_sha256": sha(state_result_raw),
        "terminal_sha256": sha(state_terminal_raw),
        "checker_sha256": sha(checker_raw),
        "nonmonotone_transitions": sum(
            1 for left, right in zip(leads, leads[1:]) if right < left),
    }


def validate_current_state(state_root: Path, delta_root: Path,
                           scalar: dict[str, Any]) -> dict[str, Any]:
    old = validate_old_state(state_root)
    progress("parent-loading", parent="accepted-seed30-delta", rank=CURRENT_RANK)
    objects = {name: read_json_exact(safe_file(delta_root, name), *pin)[0]
               for name, pin in DELTA_FILES.items()}
    manifest, result = objects["output/manifest.json"], objects["output/result.json"]
    instruction, checker = objects["output/instruction.json"], objects["checker-result.json"]
    require(all(sealed_ok(value) for value in
                (manifest, result, result["pivot"], result["target"])) and
            manifest["mode"] == "parent-plus-one-pivot-delta" and
            manifest["parent_state_manifest_sha256"] == STATE_MANIFEST_SHA256 and
            manifest["parent_state_head"] == STATE_HEAD and
            manifest["state_head"] == CURRENT_HEAD and
            manifest["rank_before"] == STATE_RANK and manifest["rank_after"] == CURRENT_RANK and
            manifest["terminal"] == result["kind"] == checker["kind"] == "Separator" and
            checker["status"] == "PASS" and checker["manifest_sha256"] ==
            DELTA_FILES["output/manifest.json"][1] and checker["result_sha256"] ==
            DELTA_FILES["output/result.json"][1] and checker["state_head"] == CURRENT_HEAD and
            checker["rank_after"] == CURRENT_RANK and checker["new_pivots"] == 1 and
            checker["old_state_derivation_premise"] is True and
            all(value["verified"] is False and value["cross_checked"] is False
                for value in (manifest, result, checker, objects["source-receipt.json"])),
            "accepted_delta_authority")
    base_parent = result["parents"]["state"]
    require(base_parent["artifact"] == STATE_ARTIFACT and
            base_parent["manifest_sha256"] == old["manifest_sha256"] and
            base_parent["head"] == STATE_HEAD and base_parent["rank"] == STATE_RANK and
            base_parent["generation"] == STATE_GENERATION and
            base_parent["physical_sha256"] == STATE_PHYSICAL_SHA256 and
            base_parent["companion_sha256"] == STATE_COMPANION_SHA256 and
            base_parent["instruction_sha256"] == STATE_INSTRUCTION_SHA256 and
            base_parent["checker_sha256"] == old["checker_sha256"] and
            base_parent["result_sha256"] == old["result_sha256"] and
            base_parent["target_sha256"] == old["target_sha256"] and
            result["target"]["parent_target_sha256"] == old["target_sha256"] and
            result["target"]["parent_result_sha256"] == old["result_sha256"],
            "accepted_delta_base_join")
    output = delta_root / "output"
    require(set(manifest["file_roster"]) == {path.name for path in output.iterdir()},
            "accepted_delta_roster")
    payloads = {item["file"]: read_exact(safe_file(output, item["file"]),
                item["bytes"], item["sha256"]) for item in manifest["files"]}
    unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
    require(instruction["predecessor"] == STATE_HEAD and
            instruction["rolling_sha256"] == CURRENT_HEAD and
            sha(bytes.fromhex(STATE_HEAD) + canonical(unsigned)) == CURRENT_HEAD and
            instruction["offer"] == STATE_GENERATION and
            instruction["generation"] == result["pivot"]["generation_after"] == CURRENT_GENERATION and
            instruction["rank"] == result["pivot"]["rank_after"] == CURRENT_RANK and
            instruction["lead"] == result["pivot"]["lead"] and
            instruction["sigma"] == result["pivot"]["scale"] and
            instruction["physical_offset"] == STATE_RANK * PHYSICAL_BYTES and
            instruction["delta_physical_offset"] == 0 and
            result["pivot"]["head_after"] == result["target"]["state_head"] == CURRENT_HEAD and
            result["target"]["state_rank"] == CURRENT_RANK and
            checker["instruction_sha256"] == DELTA_FILES["output/instruction.json"][1],
            "accepted_delta_single_append")
    normalized = payloads["physical-normalized.bin"]
    remainder = payloads["target-remainder.bin"]
    lambda_raw = payloads["lambda.bin"]
    require(sha(normalized) == result["pivot"]["normalized_sha256"] ==
            instruction["physical"]["sha256"] and
            sha(remainder) == result["target"]["remainder_sha256"] ==
            CURRENT_TARGET_REMAINDER_SHA256 and
            sha(lambda_raw) == result["separator"]["lambda_sha256"] == CURRENT_LAMBDA_SHA256,
            "accepted_delta_saved_rows")
    row, target, lam = (unpack(raw, PHYSICAL_WIDTH)
                        for raw in (normalized, remainder, lambda_raw))
    lead = instruction["lead"]
    require(lead not in old["leads"] and row[lead] == 1 and
            all(row[index] == target[index] == 0 for index in old["leads"]) and
            target[lead] == 0 and dot(lam, row) == 0 and dot(lam, target) == 1,
            "current_delta_row_and_target")
    separator = scalar["launch"]["separator"]
    require(separator["artifact"] == DELTA_ARTIFACT and
            separator["files"] == [{"file": name, "bytes": pin[0], "sha256": pin[1]}
                                   for name, pin in sorted(DELTA_FILES.items())] and
            separator["generation"] == CURRENT_GENERATION and separator["rank"] == CURRENT_RANK and
            separator["head"] == CURRENT_HEAD and separator["lambda_sha256"] == CURRENT_LAMBDA_SHA256 and
            separator["old_state_manifest_sha256"] == STATE_MANIFEST_SHA256 and
            separator["old_state_physical_sha256"] == STATE_PHYSICAL_SHA256 and
            separator["old_state_checker_sha256"] == old["checker_sha256"] and
            separator["old_state_derivation_premise"] is True and
            separator["old_state_rows_checked"] == STATE_RANK and
            separator["new_pivot_rows_checked"] == 1 and
            separator["lambda_pivots"] == 0 and separator["lambda_saved_remainder"] == 1,
            "current_scalar_state_join")
    delta_parent = {
        "artifact": DELTA_ARTIFACT, "files": separator["files"],
        "pivot_sha256": result["pivot"]["sha256"],
        "target_sha256": sha(canonical(result["target"])),
        "physical": receipt("physical-normalized.bin", normalized),
        "target_remainder": receipt("target-remainder.bin", remainder),
        "lambda": receipt("lambda.bin", lambda_raw),
    }
    current_parent = {
        "mode": "immutable-state-plus-one-accepted-delta",
        "base": base_parent, "delta": delta_parent,
        "manifest_sha256": DELTA_FILES["output/manifest.json"][1],
        "head": CURRENT_HEAD, "generation": CURRENT_GENERATION, "rank": CURRENT_RANK,
        "old_derivation_accepted_as_premise": True,
        "prior_delta_accepted_as_premise": True,
    }
    # References and one saved row are appended in memory; no parent is copied
    # to a new physical state file and no old target elimination is executed.
    records = [*old["records"], {
        "offer": instruction["offer"], "lead": lead,
        "physical_offset": instruction["physical_offset"], "coefficient_offset": None,
        "rank": CURRENT_RANK, "rolling_sha256": CURRENT_HEAD}]
    return {
        "old": old, "parent": current_parent, "records": records,
        "rho2_parent": result["parents"]["rho2"],
        "packed_rows": [*old["packed_rows"], normalized], "leads": [*old["leads"], lead],
        "lambda": lam, "lambda_receipt": receipt("lambda.bin", lambda_raw),
        "target": result["target"], "target_sha256": sha(canonical(result["target"])),
        "old_remainder": remainder, "result_sha256": DELTA_FILES["output/result.json"][1],
        "manifest_sha256": DELTA_FILES["output/manifest.json"][1],
        "prior_target_reduction_count": len(old["target"]["reductions"]) +
                                        len(result["target"]["new_reductions"]),
    }


def physical_reduce(raw: bytes, pivots: list[dict[str, Any]],
                    rows: list[bytes], *, verbose: bool = True
                    ) -> tuple[bytes, list[dict[str, Any]]]:
    """One insertion-order sweep; no numeric lead sorting or free-column stop."""
    validate_packed(raw, PHYSICAL_WIDTH)
    require(len(pivots) == len(rows) and
            len({item["lead"] for item in pivots}) == len(pivots),
            "physical_parent_rows")
    accumulator = np.frombuffer(raw, dtype=np.uint8).copy()
    reductions: list[dict[str, Any]] = []
    for pivot_id, (record, packed_row) in enumerate(zip(pivots, rows)):
        scalar = packed_trit(accumulator, record["lead"])
        if scalar:
            validate_packed(packed_row, PHYSICAL_WIDTH)
            row = np.frombuffer(packed_row, dtype=np.uint8)
            require(packed_trit(row, record["lead"]) == 1, "old_normalized_lead")
            packed_subtract(accumulator, row, scalar)
            reductions.append({
                "pivot_id": pivot_id, "offer": record["offer"],
                "lead": record["lead"], "scalar": scalar,
                "physical_offset": record["physical_offset"],
                "row_sha256": sha(packed_row),
            })
        if verbose and ((pivot_id + 1) % 128 == 0 or pivot_id + 1 == len(pivots)):
            progress("physical-reduction", pivots=pivot_id + 1,
                     total=len(pivots), reductions=len(reductions))
    require(all(packed_trit(accumulator, record["lead"]) == 0 for record in pivots),
            "new_remainder_earlier_pivot_zeros")
    return accumulator.tobytes(), reductions


def normalize_pivot(remainder: bytes, old_leads: list[int]
                    ) -> tuple[bytes, int, int]:
    first = first_nonzero(remainder, PHYSICAL_WIDTH)
    require(first is not None, "new_pivot_nonzero_rank_gate")
    lead, scale = first
    require(lead not in old_leads and scale in (1, 2), "new_unique_lead")
    dense = unpack(remainder, PHYSICAL_WIDTH)
    require(all(dense[index] == 0 for index in old_leads), "new_earlier_pivot_zeros")
    normalized = ((dense.astype(np.uint16) * scale) % 3).astype(np.uint8)
    require(normalized[lead] == 1 and
            all(normalized[index] == 0 for index in old_leads), "new_normalization")
    return pack(normalized), lead, scale


def update_target(old: bytes, normalized: bytes, lead: int,
                  old_leads: list[int]) -> tuple[bytes, int]:
    validate_packed(old, PHYSICAL_WIDTH)
    validate_packed(normalized, PHYSICAL_WIDTH)
    accumulator = np.frombuffer(old, dtype=np.uint8).copy()
    row = np.frombuffer(normalized, dtype=np.uint8)
    require(packed_trit(row, lead) == 1 and
            all(packed_trit(accumulator, index) == packed_trit(row, index) == 0
                for index in old_leads), "target_parent_and_new_pivot_zeros")
    scalar = packed_trit(accumulator, lead)
    if scalar:
        packed_subtract(accumulator, row, scalar)
    require(all(packed_trit(accumulator, index) == 0
                for index in [*old_leads, lead]), "target_delta_earlier_zeros")
    return accumulator.tobytes(), scalar


def check_final_separator(functional: np.ndarray, rows: list[bytes],
                          parent_target_raw: bytes, remainder_raw: bytes, *,
                          verbose: bool = True) -> dict[str, Any]:
    pairings = bytearray()
    for index, raw in enumerate(rows):
        value = dot(functional, unpack(raw, PHYSICAL_WIDTH))
        require(value == 0, "final_separator_nonzero_row:" + str(index))
        pairings.append(value)
        if verbose and ((index + 1) % 256 == 0 or index + 1 == len(rows)):
            progress("final-separator-direct-pairings", rows=index + 1, total=len(rows))
    require(dot(functional, unpack(parent_target_raw, PHYSICAL_WIDTH)) == 1 and
            dot(functional, unpack(remainder_raw, PHYSICAL_WIDTH)) == 1,
            "final_separator_target_pairings")
    return {"rows": len(rows), "row_pairings_sha256": sha(bytes(pairings)),
            "lambda_pivots": 0, "lambda_parent_remainder": 1, "lambda_new_remainder": 1}


def separator_after_append(parent_target_raw: bytes, remainder_raw: bytes,
                           pivots: list[dict[str, Any]], rows: list[bytes],
                           normalized: bytes, lead: int, *, verbose: bool = True
                           ) -> tuple[dict[str, Any], bytes]:
    free = first_nonzero(remainder_raw, PHYSICAL_WIDTH)
    require(free is not None and free[0] not in {item["lead"] for item in pivots} | {lead},
            "next_separator_free_coordinate")
    functional = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    functional[free[0]] = free[1]  # Inverse of a nonzero F3 element is itself.
    all_pivots = [*pivots, {"offer": CURRENT_GENERATION, "lead": lead}]
    all_rows = [*rows, normalized]
    transcript: list[dict[str, Any]] = []
    for pivot_id in range(len(all_pivots) - 1, -1, -1):
        record = all_pivots[pivot_id]
        packed_row = all_rows[pivot_id]
        row = unpack(packed_row, PHYSICAL_WIDTH)
        coordinate = record["lead"]
        require(row[coordinate] == 1 and functional[coordinate] == 0,
                "next_separator_normalized_coordinate")
        value = (-dot(row, functional)) % 3
        functional[coordinate] = value
        require(dot(row, functional) == 0, "next_separator_reverse_equation")
        transcript.append({
            "reverse_index": pivot_id, "pivot_id": pivot_id,
            "offer": record["offer"], "lead": coordinate,
            "row_sha256": sha(packed_row), "lambda_value": value, "equation": 0,
        })
        if verbose and (len(transcript) % 256 == 0 or pivot_id == 0):
            progress("next-separator", rows=len(transcript), total=len(all_rows))
    direct_pairing = check_final_separator(
        functional, all_rows, parent_target_raw, remainder_raw, verbose=verbose)
    packed_lambda = pack(functional)
    return {
        "free_coordinate": free[0], "free_value": free[1],
        "transcript": transcript, "lambda_sha256": sha(packed_lambda),
        "lambda_rho2": 1, "lambda_physical_pivots": 0,
        "lambda_rho2_basis": "accepted-parent-target-derivation",
        "direct_pairing": direct_pairing,
    }, packed_lambda


def join_parents(root_v2: ModuleType, scalar: dict[str, Any],
                 seedred: dict[str, Any], p1: dict[str, Any],
                 task712: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    source_state = state["old"]["manifest"]
    require(source_state["p1_identity"]["manifest_sha256"] ==
            p1["receipt"]["manifest_sha256"] and
            source_state["p1_identity"]["cache_sha256"] == p1["receipt"]["cache_sha256"] and
            source_state["p1_identity"]["instruction"]["sha256"] ==
            p1["receipt"]["instruction_sha256"] and
            source_state["source_ancestry"]["prepare_body_sha256"] ==
            seedred["body_sha256"][0] and
            source_state["source_ancestry"]["parents"] == seedred["body_sha256"][1:] and
            source_state["task712"]["tables"]["manifest_sha256"] ==
            task712["manifest_sha256"] and
            scalar["violation"]["p1_manifest_sha256"] == p1["receipt"]["manifest_sha256"] and
            scalar["raw_dual"]["B_adj_table_identity"] ==
            task712["tables"]["identity"]["adjoint:B"], "current_source_parent_joins")
    require(state["rho2_parent"]["packed_sha256"] == RHO2_SHA256 and
            state["target"]["rho2_sha256"] == RHO2_SHA256 and
            state["rho2_parent"]["manifest_sha256"] ==
            state["old"]["target"]["target_parent_manifest_sha256"],
            "retained_target_parent_join")
    return {
        "scalar": {
            "final_artifact": SCALAR_FINAL_ARTIFACT,
            "launch": scalar["launch_receipt"], "source": scalar["source_receipt"],
            **{key: scalar[key] for key in ("manifest_sha256", "result_sha256", "checker_sha256")},
            "character_sha256": scalar["character_record"]["sha256"],
            "violation_sha256": scalar["violation"]["sha256"],
            "raw_dual_sha256": scalar["raw_dual"]["sha256"],
            "selected_seed_relation_sha256": scalar["selected_relation"]["sha256"],
            "relation_receipt_sha256": scalar["relation_receipt_sha256"],
        },
        "task554": {
            **{key: seedred["parent"][key]
               for key in ("source_run", "source_attempt", "source_head", "artifacts")},
            "body_sha256": seedred["body_sha256"],
        },
        "p1": {key: value for key, value in p1["parent"].items() if key != "root"},
        "task712": {
            "artifact": dict(root_v2.TASK712_PARENT),
            "manifest_sha256": task712["manifest_sha256"],
            "B_fwd_identity": task712["tables"]["identity"]["forward:B"],
        },
        "state": state["parent"],
        "rho2": {**state["rho2_parent"], "target_derivation_accepted_as_premise": True},
        "source_modules": {
            ROOT_V2_PATH.name: ROOT_V2_SHA256,
            LEGACY_ARITH_PATH.name: LEGACY_ARITH_SHA256,
        },
    }


def materialize(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    output_root = args.output_root.absolute()
    require(not output_root.exists() and not output_root.is_symlink(), "fresh_output_root")
    parent_roots = [args.scalar_root, args.delta_root, args.prepare_root,
                    *args.block_root, args.p1_root, args.task712_root,
                    args.state_root]
    for parent in parent_roots:
        require(parent.is_dir() and parent.resolve() != output_root.resolve() and
                parent.resolve() not in output_root.resolve().parents and
                output_root.resolve() not in parent.resolve().parents,
                "output_disjoint_from_parents")
    progress("parent-loading", parent="source-modules")
    root_v2 = dependencies()
    scalar = validate_scalar_parent(args.scalar_root)
    state = validate_current_state(args.state_root, args.delta_root, scalar)
    seedred = collect_selected_seedred(root_v2, scalar, args.prepare_root,
                                args.block_root)
    lower = load_selected_lower(seedred)
    arithmetic_nodes = {node for node, _ in seedred["final_coefficients"]}
    reference_nodes = {item["global_index"] for item in seedred["raw_events"]}
    p1 = load_selected_p1(root_v2, scalar["launch"], args.p1_root,
                          reference_nodes, arithmetic_nodes)
    task712 = load_task712(root_v2, scalar["launch"], args.task712_root, scalar["character"])
    parents = join_parents(root_v2, scalar, seedred, p1, task712, state)
    replay = replay_selected_seed(root_v2, seedred, lower, p1, task712, scalar)
    value = scalar["value"]
    forward = task712["tables"]["forward"]["B"]
    pulled = apply_sparse(([dst, src, coefficient] for src, dst, coefficient in forward),
                          PHYSICAL_WIDTH, SOURCE2C, state["lambda"])
    require(np.array_equal(pulled, scalar["q"]) and
            dot(state["lambda"], replay["physical"]) == replay["q_pair"] == value,
            "joined_actual_q_and_physical_pairings")
    raw_physical = pack(replay["physical"])
    raw_source = pack(replay["source"])
    raw_materialization = sealed(SCHEMA + ".raw-materialization", {
        "violation_sha256": scalar["violation"]["sha256"],
        "raw_dual_sha256": scalar["raw_dual"]["sha256"],
        "lambda_sha256": CURRENT_LAMBDA_SHA256,
        "raw_q_sha256": scalar["q_receipt"]["sha256"],
        "raw_seed_sha256": replay["raw_seed"]["sha256"],
        "source_ancestry_sha256": replay["ancestry"]["sha256"],
        "lower_zero_receipt_sha256": replay["subtraction"]["sha256"],
        "raw_word_sha256": replay["literal_word_dag"]["sha256"],
        "raw_source_sha256": sha(raw_source), "raw_physical_sha256": sha(raw_physical),
        "forward_B": task712["tables"]["identity"]["forward:B"],
        "actor_path": [], "q_d": value, "lambda_G": value,
    })
    progress("physical-reduction", pivots=0, total=CURRENT_RANK)
    remainder, reductions = physical_reduce(raw_physical, state["records"],
                                            state["packed_rows"])
    normalized, lead, scale = normalize_pivot(remainder, state["leads"])
    require(dot(state["lambda"], unpack(remainder, PHYSICAL_WIDTH)) == value and
            dot(state["lambda"], unpack(normalized, PHYSICAL_WIDTH)) == (value * scale) % 3,
            "raw_remainder_normalized_pairings")
    normalized_word = sealed(SCHEMA + ".normalized-word-dag", {
        "v518_formula": "4.3", "raw_word_sha256": replay["literal_word_dag"]["sha256"],
        "operation": "ordered-product-then-scale",
        "parent_state_head": CURRENT_HEAD, "parent_state_manifest_sha256": state["manifest_sha256"],
        "reductions": [{
            "pivot_id": item["pivot_id"], "offer": item["offer"],
            "instruction_rolling_sha256": state["records"][item["pivot_id"]]["rolling_sha256"],
            "row_sha256": item["row_sha256"],
            "coefficient": item["scalar"], "literal_exponent": (3 - item["scalar"]) % 3,
        } for item in reductions],
        "scale": scale, "coefficient_two_means": "inverse",
        "coefficient_collection": False,
    })
    instruction_body = {
        "schema": SCHEMA + ".state-instruction", "kind": "physical_pivot",
        "offer": CURRENT_GENERATION, "generation": CURRENT_GENERATION + 1,
        "predecessor": CURRENT_HEAD, "parent_state": parents["state"],
        "raw_materialization_sha256": raw_materialization["sha256"],
        "source_ancestry_sha256": replay["ancestry"]["sha256"],
        "normalized_word_sha256": normalized_word["sha256"],
        "top": receipt("physical-raw.bin", raw_physical),
        "remainder": receipt("physical-remainder.bin", remainder),
        "physical": receipt("physical-normalized.bin", normalized),
        "reductions": reductions, "lead": lead, "sigma": scale,
        "lower_zero": True, "physical_zero": False, "rank": CURRENT_RANK + 1,
        "physical_offset": CURRENT_RANK * PHYSICAL_BYTES, "delta_physical_offset": 0,
        "coefficient_offset": None, "coefficient_representation": "parent-literal-DAG",
    }
    new_head = sha(bytes.fromhex(CURRENT_HEAD) + canonical(instruction_body))
    instruction = {**instruction_body, "rolling_sha256": new_head}
    instruction_raw = canonical(instruction)
    pivot = sealed(SCHEMA + ".physical-pivot", {
        "raw_materialization_sha256": raw_materialization["sha256"],
        "offer": CURRENT_GENERATION, "pivot_id": CURRENT_RANK,
        "lead": lead, "scale": scale,
        "rank_before": CURRENT_RANK, "rank_after": CURRENT_RANK + 1,
        "generation_before": CURRENT_GENERATION, "generation_after": CURRENT_GENERATION + 1,
        "head_before": CURRENT_HEAD, "head_after": new_head,
        "instruction_sha256": sha(instruction_raw), "reductions": reductions,
        "raw_sha256": sha(raw_physical), "remainder_sha256": sha(remainder),
        "normalized_sha256": sha(normalized), "earlier_pivot_zero_count": CURRENT_RANK,
        "lambda_raw": value, "lambda_remainder": value, "lambda_normalized": (value * scale) % 3,
        "literal_word_dag": normalized_word,
    })
    progress("target-append", parent_reductions=state["prior_target_reduction_count"], new_pivots=1,
             rank_before=CURRENT_RANK, rank_after=CURRENT_RANK + 1)
    target_raw, target_scalar = update_target(state["old_remainder"], normalized,
                                               lead, state["leads"])
    kind = "Separator" if first_nonzero(target_raw, PHYSICAL_WIDTH) else "ConnectionMemberCandidate"
    target_update = sealed(SCHEMA + ".target-update", {
        "parent_target_sha256": state["target_sha256"],
        "parent_result_sha256": state["result_sha256"],
        "old_remainder_sha256": CURRENT_TARGET_REMAINDER_SHA256,
        "old_reduction_count": state["prior_target_reduction_count"], "rho2_sha256": RHO2_SHA256,
        "state_head": new_head, "state_rank": CURRENT_RANK + 1,
        "scalar": target_scalar, "new_pivots_examined": 1,
        "new_reductions": ([{
            "pivot_id": CURRENT_RANK, "offer": CURRENT_GENERATION,
            "lead": lead, "scalar": target_scalar,
            "physical_offset": CURRENT_RANK * PHYSICAL_BYTES, "row_sha256": sha(normalized),
        }] if target_scalar else []),
        "remainder_sha256": sha(target_raw), "kind": kind,
        "old_target_history_copied": False, "old_target_history_replayed": False,
    })
    next_separator = None
    next_lambda = None
    if kind == "Separator":
        next_separator, next_lambda = separator_after_append(
            state["old_remainder"], target_raw, state["records"], state["packed_rows"], normalized, lead)
    result = sealed(SCHEMA + ".result", {
        "status": "PASS", "kind": kind, "candidate": True,
        "verified": False, "cross_checked": False, "claims": CLAIMS,
        "parents": parents, "raw_seed": replay["raw_seed"],
        "subtraction": replay["subtraction"], "ancestry": replay["ancestry"],
        "raw_materialization": raw_materialization,
        "pairings": {"q_d": value, "lambda_G": value, "B_adjoint_q_equal": True},
        "pivot": pivot, "target": target_update, "separator": next_separator,
        "literal_replay": {
            "formal_graded_word_dag": True, "parent_state_ancestry_premise": True,
            "normalized_exponent_pair": "NOT_REPLAYED", "eleven_slot_replay": False,
            "full_A0_witness": False, "grade2_positive_terminal_complete": False,
        },
    })
    # Only the new delta is published, after every arithmetic acceptance gate.
    output_root.mkdir(parents=True, exist_ok=False)
    files = [atomic_write(output_root, name, raw) for name, raw in (
        ("source-d.bin", raw_source), ("physical-raw.bin", raw_physical),
        ("physical-remainder.bin", remainder), ("physical-normalized.bin", normalized),
        ("target-remainder.bin", target_raw), ("instruction.json", instruction_raw))]
    if next_lambda is not None:
        files.append(atomic_write(output_root, "lambda.bin", next_lambda))
    files.append(atomic_json(output_root, "result.json", result))
    manifest = sealed(SCHEMA + ".manifest", {
        "mode": "parent-plus-one-pivot-delta", "candidate": True,
        "verified": False, "cross_checked": False,
        "files": sorted(files, key=lambda item: item["file"]),
        "file_roster": sorted([item["file"] for item in files] + ["manifest.json"]),
        "parent_state_manifest_sha256": state["manifest_sha256"],
        "parent_state_head": CURRENT_HEAD, "state_head": new_head,
        "rank_before": CURRENT_RANK, "rank_after": CURRENT_RANK + 1,
        "result_sha256": sha(canonical(result)), "terminal": kind,
        "parent_state_copied": False,
    })
    manifest_receipt = atomic_json(output_root, "manifest.json", manifest)
    progress("terminal", kind=kind, rank=CURRENT_RANK + 1,
             elapsed_seconds=round(time.monotonic() - started, 3))
    return {"status": "PASS", "kind": kind, "rank_before": CURRENT_RANK,
            "rank_after": CURRENT_RANK + 1, "manifest_sha256": manifest_receipt["sha256"],
            "verified": False, "cross_checked": False}


def selftest() -> dict[str, Any]:
    """Three tiny changed-interface canaries, with no historical parents."""
    first = sealed("synthetic-first-root", {"character": 2, "seed": 7, "scalar": 2})
    require(sealed_ok(first) and first["seed"] != 30 and
            not sealed_ok({**first, "seed": 30}), "selected_authority_seal")
    old_row = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    old_row[[2, 4]] = 1
    saved_delta = old_row * 0
    saved_delta[[0, 3]] = 1
    rows = [pack(old_row), pack(saved_delta)]
    pivots = [{"offer": 0, "lead": 2, "physical_offset": 0},
              {"offer": 1, "lead": 0, "physical_offset": PHYSICAL_BYTES}]
    raw = ((old_row.astype(np.uint16) + 2 * saved_delta.astype(np.uint16)) % 3).astype(np.uint8)
    raw[5] = 2
    remainder, reductions = physical_reduce(pack(raw), pivots, rows, verbose=False)
    normalized, lead, scale = normalize_pivot(remainder, [2, 0])
    require([item["scalar"] for item in reductions] == [1, 2] and
            lead == 5 and scale == 2, "parent_plus_saved_delta_order")
    current_target = unpack(remainder, PHYSICAL_WIDTH)
    current_target[7] = 1
    target, scalar = update_target(pack(current_target), normalized, lead, [2, 0])
    separator, lam_raw = separator_after_append(
        pack(current_target), target, pivots, rows, normalized, lead, verbose=False)
    require(scalar == 2 and separator["direct_pairing"]["rows"] == 3 and
            separator["free_coordinate"] == 7, "one_new_target_step")
    functional = unpack(lam_raw, PHYSICAL_WIDTH)
    bad_row = old_row.copy()
    bad_row[7] = 1
    try:
        check_final_separator(functional, [pack(bad_row), *rows[1:], normalized],
                              pack(current_target), target, verbose=False)
    except RuntimeError as exc:
        require(str(exc).startswith("final_separator_nonzero_row:"), "bad_row_rejection_reason")
    else:
        raise RuntimeError("final_separator_bad_row_not_rejected")
    return {"status": "PASS", "synthetic_only": True, "verified": False,
            "cross_checked": False, "tests": [
                "selected-authority-seal", "parent-plus-delta-one-target-step",
                "final-lambda-bad-row-rejection"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    for name in ("scalar-root", "delta-root", "prepare-root", "p1-root",
                 "task712-root", "state-root", "output-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    try:
        if args.selftest:
            require(not args.block_root and all(getattr(args, name) is None for name in (
                "scalar_root", "delta_root", "prepare_root", "p1_root",
                "task712_root", "state_root", "output_root")),
                "selftest_without_actual_parents")
            summary = selftest()
        else:
            require(len(args.block_root) == 4 and all(getattr(args, name) is not None for name in (
                "scalar_root", "delta_root", "prepare_root", "p1_root",
                "task712_root", "state_root", "output_root")),
                "actual_fixed_parent_paths_required")
            summary = materialize(args)
        print(canonical(summary).decode("ascii"), end="", flush=True)
        return 0
    except Exception as exc:
        progress("terminal", status="REJECTED", reason=str(exc), error_type=type(exc).__name__)
        print(canonical({"status": "REJECTED", "reason": str(exc),
                         "verified": False, "cross_checked": False}).decode("ascii"),
              end="", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
