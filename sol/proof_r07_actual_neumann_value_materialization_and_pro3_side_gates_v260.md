# R07 actual Neumann value materialization and pro-3 side gates v260

Author: Sol / 2026-08-28

Status: paper theorem after v94, v98, v173, v174, v191, and v259.  It
separates the literal nonlinear relation gate from three side conditions on
the relative pro-3 lane.  Once a Neumann value is typed in the actual
common-word correction image, compactness and the nested-kernel spelling
theorem materialize it by ordinary commutator words; the coarse mark,
charmingness, and onto gate then require no new rungwise search.  This note
does not prove that the actual A5/A6 multiplier exists, that the three PB
endpoints vanish, or that the materialized words satisfy the nonlinear
hexagon/pentagon equations.  Mixed-prime formation and perfect-core gates
remain separate.  `verified=false`.

## 1. Actual correction values, not an ambient module

Retain the nested matched pro-3 evaluation tower of v98,

\[
 \Psi_n:\widehat F_2\twoheadrightarrow H_n,
 \qquad U_n=\ker\Psi_n,
 \qquad U_{n+1}\le U_n.
\tag{1.1}
\]

Put

\[
 \mathcal C^{\rm com}=U_0\cap
 \overline{[F_2,F_2]}\subset\widehat F_2.
\tag{1.2}
\]

For each finite correction quotient used by v173, let

\[
 r_n:\mathcal C^{\rm com}\twoheadrightarrow A_n
\tag{1.3}
\]

denote its actual common-word realization map.  At an elementary-abelian
edge, (A_n) is the image of (\mathcal C^{\rm com}) in the active edge
factor and is therefore already an (\mathbf F_3)-subspace.  It is not the
span of a larger ambient product.  The surjectivity in (1.3) is a definition
of the actual correction module, not a theorem that promotes ambient rows.
This image condition is load-bearing: an element of an ambient product of
context modules is not silently promoted to (A_n).

The diagonal context group of v173 acts on every (A_n) by simultaneous
conjugation.  Normality of (U_0) and characteristicity of the commutator
subgroup show that this action preserves the images (A_n).  Hence the
actual modules form modules for the diagonal algebras (\Lambda_n), and
their inverse limit (A) is stable under (\Xi).  This is the actual-image
content of v173
Proposition 1.1, rather than a claim about an ambient direct product.

## 2. Compatible actual values have a profinite word realization

### Lemma 2.1 (ACTUAL-IMAGE INVERSE-LIMIT REALIZATION)

Let ((a_n)_n) be compatible, with (a_n\in A_n) for every (n), and with the
transition maps on (A_n) induced by the same word reductions.  Then there
is an element

\[
 c\in\mathcal C^{\rm com}
 \quad\hbox{such that}\quad
 r_n(c)=a_n\quad\text{for every }n.
\tag{2.1}
\]

If the finite values and their word-bearing ancestries are computable, v98's
shortlex nested-kernel rule computes compatible ordinary commutator words
converging to one such (c).

#### Proof

For each (n), define the fibre

\[
 X_n=\{c\in\mathcal C^{\rm com}:r_n(c)=a_n\}.
\tag{2.2}
\]

It is nonempty by the definition of (A_n), closed in the compact group
(\mathcal C^{\rm com}), and compatibility gives (X_{n+1}\subseteq X_n).
The nested intersection of nonempty compact sets is nonempty, proving
(2.1).

For the effective assertion, start with a word for (a_0).  At the next
level the discrepancy between its value and (a_1) is an actual value in the
transition image of (U_0\cap[F_2,F_2]).  V98 Theorem 2.1 chooses the
shortlex-first exponent-zero correction word in the accumulated kernel.
Iterating gives a Cauchy product; every later factor is invisible at every
earlier level.  V98 Corollary 2.2 gives the asserted limit.  \(\square\)

The lemma is only a realization theorem.  It does not turn an ambient
linear solution into an actual value; that membership is precisely what the
A5/A6 generalized-kernel gate must certify.

## 3. Applying the lemma to the pointed Neumann value

Assume the hypotheses of v174 Theorem 2.1 with one actual, word-bearing
(a\in A) and one (\mu\in\mathfrak j) satisfying

\[
 \beta-Ba=\mu\beta.
\tag{3.1}
\]

Suppose in addition that every finite value below is certified in the
actual common-word image, not merely in an ambient context module.  Define

\[
 q_\infty=\sum_{r\ge0}\mu^ra.
\tag{3.2}
\]

### Theorem 3.1 (ACTUAL NEUMANN VALUE MATERIALIZATION)

The reductions ((q_n)_n) of (3.2) are compatible actual correction values
and admit a profinite realization

