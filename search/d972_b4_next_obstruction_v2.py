#!/usr/bin/env python3
"""Literal-A.18 producer with an explicit recursive dependency closure.

The audited v1 producer remains the mathematical implementation.  This
version is a fail-closed execution wrapper: every repository Python file that
can be reached by the v1 dynamic imports is hashed before v1 is imported, and
the same closure is copied into every lossless shard/merge receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]

PARENT_PRODUCER = ROOT / "search" / "d972_b4_next_obstruction_v1.py"
PARENT_CHECKER = ROOT / "search" / "check_d972_b4_next_obstruction_v1.py"
BASE_PRODUCER = ROOT / "search" / "d972_b4_magnus_ideal_v1.py"
CORE_SHARD = ROOT / "search" / "d972_b4_magnus_ideal_shard_v2.py"
CORE_MERGE = ROOT / "search" / "d972_b4_magnus_ideal_merge_v3.py"
CORE_BASE_MERGE = ROOT / "search" / "d972_b4_magnus_ideal_merge_v2.py"
INPUT_PATH = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
WORDS_PATH = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"

PARENT_PRODUCER_SHA = "bbf91f461e0c0d9d67ea49186450e709fcb97025ac4ebc3462b3dc6c278eb886"
PARENT_CHECKER_SHA = "2cd42ed369d9bb946f474cc6c10d90aaa4a32ab53e299c190763749a07660994"
BASE_PRODUCER_SHA = "b2e5184e31e177dcf5bfdc9fcd715e2146db877e0eccda2056cc5d7f999ae6bc"
CORE_SHARD_SHA = "1a18994e3933d5d42e85274af62badb89c2f9a65c92c63862d1740ac2d47da63"
CORE_MERGE_SHA = "6ccce4e95378dfa22051bd8c09e3d3aa5a91234b8d155c0fb57fd18c34f24bf5"
CORE_BASE_MERGE_SHA = "c79abb6ff51bccaaf98992fa070fecf3aba9d70ea4f6b6deff90d4cfcef1814c"
INPUT_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"

TRACKED_PARENT_COMMIT = "0e0b0b0855f3c42c00c614b863ff0e14368734da"
SCHEMA = "d972-b4-next-obstruction/v2"
DEPENDENCY_SCHEMA = "d972-b4-literal-a18-dependency-closure/v2"
FINAL_MARKER = "D972_B4_NEXT_OBSTRUCTION_V2_FINAL"
SELFTEST_MARKER = "D972_B4_NEXT_OBSTRUCTION_V2_DEPENDENCY_SELFTEST_PASS"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"),
                      sort_keys=True).encode("ascii")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _file(role: str, path: Path, digest: str, state: str) -> dict[str, object]:
    return {"role": role, "path": rel(path), "sha256": digest, "state": state}


def dependency_closure() -> dict[str, object]:
    """The complete local file closure, including the transitive base import."""
    return {
        "schema": DEPENDENCY_SCHEMA,
        "tracked_parent_commit": TRACKED_PARENT_COMMIT,
        "files": [
            _file("parent_producer", PARENT_PRODUCER, PARENT_PRODUCER_SHA,
                  "tracked_at_parent_commit"),
            _file("parent_checker", PARENT_CHECKER, PARENT_CHECKER_SHA,
                  "tracked_at_parent_commit"),
            _file("magnus_shard_core", CORE_SHARD, CORE_SHARD_SHA,
                  "tracked_at_parent_commit"),
            _file("magnus_stream_merge_core", CORE_MERGE, CORE_MERGE_SHA,
                  "tracked_at_parent_commit"),
            _file("magnus_base_merge_core", CORE_BASE_MERGE,
                  CORE_BASE_MERGE_SHA, "tracked_at_parent_commit"),
            _file("magnus_base_producer", BASE_PRODUCER, BASE_PRODUCER_SHA,
                  "authorized_untracked_dependency"),
            _file("frozen_magnus_input", INPUT_PATH, INPUT_SHA,
                  "tracked_at_parent_commit"),
            _file("frozen_word_artifact", WORDS_PATH, WORDS_SHA,
                  "tracked_at_parent_commit"),
        ],
        "executable_local_imports": [
            rel(PARENT_PRODUCER), rel(CORE_SHARD), rel(CORE_MERGE),
            rel(CORE_BASE_MERGE), rel(BASE_PRODUCER),
        ],
        "unbound_executable_imports": [],
    }


def dependency_digest() -> str:
    return sha_bytes(canonical_json(dependency_closure()))


def verify_file(path: Path, expected: str, role: str) -> None:
    require(path.is_file(), f"missing dependency {role}: {rel(path)}")
    actual = file_sha(path)
    require(actual == expected,
            f"dependency SHA drift for {role}: {rel(path)} {actual}")


def verify_closure(input_path: Path = INPUT_PATH,
                   words_path: Path = WORDS_PATH) -> None:
    """Verify all local executable imports before a dynamic import occurs."""
    verify_file(PARENT_PRODUCER, PARENT_PRODUCER_SHA, "parent producer")
    verify_file(PARENT_CHECKER, PARENT_CHECKER_SHA, "parent checker")
    verify_file(BASE_PRODUCER, BASE_PRODUCER_SHA, "transitive base producer")
    verify_file(CORE_SHARD, CORE_SHARD_SHA, "shard core")
    verify_file(CORE_MERGE, CORE_MERGE_SHA, "stream merge core")
    verify_file(CORE_BASE_MERGE, CORE_BASE_MERGE_SHA, "base merge core")
    verify_file(input_path, INPUT_SHA, "frozen Magnus input")
    verify_file(words_path, WORDS_SHA, "frozen word artifact")


def import_parent() -> Any:
    # Keep this check immediately adjacent to the first executable import.
    verify_closure()
    spec = importlib.util.spec_from_file_location(
        "d972_literal_a18_parent_v1", PARENT_PRODUCER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {PARENT_PRODUCER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wrapper_binding() -> dict[str, str]:
    return {
        "wrapper_path": rel(Path(__file__).resolve()),
        "wrapper_sha256": file_sha(Path(__file__).resolve()),
    }


def attach_node(node: dict[str, Any], closure: dict[str, object], digest: str,
               binding: dict[str, str]) -> None:
    node["dependency_closure"] = closure
    node["dependency_closure_sha256"] = digest
    node["dependency_wrapper_path"] = binding["wrapper_path"]
    node["dependency_wrapper_sha256"] = binding["wrapper_sha256"]


def attach_receipt(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(obj, dict), "producer output is not an object")
    closure = dependency_closure()
    digest = dependency_digest()
    binding = wrapper_binding()
    attach_node(obj, closure, digest, binding)
    degrees = obj.get("degrees")
    if isinstance(degrees, dict):
        for row in degrees.values():
            require(isinstance(row, dict), "degree row is not an object")
            attach_node(row, closure, digest, binding)
            shards = row.get("shards")
            if isinstance(shards, list):
                for record in shards:
                    require(isinstance(record, dict), "shard record is not an object")
                    attach_node(record, closure, digest, binding)
    shards = obj.get("shards")
    if isinstance(shards, list):
        for record in shards:
            require(isinstance(record, dict), "shard record is not an object")
            attach_node(record, closure, digest, binding)
    path.write_text(json.dumps(obj, ensure_ascii=True, sort_keys=True,
                               indent=2) + "\n", encoding="utf-8")
    return obj


def assert_binding(node: object, label: str) -> None:
    require(isinstance(node, dict), f"{label} missing receipt object")
    expected = dependency_closure()
    require(node.get("dependency_closure") == expected,
            f"{label} dependency closure drift")
    require(node.get("dependency_closure_sha256") == dependency_digest(),
            f"{label} dependency closure digest drift")
    binding = wrapper_binding()
    require(node.get("dependency_wrapper_path") == binding["wrapper_path"] and
            node.get("dependency_wrapper_sha256") == binding["wrapper_sha256"],
            f"{label} wrapper binding drift")


def assert_all_bound(obj: dict[str, Any]) -> None:
    assert_binding(obj, "top-level")
    degrees = obj.get("degrees")
    if isinstance(degrees, dict):
        for degree, row in degrees.items():
            assert_binding(row, f"degree-{degree}")
            if isinstance(row, dict) and isinstance(row.get("shards"), list):
                for index, record in enumerate(row["shards"]):
                    assert_binding(record, f"degree-{degree}-shard-{index}")
    if isinstance(obj.get("shards"), list):
        for index, record in enumerate(obj["shards"]):
            assert_binding(record, f"shard-{index}")


def validate_merge_inputs(args: argparse.Namespace) -> None:
    require(args.shard_dir is not None and args.shard_count is not None,
            "merge shard arguments are incomplete")
    expected = [args.shard_dir / args.pattern.format(
        degree=args.degree, index=index, count=args.shard_count)
               for index in range(args.shard_count)]
    require(all(path.is_file() for path in expected),
            "merge shard set is incomplete")
    for path in expected:
        obj = json.loads(path.read_text(encoding="utf-8"))
        assert_all_bound(obj)


def negative_binding_selftests() -> None:
    """Exercise all three receipt levels on a zero-defect synthetic receipt."""
    closure = dependency_closure()
    digest = dependency_digest()
    binding = wrapper_binding()
    base: dict[str, Any] = {
        "status": "D2_ALLPASS_UNKNOWN",
        "dependency_closure": closure,
        "dependency_closure_sha256": digest,
        "dependency_wrapper_path": binding["wrapper_path"],
        "dependency_wrapper_sha256": binding["wrapper_sha256"],
        "degrees": {"2": {
            "status": "D2_ALLPASS_UNKNOWN",
            "dependency_closure": closure,
            "dependency_closure_sha256": digest,
            "dependency_wrapper_path": binding["wrapper_path"],
            "dependency_wrapper_sha256": binding["wrapper_sha256"],
            "shards": [{
                "status": "D2_ALLPASS_UNKNOWN",
                "dependency_closure": closure,
                "dependency_closure_sha256": digest,
                "dependency_wrapper_path": binding["wrapper_path"],
                "dependency_wrapper_sha256": binding["wrapper_sha256"],
            }],
        }},
    }
    assert_all_bound(base)
    mutations = [
        ("top base removal", lambda x: x["dependency_closure"]["files"].pop(5)),
        ("degree base hash", lambda x: x["degrees"]["2"]["dependency_closure"]["files"][5].__setitem__("sha256", "0" * 64)),
        ("shard base binding", lambda x: x["degrees"]["2"]["shards"][0].__setitem__("dependency_closure", {})),
    ]
    import copy
    for label, mutate in mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        try:
            assert_all_bound(candidate)
        except (TypeError, ValueError, KeyError):
            continue
        raise ValueError(f"fail-open dependency mutation: {label}")
    # The synthetic receipt deliberately has no defects; binding failure must
    # remain fatal independently of mathematical status.
    require(base["status"] == "D2_ALLPASS_UNKNOWN", "zero-defect fixture drift")


def self_test() -> None:
    verify_closure()
    parent = import_parent()
    code = parent.main(["--mode", "self-test"])
    require(code == 0, "repaired v1 producer selftest failed")
    negative_binding_selftests()
    print(SELFTEST_MARKER)
    print(f"{FINAL_MARKER} phase=DEPENDENCY_SELFTEST status=PASS degrees=2,3,4,5,6")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("self-test", "shard", "merge"),
                        default="self-test")
    parser.add_argument("--degree", type=int, default=6)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--artifact", type=Path, default=WORDS_PATH)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--shard-dir", type=Path)
    parser.add_argument("--pattern", default="d972_b4_next_d{degree}_shard_{index}_of_{count}.json")
    args = parser.parse_args(argv)
    try:
        verify_closure(args.input, args.artifact)
        if args.mode == "self-test":
            self_test()
            return 0
        if args.mode == "merge":
            validate_merge_inputs(args)
        parent = import_parent()
        forwarded = list(argv) if argv is not None else sys.argv[1:]
        code = parent.main(forwarded)
        require(code == 0, "repaired v1 producer returned nonzero")
        require(args.output is not None and args.output.is_file(),
                "producer did not write its requested receipt")
        obj = attach_receipt(args.output)
        assert_all_bound(obj)
        phase = "SHARD" if args.mode == "shard" else "MERGE"
        print(f"{FINAL_MARKER} phase={phase} status={obj.get('status', 'PASS')} "
              f"degree={args.degree} output={args.output}", flush=True)
        return 0
    except Exception as exc:
        print(f"{FINAL_MARKER} status=ERROR error={type(exc).__name__}:{exc}",
              file=sys.stderr, flush=True)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
