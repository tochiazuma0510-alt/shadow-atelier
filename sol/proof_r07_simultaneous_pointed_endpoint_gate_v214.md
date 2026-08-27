# R07 simultaneous pointed / exponent-power endpoint gate v214

Author: Sol / 2026-08-28

Status: paper theorem strengthening v184, v198, and v212--v213.  At every
matched relative Frattini edge, the matching class-two exponent-power
endpoint factors through the upper finite shadow.  Consequently its value
depends on the finite multiplier itself and not on a chosen source-word
representative.  Over an already selected downstairs multiplier, all
compatible upper multipliers are parametrized by one affine translate of
the relative ideal.  At the first edge, all pointed multipliers and the
exponent-nine endpoint condition can therefore be solved in one finite
joint rank closure.  This removes the logically weaker schedule which first
chooses an arbitrary pointed multiplier and then searches its same-multiplier
fibre.  The actual first-edge rows and endpoints have not yet been produced,
so no compatible lift, fake certificate, or Ihara witness is declared.
`verified=false`.

## 1. The matching endpoint quotient at one Frattini edge

Put \(k=\mathbf F_3\).  For \(m\geq0\), retain one edge of the correctly
typed joint tower

\[
 F=F(x,y)\twoheadrightarrow\Delta_{m+1}
 \twoheadrightarrow\Delta_m,
 \qquad
 K_m=\ker(\Delta_{m+1}\to\Delta_m).
\tag{1.1}
\]

Write

\[
 \mathscr A_{m+1}=k[\Delta_{m+1}],
 \qquad
 I_m=\ker\bigl(\mathscr A_{m+1}\to k[\Delta_m]\bigr).
\tag{1.2}
\]

At a PB3 or PB4 occurrence use the canonical quotient

\[
 Q_{r,m+1}=\mathcal N_r(3^{m+2})
 \qquad(r=3,4).
\tag{1.3}
\]

V213 Theorems 2.1 and 3.1 give, at every one of the eleven literal
occurrences, a factorization

\[
 F\longrightarrow\Delta_{m+1}
 \stackrel{q_{o,m+1}}\longrightarrow Q_{B(o),m+1}.
\tag{1.4}
\]

The joint image is

\[
 D_{m+1}\cong\mathcal H_2(3^{m+2}),
 \qquad |D_{m+1}|=3^{3(m+2)}.
\tag{1.5}
\]

For \(m=0\), (1.3) is exactly the exponent-nine screen and
\(D_1\cong\mathcal H_2(9)\) has order \(729\).

### Lemma 1.1 (MATCHING QUOTIENT KILLS SOURCE-REPRESENTATIVE DIRECTIONS)

Let

\[
 J_{m+1}=\ker\bigl(k[F]\to k[\Delta_{m+1}]\bigr).
\tag{1.6}
\]

For every occurrence \(o\), the induced linear map to
\(k[Q_{B(o),m+1}]\) kills \(J_{m+1}\).  Hence the projected value of a
finite source-algebra element depends only on its image in
\(\mathscr A_{m+1}\).

#### Proof

Equation (1.4) is a group factorization.  Passing to group algebras gives

\[
 k[F]\longrightarrow k[\Delta_{m+1}]
 \longrightarrow k[Q_{B(o),m+1}],
\tag{1.7}
\]

so the first kernel maps to zero. \(\square\)

This is stronger than merely saying that a completed finite orbit contains
no new direction.  There is no projected same-\(\Delta_{m+1}\) direction
to enumerate at all.

## 2. The projected combined endpoint is a function of the multiplier

Retain v198's occurrence data.  For each literal occurrence \(o\), let

\[
 \rho_o:F\to PB_{B(o)},\qquad
 \sigma_o\in\{1,-1\},\qquad
 P_o\in PB_{B(o)},\qquad
 \xi_o\in k[PB_{B(o)}].
\tag{2.1}
\]

Let bars denote projection to (1.3), and put

