# Luna task 265 - task227 NONMEMBER remainder and complete reconstruction repair v1

Role: bounded implementation repair only. Read task248, task257, task261,
the current five task227 files, and this second parent rejection in full. Do
not run Python, Node, GAP, git, GHA, or network. Edit only the same five
task227 files plus the existing task227 Luna reply.

## Exact parent rejection after task261

The current return cannot be executed or counted for A3.

1. `closure` computes `(remainder, c_i) = reduce_with_ancestry(...)` but drops
   the block remainder. Both producer and checker then unconditionally require
   `sum_i c_i C(w_i) == target`. This is true only for MEMBER. For NONMEMBER,
   the exact relation is

       sum_i c_i C(w_i) + block_remainder == target,

   with a nonzero canonical block remainder. Consequently every genuine
   NONMEMBER SELFTEST case is rejected before the dual certificate is read.
2. Serialized `block_echelon` is checked only for list shape and nonempty
   decoded rows. Neither implementation independently rebuilds the canonical
   echelon, pivots, or coefficient ancestry from `block_basis`.
3. The producer calls `independent_orbit(..., Budget())` with a fresh
   unmetered budget inside validation. Validation must use the invocation
   budget and remain subject to the declared caps.
4. The baseline resource datum is an unsealed four-key dictionary. Task261
   required an extant sealed typed resource-terminal canary.
5. The producer mutation `occurrence_basis_row` replaces a row by another
   well-shaped row, so the earlier ancestry replay naturally owns the failure
   (`CASE_OCCURRENCE_ANCESTRY`) instead of its preregistered
   `CASE_OCCURRENCE_BASIS`. The checker has the analogous natural-order risk.

## Required repair

1. Preserve and serialize `block_remainder` from the exact reduction. Decode,
   canonicalize, and independently validate it in both producer and checker.
   Require in all cases

       block_combined + block_remainder == target.

   Require `case.member` iff the exact terminal is MEMBER. For MEMBER require
   `block_remainder == 0`, quotient zero, and the complete replay/target chain.
   For NONMEMBER require `block_remainder != 0` and then validate the full dual
   certificate. Do not confuse this block remainder with the actor
   `quotient_remainder` used in the lambda/kappa division.
2. Independently rebuild the canonical block echelon from decoded
   `block_basis`, including pivots and coefficient ancestry, and require exact
   equality to the serialized `block_echelon` and `block_rank` in producer
   and checker. The rebuild must not use a serialized echelon entry as input.
3. Use the active invocation budget for the independent orbit/span rebuild;
   no fresh `Budget()` that bypasses the resource contract.
4. Replace the baseline resource object with a typed sealed canary containing
   an exact resource terminal (`UNKNOWN_RESOURCE`), phase, cap, value, limit,
   schema, and a self-digest over all fields except the digest. Independently
   validate the vocabulary, all values, and seal in producer/checker. The
   `resource_terminal` mutation must change an extant owner and fail at its
   preregistered resource gate.
5. Repair `occurrence_basis_row` mutation and/or validation ordering so its
   first natural semantic failure is exactly its fixed owner gate in both
   implementations. Then statically audit all 24 mutations for natural first
   failure order; do not add dynamic expected reasons or reference equality.
6. Preserve task261's exact ABI reconstruction, direct|inverse restriction,
   target canonicalization, full MEMBER/NONMEMBER semantics, caps, typed
   UNKNOWN behavior, production path, and false downstream conclusions.
   Refresh driver/fixture/reply identities and report UNEXECUTED. Parent Sol
   will run GHA after whole-file audit.

A3 remains 0/3 until an accepted actual task226 package is consumed and a
production MEMBER/NONMEMBER certificate passes both implementations.

