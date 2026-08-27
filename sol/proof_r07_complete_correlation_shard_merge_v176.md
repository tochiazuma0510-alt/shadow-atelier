# R07 complete-correlation shard merge v176

Author: Sol / 2026-08-28

Status: paper theorem and GHA sharding contract.  It proves that the expensive
support-times-boundary-occurrence correlation in tasks187/191 may be split
among workers without changing the complete ACTIVE set.  It does not permit
parallel, order-dependent pivot insertion and does not declare either
boundary target decided.

## 1. Registered pair universe

Fix one current echelon span (S), one fresh dual (lambda) annihilating
(S), and one PB3 or PB4 block (b).  Write the literal support of the dual
as

\[
 L_b=\{(j,g,\lambda_{j,g})\},
\tag{1.1}
\]

and the complete occurrence roster of the two or eleven presentation
relators as

\[
 O_b=\{(r,j,h,a_{r,j,h})\}.
\tag{1.2}
\]

Repeated occurrences remain separately indexed until their contributions
are added.  The registered pair universe is

\[
 U_b=\{((j,g,\lambda_{j,g}),(r,j,h,a_{r,j,h}))\in L_b\times O_b\},
\tag{1.3}
\]

where the component (j) must match.  For a pair (z\in U_b), put

\[
 \kappa(z)=(b,t,r),\qquad t=gh^{-1},
 \qquad w(z)=\lambda_{j,g}a_{r,j,h}\in\mathbf F_3.
\tag{1.4}
\]

The multiplication order in (1.4) is load-bearing and is checked by
(th=g).  The complete serial correlation is

\[
 C(k)=\sum_{z\in U_b:\,\kappa(z)=k}w(z).
\tag{1.5}
\]

Its ACTIVE keys are exactly those (k) for which (C(k)\ne0).

## 2. Exact shard theorem

Choose a preregistered deterministic partition

\[
 U_b=U_{b,0}\sqcup\cdots\sqcup U_{b,s-1}.
\tag{2.1}
\]

For example, enumerate (1.3) in the frozen
`(block, component, dual-support-ordinal, relator-index,
occurrence-ordinal)` order and assign ordinal (m) to shard (m\bmod s).
No process-dependent hash function may define the partition.

Worker (q) returns the sparse partial correlation

\[
 C_q(k)=\sum_{z\in U_{b,q}:\,\kappa(z)=k}w(z).
\tag{2.2}
\]

### Theorem 2.1 (COMPLETE SHARD MERGE)

If the shard manifests prove pairwise disjointness and exhaustive coverage
of the registered ordinal interval, then

\[
 \boxed{C(k)=\sum_{q=0}^{s-1}C_q(k)}
\tag{2.3}
\]

for every typed key (k).  Hence deleting zero coefficients only after the
merge gives exactly the serial ACTIVE set, including every cancellation
which crosses a shard boundary.

#### Proof

By (2.1), every (z\in U_b) occurs in exactly one inner sum in the
right-hand side of (2.3).  Finite addition in (mathbf F_3) is associative
and commutative, so regrouping the terms by shard and then by the common key
(kappa(z)) gives (1.5).  In particular, a nonzero partial coefficient is
not evidence for an ACTIVE key: only the fully merged coefficient decides
whether it survives. \(\square\)

### Corollary 2.2 (SERIAL EQUIVALENCE)

Materialize the translated boundary row belonging to every merged ACTIVE
key and sort the rows by

```text
(block, translation_blob, relator_index).
```

Reducing that list against (S) in this order and retaining exactly the
rank-raising rows produces the same echelon transcript as task191's serial
batched schedule.

#### Proof

Theorem 2.1 gives the identical input key set.  Literal row reconstruction
is a function of the typed key and the pinned boundary source.  The initial
span and the reduction order are also identical, so induction along the
ordered ACTIVE list gives the same remainder, retained/dependent decision,
pivot, ancestry, and next span at every position. \(\square\)

The translated rows themselves may be constructed in parallel.  Their
pivot insertion may not: two rank-raising rows can exchange pivots and
ancestry when inserted in a different order.

## 3. Negative and resource terminals

A fresh dual is a valid `NONMEMBER_D` certificate only if all of the
following hold:

1. it annihilates every row in the current literal span and pairs nontrivially
   with the unresolved target;
2. every shard authenticates the same source, dual, block, pair-universe and
   partition manifest;
3. the shard ordinal sets are disjoint and cover the entire registered
   interval;
4. all partial maps are merged modulo three before zero deletion; and
5. the resulting complete ACTIVE set is empty.

A missing, duplicated, timed-out, malformed, or wrong-commit shard is
`UNKNOWN_RESOURCE` or `UNKNOWN_INPUT`.  It is never interpreted as the zero
partial map.  Stopping after a nonempty merged ACTIVE set only supplies the
next exact rank batch, not a negative result.

## 4. GHA artifact contract

Each worker receipt must bind at least

```text
immutable commit SHA
producer/checker/source identities
dual sparse row and digest
block and complete occurrence-roster digest
shard_count, shard_index, partition rule and ordinal interval/count
number of matching pairs actually consumed
sparse partial correlation before global zero deletion
resource counters and typed terminal
self digest
```

The merge job authenticates every worker independently, rejects duplicate or
missing indices, verifies the partition arithmetic and total pair count,
performs the modular merge, and only then builds the canonical ACTIVE list.
An independent checker reconstructs the same partition and correlation from
the pinned arithmetic sources; sharing the producer's partial-map helper is
forbidden.

For a later dual round, all shards must use the checkpoint produced after the
previous canonical rank merge.  Shards from different duals or spans cannot
be mixed.  Thus parallelism occurs inside one complete correlation round;
the succession of fresh duals remains causally ordered.

## 5. Performance consequence

If a correlation has (N=|U_b|) matching pairs and (A) merged ACTIVE
keys, (s) balanced workers reduce the dominant pair scan from serial
(O(N)) wall work to approximately (O(N/s)) wall work, plus artifact and
merge overhead.  The (A) canonical row reductions remain serial.  This is
most useful together with task191 batching: sharding shortens each complete
correlation, while batching reduces how many complete correlations are
needed.

No linear speedup is asserted before a GHA timing receipt.  Skew, sparse-map
size, artifact transfer, and the final echelon merge may dominate for large
(s).

## 6. Fixed frontier

```text
COMPLETE CORRELATION SHARD EQUIVALENCE:       PAPER_PROOF
CANONICAL ACTIVE/RANK MERGE EQUIVALENCE:      PAPER_PROOF
FAIL-CLOSED NEGATIVE SHARD CONTRACT:          SPECIFIED
TASK191 BATCHED SELFTEST:                     IMPLEMENTATION AUDIT
GHA MATRIX SHARD IMPLEMENTATION:              NOT YET IMPLEMENTED
U0/V0 BOUNDARY DECISION:                      UNKNOWN_RESOURCE IN V1
TASK186 EXACT FIRST CORRECTION:                GHA IN PROGRESS
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED
```

`R07_COMPLETE_CORRELATION_SHARD_MERGE_V176_PAPER_GRADE`
