# Luna task 418 — independent PB4 central-split replay

## Role and scope

You are Luna, the implementation/checking owner.  Read
`sol/proof_r07_a0_pb4_central_split_direct_quotient_v402.md` completely and
implement a bounded helper-nonshared replay of its finite E4 split gate.
Do not implement the six-family production quotient, do not start a heavy
search, do not modify any workflow/prior producer/proof/v220 file, and do not
commit, push, or dispatch.

Allowed new files only:

1. `crosscheck/check_d972_r07_pb4_central_split_v1.py`
2. `search/certs/d972_r07_pb4_central_split_v1_20260830.json`
3. `sol/luna_reply_418_r07_pb4_central_split_crosscheck.md`

## Frozen inputs

- `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json`
  has 231570 bytes; recompute the physical byte count and require the frozen
  SHA-256
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`.
- The producer-side reconstruction used
  `search/d972_b345_seedspan_triple4_v1.py`, but the new checker must not
  import or execute that file.
- You may byte-pin and reuse the independent implementation in
  `search/check_d972_b345_q3_chief_v1.py`, or copy only the small required
  PC/permutation routines into the new checker.  It must not call a helper
  shared with the producer-side source.

Record the independently recomputed q3 receipt byte count in the
checker/reply.

## Required exact checks

Use original marked order

`A12,A13,A14,A23,A24,A34`

and the literal central word

`z = A12*A13*A23*A14*A24*A34`, i.e. index word `[1,2,4,3,5,6]`.

Independently require all of the following.

1. The receipt schema/terminal and PB4 PC/coarse marked widths are the frozen
   accepted ones; the PC group has order 59049, class 2, exponent 3, ten
   relative orders all 3, and the coarse Q4 degree/order fields are pinned.
2. Evaluate the matched E4 word `z` without importing the producer.  Require
   its coarse component is identity, it is nonidentity, its cube is identity,
   and it commutes with all six marked E4 generators.
3. In the PC coordinates require
   `pc(z)=(1,1,1,1,1,1,0,0,0,0)`; require the five new noncentral marked
   generators `A13,A23,A14,A24,A34` have first coordinate zero and `z` has
   first coordinate one.
4. Prove/check from the pinned PC presentation, not sampling, that first PC
   coordinate defines a homomorphism to F3.  A sound way is to check that the
   assignment on the ten PC generators satisfies every power and conjugate
   relation (including inverse-conjugate data if used by the presentation),
   so it descends to the presented group.
5. Independently generate the two relevant Artin actions on free letters
   `p,q,r` and the action of `z3=A12*A13*A23`.  Require the six formulas in
   v402 (1.4), require `z3` acts as conjugation by `w=p*q*r`, and require both
   actions fix `w`.  Do not import the producer's word helpers.
6. Check the source generator identity
   `A12 = z*A34^-1*A24^-1*A14^-1*A23^-1*A13^-1` by matched E4 evaluation.
   Together with the homomorphism gate, emit the exact conclusion
   `H=H0 direct_product <z>` as a theorem consequence, not by enumerating the
   enormous matched group.
7. Add adversarial self-checks which reject at least: wrong central word
   order, replacing first PC coordinate by a non-homomorphic coordinate (if
   available; otherwise mutate a presentation relation), and dropping one
   of the five noncentral generators.

The output JSON must distinguish `cross_checked=true` from `verified=false`,
bind every input/code hash, list every gate, and make no A0/fake/witness
claim.  Exit nonzero on any failed gate.  Run this bounded replay locally and
report wall time, exact output bytes/SHA, checker bytes/SHA, and command.
