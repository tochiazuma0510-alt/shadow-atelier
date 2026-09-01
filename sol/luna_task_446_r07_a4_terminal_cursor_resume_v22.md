# Luna task 446 — R07 A4 terminal-cursor continuation v22

Role: Luna implementation owner. This is a versioned two-cursor transport
repair after GHA run 33501732575. Do not overwrite Task443 files. Do not run
production, the 6,441-row computation, GHA, git commit, or push. Bounded
generation/static/synthetic checks only.

Read Task443's instruction/reply and v21/v27/v39 outputs in full. Read the
downloaded run artifact under
`%TEMP%/task443_run33501732575/gap-run-out/` in full, especially producer
HEAD, delta 00000001, result/verdict, and logs.

## Authorized outputs only

1. `search/d972_r07_word_independent_successor_kernel_v22.py`
2. `crosscheck/check_d972_r07_word_independent_successor_kernel_v28.py`
3. `search/d972_r07_word_independent_successor_kernel_gha_driver_v40.g`
4. `sol/luna_reply_446_r07_a4_terminal_cursor_resume_v22.md`

Temporary files stay outside the repository.

## Established input and exact scope

Run 33501732575 safely wrote exactly one row segment. Its authenticated HEAD
has `last_row=25`, `next_row=26`, `segment_count=1`; delta 00000001 has
`kind=row`, `ordinal=25`, one row digest, one bridge digest, and one R:25
record/event pair. The second segment was rejected before append/HEAD update
with `delta:one_row_terminal_pair`; row 26 is therefore not durable and must be
recomputed from the row-26 state.

The diagnosed defect is only this: after successful segment append and atomic
HEAD replacement, v21 advances row/bridge/oracle cursors but does not advance
the tracker fields for `initial_terminal_records` and
`initial_terminal_chain`. At row 26 those two slices therefore contain R:25
and R:26 while the ordinary oracle slice contains only R:26.

## Required repair

- Generate v22 as an exact wrapper successor to v21. In the successful
  post-HEAD tracker update, advance the two omitted terminal cursors by the
  exact lengths appended in the accepted segment body. Change nothing else.
- Preserve append-before-HEAD and tracker-after-HEAD order. A failed segment
  must not advance any tracker cursor.
- Add no scan, matrix copy, SELFTEST in production, changed checkpoint cadence,
  or arithmetic/gate/evaluator/queue modification.
- Generate v28 as the independent v27 successor pinning the exact v22
  producer and retaining the full segment/HEAD replay. Its bounded two-row
  toy must now assert that after accepting row 25 the second segment contains
  only row 26 in all four row/bridge/terminal pairs. Add a mutation that leaves
  either terminal cursor stale and ensure rejection. No arithmetic changes.
- Generate v40 as the v39 RESUME successor. Embed and exact-pin the immutable
  canonical base plus run 33501732575's accepted delta 00000001 and nonempty
  HEAD, reconstruct their exact versioned paths, and seed them fail-closed.
  Resume at `next_row=26`; never consume the rejected row-26 terminal/result as
  state. Existing identical files may pass the inherited seed gate; any drift
  or nonidentical target must stop.
- The v40 driver pins v22/v28, retains `D386Mode:="RESUME";;`, and contains no
  new production self-test or full reconstruction.

Report exact bytes/SHA for the three outputs and for the embedded base/delta1/
HEAD, generated-source diff confinement, two-row cursor test and mutation
outcomes, static driver reconstruction, and an explicit no-production/no-GHA/
no-git statement.
