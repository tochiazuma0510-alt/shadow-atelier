# R07 formation residual by extension descent v148

Author: Sol / 2026-08-27

Status: paper theorem and finite computation contract.  V147 reduces the
formation-purified first-rung problem to the submodule
\(V_S=V\cap R_S(H)\) in an elementary-abelian extension.  This note
characterizes \(V_S\) intrinsically by descent of the extension class.  It
explains the exact class which the return-even field-outer calculation must
test.  The R07 extension cocycle and its class have not yet been computed.
No cofinal lift, fake, or Ihara witness is declared.

## 1. One elementary-abelian extension

Let

\[
 1\longrightarrow V\longrightarrow H
 \stackrel{p}{\longrightarrow}E\longrightarrow1
\tag{1.1}
\]

be a finite extension, where \(V\) is an elementary abelian 3-group.  Thus
\(V\) is an \(\mathbf F_3[E]\)-module.  Put

\[
 R=R_S(E),\qquad C=E/R,
\tag{1.2}
\]

for \(S=PSL(2,8)\), and let

\[
 \xi_H\in H^2(E,V)
\tag{1.3}
\]

be the extension class for the action induced by (1.1).

For an \(E\)-submodule \(N\leq V\), put \(W=V/N\), and let
\(\xi_W\in H^2(E,W)\) be the pushed-forward class.

## 2. Which quotient of V survives outside the formation residual

### Theorem 2.1 (EXTENSION-DESCENT CRITERION)

The following are equivalent.

1. There are an extension

   \[
   1\to W\to Q\to C\to1
   \tag{2.1}
   \]

   and an epimorphism \(H\twoheadrightarrow Q\) whose maps on kernel and
   quotient are respectively \(V\twoheadrightarrow W\) and
   \(E\twoheadrightarrow C\).
2. Both of the following hold:

   \[
   R\text{ acts trivially on }W,
   \tag{2.2}
   \]

   and

   \[
   \boxed{
   \xi_W\in\operatorname{im}\left(
   \operatorname{Inf}:H^2(C,W)\to H^2(E,W)
   \right).}
   \tag{2.3}
   \]

#### Proof

If (2.1) and the extension morphism exist, the \(E\)-action on \(W\)
factors through \(C\), proving (2.2).  Pulling the lower extension back
along \(E\twoheadrightarrow C\) gives the pushout of (1.1) along
\(V\twoheadrightarrow W\).  Classification of extensions with fixed action
therefore gives (2.3).

Conversely, (2.2) makes \(W\) a \(C\)-module.  Choose a class
\(\bar\xi\in H^2(C,W)\) inflating to \(\xi_W\), and realize it by an
extension (2.1).  The pushout of (1.1) along \(V\twoheadrightarrow W\) is an
extension of \(E\) by \(W\) with class \(\xi_W\).  Equality of extension
classes identifies it with the pullback of (2.1) along \(E\twoheadrightarrow
C\).  Projection from that pullback to \(Q\), composed with the pushout map
from \(H\), is the required epimorphism.
\(\square\)

The theorem is about the actual extension class.  Knowing only the
\(E\)-module \(V\), its dimensions, or its return decomposition does not
decide (2.3).

### Theorem 2.2 (MAXIMAL DESCENDED QUOTIENT)

Put

\[
 V_S=V\cap R_S(H),\qquad W_{max}=V/V_S.
\tag{2.4}
\]

Then \(W_{\max}\) satisfies Theorem 2.1 and is maximal among all quotients
\(W=V/N\) satisfying it.  Equivalently,

