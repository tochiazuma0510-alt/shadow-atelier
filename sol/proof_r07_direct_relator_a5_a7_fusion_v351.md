# R07 direct-relator A5/A7 fusion and lift-null completion (v351)

Author: Sol / 2026-08-29

Status: paper theorem combining v350's direct-relator A5 bypass with the
universal endpoint fusion of v309--v310.  It gives a single positive-complete
dovetail for one fixed literal A0 word.  It does not assert that the actual
target is a member and declares no compatible lift, fake certificate or Ihara
witness.  `verified=false`.

## 1. Two kernels which must not be conflated

Let `k=F3`, let `Gamma` be the fixed common literal source image in the seven
presented PB3/PB4 contexts, and retain

\[
 \Gamma\mathrel{\mathop{\twoheadrightarrow}^{\pi _1}}\Delta _1
 \mathrel{\mathop{\twoheadrightarrow}^{\pi _{10}}}\Delta _0.
\tag{1.1}
\]

Put

\[
 J_0=\ker(k[\Gamma]\to k[\Delta _0]),\qquad
 I=\ker(k[\Delta _1]\to k[\Delta _0]),
\tag{1.2}
\]

and

\[
 \mathcal L_1=\ker(J_0\to I)
 =\ker(k[\Gamma]\to k[\Delta _1]).
\tag{1.3}
\]

The first kernel `I` is the finite first-shadow coefficient space.  The
second kernel `L1` changes the literal word-pair representative without
changing its first-shadow coefficient.  A5 depends only on the image in
`I`; the exact A7 endpoint can detect `L1`.  Hence a complete A5 column
roster alone need not contain an endpoint-zero representative.

Let the 6,441 authenticated task198 relators be `r_j`, and write

\[
 b_j=\pi _1(r_j)\in\ker(\Delta _1\to\Delta _0).
\tag{1.4}
\]

By v350,

\[
 I=\sum_{j=1}^{6441}k[\Delta _1](b_j-1).
\tag{1.5}
\]

Choose the frozen literal section `s:Delta1 -> Gamma`.  For `g in Delta1`
define the canonical direct-relator pair

\[
 P_{g,j}=s(g)r_j-s(g)\in J_0,
 \qquad \overline P_{g,j}=g(b_j-1)\in I.
\tag{1.6}
\]

Every coefficient in `I` has a finite expression in the second family of
(1.6).  Different expressions and different literal sections can differ by
an element of `L1`; this difference is invisible to A5 but not to A7.

## 2. The augmented quotient map

Fix one literal accepted A0 word and its task193 rows.  Write

\[
 t_5=(e_1,0)
\tag{2.1}
\]

for the zero-base A5 target in v350's post-`C` quotient, and let

\[
 A:I\longrightarrow Q,
 \qquad A(\theta)=T\widehat\Psi(\theta)
\tag{2.2}
\]

be the complete finite A5 map.  Here `Q` contains all typed pointed and
eleven-occurrence coordinates after quotienting by the complete PB boundary
module.

Let

\[
 \mathcal E=\mathcal E_{H1}\oplus\mathcal E_{H2}\oplus\mathcal E_P
\tag{2.3}
\]

be the direct sum of the three exact PB endpoint modules, represented by
full Artin normal-form keys rather than a finite shadow.  With v309's signs
put

\[
 \eta_c=\widetilde D_1\widetilde e_c\in\mathcal E,
 \qquad
 U(P)=\widetilde D_1(P\widetilde d)\in\mathcal E
 \quad(P\in J_0).
\tag{2.4}
\]

The map `U` is `k`-linear and `Gamma`-equivariant.  For a literal polynomial
`M in J0`, its three exact endpoints vanish exactly when

\[
 U(M)=\eta_c.
\tag{2.5}
\]

Define canonical augmented columns and lift-null columns by

\[
 c_{g,j}=\bigl(A(\overline P_{g,j}),U(P_{g,j})\bigr),
 \qquad
 z_L=(0,U(L))\quad(L\in\mathcal L_1).
\tag{2.6}
\]

### Theorem 2.1 (DIRECT-RELATOR A5/A7 FUSION)

