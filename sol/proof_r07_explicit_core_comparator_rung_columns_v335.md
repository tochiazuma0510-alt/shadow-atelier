# R07 explicit core-comparator rung columns (v335)

Author: Sol / 2026-08-29

Status: paper theorem extracting a closed-form pure-dihedral transition
column from the two explicit cores
\(\chi_{07}=[x,y][y,z]^{-1}\) and
\(\chi_{40}=[x,y]^{10}[y,z]^{-1}\).  The comparator itself changes the
R07 dihedral roof and is therefore not an A0 correction.  Its prescribed
powers give one explicit kernel direction at every standard
\(36\cdot3^j\) dihedral refinement, but membership in the full actual
common-word domain and the field-even score pairings remain unproved.
No A0 word, A3 numerator, compatible lift, fake certificate or Ihara witness
is declared.  `verified=false`.

## 1. The exact free-group comparator

Put

\[
 h=[x,y],\qquad k=[y,z],\qquad z=y^{-1}x^{-1},
\tag{1.1}
\]

and, for \(A\in\mathbf Z\), put

\[
 \chi_A=h^Ak^{-1}.
\tag{1.2}
\]

Thus \(\chi_{07}=\chi_1\) and \(\chi_{40}=\chi_{10}\).  Define the
right-hand relative comparator

\[
 n_A=\chi_1^{-1}\chi_A.
\tag{1.3}
\]

### Lemma 1.1 (EXACT COMPARATOR IDENTITY)

In the free group \(F(x,y)\),

\[
 \boxed{
 n_A=\chi_1^{-1}h^{A-1}\chi_1,\qquad
 \chi_A=\chi_1n_A=h^{A-1}\chi_1.}
\tag{1.4}
\]

In particular, with

\[
 n=n_{10}=\chi_{07}^{-1}\chi_{40},
\tag{1.5}
\]

one has

\[
 \boxed{
 n=\chi_{07}^{-1}[x,y]^9\chi_{07},\qquad
 \chi_{40}=\chi_{07}n=[x,y]^9\chi_{07}.}
\tag{1.6}
\]

#### Proof

Using \(\chi_1=h k^{-1}\),

\[
 \chi_1^{-1}\chi_A
 =\chi_1^{-1}h^Ak^{-1}
 =\chi_1^{-1}h^{A-1}(hk^{-1})
 =\chi_1^{-1}h^{A-1}\chi_1.
\]

Multiplication on the left by \(\chi_1\) gives the other two equalities.
\(\square\)

Equation (1.6) is the precise location of the apparent missing
\([x,y]^A[y,z]^B\) family: \(\chi_{40}\) differs from \(\chi_{07}\) by a
conjugated ninth power on the correction side.

For any homomorphism \(\rho:F(x,y)\to G\), (1.4) immediately gives

\[
 \boxed{
 \rho(\chi_A)=\rho(\chi_1)
 \quad\Longleftrightarrow\quad
 \rho(h)^{A-1}=1.}
\tag{1.7}
\]

Thus equality in a small quotient and legality as a correction in the
actual roof are distinct tests.

## 2. Literal evaluation on every standard dihedral rung

Let

\[
 Q_j=36\cdot3^j,\qquad j\ge0,
\tag{2.1}
\]

and let \(D_{Q_j}=\langle r_j,s_j\mid
r_j^{Q_j}=s_j^2=r_js_jr_js_j=1\rangle\), with the standard reductions
\(r_{j+1}\mapsto r_j\), \(s_{j+1}\mapsto s_j\).

The literal dihedral section formula of v5 gives, for the same word
\(\chi_A=h^Ak^{-1}\),

\[
 \psi_{Q_j}(\chi_A)
 =
 \bigl(
 r_j^{\,2(A+1)},
 r_j^{-2(A+1)},
 r_j^{-2(A-1)}
 \bigr).
\tag{2.2}
\]

Indeed \(B=-1\), \(k_{\rm dih}=A-B=A+1\), and
\(t=-(A+B)=1-A\) in the notation of that formula.

Since all three entries in (2.2) are rotations, taking the relative quotient
against \(\chi_1\) gives

\[
 \boxed{
 \psi_{Q_j}(n_A)
 =
 \bigl(
 r_j^{\,2(A-1)},
 r_j^{-2(A-1)},
 r_j^{-2(A-1)}
 \bigr).}
\tag{2.3}
\]

