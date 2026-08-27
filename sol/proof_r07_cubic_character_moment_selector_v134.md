# R07 cubic-character moment selector v134

Author: Sol / 2026-08-27

Status: paper proof and executable design.  This note strengthens v132 for
the actual \(\mathbf F_3\) all-seven module.  A complete negative correlation
test needs one exact Eisenstein-integer moment, not all Boolean-cell counts.
The same lazy multi-coordinate projection oracle is used, but the direct
expansion has only \(\prod_i(1+|T_i|)\) terms.  A positive moment still has to
be materialized by a word-bearing section.  No task177 production run, common
correction, cofinal lift, fake, or Ihara witness is declared.

## 1. Weighted correlation over F3

Use v132's exact merged formula for one normal generator \(r\):

\[
 F(\delta)=K+\sum_{i=1}^s\sum_{t\in T_i}
 c_i(t){\bf1}_{\pi_i(\delta)=t}\in\mathbf F_3,
 \qquad \delta\in\Delta.
\tag{1.1}
\]

Targets in one fixed coordinate are distinct, so at most one summand with
that coordinate is nonzero.  The coefficients \(c_i(t)\) are already merged
in \(\mathbf F_3\); equal-target cancellation must occur before (1.1).

Let

\[
 \mathcal E=\mathbf Z[\omega]
 =\mathbf Z[u]/(u^2+u+1),
 \qquad \omega^3=1,\quad\omega\ne1.
\tag{1.2}
\]

All calculations below use the integral basis \(1,\omega\).  Thus an element
is a pair \((A,B)\) denoting \(A+B\omega\), with exact multiplication

\[
 (A,B)(C,D)=(AC-BD,\ AD+BC-BD).
\tag{1.3}
\]

No floating-point root of unity is used.

## 2. One exact cubic moment

Define

\[
 \boxed{\mathcal M(F)=\sum_{\delta\in\Delta}\omega^{F(\delta)}
 \in\mathcal E.}
\tag{2.1}
\]

Let

\[
 n_j=|\{\delta\in\Delta:F(\delta)=j\}|,
 \qquad j=0,1,2.
\tag{2.2}
\]

Then

\[
 \mathcal M(F)=n_0+n_1\omega+n_2\omega^2
 =(n_0-n_2)+(n_1-n_2)\omega.
\tag{2.3}
\]

### Theorem 2.1 (CUBIC MOMENT ZERO-CORRELATION TEST)

Write \(\mathcal M(F)=A+B\omega\) and \(N=|\Delta|\).  Then

\[
 \boxed{
 F(\delta)=0\text{ for every }\delta\in\Delta
 \quad\Longleftrightarrow\quad
 (A,B)=(N,0).}
\tag{2.4}
\]

Moreover the complete value distribution is recovered by

\[
 \boxed{
 n_2=\frac{N-A-B}{3},\qquad
 n_1=B+n_2,\qquad
 n_0=A+n_2.}
\tag{2.5}
\]

Hence an ACTIVE column exists exactly when \(n_1+n_2>0\).

#### Proof

Equation (2.3) gives \(A=n_0-n_2\), \(B=n_1-n_2\).  Together with
\(N=n_0+n_1+n_2\), these equations give (2.5).  If all values vanish, then
\((A,B)=(N,0)\).  Conversely, if \(A=N\) and \(B=0\), then (2.5) gives

\[
 n_2=(N-N-0)/3=0,\qquad n_1=0,
\]

so every value is zero. \(\square\)

The integrality and nonnegativity of the three numbers in (2.5), and their
sum \(N\), are useful independent receipt checks.  Reducing the moment
modulo three would be unsound: nonzero values could cancel.  The pair
\((A,B)\) must be retained over \(\mathbf Z\).

## 3. Moment expansion by partial projection counts

Extend each \(c_i\) by zero outside \(T_i\).  Disjointness of target fibres
in coordinate \(i\) gives the pointwise identity

\[
 \omega^{c_i(\pi_i(\delta))}
 =1+\sum_{t\in T_i}
 (\omega^{c_i(t)}-1)
 {\bf1}_{\pi_i(\delta)=t}.
\tag{3.1}
\]

Since \(F=K+\sum_i c_i\circ\pi_i\), multiplying (3.1) over the coordinates
and summing over \(\Delta\) gives the following formula.

### Theorem 3.1 (LAZY PROJECTION MOMENT FORMULA)

For \(S\subseteq\{1,\ldots,s\}\) and a target tuple
\(t_S=(t_i)_{i\in S}\), put

\[
 N(t_S)=
 \begin{cases}
 |\ker\pi_S|,&t_S\in D_S=\pi_S(\Delta),\\
 0,&t_S\notin D_S.
 \end{cases}
\tag{3.2}
\]

Then

\[
 \boxed{
 \mathcal M(F)=\omega^K
 \sum_{S\subseteq[s]}
 \sum_{t_S\in\prod_{i\in S}T_i}
 \left(\prod_{i\in S}(\omega^{c_i(t_i)}-1)\right)
 N(t_S).}
\tag{3.3}
\]

The empty term is \(N(\varnothing)=|\Delta|\).  Formula (3.3) has exactly

\[
 \boxed{\prod_{i=1}^s(1+|T_i|)}
\tag{3.4}
\]

raw terms before merging equal partial assignments.

#### Proof

Expand the product of (3.1).  Choosing the constant one in coordinate \(i\)
means \(i\notin S\); choosing one target term means \(i\in S\) and selects
exactly one \(t_i\in T_i\).  The product of indicators is one precisely on
the simultaneous equality fibre \(\pi_S=t_S\), whose order is (3.2).
Multiplication by \(\omega^K\) proves (3.3), and independent choices in each
coordinate give (3.4). \(\square\)

