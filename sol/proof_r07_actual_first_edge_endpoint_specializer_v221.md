# R07 actual first-edge endpoint specializer v221

Author: Sol / 2026-08-28

Status: paper interface theorem and replacement contract for the rejected
task219 implementation.  An authenticated exact task192 word and an
authenticated word-independent task198 roof interface determine the eleven
actual occurrence prefixes, occurrence endpoints, three fixed residual
endpoints, and hence v216's single seed without any extra word search.  This
note proves determinacy and the consumer formula; it does not supply the two
positive production receipts and does not assert that the resulting gate is
positive.  No compatible lift, fake certificate, or Ihara witness is declared.
`verified=false`.

## 1. The two authenticated inputs

Put \(k=\mathbf F_3\) and \(F=F(x,y)\).

### 1.1 Actual-word input

The first input is a positive task192
`R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD` receipt carrying the exact
literal word

\[
 f=g_{760}c_{\rm exact}\in F,
\tag{1.1}
\]

together with its complete correction ancestry and direct eleven-occurrence
replay.  It must establish, rather than merely claim,

\[
 \epsilon(f)=(0,0),\qquad
 c_{\rm exact}\in\ker(F\to\Delta_0),
\tag{1.2}
\]

and retain the exact `corrected_word` used by every downstream consumer.  An
`UNKNOWN_RESOURCE`, `UNKNOWN_INPUT`, SELFTEST word, \(g_{760}\) alone, or the
historical core \(\chi_{07}\) is not this input.

### 1.2 Word-independent roof input

The second input is a positive task198 `ROOF_BRIDGE_ISOMORPHISM` receipt and
its pinned executable interface.  It supplies:

1. the ten distinct typed roof coordinates;
2. diagonal reinsertion of the repeated E3 occurrence into eleven literal
   positions;
3. the immutable occurrence ledger

\[
 o=(B(o),\rho_o,\sigma_o,\operatorname{orientation}_o,
       \operatorname{prefixSlots}_o),\qquad o=1,\ldots,11;
\tag{1.3}
\]

4. exact `eval`, `multiply`, `inverse`, `source_section`, `action`, and
   `section_cocycle` entry points;
5. the complete v190 presentation/evaluator contract and source ancestry.

The roof values are ten typed coordinate blobs.  They are not Malcev triples.
The interface fields are `entry_points` and `section_cocycle`; no consumer may
rename them to `bindings` and `cocycle` without an authenticated adapter.

Task198 remains word-independent.  In particular it does **not** serialize
the values of (1.1), the fixed residual, or word-specific ancestry.

### 1.3 Static constructors and quotient maps

The consumer also pins, as code/proof dependencies rather than a third
mathematical oracle,

- v189's ten-to-eleven typed insertion and printed H1/H2/P block order;
- v193's literal A.18 relation and affine-prefix constructors;
- v198's exact endpoint collection convention; and
- v213's canonical occurrence quotients

\[
 PB_{B(o)}\twoheadrightarrow Q_{B(o),1},\qquad
 D_1\cong H_2(9).
\tag{1.4}
\]

If a production task193 receipt is consumed rather than its constructors being
replayed, that receipt and its exact task192-word binding are authenticated as
well.

## 2. Literal specialization before projection

For each block \(B\in\{H1,H2,P\}\), apply the registered relation constructor
to the same literal word \(f\).  Retain every occurrence separately.  Write

\[
 d_o(f)\in k[PB_{B(o)}]^{X_{B(o)}},
 \qquad
 \xi_o(f)=D_{1,B(o)}d_o(f),
\tag{2.1}
\]

for its occurrence chain and endpoint, and write

\[
 e_B(f)\in k[PB_B]^{X_B},
 \qquad
 \epsilon_B(f)=D_{1,B}e_B(f)
\tag{2.2}
\]

for the corrected fixed residual chain and endpoint.

These chains may be retained for the final positive replay, but the first
endpoint decision needs only their literal endpoint words.  In particular,
for a literal Fox word \(r\),

\[
 D_1\delta(r)=\bar r-1,
\tag{2.3}
\]

and for a difference of two literal Fox words the corresponding endpoints
subtract.  Thus (2.1)--(2.2) can be independently recomputed by exact PB word
evaluation without sharing a Fox helper.

