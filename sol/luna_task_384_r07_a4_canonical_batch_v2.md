# Luna task 384 - A4 canonical exact batch v2

Commissioner: Sol / 2026-08-30

Reply to `sol/luna_reply_384_r07_a4_canonical_batch_v2.md`.

Role: bounded mechanical implementation only.  Parent Sol owns mathematics,
git, network, GHA dispatch and promotion.  Read task383 and its reply in full,
then read the complete v13/v15 generated sources before editing.

Edit only these four new files:

```text
search/d972_r07_word_independent_successor_kernel_v14.py
crosscheck/check_d972_r07_word_independent_successor_kernel_v16.py
search/d972_r07_word_independent_successor_kernel_gha_driver_v23.g
sol/luna_reply_384_r07_a4_canonical_batch_v2.md
```

Do not edit v13/v15/v22, a workflow, proof, v220, ledger, cert, fixture or
input.  Do not run production, GHA, git, network, SELFTEST or a mutation
campaign.  Static generated-source parse/loading, ASCII scan, frozen-owner
restoration and GAP `ReadAsFunction` parsing are allowed.

## 1. Exact mathematical batch

Preserve every v13/v15 arithmetic, checkpoint and terminal rule.  Change
only the existing dual-column loop.  One complete correlation already forms
the full accumulator of dual pairings with every raw translated boundary
column, but v13/v15 insert only the first nonzero candidate and recompute the
same expensive correlation.

For one fixed dual and its complete accumulator:

1. enumerate all nonzero candidate keys in the existing canonical ascending
   `(context, relation, token)` order;
2. scan that order, reconstructing each literal boundary column;
3. reduce the column against the **current combined basis**, after every
   preceding insertion in this batch;
4. skip it if that current reduction is zero;
5. otherwise call the unchanged exact `add_boundary`, retain its complete
   ledger/event ancestry, and emit one ordinary chronological
   `BOUNDARY_RANK_RISE` record with the same fixed dual digest, complete
   accumulator digest and pair count; and
6. stop after exactly 64 rank-raising insertions or exhaustion of the
   nonzero candidate roster, whichever comes first.

If the correlation has a nonzero candidate, at least the first is outside
the pre-batch combined span.  Require that the accepted count is positive.
After the batch, return to the existing outer loop, reduce the target against
the enlarged basis, and compute a new dual/correlation only if still needed.
The zero-correlation terminal and K-rank-rise rule remain byte-for-byte in
meaning.

Do not insert a candidate merely because its old dual pairing is nonzero;
the current combined-basis reduction in item 3 is load-bearing.  Do not use
the boundary-only basis for that test.  Do not scale or sum candidates, alter
their raw identities, or treat skipped candidates as insertions.

## 2. Minimal ABI rule

Keep the public correlation object and every existing receipt/checkpoint
record schema unchanged.  It may still expose `selected` as its first
canonical nonzero candidate.  Return the bounded/scannable candidate roster
to the caller through a private generated-source interface which is not
serialized into `live_duals` or the public correlation digest.  The full
accumulator digest remains the completeness owner.

Each accepted candidate uses the existing one-insertion record schema.  It
is valid for several consecutive records to have the same `query_id`,
`dual_digest`, `pair_count` and `accumulator_digest`; their `selected`,
column, ledger and rank fields must differ as actually computed.  Existing
insertion events, epoch recurrence, query-event chain and checkpoint owner
therefore remain chronological without a schema migration.

Update progress so `accepted_batch_size` is the number of actual independent
rank rises from the most recent correlation, in `1..64`, or zero at a true
zero correlation.  Do not add an audit-only hot path or retain the whole
candidate roster in a checkpoint.

## 3. Independent checker order adjudication

This v2 commission expressly supersedes task383's request for a different
batch pivot order.  Producer and checker must use the same pinned canonical
ascending candidate order because the current positive ABI deliberately
compares chronological K ancestry and action matrices.  Rewriting that ABI
is unnecessary for this speed repair.

Independence is retained because v16 restores the independent v15 owner,
reconstructs the full correlation accumulator through its own arithmetic,
performs every current-basis reduction itself, replays every raw boundary
identity and insertion, and finally retains the existing two-way pure and
mixed span comparisons.  It must not import v14 or copy a producer-selected
batch.

Add fail-closed generated-source assertions that:

- batch cap is exactly 64 on both sides;
- every accepted item passed a nonzero current combined reduction;
- accepted count is positive iff a nonzero roster branch was taken;
- one dual event is retained per complete correlation, while every accepted
  insertion retains its own ordinary event; and
- the public correlation digest excludes the private candidate roster.

## 4. Driver and delivery

The v23 driver is the smallest successor of v22: update only v14/v16 code
paths, exact byte/SHA pins and v23 output names/markers.  Preserve
PRODUCTION/RESUME, the v13 early completed-row checkpoint semantics, 14,400
internal seconds, 8 GB registered RSS, diagnostic tails and artifact
transport.  No fresh run may consume a v13 checkpoint because its code pin
differs; the first v14 run is fresh.  A later v14 resource terminal must be
resumable from the v14 checkpoint.

The reply must list exact files, bytes/SHA, frozen and generated-source pins,
the precise patch cardinalities, static commands, and any blocker.  Estimate
the reduction in full correlations from the actual rule, but do not claim a
wall-time speedup before production measurement.  End with:

```text
EARLY COMPLETED-ROW CHECKPOINT:                   RETAINED
CANONICAL CURRENT-BASIS BATCH CAP:               64
PUBLIC RECEIPT/CHECKPOINT SCHEMA MIGRATION:       NONE
INDEPENDENT CHECKER RECOMPUTATION:                RETAINED
PRODUCTION / A4 ACCEPTED WORD-BEARING K:          NOT RUN / NOT DECLARED
```

`TASK384_A4_CANONICAL_EXACT_BATCH_V2_COMMISSIONED`
