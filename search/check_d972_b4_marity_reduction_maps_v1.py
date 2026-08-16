#!/usr/bin/env python3
"""Independent, fail-closed checker for the four PB4 -> PB3 maps.

The fixture is intentionally small and immutable: it freezes only the
strand-forgetting data, not the missing PB4 presentation or the 972 fibers.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "search" / "certs" / "d972_b4_marity_reduction_maps_v1.json"

EXPECTED_MAPS = [
    {"index": 1, "deleted_strand": 1, "generator_images": [[], [], [], [1], [2], [3]]},
    {"index": 2, "deleted_strand": 2, "generator_images": [[], [1], [2], [], [], [3]]},
    {"index": 3, "deleted_strand": 3, "generator_images": [[1], [], [2], [], [3], []]},
    {"index": 4, "deleted_strand": 4, "generator_images": [[1], [2], [], [3], [], []]},
]
EXPECTED_IDENTITIES = [
    "p4 o c_(sigma3^-1) = p3",
    "p3 o c_(sigma2^-1) = p2",
    "p2 o c_(sigma1^-1) = p1",
]


def compact(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha256(value: object) -> str:
    return hashlib.sha256(compact(value)).hexdigest()


def validate(obj: dict, source: str = "artifact") -> None:
    required = {
        "schema", "status", "source_group", "target_group",
        "source_generator_labels", "target_generator_labels", "image_encoding",
        "maps", "conjugation_identities", "source_references", "maps_sha256",
    }
    missing = sorted(required - set(obj))
    if missing:
        raise AssertionError(f"{source}: missing keys {missing}")
    if obj["schema"] != "d972-b4-marity-reduction-maps/v1":
        raise AssertionError(f"{source}: schema drift")
    if obj["status"] != "PROVED_BY_CANONICAL_STRAND_FORGETTING":
        raise AssertionError(f"{source}: status drift")
    if obj["source_group"] != "PB4" or obj["target_group"] != "PB3":
        raise AssertionError(f"{source}: group type drift")
    if obj["source_generator_labels"] != ["x12", "x13", "x14", "x23", "x24", "x34"]:
        raise AssertionError(f"{source}: PB4 generator labels drift")
    if obj["target_generator_labels"] != ["y12", "y13", "y23"]:
        raise AssertionError(f"{source}: PB3 generator labels drift")
    if obj["image_encoding"] != "signed_target_generator_indices":
        raise AssertionError(f"{source}: image encoding drift")
    if obj["maps"] != EXPECTED_MAPS:
        raise AssertionError(f"{source}: map table drift")
    if obj["conjugation_identities"] != EXPECTED_IDENTITIES:
        raise AssertionError(f"{source}: conjugation identities drift")
    if not isinstance(obj["source_references"], list) or not obj["source_references"]:
        raise AssertionError(f"{source}: source references missing")
    if any(not isinstance(word, list) for row in obj["maps"] for word in row["generator_images"]):
        raise AssertionError(f"{source}: signed words must remain JSON lists (including empty words)")
    expected_digest = sha256(EXPECTED_MAPS)
    if obj["maps_sha256"] != expected_digest:
        raise AssertionError(f"{source}: maps_sha256 mismatch")


def load(path: Path = DEFAULT_ARTIFACT) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise AssertionError(f"{path}: top-level JSON must be an object")
    validate(obj, str(path))
    return obj


def selftest() -> None:
    obj = load()
    assert obj["maps"][0]["generator_images"][0] == []
    assert "B4_stable" not in obj
    mutated = copy.deepcopy(obj)
    mutated["maps"][0]["generator_images"][0] = ""
    try:
        validate(mutated, "mutated selftest fixture")
    except AssertionError:
        pass
    else:
        raise AssertionError("serializer/type mutation was accepted")
    mutated = copy.deepcopy(obj)
    mutated["maps"][3]["generator_images"][0] = [-1]
    try:
        validate(mutated, "mutated signed-word selftest fixture")
    except AssertionError:
        pass
    else:
        raise AssertionError("signed-word mutation was accepted")
    print("D972_B4_MARITY_REDUCTION_MAPS_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--check", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args()
    if args.selftest:
        selftest()
    else:
        load(args.check)
        print("D972_B4_MARITY_REDUCTION_MAPS_V1_CHECK_PASS", args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
