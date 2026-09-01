# Luna Task443 — A4 delta tracker pre-loop repair v21

Role: Luna implementation owner.  This is a transport/checkpoint-only repair.
Do not change the accepted A4 arithmetic, the 6,441-row universe, row evaluator,
kernel/queue rules, word ancestry, resource limits, workflow, or mathematical
terminal semantics.  Do not run production or GHA.

## Proven defect and safe input

The current v20/v26/v38 route is NO-GO unchanged.  In v18-generated
`write_checkpoint`, `_a4_delta_tracker` is first initialized after a completed
row.  The first segment therefore records the difference from the already
completed state and omits that row.  Run 33303302455 demonstrates the defect:
its segment 1 claims ordinal 25/next_row 26 but contains no row digest, bridge,
oracle record/event, or other row payload.  Its apparent `next_row=27` chain is
unsafe and must not be used.

The only authorized resume base is the canonical run 33263899806 artifact
9720097578:

- producer base: 25,581 bytes,
  SHA-256 `595213bab8936ef10e94ce90ccf526c105d02d871d4dc5d02b6c76cb51593445`,
  `next_row=25`;
- checker base: 8,991 bytes,
  SHA-256 `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2`.

## Required repair

1. Create producer v21 as a byte-pinned wrapper of exact producer v20
   (2,239 bytes,
   `c45d48ac27f462cf342912e17e619be02ca68322c62a21897fcdc3d524e07a6f`).
   Patch only the generated transport source.
2. On a delta resume, initialize `_a4_delta_tracker` exactly once after the
   restored state and saved counters have been installed, but before
   `for ordinal, row in ...`.  Its snapshot must contain the restored oracle,
   word DAG, queue, actions, action-event chain, matrix, counters, and existing
   delta meta.  `write_checkpoint` must then compute the first row delta against
   that pre-row snapshot.
3. Require a row segment to contain exactly one new row digest and one new
   bridge digest, the corresponding row-terminal oracle record/event, and
   cursor/ordinal continuity.  Do not require a K/queue append when the row does
   not raise K rank.  A zero-row segment must fail closed before HEAD advances.
4. Preserve append-then-atomic-HEAD ordering.  Preserve the immutable base and
   prior chain digest.  Never accept or migrate run33303302455's corrupt chain.
5. Create independent checker v27, pinning the exact v21 producer.  It must
   independently replay each segment from the canonical base, require sequence,
   previous digest, chain, ordinal, next-row, row/bridge/terminal-event deltas,
   and verify that applying the segment really advances the reconstructed state
   by that row.  Mutations must include empty first-row segment, skipped row25,
   forged next_row27, row digest deletion, bridge deletion, terminal event
   deletion, reordered segment, and HEAD-ahead-of-segment.
6. Create driver v39 from exact v38 semantics but pin v21/v27 and seed only the
   canonical next_row25 base plus a valid empty HEAD for the initial repaired
   run.  It must reject nonempty/corrupt embedded HEADs rather than silently
   reset them.  A later continuation will get its own versioned driver which
   embeds/pins the preceding nonempty chain; do not change `gap-run.yml`.
7. Keep the production call in `RESUME` mode.  The reply must record that parent
   dispatch, if authorized after audit, uses JSON-quoted
   `D386Mode:="RESUME";;`, `timeout_min=250`,
   `with_pquot_packages=true`, and `out_dir=ci/out`.

## Bounded tests only

- Python syntax/compile.
- Frozen-source pin and unique-patch-cardinality tests.
- A tiny canonical-base + two synthetic row-segment chain exercising restore,
  pre-loop tracker placement, atomic HEAD semantics, and every listed mutation.
- Driver static pin/command reconstruction and `git diff --check`.

Do not execute GAP, the 6,441-row evaluator, the real checker, production, GHA,
commit, push, or dispatch.

## Authorized outputs only

- `search/d972_r07_word_independent_successor_kernel_v21.py`
- `crosscheck/check_d972_r07_word_independent_successor_kernel_v27.py`
- `search/d972_r07_word_independent_successor_kernel_gha_driver_v39.g`
- `sol/luna_reply_443_r07_a4_delta_tracker_preloop_v21.md`

The reply must give bytes/SHA-256, exact owner/generated pins, patch cardinality,
toy/mutation results, and confirm no arithmetic source changed.
