# R07 actual zero-seed nonlinear-selector erratum (v344)

## 0. Exact correction to v343

V343 Section 1 is retained: actual run `33244921126` independently
cross-checks the projected A3 target and its MEMBER coefficient as zero, so
the canonical literal endpoint base is

\[
 \kappa_0=0.
\tag{0.1}
\]

In particular the nonzero A4 projected-generator anchor of v305 is not needed
to literalize this base point.

V343 Section 2 referred to the "v306 joint selector."  That attribution is
wrong because v307 already retracted v306's asserted linear factorization of
the task193 row.  Nothing in the zero A3 computation restores that false
linearity.  This note supersedes v343 Section 2 and gives the correct
nonlinear consequence.

## 1. Correct pointwise specialization

Let an accepted A4 closure supply

\[
 H=\ker\Phi,
 \qquad S=Hd_1,
 \qquad d_1=-\mathscr D_1(g_{760}).
\tag{1.1}
\]

For one literal registered A0 word \(c\), retain v307's full task193 direct
change

\[
 \mathscr B(c)=
 \mathscr D_1(g_{760}c)-\mathscr D_1(g_{760}),
\tag{1.2}
\]

computed with all affine prefixes and occurrence data.  Since the actual base
is (0.1), v307's target becomes

\[
 r_*=(1-\kappa_0)d_1=d_1.
\tag{1.3}
\]

Therefore the exact pointwise criterion is

\[
 \boxed{d_1-\mathscr B(c)\in S.}
\tag{1.4}
\]

If an accepted membership ancestry gives

\[
 d_1-\mathscr B(c)=\theta d_1,
 \qquad \theta\in H,
\tag{1.5}
\]

then the pointed multiplier simplifies to

\[
 \boxed{\mu_1=\theta.}
\tag{1.6}
\]

This uses no linearity of \(c\mapsto\mathscr B(c)\).

## 2. Correct simultaneous selector

V308 supplies the complete finite nonlinear state closure
\(\mathcal C\), with A0 map \(\pi_0\), target \(\tau_0\), and full next-rung
affine occurrence component \(q\).  Substituting (0.1) into v308 Theorem 4.1
gives the exact actual-class decision:

\[
 \boxed{
 \exists h=(v,q,e)\in\mathcal C:\quad
 \pi_0(h)=\tau_0,
 \qquad d_1-\mathscr B(q)\in S.}
\tag{2.1}
\]

This is a finite-state normal-closure problem, not the rejected v306 vector-
space membership.  A positive state constructs a literal A0 word and the
multiplier (1.6).  Alternatively, the active standalone A0 solver may return
one literal word first, after which (1.4) is the exact test.

## 3. Dependency frontier

The zero computation removes two operations from this actual branch:

1. constructing a nonzero projected A3 correction; and
2. constructing an A4 \(z_0\)-anchor merely to literalize that correction.

It does not remove:

1. the accepted A4 homogeneous word-bearing closure needed for \(S\);
2. a literal A0 word with full task193 affine-prefix replay, or equivalently
   the complete v308 nonlinear state closure;
3. A5 membership ancestry, exact PB endpoints, or later all-rung gates.

```text
V343 ZERO-SEED LEMMA:                         RETAINED
V343 REFERENCE TO V306 JOINT SELECTOR:        RETRACTED
ACTUAL A5 TARGET:                             d1 - B(c)
POINTWISE A5 TEST:                            d1 - B(c) in H d1
SIMULTANEOUS A0/A5 TEST:                      V308 FINITE NONLINEAR CLOSURE
A4 HOMOGENEOUS CLOSURE / A0 WORD / MU1:       NOT YET COMPUTED
COFINAL LIFT / FAKE / IHARA WITNESS:          NOT YET ESTABLISHED
```

`R07_ACTUAL_ZERO_SEED_NONLINEAR_SELECTOR_ERRATUM_V344_PAPER_GRADE`
