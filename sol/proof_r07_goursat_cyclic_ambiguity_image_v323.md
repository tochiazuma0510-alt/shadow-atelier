# R07 Goursat cyclic-ambiguity image (v323)

Author: Sol / 2026-08-29

Status: paper theorem sharpening v318 and v322.  The image of a
prefix-corrected cyclic ambiguity under any Goursat quotient is not an
arbitrary linear-algebra rank problem: it is either zero or one explicitly
translated cyclic-invariant space.  This gives a closed membership test and
a literal preimage formula.  The actual R07 Goursat quotients and return
images have not yet been authenticated, so no lift, fake certificate or
Ihara witness is declared.

## 1. Cyclic invariants under a quotient

Let \(k=\mathbf F_3\), let

\[
 \beta:G\twoheadrightarrow D
\tag{1.1}
\]

be a surjection of finite groups, and let \(r,p\in G\).  Write

\[
 R=\langle r\rangle,qquad
 \bar r=\beta(r),qquad
 \bar p=\beta(p),qquad
 o=|R|,qquad \bar o=|\langle\bar r\rangle|.
\tag{1.2}
\]

Then \(\bar o\mid o\), and put

\[
 m=o/\bar o=|R\cap\ker\beta|.
\tag{1.3}
\]

For a group \(E\) and \(s\in E\), use the right-invariant space

\[
 K_s^E=\ker\bigl(k[E]\xrightarrow{\,a\mapsto a(1-s)\,}k[E]\bigr).
\tag{1.4}
\]

The superscript will be suppressed when the group is clear.  The linear
pushforward induced by (1.1) is denoted by

\[
 \beta_*:k[G]\longrightarrow k[D].
\tag{1.5}
\]

### Theorem 1.1 (CYCLIC-INVARIANT QUOTIENT FORMULA)

Inside \(k[D]\),

\[
 \boxed{\beta_*(K_r^G)=mK_{\bar r}^D.}
\tag{1.6}
\]

Here \(m\) is read in \(k\).  Equivalently,

\[
 \beta_*(K_r^G)=
 \begin{cases}
  0,&3\mid m,\\
  K_{\bar r}^D,&3\nmid m.
 \end{cases}
\tag{1.7}
\]

#### Proof

The orbits of right multiplication by \(R\) in \(G\) are the sets \(aR\),
and their orbit sums

\[
 N_{aR}=\sum_{j=0}^{o-1}[ar^j]
\tag{1.8}
\]

form a basis of \(K_r^G\).  The image of \(R\) in \(D\) is
\(\langle\bar r\rangle\), and every element in that image occurs exactly
\(m\) times in (1.8).  Hence

\[
 \beta_*(N_{aR})
 =m\sum_{j=0}^{\bar o-1}[\beta(a)\bar r^j].
\tag{1.9}
\]

As \(a\) varies, the sums on the right contain one basis vector for every
right \(\langle\bar r\rangle\)-orbit in \(D\).  Thus their span is
\(K_{\bar r}^D\), and (1.6)--(1.7) follow. \(\square\)

The modular multiplicity \(m\) is load-bearing.  A quotient which collapses
a three-part of the cyclic return can annihilate the entire invariant
ambiguity even though its characteristic-zero pushforward is nonzero.

## 2. Prefix correction and exact local image

Let \(\epsilon\in k^\times\) and retain the v312--v313 ambiguity

\[
 U=\epsilon K_r^Gp^{-1}\leq k[G].
\tag{2.1}
\]

### Corollary 2.1 (PREFIX-CORRECTED IMAGE)

\[
 \boxed{
 \beta_*(U)=\epsilon mK_{\bar r}^D\bar p^{-1}.}
\tag{2.2}
\]

In particular, for \(d\in k[D]\),

\[
 \boxed{
 d\in\beta_*(U)
 \Longleftrightarrow
 \begin{cases}
   d=0,&3\mid m,\\
   (d\bar p)(1-\bar r)=0,&3\nmid m.
 \end{cases}}
\tag{2.3}
\]

#### Proof

Pushforward commutes with right multiplication by a group element:

\[
 \beta_*(ap^{-1})=\beta_*(a)\bar p^{-1}.
\tag{2.4}
\]

Apply Theorem 1.1 and the nonzero scalar \(\epsilon\).  When \(m\ne0\) in
\(k\), membership in the translated space
\(K_{\bar r}^D\bar p^{-1}\) is equivalent to
\(d\bar p\in K_{\bar r}^D\), which is precisely the second equation in
(2.3). \(\square\)

Thus the local MEMBER/NONMEMBER decision requires neither enumeration of
all source orbit sums nor row reduction.  It requires the two cyclic orders,
one group-algebra right translation and one exact equality.

### Corollary 2.2 (FULL-ONTO CRITERION)

The ambiguity map \(\beta_*|_U:U\to k[D]\) is onto if and only if

\[
 \boxed{\bar r=1\quad\text{and}\quad3\nmid m.}
\tag{2.5}
\]

#### Proof

If \(3\mid m\), the image is zero.  Otherwise its dimension is

\[
 \dim_kK_{\bar r}^D=[D:\langle\bar r\rangle],
\tag{2.6}
\]

which equals \(|D|=\dim_k k[D]\) exactly when \(\bar r=1\).  Right
translation and multiplication by a nonzero scalar preserve dimension.
\(\square\)

For an involutory return \(r\), one always has \(3\nmid m\).  In that case
full onto is exactly the group-theoretic condition that the Goursat overlap
kills the return image.

## 3. Literal preimage without elimination

Assume \(3\nmid m\) and let \(d\) pass (2.3).  Expand

\[
 d\bar p
 =\sum_{C\in D/\langle\bar r\rangle}c_C
   \sum_{x\in C}[x].
\tag{3.1}
\]

