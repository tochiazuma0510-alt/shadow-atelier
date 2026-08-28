# R07 ordered nonlinear residual: deeper and doubly localized v252

Author: Sol / 2026-08-28

Status: paper synthesis after v33, v37, v98, v99, v117, v194, v228,
v248, and v251.  It identifies the exact target of the nonlinear correction
which remains after ordered word materialization.  It does not prove that
this target is always in the actual correction image, and it does not declare
a compatible lift, fake certificate, or Ihara witness.  `verified=false`.

## 1. Filtered relative branch

Let \(S=PSL(2,8)\), let \(\mathcal C_S\) be the formation of finite groups
without an \(S\)-composition factor, and put

\[
 \Pi_S=\ker\bigl(\widehat F_2\longrightarrow
                    F_2^{\mathcal C_S}\bigr).
\tag{1.1}
\]

Fix the marked relative word branch and the nested matched arity-3/4/5
ladder used by v99.  Write

\[
 \Phi(F)=(H_1(F),H_2(F),P(F))
\tag{1.2}
\]

for the two literal hexagon residuals and the printed-order pentagon
residual.  The block tags are retained.  Let \(\mathcal F^k\mathcal C\)
and \(\mathcal F^k\mathcal Z\) be the complete separated correction and
residual filtrations of v117.  At an active abelian chief edge, v99 gives
the exact affine formula

\[
 [\Phi(Fc)]_k=[\Phi(F)]_k+D_{F,k}[c]_k.
\tag{1.3}
\]

The actual correction domain is not an ambient product of context kernels.
For the joint finite evaluation image

\[
 \Psi=(q_0,\psi_1,\ldots,\psi_{11}):
 \widehat F_2\twoheadrightarrow H,
\tag{1.4}
\]

v37 identifies the simultaneous relative values which preserve the coarse
mark as

\[
 \boxed{
 \Psi(\Pi_S\cap\ker q_0)=R_S(H)\cap\ker\pi_0.}
\tag{1.5}
\]

Thus every allowed value in (1.5) comes from one common source word, and all
Goursat and coface correlations are retained.

## 2. Ordered materialization raises the residual depth

Suppose

\[
 \beta_k=[\Phi(F_k)]_k
\quad\hbox{and}\quad
 v_k\in C_{F_k,k},\qquad D_{F_k,k}v_k=-\beta_k.
\tag{2.1}
\]

Retain a finite word-bearing expression

\[
 v_k=\sum_j b_j[g_ja_kg_j^{-1}],\qquad b_j\in\mathbf F_3,
\tag{2.2}
\]

in its registered order.  As in v251, lift \(0,1,2\) to word exponents
\(0,1,-1\) and define

\[
 c_k=\operatorname{Mat}(v_k)
 =\prod_j(g_ja_kg_j^{-1})^{\widetilde b_j}.
\tag{2.3}
\]

### Theorem 2.1 (ONE-STEP NONLINEAR DEPTH GAIN)

If every factor in (2.3) lies in \(\mathcal F^k\mathcal C\), then

\[
 \boxed{\Phi(F_kc_k)\in\mathcal F^{k+1}\mathcal Z.}
\tag{2.4}
\]

This conclusion concerns the exact literal group words, not only their raw
additive Fox chains.

#### Proof

V251 Lemma 3.1 says that (2.3) represents precisely \(v_k\) in the active
elementary-abelian chief factor.  Apply the exact chief-layer affine formula
(1.3):

\[
 [\Phi(F_kc_k)]_k
 =\beta_k+D_{F_k,k}v_k=0.
\tag{2.5}
\]

Vanishing of the active quotient is exactly membership in the next residual
filtration, which proves (2.4).  The crossed-prefix terms in the exact Fox
product rule are not discarded; equation (2.4) locates them in the next
layer. \(\square\)

Theorem 2.1 is stronger and safer than asking whether the raw additive Fox
chain is group-like.  A nonsingleton group-like canary can coexist with
(2.4), as v251 Proposition 2.1 shows.

## 3. Formation and Brunnian localization of the new residual

Assume the authenticated relative typing

\[
 F_k=F_{\rm arith}u_k,\qquad u_k\in\Pi_S,\qquad
 F_k\in[\widehat F_2,\widehat F_2],\qquad
 c_k\in\Pi_S\cap\ker q_0\cap[\widehat F_2,\widehat F_2].
\tag{3.1}
\]

The arithmetic word satisfies the two hexagons and pentagon.  By v33,
evaluation of any word from \(\Pi_S\) in a finite context group \(G\) lies
in \(R_S(G)\).  Equivalently, after quotienting each context group by its
formation residual, both \(u_k\) and \(c_k\) disappear and the relation word
becomes the corresponding relation word for \(F_{\rm arith}\), hence becomes
trivial.  Therefore

\[
 H_1(F_kc_k)\in R_S(G_{H1}),\qquad
 H_2(F_kc_k)\in R_S(G_{H2}),\qquad
 P(F_kc_k)\in R_S(G_P).
\tag{3.2}
\]

The last two clauses of (3.1) also imply that \(F_kc_k\) is a commutator
word.  BRUN-DEF therefore gives

\[
 P(F_kc_k)\in B_P,qquad
 B_P=\operatorname{Im}(\operatorname{Brun}_4\to G_P).
\tag{3.3}
\]

### Theorem 3.1 (DEEP DOUBLE LOCALIZATION)

Under all hypotheses of Theorem 2.1 and (3.1), the exact residual after
ordered materialization lies
in

