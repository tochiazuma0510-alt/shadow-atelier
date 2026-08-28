# R07 three exact endpoints to all pro-3 rungs v228

Author: Sol / 2026-08-28

Status: paper synthesis and three-block correction to the promotion wording
in v191.  For one finite roof-fibre word-pair polynomial, vanishing of the
three exact PB endpoints is the final linear hypothesis needed to promote the
same multiplier through every relative pro-3 rung.  No rung-by-rung choice of
new multipliers or corrections is required.  The actual task192 word,
multiplier, and exact endpoints have not yet been computed, and the nonlinear
word gates remain separate.  No compatible lift, fake certificate, or Ihara
witness is declared.  `verified=false`.

## 1. Exact actual data

Put \(k=\mathbf F_3\).  Retain the corrected two-word convention of v225:

\[
 g_0=g_{760},\qquad a=c_{\rm exact},\qquad f=g_0a,
\tag{1.1}
\]

and, for \(B\in\{H1,H2,P\}\),

\[
 d_B=-\delta_B R_B(g_0),\qquad
 e_B=-\delta_B R_B(f)=d_B-(Ba)_B.
\tag{1.2}
\]

Let

\[
 M=\sum_{i=1}^t a_i(U_i-V_i),qquad
 \pi(U_i)=\pi(V_i),qquad a_i\in k,
\tag{1.3}
\]

be one finite word-pair polynomial compiled from a pointed ancestry as in
v191.  Its exact action is the occurrence-diagonal action of v194: evaluate
each pair through all ten typed maps, reinsert the repeated E3 occurrence,
apply the eleven signed prefix transports, and only then combine in H1, H2,
and P.

Define

\[
 z_B(M)=e_B-(M\star d)_B,qquad
 \eta_B(M)=D_{1,B}z_B(M).
\tag{1.4}
\]

The three PB groups in (1.4) are infinite.  Thus exact vanishing in (1.4) is
strictly stronger than vanishing in the exponent-nine quotient used by the
v216 pre-gate.

## 2. All-rung jump theorem

### Theorem 2.1 (THREE EXACT ENDPOINTS IMPLY ONE COMPLETED MULTIPLIER)

Assume that the same finite polynomial \(M\) in (1.3) satisfies

\[
 \boxed{
 \eta_{H1}(M)=\eta_{H2}(M)=\eta_P(M)=0}
\tag{2.1}
\]

as exact PB3/PB4 group-algebra identities.  Then:

1. there are finite-support chains \(q_B\) in the complete fixed PB
   presentation modules such that

   \[
   \boxed{e_B-(M\star d)_B=D_{2,B}q_B
          \quad(B=H1,H2,P);}
   \tag{2.2}
   \]

2. the word-pair polynomial has one compatible image
   \(\mu\in\mathfrak j\subset\mathbf F_3[[\Delta_\infty]]\); and
3. at every registered matched relative pro-3 rung,

   \[
   \boxed{e_n=\mu_nd_n}
   \tag{2.3}
   \]

   in the three-block defect quotient.

If the v174 correction-domain and nonlinear word hypotheses hold for the
task192 correction \(a\), then

\[
 \boxed{
 c_\infty=-\sum_{r\geq0}\mu^ra}
\tag{2.4}
\]

is one compatible relative pro-3 correction.  Every fixed finite rung sees
only a finite initial part of (2.4).

#### Proof

For each block, v194 Theorem 3.2 applies to the finite-support chain
\(z_B(M)\).  Condition (2.1) places it in \(\ker D_{1,B}\), and exactness at
Fox degree one for the complete PB presentation gives the finite chain
\(q_B\) in (2.2).

Every pair in (1.3) has equal roof value.  Hence its difference maps into the
relative augmentation ideal at every matched refinement, and the finite sum
defines one compatible element \(\mu\in\mathfrak j\).  Literal source-word
evaluation, the ten-to-eleven insertion, occurrence prefixes, Fox maps, and
the complete presentation boundaries commute with every registered
reduction.  Reducing (2.2) to rung \(n\) therefore gives

\[
 e_n-\mu_nd_n=D_{2,n}q_n.
\tag{2.5}
\]

The right side is zero in the defect quotient, proving (2.3).  This is the
three-combined-block form of v191 Theorem 2.1; no occurrence is required to
be a cycle separately.

Finally (1.2) says \(e=d-Ba\).  Together with the compatible identities
(2.3), this is the completed pointed equation

\[
 d-Ba=\mu d.
\tag{2.6}
\]

V174 Theorem 2.1 now applies.  Since \(\mu\in\mathfrak j\), its ordered
powers are cofinally nilpotent, the series (2.4) converges, and its finite
partial sums telescope to \(d\) at every rung. \(\square\)

## 3. What the single success must be

