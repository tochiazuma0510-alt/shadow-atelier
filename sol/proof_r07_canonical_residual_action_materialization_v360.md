# R07 canonical residual-action materialization (v360)

Author: Sol / 2026-08-30

Status: paper algorithm after v149, v151 and v287.  The frozen task157ee
factor split words and the accepted 243-state task176 kernel are sufficient
to materialize two canonical word-bearing generators of
\(R_S(\Delta_0)=\widetilde S\); no 357,128,352-state joint-group roster and
no 708,588-state arithmetic quotient tree are needed.  Composing their words
with a positive A4 action receipt then computes the exact legal relative
source \([\widetilde S,K]\).  The bounded construction has not yet been run
on a positive A4 artifact, so no source rank, lift, fake certificate or Ihara
witness is declared.  `verified=false`.

## 1. Physical finite input

Retain the task176 extension of v149,

\[
 1\longrightarrow\Gamma\longrightarrow G
 \stackrel{\pi}{\longrightarrow}S\times G_9\longrightarrow1,
 \qquad |\Gamma|=243,
 \qquad S=PSL(2,8).
\tag{1.1}
\]

Put \(E=\pi^{-1}(S\times1)\).  V149 proves

\[
 E=\Gamma\times\widetilde S,
 \qquad
 \widetilde S=C_E(\Gamma)'=E^{(\infty)},
 \qquad
 R_S(G)=\widetilde S,
\tag{1.2}
\]

and the complement \(\widetilde S\) is unique.

The frozen task157ee owner contains four literal split words.  The first two,
say \(p_1,p_2\in F(x,y)\), project to the two frozen generators
\(\bar s_1,\bar s_2\) of \(S\times1\); the other two project to the
\(G_9\)-factor.  It also contains a complete two-generator presentation

\[
 S\cong\langle a,b\mid r_1,\ldots,r_5\rangle.
\tag{1.3}
\]

V287 identifies the lossless task176 owners needed below: the complete
243-state \(\Gamma\) table, a source word for every state, the marked
\(x,y\) action on that table, and the literal ten-coordinate evaluator.
These are finite semantic owners, not only hashes or cardinalities.

## 2. Removing the inner \(\Gamma\)-action

For \(i=1,2\), conjugation by the value of \(p_i\) induces an automorphism
of \(\Gamma\).  V149 Lemma 2.1 says its outer class is trivial.  Therefore
there is \(\gamma_i\in\Gamma\) such that

\[
 p_i h p_i^{-1}=\gamma_i h\gamma_i^{-1}
 \qquad(h\in\Gamma).
\tag{2.1}
\]

An exhaustive test of the 243 accepted states against a generating roster of
\(\Gamma\), followed by a full 243-state replay, finds all such
\(\gamma_i\).  Choose any one and put

\[
 c_i=\gamma_i^{-1}p_i.
\tag{2.2}
\]

Then

\[
 c_i\in C_E(\Gamma),
 \qquad \pi(c_i)=\bar s_i.
\tag{2.3}
\]

The choice in (2.2) is not yet canonical: all solutions of (2.1) form one
coset of \(Z(\Gamma)\), and v149 gives \(|Z(\Gamma)|=27\).

## 3. The 729-pair central correction

Enumerate

\[
 (z_1,z_2)\in Z(\Gamma)^2,
 \qquad |Z(\Gamma)^2|=27^2=729,
\tag{3.1}
\]

and set

\[
 s_1=z_1c_1,
 \qquad s_2=z_2c_2.
\tag{3.2}
\]

Evaluate the five presentation words from (1.3) at \((s_1,s_2)\) by the
literal task176 ten-coordinate multiplication, requiring identity in every
coordinate and in the accepted \(\Gamma\) table.

### Theorem 3.1 (CANONICAL RESIDUAL GENERATOR PAIR)

Exactly one pair in (3.1) passes all five relators.  Its values satisfy

\[
 \boxed{\langle s_1,s_2\rangle=\widetilde S,}
\tag{3.3}
\]

and the resulting elements are independent of the preliminary choices of
\(\gamma_1,\gamma_2\) in (2.1).

