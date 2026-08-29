# R07 all-first-shadow endpoint repair torsor (v338)

Author: Sol / 2026-08-29

Status: paper theorem strengthening the post-A5 endpoint search.  V196 varies
source representatives of one fixed first-shadow multiplier.  The present
note varies **all** first-shadow multipliers satisfying the A5 equations and
all of their source representatives in one affine criterion.  Thus failure
for the lexicographically selected A5 multiplier is not mistaken for failure
of the whole first-edge solution set.  The actual A3--A5 inputs, homogeneous
direction basis and endpoint columns have not been computed.  No milestone
numerator, compatible lift, fake certificate or Ihara witness is declared.
`verified=false`.

## 1. The complete first-edge solution torsor

Put (k=\mathbf F_3), and retain the corrected v247 first edge

\[
 F=F(x,y)\mathrel{\mathop{\twoheadrightarrow}^{\rho_1}}\Delta_1
 \mathrel{\mathop{\twoheadrightarrow}^{\pi}}\Delta_0.
\tag{1.1}
\]

Let

\[
 A=k[\Delta_1],\qquad
 I=\ker(A\to k[\Delta_0]).
\tag{1.2}
\]

Use the actual A5 maps

\[
 D:I\longrightarrow Z,\quad D(\mu)=\mu d_1,
 \qquad
 \Phi:I\longrightarrow E,\quad
 \Phi(\mu)=C(\mu\odot w).
\tag{1.3}
\]

The simultaneous first-shadow equations are

\[
 D(\mu)=e_1,qquad \Phi(\mu)=\bar\epsilon_1.
\tag{1.4}
\]

Suppose one A5 MEMBER ancestry returns a solution \(\mu_0\).  Define the
homogeneous pointed-and-endpoint kernel

\[
 \mathcal N_1=\ker D\cap\ker\Phi\le I.
\tag{1.5}
\]

### Lemma 1.1 (ALL FIRST-SHADOW SOLUTIONS)

The complete solution set of (1.4) is the affine space

\[
 \boxed{\mathcal S_1=\mu_0+\mathcal N_1.}
\tag{1.6}
\]

#### Proof

If \(\mu\) and \(\mu_0\) both solve (1.4), their difference is killed by
both maps in (1.3), hence belongs to \(\mathcal N_1\).  Conversely adding
any element of \(\mathcal N_1\) preserves both equations. \(\square\)

The direction (1.5) is larger than the freedom considered by v196.  V196
keeps \(\mu_0\) fixed and changes only its source representative.  A nonzero
element of \(\mathcal N_1\) changes the multiplier in \(k[\Delta_1]\) while
preserving every A5 equation.

## 2. Every homogeneous direction has a word-bearing roof-fibre lift

Let

\[
 \widetilde I_0=
 \ker\bigl(k[F]\to k[\Delta_0]\bigr),
 \qquad
 J_1=\ker\bigl(k[F]\to k[\Delta_1]\bigr).
\tag{2.1}
\]

The natural map

\[
 p:\widetilde I_0\longrightarrow I
\tag{2.2}
\]

is onto.  Indeed, fix one literal source section
\(s:\Delta_1\to F\).  If

\[
 \nu=\sum_{g\in\Delta_1}a_gg\in I,
\tag{2.3}
\]

then

\[
 \widetilde\nu=\sum_ga_gs(g)
\tag{2.4}
\]

maps to \(\nu\), and its image in \(k[\Delta_0]\) is zero because that of
\(\nu\) is zero.  Applying the fibre-difference normal form of v191 turns
(2.4) into literal pairs with equal \(\Delta_0\)-value.

Choose a basis \(\nu_1,\ldots,\nu_s\) of \(\mathcal N_1\), word-bearing
lifts \(\widetilde\nu_i\in\widetilde I_0\), and one word-pair lift
\(M_0\in\widetilde I_0\) of \(\mu_0\).

### Lemma 2.1 (SOURCE LIFTS OF THE WHOLE TORSOR)

The set of all word-algebra elements whose first-shadow value lies in
\(\mathcal S_1\) is

\[
 \boxed{
 p^{-1}(\mathcal S_1)=
 M_0+
 \operatorname{span}_k\{\widetilde\nu_1,\ldots,\widetilde\nu_s\}
 +J_1.}
\tag{2.5}
\]

#### Proof

