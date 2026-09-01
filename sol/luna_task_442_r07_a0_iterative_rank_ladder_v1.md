# Luna Task442 — A0 iterative quotient-weighted rank ladder v1

Role: Luna implementation owner.  This is a bounded implementation of
`proof_r07_a0_quotient_weighted_actor_column_generation_v409.md`, especially
Theorem 5.1.  Do not redesign A0, rebuild the old occurrence closure, add
unrelated SELFTEST machinery, edit a workflow, dispatch GHA, or run production.

## Objective

Turn the accepted `first_active` machinery into one same-process loop:

```text
rank-43 authenticated prefix
  -> exact six-action test for the current dual
  -> exact 44-seed weighted-fibre test
  -> add the first literal ACTIVE row
  -> recompute target remainder and dual
  -> repeat
```

The selective Q0/Gamma runtime must be built once and reused.  Every retained
row must strictly raise physical rank.  Persist only compact source data after
each rise; never serialize the packed physical echelon, Q0 stores, formulas,
or fibre caches.

This task may assume Task441 v6 passes the already-produced first ACTIVE row,
but the new producer must be self-contained and rediscover/replay it rather
than downloading an old artifact or changing `gap-run.yml`.

## Exact source pins and semantics

- Exact-pin and reuse the current accepted v4 producer
  `search/d972_r07_a0_actual_b72_first_active_v4.py` and its pinned v1 source.
- Preserve the actor-path construction, 40-byte singleton guard, all 44 actual
  formulae, complete 1,469,664-state Q0 roster, S0/S1/S2 membership, nine-state
  kernel fibres, direct 11-occurrence replay, normalized exponent checks, and
  strict physical rank-rise test.
- The mathematical universe is exactly v409 equation (1.7).  No bounded
  shortlex universe and no old occurrence-closure completion claim.
- `CURRENT_DUAL_CORRECTION_EMPTY` is not negative by itself.  A separator is
  permitted only after the exact six-action oracle and all 44 weighted formula
  fibres are both completely exhausted for the same current dual and the
  independent checker replays that exhaustion.

## Required producer behavior

1. Build the authenticated rank-43 `prefix` once.  Build the selective
   Q0/Gamma runtime once.  Cache data may be cleared between dual rounds if it
   depends on the old dual; fixed stores must be retained.
2. Maintain `accepted_sources`, initially empty.  A correction source is the
   compact tuple
   `(seed_index, delta_word, scalar, row_digest, pivot)`.  Action sources retain
   the existing exact six-action ancestry fields.
3. At every round, replay all accepted sources into the fresh in-memory
   `PackedEchelon` (or, within one process, add the live row immediately), then
   compute `phys.dual(target)`.  Record old/new rank, remainder digest, normalized
   dual digest, and target pairing.
4. Run the exact six-action oracle first.  If it yields a row, direct-replay it,
   require nonzero pairing and a strict rank rise, add it, checkpoint, and
   restart the round.
5. Otherwise compile the adjoint/formulae for the current dual and run the
   exact weighted fibre selector.  On ACTIVE, rebuild the literal conjugate,
   require formula scalar = direct physical scalar != 0, require normalized
   exponent divisibility, require strict rank rise, add it, append its compact
   source, atomically checkpoint, and restart the round.
6. If the target remainder becomes zero, recover the echelon coefficients and
   materialize the exact common correction word.  The positive replay must
   understand all prefix sources plus every new `DIRECT_CORRECTION` source:
   its literal atom is
   `delta_word * relator[seed_index] * delta_word^-1` with its F3 coefficient.
   Keep six-action ancestry separate.  Apply the existing v12 exactification
   lattice, then require exact exponent pair `(0,0)`, joint identity, direct
   all-seven replay, quotient correction replay, and exact target zero.  Only
   then return `COMMON_CANDIDATE`/`A0=true` for independent checking.
7. Expose a small `--max-rises` production control.  Hitting it is
   `UNKNOWN_RESOURCE:max_rises`, with a valid compact checkpoint; it is never
   NONMEMBER.  Time/RSS stops likewise retain the last completed rank rise.
8. A restart option may read only this version's authenticated compact
   checkpoint.  It must rebuild rank 43 and replay the listed compact sources,
   checking every stored rank transition/digest.  It must not require a large
   physical basis in memory beyond the normal live echelon.
9. Print one concise progress line after each strict rise, including
   `round`, `rank`, `accepted_count`, elapsed seconds, and RSS.  This is the
   production progress signal; do not add a heavy audit scan.

## Independent checker

The checker must not trust producer rows, pivots, formula scalars, target-zero,
or a declared separator.  Starting from the exact pinned rank-43 prefix, replay
the compact accepted sources in order and require every claimed rank transition,
row digest, pivot, normalized exponent condition, and current-dual nonzero
pairing.  For a positive terminal, independently reconstruct the selected word
from the final coefficients and rerun the v12 positive gates.  It may import the
old mathematical evaluators only through exact byte pins; do not share the new
producer's ladder/control-flow helpers.

For this task, a bounded fixture may exercise two synthetic rank rises, compact
restart, one mutation per compact source field, and positive reconstruction.
Do not run the 1,469,664-state production path locally.

## Authorized outputs only

- `search/d972_r07_a0_actual_b72_rank_ladder_v1.py`
- `crosscheck/check_d972_r07_a0_actual_b72_rank_ladder_v1.py`
- `search/d972_r07_a0_actual_b72_rank_ladder_gha_driver_v1.g`
- `sol/luna_reply_442_r07_a0_iterative_rank_ladder_v1.md`

In the reply give bytes/SHA-256, exact pins, fixture/mutation results, the
checkpoint schema, and a short memory audit.  Do not commit, push, dispatch, or
edit any other file.
