# Luna task 188: actual R07 PSL root-propagation inventory

Role: Luna (mechanical inventory only).  Parent Sol retains all mathematical
judgment, git, GHA dispatch, and witness claims.

Read completely:

- `sol/proof_r07_psl_strip_leaf_elimination_v52.md`
- `sol/proof_r07_return_midpoint_psl_cycle_onto_v77.md`
- `sol/proof_r07_psl_strip_rooted_peeling_v166.md`
- the latest relevant PSL roster/task/reply files you locate with `rg`.

Tasks:

1. Locate every existing script, fixture, artifact receipt, and report that
   materializes an **actual typed R07** `PSL(2,8)` strip occurrence roster.
   Separate actual rosters from synthetic/selftest fixtures and abstract
   schemas.
2. For each actual roster, report whether it retains the data required by
   v166 Section 5: ordered occurrences, repeated/parallel edges, signs,
   automorphisms/conjugators, v52 peel record, and the global onto detector.
3. Without running heavy local Python/GAP/Node, compute any immediately
   readable structural counts: variables, constraints, v52 core size, and a
   greedy propagating-root upper bound.  If input is missing, say exactly
   which producer must emit it; do not invent a roster.
4. Propose the smallest mechanical producer/checker delta needed to emit a
   v166-authenticated root-propagation receipt.  Do not implement it in this
   task.

Write only:

- `sol/luna_reply_188_psl_root_propagation_inventory.md`

Do not edit code, do not run heavy local computation, do not use git/GHA, and
do not declare nonemptiness, a lift, fake, or Ihara witness.
