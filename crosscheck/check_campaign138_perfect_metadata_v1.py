#!/usr/bin/env python3
"""Line-parser checker for campaign138 PerfectGroups metadata inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def parse_marker(line: str) -> tuple[int, int] | None:
    marker = "[16,"
    position = line.find(marker)
    if position < 0:
        return None
    remainder = line[position + len(marker) :]
    first, separator, remainder = remainder.partition(",")
    second, separator2, _ = remainder.partition("]")
    if not separator or not separator2 or not first.strip().isdigit() or not second.strip().isdigit():
        return None
    return int(first), int(second)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source_path = Path(args.source)
    source = json.loads(source_path.read_text(encoding="utf-8"))
    library = Path(source["library_root"])
    records = []
    manifest = []
    for path in sorted(library.glob("perf*.grp"), key=lambda item: item.name):
        manifest.append({"file": path.name, "sha256": sha_file(path), "bytes": path.stat().st_size})
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if '"L2(8)' not in line:
                continue
            marker = parse_marker(line)
            if marker is None:
                continue
            dimension, index = marker
            if dimension < 1 or 504 * 2**dimension > 2_000_000:
                continue
            pieces = line.split('"')
            if len(pieces) < 3:
                continue
            after = line[line.find("]", line.find("[16,")) + 1 :]
            tail = after.lstrip().lstrip(",").split(",", 1)[0].strip()
            records.append(
                {
                    "family_key": [16, dimension, index],
                    "dimension_parameter": dimension,
                    "family_index": index,
                    "order_if_2_kernel": 504 * 2**dimension,
                    "label": pieces[1],
                    "tail_token": tail,
                    "file": path.name,
                    "line": line_number,
                }
            )
    records.sort(key=lambda item: (item["dimension_parameter"], item["family_index"], item["label"]))
    checks = {
        "schema": source["schema"] == "campaign138_perfect_metadata/v1",
        "manifest": source["library_manifest"] == manifest,
        "records": source["records"] == records,
        "record_count": source["record_count"] == len(records),
        "positive_control": source["positive_control"]["passed"]
        and any(item["family_key"] == [16, 6, 2] and item["label"] == "L2(8) N 2^6" for item in records),
        "no_outcomes": source["outcomes_opened"] == {"shadow": 0, "reduction": 0, "element_survival": 0},
    }
    result = {
        "schema": "campaign138_perfect_metadata_check/v1",
        "source_sha256": sha_file(source_path),
        "checker_sha256": sha_file(Path(__file__)),
        "checks": checks,
        "all_checks_true": all(checks.values()),
        "record_count": len(records),
    }
    atomic_json(Path(args.output), result)
    if not result["all_checks_true"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
