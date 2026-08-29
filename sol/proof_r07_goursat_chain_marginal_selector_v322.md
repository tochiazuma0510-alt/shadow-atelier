# R07 Goursat-chain marginal selector (v322)

Author: Sol / 2026-08-29

Status: paper theorem generalizing v317--v318.  Every finite joint subgroup,
whether or not it is a fibre product over a tree of the visible coordinates,
has an iterated Goursat fibre-product decomposition.  Signed marginal measures
can therefore be glued sequentially along canonical cumulative common
quotients.  If each newly added local ambiguity maps onto its Goursat overlap,
this gives a closed common-source selector.  The actual R07 overlaps and
ambiguity maps have not been computed.  No lift, fake certificate or Ihara
witness is declared.

## 1. Canonical cumulative Goursat chain

Let

\[
 H\leq G_1\times\cdots\times G_m
\tag{1.1}
\]

be a finite subgroup whose projection to every \(G_i\) is onto.  Fix an
ordering of the factors and put

\[
 H_i=\operatorname{pr}_{1,\ldots,i}(H),
\qquad H_1=G_1.
\tag{1.2}
\]

For \(i\geq2\), view

\[
 H_i\leq H_{i-1}\times G_i.
\tag{1.3}
\]

Both projections in (1.3) are onto.  Define

\[
\begin{aligned}
 N^L_i&=\{h\in H_{i-1}:(h,1)\in H_i\},\\
 N^R_i&=\{g\in G_i:(1,g)\in H_i\}.
\end{aligned}
\tag{1.4}
\]

Goursat's lemma gives normal subgroups and a canonical isomorphism

\[
 D_i:=H_{i-1}/N^L_i
 \simeq G_i/N^R_i.
\tag{1.5}
\]

Let

\[
 \alpha_i:H_{i-1}\twoheadrightarrow D_i,
\qquad
 \beta_i:G_i\twoheadrightarrow D_i
\tag{1.6}
\]

be the quotient maps after fixing the Goursat isomorphism.

### Lemma 1.1 (ITERATED FIBRE-PRODUCT IDENTITY)

\[
 \boxed{
 H_i=H_{i-1}\times_{D_i}G_i
 \quad(2\leq i\leq m).}
\tag{1.7}
\]

#### Proof

This is the subgroup reconstruction clause of Goursat's lemma applied to
(1.3): a pair \((h,g)\) lies in \(H_i\) exactly when its two quotient
classes agree under (1.5). \(\square\)

Unlike v317's visible-coordinate tree, the chain (1.7) exists for every
subdirect joint image.  Its left factors are cumulative groups \(H_{i-1}\),
so the common quotients \(D_i\) can retain genuine higher-coordinate
entanglement.

If an original coordinate projection is not onto, replace \(G_i\) by its
actual image first.  A target requiring a value outside that image is already
an exact local obstruction.

## 2. Exact recursive marginal criterion

Let

\[
 P_i:k[H_i]\longrightarrow\bigoplus_{j=1}^ik[G_j]
\tag{2.1}
\]

be the tuple of coordinate pushforwards.  For prescribed signed marginals
\(\mu_1,\ldots,\mu_i\), define recursively:

\[
 \mathcal Y_1(\mu_1)=\{\mu_1\}\subseteq k[H_1],
\tag{2.2}
\]

and for \(i\geq2\),

\[
\mathcal Y_i(\mu_1,\ldots,\mu_i)
=
\left\{
 G_i^{\rm fib}(\eta,\mu_i):
 \begin{array}{l}
 \eta\in\mathcal Y_{i-1}(\mu_1,\ldots,\mu_{i-1}),\\
 (\alpha_i)_*\eta=(\beta_i)_*\mu_i
 \end{array}
 \right\}.
\tag{2.3}
\]

Here \(G_i^{\rm fib}\) is the explicit two-factor signed-measure gluing
formula of v317 Lemma 1.1 for (1.7), after choosing sections of
\(\alpha_i,\beta_i\).

### Theorem 2.1 (GOURSAT-CHAIN MARGINAL CRITERION)

There is \(\ell\in k[H]\) with coordinate marginals
\(\mu_1,\ldots,\mu_m\) if and only if

\[
 \boxed{\mathcal Y_m(\mu_1,\ldots,\mu_m)\ne\varnothing.}
\tag{2.4}
\]

Every element returned by the recursion is such an \(\ell\).