\[
 p_o=\overline{P_o},\qquad
 \bar\xi_o=\overline{\xi_o}.
\tag{2.2}
\]

Keep all eleven occurrences separately in

\[
 \widehat E_{m+1}
 =\bigoplus_{o=1}^{11}k[Q_{B(o),m+1}].
\tag{2.3}
\]

The repeated E3 value therefore still has two positions, and the E3 and E4
coordinates both labelled `C21` remain different typed coordinates.  Define
the occurrence vector

\[
 w_o=\sigma_op_o\bar\xi_o,
 \qquad w=(w_o)_o\in\widehat E_{m+1}.
\tag{2.4}
\]

There is a left \(\mathscr A_{m+1}\)-action on (2.3) given on group
elements \(g\in\Delta_{m+1}\) by

\[
 (g\odot v)_o
 =p_o q_{o,m+1}(g)p_o^{-1}v_o.
\tag{2.5}
\]

Let

\[
 C:\widehat E_{m+1}\longrightarrow
 E_{m+1}^{\rm blk}
 =k[Q_{3,m+1}]_{H1}\oplus
  k[Q_{3,m+1}]_{H2}\oplus
  k[Q_{4,m+1}]_P
\tag{2.6}
\]

sum the occurrence coordinates inside their printed H1, H2, and P blocks.
This map is only asserted to be \(k\)-linear; the occurrence-dependent
actions must be applied before \(C\).

Let \(\bar\epsilon_{m+1}\in E_{m+1}^{\rm blk}\) be the projected fixed
residual endpoint.

### Theorem 2.1 (SOURCE-INDEPENDENT PROJECTED ENDPOINT)

For \(\mu\in\mathscr A_{m+1}\), choose any finite
\(M\in k[F]\) mapping to \(\mu\).  The projected three-block endpoint is

\[
 \boxed{
 \bar\eta_{m+1}(\mu)
 =\bar\epsilon_{m+1}-C(\mu\odot w).}
\tag{2.7}
\]

It is independent of the choice of \(M\).  In particular, for every
\(N\in J_{m+1}\),

\[
 \boxed{\bar{\mathcal E}_{d,m+1}(N)=0.}
\tag{2.8}
\]

Thus a nonzero value in (2.7) excludes every finite-support source-word
representative of that same multiplier.

#### Proof

For a group element \(g\in\Delta_{m+1}\), equations (2.4)--(2.5) give

\[
 (g\odot w)_o
 =\sigma_op_oq_{o,m+1}(g)\bar\xi_o.
\tag{2.9}
\]

Extend linearly to \(\mathscr A_{m+1}\).  If \(M\) maps to \(\mu\),
Lemma 1.1 identifies the projected occurrence value of \(M\) with
\(q_{o,m+1}(\mu)\).  Substitution in v198 equation (2.2), followed by the
printed block sum \(C\), is exactly (2.7).  Two source lifts differ by
\(J_{m+1}\), which proves independence and (2.8).  If an exact endpoint
were zero, every quotient projection would be zero; hence a nonzero
projected value excludes all such representatives. \(\square\)

For \(m=0\), Theorem 2.1 is the full three-block form of v212's
same-first-successor constancy.  No 729-column repair traversal is present.

## 3. The relative ideal has a small endpoint image

Let

\[
 R_m=q_{m+1}(K_m)
 \leq D_{m+1},
\tag{3.1}
\]

where \(q_{m+1}:\Delta_{m+1}\twoheadrightarrow D_{m+1}\) is the joint map.
V213 Theorem 5.1 identifies \(R_m\) with its one-power-ahead defect group
and gives

\[
 R_m\cong(C_3)^{a_m},\qquad 0\leq a_m\leq3.
\tag{3.2}
\]

Let

\[
 I(R_m)=\ker\bigl(k[D_{m+1}]
 \to k[D_{m+1}/R_m]\bigr).
\tag{3.3}
\]