For \(c=0,1,2\), the required exact Eisenstein pairs are

\[
 \omega^0=(1,0),\quad
 \omega=(0,1),\quad
 \omega^2=(-1,-1),
\tag{3.5}
\]

and therefore

\[
 \omega-1=(-1,1),\qquad
 \omega^2-1=(-2,-1).
\tag{3.6}
\]

Thus the whole calculation uses signed integers, multiplication (1.3), and
the v125/v132 membership-and-kernel-order oracle.  No algebraic-number
package is required.

## 4. Why this is smaller than the full cell audit

V132 Theorem 2.1 remains correct and is still useful for a named Boolean
cell.  But proving that every cell has value zero first enumerates patterns
and then applies inclusion-exclusion to every star pattern.  Formula (3.3)
performs the common expansion once and retains all cancellations through the
cubic character.

For the negative branch of column generation, the exact obligations reduce
to:

1. authenticate the merged \(K,T_i,c_i\);
2. answer every \(D_S\) query which actually occurs in (3.3);
3. accumulate \((A,B)\) by exact integer arithmetic;
4. check (2.5); and
5. declare zero correlation only when \((A,B)=(|\Delta|,0)\).

A resource cap before all terms in (3.3) have been accumulated is
`UNKNOWN_RESOURCE`, not a zero moment.

## 5. Word-bearing extraction on the positive branch

The moment proves existence but does not itself print a source word.  There
are two exact successors.

### 5.1 Direct R07 fallback

If \(n_1+n_2>0\), scan the frozen Q0 section order and its matching Gamma
states as in v132 (4.2)--(4.4).  Evaluate the already merged formula (1.1)
on each source pair, and stop at the first value in \(\{1,2\}\).  The global
positive count proves that the complete bounded scan must find one.  The
emitted word is

\[
 u_\delta=u_\gamma u_{s(q)}.
\tag{5.1}
\]

This route stores no \(\Delta\) set.  Its absolute cap remains
\(243\cdot1{,}469{,}664\) source pairs.

### 5.2 Moment-guided self-reduction

For a smaller positive certificate, partition the current finite locus by
one target fibre at a time.  For each child, compute its order and restricted
cubic moment by the same simultaneous-fibre counts.  A child contains an
ACTIVE value exactly when its moment differs from its order.  The complement
child has

\[
 |L_*|=|L|-\sum_{t\in T_i}|L_t|,
 \qquad
 \mathcal M(L_*)=\mathcal M(L)-\sum_{t\in T_i}\mathcal M(L_t),
\tag{5.2}
\]

because the target fibres in one coordinate are disjoint.  Choose the first
ACTIVE child in frozen order and continue.  A subgroup-chain refinement then
ends at one word-bearing singleton, exactly as in v132 Theorem 4.1.

The restricted child moments may be computed by inclusion-exclusion over
the avoidance constraints already chosen on that one path.  This is a
positive-branch self-reduction, not an all-cell negative audit.

## 6. All-seven column generation

Replace the linked-correction correlation step in v132 Theorem 5.1 by
Theorems 2.1 and 3.1.  PB3/PB4 translated boundary families remain separately
typed and use their own exact correlation formulas.

### Corollary 6.1 (MOMENT-EXACT ONE-WORD SELECTOR)

Under the authenticated hypotheses of v132 Theorem 5.1, finite column
generation remains terminating if every linked correction family is tested
by (3.3):

- if its moment differs from \(|\Delta|\), Section 5 returns an actual
  rank-increasing word-bearing column; and
- if every correction and boundary moment is trivial, the current dual is a
  complete separator for the pinned module.

#### Proof

Theorem 2.1 is equivalent to the complete pointwise correlation test used in
v132.  Therefore it returns ACTIVE exactly for the same columns and zero
exactly when the dual annihilates the whole family.  Word-bearing extraction
supplies a genuine column on the positive branch.  Every added column raises
rank in the same finite ambient module, so v132's termination proof applies
unchanged. \(\square\)

## 7. Exact implementation contract

The task177 production implementation should retain, per dual and roster
row:

1. the merged weighted targets and their source Fox occurrences;
2. every requested ordered subset \(S\);
3. each tuple-membership answer, \(|D_S|\), and \(|\ker\pi_S|\);
4. the exact Eisenstein accumulator before and after multiplication by
   \(\omega^K\);
5. \((n_0,n_1,n_2)\) from (2.5); and
6. a source word and direct \(F(\delta)\) replay when active.

The independent checker must rebuild (3.3).  Required semantic mutations
include one weight, one \(\omega^c-1\) pair, one partial-assignment count, one
Eisenstein multiplication, the constant \(K\), and one recovered \(n_j\).

```text
CUBIC MOMENT ZERO TEST:                       PAPER_PROOF
LAZY MULTI-PROJECTION MOMENT FORMULA:          PAPER_PROOF
EXACT F3 VALUE-DISTRIBUTION RECOVERY:          PAPER_PROOF
WORD-BEARING POSITIVE EXTRACTION:              PAPER_PROOF / v132
MOMENT-EXACT COLUMN-GENERATION TERMINATION:    PAPER_PROOF
TASK175 RAW BRIDGE:                            PRODUCTION REPAIR IN PROGRESS
TASK176 EXTENSION CENSUS:                      PRODUCTION REPAIR IN PROGRESS
TASK177 BOUNDED SELFTEST:                      STATIC BUNDLE / NOT EXECUTED
TASK177 MOMENT PRODUCTION ENGINE:              NOT IMPLEMENTED
COMMON ALL-SEVEN CORRECTION WORD:              NOT CONSTRUCTED
COFINAL R07 LIFT / FAKE / IHARA WITNESS:       NOT DECLARED
```
