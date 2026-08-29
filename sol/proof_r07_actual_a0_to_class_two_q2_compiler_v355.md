# R07 actual A0 word to class-two nonlinear remainder compiler (v355)

Author: Sol / 2026-08-29

Status: paper interface theorem correcting the physical input boundary of
v266.  The first nonlinear class-two remainder is determined by the literal
correction word which task193 actually multiplies onto `g760`; the A5
coefficient ancestry represents the multiplier `mu`, not that correction
word.  The theorem gives a finite PB3/PB4 class-two compiler and removes A5
from the input dependency of `q2` itself.  It does not compute the actual A0
word, `q2`, its return orbit, a compatible lift, fake, or Ihara witness.
`verified=false`.

## 1. The physical first-correction owner

Let

\[
 f_0=g_{760},\qquad c=c_{A0},\qquad f_1=f_0c,
\tag{1.1}
\]

where `c` is exactly task193's retained `correction_word`.  The physical
binding already replayed by the v4/v5 endpoint owner is

```text
corrected_word = freely_reduce(g760 * correction_word).
```

For each of the eleven registered occurrences `o`, let

\[
 g_o=\rho_o(f_0),\qquad a_o=\rho_o(c),
\tag{1.2}
\]

in the appropriate PB3 or PB4 free-generator alphabet.  The task198
occurrence ledger fixes the block, sign, inverse slot, physical factor order
and old-factor prefix.  Thus no word has to be reconstructed from an
additive coefficient.

The A5 output has a different type.  Its retained terms spell

\[
 \mu_1=\sum_j b_j w_j(r_j-1)
\tag{1.3}
\]

and the associated word-pair polynomial `M`.  They are the first shadow of
the Neumann multiplier.  They are not the already applied word `c` in
(1.1).  Consequently v266 Section 3 must be read with the applied
first-correction word supplied by task193, not with the A5 `mu1` terms
renamed as `a`.

## 2. A finite exact class-two PB owner

For `n=3,4`, let `m=binom(n,2)`, let

\[
 V_n=\mathbf F_3^m,
\tag{2.1}
\]

and give the task292 pure generators their registered lexicographic order.
Let `r_1,...,r_s` be the complete task292 relator roster (`s=2,11`).
Collect each relator in the free exponent-three class-two group and let

\[
 R_n\leq \bigwedge^2V_n
\tag{2.2}
\]

be the span of its degree-two coordinates.  Put

\[
 W_n=(\bigwedge^2V_n)/R_n.
\tag{2.3}
\]

Represent a word by `(u,U) in V_n direct-sum W_n`, sending generator `i` to
`(e_i,0)` and using

\[
 (u,U)(v,V)=
 \left(u+v,U+V+\frac12u\wedge v\right),
 \qquad \frac12=2\in\mathbf F_3,
\tag{2.4}
\]

and `(u,U)^(-1)=(-u,-U)`.

### Lemma 2.1 (TASK292 CLASS-TWO COORDINATE)

The preceding scan is a well-defined quotient of PB_n and is exactly its
maximal exponent-three quotient of nilpotency class at most two.  In
particular it computes the first two Zassenhaus coordinates of every finite
PB word.

#### Proof

The class-two Campbell--Hausdorff law (2.4) is the free exponent-three
class-two group on the registered generators.  Quotienting its central
degree-two part by the initial forms of the complete presentation relators
is precisely the class-two quotient of the presented group.  Task292's
two/eleven relators are a complete PB3/PB4 presentation, so no additional
relation is missing.  Since the class is smaller than three, the
exponent-three class-two quotient is the quotient by the third Zassenhaus
term.  Directly scanning the relators and checking that their final
coordinates vanish supplies the finite certificate.  \(\square\)

This construction uses sparse vectors and an echelon of the relator initial
forms.  It does not enumerate PB elements, use a finite quotient as a word
equality key, or invoke a p-quotient search.

## 3. Exact occurrencewise ratio

For one block `B`, write its physical relation word as the frozen ordered
product of signed factors.  Let `P_o` be the old-factor prefix before
occurrence `o`.  Define

\[
 \widehat P_o=
 \begin{cases}
 P_og_o,&\sigma_o=+1,\\
 P_o,&\sigma_o=-1.
 \end{cases}
\tag{3.1}
\]

This is exactly the `prefix_word` already reconstructed by the v4/v5
literal owner.  Set

\[
 d_o(c)=\widehat P_o,a_o^{\sigma_o}\,\widehat P_o^{-1}.
\tag{3.2}
\]

Order these factors by the literal left-to-right factor order of the printed
hexagon or A.18 word, not merely by ordinal number.

