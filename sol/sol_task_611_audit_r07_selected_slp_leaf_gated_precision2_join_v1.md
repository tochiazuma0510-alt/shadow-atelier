# Sol(max) Task611: audit v470 leaf-gated precision-two join

Role: independent mathematical auditor. Read in full:

1. `sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md`
2. `sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md`
3. `sol/proof_r07_selected_ancestry_slp_lift_v465.md`
4. `sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md`
5. `sol/proof_r07_canonical_selected_dependency_slp_v468.md`
6. `sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md`
7. `sol/sol_reply_605_audit_r07_selected_slp_adjoint_fox_replay_v1.md`
8. `sol/sol_reply_609_audit_r07_canonical_selected_slp_physical_replay_v1.md`
9. `sol/proof_r07_selected_slp_leaf_gated_precision2_join_v470.md`

Audit whether v470 soundly replaces per-intermediate-node endpoint/Fox
evaluation by reached base-relator endpoint checks plus the unique
conjugate-leaf formula. Check the exact left Fox signs, coefficient-two
inverse convention, actor/conjugator cancellation, occurrencewise typing,
prior-root composition, lower-before-top residual gate, and the claimed
44*11 base endpoint ceiling. In particular decide whether every constructor
used by the current selected SLP preserves endpoint one and whether any
transition/old leaf is more general than a conjugate of one of the 44 compact
relators.

Return `PASS`, `PASS_AFTER_REPAIR` or `FAIL` and list only load-bearing
defects. Preserve the distinction between the canonical source graph and its
current-quotient coalesced evaluation. Do not implement, run GHA, modify
proofs/v220, or perform git operations. Write only:

`sol/sol_reply_611_audit_r07_selected_slp_leaf_gated_precision2_join_v1.md`

No actual residual, grade-two result, A0, COMMON, cofinality, fake, Ihara or
Lean verification follows.
