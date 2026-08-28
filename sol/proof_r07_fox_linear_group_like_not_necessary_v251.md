# R07 Fox-linear group-like is sufficient, not necessary v251

Author: Sol / 2026-08-28

Status: corrective paper theorem.  V249 and v250 correctly characterize when
one particular additive Fox chain is literally the Fox chain of one pro-3
word.  This note proves that this is a strictly stronger condition than the
word-bearing realization required by the R07 chief-layer correction problem.
It therefore removes that group-like test from the load-bearing A9 route.
The actual nonlinear all-rung word correction is still open.  No compatible
lift, fake certificate, or Ihara witness is declared.  verified=false.

## 1. Two different meanings of additive inverse

Let \(\mathcal P\) be a free pro-3 correction group, let
\(\mathcal R=\mathbf F_3[[\mathcal P]]\), and let

\[
 \delta:\mathcal P\longrightarrow\mathcal C_1
\tag{1.1}
\]

be the completed left Fox chain.  The crossed-product rule is

\[
 \boxed{\delta(uv)=\delta(u)+u\,\delta(v).}
\tag{1.2}
\]

In particular,

\[
 \boxed{\delta(a^{-1})=-a^{-1}\delta(a),}
\tag{1.3}
\]

not \(-\delta(a)\).

On the other hand, in an elementary-abelian chief factor written additively,
the class of the inverse word is

\[
 [a^{-1}]=-[a].
\tag{1.4}
\]

Thus the word which realizes additive negation has extra Fox prefix factors.
Forgetting those factors is harmless in the current graded layer and
generally wrong in the full completed Fox chain.

## 2. The one-line counterexample to necessity

### Proposition 2.1 (STRICT FOX-LINEAR GATE CAN FAIL FOR A WORD-BEARING CLASS)

Let \(a\ne1\) have nontrivial image in a finite 3-group correction quotient.
The additive chief-layer correction \(-[a]\) has the explicit word
representative \(a^{-1}\).  Nevertheless the raw additive Fox chain

\[
 Q=-\delta(a)
\tag{2.1}
\]

is not the Fox chain of a word.

#### Proof

Equation (1.4) proves the first assertion.  The endpoint of (2.1) gives

\[
 1+\partial Q
 =1-(a-1)=2-a
\quad\text{in }\mathbf F_3[\mathcal P].
\tag{2.2}
\]

After reduction to any finite quotient in which \(a\ne1\), (2.2) has two
distinct support elements, \(1\) and \(a\), both with coefficient two.
It is not group-like by v249 Lemma 2.1.  V249 Theorem 3.1 then proves that
\(Q\ne\delta(c)\) for every word \(c\).  In contrast, (1.3) is the actual Fox
chain of the valid representative \(a^{-1}\). \(\square\)

The example already occurs when the Neumann multiplier is zero.  Therefore
failure of the v249/v250 group-like test cannot reject a module correction,
an explicit chief-layer word, the roof branch, or the witness.

## 3. Ordered word materialization and the deeper error

Let one graded correction value have a finite word-bearing expression

\[
 v=\sum_{j=1}^m b_j[g_ja g_j^{-1}],
 \qquad b_j\in\mathbf F_3.
\tag{3.1}
\]

Fix the retained source-word order.  Lift the scalar \(0,1,2\) to word
exponents \(0,1,-1\), respectively, and define

\[
 \boxed{
 \operatorname{Mat}(v)
 =\prod_{j=1}^m
   (g_ja g_j^{-1})^{\widetilde b_j}.}
\tag{3.2}
\]

### Lemma 3.1 (MATERIALIZATION IS A GRADED SECTION)

The word (3.2) represents \(v\) in the active elementary-abelian chief
factor.  If all factors begin in filtration \(F^k\), then the difference
between its exact Fox chain and the raw additive sum of their Fox chains is
in the next multiplicative filtration.

#### Proof

The active quotient \(F^k/F^{k+1}\) is abelian of exponent three.  Products
become sums, inverses become scalar two, and conjugate words have exactly the
registered translated classes.  This proves the first assertion.

Iterating (1.2), every factor after the first is multiplied on the left by
the preceding partial product.  Each such prefix is congruent to one modulo
the active augmentation filtration.  Replacing the prefix by one gives the
raw additive Fox sum; every discarded term contains one additional
augmentation factor and hence lies in the next filtration. \(\square\)

This is the precise role of v98's nested word materialization.  It supplies
an actual word at the current layer.  The price is a new, strictly deeper
nonlinear residual, which must be evaluated and corrected rather than
discarded.

## 4. Correct interpretation of the Neumann formula

For the fixed A6 polynomial \(M\), v174/v228 give additive module values

\[
 c_N=-\sum_{r=0}^{N-1}\mu^ra.
\tag{4.1}
\]

Each finite value has retained word ancestry and hence the canonical ordered
word

\[
 w_N=\operatorname{Mat}(c_N).
\tag{4.2}
\]

Equations (4.1)--(4.2) do not assert

\[
 \delta(w_N)=-\sum_{r=0}^{N-1}\mathcal M^r\delta(a).
\tag{4.3}
\]

V249/v250 decide exactly the exceptional stronger equality (4.3).  A pass is
a useful closed Fox-linear materialization.  A failure merely says that the
prefix/cross terms from (1.2) are nonzero.

The load-bearing nonlinear test is instead:

1. construct \(w_N\) by (4.2);
2. substitute that actual word into the two hexagons and printed pentagon;
3. measure the deeper residual created by the crossed terms; and
4. correct it by the based Hensel recursion of v117, or prove a structural
   recurrence which kills every such residual.

Thus the remaining A9 problem is nonlinear residual control, not group-like
integrability of the raw additive chain.

## 5. Corrected certificate boundary

The v249/v250 support computation may be retained only under the label

    STRICT_FOX_LINEAR_MATERIALIZATION_CANARY

with these conclusions:

- singleton/cofinal PASS: sufficient for one especially rigid word formula;
- nonsingleton finite FAIL: rejects equality (4.3) for the named data only;
- neither outcome decides existence of ordered word materializations (4.2);
- neither outcome is an A9 numerator, fake certificate, or Ihara decision.

The proof-carrying A9 route must instead retain every ordered factor in
(4.2), its exact free reduction, the literal H1/H2/P evaluations, and every
deeper correction returned by the adaptive recursion.

## 6. Fixed frontier

    RAW ADDITIVE FOX CHAIN GROUP-LIKE:             SUFFICIENT, NOT NECESSARY
    NONSINGLETON SUPPORT AS WITNESS OBSTRUCTION:   RETRACTED
    ORDERED WORD MATERIALIZATION OF MODULE VALUE:  PAPER PROOF
    MATERIALIZATION ERROR LIES DEEPER:             PAPER PROOF
    EXACT NONLINEAR H1/H2/P AFTER MATERIALIZATION: OPEN
    UNIFORM BASED SELECTOR FOR DEEPER RESIDUALS:   OPEN
    ACTUAL A5/A6/A7 DATA:                          NOT COMPUTED
    COMPATIBLE LIFT / FAKE / IHARA:                NOT CONSTRUCTED

R07_FOX_LINEAR_GROUP_LIKE_NOT_NECESSARY_V251_PAPER_GRADE