Every element on the right maps to \(\mu_0+\mathcal N_1\).  Conversely, if
\(M\) maps to \(\mu_0+\sum_i a_i\nu_i\), then

\[
 M-M_0-\sum_i a_i\widetilde\nu_i\in\ker p=J_1.
\]

This proves (2.5). \(\square\)

There is no hidden choice at infinity in (2.5): the first summand and the
homogeneous roster are finite.  The only unbounded positive dovetail is the
same-successor ideal \(J_1\) already isolated by v196.

## 3. The joint endpoint criterion

Let

\[
 Y=k[PB_3]\oplus k[PB_3]\oplus k[PB_4]
\tag{3.1}
\]

and let

\[
 \mathcal E_d:k[F]\longrightarrow Y
\tag{3.2}
\]

be v196/v198's linear three-combined-block endpoint-change map, with all ten
typed values reinserted in the eleven printed occurrence positions.  For a
word-pair polynomial \(M\), write

\[
 \eta(M)=\epsilon-\mathcal E_d(M),
\tag{3.3}
\]

where \(\epsilon\) is the fixed endpoint of the corrected residual.  Thus
v194's universal promotion gate is \(\eta(M)=0\).

Choose the complete Schreier basis \(h_1,\ldots,h_r\) of
\(\ker(F\to\Delta_1)\) from v196.  Its left-ideal theorem gives

\[
 J_1=\sum_{j=1}^r k[F](h_j-1).
\tag{3.4}
\]

### Theorem 3.1 (ALL-FIRST-SHADOW ENDPOINT REPAIR)

There exists a source word-pair polynomial \(M\) which simultaneously

1. maps to **some** first-shadow solution of (1.4), and
2. has all three exact PB endpoints zero,

if and only if

\[
 \boxed{
 \eta(M_0)\in
 \operatorname{span}_k\left(
   \{\mathcal E_d(\widetilde\nu_i):1\le i\le s\}
   \cup
   \{\mathcal E_d(A(h_j-1)):A\in F,1\le j\le r\}
 \right).}
\tag{3.5}
\]

If an ancestry

\[
 \eta(M_0)=
 \sum_i a_i\mathcal E_d(\widetilde\nu_i)
 +\sum_{\ell}c_\ell
   \mathcal E_d(A_\ell(h_{j_\ell}-1))
\tag{3.6}
\]

is retained, then

\[
 \boxed{
 M=M_0+\sum_i a_i\widetilde\nu_i
       +\sum_\ell c_\ell A_\ell(h_{j_\ell}-1)}
\tag{3.7}
\]

has the two required properties.

#### Proof

By Lemma 2.1, every permitted source polynomial is \(M_0+N\), where

\[
 N\in
 \operatorname{span}\{\widetilde\nu_i\}+J_1.
\tag{3.8}
\]

Linearity and (3.3) give

\[
 \eta(M_0+N)=\eta(M_0)-\mathcal E_d(N).
\tag{3.9}
\]

Apply \(\mathcal E_d\) to (3.8) and use the exact left-ideal description
(3.4).  Equation (3.9) can vanish exactly under (3.5).  An ancestry (3.6)
gives (3.7), proves its first-shadow value belongs to (1.6), and makes
(3.9) zero. \(\square\)

V196 is the special case \(s=0\), or equivalently the search inside the
single fibre \(p^{-1}(\mu_0)\).  The new finite columns
\(\mathcal E_d(\widetilde\nu_i)\) must be inserted before concluding that
the fixed-multiplier repair orbit is insufficient.

## 4. A4 anchor choice is gauge, not a separate search axis

