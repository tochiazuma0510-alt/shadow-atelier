# R07 finite relative-arithmetic anchor v150

Author: Sol / 2026-08-27

Status: paper theorem.  This note identifies the exact finite image of the
v18 relative-dihedral correction in the task176 joint group.  It reduces the
missing arithmetic input from a literal word in the full joint group to one
coset in its no-\(PSL(2,8)\) quotient.  That coset has not yet been
materialized.  No compatible cofinal lift, fake certificate, or Ihara witness
is declared.

## 1. Formation residuals commute with a finite free image

Let \(S=PSL(2,8)\), let \(\mathcal C_S\) be the formation of finite groups
having no composition factor isomorphic to \(S\), and put

\[
 \Pi_S=\ker\bigl(\widehat F_2\longrightarrow
                  F_2^{\mathcal C_S}\bigr).
\tag{1.1}
\]

For a finite continuous epimorphism

\[
 q:\widehat F_2\twoheadrightarrow G,
\tag{1.2}
\]

write \(R_S(G)\) for the \(\mathcal C_S\)-residual of \(G\).

### Lemma 1.1 (FINITE IMAGE OF THE PRO-FORMATION KERNEL)

One has the exact equality

\[
 \boxed{q(\Pi_S)=R_S(G).}
\tag{1.3}
\]

#### Proof

The quotient \(G/R_S(G)\) belongs to \(\mathcal C_S\).  Hence the composite
\(\widehat F_2\to G/R_S(G)\) kills \(\Pi_S\), and therefore

\[
 q(\Pi_S)\leq R_S(G).
\tag{1.4}
\]

Conversely, \(G/q(\Pi_S)\) is a finite continuous quotient of
\(F_2^{\mathcal C_S}\), so it belongs to \(\mathcal C_S\).  Minimality of
the formation residual gives

\[
 R_S(G)\leq q(\Pi_S).
\tag{1.5}
\]

Equations (1.4)--(1.5) prove (1.3). \(\square\)

This lemma is stronger than the one-sided observation that a relative word
is killed in every no-\(S\) quotient: every element of the finite residual
is the image of such a relative profinite word.

## 2. The canonical representative in one residual coset

Assume that \(G\) has a marked epimorphism

\[
 \pi_S:G\twoheadrightarrow S
\tag{2.1}
\]

such that restriction to the formation residual is an isomorphism:

\[
 \pi_S|_{R_S(G)}:R_S(G)\xrightarrow{\sim}S.
\tag{2.2}
\]

Write

\[
 \iota=(\pi_S|_{R_S(G)})^{-1}:S\xrightarrow{\sim}R_S(G).
\tag{2.3}
\]

For a prescribed marked value \(a\in S\), define

\[
 \boxed{
 \Lambda_a(f)
   =f\,\iota\bigl(\pi_S(f)^{-1}a\bigr),
 \qquad f\in G.}
\tag{2.4}
\]

The multiplication side in (2.4) is the right-correction convention of
v18.  A left-correction convention would require the corresponding
conjugated formula and must not be substituted silently.

### Theorem 2.1 (FINITE RELATIVE-ANCHOR SELECTOR)

For every \(f\in G\), \(\Lambda_a(f)\) is the unique element \(b\in G\)
satisfying

\[
 bR_S(G)=fR_S(G),
 \qquad
 \pi_S(b)=a.
\tag{2.5}
\]

Consequently \(\Lambda_a\) is constant on right residual cosets and induces
a canonical bijection of sets

\[
 \boxed{
 \overline\Lambda_a:G/R_S(G)
   \xrightarrow{\sim}\pi_S^{-1}(a).}
\tag{2.6}
\]

#### Proof

The correction factor in (2.4) lies in \(R_S(G)\), so the first equality in
(2.5) holds.  Applying \(\pi_S\) gives

\[
 \pi_S(\Lambda_a(f))
 =\pi_S(f)\pi_S(f)^{-1}a=a.
\tag{2.7}
\]

