# R07 full-E4 seven-evaluation orbit selector v110

Author: Sol / 2026-08-27

Status: conditional paper theorem extending v109 from target6 alone to one
common correction for both hexagon defects and the ordered five-coface A.18
pentagon defect in universal mod-three relation modules.  The conditions are
an exact normal-generator roster, typed raw evaluators, and exact
presentation boundaries for every block.  No full stacked calculation has
been run.  Task 171 v1 reported missing raw inputs, but its toy/checker
promotion was rejected by Sol audit and its missing-word claim was refuted by
the full q3 artifact; task 172 is reauditing the remaining executable bridge.
This is not a cofinal lift and not an Ihara witness.

## 1. Why a target6 word is not enough

V109 gives an exact full-\(E_4\) orbit criterion for the first hexagon
component called target6.  Solving that criterion and then choosing unrelated
corrections for the second hexagon and the pentagon would be unsound: all
relations must be evaluated on one source word.

The correct object is therefore the joint residual

\[
 \beta(f)=
 \bigl(H_1(f),H_2(f),P_{A18}(f)\bigr),
\tag{1.1}
\]

where \(H_1,H_2\) are the two printed hexagon defects and
\(P_{A18}\) is the one ordered pentagon product formed from the five printed
A.18 coface values.  The five coface values are retained separately for
direct replay and prefix construction; they are not five independent
equations and may not be commuted.

Thus "seven evaluations" below means the two hexagon relation blocks plus
the five ordered A.18 coface blocks.  Their output equations are the two
hexagons and one pentagon in (1.1).

## 2. General finite relation-evaluator lemma

Let \(F=F(x,y)\), and let \(\psi_1,\ldots,\psi_s\) be the complete finite list
of substitutions occurring in a relation word \(R(f)\).  Constants between
the occurrences are load-bearing in the hexagons.  Thus write the literal
word, without commuting any factors, as

\[
 R(f)=q_0\psi_1(f)^{\varepsilon_1}q_1\cdots
 q_{s-1}\psi_s(f)^{\varepsilon_s}q_s,
 \qquad \varepsilon_i\in\{1,-1\},
\tag{2.1}
\]

where the \(q_i\) are the fixed braid factors, possibly identities, in the
literal printed order.  An inverse factor is differentiated with the Fox
inverse rule; it is not moved to another position.  We use the right
correction convention \(f_0\mapsto f_0c\); changing conventions requires the
v93 transport and is not implicit below.

Fix a base word \(f_0\) whose relation value is already the identity below
the active abelian layer.  Let \(N\triangleleft F\) be a correction subgroup
such that

\[
 \overline{\psi_i(c)}=1
 \quad(c\in N, 1\le i\le s).
\tag{2.2}
\]

The first active-layer change in (2.1) under \(f_0\mapsto f_0c\) has the form

\[
 \boxed{
 [R(f_0c)]-[R(f_0)]=\Sigma_R(c):=
 \sum_{i=1}^s L_i\nabla\psi_i(c),
 }
\tag{2.3}
\]

where each \(L_i\) is the fixed signed prefix transport determined by
\(f_0\), the factors preceding slot \(i\), and the inverse convention.

### Lemma 2.1 (RELATION-BLOCK ADDITIVITY)

\[
 \boxed{\Sigma_R:N\longrightarrow M_R}
\tag{2.4}
\]

is a homomorphism to the additive active-layer module \(M_R\).

#### Proof

For every slot, the Fox identity gives

\[
 \nabla\psi_i(cd)=\nabla\psi_i(c)
 +\overline{\psi_i(c)}\nabla\psi_i(d).
\tag{2.5}
\]

Condition (2.2) makes the middle value one.  Multiplication by each fixed
prefix \(L_i\) and summation preserve additivity.  The same proof covers an
inverse slot because its sign and prefix have already been included in
(2.3). \(\square\)

For \(u\in F\) and \(r\in N\), the cancellation used in v109 gives slotwise

\[
 \nabla\psi_i(uru^{-1})
 =\overline{\psi_i(u)}\nabla\psi_i(r).
\tag{2.6}
\]

Hence \(\Sigma_R(uru^{-1})\) depends only on \(r\) and the finite ordered
context state

\[
 \delta_R(u)=
 (\overline{\psi_1(u)},\ldots,
  \overline{\psi_s(u)}).
\tag{2.7}
\]

## 3. The literal R07 stack

Apply Section 2 simultaneously to