#### Proof

Induct on \(i\).  At \(i=1\) the assertion is immediate.  By Lemma 1.1,
\(H_i\) is the fibre product of \(H_{i-1}\) and \(G_i\) over \(D_i\).
V317 Lemma 1.1 says that coefficients with marginals \(\eta,\mu_i\) glue if
and only if their \(D_i\)-pushforwards agree, and its formula preserves both
marginals.  Induction identifies the possible \(\eta\), proving (2.3)--(2.4).
\(\square\)

This is an exact finite dynamic program.  It does not replace a higher
Goursat constraint by pairwise visible-coordinate tests: each \(D_i\) is
computed from the whole cumulative image \(H_i\).

## 3. Quotient ambiguities and a closed selector

For every coordinate let

\[
 U_i\leq k[G_i],
\qquad
 Q_i=k[G_i]/U_i,
\qquad
 a_i+U_i=\alpha_i^{\rm tar}\in Q_i
\tag{3.1}
\]

be a chosen representative of the prescribed local class.  The notation
\(\alpha_i^{\rm tar}\) is unrelated to the Goursat map \(\alpha_i\) in
(1.6).

Suppose that for each \(i\geq2\) the new-coordinate ambiguity map

\[
 b_i=(\beta_i)_*|_{U_i}:U_i\longrightarrow k[D_i]
\tag{3.2}
\]

has a linear right inverse

\[
 h_i:k[D_i]\longrightarrow U_i.
\tag{3.3}
\]

### Theorem 3.1 (GOURSAT-CHAIN QUOTIENT SELECTOR)

Set \(\eta_1=a_1\).  Having constructed
\(\eta_{i-1}\in k[H_{i-1}]\), put

\[
 d_i=(\alpha_i)_*\eta_{i-1}-(\beta_i)_*a_i,
\tag{3.4}
\]

\[
 u_i=h_i(d_i),
\qquad
 \mu_i=a_i+u_i,
\tag{3.5}
\]

and define

\[
 \eta_i=G_i^{\rm fib}(\eta_{i-1},\mu_i).
\tag{3.6}
\]

Then \(\eta_m\in k[H]\) has coordinate class
\(\alpha_i^{\rm tar}\) in every \(Q_i\).  The construction is linear in the
chosen representatives and is an explicit common-source selector for every
target tuple.

#### Proof

Equations (3.2)--(3.5) give

\[
 (\beta_i)_*\mu_i
 =(\beta_i)_*a_i+d_i
 =(\alpha_i)_*\eta_{i-1}.
\tag{3.7}
\]

Thus the two inputs in (3.6) satisfy the exact fibre-gluing condition.
The gluing formula preserves the entire \(H_{i-1}\)-marginal and the new
\(G_i\)-marginal.  Induction therefore preserves all earlier coordinate
marginals and adds one representative of the desired new class.
\(\square\)

The full surjectivity in (3.2) is sufficient and stronger than necessary.
For one actual branch it is enough that every recursively encountered value
(3.4) lie in \(b_i(U_i)\), with a retained preimage.  Different earlier
gluing choices can affect a later cumulative marginal, so a bounded greedy
failure is not a complete negative unless the right inverses are defined on
the entire required spaces or the full finite dynamic program is exhausted.

## 4. Exact local dual for a prefix-corrected ambiguity

For the v313 ambiguity

\[
 U_i=\epsilon_iK_{r_i}p_i^{-1},
\qquad
 K_{r_i}=\ker(a\mapsto a(1-r_i)),
\tag{4.1}
\]

the dual of (3.2) is explicit.

### Lemma 4.1 (GOURSAT-OVERLAP ORBIT DUAL)

A functional \(\lambda\in k[D_i]^*\) annihilates \(b_i(U_i)\) exactly when

\[
 \boxed{
 \sum_{g\in C}
 \lambda\!\left(\beta_i(gp_i^{-1})\right)=0}
\tag{4.2}
\]

for every right \(\langle r_i\rangle\)-orbit \(C\subseteq G_i\).

#### Proof

This is v318 Lemma 3.1 with the parent-edge quotient replaced by the
Goursat quotient \(\beta_i:G_i\to D_i\). \(\square\)

Consequently (3.2) is onto if and only if the only functional satisfying
(4.2) is zero.  For one target \(d_i\), membership is equivalent to
\(\lambda(d_i)=0\) for every such functional.  A nonzero pairing is a
complete local obstruction for the fixed preceding cumulative measure.

