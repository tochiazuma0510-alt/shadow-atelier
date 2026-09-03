# R07: exact endpoint-minimal runtime for the fresh rho2 producer (v484)

Author: Sol / 2026-09-03

Run `33761322235/1`, job `100668089672`, reached
`A0_PROGRESS ... phase=light_runtime_start` at 2026-09-03 13:40:32Z and then
hit the outer producer timeout exactly at 14:25:31Z, before emitting any later
phase marker.  The failure is therefore inside the generic `build_light`
prefix, before the Task640 endpoint/signature and precision-two arithmetic.

This note removes only objects that are absent from the Task640 call graph.  It
does not change the endpoint universe, signature equivalence, eleven
occurrences, selected SLP, precision-two arithmetic, or checker.  It makes no
unmeasured runtime promise.  `verified=false`.

## 1. Actual Task640 call graph

After parent authentication the producer uses the all-seven object through
exactly three public operations:

```text
signature(path)       -> ProducerAllSeven.coordinates(path),
extend_signature      -> quotient multiplication of stored coordinate blobs,
direct_column(d,r)    -> ProducerAllSeven.direct_column(d,r).
```

Inspection of the frozen `ProducerAllSeven` gives the following complete
runtime-key dependency table.

| operation | runtime data read |
|---|---|
| constructor | `old,e3,e4,bridge.g760` |
| `coordinates` | `p176,old,e3,e4,contexts,delete` |
| occurrence/direct Fox column | `old,e3,e4,bridge.g760,joint_group` |
| resource checks | `meter` |

In `direct_column`, `joint_group` is used only as

```text
joint_group.eval(conjugate) == joint_group.identity.          (1.1)
```

No Task640 path reads the complete relation roster, base Fox targets, PB3/PB4
boundary owners, the generic positive-search target, Q0 search states, or the
generic `runtime["model"]` installed by `build_light`.

## 2. Exact lightweight joint evaluator

Let the 31 registered E4 contexts be `(l_i,r_i)`.  Define

```text
J.identity = (e3.identity, (e4.identity)_i),
J.eval(w)  = (e3.eval(embed_F2_PB3(w)),
              (e4.eval(w,[l_i,r_i]))_i).                       (2.1)
```

Equation (2.1) is byte-for-byte the `JointGroup.eval` method and identity used
by the frozen generic runtime.  Hence it gives exactly the same truth value in
(1.1).  The Cayley closure, 243-state transition table, 6,441 relation roster,
section words and re-evaluation of the roster are not used to compute (2.1)
and may be omitted from this consumer.

### Lemma 2.1

Replacing `JointGroup` by the evaluator (2.1) does not change any value returned
by `ProducerAllSeven.coordinates`, `occurrence_column`, or `direct_column`.

#### Proof

The first two methods do not read `joint_group`.  The last reads it only in
(1.1), where (2.1) is definitionally the same evaluation and identity.  All
later Fox and serialization operations use `old,e3,e4` directly and are left
unchanged.  QED.

## 3. Endpoint-minimal construction

The replacement for the generic `build_light` performs only:

1. authenticate the unchanged `SOURCE_PINS` registry;
2. load `live,p176,old` and the pinned `q3` JSON;
3. reconstruct the exact `e3,e4` quotients;
4. reconstruct and authenticate the same 31 E4 contexts and their registered
   context receipt;
5. read `g760` from the already pinned
   `scratchpad/a0_paper_words_v1.json`, require length 760 and digest
   `518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d`;
6. install the Task700/703 accepted endpoint deletion prefix: the complete
   59,049 fine table plus the two authenticated physical Q0 marked rows;
7. install the evaluator (2.1), instantiate `ProducerAllSeven`, and replay the
   zero-word endpoint canary.

Add a meter/progress checkpoint after every numbered item.  This both enforces
the existing resource contract and makes a later finite stop attributable.

The following generic `build_light` objects are not constructed:

```text
JointGroup Cayley closure and 6,441-row roster,
H1/H2/P raw base-target Fox rows,
PB3 and PB4 boundary row families,
generic producer_exact_target,
generic runtime["model"] and light_public target receipt.
```

Their omission is semantic dead-code elimination for this consumer, not an
approximation.  The Task640 producer still authenticates its paper/source pins,
the complete Task625 parent, Task554 state and Task595 equation exactly as
before.

### Theorem 3.1

On every accepted Task640 input, the endpoint-minimal runtime produces the same
ten coordinate blobs for every word and the same complete eleven-occurrence
direct Fox column for every `(delta,relator)` as the generic runtime.

#### Proof

All data in the dependency table of Section 1 are reconstructed by Steps 2--7
with their original definitions.  Coordinates retain the same complete fine
deletion map and contexts.  Lemma 2.1 handles the only use of the removed joint
closure.  The constructor, quotient operations, word substitutions, prefix
orientation, Fox gradients and serialization code are the same frozen
`ProducerAllSeven` implementation.  Therefore every returned blob and sparse
column is unchanged.  QED.

## 4. Required finite release tests

A versioned producer must include production-called fixtures which:

- trap any call to generic `build_light`, `build_roster`, PB boundary builders,
  or `producer_exact_target`;
- compare generic and minimal runtimes on a bounded toy quotient for the empty
  word, four actor letters, a nontrivial conjugate and all eleven occurrence
  descriptors;
- mutate one E3 component and one of the 31 E4 context components so the joint
  evaluator rejects the conjugate;
- bind the exact 31-context order, g760 digest, 59,049 fine-table receipt, two
  Q0 marks, ten coordinate types/order and eleven occurrence signs/order;
- keep the independent checker nonimporting and unchanged except for a new
  exact producer-code pin/manifest schema if required.

The next GHA run must retain the 8-GiB virtual-memory guard and existing caps,
but it should give the producer enough outer wall time to report a genuine
Task640 resource stop rather than silently truncate a longer internal cap.  A
timeout remains `UNKNOWN_RESOURCE`, never a rho2 result.

## 5. Claim boundary

```text
GENERIC BUILD_LIGHT IS REQUIRED BY TASK640:  NO
ENDPOINT-MINIMAL CALL-GRAPH EQUIVALENCE:      PAPER-CLOSED
VERSIONED IMPLEMENTATION / AUDIT:            PENDING
FRESH RHO2:                                  NOT PRODUCED
GRADE-TWO MEMBER/NONMEMBER:                  NOT RUN
A0 / COMMON / COFINAL / FAKE / IHARA:        NOT DECLARED
verified:                                    false
```

`R07_TASK640_ENDPOINT_MINIMAL_RUNTIME_V484_CANDIDATE`
