# R07 authenticated frozen-boundary adapter state and local provenance v255

Author: Sol / 2026-08-28

Status: paper theorem and production-adapter contract extending v254.  It
does not implement the adapter, execute the actual task192 checkpoint, find a
COMMON word, or change a witness/fake/Ihara milestone.  verified=false.

## 1. The byte-level serial object which must be preserved

For one rank state, let \(D=(d_0,\ldots,d_{q-1})\) be the exact descriptor
list constructed by `BoundaryDescriptorCache`: its order is

\[
 (\mathrm{block},\mathrm{relator\ index},\mathrm{component},h,
   \mathrm{base\ coefficient}).                                      \tag{1.1}
\]

For every typed pair \((B,c)\), let \(S_{B,c}\) be the corresponding dual
support list in the live v3 insertion order.  A descriptor \(d_i\) of type
\((B,c)\) contributes the consecutive pairs

\[
 (d_i,s),\qquad s\in S_{B,c}.                                         \tag{1.2}
\]

Concatenating (1.2) in descriptor order is the **v3 global pair roster**
\(P=(p_0,\ldots,p_{N-1})\).  Thus a production adapter must bind not only the
descriptor digest and dual digest, but also the typed support-list digests,
their order, the descriptor prefix offsets, and \(N\).  Sorting a support
list merely because the field sum is commutative is not byte-level v3 parity.

For \(p=(d,s)\), write

\[
 k(p)=(B,r,t),\qquad t=g h^{-1},\qquad
 a(p)=b(d)\lambda(s)\in\mathbf F_3,                                  \tag{1.3}
\]

where \(r\) is the descriptor's relator index.  The winner order is exactly

\[
       (B,t,r),                                                       \tag{1.4}
\]

not the storage order in (1.3).

## 2. Sparse accumulator is sufficient

For a prefix \([0,b)\), put

\[
 A_b(k)=\sum_{i<b,\,k(p_i)=k}a(p_i).                                 \tag{2.1}
\]

Store only the nonzero coordinates of \(A_b\), in one fixed canonical key
encoding.  Individual contributor lists are not part of the algebraic state.

### Theorem 2.1 (ACCUMULATOR SUFFICIENCY)

The tuple \((b,A_b)\), together with the immutable epoch identity, is enough
to resume the v3 correlation and obtain its exact active-key set and winner.

#### Proof

Theorem 3.1 of v254 gives

\[
 A_N=A_b+\sum_{b\le i<N}a(p_i)[k(p_i)].                              \tag{2.2}
\]

The v3 active set is precisely the nonzero support of \(A_N\), and (1.4)
selects its winner.  Neither operation uses contributor history. \(\square\)

This removes a potentially huge and unnecessary contributor log from every
durable batch checkpoint.

## 3. Local reconstruction of the winning provenance

Let the winning key be \(k_*=(B,r,t)\).  Enumerate only descriptors in the
single typed relator \((B,r)\).  For such a descriptor
\(d=(B,r,c,h,b)\), calculate \(g=t h\) and look up the coefficient of \(g\)
in the exact typed support index \(S_{B,c}\).

### Theorem 3.1 (LOCAL WINNER-PROVENANCE BIJECTION)

The records obtained by the preceding local lookup, emitted in descriptor
order and support-list order, are exactly the v3 `contributing_pairs` records
whose key is \(k_*\).  Their coefficient sum is \(A_N(k_*)\).

#### Proof

For a global pair \((d,s)\), equation (1.3) has key \((B,r,t)\) exactly when
the support element \(g\) satisfies \(t=g h^{-1}\), equivalently
\(g=t h\).  Hence every v3 record for \(k_*\) is found by the local lookup.
Conversely, every local match satisfies \(t h=g\), so (1.3) sends it to
\(k_*\).  These maps preserve the descriptor-then-support order fixed in
(1.2), and are inverse.  Summing the matched coefficients is the definition
of \(A_N(k_*)\). \(\square\)

Consequently the adapter may discard all losing contributor lists.  It still
must build the translated boundary row directly and require

\[
  \langle\lambda,\mathrm{row}(B,r,t)\rangle
  =A_N(k_*)\ne0.                                                      \tag{3.1}
\]

## 4. Durable epoch state

A durable boundary record has the following logical fields (the eventual
implementation may choose canonical JSON plus authenticated sidecars):

1. `epoch_identity`: input, target, normalized-semantics, basis rank, pivot
   rows, dual, descriptor roster, typed support rosters, descriptor-prefix
   offsets, global pair count, pair-order version, F3 encoding, winner-order
   version, and all executable pins;
