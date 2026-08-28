#!/usr/bin/env python3
"""R07 A0/v11 deterministic bootstrap, fail-closed before execution.

The v10 candidate is immutable.  This version deliberately has no producer
receipt path until the exact SELFTEST receipt R and independent verdict V can
be preregistered byte-for-byte.  It is therefore a typed implementation
blocker, not a mathematical result and not a substitute SELFTEST.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-history-free-positive-fast-resume/v11"
PREREGISTRATION = ROOT / "ci/in/d972_r07_history_free_positive_fast_resume_selftest_v11.preregistration.v1.json"
BLOCKER = "preregistration_exact_R_V_bytes_unresolved_before_execution"
ALLOWED_MODES = ("SELFTEST", "PRODUCTION")
OUTER_DEADLINES = {"producer_seconds": 10800, "checker_seconds": 7200,
                   "artifact_seconds": 3600, "total_seconds": 21600}
TERMINALS = ("R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_SELFTEST_PASS",
             "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_COMMON_WORD",
             "UNKNOWN_INPUT", "UNKNOWN_RESOURCE")


class BootstrapBlocked(RuntimeError):
    """The preregistration contract is incomplete and must stop."""


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def read_preregistration() -> dict[str, object]:
    try:
        raw = PREREGISTRATION.read_bytes()
        value = json.loads(raw.decode("ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BootstrapBlocked("preregistration_owner_unreadable") from exc
    if type(value) is not dict or value.get("execution") != "UNEXECUTED":
        raise BootstrapBlocked("preregistration_execution_not_unexecuted")
    if value.get("status") != "BLOCKED":
        raise BootstrapBlocked("preregistration_status_not_blocked")
    for key in ("expected_receipt", "expected_verdict"):
        owner = value.get(key)
        if type(owner) is not dict or any(owner.get(field) is not None
                                          for field in ("bytes", "sha256",
                                                        "self_digest_sha256",
                                                        "semantic_digest_sha256")):
            raise BootstrapBlocked("preregistration_R_V_must_be_exact")
    raise BootstrapBlocked(BLOCKER)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--mode", choices=ALLOWED_MODES, required=True)
    result.add_argument("--source", type=Path, required=True)
    result.add_argument("--manifest", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    result.add_argument("--seconds", type=float, required=True)
    result.add_argument("--workers", type=int, choices=(2, 4), required=True)
    result.add_argument("--selftest-receipt", type=Path)
    result.add_argument("--resume", type=Path)
    result.add_argument("--resume-manifest", type=Path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.mode not in ALLOWED_MODES:
        raise BootstrapBlocked("unknown_driver_mode")
    if args.seconds != float(OUTER_DEADLINES["producer_seconds"]):
        raise BootstrapBlocked("producer_deadline_not_10800")
    read_preregistration()
    raise BootstrapBlocked(BLOCKER)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BootstrapBlocked as exc:
        print("R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_BLOCKED " +
              str(exc), file=sys.stderr, flush=True)
        raise SystemExit(78)
