# R07 marginal fibre-constant dual criterion (v315)

Author: Sol / 2026-08-29

Status: paper theorem dual to v314.  It identifies every obstruction to a
vertical marginal correction with a scalar common-source score which is
constant on the refinement fibres but does not descend from the lower target.
For v313's prefix-corrected cyclic quotients, the admissible local dual
functions have an explicit orbit-sum-zero description.  This gives a second,
often smaller, exact finite decision algorithm.  No actual R07 score space or
target pairing has been computed, and no lift or witness is declared.

## 1. Dual of one matched marginal edge

Retain v314's finite-dimensional commuting square over \(k=\mathbf F_3\):

\[
\begin{CD}
 A'=k[\Gamma'] @>{\mathcal T'}>> W'\\
 @V{u}VV                         @VV{v}V\\
 A =k[\Gamma ] @>{\mathcal T }>> W,
\end{CD}
\qquad
u,v\text{ surjective}.
\tag{1.1}
\]

Put

\[
 K=\ker u,
 \qquad Z=\ker v,
 \qquad R=\mathcal T'(K)\leq Z.
\tag{1.2}
\]

The pointed obstruction of v314 lies in \(Z/R\).  Define the upper dual
identity space

\[
 \mathcal E=
 \{\Lambda\in(W')^*:
       (\mathcal T')^*\Lambda\in\operatorname{im}u^*\}.
\tag{1.3}
\]

Every descended functional \(v^*\psi\), \(\psi\in W^*\), belongs to
\(\mathcal E\), because commutativity gives

\[
 (\mathcal T')^*v^*\psi=u^*\mathcal T^*\psi.
\tag{1.4}
\]

### Theorem 1.1 (VERTICAL MARGINAL DUALITY)

Restriction from \(W'\) to \(Z\) induces a canonical isomorphism

\[
 \boxed{
 (Z/R)^*\simeq
 \mathcal E/v^*(W^*).}
\tag{1.5}
\]

Consequently:

1. \(R=Z\) if and only if every element of \(\mathcal E\) descends from
   \(W^*\);
2. for \(\delta\in Z\), one has \(\delta\in R\) if and only if

   \[
    \boxed{\Lambda(\delta)=0
    \quad\text{for every }\Lambda\in\mathcal E;}
   \tag{1.6}
   \]

3. if \(\delta\notin R\), some \(\Lambda\in\mathcal E\) has
   \(\Lambda(\delta)\ne0\), and its class modulo \(v^*(W^*)\) is the
   complete v314 separating dual.

#### Proof

Because \(v\) is onto, restriction gives an exact dual sequence

\[
 0\longrightarrow W^*
 \mathrel{\mathop{\longrightarrow}^{v^*}}(W')^*
 \mathrel{\mathop{\longrightarrow}^{\operatorname{res}}}Z^*
 \longrightarrow0.
\tag{1.7}
\]

For \(\Lambda\in(W')^*\), the restriction
\(\operatorname{res}\Lambda\) annihilates \(R=\mathcal T'(K)\) exactly
when \((\mathcal T')^*\Lambda\) annihilates \(K\).  Since \(u\) is onto,

\[
 K^\perp=\operatorname{im}u^*.
\tag{1.8}
\]

Thus the inverse image under restriction of
\(R^\perp=(Z/R)^*\) is precisely \(\mathcal E\).  Its restriction kernel is
\(v^*(W^*)\) by (1.7), proving (1.5).  The three consequences are ordinary
finite-dimensional separation.  \(\square\)

The quotient by descended functionals is load-bearing.  A functional which
is merely nonzero upstairs need not be a new obstruction; it may vanish on
all of \(Z\).

## 2. Fibre-constant scalar scores

Identify \((k[\Gamma'])^*\) with all scalar functions
\(F:\Gamma'\to k\).  Let

\[
 q:\Gamma'\twoheadrightarrow\Gamma,
 \qquad N=\ker q.
\tag{2.1}
\]

For \(\Lambda\in(W')^*\), define its common-source score

\[
 F_\Lambda(g)=\Lambda(\mathcal T'([g])).
\tag{2.2}
\]

### Lemma 2.1 (FIBRE-CONSTANT FORM)

The following are equivalent:

1. \(\Lambda\in\mathcal E\);
2. \(F_\Lambda\) is constant on every fibre of \(q\);
3. for any group-generating set \(N=\langle s_1,\ldots,s_r\rangle\),

   \[
    \boxed{
    F_\Lambda(gs_i)=F_\Lambda(g)
    \quad(g\in\Gamma',\ 1\leq i\leq r).}
   \tag{2.3}
   \]

#### Proof

Under the function identification, \(\operatorname{im}u^*\) consists
exactly of functions pulled back from \(\Gamma\), hence functions constant
on the fibres of \(q\).  This proves 1 equivalent to 2.  The fibres are the
right \(N\)-cosets.  Constancy under a generating set and its inverses is
equivalent to constancy on each whole coset, proving 2 equivalent to 3.
\(\square\)

Thus the complete dual calculation may impose the scalar equalities (2.3)
instead of materializing every vector column
\(\mathcal T'(g(s_i-1))\).  These are exact transposes of the same finite
system, not a relaxation.

## 3. Explicit local duals for the prefix-corrected quotients

At one v313 block suppress the level index.  Retain

\[
 H=\epsilon K_rp^{-1}\leq k[G],
 \qquad
 K_r=\ker(a\mapsto a(1-r)),
 \qquad Q=k[G]/H,
\tag{3.1}
\]

where \(G\) is finite and \(\epsilon\in k^\times\).  A functional on \(Q\)
is a function \(\varphi:G\to k\) annihilating \(H\).

### Lemma 3.1 (PREFIX-TWISTED LOCAL DUAL CONDITION)

The space \(K_r\) has one basis vector

\[
 \sum_{h\in C}[h]
\tag{3.2}
\]

for every right \(\langle r\rangle\)-orbit \(C\subseteq G\).  Hence
\(\varphi\) defines an element of \(Q^*=H^\perp\) exactly when

\[
 \boxed{
 \sum_{h\in C}\varphi(hp^{-1})=0
 \quad\text{for every right }\langle r\rangle
 \text{-orbit }C.}
\tag{3.3}
\]

#### Proof

Right multiplication by \(r\) permutes the group basis in disjoint cycles.
The kernel of one minus this permutation consists of the constant
coefficient vectors on those cycles, proving (3.2).  Right multiplication
by \(p^{-1}\) sends (3.2) to
\(\sum_{h\in C}[hp^{-1}]\).  The nonzero scalar \(\epsilon\) does not change
its annihilator.  Pairing with \(\varphi\) gives (3.3).  \(\square\)

The right translation by \(p^{-1}\) must not be dropped.  This is the dual
counterpart of v312's correction of the naked \(1-r\) formula.

## 4. The complete marginal score

Write the upper v313 target as

\[
 W'=k[\Delta_1']\oplus\bigoplus_bQ_b'
       \oplus W'_{\rm side}.
\tag{4.1}
\]

Represent a dual row by

\[
 \Lambda=(\varphi_0,(\varphi_b)_b,\varphi_{\rm side}),
\tag{4.2}
\]

where every \(\varphi_b\) satisfies (3.3).  Then (2.2) is the explicit
additively separable score

\[
 \boxed{
 F_\Lambda(g)=
 \varphi_0(\pi_1(g))+
 \sum_b\varphi_b([\rho_b(g)])+
 \varphi_{\rm side}(S(g)).}
\tag{4.3}
\]

Here \(S(g)\) denotes the exact registered side-column value.  Repeated
occurrences remain separate summands even if their group labels coincide.

Combining Theorem 1.1 and Lemmas 2.1 and 3.1 gives the following exact R07
criterion.

### Theorem 4.1 (NO-NEW-FIBRE-IDENTITY CRITERION)

The full vertical marginal map is onto \(Z\) if and only if every tuple of
local functions satisfying the prefix-twisted orbit equations (3.3) whose
score (4.3) is constant on the \(N\)-fibres is itself the pullback of a
lower target functional.

For the one actual residual \(\delta\), full onto is unnecessary.  It is
correctable if and only if every such fibre-constant score has zero pairing
with \(\delta\).  A nonzero pairing is an exact return-even survivor at that
edge.

#### Proof

Equations (3.3) parametrize exactly the duals of the local quotient
coordinates.  Equation (4.3) is the definition of the pullback
\((\mathcal T')^*\Lambda\) on the group basis.  Lemma 2.1 identifies
membership in \(\mathcal E\), and Theorem 1.1 gives both assertions.
\(\square\)

This converts the missing class-specific second homotopy into a concrete
classification problem:

```text
local admissibility       = prefix-twisted cyclic orbit sums;
common-source identity    = scalar score constant on every refinement fibre;
old identity              = descended from the lower target;
new obstruction           = non-descended identity pairing with the actual residual.
```

## 5. Finite exact algorithm and relation to v314

At a finite edge one may work on the dual side as follows.

1. Parametrize each local dual space using (3.3), keeping all occurrence
   tags and side rows.
2. Impose (2.3) for the literal kernel generators and all
   \(g\in\Gamma'\).
3. Quotient the resulting solution space by the explicitly pulled-back rows
   \(v^*(W^*)\).
4. Pair a basis of the quotient with the actual \(\delta\).

If every pairing is zero, finite duality proves the v314 MEMBER condition;
primal elimination then recovers literal ancestry.  If a pairing is nonzero,
the corresponding row is the complete NONMEMBER certificate.  A producer may
choose whichever of primal closure (v314) or dual fibre-constancy is smaller;
an independent checker should replay the result from the opposite
description when resources permit.

For the return split, restrict Steps 1--4 to the even eigenspace after
checking that return commutes with every map.  The odd eigenspace remains the
domain of the established relative-dihedral formula.  Proving at every edge
that the actual even residual annihilates all new fibre identities is exactly
the dual form of the actual-even preimage condition in v314 (5.3).  A
uniform constructive classification of those identities would give the
corresponding all-edge selector.

The theorem is finite and linear.  It neither supplies the actual residual
nor proves the nonlinear pentagon/hexagon depth recurrence, formation, or
perfect-core gates.

## 6. Fixed frontier

```text
VERTICAL COKERNEL DUAL AS NEW FIBRE IDENTITIES:     PAPER PROOF
FIBRE CONSTANCY BY LITERAL KERNEL GENERATORS:       PAPER PROOF
PREFIX-TWISTED LOCAL DUAL ORBIT EQUATIONS:          PAPER PROOF
PRIMAL / DUAL FINITE DECISION EQUIVALENCE:          PAPER PROOF
ACTUAL EDGE SCORE SPACE:                            NOT COMPUTED
ACTUAL RETURN-EVEN PAIRINGS:                        NOT COMPUTED
ALL-EDGE NO-NEW-IDENTITY THEOREM:                   NOT PROVED
NONLINEAR / FORMATION / PERFECT-CORE GATES:         OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:     NONE
```

`R07_MARGINAL_FIBRE_CONSTANT_DUAL_V315_PAPER_GRADE`
