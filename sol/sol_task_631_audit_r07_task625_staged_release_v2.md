# Sol(max) Task631: independent static audit of Task625 staged release v2

Audit the exact release snapshot below before any commit or GHA run:

- `search/d972_r07_a0_grade1_selected_slp_v2.py`, 71,954 bytes,
  SHA-256 `c3b7d53accb8b0814049cae4e1cadebc905941031b156dd12763ac2072219cf0`;
- `search/check_d972_r07_a0_grade1_selected_slp_v2.py`, 101,254 bytes,
  SHA-256 `33dd8cf7fdc94c971e58a09211e5acbf749980dfc49109f3bf51db4495d46002`;
- `.github/workflows/d972-r07-a0-grade1-selected-slp-v2.yml`, 6,077 bytes,
  SHA-256 `35682ef40110d15199ddc5e17300b25e17d44bd414d59d2346bca86fbf95f653`;
- `sol/luna_reply_625_r07_task601_staged_adjoint_release_v2.md`, 7,968
  bytes, SHA-256
  `b3872695fb287841c5d4078471fdadc076c6a3c6eac45e0656c626e3f79b7b17`;
- `sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md`, 8,253
  bytes, SHA-256
  `757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e`;
- Task628 and Task629 replies; and
- the Task622-accepted v1 producer/checker/workflow and Task622 reply named
  in the Task625 kickoff.

This is an adversarial static/code audit.  Do not run production, GHA, or git,
and do not edit implementation files.  Bounded serial selftests are permitted
only if useful.

Check all of the following:

1. all Task622 routing/authentication/8,059-offer/3,317-coefficient/physical
   replay/compact-leaf/false-claim gates survive unchanged;
2. the actual `G,L,B,D,O` graph is scheduled exactly in the v475 topological
   order, every reduction and actor parent is strict, and no destination can
   receive a late contribution after release;
3. coefficients, signs, left-to-right actor words, free reduction, exact-word
   equality and literal-leaf serialization reproduce v1 semantics;
4. producer/checker are genuinely independent and the deterministic
   statistics comparison does not accidentally compare wall/RSS values;
5. `expanded_states` and `state_edge_traversals` implement the repaired v475
   definitions, excluding root insertion from edge traversal;
6. resource exhaustion cannot publish a partial payload and cannot become a
   negative result;
7. the workflow's immutable hashes, parents, marker, artifact gates, serial
   execution and 60-minute/8-GiB boundary are coherent; and
8. specifically audit performance: reject any needless dense boundary
   closure, full-path replay, large retained duplicate, unnecessary array
   copy, repeated released-state expansion, or selftest/diagnostic work on the
   production path.  Distinguish harmless linear prevalidation from a
   load-bearing asymptotic regression.

Try concrete adversarial mutations/counterexamples where bounded.  A finite
repair is acceptable, but identify the smallest exact change.  Do not request
unrelated hardening or broad refactoring.

Write the full verdict only to
`sol/sol_reply_631_audit_r07_task625_staged_release_v2.md`, with exact input
hashes, PASS / PASS_AFTER_REPAIR / FAIL, fixture results, performance verdict,
launch authorization or prohibition, all claim boundaries, and
`verified=false`.
