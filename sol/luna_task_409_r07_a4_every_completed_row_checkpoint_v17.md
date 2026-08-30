# Luna task 409 — A4 every-completed-row checkpoint v17

Role: Luna implementation/fixture only.  Do not dispatch GHA, commit, push,
or run production locally.

## Incident

GHA run `33274918945`, head
`ff91a7b1e21a42b278af854ca9511587a05b55fe`, ended with producer
`UNKNOWN_RESOURCE` at the 14,400-second cap.  It resumed from the sealed
producer checkpoint with `next_row=25`, completed rows 25 and 26, and entered
row 27, but the terminal checkpoint again has `next_row=25` because frozen
v13/v16 writes early checkpoints only at row 24 and then row 28.  Thus four
hours of completed-row work were not durable.  The receipt reports
`durable_checkpoint_row=24`, `completed_row=26`, and `current_row=27`.

This is a checkpoint-cadence repair only.  Do not alter the oracle,
correlation, batch-64 selection, row order, arithmetic, or resource limits.

## Required versioned files

Read producer v16, checker v22, and GHA driver v30.  Create only:

1. `search/d972_r07_word_independent_successor_kernel_v17.py`;
2. `crosscheck/check_d972_r07_word_independent_successor_kernel_v23.py`;
3. `search/d972_r07_word_independent_successor_kernel_gha_driver_v31.g`;
4. reply `sol/luna_reply_409_r07_a4_every_completed_row_checkpoint_v17.md`.

Do not modify any existing file.

## Exact repair

- Producer v17 must be a hash-pinned minimal successor of v16.
- After **every fully completed input row**, atomically write a replayable
  checkpoint whose `next_row=ordinal+1`; no checkpoint is written for a
  partially processed row.
- Preserve the existing queue-phase checkpoint schedule after all 6,441
  rows.
- The already sealed v16 checkpoint (25,581 bytes, SHA-256
  `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445`,
  `next_row=25`) must be accepted only as an explicitly pinned one-way legacy
  migration.  New v17 checkpoints bind the v17 code identity and must resume
  without a migration ambiguity.
- Preserve the small compact checkpoint representation.  Do not serialize a
  large rebuilt boundary matrix or add a SELFTEST production phase.
- Checker v23 should be the smallest pin/identity successor needed for v17;
  it must retain the existing independent arithmetic and terminal rules.
- Driver v31 stays in RESUME mode, embeds/seeds the exact existing producer
  and checker checkpoints used by v30, pins the new files, and keeps the same
  14,400-second mathematical cap.  Output names/marker must be versioned.

## Lightweight gates

Use a tiny fixture beginning at `next_row=25` which completes rows 25 and 26
and then injects a resource stop inside row 27.  Require the terminal
checkpoint to have `next_row=27`, and require resume to begin at row 27.
Mutate `next_row`, the self seal, and the legacy code identity independently
and require rejection.  Also run compile/help/generated-source pin, ASCII/GAP
parse, and driver pin checks.  No 45 MB/31 MB authority inputs and no heavy
row arithmetic locally.

Report exact bytes/SHA-256 and commands/results.

