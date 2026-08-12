"""Bounded, checkpointed runner for all Sol task 123 producer/checker steps."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "search" / "certs" / "sol123_run_checkpoint_v1_20260813.json"
HARD_TIMEOUT_SECONDS = 120
RUN_ID = "sol123-local-20260813-v1"
STEPS = [
    ("r3_u9_producer", ROOT / "search" / "sol123_r3_u9.py"),
    ("r3_u9_checker", ROOT / "crosscheck" / "check_sol123_r3_u9.py"),
    ("u3_geometry_producer", ROOT / "search" / "sol123_u3_geometry.py"),
    ("u3_geometry_checker", ROOT / "crosscheck" / "check_sol123_u3_geometry.py"),
]


def atomic_checkpoint(payload: dict) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    temporary = CHECKPOINT.with_suffix(CHECKPOINT.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, CHECKPOINT)


def main() -> None:
    checkpoint: dict = {
        "schema": "sol123-run-checkpoint/v1",
        "task": "Sol-123/R3-UNRAM",
        "run_id": RUN_ID,
        "hard_timeout_seconds_per_step": HARD_TIMEOUT_SECONDS,
        "steps": [],
        "status": "RUNNING",
    }
    atomic_checkpoint(checkpoint)

    for name, script in STEPS:
        record = {
            "name": name,
            "script": script.relative_to(ROOT).as_posix(),
            "status": "RUNNING",
        }
        checkpoint["steps"].append(record)
        atomic_checkpoint(checkpoint)
        try:
            completed = subprocess.run(
                [sys.executable, str(script)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=HARD_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired:
            record["status"] = "UNKNOWN_HARD_TIMEOUT"
            checkpoint["status"] = "UNKNOWN_STOP"
            atomic_checkpoint(checkpoint)
            raise SystemExit(f"UNKNOWN: hard timeout in {name}")

        record["returncode"] = completed.returncode
        record["stdout"] = completed.stdout.strip()
        record["stderr"] = completed.stderr.strip()
        if completed.returncode != 0:
            record["status"] = "UNKNOWN_STEP_FAILURE"
            checkpoint["status"] = "UNKNOWN_STOP"
            atomic_checkpoint(checkpoint)
            if completed.stderr:
                print(completed.stderr, file=sys.stderr)
            raise SystemExit(f"UNKNOWN: step failure in {name}")
        record["status"] = "COMPLETE"
        atomic_checkpoint(checkpoint)

    checkpoint["status"] = "COMPLETE_WITH_U3_2_UNKNOWN_STOP_RECORDED"
    atomic_checkpoint(checkpoint)
    print(
        json.dumps(
            {
                "status": checkpoint["status"],
                "run_id": RUN_ID,
                "checkpoint": CHECKPOINT.relative_to(ROOT).as_posix(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
