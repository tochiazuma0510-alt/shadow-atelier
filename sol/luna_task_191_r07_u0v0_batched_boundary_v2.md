# Luna task 191 — R07 `u0/v0` batched boundary-preimage v2

Commissioner: Sol / 2026-08-27

Reply to:
`sol/luna_reply_191_r07_u0v0_batched_boundary_v2.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP,
Node, git, GHA, or network locally.  Parent Sol owns mathematical audit,
repository brokerage, and execution.  Do not edit the running task187 v1
files or any workflow file.

## 1. Governing invariant and objective

Read the task187 instruction/reply and both v1 producer/checker in full.
Let `S` be the current retained boundary span and let `lambda` annihilate
`S` while pairing nontrivially with an unresolved target.  A complete v1
correlation returns every translated PB3/PB4 boundary column `b` with
`lambda(b) != 0`.

Instead of retaining only the first ACTIVE column and repeating the complete
correlation, process the entire canonically ordered ACTIVE list against a
working echelon and retain every column which raises rank.  This is exact:
the first ACTIVE column necessarily raises rank over the pre-batch span, and
later columns are accepted only by literal echelon replay.  After the batch,
reconsider both targets and compute a fresh dual only if needed.

The objective is a versioned, fail-closed v2 successor which reduces oracle
rounds without changing the decided space

```text
D = span of every left translate of the 2 PB3 and 11 PB4 boundary rows.
```

## 2. Authorized files

Create only:

```text
search/d972_r07_u0v0_boundary_preimage_batch_v2.py
crosscheck/check_d972_r07_u0v0_boundary_preimage_batch_v2.py
search/d972_r07_u0v0_boundary_preimage_batch_gha_driver_v2.g
search/certs/d972_r07_u0v0_boundary_preimage_batch_selftest_v2_20260827.json
sol/luna_reply_191_r07_u0v0_batched_boundary_v2.md
```

Pin exact byte/SHA identities of task187 v1, task179, and every imported
arithmetic source.  Copy or wrap v1 only behind exact authentication.  The
v1 files remain byte-for-byte unchanged.

## 3. Semantics-preserving producer changes

1. Precompute once, per runtime, every base-boundary occurrence record used
   by complete correlation: typed block/component, source element/blob,
   inverse, base coefficient, and relator index.  Do not pre-enumerate or
   sample translations.
2. For each dual, unpack each dual-support group element once.  Scan every
   support-times-occurrence pair exactly as v1, using `t=g*h^-1`, checking
   `t*h=g`, and accumulating all cancellations before declaring ACTIVE.
3. Materialize every ACTIVE translated row in canonical
   `(block,translation_blob,relator_index)` order.  Reduce it against the
   current working echelon.  Record it as retained exactly when it raises
   rank; otherwise record a literal dependency coefficient chain.
4. A retained row keeps complete v1 provenance, its pre-batch dual pairing,
   pivot, full coefficient ancestry, and rank transition.  A dependent row
   keeps its exact reconstruction from already retained rows.  No row is
   discarded silently.
5. Reconsider `u0` and `v0` after every bounded retained sub-batch and at the
   end of the ACTIVE list.  Stop a target as soon as exact membership is
   obtained.  A fresh dual is computed only after the entire current ACTIVE
   list, or after a registered resource-safe sub-batch boundary whose
   unprocessed ACTIVE suffix is checkpointed losslessly.
6. Memoize translated rows by their full typed key.  Cache only literal rows,
   never a pairing under an old dual.
7. Store a resumable checkpoint after each completed correlation and each
   retained sub-batch.  Resume must authenticate and replay every retained
   row from rank zero; stale pivots, duals, and reduced targets are not
   trusted.

Allowed decisions remain exactly `MEMBER_D`, `NONMEMBER_D`, and
`UNKNOWN_RESOURCE`.  `NONMEMBER_D` is legal only when a fresh complete
correlation has an empty ACTIVE list and the checker proves the terminal
dual conditions.  A resource stop during a scan or batch is never negative.

## 4. Independent checker

The checker must not import the producer or share its precomputation/cache
helpers.  Independently reconstruct the runtime, `u0/v0`, targets, complete
occurrence roster, every full correlation, canonical ACTIVE ordering,
retained/dependent classification, rank-zero echelon replay, coefficient
ancestry, target membership chains, and terminal duals.  Rebuild each
translated row literally and compare full rows, not hashes alone.

Require equality of the mathematical v2 decision with a direct serial toy
enumeration.  If a v1 production receipt is supplied optionally, compare
decisions and positive chains modulo literal span, while allowing a different
basis order.

## 5. SELFTEST and destructive controls

Use a bounded noncommutative toy in which one complete correlation returns
at least four ACTIVE columns, at least two are independent after batching,
and at least one later ACTIVE column becomes dependent.  Require fewer
correlation rounds than the one-column schedule while obtaining the same
span and both target decisions.

At minimum reject mutations of: one omitted ACTIVE key; ACTIVE ordering;
one cancellation; `t=g*h^-1`; a cached row under the wrong block; retained
versus dependent classification; one dependency coefficient; one pivot
ancestry entry; skipped target reconsideration; stale-dual reuse; incomplete
correlation labelled complete; truncated ACTIVE suffix omitted from a
checkpoint; sampled-as-complete; and resource stop changed to nonmembership.

## 6. Driver and performance receipt

Provide serial SELFTEST/PRODUCTION bindings, exact-one producer/checker
markers, fail-closed caps, fresh output, checkpoint upload compatibility,
and no workflow edit.  Record:

```text
complete correlation rounds
support-times-occurrence pairs per round and total
ACTIVE / retained / dependent counts per batch
row-cache hits and misses
rank gains
target reconsideration points
wall/RSS caps and terminal phase
```

Give conservative GHA wall/RSS estimates and a direct explanation of the
expected speedup relative to v1.  The reply processes Sections 1--6 in order,
lists exact identities of all five files, and ends with:

```text
BATCHED EXACT BOUNDARY DECISION:              NOT EXECUTED BY LUNA
MATHEMATICAL BOUNDARY SPACE CHANGED:          NO
TASK187 LIVE RUN MODIFIED:                     NO
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED
```
