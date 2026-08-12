#!/usr/bin/env python3
"""Merge four independently checkpointed wall-window producer artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


LABELS = ("wall24", "wall28", "wall36", "wall37")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    walls = {}
    controls = None
    receipts = []
    for path in args.input:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema") != "wall-crown-census/v1":
            raise ValueError(f"schema mismatch in {path}")
        if len(payload["walls"]) != 1:
            raise ValueError(f"expected one wall in {path}")
        wall = payload["walls"][0]
        if wall["label"] in walls:
            raise ValueError(f"duplicate wall {wall['label']}")
        walls[wall["label"]] = wall
        if controls is None:
            controls = payload["positive_controls"]
        elif controls != payload["positive_controls"]:
            raise ValueError("positive-control payloads differ across shards")
        receipts.append({"path": path.as_posix(), "sha256": sha256(path)})
    if set(walls) != set(LABELS):
        raise ValueError(f"wall coverage mismatch: {sorted(walls)}")

    output = {
        "schema": "wall-crown-census/v1",
        "generated_by": "search/combine_wall_crown_census_v1.py",
        "universe": "wall-window instances n=24,28,36,37 only",
        "method": "four independently artifacted wall-window producer jobs",
        "quarantine": {
            "K9": "group-theory positive control only",
            "K5": "not accessed",
            "name_collide": "wall-window instance",
            "u_c": "not accessed",
        },
        "positive_controls": controls,
        "walls": [walls[label] for label in LABELS],
        "shard_receipts": receipts,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print("WALL_CROWN_CENSUS_COMBINE_DONE walls=4")


if __name__ == "__main__":
    main()