For the fixed literal A0 word, the following are equivalent.

1. There is a finite literal roof-fibre polynomial `M in J0` whose image
   `mu1 in I` satisfies A5 and whose H1, H2 and P exact endpoints all vanish.
2. There are finitely many coefficients `a_gj in k` and one finite-support
   `L in L1` such that

\[
 \boxed{
 (t_5,\eta_c)
  =\sum_{g,j}a_{g,j}c_{g,j}+z_L.}
\tag{2.7}
\]

On (2.7), one may take

\[
 \boxed{
 \mu_1=\sum_{g,j}a_{g,j}g(b_j-1),\qquad
 M=\sum_{g,j}a_{g,j}P_{g,j}+L.}
\tag{2.8}
\]

#### Proof

Suppose (2.7) holds.  Its `Q` coordinate and (2.2) give

\[
 A(\mu_1)=t_5,
\tag{2.9}
\]

because `L` maps to zero in `I`.  This is exactly the zero-base A5 pointed
and occurrence condition.  The image of `M` in `I` is `mu1` by (1.3), (1.6)
and (2.8), so `M` is a literal A6 lift of that same coefficient.  The
`E` coordinate of (2.7), linearity of `U`, and (2.8) give

\[
 U(M)=\eta_c,
\tag{2.10}
\]

which is (2.5), separately in H1, H2 and P.

Conversely suppose `M` has the properties in item 1, and let `mu1` be its
image in `I`.  By (1.5), choose a finite expression

\[
 \mu_1=\sum_{g,j}a_{g,j}g(b_j-1).
\tag{2.11}
\]

The difference

\[
 L=M-\sum_{g,j}a_{g,j}P_{g,j}
\tag{2.12}
\]

maps to zero in `I`, hence lies in `L1`.  The A5 equality gives the `Q`
coordinate of (2.7), while endpoint zero and linearity give its `E`
coordinate.  Thus (2.7) holds.  \(\square\)

The theorem is stronger than testing the first A5 representative returned by
v350.  Such a representative corresponds to the special choice `L=0`; a
nonzero endpoint for that choice does not refute (2.7).

## 3. Finite seeds and positive completeness

Use v310's literal Schreier transversal for `Gamma -> Delta1`.  Its finite
roster `n_1,...,n_s` satisfies

\[
 \mathcal L_1=\sum_{i=1}^s k[\Gamma](n_i-1).
\tag{3.1}
\]

For a literal translating word `V in Gamma` put

\[
 L_{V,i}=V(n_i-1)=Vn_i-V,
 \qquad
 z_{V,i}=(0,U(L_{V,i})).
\tag{3.2}
\]

### Corollary 3.1 (FINITE-SEED POSITIVE-COMPLETE DOVETAIL)

Replace the arbitrary `z_L` in (2.7) by the translated seed columns
`z_Vi`.  A fair enumeration of the canonical direct-relator action columns
and the translated Schreier seed columns terminates positively whenever a
finite-support `M` satisfying item 1 of Theorem 2.1 exists.

#### Proof

V350 gives a finite direct-relator expression for the image of `M`.  The
remaining difference `L` is finite-support and v310 Theorem 2.2 writes it as
a finite sum of the pairs (3.2).  A fair enumeration eventually inserts all
columns in that finite equality; exact sparse elimination then reduces the
target to zero.  \(\square\)

The seed roster is finite, but its translating source words generally are
not.  Therefore a bounded failure of this dovetail is `UNKNOWN_RESOURCE`,
not A7 nonexistence.  Complete A5 NONMEMBER remains decidable after the
finite `Delta1` action closure and the complete PB boundary oracle exhaust,
because lift-null columns have zero A5 coordinate.

## 4. Raw-chain form used by the machine

Let

\[
 q:\mathcal C\twoheadrightarrow Q=\mathcal C/\mathcal B
\tag{4.1}
\]

be v350's raw typed chain quotient, where `B` is generated by the complete
translated PB boundary families.  Choose a raw target `t_tilde` above `t5`.
For each canonical pair and lift-null pair, let

\[
 \widetilde q_{g,j}\in\mathcal C,
 \qquad \widetilde q_{V,i}\in\mathcal C
\tag{4.2}
\]

