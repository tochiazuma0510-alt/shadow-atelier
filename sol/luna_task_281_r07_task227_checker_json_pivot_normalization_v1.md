# Luna task 281 - task227 checker JSON pivot normalization v1

Commissioner: Sol / 2026-08-28

Reply by appending a dated task281 section to
`sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md`.

Role: bounded mechanical checker repair only. Do not run Python, Node, GAP,
git, GHA, or network locally. Parent Sol owns mathematics and execution.

Read this commission, the current task227 producer/checker/driver and current
reply in full. Edit only:

```text
crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py
search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g
sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md
```

Do not change producer, fixture, proof, ledger, workflow, or predecessors.

## 1. Deterministic static mismatch

The producer's `block_echelon` pivot is encoded before canonical JSON as
`list(p)` for `p=(block,key_tuple)`. Canonical JSON necessarily converts the
inner tuple to a list. The independent checker currently reconstructs its
comparison object with the same Python `list(p)`, leaving the inner key a
tuple in memory, and compares it directly against the decoded producer JSON.
Thus a mathematically identical pivot has shapes

```text
checker expected: [block, key_tuple]
decoded receipt:  [block, key_list]
```

and the exact `block rows` comparison must reject a valid receipt. This is a
serialization-boundary type defect, not a rank or mathematical discrepancy.

## 2. Repair and bounded JSON-shape audit

Normalize only the checker's reconstructed echelon pivot to the exact
JSON-native shape `[block, list(key)]` before equality. Preserve the exact
row and ancestry contents and the complete equality; do not replace it by a
digest, rank, span, or Boolean flag.

Audit every other checker-created composite which is compared directly to a
decoded producer field for the same tuple-versus-list issue. Repair further
instances only if the checker itself leaves a tuple where canonical JSON
necessarily supplies a list. Report every changed site; do not broadly
round-trip the entire producer receipt or import producer helpers.

Retain task280's fail-closed log visibility. Refresh only the checker pin in
the driver. No terminal, predicate, cap, mutation, or conclusion semantics
may change.

## 3. Delivery

Record exact final byte counts and SHA-256 identities for producer, checker,
driver, fixture, and reply. Leave the result `UNEXECUTED`; parent Sol will
run the full serial GHA SELFTEST.

End with:

```text
TASK227 CHECKER JSON PIVOT SHAPE:               REPAIRED STATICALLY
FULL PRODUCER+INDEPENDENT CHECKER SELFTEST:     NOT EXECUTED BY LUNA
ACTUAL TASK226 PACKAGE / A3 GATE:               NOT OBTAINED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:         NOT DECLARED
```

`TASK281_TASK227_CHECKER_JSON_PIVOT_NORMALIZATION_COMMISSIONED`
