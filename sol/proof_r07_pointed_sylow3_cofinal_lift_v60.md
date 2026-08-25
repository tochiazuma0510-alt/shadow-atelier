# R07 pointed Sylow-3 cofinal lift v60

Author: Sol / 2026-08-25

Status: paper-proof candidate; `verified=false`,
`cross_checked=false` for the new order-nine replay and the new pointed
criterion.  The finite K2 coordinates used below come from the independently
cross-checked ordinary row-36 receipt.

This note strengthens v50.  V50 propagates fullness of the roof image and
therefore recovers one of R07/R40.  Here the initial point itself is retained.
The extra input is that R07 is a 3-element--in fact it has order exactly nine
in the finite settled B3 group $GT_3(K2)$.  Consequently a Sylow-3 subgroup
containing R07 can be propagated first into a B4 component over K2 and then
along a cofinal B4 ladder.  Every step can be written by an explicit
finite-group word and one explicit power.

The result is a sufficient criterion.  It does not assert that the required
generator lifts exist at every B4 edge.

## 1. The finite R07 point has order nine

Use the canonical finite GT-shadow product

$$
(m_1,f_1)(m_2,f_2)=
\left(2m_1m_2+m_1+m_2,
f_1E_{m_1,f_1}(f_2)\right),
\tag{1.1}
$$

where, for $u=2m+1$,

$$
E_{m,f}(x)=x^u,
\qquad
E_{m,f}(y)=f^{-1}y^u f.
\tag{1.2}
$$

The cross-checked K2 receipt places the R07 word coordinate in

$$
Q=G_{36}\times PSL(2,8)\times C_3,
\qquad G_{36}\le D_{36}^{3},
\tag{1.3}
$$

and gives

$$
m_{07}=0,\qquad
f_{07}=\bigl(((4,0),(32,0),(0,0)),1,0\bigr).
\tag{1.4}
$$

Here $(a,e)$ denotes $r^as^e\in D_{36}$ and

$$
(a,e)(b,d)=\bigl(a+(-1)^e b,\,e+d\bmod2\bigr).
\tag{1.5}
$$

The marked generators in the $G_{36}$ coordinate are

$$
x=((1,0),(0,1),(0,1)),\qquad
y=((1,1),(1,0),(1,1)).
\tag{1.6}
$$

Let $g=((4,0),(32,0),(0,0))$.  Direct use of (1.5) gives

$$
g^{-1}yg=((29,1),(1,0),(1,1)).
\tag{1.7}
$$

For completeness, encode $x,y$ by $1,2$ and their inverses by $-1,-2$.
The frozen R07 word is

$$
\begin{aligned}
\omega_{07}=(&1,1,1,1,-2,-2,-2,-2,-1,2,-1,-1,-2,-1,-1,2,\\
             &-1,-1,-2,-1,-1,-2,-1,-1,2,-1,1,2,1,1,-2,1,\\
             &-1,-2,-1,-1,2,-1).
\end{aligned}
\tag{1.8}
$$

Its immutable signed-word SHA-256 is
`6bd02922d1ccaf41323d68167269bc8d7087d11aacbcf206df2a933a3b32aa00`.
Multiplying the 38 letters by (1.5) gives the following complete
three-factor replay:

$$
\begin{array}{c|c|c|c|c}
i&x_i&y_i&(g^{-1}yg)_i&
 \omega_{07}(x_i,(g^{-1}yg)_i)\\ \hline
1&(1,0)&(1,1)&(29,1)&(4,0)\\
2&(0,1)&(1,0)&(1,0)&(32,0)\\
3&(0,1)&(1,1)&(1,1)&(0,0).
\end{array}
\tag{1.9}
$$

Thus

$$
E_{0,f_{07}}(f_{07})=f_{07}.
\tag{1.10}
$$

Indeed (1.9) proves this on $G_{36}$; the $PSL(2,8)$ and $C_3$ coordinates
of $f_{07}$ are identities, so (1.2) is the identity on those marked
coordinates when $m=0$.

