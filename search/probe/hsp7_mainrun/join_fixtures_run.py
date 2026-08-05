#!/usr/bin/env python3
"""join_fixtures_run.py -- runs search/probe/hsp7_mainrun/join_checker.py
against every fixture in join_fixtures_gen.FIXTURES, asserts the observed
verdict/reason matches the expected one declared alongside the fixture
builder, and writes a machine-readable results JSON
(search/certs 側で束ねる際の入力)。

Usage: python join_fixtures_run.py [--out PATH]
Exit code: 0 iff every fixture matched its expected verdict/reason; 1 otherwise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import join_checker  # noqa: E402
import join_fixtures_gen  # noqa: E402


def run_all() -> dict:
    join_fixtures_gen.write_all()
    rows = []
    all_pass = True
    canon_hashes = {}
    for name, (builder, expected_verdict, expected_reason) in join_fixtures_gen.FIXTURES.items():
        path = join_fixtures_gen.FIXTURE_DIR / f"{name}.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        result = join_checker.check_join(manifest)
        observed_verdict = result["verdict"]
        observed_reason = result.get("reason")
        ok_verdict = observed_verdict == expected_verdict
        ok_reason = (expected_reason is None) or (observed_reason == expected_reason)
        row_pass = ok_verdict and ok_reason
        all_pass = all_pass and row_pass
        row = {
            "fixture": name,
            "fixture_path": str(path.relative_to(HERE.parents[2])).replace("\\", "/"),
            "fixture_sha256": manifest_sha256,
            "expected_verdict": expected_verdict,
            "expected_reason": expected_reason,
            "observed_verdict": observed_verdict,
            "observed_reason": observed_reason,
            "observed_detail": result.get("detail"),
            "pass": row_pass,
        }
        if observed_verdict == "PASS":
            canon_hashes[name] = result["canonical_sort_hash"]
            row["canonical_sort_hash"] = result["canonical_sort_hash"]
        rows.append(row)

    reorder_matches_good = (
        "good" in canon_hashes and "reorder" in canon_hashes and canon_hashes["good"] == canon_hashes["reorder"]
    )
    all_pass = all_pass and reorder_matches_good

    return {
        "schema": "hsp7-join-checker-fixtures/v1",
        "checker_script": "search/probe/hsp7_mainrun/join_checker.py",
        "checker_script_sha256": hashlib.sha256((HERE / "join_checker.py").read_bytes()).hexdigest(),
        "fixture_generator_script": "search/probe/hsp7_mainrun/join_fixtures_gen.py",
        "fixture_generator_script_sha256": hashlib.sha256((HERE / "join_fixtures_gen.py").read_bytes()).hexdigest(),
        "rows": rows,
        "reorder_canonical_hash_matches_good": reorder_matches_good,
        "good_canonical_sort_hash": canon_hashes.get("good"),
        "reorder_canonical_sort_hash": canon_hashes.get("reorder"),
        "overall_pass": all_pass,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="write JSON results to this path")
    args = ap.parse_args()
    results = run_all()
    text = json.dumps(results, indent=2, ensure_ascii=False, sort_keys=False)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    return 0 if results["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
