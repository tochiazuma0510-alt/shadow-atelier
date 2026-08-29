# R07 Goursat rectangle correlation basis (v325)

Author: Sol / 2026-08-29

Status: paper theorem making v324's zero-marginal correlation direction
explicit.  In each fibre of a two-factor Goursat product, the kernel of both
marginals has a four-term rectangle basis.  Its dimension and its image in
every later cumulative quotient follow without a dense kernel calculation.
No actual R07 joint image or target is computed, and no lift, fake
certificate or Ihara witness is declared.

## 1. The zero-two-marginal kernel of a fibre product

Let

\[
 A\xrightarrow{\alpha}D\xleftarrow{\beta}B
\tag{1.1}
\]

be surjections of finite sets and put

\[
 X=A\times_DB.
\tag{1.2}
\]

For \(d\in D\), write

\[
 A_d=\alpha^{-1}(d),\qquad B_d=\beta^{-1}(d)
\tag{1.3}
\]

and choose anchors

\[
 a_d^0\in A_d,\qquad b_d^0\in B_d.
\tag{1.4}
\]

Let

\[
 M:k[X]\longrightarrow k[A]\oplus k[B]
\tag{1.5}
\]

be the pair of coefficient-summing marginals, and let \(Z=\ker M\).
For \(a\in A_d\setminus\{a_d^0\}\) and
\(b\in B_d\setminus\{b_d^0\}\), define

\[
 R_{d,a,b}
 =[(a,b)]-[(a,b_d^0)]-[(a_d^0,b)]+[(a_d^0,b_d^0)].
\tag{1.6}
\]

### Theorem 1.1 (RECTANGLE BASIS)

\[
 \boxed{
 Z=
 \bigoplus_{d\in D}
 \operatorname{span}_k
 \{R_{d,a,b}:a\ne a_d^0,\ b\ne b_d^0\}.}
\tag{1.7}
\]

The displayed rectangles are a basis.  Consequently

\[
 \boxed{
 \dim_k Z=
 \sum_{d\in D}(|A_d|-1)(|B_d|-1).}
\tag{1.8}
\]

#### Proof

The four terms of (1.6) have cancelling \(A\)- and \(B\)-marginals, so every
rectangle lies in \(Z\).  Work independently in one block
\(k[A_d\times B_d]\).  A coefficient matrix has zero marginals exactly when
all of its row sums and column sums vanish.

For a zero-marginal matrix \(z\), subtract

\[
 \sum_{\substack{a\ne a_d^0\\b\ne b_d^0}}
 z_{a,b}R_{d,a,b}.
\tag{1.9}
\]

The result is zero on every entry away from the anchor row and anchor
column.  Its zero row sums then force all remaining entries in the anchor
column to vanish; zero column sums force the anchor row to vanish.  Thus
(1.9) spans the block kernel.

For independence, each non-anchor entry \((a,b)\) occurs with coefficient
one in exactly its own \(R_{d,a,b}\) and in no other displayed rectangle.
Different \(d\)-blocks have disjoint support.  This proves (1.7), and
counting the basis gives (1.8). \(\square\)

Equivalently, if \(\widetilde k[A_d]\) and \(\widetilde k[B_d]\) denote the
zero-augmentation subspaces based at the anchors, then

\[
 Z\simeq
 \bigoplus_{d\in D}
 \widetilde k[A_d]\otimes_k\widetilde k[B_d].
\tag{1.10}
\]

This is a correlation space: it changes the joint coefficient while
changing neither factor marginal.

## 2. Group-Goursat specialization

Now suppose \(A,B,D\) are finite groups, \(\alpha,\beta\) are surjective
homomorphisms, and

\[
 N_A=\ker\alpha,\qquad N_B=\ker\beta.
\tag{2.1}
\]

Every fibre has the constant sizes \(|N_A|\) and \(|N_B|\).  Hence:

### Corollary 2.1 (GOURSAT CORRELATION DIMENSION)

\[
 \boxed{
 \dim_k Z
 =|D|(|N_A|-1)(|N_B|-1)
 =|X|-|A|-|B|+|D|.}
\tag{2.2}
\]

#### Proof

The first equality is (1.8).  Since

\[
 |A|=|D||N_A|,\quad
 |B|=|D||N_B|,\quad
 |X|=|D||N_A||N_B|,
\tag{2.3}
\]

expansion gives the second equality. \(\square\)

The same formula follows from the exact sequence

\[
 0\longrightarrow Z\longrightarrow k[X]
 \xrightarrow{M}
 \{(x,y):\alpha_*x=\beta_*y\}
 \longrightarrow0,
\tag{2.4}
\]

but the rectangle basis additionally retains literal four-term ancestry.

At v324 step \(i\), take

\[
 A=H_{i-1},\quad B=G_i,\quad D=D_i.
\tag{2.5}
\]

Then Corollary 2.1 gives the exact size of the load-bearing direction
\(Z_i\) before any matrix construction.  The anchors may be chosen from the
same authenticated sections used in the v317 gluing formula.

## 3. Sparse image in a later overlap

Let

\[
 \gamma:X\longrightarrow E
\tag{3.1}
\]

