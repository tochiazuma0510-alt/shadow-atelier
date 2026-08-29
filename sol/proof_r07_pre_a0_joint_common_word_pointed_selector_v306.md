# R07 pre-A0 joint common-word / pointed selector (v306)

## 0. Scope

The v220 schedule selects one A0 common word and only afterwards asks whether
its actual pointed row lies in the A5 slice.  V302--v305 remove A0 from the
projected A3 calculation, but v305 still lists an actual A0/task193 row as a
sequential A5 input.

This note proves a stronger finite formulation.  At the first relative
Frattini edge, both the A0 defect and the task193 direct change of a
registered correction are linear in its word-bearing correction class.
The endpoint-zero A5 slice is also a finite linear image.  Hence the A0 and
A5 equations can be solved in one joint membership problem before an
arbitrary A0 word is chosen.  A positive ancestry constructs the A0 word and
the pointed multiplier simultaneously; task193 then independently replays
the constructed word rather than supplying a prior target.

This is a paper theorem and compiler contract.  It does not assert that the
joint target is a member, and it does not supersede the soundness of the
standalone A0 or A5 consumers.  No actual word, multiplier, exact PB
endpoint, compatible lift, fake certificate, or Ihara witness is declared.

## 1. The two linear changes of one correction

Let \(k=\mathbf F_3\).  Retain the registered word-bearing A0 correction
module \(\mathcal A_0\) and the exact raw-defect quotient

\[
 B_0:\mathcal A_0\longrightarrow Z_0,
 \qquad \tau_0=-[T_0]\in Z_0,
\tag{1.1}
\]

from v140.  The two exact exponent coordinates are included in \(Z_0\).
Thus a coefficient \(a\in\mathcal A_0\) realizes an A0 common correction
exactly when

\[
 B_0a=\tau_0.
\tag{1.2}
\]

Its retained ordered word realization is denoted \(c(a)\).  Put

\[
 F(x,y)\twoheadrightarrow\Delta_1\twoheadrightarrow\Delta_0,
 \qquad K=\ker(\Delta_1\to\Delta_0).
\tag{1.3}
\]

Every registered correction factor has trivial \(\Delta_0\)-value, and
\(K\) is elementary abelian at this edge.  Therefore evaluation gives a
linear map

\[
 p:\mathcal A_0\longrightarrow K,
 \qquad p(a)=\rho_1(c(a)).
\tag{1.4}
\]

Let \(g=g_{760}\), and let

\[
 d_1=-\mathscr D_1(g)\in Z_1^{\rm full}
\tag{1.5}
\]

be the fixed noncycle pointed row of v239.  Exact first-Frattini affine
linearization, v168 (4.3), gives a linear direct-change map on the attainable
kernel image

\[
 L_g:p(\mathcal A_0)\longrightarrow Z_1^{\rm full},
 \qquad
 L_g(p(a))=\mathscr D_1(gc(a))-\mathscr D_1(g).
\tag{1.6}
\]

### Lemma 1.1 (WELL-DEFINED FIRST-EDGE CHANGE)

Formula (1.6) is independent of the chosen word-bearing coefficient with a
given value in \(p(\mathcal A_0)\), and it is \(k\)-linear.  The pointed
target belonging to \(a\) is

\[
 \boxed{e_1(a)=d_1-L_gp(a).}
\tag{1.7}
\]

#### Proof

The relative Magnus map identifies the first Frattini kernel with the Fox
one-chain modulo the complete translated presentation-boundary image.  Two
corrections with the same \(\Delta_1\)-value differ by the exact Magnus
kernel, so their direct-change rows differ by a complete boundary and give
the same class in \(Z_1^{\rm full}\).  On the elementary-abelian kernel,
Fox collection is additive modulo that boundary image; this is precisely
the affine change map of v168 (4.3).  Thus (1.6) is well-defined and linear.
Finally v239 equations (2.3) and (3.1) give

\[
 e_1(a)=d_1-
 \bigl(\mathscr D_1(gc(a))-\mathscr D_1(g)\bigr),
\]

which is (1.7).  QED.

The complete-boundary qualification is load-bearing.  Literal Fox rows of
two source representatives need not be byte-equal before passage to
\(Z_1^{\rm full}\).

## 2. The A5 slice is fixed before A0 selection

