# R07 boundary-quotient bordered echelon theorem v434

Author: Sol / 2026-09-02

Status: exact linear-algebra replacement for the duplicated `boundary` and
`combined=B+K` stores in the v272--v285 A4 oracle.  It is especially adapted
to the present row-27 checkpoint, where the authenticated public counters have
`K_rank=0`.  It proves an equivalent one-large-echelon algorithm and the
lossless migration conditions; it does not authenticate the 1,877 physical
shards, implement the replacement, complete row 27, or declare an A4, lift,
fake, or Ihara result.  `verified=false`.

## 1. Ordered boundary reduction

Let (k=\mathbf F_3), let (V=k^{(\Omega)}), and let

\[
 B=\langle b_1,\ldots,b_m\rangle\subseteq D\subseteq V
\tag{1.1}
\]

be the discovered translated-boundary space.  The rows (b_j) are the
normalized rows stored in chronological pivot order by the existing sparse
echelon.  Each (b_j) has coefficient one at its pivot and coefficient zero
at every earlier pivot.  Later pivots need not be lexicographically larger.

Let

\[
 N_B:V\longrightarrow V
\tag{1.2}
\]

be reduction through (b_1,\ldots,b_m), in that order.  Then (N_B) is
linear,

\[
 \ker N_B=B,\qquad N_B^2=N_B.
\tag{1.3}
\]

Indeed, after one pass all chronological pivot coordinates vanish.  Although
an earlier row may contain a later pivot, it is used before that later pivot
is cleared, and a second pass sees zero at every pivot.  Thus chronological
append-only echelon order supplies a genuine projection without sorting the
pivots.

Retain the raw boundary ledger at the same time:

\[
 N_B(v)=v-\Psi(Q_B(v)),\qquad Q_B(v)\in\mathcal L_D.
\tag{1.4}
\]

This is exactly the subtraction convention of v273 and v285.

## 2. The bordered representation

Let (\kappa_1,\ldots,\kappa_t\in V) be the immutable accepted K rows.  Their
classes are independent in (V/D), by the complete-zero-correlation
certificate used when each row was accepted.  Define their boundary-normal
images

\[
 z_i=N_B(\kappa_i)
     =\kappa_i-\Psi(Q_i),\qquad Q_i=Q_B(\kappa_i).
\tag{2.1}
\]

Build a second, normally small, coefficient-bearing echelon (Z) only from
the ordered rows (z_1,\ldots,z_t).  Its rows remain boundary-normal because
they are linear combinations of the (z_i).  Denote its ordered reduction by
(N_Z).

### Theorem 2.1 (BORDERED MEMBERSHIP EQUIVALENCE)

For every (v\in V),

\[
 \boxed{
 v\in B+\langle\kappa_1,\ldots,\kappa_t\rangle
 \iff
 N_B(v)\in\langle z_1,\ldots,z_t\rangle
 \iff
 N_ZN_B(v)=0.}
\tag{2.2}
\]

Moreover, inserting the rows of (B) first and the rows of (Z) second into
one virtual chronological echelon gives exactly the reduction

\[
 N_{B+K}=N_ZN_B.
\tag{2.3}
\]

#### Proof

If (v=b+\sum_i c_i\kappa_i), apply (N_B) to obtain
(N_B(v)=\sum_i c_i z_i).  Conversely, if
(N_B(v)=\sum_i c_i z_i), then
(N_B(v-\sum_i c_i\kappa_i)=0), so the difference belongs to (B).
This proves (2.2).  Every (Z) row has zero at every B pivot.  Sequential
reduction through the virtual list `B pivots; Z pivots` is therefore first
(N_B) and then (N_Z), proving (2.3).  \(\square\)

The (z_i) are automatically independent in (V/B).  A relation
(\sum_i c_i z_i=0) would put (\sum_i c_i\kappa_i\) in
(B\subseteq D), contradicting independence of the accepted classes in
(V/D).  Hence the small Z echelon always has rank (t).

## 3. Exact coefficient and boundary-ledger replay

Suppose the B reduction of a target returns (Q_v=Q_B(v)).  A normalized Z
pivot (p_\alpha) retains its coefficient vector (C_{\alpha i}) in the raw
(z_i):

\[
 p_\alpha=\sum_i C_{\alpha i}z_i
 =\sum_i C_{\alpha i}\kappa_i
  -\Psi\!\left(\sum_i C_{\alpha i}Q_i\right).
\tag{3.1}
\]

If Z reduction uses coefficients (\mu_\alpha), put

\[
 c_i=\sum_\alpha\mu_\alpha C_{\alpha i},qquad
 Q=Q_v-\sum_i c_iQ_i.
\tag{3.2}
\]

Then its final remainder has the exact v273 external meaning

\[
 \boxed{r=v-\Psi(Q)-\sum_i c_i\kappa_i.}
\tag{3.3}
\]

Thus MEMBER, normalized K-rank-rise, literal-word, and discrepancy recurrences
are unchanged.  Formula (3.2), rather than a mutable numerical pivot label,
is the coefficient bridge to v273 and v285.

## 4. Separating dual without a duplicated B echelon

If (r=N_ZN_B(v)\ne0), choose its registered pivot coordinate and pull the
coordinate functional back through the virtual chronological list.  In
memory this means:

1. back-substitute through the Z pivots in reverse order;
2. back-substitute through the B pivots in reverse order.

By (2.3), the result is exactly the v274 functional

\[
 \lambda(w)=[N_ZN_B(w)]_p,qquad
 \lambda(B+\langle\kappa_i\rangle)=0,quad\lambda(v)\ne0.
\tag{4.1}
\]

