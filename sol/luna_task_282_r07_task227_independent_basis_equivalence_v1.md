# Luna task 282 - task227 independent basis equivalence v1

Commissioner: Sol / 2026-08-28

Reply by appending a dated task282 section to
`sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md`.

Role: bounded mechanical checker repair only. Do not run Python, Node, GAP,
git, GHA, or network locally. Parent Sol owns mathematics and execution.

Read this commission, task234 Sections 6--8, task278 Section 4, and the
current task227 producer/checker/driver/reply in full. Edit only:

```text
crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py
search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g
sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md
```

Do not change producer, fixture, proof, ledger, workflow, or predecessors.

## 1. Deterministic overconstraint

The producer closure inserts generator actions in order

```text
x, x^-1, y, y^-1
```

while the independent checker deliberately rebuilds the orbit with a
different order

```text
y^-1, y, x^-1, x.
```

Both use normalized forward echelon insertion, not a unique reduced-row-
echelon canonicalization. Therefore two complete bases may differ as ordered
row lists while spanning exactly the same invariant subspace. Task234 and
task278 require two-way span equality, not literal equality of independently
pivoted bases.

The checker already executes, in both directions, exact sparse span checks
between its rebuilt orbit, the producer occurrence basis, the canonical 486
ideal rows, and all 729 translates. It also replays every producer occurrence
row from its printed coefficient ancestry. The subsequent exact

```text
require(rebuilt == occ, "occurrence basis row")
```

is therefore a representation-dependent overconstraint and can reject a
mathematically valid complete receipt.

## 2. Exact repair

Remove only that literal independent-basis-list equality. Preserve all
two-way sparse span reductions, ranks, all 486/729 exact rosters, producer
row ancestry replay, block-image comparisons, queue invariance, and the
earlier typed `occurrence basis row` guard. Do not replace the removed test
with a hash or producer Boolean.

Audit for any further direct equality between two independently generated
noncanonical echelon *basis lists*. Do not remove equalities for canonical
serialized rows, fixed rosters, encoded pivots from the same ordered input,
ancestries, or algebraic replays. Report the audit result.

Retain task280 log visibility and task281 JSON-native pivot normalization.
Refresh only the checker pin in the driver. No terminal, cap, mutation, or
conclusion semantics may change.

## 3. Delivery

Record exact byte/SHA identities for producer, checker, driver, fixture, and
reply. Leave `UNEXECUTED`; parent Sol will run the full serial GHA SELFTEST.

End with:

```text
TASK227 INDEPENDENT BASIS EQUIVALENCE:          REPAIRED STATICALLY
FULL PRODUCER+INDEPENDENT CHECKER SELFTEST:     NOT EXECUTED BY LUNA
ACTUAL TASK226 PACKAGE / A3 GATE:               NOT OBTAINED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:         NOT DECLARED
```

`TASK282_TASK227_INDEPENDENT_BASIS_EQUIVALENCE_COMMISSIONED`
