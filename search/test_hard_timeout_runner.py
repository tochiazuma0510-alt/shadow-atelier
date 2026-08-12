#!/usr/bin/env python3
"""Smoke tests for ci/hard_timeout.py using only temporary directories."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ci" / "hard_timeout.py"
TMP_PARENT = ROOT / "ci" / "out"


def invoke(prefix: Path, timeout: float, code: str) -> tuple[subprocess.CompletedProcess[str], dict]:
    checkpoint = prefix.with_suffix(".checkpoint.json")
    log = prefix.with_suffix(".child.log")
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--timeout-seconds",
            str(timeout),
            "--heartbeat-seconds",
            "0.1",
            "--kill-grace-seconds",
            "0.2",
            "--checkpoint",
            str(checkpoint),
            "--log",
            str(log),
            "--",
            sys.executable,
            "-c",
            code,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if not checkpoint.exists():
        raise AssertionError(
            f"checkpoint missing; returncode={completed.returncode}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    payload["_test_log_text"] = log.read_text(encoding="utf-8")
    checkpoint.unlink()
    log.unlink()
    return completed, payload


def main() -> None:
    TMP_PARENT.mkdir(parents=True, exist_ok=True)
    prefix = TMP_PARENT / f"hard-timeout-test-{uuid.uuid4().hex}"
    completed, checkpoint = invoke(prefix, 5.0, "print('quick-child-marker', flush=True)")
    assert completed.returncode == 0, completed
    assert checkpoint["state"] == "COMPLETED", checkpoint
    assert checkpoint["timed_out"] is False, checkpoint
    assert "quick-child-marker" in checkpoint["_test_log_text"]

    prefix = TMP_PARENT / f"hard-timeout-test-{uuid.uuid4().hex}"
    code = (
        "import subprocess,sys,time; "
        "subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
        "print('tree-child-marker',flush=True); time.sleep(60)"
    )
    completed, checkpoint = invoke(prefix, 0.5, code)
    assert completed.returncode == 124, completed
    assert checkpoint["state"] == "TIMED_OUT", checkpoint
    assert checkpoint["timed_out"] is True, checkpoint
    assert checkpoint["termination"]["term_sent"] is True, checkpoint

    print("HARD_TIMEOUT_SELFTEST_DONE", flush=True)


if __name__ == "__main__":
    main()
