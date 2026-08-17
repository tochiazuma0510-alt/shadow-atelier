# Luna reply 157ca: literal A.18 finite obstruction repair

## Corrected verdict

The previous rho-tail proposal is withdrawn.  The exact semantic audit in
`sol/luna_reply_152_b4_158_semantic_identity.md` proves that the current
158-row rho tail is not the literal A.18 coface kernel: 41 of the 140 raw
A.18 rows survive modulo the old rho ideal.  Therefore no result computed
with that ideal can be used as the A.18 finite obstruction.

The repaired bundle uses the literal A.18 presentation and the unconditional
five-coface defect.  The three authorized files are:

```text
search/d972_b4_next_obstruction_v1.py
search/check_d972_b4_next_obstruction_v1.py
.github/workflows/d972-b4-next-obstruction-v1.yml
```

The internal receipt schema is versioned as `d972-b4-next-obstruction/v2`,
so old rho-tail receipts cannot pass the new checker.  No GAP, Git mutation,
GHA dispatch, or heavy local computation was used.

## Literal presentation

The frozen six-generator source has 18 K(0,5) prefix relators and 28 M
relator seeds.  The five raw A.18 substitutions are reconstructed as:

```text
123       : (X12,       X23)
234       : (X23,       X34)
12,3,4    : (X13 X23,   X34)
1,23,4    : (X12 X13,   X24 X34)
1,2,34    : (X12,       X23 X24)
```

For each of the 28 seeds, the producer and checker independently apply these
literal signed substitutions.  The ideal input is exactly

```text
P_A18 = (the 18 K(0,5) prefix rows)
       + (the 5 x 28 raw A.18 coface rows).
```

The current rho-orbit tail is never used as an ideal generator.  The
temporary transport object retains the canonical rho field only because the
audited encoded shard parser requires that field; the final receipt marks
`rho_used=false`, `rho_tail_used=false`, and the checker rejects any receipt
that uses rho words or rho^5 as a gate.

The independent binding values are:

```text
canonical source SHA256  c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9
K(0,5) prefix SHA256      62ccbb87e2b27784b5330812252a2eaf247fea0fef4eda078ea6724c5b2a31e6
28 seed SHA256            366c893977a0684a294e8bd488741c735016ec5caf18804415dfc73acdb09822
raw 140-row A18 SHA256    1f0cacaa20ab8474245f30568469de807b5877b2ca7dd0d6668c9b8956750722
literal 158-row SHA256    783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305
literal transport SHA256 60efdb2f7fc847d065701bf27d676cec558e0be9a276ee2a782c3ff0c5754494
```

These hashes are recomputed from the source in both programs; they are not
accepted merely as fields copied from a receipt.  The checker independently
rebuilds the complete deterministic JSON transport, including the legacy rho
parser field, and requires the top-level and every shard record to equal the
reconstructed transport SHA.  The producer fixes LF serialization explicitly,
so this binding is identical on Windows and Linux.

## Unconditional defect

For an F2 roof word `f`, the tested word is the literal five-coface defect

```text
Dtilde(f) =
  f(x45,x34)^(-1) f(x12,x15)^(-1)
  f(x23,x34) f(x45,x51) f(x12,x23).
```

The source convention is `x51=x15`, with
`x15=(X12 X13 X14)^(-1)=[-3,-2,-1]` and
`x45=X34^(-1)X24^(-1)X14^(-1)` in the six-generator alphabet.  The producer
and checker independently reconstruct all 972 D-tilde words from the frozen
word/key artifact and bind their digest:

```text
word/key artifact SHA256  564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9
Dtilde word-list SHA256   32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef
```

This defect is unconditional: an actual five-coface lift forces it to vanish
modulo the literal coface ideal.  No ABS condition, `condition(I)`, or
reverse rho-norm identity is needed for that computational implication.

## Finite quotient and exactness

For each `d=2,3,4,5,6`, the calculation uses

```text
T_d = F2<X1,...,X6> / (all monomials of degree > d)
I_d = span { u (E(r)-1) v : r in P_A18,
                           |u|+degree(E(r)-1)+|v| <= d }
A_d = T_d/I_d.
```

The six generators map to `1+X_i`, with the exact finite geometric inverse
in characteristic two.  The generated unit subgroup is finite, so a nonzero
D-tilde residue is a genuine finite-quotient nonidentity and hence a finite A
candidate.  Every left/right monomial multiple is inserted; there is no
sampling or bounded word search.  The encoded producer shards the complete
ideal, and the checker rebuilds it independently with tuple sets and lowest
pivots, then re-evaluates all 158 literal relators and all 972 defects.

