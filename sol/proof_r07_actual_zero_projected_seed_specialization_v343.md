# R07 actual zero projected-seed specialization (v343)

## 0. Scope and computational input

This note records the mathematical consequence of the independently agreeing
actual A3 run `33244921126` at immutable head
`b458a49c2e7ad10fdc86a619d4e48f32099b37b4`.  The producer receipt has
schema `d972-r07-pre-a0-single-target-a3/v6/receipt/v1`, terminal
`R07_PRE_A0_A3_PROJECTED_MEMBER`, and self digest
`a3f452074bf1e722591949372ae2b16c4d9fed0a2a5cba26a7eba58c7b30b43e`.
The independent verdict has the same terminal, `accepted=true`,
`independent=true`, and self digest
`71f239868b46989b12289baa9acae73ecd19701b6b0a7dd33107527f33aa4b7e`.
Both self digests replay from canonical bodies.

The independently reconstructed closure has 486 ideal rows, 729 actor
translates, occurrence rank 243, block rank 243, and an exhausted queue.  Its
positive certificate is the zero certificate:

\[
 \beta=0,\qquad c_i=0,\qquad \lambda=0,\qquad \kappa_D=0,
\tag{0.1}
\]

where the physical receipt represents each zero sparse vector by the empty
list.  The block and quotient remainders are also empty.  This is a
cross-checked finite computation, not a Lean verification and not a claim
about a cofinal lift, fake, or Ihara witness.

## 1. Zero-seed lemma

Retain the notation of v303--v306.  For every registered A0 correction
\(a\in\Omega\), v303 identifies the projected target and action with the
computational-base data.  Hence the actual equality \(\beta=0\) implies

\[
 \bar\epsilon_1(g_{760}a)=0.
\tag{1.1}
\]

Define the literal relative-ideal coefficient

\[
 \boxed{\kappa_0:=0.}
\tag{1.2}
\]

Then, without selecting a word-bearing generator of the A4 kernel,

\[
 \kappa_0\in
 \ker\bigl(\mathbf F_3[\Delta_1]\to\mathbf F_3[\Delta_0]\bigr),
 \qquad
 \Phi_a(\kappa_0)=0=\bar\epsilon_1(g_{760}a)
 \quad(a\in\Omega).
\tag{1.3}
\]

Indeed, zero belongs to every ideal and every linear endpoint map sends zero
to zero.  Equation (1.1) supplies the required target equality.  The empty
linear combination is already a canonical literal word-bearing expression,
so v305's nonzero projected-generator anchor \(u_*\) is unnecessary for this
actual class.

## 2. Exact dependency reduction

Only the *base-point literalization* part of the A4 dependency disappears.
The homogeneous pointed slice remains

\[
 H=\ker\Phi,\qquad S=Hd_1,
\tag{2.1}
\]

and the v306 joint selector still needs an accepted A4 invariant closure with
word ancestry in order to construct and replay a basis of \(S\).  With
\(\kappa_0=0\), however, its target simplifies from
\((1-\kappa_0)d_1\) to

\[
 \boxed{r_*=d_1.}
\tag{2.2}
\]

Thus the remaining positive cone is

\[
 \boxed{
 \text{A4 homogeneous word-bearing closure}
 +\text{joint A0 pointed rows}
 \longrightarrow \text{A5 membership and }\mu_1.}
\tag{2.3}
\]

No A4 \(z_0\)-anchor construction and no A2 specialization is needed to
form this actual A5 base point.  A2 remains required later wherever the full
corrected-word package or exact PB chains are consumed.

## 3. Fixed frontier

```text
ACTUAL PROJECTED A3 PACKAGE / 486+729 CLOSURE: CROSS-CHECKED
ACTUAL A3 TERMINAL:                              MEMBER
ACTUAL TARGET / LAMBDA / KAPPA_D:                ZERO / ZERO / ZERO
ALL-A0 LITERAL ENDPOINT BASE KAPPA0:              ZERO, PAPER CONSEQUENCE
A4 z0-ANCHOR FOR THIS BASE POINT:                 BYPASSED
A4 HOMOGENEOUS WORD-BEARING CLOSURE:              STILL REQUIRED
A5 / MU1 / EXACT PB / COFINAL LIFT / FAKE:        NOT YET ESTABLISHED
IHARA WITNESS:                                    NOT YET ESTABLISHED
```

`R07_ACTUAL_ZERO_PROJECTED_SEED_SPECIALIZATION_V343_PAPER_GRADE`