The three dihedral coordinates of $g$ are rotations.  Hence

$$
\operatorname{ord}(g)=
\operatorname{lcm}
\left(\frac{36}{\gcd(4,36)},
      \frac{36}{\gcd(32,36)},1\right)=9.
\tag{1.11}
$$

Equations (1.1) and (1.10) now imply inductively

$$
R07^k=(0,f_{07}^{k}).
\tag{1.12}
$$

We have proved:

### Proposition 1.1 (R07-ORDER9)

In the finite settled B3 shadow group $GT_3(K2)$,

$$
\boxed{\operatorname{ord}(R07)=9.}
\tag{1.13}
$$

In particular R07 belongs to a Sylow $3$-subgroup of that group.

The calculation uses the GT product, not the ordinary order of a free word.
That distinction is load-bearing.

### Proposition 1.2 (K2-UNIQUE-SYL3)

Let

$$
\rho:GT_3(K2)\longrightarrow X
\tag{1.14}
$$

be reduction to the pinned 972-element roof group, and let
$A\le X$ be its arithmetic subgroup of index three.  Then:

$$
\boxed{
\begin{gathered}
\rho\text{ is onto},\qquad |\ker\rho|=2,\qquad
|GT_3(K2)|=1944,\\
GT_3(K2)\text{ has a unique Sylow }3\text{-subgroup }P_0,\\
\rho|_{P_0}:P_0\xrightarrow{\sim}X^2,\qquad |P_0|=243.
\end{gathered}}
\tag{1.15}
$$

Here $X^2$ is the pinned unique Sylow $3$-subgroup of $X$.  Moreover R07
is the unique $3$-element above its roof point, whereas

$$
\boxed{\operatorname{ord}(R40)=18.}
\tag{1.16}
$$

#### Proof

Every arithmetic roof point has a K2 component, so

$$
A\le\operatorname{Im}(\rho)\le X.
\tag{1.17}
$$

The image of R07 is the pinned row-36 point outside $A$.  Since
$[X:A]=3$, there is no proper subgroup strictly between $A$ and $X$;
hence $\rho$ is onto.

The complete K2 fibre over row 36 is exactly $\{R07,R40\}$.  Every fibre
of an epimorphism of finite groups is a coset of its kernel, so
$|\ker\rho|=2$ and

$$
|GT_3(K2)|=2|X|=1944=2^3\,3^5.
\tag{1.18}
$$

Let $L=\rho^{-1}(X^2)$.  Then

$$
1\longrightarrow C_2\longrightarrow L
\longrightarrow X^2\longrightarrow1.
\tag{1.19}
$$

The normal kernel $C_2$ is central in $L$, because
$\operatorname{Aut}(C_2)=1$.  Schur--Zassenhaus gives a complement of
order $3^5$, and all complements are conjugate by the normal Hall
subgroup $C_2$.  Centrality makes that conjugation trivial, so the
complement $P_0$ is unique.  Every Sylow $3$-subgroup of $GT_3(K2)$ maps
into the unique $X^2$ and hence lies in $L$; therefore $P_0$ is also the
unique Sylow $3$-subgroup of the whole K2 group.  Its intersection with
the order-two kernel is trivial, proving that $\rho|_{P_0}$ is an
isomorphism.

Proposition 1.1 places R07 in $P_0$.  Its fibre has one other point,
necessarily $R07\cdot k$, where $k$ is the nontrivial central kernel
element.  That point is R40.  Since the commuting factors have coprime
orders nine and two, R40 has order eighteen. $\square$

Thus a generating set of $P_0$ may be obtained without enumerating the
1944-element K2 group: take any generating set of $X^2$ and, for each
generator, choose its unique $3$-element lift.  Formula (2.7) below turns
any explicit K2 lift into that unique lift.

## 2. A pointed Sylow lifting lemma

Let

$$
\phi:H\longrightarrow G
\tag{2.1}
$$

be a homomorphism of finite groups, let $P\le G$ be a $p$-subgroup, and
assume