\[
 \mathscr R=\{H_1,H_2,P_{A18}\}.
\tag{3.1}
\]

Use the literal five cofaces in their printed A.18 order.  Equivalently, v47
allows the rho form only after the theta/symmetry component is stacked at the
same time; the direct implementation should use the literal cofaces and avoid
that semantic conversion entirely.

Let \(M_{H_1},M_{H_2},M_P\) be the corresponding full finite relation
modules, and put

\[
 M_{\rm all}=M_{H_1}\oplus M_{H_2}\oplus M_P,
 \qquad
 \Sigma_{\rm all}=
 (\Sigma_{H_1},\Sigma_{H_2},\Sigma_P).
\tag{3.2}
\]

Let \(D_{H_1},D_{H_2},D_P\) be their true presentation-boundary images and

\[
 D_{\rm all}=D_{H_1}\oplus D_{H_2}\oplus D_P.
\tag{3.3}
\]

The PB4 component \(D_P\) is now exact by v108.  Every PB3/PB4 marking and
presentation used in (3.2)--(3.3) must still be bound explicitly by the
integrated receipt.

Let \(N=\ker\Omega\) be the registered task-157ee joint value kernel.  It is
required to be contained in every context kernel needed in (3.1); this is a
typed hypothesis, not a consequence of matching context names.  Let
\(\mathcal R_\Omega\) be an expanded finite task-157ee relation-word roster
in signed \(F_2\) words, and assume the presentation theorem proves

\[
 N=\langle\!\langle\mathcal R_\Omega\rangle\!\rangle_F.
\tag{3.4}
\]

Let \(\Delta_{\rm all}\) be the image of \(F\) in the ordered tuple of all
full context values used in the seven evaluation blocks.  Duplicate
registered contexts may be shared, but no context may be dropped by name
alone.

For \(\delta\in\Delta_{\rm all}\) choose a section word \(u_\delta\), and set

\[
 w_{\delta,r}=u_\delta r u_\delta^{-1},
\qquad
 V_{\delta,r}=
 \bigl(\Sigma_{\rm all}(w_{\delta,r}),
       \epsilon_3(r)\bigr).
\tag{3.5}
\]

### Theorem 3.1 (SEVEN-EVALUATION ORBIT IMAGE)

\[
 \boxed{
 \operatorname{im}
 \bigl((\Sigma_{\rm all},\epsilon_3):N\to
 M_{\rm all}\oplus(\mathbf F_3)^2\bigr)
 =\operatorname{span}_{\mathbf F_3}
 \{V_{\delta,r}\}.}
\tag{3.6}
\]

#### Proof

Every element of \(N\) is a product of conjugates of the finite normal
generators in \(\mathcal R_\Omega\).  Lemma 2.1 makes every relation block
additive on this product.  Formula (2.6) replaces each conjugator by its
finite context state, and exponent sums are additive and invariant under
conjugation.  This proves containment in the right side.  Each displayed
column is the image of its actual word (3.5), proving the reverse
containment. \(\square\)

## 4. One exact universal relation-module solve

Let

\[
 T_{\rm all}=
 (T_{H_1},T_{H_2},T_P)
\tag{4.1}
\]

be the full unprojected defect of the fixed g760-based word in the three
universal mod-three relation modules.  With the sign convention (2.3), the
corrected defect is \(T_{\rm all}+\Sigma_{\rm all}(c)\).

### Theorem 4.1 (ONE-WORD STACKED SELECTOR)

There is a correction \(c\in N\) with exponent sums zero modulo three which
kills both universal hexagon classes and the ordered universal pentagon class
if and only if

\[
 \boxed{
 (-T_{\rm all},0,0)
 \in
 (D_{\rm all}\oplus0\oplus0)
 +\operatorname{span}\{V_{\delta,r}\}.}
\tag{4.2}
\]

Any displayed coefficient solution prints the single correction word

\[
 \boxed{
 c=\prod_{(\delta,r)}
 w_{\delta,r}^{a_{\delta,r}},
 \qquad a_{\delta,r}\in\{0,1,2\}.}
\tag{4.3}
\]

The same word (4.3), not three separately selected words, occurs in all
components.  If an implementation defines \(\Sigma\) as base minus corrected
rather than (2.3), it must reverse this sign and bind that choice by direct
word canaries.

#### Proof