The theorem separates three finite decisions which must not be conflated.

1. **Exponent-nine pre-gate.**  V216 decides whether the projection of
   \(\bar\epsilon_1\) lies in the projected relative-ideal image.  A pass
   supplies a projected seed only and does not satisfy (2.1).
2. **Pointed first-shadow gate.**  V214/v188 find a multiplier in the actual
   first successor and v191 compiles a finite word-pair representative.
   This fixes the candidate \(M\), but still does not satisfy (2.1).
3. **Three exact PB endpoints.**  Once that same \(M\) satisfies (2.1),
   Theorem 2.1 promotes it through all pro-3 rungs at once.  No second-rung,
   third-rung, or cofinal sequence of independent multiplier searches remains.

Thus the phrase "one successful stage" is valid only for the universal exact
PB endpoint identity, not for one finite quotient screen.

## 4. Certificate extraction and effective construction

For a proof-carrying witness, existence of the chains in (2.2) is followed by
v197 extraction.  A positive certificate retains:

1. the exact task192 words \(g_0,a,f\);
2. the pointed ancestry and the complete finite word-pair polynomial (1.3);
3. all eleven typed occurrence evaluations, signs, prefixes, and the three
   exact zero endpoint collections;
4. three finite relator-decomposition chains \(q_{H1},q_{H2},q_P\) and a
   direct replay of (2.2);
5. the reduction of the same words and chains through every registered map,
   specified once by their natural constructors rather than enumerated rung
   by rung; and
6. the finite partial corrections

   \[
   c_N=-\sum_{r=0}^{N-1}\mu^ra
   \tag{4.1}
   \]

   with their literal word ancestry and all registered nonlinear side gates.

The algebraic compatibility of (4.1) is automatic from the single data set.
What remains nonautomatic is whether every finite partial correction lies in
the allowed nonlinear word domain and whether the same resulting word passes
the later mixed-prime and perfect-core gates.

## 5. Exact claim boundary

Theorem 2.1 closes the relative pro-3 **linear correction** problem after one
exact three-endpoint pass.  It does not prove any of the following:

- that the current actual data pass the exponent-nine, pointed, or exact
  endpoint gates;
- that a bounded search failure is nonexistence;
- that the finite partial products satisfy the nonlinear GT word equations;
- that prime-to-three solvable refinements accept the same word;
- that the remaining field-outer/perfect-core component accepts it; or
- that a fake or Ihara witness has been constructed.

These are later gates on one fixed explicit word, not reasons to repeat the
relative pro-3 multiplier solve at every rung.

## 6. Fixed frontier

\[
\begin{array}{ll}
\text{THREE EXACT ENDPOINTS}\Rightarrow\text{FINITE UNIVERSAL }q_B
 & \text{PAPER PROOF},\\
\text{FINITE WORD-PAIR }M\Rightarrow\mu\in\mathfrak j
 & \text{PAPER PROOF},\\
\text{ONE UNIVERSAL IDENTITY}\Rightarrow\text{ALL PRO-3 RUNGS}
 & \text{PAPER PROOF},\\
\text{RUNG-BY-RUNG MULTIPLIER SELECTION AFTER (2.1)}
 & \text{REMOVED},\\
\text{ACTUAL }M\text{ AND THREE EXACT ENDPOINTS}
 & \text{NOT COMPUTED},\\
\text{ACTUAL }q_B\text{ CERTIFICATE}
 & \text{NOT EXTRACTED},\\
\text{NONLINEAR PARTIAL-CORRECTION GATES}
 & \text{OPEN},\\
\text{MIXED-PRIME / PERFECT-CORE / FAKE / IHARA}
 & \text{OPEN}.
\end{array}
\]

`R07_THREE_EXACT_ENDPOINTS_TO_ALL_PRO3_V228_PAPER_GRADE`

## 7. Dependency audit and milestone boundary

The implication above is a composition of three earlier theorems, not a new
claim that a finite screen is automatically cofinal:

1. v194 Theorem 3.2 converts the **exact** three-block endpoint equality to
   finite PB presentation boundaries;
2. v191 Theorem 2.1 promotes the one retained roof-fibre word-pair polynomial
   and those boundaries through all matched relative pro-3 reductions; and
3. v174 Theorem 2.1 applies the ordered noncommutative Neumann series only
   after the completed pointed equation and its correction-domain/nonlinear
   hypotheses are available.

Thus an A3 exponent-nine pass, an A5 first-shadow multiplier, or an A6
word-pair by itself does not trigger Theorem 2.1.  In the v220 ledger the
load-bearing positive premise is all three milestones of A7.  A8 then extracts
and independently replays the finite boundary certificate required for a
proof-carrying result, while A9 separately records the Neumann construction,
the side gates, and the all-rung descent.  This paper changes none of those
numerators.
