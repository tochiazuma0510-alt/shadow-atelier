# R07 weighted ambient-filtration Newton selector (v328)

Author: Sol / 2026-08-29

Status: paper theorem providing a second structural route around v321's
saturation kernel.  Instead of forcing the ambient filtration on a localized
module to equal its ordinary intrinsic \(J\)-adic filtration, one presents
the ambient filtration itself by finitely many depth-shifted generators.
A strict weighted free cover then supports the same based Neumann and Newton
recursion.  Finite weighted generation for the actual R07 localized module
is not yet proved.  No compatible lift, fake certificate or Ihara witness is
declared.

## 1. The induced localized filtration

Let \(\Lambda\) be complete for a two-sided ideal \(J\), let \(Z\) be a
complete separated left \(\Lambda\)-module, and let \(L\leq Z\) be a closed
\(\Lambda\)-submodule.  Use the ambiently induced filtration

\[
 L_r=L\cap J^rZ
\quad(r\geq0).
\tag{1.1}
\]

It satisfies

\[
 L_{r+1}\subseteq L_r,\qquad
 JL_r\subseteq L_{r+1}.
\tag{1.2}
\]

V321 observes that \(L_r\) need not equal \(J^rL\).  The present note keeps
\(L_r\) as the authoritative depth and changes the free cover accordingly.

## 2. Finite weighted generation

Choose elements

\[
 \ell_1,\ldots,\ell_t\in L,
\qquad
 w_1,\ldots,w_t\in\mathbf Z_{\geq0},
\qquad
 \ell_j\in L_{w_j}.
\tag{2.1}
\]

### Definition 2.1 (STRICT WEIGHTED GENERATING ROSTER)

The roster \((\ell_j,w_j)\) strictly generates the induced filtration if

\[
 \boxed{
 L_r=
 \sum_{j=1}^t
 J^{\max(0,r-w_j)}\ell_j
 \quad\text{for every }r\geq0.}
\tag{2.2}
\]

Let

\[
 F=\bigoplus_{j=1}^t\Lambda e_j
\tag{2.3}
\]

and give it the weighted filtration

\[
 F_r=
 \sum_{j=1}^t
 J^{\max(0,r-w_j)}e_j.
\tag{2.4}
\]

Define

\[
 q:F\twoheadrightarrow L,\qquad q(e_j)=\ell_j.
\tag{2.5}
\]

### Lemma 2.2 (STRICT WEIGHTED FREE COVER)

If (2.2) holds, then

\[
 \boxed{q(F_r)=L_r\quad(r\geq0).}
\tag{2.6}
\]

In particular, every ambient depth-\(r\) localized residual has a
depth-\(r\) coefficient in the weighted free cover, even when its class in
\((L\cap J^rZ)/J^rL\) is nonzero.

#### Proof

Equations (2.4)--(2.5) give

\[
 q(F_r)=
 \sum_jJ^{\max(0,r-w_j)}\ell_j,
\tag{2.7}
\]

which is (2.2). \(\square\)

The ordinary v319 cover is the special case \(w_j=0\) for every \(j\).
V326's retract route can often provide such weight-zero strictness.  Positive
weights record a finite, controlled failure of ordinary saturation rather
than pretending it is absent.

## 3. A weighted based Neumann lift

Let \(A\) be a complete filtered correction module and let

\[
 B:A\longrightarrow L
\tag{3.1}
\]

be the leading linearized residual map.  Suppose there is a
filtration-preserving map

\[
 s_0:F\longrightarrow A
\tag{3.2}
\]

and a continuous endomorphism \(R:F\to F\) such that

\[
 Bs_0-q=qR
\tag{3.3}
\]

and

\[
 R(F_r)\subseteq F_{r+1}
\quad(r\geq0).
\tag{3.4}
\]

### Theorem 3.1 (WEIGHTED BASED NEUMANN SECTION)

The series

\[
 (1+R)^{-1}=\sum_{\nu\geq0}(-R)^\nu
\tag{3.5}
\]

converges on \(F\), and

\[
 \boxed{
 s=s_0(1+R)^{-1}}
\tag{3.6}
\]

is filtration-preserving and satisfies

\[
 \boxed{Bs=q.}
\tag{3.7}
\]

#### Proof

Equation (3.4) sends the \(\nu\)-th term of (3.5) at least \(\nu\) steps
deeper, so completeness and separatedness give convergence and the inverse
identity.  Equation (3.3) says

\[
 Bs_0=q(1+R).
\tag{3.8}
\]

Right-compose with (3.5) to obtain (3.7).  Every partial sum preserves
filtration and its omitted tail tends to arbitrarily deep filtration, so
\(s\) is filtration-preserving. \(\square\)

No quotient splitter or ordinary \(J\)-adic saturation is used.  The
load-bearing finite leading certificate is now the weighted roster, the
maps \(s_0,R\), and direct replay of (3.3)--(3.4).

