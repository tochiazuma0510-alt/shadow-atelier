# Luna task 266 - task232 tuple mutation owner repair v1

Role: bounded mechanical repair only. Read task263, the task232 five-file set,
and GHA run 33146459352 failure recorded here. Do not run Python, Node, GAP,
git, GHA, or network. Edit only the same five task232 files plus its existing
Luna reply.

## Exact observed failure

GHA run 33146459352 reached producer SELFTEST and failed before semantic
validation at:

    semantic_mutation_replay, repeated_e3_insertion
    mutant["contexts"].pop()
    AttributeError: 'tuple' object has no attribute 'pop'

The baseline owner is a tuple. Repair only this mutation construction so it
creates a changed object of the correct intended container type and reaches
the preregistered semantic gate naturally. Audit the immediately adjacent
mutation constructions for the same tuple/list assumption. Do not weaken or
remove the mutation, change expected reasons dynamically, or change any
mathematical identity, roof/projection semantics, terminal, cap, or forbidden
conclusion. Refresh identities in the reply and report UNEXECUTED. Parent Sol
will rerun the full serial GHA SELFTEST.

A4 remains 0/3 because this is only a SELFTEST repair; actual task198 input K
has not been run.
