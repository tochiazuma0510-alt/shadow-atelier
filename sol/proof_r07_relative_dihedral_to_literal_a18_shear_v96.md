# R07 relative-dihedral to literal A.18 shear v96

Author: Sol / 2026-08-26

Status: exact paper proof for one abelian diagram-chief edge, natural under
refinement.  It supplies a lossless bridge from the simultaneous
theta/rho residual system to the literal printed-order A.18 residual.  It
does not prove that the theta/rho system is solvable at every edge and does
not declare a cofinal lift or Ihara witness.  `verified=false`.

## 1. Exact group identity and the abelian edge

Let $f\in[F_2,F_2]$.  Use the words of v47:

\[
\begin{aligned}
R_\rho(f)&=
 f(x_{34},x_{45})f(x_{15},x_{12})f(x_{23},x_{34})
 f(x_{45},x_{15})f(x_{12},x_{23}),\\
C(f)&=C_{A18}(f),\\
H_1(f)&=f(x_{34},x_{45})f(x_{45},x_{34}),\\
H_2(f)&=f(x_{15},x_{12})f(x_{12},x_{15}),\\
a(f)&=f(x_{45},x_{34})^{-1}.
\end{aligned}
\tag{1.1}
\]

Here $C(f)$ is the right-inverse-left defect of the literal printed A.18
equation.  V47 proves the unconditional identity

\[
\boxed{
R_\rho(f)C(f)^{-1}
=H_1(f)a(f)H_2(f)a(f)^{-1}.}
\tag{1.2}
\]

Now let

\[
1\longrightarrow V\longrightarrow \widetilde Q
\longrightarrow Q\longrightarrow1
\tag{1.3}
\]

be one abelian diagram-chief edge at the arity-four component.  Write $V$
additively.  Suppose the image of a coarse word $f_0$ satisfies the two
source symmetry relations and both pentagon forms in $Q$.  Then the four
defects in (1.1) lie in $V$.  Put

\[
h_i=H_i(f_0),\qquad r=R_\rho(f_0),\qquad c=C(f_0),
\qquad A=\operatorname{Ad}(\overline{a(f_0)})|_V.
\tag{1.4}
\]

The action $A\in\operatorname{Aut}(V)$ is determined by the coarse value,
so it is defined before a lift through (1.3) is known.

### Theorem 1.1 (REL-DIH-A18-SHEAR)

At the abelian edge (1.3),

\[
\boxed{c=r-h_1-Ah_2.}
\tag{1.5}
\]

Equivalently, for the two residual stacks

\[
\omega_\rho=(h_1,h_2,r),\qquad
\omega_{A18}=(h_1,h_2,c),
\tag{1.6}
\]

one has

\[
\boxed{
\omega_{A18}=T_A\omega_\rho,
\qquad
T_A=
\begin{pmatrix}
1&0&0\\
0&1&0\\
-1&-A&1
\end{pmatrix}.}
\tag{1.7}
\]

The shear is invertible over every characteristic:

\[
T_A^{-1}=
\begin{pmatrix}
1&0&0\\
0&1&0\\
1&A&1
\end{pmatrix}.
\tag{1.8}
\]

#### Proof

All four defects have trivial image in $Q$, hence belong to the abelian
normal subgroup $V$.  In (1.2), multiplication in $V$ becomes addition,
inverse becomes negation, and conjugation by $a(f_0)$ becomes the coarse
action $A$.  Thus

\[
r-c=h_1+Ah_2,
\]

which is (1.5).  The two displayed block matrices are visibly mutual
inverses.  No division or averaging is used.  \(\square\)

## 2. Exact affine Jacobian comparison

Let $U$ be the common-word correction module at this edge.  Corrections
may be multiplied on either fixed side, but one convention is fixed.  For
$v\in U$, the corrected word has the same coarse image as $f_0$.  Hence
the coarse element $\overline{a(f_0)}$, and therefore $A$, is constant
throughout the affine fibre.

Write the four exact affine residuals as

\[
H_i(f_v)=h_i+D_{H_i}v,\qquad
R_\rho(f_v)=r+D_\rho v,\qquad
C(f_v)=c+D_{A18}v.
\tag{2.1}
\]

### Theorem 2.1 (JACOBIAN-SHEAR)

The literal A.18 Jacobian is recovered from the simultaneous
relative-dihedral/rho Jacobian by

\[
\boxed{D_{A18}=D_\rho-D_{H_1}-A D_{H_2}.}
\tag{2.2}
\]

For the stacked matrices

\[
D_\rho^{\rm stack}=
\begin{pmatrix}D_{H_1}\\D_{H_2}\\D_\rho\end{pmatrix},
\qquad
D_{A18}^{\rm stack}=
\begin{pmatrix}D_{H_1}\\D_{H_2}\\D_{A18}\end{pmatrix},
\tag{2.3}
\]

one has the exact equality

\[
\boxed{D_{A18}^{\rm stack}=T_A D_\rho^{\rm stack}.}
\tag{2.4}
\]

