# R07 roof-abelian screens are canaries v207

Author: Sol / 2026-08-28

Status: paper audit and actual-R07 specialization of v204--v206.  Those
notes prove valid obstruction implications for a general residual, but the
authenticated R07 residual after a positive roof correction reduces to zero
in the roof Fox cokernel.  Every mod-2/mod-3 screen used there factors
through that roof.  Hence both screen values must be zero on the actual
branch.  They are typing/base-change canaries, not new witness gates.  No
task192 positive receipt, compatible lift, fake certificate, or Ihara
witness is declared.

## 1. The corrected residual is roof-zero by construction

Let \(Z^{\rm univ}\) be the complete block-tagged universal Fox cokernel and
let

\[
 Z_0=\mathbf F_3[\Delta_0]
 \otimes Z^{\rm univ}
\tag{1.1}
\]

denote its correctly typed roof base change.  More explicitly, the quotient
by the complete two PB3 and eleven PB4 presentation boundaries is taken
before base change, as required by v183 Lemma 4.3.

Let \(d_0\in Z_0\) be the signed original target.  A positive exact roof
correction \(a_0\) is defined by

\[
 B_0a_0=d_0.
\tag{1.2}
\]

The corrected residual is

\[
 e_0=d_0-B_0a_0.
\tag{1.3}
\]

Thus

\[
 \boxed{e_0=0\quad\text{in }Z_0.}
\tag{1.4}
\]

Task192 is the current exact common-word route to (1.2), and task197/task193
must preserve (1.4) under their schema conversion and genuine-successor
compilation.  Until task192 returns a positive authenticated receipt, (1.4)
is a conditional branch input, not a newly computed result.

## 2. Every roof-factor endpoint screen must vanish

For \(\ell=2,3\), v206 constructs the marked quotient

\[
 \Delta_0\twoheadrightarrow D_\ell\cong(C_\ell)^2.
\tag{2.1}
\]

Let \(Z_\ell\) be the corresponding base change of the full universal Fox
cokernel.  The map

\[
 Z_0\longrightarrow Z_\ell
\tag{2.2}
\]

is well defined by right exactness, and the endpoint map commutes with it.

### Theorem 2.1 (ACTUAL ROOF-ABELIAN RESIDUAL IS ZERO)

Under the positive roof-correction hypothesis (1.2),

\[
 \boxed{
 \bar e_2=0,
 \qquad
 \bar e_3=0.}
\tag{2.3}
\]

Equivalently, v205's fixed endpoint arrays satisfy

\[
 \boxed{
 \bar\epsilon_2=0,
 \qquad
 \bar\epsilon_3=0.}
\tag{2.4}
\]

#### Proof

Apply the base-change map (2.2) to (1.4).  This gives (2.3).  In the chain
model, a zero class in the full cokernel is represented by a complete
presentation boundary, and applying \(D_1\) gives zero.  Naturality of the
literal Fox endpoint under (2.1) identifies this value with (2.4).
\(\square\)

The theorem uses the three combined H1/H2/P blocks.  It does not require the
eleven occurrence summands to vanish separately.

### Corollary 2.2 (NONZERO OUTPUT IS AN IMPLEMENTATION STOP)

If a purported positive task192/task193 branch produces

\[
 \bar\epsilon_2\ne0
 \quad\text{or}\quad
 \bar\epsilon_3\ne0,
\tag{2.5}
\]

then at least one of the following bindings is wrong:

1. the task192 roof correction identity;
2. the task197/task193 lossless adapter;
3. the ten-coordinate/seven-block occurrence map;
4. a sign, inverse slot, prefix, or printed-order combination;
5. the full-cokernel-before-base-change convention; or
6. the PB abelian exponent evaluator.

It is not a mathematical obstruction to a correctly authenticated R07
branch, because it contradicts a defining antecedent of that branch.

## 3. Scope correction to v204--v206

The abstract implications in v204--v206 remain true:

\[
 \text{nonzero roof-factor screen}
 \Longrightarrow
 \text{no relative multiplier visible to that screen}.
\tag{3.1}
\]

For the actual post-roof-correction R07 input, Theorem 2.1 proves that the
antecedent of (3.1) is false.  Therefore the following earlier production
expectation is superseded:

> run mod-2/mod-3 and perhaps stop the expensive pointed successor solve.

The corrected use is:

1. compute the two arrays cheaply while replaying task193;
2. require both to be zero as destructive base-change controls; and
3. regardless of their expected zero values, continue to the first
   successor and the exact PB endpoint unless another independent gate
   stops the branch.

Thus v204's fibre invariance and v206's completed-ideal annihilation are
consistency theorems on this branch.  They do not decide the actual
return-even survivor.

## 4. What a nonvacuous finite screen must detect

Let

\[
 H_1\le H_0\le F
\tag{4.1}
\]

be the first-successor and roof kernels.  A quotient that factors through
\(F/H_0=\Delta_0\) kills both the already corrected residual class and every
relative direction visible only below the roof.  To test the actual
same-\(\mu_1\) endpoint repair nontrivially, a finite endpoint quotient must:

1. retain a nonzero image of the exact PB residual after its roof boundary
   has been forgotten;
2. distinguish at least some values of \(H_0/H_1\) or a finer PB-kernel
   direction; and
3. preserve the eleven typed occurrence maps and combined endpoints.

The first genuine diagonal successor, a finer authenticated relative
quotient, or the exact Artin/Garside PB endpoint can satisfy this role.  The
ordinary mod-2/mod-3 PB abelianizations cannot, because they already factor
through \(\Delta_0\) by the \(18\mathbf Z^2\) lattice theorem.

This identifies the next mathematical target without reviving an infinite
blind orbit: construct a small finite quotient of the exact endpoint groups
whose joint source map does **not** factor through \(\Delta_0\), then apply
v200's complete quotient-dual selector.  A positive quotient result still
requires exact PB replay.

## 5. Frozen corrected frontier

~~~text
v204--v206 ABSTRACT IMPLICATIONS:                  PAPER_PROOF / RETAINED
ACTUAL POSITIVE ROOF RESIDUAL e0:                   ZERO BY DEFINITION
ACTUAL MOD-2/MOD-3 ROOF-FACTOR SCREENS:             FORCED ZERO
NONZERO MOD-2/MOD-3 OUTPUT:                         IMPLEMENTATION STOP
EARLY MATHEMATICAL OBSTRUCTION FROM THESE SCREENS:  VACUOUS ON R07 BRANCH
NON-ROOF-FACTOR FINITE ENDPOINT SCREEN:              NOT CONSTRUCTED
EXACT PB ENDPOINT / SAME-mu1 REPAIR:                 NOT COMPUTED
RELATIVE PRO-3 LIFT / FAKE / IHARA WITNESS:          NOT DECLARED
~~~

R07_ROOF_ABELIAN_SCREENS_ARE_CANARIES_V207_PAPER_AUDIT
