# R07 occurrencewise transported Jacobian and additive perturbation v357

Author: Sol / 2026-08-30

Status: paper theorem after v99, v225, v252, v263, v319--v321 and v356.
It constructs the later transported-linear operator directly from the frozen
eleven-occurrence prefixes, proves filtration gain and refinement naturality,
and removes the unnecessary Xi-linearity hypothesis from the based Neumann
repair.  On the full formation/Brunnian localized target the transport term
is automatically localized.  The actual strict free-cover surjectivity and
word-bearing leading generator solve are not yet established, so no
compatible lift, fake certificate or Ihara witness is declared.
`verified=false`.

## 1. Literal occurrence derivative

Let `k=F_3`, let `P` be the relative pro-3 correction group, and use its
Zassenhaus filtration

\[
 P=P_{(1)}\supset P_{(2)}\supset\cdots .
\tag{1.1}
\]

Let `A` be the completed legal common-word correction module and `Z` the
three-block residual module.  Their filtrations are denoted `F^r A` and
`F^r Z`.  Fix the arithmetic/roof base word `F_0`.  For each of the frozen
task198 occurrences `o=1,...,11`, retain its block, substitution, sign and
task179 prefix convention

\[
 (B(o),\rho_o,\sigma_o,P_o(F)),\qquad \sigma_o\in\{1,-1\}.
\tag{1.2}
\]

The inverse-slot convention is already included in the occurrence map
`rho_(o,*)`; in particular v225's extra base factor in a positive slot is
not inserted a second time below.  The completed Fox derivative at a base
word `F` is the finite sum

\[
 D_F(a)=\sum_{o=1}^{11}
 \sigma_o P_o(F)\,\rho_{o,*}(a).
\tag{1.3}
\]

Equation (1.3) is simply the literal product rule in the stored occurrence
order.  It is valid in the completed module, before passage to an associated
graded quotient.

Now let `u in P` and put `F_1=F_0 u`.  The two words have the same coarse
roof.  Hence, in the appropriate PB3 or PB4 relative kernel, there is a
unique literal prefix ratio

\[
 k_o(u):=P_o(F_0)^{-1}P_o(F_1),
 \qquad P_o(F_1)=P_o(F_0)k_o(u).
\tag{1.4}
\]

Every `k_o(u)` is obtained by evaluating one finite word in the substitutions
of `u`; it is not an independently selected quotient element.

### Theorem 1.1 (ELEVEN-OCCURRENCE TRANSPORT FORMULA)

The difference between the two completed derivatives is the continuous
additive operator

\[
 \boxed{
 T_u:=D_{F_1}-D_{F_0},\qquad
 T_u(a)=\sum_{o=1}^{11}\sigma_oP_o(F_0)
          (k_o(u)-1)\rho_{o,*}(a).}
\tag{1.5}
\]

It raises the Zassenhaus filtration once:

\[
 \boxed{T_u(\mathcal F^rA)\subseteq\mathcal F^{r+1}Z.}
\tag{1.6}
\]

All maps in (1.5) commute with every matched refinement.  No separate
continuity or naturality hypothesis for the transported Jacobian is needed.

#### Proof

Substitute (1.4) into (1.3) and subtract the formula for `F_0`; this gives
(1.5) term by term, with the original signs and block tags unchanged.
Because `F_0` and `F_1` have the same roof, every prefix ratio lies in the
relative kernel.  Therefore `k_o(u)-1` belongs to its augmentation ideal.
Multiplication by that ideal sends a depth-`r` occurrence chain to depth
`r+1`, proving (1.6).

Every object in (1.4)--(1.5) is evaluation of a fixed finite word, followed
by the fixed Fox product rule.  Quotient homomorphisms commute with word
evaluation, substitutions, multiplication and subtraction.  Thus the same
formula reduces at every matched finite quotient and proves naturality.
Continuity follows from the finite sum and the filtration gain.  \(\square\)

The formula is additive and `k`-linear.  It need not be Xi-linear: a fixed
left coefficient need not commute with the diagonal context algebra.  The
next section shows that such linearity is not required for the perturbation
argument.

## 2. Filtered additive based perturbation

Let `F,A,L` be complete separated linearly compact filtered `k`-vector
spaces with finite-dimensional graded pieces.  Let

