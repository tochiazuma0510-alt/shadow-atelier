# R07 exponent-nine area-character gate v210

Author: Sol / 2026-08-28

Status: paper theorem strengthening v208--v209 with the actual roof exponent
lattice \(18\mathbf Z^2\).  The class-two exponent-nine joint source group
has exactly 729 elements, but the image of the entire roof kernel is contained
in one central \(C_3\).  Hence the visible image of the first-successor
kernel has dimension at most one, and the complete projected repair roster
has at most 729 columns.  A single invariant-functional test decides whether
that repair direction is zero or all of the central \(C_3\).  No actual
6,441 scalar replay, first multiplier, endpoint, repair, dual, compatible
lift, fake certificate, or Ihara witness is computed here.
verified=false.

## 1. The joint source group is exactly the order-729 quotient

Retain the class-two exponent-nine endpoint quotients
\(\mathcal N_3(9),\mathcal N_4(9)\) and the eleven-occurrence diagonal map

\[
 \phi_9:F(x,y)\twoheadrightarrow D_9
\tag{1.1}
\]

from v208.  Put

\[
 \mathcal H_2(9)=
 F(x,y)/\langle\gamma_3F,\ w^9\ (w\in F)\rangle^{\rm normal}.
\tag{1.2}
\]

It has the normal form

\[
 x^a y^b c^d,\qquad
 c=[x,y],\qquad a,b,d\in\mathbf Z/9\mathbf Z,
\tag{1.3}
\]

and order \(9^3=729\).

### Lemma 1.1 (THE TYPED PB3 COORDINATE IS FAITHFUL)

The \((x,y)\) E3 occurrence induces an embedding

\[
 \mathcal H_2(9)\hookrightarrow\mathcal N_3(9).
\tag{1.4}
\]

Consequently

\[
 \boxed{D_9\cong\mathcal H_2(9),\qquad |D_9|=729.}
\tag{1.5}
\]

#### Proof

Use the marked direct-product decomposition

\[
 PB_3\cong F(x=A_{12},y=A_{23})\times\langle z\rangle,
 \qquad z=A_{12}A_{13}A_{23}.
\tag{1.6}
\]

Both the third lower-central subgroup and the verbal ninth-power subgroup
split over this direct product.  Their intersection with the displayed free
factor is respectively \(\gamma_3F\) and the verbal ninth-power subgroup of
\(F\).  Thus the restriction of \(PB_3\to\mathcal N_3(9)\) to
\(\langle x,y\rangle\) has exactly the kernel in (1.2), proving (1.4).

Every component of (1.1) factors through \(\mathcal H_2(9)\), while the
typed PB3 coordinate is faithful on it.  The diagonal image is therefore
isomorphic to \(\mathcal H_2(9)\), proving (1.5). \(\square\)

This strengthens the upper bound in v208 Theorem 4.1 to an exact order.

## 2. The actual roof kernel lands in one central \(C_3\)

Let

\[
 \psi_0:F\twoheadrightarrow\Delta_0,
 \qquad H_0=\ker\psi_0.
\tag{2.1}
\]

V156, transported through the marked roof isomorphism in v189, gives

\[
 \operatorname{exp}_{x,y}(H_0)
 =18\mathbf Z\oplus18\mathbf Z.
\tag{2.2}
\]

### Theorem 2.1 (ROOF AREA CHARACTER)

For every \(h\in H_0\), its image under the identification (1.5) has the
unique form

\[
 \boxed{\phi_9(h)=c^{\,3\omega(h)},\qquad
        \omega(h)\in\mathbf F_3.}
\tag{2.3}
\]

The map

\[
 \omega:H_0\longrightarrow\mathbf F_3
\tag{2.4}
\]

is a group homomorphism invariant under conjugation by \(F\).  In
particular,

\[
 \boxed{\phi_9(H_0)\leq\langle c^3\rangle\cong C_3.}
\tag{2.5}
\]

#### Proof

Write the normal form of \(\phi_9(h)\) as in (1.3).  Equation (2.2) says
that its first two coordinates are divisible by 18, and therefore vanish
modulo nine.  Thus \(\phi_9(h)=c^d\) is central.

