# R07 pointed-ancestry word-pair promotion v191

Author: Sol / 2026-08-28

Status: paper theorem and post-v188 compiler. This note generalizes v175's
special polynomial \(\sum a_i(u_i-1)\) to the full relative group-algebra
ideal. A pointed first-edge ancestry canonically produces a finite sum of
differences of source words having the same roof value. That sum is the exact
all-rung candidate; no second short-word search is needed. A universal
Fox-boundary identity for the candidate is still required. No actual first
multiplier, compatible lift, fake certificate, or Ihara witness is declared.

## 1. The full relative ideal is a fibre-difference space

Let \(k=\mathbf F_3\), let

\[
 \pi:\mathcal G\twoheadrightarrow\Delta_0
\tag{1.1}
\]

be the fixed common-source group mapping to the correctly typed roof group,
and put

\[
 J_0=\ker\bigl(k[\mathcal G]\longrightarrow k[\Delta_0]\bigr).
\tag{1.2}
\]

Here \(\mathcal G\) may be the fixed presented common-source group used in
v175, or any word-bearing group through which all registered matched
refinements factor. Every element of an ordinary group algebra has finite
support.

### Lemma 1.1 (FINITE FIBRE-DIFFERENCE NORMAL FORM)

An element \(M\in k[\mathcal G]\) belongs to \(J_0\) if and only if it can be
written

\[
 \boxed{
 M=\sum_{i=1}^t a_i(U_i-V_i),
 \qquad a_i\in k,
 \qquad \pi(U_i)=\pi(V_i).}
\tag{1.3}
\]

The sum is finite. If the support elements are supplied by literal source
words, (1.3) may be chosen with literal source words for every \(U_i,V_i\).

#### Proof

Write \(M=\sum_g a_gg\). Its image in \(k[\Delta_0]\) is zero exactly when

\[
 \sum_{\pi(g)=q}a_g=0
\tag{1.4}
\]

for every roof value \(q\). For each fibre meeting the support, choose one
supported element \(V_q\). Then the part of \(M\) over that fibre is

\[
 \sum_{\substack{\pi(g)=q\\g\ne V_q}}a_g(g-V_q),
\tag{1.5}
\]

because (1.4) determines the coefficient of \(V_q\). Summing (1.5) gives
(1.3). The converse follows by applying \(\pi\) to each difference. Choosing
the retained source-word representative of every supported element gives the
last assertion. \(\square\)

V175's terms \(u_i-1\), with \(u_i\in\ker\pi\), are the special case in
which every \(V_i=1\). That special form need not contain a coefficient such
as \(g(u-1)\) without further expansion. The pair form (1.3) is the exact
finite normal form for the whole relative ideal.

Equivalently, a pair term records two common conjugators which are
indistinguishable at the roof but may separate at a finer level. This is
precisely the information retained by a word-bearing relative lift.

## 2. Universal word-pair promotion

Use the v189 seven-block action, with its ten distinct typed occurrence
coordinates. Retain v175's universal Fox modules

\[
 \widetilde D_2:\widetilde C_2\longrightarrow\widetilde C_1
\tag{2.1}
\]

and the literal rows \(\widetilde d,\widetilde e\in\widetilde C_1\). The
group \(\mathcal G\) acts diagonally through the two three-occurrence
hexagon blocks and the five one-occurrence pentagon blocks.

### Theorem 2.1 (UNIVERSAL WORD-PAIR PROMOTION)

Suppose a finite word-pair polynomial \(M\) as in (1.3) and a finite-support
boundary chain \(q\in\widetilde C_2\) satisfy the literal equality

\[
 \boxed{
 \widetilde e-M\widetilde d=\widetilde D_2q
 \quad\text{in }\widetilde C_1.}
\tag{2.2}
\]

Then \(M\) has an image \(\mu\) in the completed relative ideal
\(\mathfrak j\), and at every registered matched relative pro-3 quotient

\[
 \boxed{e_n=\mu_nd_n.}
\tag{2.3}
\]

