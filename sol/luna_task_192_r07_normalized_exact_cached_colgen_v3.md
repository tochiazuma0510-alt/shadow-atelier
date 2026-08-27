# Luna task 192 — R07 normalized exact cached column generation v3

Commissioner: Sol / 2026-08-27

Reply to:
`sol/luna_reply_192_r07_normalized_exact_cached_colgen_v3.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP,
Node, git, GHA, or network locally.  Parent Sol owns mathematical audit,
repository brokerage, and execution.  Do not edit task179, task186 v2, any
currently running file, or any workflow file.

## 1. Objective and governing semantics

Read task186 and task190, including both replies and every pinned producer,
checker, fixture, and driver dependency, in full.  Build a versioned v3
successor of task186 which preserves exactly:

```text
nu(word) = (exp(word)/18) mod 3
the complete PB3/PB4 translated-boundary family
the complete positive weighted candidate schedule
rank-zero checkpoint replay after every semantic change
literal all-eleven/direct all-seven equality
word-bearing coefficient ancestry and closed exactification
helper-nonshared independent checking
typed UNKNOWN_RESOURCE
```

The only purpose of v3 is to avoid rebuilding dual-independent Fox/group
data and avoid rewriting a growing full checkpoint after every logical
attempt.  It must return the same mathematical result as v2 for every
completed finite schedule.

## 2. Authorized files

Create only:

```text
search/d972_r07_normalized_exact_common_word_cached_v3.py
crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py
search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g
search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json
sol/luna_reply_192_r07_normalized_exact_cached_colgen_v3.md
```

Pin exact bytes/SHA-256 of task186 v2, task179 v1, task190, and every
arithmetic dependency reached at runtime.  A wrapper or copied successor is
allowed only after those pins pass.  No v1/v2 source byte may change.

## 3. Immutable template and typed-value caches

Implement deterministic caches independently on producer and checker.
Cache contents are accelerators, never trusted receipt evidence.

### 3.1 Eleven-slot Fox template

For each authenticated roster word and each of the eleven fixed slots,
cache the dual-independent data currently rebuilt by
`AllSevenModel.occurrence_data/occurrence_column`:

```text
signed substituted relation word
typed block/coordinate/sign/lift/label
complete Fox gradient terms and quotient-identity value
occurrence prefix and its inverse
every base-value inverse and canonical blob
exact integer exponent pair before normalized reduction
```

The dual-dependent support join, mod-3 merging/cancellation, weighted
formula, and exact pairing are recomputed for every dual.  A selected
candidate still receives a fresh literal direct all-seven replay and must
equal the cached eleven-slot reconstruction.  Cache keys bind the full input
digest, roster layer/ordinal/literal word, slot identity, group type, and
normalized-semantics digest.

Use a deterministic bounded memory policy and, if helpful, a regenerable
content-addressed disk chunk cache outside the receipt.  Never exceed the
registered RSS cap.  Eviction only causes recomputation.  Record hit/miss,
eviction, bytes, and regenerated-literal counters.

Cache the three fixed base relation gradients used by `direct_column`, but
not a candidate-dependent corrected gradient unless its complete literal
word is part of the cache key.

### 3.2 Boundary descriptors

Precompute once the complete sorted PB3/PB4 source descriptor roster:

```text
(block,relator_index,component,h_blob,h_inverse,base_coefficient).
```

Unpack each dual-support element once per correlation.  Preserve the full
support-times-occurrence scan, all cancellations, `t=g*h^-1`, `t*h=g`, and
the v2 lexicographic ACTIVE choice.  Memoize a translated sparse row only by
its full typed `(block,relator_index,translation_blob)` key.  Do not batch
ACTIVE columns in this task; task191 audits that separately.

### 3.3 Candidate values

Cache all 243 immutable Gamma coordinate rows.  Add a deterministic bounded
cache for q0 section words/views and the ten typed coordinate blobs of a
fixed `(qid,gid)` candidate.  On the first cache fill perform the existing
parent/letter, coordinate, and literal section replay.  Selected candidates
retain their ordinary source words and all current direct gates.  Never
materialize the full `357128352` product roster.

## 4. Chunked fail-closed checkpointing

Replace per-attempt full checkpoint serialization by a registered fixed
chunk of at most 256 logical candidate/fibre attempts.  A full sealed
checkpoint is written at every chunk boundary, every rank increase, before
a clean terminal, and in the resource-stop handler.  Interruption inside a
chunk may repeat that complete chunk but may not skip any attempt or change
the canonical first-hit result.

Bind each resumable epoch to input/target/normalized-semantics/dual digests.
Retain the v2 rank-zero replay firewall: stored pivots, target remainder,
dual, and oracle state are discarded and every retained column is rebuilt
from literal provenance.  After that replay, accept progress only through
complete roster rows and complete chunks.  Required state includes:

```text
canonical_row_cursor over complete rows
per-row formula digest, K, W, Delta and kernel-order contract
support_fibre_cursor, kernel_cursor, global_prefix, complete
chunk_start, chunk_end, attempts_done, chunk_complete
all monitor counters and the exact canonical ordering convention
```

If a resource stop occurs before a safe serialization point, seal the last
safe cursor and explicitly declare the bounded repeated suffix.  No partial
row or partial chunk can be marked complete.  `UNKNOWN_RESOURCE` remains the
only resource terminal.

## 5. Independent checker and equivalence receipt

The checker must not import the producer or consume its caches.  It builds
its own templates/descriptors/value cache using an independently written
path, reconstructs every selected literal row and candidate word, and
replays the full v2 positive/exactification receipt.  Cache hit equality is
never accepted by hash alone.

For SELFTEST, run an uncached reference schedule and cached/chunked schedule
on the same bounded noncommutative fixture and require equality of:

```text
canonical attempted candidates
full weighted formulas
selected ACTIVE columns and order
rank/pivot/ancestry transcript
target solution
ordinary correction and c_exact
direct all-seven replay
terminal and resource counters modulo explicitly repeated resume chunks
```

Exercise interruption at every position of one 256-or-smaller toy chunk,
resume from rank zero, and prove that no attempt is skipped and the terminal
is unchanged.

## 6. Destructive controls and delivery

At minimum reject mutations of: one cache key component; a stale group
type; one slot sign/order; one Fox term; one prefix inverse; one boundary
descriptor; one dual-support decode; one section parent/letter; one typed
coordinate blob; cache hit without literal regeneration; chunk end advanced
early; incomplete row marked complete; skipped/reordered resumed candidate;
stale dual progress; raw-mod-3 semantics; old-pivot reuse; coefficient-two
word repetition; one exactification cube; and resource stop changed to a
mathematical terminal.

Provide serial SELFTEST/PRODUCTION driver bindings, exact-one producer and
checker markers, fresh output, fail-closed caps, checkpoint/artifact upload
compatibility, no workflow edit, and conservative GHA time/RSS estimates.
The reply processes Sections 1--6 in order, lists exact identities for all
five files, reports expected cache/chunk gains without claiming measured
speed, and ends with:

```text
CACHED NORMALIZED FIRST-EDGE WORD:            NOT EXECUTED BY LUNA
V2 MATHEMATICAL SCHEDULE CHANGED:              NO
LIVE TASK186 RUN MODIFIED:                     NO
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED
```
