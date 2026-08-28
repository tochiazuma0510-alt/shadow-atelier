# Luna task 297 — task192 fixed-dual parallel boundary correlation v4

Requester: Sol / 2026-08-28

## 0. Role and permitted paths

This is a bounded implementation commission.  Do not make mathematical
claims and do not run Python, GAP, GHA, network, or git.  Create only these
five new versioned paths:

1. `search/d972_r07_normalized_exact_common_word_parallel_v4.py`
2. `crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v4.py`
3. `search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v4.g`
4. `search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v4_20260828.json`
5. `sol/luna_reply_297_r07_task192_parallel_boundary_v4.md`

Do not overwrite task192 v3, task295, or any other file.  Status must remain
`UNEXECUTED` and production must fail closed until parent Sol supplies an
authenticated resume input and dispatches it.

## 1. Exact optimization boundary

The adaptive rank loop remains serial.  After every retained rank change the
dual changes, so distinct dual epochs must never be run independently or
merged.  Parallelize only one invocation of
`BoundaryDescriptorCache.correlation(dual, monitor)` for one frozen dual.

For that frozen dual, partition the complete ordered descriptor/support pair
roster into deterministic contiguous shards.  Each worker returns, using only
primitive serializable records:

- its exact pair interval and pair count;
- the mod-3 partial accumulator keyed by
  `(block, relator_index, translation_blob)`;
- the complete ordered contributor records needed for any selected key; and
- a digest binding the frozen dual, descriptor roster, interval, and result.

The parent must authenticate exact disjoint cover (no gap, overlap, duplicate,
or reordering), sum all partial accumulators in F3, concatenate contributor
records in original global pair order, discard zero totals, and choose exactly
the same minimum active key as v3:

`min(active, key=(block, translation_blob, relator_index))`.

It then reconstructs the translated row and checks that its direct pairing
with the frozen dual equals the merged nonzero scalar.  Only this one selected
row is returned to the existing serial rank update.  Thus the retained-column
sequence must be byte-for-byte equal to serial v3 for the same input and caps.

Use Linux `multiprocessing` with an explicit `fork` context or another genuine
process mechanism; threads are not acceptable for this pure-Python work.  Use
an explicit `--boundary-workers` integer with production range 2..4.  Worker
count is execution metadata, never mathematical data.  Do not edit a workflow.

## 2. Resource and checkpoint truth

Do not claim `single_process=true`.  The v4 monitor/envelope must publish at
least `parallel_boundary=true`, worker count, completed shard count, total
pair count, and aggregate RSS accounting policy.  Preserve exact cumulative
`boundary_pairs` semantics.  Check the cap before launch without charging
uncomputed work; after an exact completed cover, charge exactly the returned
pair count.  Check wall time/RSS before and after every shard batch.  A worker
failure, timeout, malformed result, incomplete cover, or aggregate memory
uncertainty is `UNKNOWN_RESOURCE` or `UNKNOWN_INPUT`, never a candidate.

The existing v3 safe checkpoint must remain resumable.  A resource stop during
one frozen-dual batch may discard and replay that incomplete batch, but it must
not advance the safe pair cursor or serialize partial accumulator state as if
complete.  COMMON must still omit checkpoint state.  Production must not use
an unsealed checkpoint as evidence.

Pin by bytes/SHA every imported v3 producer/checker/driver and all transitive
inputs required by their existing contract.  A v4 receipt may use an explicit
outer envelope or a documented semantic projection into the v3 checker, but
it must never forge `single_process=true`.  The v4 checker must independently
validate the projection and then invoke/replay the existing independent v3
mathematical checker without importing v4 producer code.

## 3. Mandatory SELFTEST and mutation gates

The sealed fixture must exercise at least four frozen-dual cases:

1. ACTIVE with the winning key formed from contributions in two shards;
2. cancellation to zero across a shard boundary;
3. two active keys whose winner tests the exact v3 lex order;
4. no active key.

For worker counts 2, 3, and 4, compare the complete merged accumulator,
contributors, selected key/row/scalar, and pair count against a separately
implemented serial oracle.  Also run two consecutive dual epochs and prove
that no accumulator or contributor state leaks between epochs.

The independent checker must generate and reject semantic mutations for at
least: omitted shard, duplicated shard, overlapping interval, gap, permuted
pair order, wrong dual digest, wrong descriptor digest, changed coefficient,
changed translation key, changed contributor, wrong mod-3 merge, zero kept
active, wrong lex winner, wrong direct scalar, wrong pair count, stale epoch,
worker failure accepted, incomplete batch checkpointed, `single_process=true`,
and worker count outside 2..4.  Mutation count is the number actually executed
and rejected, not a constant.

## 4. Driver

ASCII only.  It must run SELFTEST producer and independent checker first.  Its
PRODUCTION branch must require an explicit authenticated resume path and must
fail closed if absent.  Discover `nproc`, choose `min(4,nproc)` and require at
least 2; record the chosen value.  Use the task192 caps and 19,800-second fresh
wall budget unless parent later supplies a new versioned driver.  Require exact
one producer terminal, exact one checker terminal, exact producer/checker
terminal equality, stale-output rejection, and one final sentinel.  Do not
dispatch.

## 5. Reply

Record paths, bytes/SHA, immutable pins, exact SELFTEST contract, terminal
grammar, limitations, `UNEXECUTED`, and explicitly state that no A0 COMMON,
compatible lift, fake certificate, or Ihara witness has been obtained.
