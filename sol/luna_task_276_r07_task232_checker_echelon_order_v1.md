# Luna task 276 — task232 checker echelon order repair v1

Role: bounded one-owner independent-checker repair.  Read the current task232
producer, independent checker, fixture, driver, and reply in full.  Do not run
Python, Node, GAP, git, GHA, or network.  Edit only the checker, driver pin,
and existing task232 reply.  Parent Sol owns execution and repository work.

After task273 sealed the producer SELFTEST envelope, GHA run `33148430892`,
immutable head `97de2a2943f178a29ab6c774d521ce7f0bf7bc12`, emitted the producer's exact
57/57 PASS and then stopped at:

```text
R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_CHECKER_NONPOSITIVE reason=initial span
```

The owner is the checker-only `IndependentEchelon`.  It chooses the maximum
remaining coordinate as pivot and appends pivots in descending elimination
order, but `reduce()` traverses `reversed(self.pivots)`.  Subtracting a later,
smaller-pivot row first and then an earlier, larger-pivot row can reintroduce
the smaller coordinate, so even an original generator need not reduce to
zero.  This is precisely the failed `initial span` canary.

Repair the elimination traversal consistently with the checker's independent
maximum-pivot convention.  Audit every use of this echelon's pivot order,
including `reduce`, `reduce_with_coeff`, `dual`, `insert`, and the toy
round-trip, so that:

1. every inserted source is in the rebuilt span;
2. every action translate is in the completed span;
3. coefficient replay remains exact; and
4. the dual still annihilates the completed span and pairs nontrivially with
   a nonmember.

Do not copy/import the producer, switch the checker to the producer's
minimum-pivot implementation, weaken the initial/translate span gates, alter
the 57 mutations, change any affine/roof/projection/K mathematics, or change
production acceptance.  Refresh the checker pin in the driver and the
existing reply.  Report exact identities as `UNEXECUTED`.

A4 remains `0/3`: SELFTEST acceptance is not an authenticated actual task198
presentation, an exhausted actual closure, or an accepted actual word-bearing
kernel.

