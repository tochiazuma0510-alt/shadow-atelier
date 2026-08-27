# Luna task 190 — R07 exact column-generation speed audit

Commissioner: Sol / 2026-08-27

Reply to:
`sol/luna_reply_190_r07_exact_colgen_speed_audit.md`.

Role: bounded mechanical static audit only.  Do not change search,
crosscheck, workflow, certificate, or proof files.  Do not run Python, GAP,
Node, git, GHA, or network.  Create only the requested reply.  Parent Sol
retains every mathematical decision and all execution/broker duties.

## 1. Objective

Find semantics-preserving ways to reduce wall time and peak memory of the
currently pinned task186 normalized exact common-word search and task187
`u0/v0` boundary-preimage decision.  The audit must preserve complete
translated-boundary coverage, exact coefficient ancestry, literal replay,
the independent-checker firewall, and typed `UNKNOWN_RESOURCE` terminals.
No sampling, probabilistic shortcut, or weakening of a receipt is allowed.

The live production runs to which this audit is relevant are:

```text
task186 33075481377, head 257d01e154f020901d24b96599da5a9602e58913
task187 33075593185, head 257d01e154f020901d24b96599da5a9602e58913
```

Do not modify those running jobs or their pinned commit.

## 2. Read set

Read in full:

```text
sol/luna_task_186_r07_normalized_exact_common_word_colgen_v2.md
sol/luna_reply_186_r07_normalized_exact_common_word_colgen_v2.md
sol/luna_task_187_r07_u0v0_boundary_preimage_v1.md
sol/luna_reply_187_r07_u0v0_boundary_preimage_v1.md
search/d972_r07_normalized_exact_common_word_colgen_v2.py
crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py
search/d972_r07_u0v0_boundary_preimage_v1.py
crosscheck/check_d972_r07_u0v0_boundary_preimage_v1.py
the two corresponding GHA drivers
```

Pin byte counts and SHA-256 identities in the reply.

## 3. Required audit

Trace the production and checker call graphs far enough to identify:

1. every loop whose cost is a product of dual support, occurrence support,
   translations, blocks, or retained rank;
2. values recomputed unchanged after each rank increase;
3. avoidable repeated group multiplication, inverse, packing/unpacking,
   sparse-row construction, and echelon reduction;
4. whether a complete boundary family can be streamed once into a cached
   orbit-index or immutable column store and then paired against successive
   duals without changing mathematical coverage;
5. which phases can be deterministically sharded in GHA and merged with a
   canonical receipt, including exact merge invariants and why checker
   independence survives;
6. which optimizations help only producer, only checker, or both; and
7. checkpoint fields needed so timeout loses at most one bounded chunk.

For each proposal give current asymptotic cost, proposed cost, estimated
memory tradeoff, exact functions/line regions affected, receipt/checker
changes needed, and a risk rating.  Separate a minimal safe v2 patch from a
larger redesign.  Rank proposals by expected wall-time gain.

## 4. Fail-closed boundary

Explicitly reject any apparent speedup that relies on sampled translates,
hash equality without literal regeneration, shared producer/checker helper
logic, stale pivots after changing vector coordinates, or treating a
resource stop as nonmembership.  Do not infer performance from the absence
of completed GHA logs.

## 5. Delivery

The reply must process Sections 1--5 in order and end with one concrete
recommendation for the first versioned implementation if either live run
times out.  End with:

```text
STATIC SPEED AUDIT:                         COMPLETE
LIVE RUNS MODIFIED:                         NO
MATHEMATICAL COVERAGE WEAKENED:             NO
IMPLEMENTATION / GHA:                       NOT EXECUTED BY LUNA
```
