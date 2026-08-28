# Luna task 267 - task232 four vacuous mutation repairs v1

Role: bounded implementation repair only. Read task266, current task232 files,
and this observed GHA result. Do not run Python, Node, GAP, git, GHA, or
network. Edit only the same five task232 files plus its existing Luna reply.

## Exact observed result and parent static diagnosis

JSON-dispatched full SELFTEST GHA run 33146988624 reached the producer and
returned

    R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PRODUCER_NONPOSITIVE
    reason=semantic mutation rejection

so at least one registered mutation was not rejected. Parent inspection found
four vacuous owners in `semantic_mutation_replay.validate`:

1. `context_type` changes `contexts[0].type` but validation checks only two
   tags and length.
2. `context_id` changes `contexts[0].context_id` but validation does not check
   context IDs.
3. `delta1_bfs` changes the toy binding value from `unused` to truthy `bad`,
   while validation checks only truthiness.
4. `task192_word` has the same truthiness defect.

## Required repair

Independently require the complete exact ten-entry typed context roster
(index, type, context_id, tag) against the canonical `CONTEXT_LEDGER`, so the
first two mutations are owned semantically and the E3-C21/E4-C21 distinction
remains explicit. In the production-shaped toy binding, require the exact
baseline `delta1_bfs` and `task192_word` values rather than truthiness, so the
last two mutations are rejected. Audit the remaining registered mutations
for another vacuous truthy/equality gap, but do not alter the roster, weaken a
mutation, add dynamic expected reasons, or change any roof/projection/K,
terminal, cap, or forbidden-conclusion semantics. Refresh driver pins and
reply identities; report UNEXECUTED. Parent Sol will rerun the full serial
GHA SELFTEST.

A4 remains 0/3; SELFTEST success alone is not actual task198 K.
