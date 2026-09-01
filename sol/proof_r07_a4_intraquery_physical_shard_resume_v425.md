# R07 A4: intra-query physical-shard resume (v425)

## Problem fixed

Run `33506331399` durably completed row 26, then row 27 accumulated 2,287
correlation rounds and transient boundary/combined rank 138,592 before the
wall stop.  The current delta format seals only after a row terminal, so all
row-27 work disappeared.  Saving only the 138,592 raw boundary identities is
mathematically sufficient but operationally insufficient: resume would redo
the same echelon reductions and can again consume hours.

The correct continuation object is therefore neither a whole multi-gigabyte
JSON snapshot nor a source-only ledger.  It is an append-only sequence of
closed *physical echelon shards* plus one pending query payload.

## 1. Direct physical state

For an `Echelon`, the continuation state is exactly the chronological pivot
list together with, for each pivot, its normalized packed row and label.  A
directly loaded entry is admissible when:

1. pivots and labels are unique and list/dictionary domains agree;
2. every coefficient is in `1,2`, the pivot coefficient is `1`, and the row
   contains no earlier chronological pivot;
3. the row and label digests equal the sealed shard entry; and
4. the head's rank and cumulative row digest equal the concatenated shards.

These conditions reconstruct the exact in-memory maps used by `reduce`; no
insertion or reduction is performed during producer resume.  Chronological
order, rather than lexicographic pivot order, is essential because the current
implementation permits a later pivot key to be lexicographically smaller.

For `LiveBasis`, each boundary rise stores in the same shard:

```text
kind=B, label, raw_identity
boundary pivot/normalized row/label
combined pivot/normalized row/label
boundary and combined formal-reduction data
BOUNDARY_RANK_RISE record/event and their epoch transition
```

The formal reduction data reconstructs `boundary_ledgers`,
`combined_ledgers`, `b_coefficients`, and `b_formals` from earlier entries;
`active_registry` is the union of loaded combined-row keys.  This is exactly
the information which `add_boundary` produces and subsequently reads.

## 2. Closed shard boundary

Inside `Oracle.query`, finish a canonical 64-candidate correlation batch
completely before making it durable.  All accepted candidates in that batch
must have passed current-remainder reduction and actual rank-rise gates.
Append their physical entries to a temporary shard, flush and `fsync` it,
atomically install its canonical byte/SHA seal, then atomically advance a
small HEAD.  An interrupted open 64-candidate batch is absent; a completed
one is never repeated.

To avoid one file per correlation round, a storage shard may contain a fixed
number `q` of closed 64-candidate batches.  Its internal batch offsets and
digest chain remain explicit.  The durability loss is then at most `q-1`
closed batches, not an entire row.  Choosing `q` is an operational parameter
and changes neither accepted order nor mathematics.

The producer may direct-load a structurally sealed shard for continuation.
That makes the resumed run a candidate computation.  Independent promotion
still requires a checker to reconstruct every shard entry from its
`raw_identity` and replay the reductions.  This separation is consistent with
the workshop hierarchy: fast producer continuation is not by itself
cross-check evidence.

## 3. Pending row payload

Completed-row prefixes must not include the open row.  Refactor row handling
into `prepare`, `query`, and `commit`:

- `prepare` authenticates row `r`, computes its source word, assembled target,
  bridge trace, row digest and optional sample, and stores them in one sealed
  `open_query` payload;
- `query` performs dual/correlation batches and may advance physical shards;
- only a MEMBER or ZERO terminal calls `commit`, which appends exactly one row
  digest and bridge digest, updates samples/chunks, accepts a K item if
  required, clears `open_query`, and advances `next_row`.

For an intra-query head at row `r` the required cursor equation is

```text
next_row = r
row_cursor = bridge_cursor = r - 1
open_query.query_id = "R:r"
no R:r terminal occurs in the completed terminal prefix
```

The open payload owns the actual target and source word, so resume neither
reassembles nor recharges the row.  Its target/word/bridge/row digests are
bound into every subsequent shard HEAD.  Boundary and dual events for `R:r`
are allowed before its unique terminal; completed-row counters are not.

## 4. Resume and terminal transition

Resume authenticates the old completed-row base and the ordered physical
shard chain, direct-loads both echelons/formals/events/counters, checks the
pending-query equation, and continues the `while` loop with the stored target.
The first new dual is computed against the loaded rank, so previously accepted
columns cannot be rediscovered as rises.

When the query terminates, its final record/event is appended after all its
boundary events.  `commit` then creates the ordinary row delta, advances
`next_row` by one, and makes the intra-query head obsolete.  A resource stop
returns the last closed physical HEAD.  It must never report the transient
open batch.

## 5. Independent gates

A checker must reject:

- reordered, omitted, duplicated, or unsealed shards;
- a row whose pivot is not normalized or contains an earlier pivot;
- mismatch between physical row and replay from `raw_identity`;
- mismatch of boundary/combined reductions or formal ledgers;
- an event/epoch/counter transition not owned by the same shard;
- an open query already present in completed row/bridge prefixes;
- target, word, bridge, sample, row, or query-id drift;
- a terminal duplicated across intra-query and row delta; and
- a HEAD ahead of its last atomically installed shard.

A bounded fixture must compare uninterrupted execution with interruption
after several closed correlation batches followed by direct restore.  Equality
is required for the physical echelons, formals, event/dual chains, epoch,
pending query, final terminal, and the next completed-row checkpoint.

## Consequence for v220

This construction makes row-level four-hour loss unnecessary, but it is not
yet an implementation and does not retroactively recover the lost row-27
state.  A4 remains `1/3 UNKNOWN_RESOURCE`; row 26 still awaits the v29
checker-only replay.  The immediate witness path remains A0 rank-99 plus the
compact positive A5 lane, while this theorem fixes the correct durable form
for any future full A4 continuation.
