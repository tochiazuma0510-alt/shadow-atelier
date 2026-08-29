# R07 filtered-retract saturation criterion (v326)

Author: Sol / 2026-08-29

Status: paper theorem discharging v321's same-depth saturation gate whenever
the localized residual target is the image of a filtration-preserving
module retraction.  It gives explicit projections for return eigenspaces and
for intersections of commuting split kernels.  It does not assert that the
entire formation/Brunnian R07 target is such a retract.  No compatible lift,
fake certificate or Ihara witness is declared.

## 1. A module retract is filtration-strict

Let \(\Lambda\) be a ring complete for a two-sided ideal \(J\), let \(Z\) be
a complete separated left \(\Lambda\)-module, and let \(L\leq Z\) be a
closed \(\Lambda\)-submodule.  Suppose there is a \(\Lambda\)-linear
retraction

\[
 p:Z\longrightarrow L,\qquad p|_L=1_L.
\tag{1.1}
\]

Equivalently, the composite \(e=\iota p\in\operatorname{End}_\Lambda(Z)\)
is an idempotent with image \(L\).

### Theorem 1.1 (FILTERED-RETRACT STRICTNESS)

For every \(r\geq0\),

\[
 \boxed{L\cap J^rZ=J^rL.}
\tag{1.2}
\]

Consequently every saturation kernel of v321 vanishes:

\[
 \boxed{
 (L\cap J^rZ)/J^rL=0.}
\tag{1.3}
\]

#### Proof

The inclusion \(J^rL\subseteq L\cap J^rZ\) is automatic.  Conversely let
\(z\in L\cap J^rZ\).  Since \(p\) is \(\Lambda\)-linear,

\[
 p(J^rZ)=J^rp(Z)=J^rL.
\tag{1.4}
\]

But \(p(z)=z\), so \(z\in J^rL\).  This proves (1.2), and (1.3) follows
from v321 Lemma 1.1. \(\square\)

Completeness and closedness are not needed for the equality at a fixed
depth; they are retained because v319's Newton limit needs them.  The
load-bearing property is a retraction commuting with the \(\Lambda\)-action,
not merely a vector-space complement.

## 2. Constructive intrinsic ancestry

Let

\[
 q:F=\Lambda^t\twoheadrightarrow L
\tag{2.1}
\]

be the free cover used in v319.  Suppose an ambient depth ancestry is
retained:

\[
 z=\sum_{\nu=1}^s a_\nu z_\nu,
\qquad a_\nu\in J^r,\quad z_\nu\in Z,
\qquad z\in L.
\tag{2.2}
\]

For each \(\nu\), choose \(f_\nu\in F\) with

\[
 q(f_\nu)=p(z_\nu).
\tag{2.3}
\]

Put

\[
 v=\sum_{\nu=1}^s a_\nu f_\nu\in J^rF.
\tag{2.4}
\]

### Proposition 2.1 (RETRACTED FREE-COVER CERTIFICATE)

\[
 \boxed{q(v)=z.}
\tag{2.5}
\]

#### Proof

Using (2.2), \(\Lambda\)-linearity and \(p(z)=z\),

\[
 q(v)=\sum_\nu a_\nu p(z_\nu)
     =p\left(\sum_\nu a_\nu z_\nu\right)
     =p(z)=z.
\tag{2.6}
\]

The coefficient belongs to \(J^rF\) by (2.4). \(\square\)

Thus a word-bearing retraction plus lifts of its finitely many displayed
values converts the ambient depth receipt from v252 directly into the
intrinsic coefficient demanded by v321.  No separate saturation elimination
is needed.

## 3. Return idempotents over \(\mathbf F_3\)

Assume \(k=\mathbf F_3\), \(\Lambda\) is a \(k\)-algebra, and
\(\theta:Z\to Z\) is a \(\Lambda\)-linear involution.  Since \(2\) is
invertible in \(k\), put

\[
 e_+=\frac{1+\theta}{2},\qquad
 e_-=\frac{1-\theta}{2}.
\tag{3.1}
\]

Then

\[
 e_\pm^2=e_\pm,\qquad e_+e_-=0,\qquad e_++e_-=1.
\tag{3.2}
\]

### Corollary 3.1 (RETURN-SUMMAND STRICTNESS)

The return-even and return-odd submodules

\[
 Z_+=e_+Z,\qquad Z_-=e_-Z
\tag{3.3}
\]

are filtration-strict in \(Z\):

\[
 Z_\pm\cap J^rZ=J^rZ_\pm
\quad(r\geq0).
\tag{3.4}
\]

#### Proof

Apply Theorem 1.1 to the two idempotents in (3.1). \(\square\)

This isolates an important boundary.  The relative-dihedral return split
itself creates no same-depth saturation defect when \(\theta\) is genuinely
\(\Lambda\)-linear.  Any remaining v321 defect must come from another
localization, from failure of \(\theta\)-linearity for the actual module, or
from an intersection which is not known to be a retract.

More generally, if a finite group \(Q\) of order prime to three acts
\(\Lambda\)-linearly on \(Z\), the Reynolds operator

