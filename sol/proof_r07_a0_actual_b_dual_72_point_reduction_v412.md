# R07 A0 actual block-1 b-dual 72-point reduction (v412)

Author: Sol / 2026-08-31

Status: actual-data specialization of v409--v410 after independently checked
Task435 run `33391325650`.  It proves the exact adjoint and formula universe
for the first physical dual.  It does not yet assert an ACTIVE correction,
A0 membership/nonmembership, a common word, fake, or an Ihara witness.
`verified=false`.

## 1. Cross-checked actual input

Task435 rebuilt the 44 identity compact columns and the complete v404
six-action oracle in both producer and checker.  The accepted profile is

```text
physical rank / payload nnz          43 / 1,813,674
identity compact attempted/retained  44 / 43
v404 candidate / retained            0 / 0
v404 final accumulator               EMPTY
normalized dual support              24
dual keys                             24 x (block 1, label b, 40-byte blob)
tau coefficients                     0,0,0
normalized exponent coefficients     0,0
dual/remainder pairing               1
dual SHA-256                          c75895737537f157fbbfedcdc2c41ed31c8bf0ca9bddda060079ffcda7604efd
```

The profile terminal is informational and promoted no A0 claim.  The key
typing above was independently parsed from all 24 framed quotient keys; the
`support_by_label` field records a coefficient sum, not a key count.

## 2. The quotient adjoint has only three points per key

Fix one PB3 block and use v12's orbit notation

\[
 h=rz^j,\qquad j=0,1,2.
\tag{2.1}
\]

In `contract`, after the triangular elimination, the retained noncentral
coordinate is

\[
 \bar B(r)=\sum_{j=0}^2 B(rz^j).
\tag{2.2}
\]

No central singleton and no other noncentral component contributes to
\(\bar B(r)\).  The central updates made by the triangular elimination affect
only `u0`, `u1`, and `tau`; they do not alter (2.2).

### Lemma 2.1 (LABEL-SPECIFIC ADJOINT)

For the quotient functional \(b(r)^*\),

\[
 \boxed{N^*b(r)^*=\sum_{j=0}^2 e_b(rz^j)^*.}
\tag{2.3}
\]

#### Proof

Pair a raw singleton with (2.2).  It contributes one exactly when it is the
same `b` component at one of the three points in (2.1), and contributes zero
otherwise.  This is precisely (2.3). \(\square\)

Writing the actual dual as

\[
 \lambda=\sum_{r\in S}a_r b(r)^*,\qquad |S|=24,
\tag{2.4}
\]

gives at most

\[
 \boxed{3|S|=72}
\tag{2.5}
\]

candidate new-coordinate adjoint points before duplicate cancellation.  The
uniform v410 bound would be \(15|S|=360\); the fivefold improvement is exact
because the actual dual contains no `u0`, `u1`, `tau`, or second component.

## 3. The old-coordinate adjoint is also explicit

For the first PB3 block, v401/v12's Tietze Fox map is

\[
 \begin{aligned}
 e_a(v)&\longmapsto e_z(v)-e_c(vxy)-e_b(vx),\\
 e_b(v)&\longmapsto e_b(v),\\
 e_c(v)&\longmapsto e_c(v).
 \end{aligned}
\tag{3.1}
\]

Therefore one coefficient \(\mu(h)\) in (2.3) pulls back to

\[
 \boxed{
 J_{\rm T}^*\mu:quad
 e_b(h)^*\mathrel{+}=\mu(h),\qquad
 e_a(hx^{-1})^*\mathrel{-}=\mu(h).}
\tag{3.2}
\]

There is no old-\(c\) term.  Thus the full old-coordinate dual has at most
144 candidate keys before merging.  Every coefficient can be checked without
trusting (3.2) by applying the direct physical transform to the corresponding
old singleton and pairing with \(\lambda\).

## 4. Only three context coordinates remain

Feed (3.2) to the accepted eleven-occurrence correlation formula.  Because
the adjoint is typed block 1, only the three block-1 occurrences contribute:

\[
 H1_{fxy},\qquad H1_{fxz},\qquad H1_{fyz}.
\tag{4.1}
\]

Their linked context coordinates are 0, 1, and 2.  The zero exponent and tau
coefficients give

\[
 \boxed{
 F_i(\delta)=
 \sum_{(j,t)\in R_i}c^{(i)}_{j,t}
 {\bf1}_{\pi_j(\delta)=t},
 \qquad j\in\{0,1,2\}.}
\tag{4.2}

In particular \(K_i=0\) for all at-most-44 compact seeds.  Task176 gives

\[
 |\ker\pi_0|=|\ker\pi_1|=|\ker\pi_2|=9.
\tag{4.3}
\]

Hence v142--v143 decides one formula after at most

\[
 W_i=9\,|R_i|
\tag{4.4}

literal fibre states, with duplicates across coordinates harmless.  There is
no global-prefix branch because \(K_i=0\), and no Q0/Delta scan is needed
until the formula's finitely many singleton targets are known.

### Theorem 4.1 (ACTUAL FIRST-DUAL FINITE ORACLE)

The complete current-dual correction oracle consists of:

1. at most 72 new-coordinate adjoint points;
2. at most 144 old-coordinate adjoint keys;
3. 44 exact formulae supported only on coordinates 0--2; and
4. at most \(W_i\) literal states for seed \(i\).

Complete exhaustion returns either a literal correction pairing nontrivially
with the current dual, or proves that the dual annihilates the entire compact
correction space.  Since v404 is already empty for the same dual, the latter
case is an exact A0 separator.  A resource stop before exhaustion remains
`UNKNOWN_RESOURCE`.

The formula scalar is insensitive to exponent coordinates because the current
dual has zero exponent coefficients.  The **physical column is not**: the
rank test must use v12's normalized coordinates

\[
 N_1=\operatorname{exp}_x/18\pmod 3,\qquad
 N_2=\operatorname{exp}_y/18\pmod 3,
\]

as produced by `seed_v12` and the exact v12 actor replay.  Task179's raw
exponent-modulo-three occurrence row may check the eleven local Fox terms, but
it cannot be substituted for the v12 row in the rank-43 to rank-44 test.

```text
OCCURRENCE CLOSURE:                    NOT USED
CURRENT PHYSICAL RANK:                 43
CURRENT DUAL SUPPORT:                  24 x PB3 BLOCK-1 b
NEW-COORDINATE ADJOINT CANDIDATES:     <= 72
OLD-COORDINATE ADJOINT CANDIDATES:     <= 144
FORMULA COORDINATES:                   0,1,2 ONLY
FORMULA CONSTANTS:                     ALL ZERO
SINGLETON FIBRE SIZE:                  9
ACTUAL ACTIVE/SEPARATOR TERMINAL:      PENDING TASK436
```

`R07_A0_ACTUAL_B_DUAL_72_POINT_REDUCTION_V412_PAPER_GRADE`
