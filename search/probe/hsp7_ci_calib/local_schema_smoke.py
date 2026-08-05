#!/usr/bin/env python3
"""local_schema_smoke.py -- 便104認可事項2(sol/sol_reply_104_math31.md
F104-1.4): 「同じ既知 fixture を使う local schema smoke」。

既知 fixture(Lane S, search/certs/hsp7_cond4_laneS_20260804.json、8候補)を
1shard分として使い、receipt_schema.py の build/write/read の往復が
ローカルで機能することだけを確認する。**これは GHA 上の実走ではない**
-- run_id/commit_sha はこの smoke 専用のプレースホルダ値であることを
receipt の note に明記する(GHA 実走の receipt と混同させない)。期待値は
Lane S cert から実行時に読み取る(コード非埋め込み)。

Usage: python local_schema_smoke.py [--out PATH]
Exit code: 0 iff round-trip succeeds and byte-identical + schema-valid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
REPO_ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

from receipt_schema import ReceiptSchemaError, build_receipt, read_receipt, write_receipt  # noqa: E402

LANE_S_CERT_PATH = REPO_ROOT / "search" / "certs" / "hsp7_cond4_laneS_20260804.json"


def run_smoke(out_path: Path) -> dict:
    cert_bytes = LANE_S_CERT_PATH.read_bytes()
    cert_sha256 = hashlib.sha256(cert_bytes).hexdigest()
    cert = json.loads(cert_bytes)

    # 期待値はcertから読み取る(コード非埋め込み)。cert自身が発火時の
    # 判定(hexagon_verdict)を保持している -- ここではその値を「期待値」
    # として receipt の candidates 行に転記するだけで、新たな判定は行わない
    # (local smokeはschema往復の確認が職務、数学的当否の再判定はしない)。
    rows = cert["lane_specific_results"]["hexagon_310_311_judgments"]
    candidates = []
    for row in rows:
        expected = row["hexagon_verdict"]
        candidates.append(
            {
                "candidate": row["candidate"],
                "expected_verdict": expected,
                "observed_verdict": expected,  # smoke: no fresh GAP run, round-trip only
                "agree": True,
            }
        )

    receipt = build_receipt(
        lane="S",
        run_id="LOCAL-SMOKE-NOT-A-GHA-RUN",
        run_attempt="0",
        commit_sha="LOCAL-SMOKE-PLACEHOLDER",
        driver_digest="LOCAL-SMOKE-PLACEHOLDER",
        fixture_source_cert_path=str(LANE_S_CERT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        fixture_source_cert_sha256=cert_sha256,
        candidates=candidates,
    )
    receipt["note"] = (
        "LOCAL SCHEMA SMOKE (not a GHA run) -- run_id/commit_sha/driver_digest are "
        "placeholders. observed_verdict is copied from the Lane S cert's own recorded "
        "hexagon_verdict (no fresh GAP execution here); this test validates only that "
        "the receipt schema round-trips through disk byte-identically."
    )

    write_receipt(receipt, out_path)
    written_bytes = out_path.read_bytes()
    read_back = read_receipt(out_path)
    read_back_bytes = json.dumps(read_back, indent=2, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n"

    roundtrip_byte_identical = written_bytes == read_back_bytes
    schema_valid = True
    schema_error = None
    try:
        read_receipt(out_path)
    except ReceiptSchemaError as e:
        schema_valid = False
        schema_error = str(e)

    result = {
        "smoke": "local_schema_smoke/v1",
        "shard_used": "Lane S (8 candidates)",
        "fixture_source_cert": {"path": str(LANE_S_CERT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"), "sha256": cert_sha256},
        "receipt_out_path": str(out_path),
        "receipt_out_sha256": hashlib.sha256(written_bytes).hexdigest(),
        "candidate_count": len(candidates),
        "roundtrip_byte_identical": roundtrip_byte_identical,
        "schema_valid_on_readback": schema_valid,
        "schema_error": schema_error,
        "overall_pass": roundtrip_byte_identical and schema_valid and receipt["overall_pass"],
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO_ROOT / "scratchpad" / "hsp7_ci_calib_local_smoke_receipt.json"))
    ap.add_argument("--result-out", default=None)
    args = ap.parse_args()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result = run_smoke(out_path)
    text = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=False)
    print(text)
    if args.result_out:
        Path(args.result_out).write_text(text + "\n", encoding="utf-8")
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
