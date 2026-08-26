# R07 affine residual-torsor criterion for the composition receipt v104

Author: Sol / 2026-08-26

Status: paper proof of a sufficient, finitely checkable criterion for the
`DEFECT-1-TYPED` hypothesis of v103.  It reduces the missing composition
law to one affine action on the complete actual relation-residual module.
The affine action, the completeness of its relation roster, and its R07
occurrence have not yet been constructed.  This note does not construct a
fine successor, a cofinal lift, or an Ihara witness.  `verified=false`.

## 1. The correct object is an affine action

Fix one abelian matched diagram-chief edge.  Let

\[
 1\longrightarrow C\longrightarrow \mathcal E_{\rm raw}
 \xrightarrow{\pi}P\longrightarrow1
\tag{1.1}
\]

be a typed raw-lift group.  Here (C) is the **actual allowed common-word
correction kernel**, after intersecting with the commutator, relative, and
finite side-gate domains.  Let (R_{\rm cl}) be the complete closed
relation-residual module, with a displayed (P)-action, and let

\[
 D:C\longrightarrow R_{\rm cl}
\tag{1.2}
\]

be the exact affine Jacobian of v99.

Write the affine group with the convention

\[
 (r,p)(s,q)=(r+p s,pq)
 \qquad(r,s\in R_{\rm cl},\ p,q\in P).
\tag{1.3}
\]

Say that the edge is `AFFINE-RESIDUAL-TYPED` if there is a homomorphism

\[
 \Phi:\mathcal E_{\rm raw}\longrightarrow
 R_{\rm cl}\rtimes P
\tag{1.4}
\]

such that

\[
 \operatorname{pr}_P\Phi=\pi,
 \qquad
 \Phi(c)=(D c,1)\quad(c\in C),
\tag{1.5}
\]

and, on this typed edge, an element (a c) is an admissible fine lift
exactly when the translation coordinate of \(\Phi(a c)\) is zero.  Thus all
relations and linear side gates are included in (R_{\rm cl}); a partial
or over-approximating residual roster does not satisfy the definition.

The map (1.4) is the action on the relation-residual torsor.  It is stronger
than a rank equality but much smaller than a table on
\(\mathcal E_{\rm raw}\times\mathcal E_{\rm raw}\).

## 2. The affine criterion proves the v103 typing

### Theorem 2.1 (AFFINE TORSOR IMPLIES DEFECT ONE-COCYCLE)

Every `AFFINE-RESIDUAL-TYPED` edge is `DEFECT-1-TYPED` in the sense of
v103.  More explicitly, if

\[
 \Phi(a)=(\Omega(a),\pi(a)),
 \qquad M=R_{\rm cl}/D(C),
\tag{2.1}
\]

then (D(C)) is (P)-stable and

\[
 o(p)=[\Omega(a)]\quad(\pi(a)=p)
\tag{2.2}
\]

is a well-defined crossed homomorphism

\[
 \boxed{o(pq)=o(p)+p\,o(q).}
\tag{2.3}
\]

A fixed coarse point (p) has an admissible successor if and only if

\[
 \boxed{o(p)=0.}
\tag{2.4}
\]

#### Proof

For (a,b\in\mathcal E_{\rm raw}), the homomorphism property and (1.3)
give the exact identity

\[
 \Omega(ab)=\Omega(a)+\pi(a)\Omega(b).
\tag{2.5}
\]

Since (C\lhd\mathcal E_{\rm raw}), equations (1.4)--(1.5) applied to
\(a c a^{-1}\) give

\[
 D(a c a^{-1})=\pi(a)D(c).
\tag{2.6}
\]

