# Sol(max) Task647: bind Task640 fresh rho2 to the v474 grade-two decision

Role: Sol mathematical auditor / launch-contract designer.  Work in parallel
with Task646.  Read this complete mail and write only
`sol/sol_reply_647_r07_task640_to_v474_grade2_launch_contract.md`.  Do not
implement, edit proofs/v220, run production/GHA, or use git.

## 1. Purpose and fixed status

The selected explicit grade-one SLP is accepted (Task625/639).  Task640 is the
finite fresh-rho2 consumer now under final release audit; it may produce an
accepted 48,384-trit / 12,096-byte residual but has not run yet.  V474's
targeted exact MEMBER/NONMEMBER theorem is paper-closed by Task626, generalized
by Task642, and dovetailed with the complete-presentation branch by v479/
Task641.  Current counters remain A0 `0/1 actual`, first rung `1/6`.

Prepare the exact minimal contract that lets Luna implement and root launch
the grade-two v474 owner as soon as a Task640 artifact is accepted.  This is
not permission to count rho2 or a grade-two result early.

Required core inputs:

- `sol/proof_r07_rho2_cegar_dual_decision_repair_v474.md`;
- `sol/sol_reply_626_reaudit_r07_rho2_targeted_dual_v474.md`;
- `sol/proof_r07_first_rung_witness_presentation_dovetail_v479.md`;
- `sol/sol_reply_641_audit_r07_first_rung_dovetail_v479.md`;
- `sol/sol_reply_642_audit_r07_targeted_decision_all_first_rung_grades.md`;
- Task640/643/645 quartet and Task625/639 exact parent facts;
- v451 and the existing Task565/568 implementation/artifact shelf named by
  v474, inspected read-only.

## 2. Questions, first to last

1. State the exact type and receipt gates for the future Task640 rho2 and the
   complete grade-one presentation-side input.  Distinguish accepted data,
   recomputable data and untrusted specification code.
2. Identify by exact repository paths the smallest existing producer/checker
   components that can safely be reused or translated.  Reject Task565 holes
   explicitly; do not demand a new generic framework.
3. Give a finite producer interface for: sequential `Conn`, one requested
   defect slice, four forward/adjoint actor maps, `B_a/B_a^dual`, packed
   echelon/pairing, raw ancestry and the canonical separator.  State all
   ordering/normalization invariants that are load-bearing.
4. Give the genuinely independent checker contract for MEMBER and NONMEMBER.
   MEMBER must expand literal ancestry and compare all 48,384 coordinates;
   NONMEMBER must authenticate connection EOF plus four exhausted dual-orbit
   transcripts and complete defect pairings.  Caps yield only
   `UNKNOWN_RESOURCE`.
5. Find which expensive data can be streamed, recomputed on demand, shared
   structurally or omitted.  Give honest packed-byte/RSS ceilings and propose
   only reductions proved span-preserving.  Flag any old nested metadata,
   repeated decoding, shared-floor or Python-object explosion to avoid.
6. Decide whether a single bounded GHA workflow can legally dovetail a primal
   targeted prefix with dual CEGAR passes, and give a checkpoint schema that
   preserves exact mathematical progress without retaining the whole closure.
   Checkpoints are operational state, never negative certificates.
7. End with a concrete Luna implementation order and a shortest-path release
   checklist.  Separate what can be completed before Task640 produces rho2
   from the one result-dependent join step afterward.
8. Map the result back to v220: what exact terminal would move first rung
   `1/6 -> 2/6`, what remains for A0, and why neither fresh rho2 nor a partial
   grade-two span is itself a witness/fake/Ihara result.

## 3. Boundary

Do not reopen the already accepted v474 theorem unless a concrete
counterexample is found.  Do not require full M2 materialization, SAT, Lean,
all later grades, or production-sized local calculation.  Return one of:

- `READY_FOR_LUNA_CONTRACT` with an exact finite implementation contract; or
- `BLOCKED`, naming the exact missing mathematical datum and why no existing
  authenticated source can supply it.

Report reply bytes/lines/SHA-256 and `verified=false`.
