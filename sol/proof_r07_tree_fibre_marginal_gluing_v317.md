# R07 tree fibre-product marginal gluing selector (v317)

Author: Sol / 2026-08-29

Status: paper theorem.  It gives a closed linear common-source selector when
the finite joint context image is an authenticated fibre product over a tree.
In that case the apparently global multi-marginal condition of v313 is
equivalent to pairwise agreement on the edge quotients, and compatible
cartesian refinement data give one selector on the whole inverse system.
The actual seven-context R07 image has not been proved to have this tree
form; higher Goursat entanglement is therefore still possible.  No lift,
fake certificate, or Ihara witness is declared.

## 1. The two-factor gluing formula

Let \(k\) be a field and let

\[
 A\mathrel{\mathop{\longrightarrow}^{\alpha}}D
 \mathrel{\mathop{\longleftarrow}^{\beta}}B
\tag{1.1}
\]

be surjections of finite sets.  Put

\[
 X=A\times_D B
   =\{(a,b):\alpha(a)=\beta(b)\}.
\tag{1.2}
\]

Every set map induces the coefficient-summing pushforward on its free
\(k\)-space.  Choose set-theoretic sections

\[
 s_A:D\to A,\qquad s_B:D\to B.
\tag{1.3}
\]

They define linear maps on basis vectors

\[
\begin{aligned}
 J[d]&=[(s_A(d),s_B(d))],\\
 L_A[a]&=[(a,s_B(\alpha(a)))],\\
 L_B[b]&=[(s_A(\beta(b)),b)].
\end{aligned}
\tag{1.4}
\]

### Lemma 1.1 (SIGNED-MEASURE FIBRE GLUING)

For \(x\in k[A]\) and \(y\in k[B]\), a coefficient
\(m\in k[X]\) with marginals \(x,y\) exists if and only if

\[
 \alpha_*x=\beta_*y.
\tag{1.5}
\]

When their common value is \(z\), one explicit solution is

\[
 \boxed{
 G_{A,B}(x,y)=Jz+L_A(x-s_Az)+L_B(y-s_Bz).}
\tag{1.6}
\]

Here the same symbols \(s_A,s_B\) denote their linear extensions.

#### Proof

Necessity follows by pushing either marginal to \(D\).  For sufficiency,

\[
 \alpha_*(x-s_Az)=0,
 \qquad
 \beta_*(y-s_Bz)=0.
\tag{1.7}
\]

The \(A\)-marginal of the three terms in (1.6) is respectively

\[
 s_Az,\qquad x-s_Az,\qquad
 s_A\beta_*(y-s_Bz)=0,
\tag{1.8}
\]

and the analogous calculation gives the \(B\)-marginal \(y\).  Thus
(1.6) has the required marginals.  The formula uses subtraction and is
valid over every field, including \(k=\mathbf F_3\). \(\square\)

The lemma is about signed measures.  It would be false for nonnegative
probability measures without additional positivity hypotheses; no such
positivity is required in the R07 group-algebra problem.

## 2. A junction-tree theorem

Let \(T=(V,E)\) be a finite tree.  Attach a finite set \(G_v\) to every
vertex.  For an edge \(e=\{v,w\}\), attach a finite set \(D_e\) and
surjections

\[
 \pi_{v,e}:G_v\twoheadrightarrow D_e,
 \qquad
 \pi_{w,e}:G_w\twoheadrightarrow D_e.
\tag{2.1}
\]

Define the joint fibre product

\[
 H_T=
 \left\{(g_v)_v\in\prod_{v\in V}G_v:
 \pi_{v,e}(g_v)=\pi_{w,e}(g_w)
 \text{ for every }e=\{v,w\}\right\}.
\tag{2.2}
\]

Because \(T\) is a tree and every incidence map is onto, every vertex
projection \(H_T\to G_v\) is onto.  Let

\[
 P_T:k[H_T]\longrightarrow\bigoplus_{v\in V}k[G_v]
\tag{2.3}
\]

be the tuple of marginal pushforwards, and put

\[
 C_T=\left\{(\mu_v)_v:
 (\pi_{v,e})_*\mu_v=(\pi_{w,e})_*\mu_w
 \text{ for every }e=\{v,w\}\right\}.
\tag{2.4}
\]

### Theorem 2.1 (TREE MARGINAL GLUING)