be their direct raw A5 evaluations.  The second family maps to zero in `Q`
but need not be the zero sparse row before quotienting.

### Theorem 4.1 (ONE RAW CERTIFICATE)

The equality (2.7) is equivalent to a finite raw equality

\[
 \boxed{
 (\widetilde t,\eta_c)=
 \sum a_{g,j}(\widetilde q_{g,j},U(P_{g,j}))
 +\sum h_{V,i}(\widetilde q_{V,i},U(L_{V,i}))
 +\sum_r d_r(b_r,0),}
\tag{4.3}
\]

where the `b_r` are translated presentation-boundary columns.  Consequently
one ancestry-bearing augmented echelon can return `mu1`, the literal `M`,
all three exact endpoint zeros, and the raw PB equality ledger at once.

#### Proof

Applying `q` to the first coordinate of (4.3) gives the `Q` coordinate of
(2.7); the boundary columns disappear.  The second coordinate gives its
exact endpoint coordinate.  Conversely the first-coordinate difference of
any finite equality (2.7) lies in `B`, so it has a finite expression in the
registered translated boundary generators and lifts to (4.3).  The
coefficient and lift-null ancestries give (2.8), while boundary coefficients
certify equality only and never enter `M`.  \(\square\)

It is unsound to replace `q_tilde_Vi` by raw zero unless an explicit boundary
ledger proves that reduction.  This is the precise raw/quotient distinction
which a checker must enforce.

## 5. Witness-first execution order

The current direct-relator v3 computation can be extended without rebuilding
its A5 owner.

1. Retain its A5-only echelon.  A zero remainder proves A5 and yields one
   canonical `M`, but does not stop the witness-oriented lane.
2. Beside it, append to every coefficient column its exact H1/H2/P endpoint
   coordinate and append zero endpoint coordinates to PB equality slack.
3. Dovetail the finite Schreier seeds under literal source translations as in
   (3.2), using their full raw A5 coordinate in (4.3).
4. Stop immediately on an augmented zero remainder.  Only the finitely used
   ancestry, boundary slack and exact Artin rows are required for the positive
   checker.
5. If A5 closes negatively after its complete finite closure, reject this A0
   word at A5.  If A5 passes but the augmented lane reaches a resource bound,
   preserve the A5 certificate and return A7 `UNKNOWN_RESOURCE`; do not call
   it endpoint nonzero over all representatives.

A cheaper two-phase schedule is also sound: test the first v3 `M` with the
already cross-checked task292 endpoint core, and start the lift-null dovetail
only if that exact endpoint is nonzero.  Theorem 2.1 proves that this changes
search order, not the positive universe.

## 6. Promotion boundary

An augmented MEMBER gives the actual A5 multiplier, its A6 literal
word-pair polynomial, and A7's three exact zero endpoints.  V193/v197 can
then extract and replay the three finite boundary chains, and v191/v174 can
use the same `M` at every matched relative pro-3 rung, subject to their
registered nonlinear and side gates.

Nothing in this theorem discharges the prime-to-three formation step, the
perfect-core/field-outer gate, the coupled PB4 small-window gate, or the
nonarithmetic roof binding.  Those remain necessary before a compatible
witness, fake certificate or Ihara conclusion.

```text
DIRECT-RELATOR A5 + EXACT A7 JOINT CRITERION:       PAPER PROOF
LIFT-NULL SCHREIER COMPLETION:                      PAPER PROOF
FINITE-SUPPORT POSITIVE COMPLETENESS:               PAPER PROOF
ONE RAW MEMBER -> MU1 + M + THREE ENDPOINT ZEROS:   PAPER PROOF
BOUNDED AUGMENTED MISS -> A7 NONEXISTENCE:          FORBIDDEN
ACTUAL AUGMENTED MEMBER:                            NOT COMPUTED
A8/A9 AND FORMATION/PERFECT-CORE GATES:             OPEN
COMPATIBLE LIFT / FAKE / IHARA WITNESS:             NONE
```

`R07_DIRECT_RELATOR_A5_A7_FUSION_V351_PAPER_GRADE`