Assume a positive task359 A3 ancestry and an accepted word-bearing A4 basis.
Use v305 to construct the A4-anchored endpoint base point

\[
 \kappa_0\in I,
 \qquad \Phi(\kappa_0)=\bar\epsilon_1.
\tag{2.1}
\]

These data depend on \(g\), task198, task359 and A4, not on a selected A0
word.  Put

\[
 H=\ker\Phi,
 \qquad S=Hd_1=\{\theta d_1:\theta\in H\}
       \leq Z_1^{\rm full}.
\tag{2.2}
\]

The complete occurrence-level A4 closure of v242/v283 computes a basis
\(h_1,\ldots,h_s\) of \(S\), together with literal coefficients
\(\theta_i\in H\) satisfying

\[
 h_i=\theta_i d_1.
\tag{2.3}
\]

Define the pre-A0 pointed target

\[
 \boxed{r_*=d_1-\kappa_0d_1=(1-\kappa_0)d_1.}
\tag{2.4}
\]

For a prospective correction coefficient \(a\), v238 and (1.7) give

\[
\begin{aligned}
 e_1(a)-\kappa_0d_1
 &=d_1-L_gp(a)-\kappa_0d_1\\
 &=r_*-L_gp(a).
\end{aligned}
\tag{2.5}
\]

### Lemma 2.1 (PRE-A0 A5 CLASS)

The correction \(a\) admits an endpoint-compatible pointed multiplier if
and only if

\[
 \boxed{r_*-L_gp(a)\in S.}
\tag{2.6}
\]

Equivalently, in \(Z_1^{\rm full}/S\), its kernel value satisfies the single
affine equation

\[
 \overline{L_g},p(a)=\overline{r_*}.
\tag{2.7}
\]

#### Proof

Substitute (2.5) into v238 Theorem 3.1.  Quotienting by \(S\) gives (2.7).
QED.

Thus A5 pass/fail is constant on each fibre of the finite linear map
\(\overline{L_g}p\).  It need not be constant on all A0 solutions.

## 3. One joint membership

Let \(k^s\) be the coefficient space of the retained slice basis (2.3), and
define

\[
 \mathcal J:\mathcal A_0\oplus k^s
 \longrightarrow Z_0\oplus Z_1^{\rm full}
\tag{3.1}
\]

by

\[
 \boxed{
 \mathcal J(a,c_1,\ldots,c_s)=
 \left(B_0a,
       L_gp(a)+\sum_{i=1}^sc_ih_i\right).}
\tag{3.2}
\]

### Theorem 3.1 (JOINT A0/A5 SELECTOR)

There exists a registered A0 common correction whose actual first pointed
row admits an endpoint-compatible multiplier if and only if

\[
 \boxed{(\tau_0,r_*)\in\operatorname{im}\mathcal J.}
\tag{3.3}
\]

If a coefficient-bearing MEMBER certificate gives

\[
 (\tau_0,r_*)=
 \mathcal J(a,c_1,\ldots,c_s),
\tag{3.4}
\]

then the retained word \(c(a)\) is an A0 common correction and

\[
 \boxed{
 \theta=\sum_i c_i\theta_i,
 \qquad
 \mu_1=\kappa_0+\theta}
\tag{3.5}
\]

satisfies

\[
 \boxed{
 \mu_1d_1=e_1(a),
 \qquad
 \Phi(\mu_1)=\bar\epsilon_1.}
\tag{3.6}
\]

#### Proof

The first coordinate of (3.4) is (1.2), so v140's coefficient-to-word
theorem constructs the A0 correction \(c(a)\).  The second coordinate says

\[
 r_*=L_gp(a)+\theta d_1.
\tag{3.7}
\]

Using (2.4) and (1.7), rearrangement gives

\[
 \kappa_0d_1+\theta d_1
 =d_1-L_gp(a)=e_1(a),
\tag{3.8}
\]

which is the first equality in (3.6).  Each \(\theta_i\) belongs to \(H\),
so \(\Phi(\theta)=0\); (2.1) proves the second equality.

Conversely, an A0 correction with a pointed multiplier satisfies (1.2) and,
by Lemma 2.1, has an expression
\(r_*-L_gp(a)=\sum_i c_ih_i\).  These two equations give (3.4).  QED.

## 4. Literal A6 output and independent replay

Every object in (3.5) has literal source ancestry:

