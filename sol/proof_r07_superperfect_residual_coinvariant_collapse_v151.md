# R07 superperfect residual coinvariant collapse v151

Author: Sol / 2026-08-27

Status: paper theorem.  In the first task176 relative-Frattini extension,
the formation-residual kernel inside the elementary-abelian relation module
is exactly the PSL commutator submodule.  Thus v148's extension-class descent
system is automatic after passage to coinvariants.  The action matrices and
the actual joint correction map have not yet been materialized.  No cofinal
lift, fake certificate, or Ihara witness is declared.

## 1. General setup

Let \(\mathcal C_S\) be the formation of finite groups with no composition
factor isomorphic to

\[
 S=PSL(2,8).
\tag{1.1}
\]

Consider a finite extension

\[
 1\longrightarrow V\longrightarrow H
 \stackrel{p}{\longrightarrow}E\longrightarrow1,
\tag{1.2}
\]

where \(V\) is elementary abelian.  Put

\[
 R=R_S(E),
 \qquad C=E/R,
 \qquad V_S=V\cap R_S(H).
\tag{1.3}
\]

For the \(E\)-module \(V\), write

\[
 [R,V]
 =\left\langle r\cdot v-v:r\in R,\ v\in V\right\rangle.
\tag{1.4}
\]

It is an \(E\)-submodule because \(R\triangleleft E\).  The quotient

\[
 V_R:=V/[R,V]
\tag{1.5}
\]

is the maximal quotient of \(V\) on which \(R\) acts trivially.

## 2. Cohomology of a superperfect residual

Call a finite group \(R\) superperfect here when

\[
 R_{\rm ab}=0,
 \qquad M(R)=H_2(R,\mathbf Z)=0.
\tag{2.1}
\]

### Lemma 2.1 (LOW-DEGREE VANISHING)

If \(R\) is superperfect and \(W\) is an abelian group with trivial
\(R\)-action, then

\[
 H^1(R,W)=0,
 \qquad H^2(R,W)=0.
\tag{2.2}
\]

#### Proof

The first equality is

\[
 H^1(R,W)=\operatorname{Hom}(R_{\rm ab},W)=0.
\tag{2.3}
\]

For trivial coefficients, the universal-coefficient sequence gives

\[
 0\longrightarrow
 \operatorname{Ext}^1_{\mathbf Z}(R_{\rm ab},W)
 \longrightarrow H^2(R,W)
 \longrightarrow\operatorname{Hom}(M(R),W)
 \longrightarrow0.
\tag{2.4}
\]

Both outer terms vanish by (2.1), proving (2.2). \(\square\)

### Lemma 2.2 (INFLATION IS AN ISOMORPHISM)

Let

\[
 1\to R\to E\to C\to1
\tag{2.5}
\]

have superperfect kernel, and let \(W\) be an \(E\)-module on which \(R\)
acts trivially.  Then

\[
 \boxed{
 \operatorname{Inf}:H^2(C,W)\xrightarrow{\sim}H^2(E,W).}
\tag{2.6}
\]

#### Proof

In the Lyndon--Hochschild--Serre low-degree sequence, inflation identifies
\(H^2(C,W)\) with the kernel of restriction

\[
 H^2(E,W)\longrightarrow H^2(R,W)
\tag{2.7}
\]

provided the two adjacent terms built from \(H^1(R,W)\) vanish.  Lemma 2.1
makes those terms zero, and it also makes the target in (2.7) zero.  Hence
the kernel is all of \(H^2(E,W)\), proving (2.6). \(\square\)

Equivalently, the only obstruction to descending an abelian extension across
\(E\twoheadrightarrow C\) is the nontrivial action of \(R\); after killing
that action, no independent degree-two class survives.

## 3. Exact residual-intersection theorem

### Theorem 3.1 (SUPERPERFECT RESIDUAL COLLAPSE)

