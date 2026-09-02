# Luna Task 533 — A4 bordered-echelon physical resume v1

## Role and objective

You are Luna.  Implement the paper-closed replacement in
`sol/proof_r07_boundary_quotient_bordered_echelon_v434.md` so that the saved
A4 `R:27`, `K_rank=0` physical state can be resumed without materializing two
rank-112,355 echelons.  This is implementation work, not a fresh mathematical
redesign.  Do not run the 841-MB production computation locally and do not
dispatch GHA or perform git operations.

Reply to:

`sol/luna_reply_533_r07_a4_bordered_echelon_resume_v1.md`

## Frozen inputs

Read these completely before editing:

- `sol/proof_r07_boundary_quotient_bordered_echelon_v434.md`;
- `sol/proof_r07_lazy_full_boundary_affine_kernel_algorithm_v272.md`;
- `sol/proof_r07_lazy_kernel_boundary_discrepancy_v273.md`;
- `sol/proof_r07_finite_active_coordinate_dual_oracle_v274.md`;
- `sol/proof_r07_mixed_echelon_action_and_adapted_ledger_v285.md`;
- `sol/proof_r07_a4_intraquery_physical_shard_resume_v425.md`;
- `sol/proof_r07_a4_actual_production_shard_wiring_v430.md`;
- `sol/sol_reply_532_audit_r07_a4_row27_resource_artifact_v1.md`;
- current producer `search/d972_r07_word_independent_successor_kernel_v25.py`;
- current checker `crosscheck/check_d972_r07_word_independent_successor_kernel_v35.py`;
- current driver `search/d972_r07_word_independent_successor_kernel_gha_driver_v47.g`.

The immutable base artifact is:

```text
run                 33579631937
job                 100090966487
head                efaa6234d5ea12c9f81dcb1f33f0609387964475
artifact            9831693721 / gap-run-out
ZIP bytes           841367330
ZIP SHA-256         2f77b0d3e24009a669761f1066e9e61dd79c88c14a85fd092e85cc11b70dd0b7
release tag         archive-gha-checkpoints
release asset       artifact_9831693721_gap-run-out.a4-row27-open-query.zip
physical query      R:27
physical sequence   1877
accepted/examined   112355/112376
physical B/K ranks  112355/0
```

The parent is independently streaming and publishing that exact raw ZIP.  Do
not substitute the API service identity or a newly repacked archive.  If the
release asset is not yet reachable, implementation and bounded fixtures may
proceed, but report the driver as transport-blocked rather than weakening a
pin.

## Deliverables

Create versioned successors only:

1. `search/d972_r07_word_independent_successor_kernel_v26.py`;
2. `crosscheck/check_d972_r07_word_independent_successor_kernel_v36.py`;
3. `search/d972_r07_word_independent_successor_kernel_gha_driver_v48.g`;
4. the designated reply.

Do not modify v25, v35, v47, a workflow file, v220, CLAIMS, or any other
file.  Temporary fixture data must live outside the repository.  The `.g`
driver is ASCII only.

## F1. One large owner, not an aliased double insertion

The production state must contain exactly one materialized large boundary
echelon.  Do not set `combined = boundary` while retaining the old
`add_boundary` double insertion; that would try to insert every row twice.
Implement an explicit bordered owner:

```text
large B echelon and one raw-boundary ledger owner
immutable ordered raw K rows
boundary-normal K rows z_i=N_B(k_i)
small coefficient-bearing Z echelon only
```

Membership is `N_Z(N_B(v))`.  The separating dual is pulled back through Z
in reverse order and then B in reverse order.  Its support-inversion
correlation remains the complete v272/v274 full-D test.

Do not keep copied `combined.rows`, copied `b_rows`, copied
`combined_ledgers`, or K-empty `(boundary_ledger,{})` objects for all B rows.
Use label-indexed views/references or deterministic accessors.  One extra
dictionary containing 112,355 references is acceptable only if justified in
the reply; a second copy of sparse row contents is not.

## F2. Full bordered semantics after K appears

This must not silently become a K=0-only mathematical oracle.  Retain the
immutable accepted K rows and for each current B compute

```text
z_i = N_B(k_i),  Q_i = boundary ledger removed from k_i.
```

The small Z echelon carries coefficient vectors in the raw K roster.  Export
the v273/v285 external equation

```text
r = v - Psi(Q) - sum_i c_i k_i,
Q = Q_B(v) - sum_i c_i Q_i.
```

After a new boundary rise, insert it only into B, recompute every `(z_i,Q_i)`
and deterministically rebuild Z.  Assert that its rank remains the number of
accepted K rows.  MEMBER, ZERO/K-rise, literal-word discrepancy, action
columns, queue exhaustion and anchor construction must continue to use the
same raw semantic grammar as v25.

