# Luna task 277 — task232 checker pivot-ancestry owner repair v1

Role: bounded one-owner independent-checker repair.  Read the current task232
files and GHA run `33148887439`.  Do not run Python, Node, GAP, git, GHA, or
network.  Edit only the checker, driver pin, and existing task232 reply.

At immutable head
`551d47d88a88492e47c4274cc68e7e74bb3777a8`, the repaired checker passed the
initial-span owner and next stopped at:

```text
R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_CHECKER_NONPOSITIVE
reason=producer pivot-scale ancestry
```

The producer SELFTEST envelope owns this receipt at
`mutation_controls.pivot_scale_ancestry`; the checker incorrectly reads a
nonexistent top-level `pivot_scale_ancestry`.  Point the checker at the exact
existing owner and retain the gates `replayed is True` and `scale == 2`.
Also require the containing mutation-control object already authenticated by
the adjacent attempted/rejected/name checks.  Do not duplicate or move the
producer field, weaken the ancestry canary, change the 57 mutations, alter the
echelon repair, or change any production mathematics/acceptance.

Refresh checker pin and reply identities.  Report `UNEXECUTED`; A4 remains
`0/3` pending actual task198 input and actual closure/K acceptance.