\[
 q:F\twoheadrightarrow L
\tag{2.1}
\]

be a continuous strict surjection, meaning

\[
 q(\mathcal F^rF)=\mathcal F^rL
 \quad(r\geq0).
\tag{2.2}
\]

Let `B:A -> L` and `s:F -> A` be continuous filtered `k`-linear maps with

\[
 Bs=q.
\tag{2.3}
\]

Finally let `T:A -> L` be continuous and `k`-linear with

\[
 T(\mathcal F^rA)\subseteq\mathcal F^{r+1}L.
\tag{2.4}
\]

### Lemma 2.1 (STRICT FILTERED LINEAR LIFT)

There is a continuous filtered `k`-linear section

\[
 \ell:L\longrightarrow F,
 \qquad q\ell=1_L,
 \qquad \ell(\mathcal F^rL)\subseteq\mathcal F^rF.
\tag{2.5}
\]

#### Proof

Strictness makes every induced map on finite filtered quotients surjective.
Choose a `k`-linear section on the first quotient.  Inductively, lift a basis
of the next finite-dimensional graded piece through the corresponding
surjection and alter the new section by a kernel-valued map so that it
reduces to the preceding one.  This gives compatible sections on all finite
quotients.  Their inverse limit is continuous, preserves the filtration and
satisfies (2.5).  \(\square\)

This splitting is only additive.  It asserts no Xi-module section and no
canonical choice.

### Theorem 2.2 (ADDITIVE BASED NEUMANN REPAIR)

Put

\[
 K:=\ell Ts:F\longrightarrow\mathcal F^1F.
\tag{2.6}
\]

Then `qK=Ts`, the series

\[
 V=(1+K)^{-1}=\sum_{m\geq0}(-K)^m
\tag{2.7}
\]

converges, and

\[
 \boxed{s_T:=sV,\qquad (B+T)s_T=q.}
\tag{2.8}
\]

#### Proof

Equations (2.4)--(2.6) give

\[
 K(\mathcal F^rF)\subseteq\mathcal F^{r+1}F,
 \qquad qK=Ts.
\tag{2.9}
\]

Thus `K^m(F)` tends to zero and (2.7) converges.  Only additivity is used in
the following calculation:

\[
 (B+T)s=Bs+Ts=q+qK=q(1+K).
\tag{2.10}
\]

Right composition with `(1+K)^(-1)` proves (2.8).  \(\square\)

Consequently v320's Xi-linearity requirement can be replaced by the weaker
and physically correct occurrencewise additivity.  At a finite quotient,
(2.7) is a finite polynomial because `K` strictly raises depth.

## 3. Localization of the actual transport term

Retain the R07 relative typing

\[
 F_0,F_1\in F_{\rm arith}\Pi_S,
 \qquad F_0,F_1\in[\widehat F_2,\widehat F_2],
\tag{3.1}
\]

and let `a` be a legal relative commutator correction.  Write `L_loc` for
the closed filtered target generated by

\[
 R_S(G_{H1})\times R_S(G_{H2})\times
 (B_P\cap R_S(G_P)).
\tag{3.2}
\]

### Proposition 3.1 (TRANSPORT IS DOUBLY LOCALIZED)

For the operator (1.5),

\[
 \boxed{T_u(a)\in\mathcal F^{r+1}L_{\rm loc}
 \quad\text{whenever }a\in\mathcal F^rA.}
\tag{3.3}
\]

#### Proof

Evaluate the derivative difference through a finite dual-number extension
of the active abelian layer.  It is the difference between the first-order
residuals at the two relative bases `F_0` and `F_1`.  Modulo the formation
residual, both bases reduce to the arithmetic word and every legal relative
correction disappears, so both H1/H2/P first-order residuals are zero.
Their difference is therefore in the three formation residuals.

For the pentagon block, both perturbed words remain commutator words.
BRUN-DEF puts both first-order pentagon residuals in the Brunnian image, and
that image is a subgroup at the finite layer.  Their difference is again
Brunnian.  Combining these locations with the one-depth gain (1.6) proves
(3.3), and inverse limits give the completed statement.  \(\square\)

This proves the assembly, naturality and localized codomain demanded in
v320 Section 3.  It does not prove that the localized target has the strict
finite free cover (2.1)--(2.2), or that the roof-fixed common-word Jacobian
is onto that cover.

