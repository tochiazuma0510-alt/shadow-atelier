# R07 overlap-score to nonlinear Newton bridge (v334)

Author: Sol / 2026-08-29

Status: paper composition theorem.  A complete Goursat score basis and a
legal column roster can certify the leading all-generator surjectivity needed
by v319.  Together with a strict or weighted free cover and the literal
localization hypotheses, this promotes one finite leading calculation to the
whole nonlinear pro-\(3\) recursion.  A target-specific score repair alone
does not imply this structural conclusion.  The actual R07 leading
identification, legal augmentation columns, strict cover and nonlinear
localization remain unproved.  No compatible full lift, fake certificate or
Ihara witness is declared.  `verified=false`.

## 1. Leading residual identification

Let \(\Lambda\) be complete for a two-sided ideal \(J\), let \(A\) be the
complete module of legal word-bearing corrections, and let \(L\) be the
complete localized residual module.  Retain the common-word Jacobian

\[
 B:A\longrightarrow L
\tag{1.1}
\]

and its leading map

\[
 \bar B:A/JA\longrightarrow L/JL.
\tag{1.2}
\]

Suppose an authenticated finite leading model gives an isomorphism

\[
 \xi:L/JL\mathrel{\mathop{\longrightarrow}^{\sim}}
 Q=\bigoplus_{i=1}^m Q_i
\tag{1.3}
\]

which retains every H1, H2 and printed-order pentagon occurrence and all
localized side-gate coordinates.  Let

\[
 T:k[H]\longrightarrow Q
\tag{1.4}
\]

be the complete quotient-marginal image of the ordinary
relative-dihedral/local ambiguity corrections.  Suppose additional legal
word-bearing corrections \(a_1,\ldots,a_s\in A\) have leading columns

\[
 c_j=\xi(\bar B(\bar a_j))\in Q.
\tag{1.5}
\]

Write \(C(e_j)=c_j\) and \(T_C=[T\ C]\).

The load-bearing identification hypothesis is

\[
 \boxed{\operatorname{im}(\xi\bar B)=\operatorname{im}T_C.}
\tag{1.6}
\]

It requires both containments with literal ancestry.  Equality of dimensions
or agreement on one actual residual is insufficient.

## 2. Score separation is exactly leading surjectivity

Let

\[
 \mathcal I=\ker T^*
\tag{2.1}
\]

be the complete local-score identity space, reconstructed by v330--v331.

### Theorem 2.1 (SCORE-COLUMN LEADING ONTO GATE)

Under (1.3)--(1.6), the following are equivalent:

1. the leading common-word Jacobian \(\bar B\) is onto \(L/JL\);
2. the augmented marginal map \(T_C\) is onto \(Q\);
3. the score-column evaluation

   \[
   \operatorname{ev}_C:\mathcal I\longrightarrow k^s,
   \qquad
   \phi\longmapsto(\phi(c_1),\ldots,\phi(c_s))
   \tag{2.2}
   \]

   is injective.

#### Proof

The isomorphism \(\xi\) and equality (1.6) give the equivalence of (1) and
(2).  V333 Theorem 1.1 gives the equivalence of (2) and (3).  \(\square\)

If no additional columns are used, v331 gives the smaller sufficient and
necessary condition

\[
 \bar B\text{ onto}
 \quad\Longleftrightarrow\quad
 \mathcal P_i=0\quad(2\le i\le m),
\tag{2.3}
\]

provided (1.6) is authenticated with \(C=0\).  V323's return/order criterion
can prove individual \(\mathcal P_i\) vanish when the new cyclic ambiguity is
onto the cumulative overlap.

## 3. Constructing the based leading lift

Assume \(L\) has a finite strict free cover

\[
 q:F=\Lambda^t\twoheadrightarrow L,
\qquad
 q(J^rF)=J^rL.
\tag{3.1}
\]

Choose the basis of \(F\) so the classes
\(\bar q(e_1),\ldots,\bar q(e_t)\) generate \(L/JL\).  If the equivalent
conditions of Theorem 2.1 hold, finite score/primal elimination supplies
legal word-bearing values \(b_j\in A\) with

\[
 B(b_j)-q(e_j)\in JL.
\tag{3.2}
\]

Define

\[
 s_0(e_j)=b_j.
\tag{3.3}
\]

### Theorem 3.1 (SCORE CERTIFICATE PRODUCES THE V319 BASE)

The map \(s_0:F\to A\) is a word-bearing \(\Lambda\)-linear leading lift:

\[
 (Bs_0-q)(F)\subseteq JL.
\tag{3.4}
\]

Consequently v319 constructs

\[
 s=s_0(1+R)^{-1},
\qquad
 Bs=q,
\tag{3.5}
\]

for a retained \(R:F\to JF\).

#### Proof

Equation (3.2) on a basis is exactly (3.4).  Extend the values
\(\Lambda\)-linearly and apply v319 Theorem 1.1, whose strictness hypothesis
is (3.1).  \(\square\)

The primal ancestry is essential.  Inconsistency of the normalized dual
NONMEMBER system proves that preimages exist, but a production certificate
must still recover and replay the \(b_j\).

## 4. Nonlinear all-depth consequence

Assume, in addition, v319's exact literal hypotheses:

1. every reachable H1/H2/P residual remains in the same localized module
   \(L\);
