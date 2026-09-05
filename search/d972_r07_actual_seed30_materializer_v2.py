#!/usr/bin/env python3
"""Materialize the corrected actual R07 seed-30 violation as one state delta.

This producer is deliberately narrow.  It authenticates the fixed scalar,
Task554, P1, Task712, Task904-state, and Task640-rho2 parents; replays the
complete seed-30 subtraction; appends one normalized physical pivot; and
updates the already accepted rho2 remainder by exactly that pivot.  It never
rebuilds the old 8,059-offer connection/state history and never asserts an
eleven-slot A0 witness.
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
SCHEMA = "d972.r07.actual-seed30-materializer.v1"
SEED = 30
CHARACTER = 0
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
SEED30_SUPPORT = 902
ZERO_HEAD = "0" * 64
V541_FORMULA_ID = "r07.v541.formulas-2.1-2.2-4.1.raw-seed-plus-actor-lower-adjoint"

ROOT_V2_PATH = SEARCH / "d972_r07_actual_grade2_root_scalar_batch_v2.py"
ROOT_V2_SHA256 = "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856"
LEGACY_ARITH_PATH = SEARCH / "d972_r07_targeted_grade2_owner_generated_join_v15.py"
LEGACY_ARITH_SHA256 = "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"
SEPARATOR_V2_PATH = SEARCH / "d972_r07_grade2_physical_state_separator_v2.py"
SEPARATOR_V2_SHA256 = "b068c9f3be153c5381f583b4a82448d5680777ce71ccb5250c2bbb972c8cff2e"

SCALAR_FINAL_ARTIFACT = {
    "run": 33941591417, "attempt": 1,
    "head": "2caaf1f33b6f36f8aa754f759ef0e5dccfaf5a74",
    "source_commit": "a68460cf0c1bdae9fde5d3a4fa6501d625d68388",
    "id": 9962060495,
    "name": "d972-r07-actual-root-scalar-batch-v2-candidate-33941591417-1",
    "bytes": 253544,
    "sha256": "sha256:1091f9946108ef6bf122143da58d32006eba54166ee995996efa177aa89a2ed2",
}
SCALAR_DIAGNOSTIC_ARTIFACT = {
    "run": 33941591417, "attempt": 1,
    "head": "2caaf1f33b6f36f8aa754f759ef0e5dccfaf5a74",
    "id": 9962060193,
    "name": "d972-r07-actual-root-scalar-batch-v2-diagnostics-33941591417-1",
    "bytes": 266309,
    "sha256": "sha256:78f087944047f170162587c413fcb1202bb5796b8d4fdff19da73e6e2fd321cf",
}
SCALAR_FILE_PINS = {
    "output/manifest.json": (4447, "e9637fc60d0fd27df677960d941b365a7fa207c69c6519b6c3be7dc18c6696d0"),
    "output/result.json": (5147, "b62b2a65c5120cd9429a83750dbbc3d4e9a593e50f3bc41963b33ab979de6eaa"),
    "output/terminal.json": (1381, "8fea18c57a6a309b93f9b348b106ed2d3f3960d06d6707b9022214b420a354c2"),
    "output/character-a0.json": (16354, "cb8d8f75710628b7806f0d6f38ff7fcdda91c5b1ca55748aa86ea39631534557"),
    "output/q-a0-root.bin": (9072, "af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053"),
    "output/seed-scalars-a0.bin": (44, "7f9f54936ce6fe232429f8c1033056b67a5520c5f408e21c4c6b056d38a7f708"),
    "checker-result.json": (318, "e87942af848f399660b34e08839937109ac0c2612b75590370194260c166f732"),
}
SCALAR_LAUNCH_PIN = (10342, "16adebd65d741efd473017f7a75e4ba394ae2d0cc57733d721baba6ddcf9828a")
SCALAR_SOURCE_RECEIPT_PIN = (797, "b600ae44e66ec70eaf192525561e8b5f2927a6bcf32088c1c0dd853d0e73c54c")
VIOLATION_SHA256 = "cba44225c60f14e6203ea51a053f75a56b17e6cc33f146a9262609ac43c1c0f5"
CHARACTER_SHA256 = "afeb2bd9b3e0c0cbbb10d80a9ea0fe1ccaf90835cbab286ed28cef46e2cd4da1"
RAW_DUAL_SHA256 = "c19d8972ea9185628a3ae1f67d30da589cc7e47f5a707a0810e23c84ce244dd3"

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
STATE_LAMBDA_SHA256 = "7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed"
OLD_TARGET_REMAINDER_SHA256 = "e0053fc6e745e4459e0324d26320bf9f5e434a2942fa4a519ebaf9e28df50011"

RHO2_ARTIFACT = {
    "run": 33839962829, "attempt": 1,
    "head": "17a8439c766d92719d7ae7d35846ea444da598fa",
    "id": 9925190479, "name": "task640-fresh-rho2-v17-33839962829-1",
    "bytes": 6049643,
    "sha256": "sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4",
}
RHO2_SHA256 = "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"

P1_INSTRUCTION_KEYS = {
    "node", "origin", "reductions", "scale", "raw_origin_sha256",
    "raw_origin_components_sha256", "literal_input_sha256",
    "old_defect_literal_input_sha256", "parent_row_sha256", "packet_sha256",
    "packet_row_sha256", "reduction_parent_sha256", "p1_sha256", "offset",
    "length", "row_receipt", "predecessor", "ancestry_sha256",
}

CLAIMS = {
    "ACTUAL_SEED30_MATERIALIZATION_CANDIDATE": True,
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


def dependencies() -> tuple[ModuleType, ModuleType]:
    # Root-v2 imports the legacy arithmetic module while executing.  Pin it
    # before that import edge can run.
    file_sha(LEGACY_ARITH_PATH, expected_sha=LEGACY_ARITH_SHA256, cap=1 << 28)
    if str(SEARCH) not in sys.path:
        sys.path.insert(0, str(SEARCH))
    root_v2 = load_pinned_module("task927_root_v2", ROOT_V2_PATH, ROOT_V2_SHA256)
    separator_v2 = load_pinned_module(
        "task927_separator_v2", SEPARATOR_V2_PATH, SEPARATOR_V2_SHA256)
    root_v2.verify_source_pin()
    return root_v2, separator_v2


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


def _source_receipt_expected() -> dict[str, Any]:
    return {
        "schema": "d972.r07.actual-root-scalar-batch.source-receipt.v2",
        "candidate": True,
        "files": [
            {"path": "search/d972_r07_actual_grade2_root_scalar_batch_v2.py",
             "bytes": 118315, "lf": 2106, "sha256": ROOT_V2_SHA256},
            {"path": "search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py",
             "bytes": 119619, "lf": 1968,
             "sha256": "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6"},
            {"path": "search/d972_r07_targeted_grade2_owner_generated_join_v15.py",
             "bytes": 126565, "lf": 2286, "sha256": LEGACY_ARITH_SHA256},
            {"path": "search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py",
             "bytes": 141770, "lf": 2500,
             "sha256": "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"},
        ],
        "verified": False,
    }


def validate_scalar_parent(candidate_root: Path, diagnostic_root: Path
                           ) -> dict[str, Any]:
    progress("parent-loading", parent="corrected-root-v2")
    candidate_root = candidate_root.resolve()
    diagnostic_root = diagnostic_root.resolve()
    require(candidate_root.is_dir() and diagnostic_root.is_dir(), "scalar_parent_roots")
    launch, launch_raw = read_json_exact(
        safe_file(diagnostic_root, "launch.json"), *SCALAR_LAUNCH_PIN, 1 << 24)
    source_receipt, source_raw = read_json_exact(
        safe_file(diagnostic_root, "receipts/source-receipt.json"),
        *SCALAR_SOURCE_RECEIPT_PIN, 1 << 20)
    require(source_receipt == _source_receipt_expected(), "scalar_source_receipt")
    manifest, manifest_raw = read_json_exact(
        safe_file(candidate_root, "output/manifest.json"),
        *SCALAR_FILE_PINS["output/manifest.json"], 1 << 20)
    result, result_raw = read_json_exact(
        safe_file(candidate_root, "output/result.json"),
        *SCALAR_FILE_PINS["output/result.json"], 1 << 20)
    terminal, terminal_raw = read_json_exact(
        safe_file(candidate_root, "output/terminal.json"),
        *SCALAR_FILE_PINS["output/terminal.json"], 1 << 20)
    character, character_raw = read_json_exact(
        safe_file(candidate_root, "output/character-a0.json"),
        *SCALAR_FILE_PINS["output/character-a0.json"], 1 << 20)
    checker, checker_raw = read_json_exact(
        safe_file(candidate_root, "checker-result.json"),
        *SCALAR_FILE_PINS["checker-result.json"], 1 << 20,
        canonical_required=False)
    require(all(sealed_ok(value) for value in (manifest, result, terminal, character)),
            "scalar_embedded_seals")
    output_root = candidate_root / "output"
    require(set(manifest.get("file_roster", [])) ==
            {path.name for path in output_root.iterdir() if path.is_file()},
            "scalar_output_roster")
    listed = manifest.get("files")
    require(isinstance(listed, list), "scalar_file_receipts")
    for item in listed:
        require(isinstance(item, dict) and set(item) == {"file", "bytes", "sha256"},
                "scalar_file_receipt_shape")
        file_sha(safe_file(output_root, item["file"]), item["bytes"], item["sha256"],
                 1 << 24)
    require(launch.get("schema") ==
            "d972.r07.actual-grade2.root-scalar-batch.v2.launch.v1" and
            launch.get("fixture_only") is False and launch.get("mode") == "actual" and
            result.get("launch_sha256") == sha(launch_raw) and
            result.get("sha256") == "74b11bb6f8b82e669066f028fa1e68ba0100a451e945cb306db5174a4ab16e70" and
            terminal.get("sha256") == "12f4851543837b2b6b72ef69c19a32213099df786a823b0d6db5cec76864b54e" and
            character.get("sha256") == CHARACTER_SHA256,
            "scalar_launch_result_join")
    violation = character.get("scalar")
    require(character.get("schema", "").endswith("RootViolation") and
            character.get("character") == CHARACTER and
            character.get("v541_formula_id") == V541_FORMULA_ID and
            isinstance(violation, dict) and sealed_ok(violation) and
            violation.get("sha256") == VIOLATION_SHA256 and
            violation.get("character") == CHARACTER and
            violation.get("origin_id") == SEED and
            violation.get("origin_kind") == "seed" and
            violation.get("seed") == SEED and violation.get("scalar") == 1 and
            violation.get("raw_dual_sha256") == RAW_DUAL_SHA256 and
            character.get("raw_dual", {}).get("word_node", {}).get("actors") == [] and
            character.get("raw_dual", {}).get("sha256") == RAW_DUAL_SHA256,
            "scalar_violation_pin")
    q_raw = read_exact(safe_file(candidate_root, "output/q-a0-root.bin"),
                       *SCALAR_FILE_PINS["output/q-a0-root.bin"], 1 << 20)
    seed_scalars = read_exact(safe_file(candidate_root, "output/seed-scalars-a0.bin"),
                              *SCALAR_FILE_PINS["output/seed-scalars-a0.bin"], 1 << 20)
    require(seed_scalars[2] == 0 and seed_scalars[SEED] == 1 and
            checker == {"cache_passes": 1, "complete_dual_orbits": False,
                        "future_orbit_rows_executed": 0,
                        "relation_origin_declared_count": 32280,
                        "root_characters": 4, "rows": 8059, "status": "PASS",
                        "terminal": "RootViolationBatch",
                        "v541_formula_id": V541_FORMULA_ID, "verified": False},
            "scalar_saved_values_or_checker")
    return {"launch": launch, "launch_sha256": sha(launch_raw),
            "launch_receipt": receipt("launch.json", launch_raw),
            "source_receipt": receipt("source-receipt.json", source_raw),
            "manifest_sha256": sha(manifest_raw), "result_sha256": sha(result_raw),
            "terminal_sha256": sha(terminal_raw), "character_sha256": sha(character_raw),
            "checker_sha256": sha(checker_raw), "character": character,
            "violation": violation, "q": unpack(q_raw, SOURCE2C),
            "q_receipt": receipt("q-a0-root.bin", q_raw),
            "seed_scalars_receipt": receipt("seed-scalars-a0.bin", seed_scalars)}


def _runtime_parent(descriptor: dict[str, Any], root: Path) -> dict[str, Any]:
    value = copy.deepcopy(descriptor)
    value["root"] = str(root.resolve())
    return value


def collect_seedred30(root_v2: ModuleType, launch: dict[str, Any],
                      prepare_root: Path, block_roots: list[Path]
                      ) -> dict[str, Any]:
    progress("parent-loading", parent="task554", bodies=5)
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
                "origin_id": origin_id, "term_ordinal": ordinal,
                "local_index": local_index, "global_index": global_index,
                "coefficient": coefficient,
            }
            raw_events.append(event)

    prepare = root_v2._state_descriptor(parent["prepare"], -1, need_blobs=True)
    for source, old in enumerate(prepare["body"]["old_blocks"]):
        append_expression(
            old["record"]["seed_reductions"][SEED], body_role="prepare-old",
            body_sha256=prepare["body_sha256"], source=source, target=None,
            origin_id=ORIGIN_RANGES[source][0] + SEED,
            global_offset=OLD_OFFSETS[source])
        segments.append({
            "kind": "old", "owner": source, "start": OLD_OFFSETS[source],
            "rows": OLD_RANKS[source], "root": prepare["root"],
            "body_sha256": prepare["body_sha256"],
            "lower_descriptor": copy.deepcopy(old["lower_basis_blob"]),
            "grade_descriptor": copy.deepcopy(old["lifted_grade_blob"]),
        })
    del prepare

    for target in range(4):
        block = root_v2._state_descriptor(parent["blocks"][target], target,
                                          need_blobs=True)
        body = block["body"]
        for source in range(4):
            origin_id = ORIGIN_RANGES[source][0] + SEED
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
    # Seal the ordered nonabelian ancestry before collecting F3 coefficients.
    for event in sealed_events:
        node = event["global_index"]
        coefficients[node] = (int(coefficients[node]) + event["coefficient"]) % 3
    final_coefficients = [[int(node), int(coefficients[node])]
                          for node in np.flatnonzero(coefficients)]
    require(len(final_coefficients) == SEED30_SUPPORT and
            all(value in (1, 2) for _, value in final_coefficients),
            "actual_seed30_support")
    return {
        "parent": parent, "raw_events": sealed_events,
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


def load_task712(root_v2: ModuleType, launch: dict[str, Any], task712_root: Path
                 ) -> dict[str, Any]:
    progress("parent-loading", parent="task712", character=CHARACTER)
    parents = launch.get("task712_parents")
    require(isinstance(parents, list) and len(parents) == 4 and
            all({key: item[key] for key in root_v2.TASK712_PARENT} ==
                root_v2.TASK712_PARENT for item in parents), "task712_parent_list")
    descriptor = _runtime_parent(parents[CHARACTER], task712_root)
    tables = root_v2.ARITH.read_task712_envelope(descriptor, CHARACTER)
    for key in ("B", *root_v2.ACTORS):
        root_v2.check_table_transpose(tables["forward"][key], tables["adjoint"][key])
    require(tables["identity"]["forward:B"] ==
            "B_fwd_a0.jsonl:763affaa7be5dea7a1d432fa5cf43e65177abb1b9fb4935dc4b2e5c37cb5fd67",
            "task712_B_fwd_a0_pin")
    return {"descriptor": descriptor, "tables": tables,
            "manifest_sha256": tables["manifest_sha256"]}


def replay_seed30(root_v2: ModuleType, seedred: dict[str, Any],
                  lower: dict[str, Any], p1: dict[str, Any],
                  task712: dict[str, Any], q: np.ndarray) -> dict[str, Any]:
    progress("raw-seed-evaluation", seed=SEED, character=CHARACTER)
    context, words = root_v2.source_context()
    relator = tuple(int(value) for value in words["relators"][SEED])
    raw_parts = root_v2.ARITH._seed_evaluate_seed(context, relator)
    d0, d1, d2, auxiliary = tuple(
        np.asarray(part, dtype=np.uint8).copy() for part in raw_parts)
    require(d0.shape == (4, SOURCE0C) and d1.shape == (4, SOURCE1C) and
            d2.shape == (4, SOURCE2C) and auxiliary.shape == (8,),
            "raw_seed_component_shapes")
    raw_receipt = sealed(SCHEMA + ".raw-seed", {
        "seed": SEED, "character": CHARACTER,
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
    require(total_selected == SEED30_SUPPORT, "seed30_selected_count")
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
            "complete_seed30_lower_zero")
    reduced_components = [
        component_receipt("d0", d0), component_receipt("d1", d1),
        component_receipt("d2", d2), component_receipt("aux", auxiliary),
    ]
    projected = root_v2.ARITH._seed_full_project(
        context, (d0, d1, d2, auxiliary), CHARACTERS[CHARACTER])
    projected = tuple(np.asarray(part, dtype=np.uint8) for part in projected)
    require(not np.any(projected[0]) and not np.any(projected[1]) and
            not np.any(projected[3]) and
            np.array_equal(projected[2][CHARACTER], d2[CHARACTER]) and
            all(not np.any(projected[2][index]) for index in range(1, 4)),
            "complete_lower_zero_projector_match")
    source = d2[CHARACTER].copy()
    tables = task712["tables"]
    physical = apply_sparse(tables["forward"]["B"], SOURCE2C,
                            PHYSICAL_WIDTH, source)
    q_pair = dot(q, source)
    require(q_pair == 1, "q_dot_seed30_source")
    subtraction = sealed(SCHEMA + ".complete-subtraction", {
        "formula_id": V541_FORMULA_ID,
        "seed": SEED, "character": CHARACTER,
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
        "plain_character0_source_sha256": sha(pack(source)),
        "full_projector_character0_source_sha256": sha(pack(projected[2][0])),
        "full_projector_other_character_nonzero_count": 0,
        "full_projector_applied_to_complete_defect": True,
    })
    projector_factors = []
    for label in CHARACTERS:
        sign = int(root_v2.ARITH._seed_cv(CHARACTERS[CHARACTER], label))
        require(sign == 1, "character0_projector_sign")
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
            "seed_factor": {"seed": SEED, "exponent": 1,
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
            "character": list(CHARACTERS[CHARACTER]),
            "order": [list(label) for label in CHARACTERS],
            "factors": projector_factors,
        },
        "actor_path": [],
        "forward_B": tables["identity"]["forward:B"],
        "six_source_tag_replay": True,
        "eleven_slot_replay": False,
        "full_A0_witness": False,
    })
    ancestry = sealed(SCHEMA + ".seed30-ancestry", {
        "seed": SEED, "character": CHARACTER,
        "task554_body_sha256": seedred["body_sha256"],
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


def validate_state_parent(separator_v2: ModuleType, state_root: Path
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
    lambda_raw = read_exact(safe_file(root, "output/lambda.bin"),
                            PHYSICAL_BYTES, STATE_LAMBDA_SHA256, 1 << 20)
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
    try:
        old_remainder = bytes.fromhex(target["remainder"])
    except ValueError as exc:
        raise RuntimeError("old_target_remainder_hex") from exc
    validate_packed(old_remainder, PHYSICAL_WIDTH)
    require(sha(old_remainder) == target.get("remainder_sha256") ==
            OLD_TARGET_REMAINDER_SHA256, "old_target_remainder_receipt")
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
    with instruction_path.open("rb") as stream:
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
    require(all(int(DIGITS[old_remainder[lead // 4], lead % 4]) == 0
                for lead in leads), "old_target_earlier_zero")
    require(target.get("target_parent_manifest_sha256") ==
            separator_v2.RHO2_MANIFEST["sha256"], "old_target_parent_join")
    return {
        "root": root, "manifest": state_manifest,
        "manifest_sha256": sha(state_manifest_raw), "records": pivots,
        "packed_rows": packed_rows, "leads": leads,
        "lambda": unpack(lambda_raw, PHYSICAL_WIDTH),
        "lambda_receipt": receipt("lambda.bin", lambda_raw),
        "target": target, "target_sha256": sha(canonical(target)),
        "old_remainder": old_remainder,
        "result_sha256": sha(state_result_raw),
        "terminal_sha256": sha(state_terminal_raw),
        "checker_sha256": sha(checker_raw),
        "nonmonotone_transitions": sum(
            1 for left, right in zip(leads, leads[1:]) if right < left),
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


def separator_after_append(target_raw: bytes, remainder_raw: bytes,
                           pivots: list[dict[str, Any]], rows: list[bytes],
                           normalized: bytes, lead: int, *, verbose: bool = True
                           ) -> tuple[dict[str, Any], bytes]:
    free = first_nonzero(remainder_raw, PHYSICAL_WIDTH)
    require(free is not None and free[0] not in {item["lead"] for item in pivots} | {lead},
            "next_separator_free_coordinate")
    functional = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    functional[free[0]] = free[1]  # Inverse of a nonzero F3 element is itself.
    all_pivots = [*pivots, {"offer": STATE_GENERATION, "lead": lead}]
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
    # The accepted parent insertion-triangularity and the newly checked earlier
    # zeros imply that later reverse equations remain true.  No Conn replay.
    require(dot(functional, unpack(target_raw, PHYSICAL_WIDTH)) == 1 and
            dot(functional, unpack(normalized, PHYSICAL_WIDTH)) == 0 and
            dot(functional, unpack(remainder_raw, PHYSICAL_WIDTH)) == 1,
            "next_separator_target_pairing")
    packed_lambda = pack(functional)
    return {
        "free_coordinate": free[0], "free_value": free[1],
        "transcript": transcript, "lambda_sha256": sha(packed_lambda),
        "lambda_rho2": 1, "lambda_physical_pivots": 0,
    }, packed_lambda


def join_parents(root_v2: ModuleType, scalar: dict[str, Any],
                 seedred: dict[str, Any], p1: dict[str, Any],
                 task712: dict[str, Any], state: dict[str, Any],
                 rho2_manifest: dict[str, Any]) -> dict[str, Any]:
    launch = scalar["launch"]
    separator = launch["separator_parent"]
    source_state = state["manifest"]
    require(separator["manifest"]["sha256"] == STATE_MANIFEST_SHA256 and
            separator["physical"]["sha256"] == STATE_PHYSICAL_SHA256 and
            separator["lambda"]["sha256"] == STATE_LAMBDA_SHA256 and
            separator["internal"]["result"]["sha256"] == state["result_sha256"] and
            separator["internal"]["terminal"]["sha256"] == state["terminal_sha256"] and
            separator["internal"]["checker"]["sha256"] == state["checker_sha256"],
            "scalar_to_actual_state_join")
    require(all(str(separator["artifact"][key]) == str(STATE_ARTIFACT[key])
                for key in STATE_ARTIFACT), "scalar_state_artifact_join")
    require(source_state["p1_identity"]["manifest_sha256"] ==
            p1["receipt"]["manifest_sha256"] and
            source_state["p1_identity"]["cache_sha256"] == p1["receipt"]["cache_sha256"] and
            source_state["p1_identity"]["instruction"]["sha256"] ==
            p1["receipt"]["instruction_sha256"] and
            source_state["source_ancestry"]["prepare_body_sha256"] ==
            seedred["body_sha256"][0] and
            source_state["source_ancestry"]["parents"] == seedred["body_sha256"][1:] and
            source_state["task712"]["tables"]["manifest_sha256"] ==
            task712["manifest_sha256"], "state_source_parent_joins")
    require(sha(canonical(rho2_manifest)) ==
            state["target"]["target_parent_manifest_sha256"] and
            rho2_manifest["rho2"]["packed_sha256"] == RHO2_SHA256,
            "state_rho2_parent_join")
    return {
        "scalar": {
            "final_artifact": SCALAR_FINAL_ARTIFACT,
            "diagnostic_artifact": SCALAR_DIAGNOSTIC_ARTIFACT,
            "launch": scalar["launch_receipt"], "source": scalar["source_receipt"],
            **{key: scalar[key] for key in (
                "manifest_sha256", "result_sha256", "terminal_sha256",
                "character_sha256", "checker_sha256")},
            "violation_sha256": VIOLATION_SHA256,
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
        "state": {
            "artifact": STATE_ARTIFACT, "manifest_sha256": STATE_MANIFEST_SHA256,
            "head": STATE_HEAD, "generation": STATE_GENERATION, "rank": STATE_RANK,
            "physical_sha256": STATE_PHYSICAL_SHA256,
            "companion_sha256": STATE_COMPANION_SHA256,
            "instruction_sha256": STATE_INSTRUCTION_SHA256,
            "checker_sha256": state["checker_sha256"],
            "result_sha256": state["result_sha256"],
            "target_sha256": state["target_sha256"],
            "old_derivation_accepted_as_premise": True,
        },
        "rho2": {"artifact": RHO2_ARTIFACT,
                 "manifest_sha256": sha(canonical(rho2_manifest)),
                 "packed_sha256": RHO2_SHA256},
        "source_modules": {
            ROOT_V2_PATH.name: ROOT_V2_SHA256,
            LEGACY_ARITH_PATH.name: LEGACY_ARITH_SHA256,
            SEPARATOR_V2_PATH.name: SEPARATOR_V2_SHA256,
        },
    }


def materialize(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    output_root = args.output_root.absolute()
    require(not output_root.exists() and not output_root.is_symlink(), "fresh_output_root")
    parent_roots = [args.scalar_root, args.scalar_diagnostics_root, args.prepare_root,
                    *args.block_root, args.p1_root, args.task712_root,
                    args.state_root, args.rho2_root]
    for parent in parent_roots:
        require(parent.is_dir() and parent.resolve() != output_root.resolve() and
                parent.resolve() not in output_root.resolve().parents and
                output_root.resolve() not in parent.resolve().parents,
                "output_disjoint_from_parents")
    progress("parent-loading", parent="source-modules")
    root_v2, separator_v2 = dependencies()
    scalar = validate_scalar_parent(args.scalar_root, args.scalar_diagnostics_root)
    state = validate_state_parent(separator_v2, args.state_root)
    seedred = collect_seedred30(root_v2, scalar["launch"], args.prepare_root,
                                args.block_root)
    lower = load_selected_lower(seedred)
    arithmetic_nodes = {node for node, _ in seedred["final_coefficients"]}
    reference_nodes = {item["global_index"] for item in seedred["raw_events"]}
    p1 = load_selected_p1(root_v2, scalar["launch"], args.p1_root,
                          reference_nodes, arithmetic_nodes)
    task712 = load_task712(root_v2, scalar["launch"], args.task712_root)
    progress("parent-loading", parent="task640-rho2")
    rho2_packed, rho2_manifest = separator_v2._read_target_parent(
        args.rho2_root.resolve(), live_parent=True)
    rho2_raw = rho2_packed.tobytes()
    require(sha(rho2_raw) == RHO2_SHA256, "actual_rho2_bytes")
    parents = join_parents(root_v2, scalar, seedred, p1, task712, state, rho2_manifest)
    replay = replay_seed30(root_v2, seedred, lower, p1, task712, scalar["q"])
    forward = task712["tables"]["forward"]["B"]
    pulled = apply_sparse(([dst, src, coefficient] for src, dst, coefficient in forward),
                          PHYSICAL_WIDTH, SOURCE2C, state["lambda"])
    require(np.array_equal(pulled, scalar["q"]) and
            dot(state["lambda"], replay["physical"]) == replay["q_pair"] == 1,
            "joined_actual_q_and_physical_pairings")
    raw_physical = pack(replay["physical"])
    raw_source = pack(replay["source"])
    raw_materialization = sealed(SCHEMA + ".raw-materialization", {
        "violation_sha256": VIOLATION_SHA256,
        "raw_dual_sha256": RAW_DUAL_SHA256,
        "lambda_sha256": STATE_LAMBDA_SHA256,
        "raw_q_sha256": scalar["q_receipt"]["sha256"],
        "raw_seed_sha256": replay["raw_seed"]["sha256"],
        "source_ancestry_sha256": replay["ancestry"]["sha256"],
        "lower_zero_receipt_sha256": replay["subtraction"]["sha256"],
        "raw_word_sha256": replay["literal_word_dag"]["sha256"],
        "raw_source_sha256": sha(raw_source), "raw_physical_sha256": sha(raw_physical),
        "forward_B": task712["tables"]["identity"]["forward:B"],
        "actor_path": [], "q_d": 1, "lambda_G": 1,
    })
    progress("physical-reduction", pivots=0, total=STATE_RANK)
    remainder, reductions = physical_reduce(raw_physical, state["records"],
                                            state["packed_rows"])
    normalized, lead, scale = normalize_pivot(remainder, state["leads"])
    require(dot(state["lambda"], unpack(remainder, PHYSICAL_WIDTH)) == 1 and
            dot(state["lambda"], unpack(normalized, PHYSICAL_WIDTH)) == scale,
            "raw_remainder_normalized_pairings")
    normalized_word = sealed(SCHEMA + ".normalized-word-dag", {
        "v518_formula": "4.3", "raw_word_sha256": replay["literal_word_dag"]["sha256"],
        "operation": "ordered-product-then-scale",
        "parent_state_head": STATE_HEAD, "parent_state_manifest_sha256": STATE_MANIFEST_SHA256,
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
        "offer": STATE_GENERATION, "generation": STATE_GENERATION + 1,
        "predecessor": STATE_HEAD, "parent_state": parents["state"],
        "raw_materialization_sha256": raw_materialization["sha256"],
        "source_ancestry_sha256": replay["ancestry"]["sha256"],
        "normalized_word_sha256": normalized_word["sha256"],
        "top": receipt("physical-raw.bin", raw_physical),
        "remainder": receipt("physical-remainder.bin", remainder),
        "physical": receipt("physical-normalized.bin", normalized),
        "reductions": reductions, "lead": lead, "sigma": scale,
        "lower_zero": True, "physical_zero": False, "rank": STATE_RANK + 1,
        "physical_offset": STATE_RANK * PHYSICAL_BYTES, "delta_physical_offset": 0,
        "coefficient_offset": None, "coefficient_representation": "parent-literal-DAG",
    }
    instruction, new_head, instruction_raw = separator_v2._record_state_instruction(
        instruction_body, STATE_HEAD)
    require(new_head == sha(bytes.fromhex(STATE_HEAD) + canonical(instruction_body)) and
            instruction_raw == canonical(instruction), "new_instruction_rolling")
    pivot = sealed(SCHEMA + ".physical-pivot", {
        "raw_materialization_sha256": raw_materialization["sha256"],
        "offer": STATE_GENERATION, "pivot_id": STATE_RANK,
        "lead": lead, "scale": scale,
        "rank_before": STATE_RANK, "rank_after": STATE_RANK + 1,
        "generation_before": STATE_GENERATION, "generation_after": STATE_GENERATION + 1,
        "head_before": STATE_HEAD, "head_after": new_head,
        "instruction_sha256": sha(instruction_raw), "reductions": reductions,
        "raw_sha256": sha(raw_physical), "remainder_sha256": sha(remainder),
        "normalized_sha256": sha(normalized), "earlier_pivot_zero_count": STATE_RANK,
        "lambda_raw": 1, "lambda_remainder": 1, "lambda_normalized": scale,
        "literal_word_dag": normalized_word,
    })
    progress("target-append", parent_reductions=884, new_pivots=1,
             rank_before=STATE_RANK, rank_after=STATE_RANK + 1)
    target_raw, target_scalar = update_target(state["old_remainder"], normalized,
                                               lead, state["leads"])
    kind = "Separator" if first_nonzero(target_raw, PHYSICAL_WIDTH) else "ConnectionMemberCandidate"
    target_update = sealed(SCHEMA + ".target-update", {
        "parent_target_sha256": state["target_sha256"],
        "parent_result_sha256": state["result_sha256"],
        "old_remainder_sha256": OLD_TARGET_REMAINDER_SHA256,
        "old_reduction_count": 884, "rho2_sha256": RHO2_SHA256,
        "state_head": new_head, "state_rank": STATE_RANK + 1,
        "scalar": target_scalar, "new_pivots_examined": 1,
        "new_reductions": ([{
            "pivot_id": STATE_RANK, "offer": STATE_GENERATION,
            "lead": lead, "scalar": target_scalar,
            "physical_offset": STATE_RANK * PHYSICAL_BYTES, "row_sha256": sha(normalized),
        }] if target_scalar else []),
        "remainder_sha256": sha(target_raw), "kind": kind,
        "old_target_history_copied": False,
    })
    next_separator = None
    next_lambda = None
    if kind == "Separator":
        next_separator, next_lambda = separator_after_append(
            rho2_raw, target_raw, state["records"], state["packed_rows"], normalized, lead)
    result = sealed(SCHEMA + ".result", {
        "status": "PASS", "kind": kind, "candidate": True,
        "verified": False, "cross_checked": False, "claims": CLAIMS,
        "parents": parents, "raw_seed": replay["raw_seed"],
        "subtraction": replay["subtraction"], "ancestry": replay["ancestry"],
        "raw_materialization": raw_materialization,
        "pairings": {"q_d": 1, "lambda_G": 1, "B_adjoint_q_equal": True},
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
        "parent_state_manifest_sha256": STATE_MANIFEST_SHA256,
        "parent_state_head": STATE_HEAD, "state_head": new_head,
        "rank_before": STATE_RANK, "rank_after": STATE_RANK + 1,
        "result_sha256": sha(canonical(result)), "terminal": kind,
        "parent_state_copied": False,
    })
    manifest_receipt = atomic_json(output_root, "manifest.json", manifest)
    progress("terminal", kind=kind, rank=STATE_RANK + 1,
             elapsed_seconds=round(time.monotonic() - started, 3))
    return {"status": "PASS", "kind": kind, "rank_before": STATE_RANK,
            "rank_after": STATE_RANK + 1, "manifest_sha256": manifest_receipt["sha256"],
            "verified": False, "cross_checked": False}


def selftest() -> dict[str, Any]:
    """Bounded synthetic canaries only, without loading historical parents."""
    small = np.asarray([0, 1, 2, 2, 0, 1, 0, 2, 1], dtype=np.uint8)
    require(np.array_equal(unpack(pack(small), len(small)), small), "selftest_pack")
    old0 = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    old1 = old0.copy()
    old0[[2, 4]] = 1
    old1[[0, 3]] = 1
    rows = [pack(old0), pack(old1)]
    pivots = [{"offer": 0, "lead": 2, "physical_offset": 0},
              {"offer": 1, "lead": 0, "physical_offset": PHYSICAL_BYTES}]
    raw = ((2 * old0.astype(np.uint16) + old1.astype(np.uint16)) % 3).astype(np.uint8)
    raw[5] = 2
    remainder, reductions = physical_reduce(pack(raw), pivots, rows, verbose=False)
    normalized, lead, scale = normalize_pivot(remainder, [2, 0])
    require(lead == 5 and scale == 2 and [item["scalar"] for item in reductions] == [2, 1]
            and remainder != normalized and np.count_nonzero(unpack(normalized, PHYSICAL_WIDTH)) == 1,
            "selftest_nonmonotone_and_raw_normalized")
    old_target = unpack(remainder, PHYSICAL_WIDTH)
    old_target[7] = 1
    next_raw, scalar = update_target(pack(old_target), normalized, lead, [2, 0])
    require(scalar == 2 and first_nonzero(next_raw, PHYSICAL_WIDTH) == (7, 1),
            "selftest_target_one_step")
    target = ((old_target.astype(np.uint16) + old0.astype(np.uint16)) % 3).astype(np.uint8)
    separator, packed_lambda = separator_after_append(
        pack(target), next_raw, pivots, rows, normalized, lead, verbose=False)
    lam = unpack(packed_lambda, PHYSICAL_WIDTH)
    require(separator["free_coordinate"] == 7 and dot(lam, target) == 1 and
            all(dot(lam, row) == 0 for row in (old0, old1)), "selftest_separator")
    zero, _ = update_target(remainder, normalized, lead, [2, 0])
    require(first_nonzero(zero, PHYSICAL_WIDTH) is None, "selftest_member_candidate")
    for invalid, test in ((bytes([81]), lambda data: unpack(data, 4)),
                          (bytes(PHYSICAL_BYTES), lambda data: normalize_pivot(data, [2, 0]))):
        try:
            test(invalid)
        except RuntimeError:
            continue
        raise RuntimeError("selftest_rejection_missing")
    ordered = [{"node": 3, "coefficient": 1}, {"node": 3, "coefficient": 2}]
    rolling = ZERO_HEAD
    for event in ordered:
        rolling = sha(bytes.fromhex(rolling) + canonical(event))
    require(sum(item["coefficient"] for item in ordered) % 3 == 0 and
            rolling != ZERO_HEAD, "selftest_raw_order_before_cancellation")
    parent = sealed("synthetic-parent", {"head": STATE_HEAD, "rank": STATE_RANK})
    mutated = {**parent, "rank": STATE_RANK + 1}
    require(sealed_ok(parent) and not sealed_ok(mutated), "selftest_parent_mutation")
    # The accepted P1 ABI stores LOCAL reduction indices, and permits nullable
    # raw metadata.  A nonzero block base distinguishes the old reader bug.
    p1_row = bytes(P1_ROW_BYTES)
    parent_rows = ["a" * 64] * 506
    parent_rows[0] = "b" * 64
    p1_record: dict[str, Any] = {key: None for key in P1_INSTRUCTION_KEYS}
    p1_record.update({
        "node": 506, "origin": {"kind": "actor", "parent": 0, "letter": 1},
        "reductions": [[0, 1]], "scale": 1, "raw_origin_sha256": "c" * 64,
        "raw_origin_components_sha256": {"p0": "d" * 64},
        "parent_row_sha256": [], "reduction_parent_sha256": [parent_rows[505]],
        "p1_sha256": "e" * 64, "offset": 506 * P1_ROW_BYTES, "length": P1_ROW_BYTES,
        "row_receipt": {"offset": 506 * P1_ROW_BYTES, "length": P1_ROW_BYTES,
                        "sha256": sha(p1_row)}, "predecessor": ZERO_HEAD,
    })
    p1_record["ancestry_sha256"] = sha(bytes.fromhex(ZERO_HEAD) + canonical(
        {key: value for key, value in p1_record.items() if key != "ancestry_sha256"}))
    require(validate_p1_instruction(p1_record, 506, canonical(p1_record), p1_row,
                                    ZERO_HEAD, [], parent_rows) == p1_record["ancestry_sha256"],
            "selftest_p1_local_base_and_nullable_metadata")
    return {"status": "PASS", "synthetic_only": True, "verified": False,
            "cross_checked": False,
            "tests": ["packed-roundtrip-and-rejection", "nonmonotone-insertion",
                      "raw-versus-normalized", "target-one-step", "next-separator",
                      "membership-candidate-only", "zero-pivot-rejection",
                      "ordered-raw-cancellation", "parent-mutation",
                      "p1-local-base-and-nullable-metadata"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    for name in ("scalar-root", "scalar-diagnostics-root", "prepare-root", "p1-root",
                 "task712-root", "state-root", "rho2-root", "output-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    try:
        if args.selftest:
            require(not args.block_root and all(getattr(args, name) is None for name in (
                "scalar_root", "scalar_diagnostics_root", "prepare_root", "p1_root",
                "task712_root", "state_root", "rho2_root", "output_root")),
                "selftest_without_actual_parents")
            summary = selftest()
        else:
            require(len(args.block_root) == 4 and all(getattr(args, name) is not None for name in (
                "scalar_root", "scalar_diagnostics_root", "prepare_root", "p1_root",
                "task712_root", "state_root", "rho2_root", "output_root")),
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