The reduction of (1.1) modulo three factors through \(\Delta_0\) by v208
Theorem 1.1.  Since \(h\in H_0\), its reduction is the identity.  Therefore
\(d\equiv0\pmod3\), giving the unique expression (2.3).

Products of such central elements add their exponents, so \(\omega\) is a
homomorphism.  Conjugation fixes the central element \(c^{3\omega(h)}\);
hence \(\omega(uhu^{-1})=\omega(h)\) for every \(u\in F\).  This proves
(2.5). \(\square\)

For a literal word, \(\omega\) is just its class-two signed-area coordinate
modulo nine, divided by three and reduced modulo three.  No PB4 collection
is needed to compute this scalar after the typed PB3 \((x,y)\) coordinate
has been authenticated.

## 3. The non-roof test is a 6,441-scalar test

Let

\[
 \mathcal R_{6441}=\{r_1,\ldots,r_{6441}\}
\tag{3.1}
\]

be the complete v190 normal-relator roster for \(H_0\), and put

\[
 \omega_j=\omega(r_j)\in\mathbf F_3.
\tag{3.2}
\]

### Corollary 3.1 (SCALAR NON-ROOF CRITERION)

The exponent-nine screen factors through \(\Delta_0\) if and only if

\[
 \boxed{\omega_j=0\quad(1\leq j\leq6441).}
\tag{3.3}
\]

If one scalar is nonzero, then

\[
 \boxed{\phi_9(H_0)=\langle c^3\rangle\cong C_3.}
\tag{3.4}
\]

#### Proof

V190 says that the \(r_j\) normally generate \(H_0\).  Theorem 2.1 says
that \(\omega\) is conjugation-invariant.  Hence its image is generated
additively by the 6,441 values (3.2).  This image is zero exactly in (3.3);
otherwise it is the whole one-dimensional target.  Factorization through
\(F/H_0=\Delta_0\) is equivalent to killing \(H_0\), proving both claims.
\(\square\)

Thus v208's ten-coordinate nonidentity roster may be checked independently,
but mathematically one authenticated scalar per relator is complete.

## 4. The first-successor visible kernel is zero or one dimensional

Retain

\[
 F\xrightarrow{\psi_1}\Delta_1\twoheadrightarrow\Delta_0,
 \qquad
 K=\ker(\Delta_1\to\Delta_0)\cong(C_3)^t,
 \qquad
 H_1=\ker\psi_1.
\tag{4.1}
\]

For every roof relator set

\[
 b_j=\psi_1(r_j)\in K.
\tag{4.2}
\]

V188 gives

\[
 K=k[\Delta_0]\langle b_1,\ldots,b_{6441}\rangle.
\tag{4.3}
\]

Let

\[
 \mathscr R=k[\Delta_0]^{6441}
\tag{4.4}
\]

with basis \(e_j\).  Define \(k[\Delta_0]\)-module maps

\[
 B:\mathscr R\twoheadrightarrow K,\qquad B(e_j)=b_j,
\tag{4.5}
\]

and

\[
 \Omega:\mathscr R\longrightarrow k_{\rm triv},
 \qquad \Omega(e_j)=\omega_j.
\tag{4.6}
\]

Here \(k_{\rm triv}\) is the trivial roof module.  Equation (4.6) is a
module map because \(\omega\) is conjugation-invariant.

### Theorem 4.1 (VISIBLE SUCCESSOR-KERNEL DICHOTOMY)

Put

\[
 L_1=\phi_9(H_1)\leq\langle c^3\rangle.
\tag{4.7}
\]

Then

\[
 \boxed{L_1=c^{\,3\Omega(\ker B)}.}
\tag{4.8}
\]

Exactly one of the following holds.

1. \(L_1=1\).  Equivalently there is a unique roof-invariant functional

   \[
    \lambda\in\operatorname{Hom}_{k[\Delta_0]}(K,k_{\rm triv})
   \tag{4.9}
   \]

   satisfying

   \[
    \boxed{\lambda(b_j)=\omega_j\quad(1\leq j\leq6441).}
   \tag{4.10}
   \]

2. \(L_1=\langle c^3\rangle\cong C_3\).  Equivalently no functional in
   (4.9) satisfies (4.10).

#### Proof

A finite vector

