# R07 compressed diagonal-successor relation module v188

Author: Sol / 2026-08-28

Status: paper theorem and corrected production architecture for the first
diagonal successor.  It replaces literal enumeration of an enormous finite
diagonal group by a marked-presentation relation-module closure.  The theorem
is exact and word-bearing.  The required marked presentation and the actual
task193 successor rows have not yet been joined in production.  No first
multiplier, compatible cofinal lift, fake certificate, or Ihara witness is
declared.

## 1. Why a literal state roster is the wrong interface

The authenticated task176/task179 roof machinery represents a finite
all-context group by an exact sequence

\[
 1\longrightarrow\Gamma\longrightarrow D_{\rm all}
 \longrightarrow Q_0\longrightarrow1,
\tag{1.1}
\]

with recorded orders

\[
 |\Gamma|=243,
 \qquad |Q_0|=1{,}469{,}664,
 \qquad |D_{\rm all}|=357{,}128{,}352.
\tag{1.2}
\]

The existing implementation intentionally stores a 243-state Gamma graph,
a compressed parent/letter section of \(Q_0\), and an on-demand global
cursor.  It does not serialize all \(357{,}128{,}352\) states.  Therefore a
successor contract requiring a literal BFS roster and four transitions for
every roof state destroys the compression already proved at the preceding
stage.

There is also a load-bearing type issue.  Task176's \(D_{\rm all}\) uses ten
typed coordinate values, whereas the successor relation module has two
hexagon and five pentagon blocks.  Production must authenticate the marked
map from the former common-source representation to the latter seven
relation contexts.  The symbols \(Q_0\), \(D_{\rm all}\), and the v173
\(\Delta_0\) may not be identified merely from their names.  The theorem
below applies to the resulting correctly typed \(\Delta_0\).

## 2. The kernel from finitely many relator defects

Let \(F=F(X)\) be a free group on a finite marked set \(X\).  In R07,
\(X=\{x,y\}\).  Suppose there are compatible marked maps

\[
 \rho_1:F\twoheadrightarrow\Delta_1,
 \qquad
 \rho_0:F\twoheadrightarrow\Delta_0,
 \qquad
 \pi:\Delta_1\twoheadrightarrow\Delta_0,
 \qquad
 \pi\rho_1=\rho_0,
\tag{2.1}
\]

onto their displayed marked images.  Assume

\[
 V=\ker(E_1\to E_0)
\tag{2.2}
\]

is an elementary abelian \(p\)-group in an ambient compatible extension,
\(\Delta_j\) are the two marked images inside \(E_j\), and

\[
 K=\ker(\Delta_1\to\Delta_0)=\Delta_1\cap V.
\tag{2.3}
\]

Conjugation gives \(V\) an \(\mathbf F_p[\Delta_0]\)-module structure.  It
is well defined: two lifts of a roof element differ by an element of the
abelian group \(V\), whose inner action on \(V\) is trivial.

Let a complete finite marked presentation be authenticated:

\[
 \boxed{
 \Delta_0\cong
 \langle X\mid r_1,\ldots,r_m\rangle,}
\qquad
 \ker\rho_0=\langle\!\langle r_1,\ldots,r_m\rangle\!\rangle_F.
\tag{2.4}
\]

For each relator define its successor defect

\[
 b_j=\rho_1(r_j)\in V.
\tag{2.5}
\]

### Theorem 2.1 (COMPRESSED SUCCESSOR-KERNEL THEOREM)

Under (2.1)--(2.5),

\[
 \boxed{
 K=\mathbf F_p[\Delta_0]\,\langle b_1,\ldots,b_m\rangle.}
\tag{2.6}
\]

In particular, the complete first-successor kernel is obtained by closing
the finitely many literal relator defects under the marked roof action.  No
enumeration of \(\Delta_0\), \(K\), or \(\Delta_1\) is required.

#### Proof

Put \(R=\ker\rho_0\).  Compatibility gives \(\rho_1(R)\leq V\), and
surjectivity onto the two marked images gives

\[
 K=\rho_1(R).
\tag{2.7}
\]

Every element of \(R\) is a finite product of conjugates
\(u r_j^{\pm1}u^{-1}\).  Since all their \(\rho_1\)-images lie in the
abelian group \(V\), multiplication there is addition, inversion is
negation, and