\[
 e_Q=|Q|^{-1}\sum_{g\in Q}g
\tag{3.5}
\]

is a \(\Lambda\)-linear idempotent onto \(Z^Q\).  Hence \(Z^Q\) is
filtration-strict.  This statement concerns invariant summands; it does not
identify a formation residual with such an invariant space.

## 4. Intersections of commuting split kernels

Let

\[
 f_j:Z\longrightarrow Y_j,\qquad
 s_j:Y_j\longrightarrow Z,\qquad
 f_js_j=1_{Y_j}
\quad(1\leq j\leq t)
\tag{4.1}
\]

be \(\Lambda\)-linear split epimorphisms.  Put

\[
 e_j=1-s_jf_j.
\tag{4.2}
\]

Then \(e_j\) is an idempotent with image \(\ker f_j\).

### Theorem 4.1 (COMMUTING-KERNEL INTERSECTION)

If the \(e_j\) commute pairwise, then

\[
 e=e_1e_2\cdots e_t
\tag{4.3}
\]

is an idempotent and

\[
 \boxed{
 \operatorname{im}e=
 \bigcap_{j=1}^t\ker f_j.}
\tag{4.4}
\]

In particular, the intersection in (4.4) is filtration-strict.

#### Proof

Commutativity gives \(e^2=\prod_je_j^2=e\).  If \(z=e(w)\), then
\(e_jz=z\) for every \(j\), so \(z\in\operatorname{im}e_j=\ker f_j\).
Conversely, if \(z\in\bigcap_j\ker f_j\), then \(e_jz=z\) for every \(j\),
and hence \(e(z)=z\).  This proves (4.4); Theorem 1.1 gives strictness.
\(\square\)

Face/deletion maps with authenticated degeneracy sections give individual
split kernels.  To apply Theorem 4.1 to a Brunnian intersection one must
also replay commutativity of the resulting idempotents, or supply a separate
normalized projection onto the whole intersection.  Simplicial slogans
alone do not establish (4.3) for the exact occurrence-tagged R07 maps.

## 5. Nested retracts

Suppose

\[
 L_2\subseteq L_1\subseteq Z
\tag{5.1}
\]

and there are \(\Lambda\)-linear retractions

\[
 p_1:Z\to L_1,\qquad p_2:L_1\to L_2.
\tag{5.2}
\]

### Corollary 5.1 (COMPOSED LOCALIZATION RETRACT)

\[
 p_2p_1:Z\longrightarrow L_2
\tag{5.3}
\]

is a retraction.  Hence \(L_2\) is filtration-strict in \(Z\).

This is the clean structural route for a doubly localized target: first
retract onto one localization, then retract its intersection target inside
that localization.  Merely knowing both submodules separately split in
\(Z\) is insufficient unless the projections commute or preserve the other
submodule.

## 6. Natural towers and Newton completion

Let all data carry a cofinal level \(n\).  If the retractions \(p_n\), free
covers \(q_n\), and chosen lifts in Proposition 2.1 commute with reduction,
then the intrinsic ancestries (2.4) commute with reduction.  Under v319's
leading based surjectivity and v320's transport hypotheses, v252's ambient
one-depth gain may then be iterated without a separate saturation gate.

Even without natural chosen lifts, Theorem 1.1 proves same-depth
nonemptiness at every finite level.  A constructive all-edge formula still
requires compatible choices or an appropriate finite-fibre compactness
argument including the nonlinear accepted conditions.

## 7. R07 application boundary

For v321's target

\[
 L\subseteq
 R_S(G_{H1})\times R_S(G_{H2})\times
 (B_P\cap R_S(G_P)),
\tag{7.1}
\]

the saturation gate is discharged by any one of the following authenticated
structures:

1. one \(\Lambda\)-linear idempotent on the ambient residual module with
   image exactly \(L\);
2. a chain of nested retractions ending in \(L\);
3. commuting split-kernel idempotents whose common image is \(L\); or
4. the pointed v321 ancestry for each actual remainder.

Corollary 3.1 handles a genuine return eigenspace automatically.  It does
not prove that \(R_S(G)\), \(B_P\), their intersection, or the common-word
joint image is a retract.  Those exact identifications are the remaining
structural question.

The finite certificate for a proposed retract records:

1. its matrix or word-bearing formula;
2. \(\Lambda\)-linearity on generators;
3. idempotence;
4. equality of its image with the exact localized target;
5. commutation with reduction and return where claimed; and
6. direct reconstruction of Proposition 2.1's intrinsic coefficient.

A projection onto a larger convenient space does not discharge saturation
for a smaller unsplit target.

## 8. Fixed frontier

Filtered-retract strictness, constructive intrinsic ancestry, return
eigenspace strictness, commuting-kernel intersections and nested retractions
are paper proofs.  The actual formation/Brunnian/common-word localized
retraction is not constructed.  The actual class-two remainder saturation
class is not computed.  A compatible cofinal lift, fake certificate and
Ihara witness remain absent.

R07_FILTERED_RETRACT_SATURATION_V326_PAPER_GRADE