### Lemma 3.1 (EXACT RELATIVE-IDEAL IMAGE)

The joint group-algebra map sends the complete relative ideal onto

\[
 \boxed{q_{m+1,*}(I_m)=I(R_m).}
\tag{3.4}
\]

Consequently the endpoint part of \(I_m\odot w\) has dimension at most

\[
 \boxed{
 \dim_k I(R_m)
 =|D_{m+1}|-|D_{m+1}/R_m|
 =3^{3(m+2)}\bigl(1-3^{-a_m}\bigr).}
\tag{3.5}
\]

If \(R_m=1\), this endpoint image is zero.

#### Proof

For any group extension, the kernel of the induced group-algebra map is
the ideal generated by \(k-1\) for elements \(k\) of the group kernel.
Thus

\[
 I_m=\mathscr A_{m+1}\langle s-1:s\in K_m\rangle.
\tag{3.6}
\]

The maps \(\Delta_{m+1}\to D_{m+1}\) and
\(K_m\twoheadrightarrow R_m\) are onto.  Applying them to (3.6) gives
the ideal generated by \(r-1\), \(r\in R_m\), which is (3.3).  This proves
(3.4).  The linear map
\(k[D_{m+1}]\to k[D_{m+1}/R_m]\) is onto and the two group-element bases
have the displayed cardinalities, giving (3.5).  Acting on one vector can
only lower dimension. \(\square\)

At the first edge, v211--v212 give

\[
 R_0=\langle[x,y]^3\rangle\cong C_3,\qquad
 |D_1|=729,\qquad |D_1/R_0|=243.
\tag{3.7}
\]

Hence the exponent-nine endpoint adds at most

\[
 \boxed{729-243=486}
\tag{3.8}
\]

linear directions to the pointed closure.  The billion-element PB4
quotient is never materialized as a dense group algebra.

### Corollary 3.2 (EXPLICIT 486-DIRECTION EXPONENT-NINE ROSTER)

Let \(c=[x,y]^3\), so \(R_0=\langle c\rangle\), and choose any retained
transversal \(T\subset D_1\) for \(D_1/R_0\).  Then

\[
 \boxed{
 I(R_0)=
 \bigoplus_{t\in T}
 k\{t(c-1),\ t(c-1)^2\}.}
\tag{3.9}
\]

Thus the endpoint coordinate of the simultaneous first-edge closure has a
fixed complete roster of \(243\cdot2=486\) algebra directions before its
action on \(w\) and subsequent dependencies are collected.

#### Proof

In characteristic three,

\[
 k[R_0]\cong k[T_c]/(T_c^3),\qquad T_c=c-1,
\tag{3.10}
\]

and its augmentation ideal has basis \(T_c,T_c^2\).  The group-element
basis of \(k[D_1]\) decomposes uniquely over the 243 left cosets of
\(R_0\).  Tensoring the two-dimensional augmentation ideal with the chosen
coset basis gives (3.9). \(\square\)

### Corollary 3.3 (POINTED-DATA-FREE PROJECTED PRE-GATE)

Fix a downstairs multiplier
\(\mu_m\in k[\Delta_m]\), choose any lift
\(\widetilde\mu_m\in\mathscr A_{m+1}\), and put

\[
 \bar\epsilon_{m+1}^{\,\widetilde\mu_m}
 =\bar\epsilon_{m+1}
  -C(\widetilde\mu_m\odot w).
\tag{3.11}
\]

Before the pointed rows at the upper shadow are constructed, the existence
of an upper lift of this selected multiplier with zero matching projected
endpoint is already equivalent to

\[
 \boxed{
 \exists\kappa\in I_m:
 \bar\eta_{m+1}(\widetilde\mu_m+\kappa)=0
 \quad\Longleftrightarrow\quad
 \bar\epsilon_{m+1}^{\,\widetilde\mu_m}
 \in C\bigl(I(R_m)\odot w\bigr).}
\tag{3.12}
\]

