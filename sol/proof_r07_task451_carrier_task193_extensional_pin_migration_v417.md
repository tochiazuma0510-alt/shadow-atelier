# R07 Task451 carrier -> task193 extensional pin migration (v417)

Author: Sol / 2026-09-01

Status: paper interface theorem.  It proves that the accepted task193-v4
affine-prefix mathematics is extensional in the literal carrier produced by
v416.  A Task451 dialect therefore needs a new authenticated input branch and
new exact pins, but not a new affine-prefix algorithm.  No active Task451 run
is assumed positive and no A0, A2, A5, lift, fake, or Ihara numerator is
changed.  `verified=false`.

## 1. The dialect-free carrier

Let

\[
 \mathcal L=(g_0,a,f,J,\omega)
 \tag{1.1}
\]

be a v416 normalized positive carrier.  Thus

\[
 g_0=g_{760},\qquad f=\operatorname{red}(g_0a),
 \qquad \operatorname{exp}(a)=(0,0),
 \tag{1.2}
\]

and `omega` contains the independently accepted Task451 ancestry plus a fresh
eleven-occurrence/all-seven literal replay.  Write `J.row` for the canonical
sparse direct row and `J.row_sha256` for its historical sparse serialization
digest.  Acceptance of (1.1) includes

```text
direct_all_seven_replay = true
eleven_occurrence_replay = true
right_g760_multiplication = true
hexagons = true
pentagon_printed_order = true.
```

The first three gates are mathematical; the last two fix the exact consumer
convention already used by task193.  A Task451 status or Boolean alone is not
an object (1.1).

Define the dialect-free task193 input

```text
I(L) = {
  exactification: {
    positive_receipt: true,
    literal: {c_exact: a}
  },
  exact_direct_replay: {
    row: J.row,
    row_sha256: J.row_sha256,
    replay: {
      corrected_word: f,
      direct_all_seven_replay: true
    },
    right_g760_multiplication: true,
    hexagons: true,
    pentagon_printed_order: true
  }
}.
```

This is exactly the object constructed by `minimal_input` in the accepted
task193-v2 owner and by `minimal_from_boundary` in its independent checker.
Task193-v4 is an exact-pin successor of that code and changes no compiler
arithmetic.

## 2. Extensionality of the affine-prefix compiler

### Theorem 2.1 (TASK193 DEPENDS ONLY ON THE LITERAL CARRIER)

Fix the task179/task198 owners and one vector of resource caps.  Suppose two
independently accepted adapter dialects normalize to carriers
`L` and `L'` with

\[
 (g_0,a,f,J)=(g'_0,a',f',J').
 \tag{2.1}
\]

Run the task193-v4 mathematical core from rank zero on the two normalized
inputs.  Then all mathematical output fields agree: corrected relation words,
ordinary and affine-prefix rows, `d1_pt`, `beta1`, `B1a`, `e1_pt`, `e1_aug`,
marked-map replays, equality-oracle decisions, and the presentation-boundary
transcript.  Only adapter receipt/verdict identities, their provenance fields,
and checkpoint seals containing those identities may differ.

#### Proof

The producer's accepted-adapter parser returns only

```text
c_exact, corrected_word, g760, direct_replay,
adapter_receipt identity, adapter_verdict identity.
```

Before the compiler is called, `minimal_input` deletes the two identity fields
and constructs exactly `I(L)`.  The call is

```text
owner.actual_compile(args, I(L), artifact_identity).
```

Inspection of the frozen `actual_compile` owner shows that
`artifact_identity` is used only in the resume-input equality, the emitted
checkpoint `input_identity`, and returned provenance.  Every group operation,
Fox row, affine label, boundary correlation, pivot, and relation word is a
deterministic function of `I(L)`, the frozen owners, and the caps.  Equation
(2.1) gives `I(L)=I(L')`, hence the complete mathematical execution is the
same.  The independent checker repeats the same normalization through
`adapter_boundary` and `minimal_from_boundary` and reconstructs the pointed
rows from the literal words rather than from an adapter label.  This proves
the claim. \(\square\)

The qualification "from rank zero" is load-bearing.  A checkpoint is bound to
its physical adapter identities and must not be moved between dialects merely
because (2.1) happens to hold.

## 3. Consequence for a Task451 successor

### Corollary 3.1 (PIN MIGRATION, NOT COMPILER REWRITE)

After a dedicated Task451 carrier producer/checker accepts (1.1), a correct
task193 successor may:

1. retain the task193-v4 mathematical owner and independent replay;
2. replace only the accepted adapter schema/terminal and the exact producer,
   checker, and driver pins by the new Task451-carrier dialect;
3. normalize that dialect to `I(L)` before calling the frozen mathematical
   core; and
4. advance its own schema, terminal, checkpoint schema, paths, and provenance
   tags.

It must not call the history-free adapter-v5 checker on a Task451 artifact,
forge a v5 envelope, reuse a v5 checkpoint, or copy Task451 batch/dual/echelon
state into task193.  Conversely, reimplementing the affine-prefix equality
oracle is unnecessary and introduces no new mathematics.

The same extensional boundary applies to the already prepared task193-v4
consumers: after an accepted new task193 receipt/verdict exists, their next
version is an exact live-pin migration.  Their A5/A7 or q2 arithmetic must not
be changed merely because the upstream A0 discovery dialect changed.

## 4. Fixed frontier

```text
TASK451 POSITIVE -> DIALECT-FREE LITERAL CARRIER: v416 PAPER-CLOSED
LITERAL CARRIER -> TASK193 MINIMAL INPUT:          PAPER-CLOSED
TASK193 AFFINE MATHEMATICS IS ADAPTER-EXTENSIONAL: PAPER-CLOSED
NEW TASK451 CARRIER PRODUCER/CHECKER:              IMPLEMENTATION PENDING
NEW TASK193 TAGGED PIN SUCCESSOR:                  IMPLEMENTATION PENDING
ACTUAL TASK451 POSITIVE / ACTUAL TASK193:          PENDING
A5/A7 / COMPATIBLE LIFT / FAKE / IHARA:           UNCHANGED
```

`R07_TASK451_CARRIER_TASK193_EXTENSIONAL_PIN_MIGRATION_V417_PAPER_GRADE`

