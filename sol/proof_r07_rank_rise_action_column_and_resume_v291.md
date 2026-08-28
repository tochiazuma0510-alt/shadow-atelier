# R07 rank-rise action column and resume theorem v291

Author: Sol / 2026-08-29

Status: paper-grade sign and checkpoint theorem for the A4-v5 closure.  It
does not accept an implementation, execute A4, produce an ordered kernel
basis, or construct a compatible lift, fake certificate, or Ihara witness.
`verified=false`.

## 1. Mixed reduction convention

Work over \(\mathbf F_3\).  Let \(D=\operatorname{im}\Psi\) be the raw
boundary space and let \(k_1,\ldots,k_t\) be the chronological word-bearing
K rows already accepted.  The mixed echelon reduction of a target \(v\) is
written

\[
 v=\Psi(Q)+\sum_{i=1}^t c_i k_i+r.                 \tag{1.1}
\]

Here \(Q\) is a raw boundary ledger, \(c=(c_i)\) is the K coefficient
vector, and \(r\) is the deterministic remainder.  If \(r\ne0\), let \(p\)
be its selected pivot and put

\[
 s=r_p^{-1}\in\{1,2\},\qquad k_{t+1}=s r.          \tag{1.2}
\]

Since every nonzero scalar in \(\mathbf F_3\) is its own inverse,
\(s^{-1}=s\).

## 2. Complete action column

### Proposition 2.1 (MEMBER AND RANK-RISE COLUMNS)

For a MEMBER terminal \(r=0\), the column of the action on the final K
quotient is \(c\).  For a zero-correlation rank-rise terminal, after
adjoining \(k_{t+1}\), its column is

\[
 \boxed{c+s^{-1}e_{t+1}=c+s e_{t+1}}.              \tag{2.1}
\]

#### Proof

Modulo \(D\), equation (1.1) gives \([v]=\sum c_i[k_i]+[r]\).  In the
MEMBER case \([r]=0\).  In the rank-rise case (1.2) gives
\([r]=s^{-1}[k_{t+1}]\), proving (2.1).  Later K rows have coefficient zero,
so the same sparse column remains valid in the eventual final ordered
basis. \(\square\)

Thus omitting a rank-rise action from the matrix is incorrect.  Conversely,
using coefficient \(1\) for the new row without accounting for \(s\) is
correct only when the pivot was already normalized.

## 3. Simultaneous word and discrepancy recurrence

Assume the target is represented by a roof-trivial word \(W_v\) with

\[
 \rho_1(W_v)=v+\Psi(E_v),
 \qquad
 \rho_1(W_i)=k_i+\Psi(E_i).
\tag{3.1}
\]

Fix the chronological product order on the prior labels and define

\[
 W_{t+1}=\operatorname{red}
 \left( W_v\prod_i W_i^{-c_i}\right)^s,
 \qquad
 E_{t+1}=s\left(E_v+Q-\sum_i c_iE_i\right).
\tag{3.2}
\]

### Proposition 3.1 (SIGNED RECURRENCE)

The new word has trivial roof and satisfies

\[
 \rho_1(W_{t+1})=k_{t+1}+\Psi(E_{t+1}).            \tag{3.3}
\]

#### Proof

All factors in (3.2) have trivial roof, so the affine Fox cocycle is additive
on this product.  Substitute (3.1) and then (1.1):

\[
\begin{aligned}
 \rho_1(W_{t+1})
 &=s\left(v+\Psi(E_v)-\sum_i c_i(k_i+\Psi(E_i))\right)\\
 &=sr+\Psi\left(s(E_v+Q-\sum_i c_iE_i)\right)\\
 &=k_{t+1}+\Psi(E_{t+1}).
\end{aligned}
\]

This also fixes all three signs in the implementation: \(+Q\),
\(-\sum c_iE_i\), and the outer scale \(s\). \(\square\)

An accepted machine item must therefore bind its candidate DAG node,
\(Q,c,s\), prior K nodes, resulting word node, and discrepancy simultaneously.
Checking only its final sparse row cannot certify (3.2).

## 4. Lossless partial action state

Let the signed actor order be

\[
 (x,x^{-1},y,y^{-1})=(1,-1,2,-2).                 \tag{4.1}
\]

After the first \(h\) queue parents have been processed, a lossless action
checkpoint contains exactly \(4h\) chronological action records.  For each
record it retains the parent label, signed actor, query identifier, terminal
kind, the MEMBER data or rank-rise \((Q,c,s)\), and the column given by
Proposition 2.1.  It also retains the partial four-matrix table and the queue
append caused by every rank rise.

### Theorem 4.1 (ACTION-PREFIX RESTORE)

Suppose a restore validator independently reconstructs the chronological B/K
echelons and word/ledger DAG, and then checks:

1. the first \(h\) queue entries name earlier ordered K items;
2. their records occur in the exact order (4.1), four per parent;
3. every record is tied to its query and, for a rank rise, to the unique new
   K insertion and the recurrence (3.2);
4. every stored column is recomputed by Proposition 2.1;
5. the partial matrix, queue, action-event chain, and next cursor equal the
   recomputed objects.

Then the first unprocessed action and every future deterministic A4
transition are the same as in an uninterrupted run.  No completed action
query needs to be executed again.

#### Proof

Induct over the \(4h\) records.  The reconstructed basis and DAG fix the
parent target.  A MEMBER relation fixes its column.  A rank-rise relation,
Propositions 2.1 and 3.1, fixes both the appended K item and its column.
Hence the next basis, queue and matrix prefix agree at every step.  At the
end, the queue cursor and fixed actor order determine the unique next
transition. \(\square\)

A comparison which merely deserializes `actions`, `matrix`, and `queue` and
then repackages the same values is circular and does not meet this theorem.
Likewise, a checkpoint seal detects accidental byte changes but is not a
replacement for the algebraic bindings above.

## 5. Fixed frontier

```text
MEMBER ACTION COLUMN c:                         PAPER PROOF
RANK-RISE ACTION COLUMN c+s^(-1)e_new:          PAPER PROOF
WORD/DISCREPANCY SIGNS (+Q,-c,+s):              PAPER PROOF
NO-PREFIX-REPLAY ACTION RESTORE CRITERION:       PAPER PROOF
A4-v5 IMPLEMENTATION OF THE CRITERION:           IN PROGRESS
ACTUAL A4 ORDERED K BASIS:                       NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                  NONE
```

`R07_RANK_RISE_ACTION_COLUMN_AND_RESUME_PAPER_GRADE`