\[
 \rho_1(u r_j u^{-1})
 =\rho_0(u)\cdot b_j.
\tag{2.8}
\]

Thus (2.7) is contained in the right side of (2.6).  Conversely every vector
in (2.8) is the image of an element of \(R\), and products and powers of
such elements remain in \(\rho_1(R)\).  This proves equality. \(\square\)

The completeness of the marked presentation in (2.4) is load-bearing.  A
list of words which merely evaluates to the roof identity proves only one
containment in (2.6).

## 3. Rank-bounded word-bearing closure

Represent \(V\) by the exact block-tagged sparse affine/Fox quotient used by
task193.  Begin an echelon with the rows \(b_j\).  Whenever a row raises
rank, retain:

1. its literal source ancestry as a product of conjugates of the \(r_j\);
2. its complete seven-context value;
3. its unreduced sparse row and full boundary ancestry; and
4. its pivot-normalized linear ancestry.

Place every rank-raising row in a queue.  For each queued row apply every
marked generator and inverse through the exact conjugation action, reduce,
and enqueue only a rank increase.  Stop when the queue is empty.

### Proposition 3.1 (FINITE COMPLETENESS CERTIFICATE)

The terminal echelon span is exactly \(K\).  It has at most
\(\dim_{\mathbf F_p}V\) rank increases.  Queue exhaustion is a proof of
completeness, not a search-radius terminal.

#### Proof

The terminal span contains every \(b_j\) and is stable under the marked
generators and their inverses.  Hence it contains the
\(\mathbf F_p[\Delta_0]\)-span in (2.6).  Every inserted row is obtained
from a \(b_j\) by that action and linear combination, so the reverse
containment holds.  Each successful enqueue raises finite-dimensional rank,
giving the bound. \(\square\)

If the terminal rank is \(t\), the retained pivot ancestries materialize a
word-bearing basis \(k_1,\ldots,k_t\) of \(K\).  Linear sums in an ancestry
are products and powers of the corresponding conjugated relators in the
elementary abelian group.  Consequently

\[
 K\cong(C_p)^t,
 \qquad |K|=p^t.
\tag{3.1}
\]

For \(p=3\), the augmentation ideal has the already proved bound

\[
 J_K^{2t+1}=0.
\tag{3.2}
\]

Production should still replay order three, pairwise commutation, basis
independence, and reduction to the roof identity on the retained literal
basis.  Those are cheap basis checks; exhaustive traversal of \(3^t\)
kernel elements is unnecessary.

## 4. A complete compressed model of the successor group

Let \(\sigma:\Delta_0\to\Delta_1\) be any exact algorithmic section.  It
may be supplied by nested compressed sections such as the Gamma/\(Q_0\)
representation in (1.1); it need not be a materialized state table.  Every
successor element has a unique form

\[
 k\,\sigma(q),
 \qquad k\in K,\ q\in\Delta_0.
\tag{4.1}
\]

The action and section cocycle

