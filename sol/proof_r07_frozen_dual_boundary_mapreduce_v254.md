# R07 frozen-dual boundary map/reduce and resumable epoch v254

Author: Sol / 2026-08-28

Status: paper proof for the exact A0 acceleration boundary identified in
v253. It proves equivalence with the serial fixed-dual correlation and the
correct checkpoint invariant. It does not implement the adapter, produce a
COMMON word, or change any witness/fake/Ihara milestone. verified=false.

## 1. Frozen epoch

Fix one exact dual \(\lambda\), the immutable ordered boundary-descriptor
list, and the induced ordered support list. Their Cartesian traversal in the
v3 serial order gives a finite pair roster

\[
 {\cal P}=(p_0,\ldots,p_{N-1}).
\tag{1.1}
\]

Each pair has a key

\[
 \kappa(p_i)=(B_i,r_i,t_i)
\tag{1.2}
\]

and coefficient \(\alpha_i\in\mathbf F_3\). Put

\[
 A(k)=\sum_{\kappa(p_i)=k}\alpha_i.
\tag{1.3}
\]

The v3 boundary result is None if every \(A(k)=0\). Otherwise it selects the
least active key in the frozen order

\[
 (B,t,r),
\tag{1.4}
\]

reconstructs its complete translated row, and directly checks that pairing
the row with \(\lambda\) equals the nonzero value \(A(k)\).

The word frozen is load-bearing: a retained rank increase changes the dual
and therefore starts a different epoch.

## 2. Exact map/reduce

Let

\[
 [0,N)=I_0\sqcup\cdots\sqcup I_{s-1}
\tag{2.1}
\]

be disjoint half-open intervals, listed in increasing start order. Define

\[
 A_j(k)=\sum_{\substack{i\in I_j\\\kappa(p_i)=k}}\alpha_i.
\tag{2.2}
\]

### Theorem 2.1 (FROZEN-DUAL MAP/REDUCE EQUIVALENCE)

If (2.1) is a complete disjoint cover, then

\[
 \boxed{A=\sum_{j=0}^{s-1}A_j.}
\tag{2.3}
\]

After reducing coefficients modulo three and deleting zero coordinates, the
parallel and serial active-key sets, lexicographic winner, translated row,
and direct scalar are identical.

#### Proof

For every fixed key \(k\), disjointness and completeness partition exactly
the index set occurring in (1.3). Associativity and commutativity of addition
in \(\mathbf F_3\) give

\[
 \sum_jA_j(k)
 =\sum_j\sum_{\substack{i\in I_j\\\kappa(p_i)=k}}\alpha_i
 =\sum_{\kappa(p_i)=k}\alpha_i=A(k).
\]

Thus the sparse accumulators agree coordinatewise. Their nonzero supports
and hence the least key under (1.4) agree. The translated row depends only on
that key and the immutable descriptors, so it also agrees. Its direct
pairing with the same frozen dual equals (1.3), which is the same nonzero
scalar. \(\square\)

Contributor provenance is also serially reproducible: retain the pair index
inside every worker record, sort shards by interval start, and concatenate
records in increasing pair index. No algebraic commutativity is used to
reorder provenance.

## 3. Resumable prefix invariant

For \(0\le b\le N\), define the prefix accumulator

\[
 A_{<b}(k)=\sum_{\substack{0\le i<b\\\kappa(p_i)=k}}\alpha_i.
\tag{3.1}
\]

### Theorem 3.1 (CURSOR RESUME)

Suppose a checkpoint binds the epoch identity, cursor \(b\), and the exact
prefix accumulator (3.1). If the resumed run processes every index in
\([b,N)\) exactly once, then merging the suffix accumulator with \(A_{<b}\)
returns the serial value \(A\).

#### Proof

The intervals \([0,b)\) and \([b,N)\) are a disjoint cover of \([0,N)\).
Apply Theorem 2.1. \(\square\)

It is sufficient, and safer, to checkpoint only at deterministic completed
batch boundaries. A batch is committed atomically only after every shard in
that batch has returned, its interval/digest/count/partial/contributor record
has been replayed, and its merged partial has passed direct recomputation.
If one worker fails or resource accounting is uncertain, neither the cursor
nor the persistent accumulator advances.

The prefix accumulator need not be trusted merely because it is sealed. A
checker may reconstruct it from the immutable roster and dual up to \(b\), or
authenticate an independently generated prefix digest and replay selected
coordinates. A positive production receipt must ultimately replay the full
serial correlation or an equivalent complete coordinate proof.

## 4. Epoch identity and reset

A resumable epoch identity must contain at least

\[
 \bigl(
   \operatorname{sha}(\lambda),
   \operatorname{sha}({\cal P}),
   N,
   \text{pair-order version},
   \text{field }\mathbf F_3,
   \text{winner-order version}
 \bigr).
\tag{4.1}
\]

Any change in (4.1), including a retained rank increase which changes
\(\lambda\), invalidates the cursor and prefix accumulator. The next epoch
starts at \(b=0\). This is exactly why independent workers may parallelize
one correlation but may not independently add retained columns or update the
dual.

### Corollary 4.1 (SERIAL ADAPTIVITY, PARALLEL CORRELATION)

Replacing only each fixed-dual boundary call by Theorem 2.1 or 3.1 preserves
the entire serial v3 sequence of retained boundary columns and dual epochs,
provided each returned row is subjected to the original rank-increase and
direct-replay gates before the next epoch starts.

#### Proof

Induct on dual epochs. Theorem 2.1/3.1 gives the same boundary answer in the
current epoch. The unchanged serial owner therefore adds the same row (or
proceeds to the same correction oracle), producing the same next rank state
and dual. \(\square\)

## 5. Resource truth

Pair counters must count committed, previously unprocessed global indices,
not worker launches or repeated prefixes. Per-process RSS is not the parent
RSS; a production receipt must state and enforce an aggregate policy, such as
the sum of child peaks plus the parent peak, with uncertainty returning
UNKNOWN_RESOURCE. A wall stop may occur between batches, but a partially
returned batch is discarded and does not move the durable cursor.

These rules distinguish acceleration from a merely concurrent toy example.

    FIXED-DUAL SHARD SUM = SERIAL CORRELATION:  PAPER PROOF
    CURSOR + PREFIX + SUFFIX = SERIAL:          PAPER PROOF
    SERIAL ADAPTIVE DUAL EPOCHS PRESERVED:      PAPER PROOF
    TASK303 KERNEL IMPLEMENTATION:              PENDING AUDIT
    AUTHENTICATED V3 PRODUCTION ADAPTER:         NOT IMPLEMENTED
    A0 COMMON / INDEPENDENT ACCEPTANCE:          0/1
    WITNESS / FAKE / IHARA:                      UNCHANGED

R07_FROZEN_DUAL_BOUNDARY_MAPREDUCE_V254_PAPER_GRADE
