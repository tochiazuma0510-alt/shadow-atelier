# Luna Task490 - rank-99 durable discovery v4 exact audit repair

## Role and boundary

You are Luna.  Produce one versioned successor to rejected Task482 v3.  Repair
exactly the six dispatch blockers in
`sol/sol_reply_489_audit_r07_rank99_durable_discovery_v3.md`; do not redesign
the mathematics, run production, add a cache framework, or edit v3.

The external premise is now fixed: the 56-source/rank-99 input prefix is
CROSS-CHECKED by Task487 and v220 Delta344.  Preserve the v424 candidate
order, v426 rolling resource chain, v427 short-batch flush, all frozen source
pins, and the strict resource margins from v3.

## Exact required repairs

1. **Shared producer marker.**  Give the checker an explicit pinned producer
   marker and require the producer artifact's
   `..._V4_RESOURCE_CANDIDATE` / `..._V4_COMMON_CANDIDATE`.  Keep the checker's
   own `_CHECKER_PASS` marker only for checker output.  A bounded receipt made
   with the real producer marker must enter the real checker gate; the old
   checker-marker receipt must be rejected.
2. **Immediate predecessor content and READY seal.**  For an own-schema
   resume, parse/authenticate the immediate checkpoint exactly once and carry
   that parsed state into validation.  At the next committed segment, equate
   its complete start prefix, counts, rank, round, profile and rolling ledger
   to that immediate predecessor, and bind `prior_state_seal` to the actual
   authenticated predecessor READY/state seal, not to a newly recomputed
   unrelated compact-core hash.  Retain one flat chronological O(n) walk; do
   not reopen or copy cumulative ancestors.  Add a same-count/different-prefix
   immediate-predecessor mutant that the real validator rejects.
3. **Zero-progress resume.**  Do not rebind the durable state's historical
   `input_checkpoint` before a new segment commits.  A soft zero-row stop or
   hard stop before the first close must return a state accepted by its own
   validator (preferably the prior durable state byte-for-byte); record the
   current invocation input separately in the result if needed.  After a real
   close, the current input identity and new segment must bind consistently.
   Exercise a real own-schema zero-progress rebind/fallback through the
   production helpers and validate the result.
4. **One retained-candidate ABI.**  Factor the actual correction retain order
   (nonmutating reduce, dependency skip, literal reconstruction/exponent/
   scalar gates, exactly one add, predicted=actual pivot) into one helper used
   by `run`.  The bounded fixture must call this same helper; delete or stop
   advertising any fixture-only duplicate.  Preserve the action path's exact
   direct gates.
5. **RESOURCE is not COMPLETE.**  Keep one producer and a checker only on
   COMMON.  After shell return, inspect the exact owned OK content.  RESOURCE
   must emit a distinct resource terminal and must never print the global
   COMMON `..._COMPLETE` marker.  Only a checker-approved COMMON may print
   COMPLETE.  Add a bounded generated-shell branch gate for both paths.
6. **COMMON profile and resource counts.**  Store the actual profile dictionary
   after every batch update, including `dual is None`, so a post-batch COMMON
   replays exactly.  Repair the checker resource predicates so
   `segment_rises` is treated as the invocation aggregate: a committed soft
   flush checks its final batch's local 1--16 rows, while zero-current-row and
   failed-close rollback may legitimately retain earlier committed rises.
   Validate receipts with aggregate rises 17 and the three v3 false-rejection
   shapes, plus a bounded injected post-batch COMMON profile.

## Gates

- Re-run all Task480 F1--F6 gates, not only the six new regression cases.
- Producer fixture and checker self-test/pin-check must use real production or
  real envelope entry points for the load-bearing predicates.
- AST must show real `run` calling the retained-candidate helper and every
  adjoint call targeting `v4.tau_free_adjoint(P,m,args)`, never the one-argument
  v2 helper.
- Preserve literal top-level/durable equality before replay, flat O(n) chain,
  atomic close/rollback, `14040 < 14220 < 14400`,
  `4200000000 < 4500000000 < 5120000000`, one producer, and at most one
  conditional checker.
- Use temporary files outside the repository.  Run only bounded fixtures,
  AST/static checks, generated-shell `bash -n`, and GAP parse.  No production,
  GHA, git, authority computation, persistent framework, or unrelated edits.
- If a Windows symlink fixture remains privilege-limited, state that honestly;
  do not weaken the production path guard.

## Exact outputs

Create only:

1. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py`
2. `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py`
3. `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v4.g`
4. `sol/luna_reply_490_r07_rank99_durable_discovery_v4.md`

Report final byte counts and SHA-256 pins.  End exactly
`TASK490_R07_RANK99_DURABLE_DISCOVERY_V4_PASS` or a typed STOP.
