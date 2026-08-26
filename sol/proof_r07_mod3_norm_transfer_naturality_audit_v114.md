# R07 mod-three norm-transfer audit for cofinal naturality v114

Author: Sol / 2026-08-27

Status: exact paper obstruction to one overly strong form of the v111
equivariant selector across growing three-group context images.  It separates
fixed-context Jennings lifting from genuine cofinal context enlargement.  It
does not obstruct a stagewise actual correction whose new defect reduces to
zero, and it does not prove nonexistence of an R07 lift or witness.

## 1. Why this audit is necessary

V113 compresses a stabilizer-compatible preimage by modular norm columns.
At one fixed finite context group this is exact.  Across a quotient of
three-groups, however, a norm is not preserved: fibre multiplicity is zero in
characteristic three.  Therefore ``equivariant at every stage'' and
``compatible under every refinement'' cannot be conflated without checking
how the actual defect reduces.

## 2. Norms under a three-group quotient

Let

\[
 \pi:P'\twoheadrightarrow P
\tag{2.1}
\]

be a surjection of finite three-groups, and let

\[
 \pi_*:k[P']\longrightarrow k[P],
 \qquad k=\mathbf F_3,
\tag{2.2}
\]

be the induced group-algebra map.  Let \(H'\leq P'\), put
\(H=\pi(H')\), and let

\[
 K=H'\cap\ker\pi.
\tag{2.3}
\]

### Lemma 2.1 (MODULAR NORM COLLAPSE)

For

\[
 N_{H'}=\sum_{h'\in H'}h',
 \qquad N_H=\sum_{h\in H}h,
\tag{2.4}
\]

one has

\[
 \boxed{\pi_*(N_{H'})=|K|N_H.}
\tag{2.5}
\]

Consequently, if \(K\neq1\), then

\[
 \boxed{\pi_*(N_{H'})=0.}
\tag{2.6}
\]

#### Proof

Every element of \(H\) has exactly \(|K|\) preimages in \(H'\), proving
(2.5).  A nontrivial subgroup of a three-group has order divisible by three,
so its scalar is zero in \(k\).  \(\square\)

## 3. Collapse of fixed vectors in a free orbit cover

Let

\[
 A'=k[P']^{(\mathcal R)},
 \qquad A=k[P]^{(\mathcal R)}
\tag{3.1}
\]

with the coordinatewise map induced by \(\pi_*\).  Suppose \(H'\) maps onto
\(H\).

### Proposition 3.1 (FIXED-COVER TRANSFER ZERO)

If \(K=H'\cap\ker\pi\neq1\), then

\[
 \boxed{\pi_*(A'^{H'})=0.}
\tag{3.2}
\]

#### Proof

By v113 Lemma 2.1, \(A'^{H'}\) is spanned by
\(N_{H'}g'e_r\).  Lemma 2.1 sends each such vector to

\[
 |K|N_H\pi(g')e_r=0.
\]

\(\square\)

Now let compatible equivariant correction maps be given:

\[
 \begin{array}{ccc}
 A'&\xrightarrow{B'}&Z'\\
 \downarrow&&\downarrow q\\
 A&\xrightarrow{B}&Z.
 \end{array}
\tag{3.3}
\]

### Corollary 3.2 (PERSISTENT INVARIANT CLASS NO-GO)

Assume \(z'\in Z'^{H'}\), put \(z=q(z')\), and suppose \(z\neq0\).  If
\(K\neq1\), there is no \(a'\in A'^{H'}\) with \(B'a'=z'\).

#### Proof

If such \(a'\) existed, compatibility and Proposition 3.1 would give

\[
 z=q(z')=qB'a'=B\pi_*(a')=0,
\]

a contradiction.  \(\square\)

In particular, a family of fully equivariant right inverses on a persistent
nonzero invariant subsystem cannot commute with such a quotient.  This is a
failure of that selector ansatz, not a proof that an individual preimage or a
non-equivariant compatible correction sequence does not exist.

## 4. Why chief-step defects can evade the no-go

At a genuine newly active chief edge, the fine residual class often reduces
to zero in the already settled quotient:

\[
 q(z')=0.
\tag{4.1}
\]

Then Corollary 3.2 says nothing.  Indeed norm collapse is compatible with the
same zero reduction.  Therefore every application must serialize which of
the following two situations is present:

\[
 \boxed{
 \begin{array}{ll}
 \text{persistent-class comparison:}&q(z')\neq0,\\
 \text{new chief-layer correction:}&q(z')=0.
 \end{array}}
\tag{4.2}
\]

The v99 actual Hensel recursion is designed around the second situation.
The v111 naturality theorem remains valid under its stated hypotheses, but
those hypotheses cannot be inferred merely from equivariance at the separate
finite stages.

## 5. Fixed context versus growing context

There are two distinct computations in the current R07 lane.

1. **Fixed \(\Pi_4[3]\) context, increasing Jennings depth.**  The group
   \(P\) and its orbit module stay fixed while the ideal powers
   \(I(P)^j\) decrease.  No quotient \(P'\twoheadrightarrow P\) occurs, so
   Lemma 2.1 creates no new obstruction.  V111's finite Neumann correction is
   the appropriate formula once its leading splitter is found.

2. **Cofinal B4 window refinement.**  The diagonal context image itself may
   change.  Every transition must record the induced group map, the kernel on
   the relevant stabilizer, and the reduction of the actual defect.  If a
   nonzero class persists while the stabilizer gains a nontrivial
   three-kernel, the fully equivariant natural-splitter strategy is impossible
   by Corollary 3.2 and must be weakened to a based actual-class selector.

A based selector may use the compatible accumulated-kernel spelling of v98
without extending to a module homomorphism on the whole context orbit.  Its
existence still requires actual accepted values at every active edge; this
note does not manufacture them.

## 6. Required transition receipt

Before promoting a fixed-context splitter to all refinements, record at every
context-changing transition:

```text
fine_context_group / coarse_context_group
literal generator images and surjectivity
fine stabilizer H' / coarse stabilizer H
order of H' intersect ker(pi)
fine actual defect and its literal coarse reduction
coarse reduction zero = true/false
equivariant splitter claimed = true/false
based actual-class selector used = true/false
```

The admissible promotion table is:

\[
\begin{array}{c|c|c}
H'\cap\ker\pi&q(z')&\text{conclusion}\ \hline
1&\text{any}&\text{no norm-collapse obstruction}\
\neq1&0&\text{new-layer case; continue the Hensel audit}\
\neq1&\neq0&\text{fully equivariant natural splitter impossible}.
\end{array}
\tag{6.1}
\]

```text
MOD-3 NORM TRANSFER FORMULA:                  PAPER_PROOF
PERSISTENT INVARIANT-CLASS NO-GO:             PAPER_PROOF
FIXED-CONTEXT JENNINGS APPLICATION:           UNAFFECTED
R07 COFINAL CONTEXT TRANSITION TYPING:        OPEN
BASED ACTUAL-CLASS SELECTOR IF REQUIRED:      OPEN
COMPATIBLE COFINAL R07 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```