The v272 support-inversion correlation is therefore unchanged.  It still
tests this functional on every translate generating the full D, not merely
on the discovered B.  No dense ambient roster and no duplicate numerical
copy of every B row is required.

## 5. A later boundary rise

Suppose support inversion selects (d\in D) with

\[
 \lambda(B+\langle\kappa_i\rangle)=0,qquad\lambda(d)\ne0.
\tag{5.1}
\]

Then (d\notin B+\langle\kappa_i\rangle).  Insert it only into the large B
echelon and put (B'=B+kd).  Recompute

\[
 z_i'=N_{B'}(\kappa_i),\qquad Q_i'=Q_{B'}(\kappa_i),
\tag{5.2}
\]

and deterministically rebuild the small Z echelon from the immutable ordered
K roster.

### Theorem 5.1 (BOUNDARY-GROWTH REBASE)

The rebuilt (z_i') remain independent, Theorem 2.1 continues to hold with
(B'), and every earlier accepted K class and semantic certificate remains
valid.

#### Proof

If (\sum_i c_i z_i'=0), then
(\sum_i c_i\kappa_i\in B'\subseteq D); full-D independence forces every
(c_i=0).  Theorem 2.1 applies verbatim to (B').  Earlier K acceptance
functionals annihilate all of D, so enlarging B inside D cannot invalidate
their independence.  Earlier MEMBER/action records are equations in the raw
grammar (\mathcal L_D\oplus\langle\kappa_i\rangle), not in ephemeral Z
pivot coordinates, and therefore need no change.  \(\square\)

This deterministic rebase costs reductions of the (t) retained K rows when
B grows.  It is zero work while (t=0), and it stores one large boundary
echelon plus a rank-(t) quotient border.  No claim is made here that this is
faster for every possible large (t); its guaranteed gain is elimination of
the second rank-(m) row store.

## 6. Exact K=0 collapse

### Corollary 6.1 (SINGLE-ECHELON K=0 MODE)

If (t=0), then

\[
 B+K=B,qquad N_{B+K}=N_B,
\tag{6.1}
\]

and all membership reductions, separating duals, full-D correlations, and
selected boundary columns are identical to those of the current two-echelon
algorithm.

More strongly, in the current `LiveBasis.add_boundary` chronology the two
stored echelons are entrywise identical.  Assume they agree before inserting
a raw boundary column (d).  Boundary insertion forms the normalized row
(b=sN_B(d)).  The row (b) already has coefficient zero at every old pivot
and coefficient one at its new pivot.  Inserting (b) into the identical
combined store therefore has scale one, empty old-row reduction, the same
pivot, row and label, and formal pair `(boundary_ledger,{})`.  Induction from
the empty stores proves exact equality for every K=0 boundary rise.

Consequently the present implementation's separate objects

```text
boundary rows / combined rows
boundary ledger / combined ledger
B row copy / combined formal with empty K part
```

are views of one mathematical object until the first K row.  They need not be
materialized as independent Python row dictionaries.

## 7. Lossless migration of the row-27 physical chain

The current public state reports K rank zero.  A full migration checker must
first authenticate every physical shard exactly as required by v425.  In
addition, for every chronological entry it must establish:

1. the boundary and combined pivot, normalized row and label are equal;
2. combined insertion scale is one and its old-row reduction is empty;
3. its insertion relation is exactly `{label:1}`;
4. `b_coefficients` and the K part of `b_formals` are empty;
5. `combined_ledger=boundary_ledger` and the stored formal boundary part is
   that same ledger;
6. no K insertion or K roster item occurs anywhere; and
7. ranks, events, epochs, counters, open-query payload and final HEAD bind to
   the same chronological prefix.

Only after these checks may the loader retain one physical B row per entry,
derive the duplicate views, and continue the pending target with the bordered
oracle.  Shard bodies should be streamed and discarded after their seals,
links, raw-identity replay, reductions and entry equalities are checked; the
841-MB ZIP need not be expanded into a simultaneous directory tree.

The API-level and central-directory audit of artifact `9831693721` proves only
an index-consistent candidate.  It does not discharge the seven migration
conditions above.  Hence this theorem does not call that artifact
continuation-ready.

## 8. Resource and claim boundary

At the observed open row, the public physical counters are

```text
query R:27; K rank 0; boundary/combined rank 112355;
1877 shards; accepted/examined 112355/112376.
```

Corollary 6.1 proves that the second rank-112,355 echelon is semantically
redundant.  The bordered representation also allows `b_rows` and the
K-empty combined formals to be label-indexed views rather than copies.  This
removes a structural source of the observed 8-GB pressure, but no numerical
peak-RSS or wall-time factor is asserted before an actual implementation run.

```text
BORDERED B PLUS QUOTIENT-K MEMBERSHIP:        PAPER PROOF
V273 RAW COEFFICIENT / LEDGER REPLAY:          PAPER PROOF
V274 SEPARATING DUAL / FULL-D CORRELATION:     PAPER PROOF
DYNAMIC B-GROWTH K REBASE:                    PAPER PROOF
EXACT K=0 SINGLE-ECHELON COLLAPSE:             PAPER PROOF
ARTIFACT 9831693721 FULL SHARD VALIDATION:     NOT DONE
SINGLE-ECHELON / BORDERED IMPLEMENTATION:      NOT DONE
A4:                                            1/3 THROUGH ROW 26
COMPATIBLE LIFT / FAKE / IHARA:                NONE
```

`R07_BOUNDARY_QUOTIENT_BORDERED_ECHELON_V434_PAPER_GRADE`