If \(b=fr\) is any other element satisfying (2.5), then

\[
 \pi_S(r)=\pi_S(f)^{-1}a.
\tag{2.8}
\]

The isomorphism (2.2) forces
\(r=\iota(\pi_S(f)^{-1}a)\), proving uniqueness.  In particular, replacing
\(f\) by any element of the same residual coset leaves the unique output
unchanged.  Every element of \(\pi_S^{-1}(a)\) is fixed by \(\Lambda_a\),
which proves the bijection (2.6). \(\square\)

The selector is a canonical set map, not in general a homomorphism.  Its
content is exactly the simultaneous use of the quotient coordinate and the
marked \(S\)-coordinate.

## 3. Exact finite image of the v18 correction

Fix \(e\in\{07,40\}\).  Let

\[
 (\widehat m_e,F_e)=\operatorname{Ih}(\sigma_e)
\tag{3.1}
\]

be one arithmetic dihedral base point supplied by DIH-ARITH, and let
\(a_{e,S}\in S\) be the prescribed marked \(S\)-coordinate.  V18 chooses
\(d_{\delta_e}\in\Pi_S\) with

\[
 q_S(d_{\delta_e})=\delta_e,
 \qquad
 \delta_e=q_S(F_e)^{-1}a_{e,S},
\tag{3.2}
\]

and sets

\[
 F_e^{\mathcal C}=F_ed_{\delta_e}.
\tag{3.3}
\]

### Theorem 3.1 (CHOICE-FREE FINITE CORRECTION IMAGE)

For every finite image (1.2) satisfying (2.2), put \(f_e=q(F_e)\).  Then

\[
 \boxed{
 q(F_e^{\mathcal C})
 =\Lambda_{a_{e,S}}(f_e)
 =f_e\,\iota\bigl(\pi_S(f_e)^{-1}a_{e,S}\bigr).}
\tag{3.4}
\]

Thus the finite value in (3.4) is independent of every profinite choice in
\(d_{\delta_e}\).  It depends on the arithmetic base point only through the
single quotient coordinate

\[
 f_eR_S(G)\in G/R_S(G).
\tag{3.5}
\]

#### Proof

Lemma 1.1 puts \(q(d_{\delta_e})\) in \(R_S(G)\).  Its \(S\)-image is
\(\pi_S(f_e)^{-1}a_{e,S}\).  The isomorphism (2.2) therefore forces

\[
 q(d_{\delta_e})
 =\iota\bigl(\pi_S(f_e)^{-1}a_{e,S}\bigr).
\tag{3.6}
\]

Right multiplication proves (3.4), and Theorem 2.1 proves (3.5). \(\square\)

This is the exact sense in which v18 becomes explicit at a finite joint
level.  A literal representative of \(F_e\) in the whole group \(G\) is not
needed.  Its image modulo the formation residual is sufficient.  DIH-ARITH
alone, however, proves existence of \(\sigma_e\); it does not name the
coordinate (3.5).

## 4. The arithmetic-anchor set and a lossless comparison test

Let \(d_e\) be the fixed pure-dihedral shadow and define the finite
arithmetic base set

\[
 \mathcal A_{e,G}
 =\left\{
 q(F_\sigma):
 \sigma\in G_{\mathbf Q},\ 
 \operatorname{Ih}_{K^{(36)}}(\sigma)=d_e
 \right\}\subseteq G.
\tag{4.1}
\]

Its relative-dihedral anchor set is

\[
 \mathcal B_{e,G}
 =\Lambda_{a_{e,S}}(\mathcal A_{e,G})
 \subseteq\pi_S^{-1}(a_{e,S}).
\tag{4.2}
\]

Let \(p:G\to G/R_S(G)\) be the quotient map.  Theorem 2.1 gives

\[
 \boxed{
 \mathcal B_{e,G}
 =\overline\Lambda_{a_{e,S}}
     \bigl(p(\mathcal A_{e,G})\bigr).}
\tag{4.3}
\]

