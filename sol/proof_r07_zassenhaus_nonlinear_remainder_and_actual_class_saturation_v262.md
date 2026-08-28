# R07 Zassenhaus nonlinear remainder and actual-class saturation v262

Author: Sol / 2026-08-28

Status: paper theorem after v99, v117, v174, v191, v251, v252, and
v260.  It isolates the exact extra datum needed to turn the pointed
Neumann value into a literal all-rung solution.  On a strongly central
Zassenhaus refinement the Jacobian is fixed by the roof and every omitted
word-product term is one layer deeper.  The first such term is nevertheless
generally nonzero and occurs at the next active layer, so the linear
Neumann series alone does not prove the two hexagons and pentagon.  A single
actual-class saturation identity is sufficient to absorb all of these
terms with the same homotopy.  That identity has not been proved for the
actual R07 word.  No compatible lift, fake certificate, or Ihara witness is
declared.  `verified=false`.

## 1. A cofinal strongly central refinement

Let \(P\) be the finitely generated relative pro-3 correction group on the
registered common-word lane.  Use its Zassenhaus filtration

\[
 P=P_{(1)}\supset P_{(2)}\supset\cdots .
\tag{1.1}
\]

It is characteristic, cofinal, complete and separated, and satisfies

\[
 [P_{(r)},P_{(s)}]\subset P_{(r+s)},\qquad
 P_{(r)}^3\subset P_{(3r)}.
\tag{1.2}
\]

Every source substitution and matched reduction preserves (1.1).  Give the
three block-tagged literal residual groups the induced filtration.  Write

\[
 \Phi(F)=(H_1(F),H_2(F),P_{A.18}(F))
\tag{1.3}
\]

and retain the right-correction convention \(F\mapsto Fc\).  The coarse
roof value of \(F\) is fixed throughout.

The Zassenhaus ladder is a permissible cofinal refinement of the same
relative pro-3 completion.  It is used here only to expose degrees; it does
not replace the mixed-prime or perfect-core parts of the original ladder.

## 2. The deep Jacobian is independent of earlier corrections

Let \(B_r:C_r\to Z_r\) be the v99 literal H1/H2/A.18 Jacobian on

\[
 C_r=P_{(r)}/P_{(r+1)},\qquad
 Z_r=\mathcal F^r\mathcal Z/\mathcal F^{r+1}\mathcal Z,
\tag{2.1}
\]

restricted to the actual common-word, commutator, and relative-formation
domain.  Prefix actions of the fixed arithmetic/roof word remain in
\(B_r\).

### Lemma 2.1 (ROOF-FIXED JACOBIAN)