1. v305 writes \(\kappa_0\) as A4-anchored roof-fibre pairs;
2. every \(\theta_i\) is retained by the A4 joint closure as a sum of
   translated kernel differences; and
3. v140 realizes \(a\) by the ordered product of the selected A0 correction
   factors.

Therefore a positive joint certificate simultaneously emits

\[
 c(a)
 \quad\text{and}\quad
 \widetilde\mu_1=\sum_q b_q(U_q-V_q),
 \qquad \rho_0(U_q)=\rho_0(V_q).
\tag{4.1}
\]

The first object is replayed through the full A0 checker and then the
task193 affine-prefix evaluator.  The latter must independently confirm

\[
 L_gp(a)=\mathscr D_1(gc(a))-\mathscr D_1(g)
\tag{4.2}
\]

and all three rows in (1.7).  Thus task193 remains load-bearing acceptance
evidence, but it is no longer a prerequisite for choosing the A0 word.  The
second object is the direct A6 pair polynomial; it must still pass A7's exact
PB endpoint evaluator.

## 5. Positive-only column generation

Equation (3.3) is compatible with v140's positive-only oracle.  In raw
coordinates, seed the basis with:

1. every retained A0 boundary column \((d,0)\);
2. every finite slice column \((0,h_i)\); and
3. for each visited word-bearing A0 correction column \(a_j\), the joint
   column

   \[
   \bigl(B_0^{\rm raw}a_j,L_gp(a_j)\bigr).
   \tag{5.1}
   \]

At a nonzero joint remainder, the same dual-correlation rule requests a
rank-raising boundary or correction column.  If (3.3) is true and the A0
boundary/correction enumeration is fair, a positive certificate is reached
after finitely many rank increases.  The proof is identical to v140
Theorem 3.1 in the larger finite ambient space.

A resource cap or bounded empty prefix is `UNKNOWN_RESOURCE`.  A separating
dual is a mathematical obstruction to all registered A0 corrections only
after it is proved to annihilate the complete boundary family, all slice
columns, and the complete correction family.  A positive receipt needs only
replay its finite retained ancestry.

The existing standalone A0 search remains useful: a positive word supplies
an immediate candidate column combination and an independent replay case.
It is not necessary to discard or restart that work.

## 6. Production contract

A joint producer/checker must retain and independently replay:

1. the complete task198/A3/A4 authority cone and the v305 anchor;
2. the fixed \(d_1\), the full occurrence closure, the post-\(C\) nullspace,
   all \((h_i,\theta_i)\), and two-way equality of the computed slice;
3. every selected A0 column in both coordinates of (5.1), with its literal
   normal-conjugate word and exact exponent entries;
4. the joint target \((\tau_0,r_*)\), every pivot and dual correlation, and the
   complete coefficient replay (3.4);
5. the literal A0 word, direct all-seven A0 replay, and independent task193
   replay of (4.2);
6. both pointed equalities in (3.6); and
7. the factored roof-fibre polynomial (4.1) for A6.

The checker must not accept a supplied task193 row, A5 Boolean, slice rank,
or endpoint base-point digest in place of reconstruction.  Required
mutations include one A0 coefficient, factor order, exponent coordinate,
first-successor value, affine-change row, slice coefficient, A3 anchor,
pointed sign, and one roof-fibre pair.

## 7. Fixed frontier

```text
A0 DEFECT + FIRST-EDGE DIRECT CHANGE AS JOINT LINEAR MAP: PAPER PROOF
PRE-A0 A5 PASSING VALUES FORM AN AFFINE SUBSPACE:         PAPER PROOF
ONE JOINT MEMBERSHIP SELECTS A0 WORD AND MU1:             PAPER PROOF
POSITIVE ANCESTRY -> A0 WORD + LITERAL A6 PAIRS:          PAPER PROOF
TASK193 AS PRESELECTION INPUT:                            REMOVED
TASK193 AS FINAL INDEPENDENT REPLAY:                      RETAINED
ACTUAL A3 MEMBER / A4 BASIS / JOINT MEMBERSHIP:           NOT COMPUTED
ACTUAL A0 WORD / MU1 / M / EXACT PB ENDPOINTS:            NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:                   NONE
```

`R07_PRE_A0_JOINT_COMMON_WORD_POINTED_SELECTOR_V306_PAPER_GRADE`
