# R07 structural discharge of HT1, HT2 and the residual part of HT5 v99

Author: Sol / 2026-08-26

Status: paper proof for a nested matched normal diagram-chief ladder.
It identifies which parts of the v82 A.18-Hensel package are formal word-level
consequences and which part is still the genuine lifting obstruction.  It does
not prove that the actual defect belongs to the actual correction image, does
not solve a nonabelian chief edge, and does not declare an Ihara witness.
`verified=false`.

## 1. Actual finite diagrams, not a universal rank model

Fix a nested cofinal system of finite matched arity-3/4/5 normal
diagrams

\[
 \mathcal D_{n+1}\longrightarrow\mathcal D_n
\tag{1.1}
\]

as supplied by v71, Theorem 2.1.  Refine every finite transition by a
diagram-chief chain.  At an abelian edge write its kernel diagram additively
as \(V_n\).  Let \(C_n\) be the **actual** image in \(V_n\) of the common-word
transition kernel, intersected with the commutator/relative-formation domain
required by R07.  No assertion that \(C_n\) is a free module of a prescribed
rank is made.

For a partial R07 word \(F_n\), let

\[
 \Omega_n(F_n)=(H_{1,n}(F_n),H_{2,n}(F_n),P_n(F_n))
 \in R_n
\tag{1.2}
\]

be the residual of the two printed hexagons and the printed-order five-coface
A.18 word.  Here \(R_n\) is the actual residual subquotient of the matched
diagram.  Alternatively, replace the third entry by the cyclic rho residual;
v96 gives the natural integral shear between the two stacks.

Fix one multiplication convention and write \(F_n\star c\) for the corrected
word: it means \(cF_n\) in the left convention and \(F_nc\) in the right
convention.  The two conventions are related by v93 and will not be mixed.

The distinction from v82's convenient universal model is load-bearing:
the present note proves formal properties of the actual modules
\(C_n,R_n\).  It does not assert the universal splitting or exactness called
HT3 in v82.

## 2. Exact affine linearization at every abelian edge

### Theorem 2.1 (STRUCTURAL-HT1)

There is a canonical linear map

\[
 D_n:C_n\longrightarrow R_n
\tag{2.1}
\]

such that, for every actual correction value \(c\in C_n\),

\[
 \boxed{\Omega_n(F_n\star c)=\beta_n+D_nc,\qquad
 \beta_n:=\Omega_n(F_n).}
\tag{2.2}
\]

The formula is exact in the abelian chief kernel and is defined before a
successful fine lift exists.  Under the left-correction convention its A.18
row is the literal v71 formula

\[
 \lambda_1+q_1\lambda_2+q_1q_2\lambda_3
 -q_1q_2q_3q_5^{-1}\lambda_5-\lambda_4,
\tag{2.3}
\]

with the corresponding exact Fox rows for the two hexagons.  The
right-correction convention is obtained by the exact base-change of v93.

#### Proof

Choose arbitrary set-theoretic lifts of the coarse marked generators.  Every
printed relator evaluates in the abelian normal kernel \(V_n\).  Replacing a
lifted generator by a kernel correction and collecting the correction terms
gives its Fox derivative with coefficients evaluated in the coarse quotient.
The coefficient transports depend only on coarse prefixes, while all kernel
terms commute.  Hence the Fox formula is an equality, not an associated-graded
approximation.  Restricting the resulting map to the actual common-word domain
gives (2.1)--(2.2).  Applying this to the five factors in printed A.18 order
gives (2.3), exactly as in v71 (3.3)--(3.7).  No fine solution was used.
\(\square\)

Thus HT1 is not a new all-stage existence hypothesis once the matched
diagram-chief ladder and the actual correction domain have been fixed.  What
remains open is whether \(-\beta_n\) lies in \(D_n(C_n)\).

## 3. Literal identities give closedness at every edge

Let \(\mathcal S\) be any fixed finite roster of literal identities among the
two hexagon and A.18 relator words, including the typed associahedral boundary
identities used at arity five.  Collecting the residuals in each identity
defines a linear syzygy map

\[
 E_n:R_n\longrightarrow S_n.
\tag{3.1}
\]

### Theorem 3.1 (STRUCTURAL-HT2)

For every abelian diagram-chief edge,

\[
 \boxed{E_nD_n=0,\qquad E_n\beta_n=0.}
\tag{3.2}
\]

These equalities do not assume the existence of a fine lift.

#### Proof

Evaluate each literal identity in \(\mathcal S\) on the arbitrary lifted
coarse solution.  Its relators take values in the abelian kernel, so collection
is linear and the identity gives \(E_n\beta_n=0\).  Evaluate the same identity
after an arbitrary common-word correction and subtract the first equality.
Theorem 2.1 gives \(E_nD_n=0\).  This is v71 (4.1)--(4.3), restricted to the
actual R07 domain. \(\square\)

