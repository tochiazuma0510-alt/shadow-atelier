#!/usr/bin/env python3
"""Independent checker front-end for the literal-A.18 v2 closure.

The mathematical checker is the repaired v1 checker and is loaded only after
the complete local dependency closure has been authenticated.  v2 validates
the new closure at the top, degree, and shard-record levels, then removes
only those transport annotations in a temporary copy before handing the
lossless receipt to the independent v1 algebraic checker.  Thus the extra
provenance cannot weaken any v1 schema or ideal check.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
V2_PRODUCER = ROOT / "search" / "d972_b4_next_obstruction_v2.py"
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
V2_PRODUCER_SHA = "85e2c3e954a2778579fcc3fa6d375a44effb49d34bf87b7e9c391970d2639f98"
BASE_PRODUCER_SHA = "b2e5184e31e177dcf5bfdc9fcd715e2146db877e0eccda2056cc5d7f999ae6bc"
CORE_SHARD_SHA = "1a18994e3933d5d42e85274af62badb89c2f9a65c92c63862d1740ac2d47da63"
CORE_MERGE_SHA = "6ccce4e95378dfa22051bd8c09e3d3aa5a91234b8d155c0fb57fd18c34f24bf5"
CORE_BASE_MERGE_SHA = "c79abb6ff51bccaaf98992fa070fecf3aba9d70ea4f6b6deff90d4cfcef1814c"
INPUT_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
TRACKED_PARENT_COMMIT = "0e0b0b0855f3c42c00c614b863ff0e14368734da"
DEPENDENCY_SCHEMA = "d972-b4-literal-a18-dependency-closure/v2"
CHECKER_MARKER = "D972_B4_NEXT_OBSTRUCTION_CHECKER_V2_FINAL"
SELFTEST_MARKER = "D972_B4_NEXT_OBSTRUCTION_CHECKER_V2_DEPENDENCY_SELFTEST_PASS"


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
    # This function is called before the first dynamic import below.
    verify_file(V2_PRODUCER, V2_PRODUCER_SHA, "v2 producer wrapper")
    verify_file(PARENT_PRODUCER, PARENT_PRODUCER_SHA, "parent producer")
    verify_file(PARENT_CHECKER, PARENT_CHECKER_SHA, "parent checker")
    verify_file(BASE_PRODUCER, BASE_PRODUCER_SHA, "transitive base producer")
    verify_file(CORE_SHARD, CORE_SHARD_SHA, "shard core")
    verify_file(CORE_MERGE, CORE_MERGE_SHA, "stream merge core")
    verify_file(CORE_BASE_MERGE, CORE_BASE_MERGE_SHA, "base merge core")
    verify_file(input_path, INPUT_SHA, "frozen Magnus input")
    verify_file(words_path, WORDS_SHA, "frozen word artifact")


def import_parent_checker() -> Any:
    verify_closure()
    spec = importlib.util.spec_from_file_location(
        "d972_literal_a18_parent_checker_v1", PARENT_CHECKER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {PARENT_CHECKER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def producer_binding() -> dict[str, str]:
    return {
        "path": "search/d972_b4_next_obstruction_v2.py",
        "sha256": V2_PRODUCER_SHA,
    }


def assert_bound(node: object, label: str) -> None:
    require(isinstance(node, dict), f"{label} missing receipt object")
    require(node.get("dependency_closure") == dependency_closure(),
            f"{label} dependency closure drift")
    require(node.get("dependency_closure_sha256") == dependency_digest(),
            f"{label} dependency closure digest drift")
    binding = producer_binding()
    require(node.get("dependency_wrapper_path") == binding["path"] and
            node.get("dependency_wrapper_sha256") == binding["sha256"],
            f"{label} producer wrapper binding drift")


def assert_tree_bound(obj: dict[str, Any]) -> None:
    assert_bound(obj, "top-level")
    degrees = obj.get("degrees")
    if isinstance(degrees, dict):
        for degree, row in degrees.items():
            assert_bound(row, f"degree-{degree}")
            if isinstance(row, dict) and isinstance(row.get("shards"), list):
                for index, record in enumerate(row["shards"]):
                    assert_bound(record, f"degree-{degree}-shard-{index}")
    if isinstance(obj.get("shards"), list):
        for index, record in enumerate(obj["shards"]):
            assert_bound(record, f"shard-{index}")


DEPENDENCY_KEYS = {
    "dependency_closure", "dependency_closure_sha256",
    "dependency_wrapper_path", "dependency_wrapper_sha256",
    "dependency_checker_path", "dependency_checker_sha256",
}


def without_dependency_annotations(value: object) -> object:
    if isinstance(value, dict):
        return {key: without_dependency_annotations(item)
                for key, item in value.items() if key not in DEPENDENCY_KEYS}
    if isinstance(value, list):
        return [without_dependency_annotations(item) for item in value]
    return value


def validate_receipt_paths(paths: Sequence[Path]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for path in paths:
        obj = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(obj, dict), f"receipt is not an object: {path}")
        assert_tree_bound(obj)
        objects.append(obj)
    return objects


def checker_binding(obj: dict[str, Any]) -> None:
    closure = dependency_closure()
    digest = dependency_digest()
    obj["dependency_closure"] = closure
    obj["dependency_closure_sha256"] = digest
    obj["dependency_checker_path"] = rel(Path(__file__).resolve())
    obj["dependency_checker_sha256"] = file_sha(Path(__file__).resolve())
    if isinstance(obj.get("degrees"), list):
        for row in obj["degrees"]:
            require(isinstance(row, dict), "checker degree summary is not an object")
            row["dependency_closure"] = closure
            row["dependency_closure_sha256"] = digest
            row["dependency_checker_path"] = rel(Path(__file__).resolve())
            row["dependency_checker_sha256"] = file_sha(Path(__file__).resolve())


def negative_binding_selftests() -> None:
    closure = dependency_closure()
    digest = dependency_digest()
    binding = producer_binding()
    base: dict[str, Any] = {
        "status": "D2_ALLPASS_UNKNOWN",
        "dependency_closure": closure,
        "dependency_closure_sha256": digest,
        "dependency_wrapper_path": binding["path"],
        "dependency_wrapper_sha256": binding["sha256"],
        "degrees": {"2": {
            "status": "D2_ALLPASS_UNKNOWN",
            "dependency_closure": closure,
            "dependency_closure_sha256": digest,
            "dependency_wrapper_path": binding["path"],
            "dependency_wrapper_sha256": binding["sha256"],
            "shards": [{
                "status": "D2_ALLPASS_UNKNOWN",
                "dependency_closure": closure,
                "dependency_closure_sha256": digest,
                "dependency_wrapper_path": binding["path"],
                "dependency_wrapper_sha256": binding["sha256"],
            }],
        }},
    }
    assert_tree_bound(base)
    mutations = [
        ("top base removal", lambda x: x["dependency_closure"]["files"].pop(5)),
        ("degree base hash", lambda x: x["degrees"]["2"]["dependency_closure"]["files"][5].__setitem__("sha256", "0" * 64)),
        ("shard base binding", lambda x: x["degrees"]["2"]["shards"][0].__setitem__("dependency_closure", {})),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        try:
            assert_tree_bound(candidate)
        except (TypeError, ValueError, KeyError):
            continue
        raise ValueError(f"fail-open dependency mutation: {label}")
    require(base["status"] == "D2_ALLPASS_UNKNOWN", "zero-defect fixture drift")


def self_test() -> None:
    verify_closure()
    parent = import_parent_checker()
    code = parent.main(["--self-test"])
    require(code == 0, "repaired v1 checker selftest failed")
    negative_binding_selftests()
    print(SELFTEST_MARKER)
    print(f"{CHECKER_MARKER} status=PASS degrees=2,3,4,5,6")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, action="append")
    parser.add_argument("--receipt-dir", type=Path)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--artifact", type=Path, default=WORDS_PATH)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path,
                        default=Path(tempfile.gettempdir()) /
                        "d972_literal_a18_check_v2.json")
    args = parser.parse_args(argv)
    try:
        verify_closure(args.input, args.artifact)
        if args.self_test:
            self_test()
            return 0
        if args.receipt_dir is not None:
            paths = [args.receipt_dir /
                     f"d972_b4_next_obstruction_d{degree}.json"
                     for degree in range(2, 7)]
        else:
            paths = args.receipt or []
        require(len(paths) == 5, "exactly five degree receipts are required")
        validate_receipt_paths(paths)
        parent = import_parent_checker()
        # v1 deliberately requires the exact historical shard-record schema.
        # Run it on an external, annotation-free copy after v2 has checked the
        # added closure, preserving both independent checks and fail-closed
        # provenance.
        with tempfile.TemporaryDirectory(prefix="d972_literal_a18_v2_check_") as td:
            temp_root = Path(td)
            sanitized: list[Path] = []
            for path in paths:
                obj = json.loads(path.read_text(encoding="utf-8"))
                clean = without_dependency_annotations(obj)
                target = temp_root / path.name
                target.write_text(json.dumps(clean, ensure_ascii=True,
                                             sort_keys=True, indent=2) + "\n",
                                  encoding="utf-8")
                sanitized.append(target)
            forwarded: list[str] = ["--input", str(args.input),
                                    "--artifact", str(args.artifact),
                                    "--output", str(args.output)]
            for path in sanitized:
                forwarded.extend(("--receipt", str(path)))
            code = parent.main(forwarded)
        require(args.output.is_file(), "checker did not write its result")
        result = json.loads(args.output.read_text(encoding="utf-8"))
        require(isinstance(result, dict), "checker result is not an object")
        checker_binding(result)
        args.output.write_text(json.dumps(result, ensure_ascii=True,
                                          sort_keys=True, indent=2) + "\n",
                               encoding="utf-8")
        print(f"{CHECKER_MARKER} status={result.get('status', 'REJECTED')} "
              "degrees=2,3,4,5,6", flush=True)
        return code
    except Exception as exc:
        print(json.dumps({"schema": "d972-b4-next-obstruction-check/v2",
                          "status": "REJECTED", "reason": str(exc)},
                         sort_keys=True), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