\[
 c_\infty\in U_0\cap\overline{[F_2,F_2]}.
\tag{3.3}
\]

At each fixed finite pro-3 quotient only finitely many summands in (3.2)
remain, and a deterministic nested sequence of ordinary exponent-zero words
can be produced.

#### Proof

V173 Proposition 1.1 makes the actual correction modules stable under the
diagonal (\Xi)-action.  Thus every (\mu^ra) has an actual value in every
finite reduction.  V173 Lemma 2.1 makes the image of a sufficiently high
power of (\mathfrak j) zero at a fixed finite quotient, so the reduced sum
is finite.  The reductions commute and therefore give a compatible point
of (\varprojlim A_n).  Lemma 2.1 materializes that point, with the effective
statement supplied by its second clause.  \(\square\)

The phrase “certified in the actual common-word image” cannot be dropped.
It is the exact joint ancestry output requested at v220 A5/A6.

## 4. Three pro-3 side gates are automatic after actual typing

Let (f_0=g_{760}) be the fixed coarse word.  It has exponent sums ((0,0))
and its coarse marked E4 tuple is onto.  Let (c_n) be the nested ordinary
correction-word representatives obtained from Theorem 3.1, and put
(f_n=f_0c_n).

### Theorem 4.1 (MARK--CHARMING--ONTO PERSISTENCE)

For every (n):

1. the correction from (f_0) to (f_n) is trivial under (\Psi_0), so the R07
   coarse mark is unchanged;
2. (f_n) has exact exponent sums ((0,0)); and
3. its marked E4 value is onto in every compatible finite marked pro-3
   Frattini refinement above (\Pi_4[3]).

No separate search or replay of these three properties is needed at a later
pro-3 rung.

#### Proof

Every spelling factor supplied by Lemma 2.1 lies in the accumulated kernel
(U_m) appropriate to its edge.  In particular it lies in (U_0), proving
the first assertion and preserving all already frozen coarse values.

The same factor is chosen in the ordinary commutator subgroup, so its two
integer exponent sums vanish.  Products of such factors retain exponent
sums zero, proving the second assertion.

At every finer pro-3 level the corrected marked tuple is a compatible lift
of the fixed coarse tuple.  V94 Theorems 2.1 and 3.1 say that every transition
above (\Pi_4[3]) is Frattini-invisible and that any compatible lift of the
coarse onto tuple remains onto.  This proves the third assertion. \(\square\)

This theorem is deliberately restricted to the registered pro-3 lane.  It
does not cover a new prime-to-three factor, a non-Frattini extension, or a
new nonabelian chief factor.

## 5. What remains nonlinear

Theorems 3.1 and 4.1 discharge only realization and the three named side
conditions.  They do not identify the additive Neumann equality with the
literal group-word equations.  A positive witness still has to prove that
the chosen nested corrections kill both printed hexagons and the ordered
A.18 pentagon in every finite pro-3 window.  Equivalently, one must supply
one of the following already registered inputs:

1. a genuine universal nonlinear homotopy on the actual class; or
2. a v117 based correction whose literal residual gains depth at every step;
   or
3. a direct finite-window replay of the Neumann partial products together
   with a structural recurrence proving the same replay at every later
   window.

The v191/v194 endpoint identity is the correct linear promotion gate, but
by itself it does not prove one of these three nonlinear statements.  Thus
the new boundary is

\[
 \boxed{
 \text{actual A5/A6 ancestry}
 +\text{universal linear endpoint pass}
 +\text{nonlinear depth recurrence}.}
\tag{5.1}
\]

Mixed-prime formation membership and perfect-core accepted sets remain the
separate v220 B and C gates after (5.1).

```text
COMPATIBLE ACTUAL VALUES -> ONE PROFINITE WORD:       PAPER PROOF
NEUMANN VALUE MATERIALIZATION AFTER ACTUAL TYPING:    PAPER PROOF
COARSE R07 MARK THROUGH PRO-3 TOWER:                  AUTOMATIC
EXACT CHARMINGNESS THROUGH PRO-3 TOWER:               AUTOMATIC
ONTO THROUGH MARKED PRO-3 FRATTINI TOWER:             AUTOMATIC (v94)
ACTUAL A5/A6 COMMON-WORD MEMBERSHIP:                  OPEN
THREE UNIVERSAL PB ENDPOINTS:                         NOT COMPUTED
NONLINEAR H1/H2/P DEPTH RECURRENCE:                   OPEN
MIXED-PRIME / PERFECT-CORE GATES:                     OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA:                   NOT CONSTRUCTED
```

`R07_ACTUAL_NEUMANN_VALUE_MATERIALIZATION_AND_PRO3_SIDE_GATES_V260_PAPER_GRADE`
