# Luna task 405: A0 low-memory resume from run 33267817818

Role: Luna implementation/compute support.  Do not change mathematics or the
search order.  The parent broker alone will commit, push, and dispatch.

## Frozen input

- source run: `33267817818`
- immutable head: `8227ecd4cb12f7efc8e2419306b847e228a78f36`
- artifact id/name: `9721440597` / `gap-run-out`
- checkpoint member:
  `d972_r07_history_free_positive_fast_resume_v24_checkpoint.json`
- checkpoint bytes: `1663424241`
- checkpoint SHA-256:
  `55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d`
- producer/checker terminal:
  `UNKNOWN_RESOURCE:phase=positive_boundary_correlation_cap=wall_seconds_value=10800.554579397001_limit=10800.0`
- restored mathematical frontier must bind exactly:
  `boundary_pairs=22912880`, `retained_columns=8727`,
  `dag_node_allocations=29336`, `candidate_words=0`,
  `next_clean_boundary_epoch=8728`.

## Problem to fix, and only this problem

The v21--v23 logical resume path accepts the checkpoint, but
`read_bounded_json` currently accumulates the full 1.66 GB file, copies it to
`bytes`, decodes it to one giant string, and then materializes the whole JSON.
That is an unacceptable OOM risk on a standard GHA runner.  A fresh rerun is
deterministic and would merely repeat the same frontier.

Implement a versioned successor which restores this exact canonical sealed
checkpoint with bounded peak memory.  Parse/inject large `new_records` (and
any other dominant array) incrementally and release each raw record after it
has been authenticated and injected.  Do not weaken the existing source,
basis, DAG, current-dual, counter, cleanup, heavy-identity, seal, or physical
file checks.  If the existing top-level canonical seal cannot be checked
incrementally without a new transport envelope, introduce a small separately
sealed manifest that pins the raw member bytes/SHA and retain all semantic
checks on streamed fields.  Fail closed on duplicate/missing/out-of-order
top-level fields and malformed JSON.

The restored in-memory reducer necessarily remains large; the goal is to
remove only avoidable whole-file byte/string/DOM copies.  Preserve v23's
pre-heavy replacement-worker lifecycle and every search/resource/order rule.

## GHA transport

The generic `gap-run.yml` cannot authenticate/download a prior-run artifact.
Create a new versioned A0-only workflow candidate which:

1. checks out the dispatched immutable head;
2. downloads the exact same-repository run/name using a pinned
   `actions/download-artifact` action and `github.token`;
3. requires the exact checkpoint basename, bytes, and SHA above before the
   producer starts;
4. runs the versioned producer in RESUME mode for the existing 10,800-second
   internal budget, with visible periodic progress;
5. runs the matching independent checker on every typed terminal; and
6. uploads the new checkpoint/receipt/logs under `if: always()` with enough
   workflow headroom for compression.

Do not touch the generic workflow.  Do not dispatch.  The parent will review
the new workflow because workflow edits require parent/commander approval.

## Required gates

- Static frozen-owner and source-cardinality assertions.
- A small local fixture proving the streaming reader accepts a valid sealed
  checkpoint and rejects at least: byte/SHA mismatch, seal mutation,
  duplicate/missing top-level key, reordered/duplicate `new_records`, bad DAG
  binding, and wrong restored counter.  Do not run production locally.
- Estimate/report peak avoidable parser memory and explain why the previous
  full-DOM path is no longer reachable in production resume mode.
- Report exact changed paths, bytes, SHA-256, commands, and expected dispatch
  inputs in `sol/luna_reply_405_r07_a0_streaming_resume_transport_v25.md`.

Allowed edits are the new versioned producer/checker/driver/workflow files and
that reply only.  Preserve all unrelated dirty-tree state.
