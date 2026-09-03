# R07: adjoint Fox replay of a selected SLP (v467)

Author: Sol / 2026-09-03

Status: candidate constructive theorem.  It supplies the missing bounded
evaluation bridge from the selected grade-one SLP of v465--v466 to the exact
eleven-occurrence replay and the fresh grade-two residual required by v451.
It preserves the ordered SLP as the witness, but computes its Fox image by a
reverse coefficient pass through the authenticated elimination DAG.  It does
not promote Task595, decide grade two, prove cofinal surjectivity, or declare
A0, COMMON, fake, or Ihara.  `verified=false`.

## 1. Exact Fox-pair evaluator

Let (F=F(x,y)), let (eta:F\to Q) be one registered marked finite
quotient, and let (R=k[Q]), or one of the exact truncated rings of v443.
For a word (w), put

\[
 \Phi_\eta(w)=(\eta(w),D_\eta(w)),\qquad
 D_\eta(w)=
 \left(\eta\frac{\partial w}{\partial x},
       \eta\frac{\partial w}{\partial y}\right)\in R^2.       \tag{1.1}
\]

On (Q\times R^2), define

\[
 (g,u)\odot(h,v)=(gh,u+g v),\qquad
 (g,u)^{-1}=(g^{-1},-g^{-1}u).                    \tag{1.2}
\]

The Fox product and inverse rules say exactly that

\[
 \Phi_\eta(uv)=\Phi_\eta(u)\odot\Phi_\eta(v),
 \qquad \Phi_\eta(u^{-1})=\Phi_\eta(u)^{-1}.       \tag{1.3}
\]

Thus every typed leaf, ordered product, inverse and literal actor conjugation
in v465 has an exact compositional evaluator.  Memoized evaluation of the
ordered SLP is equal to evaluation of its unexpanded free word.  No
commutation or collection hypothesis is used in (1.1)--(1.3).

For each registered occurrence, the same syntax is evaluated after that
occurrence's exact substitution, actor path, prefix and inverse convention.
The coefficient arithmetic in (R) is supplied by v443 (2.4), (3.1)--(3.2)
at the first rung.  Hence this statement does not introduce a common action
on the physically aggregated module.

## 2. Identity-endpoint linearization

Let (N=\ker\eta).  Restricting (1.3) to (N) gives

\[
 D_\eta(uv)=D_\eta(u)+D_\eta(v),\qquad
 D_\eta(u^{-1})=-D_\eta(u) \quad (u,v\in N).        \tag{2.1}
\]

Therefore (D_\eta|_N:N\to R^2) is a group homomorphism to the additive
group.  In the R07 finite-rung calculation, every compact seed is required
by the certificate gate to be a literal identity in the current marked
quotient.  Every actor conjugate, transition defect, echelon combination and
selected correction built from these seeds consequently lies in (N).

Equation (2.1) licenses linear arithmetic for the *evaluation* of the Fox
image over (k=\mathbf F_3).  It does not license changing the stored SLP,
sorting factors, deleting syntactically cancelling branches, or assuming
that the same leaves are identities in a finer quotient.  The ordered SLP
remains the explicit witness used by later quotients.

The endpoint premise is executable, not inferred from a type label.  A
direct replay must evaluate every reached literal seed under every registered
substitution and assert endpoint one before using (2.1).  Normalized exponent
and all integral side coordinates are checked separately before reduction
modulo three.

## 3. Reverse coefficient theorem

Use the v466 accepted-node convention

\[
 b_j=\sigma_j\left(z_{o(j)}-\sum_{p<j}q_{jp}b_p\right),
 \qquad \sigma_j\in\{1,2\}.                         \tag{3.1}
\]

Suppose the selected update has root coefficients (a_j\in k).  Initialize
(lambda_j=a_j), initialize every origin weight (mu_o=0), and visit
(j=r-1,r-2,\ldots,0).  At node (j), perform

\[
 \mu_{o(j)}\mathrel{+}=\sigma_j\lambda_j,
 \qquad
 \lambda_p\mathrel{+}=-\sigma_j\lambda_jq_{jp}
       \quad\text{for every recorded }(p,q_{jp}).   \tag{3.2}
\]

All operations in (3.2) are in (k).  Apply the same rule through the
reached lower-owner DAG and then through the reached block/old source DAGs.

### Theorem 3.1 (adjoint selected replay)

If the compact transcripts are authenticated and every edge points to an
earlier pivot, then

\[
 \boxed{\sum_j a_j b_j=\sum_o\mu_o z_o}.            \tag{3.3}
\]

