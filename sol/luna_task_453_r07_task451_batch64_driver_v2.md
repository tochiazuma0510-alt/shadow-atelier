# Luna task 453: Task451 frozen-dual batch-cap 64 driver v2

Role: Luna implementation owner.  Make only a driver-level speed lane for the
already accepted Task451 producer/checker.  Do not change their Python code or
the registered candidate universe.

## Mathematical boundary

`sol/proof_r07_a0_dual_anchored_active_batch_v415.md` permits every directly
replayed rank-raising row seen by one frozen separating dual to be inserted
before recomputing the target dual.  The current driver uses `batch-cap 16`
and the producer/checker already impose a cumulative 64-rise cap.  This task
changes only the per-batch cap from 16 to 64, retaining the same total cap 64.

Consequences which must remain literal:

- same frozen rank-51 prefix and exact producer/checker pins;
- same deterministic `(seed,coordinate,target,fibre_cursor)` order;
- same direct scalar, pivot, word and positive replay gates;
- same closed-batch durability and open-batch discard;
- same 7,200-second producer cap and 4.8-GB RSS cap;
- same output/checker markers and no negative claim from RESOURCE;
- no Q0 copy, new SELFTEST, retry, worker pool, eager store or search-space
  expansion.

## Output scope

Create only:

```text
search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g
sol/luna_reply_453_r07_task451_batch64_driver_v2.md
```

The v2 driver should exact-pin the accepted v1 driver and apply one
cardinality-checked replacement of `--batch-cap 16` by `--batch-cap 64`, or
equivalently reproduce v1 with an exact byte-level diff proving that this is
the sole executable change.  Use a distinct external preamble guard and final
driver marker, while retaining fresh per-run `ci/out` paths.

Run only bounded static checks: source pin, patch cardinality, generated
driver byte/SHA, ASCII-only, and parse/load far enough to show the expected
external-preamble guard rather than executing production.  Do not run Python
production, GAP production, GHA, git or network.  Report exact bytes/hashes,
the literal diff, checks, and residual risk in the reply.