$$
P\le\operatorname{Im}(\phi).
\tag{2.2}
$$

### Lemma 2.1 (POINTED-SYL-EDGE)

Every $b\in P$ has a $p$-element lift $\widetilde b\in H$.  More
precisely, if

$$
P=\langle s_1,\ldots,s_d\rangle
\tag{2.3}
$$

and explicit lifts $\widetilde s_i\in H$ are known, choose a signed word
$W$ with $W(s_1,\ldots,s_d)=b$ and put

$$
z=W(\widetilde s_1,\ldots,\widetilde s_d).
\tag{2.4}
$$

Write

$$
\operatorname{ord}(z)=p^a q,\qquad p\nmid q,\qquad
\operatorname{ord}(b)=p^r.
\tag{2.5}
$$

Choose $e$ satisfying

$$
qe\equiv1\pmod {p^r}.
\tag{2.6}
$$

Then

$$
\boxed{\widetilde b=z^{qe}}
\tag{2.7}
$$

is a $p$-element and $\phi(\widetilde b)=b$.

#### Proof

Equation (2.4) gives $\phi(z)=b$.  Since the order of an image divides
the order of the source, $r\le a$.  The exponent $qe$ is a multiple of
the prime-to-$p$ part of $\operatorname{ord}(z)$, so $z^{qe}$ has
$p$-power order.  On the other hand,

$$
\phi(z^{qe})=b^{qe}=b
\tag{2.8}
$$

by (2.6).  This proves the claim. $\square$

There is also a structural form.  Put $L=\phi^{-1}(P)$.  The restriction
$L\to P$ is onto, and every Sylow $p$-subgroup $T$ of $L$ maps onto $P$.
Indeed

$$
|T|=|L|_p=|\ker\phi|_p|P|,
\tag{2.9}
$$

whereas $|T\cap\ker\phi|\le|\ker\phi|_p$; hence
$|\phi(T)|\ge|P|$, and equality is forced.  Formula (2.7) is the pointed,
computable version of this Sylow argument.

## 3. Recursive pointed construction

Let

$$
G_0\xleftarrow{\phi_0}G_1
\xleftarrow{\phi_1}G_2\xleftarrow{}\cdots
\tag{3.1}
$$

be an inverse system of finite groups.  Fix a $p$-element $b_0\in G_0$.

Suppose recursively that, after $b_n$ has been constructed, one can:

1. choose a Sylow $p$-subgroup $P_n\le G_n$ containing $b_n$;
2. choose a finite generating set
   $P_n=\langle s_{n,1},\ldots,s_{n,d_n}\rangle$;
3. exhibit, for every $j$, one lift
   $\widetilde s_{n,j}\in G_{n+1}$ with
   $\phi_n(\widetilde s_{n,j})=s_{n,j}$.

Then the word-and-power construction (2.3)--(2.7) produces a $p$-element
$b_{n+1}$ satisfying

$$
\phi_n(b_{n+1})=b_n.
\tag{3.2}
$$

Choose a Sylow $p$-subgroup containing $b_{n+1}$ and repeat.

### Theorem 3.1 (POINTED-SYL-COFINAL)

Under the recursive hypotheses above, there is a compatible sequence

$$
(b_n)_{n\ge0}\in\varprojlim G_n
\qquad\text{whose zeroth coordinate is the prescribed }b_0.
\tag{3.3}
$$

Moreover, given multiplication, order, Sylow, membership-word, and
generator-lift certificates in the finite groups, (2.4) and (2.7) are an
explicit finite algorithm for every $b_{n+1}$.

#### Proof

Inductively apply Lemma 2.1.  Equation (3.2) is the required compatibility,
so the resulting sequence is an element of the inverse limit. $\square$

This theorem requires genuine groups and genuine homomorphisms.  A list of
solutions to a truncated residual, or an affine correction fibre not proved
closed under the GT product, cannot be substituted for the $G_n$.

## 4. R07 specialization

The rung K2 is a B3 normal subgroup, not itself a B4 window.  Let

