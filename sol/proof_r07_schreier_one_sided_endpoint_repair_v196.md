# R07 Schreier one-sided endpoint repair v196

Author: Sol / 2026-08-28

Status: paper theorem refining the production form of v195.  For the actual
rank-two free word source, the kernel of the first-successor group-algebra
map is generated as a **left** ideal by a finite Schreier basis of the
successor kernel.  Consequently endpoint repair needs one translating word
and one Schreier generator, rather than the two independent translating
words in v195's normal-relator formula.  The Schreier roster can be very
large, and the remaining translating orbit is infinite; a bounded failure is
therefore still `UNKNOWN`.  No actual multiplier, endpoint repair,
compatible lift, fake certificate, or Ihara witness is declared.

## 1. The actual free-source successor kernel

Put \(k=\mathbf F_3\), let

\[
 F=F(x,y)\xrightarrow{\psi_1}\Delta_1
\tag{1.1}
\]

be the surjective marked word map to the finite first diagonal successor,
and put

\[
 H_1=\ker\psi_1,
 \qquad
 J_1=\ker\bigl(k[F]\longrightarrow k[\Delta_1]\bigr).
\tag{1.2}
\]

Choose a rooted spanning tree in the positive \(x,y\) Cayley graph of
\(\Delta_1\).  Let \(s(q)\in F\) be the resulting prefix-closed source word
for \(q\in\Delta_1\).  For \(a\in\{x,y\}\), define the Schreier word

\[
 h(q,a)=s(q)a\,s(q\psi_1(a))^{-1}\in H_1.
\tag{1.3}
\]

Delete exactly the tree-edge words which freely reduce to the identity, and
write the remaining roster as

\[
 \mathcal H_1=\{h_1,\ldots,h_r\}.
\tag{1.4}
\]

### Lemma 1.1 (FINITE SCHREIER BASIS)

The roster \(\mathcal H_1\) is a free basis of \(H_1\).  If
\(n=|\Delta_1|\), then

\[
 \boxed{r=n+1.}
\tag{1.5}
\]

#### Proof

This is the Reidemeister--Schreier construction for the index-\(n\)
subgroup \(H_1\leq F(x,y)\), using the prefix-closed transversal supplied by
the tree.  There are \(2n\) positive directed edges and exactly \(n-1\)
tree edges.  The non-tree Schreier words form a free basis, so their number
is \(2n-(n-1)=n+1\). \(\square\)

The full basis may be streamed from an exact compressed \(\Delta_1\)
section and transition evaluator.  Formula (1.5) is not permission to
replace that stream by a bounded word ball.

## 2. The direction ideal is finitely generated on one side

### Theorem 2.1 (SCHREIER LEFT-IDEAL FORM)

With (1.1)--(1.4),

\[
 \boxed{
 J_1=\sum_{j=1}^{r} k[F](h_j-1).}
\tag{2.1}
\]

Equivalently, every finite-support \(N\in J_1\) has a finite expression

\[
 \boxed{
 N=\sum_{\ell=1}^{m}c_\ell A_\ell(h_{j_\ell}-1),
 \qquad c_\ell\in k,\qquad A_\ell\in F.}
\tag{2.2}
\]

#### Proof

The fibre-difference lemma of v195 writes every element of \(J_1\) as a
finite sum of \(U-V\) with \(\psi_1(U)=\psi_1(V)\).  Put
\(h=V^{-1}U\in H_1\).  Then

\[
 U-V=V(h-1).
\tag{2.3}
\]

By Lemma 1.1, \(h\) is a finite word in the \(h_j^{\pm1}\).  Repeatedly use

\[
 ab-1=(a-1)+a(b-1),
 \qquad
 a^{-1}-1=-a^{-1}(a-1)
\tag{2.4}
\]

to express \(h-1\) as a finite left \(k[F]\)-linear combination of the
\(h_j-1\).  Equations (2.3)--(2.4) prove one inclusion in (2.1).  Every
\(h_j-1\) maps to zero in \(k[\Delta_1]\), and \(J_1\) is a left ideal, so
the reverse inclusion follows. \(\square\)

V195 Proposition 2.2 used a small normal-relator roster and the two-sided
terms \(A(s_j-1)B\).  Theorem 2.1 makes the complementary trade: the
Schreier roster is much larger but complete as an ordinary subgroup basis,
so the independent right word \(B\) disappears exactly.  A normal-generating
roster must not be substituted for \(\mathcal H_1\) in (2.1); normal
generation alone gives the two-sided formula, not this left-ideal formula.

## 3. One-sided endpoint-repair criterion

Let

\[
 \mathcal E_d:k[F]\longrightarrow
 k[PB_3]\oplus k[PB_3]\oplus k[PB_4]
\tag{3.1}
\]

be v195's three-combined-block endpoint-change map.  Thus a word-algebra
element is evaluated separately in all ten typed coordinates, reinserted in
the eleven literal positions, prefix/sign transported, and combined in the
printed H1/H2/P order before the three endpoints are returned.  Only
\(k\)-linearity of \(\mathcal E_d\) is used below.  In particular, no false
single-component equivariance is assumed after occurrence summands have
been combined.

Let \(M_0\) be one finite word-algebra representative of the actual
first-successor multiplier \(\mu_1\), and let \(\eta(M_0)\) be its v194
endpoint.

### Theorem 3.1 (ONE-SIDED SCHREIER REPAIR)

There is a finite-support representative of the same \(\mu_1\) with zero
three-block endpoint if and only if