Hence (D(C)) is (P)-stable.  If (a') is another raw lift of
\(p=\pi(a)\), then (a'=a c) for some (c\in C), and

\[
 \Omega(a c)=\Omega(a)+pD(c).
\tag{2.7}
\]

Thus (2.2) is independent of the raw lift.  Reducing (2.5) modulo (D(C))
proves (2.3).

Finally, a right correction exists precisely when there is (c\in C)
with

\[
 0=\Omega(a c)=\Omega(a)+pD(c).
\tag{2.8}
\]

By (P)-stability of (D(C)), equation (2.8) is soluble precisely when
\(\Omega(a)\in D(C)\), which is (2.4).  The last clause of
`AFFINE-RESIDUAL-TYPED` converts zero translation into the complete
admissibility statement. \(\square\)

This theorem isolates two logically different checks:

1. the affine multiplication law (2.5);
2. completeness of the zero residual as the fine relation and side-gate
   condition.

Neither follows merely from the other.

## 3. Why word substitution naturally has this form

Let \(\mathscr T\) be the torsor of marked values of the complete relator
roster at the fine edge, based at the zero residual.  A typed raw
automorphism acts on marked relator values by substitution and transport.
At an abelian kernel, collection is affine: the linear part depends only on
the coarse automorphism, while the displacement is the residual of the raw
lift.  Therefore an authenticated action

\[
 \mathcal E_{\rm raw}\curvearrowright\mathscr T
\tag{3.1}
\]

in which the linear part factors through (P) gives (1.4) after choosing
the zero basepoint.

This observation is not yet the R07 occurrence.  To use it one must retain
the two printed hexagons, the printed-order five-coface A.18 word (or the
losslessly sheared theta/rho stack), all syzygy coordinates needed for
closedness, and all linear side gates.  One must then prove that substitution
by each raw generator sends this roster back into the displayed closed
roster.  Omitting a relation can create a spurious affine action on a
quotient and is not sound for positive lifting.

V99 supplies the exact affine correction rows and refinement naturality.
V96 supplies an invertible shear between the simultaneous theta/rho and
literal A.18 coordinates.  Neither paper by itself supplies the closure of
the complete roster under every generator of \(\mathcal E_{\rm raw}\); that
closure is the remaining occurrence check.

## 4. A finite generator-relator certificate

Suppose

\[
 \mathcal E_{\rm raw}
 =\langle e_1,\ldots,e_d\mid s_1,\ldots,s_m\rangle
\tag{4.1}
\]

is a based presentation.  Assign to every generator a proposed affine
matrix

\[
 e_i\longmapsto (b_i,A_i)\in R_{\rm cl}\rtimes P.
\tag{4.2}
\]

The signed-word replay in the semidirect product (1.3) is deterministic.

### Proposition 4.1 (FINITE AFFINE-ACTION RECEIPT)

The assignments (4.2) define the homomorphism (1.4) if and only if:

\[
 A_i=\pi(e_i)\quad(1\le i\le d),
 \qquad
 (b,A)(s_j)=(0,1)\quad(1\le j\le m).
\tag{4.3}
\]

If displayed generators (c_k) generate (C) as the required normal
correction kernel, then (1.5) is certified by

\[
 \Phi(c_k)=(D c_k,1)
\tag{4.4}
\]

together with an exact kernel/normal-generation receipt.

#### Proof

The free group on the (e_i) has a unique homomorphism to the affine group
with the values (4.2).  It factors through (4.1) exactly when every defining
relator maps to the identity, which is (4.3).  Equation (4.4), normal
generation, and conjugation in the affine group then give (1.5) on all of
(C). \(\square\)

Thus no (243^2) composition table is required.  A finite actual receipt
may contain:

1. the based raw presentation and its quotient map to the frozen (P_0);
2. the three coarse generator actions on the complete residual module;
3. the corresponding residual displacements (b_i);
4. every raw presentation-relator replay in the affine group;
5. correction-kernel generators, their (D)-columns, and the
   kernel/normal-generation proof;
6. a zero-residual completeness replay for the two hexagons, A.18, and all
   side gates;
7. the row36 word and return replay used in v103.

The presentation and completeness statements are load-bearing.  Testing a
few products of generators is only a canary and cannot replace (4.3).

## 5. Index-three and return consequence

Assume the pointwise arithmetic subgroup (H\lhd P) survives the edge and
(P/H\cong C_3).  Theorem 2.1 and v103 then put the selected return-fixed
R07 value in

\[
 \boxed{
 o(g)\in
 M^H\cap\ker(1+q+q^2)\cap M^S.}
\tag{5.1}
\]

Consequently the uniform relative-dihedral successor is reduced to one of
the two exact alternatives

\[
 M^H\cap\ker(1+q+q^2)\cap M^S=0,
\tag{5.2}
\]

or a direct affine-word evaluation proving (o(g)=0).  This is an
individual-lift (Z^1) statement.  It neither uses nor identifies the
unrelated roof-(C_9) extension class of v101--v102.

## 6. Refinement and the all-stage boundary

For matched refinements, the affine receipts must commute with the maps on
raw lifts, corrections, and complete residual modules.  If they do, the
cocycles and quotients of Theorem 2.1 form the compatible system of v103.
At every abelian edge, (5.2) or the class-specific zero then gives an actual
correction value; v98 materializes it as an ordinary commutator word and
assembles the convergent product.

The remaining work is therefore not a compatible choice of finite words.
It is:

\[
 \boxed{
 \text{construct the actual affine residual action and prove the selected
 return-even evaluation vanishes at every active edge}.}
\tag{6.1}
\]

Nonabelian accepted-set nonemptiness remains separate.

## 7. Fixed ledger

```text
AFFINE TORSOR => DEFECT-1-TYPED:                 PAPER_PROOF
FINITE GENERATOR-RELATOR AFFINE RECEIPT:         PAPER_PROOF
V99 AFFINE CORRECTION/JACOBIAN ROWS:             PAPER_PROOF
V96 THETA/RHO <-> LITERAL A18 SHEAR:             PAPER_PROOF
ACTUAL RAW PRESENTATION / SURJECTIVITY:           OPEN
COMPLETE R07 RELATION-TORSOR CLOSURE:             OPEN
ACTUAL CORRECTION-KERNEL NORMAL GENERATION:       OPEN
UNIFORM RETURN-EVEN INTERSECTION VANISHING:       OPEN
CLASS-SPECIFIC ACTUAL o_n(g_n)=0:                 OPEN
NONABELIAN ACCEPTED-SET NONEMPTINESS:             OPEN
COMPATIBLE COFINAL R07 LIFT:                      NOT CONSTRUCTED
FAKE CERTIFICATE / IHARA WITNESS:                 NOT DECLARED
```

No finite computation, external source, or Lean proof is used in this note.
