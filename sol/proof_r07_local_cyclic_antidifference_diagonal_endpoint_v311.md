# R07 local cyclic antidifference / diagonal endpoint reduction (v311)

Author: Sol / 2026-08-29

Status: paper theorem and exact decomposition of v310's endpoint homotopy.
Multiplication by each literal endpoint \(1-R_b(g)\) has a closed elementary
description: its image consists exactly of finite group-algebra chains whose
coefficient sum is zero on every right orbit of \(R_b(g)\).  Thus the local
part of the universal endpoint repair has an explicit antidifference.  The
remaining obstruction is solely whether the seven local primitives come
from one common lift-kernel coefficient.  No actual endpoint has been
computed and no witness is asserted.

## 1. One group and one right-difference operator

Let \(G\) be any group, let \(k\) be a field, and fix \(r\in G\).  On the
finite-support group algebra \(k[G]\), define

\[
 \partial_r:k[G]\longrightarrow k[G],
 \qquad
 \partial_r(a)=a(1-r).
\tag{1.1}
\]

Right multiplication by \(r\) partitions \(G\) into the sets

\[
 g\langle r\rangle.
\tag{1.2}
\]

For a finite-support chain \(z=\sum_hz_hh\), define its orbit-sum function

\[
 \Sigma_r(z)(g\langle r\rangle)
   =\sum_{h\in g\langle r\rangle}z_h.
\tag{1.3}
\]

The sum is finite even when \(r\) has infinite order.

### Theorem 1.1 (FINITE-SUPPORT CYCLIC ANTIDIFFERENCE)

\[
 \boxed{\operatorname{im}\partial_r=\ker\Sigma_r.}
\tag{1.4}
\]

Moreover every \(z\in\ker\Sigma_r\) has a finite-support preimage obtained
independently on each right orbit meeting its support.

#### Proof

For a basis element,

\[
 \partial_r(g)=g-gr,
\tag{1.5}
\]

whose two coefficients lie in the same orbit and sum to zero.  Hence
\(\operatorname{im}\partial_r\subseteq\ker\Sigma_r\).

Conversely fix one orbit.  If \(r\) has finite order \(m\), write the orbit
as \(g,gr,\ldots,gr^{m-1}\).  A vector \((z_0,\ldots,z_{m-1})\) of total
sum zero has a cyclic potential: choose one coefficient and solve
successively the coefficient equations in \(a-ar=z\); the zero sum is
exactly the closing equation.  If \(r\) has infinite order, the orbit is a
copy of \(\mathbf Z\).  Set the potential to zero to the left of the finite
support and take finite cumulative sums.  The total-sum-zero condition makes
it zero again to the right.  Thus the potential has finite support.  Summing
over the finitely many orbits meeting \(z\) gives a finite preimage.
\(\square\)

### Corollary 1.2 (KERNEL OF THE RIGHT DIFFERENCE)

If \(r\) has infinite order, \(\ker\partial_r=0\).  If \(r\) has finite
order, the kernel is spanned by the finite orbit sums

\[
 \sum_{j=0}^{|r|-1}gr^j.
\tag{1.6}
\]

#### Proof

The equation \(a=ar\) makes coefficients constant on every right orbit.  A
nonzero constant on an infinite orbit violates finite support, while on a
finite orbit it is a scalar multiple of (1.6).  \(\square\)

## 2. Apply the antidifference to all seven R07 blocks

For each occurrence-resolved universal block \(b\), let

\[
 r_b=R_b(g_{760})\in G_b.
\tag{2.1}
\]

V239's endpoint convention gives

\[
 \widetilde D_{1,b}\widetilde d_b=1-r_b.
\tag{2.2}
\]

Let

\[
 \partial=\bigoplus_b\partial_{r_b},
 \qquad
 \Sigma=\bigoplus_b\Sigma_{r_b},
 \qquad
 \mathcal K_r=\bigoplus_b\ker\partial_{r_b}.
\tag{2.3}
\]

The block tags include H1, H2 and all five ordered pentagon occurrences;
isomorphic context groups are not merged.  For v310's endpoint target
\(\eta=(\eta_b)_b\), Theorem 1.1 gives the necessary condition

\[
 \boxed{\Sigma(\eta)=0.}
\tag{2.4}
\]

If (2.4) holds, choose the deterministic finite-support local primitive

\[
 A=(A_b)_b,
 \qquad
 A_b(1-r_b)=\eta_b,
\tag{2.5}
\]

by the orbitwise construction of Theorem 1.1.  The complete set of local
primitives is

\[
 \boxed{A+\mathcal K_r.}
\tag{2.6}
\]

Thus local inversion is constructive; it is not the remaining common-word
problem.

## 3. Exact diagonal compatibility criterion

Let \(\rho_b:\Gamma\to G_b\) be the seven fixed context maps and define

\[
 \rho_*:k[\Gamma]\longrightarrow\bigoplus_bk[G_b],
 \qquad
 \rho_*(\ell)=(\rho_{b,*}(\ell))_b.
\tag{3.1}
\]

Restrict it to v310's lift kernel \(\mathcal L_1\).

### Theorem 3.1 (LOCAL-TO-DIAGONAL ENDPOINT CRITERION)

