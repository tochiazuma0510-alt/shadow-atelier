#!/usr/bin/env python3
"""GHA-ready bounded runner for the direct logged IdRel B4 lane.

The GAP file performs all group work.  This wrapper supplies caps through a
temporary GAP prelude, applies an external process timeout, preserves stage
artifacts, and then invokes the independent F6 checker when a receipt was
written.  It does not turn a finite all-pass in a different quotient into a
terminal result; only the direct logged receipt can return terminal.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAP_SOURCE = ROOT / "search" / "d972_b4_u_idrel_direct_logged_v1.g"
CHECKER = ROOT / "search" / "check_d972_b4_u_idrel_direct_logged_v1.py"
INPUT = ROOT / "search/certs/d972_b4_p2_magnus_input_v2_20260816.json"
WORDS = ROOT / "search/certs/d972_b4_word_key_artifact_v1_20260816.json"


def gap_quote(path: Path) -> str:
    return '"' + str(path.resolve()).replace("\\", "\\\\").replace('"', '\\"') + '"'


def unknown_receipt(output: Path, status: str, detail: str, timeout: int | None = None) -> None:
    payload = {
        "schema": "d972-b4-u-idrel-direct-logged/v1",
        "status": status,
        "proof_level": "F6_FREE_GROUP_LOG_REPLAY_CANDIDATE",
        "generator_count": 6,
        "relator_count": 158,
        "norm_count": 972,
        "unique_norm_count": 486,
        "stage_artifacts": [
            {"stage": i, "artifact": str(p), "status": "UNKNOWN_EXTERNAL"}
            for i, p in enumerate(sorted(output.parent.glob(output.name + ".stage*.json")))
        ],
        "runner_error": detail,
    }
    if timeout is not None:
        payload["external_timeout_seconds"] = timeout
    output.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--words", type=Path, default=WORDS)
    parser.add_argument("--source", type=Path, default=GAP_SOURCE)
    parser.add_argument("--max-passes", type=int, default=1)
    parser.add_argument("--max-rules", type=int, default=20000)
    parser.add_argument("--max-log-length", type=int, default=8192)
    parser.add_argument("--max-conjugator-length", type=int, default=16384)
    parser.add_argument("--max-log-letters", type=int, default=200000)
    parser.add_argument("--max-reduced-length", type=int, default=4096)
    parser.add_argument("--max-wall-seconds", type=int, default=1800)
    parser.add_argument("--gap-command", default="gap",
                        help="GAP executable on Linux GHA runners")
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if (
        args.max_passes < 0
        or args.max_rules <= 0
        or args.max_log_length <= 0
        or args.max_conjugator_length <= 0
        or args.max_log_letters <= 0
    ):
        parser.error("caps must be positive (max-passes may be zero)")
    if args.max_reduced_length <= 0 or args.max_wall_seconds <= 0:
        parser.error("caps must be positive")

    with tempfile.TemporaryDirectory(prefix="d972-b4-idrel-") as temp:
        prelude = Path(temp) / "driver.g"
        prelude.write_text(
            "D972_B4_IDREL_INPUT := " + gap_quote(args.input) + ";;\n"
            "D972_B4_IDREL_WORDS := " + gap_quote(args.words) + ";;\n"
            "D972_B4_IDREL_OUTPUT := " + gap_quote(output) + ";;\n"
            f"D972_B4_IDREL_MAX_PASSES := {args.max_passes};;\n"
            f"D972_B4_IDREL_MAX_RULES := {args.max_rules};;\n"
            f"D972_B4_IDREL_MAX_LOG_LENGTH := {args.max_log_length};;\n"
            f"D972_B4_IDREL_MAX_CONJUGATOR_LENGTH := {args.max_conjugator_length};;\n"
            f"D972_B4_IDREL_MAX_LOG_LETTERS := {args.max_log_letters};;\n"
            f"D972_B4_IDREL_MAX_REDUCED_LENGTH := {args.max_reduced_length};;\n"
            f"D972_B4_IDREL_MAX_WALL_MS := {args.max_wall_seconds * 1000};;\n"
            "Read(" + gap_quote(args.source) + ");;\n",
            encoding="ascii",
        )
        if os.name == "nt":
            command = [
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", str(ROOT / "gap.ps1"), str(prelude),
            ]
        else:
            command = [args.gap_command, "-q", "--quitonbreak", "-o", "2g", str(prelude)]
        try:
            run = subprocess.run(
                command, cwd=ROOT, text=True, capture_output=True,
                encoding="utf-8", errors="replace", timeout=args.max_wall_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            unknown_receipt(output, "UNKNOWN_EXTERNAL_WALL_CAP",
                            "GAP process exceeded external wall cap", args.max_wall_seconds)
            print(json.dumps({"status": "UNKNOWN_EXTERNAL_WALL_CAP",
                              "output": str(output),
                              "stdout_tail": str(exc.stdout or "")[-4000:]}, sort_keys=True))
            return 2

    if not output.exists():
        unknown_receipt(output, "UNKNOWN_GAP_RUNTIME",
                        f"GAP returned {run.returncode} without a receipt")
        print(json.dumps({"status": "UNKNOWN_GAP_RUNTIME", "returncode": run.returncode,
                          "output": str(output), "log_tail":
                          (run.stdout + run.stderr)[-12000:]}, sort_keys=True))
        return 2
    try:
        receipt = json.loads(output.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        unknown_receipt(output, "UNKNOWN_GAP_RECEIPT_JSON", "receipt is not JSON")
        return 2
    receipt["runner"] = {
        "external_wall_seconds": args.max_wall_seconds,
        "gap_returncode": run.returncode,
        "source_path": str(args.source.resolve()),
    }
    output.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    # The independent checker is deliberately a separate process and code
    # path.  Its exit 2 means a valid bounded UNKNOWN; preserve that result.
    try:
        check = subprocess.run(
            [sys.executable, str(CHECKER), "--receipt", str(output),
             "--input", str(args.input), "--words", str(args.words)],
            cwd=ROOT, text=True, capture_output=True,
            encoding="utf-8", errors="replace", timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        print(json.dumps({"status": "UNKNOWN_CHECKER_TIMEOUT",
                          "output": str(output),
                          "checker_log_tail": str(exc.stdout or "")[-4000:]}, sort_keys=True))
        return 3
    print(json.dumps({
        "status": receipt.get("status", "UNKNOWN"),
        "gap_returncode": run.returncode,
        "checker_returncode": check.returncode,
        "output": str(output),
        "gap_log_tail": (run.stdout + run.stderr)[-12000:],
        "checker_log": check.stdout[-12000:] + check.stderr[-4000:],
    }, sort_keys=True))
    if check.returncode == 1:
        return 3
    terminal_ok = (
        run.returncode == 0
        and check.returncode == 0
        and receipt.get("status") == "B4_B_DIRECT_LOGGED_TERMINAL"
    )
    return 0 if terminal_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
