# R07 g760 L3 target6: j=9 survival boundary v105

Author: Sol / 2026-08-27

Status: exact interpretation of immutable producer logs from GHA runs
`32972580814` and `32975492800`.  This is a candidate computation receipt,
not a helper-nonshared cross-check and not a positive lift certificate.
`verified=false`.

## 1. Frozen calculation

The word is the fixed 760-letter commutator word

```text
g760 = w2*(w3^-1*w2)^8*y^36*x^-108
SHA-256 = 518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
free exponent sums = [0,0]
```

The tested coordinate is the first hexagon coface, `target6`, for this one
fixed prefix.  At Jennings depth `j`, the producer forms

\[
 W_j=\operatorname{span}_{\mathbf F_3}
 \bigl(\overline{D_2^{\rm full}}+\overline{L}_{\rm legal}\bigr)
 \subseteq \Lambda/I^j,
\tag{1.1}
\]

where `D2 full` contains the registered 649,539 translated boundary rows and
`L_legal` is the complete C-13 legal-correction **overapproximation**.  It then
reduces the projected target `t_j` against an echelon basis of (1.1).  The
public flag is

\[
 \texttt{nonmember}=(t_j\notin W_j).
\tag{1.2}
\]

Only the implication `nonmember=true => no correction in the actual smaller
domain` is a sound fatal implication.  Its converse is deliberately absent.

## 2. Immutable j=9 result

V3 run `32972580814`, head
`bf9ca644867db43f09f9297cc70bbbca22b00a3f`, completed all eleven j=9
closures.  Its cumulative ranks were

```text
2578, 5075, 7653, 10069, 12371, 14868,
17230, 18739, 19498, 19563, 19621.
```

It then emitted exactly

```text
R07_760_L3_TARGET6_RELATOR_RESUME_V3_J_CHECKPOINT
j=9 nonmember=false
sha256=34a76f296e4e2fb92e1a892fd0a679e60991cd12a1381e5ac0c2d980f7c8138e
bytes=18067
```

V4 run `32975492800`, head
`73efbdb8345d4fa2802d6e948b6e7cd43897369a`, independently serialized the
same eleven closure increments as append-only deltas and reached the same
terminal rank 19,621.  Its final state commitment was

```text
2ebc7d5adc1842db2d1b9db600b52a9d0604118c1bd2c70897d6783167b3ef02
```

V4 then hit an operational post-closure bug: its wrapper called the pinned v3
validator without the required v2 module argument.  Its GAP driver separately
misread a legitimate duplicate JSON field as an envelope failure.  Neither
failure changes the eleven closure ranks or the v3 j=9 decision.  Because both
workflows skipped artifact upload, the evidence retained here is immutable
GHA log evidence, not a downloadable/replayable terminal artifact.

### Proposition 2.1 (EXACT SCOPE OF THE SURVIVAL)

Within the frozen producer model,

\[
 \boxed{t_9\in W_9.}
\tag{2.1}
\]

Consequently the j=9 L3 NONMEMBER obstruction does not kill g760.

#### Proof

The v3 implementation clones the full-D2 echelon, inserts every legal
overapproximation vector, and reduces `target_vector`.  It sets `nonmember`
to true exactly when a pivot remains.  The completed public row reports
`nonmember=false`; hence the remainder is zero, which is (2.1).  V4's equal
closure-rank trajectory is a serialization/control-flow convergence check,
not a helper-independent proof of the positive statement. \(\square\)

## 3. Why this is not yet an explicit lift

Let `C_actual` be the actual common-word correction domain for the two
hexagons, printed-order A.18, syzygies, commutator condition, and all side
gates.  The fatal screen replaces its image by a larger registered space:

\[
 D(C_{\rm actual})\subseteq W_j.
\tag{3.1}
\]

Equation (2.1) is membership in the right-hand side.  It neither supplies a
coefficient vector in `C_actual` nor proves membership in the left-hand side.
It therefore does not construct a B3/B4 lift, compatible cofinal family,
fake, or Ihara witness.

Depths `j=10,11,12` are useful stronger fatal screens.  Survival at all four
depths would remove these registered finite obstructions, but it still would
not reverse (3.1).  Positive promotion requires an actual-domain certificate:

1. serialize coefficients for one common-word correction;
2. replay the exact two hexagons and printed-order A.18, not merely target6;
3. replay every syzygy and side gate defining `C_actual`;
4. bind the correction to the g760 prefix and the correct fine edge;
5. prove refinement compatibility before taking the cofinal inverse limit.

Equivalently in v103--v104 language, one must construct the actual affine
residual torsor and materialize zero of its complete residual, rather than
solve only in the L3 overapproximation.

## 4. Current continuation point

V3 continued at j=10 and completed relators 1 through 7 before the six-hour
workflow limit.  The recorded ranks were

```text
4418, 8653, 13071, 17123, 20989, 25224, 29143.
```

No j=10 terminal decision exists.  The immediate computational continuation
is therefore exact resume at j=10 relator 8 after a versioned artifact-safe
checkpoint run.  In parallel, the positive branch begins with extraction of
an actual-domain coefficient/proof replay; it does not wait for a fictional
implication `MEMBER => lift`.

## 5. Fixed ledger

```text
g760 j=9 full-D2 final rank:                 19621 (producer log)
g760 j=9 L3 decision:                        nonmember=false
g760 j=9 fatal obstruction:                  SURVIVED
helper-nonshared positive cross-check:       NOT PERFORMED
j=10 closure progress:                       relators 1..7, rank 29143
j=10 terminal:                               UNKNOWN
actual common-word coefficient vector:       NOT EXTRACTED
complete literal A.18/hexagon replay:         NOT PERFORMED
compatible cofinal lift:                     NOT CONSTRUCTED
fake / Ihara witness:                        NOT DECLARED
```