If return commutes with the Goursat maps, the odd/even split may be imposed
in (3.2).  The relative-dihedral section handles the odd target, while the
actual field-outer work is one even preimage in each cumulative overlap.

## 5. Ordering and complexity

The Goursat chain depends on the coordinate order.  The final group \(H\)
does not, but the sizes of \(H_i,D_i\) and the ranks of (3.2) can change
substantially.  Any implementation should preregister an order and may
optimize it using only authority data, for example by:

1. adding a coordinate with the smallest common quotient \(D_i\);
2. preferring a coordinate whose ambiguity image already has full rank; and
3. keeping H1, H2 and the five pentagon occurrences tagged even if two
   underlying group maps coincide.

Changing order after seeing an actual target is a different selector and
must be recorded.  A negative in one greedy order need not be a negative in
another; full dynamic-program exhaustion on the same \(H\) is order
independent.

The chain avoids enumeration of all columns in \(k[H]\) when the local maps
are onto.  Its linear work is the sum of the overlap solves and the sparse
two-factor gluing operations.  If a cumulative \(D_i\) is as large as \(H_i\),
there may be no performance gain; the theorem is an exact structural
factorization, not an unconditional smallness claim.

## 6. Natural cofinal tower

Let the joint images, cumulative projections and Goursat quotients carry a
level \(n\).  Suppose:

1. the factor ordering is fixed;
2. every \(H_{i,n+1}\to H_{i,n}\) maps the Goursat kernels in (1.4) onto the
   corresponding lower kernels and induces \(D_{i,n+1}\to D_{i,n}\);
3. the set sections used by the two-factor gluing commute with reduction;
4. the target representatives reduce compatibly; and
5. the local right inverses \(h_{i,n}\) commute with reduction.

### Theorem 6.1 (COFINAL GOURSAT-CHAIN SELECTOR)

Under these hypotheses, the recursion (3.4)--(3.6) commutes with reduction.
It gives one compatible common-source coefficient at every level and hence
one element of the completed joint-image measure algebra.

#### Proof

Induct on \(i\) and \(n\).  Naturality of the cumulative quotient maps and
the preceding \(\eta_{i-1}\) makes (3.4) compatible.  Naturality of \(h_i\)
makes \(u_i,\mu_i\) compatible.  Naturality of the v317 gluing formula makes
\(\eta_i\) compatible. \(\square\)

If \(H_n\) is the actual image of one common source group \(\Gamma_n\), a
compatible source section or v98's nested-kernel spelling turns these
measures into one completed common word.  Independent coordinate words are
not permitted.

## 7. R07 application boundary

Unlike v317, the present theorem does not require the seven visible context
groups themselves to form a tree.  Actual application requires:

1. the authenticated full joint image \(H\), not only its coordinate or
   pairwise projections;
2. every cumulative group \(H_i\), Goursat kernel and quotient \(D_i\);
3. exact prefix-corrected ambiguity maps \(b_i\);
4. MEMBER ancestries or complete duals from Lemma 4.1;
5. naturality of the chain on the chosen cofinal refinement; and
6. one common-source word section plus literal relation and side-gate replay.

V317--v318 remain useful when a visible tree exists, because their overlaps
can be much smaller and symmetric.  V322 is the always-available structural
fallback; its unknown part is local ambiguity surjectivity, not existence of
a Goursat decomposition.

    EVERY FINITE JOINT IMAGE HAS A GOURSAT CHAIN:     PAPER PROOF
    EXACT RECURSIVE SIGNED-MARGINAL CRITERION:        PAPER PROOF
    LOCAL OVERLAP ONTO GIVES CLOSED GLOBAL SELECTOR: PAPER PROOF
    PREFIX-TWISTED GOURSAT DUAL:                     PAPER PROOF
    NATURAL CHAINS GIVE COFINAL SELECTOR:            PAPER PROOF
    ACTUAL R07 GOURSAT QUOTIENTS / LOCAL RANKS:      NOT COMPUTED
    ACTUAL RETURN-EVEN OVERLAP PREIMAGES:            NOT CONSTRUCTED
    NONLINEAR / FORMATION / PERFECT-CORE GATES:      OPEN
    COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:  NONE

R07_GOURSAT_CHAIN_MARGINAL_SELECTOR_V322_PAPER_GRADE