If a full K-after-B implementation cannot be completed honestly in this
commission, return `STOP` and identify the first concrete missing invariant;
do not ship a production driver which would stop at the first K or call a
partial prefix A4 progress.

## F3. Streaming authentication and K=0 migration

Do not extract all 1,877 physical shards simultaneously.  Read the ZIP
central directory and process shard members one at a time.  For the producer
fast-resume path, authenticate the exact base ZIP and all existing v425/v430
head/shard seals, links, query binding, counters, epochs and physical entry
structure.  Additionally enforce every v434 section-7 migration equality:

- boundary and combined pivot/row/label equality;
- combined scale one and empty old-row reduction;
- insertion relation exactly `{label:1}`;
- empty `b_coefficients` and empty K formal part;
- equal combined/boundary ledger and formal boundary part;
- no K item/insertion anywhere;
- exact rank/event/epoch/counter/open-query/HEAD binding.

Load only the boundary copy into RAM.  A mismatch is a typed input rejection,
never a fallback to the duplicated v25 layout.

The independent checker v36 must not trust the producer's migration Boolean.
It must stream the base shards independently, reconstruct each selected
translated boundary column from its raw identity, replay chronological B
reduction with its own pivot convention or otherwise independent code, and
check the same semantic state.  If full replay exceeds its registered GHA
budget, return a claims-false `UNKNOWN_RESOURCE`; never promote mere
index consistency.

## F4. Base-plus-delta durability

Do not copy or re-emit the 841-MB base archive into every new checkpoint.
The new physical owner must be a base-plus-delta chain:

- exact base release URL, bytes, SHA, base physical HEAD identity, sequence
  1877, final internal seal and chain are immutable fields;
- only newly closed canonical correlation batches are written as new delta
  shards;
- the first new shard binds the old final seal/chain and numbering continues
  without ambiguity;
- the new small HEAD binds the base identity plus every new shard, the open
  query, cumulative counters, bordered ranks and state epoch;
- a resource stop publishes the last closed delta HEAD;
- a later resume reauthenticates the base and then only the ordered delta
  chain; it never reports a completed row unless the unique query terminal
  and row commit are durable.

Do not serialize the whole rank-112,355 state into one ordinary JSON at row
completion.  Either keep the authenticated base-plus-delta physical owner
across subsequent rows or supply an equivalently bounded handoff whose size
is proportional to new data.  Preserve v425's completed-row/open-query
separation.

## F5. Resource and progress behavior

- Charge ZIP/shard validation, B rows, B ledgers, K border, active keys,
  correlations, wall time and RSS honestly.
- Emit throttled progress with base shard ordinal during restore and the
  existing row/correlation counters during production.
- The GHA producer limit remains explicit and below the job envelope.  Do not
  increase the 8-GB semantic cap as the fix.
- Avoid per-row deep copies, repeated JSON canonicalization of the full base,
  full-shard lists copied into each HEAD, and keeping decoded shard bodies
  after their entries have been installed.
- No production SELFTEST, profiling sweep, dense comparison, or full replay
  is allowed ahead of the actual continuation command in v48.

## F6. Independent terminal and claim boundary

Preserve exclusive typed terminals.  Until producer completion and v36
acceptance, all A0/COMMON/NONMEMBER/lift/fake/Ihara flags are false.  A
RESOURCE result carries no A4 numerator.  A completed A4 positive result
still requires all 6,441 row terminals, K-action queue exhaustion, complete
action matrices, word/discrepancy replay, and anchor gates from v25/v35.

The driver must:

- pin all source/proof/checker bytes and SHA values transitively;
- download the exact release asset above and check size/SHA before Python;
- avoid whole-archive extraction;
- run exactly one actual producer first, then the independent checker only on
  a producer-positive branch (or a separately typed checker-only resource
  branch if explicitly justified);
- expose the exact artifact files needed for another base-plus-delta resume;
- contain no production fixture/selftest and no hidden broad traversal.

## Bounded tests only

Use tiny synthetic echelons and a temporary miniature ZIP to prove at least:

1. old combined and new bordered membership/remainder agree before and after
   an interleaved B-after-K insertion;
2. coefficient/ledger equations (v434 (3.2)--(3.3)) replay exactly;
3. old and bordered separating duals agree in K=0 and both annihilate B+K in
   nonzero K;
4. K rank survives deterministic B growth/rebase;
5. K=0 duplicate fields migrate once and each v434 mutation is rejected;
6. base-plus-delta interruption/resume equals uninterrupted execution;
7. no duplicate sparse row contents are retained in the large K=0 fixture;
8. resource and false-claim envelopes are exclusive.

Run only bounded syntax/fixture/transport checks.  Report every command,
elapsed time, bytes/SHA of all deliverables, measured tiny-fixture memory
owner counts, and an explicit GO/STOP recommendation for an independent
Sol(max) audit.  Do not describe fixture success as actual A4 progress.