\[
 \boxed{\operatorname{im}P_T=C_T.}
\tag{2.5}
\]

After choosing one section at each leaf-gluing step, iterating (1.6) gives
an explicit linear map

\[
 \boxed{G_T:C_T\longrightarrow k[H_T],
 \qquad P_TG_T=1_{C_T}.}
\tag{2.6}
\]

#### Proof

Every joint coefficient has equal edge pushforwards, so
\(\operatorname{im}P_T\subseteq C_T\).  For the converse, induct on the
number of vertices.  The one-vertex assertion is immediate.  Remove a leaf
\(w\), let \(v\) be its neighbour and \(e=\{v,w\}\), and write \(T'\) for
the remaining tree.  Then

\[
 H_T=H_{T'}\times_{D_e}G_w,
\tag{2.7}
\]

where \(H_{T'}\to D_e\) is the \(v\)-marginal followed by
\(\pi_{v,e}\).  This map is onto.  Given a tuple in \(C_T\), induction
returns a coefficient on \(H_{T'}\) with the prescribed old marginals.
Its \(D_e\)-pushforward equals that of the prescribed \(G_w\)-marginal by
(2.4).  Lemma 1.1 glues the two coefficients on (2.7) without changing
either marginal.  This proves (2.5), and the iterated formulas are linear,
giving (2.6). \(\square\)

The tree hypothesis is load-bearing.  On a graph with a cycle, pairwise
edge agreement need not capture every higher compatibility relation.  More
generally, a proper subdirect image inside (2.2) can carry a higher Goursat
constraint invisible in all listed edge quotients.

## 3. Quotient-valued local primitives

For each vertex choose a \(k\)-subspace \(U_v\leq k[G_v]\), not assumed to
be invariant under any group action, and put

\[
 Q_v=k[G_v]/U_v.
\tag{3.1}
\]

This includes v313's prefix-corrected cyclic ambiguity spaces
\(U_v=\epsilon_vK_{r_v}p_v^{-1}\).  Given target classes
\(\alpha_v\in Q_v\), define their representative product

\[
 \mathcal R(\alpha)=
 \prod_{v\in V}(\alpha_v+U_v)
 \subseteq\bigoplus_vk[G_v].
\tag{3.2}
\]

### Corollary 3.1 (QUOTIENT MARGINAL CRITERION)

There is \(\ell\in k[H_T]\) with

\[
 [({\rm pr}_v)_*\ell]=\alpha_v
 \quad(v\in V)
\tag{3.3}
\]

if and only if

\[
 \boxed{\mathcal R(\alpha)\cap C_T\ne\varnothing.}
\tag{3.4}
\]

Every tuple \(\mu\in\mathcal R(\alpha)\cap C_T\) gives the explicit
solution

\[
 \boxed{\ell=G_T(\mu).}
\tag{3.5}
\]

#### Proof

The marginals of a solution of (3.3) lie in both sets in (3.4).  Conversely,
Theorem 2.1 glues any tuple in the intersection and preserves its vertex
classes. \(\square\)

Thus, under an authenticated tree presentation of the joint image, the
global common-source condition is no longer an orbit over all joint columns.
It is the finite linear problem of choosing local ambiguity representatives
whose pushforwards agree on each edge.  This does not make (3.4) automatic:
the prefix-twisted spaces \(U_v\) still have to supply the required edge
adjustments.

If a finite group \(\Gamma\) maps onto \(H_T\), choose one literal source
word for every basis element of \(H_T\).  Applying that section to (3.5)
turns the glued coefficient into a word-bearing element of \(k[\Gamma]\).
The section is part of a positive certificate and must not be replaced by
seven unrelated word choices.

## 4. Natural inverse-system selector

Let the data of Section 2 carry a level \(n\), with the same rooted tree and
surjective reduction maps on all vertex and edge sets.  Assume the incidence
squares are cartesian and that the rooted leaf sections are chosen
compatibly with reduction.  Cartesian incidence squares are a sufficient
way to construct such sections recursively: the upper lift of a chosen
lower section value and an upper edge value is unique in the corresponding
pullback.

The formulas (1.4)--(1.6) then commute with reduction.  Induction over the
fixed rooted tree gives

\[
 u_nG_{T,n+1}=G_{T,n}c_n,
\tag{4.1}
\]

where \(u_n:k[H_{T,n+1}]\to k[H_{T,n}]\) and
\(c_n:C_{T,n+1}\to C_{T,n}\) are the natural maps.

### Theorem 4.1 (COFINAL TREE-MARGINAL SELECTOR)

Suppose a compatible target family of quotient classes \(\alpha_n\) has a
compatible linear representative selector

\[
 R_n(\alpha_n)\in
 \mathcal R_n(\alpha_n)\cap C_{T,n},
 \qquad
 c_nR_{n+1}(\alpha_{n+1})=R_n(\alpha_n).
\tag{4.2}
\]

Then

\[
 \boxed{\ell_n=G_{T,n}R_n(\alpha_n)}
\tag{4.3}
\]

is an explicit compatible solution at every level.  Hence it defines one
element of the completed common-source measure algebra.

For a vertical target \(\delta\) at one refinement, if the representative
selector in (4.2) sends it to a tuple reducing to zero, then

\[
 h_n(\delta)=G_{T,n+1}R_{n+1}(\delta)
\tag{4.4}
\]

lies in the vertical source kernel and maps to \(\delta\).  Thus (4.4) is
the v314 relative marginal Hensel map on that registered target subspace;
both v316 base-change defects vanish there.

#### Proof

Equation (4.1) and the second equality in (4.2) give compatibility of
(4.3).  Equation (2.6) gives all required quotient marginals.  If the tuple
in (4.4) reduces to zero, (4.1) gives
\(u_nh_n(\delta)=G_{T,n}(0)=0\); (2.6) gives its prescribed upper
marginals.  Therefore it is the required vertical preimage. \(\square\)

The theorem separates two issues which v316 packages into ranks:

1. **joint-image gluing**, discharged by the tree fibre-product formula; and
2. **local ambiguity gluing**, the representative selector (4.2).

For the return split, the known relative-dihedral antisymmetrizer may supply
the odd part of (4.2).  The actual field-outer task is then the even
edge-adjustment system inside the small overlap spaces \(k[D_e]\), rather
than an unrestricted search through \(k[H_T]\).  This is a genuine
closed-form all-refinement route if the tree and cartesian hypotheses are
authenticated.

## 5. R07 application boundary

The current seven-context authority/owner data do not yet prove that their
joint common-source image is the tree fibre product (2.2).  Before using the
selector one must retain:

1. a fixed tree and every literal common quotient \(D_e\);
2. equality of the actual joint image with \(H_T\), not merely surjectivity
   to every vertex or every pair;
3. the exact prefix-twisted ambiguity spaces and a solution of (3.4);
4. cartesian reduction squares and compatible section ancestry; and
5. one common source word section, plus direct H1/H2/ordered-pentagon and
   side-gate replay after materialization.

Pairwise projection tests alone are insufficient: for example

\[
 \{(x,y,z)\in(\mathbf F_p)^3:x+y+z=0\}
\tag{5.1}
\]

projects onto every pair but is a proper joint image.  This example is why
A4's full authority trace and the actual higher joint-image identity cannot
be skipped.

If the actual image fails the tree gate, v314--v316 remain the complete
general finite criterion.  If it passes, Theorem 4.1 supplies precisely the
infinite-refinement generalization sought from the relative-dihedral lift:
odd antisymmetrization plus a finite even overlap selector, both natural on
the cofinal tower.

```text
TWO-FACTOR SIGNED-MEASURE GLUING FORMULA:       PAPER PROOF
TREE JOINT IMAGE = EDGE-COMPATIBLE MARGINALS:   PAPER PROOF
QUOTIENT-PRIMITIVE INTERSECTION CRITERION:      PAPER PROOF
CARTESIAN TOWER GIVES NATURAL GLUING MAP:       PAPER PROOF
ACTUAL SEVEN-CONTEXT TREE PRESENTATION:         NOT ESTABLISHED
ACTUAL EVEN OVERLAP REPRESENTATIVE SELECTOR:    NOT CONSTRUCTED
ACTUAL V316 DEFECTS:                            NOT COMPUTED
NONLINEAR / FORMATION / PERFECT-CORE GATES:     OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS: NONE
```

`R07_TREE_FIBRE_MARGINAL_GLUING_V317_PAPER_GRADE`