Assume that \(R=R_S(E)\) is superperfect.  Then for every extension (1.2),

\[
 \boxed{
 V\cap R_S(H)=[R,V].}
\tag{3.1}
\]

Consequently the maximal formation-visible quotient from v148 is simply

\[
 \boxed{V/V_S=V_R.}
\tag{3.2}
\]

#### Proof

Put \(N=[R,V]\) and \(W=V/N\).  By construction, \(R\) acts trivially on
\(W\).  Let

\[
 \xi_W\in H^2(E,W)
\tag{3.3}
\]

be the pushout of the actual extension class of (1.2).  Lemma 2.2 says that
\(\xi_W\) inflates from \(H^2(C,W)\).  Thus \(N\) satisfies both conditions
in v148 Theorem 2.1.  The maximality statement v148 Theorem 2.2 gives

\[
 V_S\leq [R,V].
\tag{3.4}
\]

For the reverse inclusion, formation residuals commute with epimorphic
images, so

\[
 p(R_S(H))=R_S(E)=R.
\tag{3.5}
\]

For \(r\in R\), choose \(\widetilde r\in R_S(H)\) above it.  Since
\(R_S(H)\triangleleft H\), for every \(v\in V\) the commutator

\[
 [\widetilde r,v]
\tag{3.6}
\]

lies in \(R_S(H)\cap V\).  Under the module action, the elements (3.6)
span the same submodule as all \(r\cdot v-v\); replacing \(r\) by \(r^{-1}\)
removes any commutator-convention reversal.  Hence

\[
 [R,V]\leq V_S.
\tag{3.7}
\]

Equations (3.4) and (3.7) prove (3.1), and (3.2) follows. \(\square\)

### Corollary 3.2 (RESIDUAL EXACT SEQUENCE)

Under the same hypotheses, restriction of \(p\) gives

\[
 1\longrightarrow [R,V]
 \longrightarrow R_S(H)
 \longrightarrow R
 \longrightarrow1.
\tag{3.8}
\]

Modulo \([R,V]\), the extension (1.2) is the pullback of an extension of
\(C\) by \(V_R\).  Thus v148's literal cochain equation has a solution on
\(V_R\) for the actual extension class; no search over further quotients of
\(V_R\) is required.

## 4. Why the theorem applies to task176

V149 proves

\[
 R_S(G)=\widetilde S\cong PSL(2,8).
\tag{4.1}
\]

The group \(PSL(2,8)\) is perfect and has trivial Schur multiplier, the same
input already used in v149 Theorem 2.2.  Therefore it is superperfect.

Let the first joint relative-Frattini extension be

\[
 1\longrightarrow V\longrightarrow\mathcal H_1
 \longrightarrow G\longrightarrow1.
\tag{4.2}
\]

Theorem 3.1 specializes to the exact formula

\[
 \boxed{
 V_S:=V\cap R_S(\mathcal H_1)
 =[\widetilde S,V].}
\tag{4.3}
\]

This replaces the open computation in v148 (4.2)--(4.3): the extension
cocycle \(\alpha\) is not needed to determine \(V_S\).  It remains relevant
only if one wants an explicit descended extension or a literal residual
section, not for the submodule (4.3).

The same conclusion holds when the residual is a finite direct power
\(S^t\).  Indeed a direct power of a perfect group is perfect and

\[
 M(S^t)=M(S)^t
\tag{4.4}
\]

because all tensor terms involving abelianizations vanish.  Hence a product
of task176-type PSL strips is again superperfect.

## 5. Finite computation is now linear action only

Suppose \(s_1,s_2\) are the two frozen generators of \(\widetilde S\) and
their action matrices on \(V\) are \(A_1,A_2\).  Since they generate
\(\widetilde S\),

\[
 [\widetilde S,V]
 =\operatorname{im}(A_1-I)+\operatorname{im}(A_2-I).
\tag{5.1}
\]

Thus the complete first-rung residual computation is:

