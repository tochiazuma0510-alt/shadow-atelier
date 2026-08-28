# Luna task 244 - task232 second actual-kernel repair v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_232_r07_word_independent_successor_kernel_v1.md`.

Role: bounded mechanical implementation only.  Do not run Python, Node, GAP,
git, GHA, or network locally.  Edit only the same five task232 files
authorized by task237.  Parent Sol owns mathematics, acceptance, execution,
and provenance.

## 1. Rejection boundary

The task237 return is rejected before execution.  Preserve its corrected
top-level task198 path, exact ten substitutions, actual task179 affine calls,
and removal of the unconditional UNKNOWN branch, but do not preserve any
certificate claim merely because the two current sources agree.  Repair all
Sections 2--9.  Status remains `UNEXECUTED`.

## 2. Correct normalized echelon ancestry

`Echelon.reduce(source)` currently returns coefficients with

```text
remainder = source + sum_i coeff_i * source_i.
```

If the new pivot coefficient is two, `insert` scales the row by two but does
not scale the inherited `coeff_i`; it scales only the new `source_id`.
Therefore its stored ancestry is false.  Multiply every inherited
coefficient by the same pivot scale before storing, in producer and every
checker echelon which retains ancestry.  Add a SELFTEST whose first reduction
is nontrivial and whose final pivot scale is two, then replay the union of all
source keys literally.

## 3. Keep boundary ancestry in every K row

A nonmember query returns

```text
normalized = scale * (candidate + B_coefficients + K_coefficients).
```

The current `k_terms` keeps the candidate and prior K terms but drops all B
terms, then incorrectly demands that the resulting relator combination equal
the normalized raw row literally.  Choose and serialize one of these exact
representations:

1. retain the complete translated-boundary word/row ancestry and replay
   `literal_relator_value + serialized_boundary_combination == stored_row`; or
2. retain raw literal value separately and prove its difference from the
   normalized representative by the complete boundary receipt.

In either case replay every coefficient and sign.  A Boolean `replay=true`
is not evidence.  A4's exported basis word is the explicit reduced product
of the retained conjugated relators; serialize that source word, evaluate it
in all ten successors, require roof identity, and compare its translation to
the stored basis value modulo the serialized boundary combination.

## 4. Complete the positive K certificate

For rank `t`, serialize and replay rather than merely state:

- all 6,441 initial defect containments;
- all four generator translates of every final basis row;
- source-generator action matrices on the K basis, with positive/inverse
  products equal to identity;
- order three and pairwise commutation of the retained source-word values;
- basis independence modulo the complete boundary family;
- `order=3^t` and `nilpotence_bound=2t+1`; and
- an actual evaluation receipt for the preregistered roof-trivial word
  `[x,y]^3`, including K coordinates or an honest nonmember terminal.

Do not emit `word_bearing=true` from ancestry labels alone.  Do not emit an
evaluator as metadata naming a Python function without at least the concrete
canary evaluation and a complete serialized ABI for downstream replay.

## 5. Rebuild the checker modulo complete boundaries

The current checker inserts raw defects into its K echelon, then compares
producer/checker raw spans with `in_span` while omitting the boundary family.
Producer rows are normalized modulo boundaries, so this comparison is not the
claimed quotient-span equality.  Reconstruct an independent quotient basis
and prove both containments modulo the independently completed boundary span.
Compare every producer row against checker `B+K`, and every checker row
against producer `B+K`, with explicit separated coefficients or a full
zero-correlation dual.

Decode and replay every producer initial membership, boundary insertion,
negative dual, K ancestry, generator translate, action matrix, inverse
matrix, order/commutator canary, rank/order/nilpotence field, and concrete
`[x,y]^3` evaluator receipt.  Matching rank and two raw `in_span` loops are
insufficient.

## 6. Remove shared boundary-oracle logic from the checker

Both current paths call the same imported
`task179.boundary_oracle`.  That is shared decision logic, not an independent
checker.  The checker may reuse authenticated task179 group/row data, but it
must implement its own support-times-occurrence correlation, translation
selection, and full-zero-correlation proof with a different traversal and
pivot order.  It may call primitive group multiplication/inverse and
`translated_boundary`; it may not call producer `ActualBoundaryOracle` or
task179's deciding `boundary_oracle`.  Compare the independently generated
active row/provenance with the producer transcript.

## 7. Make SELFTEST and mutations semantic

The present 50 names still collapse into four edits (`contexts=[]`,
`affine_checks={}`, `boundary=[]`, `basis=[]`, or `rank=0`) and are checked by
one shallow predicate.  Reduce aliases and mutate each retained owning datum.
Invoke the same replay functions used for a positive certificate.  An
accepted mutation must escape as a fatal exception; never catch an explicit
accepted sentinel.  At minimum retain separate live controls for pivot
scaling ancestry, boundary coefficient/sign, omitted relator, omitted
translate, early queue terminal, source word, action and inverse matrices,
quotient span direction one and two, complete zero-correlation, task198
binding, resource/UNKNOWN, and every forbidden downstream conclusion.

The SELFTEST must have overlapping boundary/defect support, rank at least two,
a dependent relator, a dependent translate, a pivot-scale-two ancestry, and
two different bases equal only modulo the nonzero boundary span.

## 8. One live resource meter and strict driver terminal equality

Production currently creates an outer `ResourceMeter` which stays almost
zero and a separate `Task179Monitor`.  Use one invocation-wide live meter or
faithfully merge every counter before sealing.  Enforce wall and RSS on the
same path.  A checkpoint must contain enough deterministic transcript to
resume or be honestly labelled rank-zero restart; it is never progress.

In production the driver currently checks only that one producer terminal
and one checker terminal exist.  Extract both exact anchored terminal values
and require literal equality before creating the sentinel.  UNKNOWN may pass
the transport lane only as UNKNOWN and must never carry A4 milestone ones or
independent acceptance.  Refresh source pins after edits.

## 9. Delivery

Process Sections 1--8 in order.  No execution or mathematical terminal may
be claimed.  End with:

```text
A4 PRESENTATION INPUT:       0/1 AWAITING ACCEPTED TASK198
A4 INVARIANT CLOSURE:        0/1 UNEXECUTED
A4 WORD-BEARING K:           0/1 UNEXECUTED
A0/A2/A3:                    UNCHANGED
A5 AND LATER:                UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```
