# R07 independent left-Fox checker contract v292

Author: Sol / 2026-08-29

Status: paper-grade independence and recurrence theorem for the A4-v5
checker.  It separates the public finite-group arithmetic which producer and
checker may share from the word substitution, Fox scan, and PB3/PB4 relation
grammar which the checker must implement independently.  It does not accept
the live v5 source, execute A4, compute an ordered K basis, or construct a
compatible lift, fake certificate, or Ihara witness.  `verified=false`.

## 1. Independence boundary

Fix one authenticated marked quotient

\[
 G=\langle \bar A_1,\ldots,\bar A_m\rangle
\tag{1.1}
\]

and the sparse left module with typed basis symbols \((j,g)\), where
\(1\leq j\leq m\) and \(g\in G\).  Producer and checker may share only the
literal marked quotient representation and its public operations

\[
 1_G,\qquad (g,h)\mapsto gh,\qquad g\mapsto g^{-1},
 \qquad \bar A_1,\ldots,\bar A_m.
\tag{1.2}
\]

They must not both call one producer-owned routine for free-word
substitution, Fox collection, `pure_relations`, composite affine evaluation,
or row assembly.  Otherwise equality of their outputs can preserve the same
implementation error and is not an independent checker result.

The current unexecuted A4-v5 draft was found to call the same pinned
`d972_b345_seedspan_triple4_v1.py` implementations of
`f2_substitute`, `fox_gradient_without_sections`, and `pure_relations` on
both sides.  Those calls are therefore outside the admissible boundary
(1.2).  This is a static implementation finding, not an A4 mathematical
terminal.

## 2. Checker-local word grammar

A signed word is a list in \(\{\pm1,\ldots,\pm m\}\).  The checker defines
free reduction locally by deleting adjacent \(a,-a\), defines

\[
 (a_1\cdots a_r)^{-1}=(-a_r)\cdots(-a_1),
\tag{2.1}
\]

and substitutes a signed free generator by its supplied literal image or
the independently reduced inverse image.  The paper-product convention is
also local and explicit:

\[
 \operatorname{PP}(w_1,\ldots,w_r)
   =\operatorname{red}(w_r\cdots w_1).
\tag{2.2}
\]

Thus the ten F2-to-PB contexts are reconstructed from literal signed words,
not by importing a composite substitution helper.  The result is compared
letter-for-letter with the authenticated ancestry word before any affine
value is accepted.

## 3. Independent left-Fox scan

For a PB word \(w=\ell_1\cdots\ell_N\), define a prefix \(p_0=1_G\) and a
sparse vector \(u_0=0\).  At step \(r\), put \(j=|\ell_r|\) and use exactly
one of the following two transitions:

\[
\begin{array}{c|c|c}
\ell_r>0 & u_r=u_{r-1}+[j,p_{r-1}]
          & p_r=p_{r-1}\bar A_j,\\[2mm]
\ell_r<0 & p_r=p_{r-1}\bar A_j^{-1}
          & u_r=u_{r-1}-[j,p_r].
\end{array}
\tag{3.1}
\]

All coefficients are reduced in \(\mathbf F_3\), so the minus sign is the
coefficient 2.  No prefix word or section word is retained.  The checker
returns

\[
 \mathcal A_{\rm chk}(w)=(p_N,u_N).
\tag{3.2}
\]

### Proposition 3.1 (LEFT-FOX RECURRENCE)

The local scan (3.1) is the exact left-Fox affine value.  In particular,

\[
 \mathcal A_{\rm chk}(uv)
  =(p_up_v,\;u_u+p_u\cdot u_v),
\qquad
 \mathcal A_{\rm chk}(u^{-1})
  =(p_u^{-1},-p_u^{-1}\cdot u_u).
\tag{3.3}
\]

#### Proof

For a positive letter, the left Fox derivative contributes the current
prefix and then advances the endpoint.  For a negative letter,
\(\partial A_j^{-1}=-A_j^{-1}\partial A_j\); hence the endpoint advances
first and the contribution is the negative new prefix.  This is exactly
(3.1).  Induction on word length proves (3.2).  Splitting the scan after the
last letter of \(u\) translates every contribution of \(v\) by \(p_u\),
giving the product formula.  Applying that formula to \(uu^{-1}=1\) gives
the inverse formula. \(\square\)

Consequently a reverse suffix DAG may combine immutable checker-local actor
values by (3.3).  A direct checker scan is needed only for the forty signed
actors, the 65 base relation words, fixed canaries, every newly accepted K
word, and the final ordered K/anchor support; it is not a second flat replay
of all 6,441 long rows.

## 4. Independent PB3/PB4 seed grammar

The checker also constructs the ordered relation words without calling the
producer's `pure_relations`.  Let

\[
 P_n=((1,2),(1,3),\ldots,(n-1,n))
\tag{4.1}
\]

in lexicographic order, and let `idx_n(i,j)` be the one-based position of
\((i,j)\).  Define the Artin action on free generators locally by