\[
 \boxed{
 V_S=\min\left\{N\leq_E V:
 \begin{array}{l}
 R\text{ acts trivially on }V/N,\\
 \xi_{V/N}\text{ inflates from }H^2(C,V/N)
 \end{array}
 \right\}.}
\tag{2.5}

Here minimum means containment: \(V_S\) is contained in every admissible
\(N\).

#### Proof

V147 proves that formation residuals commute with epimorphic images, hence

\[
 p(R_S(H))=R_S(E)=R.
\tag{2.6}
\]

The quotient \(H/R_S(H)\) belongs to \(\mathcal C_S\) and fits into

\[
 1\to V/V_S\to H/R_S(H)\to E/R\to1.
\tag{2.7}
\]

Indeed, (2.6) gives
\(p^{-1}(R)=V R_S(H)\), so the kernel over \(E/R\) is exactly
\(V/(V\cap R_S(H))\).  Therefore \(W_{\max}\) satisfies Theorem 2.1.

If \(N\) satisfies Theorem 2.1, the resulting \(Q\) has composition factors
those of \(C\) and the elementary-abelian group \(W\), so
\(Q\in\mathcal C_S\).  By definition, every map from \(H\) to a
\(\mathcal C_S\)-group kills \(R_S(H)\).  Its restriction to \(V\) thus
kills \(V_S\), proving \(V_S\leq N\). \(\square\)

This proves uniqueness of the largest formation-visible quotient without
enumerating competing complements or choosing a section of (1.1).

## 3. Literal cocycle equation

Choose a normalized section \(s:E\to H\), and let

\[
 \alpha(g,h)=s(g)s(h)s(gh)^{-1}\in V
\tag{3.1}
\]

be its normalized 2-cocycle.  Let \(\pi:V\to W=V/N\), and assume (2.2).

### Proposition 3.1 (FINITE DESCENT SYSTEM)

Condition (2.3) holds if and only if there are a normalized 1-cochain
\(b:E\to W\) and a normalized 2-cocycle
\(\bar\alpha:C\times C\to W\) satisfying, for every \(g,h\in E\),

\[
 \boxed{
 \pi\alpha(g,h)
 +b(g)+g\,b(h)-b(gh)
 =\bar\alpha(\bar g,\bar h).}
\tag{3.2}
\]

All terms are linear over \(\mathbf F_3\).  Hence, for a fixed candidate
submodule \(N\), (2.2)--(2.3) are decided by one finite linear system with
complete cochain provenance.

#### Proof

Changing the section of the pushed-out extension by the 1-cochain \(b\)
changes its cocycle by the displayed coboundary.  It is inflated from a
cocycle on \(C\) exactly when the resulting value depends only on
\((\bar g,\bar h)\).  This is (3.2). \(\square\)

The cocycle condition on \(\bar\alpha\) must either be imposed explicitly
or obtained by selecting one value per pair in \(C^2\) and replaying all
triples.  Equality on sampled pairs is not a descent certificate.

## 4. Exact computation of V_S

Theorems 2.2 and 3.1 give two independent finite routes.

### Route A: group residual

Construct the actual finite extension \(H\), compute \(R_S(H)\) from a
composition series/formation-residual algorithm, and intersect it with the
literal kernel \(V\).  Independently prove:

\[
 H/R_S(H)\in\mathcal C_S,
 \qquad
 p(R_S(H))=R_S(E),
\tag{4.1}
\]

and replay the complete kernel basis of \(V_S\).

### Route B: cochain descent

Start with the necessary action quotient

\[
 W_0=V/[R,V].
\tag{4.2}
\]

Use the exact cocycle (3.1), not a split surrogate.  Determine the largest
quotient of \(W_0\) for which (3.2) is soluble.  Its kernel in \(V\) is
\(V_S\) by Theorem 2.2.  A positive receipt retains \(b\),
\(\bar\alpha\), every equation in (3.2), and the quotient maps.  A negative
claim for a proposed larger quotient requires a complete dual certificate
for the full cochain system.

Agreement of Routes A and B makes the result cross-checkable without sharing
the main helper.  If the full group is too large to materialize, Route B may
be run by sparse/column-generated cochains; an unvisited cochain column makes
the outcome `UNKNOWN`, not non-descent.

## 5. The actual return-even class

There are two maps here, and they must not be identified by notation.  Let

\[
 \beta_{\rm ev}\in Z_{\rm ev}
\tag{5.1}
\]

be the literal return-even relation defect after the return-odd dihedral
correction.  Let \(A^{\rm com}\) be the word-bearing exact-commutator
correction domain, and write

\[
 B_{\rm ev}:A^{\rm com}\to Z_{\rm ev},\qquad
 \rho:A^{\rm com}\to V
\tag{5.2}
\]

for, respectively, the change of the relation defect and the change of the
joint formation fibre.  A correction word \(c\) must satisfy the **joint**
system

\[
 \boxed{
 B_{\rm ev}(c)=-\beta_{\rm ev},\qquad
 \rho(c)\bmod V_S=-\omega_S(\delta_{\widehat b})
 \quad\text{in }V/V_S.}
\tag{5.3}
\]

The second equation is precisely v147 (4.4), with the frozen right
convention.  The first is the actual GT relation equation.  They collapse to
one equation only after an authenticated comparison identifies the relevant
summand of \(Z_{\rm ev}\) with the corresponding summand of \(V\) and proves
that \(B_{\rm ev}\) agrees there with \(\rho\).  Equal dimensions, a shared
return label, or a common abstract module is not that comparison.

Thus `actual class identification` consists of the following literal data:

1. the extension cocycle \(\alpha\) of the **same** joint first-rung group;
2. the submodule \(V_S\) computed by (4.1) or (3.2);
3. the exact R07 error word evaluated as \(\beta_{\rm ev}\) in
   \(Z_{\rm ev}\);
4. the two word-bearing maps \(B_{\rm ev}\) and \(\rho\), including the
   comparison from the relation module to the joint extension fibre;
5. the projection of \(\rho(c)\) to \(V/V_S\); and
6. one common word-bearing preimage satisfying both equations in (5.3).

A nonzero return-even vector in an ambient relative-cohomology group is not
yet the load-bearing survivor.  It becomes so only after items 1--5 identify
it with the literal R07 defect and formation-fibre displacement.  Conversely,
item 6 is the class-specific `field-outer` homotopy value needed beside the
dihedral antisymmetrizer at this edge.

## 6. Relation to the iterated Frattini tower

At every edge of v145's relative pro-3 tower the new kernel is elementary
abelian, so Theorems 2.1--2.2 apply.  If the extension/correction complexes
are authenticated base changes of one completed system, the maximal
descended quotients and the solutions of (3.2) commute with reduction; then
the resulting class-specific inverse is the continuous return-even summand
of v147 (6.2).

Without those base-change squares, compute (2.5) and the joint system (5.3)
at the next typed edge.  Pointwise equality of dimensions at several edges
does not prove naturality of \(V_S\), \(b\), or \(\bar\alpha\).

## 7. First-rung computation contract

After task184 supplies an exact-commutator task179 component:

1. build the joint first relative Frattini extension
   \(1\to V\to\mathcal H_1\to\mathcal H_0\to1\);
2. extract a normalized multiplication cocycle \(\alpha\) with literal
   section words;
3. compute \(R_S(\mathcal H_0)\), the action quotient (4.2), and both Routes
   A and B where resources permit;
4. bind \(V_S\) and the isomorphism of v147 (4.3b);
5. evaluate the arithmetic-reference difference in \(V/V_S\), the exact R07
   defect in \(Z_{\rm ev}\), and the comparison maps in (5.2);
6. append that quotient equation to the same word-bearing common-correction
   system; and
7. replay the returned word in every joint context before promoting it to
   the second Frattini rung.

The first eligible negative is a helper-independent complete nonmembership
of the actual affine class in the full registered residual-supported domain.
It kills that finite component only.  A cap, sampled cochain system, or one
failed preimage is `UNKNOWN`.

```text
EXTENSION DESCENDS TO E/R <=> ACTION + INFLATION: PAPER_PROOF
V/(V INTERSECT R_S(H)) IS MAXIMAL DESCENDED QUOTIENT: PAPER_PROOF
LITERAL FINITE COCHAIN DESCENT SYSTEM:              PAPER_PROOF
FIRST R07 JOINT EXTENSION COCYCLE:                  NOT COMPUTED
FIRST FORMATION-RESIDUAL SUBMODULE V_S:             NOT COMPUTED
ACTUAL JOINT RETURN-EVEN R07 CLASS (5.3):            NOT IDENTIFIED
RESIDUAL-SUPPORTED WORD-BEARING PREIMAGE:           OPEN
COMPLETED NATURAL RETURN-EVEN HOMOTOPY:              OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:     NOT DECLARED
```

`R07_FORMATION_RESIDUAL_EXTENSION_DESCENT_V148_PAPER_GRADE`
