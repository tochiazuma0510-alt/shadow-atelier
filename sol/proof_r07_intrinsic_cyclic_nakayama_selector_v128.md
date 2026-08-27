# R07 intrinsic cyclic Nakayama selector v128

Author: Sol / 2026-08-27

Status: paper theorem.  It specializes the based lift of v124 to one actual
defect class and allows the leading error to be absorbed partly by a deeper
correction column and partly by a scalar multiple of that class.  Thus the
first all-seven positive solver need not construct a splitter or a full
generator error matrix.  The required intrinsic membership and its two
word-bearing coordinates have not yet been computed.  No cofinal lift, fake,
or Ihara witness is declared.

## 1. The intrinsic one-class module

Let \(\Lambda\) be a ring with a two-sided nilpotent ideal \(I\), let
\(A,Z\) be left \(\Lambda\)-modules, and let

\[
 B:A\longrightarrow Z
\tag{1.1}
\]

be \(\Lambda\)-linear.  In the R07 application, elements of \(A\) carry
actual common correction words and \(B\) is their simultaneous
H1/H2/ordered-pentagon residual.

Fix one desired target \(z\in Z\) and form only the intrinsic cyclic-image
module

\[
 \boxed{M_z=B(A)+\Lambda z\subseteq Z.}
\tag{1.2}
\]

This is smaller data than a free cover of an arbitrarily chosen ambient
residual module.  It is nevertheless the exact module relevant to deciding
whether this one named class lies in \(B(A)\).

For every \(j\geq1\), two-sidedness of \(I\) and linearity of \(B\) give

\[
 \boxed{I^jM_z=B(I^jA)+I^jz.}
\tag{1.3}
\]

Here \(I^jz=\{\rho z:\rho\in I^j\}\); finite sums are already included
because \(I^j\) is an additive subgroup.

## 2. One-class constructive theorem

Assume

\[
 I^L=0.
\tag{2.1}
\]

### Theorem 2.1 (INTRINSIC CYCLIC NAKAYAMA SELECTOR)

The following are equivalent.

1. There is \(a_0\in A\) such that

   \[
   Ba_0\equiv z\pmod {I^jM_z}.
   \tag{2.2}
   \]

2. There are \(a_0\in A\), \(d\in I^jA\), and \(\rho\in I^j\) such that

   \[
   \boxed{Ba_0-z=Bd+\rho z.}
   \tag{2.3}
   \]

Whenever these conditions hold, put

\[
 U=(1+\rho)^{-1}
   =\sum_{m=0}^{\lceil L/j\rceil-1}(-\rho)^m
\tag{2.4}
\]

and

\[
 \boxed{a=U(a_0-d).}
\tag{2.5}
\]

Then

\[
 \boxed{Ba=z.}
\tag{2.6}
\]

Thus a single intrinsic leading membership together with the two
coordinates \((d,\rho)\) constructs an exact preimage of the named class.
No annihilator condition and no right inverse on \(\Lambda z\) are needed.

#### Proof

Equivalence of (2.2) and (2.3) is exactly (1.3).  Equation (2.3) rearranges
to

\[
 B(a_0-d)=(1+\rho)z.
\tag{2.7}
\]

Since \(\rho\in I^j\), one has \(\rho^m\in I^{jm}\); hence the displayed
series (2.4) is finite and is the two-sided inverse of \(1+\rho\).  By
\(\Lambda\)-linearity,

\[
 Ba=B\bigl(U(a_0-d)\bigr)
    =U B(a_0-d)
    =U(1+\rho)z=z.
\]

This proves the theorem. \(\square\)

### Remark 2.2 (why the ambient truncation is insufficient)

A computation of

\[
 Ba_0-z\in I^jZ
\tag{2.8}
\]

does not by itself imply (2.2), because in general

\[
 M_z\cap I^jZ\ne I^jM_z.
\tag{2.9}
\]

