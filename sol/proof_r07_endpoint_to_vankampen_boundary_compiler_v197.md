# R07 endpoint-to-van-Kampen boundary compiler v197

Author: Sol / 2026-08-28

Status: paper algorithm refining v194 Section 5.  Once the three combined
endpoints vanish, the universal boundary coefficients are obtained by a
finite graph-cycle decomposition followed by proof-producing word reduction.
They do not require another translated-boundary rank search.  The algorithm
is total on a genuine zero-endpoint input; resource exhaustion in one
implementation remains UNKNOWN_RESOURCE, not a mathematical obstruction.
No actual endpoint, boundary chain, compatible lift, fake certificate, or
Ihara witness is declared.

## 1. One complete presentation block

Let

\[
 G=\langle X\mid R\rangle
\tag{1.1}
\]

be one of the fixed complete PB3 or PB4 presentations used in v194.  Put
\(k=\mathbf F_3\) and use the registered left-Fox complex

\[
 k[G]^R\xrightarrow{D_2}k[G]^X
 \xrightarrow{D_1}k[G],
\qquad
D_2[r]=\delta(r),\quad D_1(g[x])=g(x-1).
\tag{1.2}
\]

Suppose a finite chain

\[
 z=\sum_{g\in G,\ x\in X}c_{g,x}\,g[x]
\in k[G]^X
\tag{1.3}
\]

has zero endpoint:

\[
 D_1z=0.
\tag{1.4}
\]

The words representing every supported \(g\) are retained.  Equality of
group elements is decided by the authenticated PB normal form, not by a
finite quotient.

## 2. Finite fundamental-cycle decomposition

Let \(\mathscr S\) be the finite set containing every vertex \(g\) and
\(gx\) occurring in (1.3).  For every vertex in \(\mathscr S\), choose one
finite Cayley path from the identity to that vertex.  Adjoin all those paths
to the support graph, and let \(\mathscr K\) be the resulting finite
connected Cayley subgraph.  Orient its geometric edges by the positive
generators \(x\in X\);
an oppositely traversed edge is represented by

\[
 (g,x)^{-1}=-gx^{-1}[x].
\tag{2.1}
\]

Choose a spanning tree \(T\subseteq\mathscr K\), rooted at the identity.
For a vertex \(v\), let \(p_v\) be the signed edge path in \(T\) from the
identity to \(v\).
For every oriented non-tree edge \(e=(g,x)\), define the based loop

\[
 w_e=p_g\,x\,p_{gx}^{-1}.
\tag{2.2}
\]

The word \(p_v\) evaluates to \(v\), so \(w_e\) evaluates to one.  Let

\[
 \gamma_e=\delta(w_e)\in k[G]^X
\tag{2.3}
\]

be the left-Fox chain of this loop.

### Lemma 2.1 (FINITE CYCLE DECOMPOSITION)

There are uniquely determined coefficients \(a_e\in k\), one for each
chosen orientation of a non-tree edge, such that

\[
 \boxed{z=\sum_{e\notin T}a_e\gamma_e.}
\tag{2.4}
\]

They are obtained by finite tree-edge elimination.

#### Proof

The cellular chain complex of the finite graph \(\mathscr K\) has cycle
space

\[
 H_1(\mathscr K;k)=\ker(\partial:C_1(\mathscr K;k)\to C_0(\mathscr K;k)).
\tag{2.5}
\]

The fundamental cycles associated with the non-tree edges form its standard
basis.  Equation (1.4) says exactly that \(z\), viewed in this graph, lies in
that kernel.  Reading the coefficient of each non-tree edge gives \(a_e\);
subtracting those fundamental cycles leaves a cycle supported on the
tree, hence zero.  This proves existence, uniqueness, and the finite
elimination algorithm. \(\square\)

This argument works directly over \(\mathbf F_3\).  It does not interpret a
coefficient \(2\) as an unsigned multiplicity, so no false integral-flow
assumption enters.

## 3. Proof-producing identity reduction

For each nonzero \(a_e\), the freely reduced word \(w_e\) is the identity in
the presented group \(G\).  A van Kampen certificate is a finite expression

\[
 w_e=\prod_{\ell=1}^{m_e}
 s_{e,\ell}r_{i(e,\ell)}^{\epsilon_{e,\ell}}
 s_{e,\ell}^{-1}
 \quad\text{in }F(X),
\qquad
\epsilon_{e,\ell}\in\{1,-1\}.
\tag{3.1}
\]

There are two sound ways to obtain it.

1. An annotated rewriting engine reduces \(w_e\) to the empty word.  Every
   rewrite rule retains, once and for all, a decomposition of its
   left-side/right-side discrepancy into conjugates of the original
   relators \(R\).  Conjugating that annotation by the current prefix and
   concatenating the annotations gives (3.1).
2. Independently enumerate finite products of conjugates of the finite
   roster \(R^{\pm1}\), freely reduce them, and dovetail by total length.
   Since \(w_e\) is known to represent one in the complete presentation,
   the enumeration eventually returns (3.1).

The second method proves totality and does not assume a finite confluent
rewriting system.  The first is the practical extraction engine.

### Lemma 3.1 (REWRITE TRACE IS A RELATOR TRACE)

Suppose one annotated rule replaces \(\ell\) by \(r\) inside a word
\(a\ell b\), and its stored annotation is

\[
 \ell r^{-1}=\prod_j t_jR_j^{\varepsilon_j}t_j^{-1}.
\tag{3.2}
\]

