# Luna task 157dz — WordExpr memo-v9 checker pool-schedule successor

## Scope

Create only these four versioned files:

1. `search/check_d972_b345_relfrat3_wordexpr_memo_v10.py`
2. `search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v10.g`
3. `sol/luna_task_157dz_b345_relfrat3_checker_pool_schedule.md`
4. `sol/luna_reply_157dz_b345_relfrat3_checker_pool_schedule.md`

The producer `search/d972_b345_relfrat3_wordexpr_memo_v9.py`, its registered
4096-candidate order, predicate, receipt schema, q3 input, v1--v9 sources, and
workflow are frozen and must remain byte-identical.  Do not run GAP, GHA, Git,
or a full producer/checker computation.

## Frozen diagnosis

The v8 full run reached producer terminal
`B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE` after all 4096 candidates, then the
checker failed at the combined message `checker scan record
bindings/distribution`.  The packed outcome replay immediately before that
gate passed.

There are two checker-only pool-schedule omissions inherited by v9:

1. The producer constructs the base D2 basis and then persistently interns the
   six values of `raw_base_source_key` before the BFS.  The checker constructs
   the same basis but does not intern those six frozen anchors.
2. Every producer target probe is inside a candidate transaction and rolls
   back its element-pool suffix.  The checker `first_missing()` probes at BFS
   checkpoint 1 and every directed round without rollback, leaving transient
   target-prefix elements persistent.

Canonical packed outcomes can remain identical while the public
`pool_suffix_removed` field differs, which then changes both the public row and
the full-record digest.

## Required repair

- Keep the memo-v9 producer and `/v9` receipt schema/output path.
- In the independent checker, after the base `ReplayBasis` is constructed and
  before the BFS, intern the exact ordered frozen six-element source tuple.
- Wrap every `first_missing()` target probe in a pool checkpoint/rollback.
  Copy the blocker bytes, component, and unpacked value before rollback;
  `ReplayBasis` is immutable during a probe.
- Preserve persistent BFS and directed-translation inserts exactly.
- Strengthen rollback deletion to verify exact blob-to-ID suffix bindings if
  this remains local to the checker.
- Split the final aggregate check into separately named fail-closed gates for
  public record bindings, the full-record digest, and failure distribution.
  For a row mismatch report only the first candidate and first field with a
  bounded value/digest diagnostic.  Do not weaken any equality.
- The v10 driver must execute the byte-identical memo-v9 producer and the new
  v10 checker in the same job, pin both exact source hashes, retain stale-file
  cleanup and q3 regeneration/checker gates, and use distinct v10 logs and
  markers.  The produced artifact remains the registered v9 JSON.

## Self-test and freeze

Add a bounded checker regression using six distinct nonidentity source anchors
and a target probe that interns at least one new value.  It must show:

- anchors persist in exact order;
- the transactional probe returns copied evidence but leaves pool size and
  blob bindings unchanged;
- the old unscoped pattern would pollute the pool;
- an anchor-count mutation is rejected.

After all source and driver pins are final, run at most one combined lightweight
producer+checker self-test.  No other local execution is authorized.  Record
the exact command/result, hashes, bytes, unchanged producer hash, and terminal
marker in the reply.

