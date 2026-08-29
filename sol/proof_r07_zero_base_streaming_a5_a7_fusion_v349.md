# R07 zero-base streaming A5/A7 fusion

Date: 2026-08-29

Status: paper specialization of v309 using the cross-checked zero A3 base
and the streaming closure of v348.  No actual endpoint terminal is asserted.

## 1. Zero-base augmented columns

In v309 set

\[
 \kappa_0=0,\qquad M_0=0,
\tag{1.1}
\]

as supplied by the actual A3 zero result.  For one fixed accepted A0 word
and its task193 replay, retain

\[
 e_1=e_1(c),\qquad
 \eta_c=\widetilde D_1\widetilde e_c
\tag{1.2}
\]

with v309's signs and seven separately typed exact PB contexts.

Every accepted pre-`C` closure row has literal ancestry

\[
 v_j=(\theta_jd_1,\theta_j\mathbin\odot w),
 \qquad
 P_j=\sum_{i,A}a_{j,i,A}(Au_i-A),
\tag{1.3}
\]

where the first-shadow image of `P_j` is `theta_j`.  Define

\[
 U(P_j)=\widetilde D_1(P_j\widetilde d)
\tag{1.4}
\]

by literal action and exact PB normal forms, and define the augmented image

\[
 T_7(v_j)=
 (\theta_jd_1, C(\theta_j\mathbin\odot w), U(P_j)).
\tag{1.5}
\]

No finite-shadow value is substituted for the third coordinate.

## 2. Fused positive criterion

**Theorem 2.1 (ZERO-BASE STREAMING A5/A7 FUSION).**  A finite combination
of the currently generated canonical pair rows supplies simultaneously an
A5 multiplier, its literal A6 polynomial, and exact A7 endpoint zero if and
only if

\[
 \boxed{
   (e_1,0,\eta_c)\in
   \operatorname{span}\{T_7(v_j)\}.}
\tag{2.1}
\]

If

\[
 (e_1,0,\eta_c)=\sum_jq_jT_7(v_j),
\tag{2.2}
\]

then

\[
 \theta=\sum_jq_j\theta_j,qquad
 M=\sum_jq_jP_j
\tag{2.3}

satisfy

\[
 \boxed{
   \theta d_1=e_1,qquad
   \Phi(\theta)=0,qquad
   \widetilde D_1(\widetilde e_c-M\widetilde d)=0.}
\tag{2.4}

Thus `mu1=theta`, and the same finite ancestry is both the A6 pair
polynomial and the A7 zero certificate.

**Proof.**  The first two coordinates of (2.2) are v348 Theorem 2.1 and give
`theta*d1=e1` and `theta in H`.  Literal first-shadow replay of (1.3) gives
the first statement in (2.3).  Linearity and equivariance of the exact
universal boundary give

\[
 \sum_jq_jU(P_j)=\widetilde D_1(M\widetilde d).
\]

The third coordinate of (2.2) is therefore exactly the last equality in
(2.4).  The converse reverses these three coordinate equalities.  QED.

By v309/v193/v191, a positive (2.2), followed by constructive relator
decomposition, promotes this same literal `M` through every relative pro-3
rung, subject to the separately registered nonlinear and formation gates.

## 3. Witness-first streaming schedule

Keep the pre-`C` closure echelon `E_pre` and action queue exactly as in v348.
For each newly accepted pre-`C` row, independently construct its literal
`P_j` and insert both

```text
A5 column:       (theta_j*d1, C(theta_j odot w))
A5/A7 column:    (theta_j*d1, C(theta_j odot w), U(P_j))
```

into separate ancestry-bearing echelons.  Reduce respectively the targets

```text
(e1,0)          and          (e1,0,eta_c).
```

The preferred terminal is the first augmented zero remainder.  It is sound
before closure exhaustion because (2.2) is already a finite exact witness.
An early A5-only zero may be recorded, but the witness-oriented search must
continue: a later canonical row may turn it into an augmented zero.

At full `E_pre` exhaustion there are three distinct outcomes.

1. Augmented MEMBER: A5, A6 and the three exact A7 endpoint zeros have one
   common finite certificate.
2. A5 MEMBER but augmented nonmember for the canonical representatives:
   retain one canonical `M_can` and invoke v310's Schreier lift-kernel repair.
   This is not A7 NONZERO over all representatives.
3. A5 NONMEMBER with a complete joint dual: this particular literal A0 word
   has no pointed multiplier; move to v346's projected-kernel coset or the
   next literal ancestry.

## 4. Finite-seed representative repair is part of the same augmented echelon

Let `n_i` be v310's finite Schreier roster for the kernel of the common
source map to `Delta1`, and let

\[
 \zeta_i=\widetilde D_1((n_i-1)\widetilde d).
\]

Every translated lift-null pair contributes the augmented column

\[
 (0,0,V\zeta_i).
\tag{4.1}
\]

These columns may be dovetailed with the canonical rows from the beginning.
Any finite augmented equality is sound immediately.  Fair translation of
the finite Schreier seeds is positive-complete for finite-support
representative repair.  Since this orbit is generally infinite, a bounded
no-hit is `UNKNOWN_RESOURCE`, never a complete A7 negative.

## 5. Checker boundary

A positive checker replays only the finite data actually used:

1. the A0/task193 literal word and `e1,eta_c`;
2. every selected A4 seed, marked prefix and literal pair `Au_i-A`;
3. both finite coordinates and every exact PB endpoint coordinate;
4. equation (2.2), the collected `theta` and literal `M`;
5. all three equalities in (2.4); and
6. the constructive universal relator decomposition before any all-rung
   promotion claim.

It need not replay unused closure or Schreier branches for a positive
certificate.  It must not treat finite canonical augmented failure as an
all-representative negative.

```text
ZERO-BASE A5/A7 AUGMENTED IDENTITY:         PAPER PROOF
EARLY POSITIVE STREAMING CERTIFICATE:       PAPER PROOF
SAME ANCESTRY GIVES MU1 AND LITERAL M:       PAPER PROOF
FINITE-SUPPORT REPRESENTATIVE REPAIR:       POSITIVE-COMPLETE / v310
ACTUAL AUGMENTED MEMBER:                     NOT YET COMPUTED
FORMATION / PERFECT-CORE / COMPLETE LIFT:    OPEN
FAKE / IHARA WITNESS:                       NONE
```

`R07_ZERO_BASE_STREAMING_A5_A7_FUSION_V349_PAPER_GRADE`