Under the word-bearing and nonlinear side gates of v174, the single
compatible correction is

\[
 \boxed{
 c_\infty=-\sum_{r\ge0}\mu^ra.}
\tag{2.4}
\]

#### Proof

For each pair, \(\pi(U_i)=\pi(V_i)\), so \(U_iV_i^{-1}\) belongs to the roof
kernel. In every matched refinement the difference \(U_i-V_i\) therefore
lies in the relative augmentation ideal, and its compatible inverse-limit
image lies in \(\mathfrak j\). Hence the same is true of \(M\).

V175 Lemma 2.1, amended only by the v189 block typing, says that source-word
evaluation, Fox derivation, prefix transport, and the complete presentation
boundary commute with every matched reduction. Reducing (2.2) gives

\[
 e_n-\mu_nd_n=D_{2,n}q_n.
\tag{2.5}
\]

The right side vanishes in the boundary quotient, proving (2.3). V174
Theorem 2.1 then gives (2.4). \(\square\)

Thus v175 Theorem 3.1 remains valid and is strictly generalized by replacing
its restricted kernel-difference polynomial with (1.3).

## 3. Compiling the pair polynomial from a pointed ancestry

Consider the first genuine elementary-abelian successor

\[
 \Delta_1\twoheadrightarrow\Delta_0,
 \qquad K=\ker(\Delta_1\to\Delta_0)\cong(C_3)^t,
\tag{3.1}
\]

and put

\[
 A_1=k[\Delta_1],
 \qquad I_0=\ker(A_1\to k[\Delta_0]).
\tag{3.2}
\]

V188, using the complete 6,441-relator roof presentation of v190, returns a
word-bearing basis \(k_1,\ldots,k_t\) of \(K\). For each basis value it
retains a literal source word \(w_i\) whose roof value is one and whose
successor value is \(k_i\). It also retains source sections for every roof
coefficient used by its rank closures.

Suppose the pointed gate is positive and returns

\[
 e_1=\alpha d_1+\beta e_1,
 \qquad \alpha,\beta\in I_0.
\tag{3.3}
\]

With the v184/v188 order convention, put

\[
 \mu_1=(1-\beta)^{-1}\alpha
       =\left(\sum_{r=0}^{2t}\beta^r\right)\alpha.
\tag{3.4}
\]

Every operation in (3.4) is finite and word-bearing.

### Theorem 3.1 (POINTED-ANCESTRY PAIR COMPILER)

From the retained v188 ancestry in (3.3), one can algorithmically construct
a finite word-pair polynomial

\[
 \boxed{M_1=\sum_i a_i(U_i-V_i)}
\tag{3.5}
\]

such that

\[
 \pi(U_i)=\pi(V_i)\quad\text{for all }i,
 \qquad
 M_1\mapsto\mu_1\text{ in }k[\Delta_1].
\tag{3.6}
\]

The construction requires no new source-word search.

#### Proof

The rank-closure ancestry expresses \(\alpha\) and \(\beta\) as finite
linear combinations of marked translates of

\[
 (k_i-1)d_1,\quad (k_i-1)e_1.
\tag{3.7}
\]

Consequently it also gives explicit finite group-algebra expressions for
\(\alpha,\beta\), with a source word for each translating element and each
\(k_i\). Expand the ordered finite product (3.4), retaining the source-word
product for every term, and collect equal successor values. This yields a
finite-support element \(\mu_1\in A_1\).

Since \(\alpha,\beta\in I_0\), the ideal property and the finite inverse in
(3.4) give \(\mu_1\in I_0\). Apply Lemma 1.1 to the finite support of
\(\mu_1\), grouping terms by their common image in \(\Delta_0\). Use the
retained source word of one supported element as the base representative in
each fibre. The resulting pairs satisfy (3.6), and their reduction in
\(A_1\) is exactly \(\mu_1\). \(\square\)