This is Theorem 3.1 modulo the direct-sum boundary space (3.3), with the last
two coordinates constrained to zero.  The materialized product lies in the
normal kernel \(N\); its exponent coordinate is the displayed zero; and
additivity identifies its stacked correction row with the selected column
sum.  Equation (4.2) is then exactly
\(T_{\rm all}+\Sigma_{\rm all}(c)\in D_{\rm all}\). \(\square\)

For an exact presentation \(P=F_d/M\) mapping onto the settled group \(E\),
let \(D_2,D_1\) be the two Fox boundary maps of the corresponding marked
presentation cover.  The covering-chain/Fox sequence identifies

\[
 \ker D_1/\operatorname{im}D_2
 \cong H_1(\ker(P\to E);\mathbf F_3).
\tag{4.4}
\]

Every elementary abelian 3-chief residual above \(E\) factors through
(4.4).  Consequently a zero universal class produced by Theorem 4.1 kills
its specialization at every such marked chief edge.  The converse need not
hold for one chosen quotient: a nonzero universal class may die after
specialization.  Thus a positive result is promotable after the markings are
bound, while a miss is not a global nonexistence theorem.

The algebraic certificate must be followed by direct word replay of both
hexagons, all five coface factors, and their noncommutative pentagon product,
together with the typed map from each raw Fox class to (4.4).  That replay
checks the hypotheses and conventions used to derive the linear system; it
is not optional merely because (4.2) reduced to zero.

## 5. Relation to HT1--HT5

V99 already proves structural affine linearization (HT1-STRUCT), literal
syzygy closedness (HT2-STRUCT), and residual/Jacobian base-change naturality
(HT5-STRUCT) for the actual matched ladder.  V98 supplies compatible ordinary
commutator spelling after compatible correction values have been found.
Those results are not reopened here.

After all typing hypotheses and the specialization map (4.4) are bound,
Theorem 4.1 supplies one explicit common-word value at one universal finite
layer.  It also prevents the earlier error of solving target6 in isolation
and hoping that other components can be corrected later.  It does not prove:

- the class-specific, refinement-compatible actual-image contraction
  \(h_n\) of v99 (5.1)--(5.3), which is the remaining selector content of
  HT3/HT5;
- preservation of every exact commutator, marking, charmingness, onto,
  descent and settlement side gate at every edge (HT4); or
- nonemptiness of every nonabelian-chief accepted set.

Under a compatible quotient of finite windows, context states, Fox rows,
boundary rows and any already materialized word (4.3) reduce to their coarse
counterparts.  Hence a fine accepted correction maps to a coarse accepted
correction.  The converse nonemptiness and a compatible family of correction
values are not consequences of one finite success.

## 6. Implementation order

The safest executable progression is:

1. finish task 169 to obtain the projected coefficient intersection, exact
   joint relation roster and word provenance;
2. authenticate the raw-input bridge which task 171 v1 missed: typed
   full-\(E_4\) operations, the 26 signed record words/expanded roster, and
   raw full-\(E_4\) PB4 rows;
3. run the 100-plus actual conjugation canaries before a large orbit job;
4. run the v109 full-\(E_4\) target6 orbit solver as the first positive
   high-information gate and retain its complete affine solution family;
5. extend the same orbit-column representation to the stack (3.2), adding
   the second hexagon and literal pentagon blocks; and
6. solve (4.2), materialize (4.3), and directly replay all seven evaluation
   blocks and side gates.

If target6 alone is inconsistent in the exact v109 system, the fixed g760
base dies at that lane and the larger stack need not run.  If target6 is
consistent, the larger stack may still be empty; this is precisely why the
whole target6 affine family must be retained.

```text
RELATION-BLOCK ADDITIVITY:                    PAPER_PROOF
SEVEN-EVALUATION ORBIT IMAGE:                 PAPER_PROOF
ONE-WORD STACKED SELECTOR:                    PAPER_PROOF
PB4 PRESENTATION BOUNDARY (v108):             COMPLETE
STRUCTURAL HT1/HT2/HT5 (v99):                 PAPER_PROOF
FULL-E4 PREFLIGHT v1 PROMOTION:               REJECTED BY SOL AUDIT
RAW INPUT BRIDGE / ACTUAL FOX CANARIES:       TASK 172 RUNNING
FULL-E4 TARGET6 SOLVE:                        NOT RUN
FULL STACKED SOLVE / DIRECT SEVEN REPLAY:     NOT RUN
UNIFORM ACTUAL-IMAGE CONTRACTION:             OPEN
ALL-EDGE SIDE GATES / NONABELIAN NONEMPTY:    OPEN
COMPATIBLE COFINAL LIFT:                      NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```