## 4. Weighted localized Newton recursion

Let \(\Phi\) be the exact literal residual map.  Assume:

1. every legal state has residual in \(L\);
2. if \(z_r=\Phi(F_r^{\rm word})\in L_r\), a correction with leading value
   \(-z_r\) gives an exact replayed remainder in \(L_{r+1}\);
3. (2.2) holds and \(s\) is the section of Theorem 3.1; and
4. the materialization of \(s(v)\) respects the registered common-word and
   side-gate typing.

### Theorem 4.1 (WEIGHTED AMBIENT-FILTRATION NEWTON)

Starting from any \(z_0\in L_0\), choose by Lemma 2.2

\[
 v_r\in F_r,\qquad q(v_r)=z_r,
\tag{4.1}
\]

and apply the correction

\[
 a_r=-s(v_r).
\tag{4.2}
\]

Then the exact residuals satisfy

\[
 z_{r+1}\in L_{r+1}
\tag{4.3}
\]

and the corrections converge to a state with zero residual.

#### Proof

Theorem 3.1 and (4.1) give

\[
 B(a_r)=-Bs(v_r)=-q(v_r)=-z_r.
\tag{4.4}
\]

The exact affine depth law and hypothesis 2 give (4.3).  Lemma 2.2 supplies
the next coefficient in the same authoritative ambient depth.  Induction
therefore produces a Cauchy correction sequence.  Completeness gives its
limit, and separatedness of the residual filtration makes the limiting
residual zero. \(\square\)

This is the v319--v321 recursion with the correct induced filtration built
into the source.  It is not a reindexing by a bounded Artin--Rees lag: every
correction still has the exact current ambient depth.

## 5. How finite weighted generation can be certified

Condition (2.2) is an all-depth statement.  Valid finite structural
certificates include:

1. a finite homogeneous presentation of the extended Rees module associated
   to the decreasing filtration \(L_\bullet\);
2. a finite-state recurrence proving (2.2) from a registered depth onward,
   together with the finitely many initial depths;
3. a finite collection of filtered retract summands from v326 whose shifted
   images generate every \(L_r\); or
4. a direct normal form which expresses each ambient-depth element with the
   coefficient bounds in (2.2).

A finite list which spans only \(L/JL\), or an Artin--Rees inclusion with a
lag, does not prove (2.2).  A bounded computational search through several
depths is evidence only unless one of the recurrences above closes the tail.

At a finite quotient, one can test a proposed roster through the available
depth by comparing

\[
 \sum_jJ^{\max(0,r-w_j)}\ell_j
\quad\text{with}\quad
 L\cap J^rZ
\tag{5.1}
\]

and emit MEMBER ancestries or complete separating duals.  These tests are
canaries for the structural theorem.

## 6. Relation to the class-two canary

For the first nonlinear remainder \(q_2\), v321 asks whether

\[
 q_2\in J^2L
\tag{6.1}
\]

for the ordinary cover.  The weighted route asks instead for the exact
ancestry

\[
 \boxed{
 q_2=
 \sum_j a_j\ell_j,
 \qquad
 a_j\in J^{\max(0,2-w_j)}.}
\tag{6.2}
\]

Equation (6.2) may hold even when (6.1) fails, but only if the same finite
weighted roster is proved to satisfy (2.2) at every later depth.  Adding a
new ad hoc generator for each encountered remainder would merely rename the
pointed route and would not be a finite uniform selector.

## 7. Cofinal naturality

Let all modules, filtrations and rosters carry a level \(n\).  If weights
are fixed, generators reduce compatibly, and \(q_n,s_{0,n},R_n\) commute
with reduction, then (3.6) and the Newton recursion commute with reduction.
They give one explicit completed correction.

If only exact finite-level nonempty accepted sets are available, a
finite-fibre compactness theorem may give existence, but it does not turn an
unbounded sequence of new weights into the finite presentation required
here.

## 8. R07 boundary

For the v252 localized target, the structural nonlinear routes are now:

1. ordinary strictness \(L\cap J^rZ=J^rL\);
2. a filtered retraction as in v326--v327;
3. a finite strict weighted roster satisfying (2.2); or
4. actual pointed ancestry at every encountered remainder.

Route 3 can accommodate a finite amount of persistent saturation failure
without losing exact depth.  The actual weighted formation/Brunnian roster,
its Rees tail certificate, the leading maps \(s_0,R\), and nonlinear
side-gate replay are not constructed.

The weighted strict-cover lemma, weighted Neumann section and weighted
Newton recursion are paper proofs.  The actual R07 hypotheses remain open.
A compatible cofinal lift, fake certificate and Ihara witness remain absent.

R07_WEIGHTED_AMBIENT_FILTRATION_NEWTON_V328_PAPER_GRADE