Different source representatives of one successor element can give
different all-rung candidates even though they have the same first shadow.
Therefore the compiler must retain the exact chosen words; it must not
canonicalize only by a \(\Delta_1\) element ID and discard ancestry.

## 4. The one remaining positive certificate

The output \(M_1\) of Theorem 3.1 is automatically:

1. in the universal relative ideal by its word-pair typing;
2. a literal lift of the actual first-shadow multiplier; and
3. finite, explicit, and directly evaluable in every context.

It is not automatically the completed multiplier. The sole linear promotion
equation is

\[
 \boxed{
 \widetilde e-M_1\widetilde d
 \in\operatorname{im}\widetilde D_2.}
\tag{4.1}
\]

A positive certificate consists of a finite \(q\) with equality (2.2).
Because both sides have finite word support, a proposed certificate is
checked by finitely many exact word, Fox, block, sign, and coefficient
replays. Failure of a bounded search for \(q\) is UNKNOWN; it is not a
nonexistence theorem.

If (4.1) fails for the first source-representative choice, the first-shadow
solution is not lost. One may vary a representative \(U_i\) or \(V_i\) by a
word trivial in \(\Delta_1\); this preserves (3.6) while changing finer
shadows. Such variations must be preregistered and tested through the same
universal equality, not inferred from the finite quotient.

### Corollary 4.1 (NO SECOND BLIND WORD SEARCH)

After a positive v188 pointed ancestry, the Phase-A short-word search in
v175 Section 4 is superseded. The exact first candidate \(M_1\) is compiled
from the ancestry. Only the universal boundary lift (4.1), and if necessary
explicit same-first-shadow representative variations, remain.

## 5. Exact production chain

The shortest current chain is now:

1. obtain the exact task192 common word and adapt it to task193;
2. materialize the genuine second-rung rows \(d_1,e_1\);
3. use v189/v190 and v188 to compute the exact successor kernel and the
   pointed ancestry (3.3);
4. expand the ordered Neumann coefficient (3.4) with literal word ancestry;
5. compile the fibre-difference polynomial (3.5); and
6. seek and independently replay one universal boundary chain \(q\) in
   (2.2).

If Step 6 is positive and the nonlinear gates hold, Theorem 2.1 and v174
produce all relative pro-3 corrections at once. Formation purification,
prime-to-three refinements, and new perfect-core accepted sets remain
separate cofinal obligations.

The production receipt for Steps 4--6 must retain:

1. the full \(\alpha,\beta\) sparse coefficients and pointed ancestry;
2. every ordered power of \(\beta\) through \(2t\);
3. coefficient collection before and after cancellation;
4. every source word representing a support element;
5. the roof fibre partition and chosen base representative;
6. every pair \(U_i,V_i\), its equal roof value, and its successor values;
7. direct equality \(M_1\mapsto\mu_1\);
8. the universal chain \(q\), if found; and
9. direct replay of (2.2) with destructive mutations of one word, pair,
   multiplication order, block tag, and boundary coefficient.

~~~text
FULL RELATIVE IDEAL = FINITE ROOF-FIBRE DIFFERENCES: PAPER_PROOF
UNIVERSAL WORD-PAIR PROMOTION:                       PAPER_PROOF
POINTED ANCESTRY -> WORD-PAIR POLYNOMIAL:            PAPER_PROOF
SECOND BLIND SHORT-WORD SEARCH AFTER POINTED PASS:   REMOVED
ACTUAL FIRST-SHADOW MULTIPLIER mu1:                  NOT COMPUTED
ACTUAL WORD-PAIR POLYNOMIAL M1:                      NOT COMPILED
UNIVERSAL BOUNDARY CHAIN q:                          NOT FOUND
RELATIVE PRO-3 COMPATIBLE R07 LIFT:                  NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE GATES:                     OPEN
FAKE / IHARA WITNESS:                                NOT DECLARED
~~~

R07_POINTED_ANCESTRY_WORD_PAIR_PROMOTION_V191_PAPER_GRADE
