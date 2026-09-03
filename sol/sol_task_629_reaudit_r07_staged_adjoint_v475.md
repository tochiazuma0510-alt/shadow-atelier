# Sol(max) Task629: finite re-audit of staged-adjoint repair v475

Read completely:

- `sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md`
- `sol/sol_reply_628_audit_r07_staged_adjoint_v473.md`

This is a narrow paper re-audit.  Check that v475 applies exactly the two
Task628 repairs: no embedded CR bytes, and
`E_{\mathrm{reached}}` means state-edge traversals counted with multiplicity
over nonzero accumulated states.  Check that the surrounding theorem and
claim boundary were not strengthened incorrectly.  Do not run production,
GHA, or git operations and do not edit implementation files.

Write the complete verdict to
`sol/sol_reply_629_reaudit_r07_staged_adjoint_v475.md`.  State PASS or FAIL,
input hashes, remaining defects if any, and preserve `verified=false`.
