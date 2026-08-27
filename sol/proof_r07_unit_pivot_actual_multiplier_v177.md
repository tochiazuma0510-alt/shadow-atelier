# R07 unit-pivot actual multiplier v177

Author: Sol / 2026-08-28

Status: paper theorem and post-task193 alternative.  It gives a closed
multiplier formula when one equivariant functional detects the whole actual
defect subsystem.  Such a functional has not yet been constructed for R07.
No compatible lift, fake certificate, or Ihara witness is declared.

## 1. Why a raw Fox coordinate is not enough

Retain the complete diagonal algebra and ideal of v173,

\[
 \Xi=\mathbf F_3[[\Delta_\infty]],\qquad \mathfrak j\triangleleft\Xi.
\tag{1.1}
\]

The residual module is a quotient by the complete presentation-boundary
image.  Therefore projection to one raw Fox coordinate need not descend to
the residual module: a translated PB relator can change that coordinate.
The object used below must be an authenticated continuous
\(\Xi\)-linear map on the boundary quotient itself.  Equivalently, a formula
on raw rows must be proved to annihilate every complete boundary translate.

Let (W\leq Z) be a closed \(\Xi\)-submodule containing the signed original
target (d) and corrected residual (e=d-Ba).  Suppose

\[
 \ell:W\longrightarrow\Xi
\tag{1.2}
\]

is continuous and \(\Xi\)-linear.

## 2. Lifting a roof unit

### Lemma 2.1 (NONCOMMUTATIVE UNIT LIFT)

If \(\delta\in\Xi\) has invertible image in \(\Xi/\mathfrak j\), then
\(\delta\) is a unit in \(\Xi\).  Its inverse is given by ordered convergent
Neumann series.

#### Proof

Choose (v\in\Xi) lifting the inverse of \(\bar\delta\).  There are
(r,s\in\mathfrak j) with

\[
 \delta v=1-r,\qquad v\delta=1-s.
\tag{2.1}
\]

V173 Lemma 2.1 makes the ordered series converge.  Thus

\[
 x=v\sum_{n\geq0}r^n,qquad
 y=\left(\sum_{n\geq0}s^n\right)v
\tag{2.2}
\]

satisfy \(\delta x=1\) and (y\delta=1\), respectively.  Finally
(y=y(\delta x)=(y\delta)x=x), so this common element is the two-sided
inverse.  No factors were commuted. \(\square\)

A particularly easy roof certificate is that \(\bar\delta\) is a nonzero
scalar times one group element; such an element is visibly a unit in the
finite roof group algebra.  A general roof group-algebra element requires a
literal inverse certificate, not merely a nonzero coefficient.

## 3. Unit-pivot theorem

### Theorem 3.1 (ACTUAL-CLASS UNIT PIVOT)

Assume:

1. \(\ell\) is injective on (W);
2. \(\delta=\ell(d)) has invertible roof image; and
3. \(\ell(e)\in\mathfrak j\).

Then the unique scalar carrying (d) to (e) is

\[
 \boxed{\mu=\ell(e)\,\delta^{-1}\in\mathfrak j,}
\tag{3.1}
\]

and one has the completed identity

\[
 \boxed{e=\mu d.}
\tag{3.2}
\]

Consequently, subject to the word-bearing and nonlinear gates of v174, one
compatible correction is

\[
 \boxed{c_\infty=-\sum_{n\geq0}\mu^n a.}
\tag{3.3}
\]

#### Proof

Lemma 2.1 gives \(\delta^{-1}\).  Since \(\mathfrak j\) is a two-sided
ideal, (3.1) belongs to \(\mathfrak j\).  Left linearity and the displayed
order give

\[
 \ell(e-\mu d)=\ell(e)-\mu\ell(d)
 =\ell(e)-\ell(e)\delta^{-1}\delta=0.
\tag{3.4}
\]

Both (e) and \(\mu d) lie in (W).  Injectivity of \(\ell|_W\) proves
(3.2).  V174 Theorem 2.1 then proves (3.3).  If (e=\mu'd) as well, applying
\(\ell\) gives \(\mu'\delta=\ell(e)), hence \(\mu'=\mu\). \(\square\)

### Corollary 3.2 (CYCLIC SUBSYSTEM VERSION)

Suppose only that (e\in\overline{\Xi d}) and that
\(\ell(d)=\delta) is a unit.  Then \(\ell\) is automatically injective on
\(\overline{\Xi d}), because

\[
 \ell(\lambda d)=\lambda\delta=0\Longrightarrow\lambda=0.
\tag{3.5}
\]

Hence (3.1)--(3.3) follow if \(\ell(e)\in\mathfrak j\).

This corollary does not turn ambient membership into cyclic membership.  Its
gain is that, once actual cyclic membership is proved, the multiplier is
forced and no word-polynomial coefficient search remains.

## 4. Certificate contract

The unit-pivot route after task193 has four independent gates.

1. **Boundary descent.**  Give a literal formula for \(\ell\) and prove it
   kills every translate of all two PB3 and eleven PB4 presentation rows in
   the seven tagged contexts.
2. **Diagonal equivariance.**  Prove
   \(\ell(\lambda z)=\lambda\ell(z)\) for the simultaneous context action,
   not for one PB component alone.
3. **Unit and depth.**  Retain a roof inverse of \(\ell(d)\), directly replay
   both products, and prove \(\ell(e)\in\mathfrak j\).
4. **Actual injectivity.**  Prove that the kernel of \(\ell\) on the
   registered actual subsystem (W) is zero, or separately prove
   (e\in\overline{\Xi d}) and use Corollary 3.2.

A finite-stage ordinary dual is not automatically such an \(\ell\): it is
usually only \(\mathbf F_3\)-linear, can depend on the current pivot basis,
and may fail diagonal equivariance.  A single finite injectivity test also
does not prove completed injectivity unless its presentation is stable under
every matched refinement.

For discovery, task193's canonical second-rung module may search for an
equivariant boundary-annihilating functional whose pairing with (d_1) is a
unit at the roof.  A positive finite candidate must then be lifted to the
fixed presentation/completed module.  This route and v175's finite-support
word-polynomial route are complementary: either one supplies the exact
multiplier required by v174.

## 5. Fixed frontier

```text
NONCOMMUTATIVE ROOF-UNIT LIFT:                PAPER_PROOF
ACTUAL-CLASS UNIT-PIVOT FORMULA:              PAPER_PROOF
R07 EQUIVARIANT FUNCTIONAL ell:               NOT FOUND
BOUNDARY DESCENT / ACTUAL INJECTIVITY:         NOT PROVED
TASK193 SECOND-RUNG MODULE:                    FIXTURE BOOTSTRAP
V175 UNIVERSAL WORD-POLYNOMIAL ALTERNATIVE:    SPECIFIED / M NOT FOUND
TASK186 EXACT FIRST CORRECTION:                GHA IN PROGRESS
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED
```

`R07_UNIT_PIVOT_ACTUAL_MULTIPLIER_V177_PAPER_GRADE`
