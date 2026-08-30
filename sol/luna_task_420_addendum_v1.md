# Addendum to Luna task 420 - replace shortlex by the exact occurrence queue

Read `sol/proof_r07_a0_partial_boundary_occurrence_selector_v405.md`
completely.  It supersedes task420's instruction to reuse the bounded
task413 conjugator iterator.  Do **not** use a length-six or other arbitrary
conjugator cap in v2.

Implement the exact two-owner selector of v405 within the same four allowed
task420 outputs:

1. Keep all eleven correction occurrences separate.  On each of the six
   PB3 occurrences apply the full v401 normal map; on each of the five PB4
   occurrences apply only the v402 five-central-family normal map.  Keep the
   normalized exponent pair as a trivial-action summand.
2. Insert the 44 compact occurrence rows and close the occurrence quotient
   under the four frozen prefix-conjugated source actors
   `x,x^-1,y,y^-1`.  Enqueue children only for an occurrence-rank-raising
   pivot.  This is the exact `44+4*r` queue, not a joint-state or shortlex
   enumeration.  Store literal seed/conjugate/product/inverse ancestry.
3. Only after an occurrence pivot has been formed, aggregate its eleven
   tagged components into the two PB3 and one PB4 physical blocks and insert
   that aggregate into the separate physical echelon.  Physical dependence
   must never suppress occurrence-level children.
4. After the occurrence queue exhausts, use v404's exact six-action
   `t=g*h^-1` oracle on the physical remainder.  An empty accumulator is then
   conclusive for the six families because the correction queue is complete.
5. Checkpoint and restore both echelons, the occurrence frontier, source DAG,
   physical source references, six-action ancestry and all deterministic
   cursors.  Resume must match an uninterrupted bounded fixture.
6. A positive result still requires every v403 gate.  A negative result may
   be emitted only after independent replay of the exhausted occurrence
   invariant closure and an empty exact six-action accumulator; if that
   independent negative replay is not implemented in v2, return
   `UNKNOWN_RESOURCE` rather than NONMEMBER.

This addendum removes the last heuristic search universe.  It does not
authorize a full local run, multiprocessing, SAT, workflow edits, or any
additional output file.

`TASK420_ADDENDUM_V1_EXACT_OCCURRENCE_QUEUE`
