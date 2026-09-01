# Luna Task482 — rank-99 durable discovery owner v3

## Role

You are Luna.  Produce the smallest dispatchable successor to the rejected
Task472 v2.  Read and obey:

- `sol/sol_reply_480_audit_r07_rank99_actual_owner_v2.md`;
- `sol/proof_r07_rank99_actual_owner_transform_v424.md`;
- `sol/proof_r07_rank99_cached_discovery_chain_v426.md`; and
- `sol/proof_r07_deadline_flush_short_batch_v427.md`.

Do not edit v2.  Do not redesign the selector, add a persistent cache, or run
production locally.

Frozen v2 starting point:

```text
producer 64344 24eededdb4f8d2718c9dc33eb090b1f2c8cbf6dfdf5c40c32e140cb61eae07f9
checker  47201 542a4d6cda7503d27e5247742cc3f44418cf3449235eb5073e61600f369d5418
driver    5320 8f776180c0f948d8fc909c4a01c4196654970a720ecdbb8466b8c55e26dcf5e2
```

## Mandatory correctness repairs

1. Every real frozen-prefix/batch correction must call the pinned rank-ladder
   v3 wrapper `v3.tau_free_adjoint(P,m,args)`.  The bound v2 helper has ABI
   `tau_free_adjoint(P)` and must never receive three arguments.  Keep
   update/pair/profile on their correct frozen owner.  Exercise the actual
   production replay entry through an injected bounded fixture; an unused
   helper or hard-coded capability flag is not a test.
2. Before physical replay, the checker must equate every duplicated top-level
   state field to the durable checkpoint: base/appended batches, chronological
   records, accepted sources/count, batch count, round, physical rank/rank,
   current profile, segments and C99 identities.  A re-sealed top-level row
   mutation with the durable checkpoint unchanged must reject before replay.
3. Replace the cumulative historical-file walk by one chronological prefix
   validator.  Use a rolling canonical digest from C99 through each appended
   batch; store/bind segment start/end prefix digests, complete row prefixes,
   counters and READY predecessor seal.  Read/authenticate only the immediate
   resume checkpoint once.  Do not reopen every cumulative ancestor.  Bind
   each batch round consecutively and require
   `end_round-start_round=end_batch-start_batch` for each segment.  Include a
   two-segment same-count/different-row mutant and an instrumented one-input-
   read gate.  Final semantic replay, not trust in old segment files, remains
   the proof.
4. Factor the retained-candidate ABI used by production so its fixture calls
   the same function.  Exercise a real own-schema file resume and an actual
   symlink-escape rejection using temporary paths outside the repository.

## V427 durability boundary

Introduce distinct search-soft, internal-hard and external limits.  A soft
time/RSS stop raised inside candidate enumeration returns to the batch owner.
If zero rows are retained, publish the preceding `last_closed`.  If 1--16
rows are retained, perform exactly one ordinary post-batch update, append the
short closed batch/segment with its actual length, atomically write it, and
publish that new `last_closed`.  A recognized hard resource stop during close
falls back to the preceding seal; invariant/programming exceptions propagate.
Never serialize an open echelon.

Fixtures must cover flush after 1 and 15 retained rows, resumed equality at
the same early-close point, zero-row fallback, forced hard-close rollback,
and rejection of zero/17-row closed batches.  Per invocation remains at most
64 rises.

## V426 discovery-chain execution

Resource segments are producer-authenticated candidates, not cross-checked
results.  The driver must not run the expensive independent semantic checker
after an `UNKNOWN_RESOURCE` segment.  It authenticates exact producer markers,
nonempty sealed receipt/checkpoint and a fresh candidate marker, then exits so
the workflow uploads them.  The next owner reauthenticates and semantically
replays the complete prefix.

For `COMMON_CANDIDATE`, the same driver must run the independent checker over
the entire chain and issue COMPLETE only on exact PASS.  No resource/miss is a
negative claim.  Keep enough total workflow reserve for this terminal replay;
do not configure two sequential four-hour supervisors.

Use an explicit safe envelope with strict inequalities, statically tested:

```text
search soft wall < internal hard wall < producer external wall
search soft RSS  < internal hard RSS  < hard VM bytes
```

The hard VM margin must be real, not the Task472 equality
`4687500*1024 = 4800000000`.  Keep BOOTSTRAP, READY, atomic fsync/replace,
fresh paths, one producer, at most one checker, and exact branch markers.

## Bounded gates

Run AST/fixture/checker self-test/pin-check/GAP parse and static process/
timeout/RSS gates only.  Do not run the actual authority construction, GHA,
git, or create bytecode caches.  Report exact live pins and whether a later
COMMON-only artifact driver is needed.

## Exact outputs

1. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v3.py`
2. `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v3.py`
3. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v3.g`
4. `sol/luna_reply_482_r07_rank99_durable_discovery_owner_v3.md`

End with `TASK482_R07_RANK99_DURABLE_DISCOVERY_V3_PASS` or a typed STOP.
