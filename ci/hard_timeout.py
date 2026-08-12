#!/usr/bin/env python3
"""Run a command in its own process group with a hard timeout.

The parent writes an atomic JSON heartbeat periodically, mirrors child output
to stdout and a log file, and terminates the whole child process tree when the
deadline expires.  Exit code 124 means timeout; otherwise the child's exit code
is propagated.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import time
from typing import Any


TIMEOUT_EXIT_CODE = 124


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def terminate_tree(proc: subprocess.Popen[str], grace_seconds: float) -> dict[str, Any]:
    report: dict[str, Any] = {"term_sent": False, "kill_sent": False}
    if proc.poll() is not None:
        return report

    if os.name == "nt":
        # taskkill /T is the Windows equivalent of killing a POSIX process group.
        try:
            completed = subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                check=False,
                capture_output=True,
                text=True,
                timeout=max(1.0, grace_seconds),
            )
            report.update(
                {
                    "term_sent": True,
                    "taskkill_returncode": completed.returncode,
                    "taskkill_stdout": completed.stdout[-2000:],
                    "taskkill_stderr": completed.stderr[-2000:],
                }
            )
        except subprocess.TimeoutExpired:
            report.update({"term_sent": True, "taskkill_timed_out": True})
        if proc.poll() is None:
            proc.kill()
            report["direct_parent_kill_sent"] = True
        return report

    try:
        os.killpg(proc.pid, signal.SIGTERM)
        report["term_sent"] = True
    except ProcessLookupError:
        return report

    deadline = time.monotonic() + grace_seconds
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            return report
        time.sleep(0.1)

    try:
        os.killpg(proc.pid, signal.SIGKILL)
        report["kill_sent"] = True
    except ProcessLookupError:
        pass
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=float, required=True)
    parser.add_argument("--heartbeat-seconds", type=float, default=15.0)
    parser.add_argument("--kill-grace-seconds", type=float, default=5.0)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command is required after --")
    if args.timeout_seconds <= 0 or args.heartbeat_seconds <= 0:
        parser.error("timeout and heartbeat intervals must be positive")
    return args


def main() -> int:
    args = parse_args()
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    start_monotonic = time.monotonic()
    started_at = utc_now()

    popen_kwargs: dict[str, Any] = {}
    if os.name == "nt":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True

    proc = subprocess.Popen(
        args.command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        **popen_kwargs,
    )
    assert proc.stdout is not None

    output_queue: queue.Queue[str | None] = queue.Queue()

    def reader() -> None:
        try:
            for line in proc.stdout:
                output_queue.put(line)
        finally:
            output_queue.put(None)

    thread = threading.Thread(target=reader, name="hard-timeout-output", daemon=True)
    thread.start()

    state: dict[str, Any] = {
        "schema": "hard-timeout/v1",
        "state": "RUNNING",
        "command": args.command,
        "pid": proc.pid,
        "started_at_utc": started_at,
        "timeout_seconds": args.timeout_seconds,
        "heartbeat_seconds": args.heartbeat_seconds,
        "log": str(args.log),
        "checkpoint": str(args.checkpoint),
    }
    atomic_json(args.checkpoint, state)
    next_heartbeat = time.monotonic() + args.heartbeat_seconds
    reader_done = False
    timed_out = False
    timeout_detected_at: float | None = None
    termination_report: dict[str, Any] | None = None

    with args.log.open("w", encoding="utf-8", newline="") as log_handle:
        try:
            while True:
                now = time.monotonic()
                elapsed = now - start_monotonic
                if not timed_out and proc.poll() is None and elapsed >= args.timeout_seconds:
                    timed_out = True
                    timeout_detected_at = now
                    termination_report = terminate_tree(proc, args.kill_grace_seconds)

                try:
                    item = output_queue.get(timeout=0.1)
                    if item is None:
                        reader_done = True
                    else:
                        sys.stdout.write(item)
                        sys.stdout.flush()
                        log_handle.write(item)
                        log_handle.flush()
                except queue.Empty:
                    pass

                now = time.monotonic()
                if now >= next_heartbeat:
                    state.update(
                        {
                            "state": "TERMINATING" if timed_out else "RUNNING",
                            "elapsed_seconds": now - start_monotonic,
                            "heartbeat_at_utc": utc_now(),
                            "child_returncode": proc.poll(),
                            "log_bytes": args.log.stat().st_size if args.log.exists() else 0,
                        }
                    )
                    atomic_json(args.checkpoint, state)
                    next_heartbeat = now + args.heartbeat_seconds

                if proc.poll() is not None and reader_done and output_queue.empty():
                    break
                # A descendant can keep the inherited stdout pipe open even after
                # the direct child is dead.  Do not let that defeat the hard cap.
                if (
                    timed_out
                    and timeout_detected_at is not None
                    and proc.poll() is not None
                    and now - timeout_detected_at >= max(1.0, args.kill_grace_seconds)
                ):
                    break
        except BaseException:
            termination_report = terminate_tree(proc, args.kill_grace_seconds)
            raise

    thread.join(timeout=1.0)
    returncode = proc.wait()
    elapsed = time.monotonic() - start_monotonic
    state.update(
        {
            "state": "TIMED_OUT" if timed_out else "COMPLETED",
            "completed_at_utc": utc_now(),
            "elapsed_seconds": elapsed,
            "child_returncode": returncode,
            "wrapper_returncode": TIMEOUT_EXIT_CODE if timed_out else returncode,
            "timed_out": timed_out,
            "termination": termination_report,
            "log_bytes": args.log.stat().st_size if args.log.exists() else 0,
        }
    )
    atomic_json(args.checkpoint, state)
    if timed_out:
        print(f"HARD_TIMEOUT_EXPIRED seconds={args.timeout_seconds}", flush=True)
        return TIMEOUT_EXIT_CODE
    print(f"HARD_TIMEOUT_CHILD_EXIT returncode={returncode}", flush=True)
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
