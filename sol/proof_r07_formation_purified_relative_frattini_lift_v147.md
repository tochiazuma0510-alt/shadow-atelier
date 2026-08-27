# R07 formation-purified relative-Frattini lift v147

Author: Sol / 2026-08-27

Status: paper theorem and next typed gate.  This note proves the exact
condition under which a finite task179/v146 component can be combined with
the arithmetic dihedral base on every finite quotient having no
\(PSL(2,8)\) composition factor.  It also shows that this condition is a
finite linear restriction at an elementary-abelian relative Frattini edge.
The required first-rung formation residual and the actual R07 membership have
not been computed.  No cofinal lift, fake, or Ihara witness is declared.

## 1. The formation kernel maps onto the finite formation residual

Put

\[
 S=PSL(2,8)
\tag{1.1}
\]

and let \(\mathcal C_S\) be the formation of finite groups with no
composition factor isomorphic to \(S\).  For a finite group \(H\), write

\[
 R_S(H)=
 \bigcap_{\substack{N\triangleleft H\\H/N\in\mathcal C_S}}N.
\tag{1.2}
\]

Let \(F\) be a finitely generated free group, let \(\widehat F\) be its
profinite completion, and put

\[
 \mathcal R_S(F)=
 \ker\bigl(\widehat F\to F^{\mathcal C_S}\bigr).
\tag{1.3}
\]

### Theorem 1.1 (FINITE RESIDUAL IMAGE EQUALITY)

For every continuous epimorphism \(q:\widehat F\twoheadrightarrow H\) to a
finite group,

\[
 \boxed{q(\mathcal R_S(F))=R_S(H).}
\tag{1.4}
\]

#### Proof

Every quotient \(H/N\in\mathcal C_S\) kills \(\mathcal R_S(F)\), so
\(q(\mathcal R_S(F))\leq R_S(H)\).  Conversely, the quotient

\[
 H/q(\mathcal R_S(F))
\tag{1.5}
\]

is a finite image of \(F^{\mathcal C_S}\), hence belongs to
\(\mathcal C_S\).  The defining minimality in (1.2) therefore gives
\(R_S(H)\leq q(\mathcal R_S(F))\). \(\square\)

Lemma 1.1 of v33 proves the first inclusion.  Equality in (1.4) is the
additional positive direction needed to construct formation-invisible
corrections rather than merely locate their images.

## 2. Exact purification of one finite component

Let \(A\in\widehat F\) be a fixed arithmetic GT word and let

\[
 a_H=q(A)\in H.
\tag{2.1}
\]

For a desired finite component \(b\in H\), put

\[
 \delta_H=a_H^{-1}b.
\tag{2.2}
\]

### Theorem 2.1 (FORMATION-PURIFICATION CRITERION)

The following are equivalent.

1. There is \(r\in\mathcal R_S(F)\) such that \(q(Ar)=b\).
2. \(\delta_H\in R_S(H)\).

When they hold, every finite \(\mathcal C_S\)-quotient sees \(Ar\) and
\(A\) as the same word value.

#### Proof

The equality \(q(Ar)=b\) is equivalent to
\(q(r)=a_H^{-1}b=\delta_H\).  Theorem 1.1 says that such an \(r\) exists in
\(\mathcal R_S(F)\) exactly when \(\delta_H\in R_S(H)\).  The final
assertion is the definition of the kernel (1.3). \(\square\)

The criterion must be applied to the **joint** finite image of every value
which is required to agree.  Coordinatewise membership in the individual
formation residuals is not sufficient for a subdirect product: an abelian or
solvable diagonal correlation can remain between coordinates.

### Corollary 2.2 (COMPATIBLE PURIFICATION)

Let \(H_{n+1}\twoheadrightarrow H_n\) be a nested finite inverse system,
let \(b_n\) be a compatible family, and put

\[
 \delta_n=q_n(A)^{-1}b_n.
\tag{2.3}
\]

If \(\delta_n\in R_S(H_n)\) for every \(n\), there is one
\(r\in\mathcal R_S(F)\) satisfying

\[
 q_n(Ar)=b_n\qquad\text{for every }n.
\tag{2.4}
\]

#### Proof

For each \(n\), Theorem 1.1 makes

\[
 X_n=\{r\in\mathcal R_S(F):q_n(r)=\delta_n\}
\tag{2.5}
\]

a nonempty closed subset of the compact group \(\mathcal R_S(F)\).
Compatibility makes these sets nested.  Their intersection is nonempty, and
any element in it satisfies (2.4). \(\square\)