\[
 \boxed{
 \eta(M_0)\in
 \operatorname{span}_k\!\left\{
   \mathcal E_d\bigl(A(h_j-1)\bigr):
   A\in F,\ 1\leq j\leq r
 \right\}.}
\tag{3.2}
\]

If

\[
 \eta(M_0)=
 \sum_{\ell=1}^{m}c_\ell
 \mathcal E_d\bigl(A_\ell(h_{j_\ell}-1)\bigr),
\tag{3.3}
\]

then the explicit repair and corrected representative are

\[
 N=\sum_{\ell=1}^{m}c_\ell A_\ell(h_{j_\ell}-1),
 \qquad
 M=M_0+N.
\tag{3.4}

They satisfy

\[
 N\in J_1,
 \qquad
 M\mapsto\mu_1,
 \qquad
 \eta(M)=0.
\tag{3.5}

Consequently v194 supplies finite universal boundary chains
\(q_{H1},q_{H2},q_P\).

#### Proof

By v195, the representatives of \(\mu_1\) are exactly \(M_0+J_1\), and

\[
 \eta(M_0+N)=\eta(M_0)-\mathcal E_d(N).
\tag{3.6}

Apply the linear map \(\mathcal E_d\) to the exact left-ideal form
(2.1)--(2.2).  Its image is precisely the span in (3.2).  Thus (3.6) can
vanish exactly under condition (3.2), and (3.3)--(3.5) give the promised
positive certificate.  The last assertion is v194 Theorem 3.2. \(\square\)

The columns in (3.2) are formed by the full eleven-occurrence action and
then combined.  They are not eleven separate endpoint equations, and they
are not obtained by multiplying one already-combined PB row by \(A\).

## 4. Complete positive dovetail and honest negative gate

Theorem 3.1 gives a complete positive semidecision with no guessed right
factor.

1. Stream the complete Schreier basis \(h_j\) from the compressed
   \(\Delta_1\) Cayley tree.
2. Dovetail freely reduced words \(A\in F(x,y)\).
3. Form the exact sparse column
   \(\mathcal E_d(A(h_j-1))\), retaining \((A,j)\) and all eleven literal
   evaluations.
4. Maintain a sparse echelon and reconsider \(\eta(M_0)\) after every rank
   increase.
5. On membership, recover (3.3), build (3.4), and directly replay the three
   zero endpoints.

If a finite repair exists, its expression (2.2) contains finitely many
pairs \((A_\ell,j_\ell)\); a fair dovetail eventually visits all of them and
terminates positively.  This proves completeness only for the positive
branch.  Neither a word-radius cutoff nor a partial Schreier stream proves
nonmembership.

A genuine negative certificate is a linear functional \(\lambda\) on the
three combined PB group algebras such that

\[
 \lambda(\eta(M_0))\ne0,
 \qquad
 \lambda\!\left(\mathcal E_d(A(h_j-1))\right)=0
 \quad\text{for every }A\in F,\ 1\leq j\leq r.
\tag{4.1}
\]

The second condition is a complete infinite-orbit statement and needs its
own invariant proof.  A dual annihilating only generated columns certifies
only the registered finite prefix.

## 5. Production interface after the first pointed pass

After v188/v191 return \(\Delta_1,\mu_1,M_0\), the exact order is:

1. compute v194's three combined endpoints for \(M_0\);
2. if they vanish, skip repair and extract the three boundary chains;
3. otherwise use the authenticated compressed multiplication, inverse,
   transition, and source-section interface for \(\Delta_1\) to stream the
   Schreier words (1.3);
4. run the one-sided positive dovetail of Section 4;
5. retain the complete coefficient ancestry (3.3)--(3.4); and
6. rerun the endpoint and boundary replay before invoking v174.

The positive receipt binds the exact \(\Delta_1\) order, Cayley-tree
parent/letter section, every non-tree edge, every \(A_\ell,h_{j_\ell}\),
same-successor equality, the three endpoint columns, and the recovered
coefficients.  Destructive controls change one tree edge, successor state,
Schreier inverse, left word, coefficient, typed occurrence, sign, prefix, or
printed-order slot.

The first endpoint test remains the cheapest gate.  The Schreier stream is
opened only on a nonzero result.  Since \(|\Delta_1|=|\Delta_0|3^t\), full
materialization can be expensive; an on-demand compressed stream preserves
the theorem but does not turn an interrupted run into a negative result.

```text
FINITE SCHREIER BASIS OF ACTUAL H1:                  PAPER_PROOF
J1 FINITELY GENERATED AS A LEFT IDEAL:               PAPER_PROOF
TWO-INDEPENDENT-WORD REPAIR ORBIT A(s-1)B:            REPLACED FOR FREE SOURCE
ONE-SIDED REPAIR IFF SCHREIER-ORBIT MEMBERSHIP:       PAPER_PROOF
FAIR ONE-SIDED DOVETAIL FINDS EVERY FINITE REPAIR:    PAPER_PROOF
BOUNDED FAILURE / PARTIAL SCHREIER STREAM:            UNKNOWN
ACTUAL DELTA1 / FIRST MULTIPLIER M0:                  NOT COMPUTED
ACTUAL THREE-BLOCK ENDPOINT / REPAIR:                 NOT COMPUTED
COMPATIBLE RELATIVE PRO-3 LIFT:                       NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE GATES:                      OPEN
FAKE / IHARA WITNESS:                                 NOT DECLARED
```

`R07_SCHREIER_ONE_SIDED_ENDPOINT_REPAIR_V196_PAPER_GRADE`
