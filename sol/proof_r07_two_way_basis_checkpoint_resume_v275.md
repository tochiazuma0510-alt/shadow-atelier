# R07 two-way basis checkpoint resume theorem v275

Author: Sol / 2026-08-29

Status: paper fallback for the A0 positive-only search.  It gives an exact
certificate by which a retained-column span can be resumed without serially
reinserting every column from rank zero.  It does not assert that the current
checkpoint already contains this certificate, that v6 needs the repair, or
that any COMMON word exists.  `verified=false`.

## 1. The restart bottleneck to separate from boundary correlation

Let \(V\) be the finite-support F3 row module of the task192 solver.  An
authenticated checkpoint retains actual rank-raising columns

\[
 C=(c_1,\ldots,c_n).
\tag{1.1}
\]

The current firewall obtains a trusted basis by inserting (1.1) sequentially
into a new sparse echelon.  This is sound, but it is a distinct cost from the
fixed-dual translated-boundary correlation.  A worker pool installed only
after resume cannot accelerate the preceding reconstruction.

Hashing a serialized old pivot basis is not a substitute: it authenticates
bytes, not equality of spans with (1.1).  Conversely, exact equality of spans
is enough for a new positive-only solver.  It need not reproduce the same
historical pivots or dual choices, provided every future column and final
positive witness is replayed semantically.

## 2. Two-way sparse basis certificate

Let

\[
 P=(p_1,\ldots,p_r)
\tag{2.1}
\]

be a proposed normalized sparse basis.  Retain finite coefficient matrices
\(A=(a_{ij})\) and \(B=(b_{ji})\) such that

\[
 p_i=\sum_{j=1}^{n}a_{ij}c_j,
 \qquad
 c_j=\sum_{i=1}^{r}b_{ji}p_i.
\tag{2.2}

All coefficients are canonical F3 values and all sparse row equalities in
(2.2) are checked directly from the immutable raw rows.  Also require that
P has r distinct registered pivots, each normalized to one, and that every
other P row is zero at that pivot.  Thus P is linearly independent.

### Theorem 2.1 (TWO-WAY CHECKPOINT SPAN)

The data in (2.1)--(2.2) prove

\[
 \boxed{\operatorname{span}C=\operatorname{span}P,
        \qquad \dim\operatorname{span}C=r.}
\tag{2.3}
\]

#### Proof

The first family in (2.2) gives \(\operatorname{span}P\subseteq
\operatorname{span}C\).  The second gives the reverse inclusion.  The pivot
conditions make the r rows of P independent, proving the dimension. \(\square\)

Neither containment may be omitted.  In particular, proving only that all
retained columns reduce to zero against an arbitrary larger independent P
does not show that P belongs to the retained-column span.

## 3. Sound positive-only resume

After accepting Theorem 2.1's certificate, reduce the authenticated target
against P and construct a fresh exact dual by active-coordinate linear algebra.
Discard every historical reduced-target, dual, boundary accumulator, and
winner unless separately rebound to this new basis/dual identity.  Continue
the lazy column-generation search from

\[
 B_0=\operatorname{span}P.
\tag{3.1}
\]

Every new actual boundary or correction column is independently constructed,
replayed, reduced, and appended only on a true rank rise.  Only these live
objects determine later choices.

### Theorem 3.1 (HISTORY-FREE POSITIVE RESUME)

Suppose the retained raw columns in C are all sound columns of the original
membership problem and (2.2) passes.  Then a COMMON terminal reached by the
resumed solver, with a complete raw coefficient and word replay, is a valid
COMMON terminal for the original target problem even if its intermediate
basis, duals, or column order differ from serial cached-v3.

#### Proof

Theorem 2.1 identifies the exact starting span.  Every later accepted column
is an actual problem column, so the live span remains a subspace of the full
allowed column space.  A positive target reduction expresses the target as a
finite combination of the retained and newly replayed raw columns.  Replaying
that expression proves membership independently of the path used to find it.
No negative conclusion is drawn from a cap or unfinished search. \(\square\)

This is the checkpoint analogue of the history-free principle in v265.
Exact cached-v3 path parity is stronger and unnecessary for a proof-carrying
positive result.  If a wrapper nevertheless claims byte-for-byte simulation
of cached-v3, it must separately prove the exact registered pivot state and
dual; Theorem 3.1 alone does not provide that stronger claim.

## 4. Independent construction and checking

A production package has three roles which must not share an unchecked
helper:

1. a builder constructs P and one direction of (2.2), for example by sparse
   top-pivot elimination;
2. the producer checks that direction, constructs/checks the reverse map,
   and starts the live positive-only search; and
3. the independent checker reconstructs the raw columns from literal
   provenance, uses an opposite pivot/order convention, checks both families
   in (2.2), and replays the final COMMON coefficients and word.

An independently accepted precomputation of P/A/B may be transported as an
immutable artifact.  Source hashes and seals protect its identity, while the
two-way row equalities supply its mathematics.  A producer and checker which
both merely trust the same stored `span_equal=true` field do not satisfy the
theorem.

For the current task192 checkpoint, every boundary raw column must replay its
typed translated relation and every correction raw column must replay its
literal conjugated word and exact sparse defect before it may enter C.  The
existing provenance gates are retained.

## 5. Performance contract

Let \(N_C\), \(N_P\), \(N_A\), and \(N_B\) be the total sparse nonzero counts
in C, P, A, and B.  Certificate checking charges the actual sparse multiply/
accumulate work for both equalities in (2.2), typed-key comparisons, pivot
checks, target reduction, and dual construction.  These checks can be divided
into disjoint row intervals because every row equality has a fixed immutable
input, then merged in canonical order.

No universal speedup is claimed: A or B may be dense, and exact verification
may still exceed a resource cap.  The intended gain is removal of the serial
dependency chain "insert c1, then c2, ..." when a sparse two-way certificate
is materially smaller or more parallel.  Actual bytes, nonzeros, wall time,
RSS, serialization, and worker traffic must be measured before choosing this
route.

A checkpoint accepted only by probabilistic hashing or Freivalds checks is a
candidate accelerator, not a cross-checked mathematical resume.  Exact row
replay remains the promotion gate.

## 6. Mutations and failure discipline

Required negative controls include changing one raw column/provenance,
deleting one P pivot, changing a coefficient independently in A and B,
dropping either containment, using a noncanonical F3 value, adding a hidden
row key, importing a stale target/dual, claiming cached-v3 path parity from
span equality, and emitting a positive result whose raw combination does not
replay.

Failure of the two-way package is `UNKNOWN_INPUT`; exceeding a registered
verification/search cap is `UNKNOWN_RESOURCE`.  Neither is a separator or
nonexistence result.

## 7. Fixed frontier

```text
TWO-WAY RAW-COLUMN/BASIS SPAN CERTIFICATE:      PAPER PROOF
HISTORY-FREE POSITIVE RESUME FROM THAT SPAN:    PAPER PROOF
SEQUENTIAL RANK-ZERO INSERTION:                 NOT MATHEMATICALLY REQUIRED
CURRENT CHECKPOINT TWO-WAY PACKAGE:             NOT CONSTRUCTED
V6 NEED FOR THIS FALLBACK:                      UNDER TASK337 AUDIT
ACTUAL A0 COMMON + CHECKER:                     0/1
LIFT / FAKE / IHARA:                            NONE
```

`R07_TWO_WAY_BASIS_CHECKPOINT_RESUME_V275_PAPER_GRADE`