The actual endpoint equation

\[
 \exists\ell\in\mathcal L_1:\quad
 \widetilde D_1(\ell\widetilde d)=\eta
\tag{3.2}
\]

holds if and only if

\[
 \boxed{
 \Sigma(\eta)=0,
 \qquad
 \rho_*(\mathcal L_1)\cap(A+\mathcal K_r)\ne\varnothing.}
\tag{3.3}
\]

If \(B\) belongs to the intersection and \(B=\rho_*(\ell)\), then that
literal \(\ell\) solves (3.2).

#### Proof

For \(\ell\in\mathcal L_1\), equivariance and (2.2) give blockwise

\[
 \widetilde D_{1,b}(\ell\widetilde d_b)
 =\rho_{b,*}(\ell)(1-r_b).
\tag{3.4}
\]

If (3.2) holds, Theorem 1.1 gives (2.4), and
\(\rho_*(\ell)-A\) lies in every \(\ker\partial_{r_b}\), proving the
intersection condition.  Conversely an element of the intersection has
the form \(A+K\), with \(K\in\mathcal K_r\); multiplying componentwise by
\(1-r_b\) gives \(\eta\), which is (3.2).  \(\square\)

This is an exact separation:

```text
LOCAL CYCLIC DIFFERENCE:       orbit sums Sigma(eta)=0
COMMON-WORD COMPATIBILITY:     one diagonal lift-kernel coefficient
```

Separate local solutions do not construct the common coefficient.

## 4. Finite Schreier seeds in the diagonal problem

Let \(n_1,\ldots,n_s\) be v310's literal Schreier roster.  Then

\[
 \rho_*(\mathcal L_1)
 =\sum_{i=1}^s k[\Gamma]\,\rho_*(n_i-1),
\tag{4.1}
\]

with the action diagonal through all seven context maps.  Hence (3.3) becomes

\[
 \boxed{
 (A+\mathcal K_r)\cap
 \sum_{i=1}^s k[\Gamma]\rho_*(n_i-1)\ne\varnothing.}
\tag{4.2}
\]

This can be smaller than using endpoint columns directly: the local
antidifference removes multiplication by \(1-r_b\), and \(\mathcal K_r\)
records exactly the ambiguity it creates.

A positive ancestry in (4.2) gives \(\ell\), hence v310's repaired literal
polynomial.  A failure of (2.4) is a complete obstruction to that endpoint.
A bounded failure of the infinite diagonal orbit test remains UNKNOWN.

## 5. Relative-dihedral meaning

The operator \(a\mapsto a(1-r_b)\) is the local cyclic-difference part of
the relative construction.  Theorem 1.1 supplies a pointed local
antidifference on every actual target passing (2.4); no full module
contraction is needed for that value.

Return-odd dihedral antisymmetrization can make the local choice canonical
on its stable summand.  The return-even survivor is not another local
division problem: after (2.5), it is the diagonal intersection (4.2).
Thus the field-outer/class-specific homotopy sought in v171--v174 is a
common-source lifting statement for the seven local primitives, modulo the
explicit invariant spaces \(\mathcal K_r\).

For the actual endpoint, one successful diagonal ancestry is enough.  A
linear section on the entire even orbit would again require annihilator
compatibility, but that stronger assertion is unnecessary for the single
v174 correction value.

## 6. Computation contract after actual inputs exist

For each block, a producer should:

1. normalize \(r_b\) and every support word of \(\eta_b\) in the fixed PB
   presentation;
2. partition support by right \(\langle r_b\rangle\)-orbits and record every
   coefficient sum;
3. reject the exact candidate if one sum is nonzero;
4. otherwise build and replay the finite potential \(A_b\);
5. construct the finite Schreier seeds and their seven simultaneous images;
6. seek a finite diagonal ancestry landing in \(A+\mathcal K_r\); and
7. compile \(\ell\), repaired \(M\), endpoint zero and v193's boundary chain.

The independent checker reconstructs right-orbit equivalence and potentials
without importing the producer's normal-form or coset helper.  Mutations
cover one support coefficient, right-power relation, block tag, potential,
Schreier word, diagonal context value and invariant-space term.

## 7. Fixed frontier

```text
IMAGE OF a -> a(1-r):                         EXACT ORBIT-SUM KERNEL
FINITE-SUPPORT LOCAL ANTIDIFFERENCE:           PAPER CONSTRUCTION
SEVEN LOCAL ENDPOINT OBSTRUCTION:              EXPLICIT
REMAINING COMMON-SOURCE OBSTRUCTION:           EXACT DIAGONAL INTERSECTION
FINITE SCHREIER SEEDS FOR DIAGONAL SIDE:        PAPER PROOF (v310)
ACTUAL eta / LOCAL ORBIT SUMS / PRIMITIVES:     NOT COMPUTED
ACTUAL DIAGONAL LIFT-KERNEL ANCESTRY:           NOT COMPUTED
RELATIVE PRO-3 CORRECTION / COFINAL LIFT:       NOT CONSTRUCTED
FAKE / IHARA WITNESS:                          NONE
```

`R07_LOCAL_CYCLIC_ANTIDIFFERENCE_DIAGONAL_ENDPOINT_V311_PAPER_GRADE`