### Lemma 3.1 (LITERAL RATIO FACTORIZATION)

For every block,

\[
 \boxed{
 R_B(f_1)R_B(f_0)^{-1}=\prod_o d_o(c)}.
\tag{3.3}
\]

The equality holds by free-word reduction before imposing PB relations.

#### Proof

For an ordinary product `b_1...b_t`, with each `b_i` replaced by `b_i'`,
successive cancellation gives

\[
 (b_1'\cdots b_t')(b_1\cdots b_t)^{-1}
 =\prod_{i=1}^t
 (b_1\cdots b_{i-1})(b_i'b_i^{-1})
 (b_1\cdots b_{i-1})^{-1}.
\tag{3.4}
\]

If the slot is positive, `b_i'=g_o a_o` and
`b_i'b_i^(-1)=g_o a_o g_o^(-1)`.  If it is inverse,
`b_i'=a_o^(-1)g_o^(-1)` and `b_i'b_i^(-1)=a_o^(-1)`.
Substitution in (3.4) is exactly (3.1)--(3.2).  \(\square\)

An executable must construct both sides independently and require their
literal free reduction to agree.  This removes every sign/order ambiguity
from the paper notation.

## 4. Closed `q2` compiler from the A0 word

Apply Lemma 2.1 to each factor (3.2) and write

\[
 [d_o(c)]=(\ell_o,\tau_o)\in V_{r(B)}\oplus W_{r(B)}.
\tag{4.1}
\]

### Theorem 4.1 (ACTUAL APPLIED-WORD CLASS-TWO FORMULA)

The degree-two nonlinear contribution made by the actual applied A0 word is

\[
 \boxed{
 q_{2,B}=
 \sum_o\tau_o+
 \frac12\sum_{o<o'}\ell_o\wedge\ell_{o'}
 \quad\text{in }W_{r(B)},}
\tag{4.2}
\]

with the order from Lemma 3.1.  The triple

\[
 q_2=(q_{2,H1},q_{2,H2},q_{2,P})
\tag{4.3}
\]

is determined by the accepted task193 word and task198 occurrence owner.
It does not require the A5 multiplier ancestry or the A7/A8 endpoint
certificate.

#### Proof

Multiply the coordinates (4.1) in their physical order using (2.4).  The
degree-one coordinate is `sum ell_o`; the degree-two coordinate is exactly
(4.2).  By the literal identity (3.3), this is the class-two coordinate of
the exact relation-word ratio.  It is therefore the word-product/crossed-
prefix contribution isolated as `q2` in v263--v266.  All inputs in (4.2)
come from (1.1)--(1.2); equation (1.3) is not used.  \(\square\)

The theorem is invariant under the sign convention used to name the module
class `a`: the executable consumes the word actually applied in (1.1).

## 5. What still needs A5

Computing (4.3) and proving its cyclic return are different operations.  To
continue the pointed Neumann branch one must still reconstruct the actual
diagonal degree-two orbit

\[
 L_2=[\Xi\beta]_2
\tag{5.1}
\]

and test `q2 in L2` with common-source ancestry.  A5 supplies the selected
multiplier `mu`; on a MEMBER return `q2=[nu2 beta]_2`, the total next
coefficient is `lambda2=mu+nu2`.  Thus A5 is required for the continued
selector, but not for the numerical `q2` compiler.

A finite producer for (4.3) should retain the exact task193 word, all eleven
substituted correction words, the ratio identity (3.3), the two PB relator-
initial-form echelons, every `(ell,tau)`, and the three printed-order sums.
An independent checker rebuilds the PB initial forms from its own task292
roster and replays the exact relation-word ratio directly.

```text
APPLIED FIRST CORRECTION OWNER:                 TASK193 A0 LITERAL WORD
A5 COEFFICIENT TERMS TYPE:                      MULTIPLIER mu / M, NOT A0 WORD
PB3/PB4 CLASS-TWO COORDINATE ALGORITHM:         PAPER PROOF
ELEVEN-FACTOR LITERAL RATIO:                    PAPER IDENTITY
ACTUAL q2 FROM ACCEPTED A0 WORD:                FINITE PAPER COMPILER
ACTUAL A0 WORD / NUMERICAL q2:                  NOT YET AVAILABLE
q2 CYCLIC/LOCALIZED RETURN WITH ANCESTRY:        OPEN
ALL-DEPTH NONLINEAR RECURRENCE:                 OPEN
COMPATIBLE LIFT / FAKE / IHARA:                 NONE
```

`R07_ACTUAL_A0_TO_CLASS_TWO_Q2_COMPILER_V355_PAPER_GRADE`
