#!/usr/bin/env python3
"""R07 A0/v11 independent-checker bootstrap, fail-closed.

No v10 producer helper is imported.  The checker cannot issue a verdict until
the deterministic receipt/verdict pair is an exact preregistered owner.
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
TERMINALS = ("R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_SELFTEST_PASS",
             "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_COMMON_WORD",
             "UNKNOWN_INPUT", "UNKNOWN_RESOURCE")


class BootstrapBlocked(RuntimeError):
    pass


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def read_preregistration() -> dict[str, object]:
    try:
        value = json.loads(PREREGISTRATION.read_text(encoding="ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BootstrapBlocked("preregistration_owner_unreadable") from exc
    if (type(value) is not dict or
            value.get("schema") !=
            "d972-r07-history-free-positive-fast-resume/selftest-preregistration/v1"):
        raise BootstrapBlocked("preregistration_schema")
    if value.get("execution") != "UNEXECUTED" or value.get("status") != "BLOCKED":
        raise BootstrapBlocked("preregistration_execution_status")
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
    result.add_argument("--receipt", type=Path, required=True)
    result.add_argument("--verdict", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser().parse_args(argv)
    read_preregistration()
    raise BootstrapBlocked(BLOCKER)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BootstrapBlocked as exc:
        print("R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V11_BLOCKED " +
              str(exc), file=sys.stderr, flush=True)
        raise SystemExit(78)