This criterion is independent of the chosen lift
\(\widetilde\mu_m\).  At the first edge,
\(\mu_0=\widetilde\mu_0=0\), so the right side is one complete membership
test using the 486 algebra directions in (3.9).  A separating dual there
excludes every \(\mu_1\in I_0\), whether or not it later satisfies the
pointed equation.  A positive coefficient is only a projected seed and
must still satisfy the pointed and exact endpoint gates.

#### Proof

Theorem 2.1 makes endpoint zero for
\(\widetilde\mu_m+\kappa\) equivalent to

\[
 C(\kappa\odot w)
 =\bar\epsilon_{m+1}
  -C(\widetilde\mu_m\odot w).
\tag{3.13}
\]

Lemma 3.1 says that the joint images of all \(\kappa\in I_m\) are exactly
\(I(R_m)\).  The action on \(w\) factors through that joint group algebra,
so its complete image is precisely the right side of (3.12).

If the chosen lift is changed to
\(\widetilde\mu_m+\delta\), with \(\delta\in I_m\), then the target in
(3.13) changes by \(-C(\delta\odot w)\), an element of the membership
space.  Hence membership is lift-independent. \(\square\)

## 4. One joint span tests every pointed multiplier

Let \(Z_{m+1}\) be the finite upper-shadow module containing the named rows

\[
 d_{m+1},e^{\rm raw}_{m+1}\in Z_{m+1}.
\tag{4.1}
\]

Retain the selected downstairs multiplier \(\mu_m\) and one lift
\(\widetilde\mu_m\) from Corollary 3.3.  Define the affine residual

\[
 z_{m+1}^{\,\widetilde\mu_m}
 =e^{\rm raw}_{m+1}-\widetilde\mu_m d_{m+1}.
\tag{4.2}
\]

Every upper coefficient lifting \(\mu_m\) has a unique expression

\[
 \mu_{m+1}=\widetilde\mu_m+\kappa,
 \qquad\kappa\in I_m.
\tag{4.3}
\]

Its pointed coefficient equation is therefore

\[
 e^{\rm raw}_{m+1}=\mu_{m+1}d_{m+1}
 \quad\Longleftrightarrow\quad
 z_{m+1}^{\,\widetilde\mu_m}=\kappa d_{m+1}.
\tag{4.4}
\]

Choose word-bearing generators

\[
 K_m=\langle s_1,\ldots,s_t\rangle.
\tag{4.5}
\]

On \(Z_{m+1}\oplus\widehat E_{m+1}\), use the ordinary
\(\mathscr A_{m+1}\)-action on the first coordinate and the twisted action
(2.5) on the second.  Put

\[
 v_i=
 \bigl((s_i-1)d_{m+1},(s_i-1)\odot w\bigr)
\tag{4.6}
\]

and define the finite-dimensional invariant span

\[
 \widehat W_m
 =\mathscr A_{m+1}\langle v_1,\ldots,v_t\rangle.
\tag{4.7}
\]

Finally put

\[
 T(z,v)=(z,C(v)),\qquad W_m=T(\widehat W_m).
\tag{4.8}
\]

### Theorem 4.1 (SIMULTANEOUS POINTED / ENDPOINT CRITERION)

There exists an upper multiplier lifting the selected \(\mu_m\) which
satisfies both the pointed equation and the matching exponent-power endpoint
gate if and only if

\[
 \boxed{
 \exists\kappa\in I_m:
 \begin{cases}
 z_{m+1}^{\,\widetilde\mu_m}=\kappa d_{m+1},\\
 \bar\eta_{m+1}(\widetilde\mu_m+\kappa)=0
 \end{cases}
 \quad\Longleftrightarrow\quad
 \bigl(z_{m+1}^{\,\widetilde\mu_m},
       \bar\epsilon_{m+1}^{\,\widetilde\mu_m}\bigr)
 \in W_m.}
\tag{4.9}
\]

