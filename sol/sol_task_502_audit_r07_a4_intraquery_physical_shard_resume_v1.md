# Sol(max) task 502 - audit A4 intra-query physical-shard resume v1

Role: independent Sol(max) mathematical/implementation auditor.  This is a
bounded audit of Task499 only.  Do not edit implementation files, run the real
6441-row computation, run GHA, change workflows, or broaden A4 arithmetic or
the legal-source universe.  Write only
`sol/sol_reply_502_audit_r07_a4_intraquery_physical_shard_resume_v1.md`.

Read Task499 and its reply in full, together with v425, v423, v429 and the
frozen v22/v31/v41 owners named there.  Do not trust Task499's prose or
self-tests.  Use only bounded read-only checks and temporary fixtures outside
the repository.

## 1. Frozen audit subject

- producer wrapper
  `search/d972_r07_word_independent_successor_kernel_v23.py`, 14472 bytes,
  SHA-256
  `d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a`;
- generated producer, 266117 bytes, SHA-256
  `d406f1128dc66bc526fe5babf0f9fee0b086d7fce348f1435a7516d8090b9ef6`;
- checker wrapper
  `crosscheck/check_d972_r07_word_independent_successor_kernel_v32.py`,
  10036 bytes, SHA-256
  `8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0`;
- generated checker, 293042 bytes, SHA-256
  `80ac3ff80b106691f667840891e99904b1a9f2bc58dfe0b700b893904ad38440`;
- driver
  `search/d972_r07_word_independent_successor_kernel_gha_driver_v42.g`,
  4362 bytes, SHA-256
  `650b1d052dbae8df65b2b8a4e8b7a33ab6f9c66d7b74117600e361b1dfa74629`;
- Task499 reply, 3286 bytes, SHA-256
  `67a8becca1250c4b9fc59c22f7c54df0875d43f5dc6cbfdc7eb8400a974d3801`.

The immutable comparison owners are exactly the pins in Task499: v22
producer, v31 checker, v41 driver, and all six members of the row-26 release.
Any pin mismatch is a preflight STOP, not a semantic verdict.

## 2. Audit question

Decide whether v23/v32/v42 safely implement v425's first physical-shard
resume dialect from the authenticated row-26 state, without changing the
underlying A4 search and without adding an avoidable performance or memory
regression.

Independently establish all of the following.

1. The wrapper-generated diffs are confined to versioned durability plumbing:
   A4 arithmetic, row/source/candidate order, correlation and membership
   tests, rank and K/queue rules, evaluator, caps, and terminal meanings are
   extensionally unchanged from the frozen owners.
2. `prepare/query/commit` has exactly one owner for row 27.  Completed
   row/bridge prefixes exclude the open row, the cursor equation is exact,
   and a completed terminal cannot be installed twice.
3. A shard closes exactly one chronological 64-candidate batch and includes
   every accepted rise needed to restore both physical echelons, both formal
   ledgers, coefficients, events, epochs, counters and offsets.  Open batches
   do not become durable.
4. Authentication is fail-closed: shard order, uniqueness, predecessor/head
   chain, offsets, seals, raw identities, packed rows, reductions, formal
   data and pending word/target/bridge/sample digests are all bound.  HEAD
   cannot be ahead of installed shards, and stale or mixed-row chains fail.
5. The checker independently recreates each physical row from its raw
   identity and independently validates the two reductions and formal/event
   transitions.  It must not merely compare producer-supplied digests or
   import/call the v23 implementation.
6. Restore directly loads authenticated pivot/formal/event state and does not
   call insertion, reduction, correlation, or earlier-boundary reconstruction
   for admitted shard entries.  An interruption after three closed batches
   is extensionally identical to uninterrupted execution.
7. Atomicity is real: temporary shard flush+fsync precedes atomic install,
   HEAD replacement cannot publish a missing shard, and a crash at each
   boundary resumes from the next unexamined candidate without loss or
   duplication.
8. Performance is proportional to the new shard and current state.  Reject a
   hidden full-matrix JSON snapshot, cumulative-prefix rewriting, repeated
   whole-boundary closure, quadratic copy, unnecessary dense conversion, or
   in-memory retention of every historical checkpoint.  Cosmetic tuning is
   not a STOP; an executable design that restores the old memory/time failure
   is.
9. V42 exact-pins v41 plus every wrapper/generated source and all six row-26
   members, starts at row 27, keeps v41 resource limits, uploads RESOURCE
   durability without a second full semantic replay, and invokes the full
   checker only for the intended nonresource/positive terminal.  It must not
   add SELFTEST, retry, worker-pool or extra production traversal.
10. V423's unique resource-excess semantics and v429's resumed transport
    difference relation remain present and applicable.

## 3. Bounded adversarial checks

Reproduce the exact wrapper/generated pins and diff confinement.  Build
independent small fixtures for uninterrupted versus interruption after at
least three closed 64-candidate batches.  Mutate, one at a time, every bound
identity/digest/offset/formal/event/head field, a raw identity while resealing
the producer envelope, HEAD-ahead, a missing or reordered shard, a mixed row,
an open-batch fragment, and a duplicate terminal.  Re-seal outer envelopes
where necessary so the inner semantic gates are actually reached.

Instrument restore to fail if any insertion/reduction/correlation routine is
called for restored entries.  Use AST/static call analysis plus bounded copy
instrumentation to decide the performance gate; do not launch a large timing
benchmark.  Check driver pins/markers/paths and bounded GAP
`ReadAsFunction`; syntax or fixture success alone is not adoption.

Return `GO_FOR_GHA_DISPATCH` only if every gate passes.  Otherwise return
`STOP_DO_NOT_ADOPT` with the smallest exact reproducer and a minimal repair.
In either case state that A4 remains `1/3 UNKNOWN_RESOURCE`, cross-checked only
through row 26; implementation readiness is not mathematical progress.

End with exactly one of:

`TASK502_R07_A4_PHYSICAL_SHARD_RESUME_AUDIT_GO`

or

`TASK502_R07_A4_PHYSICAL_SHARD_RESUME_AUDIT_STOP`
