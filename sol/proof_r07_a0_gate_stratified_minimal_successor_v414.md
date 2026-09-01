# R07 A0 gate-stratified minimal successor (v414)

Author: Sol / 2026-09-01

Status: paper implementation corollary to v410--v413.  It proves that the
actor-adapted PB3 rebase is required only for the nonzero-`tau` terminal of
the running v3 ladder.  The other three typed terminals can be completed in
the current quotient, and the present zero-constant exhaustion has already
enumerated the whole support in the producer.  No actual A0 terminal, common
word, compatible lift, fake, or Ihara witness is asserted.  `verified=false`.

## 1. The order of the v3 gates is mathematical information

At a nonzero remainder the running producer performs the following tests in
this order:

1. exhaust the six action families against the current dual;
2. stop if one of the three physical `tau` coefficients is nonzero;
3. otherwise construct the exact v410 adjoint and all 44 formulae;
4. stop if a formula uses a context coordinate outside 0--2;
5. stop if a normalized-exponent constant is nonzero; and
6. run the complete order-nine singleton-fibre selector on coordinates 0--2.

Consequently every terminal after step 2 carries the proved hypothesis

\[
 \lambda_{\tau,1}=\lambda_{\tau,2}=\lambda_{\tau,3}=0.
\tag{1.1}
\]

For such a dual v410 applies to the present least-serialization PB3
transversal.  No coordinate change is involved: its sparse adjoint and the
resulting indicator formula are already the exact pairing with the current
physical rows.

### Proposition 1.1 (GATE-STRATIFIED REBASE)

The actor-adapted replay of v413 is necessary only after
`NONZERO_TAU_PHASE_SELECTOR`.  It is not a prerequisite for

```text
SELECTOR_COORDINATES:S3...S9
NONZERO_CONSTANT_SELECTOR
SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION.
```

#### Proof

The first terminal is precisely the case excluded from v410 and handled by
v411--v413.  Each later terminal is reached only under (1.1), where v410
proves the current-coordinate adjoint without any multiplicative splitting
of the PB3 transversal.  Therefore changing coordinates before completing a
later branch is unnecessary. \(\square\)

This proposition is an implementation restriction: a successor must branch
on the authenticated terminal and must not pay for a 44-row actor-adapted
rebuild on the three tau-free branches.

## 2. Contexts 3--9 need only one live Q0 coordinate store

For a formula

\[
 F_i(\delta)=K_i+\sum_{(j,t)\in R_i}c_{j,t}
                  {\bf1}_{\pi_j(\delta)=t},
\tag{2.1}
\]

fix one coordinate \(j\).  The authenticated singleton section supplies
either no preimage of \(t\), or a literal state \(s_j(t)\).  The complete
fibre is

\[
 \pi_j^{-1}(t)=\{\eta s_j(t):\eta\in\ker\pi_j\},
\tag{2.2}
\]

and the already authenticated kernel orders are

\[
 (9,9,9,9,9,1,1,1,3,3).
\tag{2.3}
\]

Thus a successor may build only the Q0 packed store, inverse index, `A_map`,
and kernel roster for the current \(j\).  Each returned literal word is
replayed through all ten coordinates before (2.1) is evaluated.  After all
targets with that \(j\) are exhausted, the coordinate-specific store and
index may be released before proceeding to the next \(j\).  The shared Q0
state/parent/letter roster is retained once.

### Proposition 2.1 (ONE-COORDINATE EXACTNESS)

The sequential one-coordinate procedure evaluates every state in the support
union of (2.1).  It gives the same positive-or-exhausted answer as an eager
ten-store construction.

#### Proof

Equation (2.2) is a complete fibre, not a sample.  Taking its union over all
distinct \((j,t)\in R_i\) is exactly the indicator support of (2.1).
Replaying the literal word supplies the other nine coordinates, so evaluation
does not require their packed stores.  Processing the finite union in another
order cannot change whether a nonzero value occurs. \(\square\)

Exact full-coordinate tuple bytes, or a digest index followed by byte
equality, are used for deduplication.  A digest match alone is not a proof of
state equality.  A resource stop remains `UNKNOWN_RESOURCE`.

## 3. A nonzero exponent constant needs no phase split

Under (1.1), the constant compiled by v3 is

\[
 K_i=n_1\frac{\operatorname{exp}_x(r_i)}{18}
     +n_2\frac{\operatorname{exp}_y(r_i)}{18}\pmod3.
\tag{3.1}
\]

Conjugation does not change exponent sums, so \(K_i\) is the same on all of
\(\Delta\).  Let

\[
 W_i=\sum_{(j,t)\in R_i}|\ker\pi_j|.
\tag{3.2}
\]

After the finite support fibres are evaluated, if \(K_i\ne0\) and
\(W_i<|\Delta|\), any \(W_i+1\) distinct entries of the authenticated global
roster contain a point outside the support union, where the value is
\(K_i\ne0\).  If the union bound is not smaller than \(|\Delta|\), exact
full-tuple deduplication gives \(|U_i|\); either the support evaluation was
already exhaustive, or the first \(|U_i|+1\) global states contain an outside
point.

Therefore `NONZERO_CONSTANT_SELECTOR` uses the existing global roster with
factor one.  The factor-three phase normalization of v413 is needed only when
nonzero `tau` makes the constant depend on
`exp_x mod 3`.

## 4. The present zero-constant exhaustion is already complete

Suppose v3 reaches
`SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION`.  By the preceding gate order:

\[
 \lambda_\tau=0,\qquad R_i\subseteq\{0,1,2\},\qquad K_i=0
\tag{4.1}
\]

for every compiled seed.  The selective runtime authenticates order nine for
each of the three kernels.  For every merged target, `canonical` returns an
exact singleton section or proves that the target has empty fibre, and
`ensure_kernel_prefix(j,9)` enumerates the complete kernel.  Hence a `None`
return from `weighted_hit` means that the producer evaluated all points of
every support fibre and obtained zero.  Outside those fibres (4.1) makes the
formula zero as well.

### Theorem 4.1 (ZERO-CONSTANT PRODUCER SEPARATOR)

If the six-action oracle is empty and the v3 weighted selector returns no
hit after reaching (4.1), the current dual annihilates the full A0 action plus
compact-correction space.  The remaining work is a versioned negative
certificate and an independent reconstruction of the same finite
exhaustion; no further producer search and no actor-adapted rebuild are
mathematically required.

#### Proof

The action part is empty by the complete action oracle.  Sections 2 and 4.1
show that `weighted_hit` evaluates the whole support of every compact formula.
Every evaluated value is zero, and every value outside the support is the
zero constant.  Thus every compact conjugate pairs to zero with the same
nonzero separating dual. \(\square\)

## 5. Minimal successor table

```text
NONZERO_TAU_PHASE_SELECTOR:
    actor-adapted word-bearing rebuild, then v413 phase selector
SELECTOR_COORDINATES:S3...S9:
    current quotient; lazy required-coordinate stores only
NONZERO_CONSTANT_SELECTOR:
    current quotient; exact support plus factor-one global prefix
SEPARATOR_REQUIRES_INDEPENDENT_EXHAUSTION:
    current producer exhaustion is complete; add independent negative replay
TIME/RSS/MAX-RISE RESOURCE:
    resume or optimize the named phase; infer no mathematical terminal
```

`R07_A0_GATE_STRATIFIED_MINIMAL_SUCCESSOR_V414_PAPER_GRADE`