Let \(a_o(f)=\rho_o(f)\) be the eleven typed occurrence values obtained by
evaluating the ten coordinates and reinserting the repeated E3 value.  The
printed relation word and `prefixSlots` determine the prefix

\[
 P_o(f)\in PB_{B(o)}.
\tag{2.4}
\]

The product in (2.4) is recomputed in the registered left-to-right convention.
For an inverse occurrence its inverse-word factor is already present in the
literal constructor and orientation.  It must not be replaced by the identity,
and neither its sign nor its inverse factor may be applied twice.

Define the exact specialization package

\[
 \mathcal S_{\rm PB}(f)=
 \bigl(
 (B(o),\rho_o,\sigma_o,P_o(f),\xi_o(f))_{o=1}^{11},
 (\epsilon_B(f))_{B=H1,H2,P}
 \bigr).
\tag{2.5}
\]

## 3. Canonical exponent-nine package

Project (2.5) through (1.4).  Put

\[
 p_o=\overline{P_o(f)},\qquad
 \bar\xi_o=\overline{\xi_o(f)},
\tag{3.1}
\]

and retain the eleven occurrence slots in

\[
 \widehat E_1=\bigoplus_{o=1}^{11}k[Q_{B(o),1}].
\tag{3.2}
\]

Define

\[
 w_o=\sigma_op_o\bar\xi_o,
 \qquad
 w=(w_o)_{o=1}^{11}\in\widehat E_1,
\tag{3.3}
\]

and let

\[
 \bar\epsilon_1=
 (\overline{\epsilon_{H1}(f)},
  \overline{\epsilon_{H2}(f)},
  \overline{\epsilon_P(f)})
 \in E_1^{\rm blk}.
\tag{3.4}
\]

The specialization output is

\[
 \mathcal S_9(f)=
 \bigl(\mathcal S_{\rm PB}(f),w,\bar\epsilon_1,
       \text{literal term provenance}\bigr).
\tag{3.5}
\]

It carries the immutable hashes of both input receipts, the exact word (1.1),
the v189 ledger, the quotient-map tables, and every unreduced term used in
(2.4)--(3.4).

## 4. Determinacy theorem

### Theorem 4.1 (TWO-INPUT ACTUAL SPECIALIZATION)

Under the authenticated inputs and pinned constructors of Section 1, the
packages \(\mathcal S_{\rm PB}(f)\) and \(\mathcal S_9(f)\) are uniquely
determined.  They require no choice of source section, same-roof representative,
pointed multiplier, or boundary coefficient.

For every \(\mu\in k[\Delta_1]\), the exponent-nine projection of the exact
three-block endpoint is

\[
 \boxed{
 \bar\eta_1(\mu)=
 \bar\epsilon_1-C(\mu\odot w),}
\tag{4.1}
\]

where the occurrence-dependent action is applied before the printed block sum
\(C\).  Consequently (3.5) is exactly the actual-data input required by
v214 and v216.

#### Proof

The exact word \(f\), each typed homomorphism \(\rho_o\), and every literal
relation constructor are fixed.  Hence (2.1)--(2.2) are fixed.  The eleven
values \(a_o(f)\) are obtained from the ten typed values by v189's explicit
insertion map, whose inverse deletes only the repeated H2/2 E3 coordinate.
Thus no ambiguity is introduced by the repeated occurrence.

The ledger fixes signs, orientations, and prefix slot lists.  Exact group
multiplication and inversion therefore determine every \(P_o(f)\), proving
uniqueness of (2.5).  The quotient homomorphisms in (1.4) determine
(3.1)--(3.4), proving uniqueness of (3.5).

Finally v198's endpoint collection gives, before projection,

\[
 \epsilon_B(f)-
 \sum_{o\in B}\sigma_oP_o(f)\,\rho_o(M)\,\xi_o(f).
\tag{4.2}
\]

Projecting (4.2) through (1.4) and using v214's occurrence action gives
exactly (4.1).  All choices of a source representative of \(\mu\) disappear
because the occurrence quotients factor through \(\Delta_1\).  No source
section or boundary preimage is used. \(\square\)

### Corollary 4.2 (TASK198 NEEDS NO WORD-SPECIFIC EXTENSION)

