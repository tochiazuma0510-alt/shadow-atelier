# R07 A0: exact rank-99 actual-owner transform (v424)

## Purpose

Task468 v1 is rejected: its production path is a zero-work wrapper and its
checker does not replay the mathematics.  This note fixes the replacement at
the level of the already successful Task451 owner.  No new abstract engine is
needed.  The successor must be a byte-pinned transform of the actual Task451
producer/checker arithmetic, with the exact recovered rank-99 checkpoint as a
frozen physical prefix.

This theorem is conditional only on the independent Task467 checker-only GHA
replay passing.  That condition belongs to the parent dispatch gate, never to
a synthetic runtime `UNKNOWN_RESOURCE` branch.

## 1. Frozen rank-99 dialect

Let `C99` be
`search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json`, exactly
173,082 bytes with SHA-256
`bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358`.
Its old Task451 state has:

```text
rank = 99
accepted_count = 56
round = 12
batch_count = 3
batch row counts = 16,16,16
open_batch = false
```

The first eight records are the exact rank-51 prefix, and the remaining 48
are exactly the flattened rows of those three closed receipts.  A successor
does not reinterpret this as a fresh rank-ladder checkpoint.  It authenticates
the old schema, binding, canonical seal, exact first-eight prefix, three
anchor/post chains, flattening, ranks and round, and then reconstructs its
physical state by the existing actual sequence

\[
  P_{51}\xrightarrow{\text{Task451 replay\_batches}(3)}P_{99}.
\]

Thus rank 99 is a frozen *physical* prefix, not merely a count assertion.

## 2. New append-only dialect

The new schema binding contains the hashes of the Task451 arithmetic owner,
the independent arithmetic checker lineage, `C99`, and this v424 paper.  Its
closed state contains:

- the exact `C99` identity and 56-record prefix;
- `appended_batches`, numbered globally from 4 onward;
- their exact flattened appended records;
- `accepted_count = 56 + appended_row_count`;
- `rank = 99 + appended_row_count`;
- the current round/profile;
- an append-only segment ledger; and
- `open_batch = false` plus a canonical state seal.

For every segment `s`, store

```text
input checkpoint bytes/SHA and prior state seal
start batch/count/rank/round
end batch/count/rank/round
new_rises = end_count - start_count
closed = true
```

Segments are contiguous and their first start is `(3,56,99,12)`.  Every own
checkpoint must have the exact 56-record/three-batch prefix equal to `C99` and
must flatten all appended batches exactly.  This makes prefix comparison a
load-bearing state equation, not a standalone boolean.

## 3. Delayed literal certification in the actual loop

For a nonzero formula scalar, Task451 already computes the actual correction
column

\[
r=\operatorname{aggregate}(\operatorname{replay\_atom}(i,\delta)).
\]

The successor changes only the order of the following pure checks.  Call the
real packed echelon ABI as

```python
remainder, _ = P["phys"].reduce(r)
```

without mutation.

- If `remainder` is empty, skip this candidate.  Do not construct the full
  conjugate, call `seed_v12`, compute exponents, create a receipt, or make a
  negative/exhaustion claim.
- If it is nonempty, set `predicted_pivot = min(remainder)`, then run every
  unchanged Task451 literal gate: reduced conjugate, fresh `seed_v12`
  equality, exact exponent pair and divisibility, forbidden-`E` absence,
  adjoint/selector/delta/digest gates, and formula/direct/anchor scalar
  equality.  Only then call the real `add` once and require its returned pivot
  to equal `predicted_pivot`.

The action-row path keeps its existing direct-row/scalar/rise gates.  Hence the
retained rank-raising sequence is identical to Task451 while dependent rows
avoid the second expensive full-conjugate construction.

## 4. Short batches and per-invocation cap

Fix `batch_cap = 16`.  At invocation start record the authenticated closed
count/rank as `segment_start_count/rank` and initialize `new_rises = 0`, not
the historical appended total.  After each complete batch, update the
anchor/post state, append one receipt, atomically seal the state, and replace
`last_closed`.  Stop at exactly 64 *new* rises for the max-rise resource
terminal.  A 63-rise `max_rises` terminal is invalid and 65 is impossible.

If any resource stop occurs during an open batch, the in-memory mutations are
discarded from the artifact: counts, rank, batches, accepted sources and
durable reference all come from `last_closed`.  At most 15 rises are lost.

## 5. Bootstrap and typed resource boundary

Cheaply authenticate and normalize the input state first, then atomically
write that exact closed span as `BOOTSTRAP = last_closed` before constructing
the selective runtime or replaying the physical echelons.  Put module loading,
rank-51 reconstruction, all base/appended batch replay, profile/dual
construction, selective-runtime construction and search inside one typed
wall/RSS boundary.  Write `READY` only after reconstruction reaches the
authenticated closed rank.

Only an allowlisted internal wall/RSS stop or the exact 64-rise stop may emit
`status = terminal = UNKNOWN_RESOURCE`.  It must point to the physical
`last_closed`.  A non-resource exception is `UNKNOWN`, never checker-promoted.
The internal wall bound is strictly below the external supervisor timeout so
the closed fallback can be serialized.

## 6. Independent checker

The checker may share byte-pinned arithmetic primitives, but it must not call
the producer's search, resume parser, seal verifier, or fixture.  It
independently:

1. authenticates `C99` and semantically reconstructs rank 51, its eight
   records, and the three old Task451 batches;
2. checks the new binding/seal, exact prefix equality and segment continuity;
3. replays every appended row with the actual selector literal, exponent,
   fresh retained-only `seed_v12`, forbidden-`E`, scalar, row digest,
   nonmutating predicted pivot, actual add pivot, and post-batch dual/remainder;
4. checks `rank = 99 + appended rows` and the exact segment cap; and
5. accepts only a full positive replay or an allowlisted resource terminal
   whose referenced physical checkpoint equals the last closed state.

Mutation tests must execute these real validators.  In particular they reject
changes to the base prefix, old/new batch anchors, selector/delta, exponent,
row/scalar, predicted or actual pivot, post state, segment start/end, 63/65
cap cases, open batch, missing physical fallback, repeated-dot/non-JSON input,
and any zero-work synthetic success marker.

## Consequence

Once Task467 passes and an implementation of this transform passes an
independent audit, `C99` can seed repeated actual 16-rise continuations.  A
checker-approved `COMMON_CANDIDATE` would close A0's present finite gate and
feed the explicit-lift construction.  Until that positive result exists, A0
remains `0/1 actual`; rank 99 is progress in the finite selector, not a fake or
an Ihara witness.