Then the global rewrite discrepancy is

\[
 (a\ell b)(arb)^{-1}
 =\prod_j(at_j)R_j^{\varepsilon_j}(at_j)^{-1}
\tag{3.3}
\]

after free cancellations.  Therefore concatenating the annotated rewrite
steps gives (3.1).

#### Proof

Free reduction gives

\[
 (a\ell b)(arb)^{-1}
 =a\ell r^{-1}a^{-1}.
\tag{3.4}
\]

Substitute (3.2) and distribute the outer conjugation. \(\square\)

Free cancellation steps carry the empty relator annotation.  A checker can
therefore replay (3.1) using only literal free-word multiplication,
inversion, and reduction.

## 4. Fox extraction of the boundary coefficients

In \(k[G]^X\), left Fox differentiation of (3.1) gives

\[
 \boxed{
 \gamma_e=
 \sum_{\ell=1}^{m_e}
 \epsilon_{e,\ell}\,
 \overline{s_{e,\ell}}\,
 \delta(r_{i(e,\ell)}).}
\tag{4.1}
\]

Here a negative exponent is interpreted using

\[
 \delta(r^{-1})=-r^{-1}\delta(r)=-\delta(r)
 \quad\text{in }k[G]^X,
\tag{4.2}
\]

because \(\bar r=1\) in \(G\).  Define

\[
 q=
 \sum_{e\notin T}a_e
 \sum_{\ell=1}^{m_e}
 \epsilon_{e,\ell}\,
 \overline{s_{e,\ell}}\,[r_{i(e,\ell)}]
 \in k[G]^R.
\tag{4.3}
\]

### Theorem 4.1 (ZERO ENDPOINT TO EXPLICIT BOUNDARY)

The finite chain (4.3) satisfies

\[
 \boxed{D_2q=z.}
\tag{4.4}
\]

Every coefficient and source word in \(q\) is recovered from the finite
cycle and relator traces.

#### Proof

Apply \(D_2\) to (4.3), use (4.1), and then use the fundamental-cycle
decomposition (2.4). \(\square\)

Thus v194's existence implication is effective: zero endpoint first gives a
finite graph calculation, and every resulting identity loop has a
terminating proof enumeration.  No boundary-column radius and no complete
translate orbit enter (4.4).

## 5. Three R07 blocks

Apply Sections 1--4 independently to

\[
 z_{H1}(M),\qquad z_{H2}(M),\qquad z_P(M)
\tag{5.1}
\]

only after their eleven occurrence summands have been combined in the
printed relation order.  The two PB3 blocks use separately tagged copies of
the same two-relator presentation; the PB4 block uses its complete
eleven-relator presentation.  This returns

\[
 q_{H1},\qquad q_{H2},\qquad q_P
\tag{5.2}
\]

with

\[
 D_{2,B}q_B=z_B(M)
 \quad(B=H1,H2,P).
\tag{5.3}
\]

The construction does not require the seven occurrence summands to be
cycles.  Only the three combined endpoints must vanish.

### Corollary 5.1 (NO SECOND UNIVERSAL BOUNDARY SEARCH)

For a finite word-pair candidate \(M\), the post-candidate universal gate is:

\[
 \eta_{H1}(M)=\eta_{H2}(M)=\eta_P(M)=0.
\tag{5.4}
\]

On a pass, Theorem 4.1 deterministically compiles the finite \(q_B\).
Therefore a fresh full-D2 translated-column membership search after (5.4)
is mathematically redundant.

## 6. Certificate and independent replay

For each block, retain:

1. the collected finite chain \(z_B\) and its exact zero endpoint;
2. the finite support graph, added connecting paths, spanning tree, and
   positive-edge orientation;
3. every fundamental loop \(w_e\), coefficient \(a_e\), and direct replay
   of (2.4);
4. every annotated rewrite step or the final conjugate-relator expression
   (3.1);
5. the boundary chain \(q_B\); and
6. a literal sparse replay of (5.3).

The independent checker reconstructs the graph-cycle decomposition with a
different tree, replays every free-group identity in (3.1), recomputes the
Fox derivatives from the original relators, and compares the final chain
with \(z_B\).  Different trees and van Kampen diagrams may produce
different \(q_B\); equality of their \(D_2\)-images is the invariant.

Reject mutations of one endpoint coefficient, graph edge, path orientation,
loop coefficient, rewrite side, conjugating prefix, relator index, inverse
sign, Fox coefficient, block tag, or final boundary coefficient.

~~~text
FINITE GRAPH-CYCLE DECOMPOSITION AFTER ENDPOINT ZERO: PAPER_PROOF
IDENTITY WORD TO ORIGINAL-RELATOR TRACE:              TOTAL POSITIVE ALGORITHM
RELATOR TRACE TO EXPLICIT FOX BOUNDARY q:             PAPER_PROOF
SECOND FULL-TRANSLATE BOUNDARY SEARCH AFTER PASS:      REMOVED
ACTUAL WORD-PAIR CANDIDATE M:                         NOT COMPILED
ACTUAL THREE ENDPOINTS:                               NOT COMPUTED
ACTUAL q_H1 / q_H2 / q_P:                            NOT COMPILED
COMPATIBLE RELATIVE PRO-3 LIFT:                       NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE GATES:                      OPEN
FAKE / IHARA WITNESS:                                 NOT DECLARED
~~~

R07_ENDPOINT_TO_VANKAMPEN_BOUNDARY_COMPILER_V197_PAPER_GRADE