A positive word-bearing ancestry in (4.9) returns one explicit
\(\kappa\), and therefore
\(\mu_{m+1}=\widetilde\mu_m+\kappa\), satisfying both conditions.  A
separating dual for the right-hand membership is an exact obstruction to
every upper pointed multiplier lifting the selected \(\mu_m\), not merely
to one selected same-multiplier source-word fibre.  Membership and
nonmembership are independent of the arbitrary lift
\(\widetilde\mu_m\).

#### Proof

Because the \(s_i\) generate the finite elementary-abelian normal kernel,
the standard group-algebra identities

\[
 ab-1=(a-1)+a(b-1),\qquad
 a^{-1}-1=-a^{-1}(a-1)
\tag{4.10}
\]

give

\[
 I_m=\sum_i\mathscr A_{m+1}(s_i-1).
\tag{4.11}
\]

For
\(\kappa=\sum_i a_i(s_i-1)\), the two coordinates generated from (4.6)
are, in their fixed noncommutative order,

\[
 \sum_i a_i(s_i-1)d_{m+1}=\kappa d_{m+1},
 \qquad
 \sum_i a_i\odot((s_i-1)\odot w)=\kappa\odot w.
\tag{4.12}
\]

Conversely every vector in (4.7) is obtained from a coefficient in (4.11).
Therefore

\[
 W_m=
 \{(\kappa d_{m+1},C(\kappa\odot w)):\kappa\in I_m\}.
\tag{4.13}
\]

Equations (2.7), (3.11), and (4.13) make membership of
\(\bigl(z_{m+1}^{\,\widetilde\mu_m},
\bar\epsilon_{m+1}^{\,\widetilde\mu_m}\bigr)\) exactly the two equations
on the left of (4.9).  Retained linear ancestry reconstructs \(\kappa\).
In finite
dimension, failed membership has a separating dual, and any completed
universal multiplier would satisfy both necessary equations, proving the
obstruction assertion.

If the lift changes by \(\delta\in I_m\), then the target in (4.9) changes
by

\[
 -\bigl(\delta d_{m+1},C(\delta\odot w)\bigr)\in W_m.
\tag{4.14}
\]

Translation by an element of \(W_m\) preserves membership in \(W_m\), and
the corresponding solution changes from \(\kappa\) to
\(\kappa-\delta\).  This proves lift-independence. \(\square\)

The dual in Theorem 4.1 rules out a compatible lift of the selected
downstairs coefficient \(\mu_m\) for the named upper rows
\(d_{m+1},e^{\rm raw}_{m+1}\).  It does not silently quantify over a
different downstairs coefficient, lower correction, or roof branch.

## 5. First-edge executable consequence

At \(m=0\), the downstairs coefficient and its canonical lift are both
zero, so
\(z_1^{\,0}=e_1^{\rm raw}\) and
\(\bar\epsilon_1^{\,0}=\bar\epsilon_1\).  V188 already performs a
word-bearing invariant closure for the same row, which we now abbreviate
by \(e_1=e_1^{\rm raw}\):

\[
 e_1\in I_0(\mathscr A_1d_1+\mathscr A_1e_1).
\tag{5.1}
\]

Theorem 4.1 gives the stronger production schedule:

1. as soon as the fixed residual endpoints exist, run Corollary 3.3's
   complete 486-direction pre-gate, before constructing the successor rows;
2. on a pre-gate pass, retain the word-bearing basis
   \(s_1,\ldots,s_t\) of the actual first
   successor kernel;
3. append the eleven occurrence-tagged exponent-nine endpoint coordinates
   (4.6) to the pointed rows;
4. close rank-raising rows under \(x^{\pm1},y^{\pm1}\), retaining ancestry;
5. test the single target
   \((e_1,\bar\epsilon_1)\) after the printed block map \(C\);