Adding `occurrence_values`, `fixed_residual`, or task192 ancestry to the
task198 schema is neither necessary nor type-correct.  These are deterministic
outputs of the specialization map

\[
 (\text{task192 word},\text{task198 interface})
 \longmapsto\mathcal S_9(f).
\tag{4.3}
\]

This keeps the complete roof presentation reusable for every candidate word.

## 5. Single-seed consumer and exact claim boundary

Put

\[
 z=[x,y]^3\in D_1,\qquad R_0=\langle z\rangle\cong C_3.
\tag{5.1}
\]

V216 shows

\[
 I(R_0)=k[D_1](z-1)
\tag{5.2}
\]

and that its complete action on the actual occurrence package is the invariant
closure of the one specialized seed

\[
 u_0=(z-1)\odot w.
\tag{5.3}
\]

Therefore the complete fixed-lower-correction pre-gate is

\[
 \boxed{
 \bar\epsilon_1\in
 C\bigl(\operatorname{OrbSpan}_{x^{\pm1},y^{\pm1}}(u_0)\bigr).}
\tag{5.4}
\]

A separating dual for (5.4) rejects every first multiplier in the relative
ideal for this fixed actual lower correction.  A positive (5.4) supplies only
an exponent-nine coefficient ancestry.  It does not yet prove the pointed
equation, exact PB endpoint zero, nonlinear side gates, later-rung positivity,
mixed-prime membership, or perfect-core membership.

On a pass, the next steps are fixed:

1. use the complete task198 presentation with v188 to construct the actual
   word-bearing successor kernel;
2. use v214 to solve pointed and projected endpoint coordinates jointly;
3. compile its ancestry to the finite word-pair \(M\) by v191;
4. evaluate the three exact PB endpoints from \(\mathcal S_{\rm PB}(f)\) by
   v198; and
5. if all three vanish, extract \(q\) by v197.

## 6. Independent checker obligations

An acceptable implementation has an independent checker which:

1. authenticates the exact positive task192 and task198 receipts before
   importing any producer-owned runtime;
2. parses the task198 `entry_points` ABI literally and treats roof values as
   ten typed blobs;
3. evaluates the exact task192 `corrected_word` in all ten coordinates and
   performs v189 insertion independently;
4. reconstructs all eleven printed prefixes from the relation words, then
   compares them with the ledger's `fox_prefix_occurrences` rather than using
   identities as placeholders;
5. recomputes \(\xi_o\) and \(\epsilon_B\) by literal PB endpoint identities
   and compares them with \(D_1\) of a direct full-\(C_1\) replay on a final
   positive candidate;
6. implements \(H_2(9)\) multiplication and inversion independently, checks
   \(x^{-1}=x^8\), \(y^{-1}=y^8\), \(z=h^3\), \(|D_1|=729\), and
   \(|D_1/\langle z\rangle|=243\);
7. closes the orbit in occurrence space before applying \(C\), retaining exact
   coefficient ancestry or a separating dual; and
8. rejects a mutation of any word, typed coordinate, repeated E3 insertion,
   E3/E4 `C21` type, sign, inverse orientation, prefix slot, factor order,
   quotient map, residual term, or ancestry coefficient.

## 7. Fixed frontier

\[
\begin{array}{ll}
\text{TWO-INPUT DETERMINACY} & \text{PAPER PROOF},\\
\text{WORD-INDEPENDENCE OF TASK198} & \text{PAPER INTERFACE CONSEQUENCE},\\
\text{ACTUAL }(P_o,\xi_o,\epsilon_B) & \text{AWAITING POSITIVE INPUTS},\\
\text{ACTUAL }(w,\bar\epsilon_1,u_0) & \text{NOT COMPUTED},\\
\text{SINGLE-SEED MEMBERSHIP} & \text{NOT RUN},\\
\text{POINTED }\mu_1\text{ AND WORD-PAIR }M & \text{NOT COMPILED},\\
\text{EXACT THREE PB ENDPOINTS} & \text{NOT COMPUTED},\\
\text{COMPATIBLE COFINAL LIFT / FAKE / IHARA} & \text{NOT DECLARED}.
\end{array}
\]

`R07_ACTUAL_FIRST_EDGE_ENDPOINT_SPECIALIZER_V221_PAPER_GRADE`
