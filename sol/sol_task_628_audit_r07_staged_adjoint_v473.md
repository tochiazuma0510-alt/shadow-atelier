# Sol(max) Task628: audit the staged-adjoint theorem v473

Read completely:

- `sol/proof_r07_selected_slp_staged_adjoint_v473.md`;
- the exact leaf-expansion and ancestry-construction paths in
  `search/d972_r07_a0_grade1_selected_slp_v1.py` and its checker;
- Task618, Task620 and Task622 replies as needed for the accepted source DAG;
- the run `33723160379` facts recorded in v220 Delta419 (do not access GHA).

Write only `sol/sol_reply_628_audit_r07_staged_adjoint_v473.md`. No code,
production, GHA, or git.

Check whether v473's dependency list is complete for every grade, lower,
block, defect and old constructor; whether all claimed within-stage edges are
strictly earlier; whether the displayed stage order guarantees every exact
`(node,path)` coefficient is complete before expansion; and whether exact
freely reduced multiplication/coefficients reproduce the pathwise sum with
no quotient coalescence. Try to construct a counterexample involving a
cross-stage return, actor-parent order, or cancellation arriving after a node
was released. Check that the resource statement is only result-dependent.

Conclude `PASS`, `PASS_AFTER_REPAIR`, or `FAIL`; list only finite necessary
repairs. This is a paper/static audit, not an actual Task625 acceptance or a
numerator. Keep all grade/A0/fake/Ihara claims false and `verified=false`.

