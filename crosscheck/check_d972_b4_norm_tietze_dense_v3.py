#!/usr/bin/env python3
"""Independent checker for the 100-step/61-generator canonical receipt.

The producer is not imported.  This wrapper loads only the frozen v1 replay
checker after hashing it, changes its contract constants, and binds the
measured 100-step presentation digests.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "crosscheck" / "check_d972_b4_norm_tietze_dense_v1.py"
BASE_SHA256 = "10da50ccdc4291aaa81ed44a33c24d28926fba8ba45e9b2eb2d6d2cb7cf14388"
TRACE_SCHEMA = "d972-b4-norm-tietze-trace/v4"
CHECK_SCHEMA = "d972-b4-norm-tietze-dense-check/v3"
TRACE_BASE_SHA256 = "5ec4602524ff470e4b62b7625177481c22f087ab058c85a5bd53276967fad67f"
TRACE_BASE_SCHEMA = "d972-b4-norm-tietze-trace/v2"
TRACE_STEPS = 100
DENSE_LIMIT = 61
FINAL_RELATORS_SHA256 = (
    "2327388540e9095b2c7ca9b6d0d1f9de2295e3400b0430bdf97b672d02ce745"
)
FINAL_NORMS_SHA256 = (
    "325aecb390f4c8107a92be3cca8ed16f396f1baec49b973488f8822b43bf4d70"
)


def load_base() -> Any:
    raw = BASE_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA256:
        raise ValueError("frozen v1 checker SHA drift")
    spec = importlib.util.spec_from_file_location("d972_ntz_dense_v1_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load frozen v1 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.TRACE_SCHEMA = TRACE_SCHEMA
    module.CHECK_SCHEMA = CHECK_SCHEMA
    module.TRACE_STEPS = TRACE_STEPS
    module.DENSE_LIMIT = DENSE_LIMIT
    return module


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path, nargs="?")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--word-artifact", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    checker = load_base()
    if args.selftest:
        checker.selftest()
        print("D972_NORM_TZ_DENSE_V3_SELFTEST_PASS base_sha256=" + BASE_SHA256)
        return 0
    if args.trace is None or args.input is None or args.word_artifact is None or args.output is None:
        parser.error("trace, --input, --word-artifact and --output are required")
    trace_path = args.trace.resolve()
    trace_raw = trace_path.read_bytes()
    receipt = json.loads(trace_raw.decode("utf-8"))
    if receipt.get("schema") != TRACE_SCHEMA:
        raise ValueError("v4 trace schema missing")
    if receipt.get("trace_base_schema") != TRACE_BASE_SCHEMA or \
       receipt.get("trace_base_sha256") != TRACE_BASE_SHA256:
        raise ValueError("v4 trace base binding drift")
    if receipt.get("max_steps") != TRACE_STEPS or \
       receipt.get("dense_target_max_generators") != DENSE_LIMIT:
        raise ValueError("v4 trace settings drift")
    if receipt.get("final_relators_sha256") != FINAL_RELATORS_SHA256 or \
       receipt.get("final_norm_words_sha256") != FINAL_NORMS_SHA256:
        raise ValueError("v4 final digest drift")
    result = checker.validate_receipt(trace_path, args.input.resolve(),
                                      args.word_artifact.resolve())
    if result.get("schema") != CHECK_SCHEMA:
        raise ValueError("checker schema drift")
    if result.get("steps_replayed") != TRACE_STEPS or \
       result.get("final_generator_count") != DENSE_LIMIT:
        raise ValueError("checker step/generator gate failed")
    if result.get("final_relators_sha256") != FINAL_RELATORS_SHA256 or \
       result.get("final_norm_words_sha256") != FINAL_NORMS_SHA256:
        raise ValueError("checker final digest gate failed")
    result.update({
        "schema": CHECK_SCHEMA,
        "trace_schema": TRACE_SCHEMA,
        "checker_base_sha256": BASE_SHA256,
        "trace_base_sha256": TRACE_BASE_SHA256,
        "trace_base_schema": TRACE_BASE_SCHEMA,
        "versioned_lane": "v4-step100-dense61",
        "stock_kbmag_max_generators": 63,
    })
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n",
                      encoding="utf-8")
    print("D972_NORM_TZ_DENSE_V3_CHECK",
          f"status={result['status']}",
          f"steps={result['steps_replayed']}",
          f"final_generators={result['final_generator_count']}",
          f"norm_empty={result['final_norm_empty_count']}/972",
          f"output={output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, TypeError, ValueError, KeyError, IndexError,
            json.JSONDecodeError) as exc:
        print(f"D972_NORM_TZ_DENSE_V3_CHECK_ERROR {exc}", file=sys.stderr)
        raise SystemExit(2)