If \(F'=Fu\) with \(u\in P_{(1)}\), then for every \(r\geq1\) the
linearizations of \(\Phi\) at \(F\) and \(F'\) agree on \(C_r\).

#### Proof

V99 computes each row by collecting one occurrence of a correction through
the fixed prefixes of the corresponding literal relation word.  Replacing
\(F\) by \(Fu\) changes any such prefix by an element of \(P_{(1)}\).
Its change on a class represented by \(v\in P_{(r)}\) is a product of
commutators with \(u\), hence belongs to
\([P_{(1)},P_{(r)}]\subset P_{(r+1)}\).  It therefore vanishes in
\(C_r\) and in every induced residual factor.  The arithmetic/roof prefix
has not changed.  Applying this occurrencewise, with the literal signs and
printed pentagon order retained, proves the assertion.  \(\square\)

Thus the subscript \(F\) in v117 is unnecessary on this particular
strongly central refinement: earlier relative corrections change exact
residuals but not the next associated-graded Jacobian.

### Lemma 2.2 (QUADRATIC REMAINDER)

For \(c\in P_{(r)}\),

\[
 \Phi(Fc)=\Phi(F)+B_r[c]_r+Q_F(c),
 \qquad Q_F(c)\in\mathcal F^{r+1}\mathcal Z,
\tag{2.2}
\]

whenever \(\Phi(F)\in\mathcal F^r\mathcal Z\).  More generally, a term
containing correction letters of depths \(r_1,\ldots,r_t\) with
\(t\geq2\) has depth at least \(r_1+\cdots+r_t\).

#### Proof

Expand each fixed relation word after all occurrences of \(c\) have been
inserted.  Terms containing exactly one correction occurrence are the Fox
row \(B_r[c]_r\).  Moving two or more correction occurrences past fixed
prefixes produces products and commutators whose degree is bounded below by
the sum of their Zassenhaus degrees, by (1.2).  Terms discarded when a
prefix is replaced by its roof value contain the same additional
commutator.  Hence every remaining term has degree at least \(2r\), which
is contained in degree \(r+1\) for \(r\geq1\).  The argument applies
separately to H1 and H2 and to the five factors in printed A.18 order.
This is the group-word version of v251 Lemma 3.1.  \(\square\)

## 3. Why the pointed Neumann series is not yet the nonlinear lift

Retain an actual word-bearing first value \(a\), an actual defect \(\beta\),
and a universal word-pair multiplier \(\mu\) satisfying the v174/v191
linear identity

\[
 \beta-Ba=\mu\beta,
 \qquad \mu\in\mathfrak j.
\tag{3.1}
\]

Let \(c_1\) be the ordered word materialization of \(-a\).  Collect the
first unsettled successor in its elementary-abelian residual factor.  Lemma
2.2 gives there

\[
 \boxed{
 [\Phi(Fc_1)]_2=[\mu\beta]_2+q_2,
 \qquad q_2:=[Q_F(c_1)]_2\in
 \mathcal F^2\mathcal Z/\mathcal F^3\mathcal Z.}
\tag{3.2}
\]

The term \(q_2\) is not part of (3.1).  In general it has the same depth as
\(\mu\beta\).  Consequently the next Neumann value \(-\mu a\) cancels the
displayed linear class but need not cancel \(q_2\).

### Proposition 3.1 (FIRST NONLINEAR OBSTRUCTION)

Neither the universal boundary identity of v191/v194 nor actual-value
materialization in v260 implies \(q_2=0\) or
\(q_2\in\overline{\Xi\beta}\).  A proof that simply replaces (3.2) by
\(\mu\beta\) has dropped a load-bearing crossed-prefix term.

#### Proof

V191/v194 identifies the additive multiplier action modulo complete
presentation boundaries.  V260 realizes compatible additive chief-layer
values by a word.  The exact Fox product rule is crossed:

\[
 \delta(uv)=\delta(u)+u\delta(v).
\tag{3.3}
\]

The prefix \(u\) in (3.3) is precisely the source of the terms collected in
\(Q_F(c_1)\).  The cited identities impose no equality setting those terms
to zero and no cyclic-module membership for them.  V251 Proposition 2.1
already gives a word-bearing correction for which the raw additive and
exact Fox chains differ.  Hence the omitted implication is unavailable.
\(\square\)

This is why a strict group-like pass in v249 is useful but not necessary,
and why its failure is not a witness obstruction.

## 4. One saturation identity is sufficient

Let

\[
 L=\overline{\Xi\beta}\subseteq\mathcal Z
\tag{4.1}
\]

or, more generally, let \(L\) be a closed filtered actual residual module
containing \(\beta\).  Suppose the relative-dihedral odd homotopy together
with the actual-even Neumann homotopy gives a continuous filtered map

\[
 h:L\longrightarrow A,
 \qquad Bh=1_L,
 \qquad h(\mathcal F^rL)\subseteq\mathcal F^rA.
\tag{4.2}
\]

Write \(h_r\) for the induced map on the degree-\(r\) quotients.  Assume
every value of \(h_r\) has the v260 word-bearing materialization in the
corresponding \(P_{(r)}\).  The remaining condition is

\[
 \boxed{
 \text{(NLSAT)}\quad
 \Phi\!\left(F\operatorname{Mat}(-h_r(\bar z))\right)
       \in\mathcal F^{r+1}L}
\tag{4.3}
\]

for every reachable \(F\) with \(z=\Phi(F)\in\mathcal F^rL\), where
\(\bar z=[z]_r\).  Since the old residual tail is already in \(L\), (4.3)
is equivalently the assertion that the exact nonlinear remainder after the
degree-\(r\) cancellation returns to \(\mathcal F^{r+1}L\).

### Theorem 4.1 (ACTUAL-CLASS NONLINEAR COMPLETION)

Under (4.2)--(4.3), define recursively

\[
 z_r=[\Phi(F_r)]_r,\qquad
 c_r=\operatorname{Mat}(-h_r(z_r)),\qquad
 F_{r+1}=F_rc_r.
\tag{4.4}

Then \(\Phi(F_r)\in\mathcal F^rL\) for every \(r\), the product of the
\(c_r\) converges, and its limit satisfies both literal hexagons and the
printed-order A.18 pentagon on the relative pro-3 lane.

#### Proof

Assume \(\Phi(F_r)\in\mathcal F^rL\).  Lemma 2.1 makes the active
Jacobian the fixed \(B_r\), and (4.2) gives

\[
 [\Phi(F_rc_r)]_r=z_r-B_rh_r(z_r)=0.
\tag{4.5}
\]

Lemma 2.2 places the exact remainder one layer deeper; (NLSAT) places it in
\(L\).  This proves the induction.  Since \(c_r\in P_{(r)}\), the partial
products are Cauchy.  Completeness gives a limit and separatedness gives
zero residual.  \(\square\)

The theorem uses one fixed actual-class homotopy.  It does not search for an
unrelated preimage at every rung.  Pure linear Neumann powers are recovered
only in the exceptional case in which all the nonlinear remainders vanish or
are already included in the same recursive evaluation of \(h\).

### Corollary 4.2 (CYCLIC RETURN TEST)

For the pointed v174 route with \(L=\overline{\Xi\beta}\), the relative
pro-3 nonlinear gate is reduced to the class-specific assertion that every
reachable exact remainder returns to this cyclic actual class.  In
particular the first mandatory canary is

\[
 \boxed{q_2\in\overline{\Xi\beta}.}
\tag{4.6}

A separating dual at a finite rung disproves the fixed cyclic-Neumann
completion for the named \((F,a,M)\).  It does not disprove a larger actual
class, a different first correction or multiplier, an adaptive selector, or
the existence of a witness.

## 5. Finite certificate after A5--A8

Once the actual task192 word, A5/A6 ancestry, and the three A7 endpoints are
accepted, the next proof-producing receipt should:

1. materialize \(c_1=\operatorname{Mat}(-a)\) in the retained factor order;
2. replay the literal H1, H2 and printed A.18 words in the first Zassenhaus
   successor and extract the complete \(q_2\) of (3.2);
3. independently reconstruct the actual diagonal orbit
   \(L_2=\Xi_2\beta_2\), with one common-source ancestry;
4. return MEMBER ancestry for \(q_2\in L_2\), a complete separating dual,
   or `UNKNOWN_RESOURCE`;
5. on MEMBER, compute the next exact remainder and test the same literal
   return formula; and
6. upgrade finitely many passes to Theorem 4.1 only after a symbolic
   naturality/closure proof of (NLSAT), not by extrapolation from depth two.

The Zassenhaus choice removes state-dependent Jacobian rebuilding and gives
the sharp depth estimate.  It does not manufacture the missing actual-class
membership.

## 6. Fixed frontier

```text
COFINAL STRONGLY CENTRAL PRO-3 REFINEMENT:            PAPER PROOF
ROOF-FIXED ASSOCIATED-GRADED JACOBIAN:                PAPER PROOF
EXACT WORD-PRODUCT ERROR GAINS ONE DEPTH:             PAPER PROOF
PURE LINEAR NEUMANN SERIES AUTOMATICALLY SOLVES H/P:  FALSE IN GENERAL
ONE FIXED HOMOTOPY + NLSAT COMPLETES PRO-3 H/P:       PAPER PROOF
ACTUAL FIRST QUADRATIC REMAINDER q2:                  NOT COMPUTED
ACTUAL CYCLIC RETURN q2 IN Xi beta:                   OPEN
SYMBOLIC ALL-DEPTH NLSAT FOR R07:                     OPEN
ACTUAL A5/A6/A7 INPUTS:                               NOT COMPUTED
MIXED-PRIME / PERFECT-CORE / FAKE / IHARA:            OPEN
```

`R07_ZASSENHAUS_NONLINEAR_REMAINDER_AND_ACTUAL_CLASS_SATURATION_V262_PAPER_GRADE`
