# Luna task 383 - A4 early checkpoint and bounded column-batch hot path v1

Commissioner: Sol / 2026-08-30

Reply to `sol/luna_reply_383_r07_a4_early_checkpoint_batch_hotpath_v1.md`.

Role: urgent bounded mechanical implementation.  Parent Sol owns mathematics,
git, network, GHA dispatch and promotion.  Read in full:

```text
search/d972_r07_word_independent_successor_kernel_v6.py
search/d972_r07_word_independent_successor_kernel_v12.py
crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py
crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py
search/d972_r07_word_independent_successor_kernel_gha_driver_v21.g
```

The triggering production evidence is run `33250865356`: producer terminal
`UNKNOWN_RESOURCE`, reason
`echelon_reduce:wall_seconds:14402.179492432>14400`, 27 completed rows,
28,037 boundary rank rises, 30,660,320 correlation pairs, peak RSS
3,885,568,000 bytes.  Its sealed producer checkpoint has `next_row=1`, empty
row/basis state and is only the prefrontier checkpoint.  It cannot preserve
the completed 27-row work.  Do not call workflow success a mathematical
success and do not treat that checkpoint as useful continuation data.

Edit only these four new files:

```text
search/d972_r07_word_independent_successor_kernel_v13.py
crosscheck/check_d972_r07_word_independent_successor_kernel_v15.py
search/d972_r07_word_independent_successor_kernel_gha_driver_v22.g
sol/luna_reply_383_r07_a4_early_checkpoint_batch_hotpath_v1.md
```

Do not edit predecessors, workflows, proofs, v220, ledgers, certs, fixtures or
inputs.  Do not run production, GHA, git, network, SELFTEST or a mutation
campaign.  Static Python compile, ASCII scan, frozen-owner restoration and
GAP `ReadAsFunction` parsing are allowed.  No framework rewrite.

## 1. Required early durable progress

Patch the producer and checker so a natural completed-row boundary is sealed
well before row 27.  Use a small deterministic cadence such as rows
`4,8,12,...,32`, then a geometrically/sparsely increasing cadence which stays
within the existing additive checkpoint-byte cap.  Preserve atomic sealing,
exact counters, authority identity, code identity, row/bridge digest prefixes,
basis/word ancestry and queue state.  Never serialize a half-mutated oracle
query.

The first production run of v13/v15 will be FRESH because the v12/v14
checkpoint code pins differ.  Every later resource stop must be genuinely
resumable from the last completed-row checkpoint.  The driver must support
both PRODUCTION and RESUME with the same exact behavior as v21/v6, preserve
UNKNOWN artifacts, and print the diagnostic tails; do not require a positive
sentinel merely to upload a resource checkpoint.

## 2. Bounded exact hot-path change

The current oracle performs one full dual-correlation scan, inserts only the
lexicographically first nonzero boundary translate, and repeats.  The run
needed 28,037 scans/rises for 27 rows.  Implement one bounded deterministic
batch per already-complete correlation accumulator:

1. retain the complete ordered nonzero candidate list produced by the same
   exact accumulator;
2. try candidates in canonical order, at most a small fixed cap (recommended
   32 or 64) per correlation round;
3. before insertion, reduce each candidate against the *current combined
   basis*; skip it if it became dependent after an earlier batch insertion;
4. insert only genuine boundary columns with the existing literal ledger,
   basis and counter ownership;
5. record every accepted insertion and its parent-correlation ancestry; and
6. recompute the target remainder/dual after the bounded batch.

Adding an authenticated boundary column is mathematically safe; silently
adding a combined-dependent column or deleting/replacing a K row is not.
Do not weaken full correlation completeness, dual checks, terminal semantics,
queue exhaustion, word ancestry, or independent acceptance.  If a clean
batch cannot be expressed without changing mathematical semantics, retain
the early-checkpoint repair and report the exact batch blocker instead of a
large rewrite.

The independent checker must implement the same mathematical batching with
a different deterministic candidate order and pivot order, and compare final
spaces/ancestries rather than requiring identical batch histories.  It must
not import the producer.

## 3. Observability and resource truth

Keep progress bounded and useful: at least completed row, current combined/
boundary/K ranks, correlation-round count, accepted batch size, elapsed time,
RSS and last durable checkpoint row.  Throttle to at most one line per minute.
Do not add audit-only computation to obtain progress.

Preserve the registered 14,400-second and 8-GB internal limits.  Resource
stop remains `UNKNOWN_RESOURCE`.  A mathematical pass still requires all
6,441 rows, exhausted action queue and independent acceptance.

## 4. Delivery

Use thin frozen wrappers when possible.  Record exact base bytes/SHA, every
unique patch site, static commands, checkpoint cadence, batch cap, expected
speed mechanism and any residual risk.  End with:

```text
RUN 33250865356 MATHEMATICAL TERMINAL:            UNKNOWN_RESOURCE
EARLY COMPLETED-ROW CHECKPOINT:                   IMPLEMENTED
BOUNDED EXACT COLUMN BATCH:                       IMPLEMENTED OR EXACTLY BLOCKED
FUTURE RESOURCE STOP RESUMABLE:                   YES AFTER FIRST V13 CHECKPOINT
A4 ACCEPTED WORD-BEARING K:                       NOT YET COMPUTED
```

`TASK383_A4_EARLY_CHECKPOINT_BATCH_HOTPATH_COMMISSIONED`
