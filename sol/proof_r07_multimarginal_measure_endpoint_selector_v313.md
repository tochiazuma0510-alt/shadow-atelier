# R07 multi-marginal measure endpoint selector (v313)

Author: Sol / 2026-08-29

Status: paper theorem.  V310--v312 reduce universal endpoint repair to one
common lift-kernel coefficient whose seven context images lie in explicit
affine primitive sets.  This note rewrites that intersection as one exact
multi-marginal linear problem.  It also gives the precise measure-theoretic
inverse-limit statement: nonempty finite solution sets at every matched
level have a compatible completed coefficient, even when arbitrary
levelwise choices do not reduce to one another.  It does not prove those
sets nonempty and declares no witness.

## 1. Quotient out the local antidifference ambiguity

Retain v312's exact literal endpoint factorization in every tagged block:

\[
 d_{0,b}=\epsilon_bp_b(1-r_b).
\tag{1.1}
\]

For an actual endpoint target \(\eta_b\) passing the orbit-sum test, let
\(A_b(1-r_b)=\eta_b\) be the deterministic local primitive and let

\[
 K_b=\ker(a\mapsto a(1-r_b)).
\tag{1.2}
\]

The original-coordinate solution set is

\[
 \mathcal P_b=a_b^0+H_b,
 \qquad
 a_b^0=\epsilon_bA_bp_b^{-1},
 \qquad
 H_b=\epsilon_bK_bp_b^{-1}.
\tag{1.3}
\]

Here \(H_b\) is a \(k\)-linear subspace of \(k[G_b]\); it need not be a
submodule for every left action.  Define only the vector-space quotient

\[
 Q_b=k[G_b]/H_b,
 \qquad
 \alpha_b=a_b^0+H_b.
\tag{1.4}
\]

Then a coefficient \(a_b\) solves the local endpoint equation exactly when

\[
 [a_b]=\alpha_b\quad\text{in }Q_b.
\tag{1.5}
\]

## 2. One common-source marginal map

Let \(\Gamma\twoheadrightarrow\Delta_1\) and
\(\rho_b:\Gamma\to G_b\) be the fixed source maps.  Define the \(k\)-linear
map

\[
 \mathcal T:k[\Gamma]\longrightarrow
 k[\Delta_1]\oplus\bigoplus_bQ_b
\tag{2.1}
\]

by

\[
 \mathcal T(\ell)=
 \left(
   \pi_{1,*}(\ell),
   \bigl([\rho_{b,*}(\ell)]\bigr)_b
 \right).
\tag{2.2}
\]

Put

\[
 t_\eta=\left(0,(\alpha_b)_b\right).
\tag{2.3}
\]

### Theorem 2.1 (MULTI-MARGINAL ENDPOINT CRITERION)

Assume every local orbit-sum test passes.  There is a literal finite-support
lift-kernel coefficient \(\ell\) repairing the universal endpoint if and
only if

\[
 \boxed{t_\eta\in\operatorname{im}\mathcal T.}
\tag{2.4}
\]

Every coefficient ancestry for (2.4) is itself the required common-source
coefficient.

#### Proof

The first coordinate of \(\mathcal T(\ell)=t_\eta\) says
\(\pi_{1,*}(\ell)=0\).  By v310 Lemma 2.1 this is exactly
\(\ell\in\mathcal L_1\).  The block-\(b\) coordinate says
\([\rho_{b,*}(\ell)]=\alpha_b\), equivalently
\(\rho_{b,*}(\ell)\in\mathcal P_b\) by (1.3)--(1.5).  V312 Theorem 3.1 says
that these seven conditions for the same \(\ell\) are exactly universal
endpoint repair.  \(\square\)

This formulation is independent of a chosen Schreier basis.  Expanding any
zero \(\Delta_1\)-marginal ancestry fibre by fibre recovers v310's finite
roof-fibre differences, so it remains word-bearing.

## 3. Signed-measure interpretation

Write a candidate as a finite \(k\)-valued signed measure

\[
 \ell=\sum_{j=1}^Nc_j[\gamma_j]in k[\Gamma].
\tag{3.1}
\]

Then (2.4) says simultaneously:

1. its pushforward to the finite first shadow \(\Delta_1\) is zero; and
2. its seven context pushforwards have the prescribed local primitive
   classes \(\alpha_b\).

Thus the field-outer/common-source problem is a multi-marginal coupling
problem over \(k\), not a choice of seven unrelated measures.  A source word
\(\gamma\) supplies one column

\[
 \left([pi_1(\gamma)],
       ([\rho_b(\gamma)])_b\right),
\tag{3.2}
\]

where each context coordinate is then reduced modulo \(H_b\).  Exact sparse
column generation over these common columns is positive-complete: any
finite-support solution uses only finitely many of them.

