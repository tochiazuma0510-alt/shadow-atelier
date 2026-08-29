# Luna task 407: A0 globally merged batch-64 successor v28

Role: Luna.  Versioned implementation and small local fixtures only.  Do not
edit v24--v27, commit, push, dispatch, or run the production search locally.

## Goal

Implement the paper-PASS contract in
`sol/proof_r07_a0_batched_history_free_discovery_v387.md` on top of the final
two-phase streaming producer
`search/d972_r07_history_free_positive_fast_resume_v26.py`.  The successor
must be able to resume the same authenticated v24 checkpoint directly, so it
can run on GHA in parallel with the one-column v27 transport baseline.

The only intended algorithmic change is boundary column generation with a
conservative `batch_cap=64`.  Keep
`heuristic_discovery_only=true`, `exact_cached_resume=false`, every existing
resource cap, correction oracle, positive materializer, final v278 acceptance
boundary, and worker lifecycle.

## Required batch semantics

1. Freeze one exact current dual for the whole epoch.  Scan all 104 active
   descriptors and every matching support pair through the existing disjoint
   complete worker cover.
2. Merge every worker accumulator globally in `F_3`, including cross-worker
   cancellation.  Delete global zeros and apply the existing canonical order
   only after that merge.  No shard-local top-b, truncation, or sampling.
3. Select the first `min(64, |A_lambda|)` global active indices.  The parent,
   not a worker, reconstructs each selected translated-boundary row, recomputes
   its nonzero pairing with the frozen dual, and reconstructs the full
   contributor sum/provenance.
4. Insert selected rows sequentially into the current reducer.  The first must
   raise rank.  Later rows that reduce to zero against the already enlarged
   span are counted and skipped, not treated as fatal.  Commit every retained
   row with its own immutable symbol/DAG/provenance.  Recompute the separating
   dual only after the retained prefix has been committed.
5. A resource stop during worker convolution discards the whole epoch.  A
   resource stop after a proper parent-materialized prefix preserves only that
   atomic committed prefix in the checkpoint; the unused suffix is discarded
   and a future resume computes a fresh dual.
6. Receipt/checkpoint accounting must expose at least requested batch cap,
   global active count, materialized count, retained-independent count,
   dependent count, and dual-rebuild count.  Do not call accumulator entries
   active or independent columns.
7. An empty active set or resource cap remains `UNKNOWN`; never emit a
   negative.  A target-membership candidate must pass the existing unchanged
   v278 full selected-support replay before any COMMON result.

## Minimal gates

- `batch_cap=1` reproduces the existing one-column result/provenance on a
  finite fixture apart from version/accounting metadata.
- Batch and repeated-one-column modes generate the same final span on a finite
  exhaustive fixture.
- Permuting worker completion/result order does not change the globally merged
  canonical batch.
- Cross-worker cancellation is tested before top-64 selection.
- A later selected row dependent on an earlier selected row is skipped while
  the first row raises rank.
- Row/scalar/contributor/provenance mutations are rejected.
- The generated production owner contains the two-phase streaming restore and
  has no legacy whole-file resume call.

Use new v28-or-later producer/checker/driver/workflow names.  The workflow may
bind the same prior run `33267817818`, artifact id `9721440597`, v24 member
bytes/SHA, and tracked 86 MB source ZIP/manifest.  Include pinned official GAP
4.16.0 setup, exact `${{ github.sha }}` checkout, fail-closed terminals, and
upload only `ci/out`.  Give the batch run its own artifact name.  Keep tests
small; no exhaustive production-like selftest.

Reply in `sol/luna_reply_407_r07_a0_global_batch64_v28.md` with exact files,
bytes/SHA, gates, and the dispatch contract.
