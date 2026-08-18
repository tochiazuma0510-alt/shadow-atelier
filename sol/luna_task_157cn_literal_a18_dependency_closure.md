# Luna task 157cn — literal A.18 dependency closure and v2 release

## Role

You are Luna.  Repair the literal-A.18 campaign after two fail-closed GHA
preflights.  Do not run local GAP, Git, GHA, or heavy local Python.  Modify
only the versioned files and reply below.

## Observed failures

Run `32081149872` failed before selftest because three imported Magnus cores
were absent from the commit.  The parent added those exact cores at commit
`0e0b0b0855f3c42c00c614b863ff0e14368734da`.  Run `32081758961` then passed
the source-binding step but failed every job in producer selftest because
`search/d972_b4_magnus_ideal_merge_v2.py` imports the still-untracked file
`search/d972_b4_magnus_ideal_v1.py`.

That base producer has SHA-256

```text
b2e5184e31e177dcf5bfdc9fcd715e2146db877e0eccda2056cc5d7f999ae6bc
```

Merely adding it is not enough: the current wrapper checks three core hashes
but does not pin this transitive imported dependency.  That is a fail-open
supply-chain gap even though the independent checker reconstructs the final
mathematics.

## Required files

Create versioned releases; do not overwrite the failed v1 lane:

- `search/d972_b4_next_obstruction_v2.py`
- `search/check_d972_b4_next_obstruction_v2.py`
- `.github/workflows/d972-b4-next-obstruction-v2.yml`
- `sol/luna_reply_157cn_literal_a18_dependency_closure.md`

The existing base dependency `search/d972_b4_magnus_ideal_v1.py` is an
authorized dependency for the parent to stage unchanged; do not modify it.

## Required repair/audit

1. Base v2 on the repaired v1 producer/checker/workflow, preserving literal
   18+140 A.18 semantics, unconditional D-tilde, degrees 2--6, 16 d6 shards,
   exact partitions, rho exclusion, and all 157cf fail-closed repairs.
2. Add the base producer path/hash as a first-class transitive dependency.
   Check it before any import in the wrapper.  Bind it into every shard and
   merge receipt, complete shard ledger, independent checker, and workflow
   aggregate.  The workflow must hash-check it before selftests.
3. Audit the full recursive local import/file dependency closure of all five
   Python components.  List every required repository file and prove that it
   is either already tracked at commit `0e0b0b08...` or is the one authorized
   untracked base producer above.  Reject any unpinned executable import.
4. Add negative selftests mutating/removing the base-producer binding at top,
   degree, and shard-record levels.  All must reject even on an all-zero
   defect receipt.
5. Pin all GitHub actions by immutable SHA.  Parse YAML and every embedded
   Python block.  Run only bounded producer/checker selftests and a light d2
   temporary replay; do not run d3--d6 locally.
6. Ensure the parent can exact-stage the three new files, the reply, and the
   unchanged base producer with no other dirty-tree file.

## Verdict

End with exactly one token:

- `LITERAL_A18_DEPENDENCY_CLOSURE_READY`
- `LITERAL_A18_DEPENDENCY_CLOSURE_BLOCKED`