2. the ordered materialization has leading affine law \(B\) at every depth;
3. killing the leading class raises the exact ambient depth by one; and
4. every value of \(s\) has legal common-word materialization preserving all
   side gates.

### Theorem 4.1 (FINITE SCORE GATE TO NONLINEAR PRO-\(3\) COMPLETION)

Under Sections 1--4, any reachable initial residual \(z_0\in L\) has a
compatible Newton correction sequence converging to zero residual.  At each
depth the correction is selected by the same based section (3.5); no new
unrelated marginal solve is required.

#### Proof

Theorem 3.1 supplies exactly the based section assumed by v319 Theorem 3.1.
The four present hypotheses are its nonlinear localization hypotheses.
Apply that theorem.  \(\square\)

If ordinary strictness (3.1) fails but v328's finite weighted roster and
filtration-raising error matrix are available, the same argument uses the
weighted cover instead.  In that route, leading score onto supplies the
word-bearing initial columns, while the weighted identity

\[
 Bs_0-q=qR,\qquad R(F_r)\subseteq F_{r+1}
\tag{4.1}
\]

must still be replayed; it does not follow from an unweighted rank statement.

## 5. Why one actual-class column is not automatically enough

Let \(a\in Q\) be the first named endpoint residual.  V333's
target-specific condition may prove

\[
 a\in\operatorname{im}T+\operatorname{span}\{c_1,\ldots,c_s\}
\tag{5.1}
\]

even when \(\operatorname{ev}_C\) is not injective.  This constructs the
first correction but leaves a nonzero structural cokernel

\[
 \ker T_C^*
 =\mathcal I\cap\ker\operatorname{ev}_C.
\tag{5.2}
\]

A later nonlinear remainder can pair nontrivially with (5.2).  Therefore:

- a **target-specific** legal column closes the named linear endpoint and
  can feed v174's pointed route if the same cyclic/side-gate module is proved
  invariant; but
- a **structural** nonlinear Newton lift requires injectivity of (2.2), or a
  separate proof that every reachable remainder annihilates the residual
  score space (5.2).

### Theorem 5.1 (REACHABLE-CLASS WEAKENING)

Let \(R_{\rm reach}\le Q\) be a proved linear subspace containing the leading
class of every reachable nonlinear remainder.  The augmented columns suffice
on that reachable class if and only if

\[
 \boxed{
 \phi(r)=0
 \quad
 (\phi\in\mathcal I\cap\ker\operatorname{ev}_C,\;
  r\in R_{\rm reach}).}
\tag{5.3}
\]

#### Proof

By v333 Theorem 2.1, one \(r\) lies in the augmented image exactly when every
residual identity in (5.2) annihilates it.  Quantify this equivalence over
\(R_{\rm reach}\).  \(\square\)

Full leading onto is the special case \(R_{\rm reach}=Q\).  The narrow
relative-dihedral/actual-class route seeks a much smaller invariant
\(R_{\rm reach}\), often the cyclic module generated by one explicit defect.
The localized route takes the full nonlinear-stable module.  Equation (5.3)
is the exact bridge between them.

## 6. Refinement and naturality

At consecutive levels, v332 decomposes every new identity into new overlap
score classes.  If all overlap spaces descend, a leading score-column
certificate at one level introduces no new dual obstruction upstairs.
However the literal columns, free cover, \(R\)-matrix and materializations
must also reduce naturally before (3.5) defines one completed section.

If novel overlap scores occur, the previous structural roster remains
sufficient exactly when its upper reductions separate those novel scores.
For a target-specific route, only their pairings with the actual upper
reachable class need vanish.  These are finite v332/v333 tests.

## 7. Exact R07 evidence still needed

An actual application requires:

1. a two-way, occurrence-tagged proof of (1.3) and (1.6);
2. complete Goursat/local-score bases, not a sampled row prefix;
3. literal legal columns and the full score-column pairing matrix;
4. primal preimages for a generator basis of \(L/JL\);
5. a strict retract cover or finite weighted/Rees cover;
6. the based error matrix and transported-prefix perturbation of v320;
7. exact nonlinear localization and side-gate replay; and
8. compatible reduction through the registered cofinal tower.

The pending A0/A3/A4 owners are needed to instantiate the first literal word,
target, kernel basis and maps.  This theorem does not replace those inputs.

```text
COMPLETE SCORE SEPARATION <=> LEADING B ONTO:       PAPER PROOF / IDENTIFICATION HYPOTHESIS
LEADING ONTO + STRICT COVER => BASED SECTION:       PAPER PROOF
BASED SECTION + LOCALIZATION => NONLINEAR PRO-3:    PAPER PROOF
ONE ACTUAL TARGET COLUMN => FULL STRUCTURAL ONTO:   NO
REACHABLE-CLASS WEAKENING:                         EXACT DUAL CRITERION
ACTUAL R07 LEADING IDENTIFICATION / COLUMNS:        NOT COMPUTED
STRICT OR WEIGHTED COVER / NONLINEAR STABILITY:     NOT PROVED
COMPATIBLE FULL LIFT / FAKE / IHARA WITNESS:       NOT CONSTRUCTED
```

`R07_OVERLAP_SCORE_TO_NEWTON_BRIDGE_V334_PAPER_GRADE`
