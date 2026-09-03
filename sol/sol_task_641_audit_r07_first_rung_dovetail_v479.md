# Sol(max) Task641: audit first-rung witness/presentation dovetail v479

## 1. Scope

Read this mail and v479 completely.  Perform an independent mathematical
audit only.  Do not edit v479 or implementation, do not run production/GHA,
and do not use git.  Write only
`sol/sol_reply_641_audit_r07_first_rung_dovetail_v479.md`.

The exact candidate is
`sol/proof_r07_first_rung_witness_presentation_dovetail_v479.md`, 12,280
bytes, SHA-256
`df6850c9e7c86a83ade26c37064a7deb38ec3c8d7907b1eec6ff0d5268b22986`.

Authenticate its exact parent pins.  Read the cited v444, v449, Task555,
v465, v469--v471, v474, v478 and Task639 statements as needed to decide the
claims rather than accepting the candidate's paraphrase.

## 2. Required decisions

Decide each of the following precisely.

1. Whether the complete transition presentation `P_d` is genuinely
   target-independent and can be constructed from `P_(d-1)` without the
   selected word `C_d` or residual, while the fresh residual depends on the
   exact selected word but not on completion of `P_d`.
2. Whether a target-directed v474 MEMBER ancestry is sufficient to form the
   selected update/root and replay the next residual, but is correctly *not*
   called a complete transition presentation for the following grade.
3. Whether the v470 conjugate-Fox and v471 eleven-endpoint signature proofs
   are degree-independent through the fixed first-rung group algebra, under
   the stated exact endpoint and source-graph premises.
4. Whether extending an accepted path trie only at the derived evaluation
   layer preserves the noncommutative source graph and does not smuggle in a
   refinement/cofinality claim.
5. Recompute every entry of the v479 grade-2--6 table from
   `(h0,...,h6)=(1,3,6,7,6,3,1)`, including source, lower/auxiliary, top and
   packed widths.  Check that the auxiliary counts remain correctly typed.
6. Check Theorem 5.1's dependency assertion: the witness residual branch
   and target-independent presentation branch may execute concurrently, but
   both accepted products are required at the next membership join.
7. Check the present Task639/Task640/v474 instantiation and ensure it does
   not claim that Task640 has completed, that grade two is MEMBER, or that
   any later grade, first rung, A0, cofinal lift, fake or Ihara is decided.

Look actively for a counterexample caused by source-versus-physical typing,
old/lower mixed ancestry, occurrence-first ordering, a hidden dependency of
`P_d` on the chosen correction, or reuse of an endpoint receipt at a changed
quotient.  This is a bounded theorem audit, not a request to design a larger
framework.

## 3. Verdict

Return exactly one of `PASS`, `PASS_AFTER_REPAIR` with a finite exact repair,
or `FAIL`.  State the v220 consequence without increasing a numerator:
first rung remains 1/6 cross-checked and A0 remains 0/1 actual.  Preserve
`verified=false`.

