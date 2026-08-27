# Luna task 194 — R07 `u0/v0` intra-GHA sharded boundary v3

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_194_r07_u0v0_intragha_sharded_boundary_v3.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP,
Node, git, GHA, or network locally.  Parent Sol owns mathematical audit,
hash refresh, repository brokerage, and every execution.  Do not edit any
workflow file or any task187/task191 file.

## 1. Governing theorem, frozen space, and gate

Read in full:

```text
sol/proof_r07_complete_correlation_shard_merge_v176.md
sol/luna_task_191_r07_u0v0_batched_boundary_v2.md
sol/luna_reply_191_r07_u0v0_batched_boundary_v2.md
search/d972_r07_u0v0_boundary_preimage_batch_v2.py
crosscheck/check_d972_r07_u0v0_boundary_preimage_batch_v2.py
search/d972_r07_u0v0_boundary_preimage_batch_gha_driver_v2.g
```

Authenticate every predecessor by exact bytes and SHA-256.  The mathematical
space remains literally

```text
D = span of every left translate of the 2 PB3 and 11 PB4 boundary rows.
```

This task changes only the evaluation schedule of one complete correlation.
The task191 SELFTEST is a hard parent-execution gate for v3 PRODUCTION, but it
does not prevent static implementation now.  No task191 production decision
may be assumed.

## 2. Authorized files

Create only:

```text
search/d972_r07_u0v0_boundary_preimage_sharded_v3.py
crosscheck/check_d972_r07_u0v0_boundary_preimage_sharded_v3.py
search/d972_r07_u0v0_boundary_preimage_sharded_gha_driver_v3.g
search/certs/d972_r07_u0v0_boundary_preimage_sharded_selftest_v3_20260828.json
sol/luna_reply_194_r07_u0v0_intragha_sharded_boundary_v3.md
```

Version by copying or wrapping v2 only behind the exact authentication gate.
Do not overwrite its fixture, receipt schema, checkpoint, or reply.

## 3. Producer: exact parallel correlation

Implement a production option `--workers`, restricted to integers 1 through
4.  The GHA production driver will request 4.  Parallelism is inside a single
GHA runner, using Linux processes rather than local execution or a workflow
matrix.  Require the `fork` multiprocessing start method in production and
fail closed with typed `UNKNOWN_INPUT` if it is unavailable; do not silently
fall back to a different schedule.

For one fixed current echelon, fresh dual, and boundary occurrence roster:

1. Canonicalize dual support by
   `(block, component, support_blob, coefficient)` and retain a stable support
   ordinal.  Canonicalize occurrences by
   `(block, component, relator_index, occurrence_ordinal, h_blob,
   base_coefficient)`.  Repeated occurrences remain distinct.
2. Enumerate every component-matched support-times-occurrence pair in the
   frozen lexicographic order and give it a global integer ordinal
   `0 <= m < N`.  Compute `N` exactly before launching workers.  Check the
   aggregate boundary-pair cap before the fork; a cap stop is resource
   UNKNOWN and never a partial zero correlation.
3. Worker `q` consumes exactly the ordinals `m` with `m % workers == q`.
   For every consumed pair compute literally
   `t = g*h^-1`, require `t*h == g`, and add
   `lambda_coefficient*base_coefficient` modulo 3 to the typed key
   `(block, translation_blob, relator_index)`.
4. A worker returns a sealed manifest containing the common input/pin, dual,
   occurrence-roster and pair-universe digests; worker count/index; partition
   rule; first/last/count of its arithmetic progression; exact consumed pair
   count; its sparse partial coefficient map; elapsed/resource counters; and
   a self digest.  A worker does not declare ACTIVE or NONMEMBER.
5. The parent authenticates all worker manifests, rejects a missing,
   duplicated, malformed, crashed, wrong-input, or nonexhaustive shard, proves
   that the arithmetic progressions are pairwise disjoint and cover
   `[0,N)`, adds all partial maps modulo 3, and only then deletes global zeros.
   Sort the resulting ACTIVE list exactly as v2.
6. Materialization of literal translated rows may also be farmed out, but its
   result must be returned in canonical-key slots.  Reduction, pivot insertion,
   retained/dependent classification, ancestry, target reconsideration, and
   checkpoint emission remain serial in the exact task191 order.
7. The succession of fresh duals remains causal.  No worker for round `r+1`
   may start before the canonical rank merge and checkpoint for round `r` are
   complete.  Resume authenticates and replays from rank zero exactly as v2.

