#!/usr/bin/env python3
"""receipt_schema.py -- per-job receipt schema for the HS 発火条件4 GHA
機能較正(便104認可事項1, sol/sol_reply_104_math31.md F104-1.4)。

schema: hsp7-ci-calib-receipt/v1

必須フィールド(Sol F104-1.3の要求 -- run_id/run_attempt/commit/driver
digest を束縛):
  schema, lane, run_id, run_attempt, commit_sha, driver_digest,
  fixture_source_cert{path, sha256}, candidates[], overall_pass

このモジュールは書き出し(dict -> JSON file)・読み戻し(JSON file -> dict)
の対だけを提供する。GAP 実行そのものはこのモジュールの職務外(GHA
workflow 側が実行し、本モジュールで受け渡しする receipt を組み立てる)。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_TOP_FIELDS = (
    "schema",
    "lane",
    "run_id",
    "run_attempt",
    "commit_sha",
    "driver_digest",
    "fixture_source_cert",
    "candidates",
    "overall_pass",
)
REQUIRED_FIXTURE_SOURCE_FIELDS = ("path", "sha256")
REQUIRED_CANDIDATE_FIELDS = ("candidate", "expected_verdict", "observed_verdict", "agree")


class ReceiptSchemaError(Exception):
    pass


def build_receipt(
    *,
    lane: str,
    run_id: str,
    run_attempt: str,
    commit_sha: str,
    driver_digest: str,
    fixture_source_cert_path: str,
    fixture_source_cert_sha256: str,
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    for c in candidates:
        missing = [f for f in REQUIRED_CANDIDATE_FIELDS if f not in c]
        if missing:
            raise ReceiptSchemaError(f"candidate row missing fields {missing}: {c}")
    overall_pass = all(c["agree"] for c in candidates) and len(candidates) > 0
    receipt = {
        "schema": "hsp7-ci-calib-receipt/v1",
        "lane": lane,
        "run_id": run_id,
        "run_attempt": run_attempt,
        "commit_sha": commit_sha,
        "driver_digest": driver_digest,
        "fixture_source_cert": {"path": fixture_source_cert_path, "sha256": fixture_source_cert_sha256},
        "candidates": candidates,
        "overall_pass": overall_pass,
    }
    validate_receipt(receipt)
    return receipt


def validate_receipt(receipt: dict[str, Any]) -> None:
    missing = [f for f in REQUIRED_TOP_FIELDS if f not in receipt]
    if missing:
        raise ReceiptSchemaError(f"receipt missing top-level fields: {missing}")
    if receipt["schema"] != "hsp7-ci-calib-receipt/v1":
        raise ReceiptSchemaError(f"unexpected schema tag: {receipt['schema']!r}")
    fsc = receipt["fixture_source_cert"]
    missing_fsc = [f for f in REQUIRED_FIXTURE_SOURCE_FIELDS if f not in fsc]
    if missing_fsc:
        raise ReceiptSchemaError(f"fixture_source_cert missing fields: {missing_fsc}")
    if not isinstance(receipt["candidates"], list) or len(receipt["candidates"]) == 0:
        raise ReceiptSchemaError("candidates must be a non-empty list")
    for c in receipt["candidates"]:
        missing_c = [f for f in REQUIRED_CANDIDATE_FIELDS if f not in c]
        if missing_c:
            raise ReceiptSchemaError(f"candidate row missing fields {missing_c}: {c}")
    for req_field in ("run_id", "run_attempt", "commit_sha", "driver_digest"):
        if receipt[req_field] in (None, ""):
            raise ReceiptSchemaError(f"required binding field {req_field!r} is empty")


def write_receipt(receipt: dict[str, Any], path: Path) -> None:
    validate_receipt(receipt)
    # newline="\n" pins the on-disk bytes against platform line-ending
    # translation (Windows Path.write_text defaults to CRLF) so that
    # sha256/byte-identity checks are reproducible across OSes (this file
    # runs both on the developer's Windows box and on GHA's ubuntu-latest).
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def read_receipt(path: Path) -> dict[str, Any]:
    receipt = json.loads(path.read_text(encoding="utf-8"))
    validate_receipt(receipt)
    return receipt