#### Proof

Apply the group identity (1.2) to every corrected word $f_v$.  Its coarse
image is fixed, so collection in $V$ gives

\[
c+D_{A18}v
=(r+D_\rho v)-(h_1+D_{H_1}v)-A(h_2+D_{H_2}v).
\]

The constant term is Theorem 1.1.  Subtracting it gives (2.2), hence
(2.4).  The possible variation of the word $a(f_v)$ contributes no extra
term: in the quotient its conjugated factor $H_2(f_v)$ has coarse value
one, and collection in an abelian kernel depends only on the coarse
conjugator.  \(\square\)

### Corollary 2.2 (solution-set equivalence)

The simultaneous systems

\[
H_1=H_2=R_\rho=1
\quad\text{and}\quad
H_1=H_2=C_{A18}=1
\tag{2.5}
\]

have exactly the same correction solutions.  In particular, after the
source symmetry row is killed, the rho and literal A.18 residuals and their
Jacobians agree under the displayed shear.  This is an equality of the
actual affine fibres, not merely equality of ranks or associated-graded
dimensions.

## 3. Naturality through an inverse system

Let a finer edge $j$ reduce to a coarser edge $i$, with compatible maps

\[
q_{ji}:V_j\longrightarrow V_i.
\tag{3.1}
\]

All words in (1.1) are literal and all structural maps belong to the matched
diagram.  Therefore their residuals reduce naturally.  The coarse
conjugators also reduce, so

\[
q_{ji}A_j=A_iq_{ji}.
\tag{3.2}
\]

### Theorem 3.1 (NATURAL-SHEAR)

The shears commute with every refinement map:

\[
\boxed{q_{ji}T_{A_j}=T_{A_i}q_{ji}.}
\tag{3.3}
\]

Consequently a natural contraction $S_\rho$ for the simultaneous
theta/rho system gives a natural literal A.18 contraction

\[
\boxed{S_{A18}=S_\rho T_A^{-1}.}
\tag{3.4}
\]

#### Proof

Equation (3.3) follows entrywise from (3.2); the other entries of $T_A$
are $0,1,-1$.  If $D_\rho^{\rm stack}S_\rho$ is the identity on the
typed closed residual subspace, (2.4) gives

\[
D_{A18}^{\rm stack}S_\rho T_A^{-1}
=T_AD_\rho^{\rm stack}S_\rho T_A^{-1}=1.
\]

Compatibility follows from (3.3) and the assumed naturality of
$S_\rho$.  \(\square\)

This is the precise sense in which a relative-dihedral theorem can make an
explicit all-stage literal lift easier: the pentagon conversion itself is
a natural integral shear.  The remaining difficulty is the existence and
admissible word realization of $S_\rho$ on the actual residual-bearing
class, not any extra pentagon denominator.

## 4. Application to the 760-letter base

The fixed word

\[
g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108}
\tag{4.1}
\]

has exponent sums $(0,0)$, hence belongs to $[F_2,F_2]$.  Its current
settled E4 image satisfies both hexagons and the printed ordered A.18
relation.  Therefore Theorems 1.1--3.1 apply at its first abelian
diagram-chief refinement.

There are now two independent ways to construct the missing actual matrix:

1. build the five literal coface maps and use v71 formula (3.5);
2. build the two substituted theta words and the cyclic rho word, then use
   (2.2).

A finite receipt should construct both paths from $g_{760}$, require exact
matrix/RHS equality, and destroy the equality by mutating one coface order,
one inverse, and the action $A$.  This is a genuine chain comparison for
the relevant residual stack.  It does **not** identify the current
left-Fox target6 presentation complex with literal A.18.

The current target6/L3 gate remains useful independently: a complete
nonmembership for even one hexagon coordinate kills this explicit base
before the pentagon calculation.  If that gate is passed, (2.2) is the next
construction to run.

## 5. Fixed boundary

```text
GROUP-LEVEL RHO/LITERAL IDENTITY:             PAPER_PROOF (v47)
ABELIAN-CHIEF RESIDUAL SHEAR:                 PAPER_PROOF
ABELIAN-CHIEF JACOBIAN SHEAR:                 PAPER_PROOF
REFINEMENT NATURALITY OF THE SHEAR:           PAPER_PROOF
g760 APPLICABILITY (COMMUTATOR + COARSE REL): CANDIDATE/CROSS-CHECK INPUT
g760 FIRST TARGET6 FULL-LEGAL GATE:            IN PROGRESS
g760 ACTUAL A18 MATRIX/RHS DOUBLE BUILD:       NOT YET COMPUTED
NATURAL THETA/RHO CONTRACTOR ON ACTUAL CLASS: OPEN
ADMISSIBLE WORD SECTION AT ALL EDGES:         OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT YET CONSTRUCTED
IHARA WITNESS:                                NOT DECLARED
```

No finite computation, external source or Lean proof is used in this note.
