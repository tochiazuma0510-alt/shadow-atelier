#!/usr/bin/env python3
"""Read-only fallback inventory of L2(8) extension metadata.

This does not construct a group and cannot replace the failed GAP inventory.
It only gives a bounded list of library records for later construction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / (
    "GAP-4.16.0/runtime/opt/gap-4.16.0/grp"
)
PATTERN = re.compile(
    r'"(?P<label>[^"\r\n]*L2\(8\)[^"\r\n]*)",\s*'
    r'\[16,(?P<d>\d+),(?P<index>\d+)\],(?P<tail>[^,\r\n]+),'
)


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prereg", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    began = time.monotonic()
    prereg_path = Path(args.prereg)
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    state = {"schema": "campaign138_perfect_metadata_checkpoint/v1", "stage": "start", "complete": False}
    atomic_json(checkpoint_path, state)

    def update(stage: str, **extra: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - began)), **extra)
        atomic_json(checkpoint_path, state)

    def timeout() -> None:
        if not state["complete"]:
            update("hard_timeout")
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
        if prereg["producer_sha256"] != sha_file(Path(__file__)):
            raise RuntimeError("preregistration binding mismatch")
        records = []
        manifest = []
        for path in sorted(LIBRARY.glob("perf*.grp"), key=lambda item: item.name):
            text = path.read_text(encoding="utf-8")
            manifest.append({"file": path.name, "sha256": sha_file(path), "bytes": path.stat().st_size})
            for match in PATTERN.finditer(text):
                dimension = int(match.group("d"))
                index = int(match.group("index"))
                if dimension < 1 or 504 * 2**dimension > 2_000_000:
                    continue
                records.append(
                    {
                        "family_key": [16, dimension, index],
                        "dimension_parameter": dimension,
                        "family_index": index,
                        "order_if_2_kernel": 504 * 2**dimension,
                        "label": match.group("label"),
                        "tail_token": match.group("tail").strip(),
                        "file": path.name,
                        "line": text.count("\n", 0, match.start()) + 1,
                    }
                )
        records.sort(key=lambda item: (item["dimension_parameter"], item["family_index"], item["label"]))
        positive_control = any(
            item["family_key"] == [16, 6, 2] and item["label"] == "L2(8) N 2^6"
            for item in records
        )
        result = {
            "schema": "campaign138_perfect_metadata/v1",
            "status": "METADATA_ONLY",
            "preregistration_sha256": sha_file(prereg_path),
            "producer_sha256": sha_file(Path(__file__)),
            "library_root": str(LIBRARY),
            "library_manifest": manifest,
            "records": records,
            "record_count": len(records),
            "dimension_distribution": {
                str(dimension): sum(item["dimension_parameter"] == dimension for item in records)
                for dimension in sorted({item["dimension_parameter"] for item in records})
            },
            "positive_control": {
                "required_family_key": [16, 6, 2],
                "required_label": "L2(8) N 2^6",
                "passed": positive_control,
            },
            "limitations": {
                "groups_constructed": 0,
                "radical_quotient_checked": False,
                "splitness_checked": False,
                "marked_realization_checked": False,
                "isolatedness_checked": False,
            },
            "outcomes_opened": {"shadow": 0, "reduction": 0, "element_survival": 0},
            "noncontact": {"u": False, "c": False, "sealed_three_quantities": False, "sealed_K5": False},
        }
        if not positive_control:
            raise RuntimeError("metadata positive control missing")
        atomic_json(output_path, result)
        update("complete", complete=True, record_count=len(records), output_sha256=sha_file(output_path))
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
