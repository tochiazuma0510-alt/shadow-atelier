# Luna task 263 — task232 roof-mutation owner repair v1

Role: bounded implementation repair only. Read task232, task256, task260,
GHA run 33146001722's exact traceback recorded below, and all current five
task232 files. Do not run Python, Node, GAP, git, GHA, or network. Edit only
the same five task232 files plus the existing task232 Luna reply.

## Exact executed rejection

Parent GHA SELFTEST run `33146001722`, head
`0818e23bcfdc27b3957b378df87d99f56525186d`, stopped in producer
`semantic_mutation_replay` because its validator reads
`successors[*]["roof_identity"]`. `build_typed_successors()` never serializes
that field; the truthful toy owner is the separate ten-entry
`roof_reductions` ledger. The `roof_reduction` producer mutation likewise
targets the nonexistent successor field. The independent checker already
validates and mutates `roof_reductions`.

## Required repair

1. Producer validates exactly ten typed successors/source words and separately
   requires `roof_reductions == [True] * 10`, matching the serialized owner.
2. Producer `roof_reduction` mutation changes exactly one entry of that extant
   `roof_reductions` ledger. Checker retains its independent mutation of the
   same semantic owner.
3. Inspect every remaining producer/checker mutation path for another direct
   access to a field absent from the baseline toy certificate. No mutation may
   be counted through `KeyError`; the suites catch only their semantic
   rejection class and fail open on acceptance.
4. Preserve H2 projection, selected anchor, K construction, 57-name roster,
   production semantics, and false downstream flags. Refresh driver pins and
   reply identities. Report UNEXECUTED; parent Sol reruns GHA.

A4 remains 0/3. This execution was not an actual presentation/K milestone.
