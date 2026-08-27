# Luna task 187 — R07 `u0/v0` boundary-preimage shortcut v1

Commissioner: Sol / 2026-08-27

Reply to:
`sol/luna_reply_187_r07_u0v0_boundary_preimage_v1.md`.

Role: bounded mechanical implementation only.  Do not run Python, GAP, Node,
git, GHA, or network locally.  Parent Sol owns audit, repository brokerage,
and execution.  This task is independent of the task186 full normalized
column generator and must not edit task175, task179, or task186 files.

## 1. Mathematical objective

Use the fixed task179 all-seven first-rung system.  Let `D` be the span of
all left translates of the two PB3 and eleven PB4 presentation-boundary
rows, with the three blocks kept disjoint.  Let `A(w)` be the raw H1/H2/
printed-pentagon change of a literal joint-kernel correction word, with the
two exponent coordinates removed.

From the authenticated 6,441-word roster select the unique q0-relator words
`r3,r9,r12` and form literally

```text
v0 = r9 r12 r3^-2,        exp(v0)=(0,18),
u0 = r9 v0^-8,            exp(u0)=(18,0).
```

Decide, separately and exactly,

```text
-A(u0) in D,
-A(v0) in D.
```

For every positive answer return a complete boundary coefficient chain
`d_u` or `d_v`, with

```text
A(u0)+d_u=0,              A(v0)+d_v=0.
```

Then `(u0,d_u)` and `(v0,d_v)` are word-bearing preimages of the two standard
vectors in `nu(ker A_total)`, where `nu=exp/18 mod 3` and boundaries have
zero tail.  If both answers are positive, a raw task179 correction `c` can
be normalized by right multiplying suitable powers of `u0,v0`, after which
the registered cubes exactify the integer exponent.  Do not claim a raw
task179 word exists in this task.

## 2. Authorized files

Create only:

```text
search/d972_r07_u0v0_boundary_preimage_v1.py
crosscheck/check_d972_r07_u0v0_boundary_preimage_v1.py
search/d972_r07_u0v0_boundary_preimage_gha_driver_v1.g
search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json
sol/luna_reply_187_r07_u0v0_boundary_preimage_v1.md
```

Authenticate the current task179 producer, independent checker, driver,
fixture, v156, v157, and every arithmetic source used, by exact bytes and
SHA-256.  The task179 v1 files remain byte-for-byte unchanged.

## 3. Producer algorithm

Reuse the authenticated task179 runtime only as a pinned arithmetic source.
Do not import task186.  Integer exponent is a fresh signed-letter count; do
not call task179 `exponent_pair`, because that function already reduces
modulo three.

1. Reconstruct the complete fixed runtime and the 6,441 roster.
2. Select and replay `r3,r9,r12`; evaluate each and `u0,v0` in the registered
   joint group, and recompute all five integer exponents.
3. Compute `A(u0),A(v0)` by the literal task179 direct all-seven path and
   remove exactly the two exponent keys.
4. Start one boundary-only echelon from rank zero.  Identity translates may
   be deterministic seeds, but every retained row must raise rank and retain
   full coefficient ancestry and boundary provenance.
5. For each unresolved target, form an exact dual annihilating the current
   boundary span and nonzero on that target.  Use the complete task179
   support-times-occurrence `boundary_oracle` over all translated PB3/PB4
   rows.  An ACTIVE row is replayed literally and retained.  Continue until
   the target is in the span or the complete correlation has no active row.
6. A positive result materializes and directly replays its complete boundary
   coefficient chain.  A negative result may be called `NONMEMBER_D` only
   after storing a dual whose pairing is zero with the complete translated
   boundary family and nonzero on the target; the checker must independently
   prove the full correlation is empty.  A resource cap is `UNKNOWN_RESOURCE`,
   never nonmembership.

The two targets should share retained boundary columns.  Always reconsider
both remainders after each rank increase.  This is an exact finite linear
decision, not a sampled search.

## 4. Consequence receipt

Record one of `MEMBER_D`, `NONMEMBER_D`, or typed `UNKNOWN_RESOURCE` for each
of `u0,v0`.  On membership retain:

```text
target sparse row and digest
ordered boundary coefficients and full provenance
literal reconstructed boundary sum
exact zero residual and digest
u0/v0 literal word, joint value, integer exponent, normalized residue
all rank transitions and coefficient ancestry
```

If both are `MEMBER_D`, record the proved finite consequence

```text
nu(ker(A on correction plus boundary coefficients)) = F3^2
```

and the explicit normalization rule for an arbitrary task179 raw positive
word.  This is only a first-rung selector.  Do not declare a task179 success,
cofinal lift, fake, or Ihara witness.

## 5. Independent checker

The checker must not import this producer.  It may use the authenticated
task179 independent checker as its arithmetic base, with no producer helper
sharing.  Independently reconstruct the runtime, roster ordinals, words,
integer exponents, `A(u0),A(v0)`, every translated boundary row, echelon
transition, coefficient recovery, and terminal dual correlation.  Compare
literal rows and full ordered ancestry, not booleans or hashes alone.

## 6. SELFTEST and controls

Use a bounded noncommutative toy with two targets: one in the full translated
boundary span and one outside.  Exercise the same echelon, coefficient, and
complete-dual-correlation functions.  At minimum reject mutations of one
roster ordinal, one exponent sign, the `u0` formula, the `v0` formula, one
target sign, one block tag, one boundary coefficient, one left translation,
coefficient two/inverse, one pivot ancestry entry, one positive residual,
one terminal dual coefficient, a sampled-as-complete flag, and a resource
stop changed to nonmembership.

## 7. Driver and reply

Provide serial SELFTEST/PRODUCTION bindings, fail-closed resource limits,
fresh outputs, exact-one producer/checker markers, terminal agreement, and
artifact upload compatibility.  Give a conservative GHA time/RSS estimate.
The reply processes Sections 1--7 in order, gives exact identities for all
five files, and ends with:

```text
U0 BOUNDARY PREIMAGE:                       NOT EXECUTED BY LUNA
V0 BOUNDARY PREIMAGE:                       NOT EXECUTED BY LUNA
RAW-TO-NORMALIZED SHORTCUT:                 NOT DECLARED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:     NOT DECLARED
```
