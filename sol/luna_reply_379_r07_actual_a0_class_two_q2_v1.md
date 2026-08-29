# Luna reply 379: R07 actual A0 class-two q2 compiler v1

Date: 2026-08-30

## Result

PASS.  The physical ABI needed by v355 is present in the frozen owners, so I
implemented the requested production-first producer, independent checker and
single-pass ASCII GAP driver.  Only the four task379 deliverables were
created.  Production, GHA, git, network, SELFTEST and mutation lanes were not
run.

Task193's positive physical lane is spelled `status=PASS` and terminal
`R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V3`; this is the task379
contract's MEMBER case.  Missing or non-positive task193 input is emitted as
`UNKNOWN_INPUT`.  The accepted literal input is authenticated as
`correction_word`, with

```text
corrected_word = freely_reduce(g760 * correction_word).
```

No A5 receipt is accepted and no `mu1`/`M` coefficient is converted into a
word.

## Implemented replay

The producer restores the frozen task198-v12 core and its v6 source, fully
authenticates the five physical task198 authority files, and reconstructs the
ten producer contexts and eleven owner rows.  The checker separately restores
task198-v14/v6 and its own `CheckerArithmetic`.  Both sides authenticate the
printed factor order

```text
H1: 3,2,1
H2: 6,5,4
P:  11,10,9,8,7
```

while retaining the v4 registered positions, context labels, signs, inverse
slots, literal prefixes, `g_o`, `a_o`, `P_hat_o` and every `d_o` word.  Each
block constructs its old and corrected relation words independently and
requires the freely reduced ordered `d_o` product to equal the complete
relation-word ratio.

PB3/PB4 use the frozen task292 producer roster on the producer side and the
checker-side `pure_pairs`, `presentation_relators` and free-word routines on
the checker side.  The receipt contains generator and wedge rosters, every
relator word and degree-two initial row, the relation echelon, full-relator
zero checks, raw/relation-reduced occurrence coordinates, ratio scans and the
three tagged q2 vectors.  The checker compares the independently reconstructed
sparse coordinate classes and relation spans; it does not import the task379
producer or accept producer pivot numbering/hash as mathematics.

Following v356, the implementation first computes all eleven factors and all
three q2 vectors, then requires the resulting H1/H2/P vectors to be zero.  Zero
is not injected.  A nonzero result fails closed as a v356 ABI mismatch.  This
does not claim q2 return, A9 completion, a compatible lift, mixed-prime or
perfect-core completion, fake, or Ihara.

The producer exposes seconds, RSS, operation and checkpoint-byte caps.
Checkpoints are written after PB3, PB4 and each literal occurrence.  Resume is
an all-or-none path/bytes/SHA input and binds the exact producer source, all
frozen upstream producer/checker sources, the task193 receipt/verdict and the
full task198 physical owner identity.  Controlled caps return
`UNKNOWN_RESOURCE`.  The driver invokes exactly one producer and invokes the
checker only for COMPLETE; it has no retry or dispatch lane.

## Exact executable identities

```text
search/d972_r07_actual_a0_class_two_q2_v1.py
  50355 bytes
  c61d8f2cd96e6dd5c36089ddb83f6519c5e42b0dac66b42e9cec46ca9adfe9a6

crosscheck/check_d972_r07_actual_a0_class_two_q2_v1.py
  51554 bytes
  0b2d944d1655c359ab7252a732fe99f3c92add8e7ea9d45d44825707698deaa0

search/d972_r07_actual_a0_class_two_q2_gha_driver_v1.g
  8218 bytes
  eb80e5ae0b2ae5d9cbb99e7eda38d40da31f7037779f31feca8fec11bc886d9c
```

The driver embeds the first two identities exactly.

## Bounded static checks

- Both Python files compiled from in-memory bytes.
- All three executables decoded as ASCII.
- Task193-v3, task292-v2 and task198-v12/v14 plus both frozen v6 cores were
  restored under their exact byte/SHA pins without invoking a main routine.
- Producer and checker task198 owner-layout constants matched all eleven
  frozen rows.
- The checker producer pin and both driver executable pins matched physical
  bytes exactly.
- GAP 4.16.0 `ReadAsFunction` accepted the driver.
- Static inspection confirmed one producer command, one conditional checker
  command and no SELFTEST lane.

No actual task193 receipt was consumed and no numerical production q2 receipt
was generated in this task, as required by the static-only boundary.
