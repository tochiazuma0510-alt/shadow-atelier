# Sol(max) Task 575 — adversarial audit of v454 Cayley--Fox grade caps

Read completely:

- `sol/proof_r07_associated_grade_cayley_fox_rank_cap_v454.md`
- `sol/proof_r07_filtered_transition_defect_closure_v444.md`
- `sol/proof_r07_first_rung_character_blocks_coupled_monomials_v446.md`
- `sol/proof_r07_first_rung_character_projector_word_repair_v447.md`
- the relevant coordinate formulas in
  `sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md`
- Task540 F3--F4 and the actual `evaluate_occurrence_pair` / `qnorm_affine`
  conventions in `search/d972_r07_a0_first_rung_grade1_v3.py`.

Write only
`sol/sol_reply_575_audit_r07_associated_grade_cayley_fox_rank_cap_v1.md`.

This is a bounded mathematical audit, not a request for implementation or a
new general theory.  Decide whether v454 really proves an upper bound for the
actual coupled-monomial transition-defect blocks.

Audit load-bearing points adversarially:

1. A zero-lower v444 defect has a pure degree-`d` Fox leading pair satisfying
   the associated right boundary, even with negative substitutions, crossed
   occurrence terms and old-basis lift defects.
2. The right boundary in source character `lambda` is the Cayley boundary
   with coefficient module `M_d`; its cokernel character multiplicity is
   exactly `m_(d,lambda)`, not `h_d`, zero, or an inverse-character variant.
3. Enumerate all `alpha_i in {0,1,2}` and independently check the six
   multiplicity rows `(0;1,1,1)`, `(3;1,1,1)`, `(1;2,2,2)`, repeated degree
   four/two, degree five/one, and `(1;0,0,0)`.
4. Check that the Fourier label used by the live arrays is the left source
   character and that order-two inversion cannot change the table.
5. Check the `fxy` identity occurrence and the exact PB3 normal formula make
   the stored occurrence map injective; reject any silent quotient or omitted
   auxiliary condition.
6. Check caps `1512/1513`, `3027/3025`, `3529/3530`, their reflected values,
   and `505/504`; compare grade-one ranks `1509/1512^3` only as a consistency
   check, not as proof.
7. Check that reaching the cap is a sound completion alternative, and that
   without saturation the offer bounds `32280+4*cap = 44388/44380` still
   assume the exact queue discipline actually used.
8. Check packed live-basis byte products and that no statement improperly
   bounds transcript size or physical lower-first rank.
9. Check Section 5 does not confuse a chord/kernel basis with replayable
   compact-seed ancestry and does not overclaim a direct replacement.

If a local flaw is repairable, state exact replacement text/formula.  If the
core cap is false, give the smallest counterexample or coordinate mismatch.
Do not request style changes, Lean, a full-Q2 computation, or a production
run.

End with exactly one of:

```text
ASSOCIATED_GRADE_CAYLEY_FOX_CAP_V454_AUDIT_PASS
ASSOCIATED_GRADE_CAYLEY_FOX_CAP_V454_AUDIT_PASS_AFTER_REPAIR
ASSOCIATED_GRADE_CAYLEY_FOX_CAP_V454_AUDIT_FAIL
```

No A0/COMMON/cofinal-lift/fake/Ihara promotion.