Track aggregate child RSS in the parent on Linux (parent plus live children),
terminate all children on any cap/exception, reap them, and emit only typed
`UNKNOWN_RESOURCE`/`UNKNOWN_INPUT`.  A dead or unreported worker is never an
empty partial map.

## 4. Compact but replayable correlation certificate

Do not store millions of repeated contributor dictionaries.  For each round,
bind the literal dual support, complete occurrence roster, canonical pair
universe and partition by their deterministic byte encodings and SHA-256.
Store every sealed shard partial map and the complete merged coefficient map,
including its coefficient for each globally ACTIVE key.  A retained or
dependent row points to the round identity and typed ACTIVE key; it need not
repeat all pair dictionaries.

This is certificate compression only.  The independent checker must recover
the coefficient of every ACTIVE key from the pinned literal sources.  The
producer must also retain exact counts of local cancellations, cross-shard
cancellations after merge, global zeros, ACTIVE keys, and total pairs.  No
digest alone may replace literal row reconstruction or coefficient replay.

## 5. Independent checker

The checker must not import the producer, its shard helper, its ordinal
iterator, its multiprocessing wrapper, or its sparse-map encoder.  It may
authenticate and reuse the task191 independent arithmetic layer.

Independently reconstruct every current dual, support roster, occurrence
roster and complete pair universe.  Use a different deterministic partition
for checking—contiguous ordinal intervals rather than residue classes—and
merge those independent partial maps.  Require equality with the producer's
complete merged map, ACTIVE list, counts, literal translated rows, canonical
serial pivot transcript, dependencies, ancestry, targets, checkpoint replay,
and terminal dual conditions.  Checker processes may run in parallel on GHA,
but their partition and helper code remain nonshared.

`NONMEMBER_D` is legal only after both systems cover the complete pair universe,
merge before zero deletion, obtain an empty ACTIVE list for the same fresh
dual, and check its target pairing and annihilation of every retained row.

## 6. SELFTEST and mutation gates

Use the production-shaped noncommutative task191 toy.  Require at least four
ACTIVE keys, at least two retained rows, at least one later dependent row, a
global cancellation whose nonzero summands lie in different residue shards,
and at least one empty worker when `workers=4` in a separate bounded case.

Run producer schedules with workers 1, 2, and 4 and require byte-identical
mathematical transcripts after deleting timing/process metadata.  Run the
independent contiguous checker and require the same merged map and final span.
Exercise checkpoint interruption and resume after a completed shard merge and
inside the serial ACTIVE suffix; no partial worker state may masquerade as a
completed round.

At minimum reject mutations of: pair ordinal; shard index/count; duplicated or
missing ordinal; wrong common dual/roster digest; `t=g*h^-1`; one partial
coefficient; local zero promoted to ACTIVE; cross-shard cancellation performed
too early; global zero retained; ACTIVE order; parallel pivot insertion;
dependent chain; ancestry; stale-round shard; incomplete worker treated as
zero; worker crash treated as negative; aggregate RSS stop treated as
nonmembership; compact-certificate key redirected to another round; and
worker-1/worker-4 transcript disagreement.

## 7. GHA driver and performance receipt

Provide serial SELFTEST/PRODUCTION bindings around the process-parallel Python
programs, exact-one producer/checker/final markers, visible failure logs,
fresh outputs, authenticated pins, and fail-closed caps.  Do not edit the
generic `gap-run` workflow.  Production requests four producer workers and
four independent-checker workers on the hosted Linux runner; if the runner has
fewer than four CPUs, record the observed CPU count and use
`min(4, cpu_count)` only when the receipt explicitly binds that effective
count.

Report per round and per worker: `N`, consumed ordinals, pair rate, partial-map
size, local cancellations, merged keys, cross-shard cancellations, ACTIVE
count, correlation wall time, serial merge/echelon wall time, aggregate peak
RSS, worker exit status, and end-to-end time.  Compare worker 1 versus worker 4
on the toy and give a conservative production estimate.  Never claim linear
speedup without a timing receipt.

## 8. Reply format

Process Sections 1--7 in order, list exact identities of all five authorized
files, state every static limitation, and end with:

```text
SHARDED COMPLETE-CORRELATION SELFTEST:        NOT EXECUTED BY LUNA
TASK191 BATCHED SELFTEST GATE:                 PENDING PARENT EXECUTION
MATHEMATICAL BOUNDARY SPACE CHANGED:           NO
U0/V0 BOUNDARY DECISION:                       NOT EXECUTED BY LUNA
COMPATIBLE COFINAL LIFT / FAKE / IHARA:         NOT DECLARED
```
