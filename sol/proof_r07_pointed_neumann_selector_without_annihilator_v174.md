# R07 pointed Neumann selector without an annihilator gate v174

Author: Sol / 2026-08-28

Status: paper theorem.  This note sharpens v173 for the construction of one
compatible correction value.  The annihilator condition in v173 is needed to
extend the construction to a linear homotopy on the whole cyclic defect
module; it is not needed to correct the distinguished actual defect itself.
The actual multiplier required below has not yet been computed.  No R07
lift, fake certificate, or Ihara witness is declared.

## 1. Setup and the pointed distinction

Retain the diagonal context algebra and its relative augmentation ideal from
v173:

\[
 \Xi=\mathbf F_3[[\Delta_\infty]],\qquad
 \mathfrak j=\overline{\langle p-1:p\in P\rangle}.
\tag{1.1}
\]

Let \(A,Z\) be complete continuous left \(\Xi\)-modules and let

\[
 B:A\longrightarrow Z
\tag{1.2}
\]

be continuous and \(\Xi\)-linear.  Let \(\beta\in Z\) be the distinguished
compatible actual defect.  Suppose that one literal word-bearing first
correction supplies \(a\in A\).

V173 constructed a section on the entire cyclic module
\(L=\overline{\Xi\beta}\).  For that stronger assertion the prescription
\(\lambda\beta\mapsto\lambda a\) must be independent of the expression of
\(\lambda\beta\), which is exactly where

\[
 \operatorname{Ann}_\Xi(\beta)a=0
\tag{1.3}
\]

enters.  To correct the one named vector \(\beta\), however, no such section
has to be defined.

## 2. Pointed noncommutative Neumann theorem

### Theorem 2.1 (POINTED NEUMANN SELECTOR)

Assume that there is one explicitly chosen \(\mu\in\mathfrak j\) satisfying

\[
 \boxed{\beta-Ba=\mu\beta.}
\tag{2.1}
\]

Assume also that the closed \(\Xi\)-orbit of \(a\) belongs to the registered
linear correction domain, and that the finite corrections displayed below
pass every separately registered nonlinear word gate.  Then the series

\[
 q_\infty=\sum_{r\geq0}\mu^r a
\tag{2.2}
\]

converges in \(A\) and satisfies

\[
 \boxed{Bq_\infty=\beta.}
\tag{2.3}
\]

Consequently

\[
 \boxed{c_\infty=-q_\infty
 =-\left(1+\mu+\mu^2+\cdots\right)a}
\tag{2.4}
\]

is one compatible correction of the distinguished defect.  At every fixed
finite relative pro-3 quotient, (2.4) is represented by a finite sum.

#### Proof

Because \(\mu\in\mathfrak j\), one has
\(\mu^r a\in\mathfrak j^rA\).  The cofinal nilpotence proved in v173,
Lemma 2.1, implies that these terms vanish at every fixed finite quotient for
all sufficiently large \(r\).  Hence their partial sums define one element of
the inverse limit \(A\).

For \(N\geq1\), put

\[
 q_N=\sum_{r=0}^{N-1}\mu^r a.
\tag{2.5}
\]

Equation (2.1) is equivalent to \(Ba=\beta-\mu\beta\).  Left
\(\Xi\)-linearity gives

\[
\begin{aligned}
 Bq_N
 &=\sum_{r=0}^{N-1}\mu^rBa\\
 &=\sum_{r=0}^{N-1}\mu^r\beta
   -\sum_{r=0}^{N-1}\mu^{r+1}\beta\\
 &=\beta-\mu^N\beta.
\end{aligned}
\tag{2.6}
\]

This is a purely ordered calculation in the possibly noncommutative ring
\(\Xi\); no factor is commuted past another.  The last term tends to zero in
every finite quotient.  Continuity of \(B\) proves (2.3), and changing sign
gives (2.4).  The word-bearing and nonlinear conclusions are exactly the
stated orbit and finite-partial-gate hypotheses. \(\square\)

### Corollary 2.2 (ANNIHILATOR-FREE ACTUAL-CLASS CRITERION)