## 4. Consequence for the all-depth pro-3 recursion

Assume now that the actual localized module has a strict finite free cover
`q:F -> L_loc` and a word-bearing based lift `s` with `Bs=q`, as in v319.
Apply Theorem 2.2 to the actual operator `T_u` of (1.5).  Then the full
transported derivative `B+T_u` has the based right lift `s_T`.

V356 proves that the exceptional first class-two remainder is zero.  For
every later depth `r>=2`, v266 proves that terms containing two occurrences
of the newly applied correction have depth at least `r+2`.  Changes in the
base word of depth at least two likewise alter the derivative only at depth
at least `r+2`.  Therefore, at the immediately following layer, all
transported-linear terms are handled by the single operator `T_u`, while the
remaining exact word-product terms enter the ordinary localized Newton
remainder.

### Corollary 4.1 (NO SEPARATE TRANSPORTED-LINEAR OBSTRUCTION)

Under the strict-cover, leading word-bearing lift, localized stability and
materialization hypotheses of v319, the occurrencewise transported-linear
terms require no additional all-depth return hypothesis.  The additive
repair (2.8) absorbs them once, and v319's localized Newton recursion then
constructs the relative pro-3 solution.

#### Proof

Theorem 1.1 supplies a natural filtration-raising `T_u`; Proposition 3.1
places it in the same target; Theorem 2.2 replaces `s` by a right lift for
`B+T_u`.  The depth estimates just recalled put every omitted term in the
next localized Newton remainder.  Apply v319 Theorem 3.1, with v321's
same-depth saturation condition supplied by the assumed strict cover.
\(\square\)

The load-bearing remaining pro-3 question is therefore finite at the leading
localized layer:

\[
 \boxed{
 \bar B:A/\mathcal F^1A\longrightarrow
 L_{\rm loc}/\mathcal F^1L_{\rm loc}
 \text{ must cover a finite generator roster by actual words}.}
\tag{4.1}
\]

One successful vector is not automatically this all-generator solve.  If the
chosen route uses only the pointed cyclic class instead of `L_loc`, it must
separately prove that every prefix ratio in (1.5) preserves that cyclic
class; Proposition 3.1 proves only the larger localized statement.

## 5. Executable certificate boundary

After an actual A0/task193 word exists, a finite transport receipt needs only:

1. the eleven literal prefixes at `F_0` and `F_0u` and the exact ratios
   `k_o(u)` from (1.4);
2. direct replay of the finite sum (1.5), with block tags, inverse slots and
   printed order retained;
3. the complete finite generator roster of the localized leading target;
4. word-bearing leading preimages defining `s`;
5. additive coordinates `K(e_i)` with `qK(e_i)=T_us(e_i)`;
6. the finite Neumann polynomial and direct `(B+T_u)s_T=q` replay; and
7. the intrinsic/ambient saturation and separately registered side gates.

An independent checker can reconstruct every `k_o(u)` from the task198
occurrence ledger; no abstract transport matrix is trusted.  Xi-linearity is
neither tested nor claimed.

```text
ELEVEN-OCCURRENCE TRANSPORT FORMULA:              PAPER PROOF
ONE-DEPTH GAIN AND REFINEMENT NATURALITY:          PAPER PROOF
XI-LINEARITY NEEDED FOR NEUMANN REPAIR:            NO
FILTERED ADDITIVE BASED PERTURBATION:              PAPER PROOF
TRANSPORTED TERM IN FULL LOCALIZED TARGET:          PAPER PROOF
FIRST SELF-QUADRATIC REMAINDER:                     ZERO (v356)
ACTUAL STRICT LOCALIZED FREE COVER:                 OPEN
ACTUAL LEADING ALL-GENERATOR WORD SOLVE:            OPEN
ACTUAL K COORDINATES / FINITE REPLAY:               NOT COMPUTED
RELATIVE PRO-3 COMPATIBLE LIFT:                     CONDITIONAL, NOT CLAIMED
MIXED-PRIME / PERFECT-CORE / FAKE / IHARA:          OPEN
```

`R07_OCCURRENCEWISE_TRANSPORTED_JACOBIAN_V357_PAPER_GRADE`
