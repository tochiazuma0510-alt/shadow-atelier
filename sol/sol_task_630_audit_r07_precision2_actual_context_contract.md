# Sol(max) Task630: actual precision-2 context contract audit

This is a mathematical/static interface audit for the post-Task625 consumer.
Do not implement, run production/GHA, or perform git operations.

Read completely or inspect all load-bearing definitions in:

- `sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md`;
- `search/d972_r07_history_free_positive_fast_resume_v12f.py`, especially
  the actual `pcontexts`, `raw_specs`, `occurrence_data`, and
  `occurrence_column` construction;
- `sol/sol_reply_627_audit_r07_task623_endpoint_consumer_v2.md`;
- `sol/proof_r07_rho2_cegar_dual_decision_repair_v474.md`;
- `sol/sol_reply_626_reaudit_r07_rho2_targeted_dual_v474.md`.

Determine the exact non-placeholder contract needed to turn a successful
Task625 exact leaf payload into the fresh precision-2 residual/operator input.
In particular:

1. enumerate and authenticate the actual eleven occurrence contexts (do not
   alias them to the six Task565 tags and do not use `% 6`);
2. state the exact word-action / trie recurrence and the roles of
   `C_<1`, `C_T`, and `C_1`;
3. distinguish the Task595/Task625 grade-1 membership receipt from the new
   precision-2 target and identify every required parent hash/count;
4. identify which endpoint/signature equality is permitted only after exact
   source-word preservation;
5. give a finite acceptance checklist for a future Luna implementation and
   independent checker, including full 32,260-state and 48,384-coordinate
   replay where required; and
6. flag any point that cannot be fixed until the final Task625 manifest/schema
   is known.

The output is a design audit, not an actual precision-2 result.  Preserve all
UNKNOWN/resource and false-claim boundaries.

Write the full result only to
`sol/sol_reply_630_audit_r07_precision2_actual_context_contract.md`, with
input hashes, PASS/FAIL for whether a complete implementation contract can be
stated now, explicit unresolved inputs, and `verified=false`.