For the construction of the single value (2.4), neither
\(\operatorname{Ann}_\Xi(\beta)a=0\) nor a well-defined map
\(\overline{\Xi\beta}\to A\) is required.  It is enough to retain one literal
triple

\[
 (\beta,a,\mu)
\tag{2.7}
\]

and directly prove (2.1).  Different admissible choices of \(\mu\) may give
different correction values; uniqueness is neither asserted nor needed.

#### Proof

The proof of Theorem 2.1 only applies the ordered powers of the selected
element \(\mu\) to the selected element \(a\).  It never represents a general
element of \(\overline{\Xi\beta}\), so no quotient-by-annihilator
well-definedness question occurs. \(\square\)

## 3. Finite shadows and the task193 interface

Let \(f^{(0)}=g_{760}\), let \(d\in Z\) denote the signed correction target
for \(f^{(0)}\), let \(a\) be the literal exact correction produced by a
positive task186 run, and let \(f^{(1)}=f^{(0)}a\) in the registered right-
correction convention.  Put

\[
 e=d-Ba.
\tag{3.1}
\]

With task179's target sign, the raw relation defect of \(f^{(1)}\) is
\(-e\).  Task193 is designed to materialize the first genuine successor
shadow of that raw residual as the separately block-tagged rows

\[
 \beta_{1,H1},\quad\beta_{1,H2},\quad\beta_{1,P}.
\tag{3.2}
\]

The next class-specific question is therefore not the full annihilator test
of v173.  In the same second-rung module one must also materialize
\(d_1\), the shadow of the original signed target \(d\).  The smaller
equation is

\[
 \boxed{
 e_1=\mu_1d_1,
 \qquad \mu_1\in\mathfrak j_1,}
\tag{3.3}
\]

or, in the stored task193 raw-defect sign,
\(-\beta_{1,\mathrm{task193}}=\mu_1d_1\).  Both sides use the genuine
diagonal seven-context action.  A positive finite solution of (3.3) is only
the first shadow of (2.1); it does not by
itself prove the completed identity.  Its useful output is a literal finite
combination of common source conjugators.  If that same finite word-algebra
formula can be lifted and proved natural under every matched refinement, it
defines the required \(\mu\in\mathfrak j\), after which Theorem 2.1 closes all
relative pro-3 rungs at once.

Thus the intended post-task193 computation should return one of exactly
three outcomes:

1. a literal \(\mu_1\) with a full coefficient and direct-action replay;
2. a complete dual obstruction to (3.3) in the registered finite universe;
   or
3. `UNKNOWN_RESOURCE`.

It must not replace the diagonal action by one PB3/PB4 component action, and
it must not identify a first-shadow solution with the completed theorem.

## 4. Relation to the relative-dihedral part

The return-odd relative-dihedral formula and Theorem 2.1 may be applied to
their separately typed stable summands.  On the return-even actual class,
Theorem 2.1 shows that a single explicit multiplier identity (2.1) is enough;
there is no additional annihilator census between that identity and the
Neumann series.  Formation purification, prime-to-three refinements, and new
nonabelian perfect-core gates remain separate.

## 5. Fixed frontier

```text
POINTED NONCOMMUTATIVE NEUMANN FORMULA:          PAPER_PROOF
ANNIHILATOR GATE FOR ONE ACTUAL DEFECT VALUE:    REMOVED
ANNIHILATOR GATE FOR A CYCLIC-MODULE HOMOTOPY:   STILL REQUIRED
TASK186 EXACT FIRST CORRECTION a:                GHA IN PROGRESS
TASK193 GENUINE SUCCESSOR RESIDUAL:               IMPLEMENTATION AUDIT
FIRST-SHADOW ACTUAL MULTIPLIER mu_1:              NOT COMPUTED
NATURAL COMPLETED MULTIPLIER mu:                  NOT CONSTRUCTED
RELATIVE PRO-3 COMPATIBLE R07 LIFT:               NOT YET CONSTRUCTED
PRIME-TO-3 / NEW NONABELIAN COFINAL GATES:        OPEN
FAKE / IHARA WITNESS:                             NOT DECLARED
```

`R07_POINTED_NEUMANN_SELECTOR_WITHOUT_ANNIHILATOR_V174_PAPER_GRADE`