For the R40/R07 comparator,

\[
 \psi_{Q_j}(n)
 =
 \bigl(r_j^{18},r_j^{-18},r_j^{-18}\bigr).
\tag{2.4}
\]

Every component of (2.4) has order

\[
 \frac{Q_j}{\gcd(Q_j,18)}=2\cdot3^j.
\tag{2.5}
\]

At the base \(Q_0=36\), this is the nontrivial order-two vector

\[
 \psi_{36}(n)=(r_0^{18},r_0^{18},r_0^{18})\ne1.
\tag{2.6}
\]

### Corollary 2.1 (CHI40 IS NOT AN R07 ROOF-FIBRE CORRECTION)

\(\chi_{40}\) and \(\chi_{07}\) have different pure-dihedral R07 roof
values.  Equivalently, \(n\notin\ker\psi_{36}\).

This failure occurs before the full \(PSL(2,8)\), \(C_3\), hexagon,
pentagon, charming and onto gates are considered.  Therefore \(n\) cannot
be inserted as an A0 or A4 correction merely because it is an explicit
word.

## 3. A closed-form legal direction at each pure-dihedral refinement

Although \(n\) itself is not roof neutral, its exact powers

\[
 \boxed{
 c_j=n^{\,2\cdot3^j}
 =\chi_{07}^{-1}h^{18\cdot3^j}\chi_{07}}
\tag{3.1}
\]

have the required one-rung behavior.

### Theorem 3.1 (EXPLICIT DIHEDRAL RUNG COLUMN)

For every \(j\ge0\),

\[
 \psi_{Q_j}(c_j)=1
\tag{3.2}
\]

and

\[
 \boxed{
 \psi_{Q_{j+1}}(c_j)=
 \bigl(
 r_{j+1}^{Q_{j+1}/3},
 r_{j+1}^{-Q_{j+1}/3},
 r_{j+1}^{-Q_{j+1}/3}
 \bigr),}
\tag{3.3}
\]

whose three coordinates have order three.  Moreover,

\[
 \boxed{c_{j+1}=c_j^3.}
\tag{3.4}
\]

#### Proof

Raise (2.4) to \(2\cdot3^j\).  At level \(j\), the exponent is

\[
 18(2\cdot3^j)=36\cdot3^j=Q_j,
\]

which proves (3.2).  At level \(j+1\), the same exponent is
\(Q_{j+1}/3\), proving (3.3).  Equation (3.4) follows directly from the
definition.  Finally, powers of a conjugate give the second equality in
(3.1).  \(\square\)

The corresponding alternative core is also literal:

\[
 \boxed{
 \chi_{07}c_j
 =h^{1+18\cdot3^j}k^{-1}
 =\chi_{\,1+18\cdot3^j}.}
\tag{3.5}
\]

Thus \(\chi_{40}=\chi_{10}\) is a square root, in the pure-dihedral image
at the first rung, of the first roof-neutral comparator:

\[
 c_0=(\chi_{07}^{-1}\chi_{40})^2,\qquad
 \chi_{07}c_0=\chi_{19}.
\tag{3.6}
\]

This explains both facts at once: \(\chi_{40}\) itself is in the wrong
R07 roof fibre, while its square-relative direction gives a genuine
order-three successor digit in the next standard dihedral refinement.

## 4. Why this does not change the pre-A0 A3 gate

The exponent-nine class-two quotient used by v216/v302 satisfies

\[
 q(h)^9=1.
\tag{4.1}
\]

Therefore (1.6) gives

\[
 q(n)=1,\qquad q(\chi_{40})=q(\chi_{07}),
\tag{4.2}
\]

and every \(c_j\), being a power of \(n\), also has trivial image.
The same holds after each of the eleven frozen occurrence substitutions.
Consequently the H1, H2 and P exponent-nine endpoint changes of the
R40/R07 comparator are all zero.

### Corollary 4.1 (ZERO A3 COLUMN)

Neither \(n\) nor the \(c_j\) can supply a nonzero augmentation column for
the v216 pre-A0 A3 quotient.  In v333 notation, their A3 score-column
evaluation is the zero column.

This is not a contradiction.  The A3 quotient deliberately forgets ninth
powers, while the R07 roof still sees \(n\) by (2.6).  The explicit pair
\((\chi_{07},\chi_{40})\) is therefore a concrete canary showing why
`PROJECTED_AREA_REPRESENTATIVE_ONLY` data must never be promoted to an A0
roof word or an actual successor correction.