The corrected campaign deliberately does not call the old d2--d5 all-pass
receipts a strict degree progression: those receipts used the rejected rho
ideal.  The workflow calibrates all five corrected degrees.  A nonzero
D-tilde residue at any degree is only
`D{d}_A_CANDIDATE_NEEDS_CHECK` until the independent checker accepts it.
An all-pass degree is `D{d}_ALLPASS_UNKNOWN`, never a terminal B4 result.
Any `relator_bad`, binding mismatch, construction/digest mismatch, or stale
rho field is a gate failure even when the defect list is empty.

## 157cf fail-closed repair

Every merge receipt now contains the exact campaign shard ledger.  For d2--d5
it must contain the sole shard `(index,count)=(0,1)`; d6 must contain exactly
indices 0 through 15 with count 16.  Each record binds its lossless shard-file
SHA, degree, ideal rank, literal transport SHA, complete input-digest map,
source/presentation/D-tilde hashes, producer/core hashes, and the exact list
of assigned relator indices plus its canonical digest.  The union must be the
158 indices exactly once.

The independent checker rejects:

- a missing, duplicate, extra, or out-of-range shard record;
- any shard count, assignment, assignment digest, transport SHA, or input
  digest drift;
- top-level transport SHA drift from its independently reconstructed bytes;
- a supplied pivot list that is not exactly the high pivot of each supplied
  basis row;
- any top-, degree-, or shard-level `rho_used`, `rho_tail_used`, or `rho_role`
  drift, and any stale/unversioned rho field.

The always-running workflow aggregate independently reconstructs the literal
A.18 transport again, checks every original shard artifact, and checks every
merge `shards` record against the corresponding artifact SHA and exact
158-relator partition.  It does not rely on the producer/checker helper code
for this aggregate check.

## GHA certificate plan

The matrix has 20 jobs: one shard each for d2, d3, d4, d5, and 16 shards for
d6.  The merge job combines each degree using the complete exact two-sided
ideal and writes five receipts.  The independent checker consumes all five
receipts.  The aggregate is fail-closed and always uploads evidence.

The bounded d6 workers use a 12,000,000-KB virtual-memory limit and a
350-minute process limit inside 360-minute jobs.  The lower degrees are cheap
calibration lanes.  A construction or checker gate failure makes the
campaign reject; it is never interpreted as an all-pass result.

The workflow and source pins are:

```text
producer       bbf91f461e0c0d9d67ea49186450e709fcb97025ac4ebc3462b3dc6c278eb886
checker        2cd42ed369d9bb946f474cc6c10d90aaa4a32ab53e299c190763749a07660994
shard core     1a18994e3933d5d42e85274af62badb89c2f9a65c92c63862d1740ac2d47da63
merge core     6ccce4e95378dfa22051bd8c09e3d3aa5a91234b8d155c0fb57fd18c34f24bf5
base merge     c79abb6ff51bccaaf98992fa070fecf3aba9d70ea4f6b6deff90d4cfcef1814c
workflow       cafd9bd72e636b2d942fa7065fc197063f7c5b9fcb6b20d58b37be9848f3d2f4
```

Light checks completed without GAP or GHA:

```text
python -B search/d972_b4_next_obstruction_v1.py --mode self-test
D972_B4_NEXT_OBSTRUCTION_V2_SELFTEST_PASS

python -B search/check_d972_b4_next_obstruction_v1.py --self-test
D972_B4_NEXT_OBSTRUCTION_CHECKER_V2_SELFTEST_PASS
```

The negative checker selftest explicitly checks that no defects plus a bad
relator, binding, or construction gate yields `D2_MAGNUS_GATE_FAILURE`.
It also mutates every release-blocking 157cf table case: empty shard records,
an arbitrary 64-character top transport SHA, forged pivots, shard index 99,
and degree-level rho flags.  All are rejected; additional assignment-digest,
shard-transport, input-digest, rho-role, and stale-rho mutations are rejected
as well.

A fresh light d2 temporary shard/merge/check replay passed with ideal rank 27,
quotient dimension 16, all 158 relators zero, and all 972 D-tilde residues zero:
`D2_ALLPASS_UNKNOWN`.  The workflow parsed as YAML, all five embedded Python
blocks parsed as Python AST, and every workflow source pin matched the current
file.  No d6 production was run locally.

The repaired lane is ready for the parent-controlled GHA run.  It reports a
finite A candidate or an honest UNKNOWN, not a terminal A/B claim.

NEXT_FINITE_OBSTRUCTION_READY