This compactness statement produces one profinite relative correction.  A
sequence of ordinary word approximations is obtained by solving the finite
joint cylinder at each level.  No nontrivial ordinary word is asserted to be
invisible in every finite solvable quotient.

## 3. The task179 first-rung gate

Let \(\mathcal H_1\) be the **joint** finite matched group containing:

1. the two copies of the first PB3 relative Frattini quotient;
2. the first PB4 relative Frattini quotient;
3. all ten linked source/coface values and repeated-context equalities;
4. the frozen marked roof and side values which are to agree with the
   relative-dihedral component; and
5. the reduction to the pinned level-zero joint group.

V145 proves that a task179 `COMMON_WORD` satisfies the three relation words
in the first relative Frattini quotients.  V146 strengthens its correction
to an exact commutator.  Neither theorem proves formation purification.

Let \(b_1\in\mathcal H_1\) be the complete finite component represented by
the exact-commutator common word, let \(a_1\) be the complete component of
the fixed arithmetic word \(A\), and put

\[
 \delta_1=a_1^{-1}b_1.
\tag{3.1}
\]

### Corollary 3.1 (FIRST-RUNG RELATIVE GATE)

The v146 finite component can be combined with the arithmetic word on all
\(\mathcal C_S\)-quotients if and only if

\[
 \boxed{\delta_1\in R_S(\mathcal H_1).}
\tag{3.2}
\]

If (3.2) holds, Theorem 2.1 returns a profinite relative correction having
the displayed first-rung value and invisible in every no-\(S\) finite
quotient.  If it fails, only that displayed first-rung component fails the
formation-purified branch.  Another solution in the task179/v146 affine
fibre may still pass.

The arithmetic component \(a_1\) is load-bearing.  Comparing \(b_1\) only
with the identity is correct only after proving that the chosen arithmetic
base is identity in every registered relative coordinate.

## 4. Linear restriction at an elementary-abelian edge

Consider one finite transition

\[
 1\longrightarrow V\longrightarrow H_1
 \stackrel{p}{\longrightarrow}H_0\longrightarrow1,
\tag{4.1}
\]

where \(V\) is elementary abelian of characteristic three.  Put

\[
 V_S=V\cap R_S(H_1).
\tag{4.2}
\]

Because \(R_S(H_1)\) is characteristic, \(V_S\) is an
\(\mathbf F_3[H_0]\)-submodule of \(V\).

Fix a coarse component \(b_0\) which is already formation-purified and one
arbitrary finer lift \(\widehat b_0\).  Every other finer lift has the form
\(\widehat b_0v\) with \(v\in V\).  Let

\[
 \delta_{\widehat b}=a_1^{-1}\widehat b_0\in p^{-1}(R_S(H_0)).
\tag{4.3}
\]

Formation residuals commute with epimorphic images, so

\[
 p(R_S(H_1))=R_S(H_0).
\tag{4.3a}
\]

Consequently inclusion of \(V\) induces an isomorphism

\[
 \iota_S:V/V_S\xrightarrow{\ \sim\ }
 \frac{p^{-1}(R_S(H_0))}{R_S(H_1)}.
\tag{4.3b}
\]

Write \(\omega_S(\delta_{\widehat b})\in V/V_S\) for the inverse image of
the coset of \(\delta_{\widehat b}\) under (4.3b).

### Theorem 4.1 (RESIDUAL-SUPPORTED AFFINE FIBRE)

If one finer formation-purified lift exists, the set of all such lifts over
the fixed coarse point is a coset of \(V_S\).  Equivalently, after fixing
\(\widehat b_0\), formation purification is the finite linear condition

\[
 \boxed{v\bmod V_S=
 -\omega_S(\delta_{\widehat b})}
\tag{4.4}
\]

in \(V/V_S\), with the evident change of sign/order for a left-coordinate
convention.

#### Proof

The equality (4.3a) follows directly from (1.2): the image of the residual
is contained in the residual of the image, while the quotient by that image
belongs to \(\mathcal C_S\).  It makes (4.3b) onto; its kernel is exactly
\(V\cap R_S(H_1)=V_S\).

Two finer lifts differ by a unique element of \(V\).  In the quotient
(4.3b), the difference of \(a_1^{-1}\widehat b_0v\) from the residual is
\(\omega_S(\delta_{\widehat b})+v\bmod V_S\).  It vanishes exactly under
(4.4).  Thus the solution set is one coset of \(V_S\). \(\square\)

For the first relative Frattini window, all relation-module values and all
correction changes are linear in \(V\).  Therefore (4.4) can be appended to
the task179/v146 common-word system as separately typed quotient rows.  The
same source word must satisfy the H1, H2, pentagon, exact-commutator, and
formation-residual rows.  Solving those blocks independently is invalid.

