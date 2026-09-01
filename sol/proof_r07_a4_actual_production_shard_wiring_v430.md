# R07 A4: actual production wiring for physical shards (v430)

Author: Sol / 2026-09-02

Status: implementation contract refining v425 after Task502 rejected the
unreachable v23/v32 helpers.  This note changes no A4 arithmetic, legal source
order, cap, or terminal meaning.  `verified=false`.

## 1. The exact missing map

In the frozen v22 producer, a row is assembled in `consume_row`, then
`Oracle.query` repeatedly executes one correlation round.  A nonzero round
orders the private candidates and examines

\[
 m=\min(64,|C|),\qquad 1\le m\le64.                 \tag{1.1}
\]

Some of these candidates reduce to zero against the current combined basis;
the others are inserted chronologically by `LiveBasis.add_boundary`.  A
physical shard must therefore own one *examined batch*, not 64 accepted rows.
Its batch envelope contains `m`, the ordered prefix identity/coefficient
digest, the accepted bit mask, the dual/correlation event, and one physical
entry for each `1` in that mask.  The entry count is the Hamming weight of the
mask.  Requiring 64 entries, as the rejected v23 fixture did, is false.

The required production call graph is

```text
build_kernel: construct/restore one shard controller
consume_row:  prepare(open row)
Oracle.query: close_batch(after all m candidates were examined)
consume_row:  commit(after its unique MEMBER/ZERO terminal)
ResourceStop: publish last closed physical HEAD
```

Mere helper definitions, wrapper self-tests, or uncalled validators do not
implement this graph.

## 2. Open-row ownership

`prepare` occurs after the literal source, assembled target, task198 bridge
trace, row value, and optional sample are computed, but before any of them is
appended to a completed prefix.  It seals

```text
query_id, next_row, row_cursor, bridge_cursor,
source word, target, bridge trace, row value, optional sample,
and every corresponding digest.
```

For row `r`, `next_row=r` and both completed cursors are `r-1`.  The current
v22 statements which append `bridge_chain`, `row_digests`, chunks and samples
before `Oracle.query` must move to `commit`.  `Oracle.query` may append
nonterminal dual and boundary events for `R:r`; no row terminal, row digest,
bridge digest, chunk, or sample enters the completed prefix twice.

## 3. One physical batch

Immediately before a correlation round, record the physical basis ranks,
oracle record/event/dual lengths, epoch, and semantic counters.  After the
whole prefix (1.1) has been examined, form one batch with:

1. the open-query seal and chronological batch index;
2. the recomputable dual digest, target dot, public correlation object,
   private-prefix digest, `m`, and accepted mask;
3. for each accepted identity, its raw identity and coefficient, boundary
   pivot/normalized row/label/reduction, combined
   pivot/normalized row/label/reduction, boundary and combined formal data,
   `b_coefficients`, `b_formals`, insertion event and query event;
4. exact before/after ranks, record/event/dual lengths, epoch, active-key
   addition, and semantic-counter delta.

The producer first canonicalizes and durably installs the shard, then advances
HEAD by a second atomic replace.  Both writes use the existing `write_atomic`,
which fsyncs the file and containing directory.  A partial open batch is not
named by HEAD.  HEAD binds the immutable completed-row base, open-query seal,
ordered shard seals, cumulative examined count, cumulative accepted count,
ranks, epoch and counter digest.

## 4. Direct producer restore

Restore first authenticates and rebuilds the ordinary completed-row base.
It then authenticates the HEAD and ordered shard chain and directly installs
the shard-owned physical maps into both `Echelon` objects and the associated
`LiveBasis` dictionaries, formals, active registry, insertion events, oracle
records/events/duals, epoch and semantic counters.  No admitted shard entry is
passed to `reduce`, `insert`, `correlate`, or raw-boundary reconstruction.
The next iteration recomputes a new dual from the loaded rank and the sealed
open target.  Thus a closed batch is neither lost nor repeated.

This direct load is candidate continuation only.  Structural authentication
does not make it cross-checked.

## 5. Independent checker replay

The checker starts from the same completed-row base but does not import the
producer helper.  For every batch it independently recomputes the dual,
correlation roster and exact prefix (1.1), then sequentially reduces every
candidate.  Its recomputed zero/nonzero decisions must equal the accepted
mask, and every nonzero decision must reproduce the stored boundary and
combined insertion details, formal transitions, events, epoch, ranks and
counter delta.  This simultaneously detects an omitted accepted rise and a
fabricated physical entry; digest comparison alone is insufficient.

For a resource terminal the checkpoint reference has a distinct
`physical_shard_chain` kind which binds the completed-row delta HEAD and the
open-row physical HEAD.  A continuation producer may consume it as a
candidate.  Promotion requires the independent replay above.  The production
driver may retain v41's policy of uploading a RESOURCE continuation without
paying that replay in the same job.

## 6. Commit and obsolete head

After the unique MEMBER or ZERO terminal, `commit` appends exactly one bridge
digest, row digest, applicable chunk and sample, advances the completed row,
writes the ordinary row delta once, and marks the physical HEAD obsolete.
The ordinary delta then becomes the continuation owner; the physical chain is
retained only as provenance until independent replay or artifact expiry.

## 7. Executable transport

The first row-27 production driver must actually download and authenticate
the immutable row-26 release and all six members, using the exact transport
gates already exercised by the Task483 checker-only v3 driver.  It then runs
the actual successor producer with the row-26 producer HEAD and a distinct
physical-root/HEAD path.  Wrapper/generated-source/release/member pins must be
commands, not constants.  A positive terminal alone may invoke the successor
checker; RESOURCE uploads the producer result, ordinary base/deltas, physical
HEAD and every named shard.

## 8. Acceptance test

A bounded fixture must enter through production `main`, `consume_row`, and
`Oracle.query`, interrupt after at least three closed batches, restart through
the real CLI restore path, and equal an uninterrupted terminal state.  AST
call counts for `prepare`, `close_batch`, `direct_restore`, `commit`, and the
checker validator must each be positive outside self-test definitions.
Mutations must re-seal outer envelopes so that raw identity, accepted mask,
physical reduction, event/counter, missing/reordered shard, HEAD-ahead and
duplicate-terminal gates are reached.  Copy instrumentation must show no full
matrix snapshot, cumulative-prefix rewrite, or replay of prior shard
reductions.

Until such a successor is independently audited, A4 remains
`1/3 UNKNOWN_RESOURCE`, cross-checked only through row 26.

`R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V430_PAPER_GRADE`
