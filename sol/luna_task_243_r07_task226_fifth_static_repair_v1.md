# Luna task 243 - task226 fifth static repair v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md`.

Role: bounded mechanical repair only.  Do not run Python, Node, GAP, git,
GHA, or network locally.  Edit only the same five task226 files authorized by
task240.  Parent Sol owns mathematical adjudication and every execution.

## 1. Rejection boundary

The task240 return is rejected before execution.  Read task240 in full and
preserve all correctly repaired Fox signs, sparse accumulation, actual
predecessor reconstruction, seal dialects, resource measurement, and driver
pins.  Repair every defect below.  Status remains `UNEXECUTED`.

## 2. Make both source files parsable

The checker still has inconsistent indentation in `check_attestation`:
its first statement and final loop/return are indented two spaces while the
intervening statements are indented one.  Normalize the complete function
body.  Statically inspect every `def`, `try`, `except`, and nested suite in
both files.  Do not claim syntax readiness merely from visual similarity.

## 3. Never catch an accepted-mutation sentinel

Both mutation harnesses currently do the equivalent of

```text
try:
    validate(mutated)
    raise Stop("mutation accepted")
except Stop:
    record rejected=True
```

so every accepted mutation is falsely counted as rejected.  Define a
distinct `MutationAccepted` exception outside the caught validator exception
class, or use an explicit success flag after the caught block.  If validation
accepts a mutation, abort the SELFTEST.  The serialized `rejected=true` record
may be emitted only when the intended validator/reconstruction gate actually
raised.

## 4. Repair the zero-cancellation oracle

The producer currently asserts

```text
sparse_add({one:1},{one:2},-1) == {}
```

which equals coefficient two, not zero, over F3.  Test translated-minus-
original with two coefficient-one singleton rows and scalar `-1`.  Keep
separate literal tests for `r^-1-1` and `1-R`, where coefficient one plus
coefficient two cancels without the extra scalar.  The checker must perform
the same three tests through its independent sparse routine.

## 5. Give every retained mutation a live owning gate

Task240 explicitly permitted shrinking aliases.  Use that permission.  Do
not retain names that all mutate one fallback field.  For each retained name:

1. mutate exactly its owned semantic datum;
2. reseal enclosing objects except for the seal mutation;
3. prove a nonidentical before/after digest for that datum;
4. require the validator error to equal or contain its preregistered owning
   gate; and
5. let acceptance escape as a fatal `MutationAccepted`.

The producer validator must compare a freshly rebuilt complete package/ABI
from `words.g0`, `words.a`, and the literal occurrence ledger, not only check
the ABI seal and a few shapes.  Avoid recursion: the rebuild routine may call
the pure specialization routine, but the specialization routine must not call
the validator.  The independent checker continues to rebuild from its own
arithmetic and, in production, from the actual task192/task198 values.

At minimum keep genuinely different live mutations for: `g0`, `a`, `f`, one
ledger block/sign/orientation/prefix entry, every serialized Fox identity
family (`d_occ`, `d_raw`, `B_a`, `e`, `D1_d`, `D1_e`), one Q3 and every
nonzero Q4 bracket family or a table-wide mutation checked against all
entries, actor product/inverse/conjugation, each zero-safe xi/endpoint/u0
construction, both predecessor bindings, output freshness, resource
terminal, ABI seal, and forbidden conclusions.  A smaller honest roster is
preferred to a nominal 96-control roster.

## 6. Freeze the task226 ABI used by task227

Do not silently change the schema or row meaning.  The stable object is:

```text
schema = d972-r07-v216-specialization-abi/v1
occurrences[i].u0 = sparse-list for translated_w_o - w_o
abi.u0[i] = {
  ordinal,
  terms=w_o,
  translated_terms=translated_w_o,
  source_coefficient_terms=[
    {source=translated, coefficient=1, terms=translated_w_o},
    {source=original, coefficient=-1, terms=w_o,
     ancestry=occurrences[i].ancestry}
  ]
}
```

Empty sparse lists are valid.  Validate this literal provenance, all four
top-level fields, both signed source records, and equality to the occurrence
rows.  Record this exact ABI spelling in the reply so task227 can consume it
without guessing.

## 7. Preserve the corrected Fox dictionary

For every H1/H2/P block, producer and checker must still reconstruct

```text
d_occ = d_raw = -Fox(R_B(g0))
B_a = Fox(R_B(f)) - Fox(R_B(g0))
e = d_occ - B_a = -Fox(R_B(f))
D1(d_occ) = 1 - R_B(g0)
D1(e) = 1 - R_B(f).
```

The full-cokernel row `d_occ` is not required to be a cycle.

## 8. Final static cone audit

Refresh exact producer/checker/fixture pins in the driver after all edits.
Check that the pin bytes and SHA strings in the driver equal the returned
identities.  Inspect the production path to ensure the task192
`self_digest` and task198 `self_digest_sha256` dialects remain separate, and
that checker reconstruction uses actual predecessor values.  Keep receipt
and sidecar binding, live RSS measurement, live malformed-input/resource
probes, fresh outputs, exact-one terminals, and no positive sentinel before
checker completion.

## 9. Delivery

Process Sections 1--8 in order.  State that no execution was performed and
that A2 remains paper-only pending Parent Sol's static acceptance and GHA
SELFTEST.  End with:

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
A3 AND LATER:                      UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```