The submodule \(V_S\) must be computed in the full joint extension
\(\mathcal H_1\), not by taking a product of ten coordinatewise residual
intersections.  Equal dimensions or hashes do not prove the subdirect
comparison.

## 5. Relative pro-3 tower has no new nonabelian chief factors

Use the iterated relative Frattini tower of v145.  For every \(n\),

\[
 \ker(E_{r,n}\to E_{r,0})=K_{r,0}/K_{r,n}
\tag{5.1}
\]

is a finite 3-group.  Consequently every chief factor introduced strictly
above the pinned level zero is an elementary abelian 3-group.  The
nonabelian composition factors of \(E_{r,n}\) are exactly those already
present in \(E_{r,0}\).

### Corollary 5.1

On this concrete relative pro-3 ladder, once the level-zero
\(PSL(2,8)\)-bearing component is fixed, every new lifting equation is an
abelian actual-class equation.  The nonlinear nonabelian accepted-set gate
does not recur inside this ladder.

This does not remove finite refinements with a new prime-to-3 or nonabelian
kernel; the relative pro-3 ladder is not cofinal among those windows.  It
does remove a falsely repeated nonabelian obligation from the internal
second-and-later Frattini rungs.

## 6. All-rung formation-purified selector

Suppose a compatible family \(b_n\) is constructed along the v145 relative
Frattini tower and, at every rung, its difference from the fixed arithmetic
component satisfies

\[
 a_n^{-1}b_n\in R_S(\mathcal H_n).
\tag{6.1}
\]

Then Corollary 2.2 produces one relative profinite word whose reductions are
the \(b_n\) and whose value equals the arithmetic word in every
\(\mathcal C_S\)-quotient.  Hence all no-\(S\) relations and automorphism
gates are inherited from arithmetic.  The remaining internal pro-3 problem
is precisely the compatible sequence of linear actual-class equations in
the residual-supported submodules \(V_{S,n}\).

Return-odd classes may use the relative-dihedral antisymmetrizer.  The
return-even field-outer survivor must be inverted inside the actual
residual-supported module; an ambient or coordinatewise inverse is not
enough.  Thus the completed homotopy sought in v127/v133 must have domain

\[
 \boxed{
 A_{\infty}^{\rm com,res}
 \longrightarrow Z_{\infty}^{\rm act,res},}
\tag{6.2}
\]

where `com` denotes exact commutator correction and `res` denotes the joint
formation residual.  V146 supplies the first restriction; (4.2)--(4.4)
supply the second.

## 7. Next finite certificate

After task184 returns an exact-commutator first-rung word, the next bounded
certificate is:

1. construct the full joint first relative Frattini extension
   \(\mathcal H_1\), including all repeated context maps;
2. construct \(R_S(\mathcal H_1)\) from the finite group itself and prove
   characteristicity and quotient membership in \(\mathcal C_S\);
3. reconstruct the fixed arithmetic component \(a_1\) in the same typed
   group;
4. test the displayed word's \(\delta_1\) by (3.2);
5. if it fails, compute \(V_S\), append the quotient rows (4.4) to the
   positive common-word solver, and retain literal word provenance; and
6. only a common word passing all relation, exact exponent, and residual
   rows is sent to v145's second-rung defect.

A bounded failure to construct \(\mathcal H_1\), its residual, or the
arithmetic comparison is `UNKNOWN_INPUT/UNKNOWN_RESOURCE`.  It is not a
formation nonmembership certificate.

```text
FORMATION KERNEL IMAGE = FINITE FORMATION RESIDUAL: PAPER_PROOF
ONE-COMPONENT PURIFICATION CRITERION:               PAPER_PROOF
COMPATIBLE PURIFICATION BY COMPACTNESS:              PAPER_PROOF
ELEMENTARY-ABELIAN RESIDUAL FIBRE = LINEAR COSET:    PAPER_PROOF
RELATIVE PRO-3 TOWER NEW CHIEF FACTORS ABELIAN:      PAPER_PROOF
FIRST JOINT RELATIVE FRATTINI GROUP H_1:             NOT CONSTRUCTED
FIRST RESIDUAL SUBMODULE V_S / R07 CLASS TEST:       NOT COMPUTED
RETURN-EVEN RESIDUAL-SUPPORTED HOMOTOPY:             OPEN
PRIME-TO-3 / NEW NONABELIAN REFINEMENTS:             OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:      NOT DECLARED
```

`R07_FORMATION_PURIFIED_RELATIVE_FRATTINI_LIFT_V147_PAPER_GRADE`
