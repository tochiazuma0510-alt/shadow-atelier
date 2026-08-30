# Luna task 410 — R07 A4 linear delta checkpoint v18

Role: Luna implementation only.  Do not run heavy local arithmetic, commit,
push, dispatch GHA, edit workflows, or touch files outside the outputs below.

## 1. Incident and non-negotiable diagnosis

Task409 v17 is rejected and must not be dispatched.  Changing the row gate to
write a complete checkpoint after every row makes `checkpoint_total_bytes`
exceed 2 GB before all 6,441 rows even from the two digest arrays alone, and
re-canonicalizes the entire prefix after every row.  This is a guaranteed
resource stop and an avoidable quadratic checkpoint path.

The mathematical producer/oracle, row order, row assembly, batch-64 query,
boundary/K decisions, caps and terminal meanings must not change.

## 2. Required minimal repair

Create a v18 producer over the frozen v16/v17 arithmetic with an append-only,
linear-size checkpoint transport:

1. Authenticate the existing legacy checkpoint exactly: 25,581 bytes, SHA
   `595213bab8936ef10e94ce90ccf526c105d02d871d4dc5d02b6c76cb51593445`,
   `next_row=25`, legacy producer code SHA
   `964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7`.
   Treat it as immutable base/anchor.
2. After each fully completed row, write exactly one small versioned delta
   segment under `ci/out`.  It must contain every state append/change needed
   to replay that row (row/bridge digests, oracle events/records,
   basis/insertion/word/queue changes, semantic counter delta, and any other
   changed field), its row ordinal, base identity, previous segment seal and
   its own seal.  Do not copy the preceding prefix arrays/state into a new
   segment.
3. Atomically replace a small HEAD manifest only after the segment is fully
   sealed.  HEAD names the last fully completed row.  A partial row or orphan
   segment must never advance HEAD.
4. Resume must authenticate base + HEAD + the exact segment chain in one
   forward pass and reconstruct the same live state.  Reject missing,
   duplicated, reordered, forked, mutated or post-HEAD segments.  One-way
   migration from the named legacy base is allowed; no other legacy object is.
5. Charge `checkpoint_total_bytes` only for newly written segment bytes plus
   HEAD bytes.  Do not re-charge or re-canonicalize prior prefix state per row.
   The static implementation must demonstrate O(number of rows + total delta
   payload), not O(number of rows squared), and no configured cap may force a
   stop before row 6,441 solely because every row completed.
6. Terminal reference and artifact transport must bind the base, HEAD and
   complete segment chain.  The first production driver starts from the same
   embedded legacy seed as v30/v31 and retains `RESUME`, program limit 14,400
   seconds, shell envelope 14,520 seconds and the existing authority seeds.

Do not add SELFTEST to production, a second authority scan, SAT, a second
arithmetic replay, whole-DOM prefix rebuilding per row, or any unrelated
repair.  Prefer the smallest event/delta representation already supported by
the producer's mutation ledgers.

## 3. Versioned outputs only

- `search/d972_r07_word_independent_successor_kernel_v18.py`
- `crosscheck/check_d972_r07_word_independent_successor_kernel_v24.py`
- `search/d972_r07_word_independent_successor_kernel_gha_driver_v32.g`
- `sol/luna_reply_410_r07_a4_linear_delta_checkpoint_v18.md`

The checker may advance only the producer/checkpoint transport pins needed to
independently authenticate the chain; its arithmetic and terminal vocabulary
stay frozen.  The driver must upload every segment and HEAD through the
existing `ci/out` artifact collection.

## 4. Bounded gates and report

Run only static/bounded gates: ASCII/AST/compile, generated-source pin,
GAP parse, exact legacy-seed authentication, and a tiny synthetic chain with
at least two completed rows followed by a stop inside the third row.  Show:

- HEAD advances through the first two rows and not the partial third;
- base + segments reconstruct the exact state;
- segment mutation/reorder/delete/fork/orphan/HEAD-ahead are rejected;
- each segment excludes the previous full prefix;
- total written checkpoint bytes grow linearly in the fixture;
- production path contains no full checkpoint call after every row and no
  extra heavy phase.

Report exact bytes/SHA-256 for all outputs and the generated producer/checker
sources.  If a genuinely linear delta cannot be implemented without changing
the oracle semantics, stop with a precise blocker instead of falling back to
full snapshots.