The theorem proves closedness for the authenticated literal syzygy roster.  It
does not prove

\[
 \ker E_n=\operatorname{im}D_n.
\tag{3.3}
\]

Equation (3.3), or the weaker assertion that the particular \(\beta_n\) is in
the image, is precisely the remaining abelian obstruction.

## 4. Refinement naturality is formal on residuals and Jacobians

Let \(q_{mn}:\mathcal D_m\to\mathcal D_n\) be a refinement map, \(m\ge n\).
Consider an abelian occurrence at level \(m\) which maps to the selected typed
occurrence at level \(n\) (or its induced subquotient), and use the resulting
maps on the actual correction, residual and syzygy modules.  No comparison is
asserted between unrelated chief edges.

### Theorem 4.1 (STRUCTURAL-HT5)

The word residuals, their affine Jacobians, and the literal syzygy maps commute
with refinement:

\[
\begin{aligned}
 q_{mn}\beta_m&=\beta_n,\\
 q_{mn}D_m&=D_nq_{mn},\\
 q_{mn}E_m&=E_nq_{mn}.
\end{aligned}
\tag{4.1}
\]

The same is true for the simultaneous theta/rho stack, and v96's shear
\(T_A\) intertwines (4.1).  The commutator and relative-formation correction
domains map into their coarse counterparts.

#### Proof

Every residual and syzygy in question is evaluation of one fixed signed word
in the matched diagram.  Group homomorphisms commute with word evaluation,
coface maps and deletion maps by construction of the normal diagram.  Fox
coefficients reduce with their coarse prefixes, proving the middle equality.
Functoriality of commutators and of formation residuals proves the domain
statement.  For theta/rho versus printed A.18, v96 (3.2)--(3.3) gives
\(q_{mn}A_m=A_nq_{mn}\), hence \(q_{mn}T_{A_m}=T_{A_n}q_{mn}\).
\(\square\)

This discharges the residual/matrix part of HT5.  It does **not** manufacture
a natural right inverse to \(D_n\), and it does not say that an arbitrary
finite linear solution lies in the actual common-word image or passes a split
onto gate.

## 5. The only abelian selector theorem still needed

Suppose one constructs maps on the actual closed defect subsystem

\[
 h_n:Z_n^{\rm act}\longrightarrow C_n,
 \qquad Z_n^{\rm act}\subseteq\ker E_n,
\tag{5.1}
\]

such that

\[
 D_nh_n=1\quad\hbox{on }Z_n^{\rm act},
 \qquad q_{mn}h_m=h_nq_{mn},
 \qquad \beta_n\in Z_n^{\rm act}.
\tag{5.2}
\]

Then \(d_n=-h_n(\beta_n)\) is the all-stage actual correction value.  V96
transports a theta/rho version of \(h_n\) to printed A.18.  V98 then chooses a
deterministic ordinary commutator word representing each \(d_n\) in the
accumulated kernel and proves convergence of the infinite product.  Therefore
no further naturality of word spellings is required.

Consequently the abelian frontier is the single class-specific statement

\[
 \boxed{\text{construct (5.1)--(5.2) for the actual R07 defect at every
 active abelian edge}.}
\tag{5.3}
\]

The pure dihedral antisymmetrizer supplies part of such a map on the
return-odd block.  The return-even field-outer/full-pair component is not
killed by the present formal argument and remains the substantive target.

## 6. Updated ledger

```text
MATCHED DIAGRAM-CHIEF LADDER:                 PAPER_PROOF (v71)
ACTUAL AFFINE WORD LINEARIZATION / HT1-STRUCT: PAPER_PROOF (Theorem 2.1)
LITERAL SYZYGY CLOSEDNESS / HT2-STRUCT:        PAPER_PROOF (Theorem 3.1)
RESIDUAL/JACOBIAN BASE CHANGE / HT5-STRUCT:   PAPER_PROOF (Theorem 4.1)
RHO TO PRINTED A18 NATURAL SHEAR:              PAPER_PROOF (v96)
COMPATIBLE WORD SPELLING:                     PAPER_PROOF (v98)
UNIFORM ACTUAL-IMAGE CONTRACTION (5.3):       OPEN
ADMISSIBLE SIDE-GATE VALUE AT EVERY EDGE:     OPEN
NONABELIAN ACCEPTED-SET NONEMPTINESS:          OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT YET CONSTRUCTED
IHARA WITNESS:                                NOT DECLARED
```

No finite computation, external source, or Lean proof is used in this note.