Let \(\kappa_0\) and \(\kappa_0'\) be the corrected v247 base points built
from two word-bearing A4 lifts of the projected generator.  Both satisfy

\[
 \Phi(\kappa_0)=\Phi(\kappa_0')=\bar\epsilon_1.
\tag{4.1}
\]

Put \(\delta=\kappa_0'-\kappa_0\).  Then \(\delta\in\ker\Phi\).  The two
A5 slice residuals obey

\[
 r_0'=e_1-\kappa_0'd_1=r_0-\delta d_1.
\tag{4.2}
\]

### Lemma 4.1 (ANCHOR-GAUGE BIJECTION)

The map

\[
 \theta\longmapsto\theta-\delta
\tag{4.3}
\]

is a bijection between the A5 slice ancestries based at \(\kappa_0\) and
those based at \(\kappa_0'\), and it preserves the final multiplier:

\[
 \boxed{
 \kappa_0+\theta=
 \kappa_0'+(\theta-\delta).}
\tag{4.4}
\]

#### Proof

If \(\theta\in\ker\Phi\), then \(\theta-\delta\in\ker\Phi\).  Equation
(4.2) shows

\[
 r_0=\theta d_1
 \quad\Longleftrightarrow\quad
 r_0'=(\theta-\delta)d_1.
\]

Equation (4.4) is immediate, and replacing \(\delta\) by \(-\delta\) gives
the inverse map. \(\square\)

If the same literal lift of \(\delta\) is added to the base ancestry and
subtracted from the slice ancestry, it cancels already in \(k[F]\).  Hence
different valid A4 anchor choices do not create a new mathematical family
beyond (2.5).  Source representatives trivial in \(\Delta_1\) remain the
separate \(J_1\) direction and are still load-bearing for exact PB endpoints.

## 5. Finite homogeneous roster and positive dovetail

The space \(\mathcal N_1\) is finite-dimensional.  Once the actual A4 kernel
is available, a complete but potentially large construction is ordinary
finite linear algebra:

1. choose a transversal \(T\) of \(K=\ker(\Delta_1\to\Delta_0)\);
2. use the basis

   \[
   \{t(k-1):t\in T,\ k\in K\setminus\{1\}\}
   \tag{5.1}
   \]

   of \(I\), retaining source words from the A4 basis;
3. evaluate the joint matrix \((D,\Phi)\) on (5.1); and
4. compute its complete nullspace with word-bearing ancestry.

This returns the \(\nu_i\) required by Theorem 3.1.  It is a finite complete
construction, not a word-radius search, although its size can make a GHA
implementation expensive.  An invariant-queue implementation may compress
the image computation, but it must retain domain dependencies if it claims a
complete basis of \(\ker(D,\Phi)\); image rank alone loses precisely the
homogeneous directions used here.

For the witness-first positive branch, seed one sparse endpoint echelon with
the finite columns \(\mathcal E_d(\widetilde\nu_i)\), then stream the v196
columns \(\mathcal E_d(A(h_j-1))\).  If (3.5) has a finite ancestry, fair
dovetail eventually finds it.  A bounded failure remains UNKNOWN.

A genuine negative certificate must annihilate **both** column families:

\[
 \lambda(\eta(M_0))\ne0,
 \quad
 \lambda\mathcal E_d(\widetilde\nu_i)=0,
 \quad
 \lambda\mathcal E_d(A(h_j-1))=0
\tag{5.2}
\]

for every \(i,A,j\).  A dual for the v196 family alone excludes only the
chosen multiplier, not all A5 solutions.

## 6. Consequence for the witness chain

The complete post-A5 order is now:

1. obtain one actual A5 MEMBER multiplier \(\mu_0\) and word lift \(M_0\);
2. compute the finite homogeneous kernel \(\mathcal N_1\);
3. test the finite homogeneous endpoint columns before and during the v196
   same-successor dovetail;
4. on (3.6), replay the final literal polynomial (3.7) in all eleven
   occurrences;
5. use v194/v197 to extract the three finite PB boundary chains; and
6. invoke v191 to descend that one finite identity through every matched
   relative pro-3 rung.

This removes a false negative axis: neither the lexicographically selected
A4 anchor nor the first A5 ancestry is privileged by the universal endpoint
equation.  It does not remove the need for the pending actual A0 word, A3
target, A4 kernel, A5 MEMBER result, exact endpoint columns, nonlinear side
gates, formation and perfect-core gates.

```text
ALL A5 FIRST-SHADOW SOLUTIONS:                    mu0 + ker(D,Phi)
ALL SOURCE LIFTS OF ALL A5 SOLUTIONS:             M0 + lifted kernel + J1
JOINT EXACT-ENDPOINT REPAIR CRITERION:            PAPER PROOF
V196 FIXED-MULTIPLIER SEARCH:                     STRICT SPECIAL CASE
A4 ANCHOR VARIATION:                              GAUGE / NOT NEW AXIS
FINITE HOMOGENEOUS DIRECTION BASIS:               ALGORITHM / NOT COMPUTED
ACTUAL ENDPOINT COLUMN ANCESTRY:                  NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                   NOT CONSTRUCTED
```

`R07_ALL_FIRST_SHADOW_ENDPOINT_REPAIR_TORSOR_V338_PAPER_GRADE`