\[
 \boxed{
 \mathcal F^{k+1}\mathcal Z\ \cap\
 \bigl(
 R_S(G_{H1})\times R_S(G_{H2})\times
 (B_P\cap R_S(G_P))
 \bigr).}
\tag{3.4}
\]

At the next finite edge, the correction values must still be taken from the
joint common-word subgroup (1.5), not from the product of the three displayed
targets.

#### Proof

The depth assertion is Theorem 2.1.  The three formation assertions are
(3.2), and the extra pentagon assertion is (3.3).  Intersecting them gives
(3.4).  Equation (1.5) is v37 Theorem 3.2 and supplies the final typing
statement. \(\square\)

This is a residual-location theorem.  It does not assert that the restricted
affine correction map is onto (3.4).

## 4. Why the A8 boundary is not the nonlinear correction

After the three A7 endpoints vanish, v194 and v197 return

\[
 q_{H1}\in k[PB_3]^{R_3},\quad
 q_{H2}\in k[PB_3]^{R_3},\quad
 q_P\in k[PB_4]^{R_4},
\qquad D_{2,B}q_B=z_B(M).
\tag{4.1}
\]

These are coefficients on three separately tagged presentation-relator
modules.  In contrast, a nonlinear correction is one word in
\(\Pi_S\cap\ker q_0\subset\widehat F_2\), whose eleven context values lie in
the joint image (1.5).  The construction of (4.1) supplies no map

\[
 \bigoplus_B k[PB_{r(B)}]^{R_B}\longrightarrow
 \Pi_S\cap\ker q_0
\tag{4.2}
\]

intertwining all eleven occurrences.  Such a map would itself be the missing
common-word lifting theorem.

### Proposition 4.1 (BOUNDARY/NONLINEAR TYPE SEPARATION)

The A8 identities (4.1) certify the completed linear multiplier equation,
but they neither construct nor imply a common-word correction of the exact
nonlinear residual (3.4).

#### Proof

The source of (4.1) is the direct sum of three independent cellular
\(C_2\)-modules.  Its only asserted image is the direct sum of the three
cellular \(C_1\)-modules.  The source of a legal correction is the single
joint word image (1.5).  No map of the type (4.2) occurs in v194 or v197;
forgetting this distinction would allow independent coface choices and
contradict the exact common-word equality (1.5). \(\square\)

## 5. Localized adaptive completion criterion

Let \(\beta_{k+1}=\Phi(F_kc_k)\) be the literal residual in (3.4).  At an
abelian next edge, form the actual affine map

\[
 D_{F_{k+1},k+1}:C^{\rm rel}_{F_{k+1},k+1}\longrightarrow
 Z^{\rm loc}_{k+1},
\tag{5.1}
\]

where the source is obtained from (1.5) with the commutator and registered
side gates, and the target is the localized group in (3.4).  At a nonabelian
edge use the literal finite ONE-STEP-REL accepted set in the same joint
image.

### Corollary 5.1 (LOCALIZED ONE-PATH HENSEL CRITERION)

If at every encountered abelian edge

\[
 -\beta_k\in
 D_{F_k,k}(C^{\rm rel}_{F_k,k})
\tag{5.2}
\]

with a computable word-bearing admissible preimage, and every encountered
nonabelian accepted set is nonempty, then the ordered corrections converge
to one compatible relative lift.

#### Proof

Apply v117 Theorem 3.1, using Theorem 3.1 to restrict each actual target and
v37 to retain one-word typing.  V98 supplies compatible ordinary word
spellings and convergence. \(\square\)

The advance is the strict target reduction (3.4), not a proof of (5.2).
Neither BRUN-DEF nor one A7 pass proves the quantified membership in (5.2).

## 6. Executable frontier

After an actual A5--A8 positive package, the next receipt should:

1. materialize the finite Neumann partial value in the retained factor order;
2. replay the literal H1, H2, and printed pentagon words;
3. certify that the first nonzero residual has the depth and support in
   (3.4);
4. construct the exact joint domain (1.5), including its source-word ancestry;
5. return a genuine affine MEMBER ancestry, a complete separating dual, or
   `UNKNOWN_RESOURCE`; and
6. on MEMBER, iterate without rebuilding unrelated coarse gates.

No raw-Fox group-like test and no second PB boundary search is load-bearing.

```text
ORDERED MATERIALIZATION KILLS THE ACTIVE CHIEF LAYER: PAPER PROOF
NEW EXACT RESIDUAL IS ONE LAYER DEEPER:               PAPER PROOF
H1/H2 RESIDUALS ARE FORMATION-SUPPORTED:              PAPER PROOF / ACTUAL BINDING PENDING
P RESIDUAL IS BRUNNIAN ∩ FORMATION-SUPPORTED:         PAPER PROOF / ACTUAL BINDING PENDING
LEGAL NEXT VALUES USE THE JOINT COMMON-WORD IMAGE:    PAPER PROOF (v37)
A8 PB BOUNDARY AS A NONLINEAR WORD CORRECTION:        TYPE-INVALID
UNIFORM MEMBERSHIP OF THE ACTUAL LOCALIZED RESIDUAL: OPEN
NONABELIAN ACCEPTED-SET NONEMPTINESS:                 OPEN
COMPATIBLE LIFT / FAKE / IHARA:                       NOT CONSTRUCTED
```

`R07_ORDERED_NONLINEAR_RESIDUAL_DOUBLE_LOCALIZATION_V252_PAPER_GRADE`