\[
 u=\sum a_{q,j}\,q e_j\in\mathscr R
\tag{4.11}
\]

encodes the product of the corresponding powers of conjugates of the
relators \(r_j\).  Its successor value is \(B(u)\), while its exponent-nine
area value is \(\Omega(u)\).  Every element of \(H_0\) has such an
expression, and every such expression gives an element of \(H_0\).
Therefore the expressions representing \(H_1\) are precisely
\(\ker B\), proving (4.8).

Since the target of \(\Omega\) is one dimensional,
\(\Omega(\ker B)\) is either zero or all of \(k\).  It is zero exactly when
\(\ker B\subseteq\ker\Omega\).  Because \(B\) is onto by (4.3), this is
equivalent to a unique linear factorization

\[
 \Omega=\lambda B.
\tag{4.12}
\]

Both \(B\) and \(\Omega\) are module maps and \(B\) is onto, so the
factor \(\lambda\) is a module map to the trivial module.  Equation (4.12)
on the basis \(e_j\) is exactly (4.10).  This proves the dichotomy.
\(\square\)

The test is small: compute the invariant dual
\((K^*)^{\Delta_0}\) from the two marked roof-generator actions, then impose
the 6,441 scalar equations (4.10).  No state roster of \(\Delta_0\) or
\(\Delta_1\) is involved.

## 5. At most 729 complete projected repair columns

V209 Theorem 3.1 identifies the projected first-successor direction ideal
with the group-algebra ideal generated by \(L_1-1\).

### Corollary 5.1 (ZERO OR 729-COLUMN REPAIR SPACE)

If the first branch of Theorem 4.1 holds, then

\[
 \Phi_9(J_1)=0,\qquad
 \bar{\mathcal E}_d(J_1)=0.
\tag{5.1}
\]

If the second branch holds, choose one retained ancestry
\(h_*\in H_1\) with \(\phi_9(h_*)=c^3\).  Then

\[
 \boxed{
 \bar{\mathcal E}_d(J_1)=
 \operatorname{span}_k
 \{\Lambda_9(d(c^3-1)):d\in D_9\}.}
\tag{5.2}
\]

The roster in (5.2) has exactly 729 candidate columns before dependent
columns are discarded.

#### Proof

The two cases give respectively \(L_1=1\) and
\(L_1=\langle c^3\rangle\).  Apply v209 equations (3.4)--(4.3), using
\(|D_9|=729\) from Lemma 1.1. \(\square\)

A completed nonmembership dual for (5.1) or (5.2) is an exact no-repair
certificate for every finite-support representative of the named
\(\mu_1\).  Projected membership remains only a seed for exact PB replay.

## 6. Fixed executable boundary

After task198 exports the exact roof relators and task188 returns their
successor defects:

1. compute the 6,441 signed-area scalars \(\omega_j\);
2. stop this screen as a roof canary if they are all zero;
3. otherwise compute \((K^*)^{\Delta_0}\) and test (4.10);
4. if the functional exists, the complete projected repair space is zero;
5. otherwise extract one kernel ancestry with area one and traverse the
   exact 729 columns (5.2); and
6. only after the actual \(M_0\) exists, compare its projected endpoint
   with that complete space.

~~~text
JOINT CLASS-TWO EXPONENT-NINE SOURCE GROUP:        EXACT ORDER 729
ROOF-KERNEL IMAGE IN THAT GROUP:                   AT MOST CENTRAL C3
NON-ROOF TEST:                                     6,441 AREA SCALARS
VISIBLE FIRST-SUCCESSOR KERNEL:                    ZERO OR CENTRAL C3
ZERO/C3 DICHOTOMY BY INVARIANT FUNCTIONAL:         PAPER-PROOF
COMPLETE PROJECTED REPAIR ROSTER:                  ZERO OR 729 COLUMNS
ACTUAL AREA SCALARS / K / FUNCTIONAL / M0:         NOT COMPUTED
PROJECTED ENDPOINT / DUAL / EXACT REPAIR:          NOT COMPUTED
RELATIVE PRO-3 LIFT / FAKE / IHARA WITNESS:        NOT CONSTRUCTED
~~~

R07_EXPONENT9_AREA_CHARACTER_GATE_V210_PAPER_GRADE
