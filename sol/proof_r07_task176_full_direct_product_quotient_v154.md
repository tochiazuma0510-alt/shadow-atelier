# R07 task176 full direct-product quotient v154

Author: Sol / 2026-08-27

Status: paper theorem and task185 repair contract.  The canonical
\(PSL(2,8)\) residual of the task176 joint group is a direct factor of the
whole group, not only of the inverse image of the \(PSL(2,8)\) factor.  The
708,588-element no-\(PSL(2,8)\) quotient can therefore be materialized as a
marked subgroup, without enumerating the 357,128,352-element ambient group
or relabelling the 1,469,664-element \(Q_0\) tree.  No arithmetic quotient
coordinate, cofinal lift, fake certificate, or Ihara witness is declared.

## 1. Frozen extension and canonical residual

Let

\[
 1\longrightarrow\Gamma\longrightarrow G
 \stackrel{\pi}{\longrightarrow}S\times G_9
 \longrightarrow1,
 \qquad S=PSL(2,8),
\tag{1.1}
\]

be the task157ee/task176 joint extension, where

\[
 |\Gamma|=243,
 \qquad |S|=504,
 \qquad |G_9|=2916.
\tag{1.2}
\]

Write \(\pi_S\) and \(\pi_9\) for the two components of \(\pi\), and put

\[
 E=\pi^{-1}(S\times1).
\tag{1.3}
\]

V149 proves that there is a unique canonical subgroup

\[
 R=\widetilde S=C_E(\Gamma)'=E^{(\infty)}
 \cong S
\tag{1.4}
\]

such that

\[
 E=\Gamma\times R,
 \qquad R=R_S(G),
 \qquad \pi_S|_R:R\xrightarrow{\sim}S.
\tag{1.5}
\]

Let

\[
 \iota=(\pi_S|_R)^{-1}:S\xrightarrow{\sim}R.
\tag{1.6}
\]

## 2. The residual is a direct factor of the whole joint group

Define the complementary preimage

\[
 C=\ker\pi_S=\pi^{-1}(1\times G_9).
\tag{2.1}
\]

Thus \(C\) fits into the exact sequence

\[
 1\longrightarrow\Gamma\longrightarrow C
 \longrightarrow G_9\longrightarrow1.
\tag{2.2}
\]

### Theorem 2.1 (FULL DIRECT-PRODUCT SPLITTING)

One has

\[
 \boxed{
 G=R\times C,
 \qquad C=C_G(R).}
\tag{2.3}
\]

In particular,

\[
 \boxed{
 |C|=|\Gamma|\,|G_9|=708,588,
 \qquad C\xrightarrow{\sim}G/R.}
\tag{2.4}
\]

#### Proof

The subgroup \(R\) is normal in \(G\) by v149.  If \(c\in C\) and
\(r\in R\), then \(crc^{-1}\in R\), while

\[
 \pi_S(crc^{-1})=\pi_S(r).
\tag{2.5}
\]

Restriction of \(\pi_S\) to \(R\) is injective, so (2.5) gives
\(crc^{-1}=r\).  Hence \([C,R]=1\).

For \(g\in G\), put \(s=\pi_S(g)\).  Then

\[
 \iota(s)^{-1}g\in C,
\tag{2.6}
\]

so \(G=RC\).  If \(r\in R\cap C\), then \(\pi_S(r)=1\); injectivity on
\(R\) gives \(r=1\).  Together with \([C,R]=1\), this proves
\(G=R\times C\).

It remains to identify the centralizer.  We already know
\(C\leq C_G(R)\).  If \(g\in C_G(R)\), then \(\pi_S(g)\) centralizes every
element of \(S=\pi_S(R)\).  Since \(S\) is centerless,
\(\pi_S(g)=1\), so \(g\in C\).  Thus \(C=C_G(R)\).  Equation (2.2) gives
the order in (2.4), and restriction of the quotient map has trivial kernel
and is onto by \(G=RC\). \(\square\)

The proof uses the direct-factor structure of \(Q_0=S\times G_9\), the
normality of the canonical complement \(R\), and the injectivity of its
\(S\)-projection.  It does not choose a section of (1.1).

## 3. Canonical quotient retraction

Define

\[
 \boxed{
 \kappa:G\longrightarrow C,
 \qquad
 \kappa(g)=\iota(\pi_S(g))^{-1}g.}
\tag{3.1}
\]

### Corollary 3.1 (MARKED NO-S RETRACTION)

The map \(\kappa\) is a surjective homomorphism with

\[
 \boxed{
 \ker\kappa=R,
 \qquad \kappa|_C=1_C.}
\tag{3.2}
\]