be any map of finite sets.  In the R07 application it is a later cumulative
Goursat quotient map, possibly after including \(X=H_i\) into a larger
prefix.  Pushforward sends a rectangle to

\[
 \boxed{
 \gamma_*R_{d,a,b}
 =
 [\gamma(a,b)]-[\gamma(a,b_d^0)]
 -[\gamma(a_d^0,b)]+[\gamma(a_d^0,b_d^0)].}
\tag{3.2}
\]

### Proposition 3.1 (FOUR-TERM FUTURE-IMAGE ROSTER)

\[
 \boxed{
 \gamma_*(Z)=
 \operatorname{span}_k
 \{\gamma_*R_{d,a,b}\}_{d,a,b}.}
\tag{3.3}
\]

Thus the effect of all invisible current correlations on a later overlap is
computed from four-term sparse columns.  A retained ancestry in these
columns lifts immediately to the corresponding combination of literal
rectangles in \(k[X]\).

#### Proof

Apply the linear map \(\gamma_*\) to the basis in Theorem 1.1. \(\square\)

No assumption that \(\gamma\) factors through \(A\) or \(B\) is made.  If it
does factor through either marginal, every column (3.2) is zero; this is the
exact criterion explaining when the correlation kernel can safely be
dropped for that future quotient.

### Corollary 3.2 (MARGINAL-FACTORING VANISHING)

If \(\gamma=\gamma_A\operatorname{pr}_A\) or
\(\gamma=\gamma_B\operatorname{pr}_B\), then

\[
 \gamma_*(Z)=0.
\tag{3.4}
\]

The converse need not hold for one particular coefficient field or map:
four-term cancellations may occur for other reasons.  Therefore (3.2), not
a converse slogan, is the authoritative finite test.

## 4. Dual form

For a functional \(\lambda\in k[E]^*\), pairing with (3.2) gives the mixed
rectangle difference

\[
 \begin{aligned}
 \langle\lambda,\gamma_*R_{d,a,b}\rangle
  ={}&
 \lambda(\gamma(a,b))-\lambda(\gamma(a,b_d^0))\\
 &-\lambda(\gamma(a_d^0,b))
 +\lambda(\gamma(a_d^0,b_d^0)).
 \end{aligned}
\tag{4.1}
\]

### Proposition 4.1 (ADDITIVE-SEPARABILITY DUAL)

A functional \(\lambda\) annihilates \(\gamma_*(Z)\) if and only if every
mixed difference (4.1) is zero.  Equivalently, on each fibre block
\(A_d\times B_d\), the scalar function

\[
 (a,b)\longmapsto\lambda(\gamma(a,b))
\tag{4.2}
\]

has the form

\[
 f_d(a)+g_d(b)
\tag{4.3}
\]

for some functions \(f_d:A_d\to k\), \(g_d:B_d\to k\).

#### Proof

Annihilation is equivalent to zero pairing with the rectangle basis, giving
the first assertion.  If (4.1) vanishes, set

\[
 f_d(a)=\lambda(\gamma(a,b_d^0))
        -\lambda(\gamma(a_d^0,b_d^0)),
\qquad
 g_d(b)=\lambda(\gamma(a_d^0,b)).
\tag{4.4}
\]

The zero mixed difference gives (4.3).  Conversely every additively
separable function has zero mixed differences. \(\square\)

This can be substantially smaller than primal correlation columns: the
checker tests an additive-separability identity on each fibre.  In v324
Theorem 5.1 it describes the part of
\((\alpha_{i+1})^*\lambda\in V_i^\perp\) contributed by \(Z_i\).

## 5. Exact implementation boundary

A finite producer may now retain:

1. group orders and kernel orders proving (2.2);
2. authenticated anchors in every \(D_i\)-fibre;
3. the lexicographic rectangle roster (1.6);
4. four-term future images (3.2);
5. either a sparse primal basis/ancestry or the mixed-difference dual; and
6. direct zero-marginal replay of every emitted rectangle.

An independent checker can rebuild anchors independently and compare the
resulting subspace, since different anchors yield different bases of the
same canonical kernel \(Z_i\).  Mutating any corner, sign, fibre label or
future image must reject.

The theorem removes a dense nullspace calculation, not the need to
authenticate the actual cumulative group \(H_i\).  If \(H_i\) itself is too
large to enumerate, a compact group/presentation method is still required.

## 6. Cofinal boundary

When the group quotients and anchors are chosen naturally, rectangle
reduction gives compatible correlation bases.  Naturality of anchors is not
needed for the v313 compactness route: exact finite solution-set
nonemptiness remains sufficient.

The rectangle theorem concerns only the linear common-source endpoint.
Nonlinear localized saturation, mixed-prime formation, settlement and
perfect-core accepted sets remain separate.

The rectangle basis, dimension formula, sparse future-image roster and
additive-separability dual are paper proofs.  Actual R07 rectangles and
future images are not computed.  A compatible cofinal lift, fake
certificate and Ihara witness remain absent.

R07_GOURSAT_RECTANGLE_CORRELATION_BASIS_V325_PAPER_GRADE