$$
J_0\ge J_1\ge J_2\ge\cdots,
\qquad J_n\in\mathcal I_4(K2),
\tag{4.1}
$$

be a nested cofinal ladder of isolated B4 windows whose induced arity-three
kernels satisfy $(J_n)_3\le K2$.  Thus each has a canonical restriction
map to the fixed K2 B3 group.  Form the augmented inverse system

$$
H_0=GT_3(K2),\qquad
H_{n+1}=\mathcal{ML}(J_n)\quad(n\ge0),
\tag{4.2}
$$

using the B3-component map $H_1\to H_0$ at the first edge and canonical
B4 reduction maps thereafter.

Assume the standard finite-shadow inverse-limit identification for this
cofinal ladder,

$$
\varprojlim_n\mathcal{ML}(J_n)\cong\widehat{GT},
\tag{4.3}
$$

with the canonical transition homomorphisms.  Take

$$
p=3,\qquad b_0=R07.
\tag{4.4}
$$

Proposition 1.1 starts the recursion.  Therefore:

### Corollary 4.1 (R07-SYL3-WITNESS-CRITERION)

If, at every edge $H_{n+1}\to H_n$ of the augmented system (4.2), a
generating set of a Sylow $3$-subgroup of $H_n$ containing the recursively
constructed $b_n$ has lifts to $H_{n+1}$, then there exists

$$
\widehat b\in\widehat{GT}
\tag{4.5}
$$

whose exact K2 coordinate is R07.

Since R07 reduces to the pinned outside roof row 36, such a $\widehat b$
is outside the arithmetic image.  It is therefore an Ihara
non-surjectivity witness.

Unlike v50, this conclusion cannot switch from R07 to R40: compatibility
starts at the order-nine point R07 itself.

At the initial edge, Proposition 1.2 removes the Sylow-choice ambiguity:
the subgroup containing R07 is the canonical $P_0\cong X^2$.  The first
finite task is therefore to lift a generating set of this particular
$P_0$ through $\mathcal{ML}(J_0)\to GT_3(K2)$.

## 5. What is solved and what remains

The new facts are:

$$
\boxed{
\operatorname{ord}(R07)=9,\qquad
\operatorname{Syl}_3(GT_3(K2))=P_0\cong X^2,\qquad
\text{Sylow-3 generator lifts at every edge force a cofinal lift of R07.}}
\tag{5.1}
$$

The sequence is constructive once the finite generator lifts are given:
at each edge use one membership word $W_n$ and one exponent $q_ne_n$.
No independent compatibility choice for the corrections $c_n$ remains.

The first edge in Corollary 4.1 is the typed B4-component problem
$\mathcal{ML}(J_0)\to GT_3(K2)$; it must not be silently replaced by a
B3-only refinement.

The missing input is still substantial.  The present repository has no
serialized actual isolated B4 $PSL(2,8)$-strip occurrence roster carrying
all theta, tau, and literal A.18 labels and defects.  Consequently v59
cannot yet decide the nonabelian strip edges, and the generator-lift
hypothesis of Corollary 4.1 has not been established on a cofinal ladder.

Thus (5.1) is a sharper positive route, not a declaration that R07 is
already genuine.  A complete empty R07 fibre at one finite isolated window
would still prove R07 fake.  Failure of one selected Sylow generating set,
without complete fibre coverage, proves neither fake nor genuine.

## 6. Pinned finite sources

- `ci/ordinary_idx3_artifacts_32682548731/`
  `d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json`:
  complete 48-point K2 row-36 fibre, R07/R40 positives, R07 coordinates and
  signed word.
- `sol/luna_reply_159o_ordinary_idx3_crosscheck_v1.md`:
  independent replay of the complete ordinary K2 fibre.
- `docs/week1-定義ノート.md`, equation (3.53)/(3.41) ledger:
  canonical GT multiplication and $E_{m,f}$ convention.
- `sol/proof_r07_sylow_generator_cofinal_witness_criterion_v50.md`:
  the unpointed roof-fullness criterion strengthened here.