Thus it is the canonical marked realization of \(G\twoheadrightarrow G/R\)
inside \(G\).

#### Proof

By Theorem 2.1, every \(g\) has a unique expression \(g=rc\), with
\(r\in R\) and \(c\in C\).  Equation (3.1) returns exactly \(c\).
Projection to one factor of an internal direct product is a homomorphism,
and (3.2) follows. \(\square\)

If \(x_G,y_G\) are the two marked generators of \(G\), then

\[
 x_C=\kappa(x_G),
 \qquad y_C=\kappa(y_G)
\tag{3.3}
\]

generate \(C\).  Indeed, \(\kappa\) is onto and \(x_G,y_G\) generate
\(G\).  Consequently the required 708,588-state prefix-closed Schreier tree
is the positive \(x_C,y_C\) first-seen Cayley tree of the subgroup \(C\).
It is not the task176 \(Q_0\) tree, whose order is
\(504\cdot2916=1,469,664\).

## 4. Simplified finite relative-arithmetic selector

For \(a\in S\), v150 defines

\[
 \Lambda_a(f)
 =f\,\iota(\pi_S(f)^{-1}a).
\tag{4.1}
\]

### Corollary 4.1 (DIRECT-FACTOR ANCHOR FORMULA)

For every \(f\in G\),

\[
 \boxed{
 \Lambda_a(f)=\iota(a)\,\kappa(f).}
\tag{4.2}
\]

Hence the finite relative-arithmetic correction preserves exactly the
\(C\)-coordinate and replaces exactly the \(R\)-coordinate by
\(\iota(a)\).

#### Proof

Write \(f=\iota(s)c\), where \(s=\pi_S(f)\) and
\(c=\kappa(f)\).  The two direct factors commute, so

\[
 f\,\iota(s^{-1}a)
 =\iota(s)c\,\iota(s^{-1}a)
 =\iota(a)c.
\tag{4.3}
\]

This is (4.2). \(\square\)

For the frozen candidate \(b_{760}\), the coarse arithmetic-anchor test is
therefore

\[
 \pi_S(b_{760})=a_{07,S},
 \qquad
 \kappa(b_{760})\in\kappa(\mathcal A_{07,G}).
\tag{4.4}
\]

The first coordinate is already the R07 coordinate.  The second remains an
arithmetic input; the direct-product theorem does not assert that the
arithmetic image is all of \(C\).

## 5. Exact task185 materialization contract

A sound task185 producer may avoid enumerating all of \(G\), but it must do
the following.

1. Reconstruct the 243-state group \(\Gamma\), the subgroup
   \(E=\pi^{-1}(S\times1)\), and the canonical 504-state complement
   \(R=C_E(\Gamma)'\) as required by v149.
2. Retain source words and the exact \(S\)-projection for every element of
   \(R\), thereby materializing \(\iota\).
3. Compute the two literal marked elements (3.3), directly check that they
   centralize a generating set of \(R\), and enumerate their subgroup
   \(C_0=\langle x_C,y_C\rangle\).
4. Require \(|C_0|=708,588\), trivial intersection with \(R\), the exact
   sequence (2.2), and direct replay of the task157ee presentation after
   applying \(\kappa\).
5. Retain the complete 708,588-state prefix-closed parent/letter tree and
   verify that every parent edge is an actual \(x_C\)- or \(y_C\)-edge.
6. Independently reconstruct \(R\), \(\kappa(x_G),\kappa(y_G)\), the Cayley
   tree, all orders, and the quotient relation replay.
7. Reject a 1,469,664-entry \(Q_0\) parent table or digest presented as the
   708,588-entry \(C\) tree.

The last gate is load-bearing.  The two groups have different orders and
different marked generators even though both are built from the same frozen
task176 extension.

## 6. Boundary

```text
R_S(G)=tilde-S:                                  PAPER_PROOF (v149)
G=tilde-S x C_G(tilde-S):                        PAPER_PROOF
C_G(tilde-S) ~= G/tilde-S, order 708,588:        PAPER_PROOF
CANONICAL MARKED RETRACTION kappa:                PAPER_PROOF
FINITE ANCHOR Lambda_a(f)=iota(a)kappa(f):        PAPER_PROOF
WORD-BEARING tilde-S / 708,588-STATE C TREE:      TASK185 REPAIR REQUIRED
ARITHMETIC R07 COORDINATE IN C:                   UNKNOWN_INPUT
TASK179 DIRECT SUCCESSOR:                         INDEPENDENT / IN PROGRESS
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:   NOT DECLARED
```

`R07_TASK176_FULL_DIRECT_PRODUCT_QUOTIENT_V154_PAPER_GRADE`
