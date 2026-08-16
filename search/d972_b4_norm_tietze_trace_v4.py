#!/usr/bin/env python3
"""Versioned 100-step canonical norm/Tietze producer.

The frozen v2 producer is run for exactly 100 elementary eliminations.  The
receipt is transport-only; the independent v3 checker and v4 KBMAG consumer
remain mandatory.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "search" / "d972_b4_norm_tietze_trace_v2.py"
BASE_SHA256 = "5ec4602524ff470e4b62b7625177481c22f087ab058c85a5bd53276967fad67f"
SCHEMA = "d972-b4-norm-tietze-trace/v4"
BASE_SCHEMA = "d972-b4-norm-tietze-trace/v2"
MAX_STEPS = 100
DENSE_LIMIT = 61
EXPECTED_FINAL_RELATORS_SHA256 = (
    "2327388540e9095b2c7ca9b6d0d1f9de2295e3400b0430bdf97b672d02ce745"
)
EXPECTED_FINAL_NORMS_SHA256 = (
    "325aecb390f4c8107a92be3cca8ed16f396f1baec49b973488f8822b43bf4d70"
)


def load_base() -> Any:
    raw = BASE_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA256:
        raise ValueError("frozen v2 producer SHA drift")
    spec = importlib.util.spec_from_file_location("d972_ntz_v2_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load frozen v2 producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--word-artifact", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    base = load_base()
    if args.selftest:
        if base.main(["--selftest"]) != 0:
            raise AssertionError("frozen v2 producer selftest failed")
        print("D972_NORM_TZ_V4_PRODUCER_SELFTEST_PASS base_sha256=" + BASE_SHA256)
        return 0
    if args.output is None:
        parser.error("--output is required unless --selftest is supplied")
    if args.input is None or args.word_artifact is None:
        parser.error("--input and --word-artifact are required unless --selftest is supplied")
    output = args.output.resolve()
    temporary = output.with_name(output.name + ".v2base.tmp")
    try:
        rc = base.main([
            "--input", str(args.input.resolve()),
            "--word-artifact", str(args.word_artifact.resolve()),
            "--max-steps", str(MAX_STEPS),
            "--output", str(temporary),
        ])
        if rc != 0:
            raise RuntimeError("frozen v2 producer returned nonzero")
        receipt = json.loads(temporary.read_text(encoding="utf-8"))
        if receipt.get("schema") != BASE_SCHEMA:
            raise ValueError("base producer schema drift")
        if receipt.get("max_steps") != MAX_STEPS or len(receipt.get("events", [])) != MAX_STEPS:
            raise ValueError("100-step trace was not completed")
        if receipt.get("final_generator_count") != DENSE_LIMIT:
            raise ValueError("100-step final generator count drift")
        if receipt.get("final_relators_sha256") != EXPECTED_FINAL_RELATORS_SHA256:
            raise ValueError("100-step final relator digest drift")
        if receipt.get("final_norm_words_sha256") != EXPECTED_FINAL_NORMS_SHA256:
            raise ValueError("100-step final norm digest drift")
        receipt["schema"] = SCHEMA
        receipt["trace_base_schema"] = BASE_SCHEMA
        receipt["trace_base_sha256"] = BASE_SHA256
        receipt["max_steps"] = MAX_STEPS
        receipt["dense_target_max_generators"] = DENSE_LIMIT
        receipt["versioned_lane"] = "v4-step100-dense61"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8")
        print(json.dumps({
            "schema": SCHEMA,
            "status": receipt["status"],
            "steps": len(receipt["events"]),
            "final_generators": receipt["final_generator_count"],
            "norm_empty": receipt["final_norm_empty_count"],
            "final_relators_sha256": receipt["final_relators_sha256"],
            "final_norm_words_sha256": receipt["final_norm_words_sha256"],
        }, sort_keys=True))
        return 0
    finally:
        if temporary.exists():
            temporary.unlink()


if __name__ == "__main__":
    raise SystemExit(run(__import__("sys").argv[1:]))
