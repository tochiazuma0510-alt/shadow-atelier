#!/usr/bin/env python3
"""
drophunt_checker_batch_runner_v1.py -- item4 (裁定1781): chunked runner for
the independent Python checker (drophunt_checker_v3.py) over the full
716-receipt population (358 windows x {row36,row71}) that the real launch
will produce. Falsifier-measured ratio: GAP-side full 358-window sweep
<1min (max window 266ms), but checker-side verification is far more
expensive (homomorphism-tracked chain construction per receipt) -- ~1.7h
total estimated for all 716. This script chunks that work into resumable
batches with a JSON checkpoint (processed receipt paths + PASS/FAIL
verdicts + error details), so no single invocation needs to run anywhere
near 1.7h uninterrupted (matches the house 10-minute-chunk discipline).

Usage:
  python search/drophunt_checker_batch_runner_v1.py <receipt_glob_or_dir> \
      --checkpoint <path.json> [--batch-size N] [--time-budget-seconds S]

Each invocation processes receipts (in a DETERMINISTIC sorted order) until
either batch-size receipts have been checked or the time budget is
exceeded, whichever comes first, then writes the checkpoint and exits
cleanly (status 0). Re-invoking with the SAME checkpoint path resumes from
the first not-yet-processed receipt. A final summary (PASS/FAIL counts,
list of FAIL paths+errors) is always available by reading the checkpoint
file itself -- no separate "final report" step is required.

Explorer/checker separation note: this file imports ONLY
drophunt_checker_v3.check_receipt (the existing, already-independent
checker) -- it adds no new verification logic of its own, only chunking/
checkpointing plumbing around calls to that function.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drophunt_checker_v3 as checker  # noqa: E402


def load_checkpoint(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"processed": {}, "order": []}


def write_checkpoint(path: str, state: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=True, indent=2, sort_keys=True)
    os.replace(tmp, path)  # atomic on the same filesystem


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt_glob", help="glob pattern or directory of receipts to check")
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--batch-size", type=int, default=40)
    ap.add_argument("--time-budget-seconds", type=float, default=480.0)
    args = ap.parse_args(argv)

    if os.path.isdir(args.receipt_glob):
        paths = sorted(glob.glob(os.path.join(args.receipt_glob, "*.json")))
    else:
        paths = sorted(glob.glob(args.receipt_glob))

    if not paths:
        print(f"NO_RECEIPTS_MATCHED pattern={args.receipt_glob}", file=sys.stderr)
        return 2

    state = load_checkpoint(args.checkpoint)
    if not state.get("order"):
        state["order"] = paths
        state["processed"] = {}
    elif state["order"] != paths:
        # fail-closed: the receipt population changed since the checkpoint
        # was written (a new receipt appeared, one vanished, or the glob's
        # sort order differs). Refuse to silently continue against a
        # different population than the checkpoint was built for.
        print("CHECKPOINT_POPULATION_MISMATCH: the receipt list differs from "
              "the checkpoint's recorded order -- refusing to resume "
              "(delete the checkpoint to start fresh if this is intentional)",
              file=sys.stderr)
        return 3

    t0 = time.time()
    processed_this_run = 0
    for p in state["order"]:
        if p in state["processed"]:
            continue
        if processed_this_run >= args.batch_size:
            break
        if time.time() - t0 > args.time_budget_seconds:
            print(f"TIME_BUDGET_EXCEEDED after {processed_this_run} receipts this run")
            break
        result = checker.check_receipt(p)
        state["processed"][p] = {"status": result["status"], "errors": result.get("errors", [])}
        processed_this_run += 1
        write_checkpoint(args.checkpoint, state)  # per-receipt checkpoint (item2's discipline, reused here)
        print(f"CHECKED {p} status={result['status']} "
              f"({len(state['processed'])}/{len(state['order'])} total)")

    total = len(state["order"])
    done = len(state["processed"])
    fails = {p: v for p, v in state["processed"].items() if v["status"] != "PASS"}
    print(f"BATCH_RUN_COMPLETE processed_this_run={processed_this_run} "
          f"cumulative={done}/{total} fails={len(fails)}")
    if done == total:
        print(f"ALL_RECEIPTS_CHECKED total={total} pass={total - len(fails)} fail={len(fails)}")
        if fails:
            for p, v in fails.items():
                print(f"FAIL {p}: {v['errors']}")
    return 0 if not fails or done < total else (1 if fails else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