#### Proof

By (2.3), every candidate lies in

\[
 C_E(\Gamma)=Z(\Gamma)\times\widetilde S
\tag{3.4}
\]

and projects to the fixed generators \(\bar s_1,\bar s_2\).  Existence of
the complement in (1.2) gives one choice of central factors for which
\(s_1,s_2\) are the unique lifts of those quotient generators inside
\(\widetilde S\).  They satisfy (1.3), so at least one pair passes.

Conversely, a passing pair defines a homomorphism

\[
 \sigma:S\longrightarrow C_E(\Gamma)
\tag{3.5}
\]

from the complete presentation (1.3).  Its composite with \(\pi\) fixes the
two generators of \(S\), hence is the identity.  Thus \(\sigma\) is an
injective section and its image is a complement to \(\Gamma\) in \(E\).
V149's uniqueness forces this image to be \(\widetilde S\).  Since
\(\pi|_{\widetilde S}\) is an isomorphism, the lifts of the two fixed
quotient generators are unique; hence the central pair is unique.

Replacing \(\gamma_i\) by \(\gamma_i z\), \(z\in Z(\Gamma)\), replaces
\(c_i\) by \(z^{-1}c_i\) and merely reindexes (3.1).  The unique final
element \(s_i\) is unchanged.  \(\square\)

The source words are explicit: use the accepted word for \(\gamma_i\), the
accepted word for \(z_i\), and the frozen split word \(p_i\) in the order
(2.2)--(3.2), followed by the pinned free reduction.  Literal word equality
between two independent constructions is unnecessary; compare their exact
task176 values.

## 4. Feeding the positive A4 action

Let a positive A4 receipt give an ordered basis

\[
 K=\langle k_1,\ldots,k_t\rangle_{\mathbf F_3}
\tag{4.1}
\]

and exact marked action matrices \(X^{\pm1},Y^{\pm1}\).  Compose the words
from Theorem 3.1 in the frozen multiplication convention to obtain matrices
\(S_1,S_2\).  V151 and v359 then give

\[
 \boxed{
 C_{\rm rel}=R_S(\Delta_1)\cap K
 = [\widetilde S,K]
 =\operatorname{im}(S_1-I)+\operatorname{im}(S_2-I).}
\tag{4.2}
\]

One block echelon over \(\mathbf F_3\) returns a basis.  Every seed column
has the literal common-word ancestry

\[
 [s_a,k_i]\longmapsto(S_a-I)e_i
\tag{4.3}
\]

with the registered commutator convention.  It is roof-trivial and has
integer exponent sums zero.  V37 separately proves that the same finite
value has a relative-formation preimage; (4.3) is not relabelled as that
particular profinite word.

## 5. Complexity, independence and frontier

Before A4 linear algebra, the complete new group work is bounded by:

1. two scans of 243 \(\Gamma\)-states for (2.1);
2. the complete 243-state action replay for each retained solution;
3. 729 central pairs times five short \(S\)-presentation relators; and
4. one independent reconstruction using a different \(\Gamma\) order and
   different preliminary inner representatives.

There is no enumeration of \(G\), no arithmetic no-\(S\) coset, and no
708,588-state quotient tree.  The arithmetic anchor missing from task185 is
irrelevant to the residual **action** needed in (4.2).

```text
CANONICAL R_S(Delta0)=tilde-S:                     PAPER PROOF / v149
PHYSICAL PURE-S SPLIT WORDS + 243-STATE Gamma:     EXISTING FROZEN OWNERS
243 + 729 CANONICAL COMPLEMENT COMPILER:           PAPER ALGORITHM
WORD-BEARING CANONICAL RESIDUAL GENERATORS:        NOT YET MATERIALIZED
C_rel=[tilde-S,K] FROM A4 ACTION:                   PAPER ALGORITHM
POSITIVE A4 K/ACTION INPUT:                        NOT YET AVAILABLE
ACTUAL LEGAL SOURCE RANK/BASIS:                    NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:            NOT CONSTRUCTED
```

`R07_CANONICAL_RESIDUAL_ACTION_MATERIALIZATION_V360_PAPER_GRADE`