2. `committed_cursor=b`, constrained to a deterministic completed-batch
   boundary;
3. the canonical nonzero sparse `prefix_accumulator=A_b`;
4. completed batch intervals and their exact cover/digests;
5. separate historical, committed-this-epoch, launched, retried, and discarded
   pair counters;
6. parent and child resource accounting, including uncertainty; and
7. a seal covering the checkpoint and every referenced sidecar digest.

The rank-zero checkpoint firewall must reconstruct the basis and dual first.
Only then may it compare the complete epoch identity.  Any mismatch resets
the boundary epoch to \((b,A_b)=(0,0)\).  In particular, the current task192
checkpoint has no usable boundary prefix: `restart_pair_cursor=0` and no
prefix accumulator.  Its 3,145,088 attempted pairs remain historical resource
evidence, not committed algebraic state.

## 5. Atomic batch transition

For a proposed batch \([b,b')\), workers return a disjoint exact cover and
partial accumulators.  The serial owner performs, in order:

1. worker completion and aggregate-resource checks;
2. interval, descriptor/support/epoch digest checks;
3. independent recomputation of every shard partial or an independently
   replayable equivalent certificate;
4. F3 merge into \(A_b\);
5. canonical reserialization and seal; and only then
6. one atomic replacement by \((b',A_{b'})\).

If any step fails or is uncertain, the durable state remains \((b,A_b)\).
Launched or repeated work may increase diagnostic counters, but it may not
increase `committed_cursor` or `committed_unique_pairs`.

### Theorem 5.1 (CRASH-SAFE PREFIX INVARIANT)

After every committed transition, the durable accumulator is exactly (2.1)
for its durable cursor.  Restarting after any number of failed, repeated, or
partially returned batches cannot omit or double-count a global pair.

#### Proof

Induct on commits.  The initial state is the empty sum.  A successful
transition adds an independently checked exact cover of \([b,b')\), so v254
Theorem 2.1 gives (2.1) at \(b'\).  A failed transition changes no durable
state.  Disjoint consecutive committed intervals therefore cover exactly
\([0,b')\). \(\square\)

## 6. Two permitted production modes

The first production adapter may use either of these honest modes:

- **atomic full epoch:** process \([0,N)\) in parallel and commit only the
  final answer.  This needs no mid-boundary cursor and is preferable if the
  task303 kernel finishes one actual epoch inside the wall budget;
- **resumable batches:** use Sections 4--5, with the accumulator inline or in
  authenticated sidecars transported with the checkpoint.

Claiming cursor progress while serial v3 restarts the pair loop is forbidden.
An inline/sidecar checkpoint that exceeds its registered byte cap returns
`UNKNOWN_RESOURCE`; it is not evidence of nonexistence.

## 7. Whole-search simulation

### Theorem 7.1 (ADAPTER-TO-v3 SIMULATION)

Start from the same authenticated columns and rank-zero replay as task192.
Replace only a fixed-dual `BoundaryDescriptorCache.correlation` call by an
accepted adapter completion satisfying Sections 1--6.  Keep candidate-word,
rank-addition, dual update, and correction-oracle ownership serial.  Then the
adapter search has exactly the same sequence of boundary answers, retained
columns, ranks, duals, and eventual terminal as serial v3.

#### Proof

At a fixed dual, Theorems 2.1, 3.1, and v254 Theorem 2.1 give the same
accumulator, winner, row, scalar, and byte-ordered provenance as v3.  The
unchanged owner therefore makes the same next rank decision.  Induction on
rank/dual epochs proves the claim. \(\square\)

An independent positive checker must rebuild the epoch identity and global
roster without importing the producer, replay the completed cover and F3
sum, reconstruct the winner locally by Theorem 3.1, and run the original
direct scalar/rank-increase gates.  SELFTEST parity alone is not an A0 result.

```text
EXACT v3 PAIR/WINNER ORDER:                 PAPER-SPECIFIED
PREFIX SPARSE ACCUMULATOR SUFFICIENCY:      PAPER-PROVED
LOCAL WINNER PROVENANCE RECONSTRUCTION:     PAPER-PROVED
CRASH-SAFE BATCH COMMIT:                    PAPER-PROVED
WHOLE v3 SEARCH SIMULATION:                 PAPER-PROVED
TASK303 KERNEL / PRODUCTION ADAPTER:         PENDING AUDIT / NOT IMPLEMENTED
A0 COMMON + INDEPENDENT ACCEPTANCE:          0/1
WITNESS / FAKE / IHARA:                      UNCHANGED
```

`R07_BOUNDARY_ADAPTER_STATE_LOCAL_PROVENANCE_V255_PAPER_GRADE`

