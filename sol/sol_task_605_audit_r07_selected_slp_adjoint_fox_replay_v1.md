# Sol(max) Task605: audit selected-SLP adjoint Fox replay v467

Act as an independent hostile mathematical auditor.  Read in full:

1. `sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md`
2. `sol/proof_r07_selected_ancestry_slp_lift_v465.md`
3. `sol/proof_r07_reverse_selected_physical_slp_extraction_v466.md`
4. `sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md`
5. `sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md`
6. `sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md`

Write only `sol/sol_reply_605_audit_r07_selected_slp_adjoint_fox_replay_v1.md`.
Do not edit proofs/code/workflows/v220, commit, push, dispatch, or run a large
calculation.

Check especially:

- the Fox-pair product/inverse convention and its compatibility with the
  section-left/right-action arithmetic already fixed in v443;
- whether every selected correction factor really has endpoint one at the
  *current* marked quotient, and whether v467 makes this an executable premise
  rather than smuggling it to finer quotients;
- the sign/scale equations in reverse propagation (3.1)--(3.3), including
  coefficient two and nested lower/block/old DAGs;
- whether additive Fox evaluation is enough for the complete eleven-occurrence
  physical row while the ordered source SLP remains unchanged;
- normalized exponent, PB3/boundary/auxiliary gates and the prohibition on
  using physical-lower zero as source-kernel membership;
- whether the memory/runtime claim honestly avoids one ambient row per SLP
  node without claiming a bound on literal-origin evaluation; and
- whether the fresh grade-two residual follows exactly under v451, with no
  premature first-rung/cofinal/fake/Ihara conclusion.

Give PASS, PASS_AFTER_REPAIR or FAIL.  State only exact load-bearing repairs;
reject optional exposition or redesign.  Include bytes/SHA-256 and preserve
`verified=false`.
