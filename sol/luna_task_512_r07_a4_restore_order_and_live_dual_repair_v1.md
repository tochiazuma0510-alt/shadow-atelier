# Task 512 -- minimal A4 physical-resume ordering and live-dual repair

Role: Luna implementation/fixture engineer.  This is a deliberately narrow
successor to Task503.  Do not redesign the A4 search, run the 6,441-row
production, dispatch GHA, edit workflow files, commit/push, or touch unrelated
files.  Write only the three versioned implementation files and the reply
listed below.

Read fully:

1. `sol/luna_task_503_r07_a4_actual_production_shard_wiring_v1.md` and
   `sol/luna_reply_503_r07_a4_actual_production_shard_wiring_v1.md`;
2. Task503 frozen subjects:
   - `search/d972_r07_word_independent_successor_kernel_v24.py`, 34535 /
     `8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe`;
   - `crosscheck/check_d972_r07_word_independent_successor_kernel_v33.py`,
     24033 / `44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf`;
   - `search/d972_r07_word_independent_successor_kernel_gha_driver_v43.g`,
     15449 / `36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb`;
3. `sol/sol_reply_511_audit_r07_a4_actual_production_shard_wiring_v1.md`
   when present.  Task511's decisive live-path counterexample is controlling.

Task511 reproduced two load-bearing defects in generated v24 after three real
closed physical shards and an actual `build_kernel` resume:

- `physical_store.direct_restore(...)` first installed the last shard's
  semantic counters, then inherited `meter.install_completed(...)` reset them
  to the ordinary row-26 values.  The fourth shard consequently began with
  `semantic_before != shard3.semantic_after`.
- direct restore appended one item to `oracle.live_duals` for every closed
  shard, even though the shards are successive batches of one still-open
  query.  The bounded live route observed historical count 1 becoming 4;
  uninterrupted execution retains the one query-level live-dual entry.

Produce exactly:

- `search/d972_r07_word_independent_successor_kernel_v25.py`;
- `crosscheck/check_d972_r07_word_independent_successor_kernel_v34.py`;
- `search/d972_r07_word_independent_successor_kernel_gha_driver_v44.g`;
- `sol/luna_reply_512_r07_a4_restore_order_and_live_dual_repair_v1.md`.

## Required minimal repair

R1. Pin v24/generated-v24 exactly and patch exact-cardinality anchors.  Keep
the early physical-chain/ordinary-row binding check, but do not apply physical
state before ordinary checkpoint rebuild/authentication and completed-counter
installation.  Invoke direct physical restore exactly once immediately after
the successful ordinary `meter.install_completed(...)`, before correlation
round counts, delta-tracker initialization, or any new query work.  Thus the
last physical shard's `semantic_after` is the live counter state when the
fourth batch begins.

R2. Direct restore must preserve the one query-level `oracle.live_duals`
history from the ordinary checkpoint.  Do not append a `live_duals` entry per
physical batch.  Restore the batch-level `oracle.dual_chain` events exactly
once, along with admitted basis rows/formals, records, insertion/query events,
epoch, and the last physical semantic counters.  Do not recompute reductions,
correlations, boundary rows, or raw candidates while restoring.

R3. Do not change the candidate roster, `m=min(64,len(private_candidates))`,
accepted mask, arithmetic, row order, resource caps, terminal meanings,
ordinary row-26 transport, or the Task503 physical schema.  No new snapshot,
cumulative prefix rewrite, dense conversion, worker pool, retry, SELFTEST in
production, or extra closure.

R4. V34 must remain independent of v25 and validate the corrected live
contract.  Add a bounded actual-call-path fixture which creates three genuine
closed shards for one open query, interrupts, enters generated
`build_kernel`/CLI resume, and reaches the fourth close.  It must assert at
least:

- shard4 `semantic_before ==` shard3 `semantic_after` in every semantic key;
- restored `live_duals` equals the uninterrupted route and is not increased
  by the number of physical shards;
- physical direct restore call count is exactly one;
- no insert/reduce/correlate/raw-boundary replay occurs for admitted shard
  entries;
- restored maps/formals/records/batch dual events/epoch equal uninterrupted
  state before new work;
- a fully re-sealed counter-order or duplicated-live-dual mutation is rejected.

The fixture must exercise the generated live call sites, not only a helper.
Retain all Task503 independent mutation and ordinary-positive gates.  Bound
every fixture; do not execute the production universe.

R5. V44 must pin v25, generated v25, v34, generated v34, and the same immutable
row-26 release/members as v43.  Preserve v43's reached shell, fresh paths,
pipefail, single producer, RESOURCE-no-checker rule, positive-only single
checker, 14,400-second/8-GB internal caps, external margin, typed terminals,
and false A0/fake/Ihara claims.  Change no workflow.

## Acceptance

Run only bounded source-pin, AST/generated-call-path, fixture/mutation, and GAP
`ReadAsFunction`/reached-shell checks.  Freeze nonzero wrapper-local generated
pins.  The reply must list exact bytes/SHA-256 for all three files and both
generated sources, commands/results, the live four-batch equality evidence,
and the marker:

`TASK512_R07_A4_RESTORE_ORDER_AND_LIVE_DUAL_REPAIR_PASS`

If the minimal repair cannot satisfy this contract, stop and report the exact
blocker instead of broadening the architecture.