## 5. The exact typed test for use in the full lift

Let

\[
 F\xrightarrow{\rho_{j+1}}G_{j+1}
 \xrightarrow{p_j}G_j
\tag{5.1}
\]

be an actual matched refinement, with
\(\rho_j=p_j\rho_{j+1}\), and let \(\mathcal A_j\) be its full legal
common-word correction domain.

### Proposition 5.1 (COMPARATOR TRICHOTOMY)

For any \(A\), exactly one of the following occurs.

1. If \(\rho_j(h)^{A-1}\ne1\), then \(n_A\) changes the old roof and is not
   a legal correction.
2. If \(\rho_j(h)^{A-1}=1\) but
   \(\rho_{j+1}(h)^{A-1}\ne1\), then \(n_A\) is a nonzero transition-kernel
   direction.  It becomes a legal word-bearing column only after the
   independent condition \(n_A\in\mathcal A_j\), including all side gates,
   has been proved.
3. If \(\rho_{j+1}(h)^{A-1}=1\), then \(n_A\) gives the zero column at this
   edge.  It may first become visible at a deeper refinement, but it cannot
   repair the current residual.

#### Proof

By (1.4), \(\rho_i(n_A)\) is conjugate to
\(\rho_i(h)^{A-1}\), so triviality is equivalent at each level.  The three
cases are exhaustive.  Membership in the kernel is necessary but does not
imply the extra defining equations of \(\mathcal A_j\).  \(\square\)

For the standard pure-dihedral tower, Theorem 3.1 places \(c_j\) in case 2
at every rung.  For the full actual R07 ladder this is only a candidate:
the \(PSL(2,8)\), \(C_3\), occurrence, return and side-gate components must
still be replayed.

## 6. Connection to the field-even homotopy and Newton route

Let \(B_j:\mathcal A_j\to L_j\) be the actual common-word Jacobian.  The
closed words \(c_j\) contribute to v333's legal roster only if:

1. \(c_j\in\mathcal A_j\) in the full matched diagram, not merely in its
   dihedral quotient;
2. the literal column \(B_j(c_j)\) is evaluated against the complete
   return-even score basis;
3. those pairings span the named actual cokernel class, or separate the
   whole structural score space; and
4. the columns and their side-gate data reduce naturally between rungs.

If these tests pass, v332 propagates a stable pairing and v334 feeds the
result into the strict/weighted Newton construction.  Theorem 3.1 supplies
the previously missing **closed-form pure-dihedral candidate roster**, but
it does not prove any of the four full-domain conditions above.

In particular, the field-even survivor cannot be declared killed merely
from the formula for \(c_j\): Section 4 shows that the current A3 projected
score system cannot see these columns at all.  A genuinely field-outer/full-
\(P_0\) legal column, or a proved later-depth pairing of the \(c_j\), is still
required.

## 7. Certificate boundary

An actual use of \(c_j\) must record:

1. the exact word (3.1) and its reduction;
2. old-roof identity and nonzero successor image in every marked factor;
3. full H1/H2/P and side-gate evaluation;
4. membership in the authenticated common-word domain;
5. the complete score-column pairing; and
6. reduction to \(c_{j-1}^3\) with occurrence ancestry.

The pure-dihedral identities (1.4), (2.3), and (3.1)--(3.4) are paper
theorems and require no search.  Everything in the full actual list remains
an input to computation or a later proof.

```text
R40/R07 RELATIVE WORD:                    chi07^-1 [x,y]^9 chi07
CHI40 AS R07 ROOF CORRECTION:             NO
EXPLICIT PURE-DIHEDRAL RUNG COLUMN:       c_j=n^(2*3^j)
OLD-RUNG IMAGE / NEXT-RUNG ORDER:         IDENTITY / 3
COMPATIBILITY:                            c_(j+1)=c_j^3
PRE-A0 A3 COLUMN:                        ZERO
FULL ACTUAL CORRECTION-DOMAIN MEMBERSHIP: NOT PROVED
FIELD-EVEN SCORE PAIRING:                 NOT COMPUTED
COMPATIBLE FULL LIFT / FAKE / IHARA:      NOT CONSTRUCTED
```

`R07_EXPLICIT_CORE_COMPARATOR_RUNG_COLUMNS_V335_PAPER_GRADE`