\[
 q\cdot k=\sigma(q)k\sigma(q)^{-1},
 \qquad
 \kappa(q,q')=\sigma(q)\sigma(q')\sigma(qq')^{-1}
\tag{4.2}
\]

give exact multiplication and inverse formulas in the finite crossed
extension.  Every \(k\) is stored as a length-\(t\) vector over
\(\mathbf F_3\); every roof value uses its already authenticated compressed
index/section evaluator.  The group order is certified symbolically as

\[
 \boxed{|\Delta_1|=|\Delta_0|\,3^t.}
\tag{4.3}
\]

Completeness consists of:

1. the complete marked presentation (2.4);
2. Theorem 2.1 and the exhausted rank closure;
3. exact compressed roof multiplication/inverse;
4. exact action and cocycle replay on marked generators and presentation
   relators; and
5. associativity/cocycle identities derived from direct affine evaluation.

It does not consist of listing all elements.  Hashes may seal caches but do
not decide affine equality.

## 5. The pointed canary without a group roster

Let

\[
 A=\mathbf F_3[\Delta_1],
 \qquad I=\ker(A\to\mathbf F_3[\Delta_0]),
 \qquad M=Ad+Ae
\tag{5.1}
\]

inside the full Fox cokernel.  For the basis in Section 3,

\[
 I=A\langle k_i-1:1\leq i\leq t\rangle A.
\tag{5.2}
\]

Normality of \(K\) permits either one-sided placement of the generators.
Therefore

\[
 \boxed{
 IM=A\,\langle (k_i-1)d,(k_i-1)e:1\leq i\leq t\rangle,}
\tag{5.3}
\]

and

\[
 \boxed{
 I(Ad)=A\,\langle (k_i-1)d:1\leq i\leq t\rangle.}
\tag{5.4}
\]

Construct either span by the same rank queue as in Section 3: insert the
displayed seed rows and close only under the two lifted source generators
and their inverses.  The queue stops after at most the ambient Fox-cokernel
dimension many rank increases.  It is exact because a stable span under the
marked generators is an \(A\)-submodule.

This gives all three first-edge decisions without enumerating \(A\):

\[
 \begin{array}{rcl}
 \text{pointed pass}&\Longleftrightarrow&e\in IM,\\[2mm]
 \text{direct pass}&\Longleftrightarrow&e\in I(Ad),\\[2mm]
 \text{pair canary}&\Longleftrightarrow&
 \dim M-\dim IM=\dim M_0,
 \end{array}
\tag{5.5}
\]

where \(M\) itself is the rank closure of \(d,e\), and \(M_0\) is built
independently at the roof.  A failed membership returns an echelon dual
annihilating the complete stable span and nonzero on \(e\).

If pointed ancestry returns

\[
 e=\alpha d+\beta e,
 \qquad \alpha,
 \beta\in I,
\tag{5.6}
\]

the source-word ancestry makes both coefficients literal sums of terms
\(g(k_i-1)\).  The compatible first multiplier is then

\[
 \boxed{
 \mu_1=(1-\beta)^{-1}\alpha
      =\left(\sum_{r=0}^{2t}\beta^r\right)\alpha.}
\tag{5.7}
\]

This is v184's ordered formula.  A direct pass has \(\beta=0\).  V187's
full Schreier--Jennings roster remains a valid finite normal form, but the
rank-closure formulation (5.3)--(5.4) is the production path when
\(|\Delta_1|\) is too large to enumerate.

## 6. Required revised production chain

The old literal-BFS task196 contract must be superseded by a compressed
version with the following gates, in order:

1. adapt a cross-checked task192-v3 positive receipt into a separately
   checked task193-compatible input without relabelling alone;
2. run task193 on that exact word and authenticate the actual affine rows;
3. authenticate a complete marked presentation of the correctly typed
   seven-context \(\Delta_0\), including the map from task176's ten-coordinate
   compressed representation;
4. compute \(K\) by Theorem 2.1 and Proposition 3.1;
5. export the compressed section/action/cocycle and word-bearing kernel
   basis; and
6. run the three rank closures in Section 5.

The independent checker must use a separately implemented presentation
replay, a different sparse pivot order, and a different section/cocycle
normal form.  Resource exhaustion is `UNKNOWN_RESOURCE`.  A completed rank
queue is a mathematical terminal; a sampled word radius is not.

This closes the finite-state explosion in the first-edge design.  It does
not remove the all-rung obligation: a positive \(\mu_1\) must still be
promoted by the universal identity of v175 or by the natural pointed
ancestry of v184 at every matched successor.

## 7. Fixed frontier

```text
LITERAL 357,128,352-STATE BFS REQUIREMENT:       SUPERSEDED
RELATOR-DEFECT FORMULA FOR COMPLETE K:           PAPER_PROOF
RANK-BOUNDED WORD-BEARING K CLOSURE:             PAPER_PROOF
COMPRESSED DELTA1 ACTION/COCYCLE MODEL:           PAPER_PROOF
POINTED/DIRECT/PAIR RANK CLOSURE WITHOUT ROSTER: PAPER_PROOF
TASK192-v3 -> TASK193 INPUT ADAPTER:              REQUIRED
TYPED TEN-CONTEXT -> SEVEN-CONTEXT ROOF MAP:      NOT AUTHENTICATED
ACTUAL FIRST-SUCCESSOR K / MU1:                   NOT COMPUTED
ALL-RUNG NATURAL POINTED ANCESTRY:                NOT PROVED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:           NOT DECLARED
```

`R07_COMPRESSED_DIAGONAL_SUCCESSOR_RELATION_MODULE_V188_PAPER_GRADE`
