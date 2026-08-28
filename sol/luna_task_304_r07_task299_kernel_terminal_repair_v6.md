# Luna task 304 — task299 generalized kernel terminal repair v6

Role: Luna implementation repair only.  No mathematical adjudication.  Do
not run Python, Node, GAP, GHA, network, or git; parent Sol is the execution
and git broker.

## 1. Scope

Task299/v5 is rejected before execution by the independent task301 audit.
Create exactly five new v6 paths:

1. `search/d972_r07_joint_slice_kernel_general_v6.py`
2. `crosscheck/check_d972_r07_joint_slice_kernel_general_v6.py`
3. `search/d972_r07_joint_slice_kernel_general_gha_driver_v6.g`
4. `search/certs/d972_r07_joint_slice_kernel_general_selftest_v6_20260828.json`
5. `sol/luna_reply_304_r07_task299_kernel_terminal_repair_v6.md`

Do not change v1--v5 or any other path.  The GAP driver is ASCII-only.
Production stays typed `STATIC_BLOCKED` until actual matrices are staged.

## 2. Fatal v5 repair

The v5 producer applies every mutation to the `outside-nonmember` case.  Its
`terminal` mutation writes `MUTATED`, but `compile_case` interprets every
string other than `MEMBER` as expected nonmembership.  The unchanged case is
indeed nonmember, so the mutation is accepted and the producer's required
19/19 gate can never pass.

Before converting a terminal to a Boolean, require the exact enum
`{"MEMBER","NONMEMBER"}`.  A terminal mutation must change the canonical
object and be rejected for terminal semantics, not incidentally by a summary
counter.

## 3. Preserve and strengthen the v5 contract

Retain all five fixture cases, plural seeds, distinct named actions, complete
rank-based joint closure, post-`C` left kernel, zero-dimensional and
dimension-two/cardinality-eight canaries, separate `kernel_dim=d` and
`full_nonzero_kernel_cardinality=3^d-1`, full Hd1/member-ancestry/nonmember-
dual replay, and all 19 owners.

For every producer and checker mutation:

- prove the mutated canonical object differs from baseline;
- reseal it;
- run a semantic gate independent of aggregate mutation counters; and
- attach the 19/19 summary only after all individual verdicts exist.

Audit every `require` call again: because `require` uses `is True`, every
argument must be an explicit Boolean.  Retain the producer wrong-nonempty-
fixture-seal canary and add an independently executed checker-side wrong-seal
canary rather than relying only on its ordinary fixture parse.

The checker must not import the producer.  It must reconstruct the closure,
left kernel basis dimension, full nonzero kernel roster/cardinality, Hd1,
MEMBER coefficient ancestry or NONMEMBER dual, terminal enum, receipt seal,
and all 19 mutations from raw fixture/receipt fields.

## 4. Driver

Pin v6 producer, checker, and fixture by exact bytes/SHA; reject all stale
outputs; run producer before checker; require one exact producer success
terminal and one exact checker success terminal; explicitly compare the two
normalized terminal values (or bind both to one documented common value);
require nonempty receipt/verdict/logs; and write exactly one sentinel after
all gates.  Do not edit a workflow.

## 5. Reply boundary

Report final bytes/SHA, all five expected ranks/dimensions/cardinalities and
terminals, producer and independent checker 19/19 mutation results, both
wrong-seal canaries, and `UNEXECUTED`.  State that this is only an
implementation SELFTEST candidate: actual A5 and A6 remain 0/3, and no lift,
fake, or Ihara result is declared.