For every orbit \(C=\bar a\langle\bar r\rangle\), choose one
\(a_C\in G\) with \(\beta(a_C)=\bar a\).  Put

\[
 z_C=\sum_{j=0}^{o-1}[a_Cr^j]\in K_r^G
\tag{3.2}
\]

and

\[
 \boxed{
 u_d=
 \epsilon\left((\epsilon m)^{-1}\sum_Cc_Cz_C\right)p^{-1}
 \in U.}
\tag{3.3}
\]

### Proposition 3.1 (EXPLICIT LOCAL SECOND HOMOTOPY)

\[
 \boxed{\beta_*(u_d)=d.}
\tag{3.4}
\]

#### Proof

Equation (1.9) sends each \(z_C\) to \(m\) times the corresponding orbit
sum in (3.1).  Equation (2.4), followed by the scalar cancellation in
(3.3), gives (3.4). \(\square\)

The only set-theoretic choices in (3.3) are lifts of representatives of
the quotient orbits.  Once authenticated transversals are fixed, (3.3) is a
deterministic word-bearing local section on the entire image (2.2).

If \(3\mid m\), the only correctable target is zero and the canonical
preimage \(u_0=0\) suffices.  This zero-image case must not be mistaken for
a resource failure or a bounded-search miss.

## 4. Dual collapse

V322 Lemma 4.1 says that a functional \(\lambda\in k[D]^*\) annihilates
\(\beta_*(U)\) exactly when its pullback has zero sum on every right
\(\langle r\rangle\)-orbit in \(G\).  Formula (1.9) reduces these equations
to the quotient itself:

\[
 m\sum_{x\in C}
 \lambda(x\bar p^{-1})=0
\tag{4.1}
\]

for every right \(\langle\bar r\rangle\)-orbit \(C\subseteq D\).  Hence:

1. if \(3\mid m\), every functional is an annihilator;
2. if \(3\nmid m\), the annihilator is exactly the prefix-twisted
   orbit-sum-zero space on \(D\).

This agrees with (2.3) by finite-dimensional duality and removes the need to
generate duplicated source-orbit equations.

## 5. Goursat-chain consequence

At step \(i\) of v322, apply the theorem to the Goursat quotient

\[
 \beta_i:G_i\twoheadrightarrow D_i
\tag{5.1}
\]

and the local triple \((\epsilon_i,p_i,r_i)\).  Put

\[
 m_i=
 \frac{|\langle r_i\rangle|}
 {|\langle\beta_i(r_i)\rangle|}.
\tag{5.2}
\]

The recursively encountered Goursat defect \(d_i\) is locally correctable
if and only if

\[
 \boxed{
 \begin{cases}
 d_i=0,&3\mid m_i,\\
 (d_i\beta_i(p_i))(1-\beta_i(r_i))=0,&3\nmid m_i.
 \end{cases}}
\tag{5.3}
\]

When (5.3) holds, (3.3) supplies the correction \(u_i\) used in v322
(3.5)--(3.6).  In particular, an ordering for which every new cumulative
overlap kills \(r_i\) and \(3\nmid m_i\) gives the full closed selector of
v322 Theorem 3.1.

This suggests a strictly authenticated ordering heuristic:

1. prefer a next coordinate whose \(D_i\) kills the return image;
2. otherwise minimize the exact local codimension
   \(|D_i|-[D_i:\langle\beta_i(r_i)\rangle]\), while keeping the quotient
   itself small for replay;
3. if the return loses a three-part, record the zero-image branch before
   testing the actual defect; and
4. never change the order after seeing the target without registering a new
   branch.

Unlike a generic rank heuristic, every score above has a group-theoretic
meaning and an exact replay.

## 6. Cofinal consequence and remaining boundary

Suppose the quotient maps, cyclic orders, authenticated transversals and
actual defects are compatible across a cofinal tower.  If every actual
defect passes (5.3), applying (3.3) recursively gives the finite-level
actual-even local preimages required by v322.  If these data and transversals
are natural, the v322 recursion is itself compatible.  If the chosen
transversals are not natural, the same finite-level successes instead prove
nonemptiness of the complete marginal solution set at every level, and v313
finite-fibre compactness selects a compatible completed coefficient.
Arbitrary levelwise preimages themselves are not declared compatible.  This
is distinct from v314's vertical-kernel Hensel preimage, which remains an
alternative constructive route and is not supplied merely by (3.3).

The theorem does not establish the nonlinear H1/H2/pentagon recurrence,
formation, settlement or perfect-core gates.  It does, however, replace the
previously open *local rank computation* in each Goursat overlap by the exact
test (5.3).  The remaining common-source linear question is the sequence of
actual invariance equations, together with the construction of the genuine
joint images \(H_i\) and their quotients \(D_i\).

```text
CYCLIC AMBIGUITY IMAGE UNDER ANY GROUP QUOTIENT: PAPER PROOF
MOD-3 COLLAPSE MULTIPLICITY:                    EXACT
LOCAL MEMBER TEST / LITERAL PREIMAGE:           PAPER PROOF
FULL ONTO IFF OVERLAP KILLS RETURN (+m NONZERO): PAPER PROOF
GOURSAT LOCAL RANKS FROM ORDERS:                 PAPER PROOF
ACTUAL R07 GOURSAT QUOTIENTS / RETURN IMAGES:    NOT COMPUTED
ACTUAL ALL-LEVEL INVARIANCE TESTS:               NOT PERFORMED
NONLINEAR / FORMATION / PERFECT-CORE GATES:      OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:  NONE
```

`R07_GOURSAT_CYCLIC_AMBIGUITY_IMAGE_V323_PAPER_GRADE`