A bounded failure is not negative because \(\Gamma\) and the quotient
spaces \(Q_b\) may be infinite.  A complete separating dual would have to
prove zero correlation with every common-source column (3.2), not merely a
finite prefix.

## 4. Profinite measure compactness

Now let \((\Gamma_n)_{n\geq1}\) be a matched cofinal system of finite common
source images, with compatible finite context quotients and endpoint data.
At level \(n\), let

\[
 \mathcal T_n:k[\Gamma_n]\longrightarrow W_n,
 \qquad t_n\in W_n
\tag{4.1}
\]

be the finite version of (2.1)--(2.3), including any additional registered
linear side coordinates.  Define the finite affine solution set

\[
 X_n=\{\ell_n\in k[\Gamma_n]:\mathcal T_n(\ell_n)=t_n\}.
\tag{4.2}
\]

Naturality sends a finer solution to a coarser solution, so the reductions
give maps

\[
 X_{n+1}\longrightarrow X_n.
\tag{4.3}
\]

### Theorem 4.1 (FINITE-MARGINAL COMPACTNESS)

If \(X_n\ne\varnothing\) for every \(n\), then

\[
 \boxed{\varprojlim_nX_n\ne\varnothing.}
\tag{4.4}
\]

Consequently there is one compatible completed measure

\[
 \ell_\infty\in\varprojlim_nk[\Gamma_n]
\tag{4.5}
\]

which solves all the finite marginal equations simultaneously.

#### Proof

Each \(X_n\) is finite because \(k\) and \(\Gamma_n\) are finite.  Form the
rooted tree whose level-\(n\) vertices are \(X_n\) and whose edges are the
reduction maps.  Every level is nonempty, and every vertex has finitely many
children.  Choosing any vertex at an arbitrarily deep level supplies a path
to the root, so the tree has vertices at arbitrarily large depth.  Koenig's
lemma gives an infinite path, which is exactly (4.4).  Its coordinates give
(4.5).  \(\square\)

Surjectivity of each map (4.3) is not required.  Compactness selects a branch
through the possibly shrinking finite solution sets.

## 5. What measure compactness does and does not give

The completed algebra

\[
 k[[\Gamma_\infty]]=\varprojlim_nk[\Gamma_n]
\tag{5.1}
\]

is the algebra of compatible \(k\)-valued measures on the profinite common
source image.  Thus (4.5) is a genuine single coefficient, not unrelated
finite choices.  At every finite quotient it has finite support and can be
materialized by literal source words using the retained sections.

If the endpoint maps, word-pair actions and side rows are natural and every
\(X_n\) includes all required linear conditions, \(\ell_\infty\) repairs the
completed endpoint system.  Combined with the pointed Neumann formula, it
can replace a finite universal polynomial as an existence proof on the
relative pro-3 lane.

However Theorem 4.1 does not prove any \(X_n\) nonempty.  In particular:

```text
one finite success                         does not imply all levels;
nonempty at every finite level             implies a compatible measure;
one uniform symbolic right inverse         proves those nonemptiness claims.
```

Nor does compactness automatically preserve automorphism/onto, formation,
settlement or perfect-core gates unless they are included as closed finite
conditions in the tree.  A finite universal polynomial remains the stronger
explicit certificate when v309/v310 finds one.

## 6. Relation to the generalized relative-dihedral plan

The return-odd dihedral formula supplies a symbolic section on its stable
marginal summand.  The return-even actual-class task can now be stated in
either of two equivalent positive forms:

1. find one finite-support measure satisfying (2.4); or
2. prove every finite return-even marginal set \(X_n\) nonempty and apply
   Theorem 4.1.

The first is the explicit-witness route.  The second is the measure-theoretic
uniform route.  Both target the same common-source diagonal constraint; they
do not replace it by seven componentwise solves.

## 7. Fixed frontier

```text
ENDPOINT REPAIR AS ONE MULTI-MARGINAL MEMBERSHIP:  PAPER PROOF
FINITE-SUPPORT COEFFICIENT AS SIGNED MEASURE:      EXACT
ALL FINITE LEVELS NONEMPTY -> COMPATIBLE MEASURE:  PAPER PROOF
ONE FINITE SUCCESS -> ALL LEVELS:                  FALSE / NOT CLAIMED
ACTUAL FINITE MARGINAL TARGETS:                    NOT COMPUTED
ACTUAL FINITE-SUPPORT OR COMPLETED MEASURE:        NOT CONSTRUCTED
NONLINEAR / FORMATION / PERFECT-CORE GATES:        OPEN
COFINAL LIFT / FAKE / IHARA WITNESS:               NONE
```

`R07_MULTIMARGINAL_MEASURE_ENDPOINT_SELECTOR_V313_PAPER_GRADE`
