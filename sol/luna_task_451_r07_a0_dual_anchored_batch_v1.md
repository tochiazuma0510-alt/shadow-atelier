# Luna task 451 -- dual-anchored ACTIVE batch continuation

Role: Luna implementation.  Implement the paper theorem in
`sol/proof_r07_a0_dual_anchored_active_batch_v415.md` as a parallel candidate
continuation from the exact Task450 rank-51 checkpoint.  Do not launch local
heavy production and do not perform git, push, or GHA operations.

## Scope and frozen base

Pin and consume:

```text
search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json
search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py
crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v6.py
```

The first eight accepted records must remain an exact prefix.  This is a
parallel acceleration candidate; do not modify the running v6 continuation,
its files, its workflow, or its checkpoint.

## Required outputs

Create only:

```text
search/d972_r07_a0_dual_anchored_active_batch_v1.py
crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py
search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g
sol/luna_reply_451_r07_a0_dual_anchored_active_batch_v1.md
```

## Producer contract

1. Rebuild the rank-51 state by the existing word-bearing replay.  Do not
   import old row, pivot, or dual bytes as live linear algebra.
2. At a nonzero remainder, freeze one canonical anchor dual/remainder and run
   the unchanged complete six-action oracle.  An action hit may be handled by
   one ordinary insertion; do not invent a new action universe.
3. In the correction branch, retain the current v410 tau-free compiler.  This
   v1 batch may fail closed on nonzero tau, S3--S9, or nonzero K with the same
   typed mathematical gates.  Do not implement actor-adapted code here.
4. For tau=0, coordinates S0--S2, K=0, enumerate the complete finite
   seed/target/order-nine-kernel roster instead of stopping at its first
   ACTIVE state.  For every nonzero formula value, freshly replay the literal
   conjugate and require its direct physical pairing with the frozen anchor
   dual to equal that value.
5. Traverse in deterministic `(seed,coordinate,target,fibre_cursor)` order.
   Insert every row that raises the current echelon, up to a declared
   per-batch rise cap (16 is recommended).  Recompute target remainder/dual
   exactly once after the batch, not once per row.
6. A batch row records the frozen anchor dual/remainder/rank, selector cursor,
   literal ancestry, direct scalar/row digest, and its actual pre/post
   insertion rank and pivot.  A closed-batch receipt records the single
   recomputed post-batch remainder/dual and rank.
7. Checkpoint only fully closed batches.  If a resource limit interrupts an
   open batch, return the last closed durable checkpoint and make no claim
   from the discarded partial batch.  Do not serialize physical rows or a Q0
   store.
8. `COMMON_CANDIDATE` still requires the existing strict positive expression,
   literal word, exact exponent, joint-identity, and direct physical replay.
   An empty complete batch in v1 remains a typed separator candidate pending
   its independent negative exhaustion; do not claim NONMEMBER.

Use 7,200 seconds, 4.8 GB RSS, at most 64 new rises, and a small explicit
per-batch cap in the driver.  Preserve progress lines with batch number,
rank, accepted count, elapsed seconds, and RSS.  No production SELFTEST or
FIXTURE in the driver.

## Checker contract

- Exact-pin the producer dependencies and frozen checkpoint.
- Authenticate the eight-record prefix and every checkpoint seal.
- Independently rebuild the rank-51 basis and each batch anchor.
- For every batch row, reconstruct the literal physical row, check the frozen
  anchor scalar, replay its pivot/rank rise, and require it belongs to the
  deterministic declared selector cursor.
- Recompute the declared coordinate blob, especially S0 `target_hex`, from
  the literal `delta_word`; do not inherit this auxiliary field from Task448
  or the producer without semantic replay.
- Recompute the post-batch remainder/dual once and compare the closed-batch
  receipt.
- Delegate/reuse the existing positive reconstruction for a positive
  terminal.  Never require later rows in a batch to pair with an intervening
  canonical dual.
- Add bounded synthetic mutations for changed anchor digest/scalar, reordered
  cursor, false pivot rise, altered post-batch dual, open-batch promotion, and
  altered rank-51 prefix.

Run only compile, synthetic self-tests, and small static/deterministic toy
fixtures locally.  Report exact bytes/SHA-256, dependency pins, resource
caps, and any remaining implementation blocker.  If the full implementation
cannot be made sound in this turn, return a precise STOP rather than a
partial production driver.