6. on membership, return a pointed \(\mu_1\) whose exponent-nine endpoint
   is already zero, compile its source-word pair by v191, and run v198's
   exact Artin/Garside endpoint replay; and
7. on nonmembership, retain the complete dual as an obstruction to all
   pointed first-edge multipliers for these fixed rows.

The endpoint orbit in this augmented closure has dimension at most 486 by
(3.8).  Queue exhaustion is certified by invariant-span closure, so neither
\(|\Delta_1|\), a 729-column same-fibre traversal, nor the full PB4 quotient
roster is enumerated.

This schedule is strictly stronger than:

\[
 \text{choose one }\mu_1
 \longrightarrow
 \text{test its endpoint}
 \longrightarrow
 \text{vary only }M_0+J_1.
\tag{5.2}
\]

V212 proves that the last variation in (5.2) cannot change the
exponent-nine endpoint.  The joint span instead varies every
\(\mu_1\in I_0\) satisfying the pointed equation before choosing one.

## 6. Uniformity and the remaining gap

All constructions above use the compatible quotients of v213.  Reduction

\[
 \mathcal N_r(3^{m+3})\to\mathcal N_r(3^{m+2})
\tag{6.1}
\]

commutes with the occurrence maps, prefixes, block combination, relative
ideal image, and the construction of the target/span pair.  A positive
upper-rung membership therefore descends to the lower rung.  The converse
need not hold: lower-rung membership does not manufacture an upper-rung
solution, and every edge must still be tested.  Thus Theorem 4.1 is one
uniform algorithm at every Frattini edge, not a claim that one finite pass
has already solved all later edges.

It is nevertheless a necessary class-two gate.  A positive result says
that one pointed multiplier survives the complete matching
pro-Heisenberg screen at that edge.  It does not imply that its exact PB
endpoint is zero, that the nonlinear word conditions hold, or that the
positive choices at successive edges are already coherent.  Exact zero is
still followed by v197 boundary extraction and v174's pointed Neumann
promotion; prime-to-three and perfect-core gates remain separate.

Conversely, a negative dual at any edge is terminal for the named lower
correction: an exact universal identity would satisfy (4.9), so it cannot
exist.  This is a genuine finite obstruction, not a bounded-search failure.

## 7. Fixed frontier

\[
\begin{array}{ll}
\text{MATCHING EXPONENT POWER FACTORS THROUGH }\Delta_{m+1}
 & \text{PAPER PROOF / v213},\\
\text{PROJECTED ENDPOINT DEPENDS ONLY ON }\mu_{m+1}
 & \text{PAPER PROOF},\\
\bar{\mathcal E}_{d,m+1}(J_{m+1})=0
 & \text{PAPER PROOF},\\
q_{m+1,*}(I_m)=I(R_m),\quad \dim R_m\leq3
 & \text{PAPER PROOF},\\
\text{FIRST-EDGE ENDPOINT AUGMENTATION DIMENSION}
 & \leq486,\\
\text{POINTED-DATA-FREE EXPONENT-NINE PRE-GATE}
 & \text{ONE COMPLETE 486-DIRECTION MEMBERSHIP},\\
\text{ALL POINTED }\mu_1\text{ PLUS EXPONENT-NINE GATE}
 & \text{ONE FINITE JOINT MEMBERSHIP},\\
\text{ACTUAL }d_1,e_1,\bar\epsilon_1\text{ AND JOINT SPAN}
 & \text{NOT COMPUTED},\\
\text{EXACT PB ENDPOINT / BOUNDARY CHAINS}
 & \text{NOT COMPUTED},\\
\text{COHERENT ALL-RUNG POSITIVE CHOICES}
 & \text{NOT CONSTRUCTED},\\
\text{COFINAL LIFT / FAKE / IHARA WITNESS}
 & \text{NOT CONSTRUCTED}.
\end{array}
\tag{7.1}
\]

`R07_SIMULTANEOUS_POINTED_ENDPOINT_GATE_V214_PAPER_GRADE`
