# Luna task 166: g760 target6 append-only delta checkpoint v4

Date: 2026-08-26
Role: Luna / implementation and bounded mechanical audit only

## 1. Purpose

Task 165 added exact j=9 caches and a lossless checkpoint after each complete
D2 relator.  Its v3 checkpoint repeats the entire pivot dictionary eleven
times.  At j=9 the registered uncompressed worst case is 3.801 GiB across the
eleven copies, and it grows sharply for j=10--12.

Build a versioned v4 adapter which keeps the v3 mathematical traversal and
both exact caches unchanged, but writes only the pivots newly appended by the
just-completed relator.  Replaying the authenticated delta chain must recover
the exact same `F3BitEchelon`, including its insertion order, at the exact next
relator.  This is resource recovery only, never a membership claim.

GHA runs `32966890811` (v2) and `32972580814` (v3) are live.  Do not touch,
cancel, resume, dispatch, or inspect them; parent Sol is the sole broker.

## 2. Inputs and fixed scope

Read and pin task/reply 165 and all v3 inputs.  Preserve exactly:

- g760, its SHA, inherited candidate prefix `[2,3,4,5,6,7,8]`, and fresh
  order `[9,10,11,12]`;
- saturated `(x_i-1)` BFS, D2-first row order and first-NONMEMBER rule;
- left-multiplication and per-j Jennings caches, their runtime equality
  canaries and `--disable-accelerators` fallback;
- 21,000-second inner cap and 5,600 MiB RSS cap;
- helper-nonshared v2 direct checker as the mandatory later replay of any
  producer NONMEMBER.

Do not modify v1/v2/v3, workflows, proofs, CLAIMS, or the Sol reply.

## 3. Allowed new files

Use versioned v4 paths only:

1. delta-checkpoint producer/adapter;
2. ASCII/LF-only producer GHA driver;
3. bounded preflight/schema certificate;
4. `sol/luna_reply_166_r07_target6_delta_checkpoint_v4.md`.

## 4. Exact append-only invariant

Before using a delta, assert mechanically after every relator closure that:

1. every pivot present before the closure remains present afterwards;
2. its two bitplanes are byte-for-byte/int-for-int unchanged;
3. the post-closure insertion-order list has the pre-closure list as an exact
   prefix;
4. `new_pivots` in the closure receipt equals the suffix length and rank
   increment.

Fail closed if any assertion fails.  Do not silently fall back to a lossy
delta.

## 5. Delta payload and state commitment

After relator k, atomically publish an immutable deterministic-gzip canonical
JSONL delta with at least:

```text
schema/version and canonical self-digest
j, completed_relator_prefix, next_relator
dimension/Jennings/target/legal/static and all source pins
prior-j record and exact prior-delta filename/SHA/bytes/state commitment
rank before, rank after, delta count
new pivot rows in original insertion order
cumulative insertion-order commitment
cumulative exact-state commitment
cumulative closure receipts
all global mathematical claims false
```

Use the same canonical F3 pivot row encoding as v3.  Define the cumulative
state commitment explicitly and domain-separate it.  It may be an append-log
hash chain, provided replay from the root recomputes it from the actual pivot
rows and also checks the final exact pivot dictionary/rank.  Do not rely on a
claimed digest without reconstruction.  No pickle or implementation-dependent
object graph.

## 6. Resume and completed-j binding

- Fresh start is j=9 relator 1.
- A v4 delta checkpoint resumes the same j at its exact next relator only
  after loading and authenticating every ancestor delta and replaying every
  pivot row in original insertion order into a fresh echelon.
- After relator 11, bind the reconstructed terminal state and exact closure
  receipt roster to the ordinary completed-j public row, then continue at the
  next j.
- Reject missing/reordered/duplicated ancestors, chain splices, wrong prior-j
  anchors, stale files, path substitution, rank gaps, changed old pivots,
  malformed new pivots, terminal skips, and forged/recomputed partial headers.
- A resource stop preserves completed deltas only and makes no claim about an
  interrupted relator.

Cross-run artifact ingress is not authorized in this task.  State plainly
that a later GHA run can resume only when the complete v4 chain is preseeded.

## 7. Bounded audit

Run serial local syntax/selftest/preflight only.  No full j=9 run, no parallel
Python/GAP, no git, push, workflow edit, or GHA dispatch.

Tests must include:

- toy multi-delta round trip and exact next-relator resume;
- equality with v3/legacy closure on all 59,049 j=2 PC elements and all eleven
  j=2 relators, including pivot dictionary and insertion order;
- deterministic j=9 accelerator samples;
- mutation rejection for delta bit flip, old-pivot rewrite, rank gap, order
  change, ancestor deletion/duplication/reordering, prior-j splice, closure
  roster splice, cumulative-state commitment forgery, noncanonical row, and
  stale-file injection;
- deterministic byte-equal preflight generation;
- an exact storage-accounting identity showing that the sum of delta pivot
  rows over eleven relators equals the final pivot count/row payload once,
  not eleven full copies.  Do not claim gzip size or full-run speed before GHA.

The driver must pin every input, run one producer and zero checker processes,
hash every delta/j checkpoint, and preserve all terminal claim boundaries.

## 8. Report boundary

Report paths, bytes, SHA-256, exact commands and outputs, mutation count,
cache equivalence, delta replay receipt, and remaining operational UNKNOWNs.
Repeat verbatim:

```text
delta checkpoint = resource recovery, not a mathematical result
inherited j2..8 = producer control-flow candidate only
fresh NONMEMBER = candidate until helper-nonshared direct checker agrees
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```