Hence a literal candidate \(b\in G\) is the finite projection of a v18
relative arithmetic lift for some admissible arithmetic base point if and
only if

\[
 \boxed{
 \pi_S(b)=a_{e,S}
 \quad\text{and}\quad
 p(b)\in p(\mathcal A_{e,G}).}
\tag{4.4}
\]

This test is lossless.  It does not require guessing which full element of
\(\mathcal A_{e,G}\) was chosen, and it cannot be replaced by equality of a
dihedral key or by equality of dimensions.

## 5. Specialization to task176

V149 proves for the cross-checked task157ee/task176 joint group that

\[
 R_S(G)=\widetilde S=C_E(\Gamma)'=E^{(\infty)},
 \qquad
 \widetilde S\cap\Gamma=1,
 \qquad
 \pi_S|_{\widetilde S}:\widetilde S\xrightarrow{\sim}S.
\tag{5.1}
\]

Therefore all hypotheses of Sections 2--4 hold.  If \(b_{760}\in G\) is
the complete joint value of the frozen 760-letter word, its exact
relative-arithmetic anchor gate is

\[
 \boxed{
 \pi_S(b_{760})=a_{07,S}
 \quad\text{and}\quad
 b_{760}\widetilde S
 \in p(\mathcal A_{07,G}).}
\tag{5.2}
\]

The first condition is part of the marked R07 replay.  The second is the
only missing coarse arithmetic input.  In particular:

* one need not materialize an arbitrary lift \(d_{\delta}\) in
  \(\widehat F_2\);
* one need not choose a full task176 word for \(F_{07}\);
* one must materialize the arithmetic no-\(S\) quotient coordinate in
  \(G/\widetilde S\), or its complete finite set; and
* task179 corrections, which have identity value in \(G\), cannot change
  the truth of (5.2).

The quotient in (5.2) is an extension of the 3-group \(\Gamma\) by the
solvable group \(G_9\), hence is solvable.  This makes the required finite
input smaller, but DIH-ARITH does not by itself assert arithmetic
surjectivity onto this solvable joint-context quotient.

## 6. Separation from the direct explicit-word route

Failure to supply (5.2) blocks only the claim that \(g_{760}\) is the finite
component of the particular formation-purified v18 construction.  It does
not make the direct all-seven task175/task179 calculation invalid.

If task175/task179/task184 produce a literal successor for \(g_{760}\), that
is a direct finite relative-Frattini edge.  Iterating such authenticated
successors on a cofinal original ladder could construct a genuine lift
without first identifying \(g_{760}\) with \(F_{07}^{\mathcal C}\).  The two
routes therefore have different remaining inputs:

\[
\begin{array}{c|c}
\text{formation-purified route}&
  \text{arithmetic quotient anchor (5.2) + joint residual equation}\\
\hline
\text{direct explicit-word route}&
  \text{all-seven successor + compatible repetition at every rung.}
\end{array}
\tag{6.1}
\]

They may be joined only after an authenticated equality such as (5.2), not
by reusing the same symbol \(F_{07}^{\mathcal C}\).

```text
TASK176 FORMATION RESIDUAL:                         PAPER_PROOF (v149)
FINITE RELATIVE-CORRECTION SELECTOR:                PAPER_PROOF (this note)
DEPENDENCE ON FULL ARITHMETIC WORD:                 ELIMINATED
REQUIRED ARITHMETIC INPUT:                          ONE COSET IN G/tilde-S
ARITHMETIC COSET FOR R07:                           UNKNOWN_INPUT
g760 RELATIVE-ARITHMETIC ANCHOR TEST:               NOT YET RUN
DIRECT TASK175/179 SUCCESSOR ROUTE:                  IN PROGRESS
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:     NOT DECLARED
```

`R07_FINITE_RELATIVE_ARITHMETIC_ANCHOR_V150_PAPER_GRADE`
