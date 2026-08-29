#!/usr/bin/env python3
"""Independent A4 v15 checker: frozen v14 plus early row checkpoints.

The checker restores the exact v14 generated source without importing the
producer.  Only checkpoint-prefix handling, the v13 producer identity, and
bounded progress reporting are patched; the mathematical oracle is unchanged.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v14.py")
OWNER_BYTES = 8074
OWNER_SHA256 = "7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47"

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v12.py"',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v13.py"',
    ),
    (
        b'''def progress_once(meter: Meter, phase: str, row: int) -> None:\n    now = time.monotonic()\n    if now - getattr(meter, "_a4_progress_at", -1.0e99) < 60.0: return\n    meter._a4_progress_at = now\n    counters = meter.counters\n    print(f"A4_PROGRESS phase={phase} row={int(row)} membership_queries={counters.get('membership_queries', 0)} correlation_pairs={counters.get('correlation_pairs', 0)} elapsed={now - meter.started:.1f}", flush=True)\n''',
        b'''def progress_once(meter: Meter, phase: str, row: int,\n                  combined_rank: int | None = None, boundary_rank: int | None = None,\n                  k_rank: int | None = None, accepted_batch_size: int | None = None) -> None:\n    if combined_rank is not None: meter._a4_combined_rank = int(combined_rank)\n    if boundary_rank is not None: meter._a4_boundary_rank = int(boundary_rank)\n    if k_rank is not None: meter._a4_k_rank = int(k_rank)\n    if accepted_batch_size is not None: meter._a4_last_batch = int(accepted_batch_size)\n    now = time.monotonic()\n    if now - getattr(meter, "_a4_progress_at", -1.0e99) < 60.0: return\n    meter._a4_progress_at = now\n    meter._sync(); counters = meter.counters\n    print(f"A4_PROGRESS phase={phase} current_row={int(row)} completed_row={int(getattr(meter, '_a4_completed_row', 0))} combined_rank={int(getattr(meter, '_a4_combined_rank', 0))} boundary_rank={int(getattr(meter, '_a4_boundary_rank', 0))} K_rank={int(getattr(meter, '_a4_k_rank', 0))} correlation_rounds={int(getattr(meter, '_a4_correlation_rounds', 0))} accepted_batch_size={int(getattr(meter, '_a4_last_batch', 0))} elapsed={meter.wall_base + now - meter.started:.1f} rss_bytes={int(meter.peak_counters.get('rss_bytes', 0))} durable_checkpoint_row={int(getattr(meter, '_a4_durable_row', 0))} membership_queries={counters.get('membership_queries', 0)} correlation_pairs={counters.get('correlation_pairs', 0)}", flush=True)\n''',
    ),
    (
        b'    meter.reserve("correlation_pairs", expected_pairs, "checker.full_D_correlation")',
        b'    meter._a4_correlation_rounds = int(getattr(meter, "_a4_correlation_rounds", 0)) + 1\n    meter.reserve("correlation_pairs", expected_pairs, "checker.full_D_correlation")',
    ),
    (
        b'''                          "accumulator_digest": correlation["accumulator_digest"]}; self.record(result); continue\n            q, c = self.basis.expand_correction(correction)''',
        b'''                          "accumulator_digest": correlation["accumulator_digest"]}; self.record(result)\n                progress_once(self.meter, "CORRELATION", int(getattr(self.meter, "_a4_current_row", 0)),\n                              self.basis.rank(), len(self.basis.bspace.pivots),\n                              len(self.basis.k_items), 1)\n                continue\n            q, c = self.basis.expand_correction(correction)''',
    ),
    (
        b'''                      "correlation_complete": correlation.get("complete") is True}; self.record(result); return result\n\n    def record(self, value: dict[str, Any]) -> None:''',
        b'''                      "correlation_complete": correlation.get("complete") is True}; self.record(result)\n            progress_once(self.meter, "CORRELATION", int(getattr(self.meter, "_a4_current_row", 0)),\n                          self.basis.rank(), len(self.basis.bspace.pivots),\n                          len(self.basis.k_items), 0)\n            return result\n\n    def record(self, value: dict[str, Any]) -> None:''',
    ),
    (
        b'''    if resume_state is not None:\n        require((not chunks and resume_row == 1) or\n                (chunks and int(chunks[-1]["end"]) == resume_row - 1),\n                "checker:checkpoint_row_chunk_cursor")\n        chunk_start = 1 if not chunks else int(chunks[-1]["end"]) + 1\n        require(chunk_start == resume_row, "checker:checkpoint_row_chunk_next_start")''',
        b'''    if resume_state is not None:\n        canonical_ends = (1024, 2048, 3072, 4096, 5120, 6144, ROWS)\n        expected_ends = [end for end in canonical_ends if end < resume_row]\n        require([int(chunk.get("end", 0)) for chunk in chunks] == expected_ends,\n                "checker:checkpoint_row_chunk_cursor")\n        chunk_start = 1 if not chunks else int(chunks[-1]["end"]) + 1\n        require(chunk_start <= resume_row, "checker:checkpoint_row_chunk_next_start")''',
    ),
    (
        b'''    def consume_row(ordinal: int, row: dict[str, Any]) -> None:\n        meter.check("CHECKER_ROW_" + str(ordinal)); progress_once(meter, "ROW", ordinal); source_word, parts, ancestry = replay_ancestry(row)''',
        b'''    def consume_row(ordinal: int, row: dict[str, Any]) -> None:\n        nonlocal chunk_start\n        meter._a4_current_row = ordinal\n        meter.check("CHECKER_ROW_" + str(ordinal)); progress_once(meter, "ROW", ordinal); source_word, parts, ancestry = replay_ancestry(row)''',
    ),
    (
        b'''            node = words.source(source_word); accept_k(oracle, arithmetic, boundary, words, query, node, f"K:{len(oracle.basis.k_items)}")\n            queue.append(len(oracle.basis.k_items) - 1)\n        if checkpoint is not None''',
        b'''            node = words.source(source_word); accept_k(oracle, arithmetic, boundary, words, query, node, f"K:{len(oracle.basis.k_items)}")\n            queue.append(len(oracle.basis.k_items) - 1)\n        meter._a4_completed_row = ordinal\n        progress_once(meter, "ROW_COMPLETE", ordinal, oracle.basis.rank(),\n                      len(oracle.basis.bspace.pivots), len(oracle.basis.k_items),\n                      int(getattr(meter, "_a4_last_batch", 0)))\n        if checkpoint is not None''',
    ),
    (
        b'ordinal in {32, 64, 128, 256, 512, 1024, 2048, 3072, 4096, 5120, 6144, ROWS}',
        b'ordinal in {4, 8, 12, 16, 20, 24, 28, 32, 64, 128, 256, 512, 1024, 2048, 3072, 4096, 5120, 6144, ROWS}',
    ),
    (
        b'''        meter.install_completed(meter.pending_completed_counters, dict(meter.restore_validation_counters),\n                                meter.pending_saved_peak)\n        checkpoint_writes_enabled = True''',
        b'''        meter.install_completed(meter.pending_completed_counters, dict(meter.restore_validation_counters),\n                                meter.pending_saved_peak)\n        meter._a4_completed_row = resume_row - 1\n        meter._a4_current_row = resume_row\n        meter._a4_durable_row = resume_row - 1\n        meter._a4_correlation_rounds = len(oracle.dual_chain)\n        checkpoint_writes_enabled = True''',
    ),
    (
        b'''            parent = oracle.basis.k_items[queue[cursor]]; cursor += 1; meter.check("CHECKER_K_QUEUE_" + str(cursor)); progress_once(meter, "K_QUEUE", cursor)''',
        b'''            parent = oracle.basis.k_items[queue[cursor]]; cursor += 1; meter.check("CHECKER_K_QUEUE_" + str(cursor))\n            progress_once(meter, "K_QUEUE", ROWS, oracle.basis.rank(),\n                          len(oracle.basis.bspace.pivots), len(oracle.basis.k_items),\n                          int(getattr(meter, "_a4_last_batch", 0)))''',
    ),
    (
        b'    write_checkpoint_snapshot(path, meter, make_body, "checker.checkpoint_serialize")',
        b'    write_checkpoint_snapshot(path, meter, make_body, "checker.checkpoint_serialize")\n    meter._a4_durable_row = max(0, min(ROWS, int(next_row) - 1))',
    ),
    (
        b'    require(prior_end == len(row_prefix), "checker:checkpoint_row_chunk_cursor")',
        b'''    expected_ends = [end for end in (1024, 2048, 3072, 4096, 5120, 6144, ROWS)\n                     if end <= len(row_prefix)]\n    require([int(chunk.get("end", 0)) for chunk in chunks] == expected_ends and\n            prior_end <= len(row_prefix), "checker:checkpoint_row_chunk_cursor")''',
    ),
    (
        b'''    require(value.get("rebuild_digest") == checkpoint_state_digest(value),\n            "checker:checkpoint_rebuild_digest")\n    return value''',
        b'''    require(value.get("rebuild_digest") == checkpoint_state_digest(value),\n            "checker:checkpoint_rebuild_digest")\n    meter._a4_durable_row = int(value.get("next_row", 1)) - 1\n    meter._a4_completed_row = int(value.get("next_row", 1)) - 1\n    return value''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v15 checker: frozen v14 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v14_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    source = owner_ns["SOURCE"]
    raw = source.read_bytes()
    if len(raw) != owner_ns["SOURCE_BYTES"] or hashlib.sha256(raw).hexdigest() != owner_ns["SOURCE_SHA256"]:
        raise SystemExit("v15 checker: frozen v6 source drift")
    for old, new in owner_ns["PATCHES"]:
        if raw.count(old) != 1:
            raise SystemExit("v15 checker: v14 restoration cardinality")
        raw = raw.replace(old, new)
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v15 checker: audited site is not unique")
        raw = raw.replace(old, new)
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(OWNER), "exec"), ns, ns)


if __name__ == "__main__":
    main()