1. materialize the word-bearing \(\widetilde S\) generators from v149/v150;
2. replay their conjugation action on every ordered task179 relation-module
   generator;
3. form the block matrix \([A_1-I\mid A_2-I]\) over \(\mathbf F_3\);
4. retain an exact basis of its image and an exact quotient map
   \(V\twoheadrightarrow V_{\widetilde S}\); and
5. independently reconstruct both actions and compare every matrix entry,
   image basis, pivot, and quotient coordinate.

There is no enumeration of submodules and no degree-two cochain column
generation in this step.

Two terminal cases are especially useful:

\[
 \dim V_{\widetilde S}=0
 \quad\Longrightarrow\quad
 V_S=V,
\tag{5.2}
\]

so the formation-fibre equation is vacuous, whereas

\[
 \dim V_{\widetilde S}>0
\tag{5.3}
\]

identifies the exact maximal trivial \(\widetilde S\)-quotient on which that
equation must be solved.  In modular characteristic, dimensions or
composition-factor labels do not decide (5.2); the generator matrices must be
used.

## 6. Naturality across refinement edges

The coinvariant description also removes one possible source of incompatibility.
Suppose a refinement map gives surjections

\[
 R'\twoheadrightarrow R,
 \qquad V'\twoheadrightarrow V
\tag{6.1}
\]

which are equivariant.  Then

\[
 \boxed{
 [R',V']\twoheadrightarrow[R,V].}
\tag{6.2}
\]

Indeed an equivariant map sends every generator \(r'v'-v'\) to a generator
\(rv-v\), proving one inclusion; surjectivity in (6.1) supplies lifts of
every \(r,v\), proving equality of the image.  Therefore there is a natural
surjection

\[
 V'_{R'}\twoheadrightarrow V_R.
\tag{6.3}
\]

For an inverse system whose residuals remain superperfect PSL strips and
whose module/action squares are authenticated, the formation-residual
submodules consequently commute with every transition.  One does not need a
new extension-class descent proof at each rung.

This does not yet construct the desired infinite homotopy.  The relation
defect, the correction domain, and the map from words to coinvariants must
also commute with the transitions.

## 7. Remaining actual-word equation

With (4.3), v148 (5.3) becomes

\[
 \boxed{
 B_{\rm ev}(c)=-\beta_{\rm ev},
 \qquad
 q_{\rm coinv}(\rho(c))
 =-q_{\rm coinv}(\omega_S(\delta_{\widehat b}))
 \quad\text{in }V_{\widetilde S}.}
\tag{7.1}
\]

The second target requires the finite relative-arithmetic anchor of v150 if
one follows the formation-purified route.  The direct task175/task179 route
can instead solve the first equation and replay the literal successor without
identifying its base with the v18 arithmetic representative.

The two maps in (7.1) are still distinct.  Theorem 3.1 does not identify
\(B_{\rm ev}\) with \(q_{\rm coinv}\rho\), and it does not materialize an
exact-commutator word.  It removes precisely the formerly open computation of
\(V_S\) from the joint system.

```text
SUPERPERFECT LOW-DEGREE COHOMOLOGY VANISHING:       PAPER_PROOF
V_S = [R,V] FOR SUPERPERFECT FORMATION RESIDUAL:    PAPER_PROOF
TASK176 FIRST-RUNG V_S = [tilde-S,V]:               PAPER_PROOF
EXTENSION-COCYCLE SEARCH FOR V_S:                   ELIMINATED
WORD-BEARING tilde-S ACTION ON TASK179 V:           NOT MATERIALIZED
TASK179 COINVARIANT DIMENSION/BASIS:                 NOT COMPUTED
ACTUAL JOINT WORD EQUATION (7.1):                    OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:     NOT DECLARED
```

`R07_SUPERPERFECT_RESIDUAL_COINVARIANT_COLLAPSE_V151_PAPER_GRADE`