\[
\begin{array}{c|cc}
\sigma_i & X_i\mapsto X_iX_{i+1}X_i^{-1}
         & X_{i+1}\mapsto X_i,\\
\sigma_i^{-1} & X_i\mapsto X_{i+1}
         & X_{i+1}\mapsto X_{i+1}^{-1}X_iX_{i+1},
\end{array}
\tag{4.2}
\]

with every other generator fixed.  The literal pure-braid word for
\(A_{ij}\) is

\[
 \sigma_{j-1}\cdots\sigma_{i+1}\sigma_i^2
 \sigma_{i+1}^{-1}\cdots\sigma_{j-1}^{-1}.
\tag{4.3}
\]

Starting from no relations at rank 2, embed the rank-\((n-1)\) relations in
the first \(|P_{n-1}|\) generators.  Then, for each \((i,j)\in P_{n-1}\)
and each \(1\leq k<n\), append the relation

\[
 A_{ij}^{-1}A_{k,n}A_{ij}\,
 \bigl(A_{k,n}^{A_{ij}}\bigr)^{-1},
\tag{4.4}
\]

where the second word is obtained by the locally computed Artin action
(4.2)--(4.3), substituted into
\((A_{1,n},\ldots,A_{n-1,n})\).  Free reduction and ordering are those of
Section 2.

### Proposition 4.1 (THE 65 CHECKER-LOCAL SEEDS)

The recurrence (4.1)--(4.4) returns exactly 2 ordered PB3 relation words and
11 ordered PB4 relation words.  Evaluating them by (3.1) in the five PB3 and
five PB4 contexts gives

\[
 5\cdot2+5\cdot11=65
\tag{4.5}
\]

tagged base boundary rows.

#### Proof

At rank 3, the old roster is empty and (4.4) contributes
\(|P_2|(3-1)=1\cdot2=2\) relations.  At rank 4 it retains those two and
adds \(|P_3|(4-1)=3\cdot3=9\), for a total of 11.  Formula (4.5) follows
from the ten fixed contexts.  The recurrence is the ordered
Fadell--Neuwirth conjugation presentation, and every literal word is fixed
by (4.1)--(4.4). \(\square\)

The checker must compare the resulting 2/11 literal roster, order and digest
with the authenticated owners.  Matching only the counts in (4.5) is not
sufficient.

## 5. End-to-end independent row criterion

For each of the 288 immutable primitive words, the checker inserts the
locally constructed signed-actor values into its reverse suffix DAG and
uses the right-associated form of (3.3).  Each authority row then has three
separate gates:

1. its checker-local ancestry grammar reconstructs the stored literal word;
2. its reverse DAG reconstructs the ten exact affine values; and
3. its canonical typed row is compared with the producer's streamed row
   owner only after both computations are complete.

The boundary oracle begins from the 65 rows of Proposition 4.1 and performs
the v274 support-inversion calculation locally.  The final certificate must
compare producer and checker boundary spans in both directions and compare
the chronological K relations in the common raw grammar of v285.  Equal
rank, equal seed count, or one shared helper digest is not a substitute for
these containments.

### Theorem 5.1 (ADMISSIBLE A4 CHECKER INDEPENDENCE)

Assume the checker uses only (1.2) from the shared quotient source, implements
Sections 2--4 locally, reconstructs all rows and lazy full-boundary
transitions as in Section 5, and passes the two-way span and v285 raw-relation
comparisons.  Then agreement with the forward producer is an independent
cross-check of the A4 affine/Fox and boundary calculations, up to the shared
finite-group arithmetic explicitly isolated in (1.2).

#### Proof

Proposition 3.1 proves the checker-local affine evaluator from the public
group law.  Proposition 4.1 supplies an independently generated complete
base roster.  The reverse DAG and forward producer have different word
factorizations, while the literal ancestry gate fixes their common input.
The v274 oracle tests every full translated boundary column, and two-way
containment removes dependence on either side's pivot coordinates.  V285
then compares the K/action data in the common raw ledger grammar.  Therefore
the only shared executable premise is the declared group law (1.2), not the
Fox or boundary implementation under test. \(\square\)

## 6. Fixed frontier

```text
CHECKER-LOCAL LEFT-FOX SCAN:                    PAPER PROOF
CHECKER-LOCAL PB3/PB4 2/11 RELATION GRAMMAR:    PAPER PROOF
SHARED PUBLIC GROUP-OPERATION BOUNDARY:         FIXED
SHARED PRODUCER FOX/PURE_RELATION HELPERS:      REJECTED FOR INDEPENDENCE
A4-v5 IMPLEMENTATION OF THIS CONTRACT:          IN PROGRESS
ACTUAL A4 ORDERED K BASIS:                       NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                  NONE
```

`R07_INDEPENDENT_LEFT_FOX_CHECKER_CONTRACT_V292_PAPER_GRADE`
