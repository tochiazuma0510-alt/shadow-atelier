# R07 triangular checkpoint-basis resume theorem v276

Author: Sol / 2026-08-29

Status: sparse specialization of v275 for a checkpoint whose retained-column
ancestries already form an invertible triangular transform.  It removes the
need to materialize a second reverse coefficient matrix.  It does not accept
the current checkpoint, repair A0/v6, or declare a COMMON word.  `verified=false`.

## 1. Ordered rank-raising transcript

Let the authenticated retained raw rows be

\[
 C=(c_1,\ldots,c_r)
\tag{1.1}
\]

in their exact insertion order.  Suppose the checkpoint records coefficient
maps \(a_{ji}\in\mathbf F_3\) and proposed pivot rows

\[
 p_j=\sum_{i=1}^{j}a_{ji}c_i
 \qquad(1\le j\le r),
\tag{1.2}
\]

with

\[
 a_{jj}\ne0.
\tag{1.3}
\]

Thus the coefficient matrix A is lower triangular with nonzero diagonal.
Every equality (1.2) is replayed from immutable sparse rows; neither the
stored pivot row nor its digest is trusted by itself.

Also require registered pivot keys \(q_1,\ldots,q_r\) such that the computed
rows \(p_j\) have coefficient one at \(q_j\), zero at every earlier pivot,
and no nonzero key preceding \(q_j\) in the registered sparse order.  This is
the exact forward-echelon shape needed for deterministic reduction.

## 2. One-directional triangular certificate is two-way

### Theorem 2.1 (TRIANGULAR RESUME BASIS)

Equations (1.2)--(1.3) imply

\[
 \boxed{
 \operatorname{span}(c_1,\ldots,c_r)
 =\operatorname{span}(p_1,\ldots,p_r),
 \qquad \operatorname{rank}C=r.}
\tag{2.1}
\]

#### Proof

Equation (1.2) gives \(P=AC\).  A triangular matrix over a field is
invertible exactly when all diagonal entries are nonzero, so
\(C=A^{-1}P\).  Both span inclusions follow.  The registered distinct pivots
make the p rows independent, hence both spans have dimension r. \(\square\)

Therefore v275's explicit reverse map B is optional when the producer and
checker directly establish the stronger triangular premise.  It is not
optional if any raw row was dependent, an ancestry uses a future row, a
diagonal entry vanishes, or the proposed p rows fail their pivot gates.

## 3. Parallel exact reconstruction

Each equation (1.2) depends only on immutable raw rows and one immutable
ancestry.  Its sparse accumulation can therefore be assigned independently
to a worker interval.  After canonical interval-order collection, the serial
owner validates all pivot conditions and obtains one exact basis P.  There is
no dependency "finish pivot j before beginning the arithmetic for pivot
j+1" in this certificate check.

Let

\[
 N_C=\sum_i|\operatorname{supp}c_i|,
 \qquad N_A=|\{(j,i):a_{ji}\ne0\}|.
\tag{3.1}
\]

The exact work is the measured number of sparse coordinate contributions in
the products \(a_{ji}c_i\), plus canonical collection and pivot checks.  The
number \(r(r-1)/2\) of potential historical pivot tests is not an obligatory
serial loop.  No asymptotic or wall-time improvement is claimed until the
actual ancestry-weighted supports are measured.

A memory-safe implementation streams computed p rows into a bounded ordered
sidecar or the live reducer.  It need not keep r worker copies of C: under a
Linux fork model the immutable decoded raw rows may be shared copy-on-write,
while requests carry only ancestry intervals.  All process/RSS/serialization
costs remain measured owners.

## 4. Positive-only continuation and exact cached parity

For a history-free positive continuation, Theorem 2.1 plus v275 Theorem 3.1
is sufficient.  Reduce the target against P, construct a fresh dual, discard
unbound historical oracle state, and accept only a final complete raw/word
membership replay.

If an adapter instead claims to resume the exact cached-v3 byte path, it must
also establish that the computed P and its pivot order are exactly those
produced by cached-v3's registered `Echelon.add` convention, and independently
recompute the same target remainder and dual.  Triangular span equality alone
does not prove path identity.  This distinction must be explicit in the
terminal schema.

## 5. Application boundary for the present checkpoint

The current 2,896-column checkpoint appears to retain `pivot_ancestry` data,
but file presence or a count is not the premise of Theorem 2.1.  A future
adapter must establish, from the actual bytes:

1. exactly r raw rows and r ancestry records in one sealed order;
2. canonical F3 coefficients with support only in indices at most j;
3. every diagonal coefficient nonzero;
4. every sparse equality (1.2);
5. the complete pivot conditions; and
6. independent reconstruction with a helper-nonshared association/pivot path.

Failure is `UNKNOWN_INPUT`; a cap is `UNKNOWN_RESOURCE`.  Neither changes the
A0 numerator.

## 6. Negative controls

Mutations must include a future ancestry index, zero diagonal, reordered raw
rows, changed raw sparse coordinate, changed ancestry coefficient, duplicate
pivot, wrong pivot normalization, hidden earlier key, one skipped equation,
and a false cached-v3-parity flag attached only to span equality.

## 7. Fixed frontier

```text
INVERTIBLE TRIANGULAR ANCESTRY => TWO-WAY SPAN: PAPER PROOF
PARALLEL PER-ROW EXACT PIVOT RECONSTRUCTION:    PAPER ALGORITHM
EXPLICIT REVERSE COEFFICIENT MATRIX B:          REMOVED UNDER TRIANGULAR GATE
CURRENT 2,896-ROW TRIANGULAR GATES:             NOT AUDITED / NOT EXECUTED
A0 V6 REPAIR OR V7 IMPLEMENTATION:              NOT YET COMMISSIONED
ACTUAL A0 COMMON + CHECKER:                     0/1
LIFT / FAKE / IHARA:                            NONE
```

`R07_TRIANGULAR_CHECKPOINT_BASIS_RESUME_V276_PAPER_GRADE`