The difference is the intrinsic saturation gate.  Therefore an ambient
Jennings quotient can be used as a fatal screen, but a positive receipt must
also return the decomposition (2.3), or equivalently solve inside
\(M_z/I^jM_z\).  This is precisely the information which an ordinary
Boolean `member` omits.

### Remark 2.3 (relation with v124 and v126)

V124 permits a finite free cover and a whole error endomorphism \(R\).
Theorem 2.1 is its one-class, adaptive specialization after the part of the
error lying in \(B(I^jA)\) has first been absorbed into \(d\).  It is also
the fixed-context analogue of the cyclic transition formula in v126.  It
does not define a quotient-module splitter, so the v111 annihilator test is
irrelevant to (2.5).

## 3. Fixed \(\Pi_4[3]\) formula

For the current context

\[
 \Lambda=\mathbf F_3[\Pi_4[3]],\qquad I^{29}=0,
\tag{3.1}
\]

take \(j=9\).  Then \(\rho^4\in I^{36}=0\), and Theorem 2.1 becomes

\[
 \boxed{
 a=(1-\rho+\rho^2-\rho^3)(a_0-d),
 \qquad Ba=z.}
\tag{3.2}
\]

Consequently separate searches at Jennings depths 10, 11, and 12 are not
needed after a receipt has established (2.3) at depth nine.  The four terms
in (3.2) are finite combinations of the same translated, word-bearing
correction columns.

## 4. Exact R07 specialization

Use the frozen correction convention

\[
 \beta+D(c)=0
\tag{4.1}
\]

and set

\[
 z=-\beta,\qquad B=D.
\tag{4.2}
\]

After task175 authenticates the literal all-seven module, the first stacked
solver should work in

\[
 M_z=D(A)+\Lambda z
\tag{4.3}
\]

and return the following lossless certificate:

1. a word-bearing leading coefficient \(a_0\);
2. a word-bearing deeper coefficient \(d\in I^9A\);
3. a group-algebra coefficient \(\rho\in I^9\);
4. direct equality of all coordinates in

   \[
   Da_0-z=Dd+\rho z;
   \tag{4.4}
   \]

5. materialization of (3.2) as one ordinary correction word; and
6. direct replay of that same word in H1, H2, and the printed-order
   pentagon, together with the registered side gates.

If (4.4) is returned, (3.2) closes the entire fixed \(\Pi_4[3]\) radical
for this actual class.  If only ambient membership modulo \(I^9Z\) is
returned, the intrinsic saturation remains `UNKNOWN`; it is not a positive
lift certificate.

## 5. Boundary at a changing context

Theorem 2.1 is deliberately fixed-context.  At a later quotient
\(\Lambda'\twoheadrightarrow\Lambda\), the new transverse error can lie
outside

\[
 B'(J A')+Jz'.
\tag{5.1}
\]

V126 identifies that quotient obstruction and v127 splits it into a finite
graded actual-class ladder.  Thus (3.2) supplies the first exact common word;
it does not assert that every later context edge is cartesian or that every
nonabelian accepted set is nonempty.

```text
INTRINSIC CYCLIC NAKAYAMA SELECTOR:           PAPER_PROOF
DEPTH-9 FOUR-TERM ACTUAL-CLASS FORMULA:        PAPER_PROOF
FULL GENERATOR ERROR MATRIX NEEDED FIRST:      NO
TWO COORDINATES (d,rho) FOR ACTUAL ERROR:      REQUIRED / NOT COMPUTED
AMBIENT-vs-INTRINSIC SATURATION:               REQUIRED / NOT COMPUTED
TASK175 ALL-SEVEN RAW MODULE:                  PENDING EXECUTION
FIXED-CONTEXT COMMON EXPLICIT WORD:            NOT CONSTRUCTED
CONTEXT-CHANGING GRADED SELECTORS:             OPEN (v126--v127)
NONABELIAN ACCEPTED SETS:                      OPEN
COMPATIBLE COFINAL R07 LIFT:                   NOT CONSTRUCTED
FAKE / IHARA WITNESS:                          NOT DECLARED
```