The right side uses exactly the reached literal origins of the selected SLP.

#### Proof

At step (j), substitute (3.1) for the current coefficient
(lambda_jb_j).  The first assignment in (3.2) records the resulting
origin coefficient and the second assignments record its coefficients on
earlier pivots.  No later pivot is introduced, so descending induction
preserves the represented vector and terminates with no pivot terms.  This
proves (3.3).  Repeating the identical substitution in each parent DAG proves
the final origin statement.  \(\square\)

The pass is the transpose, or adjoint, of the deterministic elimination
transcript; it is not a second search.  It also gives an exact receipt:
forward reduction of the resulting origin weights must reproduce the 3,317
Task595 root coefficients and the zero target remainder.

## 4. Direct eleven-occurrence replay without flat expansion

Keep the canonical ordered SLP roots (C_T,C_{<1},C_1) from v465.  To
evaluate the selected update at precision two:

1. authenticate the roots, selected transcript and all reached origins;
2. run (3.2) without altering the SLP payload;
3. evaluate every reached weighted literal origin at precision two in all
   eleven registered occurrences, using the v443 affine/Fox arithmetic;
4. add those rows with their weights (mu_o); and
5. apply the pinned PB3 map, fixed prefixes, signed physical aggregation,
   boundary quotient and auxiliary-coordinate maps in their registered order.

Every map in step 5 is linear on the Fox row.  Hence (2.1) and (3.3) prove
that the accumulated result is exactly the Fox image of the original ordered
(C_T) at this quotient.  The prior root (C_{<1}) is handled by its own
authenticated term list; adding its image gives the image of (C_1), after
direct endpoint-one checks.  This shortcut is legal for the row evaluation
only.  The source word exported as the witness is still the unmodified
ordered root (C_1=\operatorname{Compose}(C_{<1},C_T)).

The implementation need retain only the compact node/edge tables, scalar
weights and one running packed row per active occurrence/component.  It need
not keep one full group-algebra row for every selected SLP node.  Runtime is
linear in the selected edge count plus the cost of evaluating the reached
literal origins; peak storage has no factor equal to the number of SLP nodes
times the ambient row width.

## 5. Exact grade-two join

Let (T_{\le2}) be the authenticated target and let
(A_{\le2}(C_1)) be the result of Section 4.  The consumer first checks:

1. every reached literal endpoint is one in the current marked quotient;
2. the exact grade-one MEMBER equality and all normalized-exponent, PB3,
   boundary and auxiliary lower coordinates;
3. equality between the adjoint result and an independent general Fox-pair
   evaluation on bounded nontrivial SLP fixtures; and
4. the complete precision-one target equation for (C_1).

Only after all lower coordinates vanish may it define

\[
 \rho_2=\operatorname{gr}_2
       \left(T_{\le2}-A_{\le2}(C_1)\right).          \tag{5.1}
\]

Equation (5.1) is the fresh result-dependent input to the target-independent
grade-two fibre of v451.  It is not copied from Task595, because two literal
representatives with the same grade-one class can have different grade-two
residuals.  A MEMBER result at grade two then appends another authenticated
ordered SLP update; a NONMEMBER result requires a dual on the complete
grade-two fibre.

## 6. Certificate and claim boundary

An accepted consumer binds the Task595 decision, prepare/four-block digests,
selected-SLP manifest, exact endpoint checks, reverse-weight digest, complete
precision-two replay receipt and fresh residual digest.  A second
implementation can check the small SLP parser and Fox-pair laws and replay the
final equality without reproducing discovery pivots.

```text
GENERAL ORDERED SLP -> EXACT FOX PAIR:       PAPER-CLOSED
IDENTITY-ENDPOINT SLP -> ADDITIVE FOX ROW:   PAPER-CLOSED; ENDPOINTS MUST REPLAY
REVERSE TRANSCRIPT -> ORIGIN WEIGHTS:        PAPER-CLOSED
NO FLAT WORD / NO ROW PER SLP NODE:          PROVED FOR CURRENT-QUOTIENT REPLAY
ACTUAL SELECTED SLP / ELEVEN-OCCURRENCE RUN: NOT YET PRODUCED
FRESH GRADE-TWO RESIDUAL:                    NOT YET COMPUTED
FIRST RUNG / A0 / COMMON / COFINAL LIFT:     NOT DECLARED
FAKE / IHARA:                                NOT DECLARED
verified:                                    false
```

`R07_SELECTED_SLP_ADJOINT_FOX_REPLAY_V467_CANDIDATE`
